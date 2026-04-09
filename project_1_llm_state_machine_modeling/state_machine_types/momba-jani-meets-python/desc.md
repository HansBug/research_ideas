# Momba：JANI 遇见 Python / Momba: JANI Meets Python

## 基本信息

- 标题：Momba: JANI Meets Python
- 中文标题：Momba：JANI 遇见 Python
- 作者：Maximilian A. Köhl，Michaela Klauck，Holger Hermanns
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 389-398，2021
- DOI：`10.1007/978-3-030-72013-1_23`
- 链接：https://doi.org/10.1007/978-3-030-72013-1_23
- 形式主义：`JANI-model / Momba`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`JANI` 为中心的 Python 建模、仿真与分析框架
- 工具/实现获取方式：原文明确给出 GitHub 项目 `https://github.com/koehlma/momba` 与 Zenodo artifact 入口。
- 标准/格式获取方式：核心承载是 `JANI-model` interchange format、`Python` API 与 Jupyter/脚本化工作流；`Momba` 自身不定义新的中立标准，而是围绕 `JANI` 组织接口。

## 简报

这篇论文的关键点，是把原本偏“专家工具链”的 `JANI-model` 世界，接到人人会用的 `Python` 上。`Momba` 不只是一个模型构造器，它覆盖了 model construction、simulation、validation 和 analysis 的整个链路，把 `JANI`、`Storm`、`ePMC`、`Modest` 这类工具的接口统一成一个更亲和的 Python 工作流。

- 形式主义定位：围绕 `JANI` 的 Python 基础设施，而不是新的自动机本体。
- 构造方式简述：用 Python syntax-aware macros 生成 `JANI` 模型，再用内置 simulator 做验证，最后调用现成 model checkers。
- 基础设施与场景简述：依托 `JANI-model`、`Python`、GitHub artifact、内置仿真器与外部 model checkers，服务 formal models 的构造、验证与分析全流程。

```text
scenario description -> Python macros -> JANI model -> simulation / validation -> Storm / Modest / ePMC analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `JANI-model` interchange format。
2. Pythonic model-construction API。
3. Momba 内置 simulator。
4. 对 `Storm`、`Modest` 等分析器的统一调用接口。
5. `Racetrack` 示例中的模型族构造与验证流程。

### 核心抽象

结合论文对 `JANI` 的描述，可把 `Momba` 操作的核心模型保守写成：

$$
J = (\mathcal{A}, V, Sync, Init, Prop)
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}` 是 interacting automata 的集合。
2. `V` 是全局变量集合。
3. `Sync` 是同步/动作结构。
4. `Init` 是初始状态约束。
5. `Prop` 是附着在模型上的属性集合。
6. 这组符号是根据论文“network of interacting automata with variables and properties”做的保守归纳。

论文给了一个很具体的属性示例：

$$
P_{\max}(\Diamond(on\_goal \land fuel > 0))
$$

上式中的符号逐项解释如下：

1. `P_{\max}` 表示最大到达概率。
2. `\Diamond` 表示“最终到达”。
3. `on\_goal` 表示车到达终点格。
4. `fuel > 0` 表示油箱仍有剩余。
5. 该公式是论文在 `Racetrack` 例子中直接展示的属性形式。

### 一个最小例子与通俗解释

论文用 `Racetrack` 讲得很清楚：

1. 赛道由 start、goal、wall、blank 格组成。
2. 汽车状态包含位置、速度和油量。
3. 不同油耗模型、路面噪声和赛道实例会生成一整个模型家族。
4. Python 宏可以把这些配置自动展开成大批 `JANI` 模型。

通俗地说，`Momba` 像是把 formal modeling 变成“可以写 Python 脚本、可以交互调试、可以直接调模型检查器”的数据科学式工作流。

### 运行 / 接受 / 转移语义

论文强调 `Momba` 支持整个流程：

$$
\text{construction} \to \text{validation} \to \text{analysis}
$$

其中：

1. `construction` 通过 Python 宏和 API 完成。
2. `validation` 通过内置 simulator 与可视化/交互探索完成。
3. `analysis` 通过外部 model checker 完成。

对运行时语义，`Momba` 的 simulator 会给出当前变量绑定、automata 位置以及可采取动作/延时，因此可保守写成：

$$
s \xrightarrow{a \text{ or } d} s'
$$

上式中的符号逐项解释如下：

1. `s` 和 `s'` 是当前与后继仿真状态。
2. `a` 是可选离散动作。
3. `d` 是可选时间延迟。
4. 这条写法对应论文对 simulator 接口能力的描述，不是某个新形式主义的本体定义。

### 语义边界

论文也强调：

1. `Momba` 不想重复发明新的模型格式，而是围绕 `JANI` 工作。
2. 它的重点是集成式体验，不是替代底层 model checkers。
3. 能分析多远，最终仍取决于被调用的后端工具能力。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `JANI` 模型骨架 | `$J = (\mathcal{A}, V, Sync, Init, Prop)$` | `Momba` 围绕 interacting automata 网络工作。 |
| 示例属性 | `$P_{\max}(\Diamond(on\_goal \land fuel > 0))$` | 论文直接展示的 `Racetrack` 概率目标。 |
| 工作流 | `$\text{construction} \to \text{validation} \to \text{analysis}$` | 论文反复强调的 integrated experience。 |
| 仿真步 | `$s \xrightarrow{a \text{ or } d} s'$` | simulator 同时暴露离散动作和时间步。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 automata networks 和变量状态工作。 |
| 事件 / 触发 | 强支持 | `JANI` 网络中的动作与同步是一等对象。 |
| 守卫 / 数据 | 很强 | Python API 和 `JANI` 表达式都支持复杂条件。 |
| 层次 | 弱支持 | 主体不是层次状态机工具。 |
| 并发 / 同步 | 很强 | `JANI` 的核心就是 interacting automata。 |
| 时间约束 | 强支持 | `JANI` 和被调用后端可覆盖 timed models。 |
| 连续动态 / 随机性 | 强支持 | 论文明确说 `JANI` 可覆盖概率、实时和连续动力学。 |
| 可执行 / 可验证性 | 很强 | 内置 simulator + 外部 model checkers 双链路。 |

### 形式化问题与性质

1. `Momba` 的创新点不在于新模型，而在于把 formal models 的全流程做成 Python-friendly infrastructure。
2. `JANI` 作为 interchange format 是它成立的前提。
3. 这类工作对文库的价值，在于补“可复用建模/验证接口层”，而不是再补一个求解器。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用 Python 读取 scenario description。
2. 用 syntax-aware macros 与 API 构造 `JANI` automata network。
3. 用 simulator 做交互验证或测试。
4. 调 `Storm`、`Modest` 等后端求分析结果。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Python` 脚本与 notebook。
2. `JANI-model` 文件。
3. 内置 simulator 的状态对象与 trace。
4. 外部 model checker 可接受的统一接口调用。

### 交换与互操作

这篇论文的互操作重点在于：

1. `JANI` 作为模型交换中心。
2. `Momba` 作为 Python 宏层和工具调度层。
3. `Storm`、`ePMC`、`Modest` 等后端通过统一接口接入。

## 配套基础设施

- 建模/编辑工具：Python API、脚本与 notebook。
- 解析/交换/元模型支持：`JANI-model`。
- 仿真/执行支持：`Momba` 内置 simulator。
- 验证/分析支持：可调用 `Storm`、`ePMC`、`The Modest Toolset` 等。
- 代码生成/转换支持：主线是模型构造、验证与分析，不是部署代码生成。
- 标准化或社区生态：GitHub、Zenodo、`JANI`、Python 数据科学生态。

## 适用场景与需求前提

### 适用场景

适合需要批量生成 formal models、做交互验证、并希望把这些模型直接挂到现成 quantitative model checkers 上的研究和原型场景。

### 需求前提

1. 模型能够自然落到 `JANI` automata network。
2. 团队接受 Python 作为前端建模与实验环境。
3. 后续确实需要复用多个现成后端，而不是只绑定单一求解器。

### 不适用或高成本场景

如果团队不希望引入脚本化工作流，或者模型根本不适合 `JANI`，这套基础设施价值会下降。

## 与相邻形式主义的关系

相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，`Modest Toolset` 更像平台本体，而 `Momba` 更像 Python 外层工作流与 `JANI` 接口层；相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM` 是单点分析平台，而 `Momba` 更关注模型构造和跨工具调用；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 是专用后端，而这里强调统一前端实验环境。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果未来 `project_1` 想做大规模自动生成、批量变体、快速验证与 notebook 式实验记录，那么“Python + interchange format + backend adapters”是一条很现实的工具架构。

### 作为目标形式主义还是中间表示

更像工具基础设施与实验入口层，而不是目标形式主义。

### 对需求到模型生成的启发

1. 面向 LLM 的自动建模任务，脚本化和可批量生成能力非常关键。
2. `JANI` 这类中立格式适合当多后端之间的“交换中间层”。
3. 内置 simulator 说明“先可视化验证，再正式分析”是很有价值的工作流。

### 现实限制

`Momba` 的能力上限最终还是被 `JANI` 语义边界和外部求解器能力共同限定。

## 重要的相关工作

1. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：平台型 quantitative toolset。
2. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：概率实时后端平台。
3. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：经典 timed automata 后端教程。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：主贡献是围绕 `JANI` 的 Python 工作流与工具接口层，而不是新的状态机本体。
