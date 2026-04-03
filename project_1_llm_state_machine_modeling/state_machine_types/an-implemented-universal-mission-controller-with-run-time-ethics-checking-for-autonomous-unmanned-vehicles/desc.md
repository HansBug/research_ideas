# 面向自主无人系统的通用任务控制器与运行时伦理检查 / An Implemented Universal Mission Controller with Run Time Ethics Checking for Autonomous Unmanned Vehicles

## 基本信息

- 标题：An Implemented Universal Mission Controller with Run Time Ethics Checking for Autonomous Unmanned Vehicles—A UUV Example
- 中文标题：面向自主无人系统的通用任务控制器与运行时伦理检查
- 作者：Don Brutzman, Robert McGhee, Duane Davis
- 发表：*2012 IEEE/OES Autonomous Underwater Vehicles (AUV 2012)*, pp. 1-8
- DOI：`10.1109/AUV.2012.6380744`
- 链接：https://doi.org/10.1109/AUV.2012.6380744
- 形式主义：`Universal Mission Controller / MEA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`UUV` 任务控制 / `Prolog` mission-control `FSM` engine
- 工具/实现获取方式：原文直接给出 `Rational Behavior Model (RBM)`、`Mission Execution Engine (MEE)`、`Mission Execution Automata (MEA)` 和 `Allegro Prolog` 实现方式；未给公开仓库。
- 标准/格式获取方式：原文的核心承载方式是 structured natural language mission orders、状态图和 `Prolog` mission orders；没有独立交换标准。

## 简报

这篇论文把自主无人系统的 mission control 明确压成一个**可由任务命令专门化的有限状态机执行引擎**。作者不是把任务规划做成黑箱智能体，而是主张顶层 mission control 用显式 `FSM`，由 `Prolog` 实现一个通用 `Mission Execution Engine (MEE)`，再用 structured mission orders 将其特化成 конкретe `UUV` 任务控制器，并在此基础上叠加运行时伦理检查。

- 形式主义定位：面向长时任务执行的 mission-control `FSM` / `MEA`，强调任务顺序、查询、分支和可审计性。
- 构造方式简述：先写结构化自然语言任务命令，再整理成 state graph 和 `Prolog` mission orders，最后由通用 `MEE` 执行。
- 基础设施与场景简述：依托 `RBM` 三层架构、`Allegro Prolog`、任务日志与 exhaustive testing，服务 `UUV` 等自主无人系统的高层任务控制。

```text
自然语言任务命令 -> state graph -> Prolog mission orders -> MEE -> tactical behaviors / mission logs
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. `Rational Behavior Model (RBM)` 三层架构。
2. 顶层 mission control `FSM`。
3. `Mission Execution Automata (MEA)`。
4. `Mission Execution Engine (MEE)`，即通用执行引擎。
5. `Prolog` mission orders。
6. 运行时伦理检查约束。

### 核心抽象

根据原文对 `MEA` 的描述，可保守整理为：

$$
\mathcal{M} = (Q, q_0, F, \Sigma, E, \mathcal{A}, \mathcal{R})
$$

上式中的符号逐项解释如下：

1. `Q` 是任务阶段状态集合。
2. `q_0 \in Q` 是初始任务阶段。
3. `F \subseteq Q` 是终止状态集合，例如 `mission_complete` 或 `mission_abort`。
4. `\Sigma` 是任务命令、查询应答和事件集合。
5. `E \subseteq Q \times \Sigma \times Q` 是状态转移集合。
6. `\mathcal{A}` 是外部 agent 集合，例如战术层行为执行者或环境传感代理。
7. `\mathcal{R}` 是查询 / 命令接口集合，用于让 `FSM` 与外部 agent 交互。

原文还直接给出了 `MEE` 的核心 `Prolog` 规则，可整理为：

$$
\mathrm{execute\_mission} \Leftarrow \mathrm{initialize\_mission} \land \mathrm{repeat} \land \mathrm{execute\_current\_phase} \land \mathrm{done}
$$

上式中的符号逐项解释如下：

1. `\mathrm{execute\_mission}` 表示执行整个任务。
2. `\mathrm{initialize\_mission}` 表示将当前阶段初始化到起始阶段。
3. `\mathrm{repeat}` 表示持续推进阶段执行。
4. `\mathrm{execute\_current\_phase}` 表示读取当前阶段并执行之。
5. `\mathrm{done}` 表示任务到达 `mission_complete` 或 `mission_abort`。

论文进一步把运行时伦理检查写成任务级分支 / 中止逻辑，可保守压成：

$$
\delta_{\mathrm{eth}}(q, a) =
\begin{cases}
q_{\mathrm{abort}}, & \text{if ethical execution is not possible} \\
q', & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `q` 是当前任务阶段。
2. `a` 是当前拟执行命令或任务动作。
3. `q_{\mathrm{abort}}` 是伦理约束触发时的中止状态。
4. `q'` 是伦理检查通过时的正常后继状态。

### 一个最小例子与通俗解释

论文的最小例子是 “area search and sample” 任务：

1. 先去 `Area A` 搜索。
2. 搜索成功则去取样，失败则转去 `Area B`。
3. 再去 `Area C` 与另一台 `UUV` rendezvous。
4. 若某个关键阶段的伦理执行不成立，则直接中止任务。

通俗地说，这个模型像一个“会读任务命令的任务指挥官”：

1. 它不会自己发明目标。
2. 它按任务单逐阶段推进。
3. 每一阶段都能问外部 agent “这个条件是否成立”。
4. 若条件或伦理约束不满足，就切换到别的阶段或终止。

### 运行 / 接受 / 转移语义

该模型的运行语义可以写成：

$$
(q_t, \sigma_t, r_t) \xrightarrow{\delta} q_{t+1}
$$

上式中的符号逐项解释如下：

1. `q_t` 是当前任务阶段。
2. `\sigma_t` 是当前命令、应答或查询结果。
3. `r_t` 是外部 agent 返回的信息。
4. `q_{t+1}` 是下一任务阶段。

论文的语义重点是：**任务控制 FSM 不直接做连续控制，而是通过 queries / commands 协调战术层行为**。因此它非常适合作为高层 mission supervisor。

### 语义边界

这个模型的边界包括：

1. 它解决的是高层 mission control，不是低层连续控制。
2. 其可穷举测试性依赖任务图 loop-free 或有明确循环上界。
3. 伦理检查在文中仍然是较原始的条件约束，不是完整道德推理系统。
4. 对高度连续、强概率或开放世界任务，它仍需要更强的战术层和执行层支撑。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `MEA` 骨架 | `$\mathcal{M} = (Q, q_0, F, \Sigma, E, \mathcal{A}, \mathcal{R})$` | 任务控制器是带外部 agent 交互的 mission `FSM`。 |
| 通用执行规则 | `$\mathrm{execute\_mission} \Leftarrow \mathrm{initialize\_mission} \land \mathrm{repeat} \land \mathrm{execute\_current\_phase} \land \mathrm{done}$` | `MEE` 用少量 `Prolog` 规则实现任务执行主循环。 |
| 伦理分支 | `$\delta_{\mathrm{eth}}(q, a)$` | 伦理约束能在运行时改变任务流向。 |
| 可穷举测试前提 | `$\text{loop-free}(\mathcal{M})$` | loop-free 任务图可通过枚举查询回答做 exhaustive testing。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | mission phases 是显式有限状态。 |
| 事件 / 触发 | 强支持 | 搜索成功/失败、样本获取、伦理可执行性等都触发转移。 |
| 守卫 / 数据 | 中等支持 | 查询应答和约束充当 guards，但不强调复杂数据流。 |
| 层次 | 中等支持 | `RBM` 有战略/战术/执行三层，但顶层 mission graph 本身较扁平。 |
| 并发 / 同步 | 弱支持 | 重点是顺序任务控制。 |
| 时间约束 | 弱支持 | 可以表达阶段推进，但无显式 timed-automata 语义。 |
| 连续动态 / 随机性 | 弱支持 | 连续动态交给战术 / 执行层。 |
| 可执行 / 可验证性 | 强执行、强可审计 | `Prolog` 执行和 exhaustive testing 是本文亮点。 |

### 形式化问题与性质

1. 论文最重要的点，是把 mission order 写成**可执行且可审计的任务控制 FSM**。
2. `MEE` 的价值在于“通用引擎 + 特定任务命令”这一分离方式。
3. 伦理约束不是事后注释，而是进入任务转移逻辑的一等对象。
4. 对 `project_1` 来说，这说明高层任务需求很适合先落成可验证的 phase-based 状态机。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 编写 structured natural language mission orders。
2. 将其整理成 mission state graph。
3. 再把每个 phase 的命令、查询和后继写成 `Prolog` mission orders。
4. 由 `MEE` 在 `Allegro Prolog` 中执行。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. state graph。
2. `Prolog` 规则。
3. mission logs。
4. 伦理约束规则。

### 交换与互操作

互操作重点在：

1. 顶层 `FSM/MEA` 对战术层发命令。
2. 战术层对顶层返回查询应答。
3. 任务日志为 after-action review 和法律追责提供依据。
4. 伦理约束可在不重写全部任务结构的前提下插入现有任务流。

## 配套基础设施

- 建模/编辑工具：任务 state graph、structured natural language orders、`Allegro Prolog`。
- 解析/交换/元模型支持：`Prolog` 任务规则和 mission logs；原文无 XML/JSON 交换标准。
- 仿真/执行支持：`RBM` 三层架构、human tactical officer simulation、真实 UUV/UGV 背景。
- 验证/分析支持：loop-free 情况下的 exhaustive testing、任务日志、人工审查。
- 代码生成/转换支持：从结构化任务命令整理到 `Prolog` mission orders 的人工转换链。
- 标准化或社区生态：依托 mission planning / UUV 控制研究生态，本身不是开放工业标准。

## 适用场景与需求前提

### 适用场景

适合长时、自主无人系统的高层任务控制，例如 `UUV` 巡航、区域搜索、取样、会合和受规则约束的任务执行。

### 需求前提

1. 任务可拆成有限阶段。
2. 阶段之间的转移条件可以显式提问和回答。
3. 低层行为已经存在并可由上层调用。
4. 任务责任链、可审计性或伦理约束是重要需求。

### 不适用或高成本场景

若任务需要复杂连续最优控制、强概率决策或大规模并发协同，仅靠顶层 `MEA/MEE` 不够，还需要更强的下层模型或规划器。

## 与相邻形式主义的关系

相对普通 `FSM`，它把外部 agent、查询和任务日志纳入了 mission-control 语境；相对 `MissionLab/CDL` 一类任务编排工具，它更强调形式执行规则与可审计性；相对通用 AI planner，它牺牲了开放性，换来任务控制的透明性和责任链清晰度。

## 与本研究的关系

### 对 Project 1 的价值

它为 `project_1` 提供了一个强证据：高层任务需求可以先被整理成结构化 phase-based 状态机，再去连接执行与验证。

### 作为目标形式主义还是中间表示

它更适合作为高层中间表示或任务监督器目标表示，而不是底层控制器的最终形式主义。

### 对需求到模型生成的启发

1. 自然语言 mission orders 可以先转成阶段图，再落到可执行规则。
2. 查询与条件应答适合成为状态转移 guard 的来源。
3. 伦理 / 安全约束可以作为额外分支逻辑叠加，而不必重写整个任务模型。
4. 若目标是闭环验证与修复，可审计日志非常重要。

### 现实限制

它依赖清晰的 phase decomposition 和明确的外部 agent 接口；若需求本身模糊或高度连续，建模成本会明显上升。

## 重要的相关工作

- `Mission Execution Automata` 早期报告：本文明确继承其理论主线。
- `RBM`：论文把它作为整体机器人软件架构基础。
- 通用图灵机 / `Prolog`：作者用它们论证 `MEE` 的可执行语义基础。
- 真实 UUV/UGV 任务执行实验：文中作为 `RBM` 有效性的外部佐证。

## 文献分类总结

- 这是一篇 `📦` 类 mission-control 条目，重点是可执行任务状态机与规则化任务命令，而不是连续控制算法。
- 它主要描述无人系统的控制 / 反应式逻辑，因此记为 `🎛️`；场景是自主无人载具任务执行，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“自然语言任务命令如何压成可执行、可测试、可审计的高层状态机”这条非常关键的路线。
