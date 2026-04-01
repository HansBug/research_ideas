# 二维自动机理论综述 / A Survey of Two-Dimensional Automata Theory

## 基本信息

- 标题：A Survey of Two-Dimensional Automata Theory
- 中文标题：二维自动机理论综述
- 作者：Katsushi Inoue，Itsuo Takanami
- 发表：`Information Sciences`, Volume 55, Issues 1-3, 1991
- DOI：`10.1016/0020-0255(91)90008-I`
- 链接：https://doi.org/10.1016/0020-0255(91)90008-I
- 综述主题：二维 tape 上 automata 家族的控制能力、方向限制、封闭性、判定性与空间复杂度
- 对象类型：🧱
- 覆盖时间范围：从 `1967` 年 `Blum-Hewitt` 的二维 tape 模型起，主体覆盖到 `1980s` 末
- 覆盖主类：🧩
- 补充材料/数据获取方式：原文正文与参考文献链为主，无单独数据集、代码库或工具包
- 原文是否给出系统比较表：部分给出，主要以章节化结果与命题链组织，不是现代综述式大总表

## 综述范围与结论

这篇 survey 的核心不是介绍某一个二维 automaton，而是把“二维输入面上的自动机究竟有哪些主流控制方式”压成一张理论地图。原文先把二维输入统一为矩形 tape，再比较 alternating、nondeterministic、deterministic 三类二维图灵机及其有限自动机/marker automata 特例，随后补上 `3-way vs 4-way`、空间复杂度、封闭性、判定问题、connected pictures 识别，最后把 cellular 类型的二维自动机单独拉出一章。

- 覆盖范围：`2D Turing Machines`、`2D Finite Automata`、`Marker Automata`、方向受限扫描模型、cellular types of `2D Automata`
- 主要比较轴：控制能力（alternation / nondeterminism / determinism）、头移动方式（`3-way / 4-way`）、复杂度、封闭性、判定性、顺序扫描 vs cellular 并行更新
- 对本 collection 的直接价值：它不是控制系统常见模型，但非常适合校准“当输入从线性串升级为二维结构时，自动机本体会怎样变形，哪些能力是由扫描方向和并行更新引入的”

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🧩 | `2D Alternating Turing Machines` | 重点 | 定义对象 | 用来建立二维环境中最强的一类控制模型与复杂度上界 |
| 🧩 | `2D Nondeterministic / Deterministic Turing Machines` | 重点 | 对比对象 | 原文大量结果围绕 alternating、nondeterministic、deterministic 三者差异展开 |
| 🧩 | `2D Finite Automata` | 重点 | 定义对象 | 作为有限控制、无额外工作带的核心离散模型 |
| 🧩 | `Marker Automata` | 一般 | 扩展对象 | 作为二维有限自动机的一类增强模型参与比较 |
| 🧩 | Cellular types of `2D Automata` | 一般 | 扩展对象 | 作为与顺序扫描路线不同的并行局部更新分支收束到最后一章 |

## 分类轴与比较框架

原文真正的组织主轴有四条：第一条是**控制能力轴**，看 alternation、nondeterminism、determinism 在二维输入上的差距；第二条是**移动约束轴**，看 `3-way` 与 `4-way` 能否替代彼此；第三条是**理论性质轴**，看空间复杂度、封闭性和判定问题；第四条是**执行范式轴**，看顺序扫描模型与 cellular 并行模型的差别。

| 比较对象 | 主要增强点 | 原文重点比较维度 | 优势 | 代价或限制 |
|---|---|---|---|---|
| `2D ATM` | 在二维扫描上叠加 alternation | 表达力、空间复杂度 | 能统一表达较强的并行分支控制 | 理论强、工程载体弱，远离直接建模落地 |
| `2D NTM / DTM` | 非确定/确定控制 | `3-way` vs `4-way`、封闭性、判定问题 | 比较口径清晰，适合作为二维顺序扫描基线 | 一旦限制移动方向，表达力和判定性会显著变化 |
| `2D Finite Automata` | 去掉工作带，仅保留有限控制 | 图片识别能力、connected picture 识别 | 最接近“有限状态 + 图案输入”的纯自动机模型 | 相比图灵机表达力有限，很多性质取决于 head movement |
| `Marker Automata` | 在二维有限自动机上增加标记能力 | 与普通 `2D FA` 的能力边界 | 提供更强的局部导航和识别手段 | 仍缺少稳定的工程生态和统一承载格式 |
| Cellular types | 把扫描换成并行局部更新 | 顺序 vs 并行、局部规则传播 | 更适合表达二维局部相互作用 | 与顺序 head-based 模型语义差异大，不能直接互换 |

原文给出的总体判断很明确：二维输入一旦引入，模型间的能力差别不再只是“状态多一点还是少一点”，而是会被**移动方向**、**是否有工作带**、**是否允许 alternation** 和 **是否采用 cellular 并行更新** 这几类结构约束重新分层。

## 构造方式与表示格式版图

| 形式主义 | 图形表示 | 文本/DSL | XML/JSON/元模型 | 标准/交换格式 | 说明 |
|---|---|---|---|---|---|
| `2D Turing Machines` | 否 | 数学元组定义 | 否 | 无 | 原文使用状态集合、输入字母表、工作带字母表与移动关系的形式化定义 |
| `2D Finite Automata` | 否 | 数学元组定义 | 否 | 无 | 以二维 tape、head movement 与转移关系为核心，不依赖工程化载体 |
| `Marker Automata` | 否 | 数学元组定义 | 否 | 无 | 仍是理论定义主导，没有机器交换格式路线 |
| Cellular types | 可视化网格较自然 | 局部规则函数 | 否 | 无 | 更像“格点 + 邻域 + 局部更新规则”，但原文没有标准化承载方案 |

这篇 survey 对构造方式的价值在于：它非常明确地说明这些模型的主承载方式是**数学定义**，不是图形 DSL、不是 XML、也不是某种标准元模型。对于 `project_1` 而言，这意味着如果未来要借鉴二维 automata 的思想，中间表示必须自己显式承载二维网格、head movement 或局部邻域规则，而不能期待现成交换格式。

| 路线 | 建模入口 | 机器承载 | 自动生成时最难补齐的信息 | 原文体现 |
|---|---|---|---|---|
| 顺序扫描二维 automata | 二维 tape + head movement + 状态转移 | 理论元组 | 扫描方向约束、marker/working tape 语义 | 这些正是原文大部分比较结果的来源 |
| Cellular types | 网格状态 + 邻域 + 同步更新规则 | 理论元组 / 规则表 | 邻域定义、局部规则、同步更新口径 | 原文把其视为另一条二维自动机分支，而非顺序模型的小改版 |

## 基础设施与生态版图

| 形式主义 | 典型工具/平台 | 支持能力 | 生态成熟度 | 备注 |
|---|---|---|---|---|
| `2D Turing Machines` | 原文未系统比较 | 主要是理论分析 | 低 | 以复杂度与判定性文献链为主 |
| `2D Finite / Marker Automata` | 原文未系统比较 | 主要是图片语言与识别理论 | 低 | 没有形成类似 `UPPAAL` 这种验证工具谱系 |
| Cellular types | 原文仅概述模型族 | 理论建模与局部规则分析 | 中 | 与更大的 cellular automata 社区相连，但此文不做工具盘点 |

这篇 survey 的生态信息很薄弱，但这本身也是重要结论：二维 automata 主线更像**理论模型谱系**，而不是**成熟工程基础设施**。如果把它们纳入 `state_machine_types/`，后续更适合补“定义型与判定边界型”论文，而不是优先找标准或交换格式。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 不适合的情况 |
|---|---|---|---|
| `2D Finite / Marker Automata` | 图片语言、二维模式识别、connected picture 识别 | 输入天然是矩形或可规则化的二维结构 | 输入本质是层次树或时间约束系统 |
| `2D Turing Machines` | 需要分析二维输入上的可计算性或空间复杂度 | 除输入外，还要明确 head movement 和工作带假设 | 只想做工程化建模或直接落地到标准工具 |
| Cellular types | 二维局部相互作用、并行传播机制 | 需求可写成局部邻域更新规则 | 需要显式层次状态、复杂数据变量或标准化交换格式 |

| 需求信号 | 更适合的路线 | 原因 |
|---|---|---|
| 强依赖二维网格邻接关系 | Cellular types | 局部规则和并行传播更自然 |
| 需要研究扫描方向限制带来的能力差异 | `2D FA / Marker Automata` | `3-way / 4-way` 差异是原文主轴 |
| 需要复杂度与可判定性边界 | `2D Turing Machines` | 原文大量结果直接围绕这一点组织 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

二维 automata 不是 `project_1` 的直接首选输出，但它提醒我们：一旦需求对象不是线性事件流，而是二维布局、拓扑邻接或图片式结构，传统层次状态机并不自然，状态机本体可能要换成带网格或局部规则的 automata。

### 对中间表示设计的启发

若未来要容纳二维或局部传播型模型，中间表示至少要显式承载：

1. 输入对象的二维坐标系或邻接关系。
2. head movement 约束或局部邻域定义。
3. 顺序扫描与并行更新这两条语义路线的区分。

### 对后续扩库方向的启发

下一步更值得补的不是方法论文，而是：

1. 二维 automata 的奠基定义论文。
2. 有代表性的 `3-way / 4-way` 能力边界论文。
3. 二维 cellular types 的基础定义论文。

### 原文未覆盖但本研究仍需补的空白

原文几乎不涉及工程化文件承载、标准、DSL 或工具互操作，因此它能回答“模型家族是什么”，但回答不了“如何作为 `project_1` 的机器可处理交付格式”。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1967 | `2D Automata` 起点 | Blum, Hewitt, `Automata on a Two-Dimensional Tape` | 二维 tape 自动机主线的共同起点 | 优先补单篇 `desc.md` | 🔴 |
| 1977 | 二维有限自动机能力边界 | Blum, Sakoda, `On the Capability of Finite Automata in 2 and 3 Dimensional Space` | 直接支撑二维有限自动机表达边界比较 | 优先补单篇 `desc.md` | 🟠 |
| 1980 | cellular types / one-way 路线 | Dyer, `One-Way Bounded Cellular Automata` | 把二维/局部并行路线与受限传播能力联系起来 | 先找原文并评估是否入库为 `desc.md` | 🟡 |

## 文献分类总结

- 综述主题：二维 automata 家族的控制能力、方向限制与判定边界
- 对象类型：🧱
- 覆盖主类：🧩
- 覆盖的形式主义：`2D Turing Machines`、`2D Finite Automata`、`Marker Automata`、cellular types
- 是否覆盖构造方式/基础设施：部分覆盖，重心在数学定义，工程基础设施基本缺席
- 主要价值：把二维输入上的自动机家族按控制能力、移动方向、复杂度和判定性统一进一张理论地图
- 状态：🟢
