# UML-B 状态机动画 / Animation of UML-B State-machines

## 基本信息

- 标题：Animation of UML-B State-machines
- 中文标题：UML-B 状态机动画
- 作者：Vitaly Savicks，Colin Snook，Michael Butler
- 发表：*Rodin User and Developer Workshop*，2010
- DOI：原文未提供
- 链接：https://eprints.soton.ac.uk/268261/1/TBFMsmAnim.pdf
- 形式主义：`UML-B / Event-B / ProB animation plug-in`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：visual animation plug-in for `UML-B` state-machine diagrams backed by `ProB`
- 工具/实现获取方式：原文明确说明该工具是 `Rodin` 平台上的 prototype plug-in，需要同时安装 `UML-B` front-end 与 `ProB`；论文给出 update-site 安装入口。
- 标准/格式获取方式：主承载是 `UML-B` state-machine diagrams、由 `UML-B` 翻译得到的 `Event-B` machine，以及 animation diagrams 的独立 metamodel；它不是通用交换标准。

## 简报

这篇论文补的是 `UML-B` 工具线里一个很实用但此前未正式入账的节点：把形式模型“活起来”的 visual animation。它的重点不在再做一层证明，而是在 `Rodin + UML-B + ProB` 之间插入一个动画插件，让 state-machine diagram 能随着 `ProB` 的状态更新而动态高亮、显示可触发迁移、展示 class-lifted 实例位置，并且支持同时观察 nested/refined state-machines。对形式化建模来说，这种能力不只是 demo，而是 validation 与 refinement 理解的重要入口。

- 形式主义定位：`UML-B` 状态机图的可视动画基础设施，而不是新的状态机母型。
- 构造方式简述：`UML-B diagrams -> generated Event-B machine -> ProB animation state -> animation diagrams`。
- 基础设施与场景简述：依托 `Rodin`、`UML-B` graphical front-end、`ProB` animator、EMF/GMF animation metamodel，服务 refinement validation、nested state-machine 观察和 class-lifted instance debugging。

```text
UML-B state-machine diagram -> Event-B translation -> ProB state updates -> animation listener -> highlighted states/transitions
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML-B` state-machine diagrams。
2. 由 `UML-B` 翻译得到的 `Event-B` machines。
3. animation diagrams 的独立 metamodel。
4. `ProB` animator 输出的变量值。
5. nested/refined state-machines 与 class-lifted instances。

### 核心抽象

结合论文对工具链的描述，可把动画工作流保守整理为：

$$
\mathcal A = (SM, EB, AD, \tau, \pi)
$$

上式中的符号逐项解释如下：

1. `SM` 是被选中的 `UML-B` state-machine diagrams。
2. `EB` 是 `UML-B` 翻译生成的 `Event-B` machine。
3. `AD` 是 animation diagrams。
4. `\tau` 表示 `UML-B -> Event-B` translation options。
5. `\pi` 表示 `ProB` state values 到 animation objects 的解释映射。
6. 这组元组概括了论文的工具结构，而非原文统一显式定义。

论文特别强调同一状态机的两种翻译结果。若采用 state-function translation，则可写成：

$$
sm = \{(ci_1 \mapsto s_1), (ci_2 \mapsto s_2)\}
$$

上式中的符号逐项解释如下：

1. `sm` 是整个状态机的单变量表示。
2. `ci_1`、`ci_2` 是类实例。
3. `s_1`、`s_2` 是它们当前所在状态。
4. 这对应论文给出的 functional translation 例子。

若采用 state-sets translation，则写成：

$$
s_1 = \{ci_1\},\qquad s_2 = \{ci_2\}
$$

上式中的符号逐项解释如下：

1. 每个状态单独对应一个 `Event-B` 变量。
2. 变量值记录当前处于该状态的实例集合。
3. 论文强调不同翻译方式会显著影响动画插件如何解释 `ProB` 返回值。

### 一个最小例子与通俗解释

论文里的典型交互流程很直观：

1. 用户在 `UML-B project explorer` 里选中若干 state-machines。
2. 工具生成对应 animation diagrams，并自动启动 `ProB Animator`。
3. 当前 active states 被高亮，可触发 transitions 被加粗显示。
4. 用户直接点击 transition 触发事件；若事件带参数，工具弹出参数候选供选择。

通俗地说，这个插件做的事情就是把原本只在 `ProB` 变量面板里变化的 `Event-B` 状态，重新投影回 `UML-B` 的图上，让建模者能直观看到 refinement、嵌套状态和多个对象实例如何演化。

### 运行 / 接受 / 转移语义

论文的方法链可保守写成：

$$
SM \xrightarrow{\tau} EB \xrightarrow{\mathrm{ProB}} state \xrightarrow{\pi} AD
$$

上式中的符号逐项解释如下：

1. `SM` 是输入图。
2. `\tau` 是 `UML-B` 到 `Event-B` 的翻译。
3. `state` 是 `ProB` 返回的当前 machine state。
4. `\pi` 把 `Event-B` 变量值解释回 animation diagram 中的高亮状态、可用迁移和实例 token。

### 语义边界

1. 论文主线是 visual animation，不是额外的证明引擎。
2. 它严重依赖 `UML-B -> Event-B` 翻译方式，因此 translation details 不能被忽略。
3. 某些非状态机图元或 auxiliary variables 仍需在 `ProB` 原生界面里查看。
4. 本文是 prototype/tool paper，重点在 infrastructure feasibility 而不是完整语言语义扩展。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 工具骨架 | `$\mathcal A = (SM,EB,AD,\tau,\pi)$` | 动画插件把图、翻译、动画图和解释映射绑到一起。 |
| state-function translation | `$sm = \{(ci_1 \mapsto s_1), (ci_2 \mapsto s_2)\}$` | 整个状态机可被单变量函数式表示。 |
| state-sets translation | `$s_1 = \{ci_1\},\ s_2 = \{ci_2\}$` | 也可按“每个状态一个集合变量”的方式表示。 |
| 动画链路 | `$SM \xrightarrow{\tau} EB \xrightarrow{\mathrm{ProB}} state \xrightarrow{\pi} AD$` | 论文真正实现的执行链。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心就是状态机图的可视状态切换。 |
| 事件 / 触发 | 很强 | 用户可直接点击 enabled transitions 触发事件。 |
| 守卫 / 数据 | 中等支持 | 参数选择与 `Event-B` 变量值解释都已考虑。 |
| 层次 | 很强 | nested/refined state-machines 可同时观察。 |
| 并发 / 同步 | 中等支持 | 多个 state-machines 可并行开图联合观察。 |
| 时间约束 | 不支持 | 不是 timed animation 论文。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 很强 | 可视动画直接服务 model validation。 |

### 形式化问题与性质

1. 这篇论文的重点不是“状态机能否动画”，而是怎样在 `Rodin/UML-B/ProB` 之间建立稳定的动画基础设施。
2. 独立 animation metamodel 的设计，说明作者有意把动画层从原始 `UML-B` metamodel 解耦。
3. 支持 refinement、nested states 和 class-lifting 让它不只是演示玩具，而是能覆盖正式建模中的难点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `UML-B` state-machine diagrams。
2. `UML-B` 到 `Event-B` 的翻译选项。
3. `ProB` animator 返回的 machine states。
4. 独立 animation diagram models。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML-B` 图模型。
2. 生成的 `Event-B` variables。
3. animation metamodel objects。
4. `ProB` API 返回的变量名/变量值对。

### 交换与互操作

互操作重点在于：

1. `UML-B` 只在启动阶段用于创建 animation diagram models。
2. 动画运行时主要依赖 `ProB` API 与 animation listener extension point。
3. `Rodin` 提供 plug-in 宿主，`EMF/GMF` 提供图模型基础设施。

## 配套基础设施

- 建模/编辑工具：`Rodin` 平台与 `UML-B` graphical front-end。
- 解析/交换/元模型支持：独立 animation metamodel、EMF、GMF、translation-option handling。
- 仿真/执行支持：`ProB` animator。
- 验证/分析支持：动画主要服务 validation；同时能辅助观察 nested/refined dependencies。
- 代码生成/转换支持：主线是 `UML-B -> Event-B` 翻译与 animation diagram 生成，不主打代码生成。
- 标准化或社区生态：依托 `Rodin`、`UML-B`、`Event-B`、`ProB` 社区。

## 适用场景与需求前提

### 适用场景

适合 `UML-B` 建模中的 refinement validation、教育演示、实例级状态观察，以及需要把 `Event-B` 动画结果重新映回图形状态机图的场景。

### 需求前提

1. 模型需已经落成 `UML-B` state-machines。
2. 可接受 `UML-B -> Event-B -> ProB` 的工具链。
3. 关注点是“模型行为是否符合预期”，而不是大规模自动证明优化。
4. 若有 class-lifted instances 或 nested/refined structures，动画价值会更大。

### 不适用或高成本场景

若需求核心是 timed animation、复杂连续行为或纯文本工作流，这个 `Rodin` 插件并不会是自然入口；同时它也不替代更深的证明工具。

## 与相邻形式主义的关系

相对 [language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md](../language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md)，后者补的是 `UML-B` 的 refinement notation 与 translator，而本文补的是 visual animation plug-in；相对 [graphical-animation-of-behavior-models/desc.md](../graphical-animation-of-behavior-models/desc.md)，两者都研究“形式模型如何可视化执行”，但本文直接绑定 `UML-B / Event-B / ProB` 生态；相对 [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)，本文不是一般 `UML` survey，而是 `UML-B` 上非常具体、可运行的 tool node。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们，状态机建模闭环里“可视化验证”本身就是正式基础设施，而不是可有可无的 UI。
2. 如果后续希望让 LLM 生成的图模型可被领域专家快速审核，这种 animation bridge 很值得借鉴。
3. 对 `project_4` 的 repair 也有启发：很多 refinement 错误或 elaboration 错误可能先在动画阶段就能被人看出来。

### 作为目标形式主义还是中间表示

更像 `UML-B` 生态上的执行/验证基础设施，而不是新的本体形式主义。

### 对需求到模型生成的启发

1. 图形模型不应只停留在静态结构，还应尽量保留可映射回运行态的元信息。
2. refinement、nested states 和实例集合等信息，如果在生成阶段就被结构化保存，后续更容易做可视调试。
3. 动画层最好独立建模，而不是把演示语义硬塞进主元模型。

### 现实限制

本文是 prototype 级插件条目，工程成熟度和通用性不如大平台；它的强项也主要局限在 `UML-B / Rodin / ProB` 生态内。

## 重要的相关工作

1. [language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md](../language-and-tool-support-for-class-and-state-machine-refinement-in-uml-b/desc.md)：`UML-B` refinement 与 translator 基础设施。
2. [graphical-animation-of-behavior-models/desc.md](../graphical-animation-of-behavior-models/desc.md)：形式模型可视动画的早期基础设施路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML-family state-machine verification/tooling 全景。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML-B / Event-B / ProB animation plug-in`
- 归类理由：论文主体是 `UML-B` 生态内的状态机动画基础设施，而不是新的算法方法或通用后端，因此按 `🔣/🏗️` 归类最合适。
