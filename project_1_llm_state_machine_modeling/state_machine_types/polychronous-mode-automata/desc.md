# 多时钟模式自动机 / Polychronous Mode Automata

## 基本信息

- 标题：Polychronous Mode Automata
- 中文标题：多时钟模式自动机
- 作者：Jean-Pierre Talpin, Christian Brunette, Thierry Gautier, Abdoulaye Gamatié
- 发表：Proceedings of the 6th ACM & IEEE International Conference on Embedded Software (EMSOFT 2006), 83-92, 2006
- DOI：`10.1145/1176887.1176900`
- 链接：https://doi.org/10.1145/1176887.1176900
- 形式主义：Polychronous Mode Automata / `Signal`-based mode automata
- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：多时钟建模构件 / 元模型扩展
- 工具/实现获取方式：原文明确依托 `Polychrony` workbench、`Signal-Meta` 和 `GME`，通过 model transformation 把图形 mode automata 生成到 `Signal`。
- 标准/格式获取方式：承载方式是 `GME` 元模型、`Signal` 方程和 mode automata 图结构；原文未给出独立行业交换标准。

## 简报

这篇论文的核心不是再造一个普通状态机，而是把 `Signal/Polychrony` 的多时钟同步数据流语义，和 `mode automata` 的控制流结构拼到一起。作者用它解决的是嵌入式系统尤其是 `IMA` 航电应用里“既有局部时钟、又有控制模式切换、还要进模型驱动工具链”的问题。

- 形式主义定位：面向多时钟嵌入式系统的状态机+数据流复合建模构件。
- 构造方式简述：在 `Signal` 多时钟方程之上叠加 `mode automata`，再通过 `GME` 元模型和解释器生成 `Signal` 代码。
- 基础设施与场景简述：服务 `Polychrony` 工具链、模型变换和嵌入式/航电设计流程。

```text
嵌入式需求 -> 多时钟数据流 + mode automata -> GME / Signal-Meta / Polychrony -> 形式分析 / 代码生成前端
```

## 形式主义定义与核心对象

### 定义对象

论文要描述的是“带局部时钟的控制模式切换系统”。也就是：控制流部分像层次状态机，计算部分像多时钟同步数据流，二者在同一个数学模型和工具链中被统一。

### 核心抽象

论文直接给出了 mode automata 的核心语法骨架：

$$
a,b ::= init\ s \mid (s:p) \mid (e \Rightarrow s \to t) \mid (e \Rightarrow s \triangleright t) \mid a \parallel b
$$

上式中的符号逐项解释如下：

1. `init\ s` 指定 automaton 的初始 mode `s`。
2. `(s:p)` 表示 mode `s` 关联行为过程 `p`。
3. `e \Rightarrow s \to t` 是弱抢占迁移，表示条件 `e` 满足时把 next state 设为 `t`。
4. `e \Rightarrow s \triangleright t` 是强抢占迁移，表示进入 `s` 时若 `e` 成立就立即转到 `t`。
5. `a \parallel b` 表示 automata 的同步并行组合。

与它叠加的 `Signal` 数据流方程包括：

$$
x = y\ \mathrm{pre}\ v, \quad x = y\ \mathrm{when}\ z, \quad x = y\ \mathrm{default}\ z
$$

上式中的符号逐项解释如下：

1. `pre` 是带初值的延迟方程。
2. `when` 是采样方程，仅在条件信号成立时输出。
3. `default` 是按信号出现性进行合并的方程。

论文还明确给出了把 automaton 编译到 `Signal` 的关键规则：

$$
C_x[[c \Rightarrow s \to t]] = [x=s] \land c \Rightarrow x' = t
$$

$$
C_x[[c \Rightarrow s \triangleright t]] = [(x' \ \mathrm{pre}\ s_0)=s] \land c \Rightarrow x=t
$$

上式中的符号逐项解释如下：

1. `x` 表示 automaton 的当前状态编码。
2. `x'` 表示 next-state 编码。
3. `[x=s]` 表示 automaton 当前处于状态 `s`。
4. `c` 是 guard 或时钟条件。
5. `s_0` 是初始状态。
6. 第一条规则编码弱迁移，第二条编码强迁移。

### 一个最小例子与通俗解释

论文用一个 crossbar switch 作为最小例子：

1. switch 有 `flip` 和 `flop` 两个 mode。
2. 当处于 `flip` 时，`x1=y1`、`x2=y2`。
3. 当 reset 信号 `r` 到来时，强抢占地从 `flip` 切到 `flop`。
4. 在 `flop` 下输出交换成 `x1=y2`、`x2=y1`。

通俗地说，这个模型像“给多时钟数据流图套上一层可抢占的模式壳”。模式决定当前哪组方程生效，而方程本身又保持 `Signal` 的多时钟同步语义。

### 运行 / 接受 / 转移语义

运行时，当前 mode 决定哪些 `Signal` 方程被激活；活跃 mode 的条件可以写成：

$$
[x=s] \Rightarrow G[[p]]
$$

其中：

1. `[x=s]` 表示当前 mode 为 `s`。
2. `G[[p]]` 表示把过程 `p` 展开成底层 `Signal` 方程。

论文还给出了 micro-step automata 的操作语义骨架：

$$
A = (s_0, S, X, \rightarrow)
$$

其中：

1. `s_0` 是初始状态。
2. `S` 是状态集合。
3. `X` 是通信信号集合。
4. `\rightarrow` 是带标签迁移关系。

### 语义边界

这个形式主义的边界很清楚：

1. 它强在多时钟同步控制与模型变换，不强在开放标准交换。
2. 它适合离散控制流与多时钟数据流混合，而不是一般连续动力学建模。
3. 论文的重点是元模型、编译和语义，而不是工业执行器本身。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| mode automata 语法 | `$a,b ::= init\ s \mid (s:p) \mid (e \Rightarrow s \to t) \mid (e \Rightarrow s \triangleright t) \mid a \parallel b$` | 状态、行为、弱/强抢占和并行组合是第一层骨架。 |
| 数据流核心方程 | `$x = y\ \mathrm{pre}\ v,\ x = y\ \mathrm{when}\ z,\ x = y\ \mathrm{default}\ z$` | `Signal` 提供多时钟同步数据流语义。 |
| 弱迁移编译 | `$C_x[[c \Rightarrow s \to t]] = [x=s] \land c \Rightarrow x' = t$` | 守卫满足时设置 next state。 |
| 强迁移编译 | `$C_x[[c \Rightarrow s \triangleright t]] = [(x' \ \mathrm{pre}\ s_0)=s] \land c \Rightarrow x=t$` | 强抢占在当前 instant 内改变当前 state。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `mode automata` 直接提供 mode、子 mode 和并行 automata。 |
| 事件 / 触发 | 强支持 | 迁移由 clock/guard 驱动，支持弱和强抢占。 |
| 守卫 / 数据 | 强支持 | 守卫、信号定义、采样/合并/延迟方程共同作用。 |
| 层次 | 强支持 | `Automaton`、`AndState`、`CompoundState` 形成层次图结构。 |
| 并发 / 同步 | 强支持 | automata 并行组合与 `Signal` 同步组合都被明确定义。 |
| 时间约束 | 强支持 | 核心就是多时钟同步语义。 |
| 连续动态 / 随机性 | 不支持 | 关注的是同步离散控制和数据流。 |
| 可执行 / 可验证性 | 强支持 | 可生成 `Signal` 代码，并交给 `Polychrony` 做分析、转换和验证。 |

### 形式化问题与性质

1. 模式切换不是附着在数据流上的口头注释，而是被显式编译成状态编码和 clock equations。
2. 强抢占与弱抢占在编译规则中被区分，适合嵌入式控制里的 immediate/deferred semantics。
3. `GME` 元模型把 `Automaton`、`State`、`StrongTransition`、`WeakTransition` 固化成可工具处理对象。
4. micro-step automata 语义使并发、因果和多时钟通信可被统一解释。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. `Signal` 数据流过程与方程。
2. `Automaton / State / AndState / CompoundState` 图形对象。
3. `StrongTransition / WeakTransition` 迁移。
4. `StateObserver` 与 clock 约束。

### 机器可处理承载方式

机器可处理承载有三层：

1. `GME` 中的元模型对象。
2. `Signal-Meta` 里的 `Signal` 进程和时钟关系。
3. 由解释器生成的 `Signal` 代码。

### 交换与互操作

论文重心是模型变换和语义保真，不是行业交换格式。互操作主要靠 `GME -> Signal -> Polychrony` 这一研究型工具链。

## 配套基础设施

- 建模/编辑工具：`GME` 与 `Signal-Meta`。
- 解析/交换/元模型支持：mode automata 作为 `Signal` 元模型的扩展被显式定义。
- 仿真/执行支持：通过生成 `Signal` 代码进入 `Polychrony` 工作台。
- 验证/分析支持：原文明确提到利用 `Polychrony` 做 formal verification、model checking 与 controller synthesis。
- 代码生成/转换支持：Interpreter 把图形模型编译成 `Signal` 方程。
- 标准化或社区生态：依托 `Signal/Polychrony` 和同步语言研究生态，工业通用标准较弱。

## 适用场景与需求前提

### 适用场景

适合 `IMA` 航电、分布式实时系统、SoC 和其他需要局部时钟、控制模式切换与同步数据流共存的嵌入式系统。

### 需求前提

1. 需求同时包含控制流模式和数据流计算。
2. 系统由多个局部时钟驱动，而不是单一全局周期。
3. 希望在模型驱动环境中做语义保真的自动转换。
4. 需要强/弱抢占、状态观察和层次化结构。

### 不适用或高成本场景

如果场景只有普通平面 `FSM`、没有多时钟问题，或者更需要开放运行时标准而不是研究型工具链，这个形式主义会显得过重。

## 与相邻形式主义的关系

相对 `Lustre/Signal`，它把模式切换和抢占显式化；相对 `Stateflow/SyncCharts`，它把控制流扎进多时钟同步数据流语义；相对经典 `Mode-Automata`，它更强调 `Polychrony` 式多时钟与元模型集成。

## 与本研究的关系

### 对 Project 1 的价值

它说明状态机不一定要单独存在。对复杂控制系统，更现实的目标往往是“状态机 + 数据流 + 多时钟”的联合中间表示。

### 作为目标形式主义还是中间表示

更适合作为面向嵌入式/同步工具链的中间表示；在 `Polychrony` 生态内部，也可以直接作为目标建模载体。

### 对需求到模型生成的启发

当需求中明显存在“模式切换”和“多个局部节拍/采样周期”时，生成多时钟 mode automata 会比平面状态图更接近真实实现。

### 现实限制

它依赖 `GME` 与 `Polychrony` 路线，跨生态共享能力弱于 `SCXML` 或 `UML` 这类更普及的标准。

## 重要的相关工作

### 奠基或前身工作

- `Signal`
- `Polychrony`
- 经典 `Mode-Automata`

### 同类型或同家族工作

- `SyncCharts`
- `Stateflow`
- `Lustre with automata`

### 标准 / 格式 / 工具链工作

- `Signal-Meta`
- `GME`
- `Polychrony` workbench

### 与本研究关系最紧的工作

- 它非常适合回答“需求里哪些时序/节拍信息应进入状态机结构，哪些应落到数据流/时钟层”这个问题。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：Polychronous Mode Automata
- 论文角色：多时钟建模构件 / 元模型扩展
- 核心功能：把多时钟同步数据流和 mode automata 统一进可编译、可验证的嵌入式建模前端。
- 关键特性：弱/强抢占、多时钟语义、元模型扩展、`Signal` 编译规则。
- 构造方式：`GME` 图形元模型 + `Signal` 方程 + `Polychrony` 工具链。
