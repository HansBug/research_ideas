# T-UPPAAL：实时系统在线模型驱动测试 / T-UPPAAL: Online Model-based Testing of Real-time Systems

## 基本信息

- 标题：T-UPPAAL: Online Model-based Testing of Real-time Systems
- 中文标题：T-UPPAAL：实时系统在线模型驱动测试
- 作者：Marius Mikucionis，Kim G. Larsen，Brian Nielsen
- 发表：*Proceedings. 19th International Conference on Automated Software Engineering, 2004*，pp. 396-397，2004
- DOI：`10.1109/ASE.2004.1342774`
- 链接：https://doi.org/10.1109/ASE.2004.1342774
- 形式主义：`Timed Automata / T-UPPAAL`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：online model-based testing tool / timed automata testing workflow
- 工具/实现获取方式：论文明确给出 `T-UPPAAL` 网站 `www.cs.auc.dk/~marius/tuppaal` 与 `UPPAAL` 网站 `www.uppaal.com`；其实现是对 `UPPAAL` 引擎的非平凡扩展。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、environment/IUT 模型、adapter API、timed traces 与在线测试算法；无独立交换标准。

## 简报

这篇论文展示了一个很重要的拐点：`Timed Automata` 不只是离线模型检查用的形式主义，也可以直接驱动在线测试。`T-UPPAAL` 一边从环境与规格模型中在线生成下一步测试动作，一边监视实现输出与时间延迟是否仍落在允许范围内，从而把 timed automata 直接接进实际实时系统测试流程。

- 形式主义定位：经典 `Timed Automata` 主干上的在线测试方法与工具条目。
- 构造方式简述：将 environment 与 IUT specification 联合建成 timed automata network，并在运行时维护符号状态集 `Z`，随机执行输入、等待输出或复位。
- 基础设施与场景简述：依托 `UPPAAL` symbolic zone 算法、adapter 组件与 timed conformance 判定，服务嵌入式设备和实时控制系统的自动测试。

```text
environment model + timed specification -> symbolic state set Z -> online stimulus / observation -> pass / fail verdict
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `T-UPPAAL`：

1. environment timed automata。
2. IUT specification timed automata。
3. 运行时维护的符号状态集 `Z`。
4. `EnvOutput / ImpOutput / Delays / ZAfter` 等在线算子。
5. adapter 与物理实现接口。

### 核心抽象

论文明确说明测试规格由系统规格与环境组合构成。可写成：

$$
\mathcal{N}_{test} = A_{spec} \parallel A_{env}
$$

上式中的符号逐项解释如下：

1. `A_{spec}` 是 IUT 的 timed automata 规格。
2. `A_{env}` 是环境假设模型。
3. `\parallel` 表示二者联合决定测试过程中哪些输入、输出和延时是合法的。

运行时的核心对象是论文直接写出的符号状态集：

$$
Z \subseteq S \times E
$$

上式中的符号逐项解释如下：

1. `S` 是规格自动机的状态空间。
2. `E` 是环境自动机的状态空间。
3. `Z` 是在当前已观测 timed trace 后，所有仍可能到达的符号状态对。
4. `T-UPPAAL` 的在线算法每执行一步都在更新这个集合。

论文还给出三类基本动作的更新模式，可保守整理为：

$$
Z \xrightarrow{a} ZAfter_a(Z), \qquad
Z \xrightarrow{\delta} ZAfter_\delta(Z), \qquad
Z \xrightarrow{restart} \{(s_0,e_0)\}
$$

上式中的符号逐项解释如下：

1. `a` 是 tester 主动提供给 IUT 的输入。
2. `\delta` 是等待的一段时间。
3. `restart` 表示复位并从初始符号状态集重新开始。
4. `ZAfter` 是论文算法 1 中的核心更新算子。

### 一个最小例子与通俗解释

论文用咖啡机示例解释 timed automata testing：

1. 用户先投币，再在不同时间请求咖啡。
2. 若等待不足 30 个时间单位，结果一定是 weak coffee。
3. 若等待超过 50 个时间单位，结果一定是 strong coffee。
4. 中间区间允许非确定性。

通俗地说，`T-UPPAAL` 像一个“会看表的自动测试员”。它不会只检查事件顺序，还会检查“事件是不是在允许的时间窗里发生”，并且这个检查是在线进行的。

### 运行 / 接受 / 转移语义

论文算法 1 可压成以下在线循环：

$$
Z_0 = \{(s_0,e_0)\}
$$

$$
while\ Z \neq \emptyset\ \land\ \#iterations \le Td:\ choose\ action\ or\ delay\ or\ restart
$$

上式中的符号逐项解释如下：

1. `Z_0` 是初始符号状态集。
2. `Td` 是测试轮次或预算边界。
3. 每一步随机选择主动输入、等待延时或复位三种操作之一。

论文进一步区分了三个在线查询算子：

$$
EnvOutput(Z), \qquad ImpOutput(Z), \qquad Delays(Z)
$$

它们的含义如下：

1. `EnvOutput(Z)` 是当前环境允许 tester 提供给 IUT 的输入集合。
2. `ImpOutput(Z)` 是当前实现若遵循规格时允许输出的事件集合。
3. `Delays(Z)` 是不违反 invariants 与 guards 的允许等待时长集合。

### 语义边界

这篇论文的边界主要有：

1. 输入输出必须能离散化成 actions。
2. 它假定环境可显式建模，否则在线生成的刺激缺乏约束。
3. 主要面向实时离散控制逻辑，不直接处理连续动力学。
4. 论文重心在工具展示，未在短文中完整展开 conformance 理论细节。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 测试规格骨架 | `$\mathcal{N}_{test} = A_{spec} \parallel A_{env}$` | 说明在线测试总是依赖规格与环境的组合。 |
| 符号状态集 | `$Z \subseteq S \times E$` | 在线算法的核心运行对象。 |
| 基本更新 | `$Z \xrightarrow{a/\delta/restart} \cdots$` | 输入、等待和复位三类操作共同驱动测试。 |
| 在线算子 | `$EnvOutput(Z), ImpOutput(Z), Delays(Z)$` | 分别对应可发输入、合法输出与合法延时。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接以 timed automata 位置与时钟区间组织测试。 |
| 事件 / 触发 | 很强 | 输入、输出和延时都是一等测试对象。 |
| 守卫 / 数据 | 中等支持 | 依赖 `UPPAAL` guard、clock constraints 与有限变量。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 强支持 | 复用了 `UPPAAL` 的 automata network 组合语义。 |
| 时间约束 | 很强 | 在线 testing 的核心就是时间窗口和时钟约束。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散实时系统。 |
| 可执行 / 可验证性 | 很强 | 直接将模型变成 online testing 引擎。 |

### 形式化问题与性质

1. `T-UPPAAL` 把 test generation 与 test execution 合并成在线闭环。
2. 它通过 zones 而不是显式时钟赋值枚举来维持可扩展性。
3. 对本文库而言，它补的是 `Timed Automata` 在线测试工具线，而不是新的自动机子类。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 用 timed automata 建环境模型。
2. 用 timed automata 建 IUT 规格。
3. 实现 adapter，把抽象动作映射到真实设备接口。
4. 把模型交给 `T-UPPAAL` 在线执行测试。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` timed automata network；
2. `Z` 的 zone-based symbolic representation；
3. adapter API；
4. timed trace 与测试日志。

### 交换与互操作

这篇论文的互操作重点在：

1. `T-UPPAAL` 复用了 `UPPAAL` 引擎与模型格式。
2. adapter 把抽象动作翻到真实 IUT。
3. 环境模型让测试输入不再脱离实际使用场景。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 图形建模与验证环境。
- 解析/交换/元模型支持：直接复用 `UPPAAL` timed automata 表示。
- 仿真/执行支持：online test generation and execution。
- 验证/分析支持：zone-based symbolic state manipulation 与即时 fail 判定。
- 代码生成/转换支持：不以代码生成见长，重点是 online testing workflow。
- 标准化或社区生态：依托 `UPPAAL` 工具线和实时嵌入式测试生态。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式设备、工业控制器和需要自动化时序一致性检查的系统测试。

### 需求前提

1. 输入输出需能离散化成 actions。
2. 环境假设需要明确建模。
3. 设备必须允许通过 adapter 进行外部刺激与观测。
4. 需求重点是实时一致性，而不是复杂连续控制律。

### 不适用或高成本场景

如果环境极难建模、输入输出是高维连续信号，或系统主要靠复杂数据结构驱动，这条 timed-automata online testing 路线就会很吃力。

## 与相邻形式主义的关系

相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)，本文更接近工具母线，而后者是工业案例落地条目；相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，二者都在线测试，但 `JTorX` 更偏 `ioco`/LTS 传统，`T-UPPAAL` 更偏 timed automata；相对 [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)，后者是统计验证，本文是在线测试。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明若以后要做“生成-验证-修复”闭环，状态机输出最好能兼容 testing，而不只是离线 model checking。
2. 环境模型和系统模型必须一起考虑，这对需求到模型生成很重要。
3. adapter 这类工程接口也应被视为验证链的一部分。

### 作为目标形式主义还是中间表示

更像 timed automata 在线测试后端，而不是最终状态机前端语言。

## 重要的相关工作

- [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：`T-UPPAAL` 思想的工业案例佐证。
- [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：另一条在线模型驱动测试工具线。
- [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)：同源 `UPPAAL` 家族的统计验证工具。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / T-UPPAAL`
- 论文角色：online model-based testing tool / timed automata testing workflow
- 核心功能：在线生成输入并实时判定实现与 timed 规格的一致性
- 关键特性：symbolic state set `Z`、zones、environment assumptions、adapter、online execution
- 构造方式：`UPPAAL` timed automata + adapter + online symbolic testing algorithm
- 基础设施：`UPPAAL` engine extension、tester API、timed traces
- 适用场景：实时嵌入式设备和控制器的在线测试
- 需求前提：输入输出需离散化且环境需可建模
- 状态：🟢
