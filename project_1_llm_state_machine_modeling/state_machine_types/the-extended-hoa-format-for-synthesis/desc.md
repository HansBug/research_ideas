# 面向综合的扩展 HOA 格式 / The Extended HOA Format for Synthesis

## 基本信息

- 标题：The Extended HOA Format for Synthesis
- 中文标题：面向综合的扩展 HOA 格式
- 作者：Guillermo A. Perez
- 发表：arXiv preprint，2020
- DOI：原文未提供
- 链接：https://arxiv.org/abs/1912.05793
- 形式主义：`extended HOA / synthesis automata exchange format`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：面向 reactive synthesis 的 `HOA` 扩展与 automata-game 输入格式
- 工具/实现获取方式：论文明确给出 `hoa2pg` 工具入口 `https://github.com/gaperez64/hoa-tools`。
- 标准/格式获取方式：扩展建立在 `HOA` 标准之上，原始规范入口为 `http://adl.github.io/hoaf/`；本文增加 synthesis 专用 header 与输出约定。

## 简报

这篇论文做的不是再定义一类新的 `omega` 自动机，而是把 `HOA` 从“验证世界里的 automata interchange format”推进到“综合世界里的 automata-game input format”。关键改动只有一处，却很关键：给 `HOA` 增加 `controllable-AP` 头字段，把哪些 atomic propositions 由 controller 负责、哪些由 environment 负责明确下来。这样 `HOA` 文件就不再只是接受语言的自动机描述，而能直接承载 reactive synthesis game。

- 形式主义定位：`HOA` 的 synthesis 扩展，而不是新的自动机理论支系。
- 构造方式简述：保留原 `HOA` 的 automaton body 和 acceptance 语义，只在 header 中加入 `controllable-AP` 划分 controllable / uncontrollable propositions。
- 基础设施与场景简述：依托原始 `HOA`、`controllable-AP`、`hoa2pg`、`PGSolver` 和 `AIGER` strategy output，服务从 automata 直接做 reactive synthesis 的中间层。

```text
deterministic HOA automaton + controllable-AP -> controller/environment game -> realizability or synthesis -> AIGER strategy
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 原始 `HOA` automaton format。
2. synthesis 扩展后的 `controllable-AP` header。
3. controller 与 environment 在 automaton 上进行的无限博弈。
4. 输出策略的 `AIGER` 表示。
5. `hoa2pg` 到 `PGSolver` 的转换工具链。

### 核心抽象

论文直接给出输入 automaton 的骨架：

$$
A = (Q, q_0, \mathcal P(AP), \Delta, Acc)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集合。
2. `q_0` 是初始状态。
3. `AP` 是 atomic propositions 集合，字母表是 `\mathcal P(AP)`。
4. `\Delta` 是迁移关系。
5. `Acc` 是接受条件，也就是哪些无限运行被视为 accepting。

综合扩展的核心语法只新增一行：

$$
\texttt{header-item ::= "controllable-AP:" INT*}
$$

上式中的符号逐项解释如下：

1. `controllable-AP:` 是新增 header 关键字。
2. 后面的整数序列是 `AP` 列表中由 controller 控制的 proposition 索引。
3. 未列出的 proposition 默认由 environment 控制。
4. 这是论文的唯一格式层扩展。

论文还直接给出策略函数：

$$
\sigma : (Q \cdot \mathcal P(AP))^* \cdot Q \times U \to C
$$

上式中的符号逐项解释如下：

1. `U` 是 uncontrollable atomic propositions 的 valuation。
2. `C` 是 controllable atomic propositions 的 valuation。
3. `\sigma` 读取目前为止观察到的状态和 proposition 估值序列。
4. 输出是 controller 在当前轮要选择的 controllable valuation。
5. 若所有与 `\sigma` 一致的 plays 都生成接受运行，则该策略是 winning strategy。

### 一个最小例子与通俗解释

最小直觉例子就是在原 `HOA` header 里加一行：

```text
AP: 2 "req" "grant"
controllable-AP: 1
```

这个例子的意思是：

1. 自动机一共讨论两个 proposition，分别是 `req` 和 `grant`。
2. 第 `1` 个 proposition，也就是 `grant`，由 controller 控制。
3. `req` 默认由 environment 控制。
4. 后续 game 就围绕“环境先给 `req` 赋值，控制器再给 `grant` 赋值，然后 automaton 走一步”展开。

通俗地说，原始 `HOA` 更像“告诉你一个自动机接受哪些无限字”；扩展 `HOA` 则像“告诉你这个自动机里的字母表里哪些位由环境出、哪些位由控制器出”，从而把语言接受问题抬成了博弈和综合问题。

### 运行 / 接受 / 转移语义

论文把 automaton 上的博弈语义写得很直接：

$$
\delta : Q \times U \times C \to Q
$$

上式中的符号逐项解释如下：

1. `Q` 是 automaton 状态。
2. `U` 是 environment 选择的 uncontrollable valuation。
3. `C` 是 controller 选择的 controllable valuation。
4. `\delta` 给出下一状态。
5. 这要求输入 automaton 在综合语境下最好是 deterministic。

controller 的胜负条件可压成：

$$
\text{play is winning} \iff \rho \in Acc
$$

上式中的符号逐项解释如下：

1. `\rho` 是 game 诱导出的无限运行。
2. `Acc` 是原 automaton 的接受条件。
3. 若运行满足接受条件，则 controller 赢。

对 `SYNTCOMP 2020` 的首版限制，论文还给出 parity 条件：

$$
m(Inf) \equiv p \pmod 2
$$

上式中的符号逐项解释如下：

1. `Inf` 是在运行中无穷次出现的 transition labels 集合。
2. `m \in \{max, min\}` 指最大值或最小值版本的 parity。
3. `p \in \{0,1\}` 给出偶奇目标。
4. 例如 `max-even` 就是“无穷次出现的最大优先级必须为偶数”。

### 语义边界

1. 它扩展的是 `HOA`，不是新的 automaton acceptance family。
2. 为了求解 synthesis，输入 automaton 实际上最好 deterministic；论文也明确指出 nondeterminism 不能简单交给某一方处理。
3. 输出策略格式没有继续用 `HOA`，而是回到 `AIGER`。
4. 当前版本主要面向 `SYNTCOMP` 里的 automata-synthesis track。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| automaton 骨架 | `$A = (Q, q_0, \mathcal P(AP), \Delta, Acc)$` | 扩展仍建立在原始 `HOA` automaton 语义之上。 |
| 新 header | `$\texttt{controllable-AP: INT*}$` | synthesis 扩展的唯一格式层增量。 |
| game transition | `$\delta : Q \times U \times C \to Q$` | controller/environment 在 automaton 上交替出招。 |
| 策略函数 | `$\sigma : (Q \cdot \mathcal P(AP))^* \cdot Q \times U \to C$` | 定义 winning strategy 的输入输出形态。 |
| parity 限制 | `$m(Inf) \equiv p \pmod 2$` | 论文首版 benchmark 的 acceptance 限制。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍直接面向 `omega` 自动机状态图。 |
| 事件 / 触发 | 中等支持 | 通过 atomic propositions valuation 组织环境和控制器的动作。 |
| 守卫 / 数据 | 弱支持 | 不提供 rich data guards，本质仍是 propositional automata alphabet。 |
| 层次 | 不支持 | 不是层次状态机格式。 |
| 并发 / 同步 | 不适用 | 核心是双人博弈，而不是并发控制建模。 |
| 时间约束 | 不支持 | 不表示 clocks。 |
| 连续动态 / 随机性 | 不支持 | 不涉及 hybrid / probabilistic semantics。 |
| 可执行 / 可验证性 | 很强 | 可直接接 `PGSolver`、`AIGER` 和 synthesis competition workflow。 |

### 形式化问题与性质

1. 本文说明 `HOA` 这类 interchange format 也能进一步承担 synthesis 输入层的角色。
2. `controllable-AP` 的设计刻意保持最小增量，方便原 `HOA` 生态尽快接入。
3. 它把“LTL 翻译器”和“game solver”之间长期缺失的标准接口补出来了。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `LTL -> deterministic omega automaton` 翻译结果；
2. 原始 `HOA` 文件；
3. synthesis 轨道中的 parity automata benchmark。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `HOA` header / body；
2. `controllable-AP` header item；
3. `hoa2pg` 转换输出；
4. `AIGER` 策略文件。

### 交换与互操作

互操作路线非常明确：

1. 复用原始 `HOA` parser 和 ecosystem。
2. 通过 `hoa2pg` 接 `PGSolver`。
3. 通过 `AIGER` 输出策略，与已有 `LTL` synthesis track 保持兼容。

## 配套基础设施

- 建模/编辑工具：原始 `HOA` 规范与已存在的 `Java/C++` parsers。
- 解析/交换/元模型支持：`HOA` 本体、`controllable-AP` 扩展、`hoa2pg`。
- 仿真/执行支持：本文不主打模型执行，重点是 realizability / synthesis。
- 验证/分析支持：parity-game / `PGSolver` / automata-based synthesis workflow。
- 代码生成/转换支持：`hoa2pg` 与 `AIGER` strategy output。
- 标准化或社区生态：`HOA` 网站、`SYNTCOMP`、`hoa-tools`。

## 适用场景与需求前提

### 适用场景

适合已经把规格翻成 deterministic `omega` automata，并希望在 automata 层直接做 realizability 或 strategy synthesis 的场景。

### 需求前提

1. 规格应自然落到 `omega` 自动机。
2. 必须明确区分 controllable 与 uncontrollable atomic propositions。
3. 后端 solver 愿意接收 automata-game 输入而不是只接 `TLSF`。
4. 最好能把 acceptance 限制在 solver 支持的 family 上，首版尤其偏向 parity。

### 不适用或高成本场景

如果团队更习惯直接在 `TLSF` / `LTL` 层工作，不关心 automata 中间件，或者 automaton 仍带大量 nondeterminism，则直接使用扩展 `HOA` 的收益会下降。

## 与相邻形式主义的关系

相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，本文是在原始 `HOA` 上加 synthesis 语义；相对 [a-high-level-ltl-synthesis-format-tlsf-v11/desc.md](../a-high-level-ltl-synthesis-format-tlsf-v11/desc.md)，`TLSF` 位于更高层的规格输入端，而本文位于 `LTL -> automata` 之后的中间交换层；相对 [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)，`Strix` 是求解器和 strategy generator，而本文提供的是 solver 之前的 automata-game 标准接口。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明标准/交换格式不只服务验证，也可以服务综合。
2. 若后续要把需求性质翻成 automata 再接 synthesis backend，这类中间层格式非常有价值。
3. 它也补强了 `HOA` 这条 `omega` 工具线在文库中的“从验证走向综合”的扩展证据。

### 作为目标形式主义还是中间表示

更像中间交换层，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. 若前端生成的是 `LTL/TLSF`，后续完全可以显式保留 automata 中间件而不是黑箱化。
2. controllable / uncontrollable 划分应尽早进入统一格式，而不是只停留在求解器私有输入里。
3. 这也提示我们 future workflow 里可把“性质自动机构造”和“博弈求解”拆成两个独立模块。

### 现实限制

它假设 automata-theoretic synthesis workflow 已经成立；对直接从高层控制 DSL 出发的工程团队，仍需要额外转换步骤。

## 重要的相关工作

1. [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：原始 `HOA` 规范本体。
2. [a-high-level-ltl-synthesis-format-tlsf-v11/desc.md](../a-high-level-ltl-synthesis-format-tlsf-v11/desc.md)：更高层的 synthesis 输入格式。
3. [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)：消费此类 automata-game 输入的现代综合器代表。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`extended HOA / synthesis automata exchange format`
- 论文角色：面向 reactive synthesis 的 `HOA` 扩展与 automata-game 输入格式
- 核心功能：在原始 `HOA` 上增加 controllable / uncontrollable 划分，使 automata 可直接承载 synthesis game。
- 关键特性：`controllable-AP`、strategy function、`hoa2pg`、`AIGER` output、parity-track compatibility。
- 构造方式：deterministic `HOA` automaton + controllable partition -> game solver / strategy output。
- 基础设施：`HOA` spec、`hoa2pg`、`PGSolver`、`AIGER`。
- 适用场景：automata-theoretic reactive synthesis 与 competition benchmark exchange。
- 需求前提：规格需已落成 deterministic `omega` automata，并显式区分 controllable / uncontrollable propositions。
- 状态：🟢 直接可用
