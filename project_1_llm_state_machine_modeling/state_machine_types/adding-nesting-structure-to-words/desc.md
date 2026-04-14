# 为词增加嵌套结构 / Adding Nesting Structure to Words

## 基本信息

- 标题：Adding Nesting Structure to Words
- 中文标题：为词增加嵌套结构
- 作者：Rajeev Alur, P. Madhusudan
- 发表：Journal of the ACM, 56(3), 2009
- DOI：`10.1145/1516512.1516518`
- 链接：https://www.cis.upenn.edu/~alur/Jacm09.pdf
- 形式主义：Nested Word Automata
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：作者主页提供论文 PDF；原文聚焦模型、复杂度与逻辑刻画，不附带统一实现。
- 标准/格式获取方式：原文没有标准交换格式，核心承载方式是 nested word / tagged word / tree encoding 三种互转表示。

## 简报

这篇论文提出 `Nested Words` 与 `Nested Word Automata (NWA)`，核心目标是把“线性顺序”和“层次嵌套”这两种结构放进同一个有限状态模型里。它既不像普通 word automata 那样只看线性序列，也不像 tree automata 那样只看树，而是显式保留二者的双重结构，因此特别适合 XML/HTML、结构化程序执行轨迹和其他 dual linear-hierarchical data。

- 形式主义定位：介于 words 与 ordered trees 之间的双结构对象及其有限状态接受器。
- 构造方式简述：先定义 nested word `n=(a_1\cdots a_\ell,\nu)`，再定义带线性状态和层次状态的 `NWA`。
- 基础设施与场景简述：原文给出与 `VPL`、MSO、regular tree languages 的严格对应，并直接面向 XML、程序调用返回和结构化文档处理。

```text
线性词 + 嵌套边 -> nested word -> NWA -> regular nested languages -> MSO / VPL / tree encodings
```

## 形式主义定义与核心对象

### 定义对象

原文把 nested word 定义为一串按线性顺序排列的位置，再额外加上一组不交叉的 matching relation：

$$
n = (a_1 \cdots a_\ell,\ \nu)
$$

其中：

1. `a_i` 是第 `i` 个位置上的标签。
2. `\nu` 是从 call 到 return 的嵌套边关系。
3. 位置可分为 call、return 和 internal。

这使得 nested words 同时泛化了 ordinary words 和 ordered trees。

### 核心抽象

论文在第 3 节给出的 `NWA` 结构是：

$$
A = (Q, q_0, Q_f, P, p_0, P_f, \delta_c, \delta_i, \delta_r)
$$

上式中的符号逐项解释如下：

1. `Q` 是线性状态集。
2. `q_0` 是初始线性状态。
3. `Q_f` 是线性接受状态集。
4. `P` 是层次状态集。
5. `p_0` 是初始层次状态。
6. `P_f` 是层次接受状态集。
7. `\delta_c : Q \times \Sigma \to Q \times P` 是 call 转移。
8. `\delta_i : Q \times \Sigma \to Q` 是 internal 转移。
9. `\delta_r : Q \times P \times \Sigma \to Q` 是 return 转移。

这一定义的直觉是：线性状态沿词向前传播，而层次状态沿 nesting edge 传播；在 return 位置，二者重新汇合。

### 一个最小例子与通俗解释

一个最小例子是 XML 风格的 `<a> ... </a>` 结构。把 `<a>` 看作 call，把 `</a>` 看作 return，把正文字符看作 internal：

1. 读到 `<a>` 时，`NWA` 一边更新线性状态，一边把层次状态沿嵌套边送出去。
2. 读正文时，只沿线性边更新。
3. 读到 `</a>` 时，再把从左侧线性路径带来的状态与从 `<a>` 沿 nesting edge 带来的状态合并。

通俗地说，`NWA` 像一个“同时记住当前位置在文本哪里、又记住它在层次结构里属于谁”的自动机。它不是只沿横向看，也不是只沿树向下看，而是两条线一起看。

### 运行 / 接受 / 转移语义

对 nested word `$n=(a_1\cdots a_\ell,\nu)$`，原文把 run 写成线性状态序列 `q_i` 与 call 位置上的层次状态 `p_i`。核心规则是：

1. 若位置 `i` 是 call，则

$$
\delta_c(q_{i-1}, a_i) = (q_i, p_i)
$$

2. 若位置 `i` 是 internal，则

$$
\delta_i(q_{i-1}, a_i) = q_i
$$

3. 若位置 `i` 是 return，且其 call-predecessor 为 `j`，则

$$
\delta_r(q_{i-1}, p_j, a_i) = q_i
$$

接受条件是：

$$
q_\ell \in Q_f \quad \text{and for pending calls } i,\ p_i \in P_f
$$

这些公式中的符号逐项解释如下：

1. `q_i` 是第 `i` 个位置之后的线性状态。
2. `p_i` 是沿 call 位置 `i` 的 nesting edge 传播的层次状态。
3. `j` 是当前 return 对应的 call-predecessor。
4. `q_\ell` 是词末线性状态。

### 语义边界

相对 `Finite Automata`，它增加了显式嵌套边；相对 `Tree Automata`，它保留了线性顺序；相对 `VPA`，它更显式地把嵌套边作为一等对象，而不只是在栈纪律中隐含表示。

### 关键性质与判定边界

原文最关键的理论结果包括：

1. `NWA` 的 regular nested-word languages 对 union、intersection、complement、concatenation、Kleene-*、prefix 和 homomorphism 封闭。
2. nondeterministic `NWA` 可以 determinize。
3. 若 nondeterministic automaton 有 `s` 个线性状态，则 determinization 的线性状态数可达

$$
2^{s^2}
$$

并且这一上界是 tight 的。

4. regular nested languages 与 `MSO` 可定义性完全对应：

$$
L \text{ is regular } \iff L \text{ is definable in MSO over nested words}
$$

5. inclusion / equivalence 问题可判定，nondeterministic `NWA` 的 inclusion 是 `EXPTIME`-complete。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 同时具有线性状态和层次状态。 |
| 事件 / 触发 | 支持 | 标签驱动 call / internal / return 三类处理。 |
| 守卫 / 数据 | 不支持 | 原始模型不带变量守卫。 |
| 层次 | 强支持 | nesting edges 是一等结构。 |
| 并发 / 同步 | 不支持 | 不直接表达并发组件。 |
| 时间约束 | 不支持 | 没有时钟语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散、有限状态。 |
| 可执行 / 可验证性 | 强支持 | determinization、闭包、MSO characterization、VPL/tree correspondence 全部明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| nested word | `$n=(a_1\cdots a_\ell,\nu)$` | 同时保留线性顺序和嵌套边。 |
| 模型元组 | `$A=(Q,q_0,Q_f,P,p_0,P_f,\delta_c,\delta_i,\delta_r)$` | 同时跟踪线性状态和层次状态。 |
| call/return 语义 | `$\delta_c$` / `$\delta_r$` | 进入嵌套与退出嵌套时的状态传播。 |
| 确定化代价 | `$2^{s^2}$` | nondeterministic 到 deterministic 的 tight 上界。 |
| 逻辑刻画 | `$L \text{ regular } \iff L \in \mathrm{MSO}$` | regular nested languages 与 MSO 完全对应。 |

## 构造方式与承载格式

### 建模入口

建模先要给出 positions 的线性顺序，再给出 call-return 的 matching relation。

### 机器可处理承载方式

原文给出三种稳定承载方式：

1. nested word 本体。
2. tagged word / linear encoding。
3. ordered tree / hedge / XML 对应编码。

### 交换与互操作

论文明确建立了 `NWA` 与 `VPL`、MSO、regular tree languages、XML/hedge encodings 的互操作通道。

## 配套基础设施

- 建模/编辑工具：原文未给出具体编辑器。
- 解析/交换/元模型支持：提供 nested word、tagged word、tree 三种编码骨架。
- 仿真/执行支持：可按线性扫描 + 嵌套边传播执行。
- 验证/分析支持：支持 determinization、boolean closure、MSO characterization 和 inclusion/equivalence 判定。
- 代码生成/转换支持：原文未讨论代码生成。
- 标准化或社区生态：与 XML、程序验证、tree automata 和 visibly pushdown 理论紧密耦合。

## 适用场景与需求前提

### 适用场景

适用于 XML/HTML 文档、结构化程序执行轨迹、带匹配括号/标签的数据和其他 dual linear-hierarchical objects。

### 需求前提

1. 对象既有线性顺序也有不交叉的嵌套匹配。
2. 嵌套关系可显式给出为 matching relation。
3. 需要同时支持 word-style 与 tree-style 操作。

### 不适用或高成本场景

若对象没有稳定的嵌套边，或者需要一般图结构、并发同步或实时间语义，则 `NWA` 不是首选。

## 与相邻形式主义的关系

相对 `Tree Automata`，它保留了线性顺序；相对 `VPA`，它把嵌套边显式对象化；相对普通 `FSM`，它把“谁和谁配对”也写进模型。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合处理那些需求文本里天然带有“开始/结束”“进入/退出”“打开/关闭”一类层次配对结构的对象。

### 作为目标形式主义还是中间表示

更适合作为结构化词/文档/程序轨迹的目标形式或中间表示，而不是纯控制器执行模型的唯一终点。

### 对需求到模型生成的启发

它提示我们：若需求中既要保留事件顺序，又不能丢失嵌套配对，那么直接生成 `NWA` 或其线性化 `VPL` 往往比强行压成普通 `FSM` 更自然。

### 现实限制

它仍是离散有限状态模型，不直接覆盖数据守卫、时间约束和并发组件交互。

## 重要的相关工作

### 奠基或前身工作

- classical word automata 与 tree automata。
- pushdown / recursive program verification 路线。

### 同类型或同家族工作

- `Visibly Pushdown Languages`。
- regular hedge / XML processing 与 stepwise tree automata。

### 标准 / 格式 / 工具链工作

- 原文没有单独工程标准，但与 XML / SAX 表示和 tree encodings 对接清晰。

### 与本研究关系最紧的工作

- 如果未来要从非形式化需求中抽取“显式层次配对”的状态机结构，这一分支非常值得保留。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Nested Word Automata
- 论文角色：模型提出
- 核心功能：统一表达线性顺序与层次嵌套，并用有限状态自动机识别 regular nested languages。
- 关键特性：线性状态 + 层次状态、determinization、MSO characterization、VPL/tree correspondence。
- 构造方式：nested word + matching relation + NWA transition functions。
- 基础设施：nested word / tagged word / tree 三种互转表示。
- 适用场景：XML/HTML、结构化程序轨迹、带匹配标签的层次文本。
- 需求前提：对象同时具有线性顺序和不交叉嵌套匹配。
- 状态：🟢
