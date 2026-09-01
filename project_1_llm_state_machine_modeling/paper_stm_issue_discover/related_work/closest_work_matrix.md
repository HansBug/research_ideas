# Paper1 最接近工作对照矩阵

本文件是 R1 唯一的最接近工作对照矩阵。检索截止日为 2026-09-01（Asia/Shanghai）。它是定向的新检索，不声称已完成系统综述。方法可由适配器在声明的源语言子集上实例化，前提是适配器提供作者源属追踪、规则相关能力约定、FCSTM 投影和失败关闭边界；本文的经验案例研究使用固定的作者 PlantUML 状态机与其 NL 需求。案例研究使用人工完成的有效性和关系裁定，并在适用时提供可执行回执。

## 检索记录

| 日期 | 数据库或入口 | 检索式或入口 | 本轮候选与处理 |
| --- | --- | --- | --- |
| 2026-09-01 | OpenAlex、Crossref、出版社与作者开放版本 | `"behavioral model" requirements LLM evaluation`；`state machine requirements consistency "large language model"`；`SysML requirements consistency LLM` | 每个 OpenAlex 入口获取首页 25 条作为候选页；纳入 4 篇：MCeT、SoSyM 2026 SysML 一致性、GWT SysML 状态机补全与 Internetware 输入论文。 |
| 2026-09-01 | OpenAlex、Crossref、arXiv、出版社 | `executable behavioral specification LLM requirements`；`NL executable postconditions LLM`；`UML state machine formalization model checking` | 每个入口获取首页 25 条作为候选页；纳入 4 篇：FRET、nl2postcond、UML 状态机形式化综述与需求可满足性工作。 |
| 2026-09-01 | OpenAlex、Crossref、arXiv、出版社 | `requirements traceability large language model link recovery`；`LLM-as-a-Judge reliability software engineering`；`LLM self-correction external feedback` | 每个入口获取首页 25 条作为候选页；纳入 LiSSA、LLM-as-a-Judge in SE、LLM 自校正边界、Liu 等的可观察一致性检查，以及 IET Software 2025 的需求—UML 一致性候选。 |

纳入标准是：工作会削弱 Paper1 关于固定制品、需求关系、问题单位、证据、来源归因或人工评测的主张。仅生成模型的论文只在输入来源或边界需要时纳入。排除原因、访问异常和全文状态见下表。Crossref 的 BibTeX 入口在每个 DOI 链接旁给出；没有正式全文或无法核对段落的材料不支撑细粒度主张。

## 承重工作

| 工作与全文状态 | 对象、输入与输出 | 与 Paper1 的共同点和决定性差异 | 评测、证据与可比性 | 本文可用定位 |
| --- | --- | --- | --- | --- |
| Ahmed 等，[*MCeT*，MODELS 2025](https://arxiv.org/abs/2508.00630)，[DOI](https://doi.org/10.1109/MODELS67397.2025.00014)，[BibTeX](https://api.crossref.org/works/10.1109%2FMODELS67397.2025.00014/transform/application/x-bibtex)，全文已读，12 页 | 现有 PlantUML 序列图与自由文本需求；LLM 原子化、发现并定位问题，再由 LLM 交叉核查。 | 这是最接近的任务形态。它是序列图，本文案例研究是状态机；但其 §III 说明技术可适配其他建模语言，因此不能把“状态机而非序列图”单独写成新颖性。 | 问题解释存在，但不是状态机原生可执行证据与人工 source-first relation 协议。公开比例的分母和协议不能与本文并列作数值 baseline。 | 只可写“本文在 PlantUML 案例研究中将作者源定位、执行证据与人工评测分开。” |
| Sultan、Apvrille、Coudert，[SoSyM 2026](https://link.springer.com/content/pdf/10.1007/s10270-026-01388-4.pdf)，[DOI](https://doi.org/10.1007/s10270-026-01388-4)，[BibTeX](https://api.crossref.org/works/10.1007%2Fs10270-026-01388-4/transform/application/x-bibtex)，全文已读，40 页 | SysML 用例、块和状态机图之间的 LLM、规则与依赖图检测/纠正。 | 是最强的状态机 LLM 分析邻项，但它比较多视图模型，不比较 NL 需求与冻结作者状态机。 | 文中报告 true/false positives 而未计 false negatives；LLM 组件有 FP/FN。其对象、分母和 review protocol 与本文不同。 | 不可主张“首个 LLM 状态机分析”；可明确任务关系不同。 |
| de Biase 等，[GWT SysML 状态机补全，SoSyM](https://link.springer.com/content/pdf/10.1007/s10270-024-01228-3.pdf)，[DOI](https://doi.org/10.1007/s10270-024-01228-3)，[BibTeX](https://api.crossref.org/works/10.1007%2Fs10270-024-01228-3/transform/application/x-bibtex)，全文已读，37 页 | Given--When--Then 需求与部分 SysML 状态机；生成带 trigger、guard、effect 的迁移和 `«satisfy»` 追踪链接。 | 需求到状态机与追踪关系已被处理；它是补全，不是固定作者制品的问题发现。 | 文中 §12 明确不处理未被模型元素满足的需求等完整性检查。没有本文的 report-to-ledger relation 或回执分层。 | 不可单独主张 state-machine traceability 或需求覆盖是新颖点。 |
| Wang 等，[Internetware 2025](https://doi.org/10.1145/3755881.3755926)，[BibTeX](https://api.crossref.org/works/10.1145%2F3755881.3755926/transform/application/x-bibtex)，正式元数据与开放记录已核 | NL 与辅助上下文生成 SysML 行为模型，检查反馈进入后续生成。 | Paper1 的输入来源；它排除“首个 LLM SysML 行为模型研究”类主张。 | 此环境中 ACM 全文访问受限，细粒度论文说法只限官方标题和已冻结种子材料。 | 仅作为输入 provenance，不把上游检查或分数当预言机。 |
| Santos 等，[Requirements Satisfiability with ICL，RE 2024](https://arxiv.org/abs/2404.12576)，[DOI](https://doi.org/10.1109/RE59067.2024.00025)，[BibTeX](https://api.crossref.org/works/10.1109%2FRE59067.2024.00025/transform/application/x-bibtex)，全文已读，15 页 | LLM 判断文本设计说明是否满足 GDPR 需求。 | 共同点是相对既有制品进行需求层判断；制品不是状态机，数据和评测对象不同。 | 使用合成/法律数据，报告 300 个留出样本；不是可执行状态机证据。 | 可支持相关工作分层，不能用来声称该任务不存在先例。 |
| Endres 等，[nl2postcond，FSE 2024](https://arxiv.org/abs/2310.01831)，[DOI](https://doi.org/10.1145/3660791)，[BibTeX](https://api.crossref.org/works/10.1145%2F3660791/transform/application/x-bibtex)，全文已读，24 页 | NL 意图到可执行后置条件，评测正确性与 mutant-discriminating bug-completeness。 | 可执行行为证据和需求关联都不是 Paper1 独有；其制品是代码而非状态机。 | 文中说明 NL 非形式化，不能保证关联正确；其 bug-completeness 以 mutant 为对象。 | 不宣称“NL 到可执行行为证据”本身新颖。 |
| Liu、Tyszberowicz、Beckert，[Observable Consistency Checking across Requirements and Models，ENASE 2026](https://doi.org/10.5220/0014719400004015)，[作者机构库全文](https://publikationen.bibliothek.kit.edu/1000193552/181929484)，[BibTeX](https://api.crossref.org/works/10.5220%2F0014719400004015/transform/application/x-bibtex)，全文已读，14 页 | 从异构需求和模型抽取可观察量及约束，以本体、检索增强生成和 SMT 检查跨制品一致性。 | 是最强的需求—模型一致性与可执行证据邻项，排除“需求-模型一致性检查尚无人研究”或“LLM 加求解器形成可定位证据尚无人研究”一类说法。 | 它以异构制品共享的可观察量为单位，不是对固定作者状态机的发现报告；全文没有本文的 L/W/D、报告—台账关系或人工有效性协议。其准确率不可与本文指标并列。 | 以具体对象、约束编译和 SMT 一致性检查为相关工作；不写成本文的数值基线或同一任务。 |
| Estivill-Castro 与 Hexel，[ENASE 2026](https://www.scitepress.org/Papers/2026/147167/147167.pdf)，全文已读，10 页 | 将 NL 要求落到 LLFSM 的状态和事件，生成五类模型检查性质并检查执行轨迹一致性。 | NL、状态机、可执行验证和多后端证据都已有直接邻项，不能把这些技术成分的组合写成优先权主张。 | 任务是性质合成与验证，不是对冻结作者模型输出问题报告；其评测单位也不是本文的人工报告—台账关系。 | 只以任务单位和责任边界定位，不把可执行验证本身写为贡献。 |
| Li 与 Zheng，[IET Software 2025](https://doi.org/10.1049/sfw2/6714956)，[BibTeX](https://api.crossref.org/works/10.1049%2Fsfw2%2F6714956/transform/application/x-bibtex)，正式元数据与出版社摘要已核，全文访问受限 | 摘要说明 LLM、NL、UML 活动图/状态机过程一致性、双向需求—测试追踪和反馈闭环。 | 即使全文尚未核验，也足以拒绝“完整组合此前不存在”一类断言。 | 固定模型方向、报告形态、可执行回执和人工协议尚不能从全文核对，不能作细粒度比较或数值对照。 | 保留为直接反证候选；全文可得后再判断能否缩小本文任务差异。 |
| Giannakopoulou 等，[Formal Requirements Elicitation with FRET，REFSQ 2020](https://ceur-ws.org/Vol-2584/PT-paper4.pdf)，[CEUR 入口](https://ceur-ws.org/Vol-2584/)，全文已读 | 受限自然语言需求被形式化、解释、仿真，并映射到模型或代码信号后交给分析工具。 | 需求到可执行形式化、类型化映射和仿真都有既有工具支持。 | 它不以 LLM 对冻结作者状态机作后验问题发现，也不提供本文的报告-台账关系协议。 | 不把“NL 到可执行证据”或“类型化映射”本身写成新颖点。 |
| Fuchß 等，[LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation，ICSE 2025](https://doi.org/10.1109/ICSE55347.2025.00186)，[BibTeX](https://api.crossref.org/works/10.1109%2FICSE55347.2025.00186/transform/application/x-bibtex)，正式元数据与摘要已核，IEEE 全文不可访问 | 使用检索增强生成恢复软件制品间追踪链接。 | 追踪链接恢复是独立研究问题，不能把本文的作者源定位说成首次或通用追踪恢复。 | 当前只能用出版元数据与摘要界定对象；不对其评测协议、可复放性或人工流程作细粒度比较。 | 将本文定位为发现报告回到作者源的归因链，而非通用链接恢复方法。 |
| Huang 等，[Large Language Models Cannot Self-Correct Reasoning Yet，ICLR 2024](https://arxiv.org/abs/2310.01798)，[OpenReview](https://openreview.net/forum?id=IkmD3fKBPQ)，全文已读 | 检验缺少外部反馈时 LLM 对自身推理输出的内在自校正。 | 它直接限制“让同一模型自证候选即可形成可靠真值”的做法。 | 不是状态机或需求-模型任务，不能用于推断本文的命中率、人工协议或证据后端效果。 | 支持将模型候选与人工有效性、关系裁定分开。 |
| André 等，[UML 状态机形式化与模型检查综述，ACM CSUR 2023](https://arxiv.org/abs/2407.17215)，[DOI](https://doi.org/10.1145/3579821)，全文已读，71 页 | UML 状态机的形式化、模型检查翻译和直接操作语义。 | 证明状态机可执行分析已有成熟基础；不处理 NL 到固定作者模型的问题发现。 | 综述记录不同翻译/操作语义的覆盖边界。 | C2 只能声称采用并组织可执行证据，不能声称发明状态机验证。 |
| Wang 等，[LLM-as-a-Judge in SE，ISSTA 2025](https://arxiv.org/abs/2502.06193)，[DOI](https://doi.org/10.1145/3728963)，[BibTeX](https://api.crossref.org/works/10.1145%2F3728963/transform/application/x-bibtex)，全文已读，23 页 | 将 LLM judge 与人工评分比较。 | 提供评测可靠性边界，不是 MDE 方法。 | 结果随任务变化，位置交换后比较结果不稳定。 | 支持把方法候选与人工有效性/关系裁定分开；不把内部审阅称为 inter-rater study。 |

## 新颖性处置

| 候选主张 | 直接反证或重叠 | 最低防守措辞 | 导师决策 |
| --- | --- | --- | --- |
| LLM 对需求与行为模型作自动问题发现 | MCeT 已做最接近的序列图任务，且声称可适配其他建模语言；Liu 等和 Li 与 Zheng处理需求—模型一致性。 | “本文在冻结 PlantUML 案例研究中实例化来源约束的问题发现链路，并将适用的执行回执与人工评测分开保存。” | 是否以任务单位和证据责任定位，而不使用优先权措辞。 |
| LLM 状态机分析 | Sultan 等已有 SysML 状态机 LLM 检测与纠正。 | “任务将 NL 需求与单一作者状态机相对照，而非多视图一致性。” | 确认该差异是否足以作为方法定位。 |
| 状态机追踪与需求覆盖 | de Biase 等已有需求到迁移及 `«satisfy»` 链接。 | “来源定位用于 report-to-source 归因，不将 traceability 本身声明为贡献。” | 无。 |
| 可执行行为证据 | nl2postcond、状态机形式化/模型检查与 Estivill-Castro、Hexel已有。 | “对适用候选保留类型化执行回执，并与人工评测责任分离。” | 仅在逐条 citation 闭合后写入。 |
| LLM 评测可靠性处理 | LLM-as-a-Judge 研究已给出可靠性限制。 | “候选报告不充当自身真值；人工完成有效性和 relation 裁定。” | 无。 |

该矩阵只用于界定共同核心、任务单位、证据责任和可比较性，不能据此推导领域中不存在其他直接工作。本文的经验材料只检验 PlantUML 案例研究中的适配边界；若取得新的全文证据，应据此继续收紧任务差异与新颖性措辞。
