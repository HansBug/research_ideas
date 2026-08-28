# Paper STM Evaluation

This package owns provider-free evaluation, cross-arm comparison, witness
aggregation, costs, paired comparison, and final-results archive validation.
It may read completed method and Judge artifacts but is never imported by
either runtime package.

The canonical offline validator is:

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover:project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/judge/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline \
  --repository-root .
```

It neither calls a provider nor relies on the untracked `runs/` directory.
The explicit repository root keeps stable archive-relative review links valid
when the evaluator itself is installed outside the clean checkout.
