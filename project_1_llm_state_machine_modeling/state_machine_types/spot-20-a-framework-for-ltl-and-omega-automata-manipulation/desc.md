# Spot 2.0：LTL 与 Omega 自动机操作框架 / Spot 2.0: A Framework for LTL and Omega-Automata Manipulation

## 基本信息

- 标题：Spot 2.0 - A Framework for LTL and Omega-Automata Manipulation
- 中文标题：Spot 2.0：LTL 与 Omega 自动机操作框架
- 作者：Alexandre Duret-Lutz，Alexandre Lewkowicz，Amaury Fauchille，Thibaud Michaud，Etienne Renault，Laurent Xu
- 发表：*Automated Technology for Verification and Analysis*，pp. 122-129，2016
- DOI：`10.1007/978-3-319-46520-3_8`
- 链接：https://doi.org/10.1007/978-3-319-46520-3_8
- 形式主义：`LTL / omega-automata / Spot`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`LTL` 与 `omega` 自动机操作库 / translator-toolchain framework
- 工具/实现获取方式：原文明确给出 `https://spot.lrde.epita.fr/` 作为下载入口，并给出 `http://spot-sandbox.lrde.epita.fr/` 作为可直接重放示例的在线 `Jupyter` 环境。
- 标准/格式获取方式：原文明确说明 `Spot 2.0` 默认以 `HOA` 作为自动机交换格式，并同时提供 `C++` 库、Python bindings 与命令行工具链；它不是独立标准本体，而是围绕 `HOA` 组织的操作基础设施。

## 简报

这篇论文的重点，不是提出新的 `omega` 自动机母型，而是把 `LTL` 公式处理、`omega` 自动机构造、格式转换、等价检查、交叉测试和脚本化实验整合成一套真正可复用的工具链。`Spot 2.0` 最大的工程增量，是把 arbitrary acceptance conditions、`HOA`、`C++` 核心库、命令行流水线和 Python/Jupyter 交互环境打通。

- 形式主义定位：`LTL -> omega-automata` 的工具与执行载体，而不是新的自动机定义论文。
- 构造方式简述：围绕 `libspot`、`libbddx`、`libspot-ltsmin` 三层库，向上暴露 `ltl2tgba / autfilt / ltldo / randaut` 等命令行工具与 Python API。
- 基础设施与场景简述：依托 `HOA`、命令行 pipeline、Jupyter notebook 和 `LTSmin` 接口，服务 `LTL/PSL` 翻译、自动机过滤/变换、显式模型检查实验和教学演示。

```text
LTL/PSL formula -> Spot parser/translator -> HOA automaton -> autfilt/ltldo/Python APIs -> model checking / transformation / teaching workflow
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `Spot 2.0`：

1. `LTL / PSL` 公式对象。
2. `omega` 自动机及其多种 acceptance conditions。
3. `HOA` 交换格式。
4. `C++` 核心库、命令行工具与 Python bindings。
5. `LTSmin` 接口与 on-the-fly explicit model checking workflow。

### 核心抽象

论文最直接的形式化内容，是把接受条件统一成对 `Inf/Fin` 原语的布尔组合。可写成：

$$
Acc ::= Inf(n) \mid Fin(n) \mid Acc \land Acc \mid Acc \lor Acc
$$

上式中的符号逐项解释如下：

1. `n` 是某个 acceptance set 的编号。
2. `Inf(n)` 表示该 acceptance set 被访问无穷多次。
3. `Fin(n)` 表示该 acceptance set 只被访问有限次。
4. `\land` 与 `\lor` 分别表示布尔合取与析取。
5. 论文强调 `Spot 2.0` 之所以能统一支持 `Buchi / generalized Buchi / Rabin / Streett / parity`，关键就在这层 acceptance-agnostic 表示。

论文列出了几类经典接受条件在该语法下的写法：

$$
\text{Buchi}: Inf(0), \qquad
\text{generalized Buchi}: Inf(0) \land Inf(1) \land \cdots
$$

$$
\text{co-Buchi}: Fin(0), \qquad
\text{Rabin}: (Fin(0)\land Inf(1)) \lor (Fin(2)\land Inf(3)) \lor \cdots
$$

上式中的符号逐项解释如下：

1. `Buchi` 只要求某个 acceptance set 无穷多次命中。
2. generalized `Buchi` 要求多个 acceptance sets 都无穷多次命中。
3. `co-Buchi` 要求某个 set 只被有限次访问。
4. `Rabin` 用若干 `(Fin, Inf)` 对的析取来表达更强的接受条件。
5. `Spot 2.0` 的很多过滤和转换算法，正是建立在对这些统一公式的处理之上。

从工具架构角度，可把论文中的 `Spot 2.0` 保守整理为：

$$
\mathrm{Spot} = (\mathrm{libbddx}, \mathrm{libspot}, \mathrm{libspot\text{-}ltsmin}, \mathcal{T}, \mathcal{P})
$$

上式中的符号逐项解释如下：

1. `libbddx` 是自定义 `BDD` 支撑层。
2. `libspot` 是主要数据结构与算法库。
3. `libspot-ltsmin` 是与 `LTSmin` 共享库状态空间接口对接的桥接层。
4. `\mathcal{T}` 表示 `randltl / genltl / ltlfilt / ltl2tgba / autfilt / ltldo` 等命令行工具集合。
5. `\mathcal{P}` 表示 Python bindings 及其在 `IPython/Jupyter` 中的交互入口。

### 一个最小例子与通俗解释

论文给了一个很直观的管线例子：

```text
spin -f '[]<>a' | autfilt --complement --dot=abr | dot -Tpng
```

它表达的是：

1. 先把 `GF a` 这样的 `LTL` 公式交给 `Spin` 翻成 `Buchi` 自动机。
2. 再把输出交给 `autfilt` 做补运算与格式转换。
3. 最后用 `dot` 画出图。

通俗地说，`Spot` 像“自动机实验室里的通用扳手箱”。你不必重新写一个 LTL translator、一个 automata filter、一个 format converter，再单独拼脚本，而是直接把这些操作当 Unix 管线或 Python 函数组合起来。

### 运行 / 接受 / 转移语义

论文在 Python 侧展示了经典 automata-theoretic model checking 流程，可保守整理为：

$$
\mathcal{K}_\varphi = \mathcal{K} \otimes \mathcal{A}_{\neg \varphi}
$$

上式中的符号逐项解释如下：

1. `\mathcal{K}` 是由 `LTSmin` 或其他前端给出的 Kripke structure。
2. `\varphi` 是待验证的 `LTL` 公式。
3. `\mathcal{A}_{\neg \varphi}` 是 `Spot` 把 `\neg \varphi` 翻出来的 `omega` 自动机。
4. `\otimes` 表示 on-the-fly product。
5. 论文指出 `otfproduct()` 与 emptiness check 组合即可完成显式 `LTL` 模型检查。

对应接受判定，可压成：

$$
\mathcal{K} \models \varphi \iff L(\mathcal{K}) \cap L(\mathcal{A}_{\neg \varphi}) = \emptyset
$$

上式中的符号逐项解释如下：

1. `L(\mathcal{K})` 表示 Kripke structure 的行为语言。
2. `L(\mathcal{A}_{\neg \varphi})` 表示违反性质的运行集合。
3. 交集为空就表示模型满足性质。
4. 这是论文示例 notebook 中“翻否定、做积、查空”的理论底盘。

### 语义边界

这篇论文的边界也很清楚：

1. 它是 `LTL/omega-automata` 操作与模型检查支撑库，不是 timed、hybrid 或 probabilistic automata 的统一平台。
2. `Spot 2.0` 很强，但并不替代实际模型检查器或系统建模语言前端。
3. 一些算法虽然支持 arbitrary acceptance，但少数核心操作仍需先把 acceptance 约化到更受限的形式。
4. 它擅长“公式与自动机处理”，不直接提供像 `UML/SCXML` 那样的控制建模语言入口。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 接受条件统一语法 | `$Acc ::= Inf(n) \mid Fin(n) \mid Acc \land Acc \mid Acc \lor Acc$` | arbitrary acceptance 的统一表示基础。 |
| Buchi / Rabin 映射 | `$Inf(0)$`、`$(Fin(0)\land Inf(1)) \lor \cdots$` | 说明经典 acceptance families 如何归一化。 |
| 工具架构 | `$\mathrm{Spot} = (\mathrm{libbddx}, \mathrm{libspot}, \mathrm{libspot\text{-}ltsmin}, \mathcal{T}, \mathcal{P})$` | 论文明确的三层库 + 两层接口结构。 |
| 经典模型检查规约 | `$\mathcal{K} \models \varphi \iff L(\mathcal{K}) \cap L(\mathcal{A}_{\neg \varphi}) = \emptyset$` | Python / Jupyter 示例背后的理论主线。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 `omega` 自动机对象工作。 |
| 事件 / 触发 | 中等支持 | 主要通过命题标签和公式翻译体现，不是事件驱动控制语言。 |
| 守卫 / 数据 | 弱支持 | 没有富数据守卫语义。 |
| 层次 | 不支持 | 不处理层次状态机本体。 |
| 并发 / 同步 | 间接支持 | 可配合外部 Kripke/LTS 前端做模型检查，但不直接提供并发建模 DSL。 |
| 时间约束 | 不支持 | 非 timed family。 |
| 连续动态 / 随机性 | 不支持 | 主线是离散逻辑与 `omega` 自动机。 |
| 可执行 / 可验证性 | 很强 | 支持翻译、过滤、等价/包含检查、on-the-fly emptiness 与教学实验。 |

### 形式化问题与性质

1. `Spot 2.0` 把 acceptance conditions 的复杂性从“工具各自硬编码”转成“统一布尔语法 + 通用算法接口”。
2. 它既能做批处理流水线，也能做 notebook 级交互实验，这对教学和研究都很关键。
3. 与只提供一个 translator 的工具不同，它真正覆盖了 parse、translate、filter、compare、compose 这条完整链。

## 构造方式与承载格式

### 建模入口

原文给出三种主要入口：

1. `C++` 库接口；
2. shell 命令行工具；
3. Python bindings + `IPython/Jupyter`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `HOA` 默认格式；
2. `LBTT`、never claims、`ltl2dstar` 格式等输入输出；
3. `dot` 图可视化格式；
4. `LTSmin` shared library state spaces。

### 交换与互操作

互操作是这篇论文的核心价值之一：

1. `HOA` 让 `Spot` 能和其他 translator / model checker 做 acceptance-agnostic 交换。
2. `ltldo` 把第三方 translator 包成统一输入输出界面。
3. `libspot-ltsmin` 让显式状态空间可直接进入 automata-theoretic checking workflow。

## 配套基础设施

- 建模/编辑工具：主体不是图形建模器，而是 `C++` / Python / CLI 三层开发入口。
- 解析/交换/元模型支持：`HOA`、never claims、`LBTT`、`ltl2dstar` 格式与 `dot` 导出。
- 仿真/执行支持：不以系统仿真为主，但可在 notebook 中交互式构造、过滤和检查自动机。
- 验证/分析支持：`ltl2tgba`、`autfilt`、emptiness、language inclusion、equivalence、determinization、minimization 等。
- 代码生成/转换支持：支持公式到自动机、自动机到自动机、格式到格式的系统性转换。
- 标准化或社区生态：官网、在线 sandbox、Python notebook 支持与 `HOA`/`LTSmin`/`Spin` 等外部生态共同组成长期工具链。

## 适用场景与需求前提

### 适用场景

适合 `LTL/PSL` 翻译、`omega` 自动机比较与过滤、acceptance-condition 实验、显式模型检查原型、课程教学与算法对比实验。

### 需求前提

1. 核心对象能表成 `LTL/PSL` 或 `omega` 自动机。
2. 工作重心是公式和自动机处理，而不是完整系统前端建模。
3. 团队愿意接受 `C++`、命令行或 Python notebook 作为工作入口。
4. 若要做完整模型检查，还需要外部 Kripke/LTS 前端或显式状态空间接口。

### 不适用或高成本场景

如果目标是直接从控制需求生成 `UML/SCXML` 状态机或处理 rich data/timing semantics，`Spot 2.0` 更像后端理论工具，而不是最终执行载体。

## 与相邻形式主义的关系

相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，`HOA` 是交换标准本身，而 `Spot 2.0` 是把这层标准真正做活的操作者具；相对 [openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md](../openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md)，两者都是自动机算法库，但 `OpenFst` 面向加权有限状态转导，`Spot` 面向 `LTL/omega-automata`；相对 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，`LearnLib` 关心黑盒学习流程，而 `Spot` 关心已给定公式/自动机的构造、过滤和验证。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明“标准交换格式 + 通用操作库 + 脚本/交互环境”是状态机工具链成熟的关键组合。
2. 若后续要把需求生成的时序性质或行为约束翻成 `omega` 自动机做验证，`Spot` 是极强的后端资产。
3. 它也提示 `project_1`：模型本体之外，围绕模型的 translator/filter/checker 基础设施同样决定闭环是否可落地。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它显然更像后端中间工具层，而不是最终状态机交付形式。

## 重要的相关工作

- [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：`Spot 2.0` 默认围绕它组织互操作。
- [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)：`PRISM` 等消费端可通过 `omega` 自动机接口复用这一工具链。
- [openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md](../openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md)：可对照“自动机族库”在不同理论对象上的工程化路径。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`LTL / omega-automata / Spot`
- 论文角色：`LTL` 与 `omega` 自动机操作库 / translator-toolchain framework
- 核心功能：统一 `LTL` 翻译、`omega` 自动机过滤/转换、`HOA` 互操作与 notebook 级实验环境
- 关键特性：arbitrary acceptance、`HOA`、CLI pipeline、Python bindings、`LTSmin` bridge
- 构造方式：`C++` core libraries + command-line tools + Python notebook interfaces
- 基础设施：`libbddx`、`libspot`、`libspot-ltsmin`、`ltl2tgba`、`autfilt`、`ltldo`
- 适用场景：`LTL/PSL` 翻译、`omega` 自动机实验、显式模型检查前端集成与教学
- 需求前提：对象需能落成 `LTL/PSL` 或 `omega` 自动机，且团队接受工具链式工作流
- 状态：🟢
