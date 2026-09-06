# extraction_notes

## 1. 抽取命令 / 脚本

使用 `pandas.read_parquet("assets/raw/umlcode_state_diagram_train.parquet")` 读取 HF 一手 parquet，并全量抽取 `input` / `uml_code` 两列。

## 2. 当前全量抽取结果

- raw 行数：999。
- validator 可回溯行数：999。
- 可计生成 STM_0 行数：989。
- 不计 eligible 的生成失败行：10，索引为 `[60, 101, 162, 194, 309, 418, 607, 785, 838, 890]`，`uml_code` 内容均为同一个 sentinel：`No valid PlantUML code found.`。这 10 行已在 `validation_summary.excluded_pair_ids` 中列出，只作 NL-only / failure 审计，不参与 eligible pair 或 unique generated `STM_0` 统计；若把失败 sentinel 误当输出一起去重，会得到 990 个 `uml_code` unique，这是错误口径。

## 3. 异常与 caveat

公开学术资源按引用原作处理，许可 / 再分发不再作为升绿 blocker；本条目当前为 `final_pool_ready`。需要保留的学术 caveat 是：NL 为 synthetic feature description / 非控制系统场景，HF parquet 没有逐行 VLM / human validation score，10 行生成失败必须继续排除。

## 4. 不可提交内容说明

当前 parquet 已在仓库中提交；后续若替换或重下 raw，必须同步更新 SHA-256、HF revision、`pairs.jsonl`、`validation_summary.json` 与 [REGISTRY.md](../../../REGISTRY.md)。

## 5. 校验结果摘要

见 `validation_summary.json`。
