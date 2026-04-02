# 基于模糊逻辑与状态图的机器人挖掘全局控制 / Global Control for Robotic Excavation Using Fuzzy Logic and Statecharts

## 基本信息

- 标题：Global Control for Robotic Excavation Using Fuzzy Logic and Statecharts
- 中文标题：基于模糊逻辑与状态图的机器人挖掘全局控制
- 作者：M. Santos, Q. P. Ha, D. C. Rye, H. F. Durrant-Whyte
- 发表：*Proceedings of the 17th IAARC/CIB/IEEE/IFAC/IFR International Symposium on Automation and Robotics in Construction*, 2000
- DOI：`10.22260/ISARC2000/0108`
- 链接：https://doi.org/10.22260/ISARC2000/0108
- 形式主义：`Robotic Excavation UML Statechart Supervisor`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：施工机器人监督器 / fuzzy low-level + `UML` statechart high-level
- 工具/实现获取方式：原文直接给出 mini-excavator、joint encoders、hydraulic cylinder pressure transducers、spool valve set-points 和一组 `FLC_i` 低层控制器；未给公开代码仓库。
- 标准/格式获取方式：原文承载方式是 `UML statecharts`、task element base、task characteristic functions 与 fuzzy rule bases，不依赖独立 `XML/JSON` 标准。

## 简报

这篇论文的关键不是单独的模糊控制器，而是把挖掘任务显式拆成高层状态图与低层模糊控制器两层。高层 `UML statechart` 决定当前属于 `LowerBoom`、`Penetrate`、`Drag`、`Capture`、`DumpToTruck` 等哪一类作业相位，低层 `FLC_i` 则在每个相位内驱动 bucket、arm、boom 等具体轴运动。对本 collection 来说，它补的是一种非常典型的应用型状态机结构：状态机不直接求解连续土壤动力学，而负责调度哪类控制器在何时接管。

- 形式主义定位：面向 backhoe-type autonomous excavator 的高层 `UML statechart` 监督器，与低层 fuzzy logic controllers 组合完成 trench digging。
- 构造方式简述：先定义 task elements `\tau_1..\tau_{16}`，再把 trenching 工作循环分解成状态和子状态机，最后为每个 atomic state 绑定对应 `FLC_i`。
- 基础设施与场景简述：依托 mini-excavator、液压执行器、压力传感器和编码器，服务 trench forming 等自动土方作业。

```text
挖掘目标 -> task algorithm -> UML statechart -> atomic state / task element -> FLC_i -> 液压执行器动作
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. task element base `\tau_1..\tau_{16}`，对应 bucket curl、arm rotate、boom luff、tracks crawl 等可行动作。
2. 高层 trench-forming statechart。
3. digging sub-machine，至少包含 `LowerBoom`、`Penetrate`、`Drag`、`Capture`。
4. dump/reposition 等更高层工作循环状态。
5. `FLC_i` 模糊控制器，直接绑定各 atomic states。
6. task characteristic functions，用来判断转移何时成立。

### 核心抽象

结合原文的“task elements + statechart + fuzzy controller”组织方式，可把该监督器保守整理为：

$$
\mathcal{E} = (S, \Tau, \Gamma, \Delta, \Lambda)
$$

上式中的符号逐项解释如下：

1. `S` 是高层状态与子状态集合。
2. `\Tau = \{\tau_1,\tau_2,\ldots,\tau_{16}\}` 是原文列出的 task elements。
3. `\Gamma` 是 task characteristic functions 集合。
4. `\Delta` 是状态转移关系。
5. `\Lambda` 是 state-to-controller 绑定关系，即把状态映射到对应的 `FLC_i`。

论文在 trenching 例子中给出了一组非常清晰的 task elements，例如：

$$
\Tau = \{\tau_1,\tau_2,\ldots,\tau_{16}\}
$$

上式中的符号逐项解释如下：

1. `\tau_3` / `\tau_4` 分别表示 bucket inward / outward curl。
2. `\tau_5` / `\tau_6` 表示 arm inward / outward rotation。
3. `\tau_7` / `\tau_8` 表示 boom up / down。
4. `\tau_9..\tau_{16}` 还覆盖 swing、crawl、blade 等操作。

原文对转移特征函数的定义可压缩为：

$$
\gamma_i = \mathbf{1}[\text{transition to } S_i \text{ is active}]
$$

上式中的符号逐项解释如下：

1. `\gamma_i` 是状态 `S_i` 的 characteristic function。
2. 当到 `S_i` 的转移条件满足时，` \gamma_i = 1`。
3. 当转移条件不满足时，` \gamma_i = 0`。

对 trench forming 的 digging 子机，可保守写成：

$$
\mathcal{T}_{dig} = (\{LowerBoom, Penetrate, Drag, Capture\}, \Delta_{dig}, \Gamma_{dig}, \Lambda_{dig})
$$

上式中的符号逐项解释如下：

1. `LowerBoom` 对应把 bucket 放到地面。
2. `Penetrate` 对应 bucket teeth 入土。
3. `Drag` 对应同步移动 arm 与 boom 拉出直线轨迹。
4. `Capture` 对应 curl bucket 收土。
5. `\Delta_{dig}` 是这四个 digging phases 之间的转移。
6. `\Lambda_{dig}` 指示每个 phase 调用哪一个 `FLC_i`。

运行过程可保守写为：

$$
S_{t+1} = \delta(S_t, x_t, \gamma_t)
$$

上式中的符号逐项解释如下：

1. `S_t` 是当前 digging/work-cycle 状态。
2. `x_t` 是编码器、压力和 bucket-tip 几何等实时观测。
3. `\gamma_t` 是当前由 characteristic functions 计算出的转移激活向量。
4. `S_{t+1}` 是下一状态。

### 一个最小例子与通俗解释

最小例子可以直接用 trench forming 的一个 digging pass：

1. `LowerBoom` 把 bucket 送到 trench 起点附近。
2. `Penetrate` 用 bucket teeth 入土。
3. `Drag` 让 arm 和 boom 同步运动，沿 trench 方向拉出直线。
4. 当 arm fully contracted、bucket full 或 tip out of soil 时，转到 `Capture`。
5. `Capture` 用 `FLC_3` curl bucket 收土。
6. 如果 bucket 已经装满，则转到 `DumpToTruck`；如果 bucket stuck 或超时，则走 timeout strategy。

通俗地说，这个模型像“会安排工序的挖掘工头”。真正和土壤打交道的是下面的模糊控制器，而 statechart 负责决定当前是“下臂”“入土”“拖拽”“收土”还是“倒土”。

### 运行 / 接受 / 转移语义

其层级语义可保守写成：

$$
S_t \xrightarrow{\gamma_t} S_{t+1} \xrightarrow{\Lambda(S_{t+1})} FLC_i \xrightarrow{} u_{t+1}
$$

上式中的符号逐项解释如下：

1. `S_t \xrightarrow{\gamma_t} S_{t+1}` 表示 characteristic functions 决定高层相位切换。
2. `\Lambda(S_{t+1})` 选择该相位绑定的模糊控制器。
3. `FLC_i` 根据压力、角速度等输入产生控制输出。
4. `u_{t+1}` 是对应液压阀的 spool valve opening area 或 set-points。

原文对 `Capture` 的语义给出得很具体，可保守概括为：

$$
S_t = Capture \land (\mathrm{bucket\ full} \lor \mathrm{tip\ out\ of\ soil}) \Rightarrow S_{t+1} = DumpToTruck
$$

上式中的符号逐项解释如下：

1. `Capture` 是收土阶段。
2. `\mathrm{bucket\ full}` 和 `\mathrm{tip\ out\ of\ soil}` 是典型 exit conditions。
3. 一旦满足条件，就进入 `DumpToTruck`。

### 语义边界

这个模型的边界包括：

1. 高层 statechart 只调度工序，不直接统一表示 tool-soil 连续动力学。
2. 低层控制强依赖专家经验和模糊规则。
3. 论文面向 trench digging 等具体作业，不是通用施工机器人语言标准。
4. 若环境变化超出规则覆盖范围，仍需扩展 fuzzy rules 或额外异常策略。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 监督器骨架 | `$\mathcal{E} = (S, \Tau, \Gamma, \Delta, \Lambda)$` | 高层状态、task elements 和低层控制器被显式绑定。 |
| task element base | `$\Tau = \{\tau_1,\tau_2,\ldots,\tau_{16}\}$` | 挖掘动作先被离散成一组基础操作。 |
| 转移特征函数 | `$\gamma_i = \mathbf{1}[\text{transition to } S_i \text{ is active}]$` | 转移条件被显式编码成 characteristic functions。 |
| digging 子机 | `$\mathcal{T}_{dig} = (\{LowerBoom, Penetrate, Drag, Capture\}, \Delta_{dig}, \Gamma_{dig}, \Lambda_{dig})$` | trenching 关键相位被单独建成子状态机。 |
| 收土完成转移 | `$S_t=Capture \land (\mathrm{bucket\ full} \lor \mathrm{tip\ out\ of\ soil}) \Rightarrow S_{t+1}=DumpToTruck$` | bucket 几何与装载状态触发倒土。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | trenching 工作循环被明确分成相位状态。 |
| 事件 / 触发 | 强支持 | bucket full、tip out of soil、timeout 等都会触发转移。 |
| 守卫 / 数据 | 强支持 | 编码器、压力和位置误差直接决定 characteristic functions。 |
| 层次 | 强支持 | 高层 trench forming statechart 内含 digging sub-machine。 |
| 并发 / 同步 | 中等支持 | `UML statecharts` 允许并发与 superstate，但本文重点是单机多相位工序。 |
| 时间约束 | 中等支持 | 有显式 timeout transition，但不是 timed automata。 |
| 连续动态 / 随机性 | 强连续、无随机 | 连续液压控制很重要，但由 `FLC_i` 而非 statechart 承担。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 有 mini-excavator field tests，但没有形式验证链。 |

### 形式化问题与性质

1. 论文最重要的结构是“高层 statechart + 低层 fuzzy control”分层，而不是任意一条规则。
2. `UML statecharts` 在这里承担的是工序监督和 controller dispatch 的角色。
3. characteristic function 把传感条件和转移关系稳定连起来，避免纯口头工艺描述。
4. timeout transition 体现了应用型状态机必须显式处理 stuck / hard soil 等异常作业状态。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先根据专家经验把 excavation task 分解为一串 action phases。
2. 再把 phase 映射成 `UML statechart` 状态。
3. 为每个 atomic state 绑定对应的 `FLC_i`。
4. 用传感条件、位置误差和 bucket 状态定义 characteristic functions。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `UML statecharts` 图。
2. task element base `\tau_1..\tau_{16}`。
3. task characteristic functions。
4. `FLC_i` 模糊规则库与 defuzzification。
5. joint encoders / hydraulic pressure transducers 到 spool valve set-point 的映射。

### 交换与互操作

互操作重点在：

1. 高层 statechart 根据传感和估计信息决定工序相位。
2. 选中的相位激活对应的 `FLC_i`。
3. 模糊控制器输出阀开度或 set-points。
4. 执行结果再回到下一轮 characteristic function 评估。

## 配套基础设施

- 建模/编辑工具：`UML statecharts`、task decomposition 和 fuzzy rule bases。
- 解析/交换/元模型支持：无独立文件标准，主要是 statechart 图、task element 编号和 characteristic functions。
- 仿真/执行支持：mini-excavator、液压系统、joint encoders、cylinder pressure transducers。
- 验证/分析支持：trench digging field tests，平均 digging 部分约 `15 s`，与熟练人工操作相当。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 construction automation / field robotics 中的 `UML + fuzzy control` 路线。

## 适用场景与需求前提

### 适用场景

适合 trench forming、土方搬运等具有明确工序相位、但局部 tool-soil interaction 又难以精确建模的施工机器人场景。

### 需求前提

1. 任务可先分解成稳定的 digging / dumping / repositioning phases。
2. 现场具备压力、编码器等可用反馈。
3. 允许以专家经验和启发式规则驱动局部控制。
4. 需要在工序监督层与连续控制层之间明确分工。

### 不适用或高成本场景

如果作业环境极不规则、缺少可靠传感，或希望直接统一建模连续土壤动力学，这种 statechart + fuzzy rule 的方法会变得难以维护。

## 与相邻形式主义的关系

相对普通 `FSM`，它借助 `UML statecharts` 获得了 superstate、component reuse 和更灵活的 transition；相对纯 `Hybrid Automata`，它把连续动力学外包给模糊控制器；相对单层行为树，它更强调工序相位和异常转移的显式图结构。

## 与本研究的关系

### 对 Project 1 的价值

它很好地说明了施工工艺里的“下臂、入土、拖拽、收土、倒土”这类领域动作词，如何先变成状态，再和控制器绑定。

### 作为目标形式主义还是中间表示

对具体挖掘机器人，它可以直接作为高层执行监督器；对更一般的需求建模任务，它也适合作为把复杂控制逻辑分层组织的中间表示。

### 对需求到模型生成的启发

1. 领域流程词往往天然就是状态机状态名。
2. 若连续控制难以统一建模，LLM 更应该先生成监督层状态机。
3. 需求里的“超时”“卡住”“装满”等异常条件应显式落成 transition guards。
4. 状态到控制器的绑定关系是很多应用型条目的核心，不应在生成时遗漏。

### 现实限制

该方案高度依赖专家经验、规则调参和具体液压平台，跨设备迁移时需要重调 characteristic functions 和 `FLC_i`。

## 重要的相关工作

- automatic digging 的 fuzzy logic 研究：为本文低层控制提供直接背景。
- excavation task decomposition 和 task action space：为本文的高层状态分解提供来源。
- `UML statecharts`：为 reuse、hierarchy、concurrency 提供载体。
- field robotics 中的 excavator autonomy 路线：构成本文验证场景。

## 文献分类总结

- 这是一篇 `📦` 类施工机器人应用条目，核心是 `UML statechart` 如何监督 excavation phases，并把低层 `FLC_i` 串成完整工作循环。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；场景是施工自动化与土方作业，因此领域记为 `🏭`。
- 对 `project_1` 来说，它补的是“高层工序状态机如何调度低层连续控制器”的经典应用证据。
