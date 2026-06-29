# patterns/：脚手架模式字段入口

本目录维护 `survey_of_surveys/` 的字段 schema 和后续 A2a/A2b 模式库入口。A1 阶段只冻结 dry-run 验证后的最小字段合同，不声称得到完整软件工程综述模式库。

| 文件 | 作用 |
|---|---|
| [pattern-field-schema.md](./pattern-field-schema.md) | 六类 pattern、字段定义、证据等级、缺失值语义和 schema 回修规则。 |

使用规则：

1. 单篇 `review.md` 必须使用本目录定义的六类 pattern 名称。
2. 新增字段必须记录证据要求和缺失值语义。
3. dry-run 暴露 schema 缺口时，先记录在单篇 review，再回修 schema，再回填 [../SUMMARY.md](../SUMMARY.md)。


## A1-M0--M6 元维度入口

从 #95 十篇现代锚点扩展开始，本目录不只维护六类 pattern，还维护 A1-M0--M6 元维度字段：研究意图与综述元模型、语料收集与纳排、研究对象与主题语义、方法 / 技术 / 干预、评价 / 证据 / 复现资产、统计分析就绪、research finding 形成与裁决。详见 [pattern-field-schema.md](./pattern-field-schema.md) §4.1。

这些字段用于指导 A2a/A2b 抽取初版模式库，不能在 A1 被写成最终 A3 schema。
