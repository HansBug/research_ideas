# 定时系统的组合式规约：教程 / The Compositional Specification of Timed Systems --- A Tutorial

## 基本信息

- 标题：The Compositional Specification of Timed Systems --- A Tutorial
- 中文标题：定时系统的组合式规约：教程
- 作者：Joseph Sifakis
- 发表：收录于 *Computer Aided Verification*, LNCS 1633, pp. 2-7, 1999
- DOI：`10.1007/3-540-48683-6_2`
- 链接：https://doi.org/10.1007/3-540-48683-6_2
- 形式主义：`Timed Actions / Timed Automata with Deadlines`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型教程
- 工具/实现获取方式：原文未给公开实现；机器可处理入口是 timed action tuple、priority choice、synchronization 和 deadline-based composition。
- 标准/格式获取方式：原文没有交换标准，核心承载方式是 `(a,g,d,f)` timed action、带 clocks 的 transition-system semantics 与组合代数。

## 简报

这篇教程把 `Timed Systems` 的组合式建模压缩到一个非常清晰的 deadline 视角里：每个 transition 不只带 guard，还带 deadline；deadline 蕴含 guard，并表示“从 enabled 到必须执行”的 urgent 区域。作者据此把 timed system 写成 timed actions 的代数，并围绕 `time reactivity` 与 `activity preservation` 讨论 priority choice、parallel composition、lazy/eager/delayable action 等构造。对演化树而言，这篇条目最适合稳定挂成 `Timed Automata` 主干下的 `Timed Actions / Timed Automata with Deadlines` 分支节点。

- 形式主义定位：用 `deadline` 显式表达 urgency 的 compositional timed-system 形式主义，可视为 `Timed Automata` 家族中 deadline-based 组合分支。
- 构造方式简述：把一个 timed action 写成 `(a,g,d,f)`，再用 choice、priority 和 synchronization 把多个 timed action 组合成完整 timed system。
- 基础设施与场景简述：原文偏理论与代数语义，但它给出了 deadline、priority、parallel composition 和 delayable action 的非常稳定骨架。

```text
untimed action -> guard + deadline + clock update -> timed action -> priority / synchronization / composition -> timed system
```

## 形式主义定义与核心对象

### 定义对象

论文关心的是带全局时间概念的 executable timed formalisms，尤其是如何在组合时既表达 urgency，又避免 timelock。

### 核心抽象

它把一个最小 timed primitive 定义成 `timed action`：

$$
\alpha = (a,g,d,f)
$$

上式中的符号逐项解释如下：

1. `a` 是动作名。
2. `g` 是 guard，表示动作可被执行的 clock valuation 集。
3. `d` 是 deadline，表示动作变得 urgent 的 valuation 集。
4. `f` 是动作执行后对 clocks 的更新函数。

论文的硬约束是：

$$
d \Rightarrow g
$$

也就是 deadline 必须蕴含 guard。换句话说，动作只有在本来就 enabled 的前提下，才可能进一步变成 urgent。

### 一个最小例子与通俗解释

最小例子可以取“动作 `a` 在 `x \ge 3` 后可执行，但最迟到 `x \ge 5` 就必须执行”。这时 guard 可以是 `g: x \ge 3`，deadline 可以是 `d: x \ge 5`。于是系统在 `3` 到 `5` 之间可以等，也可以做；一旦达到 `5`，若还不做就违反 timed action 语义。

通俗地说，普通 `Timed Automata` 常把 urgency 藏在 location invariant 里，而这里直接说“这条边的 deadline 是什么”。因此它更像“边优先”的 timed 建模：先想清楚每个动作什么时候允许发生、什么时候必须发生，再去谈组合。

### 运行 / 接受 / 转移语义

论文把 timed formalism 的状态都视为 control state 与 clock valuation 的二元组：

$$
(s,v)
$$

其中 `s` 是离散控制状态，`v` 是当前 clocks 赋值。时间步和 timeless transition 都在这个层面定义。相对于普通 timed transition systems，这里最关键的是 deadline 对 time progress 的限制：若某动作 deadline 已达到，则时间不能再继续流逝而必须让某个动作发生。

### 语义边界

这条线和一般 `Timed Automata` 的区别，不在“有没有 clocks”，而在“urgency 是挂在状态上还是挂在边上”。论文明确主张用 transition-level deadlines 来表达 urgency，并把这件事做成 compositional algebra。

### 关键性质与判定边界

原文没有给出一条单独的复杂度定理，但它稳定给出了两个 sanity properties：

$$
\text{time reactivity}
$$

和

$$
\text{activity preservation}
$$

作者证明 priority choice 与 parallel composition 可以在适当条件下保留这两条性质。此外，priority choice 还能通过限制低优先级动作的 guard / deadline 来表达，不必把 priority 当成完全外加的元机制。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 通过 control state `s` 与 transition-based action system 给出。 |
| 事件 / 触发 | 强支持 | 每个 timed action 直接以动作名 `a` 为核心。 |
| 守卫 / 数据 | 强支持时钟守卫 | `g` 与 `d` 都是 clocks 上的谓词。 |
| 层次 | 不支持 | 原文核心不是层次结构。 |
| 并发 / 同步 | 强支持 | 平行组合、同步模式和 choice 是论文重点。 |
| 时间约束 | 强支持 | deadline 直接编码 urgency。 |
| 连续动态 / 随机性 | 不支持 | 仍是离散状态 + clocks 的 timed 语义。 |
| 可执行 / 可验证性 | 强理论支持 | composition laws、time reactivity 和 activity preservation 是其核心分析目标。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed action | `$\alpha=(a,g,d,f)$` | deadline-based timed primitive。 |
| urgency 约束 | `$d \Rightarrow g$` | deadline 不能超出 guard 的使能区域。 |
| 状态骨架 | `$(s,v)$` | control state + clock valuation 的统一语义入口。 |
| lazy / eager / delayable | `$d=\emptyset$`, `$d=g$`, `$d=\mathrm{fall}(g)$` | 三类典型 urgency 口径。 |
| sanity properties | `time reactivity`, `activity preservation` | 组合式 timed semantics 的两条基本正确性要求。 |

## 构造方式与承载格式

### 建模入口

1. 先把系统拆成基本 timed actions。
2. 对每个动作写出 guard、deadline 和 clock update。
3. 再决定不同动作之间是 nondeterministic choice、priority choice 还是 synchronization。
4. 最后检查组合后是否仍满足 `time reactivity` 与 `activity preservation`。

### 机器可处理承载方式

机器可处理承载方式是 timed action tuple、transition-system semantics 和基于 action algebra 的组合律，而不是某种 XML/DSL 文件。

### 交换与互操作

它与 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的基础 `TA` 母线直接相连，也为 [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md) 的 urgent 分支提供了更早的 deadline-based urgency 参考。相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，这里更重 compositionality，而不是 determinization。

## 配套基础设施

- 建模/编辑工具：原文未提供公开工具。
- 解析/交换/元模型支持：核心是 `(a,g,d,f)` timed action 与 timed-system algebra。
- 仿真/执行支持：可通过 timed transition systems 执行时间步和动作步。
- 验证/分析支持：priority choice、parallel composition、synchronization、timelock avoidance 和 compositional reasoning。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 Verimag deadline-based timed-specification 线的重要整理节点。

## 适用场景与需求前提

### 适用场景

适合带 urgency、priority、同步等待和 timelock 风险的 compositional timed-system 规格，尤其是多个局部 timed component 需要组合时。

### 需求前提

1. 需求必须能先拆成离散动作。
2. 每个动作都需要清晰地区分“何时可做”和“何时必须做”。
3. 系统正确性至少部分依赖组合时是否保持 time reactivity 与 activity preservation。

### 不适用或高成本场景

若系统主要关心单个自动机的 reachability，而不是组合代数与 urgency discipline，这套 timed-action 视角可能显得过重。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，它把 urgency 从 location invariant 风格进一步压到 transition deadlines 上；相对 [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)，这里强调 deadline 与 compositional algebra，后者则给出另一种“从 enabling time 起算固定窗口”的 urgent semantics；相对 [the-impressive-power-of-stopwatches/desc.md](../the-impressive-power-of-stopwatches/desc.md)，它仍停留在纯 clock timed systems，不进入暂停时钟或 hybrid 表达力。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Timed Automata` 主干上的 urgency 语义前推成一个更清楚的 `deadline / timed action` 子枝，这比继续补 timed 应用条目更直接服务于演化树。

### 作为目标形式主义还是中间表示

非常适合作为中间表示：先把自然语言需求抽成 timed actions，再决定是否下沉到更具体的 `TA`、`UPPAAL` 或其他工具输入。

### 对需求到模型生成的启发

当需求中频繁出现“可等待多久”“最迟何时必须做”“谁压过谁的优先级”时，LLM 先产出 `(a,g,d,f)` 级别表示，比直接产出完整 automaton 往往更稳。

### 现实限制

原文主要是教程与语义整理，没有给出统一工程交换格式；落地时仍需要后续转换层。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)
- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合挂成 `Timed Automata -> Timed Actions / Timed Automata with Deadlines` 的组合语义分支。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Timed Actions / Timed Automata with Deadlines`
- 论文角色：模型教程
- 核心功能：把 deadline-based urgency、priority 和 synchronization 统一成可组合的 timed-action 代数。
- 关键特性：`(a,g,d,f)`、`d => g`、time reactivity、activity preservation、lazy/eager/delayable actions。
- 构造方式：timed action tuple + choice / priority / parallel composition。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：需要显式 urgency / priority / timelock avoidance 的组合式 timed 规格。
- 需求前提：动作边界、deadline 和同步关系都能明确写成 clocks 上的约束。
- 状态：🟢
