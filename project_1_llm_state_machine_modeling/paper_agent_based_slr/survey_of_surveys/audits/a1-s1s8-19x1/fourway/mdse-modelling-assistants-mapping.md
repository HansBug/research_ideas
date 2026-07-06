# mdse-modelling-assistants-mapping：A1-S1S8 四分栏提取

## 总体统计池裁决

**裁决：保留为 `survey_of_surveys` S1--S8 主统计池候选，但当前只能作为 `schema_seed / statistical_pool_candidate`，A2a 页码、表图、Zenodo raw data 与实践文档来源精核前不得进入最终定量发现。**

理由：原文是 IST 2024 systematic mapping，并叠加实践侧公开文档审查；文献侧有 5 个数据库、PICO 检索式、I/E criteria、QA、滚雪球、3,176 条筛查记录、58 个 included proposals、Kappa=0.634/0.651；实践侧有 Gartner MQ 2023 的 17 个工具、7 个 documented tools、15 个 documented proposals/quotes。其“策略 / 目标 / 限制 / 指标 / 目标用户”维度森林可支撑 S1--S8 schema 统计候选；但 Table 3 “five limitation clusters” 与 L1--L6 冲突、图表气泡数值、页码、Zenodo 复现包和 vendor quote 原始网页仍需 A2a 复核。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要与 §1 明确 MRQ：文献和实践中有哪些 proposal 用于辅助人类在 MDSE tools 中完成 modelling tasks；RQ1--RQ3 分别问策略、目标/限制、指标/目标用户，RQ4 问实践状态。 | 根节点为“MDSE modelling assistance”，下接文献侧 RQ1--RQ3 与实践侧 RQ4；任务边界排除泛画图工具和元建模/工具开发。 | **合格**：可进入 S1 任务设定统计池，证据强。 | 核对 PDF 首页/§1 页码与 MRQ/RQ 版式；正式写作时确认 online-first 与卷期年份口径。 |
| S2 语料收集与筛选 | §3.2--§4.1 给出 5 数据库、1985--2024、PICO search string、I/E criteria、QA top-12 snowballing seeds、4 轮滚雪球；3,176 screened records → 77 possible proposals → 58 included；实践侧为 GMQ 2023 的 17 tools。 | 文献侧样本单位为 primary proposal/study；实践侧样本单位为 GMQ tool → documented tool → documented proposal/quote。 | **合格**：可进入 S2 分母/筛选流程统计池；实践侧需单独标注 grey-literature/documentation review。 | 复核 Fig. 3 PRISMA flow、QA top-12 选择、Zenodo raw protocol；GMQ 原始报告与 17 tool 列表需来源级核验。 |
| S3 原生维度树/样本编码对象 | §3.5 要求抽取 RQ1 strategy keywords、RQ2 goals/limitations、RQ3 metrics/users；§4.2--§4.4 与 Table 2--4 给出聚类；§5.2/Table 5 将实践文档 quote 投影到同一维度。 | 原生结构是维度森林：文献侧 proposal-level 五主干（strategy, goal, limitation, metric, target user）+ 实践侧 tool/documentation/proposal quote 投影，外接 GMQ 类别和 D/NF 文档状态。 | **合格**：可进入 S3 维度树统计池；样本单位需写成“58 proposals + 17 tools/7 documented tools/15 practice proposals”。 | 精核 Table 2--5 页码、每个聚类完整取值、practice quote 与 tool/proposal 映射；不要把 RQ 当普通结果章节。 |
| S4 字段级证据 | §3.5 要求 literal text fragments；Table 2--5 给聚类关键词与文档 quotes；§7.1 说明 data extraction bias、作者术语依赖和公开文档限制。 | 字段证据存在但当前本地证据链多为章节/表级锚点，尚未逐 proposal / quote 精确到样本 ID、页码、行号、Zenodo 原始表。 | **建议降级为中**：可作 S4 schema seed，不宜进入字段级最终统计；需 A2a 后再升级。 | 必须核对 Zenodo 10262145、raw extraction/clustered data、Table 5 vendor quote 原始网页；补齐字段级 source span。 |
| S5 维度模式演化 | §3.1 提到 9 位 SE experts 咨询 RQ；§3.5 先 literal extraction 后按作者术语聚类；§4.1 有 R4 复核聚类并报告 Kappa=0.651；§7.1 讨论主观聚类威胁。 | 模式演化链为 RQ consultation → extraction fields → author-terminology clustering → R4 triangulation/review → Kappa agreement；缺失版本化 codebook 和完整冲突日志。 | **合格**：可进入 S5 演化/裁决机制统计池，但强度标为“有过程、无完整 codebook”。 | 复核专家咨询位置、R4 disagreement/triangulation 描述、Kappa 计算对象；若 Zenodo 含 codebook，应回填。 |
| S6 统计分析 | §4.2--§4.4 给出策略比例（如 tools 39.7%、software-based 93.1%）、目标三分、limitations reported 50.0%、metrics/users 分布；§5.2 给出实践侧 10/17 NF、15 proposals、80% strategy documented、73.3% metric/user NF；§6 有 bubble/comparative analysis。 | 可统计叶子包括 strategy_cluster、goal_cluster、limitation_reported/cluster、metric_cluster、user_cluster、documentation_status、GMQ class 与若干关系边。 | **合格但 not_verified**：可进入 S6 候选统计池；A2a 前只能作候选统计观察。 | 精核 Fig. 4--13 气泡图、分母、百分比四舍五入、Table 3 L1--L6 冲突；不得把未核图形关系写成 final finding。 |
| S7 候选 finding | 摘要、§6、§8 主张 limitations/evaluation metrics/target users 文档稀缺；§8 还提出 AI/LLM/GPT 可能改变 modelling assistance 并需要 unified framework。 | 可分两类：统计支撑 finding（限制/指标/用户缺失、software-based 主导）与弱候选启发（AI disruption/unified framework future work）。 | **部分合格**：前者可进候选 finding 统计池；AI/LLM 相关只能作弱启发，不进最终领域发现。 | A2a 需把每条 finding 绑定支撑统计、反证和 scope；AI/LLM 论述必须标注为 future expectation。 |
| S8 研究者/作者质疑与裁决 | §4.1 有 R1/R2/R3/R4 分工、R3/R4 复核 77 proposals、Kappa=0.634 inclusion 与 0.651 clustering；§7 讨论 selection/data extraction/subjective interpretation/inter-rater/grey literature/search/language threats。 | 裁决树包括 multi-reviewer selection、quality assessment、R4 clustering review、Kappa、threats 与 residual limitations；数据抽取阶段未算 Kappa 是明确限制。 | **合格**：可进入 S8 质疑/裁决机制统计池；需保留“data extraction no Kappa”限制。 | 核对 §7 threats 分类与 mitigation/residual limitation；补 Zenodo/appendix 是否有更细冲突日志。 |

## 建议降级 / 修正

1. **S4 降级为中**：原文有字段抽取规则和表格/quote，但本地仍缺 proposal-level / quote-level 精确证据链；A2a 前不要升为“强字段级证据”。
2. **S6 保持候选统计，不作 final finding**：所有百分比和 bubble chart 关系边需回 PDF/Fig. 4--13 与 Zenodo 精核。
3. **Table 3 限制聚类必须保留冲突标记**：正文称 five limitation clusters，但表格和后文列出 L1--L6；A2a 前不得将 limitation_cluster 写成已解决的 5 类或 6 类最终口径。
4. **实践侧分母修正为 17 tools → 7 documented tools → 15 documented proposals/quotes**；`NF` 只表示公开文档未发现，不等于工具没有 modelling assistant。
