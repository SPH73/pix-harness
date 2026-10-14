"""The eval suite's own tests: the corpus is well formed, the field loader reads the
frontmatter shapes that exist on disk, the metrics are what they say, the canary bites,
and the corpus carries no identity the guard would block.

They use a FICTIONAL field built in a temp dir, so they need neither the private skill
snapshot nor a key, and they prove the runner rather than any result.
"""

import contextlib
import io
import pathlib
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

REPO = pathlib.Path(__file__).resolve().parents[1]
EVALS = REPO / "evals"
GUARD = REPO / "tools" / "check-identity.sh"
sys.path.insert(0, str(EVALS))

import run  # noqa: E402  (evals/run.py)


def fake_field(root: pathlib.Path) -> None:
    (root / "bake-bread").mkdir()
    (root / "bake-bread" / "SKILL.md").write_text(
        '---\nname: "bake-bread"\ndescription: "Bake a loaf. Trigger on \\"bake me a loaf\\", '
        '\\"make bread\\". NOT for cakes."\n---\nbody\n', encoding="utf-8")
    (root / "ice-cake").mkdir()
    (root / "ice-cake" / "SKILL.md").write_text(
        "---\nname: ice-cake\ndescription: |\n  Ice a cake with buttercream.\n"
        "  Fires on \"ice this cake\", \"decorate the sponge\".\n---\n", encoding="utf-8")
    (root / "plain").mkdir()
    (root / "plain" / "SKILL.md").write_text(
        "---\nname: plain\ndescription: Sweep the floor and nothing else.\n---\n", encoding="utf-8")


class TestFrontmatter(unittest.TestCase):
    def test_the_three_shapes_on_disk_parse(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            fake_field(root)
            field = run.load_field(root)
        self.assertEqual(set(field), {"bake-bread", "ice-cake", "plain"})
        self.assertIn('"bake me a loaf"', field["bake-bread"])  # quoted, with escapes
        self.assertIn("decorate the sponge", field["ice-cake"])  # block scalar joined
        self.assertEqual(field["plain"], "Sweep the floor and nothing else.")

    def test_the_six_subjects_load_from_the_repo(self) -> None:
        field = run.load_field(EVALS / "subjects")
        self.assertEqual(len(field), 6)
        self.assertTrue(all(len(d) > 100 for d in field.values()))


class TestCorpus(unittest.TestCase):
    def test_cases_tsv_is_well_formed(self) -> None:
        cases = run.load_cases()  # exits on a malformed corpus
        self.assertTrue(cases)

    def test_validate_names_each_fault(self) -> None:
        good = run.Case({"id": "x-01", "phrasing": "p", "expected": "NONE", "class": "N",
                         "provenance": "here", "judged": "Pix 2026-10-09"})
        canary = run.Case({"id": "canary-01", "phrasing": "p", "expected": "NONE", "class": "C",
                           "provenance": "built to fail", "judged": "agent"})
        self.assertEqual(run.validate([good, canary], subjects=set()), [])
        bad = run.Case({"id": "x-01", "phrasing": "", "expected": "nope", "class": "Z",
                        "provenance": "", "judged": ""})
        problems = run.validate([good, bad], subjects=set())
        joined = "\n".join(problems)
        for fault in ("duplicated", "phrasing is empty", "no provenance", "not judged",
                      "class 'Z'", "not a subject", "no canary"):
            self.assertIn(fault, joined)

    @unittest.skipUnless(GUARD.is_file(), "guard script not present")
    def test_the_corpus_carries_no_identity_even_under_ignore_allow(self) -> None:
        """Flag 9 of the scope: realistic phrasings carry real names. Strict mode."""
        result = subprocess.run(["bash", str(GUARD), "--file", str(EVALS / "cases.tsv"), "--ignore-allow"],
                                capture_output=True, text=True, cwd=str(REPO))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TestLexicalArm(unittest.TestCase):
    def setUp(self) -> None:
        self.field = {
            "bake-bread": 'Bake a loaf. Trigger on "bake me a loaf", "make bread". NOT for cakes.',
            "ice-cake": 'Ice a cake with buttercream. Fires on "ice this cake", "decorate the sponge".',
            "plain": "Sweep the floor and nothing else.",
        }
        self.lex = run.Lexical(self.field)

    def test_a_verbatim_phrase_scores_one(self) -> None:
        self.assertEqual(self.lex.pick("bake me a loaf", 0.5), ("bake-bread", 1.0))

    def test_an_unrelated_phrase_is_none(self) -> None:
        self.assertEqual(self.lex.pick("tune the piano", 0.5)[0], run.NONE)

    def test_verbatim_beats_overlap_however_short(self) -> None:
        field = {"quoted": 'Fires on "go now".', "wordy": "Go here, go there, go anywhere, go go go."}
        name, score = run.Lexical(field).pick("go now", 0.5)
        self.assertEqual((name, score), ("quoted", 1.0))
        self.assertLessEqual(run.Lexical(field).scores("go now")["wordy"], run.OVERLAP_CAP)

    def test_overlap_is_weighted_and_bounded(self) -> None:
        name, score = self.lex.pick("decorate a cake", 0.3)
        self.assertEqual(name, "ice-cake")
        self.assertTrue(0 < score <= 1)


class TestMetricsAndCanary(unittest.TestCase):
    def case(self, id, expected, cls="T"):
        return run.Case({"id": id, "phrasing": id, "expected": expected, "class": cls,
                         "provenance": "test", "judged": "test"})

    def test_precision_recall_and_too_few(self) -> None:
        cases = [self.case("a1", "s"), self.case("a2", "s"), self.case("a3", "s"),
                 self.case("b1", "NONE", "N"), self.case("c1", "t")]
        preds = {"a1": "s", "a2": "s", "a3": "NONE", "b1": "s", "c1": "t"}
        m = run.metrics(cases, preds, {"s", "t"})
        self.assertEqual((m["s"]["tp"], m["s"]["fp"], m["s"]["fn"]), (2, 1, 1))
        self.assertAlmostEqual(m["s"]["precision"], 2 / 3)
        self.assertAlmostEqual(m["s"]["recall"], 2 / 3)
        self.assertEqual(m["t"]["note"], "too few to score")

    def test_other_is_scored_by_field_membership(self) -> None:
        c = self.case("o1", "other:design-handoff", "D")
        self.assertTrue(run.correct(c, "design-handoff", {"design-handoff": ""}))
        self.assertFalse(run.correct(c, "handoff", {"design-handoff": ""}))
        self.assertTrue(run.correct(c, run.NONE, {"handoff": ""}))  # not in field: NONE is right

    def test_the_canary_bites_and_an_unbitten_canary_fails_the_run(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            fake_field(root)
            cases = root / "cases.tsv"
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "canary-01\tbake me a loaf\tice-cake\tC\tbuilt to fail\tagent\n", encoding="utf-8")
            # The real run exits 0: lexical says bake-bread, expected ice-cake, so it bit.
            self.assertEqual(run.main(["--field", str(root), "--subjects", str(root), "--cases", str(cases)]), 0)
            # Flip the expectation to the truth and the canary no longer fails: exit 3.
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "canary-01\tbake me a loaf\tbake-bread\tC\tbuilt to fail\tagent\n", encoding="utf-8")
            self.assertEqual(run.main(["--field", str(root), "--subjects", str(root), "--cases", str(cases)]), 3)


class StubClient:
    """Stands in for the anthropic client: no key, no network. Each call returns the next
    (answering model, usage.iterations) pair as a response that picks bake-bread."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.beta = types.SimpleNamespace(messages=types.SimpleNamespace(create=self.create))

    def create(self, **kwargs):
        model, iterations = self.answers.pop(0)
        return types.SimpleNamespace(
            model=model, stop_reason="end_turn",
            usage=types.SimpleNamespace(iterations=iterations),
            content=[types.SimpleNamespace(type="text", text='{"skill": "bake-bread"}')])


def fallback(model):
    return [types.SimpleNamespace(type="message", model="claude-opus-5-5"),
            types.SimpleNamespace(type="fallback_message", model=model)]


class TestAnsweringModel(unittest.TestCase):
    REQUESTED = "claude-opus-5-5"

    def header(self, arm, answers=()):
        """Run main on a fictional field and three cases; return the header lines."""
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            fake_field(root)
            cases = root / "cases.tsv"
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "t-01\tbake me a loaf\tbake-bread\tT\ttest\ttest\n"
                             "t-02\tmake bread\tbake-bread\tT\ttest\ttest\n"
                             "canary-01\tbake me a loaf\tice-cake\tC\tbuilt to fail\tagent\n", encoding="utf-8")
            client, real = StubClient(answers), run.Model
            out = io.StringIO()
            with mock.patch.object(run, "Model", lambda field, model: real(field, model, client)), \
                    contextlib.redirect_stdout(out):
                code = run.main(["--arm", arm, "--field", str(root), "--subjects", str(root), "--cases", str(cases)])
        self.assertEqual(code, 0)
        return [l for l in out.getvalue().splitlines() if l.startswith("- ")]

    def test_one_model_for_every_call(self) -> None:
        lines = self.header("model", [(self.REQUESTED, [])] * 3)
        self.assertIn("- Answering model: claude-opus-5-5 (3 of 3 calls). "
                      "Found by: response.model (no fallback entry) 3.", lines)

    def test_a_mixed_run_counts_each_model_and_names_the_fallback_cases(self) -> None:
        lines = self.header("model", [(self.REQUESTED, None),
                                      (self.REQUESTED, fallback("claude-sonnet-5-5")),
                                      (self.REQUESTED, [])])
        self.assertIn("- Answering model: claude-opus-5-5 (2 of 3 calls); claude-sonnet-5-5 (1 of 3 calls: t-02). "
                      "Found by: fallback entry 1, response.model (no fallback entry) 1, "
                      "response.model (usage.iterations absent) 1.", lines)

    def test_the_line_sits_after_the_scorer_line(self) -> None:
        lines = self.header("model", [(self.REQUESTED, [])] * 3)
        self.assertTrue(lines[2].startswith("- Scorer: model "))
        self.assertTrue(lines[3].startswith("- Answering model: "))

    def test_a_refusal_still_records_the_model(self) -> None:
        response = types.SimpleNamespace(model=self.REQUESTED, stop_reason="refusal",
                                         usage=types.SimpleNamespace(iterations=fallback("claude-sonnet-5-5")))
        client = types.SimpleNamespace(beta=types.SimpleNamespace(
            messages=types.SimpleNamespace(create=lambda **kw: response)))
        m = run.Model({"bake-bread": "x"}, self.REQUESTED, client)
        self.assertEqual(m.pick("anything"), (run.NONE, 0.0))
        self.assertEqual(m.last_answer, ("claude-sonnet-5-5", run.FOUND_FALLBACK))

    def test_the_deterministic_arm_header_is_unchanged(self) -> None:
        lines = self.header("deterministic")
        self.assertFalse(any(l.startswith("- Answering model") for l in lines))
        self.assertEqual([l.split(":")[0] for l in lines],
                         ["- Field", "- Cases", "- Scorer", "- This is a worked example of the method, not a coverage figure or a benchmark of a model."])


class TestValidate(unittest.TestCase):
    def test_validate_checks_and_stops_before_scoring(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            fake_field(root)
            cases = root / "cases.tsv"
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "t-01\tbake me a loaf\tbake-bread\tT\ttest\ttest\n"
                             "canary-01\tbake me a loaf\tice-cake\tC\tbuilt to fail\tagent\n", encoding="utf-8")
            argv = ["--field", str(root), "--subjects", str(root), "--cases", str(cases), "--validate"]
            out = io.StringIO()
            # No scorer of either arm is built: the model arm would need a key and the network.
            with mock.patch.object(run, "Lexical", side_effect=AssertionError("scored")), \
                    mock.patch.object(run, "Model", side_effect=AssertionError("scored")), \
                    contextlib.redirect_stdout(out):
                self.assertEqual(run.main(argv), 0)
                self.assertEqual(run.main(argv + ["--arm", "model"]), 0)
            self.assertEqual(out.getvalue().splitlines()[0],
                             "cases.tsv: 2 cases (1 canary), valid against a field of 3.")
            self.assertNotIn("|", out.getvalue())  # no score table
            # A malformed corpus still stops with its faults named.
            cases.write_text("\t".join(run.COLUMNS) + "\n"
                             "t-01\tbake me a loaf\tbake-bread\tT\t\ttest\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as raised:
                run.main(argv)
            self.assertIn("no provenance", str(raised.exception.code))


if __name__ == "__main__":
    unittest.main()
