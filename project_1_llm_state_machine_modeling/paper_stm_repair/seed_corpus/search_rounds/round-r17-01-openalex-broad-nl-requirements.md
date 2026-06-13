# round-r17-01-openalex-broad-nl-requirements

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | OpenAlex |
| query / 入口 | `natural language requirements state machine generation` / `requirements statechart generation` / `use cases UML state machine` |
| raw evidence | `r17_openalex_nl_requirements_state_machine.jsonl; r17_openalex_requirements_statechart_generation.jsonl; r17_openalex_use_cases_uml_state_machine.jsonl; r17_openalex_usecase_statechart_more.jsonl` |
| 原始命中 / 尝试 | 95 raw hits across four dumps |
| 操作者 | main session + scout/review subagents |

## 处理结果

Broad OpenAlex query is high noise; entered `executable-use-cases-domain-machine-specifications`, `web-tool-goal-statechart-derivation`, `ucgen-usecase-descriptions` as R1.7 new/rejudged rows; most hits were model checking/process/testing surveys.

## 排除 / 噪声

`ucgen-usecase-descriptions` -> non-STM output; many NuSMV/UPPAAL/testing hits excluded as non-seed.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

OpenAlex broad query useful for negative evidence, not enough for SS-A; refined exact-title search required.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-01-openalex-broad-nl-requirements` |
| source | OpenAlex |
| query / query cluster | `natural language requirements state machine generation` / `requirements statechart generation` / `use cases UML state machine` |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 95 raw hits across four dumps |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | OpenAlex broad query useful for negative evidence, not enough for SS-A; refined exact-title search required. |
