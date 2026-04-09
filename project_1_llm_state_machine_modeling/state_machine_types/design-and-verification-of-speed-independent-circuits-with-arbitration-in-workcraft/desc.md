# Workcraft 中带仲裁的速度无关电路设计与验证 / Design and Verification of Speed-Independent Circuits with Arbitration in Workcraft

## 基本信息

- 标题：Design and Verification of Speed-Independent Circuits with Arbitration in Workcraft
- 中文标题：Workcraft 中带仲裁的速度无关电路设计与验证
- 作者：Danil Sokolov，Victor Khomenko，Alex Yakovlev，David Lloyd
- 发表：*2018 24th IEEE International Symposium on Asynchronous Circuits and Systems (ASYNC)*，pp. 30-31，2018
- DOI：`10.1109/ASYNC.2018.00017`
- 链接：https://doi.org/10.1109/ASYNC.2018.00017
- 形式主义：`Signal Transition Graphs / speed-independent circuits / mutex-aware Workcraft flow`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：以 `STG` 为前端、面向带仲裁 `SI` 电路的设计与验证工作流
- 工具/实现获取方式：原文直接给出 `Workcraft` 入口 `https://workcraft.org/`，并说明后端使用 `Petrify` 与 `MPSat` 完成综合与验证。
- 标准/格式获取方式：主承载是 `STG` 规格、mutex-place tagging、`Petrify/MPSat` synthesis backend；它不是中立交换标准。

## 简报

这篇论文补的是“异步电路 `STG` 规格如何安全地接入仲裁元件”这条基础设施线。它并没有提出新的状态机家族，而是把传统上需要人工 factoring-out 的 mutex 流程自动化：用户在 `STG` 中标记 mutex place，`Workcraft` 自动识别 request/grant 对、验证仲裁协议、综合剩余控制器，并把 mutex 自动插回结果电路。

- 形式主义定位：`STG` 驱动的异步电路设计/验证工作流，而不是新的 `STG` 母型。
- 构造方式简述：`STG + mutex place tag -> protocol checking -> factor-out -> Petrify/MPSat synthesis -> mutex reinsertion -> implementation verification`。
- 基础设施与场景简述：依托 `Workcraft`、`STG`、`Petrify`、`MPSat` 和 mutex protocol checks，服务 speed-independent asynchronous circuit design。

```text
STG 规格 -> 标记仲裁位置 -> 协议验证 -> 标准 SI 综合 -> 自动插入 mutex -> 实现级验证
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Signal Transition Graph (STG)` 规格。
2. mutex place 及 request/grant 信号对。
3. output-persistence 检查。
4. `Workcraft` 自动综合与验证流程。

### 核心抽象

论文没有显式把 `STG` 写成统一元组；以下写法是根据正文关于 places、signal transitions、initial marking 和信号标签的描述做的保守整理：

$$
N = (P, T, F, m_0, \ell)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合。
2. `$T$` 是 transitions 集合。
3. `$F$` 是 flow relation。
4. `$m_0$` 是初始标识。
5. `$\ell$` 把 transition 标成某个 signal 的上升/下降事件或内部事件。

论文的关键不是一般 `STG` 语义，而是 mutex-aware 协议约束。对 request/grant 对 `$(r_1,g_1)$` 与 `$(r_2,g_2)$`，文中明确要求在每个 reachable state 满足例如：

$$
r_1 \land g_2 \Rightarrow g_1'
$$

$$
r_2 \land g_1 \Rightarrow g_2'
$$

上式中的符号逐项解释如下：

1. `$r_i$` 是 mutex request 信号。
2. `$g_i$` 是对应 grant 信号。
3. `$g_i'$` 是该信号的 next-state value。
4. 这些公式确保 grant 的发放与 request/grant 组合关系满足仲裁协议。

论文还额外检查 critical sections 的互斥性：

$$
(r_1 \land g_1) \land (r_2 \land g_2)
$$

上式中的符号逐项解释如下：

1. 该式在论文中被作为应当避免的 suspicious initial situation 来检查。
2. 直觉上表示两个 critical sections 不应同时持有 grant。

### 一个最小例子与通俗解释

论文最小例子就是一个被标记为 mutex place 的选择点：

1. 用户在 `STG` 里把 choice place `me` 标成“这是仲裁，不是普通 output-persistence 违例”。
2. 工具自动在周边识别出 request/grant 对，比如 `(r_1,g_1)` 和 `(r_2,g_2)`。
3. 之后 `g_1` 与 `g_2` 之间的 choice 不再被当成普通非持久性错误。
4. 但如果 request 过早撤回导致 grant 被非法禁用，工具仍会抓到。

通俗地说，这条工作流相当于把“人工把 mutex 挖出去再塞回来”的老做法，收缩成“在 `STG` 里做一个语义标签，然后自动跑完剩下的流程”。

### 运行 / 接受 / 转移语义

论文的执行流程可以概括为：

1. 用户提供带 mutex-place tag 的 `STG`。
2. `Workcraft` 在 output-persistence 检查时，对 grant-choice 做 special treatment。
3. 工具验证 request/grant 是否满足 early-release 或 late-release arbitration protocol。
4. 然后 factor out mutex、调用 `Petrify` 或 `MPSat` 综合剩余控制器，并自动把 mutex 加回。

### 语义边界

1. 论文聚焦 speed-independent circuits with arbitration，不是一般异步电路全景。
2. 它的核心条件是某对非持久信号必须真的可由 mutex 实现。
3. 支持 early release 与 late release 两种协议，但不意味着任意不持久性都能自动合法化。
4. 文章本身很短，重点在 flow automation，而不是完整 `STG` 理论重述。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 保守 `STG` 骨架 | `$N=(P,T,F,m_0,\ell)$` | 工作流的输入对象。 |
| grant 协议约束 | `$r_1 \land g_2 \Rightarrow g_1'$` 等 | 检查某 choice 是否可由 mutex 正确实现。 |
| critical-section 互斥 | `$(r_1 \land g_1) \land (r_2 \land g_2)$` | 初始与运行状态都不应出现双占用。 |
| synthesis flow | `STG -> factor out -> Petrify/MPSat -> mutex insertion` | 自动化设计与验证链。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 状态主要由 `STG` marking 与信号值组合体现。 |
| 事件 / 触发 | 很强 | signal rising/falling transitions 是核心。 |
| 守卫 / 数据 | 弱支持 | 重点不是富数据，而是仲裁协议与持久性。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 很强 | `STG` 本质上是并发/因果网模型。 |
| 时间约束 | 不支持 | speed-independent 关心相对时序与持久性，不用显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散异步控制逻辑。 |
| 可执行 / 可验证性 | 很强 | 协议检查、综合和实现验证全自动串起来。 |

### 形式化问题与性质

1. 论文核心不在 `STG` 本体，而在 mutex-aware verification/synthesis flow。
2. 它把原本容易出错的手工 factoring-out 变成了工具内闭环。
3. 对 grant 的“特殊允许”和“仍然检查 request premature withdrawal”这一组合很关键，避免把错误静默吞掉。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `STG` 规格。
2. 对某些 choice places 加 mutex tag。
3. request/grant 对的自动识别。
4. `Petrify` 或 `MPSat` 后端综合。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `STG` 模型。
2. mutex-place 标记。
3. 仲裁协议约束检查。
4. 综合后的电路与插回的 mutex。

### 交换与互操作

1. 论文主线是 `Workcraft` 内部流，不强调跨工具中立交换格式。
2. 互操作主要发生在 `Workcraft -> Petrify/MPSat` 后端层。
3. 输出既包括综合结果，也包括对环境组合后的实现验证。

## 配套基础设施

- 建模/编辑工具：`Workcraft`。
- 解析/交换/元模型支持：`STG` 输入、mutex-place tagging、环境组合处理。
- 仿真/执行支持：重点不是仿真，而是异步电路综合与协议验证。
- 验证/分析支持：output-persistence、deadlock freedom、environment conformance、mutex protocol checking。
- 代码生成/转换支持：factor-out + `Petrify/MPSat` synthesis + mutex reinsertion。
- 标准化或社区生态：依附 `Workcraft` 的异步电路设计生态，与 `Petrify/MPSat` 明确联动。

## 适用场景与需求前提

### 适用场景

适合那些用 `STG` 描述异步控制器、又确实需要仲裁元件处理非持久 choice 的 speed-independent circuit design 场景。

### 需求前提

1. 设计已能自然表成 `STG`。
2. 某些非持久 choice 真的是 mutex 语义，而不是规格错误。
3. request/grant 对能被工具从局部结构中稳定识别。
4. 团队接受 `Workcraft + Petrify/MPSat` 这条综合流。

### 不适用或高成本场景

1. 若设计并不落在 `STG` / asynchronous circuit 语境，这条流不合适。
2. 若 choice 的真实原因不是仲裁，而是更复杂的协议失配，mutex tagging 不能替代重新建模。
3. 若后端不允许依赖 `Petrify` / `MPSat` 生态，收益会明显下降。

## 与相邻形式主义的关系

相对传统“手工 factoring-out mutex”的 `STG` 设计流程，这篇论文把仲裁变成一等工作流对象；相对文库里的 `Supremica -> PLC`、`CIF 3/ESCET` 这类 supervisory-control toolchain，它面对的是异步电路 `STG`；相对 `Renew`、`Snoopy` 这类 Petri 网工作台，它更接近 `STG` 异步综合而非一般并发系统建模。

## 与本研究的关系

### 对 Project 1 的价值

它说明当某类状态机/并发网模型真正进入工程实施阶段时，“工具是否能把某类语义例外安全地工具化”非常关键。对 `project_1` 来说，这类条目能帮助区分“形式主义存在”与“形式主义可被工程化使用”之间的差异。

### 可复用启发

1. 对带局部冲突或仲裁语义的控制模型，最好把“特殊合法冲突”显式建成 profile/tag，而不是靠人工约定。
2. 自动识别接口对并追加协议检查，比简单放宽验证条件更可靠。
3. 这类“tag + backend specialization”思路可以迁移到别的状态机家族。

## 重要的相关工作

1. `Signal Transition Graphs (STG)`：整条工作流的形式化前端。
2. `Petrify`：异步控制器综合后端。
3. `MPSat`：异步逻辑综合与验证后端。
4. asynchronous arbitration primitives / mutex theory：本文协议检查的直接背景。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这篇论文最适合作为“`STG` 异步电路仲裁综合与验证基础设施”条目保留。它不新增主树节点，但能明显补强 `Workcraft` 在 `STG` / asynchronous-circuit 工具生态中的静态挂接口径。
