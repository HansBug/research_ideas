# 从 `ccf_history` 出发重排 `project_1` 文献优先级（以 `pyfcstm/FCSTM` 为目标工件）

## 1. 这份讨论稿现在要回答什么

这份讨论稿不再只回答“`ccf_history` 里哪些论文像状态机生成”，而是要回答更贴近论文写作的三个问题：

1. 如果 `project_1` 真正要生成的是 `pyfcstm` 的可执行 `FCSTM`，那么现有文献里哪些才算真正值得优先盯的 direct baseline。
2. 除 direct baseline 之外，哪些文献实际上补在 `需求规整化 -> 约束桥接 -> 状态机综合 -> 检查/修复 -> 可执行化/验证` 这条链上，应该被当成强前置工作。
3. 除了“别人怎么生成模型”，还有哪些控制系统文献定义了我们到底要生成什么样的状态机语义，这些文献虽然不是 baseline，但必须进入 related work 或 problem framing。

因此，这一版 discussion 采用三层口径：

1. **任务层 direct baseline**
   - 输入是自然语言需求、user story、use case、scenario 或相近文本工件；
   - 输出是状态机、statechart、SysML state machine 或高度等价的行为模型。
2. **表示层强前置**
   - 不一定直接输出状态机，但明确补在 `requirements normalization`、`constraint extraction`、`behavior synthesis`、`correctness checking`、`repair loop`、`executable semantics` 上。
3. **目标语义 exemplar**
   - 它们不是生成方法论文；
   - 但它们清楚定义了控制系统状态机该有什么语义槽位，例如层次模式、guard/interlock、异常恢复、时间窗口、模式切换约束；
   - 这类文献对 `FCSTM` 的 problem definition 非常关键。

这里额外说明一个变化：

1. 这一版除了继续用 `frontier_index/ccf_history/` 的筛选结果，还补看了 `project_1_llm_state_machine_modeling/baselines/`、`project_1_llm_state_machine_modeling/sources/`，以及最近出现的新论文。
2. 因此，下面的“重点文献”已经不再局限于 `ccf_history` 清单，而是面向 `FCSTM` 任务重新排过一轮优先级。

## 2. 总判断

我现在的判断比上一版更明确：

1. 如果目标只是“从文本生成一个泛 UML 状态机图”，近两年已经出现了若干 LLM 直接方法。
2. 但如果目标收敛为 **`control-system NL requirements -> semantically closed executable FCSTM core`**，那么现有工作仍然是“局部对齐多、整体对齐少”。
3. 真正值得论文重点盯的，不是一串混在一起的 related work，而是三类文献：
   - `A` 类：直接做文本到状态机建模；
   - `B` 类：补需求规整、约束桥接、检查修复、可执行化；
   - `C` 类：定义控制系统状态机目标语义的 exemplar。
4. 这一轮补查后，最应该上调优先级的新条目，是 `2026` 的 [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](https://arxiv.org/abs/2604.00275)。
   - 它直接做 **非结构化自然语言需求 -> UML state machine**；
   - 不是泛 MBSE，不是泛 UML，不是顺序图；
   - 而且它显式比较了 single-prompt、structure-driven、event-driven 和 hybrid 四种生成组织方式。
5. 这一轮补查后，还必须补上一层此前明显不够突出的文献：来自 [sources/](../sources/README.md) 的控制系统 exemplar。
   - 这些文献不回答“怎么让 LLM 生成状态机”；
   - 但它们回答“控制系统状态机到底该长成什么样”，这对 `FCSTM` 的任务定义比很多泛 UML 论文都更重要。
6. 因而，后续写 `project_1` 论文时，不能再把所有相关工作都压成一段“已有工作从需求生成状态机”。
   更合理的结构应该是：
   - `文本到状态机 direct baseline`
   - `需求规整/约束桥接前置`
   - `状态机综合/检查/修复前置`
   - `控制系统目标语义 exemplar`

## 3. 先把目标工件说清楚：`project_1` 实际要生成的是 `pyfcstm` 的 `FCSTM`

### 3.1 更合适的任务定义

如果按现在的真实研究落点来写，`project_1` 的问题不应该再被表述成：

> 从自然语言需求自动生成状态机图。

而更应该表述成：

> 从控制系统自然语言需求、设计说明或邻近文本工件中，自动构建可执行的 `FCSTM` 模型，并使其能够进入后续仿真、验证、修复与代码生成链路。

从论文视角，这里的目标工件更接近：

$$
M_{\mathrm{fcstm}} = (V, S, s_r, E_{\mathrm{loc}}, E_{\mathrm{chain}}, E_{\mathrm{abs}}, T, A_{\mathrm{enter}}, A_{\mathrm{during}}, A_{\mathrm{exit}}, A_{\mathrm{aspect}}, P)
$$

其中：

1. $V$ 是全局类型化变量。
2. $S$ 是层次状态集合，$s_r$ 是唯一根状态。
3. $E_{\mathrm{loc}} / E_{\mathrm{chain}} / E_{\mathrm{abs}}$ 对应 `::`、`:`、`/` 三种事件作用域。
4. $T$ 是带 `event / guard / effect` 的转换集合。
5. $A_{\mathrm{enter}} / A_{\mathrm{during}} / A_{\mathrm{exit}} / A_{\mathrm{aspect}}$ 表示生命周期动作与切面动作。
6. $P$ 表示伪状态、复合状态、可停止状态等执行相关属性。

### 3.2 `FCSTM` 相对一般 statechart 的关键额外语义

根据 [pyfcstm README](../../../pyfcstm-2/README.md)、[DSL 教程](../../../pyfcstm-2/docs/source/tutorials/dsl/index_zh.rst) 和 [仿真指南](../../../pyfcstm-2/docs/source/tutorials/simulation/index_zh.rst)，`FCSTM` 至少有下面这些对论文 framing 很关键的点：

1. 它是**单根层次状态机**，不是任意散图。
2. 它要求**全局类型化变量**，并让变量直接进入 guard 和 effect。
3. 它把事件分成三种作用域：
   - `::` 本地事件；
   - `:` 链事件；
   - `/` 绝对事件。
4. 它把转换看成 `source -> target + event + guard + effect` 的可执行单元，而不是单纯图形连线。
5. 它显式支持 `enter / during / exit`、复合状态 `during before / after`、以及祖先切面动作。
6. 它有明确 cycle 语义，包括事件解析、当前活动状态上的迁移选择、入口链跟随、可停止状态约束与守卫优先级。

因此，很多论文虽然也输出 “state machine”，但如果不涉及：

1. 层次模式组织；
2. guard/effect；
3. 控制动作与生命周期；
4. 可执行 cycle 语义；
5. 后续验证或代码生成；

那么它们最多只能算任务层相近，而不能算 `FCSTM` 表示层等价。

### 3.3 baseline 口径必须跟着变

一旦按 `FCSTM` 来看，baseline 应该分成三层：

1. **任务层 direct baseline**
   - 文本输入；
   - 输出状态机/行为模型；
   - 至少显式恢复 `state / transition / guard / effect` 的一部分。
2. **表示层强前置**
   - 需求规整；
   - 约束抽取；
   - 行为综合；
   - 正确性检查；
   - 反馈修复；
   - 可执行化或验证化。
3. **目标语义 exemplar**
   - 它们给出控制系统里真正重要的模式、事件、guard、恢复和时间窗口；
   - 这些文献不是对手，但会直接决定我们论文里的“目标语义槽位”怎么定义。

## 4. 最近 5 年最需要优先盯的文献（2021-2026）

下面这张表不是“全收录表”，而是从论文写作角度重新排过的优先名录。  
每篇都明确说清楚它到底做了什么，以及为什么要重点看。

| 年份 | 文献 | 类型 | 它到底做了什么 | 为什么需要重点看 |
|---|---|---|---|---|
| 2026 | [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](https://arxiv.org/abs/2604.00275) | `🟢 直接 baseline` | 直接从**非结构化自然语言需求**生成 UML 状态机，设计了 `single-prompt`、`structure-driven`、`event-driven` 和 `hybrid` 四种生成框架，并显式评测了 states、transitions、guards、actions 的 F1。 | 这是我目前看到**最近、最直接**命中我们主任务的工作。它的重要性在于：已经不再要求 GWT、use case 或其他先验结构化输入，而是正面回答“自由文本能不能生成状态机”。 |
| 2025 | [Generating SysML Behavior Models via Large Language Models: an Empirical Study](../baselines/llms_emp/DESC.md) | `🟢 直接 baseline` | 从自然语言需求直接生成 `PlantUML` 形式的 `SysML` 行为模型，并用模型检查规则做迭代修复，还系统分析了格式/语法/语义/需求不一致四类错误。 | 它最重要的贡献不是 “也生成了状态机”，而是已经把 `generate -> detect -> repair` 这条链跑通了。 |
| 2025 | [LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation](../baselines/fsm-gen-iec-61499/DESC.md) | `🟢 直接 baseline` | 以工业控制自然语言需求和 I/O 规格为输入，让 LLM 迭代生成和修改 `FSM`，再自动转成 `IEC 61499` 功能块并进入仿真/部署环境。 | 这篇和 `FCSTM` 特别像，因为它不是停在“图”，而是继续走到可执行控制逻辑。 |
| 2025 | [Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering](../baselines/req/DESC.md) | `🟢 直接 baseline` | 以汽车需求为输入，结合 NLP 特征提取、合成数据扩充和领域微调，输出 `Mermaid` 状态机。 | 它说明控制/汽车场景下，状态机生成可以走“领域数据 + 微调”的路线，而不只是通用 prompting。 |
| 2025 | [Exploring How Well Llama3 can Generate State Machines Represented in Umple](../baselines/umple/DESC.md) | `🟢 直接 baseline` | 从自然语言需求直接生成 `Umple` 状态机代码，并比较 zero-shot、one-shot 和 RAG。 | 它的价值在于输出是**状态机 DSL 代码**，这比普通图形输出更接近我们要生成 `FCSTM DSL` 的目标。 |
| 2024 | [Completion of SysML state machines from Given-When-Then requirements](../baselines/completion-of-sysml-state-machines-from-gwt-requirements/DESC.md) | `🟡 强前置` | 从 `部分 SysML 模型 + GWT 需求` 出发，把需求规整成补全规则，再自动补上 `transitions / triggers / guards / effects` 与 traceability。 | 它不是从零生成，但明确命中 `FCSTM core` 中最关键的四元组：`transition / trigger / guard / effect`。 |
| 2025 | [Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/sfw2/6714956) | `🟡 强前置` | 先把自然语言需求规整成更结构化的 use case specification，再借助 `UML activity/state machine` 检查 `process-state consistency`。 | 这篇的核心价值是说明：如果不先规整需求，后面很难稳定恢复状态、事件和 guard。 |
| 2025 | [MCeT: Behavioral Model Correctness Evaluation using Large Language Models](../baselines/mcet/DESC.md) | `🟡 强前置` | 自动比较需求文本和行为模型，输出 issue list，而不是直接生成状态机。 | 它非常适合当 `FCSTM` 生成后的轻量检查器或评审器。 |
| 2026 | [Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering](../baselines/workflow-level-design-principles-trustworthy-genai-automotive/DESC.md) | `🟠 邻近前置` | 不做从零建模，而是把 requirement delta 识别、SysML v2 更新、编译/静态分析和回归测试追踪串成一个可信工作流。 | 它最有价值的是告诉我们：安全关键工程里，`big-bang prompting` 不够，必须有分阶段工作流和工具校验。 |
| 2025 | [Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs](../baselines/spec2control/DESC.md) | `🟠 邻近前置` | 从工业控制 narrative 自动识别控制策略、连接关系和报警映射，输出图形化 PLC/DCS 控制逻辑。 | 它不是状态机生成论文，但输入和控制场景与我们高度一致，说明“控制叙述 -> 可执行控制工件”这条路已经在工业里跑起来了。 |
| 2025 | [Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts](../baselines/pushing-the-generative-envelope-mbse-artifacts/DESC.md) | `🟡 实验设计前置` | 用 local LLM 从简短系统描述生成 `requirements list + state machine diagrams`，系统比较 prompt technique 和 temperature。 | 它更像实验设计参照：告诉我们 prompt 组织方式通常比 temperature 更影响状态机生成质量。 |

### 4.1 这一组文献里，谁最像 `FCSTM` direct baseline

如果进一步从 `FCSTM` 的目标语义看，这组文献里最关键的顺序大致是：

1. `Structure- and Event-Driven Frameworks...`
   - 因为它是**非结构化文本 -> 状态机**；
   - 而且显式把状态机拆成 `states / transitions / guards / actions` 多步恢复。
2. `llms_emp`
   - 因为它已经有 `generate -> check -> repair` 闭环。
3. `fsm-gen-iec-61499`
   - 因为它已经把状态机继续推进到可执行控制逻辑。
4. `umple`
   - 因为它输出 DSL 代码，而不是只给图片。
5. `GWT completion`
   - 因为它命中 `trigger / guard / effect`，虽然不是从零生成。

反过来说，`workflow-level` 和 `Spec2Control` 很重要，但它们不是 direct baseline：

1. `workflow-level` 更像**工业工作流和可信传播**前置。
2. `Spec2Control` 更像**控制逻辑生成近邻**，而不是状态机本体。

## 5. 从论文写作角度重排：真正该重点读的能力链文献

### 5.1 直接生成与补全层

| 文献 | 到底做了什么 | 对 `FCSTM` 的直接价值 |
|---|---|---|
| [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](https://arxiv.org/abs/2604.00275) | 从非结构化需求生成 UML 状态机，比较 single-prompt、structure-driven、event-driven 和 hybrid，显式评测 states/transitions/guards/actions。 | 这是最接近“自由文本到状态机”的 direct baseline 之一，也直接告诉我们哪些槽位最难：guard 和 action。 |
| [Generating SysML Behavior Models via Large Language Models: an Empirical Study](../baselines/llms_emp/DESC.md) | 直接生成 `SysML STM/ACT/SD`，并用检查规则反馈修复。 | 说明状态机生成不该只看 first-pass 结果，而应把 checker feedback 纳入主流程。 |
| [LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation](../baselines/fsm-gen-iec-61499/DESC.md) | 让 LLM 迭代精化工业控制 `FSM`，并进一步生成 `IEC 61499`。 | 很适合作为“为什么我们的目标工件不该停在图，而该是可执行模型”的论据。 |
| [Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering](../baselines/req/DESC.md) | 用汽车需求、领域特征和微调生成状态机。 | 说明 automotive/control domain adaptation 可能显著影响生成质量。 |
| [Exploring How Well Llama3 can Generate State Machines Represented in Umple](../baselines/umple/DESC.md) | 从需求生成 `Umple` 状态机代码，比较 zero-shot、one-shot、RAG。 | 很接近 `FCSTM DSL` 的研究口味，因为输出已经是可机读状态机代码。 |
| [System Architects Are not Alone Anymore: Automatic System Modeling with AI](../baselines/ttool-ai/DESC.md) | 从自然语言规范生成 SysML 块图、内部块图和状态机，并通过反馈循环修正。 | 它说明“知识注入 + 工具链反馈 + 多图协同生成”在 MBSE 里是可行的。 |
| [Completion of SysML state machines from Given-When-Then requirements](../baselines/completion-of-sysml-state-machines-from-gwt-requirements/DESC.md) | 把 `GWT` 需求转成补全规则，为已有状态机补上 `trigger / guard / effect` 和 traceability。 | 很适合作为 `FCSTM skeleton generation + constrained completion` 路线的后半段参照。 |

### 5.2 需求规整、约束桥接与控制语义层

| 文献 | 到底做了什么 | 对 `FCSTM` 的具体价值 |
|---|---|---|
| [Enhancing Requirements via Structured Formalization and Process-State Consistency Validation](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/sfw2/6714956) | 先把自由文本规整成结构化 use case，再用 `activity/state machine` 检查流程和状态的一致性。 | 强烈支持“先规整、再建模”的方法路线。 |
| [Formal Requirements Elicitation with FRET](../baselines/formal-requirements-elicitation-with-fret/DESC.md) | 用 `FRETish` 这类受限自然语言写需求，并自动得到解释、逻辑和分析入口。 | 适合作为 `FCSTM` 前端中间语言的参照。 |
| [Evaluating OpenAI Large Language Models for Generating Logical Abstractions of Technical Requirements Documents](https://ieeexplore.ieee.org/document/10684632/) | 评估 LLM 把技术需求文档转换为逻辑表示的能力。 | 这一步虽然没到状态机，但非常适合支撑 `guard / invariant / property` 抽取。 |
| [Leveraging Natural Language Processing for a Consistency Checking Toolchain of Automotive Requirements](https://ieeexplore.ieee.org/document/10260788/) | 把非正式汽车需求规整成 Structured English，并接到 SMT 一致性分析。 | 对汽车/控制需求预处理特别贴题。 |
| [Enhancing model-based development with formalized requirements: integrating temporal logic and SysML v2 for comprehensive state and transition modeling](../baselines/enhancing-model-based-development-formalized-requirements/DESC.md) | 把形式化为 `LTL` 的需求自动编译成 `SysML v2` 状态机。 | 它告诉我们如何从约束反推 `states/transitions`。 |
| [Automated Generation of Constraints from Use Case Specifications to Support System Testing](https://ieeexplore.ieee.org/document/8367033/) | 从 use case 自动抽取前置/后置约束，补出可检查的条件。 | 和 `FCSTM` 最直接的关系是 guard/precondition/postcondition 恢复。 |
| [Safety SysML: An Executable Safety-Critical Avionics Requirement Modeling Language](https://ieeexplore.ieee.org/document/10062409/) | 扩展 SysML 状态机以表达安全关键航空需求，并配套 refinement 与 verification。 | 它回答的是“控制/安全语义怎么进状态机”，这比普通图生成更重要。 |
| [LLM-based Iterative Refinement of Finite-State Machines with STPA Controller Constraints and Generation of IEC 61499 Code](../baselines/STPA/DESC.md) | 把 `STPA` 约束作为修复信号，驱动 LLM 反复修改 FSM，再生成工业代码。 | 对 `FCSTM` 的意义在于：安全约束可以直接变成状态机修复信号。 |

### 5.3 经典综合、执行化与检查闭环层

| 文献 | 到底做了什么 | 对 `FCSTM` 的具体价值 |
|---|---|---|
| [Executable State Machines Derived from Structured Textual Requirements](../baselines/executable-state-machines-derived-from-structured-textual-requirements/DESC.md) | 把结构化文本需求映射到逻辑，再综合成一致状态机并补到可执行模型。 | 这是“需求 -> 可执行状态机”最完整的经典链路之一。 |
| [Execution of natural language requirements using State Machines synthesised from Behavior Trees](https://linkinghub.elsevier.com/retrieve/pii/S0164121212001690) | 把自然语言需求经由 `Behavior Trees` 转成可执行状态机，并支持执行。 | 这条路线和我们“先规整、再落到行为模型”的方法很接近。 |
| [Synthesizing hierarchical state machines from expressive scenario descriptions](https://dl.acm.org/doi/10.1145/1656250.1656252) | 从 expressive scenario descriptions 自动综合 `hierarchical state machines`。 | 这篇对 `FCSTM` 特别重要，因为它正中“层次状态机综合”这个点。 |
| [Beyond Scenarios: Generating State Models from Use Cases](../baselines/beyond-scenarios-generating-state-models-from-use-cases/DESC.md) | 通过规则把 use case 直接转成 state model。 | 它说明结构化需求入口确实可以稳定地产生状态模型。 |
| [Synthesis Revisited: Generating Statechart Models from Scenario-Based Requirements](../baselines/synthesis-revisited-scenario-based-requirements/DESC.md) | 以 `LSC` 场景规格为输入，综合出 UML 风格 statecharts。 | 很适合作为 `LLM 前端 -> 场景中间层 -> 状态图综合` 路线的后端前身。 |
| [Automatic Debugging Support for UML Designs](../baselines/automatic-debugging-support-for-uml-designs/DESC.md) | 从 annotated sequence diagrams 综合 statecharts，并把冲突回映射到需求端。 | 这和我们未来做反例驱动修复非常接近。 |
| [Modelling Timed Reactive Systems from Natural-Language Requirements](../baselines/modelling-timed-reactive-systems-from-natural-language-requirements/DESC.md) | 从自然语言需求自动生成带时间语义的反应式模型并支持分析。 | 对 `FCSTM` 将来进入时序/周期语义很重要。 |
| [Modelling and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements](../baselines/modelling-and-testing-timed-data-flow-reactive-systems-in-coq/DESC.md) | 把受控自然语言需求翻译成 `Coq` 中的 timed reactive model，并做验证和测试。 | 它把“生成后立即进入验证/测试”这条链走通了。 |
| [Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study](../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/DESC.md) | 用 `RSML-e` 在 Nimbus 中捕获、执行和评估灯光控制需求。 | 这是控制系统“需求 -> 状态化规格 -> 可执行评估”的经典代表。 |
| [Requirements Specification for Process-Control Systems](../baselines/requirements-specification-for-process-control-systems/DESC.md) | 为过程控制系统提出既形式化又可审阅的状态化需求规格写法。 | 直接支撑我们把论文定位成“控制需求到行为模型”。 |
| [MCeT: Behavioral Model Correctness Evaluation using Large Language Models](../baselines/mcet/DESC.md) | 自动比较需求文本和行为模型，输出 issue list。 | 可以直接当作 `FCSTM` 生成后的检查器参考。 |

## 6. 不是 baseline，但必须重点看的 `FCSTM` 目标语义 exemplar

这部分是我认为这一轮最需要补上的内容。  
这些文献不是“别人怎么生成状态机”，而是“控制系统里真正有价值的状态机语义是什么”。  
如果不把这一层写进 related work 或 problem framing，`FCSTM` 的语义设计就会显得像拍脑袋。

| `FCSTM` 语义槽位 | 重点文献 | 它到底做了什么 | 为什么必须重点看 |
|---|---|---|---|
| 层次 supervisor / mission decomposition | [Methodology To Develop A Discrete-Event Supervisory Controller For An Autonomous Helicopter Flight](../sources/methodology-to-develop-a-discrete-event-supervisory-controller-for-an-autonomous-helicopter-flight/STM.md) | 把 Bell 412 自主飞行任务拆成 `Takeoff / On Route / Landing` 三个监督子组件，并显式处理“没有合适落点时是否交还飞行员”的决策。 | 它直接说明控制系统状态机不是扁平图，而是有 supervisor 层、任务阶段层和安全接管决策层。 |
| 层次与并行子层 | [A Parallel Hierarchical Finite State Machine Approach to UAV Control for Search and Rescue Tasks](../sources/a-parallel-hierarchical-finite-state-machine-approach-to-uav-control-for-search-and-rescue-tasks/STM.md) | 给出搜救 UAV 的 `Start -> Move to Search -> Look -> Track -> Return -> Land` 高层流，并明确安全飞行子层与跟踪子层并行运行。 | 它为我们定义“模式层 + 并行安全子层”提供了非常直观的 exemplar。 |
| 细粒度模式子状态与模式序列约束 | [Mode confusion analysis of a flight guidance system using formal methods](../sources/mode-confusion-analysis-of-a-flight-guidance-system-using-formal-methods/STM.md) | 直接描述飞行引导系统的 `selected / armed / active / capture / track` 子状态组织，以及 lateral/vertical 模式间的序列约束。 | 这类文献说明控制系统模式不是简单枚举名词，而是有层次、子状态和切换约束。 |
| guard / interlock / route lifecycle | [Some Experiences on Formal Specification of Railway Interlocking Systems using Statecharts](../sources/some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts/STM.md) | 把联锁中的 `request -> check -> lock -> green` 顺序和占用/锁闭条件写得非常明确。 | 这是 guard-heavy 控制逻辑的典型 exemplar，特别适合支撑 `guard` 在 `FCSTM` 中的一等地位。 |
| 降级、故障传播与安全需求绑定 | [Safety analysis integration in a SysML-based complex system design process](../sources/sysml-safety-analysis-integration/STM.md) | 用四模态自动机描述飞机轮刹系统从 `Normal -> Alternate -> Emergency -> Fail` 的退化逻辑，并把安全需求绑定到状态机与形式化验证。 | 它清楚说明：控制状态机不只是 nominal path，更关键的是 degradation / recovery 语义。 |
| 模式切换 + 相位控制 + effect | [Developing a Prototype of a Mechanical Ventilator Controller from Requirements to Code with ASMETA](../sources/developing-a-prototype-of-a-mechanical-ventilator-controller-from-requirements-to-code-with-asmeta/STM.md) | 明确给出呼吸机的 `startup / self-test / ventilation-off / PCV / PSV` 主模式，以及吸气/呼气相位切换和阀门开闭动作。 | 这篇非常适合说明 `state / guard / effect / phase` 在医疗控制里如何同时出现，并最终进入 code generation。 |
| 时间窗口与并发状态机约束 | [Benchmarks for Temporal Logic Requirements for Automotive Systems](../sources/automotive-temporal-logic-benchmarks/STM.md) | 给出自动变速器的并发 Stateflow 逻辑，并明确 `2.5s` 内禁止快速回跳和立即再换挡等时序约束。 | 它说明控制状态机里的 timing guard / dwell time 不是附属信息，而是主语义的一部分。 |

### 6.1 这一组 exemplar 对 `FCSTM` 任务定义的直接影响

结合上面这些文献，我现在认为 `project_1` 里真正应该被明确恢复的，不只是 “状态和边”，而是下面这些**控制语义槽位**：

1. **层次模式结构**
   - supervisor mode；
   - operation mode；
   - phase / substate。
2. **控制 guard**
   - interlock；
   - permission；
   - inhibit；
   - degradation condition；
   - recovery condition。
3. **effect / lifecycle action**
   - 阀门开闭；
   - actuator enable/disable；
   - reset/cleanup；
   - acknowledgement。
4. **时间相关约束**
   - dwell time；
   - timeout；
   - minimum/maximum phase duration；
   - anti-chattering window。
5. **异常与降级**
   - failover；
   - manual takeover；
   - safe state；
   - fallback to nominal path。

换句话说，`project_1` 的论文如果要站稳，不能只说“我们从文本生成层次状态机”。  
更准确的说法应该是：

> 我们从控制系统文本中恢复一组具备层次模式、guard/effect、异常恢复和时间约束的 `FCSTM core semantics`，并使其进入可执行、可检查、可修复的闭环。

## 7. 下一步真正要深读和补强的文献清单

### 7.1 应优先补进 `baselines/` 或至少补成正式单篇分析的

这里说的“补进”，不是都要机械进 `baselines/`；  
而是优先把这些条目整理成正式可引用、可对照的单篇材料。

1. [Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models](https://arxiv.org/abs/2604.00275)
   - 原因：当前最直接的 `unstructured NL -> state machine` 新工作。
2. [Execution of natural language requirements using State Machines synthesised from Behavior Trees](https://linkinghub.elsevier.com/retrieve/pii/S0164121212001690)
   - 原因：把自然语言需求经规整中间层落到可执行状态机，和我们的方法路线很接近。
3. [Synthesizing hierarchical state machines from expressive scenario descriptions](https://dl.acm.org/doi/10.1145/1656250.1656252)
   - 原因：层次状态机综合这条线对 `FCSTM` 太关键，不能只在 discussion 里一带而过。
4. [Safety SysML: An Executable Safety-Critical Avionics Requirement Modeling Language](https://ieeexplore.ieee.org/document/10062409/)
   - 原因：安全关键控制语义进入状态机这件事，它讲得比很多 LLM 论文更对题。
5. [Inferring test models from user bug reports using multi-objective search](https://link.springer.com/10.1007/s10664-023-10333-8)
   - 原因：虽然入口是 bug report，但它证明自然语言异常描述也能恢复 `FSM`，对后续 repair loop 很有价值。

### 7.2 应保留在 discussion 主线，但不一定收进 `baselines/` 的

1. [Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering](../baselines/workflow-level-design-principles-trustworthy-genai-automotive/DESC.md)
   - 它更适合作为工作流与可信工程前置，而不是 direct baseline。
2. [Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs](../baselines/spec2control/DESC.md)
   - 它更像控制逻辑近邻工作，不宜硬说成状态机 baseline。
3. [sources/](../sources/README.md) 中这一组 exemplar 文献
   - 它们更适合当 target semantics 论据，而不是 baseline 对手。

## 8. 当前结论

如果现在只用一句话概括这轮重排结果，那就是：

> 结合 `pyfcstm/FCSTM` 之后，`project_1` 真正该重点读的文献明显比上一版 discussion 里列出的更多，而且必须分成三层来看：一层是 `unstructured text -> state machine` 的 direct baseline，一层是 `requirements normalization / constraint bridge / checking / repair / executable semantics` 的强前置工作，另一层则是定义控制系统目标语义的 exemplar 文献。

进一步说，这轮调研最重要的新增判断有三条：

1. `2026` 的 `Structure- and Event-Driven Frameworks...` 必须进入主视野。
   - 它是目前最值得直接对照的 recent baseline 之一。
2. `FCSTM` 研究不能只盯“怎么生成”，还必须单独写清楚“要生成什么样的控制状态机”。
   - 这正是第 `6` 节那些 exemplar 文献的作用。
3. 现有工作没有一篇能同时覆盖：
   - 非结构化控制需求输入；
   - 层次模式与 supervisor 组织；
   - guard / effect / 异常恢复；
   - 可执行 cycle 语义；
   - 生成后检查与反馈修复；
   - 后续验证或代码生成闭环。

这也正是 `project_1` 现在最有机会形成论文主张的地方。
