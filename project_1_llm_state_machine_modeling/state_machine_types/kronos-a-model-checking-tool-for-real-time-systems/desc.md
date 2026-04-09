# KRONOS：实时系统模型检验工具 / Kronos: A Model-Checking Tool for Real-Time Systems

## 基本信息

- 标题：Kronos: A model-checking tool for real-time systems
- 中文标题：KRONOS：实时系统模型检验工具
- 作者：Marius Bozga，Conrado Daws，Oded Maler，Alfredo Olivero，Stavros Tripakis，Sergio Yovine
- 发表：*Computer Aided Verification (CAV 1998)*，pp. 546-550，1998
- DOI：`10.1007/BFb0028779`
- 链接：https://doi.org/10.1007/BFb0028779
- 形式主义：`Timed Automata / KRONOS`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-automata verifier / `TCTL` and timed-`Buchi` model-checking tool
- 工具/实现获取方式：原文明确给出 `http://www-verimag.imag.fr/TEMPORISE/kronos/` 作为 `KRONOS` 获取入口。
- 标准/格式获取方式：原文说明输入骨架是 `timed automata` 网络，性质可写成 `TCTL`、timed `Buchi` automata 或 untimed `LTS`；原文未给独立中立交换标准。

## 简报

这篇论文补的不是 timed automata 母理论，而是最早一批把 `timed automata + TCTL + timed Buchi` 做成可工程化验证器的工具锚点。`KRONOS` 的重点在三件事：用 `timed automata` 作为系统描述语言、同时支持 fixpoint 与 explorative 两类模型检查路线、再把 `DBM + BDD + on-the-fly + minimization` 这些状态空间控制手段组合成一套完整工具箱。

- 形式主义定位：`timed automata` 的平台级验证器，而不是新的自动机子类。
- 构造方式简述：系统写成 network of timed automata，性质写成 `TCTL`、timed `Buchi` automata 或 untimed `LTS`，再交由 fixpoint 或 on-the-fly reachability 引擎处理。
- 基础设施与场景简述：依托 `DBM`、`BDD`、abstraction、time-abstracting bisimulation 与 `ALDEBARAN` 接口，服务实时协议、异步电路、调度与一般实时时序分析。

```text
timed automata network -> KRONOS symbolic/explorative engine -> DBM/BDD state-space handling -> TCTL or timed-Buchi checking -> diagnostic trail / minimized untimed interface
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. communicating timed automata；
2. network composition；
3. `TCTL` 与 timed `Buchi` property formalisms；
4. `DBM` clock-region representation 与 `BDD`-encoded discrete variables；
5. time-abstracting bisimulation 与 `LTS` export / minimization。

### 核心抽象

对 `KRONOS` 而言，基础建模对象仍可写成 timed automaton：

$$ A = (L, \ell_0, C, V, E, Inv) $$

上式中的符号逐项解释如下：

1. `L` 是 locations 集合。
2. `\ell_0` 是初始 location。
3. `C` 是 clocks 集合。
4. `V` 是有界整数或枚举型离散变量。
5. `E` 是边集合，每条边包含 guard、同步标签与更新。
6. `Inv` 是 location invariants。

系统通常写成 automata 网络：

$$ N = A_1 \parallel A_2 \parallel \cdots \parallel A_n $$

上式中的符号逐项解释如下：

1. `A_i` 是单个 timed automaton。
2. `\parallel` 表示通过 rendez-vous 或共享变量进行组合。
3. `N` 是 `KRONOS` 实际验证的全局实时状态机。

论文明确说明 fixpoint 路线是对前驱算子做嵌套不动点。保守写成：

$$ Sat(EF\,\varphi) = \mu X.(\varphi \lor Pre(X)) $$

$$ Sat(EG\,\varphi) = \nu X.(\varphi \land Pre(X)) $$

上式中的符号逐项解释如下：

1. `Sat(\cdot)` 是满足给定时序公式的状态集合。
2. `Pre(X)` 是一步前驱状态集合。
3. `\mu` 是最小不动点。
4. `\nu` 是最大不动点。
5. 这正对应论文所说“starting from an initial set of states and iterating a precondition operator until stabilization”。

### 一个最小例子与通俗解释

一个最小例子可以是双进程互斥：

1. 两个 automata 都有 `idle` 与 `crit` 两个离散位置。
2. 每个 automaton 带一个 clock `x_i`，要求“请求后在 `d` 时间内要么进入临界段，要么超时回退”。
3. 性质可以写成“不会同时在 `crit`”，以及“请求后最终在时限内响应”。
4. `KRONOS` 一边展开 network 的 reachable states，一边检查 `TCTL` 或 timed `Buchi` 条件，并可返回诊断轨迹。

通俗地说，`KRONOS` 像是把普通有限状态机上的“能不能到某状态”扩成“在这些时钟约束下能不能按时到、会不会永远拖着不动、会不会出现某条坏时间轨迹”。

### 运行 / 接受 / 转移语义

基本延时与离散转移可保守写成：

$$ (\ell,\nu,v) \xrightarrow{d} (\ell,\nu + d,v) $$

$$ (\ell,\nu,v) \xrightarrow{a} (\ell',\nu[X:=0],v') $$

上式中的符号逐项解释如下：

1. `\ell`、`\ell'` 是离散位置。
2. `\nu` 是当前 clocks 赋值。
3. `v`、`v'` 是离散变量赋值。
4. `d` 是非负延时，且沿途必须满足不变式。
5. `a` 是同步或内部动作。
6. `X:=0` 表示某些 clocks 被 reset。

`KRONOS` 的符号状态不是单个 valuation，而是“控制位置 + 时钟约束”。论文明确写到符号状态由 control location 和 `DBM` 组成，可保守整理为：

$$ Z = (\ell, D, b) $$

上式中的符号逐项解释如下：

1. `\ell` 是控制位置组合。
2. `D` 是用 `DBM` 表示的 clock valuation 集合。
3. `b` 是用 `BDD` 编码的离散部分。
4. 这也是论文表格中 symbolic states、`BDD` nodes 等性能指标的语义底座。

### 语义边界

1. 论文主体针对的是 `timed automata`，不是一般 hybrid dynamics。
2. 数据部分要求 bounded integer 或 enumeration type，不能无限制扩成富数据程序。
3. 最小化接口是 time-abstracting bisimulation，因此导出的 `LTS` 会丢失精确延时，只保留 untimed 行为等价类。
4. 这是一篇工具论文，不重讲完整 timed automata 判定理论；形式主义本体仍要回看更早的 timed automata 理论文献。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础模型 | `$A = (L, \ell_0, C, V, E, Inv)$` | `KRONOS` 的系统描述语言是 timed automata。 |
| 网络组合 | `$N = A_1 \parallel \cdots \parallel A_n$` | 真实系统通常按并行 automata 网络建模。 |
| fixpoint 可达性 / 存在性 | `$Sat(EF\,\varphi) = \mu X.(\varphi \lor Pre(X))$` | 论文的 fixpoint engine 通过前驱迭代求满足集。 |
| fixpoint 保持性 | `$Sat(EG\,\varphi) = \nu X.(\varphi \land Pre(X))$` | 论文支持一般 `TCTL` 风格的嵌套不动点检查。 |
| 符号状态 | `$Z = (\ell, D, b)$` | `DBM` 和 `BDD` 分别承载 clocks 与离散变量。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | network of timed automata 是主骨架。 |
| 事件 / 触发 | 很强 | 支持 binary / n-ary rendez-vous 与共享变量。 |
| 守卫 / 数据 | 中等支持 | 支持 bounded integer / enumeration，但不是富数据程序分析器。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 很强 | 面向 communicating timed automata 网络。 |
| 时间约束 | 很强 | `DBM`、fixpoint、timed `Buchi` 与 `TCTL` 都是核心能力。 |
| 连续动态 / 随机性 | 弱支持 | 论文只把 hybrid case studies 当应用面，不把一般连续动力学做成主对象。 |
| 可执行 / 可验证性 | 很强 | 支持符号、on-the-fly、最小化、诊断轨迹与接口导出。 |

### 形式化问题与性质

1. `KRONOS` 同时给出 fixpoint 与 explorative 两条路线，这使它既能做纯符号检查，也能做 on-the-fly 诊断。
2. 它很早就把 `timed Buchi` liveness checking 纳入主工具链，而不是只做 safety reachability。
3. `DBM + BDD + abstraction + minimization` 的组合说明这篇论文真正补的是 timed-verification infrastructure，而不是单一算法。

## 构造方式与承载格式

### 建模入口

原文给出的主要建模入口有：

1. network of timed automata；
2. binary / n-ary rendez-vous synchronisation；
3. bounded integer / enumeration shared variables；
4. `TCTL`、timed `Buchi` automata 与 untimed `LTS` 规格接口。

### 机器可处理承载方式

机器可处理承载方式包括：

1. timed automata 网络输入；
2. `DBM` 表示的 clocks 约束；
3. `BDD` 编码的离散变量；
4. 导出的 untimed `LTS` / minimized graph。

### 交换与互操作

互操作重点不在中立交换标准，而在验证接口：

1. 可以把最小化后的模型暴露成 untimed `LTS`。
2. 可与 `ALDEBARAN` 工具套件配合做 bisimulation / simulation equivalence。
3. `OPTIKRON` 等前处理工具可用于时钟约减。

## 配套基础设施

- 建模/编辑工具：原文主体聚焦验证器本身，不强调图形建模前端。
- 解析/交换/元模型支持：timed automata 网络输入、`TCTL` / timed `Buchi` / `LTS` 接口、`LTS` 导出。
- 仿真/执行支持：支持 reachability-graph generation 与 exploration-driven analysis。
- 验证/分析支持：fixpoint checking、explorative checking、safety / liveness、timed `Buchi` emptiness、abstraction、time-abstracting minimization。
- 代码生成/转换支持：不主打代码生成；主要是 `timed automata -> minimized untimed interface` 这种验证向转换。
- 标准化或社区生态：`KRONOS` 站点、`OPTIKRON`、`ALDEBARAN` 构成早期 timed-verification 生态。

## 适用场景与需求前提

### 适用场景

适合实时协议、定时异步电路、调度与一般嵌入式实时时序约束验证，尤其适合“模型是 timed automata、性质需要 `TCTL` / liveness / diagnosable trails”的场景。

### 需求前提

1. 系统可压成 communicating timed automata，而不是连续动力学主导的模型。
2. 离散数据需保持有界。
3. 关注点主要是安全、响应性、死锁、时间进展与典型实时性质。
4. 如果要与 untimed 等价检查配合，接受 time abstraction 带来的信息折叠。

### 不适用或高成本场景

如果需求核心依赖 rich data、概率、层次状态图或开放交换标准，`KRONOS` 就更像历史基础设施锚点，而不是最顺手的当前主工具。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`KRONOS` 更早地固定了 `timed automata + TCTL + timed Buchi` 的验证器骨架；相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，`UPPAAL 4.0` 更偏语言与平台升级，而 `KRONOS` 更像早期 symbolic / on-the-fly timed-checking 原型；相对 [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)，`HyTech` 向一般 linear hybrid systems 扩张，而 `KRONOS` 聚焦 clocks-only timed automata；相对 [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)，`Synthia` 补的是 timed-game synthesis，而 `KRONOS` 是 timed model checking 的更早平台锚点。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“目标状态机语言一旦带有显式时间约束，底层验证承载往往会自然落到 `DBM` 风格符号状态空间”。
2. 对 `project_1` 的“生成-验证-修复”闭环来说，`timed automata + TCTL + diagnostic trail` 是非常典型的后端形态。
3. 它还提醒我们：即使最终产物不是 `KRONOS`，也应尽量保留 clocks、同步结构和性质语言之间的对应关系，否则很难自动接入成熟 timed verifier。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`KRONOS` 更像 timed-automata 验证载体与工具锚点，而不是最终面向用户的建模语言。

## 重要的相关工作

- [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：后续更普及的 `timed automata` 教程与工具入口。
- [uppaal-40/desc.md](../uppaal-40/desc.md)：`UPPAAL` 主平台升级条目。
- [hytech-a-model-checker-for-hybrid-systems/desc.md](../hytech-a-model-checker-for-hybrid-systems/desc.md)：从 timed 走向 hybrid 的相邻验证器路线。
- [synthia-verification-and-synthesis-for-timed-automata/desc.md](../synthia-verification-and-synthesis-for-timed-automata/desc.md)：timed-automata synthesis 线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 timed-automata 验证平台锚点论文，适合作为 `KRONOS`、早期 `DBM`-driven realtime checking 与 `TCTL` / timed-`Buchi` 工具化路线的基础设施证据入账。
