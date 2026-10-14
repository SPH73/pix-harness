# Results: model arm, 2026-10-14

- Field: 46 candidate skills, trimmed live field, descriptions frozen 13 Oct 14:59 BST; snapshot 14 Oct 16:47 BST, built from the live-set list into a private snapshot repository, snapshot 2026-10-14-trimmed-held-out; descriptions sha256 d807c5bb430ed3bd; private snapshot repository HEAD 131db71 (snapshot uncommitted until the 23:20 nightly; matches 131db71 bar MANIFEST.md); this repository, a pre-publication commit; held-out set: this repository, a pre-publication commit.
- Cases: 38 (1 canary).
- Scorer: model claude-opus-5-5, effort low.
- Answering model: claude-opus-5-5 (38 of 38 calls). Found by: response.model (no fallback entry) 38.
- This is a worked example of the method, not a coverage figure or a benchmark of a model.

| Skill | n | precision | recall | tp | fp | fn | note |
|---|---|---|---|---|---|---|---|
| `channel-method-first` | 5 | 1.00 | 1.00 | 5 | 0 | 0 |  |
| `compress-video-for-sharing` | 5 | 1.00 | 1.00 | 5 | 0 | 0 |  |
| `handoff` | 5 | 1.00 | 0.60 | 3 | 0 | 2 |  |
| `session-starter-new-session-prompt` | 5 | 1.00 | 0.80 | 4 | 0 | 1 |  |
| `transcript-triage` | 5 | 1.00 | 1.00 | 5 | 0 | 0 |  |
| `verify-before-quoting` | 6 | 1.00 | 0.50 | 3 | 0 | 3 | asymmetric: recall is the metric; false positives are specified behaviour |

| id | class | expected | predicted | result | score |
|---|---|---|---|---|---|
| ho-handoff-01 | T | handoff | handoff | ok | 1.00 |
| ho-handoff-02 | T | handoff | handoff | ok | 1.00 |
| ho-handoff-03 | T | handoff | handoff | ok | 1.00 |
| ho-handoff-04 | T | handoff | NONE | MISS | 1.00 |
| ho-handoff-05 | T | handoff | NONE | MISS | 1.00 |
| ho-compress-video-01 | T | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| ho-compress-video-02 | T | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| ho-compress-video-03 | T | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| ho-compress-video-04 | T | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| ho-compress-video-05 | T | compress-video-for-sharing | compress-video-for-sharing | ok | 1.00 |
| ho-transcript-triage-01 | T | transcript-triage | transcript-triage | ok | 1.00 |
| ho-transcript-triage-02 | T | transcript-triage | transcript-triage | ok | 1.00 |
| ho-transcript-triage-03 | T | transcript-triage | transcript-triage | ok | 1.00 |
| ho-transcript-triage-04 | T | transcript-triage | transcript-triage | ok | 1.00 |
| ho-transcript-triage-05 | T | transcript-triage | transcript-triage | ok | 1.00 |
| ho-verify-before-quoting-01 | T | verify-before-quoting | other | MISS | 1.00 |
| ho-verify-before-quoting-02 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| ho-verify-before-quoting-03 | T | verify-before-quoting | other | MISS | 1.00 |
| ho-verify-before-quoting-04 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| ho-verify-before-quoting-05 | T | verify-before-quoting | verify-before-quoting | ok | 1.00 |
| ho-verify-before-quoting-06 | T | verify-before-quoting | NONE | MISS | 1.00 |
| ho-new-session-prompt-01 | T | session-starter-new-session-prompt | NONE | MISS | 1.00 |
| ho-new-session-prompt-02 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| ho-new-session-prompt-03 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| ho-new-session-prompt-04 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| ho-new-session-prompt-05 | T | session-starter-new-session-prompt | session-starter-new-session-prompt | ok | 1.00 |
| ho-channel-method-01 | T | channel-method-first | channel-method-first | ok | 1.00 |
| ho-channel-method-02 | T | channel-method-first | channel-method-first | ok | 1.00 |
| ho-channel-method-03 | T | channel-method-first | channel-method-first | ok | 1.00 |
| ho-channel-method-04 | T | channel-method-first | channel-method-first | ok | 1.00 |
| ho-channel-method-05 | T | channel-method-first | channel-method-first | ok | 1.00 |
| ho-none-handoff-01 | N | NONE | NONE | ok | 1.00 |
| ho-none-transcript-triage-01 | N | other:other | other | ok | 1.00 |
| ho-none-verify-before-quoting-01 | N | NONE | NONE | ok | 1.00 |
| ho-none-new-session-prompt-01 | N | other:other | other | ok | 1.00 |
| ho-none-channel-method-01 | N | other:other | other | ok | 1.00 |
| ho-none-compress-video-01 | N | other:other | other | ok | 1.00 |
| canary-01 | C | transcript-triage | compress-video-for-sharing | MISS | 1.00 |

Canary: bit.

