# 基于接口自动机的状态/事件故障树定性分析 / Qualitative Analysis of State/Event Fault Trees Based on Interface Automata

## 基本信息

- 标题：Qualitative Analysis of State/Event Fault Trees Based on Interface Automata
- 中文标题：基于接口自动机的状态/事件故障树定性分析
- 作者：Gaofeng He, Bingfeng Xu
- 发表：*International Journal of Safety and Security Engineering*, 11(6):663-669, 2021
- DOI：`10.18280/ijsse.110606`
- 链接：https://doi.org/10.18280/ijsse.110606
- 形式主义：`Guarded Interface Automata (GIA)`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：故障树语义建模 / 接口自动机扩展在安全分析中的应用
- 工具/实现获取方式：原文给出 `GIA`、并行组合、weak bisimilarity 划分和 `MCS` 搜索算法；未提供公开代码仓库，仅与 `SEFTAnalyzer` 做对比。
- 标准/格式获取方式：承载方式是 `SEFT` 逻辑门到 `GIA` 的翻译、product 组合、aggregation 与 cut-sequence 搜索；无独立交换格式。

## 简报

这篇论文的价值，不只是“用接口自动机做了一次故障树案例”，而是在 `SEFT` 这种同时含事件触发和状态守卫的安全模型上，给出了一种更贴近接口语义的形式化承载。作者认为，传统 `SEFT -> eDSPN -> reachability graph` 路线翻译层次太多、人工介入太重，于是直接在 `Interface Automata` 上增加 guard，得到 `Guarded Interface Automata (GIA)`，再用并行组合与弱互模拟规约来提取最小 cut sequence。

- 形式主义定位：面向状态/事件故障树语义建模的接口自动机扩展，而不是一般 fault tree 经验性分析。
- 构造方式简述：先把各类 `SEFT` 逻辑门翻译成 `GIA`，再按给定顺序做并行组合、weak bisimilarity aggregation 和行为搜索。
- 基础设施与场景简述：依托 `GIA` 元组、product 组合、弱互模拟类划分和 `MCS` 搜索算法，服务软件控制安全系统的失效原因分析。

```text
SEFT 逻辑门 / 事件 / 状态守卫 -> GIA -> 并行组合 + 弱互模拟规约 -> cut sequences -> minimal cut sequences
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. `SEFT` 中的基本事件、基本状态和逻辑门。
2. 继承自 `Interface Automata` 的状态、动作和迁移。
3. 额外加入到迁移上的 guard 集合。
4. 用于规约状态空间的 weak bisimilarity。
5. 从初始状态到 top-event 失败状态的 cut sequences。

### 核心抽象

原文把 `GIA` 直接定义为：

$$
P = (V_P, v^{init}_P, A_P, I_P, \Gamma_P)
$$

上式中的符号逐项解释如下：

1. `V_P` 是有限状态集合。
2. `v^{init}_P \in V_P` 是初始状态。
3. `A_P` 是动作集合，并被划分为输入、输出和内部动作。
4. `I_P` 是有限 guard 集合。
5. `\Gamma_P \subseteq V_P \times A_P \times I_P \times V_P` 是带 guard 的迁移集合。

论文对 guard 的语法也给了明确限制：

$$
\varphi ::= s \mid \varphi \land \varphi \mid \varphi \lor \varphi
$$

上式中的符号逐项解释如下：

1. `s` 表示系统中某个被监视的状态谓词。
2. `\land` 与 `\lor` 分别表示 guard 的合取和析取。
3. 因此 `GIA` 不是给迁移随意加代码条件，而是限定为由组件状态构成的布尔守卫。

两台可组合 `GIA` 的 product 在原文中可压缩为：

$$
P \mathbin{//} Q = (V_P \times V_Q,\ v^{init}_P \times v^{init}_Q,\ A,\ I_P \cup I_Q,\ \Gamma)
$$

上式中的符号逐项解释如下：

1. `V_P \times V_Q` 表示组合状态空间。
2. `A` 由双方共享动作与各自局部动作共同组成。
3. `I_P \cup I_Q` 是组合后的 guard 集合。
4. `\Gamma` 由三类迁移构成：仅 `P` 自行推进、仅 `Q` 自行推进、共享动作同步推进。

### 一个最小例子与通俗解释

论文最直观的最小例子，其实就是 `SEFT` 里的 event/state-AND gate：

1. 事件输入表示“某故障触发已经发生”。
2. 状态输入表示“某个状态条件当前满足”。
3. 只有当触发事件到达且状态 guard 为真时，输出故障才发生。
4. 这正对应 `GIA` 里“动作 + guard”共同决定迁移是否可走。

通俗地说，普通 `Interface Automata` 更像“收到这个消息就走边”；`GIA` 则像“收到这个消息，但还得看某个部件是否已经处于危险状态，边才真的能走”。这正好匹配 `SEFT` 里“事件触发 + 状态允许/抑制”的语义。

### 运行 / 接受 / 转移语义

原文的弱互模拟定义可以保守压缩为：

$$ (s,t) \in R \land s \xRightarrow[a,[g]]{} s' \Rightarrow \exists t'.\ t \xRightarrow[a,[g]]{} t' \land (s',t') \in R $$

上式中的符号逐项解释如下：

1. `R` 是定义在状态集合上的等价关系。
2. `\xRightarrow[a,[g]]{}` 表示带动作 `a` 与 guard `[g]` 的弱迁移。
3. 若 `s` 可以通过某个弱迁移到达 `s'`，则与它等价的 `t` 也必须能以同类弱迁移到达某个 `t'`。
4. 这就是 `GIA` 规约时可以合并状态的语义依据。

论文最终关心的不是语言接受，而是 failure behavior 搜索。保守整理后，可把 `SEFT` 的最小 cut sequence 问题写成：

$$
\mathrm{MCS}(G) = \min \{\, \sigma \mid v^{init} \xRightarrow{\sigma} v^{fail} \,\}
$$

上式中的符号逐项解释如下：

1. `G` 是组合完成后的故障树 `GIA`。
2. `\sigma` 是由触发动作和状态 guard 共同构成的 cut sequence。
3. `v^{init}` 是系统初始状态。
4. `v^{fail}` 是 top event 对应的失败状态。
5. `\min` 表示对 cut sequence 做最小化约简，得到 minimal cut sequences。

### 语义边界

这篇论文的边界比较明确：

1. 它仍然是离散接口模型，不引入时间、概率或连续动力学。
2. `GIA` 的 guard 只描述状态条件，不承载复杂数据变换。
3. 目标是 `SEFT` 语义与 `MCS` 搜索，不是一般组件契约综合。
4. 并行组合顺序仍需要人工决定，因此自动化程度高于旧方法，但还不是完全自动。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `GIA` 元组 | `$P = (V_P, v^{init}_P, A_P, I_P, \Gamma_P)$` | 在 `IA` 上补入显式 guard。 |
| guard 语法 | `$\varphi ::= s \mid \varphi \land \varphi \mid \varphi \lor \varphi$` | 限定守卫来源于组件状态。 |
| product 组合 | `$P // Q$` | 对 `SEFT` 子门语义做 compositional aggregation。 |
| weak bisimilarity | `$P \approx Q$` | 在不改变外部行为的前提下规约状态空间。 |
| `MCS` 搜索 | `$v^{init} \xRightarrow{\sigma} v^{fail}$` | 从组合语义中提取失效 cut sequences。 |
| 复杂度 | `O(n^3)` | 原文给出弱互模拟类划分算法复杂度。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 故障树状态、门状态和聚合状态都映射到显式 automaton states。 |
| 事件 / 触发 | 强支持 | 基本事件与门输出天然对应动作。 |
| 守卫 / 数据 | 强守卫、弱数据 | 重点是状态 guard，而不是复杂数据变量。 |
| 层次 | 弱支持 | 依靠 compositional aggregation，而非层次状态图。 |
| 并发 / 同步 | 强支持 | 共享动作同步与并行组合是核心。 |
| 时间约束 | 不支持 | 无时钟或 deadline。 |
| 连续动态 / 随机性 | 不支持 | 纯离散语义。 |
| 可执行 / 可验证性 | 强验证 | 可进行组合规约和 `MCS` 分析。 |

### 形式化问题与性质

1. 这篇论文最重要的增量，是把 `SEFT` 的“触发 + 状态允许”语义压成一个有正式 product 和 weak bisim 的自动机对象。
2. `GIA` 不是简单给 `IA` 加注释，而是明确把 guard 纳入迁移四元组。
3. 组合与规约之后，`SEFT` 的 cut sequence 搜索可以在单一 automaton 上进行。
4. 因而它既是接口自动机应用条目，也是一个可稳定命名的接口自动机扩展节点。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 先把 `SEFT` 的基本门识别为 `state-AND`、`event/state-AND`、`OR`、`PAND` 等局部模式。
2. 为每类门写出对应的 `GIA` 模板。
3. 按门之间的连接关系选择组合顺序。
4. 每一步组合后做 weak bisimilarity aggregation，最终得到表示整棵 `SEFT` 语义的单个 `GIA`。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `SEFT` 逻辑门到 `GIA` 的模板翻译。
2. `GIA` product 与 composability 判定。
3. weak bisimilarity classes partition。
4. cut sequence / minimal cut sequence 搜索算法。

### 交换与互操作

互操作重点在：

1. `SEFT` 门结构如何稳定映射为自动机模板。
2. 共享动作在 product 中如何同步。
3. aggregation 之后的规约模型如何继续承接后续组合和分析。

## 配套基础设施

- 建模/编辑工具：原文没有给专用建模器，主要以 `SEFT` 结构图和 `GIA` 数学定义承载。
- 解析/交换/元模型支持：无公开 XML/JSON/元模型标准。
- 仿真/执行支持：重点不在执行，而在 cut-sequence 分析。
- 验证/分析支持：`GIA` 组合、weak bisimilarity 规约、`MCS` 搜索算法。
- 代码生成/转换支持：支持从 `SEFT` 到 `GIA` 的形式翻译，但未提供公开转换器。
- 标准化或社区生态：依托 `Interface Automata` 与 safety analysis 研究线；原文对比对象是 `SEFTAnalyzer`。

## 适用场景与需求前提

### 适用场景

适合软件控制安全系统中那些既关心事件顺序、又关心状态守卫的失效场景，例如软件密集型安全系统、保护系统、火灾防护系统等。

### 需求前提

1. 故障逻辑可抽成有限个基本事件、基本状态和逻辑门。
2. 状态条件能够作为显式 guard 建模。
3. 失效因果链主要是离散的，而不是连续动力学驱动的。
4. 分析目标是最小 cut sequence，而不是概率失效评估。

### 不适用或高成本场景

如果系统主要难点是连续物理故障传播、概率失效率计算、或时间依赖失效窗口，仅靠 `GIA` 很难完整覆盖。

## 与相邻形式主义的关系

相对 [interface-automata/desc.md](../interface-automata/desc.md)，本文把 guard 提升为一等公民；相对 [refinement-of-interface-automata-strengthened-by-action-semantics/desc.md](../refinement-of-interface-automata-strengthened-by-action-semantics/desc.md)，它关注的是故障树语义与 cut-sequence 搜索，而不是组件替换精化；相对 [an-introduction-to-pervasive-interface-automata/desc.md](../an-introduction-to-pervasive-interface-automata/desc.md)，它不讨论环境假设和服务保持，而是把接口自动机拉向 safety analysis。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：接口自动机并不只适用于软件组件组合，也可以成为“需求中的触发条件 + 状态约束”这种混合逻辑的形式化承载。

### 作为目标形式主义还是中间表示

对故障分析场景，它可以直接作为目标形式主义；对更一般的控制需求建模，它也可作为从自然语言守卫条件过渡到更复杂状态机模型的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把“触发事件”和“状态允许条件”分开表示。
2. 若后续要做验证或修复，guard 不能只留在自然语言里，最好在状态机层显式化。
3. 当目标是失效因果链分析时，接口自动机式的 compositional route 比一次性平铺更可维护。

## 重要的相关工作

- [interface-automata/desc.md](../interface-automata/desc.md)：原始接口自动机主干。
- [refinement-of-interface-automata-strengthened-by-action-semantics/desc.md](../refinement-of-interface-automata-strengthened-by-action-semantics/desc.md)：把动作语义并入接口自动机的另一条扩展线。
- [an-introduction-to-pervasive-interface-automata/desc.md](../an-introduction-to-pervasive-interface-automata/desc.md)：接口自动机在环境假设与替换问题上的扩展。

## 文献分类总结

- 这是一篇 `🔌` 类高价值应用条目，但它不只是“案例”，还明确提出了 `Guarded Interface Automata (GIA)` 这条接口自动机扩展线。
- 其描述客体仍是触发/守卫驱动的交互结构，因此记为 `🤝`；论文语境偏软件控制安全分析，因此记为 `💻`。
- 对 `project_1` 来说，它补足了“事件触发 + 状态守卫”这一类需求特征在接口自动机谱系中的可落地承载。
