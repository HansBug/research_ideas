# 部分状态机模型的执行 / Execution of Partial State Machine Models

## 基本信息

- 标题：Execution of Partial State Machine Models
- 中文标题：部分状态机模型的执行
- 作者：Mojtaba Bagherzadeh，Nafiseh Kahani，Karim Jahed，Juergen Dingel
- 发表：*IEEE Transactions on Software Engineering*，48(3): 951-972，2022
- DOI：`10.1109/TSE.2020.3008850`
- 链接：https://doi.org/10.1109/TSE.2020.3008850
- 形式主义：`UML-RT State Machine / PMExec / partial model execution`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：partial-state-machine execution method combining static analysis, automatic refinement and input-driven execution
- 工具/实现获取方式：原文明确说明已实现 `PMExec`，并集成到 `Papyrus-RT`；正文说明 implementation publicly available，但未在正文中给出稳定公开仓库 URL。
- 标准/格式获取方式：主承载是 `UML-RT` / `Papyrus-RT` 状态机、调试脚本、interactive commands 与自动 refinement 生成的 decision points；它不是独立交换标准。

## 简报

这篇论文补的是“模型还没写完时，状态机能否先执行起来”的方法路线。作者提出的不是一个普通解释器，而是一个三步闭环：先做 static analysis 找出 partialness，再自动 refinement 生成 decision points，最后在执行时由用户或脚本输入补足缺失信息。`PMExec` 则把这条路线落到了 `UML-RT` / `Papyrus-RT` 上。

- 形式主义定位：围绕 `UML-RT` 状态机的 partial-model execution method，而不是新的状态机母型。
- 构造方式简述：`static analysis -> automatic refinement -> input-driven execution`，其中 refinement 通过插入 `decp` 等结构把“卡住的缺口”改造成可继续执行的分支点。
- 基础设施与场景简述：依托 `Papyrus-RT`、模型变换、交互式 / 脚本式输入、回写 design model 的规则机制，服务早期验证、unit testing 和部分模型调试。

```text
partial UML-RT model -> static analysis -> refined HSM with decision points -> interactive / scripted execution -> optional write-back to design model
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML-RT` hierarchical state machines (`HSM`)；
2. problematic partial elements，例如缺失初始状态、不可触发迁移、non-exhaustive guards；
3. 自动 refinement 产物，例如 decision point `decp`；
4. input-driven execution；
5. `PMExec` 与 `Papyrus-RT` 集成流程。

### 核心抽象

论文直接把 `HSM` 定义为：

$$
\mathrm{HSM} = \langle S, T, in \rangle
$$

上式中的符号逐项解释如下：

1. `$S$` 是状态集合，包含 basic、composite 与 pseudo states。
2. `$T$` 是 transitions 集合。
3. `$in$` 表示进入复合状态时默认激活的初始状态函数。

论文把 transition 写成五元组：

$$
t = (src, guard, trig, act, des)
$$

上式中的符号逐项解释如下：

1. `$src$` 和 `$des$` 是源 / 目标状态。
2. `$guard$` 是 guard expression。
3. `$trig$` 是可触发该迁移的消息集合。
4. `$act$` 是 transition action。

执行语义中的 configuration 可整理为：

$$
\gamma = \langle \sigma, E, H \rangle
$$

上式中的符号逐项解释如下：

1. `$\sigma$` 是当前 active state。
2. `$E$` 是变量到其值的映射。
3. `$H$` 是 history 相关信息。

论文在行为保持性证明里给出 simulation relation，可保守整理为：

$$
R = \{\, (\gamma_o,\gamma_r) \mid \gamma_o.\sigma = \gamma_r.\sigma \land \gamma_o.E = \gamma_r.E \setminus E_{new} \land \gamma_o.H = \gamma_r.H \,\}
$$

上式中的符号逐项解释如下：

1. `$\gamma_o$` 是原始 `HSM` 的 configuration。
2. `$\gamma_r$` 是 refined `HSM` 的 configuration。
3. `$E_{new}$` 是 refinement 为调试 / decision points 新引入的变量集合。
4. 该关系表达“忽略新增辅助变量后，refined model 保留原模型行为”。

### 一个最小例子与通俗解释

论文 running example 是交通灯控制器：

1. 某组件的 `CTRHSM` 有从 `yellow` 到 `red` 的行为缺口，或者某条迁移缺少 trigger / action。
2. 在普通执行器里，模型会直接卡住。
3. `PMExec` 先通过分析识别这些 partialness，再自动插入 `decp` decision point。
4. 真正运行到这里时，用户可以交互式选择迁移，或脚本提前规定怎样继续。

通俗地说，这套方法像“给不完整状态机装一个安全的临时岔道器”。当原模型缺信息走不下去时，它不直接失败，而是把“该怎么办”显式暴露给调试者或规则脚本。

### 运行 / 接受 / 转移语义

论文用 `LTS` 给出 `HSM` 执行语义，可保守压成：

$$
\langle \sigma, E, H \rangle \xrightarrow{a_1 \cdots a_n} \langle \sigma', E', H' \rangle
$$

上式中的符号逐项解释如下：

1. `$\sigma$` 与 `$\sigma'$` 是执行前后的 active state。
2. `$E,E'$` 是执行前后的变量赋值。
3. `$H,H'$` 是执行前后的 history 信息。
4. `$a_1\cdots a_n$` 是本次 execution step 执行的 action sequence。

论文的整条方法链可简写成：

$$
M \xrightarrow{\mathrm{analyze}} P \xrightarrow{\mathrm{refine}} \widehat{M} \xrightarrow{\mathrm{input}} \mathrm{run}
$$

上式中的符号逐项解释如下：

1. `$M$` 是原始 partial model。
2. `$P$` 是分析出的 problematic elements 集合。
3. `$\widehat{M}$` 是 refined model。
4. `$\mathrm{input}$` 可以是 interactive commands，也可以是 execution rules script。

### 语义边界

1. 论文面向的是 `UML-RT` / `Papyrus-RT` 这一类层次状态机，不是任意图模型。
2. 重点是 partialness 容忍和 early execution，不是完整 UML 语义覆盖。
3. 时间属性只在 `UML-RT` 背景中间接出现，正文主线不是 timed verification。
4. 该方法保持原模型行为，但新增了调试 / decision-point 辅助结构，因此它更像“执行方法 + refinement 策略”。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `HSM` 骨架 | `$\mathrm{HSM}=\langle S,T,in\rangle$` | 论文工作的直接对象。 |
| transition 五元组 | `$t=(src,guard,trig,act,des)$` | partialness 经常就出现在这些字段里。 |
| configuration | `$\gamma=\langle \sigma,E,H\rangle$` | 执行语义的基本状态对象。 |
| 方法闭环 | `$M \xrightarrow{\mathrm{analyze}} P \xrightarrow{\mathrm{refine}} \widehat{M} \xrightarrow{\mathrm{input}} \mathrm{run}$` | 三阶段方法路线的形式化缩写。 |
| simulation relation | `$R=\{(\gamma_o,\gamma_r)\mid \cdots\}$` | refined model 对原模型行为保持的证明核心。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主体就是 `UML-RT` 层次状态机。 |
| 事件 / 触发 | 很强 | partialness 常体现在 missing triggers / deadlock states 上。 |
| 守卫 / 数据 | 很强 | non-exhaustive guards、missing actions 和数据赋值都是分析重点。 |
| 层次 | 很强 | `HSM` 与 composite states 是论文中心。 |
| 并发 / 同步 | 中等支持 | `UML-RT` 组件间通过消息交互，但主线不是并发语义创新。 |
| 时间约束 | 弱支持 | 语言背景是 soft real-time，但本文主线不是 clock semantics。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / probabilistic line。 |
| 可执行 / 可验证性 | 很强 | 可交互执行、批处理脚本、保存规则并回写设计模型。 |

### 形式化问题与性质

1. 论文解决的是“partial state machine 也能执行并服务调试”的方法问题。
2. 行为保持性不是口头承诺，而是通过 simulation relation 给出形式保证。
3. 其真正创新点在“自动 refinement + input-driven continuation”，而不是单独一个 debug UI。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Papyrus-RT` / `UML-RT` 状态机模型；
2. static analysis 提取的 partialness 集合；
3. 自动生成的 refined `HSM`；
4. interactive commands 或 execution-rule scripts。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `HSM` 结构；
2. `decp` decision points；
3. execution rules grammar；
4. write-back to design model 的规则应用机制。

### 交换与互操作

互操作重点是模型生命周期内部：

1. `Papyrus-RT` 模型进入 `PMExec`。
2. 分析与 refinement 仍在模型层完成，而不是先降为代码。
3. 用户的交互决策可保存成 rules，之后还能自动回写到 design model。

## 配套基础设施

- 建模/编辑工具：`Papyrus-RT` 是默认前端。
- 解析/交换/元模型支持：模型查询、模型变换、rule grammar 和 design-model write-back。
- 仿真/执行支持：`PMExec` 本身就是 partial-model execution engine。
- 验证/分析支持：static analysis、stuck-state detection、debugging、interactive / batch execution。
- 代码生成/转换支持：强调“模型到 refined 模型”的 transformation，而不是最终部署代码生成。
- 标准化或社区生态：依托 `UML-RT`、`Papyrus-RT` 和模型变换工具栈。

## 适用场景与需求前提

### 适用场景

适合早期 `UML-RT` 设计、增量式建模、unit testing、调试 partial state machines 和需要尽早运行模型原型的场景。

### 需求前提

1. 模型属于可支持的 `UML-RT` / `HSM` 子集。
2. 团队愿意把“缺失信息如何补”显式写成 interactive decisions 或 rules。
3. 重点是尽早验证设计方向，而不是等模型完全完工后再一次性执行。
4. 模型中的 partialness 主要落在状态、迁移、trigger、guard、action 等结构层。

### 不适用或高成本场景

如果模型目标是全自动完备代码生成、连续动力学仿真或完整 UML 全语义覆盖，这条方法路线就不够直接。

## 与相邻形式主义的关系

相对 [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)，`UMerL` 解决“完整 UML 状态机怎样执行与验证”，而本文解决“部分 `UML-RT` 状态机如何先执行起来”；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，后者更强调 design-runtime bridge，本文更强调 partialness-aware debugging；相对 [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)，本文是 survey 中“可执行 / 可调试方法路线”的典型代表条目。

## 与本研究的关系

### 对 Project 1 的价值

1. 这篇论文直接对应“LLM 先产出半成品状态机，再逐步补全”的现实工作流。
2. 它说明不完整模型并不等于完全不可用，生成-验证-修复闭环可以从 partial model 就启动。
3. 对 `project_4` 的 iterative repair 尤其有启发：用户 / 脚本输入和 design-model write-back 天然形成修复闭环。

### 作为目标形式主义还是中间表示

更像 `UML-RT` 目标形式主义上的执行 / 修复方法路线，而不是新的本体。

### 对需求到模型生成的启发

1. LLM 生成的状态机如果缺少 guards、actions 或 transitions，不必立即丢弃，可以先进入 partial-execution workflow。
2. 决策点 `decp` 机制很适合把“暂时缺失的需求细节”显式化。
3. 若未来要做交互式模型修复，保存 execution rules 并回写 design model 是很值得借鉴的操作形态。

### 现实限制

本文的强项是 partial-model debugging，而不是统一验证后端；它更适合 `UML-RT` / 工程设计流程，不适合直接外推到所有状态机家族。

## 重要的相关工作

1. [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)：完整 `UML State Machine` 的执行与验证基础设施。
2. [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：设计到运行时的一体化 UML 解释执行路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 状态机形式化与自动验证总览。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML-RT State Machine / PMExec / partial model execution`
- 归类理由：主贡献是 partial-state-machine execution 的方法闭环与 `PMExec` 工程实现，而不是新的状态机本体或统一标准。
