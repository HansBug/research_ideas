# v60/current source-first re-audit v4

This versioned layer is the canonical current-side re-audit for the fair
comparison with X1v2 baseline v3. It revalidates the existing pane5-confirmed
current decisions against the immutable raw records, author NL/PlantUML
sources, source hashes, and the complete 145-item relation closure. It does
not claim a new human inter-rater experiment and it does not infer labels from
completed manual-adjudication records, predicates, W level, or ledger absence.

The current v2 layer is retained and is the evidence source for the prior
source-first review chain. This v4 layer is new and is not a replacement for
raw, reference, method, manual-adjudication, predicate, v2, or baseline-v3 artifacts.

## Predicate facts

The v60 registry contains 19 predicates in four families: Structure (6),
Topology (4), Trajectory simulation (4), and Bounded verification (5). The
method summary records 12 distinct IDs with a terminal receipt; the canonical
v4 decisions record 8 distinct IDs bound to at least one report-bound finding.
These are distinct-ID metrics and are independent of W, D/A, K/N/I, hit counts,
and the report-level diagnostic ratios (`825/1271` and `303/825`). Detailed
expected-property/input capability audits remain in the separate internal
predicate-gold overlay.

## Canonical files

| File | Meaning |
| --- | --- |
| `inventory_v4.json` | Direct raw enumeration of 162 current method cells and 1271 reports, including five empty cells, pointers, and hashes. |
| `current_report_decisions_v4.json` | Pydantic-validated canonical current decisions; one row per report and 145 dense relations per row. |
| `current_report_decisions_v4.tsv` | Fixed-column mirror of the decision rows. |
| `current_relation_projection_v4.json` / `.tsv` | 1271 x 145 relation projection. |
| `current_n_groups_v4.json` / `.tsv` | 231 final-N reports assigned exactly once to 121 same-side, same-pair substantive groups. |
| `current_i_diagnostic_composition_v4.json` | D0/A0 and A0 subtype composition; I clusters are diagnostic only. |
| `current_i_diagnostic_clusters_v4.json` | Traceable 291-report to 189-cluster diagnostic membership; clusters are invalid-claim patterns, not defects or grouped-precision units. |
| `summary_v4.json` / `recomputed_summary_v4.json` | Provider-free current metrics and the identical recomputation copy. |
| `review_log_v4.json` and `reviews/` | Review-chain provenance, arbitration entries, deterministic integrity/fairness checks, and final-gate review. |
| `manifest_v4.json` | Input/output hashes, scope, superseded pointer, and execution boundary. |

## Closure

The canonical current result is `D2/D1/D0/A0 = 721/259/120/171` and
`K/N/I = 749/231/291` over 1271 reports. D0 and A0 always map to I. D2/D1
with a FULL or PARTIAL relation maps to K; D2/D1 with 145 NO_MATCH rows maps
to N. PARTIAL is known/supporting coverage but is not a main FULL hit.

All current report IDs retain a two-entry source-first review chain from v2:
`human:pane5-supervised-adjudicator` and
`subagent:raw-first-independent-proposal`. The five recorded disagreements
are explicitly arbitrated by pane5; no current class changed in v4.

## Recompute

From the repository root:

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_current_reaudit_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

The command is provider-free and performs no method run or new manual adjudication.

To rebuild only the I diagnostic membership projection, run
`scripts/evaluation/build_current_i_diagnostic_clusters_v4.py`; to refresh only
derived summary terminology without rewriting decisions, use
`build_current_reaudit_v4.py --refresh-summaries-only`.
