# Evidence correction log

## Scope

Track C rejected the first batch-01 execution packet because its recorded
proposal/control times were later than the execution receipts, its submitted
preflight digests did not satisfy the documented canonical JSON rule, and the
`EIS-0004-01` unary `NOT` receipt described an `AND` truth function. The
rejected bytes and review remain under `attempt_01_rejected/`; they are
historical evidence and are not release evidence.

No ledger row, author artifact, frozen method predicate, Track A opinion or
Track B proposal was changed by this correction.

## Corrected layer

| Item | Corrected evidence |
| --- | --- |
| Batch-01 preflight | `../track_c_preflight_corrected/batch_01a.json`; 15 row digests and the batch digest were recomputed, with no semantic-field change |
| Batch-02 preflight | `../track_c_preflight_corrected/batch_02a.json`; submitted row and batch digests already recomputed correctly, so the corrected copy is byte-equivalent in semantic and digest fields |
| Batch-01 requests | `../../receipts/batch_01a_request_manifest.json`; proposal freeze time `2026-08-30T21:48:42Z` |
| Batch-02 requests | `../../receipts/batch_02a_request_manifest.json`; proposal freeze time `2026-08-30T21:48:42Z` |
| Corrected Track C packets | `../track_c_input/batch_01a_corrected/` and `../track_c_input/batch_02a_corrected/` |

The corrected batch-01 preflight batch digest is
`sha256:f6b317c339cdc99b49d2b3065046afe3dd27a1e0e1c200a180417bf7932b190d`.
The batch-02 digest remains
`sha256:02ec98c0febe0159c84ae1d392ff6bbcaf76f7a05bac2d0b4910b793812f6b88`.
Per-row old/new digests and exact source/output file hashes are in the two
`track_c_preflight_corrected/*_correction_log.json` files.

## Mechanical recheck

The corrected evidence covers 11 executed issues. For every issue:

- the proposal `created_at` precedes the defective receipt `started_at`;
- the defective run completed with Boolean `false`;
- the precommitted positive control completed with Boolean `true`;
- defective and control semantic replays report `overall_match=true`.

The `predicate_gold_composite.py` receipt text now branches on the declared
operator. A completed unary `NOT` receipt states that the parent verdict is the
logical negation of its single constituent and cites the unary `NOT` truth
function. This prose change does not alter the Boolean implementation.

Track C must independently re-review the corrected packet manifests. The old
FAIL remains valid for `attempt_01_rejected/`; only a new hash-bound corrected
review can release these rows.
