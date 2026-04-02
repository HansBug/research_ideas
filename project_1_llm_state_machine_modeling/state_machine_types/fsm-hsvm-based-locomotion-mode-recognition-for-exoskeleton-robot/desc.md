# 基于 FSM-HSVM 的外骨骼机器人运动模式识别 / FSM-HSVM-Based Locomotion Mode Recognition for Exoskeleton Robot

## 基本信息

- 标题：FSM-HSVM-Based Locomotion Mode Recognition for Exoskeleton Robot
- 中文标题：基于 FSM-HSVM 的外骨骼机器人运动模式识别
- 作者：Zhuo Qi, Qiuzhi Song, Yali Liu, Chaoyue Guo
- 发表：*Applied Sciences*, 12(11):5483, 2022
- DOI：`10.3390/app12115483`
- 链接：https://doi.org/10.3390/app12115483
- 形式主义：`FSM-HSVM Exoskeleton Locomotion Recognizer`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：外骨骼模式识别器 / `FSM`-constrained `HSVM`
- 工具/实现获取方式：原文直接给出 `BIT` lower-limb exoskeleton、`4` 个 `IMU`、`4` 个 plantar `FSR`、`RS485`、`Samsung S5P6818` 主控和在线识别流程；未给公开代码仓库。
- 标准/格式获取方式：原文未给独立交换标准，主要承载方式是 locomotion-mode `FSM`、`HSVM` 分类树、输入特征向量和识别性能指标公式。

## 简报

这篇论文很适合作为“状态机不只用于执行，也可用于识别”的应用证据。作者先用 `HSVM` 做五类运动模式分类，再用 `FSM` 把合理模式转移范围硬编码进去，从而减少不合理跳变和多分类开销。也就是说，状态机在这里不是输出动作，而是给分类器加上序列约束。

- 形式主义定位：面向下肢外骨骼的 locomotion-mode recognizer，其中 `FSM` 负责约束可达模式转移，`HSVM` 负责实时分类。
- 构造方式简述：先用 `IMU + FSR` 形成特征向量，再用 `DTW` 设计 `HSVM` 分层结构，最后把五种模式和八种转换写成 `FSM`。
- 基础设施与场景简述：依托自研 wearable lower-limb exoskeleton、板载计算平台和在线识别模块，服务平地、楼梯和坡道环境中的模式识别与后续控制。

```text
IMU / FSR data -> feature vector -> HSVM sub-classifiers -> FSM transition constraints -> recognized locomotion mode
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 输入特征向量 `Data`。
2. 五种稳定 locomotion modes：`FW`、`US`、`DS`、`UR`、`DR`。
3. 八种合法 locomotion mode transitions。
4. `HSVM` 分类树及四个二分类 `SVM_i`。
5. `FSM` 模式约束框架。
6. 评价指标：`RA`、`RD` 和 recognition time。

### 核心抽象

原文明确给出了输入向量：

$$
Data = [\theta_{LH}, \theta_{LK}, \theta_{RH}, \theta_{RK}, F_{LB}, F_{LH}, F_{RB}, F_{RH}]
$$

上式中的符号逐项解释如下：

1. `\theta_{LH}`、`\theta_{LK}`、`\theta_{RH}`、`\theta_{RK}` 分别是左右髋膝关节角。
2. `F_{LB}`、`F_{LH}`、`F_{RB}`、`F_{RH}` 分别是左右脚 ball/heel 的 plantar pressure。
3. 这些量由 `4` 个 `IMU` 和 `4` 个 `FSR` 提供。

论文给出的有限状态机定义为：

$$
M = (Q, \Sigma, \delta, q_0, F)
$$

上式中的符号逐项解释如下：

1. `Q` 是 locomotion mode 状态集合。
2. `\Sigma` 是输入信息集合，这里主要是 joint angles 和 plantar pressures。
3. `\delta` 是状态转移函数。
4. `q_0` 是初始状态。
5. `F` 是终止状态集合。

这套识别器可以进一步保守整理为：

$$
\mathcal{R} = (Data, \mathcal{H}, M)
$$

上式中的符号逐项解释如下：

1. `Data` 是输入特征。
2. `\mathcal{H}` 是 `HSVM` 分类树。
3. `M` 是限制模式转移的 `FSM`。

原文给出的核心模式转移约束可压缩为：

$$
Q = \{\mathrm{FW}, \mathrm{US}, \mathrm{DS}, \mathrm{UR}, \mathrm{DR}\}
$$

$$
\Delta_{legal} = \{\mathrm{FW}\leftrightarrow \mathrm{US},\ \mathrm{FW}\leftrightarrow \mathrm{DS},\ \mathrm{FW}\leftrightarrow \mathrm{UR},\ \mathrm{FW}\leftrightarrow \mathrm{DR}\}
$$

上面两式中的符号逐项解释如下：

1. `FW` 表示 flat walking。
2. `US` / `DS` 表示 up / down stairs。
3. `UR` / `DR` 表示 up / down ramp。
4. `\Delta_{legal}` 说明模式切换只能通过平地中转，不允许如 `US -> DS` 这类直接跳变。

### 一个最小例子与通俗解释

最小例子可以用“当前正在上楼梯”来说明：

1. 当前 `CurrentState = US`。
2. `FSM` 先规定下一时刻只可能还是 `US`，或回到 `FW`。
3. 因此识别时不必调用整棵 `HSVM`，而只需调用对应的局部二分类器。
4. 如果传感数据表明还在连续上楼，则保持 `US`。
5. 如果动作开始回到平地，则转到 `FW`。
6. 像 `US -> DR` 这种不合理跳变会被 `FSM` 直接排除。

通俗地说，这个模型像“先用分类器猜，再让状态机做常识检查”。分类器负责看数据像什么，状态机负责说“人不可能刚上楼就直接变成下坡”。

### 运行 / 接受 / 转移语义

其运行语义可以保守写成：

$$
\hat q_t = \mathrm{HSVM}(Data_t), \qquad q_{t+1} = \delta(q_t, \hat q_t)
$$

上式中的符号逐项解释如下：

1. `Data_t` 是当前采样周期输入向量。
2. `\hat q_t` 是 `HSVM` 给出的候选模式。
3. `q_t` 是当前 `FSM` 状态。
4. `\delta` 会根据合法转移集合筛掉不合理跳变，输出最终模式 `q_{t+1}`。

原文给出的五条融合规则可保守概括为：

$$
q_t = \mathrm{FW} \Rightarrow q_{t+1} \in \{\mathrm{FW}, \mathrm{US}, \mathrm{DS}, \mathrm{UR}, \mathrm{DR}\}
$$

$$
q_t \in \{\mathrm{US}, \mathrm{DS}, \mathrm{UR}, \mathrm{DR}\} \Rightarrow q_{t+1} \in \{q_t, \mathrm{FW}\}
$$

上面两式中的符号逐项解释如下：

1. 当当前模式是 `FW` 时，可以调用整棵 `HSVM` 识别全部可能模式。
2. 当当前模式是其他四类之一时，下一时刻只允许保持原模式或回到 `FW`。

### 语义边界

这个模型的边界包括：

1. 它是模式识别器，不是完整外骨骼运动控制器。
2. `FSM` 只能排除不合理跳变，不能弥补特征本身不可分的问题。
3. 原文主要覆盖五类基础地形模式和八类转换，未包含更复杂环境。
4. 速度变化、自适应个体差异仍是作者明确提到的后续问题。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 输入向量 | `$Data = [\theta_{LH}, \theta_{LK}, \theta_{RH}, \theta_{RK}, F_{LB}, F_{LH}, F_{RB}, F_{RH}]$` | 识别器把关节角和足底压力统一作为输入。 |
| FSM 定义 | `$M = (Q, \Sigma, \delta, q_0, F)$` | 模式约束部分是一个标准有限状态机。 |
| 模式集合 | `$Q = \{\mathrm{FW}, \mathrm{US}, \mathrm{DS}, \mathrm{UR}, \mathrm{DR}\}$` | 论文的五类稳定运动模式被显式列出。 |
| 合法转移 | `$\Delta_{legal} = \{\mathrm{FW}\leftrightarrow \mathrm{US}, \ldots \}$` | 模式切换只能经由合理路径。 |
| 识别语义 | `$\hat q_t = \mathrm{HSVM}(Data_t),\ q_{t+1} = \delta(q_t, \hat q_t)$` | `HSVM` 给候选，`FSM` 负责约束。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 五种稳定模式和八种转换被显式区分。 |
| 事件 / 触发 | 中等支持 | 模式变化由连续特征和 gait transition 共同触发。 |
| 守卫 / 数据 | 强支持 | 关节角和 plantar pressure 是核心 guard 数据。 |
| 层次 | 强支持 | `HSVM` 采用树状分层分类结构。 |
| 并发 / 同步 | 弱支持 | 主要是单外骨骼在线识别，不是多组件并发状态机。 |
| 时间约束 | 中等支持 | gait cycle、transition period 和 recognition delay 都很重要，但不是显式 timed automata。 |
| 连续动态 / 随机性 | 中等连续、无随机 | 输入是连续信号，但高层识别和约束仍是离散的。 |
| 可执行 / 可验证性 | 强执行、较强评估 | 有在线识别实验、混淆矩阵、延迟率和复杂度分析。 |

### 形式化问题与性质

1. 论文最有意思的点是把状态机用于“约束识别结果”而不是直接控制执行器。
2. `FSM` 显式编码先验运动常识，减少 `HSVM` 多分类搜索空间。
3. `DTW` 距离被用来设计 `HSVM` 的层次结构，说明状态机周围还可以挂统计/学习模块。
4. 应用型状态机在这里直接带来了精度、延迟和计算开销的三重收益。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 用 `IMU + FSR` 收集 gait 数据。
2. 抽取 joint angle 与 plantar pressure 作为特征向量。
3. 用 `DTW` 分析五种模式的相似性，构造 `HSVM` 分类树。
4. 再用 `FSM` 写出五种模式和八种合法转换。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. 输入特征向量 `Data`。
2. `HSVM` tree structure 和 `SVM_1..SVM_4`。
3. locomotion-mode `FSM` 图。
4. `RA`、`RD`、time-ratio 等评价公式。
5. 板载在线识别实现。

### 交换与互操作

互操作重点在：

1. `IMU` 和 `FSR` 通过 `RS485` 将数据送到主控。
2. 预处理后的特征先送入 `HSVM`。
3. `FSM` 根据当前状态限制允许调用的子分类器或最终模式集合。
4. 输出模式再用于后续外骨骼控制策略切换。

## 配套基础设施

- 建模/编辑工具：论文主要给出 `FSM` 图、`HSVM` 树和实验流程图。
- 解析/交换/元模型支持：特征向量、`DTW` 距离表和 `FSM` 规则。
- 仿真/执行支持：`BIT` 自研下肢外骨骼、`4 IMU + 4 FSR`、`RS485`、`Samsung S5P6818` 主控。
- 验证/分析支持：混淆矩阵、`RD` 表、累计识别时间和理论复杂度分析。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 exoskeleton intention recognition 与 wearable robotics 研究线。

## 适用场景与需求前提

### 适用场景

适合可穿戴下肢外骨骼中，需要实时区分平地、楼梯、坡道等基础模式，并希望把识别结果稳定对接到模式切换控制器的场景。

### 需求前提

1. 设备能够稳定采集 joint angles 和 plantar pressures。
2. 运动模式集合相对有限，且相邻模式关系可事先写清。
3. 系统需要在线识别而非离线分析。
4. 允许利用 gait 常识限制可达模式转移。

### 不适用或高成本场景

如果环境模式高度开放、速度变化大或个体差异极强，固定的 `FSM + HSVM` 结构可能难以长期维持高精度。

## 与相邻形式主义的关系

相对纯 `SVM/HMM` 分类器，它多了一层显式状态机先验；相对传统 gait-phase `FSM` 控制器，它更偏向模式识别而不是执行；相对端到端深度学习，它的可解释性和计算开销更友好。

## 与本研究的关系

### 对 Project 1 的价值

它证明了需求中的“模式不能乱跳”这类业务常识，很适合作为状态机结构先验，而不只是文字说明。

### 作为目标形式主义还是中间表示

对外骨骼系统，它更像控制器前面的中间识别层；但对 broader state machine 建模研究，它也说明状态机可以承担 perception-to-control 之间的桥梁角色。

### 对需求到模型生成的启发

1. 需求中的合法模式转换关系值得先被单独抽成状态机。
2. 机器学习模块和状态机并不是替代关系，而是可以串联。
3. 识别类状态机同样需要 guard、状态集合和性能指标。
4. 对应用型模型，延迟率和识别时间和准确率同等重要。

### 现实限制

当前实验主要面向五类模式、固定速度和健康受试者，复杂地形和速度自适应仍需补充。

## 重要的相关工作

- locomotion mode recognition 中的 `SVM/HMM` 路线：构成本文比较基线。
- `DTW` 与 gait similarity 分析：直接支持 `HSVM` 树结构设计。
- exoskeleton intention recognition 与 wearable sensing：提供数据采集背景。
- 基于规则或后处理的 `FSM` gait recognizer：是本文要超越的近邻方法。

## 文献分类总结

- 这是一篇 `📦` 类外骨骼应用条目，核心是如何用 `FSM` 约束学习分类器的输出，而不是提出新自动机理论。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；场景是外骨骼与具身运动识别，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“状态机如何作为学习模块的结构先验和模式切换约束”的应用证据。
