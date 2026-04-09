# 面向验证与嵌入式执行的 UML 模型模块化部署 / Modular Deployment of UML Models for V&V Activities and Embedded Execution

## 基本信息

- 标题：Modular Deployment of UML Models for V&V Activities and Embedded Execution
- 中文标题：面向验证与嵌入式执行的 UML 模型模块化部署
- 作者：Valentin Besnard，Frédéric Jouault，Matthias Brun，Ciprian Teodorov，Philippe Dhaussy，Jérôme Delatour
- 发表：*Proceedings of the 23rd ACM/IEEE International Conference on Model Driven Engineering Languages and Systems: Companion Proceedings*，pp. 1-10，2020
- DOI：`10.1145/3417990.3419227`
- 链接：https://doi.org/10.1145/3417990.3419227
- 形式主义：`UML State Machine / modular deployment architecture`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：modular UML deployment architecture / V&V-execution bridge
- 工具/实现获取方式：原文说明该方法依托作者已有 UML model interpreter 与 `OBP2` model-checker，可对同一 system model 做 trace-based simulation、state-space exploration 与 `LTL` model-checking，然后再部署到 `STM32`；未给独立公开仓库。
- 标准/格式获取方式：承载方式是按 `System / Environment / DAL / Main / DIL / Target` 切分的 UML/XMI 文件、ports/interfaces、`Element Imports`、stable `XMI IDs`、`EcoreUtil.resolve()` 与后续 `C struct initializer` 部署链；无中立行业交换标准。

## 简报

这篇论文的关键贡献，是把“同一套 UML 系统模型如何在 abstract environment、concrete environment、simulation、model checking 和真实板级执行之间切换”做成了模块化架构。作者不是去做新的 `PIM -> PSM` 语义变换，而是坚持保持同一个 `System` 模型不变，只替换 `Environment`、`DAL/DIL` 和 target-side bindings，从而尽量保留在验证阶段得到的性质与运行时部署之间的一致性。

- 形式主义定位：`UML State Machine` 的部署架构与互操作骨架，而不是新的状态机语言。
- 构造方式简述：把模型拆成 `System`、`Environment`、`DAL`、`Main` 四个核心包，并在实际部署时再补 `DIL` 和 `Target`。
- 基础设施与场景简述：依托 stable `XMI IDs`、ports/interfaces、`OBP2` 与嵌入式解释器，使 abstract environment、simulated environment 和 concrete environment 可以围绕同一 system model 切换。

```text
stable system model + replaceable environment modules -> simulation / LTL checking / embedded execution -> same UML-level behavioral reference
```

## 形式主义定义与核心对象

### 定义对象

论文把模块化部署链组织成以下对象：

1. `System`：待验证和待部署的系统组件。
2. `Environment`：可替换的抽象或具体环境模型。
3. `DAL`：device abstraction layer，固定 system 与 environment 的接口契约。
4. `Main`：把 system 与 environment 通过 ports/interfaces 组装起来的 composite structure。
5. `DIL` 与 `Target`：面向真实板卡和外设的低层映射。

### 核心抽象

结合论文的 package 切分，可保守整理其部署骨架为：

$$
\mathcal{D} = (Sys, Env, DAL, Main, DIL, Target)
$$

上式中的符号逐项解释如下：

1. `Sys` 是 system package。
2. `Env` 是 environment package，可取 abstract 或 concrete 版本。
3. `DAL` 是设备抽象接口层。
4. `Main` 是 system 与 environment 的组装入口。
5. `DIL` 是 device implementation layer。
6. `Target` 是与具体硬件资源相关的板级配置。

论文强调关键不是模型变换，而是稳定链接。其“stable XMI IDs”可以形式化写成：

$$
id(e) = fqname(e)
$$

上式中的符号逐项解释如下：

1. `e` 是某个 UML 元素。
2. `fqname(e)` 是该元素的 fully qualified name。
3. 论文用它替代普通易变的 `XMI ID`，使跨文件引用在替换环境模型后仍尽量稳定。

相应的跨文件解析可保守写成：

$$
\mathrm{Resolve} : Import \times \mathcal{R}_{xmi} \to Element
$$

上式中的符号逐项解释如下：

1. `Import` 表示某个 `Element Import` 引用。
2. `\mathcal{R}_{xmi}` 是当前 resource set 中的所有 UML/XMI 文件。
3. `Element` 是被 `EcoreUtil.resolve()` 解析出来的目标元素。

### 一个最小例子与通俗解释

论文中最直观的例子是 Button-Led system：

1. `System` 里保留 controller 的核心状态机逻辑。
2. `Environment` 可以替换成 `interactiveEnv`、`simulatedEnv`、`gpioEnv` 或 `pwmEnv`。
3. `DAL` 负责定义按钮、LED 之类的抽象接口。
4. 如果只是做 simulation 或 model checking，就接 abstract environment；如果要落到 `STM32`，就再接 `DIL` 和 `Target`。

通俗地说，它像“给同一个 UML 系统骨架换不同的壳和接口适配层”，而不是每做一种活动就拷贝一份系统模型再改一遍。

### 运行 / 接受 / 转移语义

论文的核心运行不是单个状态机，而是组合与替换。可把一次部署实例写成：

$$
\mathcal{E}_i = \mathrm{Deploy}(Sys, Env_i, DAL, Main)
$$

上式中的符号逐项解释如下：

1. `Env_i` 是某个具体环境版本，例如交互式、仿真式或板级 concrete environment。
2. `\mathcal{E}_i` 是该环境下形成的完整可执行 UML 模型。
3. 关键点是 `Sys` 不随 `Env_i` 的切换而重写。

如果进一步落到硬件部署，则可保守写成：

$$
\mathcal{E}_{hw} = \mathrm{Deploy}(Sys, Env_{conc}, DAL, Main, DIL, Target)
$$

而从验证角度，论文关注的是：

$$
\mathcal{E}_{vv} \models \varphi_{LTL}
$$

上式中的符号逐项解释如下：

1. `\mathcal{E}_{vv}` 是带 abstract environment 的验证/仿真实例。
2. `\varphi_{LTL}` 是在 `OBP2` 中检查的 `LTL` 性质。
3. 作者希望通过不改变 `Sys`、只替换环境模块的方式，让已验证性质更容易迁移到 runtime deployment 语境。

### 语义边界

论文也明确承认其边界：

1. 它不做证明完备的 `PIM -> PSM` 变换正确性论证。
2. concrete environment 必然比 abstract environment 更具体，性质迁移仍依赖“抽象环境覆盖真实情形”的前提。
3. 重点是 UML module decomposition 与 deployment discipline，而不是新的 verification calculus。
4. 整条链路仍建立在作者已有 UML interpreter 与 `OBP2` 工具之上。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 部署骨架 | `$\mathcal{D} = (Sys, Env, DAL, Main, DIL, Target)$` | 系统、环境、接口层与目标硬件被显式分层。 |
| 稳定标识 | `$id(e) = fqname(e)$` | fully qualified name 被用作 stable `XMI ID`。 |
| 引用解析 | `$\mathrm{Resolve} : Import \times \mathcal{R}_{xmi} \to Element$` | 跨文件元素引用可在 resource set 内被稳定恢复。 |
| 抽象环境部署 | `$\mathcal{E}_i = \mathrm{Deploy}(Sys, Env_i, DAL, Main)$` | 同一 system model 可挂接多个 abstract environment。 |
| 性质检查 | `$\mathcal{E}_{vv} \models \varphi_{LTL}$` | `OBP2` 在 abstract environment 上做 `LTL` 验证。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | system 与 environment 都可由 UML state machines 承载。 |
| 事件 / 触发 | 很强 | ports、signals、provided/required interfaces 是交互主线。 |
| 守卫 / 数据 | 强支持 | `DAL/DIL` 显式承载设备交互与属性更新。 |
| 层次 | 中等支持 | 重点在 package/composite 层次，而不是状态机理论层次。 |
| 并发 / 同步 | 中等支持 | system-environment 通过 ports/interfaces 协同。 |
| 时间约束 | 弱到中 | 论文里 `LTL` 与 embedded execution 都出现，但不等于 timed-automata 理论。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散 UML 交互模型。 |
| 可执行 / 可验证性 | 很强 | 同一 system model 可进入 simulation、`LTL` checking 和 concrete deployment。 |

### 形式化问题与性质

1. 论文最值得保留的思想，是“不要为了换环境或换目标板就复制一份 system model”。
2. stable `XMI IDs` 是一个很工程、但非常关键的基础设施点，因为它稳定了跨文件 UML 模块化。
3. 这条路线比传统大规模 model transformation 更保守，也更适合做验证后再部署的闭环。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 在 UML 中建 system component。
2. 单独建 abstract 或 concrete environment。
3. 用 `DAL` 定义 system-environment 之间的抽象接口。
4. 在 `Main` 中把两者通过 ports 和 interfaces 组装起来。
5. 部署到板卡时，再补 `DIL` 与 `Target`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 多文件 UML/XMI 资源集。
2. `System / Environment / DAL / Main / DIL / Target` 包结构。
3. stable `XMI IDs` 与 `Element Imports`。
4. `EcoreUtil.resolve()` 恢复的跨文件引用。
5. 底层 `C struct initializer` 与解释器加载链。

### 交换与互操作

这篇论文的互操作重点不在开放行业标准，而在可替换模块之间的稳定链接：

1. 同一 `System` 可反复接不同 `Environment`。
2. `DAL` 使 abstract environment 与 concrete environment 能共享统一接口骨架。
3. `OBP2`、解释器和 `STM32` 部署链共享同一 UML-level 表示。

## 配套基础设施

- 建模/编辑工具：UML 建模环境与多文件 `XMI` 资源集。
- 解析/交换/元模型支持：stable `XMI IDs`、`Element Imports`、`EcoreUtil.resolve()`。
- 仿真/执行支持：作者已有 UML model interpreter 与 `STM32` embedded execution chain。
- 验证/分析支持：`OBP2` 提供 trace-based simulation、state-space exploration 和 `LTL` model-checking。
- 代码生成/转换支持：坚持最小语义改写，重点是部署装配而非大规模语义变换。
- 标准化或社区生态：依托 `UML/XMI`、embedded interpreter 与 `OBP2` 工具线；原文未给独立通用标准。

## 适用场景与需求前提

### 适用场景

适合需要在设计阶段用 abstract environment 做仿真/验证，再用 concrete environment 接真实板卡，而又不希望为每种活动复制系统模型的场景。

### 需求前提

1. system 与 environment 之间的交互能够通过 ports/interfaces 明确表达。
2. 团队接受基于 UML 的模块化建模而非纯手写固件接口。
3. 目标硬件可通过 `DIL/Target` 显式映射。
4. 需要把验证、仿真和部署串成一条可追踪链路。

### 不适用或高成本场景

如果系统环境耦合太深、接口无法被抽象成 `DAL`，或者整个流程并不依赖 UML/XMI，这套模块化部署架构就很难带来收益。

## 与相邻形式主义的关系

相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，本文更偏 system-environment module decomposition；相对 [uml-251-specification/desc.md](../uml-251-specification/desc.md)，它补的是标准 UML 元模型如何被拆成可替换部署单元；相对 [mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md](../mixed-semantics-composition-of-statecharts-for-the-component-based-design-of-reactive-systems/desc.md)，这里关注的是 deployment modularity，而不是 statechart composition semantics。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果未来 `project_1` 生成的是 UML 状态机，不必把“可验证模型”和“可部署模型”看成两份完全不同的工件。

### 作为目标形式主义还是中间表示

这更像目标执行/验证链路的基础设施，而不是新的形式主义主树节点。

### 对需求到模型生成的启发

1. LLM 生成 system model 时，最好连同 environment interface skeleton 一起生成，而不是只给孤立状态机。
2. 生成结果若要服务后续验证和部署，跨文件标识和模块边界必须从一开始就稳定。
3. `System` 与 `Environment` 解耦，本质上是在给“生成-验证-修复”闭环预留替换空间。

### 现实限制

这条路线对 UML 工具链依赖较强，且对 abstract environment 的覆盖质量有明确前提；如果环境建模本身很弱，部署一致性也无法自动保证。

## 重要的相关工作

- [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：本文依赖的直接执行基础层。
- [uml-251-specification/desc.md](../uml-251-specification/desc.md)：`UML State Machine` 与 `XMI` 元模型标准入口。
- [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)：另一条面向验证后部署的 bridge。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / modular deployment architecture`
- 论文角色：modular UML deployment architecture / V&V-execution bridge
