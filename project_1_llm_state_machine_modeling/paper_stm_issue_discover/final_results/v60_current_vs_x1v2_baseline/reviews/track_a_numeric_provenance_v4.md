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
