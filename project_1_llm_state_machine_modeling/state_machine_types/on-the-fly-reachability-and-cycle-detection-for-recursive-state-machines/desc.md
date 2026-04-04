# 递归状态机的在线可达性与环检测 / On-the-Fly Reachability and Cycle Detection for Recursive State Machines

## 基本信息

- 标题：On-the-Fly Reachability and Cycle Detection for Recursive State Machines
- 中文标题：递归状态机的在线可达性与环检测
- 作者：Rajeev Alur, Swarat Chaudhuri, Kousha Etessami, P. Madhusudan
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*, pp. 61-76, 2005
- DOI：`10.1007/978-3-540-31980-1_5`
- 链接：http://dx.doi.org/10.1007/978-3-540-31980-1_5
- 形式主义：`Extended Recursive State Machines (ERSM)`，即带全局/局部变量、守卫和赋值的 `RSM`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / typed-variable `RSM`
- 工具/实现获取方式：文中实现为 `Vera`；机器可处理入口是 `ERSM` 元组、guarded commands、summary transitions 与显式状态搜索。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 components、typed variables、internal/call edges、stacked configurations 与 on-the-fly summary semantics。

## 简报

这篇论文表面上讲的是显式状态搜索，但它真正补到树上的，是 `RSM` 向“变量化递归控制流模型”迈出的稳定一步。作者明确把 `ERSM` 定义成 `RSM` 加上全局变量、局部变量、守卫和赋值的程序级抽象，从而让层次状态机支线不再只停留在纯 control-flow 递归，而是能直接承载布尔程序和带有限数据域的过程化软件。

- 形式主义定位：`RSM` 的 typed-state 扩展，也是 `RSM` 接到软件模型检查工具链的经典中间层。
- 构造方式简述：每个 component 除 entry/exit、普通节点和 call edges 外，再携带全局变量集、局部变量集、guarded internal edges 与 assignments。
- 基础设施与场景简述：文中直接给出 `Vera` 实现，以及与 `Bebop/Moped` 的对照；但更重要的是把 `ERSM` 稳定成“可抽象自 C-like 程序”的程序控制模型。

```text
recursive components -> global/local variables + guards/updates -> stacked configurations -> summary edges -> on-the-fly reachability / fair-cycle checking
```

## 形式主义定义与核心对象

### 定义对象

原文先回顾 `RSM`，再指出仅靠 boxes、entry/exit 和 call-return 还不够直接支撑软件验证，因为程序还有全局变量、局部变量和 guarded updates。于是作者把这些东西直接并入 `RSM` 本体，得到 `ERSM`。

### 核心抽象

原文把一个 `ERSM` 写成：

$$
A = \langle G,\gamma_{in},p,(A_1,\ldots,A_k)\rangle
$$

其中每个 component machine 可整理为：

$$
A_i=\langle L_i,I_i,O_i,\lambda^{in}_i,N_i,en_i,ex_i,\delta_i\rangle
$$

上式中的符号逐项解释如下：

1. `G` 是全局变量集合，`\gamma_{in}` 是其初始解释。
2. `p` 是初始 component 的编号。
3. `L_i` 是 component `A_i` 的局部变量集合。
4. `I_i` 和 `O_i` 分别是输入变量和输出变量集合，用来编码多入口/多出口参数化。
5. `\lambda^{in}_i` 是 `L_i` 的初始解释。
6. `N_i` 是节点集合，`en_i` 与 `ex_i` 分别是 entry / exit 节点。
7. `\delta_i` 是边关系，既包含 internal edges，也包含 call edges。

### 一个最小例子与通俗解释

可以把它想成“带局部变量的递归函数图”：

1. component `A_1` 里有局部变量 `x` 和全局变量 `a`。
2. 某条 internal edge 只有在 `x=F` 时可走，并把 `a` 改成 `T`。
3. 另一条 call edge 调用 component `A_2`，调用前把输入变量列表写到被调 component 的局部变量里，返回后再把输出变量拷回调用者。

通俗地说，`ERSM` 就是“会压栈调用、还会在每层作用域里带变量的递归状态机”。它比普通 `RSM` 多的不是新的并发或时间语义，而是把程序里最常见的有限数据更新也正式塞进了模型。

### 运行 / 接受 / 转移语义

原文把一个 configuration 写成：

$$
\psi=\langle \gamma, stack, u, \lambda \rangle
$$

上式中的符号逐项解释如下：

1. `\gamma` 是当前全局变量解释。
2. `stack` 是调用栈，每一帧保存调用边和调用点局部变量解释。
3. `u` 是当前节点。
4. `\lambda` 是当前 component 的局部变量解释。

全局迁移关系包含三类步：

$$
\Delta = \Delta_{int} \cup \Delta_{call} \cup \Delta_{ret}
$$

其中：

1. `\Delta_{int}` 表示沿 internal edge 前进，同时按 guard/assignment 更新变量。
2. `\Delta_{call}` 表示压栈并进入被调 component 的 entry。
3. `\Delta_{ret}` 表示从被调 component 的 exit 弹栈返回，并把输出值写回调用者。

### 语义边界

这个 family 的边界很清楚：

1. 它仍是 sequential recursive model，不处理并发。
2. 它是离散有限变量模型，不处理 dense time 或连续动力学。
3. 它的增强点在“typed variables + assignments”，不是在 hierarchy 骨架本身。
4. 若去掉变量和赋值，它就退回普通 `RSM`。

### 关键性质与判定边界

论文最重要的不是某个 DFS 技巧，而是它说明 `ERSM` 依然保留 `RSM` 的 summary-style 可分析结构。对无变量的控制骨架，文中给出：

$$
\mathrm{Reachability} \in O(n)
$$

以及 fair-cycle detection：

$$
\mathrm{CycleDetection} \in O(kn)
$$

上式中的符号逐项解释如下：

1. `n` 是无变量 control graph 的总大小。
2. `k` 是 components 的数量。

也就是说，`ERSM` 在程序抽象视角下仍然维持了可做 summary 和 on-the-fly traversal 的结构，这正是它比“直接拿程序 CFG + stack”更适合作为理论节点的地方。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components、nodes、call stack。 |
| 事件 / 触发 | 强支持 | internal/call edges 都由显式 guard 驱动。 |
| 守卫 / 数据 | 强支持 | typed global/local variables 与 assignments 是核心新增点。 |
| 层次 | 强支持 | 通过 recursive components + call stack 形成 hierarchy。 |
| 并发 / 同步 | 不支持 | 仍是单线程递归控制。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | on-the-fly reachability、fair cycle、monitor product。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=\langle G,\gamma_{in},p,(A_1,\ldots,A_k)\rangle$` | `ERSM` 顶层骨架。 |
| component 元组 | `$A_i=\langle L_i,I_i,O_i,\lambda^{in}_i,N_i,en_i,ex_i,\delta_i\rangle$` | 变量化递归模块。 |
| configuration | `$\psi=\langle \gamma,stack,u,\lambda\rangle$` | 全局变量 + 栈 + 当前节点 + 当前局部环境。 |
| 迁移分解 | `$\Delta=\Delta_{int}\cup\Delta_{call}\cup\Delta_{ret}$` | internal/call/return 三类语义步。 |
| 复杂度 | `Reachability: O(n)`, `CycleDetection: O(kn)` | 无变量控制骨架上的 on-the-fly 上界。 |

## 构造方式与承载格式

### 建模入口

1. 先按过程边界切成 components。
2. 给每个 component 定义局部变量、输入变量和输出变量。
3. 把过程内控制流写成带 guard/assignment 的 internal edges。
4. 把过程调用写成 call edges，并显式列出 input/output variable lists。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. component tuples；
2. variable interpretations；
3. stacked configurations；
4. internal/call/return transition relations；
5. summary transitions。

### 交换与互操作

它与当前文库中两条线直接相连：

1. 向上承接 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 与 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM` 母线。
2. 向软件验证侧连接 `Bebop`、`Moped`、布尔程序抽象和 monitor product。

## 配套基础设施

- 建模/编辑工具：文中实现为 `Vera`。
- 解析/交换/元模型支持：核心是 `ERSM` tuple、guarded commands 与 summary edges；原文未给统一交换格式。
- 仿真/执行支持：显式状态搜索可直接按 configuration 语义运行。
- 验证/分析支持：on-the-fly reachability、fair cycle detection、monitor product。
- 代码生成/转换支持：文中说明可从 `C`-like 程序抽象到 `ERSM`；未提供通用代码生成器。
- 标准化或社区生态：研究型 family，主要与程序模型检查和 pushdown analysis 社区互操作。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流上还带有限变量更新的程序抽象。
2. 希望把 `RSM` 直接接到软件模型检查工具的中间表示。
3. 需要 shallow bug hunting、显式状态搜索或 monitor product 的递归系统。

### 需求前提

1. 变量域必须有限或已被抽象成有限域。
2. 系统的复杂度主要来自递归与有限数据，而不是并发或时间。
3. 过程接口可以压成输入/输出变量列表。

### 不适用或高成本场景

如果主要难点是并发线程间同步，应转向 `CRSM`；如果主要难点是 open-system/game semantics，应转向 `RGG` 或 open hierarchy；如果还要 dense time，则应转向 timed recursive family。

## 与相邻形式主义的关系

相对 `RSM`，`ERSM` 把 variables、guards 和 assignments 纳入了模型本体；相对布尔程序或 pushdown program model，它仍然保留 component / box / entry-exit 的状态机直觉；相对 [verification-of-well-formed-communicating-recursive-state-machines-tcs/desc.md](../verification-of-well-formed-communicating-recursive-state-machines-tcs/desc.md)，它还没有引入 fork-join 并发。

## 与本研究的关系

### 对 Project 1 的价值

它说明层次状态机理论线不仅会长出 `RSM` 这种纯 control-flow 节点，还会自然长出 `ERSM` 这种“带有限数据作用域”的中间表示。这对后续从需求文本映射到带变量守卫的状态机尤其关键。

### 对状态机自动建模的启发

如果需求里已经同时出现“递归子过程”和“变量守卫/更新”，那最终目标模型就不应只停在 plain `RSM`，而要考虑 `ERSM` 这类 family；否则后续验证接口会缺一个关键层。

## 重要的相关工作

1. [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：给出 `RSM` 的会议版母定义。
2. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：给出 `RSM` 的 journal full version。
3. `Bebop` 与 `Moped`：文中直接把它们作为 `ERSM`/boolean-program symbolic checker 的对照基线。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🧩 经典离散状态机`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🎛️ 控制 / 反应式逻辑`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> ERSM` 位置，用来说明 `RSM` 在 classic automata-theory 语境下确实长出了“变量化递归状态机”这条可稳定命名的侧枝。
