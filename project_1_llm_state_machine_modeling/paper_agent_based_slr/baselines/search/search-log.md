# PR-B0 baseline search log

## 1. arXiv query 记录

检索时间：`2026-06-13 01:20:00` 初筛，`2026-06-13 12:40:00` 补齐原始快照与去重候选池（Asia/Shanghai）。检索入口为 arXiv API，排序按 submittedDate descending；原始 query 快照见 [arxiv-query-raw-snapshot.jsonl](./arxiv-query-raw-snapshot.jsonl)，2024--2026 去重候选池见 [arxiv-dedup-candidate-pool.jsonl](./arxiv-dedup-candidate-pool.jsonl)。

| Query | 说明 | totalResults | fetched | 2024-2026 条目 |
|---|---|---:|---:|---:|
| `Q1` | LLM + systematic literature review | 107 | 107 | 102 |
| `Q2` | LLM + systematic review + screening/extraction/synthesis | 103 | 103 | 93 |
| `Q3` | agentic literature review + LLM | 66 | 66 | 64 |
| `Q4` | LLM + evidence synthesis | 42 | 42 | 41 |
| `Q5` | LLM + research synthesis + automation/workflow | 7 | 7 | 7 |
| `Q6` | automated literature review + LLM | 6 | 6 | 6 |
| `Q7` | survey 生成 + LLM | 23 | 23 | 20 |

复核汇总：query 原始快照 `raw_rows=354`；2024--2026 去重候选池 `dedup=291`；纳入 `34` 条，其中 `25` 条建立本地 PDF / `paper_content.txt` / `bibtex.bib` / `review.md` 文库。若后续 arXiv API 漂移，以本次 JSONL 快照作为 PR-B0 审计基线。

## 2. 操作日志

| 时间 | 动作 | 结果 | 风险 / 备注 |
|---|---|---|---|
| `2026-06-13 12:40:00` | 补齐实现后 review 指出的审计缺口 | 新增 arXiv 原始快照、去重候选池、CCF DBLP 原始扫描快照、ASE 排除理由表，并更新单篇逐维证据锚点 | 仍是粗筛，不替代 P0 全文细读；CCF 负证据仍须保守。 |
| `2026-06-13 02:55:00` | 复核 arXiv query 计数 | 7 组 query 的 2024--2026 去重并集约 291 条；粗筛纳入 34 条 | arXiv 持续更新，计数会漂移；正式论文写作前需刷新。 |
| `2026-06-13 02:40:00` | 同步第二批 arXiv 候选与本地文库 | arXiv 粗筛表扩展为 34 篇；本地 P0/P1 建库 25 篇；ARISE 升级为 P1 并纳入本地目录 | 仍属于 title / abstract 粗筛 + PDF 获取，不得写成最终全文结论。 |
| `2026-06-13 02:40:00` | 重写 README / GUIDE / SUMMARY | 固化 D1-D7、PDF / `paper_content.txt`、人工下载 BibTeX、CCF gap 与 story 风险规则 | 后续 Related Work 写作必须回到单篇 PDF / `paper_content.txt`。 |
| `2026-06-13 01:20:00` | arXiv API 按 PR body §4.1 query 骨架检索 | 形成 [arxiv-query-results.jsonl](./arxiv-query-results.jsonl) 与 [arxiv-2024-2026-title-abstract-screening.md](./arxiv-2024-2026-title-abstract-screening.md)；P0/P1 候选建立本地单篇目录 | arXiv 是预印本来源；需要后续核验是否已有正式 venue 版本。 |
| `2026-06-13 01:20:00` | 自动下载 P0/P1 arXiv PDF 并提取文本 | 候选目录包含 `paper.pdf` / `paper_content.txt` / `bibtex.bib` / `review.md` | `paper_content.txt` 为文字模式提取；若后续发现公式/表格缺失，应回到 PDF 核对。 |
| `2026-06-13 01:20:00` | CCF venue title-level 粗筛 | 形成 [ccf-venue-coverage-gaps.md](./ccf-venue-coverage-gaps.md) 与 [ccf-abc-2024-2026-title-abstract-screening.md](./ccf-abc-2024-2026-title-abstract-screening.md) | 多数 CCF 年度页缺 abstract；未命中不能写成最终负证据。 |
| `2026-06-13 01:20:00` | 人工下载清单 | 生成 [manual-download-needed.bib](./manual-download-needed.bib) | 原 ICSE workshop 相关命中已由用户 / Zotero 获取全文，人工下载清单清零。 |
