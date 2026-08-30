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
| `group_id` | N group only | nullable for K/I |

All metrics use `Metric`-style numerator/denominator/percentage objects. Hit
and supported coverage use expected-round units (`145 x 3 = 435`) or unique
expected IDs as stated beside each field. W-on-hits uses FULL expected-round
hits as its denominator. Predicate usage is report-bound receipt usage;
baseline is `not_applicable`, not zero.

The main precision is report-level `(K+N)/all reports`. The diagnostic
composition records unique K expected IDs, substantive N groups, and invalid I
clusters separately. I has no substantive-group precision denominator.
