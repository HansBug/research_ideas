# round-r17-07-classic-fulltext-wave

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | publisher/OA PDFs |
| query / 入口 | classic use-case / embedded / testing fulltext downloads |
| raw evidence | `single paper directories under `papers/`` |
| 原始命中 / 尝试 | 7 downloaded or already available fulltexts |
| 操作者 | main session + scout/review subagents |

## 处理结果

Added fulltext dirs: `nlp-req-formalization-testcase-generation`, `statistical-usage-testing-uml`, `unified-use-case-statecharts`, `statechart-codesign-usecases`, `object-models-uml-embedded`, `integrating-graphical-nl-specifications`, `specification-based-verification-usecase-sm`.

## 排除 / 噪声

All strict-like classic items are paper-only (`SA-3`); two are hard boundary negatives.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

Classic use-case literature strengthens related-work/negative evidence but does not increase R2 SA-1/2 count.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-07-classic-fulltext-wave` |
| source | publisher/OA PDFs |
| query / query cluster | classic use-case / embedded / testing fulltext downloads |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 7 downloaded or already available fulltexts |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | Classic use-case literature strengthens related-work/negative evidence but does not increase R2 SA-1/2 count. |
