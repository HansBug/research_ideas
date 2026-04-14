# 良构通信递归状态机的验证 / Verification of Well-Formed Communicating Recursive State Machines

## 基本信息

- 标题：Verification of well-formed communicating recursive state machines
- 中文标题：良构通信递归状态机的验证
- 作者：Laura Bozzelli, Salvatore La Torre, Adriano Peron
- 发表：*Theoretical Computer Science*, 403(2-3):382-405, 2008
- DOI：`10.1016/j.tcs.2008.06.012`
- 链接：http://dx.doi.org/10.1016/j.tcs.2008.06.012
- 形式主义：`Well-Formed Communicating Recursive State Machines (CRSM)`，即带 fork-join 并发和同 fork 通信的 `RSM` 扩展
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / recursion + fork-join communication
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `CRSM` 元组、tree-shaped global states、`rank(S)`、`ConCaRet` 与 Buchi-CRSM emptiness reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 modules、parallel calls、synchronization alphabet、tree-shaped runs 与 `ConCaRet` local semantics。

## 简报

这篇 journal 版把 `CRSM` 从一个“并发递归的可判定特例”真正稳定成了独立 family。和 2006 会议版相比，它补上了更完整的模型定位：一方面把 `CRSM` 与 `PRS/GTR/DPN/parallel FGS` 的关系系统展开，另一方面把 `ConCaRet`、Buchi-`CRSM` 与 emptiness 构造讲完整，因而更适合在演化树里把 `RSM -> CRSM` 这条 fork-join 并发递归支线固定下来。

- 形式主义定位：`RSM` 的受限并发扩展，也是 recursive concurrent programs 上“保 decidability 的 fork-join family”。
- 构造方式简述：某个 box 不再只调用一个模块，而是一次调用有限个模块实例并行运行，调用者在 join 前挂起。
- 基础设施与场景简述：纯理论条目，但明确把 `CRSM` 接到了 `ConCaRet`、Buchi tree automata 与 `Exptime`-complete model checking。

```text
recursive module -> parallel call box -> tree-shaped local context -> same-fork synchronization -> ConCaRet / Buchi-CRSM checking
```

## 形式主义定义与核心对象

### 定义对象

原文把 `CRSM` 直接定义成“well-formed recursive concurrent programs”的抽象模型。它的核心不是一般并发，而是：

1. 并发只能通过 parallel call/fork 产生。
2. 调用者在 fork 期间暂停。
3. 通信只允许发生在同一 fork 产生的模块实例之间。

这组限制正是它能保持非图灵完备和可判定性的原因。

### 核心抽象

原文把一个 `CRSM` 写成：

$$
S=\langle (S_1,\ldots,S_k), start\rangle
$$

其中每个 module 为：

$$
S_i=\langle \Sigma_i,\Sigma_i^s,N_i,B_i,Y_i,En_i,Ex_i,\delta_i,\eta_i\rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma_i` 是模块字母表，`\Sigma_i^s` 是同步字母集合。
2. `N_i` 是节点集合，`B_i` 是 boxes 集合。
3. `Y_i:B_i\to \{1,\ldots,k\}^+` 把一个 box 映射成要并行激活的一串模块索引。
4. `En_i` 与 `Ex_i` 分别是 entry / exit 节点集合。
5. `\delta_i` 是带标签转移函数。
6. `\eta_i` 是顶点标记函数。

文中还定义了：

$$
rank(S)=\max\{|Y(b)|\mid b\in B\}
$$

它表示一次 fork 最多并行激活多少个模块实例；当 `rank(S)=1` 时，模型就退化成普通 `RSM`。

### 一个最小例子与通俗解释

论文里的典型直觉是：

1. `S_1` 中某个 box 一次激活两个 `S_2` 的副本。
2. 两个副本并行运行，期间可以通过同步字母一起走某些边。
3. 只有当这两个副本都走到各自 exit 时，控制才 join 回 `S_1`。

通俗地说，`CRSM` 就是“会 fork-join 的 `RSM`”。但它不是一般线程系统，因为同一 local context 的边界被严格圈住了。

### 运行 / 接受 / 转移语义

原文把 `CRSM` 的全局状态定义成树形结构：

$$
K_S=\langle Q,R\rangle
$$

其中每个全局状态是一个用 vertices / boxes 标记的有限树。树的叶子对应当前活跃的模块实例，叶子路径对应局部调用栈。

与普通 `RSM` 的栈序列不同，这里局部上下文是树而不是线：

$$
q=(t,D)
$$

上式中的符号逐项解释如下：

1. `t` 是描述当前激活层次与并行展开的树。
2. `D` 为树节点分配当前激活顶点或 box。

这正是 `CRSM` 比 `RSM` 更强的根本来源：它的“全局控制形状”从 stack 变成了 tree of stacks。

### 语义边界

这个 family 的边界非常明确：

1. 它允许并发，但只允许 fork-join 并发。
2. 它允许通信，但只限于同一 fork 里的模块实例。
3. 它不允许 unrestricted spawn，因此 local context 的宽度有界。
4. 它不处理 dense time 或连续变量。

### 关键性质与判定边界

论文给出的核心逻辑结果是：

$$
\mathrm{MC}(CRSM,ConCaRet)\text{ is Exptime-complete}
$$

而复杂度对并发宽度 `\rho=rank(S)` 和公式规模都是指数的。

同时，文中还指出：

$$
rank(S)=1 \Rightarrow CRSM = RSM
$$

以及 synchronization-free `CRSM` 对应 ground tree rewriting 的完整正常形态。这说明 `CRSM` 不是偶然小变体，而是位于 `RSM` 与 `GTR/recursive concurrency` 之间的稳定层。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | modules、nodes、boxes、tree-shaped contexts。 |
| 事件 / 触发 | 强支持 | 普通动作与同步字母都内建在转移里。 |
| 守卫 / 数据 | 弱支持 | 论文核心不在变量，而在并发递归骨架。 |
| 层次 | 强支持 | recursive modules + forked local contexts。 |
| 并发 / 同步 | 强支持 | fork-join 并发与 same-fork synchronization 是核心。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | `ConCaRet`、Buchi-CRSM、emptiness reduction。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$S=\langle(S_1,\ldots,S_k),start\rangle$` | `CRSM` 顶层定义。 |
| module 元组 | `$S_i=\langle \Sigma_i,\Sigma_i^s,N_i,B_i,Y_i,En_i,Ex_i,\delta_i,\eta_i\rangle$` | 并发递归模块骨架。 |
| 并发宽度 | `$rank(S)=\max\{|Y(b)|\mid b\in B\}$` | 一次 fork 的最大并行度。 |
| 全局状态系统 | `$K_S=\langle Q,R\rangle$` | tree-shaped global semantics。 |
| 复杂度 | `$\mathrm{MC}(CRSM,ConCaRet)$ is Exptime-complete` | 逻辑判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先定义各个 modules 的 nodes、boxes、entries 和 exits。
2. 用 `Y_i` 规定某个 box 一次调用哪些模块实例。
3. 把需要同步的动作放进 `\Sigma_i^s`。
4. 最后用树形 global-state semantics 解释 fork / join / local context。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `CRSM` module tuples；
2. tree-shaped global states；
3. `rank(S)`；
4. `ConCaRet` local-successor semantics；
5. Buchi-`CRSM`。

### 交换与互操作

它与当前文库中几条线直接相关：

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 与 [verification-of-well-formed-communicating-recursive-state-machines/desc.md](../verification-of-well-formed-communicating-recursive-state-machines/desc.md) 组成 `CRSM (2006 / 2008)` 的 conference / journal 双条目。
3. 与 `PRS/GTR/DPN` 社区互相参照，但保持更强的状态机可视化骨架。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 module tuple、tree-shaped global states 和 `ConCaRet`。
- 仿真/执行支持：可按全局树状态与同步标签语义执行。
- 验证/分析支持：`ConCaRet` model checking、Buchi-CRSM emptiness、GTR/automata-theoretic reduction。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要作为 recursive concurrency 的状态机化抽象。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程系统里存在受控 fork-join 并发。
2. 模块间同步只发生在同一 local context 中。
3. 需要比一般 PRS/DPN 更直观的状态机结构。

### 需求前提

1. 并发创建模式必须是 fork-join，而不是任意 spawn。
2. 通信边界需要能由 local context 严格圈定。
3. 系统仍应以递归控制流为骨架。

### 不适用或高成本场景

如果系统是完全自由的线程生成与同步，`CRSM` 约束太强；如果系统根本没有并发，只需 `RSM/ERSM`；如果关注的是双人对抗赢法，应转向 `RGG`。

## 与相邻形式主义的关系

相对 `RSM`，它增加了 fork-join 并发与 same-fork communication；相对 `PRS/GTR`，它更强调状态机式模块结构；相对 `CHSM`，它的难点不在有限并发 hierarchy，而在递归 + 并发的结合。

## 与本研究的关系

### 对 Project 1 的价值

它证明层次状态机支线里，`RSM` 之后并不只有 game/open 方向，还有一条“受限并发递归”支线。这对后续处理多任务协同、并行子过程需求非常关键。

### 对状态机自动建模的启发

如果需求里同时出现“递归子过程”和“并行调用后汇合”，那么 plain `RSM` 会丢信息，而 `CRSM` 正好给出一个仍可判定的状态机 family。

## 重要的相关工作

1. [verification-of-well-formed-communicating-recursive-state-machines/desc.md](../verification-of-well-formed-communicating-recursive-state-machines/desc.md)：`CRSM` 的会议版条目。
2. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：`CRSM` 所依附的 `RSM` 母线。
3. `ConCaRet`：这篇论文里与 `CRSM` 一起稳定提出的局部时序逻辑。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🧩 经典离散状态机`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🎛️ 控制 / 反应式逻辑`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> CRSM` 位置，并把该节点的年份口径稳定成 `2006 / 2008`。
