# 通过商化验证 State/Event 系统 / Verification of State/Event Systems by Quotienting

## 基本信息

- 标题：Verification of State/Event Systems by Quotienting
- 中文标题：通过商化验证 State/Event 系统
- 作者：Nicky Oliver Bodentien, Jacob Vestergaard, Jakob Friis, Kåre Jelling Kristoffersen, Kim Guldstrand Larsen
- 发表：*BRICS Report Series*, 6(41), 1999
- DOI：`10.7146/brics.v6i41.20111`
- 链接：https://doi.org/10.7146/brics.v6i41.20111
- 形式主义：`State/Event Machines / Systems (SEM / S/E systems)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：family semantics / quotient-based compositional anchor
- 工具/实现获取方式：原文直接以 `VisualSTATE` 的 `S/E system` 为对象；机器可处理入口是局部机三元组、guard grammar、并发组合与 quotient logic `M_I`。
- 标准/格式获取方式：原文没有独立标准格式；核心承载方式是 `S/E` 机定义、guard 投影、组合规则与 quotient 逻辑公式。

## 简报

这篇论文虽然标题是 quotienting，但它并不是在一个既定黑箱模型上随手做个算法，而是把 `State/Event system` 再次正式化了一遍，并给出可组合、可 factor-out 的语义接口。对当前演化树来说，它的重要性在于：`SEM` 节点不再只靠“工业工具里有这种模型”的侧证存在，而是有一篇会明确写出单机三元组、guard grammar、并发组合和 dependency-closed 条件的理论锚点。

- 形式主义定位：`SEM` 母线上的第二个稳定锚点，重点补足 compositional semantics 与 quotient interface。
- 构造方式简述：每台 `S/E` 机由局部状态、初始状态和带 guard 的事件迁移构成；多个机器通过同步 composition 组合。
- 基础设施与场景简述：原文引入了专门的模态逻辑 `M_I`，使“把某台机器从系统里 factor out”成为形式上可定义的操作，而不是工具工程技巧。

```text
局部 S/E 机 -> 同步组合成系统 -> 用 quotient 把部分机器折入公式 -> 保持在 S/E family 内做 compositional verification
```

## 形式主义定义与核心对象

### 定义对象

原文把 `S/E system` 视为由若干局部 `S/E machine` 组成的同步并发系统。和上一条 `SEM` 母文献相比，这里更强调“机器如何组合”以及“何时能把某些机器商化进规格里”。

### 核心抽象

论文直接给出局部机三元组：

$$
M_i = (\Sigma_{\{i\}}, s_i^0, \to_{\{i\}})
$$

上式中的符号逐项解释如下：

1. `\Sigma_{\{i\}}` 是机器 `i` 的局部状态集合。
2. `s_i^0` 是机器 `i` 的初始状态。
3. `\to_{\{i\}}` 是机器 `i` 的局部迁移关系。

对应迁移关系满足：

$$
\to_{\{i\}} \subseteq \Sigma_{\{i\}} \times E \times G_{\{i\}} \times \Sigma_{\{i\}}
$$

上式中的符号逐项解释如下：

1. `E` 是输入事件字母表。
2. `G_{\{i\}}` 是不引用机器 `i` 自身位置变量的 guard 集合。
3. 一条迁移只记录“局部状态、输入事件、guard、后继局部状态”；原文在这一版中把输出事件从验证核心中抽掉了。

原文进一步定义系统全局状态为：

$$
\Sigma = \Sigma_{\{1\}} \times \Sigma_{\{2\}} \times \cdots \times \Sigma_{\{n\}}
$$

### 一个最小例子与通俗解释

可以把它理解成三个同步工作的局部控制器：

1. `M_1` 管“运行/停止”。
2. `M_2` 管“门开/门关”。
3. `M_3` 管“告警/正常”。

若 `M_1` 的某条 `Go` 迁移 guard 写成 `M_2 = Closed`，就表示“只有门关了，运行控制器才允许启动”。`quotienting` 做的事，则是把某台机器的行为折叠进逻辑规格中，让剩余系统在更小的上下文里继续验证。

通俗地说，`SEM` 本身像“几台同步控制器一起跑”；这篇论文进一步把它变成“几台同步控制器里，某一台还能被吸收到规格里，不必一直留在系统侧”。

### 运行 / 接受 / 转移语义

论文直接给出组合规则。对两个索引集不相交的局部系统 `M_I` 与 `M_J`，其组合写成：

$$
M_I \parallel M_J = (\Sigma_I \times \Sigma_J,\ s_I^0 \times s_J^0,\ \to_{I \cup J})
$$

上式中的符号逐项解释如下：

1. `\Sigma_I` 与 `\Sigma_J` 是两侧局部系统的状态空间。
2. `s_I^0` 与 `s_J^0` 是两侧初始状态。
3. `\to_{I \cup J}` 是组合后的同步迁移关系。

原文的 inference rule 本质上表示：如果左右两边都能在同一输入事件 `e` 上迈步，则组合系统也在该事件上同步迈步，并把两个 guard 交到同一个上下文里求值。

论文还给出 dependency-closed 条件：

$$
M=(\Sigma_I,s^0,\to_I)\ \text{is dependency closed iff all guards in }\to_I\text{ are true}
$$

其含义是：若一个子系统内部已不再引用外部机器的位置变量，那么它就成了“自足”的组合单元。

### 语义边界

这篇论文的 `SEM` 边界如下：

1. 仍是纯离散同步状态机 family。
2. 不引入 hierarchy、time 或 recursion。
3. 通过 guard 依赖表达跨机约束，而不是共享变量程序语义。
4. quotient 发生在“系统与规格的边界”，不是在模型本体里引入新状态机构造子。

### 关键性质与判定边界

论文最核心的形式化问题是：

$$
(M_1 \parallel \cdots \parallel M_n) \models \varphi
$$

以及商化后的等价变形：

$$
(M_1 \parallel \cdots \parallel M_{n-1}) \models \varphi / M_n
$$

上式中的符号逐项解释如下：

1. `\varphi` 是针对 `S/E system` 的模态逻辑规格。
2. `\varphi / M_n` 表示把机器 `M_n` factor into specification 后得到的 quotient 公式。
3. 这两式表达的是 compositional verification 的核心等价。

对当前文库来说，更重要的是：为了让 quotient 有定义，论文必须先把 `SEM` 的状态、guard、组合、dependency-closed 条件明确下来。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 以多个局部 `S/E` 机组成。 |
| 事件 / 触发 | 强支持 | 输入事件驱动同步反应。 |
| 守卫 / 数据 | 部分支持 | guard 依赖其他机器局部状态。 |
| 层次 | 不支持 | 仍是 flat `SEM`。 |
| 并发 / 同步 | 强支持 | composition rule 是核心。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | quotient 与 logic `M_I` 直接面向 compositional verification。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单机三元组 | `$M_i=(\Sigma_{\{i\}},s_i^0,\to_{\{i\}})$` | `SEM` 局部单元。 |
| 局部迁移 | `$\to_{\{i\}} \subseteq \Sigma_{\{i\}} \times E \times G_{\{i\}} \times \Sigma_{\{i\}}$` | 带 guard 的事件迁移。 |
| 全局状态 | `$\Sigma=\Sigma_{\{1\}}\times\cdots\times\Sigma_{\{n\}}$` | 系统状态空间。 |
| 同步组合 | `$M_I \parallel M_J = (\Sigma_I \times \Sigma_J,s_I^0 \times s_J^0,\to_{I\cup J})$` | 并发组合语义。 |
| quotient 等价 | `$(M_1 \parallel \cdots \parallel M_n)\models\varphi \iff (M_1 \parallel \cdots \parallel M_{n-1})\models \varphi / M_n$` | compositional verification 的核心结构。 |

## 构造方式与承载格式

### 建模入口

1. 先定义每台局部 `S/E` 机的状态集合与初始状态。
2. 再为每条迁移写输入事件与 guard。
3. 用同步 composition 把多个局部机并成系统。
4. 若要做 quotient，就把部分机器逐步折进规格公式而不是继续保留在系统侧。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 局部机三元组。
2. guard grammar 与 projection。
3. 同步 composition rule。
4. 模态逻辑 `M_I` 及 quotient 运算。

### 交换与互操作

原文没有工程交换标准，但提供了谱系上非常重要的一层：

1. 它把 `SEM` 从“工具里的并发状态机”推进到“可做 compositional quotient 的 formal family”。
2. 它为后续 `HSEM` 的 hierarchy-preserving verification 提供了直接前史。
3. 它证明 `SEM` 这条线并不只是应用建模壳，而是有自己的逻辑与组合边界。

## 配套基础设施

- 建模/编辑工具：原文明确依托 `VisualSTATE`。
- 解析/交换/元模型支持：核心是 `S/E` 机定义、guard projection 和 quotient logic；无独立公开元模型标准。
- 仿真/执行支持：通过 `VisualSTATE` 的系统构造与运行语义支撑。
- 验证/分析支持：quotient-based compositional verification。
- 代码生成/转换支持：论文背景与 `VisualSTATE` 的代码生成链路直接相关，但本篇重点不在生成。
- 标准化或社区生态：主要是研究与工业工具结合的 family 说明锚点。

## 适用场景与需求前提

### 适用场景

适合：

1. 由多个同步控制部件组成的嵌入式反应式系统。
2. 想保留 `SEM` 骨架，同时做 compositional verification 的场景。
3. 需要显式分析 machine dependency 的大型并发控制逻辑。

### 需求前提

1. 关键交互仍可写成有限事件和局部状态依赖。
2. 系统可拆成多个 guard-coupled 局部机。
3. 希望验证任务能随组件 factor-out 而逐步缩减。

### 不适用或高成本场景

若需求核心是层次 superstate，应直接进入 [verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md](../verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md)；若核心是 entry/exit 与 black-box mode semantics，则更接近 [efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md](../efficient-reachability-analysis-of-hierarchic-reactive-machines/desc.md)。

## 与相邻形式主义的关系

相对上一条 `SEM` journal full version，这篇论文没有换 family，而是把 `SEM` 的 compositional semantics 和 quotient interface 讲得更清楚；相对 `HSEM`，它还没有 nested states；相对 `HSM`，它也不通过 hierarchy graph / boxes 表达结构压缩。

## 与本研究的关系

### 对 Project 1 的价值

它让 `SEM` 不只是树上的一个名字，而是一个“有清晰组合规则、可定义 dependency-closed 子系统、可与逻辑接口对接”的状态机 family。

### 作为目标形式主义还是中间表示

更像谱系父节点和中间表示，不适合作为终点模型，但非常适合说明“多个局部反应式需求怎样先汇成同步控制 family”。

### 对需求到模型生成的启发

如果需求可明显分解成多个子控制器，而且不同子控制器之间的耦合主要体现在“某个控制器在某状态时另一个控制器才允许触发”，那么 `SEM` 是很好的第一层结构化目标。

### 现实限制

它依然缺少 hierarchy、time、recursion 等更强表达力，因此很快会遇到复杂控制层次的表达上限。

## 重要的相关工作

### 前后衔接

- [verification-of-large-state-event-systems-using-compositionality-and-dependency-analysis/desc.md](../verification-of-large-state-event-systems-using-compositionality-and-dependency-analysis/desc.md)
- [verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md](../verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md)

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为对象仍是有限离散同步状态机，而不是时间、混成或概率扩展。
- 这是一篇 `🧱 模型本体` 文献，因为 quotient 的成立依赖于原文把 `SEM` 的对象、guard、组合和 dependency-closed 条件完整写清。
- 这篇论文的描述客体是 `🎛️ 控制 / 反应式逻辑`，因为模型天然面向嵌入式反应式控制系统。
- 这篇论文属于 `🧮 形式语言与自动机理论`，因为它服务的是状态机 family 的形式化语义和组合边界，而不是应用部署细节。
