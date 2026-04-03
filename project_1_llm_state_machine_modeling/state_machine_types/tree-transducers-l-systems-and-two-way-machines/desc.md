# 树变换器、L 系统与双向机器 / Tree transducers, L systems, and two-way machines

## 基本信息

- 标题：Tree transducers, L systems, and two-way machines
- 中文标题：树变换器、L 系统与双向机器
- 作者：Joost Engelfriet, Grzegorz Rozenberg, Giora Slutzki
- 发表：Journal of Computer and System Sciences, 20(2):150-202, 1980
- DOI：`10.1016/0022-0000(80)90058-6`
- 链接：https://ris.utwente.nl/ws/files/6563661/Engelfriet80tree.pdf
- 形式主义：Checking Tree Pushdown Transducers / Tree-Walking Machine Line
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文给出 `ct-pd`、`ct`、`cs-pd`、`cs` 等机器模型及其限制形式；无独立实现。
- 标准/格式获取方式：原文没有工程化标准，机器可处理入口是输入树、pushdown alphabet、输出 alphabet 与 move relation。

## 简报

这篇论文的价值在于，它把树变换主线从“平行重写系统”接到了“行走式双向机器”一侧。文中提出的 `checking tree-pushdown transducer (ct-pd)` 直接给出了一个能在树上上下游走、同时读写栈和输出串的机器模型；把栈拿掉就是 `tree-walking automaton`，再把输入限制成 monadic tree，就退化到经典 `two-way gsm`。

- 形式主义定位：树对象上的双向行走式有限控制机器，是 tree transducer 理论和 two-way machine 理论之间的桥节点。
- 构造方式简述：机器带有限状态、输入树指针、pushdown 栈顶指针和输出带尾指针，基本动作只有 `up / stay / down` 三类。
- 基础设施与场景简述：原文是纯理论模型，但它明确建立了 `top-down tree transducer` 与 `ct-pd` 之间的等价，并把 `tree-walking automaton`、`two-way gsm` 都放进同一支线。

```text
输入树 + 栈 + 有限控制 -> up / stay / down -> 输出串
                    \-> 去掉栈 -> tree-walking automaton
                    \-> 单链输入 -> two-way gsm
```

## 形式主义定义与核心对象

### 定义对象

`ct-pd transducer` 不是在树上“平行展开”的规则系统，而是在树上带栈行走的机器。它一边上下穿越树边，一边把路径信息同步压入或弹出栈，并在此过程中产生输出字符串。

### 核心抽象

原文把 checking tree-pushdown transducer 定义为：

$$
M = (Q, \Sigma, \Gamma, \Delta, \delta, q_0, F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是 ranked input alphabet，即输入树标签。
3. `\Gamma` 是 pushdown alphabet。
4. `\Delta` 是输出 alphabet。
5. `\delta` 是 move relation。
6. `q_0` 是初始状态。
7. `F` 是终止状态集。

原文给出的转移动作集合为：

$$
D = \{\mathrm{up}\} \cup \{\mathrm{stay}(\gamma) \mid \gamma \in \Gamma\} \cup \{\mathrm{down}(i,\gamma) \mid i \ge 1, \gamma \in \Gamma\}
$$

并且转移关系满足：

$$
\delta : Q \times \Sigma \times \Gamma \to \mathcal{P}(Q \times D \times \Delta^*)
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{up}` 表示从当前节点回到父节点，同时弹栈。
2. `\mathrm{stay}(\gamma)` 表示留在当前节点，只改写栈顶。
3. `\mathrm{down}(i,\gamma)` 表示走到第 `i` 个孩子，同时压入新栈符号。
4. `\mathcal{P}` 表示幂集，因为原模型允许 nondeterminism。
5. `\Delta^*` 是一次转移可以输出的字符串片段。

### 一个最小例子与通俗解释

一个最小例子是：机器从根节点出发，读到某个二叉节点 `\sigma` 时，如果当前栈顶是 `\gamma`，就执行 `down(1,\gamma')` 去左孩子并输出前缀；左子树完成后执行 `up` 回父节点，再决定是否去右孩子。整台机器始终只沿着一条路径在树里走，但会用栈记住“我现在处在树的哪一层、回去后还要做什么”。

通俗地说，它像一个“在树里巡逻的有限状态翻译器”。普通 top-down tree transducer 更像递归规则展开器，而 `ct-pd` 更像会爬树、会背包、会边走边写的机器。

### 运行 / 接受 / 转移语义

原文把一个配置写成：

$$
(q,\$(t),d,\#\gamma,w)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `\$(t)` 是在原树外包一个哨兵根后的输入树。
3. `d` 是当前输入指针所在节点。
4. `\#\gamma` 表示当前 pushdown 内容，`#` 是底标记。
5. `w` 是已经产生的输出串。

成功翻译关系可写成：

$$
M = \{(t,w) \mid (q_0,\$(t),d_0,\#\gamma,\lambda) \vdash^* (q,\$(t),d_\$, \lambda, w),\ q \in F\}
$$

上式中的符号逐项解释如下：

1. `d_0` 是原输入树根。
2. `d_\$` 是外层哨兵根。
3. `\lambda` 是空串或空栈内容。
4. `\vdash^*` 是配置之间的多步 move relation。

### 语义边界

相对 top-down tree transducer，`ct-pd` 把“递归展开”换成了“路径行走 + 栈同步”；相对 tree-walking automaton，它多了真正的 pushdown 和记输出能力；相对 two-way gsm，它把线性输入推广成树输入。

### 关键性质与判定边界

原文最关键的结构结论之一是：`ct-pd` 与 top-down tree transducer 在生成能力上等价，并且有限 crossing / finite pass 正好对应树变换器的 copying-bound 限制。可保守写成：

$$
\mathrm{CT\text{-}PD}(\mathrm{REC}) = yT(\mathrm{REC})
$$

以及限制版本上的对应：

$$
\mathrm{CT\text{-}PD}_{fc(k)}(\mathrm{REC}) \leftrightarrow yT_{(k)}(\mathrm{REC})
$$

上式中的符号逐项解释如下：

1. `\mathrm{CT\text{-}PD}` 表示 checking tree-pushdown transducer 类。
2. `yT` 表示 top-down tree transducer 生成的输出语言类。
3. `fc(k)` 表示每条树边最多被来回穿越 `2k` 次的 `k`-crossing 约束。
4. `T_{(k)}` 表示对应的 copying-bound `k` 限制。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制整个行走过程。 |
| 事件 / 触发 | 不适用 | 不是事件驱动，而是按树节点和栈顶触发。 |
| 守卫 / 数据 | 部分支持 | 通过节点标签和栈顶符号做有限条件分支。 |
| 层次 | 强支持 | 输入对象天然是树。 |
| 并发 / 同步 | 不支持 | 单机单路径行走，不是并发模型。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | 配置、行走、crossing-bound 和等价关系都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$M=(Q,\Sigma,\Gamma,\Delta,\delta,q_0,F)$` | 树上双向行走 + pushdown + 输出的机器骨架。 |
| 动作集合 | `$D=\{\mathrm{up}\}\cup\{\mathrm{stay}(\gamma)\}\cup\{\mathrm{down}(i,\gamma)\}$` | 三类原子移动覆盖返回、停留和下行。 |
| 转移关系 | `$\delta:Q\times\Sigma\times\Gamma\to\mathcal{P}(Q\times D\times\Delta^*)$` | 当前状态、节点标签和栈顶共同决定下一步。 |
| 成功翻译 | `$(q_0,\$(t),d_0,\#\gamma,\lambda)\vdash^*\cdots\vdash^*(q,\$(t),d_\$,\lambda,w)$` | 从根出发、栈清空、从哨兵根跌出并处于终态。 |
| 结构对应 | `$\mathrm{CT\text{-}PD}(\mathrm{REC}) = yT(\mathrm{REC})$` | 双向行走机器与 top-down tree transducer 在生成能力上等价。 |

## 构造方式与承载格式

### 建模入口

建模时需要：

1. 选定输入树标签集和输出字母表。
2. 设计 pushdown alphabet。
3. 规定每个“状态 + 当前节点标签 + 栈顶”对应的 `up / stay / down` 动作。
4. 选择是否施加 `k`-crossing 或 `k`-pass 限制。

### 机器可处理承载方式

其机器可处理承载方式是有限状态转移表：

1. 树节点标签；
2. pushdown 顶符号；
3. 行走动作；
4. 输出片段。

### 交换与互操作

它与 top-down tree transducers、tree-walking automata、two-way gsm、checking stack automata 和 macro grammar 路线直接互操作。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程化标准格式。
- 仿真/执行支持：配置语义和 move relation 足以直接执行。
- 验证/分析支持：crossing-bound、pass-bound、determinism 与等价性是全文核心。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：主要作为 automata theory 中的树行走/双向机器节点存在。

## 适用场景与需求前提

### 适用场景

适合解释“输入是树，但处理机制更像双向机器而不是并行树重写”的理论场景，例如语法树遍历、受限复制的树到串翻译和树上路径驱动的结构分析。

### 需求前提

1. 输入必须天然是树。
2. 系统行为能写成沿树边 `up / down / stay` 的有限控制过程。
3. 若要限制表达力，应能接受 crossing / pass 这类结构性边界。

### 不适用或高成本场景

若需求本质上是全局并行重写、复杂上下文参数传播或工程化 DSL 承载，`ct-pd` 不是最自然的入口。

## 与相邻形式主义的关系

相对 [bottom-up-and-top-down-tree-transformations-a-comparison/desc.md](../bottom-up-and-top-down-tree-transformations-a-comparison/desc.md)，它把树变换从 rule-based 解释切到了 machine-based 解释；相对 [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md)，它没有显式上下文参数，而是把上下文记忆外化为 pushdown；相对经典 two-way transducer，它是树对象上的推广版本。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Tree Automata` 主干旁边长期缺失的“tree-walking / two-way machine”支线正式挂出来，使树对象谱系不只剩识别器和规则式变换器两类。

### 作为目标形式主义还是中间表示

更适合作为演化树上的理论节点和能力边界参照，而不是控制系统最终建模语言。

### 对需求到模型生成的启发

如果未来需求涉及“树结构上的受限遍历程序”，`ct-pd` 提醒我们可以用路径行走与有限栈，而不一定非要使用全局树改写或带参数递归。

### 现实限制

缺少工程标准和主流工具，主要价值在于谱系定位和机器化解释。

## 重要的相关工作

### 奠基或前身工作

- [tree-automata/desc.md](../tree-automata/desc.md)

### 同类型或同家族工作

- [bottom-up-and-top-down-tree-transformations-a-comparison/desc.md](../bottom-up-and-top-down-tree-transformations-a-comparison/desc.md)
- [macro-tree-transducers/desc.md](../macro-tree-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合补入当前演化树中 `Tree Automata` 旁侧的“walking / two-way machine”经典支线。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Checking Tree Pushdown Transducers / Tree-Walking Machine Line
- 论文角色：模型提出
- 核心功能：用树上双向行走、pushdown 与输出带统一刻画 tree transducer 和 tree-walking machine 支线。
- 关键特性：`up / stay / down` 行走、pushdown 同步、crossing/pass 约束、与 top-down tree transducer 的等价。
- 构造方式：有限状态 + 树节点指针 + pushdown alphabet + 输出片段。
- 配套基础设施：以理论机器模型和等价结果为主，无工程标准。
- 适用场景：树到串翻译、受限树遍历、two-way machine 理论与树对象行走模型。

