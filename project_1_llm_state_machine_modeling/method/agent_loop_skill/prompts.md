# SL prompt generators

PR-0 约定：`SL-*` 只暴露 prompt generator / stage spec / schema，不绑定内部 LLM wrapper。后续 PR-1B 的内部 agents 也应复用同一 prompt generator，避免 prompt drift。

最小 generator 名预留：

- `build_sl1_initial_modeling_prompt(nl, spec_json, pyfcstm_grammar_digest, ...)`
- `build_sl5_scenario_generation_prompt(nl, current_dsl, inspect_summary, grounding_map, ...)`
- `build_sl7_model_review_prompt(nl, current_dsl, inspect_summary, sim_summary, grounding_map, ...)`
- `build_sl9_repair_prompt(nl, current_dsl, fix_plan_or_revised, selected_diagnostics, grammar_digest, preserve_list, ...)`
- `build_sl10b_delta_review_prompt(nl, grounding_map, old_dsl, candidate_dsl, fix_plan, diff_summary, ...)`

## LLM stage trace 要求

每次真实调用必须保存 `ReviewRunMeta` 或等价 LLM interaction 记录：provider、model、resolved model、prompt template version、prompt hash、input hash、temperature、seed、retry、raw output hash/path、schema validation、cache key、decision threshold、failure policy、replay key。
