# Agent Loop Skill（PR-0 Contract）

> 入口说明：本目录中的 `SKILL.md` 与 `CLAUDE.md` 是指向本文件的软链接。若某个 agent / CLI 环境不能正确跟随 symlink，应直接读取 `AGENT_LOOP_SKILL.md`，三者在语义上等价；PR comment 中需要如实记录实际读取的是哪个入口。

本目录是 project_1 agent-loop 的 repo-local skill 入口。PR-0 冻结 contract / docs / fixtures / run-record schema，不绑定具体 LLM provider。


## PR-E2 e2e ref-model 使用入口

PR-E2 需要测试的是 Codex / Claude Code 能否拿到本 repo-local skill 后，自主完成 `NL + 完整论文子路径 -> FCSTM/pyfcstm ref model 候选` 的建模、检查、修复与留痕。

- 详细流程见 [e2e_ref_model_guide.md](./e2e_ref_model_guide.md)。
- PR-E2 实测 **不得** 调用 `method.loop.run_agent_loop(...)`、PR-D representative runner 或任何一键 full staged runner。
- 允许长时间运行，时间限制只用于防止 CLI 死锁或失控；质量、grounding、验证和 PR comment 证据优先。
- 所有样本产物必须能写成 PR comment：输入 NL、论文路径、读取材料、候选模型、检查反馈、repair 轨迹、最终判断和 skill 改进建议。


### PR-E2 语法与工具版本注意

当前 skill 使用者必须以实际 `SD-2` parser 为准，而不是只相信历史 grammar 摘要：已知当前 parser 支持 `def int` / `def float`，不支持 `def bool`、`true`、`false`；外部输入注释 `// @external` 不会被默认 `SD-4` 自动消费。详细见 [e2e_ref_model_guide.md](./e2e_ref_model_guide.md)。

## 使用边界

- `SD-*`：确定性工具，后续可被 Codex / Claude / ref-model pipeline / Path1 / Path2 直接调用。
- `SL-*`：只暴露 prompt generator / stage spec / input-output schema；skill 使用者自行调用 LLM 或 subagent。
- `SC-*`：control、trace、budget、ScenarioSet freeze 与 run-record 写入。
- 每次完整 loop 必须产出一个自包含 `AgentLoopRunRecord` 单文件；PR-0 冻结字段，PR-2A/PR-2B 实现写入器。

## Stage 顺序

`SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SD-10 -> SL-10B -> SC-11 -> SC-12 -> SC-13`

其中 `SC-5F` 是 ScenarioSet freeze，`SC-11` 是接受 candidate，`SC-13` 是 Trace/Audit；不要把 `SC-11` 改义为 run-record 写入。

## 入口文档

- [tools.md](./tools.md)
- [prompts.md](./prompts.md)
- [stages/](./stages/)


## PR-C config / default runtime contract

- 默认入口：`method.loop.run_agent_loop(nl, LoopConfig())`，其中 `LoopConfig()` 必须保持 `experiment_default/full_staged_v1`，并执行 full staged runtime。
- legacy：旧 A0-A4 loop 只能通过 `method.legacy_loop.run_legacy_agent_loop()` 显式调用，并视为 deprecated。
- skill 使用者若要生成 ref model，应使用 `SL-*` prompt generators 自行调用 LLM/subagent；`SD-*` deterministic tools 可直接作为封装工具调用。
- 任何 ablation 都要显式 `condition_id/base_condition_id/changed_factors/academic_question`，并在 run record 中记录 resolved config 与 condition hash。
- 默认入口接 PR-B1 driver + PR-B2 real-env LLM adapters；provider/schema/empty-output retry exhaustion 必须以 `provider_error` / `invalid` 等可追溯 verdict 退出并写 run record，不得回退 fake。
- fake / mock / replay / hot-start 只能通过显式非默认 profile 或专用 smoke/replay runner 启用，并在 run record 中标记 `main_result_eligible=false` 或明确 exclusion reason。
- run record 必须包含 stage / iteration / LLM interaction / deterministic feedback / repair / scenario / environment / final artifacts / redaction report；secret 不得以原文落盘。

## PR-B2 LLM stage adapter 边界

- `method.llm_stages` 提供仓库内部可调用的 `SL-1/SL-5/SL-7/SL-9/SL-10B` execution units，用于 PR-C 集成。
- skill 使用者仍可只使用 prompt generator 自行调用 LLM/subagent；`llm_stages.py` 是 method runtime 的 adapter，不改变 `SL-*` prompt-only 规范。
- retry 只限 LLM 层 provider/network/schema/empty-output，不处理 deterministic stage fail。
- 每个 adapter 输出 `interaction` payload 与 `redaction_report`，应写入后续 `AgentLoopRunRecord.llm_interactions`。
