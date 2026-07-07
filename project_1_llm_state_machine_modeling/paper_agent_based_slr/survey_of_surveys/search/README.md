# search/：综述之综述检索记录

本目录记录 A1 阶段的种子检索、候选池和人工下载清单。A1 不是系统检索闭合阶段；任何种子候选都必须标注“未完成系统检索”。

> [!IMPORTANT]
> 本目录是 A1 历史检索与 dry-run 归档。PR-A2a 之后，活跃候选语料、主候选、替补、边界池、PDF 状态和人工下载清单的事实真源转到 [../corpus/](../corpus/)。本目录中的 `manual-download-needed.bib` 只保留 A1 历史 0 active 状态，不接收 A2a 新失败条目。

| 文件 | 作用 |
|---|---|
| [search-log.md](./search-log.md) | 查询、下载、失败和来源说明。 |
| [candidate-pool.md](./candidate-pool.md) | A1 候选池总表。 |
| [manual-download-needed.bib](./manual-download-needed.bib) | BibTeX 格式人工下载清单。 |

使用规则：

1. DOI / 官方 PDF / 作者主页优先。
2. 聚合页只能作为发现线索。
3. 如果下载到 HTML、登录页或错误页，必须删除伪 PDF 并记录失败。
4. 不得把 A1 种子检索写成完整系统检索。
