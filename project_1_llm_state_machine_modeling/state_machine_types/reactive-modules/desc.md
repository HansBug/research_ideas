# 反应式模块 / Reactive Modules

## 基本信息

- 标题：Reactive Modules
- 中文标题：反应式模块
- 作者：Rajeev Alur, Thomas A. Henzinger
- 发表：Formal Methods in System Design, 15(1):7-48, 1999
- DOI：`10.1023/A:1008739929481`
- 链接：https://doi.org/10.1023/A:1008739929481
- 形式主义：Reactive Modules
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：组合建模框架
- 工具/实现获取方式：原文把 `reactive modules` 作为统一建模中间层，明确面向后续验证与抽象操作，但未提供独立下载包；论文给出同步电路、共享内存协议、消息传递协议三类可直接照抄的模块模板。
- 标准/格式获取方式：机器可处理承载是论文中的模块声明、`atom`、`init/update` guarded command 与 `next/hide/trigger` 等操作；原文未给出 XML/JSON 一类开放交换格式。

## 简报

这篇论文的核心价值是把“同步系统”“异步系统”“抽象层切换”“组合验证”收进同一个模块语义里。作者没有再定义一类新的专用图形状态机，而是定义了一种更通用的反应式模块语言：变量按 `private / interface / external` 分层，更新由若干 `atom` 在一个 round 内按依赖次序执行，之后再通过 `parallel composition`、`hiding`、`next` 和 `trigger` 做空间与时间抽象。

- 形式主义定位：统一同步/异步并发系统的模块化状态机式建模框架。
- 构造方式简述：用变量分区、原子更新单元、可观测 trace 语义和模块操作子来定义系统。
- 基础设施与场景简述：天然面向组合验证、assume-guarantee 推理、显式/符号模型检查与抽象建模。

```text
组件变量与交互边界 -> atoms / rounds / trace semantics -> composition / hiding / next -> 验证 / 精化 / 抽象
```

## 形式主义定义与核心对象

### 定义对象

论文要解决的是一个长期分裂的问题：硬件倾向同步模型，协议和共享内存程序倾向异步模型，而真实系统又经常需要在多个时间粒度与抽象层之间切换。`Reactive Modules` 的答案是：

1. 用统一的变量视角替代“只按事件”或“只按共享变量”建模。
2. 用 round 和 subround 统一同步/异步执行。
3. 用显式的模块操作支撑组合、隐藏和时间抽象。

### 核心抽象

单个 `atom` 的核心结构为：

$$
A = (\mathrm{ctr}X_A, \mathrm{read}X_A, \mathrm{wait}X_A, Init_A, Update_A)
$$

上式中的符号逐项解释如下：

1. `\mathrm{ctr}X_A` 是该 `atom` 负责更新的 controlled variables。
2. `\mathrm{read}X_A` 是本轮读取其旧值的 read variables。
3. `\mathrm{wait}X_A` 是必须等到本轮新值可用后才能执行的 awaited variables。
4. `Init_A` 是初始化动作，给控制变量赋初值。
5. `Update_A` 是每个 update round 中的更新动作。

模块本体则写成：

$$
P = (X_P, A_P)
$$

其中：

1. `X_P` 是变量全集，并按 `private / interface / external` 三类划分。
2. `A_P` 是模块中的 `atom` 集合。
3. `A_P` 的 await 依赖闭包必须无环，以保证每轮存在一致执行顺序。

### 一个最小例子与通俗解释

论文里最容易理解的例子其实不是协议，而是同步电路里的 `NOT / AND / Latch`：

1. `Not` 模块把外部输入 `in` 映射成接口输出 `out`。
2. `Latch` 模块一边公开 `out`，一边在私有变量 `state` 里保存上一轮记忆。
3. 一个 round 内，环境先给外部变量赋值，随后各个 `atom` 按等待依赖顺序执行。

通俗地说，`Reactive Modules` 像“把状态机拆成多个会在一轮里顺序接力的更新块”。有些块只看旧值，有些块必须等其他块先算出新值；最后外界只看到接口变量形成的 trace。

### 运行 / 接受 / 转移语义

论文把模块状态空间定义为对变量集 `X_P` 的赋值，随后给出 successor 关系。其 trace 语义可压缩为：

$$
L_P = \{ \hat{s}[\mathrm{obs}X_P] \mid \hat{s} \text{ is a trajectory of } P \}
$$

上式中的符号逐项解释如下：

1. `\hat{s}` 是一个有限状态轨迹。
2. `\mathrm{obs}X_P` 是 `P` 的 observable variables，即接口变量和外部变量。
3. `\hat{s}[\mathrm{obs}X_P]` 表示把整条轨迹投影成外界可见的 observation sequence。
4. `L_P` 是模块的 trace language。

模块实现关系写成：

$$
P \preceq Q \iff \mathrm{obs}(P) \text{ 对 } Q \text{ 至少同样兼容，且 } L_P \subseteq L_Q
$$

这里：

1. `P \preceq Q` 表示 `P` 实现或精化 `Q`。
2. 前半句对应论文中对 interface variables、external variables 与 await dependencies 的兼容约束。
3. `L_P \subseteq L_Q` 表示实现体只保留规范允许的可观测行为。

作者还引入时间抽象算子：

$$
Q = \mathrm{next}_Y(P)
$$

其中：

1. `Y` 是 round marker，也就是决定“何时把若干细粒度 round 压成一个抽象 round”的接口变量集合。
2. `\mathrm{next}_Y` 会把若干连续 round 折叠到第一次让 `Y` 中某个变量发生可观测变化的位置。

### 语义边界

这个框架的边界很清楚：

1. 它是离散 round-based 模型，不直接描述连续动力学。
2. 它强调变量与更新顺序，而不是图形状态图。
3. 它统一同步/异步靠的是抽象和等待依赖，不是把所有系统都强行变成某一种时序假设。

### 关键性质与判定边界

论文最关键的不是单个复杂度定理，而是以下可复用性质：

1. 模块 transition relation 是 serial，因此 trace language 前缀闭合且无死锁。
2. `P \preceq Q` 是 preorder，支持层层实现精化。
3. `parallel composition` 对 trace 语义表现得像交集，能直接支撑组合证明。
4. `hiding`、`next`、`trigger` 都保持组合性，便于分层抽象。
5. 在公平性扩展中，weak/strong fairness 被显式附到 update choices 上，而不是外加口头假设。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 状态由整个变量赋值决定，私有变量可保存局部控制状态。 |
| 事件 / 触发 | 强支持 | 事件可编码为布尔变量翻转，消息握手可在 subround 内建模。 |
| 守卫 / 数据 | 强支持 | `init/update` 动作是带守卫的关系，可直接处理 typed variables。 |
| 层次 | 部分支持 | 不是图形层次状态图，但通过模块组合和抽象形成层次建模。 |
| 并发 / 同步 | 强支持 | 同步、异步、共享内存、消息传递都可作为模块实例编码。 |
| 时间约束 | 部分支持 | 有 round、subround 和 `next/trigger` 抽象，但无显式时钟约束。 |
| 连续动态 / 随机性 | 不支持 | 论文核心只覆盖离散反应式系统。 |
| 可执行 / 可验证性 | 强支持 | 明确面向显式/符号验证、assume-guarantee 与抽象证明。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `atom` 结构 | `$A = (\mathrm{ctr}X_A, \mathrm{read}X_A, \mathrm{wait}X_A, Init_A, Update_A)$` | 一个更新单元由控制变量、读取变量、等待变量和两类动作组成。 |
| 模块结构 | `$P = (X_P, A_P)$` | 模块由变量分区和若干 `atom` 组成。 |
| 轨迹语言 | `$L_P = \{ \hat{s}[\mathrm{obs}X_P] \mid \hat{s} \text{ is a trajectory of } P \}$` | 语义由可观测 trace 决定。 |
| 实现关系 | `$P \preceq Q$` | 更细实现必须满足变量兼容和 trace containment。 |
| 时间抽象 | `$Q = \mathrm{next}_Y(P)$` | 允许把若干内部 round 折叠成一个外部 round。 |

## 构造方式与承载格式

### 建模入口

建模入口是模块声明与 `atom` 级 guarded command。论文中的典型入口包括：

1. 同步电路模块，如 `Not / And / Latch`。
2. 共享内存进程模块，如 Peterson mutual exclusion。
3. 消息握手模块，如 `Sender / Receiver`。

### 机器可处理承载方式

原文的承载是文本化模块语法：

1. 变量声明区。
2. `atom` 声明区。
3. `init` 与 `update` guarded commands。
4. `rename / composition / hide / next / trigger` 操作。

### 交换与互操作

论文强调的是“把不同语言和不同同步假设翻译到同一模块语义”，而不是定义一个开放文件标准。它更像验证中间表示，而不是交换标准本身。

## 配套基础设施

- 建模/编辑工具：原文给出了一整套可直接书写的模块语法和示例模式，但未附独立 IDE。
- 解析/交换/元模型支持：支持变量重命名、组合、隐藏和时间抽象，适合作为统一中间表示。
- 仿真/执行支持：模块 round 语义可直接执行于显式状态探索或 symbolic transition system。
- 验证/分析支持：论文明确面向 model checking、assume-guarantee 证明、trace refinement 和 fairness reasoning。
- 代码生成/转换支持：原文更强调“由多种语言翻译到 reactive modules 再验证”，而不是从其直接生成工业代码。
- 标准化或社区生态：研究影响力强，但不像 `SCXML` 或 `UML` 那样存在独立标准组织。

## 适用场景与需求前提

### 适用场景

适合同步电路、异步协议、共享内存程序、消息传递组件以及需要多层抽象验证的硬件软件协同系统。

### 需求前提

1. 需求能够分解成明确的变量集合和若干受控更新单元。
2. 系统行为能接受“以 round 为单位”的离散语义。
3. 需要显式地区分私有状态、接口输出和外部输入。
4. 需要做组合验证、精化验证或抽象证明。

### 不适用或高成本场景

若系统核心在连续控制律、密集数值积分或开放标准交换，`Reactive Modules` 不是最自然的目标语言。

## 与相邻形式主义的关系

相对 `I/O Automata`，它把同步/异步统一得更激进，并加入时间抽象 `next`；相对同步语言如 `Esterel`，它更偏建模与验证而不是编程；相对 `Statecharts`，它舍弃图形层次语法，转而强调变量分区和组合算子。

## 与本研究的关系

### 对 Project 1 的价值

它特别适合当“需求到状态机”的中间验证表示：既能容纳组件边界，也能容纳抽象层切换。

### 作为目标形式主义还是中间表示

更适合作为高可信中间表示，而不是面向终端工程师的最终交付工件。

### 对需求到模型生成的启发

如果需求天然包含多组件边界、输入输出分层和不同执行粒度，那么直接生成 `Reactive Modules` 会比生成单一大状态图更利于验证。

### 现实限制

它缺少主流工业交换标准和流行图形建模入口，落地到工程链通常还需要再翻译到 `UML / SCXML / Stateflow` 等载体。

## 重要的相关工作

### 奠基或前身工作

- `I/O Automata`
- 同步语言 `Esterel / Lustre / Signal`
- 共享内存并发模型与 guarded command 传统

### 同类型或同家族工作

- `Interface Automata`
- `Timed I/O Automata`
- `Contract Automata`

### 标准 / 格式 / 工具链工作

- 论文中的 `hide / next / trigger` 可直接当验证中间表示操作子
- 后续 `Mocha` 一类工具线与该模型关系紧密

### 与本研究关系最紧的工作

- 需要做组合建模、接口约束和精化验证时，这篇是极强的中间表示参考。

## 文献分类总结

- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：Reactive Modules
- 论文角色：组合建模框架
- 核心功能：在统一 round 语义下同时表达同步/异步组件，并支持组合、隐藏和时间抽象。
