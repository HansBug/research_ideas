# 最接近工作矩阵与领域内主张边界

检索截止日为 2026-09-02。本矩阵围绕唯一任务合同，而不是宽泛的“LLM + formal methods”关键词：

`<free-form NL requirements, pre-existing source-attributed STM held fixed during analysis> -> localized requirement-relevant issue reports`

直接任务候选的二值纳入字段只有四项：`free_form_nl_input`、`pre_existing_fixed_stm_input`、`localized_requirement_relevant_issues`、`implemented_and_evaluated_on_stm`。这四个字段与 R1 盲搜 packet 的精确键名一致。source attribution、native STM semantics 和 replay receipt 是比较字段，不能被用来把满足四字段的工作降到组件层。全文状态只指本轮可复核地取得并逐节阅读的版本；访问受阻不能被当作“无工作”的证据，也不能被本地摘录替代为外部全文证据。

## 检索与处置记录

检索使用 Crossref、OpenAlex、Semantic Scholar、arXiv、DBLP、出版方页、作者/机构库和已收全文，组合查询包括：`("natural language" OR requirements) AND (state machine OR statechart OR STM) AND (issue OR defect OR consistency OR correctness)`、`"behavioral model" requirements issue LLM`、`state machine completion Given When Then`、`state machine property synthesis natural language`。2026-09-02 的 Crossref/DOI 元数据和 2026-07--08 arXiv 查询用于发现候选；标题、摘要或聚合页只用于发现，未被当作细粒度事实来源。后向追引从 MCeT、GWT、Sultan、Estivill、FRET 和 LiSSA 开始，前向追引通过 DOI/OpenAlex locations 检查。去重键为 DOI、arXiv ID、标题和作者年份；纳入标准是与四字段或 C1/C2 组件有实质重叠，排除标准是纯生成、repair、通用代码/协议分析且不处理 STM 输入输出合同。全量 candidate disposition 见下表。

为使解盲复核可以逐 candidate 重放，稳定 ID、发现阶段和 query family 另行列出。下列 query family 使用上段的逐字查询；引用追引项标为 `backward/forward snowballing`，并保留 DOI 或 arXiv ID。candidate 的规范题名只用于显示，不作为去重键。

| 稳定 candidate ID | 发现阶段 | query/citation provenance | 全文与处置落点 |
| --- | --- | --- | --- |
| `arXiv:2604.00275` | `fresh_search` | `"behavioral model" requirements issue LLM`；arXiv ID 作为去重键 | `neighborhood/cards/structure-event-driven-stm-frameworks.md`；全文，预印本，生成任务，rejected as direct task。 |
| `doi:10.1109/ETFA65518.2025` | `fresh_search` | `("natural language" OR requirements) AND (state machine OR statechart OR STM) AND (issue OR defect OR consistency OR correctness)`；DOI 作为去重键 | `neighborhood/cards/etfa2025-stpa-fsm-refinement.md`；accepted author manuscript 与 ETFA 记录，修复既有 FSM，rejected as direct task。 |
| `arXiv:2607.16708` | `fresh_search` | `"behavioral model" requirements issue LLM`；arXiv ID 作为去重键 | RADIANT 的 arXiv 全文与当前矩阵第 26 行；预印本，生成/验证/修复链，rejected as direct task。 |
| `arXiv:2608.14956` | `fresh_search` | `state machine property synthesis natural language`；arXiv ID 作为去重键 | PDEVS/statechart 的 arXiv 全文与当前矩阵第 27 行；预印本，生成 plausible facts 和 statechart，rejected as direct task。 |
| `arXiv:2608.08038` | `fresh_search` | `"behavioral model" requirements issue LLM`；arXiv ID 作为去重键 | `neighborhood/cards/stateful-multiagent-crossview-drift.md`；全文，预印本，跨视图生成/对齐，rejected as direct task。 |
| `arXiv:2607.14162` | `fresh_search` | `state machine completion Given When Then`；arXiv ID 作为去重键 | NL-to-SysMLv2 的 arXiv 全文与当前矩阵第 29 行；预印本，一致性/修复输出，rejected as direct task。 |
| `arXiv:2608.24498` | `fresh_search` | `("natural language" OR requirements) AND (state machine OR statechart OR STM) AND (issue OR defect OR consistency OR correctness)`；arXiv ID 作为去重键 | SeriCrypt 的 arXiv 全文与当前矩阵第 30 行；预印本，协议规范/消息序列，rejected as direct task。 |

| candidate ID | 发现阶段 | 版本与全文状态 | 四字段判定 | 层级与 disposition |
| --- | --- | --- | --- | --- |
| MCeT | existing/fulltext | MODELS 2025 + arXiv v1，全文 | 是 / 否（sequence diagram）/ 是 / 否（无 STM） | 直接问题邻项；不推翻 scoped STM claim，排除“首次行为图 NL evaluation”泛称。 |
| doi:10.1049/sfw2/6714956 | unblind_fulltext | IET Software 2025 VOR，Gold OA CC-BY；2026-09-02 经出版方内容的 Google Translate 镜像取得并逐节阅读全文 | 是 / 是 / 是 / 是。原始 NL 经结构化与 UCS 后进入活动图/状态机一致性流程；Algorithm 3 显式以 UCS 与既有状态机为输入并输出 `AbnStepPair`，实验在 Web Store 状态机制品上报告定位异常。 | 直接任务先例。它排除 Paper1 的完整任务优先权主张；其多制品、UCS 中介与迭代精化任务仍与 Paper1 的固定 source STM、FCSTM 与回执证据设计不同。 |
| Sultan et al. | existing/fulltext | SoSyM 2026，全文 | NL 可在上下文 / 不是固定单一 STM / 输出为多视图 consistency/repair / 评测 SysML | 状态机邻项；任务不是本文合同。 |
| GWT | existing/fulltext | SoSyM 2024，全文 | GWT requirements / 既有 partial STM / 输出新增 transition / 是 | 状态机邻项；completion 修改模型，不输出 issues。 |
| Estivill--Castro--Hexel | existing/fulltext | ENASE 2026，全文 | NL / LLFSM / 输出 synthesized properties / 是 | 状态机邻项；论文评测 property synthesis/SEG，不是运行五个 checker 的 issue verdict。 |
| Liu et al. | existing/fulltext | ENASE 2026，正式全文 | 否 / 否 / 否 / 否。需求与异构模型的 observable/ontology/SMT 一致性，评测为合成需求和汽车案例；图表/多模态制品支持是未来工作。 | 方法成分/一致性邻项；不是状态机制品上的固定输入问题发现。 |
| FRET | existing/fulltext | REFSQ 2020，全文 | 受限 NL / signals-model mapping / formal requirements / 工具评测 | 方法成分先例；不处理 LLM 对固定 STM 的后验问题发现。 |
| nl2postcond | existing/fulltext | 公开预印本，全文 | NL / code contracts / postconditions / 评测代码 | 方法成分先例；对象不是 STM。 |
| LiSSA | existing/fulltext | ICSE 2025，KITopen author version，全文 | software artifacts / trace links / link output / 是 | 方法成分先例；不是 source STM issue discovery。 |
| Structure--Event--STM | fresh_search/fulltext | arXiv:2604.00275v1，预印本，未同行评审 | 是（非结构化 NL）/ 否（从 NL 生成）/ 否（UML 状态机）/ 是 | 状态机邻项；任务是 NL 到 UML 状态机生成，不是保持既有 STM 不变并发现问题。 |
| King--Vyatkin ETFA | fresh_search/fulltext | ETFA 2025 accepted author manuscript，全文 | STPA 约束 / 是（递归修改 FSM）/ 否（修改模型）/ 是 | 状态机邻项；任务是安全约束驱动的模型修复，不输出定位的需求相关问题报告。 |
| RADIANT | fresh_search/fulltext | arXiv:2607.16708，预印本，未同行评审 | 从 requirement model 生成异构模型、RoboChart 行为模型、追溯及 verify-repair | 方法成分先例；不满足固定输入制品字段。 |
| PDEVS/statechart | fresh_search/fulltext | arXiv:2608.14956，预印本，未同行评审 | 从系统描述生成 plausible facts 和 PDEVS statechart；时序自动机对应物由人工事后创建 | 方法成分先例；不满足完整输入输出合同。 |
| CrossView | fresh_search/fulltext | arXiv:2608.08038，预印本，未同行评审 | cross-view generation/alignment | 状态机/行为模型邻项；不是单一固定 STM issue discovery。 |
| NL-to-SysMLv2 conformance | fresh_search/fulltext | arXiv:2607.14162，预印本，未同行评审 | NL-to-SysMLv2 conformance/repair | 状态机邻项；输出不是 localized issue reports。 |
| SeriCrypt | fresh_search/fulltext | arXiv:2608.24498，预印本，未同行评审 | protocol specification 到 CDSL/message sequence | 方法成分先例；对象不是 STM。 |

IET 的 Crossref record 给出 VOR PDF 和 full XML text-mining URLs，DOAJ 标为 Gold OA CC-BY。常规出版社入口和先前的可见浏览器会话曾停在 Cloudflare 验证页；随后以出版方内容的 Google Translate 公共镜像取得约 454 KB 的 VOR HTML，并逐节复核 §3--§8、Algorithm 3 与 §6 实验。该镜像只解决本文阅读与核验，不改变 DOI 作为正式引用入口。取件过程和全文处置见 [recovery log](./provenance/recovery_log.md) 与 [IET card](./neighborhood/cards/iet-software-2025-consistency-traceability.md)。

### 盲搜 candidate ID 的逐项处置

下表保留盲搜 raw record 的六个原始 candidate ID，不用论文简称或规范化 DOI 替换它们。四项布尔判断来自盲搜；解盲后的全文核验只更新 disposition evidence，不回写盲搜判断。`doi:10.1049/sfw2.6714956` 与正文中的 `10.1049/sfw2/6714956` 是同一 DOI 的点号/斜杠显示差异，不能算两个 candidate。

| 原始 candidate ID | 盲搜四字段（NL / fixed STM / localized issues / STM evaluation） | 解盲处置与证据 | 与当前矩阵条目的关系 |
| --- | --- | --- | --- |
| `doi:10.1145/1506216.1506224` | 否 / 否 / 否 / 否 | rejected：Jain 等的对象是自然语言需求文档审查，盲搜可核信息未显示状态机输入、定位的需求相关问题输出或状态机评测；不把全文未取得写成“内容不存在”。 | 组件先例，未另建同义条目。 |
| `doi:10.1109/ASE.2009.48` | 是 / 否 / 否 / 否 | rejected：Deeptimahanti 与 Babar 的标题和题录支持自然语言到 UML 模型生成；其任务不是保持既有状态机不变并输出问题报告。 | 状态机生成邻项，未另建同义条目。 |
| `doi:10.1109/SERA.2007.8` | 否 / 否 / 否 / 否 | rejected：Ng 的题录指向 UML 状态机需求验证，但盲搜可得材料不能确认自由文本需求、分析期间固定的输入状态机、定位问题输出和实证评测四项合同。 | 状态机验证邻项，未另建同义条目。 |
| `doi:10.1007/s10270-024-01228-3` | 否 / 否 / 否 / 否 | rejected：GWT 工作处理受约束的 Given--When--Then 需求并补全状态机；它不是自由文本输入与固定状态机问题发现。当前矩阵的 `GWT` 行是同一 DOI 的规范化别名，全文证据已在该行处置。 | `GWT` 行的 exact-ID alias。 |
| `doi:10.1049/sfw2.6714956` | 是 / 否 / 否 / 否 | accepted as direct challenge after unblind full-text review：IET VOR 全文确认原始 NL、既有状态机、定位的 `AbnStepPair` 和状态机实证评测四项均成立。因此它否定完整输入输出合同的优先权主张；盲搜阶段的摘要级布尔判断保持原样。 | 与 `10.1049/sfw2/6714956` 为同一 DOI 的 exact-ID alias。 |
| `doi:10.1109/QUATIC.2016.021` | 否 / 是 / 否 / 否 | rejected：该工作分析状态机图中的非确定性，但盲搜可核信息未显示自由文本需求输入或需求相关定位输出。 | 状态机分析邻项，未另建同义条目。 |

盲搜原始 record、packet、逐字 query 和候选字段保存在 R1 外部 review bundle；上表是 current-facing 的可读 identity/disposition crosswalk。后续 fresh search 候选均以 DOI 或 arXiv ID 作为稳定 ID，并在其发现行保留精确 query family、全文版本与逐项处置，避免把候选简称当作第二套 key。

## 第一层：直接问题邻项

| 工作 | object、input、output | requirement relation 与 issue unit | evidence、source attribution、human protocol | 与本文的决定性差异 |
| --- | --- | --- | --- | --- |
| Ahmed et al., MCeT | free-style NL + existing PlantUML **sequence diagram**；输出 localized NL issues。 | 三路 holistic/diagram-atom/requirement-atom LLM check，最终报告是 requirements-to-diagram correctness issues。 | parser 只抽 atoms；correctness 和 same-root-cause equivalence 都有人评估。它并非“没有 relation”，本文的差异是 separately recorded validity/relation/ledger protocol，不是首次做 relation 或更高一致性。 | sequence diagram 没有 persistent state、hierarchy、transition/guard/action semantics、reachable configuration 或 state-space quantification。它没有 FCSTM-like executable representation、four-family typed lowering、hash-bound FCSTM-backend replay、W2/W1/W0 或 compiler/runtime/projection failure isolation。它称可适配其他语言，但 threats/conclusion 将其他 behavioral models 留为 future work，未实现和评测 STM task。[^mcet] |
| Li and Zheng | 原始 NL 经结构化与 UCS 转换；Algorithm 3 以 UCS 和既有业务对象 UML 状态机为输入，输出定位的 `AbnStepPair`。 | Rule 1 的业务对象存在/对齐按本文 L 口径为 L0；Rule 2 的输入先于输出为 L1 局部顺序；Rule 3 的 action 存在和相对顺序为 L1，至多位于 L1/L2 边界。该映射是本文分析，不是 IET 原文术语。 | VOR 全文经出版方内容的 Google Translate 镜像逐节核验。流程在一个 Web Store 项目、20 个有效 UCS 和其状态机制品上实施；论文没有公开可执行实现、source-attributed fixed-artifact 协议或原生状态机回执。 | 直接任务先例，排除完整输入输出合同的优先权主张。其规则没有构造执行路径或分析可达性、死锁/终止、事件响应和全局交互；本文针对这类 L2 行为问题，以固定源 STM、可追溯 FCSTM、19 条类型化义务、原生回执和独立 D/A/relation/ledger 责任组织发现。[^li_zheng] |

MCeT 表明不应把主张写成“第一个根据 NL 自动评价行为图”或“第一个输出细粒度问题”。Li--Zheng 已在 VOR 全文中实现并评测原始 NL、既有状态机和定位异常的组合，因此本文不主张完整输入输出合同的优先权。按本文的 L 分层，IET 的 Semantic/Process/State Consistency 分别覆盖 L0、L1 和至多 L1/L2 边界的静态关系。该文没有展示跨多条迁移的路径构造或排除、初始态到目标态的可达性/必达性、无退出死端或终止、运行轨迹中的事件消费/状态保持、守卫互斥或完备、有限步响应/不变式和全局交互检查。`EIS-0002-02` 的不可达状态、`INS-0002-02` 的可达死端、`EIS-0029-05` 的跨层路由和 `INS-0029-05` 的非终止行为正落在这一区间。该映射说明 IET 的真实覆盖边界，并不否定其作为宽泛任务先例的价值。本文的具体增量是将这些 L2 候选组织为固定 source STM 上的来源保存 FCSTM、类型化义务和可回放证据；IET 的确定性 Rule 3 仍是 UCS action 与状态迁移的比较，其流程会结构化和精化需求，也没有本文的 FCSTM 原生回执或分账人工协议。

## 承重工作的全文复核维度

下表是六篇承重工作在全文阅读后的统一处置。它不把任何单一组件差异当作直接工作的排除条件：层级仍由上文四字段决定；表中的语义、证据和人工协议只限定 Paper1 可以写出的 C1/C2 差异。

| 工作 | object、输入、输出与问题单位 | 模型语义与需求关系 | 确定性证据、来源归属与人工协议 | 评测单位、结果与 Paper1 边界 |
| --- | --- | --- | --- | --- |
| MCeT | free-style NL 与既有 PlantUML 顺序图；输出定位的自然语言 correctness issue，问题单位是 requirement-to-diagram discrepancy。 | 顺序图消息与 atom，不含持久状态、层次、transition/guard/action、可达 configuration 或状态空间量化。 | parser 抽取 diagram atoms；语义检查、投票和 authority-based cross-check 由 LLM 完成，没有 native STM execution/replay。作者分别人工评估 issue correctness 与 same-root-cause equivalence。 | 在 FBench/顺序图上评测。它是行为图问题发现先例，但没有实现或评测状态机任务；Paper1 的差异不是“首次有人做 relation”，而是 STM 语义、FCSTM typed lowering、来源绑定回执和 D/A/relation/ledger 的分账。[^mcet] |
| Sultan 等 | SysML 多视图制品、分析图和规格上下文；输出视图间 inconsistency list，并可进入 correction。 | 对象是 use case、state machine、block diagram 等多视图的一致性关系，不是固定单一 source STM 相对一段自由 NL 的问题报告。 | dependency graph、预定义规则和 LLM 协作；没有 source-attributed fixed-artifact contract 或 hash-bound native replay。人工选择/确认纠正，结果分类带主观性。 | 全文案例评测受案例数量限制，作者将更多语言/模型扩展留作后续工作。它限制“LLM 加规则”的组件表述，不满足四字段合同。[^sultan] |
| de Biase 等（GWT） | Given--When--Then 需求和既有部分 SysML 状态机；输出新增 transition、trigger、guard/effect，问题单位是待补全模型元素。 | 需求驱动 state-machine completion，输入模型在流程中被修改。 | 生成/匹配保留需求到新增元素的对应；没有 requirement-relative issue report 的 native replay receipt。 | 两个案例研究验证补全；它是既有状态机制品上的建模邻项，但输出与分析语义都是 model adaptation。[^gwt] |
| Liu 等 | requirements 与异构 models；输出 observable/ontology/SMT consistency judgment，而不是定位的 STM issue。 | 要求是可观测一致性关系，状态机图和多模态制品并非实证输入；全文将图表/多模态支持列为未来工作。 | observable 抽取、ontology harmonisation 与 SMT 求解；没有 source-attributed fixed STM 或人类 relation ledger。 | 评测使用合成需求集与汽车案例。它不是四字段意义上的状态机任务，也不构成 STM-native 回执的比较对象。[^liu] |
| Estivill-Castro 与 Hexel | 自然语言与既有轻量级有限状态机（LLFSM）安排；输出 specification engineering grammar（SEG）与多个模型检查器可接受的性质语法。 | 任务是性质合成，不是让一个冻结 source STM 接受 requirement-relative issue discovery。 | 生成性质文本/语法；论文评估 SEG 与 property synthesis，不是已经运行五个 checker 并逐项报告 verdict/counterexample，也没有 Paper1 的 source-bound replay receipt。 | 22 个 SEG 示例及基准用于合成评测。它约束 NL-to-property 组件优先权，而非完整 issue-discovery 方法。[^estivill] |
| Li 与 Zheng | 原始 NL 经结构化和 UCS 转换；Algorithm 3 输入 UCS 与既有业务对象 UML 状态机，输出定位的 `AbnStepPair`，包括异常 action 与插入位置。 | Rule 1 为 L0 存在/对齐，Rule 2 为 L1 局部顺序，Rule 3 为 L1、至多 L1/L2 边界的 action 存在与顺序。这是 Paper1 的分析性映射；IET 原文未使用 L 分层。其规则不涉及执行路径、可达性、死锁/终止、轨迹响应、守卫检查或全局交互。 | 三条确定性 business-object 规则；没有公开可执行实现、FCSTM projection、typed 19-predicate layer、hash-bound native receipt 或 source-attributed fixed-artifact protocol。人和 LLM 在前序阶段迭代精化 UCS/需求。 | 一个 Web Store 项目，26 个原始 UCS 去重后 20 个有效 UCS；论文报告 `create order`/`convert Shopping Cart to Order` 缺失并定位 UCS 第 2 与第 3 步之间。它满足四字段，是任务优先权的直接先例；Paper1 的可写差异是固定 source STM 上 L2 候选的 C1/C2 证据机制。[^li_zheng] |

## 第二层：状态机或行为模型邻项

| 工作 | 实际任务 | 与本文的共同点 | 不可替代的差异 |
| --- | --- | --- | --- |
| Sultan et al. | SysML 多视图 consistency detection/correction。 | behavioral model、LLM、规则和修正。 | 比较多个视图并修正，不是 NL 与分析中固定 source STM 到 issue reports。[^sultan] |
| de Biase et al. (GWT) | Given--When--Then requirements 驱动 SysML state-machine completion，向既有 states 添加 transitions/triggers/guards/effects。 | NL、critical event-driven systems、pre-existing partial state machine。 | 模型被补全，输出是 model adaptation；不是保留输入模型并报告问题。[^gwt] |
| Estivill-Castro and Hexel | NL 到 LLFSM property synthesis 并以 SEG 评测。 | state machine、NL、可执行 properties。 | output 是 synthesized property；不能误写成五个已运行 checker 的 issue/counterexample results。[^estivill] |
| Liu et al. | requirements 与异构模型的 observable consistency checking。 | requirements/model semantics、ontology 与 SMT consistency。 | 图表与多模态制品支持是未来工作；实证不是 STM artifacts，输出也不是 fixed source STM 的 requirement-relative report。[^liu] |
| Abdulkarim et al. | 非结构化 NL 到 UML 状态机生成，比较单提示、结构驱动、事件驱动和混合策略。 | UML 状态机、NL、结构化中间输出与人工评测。 | 输入不含既有 STM，输出是生成的模型而非问题报告；即使其框架可迁移到其他语言，也没有实现本论文的固定 STM 分析任务。[^structure_event] |
| King and Vyatkin | 将 STPA 控制器约束递归应用于既有 FSM，并生成 IEC 61499 代码。 | 既有状态机制品、NL 约束、控制系统与可执行转换。 | 每轮直接修改上一轮 FSM，输出是修订制品；事后人工把改动评为正/负/中性，方法没有定位 issue report 或对固定源 STM 的评测。[^king_vyatkin] |

## 第三层：方法成分先例

FRET 和 nl2postcond 表明 NL 可以被转成可执行 formal assertion；LiSSA 表明 traceability link recovery 是独立问题；UML state-machine verification 传统说明 graph/SMT/replay 并非本文发明。这些工作分别限制 C1 的 representation/traceability 表述和 C2 的 assertion/replay 组件优先权，但不能由“某个成分已有”推出 `<NL, fixed STM> -> localized issue discovery` 没有领域增量。[^fret][^lissa][^uml_survey]

## 第四层：评测与可靠性来源

MCeT 的 correctness 与 same-root-cause human evaluation、IET 的人工精化、LLM-as-Judge 的自评限制，以及现有 ledger/relation policy 都支持把 report generation、mechanical evidence 和 human validity 分离。本文不将“保存 D/A、relation 和 ledger”描述为首次人工 relation，也不暗示未经测量的 inter-rater reliability。[^mcet][^li_zheng][^judge]

## 冻结的主张

**领域问题。** 本文面向自由文本 NL 与分析期间保持不变、带来源归属的 STM，发现并定位 requirement-relevant issues。STM 是方法层面的语言族；PlantUML 是唯一实现和评测过的 adapter，其 54 个制品只构成技术路线的案例研究。

**当前可写的领域主张。** *We present and evaluate a state-machine-specific workflow that compares free-form natural-language requirements with a pre-existing, source-attributed STM held fixed during analysis and returns localized findings.* 这是具体的任务与方法表述，不是优先权主张。IET 已构成完整输入输出合同的直接先例；按本文的 L 口径，其已发表规则主要覆盖 L0/L1 的存在、局部顺序和 action 对齐，并未展示跨迁移路径、可达性、终止、响应或全局交互的 L2 问题发现。Paper1 的台账覆盖 L0、L1 和 L2；相对 IET 的可写增量是固定 source STM 上 L2 候选的来源保存 FCSTM 工作表示、确定性 inspect augmentation、19 条类型化义务、来源绑定的原生回执和 W 分层。

**C1 wording。** *C1 provides a provenance-preserving executable working representation and deterministic inspect augmentation for the stated task.* 当前证据只支持其在声明的 PlantUML 适配器片段上的实现与案例研究，不识别跨语言语义保持或单独因果增益。

**C2 wording。** *C2 connects applicable candidates to a literature-informed, retrospectively consolidated typed-obligation layer and source-bound FCSTM-backend replay receipts, separating mechanical evidence strength from human validity and relation judgment.* 这套机制为 L2 候选提供可定位、可执行和可回放的证据组织方式，不把任一通用组成成分写成首创。

**不能推出。** 上述主张不宣称完整输入输出任务、LLM、FCSTM conversion、state-machine verification、SMT/model checking、traceability、replay 或人工 adjudication 的 first/only；不宣称所有 STM language 都被实现，或 PlantUML case study 已验证跨语言效果。IET 的全文核验不把其 UCS/活动图/状态机多制品流程等同于本文的 FCSTM 回执方法。

## 引用

[^mcet]: Khaled Ahmed et al. “MCeT: Behavioral Model Correctness Evaluation using Large Language Models.” *MODELS*, 2025, pp. 84--95. https://doi.org/10.1109/MODELS67397.2025.00014; arXiv:2508.00630.
[^li_zheng]: Haibo Li and Lixiao Zheng. “Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework.” *IET Software*, 2025. https://doi.org/10.1049/sfw2/6714956.
[^sultan]: Bastien Sultan, Ludovic Apvrille, and Sophie Coudert. “On the Consistency of State Machines, Use Cases and Block Diagrams Using Dependency Graphs and Large Language Models.” *Software and Systems Modeling*, 2026, online first. https://doi.org/10.1007/s10270-026-01388-4.
[^gwt]: Maria Stella de Biase et al. “Completion of SysML State Machines from Given--When--Then Requirements.” *Software and Systems Modeling*, 2024. https://doi.org/10.1007/s10270-024-01228-3.
[^estivill]: Estivill-Castro and Hexel. “Grammar-Prompted Synthesis of Verification Properties from Natural Language Requirements for Multiple Model Checkers.” *ENASE*, 2026. https://www.scitepress.org/Papers/2026/147167/147167.pdf.
[^liu]: Tianhai Liu, Shmuel Tyszberowicz, and Bernhard Beckert. “Observable Consistency Checking across Requirements and Models.” *ENASE*, 2026. https://doi.org/10.5220/0014719400004015.
[^fret]: Dimitra Giannakopoulou, Anastasia Mavridou, Julian Rhein, Thomas Pressburger, Johann Schumann, and Nija Shi. “Formal Requirements Elicitation with FRET.” *REFSQ 2020 Workshops*, 2020. https://ntrs.nasa.gov/api/citations/20200001989/downloads/20200001989.pdf.
[^lissa]: Fuchß et al. “LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation.” *ICSE*, 2025. https://doi.org/10.1109/ICSE55347.2025.00186.
[^structure_event]: Samer Abdulkarim et al. “Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models.” arXiv:2604.00275v1, 2026. https://arxiv.org/abs/2604.00275. arXiv preprint; not peer-reviewed as of 2026-09-02.
[^king_vyatkin]: Akira King and Valeriy Vyatkin. “LLM-based Iterative Refinement of Finite-State Machines with STPA Controller Constraints and Generation of IEC 61499 Code.” *ETFA*, 2025, pp. 1--8. https://doi.org/10.1109/ETFA65518.2025.11205687. Full text verified from the accepted author manuscript: https://aaltodoc.aalto.fi/bitstreams/9ab39cdd-e8af-4769-a1e6-974595dc7412/download.
[^uml_survey]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification – A Survey.” *ACM Computing Surveys*, 55(13s), 2023, pp. 1--47. https://doi.org/10.1145/3579821.
[^judge]: Wang et al. “LLM-as-a-Judge in Software Engineering.” *ISSTA*, 2025. https://doi.org/10.1145/3728963.
