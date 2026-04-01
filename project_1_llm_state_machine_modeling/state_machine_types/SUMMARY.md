# Project 1 State Machine Types Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_types/` 的总账，用于记录当前已经正式入账的状态机类型论文、综述类论文、统一分类口径、关键词簇和更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 若任务涉及普通条目，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 若任务涉及综述条目，再读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
5. 最后使用本文件查看统计、双表总账、关键词簇和待补方向。

## 当前收录统计

- 已收录普通类型论文：**0** 篇
- 已收录综述类论文：**10** 篇
- 本轮新增论文：**5** 篇
- 已完成 `desc.md`：**0** 篇
- 已完成 `survey.md`：**10** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮工作：新增 5 篇 `🧱 模型本体` survey，补入 `Two-Dimensional / Cellular / Tree / Multi-Tape / Weighted Automata` 五条离散 automata 支线

## 形式主义主类口径

右侧数量统计当前正式入账条目中涉及该主类的次数：普通论文按 `主类` 计数，综述论文按 `覆盖主类` 中出现的每个 emoji 分别计数。

| Emoji | 主类 | 范围 | 数量 |
|---|---|---|---:|
| 🧩 | 经典离散状态机 | `FSM`、`EFSM`、`Statechart`、`UML State Machine`、`SCXML`、`Tree Automata`、`Multi-Tape Automata`、`Two-Dimensional Automata`、`Cellular Automata`、`Weighted Automata` 等 | 7 |
| ⏱️ | 时间/时钟自动机 | `Timed Automata`、`Timed Statecharts`、`TIOA` 等 | 2 |
| 🌊 | 混成/随机扩展 | `Hybrid Automata`、概率/随机自动机、随机混成扩展等 | 1 |
| 🕸️ | Petri 网与并发网模型 | `P/T Net`、`Colored Petri Net`、`Timed Petri Net`、高层网等 | 1 |
| 🔌 | 接口/组合/契约模型 | `I/O Automata`、`Interface Automata`、`Contract Automata`、组合行为模型等 | 0 |
| 📦 | 标准、交换格式与执行载体 | `SCXML`、`PNML`、`UML/XMI`、专用 DSL、元模型、交换标准等 | 3 |

## 描述客体口径

右侧数量统计当前普通论文总表中的 `客体` 条目总数。

| Emoji | 描述客体 | 含义 | 数量 |
|---|---|---|---:|
| 📝 | 序列 / 语言对象 | 主要描述字符串、事件序列、trace、多串关系等离散序列对象 | 0 |
| 🌳 | 树 / 文档对象 | 主要描述树结构、XML 文档、层次内容或其他树形对象 | 0 |
| 🖼️ | 网格 / 图案对象 | 主要描述二维 tape、图片、网格或格点对象 | 0 |
| 🎛️ | 控制 / 反应式逻辑 | 主要描述控制器、反应式行为、事件驱动控制逻辑 | 0 |
| 🤝 | 接口 / 交互契约 | 主要描述协议、组件交互、会话、接口或契约对象 | 0 |
| 🏭 | 并发过程 / 资源流 | 主要描述并发过程、工作流、token/资源流网络 | 0 |
| 🌡️ | 物理 / 混成对象 | 主要描述物理装置、连续动力学对象或混成/CPS 对象 | 0 |

## 所属领域口径

右侧数量统计当前普通论文总表中的 `领域` 条目总数。

| Emoji | 所属领域 | 含义 | 数量 |
|---|---|---|---:|
| 🧮 | 形式语言与自动机理论 | 主要是 automata theory、formal language、语义与判定性研究 | 0 |
| 💻 | 软件建模与程序行为 | 主要面向软件状态、程序行为、反应式软件或模型驱动开发 | 0 |
| 📄 | 文档与数据交换 | 主要面向 XML、schema、文档结构与数据交换 | 0 |
| ⏱️ | 实时与嵌入式系统 | 主要面向实时、调度、时序约束和嵌入式执行 | 0 |
| 🏭 | 工业控制与自动化 | 主要面向控制工程、自动化系统和工业逻辑 | 0 |
| 🌐 | 协议 / 分布式 / 交互系统 | 主要面向通信协议、服务交互、接口组合与分布式行为 | 0 |
| 🌡️ | CPS / 物理系统建模 | 主要面向连续物理过程、CPS、混成系统与物理仿真 | 0 |

## 状态口径

右侧数量统计当前普通论文总表与综述论文总表中的状态条目总数。

| Emoji | 含义 | 数量 |
|---|---|---:|
| 🟢 | 直接可用 | 9 |
| 🟡 | 可整理 | 1 |
| ⚪ | 未收获 | 0 |
| ⏳ | 尚未提取 | 0 |

## 综述对象类型口径

右侧数量统计当前综述论文总表中的对象类型条目总数。

| Emoji | 对象类型 | 含义 | 数量 |
|---|---|---|---:|
| 🧱 | 模型本体 | 主要综述形式主义本身、语义、变体与边界 | 7 |
| 🛠️ | 方法路线 | 主要综述围绕形式主义的验证、综合、转换、形式化方法 | 2 |
| 🏗️ | 标准/基础设施 | 主要综述标准、交换格式、元模型、API、工具互操作 | 1 |
| 🧪 | 应用/案例 | 主要综述领域应用、案例与工业采用 | 0 |

## 当前收录重心

- 后续普通条目优先补**模型本体**与**标准/基础设施**，即定义、语义、构造方式、交换格式、元模型、工具链与标准材料。
- 方法路线类论文或综述只作为辅助证据使用，前提是它们能说明某一形式主义“能做什么、如何落地、依赖什么基础设施”。
- 应用/案例导向条目原则上不作为本 collection 的正式扩库方向，除非它同时补出了稳定的模型本体或基础设施证据。

## 检索关键词簇

### 当前推荐关键词簇

- `finite state machine / extended finite state machine / statechart / UML state machine / SCXML`
- `tree automata / top-down tree automata / hedge automata / XML schema automata`
- `multi-tape automata / two-dimensional automata / cellular automata / weighted automata`
- `timed automata / timed statecharts / timed transition systems / timed I-O automata`
- `hybrid automata / probabilistic automata / stochastic automata / stochastic hybrid automata`
- `petri net / colored petri net / timed petri net / PNML / hierarchical petri net`
- `interface automata / I-O automata / contract automata / reactive modules`
- `survey / review / tutorial / taxonomy / mapping study` + 上述形式主义关键词

### 已观察到的高命中特征

- `survey/review/tutorial` 与具体家族词绑定时命中率高，例如 `timed automata survey`、`formalizing UML state machines survey`
- 对理论 automata 家族，`family term + survey` 往往能直接命中作者预印本或机构开放仓储，适合先补 `🧱` 再回溯原始文献
- `standardisation / markup language / PNML / formalizing / tool support` 这类“形式主义 + 基础设施”词簇很适合挖标准化与工具生态论文
- `cyber-physical systems` 与 `hybrid automata` 联合检索时，更容易命中“建模与验证框架综述”而非单一算法论文

### 已观察到的低命中特征

- 只搜 `state machine survey` 容易漂移到工作流、AI agent、软件工程流程或分类器论文
- 只搜 `verification` 容易命中算法优化或应用案例，而不是形式主义本体综述
- 只搜 `UML tool` 容易落到商业建模工具宣传页，形式语义与验证基础不足

### 检索倾向调整

- 继续以“家族词 + survey/review/tutorial”作为第一轮入口，再由 survey 反推出原始文献、标准和工具线
- 对离散 automata 理论支线，优先补“模型谱系 + 经典判定边界 + 构造载体”三类材料，不把纯形式语言技巧论文直接当扩库主线
- 后续普通条目优先补“定义/语义 + 标准/交换格式 + 工具链”三类材料，不把应用论文或纯方法论文当扩库主线
- 对 `Petri Nets` 一类基础设施成熟方向，优先补 `standard / markup language / metamodel / API` 线，而不是只补理论定义
- `SCXML`、`Interface/Contract Automata` 仍是当前 survey 视角下的空白主线，下一轮应优先补位
- 方法路线条目只在能够反向支撑某一形式主义的能力边界或基础设施条件时再跟进

## 状态机类型论文总表

说明：

1. `主类`、`客体`、`领域` 与 `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. `主类` 的中文释义见上方“形式主义主类口径”，`客体` 的中文释义见上方“描述客体口径”，`领域` 的中文释义见上方“所属领域口径”，`状态` 的中文释义见上方“状态口径”。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 主类 | 客体 | 领域 | 形式主义 | 论文角色 | 标题 | 年份 | 核心功能 | 关键特性 | 构造方式 | 基础设施 | 适用场景 | 需求前提 | 状态 | 目录 |
|---|---|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|
| - | - | - | - | - | - | 暂无 | - | - | - | - | - | - | - | - | - |

## 综述类论文总表

说明：

1. `对象类型` 与 `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. survey 正式入账后，应继续把其引出的代表原始文献回填到下一节的追踪表。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 综述主题 | 对象类型 | 标题 | 年份 | 覆盖主类 | 覆盖的形式主义 | 是否覆盖构造方式/基础设施 | 主要价值 | 状态 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | 二维自动机理论版图 | 🧱 | A Survey of Two-Dimensional Automata Theory | 1991 | 🧩 | `2D Turing Machines`、`2D Finite Automata`、`Marker Automata`、cellular types | 部分覆盖 | 把二维 tape 上的方向限制、alternation、封闭性与判定问题统一进一个谱系 | 🟢 | [survey.md](./survey-of-two-dimensional-automata-theory/survey.md) |
| 2 | 状态图模型检验路线 | 🛠️ | Model Checking of Statechart Models: Survey and Research Directions | 2004 | 🧩 | `Statecharts`、`STATEMATE`、`RSML`、`UML State Machine`、`HRM/CRSM` | 部分覆盖 | 讲清层次状态机验证中的 flattening、语义歧义与 traceability 问题 | 🟡 | [survey.md](./model-checking-of-statechart-models/survey.md) |
| 3 | 细胞自动机理论版图 | 🧱 | Theory of Cellular Automata: A Survey | 2005 | 🧩 | 同步 `CA`、reversible `CA`、number-conserving/linear `CA`、空间受限识别 `CA` | 部分覆盖 | 把可逆性、守恒量、动力学与语言识别四条理论主线压到一篇里 | 🟢 | [survey.md](./theory-of-cellular-automata-survey/survey.md) |
| 4 | Petri 网标准化与交换格式 | 🏗️ | PN Standardisation: A Survey | 2006 | 🕸️ 📦 | `P/T Nets`、`High-level Petri Nets`、`Symmetric Nets`、`PNML` | 是 | 直接覆盖标准、元模型、XML 承载与 API 实现 | 🟢 | [survey.md](./pn-standardisation-survey/survey.md) |
| 5 | 确定性自顶向下树自动机谱系 | 🧱 | Deterministic Top-Down Tree Automata: Past, Present, and Future | 2008 | 🧩 📦 | blind/sensing、ranked/unranked、`DTD`、`XML Schema`、`Relax NG` | 是 | 讲清 deterministic top-down tree automata 在 ranked/unranked/XML schema 三条线上的 expressive power 与静态分析边界 | 🟢 | [survey.md](./deterministic-top-down-tree-automata/survey.md) |
| 6 | 多带自动机表达力与判定性 | 🧱 | A Survey of Multi-Tape Automata | 2012 | 🧩 | synchronous/asynchronous、one-way/two-way、rewind-bounded、reversal-bounded 多带自动机 | 部分覆盖 | 把多带 automata 的同步、回退、反转与确定性差异压成统一闭包与可判定性版图 | 🟢 | [survey.md](./survey-of-multi-tape-automata/survey.md) |
| 7 | 时间自动机变体与工具生态 | 🧱 | A Survey of Timed Automata for the Development of Real-Time Systems | 2013 | ⏱️ | 经典、参数化、概率、代价、博弈等 `Timed Automata` 变体 | 是 | `80` 个变体、`40` 个工具、实现问题一体化盘点 | 🟢 | [survey.md](./survey-of-timed-automata-for-real-time-systems/survey.md) |
| 8 | 混成自动机与 CPS 验证 | 🧱 | Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems | 2013 | 🌊 ⏱️ | 一般 `Hybrid Automata`、`Timed Automata`、`Initialized Rectangular`、`PCD` | 部分覆盖 | 讲清连续动力学引入后的判定边界与工具谱系 | 🟢 | [survey.md](./hybrid-automata-for-cps/survey.md) |
| 9 | 加权逻辑与加权自动机统一视角 | 🧱 | A Unifying Survey on Weighted Logics and Weighted Automata | 2018 | 🧩 | `Weighted Automata`、core weighted logic、words/ranked/unranked trees | 部分覆盖 | 把权值域、承载结构和抽象/具体语义三条轴统一起来，适合补 quantitative automata 本体 | 🟢 | [survey.md](./weighted-logics-and-weighted-automata-survey/survey.md) |
| 10 | UML 状态机形式化与自动验证 | 🛠️ | Formalizing UML State Machines for Automated Verification -- A Survey | 2023 | 🧩 📦 | `UML State Machine`、translation targets、direct operational semantics | 是 | `61` 篇工作双路线盘点，并审计工具长期可用性 | 🟢 | [survey.md](./formalizing-uml-state-machines-survey/survey.md) |

## 由综述引出的待跟进原始文献

说明：

1. 本表用于把 survey/review 条目转成下一轮可执行的补库入口。
2. `优先级` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
3. 本表属于文献跟进表，默认包含 `年份`，并按 `年份升序` 排列。
4. 若某条原始文献已经正式入库为普通条目、标准条目或其他正式总账条目，应立即从本表移除，不再重复挂在“待跟进”状态。

| # | 年份 | 来源综述 | 形式主义 / 方向 | 应追踪的原始文献或标准 | 推荐原因 | 后续动作 | 优先级 |
|---|---:|---|---|---|---|---|---|
| 1 | 1961 | 加权逻辑与加权自动机统一视角 | `Weighted Automata` | Schützenberger, `On the Definition of a Family of Automata` | 加权自动机与形式幂级数主线的原始起点 | 优先补单篇 `desc.md` | 🔴 |
| 2 | 1965 | 多带自动机表达力与判定性 | relation / multi-tape 基线 | Elgot, Mezei, `On Relations Defined by Generalized Finite Automata` | 连接多带自动机、关系语言与 rational relations 的早期基石 | 优先补单篇 `desc.md` | 🔴 |
| 3 | 1967 | 二维自动机理论版图 | `2D Automata` 起点 | Blum, Hewitt, `Automata on a Two-Dimensional Tape` | 二维 tape 自动机研究的共同起点 | 优先补单篇 `desc.md` | 🔴 |
| 4 | 1968 | 确定性自顶向下树自动机谱系 | 树自动机基线 | Thatcher, Wright, `Generalized Finite Automata Theory with an Application to a Decision Problem of Second-Order Logic` | regular tree language 与 tree automata 主线的早期理论入口 | 优先补单篇 `desc.md` | 🔴 |
| 5 | 1968 | 多带自动机表达力与判定性 | one-way multi-tape | Fischer, Rosenberg, `Multitape One-Way Nonwriting Automata` | 连接 one-way 多带机与 relation 识别能力的早期主线 | 优先补单篇 `desc.md` | 🟠 |
| 6 | 1969 | 细胞自动机理论版图 | 符号动力系统口径 | Hedlund, `Endomorphisms and Automorphisms of Shift Dynamical Systems` | 把 `CA` 放进 shift dynamics 语义框架，是后续可逆性/动力学主线的基准 | 优先补单篇 `desc.md` | 🔴 |
| 7 | 1972 | 细胞自动机理论版图 | injective / surjective 判定 | Amoroso, Patt, `Decision Procedures for Surjectivity and Injectivity of Parallel Maps for Tessellation Structures` | 一维 `CA` 可判定性主线的经典入口 | 优先补单篇 `desc.md` | 🔴 |
| 8 | 1977 | 二维自动机理论版图 | 二维有限自动机能力边界 | Blum, Sakoda, `On the Capability of Finite Automata in 2 and 3 Dimensional Space` | 直接支撑二维有限自动机的表达边界与方向受限讨论 | 优先补单篇 `desc.md` | 🟠 |
| 9 | 1987 | 状态图模型检验路线 | `Statecharts` | David Harel, `Statecharts: A Visual Formalism for Complex Systems` | 层次状态机主线的原始起点，后续 UML/STATEMATE 都要回到它校准 | 优先补单篇 `desc.md` | 🔴 |
| 10 | 1991 | 细胞自动机理论版图 | 加性守恒量 | Hattori, Takesue, `Additive Conserved Quantities in Discrete-Time Lattice Dynamical Systems` | 守恒量与 number-conserving `CA` 主线的关键入口 | 优先补单篇 `desc.md` | 🟠 |
| 11 | 1991 | Petri 网标准化与交换格式 | `Time Petri Nets` | Berthomieu, Diaz, `Modeling and Verification of Time Dependent Systems Using Time Petri Nets` | 连接 `Petri Net` 与时间扩展，是后续 Part 3 重要背景 | 优先补单篇 `desc.md` | 🟠 |
| 12 | 1993 | 混成自动机与 CPS 验证 | 一般 `Hybrid Automata` | Alur et al., `Hybrid Automata: An Algorithmic Approach to the Specification and Verification of Hybrid Systems` | 混成自动机奠基文献 | 优先补单篇 `desc.md` | 🔴 |
| 13 | 1994 | 时间自动机变体与工具生态 | 经典 `Timed Automata` | Alur, Dill, `A Theory of Timed Automata` | 时间自动机主线的定义基准 | 优先补单篇 `desc.md` | 🔴 |
| 14 | 1996 | 状态图模型检验路线 | `STATEMATE` 语义 | Harel, Naamad, `The STATEMATE Semantics of Statecharts` | 原始语义口径，对 priority/history/inter-level transition 很关键 | 优先补单篇 `desc.md` | 🔴 |
| 15 | 1997 | UML 状态机形式化与自动验证 | `UML` 标准起点 | `OMG UML 1.1 specification` | 形式化工作共同的时间边界和标准起点 | 先补标准条目 | 🟡 |
| 16 | 1998 | 混成自动机与 CPS 验证 | 判定边界 | Henzinger et al., `What's Decidable About Hybrid Automata?` | 混成自动机可判定子类和边界线的关键入口 | 优先补单篇 `desc.md` | 🔴 |
| 17 | 1999 | UML 状态机形式化与自动验证 | UML + model checking | Lilius, Paltor, `Formalising UML State Machines for Model Checking` | UML 形式化主线的重要早期节点 | 优先补单篇 `desc.md` | 🔴 |
| 18 | 1999 | 确定性自顶向下树自动机谱系 | `Hedge Automata` / XML | Murata, `Hedge Automata: A Formal Model for XML Schemata` | 连接 unranked tree automata 与 XML schema 生态的关键节点 | 优先补单篇 `desc.md` | 🔴 |
| 19 | 2000 | 状态图模型检验路线 | 保层次验证 | Alur et al., `Efficient Reachability Analysis of Hierarchic Reactive Machines` | 代表避免完全 flatten 的关键技术路线 | 先找原文并评估是否入库为 `desc.md` | 🟡 |
| 20 | 2004 | Petri 网标准化与交换格式 | `Petri Net` 标准 Part 1 | `ISO/IEC 15909-1` | 标准化术语、语义和图形记法的核心入口 | 优先补标准条目 | 🔴 |
| 21 | 2005 | Petri 网标准化与交换格式 | `PNML` / Part 2 概念线 | Ekkart Kindler, `The Petri Net Markup Language and ISO/IEC 15909-2` | 补足 `PNML` 的核心概念、状态和未来方向 | 优先补单篇 `desc.md` | 🔴 |
| 22 | 2006 | Petri 网标准化与交换格式 | High-level Petri Nets | Jensen, Rozenberg (eds.), `High-Level Petri Nets` | 回补高层网本体与标准化对象之间的理论连接 | 优先补单篇 `desc.md` | 🟠 |
| 23 | 2007 | 加权逻辑与加权自动机统一视角 | automata-logic 等价 | Droste, Gastin, `Weighted Automata and Weighted Logics` | 词上加权自动机与逻辑等价的标准入口 | 优先补单篇 `desc.md` | 🔴 |
| 24 | 2009 | 时间自动机变体与工具生态 | 参数化时间自动机 | Etienne Andre, `IMITATOR` tool line | 连接参数综合与需求到模型自动化 | 先补工具/方法条目 | 🟠 |
| 25 | 2011 | 时间自动机变体与工具生态 | 主流工具线 | Behrmann et al., `A Tutorial on UPPAAL` | 当前最值得优先追踪的时间自动机工具主线 | 优先补工具条目 | 🔴 |
| 26 | 2012 | 加权逻辑与加权自动机统一视角 | valuation monoid 语义 | Droste, Meinecke, `Weighted Automata and Regular Expressions over Valuation Monoids` | 把平均值、折扣和等非半环语义纳入统一权值模型 | 优先补单篇 `desc.md` | 🟠 |
| 27 | 2013 | UML 状态机形式化与自动验证 | 直接操作语义 | Liu et al., `USMMC` / corresponding semantics paper | 代表较完整的 UML 直接语义与验证路线 | 优先补单篇 `desc.md` | 🟠 |
| 28 | 2017 | UML 状态机形式化与自动验证 | 稳定标准语义 | `OMG UML 2.5.1 specification` | 当前更稳的 UML 参考版本，适合对齐 profile | 优先补标准条目 | 🔴 |
| 29 | 2021 | UML 状态机形式化与自动验证 | 现代工具线 | Jouault et al., `AnimUML` | 代表仍在维护、可实际试用的现代 UML 验证工具 | 先补工具条目 | 🟠 |

## 待优先补入方向

1. `Harel Statecharts -> STATEMATE -> UML profile` 这一条层次状态机原始语义线。
2. `OMG UML 2.5.1 + hugo/RT + AnimUML` 这一条 UML 形式化与现代工具线。
3. `Alur-Dill Timed Automata + UPPAAL + IMITATOR` 这一条时间自动机基础与工具线。
4. `Hybrid Automata + What's Decidable About Hybrid Automata? + HyTech/Phaver` 这一条连续动力学验证线。
5. `ISO/IEC 15909-1/2 + PNML + High-Level Petri Nets` 这一条 Petri 网标准与交换格式线。
6. `Tree Automata + Hedge Automata + XML schema validation` 这一条层次树结构与 schema 承载线。
7. `Weighted Automata + valuation monoid/structure` 这一条 quantitative automata 语义线。
8. `Two-Dimensional / Cellular / Multi-Tape Automata` 已有 survey 入口，下一步应补原始定义与典型判定边界论文。
9. 仍待补位的 survey 或定义型方向：`SCXML`、`Interface Automata`、`Contract Automata`。
10. 上述每条主线都优先补“模型本体 + 标准/基础设施”条目；方法路线只作为辅证，不单独扩成主收录方向。

## 更新日志

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-04-01 11:58:00 | 建立 `state_machine_types/` 文库骨架 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)、[SURVEY_GUIDE.md](./SURVEY_GUIDE.md)，并固定普通论文/综述论文双表口径 |
| 2026-04-01 13:03:21 | 首次收录综述类论文 | 新增 5 篇 `survey.md` 条目并回填综述总表与 follow-up 原始文献表，覆盖 `Statecharts/UML`、`Timed Automata`、`Hybrid Automata`、`Petri Net standardisation/PNML` |
| 2026-04-01 13:45:03 | 补充图例数量统计口径 | 为“形式主义主类”“状态”“综述对象类型”三张图例表增加右侧数量列，并要求后续随正式总表同步更新 |
| 2026-04-01 14:43:56 | 新增离散 automata 模型本体综述 | 补入 `Two-Dimensional`、`Cellular`、`Deterministic Top-Down Tree`、`Multi-Tape`、`Weighted Automata` 五篇 `🧱` survey，并同步回填统计、综述总表与 follow-up 文献表 |

## 失败与阻塞记录

- 当前无正式失败记录。
