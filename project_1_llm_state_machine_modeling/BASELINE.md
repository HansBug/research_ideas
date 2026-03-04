# Project 1 Baseline工作汇总

本文档整理了从MIG和TTool-AI两篇论文的相关工作中提取的、所有基于LLM生成泛UML/SysML相关软件模型的baseline工作。

## 纳入标准

只要是基于LLM生成泛UML/SysML相关软件模型的工作都算在内，包括但不限于：
- 类图（Class Diagrams）
- 状态机图（State Machine Diagrams）
- 块定义图（Block Definition Diagrams）
- 内部块图（Internal Block Diagrams）
- 用例图（Use Case Diagrams）
- 目标模型（Goal Models）
- 领域模型（Domain Models）

## Baseline工作对比表

| 论文 | 年份 | 作者 | 发表会议/期刊 | 生成的模型类型 | 使用的LLM | 主要方法 | 主要发现/结果 | 局限性 | 来源论文 |
|------|------|------|--------------|--------------|----------|---------|-------------|--------|---------|
| **LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation** | 2026 | Wu, Y. et al. | arXiv预印本 | FSM到RTL代码 | GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro等 | 全自动化benchmark构建pipeline：FSM生成→YAML格式化→NL规范生成→RTL合成 | • 最强模型（GPT-4o）整体准确率42.3%<br>• 8个状态是性能拐点<br>• SFT提升OOD任务19.4%<br>• Best-of-N采样提升31.5% | • 仅关注FSM到RTL转换<br>• NL规范由LLM生成<br>• 验证主要依赖功能测试<br>• 状态数限制在16以内<br>• 仅评估Verilog生成 | 新增 |
| **Automated Domain Modeling with Large Language Models: A Comparative Study** | 2023 | Chen, K., Yang, Y. et al. | MODELS 2023 | 领域模型（类、属性、关系） | LLM（未明确指定） | 单步方式生成完整领域模型 | 能够从文本描述自动生成领域模型 | • 大量建模元素缺失<br>• 无法识别高级模式（如player-role）<br>• 关系识别准确率低 | MIG（作为baseline） |
| **On the use of GPT-4 for creating goal models: An exploratory study** | 2023 | Chen, B., Chen, K. et al. | IEEE REW 2023 | 目标导向模型（Goal Models） | GPT-4 | 探索性研究，评估GPT-4生成目标模型的能力 | • 提示中包含语法信息有价值<br>• 领域信息数量影响有限 | • 生成的元素可能不正确或过于通用<br>• 不利于突出利益相关者之间的冲突 | MIG（前身工作） |
| **On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML** | 2023 | Cámara et al. | Software and Systems Modeling 22(3) | UML类图 | ChatGPT | 交互模式，构建带OCL约束的UML类图 | • 能频繁生成语法正确的模型<br>• 语法错误率低 | • 语义准确性不稳定（特别是类之间的关系）<br>• 需要大量人工迭代查询来改进输出<br>• 用户工作量仍然很大 | MIG、TTool-AI |
| **Towards using few-shot prompt learning for automating model completion** | 2023 | Chaaben et al. | ICSE-NIER 2023 | 模型补全 | GPT-3 | Few-shot prompt learning进行模型补全 | 能够补全部分模型 | • 缺乏领域问题规范<br>• 严重依赖已有的部分模型<br>• 不包括属性、多重性、类的类型或关系<br>• 无法从零开始生成完整模型 | MIG |
| **Towards human-bot collaborative software architecting with ChatGPT** | 2023 | Ahmad et al. | EASE 2023 | 需求、UML模型、架构评估 | ChatGPT | 使用ChatGPT进行软件架构任务 | ChatGPT作为软件架构师助手有用 | • 响应变异性问题<br>• 伦理/知识产权问题<br>• 需要人工分析和迭代提问才能收敛到正确架构 | TTool-AI |
| **MAPE-K loop-based goal model generation using generative AI** | 2023 | Nakagawa & Honiden | IEEE REW 2023 | 目标模型（Goal Models） | 生成式AI（未明确指定） | 基于MAPE-K循环生成目标模型 | 通过反馈机制能产生有希望的结果 | 需要反馈和多个提示 | TTool-AI |
| **Recommending metamodel concepts during modeling activities with pre-trained language models** | 2022 | Weyssow et al. | Software and Systems Modeling 21(3) | 元模型概念推荐 | 预训练语言模型 | 推荐元模型概念 | 预训练语言模型在建模任务中有应用潜力 | 仅提供推荐，非完全自动化生成 | MIG |

## 非LLM方法（作为对比参考）

以下是论文中提到的传统方法，虽然不是基于LLM，但作为对比参考有助于理解LLM方法的优势：

| 论文 | 年份 | 作者 | 方法类型 | 主要局限性 | 来源论文 |
|------|------|------|---------|-----------|---------|
| Automated Extraction of Conceptual Models from User Stories via NLP | 2016 | Robeer et al. | 基于规则（23个启发式规则） | 规则编写成本高，泛化能力弱 | MIG |
| From user requirements to UML class diagram | 2012 | Herchi & Ben Abdessalem | 语言规则（名词→实体类型） | 规则过于简单，容易误报 | MIG |
| An NLP-based architecture for the autocompletion of partial domain models | 2021 | Burgueño et al. | NLP词嵌入模型 | 需要部分模型输入，表达能力有限 | MIG |
| Machine Learning-Based Incremental Learning in Interactive Domain Modelling | 2022 | Saini et al. | 机器学习增量学习 | 需要监督训练和用户交互 | MIG |
| ARSENAL: automatic requirements specification extraction from natural language | 2016 | Ghosh et al. | 最小化输入语言限制 | 某些自然语言表达仍难以处理 | TTool-AI |
| Thematic role based generation of UML models from real world requirements | 2007 | Gelhausen & Tichy | 基于主题角色 | 需要对输入语法施加约束或手动预处理 | TTool-AI |
| A first step towards AI for MBSE: Generating a part of SysML models from text using AI | 2019 | Chami et al. | 基于NLP的框架 | 使用传统NLP而非LLM | TTool-AI |

## 建模助手工具（非完全自动化生成）

以下工作主要提供建模辅助功能，而非完全自动化生成：

| 论文 | 年份 | 作者 | 工具/方法 | 功能 | 来源论文 |
|------|------|------|---------|------|---------|
| A methodological assistant for use case diagrams | 2020 | Aquino et al. | 方法论助手 | 支持SysML用例图设计 | TTool-AI |
| Examples of AI-based assistance systems in context of model-based systems engineering | 2022 | Schräder et al. | AI-based MBSE助手 | • 草图转换助手<br>• 知识库设计建议<br>• 建模查询聊天机器人 | TTool-AI |

## 关键发现总结

### 1. 基于LLM的建模工作现状（截至2023-2024）

从相关工作中可以看出，基于LLM生成UML/SysML模型的研究在2023年开始活跃：

**主要工作类型**：
- **领域模型/类图生成**：Chen et al. (2023), Cámara et al. (2023), Chaaben et al. (2023)
- **目标模型生成**：Chen et al. (2023), Nakagawa & Honiden (2023)
- **软件架构**：Ahmad et al. (2023)
- **元模型推荐**：Weyssow et al. (2022)

**使用的LLM**：
- GPT-4：Chen et al. (2023)
- ChatGPT：Cámara et al. (2023), Ahmad et al. (2023)
- GPT-3：Chaaben et al. (2023)
- 预训练语言模型：Weyssow et al. (2022)

### 2. 共同的局限性

所有基于LLM的建模工作都存在以下共同问题：

1. **语义准确性不稳定**：特别是关系识别（Cámara et al., Chen et al.）
2. **需要大量人工迭代**：用户需要反复提问和修正（Cámara et al., Ahmad et al., Nakagawa & Honiden）
3. **元素缺失或不准确**：生成的模型不完整或包含错误元素（Chen et al., Chaaben et al.）
4. **依赖部分输入**：某些方法需要部分模型作为输入（Chaaben et al.）
5. **缺乏形式化验证**：所有工作都只关注生成，不涉及验证

### 3. 与传统方法的对比

**传统方法的局限性**：
- **基于规则的方法**：规则编写成本高，泛化能力弱（Robeer et al., Herchi & Ben Abdessalem, Gelhausen & Tichy）
- **基于机器学习的方法**：需要监督训练和标注数据（Saini et al.）
- **基于NLP的方法**：表达能力有限，需要部分模型输入（Burgueño et al., Chami et al.）

**LLM方法的优势**：
- 能够处理完全自由的自然语言
- 无需手动设计规则或监督训练
- 能够生成语法正确的模型

### 4. 研究空白

从相关工作分析可以看出，以下方向存在明显空白：

1. **状态机自动生成**：相关工作主要集中在结构建模（类图、块图），行为建模（状态机）的工作较少
   - **更新（2026）**：LLM-FSM填补了FSM推理评估的空白，但仅关注硬件RTL生成，控制系统软件状态机建模仍是空白
2. **形式化验证集成**：所有工作都缺乏与形式化验证工具的集成
   - **更新（2026）**：LLM-FSM使用SAT求解器进行等价性检查，但未涉及时序逻辑性质验证和模型检查
3. **自动修复机制**：没有工作提出基于验证反馈的自动修复方法
4. **时间属性处理**：缺乏对时间约束和时间自动机的支持
5. **完整闭环**：缺乏"生成-验证-修复"的完整自动化闭环

这些空白正是本博士研究的切入点。

## 对本研究的启示

### 1. 现有工作的不足

从相关工作可以看出，现有基于LLM的建模工作存在以下系统性不足：

- **只关注生成阶段**：缺乏验证和修复
- **需要大量人工干预**：无法实现完全自动化
- **语义准确性问题**：特别是关系和行为建模
- **缺乏领域知识融合**：通用LLM缺乏控制系统特定知识

### 2. 本研究的创新点

相比现有工作，本研究的创新在于：

1. **完整闭环**：构建"生成-验证-修复"的完整自动化流程
2. **形式化验证集成**：与UPPAAL等模型检查工具深度集成
3. **领域知识注入**：注入控制系统和时间自动机的专门知识
4. **自动修复机制**：基于验证反馈的迭代式自动修复
5. **时间属性支持**：专门处理时间约束和时间自动机

### 3. 可借鉴的技术

从相关工作中可以借鉴的技术包括：

- **Few-shot learning**：提供示例指导LLM（多篇论文采用）
- **反馈机制**：通过反馈改进生成质量（Nakagawa & Honiden, Cámara et al.）
- **交互式方法**：人机协作建模（Ahmad et al.）
- **语法约束注入**：提供语法信息指导生成（Chen et al.）

## 参考文献

### 基于LLM的建模工作

1. Chen, K., Yang, Y., et al. (2023). Automated Domain Modeling with Large Language Models: A Comparative Study. *MODELS 2023*.

2. Chen, B., Chen, K., et al. (2023). On the use of GPT-4 for creating goal models: An exploratory study. *IEEE REW 2023*.

3. Cámara, J., et al. (2023). On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML. *Software and Systems Modeling*, 22(3), 781-793.

4. Chaaben, N., et al. (2023). Towards using few-shot prompt learning for automating model completion. *ICSE-NIER 2023*.

5. Ahmad, A., et al. (2023). Towards human-bot collaborative software architecting with ChatGPT. *EASE 2023*.

6. Nakagawa, T., & Honiden, S. (2023). MAPE-K loop-based goal model generation using generative AI. *IEEE REW 2023*.

7. Weyssow, M., et al. (2022). Recommending metamodel concepts during modeling activities with pre-trained language models. *Software and Systems Modeling*, 21(3), 1071-1089.

### 传统方法（对比参考）

8. Robeer, M., et al. (2016). Automated Extraction of Conceptual Models from User Stories via NLP. *RE 2016*.

9. Herchi, H., & Ben Abdessalem, W. (2012). From user requirements to UML class diagram. *arXiv preprint arXiv:1211.0713*.

10. Burgueño, L., et al. (2021). An NLP-based architecture for the autocompletion of partial domain models. *CAiSE 2021*.

11. Saini, R., et al. (2022). Machine Learning-Based Incremental Learning in Interactive Domain Modelling. *MODELS 2022*.

12. Ghosh, S., et al. (2016). ARSENAL: automatic requirements specification extraction from natural language. *NFM 2016*.

13. Gelhausen, T., & Tichy, M. (2007). Thematic role based generation of UML models from real world requirements. *ICSC 2007*.

14. Chami, M., et al. (2019). A first step towards AI for MBSE: Generating a part of SysML models from text using AI.

### 建模助手工具

15. Aquino, G., et al. (2020). A methodological assistant for use case diagrams. *MODELSWARD 2020*.

16. Schräder, J., et al. (2022). Examples of AI-based assistance systems in context of model-based systems engineering. *IEEE ISSE 2022*.

## 更新日志

- 2026-03-05: 添加LLM-FSM论文（2026），首个针对FSM推理的自动化benchmark
- 2026-03-05: 重新整理，仅保留从MIG和TTool-AI相关工作中提取的基于LLM的建模工作
