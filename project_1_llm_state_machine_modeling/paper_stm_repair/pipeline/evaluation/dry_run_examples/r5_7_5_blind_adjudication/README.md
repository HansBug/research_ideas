# R5.7.5 blind adjudication dry-run bundle

本目录是 R5.7.5 在 answer-key constructed suite 之后追加的 **full blind adjudication dry-run** 工作区。`blind_inputs/` 可交给 judge；`oracle_answer_key.json` 禁止作为 judge 输入，只能由 scorer 使用。

硬纪律：blind input 不得包含 expected verdict、oracle mapping、原 Cxx answer-key slug 或构造意图。所有 judge prompt、raw output、parsed output、stdout/stderr、exit code 与 run meta 都必须写盘。

## 1. 当前最终结果

最终全量运行见 [judge_outputs/deepseek-blind-judge/final_run_manifest.json](./judge_outputs/deepseek-blind-judge/final_run_manifest.json) 与 [judge_outputs/deepseek-blind-judge/score_summary.json](./judge_outputs/deepseek-blind-judge/score_summary.json)：

| 指标 | 数值 |
|---|---:|
| judge | `deepseek-blind-judge` |
| final run window | `2026-07-05T06:56:17` -- `2026-07-05T07:18:31` |
| case_count | 20 |
| valid_output_count | 20 |
| verdict_match_count | 20 |
| scope_match_count | 20 |
| run_validity_match_count | 20 |
| leakage_detected_count | 0 |

该结果只证明 blind adjudication protocol 在 constructed cases 上可执行；不代表真实 repair loop 效果。

## 2. 文件说明

| 文件 / 子路径 | 说明 |
|---|---|
| [blind_input_index.json](./blind_input_index.json) | 20 个 Bxx blind input 的导航索引，不含 oracle。 |
| [blind_inputs/](./blind_inputs/) | judge 可读取的 blind input；每个 Bxx 包含 `input_packet.json`、NL、raw STM0、canonical STM0、candidate STMk。 |
| [oracle_answer_key.json](./oracle_answer_key.json) | hidden oracle；只能 scorer 使用，禁止进入 prompt。 |
| [build_blind_bundle.py](./build_blind_bundle.py) | 从 constructed suite 刷新 blind input 与 oracle，保留 Bxx→Cxx mapping。 |
| [leakage_check.py](./leakage_check.py) | 检查 blind inputs 是否泄露 expected verdict / oracle / Cxx slug。 |
| [run_blind_judge.py](./run_blind_judge.py) | 逐 case 构造 prompt、调用 isolated judge、写盘全过程。 |
| [score_blind_outputs.py](./score_blind_outputs.py) | 对 judge output 做 schema 校验并与 hidden oracle 比对。 |
| [judge_outputs/deepseek-blind-judge/](./judge_outputs/deepseek-blind-judge/) | 最终 DeepSeek judge 输出；每个 Bxx 保存 prompt/raw/parsed/stdout/stderr/run meta。 |

## 3. 复验命令

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_blind_bundle.py
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/leakage_check.py
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py --judge deepseek-blind-judge
```

若要重新执行真实 blind judge，必须先 `source .env`，再逐 case 调用：

```bash
source .env
BASE=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication
for i in $(seq -w 1 20); do
  python "$BASE/run_blind_judge.py" --judge deepseek --case "B$i" --timeout 900
done
python "$BASE/score_blind_outputs.py" --judge deepseek-blind-judge
```
