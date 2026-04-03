# Contract Automata 的运行时环境 / A Runtime Environment for Contract Automata

## 基本信息

- 标题：A Runtime Environment for Contract Automata
- 中文标题：Contract Automata 的运行时环境
- 作者：Davide Basile, Maurice H. ter Beek
- 发表：*Formal Methods*, pp. 550-567, 2023
- DOI：`10.1007/978-3-031-27481-7_31`
- 链接：https://doi.org/10.1007/978-3-031-27481-7_31
- 形式主义：`Contract Automata / CARE`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：运行时实现 / orchestration engine
- 工具/实现获取方式：原文明确给出 `CARE`、`CATLib`、`CATApp` 与对应 GitHub 链接；运行时基于 `Java` 与 `TCP/IP sockets`。
- 标准/格式获取方式：承载方式是 contract automata、typed labels、`CARE` 的 orchestration / service classes 与 `Uppaal` runtime model；原文未给行业标准交换格式。

## 简报

这篇论文的重要性在于，它补上了 contract automata 研究里长期缺的一环：如何把已经综合出来的 orchestration 真正落成运行中的服务协作环境。`CARE` 不是再定义一个新的契约自动机，而是把 `CATLib/CATApp` 里静态得到的 contract automata composition 和 orchestration，接到实际服务的低层消息交互上，并给出“实现遵守契约”的形式保证。

- 形式主义定位：面向 contract automata 应用落地的运行时环境，而不是新的接口理论。
- 构造方式简述：先用 `CATLib` 得到 non-empty orchestration，再由 `CARE` 的 orchestrator / orchestrated services 执行它，动作可走 centralised 或 distributed 实现。
- 基础设施与场景简述：依托 `CARE`、`CATLib`、`CATApp`、`Java sockets` 和 `Uppaal` 模型，服务 contract-based applications、service orchestration 和 runtime correctness。

```text
contract automata specification -> composition / synthesis in CATLib -> orchestration automaton -> CARE runtime -> 受控服务交互执行
```

## 形式主义定义与核心对象

### 定义对象

论文一方面复用了 `Modal Service Contract Automata (MSCA)`，另一方面引入了运行时对象：

1. `MSCA` 作为行为规格。
2. synthesised orchestration automaton。
3. `RunnableOrchestratedContract`，即带契约包装的服务。
4. `RunnableOrchestration`，即运行时 orchestrator。
5. centralised / distributed actions 与 dictatorial / majoritarian choices。

### 核心抽象

论文首先回顾 `MSCA`：

$$
A = \langle Q, \vec{q}_0, A^r, A^o, T, F \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `\vec{q}_0` 是初始状态。
3. `A^r` 是 request actions 集合。
4. `A^o` 是 offer actions 集合。
5. `T` 是转移集合，并区分 permitted 与 necessary transitions。
6. `F` 是终态集合。

论文进一步给出抽象综合的固定点框架。可保守写成：

$$
f_{\varphi_p,\varphi_f}(K_{i-1}, R_{i-1}) = (K_i, R_i)
$$

其中：

1. `K_i` 是第 `i` 次迭代后的候选 controller / orchestration。
2. `R_i` 是当前被判定为 forbidden 的状态集合。
3. `\varphi_p` 决定哪些 transitions 该被 pruning。
4. `\varphi_f` 决定哪些 states 该被判为 forbidden。

到运行时层，论文的真正新增对象是可执行服务封装。可保守整理成：

$$
\mathcal{R} = (\mathcal{O}, \mathcal{S}, \mathcal{A}, \mathcal{C})
$$

上式中的符号逐项解释如下：

1. `\mathcal{O}` 是 orchestration automaton。
2. `\mathcal{S}` 是实现各 principal contract 的运行中服务集合。
3. `\mathcal{A}` 是 centralised / distributed action 实现策略。
4. `\mathcal{C}` 是 choice 策略，如 dictatorial 或 majoritarian。

### 一个最小例子与通俗解释

论文给了两个很直观的例子。最小的一个是 `Alice and Bob`：

1. `Alice` 提供 `euro/dollar`，随后请求 `coffee/tea`。
2. `Bob` 提供与之对偶的动作。
3. `CATLib` 先综合出二者的 safe orchestration。
4. `CARE` 再把这个 orchestration 变成真实的 socket 消息交互和 Java method invocation。

通俗地说，如果 contract automata 告诉你“哪些服务动作应该怎样匹配”，那 `CARE` 就是把这张自动机契约图变成真正会跑的 runtime coordinator。

### 运行 / 接受 / 转移语义

论文在运行时层给了两套算法：orchestration 线程与 service 线程。其核心控制流可保守写成：

$$
cs_{i+1} = \mathrm{targetState}(tr_i)
$$

上式中的符号逐项解释如下：

1. `cs_i` 是当前状态。
2. `tr_i` 是本轮选择的 transition。
3. `\mathrm{targetState}` 把系统推进到该 transition 的目标状态。

运行时安全依赖于“当前执行的 transition 必须来自 orchestration 的 forward star”。可保守写成：

$$
tr_i \in \mathrm{forwardStar}(cs_i)
$$

若不满足，就会抛出异常，说明低层实现偏离了契约。

而静态正确性则来自综合后的 orchestration 性质：

$$
\mathcal{O} = \mathrm{synth}(A_1 \otimes \cdots \otimes A_n)
$$

上式中的符号逐项解释如下：

1. `A_1,\ldots,A_n` 是各个服务的 contract automata。
2. `\otimes` 是 composition。
3. `\mathrm{synth}` 表示 synthesis operation。
4. `\mathcal{O}` 是被 `CARE` 执行的 orchestration automaton。

论文还用 `Uppaal` 对 socket-level interaction model 建模，以验证 centralised/distributed actions 和 choice 机制不会破坏运行时协议。

### 语义边界

这篇论文的边界很清楚：

1. 它并不改变 contract automata 的抽象语义主体，而是补 runtime realization。
2. 运行时正确性建立在前置条件“orchestration 已正确综合”之上。
3. 重点是服务间低层交互和责任划分，不是大规模服务发现问题。
4. `CARE` 是运行时环境，不负责解决 contract synthesis 的 state explosion。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| MSCA 骨架 | `$A = \langle Q, \vec{q}_0, A^r, A^o, T, F \rangle$` | 运行时仍然建立在 contract automata 规格之上。 |
| 抽象综合 | `$f_{\varphi_p,\varphi_f}(K_{i-1}, R_{i-1}) = (K_i, R_i)$` | `CATLib` 通过固定点综合 orchestration。 |
| runtime 骨架 | `$\mathcal{R} = (\mathcal{O}, \mathcal{S}, \mathcal{A}, \mathcal{C})$` | orchestration、services、action 策略与 choice 策略共同组成 `CARE`。 |
| 运行推进 | `$cs_{i+1} = \mathrm{targetState}(tr_i)$` | runtime 每一步都沿 orchestration transition 前进。 |
| 合法执行 | `$tr_i \in \mathrm{forwardStar}(cs_i)$` | 运行时只允许执行契约当前允许的动作。 |
| 综合入口 | `$\mathcal{O} = \mathrm{synth}(A_1 \otimes \cdots \otimes A_n)$` | 运行时协调器来自静态 contract synthesis。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | orchestration 与各 service contract 都是自动机。 |
| 事件 / 触发 | 强支持 | request / offer / match 最终被映射成 runtime action。 |
| 守卫 / 数据 | 部分支持 | typed labels 处理参数/返回值类型，但主体仍是行为契约。 |
| 层次 | 部分支持 | 运行时类结构分层明显，但形式主义主体仍是平面 automata 组合。 |
| 并发 / 同步 | 强支持 | 多服务并发与 orchestrator 协调是核心。 |
| 时间约束 | 弱支持 | 论文用 `Uppaal` 验证 runtime interactions，但主形式主义不是 timed model。 |
| 连续动态 / 随机性 | 不支持 | 纯离散服务交互。 |
| 可执行 / 可验证性 | 强执行、强验证 | 既能执行，又给出 `Uppaal` 级别的 interaction correctness 证明。 |

### 形式化问题与性质

1. 论文真正补的是“从契约自动机到运行时环境”的最后一公里。
2. `typed labels` 使 contract action 不再只是抽象名字，而能约束参数和返回值兼容性。
3. `CARE` 把原本抽象掉的 orchestrator / service 低层交互显式化了。
4. 相比纯 synthesis 论文，它直接回答“怎么把综合结果运行起来并保证不偏离规格”。

## 构造方式与承载格式

### 建模入口

建模与实现入口通常是：

1. 用 `CATApp` / `CATLib` 定义并组合 contract automata。
2. 综合得到 non-empty orchestration。
3. 用 `CARE` 的 `RunnableOrchestratedContract` 包装具体服务实现。
4. 用 `RunnableOrchestration` 驱动整体应用执行。

### 机器可处理承载方式

原文直接给出的机器可处理承载方式包括：

1. `CATLib`/`CATApp` 中的 automata models。
2. `CARE` 的 Java classes。
3. `TypedCALabel`，即带参数类型和返回值类型的契约标签。
4. `Uppaal` 中的 runtime interaction model。

### 交换与互操作

互操作重点在：

1. 服务实现通过 Java interface 与 contract actions 对齐。
2. centralised / distributed 两种 action 实现允许不同部署方式。
3. 同一组服务可在不同 requirements 下被重新综合、重新编排。

## 配套基础设施

- 建模/编辑工具：`CATLib`、`CATApp`。
- 解析/交换/元模型支持：`TypedCALabel` 扩展了 contract labels 的类型信息。
- 仿真/执行支持：`CARE` 直接承担运行时协调。
- 验证/分析支持：静态上由 `CATLib` 综合保证 agreement；动态交互由 `Uppaal` 模型验证。
- 代码生成/转换支持：不是传统代码生成，而是把既有服务适配到受控 runtime。
- 标准化或社区生态：主要依托作者团队工具链和 GitHub 开源实现。

## 适用场景与需求前提

### 适用场景

适合 contract-based applications、service orchestration、分布式服务协作和想把形式契约真正跑起来的系统。

### 需求前提

1. 服务交互能先被建模为 contract automata。
2. 系统愿意引入 orchestrator 或 orchestration-aware runtime。
3. 服务接口可以通过方法与参数类型映射到 contract actions。
4. 前置的 synthesis 结果是 non-empty 且满足 agreement 的。

### 不适用或高成本场景

如果服务实现完全不可改、协议发现高度动态、或系统无法接受 orchestrator / runtime wrapper，这类 contract-aware runtime 很难直接落地。

## 与相邻形式主义的关系

相对 [Contract Automata](../contract-automata/desc.md) 与 [Controller Synthesis of Service Contracts with Variability](../controller-synthesis-of-service-contracts-with-variability/desc.md)，本文补的是 runtime realization；相对 session types / typestate toolchain，它同样想把行为规格落地，但核心对象仍是 contract automata；相对 [Interface Automata](../interface-automata/desc.md)，它更偏合成后的执行遵循，而不是静态接口兼容。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文很关键，因为它说明“形式化状态机 / 契约模型”并不止于验证，也可以直接支撑运行时执行与 adherence 保证。

### 作为目标形式主义还是中间表示

在接口/契约驱动系统里，它更像“目标执行框架 + 中间表示桥梁”的组合：contract automata 仍是核心模型，`CARE` 则是将其落地的执行环境。

### 对需求到模型生成的启发

1. 如果未来要做“生成 - 验证 - 修复 - 执行”闭环，必须考虑模型如何接到 runtime，而不是只到 verification 就停。
2. 动作名之外，还应抽取参数类型和返回类型，才能进入 typed runtime。
3. 运行时异常（如 `ContractViolationException`）可作为反向修复证据进入闭环。

## 重要的相关工作

- [Contract Automata](../contract-automata/desc.md)：运行时仍然建立在这一静态形式主义之上。
- [Controller Synthesis of Service Contracts with Variability](../controller-synthesis-of-service-contracts-with-variability/desc.md)：展示 contract automata 在组合与 variability 侧的扩展。
- `Mungo` / `StMungo` / `JaTyC`：论文中明确对比过的行为类型落地工具链。

## 文献分类总结

- 这是一篇 `🔌` 类高价值应用条目，重点不在新契约模型，而在 contract automata 的可执行 runtime 落地。
- 其描述客体是服务接口与交互契约，因此记为 `🤝`；论文语境面向服务组合与分布式交互，因此记为 `🌐`。
- 对 `project_1` 来说，它补上了“接口/组合/契约模型如何进入执行闭环”的关键一环。
