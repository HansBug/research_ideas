# 二阶理论与无限树上的自动机的可判定性 / Decidability of Second-Order Theories and Automata on Infinite Trees

## 基本信息

- 标题：Decidability of Second-Order Theories and Automata on Infinite Trees
- 中文标题：二阶理论与无限树上的自动机的可判定性
- 作者：Michael O. Rabin
- 发表：Transactions of the American Mathematical Society, 141:1-35, 1969
- DOI：`10.1090/S0002-9947-1969-0246760-1`
- 链接：https://lara.epfl.ch/w/_media/sav08/rabin69s2s.pdf
- 形式主义：Automata on Infinite Trees / Rabin Infinite-Tree Automata
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供实现；机器可处理入口是无限二叉树上的状态表 `M : S \times \Sigma \to P(S \times S)` 与 path-wise acceptance。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是 `\Sigma`-valued tree、run `r:T_x\to S` 与 `F \subseteq P(S)` 的路径接受语义。

## 简报

这篇论文的历史地位非常高：它不仅证明了二叉树后继结构上单二阶理论 `S2S` 的可判定性，还在证明过程中建立了**无限树自动机**这条主干。原文的关键对象不是普通 word automata，而是作用在无限二叉树上的有限状态机：每个节点的一个状态要分裂成左右子树上的两个后继状态，整棵树是否被接受则由每条无限路径上的“无限次出现状态集合”来判定。

- 形式主义定位：`Tree Automata` 主干上的无限树 / path-acceptance 分支，通常被后世称为 `Rabin` tree theorem 对应的 automata line。
- 构造方式简述：先定义 `\Sigma`-valued infinite binary tree，再定义状态表 `M`、run `r` 与 path-wise acceptance。
- 基础设施与场景简述：原文服务于 `S2S` 决定性证明，没有工程工具；但它直接开出了 infinite-tree automata、MSO on trees、后来的 parity / Rabin / Muller acceptance 全部主线。

```text
无限二叉树 -> 节点状态展开 run -> 路径上的无限出现状态集合 -> 树语言 T(W) -> S2S decidability
```

## 形式主义定义与核心对象

### 定义对象

论文把无限二叉树写成：

$$
T = \{0,1\}^*
$$

每个节点是一个有限 `0/1` 词，左右孩子分别是 `x0` 与 `x1`。一个 `\Sigma`-值树是节点到字母表的映射。

### 核心抽象

原文 Definition 1.3 给出的树自动机骨架是：

$$
\mathcal W = (S, M, S_0, F)
$$

其中：

$$
M : S \times \Sigma \to \mathcal P(S \times S)
$$

并且：

1. `S` 是有限状态集。
2. `M` 是节点展开表；若当前节点状态为 `s`、标签为 `a`，则 `M(s,a)` 给出左右子树可取的状态对集合。
3. `S_0 \subseteq S` 是初始状态集。
4. `F \subseteq \mathcal P(S)` 是被允许的“路径上无限次出现的状态集合”家族。

对树 `t=(v,T_x)`，run 定义为：

$$
r : T_x \to S
$$

并满足对任意 `y \in T_x`：

$$
(r(y0), r(y1)) \in M(r(y), v(y))
$$

### 一个最小例子与通俗解释

一个最小例子是识别“整棵无限二叉树所有节点都标成 `a`”的树语言。此时只需要一个状态 `q`，并规定：

1. 只有在读到 `a` 时 `(q,q)` 才允许作为两个子节点的后继状态。
2. 任何路径上无限出现的状态集合都只能是 `\{q\}`。

通俗地说，这种自动机不是沿一条线往前跑，而是站在一棵无限树的根上，把自己的状态同时分发给左孩子和右孩子。它是否接受，不看某一条单独运行，而要看所有无限路径是否都满足给定的无限访问条件。

### 运行 / 接受 / 转移语义

原文 Definition 1.5 的接受条件是：

$$
t \in T(\mathcal W)
\iff
\exists r \text{ run on } t \text{ such that } r(x)\in S_0 \text{ and } \forall \pi,\ \mathrm{In}(r|\pi)\in F
$$

这里：

1. `x` 是当前子树根。
2. `\pi` 是 `T_x` 的一条无限路径。
3. `r|\pi` 是 run 在这条路径上的限制。
4. `\mathrm{In}(r|\pi)` 是沿该路径无限次出现的状态集合。

这是一种典型的 path-wise infinitary acceptance。它后来和 `Muller`、`Rabin`、`parity` 等无限对象接受条件一起构成了自动机理论的核心分支。

### 语义边界

相对普通 word automata，它的输入对象从线性串换成了无限树；相对有限树 automata，它新增了真正的无限路径接受语义。它天然适合表达“每条分支都要满足某种长期性质”的树对象，而不只是局部节点约束。

### 关键性质与判定边界

原文在模型层面给出了几个关键结论：

1. 投影封闭：

$$
A \subseteq V_{\Sigma_1 \times \Sigma_2} \text{ f.a. definable}
\implies
p_1(A) \subseteq V_{\Sigma_1} \text{ f.a. definable}
$$

2. 补集封闭：

$$
V_\Sigma - T(\mathcal W) \text{ is f.a. definable}
$$

3. emptiness 可判定：

$$
T(\mathcal W) = \varnothing\ ?
$$

存在有效的、甚至 elementary-recursive 的判定过程。

4. 这些结果反过来支撑：

$$
S2S \text{ is decidable}
$$

也就是二叉树后继结构上的单二阶理论可判定。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制，但状态会向左右子树分裂传播。 |
| 事件 / 触发 | 支持 | 每个节点标签触发局部展开。 |
| 守卫 / 数据 | 不支持 | 无显式变量守卫。 |
| 层次 | 强支持 | 输入对象本身是树。 |
| 并发 / 同步 | 部分支持 | 一个节点的状态同时约束左右两个子分支。 |
| 时间约束 | 不支持 | 无时钟语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树结构。 |
| 可执行 / 可验证性 | 强支持 | projection、complement、emptiness 与 `S2S` 对应都非常清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 树自动机 | `$\mathcal W=(S,M,S_0,F)$` | 作用于无限二叉树的有限状态机骨架。 |
| 状态展开 | `$(r(y0),r(y1)) \in M(r(y),v(y))$` | 当前节点的状态决定左右子节点的可能状态对。 |
| 路径接受 | `$\mathrm{In}(r|\pi)\in F$` | 每条无限路径都要满足无限访问条件。 |
| 投影封闭 | `$A$ f.a. definable $\Rightarrow p_1(A)$ f.a. definable` | 树自动机对投影稳定。 |
| 空语言判定 | `$T(\mathcal W)=\varnothing?$` | emptiness 有效可判定。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 定义树标签字母表 `\Sigma`。
2. 定义状态集 `S`。
3. 为每个 `(s,a)` 给出允许的左右状态对集合 `M(s,a)`。
4. 给出路径接受家族 `F`。

### 机器可处理承载方式

机器可处理的核心承载是：

1. `\Sigma`-valued tree。
2. run `r:T_x\to S`。
3. path-wise acceptance family `F \subseteq \mathcal P(S)`。

### 交换与互操作

原文最重要的互操作是和 `S2S` 的对应：公式可构造性地转成树自动机，树自动机也可反过来支撑逻辑可判定性证明。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程格式，核心是树对象和状态展开表。
- 仿真/执行支持：可按节点递归展开 run。
- 验证/分析支持：projection、complement、emptiness 和逻辑翻译非常强。
- 代码生成/转换支持：原文未讨论代码生成。
- 标准化或社区生态：后续形成 infinite-tree automata、MSO on trees、Rabin/Muller/parity acceptance 的完整研究主线。

## 适用场景与需求前提

### 适用场景

适合描述无限树、分支结构、层次文法树、分支程序展开和任何“每条路径都必须满足长期性质”的树对象。

### 需求前提

1. 对象本身是树而不是线性串。
2. 需要同时处理无限分支和路径级长期接受条件。
3. 关注的是树语言与逻辑可定义性，而不是工程执行脚本。

### 不适用或高成本场景

若对象只是线性词，或需求主要是工程控制器执行，那么这种无限树自动机通常过强也过抽象。

## 与相邻形式主义的关系

相对 `Tree Automata` 的有限树/经典树语言路线，它把对象推到了无限树并引入路径接受；相对 `Büchi/Muller` 的 ω-word automata，它把“无限词上的无限运行”推广成“无限树上每条路径的无限运行”。

## 与本研究的关系

### 对 Project 1 的价值

它补全了演化树里 `Tree Automata` 的关键早期节点，让“树输入 / 无限对象”这条支线不再只有后来的综述性条目。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点或处理树结构需求的高级中间表示，不适合作为普通控制系统默认终点。

### 对需求到模型生成的启发

它提醒我们：一旦需求对象是树而且分支长期性质不可忽略，线性状态机或普通有限树模型都不够，需要转入无限对象自动机线。

### 现实限制

对 `project_1` 当前关注的控制系统建模，它多数时候更像一条理论地图分支，而不是直接工程输出模型。

## 重要的相关工作

### 奠基或前身工作

- `Finite Automata` 与顺序自动机理论。
- `S2S` / monadic second-order logic on trees。

### 同类型或同家族工作

- `Tree Automata`。
- `Büchi` / `Muller` / `Rabin` / `parity` 型无限对象自动机。

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或工具。

### 与本研究关系最紧的工作

- 它为“树对象是否应该进入状态机族演化树”提供了非常稳固的经典依据。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Automata on Infinite Trees / Rabin Infinite-Tree Automata
- 论文角色：模型提出
- 核心功能：用 path-wise infinite acceptance 在无限二叉树上定义树语言。
- 关键特性：节点状态展开、路径无限访问条件、projection/complement/emptiness、`S2S` 可判定性。
- 构造方式：树标签映射 + 状态展开表 `M` + 路径接受家族 `F`。
- 基础设施：理论互操作极强，但无工程标准或工具。
- 适用场景：无限树、分支结构和基于路径长期性质的树语言分析。
- 需求前提：对象必须天然是树，且性质需要对所有无限路径施加约束。
- 状态：🟢
