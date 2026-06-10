# path1_parquet/：PR #9 历史 Path-1 parquet 数据

本目录归档历史 PR #9 生成的 Path-1 sprint 数据文件。

## 文件说明

| 文件 | 说明 |
|---|---|
| [sources_path1.parquet](./sources_path1.parquet) | 历史 sprint 主数据文件。 |
| [sources_path1_backup.parquet](./sources_path1_backup.parquet) | 历史 sprint 备份数据文件。 |

## 使用原则

1. 这两个 parquet 是历史数据快照，不自动等同于当前正式 paper sample registry。
2. 后续如果继续使用，必须记录 schema、row count、hash、来源规则和 eligibility filter。
3. 若 parquet 内容与 [selection_screening/](../selection_screening/) 或 [nl_expansion/](../nl_expansion/) 不一致，应以重新冻结后的 `sample_registry.csv` 为准。
