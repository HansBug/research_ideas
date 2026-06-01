# Agent Loop Skill（PR-0 Contract）

本目录是 project_1 agent-loop 的 repo-local skill 入口。PR-0 只冻结 contract / docs / fixtures，不绑定具体 LLM provider。

## 使用边界

- `SD-*`：确定性工具，后续可被 Codex / Claude / ref-model pipeline / Path1 / Path2 直接调用。
- `SL-*`：prompt generator / stage spec，skill 使用者自行调用 LLM 或 subagent。
- 每次完整 loop 后续必须产出 `AgentLoopRunRecord` 单文件；PR-0 只冻结 schema 与 fixture。

## 入口文档

- [tools.md](./tools.md)
- [prompts.md](./prompts.md)
- [stages/](./stages/)
