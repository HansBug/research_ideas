# Raw-First Semantic Projection Review

Status: **FAIL (proposal-only)**

Reviewer: `subagent:semantic-raw-first-projection-postfix`. This is a blind
projection review, not a semantic verdict or an attestation. It made no
provider call and did not read canonical decisions, old labels or reviews,
`review_log`, pane5 files, unblind mappings, inventories, raw files, or raw
paths.

## Declared Inputs

The review read only these inputs:

1. `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`
2. `derived/manual_adjudication_v2/reviewer_projection_audit.json`
3. `discover_matrix/docs/protocol/semantic_judge_protocol.md`, lines 1--110

No other repository file informed the result.

## Checks That Passed

The following provider-free command parsed only the three declared inputs and
checked all assertions in memory:

```text
python - <<'PY'
# Read reviewer_input_projection.jsonl, reviewer_projection_audit.json,
# and semantic_judge_protocol.md[:110] only; assert row/arm/tuple/padding,
# exact key allowlist, forbidden-key absence, no arrays, and SHA-256 equality.
PY
```

- Projection row count is `2642`; audit `row_count` is also `2642`.
- Arm counts are exactly `arm-a=1321` and `arm-b=1321`.
- The `(pair_token, round, slot)` universe has `1321` units. Every unit has
  exactly one row from each arm; no tuple is missing or duplicated.
- Root-field allowlist observed on every row is exactly
  `schema`, `arm_token`, `pair_token`, `round`, `slot`, `review_key`,
  `report_evidence`, `author_source`, `redactions_applied`, and
  `projection_sha256`. Nested fields are exactly the three text fields
  (`claim_text`, `reason_text`, `location_text`) and the NL/PlantUML text plus
  their author-source hashes.
- No row contains an array. No field name contains `raw`, `target`, `pointer`,
  `report_id`, `issue_id`, `finding_id`, `element`, or `elements`; the audit's
  declared forbidden semantic/provider fields are also absent. The permitted
  `location_text` is a string, not an element array.
- There are `859` padded rows and `1783` non-padded rows, agreeing with audit
  metadata. Each padded row has empty report evidence, retains author-source
  text/hashes, and shares that author-source tuple with its other-arm peer.
  Each non-padded row has nonempty claim/reason/location text. This agrees
  with the padding contract in
  [semantic_judge_protocol.md](../../../discover_matrix/docs/protocol/semantic_judge_protocol.md)
  (line 91).
- File SHA-256 is
  `sha256:1d9b879cab647246ad1e35e8be37dc544aa88a09095120f4ab35ea98be05ef82`,
  exactly matching audit `/projection_sha256`; audit declares `provider_calls=0`.

## Finding

`SEM20-I001` (`I`, protocol/projection opacity contract conflict): the actual
projection correctly omits `raw_target_sha256`, but
[semantic_judge_protocol.md](../../../discover_matrix/docs/protocol/semantic_judge_protocol.md)
(line 89)
lists ``raw_target_sha256`` as a “unified projection field.” This conflicts
with the actual blind-input allowlist above, the same protocol's exclusion of
raw-only audit material at lines 91--95, and the required raw-first opacity
discipline for this review. A future builder following line 89 could expose a
raw-target hash in the blind projection or falsely report an absent required
field.

Reason: current opacity is good because the field is absent, but the written
contract is not unambiguous. The inconsistency is material to a blind-review
input boundary, so it is `I`, not a cosmetic wording issue.

Basis: projection leaf-key enumeration; audit `/forbidden_keys`,
`/arm_counts`, `/padded_slot_count`, `/projected_report_count`, and
`/projection_sha256`; protocol lines 76--95.

Disposition: `PENDING_FIX`. Clarify the protocol table so that only
`author_source.nl_sha256` and `author_source.plantuml_sha256` are blind-input
hashes, and state that `raw_target_sha256` is retained only outside the
raw-first projection. Rebuild and re-audit the projection after the wording
change. Repair commit: none; this reviewer made no repair.

## Conclusion

All present projection rows satisfy the requested opacity, allowlist,
two-arm symmetry, padding, and hash checks. The review remains **FAIL** solely
because `SEM20-I001` leaves the protocol and the actual blind-input contract
in conflict. A targeted rereview should re-run the command above after the
protocol clarification and require the same `2642 = 1321 + 1321`, tuple,
padding, forbidden-key, and SHA-256 checks to pass.
## Post-fix targeted rereview (2026-08-29)

Status: **PASS (proposal-only)**

Reviewer: `subagent:semantic-raw-first-projection-postfix`. This targeted
rereview again read only the sealed inputs below. It did not access this prior
review's findings, canonical decisions, labels, review logs, pane5 files,
unblind mapping contents, inventory, raw files, raw paths, or any provider.

Declared inputs:

1. `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`
2. `derived/manual_adjudication_v2/reviewer_projection_audit.json`
3. `discover_matrix/docs/protocol/semantic_judge_protocol.md`, lines 1--110

Exact provider-free check:

```text
python - <<'PY'
# Read the three declared inputs only. Assert 2642 rows, 1321 rows per arm,
# 1321 identical pair/round/slot units, 859 padding rows, empty location_text
# on every row, no raw-target/pointer/ID/element-array fields, and SHA equality.
PY
```

Evidence and result:

- `2642` projection rows; `arm-a=1321`, `arm-b=1321`; `1321` symmetric
  `(pair_token, round, slot)` units, exactly one row from each arm per unit.
- `859` padding and `1783` non-padding rows match audit. Padding claim and
  reason are empty; non-padding claim and reason are nonempty; both arm rows
  in a unit have identical author-source content and hashes.
- Every `report_evidence.location_text` is the fixed empty string. There are
  no raw-target hashes, raw/pointer/report/issue/finding IDs, element fields,
  or arrays in the projection schema.
- Current projection SHA-256 is
  `sha256:c5c4740293c5e78514016d6211676edfe5e76bd941344a2903662a093a74b68f`,
  exactly equal to audit `/projection_sha256`; audit `/provider_calls` is `0`.
- [semantic_judge_protocol.md](../../../discover_matrix/docs/protocol/semantic_judge_protocol.md)
  (line 84)
  now fixes `location_text` as empty. Lines 91--94 explicitly place raw target
  hash in inventory/canonical audit or sealed `reviewer_unblind_mapping.json`,
  and state that it does not enter blind reviewer input.

`SEM20-I001` disposition: **FIXED; targeted rereview PASS**. The prior
protocol/projection conflict is no longer present: the actual sealed input
omits `raw_target_sha256`, and the protocol now documents that same boundary.
Repair commit: not inspected by this sealed-input reviewer. No new C/I/M
finding was found in the permitted review scope.
