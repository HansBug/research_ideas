# SAL 2：符号分析实验室 / SAL 2

## 基本信息

- 标题：SAL 2
- 中文标题：SAL 2：符号分析实验室
- 作者：Leonardo de Moura，Sam Owre，Harald Rueß，John Rushby，N. Shankar，Maria Sorea，Ashish Tiwari
- 发表：*Computer Aided Verification (CAV 2004)*，pp. 496-500，2004
- DOI：`10.1007/978-3-540-27813-9_45`
- 链接：https://doi.org/10.1007/978-3-540-27813-9_45
- 形式主义：`SAL state machines / Symbolic Analysis Laboratory`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：scriptable multi-backend model-checking laboratory for finite- and infinite-state state machines
- 工具/实现获取方式：原文明确给出 `SAL` 站点 `http://sal.csl.sri.com`，并说明提供 analyzer、simulator 与 Scheme scripting API。
- 标准/格式获取方式：原文说明 `SAL` 以自身状态机语言和 XML 表示为承载，并配有人类可读 ASCII 与 `LSAL` 语法；它是分析实验室的语言/工具载体，不是独立行业标准。

## 简报

`SAL 2` 的价值，在于它不是单个 model checker，而是一个“状态机分析实验室”。论文把统一的状态机语言、共享预处理/编译链、显式/符号/有界/无限有界/witness 多种 analyzer、以及可脚本化 API 组织到同一工作台里。对文库而言，它补的是“如何把一门富类型状态机语言稳定接到多类 deductive core”的基础设施路线。

- 形式主义定位：面向状态机的 scriptable symbolic analysis laboratory。
- 构造方式简述：用 `SAL` 模块语言描述状态机，再经共享 preprocessing/compilation 编到 `BDD`、propositional `SAT` 或 `ICS` 等 backend。
- 基础设施与场景简述：依托 `CUDD`、`ICS`、`zChaff/GRASP`、Scheme API 和 simulator，服务 finite-state、timed/hybrid encoding、infinite-state bounded checking 与实验性 analyzer 组装。

```text
SAL modules -> shared preprocessing / compilation -> BDD / SAT / ICS analyzers -> proof / counterexample / scriptable analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `SAL` 状态机模块语言。
2. 共享 preprocessing / compilation routines。
3. symbolic / bounded / infinite bounded / witness 四类 model checker。
4. simulator 与 Scheme scripting API。
5. finite-state 与 infinite-state 的统一承载。

### 核心抽象

根据论文对语言的描述，可保守整理一个 `SAL` 状态机模块为：

$$
\mathcal M = (X_{in}, X_{out}, X_{loc}, X_{glob}, I, T)
$$

上式中的符号逐项解释如下：

1. `X_{in}` 是 input state variables。
2. `X_{out}` 是 output state variables。
3. `X_{loc}` 是 local state variables。
4. `X_{glob}` 是 global state variables。
5. `I` 是初始约束。
6. `T` 是 transition relation。
7. 论文明确说：状态机以 parameterized modules 给出，变量会被显式标记为 input、output、local 或 global。

论文还说明 transition relation 可以由 guarded commands 和 `SMV`-style variable-wise invariants 给出，因此单步语义可写成：

$$
s' \models T(s,s')
$$

上式中的符号逐项解释如下：

1. `s` 是当前状态赋值。
2. `s'` 是下一状态赋值。
3. `T` 综合了 guarded commands、primes 和 assignments。
4. 这也是 `SAL` 后端统一编译到 `BDD`、`SAT` 或 `ICS` 的核心对象。

对 bounded model checking，论文同样强调 `k`-induction，可整理为：

$$
\left(I(s_0) \land \bigwedge_{0 \le i < k} T(s_i,s_{i+1})\right) \rightarrow \varphi
$$

上式中的符号逐项解释如下：

1. `s_0,\ldots,s_k` 是长度为 `k` 的路径。
2. 前件表示系统在前 `k` 步上的展开。
3. `\varphi` 是要证明的状态性质或归纳目标。
4. 论文明确说 `BMC` 和 `inf BMC` 都支持 `k`-induction。

### 一个最小例子与通俗解释

按论文里的语言说明，一个最小例子可以理解成：

1. 定义一个参数化 module。
2. 在 module 内声明 input、output、local 变量。
3. 用 guarded commands 和 prime notation 写转移关系。
4. 写一个 `LTL` 或 `CTL` 公式，交给相应 analyzer。

通俗地说，`SAL 2` 像一个“状态机语言 + 多个可替换 model checker 的实验台”。你写一次模块，后面可以换 `BDD`、`SAT` 或 `ICS` 路线来验证，不必为每个求解器重写模型。

### 运行 / 接受 / 转移语义

论文对语言层面说得很清楚：

1. modules 可以同步组合、异步组合，或两者混合。
2. renaming 机制允许把不同模块的 inputs/outputs 正确“接线”。
3. `LTL` 性质会被翻译成优化后的 `Büchi` automata。
4. witness model checker 直接支持 `CTL`。

因此可以把组合系统保守写成：

$$
\mathcal S = \mathcal M_1 \parallel \cdots \parallel \mathcal M_n
$$

上式中的符号逐项解释如下：

1. `\mathcal M_i` 是单个 `SAL` module。
2. `\parallel` 表示同步、异步或混合组合。
3. 具体 wiring 由 renaming 和 ports/variables 约束决定。

### 语义边界

1. `SAL 2` 的主体是 analysis platform，而不是单一状态机母型。
2. timed/hybrid systems 的支持主要来自整数/实数状态与 `ICS`，不是专用 timed-automata engine。
3. 语言非常丰富，因此完整类型检查和 deeper checks 比一般编程语言前端更重。
4. 文章重点在 analyzer architecture，不在某个单独算法的完整理论证明。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模块骨架 | `$\mathcal M = (X_{in}, X_{out}, X_{loc}, X_{glob}, I, T)$` | `SAL` 状态机模块的最小保守抽象。 |
| 单步语义 | `$s' \models T(s,s')$` | guarded commands 与 prime notation 共同定义转移。 |
| 组合系统 | `$\mathcal S = \mathcal M_1 \parallel \cdots \parallel \mathcal M_n$` | `SAL` 支持同步、异步和混合组合。 |
| `k`-induction 工作形态 | `$\left(I(s_0) \land \bigwedge_{i<k} T(s_i,s_{i+1})\right) \rightarrow \varphi$` | `BMC/inf BMC` 都支持归纳式验证。 |
| LTL 承载 | `$LTL \rightarrow Büchi$` | 论文明确写到 `LTL` assertions 会编成优化后的 `Büchi` automata。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向参数化状态机模块。 |
| 事件 / 触发 | 中等支持 | 更偏变量更新与 guarded commands。 |
| 守卫 / 数据 | 很强 | rich type system，含 structured types、integers、reals。 |
| 层次 | 不支持 | 不是层次状态图工具。 |
| 并发 / 同步 | 强 | 支持同步、异步及其混合组合。 |
| 时间约束 | 中等支持 | 可借 real/integer state 和 `ICS` 编码 timed/hybrid systems。 |
| 连续动态 / 随机性 | 弱支持 | 不是专用连续/概率平台。 |
| 可执行 / 可验证性 | 很强 | 多 analyzer + simulator + scripting API。 |

### 形式化问题与性质

1. `SAL 2` 最重要的地方，是把状态机语言和 analyzer API 做成可脚本化实验室。
2. 它对 `timed/hybrid` 的意义，在于“无限状态也能走统一实验框架”，而不是另起一条专用 formalism。
3. 对状态机类型文库来说，它补的是 symbolic verification laboratory 这一类基础设施。

## 构造方式与承载格式

### 建模入口

主要入口有：

1. `SAL` 文本人类可读语法。
2. XML 表示。
3. `LSAL` Lisp-like syntax。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `BDD` encodings。
2. propositional `SAT` problems。
3. `ICS` decision-procedure problems。
4. `Büchi` automata 与 symbolic witnesses。

### 交换与互操作

互操作重点在 analyzer backends：

1. `CUDD`。
2. `ICS`。
3. `zChaff` / `GRASP`。
4. Scheme API 上的用户脚本。

## 配套基础设施

- 建模/编辑工具：`SAL` language、ASCII/`LSAL` front-end。
- 解析/交换/元模型支持：XML 表示、共享 type checking / preprocessing / compilation。
- 仿真/执行支持：`SAL Simulator` 支持交互执行、过滤状态与路径搜索。
- 验证/分析支持：SMC、BMC、inf BMC、WMC、`k`-induction、symbolic witnesses。
- 代码生成/转换支持：重点是编译到不同 deduction cores，而不是生成部署代码。
- 标准化或社区生态：`SAL`、`PVS`、`ICS`、Scheme scripting 共同形成实验平台生态。

## 适用场景与需求前提

### 适用场景

适合 finite-state symbolic checking、需要 richer data types 的状态机建模、以及想在同一平台里比较多种 analyzer 的研究或工程场景。

### 需求前提

1. 模型需能写成 `SAL` 参数化模块。
2. 团队接受文本建模与 scriptable workflow。
3. 若走 infinite-state 路线，性质和状态更新需适配 `ICS` 支持的理论。

### 不适用或高成本场景

如果需求主要是图形化 statechart authoring、工业代码生成或专用 timed-automata model checking，`SAL 2` 并不是最直接的入口。

## 与相邻形式主义的关系

相对 [nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md](../nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md)，`NuSMV 2` 更聚焦 `SMV` 内核和 `BDD/SAT`，而 `SAL 2` 更强调多 analyzer 与脚本化实验室；相对 [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)，`nuXmv` 是后续更强的统一 symbolic backend，而本文更像 symbolic laboratory；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，`LTSmin` 是 language-independent backend，`SAL 2` 则自带 rich front-end language。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明如果后续需要“同一状态机模型同时接多个验证后端”，最好先把前处理与后端 API 解耦。
2. `SAL` 的属性模板、witness 和 scripting 思路，对后续做自动化验证实验平台很有启发。
3. 对需求到模型闭环来说，它展示了“语言不必极简，也能通过统一编译管线支撑多类 analyzer”。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像 verification-oriented 中间语言和实验平台，而不是最终交付给领域工程师的状态机语法。

## 重要的相关工作

- [nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md](../nusmv-2-an-opensource-tool-for-symbolic-model-checking/desc.md)：另一条经典 symbolic backend 路线。
- [the-nuxmv-symbolic-model-checker/desc.md](../the-nuxmv-symbolic-model-checker/desc.md)：`NuSMV` 之后的更现代统一后端。
- [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)：language-independent 高性能 backend 对照条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇典型的 symbolic-analysis-laboratory 条目，适合作为 rich state-machine language、多 analyzer 工作台和 finite/infinite-state verification platform 的基础设施证据入账。
