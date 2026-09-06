# X1v2 Witness-Audit Data-Integrity Review

> Historical review of the Judge-exposed v1 packet. The semantic review in
> [07_x1v2_witness_semantic_metric_review.md](07_x1v2_witness_semantic_metric_review.md)
> correctly found that v1 could not certify Judge independence. v1 is retained
> under `derived/superseded_judge_exposed_witness_review_v1/` and is not the
> accepted witness audit. The accepted v2 blind-review data receive a new
> independent integrity review in `08_x1v2_witness_blind_data_integrity_review.md`.

## Scope

Independent, provider-free data-integrity review of the X1v2 witness-audit
artifacts only. This review did not participate in labeling and did not use
the narrative report totals as evidence. It read the frozen raw records,
input closure, composite-selected Judge results, review packet, decision
streams, final audit, aggregation, and adjudication log. No raw artifact,
code, or derived data file was modified.

## Method

1. Enumerated `raw/x1v2_baseline/method/run*/**/record.json` directly and
   expanded every `parsed_output.issues[]` entry into the canonical key
   `(pair_id, round, original_report_id)` and audit key.
2. Resolved each final work item's RFC 6901 JSON pointer against its raw
   `record.json`; checked the pointed finding and its `issue`, `where`, and
   `reason` text hashes. Recomputed SHA-256 for each referenced method record,
   NL input, PlantUML input, and composite-selected Judge pair result.
3. Checked every raw-baseline entry in the [side manifest](../raw/x1v2_baseline/archive_manifest.json)
   and every item in the [input-closure manifest](../reference/x1v2_input_closure/manifest.json)
   against its on-disk byte count and SHA-256.
4. Compared the raw-finding key set with the [review packet](../derived/x1v2_witness_review_packet.json),
   all [review batches](../derived/x1v2_witness_review_batches/), both decision
   streams ([primary](../derived/x1v2_witness_review_decisions/primary/) and
   [secondary](../derived/x1v2_witness_review_decisions/secondary/)), and the
   [final witness audit](../derived/x1v2_witness_level_audit.json). For every
   key, compared the embedded final reviews byte-for-structure with their
   corresponding decision records and required nonempty, distinct reviewer IDs.
5. Reconstructed the expected-row universe from the 162 composite-selected
   frozen Judge pair results named by [the composite receipt list](../raw/x1v2_baseline/judge/composite-summary.json).
   `FULL`, `PARTIAL`, and `NONE` were derived from each raw expected outcome's
   `hit` and `supported` fields. For each raw `FULL` row, recomputed max-W from
   only `full_report_ids`, then compared the result and each supporting report
   with the [FULL-hit aggregation](../derived/x1v2_full_hit_max_witness_audit.json).
6. Derived W-level disagreements directly from the two decision streams and
   compared that key set and final level with the [adjudication log](../derived/x1v2_witness_adjudications.json).

## Exact Results

| Check | Independently derived result | Integrity result |
| --- | ---: | --- |
| Raw baseline method records | 162 = 54 pairs x 3 rounds | Pass |
| Raw parsed findings | 512 | Pass |
| Raw-baseline manifest entries byte/hash checked | 842 / 842 | Pass; 0 mismatches |
| Input-closure files byte/hash checked | 108 files for 54 pairs | Pass; 0 mismatches |
| Finding JSON pointers, raw record hashes, finding-text hashes, and NL/PlantUML hashes | 512 / 512 | Pass; 0 mismatches |
| Final audit records | 512, exactly one per raw finding | Pass; no missing, extra, or duplicate keys |
| Review packet and mutually exclusive batch work items | 512 / 512 | Pass; exact raw-finding key set and work-item equality |
| Primary decisions | 512 / 512 | Pass; exact key set and final-record equality |
| Secondary decisions | 512 / 512 | Pass; exact key set and final-record equality |
| Distinct primary/secondary reviewer IDs | 512 / 512 findings | Pass |
| Final W distribution | W0/W1/W2 = 2/510/0 | Pass; direct count equals audit fields |
| Composite-selected raw Judge receipts | 162 / 162 raw method cells | Pass; all selected-result hashes match |
| Expected rows reconstructed from raw Judge results | 435 | Pass; exact aggregation-row key set |
| FULL rows reconstructed from raw Judge results | 211 | Pass; `max-W` = W0/W1/W2: 0/211/0 |
| W-level disagreements derived from reviews | 1 | Pass; one log entry and matching final adjudication |

The sole disagreement is
`0036:r3:0036:r3:baseline_issue_4`. Its primary decision is W0, secondary
decision is W1, and the adjudication log records the same key with final W0
and adjudicator `pane5-main`. No undisclosed disagreement, orphaned
adjudication, or final-label mismatch was found.

## Findings And Fixes

No data-integrity defect was found. No repository fix was warranted or
applied. A local verifier comparison was normalized to retain the zero-count
`W2` category when comparing W distributions; this was an audit-script
presentation issue only and did not alter or invalidate any archived artifact.

## Conclusion

PASS. The X1v2 witness-audit data are complete and internally consistent for
the requested integrity properties: all 512 raw findings have exactly one
final audit record, two distinct-reviewer decisions, correct raw linkage and
hash-verified inputs; the raw Judge evidence reconstructs 435 expected rows
and 211 FULL rows; and the single review disagreement is represented and
resolved in the adjudication log.
