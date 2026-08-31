# v60/current versus X1v2 baseline v3 fair comparison

This is the paper-facing comparison layer. The only headline sides are
`v60_current` from current re-audit v4 and `x1v2_baseline` from the frozen
baseline v3 layer. Historical v2/v46/v27/Judge outputs remain byte-preserved,
but current navigation and manifests expose them only as archive/provenance,
not as headline results.

## Paper-facing predicate summary

The frozen v60 registry contains 19 predicates in four families: Structure (6),
Topology (4), Trajectory simulation (4), and Bounded verification (5). The v60
method summary records 12 distinct predicate IDs with at least one terminal
receipt. The current v4 canonical decisions record 8 distinct predicate IDs
bound to at least one report-bound finding. Both are distinct-ID metrics over the
19-ID registry; neither is a finding count, W2 count, hit count, or
issue-level coverage claim. X1v2 has no corresponding predicate
binding/receipt schema, so its predicate usage is `N/A`, not zero.

The summary also retains `825/1271` report-bound binding rows and `303/825`
legacy `coverage_class=semantic_hit` markers as row-level diagnostics. These are
not substitutes for 12/19 or 8/19. The detailed per-entry property/input and
predicate-capability audit remain internal evaluation-only material.

## Canonical outputs

| File | Purpose |
| --- | --- |
| `combined_report_index_v4.json` / `.tsv` | 1271 current + 512 baseline report index with raw pointers, hashes, class, D/A, relation projections, and group IDs. |
| `combined_summary_v4.json` / `recomputed_summary_v4.json` | Same provider-free metric result; numerator and denominator are explicit in every ratio. |
| `migration_index_v4.json` | Current v4 zero-change index plus all 233 baseline-v3 non-K migrations. |
| `provenance_v4.json` | Input hashes and superseded/source-layer boundaries. |
| `reviews/` | Independent numeric, artifact, fairness, academic, and final-gate review records. |
| `fair_comparison_manifest_v4.json` | Output and review hashes plus execution boundary. |

The full narrative is [the v4 paper report](../../report/v60_current_vs_x1v2_baseline_v4_cn.md).

## Publication rule

Report precision is the primary precision: `(K reports + N reports) / all
reports`. FULL hit is deduplicated at expected-ID and round level; PARTIAL is
supported coverage only. K expected IDs and N substantive groups are separate
issue views. I is invalid and has no substantive-group metric; I clusters are
diagnostic only. Current has a side-specific `NOT_A_DEFECT_CLAIM` subtype;
baseline does not manufacture that subtype.

The report index gives every N report its substantive group ID and every I
report its diagnostic cluster ID. Current I membership is reconstructed in
`../manual_adjudication_v4_current_reaudit/current_i_diagnostic_clusters_v4.json`;
those IDs remain excluded from substantive grouped precision.

Run the comparison from the repository root:

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_fair_comparison_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

This command is provider-free and performs no method or Judge run.
