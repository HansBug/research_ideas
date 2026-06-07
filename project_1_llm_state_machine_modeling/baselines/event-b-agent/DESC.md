# Event-B Agent：面向形式化模型合成与修复的 LLM Agent / Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair

## 基本信息

- **标题**：Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair
- **中文标题**：Event-B Agent：面向形式化模型合成与修复的 LLM Agent
- **作者**：Hongshu Wang, Xinyue Zuo, Yuhan Sun, Qin Li, Yamine Ait Ameur, Jin Song Dong
- **单位**：National University of Singapore；East China Normal University；IRIT - National Polytechnic Institute of Toulouse
- **发表**：Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE211, FSE 2026, 23 pages；本地 BibTeX 标注为 arXiv:2605.17475，accepted by FSE 2026，正式 proceedings 元数据后续仍建议复核
- **DOI**：10.1145/3808218
- **PDF来源与核验**：本轮使用用户已下载的 PDF（本目录 `paper.pdf`）；公开核验入口为 arXiv 与 DOI，核验日期 2026-06-07。

**代码/仓库获取方式**：
- 原文在引言脚注和 §9 Data Availability 明确说明实现、数据集和接口公开。
- 公开入口：[GitHub: HongshuW/EventB_Agent](https://github.com/HongshuW/EventB_Agent)。
- 归档入口：[Zenodo DOI 10.5281/zenodo.19642103](https://doi.org/10.5281/zenodo.19642103)。

**数据集获取方式**：
- 原文 §9 明确说明 datasets publicly available。
- 数据集与工具同入口公开：[GitHub](https://github.com/HongshuW/EventB_Agent) 与 [Zenodo](https://doi.org/10.5281/zenodo.19642103)。
- 论文正文说明数据集包含 27 个形式系统，来源包括 Abrial 的经典 Event-B 示例 / 算法，以及 real-world systems；经典算法和真实系统的自然语言需求文档由作者基于系统描述手工构造。

## 简报

本文提出 Event-B Agent：给定自然语言需求，LLM agent 先规划 refinement strategy，再逐层合成 Event-B 形式模型，并利用 ProB model checking、Rodin / SMT / theorem proving 的 proof obligation feedback 迭代修复模型和证明工件。它解决的不是一般代码生成问题，而是“自然语言需求 -> 可验证 Event-B 状态化形式模型 + proof obligation discharge”的端到端 autoformalization 与 repair 问题。

- **输入**：自然语言需求文档；实验中需求带轻量标签如 `EQP` / `FUN` 以便计算 RC / RF，但论文强调这些标签不编码建模结构，框架可处理 unstructured natural language。
- **方法**：GPT-5 medium reasoning 作为 backbone LLM；多个 LLM 角色分别负责 refinement planning、schema-guided model synthesis、counterexample/proof-state-guided repair 和 fix strategy selection；确定性工具负责 Event-B 编译、ProB model checking、SMT / theorem proving、repair rule pattern matching、atomic repair function execution 和 proof replay。
- **输出**：Event-B formal model refinement chain，包括 contexts、machines、variables、invariants、variants、events、guards、actions、gluing invariants，以及被验证 / 修复后的 proof artifacts；最终目标是生成满足需求覆盖并尽量 discharge POs 的 Event-B 模型。

```text
输入层：自然语言系统需求文档
  -> 方法层：LLM refinement planning + JSON schema formalization + model checking + theorem proving + proof-guided repair
  -> 输出层：Event-B contexts/machines/events/refinements + proof obligations/proof artifacts
```

实验在 27 个 Event-B 形式系统上进行，按需求数量分为 Simple / Medium / Complex 三组，每组 9 个系统。Event-B Agent 总体达到 PDR 97.86%、RC 97.13%、RF 93.79%，分别优于 LLM + auto provers、Cursor、adapted PAT-Agent 等 baseline。主要不足是当前 repair rules / atomic repair functions 仍不完备，需求一致性被假设成立，且输出是 Event-B 状态化形式模型而不是 Project 1 当前主要面向的层次化状态机 / timed automata DSL。

## 研究问题与动机

### 问题背景

形式化方法追求 correct-by-construction：系统在设计和开发阶段通过数学化规格与形式验证保证正确性，而不是部署后再靠测试发现问题。Event-B / B Method 这类方法通过模型、refinement、proof obligations、model checking 和 theorem proving 支持这种开发范式，但手工构造模型、证明和修复 proof failures 高度依赖形式化专家。

LLM 已经被用于 autoformalization、LTL synthesis、program specification generation、proof generation / repair 等任务，但这些工作常常只覆盖孤立环节：要么从自然语言生成某类公式，要么在固定模型上找 proof tactic，要么只用 bounded model checking 验证生成模型。论文认为真实形式化开发中模型和证明必须共同演化：证明失败可能来自模型错误，也可能来自自动证明能力不足，因此修复对象既可能是模型，也可能是 proof artifact。

### 核心问题

论文把任务抽象为模型构造与证明推导的联合状态空间。若 $M$ 是从形式模型抽取的公式集合，$\pi$ 是证明工件，proof obligation 为 $\varphi$，则目标不是只生成 $M$，也不是只搜索 $\pi$，而是在每一步保证存在有效证明使 $M \vdash_R \varphi$。形式开发过程被看作：

$$
(M_0,\pi_0) \leadsto (M_1,\pi_1) \leadsto ... \leadsto (M_n,\pi_n)
$$

其中 $M_0=\emptyset$，初始模型由自然语言需求合成，后续每一步允许模型和证明同时更新，并通过 sound proof system 检查。

### 研究动机

论文动机集中在三点：

1. **refinement 降低复杂度**：先在抽象模型中证明关键性质，再通过 refinement POs 保证后续具体模型保留已证明性质。
2. **model checking alone 不足**：bounded model checking 能发现 counterexample，但没有 counterexample 只代表给定 bound 内未发现问题；PAT-Agent 这类方法难以给出 unbounded correctness。
3. **证明反馈应反向驱动修复**：proof obligation 失败时，proof state 包含可用于修复 invariant、guard、action、axiom 或 proof tactic 的结构化信息。

### 研究意义

对 Project 1 而言，本文的意义在于把 LLM 生成状态化模型的比较维度从“生成语法正确的图 / 代码”推进到“生成可被形式化验证工具持续反馈和修复的状态化模型”。虽然 Event-B 不是本研究当前最主要的状态机表示，但它的 context / machine / event / guard / action / invariant / refinement 语义与 guarded state-transition model 高度接近，可为“生成-验证-修复”闭环提供强 baseline。

### 现有方法的局限性

论文明确指出：

1. LLM proof assistants 通常假设模型固定，只搜索证明，不能从自然语言需求构造模型，也不能在 proof failure 后修改模型。
2. LLM-based autoformalization 通常构造模型但缺少 proof-based verification / repair，多依赖 bounded model checking。
3. PAT-Agent 是最接近的 formal model construction agent，但主要面向 PAT model checking；在论文的 adapted setting 中，它不处理 theorem proving 和 proof obligations。
4. 直接使用 GPT-5 或 Cursor 生成 Event-B 模型时，可能覆盖需求但留下未证明性质、错误初始化、过强常量假设或 refinement 关系缺失。

### 研究目标

论文目标是构建一个端到端 Event-B formal model synthesis and repair 框架，使自然语言需求、refinement strategy、模型合成、model checking、theorem proving、proof-state analysis 和模型 / 证明修复形成闭环，并在每个 refinement level 通过 proof obligations 约束已接受修改。

## 核心方法

### 方法概述

Event-B Agent 的主流程分为三个阶段：

1. **Refinement Strategy Planning**：LLM 将自然语言需求划分到多个 refinement steps，并以自然语言提出相邻 refinement levels 之间的 gluing invariants。
2. **Model Synthesis**：对每个 refinement step，LLM 在 JSON schema 约束下生成候选 Event-B 模型；系统将 JSON 解析 / 编译为 Event-B code，编译错误反馈给 LLM 迭代修复 well-formedness。
3. **Model & Proof Repair**：模型先由 ProB 进行 bounded model checking；若发现 invariant violation，counterexample trace 反馈给 LLM 修复。随后生成 POs 并由 theorem provers / SMT solvers 尝试 discharge；proof failure 被分类为 proof-state categories，再由 LLM 在 repair rules 和 atomic repair functions 约束下选择修复策略。

### 形式化对象与输出结构

论文使用 Event-B 作为目标语言。Event-B model $M$ 包含：

- `Context`：sets、constants、axioms、theorems。
- `Machine`：variables、invariants、variants、theorems、events。
- `Event`：event identifier、parameters、guards、actions。

因此输出不是普通文本摘要，而是可进入 Rodin IDE 的 Event-B 规格。语义上，它是 grounded in set theory and first-order logic 的 discrete transition system；states 由变量取值表示，events with guards/actions 表示转移。

### Refinement Strategy Planning

Refinement planning 的作用是把大需求拆成一串更容易证明的模型层。给定需求集合 $REQ$，规划阶段将其划分为互不相交的 $REQ_{M_i}$，并在相邻层之间生成 gluing invariants $I_{g_i}$。例如 motivating example 中：

- 抽象层只处理终止时最小值性质 `FUN-1`。
- 具体层再引入扫描索引 `i`、候选索引 `j`、布尔变量 `searching` 以及迭代搜索过程 `FUN-2` 到 `FUN-6`。
- gluing invariant 描述抽象变量和具体变量之间的关系，如搜索过程中 $f(j)$ 是已扫描区间中的最小值。

这些 gluing invariants 不是直接信任 LLM 结果，而是先由 model checker 做 counterexample checking / contradiction detection，再优先尝试与其相关的 proofs；只有没有 counterexample 且 proofs 成功后才被接受。

### Schema-Guided Model Synthesis

论文指出，简单 prompt-based generation 容易产生 ill-formed Event-B code，例如未声明变量、错误 invariant、语法不符合 parser。为此作者设计了编码 Event-B grammar 的 JSON schema，使 LLM 首先生成结构化 JSON，再由系统解析和编译到 Rodin 可处理的 Event-B code。

这一层的反馈主要是：

- JSON / Event-B 结构约束。
- 编译错误。
- 类型错误、未声明变量、undefined set、well-formedness 问题。

这类似 Project 1 中希望使用 DSL schema / parser diagnostics 限制 LLM 生成空间的思路，但本文目标语言是 Event-B。

### Model Checking Feedback

新模型先由 ProB 检查：

- deadlock-freeness；
- liveliness；
- consistency of axioms；
- invariant preservation；
- requirement invariants 和 gluing invariants 的 bounded counterexample。

若发现 counterexample trace，trace 会作为反馈传给 model repair LLM，用于修复模型。论文明确承认 bounded model checking 不能保证全局正确性，因此它只是 repair loop 的第一层反馈。

### Theorem Proving and Proof-Guided Repair

第二层反馈来自 proof obligations。Rodin / integrated provers / SMT solvers 尝试 discharge POs；失败时，Event-B Agent 分析 proof state，并把失败归入若干 repair rule categories。论文 Table 2 给出 7 类：

1. Contradictory Goal。
2. True by Definition。
3. Existential Goal。
4. Equality PO。
5. Well-Definedness。
6. Quantified Invariant Preservation。
7. Uninstantiated Hypothesis。

这些类别不是证明 soundness 的来源，而是给 LLM 提供修复启发。真正的 soundness 来自：修复后的模型 / proof 必须重新通过 theorem proving / SMT / proof replay。

### Fix Strategy Selection and Atomic Repair Functions

为降低 LLM hallucination 风险，Event-B Agent 不允许 LLM 任意编辑模型，而是让 LLM 在 atomic repair functions 中选择函数并给出参数。论文列出的 repair function 类型包括：

- model modification：add / update invariant、strengthen guard、modify action 等；
- proof modification：instantiate quantified hypothesis、unfold definitional equality 等；
- joint model-proof modification：同时把 hypothesis 加到 context axiom 并注入 proof context；
- information retrieval：调用 model checker 获取额外 guidance。

在每次 model modification 后，系统会 replay all proofs，确保新修改没有破坏已成功证明的 POs。

### LLM / Agent 组成

论文实验使用 GPT-5 medium reasoning configuration, 2025-08-07 version 作为 backbone LLM。文中没有把 few-shot、CoT 或 RAG 作为核心方法变量；更关键的是：

- 固定 prompt structure；
- task-specific information programmatically injected；
- JSON schema constrained generation；
- formal verification feedback；
- repair rule recommendation；
- atomic tool/function selection。

因此该工作更适合归为 verifier-mediated LLM agent / neurosymbolic formal development，而不是单纯 prompt engineering baseline。

## 实验与评估

### 数据集

论文收集 27 个 formal systems：

- 来源包括 Jean-Raymond Abrial 的经典 B / Event-B examples and algorithms，以及 real-world systems。
- 对经典算法和真实系统，作者基于系统描述手工构造 requirement documents。
- 数据集按 requirement count 分为三组，每组 9 个系统：
  - Simple：3-8 个 requirements；
  - Medium：9-13 个 requirements；
  - Complex：14-24 个 requirements。
- Event-B Agent 生成模型的平均 PO 数随复杂度上升：Simple 约 89.22，Medium 约 173.7，Complex 约 284.3；总体平均每个系统 182.41 个 POs。

公开性：数据集公开，入口为 [GitHub](https://github.com/HongshuW/EventB_Agent) 和 [Zenodo](https://doi.org/10.5281/zenodo.19642103)。

### Baseline 设置

论文认为此前没有工作把 formal development 明确建模为 model construction + proof derivation 的联合过程。为了做经验比较，选择同输入输出设置下最接近的方法：

1. **LLM + auto provers**：LLM 直接生成 Event-B specifications，再用 Rodin 内置 provers、PP、CVC4、Z3 等 discharge POs。
2. **Cursor**：adapted general-purpose coding agent；禁用 web search，保留文件编辑、代码搜索、terminal execution；用高层任务指令生成 Event-B JSON、解析成模型并运行 model checker。
3. **Adapted PAT-Agent**：将原本为 PAT model checking autoformalization 设计的 PAT-Agent 适配到 Event-B：改写语法文档和示例、把 PAT model checker 替换为 ProB、输出 Event-B models；但由于 PAT-Agent 只关注 model checking，仍不处理 proof obligations。

所有 baseline 输出后都再运行 automated provers，以保持 PDR 指标可比。

### 评估指标

论文使用三个核心指标：

- **PDR / Proof Obligation Discharge Rate**：已 discharge POs 占全部 POs 的比例，用于衡量模型 consistency。
- **RC / Requirement Coverage**：需求是否被模型元素覆盖，依赖 LLM 在生成过程中为模型元素标注 requirement labels。
- **RF / Requirement Fulfillment**：需求不仅被覆盖，而且相关 POs 被 discharge。

RC / RF 跨 refinement layers 计算时有一个关键假设：若某 requirement 在抽象模型中 covered and fulfilled，并且后续 refinement POs 被 discharge，则该 requirement 在具体 refinement 中继续成立。论文用 Refinement PDR 报告这一假设的经验可信度。

### 主要实验结果

RQ1 的总体结果：

| 方法 | PDR | RC | RF |
|---|---:|---:|---:|
| LLM + auto provers | 0.8920 | 0.9250 | 0.6896 |
| Cursor | 0.9007 | 0.8928 | 0.6886 |
| PAT-Agent | 0.9556 | 0.9205 | 0.7578 |
| Event-B Agent | 0.9786 | 0.9713 | 0.9379 |

关键结论：

- Event-B Agent 达到 PDR 97.86%，未 discharge POs 约 2.14%。
- RC 97.13%，RF 93.79%，均为最高。
- 相比第二好方法，RC 高 4.63%，RF 高 18.01%。
- RF / RC 比例约 0.97，说明一旦需求被捕获，Event-B Agent 基本能 discharge 相应 POs。
- Event-B Agent 在 Simple / Medium / Complex 三组中都维持 PDR 97% 以上。

### 消融实验

RQ2 比较 refinement 和 repair guidance 的贡献。三个 ablation baselines 为：

1. None enabled：去掉 refinement 和 repair guidance。
2. Refinement only：保留 refinement，去掉 repair guidance。
3. Repair guidance only：去掉 refinement，保留 repair guidance。

总体结果：

| 方法 | PDR | RC | RF |
|---|---:|---:|---:|
| None enabled | 0.9559 | 0.8363 | 0.7701 |
| Refinement only | 0.9650 | 0.8955 | 0.8350 |
| Repair guidance only | 0.9693 | 0.9494 | 0.8665 |
| Event-B Agent | 0.9786 | 0.9713 | 0.9379 |

Refinement PDR 从 `Refinement only` 的 overall 0.6769 提升到 Event-B Agent 的 0.9256，说明仅有 refinement 不足，必须结合 proof-guided repair 来保障 refinement links。

### 效率

RQ3 中 Event-B Agent 平均每个系统：

- overall time：74.45 minutes；
- LLM calls：57.33；
- tokens：1,657,865.15；
- refinement strategy planning：约 1.20 minutes，1 次 LLM call；
- model synthesis：约 25.07 minutes，13.59 calls；
- model & proof repair：约 43.71 minutes，42.74 calls；
- 平均每个 PO 的 discharge 尝试时间约 0.24 minutes。

论文解释，repair 成本主要随 PO 数量增长，而不是随系统复杂度失控增长；许多 POs 可由自动 prover 直接 discharge，剩余 POs 才需要 LLM repair。

### Repair 行为分析

RQ4 展示了 refinement steps 中 PDR / RC / RF 的演化，以及成功 discharge POs 的 atomic repair function 分布：

- model modifications：38.36%；
- proof modifications：33.62%；
- joint model-proof modifications：18.97%；
- information retrieval：9.10%。

这说明 Event-B Agent 并非只在模型层修补，也大量使用 proof-level 和 model-proof joint 修复。

### 方法优势

1. **验证反馈强**：同时使用 model checking 和 theorem proving，不只依赖 bounded counterexample。
2. **修复对象完整**：允许修改模型、证明或二者联合，而不是把 proof failure 简化成重新生成模型。
3. **refinement 与 repair 互补**：refinement 降低单步证明复杂度，repair 提高 refinement POs discharge 率。
4. **公开性较好**：代码、数据集和接口均公开，适合后续复现实验或作为 Project 1 baseline 资源。
5. **证据链较强**：指标不仅看语法正确或人工评分，还看 PDR、RC、RF、Refinement PDR、运行成本和 repair function distribution。

### 方法的局限性

1. **输出类型异构**：输出是 Event-B formal model，不是 UML Statechart / SysML state machine / timed automata DSL；与 Project 1 对比时需要明确模型类型适配。
2. **不直接处理时间约束**：论文主线是 Event-B refinement、invariants、guards、proof obligations，未把 timed automata clock constraints 作为核心对象。
3. **repair library 不完备**：repair rules 和 atomic functions 来自作者经验，复杂 proof states 可能超出当前库覆盖。
4. **需求一致性假设**：实验假设 requirements internally consistent；真实工业需求中不一致需求需要 human-in-the-loop，留作未来工作。
5. **RC / RF 依赖标签与 refinement assumption**：模型元素 requirement labels 有时格式不符合预期，作者手工修正以保证公平；跨 refinement 的 RC / RF 计算依赖 refinement PDR。
6. **LLM nondeterminism 仍存在**：论文用 schema constraints 和 verifier-mediated acceptance 降低影响，但不保证每次生成 identical model。
7. **数据集需求文档有人工构造成分**：classic algorithms 和 real-world systems 的 requirement documents 由作者基于系统描述手工构造；这可能比真实非结构化工业需求更规整。

## 与本研究的关系

### 相关性分析

**BASELINE评估：🟠（近直接 formal-state baseline，但不是同构状态机输出）**。

理由如下：

1. 输入是自然语言系统需求文档，与 Project 1 “从非形式化 / 半形式化需求生成状态机模型”的入口高度一致。
2. 输出是 Event-B contexts / machines / events / guards / actions / invariants / refinement chain。它不是图形化状态机，但 Event-B 本质上是 event/state-based discrete transition system，模型元素与 guarded state machine 的 state-transition semantics 高度接近。
3. 方法包含 LLM generation、schema constraints、verification feedback、repair loop、refinement 和 proof replay，正好覆盖 Project 1 关心的“生成-验证-修复”闭环。
4. 与现有 Project 1 baseline 相比，本文形式化验证强度显著更高，可作为强验证闭环 baseline；但不能把它与直接生成 UML / SysML state machine 的论文混为同一种输出类型。

因此建议在 SUMMARY 表中将其放入“直接状态化形式模型生成 / formal state-based model synthesis”或“直接生成但输出类型异构”的子类。若 Project 1 的主输出坚持为层次化状态机 / timed automata，则比较时应说明需经过语义映射或只比较生成流程、验证反馈和修复能力。

### 可借鉴之处

1. **结构化输出 schema**：Event-B JSON schema 对 Project 1 的 DSL / pyfcstm grammar 约束有直接借鉴意义。状态机生成不应只靠自然语言 prompt，而应让 LLM 输出 machine-readable structured IR。
2. **diagnostics 分层**：论文把 compilation errors、counterexample traces、proof states、proof obligation types 分层作为反馈，避免把所有错误都塞回 prompt。Project 1 可对应使用 parser diagnostics、semantic diagnostics、simulation traces、model checking results。
3. **atomic repair functions**：限制 LLM 在可审计的 atomic functions 中选择，比让 LLM 任意重写模型更容易保证修复可追踪、可回放、可归因。
4. **refinement planning**：先让 LLM 规划抽象到具体的 refinement steps，有助于处理复杂控制系统需求中层次、阶段、模式、异常处理的分解。
5. **verification-gated acceptance**：soundness 不是来自 LLM 自我解释，而是来自工具链重新验证；这与 Project 1 的学术证据链要求一致。
6. **公开 benchmark 与 run metadata**：论文公开 GitHub / Zenodo 工件，可作为复现、对照或数据集设计参考。

### 存在的不足与改进空间

1. **与控制系统状态机的语义差距**：Event-B 可表达状态化行为，但不直接提供状态层级、orthogonal regions、entry/exit actions、timed automata clocks 等 Project 1 常用目标结构。
2. **需求输入仍偏实验规整**：虽然论文称可处理 unstructured natural language，但评估需求文档带 `EQP` / `FUN` 等轻量标签，并且许多需求由作者从已知 Event-B 系统描述手工构造。
3. **对已知缺陷修复的可迁移性需验证**：本文修复主要面向 POs 和 proof states；Project 1 若面对的是状态遗漏、guard/action mismatch、时间约束错配、层次结构错误，需要建立自己的 repair category taxonomy。
4. **模型检查与定理证明成本较高**：平均每系统 74.45 minutes，token 消耗较大；Project 1 若要大规模评测，需要设计更轻量的 smoke / replay / eligibility policy。
5. **baseline 公平性要拆开看**：若 Project 1 输出目标是 pyfcstm / timed state machine，Event-B Agent 不能作为“同格式直接对比”，更适合做“formal verification loop upper baseline / heterogeneous baseline”。

### 对本研究的启发

Project 1 可把本文作为“强验证闭环 baseline”来定义自己的方法差异：

- 本研究若输出控制系统状态机，应证明自己不仅能生成状态、转移、guard、action，还能保留 traceability 到需求项，并能接受 parser / semantic / model-checker diagnostics。
- 可以借鉴 Event-B Agent 的 repair taxonomy 设计，但将 proof-state categories 替换为状态机领域 diagnostics categories，例如 unreachable state、nondeterminism、guard conflict、missing transition、invariant violation、timing bound violation、deadlock / livelock。
- 可以把 refinement strategy planning 转化为“先抽象控制模式，再细化事件、时间约束和异常处理”的 staged generation。
- 在论文写作中，Event-B Agent 可用于论证：LLM 形式模型生成正在从 direct text-to-code 走向 verifier-mediated agentic repair；Project 1 的创新点必须明确说明自己在状态机族模型、控制系统语义和可复现实验证据链上的增量。

## 重要的相关工作

### 1. 重要的前身类工作

#### Abrial 1996 / 2010：B Method 与 Event-B 基础 [1][2]

- **基本信息**：Jean-Raymond Abrial，1996，*The B-book: Assigning Programs to Meaning*；Jean-Raymond Abrial，2010，*Modeling in Event-B: System and Software Engineering*。
- **主要内容**：B / Event-B 的核心理论、refinement、proof obligations、set theory / first-order logic 建模基础。
- **论文中的引用位置或引用语义**：§1、§3 和 §5.1 多次作为 B Method、Event-B notation、correct-by-construction、经典 examples / algorithms 的来源。
- **与本论文的关系**：提供目标建模语言、proof obligation 语义、refinement 开发范式和数据集经典示例来源。
- **支撑作用**：没有 Event-B 的模型 / proof obligation / refinement 机制，Event-B Agent 的 verifier-mediated synthesis and repair pipeline 无法成立。

#### PAT-Agent：Autoformalization for Model Checking [3]

- **基本信息**：Xinyue Zuo 等，2025，*PAT-Agent: Autoformalization for Model Checking*，ASE 2025。
- **主要内容**：面向 PAT 的 formal model autoformalization agent，使用 model checking feedback 合成和修复模型。
- **论文中的引用位置或引用语义**：§1、§2.1、§5.1、§6.1 均称其为 closest work / baseline，并在实验中适配到 Event-B。
- **与本论文的关系**：最重要的直接前身和直接实验 baseline。
- **主要局限性**：论文认为 PAT-Agent 主要依赖 model checking，不处理 theorem proving 和 proof obligations，因此难以提供 unbounded correctness。

#### B / Event-B 模型构造、refinement、repair 与 code generation 传统工作 [4][5][6][7][8][9][10][11][12]

- **基本信息**：包括 Alkhammash et al. 2015 traceable Event-B models from requirements；Cai et al. 2019 / 2022 B-model repair；Dupont et al. 2021 Event-B hybridation；Mashkoor et al. 2017 refinement-based validation；Kobayashi and Ishikawa 2024 Event-B repair by quantifier elimination；Fürst et al. 2014 / Méry and Singh 2011 / Rivera et al. 2017 Event-B code generation。
- **主要内容**：传统 Event-B 建模、验证、修复和代码生成链条，多依赖人工建模或特定修复算法。
- **论文中的引用位置或引用语义**：§6.1 中作为 beyond LLMs 的 B / Event-B community 进展。
- **与本论文的关系**：提供 formal methods 背景和若干 repair / refinement 思路，但本文强调其不构成自动化 LLM synthesis-repair unified framework。

### 2. 直接参与实验的 baseline

#### LLM Model Synthesis with Automated Provers

- **基本信息**：论文自行构造的 baseline，不是单篇外部论文。
- **主要内容**：用 GPT-5 medium reasoning 直接生成 Event-B specifications，再调用 Rodin 内置 provers、PP、CVC4、Z3 等自动证明工具。
- **论文中的引用位置或引用语义**：§5.1 Baselines 和 Table 3。
- **与本论文的关系**：检验“只靠 LLM 生成 + 自动 prover”能达到什么水平。
- **结果**：Overall PDR 0.8920，RC 0.9250，RF 0.6896；明显低于 Event-B Agent。

#### Cursor：Adapted General Purpose Coding Agent [13]

- **基本信息**：Anysphere, Inc.，2025，Cursor: The AI Code Editor。
- **主要内容**：通用 coding LLM agent，具备文件编辑、代码搜索、terminal execution 等能力。
- **论文中的引用位置或引用语义**：§5.1 作为 adapted general-purpose coding agent baseline。
- **与本论文的关系**：检验通用 coding agent 在 Event-B formal model synthesis setting 下的表现。
- **结果**：Overall PDR 0.9007，RC 0.8928，RF 0.6886；PDR 随复杂度波动较大。

#### Adapted PAT-Agent [3]

- **基本信息**：Zuo et al.，2025，*PAT-Agent: Autoformalization for Model Checking*，ASE 2025。
- **主要内容**：原本生成 PAT 模型并用 model checking 验证；本文将其适配为生成 Event-B 模型、用 ProB 反馈，但不处理 POs。
- **论文中的引用位置或引用语义**：§5.1 和 Table 3。
- **与本论文的关系**：最强外部 baseline。
- **结果**：Overall PDR 0.9556，RC 0.9205，RF 0.7578；PDR 高于 GPT-5 direct 和 Cursor，但 RF 与 Event-B Agent 差距明显。

### 3. 提供了重要论证的工作

#### LTL autoformalization / property synthesis [14][15]

- **基本信息**：Cosler et al. 2023，*nl2spec*，CAV；Fuggitti and Chakraborti 2023，*NL2LTL*，AAAI。
- **主要内容**：将自然语言转成 temporal logic / LTL formulas。
- **论文中的引用位置或引用语义**：§1 和 §6.1 用来说明 LLM autoformalization 已覆盖 temporal logic synthesis。
- **与本论文的关系**：支撑“已有 autoformalization 工作多处理局部 specification fragment，尚不足以构造完整 system-level formal model”的动机。

#### Program specification generation / verification with LLMs [16][17]

- **基本信息**：Wen et al. 2024，*Enchanting program specification synthesis by large language models using static analysis and program verification*，CAV；Wu et al. 2023，*Lemur: Integrating large language models in automated program verification*。
- **主要内容**：使用 LLM 生成程序规格或辅助程序验证。
- **论文中的引用位置或引用语义**：§1 和 §6.1。
- **与本论文的关系**：作为 autoformalization 相邻方向，说明 LLM 已能辅助 specs，但多限于程序级局部任务。

#### Alloy / B-Method 的 LLM formal specification 研究 [18][19]

- **基本信息**：Capozucca et al. 2025，*Do AI assistants help students write formal specifications? A study with ChatGPT and the B-method*，CSEE&T；Hong et al. 2025，*On the Effectiveness of Large Language Models in Writing Alloy Formulas*。
- **主要内容**：研究 LLM 生成 B-method 或 Alloy formal specifications 的能力。
- **论文中的引用位置或引用语义**：§1 和 §6.1 称其为 recent attempts at system-level models / limited direct text-to-code mappings。
- **与本论文的关系**：支撑“已有 system-level formal model LLM 工作仍缺少系统化 iterative verification and repair framework”的论证。

#### Trustworthy AI agents and formal methods position work [20]

- **基本信息**：Yedi Zhang 等，2025，*Position: Trustworthy AI Agents Require the Integration of Large Language Models and Formal Methods*，ICML Position Paper Track。
- **主要内容**：论证可信 AI agents 需要结合 LLM 与 formal methods。
- **论文中的引用位置或引用语义**：§1 和 §6.1。
- **与本论文的关系**：提供宏观动机，即 LLM agent 应与可验证 symbolic tools 结合。

### 4. 在技术上提供了支持的工作

#### Rodin IDE [21]

- **基本信息**：Heinrich Heine University Düsseldorf，2025，*Rodin User's Handbook v.2.8*。
- **主要内容**：Event-B IDE，支持结构化 Event-B 模型、proof obligations、theorem proving、SMT integration。
- **论文中的引用位置或引用语义**：§1 contribution、§5.1 Tool。
- **与本论文的关系**：Event-B Agent 的实现集成目标，是模型编译、proof obligations 和 proof replay 的关键工具。

#### ProB model checker [22]

- **基本信息**：Heinrich Heine University Düsseldorf，2025，*ProB Animator and Model Checker*。
- **主要内容**：Event-B model checker / animator，支持 deadlock、liveliness、axiom consistency、invariant preservation 检查。
- **论文中的引用位置或引用语义**：§5.1 Tool；§4.4 formal verification and repair。
- **与本论文的关系**：负责 bounded counterexample feedback，作为 theorem proving 前的模型检查层。

#### SMT solvers CVC4 / Z3 [23][24]

- **基本信息**：Barrett et al. 2011，CVC4，CAV；De Moura and Bjørner 2008，Z3，TACAS。
- **主要内容**：SMT solving。
- **论文中的引用位置或引用语义**：§5.1 Baselines 中作为 Rodin integrated SMT solvers。
- **与本论文的关系**：用于 proof obligation discharge，是 PDR 指标和 proof-guided repair acceptance 的底层验证能力之一。

#### Proof tactic recommendation / LLM theorem proving 工作 [25][26][27][28][29][30][31][32][33][34][35][36][37]

- **基本信息**：包括 PaMpeR、TacticToe、Tactician、PSL、MagnusHammer、LeanDojo、LeanAgent、Lean-STaR、Baldur、CoqPyt、Proof automation with LLMs 等。
- **主要内容**：在 Isabelle/HOL、HOL4、Coq、Lean 等环境中推荐 tactic、生成 proof steps、做 premise selection 或 retrieval-augmented theorem proving。
- **论文中的引用位置或引用语义**：§6.3 Proof Tactic Recommendation。
- **与本论文的关系**：提供 proof guidance 背景；本文差异是把 tactic / proof guidance 嵌入模型构造、verification 和 repair 联合流程，而不是在固定证明任务中单独预测 tactics。

#### Neurosymbolic programming [38]

- **基本信息**：Chaudhuri et al. 2021，*Neurosymbolic programming*，Foundations and Trends in Programming Languages。
- **主要内容**：结合 neural learning 的表达能力和 symbolic reasoning 的可验证性。
- **论文中的引用位置或引用语义**：§6.2 Neurosymbolic Methods。
- **与本论文的关系**：提供方法学定位。Event-B Agent 把语义生成交给 LLM，把可接受性和 soundness 交给 Event-B 工具链。

### 5. 其他重要工作

#### Real-world Event-B systems 来源 [39][40]

- **基本信息**：Riviere et al. 2023，*Formalising liveness properties in Event-B with the reflexive EB4EB framework*，NASA Formal Methods；Riviere et al. 2025，*Extending the EB4EB framework with parameterised events*，Science of Computer Programming。
- **主要内容**：Event-B framework / real-world systems 相关工作。
- **论文中的引用位置或引用语义**：§5.1 Dataset。
- **与本论文的关系**：为 27 个 formal systems 数据集中的 real-world systems 提供来源。

#### GPT-4 / GPT-5 模型背景 [41][42]

- **基本信息**：OpenAI 2023，GPT-4 Technical Report；OpenAI 2025，GPT-5。
- **主要内容**：LLM backbone 背景。
- **论文中的引用位置或引用语义**：§1 讨论 LLM 兴起；§5.1 指定 GPT-5 medium reasoning 为 backbone LLM。
- **与本论文的关系**：提供底层 LLM 能力，但论文贡献不在提出新模型，而在 agentic formal development workflow。

## 文献分类总结

Event-B Agent 位于三条研究链的交汇处：

1. **Event-B / B Method correct-by-construction 链条**：Abrial 的 B / Event-B 理论、Rodin、ProB、SMT / theorem proving、refinement 和 proof obligations 构成本文的 symbolic backbone。
2. **LLM autoformalization 链条**：LTL、program specs、Alloy、B-method、PAT-Agent 等工作说明 LLM 已能把自然语言转为形式规格，但大多缺少完整的模型 / 证明共同演化。
3. **Proof-guided repair / neurosymbolic agent 链条**：proof tactic recommendation 和 neurosymbolic programming 提供背景，本文则把这些思想用于 Event-B 模型合成、验证反馈和 repair loop。

在 Project 1 baseline 体系中，本文不应被简单归为普通“状态机图生成”论文，而应标为“自然语言到状态化形式模型 + 强形式验证闭环”的近直接异构 baseline。它对 Project 1 最大价值不是输出格式，而是展示了一种可复现实验和强证据链：输入需求、结构化模型、验证诊断、修复动作、proof replay、公开数据集和明确指标共同构成可审计闭环。

## References

[1] Jean-Raymond Abrial. 1996. *The B-book: Assigning Programs to Meaning*. Cambridge University Press. DOI: 10.1017/CBO9780511624162.

[2] Jean-Raymond Abrial. 2010. *Modeling in Event-B: System and Software Engineering*. Cambridge University Press. DOI: 10.1017/CBO9781139195881.

[3] Xinyue Zuo et al. 2025. *PAT-Agent: Autoformalization for Model Checking*. ASE. DOI: 10.48550/arXiv.2509.23675.

[4] Eman Alkhammash, Michael Butler, Asieh Salehi Fathabadi, and Corina Cirstea. 2015. *Building Traceable Event-B Models from Requirements*. Science of Computer Programming. DOI: 10.1016/j.scico.2015.06.002.

[5] Cheng-Hao Cai, Jing Sun, and Gillian Dobbie. 2019. *Automatic B-model Repair Using Model Checking and Machine Learning*. Automated Software Engineering. DOI: 10.1007/s10515-019-00264-4.

[6] Cheng-Hao Cai et al. 2022. *Fast Automated Abstract Machine Repair Using Simultaneous Modifications and Refactoring*. Formal Aspects of Computing. DOI: 10.1145/3536430.

[7] Guillaume Dupont, Yamine Ait-Ameur, Neeraj Kumar Singh, and Marc Pantel. 2021. *Event-B Hybridation: A Proof and Refinement-Based Framework for Modelling Hybrid Systems*. ACM Transactions on Embedded Computing Systems. DOI: 10.1145/3448270.

[8] Andreas Furst et al. 2014. *Code Generation for Event-B*. Integrated Formal Methods. DOI: 10.1007/978-3-319-10181-1_20.

[9] Tsutomu Kobayashi and Fuyuki Ishikawa. 2024. *Repairing Event-B Models Through Quantifier Elimination*. International Conference on Formal Engineering Methods. DOI: 10.1007/978-981-96-0617-7_2.

[10] Atif Mashkoor, Faqing Yang, and Jean-Pierre Jacquot. 2017. *Refinement-based Validation of Event-B Specifications*. Software & Systems Modeling. DOI: 10.1007/s10270-016-0514-4.

[11] Dominique Mery and Neeraj Kumar Singh. 2011. *Automatic Code Generation from Event-B Models*. Symposium on Information and Communication Technology. DOI: 10.1145/2069216.2069252.

[12] Victor Rivera, Nestor Catano, Tim Wahls, and Camilo Rueda. 2017. *Code Generation for Event-B*. International Journal on Software Tools for Technology Transfer. DOI: 10.1007/s10009-015-0381-2.

[13] Anysphere, Inc. 2025. *Cursor: The AI Code Editor*. URL: https://cursor.com/.

[14] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. *nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models*. CAV. DOI: 10.1007/978-3-031-37703-7_18.

[15] Francesco Fuggitti and Tathagata Chakraborti. 2023. *NL2LTL: A Python Package for Converting Natural Language Instructions to Linear Temporal Logic Formulas*. AAAI. DOI: 10.1609/aaai.v37i13.27068.

[16] Cheng Wen et al. 2024. *Enchanting Program Specification Synthesis by Large Language Models Using Static Analysis and Program Verification*. CAV. DOI: 10.1007/978-3-031-65630-9_16.

[17] Haoze Wu, Clark Barrett, and Nina Narodytska. 2023. *Lemur: Integrating Large Language Models in Automated Program Verification*. arXiv. DOI: 10.48550/arXiv.2310.04870.

[18] Alfredo Capozucca, Daniil Yampolskyi, Alexander Goldberg, and Maximiliano Cristia. 2025. *Do AI Assistants Help Students Write Formal Specifications? A Study with ChatGPT and the B-method*. CSEE&T. DOI: 10.1109/CSEET66350.2025.00009.

[19] Yang Hong, Shan Jiang, Yulei Fu, and Sarfraz Khurshid. 2025. *On the Effectiveness of Large Language Models in Writing Alloy Formulas*. arXiv. DOI: 10.48550/arXiv.2502.15441.

[20] Yedi Zhang et al. 2025. *Position: Trustworthy AI Agents Require the Integration of Large Language Models and Formal Methods*. ICML Position Paper Track. URL: https://openreview.net/forum?id=wkisIZbntD.

[21] Heinrich Heine University Dusseldorf, Group for Software Engineering and Programming Languages. 2025. *Rodin User's Handbook v.2.8*. URL: https://stups.hhu-hosting.de/handbook/rodin/current/html/introduction.html.

[22] Heinrich Heine University Dusseldorf, Group for Software Engineering and Programming Languages. 2025. *ProB Animator and Model Checker*. URL: https://prob.hhu.de/.

[23] Clark Barrett et al. 2011. *CVC4*. International Conference on Computer Aided Verification. DOI: 10.1007/978-3-642-22110-1_14.

[24] Leonardo De Moura and Nikolaj Bjorner. 2008. *Z3: An Efficient SMT Solver*. TACAS. DOI: 10.1007/978-3-540-78800-3_24.

[25] Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. *The Tactician: A Seamless, Interactive Tactic Learner and Prover for Coq*. International Conference on Intelligent Computer Mathematics. DOI: 10.1007/978-3-030-53518-6_17.

[26] Pedro Carrott et al. 2024. *CoqPyt: Proof Navigation in Python in the Era of LLMs*. Companion Proceedings of FSE. DOI: 10.1145/3663529.3663814.

[27] Emily First et al. 2023. *Baldur: Whole-proof Generation and Repair with Large Language Models*. ESEC/FSE. DOI: 10.1145/3611643.3616243.

[28] Thibault Gauthier et al. 2021. *TacticToe: Learning to Prove with Tactics*. Journal of Automated Reasoning. DOI: 10.1007/s10817-020-09580-x.

[29] Fabian Gloeckle, Baptiste Roziere, Amaury Hayat, and Gabriel Synnaeve. 2023. *Temperature-scaled Large Language Models for Lean Proofstep Prediction*. Mathematical Reasoning and AI at NeurIPS.

[30] Adarsh Kumarappan et al. 2024. *LeanAgent: Lifelong Learning for Formal Theorem Proving*. arXiv. DOI: 10.48550/arXiv.2410.06209.

[31] Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming Yang. 2024. *Lean-STaR: Learning to Interleave Thinking and Proving*. arXiv. DOI: 10.48550/arXiv.2407.10040.

[32] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. 2024. *Proof Automation with Large Language Models*. ASE. DOI: 10.1145/3691620.3695521.

[33] Maciej Mikula et al. 2023. *MagnusHammer: A Transformer-based Approach to Premise Selection*. arXiv. DOI: 10.48550/arXiv.2303.04488.

[34] Yutaka Nagashima and Yilun He. 2018. *PaMpeR: Proof Method Recommendation System for Isabelle/HOL*. ASE. DOI: 10.1145/3238147.3238210.

[35] Yutaka Nagashima and Ramana Kumar. 2017. *A Proof Strategy Language and Proof Script Generation for Isabelle/HOL*. CADE. DOI: 10.1007/978-3-319-63046-5_32.

[36] Haiming Wang et al. 2024. *Proving Theorems Recursively*. NeurIPS. DOI: 10.52202/079017-2753.

[37] Kaiyu Yang et al. 2023. *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models*. NeurIPS. URL: https://proceedings.neurips.cc/paper_files/paper/2023/file/4441469427094f8873d0fecb0c4e1cee-Paper-Datasets_and_Benchmarks.pdf.

[38] Swarat Chaudhuri et al. 2021. *Neurosymbolic Programming*. Foundations and Trends in Programming Languages. DOI: 10.1561/2500000049.

[39] Peter Riviere, Neeraj Kumar Singh, Yamine Ait-Ameur, and Guillaume Dupont. 2023. *Formalising Liveness Properties in Event-B with the Reflexive EB4EB Framework*. NASA Formal Methods. DOI: 10.1007/978-3-031-33170-1_19.

[40] Peter Riviere, Neeraj Kumar Singh, Yamine Ait-Ameur, and Guillaume Dupont. 2025. *Extending the EB4EB Framework with Parameterised Events*. Science of Computer Programming. DOI: 10.1016/j.scico.2025.103279.

[41] Josh Achiam et al. 2023. *GPT-4 Technical Report*. arXiv. DOI: 10.48550/arXiv.2303.08774.

[42] OpenAI. 2025. *GPT-5*. URL: https://openai.com/gpt-5/.
