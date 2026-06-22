# extraction_notes

## 1. 抽取命令 / 脚本

使用 `pandas.read_parquet("assets/raw/umlcode_state_diagram_train.parquet")` 读取 HF 一手 parquet，并取 `input` / `uml_code` 两列。

## 2. 人工步骤

本 PR 只人工确认前三行可读性，不声称全量 PlantUML 可 parse / render。

## 3. 异常与降级

HF dataset license 未在当前 metadata 中明确出现；因此条目只能是 `conditional_final_pool`，不能标为 `final_pool_ready`。

## 4. 不可提交内容说明

当前 parquet 已在仓库中提交；若后续发现 license 限制，需改为 metadata/hash/local_only 口径。

## 5. 校验结果摘要

见 `validation_summary.json`。
