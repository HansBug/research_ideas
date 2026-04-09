# 使用层次状态机工具包编写丰富交互 / Programming Rich Interactions using the Hierarchical State Machine Toolkit

## 基本信息

- 标题：Programming Rich Interactions using the Hierarchical State Machine Toolkit
- 中文标题：使用层次状态机工具包编写丰富交互
- 作者：Renaud Blanch，Michel Beaudouin-Lafon
- 发表：*Proceedings of the Working Conference on Advanced Visual Interfaces*，pp. 51-58，2006
- DOI：`10.1145/1133265.1133275`
- 链接：https://doi.org/10.1145/1133265.1133275
- 形式主义：`HsmTk / hierarchical state machines / SVG interaction toolkit`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`SVG` 富交互控制工具包与 `HSM` 嵌入式语言
- 工具/实现获取方式：原文明确介绍 `HsmTk` 作为基于 `C++` 的 toolkit，用来把 `SVG` 对象、事件和层次状态机绑定在一起；当前提取文本未见稳定公开下载地址。
- 标准/格式获取方式：承载方式是嵌入 `C++` 的 `hsm Name { ... }` 语法、输入/变量声明、带 guard/code/broadcast/target 的 transition 规则，以及与 `SVG DOM` 绑定的运行时对象。

## 简报

这篇论文的价值不在“提出新的 Statecharts 理论”，而在于把层次状态机真正做成了可编写、可执行、可和界面对象绑定的交互控制工具包。`HsmTk` 既像一个小型 DSL，又像一个 runtime：模型直接嵌在 `C++` 中，事件来自 `SVG` 组件，transition 上能写代码、广播事件、history 跳转和 timer。

- 形式主义定位：面向 rich interaction 的层次状态机 toolkit 与宿主语言内嵌 DSL。
- 构造方式简述：用 `hsm`、`var`、`in`、`enter/leave` 和 transition rules 定义控制结构，再把它们附着到 `SVG` 图形对象与交互输入上。
- 基础设施与场景简述：依托 `C++`、`SVG`、预定义事件、timer transitions 和 target-resolution runtime，服务 post-WIMP interaction、widget behavior 和图形交互原型。

```text
交互需求 -> HsmTk 层次状态机 + C++ 动作 -> SVG 事件与对象绑定 -> toolkit runtime -> 富交互执行
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. `HSM` 本体；
2. sub-HSM hierarchy；
3. variables 和 inputs；
4. transitions；
5. `enter/leave/init/requirement` 构造；
6. pre-defined events、explicit invocation 和 timer transitions；
7. 与 `SVG` 图形对象绑定的 interactive components。

### 核心抽象

根据原文的语法说明，可把一个 `HsmTk` 状态机保守整理为：

$$
H = (N, V, I, Init, Enter, Leave, Sub, R)
$$

上式中的符号逐项解释如下：

1. `$N$` 是当前 `HSM` 的名字。
2. `$V$` 是变量集合。
3. `$I$` 是 inputs 集合。
4. `$Init$` 是初始子状态选择规则。
5. `$Enter$` 与 `$Leave$` 分别是进入和离开该 `HSM` 时执行的动作。
6. `$Sub$` 是直接子 `HSM` 集合。
7. `$R$` 是 transition rules 集合。

单条 transition rule 可保守写成：

$$
r = (src, \iota, ev, g, c, b, tgt, mode)
$$

上式中的符号逐项解释如下：

1. `$src$` 是 source `HSM`。
2. `$\iota$` 是可选 input sender。
3. `$ev$` 是触发事件类型。
4. `$g$` 是 guard condition。
5. `$c$` 是在离开 source 前执行的代码块。
6. `$b$` 是 broadcast section。
7. `$tgt$` 是目标 `HSM`。
8. `$mode$` 表示普通跳转、history 跳转或事件传播等特殊模式。

### 一个最小例子与通俗解释

论文里的按钮例子已经非常接近最小可用说明：

1. `Button` 下有 `Disarmed` 和 `Armed` 两层结构。
2. `Disarmed::OutUp` 在鼠标进入按钮时迁移到 `InUp`。
3. `InUp` 收到 `press()` 后跳到 `Armed::InDown`。
4. `Armed::InDown` 收到 `release()` 时执行 `doIt()`，再回到 `Disarmed::InUp`。

通俗地说，`HsmTk` 像“把界面控件的交互逻辑写成可执行层次状态图的库”。普通 GUI 回调往往散落在多个事件处理器里；这里则把“在哪个交互模式、收到什么事件、应该怎么换模式”全都压回一棵 `HSM`。

### 运行 / 接受 / 转移语义

论文把 target resolution 写成三段式过程，可保守压成：

$$
\mathrm{fire}(r, s) = \mathrm{enter}(\mathrm{resolve}(\mathrm{leave}(s, src(r)), tgt(r)))
$$

上式中的符号逐项解释如下：

1. `$r$` 是被触发的 transition rule。
2. `$s$` 是当前 active-state configuration。
3. `$\mathrm{leave}(s, src(r))$` 表示从最内层 active `HSM` 向上离开到 source 所在层级。
4. `$\mathrm{resolve}(\cdot, tgt(r))$` 表示找到 source 与 target 的共同祖先，再沿目标分支向下。
5. `$\mathrm{enter}(\cdot)$` 表示进入目标 `HSM` 及其初始或 history 子状态。

若使用 history transition，则最终进入的不是默认初始子状态，而是上次活跃的子状态，可保守写成：

$$
\mathrm{enter}_{hist}(h) = \mathrm{lastActive}(h)
$$

上式中的符号逐项解释如下：

1. `$h$` 是采用 history 进入的目标 `HSM`。
2. `$\mathrm{lastActive}(h)$` 是该 `HSM` 上次活跃的直接子状态。

### 语义边界

1. `HsmTk` 重点是可执行 rich-interaction 控制，不是保判定性的理论模型。
2. 它主要依赖宿主 `C++` 和 toolkit runtime，不是独立中立交换标准。
3. 层次很强，但不是通用并发状态图语言。
4. timer、event propagation 和 requirements 都是工程型执行语义扩展。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `HSM` 骨架 | `$H = (N, V, I, Init, Enter, Leave, Sub, R)$` | 一个 `HSM` 由变量、输入、子状态机和规则组成。 |
| 规则骨架 | `$r = (src, \iota, ev, g, c, b, tgt, mode)$` | transition 同时可带 guard、code、broadcast 和 target。 |
| 触发语义 | `$\mathrm{fire}(r, s) = \mathrm{enter}(\mathrm{resolve}(\mathrm{leave}(s, src(r)), tgt(r)))$` | target resolution 由 leave、resolve、enter 三步组成。 |
| history 进入 | `$\mathrm{enter}_{hist}(h) = \mathrm{lastActive}(h)$` | history transition 会恢复上次活跃子状态。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 交互模式直接写成嵌套 `HSM`。 |
| 事件 / 触发 | 很强 | `enter/leave/press/release` 及自定义事件都是一等输入。 |
| 守卫 / 数据 | 强 | transition 可带任意作用域内可计算的布尔条件和变量。 |
| 层次 | 很强 | 这是工具包主骨架。 |
| 并发 / 同步 | 弱支持 | 论文主线是 hierarchy，不是 orthogonal concurrency。 |
| 时间约束 | 部分支持 | 支持 timer-triggered transitions。 |
| 连续动态 / 随机性 | 不支持 | 纯离散交互逻辑。 |
| 可执行 / 可验证性 | 很强 | 直接嵌入 `C++` 并连接实际 `SVG` interaction runtime。 |

### 形式化问题与性质

1. `HsmTk` 的主要贡献是把层次状态机变成可直接绑定图形对象和事件的执行载体。
2. 它用 target-resolution、history、requirements 和 event propagation 固定了工程语义。
3. 对本文库而言，它补的是 “HSM as UI/interaction runtime” 这条基础设施线，而不是新的理论母线。

## 构造方式与承载格式

### 建模入口

1. 先定义顶层 `hsm Name { ... }`。
2. 在每一层声明 `var`、`in`、`init`、`enter` 和 `leave`。
3. 再定义 sub-HSM hierarchy 和 transition rules。
4. 最后把 `HSM` 绑定到 `SVG` 对象或其他交互组件。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 嵌入 `C++` 的 `HSM` 语法；
2. event-triggered transition rules；
3. history / requirement / timer 语义；
4. toolkit runtime 中的 target-resolution 执行逻辑。

### 交换与互操作

`HsmTk` 不是中立交换格式，但其互操作点很明确：

1. 上接一般 `HSM/Statecharts` 语义；
2. 下接 `SVG DOM` 与交互事件；
3. 中间由宿主语言 `C++` 承担动作代码和数据操作。

## 配套基础设施

- 建模/编辑工具：`HsmTk` toolkit 本身，原文用其编写交互组件。
- 解析/交换/元模型支持：主要是嵌入 `C++` 的解析与对象绑定，不是外部元模型标准。
- 仿真/执行支持：直接在 toolkit runtime 中执行，并与 `SVG` 对象联动。
- 验证/分析支持：论文主线不是 formal verification backend。
- 代码生成/转换支持：不主打 code generation，而是把状态机直接嵌进宿主程序。
- 标准化或社区生态：研究型 toolkit，生态更多依托 `C++` 与 `SVG`，不是标准组织推动的语言。

## 适用场景与需求前提

### 适用场景

适合富交互界面、post-WIMP widgets、图形化控件和需要精确模式切换的交互对象。

### 需求前提

1. 交互逻辑可明显分解成有限模式和事件触发。
2. 团队接受用 `C++` 嵌入状态机，而不是维护外部独立模型文件。
3. 界面对象和事件源可稳定绑定到 `HsmTk` runtime。
4. 需求更关注交互模式切换，而不是复杂并发或连续控制。

### 不适用或高成本场景

若目标是中立交换标准、跨工具模型互操作、重型验证后端或复杂并发控制，`HsmTk` 的宿主语言嵌入式设计会带来较高耦合。

## 与相邻形式主义的关系

相对一般 `Statecharts/HSM` 理论条目，`HsmTk` 更强调执行载体与交互 runtime；相对 `SCXML`，它不是独立 XML 标准，而是 `C++` 内嵌 DSL；相对后来的 `Sismic` 或 `Repast Simphony Statecharts`，它更早地展示了“层次状态机 + runtime + real UI objects”这条工具化路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机语言不一定非得是独立文件格式，也可以是宿主语言内嵌 DSL。
2. `HsmTk` 把 enter/leave/history/requirements 这些工程语义做得很具体，适合作为“LLM 生成可执行状态机代码骨架”的参考。
3. 它也提醒文库：某些重要状态机条目虽不单列为新理论分支，但在工具生态上足以形成稳定支线。

### 作为目标形式主义还是中间表示

更适合作为 UI / interaction 方向的目标执行载体和基础设施证据，而不是通用中间表示。

### 对自动建模的启发

若未来要自动生成交互式控制逻辑，`HsmTk` 这类“状态机 + 宿主语言动作 + runtime 绑定”的结构，比只输出平面状态图更接近真实落地形态。

## 重要的相关工作

- `Statecharts`
- `SCXML`
- `Repast Simphony Statecharts`
- `Sismic`

## 文献分类总结

- 形式主义：`HsmTk / hierarchical state machines / SVG interaction toolkit`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 关键词：层次状态机、rich interaction、`SVG`、`C++` 嵌入式 DSL、runtime
