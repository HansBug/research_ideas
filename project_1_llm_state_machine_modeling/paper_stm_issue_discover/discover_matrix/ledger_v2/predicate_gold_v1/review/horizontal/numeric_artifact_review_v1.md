# Predicate gold v1 numeric/artifact horizontal review

Reviewer ID: `codex:predicate-gold-v1-numeric-artifact-horizontal-r1`

Review result: **FAIL** for the release gate, with **no canonical decision impact**. The sole failure is a stale canonical hash in the saved full-replay report. All independently recomputed canonical counts, mirrors, review coverage, source pointers, receipts, and expected-vs-actual metrics pass.

## Inputs

| Input | SHA-256 |
| --- | --- |
| `predicate_gold_v1.json` | `4b1c1db4b8fc084f0302913a62a01743807ad3f642fab2c01db163f94a4532fc` |
| `predicate_gold_v1.schema.json` | `e7a341a3b75da5dffef65f71581aadac50e0c2d7ee489133e9f06248aa3f06a3` |
| `predicate_gold_v1.tsv` | `8f9062c7870d0e78350ca5fcb34398903b188464c21b19739c8688b549f45ff2` |
| `summary.json` | `160fc419a465d7f447414f99cf3154958320a7a2f95e36da4db2682e955c2d6a` |
| `inventory.json` | `31385c7448d3102a0d5c2f9b9c2afaa62df08cdf78e52a4e34c1df7fd4231672` |
| `review/active_review_manifest.json` | `8d8ea606d161fd228ed9db8af5056a5a02de9b9a66fe4b2097f4f7aa8a8b8da5` |
| `review/horizontal/full_replay_validation.json` | `a1338c52e63c9fccf7256b8eca07c736e842b7cf1ca46edb3c70e32dea59e284` |
| `expected_vs_actual_v60.json` | `b4ed4d82f7f4edf826e74b43fbb0c92b5194a147bb084a5b57d582d1499b2d35` |
| `expected_vs_actual_v60.tsv` | `de3b523a9442aa22eb2e40919e228a842f0df00b2da50f4cc01ab7cd57abe962` |
| `receipts/` deterministic tree, 1152 files | `29bcd2d777da191da7d3499d93fe8620d1a891349ab18649c70669ff4f46cd04` |

## Recomputed facts

| Check | Result | Recomputed value |
| --- | --- | --- |
| Ledger ID closure | PASS | 145 rows, 145 unique IDs, no missing or extra ID |
| Family | PASS | `EIS=90`, `INS=35`, `VU=12`, `DIFF=8` |
| D tier | PASS | `D2=98`, `D1=47` |
| L tier | PASS | `L2=39`, `L1=35`, `L0=71` |
| Gold status | PASS | `EXACT_FALSE=8`, `COMPOSITE_EXACT_FALSE=5`, `SOUND_FALSE_PROXY=34`, `UNSUPPORTED_EXACT=98`, `BLOCKED_EXECUTION=0` |
| Execution closure | PASS | 47 completed false, 47 completed-true controls, 94 matching role replays |
| Four review tracks | PASS | A/B/C/fourth each 145/145; final arbitration 145/145 |
| Canonical references | PASS | 10,300 refs over 1,042 paths; 0 missing, 0 hash mismatch, 0 invalid JSON pointer |
| JSON/TSV/schema/summary | PASS | 145-row mirrors and schema all agree |
| Expected-vs-actual | PASS | `FULL=119/145`, `supported=128/145` |
| Current raw relation refs | PASS | 964 report refs over 135 raw paths; all hashes and pointers valid |

The 19-predicate usage recomputation also matches `summary.json`. Nonzero exact/proxy counts are `S1=0/3`, `S2=0/1`, `S3=3/1`, `S4=2/2`, `S5=3/0`, and `G1=0/6`. `S6`, `G2-G4`, `R1-R4`, and `V1-V5` are all `0/0`. The separate `EVALUATION_ONLY` bucket is `8 exact / 21 proxy`; `UNSUPPORTED=98`.

All five composite rows were checked, not sampled: `DIFF-0016-05`, `DIFF-0019-05`, `EIS-0034-03`, `INS-0000-04`, and `INS-0017-01`. Their defective and control receipts set `no_short_circuit=true`; all 15 defective and all 15 control constituents have completed Boolean receipts. The parent `AND` or `NOT` verdict agrees with the complete constituent vector.

The expected-vs-actual result was rebuilt directly from the 1,271 frozen current-v4 decisions. It yields the same 119 FULL IDs and 128 FULL-or-PARTIAL IDs. Four issues retain `EXPECTED_ID_INPUT_NOT_OBSERVABLE`: `DIFF-0016-05`, `EIS-0007-02`, `INS-0000-04`, and `INS-0017-01`, covering 24 report cells. This is an explicit `NOT_OBSERVABLE_FROM_RAW` analysis result, not an omitted input.

## Failure

`NA-F-001` is release-blocking:

- Path: `review/horizontal/full_replay_validation.json`
- JSON pointer: `/canonical_sha256`
- Stored: `sha256:4225ba90bd60371bcd2e842829d138cd132376bdc02e067f3d764268e2ba924b`
- Current canonical: `sha256:4b1c1db4b8fc084f0302913a62a01743807ad3f642fab2c01db163f94a4532fc`

The replay report itself says PASS for 47 issues and 94 role receipts, and its payload hash is internally valid, but it was generated against an earlier canonical assembly. Direct inspection of the current canonical and all saved receipts passed, so this finding does not invalidate or change any canonical decision. It does prevent the current replay artifact from closing the release hash chain.

Pane5 must rerun the provider-free full replay against the current canonical, regenerate `full_replay_validation.json`, and refresh any release/active manifest hash that binds it. The corrected report must carry canonical hash `4b1c1db4b8fc084f0302913a62a01743807ad3f642fab2c01db163f94a4532fc`. No canonical decision should be edited.

## Commands

The review used `sha256sum` for byte hashes and read-only Python/JQ passes to validate JSON Schema, compare TSV mirrors, resolve every path/hash/JSON pointer, enumerate active-manifest review rows, inspect all 47 defective/control/replay triples, evaluate every composite constituent, and independently project FULL/PARTIAL relations from `current_report_decisions_v4.json`. No method, Judge, provider, or experiment command was invoked.
