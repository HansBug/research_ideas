# v3 schema map

Canonical production models live in
`evaluation/src/paper_stm_evaluation/manual_adjudication_v3_baseline_ni.py`.
Every model has a class docstring and every field uses `Field(description=...)`.

`DecisionSetV3` contains exactly 233 `BaselineReportDecisionV3` objects. A
decision stores the immutable raw finding pointer/hash and original text,
author-source fact and D/A status, validity and mechanically closed K/N/I,
145 `RelationDecision` rows, independent W evidence, source loci, dedicated
reason/basis, and `ReviewChain`. `ReviewChain` requires two distinct blind
subagent proposals plus the authorized pane5 human confirmation; proposal
identities are never reused from v2.

`GroupSetV3` contains `NGroupV3` substantive groups and `InvalidClusterV3`
diagnostic clusters. `NGroupV3` stores `member_source_refs` for every member
and `non_merge_reasons` for every pair-local conservative singleton decision.
The model and provider-free validator enforce duplicate-free membership,
member-to-group map equality, member pair/side and round closure, and exact
source-ref equality against canonical decisions. Each final N or I appears
exactly once; I clusters are not counted as substantive defects.

`NonMergeReasonV3` is not a semantic classifier. It records the neighboring
report, the homogeneity criteria that were not established, the dedicated
reason/basis, and the raw/source refs used for the conservative decision.
A singleton therefore does not claim that its report is a distinct defect.

`RelationAuditRowV3` is the flat relation projection. `Metric` carries
numerator, denominator, percentage, unit, and reason; a non-applicable metric
uses `percentage: null` and an explicit reason rather than zero.

The versioned manifests are `archive_manifest_v3_baseline_ni.json` and
`publication_manifest_v3_baseline_ni.json`. They hash every formal v3 output,
record v3 review outputs, preserve the superseded v2 pointer, and
list retained but excluded proposal files. An excluded proposal is not a
canonical input even when it remains physically present for audit history.
The top-level `archive_manifest.json` and `publication_manifest.json` are
generated separately by `paper_stm_evaluation.final_results_archive` after
all review outputs are stable and bind the complete publication archive.

Relation closure is a model validator, not a semantic classifier: D0/A0 imply
all `NO_MATCH`; D2/D1 with a positive relation imply K; D2/D1 with no positive
relation imply N. W and predicate fields are independent and cannot enter this
closure.
