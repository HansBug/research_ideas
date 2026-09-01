# 最接近工作矩阵与领域内主张边界

检索截止日为 2026-09-02。本矩阵围绕唯一任务合同，而不是宽泛的“LLM + formal methods”关键词：

`<free-form NL requirements, pre-existing source-attributed STM held fixed during analysis> -> localized requirement-relevant issue reports`

直接任务候选的二值纳入字段只有四项：`free_form_nl_input`、`preexisting_fixed_stm_input`、`localized_requirement_relevant_issues_output`、`implemented_and_evaluated_on_stm_artifacts`。source attribution、native STM semantics 和 replay receipt 是比较字段，不能被用来把满足四字段的工作降到组件层。全文状态只指本轮可复核地取得并逐节阅读的版本；访问受阻不能被当作“无工作”的证据，也不能被本地摘录替代为外部全文证据。

## 检索与处置记录

检索使用 Crossref、OpenAlex、Semantic Scholar、arXiv、DBLP、出版方页、作者/机构库和已收全文，组合查询包括：`("natural language" OR requirements) AND (state machine OR statechart OR STM) AND (issue OR defect OR consistency OR correctness)`、`"behavioral model" requirements issue LLM`、`state machine completion Given When Then`、`state machine property synthesis natural language`。2026-09-02 的 Crossref/DOI 元数据和 2026-07--08 arXiv 查询用于发现候选；标题、摘要或聚合页只用于发现，未被当作细粒度事实来源。后向追引从 MCeT、GWT、Sultan、Estivill、FRET 和 LiSSA 开始，前向追引通过 DOI/OpenAlex locations 检查。去重键为 DOI、arXiv ID、标题和作者年份；纳入标准是与四字段或 C1/C2 组件有实质重叠，排除标准是纯生成、repair、通用代码/协议分析且不处理 STM 输入输出合同。全量 candidate disposition 见下表。

| candidate ID | 发现阶段 | 版本与全文状态 | 四字段判定 | 层级与 disposition |
| --- | --- | --- | --- | --- |
| MCeT | existing/fulltext | MODELS 2025 + arXiv v1，全文 | 是 / 否（sequence diagram）/ 是 / 否（无 STM） | 直接问题邻项；不推翻 scoped STM claim，排除“首次行为图 NL evaluation”泛称。 |
| Li--Zheng | existing/metadata-and-abstract | IET Software 2025 VOR，Gold OA CC-BY；Crossref/DOAJ/出版方摘要可复核，但 Wiley 正文 PDF/XML 和一次新的 headful-browser 访问均停在 Cloudflare 验证页 | 摘要明确：NL 先用于生成 UCS / 使用 UML activity 和 state-machine diagrams / 以三条规则检查 UCS 与过程模型一致性 / 实验涉及这些模型；其余四字段须待可复核全文裁定 | 直接问题风险候选；截至本次审计不能凭摘要或旧本地摘录断言完整合同差异。 |
| Sultan et al. | existing/fulltext | SoSyM 2026，全文 | NL 可在上下文 / 不是固定单一 STM / 输出为多视图 consistency/repair / 评测 SysML | 状态机邻项；任务不是本文合同。 |
| GWT | existing/fulltext | SoSyM 2024，全文 | GWT requirements / 既有 partial STM / 输出新增 transition / 是 | 状态机邻项；completion 修改模型，不输出 issues。 |
| Estivill--Castro--Hexel | existing/fulltext | ENASE 2026，全文 | NL / LLFSM / 输出 synthesized properties / 是 | 状态机邻项；论文评测 property synthesis/SEG，不是运行五个 checker 的 issue verdict。 |
| Liu et al. | existing/fulltext | ENASE 2026，全文 | NL / behavioral models / observable consistency relation / 是 | 状态机/行为模型邻项；比较对象和输出 unit 不是固定 source STM issue report。 |
| FRET | existing/fulltext | REFSQ 2020，全文 | 受限 NL / signals-model mapping / formal requirements / 工具评测 | 方法成分先例；不处理 LLM 对固定 STM 的后验问题发现。 |
| nl2postcond | existing/fulltext | 公开预印本，全文 | NL / code contracts / postconditions / 评测代码 | 方法成分先例；对象不是 STM。 |
| LiSSA | existing/fulltext | ICSE 2025，KITopen author version，全文 | software artifacts / trace links / link output / 是 | 方法成分先例；不是 source STM issue discovery。 |
| Structure--Event--STM | fresh_search/fulltext | arXiv:2604.00275v1，预印本，未同行评审 | 是（非结构化 NL）/ 否（从 NL 生成）/ 否（UML 状态机）/ 是 | 状态机邻项；任务是 NL 到 UML 状态机生成，不是保持既有 STM 不变并发现问题。 |
| King--Vyatkin ETFA | fresh_search/fulltext | ETFA 2025 accepted author manuscript，全文 | STPA 约束 / 是（递归修改 FSM）/ 否（修改模型）/ 是 | 状态机邻项；任务是安全约束驱动的模型修复，不输出定位的需求相关问题报告。 |
| RADIANT | fresh_search | arXiv:2607.16708，预印本，未同行评审 | 生成/修复 FSM | 方法成分先例；不满足固定输入制品字段。 |
| PDEVS/statechart | fresh_search | arXiv:2608.14956，预印本，未同行评审 | 模型生成/变换 | 方法成分先例；不满足完整输入输出合同。 |
| CrossView | fresh_search | arXiv:2608.08038，预印本，未同行评审 | cross-view consistency | 状态机/行为模型邻项；不是单一固定 STM issue discovery。 |
| NL-to-SysMLv2 conformance | fresh_search | arXiv:2607.14162，预印本，未同行评审 | NL-to-model conformance/generation | 状态机邻项；输出不是 localized issue reports。 |
| SeriCrypt | fresh_search | arXiv:2608.24498，预印本，未同行评审 | protocol/formal artifact analysis | 方法成分先例；对象不是 STM。 |

IET 的 Crossref record 给出 VOR PDF 和 full XML text-mining URLs，DOAJ 标为 Gold OA CC-BY；常规出版社端和本轮新的 headful-browser 会话均返回 Cloudflare 验证页。既有 [IET card](./neighborhood/cards/iet-software-2025-consistency-traceability.md) 保存了先前会话摘录，却没有可供独立读取的全文载荷，因而它不能作为本轮一手全文依据。该工作仍保留为直接风险候选；R1 不能把访问失败解释为不存在，也不能用摘要完成细粒度 task disposition。

## 第一层：直接问题邻项

| 工作 | object、input、output | requirement relation 与 issue unit | evidence、source attribution、human protocol | 与本文的决定性差异 |
| --- | --- | --- | --- | --- |
| Ahmed et al., MCeT | free-style NL + existing PlantUML **sequence diagram**；输出 localized NL issues。 | 三路 holistic/diagram-atom/requirement-atom LLM check，最终报告是 requirements-to-diagram correctness issues。 | parser 只抽 atoms；correctness 和 same-root-cause equivalence 都有人评估。它并非“没有 relation”，本文的差异是 separately recorded validity/relation/ledger protocol，不是首次做 relation 或更高一致性。 | sequence diagram 没有 persistent state、hierarchy、transition/guard/action semantics、reachable configuration 或 state-space quantification。它没有 FCSTM-like executable representation、four-family typed lowering、hash-bound native replay、W2/W1/W0 或 compiler/runtime/projection failure isolation。它称可适配其他语言，但 threats/conclusion 将其他 behavioral models 留为 future work，未实现和评测 STM task。[^mcet] |
| Li and Zheng | 出版方摘要确认：LLM 由原始 NL 生成 UCS，并将 UCS 与 UML activity/state-machine diagrams 的过程逻辑作一致性检查。 | 摘要不足以判定模型比较端是否仍以 free-form NL 为显式输入、输出 unit 是否为 localized issue reports，或完整评测单位。 | Gold-OA 元数据、CC-BY 和摘要可复核；正文取件被 Cloudflare 阻断，既有本地摘录不充当外部全文证据。 | 它是实质直接风险候选，限制无范围的 NL-to-behavior-model consistency priority claim；在全文可复核前，不以细粒度差异承重 scoped claim。[^li_zheng] |

MCeT 表明不应把主张写成“第一个根据 NL 自动评估行为图”或“第一个输出细粒度问题”。Li--Zheng 的摘要表明不应把主张写成“第一个将 NL 与行为模型做一致性检查”。MCeT 的全文允许对其作 task disposition；Li--Zheng 在可复核全文取得前只能作为直接风险保留，不能以访问失败或本地摘录支持 scoped priority wording。最终 wording 因而必须同时覆盖记录检索、四字段合同和 IET 全文核验的完成状态，不使用 universal first/only。

## 第二层：状态机或行为模型邻项

| 工作 | 实际任务 | 与本文的共同点 | 不可替代的差异 |
| --- | --- | --- | --- |
| Sultan et al. | SysML 多视图 consistency detection/correction。 | behavioral model、LLM、规则和修正。 | 比较多个视图并修正，不是 NL 与分析中固定 source STM 到 issue reports。[^sultan] |
| de Biase et al. (GWT) | Given--When--Then requirements 驱动 SysML state-machine completion，向既有 states 添加 transitions/triggers/guards/effects。 | NL、critical event-driven systems、pre-existing partial state machine。 | 模型被补全，输出是 model adaptation；不是保留输入模型并报告问题。[^gwt] |
| Estivill-Castro and Hexel | NL 到 LLFSM property synthesis 并以 SEG 评测。 | state machine、NL、可执行 properties。 | output 是 synthesized property；不能误写成五个已运行 checker 的 issue/counterexample results。[^estivill] |
| Liu et al. | observable consistency between behavioral artifacts。 | behavioral semantics、consistency。 | object、relation 和 evaluation unit 不是 single source STM 的 requirement-relative report。 |
| Abdulkarim et al. | 非结构化 NL 到 UML 状态机生成，比较单提示、结构驱动、事件驱动和混合策略。 | UML 状态机、NL、结构化中间输出与人工评测。 | 输入不含既有 STM，输出是生成的模型而非问题报告；即使其框架可迁移到其他语言，也没有实现本论文的固定 STM 分析任务。[^structure_event] |
| King and Vyatkin | 将 STPA 控制器约束递归应用于既有 FSM，并生成 IEC 61499 代码。 | 既有状态机制品、NL 约束、控制系统与可执行转换。 | 每轮直接修改上一轮 FSM，输出是修订制品；事后人工把改动评为正/负/中性，方法没有定位 issue report 或对固定源 STM 的评测。[^king_vyatkin] |

## 第三层：方法成分先例

FRET 和 nl2postcond 表明 NL 可以被转成可执行 formal assertion；LiSSA 表明 traceability link recovery 是独立问题；UML state-machine verification 传统说明 graph/SMT/replay 并非本文发明。这些工作分别限制 C1 的 representation/traceability 表述和 C2 的 assertion/replay 组件优先权，但不能由“某个成分已有”推出 `<NL, fixed STM> -> localized issue discovery` 没有领域增量。[^fret][^lissa][^uml_survey]

## 第四层：评测与可靠性来源

MCeT 的 correctness 与 same-root-cause human evaluation、LLM-as-Judge 的自评限制，以及现有 ledger/relation policy 都支持把 report generation、mechanical evidence 和 human validity 分离。它们不挑战完整任务优先权。本文不将“保存 D/A、relation 和 ledger”描述为首次人工 relation，也不暗示未经测量的 inter-rater reliability。[^mcet][^judge]

## 冻结的主张

**领域问题。** 本文面向自由文本 NL 与分析期间保持不变、带来源归属的 STM，发现并定位 requirement-relevant issues。STM 是方法层面的语言族；PlantUML 是唯一实现和评测过的 adapter，其 54 个制品只构成技术路线的案例研究。

**当前可写的领域主张。** *We present and evaluate a state-machine-specific workflow that compares free-form natural-language requirements with a pre-existing, source-attributed STM held fixed during analysis and returns localized findings.* IET 的摘要已构成直接风险，而其可复核全文尚未取得；在四字段 disposition 完成前，本矩阵不冻结“未发现先前工作”或 scoped `first` wording。

**C1 wording。** *C1 provides a provenance-preserving executable working representation and deterministic inspect augmentation for the stated task; it does not claim a cross-language semantic-preservation theorem or a separately identified causal gain.*

**C2 wording。** *C2 connects applicable candidates to a literature-informed, retrospectively consolidated typed-obligation layer and source-bound native replay receipts, separating mechanical evidence strength from human validity and relation judgment.*

**不能推出。** 上述主张不宣称 LLM、FCSTM conversion、state-machine verification、SMT/model checking、traceability、replay 或人工 adjudication 的 first/only；不宣称所有 STM language 都被实现，或 PlantUML case study 已验证跨语言效果；不把 IET access failure 写成 absence，也不以旧本地摘录完成全文核验。

## 引用

[^mcet]: Khaled Ahmed et al. “MCeT: Behavioral Model Correctness Evaluation using Large Language Models.” *MODELS*, 2025, pp. 84--95. https://doi.org/10.1109/MODELS67397.2025.00014; arXiv:2508.00630.
[^li_zheng]: Haibo Li and Lixiao Zheng. “Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework.” *IET Software*, 2025. https://doi.org/10.1049/sfw2/6714956.
[^sultan]: Bastien Sultan, Ludovic Apvrille, and Sophie Coudert. “On the Consistency of State Machines, Use Cases and Block Diagrams Using Dependency Graphs and Large Language Models.” *Software and Systems Modeling*, 2026, online first. https://doi.org/10.1007/s10270-026-01388-4.
[^gwt]: Maria Stella de Biase et al. “Completion of SysML State Machines from Given--When--Then Requirements.” *Software and Systems Modeling*, 2024. https://doi.org/10.1007/s10270-024-01228-3.
[^estivill]: Estivill-Castro and Hexel. “Property Synthesis from Natural Language Requirements for LLFSM Models.” *ENASE*, 2026. https://www.scitepress.org/Papers/2026/147167/147167.pdf.
[^fret]: Dimitra Giannakopoulou, Anastasia Mavridou, Julian Rhein, Thomas Pressburger, Johann Schumann, and Nija Shi. “Formal Requirements Elicitation with FRET.” *REFSQ 2020 Workshops*, 2020. https://ntrs.nasa.gov/api/citations/20200001989/downloads/20200001989.pdf.
[^lissa]: Fuchß et al. “LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation.” *ICSE*, 2025. https://doi.org/10.1109/ICSE55347.2025.00186.
[^structure_event]: Samer Abdulkarim et al. “Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models.” arXiv:2604.00275v1, 2026. https://arxiv.org/abs/2604.00275. arXiv preprint; not peer-reviewed as of 2026-09-02.
[^king_vyatkin]: Akira King and Valeriy Vyatkin. “LLM-based Iterative Refinement of Finite-State Machines with STPA Controller Constraints and Generation of IEC 61499 Code.” *ETFA*, 2025, pp. 1--8. https://doi.org/10.1109/ETFA65518.2025.11205687. Full text verified from the accepted author manuscript: https://aaltodoc.aalto.fi/bitstreams/9ab39cdd-e8af-4769-a1e6-974595dc7412/download.
[^uml_survey]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification – A Survey.” *ACM Computing Surveys*, 55(13s), 2023, pp. 1--47. https://doi.org/10.1145/3579821.
[^judge]: Wang et al. “LLM-as-a-Judge in Software Engineering.” *ISSTA*, 2025. https://doi.org/10.1145/3728963.
