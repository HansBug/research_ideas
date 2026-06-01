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
