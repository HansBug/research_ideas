# 无限树上的有限树自动机 / Finite Tree Automata on Infinite Trees

## 基本信息

- 标题：FINITE TREE AUTOMATA ON INFINITE TREES
- 中文标题：无限树上的有限树自动机
- 作者：Takeshi Hayashi, Satoru Miyano
- 发表：*Bulletin of Informatics and Cybernetics*, 21(3/4):71-82, 1985
- DOI：`10.5109/13369`
- 链接：https://api.lib.kyushu-u.ac.jp/opac_download_md/13369/p071.pdf
- 形式主义：Finite Tree Automata on Infinite Trees
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文未提供实现；机器可处理入口是有限 `k` 叉树自动机 tuple、run 和 `C_1,\ldots,C_6` 接受条件。
- 标准/格式获取方式：没有工程标准，核心承载方式是 `M=\langle S,\Sigma,d,s_0,\mathcal F\rangle` 和 path-wise acceptance。

## 简报

这篇论文把 finite tree automata 明确推进到了 infinite trees 上，而且不是只给一种接受方式，而是系统整理了 `C_1,\ldots,C_6` 六类路径接受条件，并直接指出 `C_1` 对应 `Büchi`、`C_5` 对应 `Muller`。因此它非常适合挂在 `Tree Automata -> infinite-tree` 这条分支上，作为从 `Rabin` 之后继续系统化 infinite-tree acceptance 的关键节点。

- 形式主义定位：`Tree Automata` 在 infinite-tree 对象上的系统化扩展。
- 构造方式简述：先给出 finite `k`-ary tree automaton 的 run，再沿每条无限 path 用 `C_1,\ldots,C_6` 判断接受。
- 基础设施与场景简述：原文完全是理论工作，但 acceptance family、嵌入定理和确定性 / 非确定性细化非常适合拿来补树。

```text
无限 k 叉树 -> finite tree automaton run -> path-wise acceptance condition -> infinite-tree language class
```

## 形式主义定义与核心对象

### 定义对象

输入对象是带标签的无限 `k` 叉树 `t : T_k \to \Sigma`，而不是有限树。自动机仍保持 finite-state 骨架，但接受不再由根状态一次性决定，而由每条无限 path 上长期出现的状态集决定。

### 核心抽象

原文直接把 nondeterministic finite `k`-ary tree automaton 定义成：

$$
M = \langle S, \Sigma, d, s_0, \mathcal F \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `\Sigma` 是树节点标签字母表。
3. `d : S \times \Sigma \to \mathcal P(S^k)\setminus\{\emptyset\}` 是转移函数。
4. `s_0` 是初始状态。
5. `\mathcal F` 是 final-set family，其中每个 `F \in \mathcal F` 都是一组 final states。

若 `t : T_k \to \Sigma` 是一棵无限 `k` 叉树，则 `M` 在 `t` 上的一条 run `r : T_k \to S` 满足：

$$
r(\varepsilon)=s_0
$$

并且对每个 `x \in T_k` 有：

$$
(r(x0),r(x1),\ldots,r(x(k-1))) \in d(r(x), t(x))
$$

上式中的符号逐项解释如下：

1. `\varepsilon` 是根节点。
2. `x0,\ldots,x(k-1)` 是 `x` 的 `k` 个子节点。
3. `r(x)` 是 run 在节点 `x` 处的状态。
4. `t(x)` 是节点 `x` 的标签。

对路径 `\pi \subseteq T_k`，原文定义无限次出现状态集：

$$
\mathrm{Inf}(r\mid \pi)=\{\, s \in S \mid s=r(x)\text{ for infinitely many }x\in\pi \,\}
$$

### 一个最小例子与通俗解释

最小例子可以取二叉无限树上“每条路径都必须无限次看到好状态 `g`”。自动机在根启动后，对每个子节点分配后继状态；若一条 path 上 `g` 只出现有限多次，则该 path 失败，整棵树也失败。

通俗地说，这个模型像“在一棵永远长下去的树上并行展开的有限状态机”。你不能只看某个叶子，因为没有叶子；只能看每条无限分支在长期运行里会不断重复哪些状态。

### 运行 / 接受 / 转移语义

原文的核心接受定义是：存在一条 run `r`，并且对每条 path `\pi`，都存在某个 final set `F \in \mathcal F` 满足对应的 `C_i` 条件。可统一写成：

$$
t \in L_i(M)
\iff
\exists r\ \forall \pi \subseteq T_k\ \exists F \in \mathcal F,\ \mathrm{Cond}_{C_i}(r,\pi,F)
$$

原文列出的六类条件中，最关键的几个是：

$$
C_1:\ \mathrm{Inf}(r\mid\pi)\cap F \neq \emptyset
$$

$$
C_2:\ \mathrm{Inf}(r\mid\pi)\subseteq F
$$

$$
C_5:\ \mathrm{Inf}(r\mid\pi)=F
$$

$$
C_6:\ r(\pi)=F
$$

这里 `r(\pi)` 表示路径 `\pi` 上出现过的状态集合。原文并明确说明：

1. `C_1` 是 `Büchi` 式接受；
2. `C_5` 是 `Muller` 式接受。

### 语义边界

相对 finite-tree automata，它把对象从有限树扩到 infinite trees；相对 `Rabin Infinite-Tree Automata` 单一接受条件，这篇论文强调的是“同一 finite tree automaton 骨架下多种 acceptance families 的系统比较”。

### 关键性质与判定边界

论文的代表性结论包括：

1. 对 `C_1,\ldots,C_4`，单个 final set 就足够；
2. 通过 embedding theorem 把 infinite-tree 语言类与 `\omega`-word 语言类联系起来；
3. 在 infinite-tree 场景中，deterministic 与 nondeterministic 的差异可以用 nondeterministic degree 等方式进一步细化。

其中一个关键整理是：

$$
\mathcal N_i^k = \{L_i(M)\mid M \text{ is nondeterministic}\},\qquad
\mathcal D_i^k = \{L_i(M)\mid M \text{ is deterministic}\}
$$

这使 infinite-tree language classes 可以按对象和接受方式统一比较。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态控制。 |
| 事件 / 触发 | 不适用 | 输入对象是无限树而不是事件流。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般数据变量。 |
| 层次 | 强支持 | 层次来自树对象本体。 |
| 并发 / 同步 | 不支持 | 分支不是同步进程，而是对象结构。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 infinite-tree 识别。 |
| 可执行 / 可验证性 | 强支持 | 接受类比较、嵌入与表达力分析都很系统。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$M=\langle S,\Sigma,d,s_0,\mathcal F\rangle$` | finite `k`-ary tree automaton on infinite trees 的标准骨架。 |
| run 约束 | `$(r(x0),\ldots,r(x(k-1)))\in d(r(x),t(x))$` | 父节点状态和标签决定子节点状态向量。 |
| 无限出现集 | `$\mathrm{Inf}(r\mid\pi)$` | path 上无限次出现的状态集。 |
| Büchi 条件 | `$\mathrm{Inf}(r\mid\pi)\cap F\neq\emptyset$` | `C_1`。 |
| Muller 条件 | `$\mathrm{Inf}(r\mid\pi)=F$` | `C_5`。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先确定无限对象是否是 `k` 叉树；
2. 给出有限状态集和标签字母表；
3. 选定 `C_1,\ldots,C_6` 中的接受口径；
4. 决定 final-set family 的粒度。

### 机器可处理承载方式

机器可处理承载方式是 automaton tuple、run 和 path acceptance family，而不是工程 XML/JSON。

### 交换与互操作

它直接连到：

1. `\omega`-word automata；
2. `Rabin / Büchi / Muller` acceptance；
3. infinite-tree logic 和后续 parity / alternating 分支。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 tuple、run 和 acceptance family。
- 仿真/执行支持：可以定义 run，但主要服务于识别与表达力分析。
- 验证/分析支持：类关系、嵌入定理、determinism 细化是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 infinite-tree automata 经典理论主线。

## 适用场景与需求前提

### 适用场景

适用于 infinite-tree languages、分支结构上的长期性质、树路径一致性和逻辑可判定性分析。

### 需求前提

1. 对象必须天然是无限树。
2. 需求必须关心每条无限 path 的长期行为。
3. 可接受 finite-state skeleton + path acceptance 这种语义。

### 不适用或高成本场景

若对象只是有限树、XML 文档或有限深度 AST，则普通 tree automata / hedge automata 更直接。

## 与相邻形式主义的关系

相对 [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)，它从 `Rabin` 单一路线推进到统一的 `C_1,\ldots,C_6` 接受框架；相对 [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)，这里专注 infinite-tree 对象本身；相对 [tree-automata/desc.md](../tree-automata/desc.md)，它把有限树识别推进到 infinite-tree 接受。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata -> infinite-tree` 这条树枝从 `Rabin` 的单一代表，扩成了“有限树自动机骨架 + 多类长期接受”的更稳定主线。

### 作为目标形式主义还是中间表示

更适合作为理论分支节点和谱系骨架，而不是控制系统需求建模的默认终点。

### 对需求到模型生成的启发

它提醒我们：一旦对象是树且性质要约束“每条无限分支”的长期行为，`FA/PDA` 或普通 tree automata 都不够，必须切换到 infinite-tree acceptance。

### 现实限制

没有工程标准和直接工具线，主要服务于理论表达力与判定边界分析。

## 重要的相关工作

### 奠基或前身工作

- [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)

### 同类型或同家族工作

- [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)
- `Büchi / Muller` acceptance on `\omega`-words

### 标准 / 格式 / 工具链工作

- 原文没有工程标准，重点在 acceptance family 与类关系。

### 与本研究关系最紧的工作

- 它为 `Tree Automata -> Rabin Infinite-Tree -> Finite Tree Automata on Infinite Trees` 提供了清晰的后继节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Finite Tree Automata on Infinite Trees
- 论文角色：分支整理
- 核心功能：把 finite tree automata 扩展到 infinite trees，并统一比较六类路径接受条件。
- 关键特性：`C_1..C_6`、path-wise acceptance、`Büchi/Muller` 关联、deterministic/nondeterministic 细化。
- 构造方式：有限状态骨架 + infinite-tree run + final-set family。
- 基础设施：理论分析成熟，但无工程标准和工具。
- 适用场景：infinite-tree language、分支长期性质、逻辑与 automata 类比较。
- 需求前提：对象是无限树，且性质必须沿每条 path 解释。
- 状态：🟢
