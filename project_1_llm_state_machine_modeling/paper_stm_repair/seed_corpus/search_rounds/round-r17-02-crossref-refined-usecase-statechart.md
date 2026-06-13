# round-r17-02-crossref-refined-usecase-statechart

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | Crossref |
| query / 入口 | `use cases statecharts state machine generation requirements` + exact DOI/title variants |
| raw evidence | `r17_crossref_usecase_statechart_more.jsonl; r17_crossref_requirements_statechart_generation.jsonl` |
| 原始命中 / 尝试 | 50 raw hits |
| 操作者 | main session + scout/review subagents |

## 处理结果

Confirmed `unified-use-case-statecharts`; added `executable-use-cases-domain-machine-specifications`; re-found `statechart-use-case-validation-event-driven`; confirmed `synthesis-revisited-scenario-based` and `rscharter-statechart-elements` metadata.

## 排除 / 噪声

Several hits are books/standards or test-generation-only; `UCGen` outputs use case text, not STM.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

Crossref is strong for DOI discovery but cannot replace fulltext/artifact judgement.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-02-crossref-refined-usecase-statechart` |
| source | Crossref |
| query / query cluster | `use cases statecharts state machine generation requirements` + exact DOI/title variants |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 50 raw hits |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | Crossref is strong for DOI discovery but cannot replace fulltext/artifact judgement. |
