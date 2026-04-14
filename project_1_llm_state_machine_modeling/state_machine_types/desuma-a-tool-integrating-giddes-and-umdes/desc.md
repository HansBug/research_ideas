# DESUMA：集成 GIDDES 与 UMDES 的工具 / DESUMA: A Tool Integrating GIDDES and UMDES

## 基本信息

- 标题：DESUMA: A Tool Integrating GIDDES and UMDES
- 中文标题：DESUMA：集成 GIDDES 与 UMDES 的工具
- 作者：L. Ricker，S. Lafortune，S. Genc
- 发表：*2006 8th International Workshop on Discrete Event Systems*，pp. 392-393，2006
- DOI：`10.1109/WODES.2006.382402`
- 链接：https://doi.org/10.1109/WODES.2006.382402
- 形式主义：`finite-state automata / DESUMA / UMDES / GIDDES`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：DES finite-state automata graphical/control-diagnosis toolchain
- 工具/实现获取方式：原文明确说明 `DESUMA` 公开可下载，并在参考文献中给出 `UMDES-LIB` 工具箱入口 `http://www.eecs.umich.edu/umdes/toolboxes.html`。
- 标准/格式获取方式：原文说明 `DESUMA` 可打开和保存 `UMDES` `.fsm` 文件，并可把图形视图导出为 `PNG`、`JPEG`、`GIF`、`PS`、`PS2` 与 `XFIG`。

## 简报

这篇短文的价值在于把离散事件系统领域已有的 `UMDES` 命令行算法库和 `GIDDES` 图形界面前端合成一个更易用的 `DESUMA` 工具。它不是提出新的状态机语义，而是补齐 finite-state automata 在 supervisory control、diagnosis、composition 和教育可视化中的工具承载。

- 形式主义定位：面向 DES 的有限状态自动机工具链与图形化基础设施。
- 构造方式简述：用户通过 `GIDDES` 风格 GUI 创建或打开 `.fsm` 自动机，再从菜单调用 `UMDES` 的 C 例程完成控制、诊断和 FSA 操作。
- 基础设施与场景简述：依托 `UMDES`、`GIDDES`、Java 前端、C 后端、`Grappa/GraphViz` 布局和 `MVC` 架构，服务 DES supervisory control、diagnosis 和小规模 FSA 可视化教学。

```text
DES/FSA model -> DESUMA GUI -> UMDES C routines -> generated/analyzed automata -> UMDES .fsm or graphics export
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UMDES`：用于 DES finite-state automata 的 C 例程库。
2. `GIDDES`：用于可视化 DES 操作的 Java 图形前端。
3. `DESUMA`：把 `GIDDES` 前端和 `UMDES` 后端集成后的工具。
4. `UMDES` `.fsm` 文件：工具输入、输出和保存自动机的主要承载格式。
5. diagnosis automata、supervisory control operations 与 FSA manipulation / composition routines。

### 核心抽象

论文没有重新给出 DES 自动机的完整数学定义，但它明确说明 `UMDES` 和 `DESUMA` 的对象是 finite-state automata。可按 DES/FSA 工具链的保守骨架写成：

$$
G = (Q,\Sigma,\delta,q_0,Q_m)
$$

上式中的符号逐项解释如下：

1. `$G$` 是 `DESUMA/UMDES` 处理的一个 FSA plant、specification、diagnoser 或派生自动机。
2. `$Q$` 是有限状态集合。
3. `$\Sigma$` 是离散事件集合。
4. `$\delta$` 是事件触发的状态转移函数或关系。
5. `$q_0$` 是初始状态。
6. `$Q_m$` 是 marked states 集合，用于 DES 中的非阻塞和标记语言分析。
7. 该元组是根据原文“DES modeled by finite-state automata”和 `UMDES` 操作对象做的保守整理，不是原文逐字给出的新定义。

对 `DESUMA` 的软件集成可抽象为：

$$
D_{\mathrm{DESUMA}} = (F_{\mathrm{fsm}},V_{\mathrm{GUI}},R_{\mathrm{UMDES}},E_{\mathrm{export}})
$$

上式中的符号逐项解释如下：

1. `$F_{\mathrm{fsm}}$` 是 `UMDES` `.fsm` 文件输入输出。
2. `$V_{\mathrm{GUI}}$` 是 `GIDDES` 风格的图形编辑和可视化界面。
3. `$R_{\mathrm{UMDES}}$` 是菜单调用到的 `UMDES` C 例程集合。
4. `$E_{\mathrm{export}}$` 是图形导出格式集合。
5. 该式用于描述工具链承载结构，不表示新的自动机理论模型。

### 一个最小例子与通俗解释

一个最小 DESUMA 使用场景可以这样理解：

1. 用户建立一个两状态 FSA：`Idle` 和 `Run`。
2. 事件 `start` 触发 `Idle -> Run`，事件 `stop` 触发 `Run -> Idle`。
3. 用户在 `DESUMA` 中画出该自动机，并保存成 `UMDES` `.fsm` 文件。
4. 需要做诊断或监督控制分析时，用户从菜单选择对应 `UMDES` 例程，工具把当前自动机传给 C 后端并把输出再显示为图。

通俗地说，`DESUMA` 像是给原来命令行取向的 DES 自动机算法库加上一个图形工作台。它让小规模 plant/specification/diagnoser 的创建、查看和操作更顺手，但大状态空间问题仍然更适合回到 `UMDES` 命令行后端。

### 运行 / 接受 / 转移语义

FSA 层的转移语义可按工具对象保守整理为：

$$
q \xrightarrow{\sigma}_G q' \iff q' \in \delta(q,\sigma)
$$

上式中的符号逐项解释如下：

1. `$q$` 与 `$q'$` 是 FSA 的当前状态和目标状态。
2. `$\sigma$` 是一个 DES 事件。
3. `$\xrightarrow{\sigma}_G$` 表示在自动机 `$G$` 中沿事件 `$\sigma$` 发生一步转移。
4. 若 `$\delta$` 是确定函数，则 `$q'=\delta(q,\sigma)$`；若按关系处理，则 `$q'$` 属于后继集合。

在工具链层，原文描述的执行路径可写成：

$$
G' = R_{\mathrm{UMDES}}(G,p)
$$

上式中的符号逐项解释如下：

1. `$G$` 是当前 `DESUMA` 会话中的输入 FSA。
2. `$p$` 是某个 `UMDES` 例程需要的附加参数。
3. `$R_{\mathrm{UMDES}}$` 是被菜单或弹窗触发的后端例程。
4. `$G'$` 是分析、组合、诊断或控制操作后得到的输出自动机或结果。

### 语义边界

1. 论文主体是工具集成，不是 DES supervisory control 理论的新证明。
2. `DESUMA` 适合小状态空间图形可视化；原文明确说大状态空间通常更适合直接用 `UMDES` 命令行接口。
3. 工具对象主要是离散 FSA，不覆盖 timed、hybrid 或概率扩展。
4. 插件化在本文中是未来版本方向，而不是已完整稳定的公开机制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| FSA 骨架 | `$G = (Q,\Sigma,\delta,q_0,Q_m)$` | `DESUMA/UMDES` 处理的是 DES finite-state automata。 |
| 单步转移 | `$q \xrightarrow{\sigma}_G q' \iff q' \in \delta(q,\sigma)$` | 图形上的边和 `.fsm` 中的转移都可被后端消费。 |
| 后端调用 | `$G' = R_{\mathrm{UMDES}}(G,p)$` | GUI 菜单实质上调用 `UMDES` 例程并返回分析结果。 |
| 可视化边界 | `$\lvert Q\rvert$` 过大时 GUI 成本升高 | 原文明确指出大状态空间常回到命令行更合适。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心对象就是有限状态自动机。 |
| 事件 / 触发 | 很强 | DES 事件和 FSA 转移是 `UMDES` 操作对象。 |
| 守卫 / 数据 | 弱支持 | 论文未涉及 rich data guards，重点是 FSA/DES。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 间接支持 | 可通过 DES composition routines 处理组合，但论文主线是工具集成。 |
| 时间约束 | 不支持 | 不涉及 timed automata。 |
| 连续动态 / 随机性 | 弱支持 | 原文提到 logical and stochastic diagnoser automata，但 `DESUMA` 主线不是随机语义本体。 |
| 可执行 / 可验证性 | 强 | `UMDES` 例程覆盖 control、diagnosis、manipulation 和 composition。 |

### 形式化问题与性质

1. `DESUMA` 的核心贡献是把 “FSA file + command-line DES algorithms” 变成 “FSA GUI + menu-driven backend routines”。
2. 对本文库而言，它补的是 DES/FSA 工具链和文件承载证据，而不是新形式主义节点。
3. 它尤其适合作为 `libFAUDES`、`ESCET` 等后续 DES infrastructure 的早期可视化对照项。

## 构造方式与承载格式

### 建模入口

原文给出的建模入口包括：

1. 打开已有 `UMDES` `.fsm` 文件。
2. 在 `DESUMA` 图形界面中新建自动机。
3. 通过菜单选择 `UMDES` 后端 routines。
4. 在弹窗中补充特定例程所需的附加参数。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UMDES` `.fsm` 输入输出文件。
2. 调用 C executable library functions 的 Java glue code。
3. `GIDDES` 的 front-end / back-end 分离架构。
4. `MVC` 中的 model、view、controller 三层。

### 交换与互操作

互操作重点在后端复用：

1. `DESUMA` 用 Java GUI 触发 C 后端例程。
2. `UMDES` 输入输出文件通过 `GIDDES` 菜单系统传递。
3. 图形显示可导出为多种图片和绘图格式，用于报告或教学材料。

## 配套基础设施

- 建模/编辑工具：`DESUMA` 图形环境，继承 `GIDDES` 风格界面。
- 解析/交换/元模型支持：`UMDES` `.fsm` 文件，原文未说明更通用元模型。
- 仿真/执行支持：主要是 FSA 可视化、编辑和后端例程调用，非运行时执行平台。
- 验证/分析支持：`UMDES` 提供 supervisory control、diagnosis、FSA manipulation 和 composition routines。
- 代码生成/转换支持：不主打控制代码生成，重点是分析和自动机操作。
- 标准化或社区生态：依托 `UMDES`、`GIDDES`、`Grappa/GraphViz` 和 DES supervisory control / diagnosis 社区。

## 适用场景与需求前提

### 适用场景

适合 DES/FSA 的教学、交互式建模、控制/诊断算法演示和小规模 plant/specification 的可视化分析。

### 需求前提

1. 需求能整理成有限状态自动机和离散事件集合。
2. 用户需要图形编辑和结果可视化，而不只是批量命令行处理。
3. 后端分析任务属于 `UMDES` 已支持的 control、diagnosis、composition 或 manipulation 范围。
4. 状态空间不应大到让 GUI 布局和内存开销成为主要瓶颈。

### 不适用或高成本场景

如果系统有大量状态、复杂数据守卫、dense-time clocks 或连续动力学，`DESUMA` 本身不是直接承载；大规模 DES 算法任务也更适合直接走 `UMDES` 命令行。

## 与相邻形式主义的关系

相对 [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)，`DESUMA` 更偏早期 GUI + `UMDES` 集成，而 `libFAUDES` 更偏可编程 `C++` DES 算法库；相对 [overview-and-performance-evaluation-of-supervisory-controller-synthesis-with-eclipse-escet-v40/desc.md](../overview-and-performance-evaluation-of-supervisory-controller-synthesis-with-eclipse-escet-v40/desc.md)，`ESCET/CIF` 是后续更完整的工业级 supervisory-control synthesis 平台；相对 [an-educational-toolbox-on-supervisory-control-theory-using-matlab-simulink-stateflow/desc.md](../an-educational-toolbox-on-supervisory-control-theory-using-matlab-simulink-stateflow/desc.md)，两者都强调 DES 教学可视化，但后者落在 `MATLAB/Simulink/Stateflow` 生态。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒 `project_1`：LLM 生成的 DES/FSA 模型若要被工程人员使用，文件格式、图形编辑和后端算法调用同样重要。
2. `DESUMA` 的 front-end / back-end 分离适合作为“生成模型 -> 可视化核对 -> 后端分析”的早期工具链样例。
3. 对模型修复闭环而言，图形化地查看后端例程输出的 automata 很适合做人工校验入口。

### 作为目标形式主义还是中间表示

更适合作为 DES/FSA 基础设施和可视化工具证据，而不是新的目标状态机形式主义。

## 重要的相关工作

1. [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)：DES `C++` 算法库与控制工程后端。
2. [overview-and-performance-evaluation-of-supervisory-controller-synthesis-with-eclipse-escet-v40/desc.md](../overview-and-performance-evaluation-of-supervisory-controller-synthesis-with-eclipse-escet-v40/desc.md)：`CIF/ESCET` 监督控制综合平台。
3. [an-educational-toolbox-on-supervisory-control-theory-using-matlab-simulink-stateflow/desc.md](../an-educational-toolbox-on-supervisory-control-theory-using-matlab-simulink-stateflow/desc.md)：面向教学的 supervisory-control 工具箱对照项。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`finite-state automata / DESUMA / UMDES / GIDDES`
- 论文角色：DES finite-state automata graphical/control-diagnosis toolchain
- 归类理由：论文主体是把 DES finite-state automata 的算法后端、图形前端和文件格式整合成工具基础设施，典型属于 `🏗️` 条目。
