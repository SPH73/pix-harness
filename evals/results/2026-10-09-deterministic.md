# Results: deterministic arm, 2026-10-09

- Field: 234 candidate skills, skills snapshot of 2026-10-08.
- Cases: 32 (1 canary).
- Scorer: lexical, IDF-weighted overlap, threshold 0.5.
- This is a worked example of the method, not a coverage figure or a benchmark of a model.

| Skill | n | precision | recall | tp | fp | fn | note |
|---|---|---|---|---|---|---|---|
| `channel-method-first` | 2 | n/a | n/a | 2 | 0 | 0 | too few to score |
| `compress-video-for-sharing` | 3 | 1.00 | 1.00 | 3 | 0 | 0 |  |
| `handoff` | 13 | 0.83 | 0.77 | 10 | 2 | 3 |  |
| `session-starter-new-session-prompt` | 3 | 0.60 | 1.00 | 3 | 2 | 0 |  |
| `transcript-triage` | 4 | 1.00 | 1.00 | 4 | 0 | 0 |  |
| `verify-before-quoting` | 0 | n/a | n/a | 0 | 0 | 0 | too few to score |

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
| handoff-06 | E | handoff | handoff | ok | 1.00 |
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
| new-session-prompt-03 | D | NONE | session-starter-new-session-prompt | MISS | 0.57 |
| transcript-triage-04 | D | transcript-triage | transcript-triage | ok | 0.95 |
| transcript-triage-05 | D | other:other | other | ok | 0.79 |
| compress-video-03 | D | compress-video-for-sharing | compress-video-for-sharing | ok | 0.76 |
| compress-video-04 | D | other:other | other | ok | 0.95 |
| handoff-10 | D | handoff | NONE | MISS | 0.43 |
| handoff-11 | D | handoff | session-starter-new-session-prompt | MISS | 0.59 |
| handoff-12 | D | other:other | handoff | MISS | 0.95 |
| handoff-13 | D | other:other | handoff | MISS | 0.95 |
| handoff-14 | D | handoff | handoff | ok | 0.60 |
| new-session-prompt-04 | D | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.81 |
| handoff-15 | T | handoff | other | MISS | 0.88 |
| value-capture-01 | D | other:other | other | MISS | 0.65 |

Canary: bit.
