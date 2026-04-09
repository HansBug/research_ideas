# 捕获 EMSO 逻辑的数据词自动机 / An Automaton over Data Words That Captures EMSO Logic

## 基本信息

- 标题：An Automaton over Data Words That Captures EMSO Logic
- 中文标题：捕获 EMSO 逻辑的数据词自动机
- 作者：Benedikt Bollig
- 发表：*Proceedings of the 22nd International Conference on Concurrency Theory (CONCUR 2011)*, pp. 171-186, 2011
- DOI：`10.1007/978-3-642-23217-6_12`
- 链接：https://doi.org/10.1007/978-3-642-23217-6_12
- 形式主义：`Class Register Automata (CRA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 逻辑-自动机桥接
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `CRA` 元组、signature-induced look-back、register update 映射与 `rEMSO -> CRA` 的 elementary translation。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 signature `S`、带局部/全局接受条件的自动机 tuple 与基于 sphere locality 的构造。

## 简报

这篇论文提出的 `CRA`，本质上是把 `register automata` 和 `class-memory automata` 融合成一个真正面向 data words 的一向自动机本体。它一边允许当前输入位置把数据值写进寄存器，一边又允许沿着 signature 给出的“上一条同类边”回看过去的位置状态和寄存器内容，因此比单纯的 `RA` 或 `CMA` 都更适合表达动态通信和多数据值位置上的结构关系。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线里，`CRA` 是 `CMA` 再向前走一步的 register-augmented 分支。
- 构造方式简述：自动机从左到右扫描 data word；每步可根据 `prev_\triangleright(i)` 所指向的过去位置状态、过去寄存器内容和当前多维 data values 决定转移，并更新当前寄存器。
- 基础设施与场景简述：原文纯理论，但给出了 `rEMSO` 到 `CRA` 的 elementary translation，并说明 `CRA` 可覆盖 `CMA`、non-guessing `CRA`、若干 `RA / FRA` 路线以及动态通信模型。

```text
data word + signature edges -> one-way scan -> look back along signature -> compare/store data values -> local/global acceptance
```

## 形式主义定义与核心对象

### 定义对象

`CRA` 处理的是每个位置可携带多个数据值的 data words。与经典单数据值 data-word 模型不同，它允许 signature `S` 指定多种“上一相关位置”关系，例如同进程前驱、spawn 来源、消息来源等。

### 核心抽象

原文把 class register automaton 定义为：

$$
A=(Q,R,\Delta,(F_{\triangleright})_{\triangleright\in S},\Phi)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `R` 是有限寄存器集。
3. `\Delta` 是转移集合。
4. `F_{\triangleright}\subseteq Q` 是每条 signature relation `\triangleright` 对应的 local final states。
5. `\Phi` 是全局接受条件，是关于状态计数约束 `q\le N` 的布尔公式。

单条转移写成：

$$
(p,g)\xrightarrow{a}(q,f)
$$

上式中的符号逐项解释如下：

1. `p:S\rightharpoonup Q` 是部分映射，说明若某个 `\triangleright` 前驱存在，则它必须处于哪个状态。
2. `g` 是 guard，可比较当前位置的数据值和过去位置寄存器中的数据值。
3. `a` 是当前有限标签。
4. `q` 是目标状态。
5. `f:R\rightharpoonup (\mathrm{dom}(p)\times R)\cup([m]\times\mathbb N)` 指定寄存器如何从过去位置寄存器或当前/局部球内数据值更新。

### 一个最小例子与通俗解释

最能体现 `CRA` 价值的直观例子，是“一个进程在之前收到某个进程标识后，稍后必须和同一个标识发生匹配通信”。此时可以：

1. 在某个 send / fork 位置把相关数据值写入寄存器。
2. 在之后的 receive 位置，沿着 `\prec_{\mathrm{proc}}`、`\prec_{\mathrm{msg}}` 或 `\prec_{\mathrm{fork}}` 回看过去位置。
3. 用 guard 比较“当前读到的数据值”与“过去位置寄存器里存的值”是否相等。

通俗地说，`CRA` 像“能沿着几类结构化回边回看过去、而且回看时还能带寄存器”的 data-word 自动机。它不是只记“同一个数据值上次在什么状态”，而是还能记“那时手里还存着哪些别的数据值”。

### 运行 / 接受 / 转移语义

单步语义的关键是对当前位置 `i` 解释“当前数据值”和“沿某条 signature 回看的寄存器值”。原文写成：

$$
\mathrm{val}_i(k)=d^k(i),\qquad \mathrm{val}_i((\triangleright,r))=\rho_{\mathrm{prev}_{\triangleright}(i)}(r)
$$

上式中的符号逐项解释如下：

1. `d^k(i)` 是当前位置第 `k` 个数据值。
2. `\rho_j(r)` 是位置 `j` 上寄存器 `r` 的内容。
3. `\mathrm{prev}_{\triangleright}(i)` 是按照 relation `\triangleright` 找到的上一相关位置。

因此，转移是否可用取决于三层信息：

1. `p` 对过去状态的要求是否满足。
2. `g` 对当前数据值与过去寄存器值的比较是否为真。
3. `f` 是否把寄存器更新为过去寄存器中的某值，或当前位置 / 局部球中的某值。

接受条件也分两层：

$$
L(A)=\{w\mid \exists\ \text{accepting run of}\ A\ \text{on}\ w\}
$$

其中“accepting”要求：

1. 所有在某条 relation 上已经没有后继的位置，其状态落入对应的 `F_{\triangleright}`。
2. 整条运行还必须满足全局计数条件 `\Phi`。

### 语义边界

`CRA` 的增强点是“signature-guided look-back + registers”，而不是：

1. 任意双向读头；
2. 栈或树导航；
3. 数值算术和全序数据运算；
4. timed clocks 或连续变量。

它仍然属于一向、有限控制的 infinite-alphabet automata，只是把“过去可访问的位置”做成了结构化的一等对象。

### 关键性质与判定边界

原文最关键的谱系与逻辑结论可压成：

$$
rEMSO(S)\subseteq CRA(S)
$$

$$
\mathrm{CMA}(S)\subseteq CRA(S),\qquad CRA^{-}(S)\subseteq CRA(S)
$$

$$
\text{register automata over } S^m_{+1}\ \subseteq\ CRA^{-}(S)
$$

上面几式中的符号逐项解释如下：

1. `rEMSO(S)` 是论文中的 local existential monadic second-order logic。
2. `CRA^{-}(S)` 是 non-guessing `CRA`，只允许把寄存器更新为过去寄存器值或当前位置数据值。
3. `CMA` 可看成 `CRA` 的一个特例：寄存器更新函数处处未定义。
4. 论文主定理给出了 `rEMSO -> CRA` 的 elementary-time realizability translation。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍保持有限状态主骨架。 |
| 事件 / 触发 | 强支持 | 每个 data-word 位置都会触发一次 state/register lookup 与更新。 |
| 守卫 / 数据 | 强支持 | 可比较当前多维数据值、过去寄存器值与过去位置之间的关系。 |
| 层次 | 部分支持 | 不支持树层次，但支持由 signature 定义的结构化回看。 |
| 并发 / 同步 | 部分支持 | 可建模动态通信和多进程交互，但不是显式并发组合代数。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 有明确的逻辑翻译链和多模型包容关系。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,R,\Delta,(F_{\triangleright})_{\triangleright\in S},\Phi)$` | `CRA` 的标准定义。 |
| 单步转移 | `$(p,g)\xrightarrow{a}(q,f)$` | 同时依赖过去状态、guard 与寄存器更新。 |
| 值读取 | `$\mathrm{val}_i((\triangleright,r))=\rho_{\mathrm{prev}_{\triangleright}(i)}(r)$` | 体现 signature-guided look-back。 |
| 逻辑桥接 | `$rEMSO(S)\subseteq CRA(S)$` | 论文最重要的 realizability 结果。 |
| 子类关系 | `$\mathrm{CMA}\subseteq CRA,\ CRA^{-}\subseteq CRA$` | 把 class-memory 与 register 线路统一起来。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输入是否适合写成带 signature 的 data word，而不是普通字符串。
2. 再明确哪些过去位置是“允许回看”的，例如同进程前驱、上一条消息边或 spawn 来源。
3. 用寄存器决定哪些历史数据值要被显式带到未来比较。
4. 若不需要寄存器，只要 per-class 最近状态，优先退回 `CMA`。

### 机器可处理承载方式

机器可处理承载方式就是：

1. `CRA` 元组；
2. signature `S` 及其 `prev_\triangleright` 关系；
3. guard 里的等值比较；
4. register update 映射 `f`；
5. local / global acceptance。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

它直接连接 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 的 `CMA`、[fresh-register-automata/desc.md](../fresh-register-automata/desc.md) 路线以及动态通信模型；其中单父边蓝本树更适合把它挂在 `Class-Memory Automata` 之下，但在语义上它同时吸收了 register-style 机制。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 signature、sphere locality、guard 与 register update。
- 仿真/执行支持：可按一向扫描、回看过去位置和寄存器更新的 operational semantics 执行。
- 验证/分析支持：`rEMSO -> CRA` elementary translation、Hanf-locality 风格 sphere 构造、多个子类互译。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：主要存在于 data words、XML/database logic 与 communicating-systems 理论生态中。

## 适用场景与需求前提

### 适用场景

适合建模带进程标识、消息标识、会话标识的 data words，尤其是那些需要“从当前点沿某条结构化关系回看过去，并比较当时寄存器内容”的对象。

### 需求前提

1. 输入能压成 data word。
2. 过去可访问位置能通过有限个 relation `S` 稳定定义出来。
3. 关键约束主要是 equality、局部回看和有限寄存器携带，而不是数值算术。

### 不适用或高成本场景

如果需求只需简单 class-level last-state，则 `CMA` 更轻；如果需求是 tree / stack / timed / hybrid 结构，则应转向相应家族；如果需要更强的全局逻辑能力，单靠 `CRA` 也可能不够。

## 与相邻形式主义的关系

相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 中的 `CMA`，`CRA` 多了显式寄存器和过去寄存器值引用；相对 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)，它不再只沿输入前缀历史做 freshness / equality，而是允许沿 signature 指向的结构边回看；相对 [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)，它更强调 register-carrying look-back 而不是纯 class memory。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里的 class-memory 方向从“只记最近状态”推进到“最近状态 + 历史寄存器内容”，使 `Data / Infinite-Alphabet` 主枝更完整。

### 作为目标形式主义还是中间表示

更适合作为理论节点和高阶中间表示，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

当需求文本里反复出现“当前事件要和某类过去事件上的某个 ID 对上”“需要按消息/进程关系回看历史并比较标识符”时，LLM 应优先考虑 `CRA` 风格，而不是只靠普通 `FSM` 扩状态。

### 现实限制

它的价值主要在谱系、表达力和逻辑桥接；原文没有工程级标准格式与现成工具链。

## 重要的相关工作

### 奠基或前身工作

- [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md)
- [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md)

### 同类型或同家族工作

- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)
- [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)
- [history-register-automata/desc.md](../history-register-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合挂到当前演化树 `Finite Automata -> Data / Infinite-Alphabet -> Class-Memory Automata` 之后的 `Class Register Automata` 子枝。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
