# Experiment / Protocol Inventory

当前不是实验结果 PR，而是 #85 manuscript-start 前的 baseline / related-work / workspace foundation。没有真实 LLM run，也不需要四例 agent-loop 运行。

## Data needed before results

| 数据 | 交付物 | 用途 |
|---|---|---|
| Frozen corpus snapshot | `snapshot_manifest` / scripts | 复算 787/746 等统计 |
| Inclusion trace | `INCLUSION_TRACE.csv/jsonl` | retrospective protocol audit |
| Codebook and reliability | `CODEBOOK.md` / agreement log | 支撑分类统计 |
| Related-work verified matrix | P0/P1 fulltext notes | 防止 novelty overclaim |
| Sanitized task cards | benchmark-card pilot | 支撑 usefulness claim |
