# Numeric Post-Fix Review (Proposal Only)

**Status: FAIL**

This is an independent provider-free subagent proposal, not a human
adjudication and not a replacement for canonical decisions. It reads frozen
raw artifacts, the ledger, canonical `manual_adjudication_v2` files, and the
two preserved calibration sources directly. It does not use earlier numeric
reviews as evidence, call a provider, or modify `raw/` or canonical decisions.

## Scope And Method

- Frozen archive: `raw/v60_current/`, `raw/x1v2_baseline/`,
  `reference/ledger.json`, and `derived/x1v2_witness_level_audit.json`.
- Canonical audit: `derived/manual_adjudication_v2/` decision JSON/TSV,
  relation, group, hit-witness, predicate-witness, reference-aggregate,
  summary, calibration, and manifest files.
- Calibration sources: `reviews/12_v60_valid_novel_posthoc_reaudit.json`
  (444 rows) and `reviews/11_v60_invalid_manual_reaudit.tsv` (106 rows).

The independent aggregation read each of the 303 raw method-record files once,
then used the frozen pointer/hash inventory and the final decision records. It
uses no text similarity or semantic inference.

## Passing Checks

| Check | Independent result |
|---|---:|
| Raw inventory | 162 + 162 cells; 1271 + 512 reports; all 1,783 raw hashes and pointers closed |
| Decision closure | 1271/1271 v60 and 512/512 X1v2 IDs exactly match inventory |
| Dense relations | 258535/258535 rows, exactly equal to the nested decision projection |
| JSON/TSV mirrors | exact for both sides |
| D/A -> validity -> K/N/I | all 1,783 rows closed; no invalid positive relation |
| N/I groups | 543 groups, covering exactly 755 N/I reports; no cross-side or cross-pair member |
| Hit witnesses | 870 side/expected/round rows, all supporting IDs and max-W values exact |
| Predicate audit | 19/19 frozen predicates; 825 binding usages = W0/W1/W2 0/303/522; 522 terminal receipts; baseline is `not_applicable` |
| Canonical manifest | 77/77 files hash-closed; `FINAL`, 1271/512 report counts, no manifest blocker |

Independent publication totals agree with `summary.json` and the current main
results table. The comparison ignores only the explanatory `unit` string in
`ledger_based`; all numeric fields are identical.

| Metric | v60/current | X1v2 baseline |
|---|---:|---:|
| D2/D1/D0/A0 | 721/259/120/171 | 408/3/2/99 |
| K/N/I | 749/231/291 | 279/132/101 |
| hit@1, FULL | 310/435 (71.26%) | 212/435 (48.74%) |
| L2 hit@1, FULL | 105/117 (89.74%) | 46/117 (39.32%) |
| hit@3 / hit@all | 119/145 (82.07%) / 86/145 (59.31%) | 104/145 (71.72%) / 38/145 (26.21%) |
| report precision / FP rate | 980/1271 (77.10%) / 291/1271 (22.90%) | 411/512 (80.27%) / 101/512 (19.73%) |
| K_hit / N_group / I_group | 119 / 121 / 189; denominator 429 | 104 / 132 / 101; denominator 337 |
| ledger precision / FP rate | 119/429 (27.74%) / 189/429 (44.06%) | 104/337 (30.86%) / 101/337 (29.97%) |
| partial-only report / expected | 110/1271, 21/145 | 45/512, 24/145 |
| FULL-hit max W2/W1/W0 | 197/113/0 of 310 | 0/212/0 of 212 |
| W2/all expected | 197/435 (45.29%) | 0/435 (0.00%) |

The main-result values above also occur in
`report/v60_current_vs_x1v2_baseline_cn.md:21-40` and `:68-74`.

## Findings

### 21-NUM-I-001 - Calibration report is stale relative to final decisions

**Severity: I.**

`calibration_report.json` reports strict D/A+A0 agreement as 546/550, A0-type
agreement as 549/550, and five mismatches. Recomputing from the current final
v60 decisions and the 444+106 preserved reference rows yields 516/550
(93.82%), 519/550 (94.36%), and 34 mismatches: 33 D/A-only and one D/A plus
relation mismatch. K/N/I remains 550/550 and dense relation remains 549/550.

The result still clears the numeric 90% D/A and relation thresholds and the
5pp distribution threshold, but it is not the recorded calibration result;
the stored mismatch list cannot support the claimed review closure.

**Evidence and basis:**

- Stored agreement and mismatch metadata:
  `derived/manual_adjudication_v2/calibration_report.json:3-18,1845-1859`.
- The calibration reader correctly treats a frozen-N row's `relation` field
  as controlling whether its ledger IDs are FULL or PARTIAL:
  `scripts/evaluation/audit_calibration.py:60-72`.
- Its comparison is against current canonical decisions:
  `scripts/evaluation/audit_calibration.py:120-158`.
- The independent relation-aware recomputation used those same two preserved
  sources and all 550 canonical report IDs.

**Reproduction:** run the provider-free aggregation embedded in this review's
scope, or reproduce the same comparison by reading the code at
`scripts/evaluation/audit_calibration.py:56-158` without allowing it to write
its output. It produces `strict_da_and_a0_type=516/550`,
`a0_type=519/550`, `corrected_kni=550/550`, `dense_relation=549/550`, and 34
mismatches from the current files.

**Disposition:** open. Regenerate `calibration_report.json` from the current
canonical decisions, retain all 34 mismatch rows, and perform/record targeted
rereview for every retained mismatch before declaring the calibration gate
ready. Re-run this numeric review after that change.

**Repair commit:** not applicable; proposal-only review did not modify data.

**Targeted rereview:** FAIL pending the regenerated record and closure.

### 21-NUM-I-002 - Reference aggregate discards preserved relation type

**Severity: I.**

`reference_ledger_aggregate.json` treats every list-valued `ledger_ids` field
from the frozen-N reference as FULL. That conflicts with the reference row's
own `relation` field. The code path at
`scripts/evaluation/generate_manual_adjudication.py:643-645` calls
`parse_ledger_ids()` without passing or inspecting `row["relation"]`, while
the calibration reader preserves that distinction at
`scripts/evaluation/audit_calibration.py:60-69`.

The affected stored aggregates are `partial_only_known_report=1/550` and
`partial_round_units=2/435`; the relation-aware recomputation is respectively
`5/550` and `4/435`. `K_hit=16/145`, `N_group=121`, `I_group=187`,
`full_round_units=20/435`, and `partial_only_known_expected=2/145` remain the
same. Therefore the required same-unit calibration aggregate is not currently
derived under one relation definition.

**Evidence and basis:**

- Stored aggregate: `derived/manual_adjudication_v2/reference_ledger_aggregate.json:1`.
- Legacy partial example: `reviews/12_v60_valid_novel_posthoc_reaudit.json`
  contains `0045:r1:issue:2` with `relation=PARTIAL_MATCH` and
  `ledger_ids=["EIS-0045-01"]`; its final canonical relation is also PARTIAL.
- The incompatible aggregation and relation-aware parsing code are cited
  above.

**Reproduction:** provider-free parse of the 444 JSON rows and 106 TSV rows:
expand FULL/PARTIAL from the preserved relation field, then calculate units by
`(pair_id, round, expected_id)` and groups by `(pair_id, group_key)`.

**Disposition:** open. Make the reference aggregate use the same
relation-aware parser as the calibration calculation, regenerate the aggregate,
calibration, manifest, and rendered report, then targeted-rereview the
calibration figures.

**Repair commit:** not applicable; proposal-only review did not modify data.

**Targeted rereview:** FAIL pending a relation-aware reaggregation.

### 21-NUM-I-003 - Report calibration paragraph disagrees with both stored and recomputed evidence

**Severity: I.**

The current report says 547/550 strict D/A agreement, 549/550 dense relation
agreement, four mismatches, and that all mismatches have targeted rereads
([`report/v60_current_vs_x1v2_baseline_cn.md`](../report/v60_current_vs_x1v2_baseline_cn.md#L100)).
The stored calibration file instead says 546/550 and five mismatches, with
`all_mismatches_targeted=false`; the relation-aware recomputation finds
516/550 and 34 mismatches. The report therefore has no matching structured
evidence for this claim.

**Evidence and basis:**

- Report claim: `report/v60_current_vs_x1v2_baseline_cn.md:100`.
- Stored status and failed targeted-closure flag:
  `derived/manual_adjudication_v2/calibration_report.json:1845-1859`.
- Report renderer unconditionally writes "均有 targeted reread" rather than
  testing the closure flag: `scripts/evaluation/render_manual_report.py:167`.

**Disposition:** open. Do not publish a calibration pass statement until
findings `21-NUM-I-001` and `21-NUM-I-002` are fixed and the report is rendered
from the corrected structured files with a real targeted-closure condition.

**Repair commit:** not applicable; proposal-only review did not modify data.

**Targeted rereview:** FAIL pending corrected calibration artifacts and report.

## Gate Conclusion

No C finding was found. The raw closure, two-side publication metrics, W
projection, predicate usage, group boundary, canonical manifest, and main
result table pass independent provider-free recomputation. The calibration
audit and the report's calibration statement have three unresolved I findings.
Accordingly this review is **FAIL** and cannot sign the finalization gate.

Provider calls: **0**. Frozen raw changes by this review: **0**. Canonical
decision changes by this review: **0**.
