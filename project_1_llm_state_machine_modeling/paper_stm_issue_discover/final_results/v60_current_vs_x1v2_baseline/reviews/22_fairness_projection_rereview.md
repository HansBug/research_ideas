# Targeted Raw-First Fairness Rereview: PASS

## Scope and Blind Visibility

This is a proposal-only rereview of the current reviewer-input projection. The
only inputs opened were:

1. `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`
2. `derived/manual_adjudication_v2/reviewer_projection_audit.json`
3. `discover_matrix/docs/protocol/semantic_judge_protocol.md`, lines 1-110

No canonical decision, raw artifact, unblind mapping, legacy label, prior
review, or other agent conclusion was opened. No provider was called. The
projection SHA-256 is
`sha256:fef163ee00b7dc48b401d7a37845e21f0a16abdd84150593a73a5c9ee73dc6e6`.

## Verdict

**PASS.** The current reviewer-input projection is a closed two-arm blind
projection under the protocol's allowlist. No producer identity, side mapping,
semantic-adjudication label, forbidden metadata key, source asymmetry, or
padding failure was found.

## Findings

| ID | Severity | Path | Reason | Basis | Commands |
| --- | --- | --- | --- | --- | --- |
| F-001 | INFO | `reviewer_input_projection.jsonl:1485,1503` (`report_evidence.claim_text`) | A conservative textual scan matched `invalid` in “synthetic invalid state” and “Targets Invalid State.” These are state-machine claim prose, not the protocol's `INVALID` adjudication label, and carry no validity/relation result. | All 31,704 textual leaf values were scanned; no K/N/I, relation, validity, expected-ledger, predicate, receipt, or other forbidden semantic-label occurrence was found. | `node` JSONL all-string allowlist/lexical scan below. |
| F-002 | INFO | all projection string fields | Producer-ID leakage is **not present**. There were zero matches for provider/model families, `v60`, `x1v2`, `baseline`, or repository/artifact path patterns. `arm-a`/`arm-b` are the protocol-permitted sealed tokens only. | The protocol's dual-side mapping permits sealed arm tokens and excludes producer-specific pointers and IDs. | `node` JSONL all-string allowlist/lexical scan below. |
| F-003 | INFO | all `pair_token`/`round`/`slot` groups | Closure, padding, and author-source symmetry hold: 2,642 rows form 1,321 complete groups, each with one `arm-a` and one `arm-b`; every paired slot has byte-identical NL and PlantUML text plus identical source hashes. | Recomputed source hashes match every row. The permitted audit manifest mirrors every projection row and records 859 correctly empty `slot-*` padding rows and 1,783 non-padding `report-*` rows. | `node` JSONL/audit structural, hash, closure, and padding scan below. |

## Checks Performed

- Parsed all 2,642 JSONL lines; each row has exactly the common projection
  allowlist and each nested object has exactly its permitted keys.
- Checked all textual fields and nested keys: 31,704 string leaves scanned.
  No forbidden key occurred, and no producer/side identifier or forbidden
  semantic metadata occurred.
- Validated opaque forms: every pair token is `pair-` plus 20 lowercase hex
  characters; every review key is `report-` or `slot-` plus 20 lowercase hex
  characters; every visible hash is `sha256:` plus 64 lowercase hex
  characters.
- Recomputed every visible NL and PlantUML SHA-256; all matched. Checked the
  whole-file SHA-256 against the audit manifest; it matched.
- Checked arm/slot closure and source/hash symmetry for every
  `(pair_token, round, slot)` group. No group was malformed or asymmetric.
- Used the permitted audit manifest only to classify padding, because the
  reviewer input deliberately represents padding as empty evidence with an
  opaque `slot-*` key. All 859 padding rows are empty; no non-padding row is
  empty.

## Commands

```bash
sed -n '1,110p' project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/semantic_judge_protocol.md
sha256sum project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/reviewer_input_projection.jsonl
node <inline JSONL/audit parser>
```

The inline parser read only the two permitted files. It parsed every JSONL
record; enforced the row and nested-key allowlists; scanned every string leaf
and key against the audit's forbidden-key set plus producer/side and
semantic-label patterns; recomputed author-source hashes; compared all
same-slot sources and hashes across arms; validated token shapes; and matched
each row to the permitted audit manifest for closure and padding checks.
