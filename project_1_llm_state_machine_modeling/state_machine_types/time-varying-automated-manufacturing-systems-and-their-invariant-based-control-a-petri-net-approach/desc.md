# 面向时变制造系统的 Petri 网不变式控制 / Time-Varying Automated Manufacturing Systems and Their Invariant-Based Control: A Petri Net Approach

## 基本信息

- 标题：Time-Varying Automated Manufacturing Systems and Their Invariant-Based Control: A Petri Net Approach
- 中文标题：面向时变自动化制造系统的 Petri 网不变式控制
- 作者：Chen Chen, Hesuan Hu
- 发表：*IEEE Access*, 7:23149-23162, 2019
- DOI：`10.1109/ACCESS.2019.2899190`
- 链接：https://doi.org/10.1109/ACCESS.2019.2899190
- 形式主义：`Tv-S4R / Time-Varying S4R Petri Net`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：制造系统时变监督控制 / Petri 网应用与模型扩展
- 工具/实现获取方式：原文给出 reachability-graph 分析、monitor synthesis、weighted state/event-based supervisor algorithms；未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `S^4R`、`TPPN`、`Tv-S^4R`、monitor place、`GMEC/GLC` 与 `P-invariant` 线性约束；无独立交换格式。

## 简报

这篇论文的核心价值，不只是“又做了一次制造系统监督控制”，而是把“不同时间段允许不同工艺模式”这件事显式纳入 `Petri Net` 本体。作者先定义 `Tv-S^4R`，把物理制造过程和一个表示时间区段轮换的虚拟循环网并起来，然后再比较 state-based、event-based、weighted state-based、weighted event-based 四类不变式监督器，讨论哪种更简洁、哪种更 permissive。

- 形式主义定位：面向共享资源制造系统的时变 `Petri Net` 扩展与监督控制，不是单纯调度算法。
- 构造方式简述：先建立 `S^4R` 生产网，再加一条表示时间区段轮换的 `TPPN` 环，并用 monitor places 把 transition 绑定到可执行时间窗。
- 基础设施与场景简述：依托 `Tv-S^4R`、`GMEC/GLC`、`P-invariant`、reachability graph 和 supervisor simplification，服务自动化制造系统的 deadlock-free control。

```text
AMS 资源/工序网 + 时间区段循环网 -> Tv-S^4R -> time-varying specifications -> invariant-based supervisor -> deadlock-free / more-permissive control
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 表示制造工序和共享资源的 `S^4R` 网。
2. 表示时间区段轮换的一条单向 `TPPN` 环。
3. 两者拼接得到的 `Tv-S^4R`。
4. 对 transition 可执行时间窗的 monitor places。
5. `GMEC`、`GLC`、加权线性约束和 `P-invariant` 监督器。

### 核心抽象

原文先定义了 `S^4R`，再引入时变扩展。最终 `Tv-S^4R` 被写成：

$$
\hat{N} = (\hat{P}, \hat{T}, \hat{F}, \hat{W}, \hat{D})
$$

上式中的符号逐项解释如下：

1. `\hat{P} = P \cup P_{Tv}`，由物理制造网 places 与时间区段 places 组成。
2. `\hat{T} = T \cup T_{Tv}`，由物理 transition 与时间循环 transition 组成。
3. `\hat{F}` 是两部分弧集合的并。
4. `\hat{W}` 是统一的弧权函数。
5. `\hat{D}` 是延时向量，其中 `P_{Tv}` 上的 place 具有显式时间延迟。

论文进一步把整体 marking 写成：

$$
\hat{M} = [M;\ M_{Tv}]
$$

上式中的符号逐项解释如下：

1. `M` 是制造过程部分的 marking。
2. `M_{Tv}` 指示当前 token 落在哪个时间区段 place 上。
3. 因而 `\hat{M}` 同时包含“系统正在做什么”和“现在处于哪个时间段”。

对 transition 的三类使能，原文给出了明确划分：

$$ t \text{ fireable at } M \iff t \text{ is process-enabled } \land t \text{ is resource-enabled } \land t \text{ is time-enabled} $$

其中 time-enabled 在原文中写成：

$$
M(\tilde{P}_{Tv}) = 1
$$

上式中的符号逐项解释如下：

1. `\tilde{P}_{Tv}` 是允许某个 transition 执行的时间区段子集。
2. 若当前时间 token 正好落在这个子集上，则该 transition 在时间上可执行。

### 一个最小例子与通俗解释

论文最直观的例子是两条工艺分支轮流开放：

1. `p16,p17,p18,p19` 组成一个 24 小时循环的时间区段环。
2. transition `t2` 只允许在第 1 和第 3 个时间区段触发。
3. transition `t4` 只允许在第 2 和第 4 个时间区段触发。
4. 为此分别构造 monitor `\tilde{p}_{c2}` 和 `\tilde{p}_{c4}`，把时间窗约束变成网结构上的自循环使能。

通俗地说，这个模型像是在普通制造网旁边再挂一只“时间拨盘”：token 转到哪个时段，哪些工位就能开工，哪些工位就必须等到下一时段。

### 运行 / 接受 / 转移语义

原文给出用于把时间窗结构化为网的 monitor 规则。保守整理后，可写成：

$$ \bullet \tilde{p}_c = \{t\} \cup \bullet \tilde{P}_{Tv},\qquad \tilde{p}_c \bullet = \{t\} \cup \tilde{P}_{Tv} \bullet,\qquad M_0(\tilde{p}_c)=0 $$

上式中的符号逐项解释如下：

1. `\tilde{p}_c` 是约束 transition `t` 的监视 place。
2. `\bullet \tilde{P}_{Tv}` 和 `\tilde{P}_{Tv} \bullet` 分别是时间区段子集的前继和后继。
3. 这样一来，只要时间 token 处在允许区段，`t` 的自循环就可保持 enable。

在加权 state-based 监督器里，论文把坏 marking `M^*` 对应的线性约束写成：

$$ \sum_{i=1}^{|P_A|} M^*(p_i)\, M(p_i) \le \sum_{i=1}^{|P_A|} M^*(p_i)\, M^*(p_i) - 1 $$

上式中的符号逐项解释如下：

1. `P_A` 是 activity places 集合。
2. `M^*(p_i)` 是坏 marking 在 `p_i` 上的 token 数。
3. `M(p_i)` 是当前 marking 在 `p_i` 上的 token 数。
4. 该不等式确保系统不会再走回这个 forbidden bad marking。

对应的加权 event-based 版本则是：

$$ \sum_{i=1}^{|P_A|} M^*(p_i)\, M(p_i) + q_i \le \sum_{i=1}^{|P_A|} M^*(p_i)\, M^*(p_i) $$

其中：

1. `q_i` 是某个非法 firing 的布尔变量。
2. 当系统位于 critical good marking 时，它阻止该非法 transition 继续触发。

### 语义边界

这篇论文的边界主要体现在：

1. 时间变化体现在“时间区段开放/关闭 transition”，不是一般 `Time Petri Net` 的 firing interval 语义。
2. 重点是 deadlock-free supervisory control，而不是性能最优调度。
3. 研究对象仍然是共享资源制造系统，不是通用 `Petri Net` 理论。
4. 权重系数是为提高 permissiveness 而设计的工程化扩展，不改变 `PN` 的基本 firing 语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `Tv-S^4R` 骨架 | `$\hat{N} = (\hat{P}, \hat{T}, \hat{F}, \hat{W}, \hat{D})$` | 把制造网和时间区段网统一起来。 |
| 整体 marking | `$\hat{M} = [M; M_{Tv}]$` | 同时记录制造状态和时间区段。 |
| time-enabledness | `$M(\tilde{P}_{Tv}) = 1$` | 规定 transition 是否在当前时间段可执行。 |
| monitor 结构 | `$\bullet \tilde{p}_c, \tilde{p}_c \bullet$` | 把时间约束转成结构约束。 |
| 加权 state-based 约束 | `$\sum M^*(p_i) M(p_i) \le \sum M^*(p_i)^2 - 1$` | 阻断 forbidden bad marking。 |
| 加权 event-based 约束 | `$\sum M^*(p_i) M(p_i) + q_i \le \sum M^*(p_i)^2$` | 在 critical good marking 阻断非法 firing。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 同时表达工序状态、资源状态和时间区段。 |
| 事件 / 触发 | 强支持 | transition firing 就是制造事件。 |
| 守卫 / 数据 | 中等支持 | 时间窗和线性约束是主体，复杂数据不多。 |
| 层次 | 弱支持 | 更像“制造网 + 时间网”的并置组合。 |
| 并发 / 同步 | 强支持 | 共享资源和多工序并发是核心。 |
| 时间约束 | 强支持 | 但强调 time-varying availability，而非一般 firing interval。 |
| 连续动态 / 随机性 | 不支持 | 纯离散资源流模型。 |
| 可执行 / 可验证性 | 强验证 | reachability、liveness、monitor synthesis 都是主体。 |

### 形式化问题与性质

1. 论文补出的关键对象是 `Tv-S^4R`，而不是只在普通 `PN` 上加几条调度规则。
2. monitor place 让时间窗真正落进了网结构，而不是停留在外部调度表。
3. 加权 invariant-based supervisor 给出了比普通 state/event-based 方法更高的 permissiveness。
4. 因而它既是 `Petri Net` 应用条目，也是一条可稳定命名的制造系统网模型扩展线。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 先把制造流程与共享资源建成 `S^4R`。
2. 再构造一条表示时间区段轮换的单向循环 `TPPN`。
3. 选出只在特定时间段可执行的 transition。
4. 为这些 transition 加上 time-varying specification monitors。
5. 最后生成 `GMEC/GLC` 或加权约束并合成 supervisor。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `S^4R / Tv-S^4R` 网结构。
2. 时间区段循环 places。
3. `GMEC/GLC` 线性约束。
4. `P-invariant` 和 monitor places。

### 交换与互操作

互操作重点在：

1. 物理制造网与时间区段网如何组合。
2. 时间窗如何转成结构性 monitor。
3. 线性约束如何进一步转成控制 place 并落地到监督器。

## 配套基础设施

- 建模/编辑工具：原文主要以数学定义、reachability graph 和算法描述承载。
- 解析/交换/元模型支持：无独立 `PNML`/XML 交换格式说明。
- 仿真/执行支持：重点是 reachability-based analysis，而不是在线执行平台。
- 验证/分析支持：reachability graph、liveness analysis、supervisor synthesis、supervisor simplification。
- 代码生成/转换支持：原文未提供公开实现。
- 标准化或社区生态：依托 `Petri Nets`、`S^4R` 与 invariant-based supervisory control 研究线。

## 适用场景与需求前提

### 适用场景

适合那些在不同时间段开放不同工艺路线或资源使用策略的自动化制造系统、共享资源生产线和可重构车间。

### 需求前提

1. 工序与共享资源可离散成 `Petri Net` places/transitions。
2. 时间变化主要体现在“某些 transition 只在某些时间段可执行”。
3. 系统关心死锁避免和 permissive supervisor。
4. 约束能够写成 marking / firing vector 线性不等式。

### 不适用或高成本场景

如果系统关注的是精细连续时间调度、随机加工时间分布或底层物理控制，这种 `Tv-S^4R` 结构会显得过于粗粒度。

## 与相邻形式主义的关系

相对 [time-petri-nets/desc.md](../time-petri-nets/desc.md)，本文的时间语义不是 transition firing interval，而是 time-varying operation mode；相对 [fms-scheduling-under-availability-constraint-with-supervisor-based-on-timed-petri-nets/desc.md](../fms-scheduling-under-availability-constraint-with-supervisor-based-on-timed-petri-nets/desc.md)，它更强调模型本体和 supervisor family 比较；相对 [petri-net-approach-of-collision-prevention-supervisor-design-in-port-transport-system/desc.md](../petri-net-approach-of-collision-prevention-supervisor-design-in-port-transport-system/desc.md)，它是更纯的 shared-resource manufacturing net 扩展。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求明确含有“时间段切换的工艺权限”时，普通 `Petri Net` 可以通过结构扩展升格成更贴切的目标模型，而不必把所有时变逻辑外置到调度器。

### 作为目标形式主义还是中间表示

对制造类共享资源系统，它可以直接作为目标形式主义；对更一般系统，它也适合作为并发资源层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把“资源约束”和“时间段开放规则”分开编码。
2. 如果某些事件只在特定班次/时间窗可执行，应考虑显式时间区段 places，而不是仅写注释。
3. 对后续验证与修复任务，线性不等式型约束很适合成为可操作的中间表示。

## 重要的相关工作

- [time-petri-nets/desc.md](../time-petri-nets/desc.md)：Petri 网时间扩展的经典路线。
- [fms-scheduling-under-availability-constraint-with-supervisor-based-on-timed-petri-nets/desc.md](../fms-scheduling-under-availability-constraint-with-supervisor-based-on-timed-petri-nets/desc.md)：制造调度方向的 `Timed Petri Net` 应用。
- [petri-net-approach-of-collision-prevention-supervisor-design-in-port-transport-system/desc.md](../petri-net-approach-of-collision-prevention-supervisor-design-in-port-transport-system/desc.md)：`P-invariant` 监督控制在交通资源系统中的应用。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心贡献是提出 `Tv-S^4R` 并比较多类 invariant-based supervisor 在时变制造系统中的效果。
- 其描述客体是共享资源和并发工序流，因此记为 `🏭`；论文语境也明确落在工业制造自动化，因此记为 `🏭`。
- 对 `project_1` 来说，它补足了“时间段开放规则 + 共享资源监督控制”这一类需求的 `Petri Net` 形式化证据。
