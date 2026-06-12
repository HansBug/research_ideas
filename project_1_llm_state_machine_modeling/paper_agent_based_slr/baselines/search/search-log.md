# PR-B0 baseline search log

## 1. arXiv query 记录

检索时间：`2026-06-13 01:20:00` 初筛，`2026-06-13 02:55:00` 复核 query 计数（Asia/Shanghai）。检索入口为 arXiv API，排序按 submittedDate descending；原始纳入候选见 [arxiv-query-results.jsonl](./arxiv-query-results.jsonl)。本表中的返回数是 API 复核时的可复现近似值，后续 arXiv 新增论文可能导致漂移。

| Query | totalResults | fetched | 2024-2026 条目 | 2024-2026 去重 |
|---|---:|---:|---:|---:|
| `all:"systematic literature review" AND (all:"large language model" OR all:LLM OR all:ChatGPT)` | 107 | 107 | 102 | 102 |
| `all:"systematic review" AND (all:LLM OR all:"large language model") AND (all:screening OR all:extraction OR all:synthesis)` | 103 | 103 | 93 | 93 |
| `all:"literature review" AND (all:agent OR all:agentic OR all:autonomous) AND (all:LLM OR all:"large language model")` | 66 | 66 | 64 | 64 |
| `all:"evidence synthesis" AND (all:LLM OR all:"large language model" OR all:ChatGPT)` | 42 | 42 | 41 | 41 |
| `all:"research synthesis" AND (all:LLM OR all:"large language model") AND (all:automation OR all:workflow)` | 7 | 7 | 7 | 7 |
| `all:"automated literature review" AND (all:LLM OR all:"large language model")` | 6 | 6 | 6 | 6 |
| `all:"survey generation" AND (all:LLM OR all:"large language model")` | 23 | 23 | 20 | 20 |

复核汇总：上述 query 的 2024--2026 去重并集约 `291` 条；PR-B0 按 D1-D7 title / abstract 粗筛保留 `34` 条，其中 `25` 条建立本地 PDF / `paper_content.txt` / `bibtex.bib` / `review.md` 文库，`9` 条暂作 P2 背景保留。

## 2. 操作日志

| 时间 | 动作 | 结果 | 风险 / 备注 |
|---|---|---|---|
| `2026-06-13 02:55:00` | 复核 arXiv query 计数 | 7 组 query 的 2024--2026 去重并集约 291 条；粗筛纳入 34 条 | arXiv 持续更新，计数会漂移；正式论文写作前需刷新。 |
| `2026-06-13 02:40:00` | 同步第二批 arXiv 候选与本地文库 | arXiv 粗筛表扩展为 34 篇；本地 P0/P1 建库 25 篇；ARISE 升级为 P1 并纳入本地目录 | 仍属于 title / abstract 粗筛 + PDF 获取，不得写成最终全文结论。 |
| `2026-06-13 02:40:00` | 重写 README / GUIDE / SUMMARY | 固化 D1-D7、PDF / `paper_content.txt`、人工下载 BibTeX、CCF gap 与 story 风险规则 | 后续 Related Work 写作必须回到单篇 PDF / `paper_content.txt`。 |
| `2026-06-13 01:20:00` | arXiv API 按 PR body §4.1 query 骨架检索 | 形成 [arxiv-query-results.jsonl](./arxiv-query-results.jsonl) 与 [arxiv-2024-2026-title-abstract-screening.md](./arxiv-2024-2026-title-abstract-screening.md)；P0/P1 候选建立本地单篇目录 | arXiv 是预印本来源；需要后续核验是否已有正式 venue 版本。 |
| `2026-06-13 01:20:00` | 自动下载 P0/P1 arXiv PDF 并提取文本 | 候选目录包含 `paper.pdf` / `paper_content.txt` / `bibtex.bib` / `review.md` | `paper_content.txt` 为文字模式提取；若后续发现公式/表格缺失，应回到 PDF 核对。 |
| `2026-06-13 01:20:00` | CCF venue title-level 粗筛 | 形成 [ccf-venue-coverage-gaps.md](./ccf-venue-coverage-gaps.md) 与 [ccf-abc-2024-2026-title-abstract-screening.md](./ccf-abc-2024-2026-title-abstract-screening.md) | 多数 CCF 年度页缺 abstract；未命中不能写成最终负证据。 |
| `2026-06-13 01:20:00` | 人工下载清单 | 生成 [manual-download-needed.bib](./manual-download-needed.bib) | 至少包含 ICSE workshop 相关命中，待用户 / Zotero 获取全文。 |
