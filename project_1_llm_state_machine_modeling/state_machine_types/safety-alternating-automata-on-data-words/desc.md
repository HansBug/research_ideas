# 数据词上的安全交替自动机 / Safety Alternating Automata on Data Words

## 基本信息

- 标题：Safety Alternating Automata on Data Words
- 中文标题：数据词上的安全交替自动机
- 作者：Ranko Lazić
- 发表：*ACM Transactions on Computational Logic*, 12(2):1-24, 2011
- DOI：`10.1145/1877714.1877716`
- 链接：https://doi.org/10.1145/1877714.1877716
- 形式主义：`Safety Alternating One-Register Automata / Safety 1ARA1`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 安全接受变体
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `A=(\Sigma,Q,q_I,\delta)`、configuration `\langle q,D\rangle`、run sequence `F_0 \to F_1 \to \cdots` 与到 safety `IPCANT` 的化简。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data `\omega`-word、正布尔转移公式 `B^+_\downarrow(Q)` 与 safety 接受语义。

## 简报

这篇论文把“带一个寄存器的交替 register automata”正式推进到 data `\omega`-words 的 safety 语义上。它的关键收获不是再给 data word 加一点逻辑花样，而是把一个真正能挂到演化树上的模型家族稳定命名出来：`Safety 1ARA1`。这个模型只记一个数据值，但允许交替分支，并且把接受机制限制成 safety，从而换回可判定的空性和包含性。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上的 `\omega`-word / safety 分支，可视为一寄存器交替 data automata 的安全接受子类。
- 构造方式简述：每个线程由一个有限状态和一个寄存器类值组成；迁移依据当前字母和“当前 datum 是否等于寄存器 datum”来选择一组保留旧 datum 或覆盖为当前 datum 的后继线程。
- 基础设施与场景简述：原文纯理论，但给出从 safety `LTL↓_1(X,R)` 到 `Safety 1ARA1` 的对数空间翻译，并以带错误增长的计数器自动机建立判定边界。

```text
data ω-word -> one-register alternating threads -> safety run semantics -> counter-automata reduction / safety-LTL bridge
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 data `\omega`-words。每个位置都带一个有限字母 `\sigma(i)\in\Sigma`，并通过等价关系 `\sim` 指示哪些位置拥有相同数据值。模型只允许比较“当前位置的数据类”与“寄存器里记住的数据类”是否相等，不做算术或次序比较。

### 核心抽象

原文把 `Safety 1ARA1` 定义为：

$$
A=(\Sigma,Q,q_I,\delta)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是有限输入字母表。
2. `Q` 是有限状态集。
3. `q_I\in Q` 是初始状态。
4. `\delta:(Q\times\Sigma\times\{\uparrow,\not\uparrow\})\to B^+_\downarrow(Q)` 是转移函数。

其中 `B^+_\downarrow(Q)` 是关于 `Q\cup\downarrow Q` 的正布尔公式集合。这里：

$$
\varphi ::= q \mid \downarrow q \mid \top \mid \bot \mid \varphi\land\varphi \mid \varphi\lor\varphi
$$

上式中的符号逐项解释如下：

1. `q` 表示后继线程保留旧寄存器值并进入状态 `q`。
2. `\downarrow q` 表示后继线程把寄存器改写为当前数据类并进入状态 `q`。
3. `\uparrow` 表示当前位置的数据类等于寄存器中的数据类。
4. `\not\uparrow` 表示两者不相等。

### 一个最小例子与通俗解释

一个直观例子是“同一个会话 ID 一旦出现 `close`，以后不能再出现 `write`”。`Safety 1ARA1` 的做法是：

1. 在读到某个 `(close,d)` 时，把当前 datum `d` 冻结进寄存器。
2. 后续沿时间向右推进。
3. 只要再遇到 `write` 且当前 datum 与寄存器 datum 相等，就进入拒绝情况。

通俗地说，它像“每个线程手里只拿一张数据值便签的交替自动机”。普通有限自动机只能记有限状态；这里每条线程还可以记住一个“刚才关注的 ID”，然后在未来检查这个 ID 是否再次触发坏事。

### 运行 / 接受 / 转移语义

对一个 data `\omega`-word `\sigma`，configuration 可写成：

$$
\langle q,D\rangle \in Q\times (\mathbb N/{\sim})
$$

其中 `q` 是当前状态，`D` 是寄存器中保存的数据类。

若在位置 `i` 的线程集合为 `F`，则一步转移满足：

$$
F \xrightarrow{\sigma,i} F'
$$

当且仅当对每个 `\langle q,D\rangle\in F`，都能找到满足 `\delta(q,\sigma(i),\uparrow)` 或 `\delta(q,\sigma(i),\not\uparrow)` 的一对状态集 `Q',Q'_\downarrow`，并令：

$$
F'=\{\langle q',D\rangle:q'\in Q'\}\ \cup\ \{\langle q',[i]_\sim\rangle:q'\in Q'_\downarrow\}
$$

上式中的符号逐项解释如下：

1. `Q'` 产生“保留旧寄存器值”的后继线程。
2. `Q'_\downarrow` 产生“把寄存器覆写为当前数据类”的后继线程。
3. `[i]_\sim` 是当前位置 `i` 的数据等价类。

初始线程集合为：

$$
F_0=\{\langle q_I,[0]_\sim\rangle\}
$$

只要存在无限 run

$$
F_0 \xrightarrow{\sigma,0} F_1 \xrightarrow{\sigma,1} F_2 \xrightarrow{\sigma,2} \cdots
$$

就认为 `A` 接受 `\sigma`。这里没有额外的 Büchi / parity 条件；安全性来自“run 中永远不能出现无法继续的 rejecting configuration”。

### 语义边界

这个模型比普通 `RA` 更强，因为它允许交替分支；但它也比一般的 weak/Büchi 接受型 data automata 更克制，因为它只保留 safety 语义。它的表达重点是“坏前缀永远不应出现”的 data `\omega`-property，而不是一般的长期重复接受。

### 关键性质与判定边界

原文最关键的结论可压成：

$$
\mathrm{emptiness}(\mathrm{Safety}\text{-}1ARA1)\ \text{is ExpSpace-complete}
$$

$$
\mathrm{Safety}\text{-}LTL^\downarrow_1(X,R)\ \leq_{\log}\ \mathrm{Safety}\text{-}1ARA1
$$

$$
L(A)\ \text{is safety}
$$

$$
\mathrm{inclusion}(\mathrm{Safety}\text{-}1ARA1)\ \text{decidable}
$$

同时，原文也强调：

$$
\text{dropping safety, adding past, or adding one more register causes undecidability}
$$

上面几式中的符号逐项解释如下：

1. `\leq_{\log}` 表示对数空间可翻译。
2. `L(A)` 是自动机识别的 data `\omega`-language。
3. 最后一条说明这条可判定边界非常紧。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是有限状态骨架。 |
| 事件 / 触发 | 强支持 | 沿 data `\omega`-word 单向推进。 |
| 守卫 / 数据 | 强支持 | 一寄存器数据类比较是核心。 |
| 层次 | 不支持 | 仅处理线性 data `\omega`-word。 |
| 并发 / 同步 | 强支持 | 交替语义通过线程集合表达并行义务。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 空性和包含性可判定，并与 safety `LTL↓_1` 对齐。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(\Sigma,Q,q_I,\delta)$` | `Safety 1ARA1` 的标准骨架。 |
| 线程配置 | `$\langle q,D\rangle$` | 每条线程保存一个状态和一个数据类。 |
| 转移公式 | `$\delta:(Q\times\Sigma\times\{\uparrow,\not\uparrow\})\to B^+_\downarrow(Q)$` | 用正布尔公式同时表达 existential / universal 分支。 |
| safety 接受 | `$F_0\to F_1\to\cdots$` | 只要存在无限 run 且中途不死掉即可接受。 |
| 复杂度 | `$\mathrm{emptiness}$ ExpSpace-complete` | safety 约束换回可判定空性。 |

## 构造方式与承载格式

### 建模入口

1. 先确认需求是 data `\omega`-word 上的 safety property，而不是一般 liveness。
2. 再明确哪些事件需要把当前 datum 冻结进寄存器。
3. 根据后续是否要保留旧 datum 或覆盖当前 datum，写出 `q / \downarrow q` 风格的正布尔转移公式。

### 机器可处理承载方式

机器可处理承载方式就是：

1. data `\omega`-word；
2. `A=(\Sigma,Q,q_I,\delta)`；
3. 线程集合 `F_i`；
4. 到 safety `IPCANT` 的计数器自动机化简。

原文没有 XML、JSON 或 DSL 层级的交换格式。

### 交换与互操作

它和 safety `LTL↓_1(X,R)` 的互操作最直接；与普通 register automata 的关系，则体现在“多了 alternation、但只保留 safety acceptance”。其判定证明又依赖到带增量错误的 powerset counter automata。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是正布尔转移公式、数据等价类和 configuration-set 语义。
- 仿真/执行支持：可按线程集合逐位置推进解释。
- 验证/分析支持：到 safety `IPCANT` 的化简、`LTL↓_1` 翻译、包含性判定。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 data-word / register-logic / safety-automata 交叉地带的经典理论节点。

## 适用场景与需求前提

### 适用场景

适合“同一数据值在未来永远不能触发某种坏模式”这类 safety requirement，例如 session ID、resource ID、channel ID 的长期禁止约束。

### 需求前提

1. 输入对象应能压成 data `\omega`-word。
2. 关键数据关系主要是 datum equality。
3. 性质应更接近 bad-prefix / safety，而非一般 liveness。

### 不适用或高成本场景

若需求需要多寄存器、past navigation、一般 Büchi / parity 接受或算术比较，这个家族就不够，必须转向更强但更贵的模型。

## 与相邻形式主义的关系

相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它处理的是 infinite data words 上的 safety 接受，而不是 finite words/trees 上的 `guess/spread` 扩展；相对 [extending-buchi-automata-with-constraints-on-data-values/desc.md](../extending-buchi-automata-with-constraints-on-data-values/desc.md)，它的核心不是给 Büchi skeleton 加全局约束，而是把一寄存器交替线程推进到 safety 语义。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Data / Infinite-Alphabet` 主枝继续长到了 `\omega`-word / safety 一侧，使数据自动机家族不再只停在 finite-word 模型上。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示或谱系节点，而不是控制系统最终交付建模语言。

### 对需求到模型生成的启发

当需求文本里出现“某个 ID 一旦进入某类坏状态，未来永远不能再触发某事件”时，LLM 应优先识别出这是 safety-data-word 需求，而不是误落到普通 `FSM` 或无界时序逻辑。

### 现实限制

它没有工程标准、运行时或编辑器；价值主要在定义、判定边界和演化树定位。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)
- [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)

### 同类型或同家族工作

- [extending-buchi-automata-with-constraints-on-data-values/desc.md](../extending-buchi-automata-with-constraints-on-data-values/desc.md)
- [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md)
- [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合补到 `Finite Automata -> Data / Infinite-Alphabet` 主枝向 `\omega`-word / safety family 生长出来的那条经典分叉。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Safety Alternating One-Register Automata / Safety 1ARA1`
- 论文角色：模型提出 / 安全接受变体
- 核心功能：在 infinite data words 上用一寄存器交替线程表达 safety property，并保住可判定空性与包含性。
- 关键特性：一寄存器、alternation、safety acceptance、`LTL↓_1(X,R)` 对应、counter-automata reduction。
- 构造方式：`A=(\Sigma,Q,q_I,\delta)` + 正布尔转移公式 + thread-set run semantics。
- 基础设施：纯理论模型，无工程标准/工具；核心分析设施是 safety `IPCANT` 化简。
- 适用场景：per-ID safety 约束、data `\omega`-word 长期坏模式禁止。
- 需求前提：输入可压成 data `\omega`-word，且关键关系主要是 datum equality 与 safety semantics。
- 状态：🟢
