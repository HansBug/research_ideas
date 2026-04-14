# Issy：无限状态反应式系统的规格与综合平台 / Issy: A Comprehensive Tool for Specification and Synthesis of Infinite-State Reactive Systems

## 基本信息

- 标题：Issy: A Comprehensive Tool for Specification and Synthesis of Infinite-State Reactive Systems
- 中文标题：Issy：无限状态反应式系统的规格与综合平台
- 作者：Philippe Heim，Rayna Dimitrova
- 发表：*Computer Aided Verification*，pp. 298-312，2025
- DOI：`10.1007/978-3-031-98685-7_14`
- 链接：https://doi.org/10.1007/978-3-031-98685-7_14
- 形式主义：`infinite-state reactive synthesis / RP-LTL / symbolic games / Issy`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：无限状态反应式综合的统一规格格式、编译中间层与 solver portfolio 平台
- 工具/实现获取方式：论文给出开源仓库 `https://github.com/phheim/issy`，实现采用 `Haskell`，并说明可通过 `Stack` 构建；外部依赖包括 `Spot`、`z3`、`MuVal` 与 `OptPCSat`。
- 标准/格式获取方式：高层输入是 `Issy` format，低层中间格式是 `LLissy`；同时兼容旧的 `rpg` 与 `tslmt` 输入。它是研究社区统一输入层候选，不是正式行业标准。

## 简报

`Issy` 的贡献不只是“又一个综合器”。它真正补的是无限状态 reactive synthesis 领域长期缺失的统一工作台：同一个高层格式里同时容纳 temporal formulas 和 explicit games，同一条编译链里把它们压到 `LLissy` 和 symbolic games，再由 attractor-acceleration solver portfolio 去做 realizability 与 synthesis。相对只支持某一种规格形式或某一个 prototype solver 的工具，`Issy` 更像“无限状态综合的输入层 + 中间层 + 多解法后端”。

- 形式主义定位：无限状态 reactive synthesis 的规格与求解基础设施，而不是新的状态机母型。
- 构造方式简述：`Issy` high-level spec -> `LLissy` -> formulas-to-games / monitor enhancement -> symbolic game product -> acceleration-based solving -> reactive program / `C` extraction。
- 基础设施与场景简述：依托 `Issy/LLissy`、`RP-LTL`、symbolic games、`Spot`、acceleration lemmas 与 `Haskell` 工程化实现，服务带整数/实数数据的 reactive controller synthesis。

```text
logic formulas + game blocks -> Issy/LLissy -> symbolic infinite-state game -> acceleration-based solver -> realizability result / reactive program
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Issy` 高层规格格式。
2. `LLissy` 低层中间格式。
3. `RP-LTL` 公式块与带显式 locations 的 game blocks。
4. 由各组件乘积得到的 symbolic synthesis game。
5. attractor acceleration 与 geometric acceleration 求解器。

### 核心抽象

论文明确说明公式块的语义是“assumptions 的合取蕴含 asserts 的合取”，可写成：

$$
\bigwedge_{i=1}^{m} \mathrm{assume}_i \Rightarrow \bigwedge_{j=1}^{n} \mathrm{assert}_j
$$

上式中的符号逐项解释如下：

1. `$\mathrm{assume}_i$` 是环境约束。
2. `$\mathrm{assert}_j$` 是系统保证。
3. 每个原子命题不是布尔 proposition，而是关于 `bool/int/real` 变量的量词自由一阶约束。

根据论文给出的语法与求解流程，可把 `Issy` 中单个 game block 的骨架保守整理为：

$$
G = (L, l_0, U, X, T, \Omega)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 locations 集合。
2. `$l_0$` 是初始 location。
3. `$U$` 是 environment-controlled input variables。
4. `$X$` 是 system-controlled state variables。
5. `$T(l,u,x,l',x')$` 是从当前 location 到下一 location 的转移约束。
6. `$\Omega$` 是 winning condition，论文支持 `Safety`、`Reachability`、`Buechi`、`CoBuechi` 与 `ParityMaxOdd`。
7. 该元组是依据论文格式说明做的保守整理，原文给出的具体语法是 `loc` 与 `from ... to ... with ...` 这类声明。

论文还明确指出整个规格的语义是所有公式与游戏分量乘积得到的单一 synthesis game：

$$
G_{\mathrm{spec}} = \prod_{i=1}^{m} G_{\varphi_i} \times \prod_{j=1}^{n} G_j
$$

上式中的符号逐项解释如下：

1. `$G_{\varphi_i}$` 是第 `$i$` 个公式分量翻译得到的 game。
2. `$G_j$` 是第 `$j$` 个显式 game block。
3. `Issy` 要求并检查其中至多一个分量带非 safety winning condition。

### 一个最小例子与通俗解释

论文给出的 load-balancing 例子很说明问题：

1. 环境输入 `add/rem` 表示外部负载增加量与可用吞吐。
2. 系统状态 `load1/load2/rem1/rem2` 表示两个组件当前负载与系统给出的吞吐分配。
3. 一部分需求自然写成 `F G [add <= 0]` 这类时间公式。
4. 另一部分“从某个 location 出发，在满足某些当前/下一状态约束时可走到哪个 location”的内容，更适合写成显式 game transitions。

通俗地说，`Issy` 像“把逻辑规格和博弈图规格放进同一个文件”的综合工作台。你不必勉强把所有状态相关控制流都硬塞进一条巨大公式，也不必把所有高层目标都拆成底层博弈边。

### 运行 / 接受 / 转移语义

论文把 realizability / synthesis 统一还原为 symbolic game 求解，可保守写成：

$$
\exists \sigma_{sys}\ \forall \sigma_{env}:\ \mathrm{Win}(\mathrm{play}(\sigma_{sys}, \sigma_{env}))
$$

上式中的符号逐项解释如下：

1. `$\sigma_{sys}$` 是系统策略。
2. `$\sigma_{env}$` 是环境策略。
3. `$\mathrm{play}$` 是两者在乘积 game 上诱导出的运行。
4. `$\mathrm{Win}$` 根据 `Safety/Buechi/Parity...` 等 winning condition 判定该运行是否满足规格。

对公式到 game 的翻译，论文说明先经 `Spot` 得到 deterministic `\omega`-automaton，再与 monitor 做按需乘积。可保守写成：

$$
\varphi \xrightarrow{\mathrm{Spot}} A_\varphi \xrightarrow{\mathrm{monitor\ product}} G_\varphi^{+}
$$

上式中的符号逐项解释如下：

1. `$\varphi$` 是输入公式。
2. `$A_\varphi$` 是由 `Spot` 生成的 deterministic `\omega`-automaton。
3. `$G_\varphi^{+}$` 是结合 monitor 语义信息后的 enhanced game。
4. 论文说明 `--pruning` 参数控制 monitor reasoning 的强度。

### 语义边界

1. 论文目标是 infinite-state synthesis framework，不是证明该大类问题整体可判定。
2. `Issy` 通过不完备但实用的 acceleration-based solver 处理许多含无界循环的实例。
3. `RP-LTL` 允许 primed state variables，但不允许 primed environment inputs；若要比较历史输入值，必须显式存入状态变量。
4. 格式统一了 temporal formulas 与 games，但复杂连续动力学仍需先抽象到 `bool/int/real` 变量转移层。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 公式块语义 | `$\bigwedge_i \mathrm{assume}_i \Rightarrow \bigwedge_j \mathrm{assert}_j$` | 高层 `Issy` 公式分量的组合方式。 |
| game block 骨架 | `$G = (L,l_0,U,X,T,\Omega)$` | 依据语法说明整理出的显式博弈对象。 |
| 规格乘积 | `$G_{\mathrm{spec}} = \prod_i G_{\varphi_i} \times \prod_j G_j$` | 整个综合问题的统一求解对象。 |
| 综合目标 | `$\exists \sigma_{sys}\forall \sigma_{env}: \mathrm{Win}(\mathrm{play}(\sigma_{sys},\sigma_{env}))$` | realizability / synthesis 的基本语义。 |
| 公式翻译链 | `$\varphi \xrightarrow{\mathrm{Spot}} A_\varphi \xrightarrow{\mathrm{monitor\ product}} G_\varphi^{+}$` | 公式分量进入 solver 的关键步骤。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 显式 locations 与全局 state variables 都是一等对象。 |
| 事件 / 触发 | 强支持 | 环境先选输入，系统再选下一状态与下一 location。 |
| 守卫 / 数据 | 很强 | 原子约束可直接涉及 `bool/int/real` 变量与 next-state 变量。 |
| 层次 | 不支持 | 格式不是层次状态机语法。 |
| 并发 / 同步 | 间接支持 | 通过 game product 组合多公式 / 多 game 分量，不是并发组件代数。 |
| 时间约束 | 间接支持 | 可通过公式或 game 约束表达离散步上的时序关系，但不是 timed automata clocks。 |
| 连续动态 / 随机性 | 不支持 | 核心对象仍是无限状态但离散步进的 symbolic games。 |
| 可执行 / 可验证性 | 很强 | 支持 realizability、program extraction、`C` program 生成与 benchmark 统一输入。 |

### 形式化问题与性质

1. `Issy` 的最大价值是把“公式规格”和“博弈规格”真正合并成同一个输入层。
2. `LLissy` 让不同前端格式可以共享一个低层表示，这是无限状态 synthesis 生态里非常稀缺的基础设施。
3. geometric acceleration 说明它并不满足于包装旧 solver，而是在 game-solving 层做了新的工程化启发。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `input/state` 变量声明及 `bool/int/real` 类型。
2. `formula { assume ...; assert ... }` 逻辑规格块。
3. `game ... from ... { loc ...; from ... to ... with ... }` 博弈规格块。
4. `def` 宏定义与旧的 `rpg/tslmt` 兼容输入。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Issy` 高层格式。
2. `LLissy` 低层 `s-expression` 风格中间格式。
3. 由 `Spot`、monitor 和 product 生成的 symbolic game。
4. 抽取出的 reactive program 与 `C` 程序。

### 交换与互操作

1. `Issy` compiler 把高层格式压成更易解析的 `LLissy`。
2. 论文明确鼓励其他前端翻译到 `LLissy`，形成 benchmark 交换层。
3. 工具同时支持 `Issy`、`LLissy`、`rpg` 和 `tslmt` 输入，降低了既有原型迁移成本。

## 配套基础设施

- 建模/编辑工具：核心是 `Issy` / `LLissy` 文本格式与编译器。
- 解析/交换/元模型支持：`LLissy`、`Spot` automata translation、monitor enhancement、symbolic game product。
- 仿真/执行支持：支持 strategy synthesis 与 reactive program / `C` extraction。
- 验证/分析支持：realizability、infinite-state parity solving、attractor acceleration、geometric acceleration。
- 代码生成/转换支持：可从求解结果导出 reactive programs 与 `C` programs。
- 标准化或社区生态：`Haskell`、`Stack`、`Spot`、`z3`、`MuVal`、`OptPCSat` 共同构成研究型工具链。

## 适用场景与需求前提

### 适用场景

适合带整数/实数数据的无限状态 reactive synthesis、既有显式控制相位又有高层时序要求的控制器建模，以及需要统一 benchmark 交换层的无限状态综合研究。

### 需求前提

1. 需求需能在离散步语义下表达为公式约束与/或显式 game transitions。
2. 环境输入与系统状态更新需要能写成量词自由约束。
3. 若要利用 monitor pruning 或 acceleration，问题结构最好存在可提炼的 ranking / geometric progress。
4. 若要导出 `C` 程序，最终策略需能落到工具支持的 reactive program 数据结构。

### 不适用或高成本场景

如果系统本质上依赖稠密时间 clocks、连续动力学或高阶数据结构，直接写进 `Issy` 会很费力；此时更适合先做 timed/hybrid abstraction，再决定是否进入该框架。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 聚焦有限离散 `GR(1)`，`Issy` 面向无限状态数据与更一般 symbolic games；相对 [a-high-level-ltl-synthesis-format-tlsf-v11/desc.md](../a-high-level-ltl-synthesis-format-tlsf-v11/desc.md)，`TLSF` 是有限状态 `LTL` synthesis 的规格标准，而 `Issy/LLissy` 试图为 infinite-state synthesis 提供对应输入层；相对 [spectra-a-specification-language-for-reactive-systems/desc.md](../spectra-a-specification-language-for-reactive-systems/desc.md)，`Spectra` 是结构化 `GR(1)` DSL，`Issy` 则把 formulas 与 games 一起作为统一前端。

## 与本研究的关系

### 对 Project 1 的价值

`Issy` 对本研究最直接的启发，是“同一需求可以部分落成 temporal formulas、部分落成显式 game structure”。这和 LLM 从自然语言中同时抽取状态相位、守卫条件和高层目标的任务非常吻合，比强迫所有内容都进入单一公式或单一状态图更稳健。

### 可复用启发

1. 可以把 LLM 生成结果拆成“公式块 + 状态转移块”两类中间表示，再统一编译。
2. `LLissy` 说明中间层格式对多工具生态很关键，值得在本仓库后续实验里借鉴。
3. acceleration lemmas 与 geometric progress 提示：修复与验证阶段不应只做 SAT/SMT 暴力枚举，还要利用结构性 ranking 信息。

## 重要的相关工作

1. `rpgsolve` / `rpg-STeLA`：无限状态 reactive program game 求解基线。
2. `TSL-MT` 与 `tslmt2rpg`：旧格式与翻译路线。
3. `Spot`：公式到自动机翻译后端。
4. `MuVal` 与 `OptPCSat`：monitor 与约束求解辅助工具。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 关键特性：`Issy/LLissy`、`RP-LTL`、symbolic games、geometric acceleration、reactive program extraction。
- 构造方式：high-level spec -> `LLissy` -> symbolic game -> acceleration-based solving -> program extraction。
- 基础设施：`Haskell/Stack`、`Spot`、`z3`、`MuVal`、`OptPCSat`、benchmark exchange layer。
- 对状态机族演化树而言，它提供的是 infinite-state reactive synthesis 的规格/求解平台锚点，不形成新的主树节点。
