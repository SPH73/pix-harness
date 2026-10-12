# The case schema

One case is one line of `cases.tsv`, tab-separated, six columns, header row first.

| Column | What goes in it |
|---|---|
| `id` | Unique, stable, lowercase: `<skill-or-topic>-<nn>`. A case built to fail starts with `canary-`. |
| `phrasing` | What the user said, verbatim from its source. Never composed to fit a class. |
| `expected` | The one skill that should fire, `NONE` if nothing should, or `other:<name>` when a skill outside the six should win (its description is not published here; it is scored by name in the full field). |
| `class` | One letter from the table below. |
| `provenance` | Where the phrasing comes from: `verbatim from <skill>/SKILL.md description`, or a path that resolves on the maintaining machine. A case without one is not in the corpus. |
| `judged` | Who judged the case and when, `Pix 2026-10-09`. The judgement is the author's, not the runner's. |

## Classes

| Class | What it is | Where it comes from |
|---|---|---|
| `T` | A direct trigger: the description names it as a phrase that should fire the skill. | The skill's own frontmatter. |
| `E` | A near-miss the description already anticipates and says should still fire. | The skill's own frontmatter. |
| `D` | A confusable pair: a phrasing that sits on a boundary the skill author wrote down between two skills. | Both frontmatters, or the body line that draws the boundary. |
| `F` | The deliberate overtrigger. `verify-before-quoting` states its own asymmetry: undertriggering costs reputation, overtriggering costs a little time. Recall is the metric; a false positive is specified behaviour and is reported, not penalised. | Its frontmatter, plus phrasings from real work. |
| `N` | An explicit anti-trigger: the description says this should not fire, so `expected` is `NONE` or `other:<name>`. | The skill's own frontmatter. |
| `C` | The canary. Built to fail. If it passes, the runner is broken and exits non-zero. | This file. |

Classes A, B and C of the scope document are not trigger cases and are not here.

## What the corpus is not

- Not a benchmark of a model. It scores six skill descriptions, against a stated field of candidate skills, on a stated date, with a stated scorer.
- Not stable across model versions. Every results file is dated.
- Not a coverage figure. About 25 cases across six skills is a worked example of the method.

## Known limits

- **Single-label.** One `expected` per sentence, and the scorer asks for one skill. A sentence that should fire two skills at once (the author's example: a long session that is ending and has value in it, which wants both `handoff` and `session-value-capture`) cannot be scored here and is not in the corpus. Multi-label cases are the next increment, not Part 1.
- **Few repeats.** On 10 October the model arm was run three times on one field; from 11 October, three times on the trimmed field and once on the full field. The same case can be answered differently between runs; each results file is one run on its stated date and model. _(Changed 2026-10-12. Prior value: "**The model arm is one run.** The same case can be answered differently on a rerun. A results file is n=1 per case on its stated date and model, and says so.")_
