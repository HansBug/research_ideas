# SL prompt generators

PR-0 约定：`SL-*` 只暴露 prompt generator / stage spec / schema，不绑定内部 LLM wrapper。后续 PR-1B 的内部 agents 也应复用同一 prompt generator，避免 prompt drift。

最小 generator 名预留：

- `build_sl1_initial_modeling_prompt(...)`
- `build_sl5_scenario_generation_prompt(...)`
- `build_sl7_model_review_prompt(...)`
- `build_sl9_repair_prompt(...)`
- `build_sl10b_delta_review_prompt(...)`
