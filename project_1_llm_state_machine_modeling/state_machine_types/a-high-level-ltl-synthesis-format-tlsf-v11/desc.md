# 高层 LTL 综合格式：TLSF v1.1 / A High-Level LTL Synthesis Format: TLSF v1.1

## 基本信息

- 标题：A High-Level LTL Synthesis Format: TLSF v1.1
- 中文标题：高层 LTL 综合格式：TLSF v1.1
- 作者：Swen Jacobs，Felix Klein，Sebastian Schirmer
- 发表：*Electronic Proceedings in Theoretical Computer Science*，Vol. 229，pp. 112-132，2016
- DOI：`10.4204/EPTCS.229.10`
- 链接：https://doi.org/10.4204/EPTCS.229.10
- 形式主义：`TLSF / SyFCo / LTL synthesis specification format`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：高层 `LTL` 反应式综合规格格式与 `SyFCo` 转换工具
- 工具/实现获取方式：原文明确给出 `SyFCo` 作为 `TLSF` 转换工具；当前公开入口可见 `https://github.com/reactive-systems/syfco`。
- 标准/格式获取方式：论文本体定义 `TLSF v1.1` 语法与语义；benchmark 与格式资料由 `SYNTCOMP` / `TLSF` 生态持续维护。

## 简报

这篇论文解决的不是“怎么综合”，而是“综合问题该如何稳定地表达、交换和复现实验”。`TLSF` 的贡献，在于把原本分散在 `AIGER`、各家私有语法和 benchmark 脚本里的 synthesis specification，统一成一个既适合人写、又可以自动降编到 basic `LTL` 或其他后端格式的高层载体。它把输入输出分区、假设/保证结构、参数化族、枚举和函数这些综合工作流里真正需要的东西，都固定到了一个标准规格层。

- 形式主义定位：反应式综合规格格式，不是新的自动机母型或新的求解器。
- 构造方式简述：用户编写 full `TLSF` 规格，`SyFCo` 负责展开参数、函数和语法糖，并降到 basic `TLSF` 或其他后端可消费格式。
- 基础设施与场景简述：依托 `TLSF`、`SyFCo`、`SYNTCOMP` benchmark、`Mealy/Moore` 语义选项与 strict implication，服务 `LTL` synthesis 的标准化输入层。

```text
high-level synthesis specification -> TLSF -> SyFCo lowering / conversion -> plain LTL or solver-specific format -> synthesis backend
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `TLSF` 的 `INFO / GLOBAL / MAIN` 结构。
2. 输入输出分区与 assumption / guarantee 风格规格。
3. `Mealy / Moore` target 与 standard / strict semantics。
4. 参数、枚举、函数、big operators 等高层语法。
5. `SyFCo` 转换工具与 benchmark 工作流。

### 核心抽象

对综合规格本体，可按正文结构保守整理为：

$$
\mathcal T = (I, O, \theta_e, \theta_s, \psi_e, \psi_s, \varphi_e, \varphi_s)
$$

上式中的符号逐项解释如下：

1. `I` 是输入信号集合。
2. `O` 是输出信号集合。
3. `\theta_e` 和 `\theta_s` 分别对应 `INITIALLY` 与 `PRESET`。
4. `\psi_e` 和 `\psi_s` 分别对应 `REQUIRE` 与 `ASSERT`。
5. `\varphi_e` 和 `\varphi_s` 分别对应 `ASSUME` 与 `GUARANTEE`。
6. 这不是论文显式统一元组，而是把 `MAIN` 区域直接压缩成后续语义公式会用到的对象。

论文直接给出 basic `LTL` expression grammar：

$$
\varphi' := true \mid false \mid s \mid !\varphi \mid \varphi \land \varphi \mid \varphi \lor \varphi \mid \varphi \rightarrow \varphi \mid \varphi \leftrightarrow \varphi \mid X\varphi \mid G\varphi \mid F\varphi \mid \varphi U \varphi \mid \varphi R \varphi \mid \varphi W \varphi
$$

上式中的符号逐项解释如下：

1. `s` 是输入或输出信号。
2. `!`、`\land`、`\lor`、`\rightarrow`、`\leftrightarrow` 是布尔连接词。
3. `X`、`G`、`F`、`U`、`R`、`W` 是时序算子。
4. 这正是论文给出的 basic format 语法核心。

论文附录还明确给出目标实现模型：

$$
Me = (I, O, Q, q_0, \delta, \lambda_e), \qquad Mo = (I, O, Q, q_0, \delta, \lambda_o)
$$

上式中的符号逐项解释如下：

1. `Me` 是 `Mealy` automaton。
2. `Mo` 是 `Moore` automaton。
3. `Q` 是状态集合，`q_0` 是初始状态。
4. `\delta` 是状态转移函数。
5. `\lambda_e : Q \times I \to O` 表示 `Mealy` 输出依赖当前状态和当前输入。
6. `\lambda_o : Q \to O` 表示 `Moore` 输出只依赖当前状态。

### 一个最小例子与通俗解释

顺着论文给出的 basic format，一个最小 `TLSF` 规格可以写成：

```text
INFO {
  TITLE: "toy"
  SEMANTICS: Mealy
  TARGET: Mealy
}
MAIN {
  INPUTS { req; }
  OUTPUTS { grant; }
  GUARANTEE { G(req -> F grant); }
}
```

这个例子的直觉是：

1. 环境只有一个输入 `req`。
2. 系统只有一个输出 `grant`。
3. 目标是综合一个控制器，使得只要请求出现，未来最终必须发出授权。

通俗地说，`TLSF` 的价值就是把“要综合的东西到底是什么”写清楚。它不像 `AIGER` 那样一开始就把问题压成电路级游戏，而是在更高层保留输入输出、假设保证和参数化结构，让 benchmark 与工具对比更可复现。

### 运行 / 接受 / 转移语义

论文直接给出 standard semantics 下的解释公式：

$$
\theta_e \rightarrow (\theta_s \land ((G\psi_e \land \varphi_e) \rightarrow (G\psi_s \land \varphi_s)))
$$

上式中的符号逐项解释如下：

1. `\theta_e` 和 `\theta_s` 分别表示环境和系统的初始条件。
2. `\psi_e` 和 `\psi_s` 分别表示环境与系统的不变条件。
3. `\varphi_e` 和 `\varphi_s` 分别表示环境假设与系统保证。
4. `G\psi_e` 表示环境 invariant 在全局上持续成立。
5. 整个公式表示：当环境满足条件时，系统必须满足自己的 preset、assert 和 guarantee。

strict semantics 则被定义为：

$$
\theta_e \rightarrow (\theta_s \land (\psi_s\ W\ \neg \psi_e) \land ((G\psi_e \land \varphi_e) \rightarrow \varphi_s))
$$

上式中的符号逐项解释如下：

1. `W` 是 weak-until。
2. `\psi_s\ W\ \neg \psi_e` 表示系统 assertion 至少要维持到环境 requirement 被打破为止。
3. 这就是论文所说的 strict implication semantics。

当 `SEMANTICS` 与 `TARGET` 不一致时，论文还给出简单转换原则：

$$
\text{Moore} \to \text{Mealy}: X\text{-prefix on inputs}, \qquad \text{Mealy} \to \text{Moore}: X\text{-prefix on outputs}
$$

上式中的符号逐项解释如下：

1. 从 `Moore` 语义转到 `Mealy` target 时，要给输入原子命题加一层 `X`。
2. 反向转换则给输出原子命题加 `X`。
3. 其目的是保持 realizability 等价。

### 语义边界

1. `TLSF` 只描述 synthesis problem，不负责具体求解。
2. 它面向 `LTL` synthesis，而不是一般 timed / probabilistic model input format。
3. `SyFCo` 的价值主要是 lowering 和 conversion，不是验证或综合本身。
4. 若团队只关心单一低层后端并手写其专用输入，`TLSF` 的收益会下降。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 规格骨架 | `$\mathcal T = (I, O, \theta_e, \theta_s, \psi_e, \psi_s, \varphi_e, \varphi_s)$` | 把 `TLSF` 的 `MAIN` 结构压成语义对象。 |
| basic `LTL` 语法 | `$\varphi' := true \mid false \mid s \mid \cdots \mid \varphi W \varphi$` | 说明 basic format 的表达核心仍是标准 `LTL`。 |
| target model | `$Me = (I, O, Q, q_0, \delta, \lambda_e),\ Mo = (I, O, Q, q_0, \delta, \lambda_o)$` | 明确 `Mealy / Moore` 两种目标实现模型。 |
| standard semantics | `$\theta_e \rightarrow (\theta_s \land ((G\psi_e \land \varphi_e) \rightarrow (G\psi_s \land \varphi_s)))$` | 定义非 strict 解释。 |
| strict semantics | `$\theta_e \rightarrow (\theta_s \land (\psi_s\ W\ \neg\psi_e) \land ((G\psi_e \land \varphi_e) \rightarrow \varphi_s))$` | 定义 `GR(1)` 风格 strict implication。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | `TLSF` 本身不描述状态机结构，而是描述目标控制器应满足的规格。 |
| 事件 / 触发 | 很强 | 输入输出分区是一等对象。 |
| 守卫 / 数据 | 中等支持 | 通过函数、参数、枚举和 bus 提升规格表达力。 |
| 层次 | 不适用 | 不是层次状态机语言。 |
| 并发 / 同步 | 间接支持 | 通过 `LTL` 规格描述交互约束，而不是直接建模同步结构。 |
| 时间约束 | 弱支持 | 论文主体是 plain `LTL` synthesis，不是 timed logic。 |
| 连续动态 / 随机性 | 不支持 | 不涉及 hybrid / stochastic semantics。 |
| 可执行 / 可验证性 | 很强 | `SyFCo`、benchmark repository、`SYNTCOMP` 接入都是成熟基础设施。 |

### 形式化问题与性质

1. `TLSF` 的核心价值是 benchmark、工具比较和规格交换，而不是算法创新。
2. 它把综合前端从“低层电路格式”拉回到“人能读写的规格层”。
3. 参数、枚举和函数让它特别适合表达规格族，而不是单个固定实例。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 直接编写 `TLSF` 文本。
2. 从 benchmark repository 复用模板。
3. 用 `SyFCo` 调整参数、展开语法糖或转换到其他格式。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `INFO / GLOBAL / MAIN` 三段文本结构；
2. `INPUTS/OUTPUTS/ASSUME/GUARANTEE` 等小节；
3. 参数、枚举、函数和 buses；
4. `SyFCo` 输出的 basic `TLSF`、`LTL`、`Promela LTL` 或 `PSL`。

### 交换与互操作

这篇论文的重心几乎全在互操作：

1. 统一综合 benchmark 的高层表示。
2. 让 synthesis solver 只需支持 basic format。
3. 借 `SyFCo` 把高层结构自动压到 solver 能吃的低层输入。

## 配套基础设施

- 建模/编辑工具：`TLSF` 文本格式与 benchmark 仓库。
- 解析/交换/元模型支持：`SyFCo` 负责 lowering、参数修改和格式转换。
- 仿真/执行支持：`TLSF` 自身不执行系统，执行与综合依赖后端 solver。
- 验证/分析支持：间接支持，通过后端 synthesis 工具与 `SYNTCOMP` 工作流完成。
- 代码生成/转换支持：`SyFCo` 可转到 plain `LTL`、`Promela LTL`、`PSL` 等输出。
- 标准化或社区生态：`TLSF` 已被 `SYNTCOMP` 新赛道采用，是反应式综合 benchmark 生态的重要标准层。

## 适用场景与需求前提

### 适用场景

适合需要标准化表达 `LTL` synthesis 问题、共享 benchmark、批量生成参数化规格族，以及比较不同 synthesis solver 的场景。

### 需求前提

1. 需求需能写成有限输入输出上的 `LTL` 规格。
2. 团队关心 solver 可比性与 benchmark 复现。
3. 需要高层参数化而不是手写低层 `AIGER`。
4. 后端工具愿意通过 `SyFCo` 接入。

### 不适用或高成本场景

如果需求主要是 timed / probabilistic / hybrid synthesis，或团队只接受低层 circuit-game 输入，`TLSF` 就不是最佳最终载体。

## 与相邻形式主义的关系

相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，`HOA` 是 `omega` 自动机交换格式，而 `TLSF` 是更前端的 synthesis 规格格式；相对 [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)，`Strix` 是求解器，而 `TLSF` 是它可直接消费的规格输入层；相对 [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)，`Acacia+` 属于 `LTL` synthesis tool 路线，而本文提供的是 solver 之间共享的高层格式。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“统一中间格式”在综合问题上同样重要，不只是验证问题。
2. 对未来从需求生成性质或控制器规格的工作，`TLSF` 这类格式非常适合作为中间层。
3. 参数化规格族的设计，也对批量 scenario / property 生成很有启发。

### 作为目标形式主义还是中间表示

更像高层中间表示和 benchmark / 工具互操作标准，不是最终状态机本体。

### 对需求到模型生成的启发

1. 若需求要服务多个综合器，先生成统一规格层比直接面向单一求解器更稳。
2. 输入输出分区、假设保证结构和 strict semantics 是自动建模时应显式保留的元信息。
3. 参数、枚举和大算子说明规格生成器应支持“族”而不是只支持“单实例”。

### 现实限制

它只标准化了规格表达，不解决 realizability 或 strategy extraction 本身的复杂度问题。

## 重要的相关工作

1. [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：`LTL` 翻译后常见的后续 automata interchange format。
2. [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)：直接消费 `TLSF` 的现代综合器代表。
3. [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)：`LTL` synthesis 求解器路线的对照项。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`TLSF / SyFCo / LTL synthesis specification format`
- 论文角色：高层 `LTL` 反应式综合规格格式与 `SyFCo` 转换工具
- 核心功能：统一表达 `LTL` synthesis 问题，并为多后端综合器提供标准输入层。
- 关键特性：参数化规格、枚举、函数、`Mealy/Moore` 语义、strict implication、`SyFCo` lowering。
- 构造方式：high-level `TLSF` -> `SyFCo` -> basic `TLSF` / solver-specific format。
- 基础设施：`TLSF`、`SyFCo`、`SYNTCOMP` benchmark 生态。
- 适用场景：反应式综合 benchmark、规格共享、参数化 synthesis 问题表达。
- 需求前提：需求需能写成有限输入输出上的 `LTL` 假设/保证结构。
- 状态：🟢 直接可用
