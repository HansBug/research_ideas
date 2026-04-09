# Petri 博弈：具有因果记忆的分布式系统综合 / Petri Games: Synthesis of Distributed Systems with Causal Memory

## 基本信息

- 标题：Petri Games: Synthesis of Distributed Systems with Causal Memory
- 中文标题：Petri 博弈：具有因果记忆的分布式系统综合
- 作者：Bernd Finkbeiner，Ernst-Rüdiger Olderog
- 发表：*Electronic Proceedings in Theoretical Computer Science*，161:217-230，2014
- DOI：`10.4204/EPTCS.161.19`
- 链接：https://doi.org/10.4204/EPTCS.161.19
- 形式主义：`Petri games / causal-memory distributed synthesis`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：`Petri games` 母论文 / distributed-synthesis formalism with causal memory
- 工具/实现获取方式：原文主体是形式主义与可判定性结果，没有给独立公开工具；后续实现与工具化路线由文库中的 [symbolic-vs-bounded-synthesis-for-petri-games/desc.md](../symbolic-vs-bounded-synthesis-for-petri-games/desc.md) 和 `ADAM` 系列条目继续补齐。
- 标准/格式获取方式：主承载对象是 safe `P/T Petri net`、place partition、unfolding、strategy subprocess 与 bad places；不是行业交换标准。

## 简报

这篇论文补的是 `Petri` 线里一条非常关键的“分布式控制器综合”母线。普通 `Petri Net` 负责描述并发与因果，但不直接说“哪些 token 在做决策、它们知道什么、何时同步后才能共享信息”。`Petri games` 的做法是把 token 直接解释成玩家，把同步 transition 解释成信息交换点，并把 system/environment place 划分固定进模型。

- 形式主义定位：它不是新的高层网语法，而是把 safe `P/T Petri net` 重新解释为带局部知识和因果记忆的分布式博弈。
- 构造方式简述：`partitioned Petri net -> unfolding -> strategy as subprocess -> finite graph game reduction -> winning strategy / local controllers`。
- 基础设施与场景简述：依托 unfolding、finite graph game reduction、local-controller distribution，适合分布式报警、工作流协同、工业单元协作这类“并发决策 + 局部信息”问题。

```text
partitioned Petri net -> unfolding with causal histories -> strategy pruning -> finite graph game -> distributed winning strategy
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 以 place 分区区分 `system` 与 `environment` 的 safe `P/T Petri net`。
2. 将 token 解释为玩家，将同步 transition 解释为信息交换事件。
3. 通过 unfolding 显式恢复每个玩家可见的 causal history。
4. 通过 strategy subprocess 限制 system 侧可选分支，而不替 environment 做决定。

### 核心抽象

论文直接把 `Petri game` 写成：

$$
G = (P_S, P_E, T, F, In, B)
$$

上式中的符号逐项解释如下：

1. `$P_S$` 是 system places。
2. `$P_E$` 是 environment places。
3. `$T$` 是 transition 集合。
4. `$F \subseteq (P \times T) \cup (T \times P)$` 是 flow relation，其中 `$P = P_S \cup P_E$`。
5. `$In$` 是初始 marking。
6. `$B$` 是 bad places，从 system 视角看，任何 play 一旦到达 `$B$` 就算输。

strategy 不是一个中心控制器，而是 unfolding 上的一个 subprocess。论文给出两条核心约束：

$$
\text{(S1) } p \in P^\sigma_S \Rightarrow \sigma \text{ 在 } p \text{ 上是确定的}
$$

$$
\text{(S2) } p \in P^\sigma_E \Rightarrow \forall t \in T_U,\ (p,t)\in F_U \land |pre_U(t)|=1 \Rightarrow (p,t)\in F_\sigma
$$

上式中的符号逐项解释如下：

1. `$P^\sigma_S$` 与 `$P^\sigma_E$` 分别是 strategy 中的 system places 与 environment places。
2. `(S1)` 表示 system 不能在同一局部历史上保留多个互斥选择。
3. `(S2)` 表示 environment 的局部可选动作不能被 strategy 私自删掉。
4. `$T_U,F_U$` 是 unfolding 上的 transition 与 flow relation；`$F_\sigma$` 是 strategy subprocess 的 flow relation。

论文还把“system 不能靠拒绝动作来伪造安全”压成 deadlock-avoidance 条件：

$$
\forall M \in R(N_\sigma):\ \Big(\exists t \in T_U:\ pre(t)\subseteq M\Big) \Rightarrow \Big(\exists t \in T_\sigma:\ pre(t)\subseteq M\Big)
$$

上式中的符号逐项解释如下：

1. `$R(N_\sigma)$` 是 strategy net `$N_\sigma$` 的可达 marking 集。
2. `$T_U$` 是 unfolding 的 transition 集，`$T_\sigma$` 是 strategy 保留的 transition 集。
3. 如果 unfolding 在某个 marking 上还能走，strategy 也必须允许至少一个后继。
4. 这条约束排除了“system 直接把自己卡死”这种平凡安全解。

### 一个最小例子与通俗解释

论文开头用分布式安全报警系统举例：

1. environment token 先决定入侵点是 `A` 还是 `B`。
2. 两个 system token 分别控制两处本地报警逻辑。
3. 若 system token 不同步，它们只知道自己当前所在的局部 place，不知道 environment 先前选择了哪里。
4. 一旦通过联合 transition 同步，双方就交换 causal history，然后才知道应该共同发出哪一种报警。

通俗地说，`Petri games` 把“通信前不知道，通信后知道”这件事直接嵌进了网的因果结构里。它和普通博弈图最大的不同，是玩家的知识不是全局状态，而是 token 自己因果历史里真正能看到的那一部分。

### 运行 / 接受 / 转移语义

论文的关键语义链是：

$$
G \xrightarrow{\text{unfold}} \beta_U \supseteq \sigma
$$

上式中的符号逐项解释如下：

1. `$G$` 是原始 `Petri game`。
2. `$\beta_U$` 是 underlying net 的 unfolding。
3. `$\sigma$` 是 unfolding 上的 strategy subprocess。
4. unfolding 把“同步前后知道多少信息”显式编码成不同的 causal copies。

winning condition 仍然是 safety-oriented：

$$
\pi \cap B = \varnothing
$$

上式中的符号逐项解释如下：

1. `$\pi$` 是一条 conforming play。
2. `$B$` 是 bad places 集。
3. 若 play 经过任何 bad place，则 environment 赢。
4. system 的目标是构造对所有 conforming plays 都安全的 strategy。

### 语义边界

1. 论文主线是 safe `Petri games` 的 safety synthesis，不是一般 `Petri` 分析总论。
2. 原文的可判定性主结果针对“单 environment player + 有界 system players”。
3. 模型重点在因果记忆与分布式信息流，不处理富数据守卫、概率或连续时间。
4. 局部控制器的可分发性依赖 concurrency-preserving 等结构前提。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `Petri game` 元组 | `$G = (P_S, P_E, T, F, In, B)$` | 把 place 划成 system / environment，并显式标记 bad places。 |
| strategy 约束 | `(S1)` 与 `(S2)` | system 决策必须确定，environment 的局部选择不能被偷删。 |
| deadlock avoidance | `$\forall M \in R(N_\sigma)\ldots$` | 禁止 system 靠人为制造死锁来“赢”。 |
| 判定复杂度 | `EXPTIME`-complete | 单 environment player、bounded system players 的安全综合可判定且单指数时间可解。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | marking 与 unfolding copies 一起定义全局与局部状态。 |
| 事件 / 触发 | 很强 | transition firing 就是玩家决策和同步事件。 |
| 守卫 / 数据 | 弱支持 | 主体不在富数据，而在因果历史与可见信息。 |
| 层次 | 不支持 | 不是层次状态机或 profile。 |
| 并发 / 同步 | 很强 | 多 token 并发、同步通信和因果依赖是模型本体。 |
| 时间约束 | 不支持 | 本文不是 timed Petri games。 |
| 连续动态 / 随机性 | 不支持 | 纯离散分布式博弈。 |
| 可执行 / 可验证性 | 很强 | 可约化为 finite graph game，并进一步分发成 local controllers。 |

### 形式化问题与性质

1. `Petri games` 解决的是“局部知识下的分布式综合”，不是中心化 controller synthesis。
2. token 的同步既是控制动作，也是信息交换动作。
3. unfolding 在这里不是单纯证明工具，而是“玩家知道什么”的语义载体。
4. 对本论文集而言，这篇就是 `Petri games` 支线的主挂点。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 一个 safe `P/T Petri net`。
2. 对 places 的 `system / environment` 分区。
3. 一组 bad places。
4. 需要由局部控制器协同避免 bad places 的 safety 目标。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `P/T` 网的 places、transitions、flow relation 与 initial marking。
2. unfolding / branching process。
3. strategy subprocess。
4. finite graph game 与 local-controller decomposition。

### 交换与互操作

本文本身不定义交换标准；它更像一条“模型本体 -> unfolding -> graph game / local controllers”的理论承载链。后续真正的工具互操作主要由 `ADAM` 系列与 bounded-synthesis 条目补齐。

## 配套基础设施

- 建模/编辑工具：原文未给独立编辑器；主要假定已有 `Petri net` 建模能力。
- 解析/交换/元模型支持：核心是 unfolding、subprocess、finite graph game reduction，而非 XML/JSON 标准。
- 仿真/执行支持：原文重点是综合 winning strategy，不是运行时仿真平台。
- 验证/分析支持：finite graph game solving、deadlock-avoidance analysis、distribution to local controllers。
- 代码生成/转换支持：可从 global strategy 分发到 local controllers，但不是 PLC/代码部署链。
- 标准化或社区生态：后续由 `ADAM`、bounded synthesis、`Petri net with transits` 等分支扩充出更完整生态。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 多局部控制器需要同步交换信息后再做一致决策的分布式控制问题。
2. workflow / alarm / manufacturing 这类天然适合 token-flow 建模的系统。
3. 目标主要是 safety-style distributed synthesis，而不是单纯 reachability verification。

### 需求前提

1. 系统必须能稳定落成 safe `Petri net`。
2. system 与 environment 的 place 边界需要明确。
3. 关键性质最好能表达成“避免 bad place”这类 safety objective。
4. 通信点必须能离散化成同步 transition。

### 不适用或高成本场景

若需求核心在 rich data、数值优化、概率博弈或连续时间，而不是局部信息与同步通信，那么 `Petri games` 不是最自然的一层。

## 与相邻形式主义的关系

相对 [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)，这里不再只是并发过程建模，而是把 token 解释成有局部知识的玩家；相对 [symbolic-vs-bounded-synthesis-for-petri-games/desc.md](../symbolic-vs-bounded-synthesis-for-petri-games/desc.md)，那篇是后续求解路线与工具比较，本文是母模型与判定性起点；相对 [model-checking-data-flows-in-concurrent-network-updates/desc.md](../model-checking-data-flows-in-concurrent-network-updates/desc.md)，两者都沿着 `Petri` 的因果结构做扩展，但本文强调 distributed synthesis 与 causal memory，后者强调 token-flow verification 与 `Flow-LTL`。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 `Petri` 线不是只能做并发建模，还能自然承载“部分可观测 + 协同决策”的状态机扩展需求。
2. 对需求到模型生成而言，如果需求中存在“只有同步后才知道”的知识约束，`Petri games` 比普通 `FSM` 更贴切。
3. 它也为后续把控制逻辑生成目标扩展到 distributed-synthesis family 提供了明确挂点。

### 作为目标形式主义还是中间表示

更适合作为特定类型分布式控制问题的目标形式主义，也可作为从非形式化协作需求过渡到综合后端的中间表示。

### 对需求到模型生成的启发

1. 需求若含多个局部主体，应尽早区分哪些信息是本地可见、哪些只能通过同步获得。
2. 应在需求阶段显式标出 bad situations，而不是只给松散的全局目标。
3. 若未来做自动修复，bad-place 结构和同步边界会是很好的修复定位入口。

### 现实限制

它的工程生态不如 `UPPAAL`、`SCXML` 或 supervisory-control 工具链成熟；而且一旦系统需要丰富数据或时间语义，通常还要叠加其他形式主义。

## 重要的相关工作

### 奠基或前身工作

- Zielonka automata 与因果记忆分布式系统母线。
- 经典 safe `P/T Petri net` 与 unfolding 理论。

### 同类型或同家族工作

- [symbolic-vs-bounded-synthesis-for-petri-games/desc.md](../symbolic-vs-bounded-synthesis-for-petri-games/desc.md)：后续求解算法与工具比较。
- [adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md](../adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md)：同一作者群沿 `Petri` 因果结构发展出的 flow-sensitive verification 工具线。

### 标准 / 格式 / 工具链工作

- 原文未给标准交换格式；工具化主要由后续 `ADAM` 系列工作承担。

### 与本研究关系最紧的工作

- [symbolic-vs-bounded-synthesis-for-petri-games/desc.md](../symbolic-vs-bounded-synthesis-for-petri-games/desc.md)
- [model-checking-data-flows-in-concurrent-network-updates/desc.md](../model-checking-data-flows-in-concurrent-network-updates/desc.md)

## 文献分类总结

- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`Petri games / causal-memory distributed synthesis`
- 论文角色：`Petri games` 母论文 / distributed-synthesis formalism with causal memory
- 核心功能：把 `Petri net` 因果结构升级为局部知识下的分布式博弈，并给出 safety synthesis 可判定性。
- 关键特性：token-as-player、同步即通信、causal memory、unfolding-based strategy、deadlock avoidance、local-controller distribution。
- 构造方式：`partitioned Petri net + unfolding + strategy subprocess + finite graph game`。
- 基础设施：unfolding、finite graph game、local-controller decomposition；原文无独立公开工具。
- 适用场景：分布式报警、协同控制、工作流/制造等多主体并发决策系统。
