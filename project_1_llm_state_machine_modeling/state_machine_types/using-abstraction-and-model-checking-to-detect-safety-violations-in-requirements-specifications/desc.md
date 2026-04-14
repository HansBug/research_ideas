# 用抽象与模型检查检测需求规格中的安全违规 / Using Abstraction and Model Checking to Detect Safety Violations in Requirements Specifications

## 基本信息

- 标题：Using Abstraction and Model Checking to Detect Safety Violations in Requirements Specifications
- 中文标题：用抽象与模型检查检测需求规格中的安全违规
- 作者：Constance Heitmeyer, James Kirby, Jr., Bruce Labaw, Myla Archer, Ramesh Bharadwaj
- 发表：IEEE Transactions on Software Engineering, 24(11):927-948, 1998
- DOI：`10.1109/32.730543`
- 链接：https://doi.org/10.1109/32.730543
- 形式主义：`SCR` tabular notation
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：需求规格方法 / 验证工具链
- 工具/实现获取方式：原文明确给出 `SCR` specification editor、dependency graph browser、consistency checker、simulator，以及与 `Spin` 的集成；论文未提供公开下载地址。
- 标准/格式获取方式：承载方式是 `SCR` 的 tabular notation，包括 condition tables、event tables、assertion dictionary 和 conditional assignments；未给 XML/JSON 交换格式。

## 简报

这篇论文的重点不是重新发明一个求解器，而是展示 `SCR` 这类需求状态机 / 表格规格怎样和“可按按钮触发”的工具链连起来。作者把 `SCR` 规格视为同步状态机：环境通过 monitored variables 产生输入事件，系统通过 table functions 更新 terms / modes / controlled variables，并用 assertion dictionary 表示安全性质；在此基础上，再用 abstraction + `Spin` 去检查实际的安全关键控制面板规格。

- 形式主义定位：面向安全关键控制系统需求规格的 tabular state-machine method。
- 构造方式简述：以 monitored / controlled variables、terms、mode classes、condition tables、event tables 与 assertions 联合构造。
- 基础设施与场景简述：依托 specification editor、consistency checker、dependency graph browser、simulator 与 `Spin` 集成，服务 avionics、space、telephone network、nuclear control 等安全关键系统。

```text
需求与环境变量 -> SCR 表格规格 -> table functions / conditional assignments -> simulator / consistency checker / Spin -> 安全性质检查
```

## 形式主义定义与核心对象

### 定义对象

`SCR` 用四变量模型的口径来描述系统需求：环境提供 monitored quantities，系统必须让 controlled quantities 满足所需关系；为了把这个关系写得更紧凑，还引入 terms 和 mode classes 作为辅助状态。

### 核心抽象

论文直接给出系统模型：

$$
S = (\mathcal{S}, \mathcal{S}_0, E_m, T)
$$

上式中的符号逐项解释如下：

1. `\mathcal{S}` 是系统状态集合。
2. `\mathcal{S}_0 \subseteq \mathcal{S}` 是初始状态集合。
3. `E_m` 是输入事件集合。
4. `T` 是 transform，描述允许的状态转移。

论文还给出了状态与事件的基本口径：

$$
s : RF \to TY
$$

$$
@T(c) = \neg c \land c', \qquad @F(c) = @T(\neg c)
$$

这些符号逐项解释如下：

1. `RF` 是规格中全部状态变量名的集合。
2. `TY` 给每个变量分配其合法取值域。
3. `s` 是一个状态，把每个变量映射到其当前值。
4. `@T(c)` 表示条件 `c` 在当前步中“变为真”。
5. `@F(c)` 表示条件 `c` 在当前步中“变为假”。
6. 撇号 `c'` 表示在 next state 中计算 `c`。

在 `SCR` 中，规格变量分为 monitored、terms / modes 和 controlled 三层，且它们的直接依赖必须形成偏序，保证 transform `T` 定义良好。

### 一个最小例子与通俗解释

论文给了两个很典型的表格例子。

第一个是普通 condition table：

1. 若 `mLAMP_CHECK = up` 或 `not mHYDRAULIC_OIL_PRESSURE`，则 `cHYDRAULIC_PRESSURE_LOW_INDICATOR = true`。
2. 否则为 `false`。

第二个是 history-dependent 的 event table：

1. 当 `@T(mPRESSURE_HOLD \land tPRESSURE_AUTO)` 发生时，令 `tPRESSURE_LATCH := true`。
2. 当 `@F(tPRESSURE_AUTO)` 发生时，令 `tPRESSURE_LATCH := false`。

通俗地说，`SCR` 像“把安全关键系统需求写成一组带历史的状态表”。普通条件表描述当前状态下应有的输出，事件表描述 latch 这类会记住过去事件的内部状态。

### 运行 / 接受 / 转移语义

论文把 table semantics 压成 conditional assignments。对 `tPRESSURE_LATCH` 的 event table，直接给出：

$$
\begin{aligned}
\text{if } & @T(mPRESSURE\_HOLD \land tPRESSURE\_AUTO) \to tPRESSURE\_LATCH := true \\
\text{if } & @F(tPRESSURE\_AUTO) \to tPRESSURE\_LATCH := false
\end{aligned}
$$

对 `cTEST_MODE_INDICATOR` 的 condition table，则给出：

$$
\begin{aligned}
\text{if } & \neg(mLAMP\_CHECK = up \lor tTEST\_MODE) \to cTEST\_MODE\_INDICATOR := off \\
\text{if } & mLAMP\_CHECK = up \to cTEST\_MODE\_INDICATOR := on \\
\text{if } & tTEST\_MODE \land \neg(mLAMP\_CHECK = up) \to cTEST\_MODE\_INDICATOR := flash
\end{aligned}
$$

上式中的符号逐项解释如下：

1. 第一组规则对应 event table，表示历史相关变量的更新。
2. 第二组规则对应 condition table，表示当前状态条件下的直接输出选择。
3. condition table 要求各行 guard 完全覆盖且互斥。
4. event table 要求事件 guard 互斥；若没有 guard 为真，则变量值保持不变。

论文还强调运行假设是同步的“一次只处理一个 input event”：

$$
\text{One Input Assumption}:\quad \forall \text{ step},\ \text{exactly one monitored change is processed}
$$

这意味着：

1. 当前输入事件先决定 monitored variables 的新值。
2. 再按变量偏序计算 terms / modes / controlled variables。
3. 整个系统处理完这一输入事件后才进入下一步。

### 语义边界

`SCR` 的边界是：

1. 它擅长安全关键需求规格，不直接等于实现代码。
2. 它的 step semantics 比 `RSML` 一类状态图更克制、也更容易做 consistency checking。
3. 它主要面向离散、同步、表驱动需求；连续动力学不在核心范围内。
4. 论文中的模型检查结果还依赖 abstraction，因为实际规格的状态空间往往极大甚至无限。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统模型 | `$S = (\mathcal{S}, \mathcal{S}_0, E_m, T)$` | `SCR` 规格最终仍对应同步状态机。 |
| 状态定义 | `$s : RF \to TY$` | 每个状态就是所有变量到其取值域的映射。 |
| 事件语义 | `$@T(c)=\neg c \land c',\ @F(c)=@T(\neg c)$` | `SCR` 直接把“条件变真 / 变假”提升为事件。 |
| 条件 / 事件表执行 | `if guard -> assignment` | 所有表格最终都可编译成 conditional assignment。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | terms、mode classes、controlled variables 共同构成规格状态。 |
| 事件 / 触发 | 强支持 | `@T(c)`、`@F(c)` 和 monitored input events 是核心。 |
| 守卫 / 数据 | 强支持 | condition table / event table 都直接依赖变量与事件谓词。 |
| 层次 | 不支持 | 原文不是层次状态图，而是表格化同步状态机。 |
| 并发 / 同步 | 部分支持 | 通过同步 step semantics 统一处理输入，不是显式并发区。 |
| 时间约束 | 弱支持 | 本文聚焦安全需求与抽象模型检查，不是时间自动机。 |
| 连续动态 / 随机性 | 不支持 | 纯离散需求规格方法。 |
| 可执行 / 可验证性 | 强支持 | editor、simulator、consistency checker、`Spin` 集成齐全。 |

### 形式化问题与性质

1. `SCR` 最大的工程价值在于把需求规格收束成“可表格检查、可模拟、可模型检查”的对象。
2. condition table 与 event table 的完全性 / 互斥性要求，是 transform `T` 成为函数的关键。
3. abstraction 在这里不是可选优化，而是把大规格送进 model checker 的前提。
4. 对 transition invariant，一旦抽象是 sound / complete，就能在 abstract machine 上可靠地检查原规格性质。

## 构造方式与承载格式

### 建模入口

建模入口主要有三类：

1. variable dictionaries：定义 monitored、controlled、terms / modes。
2. condition tables / event tables：定义 dependent variables。
3. assertion dictionary：写安全性质。

### 机器可处理承载方式

机器可处理承载就是 `SCR` 自身的表格表示及其 conditional assignment 展开结果：

1. condition tables 描述同一状态中的函数关系。
2. event tables 描述跨两状态的历史相关更新。
3. abstraction 后的规格仍保持同样的表格结构。

### 交换与互操作

`SCR` 的互操作重点不在开放文件标准，而在工具链：

1. specification editor 维护表格规格。
2. dependency graph browser 用于导航与切片。
3. simulator、consistency checker 和 `Spin` 共享同一规格基础。

## 配套基础设施

- 建模/编辑工具：specification editor。
- 解析/交换/元模型支持：dependency graph browser 和表格语义展开。
- 仿真/执行支持：simulator 可符号执行规格。
- 验证/分析支持：consistency checker、`Spin` 集成、assertion checking。
- 代码生成/转换支持：论文重点是从 `SCR` 到 model checker 输入与抽象规格，而非直接代码生成。
- 标准化或社区生态：在高保证需求工程社区影响稳定，但不是通用交换标准。

## 适用场景与需求前提

### 适用场景

适合 avionics、space systems、核电控制、武器控制面板、电话网络等安全关键系统的需求规格与验证。

### 需求前提

1. 需求可整理成 monitored / controlled relation。
2. 系统行为能用离散同步 step semantics 表示。
3. 需要显式记录 latch、mode 或历史相关内部状态。
4. 需要 consistency checking、simulation 和 property checking 联动。

### 不适用或高成本场景

若需求高度连续、强并发且缺少清晰的输入事件边界，`SCR` 并不自然；若只需轻量流程图，不需要高保证分析，它也可能过重。

## 与相邻形式主义的关系

相对 `RSML / SpecTRM-RL` 这类状态图 / 表格结合的需求语言，`SCR` 更纯粹地站在 tabular notation 侧；相对 `Statecharts`，它没有层次状态图的表达自由，但更利于一致性检查与模型检查；相对一般 FSM，它通过 event operators、terms 和 mode classes 提供了更实用的需求规格层抽象。

## 与本研究的关系

### 对 Project 1 的价值

`SCR` 说明“状态机建模”在安全关键需求工程中完全可以不长成图，而长成一套可分析的表格状态机。这对 `project_1` 很重要，因为需求到模型的输出形态不必局限于图形状态图。

### 作为目标形式主义还是中间表示

对需求规格审查与高保证验证，它可以直接作为目标形式主义；在更一般的链路里，它也可以作为从自然语言需求到后端验证模型之间的中间表示。

### 对需求到模型生成的启发

1. monitored / controlled / term 的三层分解很适合做需求结构化。
2. 条件表和事件表是把静态逻辑与历史相关逻辑分开的好方式。
3. 若未来希望接模型检查，生成阶段就要主动控制变量依赖和状态空间。

## 重要的相关工作

- `Spin` 集成：说明 `SCR` 可直接进入 mainstream model checking workflow。
- 四变量模型：给 `SCR` 的 monitored / controlled relation 提供了理论来源。
- 论文中提到的 `RSML`、`Modechart`、`Petri nets + TRIO`：构成 dual-language / requirements verification 的相邻路线。

## 文献分类总结

- 这是一篇 `📦` 类需求规格 / 工具链条目，核心价值在“把安全关键需求状态机化，并做成可检查、可模拟、可模型检查的表格方法”。
- 它描述的对象是控制系统需求逻辑，因此记为 `🎛️`；应用场景是安全关键控制与工业装置，因此记为 `🏭`。
- 对 `project_1` 来说，它提供了一个很重要的参照：状态机目标形式不仅可以是图，也可以是高约束表格 DSL。
