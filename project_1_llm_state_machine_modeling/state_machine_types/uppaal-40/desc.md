# UPPAAL 4.0：定时自动机验证平台 4.0 / UPPAAL 4.0

## 基本信息

- 标题：UPPAAL 4.0
- 中文标题：UPPAAL 4.0：定时自动机验证平台 4.0
- 作者：Gerd Behrmann，Alexandre David，Kim G. Larsen，John Håkansson，Paul Pettersson，Wang Yi，Martijn Hendriks
- 发表：*Third International Conference on the Quantitative Evaluation of Systems (QEST 2006)*，pp. 125-126，2006
- DOI：`10.1109/QEST.2006.59`
- 链接：https://user.it.uu.se/~wangyi/pdf-files/qest06.pdf
- 形式主义：`Timed Automata / UPPAAL 4.0`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-automata verification workbench / major tool release
- 工具/实现获取方式：原文明确说明 `UPPAAL 4.0` 与若干开源库可从 `http://www.uppaal.com/` 免费下载，用于 academic / educational / evaluation purposes。
- 标准/格式获取方式：承载方式沿用 `UPPAAL` 的 declarations + templates + locations/edges + query language，同时新增 user-defined functions、channel / automaton priorities 与 scalar datatype；原文未引入独立中立交换标准。

## 简报

这篇论文不是再解释 timed automata 理论，而是把 `UPPAAL` 推进到一个更成熟的工程版本。其核心增量有三条：把复杂更新逻辑压进**原子用户函数**、把资源竞争和调度顺序压进**显式优先级**、把同构进程场景压进**自动对称性约减**。这三条直接解决了“模型图太脏、状态空间太大、共享资源语义不清”的老问题。

- 形式主义定位：`UPPAAL` 的平台级 release 论文，重点在 timed-automata tooling，而不是 timed automata 母模型本体。
- 构造方式简述：继续使用 network of timed automata，但把复杂更新写成 C 风格 deterministic functions，把同步冲突写成 channel / automaton priorities。
- 基础设施与场景简述：依托 graphical editor、byte-code stack machine、`DBM` library、parser library 与 symmetry reduction，服务实时协议、嵌入式控制、调度与互斥验证。

```text
timed automata network -> UPPAAL declarations/templates -> functions + priorities + scalar sets -> DBM/state-space exploration -> verification / diagnostics
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. network of timed automata；
2. user-defined functions；
3. channel priorities 与 automaton priorities；
4. scalar datatype 与 symmetry reduction；
5. `DBM` / parser libraries。

### 核心抽象

对 `UPPAAL 4.0` 而言，基础建模对象仍可保守写成：

$$ A = (L, \ell_0, C, V, E, Inv) $$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `\ell_0` 是初始 location。
3. `C` 是 clock 集合。
4. `V` 是 bounded discrete variables。
5. `E` 是边集合，每条边可携带 guard、synchronisation 与 update。
6. `Inv` 是 location invariants。

组合系统则写成：

$$ N = A_1 \parallel A_2 \parallel \cdots \parallel A_n $$

上式中的符号逐项解释如下：

1. `A_i` 是单个 timed automaton template 的实例。
2. `\parallel` 表示 network composition。
3. `N` 是 `UPPAAL` 实际探索的全局状态机。

`UPPAAL 4.0` 新增的函数机制可保守整理为：

$$ f : Val(V) \to Val(V) $$

上式中的符号逐项解释如下：

1. `Val(V)` 是当前离散变量赋值。
2. `f` 是原文中的 user-defined function。
3. 函数在语义上被当作**原子且确定**的更新，不产生中间状态。

优先级语义可保守整理为：

$$ Enabled_{\prec}(s) = \{\, t \in Enabled(s) \mid \nexists t' \in Enabled(s): t \prec t' \,\} $$

上式中的符号逐项解释如下：

1. `Enabled(s)` 是状态 `s` 下所有已使能迁移。
2. `\prec` 是原文中的 total priority order。
3. `Enabled_{\prec}(s)` 是在优先级屏蔽后真正允许执行的迁移集合。

### 一个最小例子与通俗解释

论文直接给了最小优先级语法：

```uppaal
chan priority a < b, c;
system P < Q, R;
```

它表达的是：

1. 若 `a`、`b`、`c` 同时可触发，则 `b`、`c` 先于 `a`。
2. 若 channel priority 相同，再比较 automata priority，`Q`、`R` 先于 `P`。
3. 因而共享资源上的竞争顺序不必再靠“补一堆中间状态”来编码。

通俗地说，`UPPAAL 4.0` 做的事情很像把“图上的技巧活”变回“语言里的正规构造”：复杂更新塞进函数，竞争顺序塞进 priority，进程置换对称性交给工具自动消化。

### 运行 / 接受 / 转移语义

`UPPAAL` 的基本运行仍是 delay / action 两类步骤：

$$ (\ell, \nu) \xrightarrow{d} (\ell, \nu + d) $$

$$ (\ell, \nu) \xrightarrow{a} (\ell', \nu') $$

上式中的符号逐项解释如下：

1. `\ell`、`\ell'` 是离散位置。
2. `\nu`、`\nu'` 是当前时钟赋值。
3. `d` 是非负延时。
4. `a` 是同步动作或内部动作。
5. 第二条式子要求 guard 满足，且执行 update / reset。

在 `UPPAAL 4.0` 中，若某条动作边携带函数调用，则其更新可写成：

$$ \nu' = \nu[X := 0], \quad v' = f(v) $$

上式中的符号逐项解释如下：

1. `X := 0` 表示对若干 clocks 做 reset。
2. `v`、`v'` 是离散变量赋值。
3. `f(v)` 是原子执行的用户函数结果。

### 语义边界

1. user-defined functions 必须 deterministic，且不允许 recursion。
2. 函数若进入无限循环，工具不会终止；原文明确说当前版本不自动检查这一点。
3. scalar datatype 只支持同类型赋值、等值测试与同型数组索引，用于保障 symmetry reduction 的安全性。
4. 这篇论文是 release paper，因此更强调语言与引擎变化，不重讲完整 timed-automata 语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础模型骨架 | `$A = (L, \ell_0, C, V, E, Inv)$` | `UPPAAL` 继续围绕 timed automata network 工作。 |
| 网络组合 | `$N = A_1 \parallel \cdots \parallel A_n$` | 实际验证对象仍是并行组合系统。 |
| 原子函数更新 | `$f : Val(V) \to Val(V)$` | 复杂离散更新不再需要展开成一串 committed states。 |
| 优先级筛选 | `$Enabled_{\prec}(s) = \{ t \in Enabled(s) \mid \nexists t': t \prec t' \}$` | 明确谁能屏蔽谁。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍以 timed automata locations/network 为核心。 |
| 事件 / 触发 | 很强 | channels、synchronisation 与 priority 都是主线。 |
| 守卫 / 数据 | 很强 | guards、bounded data、原子函数更新都支持。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 很强 | network composition 与 shared channels 是基础能力。 |
| 时间约束 | 很强 | `DBM` zone exploration 是核心引擎。 |
| 连续动态 / 随机性 | 不支持 | 不面向 hybrid / stochastic semantics。 |
| 可执行 / 可验证性 | 很强 | GUI、libraries、symmetry reduction 与性能优化都到位。 |

### 形式化问题与性质

1. `UPPAAL 4.0` 的主要价值不是新模型，而是“把常见建模绕法吸收到语言层”。
2. user-defined functions 降低了 graph clutter，也减少了因中间位置带来的无关交错。
3. priorities 与 scalar sets 分别瞄准共享资源竞争和对称进程爆炸这两类工程痛点。

## 构造方式与承载格式

### 建模入口

原文给出的建模入口有：

1. 图形 editor 中的 templates、locations、edges；
2. declarations 区里的 clocks、bounded data、user-defined functions；
3. channel / automaton priority declarations；
4. scalar datatype declarations。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` model declarations 与 templates；
2. C 风格 byte-code compiled functions；
3. `DBM`-based zone representation；
4. parser library 与独立 `DBM` library。

### 交换与互操作

互操作重点不在中立交换格式，而在可复用库：

1. `DBM` library 被单独开放出来。
2. parser library 也可独立复用。
3. 这意味着 `UPPAAL` 不只是 GUI 工具，而是可嵌入的 timed-analysis backend。

## 配套基础设施

- 建模/编辑工具：强化后的 graphical editor，继续保持易用的 timed-automata 建模入口。
- 解析/交换/元模型支持：parser library、模型语言声明区、函数字节码与 priority declarations。
- 仿真/执行支持：延续 `UPPAAL` simulator / verifier 路线。
- 验证/分析支持：`DBM` zone exploration、priority handling、symmetry reduction、memory optimization。
- 代码生成/转换支持：原文不主打代码生成；重点是建模语言和验证后端。
- 标准化或社区生态：`UPPAAL` 主站、开源 `DBM` / parser libraries 与长期 case-study 生态。

## 适用场景与需求前提

### 适用场景

适合实时协议、嵌入式控制、互斥与调度分析，以及那些既有 clocks，又有复杂 bounded-data 更新的 timed models。

### 需求前提

1. 时间行为仍能压成 timed automata，而不是连续动力学。
2. 复杂更新逻辑必须保持 deterministic 且 bounded。
3. 若想吃到 symmetry reduction 红利，系统里需要存在真正的 process symmetry。

### 不适用或高成本场景

如果需求主要依赖概率、连续微分方程或富层次结构，`UPPAAL 4.0` 仍不是直接答案；此时要转向 `PRISM`、hybrid tools 或 statechart-family tools。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，教程论文更像 timed-automata language manual，而本文更像一次平台升级说明；相对 [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)，`UPPAAL-Tiga` 把 timed games 做成求解器，而本文补的是 `UPPAAL` 主平台本身的语言与库；相对 [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)，`UPPAAL-SMC` 补的是统计分析路线，而本文补的是核心建模/状态空间引擎升级。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机建模语言要不要把复杂更新、优先级和对称结构作为一等公民”会直接决定可用性。
2. 如果后续 `project_1` 要把自然语言需求落成 timed model，`function / priority / scalar-set` 这三类构造都值得作为目标语言选择时的重要考量。
3. 对“生成-验证-修复”闭环来说，`DBM` / parser libraries 这种可复用底层很有参考价值。

### 局限

1. 本文不是 timed automata 定义论文，因此形式主义本体部分必须回看更早文献。
2. 它仍然不覆盖概率、混成和层次状态机语义。

## 重要的相关工作

- [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：`UPPAAL` 经典语言与工具教程基线。
- [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)：`UPPAAL` 生态里的 timed-game synthesis 线。
- [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)：概率/统计扩展线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 timed-automata 平台升级条目，适合作为 `UPPAAL` 主平台语言与底层库演化的基础设施证据入账。
