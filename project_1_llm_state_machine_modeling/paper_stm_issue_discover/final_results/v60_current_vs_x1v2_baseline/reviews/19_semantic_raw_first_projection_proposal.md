# Semantic raw-first projection proposal

## Verdict

`FAIL` for the strict sealed-arm claim. This is a provider-free, read-only
`subagent` proposal about the reviewer input projection. It is not a human
adjudication, does not replace pane5 decisions, and assigns no `D/A`,
relation, validity, `K/N/I`, or `W` label to an individual report.

- Reviewer identity: `subagent:semantic-raw-first-projection`
- Provider calls: `0`
- Method/Judge/rejudge calls: `0`
- Frozen raw changes: `0`
- Canonical decision changes: `0`
- Evidence used for this proposal: frozen method raw, frozen NL/PlantUML,
  `reviewer_input_projection.jsonl`, its audit, the projection builder,
  projection-only validator, and the current semantic protocol.
- No primary decision, legacy reference label, or other review conclusion is
  cited as evidence below.

The projection has a uniform field schema, closes mechanically over the raw
reports, and suppresses the listed provider and semantic-label fields. It
does not, however, keep `arm-a` and `arm-b` sealed from a reviewer who is
allowed to read the frozen raw as this review role requires. The direct target
digest and deterministic pair token recover the source side for every actual
report.

## Stable input snapshot

The following snapshot was stable across three two-second reads before this
proposal was written.

| item | value |
| :-- | :-- |
| projection | `derived/manual_adjudication_v2/reviewer_input_projection.jsonl` |
| projection SHA-256 | `sha256:299eaa144026f64b166a9f79e7e522496a441eed7f9057bcba3925b06a10b95e` |
| audit | `derived/manual_adjudication_v2/reviewer_projection_audit.json` |
| audit SHA-256 | `sha256:c9b1bc7f172013fbc7b31680b8191e222743022002e6d288619a25826b12ee4f` |
| projection rows | `2642` |
| actual raw reports | `1783 = 1271 + 512` |
| padded slots | `859 = 50 + 809` |
| pair/round universe | `162` |

The earlier transient read during concurrent regeneration is not used as
evidence. This proposal uses only the stable hashes above.

## Passing checks

1. The projection-only validator passes after a fresh provider-free
   enumeration of frozen raw: `1783` report items, `162 + 162` cells, and no
   provider call.
2. Both arms expose the same row keys, report-evidence keys, author-source
   keys, pair/round/slot universe, and author-source bytes at each shared
   slot. `arm-a` contains `1271` actual rows plus `50` padding rows; `arm-b`
   contains `512` actual rows plus `809` padding rows.
3. Every actual projected target hash maps once to the appropriate frozen raw
   target: `1271/1271` for `arm-a` and `512/512` for `arm-b`. Reconstructed
   `claim_text`, `reason_text`, `location_text`, pair token, and round match
   the frozen target for all `1783` rows. Author NL/PlantUML content and hashes
   also match for all actual rows.
4. The projection contains none of the audit's forbidden provider, prompt,
   legacy Judge, or semantic-label keys. Padding has null
   `raw_target_sha256` and three empty report-evidence strings; it is not a
   report and must not receive a semantic label.

## Finding

### PRJ-SEM-019-001 [I] Raw-first access defeats the claimed sealed arm mapping

**Paths and pointers:**

- `derived/manual_adjudication_v2/reviewer_projection_audit.json#/policy/side_mapping`
  states that `arm-a/arm-b` is sealed until unblind.
- `scripts/evaluation/build_reviewer_projection.py:147-148` computes
  `raw_target_sha256` as a public SHA-256 of each exact frozen report target.
- `scripts/evaluation/build_reviewer_projection.py:162-166` writes the arm
  token, unsalted pair token, round, slot, and target digest together.
- `scripts/evaluation/build_reviewer_projection.py:163` derives
  `pair_token` directly from the four-digit pair ID using unkeyed SHA-256.
- `discover_matrix/docs/protocol/semantic_judge_protocol.md:78-95` presents
  the projection as the blind common allowlist and calls the arm mapping
  sealed.

**Reason:** The frozen raw is in scope for a raw-first semantic reviewer. A
reviewer can canonicalize each raw report target, hash it with the disclosed
algorithm, and compare it to `raw_target_sha256`. It can likewise enumerate
the fixed corpus IDs and recover `pair_token`. In the stable snapshot, this
recovers `arm-a -> v60_current` for `1271/1271` actual rows and
`arm-b -> x1v2_baseline` for `512/512` actual rows. Therefore the mapping is
not sealed under the stated reviewer-access model.

The same conflict affects W review. The projection intentionally excludes
`execution_receipt`, `predicate_inputs`, `predicate_execution_receipts`,
artifact hash, terminal result, and `witness_level`; reading frozen raw to
inspect current W2 receipts necessarily gives the reviewer the arm mapping.
This is not a claim that baseline needs predicate evidence. It is a conflict
between a sealed-arm blind review and direct raw evidence access.

**Basis:** Direct provider-free enumeration found unique target digests for
all `1271` current and `512` baseline report objects, and a zero-error
projection-to-raw reconstruction for all `1783` actual rows. The projection
does not contain any of the W2 proof keys. Current raw report targets expose
receipt-related fields; baseline raw report targets do not expose the same
schema. No semantic label from those fields was used in this proposal.

**Reproduction:**

```bash
ROOT=project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation:project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
  python - <<'PY'
from pathlib import Path
from validate_manual_adjudication import build_inventory_from_archive, validate_reviewer_projection

root = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline").resolve()
validate_reviewer_projection(root / "derived/manual_adjudication_v2", build_inventory_from_archive(root))
print("projection-only validation PASS")
PY

sha256sum "$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl" \
  "$ROOT/derived/manual_adjudication_v2/reviewer_projection_audit.json"
wc -l "$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
```

To reproduce the side-reidentification result, enumerate frozen
`report_issue_clusters` and `parsed_output.issues`, serialize each target with
`ensure_ascii=False`, `sort_keys=True`, and `separators=(',', ':')`, then
compare the SHA-256 to `raw_target_sha256`. The builder provides the exact
algorithm at `scripts/evaluation/build_reviewer_projection.py:36-54`.

**Disposition:** `open; required protocol or projection repair`. A repair
must choose one coherent policy:

- make the raw-first proposal arm-unblinded and remove the false sealed-arm
  claim, while retaining blindness to primary/reference labels; or
- keep arm blindness by withholding the direct raw-target and reversible pair
  mapping from the reviewer-visible projection, with a separately controlled
  post-submission evidence/receipt audit.

Either path must describe when relation and W2 evidence becomes available and
must be re-reviewed against the regenerated projection. No frozen raw,
canonical decision, or existing method result needs to change.

**Repair commit:** `not available`.

**Targeted rereview:** `NOT RUN`; this reviewer is read-only and the finding
remains open in the stable projection snapshot.

## Scope boundary

The raw-first projection is adequate for an initial fact/D-A proposal on its
`1783` non-padding rows: it provides the report's prose/locus, complete author
NL, complete author PlantUML, round, a stable review key, and source hashes.
It deliberately cannot itself assign an expected-specific
`FULL_MATCH/PARTIAL_MATCH/NO_MATCH` relation because the expected ledger is
absent. It also cannot itself establish W2 because the terminal receipt,
typed input, and evaluated-artifact evidence are absent. The protocol states
this deferral at `semantic_judge_protocol.md:91-94`; it is a review-stage
boundary, not an automatic `NO_MATCH`, `W0`, `INVALID`, or semantic finding.

Accordingly, this proposal does not certify a full report-level semantic
review. It certifies the structural checks above and records the sealed-arm
contradiction that must be resolved before such a blind-review claim can pass.
