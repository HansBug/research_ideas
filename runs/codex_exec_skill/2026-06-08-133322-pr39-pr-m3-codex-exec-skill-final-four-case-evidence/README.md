# PR39 / PR-M3 codex exec skill final four-case evidence（2026-06-08 13:33:22）

本目录是 PR #39 合并前保留的 **skill / codex-exec 侧最后一次代表性真实运行结果**。它来自 PR-M3，将 `codex exec --json` 作为 mature-agent skill 实验入口来验证 `agent_loop_skill/` 在 M1 后仍能被 Codex 类 agent 独立读取、执行、记录与审计。

## 为什么保留这份 evidence

- 时间：`2026-06-08 13:33:22`（目录名中的 `133322`）。
- PR：PR-M3 [#79](https://github.com/HansBug/research_ideas/pull/79)，已 merge 回 PR #39。
- 用途：作为 #39 skill / codex-exec 侧 retained evidence root，支撑最终 review 对 `codex exec --json`、artifact package、redaction、forbidden-call check、NFRR/report 可审计性的检查。
- 范围：只代表 PR-M3 clean 四例 evidence；历史 dry-run / superseded runs 已按用户要求从 PR-facing diff 中清理。

## 子目录说明

| 子目录 | case | 结论 | 说明 |
|---|---|---|---|
| [path1-abs-codex-exec-skill-completed](./path1-abs-codex-exec-skill-completed/README.md) | `path1_abs` | completed | ABS 三态制动监管器，skill 入口完整产物。 |
| [path1-cara-codex-exec-skill-completed](./path1-cara-codex-exec-skill-completed/README.md) | `path1_cara` | completed | CARA 样例，skill 入口完整产物。 |
| [path1-elevator-codex-exec-skill-completed](./path1-elevator-codex-exec-skill-completed/README.md) | `path1_elevator` | completed | Elevator 样例，skill 入口完整产物。 |
| [path2-lng-ems-codex-exec-skill-completed](./path2-lng-ems-codex-exec-skill-completed/README.md) | `path2_lng_ems` | completed | LNG EMS 样例，LNG recovered provider errors=2 已显式入账。 |

## 入口文件

- [runner_summary.json](./runner_summary.json)：四例机器可读总摘要。
- [runner_invocation.json](./runner_invocation.json)：runner 调用参数摘要。
- [refresh_summary.json](./refresh_summary.json)：postprocess / refresh 摘要。

## 审计注意事项

1. 子目录名称是后续为可读性重命名的 PR-facing retained evidence 名称。
2. `codex_events.jsonl`、`codex_transcript.redacted.md`、`command.redacted.txt`、`prompt.md`、`run_manifest.json` 等 runner-owned 原始审计文件 **保留运行当时写入的原始输出路径文本**；这不是 stale link，而是为了不篡改真实执行日志。
3. 导航性文件（README、report/metadata 中的审计入口）可用当前语义化目录名追踪；若需要核对真实命令，应以 runner-owned 原始日志为准。
4. 本 evidence 不调用顶层 agent-loop 冒充 E1；它证明的是 skill / mature-agent 入口的可执行性与可审计性。
