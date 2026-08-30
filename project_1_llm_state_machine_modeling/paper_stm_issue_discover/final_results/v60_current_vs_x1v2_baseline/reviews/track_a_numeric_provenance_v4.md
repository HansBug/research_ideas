# Track A: numeric and provenance review

**Reviewer:** `01a05261-bfcb-7c60-b697-b146093725a3`
**Mode:** independent, read-only subagent review; no provider, method, or Judge run

## Commands

From the repository root:

`PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_current_reaudit_v4.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only`

`PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_baseline_v3.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline`

`PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_fair_comparison_v4.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --validate-only`

## Final results

| Check | Result | Evidence |
| --- | --- | --- |
| Current v4 | PASS | `1271` reports, `162` cells, `184295` dense relations, `231` N, `291` I, `121` N groups |
| Baseline v3 | PASS | `512` reports, `162` cells, `233` reviewed non-K, `279` frozen K, `98` N groups, `95` I clusters |
| Fair recomputation | PASS | `1783` combined reports and `145` expected IDs |
| Summary mirrors | PASS | current `summary_v4.json` and `recomputed_summary_v4.json`, baseline v3 summaries, and fair summaries compare equal |
| Dense relation closure | PASS | current `685 FULL + 279 PARTIAL + 183331 NO = 184295`; baseline `288 FULL + 124 PARTIAL + 73828 NO = 74240` |
| Headline values | PASS | Current `K/N/I=749/231/291`, `D2/D1/D0/A0=721/259/120/171`, precision `980/1271`; baseline `312/105/95`, `342/75/85/10`, precision `417/512` |
| Publication provenance | PASS after fix | Historical-report relative links repaired; top-level manifests regenerated from the explicit publication allowlist |

## Reconciliation

The initial review found only publication-layer failures: stale top-level
manifest hashes, the pre-finalization broad publication list, and a broken
relative link introduced by moving the historical report. These were closed
without changing canonical data. The raw/source/hash identity and all metric
numerators and denominators remain unchanged.

## HEAD-specific independent rerun and closure (2026-08-31)

Reviewer `track-a:numeric-provenance-independent-v4` independently checked the
current v4, baseline v3 and fair v4 JSON/TSV/manifests. The canonical metrics
passed, but the reviewer recorded two publication FAILs at input commit
`848d9832dad6f0267e3848b5f0f3c33121a89915`: the report omitted the fixed
report-bound `825/1271` and `303/825` rows, and three manifests still carried
the pre-edit report hash `a7ada7...4970ca`.

Pane5 preserved both report-bound values and named their units explicitly. The
fair/current summaries now expose `report_bound_binding=825/1271` and
`legacy_semantic_hit_marker_among_report_bound_bindings=303/825`, while method
execution remains a separate `12/15` predicates and `1237` terminal receipts.
This resolves the review disagreement without changing a decision or treating
303 as a terminal-false count. The baseline historical input `132` is now
labeled as source-layer context rather than a second headline.

Final provider-free checks passed with current `1271`, baseline `512`, combined
`1783`, expected `145`, current precision `980/1271`, baseline precision
`417/512`, and byte-valid publication/fair/archive manifests. No provider,
method or Judge run was used.
