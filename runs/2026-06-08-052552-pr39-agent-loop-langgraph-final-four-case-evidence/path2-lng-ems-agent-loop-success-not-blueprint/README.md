# path2-lng-ems-agent-loop-success-not-blueprint

LNG EMS Path2 样例，agent-loop 主运行成功，但不具备 Path2 ref-model blueprint 资格。

## 基本信息

| 字段 | 值 |
|---|---|
| evidence root | [2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/](../README.md) |
| case_key | `path2_lng_ems` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| path | `path2` |
| run_id | `pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f` |
| record_status | `success` |
| result_status | `converged` |
| main_result_eligible | `True` |
| path2_ref_model_blueprint_eligible | false（不可宣传为 Path2 ref-model blueprint） |

## 主要文件

| 文件 | 用途 |
|---|---|
| [report.md](./report.md) | 人类可读完整运行报告：NL/NL_zh、stage 表、scenario pass 情况、repair 细节、final FCSTM 等。 |
| [summary.json](./summary.json) | 机器可读 case 摘要。 |
| [checks.json](./checks.json) | 本次运行的检查结果摘要。 |
| [final.fcstm](./final.fcstm) | 最终生成的 FCSTM 模型。 |
| [fix_log.json](./fix_log.json) | Fix request / accept-reject / repair / review 台账。 |
| [flow_log.json](./flow_log.json) | stage 进入、退出与跳转流程日志。 |
| [pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) | 压缩后的完整 `AgentLoopRunRecord` 原始证据。 |
| [pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.operator_log.jsonl](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.operator_log.jsonl) | terminal/operator 友好的 LangGraph stream / stage 事件日志。 |
| [pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.stream_summary.json](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.stream_summary.json) | LLM stream 汇总与 payload hash。 |
| [run_logs/stdout.txt](./run_logs/stdout.txt) | 真实运行 stdout 留档。 |
| [run_logs/stderr.txt](./run_logs/stderr.txt) | 真实运行 stderr 留档。 |

## 审计口径

1. 子目录名称是 PR #39 retained evidence cleanup 后追加的语义化名称；内部 `run_id` 文件名保持真实运行时生成的唯一 ID。
2. 若 `report.md` / `summary.json` 中存在运行时生成的原始 run ID，这是正常现象，不应视为无意义残留。
3. 本目录只代表该 case 的最后一次保留运行，不包含被 superseded 的历史探索 run。

## Path2 特别说明

该运行 `main_result_eligible=true`，但 `path2_ref_model_blueprint_eligible=false`。它可以作为 agent-loop 收敛性、repair/waiver、scenario/review 过程的压力证据，但不能在论文或上游 PR 中宣传为 LNG Path2 reference model blueprint。
