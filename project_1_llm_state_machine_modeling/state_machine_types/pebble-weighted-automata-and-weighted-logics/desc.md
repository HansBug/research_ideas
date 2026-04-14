# Pebble 加权自动机与加权逻辑 / Pebble Weighted Automata and Weighted Logics

## 基本信息

- 标题：Pebble Weighted Automata and Weighted Logics
- 中文标题：Pebble 加权自动机与加权逻辑
- 作者：Benedikt Bollig, Paul Gastin, Benjamin Monmege, Marc Zeitoun
- 发表：*ACM Transactions on Computational Logic*, 15(2):1-35, 2014
- DOI：`10.1145/2579819`
- 链接：https://doi.org/10.1145/2579819
- 形式主义：`Pebble Weighted Automata (P2WA / P1WA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 逻辑-自动机桥接
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 weighted automaton 元组、`P2WA/P1WA` 转移与配置语义、以及到 `wFOTCb` 系列逻辑的双向翻译。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 semiring、weighted transition relation、stack-discipline pebbles 与 weighted logic formulas。

## 简报

这篇论文解决的是 weighted automata 主线上的一个真实缺口：普通 weighted automata 不足以覆盖带 transitive closure 的加权逻辑，而 pebble weighted automata 正是补这个缺口的机器模型。它先把经典 `1WA` 作为基线，再引入带 pebbles 的 two-way / one-way weighted automata，最后证明在交换半环上 `P2WA`、`P1WA` 与 `wFOTCb` 逻辑完全等价。对当前演化树而言，这正好把 `Weighted Automata` 旁边又补出一条不同于 `CRA` 的经典子枝。

- 形式主义定位：`Finite Automata -> 加权 / 随机扩展 -> Weighted Automata` 之下的 pebble-weighted 子线。
- 构造方式简述：自动机在有限状态和半环权值之上，再叠加 stack-discipline pebbles 与 two-way / one-way 读头移动；接受词的值是所有 simple accepting runs 权值的半环求和。
- 基础设施与场景简述：原文纯理论，但把 `P2WA / P1WA`、weighted automata、`wFOTCb` 逻辑以及 evaluation / emptiness 边界统一到了同一框架里。

```text
输入词 -> weighted states + semiring weights + pebbles -> run weights 聚合 -> weighted series / weighted logic
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是把有限字符串映到半环值的 formal power series。与 Boolean 自动机不同，词不再只是“接收或拒绝”，而是被映成一个来自半环 `S` 的权值，例如计数、最小代价、最大得分或整数差值。

### 核心抽象

作为基线，普通 weighted automaton 写成：

$$
A = (Q, A, I, F, \Delta, \mathrm{weight})
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `A` 是有限输入字母表。
3. `I \subseteq Q` 是初始状态集。
4. `F \subseteq Q` 是接受状态集。
5. `\Delta \subseteq Q \times A \times Q` 是转移集合。
6. `\mathrm{weight} : \Delta \to S` 为每条转移赋半环权值。

论文在此基础上引入 `p`-pebble two-way weighted automaton：

$$
A = (Q, A, I, F, \Delta, \mathrm{weight})
$$

虽然元组外形与 `1WA` 相同，但此时

$$
\Delta \subseteq Q \times \widetilde A \times 2^{\{1,\ldots,p\}} \times D \times Q
$$

其中：

1. `\widetilde A = A \cup \{B,C\}`，`B/C` 是输入左右端标记。
2. `2^{\{1,\ldots,p\}}` 记录当前输入位置上有哪些 pebbles。
3. `D = \{\rightarrow,\leftarrow,\mathrm{drop},\mathrm{lift}\}` 是动作集合。

`P2WA` 在词 `u` 上的 configuration 写成：

$$
(q,\pi,i)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `\pi` 编码当前已放下 pebbles 的位置栈。
3. `i` 是当前头位置。

一步转移可保守写成：

$$
(q,\pi,i) \vdash (q',\pi',i')
$$

其更新规则由动作决定：

1. `\rightarrow` / `\leftarrow` 改变头位置。
2. `\mathrm{drop}` 在当前位置放下一枚新 pebble，并把头重置到左端。
3. `\mathrm{lift}` 弹出最内层 pebble，并把头恢复到该 pebble 所在位置。

### 一个最小例子与通俗解释

论文给出的经典例子是：用一枚 pebble 计算

$$
u \mapsto 2^{|u|^2}
$$

其做法是：

1. 依次在每个输入位置 drop 一枚 pebble。
2. 每次 drop 后都从左到右扫描整条词。
3. 在这次扫描中的每一步都乘上权值 `2`。

因为这样的全词扫描一共做了 `|u|` 次，每次长度又是 `|u|`，最后得到的正是 `2^{|u|^2}`。

通俗地说，`PWA` 像“带位置书签的 weighted automaton”。普通 weighted automaton 只能在一次线性扫描里累积局部代价；加了 pebbles 后，它可以把某些位置保存下来，围绕这些位置重复做加权扫描和组合。

### 运行 / 接受 / 转移语义

对普通 weighted automaton，词 `u=u_1\cdots u_n` 上一条 run `\rho` 的权值定义为：

$$
\mathrm{weight}(\rho) = \prod_{i=1}^n \mathrm{weight}(q_{i-1},u_i,q_i)
$$

接受词的总值是所有 accepting runs 的半环和。

对 `P2WA`，run 是 configuration 序列。其总权值同样是单步权值的乘积，而词值定义为：

$$
\llbracket A \rrbracket(u) = \sum_{\rho \text{ simple accepting run on } u} \mathrm{weight}(\rho)
$$

这里“simple”很关键，意思是同一条 run 中不允许重复访问相同 configuration，否则 two-way + pebble 的组合会让语义失控。

论文随后定义 `P1WA`，它是 `P2WA` 的语法受限版：

1. 不允许左移。
2. lift 后不能立刻 drop。

在这个限制下，所有 runs 都天然 simple。

### 语义边界

这篇论文给 `PWA` 画出的边界很清楚：

1. 它仍然只处理线性词，不处理树。
2. 它保留 weighted automata 的半环值语义，而不是回到 Boolean 接受。
3. `P2WA` 与 `P1WA` 的等价依赖交换半环；若半环不交换，这个结论不能直接照搬。
4. emptiness / satisfiability 的正结果也只在某些半环类别上成立。

### 关键性质与判定边界

原文第 5 节的核心结果是：

$$
\mathrm{P2WA} \equiv \mathrm{P1WA}
$$

更精确地说：

$$
f \text{ recognizable by P2WA } \iff f \text{ recognizable by P1WA}
$$

前提是工作在交换半环上。

第 5.4 节把 automata 与逻辑完全接通：

$$
f \text{ is } \mathrm{wFOTCb}(FO)\text{-definable}
\iff
f \text{ is recognizable by P2WA}
\iff
f \text{ is recognizable by P1WA}
$$

论文还给出更细的等价口径：

$$
\mathrm{wFOTCb}(FO) \equiv \mathrm{wFOTCb;<}(FO) \equiv \mathrm{P2WA} \equiv \mathrm{P1WA}
$$

算法边界方面，原文给出：

$$
\mathrm{Eval}(P1WA) = O(|Q|^3 \cdot |u|^{\max(p,1)})
$$

同时在一般半环上保留一个重要负结果：

$$
\mathrm{emptiness}(\mathrm{P1WA\ with\ 2\ pebbles\ over\ } \mathbb Z) \text{ undecidable}
$$

这说明 `PWA` 不是“只比 weighted automata 多一点点”的保守扩展，而是显著更强的一条 family。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保留有限状态控制。 |
| 事件 / 触发 | 强支持 | 输入是线性词上的逐位置扫描。 |
| 守卫 / 数据 | 部分支持 | 通过 pebbles 观察位置，不是一般数据寄存器。 |
| 层次 | 不支持 | 对象不是树。 |
| 并发 / 同步 | 不支持 | 非并发模型，但权值求和会聚合多条 run。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 强支持 | 半环权值是核心，不限于 Boolean。 |
| 可执行 / 可验证性 | 强理论支持 | logic equivalence、evaluation complexity 与 emptiness boundary 明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基线模型 | `$A=(Q,A,I,F,\Delta,\mathrm{weight})$` | ordinary weighted automaton 的标准元组。 |
| `P2WA` 配置 | `$(q,\pi,i)$` | 当前状态、pebble 栈位置编码与头位置。 |
| one-way / two-way 等价 | `$\mathrm{P2WA}\equiv \mathrm{P1WA}$` | 在交换半环上 two-way 不增加表达力。 |
| logic bridge | `$\mathrm{wFOTCb}(FO)\equiv \mathrm{P2WA}\equiv \mathrm{P1WA}$` | 补齐 weighted logic 的 automata 落点。 |
| 负结果 | `$\mathrm{emptiness}(\mathrm{P1WA},\mathbb Z,2\text{ pebbles})$ undecidable` | 强度已经足够高到出现经典不可判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输出值所在的半环以及加法 / 乘法含义。
2. 若普通 weighted automata 不能表达需要的 transitive-closure / nested positional aggregation，再升级到 `PWA`。
3. 尽量优先使用 `P1WA` 视角，因为它的 simple-run 语义是语法保证的。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 半环 `S`；
2. weighted transition relation；
3. pebbles 的位置栈 `\pi`；
4. `P2WA / P1WA` configuration semantics；
5. 到 `wFOTCb` 逻辑的双向翻译。

原文没有 XML、JSON、DSL 或标准交换格式。

### 交换与互操作

它与普通 weighted automata 的互操作是“0 pebble 即退化回 weighted automata”；与加权逻辑的互操作则是整篇论文的主线；在演化树上，它同 [regular-functions-and-cost-register-automata/desc.md](../regular-functions-and-cost-register-automata/desc.md) 一起构成 `Weighted Automata` 下面两条风格不同的后继线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 semiring、simple run 语义、crossing-sequence 构造和 weighted logic。
- 仿真/执行支持：`P1WA` 可按 one-way semantics 直接评价。
- 验证/分析支持：evaluation complexity、logic equivalence、emptiness / satisfiability 边界是主线。
- 代码生成/转换支持：原文不讨论工程代码生成，但给出 automata / logic 的理论双向翻译。
- 标准化或社区生态：属于 weighted automata 与 quantitative logic 交叉地带的经典理论节点。

## 适用场景与需求前提

### 适用场景

适合以下类型的问题：

1. 词到权值的 regular-style 映射。
2. 需要围绕某些位置做重复扫描与权值聚合的 quantitative language。
3. 需要把 weighted logic 落到具体 automaton family。

### 需求前提

1. 输入必须是线性词。
2. 输出必须是某个半环上的值，而不是结构化字符串 / 树。
3. 需要的位置回看应能用有限枚 pebbles 表达。

### 不适用或高成本场景

若只需普通 weighted automata 即可表达，`PWA` 会显得过重；若输出是 cost register 风格的确定性值更新，则 `CRA` 可能更自然；若对象是树，则要转向 tree-weighted family。

## 与相邻形式主义的关系

相对 [weighted-logics-and-weighted-automata-survey/survey.md](../weighted-logics-and-weighted-automata-survey/survey.md) 中的普通 weighted automata 主线，这篇论文补出了带位置书签的加权后继；相对 [regular-functions-and-cost-register-automata/desc.md](../regular-functions-and-cost-register-automata/desc.md)，这里走的是 semiring + runs aggregation，而不是 deterministic cost-register 更新；相对 [copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md](../copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md)，两者都属于 quantitative family，但母型完全不同。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里 `Weighted Automata` 下面原本主要是 `CRA` 的一侧，再补出 `Pebble Weighted Automata` 这条更接近 logic/automata 等价的经典分支。

### 作为目标形式主义还是中间表示

更适合作为定量需求的理论中间表示与谱系节点，而不是控制系统最终执行语言。

### 对需求到模型生成的启发

如果需求文本里不仅有“累计代价”，还带有“围绕某些位置重复聚合”“带 transitive closure 的 quantitative specification”这类结构，LLM 应考虑 `PWA` 而不只是普通 weighted automata 或 `CRA`。

### 现实限制

原文没有工程生态，而且 many positive results 依赖交换半环，因此它在本研究里的价值主要是演化树与表达力边界。

## 重要的相关工作

### 奠基或前身工作

- [weighted-logics-and-weighted-automata-survey/survey.md](../weighted-logics-and-weighted-automata-survey/survey.md)

### 同类型或同家族工作

- [regular-functions-and-cost-register-automata/desc.md](../regular-functions-and-cost-register-automata/desc.md)
- [copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md](../copyless-cost-register-automata-structure-expressiveness-and-closure-properties/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合在主蓝本树中作为 `Weighted Automata` 之下 `Pebble Weighted Automata` 子节点的代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Pebble Weighted Automata (P2WA / P1WA)`
- 论文角色：模型提出 / 逻辑-自动机桥接
- 核心功能：把 weighted automata 提升到带 pebbles 的 two-way / one-way 形式，并与 weighted transitive-closure logic 精确对齐。
- 关键特性：semiring weights、simple accepting runs、`P2WA/P1WA` 等价、weighted logic bridge、整数半环上的不可判定边界。
- 构造方式：`(Q,A,I,F,\Delta,\mathrm{weight})` 元组加配置 `(q,\pi,i)` 与 `drop/lift/move` 规则。
- 基础设施：纯理论模型，无工程标准或工具；核心在于 semiring、crossing sequences 与 weighted logic translation。
- 适用场景：quantitative languages、位置相关加权聚合、weighted logic automata 落点分析。
- 需求前提：输入是线性词，输出是半环值，且需要有限枚 pebbles 的位置书签能力。
- 状态：🟢
