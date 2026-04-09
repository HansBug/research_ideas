# 结合黑盒与白盒技术学习寄存器自动机 / Combining Black-Box and White-Box Techniques for Learning Register Automata

## 基本信息

- 标题：Combining Black-Box and White-Box Techniques for Learning Register Automata
- 中文标题：结合黑盒与白盒技术学习寄存器自动机
- 作者：Falk Howar，Bengt Jonsson，Frits Vaandrager
- 发表：*Computing and Software Science*，`LNCS 10000`，pp. 563-588，2019
- DOI：`10.1007/978-3-319-91908-9_26`
- 链接：https://doi.org/10.1007/978-3-319-91908-9_26
- 形式主义：`register automata learning / MAT / black-box + white-box integration`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：register-automata learning method / white-box enhanced active learning route
- 工具/实现获取方式：原文不是单一工具论文，但明确说明第 5.2 节的 register-automata learning framework 已在 `RAlib` 中实现，并把它放在 `LearnLib`/active automata learning 生态里讨论；论文未给出直接仓库链接。
- 标准/格式获取方式：原文不主打交换标准；主要承载方式是 data words、MAT-style queries、register automata 元组、guards/assignments 与 white-box information extraction。

## 简报

这篇论文的重点，不是再定义一种新的寄存器自动机，而是讨论如何把主动自动机学习从纯黑盒提升到“黑盒主线 + 白盒辅证”的混合路线。作者的判断很直接：当模型需要 guards、register assignments 和 richer theories 时，单靠 membership/equivalence queries 的代价会迅速失控，因此应该把 symbolic execution、static analysis 和 richer query interfaces 引进学习流程。

- 形式主义定位：围绕 `register automata` 的学习方法路线，而不是新的 `RA` 理论奠基论文。
- 构造方式简述：保留 `MAT`/active learning 的黑盒骨架，但在 guard inference、register discovery、counterexample finding 等环节引入 white-box information。
- 基础设施与场景简述：依托 `membership/equivalence queries`、`RAlib`、symbolic execution、static code analysis，服务带数据参数的软件组件模型学习。

```text
SUL + data alphabet -> MQ / EQ -> RA hypothesis -> white-box information extraction -> refined guards/registers -> learned RA
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织讨论：

1. active automata learning / `MAT`；
2. membership query 与 equivalence query；
3. register automata (`RA`)；
4. guards over parameters and registers；
5. assignments to registers；
6. white-box techniques，如 symbolic execution、static analysis。

### 核心抽象

论文明确回到 `MAT` 学习框架。可写成：

$$
\mathcal{L} = (\Sigma, SUL, MQ, EQ, H)
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是输入字母表或 data alphabet。
2. `SUL` 是 system under learning。
3. `MQ` 是 membership query 机制。
4. `EQ` 是 equivalence query 机制。
5. `$H$` 是当前学习得到的 hypothesis。

论文给出的寄存器自动机定义是：

$$
A = (L, l_0, X, \Gamma, \lambda)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 locations 集合。
2. `$l_0$` 是初始 location。
3. `$X$` 为每个 location 指派一组 registers。
4. `$\Gamma$` 是带 parameter、guard、assignment 的转移集合。
5. `$\lambda$` 把 location 映射到 accept/reject。

论文还给出一步运行语义。可直接写成：

$$
\langle l,\nu \rangle \xrightarrow{\alpha(d)} \langle l',\nu' \rangle
$$

上式中的符号逐项解释如下：

1. `$\langle l,\nu \rangle$` 是当前 `RA` 状态，由 location 和 register valuation 构成。
2. `$\alpha(d)$` 是带数据值 `$d$` 的输入符号。
3. 若存在转移 `\langle l,\alpha(p),g,\pi,l' \rangle` 且 guard 被满足，则可发生该步。
4. `$\nu'$` 由 assignment `$\pi$` 计算得到。

### 一个最小例子与通俗解释

论文用 priority-queue 风格的 `offer/poll` 例子说明 register automata 的学习难点。可以把最小例子理解成：

1. `offer(3)` 和 `offer(5)` 后，系统记住两个数据值。
2. 如果随后 `poll(3)` 被接受，而 `poll(4)` 被拒绝。
3. 学习器就必须推断：当前行为依赖“参数是否等于某个已存 register 值”，而不是只依赖离散控制状态。

通俗地说，普通有限自动机学习只需要猜“现在在哪个离散状态”，而寄存器自动机学习还得猜“之前记住了哪些数据值、接下来比较的是哪个值、守卫到底长什么样”。

### 运行 / 接受 / 转移语义

论文明确指出 `MQ` 与 `EQ` 是学习骨架。可写成：

$$
MQ : \Sigma^* \to O, \qquad EQ(H) \in \{\mathrm{yes}\} \cup CEX
$$

上式中的符号逐项解释如下：

1. `MQ` 对给定输入序列返回可观测输出或接受/拒绝结果。
2. `EQ(H)` 用于判断当前假设模型 `$H$` 是否等价于目标系统。
3. 若不是，则返回 counterexample `CEX`。
4. 论文的核心问题是：纯黑盒下，这些查询对富数据模型过于昂贵。

作者讨论的增强方向，可保守写成：

$$
\mathcal{L}^{+} = (\Sigma, SUL, MQ, EQ, WQ)
$$

上式中的符号逐项解释如下：

1. `WQ` 表示 white-box aided queries 或 white-box extracted facts。
2. 它们可能告诉学习器“哪些 registers 实际需要”“某个 guard 的结构长什么样”等。
3. 这是根据论文第 6 节对 richer queries 的讨论做的保守抽象。
4. 它体现的不是新模型，而是增强后的学习接口。

### 语义边界

这篇论文的边界主要有：

1. 主线不是工业级完整工具介绍，而是研究路线与问题框架梳理。
2. 白盒信息被当成增强学习的辅助手段，而不是替代黑盒学习。
3. 论文以 `register automata` 为主要论证载体，不覆盖所有 EFSM family。
4. 作者明确承认 richer theories、structured data 和 scalable EQ 仍是难点。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 学习骨架 | `$\mathcal{L} = (\Sigma, SUL, MQ, EQ, H)$` | 主动自动机学习的最小框架。 |
| `RA` 元组 | `$A = (L, l_0, X, \Gamma, \lambda)$` | 论文选定的目标模型家族。 |
| 一步运行 | `$\langle l,\nu \rangle \xrightarrow{\alpha(d)} \langle l',\nu' \rangle$` | guards 与 assignments 如何共同决定行为。 |
| 白盒增强 | `$\mathcal{L}^{+} = (\Sigma, SUL, MQ, EQ, WQ)$` | 作者提倡的黑盒 + 白盒混合路线。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 目标是 learning richer `RA/EFSM` 而非 plain `DFA`。 |
| 事件 / 触发 | 强支持 | `offer/poll` 这类 action 是学习入口。 |
| 守卫 / 数据 | 很强 | guards、registers、assignments 是论文主轴。 |
| 层次 | 不支持 | 主线不在层次状态机。 |
| 并发 / 同步 | 弱支持 | 论文主要讨论单组件学习。 |
| 时间约束 | 不支持 | timed learning 不是本文核心。 |
| 连续动态 / 随机性 | 不支持 | 纯离散数据参数系统。 |
| 可执行 / 可验证性 | 条件支持 | 依赖 `RAlib`、LearnLib 生态与外部白盒分析能力。 |

### 形式化问题与性质

1. 这篇论文最有价值的地方，是把“为什么纯黑盒在数据自动机上会卡住”讲得很清楚。
2. 它并不简单鼓吹白盒替代黑盒，而是主张保留黑盒抽象优势，再精准引入白盒信息。
3. 对本文库而言，它把 active automata learning 线从 `DFA/Mealy` 推到了 `RA/EFSM` 级别。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 把 SUL 暴露为可查询系统。
2. 用 data words 表达交互轨迹。
3. 对目标模型选择 `RA` 而不是 plain finite automata。
4. 再在 guard/register inference 处引入 white-box 辅助。

### 机器可处理承载方式

机器可处理承载方式包括：

1. data words；
2. `MQ/EQ` query traces；
3. `RA` tuples with guards and assignments；
4. `RAlib`-style learning framework；
5. symbolic execution / static analysis 提取的白盒信息。

### 交换与互操作

这条路线的互操作重点不在文件标准，而在学习接口：

1. 黑盒部分通过 `MQ/EQ` 与 SUL 交互。
2. 白盒部分通过 symbolic execution 或 static analysis 返回结构信息。
3. 二者在 hypothesis refinement 处会合。

## 配套基础设施

- 建模/编辑工具：不是图形编辑器，核心是 query-based learning framework。
- 解析/交换/元模型支持：data words、guards、assignments、register valuations。
- 仿真/执行支持：通过 membership/equivalence queries 与 SUL 交互。
- 验证/分析支持：conformance testing、counterexample processing、symbolic execution、static analysis。
- 代码生成/转换支持：不以生成代码为主，重点是从行为中学习可分析模型。
- 标准化或社区生态：依托 `LearnLib`、`RAlib`、MAT 学习理论与 automata learning 社区。

## 适用场景与需求前提

### 适用场景

适合带数据参数的软件组件、协议接口、API 序列和需要从实现中恢复 `RA/EFSM` 风格模型的场景。

### 需求前提

1. 系统必须可执行 `MQ/EQ` 风格查询。
2. 核心行为可压成 data words 与 registers/guards 结构。
3. 若要获得白盒收益，需要拿到可分析代码或可执行体。
4. 团队接受 learned model 作为抽象分析资产，而不是精确源码替代物。

### 不适用或高成本场景

如果系统没有稳定查询接口、数据理论过于复杂，或完全拿不到任何白盒信息，这条路线的收益会显著下降。

## 与相邻形式主义的关系

相对 [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)，`AALpy` 更像通用学习基础设施，而本文更聚焦 `RA/EFSM` 级别的学习难点；相对 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，`LearnLib` 是工具框架盘点，本文更像方法论扩展；相对 [towards-regular-languages-over-infinite-alphabets/desc.md](../towards-regular-languages-over-infinite-alphabets/desc.md)，后者讲 `RA` 本体与表达边界，本文讲如何把这类模型从实现中学出来。

## 与本研究的关系

### 对 Project 1 的价值

1. 它给 `project_1` 一个很重要的补充视角：状态机不一定只从需求里生成，也可以反过来从实现或仿真对象中学习出来，用于交叉验证。
2. 如果未来要做“需求生成模型”和“实现反推模型”的双向闭环，这篇论文正好提供了中间桥梁。
3. 它还提示：对带变量和数据守卫的状态机，单纯自然语言到模型并不够，后续可能需要白盒证据辅助修正。

### 作为目标形式主义还是中间表示

更适合作为中间验证资产和对照模型，而不是最终交付给控制工程师的首选前端形式。

## 重要的相关工作

1. [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)：主动自动机学习基础设施。
2. [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：active learning 框架生态盘点。
3. [towards-regular-languages-over-infinite-alphabets/desc.md](../towards-regular-languages-over-infinite-alphabets/desc.md)：寄存器自动机的本体与理论边界。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`register automata learning / MAT / black-box + white-box integration`
- 论文角色：register-automata learning method / white-box enhanced active learning route
- 归类理由：论文主体聚焦 `register automata` 学习方法，核心贡献是如何把白盒信息融入学习流程，而不是构建新的工具平台或提出新的 automata family。
