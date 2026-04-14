# Strix：显式反应式综合再出击 / Strix: Explicit Reactive Synthesis Strikes Back!

## 基本信息

- 标题：Strix: Explicit Reactive Synthesis Strikes Back!
- 中文标题：Strix：显式反应式综合再出击
- 作者：Philipp J. Meyer，Salomon Sickert，Michael Luttenberger
- 发表：*Computer Aided Verification*，`LNCS 10981`，pp. 578-586，2018
- DOI：`10.1007/978-3-319-96145-3_31`
- 链接：https://doi.org/10.1007/978-3-319-96145-3_31
- 形式主义：`LTL reactive synthesis / DPA / parity games / Strix`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：explicit-state reactive-synthesis tool / on-the-fly `DPA`-parity route
- 工具/实现获取方式：原文明确给出入口 `https://strix.model.in.tum.de/`；实现采用 `Java + C++`，并可接外部 `MeMin`、`Speculoos`、`ABC`。
- 标准/格式获取方式：输入支持 `LTL` 与 `TLSF`；输出可为 `Mealy` 机或 `AIGER` 电路，不是中立行业标准。

## 简报

`Strix` 补的是 reactive synthesis 工具线里另一条非常重要的主干：它不再把公式先整体翻成一个大自动机再统一求解，而是把公式拆开、按 parity-game solver 真正需要的状态来 on-the-fly 地构造 `DPA`，再用显式多线程 parity-game 求解器和 strategy iteration 同步推进。这样既保持 automata-theoretic synthesis 的透明结构，又尽量削弱中间自动机爆炸。

- 形式主义定位：围绕 `LTL` 综合的显式 `DPA/parity-game` 方法路线与工具载体。
- 构造方式简述：`LTL/TLSF -> formula splitting -> on-the-fly DPA -> explicit parity game -> strategy iteration -> Mealy/AIGER`。
- 基础设施与场景简述：依托 `Java + C++`、`MeMin`、`Speculoos`、`ABC` 与 `SYNTCOMP` benchmark，服务 reactive controller synthesis 与硬件/控制器电路生成。

```text
LTL/TLSF specification -> decomposed formulas -> on-the-fly deterministic parity automata -> parity game -> winning strategy -> Mealy machine / AIGER circuit
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTL` reactive synthesis；
2. deterministic parity automata (`DPA`)；
3. parity games；
4. strategy iteration；
5. `Mealy` / `AIGER` controller generation。

### 核心抽象

论文虽然是工具论文，但核心对象非常清楚：先把 `LTL` 公式变成 `DPA`，再把多个 automata 组合成 parity game。可保守整理为：

$$
\mathcal{A} = (Q, \Sigma, q_0, \delta, \Omega)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是 `DPA` 状态集合。
2. `$\Sigma$` 是输入/输出字母表。
3. `$q_0$` 是初始状态。
4. `$\delta : Q \times \Sigma \to Q$` 是确定转移函数。
5. `$\Omega : Q \to \mathbb{N}$` 是 parity priority 标号。

组合后得到的博弈对象可保守写成：

$$
G = (V_0, V_1, E, \Omega)
$$

上式中的符号逐项解释如下：

1. `$V_0$` 与 `$V_1$` 分别是系统玩家与环境玩家的结点集合。
2. `$E \subseteq (V_0 \cup V_1) \times (V_0 \cup V_1)$` 是边集合。
3. `$\Omega$` 在博弈结点上继承 parity priority。
4. `Strix` 的 solver 在部分 arena 上即可开始策略迭代，不必等整个博弈一次性构完。

最终输出实现可再次落成 `Mealy` 机：

$$
M = (S, s_0, \Sigma_I, \Sigma_O, \delta_M, \lambda)
$$

上式中的符号逐项解释如下：

1. `$S$` 是控制器状态集合。
2. `$\Sigma_I$` 与 `$\Sigma_O$` 是输入、输出字母表。
3. `$\delta_M$` 是读取输入后的状态迁移函数。
4. `$\lambda$` 给出状态上的输出。
5. 工具也可进一步把它转成 `AIGER` 电路。

### 一个最小例子与通俗解释

论文用仲裁器和 `AMBA` 规格做例子最典型。一个最小直觉版可以写成：

1. 环境输入 `req_0, req_1` 表示两个客户端发起请求。
2. 系统输出 `grant_0, grant_1` 表示向哪个客户端授权。
3. 规格要求“任何时刻最多授权一个客户端，且持续请求最终会被响应”。
4. `Strix` 会把这些要求拆成 safety / co-safety / 其余一般 `LTL` 部分，再按需构造 automata 和 parity game。

通俗地说，`Strix` 像一个“按需展开的综合器”：它只在求解器真正问到的时候，才把对应公式片段翻成自动机状态，而不是先把所有可能状态一口气建出来。

### 运行 / 接受 / 转移语义

论文把综合链路明确描述为四步：

$$
\varphi \Rightarrow \{\mathcal{A}_1,\ldots,\mathcal{A}_n\} \Rightarrow G \Rightarrow M
$$

上式中的符号逐项解释如下：

1. `$\varphi$` 是输入的 `LTL/TLSF` 规格。
2. `$\{\mathcal{A}_1,\ldots,\mathcal{A}_n\}$` 是拆分后、按需构造的若干 `DPA`。
3. `$G$` 是组合后的 parity game。
4. `$M$` 是从 winning strategy 抽取出来的 `Mealy` 机。

论文还特别强调 non-deterministic strategy iteration 的价值：在 parity-game 阶段允许策略暂时保留多个可行动作，后续再用这些 “don't care” 空间做 `Mealy/AIGER` 最小化。

### 语义边界

1. `Strix` 仍然是 automata-theoretic `LTL` synthesis，不是通用定量博弈综合器。
2. 优势建立在公式可拆分以及 on-the-fly `DPA` 明显减少无用状态的前提上。
3. 工具高度依赖 parity-game solver 与后续电路最小化链路。
4. 不是显式时钟或混成控制器综合工具。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `DPA` 骨架 | `$\mathcal{A} = (Q,\Sigma,q_0,\delta,\Omega)$` | `Strix` 的直接目标中间表示。 |
| parity game 骨架 | `$G = (V_0,V_1,E,\Omega)$` | 综合问题实际求解对象。 |
| 综合链路 | `$\varphi \Rightarrow \{\mathcal{A}_i\} \Rightarrow G \Rightarrow M$` | 论文四步核心流程。 |
| 输出控制器 | `$M = (S,s_0,\Sigma_I,\Sigma_O,\delta_M,\lambda)$` | 最终返回的可执行实现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 输出为有限状态 `Mealy` 控制器或等价电路。 |
| 事件 / 触发 | 很强 | 输入/输出字母表是 reactive synthesis 主轴。 |
| 守卫 / 数据 | 弱支持 | 主要是命题逻辑级离散接口。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 通过交互式 reactive game 表达系统/环境对抗。 |
| 时间约束 | 不支持 | 不是 timed synthesis。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic 路线。 |
| 可执行 / 可验证性 | 很强 | 可输出 `Mealy` 或 `AIGER`，并能用 `SYNTCOMP` benchmark 验证。 |

### 形式化问题与性质

1. `Strix` 的代表性在于把显式 `DPA` 和显式 parity-game solver 做成了真正可竞争的综合器。
2. on-the-fly `DPA` 是关键，因为它让“显式方法”重新具有工程可行性。
3. strategy iteration 保留的 nondeterminism，还能反过来服务后续控制器最小化。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `LTL` 公式；
2. `TLSF` 规格；
3. formula splitting；
4. optional `Mealy/AIGER` 输出链路。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `LTL/TLSF` 输入；
2. on-the-fly `DPA`；
3. explicit parity game arena；
4. `Mealy` 机与 `AIGER` 电路。

### 交换与互操作

1. 支持 `TLSF`，便于直接接 `SYNTCOMP` 规格。
2. 可把 winning strategy 导出为 `Mealy` 机或 `AIGER`。
3. 依赖 `MeMin`、`Speculoos`、`ABC` 做后处理与最小化。

## 配套基础设施

- 建模/编辑工具：核心是 `Strix` 命令行 / 在线入口。
- 解析/交换/元模型支持：`LTL`、`TLSF`、`DPA` 和 parity game 中间层。
- 仿真/执行支持：输出 `Mealy` / `AIGER` 后可进入下游执行或验证工具。
- 验证/分析支持：realizability、synthesis、benchmark comparison、strategy iteration。
- 代码生成/转换支持：`Mealy` 到 `AIGER` 的转换与最小化是论文重点之一。
- 标准化或社区生态：`Java + C++` 主实现，外接 `MeMin`、`Speculoos`、`ABC`。

## 适用场景与需求前提

### 适用场景

适合 reactive controller synthesis、仲裁器 / 总线协议综合、硬件控制逻辑生成，以及希望保留 automata-theoretic 透明结构的 `LTL` 综合场景。

### 需求前提

1. 需求需能写成 `LTL` 或 `TLSF`。
2. 输入 / 输出接口必须是有限离散字母表。
3. 团队接受 parity-game 中间层以及外部 minimization 工具链。
4. 若目标是大规格，最好能从公式分裂中受益。

### 不适用或高成本场景

若需求只需 `GR(1)` 片段，专门工具可能更轻；若目标涉及时钟、连续动力学或定量 payoff，`Strix` 不是直接后端。

## 与相邻形式主义的关系

相对 [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)，`Acacia+` 走安全博弈与 antichain 路线，`Strix` 则走 on-the-fly `DPA + parity game` 路线；相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 专注 `GR(1)` 子片段，而 `Strix` 直接处理一般 `LTL`；相对 [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md) 与 [rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md](../rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md)，后两者更偏 `LTL` 到 `omega`-automata 的翻译/操作，而 `Strix` 把这些自动机直接接到综合器链路上。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明从结构化时序需求直接走到控制器实现，在工具上已经有成熟且可对比的主流路线。
2. on-the-fly `DPA` 和 partial arena solving 的思想，对 LLM 生成后端的分步展开很有借鉴价值。
3. `Mealy/AIGER` 双输出也提示我们：研究里最好区分“逻辑控制器表示”和“最终部署表示”。

### 作为目标形式主义还是中间表示

更像综合后端与实现载体，而不是最终前端建模语言。

### 对需求到模型生成的启发

1. 若需求能稳定转成 `LTL/TLSF`，可以直接把状态机生成问题推进到“控制器生成”层。
2. 自动机与博弈的分层，让复杂需求能被拆成更小的求解单元。
3. 非确定 winning strategy 的保留，也提示后续代码生成阶段应留出最小化空间。

## 重要的相关工作

1. [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)：较早的 `LTL` safety-game synthesis 工具线。
2. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：`GR(1)` 片段上的工程化综合平台。
3. `BoSy`、`Party`、`ltlsynt`：论文实验中直接对比的几条主流综合路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`LTL reactive synthesis / DPA / parity games / Strix`
- 论文角色：explicit-state reactive-synthesis tool / on-the-fly `DPA`-parity route
- 归类理由：论文主体是 `LTL` 综合后端的工具与算法链，关键贡献在公式拆分、on-the-fly `DPA` 和显式 parity-game 求解，而不是新的状态机本体。
