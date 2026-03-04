# TTool-AI: 使用AI自动生成系统建模

## 文献信息
- **标题**: System Architects Are not Alone Anymore: Automatic System Modeling with AI
- **作者**: Ludovic Apvrille, Bastien Sultan
- **会议**: MODELSWARD 2024
- **机构**: Télécom Paris, IP Paris

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

### 1. 传统模型生成方法

**1.1 Landhäußer, M., Körner, S. J., & Tichy, W. F. (2014)**
- 标题: From requirements to UML models and back: how automatic processing of text can support requirements engineering
- 期刊: Software Quality Journal, 22, 121-149
- 贡献: 综述了1990年代末以来从需求自动生成形式化模型的研究历史和方法
- 局限: 指出早期方法普遍需要对输入语言施加限制或进行手动预处理

**1.2 Gelhausen, T., & Tichy, W. F. (2007)**
- 标题: Thematic role based generation of UML models from real world requirements
- 会议: International Conference on Semantic Computing (ICSC 2007), pp. 282-289
- 贡献: 提出基于主题角色的UML模型自动生成方法
- 局限: 需要对输入的自然语言施加严格约束

**1.3 Ghosh, S., Elenius, D., Li, W., Lincoln, P., Shankar, N., & Steiner, W. (2016)**
- 标题: ARSENAL: automatic requirements specification extraction from natural language
- 会议: NASA Formal Methods: 8th International Symposium, NFM 2016, Minneapolis, MN, USA, June 7-9, 2016, Proceedings 8, pp. 41-46. Springer
- 贡献: ARSENAL框架，显著减少了对输入语言的限制
- 局限: 仍然无法处理某些完全自由的自然语言表达

### 2. 建模助手工具

**2.1 Savary-Leblanc, M., Burgueño, L., Cabot, J., Le Pallec, X., & Gérard, S. (2023)**
- 标题: Software assistants in software engineering: A systematic mapping study
- 期刊: Software: Practice and Experience, 53(3), 856-892
- 贡献: 系统性综述了2010-2022年间的建模助手研究
- 发现: 共识别11篇相关论文，其中4篇关注UML模型，1篇关注SysML模型
- 结论: 建模助手工具数量有限，大多不支持行为建模

**2.2 Aquino, E. R., De Saqui-Sannes, P., & Vingerhoeds, R. A. (2020)**
- 标题: A methodological assistant for use case diagrams
- 会议: 8th MODELSWARD: International Conference on Model-Driven Engineering and Software Development, pp. 1-11
- 贡献: 提供SysML用例图设计支持的方法论助手工具

**2.3 Chami, M., Zoghbi, C., & Bruel, J.-M. (2019)**
- 标题: A first step towards AI for MBSE: Generating a part of SysML models from text using AI
- 出版物: A First Step towards AI
- 贡献: 基于自然语言处理（NLP）的框架，从文本需求自动生成SysML用例图和块图
- 特点: 早期将AI应用于MBSE的尝试

**2.4 Schräder, E., Bernijazov, R., Foullois, M., Hillebrand, M., Kaiser, L., & Dumitrescu, R. (2022)**
- 标题: Examples of AI-based assistance systems in context of model-based systems engineering
- 会议: 2022 IEEE International Symposium on Systems Engineering (ISSE), pp. 1-8. IEEE
- 贡献: 提出三种AI辅助系统：
  1. 工作坊助手：将手绘草图转换为正式SysML模型
  2. 知识库助手：基于模型训练数据提供设计建议
  3. 聊天机器人：处理关于建模的自然语言查询并以自然语言回复

### 3. 基于LLM的最新工作

**3.1 Cámara, J., Troya, J., Burgueño, L., & Vallecillo, A. (2023)**
- 标题: On the assessment of generative AI in modeling tasks: an experience report with ChatGPT and UML
- 期刊: Software and Systems Modeling, pp. 1-13
- 实验设计: 评估ChatGPT生成UML类图的能力，测试了40个不同的建模练习
- 主要发现:
  - ChatGPT能够频繁生成语法正确的模型
  - 语义准确性（特别是类之间的关系）不稳定
  - 需要一系列迭代查询来改进和增强输出
- 结论: 用户仍需投入大量工作进行迭代提问才能获得准确模型

**3.2 Ahmad, A., Waseem, M., Liang, P., Fahmideh, M., Aktar, M. S., & Mikkonen, T. (2023)**
- 标题: Towards human-bot collaborative software architecting with ChatGPT
- 会议: Proceedings of the 27th International Conference on Evaluation and Assessment in Software Engineering, pp. 279-285
- 研究内容: 使用ChatGPT进行软件架构任务，包括需求生成、UML建模和架构评估
- 主要发现:
  - ChatGPT作为软件架构师助手具有实用性
  - 存在响应变异性问题
  - 存在伦理和知识产权问题
- 结论: 人工分析和必要时的迭代提问对于收敛到正确的系统架构至关重要

**3.3 Chen, B., Chen, K., Hassani, S., Yang, Y., Amyot, D., Lessard, L., Mussbacher, G., Sabetzadeh, M., & Varró, D. (2023)**
- 标题: On the use of GPT-4 for creating goal models: An exploratory study
- 会议: 2023 IEEE 31st International Requirements Engineering Conference Workshops (REW), pp. 262-271. IEEE
- 研究内容: 评估GPT-4在目标模型生成中的应用
- 主要发现: 通过反馈机制和多次提示可以获得良好结果
- 特点: 在设计周期的早期阶段（需求工程）应用LLM

**3.4 Nakagawa, H., & Honiden, S. (2023)**
- 标题: MAPE-K loop-based goal model generation using generative AI
- 会议: 2023 IEEE 31st International Requirements Engineering Conference Workshops (REW), pp. 247-251. IEEE
- 研究内容: 使用生成式AI进行基于MAPE-K循环的目标模型生成
- 主要发现: 通过反馈和多次提示的谨慎使用可以获得良好结果

### 4. 本文的独特贡献

相比于上述所有工作，本文是**首次报告**以下三个方面的集成：

1. **直接工具集成**: 将ChatGPT直接集成到MBSE工具包（TTool）中，而非作为独立工具
2. **自动图表生成**: 从LLM的JSON响应自动生成可视化SysML图表并在工具中渲染
3. **自动化反馈循环**: 实现完全自动化的错误检测和修正循环，无需人工迭代提问

这三个特性的结合使得TTool-AI能够在40秒内生成质量超过人类的块图，相比人工建模快67.5倍，同时保持更高的一致性（标准差15分 vs 30分）。

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
