# Fair comparison v4 schema

`recompute_fair_comparison_v4.py` uses Pydantic `Metric` and
`ReportIndexRow` models. Every field has a description and the models reject
unknown fields. The side canonical decisions remain in the current-v4 and
baseline-v3 directories; this layer contains compact references and derived
metrics, not a second semantic label source.

| Field | Meaning | Unit/nullability |
| --- | --- | --- |
| `side`, `pair_id`, `round`, `report_id`, `finding_index` | Stable report identity | strings/round/index; required |
| `canonical_class`, `validity`, `d_tier`, `witness_level` | Side canonical projections | required enums |
| `source_layer`, `canonical_path` | Versioned source of the row | required repository-relative paths |
| `raw_method_path`, `raw_json_pointer`, `raw_sha256` | Immutable raw evidence address | required path/pointer/hash |
| `full_ledger_ids`, `partial_ledger_ids` | Positive relation projections | required arrays, possibly empty |
| `group_id` | N substantive group or I diagnostic cluster; current and baseline I IDs are traceable but diagnostic only and never a defect/group-precision unit | nullable only for K |

All metrics use `Metric`-style numerator/denominator/percentage objects. Hit
and supported coverage use expected-round units (`145 x 3 = 435`) or unique
expected IDs as stated beside each field. W-on-hits uses FULL expected-round
hits as its denominator. The current predicate block contains four separate
units: registry size/family counts; distinct predicate IDs with a terminal
receipt (12/19); distinct predicate IDs in report-bound findings (8/19); and
row-level diagnostics (`report_bound_binding` 825/1271 plus the legacy
legacy coverage marker 303/825). The distinct-ID metrics are sourced from the
frozen method summary and current v4 canonical decisions; the row-level
diagnostics are not substitutes for them. None is a finding, W2, hit, or
issue-level coverage metric. The marker is not equated with a
terminal-false receipt. Baseline is `not_applicable`, not zero.

The current `predicate` object uses these names:

| Field | Meaning |
| --- | --- |
| `registry_predicate_count`, `registry_version`, `family_counts` | Frozen registry identity and four-family composition |
| `distinct_terminal_receipt_predicates` | `predicate_ids` and a `Metric` ratio; v60 is 12/19 |
| `distinct_report_bound_predicates` | `predicate_ids` and a `Metric` ratio; v60 is 8/19 |
| `report_bound_binding`, `legacy_semantic_hit_marker_among_report_bound_bindings` | Row-level diagnostic ratios; v60 is 825/1271 and 303/825 |
| `sources`, `naming_boundary`, `report_level_naming_boundary` | Evidence paths and explicit non-equivalence boundaries |

For X1v2, `predicate` remains an explicit `not_applicable` object because the
baseline contract has no current-side binding or receipt schema.

The main precision is report-level `(K+N)/all reports`. The diagnostic
composition records unique K expected IDs, substantive N groups, and invalid I
clusters separately. I has no substantive-group precision denominator.
