# 用定时自动机改写机器人计划以满足平台时序约束 / Transforming Robotic Plans with Timed Automata to Solve Temporal Platform Constraints

## 基本信息

- 标题：Transforming Robotic Plans with Timed Automata to Solve Temporal Platform Constraints
- 中文标题：用定时自动机改写机器人计划以满足平台时序约束
- 作者：Tarik Viehmann, Till Hofmann, Gerhard Lakemeyer
- 发表：*Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence (IJCAI-2021)*, pp. 2083-2089, 2021
- DOI：`10.24963/ijcai.2021/287`
- 链接：https://doi.org/10.24963/ijcai.2021/287
- 形式主义：`Timed Automata + MTL-Constrained Plan Transformation`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：机器人平台时序约束求解 / 定时自动机应用建模
- 工具/实现获取方式：原文公开 `taptenc` 原型，并使用 `UPPAAL verifyta` 求解 reachability 与 concrete trace。
- 标准/格式获取方式：承载方式是 plan `P`、platform `TA`、`MTL` 约束和编码后的 `A_enc`；原文未提供统一交换格式。

## 简报

这篇论文的核心想法很实用：高层规划器可以继续忽略底层平台细节，但在真正执行前，先用定时自动机把这些平台约束补回来。作者把相机预热、抓取前扫描、夹爪校准、机器通信等平台细节建成 `TA`，再把“某个高层动作前后必须满足什么时序关系”写成一小段 `MTL`。之后，他们把抽象计划和平台模型一起编码成一个 reachability 问题，求出一条既保留高层计划意图、又满足平台时序约束的可执行 trace。

- 形式主义定位：面向 plan-to-execution bridge 的 `Timed Automata` 应用模型，而不是一般时序逻辑教程。
- 构造方式简述：先把抽象计划编码成 `TA`，再加入 platform automata 和 `MTL` 约束，最终在 `UPPAAL` 中做 reachability。
- 基础设施与场景简述：依托 `taptenc`、`UPPAAL verifyta`、`MTL` 约束编码和机器人平台组件模型，服务 `RoboCup Logistics` 与 domestic service robot 两类场景。

```text
抽象 plan -> plan TA -> 平台 TA + MTL 约束 -> 编码后的 reachability TA -> UPPAAL 求 trace -> 可执行平台动作序列
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象包括：

1. 抽象高层计划 `P = \langle a_1,\ldots,a_n \rangle`。
2. 平台组件的 timed automata。
3. 连接高层动作与底层状态的 `MTL` 约束。
4. 编码后用于 reachability 的统一自动机 `A_enc`。
5. 从 symbolic trace 解码出的 concrete execution trace。

### 核心抽象

原文使用的 timed automaton 骨架是：

$$
A = (L, l_0, E, I)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `l_0` 是初始 location。
3. `E` 是带 guard、action 与 reset 的迁移集合。
4. `I` 是 location invariant 映射。

计划动作之间的绝对/相对时序约束被写成 `MTL` 宏。原文给出的两个关键模板是：

$$
abs(i, I) := F_I \mathrm{PlanOrder}(i)
$$

$$
rel(i, j, I) := F\bigl(\mathrm{PlanOrder}(i) \land F_I \mathrm{PlanOrder}(j)\bigr)
$$

上式中的符号逐项解释如下：

1. `PlanOrder(i)` 表示“当前是计划中的第 `i` 个动作”。
2. `I` 是允许的时间区间。
3. `abs(i, I)` 约束第 `i` 个动作的开始时间。
4. `rel(i, j, I)` 约束第 `i` 个动作与第 `j` 个动作之间的相对时间间隔。

论文最后把所有约束压成一个 reachability 任务：

$$
\exists \rho \text{ satisfying } C_{abs} \cup C_{rel} \cup C_{uc}
\iff
\mathrm{Reach}_{A_{enc}}(\mathrm{fin})
$$

上式中的符号逐项解释如下：

1. `C_abs` 是绝对时间约束集合。
2. `C_rel` 是相对时间约束集合。
3. `C_uc` 是平台控制类 until-chain 约束集合。
4. `A_enc` 是编码后的总自动机。
5. `fin` 是目标终止状态。

### 一个最小例子与通俗解释

论文里最直观的例子是抓取前打开相机：

1. 高层计划只写 `spick` 和 `epick`，并不关心相机预热。
2. 平台模型中，相机需要经历 `off -> warm-up -> running`。
3. `MTL` 约束要求：抓取动作开始前，平台必须提前若干秒进入 `running`。
4. 转换器于是会自动在原计划前插入 `boot` / `warm-up` 一类平台动作，并给出合法执行时刻。

通俗地说，它像一层“计划补时序胶水”：高层只管说“去抓东西”，这层胶水负责把“先开相机、等预热、再抓”补齐，而且保证时间上真的可行。

### 运行 / 接受 / 转移语义

定时自动机的语义仍遵循标准 clock-based 运行方式：状态是配置 `\langle l, \nu \rangle`，其中 `l` 是 location，`\nu` 是 clock valuation。只有在 guard 满足、且执行 reset 后仍满足目标 invariant 的情况下，迁移才能发生。

论文的 plan encoding 还引入了 reachability 目标：

$$
\langle l, \nu \rangle \xrightarrow{e} \langle l', \nu' \rangle
$$

上式中的符号逐项解释如下：

1. `e` 是 `TA` 的一条边。
2. `\nu` 满足当前 guard 后，允许跳转。
3. `\nu'` 是执行 reset 后的新 clock valuation。
4. 通过 reachability，可以从解空间中找到满足所有时序约束的一条具体 trace。

### 语义边界

这篇论文的边界相当明确：

1. 它假设高层计划动作与平台动作可分层，不直接修改规划器内部语义。
2. 平台细节必须能建成有限个 `TA`，并能写成 `MTL` 关系。
3. 它处理的是时序可执行性，不是连续动力学或概率可靠性。
4. 若平台约束依赖复杂数据流、非定量知识或连续控制律，本方法就不够。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 定时自动机 | `$A = (L, l_0, E, I)$` | 平台组件的时序骨架。 |
| 绝对时间约束 | `$abs(i, I) := F_I \mathrm{PlanOrder}(i)$` | 限定第 `i` 个计划动作何时能发生。 |
| 相对时间约束 | `$rel(i, j, I)$` | 限定两个计划动作之间的时间间隔。 |
| 编码目标 | `$\mathrm{Reach}_{A_{enc}}(\mathrm{fin})$` | 把可执行性问题转成 reachability。 |
| 解码结果 | timed trace | 从 symbolic trace 还原高层动作和平台动作的具体时刻。 |
| 复杂度 | PSPACE-complete reachability | 继承标准 `TA` reachability 的判定难度。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 平台组件状态和 plan steps 都是一等对象。 |
| 事件 / 触发 | 强支持 | 高层动作、平台动作和状态标签都进入约束。 |
| 守卫 / 数据 | 部分支持 | 主要靠 clock guards 和原子命题，不做复杂数据推理。 |
| 层次 | 弱支持 | 重点不在层次结构。 |
| 并发 / 同步 | 部分支持 | 多平台组件可用 product 合成，但论文重点是时序约束。 |
| 时间约束 | 强支持 | `MTL` + clocks 是本文核心。 |
| 连续动态 / 随机性 | 不支持 | 不处理连续系统与概率行为。 |
| 可执行 / 可验证性 | 强支持 | 直接生成 `UPPAAL` reachability 问题并解码执行 trace。 |

### 形式化问题与性质

1. 这篇论文把“计划后处理”做成了标准 `TA` reachability，而不是 ad hoc scheduler。
2. `MTL` 约束在这里不是验证性质，而是 plan 与 platform 之间的桥接语言。
3. 编码后的 `TA` 显式包含了平台动作插入点，因此结果可直接用于执行。
4. 其工程价值在于不需要把底层平台细节塞回高层 planning domain。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 给出抽象计划 `P`。
2. 给出若干 platform components 的 `TA`。
3. 用 `MTL` 写 `abs / rel / uc` 三类约束。
4. 通过 `taptenc` 把它们编码成统一的 `A_enc`。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. 抽象计划序列。
2. `TA` 位置、时钟、guard、reset。
3. `MTL` 约束模板。
4. 编码后的 `UPPAAL` 模型与 symbolic trace。

### 交换与互操作

互操作重点在于：

1. 高层计划与平台组件要使用可对齐的动作字母表。
2. 平台约束必须能被翻译成 `TA` 与 `MTL`。
3. 最终结果要能从 `UPPAAL` symbolic trace 解码回平台动作序列。

## 配套基础设施

- 建模/编辑工具：原文公开 `taptenc`，并使用 `UPPAAL verifyta` 求解。
- 解析/交换/元模型支持：以 `TA` 和 `MTL` 编码为主，未给独立标准 schema。
- 仿真/执行支持：从 reachability trace 解码出 concrete action sequence。
- 验证/分析支持：`UPPAAL` reachability analysis。
- 代码生成/转换支持：核心贡献就是从 abstract plan 到 executable trace 的转换。
- 标准化或社区生态：依托 `Timed Automata`、`UPPAAL` 和 temporal planning 研究生态。

## 适用场景与需求前提

### 适用场景

适合平台约束明显、但高层规划又不想被底层细节污染的机器人系统，例如感知预热、校准、机器通信、家务机器人动作前置流程等。

### 需求前提

1. 高层行为已能给出有限计划序列。
2. 平台组件能建成有限 `TA`。
3. 关键时序依赖能写成 `MTL` 片段。
4. 可以接受把求解转化为离线或准在线 reachability 分析。

### 不适用或高成本场景

如果系统需要在连续动力学、概率故障或大规模不确定时延上做严谨分析，这条 `TA + MTL` 路线还不够。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文是面向机器人执行约束的工程化落地；相对 [multi-robot-planning-a-timed-automata-approach/desc.md](../multi-robot-planning-a-timed-automata-approach/desc.md)，它不直接把任务规划本身写成 `TA` 网络，而是把已有 plan 转成 platform-aware trace；相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，它更强调“计划补约束”而不是中间件消息时序验证。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求已经生成了高层状态机或计划后，仍然可以再用 timed automata 层做一次平台约束补全，而不必把所有底层细节都前置到初次建模。

### 作为目标形式主义还是中间表示

对平台时序协调问题，它可以直接作为目标形式主义；对更一般的控制系统，它非常适合作为“高层行为模型到执行约束模型”的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应区分高层任务动作和平台约束动作。
2. LLM 生成高层计划后，可再补一层 `TA` 编码来吸收感知、执行器和通信时序。
3. 对机器人系统，“计划正确”和“计划可执行”是两层不同问题，后者很适合 timed automata 接管。

## 重要的相关工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：定时自动机理论基础。
- [multi-robot-planning-a-timed-automata-approach/desc.md](../multi-robot-planning-a-timed-automata-approach/desc.md)：另一条多机器人任务规划的 `TA` 路线。
- [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：中间件通信与 callback 时序验证路线。

## 文献分类总结

- 这是一篇 `⏱️` 类高价值应用条目，核心贡献是把平台时序约束重写成 `Timed Automata` reachability。
- 其描述客体是机器人执行控制与动作插入，因此记为 `🎛️`；论文语境是具身机器人平台执行，因此记为 `🌡️`。
- 对 `project_1` 来说，它补足了“抽象行为模型之后，如何再接一层平台时序约束”的重要桥梁。
