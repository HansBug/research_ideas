# PR39 agent-loop / LangGraph final four-case evidence（2026-06-08 05:25:52）

本目录是 PR #39 合并前保留的 **agent-loop 侧最后一次代表性真实运行结果**。它用于证明 LangGraph 化后的 `method.loop.run_agent_loop(...)` 在四个代表样例上的最终可审计运行状态，而不是保存所有中间探索产物。

## 为什么保留这份 evidence

- 时间：`2026-06-08 05:25:52`（目录名中的 `052552`）。
- PR：[#39](https://github.com/HansBug/research_ideas/pull/39) `feature/project1-pr-langgraph`。
- 用途：作为 #39 agent-loop 侧 retained evidence root，支撑最终 review 对 LangGraph runtime、FixLog、stream/operator log、scenario/report 可审计性的检查。
- 范围：只代表 #39 最后一轮有借鉴意义的四例 agent-loop evidence；历史中间 runs 已按用户要求从 PR-facing diff 中清理。

## 子目录说明

| 子目录 | case | 结论 | 说明 |
|---|---|---|---|
| [path1-abs-agent-loop-success](./path1-abs-agent-loop-success/README.md) | `path1_abs` | success | ABS 三态制动监管器，Path1 样例。 |
| [path1-cara-agent-loop-success](./path1-cara-agent-loop-success/README.md) | `path1_cara` | success | CARA 控制样例，经历 repair 后收敛。 |
| [path1-elevator-agent-loop-success](./path1-elevator-agent-loop-success/README.md) | `path1_elevator` | success | Elevator 控制样例，Path1 样例。 |
| [path2-lng-ems-agent-loop-success-not-blueprint](./path2-lng-ems-agent-loop-success-not-blueprint/README.md) | `path2_lng_ems` | success / not blueprint | LNG EMS Path2 样例，主运行收敛但 `path2_ref_model_blueprint_eligible=false`，不能宣传为 Path2 ref-model blueprint。 |

## 入口文件

- [SUMMARY.md](./SUMMARY.md)：四例总体摘要。
- [summary.json](./summary.json)：机器可读摘要。
- [pr_comment.md](./pr_comment.md)：当时用于 PR comment 的长报告正文。
- [comment_parts/](./comment_parts/)：长 comment 分片。

## 审计注意事项

1. 本目录下每个 case 的 `*.agent_loop.json.gz`、`operator_log.jsonl`、`stream_summary.json`、`flow_log.json`、`fix_log.json`、`run_logs/` 是真实运行证据。
2. 子目录名称是后续为可读性重命名的 PR-facing retained evidence 名称；内部 `run_id` 文件名保留当时生成的唯一运行 ID，便于与原始 run record 对齐。
3. 本 evidence 只证明 agent-loop 侧最终代表性状态；skill / codex-exec 侧 evidence 见 [../codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/README.md](../codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/README.md)。
