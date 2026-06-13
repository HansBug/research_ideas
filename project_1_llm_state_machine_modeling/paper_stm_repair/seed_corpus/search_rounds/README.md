# search rounds

本目录保存 PR-R1.6 每轮检索的可复查事实源。`search_log.md` 只存总账，`search_rounds/` 负责每轮原始细节。

## 每轮最低字段

- `round_id`
- 日期 / 时间
- source
- query / query hash
- top-k / page cap
- 原始命中
- 去重后命中
- title / abstract 入账数
- fulltext / artifact 入账数
- 排除码分布
- pending / still-blocked
- noise pattern
- 下一步

## 命名约定

建议使用：

```text
round-001-<source>-<slug>.md
round-001-<source>-<slug>.jsonl
```

其中 `<slug>` 使用简短英文短横线，优先来自 query 意图或 source 名称。
