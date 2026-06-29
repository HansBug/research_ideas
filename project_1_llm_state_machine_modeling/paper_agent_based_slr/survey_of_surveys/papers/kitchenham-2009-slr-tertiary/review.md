# Systematic literature reviews in software engineering – A systematic literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic literature reviews in software engineering – A systematic literature review |
| 年份 | 2009 |
| 类型 | tertiary-like SLR / SE SLR 状态综述 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 对 SE SLR 的三级/二级综述；文中自称 review of SLRs / tertiary study |
| SE 子领域 | EBSE / SE 二级研究方法学 |
| A1 角色 | 提供 RQ、搜索范围、纳排、质量评价、数据抽取、数据分析、limitations 都较清晰的 tertiary-study 样例。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 缺口 | 无硬缺口；但 quality score 数值需 PDF 图表级核对后才能进入正式统计。 |

## 2. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖活动规模、主题分布、研究者 / 机构、当前研究限制；属于“领域现状 + 局限”组合。 | `paper_content.txt` Page 2 lines around RQ1--RQ4。 | 可迁移到 Paper2 的 research finding：不仅统计数量，还问主题覆盖与限制。 | 早期 EBSE 样本，不能代表近年 SE/LLM4SE 综述 RQ 全貌。 |
| dimension pattern | 抽取范围包括 search venues、纳排标准、quality assessment、data collection、data analysis、deviation from protocol。 | `paper_content.txt` Page 1 contents；Page 2--3 Method。 | 可迁移为 survey-of-surveys review 表字段。 | 字段反映早期 SLR 生态，现代开放科学字段需 A2a 补充。 |
| finding pattern | 从数量、主题、组织、限制和实践影响形成 findings；结论指出主题覆盖有限、部分 SLR 可为实践提供指南。 | `paper_content.txt` Page 1 abstract；Page 7--8 discussion/conclusion。 | 可迁移为“统计观察 → 研究发现”的桥接模板。 | 只作为“统计到发现”的模板，不能迁移具体领域结论。 |
| evidence presentation pattern | 用 manual search 分母、search results、quality evaluation、quality factors 支撑结论。 | `paper_content.txt` Page 1 abstract；Page 3--5 results。 | 可迁移为字段证据与统计表结构。 | 质量评价和搜索分母可迁移，具体指标需现代样本校准。 |
| validity / threat pattern | 单列 limitations of study，包含搜索范围、术语历史和 protocol deviation。 | `paper_content.txt` Page 1 contents；Page 7 limitations。 | 可迁移到 Paper2 的效度威胁章节。 | 早期 threat 口径可能不足以覆盖 LLM 辅助综述风险。 |
| report structure pattern | 标准结构：Introduction → Method → Results → Discussion → Conclusions，并将每个 RQ 映射到 discussion 小节。 | `paper_content.txt` Page 1 contents。 | 高度可迁移。 | 结构可参考，但后续必须加入人机协同与审计制品链部分。 |

## 3. 对 PR-A1 schema 的启发

1. `RQ pattern` 应允许“规模 / 主题 / 主体 / 局限”四类组合，不只允许 PICO 式技术效果问题。
2. `finding pattern` 需要区分统计观察和可行动结论，例如“SLR 数量增加”与“需要更好实践指导”。
3. `evidence presentation pattern` 应要求每个 finding 对应搜索范围、筛选分母、质量评价或 data extraction 字段。
4. `validity pattern` 需要记录 protocol deviation，而不是只列外部效度。

## 4. 待复核

- Table / quality score 数值正式使用前需回 PDF 核对。
- 该文是早期 SE tertiary study；A2a/A2b 需要补近年样本，避免 pattern 过拟合早期 EBSE。
