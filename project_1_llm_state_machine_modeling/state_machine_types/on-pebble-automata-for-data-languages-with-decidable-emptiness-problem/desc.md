# 关于具有可判定空性的 Pebble 数据语言自动机 / On Pebble Automata for Data Languages with Decidable Emptiness Problem

## 基本信息

- 标题：On Pebble Automata for Data Languages with Decidable Emptiness Problem
- 中文标题：关于具有可判定空性的 Pebble 数据语言自动机
- 作者：Tony Tan
- 发表：*Journal of Computer and System Sciences*, 76(8):778-791, 2010
- DOI：`10.1016/j.jcss.2010.03.004`
- 链接：https://doi.org/10.1016/j.jcss.2010.03.004
- 形式主义：`Top-View Weak Pebble Automata (Top-View Weak PA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 可判定边界整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 weak `k`-PA / top-view weak `k`-PA 的 transition relation、pebble assignment `\theta` 与到一向交替 `1`-register automaton 的模拟。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data word、栈式 pebble 纪律和 `Guess-Split-Verify` 风格的 register-automata 编译。

## 简报

这篇论文的价值，不只是给 pebble automata 再做一条复杂度结论，而是把一个可以稳定挂树的新家族命名出来：`Top-View Weak Pebble Automata`。原文先证明 weak `2`-pebble automata 的空性可判定、weak `3`-pebble automata 的空性不可判定，然后进一步提出 top-view 弱化版，只允许当前 pebble 和最近上一枚 pebble 做数据值比较。这个限制看起来很小，但恰好把模型压到“仍有表达力、又能通过 `1`-register alternating automata 判空”的可判定边界上。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 主枝上的 pebble 型 data-word 子类，位于 full pebble automata 与 register automata 之间的可判定边界。
- 构造方式简述：输入上维护一组按栈纪律放置的 pebbles；head pebble 决定当前读头，top-view 限制只允许与紧邻上一层 pebble 的 data value 做 equality test。
- 基础设施与场景简述：原文纯理论，但给出与 alternating / nondeterministic / deterministic 版本的一致表达力，以及到一向交替 `1`-register automata 的有效翻译。

```text
data word -> stack-disciplined pebbles -> local equality with previous pebble -> alternating / deterministic analysis -> 1-register simulation
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 finite data strings，也就是每个位置携带有限标签和无限域数据值的线性词。模型使用有限个 pebbles 在输入上做嵌套放置与回收，并以 pebble 的当前位置和数据值关系驱动状态转移。

### 核心抽象

原文先回顾 weak `k`-pebble automata，再在第 6 节把 top-view 版本写成：

$$
A=\langle \Sigma,Q,q_0,\mu,F\rangle
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是有限标签字母表。
2. `Q` 是有限状态集。
3. `q_0\in Q` 是初始状态。
4. `F\subseteq Q` 是接受状态集。
5. `\mu` 是转移集合。

对 weak `k`-PA，transition 形如：

$$
(i,\sigma,V,q)\to(q',act)
$$

上式中的符号逐项解释如下：

1. `i` 是当前 head pebble 编号。
2. `\sigma` 是当前读到的有限标签。
3. `V` 记录可见 pebble 的 equality 信息。
4. `q,q'` 是源状态与目标状态。
5. `act` 属于 `\{\mathrm{stay},\mathrm{right},\mathrm{place\text{-}pebble},\mathrm{lift\text{-}pebble}\}`。

top-view weak `k`-PA` 的关键限制是：

$$
V\in\{\emptyset,\{i+1\}\}
$$

并且其语义由下式确定：

$$
V=
\begin{cases}
\emptyset, & a_{\theta(i+1)}\neq a_{\theta(i)} \\
\{i+1\}, & a_{\theta(i+1)} = a_{\theta(i)}
\end{cases}
$$

这里 `\theta(i)` 是 pebble `i` 当前指向的位置，`a_{\theta(i)}` 是该位置的数据值。也就是说，head pebble 只能拿自己当前看到的 datum 与上一层 pebble 的 datum 比较，而不能再看更外层的 pebble。

### 一个最小例子与通俗解释

一个直观例子是“当前位置的 datum 以后还会不会再次在某个局部窗口里重现，并满足某个标签模式”。普通有限自动机做不了这种跨位置 equality 检查；full pebble automata 可以，但太强而导致空性快速不可判定。top-view weak PA 的做法是：

1. 先用外层 pebble 固定一个基准位置。
2. 再放下内层 pebble 向右扫描。
3. 只比较这两层 pebble 当前看到的数据值是否相等。

通俗地说，它像“只能看最近一层上下文的 pebble 机器”。它允许有限层嵌套书签，但每一步只允许做非常局部的 data-equality 比较，因此刚好落在可判定区间内。

### 运行 / 接受 / 转移语义

原文对 weak pebble automata 的 configuration 写成：

$$
[i,q,\theta]
$$

上式中的符号逐项解释如下：

1. `i` 是当前 head pebble 编号。
2. `q` 是当前状态。
3. `\theta` 是 pebble assignment，记录每个 pebble 所在输入位置。

初始 configuration 为：

$$
[k,q_0,\theta_0],\quad \theta_0(k)=0
$$

若存在合适的 transition `(i,\sigma,V,q)\to(q',act)`，则一步转移可写成：

$$
[i,q,\theta]\vdash_A[i',q',\theta']
$$

其中 `act` 决定 `i'` 和 `\theta'` 的变化：

1. `right` 让 head pebble 向右移动。
2. `place-pebble` 在当前 pebble 位置之上再放一个新 pebble。
3. `lift-pebble` 把当前 pebble 移除并返回上一层。
4. `stay` 只变状态，不移动 pebble。

接受语义仍是 alternating 风格的“leads to acceptance”：universal state 的所有后继都必须 leads to acceptance，existential state 只要有一个后继 leads to acceptance 即可。

### 语义边界

原文给出的关键边界不是“pebble 越多越强”这么简单，而是：

1. weak `2`-PA 仍可判定；
2. weak `3`-PA 已不可判定；
3. top-view weak `k`-PA` 把 equality 视野限制到最近两层 pebble 后，又重新回到可判定；
4. 并且 alternating / nondeterministic / deterministic 三种控制方式表达力相同。

这使得 top-view weak PA 更像一个“受控的 pebble family”，而不是单纯的 lower-bound gadget。

### 关键性质与判定边界

原文最关键的结论可压成：

$$
\mathrm{emptiness}(\mathrm{weak}\ 2\text{-}\mathrm{PA})\ \text{decidable}
$$

$$
\mathrm{emptiness}(\mathrm{weak}\ 3\text{-}\mathrm{PA})\ \text{undecidable}
$$

$$
\forall k\ge 2,\ \mathrm{TopViewWeak}\ k\text{-}\mathrm{PA}\ \le\ \mathrm{one\text{-}way\ alternating}\ 1\text{-}\mathrm{RA}
$$

$$
\mathcal L(\mathrm{Alt\ TopViewWeak}\ k\text{-}\mathrm{PA}) = \mathcal L(\mathrm{Det\ TopViewWeak}\ k\text{-}\mathrm{PA})
$$

并且：

$$
LTL^\downarrow_1(\Sigma,X,U)\subseteq \mathcal L(\mathrm{TopViewWeak}\ k\text{-}\mathrm{PA})
$$

上面几式中的符号逐项解释如下：

1. 第三式表示可有效编译到一向交替 `1`-register automaton。
2. 第四式说明 alternation 与 nondeterminism 在这个子类上不会额外增益表达力。
3. 最后一式表示它足够强，能覆盖带 `freeze` 的线性时序逻辑语言。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制是主骨架。 |
| 事件 / 触发 | 强支持 | 在线性 data word 上单向扫描。 |
| 守卫 / 数据 | 强支持 | 通过最近两层 pebble 的 datum equality 进行判断。 |
| 层次 | 不支持 | 对象仍是线性词，不是树。 |
| 并发 / 同步 | 部分支持 | alternating 语义提供分支义务，但非并发组合模型。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 空性可判定，且能有效编译到 `1`-RA。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=\langle \Sigma,Q,q_0,\mu,F\rangle$` | top-view weak `k`-PA 的标准骨架。 |
| 配置 | `$[i,q,\theta]$` | 运行由当前 head pebble、状态和 pebble 赋值组成。 |
| top-view 限制 | `$V\in\{\emptyset,\{i+1\}\}$` | 只允许与最近上一层 pebble 做 equality test。 |
| 可判定边界 | `$\mathrm{weak}\ 2\text{-}\mathrm{PA}$ decidable, `$\mathrm{weak}\ 3\text{-}\mathrm{PA}$ undecidable` | 说明普通 weak pebble family 的边界。 |
| register 化 | `$\mathrm{TopViewWeak}\ k\text{-}\mathrm{PA}\le \mathrm{Alt}\ 1\text{-}\mathrm{RA}$` | 为空性判定提供基础设施。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求是否真的是“局部嵌套比较最近两层 datum”，而不是任意跨层 pebble 比较。
2. 设计各层 pebble 放置、抬起与向右扫描的行为。
3. 只在最近两层 pebble 之间写 equality tests，避免滑回 full pebble automata。

### 机器可处理承载方式

机器可处理承载方式是：

1. data word；
2. weak/top-view weak `k`-PA transition system；
3. pebble assignment `\theta`；
4. 到一向交替 `1`-register automaton 的模拟。

原文没有 XML、JSON 或专门建模语言。

### 交换与互操作

它与 register automata 的互操作最关键，因为其判空性正是靠编译到 `1`-RA 获得；与 `LTL↓_1(\Sigma,X,U)` 的关系则说明它不只是 lower-bound gadget，而是能承载一整类逻辑规格。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 pebble assignment、transition relation 与 alternating acceptance。
- 仿真/执行支持：deterministic top-view weak `k`-PA 的 membership 可在 `O(n^k)` 时间内求解。
- 验证/分析支持：空性判定、alternation 去除、到 `1`-RA 的编译、复杂度边界。
- 代码生成/转换支持：无工程代码生成，但有明确 automaton-to-automaton translation。
- 标准化或社区生态：是 infinite-alphabet pebble family 的经典可判定边界节点。

## 适用场景与需求前提

### 适用场景

适合 data word 上带局部嵌套引用的数据模式，例如“当前值与上一层上下文里的值相等时才继续某条模式”，以及可由 `LTL↓_1` 描述的冻结逻辑约束。

### 需求前提

1. 输入对象需可压成 finite data word。
2. 数据比较主要发生在最近两层上下文之间。
3. 需求更像局部嵌套书签，而不是任意全局数据约束。

### 不适用或高成本场景

若需要 full pebble visibility、三层以上自由比较、树对象或时间约束，这个 family 就不够，需转向更强模型。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，它不通过有限寄存器直接存 datum，而是通过栈式 pebble 布置形成局部比较上下文；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它的判定性最终又落回 `1`-register automata，这说明它更像 pebble 视角下的可判定同层分支。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Data / Infinite-Alphabet` 主枝补出了一条此前没有稳定命名的 pebble 型子线，尤其适合扩树。

### 作为目标形式主义还是中间表示

更适合作为理论节点或中间表示，而不是需求工程最终输出语言。

### 对需求到模型生成的启发

当需求文本反复出现“当前位置只需与上一层上下文绑定值比较”的模式时，LLM 可以优先考虑 top-view pebble / one-register family，而不是直接上更强但更贵的 data automata。

### 现实限制

没有工程标准和成熟运行时；其主要价值在模型边界、表达力和可判定性。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)
- `Finite state machines for strings over infinite alphabets` 是本文明确承接的 register / pebble 母线入口，但当前文库仍缺正式条目。

### 同类型或同家族工作

- [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md)
- [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)
- [variable-automata-over-infinite-alphabets/desc.md](../variable-automata-over-infinite-alphabets/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合补到 `Finite Automata -> Data / Infinite-Alphabet` 主枝里作为 pebble family 的稳定命名节点，并帮助说明“为什么 full pebble 太强、top-view 才是可判定边界”。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Top-View Weak Pebble Automata (Top-View Weak PA)`
- 论文角色：模型提出 / 可判定边界整理
- 核心功能：在 data words 上用栈式 pebble 比较最近两层 datum，并把 pebble family 压回可判定空性的子类。
- 关键特性：top-view equality、stack-disciplined pebbles、weak `2/3` 边界、到 `1`-RA 的编译、`LTL↓_1` 覆盖。
- 构造方式：`A=\langle \Sigma,Q,q_0,\mu,F\rangle` + configuration `[i,q,\theta]` + top-view restriction `V\in\{\emptyset,\{i+1\}\}`。
- 基础设施：纯理论模型，无工程标准/工具；核心分析设施是 automata-to-register translation。
- 适用场景：finite data words 上的局部嵌套 data-equality 模式分析。
- 需求前提：输入需是 data word，且主要比较发生在最近两层 pebble 上下文之间。
- 状态：🟢
