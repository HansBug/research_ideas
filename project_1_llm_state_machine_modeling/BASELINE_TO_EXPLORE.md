# Project 1 待探索的Baseline工作

本文档整理了需要进一步检索和阅读的、基于大语言模型生成UML/SysML模型的学术工作线索。

## 检索策略

### 学术数据库
- **arXiv**: https://arxiv.org/
- **ACM Digital Library**: https://dl.acm.org/
- **IEEE Xplore**: https://ieeexplore.ieee.org/
- **Springer**: https://link.springer.com/
- **Google Scholar**: https://scholar.google.com/

### 检索关键词组合

#### 核心关键词
1. **模型类型**：
   - UML (Unified Modeling Language)
   - SysML (Systems Modeling Language)
   - Class Diagram
   - State Machine / State Diagram
   - Sequence Diagram
   - Activity Diagram
   - Domain Model
   - Goal Model

2. **技术方法**：
   - Large Language Model / LLM
   - GPT / GPT-4 / GPT-3.5
   - ChatGPT
   - Generative AI
   - Transformer
   - Pre-trained Language Model

3. **任务类型**：
   - Generation / Automatic Generation
   - Synthesis
   - Modeling / Automated Modeling
   - Model-Driven Engineering / MDE
   - Model-Based Systems Engineering / MBSE

#### 推荐检索式

**检索式1：UML类图生成**
```
("large language model" OR "LLM" OR "GPT" OR "ChatGPT") AND
("UML" OR "class diagram") AND
("generation" OR "synthesis" OR "automated") AND
(2023 OR 2024 OR 2025)
```

**检索式2：SysML建模**
```
("large language model" OR "LLM" OR "GPT") AND
("SysML" OR "systems modeling") AND
("automatic" OR "generation") AND
(2023 OR 2024 OR 2025)
```

**检索式3：状态机生成**
```
("large language model" OR "LLM" OR "GPT") AND
("state machine" OR "state diagram" OR "statechart") AND
("generation" OR "synthesis") AND
(2023 OR 2024 OR 2025)
```

**检索式4：软件建模**
```
("generative AI" OR "LLM") AND
("software modeling" OR "domain modeling") AND
("UML" OR "SysML") AND
(2023 OR 2024 OR 2025)
```

**检索式5：MBSE相关**
```
("large language model" OR "GPT") AND
("MBSE" OR "model-based systems engineering" OR "MDE") AND
(2023 OR 2024 OR 2025)
```

### 重点会议和期刊

#### 软件工程顶会/期刊
- **ICSE** (International Conference on Software Engineering)
- **FSE/ESEC** (Foundations of Software Engineering)
- **ASE** (Automated Software Engineering)
- **TSE** (IEEE Transactions on Software Engineering)
- **TOSEM** (ACM Transactions on Software Engineering and Methodology)

#### 建模相关会议/期刊
- **MODELS** (ACM/IEEE International Conference on Model Driven Engineering Languages and Systems)
- **SoSyM** (Software and Systems Modeling)
- **MODELSWARD** (International Conference on Model-Driven Engineering and Software Development)
- **MoDELS Companion** (MODELS会议的companion proceedings)

#### 需求工程会议
- **RE** (Requirements Engineering Conference)
- **REW** (Requirements Engineering Workshops)

#### AI/ML相关会议
- **NeurIPS** (Neural Information Processing Systems)
- **ICML** (International Conference on Machine Learning)
- **AAAI** (Association for the Advancement of Artificial Intelligence)
- **ICLR** (International Conference on Learning Representations)

#### 系统工程会议
- **INCOSE** (International Council on Systems Engineering)
- **IEEE ISSE** (IEEE International Symposium on Systems Engineering)

## 已知待探索的工作线索

基于BASELINE.md中提到的相关工作，以下是需要进一步追踪的研究线索：

### 1. 来自MIG论文的线索

| 线索 | 描述 | 优先级 | 检索建议 |
|------|------|--------|---------|
| Chen et al. (2023) 单步建模 | MIG的前身工作，MODELS 2023 | 高 | 已在BASELINE.md中，需获取全文 |
| Weyssow et al. (2022) | 预训练语言模型推荐元模型概念 | 中 | 搜索"Weyssow metamodel language model" |
| Burgueño et al. (2021) | NLP自动补全部分领域模型 | 低 | 传统NLP方法，非LLM |
| Saini et al. (2022) | 机器学习增量学习交互式建模 | 低 | 传统ML方法，非LLM |

### 2. 来自TTool-AI论文的线索

| 线索 | 描述 | 优先级 | 检索建议 |
|------|------|--------|---------|
| Cámara et al. (2023) | ChatGPT生成UML类图评估 | 高 | 已在BASELINE.md中，需获取全文 |
| Ahmad et al. (2023) | ChatGPT协作软件架构 | 高 | 已在BASELINE.md中，需获取全文 |
| Chen et al. (2023) 目标模型 | GPT-4创建目标模型 | 中 | 已在BASELINE.md中，需获取全文 |
| Nakagawa & Honiden (2023) | MAPE-K循环目标模型生成 | 中 | 已在BASELINE.md中，需获取全文 |
| Chaaben et al. (2023) | Few-shot prompt learning模型补全 | 中 | 已在BASELINE.md中，需获取全文 |
| Schräder et al. (2022) | AI-based MBSE助手系统 | 低 | 主要是辅助工具，非完全生成 |

### 3. 引用追踪线索

需要对以下高优先级论文进行**前向引用追踪**（谁引用了它们）和**后向引用追踪**（它们引用了谁）：

1. **Cámara et al. (2023)** - ChatGPT UML评估
   - 前向追踪：查找2024-2025年引用该论文的工作
   - 后向追踪：查看其参考文献中的LLM建模工作

2. **Chen et al. (2023)** - 单步领域建模（MIG baseline）
   - 前向追踪：查找后续改进工作
   - 后向追踪：查看其参考文献

3. **Ahmad et al. (2023)** - ChatGPT软件架构
   - 前向追踪：查找相关架构建模工作

### 4. 作者追踪线索

追踪以下活跃研究者的最新工作（2024-2025）：

| 研究者 | 机构 | 已知工作 | 检索建议 |
|--------|------|---------|---------|
| Javier Cámara | University of Málaga | ChatGPT UML评估 | Google Scholar搜索"Javier Cámara LLM modeling" |
| Kua Chen | McGill University | MIG单步建模、目标模型 | 搜索"Kua Chen domain modeling LLM" |
| Yujing Yang | McGill University | MIG | 搜索"Yujing Yang LLM modeling" |
| Gunter Mussbacher | McGill University | MIG | 搜索"Gunter Mussbacher LLM" |
| Ludovic Apvrille | Télécom Paris | TTool-AI | 搜索"Ludovic Apvrille AI modeling" |
| Aamir Ahmad | - | ChatGPT架构 | 搜索"Aamir Ahmad ChatGPT software" |

### 5. 相关研究组/实验室

| 研究组 | 机构 | 研究方向 | 检索建议 |
|--------|------|---------|---------|
| Software Engineering Lab | McGill University | 模型驱动工程、LLM建模 | 查看实验室网站和成员发表 |
| COMET Lab | Télécom Paris | 系统建模、MBSE | 查看Apvrille团队的工作 |
| Software Modeling Group | University of Málaga | UML建模、生成式AI | 查看Cámara团队的工作 |

## 待检索的具体工作

### 高优先级（必须获取）

以下工作已在BASELINE.md中提到，需要获取全文并详细分析：

1. **Cámara, J., et al. (2023)**
   - 标题: On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML
   - 期刊: Software and Systems Modeling, 22(3), 781-793
   - DOI: 待查
   - 重要性: 直接评估ChatGPT生成UML的能力，是重要baseline

2. **Chen, K., Yang, Y., et al. (2023)**
   - 标题: Automated Domain Modeling with Large Language Models: A Comparative Study
   - 会议: MODELS 2023
   - DOI: 待查
   - 重要性: MIG的前身工作，单步建模baseline

3. **Ahmad, A., et al. (2023)**
   - 标题: Towards human-bot collaborative software architecting with ChatGPT
   - 会议: EASE 2023
   - DOI: 待查
   - 重要性: ChatGPT在软件架构中的应用

4. **Chen, B., Chen, K., et al. (2023)**
   - 标题: On the use of GPT-4 for creating goal models: An exploratory study
   - 会议: IEEE REW 2023
   - DOI: 待查
   - 重要性: GPT-4在目标建模中的应用

5. **Chaaben, N., et al. (2023)**
   - 标题: Towards using few-shot prompt learning for automating model completion
   - 会议: ICSE-NIER 2023
   - DOI: 待查
   - 重要性: Few-shot learning在模型补全中的应用

### 中优先级（建议获取）

6. **Nakagawa, T., & Honiden, S. (2023)**
   - 标题: MAPE-K loop-based goal model generation using generative AI
   - 会议: IEEE REW 2023
   - DOI: 待查
   - 重要性: 反馈循环机制在目标模型生成中的应用

7. **Weyssow, M., et al. (2022)**
   - 标题: Recommending metamodel concepts during modeling activities with pre-trained language models
   - 期刊: Software and Systems Modeling, 21(3), 1071-1089
   - DOI: 待查
   - 重要性: 预训练语言模型在建模中的早期应用

### 低优先级（可选）

8. **Schräder, J., et al. (2022)**
   - 标题: Examples of AI-based assistance systems in context of model-based systems engineering
   - 会议: IEEE ISSE 2022
   - DOI: 待查
   - 重要性: AI辅助MBSE工具综述

9. **Aquino, G., et al. (2020)**
   - 标题: A methodological assistant for use case diagrams
   - 会议: MODELSWARD 2020
   - DOI: 待查
   - 重要性: 用例图辅助工具

## 潜在的新工作（2024-2025）

基于研究趋势，以下是可能存在但尚未发现的工作方向：

### 1. LLM + 状态机生成
- **预期关键词**: "LLM state machine generation", "GPT statechart synthesis"
- **预期会议**: MODELS 2024/2025, ASE 2024/2025
- **研究空白**: 目前状态机自动生成的LLM工作较少

### 2. LLM + 形式化验证
- **预期关键词**: "LLM formal verification", "GPT model checking"
- **预期会议**: ICSE 2024/2025, FSE 2024/2025
- **研究空白**: LLM生成的模型缺乏验证

### 3. LLM + 时间自动机
- **预期关键词**: "LLM timed automata", "GPT temporal constraints"
- **预期会议**: FORMATS, CAV, TACAS
- **研究空白**: 时间属性的自动生成

### 4. LLM + 模型修复
- **预期关键词**: "LLM model repair", "GPT automated debugging"
- **预期会议**: ICSE 2024/2025, ASE 2024/2025
- **研究空白**: 基于验证反馈的自动修复

### 5. 多模态LLM + 建模
- **预期关键词**: "multimodal LLM UML", "vision-language model diagram"
- **预期会议**: NeurIPS 2024, ICLR 2025
- **研究空白**: 从图像或草图生成模型

### 6. 领域特定LLM建模
- **预期关键词**: "domain-specific LLM modeling", "control system LLM"
- **预期会议**: MODELS 2024/2025, EMSOFT
- **研究空白**: 针对控制系统的专门建模

## 检索执行计划

### 阶段1：获取已知工作全文（1-2周）

1. 通过学术数据库下载高优先级论文全文
2. 使用`tools/pdf_extractor.py`提取文本
3. 按照CLAUDE.md规范创建论文目录和desc.md
4. 更新BASELINE.md

### 阶段2：引用追踪（1-2周）

1. 对高优先级论文进行前向引用追踪（使用Google Scholar）
2. 对高优先级论文进行后向引用追踪
3. 识别新的相关工作
4. 更新本文档

### 阶段3：系统性检索（2-3周）

1. 在主要学术数据库执行检索式1-5
2. 筛选2023-2025年的相关论文
3. 按优先级排序
4. 获取全文并分析

### 阶段4：作者和研究组追踪（1周）

1. 追踪关键作者的最新工作
2. 查看相关研究组的网站和发表列表
3. 识别未发表的预印本（arXiv）

### 阶段5：整理和总结（1周）

1. 将所有发现的工作整理到BASELINE.md
2. 创建详细的对比表格
3. 分析研究空白和创新点
4. 撰写文献综述

## 检索工具和资源

### 学术搜索引擎
- **Google Scholar**: https://scholar.google.com/
- **Semantic Scholar**: https://www.semanticscholar.org/
- **Connected Papers**: https://www.connectedpapers.com/
- **ResearchGate**: https://www.researchgate.net/

### 引用追踪工具
- Google Scholar的"Cited by"功能
- Semantic Scholar的引用图
- Connected Papers的可视化引用网络

### 预印本服务器
- **arXiv**: https://arxiv.org/ (cs.SE, cs.AI, cs.LG)
- **HAL**: https://hal.science/
- **TechRxiv**: https://www.techrxiv.org/

### 会议论文集
- **DBLP**: https://dblp.org/
- **ACM DL**: https://dl.acm.org/
- **IEEE Xplore**: https://ieeexplore.ieee.org/

## 记录和追踪

### 检索记录模板

每次检索后，记录以下信息：

```markdown
### 检索记录 [日期]

**检索式**: [具体的检索式]
**数据库**: [使用的数据库]
**结果数量**: [初步结果数]
**筛选后数量**: [相关论文数]
**发现的重要工作**:
1. [论文1标题] - [作者] - [会议/期刊] - [年份]
2. [论文2标题] - [作者] - [会议/期刊] - [年份]
...

**备注**: [其他发现或观察]
```

### 论文评估标准

对每篇发现的论文，评估以下维度：

1. **相关性** (1-5分)
   - 5: 直接相关，必须深入研究
   - 4: 高度相关，建议研究
   - 3: 中度相关，可选研究
   - 2: 低度相关，仅供参考
   - 1: 不相关

2. **创新性** (1-5分)
   - 方法是否新颖
   - 是否有独特的技术贡献

3. **实验质量** (1-5分)
   - 实验设计是否严谨
   - 数据集是否充分
   - 对比是否全面

4. **对本研究的价值** (1-5分)
   - 是否可作为baseline
   - 是否提供可借鉴的技术
   - 是否揭示研究空白

## 下一步行动

1. **立即行动**：
   - [ ] 在Google Scholar搜索高优先级论文的完整引用信息
   - [ ] 通过学术数据库下载可获取的论文全文
   - [ ] 对已有的MIG和TTool-AI论文进行引用追踪

2. **本周内**：
   - [ ] 执行检索式1-3，重点关注UML/SysML生成
   - [ ] 追踪关键作者的最新工作
   - [ ] 创建前3篇高优先级论文的desc.md

3. **本月内**：
   - [ ] 完成所有高优先级论文的获取和分析
   - [ ] 执行完整的引用追踪
   - [ ] 更新BASELINE.md，添加新发现的工作

## 更新日志

- 2026-03-05: 创建文档，制定检索策略和执行计划
