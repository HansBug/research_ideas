# round-r17-03-crossref-textual-usecase-behavior

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | Crossref |
| query / 入口 | `textual use case descriptions behavior models state machine` |
| raw evidence | `r17_crossref_textual_usecase_behavior.jsonl` |
| 原始命中 / 尝试 | 30 raw hits |
| 操作者 | main session + scout/review subagents |

## 处理结果

Reconfirmed `maritaca-use-case-behavior-models`; found `UCGen` as negative sentinel; did not locate open artifact for MARITACA.

## 排除 / 噪声

Many hits are use-case description generation or quality analysis, not state-machine output.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

MARITACA remains high-priority manual queue; UCGen proves adjacent LLM work may be output-not-STM.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-03-crossref-textual-usecase-behavior` |
| source | Crossref |
| query / query cluster | `textual use case descriptions behavior models state machine` |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 30 raw hits |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | MARITACA remains high-priority manual queue; UCGen proves adjacent LLM work may be output-not-STM. |
