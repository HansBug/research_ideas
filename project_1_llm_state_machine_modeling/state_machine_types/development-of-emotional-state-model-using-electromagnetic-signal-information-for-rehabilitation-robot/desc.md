# 基于电磁信号信息的康复机器人情绪状态模型构建 / Development of Emotional State Model using Electromagnetic Signal Information for Rehabilitation Robot

## 基本信息

- 标题：Development of Emotional State Model using Electromagnetic Signal Information for Rehabilitation Robot
- 中文标题：基于电磁信号信息的康复机器人情绪状态模型构建
- 作者：Aimi Shazwani Ghazali, Shahrul Naim Sidek, Sado Fatai
- 发表：*International Journal of Computational Intelligence Systems*, 9(1):65-79, 2016
- DOI：`10.1080/18756891.2016.1144154`
- 链接：https://doi.org/10.1080/18756891.2016.1144154
- 形式主义：`Hybrid Automata for Emotion-Aware Rehabilitation Robot Control`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：情绪感知康复机器人控制 / 混成自动机应用建模
- 工具/实现获取方式：原文明确使用 `GUI + Stateflow + rehabilitation robot platform` 实现 emotion-recognition 与 hybrid-automata controller 的联动；论文未给独立仓库。
- 标准/格式获取方式：承载方式是 hybrid automata 状态图、情绪编码、机器人位移/速度连续变量与 `Stateflow` 控制框架；原文未给统一交换标准。

## 简报

这篇论文的核心不是做一个更强的情绪识别器，而是把“病人的情绪变化如何实时改变康复机器人轨迹和速度”这件事，压成了一个明确的混成自动机控制框架。作者先从人体电磁信号里识别出 `sad / nervous / happy / calm` 四类情绪，再把这些离散情绪作为 hybrid automata 的 mode trigger，而把 gripper 的位置、速度和方向作为连续状态，从而实现一种情绪驱动的康复平台控制器。

- 形式主义定位：这是 `Hybrid Automata` 主干上的应用型条目，核心价值是把情绪分类结果和康复机械臂连续运动统一到一个混成控制模型里。
- 构造方式简述：先将电磁信号分类为离散情绪编码，再以情绪为 guard 驱动模式切换，用连续位置/速度/方向变量控制 gripper 在 home/goal 之间往返，并在不同情绪下采用不同目标速度。
- 基础设施与场景简述：依托 `Stateflow`、`GUI`、情绪识别模块与康复机器人平台，服务情绪感知型康复训练与 human-in-the-loop 机器人辅助治疗。

```text
EM signal -> emotion classification -> hybrid automata mode switch -> gripper speed / direction / trajectory update -> rehabilitation session adaptation
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 由电磁信号分类得到的离散情绪状态。
2. 表达控制阶段的 hybrid automata control states。
3. 表达情绪变化和轨迹切换的 plant symbols / transitions。
4. 表达 gripper 位置、速度与方向的连续变量。
5. home/goal 两个关键位置与来回切换逻辑。
6. 由 `GUI + Stateflow` 驱动的混成控制实现。

### 核心抽象

论文直接给出了该康复系统的 hybrid automata 六元组：

$$
H = \langle X, \Sigma, \Sigma_G, f, X_0, X_m \rangle
$$

上式中的符号逐项解释如下：

1. `X = \{S_1, S_2, \ldots, S_{11}\}` 是控制状态集合，对应初始化、前进、后退、末端缓冲等离散模式。
2. `\Sigma = \{x_1, x_2, \ldots, x_{29}\}` 是 plant symbols，表示情绪变化、位置到达等导致状态切换的事件。
3. `\Sigma_G = \{r_1, r_2, \ldots, r_{11}\}` 是 control symbols，对应各模式下的平台控制规则。
4. `f` 是迁移函数，例如 `f(S_1, x_1) = S_6`、`f(S_6, x_2) = S_7` 等。
5. `X_0 = \{S_1\}` 是初始状态。
6. `X_m = \{S_i\}` 是最终状态集合，表示任务在不同终止位置上的收束模式。

文中又明确指出，该系统同时包含离散情绪与连续平台运动。可把连续状态保守整理为：

$$
z = \langle x, v, dir, E \rangle
$$

上式中的符号逐项解释如下：

1. `x` 是 gripper 位置。
2. `v` 是 gripper 速度，单位为 `cm/s`。
3. `dir` 是 gripper 运动方向，表示 forward 或 backward。
4. `E` 是当前情绪编码。
5. 其中 `E` 属于离散情绪集合，而 `x` 与 `v` 是连续变量，因此系统属于典型的混成状态。

论文给出的速度设定可进一步整理为：

$$
v^\star(E) =
\begin{cases}
0.5, & E = sad \\
0.667, & E = nervous \\
1.0, & E = happy \\
0.833, & E = calm
\end{cases}
$$

上式中的符号逐项解释如下：

1. `v^\star(E)` 表示当前情绪对应的目标 gripper 速度。
2. `sad` 对应最低训练速度，反映病人注意力或投入程度较低。
3. `nervous` 对应中间速度。
4. `happy` 对应最高速度。
5. `calm` 是默认情绪，对应基准训练速度。
6. 文中还给出了靠近端点切换方向时的最低缓冲速度，用来减小动量冲击。

### 一个最小例子与通俗解释

文中最直观的例子是 gripper 在 home 与 goal 之间的往返训练：

1. 系统初始位于 `S_1`，gripper 先以 `1 cm/s` 向 home position `X=20` 回退。
2. 回到 home 后，系统根据当前情绪进入相应的前进模式，例如 calm 对应 `0.833 cm/s`，happy 对应 `1.0 cm/s`。
3. 如果训练过程中情绪从 `calm` 变成 `nervous`，hybrid automata 立即切换到对应模式并把速度调成 `0.667 cm/s`。
4. 当 gripper 接近 goal `X=5` 时，系统再进入缓冲/换向状态，用较小速度反向运行，继续下一轮康复动作。

通俗地说，这个模型像“一个会看病人情绪来调节动作节奏的康复教练”。普通状态机只能说“往前、往后、停止”，而 hybrid automata 还能把“速度是多少、位置到哪了、情绪变了以后怎么平滑切换”一起放进模型里。

### 运行 / 接受 / 转移语义

论文中的运行语义有三层：

1. 情绪识别模块把电磁信号映射为离散情绪编码 `E \in \{0,1,2,3\}`。
2. hybrid automata 根据情绪和位置条件触发离散 mode switch。
3. 每个 mode 规定 gripper 的连续速度、方向和端点切换行为。

文中给出的情绪编码可整理为：

$$
E \in \{0,1,2,3\}
$$

上式中的符号逐项解释如下：

1. `E=0` 表示 `calm`，是默认状态。
2. `E=1` 表示 `sad`。
3. `E=2` 表示 `nervous`。
4. `E=3` 表示 `happy`。
5. 该编码作为离散输入直接驱动自动机切换。

位置与方向切换的核心守卫可保守整理为：

$$
\text{if } x = 20 \Rightarrow dir := forward,\qquad
\text{if } x = 5 \Rightarrow dir := backward
$$

上式中的符号逐项解释如下：

1. `x=20` 对应 home position。
2. `x=5` 对应 goal position。
3. `dir` 表示 gripper 当前运动方向。
4. 到达端点时，系统通过离散切换改变方向并切换到新的控制状态。
5. 这也是文中 `S_{10}`、`S_{11}` 这类 end states 的主要语义。

### 语义边界

这篇论文的边界主要在于：

1. 混成模型关注的是情绪驱动的训练速度与方向调整，而不是完整人体生理动力学。
2. 情绪识别结果被离散成四类，模型没有覆盖更细粒度心理状态。
3. 连续动力学主要以位置/速度/方向为主，没有给出更复杂的机械臂方程。
4. 论文强调控制框架可行性，而不是混成自动机可达性或判定性理论边界。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统六元组 | `$H = \langle X, \Sigma, \Sigma_G, f, X_0, X_m \rangle$` | 给出情绪感知康复平台的 hybrid automata 骨架。 |
| 连续/离散联合状态 | `$z = \langle x, v, dir, E \rangle$` | 把位置、速度、方向和情绪统一进混成状态。 |
| 情绪驱动速度策略 | `$v^\star(E)$` 分段定义 | 不同情绪触发不同训练速度。 |
| 情绪编码 | `$E \in \{0,1,2,3\}$` | `calm/sad/nervous/happy` 的离散输入映射。 |
| 端点换向守卫 | `$x=20 \Rightarrow dir:=forward,\ x=5 \Rightarrow dir:=backward$` | 训练平台在 home/goal 处切换模式和方向。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `S_1` 到 `S_{11}` 明确表示不同训练模式与端点阶段。 |
| 事件 / 触发 | 强支持 | 情绪变化、到达端点和初始化完成都是主要触发。 |
| 守卫 / 数据 | 部分支持 | 位置和情绪编码作为 guard 明确出现，但数据复杂度不高。 |
| 层次 | 不支持 | 原文采用平铺状态图，不是层次混成自动机。 |
| 并发 / 同步 | 弱支持 | 主体是单平台控制，不强调多模块并发组合。 |
| 时间约束 | 弱支持 | 核心是速度和位置演化，而不是显式 clocks / deadlines。 |
| 连续动态 / 随机性 | 强连续、无随机性 | gripper 位置/速度连续演化，但不建模概率。 |
| 可执行 / 可验证性 | 部分可执行 | 已在 `GUI + Stateflow + robot platform` 上实现和实验，但形式验证不是主线。 |

### 形式化问题与性质

1. 论文把情绪识别结果真正接到了连续运动控制上，而不是只做离线情绪分类。
2. 它展示了 hybrid automata 很适合表达“离散心理状态 + 连续物理平台”的结合系统。
3. 对文库来说，它补的是混成自动机在康复机器人和 human-in-the-loop 场景中的一种典型应用证据。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 采集人体电磁信号并做情绪分类。
2. 把情绪分类结果编码成离散输入 `E`。
3. 为平台运动模式定义 hybrid automata control states。
4. 给每个 mode 指定速度、方向与端点切换规则。
5. 通过 `Stateflow` 与 `GUI` 把情绪输入和平台控制联接起来。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. hybrid automata 状态图与六元组定义。
2. 情绪编码和模式转移函数。
3. `Stateflow` 控制图。
4. 机器人平台位置/速度实验曲线。

### 交换与互操作

互操作重点在：

1. 情绪识别模块如何把分类结果传给 hybrid automata。
2. `Stateflow` 如何把自动机模式映射成平台速度/方向控制。
3. 位置传感器如何把连续位置反馈回离散模式切换。

## 配套基础设施

- 建模/编辑工具：原文直接采用 `GUI + Stateflow` 作为控制实现载体。
- 解析/交换/元模型支持：有图式状态机和情绪编码，但无独立交换标准。
- 仿真/执行支持：论文提供仿真和实验平台结果。
- 验证/分析支持：主要是实验验证和轨迹/速度对照，不是可达性模型检查。
- 代码生成/转换支持：原文未强调自动代码生成链。
- 标准化或社区生态：依托 `Hybrid Automata` 学术主干与 `Stateflow` 工业工具生态。

## 适用场景与需求前提

### 适用场景

适合康复机器人、情绪感知人机交互、需要根据操作者/病人状态实时调节连续动作参数的 human-in-the-loop 控制系统。

### 需求前提

1. 系统存在有限个可辨识的离散情绪或模式类别。
2. 平台连续运动可用位置、速度和方向等低维变量表达。
3. 离散情绪变化与连续动作参数之间存在稳定映射关系。
4. 任务主要关注动作节奏调节，而不是高精度动力学求解。

### 不适用或高成本场景

如果系统需要精确建模人体肌肉骨骼动力学、复杂多关节控制或高维不确定性，仅靠本文这种简化 hybrid automata 抽象会明显不够。

## 与相邻形式主义的关系

相对 [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)，本文不是混成自动机本体，而是把离散情绪和连续 gripper 运动联合进一个具体康复场景；相对 [A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata](../a-human-operator-model-for-medical-device-interaction-using-behavior-based-hybrid-automata/desc.md)，这里描述的是康复机器人控制，而不是医疗设备上的人机输入行为；相对 [Behavior Based Robotics Using Regularized Hybrid Automata](../behavior-based-robotics-using-regularized-hybrid-automata/desc.md)，这里强调情绪驱动速度调节，而不是避障与行为切换的 `Filippov` 正则化。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求中本身包含“操作者情绪/状态变化会改变控制策略”，那么生成的状态机不能只建离散控制流，还要把连续变量和 mode-dependent control law 一起带进模型。

### 作为目标形式主义还是中间表示

对情绪感知康复控制，它可以直接作为目标形式主义；对更一般的控制系统需求链路，它适合作为“离散用户状态 + 连续执行器动态”的中间混成表示。

### 对需求到模型生成的启发

1. 自然语言需求中的“高兴时加快、紧张时减速、到端点后换向”都可以直接转成 hybrid automata 的 guards 和 mode-dependent outputs。
2. 人的内部状态不一定是噪声变量，也可以是状态机的显式离散输入。
3. 如果后续要做性质生成，可以围绕速度上界、端点安全和换向平滑性自动生成约束。

## 重要的相关工作

- [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)：提供本文所依赖的混成自动机基础骨架。
- [A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata](../a-human-operator-model-for-medical-device-interaction-using-behavior-based-hybrid-automata/desc.md)：同样把人的离散行为与连续系统联系起来，但对象是医疗设备交互。
- [A Hybrid Automata Approach for Monitoring the Patient-In-The-Loop in Artificial Pancreas Systems](../a-hybrid-automata-approach-for-monitoring-the-patient-in-the-loop-in-artificial-pancreas-systems/desc.md)：同样面向医疗/康复相关 human-in-the-loop 混成系统。
- [Behavior Based Robotics Using Regularized Hybrid Automata](../behavior-based-robotics-using-regularized-hybrid-automata/desc.md)：展示 hybrid automata 在机器人控制上的另一条典型应用路线。

## 文献分类总结

- 这是一篇 `🌊` 类应用型条目，核心价值是把情绪识别、模式切换和康复机器人连续运动统一成一个 hybrid automata 控制框架。
- 它描述的是带连续运动的康复平台与病人状态耦合对象，因此记为 `🌡️`；论文语境显然落在 `CPS / 物理系统建模`，因此记为 `🌡️`。
- 对 `project_1` 来说，它提供了一个很直接的启发：需求里的人因状态、连续执行器动态和任务阶段切换，应被联合建模，而不是分散写成纯文本注释。
