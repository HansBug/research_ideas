# Machine Learning for Software Engineering: A Tertiary Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Machine Learning for Software Engineering: A Tertiary Study |
| 年份 | 2023 |
| 类型 | tertiary study |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [CSUR](https://dl.acm.org/journal/csur) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| 来源等级 | 高等级综述期刊；ACM Computing Surveys；arXiv 开放 PDF；CCF 官方等级不填写 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | tertiary study；汇总 83 篇 reviews 与 6117 篇 primary studies |
| SE 子领域 | ML4SE；覆盖软件生命周期多个活动 |
| A1 角色 | 现代高等级 tertiary study 样本，用于压测大规模二次研究汇总、分类体系、research challenges 与 action recommendations。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 缺口 | 暴露“挑战 / 行动建议”类 finding pattern；已在 SUMMARY 中作为 A2a 重点候选。 |

## 2. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 原文以 ML for SE 的覆盖、分类、质量评估与研究挑战组织三级研究；摘要直接说明 systematically collected、quality-assessed、summarized、categorized 83 reviews。 | `paper_content.txt` Page 1 摘要。 | 可迁移为“覆盖 + 分类 + 质量 + 挑战 / 行动”组合。 | ML4SE 的覆盖/挑战 RQ 可迁移为样式，不迁移具体领域问题。 |
| dimension pattern | 维度包括 SE 生命周期活动、ML 技术、review 质量、primary study 数量、研究挑战和建议行动。 | `paper_content.txt` Page 1 摘要；全文目录与分类章节待 PDF 表格核对。 | 高度可迁移，但字段树较大，A2a 需细分。 | 字段树较大，A2a 需要拆分并验证取值空间。 |
| finding pattern | 发现不仅是分布统计，还提出 ML4SE research challenges/actions，如更多实证验证、工业研究、数据/管线文档化、增量 ML。 | `paper_content.txt` Page 1 摘要。 | 可迁移为 Paper2 的 candidate finding heuristic：统计观察之后要形成行动建议。 | 挑战/行动建议是启发式，不代表目标主题最终 finding。 |
| evidence presentation pattern | 使用 83 reviews / 6117 primary studies 的分母、质量评估、分类表和挑战列表。 | `paper_content.txt` Page 1 摘要；表格待 PDF 核对。 | 可迁移为大规模总账和 pattern-to-source anchor。 | 83 reviews/6117 primary studies 的数值需 PDF 表格核对后才能引用。 |
| validity / threat pattern | 本轮只读题摘和全文开头，threats 章节待进一步定位；当前不能写成已完整核验。 | `paper_content.txt` 全文待 A2a 深读。 | 作为待核验字段，不能强写。 | 本轮未完整定位 threat 章节，不能强写完整核验。 |
| report structure pattern | CSUR 综述结构，含 introduction、method、classification/results、discussion/challenges；具体章节待 A2a 深读。 | `paper_content.txt` 目录提取不完整；需 PDF 目录核对。 | 候选可迁移。 | CSUR 长综述结构适合参考，但 paper2 仍需突出方法贡献。 |

## 3. 对 PR-A1 schema 的启发

1. 新增 `challenge_action_pattern` 作为 `finding_pattern` 的子类型：从统计分布转为研究挑战和行动建议。
2. 大型 tertiary study 需要 `secondary_count`、`primary_count`、`classification_axis` 等字段。
3. 高等级现代样本会暴露 A1 早期 EBSE 文献过旧的问题，A2a 应优先扩展 2020 年后的 SE tertiary/survey。

## 4. 待复核

- 需进一步定位 RQ、threats、classification 表和 challenge 表的页码。
- DOI/最终出版页已记录；正式写作前应核对 ACM 版与 arXiv 版差异。
