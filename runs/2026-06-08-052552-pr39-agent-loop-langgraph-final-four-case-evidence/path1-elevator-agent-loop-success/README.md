# path1-elevator-agent-loop-success

Elevator 控制样例，Path1 agent-loop 成功样例。

## 基本信息

| 字段 | 值 |
|---|---|
| evidence root | [2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/](../README.md) |
| case_key | `path1_elevator` |
| case_id | `automatic-elevator-controller` |
| path | `path1` |
| run_id | `pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175` |
| record_status | `success` |
| result_status | `converged` |
| main_result_eligible | `True` |
| path2_ref_model_blueprint_eligible | 不适用 |

## 主要文件

| 文件 | 用途 |
|---|---|
| [report.md](./report.md) | 人类可读完整运行报告：NL/NL_zh、stage 表、scenario pass 情况、repair 细节、final FCSTM 等。 |
| [summary.json](./summary.json) | 机器可读 case 摘要。 |
| [checks.json](./checks.json) | 本次运行的检查结果摘要。 |
| [final.fcstm](./final.fcstm) | 最终生成的 FCSTM 模型。 |
| [fix_log.json](./fix_log.json) | Fix request / accept-reject / repair / review 台账。 |
| [flow_log.json](./flow_log.json) | stage 进入、退出与跳转流程日志。 |
| [pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) | 压缩后的完整 `AgentLoopRunRecord` 原始证据。 |
| [pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.operator_log.jsonl](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.operator_log.jsonl) | terminal/operator 友好的 LangGraph stream / stage 事件日志。 |
| [pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.stream_summary.json](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.stream_summary.json) | LLM stream 汇总与 payload hash。 |
| [run_logs/stdout.txt](./run_logs/stdout.txt) | 真实运行 stdout 留档。 |
| [run_logs/stderr.txt](./run_logs/stderr.txt) | 真实运行 stderr 留档。 |

## 审计口径

1. 子目录名称是 PR #39 retained evidence cleanup 后追加的语义化名称；内部 `run_id` 文件名保持真实运行时生成的唯一 ID。
2. 若 `report.md` / `summary.json` 中存在运行时生成的原始 run ID，这是正常现象，不应视为无意义残留。
3. 本目录只代表该 case 的最后一次保留运行，不包含被 superseded 的历史探索 run。
