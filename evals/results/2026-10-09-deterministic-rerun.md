# Results: deterministic arm, 2026-10-09

- Field: 235 candidate skills, skills snapshot of 2026-10-09 21:13 BST, after the trigger-phrase pass.
- Cases: 126 (1 canary).
- Scorer: lexical, IDF-weighted overlap, threshold 0.5.
- This is a worked example of the method, not a coverage figure or a benchmark of a model.

| Skill | n | precision | recall | tp | fp | fn | note |
|---|---|---|---|---|---|---|---|
| `channel-method-first` | 8 | 0.80 | 1.00 | 8 | 2 | 0 |  |
| `compress-video-for-sharing` | 6 | 0.86 | 1.00 | 6 | 1 | 0 |  |
| `handoff` | 16 | 0.77 | 0.62 | 10 | 3 | 6 |  |
| `session-starter-new-session-prompt` | 7 | 0.83 | 0.71 | 5 | 1 | 2 |  |
| `transcript-triage` | 8 | 1.00 | 0.88 | 7 | 0 | 1 |  |
| `verify-before-quoting` | 7 | 1.00 | 1.00 | 7 | 0 | 0 | asymmetric: recall is the metric; false positives are specified behaviour |

| id | class | expected | predicted | result | score |
|---|---|---|---|---|---|
| canary-01 | C | transcript-triage | compress-video-for-sharing | MISS | 1.00 |
| compress-video-01 | E | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| compress-video-02 | E | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| handoff-01 | E | handoff | handoff | ok | 1.00 |
| handoff-02 | E | handoff | handoff | ok | 1.00 |
| handoff-03 | E | handoff | handoff | ok | 1.00 |
| handoff-04 | E | handoff | handoff | ok | 1.00 |
| handoff-05 | E | handoff | handoff | ok | 1.00 |
| handoff-06 | E | handoff | other | MISS | 1.00 |
| handoff-07 | E | handoff | handoff | ok | 1.00 |
| handoff-08 | E | handoff | handoff | ok | 1.00 |
| handoff-09 | E | handoff | handoff | ok | 1.00 |
| transcript-triage-01 | T | transcript-triage | transcript-triage | ok | 1.00 |
| transcript-triage-02 | T | transcript-triage | transcript-triage | ok | 1.00 |
| transcript-triage-03 | T | transcript-triage | transcript-triage | ok | 1.00 |
| new-session-prompt-01 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| new-session-prompt-02 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| channel-method-01 | T | channel-method-first | channel-method-first | ok | 1.00 |
| channel-method-02 | T | channel-method-first | channel-method-first | ok | 1.00 |
| new-session-prompt-03 | D | NONE | session-starter-new-session-prompt | MISS | 0.55 |
| transcript-triage-04 | D | transcript-triage | other | MISS | 0.95 |
| transcript-triage-05 | D | other:other | other | ok | 0.78 |
| compress-video-03 | D | compress-video-for-sharing | compress-video-for-sharing | ok | 0.76 |
| compress-video-04 | D | other:other | other | ok | 0.95 |
| handoff-10 | D | handoff | other | MISS | 0.52 |
| handoff-11 | D | handoff | NONE | MISS | 0.38 |
| handoff-12 | D | other:other | handoff | MISS | 0.95 |
| handoff-13 | D | other:other | other | ok | 0.70 |
| handoff-14 | D | handoff | handoff | ok | 0.60 |
| new-session-prompt-04 | D | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.85 |
| handoff-15 | T | handoff | other | MISS | 0.88 |
| value-capture-01 | D | other:other | other | ok | 1.00 |
| new-session-prompt-05 | D | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.95 |
| compress-video-05 | T | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| compress-video-06 | E | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| compress-video-07 | D | NONE | compress-video-for-sharing | MISS | 0.95 |
| compress-video-08 | D | compress-video-for-sharing | compress-video-for-sharing | ok | 0.95 |
| transcript-triage-06 | T | transcript-triage | transcript-triage | ok | 1.00 |
| transcript-triage-07 | T | transcript-triage | transcript-triage | ok | 1.00 |
| transcript-triage-08 | D | transcript-triage | transcript-triage | ok | 0.95 |
| transcript-triage-09 | D | other:other | other | MISS | 0.75 |
| transcript-triage-10 | D | other:other | other | ok | 1.00 |
| handoff-16 | T | handoff | other | MISS | 1.00 |
| handoff-17 | D | NONE | handoff | MISS | 1.00 |
| handoff-18 | T | handoff | handoff | ok | 0.95 |
| handoff-19 | D | handoff | other | MISS | 0.86 |
| handoff-20 | D | NONE | handoff | MISS | 0.95 |
| new-session-prompt-06 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| new-session-prompt-07 | D | session-starter-new-session-prompt | other | MISS | 0.95 |
| new-session-prompt-08 | D | session-starter-new-session-prompt | other | MISS | 0.95 |
| channel-method-03 | T | channel-method-first | channel-method-first | ok | 1.00 |
| channel-method-04 | T | channel-method-first | channel-method-first | ok | 1.00 |
| channel-method-05 | T | channel-method-first | channel-method-first | ok | 1.00 |
| channel-method-06 | T | channel-method-first | channel-method-first | ok | 1.00 |
| channel-method-07 | T | channel-method-first | channel-method-first | ok | 1.00 |
| channel-method-08 | T | channel-method-first | channel-method-first | ok | 1.00 |
| verify-before-quoting-01 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| verify-before-quoting-02 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| verify-before-quoting-03 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| verify-before-quoting-04 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| verify-before-quoting-05 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| verify-before-quoting-06 | D | verify-before-quoting | verify-before-quoting | ok | 0.61 |
| verify-before-quoting-07 | D | verify-before-quoting | verify-before-quoting | ok | 0.95 |
| handoff-21 | D | NONE | other | MISS | 0.95 |
| channel-method-09 | D | other:other | channel-method-first | MISS | 0.93 |
| channel-method-10 | D | NONE | NONE | ok | 0.46 |
| channel-method-11 | D | other:other | channel-method-first | MISS | 0.91 |
| verify-before-quoting-08 | D | other:other | other | ok | 0.76 |
| verify-before-quoting-09 | D | NONE | NONE | ok | 0.48 |
| block-briefing-01 | T | other:other | other | ok | 0.95 |
| block-briefing-02 | T | other:other | other | ok | 1.00 |
| block-briefing-03 | T | other:other | other | ok | 1.00 |
| block-briefing-04 | T | other:other | other | ok | 1.00 |
| block-briefing-05 | T | other:other | other | ok | 1.00 |
| block-briefing-06 | D | other:other | other | ok | 0.95 |
| block-briefing-07 | D | other:other | other | ok | 0.66 |
| block-briefing-08 | D | other:other | other | ok | 0.95 |
| value-capture-02 | D | NONE | other | MISS | 1.00 |
| whole-first-01 | T | other:other | other | ok | 1.00 |
| whole-first-02 | T | other:other | other | ok | 1.00 |
| whole-first-03 | T | other:other | other | ok | 1.00 |
| whole-first-04 | T | other:other | other | ok | 1.00 |
| whole-first-05 | T | other:other | other | ok | 1.00 |
| whole-first-06 | D | other:other | other | MISS | 0.95 |
| whole-first-07 | D | other:other | other | ok | 0.74 |
| whole-first-08 | D | other:other | other | MISS | 0.71 |
| consistency-01 | T | other:other | other | ok | 1.00 |
| consistency-02 | T | other:other | other | ok | 1.00 |
| consistency-03 | T | other:other | other | ok | 1.00 |
| consistency-04 | T | other:other | other | ok | 1.00 |
| consistency-05 | D | other:other | other | ok | 1.00 |
| consistency-06 | D | NONE | other | MISS | 0.56 |
| consistency-07 | D | other:other | other | ok | 0.69 |
| consistency-08 | D | NONE | other | MISS | 0.59 |
| consistency-09 | D | other:other | other | MISS | 0.63 |
| consistency-10 | D | other:other | other | ok | 0.95 |
| guide-pix-01 | T | other:other | other | ok | 1.00 |
| guide-pix-02 | T | other:other | other | ok | 1.00 |
| guide-pix-03 | T | other:other | other | ok | 1.00 |
| guide-pix-04 | T | other:other | other | ok | 1.00 |
| guide-pix-05 | T | other:other | other | ok | 1.00 |
| guide-pix-06 | D | NONE | other | MISS | 1.00 |
| facts-01 | T | other:other | other | ok | 1.00 |
| facts-02 | T | other:other | other | ok | 1.00 |
| facts-03 | T | other:other | other | ok | 1.00 |
| facts-04 | T | other:other | other | ok | 1.00 |
| facts-05 | T | other:other | other | ok | 1.00 |
| facts-06 | T | other:other | other | ok | 1.00 |
| sidebar-01 | D | NONE | other | MISS | 0.95 |
| sidebar-02 | T | other:other | other | ok | 1.00 |
| sidebar-03 | T | other:other | other | ok | 1.00 |
| sidebar-04 | T | other:other | other | ok | 1.00 |
| sidebar-05 | T | other:other | other | ok | 1.00 |
| oem-profile-01 | T | other:other | other | ok | 1.00 |
| oem-profile-02 | T | other:other | other | ok | 1.00 |
| oem-profile-03 | T | other:other | other | ok | 1.00 |
| oem-profile-04 | D | other:other | other | ok | 0.95 |
| oem-profile-05 | D | other:other | other | MISS | 0.81 |
| acceptance-01 | D | other:other | other | MISS | 0.81 |
| transcript-triage-11 | D | transcript-triage | transcript-triage | ok | 0.81 |
| sidebar-06 | T | other:other | other | ok | 0.95 |
| sidebar-07 | D | NONE | other | MISS | 0.71 |
| sidebar-08 | D | NONE | other | MISS | 1.00 |
| sidebar-09 | D | NONE | other | MISS | 1.00 |
| sidebar-10 | D | NONE | other | MISS | 1.00 |
| sidebar-11 | D | NONE | other | MISS | 1.00 |

Canary: bit.

