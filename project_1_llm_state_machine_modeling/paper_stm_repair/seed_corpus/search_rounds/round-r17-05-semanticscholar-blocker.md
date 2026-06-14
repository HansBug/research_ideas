# round-r17-05-semanticscholar-blocker

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | Semantic Scholar API |
| query / 入口 | six query clusters required by PR body |
| raw evidence | `r17_semanticscholar_*.jsonl` |
| 原始命中 / 尝试 | 6 API attempts |
| 操作者 | main session + scout/review subagents |

## 处理结果

All attempts returned HTTP 429 Too Many Requests; raw error JSONL retained. Coverage degraded to Crossref/OpenAlex/arXiv/DBLP/web exact-title.

## 排除 / 噪声

N/A; blocker round.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

Source blocker recorded; PR-R2 risk low because OpenAlex + Crossref + arXiv + exact DOI covered same discovery space this round.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-05-semanticscholar-blocker` |
| source | Semantic Scholar API |
| query / query cluster | six query clusters required by PR body |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 6 API attempts |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | Source blocker recorded; PR-R2 risk low because OpenAlex + Crossref + arXiv + exact DOI covered same discovery space this round. |
