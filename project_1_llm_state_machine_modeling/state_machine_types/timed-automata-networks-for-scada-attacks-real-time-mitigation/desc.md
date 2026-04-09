# 面向 SCADA 攻击实时缓解的定时自动机网络 / Timed Automata Networks for SCADA Attacks Real-Time Mitigation

## 基本信息

- 标题：Timed Automata Networks for SCADA Attacks Real-Time Mitigation
- 中文标题：面向 SCADA 攻击实时缓解的定时自动机网络
- 作者：Fabio Martinelli, Francesco Mercaldo, Antonella Santone, Christina Tavolato-Wötzl, Paul Tavolato
- 发表：*Proceedings of the 5th International Conference on Software Security and Assurance (ICSSA 2019)*, 2019
- DOI：原文未见
- 链接：https://uppaal.org/texts/mmstt-icssa19.pdf
- 形式主义：`Timed Automata Network for SCADA Attack Detection`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：SCADA 攻击检测 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL` 对由 SCADA 时序日志生成的 timed automata network 做模型检查；PDF 由 `UPPAAL` published material 页面公开提供。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata、离散化后的 `Up/Basal/Low` 特征轨迹与 `TCTL` 性质；原文未提供独立交换标准。

## 简报

这篇论文的核心做法不是直接对 SCADA 协议源码建模，而是把压力值和泵速这类 time-series logs 离散化成符号轨迹，再自动拼成同步推进的 timed automata network。随后，作者把“DoS 攻击”与“malicious injection 攻击”写成 `TCTL` reachability 性质，通过 `UPPAAL` 来判定一个 100ms 窗口是否呈现攻击特征。

- 形式主义定位：面向工业控制安全监测的 `Timed Automata` 应用条目，而不是协议级或接口级组合理论。
- 构造方式简述：先把连续特征等宽分箱到 `Up/Basal/Low`，再为每个特征构造一个 timed automaton，用同步通道 `s` 推进时间窗口。
- 基础设施与场景简述：依托 `UPPAAL`、`TCTL`、ARFF/文本日志和 100ms 观测窗口，服务气体管网 SCADA 攻击检测与实时告警。

```text
SCADA time-series logs -> equal-width discretisation -> per-feature timed automata -> synchronized network -> TCTL attack queries -> attack/no-attack judgement
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. 按时间窗口切片后的 pump / pressure 轨迹。
2. 每个离散化特征对应的一个 timed automaton。
3. 用于同步多个 automata 的 channel `s`。
4. 记录 `Up/Basal/Low` 计数的本地离散变量。
5. 表达 DoS 与 malicious injection 的 `TCTL` reachability 性质。

### 核心抽象

原文直接给出了 timed automaton 的定义：

$$
A = (L, l_0, C, A, E, I)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `l_0` 是初始 location。
3. `C` 是时钟集合。
4. `A` 是动作、共动作与内部动作集合。
5. `E` 是带有 guard、reset 和目标节点的边集合。
6. `I` 是对 location 施加时间不变式的函数。

论文把若干 automata 并联成网络，系统状态由位置、时钟和离散变量共同决定。可保守整理为：

$$
s = (\vec{l}, \nu, \sigma)
$$

上式中的符号逐项解释如下：

1. `\vec{l}` 是所有 feature automata 的当前位置向量。
2. `\nu` 是所有时钟的赋值。
3. `\sigma` 是本地计数变量，如 `u_1,b_1,l_1` 与 `u_2,b_2,l_2` 的当前取值。

### 一个最小例子与通俗解释

原文的最小例子就是两个特征 `F1/F2`：

1. 先把 pump 和 pressure 在某个 100ms 窗口内离散成 `Up/Basal/Low`。
2. 若连续几个采样点都保持 `Up`，对应 automaton 会在 `Up` 位置上做 loop，并用本地变量累计次数。
3. 两个 automata 通过同步通道 `s` 一起从第 `t_i` 个采样推进到第 `t_{i+1}` 个采样。
4. 最后如果低压 / 低泵速计数达到阈值，就满足 `DoS` 性质；如果高压 / 高泵速计数达到阈值，就满足 `MI` 性质。

通俗地说，它相当于把原始传感器曲线先压成“高/中/低”的符号序列，再用会计时、会同步的状态机去看“这 100ms 内有没有出现攻击特征模式”。

### 运行 / 接受 / 转移语义

原文给出了 delay 与 action 两类转移语义：

$$
(l, u) \xrightarrow{d} (l, u + d)
$$

以及

$$
(l, u) \xrightarrow{a} (l', u')
$$

上式中的符号逐项解释如下：

1. `l` 与 `l'` 是源/目标 location。
2. `u` 与 `u'` 是时钟赋值。
3. `d` 是时间延迟，要求延迟期间始终满足当前位置不变式。
4. `a` 是动作转移，要求对应 edge 的 guard 满足且 reset 后的新状态也满足目标不变式。

论文真正拿来做攻击判定的是 `TCTL` reachability 性质：

$$
E\langle\rangle \varphi_{DoS}, \qquad \varphi_{DoS} = l_1 \ge 7 \land l_2 \ge 12
$$

以及

$$
E\langle\rangle \varphi_{MI}, \qquad \varphi_{MI} = h_1 \ge 9 \land h_2 \ge 14
$$

上式中的符号逐项解释如下：

1. `E\langle\rangle` 表示存在某个可达状态满足目标谓词。
2. `l_1,l_2` 分别是两个特征在窗口中出现 `Low` 的计数。
3. `h_1,h_2` 分别是两个特征出现 `Up` 的计数。
4. `\varphi_{DoS}` 与 `\varphi_{MI}` 分别编码 DoS 与 malicious injection 的经验阈值模式。

### 语义边界

这篇论文的边界非常清楚：

1. 它不是对 SCADA 控制程序本体建模，而是对时间窗口内的观测轨迹建模。
2. 离散化把连续数值压成 `Up/Basal/Low` 三值，因此会丢掉精细数值结构。
3. 当前只用了 pressure 和 pump 两类特征。
4. 攻击性质依赖领域专家给出的阈值公式，不是自动学习出的完整行为模型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 定时自动机 | `$A = (L, l_0, C, A, E, I)$` | 每个离散化特征都被写成一个 timed automaton。 |
| 系统状态 | `$s = (\vec{l}, \nu, \sigma)$` | 同时跟踪位置、时钟和本地计数变量。 |
| 延迟语义 | `$(l, u) \xrightarrow{d} (l, u+d)$` | 在满足 invariant 的前提下让时间推进。 |
| DoS 判定 | `$E\langle\rangle \varphi_{DoS}$`，`$\varphi_{DoS} = l_1 \ge 7 \land l_2 \ge 12$` | 当低值累计达到阈值时，窗口被判为 DoS。 |
| MI 判定 | `$E\langle\rangle \varphi_{MI}$`，`$\varphi_{MI} = h_1 \ge 9 \land h_2 \ge 14$` | 当高值累计达到阈值时，窗口被判为 malicious injection。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个离散化特征都对应显式 locations 与 loops。 |
| 事件 / 触发 | 强支持 | 同步通道 `s` 与窗口推进共同驱动状态迁移。 |
| 守卫 / 数据 | 强支持 | guard、invariant 与离散计数变量共同决定攻击判定。 |
| 层次 | 弱支持 | 重点是并行网络，不是层次状态机。 |
| 并发 / 同步 | 强支持 | 多个特征 automata 通过 channel 同步推进。 |
| 时间约束 | 强支持 | 核心正是 timed automata 与 `TCTL`。 |
| 连续动态 / 随机性 | 不支持 | 连续值先被离散化，随机性不是主体。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 直接承担 reachability 检查。 |

### 形式化问题与性质

1. 论文最关键的创新点是“从 SCADA 时间序列日志自动拼出可验证的定时自动机网络”。
2. 它把安全攻击检测问题重写成 `TCTL` reachability 问题，而不是单纯统计分类。
3. `Up/Basal/Low` 三值离散化使模型简洁，但也决定了它更适合做模式级攻击判定而不是精细物理诊断。
4. 对时间自动机主干来说，这篇论文展示了“从日志到 timed automata”的另一条工程应用路线。

## 构造方式与承载格式

### 建模入口

建模入口可概括为：

1. 从 SCADA 数据集中读取 pressure 与 pump 序列。
2. 用等宽分箱把连续值离散成 `Up/Basal/Low`。
3. 为每个离散化特征构建一个 timed automaton。
4. 用同步通道和 `TCTL` 性质把多特征行为组装成攻击检测器。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` timed automata network。
2. 本地离散变量 `u_i/b_i/l_i`。
3. 两个时钟 `x/y` 用于控制 loop 进入与退出。
4. `TCTL` reachability 查询。

### 交换与互操作

互操作重点不在标准化，而在“日志到模型”的转换链：

1. 原始数值日志先转换成符号序列。
2. 符号序列再转换成 timed automata。
3. 攻击知识通过 `TCTL` 查询与 automata network 对接。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：原文无通用元模型，主要依赖自定义日志离散化与 `UPPAAL` 模型。
- 仿真/执行支持：重点不在 runtime 执行，而在离线 / 在线窗口判定。
- 验证/分析支持：`UPPAAL` reachability model checking。
- 代码生成/转换支持：从文本 / ARFF 日志到 timed automata 的转换流程在论文中明确给出。
- 标准化或社区生态：依托 `Timed Automata` / `UPPAAL` 生态，但攻击公式本身是场景定制的。

## 适用场景与需求前提

### 适用场景

适合气体管网、工业控制、远程监控等 SCADA 场景中的时序攻击检测，尤其是攻击模式可以用“某类符号状态在窗口内反复出现若干次”来表达的情况。

### 需求前提

1. 观测信号能切成固定长度时间窗口。
2. 连续值离散化后仍能保留攻击模式差异。
3. 攻击特征可以写成有限状态 + 计数阈值。
4. 系统能接受 `UPPAAL` 这类模型检查式检测链路。

### 不适用或高成本场景

如果攻击模式高度依赖复杂多变量连续动力学、隐蔽长期统计漂移或大量上下文数据，仅靠这种离散化 timed automata network 会丢掉太多信息。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文把时钟语义用在 log-based attack detection；相对 [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，它不是从协议实现反向抽象，而是从运行日志正向生成 automata；相对 [Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems](../hybrid-automata-for-cps/survey.md)，它主动丢掉连续值细节，换取简单可验证的实时离散模型。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文很适合作为“日志/需求片段如何被压成定时状态机”的例子，说明实时语义不一定只能从规范出发，也可以从观测轨迹出发。

### 作为目标形式主义还是中间表示

它更适合作为检测/验证导向的中间表示，而不是人类工程师最终维护的主模型。

### 对需求到模型生成的启发

1. LLM 生成时间自动机时，可以先做符号化和窗口化，再去抽 location / guard / invariant。
2. 实时攻击、异常或安全性质很适合先写成 reachability/TCTL 模式，再反向约束模型结构。
3. 对传感器驱动系统，计数阈值、窗口大小和离散化粒度本身就是需求建模的重要部分。

### 现实限制

论文当前只演示了少量特征和两类攻击，对更复杂工控系统还需要更丰富的特征工程与性质设计。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：给出 timed automata 的理论母体。
- [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：展示 `UPPAAL` 在工业控制领域的另一类应用路线。
- [A Survey of Timed Automata for the Development of Real-Time Systems](../survey-of-timed-automata-for-real-time-systems/survey.md)：提供时间自动机工具与应用全景。

## 文献分类总结

- 这是一篇 `⏱️` 类应用条目，关键价值在于把 SCADA 观测日志压成 timed automata network 并用 `TCTL` 做攻击判定。
- 其描述客体是工业控制过程的观测状态，因此记为 `🎛️`；论文语境落在气体管网与 SCADA 安全，因此记为 `🏭`。
- 对 `project_1` 来说，它提示我们：实时状态机不一定只来自规范，也可以来自对控制日志和异常模式的结构化抽象。
