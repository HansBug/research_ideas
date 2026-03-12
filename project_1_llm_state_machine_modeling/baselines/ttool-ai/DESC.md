# TTool-AI: 使用AI自动生成系统建模

## 文献信息
- **标题**: System Architects Are not Alone Anymore: Automatic System Modeling with AI
- **作者**: Ludovic Apvrille, Bastien Sultan
- **会议**: MODELSWARD 2024
- **机构**: Télécom Paris, IP Paris
- **代码/仓库获取（原文）**：论文第5.2节明确给出公开仓库
  - https://github.com/zebradile/ttool-ai
  - 仓库包含3个测试系统目录（platooning、space-basedsystem、AutomatedBraking）、规范desc文件、TTool-AI生成的.xml模型、复现实验README与result.ods
- **数据集获取（原文）**：论文未单独发布“独立数据集下载页”；数据获取方式为直接使用上述GitHub仓库中的公开实验工件（规范+模型+结果）

## 简报

**解决的问题**：本文提出了TTool-AI框架，将大语言模型集成到系统建模工具中，实现从自然语言规范自动生成SysML图表（块定义图、内部块图和状态机图）。

- **输入**：自然语言形式的系统规范（system specification）、系统工程领域知识（domain knowledge）、SysML语法约束（syntax constraints）
- **方法**：TTool-AI框架，包括知识注入机制、自动反馈循环（最多20次迭代）、JSON到SysML的自动转换
- **输出**：可视化SysML图表，包括块定义图（Block Definition Diagrams）、内部块图（Internal Block Diagrams）、状态机图（State Machine Diagrams）

```
┌─────────────────────────────────────────────────────────────────┐
│                           输入层                                 │
├─────────────────────────────────────────────────────────────────┤
│ • 自然语言系统规范（完全自由的自然语言）                          │
│ • 系统工程领域知识（注入到LLM）                                   │
│ • SysML语法约束和格式要求                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      TTool-AI框架                                │
├─────────────────────────────────────────────────────────────────┤
│  知识注入 → LLM生成JSON → 语法/语义检查                          │
│                    ↓                                             │
│              错误检测？                                          │
│            ↙        ↘                                           │
│        有错误      无错误                                        │
│          ↓           ↓                                          │
│    反馈修正循环   转换为SysML                                    │
│   (最多20次迭代)                                                 │
│          ↓                                                       │
│    重新生成JSON                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          输出层                                  │
├─────────────────────────────────────────────────────────────────┤
│ • 块定义图（Block Definition Diagrams）                          │
│ • 内部块图（Internal Block Diagrams）                            │
│ • 状态机图（State Machine Diagrams）                             │
│ • TTool中的可视化图表                                            │
└─────────────────────────────────────────────────────────────────┘
```

实验证明，TTool-AI在块图生成上得分81/100（学生70/100），速度快67.5倍；状态机生成得分63/100（学生58/100），速度快15.2倍。

**研究动机**：传统的从需求到模型的转换过程耗时且需要专业知识。现有自动化方法对输入语言有严格限制，需要手动预处理。直接使用LLM（如ChatGPT）虽然能处理自由自然语言，但存在语义准确性不稳定、需要大量人工迭代提问的问题。作者发现简单地向ChatGPT提问无法获得高质量模型，特别是类之间的关系识别不准确，用户仍需投入大量工作进行迭代才能收敛到正确模型。

**方法创新**：TTool-AI的核心创新在于三个方面：（1）知识注入机制，向LLM系统性地注入系统工程领域知识、SysML语法约束和格式要求，而非依赖LLM的预训练知识；（2）自动反馈循环，框架自动检测AI生成结果的语法和语义错误，并迭代修正（最多20次），无需人工干预；（3）工具链集成，将AI生成的JSON格式模型自动转换为TTool中的可视化SysML图表，实现端到端自动化。

**实验设计**：实验使用3个来自欧洲项目的真实系统规范（Platooning车辆编队、Space-based空间系统、Automated Braking自动刹车）。对比对象是约15名接受过21小时SysML和TTool培训的硕士研究生，他们在1.5小时考试中完成相同的建模任务。评估指标包括图表与规范的符合度、交互数量、可读性、命名一致性、属性使用情况和语法正确性六个维度。TTool-AI配置为完全自动化模式（禁用人工交互），块图反馈循环最多20次，状态机反馈循环最多10次。使用GPT-3.5 turbo模型。

**结论与不足**：实验结果表明，TTool-AI在质量和速度上都优于人类。块图质量提升15.7%（81分vs70分），生成速度快67.5倍（40秒vs2700秒）；状态机质量提升8.6%（63分vs58分），生成速度快15.2倍（178秒vs2700秒）。一致性更高（标准差15分vs30分）。但方法也存在局限：（1）AI知识容量限制，信息过载时模型质量下降；（2）对于复杂、冗长、模糊的规范，性能有待提升；（3）结构建模（块图81分）明显优于行为建模（状态机63分）；（4）即使经过多次反馈循环，仍可能存在小问题（如无用的guard、信号参数数量错误），需要人工修正。

## 核心工作

本文提出了**TTool-AI框架**，这是一个将大语言模型（LLM，特别是ChatGPT 3.5）集成到系统建模工具TTool中的自动化框架。该框架能够从自然语言的系统规范自动生成SysML图表，包括：

1. **结构图**：Block Definition Diagrams（块定义图）和Internal Block Diagrams（内部块图）
2. **行为图**：State Machine Diagrams（状态机图）

核心创新点包括：
- **知识注入机制**：向LLM注入系统工程领域知识、SysML语法约束和格式要求
- **自动反馈循环**：自动检测AI生成结果的语法和语义错误，并迭代修正（最多20次迭代）
- **工具集成**：将AI生成的JSON格式模型自动转换为TTool中的可视化SysML图表

## 解决的问题

### 之前存在的问题

1. **从需求到模型的转换困难**：系统开发遵循V模型，需要将自然语言规范转换为SysML图表，这个过程耗时且需要专业知识
2. **现有自动化方法的局限性**：
   - 早期方法（1990年代末至今）对输入语言有严格限制，需要手动预处理
   - 即使是较新的框架（如ARSENAL），仍然无法处理完全自由的自然语言表达
   - 现有建模助手工具数量有限，且大多不支持行为建模

3. **直接使用LLM的问题**：
   - 简单地向ChatGPT提问无法获得高质量的模型
   - 语义准确性不稳定（特别是类之间的关系）
   - 需要大量人工迭代提问才能收敛到正确模型
   - 用户工作量仍然很大

## 相比之前工作的进展

### 与传统方法对比

| 方面 | 传统方法 | TTool-AI |
|------|---------|----------|
| 输入语言限制 | 需要受限的自然语言或预处理 | 完全自由的自然语言 |
| 自动化程度 | 需要大量人工干预 | 自动生成+自动反馈循环 |
| 工具集成 | 独立工具 | 直接集成到MBSE工具链 |

### 与直接使用LLM对比

- **自动化反馈**：无需人工迭代提问，系统自动检测和修正错误
- **领域知识注入**：通过结构化的知识注入提高生成质量
- **工具链集成**：自动将AI输出转换为可用的模型，而非仅生成文本

### 实验设计与结果

#### 实验方法

**测试环境**：
- 工具版本：TTool nightly build (2023年10月)
- AI模型：ChatGPT 3.5 turbo
- 测试系统：3个来自欧洲项目的真实用例规范
  - Platooning（车辆编队）系统
  - Space-based system（空间系统）
  - Automated Braking（自动刹车）系统

**对照组设置**：
- 参与者：约15名硕士研究生
- 培训时长：21小时SysML和TTool培训
- 练习准备：至少3个不同规范的练习机会
- 考试时长：1.5小时完成设计和绘制状态机
- 评分标准：对TTool-AI和学生使用完全相同的评分标准

**评分维度**（软件工程质量标准）：
1. 图表与规范的符合度（架构是否满足规范？状态机行为是否符合规范？）
2. 块之间的交互数量
3. 图表可读性
4. 块和状态的数量及命名一致性
5. 属性使用情况（是否有声明但未使用的属性）
6. 语法正确性（TTool语法检查器检测到的错误和警告数量）

**TTool-AI配置**：
- 禁用人工交互功能（完全自动化）
- 块图反馈循环：最多20次迭代
- 状态机反馈循环：最多10次迭代

#### 实验结果

**定量对比**：

| 指标 | TTool-AI | 学生 | TTool-AI优势 |
|------|----------|------|-------------|
| 块图平均得分 | 81/100 | 70/100 | +11分 (15.7%提升) |
| 块图生成时间 | 40秒 | 2700秒 | 快67.5倍 |
| 状态机平均得分 | 63/100 | 58/100 | +5分 (8.6%提升) |
| 状态机生成时间 | 178秒 | 2700秒 | 快15.2倍 |
| 块图得分标准差 | 16分 | 26分 | 一致性更高 |
| 状态机得分标准差 | 15分 | 32分 | 一致性更高 |

**结果分析**：

1. **速度优势显著**：
   - 块图生成速度提升67.5倍（40秒 vs 2700秒）
   - 状态机生成速度提升15.2倍（178秒 vs 2700秒）
   - **佐证问题**：证明了自动化框架能够大幅减少建模时间，解决了传统手工建模耗时的问题

2. **质量略优于人类**：
   - 块图质量提升15.7%（81分 vs 70分）
   - 状态机质量提升8.6%（63分 vs 58分）
   - **佐证问题**：证明了通过知识注入和反馈循环，AI生成的模型质量可以达到甚至超过受过培训的人类水平

3. **一致性更高**：
   - TTool-AI标准差约15分，学生标准差约30分
   - **佐证问题**：证明了AI方法的稳定性和可靠性，不会像人类一样因个体差异产生大幅波动

4. **系统复杂度影响**：
   - 简单系统（platooning, space-based）：TTool-AI表现优异
   - 复杂系统（automated braking，规范冗长、复杂、模糊）：学生在状态机上略有优势，但块图仍是TTool-AI更好
   - **佐证问题**：揭示了当前方法的局限性——对于高度复杂和模糊的规范，AI理解能力仍有待提升

5. **结构建模 vs 行为建模**：
   - 块图得分（81）明显高于状态机得分（63）
   - 学生也表现出相同趋势（70 vs 58）
   - **佐证问题**：说明识别系统结构比识别行为更容易，这对AI和人类都成立

#### 关键发现

1. **TTool-AI不是要取代工程师**：
   - 实验中禁用了人工交互功能
   - 如果学生在1.5小时内与TTool-AI协作，预期会获得更高分数
   - **最佳使用场景**：AI快速生成初始架构和状态机草图，工程师进行精细化调整和优化

2. **自动反馈循环的价值**：
   - 相比Cámara et al. (2023)的研究（需要大量人工迭代提问），TTool-AI通过自动反馈循环显著减少了用户工作量
   - 即使经过10次反馈循环，仍可能存在小问题（如无用的guard、信号参数数量错误），但这些问题可以轻松手工修正

3. **可复现性**：
   - 所有测试系统已公开在GitHub：https://github.com/zebradile/ttool-ai
   - 包含系统规范（.desc文件）和生成的模型（.xml文件）
   - 提供了详细的结果数据（result.ods文件）

## 重要的相关工作

### 1. 重要的前身类工作

**无**

论文中没有明确提到作者团队自己的前期工作，也没有明确表示基于某个特定工作进行改进或继续发展。

### 2. 直接参与实验的baseline

**无**

论文的实验部分（第5节）主要是将TTool+AI与学生手工建模进行对比（表1，第992-1000行），并没有与其他自动化工具或方法进行直接的实验对比。

### 3. 提供了重要论证的工作

**3.1 Landhäußer et al. (2014) - 自动模型生成综述**
- 标题: From requirements to UML models and back: how automatic processing of text can support requirements engineering
- 期刊: Software Quality Journal, 22:121–149
- 主要内容: 提供了从需求到UML模型自动生成领域的综合文献综述，涵盖了1990年代末以来的研究历史。
- 论文中的引用:
  - 第935行："As elucidated in the comprehensive literature review contained in (Landhäußer et al., 2014), this area of study has been active since the late 1990s."
- 主要发现: 该领域自1990年代末就开始活跃，但一直存在挑战。
- 与TTool-AI的关系: 为TTool-AI的研究背景提供了历史脉络，说明自动模型生成是一个长期存在的研究挑战。
- 佐证内容: 提供历史背景和文献综述支持，论证该研究问题的长期性和重要性

**3.2 Gelhausen & Tichy (2007) - 基于主题角色的UML生成**
- 标题: Thematic role based generation of UML models from real world requirements
- 会议: International Conference on Semantic Computing (ICSC 2007), pages 282–289
- 主要内容: 基于主题角色从真实世界需求生成UML模型的方法。
- 论文中的引用:
  - 第939-940行："However, the process of model generation often requires imposing constraints on the syntax of input requirements or necessitates manual preprocessing, as exemplified in the work by Gelhausen et al."
- 局限性: 模型生成过程需要对输入需求的语法施加约束或需要手动预处理。
- 与TTool-AI的关系: 作为传统方法的代表，说明了现有方法的局限性（需要约束输入语法或手动预处理），为TTool-AI使用LLM处理完全自由的自然语言提供了动机。
- 佐证内容: 论证现有方法需要约束输入或手动预处理的不足，支持研究动机

**3.3 Ghosh et al. (2016) - ARSENAL框架**
- 标题: ARSENAL: automatic requirements specification extraction from natural language
- 会议: NASA Formal Methods: 8th International Symposium, NFM 2016, Minneapolis, MN, USA, June 7-9, 2016, Proceedings 8, pages 41–46. Springer
- 主要内容: ARSENAL框架，一种从自然语言自动提取需求规范的方法。
- 论文中的引用:
  - 第941-943行："Recent advancements, such as the ARSENAL framework (Ghosh et al., 2016), have introduced model generation approaches that minimize restrictions on the input language."
  - 第943-947行："Nonetheless, even with these powerful tools, certain natural language expressions can still pose challenges, eluding their automated transformation into formal models."
- 主要发现: 虽然最小化了对输入语言的限制，但某些自然语言表达仍然会带来挑战。
- 局限性: 难以自动转换某些自然语言表达为形式化模型。
- 与TTool-AI的关系: 代表了最新的传统方法，但仍存在局限性。TTool-AI认为LLM（如GPT）的出现为处理完全自由的自然语言提供了新机会。
- 佐证内容: 论证即使是先进的传统方法也存在不足，支持采用LLM的研究动机

**3.4 Savary-Leblanc et al. (2023) - 建模助手系统性综述**
- 标题: Software assistants in software engineering: A systematic mapping study
- 期刊: Software: Practice and Experience, 53(3):856–892
- 主要内容: 关于软件工程中软件助手的系统性映射研究，涵盖2010-2022年间的论文。
- 论文中的引用:
  - 第958-963行："In a comprehensive survey conducted by Savary-Leblanc et al., which encompassed papers published between 2010 and 2022, the authors identified 11 notable papers introducing tools aimed at aiding engineers in the process of model design."
- 主要发现: 识别了11篇引入建模辅助工具的重要论文，其中4篇专注于UML模型，1篇涉及SysML模型。
- 与TTool-AI的关系: 提供了建模助手领域的全面综述，为TTool-AI的研究定位提供了背景。
- 佐证内容: 提供领域综述，论证建模助手是一个持续的研究方向

**3.5 Aquino et al. (2020) - 用例图方法论助手**
- 标题: A methodological assistant for use case diagrams
- 会议: 8th MODELSWARD: International Conference on Model-Driven Engineering and Software Development, pages 1–11
- 主要内容: 一个支持用例图设计的方法论助手工具。
- 论文中的引用:
  - 第963-967行："Among these papers, four specifically concentrated on UML models, with one of them addressing SysML models, introducing a tool that offers support for the design of use-case diagrams (Aquino et al., 2020)."
- 主要发现: 专注于SysML用例图的设计支持。
- 与TTool-AI的关系: 作为现有SysML建模助手的代表，但仅支持用例图，而TTool-AI支持块图和状态机图。
- 佐证内容: 说明现有工具的范围有限，支持TTool-AI扩展到块图和状态机图的必要性

**3.6 Chami et al. (2019) - 基于NLP的SysML生成**
- 标题: A first step towards AI for MBSE: Generating a part of SysML models from text using AI
- 出处: A First Step towards AI
- 主要内容: 基于NLP的框架，从文本需求自动生成SysML用例图和块图。
- 论文中的引用:
  - 第971-974行："In this context, Chami et al. introduced a framework grounded in natural language processing (NLP) that autonomously generates SysML use-case and block diagrams from textual requirements inputs."
- 主要发现: 使用传统NLP方法生成SysML模型。
- 与TTool-AI的关系: 代表了AI-based MBSE助手的早期尝试，但使用的是传统NLP而非LLM。TTool-AI使用更先进的LLM技术。
- 佐证内容: 论证AI在MBSE中的应用趋势，但指出传统NLP方法的局限性

**3.7 Schräder et al. (2022) - AI-based MBSE助手系统**
- 标题: Examples of AI-based assistance systems in context of model-based systems engineering
- 会议: 2022 IEEE International Symposium on Systems Engineering (ISSE), pages 1–8. IEEE
- 主要内容: 三个AI-based MBSE助手：草图转换助手、知识库设计建议助手、建模查询聊天机器人。
- 论文中的引用:
  - 第975-984行："Furthermore, Schräder et al. introduced three AI-based MBSE assistants, each serving distinct purposes: a workshop assistant capable of converting hand-drawn sketches into formal SysML models, a knowledge-based assistant offering design suggestions based on training data derived from a set of models, and a chatbot designed to process natural language queries related to modeling and provide responses in a natural language format."
- 主要发现: 提供了多种AI辅助功能，但主要是辅助性质。
- 局限性: 主要是辅助性质，而非自动生成完整模型。
- 与TTool-AI的关系: 代表了AI在MBSE中的多样化应用，但TTool-AI专注于从自然语言自动生成完整的SysML模型。
- 佐证内容: 论证AI-based MBSE助手的多样性，但指出现有工具主要是辅助性质

**3.8 Cámara et al. (2023) - ChatGPT在UML建模中的评估**
- 标题: On the assessment of generative AI in modeling tasks: an experience report with ChatGPT and UML
- 期刊: Software and Systems Modeling, pages 1–13
- 主要内容: 评估ChatGPT在UML类图生成任务中的能力，基于40个建模练习。
- 论文中的引用:
  - 第1001-1007行："Indeed, these chatbots can now generate responses formatted to cater specifically to the requirements of model designers, such as producing UML diagrams with a remarkably low rate of syntax errors (Cámara et al., 2023)."
  - 第1007-1018行："In this study, the authors assessed ChatGPT's model generation capabilities by tasking it with producing UML class diagrams based on specifications provided in natural language. An examination of the algorithm's responses to 40 distinct modeling exercises led the authors to the observation that ChatGPT frequently succeeded in generating syntactically correct models. However, it was noted that the semantic accuracy of these models (particularly concerning the relationships between classes) was not consistently achieved."
  - 第1018-1022行："Given these imperfections, achieving an accurate model necessitates a series of iterative inquiries to refine and enhance the output. Consequently, the authors concluded that the effort required by the user is still important."
- 主要发现:
  - ChatGPT能够生成语法正确的模型，语法错误率低
  - 但语义准确性（特别是类之间的关系）不一致
  - 需要一系列迭代查询来完善输出
  - 用户仍需投入大量精力
- 局限性: 直接使用ChatGPT需要大量用户迭代。
- 与TTool-AI的关系: **这是TTool-AI最重要的论证支持**。指出了直接使用ChatGPT的核心问题（需要大量用户迭代），TTool-AI通过自动化反馈循环解决了这个问题，实验显示TTool-AI在40秒内生成的块图质量超过人类，比人工建模快67.5倍。
- 佐证内容: 论证直接使用LLM需要大量人工迭代的不足，支持TTool-AI的自动化反馈循环设计

**3.9 Ahmad et al. (2023) - ChatGPT在软件架构中的应用**
- 标题: Towards human-bot collaborative software architecting with ChatGPT
- 会议: Proceedings of the 27th International Conference on Evaluation and Assessment in Software Engineering, pages 279–285
- 主要内容: 使用ChatGPT进行软件架构任务的综合报告，包括生成需求、UML模型和评估架构。
- 论文中的引用:
  - 第1026-1034行："In a more architecture process-oriented study, Ahmad et al. present a comprehensive report detailing their use of ChatGPT for software architecture tasks, which include generating requirements, UML models, and evaluating the proposed architecture. Their experiment highlights the utility of ChatGPT as an assistant for software architects, but also raises several concerns about its responses, including response variability and ethics/intellectual property issues."
  - 第1034-1037行："In both cases, human analysis and, if necessary, iterative questioning are essential to converge towards a correct system architecture."
- 主要发现:
  - ChatGPT作为软件架构师助手有用
  - 但存在响应变异性和伦理/知识产权问题
  - 需要人工分析和迭代提问才能收敛到正确的系统架构
- 局限性: 需要大量人工干预。
- 与TTool-AI的关系: 进一步论证了直接使用ChatGPT需要大量人工干预的问题，支持TTool-AI的自动化反馈循环设计。
- 佐证内容: 论证直接使用LLM需要人工迭代的局限性，支持TTool-AI的自动化方法

**3.10 Chen et al. (2023) - GPT-4创建目标模型**
- 标题: On the use of GPT-4 for creating goal models: An exploratory study
- 会议: 2023 IEEE 31st International Requirements Engineering Conference Workshops (REW), pages 262–271. IEEE
- 主要内容: 使用GPT-4创建目标模型的探索性研究。
- 论文中的引用:
  - 第1038-1042行："At an earlier stage in the design cycle, LLM have also been evaluated on the generation of goal-models (Chen et al., 2023; Nakagawa and Honiden, 2023), yielding promising results when used judiciously (e.g., through the incorporation of feedback and/or running multiple prompts)."
- 主要发现: 当谨慎使用时（例如通过反馈和/或运行多个提示）能产生有希望的结果。
- 与TTool-AI的关系: 说明LLM在设计周期早期阶段（目标模型生成）的应用，支持LLM在建模任务中的潜力，特别是通过反馈机制的重要性。
- 佐证内容: 论证LLM在建模任务中的潜力，特别是反馈机制的重要性

**3.11 Nakagawa & Honiden (2023) - 基于MAPE-K循环的目标模型生成**
- 标题: MAPE-K loop-based goal model generation using generative AI
- 会议: 2023 IEEE 31st International Requirements Engineering Conference Workshops (REW), pages 247–251. IEEE
- 主要内容: 基于MAPE-K循环使用生成式AI生成目标模型。
- 论文中的引用:
  - 第1038-1042行："At an earlier stage in the design cycle, LLM have also been evaluated on the generation of goal-models (Chen et al., 2023; Nakagawa and Honiden, 2023), yielding promising results when used judiciously (e.g., through the incorporation of feedback and/or running multiple prompts)."
- 主要发现: 通过反馈机制能产生有希望的结果。
- 与TTool-AI的关系: 说明反馈循环在LLM建模中的重要性，与TTool-AI的自动化反馈循环设计理念一致。
- 佐证内容: 论证反馈机制在LLM建模中的重要性，支持TTool-AI的反馈循环设计

### 4. 在技术上提供了支持的工作

**4.1 OpenAI (2023) - GPT-4**
- 标题: GPT-4 Technical Report
- 类型: Technical report
- 主要内容: GPT-4技术报告，描述了GPT-4的架构和能力。
- 论文中的引用:
  - 第43行："Large Language Models (LLMs) like OpenAI's GPT, surely"
  - 第131-132行："Large Language Models (LLMs), such as OpenAI's GPT (OpenAI, 2023), draw upon techniques from"
  - 第159行："an API key obtained from OpenAI), the specific lan-"
  - 第780行："the capability of OpenAI's API to inject knowl-"
- 主要发现: 提供了强大的自然语言处理和生成能力。
- 与TTool-AI的关系: **TTool-AI直接使用OpenAI的GPT（通过API）作为核心技术组件**，用于从自然语言生成SysML模型。论文多处提到使用OpenAI API和GPT模型。
- 技术使用: 提供核心技术支持，TTool-AI直接采用GPT作为LLM引擎

### 5. 其他重要工作

**无**

论文中引用的所有文献都已在上述类别中分类。

## 文献分类总结

TTool-AI论文共引用**12篇文献**（包括OpenAI技术报告），按作用分类如下：

1. **前身类工作（0篇）**：无
2. **实验baseline（0篇）**：无
3. **论证支持（11篇）**：主要论证现有方法的局限性和LLM的潜力
4. **技术支持（1篇）**：OpenAI GPT-4
5. **其他支持（0篇）**：无

TTool-AI的核心创新在于：
- **自动化反馈循环**：解决了直接使用LLM需要大量人工迭代的问题
- **知识库注入**：为LLM提供SysML建模的专门知识
- **工具集成**：将LLM直接集成到MBSE工具（TTool）中
- **自动图表生成**：从LLM的JSON响应自动生成可视化SysML图表

实验结果表明，TTool-AI在40秒内生成的块图质量超过人类（平均分85 vs 70），比人工建模快67.5倍（40秒 vs 45分钟），且一致性更高（标准差15 vs 30）。

## 局限性与未来工作

1. **规模化挑战**：AI知识容量限制，信息过载时模型质量下降
2. **复杂系统处理**：对于复杂、冗长、模糊的规范，性能有待提升
3. **未来方向**：
   - 层次化建模
   - 增量式建模
   - 精化过程

## 技术细节

- **使用模型**：GPT-3.5 turbo（16,000 tokens上下文限制）
- **知识实例限制**：每个不超过200词
- **反馈循环次数**：默认20次（块图）或10次（状态机）
- **输出格式**：JSON → SysML V2文本格式 → TTool可视化图表
