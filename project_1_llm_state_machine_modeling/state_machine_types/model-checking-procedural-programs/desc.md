# 过程程序的模型检验 / Model Checking Procedural Programs

## 基本信息

- 标题：Model Checking Procedural Programs
- 中文标题：过程程序的模型检验
- 作者：Rajeev Alur、Ahmed Bouajjani、Javier Esparza
- 发表：*Handbook of Model Checking*, pp. 541-572, 2018
- DOI：`10.1007/978-3-319-10575-8_17`
- 链接：https://www.cis.upenn.edu/~alur/hmch13.pdf
- 形式主义：`Extended Recursive State Machines (ERSM) / Recursive State Machines (RSM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：手册级 formalization / `ERSM` 与 procedural-program bridge
- 工具/实现获取方式：原文明确把 `Bebop/SLAM`、`MOPED/jMOPED` 与 `WALi` 作为 reachability、saturation 与 inter-procedural analysis 的代表实现线索。
- 标准/格式获取方式：原文没有 DSL、XML 或交换标准；机器可处理入口是 `ERSM -> RSM -> PDS` 这条 tuple / transition 级形式化链路。

## 简报

这篇手册章节的真正价值，不是再讲一次一般性的“程序模型检验”，而是把 `while program -> extended state machine -> procedural program -> ERSM -> RSM -> PDS` 这条层次化控制流母线写得非常清楚。对当前文库来说，它最有价值的部分是：它把 `ERSM` 明确固定成 `RSM` 的有限数据化分支，并再次强调“若 state-machine dependency 无环，就是 `HSM`；若允许递归调用，就是 `RSM/ERSM`”。

- 形式主义定位：`Statecharts -> HSM -> uHSM -> RSM -> ERSM` 这条线上的 procedural-program presentation。
- 构造方式简述：先用 control points、guards、assignments 建 extended state machine，再把 procedure calls 变成 boxes 与 ports，最后通过 valuation flattening 得到 ordinary `RSM`。
- 基础设施与场景简述：原文虽是 handbook chapter，但直接把 `SLAM/Bebop`、`MOPED/jMOPED`、`WALi` 这几条经典工具线和 summarization / saturation 语义放在一起，适合作为 `ERSM` 节点的整理锚点。

```text
procedural program -> ERSM -> flattened RSM -> pushdown system -> reachability / fair computation / model checking
```

## 形式主义定义与核心对象

### 定义对象

原文把过程程序看成“带有限变量的递归控制流”。它先说明普通 `while` 程序可用 extended state machines 表达，再指出带 procedure call 的程序已不能只靠一张平面状态图描述，因此必须进入 `RSM/ERSM` 口径。

### 核心抽象

对带变量的局部控制图，原文先给出“展平后节点”的核心记法：

$$
u=\langle \ell,\nu \rangle
$$

上式中的符号逐项解释如下：

1. `\ell` 是 extended state machine 中的一个控制点。
2. `\nu` 是变量集合 `V` 上的一个 valuation。
3. `u` 是 flattening 之后 ordinary state machine 或 ordinary `RSM` 中的节点。

原文随后正式定义 ordinary `RSM`：

$$
M=(A_1,\ldots,A_k),\qquad A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `A_1,\ldots,A_k` 是各个组件，对应不同 procedures。
2. `N_i` 是组件 `A_i` 的节点集。
3. `B_i` 是组件中的 boxes，也就是“调用另一个组件”的位置。
4. `Y_i:B_i\to\{1,\ldots,k\}` 指定每个 box 调到哪个组件。
5. `En_i` 与 `Ex_i` 分别是 entry / exit 节点集合。
6. `\delta_i` 是组件内部的转移集合。

原文明确指出：`RSMs with acyclic dependencies among state machines are called hierarchical state machines`。因此这里的 `ERSM` 不另起新主线，而是把 `RSM` 接到有限数据程序抽象上。

### 一个最小例子与通俗解释

原文图 2 给的是一个很典型的例子：`P1` 和 `P2` 两个 procedure，共享全局布尔变量 `x,y`。

1. `P1` 在某个 control point 上调用 `P2`。
2. 组件 `A_1` 中于是出现一个标记为 `A_2` 的 box。
3. box 不直接“吞掉”整个被调过程，而是通过 call port 进入 `A_2` 的 entry，再通过 return port 从 `A_2` 的 exit 回来。
4. 若把变量 valuation 也并入节点，就得到 ordinary `RSM` 的 `\langle \ell,\nu \rangle` 节点。

通俗地说，`ERSM` 就像“给递归状态机再加一层有限变量解释”。`RSM` 负责 call/return 结构，变量 valuation 负责把 guarded assignments 压进有限状态骨架，所以它特别适合 Boolean programs 这类“控制流递归 + 有限数据抽象”的对象。

### 运行 / 接受 / 转移语义

原文把 `RSM` 的 operational semantics 明确落到 `PDS`：

$$
P_M=(P_M,\Gamma_M,\Delta_M)
$$

上式中的符号逐项解释如下：

1. `P_M=N` 是所有 ordinary nodes 的集合。
2. `\Gamma_M=B` 是所有 boxes，作为 stack alphabet。
3. `\Delta_M` 是 pushdown rules，对应 ordinary `RSM` 的四类转移。

调用与返回的关键直觉是：

1. 进入 box 时，把该 box 压栈。
2. 从被调组件的 exit 返回时，把 box 弹栈。
3. 因此 configuration 不只是当前节点，还包含未返回调用的 box 序列。

原文对 `PDS` configuration 的记法可压成：

$$
c = ps,\qquad p\in P,\ s\in \Gamma^*
$$

上式中的符号逐项解释如下：

1. `p` 是当前 control state。
2. `s` 是当前调用栈，对应尚未退出的 box 序列。
3. `c` 是程序在 call/return 语义下的一个完整执行状态。

### 语义边界

这一 family 的边界在原文里非常清楚：

1. `ERSM` 仍要求变量域是有限的，或已经被 Boolean / finite-range abstraction 压成有限域。
2. 若 component dependency 无环，就退化成 `HSM`。
3. 若允许递归调用，就必须进入 `RSM/PDS` 栈语义。
4. 它不处理概率、时间或连续动力学；那些都属于后续 sibling 分支。

### 关键性质与判定边界

原文把三类基础问题固定了下来：

$$
p \xRightarrow{*} qs
$$

上式中的符号逐项解释如下：

1. `p` 是某个 entry node。
2. `q` 是目标节点。
3. `s` 是某个 stack word。
4. 该式表示 state reachability，即从 `p` 是否能到达某个以 `q` 为控制点的 configuration。

对应地，原文系统区分：

1. state reachability；
2. configuration reachability；
3. fair computation。

更重要的是，这一章把两条经典分析路线并列固定下来：

1. summarization：更像求 entry-to-exit / control-location 级摘要信息；
2. saturation：直接计算可达 configurations 的有限自动机表示。

因此它虽然是手册章节，但对 `ERSM` 节点来说不是“二手综述”，而是一个把 family、语义和基础设施重新捏合到一起的主入口。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 普通节点、entry/exit、box、call/return 都是模型本体的一部分。 |
| 事件 / 触发 | 中等支持 | 原文更强调程序控制流与 guarded commands，而不是独立事件字母表。 |
| 守卫 / 数据 | 强支持 | `ERSM` 正是把有限变量 valuation、guards 和 assignments 纳入 `RSM`。 |
| 层次 | 强支持 | procedure/component/box 形成显式层次。 |
| 并发 / 同步 | 不支持 | 讨论的是 sequential procedural programs。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 无 ODE、无概率。 |
| 可执行 / 可验证性 | 强理论支持 | `ERSM -> RSM -> PDS` 之后可做 summarization、saturation 与 temporal verification。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| flattening 节点 | `$u=\langle \ell,\nu\rangle$` | 把控制点与有限 valuation 合并成 ordinary node。 |
| `RSM` 骨架 | `$M=(A_1,\ldots,A_k)$` | procedural hierarchy 的核心元组。 |
| component tuple | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)$` | box、entry/exit 与 call/return 结构的最小骨架。 |
| `PDS` 语义 | `$P_M=(P_M,\Gamma_M,\Delta_M)$` | 把 `RSM` 的执行语义落到 pushdown system。 |
| reachability | `$p \xRightarrow{*} qs$` | 区分 state-level 与 configuration-level reachability。 |

## 构造方式与承载格式

### 建模入口

1. 先按 procedures 划分组件。
2. 再把每个 procedure 的 control points 编成 component graph。
3. 用 boxes 表达 procedure call。
4. 最后把有限变量 valuation 展平进节点，得到 ordinary `RSM`。

### 机器可处理承载方式

机器可处理承载方式主要是：

1. `ERSM/RSM` tuple；
2. call / return ports；
3. valuation flattening；
4. `PDS` rules。

### 交换与互操作

原文没有标准交换格式，但理论互操作非常强：

1. 向上衔接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 `HSM`。
2. 向旁边衔接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 ordinary `RSM`。
3. 向下直接接到 `PDS`、nested words 与 procedure-aware temporal logics。

## 配套基础设施

- 建模/编辑工具：原文提到 `SLAM/Bebop`、`MOPED/jMOPED`、`WALi`。
- 解析/交换/元模型支持：核心是 `ERSM/RSM/PDS` 之间的系统化转换。
- 仿真/执行支持：`PDS` configuration semantics 可直接执行。
- 验证/分析支持：summarization、saturation、fair computation、temporal verification。
- 代码生成/转换支持：原文不讨论代码生成，但讨论从 procedural program abstraction 到 `ERSM/RSM/PDS` 的形式化落地。
- 标准化或社区生态：属于 recursive-state-machine / pushdown / software verification 交叉地带的经典理论入口。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流建模。
2. Boolean programs 或有限数据程序抽象。
3. 希望把 hierarchy 明确落成 call/return 语义的需求到模型映射。

### 需求前提

1. 变量域必须有限，或已被抽象成有限域。
2. 系统复杂度主要来自 procedure hierarchy，而不是并发、时间或连续过程。
3. 需求需要保留调用栈上下文，而不是只看单层控制点。

### 不适用或高成本场景

如果系统本质上是概率递归过程，应转向 `RMC/RMDP`；如果需求含时间或连续动力学，应转向 `RTA/RHA`；如果只是普通平面有限状态控制流，`FSM/EFSM` 更轻。

## 与相邻形式主义的关系

相对 `HSM`，`ERSM` 的关键新增点是显式 call/return；相对 ordinary `RSM`，它又把有限变量 valuation、guard 和 assignment 纳入模型本体；相对 `PDS`，它更保留 procedure/component 的工程直觉，而不是只留下栈符号重写。

## 与本研究的关系

### 对 Project 1 的价值

它说明了一个很关键的事实：当需求里出现“子过程调用 + 有限模式变量 + 调用结束后继续执行”时，最自然的目标并不是平面 `FSM`，而是 `ERSM/RSM`。

### 作为目标形式主义还是中间表示

更适合作为高层需求到程序化控制流模型之间的中间表示，也可直接作为形式验证目标模型。

### 对需求到模型生成的启发

如果 LLM 从需求中已经识别出 procedures、局部调用和有限变量，那么让它直接生成 `ERSM` 往往比先写扁平 `Statecharts` 再事后恢复调用栈更自然。

## 重要的相关工作

1. [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)：`HSM` 母线。
2. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：ordinary `RSM` 的 journal-level 整理。
3. [on-the-fly-reachability-and-cycle-detection-for-recursive-state-machines/desc.md](../on-the-fly-reachability-and-cycle-detection-for-recursive-state-machines/desc.md)：`ERSM` 的原始 formal model 条目。

## 文献分类总结

- 这篇论文属于 `🧩 经典离散状态机`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🎛️ 控制 / 反应式逻辑`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> ERSM` 这条线下，作为 `ERSM` 的 handbook-level 稳定表述，而不是另起新的 DSL 或应用分支。
