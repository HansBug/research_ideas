# interactive-llm-systematic-mapping：S1--S8 四分栏审计补充

## 总体统计池裁决

不进入主统计池。本文是作者自述的 solution proposal，目标是讨论 LLM 支持 systematic mapping process 的可能流程；没有执行系统检索、纳排、数据抽取、样本编码或统计分析。`paper_content.txt` 明确显示方法为 solution proposal，并声明 “No data was used”。因此只可作为方法学种子 / schema seed / boundary anchor，不能作为 Paper2 主统计池或实证 finding 来源。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 原文目标是讨论 LLM 如何用于 mapping study process；Method 自述为 solution proposal，非已执行 SMS/SLR。 | 对应概念流程树根节点与 B1 流程阶段；可复原 “need/RQ → search → inc/exc → extraction → visualization → reporting” 的任务脚手架。 | 不进主统计池；可作任务设定与 interactive scaffold 的方法学种子。 | 核对 PDF Fig. 1 中阶段名称与文本 §2 是否完全一致；补充材料术语定义待核验。 |
| S2 语料收集与筛选 | 原文未给数据库、检索式、PRISMA、候选分母、纳排清单；10 条 references 仅作 relevant literature 叙事旁证。 | S2 在原生树中只是方案阶段：search 子阶段含 3 agents，inc/exc 子阶段强调 rationale/citation/traceability；不是实际 corpus pipeline。 | 不适用主统计池；不得把 references 或被引研究结果当本文样本。 | A2a 核对是否存在隐藏 supplement 中的术语定义；但即使有定义，也不能改变“无语料分母”裁决。 |
| S3 原生维度树/样本编码对象 | 原文逐节描述的是 LLM-supported SMS 的流程阶段、agent 角色和 HITL 节点；无原始研究样本编码表。 | 复原为降级维度森林：B1 流程阶段、B2 input/refinement/output 三元组、B3 search 三智能体、B4 技术机制、B5 audit 字段、B6 risk、B7 roadmap。 | 不进统计池；可作 schema seed，尤其是阶段 × 人机角色 × audit 字段。 | PDF 版面核对 Fig. 1 的框图、箭头和输入/输出槽；确认是否存在文本抽取遗漏。 |
| S4 字段级证据 | 明确字段包括研究者输入、LLM 输出、交互修订、search agents、inc/exc 理由与 citation、inductive/deductive coding。 | 可映射到 B2 triplet、B3 agents、B5 audit fields；但 `override`、`source_loc` 等更细字段部分是本地审计增强。 | 不进主统计；可作为字段设计候选，需标注“原文明示”与“本地扩展”边界。 | A2a 逐项区分原文显式字段 vs. Paper2 增强字段，避免把增强字段写成作者原生 schema。 |
| S5 维度模式演化 | 原文只有作者基于经验迭代设计 proposal，以及末尾建议先优化单步骤、再做整体 prototype；没有 coding saturation 或 taxonomy evolution。 | 仅可复原为 B7 roadmap：individual steps evaluation 与 end-to-end prototype；不构成维度演化证据。 | 基本不进统计池；最多作为路线图/研究议程种子。 | 核对 §3 末尾两条 research directions 的表述；不得扩写成“已验证迭代方法”。 |
| S6 统计分析 | 本文没有自身统计表、分母或实验指标；recall/precision/GPT-4 表现均来自被引文献 [5]--[9]。 | 原生树无统计分析节点；相关数字只能挂在“被引文献旁证”而非本文 finding。 | 不适用主统计池；严禁把被引研究统计混入本文主统计。 | A2a 标注所有被引统计的来源归属，防止二次引用时误标为 Petersen & Gerken 结果。 |
| S7 候选 finding | 可支持的方法学 claim：LLM 可辅助 SMS 各阶段，但需专家在环、可复现检索、traceability、SE-specific evaluation。 | 可挂到 B5 audit/risk 与 B6 validity/risk；属于 design claim / methodological insight，不是效果 finding。 | 不进实证 finding 池；可作为 boundary anchor 和 method rationale。 | 核对 claim 强度：只能写“作者提出/建议/强调”，不能写“证明有效”。 |
| S8 研究者/作者质疑与裁决 | 原文强调 reviewers 需懂 mapping 方法且是主题专家；inc/exc 需理由、citation、traceability；但无多评审者协议或一致性统计。 | 可映射到 B2 HITL、B5 audit 字段、B6 risk；不含正式 adjudication workflow。 | 不进统计池；可作审计机制启发。 | A2a 明确区分 human-in-the-loop 原则与正式 reviewer adjudication/override 机制。 |

## 建议降级 / 修正

1. S1：维持“中”，但需解释为“方法设定中”，不是实证综述任务设定中。
2. S3：建议从“中”标注为“中（降级维度森林）”，避免读者误以为存在原始研究样本编码 schema。
3. S4：建议从“中”改为“中偏弱 / 部分强”：阶段与 triplet 较强，override/source location 等字段是本地增强，不能整体算原文明示。
4. S7：建议从“中”降为“弱--中”：可作方法学候选 finding，但不是经验证 finding。
5. S8：维持“弱”：原文只有 HITL 与 traceability 原则，没有正式裁决协议、一致性或 QA 日志。
