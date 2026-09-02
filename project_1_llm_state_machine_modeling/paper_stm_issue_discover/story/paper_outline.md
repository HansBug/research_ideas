# Paper1 唯一论文大纲

本文件是 Paper1 唯一的规范论文大纲，给出可直接扩写的中文论文正文、表图内容、证据落点和边界。数字来自规范结果归档，谓词资格来自[当前谓词审计](../related_work/provenance/predicate_provenance.md)，直接工作处置来自[最接近工作矩阵](../related_work/closest_work_matrix.md)。

<a id="outline-0"></a>
## 题目与摘要

**暂定题目：** 面向固定源状态机类模型的 L2 问题发现与可执行验证。

**摘要。** 控制系统状态机把需求中的行为约束落实为状态、事件、迁移、守卫和动作。自由文本需求与既有状态机制品之间最难复查的偏差，常常需要跨越多条迁移判断路径、可达性、终止或响应，单个元素的名称比对无法给出充分依据。本文研究自由文本自然语言（natural language，NL）需求与分析期间保持不变、具有来源归属的状态机（state machine，STM）制品之间的定位问题发现。源状态机制品（source-attributed state-machine artifact）可以由人工或上游大语言模型（large language model，LLM）流程产生，本文不生成或修改该输入。

本文提出一个面向状态机类模型的工作流。满足适配器契约的建模语言或制品形式可以接入该工作流；PlantUML 适配器（PlantUML adapter）是本文完成端到端实现与评测的案例。C1 将源制品转换为保留来源归属（provenance）的有限控制状态机（finite control state machine，FCSTM）工作表示，并将确定性检查事实（deterministic inspect facts）送入问题发现阶段。C2 基于领域学术普查归纳的四族 19 条类型化谓词（typed predicate）义务，对适用发现执行后端断言并记录原生执行和回放回执（replay receipt）。报告并列保存问题主张、需求义务、源制品位置、执行证据和人工裁定，使发现与验证的责任边界可以逐项复查。

案例研究包含 9 个自然语言簇中的 54 个输入对、145 条有来源依据的预期问题和 3 轮共 435 个轮次级单元。当前方法/基线（current/baseline）的整体 FULL `hit@1` 分别为 `310/435=71.26%` 和 `227/435=52.18%`；L2 FULL `hit@1` 为 `105/117=89.74%` 和 `50/117=42.74%`。当前方法产生 `1271` 份报告，基线为 `512` 份；报告级有效性精确率分别为 `980/1271=77.10%` 和 `417/512=81.45%`。对 310 个当前方法 FULL-hit 单元，最终 W0/W1/W2 为 `0/142/168`。本案例研究刻画固定 PlantUML 源制品上的发现覆盖、报告有效性与机械确认，结论范围限于该适配器和案例协议。[^fair][^wang2025][^input_selection]

<a id="outline-1"></a>
## 1. 引言

控制系统状态机将需求中的事件、条件和后续行为落实为状态、迁移、守卫与动作。审查者面对的关键问题常常具有行为性质：目标状态是否可达，进入后能否离开，事件是否在轨迹中被消费，反馈能否使系统回到规定状态。原始图文本把层次、连接关系和运行语义交织在一起，难以稳定支撑这类复查；UML 状态机语义与有限状态性质模式提供了相应的形式基础。[^uml251][^dwyer]

本文研究自由文本自然语言需求与一个在分析期间保持不变、带明确来源归属的状态机制品之间的定位问题发现。任务合同为 `<free-form NL requirements, pre-existing source-attributed STM held fixed during analysis> -> localized requirement-relevant issue reports`。输入制品可以由人工或上游大语言模型流程产生，本文既不生成，也不修改该制品。案例研究使用 Wang 等上游流程产生的 54 个 PlantUML 输入对，它们来自 9 个自然语言簇，范围规则排除了并发或秒级时间约束制品。[^wang2025][^input_selection]

已有工作界定了任务的起点。MCeT 从自由文本需求和既有 PlantUML 顺序图生成定位的自然语言问题。Li 与 Zheng 的 IET Software 2025 工作更接近宽泛任务形态：原始需求经结构化与用例规约（use-case specification，UCS）转换后，Algorithm 3 比较 UCS 与既有 UML 状态机，输出定位的 `AbnStepPair`，并在 Web Store 状态机制品上报告实验。因此，本文不主张“自然语言需求加既有状态机到定位问题报告”这一宽泛合同的优先权。[^mcet][^li_zheng]

这一先例由此明确了本文的问题定位。按本文的分析性信息层级，IET 的 Semantic Consistency 比较业务对象的出现与对齐，属于 L0；Process Consistency 比较输入对象与输出对象的局部顺序，属于 L1；State Consistency 检查触发动作的出现与相对顺序，属于 L1，至多位于 L1/L2 边界。IET 原文没有采用 L 分层；其已发表规则和实验未展示跨迁移路径构造或排除、初始状态到目标状态的可达性、无退出死端或终止、轨迹响应、守卫性质或全局交互。[^li_zheng]

L2 问题要求状态机行为论证。台账中的 `EIS-0002-02` 排除到三个目标状态的所有路径，`INS-0002-02` 识别可达 `InitialState` 的无退出行为，`EIS-0029-05` 需要跨层路由推理，`INS-0029-05` 刻画可重复进入终态的非终止行为。这些判断分别需要构造或排除路径、配置与轨迹，局部步骤对的一致性比对不足以决定它们。[^l_tier][^ledger_v2]

本文以两步完成这项工作。C1 构造保留来源的有限控制状态机（FCSTM）工作表示和确定性检查事实，使状态、迁移、守卫、动作、拓扑与运行事实进入 L2 问题发现。C2 将适用发现连接到由领域学术普查归纳的 19 条类型化义务，执行原生后端断言并记录回放回执，同时保持候选发现、机械确认与人工裁定的责任分离。图 1 以 `EIS-0002-02` 的可达性义务为例，从需求引用和固定源状态机开始，展示定位报告如何经类型化计划取得 W1/W2 回执。[^predicate][^ledger_v2]

**图 1：从 L2 可达性义务到定位报告的运行示例。** 图以 `EIS-0002-02` 为唯一例子：需求要求进入三个子状态，固定源制品的入口却把执行引向无后继的 `InitialState`。图中依次标出需求引文、源制品载体、目标集合、类型化查询和回执；读者由此看到一条 L2 结论为何需要路径排除，而不是名称匹配。

本文有两项技术贡献，并以 PlantUML 案例研究评估其结果。第一，C1 通过保留来源的 FCSTM 转换和确定性检查信息增强固定源状态机上的 L2 问题发现。IET 的已发表规则主要处理 L0/L1 一致性，台账中的可达性、死端、跨层路由与非终止实例说明路径和全局行为问题仍需要这类发现信息。第二，C2 将领域学术普查归纳的四族 19 条谓词落实为后端执行语义，对适用发现给出机械确认、来源绑定和回放回执。案例研究报告完整方法与同模型基线的发现覆盖、报告有效性、C2 使用面和失败归因；各项结果均给出分母与适用范围。[^li_zheng][^l_tier][^predicate][^fair]

在 PlantUML 案例研究中，当前方法的整体 FULL `hit@1` 为 `310/435=71.26%`，基线为 `227/435=52.18%`；L2 的 FULL `hit@1` 为 `105/117=89.74%`，基线为 `50/117=42.74%`。当前方法产生更多报告，报告级有效性精确率为 `980/1271=77.10%`，基线为 `417/512=81.45%`。这些数值描述同一案例协议下的发现覆盖与报告有效性。第 6 节把它们与类型化证据、失败归因和费用资格一并解释。[^fair]

<a id="outline-2"></a>
## 2. 背景与相关工作

### 2.1 状态机义务与证据语言

需求相对的状态机检查同时需要领域义务和可执行语义。UML 2.5.1 给出状态、迁移、触发、守卫和动作在模型中的位置；Dwyer 等的性质模式给出响应、缺失和全称等可验证的行为形状；Heimdahl--Leveson 与 Heitmeyer 等说明守卫覆盖、互斥和事件响应如何成为需求分析义务。这些来源界定了应检查的关系。FCSTM 的令牌、抽象语法树、`macrostep` 与 `called()` 是本文的执行定义，其正确性由方法规范和回归测试承担。[^uml251][^dwyer][^heimdahl][^heitmeyer]

表 1 定义本文使用的证据语言。L 描述预期问题成立所需的信息深度，W 描述候选得到的运行时证据，D/A 描述人工审查的事实、义务与归因，`relation` 描述报告和预期问题的对应，K/N/I 则是报告级有效性记账。它们回答不同的问题，任何一个量都不替代另一个量。

**表 1：术语与责任边界。**

| 标签 | 对象 | 取值或单位 | 在本文中的作用 |
| --- | --- | --- | --- |
| `(r,m)` | 自然语言与固定源状态机制品输入对 | 54 个输入对，嵌套于 9 个自然语言簇 | 输入与聚类单位 |
| `L` | 台账信息层级 | `L0/L1/L2` | 预期问题的信息深度 |
| `D/A` | 人工裁定 | `D2/D1/D0/A0` | 事实、义务与归因记录 |
| `W` | 见证强度 | `W0/W1/W2` | 候选的机械证据边界 |
| `relation` | 报告与预期问题的关系 | `FULL/PARTIAL/NONE` | 预期问题上的命中闭合 |
| `K/N/I` | 记账类别 | `K/N/I` | 报告级有效性分子与分母 |

### 2.2 直接先例与方法邻项

本文以四个可观察字段识别直接任务邻项：自由文本 NL 是否为显式输入，既有且固定的状态机是否为显式输入，输出是否为定位的需求相关问题，以及方法是否在状态机制品上实现并评测。MCeT 保留了需求到定位问题的形态，但对象是顺序图。IET 满足四个字段，是宽泛任务形态的直接先例。表 2 将需求中介、问题单位、状态机语义、确定性证据、来源归属和人工责任逐项展开，任务重叠与方法差异因而可以分别判断。[^mcet][^li_zheng]

IET 的三条规则也说明其已展示的检查深度：Semantic Consistency 比较业务对象的存在，Process Consistency 比较局部输入/输出顺序，State Consistency 比较触发动作及其相对顺序。本文依据 IET §5.2 的规则定义和 Algorithm 3 的 `AbnStepPair` 输出，将它们分析性映射为 L0/L1；IET 作者并未采用 L 分类。表 2 将任务重叠与问题深度分开呈现：IET 是宽泛任务先例，而其已发表规则尚未展示路径构造、可达性、终止、轨迹响应、守卫性质和全局交互。[^li_zheng]

Schamai 的工作提供另一种有价值的行为验证路线。它从自然语言需求出发，由需求分析人员将需求与场景形式化，再与系统设计模型组合为仿真验证模型，最后用仿真结果判断需求违反；论文讨论状态机、守卫、事件、层次和死锁。它建立了模型化验证的行为语义基础，但不从原始 NL 与固定源状态机直接产生定位问题报告。与 IET 一起，这条路线说明本文的对象是固定源制品上的 L2 问题发现；本文随后以可执行谓词和后端回放确认适用发现。[^schamai]

GWT、Estivill-Castro 与 Hexel、Sultan 等分别研究状态机补全、自然语言到轻量级有限状态机（Lightweight Finite State Machine，LLFSM）性质合成和多视图不一致修正。FRET、nl2postcond、LiSSA 与状态机验证综述则说明形式化需求、后置条件、追溯恢复和模型检查均有清晰的技术谱系。本文借用这些基础，却不把任何一个组成成分写成首创；它们的作用是解释 C1/C2 的设计选择和解释边界。[^gwt][^estivill][^sultan][^fret][^nl2postcond][^lissa][^uml_survey][^judge]

**表 2：直接工作与行为验证邻项。** 表按对象、输入、输出、问题单位、状态机语义、证据和评测单位比较承重工作。IET 这一行承认宽任务形态的重叠；L 层只按本研究口径分析 IET 已发表规则。

| 工作 | 输入与输出 | 状态机问题深度 | 证据与人工责任 | 与本文的关系 |
| --- | --- | --- | --- | --- |
| MCeT | 自由文本需求与既有 PlantUML 顺序图，输出定位自然语言问题 | 顺序交互，不是状态机行为 | LLM 检查、投票和 authority-based cross-check；评估问题正确性与同根因对应关系 | 保留需求到定位问题的形态，不是 STM 输入任务 |
| IET | 原始需求经 UCS 中介，与既有 UML 状态机比较，输出 `AbnStepPair` | Semantic=L0；Process=L1；State=L1 至多 L1/L2 边界 | 三条业务对象规则和算法；实验报告 Web Store 异常 | 宽泛任务先例；未展示 L2 路径、可达性、终止、响应或全局交互 |
| Schamai | 分析人员形式化需求/场景并组合设计模型，输出仿真验证结果 | 可涉及状态、守卫、事件、层次和死锁 | 模型化仿真验证；不以固定源 STM 的定位报告为输出 | 行为验证邻项，说明 L2 语义已有验证传统 |
| 本文 | 自由文本需求与固定源状态机，输出定位报告及适用的回放回执 | L0/L1/L2；重点发现 L2 行为级问题 | FCSTM 转换和确定性检查增强发现；19 条义务与原生回放确认适用发现；人工 D/A、有效性与对应关系独立记录 | 面向固定源 STM 的 L2 问题发现，并为适用发现提供执行验证 |

表 2 的比较给出本文的定位。IET 使宽泛输入输出合同成为既有工作，Schamai 表明行为验证已有深厚传统；本文处理的是固定源状态机上的 L2 问题发现，并以可执行验证确认其中适用的发现。[^mcet][^li_zheng][^schamai]

<a id="outline-3"></a>
## 3. 问题定义

### 3.1 输入、输出与适用范围

输入对写为 `(r,m)`，其中 `r` 是自由文本需求，`m` 是分析开始前已经存在、在分析中保持不变且具有来源归属的状态机类制品。适配器产生保留载体映射的 FCSTM 投影 `p(m)` 和确定性检查事实 `i(m)`；方法先输出定位发现，再将适用发现写为 `f=(nl_ref, source_ref, obligation, location, evidence)` 的报告。该表示将需求义务、源制品位置、类型化计划和执行证据留在同一可审查报告中，同时保留原始模型的证据地位。本文允许满足适配器合同的状态机类模型进入方法范围；PlantUML 是目前唯一完成适配器合同并进入本研究评测的建模记法，54 个输入对构成该 PlantUML 案例研究。[^input_selection]

台账信息层级（ledger depth，L）的 L0/L1/L2 描述预期问题成立所需的信息范围：L0 是点状或表面对齐性质，L1 是结构或局部状态性质，L2 是跨迁移、路径、可达性、终止、响应或全局交互的行为性质。L 不等同于报告质量、谓词家族、后端或 W。本文的适用范围限于声明的 FCSTM 片段；时钟、不变式、正交区域、并发和混合行为均在该片段之外。有限域、界限、范围和期望占据值只能由当前输入对的需求或源制品事实授权，不能从后端能力反推。[^l_tier]

### 3.2 候选、证据与人工判断

候选发现需要解释自然语言中的指代、义务与关联；确定性编译和后端执行只接受已绑定的 19 条谓词义务。见证强度（witness strength，W）的发表解释遵循下式：

`W2(f) iff F(f) and B(f) and I(f) and Q(f) and E(f)`。

其中，`F` 是受支持片段，`B` 是精确实例绑定，`I` 是 pair/obligation/plan/model/program/receipt 的精确身份链，`Q` 是非空且可核验的需求引文、源引用和绑定引用，`E` 是完成的原生布尔回执。任一条件缺失时，定位明确的候选保留为 W1；定位不足的候选为 W0。谓词与极性元数据另行限定论文可对该回执作出的最强语义主张，例如有限界限结果不能扩展为无界性质证明；它们不把来源绑定且已完成的 Boolean 执行改写为 W1。执行事实、来源归属和 W2 资格分字段保存，因此来源绑定不完整不会把 `completed`、`executed` 或 `true`/`false` 改写为失败。[^predicate]

人工裁定（human adjudication，D/A）、报告有效性和对应关系（relation）由独立评测阶段完成，程序再据此闭合记账类别（bookkeeping category，K/N/I）。这一区分保留机械回执、人工有效性和报告对应关系各自的责任。第 5 节据此给出研究问题、指标和分析单位，第 6 节报告这些指标的结果。

<a id="outline-4"></a>
## 4. 方法

### 4.1 从固定源制品到定位问题报告

图 2 展示端到端方法：`需求 + 固定源状态机 + 转换后的 FCSTM + 检查信息 -> 大语言模型问题发现与定位 -> 适用的类型化谓词绑定 -> FCSTM 后端执行与回放 -> 带 D/W 和回执的问题报告`。C1 覆盖前两步：转换和检查信息为发现阶段补充结构、拓扑和运行信息。C2 覆盖后两步：领域学术普查归纳的 19 条谓词决定可执行义务，后端对适用发现给出机械确认。人工评测独立判断事实、义务和报告对应关系。图中将输入、程序、原生回执和人工字段分置于四条责任泳道，读者可据此追溯每项结论的主体与依据。

**图 2：问题发现与执行验证的责任链。** 图以四条责任泳道呈现固定源状态机、问题发现、确定性程序和人工评测之间的关系：转换与检查信息进入发现阶段，类型化绑定触发适用义务的后端执行，回执与人工裁定共同回到定位报告。责任链将 C1 的发现增强与 C2 的执行验证组织为连续的两个环节。

图 1 使用 `EIS-0002-02` 的运行示例把这条链具体化。需求句授权三个目标状态的可达性义务，源制品中经 `InitialState` 的入口迁移提供定位，类型化计划固定目标集合和查询范围，原生回放给出布尔结果或失败阶段。图 2 再将该例推广到完整流程。输入片段不受支持、绑定不完整、原生加载失败、超时或回放失败时，系统仍保留来源定位和失败阶段，并以 W1/W0 表示证据尚未闭合。源制品问题、投影边界、编译器边界、运行时失败和人工裁定因此具有可区分的归因位置。[^ledger_v2]

### 4.2 C1：保留来源的工作表示与确定性检查事实

C1 通过状态机类模型的适配器把源制品组织为规范源中间表示、FCSTM 和确定性检查事实，同时保留源行、具名载体、所有者路径、伪状态、生命周期动作和迁移来源。状态、事件、迁移、守卫、效果、拓扑和可运行场景由此成为发现阶段可引用的上下文，大语言模型据此提出并定位 L2 路径、可达性、死端/终止、响应和全局交互问题。当前 PlantUML 案例研究中，完整方法相对同模型基线的 overall FULL `hit@1` 为 `310/435=71.26%` 对 `227/435=52.18%`，L2 FULL `hit@1` 为 `105/117=89.74%` 对 `50/117=42.74%`。这些数值支持完整方法在该案例中的端到端发现差异。它们不单独识别转换或确定性检查信息的组件级因果效应。另一种状态机类建模语言或制品形式需重新声明支持片段、来源映射、能力合同和失败处置，才能进入同一方法范围。[^fair]

**表 3：C1/C2 的衔接与 19 条义务概览。** 表 3 将四族义务放回各自的解释范围：`S1--S6` 检查声明与挂接，`G1--G4` 检查图路径，`R1--R4` 检查有限轨迹，`V1--V5` 检查有限域或有限步性质。附录 A 对每条给出精确命题、外部依据、方法语义、实例授权、支持片段和极性资格。[^predicate]

| 家族 | 谓词 | 主要输入 | 论文中的解释范围 |
| --- | --- | --- | --- |
| 结构 | `S1--S6` | 源载体、元素引用、触发/守卫/效果 AST | 声明的 PlantUML 适配器片段 |
| 拓扑 | `G1--G4` | 来源/目标集合、节点或边、图路径 | 图路径及其明确的终止条件 |
| 轨迹 | `R1--R4` | 事件、状态、所有者、有限轨迹窗口 | `macrostep` 与回放定义的运行片段 |
| 有界验证 | `V1--V5` | 守卫组、有限域、steps、稳定配置、期望占据值 | 有限域、界限和极性限定的查询 |

### 4.3 C2：类型化义务、回放与发表解释

C2 将领域分析、真实文献、标准和技术资料的学术普查映射为四族 19 条义务层，并把这些义务应用到 54 个输入对以指导提示和类型化绑定。附录 A 逐条给出每项义务的来源、语义和执行范围。S3/S5 把需求相关的触发集合或守卫相等性与 FCSTM 令牌、抽象语法树相等性分开说明；R1/R3 将事件响应和生命周期义务与 `macrostep`、`called()` 的执行语义分开说明；V1/V2 将守卫互斥或完备性的形式基础与具体有限域的输入绑定分开说明。UML 的槽位定义、性质模式与守卫/事件需求分析文献支撑义务形状，方法规范与测试支撑执行语义，当前需求和源制品支撑实例参数。[^uml251][^dwyer][^heimdahl][^heitmeyer][^predicate]

回执记录查询、绑定输入、范围、界限、布尔结果、轨迹与失败阶段。来源绑定和谓词/极性资格据此限定发表解释。G2 的有界 `must_reach` 支持声明界限内的可达性解释；V4 的叶状态探测只描述其覆盖的状态片段；V5 的 bounded `false` 可构成状态不变式的单向反例，bounded `true` 只说明声明范围内的通过。附录 A 逐条给出这些语义边界。[^predicate]

<a id="outline-5"></a>
## 5. 研究设计

### 5.1 案例研究、比较条件与分析单位

案例研究包含 9 个自然语言簇，每簇 6 个制品，共 54 个输入对；145 条有来源依据的预期问题在 3 轮中形成 435 个轮次级单元。54 表示需求与制品的配对数，不表示 54 个独立需求；435 是同一预期问题的重复观测，并嵌套于输入对、制品和自然语言簇。当前方法与基线共享输入、模型、提示词、轮次和指标定义，比较同一案例协议下的两个运行点。[^wang2025][^input_selection][^fair]

**表 4：案例研究的单位与嵌套关系。** 表 4 将自然语言簇、每簇制品数、输入对、预期问题、轮次与轮次级单元并列，并在正文中限定分母的解释范围。

| 自然语言簇 | 每簇制品 | 输入对 | 预期问题 | 轮次 | 轮次级单元 | 嵌套关系 |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 9 | 6 | 54 | 145 | 3 | 435 | 轮次级单元嵌套于输入对、制品和自然语言簇 |

### 5.2 研究问题、指标与人工协议

本研究提出四个互补的问题。RQ1 询问完整方法相对同模型基线的发现覆盖、报告量和报告级有效性在该案例协议下呈现何种描述性差异。RQ2 询问在保持 PlantUML 到 FCSTM 的转换、模型、提示词、输入对、轮次和 C2 不变时，确定性检查增强能带来何种独立变化；本案例不估计这一组件级增量。RQ3 询问 C2 如何以谓词、绑定和原生回执执行验证适用发现，以及相应的 W 分布为何。RQ4 询问报告归因边界和方法费用如何限定这些结果的解释。

RQ1 使用 FULL `hit@1`、`hit@3`、`hit@all`、报告数和报告级有效性精确率。RQ3 以最终报告、FULL 命中单元、谓词标识和报告绑定行为单位，报告 C2 的执行验证使用面与最终 W 分布。RQ4 以报告和无效报告为单位，说明 K/N/I、D/A、归因边界和费用资格。所有已有指标均在[结果处置清单](./paper_result_inventory.md)中取得正文、附录或排除处置，第 6 节和附录对每个入选指标说明分子、分母与解释范围。

人工评测逐报告完成 D/A、有效性、对应关系与最终确认，程序只根据这些字段闭合 K/N/I。两侧复核的细节不完全对称：当前方法的 v4 源制品优先复审覆盖 1271 条报告，基线由 233 条 non-K 复核报告和 279 条 K 复核报告组成。这一协议提供报告复核记录，但不提供独立双人标注或评审者间一致性证据。

<a id="outline-5-2"></a>
本案例比较评价完整方法相对基线的端到端结果；确定性检查信息的独立组件效应不在本研究的估计范围内。[^fair]

### 5.3 统计解释与费用资格

435 个观测来自 145 条预期问题的三轮重复，并嵌套于 54 个制品和 9 个自然语言簇。本文因此将两臂差异报告为案例研究中的描述性比较，不采用把轮次级单元视为独立同分布样本的总体显著性或因果措辞。[^fair]

费用记录覆盖两侧各 162 个方法单元。当前方法的 `$7.18277320` 记录完整；基线的 `$0.22523328` 缺少一次可计费的模式尝试使用回执，只能作为不完整小计。因此第 6 节只报告已记录费用，不计算成本倍率。[^cost]

<a id="outline-6"></a>
## 6. 结果

### 6.1 RQ1：发现覆盖、报告量与报告级有效性

当前方法的整体 FULL `hit@1` 为 `310/435=71.26%`，基线为 `227/435=52.18%`；按唯一预期问题标识计算，整体 FULL `hit@3` 为 `119/145=82.07%` 对 `106/145=73.10%`，FULL `hit@all` 为 `86/145=59.31%` 对 `46/145=31.72%`。L2 分层的 FULL `hit@1` 为 `105/117=89.74%` 对 `50/117=42.74%`，`hit@3` 为 `37/39=94.87%` 对 `26/39=66.67%`，`hit@all` 为 `33/39=84.62%` 对 `8/39=20.51%`。这些指标分别使用轮次级或唯一预期问题分母，表 5 将其并列而不混用。[^fair][^l_tier]

当前方法输出 `1271` 份报告，基线输出 `512` 份。报告级有效性精确率为 `980/1271=77.10%` 和 `417/512=81.45%`，差异为 `-4.34 pp`。有支撑覆盖的轮次级单元为 `337/435=77.47%` 对 `264/435=60.69%`，唯一预期问题标识覆盖为 `128/145=88.28%` 对 `119/145=82.07%`。图 3 用三部分呈现这一运行点：3a 以发现指标为横轴、百分比为纵轴；3b 比较两侧报告数；3c 比较报告级有效性精确率。图与表表明，在这一案例研究中，更高的发现覆盖伴随更多报告和较低的报告级有效性精确率。[^fair]

**图 3：发现覆盖与报告级有效性的案例研究比较。** 3a 的柱组分别给出整体和 L2 的 FULL 命中；3b 以报告数显示两臂的审查负载；3c 以报告级有效性精确率显示与覆盖增幅同时出现的代价。图不用于显著性推断，所有百分比均在柱旁标出分子和分母。

**表 5：发现与报告的主结果。** 表 5 以整体/L2、指标、当前方法、基线和分母解释组织正文的主比较。

| 层级 | 指标 | 当前方法 | 基线 | 分母与解释 |
| --- | --- | ---: | ---: | --- |
| 整体 | FULL `hit@1` | `310/435=71.26%` | `227/435=52.18%` | 435 个轮次级预期槽位 |
| L2 | FULL `hit@1` | `105/117=89.74%` | `50/117=42.74%` | 39 条 L2 预期问题的 3 轮重复 |
| 整体 | FULL `hit@all` | `86/145=59.31%` | `46/145=31.72%` | 145 条预期问题的三轮全命中 |
| 报告 | 有效性精确率 | `980/1271=77.10%` | `417/512=81.45%` | 报告级 K 或 N / 全部报告 |

**表 6：覆盖细目。** 表 6 区分唯一预期问题与轮次级单元，并将有支撑覆盖与主 FULL 指标分开解释。

| 指标 | 当前方法 | 基线 | 分母与资格 |
| --- | ---: | ---: | --- |
| 整体 FULL `hit@3` | `119/145=82.07%` | `106/145=73.10%` | 唯一预期问题标识 |
| 整体有支撑覆盖 | `337/435=77.47%` | `264/435=60.69%` | 轮次级单元 |
| 整体唯一标识覆盖 | `128/145=88.28%` | `119/145=82.07%` | 唯一预期问题标识 |
| L2 FULL `hit@3` | `37/39=94.87%` | `26/39=66.67%` | 39 条 L2 预期问题标识 |
| L2 FULL `hit@all` | `33/39=84.62%` | `8/39=20.51%` | 39 条 L2 预期问题在 3 轮中均命中 |

RQ1 的答案限于本案例协议：当前方法在整体与 L2 的 FULL 命中上取得更高覆盖，并以更多报告和较基线低 `4.34 pp` 的报告级有效性精确率为代价。表 5 和图 3 将这三项量并列，避免将覆盖差异误读为报告有效性或跨语言效果。

<a id="outline-6-2"></a>
### 6.2 RQ2：确定性检查增强的单独作用

现有案例没有保持转换、模型、提示词、输入对、轮次和 C2 不变的检查信息开关对照。因此，当前方法与基线在 RQ1 中表现出的端到端差异不能单独归因于确定性检查信息。

因此，C1 的端到端发现增益与确定性检查信息的独立增量需要分开解释。前者由本案例结果支持，后者仍缺少组件级对照。[^fair]

<a id="outline-6-3"></a>
### 6.3 RQ3：C2 可执行验证与见证强度

310 个当前方法 FULL 命中单元的最终 W0/W1/W2 为 `0/142/168`。19 个谓词中，`12/19` 有至少一个终止回执，`8/19` 至少绑定一份报告；报告绑定行是 `825/1271=64.91%`。这些指标描述 C2 在案例研究中的执行验证使用面，不估计缺陷覆盖、候选层计划闭合、回放成功率或谓词的边际贡献。[^fair][^predicate]

表 7 将最终 W 分布与谓词、绑定使用面并列呈现。W2 表示适用报告取得了合格机械确认；来源、绑定和身份链使这一确认可复查。G2、V4 和 V5 的回执保留 W2，其可表述结论分别受有限步、叶状态探测和有限范围约束。附录 A 逐谓词给出支持片段与极性解释，附录 C 给出完整结果材料。[^predicate]

**表 7：C2 可执行验证的最终 W 与使用面。**

| 项目 | 当前方法 | 基线 | 论文解释 |
| --- | ---: | ---: | --- |
| FULL-hit 单元 | `310` | `227` | 整体 `hit@1` 的命中单元 |
| 最终 FULL-hit W0/W1/W2 | `0/142/168`（分母 310） | 不适用 | C2 的最终发表 W 主指标 |
| 终止回执谓词标识 | `12/19` | 不适用 | 不同谓词标识 |
| 报告绑定谓词标识 | `8/19` | 不适用 | 不同谓词标识 |
| 报告绑定行 | `825/1271=64.91%` | 不适用 | 当前方法的诊断面 |

RQ3 表明，C2 在案例研究中形成了可执行的类型化计划和原生回执。FULL-hit cells 的最终 W 分布为 `0/142/168`。谓词和极性的语义范围限制最强可表述主张，W 则描述合格机械确认；它们与问题集合、FULL 命中、有效性、D/A、对应关系和 K/N/I 分别承担不同结论。[^predicate]

<a id="outline-6-4"></a>
### 6.4 RQ4：归因边界与费用资格

当前方法的 K/N/I 为 `749/231/291`，基线为 `312/105/95`；D2/D1/D0/A0 为 `721/259/120/171`，基线为 `342/75/85/10`。当前方法的 291 个 I 类报告由 D0 `120`、普通源制品层假阳性 `53` 和非缺陷主张（not-a-defect claim，NADC）`118` 组成。NADC 进一步分为编译器责任 `38`、投影/追踪边界 `24`、运行时/证据闭合 `48` 和归因不确定 `8`，确认仅由 lowering 导致的项为 `0`。该分解只在当前方法一侧存在同构标签，因而用来定位方法边界，不作为跨臂零值。[^attribution]

N 类报告为 `231` 对 `105`，其中 D2/D1 组成是 `38/193` 对 `50/55`，保守的实质性 N 组为 `121` 对 `98`；分组用于附录解释 N 的异质性，不替代报告级精确率分母。表 8 保留报告归因的组成边界，表 9 单独说明费用资格，因此正文不把 `$7.18277320` 与 `$0.22523328` 转化为成本倍率。[^fair][^cost][^attribution]

**表 8：无效报告与归因边界。** 表 8 将 I 类组成、NADC overlay、K/N/I、D/A 和 N 报告组成分开列出，并标出仅能作 current-side diagnostic 的列。

| 项目 | 当前方法 | 基线 | 论文解释 |
| --- | ---: | ---: | --- |
| K/N/I | `749/231/291` | `312/105/95` | 人工字段后的确定性闭合 |
| D2/D1/D0/A0 | `721/259/120/171` | `342/75/85/10` | 复核条件不完全对称 |
| NADC 细分 | `38/24/48/8` | 不适用 | 编译器 / 投影追踪 / 运行时证据 / 归因不确定 |
| 确认仅由降阶导致 | `0` | 不适用 | 不将转换写成精确率差距的主因 |
| N 类报告 | `231` | `105` | D2/D1 为 `38/193` 对 `50/55`；实质性 N 组为 `121` 对 `98` |

**表 9：费用资格。** 当前方法费用完整，基线小计缺少一个可计费 schema-attempt usage receipt，因而本表只给出已记录费用与资格，不生成成本倍率。[^cost]

| 项目 | 当前方法 | 基线 | 费用资格 |
| --- | ---: | ---: | --- |
| 记录费用 | `$7.18277320` | `$0.22523328` | 当前完整；基线为不完整小计 |
| 可报告比较 | 当前方法实际记录额 | 不给可靠倍率 | baseline 缺少一个 billable schema-attempt usage receipt |

RQ4 的答案是归因与费用资格均可审计，但它们承担不同结论。NADC 分解定位当前方法的失败边界，费用表仅报告两臂已记录的资格状态；两者都不支持跨臂成本倍率或生产率结论。

<a id="outline-7"></a>
## 7. 讨论

### 7.1 L2 行为级发现的实践含义

IET 表明业务对象存在、局部顺序和动作对齐可以成为需求与状态模型之间的检查面。本文的 L2 结果覆盖跨迁移路径、可达性、终止和轨迹行为。C1 将图文本中的结构、拓扑和运行事实变成可引用对象，C2 将适用候选落实为可重放的查询与回执。工程师可以沿着需求、源制品载体和证据强度审阅报告，优先处理义务明确、来源清楚且具有可执行证据的候选。[^li_zheng][^l_tier][^predicate]

回执中的模型、查询与程序哈希支持在需求、模型或工具版本变化后复查同一证据计划，并将发现本身与投影、编译器、运行时或证据闭合的失败分开记录。案例研究没有测量审查者工时、用户研究、安全认证或部署收益，因而这些人类和工程结果不在本文的经验结论中。[^attribution]

### 7.2 覆盖、有效性与证据的共同解释

结果将完整方法定位为发现覆盖、报告量和报告级有效性之间存在取舍的案例研究运行点。当前方法在整体和 L2 FULL 命中上高于基线，同时产生更多报告，报告级有效性精确率较基线低 `4.34 pp`。报告覆盖、人工有效性和 W 回答不同问题：K/N/I 反映人工字段后的报告记账，W 表示机械证据。FULL-hit 的最终 W `0/142/168` 说明适用发现中取得合格机械确认的分布。[^fair]

NADC 的 `38/24/48/8` 分解把编译器、投影/追踪、运行时/证据和归因不确定的边界留在结果中，使方法故障不会被直接归于上游源制品。该归因设计为维护者提供了复查路径，也使后续适配器和后端工作能够针对明确的失败位置改进。[^attribution]

“面向状态机”由适配器合同定义：新的状态机类建模语言或制品形式需要声明支持片段、来源映射、规则能力、失败处置和独立评测，才能进入同一方法范围。当前结果刻画完整方法和基线在 PlantUML 案例研究中的端到端差异；确定性检查信息的独立作用仍需组件级对照才能判断。[^fair]

<a id="outline-8"></a>
## 8. 有效性威胁

### 8.1 构念与内部有效性

报告有效性精确率、FULL 对应关系、W 和 K/N/I 对应不同对象。人工保存 D/A、有效性、对应关系与最终确认形成可审计的评测协议，却不构成独立双人盲标、重叠比例或评审者间一致性证据。145 条预期问题也不是状态机缺陷的完整总体，当前方法与基线的端到端差异同时包含工作表示、确定性检查事实和 C2 的可执行验证，不能分解为 C1 或 C2 的独立因果收益。[^fair]

### 8.2 统计、语义与外部有效性

435 个轮次级单元来自 145 条预期问题的三轮重复，并嵌套于 54 个制品和 9 个自然语言簇；本文因此只作案例研究中的描述性比较。G2 的查询范围是声明的有限步，V4 覆盖拓扑可达的叶状态探测，V5 的 `true` 只说明有限范围内的通过，而 `false` 还能构成相应无界不变式的反例。W2 还要求受支持片段、精确实例绑定、完整身份链和可核验的来源引用。[^predicate]

当前实证限于 PlantUML 适配器的声明片段、上游来源归属和本案例研究。相关工作方面，MCeT、IET 与 Schamai 已按全文材料定位，其他工作在矩阵中按正式全文、预印本和访问状态区分。IET 是宽泛任务形态的直接先例；本文关于 L2 空缺的判断限于其已发表规则和实验没有展示路径、可达性、终止、响应和全局交互检查。该比较界定问题深度，不评价 IET 的学术价值，也不将本文的 PlantUML 案例研究推广为跨语言结论。[^mcet][^li_zheng][^schamai][^l_tier]

<a id="outline-9"></a>
## 9. 结论

本文提出并评估一个面向固定源状态机制品的问题发现工作流。它面向满足适配器契约的状态机类模型，并在 PlantUML 适配器上完成案例研究。C1 以保留来源的 FCSTM 工作表示和确定性检查事实增强 L2 问题发现，C2 将适用候选连接到 19 条类型化义务、原生执行与回放回执，并将机械确认与人工有效性、对应关系和记账责任分开。IET 是宽泛任务形态的直接先例。本文的贡献是面向固定源状态机发现路径、可达性、终止、响应和全局交互类 L2 问题，并对适用发现给出可执行验证。[^li_zheng][^predicate]

在 54 个输入对、145 条预期问题和 3 轮的 PlantUML 案例研究中，当前方法的整体与 L2 FULL `hit@1` 分别为 `71.26%` 和 `89.74%`，基线为 `52.18%` 和 `42.74%`；当前方法报告更多，报告级有效性精确率低 `4.34 pp`。这些结果要求将发现覆盖、报告有效性、见证强度和失败归因并列报告，而不把其中任何一个量作为其余量的替代。[^fair][^attribution]

<a id="outline-10"></a>
## 10. 数据可得性

论文的数据与制品声明绑定投稿时的确切提交。该制品提供输入范围、台账、人工裁定、方法实现、谓词注册表、结果汇总和版本标识，使正文中的数字、模型范围与来源归属可以回查。[^fair]

原始输入、台账、人工裁定和结果遵守仓库与数据的既有访问边界。公开材料不包含服务提供方凭据、人工身份资料或未获许可的外部全文；可用制品支持对归档结果、方法版本和既有回执的复查。

<a id="outline-appendix"></a>
## 附录

**附录 A：谓词证据与语义边界。** 按 `S1--S6`、`G1--G4`、`R1--R4`、`V1--V5` 给出 19 行完整表，包括精确命题、逐字引文与定位、方法语义、实例授权、支持片段、`implementation_relation`、逐极性 W2 条件和发表资格。G2、G3、V3、V4、V5 的片段和极性边界，以及来源授权条件在此逐项列出。[^predicate]

**附录 B：输入、适配器与执行合同。** 给出输入闭合、PlantUML 适配器支持片段、来源映射、类型化绑定和失败处置。图 B.1 从一条自然语言义务和固定源制品走到类型化计划、W1/W2 回执与回放轨迹，所有载体保留来源引用而不增加实验统计。

**附录 C：完整结果与归因。** 给出按 L、轮次、预期问题和报告单位分层的完整结果，列出最终 W/谓词使用、I/NADC、N 分组和费用资格。每张附表都包含分子、分母、来源指针和解释范围；G2、V4 和 V5 的有限范围解释与 W2 条件在对应表项中说明。[^fair][^cost][^attribution]

<a id="outline-references"></a>
## 参考文献

[^fair]: v60/current versus X1v2 baseline v3 canonical summary. `final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json`, 2026-09-01. Stable repository artifact.
[^cost]: Paper1 method cost audit v1. `final_results/v60_current_vs_x1v2_baseline/derived/final_talk_cost_section7_v1/cost_summary_v1.json`, 2026-09-01. Stable repository artifact.
[^attribution]: Paper1 conversion-attribution audit v1. `final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/i_attribution_summary_v1.json`, 2026-09-01. Stable repository artifact.
[^predicate]: Paper1 predicate provenance audit. `related_work/provenance/predicate_provenance.md`, 2026-09-02. This points to the audited external primary sources, not to a local citation substitute.
[^uml251]: Object Management Group. *Unified Modeling Language (UML), Version 2.5.1*. 2017. https://www.omg.org/spec/UML/2.5.1/PDF.
[^dwyer]: Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. “Patterns in Property Specifications for Finite-State Verification.” *ICSE*, 1999. https://doi.org/10.1145/302405.302672.
[^heimdahl]: Mats P. E. Heimdahl and Nancy G. Leveson. “Completeness and Consistency in Hierarchical State-Based Requirements.” *IEEE TSE*, 1996. https://doi.org/10.1109/32.508311.
[^heitmeyer]: Constance Heitmeyer, Robert Jeffords, and Bruce Labaw. “Automated Consistency Checking of Requirements Specifications.” *ACM TOSEM*, 1996. https://doi.org/10.1145/234426.234431.
[^mcet]: Khaled Ahmed, Jialing Song, Ou Wei, Bingzhou Zheng, and Boqi Chen. “MCeT: Behavioral Model Correctness Evaluation using Large Language Models.” *MODELS*, 2025, pp. 84--95. https://doi.org/10.1109/MODELS67397.2025.00014; arXiv:2508.00630.
[^sultan]: Bastien Sultan, Ludovic Apvrille, and Sophie Coudert. “On the Consistency of State Machines, Use Cases and Block Diagrams Using Dependency Graphs and Large Language Models.” *Software and Systems Modeling*, 2026, online first. https://doi.org/10.1007/s10270-026-01388-4.
[^li_zheng]: Haibo Li and Lixiao Zheng. “Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework.” *IET Software*, 2025, 2025(1), Article 6714956. https://doi.org/10.1049/sfw2/6714956. Gold OA, CC-BY. The VOR HTML was verified on 2026-09-02 through the publisher-content Google Translate mirror recorded in `related_work/provenance/recovery_log.md`; the DOI remains the canonical citation.
[^schamai]: Wladimir Schamai. *Model-Based Verification of Dynamic System Behavior against Requirements: Method, Language, and Tool*. Linkoping Studies in Science and Technology, Dissertation No. 1547, 2013. https://doi.org/10.3384/diss.diva-98107. Full text verified at http://liu.diva-portal.org/smash/get/diva2:654890/FULLTEXT01.
[^gwt]: Maria Stella de Biase et al. “Completion of SysML State Machines from Given--When--Then Requirements.” *Software and Systems Modeling*, 2024. https://doi.org/10.1007/s10270-024-01228-3.
[^estivill]: Estivill-Castro and Hexel. “Grammar-Prompted Synthesis of Verification Properties from Natural Language Requirements for Multiple Model Checkers.” *ENASE*, 2026. https://www.scitepress.org/Papers/2026/147167/147167.pdf.
[^fret]: Dimitra Giannakopoulou, Anastasia Mavridou, Julian Rhein, Thomas Pressburger, Johann Schumann, and Nija Shi. “Formal Requirements Elicitation with FRET.” *REFSQ 2020 Workshops*, 2020. https://ntrs.nasa.gov/api/citations/20200001989/downloads/20200001989.pdf.
[^lissa]: Fuchß et al. “LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation.” *ICSE*, 2025. https://doi.org/10.1109/ICSE55347.2025.00186.
[^judge]: Wang et al. “LLM-as-a-Judge in Software Engineering.” *ISSTA*, 2025. https://doi.org/10.1145/3728963.
[^nl2postcond]: Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K. Lahiri. “Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions?” *Proceedings of the ACM on Software Engineering*, FSE 2024. https://doi.org/10.1145/3660791; arXiv:2310.01831.
[^uml_survey]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification – A Survey.” *ACM Computing Surveys*, 55(13s), 2023, pp. 1--47. https://doi.org/10.1145/3579821.
[^wang2025]: Yuan Wang, Ning Ge, Jiangxi Liu, Zhilong Cao, Zheping Chen, and Chunming Hu. “Generating SysML Behavior Models via Large Language Models: an Empirical Study.” *Proceedings of the 16th International Conference on Internetware*, ACM, 2025, pp. 366--377. https://doi.org/10.1145/3755881.3755926.
[^input_selection]: Paper1 input provenance: `corpora/seed_library/llms-emp-stm-subset/assets/extracted/feedback_final_validation_summary.json` fixes the 60-row stage/fallback pool; `selected_seed_examples/README.md` fixes the six out-of-scope exclusions and the 54-pair grid; `release_validation/input_closure_preflight.json` records the frozen-input SHA-256 preflight. Accessed 2026-09-02.
[^l_tier]: Paper1 L-tier definition and classification. `discover_matrix/ledger_v2/l_tier.json`, 2026-09-02. The file defines L0/L1/L2 and records the classification basis for each frozen expected issue.
[^ledger_v2]: Paper1 expected-issue ledger. `discover_matrix/ledger_v2/README.md` and `discover_matrix/ledger_v2/ledger.json`, 2026-09-02. The cited identifiers are frozen ledger examples, not additional experimental observations.
