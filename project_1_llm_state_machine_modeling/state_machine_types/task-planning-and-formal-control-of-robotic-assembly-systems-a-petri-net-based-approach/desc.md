# 机器人装配系统的任务规划与形式化控制：一种基于 Petri 网的方法 / Task Planning and Formal Control of Robotic Assembly Systems: A Petri Net-Based Approach

## 基本信息

- 标题：Task Planning and Formal Control of Robotic Assembly Systems: A Petri Net-Based Approach
- 中文标题：机器人装配系统的任务规划与形式化控制：一种基于 Petri 网的方法
- 作者：G{\"o}khan Gelen, Yasemin {\.I}{\c{c}}mez
- 发表：*Ain Shams Engineering Journal*, 15(7):102804, 2024
- DOI：`10.1016/j.asej.2024.102804`
- 链接：https://doi.org/10.1016/j.asej.2024.102804
- 形式主义：`Automation Petri Net (APN) + Place-Invariant Supervisor`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：机器人装配任务规划 / Petri 网监督控制与代码落地
- 工具/实现获取方式：原文给出 `APN` 建模、place-invariant supervisor synthesis 与 Mitsubishi `MELFA BASIC` 控制代码映射方法；未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `APN`、incidence matrix、control places 与 `MELFA BASIC` 程序结构；原文未给独立交换格式。

## 简报

这篇论文的重要性，在于它把 “任务序列 -> 监督器 -> 机器人控制代码” 打通了。很多 Petri 网机器人论文停在建模或分析层，而本文明确把装配任务先写成 `Automation Petri Net`，再按 place invariants 合成 supervisor，最后把 token 流映射成工业机器人控制程序。

- 形式主义定位：面向工业机器人装配单元的 `Petri Net` 应用与控制落地，而不是纯分析网模型。
- 构造方式简述：先用 `APN` 描述任务序列和传感触发，再把控制规格写成线性约束，随后通过 `Ns = L N` 求 control places，最后映射到 `MELFA BASIC`。
- 基础设施与场景简述：依托 `APN`、incidence matrix、place invariants、robot controller 与 assembly cell，服务工业装配任务的实时监督执行。

```text
assembly task sequence -> automation Petri net -> place-invariant constraints -> supervisor control places -> robot control code
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 装配任务序列。
2. 带传感器条件和动作映射的 `Automation Petri Net`。
3. 以 control places 形式出现的 supervisor。
4. 工业机器人装配单元与控制代码实现。

### 核心抽象

原文先给出普通 `PN`：

$$
N = (P, T, F, W)
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合。
2. `T` 是 transition 集合。
3. `F` 是流关系。
4. `W` 是弧权函数。

随后扩成 automation Petri net：

$$
APN = (N, X, Q, M_0)
$$

上式中的符号逐项解释如下：

1. `N` 是基础 Petri 网结构。
2. `X = \{\chi_1, \chi_2, \ldots, \chi_m\}` 是 transition 的 firing conditions，通常来自传感器读数。
3. `Q = \{q_1, q_2, \ldots, q_n\}` 是可分配给 place 的动作集合。
4. `M_0` 是初始 marking。

place-invariant supervisor 的控制目标被写成：

$$
\sum_{i=1}^{n} l_i \mu_i \le \beta
$$

上式中的符号逐项解释如下：

1. `\mu_i` 是 place `p_i` 的 marking。
2. `l_i` 是约束系数。
3. `\beta` 是允许上界。

加入 slack/control place 后，该约束改写为：

$$
\sum_{i=1}^{n} l_i \mu_i + \mu_c = \beta
$$

所有约束可以写成矩阵形式：

$$
L \mu_p \le b, \qquad L \mu_p + \mu_s = b
$$

原文接着给出 control-place incidence matrix 和初始 marking 的计算：

$$
N_s = L N
$$

$$
\mu_{s0} = b - L \mu_{p0}
$$

上式中的符号逐项解释如下：

1. `N_s` 是 supervisor control places 的 incidence matrix。
2. `\mu_{p0}` 是 plant net 的初始 marking。
3. `\mu_{s0}` 是 supervisor 的初始 marking。

### 一个最小例子与通俗解释

论文中的装配单元需要完成 body、piston、spring、cover 的装配，最小可理解例子是“同一时刻只能做一个机器人任务”：

1. place `p_1, p_2, p_4, p_5, p_6, p_7, p_8` 对应若干装配任务。
2. 作者要求这些位置上的 token 总数不超过 `1`，因为系统只有一台机器人。
3. 于是得到约束 `\mu_1 + \mu_2 + \mu_4 + \mu_5 + \mu_6 + \mu_7 + \mu_8 \le 1`。
4. 通过 `N_s = L N` 自动生成 control place `C_1`，从而阻止两个任务并行启动。

通俗地说，这个模型像“给装配流程图装上闸门”：任务网照常表示流程，但 supervisor places 负责在关键节点拦住那些违反资源约束的 token 流。

### 运行 / 接受 / 转移语义

运行语义仍是标准 `PN/APN` firing，只是 transition 还要满足传感器条件：

$$
t \text{ may fire only if } \chi_t = 1
$$

其中：

1. `\chi_t` 是分配给 transition `t` 的 firing condition。
2. 该条件通常来自传感器或外部信号。

当约束被写成 `L \mu_p \le b` 后，supervisor control places 通过 `N_s = L N` 被并入闭环网，形成受控模型。论文中的第一条装配规格就是：

$$
\mu_1 + \mu_2 + \mu_4 + \mu_5 + \mu_6 + \mu_7 + \mu_8 \le 1
$$

由此得到：

$$
L_1 = [1\ 1\ 0\ 1\ 1\ 1\ 1\ 1\ 0\ 0\ 0\ 0]
$$

并最终求出相应 control place 的 incidence vector 与初始 marking。

### 语义边界

这篇论文的边界很清楚：

1. 重点是高层任务序列和资源约束监督，而不是低层轨迹控制。
2. `APN` 里的传感器条件是布尔触发，不建模连续控制误差。
3. 代码映射主要面向 Mitsubishi 机器人控制程序，不是通用工业标准。
4. 论文依赖装配流程可被有限离散任务与容量约束表达。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础 Petri 网 | `$N = (P, T, F, W)$` | 描述任务流程骨架。 |
| 自动化 Petri 网 | `$APN = (N, X, Q, M_0)$` | 把传感器条件和动作映射接入任务网。 |
| 约束不等式 | `$\sum l_i \mu_i \le \beta$` | 表达单机器人、单夹具容量等装配控制规格。 |
| 矩阵约束 | `$L \mu_p \le b$` | 多条控制规格的统一写法。 |
| supervisor incidence | `$N_s = L N$` | control places 的结构由 plant net 自动导出。 |
| supervisor 初始值 | `$\mu_{s0} = b - L \mu_{p0}$` | control places 的初始 token 数。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 部分支持 | 状态由 marking 分布表达，不是传统单状态机。 |
| 事件 / 触发 | 强支持 | transition 与 sensor condition 共同驱动流程推进。 |
| 守卫 / 数据 | 强支持 | `APN` 明确把传感器触发条件作为 firing guard。 |
| 层次 | 弱支持 | 主要是单层任务序列和控制 place。 |
| 并发 / 同步 | 强支持 | 资源约束和互斥通过 control places 精确编码。 |
| 时间约束 | 不支持 | 论文未引入显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 关注离散装配监督。 |
| 可执行 / 可验证性 | 强执行 | 直接落到工业机器人控制代码。 |

### 形式化问题与性质

1. 本文最大的增量，是把 formal supervisor synthesis 和 robot code realization 连到一起。
2. `APN` 让 sensor conditions 成为网模型的一部分，而不是外部注释。
3. place-invariant method 使得装配容量、互斥和先后约束都能系统化处理。
4. 这类条目对 Petri 并发主干很有价值，因为它不只分析，还证明能落地控制器。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 将装配过程分成离散任务序列。
2. 用 `APN` 表达任务、传感触发和动作。
3. 把控制规格写成 place invariants / 线性不等式。
4. 自动求出 control places 并映射到机器人代码。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `APN` 图结构。
2. incidence matrix。
3. `L`、`b`、`N_s`、`\mu_{s0}` 等矩阵表达。
4. Mitsubishi `MELFA BASIC` 控制代码。

### 交换与互操作

互操作主要体现在：

1. 任务网与 supervisor 的结构化耦合。
2. 从 Petri 网 places/transitions 到机器人变量与子程序调用的映射。
3. 从 formal model 到 controller implementation 的闭环。

## 配套基础设施

- 建模/编辑工具：原文围绕 `APN` 建模与矩阵计算，未绑定通用 PN 工具。
- 解析/交换/元模型支持：使用 incidence matrix 和 `APN` 结构，但无统一交换格式。
- 仿真/执行支持：FESTO Didactic assembly cell、Mitsubishi `RV-2SDB`、`CR1-571` robot controller。
- 验证/分析支持：place-invariant supervisor synthesis、timing diagram-based execution checks。
- 代码生成/转换支持：从 `PN` 结构映射到 `MELFA BASIC`。
- 标准化或社区生态：依托 Petri nets 与工业机器人编程语境，标准化较弱但工程落地直接。

## 适用场景与需求前提

### 适用场景

适合工业装配单元、顺序装配、夹具/工位容量受限、单机器人或小规模离散协作流程的监督控制。

### 需求前提

1. 任务可分解成有限离散步骤。
2. 传感器事件可作为布尔 firing conditions 使用。
3. 控制规格可表达为容量、互斥或顺序约束。
4. 工程团队接受 supervisor 驱动的控制程序结构。

### 不适用或高成本场景

如果系统核心难点在连续力控、复杂运动规划或高随机装配误差，则单纯 `APN + place invariants` 不够，还需与 motion/hybrid 模型结合。

## 与相邻形式主义的关系

相对 [application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md](../application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md)，本文不强调节拍分析，而强调 supervisor 与代码落地；相对 [towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md](../towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md)，它更偏工业装配任务控制而非安全门控；相对 [distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md](../distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md)，它更靠近单元级装配控制和工业机器人代码生成。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提供了非常直接的证据：当需求主要是离散任务顺序、工位容量和资源互斥时，Petri 网可以从建模一路走到控制器实现。

### 作为目标形式主义还是中间表示

对工业装配与离散制造控制，它可以直接作为目标形式主义；对更复杂系统，也适合作为任务调度/资源约束层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把任务序列、传感触发、资源容量和互斥条件显式分开。
2. 若目标是落地控制代码，模型里必须包含 sensor/actuator 对应关系，不能只有抽象状态图。
3. 对 `LLM` 建模来说，place-invariant 约束是一类很适合结构化生成的对象。

## 重要的相关工作

- [application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md](../application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md)：制造单元调度与 timed `PN` 分析。
- [towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md](../towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md)：`HRC` 安全门控方向的 Petri 应用。
- [distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md](../distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md)：面向现代机器人软件的分布式 Petri 工具链。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心贡献是把机器人装配任务从 `APN` 建模推进到 place-invariant supervisor synthesis 和控制代码实现。
- 其描述客体是装配任务流与资源约束，因此记为 `🏭`；论文语境是工业装配与自动化，因此记为 `🏭`。
- 对 `project_1` 来说，它补足了“Petri 网如何直接走到机器人控制器实现”的重要证据链。
