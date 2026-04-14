# TarTar：时间自动机修复工具 / TarTar: A Timed Automata Repair Tool

## 基本信息

- 标题：TarTar: A Timed Automata Repair Tool
- 中文标题：TarTar：时间自动机修复工具
- 作者：Martin Kolbl，Stefan Leue，Thomas Wies
- 发表：*Computer Aided Verification*，pp. 529-540，2020
- DOI：`10.1007/978-3-030-53288-8_25`
- 链接：https://doi.org/10.1007/978-3-030-53288-8_25
- 形式主义：`timed automata / timed diagnostic trace / repair analysis / TarTar`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：基于 `TDT` 的 `Timed Automata` 自动修复与 admissibility filtering 工具条目
- 工具/实现获取方式：论文给出开源仓库 `https://github.com/sen-uni-kn/tartar`，并说明核心实现是一个支持 `GUI / CLI / web` 的 `Java` 工具。
- 标准/格式获取方式：输入主体是 `Uppaal` 模型和可选 `TDT` XML；中间层使用 `SMT-LIB2` 约束与 `TTS`，不是独立标准。

## 简报

`TarTar` 的核心价值不在“再做一个 timed model checker”，而在于把 timed counterexample 真正变成修复入口。它从违反 timed safety property 的 timed diagnostic trace 出发，把 trace 编码成线性实数约束，再通过 `MaxSMT` 计算一组语法级修补，并用 untimed language equivalence 过滤掉会破坏系统功能行为的候选修复。

- 形式主义定位：围绕 `Network of Timed Automata` 的修复方法路线与工程化工具，而不是新的时间自动机变体。
- 构造方式简述：`Uppaal model + property -> TDT -> SMT-LIB2 repair constraints -> MaxSMT repair candidate -> untimed-language admissibility check -> repaired model`。
- 基础设施与场景简述：依托 `Uppaal`、`Z3`、修改过的 `opaal`、`AutomataLib` 与 `Java` 数据流架构，服务 timed safety violation 的自动修补与解释。

```text
timed safety violation -> timed diagnostic trace -> repair variables -> candidate repairs -> admissibility filter -> repaired NTA
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Network of Timed Automata` (`NTA`)。
2. 违反 timed safety property 的 `Timed Diagnostic Trace` (`TDT`)。
3. bound / operator / clock-reference / reset / urgency 五类修复变量。
4. `MaxSMT` 求解出的修复候选。
5. 基于 untimed language equivalence 的 admissibility 检查。

### 核心抽象

论文默认基于标准 `Timed Automata` / `NTA` 语义；结合文中叙述，可把单个自动机保守整理为：

$$
A = (L, l_0, C, \Sigma, E, \mathrm{Inv})
$$

上式中的符号逐项解释如下：

1. `$L$` 是 locations 集合。
2. `$l_0$` 是初始 location。
3. `$C$` 是 clocks 集合。
4. `$\Sigma$` 是动作标签集合。
5. `$E$` 是带 guard、reset 与同步标签的边集合。
6. `$\mathrm{Inv}$` 为 location invariants。
7. 论文对象通常是多个自动机同步组成的 `NTA`，这里的元组是依据标准用法做的保守整理。

论文的输入反例是 timed diagnostic trace。可保守写成：

$$
\tau = d_0 a_0 d_1 a_1 \cdots d_n
$$

上式中的符号逐项解释如下：

1. `$d_i \in \mathbb{R}_{\ge 0}$` 是一次时间延迟。
2. `$a_i \in \Sigma$` 是一次离散动作或同步事件。
3. 这条序列在原始 `NTA` 中可行，并导致 timed safety property 被违反。
4. 论文中的 sequence diagram 与 symbolic `TDT` 本质上都在描述这种“延迟与动作交替”的诊断轨迹。

论文展示的最直接修复是 clock-bound variation：

$$
x \le 2 + v
$$

上式中的符号逐项解释如下：

1. `$x \le 2$` 是原始约束。
2. `$v$` 是 bound-variation 变量。
3. 当 `MaxSMT` 求得 `$v \neq 0$` 时，就对应一个具体的 bound 修改。
4. 论文还把同样思路扩展到 comparison operator、clock reference、reset status 与 urgency 的变化。

修复的两条核心目标可压成：

$$
\tau \notin \mathrm{TTraces}(\mathcal N')
$$

以及

$$
L_{\mathrm{untimed}}(\mathcal N') = L_{\mathrm{untimed}}(\mathcal N)
$$

上式中的符号逐项解释如下：

1. `$\mathcal N$` 是原始 `NTA`，`$\mathcal N'$` 是修复后模型。
2. 第一式表示给定 `TDT` 在修复后模型中不再可行。
3. 第二式表示修复前后 untimed language 相同，也就是论文所说的 functional equivalence。
4. 第二条正是 admissibility check 的判定标准。

### 一个最小例子与通俗解释

论文 running example 是一个 client 向 database 发送请求并要求 `4` 个时间单位内收到响应的 `NTA`：

1. client 在发送请求后进入等待响应位置，并用 clock `x` 计时。
2. `TDT` 展示了一条虽然消息最终返回、但响应超时的执行。
3. `TarTar` 可以建议把某个约束从 `w \le 2` 收紧到 `w \le 1`，也可以改 comparison operator、换 clock、增删 reset，甚至把某个 location 改成 urgent。
4. 工具不会把所有“能堵住这条坏轨迹”的修改都直接输出，而是继续筛掉那些改变原模型 untimed 功能行为的候选。

通俗地说，`TarTar` 像“针对 timed counterexample 的自动补丁搜索器”。它既不是纯调参器，也不是任意代码修复器，而是专门在 `Timed Automata` 语法层里找那种“能堵住坏时间行为，但别把系统本来会做的事删掉”的修补。

### 运行 / 接受 / 转移语义

论文仍沿用标准 `Timed Automata` 两步语义。可保守写成：

$$
(l,u) \xrightarrow{d} (l, u + d),\qquad (l,u) \xrightarrow{a} (l', [r:=0]u)
$$

上式中的符号逐项解释如下：

1. `$l$` 与 `$l'$` 是 locations。
2. `$u$` 是当前 clock valuation。
3. `$d$` 是时间推进量，必须与 invariants 相容。
4. `$a$` 是离散动作。
5. `$r$` 是本步需要 reset 的 clocks 集。

论文的修复流水线可保守整理为：

$$
\tau \xrightarrow{\mathrm{encode}} \Phi_\tau(\theta) \xrightarrow{\mathrm{MaxSMT}} \theta^\ast \xrightarrow{\mathrm{apply}} \mathcal N'
$$

上式中的符号逐项解释如下：

1. `$\tau$` 是输入 `TDT`。
2. `$\Phi_\tau(\theta)$` 是加入修复变量 `$\theta$` 后得到的线性实数约束系统。
3. `$\theta^\ast$` 是 `MaxSMT` 找到的最优或某个可行修复解。
4. `$\mathcal N'$` 是把该解回填到原模型后得到的 repaired model。

admissibility 检查则基于两个模型的 timed transition systems。可压成：

$$
\mathrm{Untime}(\mathrm{TTS}(\mathcal N)) \equiv \mathrm{Untime}(\mathrm{TTS}(\mathcal N'))
$$

上式中的符号逐项解释如下：

1. `$\mathrm{TTS}(\mathcal N)$` 是由 `opaal` 计算的 timed transition system。
2. `$\mathrm{Untime}$` 表示去掉具体时间信息后得到的动作语言。
3. 等价成立时，该修复被视为 admissible。
4. 论文说明这一检查由 `AutomataLib` 完成。

### 语义边界

1. `TarTar` 聚焦 timed safety violation，不处理一般 liveness repair。
2. 修复空间是语法级、局部的：bound、operator、clock reference、reset 与 urgency，而不是任意结构重写。
3. admissibility 用 untimed language equivalence 收束，因此允许改变 timing，但不允许增删 untimed 行为。
4. 工具依赖 `Uppaal` 模型与 `TDT`，不面向一般 hybrid system。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `Timed Automata` 骨架 | `$A = (L, l_0, C, \Sigma, E, \mathrm{Inv})$` | `TarTar` 处理的基础模型对象。 |
| `TDT` 形态 | `$\tau = d_0 a_0 d_1 a_1 \cdots d_n$` | 输入反例是带时间延迟的诊断轨迹。 |
| bound variation | `$x \le 2 + v$` | 论文显式给出的修复编码例子。 |
| trace elimination | `$\tau \notin \mathrm{TTraces}(\mathcal N')$` | 修复后坏轨迹必须不可行。 |
| admissibility | `$L_{\mathrm{untimed}}(\mathcal N') = L_{\mathrm{untimed}}(\mathcal N)$` | 修复不能改变原模型的 untimed 功能行为。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 `NTA` locations、clocks 与同步结构。 |
| 事件 / 触发 | 很强 | `TDT` 就是事件与延迟交替的核心对象。 |
| 守卫 / 数据 | 强支持 | 修复主要落在 guard、invariant、clock reference、reset 与 urgency。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 处理的是 `NTA` network，但焦点不在组合语义本身。 |
| 时间约束 | 很强 | 整个工具就是围绕 timed safety violation 修复。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic repair。 |
| 可执行 / 可验证性 | 很强 | `Uppaal`、`MaxSMT`、admissibility checking 与多种前端接口都已成型。 |

### 形式化问题与性质

1. `TarTar` 的关键点不是“算一个 repair”，而是把 repair 定义成“堵住坏轨迹且保持 untimed 功能等价”的二重目标。
2. `TDT -> SMT -> repaired model -> language check` 这条链路非常适合后续做自动化修复闭环。
3. 五类修复操作共同说明：timed model repair 不一定非得重建整个 automaton，很多时候局部约束修补就足够。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Uppaal` 模型文件。
2. 待验证 timed safety property。
3. 可选外部提供的 `TDT` 文件；若未提供，可由 `TarTar` 自动调用 `Uppaal` 生成。
4. repair kind 选择与 admissibility 开关。

### 机器可处理承载方式

机器可处理承载方式包括：

1. symbolic `TDT` 内部表示 `Trace`。
2. `SMT-LIB2` 线性实数约束。
3. repaired `Uppaal` model。
4. `TTS` 与 witness traces。

### 交换与互操作

1. `TarTar` 以 `Uppaal` 为前端建模标准事实来源。
2. `Z3` 负责 `MaxSMT` 求解。
3. 修改过的 `opaal` 负责导出 `TTS`。
4. `AutomataLib` 负责 untimed language equivalence 检查。

## 配套基础设施

- 建模/编辑工具：`GUI`、`CLI`、web 三种前端，共用同一 `Java` 后端。
- 解析/交换/元模型支持：`Trace`、`SMT-LIB2`、`TTS` 和 repaired-model artifact 构成数据流。
- 仿真/执行支持：核心不是仿真，而是反例驱动的修复候选生成。
- 验证/分析支持：`Uppaal` 反例生成、`Z3` 求解、`opaal` 状态系统导出、`AutomataLib` 等价检查。
- 代码生成/转换支持：将 `TDT` 编码成约束、把修复结果回写到 `Uppaal` 模型，是其关键转换链。
- 标准化或社区生态：`Uppaal`、`SMT-LIB2`、`Z3`、`AutomataLib`、`LearnLib` 共同构成研究型 timed-repair 生态。

## 适用场景与需求前提

### 适用场景

适合 timed safety property 被反例击穿后的模型修复、实时协议 / 控制器的 clock-constraint 调参、以及需要把反例直接变成自动修补建议的 `Timed Automata` 工作流。

### 需求前提

1. 系统必须已能落成 `Uppaal` 风格 `Timed Automata` 模型。
2. 失败性质最好是 timed safety property，并能生成代表性 `TDT`。
3. 问题应主要来自局部约束、reset 或 urgency 的错误，而不是宏观结构错误。
4. 使用者接受“功能等价按 untimed language 收束”的 admissibility 口径。

### 不适用或高成本场景

若错误根源是模型缺状态、缺同步组件、缺连续动力学抽象，或需求本身并非 timed safety，`TarTar` 这类局部语法修复就不够。

## 与相邻形式主义的关系

相对 [fault-diagnosis-for-timed-automata/desc.md](../fault-diagnosis-for-timed-automata/desc.md)，后者是 timed counterexample 与可观测性分析的诊断母线，`TarTar` 则把 counterexample 进一步推进到 repair；相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md) 与 zone/backward-reachability 路线，`TarTar` 不主要发明新抽象，而是复用 model-checking backend 服务修复；相对 [tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md](../tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md)，`Tarzan` 是 reachability backend，`TarTar` 是反例驱动的 timed-repair 工具；相对 `TACK / TA2SMT` 这类 timed-logic compiler 路线，`TarTar` 聚焦模型修补而不是公式编译。

## 与本研究的关系

### 对 Project 1 的价值

`TarTar` 对本研究最直接的启发，是“验证失败后的模型修复不一定靠重新生成整模，而可以围绕已知坏轨迹做结构化局部修补”。这与本仓库后续的“已知缺陷驱动的迭代修复”方向高度一致。

### 可复用启发

1. 让验证后端输出结构化反例，而不是只输出真假结论，是自动修复的前提。
2. 修复空间应事先显式化成若干可解释的 edit families，而不是黑盒神经补丁。
3. “修对了坏轨迹”与“没破坏原有功能”必须同时检查，后者可借助语言等价或行为包含关系。

## 重要的相关工作

1. [fault-diagnosis-for-timed-automata/desc.md](../fault-diagnosis-for-timed-automata/desc.md)：timed counterexample 与诊断主线的理论锚点。
2. [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)：timed reachability 抽象后端对照。
3. [tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md](../tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md)：更底层的 timed reachability library。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 关键特性：`TDT`、`MaxSMT`、bound/operator/clock/reset/urgency repairs、admissibility check、`Uppaal` toolchain。
- 构造方式：`counterexample -> repair constraints -> MaxSMT candidate -> untimed-language filter -> repaired model`。
- 基础设施：`Uppaal`、`Z3`、`opaal`、`AutomataLib`、`Java GUI/CLI/web`。
- 对状态机族演化树而言，它是 timed-automata repair route 的静态挂接口径，不形成新的主树节点。
