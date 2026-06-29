# Systematic Reviews in Requirements Engineering: A Tertiary Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic Reviews in Requirements Engineering: A Tertiary Study |
| 年份 | 2014 |
| 类型 | tertiary study |
| 出版形态 | 工作坊 |
| 期刊/会议/预印本 | [EmpiRE](https://empire2014.wordpress.com/) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| CCF 复核状态 | -- |
| 来源等级 | EmpiRE 2014 workshop；非顶级会议；IEEE DOI |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | Requirements Engineering 领域 tertiary study |
| SE 子领域 | Requirements Engineering |
| A1 角色 | 领域专门化 tertiary study 样本，用于验证“特定 SE 子领域如何定义 topic / quality / impact / practitioners”。 |
| 是否目标证据池 | 否。 |
| schema 缺口 | 暴露“领域专门化”字段：目标 SE 子领域、topic taxonomy、教育/实践影响。 |

## 2. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 目标是给出 RE 领域 SLR 的 comprehensive overview，并评估 quality、topics、impact for education/practice。 | `paper_content.txt` Page 2 摘要。 | 可迁移为“特定 SE 子领域的综述元模型”。 | RE 子领域样本，不能直接代表 testing/MDE/LLM4SE 等主题。 |
| dimension pattern | 维度包括 automated/manual search、53 distinct reviews、64 publications、quality、topics、education/practice relevance。 | `paper_content.txt` Page 2 摘要与方法段。 | 可迁移到 A2a 的领域专门字段。 | 教育/实践影响字段可参考，但字段树需由目标主题研究者裁定。 |
| finding pattern | finding 关注 RE SLR 数量、主题与质量；具体结论需进一步深读结果章节。 | `paper_content.txt` Page 2 摘要。 | 候选可迁移。 | 当前只读摘要级结果，具体 finding 需 A2a 深读结果章节。 |
| evidence presentation pattern | 使用 distinct reviews / publications 分母、自动与手工搜索来源、质量评估结果。 | `paper_content.txt` Page 2 摘要。 | 可迁移为候选池和去重字段。 | distinct reviews/publications 分母可迁移，细节需 PDF 表格核对。 |
| validity / threat pattern | 本轮未完整定位 threat section；需 A2a 深读。 | `paper_content.txt` Page 2--9。 | 待核验。 | threat section 未完整定位，不能作为已饱和 threat 模板。 |
| report structure pattern | 短 workshop tertiary study，结构紧凑；适合压测短文档字段缺失情况。 | `paper_content.txt` Page 1--9。 | 可迁移为“短论文也要记录缺失字段”。 | 短 workshop 结构紧凑，不能当成完整期刊综述结构。 |

## 3. 对 PR-A1 schema 的启发

1. `target_se_subfield` 应成为候选字段，避免把所有 SE SLR 混为一个领域。
2. `publication_count` 与 `distinct_study_count` 应分开，避免多篇报告同一 SLR 造成重复。
3. 需要 `education_practice_relevance` 字段，承接导师强调的 research finding / practical impact。

## 4. 待复核

- PDF 表格与质量评价细节待人工核对。
- EmpiRE 是 workshop，不能写成顶级 venue。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 将 Requirements Engineering 二次研究作为 tertiary study 对象。 | 可迁移“SE 子领域 tertiary”元模型。 |
| A1-M1 语料收集与纳排 | 提供 RE 三级研究的搜索与选择流程。 | EmpiRE workshop 来源需标注非顶级 venue。 |
| A1-M2 研究对象与主题语义 | 提供 RE 子领域 topic / evidence 分类样本。 | 可作为 RE 子领域 schema seed。 |
| A1-M3 方法 / 技术 / 干预 | 主要关注 RE review 类型和主题，不是具体技术干预。 | 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 可迁移 quality / reporting / evidence-presentation 字段。 | 表格需后续核对。 |
| A1-M5 统计分析就绪 | 可形成 RE secondary studies 的分布统计。 | 小样本与 workshop 语境需降级。 |
| A1-M6 research finding 形成与裁决 | 可从 RE review 覆盖缺口形成候选 finding。 | 不支撑 Paper2 目标领域结论。 |
