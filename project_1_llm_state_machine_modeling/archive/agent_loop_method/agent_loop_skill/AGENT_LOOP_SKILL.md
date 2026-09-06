# Agent Loop Skill（PR-0 Contract）

> 入口说明：本目录中的 `SKILL.md` 与 `CLAUDE.md` 是指向本文件的软链接。若某个 agent / CLI 环境不能正确跟随 symlink，应直接读取 `AGENT_LOOP_SKILL.md`，三者在语义上等价；PR comment 中需要如实记录实际读取的是哪个入口。

本目录是 project_1 agent-loop 的 repo-local skill 入口。PR-0 冻结 contract / docs / fixtures / run-record schema，不绑定具体 LLM provider。


## LG-M1-F provenance legend（2026-06-08）

- `PR-0`、`PR-1A`、`PR-B2`、`PR-C`、`PR-E1`、`PR-E2`、`PR-skill-fix` 等是 historical provenance，用于说明 skill contract、stage adapter、repair chain 与 ref-model 质量门的来源；它们不是当前功能模块命名规范。
- 当前程序化工具入口优先级是：`archive.agent_loop_method.stages.api` / `archive.agent_loop_method.stages.sc_control` / `archive.agent_loop_method.stages.sl_prompt_api`；这些入口不读 `.env`、不调 provider、也不得调用 `archive.agent_loop_method.loop.run_agent_loop(...)`。
- `archive.agent_loop_method.loop.run_agent_loop(...)` 是 Path1/Path2 默认完整 runtime，不是 skill 侧一键 ref-model producer。
- `LG-*` / `PR-*` marker 若已进入 run record、schema、historical evidence 或旧 PR reproduction path，应作为 provenance 保留；不得在 docs sweep 中机械删除。


## PR-M3 codex exec 标准实验入口

PR-M3 将 `codex exec` / mature coding agent 的 skill 使用方式提升为可复跑、可审计的标准实验入口。它不复现 E1 的 hidden/internal reasoning，也不得调用 `archive.agent_loop_method.loop.run_agent_loop(...)`；它保存的是 `codex exec --json` 外部事件流、实际读取文件、工具/检查/修复 ledger、NFRR 和人类友好 `report.md`。

- 详细配置、artifact schema、redaction、forbidden-call、四例运行纪律见 [codex_exec_experiment_guide.md](./codex_exec_experiment_guide.md)。
- 非敏感默认配置固定为 `CODEX_EXEC_DEFAULT_CONFIG=model_provider=airouter`，正式实验必须从 `.env`/环境解析并展开为 `codex exec -c model_provider=airouter` 或覆盖后的脱敏配置。
- 每个 run 必须生成 `run_manifest.json`、`codex_events.jsonl`、`actual_file_reads.json`、`tool_stage_check_ledger.json`、`repair_ledger.json`、`nfrr_report.json`、`forbidden_call_check.json`、`redaction_report.json`、`report.md` 与 `run_summary.md`；`report.md` 必须能让 reviewer 快速理解全过程，而不是只贴 final FCSTM。
- PR-M3 实现阶段四例为 ABS / CARA / Elevator / LNG；产物可暂时提交到 `runs/codex_exec_skill/...` 供 reviewer 审计，后续是否清理等待用户指示。

## PR-E2 e2e ref-model 使用入口

PR-E2 需要测试的是 Codex / Claude Code 能否拿到本 repo-local skill 后，自主完成 `NL + 完整论文子路径 -> FCSTM/pyfcstm ref model 候选` 的建模、检查、修复与留痕。

- 详细流程见 [e2e_ref_model_guide.md](./e2e_ref_model_guide.md)。
- 模型质量评价与准出标准见 [nfrr_evaluation_guide.md](./nfrr_evaluation_guide.md)；PR-E2 产物必须给出 NFRR claim/vector/tier/cap/allowed_use，并且必须包含可审计的 NL span ledger、obligation ledger、scenario provenance ledger 与 waiver ledger。
- PR-E2 实测 **不得** 调用 `archive.agent_loop_method.loop.run_agent_loop(...)`、PR-D representative runner 或任何一键 full staged runner。
- 允许长时间运行，时间限制只用于防止 CLI 死锁或失控；质量、grounding、验证和 PR comment 证据优先。
- 所有样本产物必须能写成 PR comment：输入 NL、论文路径、读取材料、候选模型、检查反馈、repair 轨迹、NFRR 评价、最终判断和 skill 改进建议。
- 单个 sample 最低准出：`final_tier >= T2`、`SD-2/SD-3` pass、无 unwaived `SD-4` blocking、至少一个可计入主 BVS 的 obligation-anchored `SD-6` scenario pass、无 critical contradiction / reachable test-harness pollution。可计入主 BVS 的 scenario 只能是 `default_prefix`、有可复核前缀的 `reachable_prefix`，或带 external-input ledger 的 `external_input_initial_vars`；`diagnostic_hot_start` / `model_derived_oracle` 只能 debug，不能作为最低准出或 BVS 主证据。
- Ground-Truth 级 ref-model candidate 目标准出：`final_tier >= T3`、`evidence_mode in {NL+paper, authoritative_NL}`、`obligation_independence in {independent_adjudicated, model_blind_independent}`、`FE=3`、`REC=3`、`BVS=3`，且 NFRR scenario ledger 必须证明 critical scenario obligations 不是主要依赖 hot-start；未人工/专家签核前仍必须标 `signed_reference=false`。


### PR-E2 语法与工具版本注意

当前 skill 使用者必须以实际 `SD-2` parser 为准，而不是只相信历史 grammar 摘要：已知当前 parser 支持 `def int` / `def float`，不支持 `def bool`、`true`、`false`；外部输入注释 `// @external` 不会被默认 `SD-4` 自动消费。详细见 [e2e_ref_model_guide.md](./e2e_ref_model_guide.md)。

### PR-skill-fix / PR-E1 设计变更残留审计

PR-skill-fix 后续使用本 skill 时，必须确认 PR-E1 大改后的设计口径已经在 skill 侧生效：

- repair 主链是 `SD-8 FixRequestBatch -> SL-9 per-request accept/reject + repair -> SL-10(NL + FixLog + local evidence) -> SC-11 -> SD-2`。
- `FixLog` / repair memory / waiver / rework ledger 是必要 evidence；producer 不能只给最终 DSL 而不交代 request、decision、diff、SL-10 批示和下一步。
- `SD-10` / `SL-10B` 只允许作为 local-evidence / legacy-ablation 线索，不是默认主链。
- scenario 证据必须区分 `default_prefix`、`executed_prefix`、`reachable_prefix`、`external_input_initial_vars` 与 `diagnostic_hot_start`；不能把 hot-start 冒充主 BVS。
- `SD-6` 与 NFRR scenario provenance 是 skill evidence 的必要组成；若工具或样本复杂度导致只能做弱 oracle，必须显式标注。
- 禁止针对 ABS / Elevator / CARA / LNG 等具体样本写 lexical special-case；所有优化必须是普适、可迁移的 skill/toolbox 使用规则。

## 使用边界

- `SD-*`：确定性工具，后续可被 Codex / Claude / ref-model pipeline / Path1 / Path2 直接调用。
- `SL-*`：只暴露 prompt generator / stage spec / input-output schema；skill 使用者自行调用 LLM 或 subagent。
- `SC-*`：control、trace、budget、ScenarioSet freeze 与 run-record 写入。
- 程序化调用入口优先使用 `archive.agent_loop_method.stages.api`；SC/control 摘要使用 `archive.agent_loop_method.stages.sc_control`；SL prompt facade 使用 `archive.agent_loop_method.stages.sl_prompt_api`。这些入口不读取 `.env`、不调用 provider，也不得调用 `archive.agent_loop_method.loop.run_agent_loop(...)`。
- `agent_loop_skill/stages/` 下的 symlink 只是人类可读 stage 文档索引，不是程序化调用 API；工具调用必须走上面的 Python facade。
- 每次完整 loop 必须产出一个自包含 `AgentLoopRunRecord` 单文件；PR-0 冻结字段，PR-2A/PR-2B 实现写入器。

## Stage 顺序

`SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13`

其中 `SC-5F` 是 ScenarioSet freeze，`SC-11` 是接受 candidate 并触发下一轮 `SD-2` 完整重验的 control 节点，`SC-13` 是 Trace/Audit；不要把 `SC-11` 改义为 final success 或 run-record 写入。PR-E1 默认 repair 链路是 `SD-8 FixRequestBatch -> SL-9 per-request accept/reject + repair -> SL-10(NL + FixLog + local evidence) -> SC-11`；旧 `SD-10`/`SL-10B` 仅作为 local evidence / legacy ablation。

## 入口文档

- [tools.md](./tools.md)
- [prompts.md](./prompts.md)
- [stages/README.md](./stages/README.md)
- [health_check.py](./health_check.py)
- [codex_exec_experiment_guide.md](./codex_exec_experiment_guide.md)


## PR-C config / default runtime contract

- 默认入口：`archive.agent_loop_method.loop.run_agent_loop(nl, LoopConfig())`，其中 `LoopConfig()` 必须保持 `experiment_default/full_staged_v1`，并执行 full staged runtime；这不是 skill 程序化调用入口，PR-E2 ref-model producer 不得调用它。
- legacy：旧 A0-A4 full loop 已从 active skill entry 移除；新工作不得调用 `archive.agent_loop_method.legacy_loop`，确定性对照应走 `archive.agent_loop_method.experiments.ablation`。
- skill 使用者若要生成 ref model，应使用 `SL-*` prompt generators 自行调用 LLM/subagent；`SD-*` deterministic tools 可直接作为封装工具调用。
- 任何 ablation 都要显式 `condition_id/base_condition_id/changed_factors/academic_question`，并在 run record 中记录 resolved config 与 condition hash。
- 默认入口接 PR-B1 driver + PR-B2 real-env LLM adapters；provider/schema/empty-output retry exhaustion 必须以 `provider_error` / `invalid` 等可追溯 verdict 退出并写 run record，不得回退 fake。
- fake / mock / replay / hot-start 只能通过显式非默认 profile 或专用 smoke/replay runner 启用，并在 run record 中标记 `main_result_eligible=false` 或明确 exclusion reason。
- run record 必须包含 stage / iteration / LLM interaction / deterministic feedback / repair / scenario / environment / final artifacts / redaction report；secret 不得以原文落盘。

## PR-B2 LLM stage adapter 边界

- `archive.agent_loop_method.llm_stages` 提供仓库内部可调用的 `SL-1/SL-5/SL-7/SL-9/SL-10` execution units，用于 PR-C/PR-E1 集成；旧 `SL-10B` 保留为 legacy/ablation。
- skill 使用者仍可只使用 prompt generator 自行调用 LLM/subagent；`llm_stages.py` 是 method runtime 的 adapter，不改变 `SL-*` prompt-only 规范。
- retry 只限 LLM 层 provider/network/schema/empty-output，不处理 deterministic stage fail。
- 每个 adapter 输出 `interaction` payload 与 `redaction_report`，应写入后续 `AgentLoopRunRecord.llm_interactions`。
