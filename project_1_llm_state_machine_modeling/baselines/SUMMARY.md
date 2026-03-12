# Project 1 Baselines Summary

本文件是 `project_1_llm_state_machine_modeling/baselines/` 的总账，用于记录当前已经正式入账的 baseline 论文、统一比较口径、数据集与 benchmark 盘点、待补充候选与更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 再使用本文件查看统计、论文清单、数据集盘点和待补充候选。
4. 若需要重写某篇单论文分析，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。

## 当前收录统计

- 已收录 baseline 论文：**16** 篇
- 本轮新增论文：**5** 篇
- 已完成 `DESC.md`：**16** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮规范化工作：新增 5 篇 baseline 论文目录并补齐 `paper.pdf / paper_content.txt / bibtex.bib / DESC.md`

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

### 已观察到的高命中特征

- 题名同时出现 `LLM` 与 `state machine/statechart/FSM/SysML behavior`
- 明确写出输入输出链路，如 `requirements -> statechart`、`diagram -> code/test`
- `partial model -> completion/repair` 且对象明确是状态机时，命中率更稳定
- 出现 `iterative`、`refinement`、`feedback`、`few-shot`、`RAG` 等方法词
- 安全关键或工业领域关键词常能带来更贴近 `project_1` 的论文

### 已观察到的低命中特征

- `FSM` 仅用于提示范式、规划器、对话流或智能体编排
- 纯机器人执行流程、纯协议推理、纯智能合约生成但无建模工件
- 输出是顺序图、类图、goal model、一般 domain model 的论文默认不是本 collection 的主线
- 纯教学经验、课堂问卷或学习体验类 UML 论文通常弱于“真正生成模型”的论文
- 纯综述、纯经验报告，缺少明确方法与实验对比

### 检索倾向调整

- 优先补“直接生成状态机模型”和“带反馈闭环的状态机精化/修复”两类工作
- 泛 UML/SysML 论文仅在其方法明确输出状态机时保留
- 多模态图样识别和自动 benchmark 构建可保留，但需在 `DESC.md` 中明确说明其“邻近 baseline”性质
- 非状态机输出论文原则上不再继续扩张收录，只在少量必要场合作为弱相关参照保留

## 论文清单

| # | 评估 | 类别 | 标题 | 年份 | 输入 | 输出 | 输出模型类型 | 使用的LLM | 主要方法 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | 🟢 | 直接生成 | Generating SysML Behavior Models via Large Language Models: an Empirical Study | 2025 | 自然语言需求描述 | PlantUML 格式行为模型 | SysML STM / ACT / SD | GPT-4、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 | 两阶段框架：提示生成 + 模型检查反馈修复 | [paper](./llms_emp/) |
| 2 | 🟢 | 直接生成 | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | 自然语言控制需求 + I/O 接口规范 | 可视化 FSM + IEC 61499 功能块代码 | FSM | 未明确指定 | 自然语言到 FSM 的迭代精化，并接入仿真和代码生成 | [paper](./fsm-gen-iec-61499/) |
| 3 | 🟢 | 直接生成 | Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering | 2025 | 自然语言产品功能需求 | Mermaid.js 状态机 | Statechart | GPT-3.5、GPT-4、GPT-4o（微调） | NLP 特征提取 + 合成数据扩充 + 领域微调生成状态机 | [paper](./req/) |
| 4 | 🟢 | 直接生成 | Exploring How Well Llama3 can Generate State Machines Represented in Umple | 2025 | 自然语言需求描述 | Umple 状态机代码 | Umple 状态机 | Llama 3 (8B) | 比较 Zero-shot、One-shot 与 RAG 三种提示策略 | [paper](./umple/) |
| 5 | 🟢 | 直接生成 | System Architects Are not Alone Anymore: Automatic System Modeling with AI | 2024 | 自然语言系统规范 | SysML 块图、内部块图和状态机图 | 含状态机的 SysML 联合模型 | GPT-4 | 知识注入 + 自动反馈循环 + TTool 工具链集成 | [paper](./ttool-ai/) |
| 6 | 🟠 | FSM代码生成 | Enhancing Finite State Machine Design Automation with Large Language Models and Prompt Engineering Techniques | 2024 | HDLBits FSM 设计问题描述 | SystemVerilog FSM 代码 | FSM 代码工件 | Claude 3 Opus、GPT-4、GPT-4o | Markdown 提示模板 + TOP Patch + CoT 多轮对话 | [paper](./enhance/) |
| 7 | 🟠 | FSM代码生成 | LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation | 2026 | FSM 配置参数 + 自然语言规范 | Verilog RTL 代码 + 测试平台 | RTL / 测试工件 | GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro 等 | 自动构建 FSM-to-RTL benchmark 并系统评估有限状态推理 | [paper](./LLM-FSM/) |
| 8 | 🟡 | 精化/修复 | LLM-based iterative refinement of finite-state machines with STPA controller constraints and generation of IEC 61499 code | 2025 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | FSM | OpenAI GPT（通过 fbAssistant） | 用 STPA 约束驱动递归迭代精化 | [paper](./STPA/) |
| 9 | 🟡 | 精化/扩展 | State Diagram Extension and Test Case Generation Based on Large Language Models for Improving Test Engineers’ Efficiency in Safety Testing | 2024 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | State Diagram | Qwen2-72B-Instruct（微调） | 安全准则提取 + 状态图扩展 + 测试路径/数据生成 | [paper](./safety/) |
| 10 | 🟠 | 泛建模 | Multi-step Iterative Automated Domain Modeling with Large Language Models | 2024 | 自然语言问题描述 / 领域描述文本 | 领域模型 | UML 类图 / 领域模型 | GPT-4 | 多步任务分解 + few-shot + 迭代优化 | [paper](./MIG/) |
| 11 | 🟡 | 多模态邻近 | Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition | 2025 | 状态图图像（来自工业规范 PDF） | 状态机表示 + C++ 代码 + 测试 | 图像状态图 / 可机读状态机表示 | gpt-4o、claude-3-sonnet、Llama-3.2-11b | 图像裁剪 + LLM 识别 + 模板化代码/测试生成 | [paper](./I4.0/) |
| 12 | 🟠 | 泛建模经验 | On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML | 2023 | 自然语言建模任务描述 + 修正提示 | UML 类图 + OCL 约束 | UML 类图 / OCL | ChatGPT | 经验性对话实验，系统评估 UML/OCL 建模能力与缺陷模式 | [paper](./chatgpt-uml-assessment/) |
| 13 | 🟠 | 邻近行为建模 | Model Generation with LLMs: From Requirements to UML Sequence Diagrams | 2024 | 自然语言需求文档 | UML sequence diagram | UML 顺序图 | ChatGPT | 从真实需求文档直接生成顺序图，并做问题主题分析 | [paper](./requirements-to-uml-sequence-diagrams/) |
| 14 | 🟠 | 多模态邻近 | From Image to UML: First Results of Image-Based UML Diagram Generation Using LLMs | 2024 | UML 类图图像 / 手绘图 | PlantUML 类图代码 | UML 类图 | GPT-4V、Gemini Pro、Gemini Ultra、CogVLM | 多模态图像识别到 PlantUML 的重复实验比较 | [paper](./from-image-to-uml/) |
| 15 | 🟠 | 泛建模补全 | Towards using Few-Shot Prompt Learning for Automating Model Completion | 2023 | 部分 UML 类图 / 活动图 | 类、属性、关联名与活动流补全建议 | UML 类图 / 活动图 | GPT-3 (`text-davinci-002`) | 将模型补全转写为 few-shot prompt learning 任务 | [paper](./few-shot-model-completion/) |
| 16 | 🟠 | 泛建模 | On the Use of GPT-4 for Creating Goal Models: An Exploratory Study | 2023 | 领域描述 + TGRL 语法提示 | GRL/TGRL 目标模型 | Goal model | GPT-4 | 多 prompt、多次运行与结果聚合的目标建模探索 | [paper](./gpt4-goal-models/) |

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
3. `论文` 列统一使用 `[paper](./subdir/)` 形式的跳转链接，不再显示子目录名。

| # | 论文 | 评估 | 数据集/Benchmark | 来源类型 | 制作方法 | 输入 | 输出 | 规模 | 可获取性 | 获取方式/链接 | 简述来源 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [paper](./llms_emp/) | 🟢 | G_Model SysML 行为模型数据集 | 自己搜集制作 | 从 Google Scholar、CNKI、GitHub 搜集 303 个来源，经筛选后统一重建为 PlantUML + 需求描述并交叉验证 | 自然语言需求描述 | SysML 行为模型（ACT/STM/SD） | 107 个行为模型（36 ACT / 36 STM / 35 SD） | 🟢 | [Google Drive 数据集](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 从学术文献、教材和开源项目中系统重建的公开行为模型集 |
| 2 | [paper](./fsm-gen-iec-61499/) | 🟢 | fbAssistant 工业案例集 | 自己制作 | 基于工业自动化实践和 IEC 61499 标准设计 2 个案例系统，并配套 I/O 接口和需求规格 | 自然语言控制需求 + I/O 规格 | FSM + IEC 61499 功能块代码 | 2 个案例系统 | 🟠 | 原文未提供公开数据集/代码链接；仅公开了 [工具演示视频](https://www.youtube.com/live/aR20KBmZnA4?si=wxyMOcAX4tirRgQf) | 基于作者团队长期工业自动化研究积累设计的典型控制系统案例 |
| 3 | [paper](./req/) | 🟢 | Volvo Cars 需求数据 + 合成扩充数据 | 工业专有数据 | 使用 Volvo Cars 内部 Car Weaver 的 20 个真实需求，并通过受控随机化生成合成训练数据 | 自然语言产品功能需求 | Mermaid 状态机 | 20 个真实需求 + 合成扩充数据；12 个测试用例 | 🔒 | 原文未提供公开下载链接 | 来自汽车工业内部需求管理工具的真实产品功能需求 |
| 4 | [paper](./umple/) | 🟢 | 5 个 Umple 测试系统 | 自己设计制作 | 作者设计 5 个测试系统，包含需求描述和参考状态机，其中 Course Section 来自 Umple 文档 | 自然语言需求描述 | Umple 状态机代码 | 5 个系统 | 🟠 | 论文正文给出需求与参考示例，但无独立下载页 | 基于 Umple 建模语言特点设计的小规模测试集 |
| 5 | [paper](./ttool-ai/) | 🟢 | 3 个真实系统规范案例 | 使用现成规范 | 使用 3 个欧洲项目真实系统规范做工具与人工对照实验，并公开规范、模型和结果 | 自然语言系统规范 | SysML 块图、内部块图、状态机 | 3 个系统 | 🟢 | [GitHub 实验工件](https://github.com/zebradile/ttool-ai) | 来自真实欧洲安全关键系统项目的公开实验工件 |
| 6 | [paper](./enhance/) | 🟠 | HDLBits FSM 设计问题集 | 使用现成数据集 | 直接使用 HDLBits 在线平台中的 FSM 设计问题作为测试集 | FSM 设计问题描述 | SystemVerilog FSM 代码 | 20 个 FSM 设计问题 | 🟢 | [HDLBits FSM 题库](https://hdlbits.01xz.net/) | 公开硬件设计教育平台的 FSM 练习题 |
| 7 | [paper](./LLM-FSM/) | 🟠 | LLM-FSM benchmark | 自动化生成 | 约束随机 FSM 生成 + LLM 生成 YAML 与自然语言规范 + 正确性构造 RTL/testbench + 多层验证 | FSM 配置参数 + 自然语言规范 | RTL 代码 + 测试平台 | 1000 个 FSM-to-RTL 问题（状态 2-16） | 🟠 | 论文公开，但 benchmark 文件未给出明确下载链接 | 通过自动化 pipeline 生成的大规模 FSM 推理 benchmark |
| 8 | [paper](./STPA/) | 🟡 | Pick-and-Place + STPA 约束实验集 | 自己制作 | 对 pick-and-place 机器做 STPA 分析，生成 UCA 与控制器约束，再做多轮迭代实验 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | 9 个约束 × 20 次迭代 + 1 组组合约束 × 10 次迭代 = 190 次迭代 | 🟡 | 原文未提供公开下载链接；当前可行路径更接近联系作者获取 STPA 结果与实验记录 | 基于单个工业案例和手工 STPA 分析构建的精化实验集 |
| 9 | [paper](./safety/) | 🟡 | 航空高度控制安全测试案例 | 自己制作 + 在线收集 | 使用航空高度控制系统案例，并从 DO-178C、ARP4754A 提取 4 类 25 项安全准则，结合在线爬取需求做实验 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | 单个航空案例 + 25 项安全准则 | 🟡 | 原文未提供公开下载链接，文意上更接近联系作者团队获取 | 面向航空安全测试的状态图扩展与测试生成案例 |
| 10 | [paper](./MIG/) | 🟠 | 公开领域建模数据集（原文未明确命名） | 公开数据集（细节未明确） | 原文说明使用公开领域建模数据集和人工标注参考模型，但未细述构造流程 | 自然语言问题描述 / 领域描述文本 | 领域模型 | 原文未明确 | 🟠 | 原文未提供公开下载链接 | 用于评估多步领域建模效果的公开类图/领域模型数据 |
| 11 | [paper](./I4.0/) | 🟡 | PROFINET / OPC UA 状态图识别数据 | 使用现成规范并人工裁剪 | 从 IEC 61158 和 IEC 62541 规范 PDF 中手工裁剪状态图，并对公开版本做文本打乱处理 | 状态图图像 | 可机读状态机表示 + 代码/测试 | PROFINET 80 个状态图 + OPC UA 15 个状态图 | 🔒 | [Zenodo 实现与处理结果](https://zenodo.org/records/14730727)；原始标准文档需购买 | 来自工业通信协议规范文档的状态图图像数据 |
| 12 | [paper](./chatgpt-uml-assessment/) | 🟠 | ChatGPT-UML 练习与实验记录 | 自己制作 | 作者围绕 UML 类图与 OCL 准备 40 个练习，并记录对话实验与报告 | 自然语言建模任务描述 | UML 类图 + OCL | 40 个练习，8 个代表性模型做深入实验 | 🟢 | [GitHub 仓库](https://github.com/atenearesearchgroup/chatgpt-uml) | 面向 ChatGPT 建模能力评估的公开实验工件 |
| 13 | [paper](./requirements-to-uml-sequence-diagrams/) | 🟠 | 28 份需求文档评估集 | 混合公开/工业数据 | 从 Lockheed Martin 挑战集、PURE 和 user story 数据中筛出 28 份真实需求文档，并附评估日志 | 自然语言需求文档 | UML sequence diagram | 28 份文档，18 个领域 | 🟢 | [Zenodo replication package](https://doi.org/10.5281/zenodo.10579731) | 面向需求到顺序图生成的真实需求评估集 |
| 14 | [paper](./from-image-to-uml/) | 🟠 | IMG2UML examples | 自己制作 + 开源示例 | 准备 4 张 UML 类图图像，比较 4 个视觉 LLM 在不同 prompts 下的转写效果 | UML 类图图像 | PlantUML 类图代码 | 4 个图像样例 × 3 prompts × 3 runs | 🟢 | [IMG2UML-Examples](https://github.com/BESSER-PEARL/IMG2UML-Examples) | 面向图像到 UML 转写的开放示例集 |
| 15 | [paper](./few-shot-model-completion/) | 🟠 | ModelSet + activity diagram examples | 使用现成数据集 | 从 ModelSet 中选取 30 个领域模型做类名补全，并基于公开活动图示例展示动态图补全 | 部分 UML 类图 / 活动图 | 模型补全建议 | 30 个领域模型；212 个类；40 对关联名 | 🟢 | [GitHub 仓库](https://github.com/meriembenchaaben/model-completion) | 面向模型补全的 few-shot prompting 实验工件 |
| 16 | [paper](./gpt4-goal-models/) | 🟠 | GRL_GPT prompts 与评分结果 | 自己制作 | 整理 18 个 goal-modeling 问题和 2 个案例的 prompts、评分结果与实验记录 | 领域描述 + TGRL 提示 | GRL/TGRL 目标模型 | 18 个问题 + 2 个案例 | 🟢 | [GitHub 仓库](https://github.com/ChenKua/GRL_GPT) | 面向 GPT-4 目标建模评估的开放实验记录 |

## 初步归类与覆盖盘点

### 类别分布

| 类别 | 篇数 | 说明 |
|---|---:|---|
| 直接生成 | 5 | 直接从自然语言或系统规格生成状态机、状态图或 SysML 状态机等核心工件 |
| 精化/修复/扩展 | 2 | 从已有 FSM/状态图出发做约束注入、扩展或修复 |
| FSM代码生成 | 2 | 围绕有限状态机问题生成 RTL / HDL 代码，但输出不是状态机模型 |
| 泛建模/邻近 baseline | 5 | 结构建模、目标建模、UML 建模经验评估与非状态机补全等支撑项 |
| 多模态邻近 | 2 | 图像状态图或 UML 图像识别到机读模型/代码的邻近工作 |
| 邻近行为建模 | 1 | 输出是行为图但不是状态机，保留作弱相关参照 |

### BASELINE评估分布

| 评估 | 篇数 | 说明 |
|---|---:|---|
| 🟢 | 5 | 可与“自然语言自动生成状态机模型”直接对比的核心 baseline |
| 🟡 | 3 | 仍围绕状态机精化、扩展或识别，但不属于纯自然语言直接建模 |
| 🟠 | 8 | 邻近建模、多模态识别、FSM代码生成、非状态机行为建模或经验评估工作，可借鉴但不可直接公平对比 |
| ⚪ | 0 | 当前正式收录中暂无仅作背景资料的论文 |

### 当前最有价值的整体观察

1. 真正直接做“自然语言到状态机模型”的论文仍然不多，当前直接 baseline 仍集中在 5 篇核心论文。
2. 直接可比 baseline 主要集中在 `llms_emp`、`fsm-gen-iec-61499`、`req`、`umple` 和 `ttool-ai`。
3. 真正仍可评为 `🟡` 的，只剩 `STPA`、`safety` 和 `I4.0` 这三类明确围绕状态机本体的精化、扩展或识别工作。
4. `requirements-to-uml-sequence-diagrams` 虽然输入也是自然语言需求，但输出是顺序图而非状态机，因此只能作为弱相关邻近证据，不能算直接 baseline。
5. `enhance` 与 `LLM-FSM` 虽然都围绕 FSM，但输出是 HDL/RTL 代码与推理 benchmark，因此按新标准都应降为 `🟠`，不能再算状态机 baseline。
6. `chatgpt-uml-assessment`、`few-shot-model-completion` 与 `gpt4-goal-models` 提供了重要负面和中性证据：通用 LLM 有建模潜力，但若输出不是状态机族模型，就只能作为弱相关参照。
7. 多模态方向中 `I4.0` 仍保留为 `🟡`，因为它能恢复可机读状态机；而 `from-image-to-uml` 只到类图，因此仅是 `🟠`。

## 待补充高优先级候选

以下候选已在 `project_1` 根目录历史工作文档中出现，后续若正式收录，应优先进入本论文集：

| 优先级 | 标题 | 来源文档 | 当前价值 |
|---|---|---|---|
| 中 | 当前暂无比现有 16 篇更高优先级的新增状态机候选 | - | 后续应优先继续检索真正输出状态机/Statechart/SysML 状态机的论文，而不是扩张到顺序图、goal model 或一般 UML 建模 |

## 更新日志

| 时间 | 更新内容 | 说明 |
|---|---|---|
| 2026-03-12 | 新增 5 篇 baseline 并补齐单篇分析 | 新增 `chatgpt-uml-assessment`、`requirements-to-uml-sequence-diagrams`、`from-image-to-uml`、`few-shot-model-completion`、`gpt4-goal-models`，均已补齐 PDF、文本、BibTeX 与 `DESC.md` |
| 2026-03-12 | 建立 `baselines/` 四件套并统一命名 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)，并将全部 `desc.md` 更名为 `DESC.md` |
| 2026-03-12 | 补充 BASELINE 评估、输入输出方法字段和数据集总表 | 将论文清单改为固定字段表，并新增“数据集与 Benchmark 清单” |
| 2026-03-12 | 细化数据集可获取性口径与链接写法 | 为数据集表新增 `🟢/🟡/🟠/🔒` 口径，并将已确认的公开地址统一改为 Markdown 链接 |
