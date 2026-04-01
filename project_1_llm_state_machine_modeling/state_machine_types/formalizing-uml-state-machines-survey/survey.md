# 面向自动验证的 UML 状态机形式化综述 / Formalizing UML State Machines for Automated Verification -- A Survey

## 基本信息

- 标题：Formalizing UML State Machines for Automated Verification -- A Survey
- 中文标题：面向自动验证的 UML 状态机形式化综述
- 作者：Etienne Andre，Shuang Liu，Yang Liu，Christine Choppy，Jun Sun，Jin Song Dong
- 发表：`ACM Computing Surveys`, 55(13s), 2023
- DOI：`10.1145/3579821`
- 链接：https://doi.org/10.1145/3579821
- 综述主题：`UML behavioral state machines` 的形式化路线、特征覆盖与工具支持
- 对象类型：🛠️
- 覆盖时间范围：1997 年 `UML 1.1` 正式发布至 2021 年底
- 覆盖主类：🧩 📦
- 补充材料/数据获取方式：原文本身包含系统性文献检索与大量对比表
- 原文是否给出系统比较表：是，原文以多张对比表汇总语法覆盖、工具支持、可用性与路线差异

## 综述范围与结论

这篇 survey 是 `UML State Machine` 形式化路线的总账。它不是只讲少数几篇经典论文，而是通过系统性文献回顾筛出 `61` 篇工作，把它们分成“翻译到既有形式语言”的间接路线和“直接给 UML 状态机操作语义”的直接路线，并专门审视这些路线的工具是否还存在。

- 覆盖范围：`UML State Machine` 语义形式化、translation approaches、operational semantics、工具可用性
- 主要比较轴：直接/间接路线、目标形式语言、UML 版本、语法覆盖、工具支持与长期可用性
- 对本 collection 的直接价值：它能帮助 `project_1` 判断 `UML State Machine` 更适合做“用户可读前端”，还是“真正的验证中间表示/最终输出”

## 覆盖的形式主义版图

| 主类 | 形式主义 | 覆盖深度 | 文中角色 | 关键说明 |
|---|---|---|---|---|
| 🧩 | UML behavioral state machines | 重点 | 定义对象 | 整篇 survey 的核心对象 |
| 🧩 | Harel statecharts | 一般 | 背景对象 | 作为 UML 状态机的历史来源与差异参照 |
| 📦 | XMI / tool-specific carriers | 一般 | 承载对象 | 多个工具以 `XMI` 作为输入载体 |
| 📦 | Translation targets (`PROMELA`、`SMV`、`Uppaal`、Petri nets、ASM) | 重点 | 对比对象 | 用来解释 UML 形式化为何长期依赖外部验证器 |

## 分类轴与比较框架

原文的比较框架主要有五个层面：

1. 路线维度：translation-based 间接路线 vs. direct operational semantics 直接路线。
2. 语法维度：entry/exit/do、history、fork/join、deferred events、`run-to-completion` 等是否被支持。
3. 版本维度：`UML 1.x` 与 `UML 2.x` 的语义差异是否被处理。
4. 工具维度：是否有自动验证工具、是否支持 counterexample、工具今天是否还能获取。
5. 工程维度：语义是否接近标准、是否存在 soundness gap、是否能把反例映射回 UML 模型。

这篇 survey 的强点在于，它不仅看“有没有论文”，还看“能不能真的用”。

## 构造方式与表示格式版图

| 形式主义 | 图形表示 | 文本/DSL | XML/JSON/元模型 | 标准/交换格式 | 说明 |
|---|---|---|---|---|---|
| UML State Machine | 是 | 动作、守卫、事件文本 | 常见承载为 `XMI` | `OMG UML` | 语法丰富但标准语义主要是自然语言 |
| Translation route | 否 | `PROMELA`、`SMV`、`Uppaal`、`B`、`ASM`、Petri nets 等 | 依目标语言而异 | 否 | 多数验证工作真正依赖这些后端语言 |
| Direct semantics route | 否 | SOS / inference rules / dedicated semantics | 原文未强调统一机器交换格式 | 否 | 语义更贴近 UML，但工具较少 |

从构造方式上看，`UML State Machine` 的最大问题不是“画不出来”，而是“标准语义并不天然适合自动验证”。因此大量工作都要先把 UML 变成别的形式。

## 基础设施与生态版图

| 形式主义 | 典型工具/平台 | 支持能力 | 生态成熟度 | 备注 |
|---|---|---|---|---|
| UML front-end + external checker | `vUML`、`hugo`、`hugo/RT`、`TABU`、`PROCO` | 翻译到 `Spin`、`SMV`、`Uppaal` 等后端 | 中 | 大多是研究原型 |
| Dedicated operational tools | `USMMC`、`AnimUML`、`EMI-UML` | 直接按 UML 语义做验证或执行 | 中 | 语义更贴近 UML，但数量少 |
| Commercial modeling tools | `Papyrus`、`Rhapsody`、`Yakindu` 等 | 图形建模为主 | 高 | 原文认为其形式验证学术基础公开不足 |

原文最有价值的生态观察是：绝大多数学术工具都已经失联，只剩少数仍可获取和维护的项目，如 `hugo/RT`、`AnimUML`、`EMI-UML`。

## 适用场景与需求映射

| 形式主义 | 适用场景 | 需求前提 | 不适合的情况 |
|---|---|---|---|
| UML State Machine 作为前端 | 软件设计、对象行为建模、与工程团队沟通 | 需要图形化、对象导向、工业熟悉度 | 希望直接把标准自然语言语义送入验证器 |
| Translation-based verification | 希望复用成熟后端验证器 | 可接受把 UML 映射到外部形式语言 | 无法接受语义差异或反例不回写 UML 时 |
| Direct operational semantics | 希望保留更多 UML 语义细节 | 愿意使用较专门的工具或语义框架 | 需要立即接入广泛成熟生态时 |

## 对本研究的启发

### 对 Project 1 目标形式主义选型的启发

`UML State Machine` 很适合作为“研究结果对人展示的表层形式”，因为它有工业熟悉度、图形性强、沟通成本低。但若它还承担“自动验证入口”的职责，就必须选定一个明确的语义 profile，而不能只说“符合 OMG 标准”。

### 对中间表示设计的启发

如果 `project_1` 未来把 UML 作为输出或中间层，至少要固定以下要素：

1. 事件队列与 `run-to-completion` 的精确定义。
2. entry/exit/do 与 transition effect 的执行顺序。
3. history、fork/join、deferred events 的语义边界。
4. 与后端验证器之间的可追溯映射。

### 对后续扩库方向的启发

后续补库不应只看“UML 标准”本身，还要沿三条线一起补：

1. 标准线：`OMG UML` 规范与关键语义条款。
2. 形式化线：translation vs. direct operational semantics。
3. 工具线：`hugo/RT`、`AnimUML`、`EMI-UML` 这类仍可用工具。

### 原文未覆盖但本研究仍需补的空白

原文也指出，时间和概率扩展仅被少数工作触及，`fUML`、`SysML`、`MARTE` 与工业实践间的衔接仍值得单独补库。因此，对控制系统研究而言，UML 线后续还要与实时/定量扩展重新对接。

## 应追踪的代表原始文献

优先级口径：`🔴` 高优先级，`🟠` 次高优先级，`🟡` 中优先级，`⚪` 背景跟踪。

| 年份 | 形式主义 / 方向 | 代表原始文献 | 推荐原因 | 后续动作 | 优先级 |
|---:|---|---|---|---|---|
| 1997 | UML standard | `OMG UML 1.1` specification | 形式化工作的时间边界和标准起点 | 先找规范或权威版本说明 | 🟡 |
| 1999 | UML + model checking | Lilius, Paltor, `Formalising UML State Machines for Model Checking` | 早期 UML 形式化主线入口 | 优先补单篇 `desc.md` | 🔴 |
| 2001 | Tool line | Knapp et al., `hugo` | 代表翻译到 `PROMELA/Spin` 的工具路线 | 先找原文并补工具条目 | 🟠 |
| 2013 | Direct operational semantics | Liu et al., `USMMC` / corresponding semantics paper | 代表较完整的 UML 直接语义与验证路线 | 优先补单篇 `desc.md` | 🟠 |
| 2017 | Standard semantics | `OMG UML 2.5.1` specification | 当前更稳定的 UML 标准参考点 | 优先补标准条目 | 🔴 |
| 2021 | Tool line | Jouault et al., `AnimUML` | 代表仍活跃、可用的现代 UML 验证工具 | 先补工具条目 | 🟠 |

## 文献分类总结

- 综述主题：UML 状态机形式化与自动验证
- 对象类型：🛠️
- 覆盖主类：🧩 📦
- 覆盖的形式主义：`UML State Machine`、translation targets、direct operational semantics
- 是否覆盖构造方式/基础设施：是
- 主要价值：把 `UML State Machine` 的两大形式化路线、语法覆盖情况和工具失联问题一次讲清楚
- 状态：🟢
