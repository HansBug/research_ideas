# 卵石交替树行走自动机及其识别能力 / Pebble Alternating Tree-Walking Automata and Their Recognizing Power

## 基本信息

- 标题：Pebble Alternating Tree-Walking Automata and Their Recognizing Power
- 中文标题：卵石交替树行走自动机及其识别能力
- 作者：Loránd Muzamel
- 发表：*Acta Cybernetica*, 18(3):427-450, 2008
- DOI：原文未提供
- 链接：https://cyber.bibl.u-szeged.hu/index.php/actcybern/article/view/3731
- 形式主义：`Pebble Alternating Tree-Walking Automata (PATWA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `A=(Q,\Sigma,q_0,q_{yes},R)`、pebble configuration、tests 函数与 alternating rules。
- 标准/格式获取方式：原文没有工程 DSL 或交换标准，核心承载方式是 ranked tree、状态分层、强/弱 pebble handling 和 computation-tree 语义。

## 简报

这篇论文把 tree-walking + pebble 这条线再往前推了一步：它在 nested-pebble tree-walking automata 上加入 alternation，并证明带 strong pebble handling 的 `n-PATWA` 仍然恰好识别全部 regular tree languages。它的关键价值，是把 `Tree-Walking` 支线补成一条更完整的层级链条：普通 `TWA` 不够强，nested pebble 提供更强记忆，而 alternating pebble 则把 regular tree languages 全部覆盖。

- 形式主义定位：`Nested-Pebble Tree-Walking Automata` 的 alternating 扩展，是 `Tree Automata` 旁边顺序树机器支线的重要增强节点。
- 构造方式简述：机器在树上移动一个 reading head，stack-like 地 drop/lift pebbles，并允许 alternating rules 产生并行计算线程。
- 基础设施与场景简述：原文是纯理论工作，但给出 `REG = n-PATWA`、deterministic non-looping hierarchy 以及 strong pebble handling 的表达力结论。

```text
输入树 -> tree walking + nested pebbles + alternation -> computation tree -> regular tree language recognition
```

## 形式主义定义与核心对象

### 定义对象

`PATWA` 处理的是 ranked tree language recognition。它与普通 `TWA` 的区别，不只是多了 pebbles，而是允许在同一 configuration 上分裂出多个必须同时成功的并行分支。

### 核心抽象

原文把 `n`-pebble alternating tree-walking automaton 定义为：

$$
A = (Q,\Sigma,q_0,q_{yes},R)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限非空状态集，并被分成 `Q_0,\ldots,Q_n`。
2. `\Sigma` 是 ranked input alphabet。
3. `q_0 \in Q_0` 是初始状态。
4. `q_{yes}` 是唯一接受状态。
5. `R` 是规则集，也按 pebble 数分层为 `R_0,\ldots,R_n`。

原文的 alternating rule 形如：

$$
\langle q,\sigma,b,j \rangle \to \{ \langle p_1,\mathrm{stay} \rangle,\langle p_2,\mathrm{stay} \rangle \}
$$

而普通 pebble/tree-walking rule 形如：

$$
\langle q,\sigma,b,j \rangle \to \langle p,\varphi \rangle
$$

上面两式中的符号逐项解释如下：

1. `q,p,p_1,p_2` 是状态。
2. `\sigma` 是当前节点标签。
3. `b` 是一个 bit vector，记录当前节点上可见的 pebbles。
4. `j` 是当前节点的 child number。
5. `\varphi` 是 `\mathrm{stay}/\mathrm{up}/\mathrm{down}_i/\mathrm{drop}/\mathrm{lift}` 之一。

### 一个最小例子与通俗解释

一个最小直觉例子是：当机器站在某个树节点上时，先通过 alternating rule 把计算分成两个线程，一个线程继续检查左侧子树，另一个线程检查右侧子树；只有两个线程都能最终到达 `q_{yes}`，整棵树才算被接受。与此同时，如果某个祖先位置需要稍后再用，机器可以先把当前节点用 pebble 标出来，等子任务做完后再按 stack discipline 回收。

通俗地说，`PATWA` 像“会在树上走动、会做书签、还能把检查任务分派成若干必须都通过的小检查员”。普通 `TWA` 只有一个人在树上来回跑；`PATWA` 则允许它在关键点分叉出并行义务。

### 运行 / 接受 / 转移语义

原文先把 pebble configuration 定义为：

$$
h = (u,\pi)
$$

上式中的符号逐项解释如下：

1. `u` 是当前 reading head 所在节点。
2. `\pi` 是当前已丢下 pebbles 的位置串，长度至多为 `n`。

测试函数写成：

$$
\mathrm{tests}(h) = (\sigma,b,j)
$$

上式中的符号逐项解释如下：

1. `\sigma` 是当前节点标签。
2. `b` 记录哪些 pebbles 正好位于当前节点。
3. `j` 是当前节点的 child number。

原文的最关键接受结论是：从根节点、无 pebble 的初始配置出发，若 computation tree 的所有分支都能终止于 `q_{yes}`，则输入树被接受。

### 语义边界

相对普通 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md) 的 `TWA`，它多了 pebbles 和 alternation；相对 [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md) 的 nested-pebble `TWA`，它进一步允许并行义务；相对 classic bottom-up `Tree Automata`，它仍然是顺序行走式而不是一次性汇总所有子树。

### 关键性质与判定边界

原文主结论是：

$$
\mathrm{REG} = n\text{-}\mathrm{PATWA}
$$

并进一步证明 deterministic non-looping 子类存在严格层级：

$$
\mathrm{dTWA} \subset \mathrm{dATWA}_{nl} \subset 1\text{-}\mathrm{dPATWA}_{nl} \subset 2\text{-}\mathrm{dPATWA}_{nl} \subset \cdots \subset \mathrm{REG}
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{REG}` 是 regular tree languages。
2. `n\text{-}\mathrm{PATWA}` 是使用 `n` 个 pebbles 的 alternating tree-walking automata。
3. `\mathrm{dATWA}_{nl}` 是 deterministic non-looping alternating tree-walking automata。
4. `\mathrm{dPATWA}_{nl}` 是 deterministic non-looping pebble alternating tree-walking automata。

这说明 alternation + pebbles 组合起来后，顺序 tree-walking 支线终于能覆盖 regular tree languages；但把模型限制成 deterministic non-looping 后，又会重新出现严格表达力层级。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态仍是主控制骨架。 |
| 事件 / 触发 | 不适用 | 输入是静态树结构。 |
| 守卫 / 数据 | 部分支持 | 支持标签、child number 和 pebble presence 测试。 |
| 层次 | 强支持 | 输入天然是树。 |
| 并发 / 同步 | 强支持 | alternation 直接产生必须同时成功的并行线程。 |
| 时间约束 | 不支持 | 纯离散树机器。 |
| 连续动态 / 随机性 | 不支持 | 无连续或概率语义。 |
| 可执行 / 可验证性 | 强理论支持 | 有明确规则系统、正则树语言刻画和子类层级。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=(Q,\Sigma,q_0,q_{yes},R)$` | `PATWA` 的规则式骨架。 |
| pebble 配置 | `$h=(u,\pi)$` | 记录当前节点和 stack-like pebble 位置。 |
| 测试函数 | `$\mathrm{tests}(h)=(\sigma,b,j)$` | 当前标签、pebble presence 与 child number 决定可用规则。 |
| 正则性结论 | `$\mathrm{REG}=n\text{-}\mathrm{PATWA}$` | alternating pebble tree-walking 足以识别全部 regular tree languages。 |
| deterministic 层级 | `$\mathrm{dTWA}\subset\mathrm{dATWA}_{nl}\subset 1\text{-}\mathrm{dPATWA}_{nl}\subset\cdots$` | 加 pebble 数会严格提升 deterministic non-looping 子类能力。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输入对象是 ranked tree。
2. 再定义状态层级、可见 pebble 数和当前节点测试方式。
3. 为每类测试结果写出 move / drop / lift 规则。
4. 在需要 universal obligation 的地方引入 alternating rules。

### 机器可处理承载方式

机器可处理承载方式是规则表 `R`、pebble configuration、tests 函数和 computation-tree 语义，而不是工程化 DSL。

### 交换与互操作

它和 [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md) 的 nested-pebble `TWA` 直接形成前后继，也和 [tree-automata/desc.md](../tree-automata/desc.md) 的 regular tree language 主干在表达力上对齐。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是规则系统、pebble configuration 和 alternating semantics。
- 仿真/执行支持：可按规则集对 configuration sets 做解释执行。
- 验证/分析支持：regular tree language 等价、deterministic non-looping hierarchy 和表达力比较是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 tree automata / XML / descriptive tree-walking 理论的经典增强节点。

## 适用场景与需求前提

### 适用场景

适合“树对象 + 顺序导航 + 并行义务检查”的理论建模，以及 regular tree language 与 sequential tree-walking family 的能力对比。

### 需求前提

1. 输入必须是树。
2. 需求要能写成局部导航、有限状态判断和少量 nested pebbles。
3. 若要利用 alternation，问题本身应存在“多个子检查必须同时成功”的结构。

### 不适用或高成本场景

若对象是线性词、需要时间/概率/连续变量，或更关注工程载体与执行格式，这个模型就不合适。

## 与相邻形式主义的关系

相对 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md) 的 `TWA`，它补上了 pebble 和记忆增强；相对 [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md) 的 nested-pebble `TWA`，它再加入 alternation；相对 [tree-automata/desc.md](../tree-automata/desc.md)，它不是 bottom-up recognizer，而是顺序行走式 recognizer。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Tree-Walking` 支线从“普通 `TWA` -> nested pebbles -> alternating pebbles”补成完整母链，并明确哪一个节点第一次覆盖全部 regular tree languages。

### 作为目标形式主义还是中间表示

更适合作为谱系节点和能力边界参照，而不是控制系统主线的最终输出形式。

### 对需求到模型生成的启发

如果需求天然是树结构，并且一个节点上的判断需要分解成若干必须同时满足的子检查，那么 alternating tree-walking 模型比单线程 `TWA` 更贴切。

### 现实限制

这条路线几乎完全停留在理论层面，缺乏工程工具链，现实项目中主要价值仍然是谱系建树和能力理解。

## 重要的相关工作

### 奠基或前身工作

- [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)
- [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md)

### 同类型或同家族工作

- [tree-automata/desc.md](../tree-automata/desc.md)
- [tree-transducers-l-systems-and-two-way-machines/desc.md](../tree-transducers-l-systems-and-two-way-machines/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合补当前演化树里 `Nested-Pebble Tree-Walking` 下的 `Alternating` 子节点，并把 regular-tree 识别能力和顺序行走机器支线接通。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Pebble Alternating Tree-Walking Automata (PATWA)`
- 论文角色：模型扩展
- 核心功能：把 nested-pebble tree-walking 模型扩成 alternating 版本，并证明其恰好识别 regular tree languages。
- 关键特性：alternation、strong pebble handling、规则分层、regular-tree 完整表达力、deterministic non-looping 严格层级。
- 构造方式：`(Q,\Sigma,q_0,q_{yes},R)` 规则系统加 pebble configuration 与 computation-tree 语义。
- 基础设施：纯理论模型，无工程标准或工具。
- 适用场景：树语言识别、sequential tree-walking 能力边界、regular tree languages 理论分析。
- 需求前提：对象必须是树，且问题可由局部导航、pebbles 与 alternating obligations 描述。
- 状态：🟢
