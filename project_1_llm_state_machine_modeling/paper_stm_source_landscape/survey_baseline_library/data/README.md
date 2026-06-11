# 全文级 baseline 数据

本目录保存机器可审计的全文级 baseline 数据。每篇论文的原始 PDF 与抽取文本放在相应单论文目录中；本目录只保存跨论文矩阵和 receipt。

| 文件 | 行数 | 职责 |
|---|---:|---|
| [fulltext_review_matrix.csv](./fulltext_review_matrix.csv) | 25 | P0/P1 全文初检主矩阵，含 D1--D7 全文级评分、方法学 checklist、最终关系、claim impact、单篇文件相对路径 |
| [local_fulltext_receipt.csv](./local_fulltext_receipt.csv) | 25 | 本地导出 PDF 到仓库单篇目录的 receipt，记录 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md` 路径、短哈希、页数和抽取状态 |

更新时间：`2026-06-12 00:10:00`。
