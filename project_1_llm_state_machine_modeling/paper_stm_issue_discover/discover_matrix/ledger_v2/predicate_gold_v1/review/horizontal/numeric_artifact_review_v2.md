# Predicate gold v1 numeric/artifact horizontal re-review v2

Reviewer ID: `codex:predicate-gold-v1-numeric-artifact-horizontal-r2`

Result: **PASS**. The prior `NA-F-001` is **CLOSED**. This re-review did not modify the canonical or any semantic decision.

## Closure

| Evidence | Result |
| --- | --- |
| Current `predicate_gold_v1.json` byte SHA-256 | `4b1c1db4b8fc084f0302913a62a01743807ad3f642fab2c01db163f94a4532fc` |
| Saved replay report `/canonical_sha256` | `4b1c1db4b8fc084f0302913a62a01743807ad3f642fab2c01db163f94a4532fc` |
| Saved replay report file SHA-256 | `db7c3cec79ad57da899ebe503ce3d633c550332b2d50a8af90091b643747ea33` |
| Saved replay report payload SHA-256 | `675f6cfee31a27eb3ad7fba81e1e47863909fa01244ab6590d738778fa16b0f2` |
| Repaired replay implementation SHA-256 | `3185b8dc1a7620dc7d3e52bf4f5a91b1431ec582a64bfa7cc75fb27d12a2bfbf` |
| Independent provider-free replay | PASS: 47 issues, 94 receipts |
| Saved versus independent replay rows | Identical, 94/94 |

The repaired implementation uses `sha256_path(canonical_path)` at `predicate_gold_replay_all.py:173`. This hashes the canonical file bytes directly. It therefore closes the exact defect reported in v1, where the replay report carried the hash of an earlier canonical assembly.

The v1 review remains unchanged and traceable:

- `numeric_artifact_review_v1.json`: `cb01fd1fce4621cdff474b1bc24675eb0eecd750bd294c0435f5a036f6b03eb1`
- `numeric_artifact_review_v1.md`: `fb298b7a394b68a5e76417782c30bd32d99216c2a38f8ae160c807220cd71411`

## Independent replay

The re-review ran the provider-free replay module against the current canonical and directed all generated evidence to temporary directories. The command returned `PASS executable=47 receipts=94`.

The PASS line was not accepted on its own. A separate read-only validator checked:

- exactly 47 executable ledger IDs from the current canonical;
- exactly one `DEFECTIVE` and one `POSITIVE_CONTROL` row per ID;
- 47 completed Boolean `false` defective results;
- 47 completed Boolean `true` positive controls;
- all 94 `request_sha256`, roles, states, verdicts, saved paths, and constituent counts against the persisted receipts;
- the saved report's payload self-hash;
- complete equality of all 94 saved rows with the independently generated rows.

All checks passed. Temporary replay directories were cleaned, and no receipt or canonical file was overwritten.

## Finding status

| Finding | v1 | v2 | Canonical impact |
| --- | --- | --- | --- |
| `NA-F-001` stale `/canonical_sha256` in `full_replay_validation.json` | FAIL | CLOSED | None |

There are no remaining findings in this re-review scope. Counters remain `provider_experiment_calls=0`, `method_reruns=0`, `judge_reruns=0`, and `full_experiment_reruns=0`.
