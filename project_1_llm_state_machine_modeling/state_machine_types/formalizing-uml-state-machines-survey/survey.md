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

真正需要保留下来的，不只是“直接路线 vs 间接路线”这一层，而是每条路线在**语法覆盖、语义贴近度、工具可用性、反例可追溯性**上的系统差异。

| 比较对象 | 代表承载/代表工作 | 语义贴近 UML 程度 | 语法覆盖情况 | 工具与自动化 | 反例/可追溯性 | 原文给出的主要问题 |
|---|---|---|---|---|---|---|
| ASM / OMA 一类翻译路线 | `ASM`、`OMA`、attributed graph | 中高 | 在 translation 路线中覆盖面通常较高，某些工作能覆盖 history、deferred events、entry/exit/do 等复杂语法 | 自动翻译工具很少，更多停留在语义刻画 | 通常不强，很多工作没有完整工具链 | 语义表达灵活，但缺少持续维护的自动化实现 |
| 面向既有验证器的翻译路线 | `PROMELA/Spin`、`SMV`、Petri nets、`B`、`Uppaal` | 中 | 原文总结为 translation 路线整体覆盖不完整，没有工作超过约 `65%` 语法覆盖，多数低于 `50%` | 可以复用成熟 model checker，是其最大优势 | 经常断在后端形式语言，难映射回 UML 原模型 | translation soundness 难证明，且语义 profile 往往偏离 UML 标准自然语言语义 |
| 直接操作语义路线 | SOS / inference rules / dedicated semantics | 高 | 原文认为 direct 路线整体覆盖优于 translation 路线，至少两条线接近“近完整 UML 语法” | 可直接驱动专用验证器，但工具数量少 | 理论上最有利于回写到 UML；实践里仍依赖工具实现质量 | 工具稀少、实现门槛高，长期维护性弱于成熟后端生态 |
| 工具可用性视角 | `hugo/RT`、`AnimUML`、`EMI-UML`、`USMMC` 等 | 不同工具差异大 | 只有少数工具覆盖较宽 UML 子集 | 原文明确指出大多数历史工具已经失联 | 只有极少数工具能把 counterexample 回写到 UML | “能发表”不等于“能长期使用”，这是原文最强烈的负面结论之一 |

| 维度 | translation-based 路线 | direct operational semantics 路线 | 对 `project_1` 的含义 |
|---|---|---|---|
| 核心目标 | 尽快接入成熟后端验证器 | 尽量保留 UML 自身语义 | 前者利于复用工具，后者利于维持语义一致性 |
| 语义来源 | 后端形式语言的既有语义 | 针对 UML 定制的操作语义 | 若要保证“生成的就是 UML”，direct 更自然 |
| 语法覆盖 | 整体偏碎片化 | 整体更完整 | 若输入需求会落到 history/fork/join/deferred events，translation 更容易缺项 |
| 工具成熟度 | 借力成熟后端，但前端桥接常是原型 | 专用工具更少 | 若强调今天就能跑，仍要现实地接受“桥接到后端” |
| 反例回写 | 通常较弱 | 理论上更好，实践受工具限制 | 若后续要做“验证失败后自动修复”，反例可追溯性非常关键 |
| 长期维护 | 后端稳定，前端桥接易失联 | 更依赖少数维护者 | 需要优先跟踪仍活跃的 `hugo/RT`、`AnimUML`、`EMI-UML` |

## 构造方式与表示格式版图

| 对象/路线 | 建模入口 | 机器可处理承载 | 常见交换/输入方式 | 自动生成友好性 | 主要限制 |
|---|---|---|---|---|---|
| UML State Machine 本体 | 图形状态图 + 文本事件/守卫/动作 | `OMG UML` 抽象语法 + 半形式自然语言语义 | 常借助 `XMI` 导出模型结构 | 对工程建模友好，对直接验证不够友好 | 标准语义精度不足，很多关键点仍要靠 profile 补充 |
| Translation route | 以 UML 图为前端，再映射到后端形式语言 | `PROMELA`、`SMV`、`Uppaal`、`Petri nets`、`ASM/B` 等 | 多数经 `XMI` 或工具内部模型导入 | 对“已有后端复用”友好 | 真正执行和验证的是后端语言，不是 UML 自身 |
| Direct semantics route | 直接以 UML 抽象语法为对象 | SOS rules、Kripke structure、dedicated semantics engine | 原文未给统一交换标准，通常由专用工具内部承载 | 对语义保真更友好 | 缺少像 `PNML` 这类统一交换格式 |
| Tool-specific carriers | 建模工具导出的工程模型 | 工具自有 parser / metamodel | `XMI` 最常见，但常带供应商差异 | 对“工具内自动化”友好 | 互操作性受具体工具链约束 |

从构造方式上看，`UML State Machine` 的最大问题不是“画不出来”，而是“标准语义并不天然适合自动验证”。因此大量工作都要先把 UML 变成别的形式。

| 路线 | 是否直接保留 UML 语义对象 | 是否依赖统一标准载体 | 与验证器的衔接方式 | 对自动生成/自动修复的启发 |
|---|---|---|---|---|
| 纯 UML 标准语义 | 保留 | 有 `OMG UML`，但语义不够形式化 | 弱 | 只能作为面向人的前端，不适合作为裸验证输入 |
| `XMI` + translation | 部分保留，随后丢到后端 | 结构层面较强 | 强 | 适合作为“前端 UML -> 中间形式语言”的工程桥梁 |
| direct operational semantics | 强保留 | 统一交换载体弱 | 中 | 更适合作为 `project_1` 中“精确定义的 UML profile”基础 |

## 基础设施与生态版图

| 工具/路线 | 底层验证引擎 | 支持能力 | 反例是否能回到 UML | 长期可用性 | 原文中的位置 |
|---|---|---|---|---|---|
| `vUML` | `Spin` | 死锁与部分健壮性检查 | 是 | 差，历史工具已失联 | UML 早期自动验证线的重要入口 |
| `hugo` / `hugo/RT` | `Spin` / `Uppaal` | reachability、deadlock、LTL/CTL，`hugo/RT` 覆盖更完整 | `hugo/RT` 可回写 | `hugo/RT` 仍可获取，旧 `hugo` 较差 | translation 路线中最值得继续跟踪的一条 |
| `USMMC` | standalone | 直接操作语义下的验证 | 只能给翻译后层面的反例，不强回写 | 工具链已弱化 | direct semantics 路线代表 |
| `AnimUML` | `OBP2` | 动画、验证、sequence diagram 级 counterexample 表达 | 是，且表达更接近 UML | 好，开源且仍维护 | 现代 direct 路线代表 |
| `EMI-UML` | `OBP2` | 执行、deadlock-freeness 等 | 是 | 好，仍在开发 | direct 路线中较实用的一支 |
| `UML-B` | `ProB` | 偏 Event-B 方向的验证 | 回写能力有限 | 可获取 | 更接近“桥接到其他形式方法” |

| 比较维度 | translation front-end 工具 | dedicated operational 工具 | 结论 |
|---|---|---|---|
| 是否复用成熟后端 | 强 | 弱到中 | translation 工具更容易借现成引擎起步 |
| 是否贴近 UML 语义 | 中 | 高 | direct 工具更适合作为语义基线 |
| counterexample 回写 | 普遍偏弱，仅少数工具较好 | 理论更好，现代工具表现更优 | 若关心修复闭环，必须优先看回写能力 |
| 今天还能否获取 | 大量历史工具失联 | 现代少数工具仍活跃 | 长期维护比“当年是否发论文”更重要 |

原文最有价值的生态观察是：绝大多数学术工具都已经失联，只剩少数仍可获取和维护的项目，如 `hugo/RT`、`AnimUML`、`EMI-UML`。

## 适用场景与需求映射

| 对象/路线 | 适用场景 | 需求前提 | 为什么适合 | 不适合的情况 |
|---|---|---|---|---|
| UML State Machine 作为前端 | 软件设计、对象行为建模、与工程团队沟通 | 需求天然带对象、事件、层次状态、并发 region 视角 | 图形化强、工业沟通成本低 | 希望直接把标准自然语言语义送入验证器 |
| Translation-based verification | 希望快速复用 `Spin/SMV/Uppaal` 等成熟后端 | 能接受中间翻译、能固定一个语义 profile | 工具门槛较低，易接现有验证生态 | 无法接受语义差异、反例只停留在后端形式语言时 |
| Direct operational semantics | 希望保留更多 UML 语义细节并减少 profile 漂移 | 愿意使用专门工具或语义框架 | 更接近“验证的就是 UML 本身” | 需要立即接入广泛成熟生态时 |
| UML + active tool chain (`hugo/RT`、`AnimUML`、`EMI-UML`) | 想在 UML 路线中兼顾工程可用性与形式验证 | 必须选定具体工具链，而不是只说“支持 UML” | 能把抽象 UML 变成可执行验证资产 | 若团队无法接受工具特定约束或 profile 收缩时 |

| 路线 | 需求中至少要明确的信息 | 若缺失会发生什么 |
|---|---|---|
| UML 前端建模 | 状态、事件、守卫、动作、层次结构 | 图能画出来，但无法稳定转成形式语义 |
| translation 路线 | 还要明确事件队列、优先级、RTC、history/fork/join 语义 | 翻译结果可能因 profile 不同而偏离原意 |
| direct 路线 | 还要明确更细粒度的执行顺序与语义例外 | 工具难以给出唯一、可复现实义 |

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
