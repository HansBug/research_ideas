# 符号化模块化监督控制器的 PLC 实现 / PLC Implementation of Symbolic, Modular Supervisory Controllers

## 基本信息

- 标题：PLC Implementation of Symbolic, Modular Supervisory Controllers
- 中文标题：符号化模块化监督控制器的 PLC 实现
- 作者：Laurin Prenzel，Julien Provost
- 发表：*IFAC-PapersOnLine*，51(7):304-309，2018
- DOI：`10.1016/j.ifacol.2018.06.317`
- 链接：https://doi.org/10.1016/j.ifacol.2018.06.317
- 形式主义：`Symbolic Modular Supervisory Controllers / Supremica -> PLC Structured Text`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：supervisory-control code-generation bridge / PLC deployment framework
- 工具/实现获取方式：原文明确说明建模与综合在 `Supremica` 中完成，自动代码生成可执行程序发布在作者课题组站点 `www.ses.mw.tum.de`。
- 标准/格式获取方式：承载方式是 symbolic modular supervisor、`IEC 61131-3 Structured Text`、TwinCAT Soft PLC 与 didactic platform I/O；原文未给中立交换标准。

## 简报

这篇论文补的是监督控制线里非常缺的一环：从“综合出来的 supervisor”到“PLC 上真的能跑的控制逻辑”。它不是再讲一遍监督控制理论，而是把 `Supremica` 生成的 symbolic modular supervisor 翻译成 `IEC 61131-3 Structured Text`，并明确处理 event-to-signal、interleave、delay、choice、同步和 state-space explosion 等真正卡工业落地的问题。

- 形式主义定位：`SCT/Supremica` supervisor 的 PLC 实施桥，而不是新的 DES 语言。
- 构造方式简述：先在 `Supremica` 中建立 plant/specification models 并综合 symbolic modular supervisor，再生成 `Structured Text`，在 `MAIN/reset/localcontroller/virtualsensor/synthcontrol` 结构中执行。
- 基础设施与场景简述：依托 `Supremica`、`IEC 61131-3`、TwinCAT Soft PLC、didactic platform 和 local-controller / virtual-sensor 机制，服务模块化离散事件控制的教学与工业迁移。

```text
plant/spec models in Supremica -> symbolic modular supervisor -> Structured Text code generation -> Soft PLC cycle execution -> physical plant control
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Supremica` 中的 plant 与 specification models。
2. controllable / uncontrollable events。
3. symbolic modular supervisor。
4. `Structured Text` 中的 states、transitions、event edges 与 guards。
5. PLC scan cycle 下的 uncontrollable / controllable transition loops。

### 核心抽象

结合论文对生成代码结构的描述，可把部署级 supervisor 保守整理为：

$$
\mathcal{C} = (\Sigma_u, \Sigma_c, X, T, \Gamma)
$$

上式中的符号逐项解释如下：

1. `\Sigma_u` 是 uncontrollable events 集合。
2. `\Sigma_c` 是 controllable events 集合。
3. `X` 是编码 active states 的布尔变量集合。
4. `T` 是编码本周期触发 transitions 的布尔变量集合。
5. `\Gamma` 是 guard 集合，其中既包含 model synchronization guards，也包含 symbolic supervisor guards。
6. 这组元组是依据论文 `states/transitions/events/guards` 的代码结构做的保守整理。

论文明确说明某个 event 是否可执行，取决于同步守卫与 supervisor 守卫，可保守写成：

$$
enabled(e, X) \iff sync_e(X) \land sup_e(X)
$$

上式中的符号逐项解释如下：

1. `e` 是当前被评估的事件。
2. `X` 是当前 active-state set。
3. `sync_e(X)` 表示该事件在各 modular models 当前状态下同步一致。
4. `sup_e(X)` 表示 symbolic supervisor 没有禁用该事件。

论文给出的 `Listing 1` 直接展示了生成代码的状态更新模式：

$$
T_{REls} := X_{off},\quad X_{off} := T_{FEls} \lor (X_{off} \land \neg T_{REls}),\quad X_{on} := T_{REls} \lor (X_{on} \land \neg T_{FEls})
$$

上式中的符号逐项解释如下：

1. `T_{REls}`、`T_{FEls}` 是某两个边沿事件对应的 transition bits。
2. `X_{off}`、`X_{on}` 是 conveyor-belt 小模型中的 state bits。
3. 这些布尔方程把 supervisor state update 直接落成 `Structured Text` 赋值。

### 一个最小例子与通俗解释

论文用 light sensor + conveyor belt 的小例子说明核心思路：

1. 输入信号先被转换成 rising / falling edge events。
2. `Supremica` 综合出的 supervisor 决定某些 controllable actions 当前能不能发。
3. PLC 在一个 scan cycle 中先处理 uncontrollable events，再处理 controllable events。
4. 状态和 transition 都用布尔变量显式维护，因此代码可以直接在 Soft PLC 中运行。

通俗地说，这篇论文干的事，是把“事件驱动 supervisor”翻译成“PLC 每个周期都能算的布尔控制程序”，同时尽量不丢掉监督控制的结构和 permissiveness。

### 运行 / 接受 / 转移语义

论文的运行语义本质上是“scan-cycle 版 supervisor execution”：

1. 先扫描输入，计算边沿事件。
2. 进入 uncontrollable transition loop，检查同步并更新状态。
3. 再进入 controllable transition loop，按静态顺序尝试可控事件。
4. 最后把已选中的 controllable events 转回输出信号。

关键的工程问题包括：

1. event generation。
2. avalanche effect。
3. interleave insensitivity。
4. choice of controllable events。
5. inexact synchronization。

### 语义边界

论文对边界很坦率：

1. supervisor 本体仍然是 event-based，而 PLC 是 signal-based。
2. 多个 controllable events 在一个周期内可连续执行，这对 supervisor 提出更强 delay-insensitivity 要求。
3. interleave sensitivity 在实现中没有被完全消除，而是要求建模者在 plant/specification 模型中预先考虑。
4. 这条路线强依赖 `Supremica` 与 `Structured Text` 生态，不是中立交换层。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 部署级 supervisor 骨架 | `$\mathcal{C} = (\Sigma_u, \Sigma_c, X, T, \Gamma)$` | 代码实现围绕事件、状态位、transition 位与 guards 展开。 |
| 事件可执行条件 | `$enabled(e, X) \iff sync_e(X) \land sup_e(X)$` | 既要满足模型同步，也要满足 supervisor 许可。 |
| 代码级状态更新 | `$T_{REls} := X_{off},\ X_{off} := \cdots,\ X_{on} := \cdots$` | 生成代码直接体现 supervisor 的离散更新逻辑。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | states 和 transitions 被显式编码成布尔变量。 |
| 事件 / 触发 | 很强 | controllable / uncontrollable events 是核心。 |
| 守卫 / 数据 | 强支持 | synchronization guards 与 supervisor guards 共同决定动作可行性。 |
| 层次 | 弱支持 | 主体是模块化 supervisor，不是层次状态机语义。 |
| 并发 / 同步 | 很强 | modular models 的 on-the-fly synchronization 是关键。 |
| 时间约束 | 中等支持 | 主要体现为 PLC cycle、timers 与 virtual sensors，不是 timed automata 语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散事件控制。 |
| 可执行 / 可验证性 | 很强 | 真正落到 Soft PLC 与物理教学平台执行。 |

### 形式化问题与性质

1. 论文真正补的是 supervisory-control 落地时最麻烦的 bridge 问题。
2. symbolic modular supervisor 让“极大状态空间 + 可落地代码”第一次能兼得。
3. local controllers 与 virtual sensors 提供了 supervisor 与低层时序/legacy logic 之间的现实接口。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 在 `Supremica` 中建 plant/specification models。
2. 综合 symbolic modular supervisor。
3. 生成 `Structured Text`。
4. 在 TwinCAT Soft PLC 中执行，并通过 didactic platform 验证。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Supremica` models。
2. symbolic supervisor guards。
3. `IEC 61131-3 Structured Text`。
4. `GVL/POU` 结构化 PLC 程序。

### 交换与互操作

互操作重点在于：

1. `Supremica` 与 PLC 代码生成器之间的桥。
2. 物理 I/O、Soft PLC 与 didactic platform 的连接。
3. localcontroller / virtualsensor 对外部时序逻辑的包容。

## 配套基础设施

- 建模/编辑工具：`Supremica`。
- 解析/交换/元模型支持：symbolic modular supervisor 到 `Structured Text` 的自动代码生成。
- 仿真/执行支持：TwinCAT Soft PLC、didactic platform、remote I/O modules。
- 验证/分析支持：主线在 supervisor 综合前由 `Supremica` 提供；部署后通过 error mode、同步检查和教学平台测试做运行期核对。
- 代码生成/转换支持：`Supremica -> IEC 61131-3 Structured Text` 是论文核心。
- 标准化或社区生态：`IEC 61131-3`、TwinCAT、`Supremica` 与 DES supervisory-control 社区。

## 适用场景与需求前提

### 适用场景

适合离散事件制造系统、模块化产线、机器人单元、教学平台以及需要把 supervisor 真正下放到 PLC 的工业控制场景。

### 需求前提

1. 系统能分解成 plant/specification models。
2. 事件能从信号边沿稳定提取。
3. supervisor 最好本身就考虑 cyclic execution、interleave 和 delay constraints。
4. 团队愿意接受 `Supremica + Structured Text + Soft PLC` 这套技术栈。

### 不适用或高成本场景

若系统严重依赖连续动力学、rich data 或复杂异步软件协议，仅靠 PLC-cycle supervisor code generation 就会显得过窄。

## 与相邻形式主义的关系

相对 [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)，这篇不是再讲 synthesis IDE，而是把 synthesis 结果真正落到 PLC；相对 [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)，两者都强调 supervisory-control toolchain，但本文更聚焦 `Structured Text` 实施；相对 [method-of-analysing-extended-finite-state-machine-specifications/desc.md](../method-of-analysing-extended-finite-state-machine-specifications/desc.md)，这里不是 EFSM 规格方法，而是 supervisor deployment bridge。

## 与本研究的关系

### 对 Project 1 的价值

它说明状态机或离散事件模型若要进入工业控制闭环，最终必须回答“怎么变成 PLC 上的可运行控制逻辑”。

### 作为目标形式主义还是中间表示

更像 `supervisory-control` 线的执行基础设施，而不是新的目标语言。

### 对需求到模型生成的启发

1. 生成 supervisor-friendly 模型时，应及早区分 controllable / uncontrollable events。
2. 运行期 bridge 的难点经常不在综合，而在 event-to-signal、interleave 和 timing assumptions。
3. 如果未来做“生成-验证-修复”闭环，部署端约束也要尽早纳入模型。

### 现实限制

这条路线非常工程化，但也高度绑定具体 PLC 执行语义与 supervisor assumptions。

## 重要的相关工作

1. [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)：symbolic/modular supervisor 的上游 IDE 与综合平台。
2. [cif-3-model-based-engineering-of-supervisory-controllers/desc.md](../cif-3-model-based-engineering-of-supervisory-controllers/desc.md)：另一条 supervisory-control 工程工具链。
3. [method-of-analysing-extended-finite-state-machine-specifications/desc.md](../method-of-analysing-extended-finite-state-machine-specifications/desc.md)：离散事件控制与扩展状态机规格的更早方法学基线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 归类理由：论文主体是 supervisor 到 PLC 的代码生成与执行基础设施，不是新的 DES 形式主义，因此按 `📦/🏗️` 归类更稳妥。
