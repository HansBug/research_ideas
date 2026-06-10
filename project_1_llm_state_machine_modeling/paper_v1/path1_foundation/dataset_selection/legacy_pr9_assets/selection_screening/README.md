# selection_screening/：PR #9 sources 样本筛选归档

本目录归档历史 PR #9 中对 `sources/` T0+🟢 样本池进行自动筛选的详细数据与结果。

## 文件说明

| 文件 / 目录 | 内容 |
|---|---|
| [SELECTION_REPORT.md](./SELECTION_REPORT.md) | 人类可读筛选报告，包含评分图例、统计、Top-15、Backup-15 和全量评审表。 |
| [summary.csv](./summary.csv) | 机器可读全量评分 CSV。 |
| [candidates.jsonl](./candidates.jsonl) | 323 条候选 sample 元数据。 |
| [reviews/](./reviews/) | 323 个 Codex 自动评审 JSON。 |
| [domain_emoji.json](./domain_emoji.json) | 历史领域 emoji 映射。 |

## 使用原则

1. 这里的数据是历史 stress-test selection，不是当前正式 benchmark。
2. Top-15 / Backup-15 可作为候选样本和选样依据，但必须在正式 sample registry 中重新确认 eligibility。
3. 323 个 review JSON 可以追溯自动评分理由；不能单独作为 paper result 或 human oracle。
4. 若报告中出现旧路径或旧 sprint 术语，以历史语境理解；当前论文入口回到 [../../README.md](../../README.md)。
