# Round 3 主线程裁决与回填记录

## 1. 裁决范围

本文件记录 `survey_of_surveys/` 在 PR-A1 中针对 S1--S8 与原生维度树 / 维度森林的第三轮独立审计裁决。Round 3 的执行纪律是：**一篇论文一个 subagent**，每个 subagent 只处理自己负责的一篇论文，输出到本目录同名 `*.md` 文件；主线程统一裁决、压缩和回填到单篇 `review.md`、必要的 `evidence_chain.md`、[SUMMARY.md](../../../SUMMARY.md) 与 [GUIDE.md](../../../GUIDE.md)。

本轮不把任何 A1 文本级结果升级为 Paper2 final quantitative finding；所有 `强 / 中 / 弱` 只表示二级综述 schema 的可用度。A2a 完成页码、表图、supplementary、Zenodo / replication package 与 publisher final 精核前，任何候选统计都只能作为 `schema_seed` 或 `boundary_anchor` 使用。

## 2. 19/19 独立审计完成表

| 论文 | round3 审计 | subagent 状态 | 主线程裁决 | 回填状态 |
|---|---|---|---|---|
| ai-native-se-roadmap | [ai-native-se-roadmap.md](./ai-native-se-roadmap.md) | completed | 采纳：roadmap 降级、S4/S6 边界、非最终定量声明 | 已回填 review / SUMMARY 口径 |
| app-reviews-slr-se | [app-reviews-slr-se.md](./app-reviews-slr-se.md) | completed | 采纳：方法池 / 目标领域证据池拆分、A2a 前不最终统计 | 已回填 review |
| da-silva-2011-six-years-slr | [da-silva-2011-six-years-slr.md](./da-silva-2011-six-years-slr.md) | completed | 采纳：后续主统计池候选、Practitioner Guidelines 回归、A1/A2a 边界 | 已回填 review / SUMMARY 口径 |
| devsecops-primary-dimensions | [devsecops-primary-dimensions.md](./devsecops-primary-dimensions.md) | completed | 采纳：文本级强与 `not_verified` 不冲突、主 MLR / confirmatory / prior-review supplement 分母隔离 | 已回填 review / evidence_chain |
| formal-re-llm-roadmap | [formal-re-llm-roadmap.md](./formal-re-llm-roadmap.md) | completed | 采纳：Roadmap topic/item 与 Action Point statement 分层、roadmap 不进主统计池 | 已回填 review / evidence_chain |
| interactive-llm-systematic-mapping | [interactive-llm-systematic-mapping.md](./interactive-llm-systematic-mapping.md) | completed | 采纳：proposal 降级、原文字段与 Paper2 增强字段拆分、Fig.1 核验状态统一 | 已回填 review |
| kitchenham-2009-slr-tertiary | [kitchenham-2009-slr-tertiary.md](./kitchenham-2009-slr-tertiary.md) | completed | 采纳：tertiary SLR / SE SLR 状态综述、20 篇 SLR 主树与 DARE / 检索漏斗辅助树分层 | 已回填 review / SUMMARY |
| kitchenham-charters-2007-slr-guidelines | [kitchenham-charters-2007-slr-guidelines.md](./kitchenham-charters-2007-slr-guidelines.md) | completed | 采纳：guideline 方法参考池、Appendix 2/3 只作边界样本 | 已回填 review |
| llm-assistants-developer-productivity | [llm-assistants-developer-productivity.md](./llm-assistants-developer-productivity.md) | completed | 采纳：2025-Jan 异常、NASA-TLX / cognitive-load 子集待拆、文本级 schema_seed | 已回填 review |
| llm4se-systematic-review | [llm4se-systematic-review.md](./llm4se-systematic-review.md) | completed | 采纳：分母冲突显式待核、Table 8/10 分母语义区分、主统计池候选而非最终统计 | 已回填 review |
| mde-ml-components-slr | [mde-ml-components-slr.md](./mde-ml-components-slr.md) | completed | 采纳：RQ 是结果视角 / 字段分支，Fig.5 主 feature tree 与 gate/rubric 并列 | 已回填 review |
| mdse-modelling-assistants-mapping | [mdse-modelling-assistants-mapping.md](./mdse-modelling-assistants-mapping.md) | completed | 采纳：文献侧 / 实践侧双样本单位、limitation 子类冲突待 A2a | 已回填 review |
| ml4se-tertiary-study | [ml4se-tertiary-study.md](./ml4se-tertiary-study.md) | completed | 采纳：83 reviews / 6,117 非唯一 primary 覆盖计数、SWEBOK 与开放编码分层 | 已回填 review |
| petersen-2008-systematic-mapping | [petersen-2008-systematic-mapping.md](./petersen-2008-systematic-mapping.md) | completed | 采纳：SMS 方法学种子，Tree A/B/C/D 分层，Figure 3 / 中位数口径修正 | 已回填 review |
| petersen-2015-mapping-guidelines-update | [petersen-2015-mapping-guidelines-update.md](./petersen-2015-mapping-guidelines-update.md) | completed | 采纳：52 final mapping studies、Table 3 11 data items、五元 facet 与三元最终推荐拆分 | 已回填 review |
| re-agile-sms-2015 | [re-agile-sms-2015.md](./re-agile-sms-2015.md) | completed | 采纳：problem→solution 是 prose 本地复原关系边，不是原文 formal relation table | 已回填 review / evidence_chain |
| re-tertiary-study-2014 | [re-tertiary-study-2014.md](./re-tertiary-study-2014.md) | completed | 采纳：64 publications / 53 distinct SLR / QA 51 分母拆分，future researcher relevance 边界 | 已回填 review / SUMMARY |
| requirements-quality-theory-roadmap | [requirements-quality-theory-roadmap.md](./requirements-quality-theory-roadmap.md) | completed | 采纳：VIEW POINT / commentary 降级、57 篇 convenience sample、A2a 待精核替代旧“缺失”段 | 已回填 review |
| research-artifacts-secondary-studies | [research-artifacts-secondary-studies.md](./research-artifacts-secondary-studies.md) | completed | 采纳：logistic regression 移出 S3 原生树、16 ISSN token / 15 期刊、availability 四类状态、Zenodo 未核 | 已回填 review / evidence_chain / SUMMARY 口径 |

## 3. 主线程统一裁决

1. **Round 3 产物完整**：19 篇单篇审计均已写入 [./](./)，[TASKS.tsv](./TASKS.tsv) 状态均为 `completed`。
2. **单篇 `review.md` 已回填**：19 篇均保留 `## survey_of_surveys 自身 schema 抽取` 与 `### S1--S8 四分栏证据拆分`，并显式声明 A1 文本级结果不得作为 final quantitative finding。
3. **证据链边界已收紧**：已重点修正会污染证据链的残留，包括 roadmap action 分母、logistic regression 是否属于原生树、problem→solution 是否为 formal schema、统计池候选与最终统计的区别。
4. **SUMMARY 已接入 round3**：总账新增 Round 3 状态说明，后续以本文件和单篇 `review.md` 为 A1 当前事实入口；早期 `results/` / `adjudications/` 保留为历史审计来源。
5. **A2a 接力项仍存在**：本轮不追求所有 PDF 页码、表图、supplementary、Zenodo / replication package 的 final evidence；这些必须在 A2a 中逐项补入 `evidence_chain.md` A.2/A.3。

## 4. 拒收 / 降级规则

- roadmap、vision、solution proposal、guideline、theory-roadmap 不进入普通主统计池。
- 完成型 SLR / SMS / tertiary / MLR / 系统映射即便是后续主统计池候选，A1 阶段也只允许写 `schema_seed`；不得把原文数字复制为 Paper2 最终定量发现。
- 原文未显式给出的 `borderline`、精确 locator、override log、claim map 等字段只能写作 Paper2 增强字段，不得冒充原生字段。
- 派生统计层（如 logistic regression、odds ratio、p value）不得写作 S3 原生样本编码叶子，应放入 S6 统计分析或关系边层。

## 5. 验收命令

```bash
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1-s1s8-19x1/check_s1s8.py
git diff --check
```

通过上述命令只说明 A1 结构与残留门禁通过；不代表 A2a 的页码 / 表图 / supplementary final evidence 已完成。
