# Supremica：面向大规模离散事件系统的高效工具 / Supremica--An Efficient Tool for Large-Scale Discrete Event Systems

## 基本信息

- 标题：Supremica--An Efficient Tool for Large-Scale Discrete Event Systems
- 中文标题：Supremica：面向大规模离散事件系统的高效工具
- 作者：Robi Malik，Knut Åkesson，Hugo Flordal，Martin Fabian
- 发表：*IFAC-PapersOnLine*，50(1):5794-5799，2017
- DOI：`10.1016/j.ifacol.2017.08.427`
- 链接：https://doi.org/10.1016/j.ifacol.2017.08.427
- 形式主义：`FSM / EFSM / Supervisory Control / Supremica`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：supervisory-control IDE / verifier / synthesiser
- 工具/实现获取方式：原文明确给出 `www.supremica.org`，并说明工具可免费用于教育与科研。
- 标准/格式获取方式：承载方式是 Supremica 图形 editor 中的 `FSM/EFSM`、parameterized modules、shared events、guards/actions 与 synthesis 结果；原文未给中立交换标准。

## 简报

这篇论文的价值，在于把监督控制理论里常见的 plant/specification/supervisor 流程做成了一套真能处理工业规模模型的 IDE。`Supremica` 不是单一分析算法论文，而是同时提供 editor、simulator、analyser、verification 和 synthesis 的工具载体，并把 `FSM` 与 `EFSM`、显式算法与 `BDD`、单体分析与 compositional abstraction 放到同一环境里。

- 形式主义定位：离散事件监督控制的工程工具链，而不是新的状态机族。
- 构造方式简述：用 `FSM/EFSM` 描 plant 与 specification，再由 shared events、guards/actions、modules 和 parameters 组成大模型，最后调用 controllability / nonblocking verification 与 supervisor synthesis。
- 基础设施与场景简述：依托图形建模、交互式 simulator、counterexample replay、`BDD` 和 compositional algorithms、以及面向 `PLC` 的 guard synthesis，服务工业控制和嵌入式离散事件控制函数开发。

```text
plant/specification FSM or EFSM -> shared-event synchronous model -> controllability/nonblocking check -> supervisor synthesis / guard extraction
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `Supremica`：

1. 普通 `FSM` 与带变量、guards、actions 的 `EFSM`。
2. plant 与 specification 两类状态机。
3. controllable / uncontrollable、observable / unobservable events。
4. simulator、analyser 与 synthesis backend。
5. 由 least restrictive controllable and nonblocking supervisor 表达的综合结果。

### 核心抽象

结合论文对 `EFSM` 的描述，可把单个扩展状态机保守整理为：

$$
E = (Q, q_0, \Sigma, V, \rightarrow)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `q_0` 是初始状态。
3. `\Sigma` 是事件集合。
4. `V` 是有限整型区间或枚举型变量集合。
5. `\rightarrow` 是带 event、guard、action 的迁移关系。

单条 `EFSM` 迁移可写成：

$$
q \xrightarrow{e[g]/a} q'
$$

上式中的符号逐项解释如下：

1. `e` 是触发事件。
2. `g` 是 guard formula。
3. `a` 是 action/update。
4. `q'` 是目标状态。

监督控制的综合目标则可保守写成：

$$
K^\star = \sup \{ K \subseteq L(P \parallel S) \mid K\ \text{controllable and nonblocking} \}
$$

上式中的符号逐项解释如下：

1. `P` 是 plant model。
2. `S` 是 specification model。
3. `P \parallel S` 表示基于 shared events 的同步组合。
4. `L(P \parallel S)` 是系统可实现行为语言。
5. `K^\star` 是最宽松、仍满足 controllable 且 nonblocking 的目标行为。

### 一个最小例子与通俗解释

论文用 distributed prime sieve 的 `EFSM` 片段解释 guards/actions：

1. 变量 `c3`、`c5`、`x3` 取值于有限整数范围。
2. 迁移 `q_0 -> q_1` 带事件 `tau3` 和 guard `c3 > 0`。
3. 迁移 `q_1 -> q_2` 带 action `x3 = c3`。
4. 事件只有在相关状态机都允许时才能通过 shared-event handshaking 同步触发。

通俗地说，`Supremica` 是“把多台小状态机和少量数据变量拼成一台大离散事件控制器，再自动检查哪里会堵死、哪里违反约束，并且尽量帮你合成一个不那么保守的 supervisor”。

### 运行 / 接受 / 转移语义

对单个 `EFSM`，迁移使能可写成：

$$
enabled(q \xrightarrow{e[g]/a} q', \nu) \iff g(\nu)=true
$$

上式中的符号逐项解释如下：

1. `\nu` 是变量 valuation。
2. `g(\nu)=true` 表示当前 valuation 满足 guard。
3. 若迁移发生，则 action `a` 产生新的 valuation `\nu'`。

多个状态机的同步组合可保守写成：

$$
M = M_1 \parallel M_2 \parallel \cdots \parallel M_n
$$

其含义是：

1. 若若干状态机共享同一事件 `e`，则只有它们都能执行 `e` 时该事件才会发生。
2. 发生时相关状态机一起迁移。
3. 对 `EFSM` 来说，对应 guards/actions 还要做 conjunction 或一致化处理。

论文列出的核心验证问题包括：

$$
\mathrm{Controllable}(M), \quad \mathrm{Nonblocking}(M)
$$

而安全性质验证则被整理成语言包含：

$$
L(M) \subseteq L(SafeSpec)
$$

其中：

1. `SafeSpec` 是用户设计的允许行为上界状态机。
2. 若包含不成立，工具会给出 counterexample trace，并可在 simulator 中回放。

### 语义边界

这篇论文的边界同样很清楚：

1. 主体是离散事件监督控制，不是 timed 或 hybrid family。
2. `EFSM` 的分析经常仍要翻译或约简到普通 `FSM` 语义上。
3. 论文关注的是 industrial-size control problems，而不是 DSL 标准化。
4. 对一般数据结构、连续动力学和开放异步环境建模支持有限。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `EFSM` 骨架 | `$E = (Q, q_0, \Sigma, V, \rightarrow)$` | `Supremica` 的工程建模对象不是只含事件的纯 `FSM`。 |
| 扩展迁移 | `$q \xrightarrow{e[g]/a} q'$` | event、guard 和 action 是 `EFSM` 的基本语义单元。 |
| 组合系统 | `$M = M_1 \parallel \cdots \parallel M_n$` | 共享事件驱动的 handshaking composition 是工具底座。 |
| 最优综合目标 | `$K^\star = \sup \{ K \subseteq L(P \parallel S) \mid K\ \text{controllable and nonblocking} \}$` | 监督器综合追求 least restrictive controllable/nonblocking behaviour。 |
| 安全验证 | `$L(M) \subseteq L(SafeSpec)$` | 应用特定 safety properties 被转成 language inclusion。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以 `FSM/EFSM` 为核心建模骨架。 |
| 事件 / 触发 | 很强 | controllable/uncontrollable、observable/unobservable event 分类明确。 |
| 守卫 / 数据 | 很强 | `EFSM` 支持 finite-range variables、guards 和 actions。 |
| 层次 | 弱支持 | 重点是 modules/parameters，不是层次状态机理论。 |
| 并发 / 同步 | 很强 | 基于 shared events 的 handshaking composition 是核心。 |
| 时间约束 | 不支持 | 不是 timed formalism。 |
| 连续动态 / 随机性 | 不支持 | 主体是纯离散事件控制。 |
| 可执行 / 可验证性 | 很强 | editor、simulator、counterexamples、verification、synthesis 一体化。 |

### 形式化问题与性质

1. `Supremica` 的代表性，不在某个单一算法，而在它把 supervisory control 的完整工程闭环做成了工具环境。
2. `BDD`、modular、compositional 和 explicit 算法并存，说明它追求的是规模可用性而不是某一类理论优雅性。
3. “把综合结果直接写回 `EFSM` guards 里供 `PLC` 实施”这一步，是它非常有工程含义的基础设施贡献。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 在 editor 中图形化创建 plant 与 specification `FSM/EFSM`。
2. 为 events 指定 controllable/uncontrollable、observable/unobservable 属性。
3. 为 `EFSM` 定义变量、guards 和 actions。
4. 用 parameters 和 modules 复用模式化组件。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `FSM/EFSM` 图形模型。
2. parameterized templates 与 modules。
3. 共享事件同步组合。
4. `BDD` 表达的 symbolic supervisor。
5. 写回 `EFSM` guards 的 synthesis 结果。

### 交换与互操作

这篇论文的互操作重点不在开放标准，而在工具内部多语义协作：

1. 同一模型既能进入 simulator，也能进入 analyser/synthesiser。
2. `EFSM` 可被翻译成普通 `FSM`，也可被新算法直接处理。
3. 综合结果可重新投回工程控制器，例如 `PLC` guards。

## 配套基础设施

- 建模/编辑工具：图形化 editor，支持 `FSM`、`EFSM`、parameters 与 modules。
- 解析/交换/元模型支持：工具内部模型、symbolic `BDD` representation 与 parameter substitution；原文未给中立交换标准。
- 仿真/执行支持：interactive simulator，可显示当前状态和 eligible events，并回放历史。
- 验证/分析支持：controllability、nonblocking、control loops、language inclusion 与 counterexample generation。
- 代码生成/转换支持：可把综合结果以 guard 形式无缝加入 `EFSM`，便于 `PLC` 实施。
- 标准化或社区生态：`Supremica` 官网、academic free release 与工业案例构成主要工程生态。

## 适用场景与需求前提

### 适用场景

适合制造系统、嵌入式控制器、工业机器人、自动驾驶代码验证等可用离散事件监督控制表述的问题。

### 需求前提

1. 系统能够拆成 plant 与 specification。
2. 控制逻辑主要围绕离散事件、可控/不可控事件和 blocking 性质展开。
3. 数据需求可压到有限范围变量和 `EFSM` guards/actions。
4. 目标更接近 supervisor synthesis 或 safety checking，而不是连续动力学分析。

### 不适用或高成本场景

如果模型核心是 dense time、连续动力学或开放式异步软件协议，`Supremica` 这条 supervisory control 路线就不一定合适。

## 与相邻形式主义的关系

相对 [method-of-analysing-extended-finite-state-machine-specifications/desc.md](../method-of-analysing-extended-finite-state-machine-specifications/desc.md)，本文补的是 `EFSM` 在 supervisory control 语境下的成熟工具链；相对 [pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md](../pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md) 与 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)，它站在另一条离散事件控制家族线上；相对 [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)，这里没有 hybrid semantics，而是纯离散 supervisory control。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果目标状态机最终服务于工业离散事件控制，那么“能不能验证 controllability / nonblocking、能不能综合 supervisor”是非常实际的选型维度。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像一条目标执行/分析生态线，而不是中立交换格式。

### 对需求到模型生成的启发

1. 若要自动生成适合 `Supremica` 的模型，需求端应能区分 plant 与 specification。
2. 事件的 controllable/uncontrollable 划分要尽量前置，因为这直接影响 supervisor synthesis。
3. `EFSM` 中的数据变量最好被收束在有限范围，否则工具优势很难发挥。

### 现实限制

`Supremica` 很强，但它解决的是离散事件监督控制，不等于普适的状态机执行平台；若问题是混成、概率或开放接口协议，需要转向其他主干。

## 重要的相关工作

- [method-of-analysing-extended-finite-state-machine-specifications/desc.md](../method-of-analysing-extended-finite-state-machine-specifications/desc.md)：`EFSM` 的更早方法学母线。
- [pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md](../pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md)：另一条面向并发控制与数据流的离散事件工具线。
- [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：时间扩展的并发网分析工具锚点。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`FSM / EFSM / Supervisory Control / Supremica`
- 论文角色：supervisory-control IDE / verifier / synthesiser
