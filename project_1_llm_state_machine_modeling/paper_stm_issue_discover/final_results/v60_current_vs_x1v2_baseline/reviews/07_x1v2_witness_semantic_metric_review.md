# X1v2 Witness Semantic And Metric Review

> Historical review of the Judge-exposed v1 packet. Its isolation finding was
> accepted and corrected: `paper1.x1v2-witness-review-packet.v2` excludes all
> Judge paths, hashes, validity values, expected relations, and ledger IDs;
> fresh reviewers then completed two blind passes. The v1 materials are retained
> under `derived/superseded_judge_exposed_witness_review_v1/` and do not support
> the accepted W metrics. The v2 result receives a new independent semantic and
> metric review in `09_x1v2_witness_blind_semantic_metric_review.md`.

## Scope And Method

This was an independent, provider-free review of the frozen X1v2 material. No
provider, method, Judge, or pipeline code was invoked or modified. I read the
two final W0 source findings and the only W-level disagreement against their
hash-verified NL and PlantUML inputs, inspected the 162 original X1v2 method
records, and recomputed the requested joins directly from the 162 frozen
`PairJudgeResult` files.

The method-record scan found one uniform schema across all 162 records and
512 findings: every finding has only `issue`, `where`, and `reason`; no record
has an execution, receipt, executable-object, evaluated-artifact-hash, or
terminal-result field. All 512 raw `original_report_id` values join one-to-one
to the 512 final W labels in the [finding-level audit](../derived/x1v2_witness_level_audit.json).
For FULL-hit aggregation I used only each raw `expected_outcomes[].full_report_ids`;
`partial_report_ids` were not read for the max-W calculation. L2 membership
comes from the frozen [ledger](../reference/ledger.json).

## Semantic Witness Check

The two final W0 records are `0036:r1:...:baseline_issue_4` and
`0036:r3:...:baseline_issue_4`, from the
[round-1 source record](../raw/x1v2_baseline/method/run1/0036-luna/record.json) and
[round-3 source record](../raw/x1v2_baseline/method/run3/0036-luna/record.json) for
pair 0036. I verified the record and input hashes for both records and their shared
[NL](../reference/x1v2_input_closure/pairs/0036/nl.txt) and
[PlantUML](../reference/x1v2_input_closure/pairs/0036/plantuml.puml) closure.

- Round 1 says only "the overall state machine, especially termination/completion
  modelling" and names no completion carrier, endpoints, guard, action, or
  finite path. W0 is correct.
- Round 3 says only "the whole PlantUML model" and likewise does not bind the
  missing completion mechanism to a concrete model element or finite path. W0
  is correct.

The round-3 item is also the sole W-level disagreement: primary assigned W0
and secondary assigned W1 because it treated whole-model scope as a location.
I agree with the final W0 adjudication in the [adjudication record](../derived/x1v2_witness_adjudications.json): whole-model scope is not a checkable
state, transition, source/target pair, guard, action, or finite path. Both
items have empty executable-object, receipt, evaluated-artifact-hash, and
terminal-result fields.

There are no final W2 claims: `W2 = 0/512`. Consequently there is no W2 claim
missing any of the four required original-run items. More strongly, all
`512/512` final audit records have all four fields null, consistent with the
original method-record schema. The W2 admissibility gate is therefore
satisfied without exception.

## Recomputed Finding Counts

`K`, `N`, and `I` below mean `VALID_KNOWN`, `VALID_NOVEL`, and `INVALID` from
the frozen raw Judge report outcomes. They are reported as an orthogonal
cross-tab, not used to derive W.

| Round | W0 | W1 | W2 | K | N | I | Findings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 172 | 0 | 85 | 45 | 43 | 173 |
| 2 | 0 | 163 | 0 | 91 | 45 | 27 | 163 |
| 3 | 1 | 175 | 0 | 100 | 44 | 32 | 176 |
| Total | 2 | 510 | 0 | 276 | 134 | 102 | 512 |

The two W0s are both `VALID_NOVEL`; the validity-by-W totals are
`INVALID: 0/102/0`, `VALID_KNOWN: 0/276/0`, and
`VALID_NOVEL: 2/132/0` for W0/W1/W2 respectively.

## Recomputed FULL Metrics

The raw expected universe is `435`: `211` FULL, `33` PARTIAL, and `191` NONE.
The L2 universe is `117` expected rows (`39` ledger items across three rounds),
of which `46` are FULL. Every one of the 211 FULL rows has at least one
`full_report_id` and a resolved W label.

| Metric | W0 | W1 | W2 | Denominator |
| --- | ---: | ---: | ---: | ---: |
| Overall FULL-hit max W | 0 | 211 | 0 | 211 FULL rows |
| L2 FULL-hit max W | 0 | 46 | 0 | 46 L2 FULL rows |
| W2 / all expected | - | - | 0 | 435 expected rows |

By round, FULL rows are `64`, `73`, and `74`; every one has max W1. These
results match the [stored FULL-only aggregation](../derived/x1v2_full_hit_max_witness_audit.json), but were recomputed from raw outcome rows rather than copied from it.

## Finding: Judge Isolation Is Not Demonstrated

The audit cannot support the claim that Judge facts were not used to create W
labels. Every `512/512` work item in the purportedly label-free
[review batches](../derived/x1v2_witness_review_batches/) contains a
`judge_association`, including `validity`, full/partial ledger IDs, and a
Judge-result path and hash. The round-1 W0 work item and the round-3
disagreement work item both expose `VALID_NOVEL` and their hit linkage before
the review decision.

The primary and secondary decision prose says that Judge association was not
used, and the recorded W0 rationales rely on the raw finding and source
closure rather than citing Judge content. That is useful corroboration, but
it is not a technical blindness control: the facts were present in the
materials the reviewers were asked to read. I therefore cannot confirm the
requested non-use condition from this archive.

Required fix: rebuild a fresh 512-item W packet that omits all Judge paths,
hashes, validity values, expected relations, and ledger IDs; give it to new
independent reviewers with no access to the Judge artifact tree. Preserve a
hash of that blind packet, collect two fresh decisions and any adjudication,
then rerun the same `full_report_ids`-only aggregation.

## Conclusion

The original-X1v2 evidence gate, both final W0 semantic decisions, raw
finding/validity counts, and all requested FULL and W2 metrics are correct.
The reported W metrics are therefore arithmetically reproducible conditional
on the existing W labels. They are not yet certifiable as a Judge-independent
witness audit because Judge facts were exposed in every labeling work item.
