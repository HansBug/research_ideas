# PIPE+：高级 Petri 网建模工具 / PIPE+ - A Modeling Tool for High Level Petri Nets

## 基本信息

- 标题：PIPE+ - A Modeling Tool for High Level Petri Nets
- 中文标题：PIPE+：高级 Petri 网建模工具
- 作者：Su Liu，Reng Zeng，Xudong He
- 发表：*Proceedings of the 23rd International Conference on Software Engineering and Knowledge Engineering*，pp. 115-121，2011
- DOI：原文未提供
- 链接：https://users.cs.fiu.edu/~hex/PIPE%2B-15/PIPEplus%20%20A%20Modeling%20Tool%20for%20High%20Level%20Petri%20Nets.pdf
- 形式主义：`High Level Petri Nets / PIPE+`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：high-level PN editor / simulator built on PIPE
- 工具/实现获取方式：原文明确说明 `PIPE+` 可从作者页面下载，并强调其基于开源 `PIPE` 扩展而成。
- 标准/格式获取方式：承载方式是 `PIPE` 图形编辑器、其 `PNML` 存储链路以及 `PIPE+` 自定义的数据类型、token、arc annotation 与 transition formula 机制；原文未给中立的高层网交换标准实现。

## 简报

这篇论文的价值，在于把“国际标准里相当抽象的 high-level Petri net 概念”压成一个真的能画、能存、能跑的工具原型。`PIPE+` 不是重新发明一种全新的网模型，而是选择了 `PIPE` 作为底座，用 place type、structured token、arc variable、受限一阶逻辑 transition formula 和 simulator 把高层网做成了一条可执行工具线。它补的是文库里长期缺的 `High-Level Petri Nets` 工具锚点。

- 形式主义定位：高级 Petri 网的图形建模与仿真工具，而不是新的网理论母文。
- 构造方式简述：在 `PIPE` 的 place / transition / arc 图形骨架上，增添 place type、token data structure、arc annotation、transition condition formula 与 symbol table 解释器。
- 基础设施与场景简述：依托 `PIPE` 的 GUI、`PNML` 持久化、扩展后的 `DataLayer`、parser/interpreter 与 simulator，服务需要同时表达控制流和数据流的并发系统。

```text
concurrent process + data tokens -> high-level Petri net in PIPE+ -> formula-driven transition firing -> token-flow simulation
```

## 形式主义定义与核心对象

### 定义对象

论文直接把 high-level Petri nets 的核心组成列成六类：

1. net graph。
2. place types。
3. place markings。
4. arc annotations。
5. transition conditions。
6. declarations。

### 核心抽象

结合论文对标准 high-level Petri net 的归纳，可保守整理为：

$$
HLPN = (P, T, F, Type, Mark, Ann, Cond, Decl)
$$

上式中的符号逐项解释如下：

1. `P` 是 places 集合。
2. `T` 是 transitions 集合。
3. `F` 是 arcs 集合。
4. `Type` 为各 place 指派 token 数据结构。
5. `Mark` 为各 place 指派当前 token 集合。
6. `Ann` 是 arc annotations，即弧上的变量或表达式。
7. `Cond` 是 transition condition formulas。
8. `Decl` 是类型、变量和函数等声明。

论文把 `PIPE+` 的执行关键落在“arc variable 绑定 + pre/post 逻辑条件”上。可保守压成：

$$
\theta : Var_{arc} \to Token \cup 2^{Token}
$$

上式中的符号逐项解释如下：

1. `Var_{arc}` 是弧上变量集合。
2. `Token` 是普通结构化 token。
3. `2^{Token}` 对应 power-set 风格的 abstract token。
4. `\theta` 是由输入 places 中 token 组合得到的符号表绑定。

在绑定 `\theta` 下，transition 的使能条件可写成：

$$
enabled(t,M) \iff \exists \theta.\ \Phi_t^{pre}(\theta, M) = \mathrm{true}
$$

上式中的符号逐项解释如下：

1. `t` 是待检查的 transition。
2. `M` 是当前 marking。
3. `\Phi_t^{pre}` 是 transition formula 的 pre-condition 部分。
4. 若存在某个 token 组合绑定 `\theta` 使其为真，则 `t` 可发生。

发生后的 marking 更新可保守写成：

$$
M' = (M \ominus In_t(\theta)) \oplus Out_t(\theta, \Phi_t^{post})
$$

上式中的符号逐项解释如下：

1. `In_t(\theta)` 表示 firing 时从输入 places 消耗的 token 组合。
2. `Out_t(\theta, \Phi_t^{post})` 表示根据 post-condition 计算后写入输出 places 的 token。
3. `\ominus` 与 `\oplus` 分别表示删除和加入 token multiset。

### 一个最小例子与通俗解释

论文里最直观的解释，是把普通黑点 token 换成有结构的数据：

1. 一个登录用户 token 可以是 `(username, password)` 这样的二元组。
2. place type 规定这个 place 里只能放这种结构的 token。
3. transition 通过 arc variables 把输入 token 绑定到逻辑公式变量。
4. 公式成立时，输出变量就会被赋值，生成新的结构化 token 流向输出 place。

通俗地说，`PIPE+` 像“给 Petri 网的 token 装上数据字段，再给 transition 装上解释器”。普通低层网主要追踪 token 个数，而这里一个 transition 可以根据 token 内容决定是否触发、生成什么新 token。

### 运行 / 接受 / 转移语义

论文把 transition formula 分成 pre-condition 与 post-condition 两部分。pre-condition 判断使能，post-condition 负责构造输出 token。其计算流程可保守写成：

$$
\theta = \mathrm{bind}(Ann_t, M)
$$

$$
\Phi_t^{pre}(\theta) = \mathrm{true} \Rightarrow fire(t,\theta)
$$

$$
\Phi_t^{post}(\theta) \Rightarrow \text{assign output variables and generate output tokens}
$$

上式中的符号逐项解释如下：

1. `Ann_t` 是 transition 相邻 arcs 上的变量标注。
2. `\mathrm{bind}` 会枚举输入 places 中 token 组合并填充 symbol table。
3. `\Phi_t^{pre}` 成立后，transition 才可发生。
4. `\Phi_t^{post}` 把右侧表达式结果赋给输出变量，再按输出弧把 token 写回 places。

论文还强调：

1. abstract token 用来处理 power-set 风格 place。
2. interpreter 要区分 `=` 在 pre-condition 中代表逻辑相等，在 post-condition 中代表赋值。
3. simulator 采用 locality-based scheduling，尽量避免无谓重算 disabled transitions。

### 语义边界

这篇论文同样明确给出局限：

1. 基本类型目前只支持 `string` 和 `integer`。
2. nested power set 被拍平成 flat tokens。
3. transition formula 是受限一阶逻辑，而不是完全一般的逻辑语言。
4. 只支持 interleaving semantics，不支持 true concurrency 与 timed Petri nets。
5. 还缺少成熟的 integrated analysis module。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 高层网骨架 | `$HLPN = (P, T, F, Type, Mark, Ann, Cond, Decl)$` | 把 place type、marking、arc annotation 与条件公式纳入同一模型。 |
| 符号表绑定 | `$\theta : Var_{arc} \to Token \cup 2^{Token}$` | 用 arc variables 把输入 token 组合映射到公式变量。 |
| 使能判定 | `$enabled(t,M) \iff \exists \theta.\ \Phi_t^{pre}(\theta, M) = \mathrm{true}$` | 只有存在满足 pre-condition 的 token 组合时才能发生。 |
| firing 更新 | `$M' = (M \ominus In_t(\theta)) \oplus Out_t(\theta, \Phi_t^{post})$` | 发生时既消费输入 token，又根据 post-condition 生成输出 token。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 仍是系统状态骨架。 |
| 事件 / 触发 | 强支持 | transitions 表示离散事件发生。 |
| 守卫 / 数据 | 很强 | 结构化 token、arc annotation 和逻辑公式是主线。 |
| 层次 | 不支持 | 工具主要关注单层高层网。 |
| 并发 / 同步 | 强支持 | Petri 网并发语义仍是底座，但实现为 interleaving simulation。 |
| 时间约束 | 不支持 | 原文明确指出暂不支持 timed Petri nets。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散并发数据流。 |
| 可执行 / 可验证性 | 中等支持 | 图形编辑与 simulation 已有，analysis module 仍偏弱。 |

### 形式化问题与性质

1. `PIPE+` 的关键不是提出新数学家族，而是把 high-level PN 的若干核心构件压成可执行子集。
2. 论文最有价值的工程细节，是如何在低层 `PIPE` 上逐步增添 DataType、Token、abToken、parser 和 scheduler。
3. 它证明“高层 Petri 网”要落地，不能只给抽象标准定义，还需要绑定机制、解释器和仿真调度器。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 在 `PIPE` 图形编辑器中画 net graph。
2. 给 places 定义 data type 并手工填 token。
3. 给 arcs 标注变量名。
4. 给 transitions 写受限一阶逻辑公式。
5. 用 simulator 观察 token 值在 places 之间流动。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PIPE` 图形模型。
2. place data type、token list 与 abstract token。
3. arc variable annotations。
4. transition formula 的 parser / interpreter 内部表示。
5. 继承自 `PIPE` 的 `PNML` 存储链路。

### 交换与互操作

这篇论文的互操作重点是“在既有低层工具上增量扩展”：

1. 直接复用 `PIPE` 的 GUI、`DataLayer` 与 `PNML`。
2. 新增的数据类型、token 与 formula 逻辑都挂在同一底座上。
3. 这比从零实现高层网工具更现实，也更便于后续共享和扩展。

## 配套基础设施

- 建模/编辑工具：基于 `PIPE` 的图形 editor，新增 place data type、token 编辑、transition formula 与 arc variable UI。
- 解析/交换/元模型支持：扩展后的 `DataLayer`、`DataType`、`Token`、`abToken` 类与 `PNML` 存储链路。
- 仿真/执行支持：高层网 simulator、symbol table、parser/interpreter 与 locality-based scheduler。
- 验证/分析支持：基本 simulation 已有，但 integrated analysis module 仍缺。
- 代码生成/转换支持：原文未涉及代码生成；重点是编辑与仿真。
- 标准化或社区生态：基于开源 `PIPE`，并且 `PIPE+` 本身被描述为 open source，可供社区继续扩展。

## 适用场景与需求前提

### 适用场景

适合需要同时表达并发资源流和结构化数据对象的系统，如协议、信息系统、事务流与一般离散并发软件模型。

### 需求前提

1. 系统仍能抽成 Petri 网式 token/marking 语义。
2. token 数据结构可用有限个 `string/integer` 字段表达。
3. 守卫逻辑能压进受限一阶逻辑。
4. 当前目标更偏建模与仿真，而不是成熟验证后端。

### 不适用或高成本场景

如果必须支持复杂类型系统、嵌套集合、严格 true concurrency 语义或 timed Petri nets，当前 `PIPE+` 版本就不够。

## 与相邻形式主义的关系

相对 [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md)，`PIPE+` 更贴近“标准 high-level Petri nets 的受限可执行子集”，而 `CPN Tools` 更成熟也更偏 coloured nets；相对 [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)，本文讲的是编辑/仿真工具而不是交换标准；相对 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md) 与 [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)，它强调的是高层数据表达，而不是时间或随机分析。

## 与本研究的关系

### 对 Project 1 的价值

它补了一个很关键的事实：若后续想把需求中的对象、数据和值域一起压进网模型，仅有低层网远远不够，必须考虑 high-level token 与公式解释器。

### 作为目标形式主义还是中间表示

更适合作为数据驱动并发逻辑的中间表示或专题目标表示，而不是所有控制系统需求的统一终态。

### 对需求到模型生成的启发

1. 生成高层网时不能只吐 place/transition 结构，还要吐 token schema、arc variable 和 transition formulas。
2. 若需求里对象身份和字段值很重要，高层 Petri 网会比低层网更自然。
3. 真实落地需要考虑解释器、调度器和图形建模交互，而不只是数学定义。

### 现实限制

当前工具原型在分析能力和类型能力上都还有限，更像一个高层网可执行锚点，而不是成熟工业级平台。

## 重要的相关工作

- [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md)：成熟 `CPN` 工具链，对比 `PIPE+` 更工业化。
- [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)：Petri 网交换格式标准线。
- [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：时间网分析环境，对比 `PIPE+` 更偏 time semantics 而非高层 token 数据。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
