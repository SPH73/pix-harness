#!/usr/bin/env python3
"""The skill-trigger eval runner.

Reads `cases.tsv`, reads a FIELD of candidate skills (every `*/SKILL.md` under a
directory, frontmatter only), asks a scorer which skill each phrasing should fire, and
reports precision and recall per subject skill.

Two arms, chosen with --arm:

  deterministic   Lexical. No model, no key, no network. Each phrasing is scored
                  against each description by IDF-weighted word overlap; a phrasing
                  that appears verbatim inside a description scores 1.0. Below
                  --threshold the answer is NONE. It is a baseline, and it is named as
                  one in every results file: a case lifted verbatim from a description
                  is trivially found by it. Its value is on the paraphrased and the
                  confusable cases, and on the field: does ANOTHER description also
                  claim the phrase?
  model           Claude picks from the field. Needs the eval-only key, read from
                  ANTHROPIC_API_KEY or from ~/.config/pix-harness/.env, which is never
                  printed. The model and the date go into the results file, because a
                  figure without them is worthless in a month.

The CANARY. Any case whose id starts with `canary-` is built to be scored wrong. The
runner asserts it IS scored wrong and exits 3 if it is not. A suite that cannot fail
certifies nothing; this is the test that it can.

Exit codes: 0 ran, 2 misuse or a malformed corpus, 3 the canary did not bite.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CASES = HERE / "cases.tsv"
SUBJECTS = HERE / "subjects"
RESULTS = HERE / "results"
KEY_FILE = pathlib.Path.home() / ".config" / "pix-harness" / ".env"

COLUMNS = ["id", "phrasing", "expected", "class", "provenance", "judged"]
CLASSES = {"T", "E", "D", "F", "N", "C"}
NONE = "NONE"
TOO_FEW = 3  # a skill with fewer expected cases than this is "too few to score"

# The asymmetric skill (SCHEMA.md, class F): recall is its metric; a false positive is
# the behaviour its description specifies, so it is reported and not penalised.
ASYMMETRIC = {"verify-before-quoting"}

STOPWORDS = set("""
a an and are as at be by can do does for from has have i in is it its me my of on or
so that the this to us we what when which with you your
""".split())


# --- the corpus -------------------------------------------------------------------

class Case:
    def __init__(self, row: dict[str, str]):
        self.id = row["id"].strip()
        self.phrasing = row["phrasing"].strip()
        self.expected = row["expected"].strip()
        self.cls = row["class"].strip()
        self.provenance = row["provenance"].strip()
        self.judged = row["judged"].strip()

    @property
    def is_canary(self) -> bool:
        return self.id.startswith("canary-")

    @property
    def expected_other(self) -> str | None:
        return self.expected[6:] if self.expected.startswith("other:") else None


def load_cases(path: pathlib.Path = CASES, allowed: set[str] | None = None) -> list[Case]:
    """allowed: the skill names `expected` may name; default the six subjects."""
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
        if reader.fieldnames != COLUMNS:
            sys.exit(f"run.py: {path.name} header must be {COLUMNS}, got {reader.fieldnames}")
        cases = [Case(row) for row in reader]
    problems = validate(cases, allowed)
    if problems:
        sys.exit("run.py: malformed corpus:\n  " + "\n  ".join(problems))
    return cases


def validate(cases: list[Case], subjects: set[str] | None = None) -> list[str]:
    """Every rule the corpus has to meet, as a list of what it broke. Empty is good."""
    subjects = subjects if subjects is not None else subject_names()
    problems, seen = [], set()
    for c in cases:
        if not c.id or c.id in seen:
            problems.append(f"{c.id or '(blank id)'}: id missing or duplicated")
        seen.add(c.id)
        if not c.phrasing:
            problems.append(f"{c.id}: phrasing is empty")
        if not c.provenance:
            problems.append(f"{c.id}: no provenance, so it is not in the corpus")
        if not c.judged:
            problems.append(f"{c.id}: not judged")
        if c.cls not in CLASSES:
            problems.append(f"{c.id}: class {c.cls!r} is not one of {sorted(CLASSES)}")
        if c.is_canary != (c.cls == "C"):
            problems.append(f"{c.id}: canary ids and class C go together")
        if not (c.expected == NONE or c.expected_other or c.expected in subjects):
            problems.append(f"{c.id}: expected {c.expected!r} is not a subject, NONE or other:<name>")
    if cases and not any(c.is_canary for c in cases):
        problems.append("no canary case: a suite that cannot fail certifies nothing")
    return problems


# --- the field ---------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict[str, str]:
    """name and description from a SKILL.md frontmatter, the three shapes seen on
    disk: a quoted one-line value, a bare one-line value, or a `|` / `>` block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in ("|", ">", "|-", ">-"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                if lines[i].strip() == "---":
                    break
                block.append(lines[i].strip())
                i += 1
            out[key] = " ".join(b for b in block if b).strip()
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"')
        out[key] = value
        i += 1
    return out


def load_field(root: pathlib.Path) -> dict[str, str]:
    """{skill name: description} for every <dir>/SKILL.md under root."""
    field: dict[str, str] = {}
    for skill_md in sorted(root.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = fm.get("name", skill_md.parent.name).strip().strip('"')
        field[name] = fm.get("description", "")
    if not field:
        sys.exit(f"run.py: no */SKILL.md under {root}")
    return field


def subject_names(root: pathlib.Path = SUBJECTS) -> set[str]:
    return {p.parent.name for p in root.glob("*/SKILL.md")}


# --- the deterministic arm -----------------------------------------------------------

def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9']+", text.lower()) if t not in STOPWORDS]


OVERLAP_CAP = 0.95  # word overlap never reaches 1.0: that score means verbatim containment


class Lexical:
    """IDF-weighted overlap between the phrasing and each description, capped at
    OVERLAP_CAP; a verbatim containment scores 1.0 outright. So a description that
    quotes the phrase always beats one that merely shares its words, and a tie at 1.0
    means two descriptions both claim the phrase, which is a finding about them."""

    def __init__(self, field: dict[str, str]):
        self.field = field
        self.desc_tokens = {name: set(tokens(d)) for name, d in field.items()}
        n = len(field)
        df: dict[str, int] = {}
        for toks in self.desc_tokens.values():
            for t in toks:
                df[t] = df.get(t, 0) + 1
        self.idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}

    def scores(self, phrasing: str) -> dict[str, float]:
        p = phrasing.lower().strip()
        ptoks = tokens(phrasing)
        denom = sum(self.idf.get(t, 1.0) for t in ptoks) or 1.0
        out = {}
        for name, desc in self.field.items():
            if p and p in desc.lower():
                out[name] = 1.0
                continue
            hit = sum(self.idf.get(t, 1.0) for t in ptoks if t in self.desc_tokens[name])
            out[name] = min(hit / denom, OVERLAP_CAP)
        return out

    def pick(self, phrasing: str, threshold: float) -> tuple[str, float]:
        s = self.scores(phrasing)
        best = max(s, key=lambda k: (s[k], k))
        return (best, s[best]) if s[best] >= threshold else (NONE, s[best])


# --- the model arm ---------------------------------------------------------------------

def api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key and KEY_FILE.is_file():
        for line in KEY_FILE.read_text(encoding="utf-8").splitlines():
            k, _, v = line.strip().partition("=")
            if k == "ANTHROPIC_API_KEY":
                key = v.strip().strip('"').strip("'")
    if not key:
        sys.exit(f"run.py: no ANTHROPIC_API_KEY in the environment or {KEY_FILE}")
    return key


class Model:
    """Claude chooses one skill from the field, or NONE. The field goes in a cached
    system block, since it is identical for every case and is most of the tokens."""

    def __init__(self, field: dict[str, str], model: str):
        try:
            import anthropic  # the only non-stdlib dependency, and only for this arm
        except ImportError:
            sys.exit("run.py: the model arm needs the anthropic package: pip install anthropic")
        # The real API, explicitly: an ANTHROPIC_BASE_URL left in the environment by a
        # coding tool would otherwise send the eval key somewhere else (seen 2026-10-09).
        self.client = anthropic.Anthropic(api_key=api_key(), base_url="https://api.anthropic.com")
        self.model = model
        self.names = sorted(field)
        listing = "\n".join(f"- {n}: {d}" for n, d in sorted(field.items()))
        self.system = [{
            "type": "text",
            "text": (
                "You are the skill-selection step of an agent. Below is every skill "
                "available at runtime, one per line as `- name: description`. Given a "
                "user's message, answer with the single skill whose description says it "
                "should fire for that message, or NONE if no description claims it. "
                "Judge from the descriptions only.\n\n" + listing
            ),
            "cache_control": {"type": "ephemeral"},
        }]
        self.schema = {
            "type": "object",
            "properties": {"skill": {"type": "string", "enum": self.names + [NONE]}},
            "required": ["skill"],
            "additionalProperties": False,
        }

    def pick(self, phrasing: str) -> tuple[str, float]:
        response = self.client.beta.messages.create(
            model=self.model,
            max_tokens=4096,  # thinking tokens count against this; 256 truncated the JSON
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=self.system,
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": self.schema}},
            messages=[{"role": "user", "content": f"User's message:\n\n{phrasing}"}],
        )
        if response.stop_reason == "refusal":
            return NONE, 0.0
        if response.stop_reason != "end_turn":
            sys.exit(f"run.py: model stopped with {response.stop_reason!r}; raise max_tokens")
        text = next(b.text for b in response.content if b.type == "text")
        return json.loads(text)["skill"], 1.0


# --- scoring -------------------------------------------------------------------------

def correct(case: Case, predicted: str, field: dict[str, str]) -> bool:
    other = case.expected_other
    if other is not None:
        # The named skill should win when it is in the field; when it is not (the
        # six-candidate run), the right outcome is that no subject fires.
        return predicted == other if other in field else predicted == NONE
    return predicted == case.expected


def metrics(cases: list[Case], predictions: dict[str, str], subjects: set[str]) -> dict[str, dict]:
    out = {}
    for s in sorted(subjects):
        tp = fp = fn = 0
        for c in cases:
            if c.is_canary:
                continue
            p = predictions[c.id]
            if c.expected == s and p == s:
                tp += 1
            elif p == s:
                fp += 1
            elif c.expected == s:
                fn += 1
        n = sum(1 for c in cases if c.expected == s and not c.is_canary)
        row = {"n": n, "tp": tp, "fp": fp, "fn": fn}
        if n < TOO_FEW:
            row["note"] = "too few to score"
        else:
            row["precision"] = tp / (tp + fp) if tp + fp else None
            row["recall"] = tp / (tp + fn) if tp + fn else None
            if s in ASYMMETRIC:
                row["note"] = "asymmetric: recall is the metric; false positives are specified behaviour"
        out[s] = row
    return out


def fmt(x) -> str:
    return "n/a" if x is None else f"{x:.2f}"


# --- main ----------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", choices=["deterministic", "model"], default="deterministic")
    ap.add_argument("--field", type=pathlib.Path,
                    default=pathlib.Path(os.environ.get("PIX_HARNESS_SKILL_FIELD", str(SUBJECTS))),
                    help="directory of <skill>/SKILL.md; default $PIX_HARNESS_SKILL_FIELD or evals/subjects")
    ap.add_argument("--field-label", default="", help="how the results file names the field, e.g. 'skills snapshot of 2026-10-08'")
    ap.add_argument("--cases", type=pathlib.Path, default=CASES)
    ap.add_argument("--subjects", type=pathlib.Path, default=SUBJECTS,
                    help="directory of the subject skills, the ones scored; default evals/subjects")
    ap.add_argument("--threshold", type=float, default=0.5, help="deterministic arm: below this, NONE")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--write", action="store_true", help="write evals/results/<date>-<arm>.md")
    args = ap.parse_args(argv)

    field = load_field(args.field)
    subjects = subject_names(args.subjects)
    cases = load_cases(args.cases, subjects | set(field))
    missing = subjects - set(field)
    if missing:
        sys.exit(f"run.py: the field at {args.field} lacks subject skills: {sorted(missing)}")

    scorer = Lexical(field) if args.arm == "deterministic" else Model(field, args.model)
    predictions, scores = {}, {}
    for c in cases:
        p, s = scorer.pick(c.phrasing, args.threshold) if args.arm == "deterministic" else scorer.pick(c.phrasing)
        predictions[c.id], scores[c.id] = p, s

    canaries = [c for c in cases if c.is_canary]
    unbitten = [c.id for c in canaries if correct(c, predictions[c.id], field)]
    def public(name: str) -> str:
        # Only the subject skills are named in a results file; every other skill in the
        # field appears as a count, since nothing of anyone else's skills is published.
        return name if name == NONE or name in subjects else "other"

    rows = []
    for c in cases:
        ok = correct(c, predictions[c.id], field)
        shown = c.expected if c.expected_other is None else "other:" + public(c.expected_other)
        rows.append((c.id, c.cls, shown, public(predictions[c.id]), "ok" if ok else "MISS", scores[c.id]))

    today = dt.date.today().isoformat()
    m = metrics(cases, predictions, subjects)
    lines = [
        f"# Results: {args.arm} arm, {today}",
        "",
        f"- Field: {len(field)} candidate skills" + (f", {args.field_label}" if args.field_label else "") + ".",
        f"- Cases: {len(cases)} ({len(canaries)} canary).",
        f"- Scorer: {'lexical, IDF-weighted overlap, threshold ' + str(args.threshold) if args.arm == 'deterministic' else 'model ' + args.model + ', effort low'}.",
        "- This is a worked example of the method, not a coverage figure or a benchmark of a model.",
        "",
        "| Skill | n | precision | recall | tp | fp | fn | note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s, r in m.items():
        lines.append(f"| `{s}` | {r['n']} | {fmt(r.get('precision'))} | {fmt(r.get('recall'))} | {r['tp']} | {r['fp']} | {r['fn']} | {r.get('note', '')} |")
    lines += ["", "| id | class | expected | predicted | result | score |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.2f} |")
    lines += ["", f"Canary: {'bit' if not unbitten else 'DID NOT BITE: ' + ', '.join(unbitten)}."]
    report = "\n".join(lines) + "\n"
    print(report)

    if args.write:
        RESULTS.mkdir(exist_ok=True)
        out = RESULTS / f"{today}-{args.arm}.md"
        out.write_text(report, encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)

    if unbitten:
        print("run.py: the canary did not bite; the runner cannot be trusted.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
