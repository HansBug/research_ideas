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

## 构造方式与表示格式版图

原文对交换格式讨论较弱，但对“状态图如何被承载并送入验证器”有较清楚的脉络。

| 形式主义 | 图形表示 | 文本/DSL | XML/JSON/元模型 | 标准/交换格式 | 说明 |
|---|---|---|---|---|---|
| Harel Statecharts | 是 | 否 | 原文未系统比较 | 否 | 核心是图形化层次状态图 |
| STATEMATE statecharts | 是 | 有工具内部表示 | 原文未系统比较 | 否 | 更强调 CASE 工具中的执行语义 |
| RSML | 是 | 守卫与条件有文本表达 | 原文未系统比较 | 否 | 常作为安全关键变体进入 `SMV` |
| UML State Machine | 是 | 有动作/守卫文本 | 原文未系统比较 | 未展开 | 作为对象导向 `Statecharts` 变体出现 |
| 验证后端载体 | 否 | `SMV`、`PROMELA`、`Esterel` | 否 | 否 | 真正可机读的往往是翻译后的验证 DSL，而非原始状态图 |

可见，这篇 survey 的重点不在统一交换格式，而在说明：经典层次状态机往往必须先失去一部分原貌，才能进入成熟验证基础设施。

## 基础设施与生态版图

| 形式主义 | 典型工具/平台 | 支持能力 | 生态成熟度 | 备注 |
|---|---|---|---|---|
| RSML / Statecharts | `SMV` | `CTL` 模型检验、BDD 符号化搜索 | 中 | 依赖翻译到 `SMV` 后的有限状态模型 |
| UML State Machine | `SPIN` / `PROMELA`、`vUML` | 事件队列、`RTC` 语义的模型检验 | 中 | 对语义 profile 很敏感 |
| STATEMATE | `STATEMATE Verification Environment` | 组合验证、抽象、工业案例验证 | 高 | 原文中最接近工业化的一条线 |
| Statecharts deterministic fragment | `Esterel` 工具链 | 验证与代码生成 | 中 | 只适合确定性片段 |
| 层次模型检验 | `HRM` / 专用 checker | 尝试直接利用层次结构 | 中 | 语义与经典 statecharts 仍有差异 |

原文明确指出，多数工具都还是学术原型；真正比较成熟的是 `STATEMATE` 路线，而保层次的验证路线在语义兼容性上仍有明显缺口。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 不适合的情况 |
|---|---|---|---|
| Harel Statecharts | 复杂事件驱动反应系统的高层行为建模 | 需要层次、并发、广播通信 | 需要直接进入成熟验证器且不愿承受 flatten 代价 |
| STATEMATE statecharts | 工业控制/嵌入式设计与前期验证 | 需要接受 `STATEMATE` 语义口径 | 若目标工具链并非 `STATEMATE` 生态 |
| UML State Machine | 软件设计阶段的对象行为建模与早期验证 | 需要固定 `RTC`、事件队列、优先级等 profile | 仅靠标准自然语言语义而不补形式化约束时 |
| HRM / 层次验证模型 | 需要尽量保留层次结构进行验证 | 可以接受与原始 statechart 语义的映射/约束 | 原始模型大量 inter-level transition、全局变量耦合强 |

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
