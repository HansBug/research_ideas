# path2-lng-ems-codex-exec-skill-completed

LNG EMS Path2 样例，codex exec skill 标准入口完成样例；provider 恢复错误已入账。

## 基本信息

| 字段 | 值 |
|---|---|
| evidence root | [2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/](../README.md) |
| case_key | `path2_lng_ems` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| path | `path2` |
| status | `success` |
| run_label | `pr_m3_four_clean_20260608_133322` |
| exit_code | `0` |
| nfrr_final_tier | `T2` |
| allowed_use | `reviewer_queue` |
| recovered_provider_error_count | `2` |

## 主要文件

| 文件 | 用途 |
|---|---|
| [report.md](./report.md) | 人类可读实验报告：输入、实际读取文件、过程摘要、检查/修复/NFRR、final FCSTM、质量风险。 |
| [metadata.json](./metadata.json) | producer 写出的机器可读 metadata。 |
| [final_model.fcstm](./final_model.fcstm) | codex exec skill 入口生成的最终模型。 |
| [actual_file_reads.json](./actual_file_reads.json) | 实际读取材料记录。 |
| [tool_stage_check_ledger.json](./tool_stage_check_ledger.json) | tool / stage check 证据台账。 |
| [repair_ledger.json](./repair_ledger.json) | repair / waiver / diff / review 台账。 |
| [nfrr_report.json](./nfrr_report.json) | NFRR v3 自评与 cap / allowed-use 结果。 |
| [run_manifest.json](./run_manifest.json) | runner-owned 运行 manifest。 |
| [run_summary.md](./run_summary.md) | runner-owned 人类摘要。 |
| [codex_events.jsonl](./codex_events.jsonl) | `codex exec --json` 原始 event stream。 |
| [codex_transcript.redacted.md](./codex_transcript.redacted.md) | 脱敏 transcript。 |
| [command.redacted.txt](./command.redacted.txt) | 脱敏命令。 |
| [env.redacted.json](./env.redacted.json) | 脱敏环境摘要。 |
| [forbidden_call_check.json](./forbidden_call_check.json) | 禁止调用顶层 agent-loop / PR-D / PR-E1 runner 的检查结果。 |
| [redaction_report.json](./redaction_report.json) | 脱敏检查结果。 |
| [checks/normalized_summary.json](./checks/normalized_summary.json) | postprocess 后的标准化摘要。 |

## 审计口径

1. 子目录名称是 PR #39 retained evidence cleanup 后追加的语义化名称。
2. `prompt.md`、`command.redacted.txt`、`codex_events.jsonl`、`codex_transcript.redacted.md`、`run_manifest.json` 等 runner-owned 文件保留运行当时写入的原始输出路径文本；这不是 stale link，而是为了保留真实执行日志。
3. 若需要点击当前 PR-facing 路径，请优先使用本 README 中的相对链接；若需要核对真实运行命令，请以 runner-owned 原始日志为准。
4. 本目录证明的是 skill / mature-agent 入口的可执行性与审计链，不等价于 agent-loop E1 hidden reasoning/run record。

## LNG 特别说明

该 case 的 recovered provider/network error 已在 runner summary / normalized summary 中显式入账；这类外部错误不作为模型质量失败，但必须保留在审计证据中。
