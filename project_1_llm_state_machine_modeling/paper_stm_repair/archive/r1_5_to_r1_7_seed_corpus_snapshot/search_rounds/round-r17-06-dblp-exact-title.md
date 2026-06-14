# round-r17-06-dblp-exact-title

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | DBLP API |
| query / 入口 | 12 exact title queries from R1.6/R1.7 manual/classic candidates |
| raw evidence | `r17_dblp_exact_titles.jsonl` |
| 原始命中 / 尝试 | 12 attempted exact queries |
| 操作者 | main session + scout/review subagents |

## 处理结果

Confirmed DBLP metadata for `unified-use-case-statecharts`, `maritaca-use-case-behavior-models`, and `automated-transition-use-cases-uml-sm`; later queries hit 429/connection limits and were recorded.

## 排除 / 噪声

No fulltext/artifact from DBLP; failed exact queries do not imply nonexistence.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

DBLP is used as metadata corroboration, not evidence of seed eligibility.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-06-dblp-exact-title` |
| source | DBLP API |
| query / query cluster | 12 exact title queries from R1.6/R1.7 manual/classic candidates |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 12 attempted exact queries |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | DBLP is used as metadata corroboration, not evidence of seed eligibility. |
