# 布奇自动机 / Büchi Automata

## 基本信息

- 标题：On a Decision Method in Restricted Second Order Arithmetic
- 中文标题：受限二阶算术中的一种判定方法
- 作者：J. Richard Büchi
- 发表：`1960` 年国际会议论文；后收入 *Logic, Methodology and Philosophy of Science, Proceeding of the 1960 International Congress*，Elsevier，1966，pp. 1-11
- DOI：`10.1016/S0049-237X(09)70564-6`
- 链接：https://people.irisa.fr/Nicolas.Markey/PDF/Papers/lmps1960-Buc.pdf
- 形式主义：Büchi Automata / Infinite-Input Finite Automata
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：奠基定义
- 工具/实现获取方式：原文没有工程实现；机器可处理入口是 finite automata recursion、behavior 与后续稳定化的 `\omega`-word 接受条件。
- 标准/格式获取方式：原文没有工程标准，核心承载方式是状态递归 `r(0)=I,\ r(t')=J[i(t),r(t)]` 与关于无限输入的有限状态行为定义。

## 简报

这篇论文的直接目标是给受限二阶算术 `SC` 建立判定方法，但它真正固定下来的关键对象，是“有限状态控制如何读无限输入并与逻辑可定义性对接”的骨架。后来的 `Büchi automata` 这一稳定命名，就是沿这条线长出来的。因此，把它收为演化树上的 `Büchi` 节点是一个基于原文对象与后续标准术语的保守归纳。

- 形式主义定位：有限自动机主干向无限输入 / `\omega`-word 长期行为扩展的奠基节点。
- 构造方式简述：原文直接使用 finite automata recursion 和 behavior；后续稳定写法可压成 `\omega`-word 上带无限重复接受条件的有限自动机。
- 基础设施与场景简述：原文纯理论，但把 automata、周期性类、逻辑可定义性和判定方法绑到了一起，是 `\omega`-automata 总线最关键的早期源头之一。

```text
无限输入序列 -> 有限状态递归 -> 长期行为 / 周期类 -> 逻辑可定义性与判定
```

## 形式主义定义与核心对象

### 定义对象

原文的直接对象不是今天教科书里已经完全定型的 `Büchi automaton` 五元组，而是“在无限输入序列上运行的有限状态递归”。因此，本条目把两层定义分开写：

1. 原文直接给出的，是 finite automata recursion / behavior。
2. 演化树使用的 `Büchi Automata` 命名，是基于这一路线后来稳定化的标准术语。

### 核心抽象

原文第 3 节给出的核心有限状态递归可以写成：

$$
r(0) = I,\qquad r(t') = J[i(t), r(t)]
$$

并以输出谓词 `U` 读取状态：

$$
U[r(t)]
$$

上式中的符号逐项解释如下：

1. `i(t)` 是输入序列在位置 `t` 的符号或谓词值。
2. `r(t)` 是时刻 `t` 的有限状态。
3. `I` 是初始状态。
4. `J` 是由当前输入和当前状态决定下一状态的有限递归更新。
5. `U` 是定义“当前状态属于某个可观察行为类”的输出条件。

原文进一步把这类 behavior 与 `IO` 公式以及 multi-periodic sets 联系起来：

$$
\text{behavior} = EO = \text{multi-periodic sets}
$$

这里的等式是对原文 Lemma 2 和 Lemma 6 的压缩整理，表示：

1. `EO` 级公式可定义的词集合，
2. 有限自动机行为，
3. multi-periodic 词集合，

在原文口径下是同一类对象。

为了和后来的稳定树节点对齐，可以把这条路线的标准化写法保守整理成：

$$
A = (Q, \Sigma, \delta, q_0, F)
$$

以及对无限词 `\alpha \in \Sigma^\omega` 的 run：

$$
r_\alpha(0)=q_0,\qquad r_\alpha(n+1)\in \delta(r_\alpha(n), \alpha(n))
$$

接受条件写成：

$$
\alpha \in L(A) \iff \mathrm{Inf}(r_\alpha)\cap F \neq \emptyset
$$

这里最后这组三式是把原文的 infinite-input finite automata 思想，按后续稳定术语重写成 today 的 `Büchi` 形式。换言之，这里明确包含了“基于原文对象所做的后设整理”。

### 一个最小例子与通俗解释

最小例子可以取“无限词中 `a` 出现无限多次”。令自动机有两个状态：

1. `q_wait`：当前还在等待下一次 `a`；
2. `q_hit`：刚刚读到 `a`。

每当输入是 `a` 时就跳到 `q_hit`，否则回到或保持 `q_wait`。若把 `F=\{q_hit\}`，那么一条无限输入被接受，当且仅当这条运行里 `q_hit` 会被无限次访问。

通俗地说，`Büchi automata` 像“看不见结尾的有限自动机”。普通 `FA` 在读完整个词以后看最后状态；这里没有“最后一步”，于是要改成看“哪些好状态会在长期运行中反复出现”。

### 运行 / 接受 / 转移语义

原文直接使用的是状态递归和 behavior 输出，因此其无限输入语义首先体现为：

$$
r(0)=I,\qquad r(t')=J[i(t),r(t)]
$$

而在后续稳定化的 `Büchi` 语义中，接受的核心是“无限次出现”：

$$
\mathrm{Inf}(r_\alpha)=\{q\in Q \mid q\text{ appears infinitely often in }r_\alpha\}
$$

$$
\alpha \in L(A)\iff \mathrm{Inf}(r_\alpha)\cap F\neq\emptyset
$$

上式中的符号逐项解释如下：

1. `\mathrm{Inf}(r_\alpha)` 是运行中无限次出现的状态集合。
2. `F` 是被看作“good states”的接受集合。
3. 交集非空表示至少有一个好状态在长期运行里反复出现。

### 语义边界

它与普通 `Finite Automata` 的根本区别，不是状态更新骨架，而是接受语义：有限词看终止状态，无限词看长期重复访问模式。

### 关键性质与判定边界

原文直接给出的关键结果是：

1. `EO` 公式、有限自动机行为与 multi-periodic sets 等价。
2. 这条 automata-theoretic 路线可用于受限二阶算术的判定。

可把其中最关键的对象压成：

$$
\mathcal B = \{\, w \mid w \text{ is a behavior of some finite automaton recursion} \,\}
$$

$$
\mathcal B = \text{multi-periodic sets}
$$

对演化树而言，更重要的结论是：无限输入上的有限状态识别不再只是普通 `FA` 的小修小补，而是足以支撑 `\omega`-style 接受条件与逻辑可判定性的独立分支。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍保留有限状态控制骨架。 |
| 事件 / 触发 | 支持 | 输入是离散无限序列。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般数据变量。 |
| 层次 | 不支持 | 对象是线性 `\omega`-word。 |
| 并发 / 同步 | 不支持 | 不是并发交互模型。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散长期行为。 |
| 可执行 / 可验证性 | 强支持 | 其核心价值就在于把长期接受与逻辑判定接通。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 状态递归 | `$r(0)=I,\ r(t')=J[i(t),r(t)]$` | 原文直接给出的 infinite-input finite-state recursion。 |
| 输出观察 | `$U[r(t)]$` | 用有限状态输出刻画行为类。 |
| 行为等价 | `$\text{behavior}=EO=\text{multi-periodic sets}$` | 原文 Lemma 2 与 Lemma 6 的压缩表达。 |
| 后续稳定写法 | `$A=(Q,\Sigma,\delta,q_0,F)$` | 演化树中 `Büchi` 节点的 today 规范化写法。 |
| 接受条件 | `$\mathrm{Inf}(r_\alpha)\cap F\neq\emptyset$` | 后续稳定化后的 Büchi 接受条件。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 给定无限输入序列或其逻辑谓词表示；
2. 设计有限状态递归；
3. 指定行为输出或长期接受条件。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. 状态递归矩阵 / 函数；
2. 输出谓词；
3. 逻辑公式与周期类之间的对应。

### 交换与互操作

它天然连到：

1. `S1S` / monadic second-order logic；
2. `\omega`-regular languages；
3. 后来的 `Muller / Rabin / alternating` 接受条件分支。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：没有工程化交换格式。
- 仿真/执行支持：核心是有限状态递归，而不是运行时框架。
- 验证/分析支持：与逻辑判定、周期类和长期接受直接耦合。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：后续形成了 `Büchi / Muller / Rabin / parity` 整条 `\omega`-automata 生态，但原文本身仍是奠基性理论来源。

## 适用场景与需求前提

### 适用场景

适用于无限执行、非终止协议、长期重复性质、`LTL/MSO` 型逻辑语义和 `\omega`-language 识别。

### 需求前提

1. 对象必须天然是无限输入序列或可等价编码成无限序列。
2. 需求关注长期行为，而不是有限前缀终止。
3. 接受语义要能写成“某些状态无限次出现”之类的长期条件。

### 不适用或高成本场景

若对象只是有限词、单次交互或有限长度控制流程，用普通 `FA/Mealy/Moore` 更自然。

## 与相邻形式主义的关系

相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，它不是换了一套状态机骨架，而是把“接受”从 finite end-state 推向了 infinite-run condition；相对 [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)，它更像这条总线最早的 `\omega`-word 奠基点；相对 [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)，这里处理的是无限词而不是 infinite tree。

## 与本研究的关系

### 对 Project 1 的价值

它把演化树上的 `Infinite-Object / \omega-Automata` 主线真正向前推到了最早的经典入口，使 `Büchi` 节点不再只是 survey 中的待补名字。

### 作为目标形式主义还是中间表示

更适合作为理论母型与分支节点，而不是控制系统需求建模的默认终点。

### 对需求到模型生成的启发

它提示我们：一旦需求包含“始终 / 最终反复 / 无限次满足”这种长期性质，就不能再只靠 finite acceptance，必须切换到 `\omega`-style 自动机语义。

### 现实限制

原文没有工程标准、格式或工具链；它的价值主要在于奠定谱系，而不是提供可直接部署的建模载体。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)

### 同类型或同家族工作

- [finite-automata-on-infinite-objects/desc.md](../finite-automata-on-infinite-objects/desc.md)
- [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原文无工程标准；后续 `\omega`-automata 工具线是从这条理论主干继续长出来的。

### 与本研究关系最紧的工作

- 它为 `Infinite-Object / \omega-Automata -> Büchi` 这条树枝提供了最早可入库的经典奠基条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Büchi Automata / Infinite-Input Finite Automata
- 论文角色：奠基定义
- 核心功能：把有限状态递归推广到无限输入，并把长期行为与逻辑可定义性连接起来。
- 关键特性：finite automata recursion、multi-periodic sets、长期接受、`SC/S1S` 路线奠基。
- 构造方式：有限状态递归 `r(0)=I,\ r(t')=J[i(t),r(t)]`；后续稳定为 `\omega`-word 自动机。
- 基础设施：无工程标准或工具，主要提供理论母型。
- 适用场景：无限输入、长期行为、逻辑到自动机的桥接分析。
- 需求前提：对象是无限序列，且关心无限次出现或长期重复性质。
- 状态：🟢
