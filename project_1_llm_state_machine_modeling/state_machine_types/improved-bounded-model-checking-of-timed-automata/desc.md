# 时间自动机有界模型检查的改进 / Improved Bounded Model Checking of Timed Automata

## 基本信息

- 标题：Improved Bounded Model Checking of Timed Automata
- 中文标题：时间自动机有界模型检查的改进
- 作者：Robert L. Smith，Marcello M. Bersani，Matteo Rossi，Pierluigi San Pietro
- 发表：*2021 IEEE/ACM 9th International Conference on Formal Methods in Software Engineering (FormaliSE)*，pp. 97-110，2021
- DOI：`10.1109/FORMALISE52586.2021.00016`
- 链接：https://doi.org/10.1109/FORMALISE52586.2021.00016
- 形式主义：`Timed Automata / TACK / TA2SMT / BitVector-SMT bounded model checking`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-automata bounded-model-checking method replacing TA2CLTLoc with direct TA2SMT encoding
- 工具/实现获取方式：原文明确说明该方法建立在 `TACK` bounded model checker 之上，并比较新旧编码在 `TACK` 中的实现；本文未给独立公开仓库链接。
- 标准/格式获取方式：主承载是 network of timed automata、`MITL` properties、`TA2SMT` BitVector/SMT encoding 和 `Z3` solver 输入；它不是交换标准。

## 简报

这篇论文补的是 `Timed Automata` 验证里的求解方法路线。它没有改写 `TA` 母理论，而是把 `TACK` 里原先的 `TA2CLTLoc -> Zot -> SMT` 路线改成“性质仍走 `MITL/CLTLoc`，但 `TA` 网络直接编码成 BitVector + SMT”的 `TA2SMT` 路线，从而明显提升 `BMC` 性能并修复旧实现对整数变量、broadcast 和 interval edge 的支持缺口。

- 形式主义定位：围绕 `Timed Automata` 的有界模型检查方法，而不是新的时间自动机子类。
- 构造方式简述：`MITL` 性质继续沿用 `TACK` 既有编码；`TA` 网络则直接编码成 BitVector/SMT terms，再与性质侧公式汇合。
- 基础设施与场景简述：依托 `TACK`、BitVector aliases、per-location null transitions、lasso-shaped traces 与 `Z3`，服务 network of `TA` 的 `SMT`-based bounded verification。

```text
TA network + MITL property -> TA2SMT terms + property encoding -> BitVector/SMT formula -> Z3 bounded check
```

## 形式主义定义与核心对象

### 核心抽象

论文围绕以下对象组织：

1. 带变量的 timed automata。
2. network of timed automata 及其 configuration / trace / signal semantics。
3. `TACK` 的旧 `TA2CLTLoc` 路线。
4. 新的 `TA2SMT` BitVector-based encoding。
5. lasso-shaped bounded traces 与 `SMT` solving。

### 定义对象

论文直接给出带变量 `TA` 的元组，可写成：

$$
A=\langle AP, X, Act_\tau, Int, Q, q_0, v^0_{var}, Inv, L, T \rangle
$$

上式中的符号逐项解释如下：

1. `$AP$` 是 atomic propositions 集合。
2. `$X$` 是 clocks 集合。
3. `$Act_\tau$` 是动作与空动作集合。
4. `$Int$` 是整数变量集合。
5. `$Q$` 是 locations 集合，`$q_0$` 是初始 location。
6. `$v^0_{var}$` 是整数变量初值函数，`$Inv$` 是 location invariants，`$L$` 是 location labeling，`$T$` 是 transitions。

network configuration 的定义可写成：

$$
(l, v_{var}, v)
$$

上式中的符号逐项解释如下：

1. `$l=[q_1,\ldots,q_N]$` 是网络中每个 automaton 的当前位置向量。
2. `$v_{var}$` 是整数变量赋值。
3. `$v$` 是 clocks valuation。
4. 这是论文定义 network semantics、trace 与 signal 的基本状态对象。

新编码的总体公式直接写成：

$$
\varphi_N := \varphi_{init} \land \varphi_{trans} \land \varphi_{sync} \land \varphi_{loop}
$$

上式中的符号逐项解释如下：

1. `$\varphi_{init}$` 约束初始位置、初始变量和初始时钟。
2. `$\varphi_{trans}$` 编码 transitions、guards、assignments、invariants 和位置更新。
3. `$\varphi_{sync}$` 编码网络中的同步语义。
4. `$\varphi_{loop}$` 保证 bounded trace 形成合法 lasso-shaped run。

### 一个最小例子与通俗解释

论文用一个简单 `TA` 展示 guards、assignments 和 invariants：

1. 某条迁移只有在时钟 `x > 5` 时可触发。
2. 触发时会执行 `x := 0` 和 `n := n + 1` 这类更新。
3. 若某个 location 的 invariant 是 `x < 2`，系统就不能一直停在该位置。
4. `TA2SMT` 把“当前位置激活了哪条迁移、边是 left-closed 还是 right-closed、变量值是多少”都编码成 bounded BitVector / numeric terms，再交给 `SMT` 求解器。

通俗地说，这套方法像“把时间自动机一步一步压成二进制约束”。旧路线先绕到 `CLTLoc` 再翻到 `SMT`；新路线直接把 `TA` 网络写成求解器更容易吃的 BitVector 约束。

### 运行 / 接受 / 转移语义

论文给出 network discrete transition 的骨架，可保守写成：

$$
(l,v_{var},v)\xrightarrow{\ast}(l',v'_{var},v')
$$

上式中的符号逐项解释如下：

1. `$\ast$` 表示一个网络离散步，它由各 automata 的动作元组组成。
2. `$l,l'$` 是离散位置向量。
3. `$v_{var},v'_{var}$` 是整数变量赋值前后状态。
4. `$v,v'$` 是时钟赋值前后状态。
5. 论文进一步区分 left-closed 与 right-closed edge，以及 null transition 与真正 firing transition。

time transition 则可写成：

$$
(l,v_{var},v)\xrightarrow{\delta}(l,v_{var},v+\delta)
$$

上式中的符号逐项解释如下：

1. `$\delta>0$` 是经过的真实时间。
2. 离散位置向量 `$l$` 不变。
3. 整数变量 `$v_{var}$` 不变。
4. 时钟 valuation 统一加上 `$\delta$`，同时必须满足弱满足或普通满足的 invariant 约束。

`TA2SMT` 中关键的工程改动是用 BitVector 表示 active transitions，并据此定义 location aliases。其直觉可保守压成：

$$
q \equiv \bigvee_{t \in T,\ src(t)=q} t
$$

上式中的符号逐项解释如下：

1. `$q$` 是某个 location alias。
2. `$t$` 是 source location 为 `$q$` 的 transition alias。
3. 由于引入了每个 location 各自的 null transition，location 不再需要单独变量即可由 active transition 唯一定义。

### 语义边界

1. 本文研究的是 network of `TA` 的 bounded model checking，不是一般 hybrid automata reachability。
2. `MITL` 性质编码仍沿用旧 `TACK` 路线，创新点主要在 `TA` 侧 encoding。
3. 方法依赖 bounded lasso-shaped traces，因此更像 `BMC` 而不是完整 symbolic fixpoint verifier。
4. 论文更强调 solver-facing encoding 与工程修复，而不是重讲 `TA` 母理论。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 元组 | `$A=\langle AP,X,Act_\tau,Int,Q,q_0,v^0_{var},Inv,L,T\rangle$` | 论文直接给出的带变量 `TA` 定义。 |
| network configuration | `$(l,v_{var},v)$` | `TA` 网络语义的基本状态对象。 |
| 时间推进 | `$(l,v_{var},v)\xrightarrow{\delta}(l,v_{var},v+\delta)$` | bounded trace 中的 delay step。 |
| 总编码公式 | `$\varphi_N=\varphi_{init}\land\varphi_{trans}\land\varphi_{sync}\land\varphi_{loop}$` | `TA2SMT` 的完整 solver 输入骨架。 |
| location alias | `$q \equiv \bigvee_{t:src(t)=q} t$` | 新编码用 transition BitVectors 推导 active locations。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 network of timed automata。 |
| 事件 / 触发 | 很强 | actions、null transitions、同步与 edge types 都被显式编码。 |
| 守卫 / 数据 | 很强 | 相比旧编码，整数变量不再只支持 equality，完整 guard / assignment grammar 可进入 `SMT`。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 很强 | network semantics 与 `\varphi_{sync}` 明确编码同步行为。 |
| 时间约束 | 很强 | clocks、weak satisfaction、left/right-closed intervals 和 lasso traces 都是主轴。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic line。 |
| 可执行 / 可验证性 | 很强 | `TACK + TA2SMT + Z3` 已完成实验实现并优于旧编码。 |

### 形式化问题与性质

1. `TA2SMT` 的本质不是换一个 solver，而是让 `TA` 网络以更贴近 solver 的方式表达。
2. per-location null transitions 和 location aliases 是最关键的结构性优化之一。
3. 新编码不仅更快，还补齐了旧实现对变量比较、broadcast 和 interval edges 的支持缺口。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. network of timed automata。
2. `MITL` property。
3. bounded length `k+2` lasso-shaped traces。
4. `TACK` / `Z3` based solver workflow。

### 机器可处理承载方式

机器可处理承载方式包括：

1. transition BitVectors。
2. location aliases。
3. integer-variable BitVectors in two's-complement notation。
4. real-valued clock functions。
5. `\varphi_{init}`、`\varphi_{trans}`、`\varphi_{sync}`、`\varphi_{loop}` 四类公式。

### 交换与互操作

互操作重点不在中立交换标准，而在 `TACK` 的内部编译链：

1. `MITL` 侧继续走既有 `CLTLoc` / property translation。
2. `TA` 侧改用 direct BitVector encoding。
3. 二者最终在 `SMT` 层汇合并交由 `Z3` 求解。

## 配套基础设施

- 建模/编辑工具：原文依赖 `TACK`，不强调新的图形化前端。
- 解析/交换/元模型支持：network-of-`TA` parser、property parser 和 solver-facing BitVector encoding。
- 仿真/执行支持：主线是 bounded symbolic solving，不是 runtime simulation platform。
- 验证/分析支持：`MITL` bounded verification、network semantics、interval-edge handling、broadcast synchronization、integer guards / assignments。
- 代码生成/转换支持：重点是 `TA -> SMT` 的编码转换，而非控制代码生成。
- 标准化或社区生态：`TACK`、`Zot` 背景、`Z3` solver、`TA` / `MITL` verification ecosystem。

## 适用场景与需求前提

### 适用场景

适合需要把 network of `TA` 与 `MITL` 性质做有界 `SMT` 验证的场景，尤其适合性质复杂、旧 `TA2CLTLoc` 编码已成为性能瓶颈的实时系统模型。

### 需求前提

1. 系统需能落成 finite network of `TA`。
2. 性质最好已写成 `MITL` 或可转到 `MITL`。
3. 关注 bounded lasso-shaped counterexample / witness，而不是无界完整判定。
4. 团队接受 `SMT`-based verification pipeline。

### 不适用或高成本场景

如果问题核心是完整无界证明、连续动力学、概率语义或层次状态图，本文方法就不是最自然的主入口。

## 与相邻形式主义的关系

相对 [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)，`KRONOS` 是经典 symbolic timed-model-checking platform，而本文是 `SMT/BMC` 编码改进路线；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 更偏成熟平台与 zone-based verification，而本文强调 bounded `SMT` encoding；相对 [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)，`nuXmv` 是同步 transition systems 的 symbolic backend，本文则专注 `TA` 网络的 solver-facing encoding。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明当目标模型带时间约束时，验证后端不仅可选 zone-based，也可选 `SMT/BMC` 路线。
2. 对“生成 - 验证 - 修复”闭环来说，solver-friendly encoding 直接影响验证速度和反例可得性。
3. 变量、broadcast 和 interval edge 这些细节会强烈影响自动验证可用性，生成阶段就应尽量保留。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Timed Automata` 是可选目标形式主义，而 `TA2SMT` 更像验证阶段的方法后端。

### 对需求到模型生成的启发

1. 需求中的时钟、变量和同步模式若能早期结构化，后续更容易自动编码到求解器。
2. 一个好的验证管线不只是逻辑正确，还要关注 encoding 颗粒度。
3. 若后续要做自动修复，solver 级反例和边界条件支持往往比单纯 reachability 更关键。

## 重要的相关工作

1. [kronos-a-model-checking-tool-for-real-time-systems/desc.md](../kronos-a-model-checking-tool-for-real-time-systems/desc.md)：经典 timed-automata symbolic verifier。
2. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：主流 `Timed Automata` 平台与 zone-based workflow。
3. [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)：`SAT/SMT`-enabled symbolic backend 对照项。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / TACK / TA2SMT / BitVector-SMT bounded model checking`
- 论文角色：timed-automata bounded-model-checking method replacing TA2CLTLoc with direct TA2SMT encoding
- 核心功能：把 network of `TA` 直接编码为 BitVector/SMT 公式以提升 `TACK` 的 bounded verification 性能
- 关键特性：`TA2SMT`、transition BitVectors、location aliases、integer guards、broadcast fix、interval-edge support
- 构造方式：`TA network + MITL -> TA2SMT + property encoding -> SMT`
- 基础设施：`TACK`、`Z3`、bounded lasso-shaped traces、BitVector logic
- 适用场景：实时系统 `SMT/BMC` 验证、含变量和同步约束的 `TA` 网络检查
- 需求前提：系统需落成 finite `TA` network，性质适合 bounded `MITL` verification
- 状态：🟢
