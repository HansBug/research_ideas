# requirements-quality-theory-roadmap：A1-S1S8 四分栏提取

## 总体统计池裁决

**裁决：不进入 `survey_of_surveys` 的 SLR/SMS 主统计池；仅作为 `schema_seed / methodological_seed / boundary_anchor`。** 原因是本文原型是 VIEW POINT / research commentary，结构为 **theory → evaluation → roadmap**：先提出 RQT 概念理论，再用继承自前作的 57 篇 requirements quality primary studies 做状态评价，最后生成六条 roadmap streams。其 §4 内部有编码本、分母与描述统计，因而可作为“理论概念如何转成 categorical-variable codebook”的方法样本；但样本是 inherited convenience sample，且整体不是新执行的标准 SLR/SMS，不能把 RE 领域比例、roadmap 结论或候选 finding 并入 Paper2 主统计发现。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要和 §1 明确本文是 research commentary，贡献为 RQT 理论统一、requirements quality literature survey、research roadmap；§4 提出 RQ：“How are the concepts of the requirements quality theory reported in requirements quality literature?” | 根任务不是常规 SLR/SMS，而是三段式 commentary：Tree A 理论概念、Tree B 文献编码评价、Tree C roadmap。 | **不入主池**；S1 可作“hybrid commentary / theory-evaluation-roadmap”边界类型，当前 review.md 标“强”可保留但必须带类型限定。 | 核对 PDF 首页 VIEW POINT、摘要贡献句、§4 RQ 页码；确认正式出版版没有额外 protocol 附录。 |
| S2 语料收集与筛选 | §4.1 说明 target population 是 requirements quality factors 文献；样本来自前作 systematic study 的 57 篇 primary studies，并明确是 non-probabilistic convenience sampling。 | 样本单位是 57 篇原始研究；不是本文新检索得到的 SLR/SMS 纳排漏斗。 | **不入主池**；只能作为“继承样本 / convenience sample”风险模式。建议 S2 保持“中”，不得升强。 | 核对前作样本来源、57 篇清单、是否只覆盖 empirical contributions；若写入论文，必须注明 inherited sample。 |
| S3 原生维度树/样本编码对象 | §3 给出 RQT 11 concepts；§4.2 说明每个 concept 关联一个或多个 categorical variables 与 codes；§5 给出 roadmap streams。 | 复原为维度森林：A = RQT 11 概念元模型；B = §4 extraction guideline/codebook，是真正样本编码树；C = §5 六条 roadmap streams。 | **局部可用但不入主池**；可作维度树设计样本，不能把 RQT 概念或 roadmap streams 统计为 survey 主发现。 | 精核 Fig. 2、Table 1、Fig. 4、Fig. 5 与 Zenodo 复现包字段；确认 B 树叶子未漏。 |
| S4 字段级证据 | §4.2 给出 entity explicit/implicit、factor explicitness/form 等示例；§4.3 给出多项分母和结果，但部分 code 只在 replication package 中。 | 字段层由 RQT concept 派生 categorical variables；已知叶子包括 entity explicitness、factor explicitness/form、impact evidence/modality、context/cost/resource 等。 | **不入最终定量字段池**；可作 codebook construction seed。当前 S4 “中”合理，不能写成字段全集已完全核验。 | 逐项核验 Zenodo 8167598、Fig. 4 数值、impact remaining dimensions、context/cost/resource 完整枚举。 |
| S5 维度模式演化 | §4.2 说明 codes 第一轮 ad hoc 创建，第二轮基于讨论和理论背景精炼；§4.5 讨论隐式概念抽取造成的 construct/internal validity 风险。 | 维度演化模式是“理论概念 → 初始 codes → 讨论/理论精炼 → descriptive statistics”，不是跨综述迭代 taxonomy。 | **方法种子可用，不入主池**；S5 可保持“中”，用于提示 A2a 记录字段来源与 refinement 过程。 | 核对 extraction guideline 版本、讨论/精炼证据是否只在复现包；不得臆测有完整裁决日志。 |
| S6 统计分析 | §4.3 报告 n=57、impact 子集 n=40、24/57、17/57、14/57、8/57、37/40、19/40、11/40、10/40 等；§4.2 报告 agreement 83.3%、Kappa 54.2%、S-Score 76.8%。 | 统计树服务于本文内部评价：RQT concept coverage 与 reporting modes 的 descriptive statistics。 | **只承认内部统计强，不进 Paper2 主统计池**；S6 应维持“中”或写“内部强/外部不合格”，避免把 convenience sample 当主样本。 | 复核 Fig. 4 与正文数字一致性、n=40 子集定义、reliability 计算样本 2+4 的解释。 |
| S7 候选 finding | §4.4/§6 将结果解释为 artifact-centric bias 与 activity/context/economic concepts 被忽视；§5 把缺口转为六条 roadmap streams。 | finding 形态是“字段覆盖缺口 → 理论/实践风险 → roadmap action”；C 树是路线图，不是样本编码结果。 | **不入主统计池**；只作 gap-to-roadmap 写法样本。S7 “中”可保留，必须禁止迁移 RE 领域比例和 roadmap 内容。 | 核对 §4.4、§5.1--§5.6 与结论页码；区分作者解释、领域结论与可迁移方法模式。 |
| S8 研究者/作者质疑与裁决 | §4.2 有第一作者全量抽取、第二作者约 10% 随机样本 instrument validation、inter-rater reliability；§4.5 有 internal/construct/external validity threats。 | 质量控制节点包括独立抽取、训练/正式 reliability、复现包和 validity threats；但没有类似 SLR review 的完整纳排裁决日志。 | **方法种子可用，不入主池**；S8 “中”合理，不应升强。 | 核对六篇子样、两篇 training 与四篇 IRR 的原文表述；检查复现包是否含争议处理记录。 |

## 建议降级 / 修正

1. **总账必须标为主统计池排除**：`theory / evaluation / roadmap` 与 `convenience sample` 均不能进入 Paper2 主统计池。
2. **S6 建议写成“内部统计强 / 主池资格中或不合格”**：有描述统计与 IRR，但只支持本文内部状态评价。
3. **S7 必须保守**：roadmap 可迁移为写作结构，不可迁移为跨综述候选 finding。
