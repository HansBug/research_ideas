# SCADE 设计系统的模型检查 / Model Checking of SCADE Designed Systems

## 基本信息

- 标题：Model Checking of SCADE Designed Systems
- 中文标题：SCADE 设计系统的模型检查
- 作者：S. Heim，Xavier Dumas，E. Bonnafous，Philippe Dhaussy，C. Teodorov，Lise Leroux
- 发表：*8th European Congress on Embedded Real Time Software and Systems (ERTS 2016)*，2016
- DOI：原文未给 DOI，当前公开入口以 HAL 版本为主
- 链接：https://hal.science/hal-01289454
- 形式主义：`SCADE / Lustre / FIACRE / OBP / CDL / GALS`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：将同步 `SCADE/Lustre` 系统通过 `FIACRE + OBP + context-aware verification` 接入异步模型检查的桥接方法
- 工具/实现获取方式：原文明确依托 `SCADE`、其合格代码生成器 `KCG51`、`FIACRE`、`OBP` 和 `CDL`；正文未给独立开源仓库入口。
- 标准/格式获取方式：核心承载不是中立交换标准，而是 `SCADE/Lustre` 模型、生成的 `C` 代码、`FIACRE` 包装模型与 `CDL` 上下文/观察器描述。

## 简报

这篇论文补的是一个很典型但又常被忽略的问题：工业里很多控制系统先在 `SCADE/Lustre` 这类同步 DSL 里建模，但真正想做上下文敏感模型检查时，现成后端却往往是异步探索引擎。作者给出的办法是用 `KCG51` 先把 `Lustre` 编译成 `C`，再包上一层 `FIACRE` wrapper，把同步步进语义嵌入到 `OBP` 的异步上下文验证框架里。

- 形式主义定位：围绕 `SCADE/Lustre -> FIACRE/OBP` 的验证桥接方法，而不是新的 DSL 本体定义。
- 构造方式简述：`SCADE/Lustre model -> qualified C code -> FIACRE wrappers/data structure -> asynchronous CDL contexts -> OBP exploration`。
- 基础设施与场景简述：依托 `GALS` 思想、上下文建模和 splitting method，服务同步工业控制软件在异步环境下的安全性质验证。

```text
SCADE / Lustre -> C code -> FIACRE wrapper -> CDL context / observer -> OBP exploration -> property checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `SCADE` 设计系统，其核心行为语言是 `Lustre`。
2. 同步 step 语义与 `KCG51` 生成的 `C` 实现。
3. `FIACRE` 异步模型与 I/O data structure。
4. `CDL` 描述的 context、event、predicate 与 property automaton。
5. `OBP` 的 context-aware verification 与 splitting method。

### 核心抽象

从方法角度看，同步 `Lustre` 组件可保守整理为：

$$
S = (I, O, M, step)
$$

上式中的符号逐项解释如下：

1. `$I$` 是输入集合。
2. `$O$` 是输出集合。
3. `$M$` 是内部记忆状态。
4. `$step : Val(I) \times M \to Val(O) \times M$` 表示一次同步反应步。

论文的桥接核心是把这个同步步包进异步验证环境。可保守写成：

$$
Sys_{OBP} = Wrap(C_{Lustre}, D_{io}, Ctx_{CDL})
$$

上式中的符号逐项解释如下：

1. `$C_{Lustre}$` 是由 `SCADE/Lustre` 经过 `KCG51` 生成的 `C` 代码。
2. `$D_{io}$` 是 `FIACRE` 中维护的输入输出共享数据结构。
3. `$Ctx_{CDL}$` 是异步环境上下文与观察器。
4. `Wrap` 表示论文所做的 wrapper、数据复制和异步调度封装。

数据交换语义可压成：

$$
d' = copy_{out}(call_C(copy_{in}(ctx,d)))
$$

上式中的符号逐项解释如下：

1. `$ctx$` 是环境刺激产生的输入上下文。
2. `$d$` 是当前 `FIACRE` 数据结构。
3. `copy_{in}` 把环境提供的值写入 `C` 侧共享结构。
4. `call_C` 调用同步计算步骤。
5. `copy_{out}` 把新的输出状态回写到 `FIACRE`，供 `OBP` 继续观察与验证。

论文还给出 `CDL` 风格的性质描述。以 cruise control 为例，其一个谓词和事件可写成：

$$
p_{unset} \equiv CruiseSpeed < 40 \lor CruiseSpeed > 180, \qquad e_{unset} \equiv p_{unset}\ \mathrm{becomes\ true}
$$

上式中的符号逐项解释如下：

1. `$p_{unset}$` 判断目标巡航速度当前是否处于非法范围，因此可视为“未设置”。
2. `$e_{unset}$` 不是静态布尔值，而是谓词变为真的上升沿事件。
3. 这种“predicate -> event” 映射是 `CDL/OBP` 上下文建模的关键。
4. 它允许把同步系统输出转换为异步观察器可消费的可观测事件。

### 一个最小例子与通俗解释

论文里最清楚的例子是 cruise-control：

1. 司机先按 `On` 让系统进入待机。
2. 再按 `Set` 设置目标速度。
3. 之后松开油门，系统开始 regulate。
4. 但如果目标速度尚未设置，系统绝不能自己 engage。

在 `SCADE` 里，这些逻辑原本按同步反应步运行；在 `OBP` 里，作者用 `CDL` 观察器把“非法情况下 engage”写成 reject 转移。通俗地说，这套方法像是给同步控制软件套了一个“异步环境试验场”，从而能在更现实的上下文里做模型检查。

### 运行 / 接受 / 转移语义

论文的性质验证不再是“对整个环境全展开”，而是只在给定 context 上探索。可保守整理为：

$$
Reach(Reject, Sys_{OBP} \parallel Obs_{CDL} \parallel Ctx_{CDL}) = \emptyset
$$

上式中的符号逐项解释如下：

1. `$Obs_{CDL}$` 是以 `CDL` 写成的观察器自动机。
2. `$Ctx_{CDL}$` 是环境行为描述。
3. `$\parallel$` 表示系统、观察器与上下文的组合探索。
4. 若 `Reject` 不可达，则性质成立。

论文还强调 splitting method：当全局 context 太大时，把它拆成多个 sub-context 分别验证，再汇总覆盖整个探索空间。

### 语义边界

1. 论文主要验证的是行为安全性质，而不是数值精度或完整代码级语义等价。
2. 方法成立依赖同步 `Lustre` 步可被原子地包入异步 wrapper 中。
3. context 建模带有明显工程判断成分，不是全自动生成。
4. 这条路线更像 verification bridge，而不是 `SCADE` 本体标准扩展。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 同步组件骨架 | `$S=(I,O,M,step)$` | `SCADE/Lustre` 行为本质上是 step-driven。 |
| 桥接系统 | `$Sys_{OBP}=Wrap(C_{Lustre},D_{io},Ctx_{CDL})$` | 同步模型通过 wrapper 被纳入异步验证环境。 |
| 数据交换 | `$d'=copy_{out}(call_C(copy_{in}(ctx,d)))$` | `FIACRE` 与生成的 `C` 代码之间的接口语义。 |
| 谓词事件化 | `$e_{unset}\equiv p_{unset}\ \mathrm{becomes\ true}$` | `CDL` 把状态谓词转成可观测事件。 |
| 性质判定 | `$Reach(Reject,\cdots)=\emptyset$` | 观察器 reject 是否可达即为验证结果。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `SCADE` 控制状态与 `FIACRE` wrapper 状态都可观察。 |
| 事件 / 触发 | 很强 | `CDL` 用事件、谓词上升沿和环境刺激驱动验证。 |
| 守卫 / 数据 | 强 | 输入输出数据结构、谓词与系统状态都参与上下文约束。 |
| 层次 | 中等支持 | 系统可分为组件与环境 actor，但主线不是层次状态机语义。 |
| 并发 / 同步 | 很强 | 关键就在同步 `Lustre` 与异步 `FIACRE/OBP` 的组合。 |
| 时间约束 | 中等支持 | 面向嵌入式实时系统，但本文重点是同步/异步桥接而非 dense-time 公式。 |
| 连续动态 / 随机性 | 不支持 | 主要是离散控制逻辑。 |
| 可执行 / 可验证性 | 很强 | 直接给出从工业 DSL 到模型检查后端的工程路径。 |

### 形式化问题与性质

1. 这篇论文的核心不在重新定义 `SCADE`，而在于让 `SCADE` 模型进入更有表达力的上下文验证环境。
2. `GALS` 在这里不是硬件流行语，而是“同步系统如何被异步环境安全包裹”的方法学。
3. context-aware verification 明确告诉我们：验证不一定非得探索“全环境”，可以只探索与性质相关的环境切片。

## 构造方式与承载格式

### 建模入口

论文中的主要入口有：

1. `SCADE` 组件模型。
2. `Lustre` 代码。
3. `KCG51` 生成的 `C` 代码。
4. `FIACRE` wrapper 与共享数据结构。
5. `CDL` 写成的 context 与 property observer。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `SCADE/Lustre` 模型。
2. `C` 代码及其输入输出结构体。
3. `FIACRE` 系统模型。
4. `CDL` 的 predicate、event、property、activity。

### 交换与互操作

1. 这条路线的关键不是标准交换文件，而是 DSL 到验证后端的桥接流水线。
2. `FIACRE` 承担了同步 `SCADE` 与异步 `OBP` 之间的中间载体角色。
3. `CDL` 则承担环境和观察器的统一描述角色。

## 配套基础设施

- 建模/编辑工具：`SCADE` 用于同步工业系统设计。
- 解析/交换/元模型支持：`KCG51` 负责 `Lustre -> C`，`FIACRE` 负责异步承载，`CDL` 负责上下文与观察器。
- 仿真/执行支持：通过 wrapper 调用生成的 `C` 代码，把一步同步计算嵌入 `FIACRE/OBP` 探索。
- 验证/分析支持：`OBP`、context-aware verification、splitting method、predicate/event observers。
- 代码生成/转换支持：`SCADE -> C -> FIACRE` 是全文主线。
- 标准化或社区生态：原文依托现有 `SCADE/Lustre` 工业生态与 `OBP/FIACRE` 研究工具生态。

## 适用场景与需求前提

### 适用场景

适合已经使用 `SCADE/Lustre` 建模的实时嵌入式控制系统，尤其是需要在上下文约束下验证安全性质的工业场景。

### 需求前提

1. 系统主体应位于 `SCADE/Lustre` 可表达的同步反应模型内。
2. 性质需能写成 `CDL` predicate / event / observer 风格。
3. 环境需要能被人工整理成一组可验证的 actors、stimuli 与 scenarios。
4. 团队接受“同步核心 + 异步上下文”这一桥接式验证思路。

### 不适用或高成本场景

1. 若系统大量依赖连续动力学或复杂时序调度，单纯这条 `SCADE -> FIACRE` 路线可能还不够。
2. 若环境完全开放且难以裁剪，上下文建模成本会很高。
3. 若目标是证明与生成代码完全位级等价，本文给出的包装验证仍偏行为级。

## 与相邻形式主义的关系

相对 [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md) 与 [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)，这些条目更多服务 `UML` 解释执行与验证统一，而本文服务的是 `SCADE/Lustre` 同步 DSL；相对 [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)，两者都在做“设计模型到验证/执行后端桥接”，但本文更强调 `GALS` 与 context-aware verification；相对 [execution-of-partial-state-machine-models/desc.md](../execution-of-partial-state-machine-models/desc.md)，后者关注不完整状态机执行，本文关注同步工业 DSL 的上下文模型检查。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对博士主线的意义很直接：它展示了“领域 DSL 生成模型之后，如何接到真正可用的验证后端”。这与你的研究目标高度相关，因为：

1. LLM 生成的状态机若最终需要严肃验证，往往也要经过类似的桥接层。
2. context-aware verification 说明验证不该只面向裸模型，还要面向环境与场景。
3. 这与 `project_2` 和 `project_3` 中的场景生成、验证 profile 非常契合。

### 可借鉴点

1. 可以借鉴其“模型核心 + 环境上下文 + 观察器性质”三层分离结构。
2. `predicate -> event -> observer` 的 `CDL` 写法对性质自动生成很有启发。
3. `splitting` 思想也适合做大模型验证时的 profile 分解。

### 局限与注意事项

1. 该方法默认已有结构化 DSL 模型，不解决从自然语言直接到 `SCADE` 的建模问题。
2. context 建模仍偏手工，离你希望的自动化闭环还有距离。
3. 对同步语义的包装是工程有效方案，但是否最适合所有嵌入式 DSL，需要进一步比较。

## 重要的相关工作

1. [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md)：统一设计期与部署期解释执行，和本文一样都在做 DSL 到后端的桥接。
2. [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)：展示状态机 DSL 与验证/执行双后端联动的另一条路线。
3. [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)：说明模型到验证/执行的模块化部署思想可以跨 DSL 复用。

## 文献分类总结

- 这是一篇 `🔣 DSL / 专用建模语言` 条目，因为主对象始终是 `SCADE/Lustre` 这类同步工业 DSL。
- 这是一篇 `🛠️ 方法路线` 条目，而不是 `🏗️ 标准/基础设施` 条目，因为核心贡献是桥接与验证流程方法，而不是新的独立工具标准。
- 它描述的核心对象是 `🎛️ 控制 / 反应式逻辑`，落点是实时嵌入式控制系统的行为安全验证。
- 它应挂在 `SCADE/Lustre -> FIACRE/OBP GALS verification bridge` 的静态挂接口径下，作为同步 DSL 接入异步验证后端的代表性方法证据。
