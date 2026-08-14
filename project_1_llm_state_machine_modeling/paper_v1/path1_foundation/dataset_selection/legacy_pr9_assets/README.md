# legacy_pr9_assets/：PR #9 历史资产归档

本目录从历史 Path-1 sprint PR [#9](https://github.com/HansBug/research_ideas/pull/9) 复制可复用资产，用作当前第一篇论文后续样本冻结、NL 输入构造、reference discipline 和实验设计的证据来源。

## 目录结构

| 路径 | 内容 | 当前用途 |
|---|---|---|
| [selection_screening/](./selection_screening/) | 323 条 sources T0+🟢 sample 的筛选输入、自动评审 JSON、Top-15 / Backup-15 报告与 summary。 | 样本池来源、stress-test 选择依据、候选样本追溯。 |
| [nl_expansion/](./nl_expansion/) | 30 条 candidate / backup 样本的严格溯源扩充 NL、provenance JSON、扩充报告和 prompt。 | 后续 frozen NL input / provenance packet 候选。 |
| [path1_parquet/](./path1_parquet/) | `sources_path1.parquet` 与 `sources_path1_backup.parquet`。 | 历史 sprint 数据文件；后续正式 registry 需重核。 |
| [reference_drafts/](./reference_drafts/) | CARA / CubeSat historical ref-STM draft、handover、codex draft、prompt 与辅助脚本。 | reference discipline、V-rich/V-poor case 经验和 few-shot 候选。 |

## 归档口径

- 本目录保留 PR #9 的历史事实，不表示这些资产已经通过当前论文的正式 oracle / benchmark gate。
- 所有进入论文主实验的样本、NL、reference model 和 annotation 都必须重新进入正式冻结协议。
- 若本目录内历史 README 或 report 提到旧路径、旧 guide 或旧 sprint 状态，应按“历史上下文”理解；当前入口以本文件和上级 [dataset_selection/README.md](../README.md) 为准。

## 校验入口

- 文件级清单：[../asset_manifest.tsv](../asset_manifest.tsv)
- 数量摘要：[../asset_summary.json](../asset_summary.json)
