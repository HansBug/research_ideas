# 状态图模型的模型检验：综述与研究方向 / Model Checking of Statechart Models: Survey and Research Directions

## 基本信息

- 标题：Model Checking of Statechart Models: Survey and Research Directions
- 中文标题：状态图模型的模型检验：综述与研究方向
- 作者：Purandar Bhaduri，S. Ramesh
- 发表：arXiv preprint `cs/0407038`
- DOI：原文未提供
- 链接：https://arxiv.org/abs/cs/0407038
- 综述主题：`Statecharts / STATEMATE / RSML / UML State Machine` 的模型检验路线与可扩展性问题
- 对象类型：🛠️
- 覆盖时间范围：以 1987 年 `Statecharts` 起点为背景，主体覆盖 1998-2004 年前后的模型检验工作
- 覆盖主类：🧩
- 补充材料/数据获取方式：无单独数据集；主要依据原文正文、案例图和参考文献
- 原文是否给出系统比较表：原文未给出一张统一总表，而是按 `SMV / PROMELA-SPIN / Esterel / Hierarchical checker` 等路线逐段比较

## 综述范围与结论

该文聚焦的不是“状态图定义史”，而是“状态图一旦进入模型检验链条后会发生什么”。原文从 `Statecharts` 的层次、并发、通信和 inter-level transition 出发，回顾了多条验证路线，并反复强调一个核心事实：大多数工作都会把层次结构翻译成后端工具可接受的扁平状态空间，这直接带来状态爆炸、语义偏移和调试可追溯性下降。

- 覆盖范围：以 `Harel Statecharts` 为核心对象，重点比较 `STATEMATE`、`RSML`、`UML State Machine` 及若干模型检验后端
- 主要比较轴：语义口径、后端建模语言、是否保留层次结构、是否支持 traceability、是否有工业级验证经验
- 对本 collection 的直接价值：它清楚说明了层次状态机在“可读建模”与“可验证后端”之间的典型裂缝，尤其适合指导 `project_1` 未来如何设计中间表示和语义 profile

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🧩 | Harel Statecharts | 重点 | 定义对象 | 作为层次、并发、广播通信的原始参照 |
| 🧩 | STATEMATE statecharts | 重点 | 对比对象 | 强调 step semantics、外层优先级、inter-level transitions |
| 🧩 | RSML | 一般 | 对比对象 | 以安全关键建模变体进入 `SMV` 验证路线 |
| 🧩 | UML State Machine | 重点 | 对比对象 | 强调 `run-to-completion`、事件队列和深层优先级 |
| 🧩 | CRSM / HRM 等层次验证模型 | 一般 | 对比对象 | 作为避免完全 flatten 的替代验证载体 |

## 分类轴与比较框架

原文主要沿以下几个轴来组织材料：

1. 前端语义对象是什么：`STATEMATE`、`RSML`、`UML State Machine` 还是更抽象的层次状态机。
2. 后端验证器是什么：`SMV`、`SPIN`、`Esterel`、专门的层次检验器。
3. 是否保留层次结构：多数路线把层次状态机 flatten；少数路线尝试保留或部分利用 hierarchy。
4. 语义冲突在哪里：同步/异步 step、事件生命周期、transition priority、inter-level transition、queue/RTC。
5. 工程可用性如何：是否支持 traceability、是否用于工业案例、是否只停留在原型工具。

对本 collection 最有价值的一点是，原文把“层次状态机为什么难验证”拆成了几个可操作问题：`flattening`、`priority resolution`、`queue/RTC semantics`、`traceability` 与 `modularity`。

把原文提到的主路线逐条展开，可以看到它们其实在解决的是**不同层面的问题**：

| 路线 | 前端对象 | 后端/承载 | 是否保留层次 | 对 priority / queue / RTC 的处理 | traceability | 原文评价 |
|---|---|---|---|---|---|---|
| RSML -> `SMV` | `RSML` 变体 | `SMV` | 否，基本扁平化 | 可表达事件、状态、守卫；优先级需额外修改；RSML 本身没有 history | 弱 | 早期可运行路线，但主要适合确定性/安全关键子集 |
| `STATEMATE` -> modular `SMV` | `STATEMATE` | `SMV` 模块化编码 | 语法上尽量保层次，但内部仍会 flatten | 不处理 inter-level transitions，STATEMATE priority 也难保真 | 弱 | 更模块化，但保层次收益有限，核心难点仍没解决 |
| `Statecharts/UML` -> `PROMELA/Spin` | `STATEMATE`、`UML` | `PROMELA` + `Spin` | 通常不保原层次，转 Kripke/EHA 再编码 | 对 queue、candidate transitions、RTC 能写得更细 | 中到强，部分工具可回写 | 适合把执行语义做细，但翻译和语义复杂度更高 |
| `STATEMATE Verification Environment` | `STATEMATE` | `SMI` + `VIS/CUDD` | 面向工业工具链，不强调理论保层次 | 通过 observer 和 pattern 库支持 robustness checks | 强 | 原文里最接近工业级的一条线 |
| `Esterel` 路线 | `STATEMATE` 确定性片段 | `Esterel` | 一定程度保结构 | 借 `STEP` 信号实现 super-step | 弱 | 更偏代码生成/同步语义，不适合作为通用解 |
| `HRM` / hierarchy-preserving model checking | `HRM`，不是原生 `Statecharts` | 专用 checker | 是 | 通过 entry/exit point、mode 语义重写层次 | 中 | 提供保层次思路，但对象已偏离原始 statecharts |

把它们放到用户真正关心的几个维度上，比较结果更清楚：

| 维度 | 扁平翻译路线 | 保层次/专用路线 | 对 `project_1` 的含义 |
|---|---|---|---|
| 接成熟后端的难度 | 低到中 | 高 | 扁平翻译更容易接成熟工具 |
| 保留原语义的能力 | 低到中 | 中到高 | 若以后要自动修复，语义保真不能只靠 flatten |
| inter-level transition 处理 | 难 | 仍难，但更容易显式建模 | 这是层次状态机 profile 必须先固定的点 |
| traceability | 普遍偏弱，少数工具较好 | 专用环境往往更好 | 验证失败后若想回到原模型，必须优先看 traceability |
| 工业可扩展性 | 取决于工具链 | 原文认为仅少数路线有工业证据 | 文库不能只收理论路线，还要记住哪条线真在工业上跑过 |

## 构造方式与表示格式版图

原文对交换格式讨论较弱，但对“状态图如何被承载并送入验证器”有较清楚的脉络。

| 形式主义/路线 | 前端承载方式 | 后端机器承载 | 是否有统一交换格式 | 语义关键点如何落地 | 原文体现出的主要限制 |
|---|---|---|---|---|---|
| Harel Statecharts | 图形化层次状态图 | 原文不聚焦统一机读承载 | 否 | 依赖对 hierarchy / concurrency / broadcast 的语义解释 | 适合做原始语义参照，不直接等于验证输入 |
| `STATEMATE` | 图形化 + CASE 工具内部模型 | `STATEMATE` 工具内部语义对象、后续可翻到 `SMV` 等 | 原文未系统比较 | step semantics、外层优先级、history | 工程环境较强，但外部交换标准弱 |
| `RSML` | 图形化 + 条件/守卫文本 | `SMV` 变量与 `next` 更新编码 | 否 | 通过枚举变量、事件布尔量和启用条件编码 | 主要服务安全关键子集，不代表通用 statecharts |
| `UML State Machine` | 图形 + 守卫/动作文本 | `PROMELA`/`Spin`、`SMV` 等翻译后语言 | 原文未展开统一格式 | queue/RTC/priority 需额外定义 | 标准自然语言语义不足以直接验证 |
| 验证后端载体 | 否 | `SMV`、`PROMELA`、`Esterel`、专用层次 checker | 否 | 真正可机读的是翻译后的 DSL 或专用模型 | 交换标准弱，语义 profile 强依赖工具路线 |

可见，这篇 survey 的重点不在统一交换格式，而在说明：经典层次状态机往往必须先失去一部分原貌，才能进入成熟验证基础设施。

| 路线 | 自动生成最需要补齐的信息 | 缺失后会怎样 |
|---|---|---|
| `STATEMATE` / `UML` 前端建模 | hierarchy、并发 region、priority、queue/RTC、history | 即使图生成出来，也无法稳定翻译到后端 |
| `SMV` 扁平路线 | 状态枚举、启用条件、事件生命周期 | 会导致 state explosion 或语义偏差 |
| `PROMELA/Spin` 路线 | 队列策略、候选迁移选择、atomic RTC step | 会直接影响验证语义与反例解释 |
| 保层次专用路线 | entry/exit point、mode 语义、模块边界 | 无法真正利用 hierarchy 做缩减 |

## 基础设施与生态版图

| 工具/平台 | 主要对象 | 支持能力 | 是否强调 traceability | 成熟度 | 原文中的关键判断 |
|---|---|---|---|---|---|
| `SMV` 路线 | `RSML`、`STATEMATE` 扁平/模块化翻译 | `CTL`、BDD 符号搜索 | 弱 | 中 | 易接成熟验证器，但 hierarchy 和 inter-level transitions 容易丢失 |
| `PROMELA/Spin`、`vUML` | `UML` / `Statecharts` 翻译验证 | 事件队列、`RTC`、死锁/鲁棒性检查 | 中到强 | 中 | 更适合细化执行语义，但 translation 复杂 |
| `STATEMATE Verification Environment` | `STATEMATE` | observer、抽象、COI reduction、industrial robustness checks | 强 | 高 | 原文里最接近工程级环境 |
| `Esterel` 工具链 | 确定性 `Statecharts` 片段 | 验证、代码生成 | 弱 | 中 | 更像同步代码路线而非通用层次状态机验证路线 |
| `HRM` / 专用层次 checker | 保层次模型 | 利用 hierarchy 进行 reachability | 中 | 中 | 提供了“不要 flatten”的方向，但模型已不再是原始 statecharts |

| 比较维度 | `SMV` / `PROMELA` 等翻译路线 | `STATEMATE` 验证环境 / `HRM` 等专用路线 |
|---|---|---|
| 复用成熟后端 | 强 | 弱到中 |
| 对原始 statechart 语义的保真 | 中 | 中到高 |
| traceability | 普遍不足 | 明显更受重视 |
| 工业案例支撑 | 少 | `STATEMATE` 线最强 |

原文明确指出，多数工具都还是学术原型；真正比较成熟的是 `STATEMATE` 路线，而保层次的验证路线在语义兼容性上仍有明显缺口。

## 适用场景与需求映射

| 形式主义/路线 | 适用场景 | 需求前提 | 为什么适合 | 不适合的情况 |
|---|---|---|---|---|
| Harel Statecharts | 复杂事件驱动反应系统的高层行为建模 | 需要层次、并发、广播通信 | 表达复杂反应行为的可读性最好 | 需要直接进入成熟验证器且不愿承受 flatten 代价 |
| `STATEMATE` statecharts | 工业控制/嵌入式设计与前期验证 | 需要接受 `STATEMATE` 语义口径和工具链 | 有较强工程环境与验证经验 | 若目标工具链并非 `STATEMATE` 生态 |
| `UML State Machine` | 软件设计阶段的对象行为建模与早期验证 | 需要固定 `RTC`、事件队列、优先级等 profile | 与工程设计过程衔接最好 | 仅靠标准自然语言语义而不补形式化约束时 |
| `HRM` / 层次验证模型 | 需要尽量保留层次结构进行验证 | 可以接受与原始 statechart 语义的映射/约束 | 给出“利用 hierarchy 缩减状态空间”的直接思路 | 原始模型大量 inter-level transition、全局变量耦合强 |

| 输入需求里最突出的要素 | 更适合的路线 | 原因 |
|---|---|---|
| 重点是可读的层次行为结构 | `Statecharts/UML` 前端 | 表达清晰，适合作为对人交付形态 |
| 重点是尽快接成熟验证后端 | `SMV` / `PROMELA` 翻译路线 | 后端生态成熟，但要接受 profile 收缩 |
| 重点是验证后还能回到原模型调试 | `STATEMATE` 工具线、带 traceability 的 `PROMELA` 路线 | 原文明确把 traceability 当成关键工程问题 |
| 重点是尽量少 flatten | `HRM` 一类保层次路线 | 直接针对 hierarchy 带来的状态爆炸问题 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

如果 `project_1` 未来想把“层次状态机”作为对外可读目标，`Statechart/UML` 仍然有很强吸引力；但如果它们同时还是验证入口，就必须额外固定语义 profile。否则，“同样一张图”在不同工具后端前并不等价。

### 对中间表示设计的启发

中间表示至少应把以下要素显式化，而不能留给自然语言解释：

1. 事件队列是否存在、如何出队。
2. `run-to-completion` 的边界。
3. transition priority 的判定规则。
4. inter-level transition 的进入/退出序列。
5. history、fork/join 与并发 region 的求值顺序。

### 对后续扩库方向的启发

后续不应只补“Statecharts 定义论文”，还应沿三条线并行扩：

1. 原始语义线：`Harel Statecharts`、`STATEMATE semantics`。
2. UML 形式化线：`vUML`、`hugo`、更完整的 operational semantics。
3. hierarchy-preserving verification 线：`HRM`、compositional verification、abstraction/slicing。

### 原文未覆盖但本研究仍需补的空白

原文几乎不系统讨论状态机的机器可交换格式，也没有把 `SCXML`、`XMI` 之类标准化承载线拉进来。因此它更适合回答“怎么验证层次状态机”，不直接回答“怎么统一生成和交换层次状态机”。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1987 | Statecharts | David Harel, `Statecharts: A Visual Formalism for Complex Systems` | 经典层次状态机源头，后续所有语义分歧都要回到这里校准 | 优先补单篇 `desc.md` | 🔴 |
| 1996 | STATEMATE 语义 | David Harel, Amnon Naamad, `The STATEMATE Semantics of Statecharts` | 原文反复以其为语义基准之一，涉及 step、priority、history | 优先补单篇 `desc.md` | 🔴 |
| 1998 | RSML + SMV 路线 | Chan et al., `Model Checking of RSML` | 代表安全关键状态图进入 `SMV` 的早期路线 | 先找原文并补 `desc.md` | 🟠 |
| 1999 | UML 状态机验证 | Lilius, Paltor, `Formalising UML State Machines for Model Checking` | UML 形式化与 `vUML` 路线的重要起点 | 优先补单篇 `desc.md` | 🔴 |
| 2000 | 保层次验证 | Alur, Grosu, McDougall, `Efficient Reachability Analysis of Hierarchic Reactive Machines` | 代表“避免完全 flatten”的关键分支 | 先找原文并判断是否收录为 `desc.md` | 🟡 |

## 文献分类总结

- 综述主题：层次状态机模型检验路线
- 对象类型：🛠️
- 覆盖主类：🧩
- 覆盖的形式主义：`Harel Statecharts`、`STATEMATE`、`RSML`、`UML State Machine`、`HRM/CRSM`
- 是否覆盖构造方式/基础设施：部分覆盖，重点在验证后端和语义差异，交换格式覆盖弱
- 主要价值：把层次状态机在验证时遇到的 `flattening`、语义歧义、traceability 与工业可扩展性问题讲清楚了
- 状态：🟡
