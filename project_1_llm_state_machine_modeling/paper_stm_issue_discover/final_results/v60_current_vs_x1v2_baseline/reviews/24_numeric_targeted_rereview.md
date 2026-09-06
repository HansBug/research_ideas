# Numeric Targeted Rereview (Proposal Only)

**Status: PASS**

This is an independent, provider-free numeric subagent proposal. It reads the
current canonical package and preserved calibration sources directly. It does
not modify `raw/`, canonical decisions, calibration files, manifests, or
reports, and it makes no provider call.

## Scope

- Canonical inputs: `derived/manual_adjudication_v2/v60_report_decisions.json`,
  `reference_ledger_aggregate.json`, `calibration_report.json`, and
  `pane5_targeted_re_review.json`.
- Frozen inputs: `reference/ledger.json`,
  `reviews/12_v60_valid_novel_posthoc_reaudit.json` (444 rows), and
  `reviews/11_v60_invalid_manual_reaudit.tsv` (106 rows).

## Independent Recompute

The read-only aggregation rebuilt the 550-reference universe and expanded each
row to the 145-item ledger. It uses the preserved row's explicit `relation` to
place `ledger_ids` in FULL or PARTIAL, and maps legacy empty `NA`, `-`, and
empty cells to `null` before comparing A0 types. This follows the documented
normalization and relation-aware parser in
[`audit_calibration.py`](../../../scripts/evaluation/audit_calibration.py#L28-L103),
but the rereview used a read-only process rather than that writer script.

| Reference aggregate | Independent | Stored |
|---|---:|---:|
| K_hit | 16/145 | 16/145 |
| N_group | 121/121 | 121/121 |
| I_group | 187/187 | 187/187 |
| partial-only known report | 5/550 | 5/550 |
| partial-only known expected | 2/145 | 2/145 |
| FULL round units | 20/435 | 20/435 |
| PARTIAL round units | 4/435 | 4/435 |

The 550 reference IDs are unique and all occur in the current canonical v60
decision set. The aggregate exactly equals
[`reference_ledger_aggregate.json`](../derived/manual_adjudication_v2/reference_ledger_aggregate.json).

| Calibration check | Independent | Stored |
|---|---:|---:|
| strict D/A plus A0 type | 546/550 (99.27%) | 546/550 (99.27%) |
| A0 type | 549/550 (99.82%) | 549/550 (99.82%) |
| corrected K/N/I | 550/550 (100.00%) | 550/550 (100.00%) |
| dense relation | 549/550 (99.82%) | 549/550 (99.82%) |
| mismatches | 5 | 5 |

The recomputed mismatch set is exactly
`0009:r1:issue:4`, `0009:r2:issue:10`, `0009:r3:issue:8`,
`0023:r1:issue:5`, and `0049:r2:issue:30`.

Every mismatch has an `ARBITRATED` row in
`pane5_targeted_re_review.json`, with nonempty reason, basis, and source
references; `human_confirmation=true`; `human_supervised_session=true`; and
final adjudicator `human:pane5-supervised-adjudicator`. Its corresponding
canonical decision is also `FINAL` with `human_confirmation=true`. The five
IDs equal the stored calibration mismatch set and are contained in the 15
targeted rereview rows. `all_mismatches_targeted=true` is independently
confirmed.

## Evidence Commands

```bash
jq '{aggregates, source_reports}' \
  final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/reference_ledger_aggregate.json

jq '{status, agreement, targeted_re_review_closure, mismatch_ids: [.mismatches[].report_id]}' \
  final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/calibration_report.json

jq '.rows[] | select(.report_id == "0009:r1:issue:4" or .report_id == "0009:r2:issue:10" or .report_id == "0009:r3:issue:8" or .report_id == "0023:r1:issue:5" or .report_id == "0049:r2:issue:30")' \
  final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/pane5_targeted_re_review.json
```

The independent aggregation was a read-only `venv/bin/python -` process. It
parsed the preserved sources with the relation-aware rule above, expanded dense
relation maps, compared them to canonical decisions, and checked every
mismatch against targeted-rereview and final-review fields. No writer,
generator, evaluator, method runner, Judge runner, or provider was invoked.

## Findings And Disposition

No C, I, or M finding in this targeted scope.

**Disposition:** accepted. The prior relation-aware aggregate and calibration
closure findings are resolved in the current canonical package.

**Targeted rereview conclusion:** PASS. Provider calls: **0**. Frozen raw
changes: **0**. Canonical-data changes by this review: **0**.
