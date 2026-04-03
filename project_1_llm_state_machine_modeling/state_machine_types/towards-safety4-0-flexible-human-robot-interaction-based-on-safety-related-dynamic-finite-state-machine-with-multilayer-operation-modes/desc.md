# 面向 Safety4.0 的多层操作模式安全相关动态有限状态机 / Towards safety4.0: A novel approach for flexible human-robot-interaction based on safety-related dynamic finite-state machine with multilayer operation modes

## 基本信息

- 标题：Towards safety4.0: A novel approach for flexible human-robot-interaction based on safety-related dynamic finite-state machine with multilayer operation modes
- 中文标题：面向 Safety4.0 的多层操作模式安全相关动态有限状态机
- 作者：Mohamad Bdiwi, Ibrahim Al Naser, Jayanto Halim, Sophie Bauer, Paul Eichler, Steffen Ihlenfeldt
- 发表：*Frontiers in Robotics and AI*, 9:1002226, 2022
- DOI：`10.3389/frobt.2022.1002226`
- 链接：https://doi.org/10.3389/frobt.2022.1002226
- 形式主义：`Safety4.0 Dynamic FSM`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧪 应用/案例
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🏭 工业控制与自动化
- 论文角色：安全模式框架 / 风险分析载体
- 工具/实现获取方式：原文明确说明该方法被集成到动态风险评估工具中，用于规划和实现柔性人机协作工作站；正文未给公开仓库。
- 标准/格式获取方式：承载方式是 interaction levels、clustered operation modes、state graph 与 safety-function 逻辑公式；其语义直接映射到 `ISO 12100`、`ISO 10218`、`ISO/TS 15066`、`IEC 61800-5-2` 等安全标准口径，而不是独立文件标准。

## 简报

这篇论文的关键贡献是把本来零散存在的 `HRI/HRC` 交互层级、operation modes 和 safety functions 压成一个真正可执行的状态机骨架。作者不是只做风险分析，也不是只列标准，而是提出四层结构：先按 interaction level 归类任务，再选 operation mode clusters，再把这些 mode 变成状态机状态，最后把安全功能写进转移条件。这样，安全模式不再只是规范文字，而是能落成 state graph、能被动态风险工具使用的执行载体。

- 形式主义定位：面向工业 `HRC/HRI` 规划与安全切换的 domain-specific dynamic `FSM`，而不是通用控制状态机。
- 构造方式简述：先定 interaction level，再组合 operation mode clusters，再把 mode 变成状态节点，用 safety functions 公式定义转移 guards。
- 基础设施与场景简述：依托动态风险评估工具和工业机器人安全标准，服务柔性人机协作工作站。

```text
HRI task requirements -> interaction levels -> clustered operation modes -> safety-related dynamic FSM -> risk analysis / implementation tool
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. level planner：按 interaction level 对任务做一级分类。
2. clustered operation modes：每个 level 下的模式组合。
3. mode states：例如 `SRMS`、`SSM`、`PFL`、`HandGuiding`、`AutoMode`、`Stop1`。
4. safety functions：如 `SS1`、`SBC`、`STO`、`SLS`、`SSR`、`SDI`。
5. transition conditions：由安全函数布尔公式定义的状态切换条件。
6. dynamic risk assessment tool：把上述结构用于规划和验证的工具承载。

### 核心抽象

根据论文第 3.4 节，可保守整理该安全相关状态机为：

$$
M = (S, S_0, F, T, \lambda)
$$

上式中的符号逐项解释如下：

1. `S` 是 collaborative operation mode 状态集合。
2. `S_0 \subseteq S` 是初始状态集合，例如 `AutoMode` 或某个安全待机模式。
3. `F` 是 safety functions 集合。
4. `T` 是状态迁移集合，每条迁移记为 `T_n^m`。
5. `\lambda : T \to \mathrm{Bool}(F)` 为每条迁移分配一个基于安全函数的布尔条件。

论文明确强调转移由安全函数逻辑决定，因此状态迁移可直接写成：

$$
S_n \xrightarrow{T_n^m} S_m \iff \lambda(T_n^m)(F)=\mathrm{true}
$$

上式中的符号逐项解释如下：

1. `S_n`、`S_m` 是起止状态。
2. `T_n^m` 是从 `S_n` 到 `S_m` 的转移。
3. `\lambda(T_n^m)(F)` 是该转移绑定的安全函数布尔公式。
4. 只有在该公式为真时，状态才允许切换。

### 一个最小例子与通俗解释

论文在 level 1 的 cluster 里给了很直观的状态图：

1. `S10 (AutoMode)` 表示自动运行。
2. `S4 (SSM)` 表示 speed and separation monitoring。
3. `S3 (SRMS)` 表示 safety-rated monitored stop。
4. `S1 (Stop1)` 表示紧急或危险区域进入后的停止状态。

例如，当人进入危险区时，系统会从协作模式切到 `Stop1`；只有危险区清空并且操作员通过 restart 信号确认，系统才允许回到 `AutoMode` 或协作模式。

通俗地说，这个模型像“把安全规范写成一张会动的模式切换图”：图上每条边都不是随便画的，而是由一组安全功能是否同时满足来决定能不能走。

### 运行 / 接受 / 转移语义

论文给出了多条具体转移公式。比如从自动模式切到协作速度监控模式的条件可整理为：

$$
T_{10}^{4} = (CFE_1 \lor \cdots \lor CFE_X) \land SLS \land SSM \land SSR \land SDI
$$

上式中的符号逐项解释如下：

1. `CFE_1 \lor \cdots \lor CFE_X` 表示某个 collaborative field 被进入。
2. `SLS` 是 safe limited speed。
3. `SSM` 是 speed and separation monitoring。
4. `SSR` 是 safe speed range。
5. `SDI` 是 safe direction。

从 `SRMS` 回到 `Stop1` 的紧急停机条件则可整理为：

$$
T_{3}^{1} = DFE \land SS1 \land SBC \land STO
$$

上式中的符号逐项解释如下：

1. `DFE` 表示 danger field entry。
2. `SS1` 是 safe stop 1。
3. `SBC` 是 safe brake control。
4. `STO` 是 safe torque off。

### 语义边界

这套状态机的边界也很清楚：

1. 它描述的是 operation modes 与 safety functions 的切换逻辑，不是机器人底层运动控制器。
2. 它比单纯 STPA 更接近可执行模式图，但仍不替代全部安全工程流程。
3. 状态与转移高度依赖工业标准术语，因此跨领域可移植性有限。
4. 它主要处理离散模式切换，不描述连续动力学与碰撞物理细节。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$M = (S, S_0, F, T, \lambda)$` | operation modes、safety functions 和转移逻辑被压成统一状态机。 |
| 转移判定 | `$S_n \xrightarrow{T_n^m} S_m \iff \lambda(T_n^m)(F)$` | 模式切换取决于安全功能逻辑是否满足。 |
| 协作进入条件 | `$T_{10}^{4} = (CFE_1 \lor \cdots \lor CFE_X) \land SLS \land SSM \land SSR \land SDI$` | 自动模式进入协作监控模式需要一组安全函数共同激活。 |
| 停机条件 | `$T_{3}^{1} = DFE \land SS1 \land SBC \land STO$` | 人进入危险区时系统进入 Stop1。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | operation modes 被显式建成状态。 |
| 事件 / 触发 | 强支持 | 人员进入区域、重启确认和安全功能变化都会触发转移。 |
| 守卫 / 数据 | 强支持 | 转移 guard 就是安全功能布尔公式。 |
| 层次 | 中等支持 | 通过 level planner 和 clusters 实现分层，不是通用 `HFSM` 层次语义。 |
| 并发 / 同步 | 弱支持 | 重点是模式切换，不是并发协同语义。 |
| 时间约束 | 弱支持 | 考虑停止类别和运行模式，但无显式时钟系统。 |
| 连续动态 / 随机性 | 不支持 | 不建模连续物理过程，只引用对应安全函数。 |
| 可执行 / 可验证性 | 强执行、弱形式验证 | 能落入动态风险工具和状态图实现；形式证明不是重点。 |

### 形式化问题与性质

1. 该方法最重要的地方是把 safety functions 从“附录清单”变成了状态机 guards。
2. `interaction level -> cluster -> mode state -> safety function` 四层结构让模式规划不再是一次性人工表格。
3. 与单纯模式枚举不同，作者把转移写成可扩展的布尔公式，便于加新的 safety function bundle。
4. 与 STPA 相比，它更聚焦于功能级调试和实际模式切换实现。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先按 interaction level 分类具体 `HRC/HRI` 任务。
2. 为该 level 选择合适的 collaborative operation mode clusters。
3. 把 cluster 中各 mode 建成状态图。
4. 为每条边写出安全功能公式。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. level planner。
2. clustered operation modes。
3. state graph。
4. safety-function 逻辑公式。
5. dynamic risk assessment tool。

### 交换与互操作

互操作重点在：

1. 状态和转移直接引用标准中的 safety function 术语。
2. 不同 interaction level 可复用类似 cluster，但 safety function bundles 不同。
3. 工具能把风险分析、模式规划和实现层联起来，而不是只停留在纸面规范。

## 配套基础设施

- 建模/编辑工具：论文明确提到动态风险评估工具承载该方法。
- 解析/交换/元模型支持：通过状态图和安全功能公式组织模式逻辑。
- 仿真/执行支持：目标是工业 `HRC/HRI` 工作站规划与实现，非纯仿真研究。
- 验证/分析支持：与标准和风险分析流程紧密耦合，但没有时序逻辑式形式验证。
- 代码生成/转换支持：论文没有展开自动代码生成，重点在规划和实现指导。
- 标准化或社区生态：高度依赖 `ISO 12100`、`ISO 10218`、`ISO/TS 15066`、`IEC 61800-5-2` 等标准体系。

## 适用场景与需求前提

### 适用场景

适合工业柔性生产、协作机器人工作站、需要在不同协作模式之间安全切换的人机协作系统。

### 需求前提

1. 任务能先按 interaction level 做层级划分。
2. 系统的 operation modes 可以枚举并组合成 clusters。
3. 安全设计可明确映射到一组标准化 safety functions。
4. 需要把风险分析结果下沉到实现级模式切换逻辑。

### 不适用或高成本场景

若应用场景没有明确的工业安全标准约束、也不存在多 operation mode 规划需求，则该方法会显得偏重；它主要服务严肃工业协作场景。

## 与相邻形式主义的关系

相对一般 `FSM`，它把状态语义专门绑定到 `HRI/HRC` operation modes；相对 `STPA`，它更偏可执行模式切换而非广义因果分析；相对 `SCR` 这类需求规格方法，它更专注安全模式和功能集合，而不是完整需求表格。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，状态机可以直接成为“标准术语 -> 风险分析 -> 实施逻辑”之间的桥梁，而不只是控制流程图。

### 作为目标形式主义还是中间表示

它更适合作为工业协作安全规划的领域目标载体，不适合作为通用中间表示。

### 对需求到模型生成的启发

1. 安全需求中的模式、区域和功能 bundle 都应被显式提炼成状态机元素。
2. 需求生成模型时，标准约束不必只写成备注，也可以直接落成转移 guard。
3. 对工业场景，interaction level 这类上层任务分类能够显著影响状态机结构。

## 重要的相关工作

- `STPA`：论文专门拿来和 `FSM` 做安全分析视角对比。
- `ISO 12100`、`ISO 10218`、`ISO/TS 15066`、`IEC 61800-5-2`：是该状态机 guard 语义的直接来源。
- `Safety skills`、HRC 风险分析方法：是其试图统一的前序工作。

## 文献分类总结

- 这是一篇 `📦` 类安全模式框架条目，重点在把多层协作 operation modes 与 safety functions 压成可实现的动态 `FSM`。
- 其描述客体是人机协作模式与安全交互，因此记为 `🤝`；论文语境是工业生产与协作机器人安全，因此领域记为 `🏭`。
- 对 `project_1` 来说，它补的是“特定安全需求如何直接生成为模式状态机”的领域化证据。
