# 加权逻辑与加权自动机统一综述 / A Unifying Survey on Weighted Logics and Weighted Automata

## 基本信息

- 标题：A Unifying Survey on Weighted Logics and Weighted Automata
- 中文标题：加权逻辑与加权自动机统一综述
- 作者：Paul Gastin，Benjamin Monmege
- 发表：`Soft Computing`, Volume 22, Issue 4, 2018
- DOI：`10.1007/s00500-015-1952-6`
- 链接：https://doi.org/10.1007/s00500-015-1952-6
- 综述主题：`Weighted Automata` 在不同权值域、不同载体结构和对应逻辑表述下的统一语义框架
- 对象类型：🧱
- 覆盖时间范围：从 `Schützenberger 1961` 起，整理到 `2015/2018` 前后的 semiring、valuation monoid、valuation structure 与树上扩展
- 覆盖主类：🧩
- 补充材料/数据获取方式：原文正文与参考文献链为主，无独立数据集；正文本身给出统一抽象语义
- 原文是否给出系统比较表：是，按权值域、结构载体、逻辑片段与等价结果系统展开

## 综述范围与结论

这篇 survey 的主线不是做工具盘点，而是做**语义统一**。原文把 `Weighted Automata` 看成一个家族：不同的 carrier 可以是 words、ranked trees、unranked trees；不同的 weight domain 可以是 semirings、valuation monoids、valuation structures；不同的 specification side 可以是 weighted MSO 或更简洁的 core weighted logic。作者的核心目标是说明：这些看似分散的加权 automata / logic 结果，其实共享一套统一的抽象语义骨架。

- 覆盖范围：`Weighted Automata`、semiring 语义、valuation monoid / valuation structure 扩展、core weighted logic、words / ranked trees / unranked trees
- 主要比较轴：权值域、承载结构、自动机语义、逻辑表达能力、抽象语义 vs 具体语义
- 对本 collection 的直接价值：它能帮助我们把“带权状态机”当成一种模型本体，而不是零散的 cost/probability 附加技巧

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🧩 | `Weighted Automata` over words | 重点 | 定义对象 | 作为最基础的 carrier 与经典语义入口 |
| 🧩 | `Weighted Automata` over ranked / unranked trees | 重点 | 扩展对象 | 用于说明统一框架可推广到树结构 |
| 🧩 | semiring-based weighted automata | 重点 | 基线对象 | 经典乘加语义路线 |
| 🧩 | valuation monoid / valuation structure routes | 重点 | 扩展对象 | 用来覆盖 average、discounted sum、ratio 等非传统权值组合 |
| 🧩 | core weighted logic / weighted MSO | 重点 | 对应对象 | 不是方法路线，而是 automata 的等价规格化表述 |

## 分类轴与比较框架

原文的比较框架有三条特别强的主轴。第一条是**权值域轴**：semiring、valuation monoid、valuation structure。第二条是**承载结构轴**：words、ranked trees、unranked trees。第三条是**语义层次轴**：abstract semantics、concrete semantics、logic equivalence。它真正解决的是：带权自动机家族如何在不丢失统一性的前提下扩张表达力。

| 比较对象 | 主要增加的能力 | 原文比较维度 | 优势 | 代价或限制 |
|---|---|---|---|---|
| semiring-weighted automata | 乘加式权值累积 | 运行值、接受语义、逻辑等价 | 语义经典、结果成熟 | 很多 quantitative 需求超出 semiring 乘积能力 |
| valuation monoid routes | 支持 average、discounted sum 等 | valuation operator | 能表达更广的数值聚合 | 代数假设更弱，证明更复杂 |
| valuation structure routes | 分离运行值与最终 evaluator | `Val` + `F` 双层语义 | 能表达 ratio、多资源综合评价 | 结构更灵活，也更抽象 |
| words vs trees | 从串扩到树 | 结构承载 | 同一权值思想可复用于层次结构 | 自动机构造和逻辑语法都要扩展 |
| core weighted logic | 极简逻辑规格化 | 表达能力、等价定理 | 适合做统一中间表示或规范层 | 本身不是标准交换格式 |

原文的关键结论是：`Weighted Automata` 不是“普通自动机再给边上贴几个数字”这么简单，它背后真正决定家族差异的是**权值域语义**和**承载结构**。

## 构造方式与表示格式版图

| 形式主义 | 图形表示 | 文本/DSL | XML/JSON/元模型 | 标准/交换格式 | 说明 |
|---|---|---|---|---|---|
| word-weighted automata | 状态图常见 | 转移 + weight 标注 | 否 | 无统一标准 | 最直接的承载是“带权转移系统” |
| tree-weighted automata | 树/状态图可视化 | 结构相关规则 + weight | 否 | 无统一标准 | 依赖树的 carrier 结构扩展 |
| core weighted logic | 否 | 逻辑公式 | 否 | 无统一标准 | 是 automata 的规格化表述，不是工业交换格式 |
| abstract semantics route | 否 | 多重集语义对象 | 否 | 无 | 原文的统一性正是靠这一层建立 |

这篇 survey 对构造方式的最大价值是把“机器承载”和“数值解释”拆开：先有结构化 run / abstract semantics，再由具体权值域去聚合。这对 `project_1` 很有启发，因为它说明 quantitative automata 的中间表示不应直接把所有数值语义压死在 transition label 上。

| 路线 | 建模入口 | 机器承载 | 自动生成最关键的信息 | 原文体现 |
|---|---|---|---|---|
| classical weighted automata | 状态 + 带权转移 | automaton tuple | 权值域与聚合规则 | semiring 语义是最基础入口 |
| valuation monoid / structure | automaton + valuation/evaluator | automaton tuple + semantic operators | 序列权值如何汇总、最终如何评估 | 是原文最重要的统一扩展轴 |
| weighted logic | 结构谓词 + 量化 + 权值构造 | 逻辑公式 | 逻辑片段与自动机等价边界 | 说明逻辑可作为 companion carrier |

## 基础设施与生态版图

| 形式主义 | 典型工具/平台 | 支持能力 | 生态成熟度 | 备注 |
|---|---|---|---|---|
| semiring-weighted automata | handbook / theory community 丰富 | 形式建模、语义分析 | 高 | 原文主要盘理论，不盘软件 |
| valuation extensions | 原文未系统盘工具 | 数值语义扩张 | 中 | 仍偏理论统一框架 |
| tree-weighted extensions | 原文未系统盘工具 | 层次结构 quantitative 建模 | 中 | 作为 words 路线的扩张 |
| weighted logic | 逻辑规格与等价证明 | 规格化表达 | 中 | 更像规范层，而非工程工具线 |

原文几乎不比较工程工具，但它给出了清楚的理论基础设施：统一语义、统一逻辑片段、统一等价证明。对本 collection 而言，这是一条**模型语义基础设施**，而不是**软件工具基础设施**。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 不适合的情况 |
|---|---|---|---|
| semiring-weighted automata | cost、counting、shortest / best 路径式量化行为 | 需求可写成乘加累积 | 需要平均值、折扣、比值等更复杂聚合 |
| valuation monoid routes | average、discounted、非标准聚合 | 必须明确 valuation operator | 若需求只需普通 semiring 时显得过重 |
| valuation structure routes | 多资源综合评价、ratio、复杂 evaluator | 需求要清楚区分 run value 与 final evaluation | 若只需单一标量聚合时过于抽象 |
| tree-weighted automata | 层次结构上的 quantitative 约束 | 需求对象天然是树 | 对象是普通平面状态图或时间自动机时 |

| 需求信号 | 更适合的 weighted 路线 | 原因 |
|---|---|---|
| 只需累加/取最优 | semiring-weighted | 经典且工具/理论最稳 |
| 需要折扣、平均 | valuation monoid | semiring 乘法不够表达 |
| 需要多资源综合或比值 | valuation structure | evaluator 可把多维运行值压成最终结果 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

如果 `project_1` 后续不只关心“是否满足”，还关心代价、资源、偏好或打分，那么 `Weighted Automata` 不是附属技巧，而是一条独立的模型本体路线。

### 对中间表示设计的启发

中间表示至少要区分：

1. 结构载体是什么，word 还是 tree。
2. transition 上记录的原始 weight 是什么。
3. 序列级聚合如何做。
4. 全局 evaluator 如何做。

否则很多 quantitative 需求会被错误压扁。

### 对后续扩库方向的启发

应优先补：

1. `Schützenberger 1961` 的原始带权自动机定义。
2. `Weighted Automata and Weighted Logics` 的经典等价路线。
3. valuation monoid / structure 的扩展语义论文。

### 原文未覆盖但本研究仍需补的空白

原文不提供工业标准化格式，也不讨论 XML/JSON/DSL 承载，因此它能回答“带权自动机语义如何统一”，但还不能直接回答“如何作为工程模型文件交换”。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1961 | `Weighted Automata` 起点 | Schützenberger, `On the Definition of a Family of Automata` | 带权自动机与形式幂级数主线的共同起点 | 优先补单篇 `desc.md` | 🔴 |
| 2007 | 经典 automata-logic 等价 | Droste, Gastin, `Weighted Automata and Weighted Logics` | 词上 weighted automata / logic 等价的标准入口 | 优先补单篇 `desc.md` | 🔴 |
| 2012 | valuation monoid 语义 | Droste, Meinecke, `Weighted Automata and Regular Expressions over Valuation Monoids` | 把平均值、折扣等语义拉进统一带权模型 | 优先补单篇 `desc.md` | 🟠 |
| 2013 | valuation structure 语义 | Droste, Perevoshchikov, valuation structure line | 支撑 ratio、多资源 evaluator 等更一般语义 | 先找原文并评估是否入库为 `desc.md` | 🟠 |

## 文献分类总结

- 综述主题：`Weighted Automata` 在不同权值域和结构载体上的统一语义框架
- 对象类型：🧱
- 覆盖主类：🧩
- 覆盖的形式主义：semiring-weighted automata、valuation monoid / structure 路线、words / ranked trees / unranked trees、core weighted logic
- 是否覆盖构造方式/基础设施：部分覆盖，语义承载讲得很清楚，但工程交换格式和工具生态弱
- 主要价值：把带权自动机从“零散扩展”提升为一套可统一比较的模型家族
- 状态：🟢
