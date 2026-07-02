# devsecops-primary-dimensions：S1--S8 四分栏审计补充

## 总体统计池裁决

本文是 A2a 主统计池候选 / A1 阶段仅作模式种子。理由：原文具备系统 MLR、WL/GL 双轨检索、QA、TA 编码链、CPTM 关系模型与开放材料；但当前审计仍未逐项核验 PDF 表图页码、Fig. 5--9 连线、Table 21 全关系边与 Zenodo full CPTM。因此可进入后续精核队列，不应在 A2a 前进入最终定量统计或支撑 Paper2 目标领域最终 finding。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文明确为 DevSecOps MLR；RQ1 问 aspects / themes / links，RQ2 问 GSE contexts。 | 根节点可复原为“DevSecOps 当前状态 + 全球采用探测”，下接 RQ1 维度森林与 RQ2 context probe。 | 候选可用：任务设定清晰，可统计为“现状 + 维度 + 关系 + 缺失探测”型综述。 | 核对 PDF 中 §3.3 RQ 原文页码；确认 RQ2 是否只作 gap probe，不并入五大 aspect。 |
| S2 语料收集与筛选 | 原文报告 WL 104、GL 43；RQ1 主池为 102 WL + 43 GL，RQ2 另 2 WL；confirmatory 13 WL + 7 GL 不进 TA/CPTM。 | 样本单位需拆两层：外层 primary studies，内层 text segments / codes / themes / model items。 | 候选可用但需分母隔离：主 MLR、RQ2、confirmatory 必须分开统计。 | 精核 Table 3、Fig. 3、Appendix A.1--A.3；统一 104/102+2/147/20 confirmatory 口径。 |
| S3 原生维度树/样本编码对象 | 摘要与 §4.1 明确五大 aspects；§3.8.2 明确 Text → Code → Themes → Model。 | 复原为 5 棵 aspect 子树：Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement；C/P/T/M 再接 CPTM 关系图。 | 强候选：有原生树和编码对象，不是 reviewer 后验投影。 | 核验 Table 5 的 text segment / code / theme / category 计数；确认 definitions 是否不进入 CPTM。 |
| S4 字段级证据 | Tables 5--19 给出 aspect、code、theme、category、ID、频次、source IDs；Table 21 给 C/P/T/M 映射。 | 叶子字段可复原为 aspect、category、text segment、code、theme、C/P/M/T ID、frequency、source track、source ID、prior-review match、lifecycle stage、关系边。 | 候选可用但暂不最终入池：字段丰富，可统计；但关系边需版面/补充材料精核。 | 打开 PDF 核 Tables 6--21 跨页对齐；核 Zenodo raw text/codes、TA tables、full CPTM。 |
| S5 维度模式演化 | 原文说明 WL 先归纳编码，GL 主要基于 WL codes/themes 演绎分析，再映射 Gartner lifecycle 形成 CPTM。 | 模式演化链为 inductive WL → deductive GL → category → lifecycle projection → CPTM model。 | 候选可用：可统计为“归纳-演绎混合模式演化”。 | 核 §3.8.2 对 WL/GL 分工和 Gartner lifecycle 的表述；核 Fig. 5 模型生成链。 |
| S6 统计分析 | 原文提供 aspect 分布、WL/GL 差异、C/P/T/M 项数、频次、category 排序、RQ2 命中链。 | 可复原统计层：aspect 频次、category 分布、source-track 差异、prior-review overlap、CPTM edge coverage、GSE absence count。 | 候选可用但需限制：只统计原文内部样本，不外推为当前 DevSecOps 全貌。 | 精核 Fig. 4、Table 2、Tables 8--21；确认 confirmatory search 不混入主统计。 |
| S7 候选 finding | 原文讨论 practices 最多、metrics 最薄弱、WL/GL 互补、GSE 缺失、framework design 趋势等。 | finding 应挂接到统计观察、CPTM 缺口、RQ2 absence probe 与 confirmatory-only 标志。 | 中等候选：可作为作者候选发现池；不能直接作为 Paper2 目标领域最终 finding。 | 对每条 finding 标注主样本 / confirmatory / prior-review 补入；尤其核 GSE negative finding 的竞争解释。 |
| S8 研究者/作者质疑与裁决 | 原文没有独立“质疑-裁决”机制；但有 reflexive TA、多作者 weekly/bi-weekly 协商、trustworthiness、threats、open material。 | 可复原为“研究者协商与信度控制”节点，而不是正式 adversarial adjudication 节点。 | 仅弱/中候选：可统计为 trustworthiness / author-consensus evidence，不宜计为完整裁决流程。 | 核 §3.8.2、§3.8.3、§5.1--§5.3；确认是否存在 Zenodo 中额外 reviewer/coder decision log。 |

## 建议降级 / 修正

1. S7 从“强”降为“中”：原文 finding 很丰富，但包含领域结论、confirmatory trend 与 negative finding；A2a 前不宜与 S1--S6 的结构性证据同等强。
2. S8 保持“中”或降为“弱-中”：有 trustworthiness 与多作者协商，但没有独立质疑-裁决流程，不能写成强裁决证据。
3. 总体统计池表述应统一：建议固定为“后续主统计池候选；A2a 前仅作模式种子 / schema seed，不进入最终定量统计”。
