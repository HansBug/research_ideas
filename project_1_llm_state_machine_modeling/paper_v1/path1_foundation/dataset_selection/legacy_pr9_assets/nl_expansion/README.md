# nl_expansion/：PR #9 严格溯源 NL 扩充归档

本目录归档历史 PR #9 对 Top-15 / Backup-15 共 30 个样本所做的 natural-language expansion 资产。

## 文件说明

| 文件 / 目录 | 内容 |
|---|---|
| [EXPANSION_REPORT.md](./EXPANSION_REPORT.md) | 人类可读扩充报告，包含 30 条扩充 NL、provenance 和 axis coverage 摘要。 |
| [expansions.csv](./expansions.csv) | 30 条扩充结果的机器可读 CSV。 |
| [expansions/](./expansions/) | 30 个 JSON，每个包含 expanded NL、inline marker、provenance 与 axis coverage。 |
| [pool.tsv](./pool.tsv) / [selection.json](./selection.json) | 历史扩充任务 manifest。 |
| [briefs/](./briefs/) | 扩充前的 baseline NL style 与 pyfcstm grounding 调研摘要。 |
| [prompts/](./prompts/) | 历史扩充 prompt 模板。 |

## 使用原则

- 扩充 NL 可作为后续输入候选，但不能直接作为人工 oracle。
- 使用任何 expanded NL 前必须复核 provenance，确认每条事实均由原文支持。
- 如果后续模型输入需要去除 inline marker，应在正式 run record 中记录转换规则和输入 hash。
