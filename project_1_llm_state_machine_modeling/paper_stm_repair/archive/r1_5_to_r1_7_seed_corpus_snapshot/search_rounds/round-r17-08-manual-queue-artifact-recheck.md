# round-r17-08-manual-queue-artifact-recheck

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | publisher exact + artifact search |
| query / 入口 | R1.6 manual queue and R1.7 new manual candidates |
| raw evidence | `manual_download_queue.md; exclusion_ledger.md` |
| 原始命中 / 尝试 | 11 legacy + 2 new manual candidates checked |
| 操作者 | main session + scout/review subagents |

## 处理结果

Downloaded `towards-automatic-model-completion` from arXiv and excluded it as `X_REPAIR_ONLY`; kept 10 still-blocked legacy items; added two new manual pending items.

## 排除 / 噪声

Most legacy items remain paywalled or browser-only; artifact search found no public code/model package for classic closed candidates.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

Manual queue now has status distribution and PR-R2 impact; closed items are not blockers for R2 if not used.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-08-manual-queue-artifact-recheck` |
| source | publisher exact + artifact search |
| query / query cluster | R1.6 manual queue and R1.7 new manual candidates |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 11 legacy + 2 new manual candidates checked |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | Manual queue now has status distribution and PR-R2 impact; closed items are not blockers for R2 if not used. |
