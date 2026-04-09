# 定时性质监测再审视 / Monitoring Timed Properties (Revisited)

## 基本信息

- 标题：Monitoring Timed Properties (Revisited)
- 中文标题：定时性质监测再审视
- 作者：Thomas Møller Grosen，Sean Kauffman，Kim Guldstrand Larsen，Martin Zimmermann
- 发表：*Formal Modeling and Analysis of Timed Systems*，pp. 43-62，2022
- DOI：`10.1007/978-3-031-15839-1_3`
- 链接：https://doi.org/10.1007/978-3-031-15839-1_3
- 形式主义：`MITL / Timed Büchi Automata / MoniTAal`
- 主类：⏱️ 时间 / 时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`MITL / TBA` 在线监测与 `MoniTAal` 区域化运行时验证路线
- 工具/实现获取方式：原文明确给出 `MoniTAal` 仓库 `https://github.com/DEIS-Tools/MoniTAal` 与 `PARDIBAAL` 仓库 `https://github.com/DEIS-Tools/PARDIBAAL`。
- 标准/格式获取方式：输入是互为否定的两台 `Timed Büchi Automata`，上游可由 `MITL` 公式翻译得到；输出是三值 verdict `⊤ / ⊥ / ?`。

## 简报

这篇论文补的不是新的 timed-automata 语言，而是一条比较完整的 `MITL / Timed Büchi Automata -> zone-based online monitoring` 路线。它把“在线监测无限 timed traces、考虑 time divergence、再叠加 timing uncertainty”三件事放进同一个符号化过程里，并给出 `MoniTAal` 原型。

- 形式主义定位：围绕 `MITL / TBA` 的在线监测方法路线，而不是新的模型本体。
- 构造方式简述：`MITL -> TBA -> 与 divergence automaton 求交 -> zone reach-set online update -> verdict`。
- 基础设施与场景简述：依托 `MoniTAal`、`PARDIBAAL`、`DBM/zones` 与 `Timed Büchi Automata`，适合实时 traces 的运行时验证与在线测试。

```text
timed property -> MITL / TBA -> symbolic reach-set update -> timed-divergence / uncertainty aware verdict
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `MITL` 公式。
2. `Timed Büchi Automata (TBA)`。
3. 在线监测 verdict 语义 `⊤ / ⊥ / ?`。
4. 考虑 time divergence 的 verdict 函数。
5. 基于 zones 的可达集与非空语言状态集合。

### 核心抽象

论文直接给出 `MITL` 语法：

$$
\varphi ::= p \mid \neg \varphi \mid \varphi \lor \varphi \mid X_I \varphi \mid \varphi \ U_I \ \varphi
$$

上式中的符号逐项解释如下：

1. `$p$` 是字母表中的命题符号。
2. `$I$` 是定义在 `$R_{\ge 0}$` 上的非奇点时间区间。
3. `$X_I$` 是带时间约束的 next。
4. `$U_I$` 是带时间约束的 until。

论文使用的自动机骨架是：

$$
A = (Q, Q_0, \Sigma, X, \Delta, F)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是 location 集合。
2. `$Q_0$` 是初始 location 集合。
3. `$\Sigma$` 是输入字母表。
4. `$X$` 是 clocks 集合。
5. `$\Delta$` 是带 guard 与 reset 的迁移集合。
6. `$F$` 是接受 location 集合。

在线 verdict 的核心定义是：

$$
V(\phi)(\rho, t) =
\begin{cases}
\top & \text{if } \rho \cdot_t \mu \in \phi \text{ for all } \mu \in T_\Sigma^\omega, \\
\bot & \text{if } \rho \cdot_t \mu \notin \phi \text{ for all } \mu \in T_\Sigma^\omega, \\
? & \text{otherwise.}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$\rho$` 是当前已经观察到的有限 timed prefix。
2. `$t$` 是当前观察时刻，且 `$t \ge \tau(\rho)$`。
3. `$\mu$` 是任意未来无限 timed continuation。
4. `$\rho \cdot_t \mu$` 表示从时刻 `$t$` 接上未来 continuation。

论文进一步把现实中的 time divergence 编进 verdict：

$$
V_D(\phi)(\rho, t) =
\begin{cases}
\top & \text{if } \rho \cdot_t \mu \in \phi \text{ for all } \mu \in TD_\Sigma^\omega, \\
\bot & \text{if } \rho \cdot_t \mu \notin \phi \text{ for all } \mu \in TD_\Sigma^\omega, \\
? & \text{otherwise.}
\end{cases}
$$

这里的 `$TD_\Sigma^\omega$` 是所有 time-divergent timed words 的集合。原文的关键结论是：如果不把 time divergence 单独纳入 verdict 语义，就会对某些性质给出错误的在线结论。

### 一个最小例子与通俗解释

论文最直观的例子是 bounded response：

$$
\varphi = G_{\ge 0}(a \rightarrow F_{\le 30} b)
$$

它表示“每次观察到 `a` 之后，都必须在 30 个时间单位内观察到 `b`”。若当前 prefix 为 `(b,10),(a,20)`，那在 `t \le 50` 时仍可能通过未来的 `b` 满足性质，但当 `t > 50` 且还没看到响应，就已经能给出 `⊥`。

通俗地说，这个监测器像“盯着一条带时间戳的事件流跑的 timed-automata 裁判”。它不是看整个系统模型，只看当前 trace 是否已经足够证明“无论未来怎么补都满足”或者“无论未来怎么补都违反”。

### 运行 / 接受 / 转移语义

论文把 `MITL` 性质先翻成 `TBA`，再在 zone 图上做在线 successor 更新。它的 symbolic state 写成：

$$
(q, Z)
$$

其中：

1. `$q$` 是当前 automaton location。
2. `$Z$` 是一组满足 clock constraints 的 valuation zone。

定义 7 给出的关键 zone 操作之一是：

$$
Z[\lambda] = \{ v : \exists v' \in Z,\ v(x)=0 \text{ if } x \in \lambda,\ \text{otherwise } v(x)=v'(x) \}
$$

它表示对一组时钟 `$\lambda$` 执行 reset。在线 successor 则由 Algorithm 4 实现，可保守压缩成：

$$
\mathrm{Succ}_A^S(\sigma,\tau) = \{ (q', (Z^{\uparrow[\tau,\tau]} \land g)[\lambda]) \}
$$

上式中的符号逐项解释如下：

1. `$(q,Z)$` 是当前 symbolic state。
2. `$\sigma$` 是新到达的观测符号。
3. `$\tau$` 是该符号对应的时间点。
4. `$g$` 是迁移 guard。
5. `$\lambda$` 是迁移触发时需要 reset 的时钟集合。

最后，`MoniTAal` 用 reach-set 是否仍和非空语言状态集合相交来决定输出 `⊤ / ⊥ / ?`。

### 语义边界

1. 论文关注的是在线监测 / 在线测试，而不是通用 model checking。
2. 对象是 timed words 上的 `MITL / TBA` 性质，不是混成系统或概率时序模型。
3. `MoniTAal` 的核心输入是两台互为否定的 `TBA`，因此上游翻译链仍是重要前提。
4. timing uncertainty 在本文支持的是“带界限的时间观测误差”，不是一般 parametric timed automata 的全问题。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `MITL` 语法 | `$\varphi ::= p \mid \neg \varphi \mid \varphi \lor \varphi \mid X_I \varphi \mid \varphi U_I \varphi$` | 性质前端。 |
| `TBA` 骨架 | `$A=(Q,Q_0,\Sigma,X,\Delta,F)$` | 监测后端 automaton。 |
| 基本 verdict | `$V(\phi)(\rho,t)\in\{\top,\bot,?\}$` | 对有限 prefix 的三值解释。 |
| divergence-aware verdict | `$V_D(\phi)(\rho,t)$` | 排除时间收敛带来的错误 verdict。 |
| symbolic state | `$(q,Z)$` | zone-based reach-set 的基本单位。 |
| 在线 successor | `$\mathrm{Succ}_A^S(\sigma,\tau)$` | 每次观测后更新 reach-set。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 通过 `TBA` location 表达性质状态。 |
| 事件 / 触发 | 很强 | 监测对象本质上就是 timed event trace。 |
| 守卫 / 数据 | 弱支持 | 重点是 clocks 与时间区间，不是富数据状态。 |
| 层次 | 不适用 | 不是层次状态机路线。 |
| 并发 / 同步 | 弱支持 | 只在 trace 层面出现，不是并发模型主线。 |
| 时间约束 | 很强 | `MITL`、`TBA`、zones、timing uncertainty 都是核心。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 有 `MoniTAal` 原型与 `PARDIBAAL` 支撑。 |

### 形式化问题与性质

1. 这篇论文的核心，不是“离线判断一个固定 finite trace”，而是“在线判断当前 finite prefix 是否已经足够推出最终 verdict”。
2. 它把 `MITL -> TBA -> zone-based monitoring` 做成了可执行原型，并补上了 time divergence 与 timing uncertainty 这两个实际问题。
3. 对 `state_machine_types` 文库来说，它补的是 timed-automata 支线上的 runtime verification 路线，而不是新的 timed-automata 子类节点。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 先写 `MITL` 公式。
2. 再把公式翻成 `Timed Büchi Automata`。
3. 输入给 `MoniTAal` 的是正性质 automaton 和否性质 automaton。
4. 在线馈入 concrete 或 interval-timed observations。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `MITL` 公式。
2. `TBA`。
3. `zones / DBMs / federations`。
4. 在线观测日志或嵌入式库接口。

### 交换与互操作

1. `MoniTAal` 本身接收 `TBA`，因此和 `MITL` 前端之间通过 automata 翻译链衔接。
2. 论文实现依托 `PARDIBAAL` 处理 `DBM`，并把工业 gear controller trace 作为监测对象。
3. 这条路线和 `Uppaal TRON`、`Uppaal SMC` 在 timed verification 工具生态中是相邻但不同的 runtime 方向。

## 配套基础设施

- 建模/编辑工具：上游需要 `MITL` 或其他能导出 `TBA` 的前端。
- 解析/交换/元模型支持：`TBA` 输入、zones、`DBM` 与 federations。
- 仿真/执行支持：可作为在线库嵌入，也可直接监测日志。
- 验证/分析支持：`MoniTAal`、`PARDIBAAL`、非空语言状态计算、time-divergence 交集构造。
- 代码生成/转换支持：不做代码生成，重心是 monitor construction。
- 标准化或社区生态：与 `MITL` 翻译器、`Timed Automata` 工具链和 `DBM` 生态相连。

## 适用场景与需求前提

### 适用场景

适合对实时系统运行 traces 做在线验收、在线测试或运行时保障，尤其是需求本身已经能表达成 `MITL` 或 `TBA` 的场合。

### 需求前提

1. 关键性质要能落成 `MITL` 或 `TBA`。
2. 观测 trace 需要有时间戳，或至少有时间区间。
3. 团队接受三值在线 verdict，而不是只看最终离线结果。
4. 若存在 time divergence 或观测误差，就应显式启用本文对应语义。

### 不适用或高成本场景

若需求主要依赖复杂数据变量、连续动力学或难以转换成 `TBA` 的 rich specification，这条路线会变重。

## 与相邻形式主义的关系

它和传统 `UPPAAL` reachability / model-checking 关系很近，但对象不是完整系统模型，而是性质 automata 与运行 trace。相对纯离线 trace checking，它额外解决的是在线 verdict、time divergence 与 uncertainty；相对一般 `MITL` 翻译论文，它又往前走了一步，把 symbolic monitoring 直接落成工具。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提示 `project_1` 后续若输出的是 timed-state-machine family，不一定只能做离线验证，还能接 runtime monitoring。

### 作为目标形式主义还是中间表示

对 `project_1` 来说，`MITL / TBA` 更像验证侧中间表示与性质载体，不是需求到状态机生成的最终交付模型。

### 对需求到模型生成的启发

1. 若未来要做“生成 - 验证 - 运行期监测”闭环，性质生成必须考虑能否翻到 `MITL / TBA`。
2. 生成 timed 模型时，最好同时考虑 trace 级 monitorability，而不是只考虑一次性模型检查。
3. 对真实控制系统，time divergence 与 timing uncertainty 不能被当成边角条件。

### 现实限制

原文的工具输入仍是 automata，而不是任意高层 DSL；因此它更适合接在已有 timed verification 工具链之后，而不是直接做前端建模入口。

## 重要的相关工作

1. `Uppaal TRON`：同样是 timed online checking/testing 的重要工具锚点，但重心更偏 conformance testing。
2. `R2U2`、`MonPoly`：都属于 runtime verification 工具线，不过处理的逻辑与时间语义不同。
3. `Uppaal SMC` 中的 Weighted MTL 监测：论文明确提到希望未来用 `MoniTAal` 的 symbolic engine 替换其重写式实现。

## 文献分类总结

- 这篇论文应归入：⏱️ 时间 / 时钟自动机
- 这篇论文应归入：🛠️ 方法路线
- 这篇论文应归入：📝 序列 / 语言对象
- 这篇论文应归入：⏱️ 实时与嵌入式系统
- 作为 `state_machine_types` 条目，它补的是 timed-automata runtime verification 路线与 `MoniTAal` 工具锚点，不形成新的主树节点。
