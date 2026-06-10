# dataset_selection/：Path-1 样本选择与历史资产归档

本目录集中管理第一篇 Path-1 paper 的样本选择依据、历史 PR #9 资产归档和后续 frozen sample registry 的入口。

## 文件与目录说明

| 路径 | 作用 |
|---|---|
| [sample_assets.md](./sample_assets.md) | 对 PR #9 可复用样本、扩充 NL、parquet、reference draft 的摘要说明和风险口径。 |
| [asset_summary.json](./asset_summary.json) | 当前归档资产数量摘要，用于快速核对。 |
| [asset_manifest.tsv](./asset_manifest.tsv) | 归档文件级清单，含路径、字节数和 SHA-256，便于追溯。 |
| [legacy_pr9_assets/](./legacy_pr9_assets/) | 从历史 PR #9 搬入的 selection / expansion / parquet / ref-STM 原始资产归档。 |

## 当前归档规模

见 [asset_summary.json](./asset_summary.json)。当前归档包括：

- 323 个 selection review JSON。
- 30 个 NL expansion JSON。
- `sources_path1.parquet` 与 `sources_path1_backup.parquet`。
- CARA 与 CubeSat 两个 historical reference draft 目录。

## 使用原则

1. `legacy_pr9_assets/` 是历史资产归档，不是当前正式 benchmark。
2. PR #9 的 selection 是 stress-test design，不是代表性随机抽样。
3. PR #9 的 expansion 可作为 NL/provenance 候选，但不能作为人工 oracle。
4. PR #9 的 ref draft 可作为 reference discipline / few-shot 经验，不能直接作为 final signed oracle。
5. 正式实验必须另建 frozen sample registry、eligibility filter、human adjudication protocol 和 run record。
