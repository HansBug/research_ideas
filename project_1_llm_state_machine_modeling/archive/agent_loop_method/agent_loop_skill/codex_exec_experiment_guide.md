# PR-M3 codex exec skill 标准实验入口指南

本文件定义 PR-M3 中 `codex exec` / mature coding agent 使用 `agent_loop_skill` 的标准实验入口。它与 E1 LangGraph full staged agent-loop 是并列但不同的证据来源：E1 保存受控 `AgentLoopRunRecord`，M3 保存外部可观测的 `codex exec --json` event stream、工具/检查/修复 ledger、NFRR 与人类可读 `report.md`。

## 1. 入口与配置合同

正式运行必须从仓库根目录执行，并在运行前加载本地环境：

```bash
source venv/bin/activate
set -a; source .env; set +a
python -m project_1_llm_state_machine_modeling.method.experiments.codex_exec_skill_runs --case-set all --out-root runs/codex_exec_skill/<run_id>
```

默认非敏感配置为：`CODEX_EXEC_DEFAULT_CONFIG=model_provider=airouter`。解析优先级固定为：tracked default -> `.env` -> process env -> CLI default -> extra -> override；最终必须展开成一个或多个 `codex exec -c key=value`，并在 `run_manifest.json` / `env.redacted.json` / `command.redacted.txt` 中以脱敏形式记录。正式实验必须使用 `codex exec --json`，不得使用 `--ephemeral`。

可选环境变量：

| 变量 | 用途 |
|---|---|
| `CODEX_EXEC_DEFAULT_CONFIG` | 默认 `-c` 配置，默认值应包含 `model_provider=airouter`。 |
| `CODEX_EXEC_EXTRA_CONFIG` | 追加配置，例如模型名或 reasoning 配置。 |
| `CODEX_EXEC_OVERRIDE_CONFIG` | 覆盖同名 key；优先级最高。 |

## 2. 禁止项与允许项

禁止调用：`method.loop.run_agent_loop(...)`、PR-D representative runner、PR-E1 real-run runner、任何一键 full staged runner。M3 不能把 E1 运行结果包装成 E2 skill 产物。

允许使用：仓库搜索、论文材料、`method.stages.api` / `method.stages.sc_control` / `method.stages.sl_prompt_api`、SD deterministic tools、SL prompt generators、pyfcstm parse/build/inspect/sim utilities。Codex 可以发挥 mature-agent 能力组织 scratch scripts、局部检查、重试和自我修复，但过程必须落盘并可审计。

## 3. 每例 artifact package

每个样本目录至少包含：

```text
run_manifest.json
prompt.md
command.redacted.txt
env.redacted.json
codex_events.jsonl
codex_stdout.log
codex_stderr.log
codex_transcript.redacted.md
last_message.md
final_model.fcstm
report.md
metadata.json
actual_file_reads.json
tool_stage_check_ledger.json
repair_ledger.json
nfrr_report.json
forbidden_call_check.json
redaction_report.json
run_summary.md
```

invalid-run 不能伪造模型；但仍必须保留 manifest、命令、env、事件/日志、redaction report、exit code、duration 与 invalid reason。

## 4. `report.md` 人类可读要求

`report.md` 必须中文为主，允许必要英文术语，帮助 reviewer 不下载原始 JSON 也能理解本次运行：

| 章节 | 必须内容 |
|---|---|
| Run identity | case、Path、输入模式、输出目录、provider config 脱敏标签、状态。 |
| Input | NL 原文、NL 中文翻译/释义、paper_dir。 |
| Actual reads | 实际读取 skill docs、论文文件、工具/API 文件。 |
| Process table | grounding、initial modeling、SD checks、repair/waiver、NFRR、final audit 的全过程摘要。 |
| Final FCSTM | 模型全文与 hash。 |
| Checks | SD-2/SD-3/SD-4/SD-5A/SD-6、forbidden-call、redaction。 |
| Repair ledger | 每个 fix request、accept/reject/waiver、diff/local evidence/SL-10 式判断。 |
| NFRR | claim、ledger 摘要、八维 vector、tier/cap/allowed_use。 |
| Limitations | synthetic abstraction、弱 oracle、无法主 BVS 的场景、人工签核缺口。 |

## 5. PR comment evidence 要求

四例运行后，PR comment 不得只贴 final FCSTM。至少要包含每例的 NL/NL_zh、paper_dir、实际读取文件摘要、artifact 链接、final FCSTM、全过程摘要表、检查/修复/NFRR 结果、禁止调用项检查、redaction 状态、与 E1 evidence 锚点的边界比较。

## 6. 四例纪律

PR-M3 实现阶段必须运行 ABS / CARA / Elevator / LNG 四例。provider/network/CLI 50x/timeout/crash 属于 invalid evidence，需要重跑；模型质量、证据链、禁止调用项、redaction 或 report 缺失属于本 PR 可修复问题。运行产物可暂时提交进 PR 供 reviewer 审计，是否清理等待用户指示。
