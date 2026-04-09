# 运行时监控一台 Rover：基于开源软件与低成本硬件的 MDE 研究 / Run-time Monitoring of a Rover: MDE Research with Open Source Software and Low-cost Hardware

## 基本信息

- 标题：Run-time Monitoring of a Rover: MDE Research with Open Source Software and Low-cost Hardware
- 中文标题：运行时监控一台 Rover：基于开源软件与低成本硬件的 MDE 研究
- 作者：Reza Ahmadi，Nicolas Hili，Leo Jweda，Nondini Das，Suchita Ganesan，Juergen Dingel
- 发表：*Joint Proceedings of the 12th Educators Symposium (EduSymp 2016) and 3rd International Workshop on Open Source Software for Model Driven Engineering (OSS4MDE 2016) co-located with MODELS 2016*，pp. 37-44，2016
- DOI：原文未给出
- 链接：https://ceur-ws.org/Vol-1835/paper06.pdf
- 形式主义：`UML-RT / Papyrus-RT runtime monitoring pipeline`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：`Papyrus-RT` 运行时监控方法 / 低成本 `UML-RT` 部署与 trace 动画链
- 工具/实现获取方式：原文明确给出 `Papyrus-RT`、`LTTng`、`Trace Compass` 和 Rover GitHub 项目入口，并说明监控插件将并入 `Papyrus-RT` 主仓库。
- 标准/格式获取方式：核心承载是 `UML-RT` capsules / ports / protocols / state machines、`LTTng` 生成的 `CTF` traces 和 `Papyrus-RT` plugins；它不是独立交换标准。

## 简报

这篇论文的核心不是提出新的状态机语言，而是把 `Papyrus-RT` 模型、生成代码、运行时 trace 和模型级动画真正连成闭环。作者先在 `Papyrus-RT` 中建 `UML-RT` rover 模型，再生成代码和 trace points，运行后由 `LTTng` 采集 `CTF` traces，最后用 `Trace Compass` 解析并回导到 `Papyrus-RT` 做动画和 timing checks。

- 形式主义定位：围绕 `UML-RT` 的 runtime monitoring 方法路线，而不是新的状态机本体。
- 构造方式简述：`Papyrus-RT model -> generated code + trace points -> LTTng CTF traces -> Trace Compass -> Papyrus-RT animation/checking`。
- 基础设施与场景简述：依托开源建模、追踪与可视化工具，把实时嵌入式系统的模型级监控落到低成本 Rover 平台。

```text
UML-RT 模型 -> 代码与 trace points -> CTF traces -> trace parsing -> 模型级动画与 timing 检查
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Papyrus-RT` 中的 `UML-RT` 模型。
2. timing annotations 与 runtime-monitoring annotations。
3. 生成代码与 trace points。
4. `LTTng` 产生的 `CTF` trace files。
5. `Trace Compass` 与 `Papyrus-RT` animation plugins。

### 核心抽象

结合论文描述，可把整条监控链保守整理为：

$$
\mathcal{R} = (U, \Lambda, G, T, V)
$$

上式中的符号逐项解释如下：

1. `U` 是 `UML-RT` 模型。
2. `\Lambda` 是 timing 与 monitoring annotations。
3. `G` 是从模型生成的代码与 trace point 信息。
4. `T` 是运行后采集到的 traces。
5. `V` 是回导到 `Papyrus-RT` 的可视化与检查结果。

论文的主流程可压成：

$$
U \xrightarrow{\mathrm{Papyrus\text{-}RT}} G \xrightarrow{\mathrm{LTTng}} T_{ctf} \xrightarrow{\mathrm{Trace\ Compass}} V
$$

上式中的符号逐项解释如下：

1. `U` 是建好的 `UML-RT` 模型。
2. `G` 包含生成的 `C++` 代码与 trace points。
3. `T_{ctf}` 是 `LTTng` 输出的 `Common Trace Format` 文件。
4. `V` 是经 `Trace Compass` 解析后回到 `Papyrus-RT` 的动画与检查结果。

论文还给出了 Rover 的五层结构，可整理为：

$$
\mathcal{P} = (HW, FS, GPIO, Lib, App)
$$

其中：

1. `HW` 是 Raspberry Pi 与传感器/执行器硬件层。
2. `FS` 是 Linux 文件系统层。
3. `GPIO` 是封装 GPIO 读写的 `C++` wrapper。
4. `Lib` 是 `Rover Library` 层的 `UML-RT` capsules。
5. `App` 是最上层应用逻辑。

### 一个最小例子与通俗解释

论文的 Rover 行为很简单但很典型：

1. 初始状态向前运动。
2. 检测到障碍后转向 `90` 度。
3. 再次前进。
4. 全程持续收集温湿度。

通俗地说，这项工作像是在 `UML-RT` 模型外面加了“黑匣子 + 回放器”。模型不只是设计时的图，运行后的每一步都能被采样、回放并重新映射到原始状态机上。

### 运行 / 接受 / 转移语义

监控语义的关键不是重新定义 Rover 状态机，而是定义模型到 trace 的对应关系，因此可保守写成：

$$
\mathrm{Trace}(G,\rho) = T_{ctf}
$$

上式中的符号逐项解释如下：

1. `G` 是已生成并部署的代码与 trace points。
2. `\rho` 是目标平台上的真实运行。
3. `T_{ctf}` 是采集到的 `CTF` traces。
4. 这说明 trace 不是离线日志附属物，而是运行时监控的主工件。

对回导与检查流程，可进一步写成：

$$
\mathrm{Animate}(T_{ctf},U) = V
$$

其中：

1. `T_{ctf}` 是解析后的 traces。
2. `U` 是原始 `UML-RT` 模型。
3. `V` 是 `Papyrus-RT` 中可见的动画、轨迹与 timing-check 结果。
4. 这正是论文把 runtime execution 拉回 model-level 的关键。

### 语义边界

边界主要有：

1. 论文关注的是监控与动画，不是形式语义新定义。
2. 运行时分析能力仍受 trace points 布设质量影响。
3. 低成本硬件平台是 demonstrator，不意味着方法只适用于 Rover。
4. 强项是模型级回放与 timing 检查，不是自动纠错或完备验证。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
| --- | --- | --- |
| 监控链骨架 | `$\mathcal{R} = (U, \Lambda, G, T, V)$` | 模型、注解、生成物、trace 与可视化共同组成闭环。 |
| 主流程 | `$U \xrightarrow{\mathrm{Papyrus\text{-}RT}} G \xrightarrow{\mathrm{LTTng}} T_{ctf} \xrightarrow{\mathrm{Trace\ Compass}} V$` | 从模型到 trace 再回模型的全链路。 |
| Rover 五层结构 | `$\mathcal{P} = (HW, FS, GPIO, Lib, App)$` | 低成本平台上的 UML-RT 部署分层骨架。 |
| 采集语义 | `$\mathrm{Trace}(G,\rho) = T_{ctf}$` | trace files 是真实运行的主监控工件。 |
| 回导语义 | `$\mathrm{Animate}(T_{ctf},U) = V$` | traces 被重新映回模型级动画与 timing 检查。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
| --- | --- | --- |
| 状态 / 模式 | 强支持 | Rover 逻辑由 `UML-RT` capsules 内部状态机承载。 |
| 事件 / 触发 | 强支持 | 端口、协议和 trace points 都围绕事件交互展开。 |
| 守卫 / 数据 | 强支持 | timing annotations、monitoring annotations 与环境数据采集都被显式纳入。 |
| 层次 | 中等支持 | 重点在 `UML-RT` 结构层和部署分层，而不是状态层次理论。 |
| 并发 / 同步 | 中等支持 | 多 capsule 与 trace collection 协同运行。 |
| 时间约束 | 强支持 | 论文直接面向 real-time monitoring 与 timing checks。 |
| 连续动态 / 随机性 | 不突出 | Rover 是嵌入式反应系统，连续物理不是方法核心。 |
| 可执行 / 可验证性 | 强执行、强监控 | 代码生成、trace 采集和模型级动画是主卖点。 |

### 形式化问题与性质

1. 论文真正补的是 `Papyrus-RT` 的运行时可观测性，而不是再定义一门 `UML-RT` 方言。
2. `CTF` 作为中间承载，使 trace 处理与可视化链解耦，这是很重要的基础设施决策。
3. 把模型级动画建立在真实生成代码运行之上，而不是纯模拟器，是这条路线相对 `Moka` 类方案的关键差异。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 在 `Papyrus-RT` 中建 `UML-RT` capsules、ports、protocols 和 state machines。
2. 给模型添加 timing / monitoring annotations。
3. 生成代码并部署到目标平台。
4. 运行后采集 traces，再回导做动画与检查。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML-RT` 模型。
2. 生成的 `C++` 代码与 trace points。
3. `CTF` traces。
4. `Papyrus-RT` plugins 与 `Trace Compass` 解析结果。

### 交换与互操作

互操作重点在：

1. `Papyrus-RT` 负责前端建模与后端动画。
2. `LTTng` 负责轻量 instrumentation。
3. `Trace Compass` 负责通用 trace parsing。
4. 低成本 Rover 平台证明这条链可落到真实嵌入式对象。

## 配套基础设施

- 建模/编辑工具：`Papyrus-RT`。
- 解析/交换/元模型支持：`UML-RT`、annotations 与 `CTF` traces。
- 仿真/执行支持：`Papyrus-RT` 代码生成、Linux RTS、Raspberry Pi 3、GPIO wrapper。
- 验证/分析支持：`Trace Compass`、`Papyrus-RT` animation 与 timing checks。
- 代码生成/转换支持：`Papyrus-RT` 生成 `C++` 代码与 trace point 信息。
- 标准化或社区生态：依托 Eclipse 开源生态、`LTTng`、`Trace Compass` 和 `CTF`。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式系统、机器人平台和 `UML-RT` 建模流程中需要“真实代码运行后仍能回到模型层观察行为”的场景。

### 需求前提

1. 系统已用 `UML-RT` 描述或至少能落到 `Papyrus-RT`。
2. 团队愿意在生成代码阶段插入 trace points。
3. 目标平台支持 `LTTng` / Linux 风格运行时。
4. 关注点包含 timing checks、trace replay 或 model-level runtime explanation。

### 不适用或高成本场景

若系统无法部署 `LTTng`、并非 `Papyrus-RT/UML-RT` 工作流，或更关注离线形式证明而非运行时监控，这条路线价值会下降。

## 与相邻形式主义的关系

相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，本文更强调 trace collection 与 model-level animation；相对 [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)，它更偏 runtime monitoring，而不是 system/environment 模块化部署；相对 [symbolic-execution-of-uml-rt-state-machines/desc.md](../symbolic-execution-of-uml-rt-state-machines/desc.md)，它处理真实运行 traces，而不是符号路径分析。

## 与本研究的关系

### 对 Project 1 的价值

这篇条目说明，如果未来 `project_1` 输出 `UML-RT` 或相邻状态机，后续不仅可以“验证”，还可以把生成代码实际跑起来，再把真实执行回映到模型层做解释和定位。

### 作为目标形式主义还是中间表示

它更像目标形式主义周边的运行时监控方法，而不是新的中间表示。

### 对需求到模型生成的启发

1. 生成模型时最好同时预留 trace points 与 timing annotations 的位置。
2. 生成-验证-修复闭环中，真实运行 traces 可以成为修复反馈的重要证据。
3. 低成本实物 demonstrator 说明“跑起来再看”不一定要依赖昂贵工业平台。

### 现实限制

它严重依赖 `Papyrus-RT` 与 Linux trace 生态，且强项是运行时观测，不是完备性质证明。

## 重要的相关工作

1. [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：`UML` 直接执行与 design-runtime bridge。
2. [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)：`UML` 验证与部署模块化链路。
3. [symbolic-execution-of-uml-rt-state-machines/desc.md](../symbolic-execution-of-uml-rt-state-machines/desc.md)：`UML-RT` 设计期分析路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 归类理由：论文主体集中在 `Papyrus-RT -> LTTng -> Trace Compass` 的运行时监控方法与集成流程上，属于方法路线而非单纯工具发布。
