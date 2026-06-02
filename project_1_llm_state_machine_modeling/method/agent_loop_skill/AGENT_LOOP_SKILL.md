# Agent Loop Skill（PR-0 Contract）

本目录是 project_1 agent-loop 的 repo-local skill 入口。PR-0 冻结 contract / docs / fixtures / run-record schema，不绑定具体 LLM provider。

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


## PR-A config / ablation contract

- 默认入口：`method.loop.run_agent_loop(nl, LoopConfig())`，其中 `LoopConfig()` 必须保持 `experiment_default/full_staged_v1`。
- legacy：旧 A0-A4 loop 只能通过 `method.legacy_loop.run_legacy_agent_loop()` 显式调用，并视为 deprecated。
- skill 使用者若要生成 ref model，应使用 `SL-*` prompt generators 自行调用 LLM/subagent；`SD-*` deterministic tools 可直接作为封装工具调用。
- 任何 ablation 都要显式 `condition_id/base_condition_id/changed_factors/academic_question`，并在 run record 中记录 resolved config 与 condition hash。
- PR-A 阶段 façade 只写 contract-only run record；`main_result_eligible=false`。真实 full runtime 在后续 PR-C 才可作为 Path1/Path2 主实验入口。

## PR-B2 LLM stage adapter 边界

- `method.llm_stages` 提供仓库内部可调用的 `SL-1/SL-5/SL-7/SL-9/SL-10B` execution units，用于 PR-C 集成。
- skill 使用者仍可只使用 prompt generator 自行调用 LLM/subagent；`llm_stages.py` 是 method runtime 的 adapter，不改变 `SL-*` prompt-only 规范。
- retry 只限 LLM 层 provider/network/schema/empty-output，不处理 deterministic stage fail。
- 每个 adapter 输出 `interaction` payload 与 `redaction_report`，应写入后续 `AgentLoopRunRecord.llm_interactions`。
