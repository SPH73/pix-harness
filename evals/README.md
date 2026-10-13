# Part 1: a skill-trigger eval suite

**Results to 12 October 2026.** Started 9 October 2026.

The suite tests whether a user's phrasing fires the right skill out of the skills present at runtime. Each case is a phrasing with its provenance and the one skill expected to fire (or none); a scorer is shown the candidate skills' descriptions and picks one, and the runner reports precision and recall per subject skill. Each results file is a worked example of the method, not a coverage figure or a benchmark of a model.

## Method

- **Subjects:** six skills, their frontmatter verbatim in `subjects/`.
- **Corpus:** 137 cases in `cases.tsv`. 136 are judged by the author; 1 is a canary built to fail. Case format and the six classes (direct trigger, anticipated near-miss, confusable pair, deliberate overtrigger, anti-trigger, canary) are in `SCHEMA.md`.
- **Sets:** 31 original cases, judged before the descriptions were revised on 9 October; 102 cases in a development set (`Set: trigger-pass 2026-10-09`), written in the same session as the descriptions they score, so their figures are not a claim of generalisation; 3 cases added on 11 October. A held-out set is not in this repository.
- **Arms:** `model` (claude-opus-5-5 requested, effort low) and `deterministic` (lexical overlap, no model; run on 9 October only).
- **Fields:** trimmed (46 skills, the set live at runtime since 11 October) and full (236 skills, every skill on the maintaining machine; 234 or 235 before 11 October). Trimmed results are given first because that is the field live at runtime.
- **Repeats:** three runs on the 235-skill field on 10 October; from 11 October, three runs per trimmed field and one per full field.
- **Canary:** scored a miss on every run, as built.
- **Miss:** a case whose scorer answer differs from `expected`. This includes cases expected to fire no skill or a skill outside the six. Miss counts below exclude the canary.

## Headline results

Latest runs: `2026-10-13-model-run19.md`, `-run20.md`, `-run21.md` (trimmed field) and `2026-10-13-model-run19-fullfield.md` (full field). Same cases and labels across all four; the three trimmed runs share one descriptions hash.

| Set | n | Trimmed, three runs (range) | Full, one run |
|---|---|---|---|
| All judged cases | 136 | 128 to 129 | 125 |
| Original 31 | 31 | 28 to 29 | 26 |
| Development set | 102 | 98 | 97 |
| Added 11 October | 3 | 2 | 2 |
| Misses | 136 | 7 to 8 | 11 |

Per subject skill:

| Skill | n | Trimmed precision, mean (range) | Trimmed recall, mean (range) | Full precision / recall |
|---|---|---|---|---|
| `channel-method-first` | 8 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 0.88 |
| `compress-video-for-sharing` | 6 | 0.83 (0.83 to 0.83) | 0.83 (0.83 to 0.83) | 1.00 / 0.83 |
| `handoff` | 16 | 0.92 (0.89 to 0.94) | 1.00 (1.00 to 1.00) | 0.93 / 0.88 |
| `session-starter-new-session-prompt` | 7 | 0.88 (0.88 to 0.88) | 1.00 (1.00 to 1.00) | 1.00 / 1.00 |
| `transcript-triage` | 8 | 1.00 (1.00 to 1.00) | 0.92 (0.88 to 1.00) | 1.00 / 0.88 |
| `verify-before-quoting` | 7 | 1.00 (1.00 to 1.00) | 1.00 (1.00 to 1.00) | 1.00 / 0.86 |

`verify-before-quoting` is asymmetric: recall is its metric, and false positives are specified behaviour.

The original-31 figure is not given as a single number across dates: two of the 31 are scored against different expectations from 11 October, so the 9 and 10 October readings (25 of 31 before the descriptions were revised, 27 to 28 after, in `2026-10-09-rerun-before-after.md` and `2026-10-10-model-repeats.md`) are not on the same labels or field as the 12 October ones.

## What changed across runs

- **9 October:** descriptions revised twice (snapshots 21:13 and 23:26) and the development set written; cases grew from 32 to 126 to 134 (`2026-10-09-*-rerun.md`, `-rerun2.md`).
- **10 October:** three repeats on an unchanged field and cases (`2026-10-10-model-repeats.md`).
- **11 October:** the runtime field trimmed to 46 skills and new descriptions saved before run4 (`2026-10-11-model-run4.md` header); further description saves before run7, run10 and run13 (each header); two cases re-judged before run7 (footnote in `2026-10-11-model-run7.md`); 3 cases added before run10 (`2026-10-11-model-run10.md`, 137 cases).
- **12 October:** one description saved and one case relabelled before run16 (`2026-10-12-model-run16.md` header).
- Each file's header names its field, case count and descriptions hash.

Trimmed-field misses went from 17, 14, 12 (run4 to run6) to 8, 8, 7 (run16 to run18); between those rows the descriptions changed four times, three cases were added and three were relabelled, so the rows do not share cases or field.

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

## Known limits

- **Development set.** 102 of the 136 judged cases were written alongside the descriptions they score. No held-out set is in this repository.
- **Single-label.** One expected skill per case; a phrasing that should fire two skills cannot be scored (`SCHEMA.md`).
- **Few repeats.** Three runs per trimmed field and one per full field; the same case can be answered differently between runs (the original 31 read 28, 28 and 29 on the latest trimmed field).
- **Answering model.** From run4 the runner enables a server-side fallback and the answering model is not recorded; claude-opus-5-5 is the model requested (each header).
- **Full field not reproducible here.** The other skills' descriptions are not published; a reader can repeat the six-candidate run, not the full-field one.
- **Not a benchmark.** Six skill descriptions, a stated field, a stated date, a stated scorer.

## Files

| Path | What it is |
|---|---|
| `SCHEMA.md` | The case format and the six classes. |
| `cases.tsv` | The corpus. Grows only by judged, provenanced cases. |
| `subjects/` | The six subject skills' frontmatter, verbatim, so the six-candidate run can be repeated from this repository. |
| `run.py` | The runner. Two arms: `deterministic` (lexical, no model) and `model`. |
| `results/` | Dated results files, one per run worth keeping, plus the summaries `2026-10-09-rerun-before-after.md` and `2026-10-10-model-repeats.md`. |

---

Receipt: until 2026-10-12 the status line read "**In progress.** Started 9 October 2026. Nothing here is a result yet."
