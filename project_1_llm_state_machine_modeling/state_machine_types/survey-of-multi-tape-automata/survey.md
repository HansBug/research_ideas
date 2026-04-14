# 多带自动机综述 / A Survey of Multi-Tape Automata

## 基本信息

- 标题：A Survey of Multi-Tape Automata
- 中文标题：多带自动机综述
- 作者：Carlo A. Furia
- 发表：`CoRR`, `abs/1205.0178`, 2012
- DOI：原文未提供 DOI
- 链接：https://arxiv.org/abs/1205.0178
- 综述主题：多带自动机的表达力、封闭性、判定问题，以及同步/异步与回退/反转的系统比较
- 对象类型：🧱
- 覆盖时间范围：从 `Rabin-Scott / Elgot-Mezei / Rosenberg` 一线经典工作回顾到 `2012` 年前后的性质总结
- 覆盖主类：🧩
- 补充材料/数据获取方式：原文正文为 survey 主体，并在末尾附交算法作为附加贡献
- 原文是否给出系统比较表：是，目录和总结章节本身就是围绕 expressiveness / closure / decidability 三张对照口径组织

## 综述范围与结论

这篇 survey 的价值在于，它把本来很容易碎成许多小变体的多带自动机统一成了一个参数化家族：带数 `n`、同步度 `s`、反转界 `r`、是否允许 rewind、是否确定。原文先给出统一定义和弱包含关系，再把性质分成 synchronized 与 asynchronous 两大块，分别比较表达力、封闭性与可判定性，最后再给一个总表收束。

- 覆盖范围：synchronous / asynchronous、one-way / two-way、rewind-bounded / reversal-bounded、deterministic / nondeterministic 多带自动机
- 主要比较轴：同步约束、head reversal、rewind、determinism、closure、decidability
- 对本 collection 的直接价值：它非常适合帮助我们理解“多输入序列之间的关系”应该用什么类型的 automata 承载，以及为什么 convolution 路线只覆盖同步子类

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🧩 | synchronous multi-tape automata | 重点 | 定义对象 | 原文证明它们本质上可约到 convolution 上的 regular languages |
| 🧩 | asynchronous multi-tape automata | 重点 | 定义对象 | 作为真正更强的多带 automata 主体 |
| 🧩 | one-way / two-way classes | 重点 | 比较对象 | 通过 reversal 能力决定表达差异 |
| 🧩 | rewind-bounded classes | 一般 | 扩展对象 | 作为 reversals 的受限特例参与比较 |
| 🧩 | deterministic / nondeterministic variants | 重点 | 比较对象 | 原文系统讨论二者能否互相替代 |

## 分类轴与比较框架

这篇 survey 的组织方式几乎就是多带 automata 的分类法本身。第一条轴是**同步度**：synchronous vs asynchronous。第二条轴是**移动能力**：one-way、reversal-bounded、two-way。第三条轴是**控制方式**：deterministic vs nondeterministic。第四条轴是**理论结果类型**：expressiveness、closure、decidability。

| 形式主义 / 路线 | 主要增强点 | 原文比较维度 | 优势 | 代价或限制 |
|---|---|---|---|---|
| synchronous classes | 所有 heads 保持有限同步差 | convolution、regularity、closure | 可转成 regular language 问题，理论非常稳 | 表达不了真正异步关系 |
| asynchronous classes | heads 可停在任意不同位置 | expressiveness、closure、decidability | 能表达更一般的 word relation | 许多闭包与判定性质立刻变差 |
| one-way classes | 不允许向左 | determinization、closure | 结构简单，适合关系识别基线 | 能力受限 |
| rewind-bounded classes | 只允许整批 rewind | 与 nondeterminism 的替代关系 | 比一般 two-way 更受控 | 不能完全替代 reversals 或 nondeterminism |
| full two-way classes | 可任意左右移动 | expressiveness / decidability | 能力最强 | 判定性最不稳定 |

原文的关键结论之一是：**同步多带自动机本质上还是“regular-on-convolution”世界的一部分，而异步多带自动机才真正进入更强的关系语言世界**。这对选型非常重要。

## 构造方式与表示格式版图

| 形式主义 | 图形表示 | 文本/DSL | XML/JSON/元模型 | 标准/交换格式 | 说明 |
|---|---|---|---|---|---|
| multi-tape automata 统一定义 | 否 | 状态机元组 | 否 | 无 | 以 `⟨Σ, Q, δ, q0, F⟩` 和多头读带语义为核心 |
| synchronous classes | 否 | convolution 视图 + automaton 定义 | 否 | 无 | 同步子类可转成 padded alphabet 上的 regular language |
| asynchronous classes | 否 | 多头独立位置 + 转移关系 | 否 | 无 | 机器承载仍是理论元组，不依赖工业标准 |
| rewind-bounded classes | 否 | 在元组语义上增加 rewind 约束 | 否 | 无 | 是反转能力的受限变体，而不是新交换格式 |

这篇 survey 在构造方式上最有价值的一点是，它把 convolution 说清楚了：只有同步子类才天然适合投影到统一串表示。异步子类则必须在机器承载里保留“每个 tape 一个 head 位置”的独立状态。

| 路线 | 建模入口 | 机器承载 | 自动生成最关键的信息 | 原文体现 |
|---|---|---|---|---|
| synchronous multi-tape | 多个输入串 + 同步差界 | padded convolution 或同步多头机 | 各 tape 的对齐口径 | 这是原文把同步类压成 regular language 的基础 |
| asynchronous multi-tape | 多个输入串 + 独立 head | 多头机配置 | 哪些 head 可以独立推进或回退 | 这是表达力提升的主要来源 |
| rewind / reversal-bounded | 多头机 + 移动约束 | 多头机配置 | 允许多少次回退或反转 | 原文大量性质结果围绕此参数变化 |

## 基础设施与生态版图

| 形式主义 | 典型工具/平台 | 支持能力 | 生态成熟度 | 备注 |
|---|---|---|---|---|
| synchronous multi-tape | regular language / relation 工具链可部分复用 | 关系建模、闭包分析 | 中 | 因 convolution 可回到熟悉的 automata 工具口径 |
| asynchronous multi-tape | 原文未系统比较工具 | 主要是理论分析 | 低 | 缺少统一标准工具生态 |
| application links | automatic structures、string DB、computational linguistics | 说明可用方向 | 中 | 原文把这些当应用背景，而不是工具目录 |

原文给出了一些应用入口，但没有形成类似标准化语言或成熟编辑器生态。对本 collection 而言，这意味着多带 automata 更像**关系建模本体**，不是标准/工具线。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 不适合的情况 |
|---|---|---|---|
| synchronous multi-tape automata | 多串对齐、同步比较、关系识别 | 各输入之间有稳定对齐口径 | 输入间存在强异步或自由停顿 |
| asynchronous multi-tape automata | 一般字符串关系、自动结构、复杂查询 | 需求允许不同输入独立推进 | 希望复用 regular-on-convolution 工具链时 |
| rewind-bounded classes | 需要有限次全局重扫 | 需求明确只需少量 rewind | 需要任意两向移动或复杂局部回退 |
| deterministic classes | 可预测、结构更清楚的 relation 识别 | 需求不依赖 nondeterministic 分支 | 表达力必须覆盖更复杂关系时 |

| 需求信号 | 更适合的路线 | 原因 |
|---|---|---|
| 多输入之间天然可按位置对齐 | synchronous classes | 可直接用 convolution 表达 |
| 需要表达非对齐关系 | asynchronous classes | heads 独立推进能力是关键 |
| 只允许有限次重扫 | rewind-bounded classes | 比 full two-way 更受控 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

如果未来 `project_1` 需要把多个需求文本流、多种事件轨迹或多个观测序列联合建模，多带 automata 是比普通 FSM 更自然的“关系型状态机”候选。

### 对中间表示设计的启发

中间表示至少应区分：

1. 是否要求跨输入同步。
2. 是否允许 head 独立前进。
3. 是否允许 rewind 或左右反转。

否则就无法决定能否降回 convolution + regular language 的稳定子类。

### 对后续扩库方向的启发

下一步更应补：

1. generalized finite automata relation 主线。
2. multitape one-way relation 经典论文。
3. automatic structures 相关代表性本体论文。

### 原文未覆盖但本研究仍需补的空白

原文几乎不涉及可执行建模 DSL、交换格式或工业工具，因此它能回答“关系型 automata 家族有哪些变体”，但不能直接回答“如何作为工程建模工件落地”。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1965 | relation / multi-tape 基线 | Elgot, Mezei, `On Relations Defined by Generalized Finite Automata` | 多带 automata 与 rational relations 的经典起点 | 优先补单篇 `desc.md` | 🔴 |
| 1968 | one-way nonwriting multi-tape | Fischer, Rosenberg, `Multitape One-Way Nonwriting Automata` | 连接 one-way 多带机与 relation 识别能力的早期主线 | 优先补单篇 `desc.md` | 🟠 |
| 2012 | async one-way intersection | Furia, survey 中的 intersection algorithm 线 | 说明异步 one-way 子类为何不闭合于 intersection，以及工程上怎么近似处理 | 先补方法/工具备注条目 | 🟡 |

## 文献分类总结

- 综述主题：多带 automata 的同步度、移动能力与判定边界
- 对象类型：🧱
- 覆盖主类：🧩
- 覆盖的形式主义：synchronous / asynchronous、one-way / two-way、rewind-bounded、reversal-bounded、deterministic / nondeterministic 多带自动机
- 是否覆盖构造方式/基础设施：部分覆盖，统一机器定义和 convolution 承载解释很清楚，但标准/工具生态弱
- 主要价值：把多带 automata 家族压成一套可比较的参数化谱系，适合做关系型自动机入口
- 状态：🟢
