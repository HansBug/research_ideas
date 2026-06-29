# Six years of systematic literature reviews in software engineering: An updated tertiary study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Six years of systematic literature reviews in software engineering: An updated tertiary study |
| 年份 | 2011 |
| 类型 | updated tertiary study |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 更新型三级研究；整合前两项 tertiary study 并扩展时间窗口。 |
| SE 子领域 | EBSE / SE 二级研究方法学 |
| A1 角色 | 提供“扩展旧 tertiary study + 自动/人工搜索 + 质量/覆盖/影响分析”的更新型模式。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 缺口 | 暴露“更新型 tertiary study”需要记录与先前研究的合并/对比字段；已在 schema 中加入 `前序综述关系` 候选字段。 |

## 2. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖新时间段数量、主题、活跃作者/机构、旧研究限制是否仍存在、质量是否提升。 | `paper_content.txt` Page 1 abstract；Page 2--3 Method / RQ。 | 可迁移为“增量更新型 survey-of-surveys”模式。 | 更新型 RQ 适合 longitudinal review，不适合所有单次 SLR。 |
| dimension pattern | 维度包括搜索策略、study selection、quality assessment、data extraction、研究主题、教育 / 实践影响。 | `paper_content.txt` Page 1 contents；Page 3--5 Method / Data extraction。 | 可迁移到 A2a 的字段树。 | 教育/实践影响字段有价值，但不能替代目标主题维度。 |
| finding pattern | 发现包括 SLR 数量增长、主题覆盖扩大、质量提升、但多数未评价 primary study 质量且缺实践指南。 | `paper_content.txt` Page 1 abstract。 | 可迁移为“增长 + 质量 + 影响缺口”的 finding pattern。 | 具体增长和质量结论只属于当年 SE SLR 生态。 |
| evidence presentation pattern | 用 67 个新 SLR、24 个 SE topics、quality assessment、curriculum / practitioner relevance 支撑结论。 | `paper_content.txt` Page 1 abstract；Page 6--10 results/discussion。 | 可迁移为统计表 + 解释性结论。 | 分母与统计方式可迁移，具体数值不可迁移。 |
| validity / threat pattern | 关注搜索过程、前序研究合并、quality assessment 口径和对教育 / 实践影响的解释。 | `paper_content.txt` Page 3--5 Method。 | 可迁移到更新型 review 的 threat 模式。 | 更新型合并风险可参考，但需补现代检索库和开放科学风险。 |
| report structure pattern | Previous studies → Method → Data extraction results → Discussion of RQs → Conclusions。 | `paper_content.txt` Page 1 contents。 | 可迁移，尤其适合 A2b 对旧 / 新样本分层。 | 适合 update/integrate 型综述，非更新型主题需调整。 |

## 3. 对 PR-A1 schema 的启发

1. 新增 `前序综述关系` 字段：是否扩展、复现、整合或更新已有 tertiary study。
2. 新增 `实践 / 教育影响字段`：不能只统计主题，还要问研究发现是否转化为实践/教育建议。
3. 对 finding 必须保留“仍然不足”的负向发现模式，避免只总结增长。
4. 对更新型综述，需记录时间窗和与旧窗口的合并策略。

## 4. 待复核

- 正式引用质量/数量表前需 PDF 表格核对。
- 后续 A2a/A2b 需要补近十年 SE SLR/SMS/survey，以避免 A1 仅受早期 EBSE 文献影响。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | updated tertiary study 展示如何定义“更新 / 扩展 / 整合前序综述”。 | 可迁移 predecessor_relation 字段。 |
| A1-M1 语料收集与纳排 | 展示沿用和扩展前序检索边界的方式。 | 可迁移 update protocol 字段；具体语料年代需降级。 |
| A1-M2 研究对象与主题语义 | 继续组织 SE SLR topic、质量与报告维度。 | 可作为历史对比字段，不支撑现代结论。 |
| A1-M3 方法 / 技术 / 干预 | 主要贡献是二次研究更新方法，不是技术 taxonomy。 | 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 体现质量评价、报告质量和前序研究对齐。 | 可迁移到“复用前序证据时如何记录差异”。 |
| A1-M5 统计分析就绪 | 可形成跨年份 update / trend / quality 分布。 | 必须标注年份窗口。 |
| A1-M6 research finding 形成与裁决 | 从 update 对比中生成方法学 gap 和改进建议。 | 可迁移为“前序差异 -> 新 finding”的启发式。 |
