# 业务过程验证：模型检测与定时自动机的应用 / Business Process Verification: The Application of Model Checking and Timed Automata

## 基本信息

- 标题：Business Process Verification: The Application of Model Checking and Timed Automata
- 中文标题：业务过程验证：模型检测与定时自动机的应用
- 作者：Luis E. Mendoza Morales
- 发表：*CLEI Electronic Journal*, 17(2), Paper 2, 2014
- DOI：`10.19153/cleiej.17.2.2`
- 链接：https://doi.org/10.19153/cleiej.17.2.2
- 形式主义：`Timed Automata / BPMN-to-TA Network + CCTL`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：💻
- 论文角色：`BPMN` 业务过程验证 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL` 对由 `BPMN` 任务模型映射得到的 `TA-network` 做仿真与验证，但未提供独立公开仓库。
- 标准/格式获取方式：承载方式是 `BPMN` 图、`Timed Automata`、`TA-network` 与 `CCTL/UPPAAL` 查询；原文未给独立交换标准。

## 简报

这篇论文的核心，不是重新提出新的定时自动机理论，而是把一个长期存在的工程问题做成了清晰的形式化管线：`BPMN` 虽然适合业务分析师画流程，但没有足够精确的形式语义来做时序与并发验证；因此作者把 `BPMN` 中的 worker、任务、消息同步和时间窗口系统地映射成 `Timed Automata` 网络，再交给 `UPPAAL` 用 `CCTL` 风格性质做检查。

- 形式主义定位：这是 `Timed Automata` 在业务过程建模与验证中的应用型条目，重点在 `BPMN -> TA-network -> UPPAAL` 的落地链路。
- 构造方式简述：先把 `BPMN` 过程拆成若干 `BP-worker` 自动机，再通过 `c! / c?` 握手同步组合成 `TA-network`，最后用 `A[] not deadlock`、时间上界可达性等查询检查业务规则。
- 基础设施与场景简述：依托 `BPMN`、`Timed Automata`、`CCTL` 与 `UPPAAL`，服务 `CRM` 这类含消息交互、任务时长和 `QoS` 约束的业务过程验证。

```text
BPMN 业务过程 -> worker 级 TA -> parallel TA-network -> UPPAAL queries -> deadlock / QoS / deadline 验证
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `BPMN` 中的 pools、tasks、events、gateways 与 message flows。
2. 每个 `BP-worker` 对应的 `Timed Automaton`。
3. 由多个 worker 自动机构成的 `TA-network`。
4. `UPPAAL` 中的握手同步通道、clock guards、invariants 与 resets。
5. 用于表达业务时限与死锁性质的 `CCTL/UPPAAL` 查询。

### 核心抽象

论文给出的定时自动机定义是：

$$
A = \langle S, \Sigma, C, E, s_0 \rangle
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集合，对应业务任务模型中的控制位置。
2. `\Sigma` 是动作或字母表，通常对应 worker 之间的交互事件。
3. `C` 是时钟集合，用来记录活动持续时间与等待时间。
4. `E` 是边集合，每条边都带动作、guard 和 reset。
5. `s_0` 是初始状态。

原文对边的结构写成五元组 `\langle s, a, g, r, s' \rangle`，可保守整理为：

$$
\langle s, a, g, r, s' \rangle \in E
$$

上式中的符号逐项解释如下：

1. `s` 和 `s'` 分别是源状态与目标状态。
2. `a` 是动作。
3. `g \in B(C)` 是关于时钟集合 `C` 的布尔约束。
4. `r \subseteq C` 是该次迁移需要复位的时钟集合。
5. 只有当 `g` 满足时，自动机才能执行这条迁移。

为了表达业务过程中的并发 worker，论文使用 `TA-network`：

$$
TAN = A_1 \parallel \cdots \parallel A_n
$$

上式中的符号逐项解释如下：

1. `A_1,\dots,A_n` 是各个业务参与者对应的定时自动机。
2. `\parallel` 表示并行组合。
3. 组合后的系统既允许动作交错，也允许通过 `c! / c?` 进行握手同步。
4. 这正对应论文把多个 `BP-worker` 组成完整业务过程任务模型的做法。

论文还强调 timed trace 的语义，原文把一个时序动作序列写成：

$$
\xi = (t_1,a_1)(t_2,a_2)\cdots(t_i,a_i)\cdots,\quad t_i \le t_{i+1}
$$

上式中的符号逐项解释如下：

1. `a_i` 是第 `i` 个离散动作。
2. `t_i` 是该动作发生时的绝对时间戳。
3. `t_i \le t_{i+1}` 表示动作序列在时间上单调不减。
4. 业务过程的响应时间、等待时间和 `QoS` 约束就是在这些时序 trace 上检查的。

### 一个最小例子与通俗解释

论文给出的 `CRM` 例子很适合解释这种模型到底在做什么：

1. 当客户发起购买请求时，`Customer` 或 `Attention Channel` 相关 worker 会进入某个等待通信的状态。
2. 该状态上的时钟开始计时，例如“必须在 2 个时间单位内建立通信”。
3. 若另一个 worker 通过 `message flow` 对应的 `c! / c?` 成功同步，则系统转入已通信状态。
4. 若直到不变式上界前仍无法同步，就会出现 violation 或 deadlock 风险。

通俗地说，这种方法像“把流程图里每个工作人员都变成会计时的小状态机”，然后检查它们是否能在规定时间内把业务接力完成。

### 运行 / 接受 / 转移语义

论文明确指出定时自动机有两类基本迁移：

1. delay transition：系统只流逝时间，不改变离散位置。
2. action transition：某条 guard 已满足，于是执行带动作的边并可能复位时钟。

在网络语义下，最关键的是：

1. 多个 worker 自动机并行运行。
2. 共享动作通过 `c! / c?` 握手同步。
3. `UPPAAL` 在验证时按需构造 product automaton。
4. 业务规则被转成 `CCTL/UPPAAL` 查询，对整个 `TA-network` 做穷尽检查。

论文中实际使用的关键查询包括：

$$
A[]\ \neg deadlock
$$

以及：

$$
E\langle\rangle\ Product\_service.Prom\_inf \Rightarrow ta \le 44
$$

上式中的符号逐项解释如下：

1. `A[] \neg deadlock` 检查任何可达状态下都不存在死锁。
2. `E<>` 检查是否存在一条执行能到达目标位置。
3. `Product_service.Prom_inf` 是论文 `CRM` 模型中的具体 worker 位置。
4. `ta \le 44` 表示作者希望该业务目标在 `44` 个时间单位内可达。

### 语义边界

这篇论文的边界主要体现在：

1. 它处理的是从 `BPMN` 抽出的 `BP-task model`，不是 `BPMN` 全语法的完全形式语义。
2. 核心关注时间、并发和同步，不是复杂数据操作与资源最优化。
3. 模型需要先拆成有限个 worker 与有限个显式时间约束。
4. 论文重点是 qualitative verification，不是统计仿真或概率分析。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 元组 | `$A = \langle S, \Sigma, C, E, s_0 \rangle$` | 单个业务 worker 的定时行为模型。 |
| 边定义 | `$\langle s, a, g, r, s' \rangle \in E$` | 每条迁移都绑定动作、guard 和复位。 |
| 网络组合 | `$TAN = A_1 \parallel \cdots \parallel A_n$` | 把多个 worker 组合成完整业务过程。 |
| timed trace | `$\xi = (t_1,a_1)(t_2,a_2)\cdots$` | 用绝对时间序列表达执行。 |
| deadlock 检查 | `$A[]\ \neg deadlock$` | 检查业务过程不会卡死。 |
| deadline 可达性 | `$E<> \, Product\_service.Prom\_inf \Rightarrow ta \le 44$` | 检查业务目标能否在规定时间内完成。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个 worker 都被压成显式位置集合。 |
| 事件 / 触发 | 强支持 | `message flow`、任务开始/结束和同步事件都是核心。 |
| 守卫 / 数据 | 部分支持 | 重点是 clock guard；复杂业务数据不是主体。 |
| 层次 | 弱支持 | 原文主打并行 worker 组合，不走层次状态机路线。 |
| 并发 / 同步 | 强支持 | `TA-network` 与 `c! / c?` 握手是核心。 |
| 时间约束 | 强支持 | 响应时间、等待时间和 `QoS` 时限就是建模重点。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散时序行为，不建模连续流或概率。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 直接提供仿真、可达性与死锁分析。 |

### 形式化问题与性质

1. 论文真正补的是 `BPMN` 在分析阶段缺乏形式语义这一空白。
2. `Timed Automata` 在这里承担的是“业务流程时间与并发一致性”的验证骨架。
3. `CCTL/UPPAAL` 查询让业务规则能直接转成可检验性质，而不是停留在文本约束。
4. 因而它是 `Timed Automata` 主干在软件过程建模方向上一条很典型的应用线。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先用 `BPMN` 画出业务过程图。
2. 把每个参与执行的 worker 抽成单独 `TA`。
3. 根据消息流和时限规则，把同步、guard、invariant 和 reset 回填到自动机。
4. 最后把所有 worker 组合成 `TA-network` 并放入 `UPPAAL`。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `BPMN` 图。
2. worker 级 `Timed Automata`。
3. `TA-network`。
4. `CCTL/UPPAAL` 查询表达式。

### 交换与互操作

互操作重点在：

1. `BPMN` 建模元素如何映射到 `TA` 状态和迁移。
2. worker 间消息流如何变成握手同步。
3. 时间约束如何转成 `UPPAAL` guard、invariant 与 clocks。

## 配套基础设施

- 建模/编辑工具：业务建模侧使用 `BPMN`，验证侧使用 `UPPAAL`。
- 解析/交换/元模型支持：原文给出了 `BPMN -> TA` 转换指南，但未提供独立元模型或交换 schema。
- 仿真/执行支持：`UPPAAL` 提供交互式 simulation。
- 验证/分析支持：支持 deadlock、时间上界可达性和业务规则验证。
- 代码生成/转换支持：论文强调手工/规则式转换指南，未提供独立自动转换器仓库。
- 标准化或社区生态：依托 `BPMN` 标准和 `Timed Automata / UPPAAL` 生态。

## 适用场景与需求前提

### 适用场景

适合 `CRM`、审批流、服务交付链或其他以消息交互、任务持续时间和并发协作为核心的业务过程分析。

### 需求前提

1. 流程可以拆成有限个 worker 和活动状态。
2. 关键时间约束能写成显式上界、下界或 deadline。
3. 消息交互边界清晰，能映射成同步动作。
4. 目标是验证正确性与 `QoS` 是否满足，而不是做成本优化。

### 不适用或高成本场景

如果业务过程的关键难点主要在复杂数据变换、概率服务质量或大规模资源优化，而不是显式并发和时序约束，那么单靠本文这条 `TA` 管线并不够。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文不是本体定义而是业务过程应用；相对 [Automatic Verification of Component-Based Real-Time CORBA Applications](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)，这里面向的是 `BPMN` 业务任务而不是实时中间件组件；相对 [Timed Automata Networks for SCADA Attacks Real-Time Mitigation](../timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md)，这里关注的是业务规则与 `QoS`，后者更偏工业攻击检测。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求原始载体不是传统控制需求，而是业务流程、组织协作或任务编排图时，`Timed Automata` 仍然可以充当高可信验证目标模型。

### 作为目标形式主义还是中间表示

对显式时间约束的流程验证，它可以直接作为目标形式主义；对更大的需求建模链路，它也很适合作为从图形需求到模型检查的中间表示。

### 对需求到模型生成的启发

1. 自然语言中的时限、等待和响应规则应尽量抽成 clocks 与 invariants。
2. 组织角色或 worker 适合先拆成局部自动机，再做网络组合。
3. 若后续需要闭环修复，`UPPAAL` counterexample 可直接回指到哪个 worker 同步或时间窗出了问题。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文使用的全部时钟语义与网络验证都建立在经典 `TA` 主干上。
- [Automatic Verification of Component-Based Real-Time CORBA Applications](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)：同样把工程系统压成 `Timed Automata` 网络，但面向实时组件中间件。
- [Timed Automata Networks for SCADA Attacks Real-Time Mitigation](../timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md)：同属 `TA-network + query` 路线，不过应用客体从业务流程换成工业控制攻击检测。

## 文献分类总结

- 这是一篇 `⏱️` 类应用型条目，核心贡献是把 `BPMN` 业务过程系统地映射到 `Timed Automata` 网络并用 `UPPAAL` 验证。
- 它描述的是 worker 级任务逻辑与 `QoS` 时限，因此客体记为 `🎛️`；论文语境主要面向业务过程与软件分析，因此领域记为 `💻`。
- 对 `project_1` 来说，它证明了“图形化需求流程 -> 形式时序模型 -> 模型检查”这条链路在非传统控制软件领域同样成立。
