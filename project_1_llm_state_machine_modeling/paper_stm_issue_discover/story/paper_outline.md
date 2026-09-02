# Paper1 唯一论文大纲

本文件是 Paper1 唯一的规范论文大纲。章节顺序与 PR #196 的 LaTeX 骨架一致；这里给出可直接扩写的中文论文正文、表图内容、证据落点和边界。数字来自 `final_results/v60_current_vs_x1v2_baseline/`，谓词资格来自[当前谓词审计](../related_work/provenance/predicate_provenance.md)，直接工作处置来自[最接近工作矩阵](../related_work/closest_work_matrix.md)。

<a id="outline-0"></a>
## 题目与摘要

**暂定题目：** 面向自然语言需求与既有状态机的可追溯问题发现：PlantUML 案例研究。

**摘要。** 控制系统状态机把需求中的行为约束落实为状态、事件、迁移、守卫和动作；当需求仍是自由文本时，既有模型中的结构与行为偏差难以被稳定定位和复查。本文研究自由文本自然语言（natural language，NL）需求与分析期间保持不变、带来源归属的状态机（state machine，STM）制品之间的问题发现。源状态机制品（source-attributed state-machine artifact）可以由人工或上游大语言模型（large language model，LLM）流水线产生，本文不生成或修改该输入。

本文提出一个面向状态机的工作流，并以 PlantUML 适配器（PlantUML adapter）开展案例研究。C1 将源制品转换为保留来源归属（provenance）的有限控制状态机（finite control state machine，FCSTM）工作表示，并提供确定性检查事实（deterministic inspect facts）。C2 将适用候选连接到四族 19 条类型化谓词（typed predicate）义务，为可机械评估的候选记录原生执行和回放回执（replay receipt）。该结构把候选发现、机械证据和人工裁定置于同一报告中，而不混淆三者的责任。

冻结案例研究包含 9 个自然语言簇中的 54 个输入对、145 条有来源依据的预期问题和 3 轮共 435 个轮次级单元。当前方法/基线（current/baseline）的整体 FULL `hit@1` 分别为 `310/435=71.26%` 和 `227/435=52.18%`；L2 FULL `hit@1` 为 `105/117=89.74%` 和 `50/117=42.74%`。当前方法产生 `1271` 份报告，基线为 `512` 份；报告级有效性精确率分别为 `980/1271=77.10%` 和 `417/512=81.45%`。在 310 个当前方法 FULL 命中单元中，`197` 个最高运行时见证为 W2，`113` 个为 W1。结果表明，该工作流能够在固定 PlantUML 源制品上同时报告发现覆盖、报告有效性和证据强度；其结论限于本案例研究，不估计跨语言效果、审查工时或组件因果效应。[^fair][^wang2025][^input_selection]

图 1 以一个运行示例呈现从需求义务和固定源状态机到定位报告、W1/W2 回执的全过程。图中标出自然语言引用、源载体、类型化计划与回放轨迹，展示报告如何保留可复查依据，不引入新的实验数字。

<a id="outline-1"></a>
## 1. 引言

### 1.1 问题与研究对象

控制系统的状态机把事件驱动行为组织为可执行结构，需求中的遗漏、错误迁移或行为冲突会直接影响后续实现与审查。当前 54 个 PlantUML 制品来自 Wang 等的上游大语言模型生成与反馈流水线：60 行 `feedback-final` 池的 stage/fallback 选择已经冻结，范围规则排除了 6 个包含并发或秒级时间约束的制品。本文将这些制品视为需要分析的源对象，而不将其归为人工创作，也不将问题发现延伸为自动修复。UML 状态机语义和有限状态验证传统已为迁移、守卫、可达性和行为性质提供了清晰的分析基础。[^wang2025][^input_selection][^uml251][^dwyer]

本文的任务合同是 `<free-form NL requirements, pre-existing source-attributed STM held fixed> -> localized requirement-relevant issue reports`。每一份报告指出相关需求、源制品载体和问题位置；当候选可以机械评估时，报告还携带来源绑定的回放证据。该任务关心的是保持不变的单一源状态机制品相对于需求的偏差，因而与模型生成、状态机补全、性质合成、模型修复和多视图一致性形成不同的输入输出关系。

### 1.2 研究空缺与相关工作定位

MCeT 已对自由文本需求与既有 PlantUML 顺序图输出定位的自然语言问题，说明“依据自然语言自动评价任意行为图”不是可写的主张。Li 与 Zheng 的 IET Software 2025 工作进一步构成“自然语言需求加既有状态模型到定位一致性异常”这一宽泛任务形态的直接先例：原始 NL 经结构化和用例规约（use-case specification，UCS）转换后，算法 3 对 UCS 与既有 UML 状态机输出 `AbnStepPair`，并在 Web Store 状态机制品上评测。本文不对这一宽泛任务合同主张优先权。[^mcet][^li_zheng]

IET 的直接先例同时界定了尚待处理的问题深度。按本文的分析性 L 分层，Semantic Consistency 是业务对象的存在与对齐，属于 L0；Process Consistency 检查输入对象先于输出对象出现，属于 L1；State Consistency 检查触发迁移的动作出现与相对顺序，属于 L1，至多处于 L1/L2 边界。IET 原文没有采用这一分类，其规则和实验也没有展示跨迁移路径构造或排除、初始状态到目标状态的可达性、无退出死端、终止、轨迹响应、守卫性质或全局交互检查。本文由此聚焦 L2 行为级候选的证据组织：`EIS-0002-02` 排除到三个目标状态的所有路径，`INS-0002-02` 识别可达 `InitialState` 的无退出行为，`EIS-0029-05` 需要跨层路由推理，`INS-0029-05` 则刻画可重复进入终态导致的非终止行为。[^li_zheng][^l_tier][^ledger_v2]

### 1.3 方法贡献与结果预告

本文的贡献由共享同一 FCSTM 工作表示的 C1 和 C2 构成。C1 提供保留来源的可执行工作表示与确定性检查事实，使候选能够锚定状态、迁移、守卫、动作、拓扑和运行事实。C2 将候选连接到具有来源谱系的类型化义务、原生执行与回放回执，并以 W0/W1/W2 区分证据强度。两者共同构成固定源状态机上的问题发现方法：C1 使模型事实可被稳定引用，C2 使适用候选可获得可执行证据。

实证部分将整体和 L2 的发现覆盖与报告级有效性并列呈现。整体和 L2 的 FULL `hit@1` 分别为 `310/435=71.26%` 与 `105/117=89.74%`，对应基线为 `227/435=52.18%` 和 `50/117=42.74%`；报告级精确率的观察差异为 `-4.34 pp`。这些结果描述完整方法在冻结案例研究中的运行表现，后续章节据此讨论覆盖、报告量和证据强度之间的关系。[^fair]

<a id="outline-2"></a>
## 2. 背景与相关工作

### 2.1 状态机义务与可执行证据的基础

UML 2.5.1 规定状态、迁移、触发、守卫与动作的结构位置；Dwyer 等给出响应、缺失和全称等有限状态性质模式；Heimdahl--Leveson 与 Heitmeyer 等说明守卫覆盖、互斥和事件响应可成为需求分析中的检查义务。本文借用这些文献来说明何种义务具有领域和形式基础，而不把 FCSTM 令牌、抽象语法树、`macrostep` 或 `called()` 等本项目执行语义归为外部标准。[^uml251][^dwyer][^heimdahl][^heitmeyer]

**表 1：术语与责任边界。** 表 1 将输入对、台账信息层级 L、人工裁定 D/A、见证强度 W、报告与预期问题的对应关系以及记账类别 K/N/I 分列。正文以该表避免把“问题需要多少行为信息”“机械证据有多强”与“人工是否认可报告”写成同一变量。

| 标签 | 对象 | 取值或单位 | 在本文中的作用 |
| --- | --- | --- | --- |
| `(r,m)` | 自然语言与固定源状态机制品输入对 | 54 个输入对，嵌套于 9 个自然语言簇 | 输入与聚类单位 |
| `L` | 台账信息层级 | `L0/L1/L2` | 预期问题的信息深度 |
| `D/A` | 人工裁定 | `D2/D1/D0/A0` | 事实、义务与归因记录 |
| `W` | 见证强度 | `W0/W1/W2` | 候选的运行时证据边界 |
| `relation` | 报告与预期问题的关系 | `FULL/PARTIAL/NONE` | 预期问题上的命中闭合 |
| `K/N/I` | 记账类别 | `K/N/I` | 报告级有效性分子与分母 |

### 2.2 直接任务邻项

直接任务邻项按四个字段比较：自由文本 NL 是否是显式输入、既有且在分析中保持不变的状态机是否是显式输入、输出是否为定位的需求相关问题、方法是否已在状态机制品上实现并评测。MCeT 的对象是顺序图，它保留了需求到定位问题的形态，却没有状态机的持久状态、层次、迁移/守卫/动作语义、可达配置或原生状态机回放。IET 满足四字段，因此承担宽泛任务先例的角色；其 UCS 中介、三条业务对象规则、人工精化过程以及缺少来源绑定原生状态机回执，构成与本文的具体比较维度。[^mcet][^li_zheng]

**表 2：直接工作对照。** 表 2 以对象、输入、输出、问题单位、需求关系、状态机语义、确定性证据、来源归属、人工协议和评测单位对照 MCeT、IET 与本文。正文由该表说明两个事实：IET 排除宽泛任务优先权；其 L0/L1 规则没有替代 L2 行为级发现所需的路径、可达性、终止与响应证据。

### 2.3 状态机邻项、方法先例与评测责任

GWT 从 Given--When--Then 需求补全既有 SysML 状态机，输出是新增迁移、触发、守卫或效果；Estivill-Castro 与 Hexel 将自然语言合成为轻量级有限状态机（Lightweight Finite State Machine，LLFSM）的性质文本；Sultan 等分析 SysML 多视图不一致并进入修正。这些工作使用状态机或行为模型，但它们的目标分别是补全、性质合成和多视图修正，而不是在固定源状态机上报告需求相关问题。[^gwt][^estivill][^sultan]

FRET 和 nl2postcond 说明自然语言可以转为可执行形式或后置条件，LiSSA 说明追溯链接恢复是独立任务，状态机验证综述说明转换、模型检查和回放具有既有技术谱系。LLM-as-Judge 文献则支持将生成性判断与人工真值分开。本文据此将这些工作写为 C1/C2 的组成成分先例和评测责任来源，而非把单个组件的相似性当作对状态机问题发现任务的否定。[^fret][^nl2postcond][^lissa][^uml_survey][^judge]

<a id="outline-3"></a>
## 3. 问题定义

### 3.1 输入、输出与适用范围

输入对写为 `(r,m)`，其中 `r` 是自由文本自然语言，`m` 是分析前已存在、带来源归属的状态机。适配器产生保留载体映射的 FCSTM 投影 `p(m)` 与确定性检查事实 `i(m)`；方法输出发现 `f=(nl_ref, source_ref, obligation, location, evidence)`。该表示把需求义务、源制品载体、类型化计划和证据放在一个可审查对象中。PlantUML 是目前唯一完成适配器合同并进入评测的语言，其 54 个输入对构成该技术路线的案例研究。[^input_selection]

台账信息层级（ledger depth，L）的 L0/L1/L2 描述预期问题成立所需的信息范围：L0 是点状或表面对齐性质，L1 是结构或局部状态性质，L2 是跨迁移、路径、可达性、终止、响应或全局交互的行为性质。L 既不表示报告质量，也不等同于谓词、后端或 W。范围明确排除时钟、不变式、正交区域或并发、混合行为及未声明的 FCSTM 片段；当一项义务需要有限域、界限、范围或期望占据值时，这些实例参数由当前输入对中的需求或源制品事实授权。[^l_tier]

### 3.2 候选、证据与人工判断

候选发现可以处理自然语言中的指代、义务与关联。确定性编译和后端执行只接受冻结谓词和已绑定输入，因而把“需要人工解释的候选”与“可机械回放的证据”区分开来。见证强度（witness strength，W）中的 W2 表示在相应受支持片段、精确实例绑定和完整回执下形成的最高运行时证据；W1 保留定位明确但未完成执行或不适用的候选，W0 表示定位不足。人工裁定（human adjudication，D/A）、报告有效性与对应关系（relation）由独立评测阶段完成，程序随后依据这些人工字段闭合记账类别（bookkeeping category，K/N/I）。[^predicate]

这一分工决定了本文的四个研究问题。RQ1 比较完整方法与同模型基线的发现覆盖、报告量和报告级有效性；RQ2 询问保持转换不变时确定性检查增强的单独作用；RQ3 描述类型化证据的使用与最高 W 分布；RQ4 说明失败归因与费用资格。RQ1、RQ3 和 RQ4 使用冻结数据回答，RQ2 的估计对象和对照条件在第 5 节单独固定。

<a id="outline-4"></a>
## 4. 方法

### 4.1 从固定源制品到问题报告的证据链

图 2 展示端到端方法：`NL + fixed source STM -> provenance-preserving FCSTM projection + inspect facts -> candidate discovery and binding -> typed predicate plan -> FCSTM-backend execution/replay -> W evidence -> source-attributed report`。图中将大语言模型、确定性程序和人工评测分别着色：大语言模型提出和定位候选，程序提取事实、编译并回放适用义务，人工评测判断事实、义务和报告对应关系。该图解释为什么同一报告可以同时带有自然语言定位、源制品定位和机械证据，而不会把任何一层写成另一层的替代物。

当输入片段不受支持、绑定不完整、原生加载失败、超时或回放失败时，系统保留来源定位和失败阶段，并以 W1/W0 表示证据尚未闭合。这样，源制品问题、投影边界、编译器边界、运行时失败和人工裁定具有可区分的归因位置。该安排也使结果章节能够把问题发现、报告有效性和方法边界分别统计。

### 4.2 C1：保留来源的工作表示与确定性检查事实

C1 在 PlantUML 案例研究中把源制品组织为规范源中间表示、FCSTM 和确定性检查事实，同时保留源行、具名载体、所有者路径、伪状态、生命周期动作和迁移来源。状态、事件、迁移、守卫、效果、拓扑和可运行场景由此成为候选的可引用上下文，大语言模型无需仅靠原始图文本猜测结构。对于另一种状态机语言，等价的适配器必须重新声明支持片段、来源映射、能力合同和失败处置，才能进入方法范围。

**表 3：C1/C2 的衔接与 19 条义务概览。** 表 3 以四行概括结构、拓扑、轨迹和有界验证四族的输入与解释范围：`S1--S6` 检查声明与挂接，`G1--G4` 检查图路径，`R1--R4` 检查有限轨迹，`V1--V5` 检查有限域或有限步性质。附录 A 给出每一条的精确命题、外部依据、方法语义、实例授权和极性资格。[^predicate]

| 家族 | 谓词 | 主要输入 | 论文中的解释范围 |
| --- | --- | --- | --- |
| 结构 | `S1--S6` | 源载体、元素引用、触发/守卫/效果 AST | 声明的 PlantUML 适配器片段 |
| 拓扑 | `G1--G4` | 来源/目标集合、节点或边、图路径 | 图路径及其明确的终止条件 |
| 轨迹 | `R1--R4` | 事件、状态、所有者、有限轨迹窗口 | `macrostep` 与回放定义的运行片段 |
| 有界验证 | `V1--V5` | 守卫组、有限域、steps、稳定配置、期望占据值 | 有限域、界限和极性限定的查询 |

### 4.3 C2：类型化义务、回放与发表解释

C2 将候选连接到文献启发、事后整合的义务层。S3/S5 把需求相关的触发集合或守卫相等性与 FCSTM 令牌、抽象语法树相等性分开说明；R1/R3 将事件响应和生命周期义务与 `macrostep`、`called()` 的执行语义分开说明；V1/V2 将守卫互斥或完备性的形式基础与具体有限域的输入绑定分开说明。UML 的槽位定义、性质模式与守卫/事件需求分析文献支撑义务形状，方法规范与测试支撑执行语义，当前需求和源制品支撑实例参数。[^uml251][^dwyer][^heimdahl][^heitmeyer][^predicate]

回执记录模型、查询和程序哈希、绑定输入、范围、界限、布尔结果、轨迹与失败阶段。W2 的发表解释随谓词和极性而变化：G2 的有界 `must_reach` 不承担无界最终可达的解释；V4 的叶状态探测不承担所有可达稳定配置的无死锁解释；V5 的 bounded `false` 可以作为状态不变式的单向反例，bounded `true` 不承担无界证明。附录 A 据此列出 G2 的 2 条、V4 的 88 条和来源授权未闭合的 125 条历史 W2 的发表级排除，同时保留冻结的报告、W 与 headline 指标。[^predicate]

<a id="outline-5"></a>
## 5. 研究设计

### 5.1 案例研究、比较条件与分析单位

案例研究包含 9 个在用自然语言簇，每簇 6 个制品，共 54 个输入对；145 条有来源依据的预期问题在 3 轮中形成 435 个轮次级单元。54 表示需求与制品的配对数，不表示 54 个独立需求；435 是同一预期问题的重复观测，并嵌套于输入对、制品和自然语言簇。当前方法与基线共享冻结输入、模型、提示词/配置、轮次和指标定义，比较因而描述同一案例协议下的两个运行点。[^wang2025][^input_selection][^fair]

**表 4：案例研究的单位与嵌套关系。** 表 4 将自然语言簇、每簇制品数、输入对、预期问题、轮次与轮次级单元并列，并在正文中限定分母的解释范围。

| 自然语言簇 | 每簇制品 | 输入对 | 预期问题 | 轮次 | 轮次级单元 | 嵌套关系 |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 9 | 6 | 54 | 145 | 3 | 435 | 轮次级单元嵌套于输入对、制品和自然语言簇 |

### 5.2 研究问题、指标与未运行的成对实验

RQ1 使用 FULL `hit@1`、`hit@3`、`hit@all`、报告数和报告级有效性精确率描述端到端发现表现。RQ3 以 FULL 命中单元、谓词标识和报告绑定行为单位，报告最高 W、回执与绑定使用。RQ4 以报告和无效报告为单位，说明 K/N/I、D/A、归因边界和费用资格。所有现有指标均已在[结果处置清单](./paper_result_inventory.md)中被列为正文、附录或排除项，并在第 6 节或附录中解释其分子、分母和边界。

<a id="outline-5-2"></a>
#### RQ2 的投稿前成对实验

RQ2 的估计对象不同：在固定 PlantUML 到 FCSTM 转换、模型、提示词、输入对、轮次和 C2 的条件下，只切换确定性检查增强，并在成对预期问题轮次槽位上比较 FULL 命中、报告数和报告级精确率。该问题唯一对应 `TODO-EXPERIMENT-01`；冻结归档没有这组开/关条件，因此本文不从当前方法/基线的端到端差异推断 C1 的单独因果作用。该实验阻塞论文投稿，不阻塞当前 R1 的故事合同。[^fair]

### 5.3 人工协议、统计解释与费用资格

人工评测逐报告完成 D/A、有效性、对应关系与最终确认，程序基于这些已完成字段确定性闭合 K/N/I。两侧复核的细节并不完全对称：当前方法的 v4 源制品优先复审覆盖 1271 条报告，基线由 233 条 non-K 复核报告和 279 条冻结 K 报告组成。435 个观测又具有重复和嵌套结构，因此结果使用案例研究中的描述性比较，不采用独立同分布样本的总体显著性或因果措辞。[^fair]

费用审计覆盖两侧各 162 个方法单元。当前方法的 `$7.18277320` 是完整记录；基线的 `$0.22523328` 缺少一个可计费的 `schema-attempt usage receipt`，只能作为不完整小计。该资格差异决定第 6 节报告已记录费用，而不计算成本倍率。[^cost]

<a id="outline-6"></a>
## 6. 结果

### 6.1 RQ1：发现覆盖、报告量与报告级有效性

当前方法的整体 FULL `hit@1` 为 `310/435=71.26%`，基线为 `227/435=52.18%`；按唯一预期问题标识计算，整体 FULL `hit@3` 为 `119/145=82.07%` 对 `106/145=73.10%`，FULL `hit@all` 为 `86/145=59.31%` 对 `46/145=31.72%`。L2 分层的 FULL `hit@1` 为 `105/117=89.74%` 对 `50/117=42.74%`，`hit@3` 为 `37/39=94.87%` 对 `26/39=66.67%`，`hit@all` 为 `33/39=84.62%` 对 `8/39=20.51%`。这些指标分别使用轮次级或唯一预期问题分母，表 5 将其并列而不混用。[^fair][^l_tier]

当前方法输出 `1271` 份报告，基线输出 `512` 份。报告级有效性精确率为 `980/1271=77.10%` 和 `417/512=81.45%`，差异为 `-4.34 pp`。有支撑覆盖的轮次级单元为 `337/435=77.47%` 对 `264/435=60.69%`，唯一预期问题标识覆盖为 `128/145=88.28%` 对 `119/145=82.07%`。图 3 以三部分呈现这些观察：3a 的横轴为发现指标、纵轴为百分比；3b 给出两侧报告数；3c 给出报告级有效性精确率。图与表共同说明，在该冻结案例研究中，更高的发现覆盖伴随更多报告和较低的报告级精确率。[^fair]

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
| L2 FULL `hit@all` | `33/39=84.62%` | `8/39=20.51%` | 39 L2 IDs across 3 rounds |

### 6.2 RQ3：类型化证据与见证强度

310 个当前方法 FULL 命中单元的最高 W 为 `0/113/197`，基线的对应分布为 `0/227/0`。这一差异说明当前方法具有类型化回执和运行时证据面，并不评价基线报告的语义有效性。19 个谓词中，`12/19` 有至少一个终止回执，`8/19` 至少绑定一份报告；报告绑定行是 `825/1271=64.91%`，其中旧覆盖标记为 `303/825=36.73%`。这些都是使用与绑定诊断，不代表缺陷覆盖、候选层计划闭合、回放成功率或谓词的边际贡献。[^fair][^predicate]

**表 7：证据使用与发表解释。** 表 7 报告命中分母、最高 W、终止回执与报告绑定谓词标识，并将运行时记录与发表解释分开。G2 的 2 条、V4 的 88 条以及来源授权未闭合的 125 条历史 W2 保留在冻结记录中，却不承载相应的更强发表级解释；附录 A 按谓词、片段和极性给出原因。[^predicate]

| 项目 | 当前方法 | 基线 | 解释边界 |
| --- | ---: | ---: | --- |
| FULL-hit 分母 | `310` | `227` | 整体 `hit@1` 的命中单元 |
| 最高 W0/W1/W2 | `0/113/197` | `0/227/0` | 运行时见证，不等于人工有效性 |
| 终止回执谓词标识 | `12/19` | 不适用 | 不同谓词标识 |
| 报告绑定谓词标识 | `8/19` | 不适用 | 不同谓词标识 |
| 报告绑定行 | `825/1271=64.91%` | 不适用 | 当前方法的诊断面 |
| 旧覆盖标记/绑定行 | `303/825=36.73%` | 不适用 | 绑定行子集诊断 |

<a id="outline-6-3"></a>
### 6.3 RQ4：归因边界与费用资格

当前方法的 K/N/I 为 `749/231/291`，基线为 `312/105/95`；D2/D1/D0/A0 为 `721/259/120/171`，基线为 `342/75/85/10`。当前方法的 291 个 I 类报告由 D0 `120`、普通源制品层假阳性 `53` 和非缺陷主张（not-a-defect claim，NADC）`118` 组成。NADC 进一步分为编译器责任 `38`、投影/追踪边界 `24`、运行时/证据闭合 `48` 和归因不确定 `8`，确认仅由 lowering 导致的项为 `0`。该分解只在当前方法一侧存在同构标签，因而用来定位方法边界，不作为跨臂零值。[^attribution]

N 类报告为 `231` 对 `105`，其中 D2/D1 组成是 `38/193` 对 `50/55`，保守的 substantive N groups 为 `121` 对 `98`；分组用于附录解释 N 的异质性，不替代报告级精确率分母。表 8 保留报告归因的组成边界，表 9 单独说明费用资格，因此正文不把 `$7.18277320` 与 `$0.22523328` 转化为成本倍率。[^fair][^cost][^attribution]

**表 8：无效报告与归因边界。** 表 8 将 I 类组成、NADC overlay、K/N/I、D/A 和 N 报告组成分开列出，并标出仅能作 current-side diagnostic 的列。

| 项目 | 当前方法 | 基线 | 论文解释 |
| --- | ---: | ---: | --- |
| K/N/I | `749/231/291` | `312/105/95` | 人工字段后的确定性闭合 |
| D2/D1/D0/A0 | `721/259/120/171` | `342/75/85/10` | 复核条件不完全对称 |
| NADC 细分 | `38/24/48/8` | 不适用 | 编译器 / 投影追踪 / 运行时证据 / 归因不确定 |
| 确认仅由降阶导致 | `0` | 不适用 | 不将转换写成精确率差距的主因 |
| N reports | `231` | `105` | D2/D1 为 `38/193` 对 `50/55`；substantive groups 为 `121` 对 `98` |

**表 9：费用资格。** 当前方法费用完整，基线小计缺少一个可计费 schema-attempt usage receipt，因而本表只给出已记录费用与资格，不生成成本倍率。[^cost]

| 项目 | 当前方法 | 基线 | 费用资格 |
| --- | ---: | ---: | --- |
| 记录费用 | `$7.18277320` | `$0.22523328` | 当前完整；基线为不完整小计 |
| 可报告比较 | 当前方法实际记录额 | 不给可靠倍率 | baseline 缺少一个 billable schema-attempt usage receipt |

<a id="outline-7"></a>
## 7. 讨论

### 7.1 L2 行为级发现的实践含义

IET 表明业务对象存在、局部顺序和动作对齐可以成为需求与状态模型之间的有效检查面。本文的 L2 结果表明，状态机维护还需要处理跨迁移路径、可达性、终止和轨迹行为。C1 将图文本中的结构、拓扑和运行事实变成可引用对象，C2 将适用候选落实为可重放的查询与回执。工程师因而可以从需求、源制品载体和证据强度共同查看问题报告，优先处理具有明确义务、来源归属和可执行证据的候选。[^li_zheng][^l_tier][^predicate]

这一工作流能力不等同于已测得的生产率或安全收益。本文没有审查者工时、用户研究、安全认证或部署数据，但回执中的模型、查询与程序哈希支持在需求、模型或工具版本变化后复查同一证据计划，并区分发现本身与投影、编译器、运行时或证据闭合的失败。[^attribution]

### 7.2 覆盖、有效性与证据的共同解释

结果中的主要张力是发现覆盖、报告量与报告级精确率并未沿同一方向变化。当前方法在整体和 L2 FULL 命中上高于基线，同时产生更多报告，报告级有效性精确率低 `4.34 pp`。这一观察要求报告覆盖、人工有效性和 W 分布并列呈现：W2 说明适用候选具有较强的运行时证据，不能替代人工有效性；K/N/I 说明人工字段后的报告账，不能替代问题深度。[^fair]

NADC 的 `38/24/48/8` 分解把编译器、投影/追踪、运行时/证据和归因不确定的边界留在结果中，使方法故障不会被直接归于上游源制品。该归因设计为维护者提供了复查路径，也使后续适配器和后端工作可以针对明确的失败位置改进。[^attribution]

<a id="outline-7-3"></a>
### 7.3 可推广架构与后续实证

“面向状态机”描述的是适配器合同，而不是已经完成跨语言实证。任何新语言需要声明其支持片段、来源映射、规则能力、失败处置和独立评测，才能进入同一方法范围。对 C1 的单独因果作用，现有归档只支持完整方法与基线的端到端比较；`TODO-EXPERIMENT-01` 为投稿前的成对开/关研究固定了对象、对照、单位、分母和指标。[^fair]

<a id="outline-8"></a>
## 8. 有效性威胁

### 8.1 构念与内部有效性

报告有效性精确率、FULL 对应关系、W 和 K/N/I 对应不同对象。人工保存 D/A、有效性、对应关系与最终确认形成可审计的评测协议，却不构成独立双人盲标、重叠比例或评审者间一致性证据。145 条预期问题也不是状态机缺陷的完整总体，当前方法与基线的端到端差异同时包含工作表示、确定性检查事实和类型化证据层，不能分解为 C1 或 C2 的独立因果收益。[^fair]

### 8.2 统计、语义与证据解释

435 个轮次级单元来自 145 条预期问题的三轮重复，并嵌套于 54 个制品和 9 个自然语言簇；本文因此只作案例研究中的描述性比较。G2 的 2 条历史 W2 缺少无界完整性或环路论证，V4 的 88 条历史 W2 未覆盖所有可达稳定配置，另有 125 条历史 false W2 缺少当前合同要求的来源授权闭合。V5 的 bounded `false` 具有单向反例意义，bounded `true` 不承担无界不变式证明。这些限制收窄发表解释，不改变冻结的 W、报告或 headline 指标。[^predicate]

### 8.3 外部有效性与相关工作边界

当前实证限于 PlantUML 适配器的声明片段、上游来源归属和冻结案例研究。相关工作方面，MCeT 与 IET 已完成全文核验，其他工作在矩阵中按正式全文、预印本和访问状态区分。IET 是宽泛任务形态的直接先例；本文关于 L2 空缺的判断限于其已发表规则和实验没有展示路径、可达性、终止、响应和全局交互检查。这一比较说明问题深度的差异，不评价 IET 的学术价值。[^mcet][^li_zheng][^l_tier]

<a id="outline-9"></a>
## 9. 结论

本文提出并评估一个面向固定源状态机制品的问题发现工作流。C1 以保留来源的 FCSTM 工作表示和确定性检查事实组织模型语义，C2 将适用候选连接到 19 条类型化义务、原生执行与回放回执，并把机械证据与人工有效性、对应关系和记账责任分开。IET 是宽泛任务形态的直接先例；本文的具体贡献是为 L2 行为级候选提供可追溯、可执行、可回放的证据组织。[^li_zheng][^predicate]

在 54 个输入对、145 条预期问题和 3 轮的 PlantUML 案例研究中，当前方法的整体与 L2 FULL `hit@1` 分别为 `71.26%` 和 `89.74%`，基线为 `52.18%` 和 `42.74%`；同时，当前方法报告更多，报告级有效性精确率低 `4.34 pp`。这些结果支持将发现覆盖、报告有效性、见证强度和失败归因作为相互关联但不可互相替代的证据维度来报告。[^fair][^attribution]

<a id="outline-10"></a>
## 10. 数据可得性

论文的数据与制品声明绑定投稿时的确切提交，并列出 `final_results/v60_current_vs_x1v2_baseline/archive_manifest.json`、`publication_manifest.json`、`derived/fair_comparison_v4/combined_summary_v4.json`、当前/基线决策文件、复算脚本、方法代码、`predicate_registry.json` 的版本和 SHA-256，以及输入/输出模式和来源归属。读者可在该提交上运行归档校验器、`build_current_reaudit_v4.py --validate-only` 和 `recompute_fair_comparison_v4.py --validate-only`，正文数字均回指规范汇总。[^fair]

原始输入、台账、人工裁定和结果遵守仓库与数据的既有访问边界。公开材料不包含服务提供方凭据、人工身份资料或未获许可的外部全文；可复算材料覆盖归档完整性、不调用服务提供方的汇总和既有回执审查，不承诺重放外部服务调用或生成与冻结运行完全相同的新输出。

<a id="outline-appendix"></a>
## 附录

**附录 A：谓词证据与语义边界。** 按 `S1--S6`、`G1--G4`、`R1--R4`、`V1--V5` 给出 19 行完整表，包括精确命题、legacy/current 双向承接、逐字引文与定位、方法语义、实例授权、支持片段、`implementation_relation`、逐极性 W2 条件和发表资格。G2、G3、V3、V4、V5 的片段和极性边界，以及 125 条来源授权排除，在此逐项列出。[^predicate]

**附录 B：输入、适配器与执行合同。** 给出输入闭合、PlantUML 适配器支持片段、来源映射、类型化绑定和失败处置。图 B.1 从一条自然语言义务和固定源制品走到类型化计划、W1/W2 回执与回放轨迹，所有载体保留来源引用而不增加实验统计。

**附录 C：完整结果、归因与复算入口。** 给出按 L、轮次、预期问题和报告单位分层的完整结果，列出 W/谓词使用、I/NADC、N 分组、费用资格与制品哈希。每张附表都包含分子、分母、来源指针和解释范围；G2 的 2 条、V4 的 88 条与 125 条来源授权未闭合历史 W2 的发表解释排除列为附录修正。[^fair][^cost][^attribution]

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
