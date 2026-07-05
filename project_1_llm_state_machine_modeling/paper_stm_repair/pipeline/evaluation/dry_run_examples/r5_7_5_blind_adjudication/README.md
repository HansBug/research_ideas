# R5.7.5 blind adjudication dry-run bundle

本目录是 R5.7.5 在 answer-key constructed suite 之后追加的 **full blind adjudication dry-run** 工作区。`blind_inputs/` 可交给 judge；`oracle_answer_key.json` 禁止作为 judge 输入，只能由 scorer 使用。

硬纪律：blind input 不得包含 expected verdict、oracle mapping、原 Cxx answer-key slug 或构造意图。所有 judge prompt、raw output、parsed output、stdout/stderr、exit code 与 run meta 都必须写盘；final 结果还必须通过 prompt consistency check，避免候选或 prompt 修改后继续引用 stale output。

## 1. 当前最终结果

最终 eligible 全量运行见 [judge_outputs/claude-blind-judge/final_run_manifest.json](./judge_outputs/claude-blind-judge/final_run_manifest.json)、[judge_outputs/claude-blind-judge/score_summary.json](./judge_outputs/claude-blind-judge/score_summary.json) 与 [judge_outputs/claude-blind-judge/prompt_consistency_check.stdout.json](./judge_outputs/claude-blind-judge/prompt_consistency_check.stdout.json)：

| 指标 | 数值 |
|---|---:|
| judge | `claude-blind-judge` |
| final run window | `2026-07-05T14:40:09` -- `2026-07-05T14:54:39` |
| case_count | 20 |
| valid_output_count | 20 |
| verdict_match_count | 20 |
| scope_match_count | 20 |
| run_validity_match_count | 20 |
| gate_all_match_count | 6 |
| gate_disagreement_count | 25 |
| leakage_detected_count | 0 |
| prompt mismatch count | 0 |

该结果只证明 blind adjudication protocol 在 constructed cases 上可执行，并为 prompt/oracle/case calibration 提供证据；不代表真实 repair loop 效果。`run_validity_match_count=20` 使用 scorer 中的归一化等价桶（例如 constructed-valid 与 blind-valid 都归为 `valid`），不是 expected / observed 原始字符串逐字相等。Claude final run 的 archived command 记录 requested model alias 为 `sonnet`，当前 CLI run meta 未暴露 provider-side exact `model_id`；因此本目录不能作为模型比较证据，后续真实 LLM runs 必须在 provider 支持时补齐精确模型 ID。


## 1.5 Multi-judge 追加复验（Codex / DeepSeek）

R5.7.5 后续追加了 Codex-DeepSeek 与 Codex CLI 的 replication，用于检查同一 blind bundle / prompt / schema 是否跨 judge family 仍可执行。该结果仍只服务于 constructed protocol dry-run，不是 repair effectiveness 或模型比较。

Codex 复验口径：完整 B01 prompt 在 `codex exec --output-schema` 下仍会触发 provider 502；当前 final Codex run 改用直接 `codex exec` + `-o last_message.txt`，并由本地 `jsonschema` 对 archived `last_message/stdout` 做严格结构校验后才计入 eligible。每个 case 的 `run_meta_start.json` 均记录 `cli_output_schema_mode=local_jsonschema_validation_no_cli_output_schema`。

| judge | case_count | valid outputs | verdict match | scope match | run-validity match | gate all match | gate disagreements | leakage | 当前用途 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [`claude-blind-judge`](./judge_outputs/claude-blind-judge/) | 20 | 20 | 20 | 20 | 20 | 6 | 25 | 0 | final eligible truth。 |
| [`deepseek-blind-judge`](./judge_outputs/deepseek-blind-judge/) | 20 | 20 | 20 | 19 | 20 | 6 | 26 | 0 | 有效 replication；B17 的 T0.5 caveat scope mismatch 保留为 calibration evidence。 |
| [`codex-blind-judge`](./judge_outputs/codex-blind-judge/) | 20 | 20 | 18 | 20 | 20 | 9 | 21 | 0 | 有效 replication；B08 `partial→better`、B11 `not_better→unknown` 保留为 calibration evidence。 |

DeepSeek 与 Codex 的 `score_summary.json`、`final_run_manifest.json`、`prompt_consistency_check.stdout.json` 可作为 multi-judge calibration evidence。Codex 当前不再是 provider-failure audit：`score_summary.json` 明确 `eligible_score_applicable=true`、attempted=20、completed=20、provider failures=0、valid outputs=20。旧 `--output-schema` 502 只作为被 supersede 的 provider/CLI caveat，不能再作为当前 Codex final score 口径。

## 2. 文件说明

| 文件 / 子路径 | 说明 |
|---|---|
| [blind_input_index.json](./blind_input_index.json) | 20 个 Bxx blind input 的导航索引，不含 oracle。 |
| [blind_inputs/](./blind_inputs/) | judge 可读取的 blind input；每个 Bxx 包含 `input_packet.json`、NL、raw STM0、canonical STM0、candidate STMk。 |
| [oracle_answer_key.json](./oracle_answer_key.json) | hidden oracle；只能 scorer 使用，禁止进入 prompt。 |
| [build_blind_bundle.py](./build_blind_bundle.py) | 从 constructed suite 刷新 blind input 与 oracle，保留 Bxx→Cxx mapping。 |
| [leakage_check.py](./leakage_check.py) | 检查 blind inputs 是否泄露 expected verdict / oracle / Cxx slug。 |
| [run_blind_judge.py](./run_blind_judge.py) | 逐 case 构造 prompt、调用 isolated judge、写盘全过程。 |
| [score_blind_outputs.py](./score_blind_outputs.py) | 对 judge output 做 schema 校验并与 hidden oracle 比对；provider/CLI nonzero 或 schema-invalid 不计入 final eligible。 |
| [build_final_run_manifest.py](./build_final_run_manifest.py) | 汇总 final score 与每 case prompt/raw/parsed/stdout/stderr/run meta 路径。 |
| [prompt_consistency_check.py](./prompt_consistency_check.py) | 重建当前 prompt 并与归档 `prompt.txt` 比对，防止 stale prompt / stale candidate output 被误报 final。 |
| [judge_outputs/claude-blind-judge/](./judge_outputs/claude-blind-judge/) | 当前 final eligible Claude judge 输出；每个 Bxx 保存 prompt/raw/parsed/stdout/stderr/run meta。 |
| [judge_outputs/deepseek-blind-judge/](./judge_outputs/deepseek-blind-judge/) | DeepSeek full blind replication 输出；primary verdict 20/20，对 B17 scope route 有 1 处 calibration mismatch。 |
| [judge_outputs/codex-blind-judge/](./judge_outputs/codex-blind-judge/) | Codex full blind replication 输出；当前采用 local-jsonschema mode，primary verdict 18/20，对 B08/B11 有 2 处 calibration mismatch。 |

## 3. 复验命令

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_blind_bundle.py
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/leakage_check.py
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/prompt_consistency_check.py --judge claude-blind-judge
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py --judge claude-blind-judge --require-all-valid --require-all-core-match --require-no-leakage
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_final_run_manifest.py --judge claude-blind-judge
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/prompt_consistency_check.py --judge deepseek-blind-judge
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py --judge deepseek-blind-judge --require-all-valid --require-no-leakage
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/prompt_consistency_check.py --judge codex-blind-judge
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py --judge codex-blind-judge --require-all-valid --require-no-leakage
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_final_run_manifest.py --judge codex-blind-judge
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --parse
```

若要重新执行真实 blind judge，必须先 `source .env`，再逐 case 调用：

```bash
source .env
BASE=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication
for i in $(seq -w 1 20); do
  python "$BASE/run_blind_judge.py" --judge claude --case "B$i" --timeout 900
done
python "$BASE/score_blind_outputs.py" --judge claude-blind-judge --require-all-valid --require-all-core-match --require-no-leakage
python "$BASE/build_final_run_manifest.py" --judge claude-blind-judge
python "$BASE/prompt_consistency_check.py" --judge claude-blind-judge
```
