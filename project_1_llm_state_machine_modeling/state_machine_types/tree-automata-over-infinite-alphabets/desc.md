# 无限字母表上的树自动机 / Tree Automata over Infinite Alphabets

## 基本信息

- 标题：Tree Automata over Infinite Alphabets
- 中文标题：无限字母表上的树自动机
- 作者：Michael Kaminski, Tony Tan
- 发表：*Pillars of Computer Science*, LNCS 4800, pp. 386-423, 2008
- DOI：`10.1007/978-3-540-78127-1_21`
- 链接：https://doi.org/10.1007/978-3-540-78127-1_21
- 形式主义：`Tree Finite-Memory Automata over Infinite Alphabets (↓-FMA / ↑-FMA / ↓-NR-FMA / ↑-NR-FMA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 家族分层
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 top-down / bottom-up 的 tree-FMA 元组、assignment merge 规则、frontier 映射与 quasi-context-free grammar 对应。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 binary `\Sigma`-tree、register assignment、deterministic / nondeterministic reassignment 与 run semantics。

## 简报

这篇论文把 `Finite-Memory Automata` 从线性词真正推进到了树对象上，而且不是只给一个含糊的“树版 FMA”，而是把 top-down / bottom-up、deterministic / nondeterministic reassignment 四个变体全部拆开比较。结果也很有辨识度：deterministic reassignment 的上下行版本都偏弱且互不等价，而允许 nondeterministic reassignment 后，top-down 与 bottom-up 又重新汇合成同一表达力，并保持 membership / emptiness 可判定。

- 形式主义定位：`Tree Automata -> Data / Infinite-Alphabet Tree` 主枝上的早期母型，位于后续 `BUDA / ODTA` 等更专门 data-tree family 之前。
- 构造方式简述：每个节点仍只有有限控制状态，但额外挂一组保存无限字母表值的寄存器；top-down 版本把 assignment 从父节点传给子节点，bottom-up 版本则要把两个孩子的 assignments 合并到父节点。
- 基础设施与场景简述：原文纯理论，但把 quasi-context-free frontier 关系、membership / emptiness / universality 边界和四类模型的相互比较都整理齐全了。

```text
无限字母表树 -> 有限控制 + 有界寄存器 -> top-down 传播 / bottom-up 合并 -> tree language / frontier language
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是二叉 `\Sigma`-tree。每个节点携带一个来自无限字母表 `\Sigma` 的符号；自动机真正能观察到的仍然只是“当前节点标签是否已经出现在某个寄存器中”，而不是其数值结构。

### 核心抽象

top-down deterministic reassignment 版本 `↓-FMA` 定义为：

$$
A = \langle S, s_0, u, \rho, \mu, F \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集。
2. `s_0 \in S` 是初始状态。
3. `u \in \Sigma^r_{\neq}` 是初始寄存器 assignment。
4. `\rho : S \to \{1,\ldots,r\}` 是 deterministic reassignment function，表示当当前标签未命中任何寄存器时要覆写哪一个寄存器。
5. `\mu \subseteq S \times \{1,\ldots,r\} \times S^2` 是转移关系，`(p,i)\to(p_0,p_1)` 表示在状态 `p` 且当前节点标签等于第 `i` 个寄存器内容时，左孩子进入 `p_0`、右孩子进入 `p_1`。
6. `F \subseteq S \times \{1,\ldots,r\}` 是终结关系。

其 configuration 是状态加寄存器内容：

$$
(p,w) \in S_c = S \times \Sigma^r_{\neq}
$$

若当前节点标签为 `\sigma`，则诱导转移可写成：

$$
(p,w),\sigma \to (p_0,w_0),(p_1,w_1)
$$

其中：

1. 若 `\sigma = w_i \in [w]`，则 `w_0 = w_1 = w`，并使用 `(p,i)\to(p_0,p_1)`。
2. 若 `\sigma \notin [w]`，则把寄存器 `\rho(p)` 在两个子节点 assignment 中都改写成 `\sigma`。

bottom-up deterministic 版本 `↑-FMA` 在此基础上多出合并关系 `\tau`：

$$
A = \langle S, s_0, u, \rho, \tau, \mu, F \rangle
$$

这里 `\tau` 的作用，是依据两个子树 assignments 的 type 与 selector，把孩子端的 `2r` 个候选值合成父节点端的 `r` 个寄存器值。

nondeterministic reassignment 版本把 `\rho` 从单个寄存器编号提升成寄存器子集：

$$
\rho : S \to 2^{\{1,\ldots,r\}}
$$

这表示在状态 `p` 时，自动机可同时重置若干个寄存器，并把它们装入任意一组两两不同的新符号。

### 一个最小例子与通俗解释

原文给了两个非常好的对照例子。

top-down 例子是语言

$$
L_{\varepsilon} = \{ \sigma:T\to\Sigma \mid \forall n\in T\setminus\{\varepsilon\},\ \sigma(n)\neq \sigma(\varepsilon) \}
$$

也就是“除根节点外，所有节点标签都与根不同”。`↓-FMA` 很容易接受它：在根节点把根标签写进寄存器，然后沿整棵树向下传播并持续检查子节点都不等于该寄存器内容。

与之相对，bottom-up 例子 `L_2` 表示“存在两个不同叶子带相同标签”。这个性质 `↑-FMA` 可以通过自底向上汇合两片子树信息来识别，但 `↓-FMA` 做不到。

通俗地说，tree-FMA 就像“树上的有限状态检查员 + 少量名字便签”。top-down 版本擅长把祖先看到的值往下传，bottom-up 版本擅长把不同子树中的值往上汇总。

### 运行 / 接受 / 转移语义

对 top-down 版本，一个 run 是映射

$$
R : T \to S_c
$$

满足：

$$
R(\varepsilon) = (s_0,u)
$$

并且对每个非叶节点 `n`，

$$
(R(n),\sigma(n)) \to (R(n0),R(n1)) \in \mu_c
$$

若每个叶节点 `n` 都满足

$$
(R(n),\sigma(n)) \in F_c
$$

则该 run 接受输入树。

对 bottom-up 版本，run 同样是 `R:T\to S_c`，但方向相反：

1. 每个叶子先从相同的初始 configuration `(s_0,u)` 开始。
2. 每个内部节点根据两个孩子的 configurations、当前孩子标签和 merge 规则 `\tau` 计算自己的 configuration。
3. 根节点若满足终结关系 `F_c` 则接受。

### 语义边界

这篇论文的家族边界非常清楚：

1. deterministic reassignment 的 top-down / bottom-up 版本都偏弱，而且各自擅长的性质不同。
2. 允许 nondeterministic reassignment 后，tree-FMA 才真正变成“树上 infinite alphabet regularity”的稳定候选。
3. 模型仍然只处理 equality-style memory，不处理 datum order、算术或复杂逻辑约束。

### 关键性质与判定边界

原文最核心的等价结论是：

$$
L(\downarrow\text{-}\mathrm{NR\text{-}FMA}) = L(\uparrow\text{-}\mathrm{NR\text{-}FMA})
$$

这表示只要允许 nondeterministic reassignment，top-down 与 bottom-up 在表达力上重新汇合。

判定性方面，论文给出：

$$
\mathrm{membership}(\downarrow\text{-}\mathrm{NR\text{-}FMA}) \text{ decidable}
$$

$$
\mathrm{emptiness}(\downarrow\text{-}\mathrm{NR\text{-}FMA}) \text{ decidable}
$$

同时：

$$
\mathrm{universality}(\downarrow\text{-}\mathrm{FMA}) \text{ undecidable}, \qquad
\mathrm{universality}(\uparrow\text{-}\mathrm{FMA}) \text{ undecidable}
$$

原文还把 frontier language 同 quasi-context-free language 对齐：

$$
\mathcal L_{\mathrm{frontier}}(\text{tree-FMA}) = \text{quasi-context-free languages}
$$

更精确地说，任一被 top-down 或 bottom-up tree-FMA 接受的树语言，其所有 frontier 组成的词语言都是 quasi-context-free；反过来，每个 quasi-context-free language 都能由某个相应 tree-FMA 的 frontier 获得。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍然保持有限控制骨架。 |
| 事件 / 触发 | 不适用 | 输入是静态树而不是事件流。 |
| 守卫 / 数据 | 强支持 | 通过有限寄存器对无限字母表做 equality-style 记忆。 |
| 层次 | 强支持 | 对象天然是树。 |
| 并发 / 同步 | 不支持 | 不是并发模型，但 bottom-up 版本会汇合子树信息。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | membership / emptiness 与 family-comparison 结论明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| top-down 模型 | `$A=\langle S,s_0,u,\rho,\mu,F\rangle$` | `↓-FMA` 的标准元组。 |
| bottom-up 模型 | `$A=\langle S,s_0,u,\rho,\tau,\mu,F\rangle$` | `↑-FMA` 在此基础上加入 merge relation。 |
| configuration | `$(p,w)$` | 状态和寄存器 assignment 的组合。 |
| 家族等价 | `$L(\downarrow\text{-}\mathrm{NR\text{-}FMA})=L(\uparrow\text{-}\mathrm{NR\text{-}FMA})$` | nondeterministic reassignment 下的 top-down / bottom-up 汇合。 |
| frontier 对应 | `$\mathcal L_{\mathrm{frontier}}=\text{quasi-context-free}$` | 树语言与无限字母表上下文无关词语言之间的桥梁。 |

## 构造方式与承载格式

### 建模入口

1. 先判断目标到底是祖先到后代传播，还是子树到父节点汇合。
2. 若性质更像“根或祖先的名字向下约束子树”，优先用 `↓-FMA` 视角。
3. 若性质更像“两片子树的信息要在父节点处合并判断”，优先用 `↑-FMA` 视角。
4. 若 deterministic reassignment 不够，再升级到 `NR-FMA`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. binary `\Sigma`-tree；
2. `r` 个寄存器的 assignment；
3. top-down / bottom-up 的 transition relation；
4. bottom-up 的 type / selector / merge relation；
5. frontier 映射与 quasi-context-free grammar 对应。

原文没有 XML schema、JSON 或其他工程交换格式。

### 交换与互操作

它与 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md) 的关系最直接，因为本质上就是 tree lift of word-FMA；与 [bottom-up-automata-on-data-trees/desc.md](../bottom-up-automata-on-data-trees/desc.md) 和 [an-automata-model-for-trees-with-ordered-data-values/desc.md](../an-automata-model-for-trees-with-ordered-data-values/desc.md) 的关系，则是“更早、更一般，但也更粗粒度”的 tree-side infinite-alphabet 母线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 assignments、merge relation、frontier 映射与 grammar correspondence。
- 仿真/执行支持：可按 top-down 或 bottom-up run semantics 直接解释。
- 验证/分析支持：membership、emptiness、universality 和 quasi-context-free correspondence 是主线。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 data-tree automata 之前的一条重要早期理论母线。

## 适用场景与需求前提

### 适用场景

适合以下对象与任务：

1. 节点标签来自无限域的树语言。
2. XML / 文档 / 层次结构上只依赖 equality memory 的约束。
3. 需要区分“自顶向下传播”与“自底向上合并”的 family 分化。

### 需求前提

1. 对象必须天然是树。
2. 需求中的无限域操作主要是 equality 和记忆，而非 order 或算术。
3. 若要稳定的正结果，往往需要 `NR-FMA` 而不是 deterministic reassignment 版本。

### 不适用或高成本场景

若需求需要 datum order、复杂 XPath 风格 path tests、并行线程或时间信息，后续 `BUDA / ODTA`、tree-walking、timed family 会更合适；若对象只是线性词，退回 word-side `FMA / RA` 更自然。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，它把 infinite-alphabet memory 从词提升到树；相对 [bottom-up-automata-on-data-trees/desc.md](../bottom-up-automata-on-data-trees/desc.md)，这里还没有 alternating thread、single-register descendant test 等更专门的 data-tree machinery；相对 [an-automata-model-for-trees-with-ordered-data-values/desc.md](../an-automata-model-for-trees-with-ordered-data-values/desc.md)，它只处理 equality memory，不处理数据值顺序；相对 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)，它不是 sequential walking machine，而是寄存器驱动的 tree acceptor family。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里 `Tree Automata` 侧的 `Data / Infinite-Alphabet Tree` 母线真正补出来，使后续 `BUDA / ODTA` 不再悬空。

### 作为目标形式主义还是中间表示

更适合作为谱系母节点和树侧理论中间表示，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

如果需求文本本身在描述“树状对象 + 少量名字记忆 + 祖先传播 / 子树合并”，LLM 不应直接跳到更复杂的 XPath 或 data-tree logic，而可以先判断 tree-FMA 级别是否已足够。

### 现实限制

原文没有工程生态，deterministic reassignment 版本也明显偏弱，因此它在本研究中的价值主要是演化树骨架和理论边界。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [bottom-up-automata-on-data-trees/desc.md](../bottom-up-automata-on-data-trees/desc.md)
- [an-automata-model-for-trees-with-ordered-data-values/desc.md](../an-automata-model-for-trees-with-ordered-data-values/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合在主蓝本树中作为 `Tree Automata -> Data / Infinite-Alphabet Tree` 的早期母节点，并把 `BUDA / ODTA` 重新挂到其下。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Tree Finite-Memory Automata over Infinite Alphabets (↓-FMA / ↑-FMA / ↓-NR-FMA / ↑-NR-FMA)`
- 论文角色：模型提出 / 家族分层
- 核心功能：把有限寄存器的 infinite-alphabet 自动机推广到树，并系统比较 top-down / bottom-up、deterministic / nondeterministic reassignment 四种变体。
- 关键特性：tree-valued input、assignment propagation / merge、family comparison、membership / emptiness decidability、frontier-quasi-CFL correspondence。
- 构造方式：top-down 的 `\langle S,s_0,u,\rho,\mu,F\rangle` 与 bottom-up 的 `\langle S,s_0,u,\rho,\tau,\mu,F\rangle` 元组加 run semantics。
- 基础设施：纯理论模型，无工程标准或工具；核心在于 assignment、merge rule 与 grammar correspondence。
- 适用场景：infinite-alphabet tree languages、树文档 equality-memory 理论、树侧 data-family 谱系建设。
- 需求前提：对象必须是树，数据关系主要是 equality，且需求能用少量寄存器的传播或合并表达。
- 状态：🟢
