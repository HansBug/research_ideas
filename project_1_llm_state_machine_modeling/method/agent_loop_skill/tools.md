# SD deterministic tools

PR-0 约定：`SD-*` 是确定性工具层，不调用 LLM、不读取 `.env`。后续 PR-1A 实现 façade 时必须复用 canonical feedback wrappers，不能形成第二套 parse/semantic/sim/design 实现。

最小工具名预留：

- `run_sd2_parse(...)`
- `run_sd3_semantic(...)`
- `run_sd4_design(...)`
- `run_sd5a_scenario_coverage(...)`
- `run_sd6_sim(...)`
- `run_sd8_fix_plan(...)`
- `run_sd10_repair_review(...)`
