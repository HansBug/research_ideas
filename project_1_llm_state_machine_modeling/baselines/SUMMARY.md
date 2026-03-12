# Project 1 Baselines Summary

本文件是 `project_1_llm_state_machine_modeling/baselines/` 的总账，用于记录当前已经正式入账的 baseline 论文、统一比较口径、数据集与 benchmark 盘点、待补充候选与更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 再使用本文件查看统计、论文清单、数据集盘点和待补充候选。
4. 若需要重写某篇单论文分析，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。

## 当前收录统计

- 已收录 baseline 论文：**11** 篇
- 本轮新增论文：**0** 篇
- 已完成 `DESC.md`：**11** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮规范化工作：新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)，并将全部单篇分析统一更名为 `DESC.md`

## BASELINE评估口径

| Emoji | 含义 |
|---|---|
| 🟢 | 直接构成 baseline：输入是自然语言系统设计/描述/需求，输出是状态机/Statechart/SysML 行为模型或高度等价工件，与本研究直接可比 |
| 🟡 | 相关但非直接 baseline：与状态机生成/精化/扩展密切相关，但输入不是纯自然语言，或任务更偏精化、扩展、多模态识别、测试生成 |
| 🟠 | 弱相关/可比性有限：与有限状态推理或泛 UML/SysML 建模相关，但不构成公平直接对比 |
| ⚪ | 背景资料：只适合当背景文献或补充相关工作，不建议作为 baseline 对照 |

## 检索关键词簇

### 当前推荐关键词簇

- `LLM/GPT/Claude/Gemini` + `state machine/statechart/state diagram/FSM`
- `LLM` + `SysML/UML/behavior model/domain model`
- `requirements` + `statechart/state machine` + `automotive/industrial/control`
- `iterative refinement/model repair/model completion/test generation` + `FSM/UML`
- `diagram recognition/vision-language/multimodal` + `state diagram/FSM`

### 已观察到的高命中特征

- 题名同时出现 `LLM` 与 `state machine/statechart/FSM/SysML behavior`
- 明确写出输入输出链路，如 `requirements -> statechart`、`diagram -> code/test`
- 出现 `iterative`、`refinement`、`feedback`、`few-shot`、`RAG` 等方法词
- 安全关键或工业领域关键词常能带来更贴近 `project_1` 的论文

### 已观察到的低命中特征

- `FSM` 仅用于提示范式、规划器、对话流或智能体编排
- 纯机器人执行流程、纯协议推理、纯智能合约生成但无建模工件
- 纯综述、纯经验报告，缺少明确方法与实验对比

### 检索倾向调整

- 优先补“直接生成状态机/行为模型”和“带反馈闭环的精化/修复”两类工作
- 泛 UML/SysML 论文仅在其方法确实能支撑 `project_1` 比较维度时保留
- 多模态图样识别和自动 benchmark 构建可保留，但需在 `DESC.md` 中明确说明其“邻近 baseline”性质

## 论文清单

| # | 评估 | 类别 | 标题 | 年份 | 输入 | 输出 | 输出模型类型 | 使用的LLM | 主要方法 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | 🟢 | 直接生成 | Generating SysML Behavior Models via Large Language Models: an Empirical Study | 2025 | 自然语言需求描述 | PlantUML 格式行为模型 | SysML STM / ACT / SD | GPT-4、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 | 两阶段框架：提示生成 + 模型检查反馈修复 | [llms_emp](./llms_emp/) |
| 2 | 🟢 | 直接生成 | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | 自然语言控制需求 + I/O 接口规范 | 可视化 FSM + IEC 61499 功能块代码 | FSM | 未明确指定 | 自然语言到 FSM 的迭代精化，并接入仿真和代码生成 | [fsm-gen-iec-61499](./fsm-gen-iec-61499/) |
| 3 | 🟢 | 直接生成 | Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering | 2025 | 自然语言产品功能需求 | Mermaid.js 状态机 | Statechart | GPT-3.5、GPT-4、GPT-4o（微调） | NLP 特征提取 + 合成数据扩充 + 领域微调生成状态机 | [req](./req/) |
| 4 | 🟢 | 直接生成 | Exploring How Well Llama3 can Generate State Machines Represented in Umple | 2025 | 自然语言需求描述 | Umple 状态机代码 | Umple 状态机 | Llama 3 (8B) | 比较 Zero-shot、One-shot 与 RAG 三种提示策略 | [umple](./umple/) |
| 5 | 🟢 | 直接生成 | System Architects Are not Alone Anymore: Automatic System Modeling with AI | 2024 | 自然语言系统规范 | SysML 块图、内部块图和状态机图 | SysML 结构/行为模型 | GPT-4 | 知识注入 + 自动反馈循环 + TTool 工具链集成 | [ttool-ai](./ttool-ai/) |
| 6 | 🟡 | 相关非直接 | Enhancing Finite State Machine Design Automation with Large Language Models and Prompt Engineering Techniques | 2024 | HDLBits FSM 设计问题描述 | SystemVerilog FSM 代码 | FSM 代码工件 | Claude 3 Opus、GPT-4、GPT-4o | Markdown 提示模板 + TOP Patch + CoT 多轮对话 | [enhance](./enhance/) |
| 7 | 🟠 | 弱相关 | LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation | 2026 | FSM 配置参数 + 自然语言规范 | Verilog RTL 代码 + 测试平台 | RTL / 测试工件 | GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro 等 | 自动构建 FSM-to-RTL benchmark 并系统评估有限状态推理 | [LLM-FSM](./LLM-FSM/) |
| 8 | 🟡 | 精化/修复 | LLM-based iterative refinement of finite-state machines with STPA controller constraints and generation of IEC 61499 code | 2025 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | FSM | OpenAI GPT（通过 fbAssistant） | 用 STPA 约束驱动递归迭代精化 | [STPA](./STPA/) |
| 9 | 🟡 | 精化/扩展 | State Diagram Extension and Test Case Generation Based on Large Language Models for Improving Test Engineers’ Efficiency in Safety Testing | 2024 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | State Diagram | Qwen2-72B-Instruct（微调） | 安全准则提取 + 状态图扩展 + 测试路径/数据生成 | [safety](./safety/) |
| 10 | 🟠 | 泛建模 | Multi-step Iterative Automated Domain Modeling with Large Language Models | 2024 | 自然语言问题描述 / 领域描述文本 | 领域模型 | UML 类图 / 领域模型 | GPT-4 | 多步任务分解 + few-shot + 迭代优化 | [MIG](./MIG/) |
| 11 | 🟡 | 多模态邻近 | Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition | 2025 | 状态图图像（来自工业规范 PDF） | 状态机表示 + C++ 代码 + 测试 | 图像状态图 / 可机读状态机表示 | gpt-4o、claude-3-sonnet、Llama-3.2-11b | 图像裁剪 + LLM 识别 + 模板化代码/测试生成 | [I4.0](./I4.0/) |

## 数据集与 Benchmark 清单

### 数据集可获取性口径

| Emoji | 含义 |
|---|---|
| 🟢 | 可直接获取：论文给出了可直接下载、浏览或通过清晰公开渠道直接取得完整内容的链接/入口 |
| 🟡 | 需联系申请：论文明确说明需要向作者团队、项目方或维护方申请后才能获取 |
| 🟠 | 信息不清：论文只提到制作方式、来源或使用过该数据，但未给出足够清晰的获取路径 |
| 🔒 | 难以取得：数据依赖企业/团队内部资料、付费标准、受限工业资产或其他现实上很难取得的来源 |

| # | 论文 | 评估 | 数据集/Benchmark | 来源类型 | 制作方法 | 输入 | 输出 | 规模 | 可获取性 | 获取方式/链接 | 简述来源 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | llms_emp | 🟢 | G_Model SysML 行为模型数据集 | 自己搜集制作 | 从 Google Scholar、CNKI、GitHub 搜集 303 个来源，经筛选后统一重建为 PlantUML + 需求描述并交叉验证 | 自然语言需求描述 | SysML 行为模型（ACT/STM/SD） | 107 个行为模型（36 ACT / 36 STM / 35 SD） | 🟢 | [Google Drive 数据集](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 从学术文献、教材和开源项目中系统重建的公开行为模型集 |
| 2 | fsm-gen-iec-61499 | 🟢 | fbAssistant 工业案例集 | 自己制作 | 基于工业自动化实践和 IEC 61499 标准设计 2 个案例系统，并配套 I/O 接口和需求规格 | 自然语言控制需求 + I/O 规格 | FSM + IEC 61499 功能块代码 | 2 个案例系统 | 🟠 | 原文未提供公开数据集/代码链接；仅公开了 [工具演示视频](https://www.youtube.com/live/aR20KBmZnA4?si=wxyMOcAX4tirRgQf) | 基于作者团队长期工业自动化研究积累设计的典型控制系统案例 |
| 3 | req | 🟢 | Volvo Cars 需求数据 + 合成扩充数据 | 工业专有数据 | 使用 Volvo Cars 内部 Car Weaver 的 20 个真实需求，并通过受控随机化生成合成训练数据 | 自然语言产品功能需求 | Mermaid 状态机 | 20 个真实需求 + 合成扩充数据；12 个测试用例 | 🔒 | 原文未提供公开下载链接 | 来自汽车工业内部需求管理工具的真实产品功能需求 |
| 4 | umple | 🟢 | 5 个 Umple 测试系统 | 自己设计制作 | 作者设计 5 个测试系统，包含需求描述和参考状态机，其中 Course Section 来自 Umple 文档 | 自然语言需求描述 | Umple 状态机代码 | 5 个系统 | 🟠 | 论文正文给出需求与参考示例，但无独立下载页 | 基于 Umple 建模语言特点设计的小规模测试集 |
| 5 | ttool-ai | 🟢 | 3 个真实系统规范案例 | 使用现成规范 | 使用 3 个欧洲项目真实系统规范做工具与人工对照实验，并公开规范、模型和结果 | 自然语言系统规范 | SysML 块图、内部块图、状态机 | 3 个系统 | 🟢 | [GitHub 实验工件](https://github.com/zebradile/ttool-ai) | 来自真实欧洲安全关键系统项目的公开实验工件 |
| 6 | enhance | 🟡 | HDLBits FSM 设计问题集 | 使用现成数据集 | 直接使用 HDLBits 在线平台中的 FSM 设计问题作为测试集 | FSM 设计问题描述 | SystemVerilog FSM 代码 | 20 个 FSM 设计问题 | 🟢 | [HDLBits FSM 题库](https://hdlbits.01xz.net/) | 公开硬件设计教育平台的 FSM 练习题 |
| 7 | LLM-FSM | 🟠 | LLM-FSM benchmark | 自动化生成 | 约束随机 FSM 生成 + LLM 生成 YAML 与自然语言规范 + 正确性构造 RTL/testbench + 多层验证 | FSM 配置参数 + 自然语言规范 | RTL 代码 + 测试平台 | 1000 个 FSM-to-RTL 问题（状态 2-16） | 🟠 | 论文公开，但 benchmark 文件未给出明确下载链接 | 通过自动化 pipeline 生成的大规模 FSM 推理 benchmark |
| 8 | STPA | 🟡 | Pick-and-Place + STPA 约束实验集 | 自己制作 | 对 pick-and-place 机器做 STPA 分析，生成 UCA 与控制器约束，再做多轮迭代实验 | 初始 FSM + STPA 控制器约束 | 优化后的 FSM + IEC 61499 代码 | 9 个约束 × 20 次迭代 + 1 组组合约束 × 10 次迭代 = 190 次迭代 | 🟡 | 原文未提供公开下载链接；当前可行路径更接近联系作者获取 STPA 结果与实验记录 | 基于单个工业案例和手工 STPA 分析构建的精化实验集 |
| 9 | safety | 🟡 | 航空高度控制安全测试案例 | 自己制作 + 在线收集 | 使用航空高度控制系统案例，并从 DO-178C、ARP4754A 提取 4 类 25 项安全准则，结合在线爬取需求做实验 | 基本状态图 + 航空安全准则 | 扩展状态图 + 测试用例 | 单个航空案例 + 25 项安全准则 | 🟡 | 原文未提供公开下载链接，文意上更接近联系作者团队获取 | 面向航空安全测试的状态图扩展与测试生成案例 |
| 10 | MIG | 🟠 | 公开领域建模数据集（原文未明确命名） | 公开数据集（细节未明确） | 原文说明使用公开领域建模数据集和人工标注参考模型，但未细述构造流程 | 自然语言问题描述 / 领域描述文本 | 领域模型 | 原文未明确 | 🟠 | 原文未提供公开下载链接 | 用于评估多步领域建模效果的公开类图/领域模型数据 |
| 11 | I4.0 | 🟡 | PROFINET / OPC UA 状态图识别数据 | 使用现成规范并人工裁剪 | 从 IEC 61158 和 IEC 62541 规范 PDF 中手工裁剪状态图，并对公开版本做文本打乱处理 | 状态图图像 | 可机读状态机表示 + 代码/测试 | PROFINET 80 个状态图 + OPC UA 15 个状态图 | 🔒 | [Zenodo 实现与处理结果](https://zenodo.org/records/14730727)；原始标准文档需购买 | 来自工业通信协议规范文档的状态图图像数据 |

## 初步归类与覆盖盘点

### 类别分布

| 类别 | 篇数 | 说明 |
|---|---:|---|
| 直接生成 | 5 | 直接从自然语言或系统规格生成状态机、SysML 行为图等核心工件 |
| 精化/修复/扩展 | 3 | 从已有 FSM/状态图出发做约束注入、扩展或测试生成 |
| 泛建模/邻近 baseline | 3 | 结构建模、多模态图样识别、FSM 推理 benchmark 等对比支撑项 |

### BASELINE评估分布

| 评估 | 篇数 | 说明 |
|---|---:|---|
| 🟢 | 5 | 可与“自然语言自动生成状态机模型”直接对比的核心 baseline |
| 🟡 | 4 | 与状态机生成/精化/扩展高度相关，但不属于纯自然语言直接建模 |
| 🟠 | 2 | 邻近建模或有限状态推理工作，可借鉴但不可直接公平对比 |
| ⚪ | 0 | 当前正式收录中暂无仅作背景资料的论文 |

### 当前最有价值的整体观察

1. 真正直接做“自然语言到状态机/行为模型”的论文数量仍然不多，且集中在 2024-2026。
2. 直接可比 baseline 主要集中在 `llms_emp`、`fsm-gen-iec-61499`、`req`、`umple` 和 `ttool-ai`。
3. `STPA`、`safety`、`I4.0` 和 `enhance` 虽然不构成纯自然语言直接对比，但分别覆盖了精化、安全扩展、多模态识别和 FSM 代码生成这些重要邻近场景。
4. `MIG` 和 `LLM-FSM` 更适合提供多步建模与有限状态推理层面的借鉴，不适合作为主 baseline。
5. 数据开放性不均衡；`llms_emp`、`ttool-ai`、`enhance` 的复现实用价值相对更高，`I4.0` 虽公开了实现与处理结果，但其原始标准来源仍受限，工业私有数据和作者自建小样本仍占很大比例。

## 待补充高优先级候选

以下候选已在 `project_1` 根目录历史工作文档中出现，后续若正式收录，应优先进入本论文集：

| 优先级 | 标题 | 来源文档 | 当前价值 |
|---|---|---|---|
| 高 | Automated Domain Modeling with Large Language Models: A Comparative Study | `BASELINE.md` / `BASELINE_TO_EXPLORE.md` | MIG 的单步前身工作，适合补齐“多步 vs 单步”对比 |
| 高 | On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML | `BASELINE.md` / `BASELINE_TO_EXPLORE.md` | ChatGPT 做 UML 建模的重要经验基线 |
| 高 | On the use of GPT-4 for creating goal models: An exploratory study | `BASELINE.md` / `BASELINE_TO_EXPLORE.md` | 泛建模邻近 baseline，可补足目标建模视角 |
| 高 | Towards using few-shot prompt learning for automating model completion | `BASELINE.md` / `BASELINE_TO_EXPLORE.md` | few-shot 模型补全工作，适合与多步/反馈式方法对比 |
| 中 | Towards human-bot collaborative software architecting with ChatGPT | `BASELINE.md` / `BASELINE_TO_EXPLORE.md` | 支撑“人机协同建模”视角，但与状态机生成距离略远 |
| 中 | MAPE-K loop-based goal model generation using generative AI | `BASELINE.md` / `BASELINE_TO_EXPLORE.md` | 可补“反馈循环建模”相关证据 |

## 更新日志

| 时间 | 更新内容 | 说明 |
|---|---|---|
| 2026-03-12 | 建立 `baselines/` 四件套并统一命名 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)，并将全部 `desc.md` 更名为 `DESC.md` |
| 2026-03-12 | 补充 BASELINE 评估、输入输出方法字段和数据集总表 | 将论文清单改为固定字段表，并新增“数据集与 Benchmark 清单” |
| 2026-03-12 | 细化数据集可获取性口径与链接写法 | 为数据集表新增 `🟢/🟡/🟠/🔒` 口径，并将已确认的公开地址统一改为 Markdown 链接 |
