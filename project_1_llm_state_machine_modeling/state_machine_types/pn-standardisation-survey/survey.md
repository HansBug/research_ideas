# Petri 网标准化综述 / PN Standardisation: A Survey

## 基本信息

- 标题：PN Standardisation: A Survey
- 中文标题：Petri 网标准化综述
- 作者：L. Hillah，F. Kordon，L. Petrucci，N. Treves
- 发表：`Formal Techniques for Networked and Distributed Systems - FORTE 2006`
- DOI：`10.1007/11888116_23`
- 链接：https://doi.org/10.1007/11888116_23
- 综述主题：`Petri Net` 标准化、`PNML` 交换格式与配套实现框架
- 对象类型：🏗️
- 覆盖时间范围：以 1960s 以来的 `Petri Net` 发展为背景，重点讨论截至 2006 年的 `ISO/IEC 15909`
- 覆盖主类：🕸️ 📦
- 补充材料/数据获取方式：原文给出 `PNML Framework`、`GraphViz` 转换示例和标准分部结构
- 原文是否给出系统比较表：原文虽未用一张总表覆盖全部内容，但对 `Part 1 / Part 2 / Part 3`、`Core model / P/T / High-level`、`PNML Framework` 均有清晰结构化说明

## 综述范围与结论

这篇 survey 的核心不是再解释一遍 `Petri Net` 理论，而是回答“如何让不同 Petri 网工具之间能够稳定交换模型”。原文把 `ISO/IEC 15909` 分成语义与图形定义、交换格式 `PNML`、未来扩展三大部分，并强调：如果没有统一术语、统一元模型和统一交换语法，Petri 网社区的工具生态就无法真正互通。

- 覆盖范围：`P/T nets`、`High-level Petri Nets`、`Symmetric Nets`、`PNML`、`PNML Framework`
- 主要比较轴：标准分部职责、抽象语法与具体语法、Petri 网类型层级、标准兼容性与工具本地变体
- 对本 collection 的直接价值：这是本 collection 里少见的“既讲形式主义，又讲元模型、XML、API 和工具互操作”的强基础设施文献

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🕸️ | Place/Transition Nets | 重点 | 定义对象 | 作为 Part 1 与 Part 2 的基础网类 |
| 🕸️ | High-level Petri Nets | 重点 | 定义对象 | 标准化语义、图形与标签体系的重要对象 |
| 🕸️ | Symmetric Nets | 一般 | 扩展对象 | 作为 Part 1 addendum 和高层网受限子类 |
| 🕸️ | Timed / Stochastic / Hierarchical Net extensions | 一般 | 待扩展对象 | 作为 Part 3 方向被明确提出 |
| 📦 | PNML | 重点 | 基础设施对象 | `Petri Net Markup Language`，标准交换格式核心 |

## 分类轴与比较框架

原文的比较和组织方式很清晰，主要有四个轴：

1. 标准分部轴：`Part 1` 定义术语、语义和图形；`Part 2` 定义交换格式；`Part 3` 面向扩展。
2. 类型层级轴：`Core model -> P/T Systems -> High-level Petri Nets -> local variations / future extensions`。
3. 语法层次轴：先做 metamodel 级抽象语法，再映射到 `PNML` 具体语法。
4. 工具互操作轴：标准本体、局部变体、兼容性、版本迁移、语义约束 enforcement。

对 `project_1` 最重要的是第三轴和第四轴：它说明了一个成熟形式主义不只是“有定义”，还需要 `metamodel + schema + validation + API` 一整条链路。把这些对象展开后，可以更清楚地看到，文章不是单纯在讲“一个 XML 格式”，而是在讲**标准化分工**：

| 对象 | 主要职责 | 解决的问题 | 承载层级 | 原文强调的限制/后续工作 |
|---|---|---|---|---|
| `Part 1` | 术语、语义、图形记法、本体网类 | 先统一“什么是标准 Petri 网对象” | 形式主义定义层 | 高层网与扩展网类仍需继续细化 |
| `Part 2` | `PNML` 交换格式 | 让不同工具能交换模型 | 抽象语法 -> XML 具体语法 | 需要兼顾主流网类、局部方言和未来扩展 |
| `Part 3` | 扩展标准化方向 | 时间、随机、层次等扩展 | 扩展规划层 | 在论文写作时仍主要是 future work，不算成熟部分 |
| `PNML Core Model` | 抽象语法公共骨架 | 统一 nodes、arcs、labels 等共性对象 | 元模型层 | 只解决共性骨架，不自动解决高层标签语义 |
| `PNML Framework` | 把标准变成可集成 API | 让工具开发者真的能 import/export | 实现/API 层 | 仍需跟随标准演化，并逐步补足更多网类 |

| 维度 | 仅有形式主义定义 | 有 `PNML` 抽象/具体语法 | 有 `PNML Framework` 参考实现 |
|---|---|---|---|
| 能否统一术语与对象 | 是 | 是 | 是 |
| 能否稳定交换模型 | 否 | 是 | 是 |
| 能否直接接入工具开发 | 否 | 部分 | 是 |
| 能否处理局部变体/未来扩展 | 弱 | 中 | 中到强 |
| 对 `project_1` 的启发 | 只够“定义模型” | 已能“承载模型” | 才真正接近“可工程落地的基础设施” |

## 构造方式与表示格式版图

这篇 survey 在“构造方式与承载格式”上信息密度非常高。

| 对象 | 图形表示 | 文本/标签承载 | 元模型/Schema | 标准/交换格式 | 原文给出的关键说明 |
|---|---|---|---|---|---|
| `P/T Nets` | 是 | 基本无复杂标签 | `UML` class diagram 元模型可承载 | `ISO/IEC 15909-1/2` | 是整个层级的基础根类 |
| High-level Petri Nets | 是 | 标签、函数、代数表达式 | 元模型 + 高层标签约束 | `ISO/IEC 15909-1/2` | 难点在“如何既表达语义又保证互操作” |
| Symmetric Nets | 是 | 受限代数表达 | 元模型扩展 | Part 1 addendum | 被当成高层网标准化的可控切口 |
| `PNML Core Model` | 否 | 否 | `UML metamodel` + `OCL` 约束 | `PNML` | 负责所有网类共享骨架，而不是具体网语义细节 |
| `PNML` concrete syntax | 否 | 否 | `RELAX NG` schema | `PNML` | 把抽象语法映射成 XML 交换格式 |

| 阶段 | 产物 | 作用 | 缺什么就会出问题 |
|---|---|---|---|
| 本体定义 | `Part 1` 里的网类、语义、图形 | 统一研究对象 | 没有本体定义，就没有统一交换的基础 |
| 抽象语法 | `PNML Core Model` | 统一工具之间共享的数据结构 | 没有抽象语法，XML 只会退化成随意标签堆砌 |
| 具体语法 | `RELAX NG` + `PNML` 文档 | 真正交换文件 | 没有 schema，工具无法稳定互导 |
| 受控高层语义 | 标签子语言、受限 `MathML` 思路 | 保证高层网仍可互操作 | 若直接开放任意数学表达，会失去语义一致性 |
| 参考实现 | `PNML Framework` | 把标准变成工具 API | 没有实现，标准很难形成生态效应 |

## 基础设施与生态版图

| 平台/部件 | 主要作用 | 支持能力 | 生态成熟度 | 原文中的关键观察 |
|---|---|---|---|---|
| `CPN-AMI`、`GreatSPN`、`PEP`、`CPN Tools` | Petri 网建模、分析、仿真 | 证明“社区里确实有大量工具需要互操作” | 高 | 它们本身就是标准化需求的现实来源 |
| `PNML Framework` | 标准参考实现 | import/export、约束检查、模型转换、API 集成 | 高 | 不只是 demo，而是面向工具开发者的实用框架 |
| `EMF/Ecore` 路线 | 元模型实现与代码生成 | 把 metamodel 变成可编程 API | 高 | 说明标准化与 model-driven engineering 可直接结合 |
| `GraphViz` converter 等 | 转换与可视化示例 | 帮助理解从私有格式到 `PNML` 的流程 | 中 | 展示标准如何进入工具链，而不只是停留在规范文本 |

| 基础设施层 | 代表对象 | 直接服务谁 | 主要收益 |
|---|---|---|---|
| 规范层 | `ISO/IEC 15909` | 研究者、标准制定者、工具实现者 | 统一术语、网类与语义边界 |
| 数据层 | `PNML` + schema | 工具之间的模型交换 | 统一文件承载与验证 |
| API 层 | `PNML Framework` | 工具开发者 | 降低接入标准的工程成本 |
| 生态层 | 既有 Petri 网工具群 | 整个 Petri 网社区 | 形成互操作和长期演化的现实土壤 |

原文最强的地方在于，它不是停留在“我们应该标准化”，而是已经给出 `PNML Framework` 作为参考实现，打通 `create / save / load / fetch` API。

## 适用场景与需求映射

| 对象 | 适用场景 | 需求前提 | 为什么适合 | 不适合的情况 |
|---|---|---|---|---|
| `P/T Nets` | 并发、同步、离散事件系统建模 | 需要清晰的 place/transition 结构 | 基础网类最稳定，最利于标准化承载 | 需要复杂高层数据但又不愿引入高层标签时 |
| High-level Petri Nets | 结构复杂、数据富集的系统建模 | 接受高层标签、代数表达式与更强工具需求 | 能表达更复杂语义，同时仍尝试纳入标准化 | 只想要轻量交换，不愿处理标签语义时 |
| `PNML` | 多工具之间模型交换、长期存档、互操作 | 需要遵守标准类型层级和 schema | 是 Petri 网社区最明确的交换载体 | 各工具坚持私有方言且不愿对齐语义时 |
| `PNML Framework` | 需要把私有格式与标准格式打通的工具链 | 能接入 Java/EMF 或接受生成 API | 能把标准直接转成开发者可用接口 | 只做一次性脚本转换、不维护长期兼容性时 |

| 需求目标 | 更应该关注的对象 | 原因 |
|---|---|---|
| 只想选一种并发状态机形式主义 | `P/T Nets` / High-level nets | 先把模型本体搞清楚即可 |
| 想让生成结果能长期交换、复用、被多工具消费 | `PNML` | 没有统一承载，后续工具链会很脆弱 |
| 想真正落地到工程工具链 | `PNML Framework` | 只有格式没有 API，还不算可用基础设施 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

如果 `project_1` 后续不仅想“生成一个状态机”，还想“可交换、可验证、可复用”，那么 `Petri Net/PNML` 这条线提供了非常成熟的基础设施思路。它提醒我们：选型不能只看表达力，还要看有没有标准化承载物。

### 对中间表示设计的启发

原文给出的最佳实践非常直接：

1. 先定义抽象语法，不要一开始就绑死到某种序列化格式。
2. 用 schema 映射抽象语法到机器可处理载体。
3. 用约束语言保证语义一致性，而不是仅靠文档说明。
4. 用参考实现让工具生态真正能落地，而不只是纸面标准。

### 对后续扩库方向的启发

本 collection 后续应沿三条线继续补：

1. `Petri Net` 理论与网类主线。
2. `PNML / ISO` 标准与交换格式主线。
3. `Time / Stochastic / Hierarchical` 扩展线。

### 原文未覆盖但本研究仍需补的空白

原文对 `Part 3` 只给出方向，没有给出现成成熟标准，因此时间网、随机网、层次网扩展仍需逐条追踪原始文献和后续标准进展。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1991 | Time Petri Nets | Berthomieu, Diaz, `Modeling and Verification of Time Dependent Systems Using Time Petri Nets` | 直通时间 Petri 网主线，是后续 Part 3 的关键背景 | 优先补单篇 `desc.md` | 🟠 |
| 2004 | Petri 网标准 Part 1 | `ISO/IEC 15909-1` | 标准化术语、语义和图形记法的核心入口 | 优先补标准条目 | 🔴 |
| 2005 | PNML / Part 2 概念线 | Ekkart Kindler, `The Petri Net Markup Language and ISO/IEC 15909-2` | 直接补足 `PNML` 的概念、状态和未来方向 | 优先补单篇 `desc.md` | 🔴 |
| 2006 | High-level Petri Nets | Jensen, Rozenberg (eds.), `High-Level Petri Nets` | 高层网的经典参考源，适合回补形式主义本体 | 优先补单篇 `desc.md` | 🟠 |
| 2006 | PNML 参考实现 | `PNML Framework` project / tool line | 标准真正落地到 API 和工具互操作的关键线索 | 先找工具/文档论文 | 🟡 |

## 文献分类总结

- 综述主题：Petri 网标准化与交换格式
- 对象类型：🏗️
- 覆盖主类：🕸️ 📦
- 覆盖的形式主义：`P/T Nets`、`High-level Petri Nets`、`Symmetric Nets`、`PNML`
- 是否覆盖构造方式/基础设施：是，且覆盖很强
- 主要价值：把 `Petri Net` 从“理论形式主义”延伸到“标准、交换格式、元模型、API 实现”这一整条基础设施链
- 状态：🟢
