# SENSE：面向网络化控制系统的基于抽象的综合 / SENSE: Abstraction-Based Synthesis of Networked Control Systems

## 基本信息

- 标题：SENSE: Abstraction-Based Synthesis of Networked Control Systems
- 中文标题：SENSE：面向网络化控制系统的基于抽象的综合
- 作者：Mahmoud Khaled，Matthias Rungger，Majid Zamani
- 发表：*Electronic Proceedings in Theoretical Computer Science*，272:65-78，2018
- DOI：`10.4204/eptcs.272.6`
- 链接：https://doi.org/10.4204/EPTCS.272.6
- 形式主义：`networked control systems / symbolic models / BDD-based controller synthesis / SENSE`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：BDD-based symbolic-abstraction and controller-synthesis framework for networked control systems
- 工具/实现获取方式：原文将 `SENSE` 说明为 open-source extensible framework；公开入口可通过作者团队归档页面 `https://webarchiv.typo3.tum.de/EI/hcs/software/sense/` 获取。
- 标准/格式获取方式：主承载是 plant symbolic model 的 BDD files、delay-bound configuration、controller BDDs、`MATLAB/OMNeT++` interfaces 与自动代码生成工具；不是中立行业标准。

## 简报

`SENSE` 可以看作 `SCOTS` 在线控网络环境下的扩展版后端：它不重新从零建 plant abstraction，而是拿 plant 的 symbolic model，加上 sensor-to-controller / controller-to-actuator 的延迟、丢包、量化等网络非理想因素，直接构造 NCS 的 symbolic model，并继续在其上综合满足 `LTL`-style safety / reachability / persistence / recurrence 规格的控制器。

- 形式主义定位：网络化控制系统 (`NCS`) 的 symbolic modeling、controller synthesis 与 deployment helper framework。
- 构造方式简述：`SCOTS` 生成 plant symbolic model -> `SENSE` 用 `L` operator 和 BDD operations 扩展到 NCS symbolic model -> fixed-point controller synthesis -> `MATLAB/OMNeT++` simulation -> `C/C++` 或 `VHDL/Verilog` code generation。
- 基础设施与场景简述：依托 `BDD/CUDD`、`SCOTS`、`MATLAB`、`OMNeT++` 和 helper tools，服务带延迟、丢包和量化误差的 CPS/NCS 控制综合。

```text
plant symbolic model + network delay bounds -> BDD-based NCS symbolic model -> fixed-point controller synthesis -> simulation / analysis / code generation
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `NCS` 中的 plant symbolic model；
2. 网络非理想因素下的扩展 symbolic model；
3. `BDD`-based transition representation；
4. fixed-point synthesis algorithms；
5. simulation / analysis / code-generation toolchain。

### 核心抽象

论文先给出统一的 system 定义：

$$
S = (X, X_0, U, F)
$$

上式中的符号逐项解释如下：

1. `$X$` 是状态集合。
2. `$X_0 \subseteq X$` 是初始状态集合。
3. `$U$` 是输入集合。
4. `$F \subseteq X \times U \times X$` 是转移关系。
5. 作为 map 看时，`$F(x,u)$` 表示所有后继状态。

对连续 plant 的符号抽象，论文记为：

$$
S_q(S) = (X_q, X_{q,0}, U_q, F_q)
$$

上式中的符号逐项解释如下：

1. `$X_q$` 是有限抽象状态集。
2. `$X_{q,0}$` 是抽象初始状态集。
3. `$U_q$` 是有限输入集。
4. `$F_q$` 是抽象转移关系。
5. 该 symbolic model 通常由 `SCOTS` 构造。

`SENSE` 的关键对象是把网络影响并入后的扩展模型：

$$
\widetilde{S}_q(S) = L(S_q(S), N^{sc}_{min}, N^{sc}_{max}, N^{ca}_{min}, N^{ca}_{max}) = (\widetilde{X}_q, \widetilde{X}_{q,0}, U_q, \widetilde{F}_q)
$$

上式中的符号逐项解释如下：

1. `$L(\cdot)$` 是把 plant symbolic model 扩展为 `NCS` symbolic model 的构造算子。
2. `$N^{sc}_{min}, N^{sc}_{max}$` 是 sensor-to-controller delay bounds。
3. `$N^{ca}_{min}, N^{ca}_{max}$` 是 controller-to-actuator delay bounds。
4. `$\widetilde{X}_q$` 把原 plant state、传输中的 packets 和 delay counters 一起编码进抽象状态。
5. `$\widetilde{F}_q$` 是考虑网络非理想因素后的抽象转移关系。

### 一个最小例子与通俗解释

一个最小例子可以这样理解：

1. 你已经有了一个 plant 的符号抽象，例如移动机器人在二维平面上的离散状态和控制输入。
2. 但真实系统不是“控制器直接连 plant”，而是隔着网络，存在延迟、丢包、量化误差。
3. `SENSE` 会把“当前真实状态 + 网络里排队的旧状态包 + 旧控制包 + 各通道延迟计数”一起做成新状态。
4. 然后它再在这个更大的离散系统上综合 controller，并给出仿真接口与实现代码。

通俗地说，`SENSE` 做的是“把网络问题也放进状态机里一起考虑”，而不是先综合一个理想控制器，部署时再祈祷网络别出事。

### 运行 / 接受 / 转移语义

论文在 `NCS` symbolic model 上定义 predecessor：

$$
\mathrm{pre}(Z) = \{(x, u) \in \widetilde{X}_q \times U_q \mid \widetilde{F}_q(x, u) \neq \emptyset \land \widetilde{F}_q(x, u) \subseteq p_{\widetilde{X}_q}(Z)\}
$$

上式中的符号逐项解释如下：

1. `$Z \subseteq \widetilde{X}_q \times U_q$` 是 state-input pairs 的集合。
2. `$p_{\widetilde{X}_q}(Z)$` 是把 `$Z$` 投影回状态空间后的集合。
3. `$\mathrm{pre}(Z)$` 表示存在某控制输入能把所有后继都留在目标投影内的状态-输入对。
4. 论文强调该算子与 fixed-point routines 一起，通过 `BDD` operations 实现。

工具原生支持的规格包括安全、可达、持久和复发，论文把它们写成：

$$
\Box \, jS,\qquad \Diamond \, jT,\qquad \Diamond \Box \, jS,\qquad \Box \Diamond \, jT
$$

上式中的符号逐项解释如下：

1. `$jS$` 和 `$jT$` 分别是安全集和目标集谓词。
2. `$\Box$` 表示 always，`$\Diamond$` 表示 eventually。
3. 四类规格分别对应 safety、reachability、persistence、recurrence。

### 语义边界

1. `SENSE` 的强项是“已抽象好的 plant + bounded network imperfections”，不是从连续 plant 直接一键得到全部语义。
2. 当前理论下，为了能把综合控制器真正下放到 concrete NCS，论文要求 delayed channels 采用 prolonged-delay setting，且 plant symbolic model 通常需满足 determinism 等前提。
3. 工具原生支持的时序目标是 safety/reachability/persistence/recurrence 这几类，不是任意一般 `LTL`。
4. `BDD` 表示虽然节省内存，但状态扩张后复杂度依然可能很高。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| system 骨架 | `$S = (X, X_0, U, F)$` | 统一表示 plant 和其抽象。 |
| plant symbolic model | `$S_q(S) = (X_q, X_{q,0}, U_q, F_q)$` | `SENSE` 的基础输入对象。 |
| NCS expansion | `$\widetilde{S}_q(S) = L(S_q(S), N^{sc}_{min}, N^{sc}_{max}, N^{ca}_{min}, N^{ca}_{max})$` | 论文最核心的网络环境扩展算子。 |
| predecessor | `$\mathrm{pre}(Z) = \{(x,u)\mid \widetilde{F}_q(x,u)\subseteq p_{\widetilde{X}_q}(Z)\}$` | fixed-point synthesis 的核心算子。 |
| 原生支持规格 | `$\Box jS,\ \Diamond jT,\ \Diamond \Box jS,\ \Box \Diamond jT$` | safety/reachability/persistence/recurrence 四类目标。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 状态里同时编码 plant 抽象状态、网络包和 delay counters。 |
| 事件 / 触发 | 中等支持 | 主体仍是 sampled control inputs，而不是协议事件脚本。 |
| 守卫 / 数据 | 很强 | 量化误差、延迟界、丢包与安全/目标集都进入符号条件。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 网络双通道和 packet evolution 带来明显时序同步语义。 |
| 时间约束 | 很强 | delay bounds、sampling periods、prolonged delays 是主轴。 |
| 连续动态 / 随机性 | 很强 | 底层仍锚定在连续 plant symbolic model。 |
| 可执行 / 可验证性 | 很强 | synthesis、simulation、BDD inspection、code generation 都已工程化。 |

### 形式化问题与性质

1. `SENSE` 的关键价值在于把网络非理想因素前移进控制综合，而不是后补鲁棒性。
2. 它展示了 `BDD` 在控制抽象与 controller encoding 上的双重作用。
3. 对文库而言，它是 `SCOTS` 之后非常明确的 NCS tooling 锚点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 来自 `SCOTS` 的 plant symbolic model BDD file；
2. sensor/controller 和 controller/actuator 的 delay bounds；
3. 安全集/目标集的 BDD files；
4. fixed-point specification choice；
5. helper tools 的分析或部署选项。

### 机器可处理承载方式

机器可处理承载方式包括：

1. plant symbolic model BDD；
2. expanded NCS transition relation BDD；
3. synthesized controller BDD；
4. `MATLAB` 和 `OMNeT++` interfaces；
5. `C/C++`、`VHDL/Verilog` generated code。

### 交换与互操作

1. `SENSE` 直接消费 `SCOTS` 产生的 plant symbolic model。
2. helper tool `bdd2fsm` 可导出 FSM-like data format，便于图可视化。
3. controller 既可走软件实现，也可走硬件 RTL 路线。

## 配套基础设施

- 建模/编辑工具：主体不是 GUI 建模器，而是 symbolic-model engine、fixed-point engine 与 helper tools。
- 解析/交换/元模型支持：BDD files、delay-bound configuration、`bddDump`、`bdd2fsm` 等工具。
- 仿真/执行支持：`MATLAB` closed-loop simulation、`OMNeT++` realistic network simulation。
- 验证/分析支持：BDD-based `pre` operation、controller synthesis、coverage visualization、transition exploration。
- 代码生成/转换支持：`bdd2implement` 自动生成 `C/C++` 或 `VHDL/Verilog` 实现。
- 标准化或社区生态：`SCOTS`、`CUDD`、`MATLAB`、`OMNeT++` 和 SENSE helper-tool suite 共同构成生态。

## 适用场景与需求前提

### 适用场景

适合 networked control systems、远程控制机器人、带通信不可靠性的 CPS，以及需要把网络延迟/丢包显式纳入合成的场景。

### 需求前提

1. 需要先获得 plant 的 symbolic model。
2. 网络延迟和丢包等非理想因素需有有界假设。
3. 安全集、目标集和控制规格需能落成工具支持的谓词形式。
4. 若要 refinement 到 concrete NCS，需满足论文当前理论中的 prolonged-delay 和 determinism 等前提。

### 不适用或高成本场景

若系统还没有可用的 plant abstraction，或网络语义远超 bounded-delay/dropout 模型，`SENSE` 的现有实现就不够直接。

## 与相邻形式主义的关系

相对 [scots-a-tool-for-the-synthesis-of-symbolic-controllers/desc.md](../scots-a-tool-for-the-synthesis-of-symbolic-controllers/desc.md)，`SCOTS` 关注 plant symbolic abstraction，而 `SENSE` 继续把网络非理想因素并入控制综合；相对 [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md) 与 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)，这些工作偏 timed-automata symbolic backend，`SENSE` 则面向连续 plant 的 network-aware control abstraction；相对 [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md)，后者偏 reachability verification，`SENSE` 更强调 controller synthesis 和 deployment。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明对 CPS 来说，“状态机/抽象模型生成”不能忽视网络传输语义。
2. 若未来研究考虑 distributed sensing/control，`SENSE` 是非常直接的后端锚点。
3. `BDD`-based controller encoding 与自动代码生成也为“生成-验证-部署”闭环提供了现成路径。

### 作为目标形式主义还是中间表示

更像部署前后端之间的高价值基础设施，而不是需求侧目标语言。

### 对需求到模型生成的启发

1. 若需求里显式包含通信延迟、丢包和采样约束，后端就不能只生成理想控制器。
2. 目标集/安全集谓词和网络参数本身应被纳入结构化需求输入。
3. 从 plant symbolic model 到 network-aware controller 的链路说明，中间表示最好保留 geometry/network meta-data。

### 现实限制

当前理论对 refinement 和 delay setting 仍有前提；因此它更适合研究和特定工程条件下的高可信控制，而不是所有网络控制问题的通用框架。

## 重要的相关工作

### 奠基或前身工作

1. `SCOTS`：plant symbolic model 的主要来源。
2. symbolic models of NCS / `FRR` theory：论文明确依赖的理论基础。

### 同类型或同家族工作

1. [scots-a-tool-for-the-synthesis-of-symbolic-controllers/desc.md](../scots-a-tool-for-the-synthesis-of-symbolic-controllers/desc.md)
2. [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

1. `CUDD`：BDD 管理核心。
2. `MATLAB` / `OMNeT++`：分析和仿真接口。
3. `bdd2implement`、`bdd2fsm`、`bddDump`、`contCoverage`、`sysExplorer`：论文列出的 helper-tool suite。

### 与本研究关系最紧的工作

1. [scots-a-tool-for-the-synthesis-of-symbolic-controllers/desc.md](../scots-a-tool-for-the-synthesis-of-symbolic-controllers/desc.md)
2. [hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md](../hylaa-a-tool-for-computing-simulation-equivalent-reachability-for-linear-systems/desc.md)

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`networked control systems / symbolic models / BDD-based controller synthesis / SENSE`
- 论文角色：BDD-based symbolic-abstraction and controller-synthesis framework for networked control systems
- 核心功能：在 plant symbolic model 上显式加入网络非理想因素，并综合满足安全/可达/持久/复发规格的控制器
- 关键特性：`L` operator、BDD expansion、fixed-point synthesis、`MATLAB/OMNeT++` simulation、code generation
- 构造方式：plant symbolic model + delay bounds -> expanded NCS model -> fixed-point controller -> BDD/code outputs
- 基础设施：`SCOTS`、`CUDD`、BDD files、helper tools、simulation interfaces
- 适用场景：带延迟/丢包/量化误差的网络化控制系统
- 归类理由：论文主体是 network-aware symbolic-control 工具链与部署辅助设施，而不是单一算法或模型本体。
