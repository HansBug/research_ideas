# 面向过程控制系统的规格语言设计：经验与未来步骤 / Designing Specification Languages for Process Control Systems: Lessons Learned and Steps to the Future

## 基本信息

- 标题：Designing Specification Languages for Process Control Systems: Lessons Learned and Steps to the Future
- 中文标题：面向过程控制系统的规格语言设计：经验与未来步骤
- 作者：Nancy G. Leveson, Mats P. E. Heimdahl, Jon Damon Reese
- 发表：Software Engineering --- ESEC/FSE '99, Lecture Notes in Computer Science 1687, 127-146, 1999
- DOI：`10.1007/3-540-48166-4_9`
- 链接：https://doi.org/10.1007/3-540-48166-4_9
- 形式主义：RSML / SpecTRM-RL
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：需求规格语言
- 工具/实现获取方式：论文明确说明其工具链为 `SpecTRM`，规格语言为 `SpecTRM-RL`，并把它定位成从 `RSML` 继续演化出的实验性工具集。
- 标准/格式获取方式：承载方式是图形状态机、输出消息规格、状态变量定义、transition table、macro 和 function；原文未给出独立交换标准。

## 简报

这篇论文的重点不是“再造一个通用状态机语言”，而是把安全关键过程控制系统真正需要的黑盒需求规格语言做窄、做稳、做可审查。作者从 `RSML` 的使用经验出发，提出 `SpecTRM-RL`：底层仍是 Mealy 自动机，但语言层不再鼓励工程师写通用 `Statecharts` 式设计，而是强制围绕控制器 operating modes、supervisory interface 和 controlled process 三个模型来写需求，并用可读性更高的 and/or tables 代替拥挤的逻辑表达式。

- 形式主义定位：面向安全关键过程控制需求的黑盒状态机式规格语言。
- 构造方式简述：以 Mealy 机为底层模型，用模式图、状态变量表、输出消息表、transition and/or tables、macro 与 function 组织规格。
- 基础设施与场景简述：服务需求审查、完整性检查、安全分析和控制器需求建模，而不是直接做实现设计。

```text
控制需求 -> modes / interface model / process model -> and/or tables + macros -> black-box requirements specification
```

## 形式主义定义与核心对象

### 定义对象

论文的出发点很直接：通用状态机语言允许太多内部设计细节混进需求规格，导致审查困难、语义距离大、内部广播事件错误频发。因此作者要构造一个更克制的黑盒规格语言。

### 核心抽象

论文明确指出 `SpecTRM-RL` 的底层模型仍然是 Mealy 自动机，可写成：

$$
RSM = (Q, \Sigma_{in}, \Sigma_{out}, \delta, \lambda)
$$

上式中的符号逐项解释如下：

1. `Q` 是离散状态集合。
2. `\Sigma_{in}` 是输入集合。
3. `\Sigma_{out}` 是输出集合。
4. `\delta` 是状态转移函数。
5. `\lambda` 是输出函数。

但 `SpecTRM-RL` 不鼓励直接裸写这个自动机，而是把控制软件规格固定成三部分：

$$
Spec = (M_{op}, M_{if}, M_{cp})
$$

其中：

1. `M_{op}` 是 controller operating modes 模型。
2. `M_{if}` 是 controller 对 supervisory interface 的内部模型。
3. `M_{cp}` 是 controlled process 的内部模型。

对于 and/or tables，论文给出的判定直觉可压缩为：

$$
Table = \bigvee_j \bigwedge_i \phi_{ij}
$$

这里：

1. 每一列 `j` 是一个 conjunction。
2. 每个单元 `\phi_{ij}` 记录某个短语为真、为假或 don't care。
3. 只要某一列完全匹配，整张表就为真。

### 一个最小例子与通俗解释

论文第 3 节给了一个非常典型的模式例子：

1. 一个简单状态机有 `s1` 到 `s5` 五个状态。
2. 在 `startup mode` 下，从 `s3` 触发时会去 `s4`。
3. 在 `normal mode` 下，同样从 `s3` 触发时则去 `s1`。

通俗地说，`SpecTRM-RL` 认为“mode 也是一种状态，只是它负责解释其他状态机的行为方式”。同样的触发，在不同 mode 下可以合法地导向不同结果。

### 运行 / 接受 / 转移语义

论文最关键的语义收束之一是：

$$
FC : (M_{op}, M_{if}, M_{cp}, V_c) \mapsto Outputs
$$

上式中的符号逐项解释如下：

1. `FC` 是控制器要实现的 black-box control function。
2. `M_{op}`、`M_{if}`、`M_{cp}` 分别给出 operating modes、supervisory interface 和 controlled process 的内部模型。
3. `V_c` 是受控/监测变量提供的当前信息。
4. `Outputs` 是当前应发出的控制命令或消息。

在 transition 规格层，触发条件不是画在箭头上的几字短注，而是独立表格：

$$
\delta(q, \psi) = q'
$$

其中：

1. `q` 是当前状态或 mode。
2. `\psi` 是 and/or table 表示的复杂触发条件。
3. `q'` 是目标状态。

论文还特别强调：过程状态模型中的状态变量默认应包含 `Unknown` 值，以便系统重启或模式切换后强制重新同步外部世界，而不是想当然沿用旧状态。

### 语义边界

`SpecTRM-RL` 的边界就是“黑盒需求规格”：

1. 它不是通用设计语言，不鼓励写内部实现结构。
2. 它故意删去许多对需求规格无益但对设计很方便的通用状态机自由度。
3. 它服务审查和安全分析，优先级高于表达炫技。

### 关键性质与判定边界

论文强调的关键性质包括：

1. 通过 `modes` 降低需求表达与审查者心智模型之间的语义距离。
2. 用 and/or tables 管理复杂逻辑条件，避免传统命题公式难以审查的问题。
3. 用 `Unknown` 和显式 interface/process models 控制“内部模型与真实系统状态不一致”的安全风险。
4. 通过 macro、function 和 parallel state machines 支持复用与产品族规格。
5. 明确抛弃 `RSML`/`Statecharts` 中高错误率的内部 broadcast events。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | operating modes、interface modes、process state variables 都是核心。 |
| 事件 / 触发 | 强支持 | transition 由事件、条件或时间相关约束触发，但以表格显式给出。 |
| 守卫 / 数据 | 强支持 | and/or tables、state variable definitions、functions 都围绕复杂条件构造。 |
| 层次 | 部分支持 | 通过 parallel state machines、modes 和 macros 形成结构化层次，不追求通用层次状态图花样。 |
| 并发 / 同步 | 部分支持 | 论文更关注多个并行状态机的需求组织，而不是同步执行算法本身。 |
| 时间约束 | 部分支持 | timing constraints 可以进入表格条件，但不是显式时钟自动机。 |
| 连续动态 / 随机性 | 不支持 | 被控过程通过离散状态变量和模式抽象，而非连续方程。 |
| 可执行 / 可验证性 | 强支持 | 目标是审查、完整性检查和安全分析友好的高可信需求规格。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 底层模型 | `$RSM = (Q, \Sigma_{in}, \Sigma_{out}, \delta, \lambda)$` | `SpecTRM-RL` 的形式基础仍是 Mealy 自动机。 |
| 三部分规格 | `$Spec = (M_{op}, M_{if}, M_{cp})$` | 规格必须同时覆盖模式、监督接口和受控过程模型。 |
| 控制函数 | `$FC : (M_{op}, M_{if}, M_{cp}, V_c) \mapsto Outputs$` | 控制输出由三个内部模型和受控变量共同决定。 |
| 表格逻辑 | `$Table = \bigvee_j \bigwedge_i \phi_{ij}$` | and/or tables 把复杂逻辑条件压成可审查表格。 |
| 转移规格 | `$\delta(q, \psi) = q'$` | 状态迁移由表格化条件 `\psi` 控制，而非简单箭头标签。 |

## 构造方式与承载格式

### 建模入口

建模入口由以下部分组成：

1. Graphical state machine。
2. Output message specification。
3. State variable definition。
4. State transition specification。
5. Macros and functions。

### 机器可处理承载方式

机器可处理承载是结构化规格文档与表格：

1. 图形部分负责模式与状态变量骨架。
2. 表格部分负责输出条件与转移条件。
3. macro/function 部分负责复用和域抽象。

### 交换与互操作

论文并不追求开放交换，而是追求“需求表达正确、可审查、可分析”。它更像安全关键需求 DSL，而不是标准交换格式。

## 配套基础设施

- 建模/编辑工具：`SpecTRM` 工具集和 `SpecTRM-RL` 语言。
- 解析/交换/元模型支持：模式图、输出消息表、状态变量表、转移表、macro、function 构成稳定承载。
- 仿真/执行支持：论文重心在需求规格和分析，不主打在线执行环境。
- 验证/分析支持：直接面向 completeness、consistency、safety-oriented review 和模式错误分析。
- 代码生成/转换支持：本文不是代码生成论文，但其结构非常适合后续自动转换到设计/实现模型。
- 标准化或社区生态：以 FAA/TCAS 等安全关键需求实践为背景，影响力集中在 requirements engineering 和安全工程。

## 适用场景与需求前提

### 适用场景

适合安全关键控制系统、过程控制系统、航电或其他需要黑盒高可信需求规格的场景。

### 需求前提

1. 系统要被描述成输入输出控制函数，而不是内部实现设计。
2. 需求中存在清晰的模式、接口状态和被控过程状态。
3. 复杂触发条件需要被审查者直接阅读和确认。
4. 必须控制“软件内部模型与真实受控过程不一致”的安全风险。

### 不适用或高成本场景

如果目标是快速原型设计、通用行为建模或直接部署执行，`SpecTRM-RL` 会显得过于约束和保守。

## 与相邻形式主义的关系

相对 `RSML/Statecharts`，它更克制、更黑盒、更强调需求审查；相对 `SCR/Parnas Tables`，它同样基于 Mealy 机和表格逻辑，但加入了更明确的 process-control 结构与模式分类；相对一般 `Statecharts`，它明确拒绝许多与需求规格无关的表达自由。

## 与本研究的关系

### 对 Project 1 的价值

它非常接近“从非形式化控制需求走向高可信状态机”的前半段工作，为需求规约如何结构化提供了直接参考。

### 作为目标形式主义还是中间表示

更适合作为需求侧高可信中间表示，而不是最终交付给执行引擎的状态机载体。

### 对需求到模型生成的启发

如果未来要让 LLM 从需求文本生成模型，`SpecTRM-RL` 提供了一个很好的模板：先生成 modes、process model、interface model 和 and/or tables，再考虑落到更工程化执行载体。

### 现实限制

它对控制需求分析极有帮助，但与工业执行链之间通常还需要再做一次从 requirements DSL 到 design/executable model 的转换。

## 重要的相关工作

### 奠基或前身工作

- `RSML`
- `Statecharts`
- `SCR`
- `Parnas Tables`

### 同类型或同家族工作

- `SpecTRM`
- 面向产品族和安全分析的需求 DSL

### 标准 / 格式 / 工具链工作

- TCAS/FAA 需求规格实践
- completeness / review / safety analysis 路线

### 与本研究关系最紧的工作

- 它直接说明了“需求规格语言应该如何约束表达自由，才能为后续形式化建模与验证服务”。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 形式主义：RSML / SpecTRM-RL
- 论文角色：需求规格语言
- 核心功能：把安全关键过程控制需求约束成黑盒、表格化、模式驱动的状态机式规格。
