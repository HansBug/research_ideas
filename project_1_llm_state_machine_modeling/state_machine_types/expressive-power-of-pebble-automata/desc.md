# Pebble 自动机的表达力 / Expressive Power of Pebble Automata

## 基本信息

- 标题：Expressive Power of Pebble Automata
- 中文标题：Pebble 自动机的表达力
- 作者：Mikołaj Bojańczyk, Mathias Samuelides, Thomas Schwentick, Luc Segoufin
- 发表：*Automata, Languages and Programming (ICALP 2006)*, LNCS 4052, pp. 157-168, 2006
- DOI：`10.1007/11786986_15`
- 链接：https://doi.org/10.1007/11786986_15
- 形式主义：`Pebble Tree-Walking Automata / Strong and Weak Pebble Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：家族整理 / 表达力分层
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `n`-pebble automaton 元组、`i`-configuration、loop / simulation / behavior folding 构造，以及 strong/weak 互模拟。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是二叉树、pebble assignment、tree-walking move set 与 acceptance run semantics。

## 简报

这篇论文做了三件对演化树都很关键的事。第一，它把 tree-walking 线上“带 pebbles 的版本”整理成了可稳定命名的 family，而不再只是 scattered tricks。第二，它证明 pebble 数量形成严格层级。第三，它还把 strong pebble 看似更强的直觉直接推翻，证明 strong 与 standard 在表达力上其实等价。对当前文库来说，这正好提供了 `Tree-Walking Automata -> Pebble Tree-Walking Automata` 这一中间母节点，使后续 `Nested-Pebble` 与 `PATWA` 不再悬空。

- 形式主义定位：`Tree Automata -> Tree-Walking / Pushdown Machine` 支线上的 pebble 母型，位于 plain `TWA` 与后续 nested / alternating pebble family 之间。
- 构造方式简述：自动机在二叉树上单头行走，并按栈纪律放置 / 提起 pebbles；状态转移依赖当前节点类型、当前可见 pebbles、当前标签和动作指令。
- 基础设施与场景简述：原文纯理论，但系统给出 `PA_n` 的严格层级、与 regular tree languages 的差距，以及 strong-vs-weak 等价。

```text
二叉树 -> tree-walking head + stack pebbles -> 位置书签与局部导航 -> 表达力层级 / strong-vs-weak 比较
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是有序二叉树。与 bottom-up tree automata 不同，这里的机器始终保持“当前头位置 + 有限控制”这一 sequential walking 视角；pebbles 的作用是把某些关键节点位置临时保存在树上，以便稍后回看。

### 核心抽象

`n`-pebble automaton 被定义为：

$$
A = (Q,\Sigma,I,F,\delta)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是输入树字母表。
3. `I \subseteq Q` 是初始状态集。
4. `F \subseteq Q` 是接受状态集。
5. `\delta` 是转移关系。

源侧测试所依赖的信息来自如下形状：

$$
(q,\beta,i,S,\sigma)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `\beta` 描述当前节点类型，例如 root / 左子 / 右子 / leaf / internal。
3. `i` 是当前已经放下的 pebble 深度。
4. `S \subseteq \{1,\ldots,n\}` 记录当前节点上可见的 pebbles。
5. `\sigma \in \Sigma` 是当前节点标签。

目标侧动作为：

$$
(q',m), \qquad m \in \{\mathrm{stay},\mathrm{up},\mathrm{down}_0,\mathrm{down}_1,\mathrm{lift},\mathrm{drop}\}
$$

也就是说，自动机可以停留、上移、下到左 / 右孩子、提起 pebble 或放下新 pebble。

论文还定义了 `i`-configuration：

$$
c = (v,q,f)
$$

上式中的符号逐项解释如下：

1. `v` 是当前头所在树节点。
2. `q` 是当前状态。
3. `f` 是对 pebbles `i+1,\ldots,n` 的 assignment，也就是已经放下的较外层 pebbles 的位置。

### 一个最小例子与通俗解释

一个最直观的 pebble 用法，是“先在某个祖先节点上做书签，再进入另一片子树搜索，最后回到原书签继续运行”。例如，若想检查某个路径上的分叉节点是否还有另一棵子树满足某个标签条件，普通 `TWA` 很快就会丢失祖先位置；pebble automaton 则可以：

1. 在当前祖先节点 drop 一枚 pebble。
2. 沿左子树向下搜索。
3. lift 回到原位置，再改走右子树或向上继续。

通俗地说，这个模型像“会在树上插栈式书签的巡逻员”。它还是单头 tree-walking，但 pebbles 让它不再只能靠有限状态硬记路径上下文。

### 运行 / 接受 / 转移语义

原文把一步转移写成：

$$
c \vdash_{A,t} c'
$$

其中 `t` 是输入树，`c=(v,q,f)`、`c'=(v',q',f')` 是前后两个 configuration。与普通 `TWA` 相比，关键差别在于 `lift` 的约束：

1. 在 standard model 中，只有当前头确实位于某枚 pebble 所在节点时，才允许 lift 这枚 pebble。
2. 在 strong model 中，这个限制被拿掉。

接受 run 要求：

1. 从根节点、无 pebble、初始状态开始。
2. 最终也回到根节点。
3. 结束时树上没有残留 pebble，且状态属于 `F`。

### 语义边界

这篇论文把 pebble family 的语义边界压得很清楚：

1. 它仍然是 sequential tree machine，不是 bottom-up 并行汇总器。
2. pebbles 按栈纪律工作，否则会退化成多头自动机。
3. strong 与 standard 的区别只在 lift 限制，但表达力并不因此拉开。
4. 即使允许任意有限枚 pebbles，模型也仍严格弱于全体 regular tree languages。

### 关键性质与判定边界

原文最重要的表达力结论可直接写成：

$$
\mathrm{PA} \subsetneq \mathrm{REG}
$$

这表示 pebble tree-walking automata 仍不能识别全部 regular tree languages。

关于 pebble 数量，论文证明严格层级：

$$
\mathrm{PA}_n \subsetneq \mathrm{PA}_{n+1}, \qquad
\mathrm{DPA}_n \subsetneq \mathrm{DPA}_{n+1}
$$

也就是说，每增加一枚 pebble，family 的表达力都会真正提升。

对 plain tree-walking family 的比较，论文还给出：

$$
\mathrm{TWA} \not\subseteq \mathrm{DPA}_n
$$

这说明 deterministic pebble family 与 nondeterministic plain `TWA` 也不是简单包含关系。

最后，最适合挂到演化树上的结论是 strong-vs-weak 等价：

$$
\mathrm{sPA}_n = \mathrm{PA}_n, \qquad
\mathrm{sDPA}_n = \mathrm{DPA}_n
$$

这意味着我们在树上建 family 时，没有必要再为“强 pebble”单独开一条并列大枝；它更适合作为同一母型内部的语义变体说明。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制是主骨架。 |
| 事件 / 触发 | 不适用 | 输入是静态树。 |
| 守卫 / 数据 | 部分支持 | 依赖节点类型、标签和可见 pebble 集。 |
| 层次 | 强支持 | 对象天然是树。 |
| 并发 / 同步 | 不支持 | 单头 sequential walking。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | family hierarchy、simulation 和 strong/weak 等价都很清楚。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,\Sigma,I,F,\delta)$` | pebble tree-walking automaton 的标准骨架。 |
| 配置 | `$c=(v,q,f)$` | 当前节点、状态和外层 pebbles assignment。 |
| regular gap | `$\mathrm{PA}\subsetneq\mathrm{REG}$` | pebble family 仍识别不了所有 regular tree languages。 |
| pebble hierarchy | `$\mathrm{PA}_n\subsetneq\mathrm{PA}_{n+1}$` | pebble 数量形成严格层级。 |
| strong/weak equivalence | `$\mathrm{sPA}_n=\mathrm{PA}_n$` | strong pebbles 不产生额外表达力。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求是否真是 sequential tree navigation，而不是 bottom-up 合并。
2. 再确定需要几枚 pebbles 才能把关键节点位置“压栈”保存下来。
3. 若只需局部导航，plain `TWA` 足够；若需要回到祖先或切换子树时保留位置，就升级到 pebble family。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 输入二叉树；
2. 状态集与 move set；
3. pebble assignment；
4. configuration 语义；
5. behavior folding / simulation 构造。

原文没有 XML、JSON、DSL 或工程文件格式。

### 交换与互操作

它与 plain `TWA` 的关系最直接，同时也是后续 nested-pebble / alternating pebble work 的母线。对当前文库而言，它最重要的作用是为 `Nested-Pebble Tree-Walking Automata` 提供清晰父节点。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 pebble assignment、simulation、behavior equivalence 与 crossing-style arguments。
- 仿真/执行支持：可按 tree-walking + pebble operations 直接解释。
- 验证/分析支持：hierarchy proof、regular-gap proof、strong-vs-weak simulation 是主线。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 tree-walking / descriptive complexity / XML tree processing 理论里的经典中间节点。

## 适用场景与需求前提

### 适用场景

适合以下理论任务：

1. 树结构上的顺序导航与局部回看。
2. 需要有限控制加少量位置书签，而不是完整 bottom-up regular tree machinery。
3. 想在演化树中明确区分 plain `TWA`、pebble `TWA`、nested-pebble `TWA` 与 alternating pebble `TWA`。

### 需求前提

1. 对象必须天然是树。
2. 需求主要依赖路径导航与关键位置暂存。
3. pebble 数量最好能压成很小的常数，否则模型与证明都会变重。

### 不适用或高成本场景

若需求需要全部 regular tree language 的识别能力，bottom-up tree automata 更合适；若需要数据值、时间、概率或输出变换，这个 family 也不是终点。

## 与相邻形式主义的关系

相对 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)，它把 plain `TWA` 推进到了带栈式位置书签的 pebble family；相对 [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md)，这里还没有 multi-head 与 abstract nested pebble machinery；相对 [pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md](../pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md)，这里也还没有 alternation。

## 与本研究的关系

### 对 Project 1 的价值

它能把当前演化树里 `Tree-Walking Automata` 与 `Nested-Pebble / PATWA` 之间缺失的母节点正式补出来，使 pebble-walking family 的演化顺序更自然。

### 作为目标形式主义还是中间表示

更适合作为谱系节点和理论中间表示，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

如果需求文本在描述“沿树顺序走动，并临时记住某几个关键节点再回来”的逻辑，LLM 应先想到 pebble tree-walking family，而不是直接跳到更强或更重的树自动机。

### 现实限制

原文没有工程生态，而且 `PA` 仍弱于全部 regular tree languages；其价值主要在于演化树和表达力边界。

## 重要的相关工作

### 奠基或前身工作

- [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)

### 同类型或同家族工作

- [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md)
- [pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md](../pebble-alternating-tree-walking-automata-and-their-recognizing-power/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合在主蓝本树中作为 `Tree-Walking Automata` 之下 `Pebble Tree-Walking Automata / Strong and Weak Pebble Automata` 的代表节点，并把 `Nested-Pebble` 重新挂到其下。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Pebble Tree-Walking Automata / Strong and Weak Pebble Automata`
- 论文角色：家族整理 / 表达力分层
- 核心功能：把 tree-walking pebble family 立成稳定母型，并给出严格 pebble 层级与 strong/weak 等价。
- 关键特性：stack-discipline pebbles、tree navigation、regular-gap、hierarchy、strong-vs-weak equivalence。
- 构造方式：`(Q,\Sigma,I,F,\delta)` 元组加 `i`-configuration `(v,q,f)` 与 `drop/lift/up/down` 动作。
- 基础设施：纯理论模型，无工程标准或工具；核心在于 simulation、behavior folding 与层级证明。
- 适用场景：tree query / navigation 理论、tree-walking 谱系建设、位置书签式树分析。
- 需求前提：对象是树，需求依赖顺序导航和少量节点位置保存，而不是全 regular tree recognition。
- 状态：🟢
