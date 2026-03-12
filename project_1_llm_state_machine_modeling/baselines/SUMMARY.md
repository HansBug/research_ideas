# Project 1 Baselines Summary

本文件是 `project_1_llm_state_machine_modeling/baselines/` 的总账，用于记录当前已经正式入账的 baseline 论文、统一比较口径、数据集与 benchmark 盘点、待补充候选与更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 再使用本文件查看统计、论文清单、数据集盘点和待补充候选。
4. 若需要重写某篇单论文分析，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。

## 当前收录统计

- 已收录 baseline 论文：**31** 篇
- 本轮新增论文：**15** 篇
- 已完成 `DESC.md`：**31** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮规范化工作：新增 15 篇 baseline 论文目录并补齐 `paper.pdf / paper_content.txt / bibtex.bib / DESC.md`

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

### 已观察到的高命中特征

- 题名同时出现 `LLM` 与 `state machine/statechart/FSM/SysML behavior`
- 明确写出输入输出链路，如 `requirements -> statechart`、`diagram -> code/test`
- `partial model -> completion/repair` 且对象明确是状态机时，命中率更稳定
- 出现 `iterative`、`refinement`、`feedback`、`few-shot`、`RAG` 等方法词
- 安全关键或工业领域关键词常能带来更贴近 `project_1` 的论文
- `process-control`、`reactive systems`、`RSML`、`state-based specification` 这条经典控制软件线索很容易找到高任务对齐前身工作
- `Given-When-Then`、`LTL -> state machine`、`sequence diagrams -> statecharts` 这类显式桥接链路词，命中率明显高于泛 MBSE 关键词

### 已观察到的低命中特征

- `FSM` 仅用于提示范式、规划器、对话流或智能体编排
- 纯机器人执行流程、纯协议推理、纯智能合约生成但无建模工件
- 输出是顺序图、类图、goal model、一般 domain model 的论文默认不是本 collection 的主线
- 纯教学经验、课堂问卷或学习体验类 UML 论文通常弱于“真正生成模型”的论文
- 纯综述、纯经验报告，缺少明确方法与实验对比
- 只做 requirements formalization、DSL 翻译或 temporal logic 输出的论文，若没有状态机落点，通常只能保留为 `🟠`
- 控制逻辑图、功能块图、PLC/DCS 工程图等虽然很贴近工业控制，但若没有显式状态机语义，也不能直接算 `🟢`

### 检索倾向调整

- 优先补“直接生成状态机模型”和“带反馈闭环的状态机精化/修复”两类工作
- 当 LLM 直接命中不足时，优先补“任务定义高度一致”的经典非 LLM 前身，而不是继续扩张到泛建模论文
- 泛 UML/SysML 论文仅在其方法明确输出状态机时保留
- 多模态图样识别和自动 benchmark 构建可保留，但需在 `DESC.md` 中明确说明其“邻近 baseline”性质
- 非状态机输出论文原则上不再继续扩张收录，只在少量必要场合作为弱相关参照保留

## 论文清单

| # | 评估 | 类别 | 标题 | 年份 | 输入 | 输出 | 输出模型类型 | 使用的LLM | 主要方法 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | 🟢 | 直接生成 | Generating SysML Behavior Models via Large Language Models: an Empirical Study | 2025 | 自然语言需求描述 | PlantUML 格式行为模型 | SysML STM / ACT / SD | GPT-4、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 | 两阶段框架：提示生成 + 模型检查反馈修复 | [paper](./llms_emp/DESC.md) |
| 2 | 🟢 | 直接生成 | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | 自然语言控制需求 + I/O 接口规范 | 可视化 FSM + IEC 61499 功能块代码 | FSM | 未明确指定 | 自然语言到 FSM 的迭代精化，并接入仿真和代码生成 | [paper](./fsm-gen-iec-61499/DESC.md) |
| 3 | 🟢 | 直接生成 | Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering | 2025 | 自然语言产品功能需求 | Mermaid.js 状态机 | Statechart | GPT-3.5、GPT-4、GPT-4o（微调） | NLP 特征提取 + 合成数据扩充 + 领域微调生成状态机 | [paper](./req/DESC.md) |
| 4 | 🟢 | 直接生成 | Exploring How Well Llama3 can Generate State Machines Represented in Umple | 2025 | 自然语言需求描述 | Umple 状态机代码 | Umple 状态机 | Llama 3 (8B) | 比较 Zero-shot、One-shot 与 RAG 三种提示策略 | [paper](./umple/DESC.md) |
| 5 | 🟢 | 直接生成 | System Architects Are not Alone Anymore: Automatic System Modeling with AI | 2024 | 自然语言系统规范 | SysML 块图、内部块图和状态机图 | 含状态机的 SysML 联合模型 | GPT-4 | 知识注入 + 自动反馈循环 + TTool 工具链集成 | [paper](./ttool-ai/DESC.md) |
| 6 | 🟠 | FSM代码生成 | Enhancing Finite State Machine Design Automation with Large Language Models and Prompt Engineering Techniques | 2024 | HDLBits FSM 设计问题描述 | SystemVerilog FSM 代码 | FSM 代码工件 | Claude 3 Opus、GPT-4、GPT-4o | Markdown 提示模板 + TOP Patch + CoT 多轮对话 | [paper](./enhance/DESC.md) |
| 7 | 🟠 | FSM代码生成 | LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation | 2026 | FSM 配置参数 + 自然语言规范 | Verilog RTL 代码 + 测试平台 | RTL / 测试工件 | GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro 等 | 自动构建 FSM-to-RTL benchmark 并系统评估有限状态推理 | [paper](./LLM-FSM/DESC.md) |
| 8 | 🟡 | 精化/修复 | LLM-based iterative refinement of finite-state machines with STPA controller constraints and generation of IEC 61499 code | 2025 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | FSM | OpenAI GPT（通过 fbAssistant） | 用 STPA 约束驱动递归迭代精化 | [paper](./STPA/DESC.md) |
| 9 | 🟡 | 精化/扩展 | State Diagram Extension and Test Case Generation Based on Large Language Models for Improving Test Engineers’ Efficiency in Safety Testing | 2024 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | State Diagram | Qwen2-72B-Instruct（微调） | 安全准则提取 + 状态图扩展 + 测试路径/数据生成 | [paper](./safety/DESC.md) |
| 10 | 🟠 | 泛建模 | Multi-step Iterative Automated Domain Modeling with Large Language Models | 2024 | 自然语言问题描述 / 领域描述文本 | 领域模型 | UML 类图 / 领域模型 | GPT-4 | 多步任务分解 + few-shot + 迭代优化 | [paper](./MIG/DESC.md) |
| 11 | 🟡 | 多模态邻近 | Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition | 2025 | 状态图图像（来自工业规范 PDF） | 状态机表示 + C++ 代码 + 测试 | 图像状态图 / 可机读状态机表示 | gpt-4o、claude-3-sonnet、Llama-3.2-11b | 图像裁剪 + LLM 识别 + 模板化代码/测试生成 | [paper](./I4.0/DESC.md) |
| 12 | 🟠 | 泛建模经验 | On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML | 2023 | 自然语言建模任务描述 + 修正提示 | UML 类图 + OCL 约束 | UML 类图 / OCL | ChatGPT | 经验性对话实验，系统评估 UML/OCL 建模能力与缺陷模式 | [paper](./chatgpt-uml-assessment/DESC.md) |
| 13 | 🟠 | 邻近行为建模 | Model Generation with LLMs: From Requirements to UML Sequence Diagrams | 2024 | 自然语言需求文档 | UML sequence diagram | UML 顺序图 | ChatGPT | 从真实需求文档直接生成顺序图，并做问题主题分析 | [paper](./requirements-to-uml-sequence-diagrams/DESC.md) |
| 14 | 🟠 | 多模态邻近 | From Image to UML: First Results of Image-Based UML Diagram Generation Using LLMs | 2024 | UML 类图图像 / 手绘图 | PlantUML 类图代码 | UML 类图 | GPT-4V、Gemini Pro、Gemini Ultra、CogVLM | 多模态图像识别到 PlantUML 的重复实验比较 | [paper](./from-image-to-uml/DESC.md) |
| 15 | 🟠 | 泛建模补全 | Towards using Few-Shot Prompt Learning for Automating Model Completion | 2023 | 部分 UML 类图 / 活动图 | 类、属性、关联名与活动流补全建议 | UML 类图 / 活动图 | GPT-3 (`text-davinci-002`) | 将模型补全转写为 few-shot prompt learning 任务 | [paper](./few-shot-model-completion/DESC.md) |
| 16 | 🟠 | 泛建模 | On the Use of GPT-4 for Creating Goal Models: An Exploratory Study | 2023 | 领域描述 + TGRL 语法提示 | GRL/TGRL 目标模型 | Goal model | GPT-4 | 多 prompt、多次运行与结果聚合的目标建模探索 | [paper](./gpt4-goal-models/DESC.md) |
| 17 | 🟡 | 状态机补全 | Completion of SysML state machines from Given–When–Then requirements | 2024 | 部分 SysML 模型 + GWT 需求 | 补全后的 SysML 状态机 | SysML state machine | 未使用 | GWT 需求规则化后补全迁移与 traceability | [paper](./completion-of-sysml-state-machines-from-gwt-requirements/DESC.md) |
| 18 | 🟡 | 形式化需求到状态机 | Enhancing model-based development with formalized requirements: integrating temporal logic and SysML v2 for comprehensive state and transition modeling | 2025 | LTL 形式化需求 | SysML v2 状态机 | SysML v2 state machine | 未使用 | LTL 生成允许状态/迁移并编译到 SysML v2 | [paper](./enhancing-model-based-development-formalized-requirements/DESC.md) |
| 19 | 🟠 | 需求状态抽取 | Extraction of System States from Natural Language Requirements | 2019 | 自然语言需求文本 | 状态实体/状态短语 | 状态标签列表 | BiLSTM-CNN | 需求文本 NER 抽取系统状态 | [paper](./extraction-of-system-states-from-natural-language-requirements/DESC.md) |
| 20 | 🟢 | 经典直接建模 | Executable State Machines Derived from Structured Textual Requirements - Connecting Requirements and Formal System Design | 2019 | 结构化文本需求 | 可执行有限状态机模型 | Executable FSM | 未使用 | 结构化需求 -> 时序逻辑 -> 状态机 -> 可执行模型 | [paper](./executable-state-machines-derived-from-structured-textual-requirements/DESC.md) |
| 21 | 🟠 | 邻近UML设计生成 | Automatic Synthesis of UML Designs from Requirements in an Iterative Process | 2002 | 用例 / 场景 / Sequence Diagrams | UML 设计工件（含 statecharts） | UML statecharts + class diagrams | 未使用 | 场景驱动综合 UML 设计并在迭代中保持一致性 | [paper](./automatic-synthesis-of-uml-designs-from-requirements/DESC.md) |
| 22 | 🟠 | 需求形式化 | Technical Report on Neural Language Models and Few-Shot Learning for Systematic Requirements Processing in MDSE | 2022 | 非正式汽车需求 | Requirement DSL | Requirement DSL | 预训练语言模型（few-shot） | few-shot requirements-to-DSL 翻译 | [paper](./tech-report-neural-language-models-few-shot-mdse/DESC.md) |
| 23 | 🟠 | LLM控制逻辑邻近 | Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs - A Multi-Plant Evaluation | 2025 | 自然语言 control narratives | 图形化 PLC/DCS 控制逻辑 | Graphical control logic | GPT-5 等 | 从 control narrative 识别策略/连接/报警并生成控制逻辑图 | [paper](./spec2control/DESC.md) |
| 24 | 🟡 | 状态机执行化 | Specification-based Prototyping for Embedded Systems | 1999 | 形式化需求规格 | 可执行层次状态机原型 | Hierarchical state machine prototype | 未使用 | 把规格当作原型执行并沿层次状态机做 refinement | [paper](./specification-based-prototyping-for-embedded-systems/DESC.md) |
| 25 | 🟠 | 工具环境 | NIMBUS: A Tool for Specification Centered Development | 2000 | RSML-e 规格 | 分析/执行/代码测试工件 | RSML-e toolchain | 未使用 | 围绕 RSML-e 提供分析、仿真、代码生成与测试 | [paper](./nimbus-tool-for-specification-centered-development/DESC.md) |
| 26 | 🟢 | 经典直接建模 | Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study | 2000 | 灯光控制系统需求 | RSML-e 状态化需求模型 | State-based requirements model | 未使用 | 用 RSML-e + Nimbus 捕获并执行灯光控制需求 | [paper](./requirements-capture-and-evaluation-in-nimbus-light-control/DESC.md) |
| 27 | 🟢 | 经典直接建模 | Requirements Specification for Process-Control Systems | 1994 | 过程控制系统需求 | 形式化状态化需求规格 | State-based formal requirements spec | 未使用 | 面向过程控制的规格语言建模并以 TCAS II 演示 | [paper](./requirements-specification-for-process-control-systems/DESC.md) |
| 28 | 🟠 | 需求分析 | Software Requirements Analysis for Real-Time Process-Control Systems | 1991 | 状态机式需求规格 | 语义分析准则 | Semantic analysis criteria | 未使用 | 基于抽象状态机模型定义需求分析准则 | [paper](./software-requirements-analysis-for-real-time-process-control/DESC.md) |
| 29 | 🟡 | 状态机补全/调试 | Automatic Debugging Support for UML Designs | 2000 | Annotated sequence diagrams | Structured statecharts + 冲突解释 | Structured statecharts | 未使用 | 序列图综合 statecharts 并做 backward debugging | [paper](./automatic-debugging-support-for-uml-designs/DESC.md) |
| 30 | 🟡 | 需求-状态机集成 | Integrating Inter-Object Scenarios with Intra-object Statecharts for Developing Reactive Systems | 2020 | LSC 场景规格 | LSC + Statecharts 联合模型 | Integrated scenario-statechart model | 未使用 | 将 scenario-based programming 与 Statecharts 联合执行 | [paper](./integrating-inter-object-scenarios-with-intra-object-statecharts/DESC.md) |
| 31 | 🟠 | 需求形式化 | Formal Requirements Elicitation with FRET | 2020 | FRETish 需求 | FRETish + 时序逻辑 | Restricted NL / temporal logic | 未使用 | 受限自然语言到时序逻辑、解释与仿真分析入口 | [paper](./formal-requirements-elicitation-with-fret/DESC.md) |

## 数据集与 Benchmark 清单

### 数据集可获取性口径

| Emoji | 含义 |
|---|---|
| 🟢 | 可直接获取：论文给出了可直接下载、浏览或通过清晰公开渠道直接取得完整内容的链接/入口 |
| 🟡 | 需联系申请：论文明确说明需要向作者团队、项目方或维护方申请后才能获取 |
| 🟠 | 信息不清：论文只提到制作方式、来源或使用过该数据，但未给出足够清晰的获取路径 |
| 🔒 | 难以取得：数据依赖企业/团队内部资料、付费标准、受限工业资产或其他现实上很难取得的来源 |

说明：

1. 本表的 `#` 与上方“论文清单”的 `#` 严格一一对应。
2. 每篇论文在本表中只占一行；若原文涉及多个数据源或 benchmark，应合并写入同一行，而不是拆成多行。
3. `论文` 列统一使用 `[paper](./subdir/DESC.md)` 形式的跳转链接，不再显示子目录名。

| # | 论文 | 评估 | 数据集/Benchmark | 来源类型 | 制作方法 | 输入 | 输出 | 规模 | 可获取性 | 获取方式/链接 | 简述来源 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [paper](./llms_emp/DESC.md) | 🟢 | G_Model SysML 行为模型数据集 | 自己搜集制作 | 从 Google Scholar、CNKI、GitHub 搜集 303 个来源，经筛选后统一重建为 PlantUML + 需求描述并交叉验证 | 自然语言需求描述 | SysML 行为模型（ACT/STM/SD） | 107 个行为模型（36 ACT / 36 STM / 35 SD） | 🟢 | [Google Drive 数据集](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 从学术文献、教材和开源项目中系统重建的公开行为模型集 |
| 2 | [paper](./fsm-gen-iec-61499/DESC.md) | 🟢 | fbAssistant 工业案例集 | 自己制作 | 基于工业自动化实践和 IEC 61499 标准设计 2 个案例系统，并配套 I/O 接口和需求规格 | 自然语言控制需求 + I/O 规格 | FSM + IEC 61499 功能块代码 | 2 个案例系统 | 🟠 | 原文未提供公开数据集/代码链接；仅公开了 [工具演示视频](https://www.youtube.com/live/aR20KBmZnA4?si=wxyMOcAX4tirRgQf) | 基于作者团队长期工业自动化研究积累设计的典型控制系统案例 |
| 3 | [paper](./req/DESC.md) | 🟢 | Volvo Cars 需求数据 + 合成扩充数据 | 工业专有数据 | 使用 Volvo Cars 内部 Car Weaver 的 20 个真实需求，并通过受控随机化生成合成训练数据 | 自然语言产品功能需求 | Mermaid 状态机 | 20 个真实需求 + 合成扩充数据；12 个测试用例 | 🔒 | 原文未提供公开下载链接 | 来自汽车工业内部需求管理工具的真实产品功能需求 |
| 4 | [paper](./umple/DESC.md) | 🟢 | 5 个 Umple 测试系统 | 自己设计制作 | 作者设计 5 个测试系统，包含需求描述和参考状态机，其中 Course Section 来自 Umple 文档 | 自然语言需求描述 | Umple 状态机代码 | 5 个系统 | 🟠 | 论文正文给出需求与参考示例，但无独立下载页 | 基于 Umple 建模语言特点设计的小规模测试集 |
| 5 | [paper](./ttool-ai/DESC.md) | 🟢 | 3 个真实系统规范案例 | 使用现成规范 | 使用 3 个欧洲项目真实系统规范做工具与人工对照实验，并公开规范、模型和结果 | 自然语言系统规范 | SysML 块图、内部块图、状态机 | 3 个系统 | 🟢 | [GitHub 实验工件](https://github.com/zebradile/ttool-ai) | 来自真实欧洲安全关键系统项目的公开实验工件 |
| 6 | [paper](./enhance/DESC.md) | 🟠 | HDLBits FSM 设计问题集 | 使用现成数据集 | 直接使用 HDLBits 在线平台中的 FSM 设计问题作为测试集 | FSM 设计问题描述 | SystemVerilog FSM 代码 | 20 个 FSM 设计问题 | 🟢 | [HDLBits FSM 题库](https://hdlbits.01xz.net/) | 公开硬件设计教育平台的 FSM 练习题 |
| 7 | [paper](./LLM-FSM/DESC.md) | 🟠 | LLM-FSM benchmark | 自动化生成 | 约束随机 FSM 生成 + LLM 生成 YAML 与自然语言规范 + 正确性构造 RTL/testbench + 多层验证 | FSM 配置参数 + 自然语言规范 | RTL 代码 + 测试平台 | 1000 个 FSM-to-RTL 问题（状态 2-16） | 🟠 | 论文公开，但 benchmark 文件未给出明确下载链接 | 通过自动化 pipeline 生成的大规模 FSM 推理 benchmark |
| 8 | [paper](./STPA/DESC.md) | 🟡 | Pick-and-Place + STPA 约束实验集 | 自己制作 | 对 pick-and-place 机器做 STPA 分析，生成 UCA 与控制器约束，再做多轮迭代实验 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | 9 个约束 × 20 次迭代 + 1 组组合约束 × 10 次迭代 = 190 次迭代 | 🟡 | 原文未提供公开下载链接；当前可行路径更接近联系作者获取 STPA 结果与实验记录 | 基于单个工业案例和手工 STPA 分析构建的精化实验集 |
| 9 | [paper](./safety/DESC.md) | 🟡 | 航空高度控制安全测试案例 | 自己制作 + 在线收集 | 使用航空高度控制系统案例，并从 DO-178C、ARP4754A 提取 4 类 25 项安全准则，结合在线爬取需求做实验 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | 单个航空案例 + 25 项安全准则 | 🟡 | 原文未提供公开下载链接，文意上更接近联系作者团队获取 | 面向航空安全测试的状态图扩展与测试生成案例 |
| 10 | [paper](./MIG/DESC.md) | 🟠 | 公开领域建模数据集（原文未明确命名） | 公开数据集（细节未明确） | 原文说明使用公开领域建模数据集和人工标注参考模型，但未细述构造流程 | 自然语言问题描述 / 领域描述文本 | 领域模型 | 原文未明确 | 🟠 | 原文未提供公开下载链接 | 用于评估多步领域建模效果的公开类图/领域模型数据 |
| 11 | [paper](./I4.0/DESC.md) | 🟡 | PROFINET / OPC UA 状态图识别数据 | 使用现成规范并人工裁剪 | 从 IEC 61158 和 IEC 62541 规范 PDF 中手工裁剪状态图，并对公开版本做文本打乱处理 | 状态图图像 | 可机读状态机表示 + 代码/测试 | PROFINET 80 个状态图 + OPC UA 15 个状态图 | 🔒 | [Zenodo 实现与处理结果](https://zenodo.org/records/14730727)；原始标准文档需购买 | 来自工业通信协议规范文档的状态图图像数据 |
| 12 | [paper](./chatgpt-uml-assessment/DESC.md) | 🟠 | ChatGPT-UML 练习与实验记录 | 自己制作 | 作者围绕 UML 类图与 OCL 准备 40 个练习，并记录对话实验与报告 | 自然语言建模任务描述 | UML 类图 + OCL | 40 个练习，8 个代表性模型做深入实验 | 🟢 | [GitHub 仓库](https://github.com/atenearesearchgroup/chatgpt-uml) | 面向 ChatGPT 建模能力评估的公开实验工件 |
| 13 | [paper](./requirements-to-uml-sequence-diagrams/DESC.md) | 🟠 | 28 份需求文档评估集 | 混合公开/工业数据 | 从 Lockheed Martin 挑战集、PURE 和 user story 数据中筛出 28 份真实需求文档，并附评估日志 | 自然语言需求文档 | UML sequence diagram | 28 份文档，18 个领域 | 🟢 | [Zenodo replication package](https://doi.org/10.5281/zenodo.10579731) | 面向需求到顺序图生成的真实需求评估集 |
| 14 | [paper](./from-image-to-uml/DESC.md) | 🟠 | IMG2UML examples | 自己制作 + 开源示例 | 准备 4 张 UML 类图图像，比较 4 个视觉 LLM 在不同 prompts 下的转写效果 | UML 类图图像 | PlantUML 类图代码 | 4 个图像样例 × 3 prompts × 3 runs | 🟢 | [IMG2UML-Examples](https://github.com/BESSER-PEARL/IMG2UML-Examples) | 面向图像到 UML 转写的开放示例集 |
| 15 | [paper](./few-shot-model-completion/DESC.md) | 🟠 | ModelSet + activity diagram examples | 使用现成数据集 | 从 ModelSet 中选取 30 个领域模型做类名补全，并基于公开活动图示例展示动态图补全 | 部分 UML 类图 / 活动图 | 模型补全建议 | 30 个领域模型；212 个类；40 对关联名 | 🟢 | [GitHub 仓库](https://github.com/meriembenchaaben/model-completion) | 面向模型补全的 few-shot prompting 实验工件 |
| 16 | [paper](./gpt4-goal-models/DESC.md) | 🟠 | GRL_GPT prompts 与评分结果 | 自己制作 | 整理 18 个 goal-modeling 问题和 2 个案例的 prompts、评分结果与实验记录 | 领域描述 + TGRL 提示 | GRL/TGRL 目标模型 | 18 个问题 + 2 个案例 | 🟢 | [GitHub 仓库](https://github.com/ChenKua/GRL_GPT) | 面向 GPT-4 目标建模评估的开放实验记录 |
| 17 | [paper](./completion-of-sysml-state-machines-from-gwt-requirements/DESC.md) | 🟡 | ETCS Level 3 + 医疗告警系统案例 | 案例系统 | 基于部分 SysML 模型和 GWT 需求做状态机补全与 traceability 建模 | 部分 SysML 模型 + GWT 需求 | SysML 状态机 | 2 个案例 | 🟠 | 原文未提供公开下载链接 | 关键系统案例驱动的状态机补全实验 |
| 18 | [paper](./enhancing-model-based-development-formalized-requirements/DESC.md) | 🟡 | 汽车照明系统示例 | 简化工业示例 | 将需求人工形式化为 LTL，再自动生成允许状态/迁移并落到 SysML v2 | LTL 形式化需求 | SysML v2 状态机 | 1 个示例 | 🟠 | 原文未提供公开数据集下载链接 | 车辆功能需求的形式化与状态机建模示例 |
| 19 | [paper](./extraction-of-system-states-from-natural-language-requirements/DESC.md) | 🟠 | 需求状态抽取语料 | 需求文档 | 人工/半自动标注约 2000 条需求，用于训练状态抽取 NER 模型 | 自然语言需求文本 | 状态实体 | 约 2000 条需求 | 🟠 | 原文未提供公开语料链接 | 用于从需求文本中抽取状态短语的标注语料 |
| 20 | [paper](./executable-state-machines-derived-from-structured-textual-requirements/DESC.md) | 🟢 | Adaptive Outside Light Control 案例 | 工业汽车案例 | 将结构化文本需求映射到时序逻辑，再生成可执行状态机 | 结构化文本需求 | Executable FSM | 1 个工业案例 | 🟠 | 原文未提供公开下载链接 | Daimler 汽车系统的可执行状态机派生案例 |
| 21 | [paper](./automatic-synthesis-of-uml-designs-from-requirements/DESC.md) | 🟠 | 场景驱动 UML 设计示例 | 说明性示例 | 从用例和场景综合 UML 设计，并在迭代中保持一致 | 用例 / 场景 / Sequence Diagrams | UML 设计工件（含 statecharts） | 原文未明确 | 🟠 | 原文未提供公开数据集链接 | 早期 UML 需求到设计综合的说明性流程 |
| 22 | [paper](./tech-report-neural-language-models-few-shot-mdse/DESC.md) | 🟠 | 开源汽车需求集 | 开源需求语料 | 在汽车需求语料上做 few-shot requirements-to-DSL 翻译 | 非正式汽车需求 | Requirement DSL | 原文首页未明确 | 🟠 | 原文首页未给出统一下载链接 | 面向 MDSE 的需求结构化语料与翻译实验 |
| 23 | [paper](./spec2control/DESC.md) | 🟠 | 开放 control narratives 测试集 | 开放数据集 | 10 份 control narratives + 65 个复杂测试用例，用于评估控制逻辑自动生成 | 自然语言 control narratives | 图形化控制逻辑 | 10 narratives + 65 tests | 🟠 | PDF 首页未给出明确下载入口 | 工业控制 narrative 与测试用例集合 |
| 24 | [paper](./specification-based-prototyping-for-embedded-systems/DESC.md) | 🟡 | Nimbus/RSML-e 原型化案例 | 方法与环境示例 | 以形式化规格驱动可执行原型与状态机 refinement | 形式化需求规格 | 可执行层次状态机原型 | 原文未明确 | 🟠 | 原文未提供公开数据集链接 | 规格即原型的嵌入式系统案例脉络 |
| 25 | [paper](./nimbus-tool-for-specification-centered-development/DESC.md) | 🟠 | 无独立 benchmark | 工具环境说明 | 围绕 RSML-e 规格提供分析、执行、代码生成与测试支持 | RSML-e 规格 | 分析/执行/代码测试工件 | 不适用 | 🟠 | 不适用 | 规格中心开发工具链说明 |
| 26 | [paper](./requirements-capture-and-evaluation-in-nimbus-light-control/DESC.md) | 🟢 | Light Control System case study | 参考案例 | 用 RSML-e 与 Nimbus 捕获、执行并评估灯光控制需求 | 灯光控制需求 | RSML-e 状态化需求模型 | 1 个案例 | 🟢 | 论文正文即给出案例与建模过程 | 经典灯光控制状态化需求建模案例 |
| 27 | [paper](./requirements-specification-for-process-control-systems/DESC.md) | 🟢 | TCAS II 案例 | 工业航空案例 | 用面向过程控制的规格语言把需求写成形式化状态模型 | 过程控制系统需求 | 形式化状态化需求规格 | 1 个案例 | 🟠 | 原文未提供独立案例下载页 | TCAS II 需求规格化与状态建模案例 |
| 28 | [paper](./software-requirements-analysis-for-real-time-process-control/DESC.md) | 🟠 | 无独立 benchmark | 理论分析 | 基于抽象状态机模型定义需求语义分析准则 | 状态机式需求规格 | 分析准则 | 不适用 | 🟠 | 不适用 | 面向实时过程控制需求规格的分析框架 |
| 29 | [paper](./automatic-debugging-support-for-uml-designs/DESC.md) | 🟡 | UML 需求/设计示例 | 算法示例 | 从 annotated sequence diagrams 综合 structured statecharts 并回查冲突 | Annotated sequence diagrams | Structured statecharts | 原文未明确 | 🟠 | 原文未提供公开数据集链接 | 场景需求到状态图再到冲突调试的示例链路 |
| 30 | [paper](./integrating-inter-object-scenarios-with-intra-object-statecharts/DESC.md) | 🟡 | 无统一 benchmark | 环境/语义说明 | 将 LSC 场景规格和 Statecharts 做联合执行集成 | LSC 场景规格 | LSC + Statecharts 联合模型 | 不适用 | 🟠 | 原文未提供公开数据集链接 | 需求场景与状态图集成开发环境 |
| 31 | [paper](./formal-requirements-elicitation-with-fret/DESC.md) | 🟠 | NASA / LMCPS 案例需求 | 工业/航空案例 | 在 FRET 中用 FRETish 写需求并自动得到时序逻辑与解释 | FRETish 需求 | FRETish + 时序逻辑 | 原文首页未明确 | 🟠 | [FRET GitHub](https://github.com/NASA-SW-VnV/fret) | 受限自然语言需求形式化与分析案例 |

## 初步归类与覆盖盘点

### 类别分布

| 类别 | 篇数 | 说明 |
|---|---:|---|
| 直接状态机建模 | 8 | 直接从自然语言、结构化需求或控制系统需求得到状态机/状态化规格的核心基线 |
| 补全/精化/扩展/集成 | 8 | 围绕已有模型、场景或形式化需求做状态机补全、扩展、调试、执行化或双层集成 |
| 需求形式化/分析/状态抽取 | 5 | 需求 DSL、时序逻辑、状态抽取与需求语义分析等前置/支撑方法 |
| 邻近建模与控制逻辑 | 10 | 非状态机输出的 UML/goal/domain/control-logic 邻近工作与多模态/代码生成参照 |

### BASELINE评估分布

| 评估 | 篇数 | 说明 |
|---|---:|---|
| 🟢 | 8 | 可与“需求/描述到状态机或等价状态化规格”直接对比的核心 baseline，其中包含 5 篇 LLM 直接工作和 3 篇经典前身工作 |
| 🟡 | 8 | 仍围绕状态机补全、扩展、调试、执行化或场景-状态机集成，但不是纯自然语言直接建模 |
| 🟠 | 15 | 邻近建模、需求形式化、状态抽取、控制逻辑生成、FSM代码生成或经验评估工作，可借鉴但不可直接公平对比 |
| ⚪ | 0 | 当前正式收录中暂无仅作背景资料的论文 |

### 当前最有价值的整体观察

1. 真正直接做“自然语言到状态机模型”的**LLM** 论文仍然不多，直接 LLM baseline 依旧集中在 `llms_emp`、`fsm-gen-iec-61499`、`req`、`umple` 和 `ttool-ai` 五篇。
2. 本轮新增最有价值的补充不是更多 LLM 直出状态机论文，而是 1990s-2020s 间一条很清晰的经典前身线：`Requirements Specification for Process-Control Systems`、`Requirements Capture and Evaluation in Nimbus`、`Executable State Machines Derived...` 等。
3. 这条经典线说明：控制系统/安全关键系统里，“需求 -> 状态化规格/状态机/可执行模型”并不是新问题，真正稀缺的是把这条链现代化为 LLM 驱动、低门槛、可验证的自动建模流程。
4. 很多新增论文虽然不能评为 `🟢`，但在前处理和后处理层面极有价值，例如状态抽取（`Extraction of System States...`）、DSL/LTL 形式化（`Technical Report...`、`FRET`）、状态机调试回写（`Automatic Debugging Support...`）和规格执行化（`Specification-based Prototyping...`）。
5. `Spec2Control` 这类新近工业 LLM 工作说明：控制系统自然语言到图形化工件已经开始落地，但主流落点仍是 PLC/DCS control logic，而不是状态机。
6. `requirements-to-uml-sequence-diagrams`、`from-image-to-uml`、`gpt4-goal-models` 等工作继续提供重要边界证据：输入形式虽然接近，但只要输出不是状态机族模型，就不能混入直接 baseline。
7. 新增经典控制规格论文也为本课题后续“生成-验证-修复”闭环提供了现成约束源，可用于提炼状态、守卫、模式切换和鲁棒性检查规则。

## 待补充高优先级候选

以下候选已在 `project_1` 根目录历史工作文档中出现，后续若正式收录，应优先进入本论文集：

| 优先级 | 标题 | 来源文档 | 当前价值 |
|---|---|---|---|
| 中 | 当前暂无比现有 16 篇更高优先级的新增状态机候选 | - | 后续应优先继续检索真正输出状态机/Statechart/SysML 状态机的论文，而不是扩张到顺序图、goal model 或一般 UML 建模 |

## 更新日志

| 时间 | 更新内容 | 说明 |
|---|---|---|
| 2026-03-12 | 新增 15 篇更贴近任务定义的 baseline/经典前身/邻近支撑论文 | 本轮补入 `completion-of-sysml-state-machines-from-gwt-requirements`、`enhancing-model-based-development-formalized-requirements`、`extraction-of-system-states-from-natural-language-requirements`、`executable-state-machines-derived-from-structured-textual-requirements`、`automatic-synthesis-of-uml-designs-from-requirements`、`tech-report-neural-language-models-few-shot-mdse`、`spec2control`、`specification-based-prototyping-for-embedded-systems`、`nimbus-tool-for-specification-centered-development`、`requirements-capture-and-evaluation-in-nimbus-light-control`、`requirements-specification-for-process-control-systems`、`software-requirements-analysis-for-real-time-process-control`、`automatic-debugging-support-for-uml-designs`、`integrating-inter-object-scenarios-with-intra-object-statecharts`、`formal-requirements-elicitation-with-fret`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 | 新增 5 篇 baseline 并补齐单篇分析 | 新增 `chatgpt-uml-assessment`、`requirements-to-uml-sequence-diagrams`、`from-image-to-uml`、`few-shot-model-completion`、`gpt4-goal-models`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 | 建立 `baselines/` 四件套并统一命名 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)，并将全部 `desc.md` 更名为 `DESC.md` |
| 2026-03-12 | 补充 BASELINE 评估、输入输出方法字段和数据集总表 | 将论文清单改为固定字段表，并新增“数据集与 Benchmark 清单” |
| 2026-03-12 | 细化数据集可获取性口径与链接写法 | 为数据集表新增 `🟢/🟡/🟠/🔒` 口径，并将已确认的公开地址统一改为 Markdown 链接 |
