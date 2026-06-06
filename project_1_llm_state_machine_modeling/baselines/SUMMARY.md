# Project 1 Baselines Summary

本文件是 `project_1_llm_state_machine_modeling/baselines/` 的总账，用于记录当前已经正式入账的 baseline 论文、统一比较口径、数据集与 benchmark 盘点、待补充候选与更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 再使用本文件查看统计、论文清单、数据集盘点和待补充候选。
4. 若需要重写某篇单论文分析，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。

## 当前收录统计

- 已收录 baseline 论文：**62** 篇
- 本轮新增论文：**1** 篇
- 已完成 `DESC.md`：**62** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮规范化工作：在论文总表新增 `需求词工程 / 运行仿真 / 形式化验证` 三列，并基于全文阅读逐篇补齐其“程度｜技术｜角色”口径；同时保留既有 baseline 收录统计不变

## BASELINE评估口径

| Emoji | 含义 |
|---|---|
| 🟢 | 直接构成 baseline：输入是自然语言系统设计/描述/需求，输出必须是状态机/Statechart/SysML 状态机或高度等价的状态机族模型，与本研究直接可比 |
| 🟡 | 相关但非直接 baseline：仍围绕状态机生成/精化/扩展/修复，但输入不是纯自然语言，或任务更偏已有状态机的 refinement / test generation |
| 🟠 | 弱相关/可比性有限：输出不是状态机族模型，或任务只是有限状态推理、多模态识别、泛 UML/SysML/goal/domain 建模，不构成公平直接对比 |
| ⚪ | 背景资料：只适合当背景文献或补充相关工作，不建议作为 baseline 对照 |

## 检索关键词簇

### 当前推荐关键词簇

- `LLM/GPT/Claude/Gemini` + `state machine/statechart/state diagram/FSM`
- `requirements` + `statechart/state machine` + `automotive/industrial/control`
- `iterative refinement/model repair/model completion/test generation` + `state machine/FSM`
- `diagram recognition/vision-language/multimodal` + `state diagram/FSM`
- `state machine` + `formal verification/model checking/constraint repair`
- `Given-When-Then` + `SysML state machine`
- `process-control/control system` + `requirements specification` + `state-based/RSML/statechart`
- `temporal logic/LTL` + `SysML v2 state machine`
- `MBSE/SysML v2` + `state machine diagram` + `prompt/temperature`
- `behavioral model correctness / sequence diagram` + `benchmark / judge / evaluation`
- `requirements` + `UML` + `multi-agent / judge / benchmark`
- `scenario / use case / MSC / LSC` + `statechart / state model / LTS / FSM`
- `controlled natural language` + `reactive system / timed / data-flow / Coq`

### 已观察到的高命中特征

- 题名同时出现 `LLM` 与 `state machine/statechart/FSM/SysML behavior`
- 明确写出输入输出链路，如 `requirements -> statechart`、`diagram -> code/test`
- `partial model -> completion/repair` 且对象明确是状态机时，命中率更稳定
- 出现 `iterative`、`refinement`、`feedback`、`few-shot`、`RAG` 等方法词
- 安全关键或工业领域关键词常能带来更贴近 `project_1` 的论文
- `process-control`、`reactive systems`、`RSML`、`state-based specification` 这条经典控制软件线索很容易找到高任务对齐前身工作
- `Given-When-Then`、`LTL -> state machine`、`sequence diagrams -> statecharts` 这类显式桥接链路词，命中率明显高于泛 MBSE 关键词
- arXiv 预印本里，直接出现 `state machine diagrams`、`SysML behavior`、`Mermaid/PlantUML` 的题名或摘要，命中率显著高于泛泛的 `UML modeling`
- `benchmark`、`judge`、`correctness evaluation` 常能命中公开工件更好的论文，虽然很多只能评为 `🟠`
- `scenario / use case / statechart`、`LSC / MSC / UML state machine` 这条经典软件工程线索，更容易命中真正任务对齐的前身工作
- `controlled natural language`、`reactive systems`、`timed`、`Coq` 常能命中带验证闭环的经典自动化方法

### 已观察到的低命中特征

- `FSM` 仅用于提示范式、规划器、对话流或智能体编排
- 纯机器人执行流程、纯协议推理、纯智能合约生成但无建模工件
- 输出是顺序图、类图、goal model、一般 domain model 的论文默认不是本 collection 的主线
- 纯教学经验、课堂问卷或学习体验类 UML 论文通常弱于“真正生成模型”的论文
- 纯综述、纯经验报告，缺少明确方法与实验对比
- 只做 requirements formalization、DSL 翻译或 temporal logic 输出的论文，若没有状态机落点，通常只能保留为 `🟠`
- 控制逻辑图、功能块图、PLC/DCS 工程图等虽然很贴近工业控制，但若没有显式状态机语义，也不能直接算 `🟢`
- `semantic alignment`、`architecture candidate generation`、`accessible interface` 这类 MBSE/SE 预印本容易“看起来很像”，但往往不直接产出状态机
- 只做 sequence diagram correctness / UML classroom study 的论文通常只能提供边界证据，不能抬成直接 baseline

### 检索倾向调整

- 优先补“直接生成状态机模型”和“带反馈闭环的状态机精化/修复”两类工作
- 当 LLM 直接命中不足时，优先补“任务定义高度一致”的经典非 LLM 前身，而不是继续扩张到泛建模论文
- 泛 UML/SysML 论文仅在其方法明确输出状态机时保留
- 多模态图样识别和自动 benchmark 构建可保留，但需在 `DESC.md` 中明确说明其“邻近 baseline”性质
- 非状态机输出论文原则上不再继续扩张收录，只在少量必要场合作为弱相关参照保留
- 对 arXiv/作者版预印本，应优先追 `state machine diagram / SysML behavior / behavioral model`，其次才是 `class/use case/sequence`
- 若预印本主要贡献是 benchmark、judge 或 correctness evaluation，应明确把它们归为“生成后基础设施”，而不是误标成直接状态机 baseline


## 论文清单

### 三个新增列的填写口径

- `需求词工程`：按“程度｜技术｜角色”填写。`无` 表示几乎未把 prompt/pattern 设计当成方法变量；`低/中/高` 分别对应从基础指令到 few-shot / CoT / RAG / 多阶段 / 多智能体等更强介入。
- `运行仿真`：按“程度｜技术｜角色”填写。区分 `无`、`评测支撑`、`执行化/原型运行`、`simulation-in-the-loop`、`co-simulation/HIL` 等。
- `形式化验证`：按“程度｜技术｜角色”填写，并**严格区分**真正的 formal verification（如 model checking / theorem proving / SAT 等）与仅有语法检查、静态分析、规则检查或人工评审的情况；后者不得写成“高”。
- 对 `llms_emp`、`ttool-ai` 这类带“检查/修复反馈”环的论文，若正文证据主要是语法、约束、JSON/schema、一致性或 rule-based checking，而非真正的 model checking / theorem proving，则统一按“弱形式化或半形式化约束”回填，不上调为“高形式化验证”。

| # | 评估 | 类别 | 标题 | 年份 | 输入 | 输出 | 输出模型类型 | 使用的LLM | 主要方法 | 需求词工程 | 运行仿真 | 形式化验证 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| 1 | 🟢 | 直接生成 | Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models | 2026 | 非结构化自然语言系统描述 | UML 状态机 | UML state machine | GPT-4o、Claude 3.5 Sonnet | 比较 `Single-Prompt`、`Structure-Driven SMF`、`Event-Driven SMF`、`Hybrid` 四种框架，并按 states/transitions/guards/actions 等槽位评测 F1 | 高｜zero/one/few-shot 思路、分步提示、Hybrid 追加基线解｜主驱动生成质量，决定分解粒度与召回 | 无｜无 simulator / execution loop，仅离线评测｜不承担闭环反馈 | 无｜仅规则后处理与参考解比对，无 formal checking｜不进入验证闭环 | [paper](./structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) · [review](../state_machine_review_corpus/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/review_extraction.md) |
| 2 | 🟢 | 直接生成 | Generating SysML Behavior Models via Large Language Models: an Empirical Study | 2025 | 自然语言需求描述 | PlantUML 格式行为模型 | SysML STM / ACT / SD | GPT-4、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 | 两阶段框架：提示生成 + 模型检查反馈修复 | 高｜角色/指令/需求/示例/RAG/错误信息五段 prompt｜主生成接口，也是二阶段修复入口 | 低｜论文将 simulation traces 视为未来更优反馈，正文未真正接入｜当前无 run-in-the-loop | 中-｜PlantUML / SysML grammar / semantics / consistency 规则检查｜充当错误检测与再生成反馈，但多数仍是 rule-based checking 而非完整 formal verification | [paper](./llms_emp/DESC.md) · [review](../state_machine_review_corpus/llms_emp/review_extraction.md) |
| 3 | 🟢 | 直接生成 | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | 自然语言控制需求 + I/O 接口规范 | 可视化 FSM + IEC 61499 功能块代码 | FSM | 未明确指定 | 自然语言到 FSM 的迭代精化，并接入仿真和代码生成 | 中｜初始需求提示 + 人类评论式增量修订｜用于把需求逐轮压到可执行控制逻辑 | 高｜EAE/softPLC 闭环仿真、virtual commissioning、代码部署测试｜是主反馈来源，用来验证行为并驱动 refinement | 低-中｜文中主要是人工/可视化检查与后续计划接 formal verification framework｜当前 formal verification 还是预留接口，不是主实验核心 | [paper](./fsm-gen-iec-61499/DESC.md) |
| 4 | 🟢 | 直接生成 | Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering | 2025 | 自然语言产品功能需求 | Mermaid.js 状态机 | Statechart | GPT-3.5、GPT-4、GPT-4o（微调） | NLP 特征提取 + 合成数据扩充 + 领域微调生成状态机 | 中｜prompt-completion 对、数据增广、微调输入设计｜主要承担监督学习任务定义，不是复杂 agent loop | 低｜输出状态图在 Mermaid editor 中渲染，结合专家做功能正确性评审｜更偏可视化评测支撑 | 无｜无 model checker / theorem prover；依赖专家评分与数据处理规则｜不在 formal V&V 闭环中 | [paper](./req/DESC.md) |
| 5 | 🟢 | 直接生成 | Exploring How Well Llama3 can Generate State Machines Represented in Umple | 2025 | 自然语言需求描述 | Umple 状态机代码 | Umple 状态机 | Llama 3 (8B) | 比较 Zero-shot、One-shot 与 RAG 三种提示策略 | 高｜系统消息格式、zero/one-shot、基于相似度选例的 RAG｜是论文核心自变量，用来比较不同提示路线 | 中｜借助 Umple 可执行性/样例验证 pass@k｜主要作为代码/模型可运行性检验 | 低｜依赖 Umple 编译/语义可执行性而非独立 formal proof｜是轻量可执行验证，不是性质证明 | [paper](./umple/DESC.md) |
| 6 | 🟢 | 直接生成 | System Architects Are not Alone Anymore: Automatic System Modeling with AI | 2024 | 自然语言系统规范 | SysML 块图、内部块图和状态机图 | 含状态机的 SysML 联合模型 | GPT-4 | 知识注入 + 自动反馈循环 + TTool 工具链集成 | 高｜知识注入、约束化 JSON 输出、自动反馈问答｜是把系统规格压成可绘图 SysML 的主控制手段 | 中｜评测时用 TTool simulator 观察状态机行为是否符合规范｜主要作为评分支撑，不是连续仿真闭环 | 中-｜TTool 本身支持 model-checkers/simulators，但本文反馈环主要检查 JSON/语法/约束｜formal capability 是工具背景与后续入口，不是正文主验证机制 | [paper](./ttool-ai/DESC.md) · [review](../state_machine_review_corpus/ttool-ai/review_extraction.md) |
| 7 | 🟠 | FSM代码生成 | Enhancing Finite State Machine Design Automation with Large Language Models and Prompt Engineering Techniques | 2024 | HDLBits FSM 设计问题描述 | SystemVerilog FSM 代码 | FSM 代码工件 | Claude 3 Opus、GPT-4、GPT-4o | Markdown 提示模板 + TOP Patch + CoT 多轮对话 | 高｜系统化 markdown prompt + TOP Patch 待办清单｜主提升手段，针对同步复位/one-hot 等痛点补提示 | 低｜依赖 HDLBits/代码是否通过测试来判成功｜属于代码评测而非过程仿真 | 无｜无 formal verification；以语法正确和题目通过率为主｜不承担 formal assurance | [paper](./enhance/DESC.md) |
| 8 | 🟠 | FSM代码生成 | LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation | 2026 | FSM 配置参数 + 自然语言规范 | Verilog RTL 代码 + 测试平台 | RTL / 测试工件 | GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro 等 | 自动构建 FSM-to-RTL benchmark 并系统评估有限状态推理 | 中｜规格到 YAML / RTL 的任务提示、test-time scaling｜用于 benchmark 构造与推理评测，不是需求工程主贡献 | 高｜reference testbench、cycle-level waveform matching、SystemC-Verilog co-sim｜是 correctness 判定主链路 | 高｜SAT-solver equivalence checking（Yosys）验证规格-RTL 一致性｜构成 benchmark 过滤与正确性保证核心 | [paper](./LLM-FSM/DESC.md) |
| 9 | 🟡 | 精化/修复 | LLM-based iterative refinement of finite-state machines with STPA controller constraints and generation of IEC 61499 code | 2025 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | FSM | OpenAI GPT（通过 fbAssistant） | 用 STPA 约束驱动递归迭代精化 | 中｜约束注入式 prompt + 评审评论迭代｜用于把安全约束转成模型修订动作 | 高｜虚拟环境测试 / commissioning 验证修改后的控制逻辑｜是 refinement 是否可接受的主反馈 | 中｜STPA 本身是安全分析而非 model checking；约束起到半形式化过滤作用｜偏安全约束驱动修复，不是自动性质证明 | [paper](./STPA/DESC.md) |
| 10 | 🟡 | 精化/扩展 | State Diagram Extension and Test Case Generation Based on Large Language Models for Improving Test Engineers’ Efficiency in Safety Testing | 2024 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | State Diagram | Qwen2-72B-Instruct（微调） | 安全准则提取 + 状态图扩展 + 测试路径/数据生成 | 高｜无上下文/有上下文两类 prompt、步骤化系统提示｜核心用于把 safety criteria 注入扩图与测例生成 | 低｜DFS 路径生成 + GA test data，不是系统仿真｜更偏测试用例构造 | 低-中｜含数据帧验证/故障处理准则等安全规则，但不是独立 formal method engine｜扮演安全规则过滤器与测试设计依据 | [paper](./safety/DESC.md) |
| 11 | 🟠 | 泛建模 | Multi-step Iterative Automated Domain Modeling with Large Language Models | 2024 | 自然语言问题描述 / 领域描述文本 | 领域模型 | UML 类图 / 领域模型 | GPT-4 | 多步任务分解 + few-shot + 迭代优化 | 高｜多步任务分解、few-shot、迭代重写｜是主要贡献，靠提示分工提升类图质量 | 无｜无执行模型或 simulator｜不在运行闭环中 | 无｜无 formal verification，仅人工/指标评估｜不承担 formal role | [paper](./MIG/DESC.md) |
| 12 | 🟡 | 多模态邻近 | Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition | 2025 | 状态图图像（来自工业规范 PDF） | 状态机表示 + C++ 代码 + 测试 | 图像状态图 / 可机读状态机表示 | gpt-4o、claude-3-sonnet、Llama-3.2-11b | 图像裁剪 + LLM 识别 + 模板化代码/测试生成 | 中｜识别与生成 prompt、模板化后处理｜用于从图到机读模型/代码 | 中｜生成代码与测试工件，用测试验证识别结果可用性｜属于测试执行支撑 | 低｜主要是识别正确性与测试，不是 formal verification｜formal role 很弱 | [paper](./I4.0/DESC.md) |
| 13 | 🟠 | 泛建模经验 | On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML | 2023 | 自然语言建模任务描述 + 修正提示 | UML 类图 + OCL 约束 | UML 类图 / OCL | ChatGPT | 经验性对话实验，系统评估 UML/OCL 建模能力与缺陷模式 | 中｜人工多轮修正提示｜作为经验研究变量，而非稳定流水线 | 无｜无运行/仿真｜无闭环 | 低｜涉及 OCL 形式约束，但未形成自动 formal verification 链｜更多是建模能力观察 | [paper](./chatgpt-uml-assessment/DESC.md) |
| 14 | 🟠 | 邻近行为建模 | Model Generation with LLMs: From Requirements to UML Sequence Diagrams | 2024 | 自然语言需求文档 | UML sequence diagram | UML 顺序图 | ChatGPT | 从真实需求文档直接生成顺序图，并做问题主题分析 | 低-中｜直接 prompt 生成为主｜主要承担 baseline 生成 | 无｜无仿真或执行｜无动态闭环 | 无｜无 formal verification；靠人工质量分析｜不承担 formal role | [paper](./requirements-to-uml-sequence-diagrams/DESC.md) |
| 15 | 🟠 | 多模态邻近 | From Image to UML: First Results of Image-Based UML Diagram Generation Using LLMs | 2024 | UML 类图图像 / 手绘图 | PlantUML 类图代码 | UML 类图 | GPT-4V、Gemini Pro、Gemini Ultra、CogVLM | 多模态图像识别到 PlantUML 的重复实验比较 | 中｜多 prompt 比较｜用于提升 OCR/diagram parsing 质量 | 无｜无仿真｜无动态角色 | 无｜无 formal verification；主要看转写质量｜不承担 formal role | [paper](./from-image-to-uml/DESC.md) |
| 16 | 🟠 | 泛建模补全 | Towards using Few-Shot Prompt Learning for Automating Model Completion | 2023 | 部分 UML 类图 / 活动图 | 类、属性、关联名与活动流补全建议 | UML 类图 / 活动图 | GPT-3 (`text-davinci-002`) | 将模型补全转写为 few-shot prompt learning 任务 | 高｜few-shot 是方法核心｜把补全任务转换为 prompt 学习问题 | 无｜无仿真｜无运行角色 | 无｜无 formal verification｜仅补全建议生成 | [paper](./few-shot-model-completion/DESC.md) |
| 17 | 🟠 | 泛建模 | On the Use of GPT-4 for Creating Goal Models: An Exploratory Study | 2023 | 领域描述 + TGRL 语法提示 | GRL/TGRL 目标模型 | Goal model | GPT-4 | 多 prompt、多次运行与结果聚合的目标建模探索 | 高｜多 prompt 设计与重复采样｜是主实验变量 | 无｜无运行/仿真｜无动态角色 | 无｜无 formal verification｜仅做目标模型生成评估 | [paper](./gpt4-goal-models/DESC.md) |
| 18 | 🟡 | 状态机补全 | Completion of SysML state machines from Given–When–Then requirements | 2024 | 部分 SysML 模型 + GWT 需求 | 补全后的 SysML 状态机 | SysML state machine | 未使用 | GWT 需求规则化后补全迁移与 traceability | 中｜GWT clause templates / MetaReqX / grammar templates｜需求模式本身就是主要结构化媒介 | 低｜面向可执行测试与 traceability，但正文重点不是仿真｜更多是补全与一致性支持 | 中｜以语法模板、模式检测、文本/模型一致性检查为主；文中提及可接 model checking｜更像半形式化需求-模型桥梁 | [paper](./completion-of-sysml-state-machines-from-gwt-requirements/DESC.md) |
| 19 | 🟡 | 形式化需求到状态机 | Enhancing model-based development with formalized requirements: integrating temporal logic and SysML v2 for comprehensive state and transition modeling | 2025 | LTL 形式化需求 | SysML v2 状态机 | SysML v2 state machine | 未使用 | LTL 生成允许状态/迁移并编译到 SysML v2 | 中｜前置要求是把 NL 手工 formalize 为 LTL｜需求结构化非常强，但不是 LLM prompt 路线 | 无｜无仿真闭环｜主要是建模生成 | 高｜LTL 是主输入，transition permissibility 由逻辑规则判定｜承担核心 formal semantics / transition legality 约束 | [paper](./enhancing-model-based-development-formalized-requirements/DESC.md) |
| 20 | 🟠 | 需求状态抽取 | Extraction of System States from Natural Language Requirements | 2019 | 自然语言需求文本 | 状态实体/状态短语 | 状态标签列表 | BiLSTM-CNN | 需求文本 NER 抽取系统状态 | 低｜无 prompt 工程，主要是监督抽取模型｜仅承担前置状态抽取 | 无｜无仿真｜无运行角色 | 无｜无 formal verification｜不进入 formal 链路 | [paper](./extraction-of-system-states-from-natural-language-requirements/DESC.md) |
| 21 | 🟢 | 经典直接建模 | Executable State Machines Derived from Structured Textual Requirements - Connecting Requirements and Formal System Design | 2019 | 结构化文本需求 | 可执行有限状态机模型 | Executable FSM | 未使用 | 结构化需求 -> 时序逻辑 -> 状态机 -> 可执行模型 | 中｜依赖 SPS/EARS 等结构化需求模板，而非 LLM prompt｜需求规约是形式化前提 | 高｜加入 execution layer、GUI 输入、eTrice 导出与动态模拟｜主用于验证派生模型的动态行为与 traceability | 高｜SPS→LTL→FSM 的数学变换、逐步可证明正确｜承担核心 formal transformation chain | [paper](./executable-state-machines-derived-from-structured-textual-requirements/DESC.md) |
| 22 | 🟠 | 邻近UML设计生成 | Automatic Synthesis of UML Designs from Requirements in an Iterative Process | 2002 | 用例 / 场景 / Sequence Diagrams | UML 设计工件（含 statecharts） | UML statecharts + class diagrams | 未使用 | 场景驱动综合 UML 设计并在迭代中保持一致性 | 无｜非 LLM prompt 工程｜迭代综合靠规则/算法 | 低｜强调迭代调试而非仿真｜运行角色弱 | 低-中｜重在一致性维护与调试支持，不是现代 formal verification 主线｜更像设计一致性分析 | [paper](./automatic-synthesis-of-uml-designs-from-requirements/DESC.md) |
| 23 | 🟠 | 需求形式化 | Technical Report on Neural Language Models and Few-Shot Learning for Systematic Requirements Processing in MDSE | 2022 | 非正式汽车需求 | Requirement DSL | Requirement DSL | 预训练语言模型（few-shot） | few-shot requirements-to-DSL 翻译 | 高｜few-shot requirements-to-DSL｜主作用是把非正式需求压成更规整 DSL | 无｜无仿真｜无动态角色 | 低｜形式化作用体现在 DSL 前置，不是验证执行｜是 formalization 前阶段 | [paper](./tech-report-neural-language-models-few-shot-mdse/DESC.md) |
| 24 | 🟠 | LLM控制逻辑邻近 | Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs - A Multi-Plant Evaluation | 2025 | 自然语言 control narratives | 图形化 PLC/DCS 控制逻辑 | Graphical control logic | GPT-5 等 | 从 control narrative 识别策略/连接/报警并生成控制逻辑图 | 高｜规划/分块/多 prompt 工作流、agent supervision、可接 RAG｜是控制叙事到控制逻辑的主生产线 | 低-中｜工业实践需要 simulation test / FAT / SAT，但本文原型尚缺 FBD verification｜仿真是明确后续环节而非当前核心 | 低｜提到行业需要 layered verification，正文尚未完成 simulation-based / formal verification｜当前更像生成前端 | [paper](./spec2control/DESC.md) |
| 25 | 🟡 | 状态机执行化 | Specification-based Prototyping for Embedded Systems | 1999 | 形式化需求规格 | 可执行层次状态机原型 | Hierarchical state machine prototype | 未使用 | 把规格当作原型执行并沿层次状态机做 refinement | 无｜非 prompt 路线｜靠规格语言与 refinement | 高｜specification-based prototyping、可执行原型｜运行原型是方法核心 | 中-高｜形式化规格 + 分析/一致性/可执行 refinement｜formal 和 prototyping 并重 | [paper](./specification-based-prototyping-for-embedded-systems/DESC.md) |
| 26 | 🟠 | 工具环境 | NIMBUS: A Tool for Specification Centered Development | 2000 | RSML-e 规格 | 分析/执行/代码测试工件 | RSML-e toolchain | 未使用 | 围绕 RSML-e 提供分析、仿真、代码生成与测试 | 无｜非 prompt 路线｜工具导向 | 高｜执行、仿真、测试、代码生成｜是工具核心能力 | 高｜RSML-e 形式语义、分析与验证工具栈｜是 formal method 基础设施 | [paper](./nimbus-tool-for-specification-centered-development/DESC.md) |
| 27 | 🟢 | 经典直接建模 | Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study | 2000 | 灯光控制系统需求 | RSML-e 状态化需求模型 | State-based requirements model | 未使用 | 用 RSML-e + Nimbus 捕获并执行灯光控制需求 | 无｜非 LLM；需求通过 RSML-e formal capture｜需求结构化依赖规格语言 | 高｜执行、环境仿真、日志回放、闭环与 HIL 路线｜本文主验证手段就是 execution/simulation | 高-｜RSML-e 具完整形式语义，formal analysis/verification 是工具栈一环；但本文 case study 重点在仿真验证｜formal methods 是底座，simulation 是正文主角 | [paper](./requirements-capture-and-evaluation-in-nimbus-light-control/DESC.md) |
| 28 | 🟢 | 经典直接建模 | Requirements Specification for Process-Control Systems | 1994 | 过程控制系统需求 | 形式化状态化需求规格 | State-based formal requirements spec | 未使用 | 面向过程控制的规格语言建模并以 TCAS II 演示 | 无｜非 prompt｜依赖规格语言 | 低｜更偏规格建模与案例说明，非仿真论文 | 高｜核心是 formal state-based requirements specification｜为后续分析/验证提供形式语义基础 | [paper](./requirements-specification-for-process-control-systems/DESC.md) |
| 29 | 🟠 | 需求分析 | Software Requirements Analysis for Real-Time Process-Control Systems | 1991 | 状态机式需求规格 | 语义分析准则 | Semantic analysis criteria | 未使用 | 基于抽象状态机模型定义需求分析准则 | 无｜非 prompt｜分析方法文 | 无｜无仿真闭环 | 中｜以语义分析/一致性为主，不是执行式 formal verification｜偏理论分析支撑 | [paper](./software-requirements-analysis-for-real-time-process-control/DESC.md) |
| 30 | 🟡 | 状态机补全/调试 | Automatic Debugging Support for UML Designs | 2000 | Annotated sequence diagrams | Structured statecharts + 冲突解释 | Structured statecharts | 未使用 | 序列图综合 statecharts 并做 backward debugging | 无｜非 prompt｜算法驱动 | 低｜偏调试解释，不是仿真 | 中｜debugging/support consistency 的形式化味道较强，但不是性质证明核心 | [paper](./automatic-debugging-support-for-uml-designs/DESC.md) |
| 31 | 🟡 | 需求-状态机集成 | Integrating Inter-Object Scenarios with Intra-object Statecharts for Developing Reactive Systems | 2020 | LSC 场景规格 | LSC + Statecharts 联合模型 | Integrated scenario-statechart model | 未使用 | 将 scenario-based programming 与 Statecharts 联合执行 | 无｜非 prompt｜场景规格驱动 | 中｜联合执行/运行语义是重要角色 | 中｜LSC/Statecharts 有强形式语义背景，但本文更偏集成与执行 | [paper](./integrating-inter-object-scenarios-with-intra-object-statecharts/DESC.md) |
| 32 | 🟠 | 需求形式化 | Formal Requirements Elicitation with FRET | 2020 | FRETish 需求 | FRETish + 时序逻辑 | Restricted NL / temporal logic | 未使用 | 受限自然语言到时序逻辑、解释与仿真分析入口 | 中｜模板化 fretish / template keys｜需求书写范式本身就是“词工程” | 中｜可交互 simulator 浏览公式语义与场景｜支撑需求理解与调试 | 高｜formalizer + verifier + LTL / CoCoSpec / model checker 接口｜承担需求 formalization 与分析桥梁角色 | [paper](./formal-requirements-elicitation-with-fret/DESC.md) |
| 33 | 🟡 | 增量建模/验证 | Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering | 2026 | 需求变更片段 + 既有 SysML v2 工件 | 更新后的 SysML v2 工件 + 回归测试追踪 | SysML v2 architecture | Qwen3、Nemotron3、GPT-OSS | requirement delta 分段识别 + 工件更新 + 编译/静态分析 | 高｜反单体 prompting、模块化 workflow、多模型 union、检查点回滚｜是论文核心主张 | 低｜偏编译/静态分析/回归测试追踪，不是运行仿真 | 中-高｜checker-based workflow、compile/static analysis、verification artifact regeneration｜formal verification 更偏兼容性与工件追踪，不是完整性质证明 | [paper](./workflow-level-design-principles-trustworthy-genai-automotive/DESC.md) |
| 34 | 🟠 | Benchmark | A System Model Generation Benchmark from Natural Language Requirements | 2025 | 自然语言需求描述 | 参考系统模型 + 评测框架 | System-model benchmark | 多种开源 LLM（评测对象） | 构建 151 场景 SysMBench，并用 SysMEval-F1 等指标评测 | 高｜zero-shot / few-shot / CoT / grammar prompting 全部纳入评测自变量｜研究重点是 prompting 对评测的影响 | 无｜无仿真闭环｜benchmark only | 低-中｜强调 traceability / grammar / compile correctness，但不做系统级 formal verification｜主要是评测规范化 | [paper](./sysmbench-system-model-generation-benchmark/DESC.md) |
| 35 | 🟠 | SysML建模 | Text to model via SysML: Automated generation of dynamical system computational models from unstructured natural language text via enhanced System Modeling Language diagrams | 2025 | 工程文本语料 + 特定系统描述 | SysML 图 + 动态系统计算模型 | SysML BDD / computational model | LLM + NLP 混合 | 五步 text-to-model pipeline，经 SysML 中转到代码/模型 | 中｜one-shot 属性抽取 / 零样本对照 / 模板选择提示｜用于信息抽取与代码模板选择 | 高｜生成代码后运行 simulation，分析系统性能｜仿真是最后模型有效性的主落点 | 低｜更偏 simulation-based verification / performance checking，不是 formal proof｜承担动态可行性验证 | [paper](./text-to-model-via-sysml/DESC.md) |
| 36 | 🟢 | 直接生成 | Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts | 2025 | 简短自然语言系统描述 | requirements list + state machine diagrams | SysML v2 state machine | Mixtral-8x7B-Instruct、Llama-3-Smaug-8B | 比较 zero/one/few-shot、CoT 和 temperature 对状态机生成的影响 | 高｜zero/one/few-shot、CoT、温度对照｜论文核心就是 prompt technique effect | 无｜无仿真/执行，仅文本质量评测 | 无｜无 formal verification；用 METEOR/质性评审｜不进入 verification 闭环 | [paper](./pushing-the-generative-envelope-mbse-artifacts/DESC.md) |
| 37 | 🟠 | 需求验证邻近 | Inference-Time Intervention in Large Language Models for Reliable Requirement Verification | 2025 | 需求 + Capella/SysML 模型图 | fulfillment 判断 | Requirement verification | Llama-3.1-8B、Claude-3.5 | ITI 干预 + self-consistency 做需求验证 | 中-高｜CoT prompt、self-consistency、ITI steering｜用于让 judge/verifier 更稳 | 无｜无仿真｜模型图转文本后做判定 | 中｜任务是 requirement verification，但基于图表示+LLM推理，不是传统 model checking｜在早期 MBSE 验证上扮演语义判别器 | [paper](./inference-time-intervention-requirement-verification/DESC.md) |
| 38 | 🟠 | 模型对齐 | LLM-Assisted Semantic Alignment and Integration in Collaborative Model-Based Systems Engineering Using SysML v2 | 2025 | 多个 SysML v2 模型 | 语义对齐后的集成模型 | SysML v2 structural model | 原文未强调固定单一模型 | prompt-driven semantic alignment 与 variation-point 集成 | 中｜prompt-driven 对齐与集成｜主要用于模型语义协调 | 无｜无仿真｜无动态角色 | 低｜更偏集成一致性，不是 formal verification｜formal role 弱 | [paper](./llm-assisted-semantic-alignment-sysml-v2/DESC.md) |
| 39 | 🟠 | 需求到用例 | Leveraging Large Language Models for Use Case Model Generation from Software Requirements | 2025 | 软件需求文本 | actors + use cases + 用例模型 | UML use case model | Llama 3.1 70B | actor/use-case 抽取 + prompt engineering | 中｜prompt engineering 辅助 actor/use-case 抽取｜是主要技术变量 | 无｜无运行/仿真 | 无｜无 formal verification｜仅建模生成 | [paper](./leveraging-llms-for-use-case-model-generation/DESC.md) |
| 40 | 🟠 | 需求到类图 | NOMAD: A Multi-Agent LLM System for UML Class Diagram Generation from Natural Language Requirements | 2025 | 自然语言需求 | UML 类图 | UML class diagram | GPT-4o、DeepSeek-V3 | 多智能体拆分实体/关系/图综合 | 高｜多代理分工、结构化 prompt、validator｜是论文核心方法 | 无｜无仿真｜无动态角色 | 低-中｜有 verifier agent / self-consistency 讨论，但定位为 design probe｜主要是结构一致性与错误减少，不是 formal proof | [paper](./nomad-uml-class-diagram-generation/DESC.md) |
| 41 | 🟠 | 需求到类图 | Class Model Generation from Requirements using Large Language Models | 2026 | 自然语言需求 | PlantUML 类图 | UML class diagram | GPT-5、Claude Sonnet 4、Gemini 2.5、Llama-3.1-8B | CoT 生成 + LLM judge + 人工评审 | 中-高｜CoT prompting + judge prompts｜prompt 同时用于生成和评审 | 无｜无运行/仿真 | 低｜judge 评审和 compile 要求不等于 formal verification｜主要是评测与一致性比较 | [paper](./class-model-generation-from-requirements-llm/DESC.md) |
| 42 | 🟠 | 行为补全 | Behavioral Augmentation of UML Class Diagrams: An Empirical Study of Large Language Models for Method Generation | 2025 | 无方法类图 + 结构化 use cases | 增强后的类图与方法签名 | Augmented UML class diagram | 9 个 LLM | 从 use case 推断 methods/params/注释 | 高｜三段 prompt、结构化约束、统一 use-case 输入｜主控制方法生成范围与风格 | 无｜无仿真 | 低｜强调 structural/behavioral consistency 指标，但不做 formal behavior validation｜偏评测框架 | [paper](./behavioral-augmentation-uml-class-diagrams/DESC.md) |
| 43 | 🟠 | Benchmark | MermaidSeqBench: An Evaluation Benchmark for LLM-to-Mermaid Sequence Diagram Generation | 2025 | 文本提示 | Mermaid 顺序图 + 评分 | Sequence diagram benchmark | Qwen/Llama/Granite；judge 为 DeepSeek-V3 / GPT-OSS | 132 样本 benchmark + LLM judge | 中-高｜prompt generation + LLM-as-a-judge prompts｜prompt 主要承担 benchmark 评测协议 | 无｜无运行/仿真 | 低｜有 manual verification 与 syntax correctness，但无 formal verification｜偏评测基准 | [paper](./mermaidseqbench/DESC.md) |
| 44 | 🟠 | 行为模型评估 | MCeT: Behavioral Model Correctness Evaluation using Large Language Models | 2025 | 需求 + 顺序图 | issue 报告 | Sequence diagram evaluation | GPT-4o-mini、GPT-4o、DeepSeek-v3、DeepSeek-R1 | 多检查器 + self-consistency 自动查错 | 高｜P1-P4 prompts、few-shot、CoT、self-consistency、authority cross-check｜prompt 是整个 evaluator 的程序 | 无｜无仿真 | 中｜论文明确区分自己与 formal verification；使用 PlantUML formal syntax + 多检查器推理，但不是模型检查｜扮演非形式文本对图的一致性审查器 | [paper](./mcet/DESC.md) |
| 45 | 🟠 | UML经验研究 | How LLMs Aid in UML Modeling: An Exploratory Study with Novice Analysts | 2024 | 课程案例 + 学生 prompts | 用例图 / 类图 / 顺序图 | UML multi-diagram | ChatGPT | 45 名学生的人机协作建模实验 | 中｜观察不同 prompt patterns 和使用习惯｜是经验研究对象 | 无｜无仿真 | 无｜无 formal verification｜仅教学与质量观察 | [paper](./how-llms-aid-uml-modeling/DESC.md) |
| 46 | 🟠 | 需求到架构 | From Requirements to Architecture: An AI-Based Journey to Semi-Automatically Generate Software Architectures | 2024 | 需求 + 领域模型/用例场景 | 架构候选 | Software architecture | LLaMA（探索性） | 分阶段半自动 requirements-to-architecture 流程 | 中｜分阶段 prompts + 人工精炼｜主要用于架构候选生成 | 无｜无仿真 | 低｜提到 formal ADL 背景，但本文不靠 formal verification｜formal role 弱 | [paper](./from-requirements-to-architecture/DESC.md) |
| 47 | 🟡 | 设计恢复/行为恢复 | Generating Software Architecture Description from Source Code using Reverse Engineering and Large Language Model | 2025 | 源码 + 逆向工程结果 | SAD + component/state machine views | Architecture + state machine views | GPT-4o | reverse engineering + few-shot prompting 恢复组件图和状态机图 | 高｜structured prompt + few-shot + domain examples｜核心用于从代码恢复视图 | 低｜依赖静态分析与少量人工检查，无仿真 | 低｜主要是 static analysis + judge rubric，不是 formal verification｜formal role 弱 | [paper](./generating-software-architecture-description-source-code-llm/DESC.md) |
| 48 | 🟡 | 场景到状态图综合 | Synthesis Revisited: Generating Statechart Models from Scenario-Based Requirements | 2005 | LSC 场景化需求 | UML 风格 statecharts | Statechart | 未使用 | 通过 Play-Engine 把 LSC 需求自动综合为 statecharts | 无｜非 prompt｜场景规格驱动 | 中｜可执行/Play-in/Play-out 背景较强 | 中-高｜LSC 语义与综合约束很强｜承担场景到状态图的形式化综合角色 | [paper](./synthesis-revisited-scenario-based-requirements/DESC.md) |
| 49 | 🟡 | 场景到状态系统综合 | Synthesizing State-Based Object Systems from LSC Specifications | 2002 | LSC 规格 | 状态化对象系统 | State-based object system | 未使用 | 在一致性约束下自动综合满足 LSC 的状态化对象系统 | 无｜非 prompt | 低-中｜重在综合结果可执行语义 | 高｜一致性条件下的自动综合，本质是 formal synthesis | [paper](./synthesizing-state-based-object-systems-from-lsc-specifications/DESC.md) |
| 50 | 🟡 | 多场景到状态图综合 | Synthesizing Statecharts from Multiple Interrelated Scenarios | 2001 | 多个互相关联场景 | statecharts | Statechart | 未使用 | 基于场景关系规则联合综合 statecharts | 无｜非 prompt | 低｜无仿真主线 | 中-高｜场景规则到 statechart 的约束综合｜formal flavor 较强 | [paper](./synthesizing-statecharts-from-multiple-interrelated-scenarios/DESC.md) |
| 51 | 🟡 | 用例到状态图中间建模 | An Approach to Building Object Models with UML in Embedded Systems | 2004 | 嵌入式系统 use case 文本 | statechart + object model | Statechart / object model | 未使用 | 先把 use case 转成 statechart，再基于状态图识别对象 | 无｜非 prompt | 低｜偏中间建模 | 低-中｜规则映射与一致性为主 | [paper](./from-use-cases-to-statecharts/DESC.md) |
| 52 | 🟢 | 用例到状态模型直接建模 | Beyond Scenarios: Generating State Models from Use Cases | 2002 | use case 规格 | state models | State model | 未使用 | 用规则化转换直接从 use case 生成状态模型 | 无｜非 prompt | 低｜无仿真主线 | 中｜规则转换式建模，形式程度中等 | [paper](./beyond-scenarios-generating-state-models-from-use-cases/DESC.md) |
| 53 | 🟡 | 场景与目标驱动行为综合 | Scenarios, Goals, and State Machines: a Win-Win Partnership for Model Synthesis | 2006 | end-user scenarios + goals | 行为模型 | LTS | 未使用 | 把 goals 注入场景综合器，减少提问并生成 LTS | 无｜非 prompt | 低｜无仿真主线 | 中｜目标/场景约束综合，偏形式化学习/综合 | [paper](./scenarios-goals-and-state-machines/DESC.md) |
| 54 | 🟡 | 场景到可解释行为模型 | Generating Annotated Behavior Models from End-User Scenarios | 2006 | MSC 正反例场景 | 带状态注释的局部/全局行为模型 | LTS | 未使用 | 从场景交互式学习 LTS，并自动生成状态不变式 | 无｜非 prompt | 低｜无仿真 | 中｜自动生成状态不变式与行为模型，偏形式化学习 | [paper](./generating-annotated-behavior-models-from-end-user-scenarios/DESC.md) |
| 55 | 🟡 | 场景与性质约束下的 FSM 综合 | Exact Finite-State Machine Identification from Scenarios and Temporal Properties | 2017 | 场景 + temporal properties | FSM | Finite-state machine | 未使用 | 在场景和时序性质约束下精确识别最小 FSM | 无｜非 prompt | 无｜无仿真主线 | 高｜temporal properties 约束 + exact identification｜是典型性质约束下的 formal synthesis | [paper](./exact-finite-state-machine-identification-from-scenarios-and-temporal-properties/DESC.md) |
| 56 | 🟡 | 场景与需求综合协议 | Synthesizing Finite-state Protocols from Scenarios and Requirements | 2014 | 场景 + 安全/活性 requirements | 分布式有限状态协议 | Distributed FSM | 未使用 | 先得不完整状态机，再补全转移关系满足 requirements | 无｜非 prompt | 无｜无仿真主线 | 高｜安全/活性需求满足性驱动协议综合｜formal role 很强 | [paper](./synthesizing-finite-state-protocols-from-scenarios-and-requirements/DESC.md) |
| 57 | 🟢 | 自然语言到定时反应模型 | Modelling Timed Reactive Systems from Natural-Language Requirements | 2016 | 自然语言需求 | DFRS[^dfrs] 模型 | Timed reactive model | 未使用 | 从自然语言需求自动构建 symbolic / expanded DFRS[^dfrs] | 中｜依赖受控/受限需求处理而非 LLM prompt｜需求结构化是关键入口 | 中｜可进一步做模拟/测试，但本篇主线是建模 | 高｜timed reactive formalism / DFRS 建模是核心｜formal model generation 主线 | [paper](./modelling-timed-reactive-systems-from-natural-language-requirements/DESC.md) |
| 58 | 🟢 | 受控自然语言到形式化反应模型 | Modelling and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements | 2019 | 受控自然语言需求 | Coq[^coq] 中的 timed DFRS[^dfrs] | Formal reactive model in Coq[^coq] | 未使用 | 把 CNL 需求自动翻译为 Coq[^coq] 中的 DFRS[^dfrs]，并结合 QuickChick 测试 | 中｜SysReq-CNL 模板化要求是前置“词工程”｜控制需求书写以支持自动翻译 | 中｜QuickChick property-based testing、历史 NAT2TEST 分支也含 simulation｜运行主要为测试生成而非系统仿真 | 高｜Coq 统一建模/证明/测试，well-formedness 与性质验证有形式保证｜是典型 theorem-proving 路线 | [paper](./modelling-and-testing-timed-data-flow-reactive-systems-in-coq/DESC.md) |
| 59 | 🟢 | 受控自然语言到形式化反应模型扩展版 | Validating, Verifying and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements | 2020 | 受控自然语言需求 | Coq[^coq] 中的 timed DFRS[^dfrs] | Formal reactive model in Coq[^coq] | 未使用 | 在 Coq[^coq] 中统一完成 DFRS[^dfrs] 的 validation / verification / testing | 中｜继续依赖 CNL / grammar 驱动自动翻译｜需求语言设计直接决定可验证性 | 中｜bounded exploration + QuickChick 测试生成与执行｜承担 validation / testing 环节 | 高｜Coq 中 formally verified well-formedness，统一 validation / verification / testing｜是最完整的 formal 路线之一 | [paper](./validating-verifying-and-testing-timed-data-flow-reactive-systems-in-coq/DESC.md) |
| 60 | 🟡 | 需求模型到 UML FSM 转换 | A Transformation Approach for Collaboration Based Requirement Models | 2012 | augmented UML activity diagrams | distributed UML FSM | UML finite state machine | 未使用 | 用元模型和 ATL 规则把需求模型自动转换为分布式 FSM | 无｜非 prompt | 无｜无仿真主线 | 中｜模型变换规则是核心，但验证强度有限 | [paper](./transformation-approach-for-collaboration-based-requirement-models/DESC.md) |
| 61 | 🟠 | 用例到形式规范自动提取 | Extração Automática de Modelos CSP a Partir de Casos de Uso | 2011 | 状态化 use cases | CSP 形式模型 | Process algebra model | 未使用 | 用受控自然语言模板把状态化 use case 自动翻译成 CSP | 中｜受控模板承担需求结构化角色 | 无｜无仿真主线 | 高｜输出 CSP，本身面向 formal analysis / model checking 生态 | [paper](./automated-formal-specification-generation-and-refinement-from-requirement-documents/DESC.md) |
| 62 | 🟠 | 需求形式化支持 | Computer-Aided Formalization of Requirements Based on Patterns | 2014 | 文本需求 | 形式化规格 | Formal specification | 未使用 | 用 pattern system 与 HFSM 组织 formalization knowledge 并辅助形式化 | 中｜pattern-based requirement templates｜核心是辅助 formalization | 无｜无仿真 | 中-高｜聚焦 requirement formalization knowledge，而非执行验证｜为 formal verification 前置打底 | [paper](./computer-aided-formalization-of-requirements-based-on-patterns/DESC.md) |

## 数据集与 Benchmark 清单

> 本节按 [GUIDE.md](./GUIDE.md) §6.7 维护，含 `### 数据集可获取性口径` 与正式数据集表两层结构。
>
> **当前覆盖范围**：本表当前回填的是 2026-03-05 时刻已审查的 7 篇“从零生成”论文（来自历史 `BASELINE.md` 中"数据集与代码可获取性分析"段落，commit `f6bea920`）；可获取性口径已按本节 §数据集可获取性口径 从旧 ✅/⚠️/❌ 映射到新 🟢/🟡/🟠/🔒。
>
> **后续待补**：W4.x 期间新增的 baselines（包括但不限于 `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models`、`pushing-the-generative-envelope-mbse-artifacts`、`how-llms-aid-uml-modeling`、`I4.0`、`mermaidseqbench` 等）需在下一轮工作中按相同口径补行。
>
> **配套资产**：4 个数据集（`llms_emp` / `ttool-ai` / `Light Control - Nimbus` / `Structure-and-Event-Driven`）的下载、解析、parquet 化与人评字段对齐已完成，详见 [`../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md`](../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.md)（含 21 个 parquet + 2 个生成脚本）。

### 数据集可获取性口径

| Emoji | 含义 |
|---|---|
| 🟢 | 可直接获取：论文给出了可直接下载、浏览或通过清晰公开渠道直接取得完整内容的链接/入口 |
| 🟡 | 需联系申请：论文明确说明需要联系作者团队、项目方或维护方申请获取，或宣布将后续公开但尚未发布 |
| 🟠 | 信息不清：论文只提到制作方式、来源或使用过该数据，但没有给出足够清晰的获取路径 |
| 🔒 | 难以取得：数据依赖企业/团队内部资料、付费标准、受限工业资产或其他现实上很难取得的来源 |

> 历史 `BASELINE.md` 表格使用的旧符号映射如下，仅供回溯：`✅ 可立即获取 → 🟢`；`⚠️ 部分可获取（论文中描述需自行构建 / 仅演示视频）→ 🟠`；`❌ 未公开（工业专有）→ 🔒`；`❌ 未公开（待发布）→ 🟡`。

### 数据集与 Benchmark 表

| # | 论文 | 评估 | 数据集/Benchmark | 来源类型 | 制作方法 | 输入 | 输出 | 规模 | 可获取性 | 获取方式/链接 | 简述来源 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | [paper](./llms_emp/) | 🟢 | G_Model SysML behavior model dataset | 作者搜集制作 | 从 Google Scholar / CNKI / GitHub 搜集 303 个来源（148 篇英文论文 + 2 本书 + 151 篇中文论文 + 2 个开源项目），使用 PlantUML 重建模型并编写需求描述 | 自然语言需求描述 | PlantUML 格式 SysML STM / ACT / SD | 107 个案例（36 STM / 36 ACT / 35 SD），其中 98 个为完整 input+output 实验样本 | 🟢 | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 通用 SysML 行为模型，包含状态机；与控制系统相关性中等 |
| 3 | [paper](./fsm-gen-iec-61499/) | 🟢 | fbAssistant 工业自动化案例 | 作者制作 | 基于工业自动化实践和 IEC 61499 标准设计的 2 个案例系统，继承作者团队近 30 年的自动机编程研究积累 | 自然语言控制需求 + I/O 接口规范 | 可视化 FSM + IEC 61499 功能块代码 | 2 个案例（气动缸、拾取放置机械手） | 🟠 | [YouTube 演示](https://www.youtube.com/live/aR20KBmZnA4?si=wxyMOcAX4tirRgQf)（仅演示，需根据论文描述复现） | 工业自动化控制系统，IEC 61499 标准；与控制系统相关性高 |
| 4 | [paper](./req/) | 🟢 | Volvo Cars Car Weaver 需求集 | 工业专有 | 来自 Volvo Cars 内部 Car Weaver 工具的 20 个产品功能需求，使用合成数据生成技术扩充训练集 | 自然语言产品功能需求 | Mermaid.js 状态机（Statechart） | 20 个真实需求 + 合成扩充 | 🔒 | 原文未提供公开下载链接；Volvo Cars 专有数据，需联系作者 | 汽车控制系统；工业专有，无法获取 |
| 5 | [paper](./umple/) | 🟢 | Umple 5 测试系统 | 作者设计制作 | 作者设计的 5 个测试系统（Blackjack 基于标准游戏规则、Course Section 来自 Umple 文档，其余 3 个为作者原创设计） | 自然语言需求描述 | Umple 状态机代码 | 5 个系统（Blackjack 等） | 🟠 | 原文未提供公开下载链接；论文中有详细描述，需自行构建 | 通用状态机，非控制系统领域 |
| 6 | [paper](./ttool-ai/) | 🟢 | TTool-AI AVATAR design artifacts | 作者使用现成规范 | 来自 3 个真实欧洲项目的系统规范（Platooning 车辆编队、Space-based 空间系统、Automated Braking 自动刹车） | 自然语言系统规范 | 含状态机的 SysML / AVATAR 联合模型 | 3 个真实案例系统（解析后 15 个模型变体 / 122 状态机面板 / 708 状态 / 798 迁移） | 🟢 | [GitHub ttool-ai](https://github.com/zebradile/ttool-ai) | 包含自动驾驶和航空系统，与控制系统相关性高；代码 + 数据均可立即获取 |
| 7 | [paper](./enhance/) | 🟠 | HDLBits FSM 题集 | 第三方现成 | 直接使用 HDLBits 在线教育平台的 20 个 FSM 设计问题（基础 FSM、同步/异步复位、one-hot 编码等） | HDLBits FSM 设计问题描述 | SystemVerilog FSM 代码 | 20 个 FSM 设计问题 | 🟢 | [HDLBits 平台](https://hdlbits.01xz.net/) | 硬件 FSM 设计，偏向数字电路；与控制系统软件需求关联较弱 |
| 8 | [paper](./LLM-FSM/) | 🟠 | LLM-FSM benchmark | 作者完全自动生成 | 自动化 pipeline 生成（约束随机 FSM 生成 → YAML 格式化 → LLM 生成 NL 规范 → 参考 RTL 合成 → 多层验证） | FSM 配置参数 + 自然语言规范 | Verilog RTL 代码 + 测试平台 | 1000 个 FSM-to-RTL 问题 | 🟡 | 原文未提供下载链接；需关注后续发布或联系作者 | RTL 代码生成，偏向硬件设计 |

## 初步归类与覆盖盘点

### 类别分布

| 类别 | 篇数 | 说明 |
|---|---:|---|
| 直接状态机建模 | 17 | 直接从自然语言、结构化需求、use case 或场景规格得到状态机/状态化规格的核心基线 |
| 补全/精化/扩展/集成 | 17 | 围绕已有模型、场景、目标或形式化需求做状态机补全、综合、调试、恢复、执行化或双层集成 |
| 需求形式化/分析/状态抽取 | 7 | 需求 DSL、时序逻辑、状态抽取与需求语义分析等前置/支撑方法 |
| 邻近建模与控制逻辑 | 21 | 非状态机输出的 UML/goal/domain/control-logic/benchmark 邻近工作与多模态/代码生成参照 |

### BASELINE评估分布

| 评估 | 篇数 | 说明 |
|---|---:|---|
| 🟢 | 14 | 可与“需求/描述到状态机或等价状态化规格”直接对比的核心 baseline；新增的 2026 预印本首次把任务明确推进到“非结构化自由文本 -> UML 状态机” |
| 🟡 | 19 | 围绕场景/用例/目标/需求模型做状态机综合、扩展、调试、恢复或形式化执行化，但入口不是纯自然语言长文本 |
| 🟠 | 29 | 邻近建模、形式规范、benchmark、需求形式化、控制逻辑生成、FSM代码生成或评测基础设施，可借鉴但不可直接公平对比 |
| ⚪ | 0 | 当前正式收录中暂无仅作背景资料的论文 |

### 当前最有价值的整体观察

1. `Structure- and Event-Driven Frameworks...` 是当前文库里最直接回答“非结构化自由文本能否直接生成状态机”的新基线；它表明 direct baseline 已经出现，但 guard、action 和复杂结构仍是主要短板。
2. 这篇 2026 预印本还说明“多步 prompting 是否有效”依赖模型类型：`GPT-4o` 受益于 `Structure-Driven/Hybrid`，但 `Claude 3.5 Sonnet` 反而以 `Single-Prompt` 最优。
3. 真正与 `project_1` 任务定义长期最贴近的条目，仍有不少来自前大模型时代的经典线路；尤其是 `use case/scenario -> state model` 和 `controlled NL -> reactive model` 两条线最有产出。
4. 经典直接基线往往不直接处理完全自由的自然语言，而是要求中间层更规整，例如 `LSC`、`MSC`、`use case`、`controlled natural language`；因此“先规范化、再综合”仍然是需要与 direct prompting 并行比较的主线。
5. 若只盯 `statechart` 关键词，会漏掉不少高度相关工作；很多直接基线实际输出 `LTS`、`FSM`、`DFRS` 或 `Coq` 中的反应式模型，但任务本质仍是需求到行为模型自动建模。
6. 时间与反应约束处理在经典文献里主要由 `DFRS / Coq / timed reactive systems` 这条线承担，这对控制系统建模比泛 UML 生成更有直接价值。
7. 多个经典场景综合论文表明：需求到状态机往往不是一次成图，而是“场景采样 -> 不完整行为模型 -> 补全/约束求解”的过程，这对本研究的生成-验证-修复闭环很有启发。
8. 后续继续扩检时，应优先追 `non-structured requirements + state machine + LLM` 与 `use case/scenario/MSC/LSC/CNL + statechart/LTS/FSM/reactive model` 这两条线，而不是继续扩张到一般 UML 结构图生成。

## 待补充高优先级候选

以下候选已在 `project_1` 根目录历史工作文档中出现，后续若正式收录，应优先进入本论文集：

| 优先级 | 标题 | 来源文档 | 当前价值 |
|---|---|---|---|
| 中 | 当前暂无比现有条目更高优先级的新增状态机候选 | - | 后续应继续优先检索题名或摘要显式出现 `state machine diagrams`、`SysML behavior`、`behavioral model` 的预印本，而不是继续扩张到一般 UML 建模 |

## 更新日志

| 时间 | 更新内容 | 说明 |
|---|---|---|
| 2026-05-09 16:18:22 | 回填 `## 数据集与 Benchmark 清单` 章节 | 按 [GUIDE.md](./GUIDE.md) §6.7 在 `## 论文清单` 与 `## 初步归类与覆盖盘点` 之间补回长期缺失的 §`数据集与 Benchmark 清单` 与 §`数据集可获取性口径` 两个小节；7 行可获取性内容直接复用历史 `BASELINE.md` 中 commit `f6bea920`（2026-03-05）的 `数据集与代码可获取性分析` 段落，旧 ✅/⚠️/❌ 按 GUIDE §5.3 映射为 🟢/🟡/🟠/🔒；W4.x 期间新增的 baseline（如 `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 等）暂未补行，待下一轮统一审查。 |
| 2026-05-06 13:54:54 | 标注 3 篇硬条件符合论文同时进入 `state_machine_review_corpus/` | `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` / `llms_emp` / `ttool-ai` 现同时存在于本论文集与 `state_machine_review_corpus/`；前者从 baseline 方法对照角度，后者从可获取 human review 数据资产角度。各自维护独立的派生文件（`DESC.md` 留在本文库；`review_extraction.md` 在新文库）。论文总表对应行追加 `· [review](../state_machine_review_corpus/<slug>/review_extraction.md)` 链接。 |
| 2026-04-16 12:41:58 | 在论文总表新增 `需求词工程 / 运行仿真 / 形式化验证` 三列并逐篇回填 | 基于全文阅读，统一按“程度｜技术｜角色”补齐 62 篇论文，重点区分 LLM 工作中的 prompt engineering、simulation/execution 与真正 formal verification；其中 `llms_emp`、`ttool-ai` 等带检查反馈环的论文，明确不把单纯语法/规则/静态检查误记为高强度形式化验证 |
| 2026-04-14 17:29:20 | 新增 `Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models` 并补齐 baseline 四件套 | 新增目录 `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models`，补齐 `paper.pdf / paper_content.txt / bibtex.bib / DESC.md`，并回填论文清单、数据集表、类别统计、BASELINE评估统计与整体观察；该文是当前最直接命中“非结构化自然语言 -> UML 状态机”的 2026 arXiv baseline |
| 2026-03-12 17:00:14 | 新增 15 篇更贴近 `自然语言/用例/场景/需求模型 -> 状态机或等价行为模型` 的经典前身与传统自动化方法 | 本轮补入 `synthesis-revisited-scenario-based-requirements`、`synthesizing-state-based-object-systems-from-lsc-specifications`、`synthesizing-statecharts-from-multiple-interrelated-scenarios`、`from-use-cases-to-statecharts`、`beyond-scenarios-generating-state-models-from-use-cases`、`scenarios-goals-and-state-machines`、`generating-annotated-behavior-models-from-end-user-scenarios`、`exact-finite-state-machine-identification-from-scenarios-and-temporal-properties`、`synthesizing-finite-state-protocols-from-scenarios-and-requirements`、`modelling-timed-reactive-systems-from-natural-language-requirements`、`modelling-and-testing-timed-data-flow-reactive-systems-in-coq`、`validating-verifying-and-testing-timed-data-flow-reactive-systems-in-coq`、`transformation-approach-for-collaboration-based-requirement-models`、`automated-formal-specification-generation-and-refinement-from-requirement-documents`、`computer-aided-formalization-of-requirements-based-on-patterns`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 15:55:26 | 新增 15 篇以 arXiv/作者版预印本为主的 LLM baseline/邻近论文 | 本轮补入 `workflow-level-design-principles-trustworthy-genai-automotive`、`sysmbench-system-model-generation-benchmark`、`text-to-model-via-sysml`、`pushing-the-generative-envelope-mbse-artifacts`、`inference-time-intervention-requirement-verification`、`llm-assisted-semantic-alignment-sysml-v2`、`leveraging-llms-for-use-case-model-generation`、`nomad-uml-class-diagram-generation`、`class-model-generation-from-requirements-llm`、`behavioral-augmentation-uml-class-diagrams`、`mermaidseqbench`、`mcet`、`how-llms-aid-uml-modeling`、`from-requirements-to-architecture`、`generating-software-architecture-description-source-code-llm`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 14:55:59 | 新增 15 篇更贴近任务定义的 baseline/经典前身/邻近支撑论文 | 本轮补入 `completion-of-sysml-state-machines-from-gwt-requirements`、`enhancing-model-based-development-formalized-requirements`、`extraction-of-system-states-from-natural-language-requirements`、`executable-state-machines-derived-from-structured-textual-requirements`、`automatic-synthesis-of-uml-designs-from-requirements`、`tech-report-neural-language-models-few-shot-mdse`、`spec2control`、`specification-based-prototyping-for-embedded-systems`、`nimbus-tool-for-specification-centered-development`、`requirements-capture-and-evaluation-in-nimbus-light-control`、`requirements-specification-for-process-control-systems`、`software-requirements-analysis-for-real-time-process-control`、`automatic-debugging-support-for-uml-designs`、`integrating-inter-object-scenarios-with-intra-object-statecharts`、`formal-requirements-elicitation-with-fret`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 14:07:52 | 新增 5 篇 baseline 并补齐单篇分析 | 新增 `chatgpt-uml-assessment`、`requirements-to-uml-sequence-diagrams`、`from-image-to-uml`、`few-shot-model-completion`、`gpt4-goal-models`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 13:23:51 | 建立 `baselines/` 四件套并统一命名 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)，并将全部 `desc.md` 更名为 `DESC.md` |
| 2026-03-12 13:23:51 | 补充 BASELINE 评估、输入输出方法字段和数据集总表 | 将论文清单改为固定字段表，并新增“数据集与 Benchmark 清单” |
| 2026-03-12 13:23:51 | 细化数据集可获取性口径与链接写法 | 为数据集表新增 `🟢/🟡/🟠/🔒` 口径，并将已确认的公开地址统一改为 Markdown 链接 |
