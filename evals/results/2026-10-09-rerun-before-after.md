# Before and after: the original 31 judged cases across three snapshots of 8 and 9 October 2026

Same 31 cases, same scorers, same runner. What changed between runs is only the skill descriptions. **Before:** snapshot 2026-10-08, the descriptions as they stood when the cases were judged. **After the trigger pass:** snapshot 2026-10-09 21:13, after the author rewrote all 18 of her skills with her own phrasings (17 hashes changed in a field of 234, one skill added). **After the edits:** snapshot 2026-10-09 23:26, after six further edits the evening's findings produced (the sidebar skill's trigger narrowed to "edit", a word dropped from block-briefing, a named-person skill renamed to `ask-the-stakeholder` with no name in it, three pointers renamed); the deleted skill is excluded from the field, so it stays 235.

The cases judged on 9 October (102 in the end, labelled `Set: trigger-pass 2026-10-09` in their provenance) are scored in the `-rerun` and `-rerun2` files as a separate set and are NOT in the per-case table below: they were written alongside the new descriptions, so scoring them against those descriptions is partly circular. Of them, 57 name no subject skill and test only that no subject fires on them.

| Arm | Before (2026-10-08) | After the trigger pass (21:13) | After the edits (23:26) | New set, after the edits |
|---|---|---|---|---|
| deterministic (lexical) | 24 of 31 | 24 of 31 | 24 of 31 | 74 of 102 |
| model (claude-opus-5-5, effort low, n=1) | 25 of 31 | 27 of 31 | 28 of 31 | 100 of 102 |

The model arm is one run per case (SCHEMA.md, known limits). Across the evening's seven model runs the original-31 figure read 28 or 27 on identical descriptions; `transcript-triage-04` and `new-session-prompt-04` each flipped. A model-arm figure on this corpus carries plus or minus one.

Files: `2026-10-09-deterministic.md`, `2026-10-09-model.md` (before) · `2026-10-09-deterministic-rerun.md`, `2026-10-09-model-rerun.md` (after the trigger pass) · `2026-10-09-deterministic-rerun2.md`, `2026-10-09-model-rerun2.md` (after the edits).

| id | class | expected | lexical before | lexical 21:13 | lexical 23:26 | model before | model 21:13 | model 23:26 |
|---|---|---|---|---|---|---|---|---|
| compress-video-01 | E | compress-video-for-sharing | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) |
| compress-video-02 | E | compress-video-for-sharing | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) |
| handoff-01 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-02 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-03 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-04 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-05 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-06 | E | handoff | ok (handoff) | MISS (other) | MISS (other) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-07 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-08 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-09 | E | handoff | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) | ok (handoff) |
| transcript-triage-01 | T | transcript-triage | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) |
| transcript-triage-02 | T | transcript-triage | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) |
| transcript-triage-03 | T | transcript-triage | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) | ok (transcript-triage) |
| new-session-prompt-01 | T | session-starter-new-session-prompt | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) |
| new-session-prompt-02 | T | session-starter-new-session-prompt | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) |
| channel-method-01 | T | channel-method-first | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) |
| channel-method-02 | T | channel-method-first | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) | ok (channel-method-first) |
| new-session-prompt-03 | D | NONE | MISS (session-starter-new-session-prompt) | MISS (session-starter-new-session-prompt) | MISS (session-starter-new-session-prompt) | MISS (other) | MISS (session-starter-new-session-prompt) | MISS (other) |
| transcript-triage-04 | D | transcript-triage | ok (transcript-triage) | MISS (other) | MISS (other) | MISS (NONE) | MISS (NONE) | ok (transcript-triage) |
| transcript-triage-05 | D | other:other | ok (other) | ok (other) | ok (other) | ok (other) | ok (other) | ok (other) |
| compress-video-03 | D | compress-video-for-sharing | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) | ok (compress-video-for-sharing) |
| compress-video-04 | D | other:other | ok (other) | ok (other) | ok (other) | ok (other) | ok (other) | ok (other) |
| handoff-10 | D | handoff | MISS (NONE) | MISS (other) | MISS (other) | MISS (other) | ok (handoff) | ok (handoff) |
| handoff-11 | D | handoff | MISS (session-starter-new-session-prompt) | MISS (NONE) | MISS (NONE) | ok (handoff) | ok (handoff) | ok (handoff) |
| handoff-12 | D | other:other | MISS (handoff) | MISS (handoff) | MISS (handoff) | MISS (other) | MISS (other) | MISS (other) |
| handoff-13 | D | other:other | MISS (handoff) | ok (other) | ok (other) | MISS (other) | MISS (other) | MISS (other) |
| handoff-14 | D | handoff | ok (handoff) | ok (handoff) | ok (handoff) | MISS (other) | ok (handoff) | ok (handoff) |
| new-session-prompt-04 | D | session-starter-new-session-prompt | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) | ok (session-starter-new-session-prompt) |
| handoff-15 | T | handoff | MISS (other) | MISS (other) | MISS (other) | ok (handoff) | ok (handoff) | ok (handoff) |
| value-capture-01 | D | other:other | MISS (other) | ok (other) | ok (other) | ok (other) | ok (other) | ok (other) |

## What moved, before to after the edits

- **lexical**: fixed handoff-13, value-capture-01; newly missed handoff-06, transcript-triage-04; still missed new-session-prompt-03, handoff-10, handoff-11, handoff-12, handoff-15.
- **model**: fixed transcript-triage-04, handoff-10, handoff-14; newly missed none; still missed new-session-prompt-03, handoff-12, handoff-13.

## The new set, after the trigger pass and after the edits (model arm)

- After the trigger pass (94 cases): 86 ok; misses compress-video-07, sidebar-01, transcript-triage-11, sidebar-07, sidebar-08, sidebar-09, sidebar-10, sidebar-11.
- After the edits (102 cases, eight stakeholder cases added): 100 ok; misses compress-video-07, transcript-triage-11.
- The five `sidebar-07` to `-11` misses cleared once the author removed the notes-mode words from the sidebar skill's description: the eval named the over-claim, the edit removed it, the rerun confirmed it. The two that remain are the compress near-miss the model generalises to and "summarise this meeting", which the transcript-triage description does not claim.
- The lexical arm still misses the five sidebar cases and two stakeholder should-nots because those descriptions now mention the phrases as should-nots, and word overlap cannot read a negation. The model arm can. That is the known limit of the baseline, stated in run.py.
