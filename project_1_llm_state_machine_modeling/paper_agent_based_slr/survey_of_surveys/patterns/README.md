# patterns/：脚手架模式字段入口

本目录维护 `survey_of_surveys/` 的字段 schema 和后续 A2a/A2b 模式库入口。A1 阶段只冻结 dry-run 验证后的最小字段合同，不声称得到完整软件工程综述模式库。

| 文件 | 作用 |
|---|---|
| [pattern-field-schema.md](./pattern-field-schema.md) | 六类 pattern、字段定义、证据等级、缺失值语义和 schema 回修规则。 |

使用规则：

1. 单篇 `review.md` 必须使用本目录定义的六类 pattern 名称。
2. 新增字段必须记录证据要求和缺失值语义。
3. dry-run 暴露 schema 缺口时，先记录在单篇 review，再回修 schema，再回填 [../SUMMARY.md](../SUMMARY.md)。
