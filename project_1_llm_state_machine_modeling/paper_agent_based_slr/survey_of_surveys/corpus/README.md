# A2a 综述语料候选库

本目录是 Paper2 PR-A2a 的集中语料入口，用于把近年软件工程综述候选整理成后续 A2b 可全文深读的候选框。它不是最终综述结论，也不是 A2b 的全文 `review.md` / `evidence_chain.md` 完成证据。

## 当前速读

| 项 | 当前数量 | 入口 |
|---|---:|---|
| 全量候选账本 | 438 | [tables/full-candidate-ledger.csv](./tables/full-candidate-ledger.csv) |
| 系统化候选池 | 293 | [tables/systematic-candidates.csv](./tables/systematic-candidates.csv) |
| 主候选语料 | 120 | [tables/core-corpus.csv](./tables/core-corpus.csv) |
| 替补 / 留出语料 | 40 | [tables/reserve-corpus.csv](./tables/reserve-corpus.csv) |
| 边界 / 方法启发池 | 145 | [tables/boundary-pool.csv](./tables/boundary-pool.csv) |
| PDF 状态记录 | 305 | [tables/pdf-status.csv](./tables/pdf-status.csv) |
| 已取得 PDF / 文本 | 70 | [tables/pdf-status.csv](./tables/pdf-status.csv) |
| 需人工下载 | 90 | [manual-download-needed.md](./manual-download-needed.md)、[manual-download-needed.bib](./manual-download-needed.bib) |

当前 PDF 状态：core + reserve 中 70 篇已有本地 PDF / 文本，其中 13 篇继承 A1 精核资产，2 篇由 A2a 自动从开放 PDF 链接获取，55 篇由用户本地 Zotero 导出显式复制入仓库；仍有 90 篇保留在人工下载清单中。PDF 可得性不改变候选资格，只改变执行状态。`PDF 状态记录 = 305` 指 core 120 + reserve 40 + boundary 145 三层状态记录之和，其中 boundary 145 均为 `not_applicable`。

## 文件说明

| 文件 / 目录 | 作用 |
|---|---|
| [selection.md](./selection.md) | 说明 L0→L4 的纳排、去重、主候选、替补和边界池规则。 |
| [source-audit.md](./source-audit.md) | 记录原始候选来源、快照时间、字段口径和不确定性。 |
| [pdf-acquisition.md](./pdf-acquisition.md) | 记录 PDF 自动获取策略、当前结果、失败类型和人工下载优先级。 |
| [handoff-to-next-stage.md](./handoff-to-next-stage.md) | 给 A2b 的交接说明：哪些可深读、哪些待下载、哪些不得直接用于 schema 冻结。 |
| [tables/](./tables/) | 可复算 CSV 表，供脚本和 reviewer 使用。 |
| [raw/](./raw/) | 原始候选快照、主候选选择种子与 Zotero PDF 导入审计清单；除换行符、行尾空白和显式人工导入记录外，不人工改候选字段语义。 |

## 使用顺序

1. 先读本文件理解 A2a 当前语料建设状态。
2. 再读 [selection.md](./selection.md) 确认候选资格与分层规则。
3. 如需核查来源，读 [source-audit.md](./source-audit.md) 和 [raw/](./raw/)。
4. 如需补全文，读 [pdf-acquisition.md](./pdf-acquisition.md) 与 [manual-download-needed.bib](./manual-download-needed.bib)。
5. A2b 开始前必须读 [handoff-to-next-stage.md](./handoff-to-next-stage.md)。

## 禁止误读

- 不得把 `core-corpus.csv` 里的 120 篇写成已经全文深读完成。
- 不得把 `manual-download-needed.bib` 里的失败条目当作排除条目。
- 不得在 A2a 阶段从这些候选直接写最终 research finding。
- 不得用本目录替代 A2b 的逐篇 `review.md`、`evidence_chain.md` 和 claim map。
