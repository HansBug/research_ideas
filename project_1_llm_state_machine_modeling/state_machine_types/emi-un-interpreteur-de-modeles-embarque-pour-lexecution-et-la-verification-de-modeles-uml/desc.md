# EMI：用于 UML 模型执行与验证的嵌入式解释器 / EMI: Un Interpréteur de Modèles Embarqué pour l’Exécution et la Vérification de Modèles UML

## 基本信息

- 标题：EMI : Un Interpréteur de Modèles Embarqué pour l’Exécution et la Vérification de Modèles UML
- 中文标题：EMI：用于 UML 模型执行与验证的嵌入式解释器
- 作者：Valentin Besnard，Matthias Brun，Philippe Dhaussy，Frédéric Jouault，Ciprian Teodorov
- 发表：*18e journées Approches Formelles dans l’Assistance au Développement de Logiciels*，2019
- DOI：原文未提供
- 链接：https://www.obpcdl.org/assets/papers/afadl-2019-outil.pdf
- 形式主义：`executable UML subset / EMI / OBP2 bridge`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：统一 `UML` 解释执行与形式验证语义的嵌入式运行时 / 验证桥接器
- 工具/实现获取方式：原文说明 `EMI` 可与 `OBP2` 配合使用，并给出 `OBP2` 入口 `https://plug-obp.github.io/`；未给独立公开仓库。
- 标准/格式获取方式：核心承载不是独立交换标准，而是受限 `UML` 子集、模型到 `C` 结构初始化器的序列化形式，以及解释器通信接口。

## 简报

这篇论文补的是 `UML` 线里非常关键的一类基础设施证据：不是再做一次 `UML -> formal model -> verifier` 的离线翻译，而是直接让同一个模型解释器同时承担执行语义和验证语义。`EMI` 的核心承诺是“执行时用哪套语义，验证时就还是哪套语义”，从而尽量消除模型转换与可执行代码之间的语义偏差。

- 形式主义定位：可执行 `UML` 子集的统一运行时与验证桥接载体。
- 构造方式简述：先用 `UML` 类图、组合结构图和状态机描述系统，再把模型序列化为 `C` 结构初始化数据，编译进解释器，由 `EMI` 统一执行。
- 基础设施与场景简述：依托 `EMI`、通信接口、`OBP2`、`LTL`/observer 验证、状态空间探索与 `STM32` bare-metal 部署，服务嵌入式软件的设计期验证与执行期运行。

```text
UML design model -> C-serialized runtime model -> EMI operational semantics -> simulation / OBP2 exploration / LTL checking / embedded execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 一个受限但可执行的 `UML` 子集。
2. `EMI` 解释器内部的统一操作语义。
3. 从 `UML` 到 `C` 结构初始化器的模型序列化。
4. 与 `OBP2` 连接的通信接口。
5. 直接在解释器之上开展的 `LTL`、observer、simulation、state-space exploration 与 deadlock detection。

### 核心抽象

结合原文“支持类图、组合结构图、状态转换图，并用 `C` 宏扩展动作语言”的描述，可把 `EMI` 面向的可执行模型骨架保守整理为：

$$
\mathcal U = (\mathcal C,\mathcal R,\mathcal S,\mathcal T,\mathcal A)
$$

上式中的符号逐项解释如下：

1. `\mathcal C` 是类与对象类型集合。
2. `\mathcal R` 是组合结构、端口与连接关系。
3. `\mathcal S` 是各对象关联的状态机集合。
4. `\mathcal T` 是状态机中的转移集合。
5. `\mathcal A` 是用 `C` 语言及其宏表达的 guard/effect/action 片段。
6. 该元组不是论文直接给出的统一记法，而是依据论文支持的 `UML` 子集做的保守压缩。

解释器在任意时刻维护的动态配置，可保守写成：

$$
\gamma = (\sigma_{obj},\sigma_{sm},\sigma_{evt})
$$

上式中的符号逐项解释如下：

1. `\sigma_{obj}` 表示对象及其属性值的当前存储。
2. `\sigma_{sm}` 表示各状态机当前所处的控制配置。
3. `\sigma_{evt}` 表示事件池或待处理事件相关信息。
4. 这组记号对应论文所说“解释器当前配置”的动态部分。

### 一个最小例子与通俗解释

一个最小直觉例子可以是单个主动对象的门控控制器：

1. 初始状态是 `Idle`。
2. 事件 `trainComing` 到达后，满足 guard，就触发从 `Idle` 到 `Closing` 的转移。
3. 转移效果调用动作语言里的 `C` 宏，修改对象属性，例如“门正在下降”。
4. 当传感器确认 `gateDown` 后，再从 `Closing` 进入 `Closed`。

通俗地说，`EMI` 像“把 `UML` 状态机装进一个统一虚拟机”。模型不先被改写成另一套形式语言再验证，而是直接由解释器给出“当前配置是什么、哪些转移可触发、触发后到哪”的统一语义。

### 运行 / 接受 / 转移语义

论文明确说明通信接口至少支持“读当前配置、设定配置、收集可触发转移、触发某个转移”。这可以压成：

$$
\mathrm{Enabled}(\gamma) = \{\, t \in \mathcal T \mid \gamma \xrightarrow{t} \gamma' \,\}
$$

上式中的符号逐项解释如下：

1. `\gamma` 是当前解释器配置。
2. `t` 是某条候选转移。
3. `\gamma \xrightarrow{t} \gamma'` 表示在当前配置下触发 `t` 后到达新配置 `\gamma'`。
4. `\mathrm{Enabled}(\gamma)` 是当前所有可触发转移的集合，也就是外部验证器可查询到的 fireable transitions。

该论文最重要的语义主张可压成：

$$
\mathrm{Sem}_{exec}(\mathcal U) = \mathrm{Sem}_{vv}(\mathcal U)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Sem}_{exec}` 表示执行期使用的操作语义。
2. `\mathrm{Sem}_{vv}` 表示验证与确认活动使用的操作语义。
3. 这不是形式定理，而是论文的系统设计原则：执行与验证复用同一解释器语义实现。

### 语义边界

1. `EMI` 并不覆盖完整 `UML`，而是依赖一个受限子集。
2. 动作语言采用 `C` 及宏扩展，这意味着复杂语义仍可能落在外部 `C` 代码里。
3. `UML` 的语义变异点并非保持开放，而是由解释器固定或在编译时配置。
4. 论文重点是“统一语义实现”，不是提出新的 `UML` 数学本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 可执行模型骨架 | `$\mathcal U = (\mathcal C,\mathcal R,\mathcal S,\mathcal T,\mathcal A)$` | `EMI` 面向的是带结构、状态机与动作语言的受限 `UML` 子集。 |
| 当前运行配置 | `$\gamma = (\sigma_{obj},\sigma_{sm},\sigma_{evt})$` | 解释器把对象、状态机控制位和事件环境统一成可查询配置。 |
| 可触发转移查询 | `$\mathrm{Enabled}(\gamma)=\{t \mid \gamma \xrightarrow{t} \gamma'\}$` | 外部验证器通过接口获取当前 fireable transitions。 |
| 统一语义原则 | `$\mathrm{Sem}_{exec}(\mathcal U)=\mathrm{Sem}_{vv}(\mathcal U)$` | 执行与验证共享同一解释器语义实现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `UML` 状态机是主体。 |
| 事件 / 触发 | 很强 | 通过事件池与可触发转移接口驱动。 |
| 守卫 / 数据 | 强支持 | guard/effect 可由 `C` 宏访问对象属性。 |
| 层次 | 中等支持 | 基于 `UML` 状态机，但本文重点不在层次语义全覆盖。 |
| 并发 / 同步 | 中等支持 | 组合结构与多个对象并存，但论文未把复杂并发语义作为主卖点。 |
| 时间约束 | 弱支持 | 本文不是 timed semantics 路线。 |
| 连续动态 / 随机性 | 不支持 | 不属于该解释器主线。 |
| 可执行 / 可验证性 | 很强 | simulation、`LTL`、observer、state exploration、deadlock detection 与嵌入式执行已打通。 |

### 形式化问题与性质

1. 这篇论文最关键的不是 `UML` 状态机语法，而是“不要在执行链和验证链里维护两套语义实现”。
2. 解释器通信接口把 `UML` 模型暴露成了一个可被验证器操控的 transition system。
3. 对文库而言，它是 `UML runtime / verification bridge` 的高价值基础设施条目，而不是新的主树节点。

## 构造方式与承载格式

### 建模入口

原文明确给出的建模入口包括：

1. `UML` 类图。
2. 组合结构图。
3. 状态转换图。
4. 以 `C` 为基础、带模型访问宏的动作语言。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 将模型元素转写成 `C` 结构初始化器。
2. 编译后的解释器可执行二进制。
3. 面向外部验证器的当前配置 / 设置配置 / 可触发转移 / 触发转移接口。

### 交换与互操作

这篇论文的互操作重点不在中立文件标准，而在运行时桥接：

1. `UML` 模型先被装载进 `EMI`。
2. `OBP2` 通过通信接口驱动解释器。
3. `LTL`、observer、simulation、state-space exploration 与 deadlock detection 全部围绕同一个解释器实例进行。

## 配套基础设施

- 建模/编辑工具：原文要求模型符合受限 `UML` 子集，但未固定某一具体建模器。
- 解析/交换/元模型支持：模型序列化为 `C` 结构初始化数据，再与解释器一起编译装载。
- 仿真/执行支持：支持交互式 simulation，可在 Linux 和 bare-metal `STM32 discovery` 上运行。
- 验证/分析支持：`OBP2` 支持 `LTL`、observer automata、状态空间探索与 deadlock detection。
- 代码生成/转换支持：核心不是传统代码生成，而是“模型序列化 + 解释器编译装载”式部署。
- 标准化或社区生态：依托 `UML` 子集、`EMI` 原型和 `OBP2` 工具线；原文未给更广泛的通用标准生态。

## 适用场景与需求前提

### 适用场景

适合那些已经采用 `UML` 状态机建模、又强烈担心“设计模型验证结果无法传到可执行系统”的嵌入式软件场景，尤其适合需要把 simulation、formal verification 和部署尽量收束到同一语义底盘的团队。

### 需求前提

1. 模型必须能落到 `EMI` 支持的受限 `UML` 子集。
2. guard 与 effect 最好能稳定写成 `C` 动作语言宏。
3. 团队确实需要在设计、验证与执行之间保持统一语义实现，而不是只做离线代码生成。

### 不适用或高成本场景

如果系统强依赖完整 `UML` 全语义、复杂时间/概率扩展，或者更希望使用中立交换标准而非解释器式运行时，`EMI` 就不是最直接的入口。

## 与相邻形式主义的关系

相对 [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)，本文更像其同一研究线中的工具化锚点；相对 [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)，那篇更强调 observer 工作流，而本文更强调统一解释器本体；相对 [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)，后者补的是多环境部署结构，本文补的是核心解释器与验证接口。

## 与本研究的关系

### 对 Project 1 的价值

1. 它直接说明“同一状态机语义实现贯穿建模、验证、部署”是一条可行路线。
2. 这对 `project_1` 很关键，因为后续若由 `LLM` 生成状态机，仅有静态模型还不够，还要考虑解释与验证是不是共用同一语义。
3. 它也为 `UML` 线提供了比“只会导出到别的验证器”更强的一类基础设施证据。

### 作为目标形式主义还是中间表示

更像目标形式主义周边的执行 / 验证载体，而不是新的中间表示家族。

### 对需求到模型生成的启发

1. 若未来从需求自动生成 `UML` 状态机，最好同步生成“可执行语义所需的最小子集约束”，而不是放任使用全量 `UML`。
2. 解释器公开“当前配置 / 可触发转移”接口，提示后续验证闭环可以直接围绕运行时状态搭建，而不必总是再做一次模型转换。
3. 对安全关键场景而言，“语义共用”本身就是一项高价值基础设施特性。

### 现实限制

这条路线很依赖特定解释器实现和其支持子集，离“开放标准级互操作”还有距离。

## 重要的相关工作

1. [unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md](../unified-ltl-verification-and-embedded-execution-of-uml-models/desc.md)：同一 `UML` 解释执行与 `LTL` 验证母线。
2. [verifying-and-monitoring-uml-models-with-observer-automata/desc.md](../verifying-and-monitoring-uml-models-with-observer-automata/desc.md)：`EMI + OBP2` 的 observer 监控分支。
3. [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：设计到运行时桥接的相邻 `UML` 解释执行路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`executable UML subset / EMI / OBP2 bridge`
- 归类理由：主贡献是统一 `UML` 模型执行与验证语义的解释器、接口和运行时工具链，而不是新的状态机母型。
