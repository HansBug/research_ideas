# 用 Neco 做 LTL 模型检查 / LTL Model Checking with Neco

## 基本信息

- 标题：LTL Model Checking with Neco
- 中文标题：用 Neco 做 LTL 模型检查
- 作者：Łukasz Fronc，Alexandre Duret-Lutz
- 发表：*Automated Technology for Verification and Analysis (ATVA 2013)*，LNCS 8172，pp. 451-454，2013
- DOI：`10.1007/978-3-319-02444-8_33`
- 链接：https://doi.org/10.1007/978-3-319-02444-8_33
- 形式主义：`High-Level Petri Nets / Neco / neco-spot / Spot TGBA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：`Neco + Spot` integration route for Petri-net `LTL` model checking
- 工具/实现获取方式：原文直接给出历史入口 `http://code.google.com/p/neco-net-compiler/`，并说明 `neco-spot` 建立在 `Neco` 与 `Spot` 之上；其中 `Spot` 是公开的 `C++` automata/model-checking 库。
- 标准/格式获取方式：输入承载是 `SNAKES`/`PNML` 风格 Petri net、编译出的 `net.so` exploration engine、`checker.so` atomic-proposition checker 与 `Spot` 公式文件；它不是中立交换标准。

## 简报

这篇论文的贡献，不是重讲一遍 `Neco` 编译器，而是把 `Neco` 原本的 reachability engine 和 `Spot` 的 automata-theoretic `LTL` algorithms 接起来，形成一个真正可用的 Petri-net `LTL` model-checking flow。它说明，只要能把自定义形式主义包装成 `Spot` 需要的 Kripke 接口，就能很快获得成熟的 `TGBA`、product 和 emptiness-checking 能力。

- 形式主义定位：Petri 网上的 `LTL` 检查方法/工具桥，而不是新的 Petri 网本体。
- 构造方式简述：`Neco` 先把高层 Petri 网编译成 exploration engine，再由 `neco-check` 生成 atomic-proposition checker，最后 `neco-spot` 把状态空间包装成 `Spot` 的 Kripke 接口并执行 product + emptiness check。
- 基础设施与场景简述：依托 `SNAKES`、`Neco`、`Spot`、`TGBA` 和按需状态空间探索，服务高层 Petri 网的 `LTL` 违例搜索。

```text
Petri net model -> neco-compile -> net.so exploration engine -> neco-check -> checker.so -> neco-spot + Spot TGBA -> LTL counterexample / satisfaction
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 高层 Petri 网模型。
2. `Neco` 编译得到的 `net.so` exploration engine。
3. `checker.so` atomic-proposition checker。
4. `Spot` 的 `TGBA` 与 emptiness-checking algorithms。
5. Kripke wrapper 与 on-the-fly product。

### 核心抽象

把 `Neco` 暴露给 `Spot` 的检查接口保守写成：

$$
\mathcal{K} = (S, s_0, R, L)
$$

上式中的符号逐项解释如下：

1. `S` 是 Petri 网可达标识集合。
2. `s_0` 是初始标识。
3. `R` 是由 `net.so` 的 successor functions 给出的后继关系。
4. `L : S \to 2^{AP}` 是 atomic proposition labelling，由 `checker.so` 负责。
5. 论文明确说明：`neco-spot` 的关键工作就是把 `Neco` 模型包装成 `Spot` 的 Kripke 接口。

论文中的 AP checker 接口可直接保守写成：

$$
\mathrm{check} : S \times AP \to \{\mathrm{true}, \mathrm{false}\}
$$

上式中的符号逐项解释如下：

1. `S` 是某个标识状态。
2. `AP` 是原子命题集合或其编号。
3. `check` 返回该状态是否满足指定原子命题。
4. 这正对应原文 `neco-check` 生成的 checker module。

对 automata-theoretic 检查流程，可压成：

$$
\mathcal{P} = \mathcal{K} \otimes \mathcal{A}_{\neg \varphi}
$$

上式中的符号逐项解释如下：

1. `\mathcal{K}` 是 Petri 网状态空间的 Kripke 表示。
2. `\mathcal{A}_{\neg \varphi}` 是 `Spot` 由 `\neg \varphi` 生成的 `TGBA`。
3. `\otimes` 是同步 product。
4. 若 `\mathcal{P}` 存在 accepting cycle，则得到 `LTL` counterexample。

### 一个最小例子与通俗解释

论文给出的最小用法很清晰：

1. 先用 `SNAKES` 或 `PNML` 写一个高层 Petri 网。
2. 运行 `neco-compile`，得到 `net.so`，它能按需给出后继。
3. 再给一条 `LTL` 公式，让 `neco-check` 生成 `checker.so`。
4. 最后 `neco-spot` 把 `net.so` 与 `checker.so` 接到 `Spot`，如果公式不成立，就输出 counterexample。

通俗地说，这像“给 Petri 网装上一个会按需展开状态空间的后端，再把它插到现成的 `LTL` 自动机库里”。这样既不用重写整套 `LTL` 算法，也保留了 `Neco` 高层 Petri 网编译的性能优势。

### 运行 / 接受 / 转移语义

从 `Neco` 一侧看，运行语义仍是 Petri 网 marking 的 successor expansion：

$$
Reach(N) = \mu Z.\ \{s_0\} \cup Succ(Z)
$$

上式中的符号逐项解释如下：

1. `N` 是输入 Petri 网。
2. `s_0` 是初始标识。
3. `Succ` 由 `net.so` 中的 successor functions 提供。
4. `\mu Z` 表示不断扩展直到到达最小不动点。

从 `Spot` 一侧看，接受语义则变成 product automaton 上的 emptiness：

$$
\mathcal{K} \models \varphi \iff Lang(\mathcal{P}) = \emptyset
$$

其中：

1. `\mathcal{P} = \mathcal{K} \otimes \mathcal{A}_{\neg \varphi}`。
2. `Lang(\mathcal{P}) = \emptyset` 表示不存在满足反公式的 accepting run。
3. 这正是 automata-theoretic `LTL` model checking 的核心。

### 语义边界

1. 论文的主线是 `LTL` checking，不是 general Petri verification 全景。
2. 高层 Petri 网表达能力取决于 `SNAKES/Neco` 前端，而不是 `Spot`。
3. 当模型 heavily 使用 Python 动态特性时，编译收益可能下降。
4. 这篇论文只有短篇幅，重点是 tool integration，不是完整 `Neco` 手册。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| Kripke 接口 | `$\mathcal{K} = (S, s_0, R, L)$` | `Neco` 暴露给 `Spot` 的统一状态空间对象。 |
| AP 检查器 | `$\mathrm{check} : S \times AP \to \{\mathrm{true}, \mathrm{false}\}$` | `checker.so` 的核心职责。 |
| product 检查 | `$\mathcal{P} = \mathcal{K} \otimes \mathcal{A}_{\neg \varphi}$` | Petri 网与 `LTL` 自动机同步。 |
| emptiness 判定 | `$\mathcal{K} \models \varphi \iff Lang(\mathcal{P}) = \emptyset$` | 是否存在违例 accepting run。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 核心状态是 Petri 网 marking。 |
| 事件 / 触发 | 中等支持 | 通过 Petri 迁移 firing 体现。 |
| 守卫 / 数据 | 强支持 | 继承高层 Petri 网和 `SNAKES` 的表达力。 |
| 层次 | 不适用 | 不是层次状态机路线。 |
| 并发 / 同步 | 很强 | Petri 网与 `LTL` product 双重体现并发结构。 |
| 时间约束 | 不支持 | 本文不处理 timed nets。 |
| 连续动态 / 随机性 | 不支持 | 主线是离散 `LTL` checking。 |
| 可执行 / 可验证性 | 很强 | `Neco` 编译 + `Spot` 算法形成完整工具链。 |

### 形式化问题与性质

1. 论文最有价值的部分是“如何把自定义形式主义包装成 `Spot` 的 Kripke front-end”。
2. `Neco` 负责高效状态空间生成，`Spot` 负责 automata-theoretic `LTL` 核心算法，两者分工清晰。
3. 这是一条很典型的“形式主义专用前端 + 通用后端算法库”的基础设施路线。

## 构造方式与承载格式

### 建模入口

论文中的主要建模入口包括：

1. `SNAKES` 程序化 Petri 网。
2. `PNML` 或其他 `Neco` 支持的前端表示。
3. `LTL` 公式文件。
4. `neco-compile`、`neco-check`、`neco-spot` 三段式工作流。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `net.so` exploration engine。
2. `checker.so` atomic-proposition checker。
3. `Spot` formula / automaton objects。
4. compilation trace metadata。

### 交换与互操作

1. `Neco` 把 Petri 网编译成共享库接口。
2. `Spot` 提供 `TGBA`、product 与 emptiness-checking 算法。
3. 两者通过 Kripke wrapper 与 AP checker glue code 完成互操作。

## 配套基础设施

- 建模/编辑工具：`SNAKES`、`PNML` 输入与 `Neco` 编译前端。
- 解析/交换/元模型支持：compilation trace、marking structure 元数据和 AP 编号映射。
- 仿真/执行支持：`net.so` 负责 on-the-fly state-space exploration。
- 验证/分析支持：`Spot` 负责 `TGBA` 构造、product 和 emptiness check。
- 代码生成/转换支持：`Neco` 把 Petri 网编译成 native shared libraries。
- 标准化或社区生态：与 `Neco`、`SNAKES`、`Spot` 三条开源工具线直接相连。

## 适用场景与需求前提

### 适用场景

适合需要在高层 Petri 网模型上做 `LTL` 违例搜索、又希望复用成熟 automata-theoretic backend 的场景，尤其适合研究型 Petri verification tooling。

### 需求前提

1. 系统需能自然建模成高层 Petri 网。
2. 关心的性质适合表达成 `LTL`。
3. 团队接受编译式 exploration engine + library backend 的工作流。

### 不适用或高成本场景

如果需求主体是 timed / stochastic / hybrid Petri nets，或需要图形建模 IDE，而不是 `LTL` checking，本条目收益会下降。

## 与相邻形式主义的关系

相对 [building-petri-nets-tools-around-neco-compiler/desc.md](../building-petri-nets-tools-around-neco-compiler/desc.md)，本文更聚焦 `LTL` integration 而不是 `Neco` 整体编译器骨架；相对 [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)，这里展示的是 `Spot` 作为后端库的一个具体 Petri 用例；相对 [quickly-prototyping-petri-nets-tools-with-snakes/desc.md](../quickly-prototyping-petri-nets-tools-with-snakes/desc.md)，`SNAKES` 负责高层表达，而 `Neco + Spot` 把它推向高性能检查。

## 与本研究的关系

### 对 Project 1 的价值

1. 它很好地说明了“前端形式主义保留自身表达力，后端算法尽量复用成熟库”这条工程模式。
2. 对 `project_1` 来说，这意味着 LLM 生成的中间模型不一定要直接面向最终求解器，可以先通过 glue layer 接入成熟 backend。
3. 若未来某些状态机族需要 `LTL` 检查，这篇论文提供了很清楚的 architecture 模板。

### 作为目标形式主义还是中间表示

更像 Petri-net verification toolchain 的中间层与方法桥，而不是目标建模语言。

### 对需求到模型生成的启发

1. 如果目标形式主义已有高质量后端库，不要重复造轮子，优先做适配层。
2. 把状态空间生成和时序性质算法分离，有利于后续验证/修复闭环复用。

### 现实限制

文章篇幅很短，很多 `Neco` 编译细节需要结合其基础编译器论文一起看，单读本文更适合把握桥接架构而不是全部实现细节。

## 重要的相关工作

1. [building-petri-nets-tools-around-neco-compiler/desc.md](../building-petri-nets-tools-around-neco-compiler/desc.md)：`Neco` 编译器总体骨架。
2. [quickly-prototyping-petri-nets-tools-with-snakes/desc.md](../quickly-prototyping-petri-nets-tools-with-snakes/desc.md)：高层 Petri 前端 `SNAKES`。
3. [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)：`Spot` 的 automata-based backend。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
