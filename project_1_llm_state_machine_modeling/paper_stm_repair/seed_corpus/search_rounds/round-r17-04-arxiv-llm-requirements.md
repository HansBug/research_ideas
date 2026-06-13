# round-r17-04-arxiv-llm-requirements

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | arXiv |
| query / 入口 | `LLM state machine requirements` / `state diagram requirements LLM` |
| raw evidence | `r17_arxiv_llm_state_machine_requirements.jsonl; r17_arxiv_state_diagram_requirements_llm.jsonl` |
| 原始命中 / 尝试 | 40 raw hits |
| 操作者 | main session + scout/review subagents |

## 处理结果

Mostly requirements-engineering LLM papers rather than STM output; no new SA-1/2 seed found. Existing recent LLM candidates remain `sefm`, `llms-emp`, `designing-fsm`, `unified-uml`, `fsm-bench`.

## 排除 / 噪声

LLM+requirements search has strong false positives: requirements quality, slicing, satisfiability/string checks, requirements generation.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

Use exact-title and artifact search for recent LLM seed; broad arXiv is negative evidence.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-04-arxiv-llm-requirements` |
| source | arXiv |
| query / query cluster | `LLM state machine requirements` / `state diagram requirements LLM` |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 40 raw hits |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../candidate_matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../papers/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../exclusion_ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../manual_download_queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | Use exact-title and artifact search for recent LLM seed; broad arXiv is negative evidence. |
