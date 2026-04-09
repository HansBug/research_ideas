# PAT 3：构建多领域模型检查器的可扩展体系结构 / PAT 3: An Extensible Architecture for Building Multi-domain Model Checkers

## 基本信息

- 标题：PAT 3: An Extensible Architecture for Building Multi-domain Model Checkers
- 中文标题：PAT 3：构建多领域模型检查器的可扩展体系结构
- 作者：Yang Liu，Jun Sun，Jin Song Dong
- 发表：*2011 IEEE 22nd International Symposium on Software Reliability Engineering*，pp. 190-199，2011
- DOI：`10.1109/ISSRE.2011.19`
- 链接：https://doi.org/10.1109/ISSRE.2011.19
- 形式主义：`PAT 3 / IRL / LTS / TTS / MDP`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：multi-domain model-checking architecture / intermediate-representation tool platform
- 工具/实现获取方式：原文明确说明 `PAT 3` 以 `C#` 实现，模块按 plug-in `DLL` 打包，并提供 module generator tool、内嵌 `BDD` library 与统一 GUI；正文未给独立源码仓库。
- 标准/格式获取方式：原文没有给出中立交换标准；主要承载方式是各领域 DSL 的 plug-in 语法、`IRL` 抽象类、`MoveOneStep/EncodeProcess` 接口和 `BDD` 编码。

## 简报

这篇论文的核心贡献，不是再定义一个新的状态机族，而是把“多种建模语言 + 多类验证算法 + 多个语义域”重新组织成一套可扩展的模型检查器体系结构。`PAT 3` 用中间表示层 `IRL` 把前端 DSL 和后端算法解耦，使同一套平台能够同时容纳并发系统、实时系统和概率系统的分析。

- 形式主义定位：多领域模型检查基础设施，而不是新的状态机本体。
- 构造方式简述：每个 application domain 封装成独立 plug-in；其语义通过 `IRL` 映射到 `LTS / TTS / MDP` 等共同语义层，再由显式或符号算法统一消费。
- 基础设施与场景简述：依托 `C#` plug-in 架构、`IRL` 抽象接口、`BDD` 编码与 module generator tool，服务 DSL 研究、验证算法复用和多语义域实验平台建设。

```text
domain DSL / plug-in -> IRL semantic model -> explicit / symbolic verification algorithms -> analysis results / simulator / checker
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `PAT 3`：

1. application-domain plug-ins；
2. abstraction/support layer；
3. intermediate representation layer (`IRL`)；
4. analysis / verification layer；
5. `MoveOneStep`、`EncodeProcess` 与 `BDD` 编码接口。

### 核心抽象

根据论文给出的四层结构，可把 `PAT 3` 的体系骨架保守整理为：

$$
PAT3 = (ML, AL, IRL, VL)
$$

上式中的符号逐项解释如下：

1. `ML` 是 modeling layer，对应各 application-domain plug-ins 及其 DSL。
2. `AL` 是 abstraction/support layer，承载 GUI、语法支持、共享数据结构和编码设施。
3. `IRL` 是 intermediate representation layer，用于把不同 DSL 收束到共同语义域。
4. `VL` 是 verification layer，负责模型检查、仿真和分析算法。
5. 这是依据论文的架构图和分层文字说明做的保守抽象。

论文明确指出 `IRL` 不止一个模型，而是多种共享语义模型的集合：

$$
IRL = \{ LTS, TTS, MDP \}
$$

上式中的符号逐项解释如下：

1. `LTS` 用于并发离散系统。
2. `TTS` 用于实时系统。
3. `MDP` 用于概率与非确定性混合系统。
4. 这三类语义模型是 `PAT 3` 多领域复用的关键桥层。

论文把统一状态展开接口收束到 `MoveOneStep` 方法。可保守写成：

$$
s \xrightarrow{\mathrm{MoveOneStep}} \{(\alpha_i, s_i')\}_{i=1}^k
$$

上式中的符号逐项解释如下：

1. `s` 是当前 `IRL` 状态对象。
2. `\alpha_i` 是第 `i` 个一步动作或标签。
3. `s_i'` 是执行该动作后的后继状态。
4. `k` 是当前状态可生成的后继分支数量。
5. 论文强调验证算法尽量只依赖这类统一一步展开接口，而不是依赖具体 DSL 细节。

### 一个最小例子与通俗解释

可以把一个最小例子理解成：

1. 某个 plug-in 里有状态 `Idle`。
2. 从 `Idle` 可以一步走向 `Send` 或 `Timeout` 两个后继。
3. 该 plug-in 只要实现 `MoveOneStep`，`PAT 3` 的通用 deadlock checking、reachability 或 refinement checking 就能直接复用。
4. 如果该 plug-in 还提供 `EncodeProcess`，同一模型还能进入 `BDD` 风格符号分析。

通俗地说，`PAT 3` 像“给多种状态机语言搭了一个共同插槽”。前端 DSL 不必各写一套完整工具链，只要把自己的语义接到 `IRL` 插槽上，就能吃到后端验证算法。

### 运行 / 接受 / 转移语义

对显式状态算法而言，核心运行语义就是不断调用统一的一步展开接口：

$$
\mathrm{Succ}(s) = \{ s' \mid \exists \alpha,\ (s \xrightarrow{\alpha} s') \}
$$

上式中的符号逐项解释如下：

1. `\mathrm{Succ}(s)` 是状态 `s` 的后继集合。
2. `\xrightarrow{\alpha}` 表示某个带标签的一步转移。
3. 不同 DSL 的 operational semantics 最终都要落到这个统一可枚举后继集合上。

对符号算法而言，论文强调 `PAT 3` 还支持 `BDD` 编码。可保守写成：

$$
\mathrm{EncodeProcess}(s) = B_s
$$

上式中的符号逐项解释如下：

1. `s` 是某个 process / system state。
2. `B_s` 是与之对应的 `BDD` 编码。
3. 该编码使同一 `IRL` 状态既可被显式遍历，也可被符号算法消费。

### 语义边界

这篇论文的边界主要有：

1. 它解决的是工具架构与语义接口复用，不是某个单一形式主义的完整理论定义。
2. `IRL` 目前主要覆盖 `LTS / TTS / MDP` 三类主干，并不等于“所有形式化模型都能无损纳入”。
3. 各 plug-in 仍需自己实现语言语义与到 `IRL` 的映射。
4. 连续动力学和高维混成模型不在这篇论文的主线范围内。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 四层体系骨架 | `$PAT3 = (ML, AL, IRL, VL)$` | 说明 `PAT 3` 通过分层解耦前端 DSL 与后端算法。 |
| 共享语义域 | `$IRL = \{ LTS, TTS, MDP \}$` | 并发、实时、概率三类系统在平台里共用的语义骨架。 |
| 一步展开接口 | `$s \xrightarrow{\mathrm{MoveOneStep}} \{(\alpha_i, s_i')\}_{i=1}^k$` | 通用验证算法最依赖的统一状态接口。 |
| 符号编码接口 | `$\mathrm{EncodeProcess}(s) = B_s$` | 同一体系同时支持显式与 `BDD` 风格符号分析。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以 `IRL` 状态对象为核心统一多类模型。 |
| 事件 / 触发 | 强支持 | `MoveOneStep` 返回带标签的一步转移。 |
| 守卫 / 数据 | 条件支持 | 由各 plug-in 语言自行承载，再映射到 `IRL`。 |
| 层次 | 弱支持 | 不是层次状态机本体论文，但可通过 plug-in 接入复杂 DSL。 |
| 并发 / 同步 | 强支持 | `LTS` 线直接面向并发系统。 |
| 时间约束 | 强支持 | `TTS` 是论文明确支持的共享语义域。 |
| 连续动态 / 随机性 | 支持随机性，不支持连续动态 | `MDP` 已纳入；连续混成不在主线内。 |
| 可执行 / 可验证性 | 很强 | 同时支持显式模型检查、符号模型检查与多种算法复用。 |

### 形式化问题与性质

1. `PAT 3` 的关键价值是“语言与算法的中间解耦层”，而不是单个模型检查算法。
2. `MoveOneStep` 和 `EncodeProcess` 这类接口使新 DSL 可以低成本接到既有验证器上。
3. 对本文库而言，它补的是“多语义域状态机平台如何工程化”的基础设施证据。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 为某个 application domain 编写语法和语义 plug-in。
2. 把该 DSL 的运行语义映射到 `IRL`。
3. 视需要实现 `MoveOneStep`、`EncodeProcess` 等接口。
4. 再复用平台已有 checker、simulator 和 reduction algorithm。

### 机器可处理承载方式

机器可处理承载方式包括：

1. plug-in `DLL`；
2. 语法文件与语义类；
3. `IRL` 抽象类；
4. `BDD` 编码；
5. module generator tool 生成的骨架工程。

### 交换与互操作

这篇论文的互操作重点不在外部中立文件标准，而在平台内部语义互操作：

1. 不同 DSL 通过 `IRL` 共享算法。
2. 显式与符号分析通过统一状态接口并行成立。
3. 新 plug-in 可以独立开发，再被 GUI 和分析层自动识别。

## 配套基础设施

- 建模/编辑工具：统一 GUI、语法文件与 module generator tool。
- 解析/交换/元模型支持：plug-in framework、抽象类接口与语义层分离。
- 仿真/执行支持：各 `IRL` 模型上的 simulator 与状态探索。
- 验证/分析支持：deadlock checking、reachability、refinement checking、`BDD`-based symbolic model checking 等。
- 代码生成/转换支持：不是代码生成平台，重点是语义映射与算法复用。
- 标准化或社区生态：以 `PAT` 平台和 plug-in 机制为中心，适合持续扩展研究型 DSL。

## 适用场景与需求前提

### 适用场景

适合需要快速构造新建模 DSL、又希望立即复用成熟模型检查算法的研究平台、教学平台和原型工具链。

### 需求前提

1. 目标语言的 operational semantics 能稳定映射到 `LTS / TTS / MDP` 一类共享语义。
2. 团队接受 plug-in 式平台扩展，而不是每种 DSL 单独重写验证器。
3. 需要同时覆盖显式与符号分析路径。
4. 关注点是多领域模型检查基础设施，而不是某一行业专用应用界面。

### 不适用或高成本场景

如果目标模型强依赖连续动力学、重度数值仿真或完全不同的语义骨架，直接接入 `PAT 3` 会比较困难。

## 与相邻形式主义的关系

相对 [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)，`PRISM` 聚焦概率模型检查平台，而 `PAT 3` 追求多语义域统一架构；相对 [d-finder-a-tool-for-compositional-deadlock-detection-and-verification/desc.md](../d-finder-a-tool-for-compositional-deadlock-detection-and-verification/desc.md)，`D-Finder` 更偏 `BIP` 死锁验证专用后端，而 `PAT 3` 更像多 DSL 的公共母平台；相对 [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)，二者都重视工程化工具链，但 `CIF 3` 更偏单家族 supervisory-control engineering，`PAT 3` 更偏跨领域模型检查架构。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机文库的价值不只在模型本体，还在能否接入统一的分析平台”。
2. 如果 `project_1` 未来要让 LLM 生成多种状态机工件并共享验证后端，`IRL` 这种中间语义层非常值得借鉴。
3. 对生成-验证-修复闭环来说，`MoveOneStep` 级统一接口也有利于把模型操作做成通用工具能力。

### 作为目标形式主义还是中间表示

它显然更像多形式主义验证平台和中间基础设施，而不是最终交付给用户的状态机语言。

## 重要的相关工作

- [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)：概率模型检查平台的另一条重量级基础设施母线。
- [d-finder-a-tool-for-compositional-deadlock-detection-and-verification/desc.md](../d-finder-a-tool-for-compositional-deadlock-detection-and-verification/desc.md)：专门面向 `BIP` 的组合验证后端，对照 `PAT 3` 的多领域平台定位。
- [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)：单家族控制工程工具链与跨领域平台之间的对照条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`PAT 3 / IRL / LTS / TTS / MDP`
- 论文角色：multi-domain model-checking architecture / intermediate-representation tool platform
- 核心功能：用 `IRL` 解耦多前端 DSL 与多后端验证算法
- 关键特性：四层架构、plug-in `DLL`、`MoveOneStep`、`EncodeProcess`、`BDD` 库
- 构造方式：domain plug-in -> `IRL` semantic model -> explicit / symbolic analysis
- 基础设施：GUI、module generator、`IRL` 抽象接口、显式/符号模型检查器
- 适用场景：研究型 DSL 平台、多领域模型检查实验与语义复用
- 需求前提：语言语义需能稳定映射到共享 `IRL` 骨架
