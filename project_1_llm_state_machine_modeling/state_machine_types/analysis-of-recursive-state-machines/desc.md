# 递归状态机的分析 / Analysis of Recursive State Machines

## 基本信息

- 标题：Analysis of Recursive State Machines
- 中文标题：递归状态机的分析
- 作者：Rajeev Alur, Kousha Etessami, Mihalis Yannakakis
- 发表：*Computer Aided Verification*, pp. 207-220, 2001
- DOI：`10.1007/3-540-44585-4_18`
- 链接：https://doi.org/10.1007/3-540-44585-4_18
- 形式主义：`Recursive State Machines (RSM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 component tuple、global state `\langle b_1,\ldots,b_r,u\rangle`、call / return 语义与 reachability / cycle-detection rules。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 component machine、boxes、entry / exit nodes 与 call-return expansion semantics。

## 简报

这篇论文把层次状态机再往前推了一步：如果说 `HSM` 允许“状态展开成子状态机”，那么 `RSM` 允许“这个子状态机还能递归调用自己或别的组件”。作者把它明确定位成“statecharts-like hierarchical state machines 的递归变体”，并说明它可以直接表达顺序命令式程序里的递归过程控制流。对当前演化树来说，`RSM` 是层次状态机支线与 pushdown / call-return 语义真正接上的关键节点。

- 形式主义定位：`HSM` 的递归扩展，也是程序控制流 / pushdown family 与 hierarchical state-machine family 的桥接点。
- 构造方式简述：系统由若干 component machine 组成；组件里既有普通节点，也有映射到其他组件的 boxes；进入 box 等于 call，沿 box-port 返回等于 return。
- 基础设施与场景简述：原文纯理论，但同时给出 global transition semantics、reachability、cycle detection 与和 pushdown / boolean-program line 的关系。

```text
层次控制流 -> components + boxes + entry/exit -> call / return stack semantics -> recursive reachability / cycle detection
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 sequential imperative program 的递归控制流，但故意用“state machine + box + ports”的视觉化骨架来表达，而不是直接写成 pushdown system。

### 核心抽象

原文把一个 `RSM` 写成：

$$
A = \langle A_1,\ldots,A_k \rangle
$$

其中每个 component machine 可以整理为：

$$
A_i = (N_i \cup B_i,\ Y_i,\ En_i,\ Ex_i,\ \delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i : B_i \to \{1,\ldots,k\}` 指定每个 box 调用哪个组件。
4. `En_i \subseteq N_i` 是 entry nodes。
5. `Ex_i \subseteq N_i` 是 exit nodes。
6. `\delta_i` 是带标签迁移关系，边既可以连普通节点，也可以连到某个 box 的 port。

### 一个最小例子与通俗解释

一个最小直觉例子是“递归下降处理括号表达式”：

1. 顶层组件 `A_1` 里遇到 `(` 时进入一个 box，调用 `A_1` 自己。
2. 当递归子调用处理完毕并到达 exit node 时，再沿 box 的 return edge 回到外层继续。
3. 整个运行过程中，当前全局状态不再是一个普通节点，而是“调用栈上的若干 boxes + 当前节点”。

通俗地说，`RSM` 就是“会调用子状态机、并把调用现场压栈保存起来的层次状态机”。它比 `HSM` 多的，不是并发，不是变量，而是无界 call stack。

### 运行 / 接受 / 转移语义

原文把 global state 定义成：

$$
\langle b_1,\ldots,b_r,u \rangle \in B^*N
$$

上式中的符号逐项解释如下：

1. `b_1,\ldots,b_r` 是当前调用栈上的 boxes。
2. `u` 是当前最内层组件里的普通节点。
3. 因为有递归，这个 global state space 一般是无限的。

global transition relation `\delta` 分四类：

1. 当前组件内部普通迁移；
2. 进入 box 并把 `(box, entry)` 压到栈上；
3. 到达 exit node 后返回上一层；
4. 返回后又立即进入上一层的另一个 box。

可把一类关键 call / return 语义压成：

$$
\langle b_1,\ldots,b_r,u \rangle \xrightarrow{\sigma}
\langle b_1,\ldots,b_r,b',e \rangle
$$

表示从当前节点 `u` 调用 box `b'` 并进入被调组件的 entry `e`；

以及

$$
\langle b_1,\ldots,b_r,u \rangle \xrightarrow{\sigma}
\langle b_1,\ldots,b_{r-1},u' \rangle
$$

表示当前节点 `u` 已经是被调组件的 exit node，因此沿返回边退栈并回到上一层节点 `u'`。

### 语义边界

`RSM` 的边界非常明确：

1. 仍是 sequential，没有并发。
2. 仍是离散，没有时间和连续变量。
3. hierarchy 被提升为 recursion，因此 global state space 一般无限。
4. 与 pushdown systems 等价相关，但作者强调 `RSM` 更适合作为 visual / state-based recursive-control model。

### 关键性质与判定边界

原文聚焦两个核心问题：reachability 与 cycle detection。代表性结论是：

$$
\mathrm{Reachability}(\mathrm{RSM}),\ \mathrm{CycleDetection}(\mathrm{RSM})
$$

都可在

$$
O(n\theta^2)
$$

时间和

$$
O(n\theta)
$$

空间内求解，其中 `n` 是 `RSM` 大小，`\theta` 是各组件 `\min(\#entries,\#exits)` 的最大值。

这个结论非常关键，因为它说明：虽然 `RSM` 的全局语义像 pushdown system 一样有无限状态，但由于组件接口结构明确，分析成本可以明显优于一般 cubic-style pushdown analysis。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components + boxes + nodes。 |
| 事件 / 触发 | 强支持 | 由带标签边触发。 |
| 守卫 / 数据 | 不支持 | 原文核心不在变量。 |
| 层次 | 强支持 | box 调用形成层次结构。 |
| 并发 / 同步 | 不支持 | 明确是 sequential。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability / cycle detection / Büchi line完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| RSM 总元组 | `$A=\langle A_1,\ldots,A_k\rangle$` | 组件化递归机器。 |
| 组件元组 | `$A_i=(N_i\cup B_i,Y_i,En_i,Ex_i,\delta_i)$` | box / call / return 的局部骨架。 |
| global state | `$\langle b_1,\ldots,b_r,u\rangle \in B^*N$` | 调用栈 + 当前节点。 |
| call 语义 | `$\langle \cdots,u\rangle \to \langle \cdots,b',e\rangle$` | 进入被调组件。 |
| return 语义 | `$\langle \cdots,u\rangle \to \langle \cdots,u'\rangle$` | 退出组件并退栈返回。 |

## 构造方式与承载格式

### 建模入口

1. 先按过程 / 子任务划分 components。
2. 给每个 component 定义 entries 和 exits。
3. 再用 boxes 表达对其他 components 的调用。
4. 最后用 ordinary edges 接好内部 flow 与 return flow。

### 机器可处理承载方式

机器可处理承载方式就是：

1. component tuple；
2. ports；
3. box-to-component mapping；
4. stack-based global semantics。

### 交换与互操作

原文没有工程交换格式，但和两个谱系直接互操作：

1. 往上承接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 hierarchy。
2. 往旁边连接 pushdown / boolean-program / recursive-control analysis family。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 component / box / port / stack semantics。
- 仿真/执行支持：可直接按 global transition system 运行。
- 验证/分析支持：reachability、cycle detection、`LTL/Büchi` 入口清楚。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型理论路线，主要与 pushdown / program-analysis 社区互动。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流。
2. 可视化的 call-return 行为建模。
3. 想把层次状态机支线接到 pushdown 语义上。

### 需求前提

1. 并发不是核心难点。
2. 递归调用才是结构复杂度来源。
3. 接口可抽成有限 entries / exits。

### 不适用或高成本场景

如果系统没有 recursion，只是有限层次复用，则 `HSM` 更轻；如果还要 supernode proposition inheritance，则需要 [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)。

## 与相邻形式主义的关系

相对 `HSM`，`RSM` 允许 recursion；相对 `CHSM`，`RSM` 不走并发同步路线；相对一般 pushdown system，`RSM` 更 state-machine / visual；相对后续 context-dependent family，它的 atomic propositions 仍主要贴在普通节点上。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机支线并不止于 `Statecharts/UML` 这类 DSL，也可以自然演化到递归控制流和 pushdown-style formal model。

### 作为目标形式主义还是中间表示

更像高表达力中间表示或理论比较基线，而不是直接工程交付语言。

### 对需求到模型生成的启发

如果需求文本里已明显出现“子流程自调用 / 过程返回 / 嵌套任务栈”，直接生成 flat `FSM` 或普通 `HSM` 都会损失结构；`RSM` 才是更自然的目标 family。

### 现实限制

因为 global state space 无限、工程标准缺失，`RSM` 更适合理论分析和中间建模，不适合作为一线工业可视化建模语言。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)

### 同类型或同家族工作

- [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)
- `Recursive timed automata`、`Recursive hybrid automata`：时间 / 混成主干上的递归后继。

## 文献分类总结

- 这篇论文是层次状态机支线里最经典的 recursion 节点。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、工具或应用案例。
- 在演化树里最适合作为 `HSM` 下面的 `RSM` 子枝，并为后续 context-dependent / timed / hybrid recursive family 提供父边。
