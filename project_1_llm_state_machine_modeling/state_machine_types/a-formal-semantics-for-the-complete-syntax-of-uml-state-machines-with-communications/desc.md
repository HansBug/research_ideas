# 带通信的 UML 状态机完整语法形式语义 / A Formal Semantics for the Complete Syntax of UML State Machines with Communications

## 基本信息

- 标题：A Formal Semantics for the Complete Syntax of UML State Machines with Communications
- 中文标题：带通信的 UML 状态机完整语法形式语义
- 作者：Shuang Liu，Yang Liu，Étienne André，Christine Choppy，Jun Sun，Bimlesh Wadhwa，Jin Song Dong
- 发表：*Integrated Formal Methods (IFM 2013)*，LNCS 7940，pp. 331-346，2013
- DOI：`10.1007/978-3-642-38613-8_23`
- 链接：https://doi.org/10.1007/978-3-642-38613-8_23
- 形式主义：`UML State Machine / USM2C`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：完整语义 + model checker
- 工具/实现获取方式：原文明确说明实现了自包含工具 `USM2C`，支持编辑、仿真、deadlock 检查与 `LTL` 模型检查；正文未给公开仓库链接。
- 标准/格式获取方式：承载方式是 `UML 2.4.1` state machine 语法、event pool 机制、`LTS` 语义模型与 `USM2C` 查询输入；无独立行业交换标准。

## 简报

这篇论文的重要性在于，它不再满足于“形式化 UML 状态机的一小部分”，而是明确把 `UML 2.4.1` 中大量实际会用到的元素拉进正式语义里，包括 `choice / fork / join`、completion transition、event deferral，以及多个状态机之间的同步/异步通信。论文的目标很工程化：不是抽象讨论一个 core subset，而是给出一套足够完整的 operational semantics，并把它真正装进 `USM2C` 这样的 model checker。

- 形式主义定位：`UML State Machine` 的完整操作语义与验证方法，而不是一般 statechart 的泛讨论。
- 构造方式简述：先把 UML 语法对象编码为 tuples，再定义 RTC step、event pools、system-level `LTS`，最后让 `USM2C` 在这些语义上做模拟与 `LTL` 检查。
- 基础设施与场景简述：依托 `USM2C`、`LTS` 语义、event pool 抽象和 system-level communication semantics，服务软件行为建模、对象交互分析与 UML 级验证。

```text
UML 2.4.1 state machines -> tuple-based syntax + RTC semantics + system LTS -> USM2C simulation / model checking
```

## 形式主义定义与核心对象

### 定义对象

论文显式 formalize 了以下对象：

1. `State`、`Pseudostate`、`Transition`、`Region`、`State Machine`。
2. compound transitions。
3. active state configuration 与 active vertex configuration。
4. completion / deferred / normal 三类 event pools。
5. 多个状态机组成的 system-level `LTS`。

### 核心抽象

论文首先把单个状态定义为 tuple：

$$
s = (br, dtdef, \alpha_{en}, \alpha_{ex}, \alpha_{do}, cen, cex, dcpr, sm, bt)
$$

上式中的符号逐项解释如下：

1. `br` 是该 state 直接包含的 regions 集合。
2. `dtdef` 是 deferral triggers 集合。
3. `\alpha_{en}`、`\alpha_{ex}`、`\alpha_{do}` 分别是 entry、exit 和 do behaviors。
4. `cen` 与 `cex` 是 entry/exit point references。
5. `dcpr` 是 submachine state 的 connection point references。
6. `sm` 是该 submachine state 所引用的 state machine。
7. `bt` 是定义在该 state 上的 internal transitions 集合。

单个 UML state machine 被定义为：

$$
sm = (br, ccp)
$$

上式中的符号逐项解释如下：

1. `br` 是 top-most region。
2. `ccp` 是该 state machine 定义的 connection points。

而论文把 system 级对象定义为多个状态机的组合：

$$
sys = \parallel^C_{i \in [1,n]} Sm_i
$$

上式中的符号逐项解释如下：

1. `Sm_i = (sm_i, EP_i, GV_i)` 是第 `i` 个状态机及其事件池和全局变量。
2. `\parallel^C` 表示带同步通信约束的系统级组合。
3. `n` 是系统中的状态机数量。

### 一个最小例子与通俗解释

论文实验里最直观的是 `BankATM`：

1. `ATM` 和 `Bank` 各自是 UML state machine。
2. 有些交互是同步的 call action，有些是异步 message。
3. 每个状态机都有自己的 event pool，但系统最终要看整体 `LTS`。
4. `USM2C` 在 system level 检查 deadlock 和 `LTL` 性质，例如“卡片被吞卡前，错误 PIN 次数必须达到上限”。

通俗地说，这篇论文把 UML 状态机从“图画得很全”推进到“把 run-to-completion、消息收发、deferred events 和正交区 nondeterminism 都讲清楚”，这样工具才能真的验证整个对象系统。

### 运行 / 接受 / 转移语义

论文把 event pool 显式拆成三类：

$$
EP = (CEP, DEP, NEP)
$$

上式中的符号逐项解释如下：

1. `CEP` 是 completion event pool。
2. `DEP` 是 deferred event pool。
3. `NEP` 是 normal event pool。

这一步很关键，因为 completion、deferral 和 ordinary event 在 UML 里并不是同一种调度优先级。

对整个系统，论文把语义最终收束为：

$$
L = (S, S_{init}, \to)
$$

上式中的符号逐项解释如下：

1. `S` 是系统的 `LTS` 状态集合。
2. `S_{init}` 是系统初始状态。
3. `\to` 是系统级转移关系。

其中每个 `LTS` 状态又是多个状态机 configuration 的 tuple：

$$
(k_1, \ldots, k_n)
$$

这里 `k_i` 表示第 `i` 个状态机当前的 active-state configuration、event pool 与全局变量状态。

论文把异步通信和同步通信分别写成系统级规则。可保守整理成：

$$
(k_1,\ldots,k_j,\ldots,k_n) \to (k_1,\ldots,k'_k,\ldots,k'_j,\ldots,k_n)
$$

上式中的符号逐项解释如下：

1. `k_j \to k'_j` 表示当前发起者状态机执行了一个 RTC step。
2. 若是 `SendSignal(j,k)`，则消息被 merge 到被调者 `k` 的 event pool 中。
3. 若是 `Call(j,k)`，则 `k` 也被同步触发，且 `j` 的 RTC step 直到 `k` 返回后才完成。

论文还对 active-state 更新给出函数：

$$
NextK(ks, (\tilde{t}_1,\ldots,\tilde{t}_n))
$$

上式中的符号逐项解释如下：

1. `ks` 是当前 active state configuration。
2. `\tilde{t}_i` 是一个 compound transition。
3. `NextK` 计算执行这些 compound transitions 后的新 active-state configuration。

### 语义边界

这篇论文也明确有边界：

1. 它解决的是 `UML 2.4.1` state machine 的离散行为语义，不是实时/连续语义。
2. 重点是 run-to-completion、pseudostates 和 communications，而不是代码生成。
3. 虽然语义覆盖“完整语法”，但实现工具 `USM2C` 的规模能力仍有限。
4. 论文给的是自包含语义与工具线，不是开放交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| state tuple | `$s = (br, dtdef, \alpha_{en}, \alpha_{ex}, \alpha_{do}, cen, cex, dcpr, sm, bt)$` | 把 UML state 直接编码为可操作语义对象。 |
| state machine tuple | `$sm = (br, ccp)$` | 单个 UML state machine 的顶层骨架。 |
| event pool | `$EP = (CEP, DEP, NEP)$` | completion / deferred / normal events 必须分池处理。 |
| system 组合 | `$sys = \parallel^C_{i \in [1,n]} Sm_i$` | 多状态机系统层面的组合入口。 |
| LTS 语义 | `$L = (S, S_{init}, \to)$` | 最终所有 UML 运行语义都被压成 `LTS`。 |
| active-state 更新 | `$NextK(ks, (\tilde{t}_1,\ldots,\tilde{t}_n))$` | RTC step 的核心就是执行 compound transitions 后更新活动配置。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 简单、复合、正交、submachine states 都被覆盖。 |
| 事件 / 触发 | 很强 | completion、deferral、sync call、async signal 都有明确语义。 |
| 守卫 / 数据 | 强支持 | guards、effects、global variables 与 behaviors 都进入语义。 |
| 层次 | 很强 | composite / orthogonal / submachine 三条线都被正式覆盖。 |
| 并发 / 同步 | 很强 | 正交区 nondeterminism 与跨状态机同步/异步通信是主轴。 |
| 时间约束 | 不支持 | 不是 timed UML 语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 UML 行为层。 |
| 可执行 / 可验证性 | 很强 | `USM2C` 直接支持编辑、仿真和 `LTL` 检查。 |

### 形式化问题与性质

1. 论文真正补的是“UML 状态机完整语法如何落成可检查语义”。
2. 它不再把 `choice/fork/join`、completion 和 deferral 当成可忽略细节。
3. system-level communication semantics 让验证对象从单机状态图升级为对象系统。
4. `USM2C` 说明这套语义不是纸上 tuple，而是工具可执行的。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. `UML 2.4.1` state / region / transition / pseudostate 语法。
2. compound transitions、entry/exit points、submachine states。
3. event pool 及其调度机制。
4. system-level synchronous / asynchronous communications。

### 机器可处理承载方式

机器可处理承载方式包括：

1. UML state machine 图形模型。
2. tuple-based syntax encoding。
3. `LTS` 语义状态与 transition relation。
4. `USM2C` 可消费的 deadlock / `LTL` 验证输入。

### 交换与互操作

这篇论文的互操作重点在：

1. 从 UML 前端直接落到自定义 `LTS` 语义。
2. `USM2C` 保留 UML 级 counterexample traces，而不是只给后端编码痕迹。
3. 它与 `Spin/HUGO` 这类翻译路线形成对照，强调“不先把 UML 压扁到太小的子集”。

## 配套基础设施

- 建模/编辑工具：`USM2C` 支持 editing、step-wise simulation。
- 解析/交换/元模型支持：tuple-based syntax formalization 与 event-pool abstraction 构成语义承载。
- 仿真/执行支持：`USM2C` 可以按 RTC step 模拟状态机执行。
- 验证/分析支持：deadlock-freeness 与 `LTL` model checking。
- 代码生成/转换支持：论文不以代码生成见长，重点是直接语义和验证。
- 标准化或社区生态：直接对齐 `UML 2.4.1`，但工具生态仍偏研究型。

## 适用场景与需求前提

### 适用场景

适合需要保留 UML 原生建模习惯、又希望把对象行为和对象间通信一起纳入形式验证的软件建模场景。

### 需求前提

1. 行为模型必须主要是离散状态切换。
2. 团队确实会用到 `choice / fork / join / deferral / completion` 这类 UML 语法，而不是只用极简子集。
3. 需要验证的是整体对象系统，而不只是单一状态机。
4. 能接受 run-to-completion 和 event-pool 这类显式语义约束。

### 不适用或高成本场景

如果目标只是轻量状态图草图、纯代码级实现、或实时/连续行为验证，这套完整 UML 语义会显得过重。

## 与相邻形式主义的关系

相对 [uml-251-specification/desc.md](../uml-251-specification/desc.md)，本文补的是可执行语义与验证；相对 [the-statemate-semantics-of-statecharts/desc.md](../the-statemate-semantics-of-statecharts/desc.md)，它面向标准化 UML 而不是 `STATEMATE`；相对 [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)，这篇正好是 survey 里最典型的“direct operational semantics + self-contained tool”路线之一。

## 与本研究的关系

### 对 Project 1 的价值

如果 `project_1` 最终要输出工程团队能接受的标准状态机载体，`UML State Machine` 很难绕开；而这篇论文说明它并不是只能画图，也可以接上正式验证。

### 作为目标形式主义还是中间表示

它既可以作为面向工程交付的目标形式主义，也可以作为更下游验证模型之前的高层中间表示。

### 对需求到模型生成的启发

1. 若未来让 LLM 生成 UML 状态机，必须处理 completion、deferral、fork/join 等细节，而不能只生成 state/transition 外壳。
2. communication semantics 很重要，尤其在多对象系统里。
3. 若不想严重失真，生成阶段就要考虑 RTC 与 event-pool 语义，而不是事后硬译。

### 现实限制

完整 UML 语义很强，但也更重；如果需求本来只需要简单可执行状态机，`SCXML` 或更轻量 DSL 可能更实用。

## 重要的相关工作

- [uml-251-specification/desc.md](../uml-251-specification/desc.md)：给出 UML 状态机的规范母线。
- [the-statemate-semantics-of-statecharts/desc.md](../the-statemate-semantics-of-statecharts/desc.md)：代表另一条经典层次状态机工具语义路线。
- [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：系统比较 UML 形式化与自动验证路线的综述入口。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / USM2C`
- 论文角色：完整语义 + model checker
