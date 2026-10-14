# Part 1: a skill-trigger eval suite

**Results to 14 October 2026.** Started 9 October 2026.

The suite tests whether a user's phrasing fires the right skill out of the skills present at runtime. Each case is a phrasing with its provenance and the one skill expected to fire (or none); a scorer is shown the candidate skills' descriptions and picks one, and the runner reports precision and recall per subject skill. Each results file is a worked example of the method, not a coverage figure or a benchmark of a model.

## Method

- **Subjects:** six skills, their frontmatter verbatim in `subjects/`.
- **Corpus:** 137 cases in `cases.tsv`. 136 are judged by the author; 1 is a canary built to fail. Case format and the six classes (direct trigger, anticipated near-miss, confusable pair, deliberate overtrigger, anti-trigger, canary) are in `SCHEMA.md`.
- **Sets:** 31 original cases, judged before the descriptions were revised on 9 October; 102 cases in a development set (`Set: trigger-pass 2026-10-09`), written in the same session as the descriptions they score, so their figures are not a claim of generalisation; 3 cases added on 11 October. A held-out set of 37 cases plus a copy of the canary, in `held-out.tsv`, written on 14 October by the author without the six descriptions in view, from real situations, and judged by her (5 positives per skill, 6 for `verify-before-quoting`, and 6 anti-triggers).
- **Arms:** `model` (scorer requested as claude-opus-5-5, effort low, as each header states) and `deterministic` (lexical overlap, no model; run on 9 October and on the held-out set on 14 October).
- **Fields:** trimmed (46 skills, the set live at runtime since 11 October) and full (236 skills, every skill on the maintaining machine; 234 or 235 before 11 October). Trimmed results are given first because that is the field live at runtime.
- **Repeats:** three runs on the 235-skill field on 10 October; from 11 October, three runs per trimmed field and one per full field. The held-out set was scored once in that shape, on 14 October.
- **Frozen descriptions:** the six descriptions were frozen at 14:59 BST on 13 October and not changed for the held-out runs. They were not reviewed against current practice before the freeze; from now on that review comes before any freeze.
- **Canary:** scored a miss on every run, as built.
- **Miss:** a case whose scorer answer differs from `expected`. This includes cases expected to fire no skill or a skill outside the six. Miss counts below exclude the canary.

## Headline results

### Held-out set, 14 October

Files: `2026-10-14-model-held-out-run1.md`, `-run2.md`, `-run3.md` (trimmed field), `2026-10-14-model-held-out-fullfield.md` (full field), and the deterministic arm on both fields (`2026-10-14-deterministic-held-out.md`, `-fullfield.md`). Same 37 judged cases and frozen descriptions across all six files. Each model-arm header records the answering model: claude-opus-5-5 in 38 of 38 calls in every run.

| Set | n | Trimmed, three runs | Full, one run |
|---|---|---|---|
| Held-out cases correct | 37 | 30, 31, 32 | 28 |
| Misses | 37 | 7, 6, 5 | 9 |

The deterministic arm missed 28 of 37 on each field: a floor for comparison.

Per subject skill:

| Skill | n | Trimmed precision, mean (range) | Trimmed recall, mean (range) | Full precision / recall |
|---|---|---|---|---|
| `channel-method-first` | 5 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 0.80 |
| `compress-video-for-sharing` | 5 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 1.00 |
| `handoff` | 5 | 1.00 (1.00 to 1.00) | 0.60 (0.60 to 0.60) | 1.00 / 0.40 |
| `session-starter-new-session-prompt` | 5 | 1.00 (1.00 to 1.00) | 0.87 (0.80 to 1.00) | 1.00 / 1.00 |
| `transcript-triage` | 5 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 1.00 |
| `verify-before-quoting` | 6 | 1.00 (1.00 to 1.00) | 0.50 (0.50 to 0.50) | 1.00 / 0.33 |

On the 46-skill field, against the development runs below, three skills held their recall, `session-starter-new-session-prompt` missed one case in two of three runs, and two fell (`handoff` 1.00 to 0.60, `verify-before-quoting` 1.00 to 0.50; on the 236-skill field, 0.94 to 0.40 and 0.86 to 0.33). Five cases missed in all four model runs:

- `handoff`: `ho-handoff-04` and `-05` ask whether a run's named work is covered, and return no skill. The description was written before the author used handoffs to close a supervised run, so it does not cover that use. Recorded as a gap in the description; the description stays frozen and the labels stand.
- `verify-before-quoting`: `ho-verify-before-quoting-01` and `-03` go to a skill outside the six in every run. The results files mask its name, and it was not probed, so it is not named here. `ho-verify-before-quoting-06` returns no skill in three runs and a skill outside the six in one.

### Development set, 13 October

Files: `2026-10-13-model-run19.md`, `-run20.md`, `-run21.md` (trimmed field) and `2026-10-13-model-run19-fullfield.md` (full field). Same cases and labels across all four; the three trimmed runs share one descriptions hash. These files do not record the answering model. The descriptions differ from the held-out runs' in one place: `compress-video-for-sharing` was saved again at the 14:59 freeze.

| Set | n | Trimmed, three runs (range) | Full, one run |
|---|---|---|---|
| All judged cases | 136 | 127 to 129 | 126 |
| Original 31 | 31 | 28 to 29 | 28 |
| Development set | 102 | 97 to 98 | 96 |
| Added 11 October | 3 | 2 | 2 |
| Misses | 136 | 7 to 9 | 10 |

Per subject skill:

| Skill | n | Trimmed precision, mean (range) | Trimmed recall, mean (range) | Full precision / recall |
|---|---|---|---|---|
| `channel-method-first` | 8 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 0.88 |
| `compress-video-for-sharing` | 6 | 0.86 (0.86 to 0.86) | 1.00 (1.00 to 1.00) | 1.00 / 1.00 |
| `handoff` | 16 | 0.92 (0.89 to 0.94) | 1.00 (1.00 to 1.00) | 0.94 / 0.94 |
| `session-starter-new-session-prompt` | 7 | 0.88 (0.88 to 0.88) | 1.00 (1.00 to 1.00) | 0.88 / 1.00 |
| `transcript-triage` | 8 | 1.00 (1.00 to 1.00) | 0.92 (0.88 to 1.00) | 1.00 / 0.88 |
| `verify-before-quoting` | 7 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 0.86 |

`verify-before-quoting` is asymmetric: recall is its metric, and false positives are specified behaviour.

The original-31 figure is not given as a single number across dates: two of the 31 are scored against different expectations from 11 October, so the 9 and 10 October readings (25 of 31 before the descriptions were revised, 27 to 28 after, in `2026-10-09-rerun-before-after.md` and `2026-10-10-model-repeats.md`) are not on the same labels or field as the later ones.

## What changed across runs

- **9 October:** descriptions revised twice (snapshots 21:13 and 23:26) and the development set written; cases grew from 32 to 126 to 134 (`2026-10-09-*-rerun.md`, `-rerun2.md`).
- **10 October:** three repeats on an unchanged field and cases (`2026-10-10-model-repeats.md`).
- **11 October:** the runtime field trimmed to 46 skills and new descriptions saved before run4 (`2026-10-11-model-run4.md` header); further description saves before run7, run10 and run13 (each header); two cases re-judged before run7 (footnote in `2026-10-11-model-run7.md`); 3 cases added before run10 (`2026-10-11-model-run10.md`, 137 cases).
- **12 October:** one description saved and one case relabelled before run16 (`2026-10-12-model-run16.md` header).
- **13 October:** the `compress-video-for-sharing` description saved before run19 (`2026-10-13-model-run19.md` header), and saved again when the descriptions were frozen at 14:59 BST.
- **14 October:** the held-out set written and judged; the runner records the answering model in each model-arm header from here on; the held-out set scored on the frozen descriptions (`2026-10-14-*-held-out*.md` headers).
- Each file's header names its field, case count and descriptions hash.

Trimmed-field misses on all judged cases went from 17, 14, 12 (run4 to run6) to 8, 9, 7 (run19 to run21); between those rows the descriptions changed five times, three cases were added and three were relabelled, so the rows do not share cases or field.

Misses per run:

| Date | Arm | Files | Cases | Field | Misses per run |
|---|---|---|---|---|---|
| 9 Oct | deterministic | `2026-10-09-deterministic.md`, `-rerun.md`, `-rerun2.md` | 32, 126, 134 | 234, 235, 235 | 7, 33, 35 |
| 9 Oct | model | `2026-10-09-model.md`, `-rerun.md`, `-rerun2.md` | 32, 126, 134 | 234, 235, 235 | 6, 12, 5 |
| 10 Oct | model | `2026-10-10-model-run1.md` to `-run3.md` | 134 | 235 | 8, 8, 8 |
| 11 Oct | model | `2026-10-11-model-run4.md` to `-run6.md` | 134 | 46 | 17, 14, 12 |
| 11 Oct | model | `2026-10-11-model-run4-fullfield.md` | 134 | 236 | 16 |
| 11 Oct | model | `2026-10-11-model-run7.md` to `-run9.md` | 134 | 46 | 9, 10, 10 |
| 11 Oct | model | `2026-10-11-model-run7-fullfield.md` | 134 | 236 | 8 |
| 11 Oct | model | `2026-10-11-model-run10.md` to `-run12.md` | 137 | 46 | 9, 9, 8 |
| 11 Oct | model | `2026-10-11-model-run10-fullfield.md` | 137 | 236 | 13 |
| 11 Oct | model | `2026-10-11-model-run13.md` to `-run15.md` | 137 | 46 | 11, 10, 9 |
| 11 Oct | model | `2026-10-11-model-run13-fullfield.md` | 137 | 236 | 14 |
| 12 Oct | model | `2026-10-12-model-run16.md` to `-run18.md` | 137 | 46 | 8, 8, 7 |
| 12 Oct | model | `2026-10-12-model-run16-fullfield.md` | 137 | 236 | 11 |
| 13 Oct | model | `2026-10-13-model-run19.md` to `-run21.md` | 137 | 46 | 8, 9, 7 |
| 13 Oct | model | `2026-10-13-model-run19-fullfield.md` | 137 | 236 | 10 |
| 14 Oct | deterministic | `2026-10-14-deterministic-held-out.md`, `-fullfield.md` | 38 (held-out) | 46, 236 | 28, 28 |
| 14 Oct | model | `2026-10-14-model-held-out-run1.md` to `-run3.md` | 38 (held-out) | 46 | 7, 6, 5 |
| 14 Oct | model | `2026-10-14-model-held-out-fullfield.md` | 38 (held-out) | 236 | 9 |

## Known limits

- **Development set.** 102 of the 136 judged cases were written alongside the descriptions they score, and the descriptions were revised after reviewing misses on the rest, so no development case is unseen by that tuning. Only the held-out set carries a generalisation figure.
- **Held-out set, written by the author.** It was written without the descriptions in view, from real situations, by the person who wrote the descriptions and the development set, so it is not blind to her. It is small: 5 or 6 positives per skill, so one case moves recall by 0.17 to 0.20.
- **Held-out coverage.** No phrasing stops a session part-way: the set was written in a period without short-notice stops. The development set covers that case.
- **Held-out answers changed.** Four of the six held-out anti-trigger rows were first judged to fire no skill and changed to a skill outside the six after the descriptions were shown. Both answers and the reason are in each row's provenance; the changed answers are scored. Neither reading moves a subject skill's precision or recall.
- **Single-label.** One expected skill per case; a phrasing that should fire two skills cannot be scored (`SCHEMA.md`). Live instance: the author would want `ho-none-compress-video-01` to fire one skill and then another, and it is scored on the first only.
- **Few repeats.** Three runs per trimmed field and one per full field; the same case can be answered differently between runs (the original 31 read 28, 28 and 29 on the latest trimmed field).
- **Answering model.** From run4 the runner enables a server-side fallback. From the held-out runs on, each model-arm header records the model that answered: claude-opus-5-5 in 38 of 38 calls in each of the four held-out runs, with no fallback. The development runs (run4 to run21) do not record it; claude-opus-5-5 is the model they requested. The effort a fallback model would run at is not recorded.
- **No published figure is reproducible from this repository.** Every results file is on a field that includes skills whose descriptions are not published: the trimmed field (46 skills) and the full field (234 to 236). A reader can run the six subjects alone from `subjects/`, the deterministic arm with no key or the model arm with their own, but no published results file is on that field.
- **Not a benchmark.** Six skill descriptions, a stated field, a stated date, a stated scorer.

## Files

| Path | What it is |
|---|---|
| `SCHEMA.md` | The case format and the six classes. |
| `cases.tsv` | The corpus. Grows only by judged, provenanced cases. |
| `held-out.tsv` | The held-out set, in the same format: 37 judged cases and a copy of the canary. |
| `subjects/` | The six subject skills' frontmatter, verbatim, so the six subjects can be run alone from this repository. |
| `run.py` | The runner. Two arms: `deterministic` (lexical, no model) and `model`. |
| `results/` | Dated results files, one per run worth keeping, plus the summaries `2026-10-09-rerun-before-after.md` and `2026-10-10-model-repeats.md`. |

---

Receipt: until 2026-10-12 the status line read "**In progress.** Started 9 October 2026. Nothing here is a result yet."
