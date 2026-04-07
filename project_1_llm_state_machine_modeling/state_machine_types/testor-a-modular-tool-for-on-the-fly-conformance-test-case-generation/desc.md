# TESTOR：一种模块化的在线一致性测试用例生成工具 / TESTOR: A Modular Tool for On-the-Fly Conformance Test Case Generation

## 基本信息

- 标题：TESTOR: A Modular Tool for On-the-Fly Conformance Test Case Generation
- 中文标题：TESTOR：一种模块化的在线一致性测试用例生成工具
- 作者：Lina Marsso，Radu Mateescu，Wendelin Serwe
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 211-228，2018
- DOI：`10.1007/978-3-319-89963-3_13`
- 链接：https://doi.org/10.1007/978-3-319-89963-3_13
- 形式主义：`IOLTS / ioco / CADP / TESTOR`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：CADP-based modular on-the-fly conformance testing tool
- 工具/实现获取方式：论文明确给出 `TESTOR` 工具与原始入口 `http://convecs.inria.fr/software/testor`，并说明它构建在 `CADP / OPEN-CAESAR` 之上。
- 标准/格式获取方式：核心承载方式是 `IOLTS`、test purpose、`LNT`、`CADP` post functions 与 `OPEN-CAESAR` 图变换组件，不是单独交换标准。

## 简报

这篇论文的价值，不在于再定义一次 `ioco`，而在于把 test purpose guided conformance testing 做成真正模块化、按需、可在线抽取的工具链。`TESTOR` 沿着 `TGV` 传统走，但把同步积、`τ`-reduction、determinization、`BES` 求解和 controllable test case 提取拆成可替换的组件，并直接利用 `CADP` 的图操作底盘。

- 形式主义定位：`IOLTS / ioco` testing infrastructure，而不是新的接口模型家族。
- 构造方式简述：从 model 和 test purpose 出发，先算 `SP_{vis} = det(\Delta(SP))`，再用 explorer + `BES` solver 在线抽 `CTG` 或 controllable `TC`。
- 基础设施与场景简述：依托 `CADP / OPEN-CAESAR / LNT`，服务黑盒一致性测试、异步并发系统与大型非回归测试集。

```text
IOLTS model + test purpose -> synchronous product -> τ-reductions + determinization -> SPvis -> explorer + BES solver -> CTG / controllable TC -> online conformance testing
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. input/output labelled transition system (`IOLTS`)。
2. test purpose (`TP`)。
3. complete test graph (`CTG`)。
4. test case (`TC`)。
5. `TESTOR` 的 modular architecture。

### 核心抽象

论文对行为模型采用 `IOLTS`：

$$
M = (Q, A, T, q_0)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `A = A_I \cup A_O \cup \{\tau\}` 是动作集合。
3. `T \subseteq Q \times A \times Q` 是迁移关系。
4. `q_0` 是初始状态。
5. `A_I` 与 `A_O` 分别是输入与输出动作集合。

论文把 tester 选择的可观察语义收束为：

$$
SP_{vis} = \det(\Delta(SP))
$$

上式中的符号逐项解释如下：

1. `SP` 是 model 与 test purpose 的同步积。
2. `\Delta(SP)` 是把 quiescence 显式化后的 suspension automaton。
3. `\det` 是确定化。
4. `SP_{vis}` 是后续构造 `CTG / TC` 的共同底盘。

论文对 reachability-to-accept 的判断直接给出 `PDL` 公式：

$$
\varphi_{l2a} = \langle true^* \rangle accept
$$

上式中的符号逐项解释如下：

1. `accept` 表示 test purpose 的接受状态。
2. `\langle true^* \rangle` 表示从当前状态沿任意有限路径可达。
3. 满足该公式的状态属于 `L2A`，也就是“lead to accept” 的状态集合。
4. `TESTOR` 用 `BES` solver 在线判断这个条件。

围绕工具架构，可保守压成：

$$
\mathrm{TESTOR} = (\mathrm{SyncProd}, \mathrm{TauComp}, \mathrm{TauConfl}, \mathrm{TauClosure}, \mathrm{Det}, \mathrm{Explorer}, \mathrm{BES})
$$

上式中的符号逐项解释如下：

1. `SyncProd` 生成 model 与 `TP` 的同步积。
2. `TauComp / TauConfl / TauClosure` 是若干 `τ`-reduction。
3. `Det` 是确定化组件。
4. `Explorer` 在线抽取 `CTG` 或 `TC`。
5. `BES` 是 reachability-to-accept 的在线求解后端。

### 一个最小例子与通俗解释

论文里的 toy example 非常适合直觉说明：

1. model 有若干 `?a / ?b / !x / !y / !z` 行为。
2. test purpose 想捕捉“先观察到 `!y` 再观察到 `!z`”这条路径。
3. `TESTOR` 不会先把所有测试树完整离线展开，而是先算 `SP_{vis}`，再只保留能 lead to accept 的部分。
4. 如果某处需要控制输入，它就只保留一条输入分支；如果某处需要观察输出，它就保留所有 relevant outputs。

通俗地说，`TESTOR` 像一个“带目标的在线测试提取器”。你先告诉它想把系统往哪个 accept 状态赶，它再边探索边抽出一个真正可执行、可控的测试器。

### 运行 / 接受 / 转移语义

论文强调 `CTG` 是 `SP_{vis}` 上所有 `L2A` 状态诱导出的子图，而 `TC` 则是其 controllable 子图。可保守写成：

$$
CTG = SP_{vis}\!\upharpoonright_{L2A}
$$

并且：

$$
q \in L2A \iff q \models \varphi_{l2a}
$$

上式中的符号逐项解释如下：

1. `SP_{vis}\!\upharpoonright_{L2A}` 表示限制在 `L2A` 上的子图。
2. `q \models \varphi_{l2a}` 表示状态 `q` 能到达 accept。
3. 这决定了某个分支应保留、标成 pass，还是转成 inconclusive / fail。

### 语义边界

边界主要有：

1. 主线依赖 `IOLTS / ioco` testing 假设。
2. 工具主要面向黑盒 conformance testing，而不是白盒执行验证。
3. test purpose 语义和 controllability 约束是工具关键前提。
4. 它继承 `CADP` 生态，因此工程入口更偏形式模型和图变换工作流。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `IOLTS` 骨架 | `$M = (Q, A, T, q_0)$` | `TESTOR` 的输入模型。 |
| 可观察底盘 | `$SP_{vis} = \det(\Delta(SP))$` | 先显式化 quiescence，再确定化。 |
| accept 可达性 | `$\varphi_{l2a} = \langle true^* \rangle accept$` | 由 `BES` 在线判断哪些状态还能到 accept。 |
| 工具架构 | `$\mathrm{TESTOR} = (\mathrm{SyncProd}, \mathrm{TauComp}, \mathrm{TauConfl}, \mathrm{TauClosure}, \mathrm{Det}, \mathrm{Explorer}, \mathrm{BES})$` | 模块化流水线的最小抽象。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心对象就是 `IOLTS` 状态图和其变换。 |
| 事件 / 触发 | 很强 | test purpose、输入控制和输出观察都以动作标签为中心。 |
| 守卫 / 数据 | 中等支持 | 通过 `LNT` 与 CADP 模型承载数据化 test purpose，但主线仍是行为测试。 |
| 层次 | 不适用 | 不是层次状态机论文。 |
| 并发 / 同步 | 很强 | 同步积、multiway rendezvous 与 `τ`-interleavings 都是主线。 |
| 时间约束 | 弱支持 | 主体不是 timed-testing。 |
| 连续动态 / 随机性 | 不支持 | 完全不在本文范围。 |
| 可执行 / 可验证性 | 很强 | 直接在线提取 controllable `TC` 并接真实测试流程。 |

### 形式化问题与性质

1. `TESTOR` 真正的改进点是“完全按需在线抽 `TC`”，而不是先整张 `CTG` 落地。
2. 模块化架构使 `τ`-reduction、同步积与 explorer 都能替换或细化。
3. 多路 rendezvous 让 test purpose 表达比传统 TGV 路线更灵活。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. `IOLTS` 模型。
2. test purpose。
3. `LNT` 进程描述。
4. `CADP` / `OPEN-CAESAR` post functions。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `SP`、`Δ(SP)` 与 `SP_{vis}` 这些中间图对象；
2. `CTG / TC`；
3. `BES` 公式与 diagnostics；
4. `CADP` 图操作组件。

### 交换与互操作

互操作重点在 `CADP` 生态内部：

1. 上游可以用 `LNT` 等形式模型描述待测系统与 test purpose。
2. 中间完全基于 `OPEN-CAESAR` 图变换接口。
3. 下游输出的是 controllable `TC` 或 `CTG`，可直接服务在线测试。

## 配套基础设施

- 建模/编辑工具：`LNT` 与 `CADP` 建模环境。
- 解析/交换/元模型支持：`OPEN-CAESAR` 提供 on-the-fly graph manipulation。
- 仿真/执行支持：工具直接面向在线测试用例抽取。
- 验证/分析支持：`τ`-compression、`τ`-confluence、`τ`-closure、determinization、`BES` 求解与 diagnostics。
- 代码生成/转换支持：不是代码生成论文，但它实现了从 model/test purpose 到 `TC/CTG` 的自动变换链。
- 标准化或社区生态：深度依赖 `CADP` 和 `ioco` testing 传统。

## 适用场景与需求前提

### 适用场景

适合异步并发系统、协议、组件接口与其他需要黑盒在线 conformance testing 的系统，尤其适合 test purpose 明确、只想抽取可执行局部测试器的场景。

### 需求前提

1. 系统可被建模成 `IOLTS`。
2. 输入输出方向必须清晰。
3. 团队愿意显式编写 test purposes。
4. 测试更关注 conformance 与 acceptance reachability，而不是代码覆盖率。

### 不适用或高成本场景

如果系统不能稳定压成 `IOLTS`，或者团队没有 formal model / test purpose 工作流，`TESTOR` 的门槛会较高。

## 与相邻形式主义的关系

相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，`TorX` 更像早期在线 MBT 原型骨架；相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，`JTorX` 更强调 Twente 工具线和 explorer/adapter 协议，而 `TESTOR` 更深地绑定 `CADP` 模块化图操作底盘；相对 [conformance-testing-with-labelled-transition-systems-implementation-relations-and-test-generation/desc.md](../conformance-testing-with-labelled-transition-systems-implementation-relations-and-test-generation/desc.md)，本文是理论母线之后的工具化、组件化落地。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的意义在于，它展示了“状态机生成之后怎么接到在线测试闭环”这件事可以做到多模块、可替换、按需探索。如果未来 LLM 生成模型后还要继续做测试场景生成、counterexample 回流与修复，`TESTOR` 这类架构很有参考价值。

### 作为目标形式主义还是中间表示

更像测试基础设施，而不是最终交付给领域工程师编辑的状态机形式主义。

### 对需求到模型生成的启发

1. 需求里最好尽早分清“必须达到的接受状态”和“可忽略分支”，这样 test purpose 更容易自动化。
2. 若生成模型天然能落成 `IOLTS`，后续在线测试就有成熟基础设施可接。
3. toolchain 设计上要保留中间图对象和 diagnostics，而不是只要最终 verdict。

### 现实限制

它依赖 formal testing workflow，且主要针对离散输入输出系统。

## 重要的相关工作

1. [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：更早的在线 `ioco` 测试工具原型。
2. [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：Twente `ioco` 工具线的 Java 工作台。
3. [conformance-testing-with-labelled-transition-systems-implementation-relations-and-test-generation/desc.md](../conformance-testing-with-labelled-transition-systems-implementation-relations-and-test-generation/desc.md)：`ioconf` / conformance-testing 理论母线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`IOLTS / ioco / CADP / TESTOR`
- 论文角色：CADP-based modular on-the-fly conformance testing tool
- 归类理由：论文主体是基于 `IOLTS / ioco` 的测试基础设施与在线提取方法，贡献落在工具链和方法闭环，而不是新的模型本体。
