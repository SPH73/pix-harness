# Results: deterministic arm, 2026-10-14

- Field: 236 candidate skills, full skills snapshot of 14 Oct 16:47 BST, descriptions frozen 13 Oct 14:59 BST (236 skills); descriptions sha256 6eba411b9bec3bab; private snapshot repository HEAD 131db71 (snapshot uncommitted until the 23:20 nightly; matches 131db71 bar MANIFEST.md); this repository, a pre-publication commit; held-out set: this repository, a pre-publication commit.
- Cases: 38 (1 canary).
- Scorer: lexical, IDF-weighted overlap, threshold 0.5.
- This is a worked example of the method, not a coverage figure or a benchmark of a model.

| Skill | n | precision | recall | tp | fp | fn | note |
|---|---|---|---|---|---|---|---|
| `channel-method-first` | 5 | 1.00 | 0.40 | 2 | 0 | 3 |  |
| `compress-video-for-sharing` | 5 | n/a | 0.00 | 0 | 0 | 5 |  |
| `handoff` | 5 | n/a | 0.00 | 0 | 0 | 5 |  |
| `session-starter-new-session-prompt` | 5 | 1.00 | 0.80 | 4 | 0 | 1 |  |
| `transcript-triage` | 5 | 1.00 | 0.20 | 1 | 0 | 4 |  |
| `verify-before-quoting` | 6 | 0.50 | 0.17 | 1 | 1 | 5 | asymmetric: recall is the metric; false positives are specified behaviour |

| id | class | expected | predicted | result | score |
|---|---|---|---|---|---|
| ho-handoff-01 | T | handoff | NONE | MISS | 0.29 |
| ho-handoff-02 | T | handoff | NONE | MISS | 0.33 |
| ho-handoff-03 | T | handoff | NONE | MISS | 0.24 |
| ho-handoff-04 | T | handoff | other | MISS | 0.54 |
| ho-handoff-05 | T | handoff | other | MISS | 0.60 |
| ho-compress-video-01 | T | compress-video-for-sharing | other | MISS | 0.68 |
| ho-compress-video-02 | T | compress-video-for-sharing | other | MISS | 0.70 |
| ho-compress-video-03 | T | compress-video-for-sharing | NONE | MISS | 0.38 |
| ho-compress-video-04 | T | compress-video-for-sharing | other | MISS | 0.60 |
| ho-compress-video-05 | T | compress-video-for-sharing | NONE | MISS | 0.35 |
| ho-transcript-triage-01 | T | transcript-triage | transcript-triage | ok | 0.56 |
| ho-transcript-triage-02 | T | transcript-triage | NONE | MISS | 0.37 |
| ho-transcript-triage-03 | T | transcript-triage | NONE | MISS | 0.32 |
| ho-transcript-triage-04 | T | transcript-triage | NONE | MISS | 0.48 |
| ho-transcript-triage-05 | T | transcript-triage | NONE | MISS | 0.48 |
| ho-verify-before-quoting-01 | T | verify-before-quoting | other | MISS | 0.53 |
| ho-verify-before-quoting-02 | T | verify-before-quoting | verify-before-quoting | ok | 0.93 |
| ho-verify-before-quoting-03 | T | verify-before-quoting | other | MISS | 0.95 |
| ho-verify-before-quoting-04 | T | verify-before-quoting | NONE | MISS | 0.41 |
| ho-verify-before-quoting-05 | T | verify-before-quoting | other | MISS | 0.82 |
| ho-verify-before-quoting-06 | T | verify-before-quoting | other | MISS | 0.57 |
| ho-new-session-prompt-01 | T | session-starter-new-session-prompt | NONE | MISS | 0.32 |
| ho-new-session-prompt-02 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.95 |
| ho-new-session-prompt-03 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.75 |
| ho-new-session-prompt-04 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.54 |
| ho-new-session-prompt-05 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 0.83 |
| ho-channel-method-01 | T | channel-method-first | NONE | MISS | 0.26 |
| ho-channel-method-02 | T | channel-method-first | NONE | MISS | 0.28 |
| ho-channel-method-03 | T | channel-method-first | NONE | MISS | 0.49 |
| ho-channel-method-04 | T | channel-method-first | channel-method-first | ok | 0.95 |
| ho-channel-method-05 | T | channel-method-first | channel-method-first | ok | 0.82 |
| ho-none-handoff-01 | N | NONE | other | MISS | 0.80 |
| ho-none-transcript-triage-01 | N | other:other | NONE | MISS | 0.42 |
| ho-none-verify-before-quoting-01 | N | NONE | verify-before-quoting | MISS | 0.61 |
| ho-none-new-session-prompt-01 | N | other:other | other | ok | 0.71 |
| ho-none-channel-method-01 | N | other:other | NONE | MISS | 0.21 |
| ho-none-compress-video-01 | N | other:other | other | MISS | 0.95 |
| canary-01 | C | transcript-triage | compress-video-for-sharing | MISS | 1.00 |

Canary: bit.

