# extraction_notes

## 1. 抽取命令 / 脚本

使用 `pandas.read_parquet("assets/raw/umlcode_state_diagram_train.parquet")` 读取 HF 一手 parquet，并全量抽取 `input` / `uml_code` 两列。

## 2. 当前全量抽取结果

- raw 行数：999。
- validator 可回溯行数：999。
- 可计生成 STM_0 行数：989。
- 不计 eligible 的生成失败行：10，索引为 `[60, 101, 162, 194, 309, 418, 607, 785, 838, 890]`，`uml_code` 内容为 `No valid PlantUML code found.`。

## 3. 异常与降级

HF dataset license 未在当前 metadata 中明确出现，且 NL 是 synthetic feature description / 非控制系统场景；因此条目只能是 `conditional_final_pool`，不能标为 `final_pool_ready`。

## 4. 不可提交内容说明

当前 parquet 已在仓库中提交；若后续发现 license 限制，需改为 metadata/hash/local_only 口径。

## 5. 校验结果摘要

见 `validation_summary.json`。
