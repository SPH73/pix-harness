# Model arm, repeated: three runs on one field, 10 October 2026

The model arm had been one run per case (SCHEMA.md, known limits), and on 9 October two runs on identical descriptions read 28 then 27 on the original 31 cases. This file turns the single-run figure into a range.

- **Field:** 235 candidate skills, the skills snapshot of 2026-10-09 23:26 BST with the deleted skill removed from the snapshot by the author (9 Oct, after the 23:26 run had excluded it by hand). The same 235 descriptions the 23:26 run scored, so the runs are comparable cell for cell with `2026-10-09-model-rerun2.md`.
- **Cases:** 134 (31 original, 102 in `Set: trigger-pass 2026-10-09`, 1 canary). No case or description was changed between runs.
- **Scorer:** model claude-opus-5-5, effort low, as in every run so far.
- **Runs:** 3, launched 15:46 BST, finished 15:51 BST. Raw outputs kept: `2026-10-10-model-run1.md`, `-run2.md`, `-run3.md`. The canary bit on all three.
- **Why 3 and not 5:** the author's rule for this session was three runs, two more only if the original-31 range came back wider than 25 to 28. It did not.

## Score per run, per set

| Set | n | 9 Oct 23:26 (n=1, same field) | Run 1 | Run 2 | Run 3 | Range, 3 runs | Range, all 4 runs on this field |
|---|---|---|---|---|---|---|---|
| Original 31 | 31 | 28 | 27 | 27 | 27 | 27 to 27 | 27 to 28 |
| Trigger-pass set | 102 | 100 | 98 | 98 | 98 | 98 to 98 | 98 to 100 |

The 102-case set is a development set: it was written in the same session as the descriptions it scores, and two descriptions were edited after seeing misses and re-scored on the same cases. Its figure is not a claim of generalisation. A held-out set written blind to the descriptions is separate work and is not in this file.

## Cases that flipped

**Between the three runs today:** none changed between ok and MISS. One case changed its wrong answer: `new-session-prompt-03` (expected NONE) was answered `session-starter-new-session-prompt` on runs 1 and 3 and another skill on run 2. It is a miss either way, and it is the only movement the per-subject table shows (that subject's precision reads 0.88, 1.00, 0.88).

**Between the 23:26 run and today's three, same field:**

| id | set | 23:26 | today, 3 of 3 | reading |
|---|---|---|---|---|
| `transcript-triage-04` | original | ok | MISS (NONE) | The case that flipped on 9 Oct. Across the four runs on this field it is ok once and MISS three times. The 28 of 9 Oct was the run it happened to pass. |
| `consistency-02` | trigger-pass | ok | MISS (NONE) | Not noise. The field's copy of that skill's description is older than the one the case was judged against (below). |
| `consistency-08` | trigger-pass | ok | MISS (another skill) | Same cause. |

**The two consistency cases.** The snapshot's copy of `consistency-side-by-side/SKILL.md` is the 7 October text; the live skill was saved again on 9 October at 20:01 and the snapshot's own MANIFEST carries the live file's hash, which the copy on disk does not match. The two cases were judged against the live description, which quotes the `consistency-02` phrasing and no longer lists the `consistency-08` phrasing as a trigger. The copy the runner scored against does the reverse on both. The 23:26 run got both right by generalising past the text; today's three runs read the text as written, three times. So on the current field the honest figure for the set is 98 of 102, and 100 of 102 needs the field copy refreshed, not another run. Refreshing the snapshot is the author's act (the snapshot is a generated, additive recovery copy and is not hand-edited by a session); until then the two cases score against a description that does not claim them.

## Per subject, across the three runs

| Skill | n | precision | recall |
|---|---|---|---|
| `channel-method-first` | 8 | 1.00 | 1.00 |
| `compress-video-for-sharing` | 6 | 0.86 | 1.00 |
| `handoff` | 16 | 1.00 | 1.00 |
| `session-starter-new-session-prompt` | 7 | 0.88 to 1.00 | 1.00 |
| `transcript-triage` | 8 | 1.00 | 0.75 |
| `verify-before-quoting` | 7 | 1.00 | 1.00 (asymmetric: recall is the metric) |

Misses on every run: original set `new-session-prompt-03`, `transcript-triage-04`, `handoff-12`, `handoff-13`; trigger-pass set `compress-video-07`, `transcript-triage-11`, and the two consistency cases above.

## What the range means for the 25 to 28 claim

The before figure, 25 of 31 against the 8 October snapshot, is still n=1 and was not repeated here (that field is recoverable from the nightly backup's history, so it could be). The after figure is 27 on three of four runs on the current field and 28 on one. **The claim that survives is 25 (n=1) to 27 (n=4, range 27 to 28), and the two cases that account for the gain, `handoff-10` and `handoff-14`, passed on all four runs.** A third case, `transcript-triage-04`, passed on one run of the four and is the whole of the 27 to 28 spread. Nothing in these runs supports writing 28.
