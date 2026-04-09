# TT-BIP：面向时间触发范式的正确性先行 BIP 变换 / TT-BIP: Using Correct-by-Design BIP Approach for Modelling Real-Time System with Time-Triggered Paradigm

## 基本信息

- 标题：TT-BIP: Using Correct-by-Design BIP Approach for Modelling Real-Time System with Time-Triggered Paradigm
- 中文标题：TT-BIP：面向时间触发范式的正确性先行 BIP 变换
- 作者：Hela Guesmi，Belgacem Ben Hedia，Simon Bliudze，Saddek Bensalem，Briag Lenabec
- 发表：*Innovations in Systems and Software Engineering*，Vol. 14，No. 2，pp. 117-142，2018
- DOI：`10.1007/s11334-018-0312-y`
- 链接：https://doi.org/10.1007/s11334-018-0312-y
- 形式主义：`BIP / TT-BIP / BIP2TT-BIP`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：从高层 `BIP` 模型到 time-triggered communication architecture 的模型变换方法
- 工具/实现获取方式：原文明确说明变换规则已实现为 `BIP` toolset 的 Eclipse 插件 `BIP2TT-BIP`。
- 标准/格式获取方式：输入是高层 `BIP` 模型与 task mapping，输出是遵循 `TT-BIP` 三层架构的 `BIP` 模型；原文未给中立交换标准。

## 简报

这篇论文的核心价值，不在于再发明一门全新的组件语言，而在于把高层 `BIP` 组件模型系统性地下钻到满足 time-triggered communication 原则的中间模型。`TT-BIP` 通过 task layer、communication layer 和 conflict-resolution layer，把原来由 `BIP` engine 原子处理的多方同步，改写成显式的 send/receive communication media 和 CRP conflict resolution，并且给出 observational equivalence 证明。

- 形式主义定位：`BIP` 到 TT implementation 之间的 correct-by-construction 中间模型与变换路线。
- 构造方式简述：先根据 task mapping 分析 inter-task / conflicting interactions，再把相关 atomic components 改写成发送 offer、等待 notification 的 TT-compatible components，并引入 `TTCC` 与 `CRP` 层。
- 基础设施与场景简述：依托 `BIP` timed-automata semantics、`TTCC`/`CRP` 组件、send/receive connectors 和 `BIP2TT-BIP` 插件，服务时间触发 RTOS/平台的高层建模到实现桥接。

```text
high-level BIP model + task mapping -> analysis of inter-task/conflicting interactions -> TT-BIP task/TTCC/CRP layers -> time-triggered implementation-oriented model
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `BIP` 组件与交互语义。
2. user-defined task mapping。
3. `TT-BIP` 的三层架构。
4. component transformation、`TTCC` construction 与 `CRP` conflict resolution。
5. `BIP2TT-BIP` 工具与 weak bisimulation 正确性证明。

### 核心抽象

论文直接给出 `BIP` 组件：

$$
B = (L, P, X, C, T, tpc)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `P` 是 ports 集合。
3. `X` 是局部变量集合。
4. `C` 是 clocks 集合。
5. `T` 是带 guards、reset 和 update 的 transitions。
6. `tpc` 是 time progress condition 函数。

论文对 interaction 的定义是：

$$
\alpha = (P_\alpha, G_\alpha, F_\alpha)
$$

上式中的符号逐项解释如下：

1. `P_\alpha` 是参与该交互的 ports 集合。
2. `G_\alpha` 是定义在交互变量上的 guard。
3. `F_\alpha` 是交互执行时的数据传递与更新函数。

目标模型的架构语法则被直接写成：

$$
\mathrm{TT\mbox{-}BIP\mbox{-}Model} ::= \mathrm{Task}^+ . \mathrm{TTCC}^+ . \mathrm{CRP}
$$

上式中的符号逐项解释如下：

1. `Task` 是 task layer 中的组件集合。
2. `TTCC` 是 communication layer 中的 communication components。
3. `CRP` 是 conflict resolution policy 组件。
4. `+` 表示一个或多个该类元素。

论文对 task mapping 给出：

$$
\mathcal{T} = \{T_k\}_{k \in K}
$$

并要求它满足对原组件集 `\mathcal{B}` 的划分。上式中的符号逐项解释如下：

1. `T_k` 是第 `k` 个 task 中的一组 `BIP` 组件。
2. `K` 是 task 索引集合。
3. 各个 `T_k` 两两不交，并覆盖原模型组件集。

正确性证明所依赖的结论则是：

$$
G(B) \sim_\beta G(B^{TT})
$$

上式中的符号逐项解释如下：

1. `G(B)` 是原始 `BIP` 模型的语义 `LTS`。
2. `G(B^{TT})` 是变换后 `TT-BIP` 模型的语义 `LTS`。
3. `\sim_\beta` 表示相对于标签对应关系 `\beta` 的 weak bisimilarity。

### 一个最小例子与通俗解释

论文里的最小直觉例子是：

1. 高层 `BIP` 中多个组件通过一次 multi-party interaction 原子同步。
2. 变成 `TT-BIP` 后，原子同步不再直接发生。
3. 组件先通过 send ports 发 offer，`TTCC` 收集 enabledness、timing constraints 和 data，再由 `CRP` 解决冲突，最后发送 notification。
4. 组件收到 notification 后才真正完成原先那一步交互。

通俗地说，`TT-BIP` 像是把“大家同时一步到位地握手”改写成“先报到、再仲裁、最后通知执行”的 time-triggered 通信流程，但保证从外部看行为等价。

### 运行 / 接受 / 转移语义

论文的 `BIP` 语义中，jump transition 与 delay transition 分别满足：

$$
(l,v_x,v_c) \xrightarrow{p} (l',v'_x,v'_c)
$$

和

$$
(l,v_x,v_c) \xrightarrow{\delta} (l,v_x,v_c+\delta)
$$

上式中的符号逐项解释如下：

1. `l,l'` 是控制位置。
2. `v_x` 是变量赋值。
3. `v_c` 是 clock valuation。
4. `p` 是 port-labeled jump。
5. `\delta` 是时间流逝。

对 `TT-BIP`，关键语义变化是：

1. inter-task communication 被拆成 send/receive interactions。
2. `TTCC` 负责通信媒介。
3. `CRP` 负责冲突解决。
4. 原模型的可观察交互通过 `\beta` 关系映射到目标模型的 send-side observable actions。

### 语义边界

边界也很明确：

1. 论文处理的是 `BIP` 到 `TT-BIP` 的第一步变换，还没走到最终平台代码。
2. 重点是 communication architecture，不是一般-purpose distributed implementation。
3. task mapping 由用户给定，不是自动推导。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 组件定义 | `$B = (L, P, X, C, T, tpc)$` | `BIP` 组件的 timed-automata 骨架。 |
| 交互定义 | `$\alpha = (P_\alpha, G_\alpha, F_\alpha)$` | 交互由 ports、guards 和 data transfer 组成。 |
| 目标架构 | `$\mathrm{TT\mbox{-}BIP\mbox{-}Model} ::= \mathrm{Task}^+ . \mathrm{TTCC}^+ . \mathrm{CRP}$` | 目标模型被固定成三层结构。 |
| task mapping | `$\mathcal{T} = \{T_k\}_{k \in K}$` | 用户先把原组件划分到任务。 |
| 正确性 | `$G(B) \sim_\beta G(B^{TT})$` | 变换保持可观察行为等价。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍以 `BIP` timed components 为骨架。 |
| 事件 / 触发 | 很强 | 端口交互、send/receive、offer/notify 都是一等对象。 |
| 守卫 / 数据 | 很强 | ports 自带变量，interaction 带 guard 和 data transfer。 |
| 层次 | 弱支持 | 主体不是层次状态机。 |
| 并发 / 同步 | 很强 | 变换的核心就是重写并发同步方式。 |
| 时间约束 | 很强 | 针对 time-triggered real-time systems。 |
| 连续动态 / 随机性 | 不支持 | 不在主体范围。 |
| 可执行 / 可验证性 | 很强 | 有 Eclipse plugin 实现，且给出 weak bisimulation 证明。 |

### 形式化问题与性质

1. 论文最重要的是把 `BIP` 原子交互重写成符合 TT communication 的显式媒介层。
2. `TT-BIP` 不是简单代码生成，而是保持语义的模型变换。
3. 正确性证明让它不只是工程技巧，而是正式方法路线。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 高层 `BIP` 模型。
2. 用户给定的 task mapping。
3. `BIP2TT-BIP` 变换规则。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `BIP` components 与 connectors。
2. `TTCC` / `CRP` 组件。
3. send/receive interactions。
4. Eclipse 插件化的 transformation flow。

### 交换与互操作

这条路线的互操作重点在于：

1. 在保留 `BIP` 语义基础上引入 TT-compatible communication media。
2. 把高层多方交互转成 task/communication/conflict-resolution 三层结构。
3. 为后续 TT platform programming language 生成提供中间模型。

## 配套基础设施

- 建模/编辑工具：`BIP` toolset 与其 Eclipse 插件环境。
- 解析/交换/元模型支持：输入为 `BIP` 模型，输出仍为结构化 `BIP` 模型，只是遵循 `TT-BIP` 架构。
- 仿真/执行支持：原文用 `BIP` simulator 生成 `C++` 代码比较原模型与变换后模型行为。
- 验证/分析支持：分析 inter-task/conflicting interactions、保证目标模型有效性、证明 weak bisimulation。
- 代码生成/转换支持：本文完成从高层 `BIP` 到 `TT-BIP` 的第一步变换，后续工作再做 TT implementation generation。
- 标准化或社区生态：依附 `BIP` toolset，不是中立标准。

## 适用场景与需求前提

### 适用场景

适合 safety-critical real-time systems、time-triggered RTOS 场景、需要 temporal firewall/communication media 的组件式嵌入式系统设计。

### 需求前提

1. 系统已能建成 `BIP` 组件模型。
2. 用户可以给出合理的 task mapping。
3. 目标平台遵循 time-triggered communication principle。
4. 需要 correct-by-design 的中间模型，而不是直接手写 TT code。

### 不适用或高成本场景

如果系统不是 `BIP` 风格组件化建模，或不关心 time-triggered implementation，`TT-BIP` 的额外结构会显得偏重。

## 与相邻形式主义的关系

相对 [designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md](../designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md)，这里不是 `BIP` 图形前端，而是 implementation-oriented transformation；相对 [coordination-of-dynamic-software-components-with-javabip/desc.md](../coordination-of-dynamic-software-components-with-javabip/desc.md)，`JavaBIP` 关注运行时协调，而 `TT-BIP` 关注 time-triggered architecture rewrite；相对 [modeling-heterogeneous-real-time-components-in-bip/desc.md](../modeling-heterogeneous-real-time-components-in-bip/desc.md)，2006 `BIP` 给出组件语义母线，`TT-BIP` 则是其一个面向 TT 实现的正确性先行变换分支。

## 与本研究的关系

### 对 Project 1 的价值

它很适合说明“生成状态机”之后还可以再做 architecture-aware refinement：先有高层组件交互状态机，再根据部署范式下钻成更接近实现的中间模型。

### 作为目标形式主义还是中间表示

更像 implementation-oriented 中间表示，而不是终态交付语言。

### 对需求到模型生成的启发

1. 若需求里已经包含 task partition 与 time-triggered communication 假设，就不应只输出普通交互状态机。
2. 状态机生成之后的“结构化变换”本身也可以是正式方法研究点。
3. 对 LLM 而言，task mapping 和 communication conflict 的显式化，可能比直接生成平台代码更稳。

### 现实限制

task mapping 仍由人提供，而且本文只完成第一步变换，离最终平台语言还有距离。

## 重要的相关工作

1. [modeling-heterogeneous-real-time-components-in-bip/desc.md](../modeling-heterogeneous-real-time-components-in-bip/desc.md)：`BIP` 语义母线。
2. [designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md](../designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md)：`BIP` 图形化建模与代码生成工作台。
3. [d-finder-a-tool-for-compositional-deadlock-detection-and-verification/desc.md](../d-finder-a-tool-for-compositional-deadlock-detection-and-verification/desc.md)：`BIP` 组合验证工具。

## 文献分类总结

- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`BIP / TT-BIP / BIP2TT-BIP`
- 归类理由：论文主体是把 `BIP` 组合模型变换到 time-triggered 架构的正式方法路线，主线仍然挂在 `BIP` 组合行为家族上。
