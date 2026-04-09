# 可见下推转换器 / Visibly Pushdown Transducers

## 基本信息

- 标题：Visibly pushdown transducers
- 中文标题：可见下推转换器
- 作者：Emmanuel Filiot, Jean-Francois Raskin, Pierre-Alain Reynier, Frederic Servais, Jean-Marc Talbot
- 发表：*Journal of Computer and System Sciences*, 97:147-181, 2018
- DOI：`10.1016/j.jcss.2018.05.002`
- 链接：https://doi.org/10.1016/j.jcss.2018.05.002
- 形式主义：`Visibly Pushdown Transducers (VPT)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型系统化
- 工具/实现获取方式：原文未提供统一实现；机器可处理入口是 underlying `VPA`、transition-output morphism、well-nested restriction 与 look-ahead / well-nested-output 变体。
- 标准/格式获取方式：原文没有标准交换格式，核心承载方式是 `T=(A,\Omega)`、nested-word 输入字母表 `(\Sigma_c,\Sigma_i,\Sigma_r)` 与 run-level 输出拼接语义。

## 简报

这篇论文把 `Visibly Pushdown Automata` 从“识别 nested words”推进到“变换 nested words”。`VPT` 的关键点不是简单给 `VPA` 加一条输出带，而是坚持保留 visible stack discipline：读到 call 必须 push，读到 return 必须 pop，读到 internal 才能保持栈不变。这样做的结果是，`VPT` 一方面足够表达 XML / nested-word 到字符串的结构化变换，另一方面又不像一般 pushdown transducer 那样迅速掉进大面积不可判定。

- 形式主义定位：`Pushdown Automata -> Structured-word / nested-word` 子枝上的 transducer 母节点。
- 构造方式简述：在 `VPA` 的每条输入转移上附一个输出词，整条运行的输出由这些局部输出串接得到。
- 基础设施与场景简述：原文系统整理了 `dVPT / fVPT / VPT` 三层、emptiness / functionality / k-valuedness / equivalence 的复杂度，以及为什么原始 `VPT` 不合成、而 `well-nested VPT` 能恢复 composition。

```text
nested word 输入 -> visibly pushdown 栈纪律 + 转移输出 -> word transduction -> XML / structured trace 变换
```

## 形式主义定义与核心对象

### 定义对象

`VPT` 处理的是 nested words，也就是在结构化字母表上书写的有限串。输入字母表被分成三类：

$$
\Sigma=(\Sigma_c,\Sigma_i,\Sigma_r)
$$

其中：

1. `\Sigma_c` 是 call 符号。
2. `\Sigma_i` 是 internal 符号。
3. `\Sigma_r` 是 return 符号。

模型读取的是 nested-word 输入，输出则是一般字母表 `\Delta` 上的普通词，不要求输出本身也带 nesting 结构。

### 核心抽象

原文把 `VPT` 定义为：

$$
T=(A,\Omega)
$$

其中 underlying visibly pushdown automaton 为：

$$
A=(Q,I,F,\Gamma,\delta)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `I\subseteq Q` 是初始状态集。
3. `F\subseteq Q` 是接受状态集。
4. `\Gamma` 是栈字母表。
5. `\delta` 是 call / internal / return 三类可见下推转移。
6. `\Omega:\delta\to\Delta^*` 是把每条转移映射到输出词的 morphism。

### 一个最小例子与通俗解释

一个最小例子是把 XML 风格 nested word 压平成纯文本：对 opening tag 的 call 转移输出 `\varepsilon`，对 closing tag 的 return 转移也输出 `\varepsilon`，只在 internal 字符上原样输出。

通俗地说，`VPT` 像“会做结构化流式改写的 `VPA`”。它不是先把整棵树读完再统一生成输出，而是边按 nested-word 栈纪律走，边在每步转移上增量吐出一小段字符串。

### 运行 / 接受 / 转移语义

设一条运行在输入 `u=a_1\cdots a_\ell` 上走过的转移序列为：

$$
\rho=t_1\cdots t_\ell\in\delta^*
$$

则这条运行的输出定义为：

$$
\Omega(\rho)=\Omega(t_1)\cdots \Omega(t_\ell)
$$

若从配置 `(q,\sigma)` 出发读取 `u` 并输出 `v` 到达 `(q',\sigma')`，原文记为：

$$
(q,\sigma)\xrightarrow{u/v}(q',\sigma')
$$

整台转导机定义的关系是：

$$
R(T)=\{(u,v)\mid \exists q\in I,\ q'\in F,\ \sigma\in \Gamma^*.\ (q,\bot)\xrightarrow{u/v}(q',\sigma)\}
$$

上式中的符号逐项解释如下：

1. `\sigma`、`\sigma'` 是栈内容。
2. `\bot` 是初始空栈记号。
3. `R(T)` 是由所有接受运行产生的输入输出对组成的二元关系。
4. `T` 若是 functional，则每个输入 `u` 至多对应一个输出 `v`。

### 语义边界

`VPT` 继承了 `VPA` 的 visible stack discipline，因此比一般 pushdown transducer 弱很多，但也正因此保住了很多判定性。它能表达层次结构输入上的单遍栈式变换，但不能像任意 pushdown transducer 那样随意操纵输入相关的栈动作。

### 关键性质与判定边界

原文给出的主结论可压成：

$$
\mathrm{dom}(T)\in \mathrm{VPL}
$$

$$
\mathrm{range}(T)\in \mathrm{CFL}
$$

$$
\mathrm{emptiness}(\mathrm{VPT}) \in \mathrm{PTime}
$$

$$
\mathrm{functionality}(\mathrm{VPT}) \in \mathrm{PTime},\qquad k\text{-}\mathrm{valuedness}(\mathrm{VPT}) \in \mathrm{coNP}
$$

$$
\mathrm{equivalence}(\mathrm{fVPT}) \text{ is Exptime-complete},\qquad \mathrm{equivalence}(\mathrm{dVPT}) \in \mathrm{PTime}
$$

并且闭包边界是：

$$
R(\mathrm{VPT}) \text{ 对 } \cup \text{ 封闭，但不对 } \cap,\ \mathrm{complement},\ \mathrm{composition} \text{ 封闭}
$$

上面几式中的符号逐项解释如下：

1. `\mathrm{dom}(T)` 是输入域。
2. `\mathrm{range}(T)` 是输出值域。
3. `\mathrm{VPL}` 是 visibly pushdown languages。
4. `\mathrm{fVPT}` 和 `\mathrm{dVPT}` 分别是 functional / deterministic `VPT`。
5. 原始 `VPT` 不合成，是后续 `well-nested VPT` 被引入的直接原因。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | underlying `VPA` 提供有限控制。 |
| 事件 / 触发 | 强支持 | call / internal / return 三类输入决定转移与栈行为。 |
| 守卫 / 数据 | 不支持 | 原始模型无显式变量与数据守卫。 |
| 层次 | 强支持 | 栈纪律与 nested-word 输入直接绑定。 |
| 并发 / 同步 | 不支持 | 对象是单个 nested word。 |
| 时间约束 | 不支持 | 无时钟与时间语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散字符串 / 文档变换。 |
| 可执行 / 可验证性 | 强支持 | emptiness、membership、functionality、equivalence 等边界清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$T=(A,\Omega)$` | `VPT` 的标准定义。 |
| underlying automaton | `$A=(Q,I,F,\Gamma,\delta)$` | 仍然是 visibly pushdown 自动机骨架。 |
| 输出语义 | `$\Omega(\rho)=\Omega(t_1)\cdots\Omega(t_\ell)$` | 输出是逐转移拼接得到。 |
| 转导关系 | `$R(T)\subseteq \Sigma^*\times\Delta^*$` | 输入 nested word 到输出 word 的关系定义。 |
| 判定边界 | `PTime / coNP / Exptime` | 原文系统给出的功能性、值域数和等价性复杂度。 |

## 构造方式与承载格式

### 建模入口

1. 先判断输入对象是否真的是 nested words 或其线性化树。
2. 再为 call / internal / return 三类输入设计状态迁移和 push/pop 规则。
3. 最后把局部输出挂到转移上，而不是额外引入独立生成文法。

### 机器可处理承载方式

机器可处理承载方式就是：

1. structured input alphabet `(\Sigma_c,\Sigma_i,\Sigma_r)`；
2. underlying `VPA` 的状态和栈；
3. 转移到输出词的映射 `\Omega`；
4. 需要时再扩展到 well-nested outputs 或 look-ahead 变体。

### 交换与互操作

它与 [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md) 的关系最直接：`VPT` 是在 `nested words / VPA` 母线上把“识别”变成“变换”。它与 [two-way-visibly-pushdown-automata-and-transducers/desc.md](../two-way-visibly-pushdown-automata-and-transducers/desc.md) 的关系则是：后者把读头改成双向，从而获得更强的 MSO 级变换能力。

## 配套基础设施

- 建模/编辑工具：原文未提供统一编辑器。
- 解析/交换/元模型支持：核心是 structured alphabet、underlying `VPA` 与 output morphism。
- 仿真/执行支持：可按流式读取 nested word 并逐步产生输出。
- 验证/分析支持：emptiness、translation membership、type checking、functionality、k-valuedness、equivalence。
- 代码生成/转换支持：原文未讨论工程代码生成，但后续给出 `well-nested VPT` 与 look-ahead 变体。
- 标准化或社区生态：与 XML、nested words、tree transducers、MSO transductions 和 streaming transformations 紧密相关。

## 适用场景与需求前提

### 适用场景

适合 XML 文档处理、结构化程序轨迹变换、nested-word 到纯文本或规范化结构输出的变换任务。

### 需求前提

1. 输入必须带稳定的 call / return / internal 结构。
2. 变换逻辑主要依赖层次结构，而不是一般数据计算。
3. 输出最好能按输入扫描过程逐步产生。

### 不适用或高成本场景

若输出本身也必须保持复杂树结构且要求合成闭包，或若输入不是 visibly-structured word，那么原始 `VPT` 往往不够；此时更合适的是 well-nested / two-way / tree-transducer family。

## 与相邻形式主义的关系

相对 [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)，`VPT` 从识别提升到变换；相对 [two-way-visibly-pushdown-automata-and-transducers/desc.md](../two-way-visibly-pushdown-automata-and-transducers/desc.md)，它保持单向扫描，因此表达力更弱但模型更简单；相对 [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)，它没有 typed variables 和更强的 single-pass tree-output 机制。

## 与本研究的关系

### 对 Project 1 的价值

它能把演化树中 `Structured-word / nested-word` 支线从 acceptor 补到 transducer，避免 `NWA` 与 `STT/2VPT` 之间出现空洞。

### 作为目标形式主义还是中间表示

更适合作为结构化输入变换的目标形式或中间表示，而不是一般控制器行为建模语言。

### 对需求到模型生成的启发

如果需求同时强调“输入是层次结构化事件/文档”与“输出是一个顺序化结果串”，那 `VPT` 往往比普通 `FST` 或一般 `PDT` 更自然，也更容易维持可判定性。

### 现实限制

原始 `VPT` 不对 composition 封闭，这意味着它虽是很好的母节点，但并不是所有工程流水线都适合直接压在它上面。

## 重要的相关工作

### 奠基或前身工作

- [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)

### 同类型或同家族工作

- [two-way-visibly-pushdown-automata-and-transducers/desc.md](../two-way-visibly-pushdown-automata-and-transducers/desc.md)
- [streaming-tree-transducers/desc.md](../streaming-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准，但其应用背景与 XML / SAX / nested-word processing 明确相连。

### 与本研究关系最紧的工作

- 它最适合补到 `Pushdown Automata -> Structured-word / nested-word` 的 transducer 母节点，并为继续追 `2VPT`、well-nested 输出与 XML/tree transformation 分支提供接口。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Visibly Pushdown Transducers (VPT)`
- 论文角色：模型系统化
- 核心功能：在 `VPA` 的 visible-stack 骨架上增量产生输出，从而定义 nested-word 到 word 的结构化变换。
- 关键特性：structured input、visible stack、run-level output morphism、functionality/k-valuedness/equivalence 可分析、原始 composition 不封闭。
- 构造方式：`T=(A,\Omega)`，其中 `A` 是 underlying `VPA`，`\Omega` 把每条转移映射成输出词。
