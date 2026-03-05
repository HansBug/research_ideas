# Project 1 Baseline工作汇总

本文档整理了Project 1中已收录的、基于LLM生成UML/SysML相关软件模型的baseline工作，并按“状态机生成”与“其他泛UML/SysML生成”分别展示。

## 纳入标准

只要是基于LLM生成泛UML/SysML相关软件模型的工作都算在内，包括但不限于：
- 类图（Class Diagrams）
- 状态机图（State Machine Diagrams）
- 块定义图（Block Definition Diagrams）
- 内部块图（Internal Block Diagrams）
- 用例图（Use Case Diagrams）
- 目标模型（Goal Models）
- 领域模型（Domain Models）

## 已收录的核心Baseline论文

以下论文已完整收录到本项目的baselines目录，包含PDF原文、提取文本和desc.md分析。

### 1) 自然语言→状态机生成相关工作（从零生成）

| 论文 | 年份 | 作者 | 发表会议/期刊 | 输入 | 输出 | 使用的LLM | 主要方法 | 数据集（来源/制作/可获取性） | 主要发现/结果 | 局限性 | 文档路径 |
|------|------|------|--------------|------|------|----------|---------|---------------------------|-------------|--------|---------|
| **Generating SysML Behavior Models via Large Language Models: an Empirical Study (llms_emp)** | 2025 | Wang, Y. et al. | Internetware 2025 (ACM) | 自然语言需求描述 | PlantUML格式的SysML行为模型（STM/ACT/SD） | GPT-4、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 | 两阶段框架：Phase-I提示生成（Role+Instruction+Req+Sample+RAG）→Phase-II基于模型检查反馈迭代修复 | **来源**：Google Scholar/CNKI/GitHub收集303个来源（论文/书籍/开源项目）<br>**制作**：按IC/EC筛选后，G_Model将案例统一重建为PlantUML + 需求描述，交叉验证一致性<br>**规模**：107个行为模型（36 ACT/36 STM/35 SD）<br>**可获取**：公开数据集（Google Drive） | • STM语法准确率>98%，STM语义F1≈69.29%<br>• 并发区域缺失是STM主要语义错误<br>• 反馈修复后STM需求一致性修复率≈42.14% | • 语义修复能力有限（尤其并发/层次语义）<br>• 生成时间显著增加（2.72–7.67x）<br>• PlantUML缺少原生SysML语义检查，需大量人工检查 | [baselines/llms_emp/](baselines/llms_emp/) |
| **LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation (fbAssistant)** | 2025 | Vyatkin, V. et al. | IEEE INDIN 2025 | 自然语言控制需求 + 系统I/O接口规范 | 可视化FSM + IEC 61499功能块代码 | LLM（未明确指定具体模型） | 迭代精化框架：NL需求→LLM生成FSM→可视化验证→迭代修改→内置解释器仿真→生成IEC 61499功能块→部署测试 | **来源**：工业自动化案例（气动缸、拾取放置机械手）<br>**制作**：论文未新建公开数据集，基于真实工业系统规范进行工具验证<br>**规模**：2个案例系统（简单+复杂）<br>**可获取**：工具演示视频公开（YouTube），代码仓库未公开 | • 显著减少开发时间<br>• 支持多语言需求（含中文）<br>• 闭环仿真验证有效<br>• 成功部署到实际系统 | • 需少量手动调整<br>• 存在LLM幻觉（无前驱状态、误删动作）<br>• 缺乏形式化验证<br>• 无时间约束支持<br>• 可扩展性未充分验证 | [baselines/fsm-gen-iec-61499/](baselines/fsm-gen-iec-61499/) |
| **Automated Statechart Generation from Natural Language Requirements in Automotive (req)** | 2025 | Kurukuri, L.S.R. | 硕士学位论文，Chalmers/Gothenburg | 自然语言产品功能需求 | Mermaid.js格式状态机 | GPT-3.5、GPT-4、GPT-4o（微调） | NLP特征提取（NER/POS）→合成数据生成→领域特定微调→状态机生成 | **来源**：Volvo Cars的Car Weaver工具，20个产品功能需求<br>**制作**：合成数据生成扩充训练集<br>**规模**：20个真实需求+合成数据，12个测试用例<br>**可获取**：工业专有数据，未公开 | • 微调后GPT-4功能正确性3.52（基础模型2.60）<br>• 可理解性3.75（基础模型2.96）<br>• 简单场景接近人工水平（4.5/5分） | • 复杂场景处理能力不足<br>• 迁移不完整、循环逻辑不清晰<br>• 术语不一致、需求对齐度不足<br>• 数据集规模有限（20个）<br>• 仍需专家验证 | [baselines/req/](baselines/req/) |
| **Exploring How Well Llama3 can Generate State Machines Represented in Umple (umple)** | 2025 | Pathak, P. | 硕士学位论文，University of Ottawa | 自然语言需求描述 | Umple格式状态机 | Llama 3 (8B) | 三种提示工程策略：Zero-shot（完全失败）→One-shot（中等效果）→RAG（最佳效果，使用Nomic嵌入+余弦相似度检索） | **来源**：5个测试系统（Blackjack/Course Section/Credit Card Transaction/Driver License/Hotel Stay）<br>**制作**：论文自行设计的测试系统，包含需求描述和参考状态机<br>**规模**：5个系统，每个系统多次迭代生成<br>**可获取**：论文正文中有详细描述，但未提供独立数据集下载链接 | • RAG方法归一化Levenshtein距离0.07-0.32<br>• Credit Card Transaction表现最佳（0.07）<br>• 提出专用评估指标（ICP/EUCP/归一化Levenshtein距离） | • 仅测试5个简单系统<br>• 使用8B小模型（受本地机器限制）<br>• 未涉及时间约束和守卫条件<br>• 缺乏形式化验证<br>• Umple是小众语言 | [baselines/umple/](baselines/umple/) |
| **System Architects Are not Alone Anymore: Automatic System Modeling with AI (TTool-AI)** | 2024 | Apvrille & Sultan | MODELS 2024 | 自然语言系统规范 | SysML块图、内部块图和状态机图 | GPT-4 | 交互式生成：需求分析→模型生成→迭代优化（知识注入+自动反馈循环，最多20次迭代） | **来源**：3个欧洲项目真实规范（Platooning / Space-based / Automated Braking）<br>**制作**：论文未新建大规模公开数据集，基于真实规范做工具与人工对照实验；同一评分标准评估<br>**可获取**：测试系统、规范与生成模型在GitHub公开（ttool-ai仓库） | • 能生成SysML块图和状态机<br>• 交互式方法有效<br>• 支持TTool工具集成 | • 需要人工迭代<br>• 模型质量不稳定<br>• 缺乏自动验证 | [baselines/ttool-ai/](baselines/ttool-ai/) |
| **Enhancing Finite State Machine Design Automation with LLMs and Prompt Engineering (enhance)** | 2024 | Lin, Q.-K. et al. | IEEE APCCAS 2024 | HDLBits FSM设计问题描述 | SystemVerilog格式的FSM代码 | Claude 3 Opus、GPT-4、GPT-4o | 系统化Markdown格式提示+TOP Patch（To-do-Oriented Prompting）任务导向补丁+CoT多轮对话 | **来源**：HDLBits平台的20个FSM设计问题<br>**制作**：使用公开的HDLBits问题集<br>**可获取**：HDLBits网站（https://hdlbits.01xz.net/） | • Claude 3 Opus单次生成成功率41%（20个问题中11个）<br>• TOP Patch后同步复位成功率从30%→70%<br>• one-hot FSM设计成功率达90% | • 所有模型在one-hot设计上表现较差<br>• 处理真值表和卡诺图时容易出错<br>• 状态数量少但逻辑复杂的FSM容易误解<br>• TOP Patch生成仍需人工设计 | [baselines/enhance/](baselines/enhance/) |
| **LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation** | 2026 | Wu, Y. et al. | arXiv预印本 | FSM配置参数 + 自然语言规范 | Verilog RTL代码 + 测试平台 | GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro等 | 全自动benchmark构建：FSM生成→YAML格式化→NL规范生成→RTL合成 | **来源**：自动化生成，不依赖手工收集语料<br>**制作**：约束随机FSM生成（连通/确定/完备约束）+ LLM生成语义化描述 + 参考RTL与testbench + 多层验证（LLM检查/SAT/人工抽查）<br>**规模**：1000个FSM-to-RTL问题（状态2-16）<br>**可获取**：论文为arXiv公开，desc中未给出独立数据仓库链接 | • 最强模型整体准确率42.3%<br>• 8个状态为性能拐点<br>• SFT提升OOD任务19.4% | • 聚焦FSM→RTL，不是控制系统UML/SysML建模<br>• NL规范由LLM生成，存在传播误差 | [baselines/LLM-FSM/](baselines/LLM-FSM/) |

#### 数据集与代码可获取性分析

| 论文 | 数据集可获取性 | 代码可获取性 | 数据集规模 | 数据集链接/获取方式 | 代码链接/获取方式 | 与控制系统的相关性 | 推荐优先级 |
|------|--------------|------------|-----------|-------------------|-----------------|------------------|----------|
| **llms_emp** | ✅ 可立即获取 | ❌ 未公开 | 107个案例（36 STM/36 ACT/35 SD） | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) | 需自行复现 | ⭐⭐⭐ 通用SysML行为模型，包含状态机 | **高** |
| **TTool-AI** | ✅ 可立即获取 | ✅ 可立即获取 | 3个系统（Platooning/Space-based/Automated Braking） | [GitHub ttool-ai](https://github.com/zebradile/ttool-ai) | [GitHub ttool-ai](https://github.com/zebradile/ttool-ai) | ⭐⭐⭐⭐ 包含自动驾驶和航空系统，与控制系统高度相关 | **最高** |
| **enhance** | ✅ 可访问 | ❌ 未公开 | 20个FSM设计问题 | [HDLBits平台](https://hdlbits.01xz.net/) | 需自行复现 | ⭐⭐ 硬件FSM设计，偏向数字电路 | 中 |
| **umple** | ⚠️ 部分可获取 | ❌ 未公开 | 5个系统（Blackjack等） | 论文中有详细描述，需自行构建 | 需自行复现 | ⭐ 通用状态机，非控制系统领域 | 低 |
| **fbAssistant** | ⚠️ 部分可获取 | ⚠️ 仅演示视频 | 2个案例（气动缸、拾取放置机械手） | 论文中详细描述，需根据描述复现 | [YouTube演示](https://www.youtube.com/live/aR20KBmZnA4?si=wxyMOcAX4tirRgQf) | ⭐⭐⭐⭐⭐ 工业自动化控制系统，IEC 61499标准 | 高 |
| **req** | ❌ 未公开 | ❌ 未公开 | 20个需求 | Volvo Cars专有数据，需联系作者 | Volvo Cars内部环境 | ⭐⭐⭐⭐ 汽车控制系统 | 低（无法获取） |
| **LLM-FSM** | ❌ 未公开 | ❌ 未公开 | 1000个FSM-to-RTL问题 | 需关注后续发布或联系作者 | 需关注后续发布或联系作者 | ⭐⭐ RTL代码生成，偏向硬件设计 | 中（待发布） |

**数据集特点分析**：

1. **规模对比**：
   - 最大规模：LLM-FSM（1000个，但未公开）
   - 中等规模：llms_emp（107个，可获取）
   - 小规模：TTool-AI（3个）、fbAssistant（2个）、umple（5个）、enhance（20个）、req（20个）

2. **领域分布**：
   - **控制系统相关**：TTool-AI（自动驾驶/航空）、fbAssistant（工业自动化）、req（汽车）
   - **通用建模**：llms_emp（SysML）、umple（通用状态机）
   - **硬件设计**：enhance（HDL）、LLM-FSM（RTL）

3. **可获取性统计**：
   - 数据集可立即获取：3篇（llms_emp、TTool-AI、enhance）
   - 代码可立即获取：1篇（TTool-AI）
   - 完全未公开：2篇（req、LLM-FSM）
   - 部分可获取：2篇（umple、fbAssistant）

**针对Project 1的建议**：

根据你的研究内容（基于控制系统软件需求的LLM状态机结构化建模，关注时间自动机、形式化验证、时间约束），推荐以下数据集入手顺序：

**第一优先级：TTool-AI数据集** ⭐⭐⭐⭐⭐
- **理由**：
  - 代码和数据均可立即获取，可快速启动实验
  - 包含真实控制系统案例（自动驾驶Platooning、航空Automated Braking）
  - 生成SysML状态机图，与你的研究目标一致
  - 有完整的工具链（TTool），支持形式化验证
  - 案例包含安全关键系统，适合研究时间约束和安全性质
- **建议用途**：
  - 作为初始实验平台，验证你的方法框架
  - 分析现有方法在控制系统上的不足（特别是时间约束缺失）
  - 扩展TTool-AI的能力，添加时间自动机生成

**第二优先级：llms_emp数据集** ⭐⭐⭐⭐
- **理由**：
  - 数据集规模最大（107个案例），可立即获取
  - 包含状态机图（STM），与你的研究直接相关
  - 已有模型检查反馈机制，可借鉴其验证方法
  - 数据集质量高（经过交叉验证）
- **建议用途**：
  - 作为大规模实验的数据基础
  - 研究语义修复和迭代优化方法
  - 对比你的方法与现有方法在语义准确性上的提升
- **局限性**：
  - 使用PlantUML格式，需要转换为时间自动机格式
  - 缺少时间约束，需要你自行添加或扩展

**第三优先级：fbAssistant案例** ⭐⭐⭐⭐
- **理由**：
  - 工业自动化控制系统，与你的目标领域高度契合
  - IEC 61499标准，工业界广泛使用
  - 虽然数据集小，但案例质量高、真实性强
- **建议用途**：
  - 作为工业验证案例
  - 研究IEC 61499标准下的状态机建模
  - 与fbAssistant工具对比，展示你的方法优势
- **局限性**：
  - 数据集规模小（仅2个案例）
  - 需要根据论文描述自行复现
  - 工具未完全公开

**第四优先级：enhance数据集（HDLBits）** ⭐⭐⭐
- **理由**：
  - 数据集可访问，20个FSM设计问题
  - 有明确的评估标准（功能正确性）
- **建议用途**：
  - 作为补充实验，验证方法在硬件FSM上的泛化能力
- **局限性**：
  - 偏向硬件设计，与控制系统软件需求有差异
  - 缺少时间约束和安全性质

**不推荐立即使用**：
- **req**：数据集未公开，无法获取
- **LLM-FSM**：数据集未公开，需等待后续发布
- **umple**：规模小，非控制系统领域，需自行构建

**实施路线图**：

1. **阶段1（1-2个月）**：使用TTool-AI数据集
   - 快速搭建实验框架
   - 验证基本方法可行性
   - 识别时间约束建模的关键挑战

2. **阶段2（2-3个月）**：扩展到llms_emp数据集
   - 大规模实验验证
   - 对比现有方法
   - 发表初步成果

3. **阶段3（3-4个月）**：添加fbAssistant案例
   - 工业验证
   - 展示实际应用价值
   - 与工业标准对接

4. **阶段4（可选）**：关注LLM-FSM数据集发布
   - 如果公开，可作为大规模benchmark
   - 验证方法的泛化能力

### 2) 状态机精化/优化相关工作（基于已有模型）

| 论文 | 年份 | 作者 | 发表会议/期刊 | 输入 | 输出 | 使用的LLM | 主要方法 | 数据集（来源/制作/可获取性） | 主要发现/结果 | 局限性 | 文档路径 |
|------|------|------|--------------|------|------|----------|---------|---------------------------|-------------|--------|---------|
| **LLM-based Iterative Refinement of FSM with STPA Controller Constraints (STPA)** | 2025 | King, A. & Vyatkin, V. | IEEE ETFA 2025 | 初始FSM + STPA控制器约束 | 优化后的FSM + IEC 61499代码 | OpenAI GPT（通过fbAssistant） | STPA控制器约束作为提示→递归迭代优化（每个约束20次）→IEC 61499代码生成 | **来源**：pick-and-place机器案例，STPA分析生成33个UCA和11个控制器约束<br>**制作**：手工进行STPA分析<br>**规模**：9个约束×20次迭代+1组组合约束×10次=190次迭代<br>**可获取**：未公开，建议联系作者 | • 9组测试中1组成功（约束C-7）<br>• 成功修复工件掉落问题<br>• 第11次迭代达到最佳状态后保持稳定 | • 成功率低（10%）<br>• 状态漂移严重<br>• 引入不必要变量<br>• 过度假设互补行为<br>• 约束描述不完整<br>• 语言不一致 | [baselines/STPA/](baselines/STPA/) |
| **State Diagram Extension and Test Case Generation Based on LLMs for Safety Testing (safety)** | 2024 | Su, Q. et al. | IEEE ISSREW 2024 | 基本状态图 + 航空安全准则 | 扩展的安全状态图 + 测试用例 | Qwen2-72B-Instruct（微调） | 安全准则提取（DO-178C+ARP 4754A）→LLM状态图扩展→边优先深度遍历生成测试路径→LLM优化遗传算法生成测试数据 | **来源**：航空高度控制系统案例+在线爬取的机载软件需求<br>**制作**：从航空标准提取4类25项安全准则<br>**可获取**：未提供公开数据集，建议联系作者 | • 与经典遗传算法相比平均执行轮数减少90%<br>• 与6种改进遗传算法相比平均迭代次数减少77.32%<br>• LLM优化策略可增强其他改进遗传算法 | • 安全准则覆盖有限（仅4类25项）<br>• 测试路径生成未考虑上下文关系<br>• 仅在单个航空案例上验证<br>• 依赖大规模LLM（Qwen2-72B）<br>• 未提供与人工扩展方法的对比 | [baselines/safety/](baselines/safety/) |

### 3) 其他泛UML/SysML生成工作

| 论文 | 年份 | 作者 | 发表会议/期刊 | 生成的模型类型 | 使用的LLM | 主要方法 | 数据集（来源/制作/可获取性） | 主要发现/结果 | 局限性 | 文档路径 |
|------|------|------|--------------|--------------|----------|---------|---------------------------|-------------|--------|---------|
| **Multi-step Iterative Automated Domain Modeling with Large Language Models (MIG)** | 2024 | Yang, Y. et al. | MODELS 2024 | 领域模型（类图） | GPT-4 | 多步迭代生成：任务分解→Few-shot学习→迭代优化 | **来源**：未明确说明<br>**可获取**：未提供公开数据集 | • 相比单步方法提升显著<br>• Few-shot学习有效<br>• 迭代优化能改进质量 | • 仍存在元素缺失<br>• 关系识别不完善<br>• 需要多轮迭代 | [baselines/MIG/](baselines/MIG/) |
| **Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition (I4.0)** | 2025 | Otto, B. et al. | IEEE WFCS 2025 | 状态图图像→状态机表示→C++代码+测试 | gpt-4o、claude-3-sonnet、Llama-3.2-11b | 三步流水线：裁剪状态图图像→LLM识别（零样本/少样本）→模板化代码和测试生成 | **来源**：IEC 61158（PROFINET）80个状态图+IEC 62541（OPC UA）15个状态图<br>**制作**：从PDF规范文档手工裁剪状态图<br>**可获取**：Zenodo（https://zenodo.org/records/14730727），图样经打乱处理 | • PROFINET识别准确率63%（411/657条边）<br>• OPC UA识别准确率45%（57/127条边）<br>• 自动生成7017+1614行代码和3934+1034行测试 | • 裁剪步骤需手工完成<br>• LLM遗漏边（37%）或产生幻觉边（14%）<br>• 少样本学习可能"压倒"模型<br>• 复杂图样（边标签、多重边）识别率下降<br>• 端到端生成质量不佳 | [baselines/I4.0/](baselines/I4.0/) |

## 相关工作对比表

以下是从MIG和TTool-AI论文的相关工作中提取的其他基于LLM的建模工作：

| 论文 | 年份 | 作者 | 发表会议/期刊 | 生成的模型类型 | 使用的LLM | 主要方法 | 主要发现/结果 | 局限性 | 来源论文 |
|------|------|------|--------------|--------------|----------|---------|-------------|--------|---------|
| **Automated Domain Modeling with Large Language Models: A Comparative Study** | 2023 | Chen, K., Yang, Y. et al. | MODELS 2023 | 领域模型（类、属性、关系） | LLM（未明确指定） | 单步方式生成完整领域模型 | 能够从文本描述自动生成领域模型 | • 大量建模元素缺失<br>• 无法识别高级模式（如player-role）<br>• 关系识别准确率低 | MIG（作为baseline） |
| **On the use of GPT-4 for creating goal models: An exploratory study** | 2023 | Chen, B., Chen, K. et al. | IEEE REW 2023 | 目标导向模型（Goal Models） | GPT-4 | 探索性研究，评估GPT-4生成目标模型的能力 | • 提示中包含语法信息有价值<br>• 领域信息数量影响有限 | • 生成的元素可能不正确或过于通用<br>• 不利于突出利益相关者之间的冲突 | MIG（前身工作） |
| **On the Assessment of Generative AI in Modeling Tasks: An Experience Report with ChatGPT and UML** | 2023 | Cámara et al. | Software and Systems Modeling 22(3) | UML类图 | ChatGPT | 交互模式，构建带OCL约束的UML类图 | • 能频繁生成语法正确的模型<br>• 语法错误率低 | • 语义准确性不稳定（特别是类之间的关系）<br>• 需要大量人工迭代查询来改进输出<br>• 用户工作量仍然很大 | MIG、TTool-AI |
| **Towards using few-shot prompt learning for automating model completion** | 2023 | Chaaben et al. | ICSE-NIER 2023 | 模型补全 | GPT-3 | Few-shot prompt learning进行模型补全 | 能够补全部分模型 | • 缺乏领域问题规范<br>• 严重依赖已有的部分模型<br>• 不包括属性、多重性、类的类型或关系<br>• 无法从零开始生成完整模型 | MIG |
| **Towards human-bot collaborative software architecting with ChatGPT** | 2023 | Ahmad et al. | EASE 2023 | 需求、UML模型、架构评估 | ChatGPT | 使用ChatGPT进行软件架构任务 | ChatGPT作为软件架构师助手有用 | • 响应变异性问题<br>• 伦理/知识产权问题<br>• 需要人工分析和迭代提问才能收敛到正确架构 | TTool-AI |
| **MAPE-K loop-based goal model generation using generative AI** | 2023 | Nakagawa & Honiden | IEEE REW 2023 | 目标模型（Goal Models） | 生成式AI（未明确指定） | 基于MAPE-K循环生成目标模型 | 通过反馈机制能产生有希望的结果 | 需要反馈和多个提示 | TTool-AI |
| **Recommending metamodel concepts during modeling activities with pre-trained language models** | 2022 | Weyssow et al. | Software and Systems Modeling 21(3) | 元模型概念推荐 | 预训练语言模型 | 推荐元模型概念 | 预训练语言模型在建模任务中有应用潜力 | 仅提供推荐，非完全自动化生成 | MIG |

## 非LLM方法（作为对比参考）

以下是论文中提到的传统方法，虽然不是基于LLM，但作为对比参考有助于理解LLM方法的优势。按年份从新到旧排序：

| 论文 | 年份 | 作者 | 发表会议/期刊 | 输入 | 输出 | 方法类型 | 主要功能 | 主要局限性 | 来源论文 |
|------|------|------|--------------|------|------|---------|---------|-----------|---------|
| Sketch2process: End-to-end BPMN sketch recognition | 2023 | Schäfer et al. | IEEE TSE, vol. 49, no. 4 | 手绘BPMN草图图像 | 形式化BPMN模型 | 基于神经网络的端到端识别 | 将手绘业务流程图转换为形式化模型 | 在业务流程图上训练，泛化能力有限，无法识别工业状态图 | I4.0 |
| Machine Learning-Based Incremental Learning in Interactive Domain Modelling | 2022 | Saini et al. | MODELS 2022 | 用户交互+部分模型 | 领域模型 | 机器学习增量学习 | 交互式领域建模 | 需要监督训练和用户交互 | MIG |
| An NLP-based architecture for the autocompletion of partial domain models | 2021 | Burgueño et al. | CAiSE 2021 | 部分领域模型 | 补全的领域模型 | NLP词嵌入模型 | 自动补全部分模型 | 需要部分模型输入，表达能力有限 | MIG |
| Automated Grading of Class Diagrams | 2019 | Bian et al. | MODELS-C 2019 | 学生生成的类图 | 评分和反馈 | 自动评分方法 | 评估类图质量（精确率、召回率、F1-score） | 评估工具而非生成工具 | MIG |
| A first step towards AI for MBSE: Generating a part of SysML models from text using AI | 2019 | Chami et al. | 未明确 | 文本需求 | SysML用例图和块图 | 基于传统NLP的框架 | 从文本需求生成SysML模型 | 使用传统NLP而非LLM，能力有限 | TTool-AI |
| ARSENAL: automatic requirements specification extraction from natural language | 2016 | Ghosh et al. | NASA NFM 2016 | 自然语言需求 | 形式化需求规范 | 最小化输入语言限制 | 从自然语言提取需求规范 | 某些自然语言表达仍难以处理 | TTool-AI |
| Automated Extraction of Conceptual Models from User Stories via NLP | 2016 | Robeer et al. | IEEE RE 2016 | 用户故事 | 概念模型 | 基于规则（23个启发式规则） | 从用户故事提取实体和关系 | 规则编写成本高，泛化能力弱 | MIG |
| From requirements to UML models and back | 2014 | Landhäußer et al. | Software Quality Journal, 22:121–149 | 文本需求 | UML模型 | 综合文献综述 | 提供从需求到UML自动生成的历史脉络 | 综述论文，非具体方法 | TTool-AI |
| Cyber-physical components for heterogeneous modelling | 2014 | Zhabelova et al. | IEEE INDIN 2014 | 系统需求和组件规范 | 功能块应用 | 面向对象MVC模式适配 | 为基于组件的自动化提供架构框架 | 架构框架而非自动生成工具 | fsm-gen-iec-61499 |
| From user requirements to UML class diagram | 2012 | Herchi & Ben Abdessalem | arXiv:1211.0713 | 用户需求文本 | UML类图 | 语言规则（名词→实体类型） | 使用简单语言规则提取UML概念 | 规则过于简单，容易误报 | MIG |
| Thematic role based generation of UML models | 2007 | Gelhausen & Tichy | IEEE ICSC 2007 | 真实世界需求 | UML模型 | 基于主题角色 | 从真实世界需求生成UML模型 | 需要对输入语法施加约束或手动预处理 | TTool-AI |
| Methods of object-oriented reactive agents implementation | 2005 | Shalyto et al. | KIMAS 2005 | 系统需求 | 面向对象反应式智能体 | 基于有限自动机 | 将自动机方法与面向对象编程结合 | 方法论而非自动化工具 | fsm-gen-iec-61499 |
| Automata-based programming of reactive multi-agent control systems | 2005 | Yartsev et al. | KIMAS 2005 | 系统需求 | 反应式多智能体控制系统 | 自动机编程 | 自动机方法在控制系统中的应用 | 方法论而非自动化工具 | fsm-gen-iec-61499 |
| Automata theory for multi-agent systems implementation | 2003 | Naumov & Shalyto | IEMC 2003 | 系统需求 | 多智能体系统实现 | 自动机理论 | 为基于自动机的编程奠定理论基础 | 理论基础而非自动化工具 | fsm-gen-iec-61499 |
| Chartware - structured visual programming for industrial logic control | 1996 | Vyatkin et al. | Controllers and Control Systems, vol. 3, no. 4 | 工业逻辑控制需求 | 结构化可视化程序 | Chartware方法 | 工业逻辑控制的结构化可视化编程 | 早期方法，自动化程度有限 | fsm-gen-iec-61499 |

## 建模助手工具（非完全自动化生成）

以下工具主要提供建模辅助功能，而非完全自动化生成。按年份从新到旧排序：

| 工具/论文 | 年份 | 作者/厂商 | 会议/期刊 | 输入 | 输出 | 主要功能 | 局限性 | 来源论文 |
|---------|------|---------|---------|------|------|---------|--------|---------|
| AI-based MBSE助手系统 | 2022 | Schräder et al. | IEEE ISSE 2022 | 手绘草图、模型库、自然语言查询 | 形式化SysML模型、设计建议、自然语言响应 | • 草图转换助手<br>• 知识库设计建议<br>• 建模查询聊天机器人 | 辅助性质，非完全自动化生成 | TTool-AI |
| Umple | 2021 | Lethbridge et al. | 开源项目 | Umple建模语言代码 | C++、Java等传统编程语言代码 | 开源建模技术，支持UML模型（含状态机）创建，生成传统编程语言代码 | 需要手工编写Umple代码，小众语言 | umple |
| 用例图方法论助手 | 2020 | Aquino et al. | MODELSWARD 2020 | 用户交互和需求描述 | SysML用例图 | 支持SysML用例图设计 | 仅支持用例图，不支持状态机或块图 | TTool-AI |
| Stateflow | - | MathWorks | 商业工具 | 手工绘制的状态机 | 可执行的状态机模型和代码 | 广泛使用的状态机建模和仿真工具 | 需要大量手工工作 | req |
| Yakindu Statechart Tools | - | itemis AG | 商业工具 | 手工定义的状态机 | 状态机模型和代码 | 商业状态机建模工具 | 需要大量手工工作 | req |
| Enterprise Architect | - | Sparx Systems | 商业工具 | 手工创建的模型 | UML/SysML模型 | 企业级建模工具，支持UML和状态机建模 | 需要大量手工工作 | req |

## 自然语言→状态机工作综合分析

### 1. 研究现状概览（2024-2025）

截至2025年，基于LLM的状态机相关研究已成为热点，共收录9篇核心论文，按研究类型分为：
- **从零生成**（7篇）：llms_emp、fbAssistant、req、umple、TTool-AI、enhance、LLM-FSM
- **精化/优化**（2篇）：STPA、safety

**应用领域分布**：
- **工业自动化**：fbAssistant（IEC 61499）、STPA（IEC 61499精化）
- **汽车软件**：req（Volvo Cars）
- **航空航天**：safety（航空高度控制，状态图扩展）
- **硬件设计**：enhance（SystemVerilog HDL）、LLM-FSM（RTL代码）
- **通用建模**：llms_emp（SysML）、TTool-AI（SysML）、umple（Umple）

**技术路线分类**：
1. **端到端生成**：llms_emp、TTool-AI、req、umple
2. **多步流水线**：enhance（提示工程→HDL生成）
3. **迭代优化**：fbAssistant（从零生成+迭代）、STPA（精化）、safety（扩展）
4. **基准测试**：LLM-FSM（自动化benchmark构建）

### 2. 主要方法与技术创新

#### 2.1 提示工程策略

**Zero-shot vs Few-shot vs RAG**：
- umple论文系统比较了三种策略，RAG方法表现最佳（Levenshtein距离0.07-0.32）
- enhance论文提出TOP Patch（To-do-Oriented Prompting），将成功率从30%提升至70%

**提示词设计原则**（综合多篇论文）：
- 使用与现有模型一致的术语和变量名（STPA论文）
- 完整描述组件行为，避免给LLM留下假设空间（STPA论文）
- 系统化Markdown格式提示，包含规格说明、I/O表格、状态转换表（enhance论文）
- 组合多个相关约束比单独使用更有效（STPA论文）

#### 2.2 迭代优化方法

**从零生成中的迭代策略**：
- **反馈驱动迭代**（llms_emp）：基于模型检查反馈，STM需求一致性修复率42.14%
- **人工引导迭代**（fbAssistant）：可视化验证+人工调整，成功部署到实际系统

**精化/优化中的迭代策略**：
- **递归迭代**（STPA）：基于前一次迭代结果，成功率低（10%），易导致状态漂移
- **LLM优化遗传算法**（safety）：平均执行轮数减少90%

**迭代失败模式**（STPA论文识别）：
1. 状态漂移：FSM逐渐偏离原始结构，关键状态被移除
2. 引入不必要变量：LLM创建新变量而非使用现有传感器输入
3. 过度假设：对未明确定义的行为做出错误假设
4. 约束描述不完整：给LLM留下过多假设空间

#### 2.3 数据集构建方法

**数据来源多样化**：
- **公开数据集**：llms_emp（107个SysML模型）、enhance（HDLBits 20个问题）
- **工业案例**：req（Volvo Cars 20个需求）、fbAssistant（工业自动化案例）
- **标准规范**：I4.0（IEC 61158/62541共95个状态图）
- **自动生成**：LLM-FSM（1000个FSM-to-RTL问题）

**合成数据生成**：
- req论文：受控随机化，从有限真实数据生成大量训练样本
- LLM-FSM论文：约束随机FSM生成+LLM生成语义化描述

#### 2.4 评估方法创新

**多维度评估框架**：
- **语法正确性**：llms_emp（STM语法准确率>98%）
- **语义正确性**：llms_emp（STM语义F1≈69.29%）、req（功能正确性3.52/5）
- **可理解性**：req（3.75/5）
- **需求对齐度**：req（2.75/5）
- **变更分类**：STPA（正面/负面/中性变更）

**专用评估指标**：
- umple：ICP（Incorrect Component Penalty）、EUCP（Extra/Unnecessary Component Penalty）、归一化Levenshtein距离

### 3. 共同挑战与局限性

#### 3.1 语义理解不足

**并发与层次语义**：
- llms_emp：并发区域缺失是STM主要语义错误
- req：嵌套迁移、条件逻辑处理能力不足

**复杂逻辑处理**：
- req：循环逻辑不清晰，迁移不完整
- enhance：状态数量少但逻辑复杂的FSM容易误解
- LLM-FSM：8个状态为性能拐点，最强模型整体准确率仅42.3%

#### 3.2 形式化验证缺失

**验证能力有限**：
- 大多数从零生成工作缺乏形式化验证（TTool-AI、fbAssistant、req）
- llms_emp使用PlantUML，缺少原生SysML语义检查
- fbAssistant仅使用闭环仿真验证，未集成形式化验证

**时间约束支持不足**：
- fbAssistant、req均未涉及时间约束
- 缺乏时间自动机的生成和验证能力

**精化/优化工作的验证**：
- STPA：缺乏自动化验证，依赖人工评估变更
- safety：使用UPPAAL验证扩展状态图的完整性和一致性（唯一使用形式化验证的工作）

#### 3.3 数据集规模与质量

**规模有限**：
- req：仅20个真实需求（从零生成）
- umple：仅5个测试系统（从零生成）
- safety：仅1个航空案例（状态图扩展）
- STPA：仅1个pick-and-place案例（FSM精化）

**领域泛化能力未知**：
- 大多数工作仅在单一领域验证
- 跨领域适用性有待研究

#### 3.4 成功率与可靠性

**成功率差异巨大**：
- STPA：10%（1/10）（FSM精化）
- enhance：41%（Claude 3 Opus单次生成，从零生成）
- req：简单场景接近人工水平，复杂场景表现较差（从零生成）

**需要人工干预**：
- 所有工作都强调仍需专家验证和调整
- 完全自动化尚不可行

### 4. 技术演进趋势

#### 4.1 从单步到多步

**早期（2023-2024）**：
- 单步端到端生成（Chen et al. 2023, Cámara et al. 2023）
- 需要大量人工迭代

**当前（2024-2025）**：
- 多步流水线（I4.0：识别→生成，在"其他泛UML/SysML生成工作"中）
- 迭代优化框架（llms_emp、fbAssistant：从零生成+迭代；STPA：精化）
- 分阶段生成（safety：扩展→测试生成）

#### 4.2 从通用到领域特定

**通用LLM**：
- 早期使用通用LLM（GPT-4、ChatGPT）
- 性能不稳定，需要大量提示工程

**领域微调**：
- req：在汽车领域数据上微调GPT-4，功能正确性提升35%（从零生成）
- safety：微调Qwen2-72B-Instruct，执行轮数减少90%（状态图扩展）

**领域知识注入**：
- safety：从航空标准提取安全准则（状态图扩展）
- STPA：使用STPA控制器约束作为提示（FSM精化）

#### 4.3 从生成到验证

**早期**：仅关注生成，缺乏验证

**当前**：
- llms_emp：集成模型检查反馈
- fbAssistant：内置解释器仿真
- I4.0：基于覆盖准则的测试生成

**未来方向**：形式化验证集成（UPPAAL、模型检查）

#### 4.4 从文本到多模态

**文本输入**：大多数工作基于自然语言需求

**多模态输入的探索**（在"其他泛UML/SysML生成工作"中）：
- I4.0：状态图图像识别（工业通信协议规范）
- Koziolek & Koziolek (2024)：P&ID图像识别

### 5. 与本研究的关系

#### 5.1 研究空白确认

**时间约束建模**（最大空白）：
- 所有从零生成论文均未充分支持时间自动机
- 精化/优化工作也未涉及时间约束
- 缺乏时钟约束和不变式的生成能力
- **本研究创新点**：显式建模时间约束，支持时间自动机

**形式化验证集成**：
- 大多数工作缺乏与UPPAAL等工具的深度集成
- **本研究创新点**：构建"生成-验证-修复"完整闭环

**自动修复机制**：
- 现有迭代方法成功率低（STPA 10%）或依赖人工（fbAssistant）
- **本研究创新点**：基于验证反馈的自动修复方法

#### 5.2 可借鉴的技术

**提示工程**：
- TOP Patch任务导向提示（enhance）
- STPA约束作为系统化提示来源（STPA）
- 组合约束策略（STPA）

**数据增强**：
- 合成数据生成（req、LLM-FSM）
- 受控随机化方法（req）

**评估方法**：
- 变更分类评估（STPA）
- 多维度评估框架（req）
- 专用评估指标（umple）

**迭代策略**：
- 反馈驱动迭代（llms_emp）
- 可视化验证+人工引导（fbAssistant）

#### 5.3 需要改进的方向

**提高成功率**：
- 引入结构约束，防止状态漂移
- 使用形式化约束表达，减少歧义
- 设计非递归迭代策略

**增强验证能力**：
- 集成UPPAAL等模型检查工具
- 自动生成验证性质
- 使用反例指导修复

**扩展数据集**：
- 构建更大规模的控制系统需求数据集
- 涵盖多个领域（BSN、CARA、Elevator等）
- 包含时间约束和守卫条件

**支持时间约束**：
- 扩展方法以支持时间自动机
- 生成时钟约束和不变式
- 验证时序性质（LTL/CTL）

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
   - **更新（2025）**：fbAssistant填补了工业自动化FSM生成的空白，提供了迭代精化和IEC 61499代码生成能力
   - **更新（2026）**：LLM-FSM填补了FSM推理评估的空白，但仅关注硬件RTL生成，控制系统软件状态机建模仍是空白
2. **形式化验证集成**：所有工作都缺乏与形式化验证工具的集成
   - **更新（2025）**：fbAssistant仅使用闭环仿真验证，未集成形式化验证（计划未来集成）
   - **更新（2026）**：LLM-FSM使用SAT求解器进行等价性检查，但未涉及时序逻辑性质验证和模型检查
3. **自动修复机制**：没有工作提出基于验证反馈的自动修复方法
   - **更新（2025）**：fbAssistant支持迭代精化，但依赖人工反馈，无自动修复
4. **时间属性处理**：缺乏对时间约束和时间自动机的支持
   - **更新（2025）**：fbAssistant未涉及时间约束
5. **完整闭环**：缺乏"生成-验证-修复"的完整自动化闭环
   - **更新（2025）**：fbAssistant提供"生成-仿真-迭代"闭环，但验证和修复环节需人工参与

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

- 2026-03-05: 重构"非LLM方法"和"建模助手工具"表格：
  - 添加"输入"、"输出"、"主要功能"等列，与LLM方法表格保持一致
  - 从所有desc.md中提取15个非LLM方法（1996-2023）
  - 从所有desc.md中提取6个建模助手工具
  - 按年份从新到旧排序
- 2026-03-05: 将I4.0论文从状态机生成表格移至"其他泛UML/SysML生成工作"表格（输入是图像而非文本）
- 2026-03-05: 添加4篇新论文到状态机生成表格（自然语言→状态机）：
  - enhance (Lin et al. 2024)：FSM HDL设计自动化，TOP Patch提示工程
  - safety (Su et al. 2024)：航空安全状态图扩展与测试生成
  - req (Kurukuri 2025)：汽车软件需求自动状态机生成（Volvo Cars案例）
  - STPA (King & Vyatkin 2025)：STPA约束驱动的FSM迭代优化
- 2026-03-05: 添加I4.0论文到"其他泛UML/SysML生成工作"表格（图像→状态机）
- 2026-03-05: 添加"自然语言→状态机工作综合分析"章节，系统总结9篇自然语言→状态机论文的方法、挑战和趋势
- 2026-03-05: 添加"针对控制系统状态机建模的学术建议"章节，明确研究方向和创新点
- 2026-03-05: 添加umple论文（2025），Llama3生成Umple状态机的硕士论文，系统比较Zero-shot/One-shot/RAG三种方法
- 2026-03-05: 添加fsm-gen-iec-61499论文（2025），基于LLM的工业自动化FSM迭代精化与IEC 61499代码生成
- 2026-03-05: 添加LLM-FSM论文（2026），首个针对FSM推理的自动化benchmark
- 2026-03-05: 重新整理，仅保留从MIG和TTool-AI相关工作中提取的基于LLM的建模工作

## 针对控制系统状态机建模的学术建议

### 1. 控制系统的特殊性定义

基于已收录论文的分析，控制系统相较于通用软件系统具有以下特殊性：

#### 1.1 安全关键性（Safety-Critical）

**特征**：
- 失效可能导致人员伤亡、设备损坏或任务失败（safety论文）
- 需要满足严格的安全标准（DO-178C、ARP 4754A、ISO 26262、IEC 61499）
- 必须进行系统化的危害分析（STPA论文）

**对建模的影响**：
- 需要生成安全状态和故障处理逻辑（safety论文：DataValidation、FaultDiagnosis状态）
- 必须满足控制器约束（STPA论文：11个控制器约束）
- 需要形式化验证以证明安全性质

#### 1.2 实时性与时间约束（Real-Time）

**特征**：
- 必须在规定时间内响应（fbAssistant论文：气动缸控制）
- 包含时间触发的状态迁移（safety论文：时序约束）
- 需要处理超时和时间窗口（STPA论文：提供过早/过晚、时间过长/过短）

**对建模的影响**：
- 需要时间自动机表示（时钟变量、时钟约束、不变式）
- 必须验证时序性质（LTL/CTL）
- 当前所有论文均未充分支持时间约束

#### 1.3 物理交互与传感器/执行器

**特征**：
- 与物理世界交互（I4.0论文：pick-and-place机器）
- 依赖传感器输入和执行器输出（STPA论文：4个执行器、多个传感器）
- 需要处理传感器噪声和执行器故障

**对建模的影响**：
- 状态迁移依赖传感器输入（STPA论文：s0, s1, s2, s3传感器）
- 动作对应执行器命令（STPA论文：vextend、turn_vacuum_on）
- 需要建模故障模式和容错机制

#### 1.4 并发与分布式

**特征**：
- 多个控制器并发执行（IEC 61499分布式控制）
- 需要协调多个执行器（I4.0论文：2个水平+1个垂直执行器）
- 存在通信延迟和同步问题

**对建模的影响**：
- 需要并发状态机表示（llms_emp论文：并发区域）
- 必须处理同步和互斥
- 当前LLM在并发语义上表现较差（llms_emp论文）

#### 1.5 领域特定知识

**特征**：
- 需要领域专家知识（req论文：Volvo Cars专家评审）
- 使用领域特定术语（I4.0论文：PROFINET、OPC UA）
- 遵循领域标准和规范（IEC 61499、IEC 61158、IEC 62541）

**对建模的影响**：
- 需要领域特定微调（req论文：汽车领域微调）
- 提示词应使用领域术语（STPA论文：语言一致性）
- 需要注入领域知识（safety论文：航空安全准则）

### 2. 控制系统状态机的特殊性

相较于主流状态机（如UML状态机、业务流程状态机），控制系统状态机具有以下特殊性：

#### 2.1 守卫条件的复杂性

**主流状态机**：
- 守卫条件通常是简单的布尔表达式
- 主要基于内部变量

**控制系统状态机**：
- 守卫条件依赖传感器输入（物理世界状态）
- 包含时间约束（时钟比较）
- 需要处理传感器不确定性
- 示例（STPA论文）：`s0 && !s1 && !s2 && !s3`（托盘位置传感器组合）

**挑战**：
- LLM容易引入不必要的新变量（STPA论文：aboveTray、vacantTray）
- LLM难以正确理解传感器组合逻辑

#### 2.2 动作的物理意义

**主流状态机**：
- 动作通常是软件操作（赋值、函数调用）
- 执行时间可忽略

**控制系统状态机**：
- 动作对应物理执行器命令（vextend、turn_vacuum_on）
- 执行需要时间（垂直执行器伸展需要时间）
- 动作有物理约束（不能同时伸展和收回）
- 示例（STPA论文）：垂直执行器必须完全伸展后才能释放工件

**挑战**：
- LLM容易过度假设互补行为（STPA论文：假设"关闭真空"应在所有其他情况下提供）
- LLM难以理解动作的物理约束和时序

#### 2.3 状态的物理对应

**主流状态机**：
- 状态是抽象的软件状态
- 状态数量可以很多

**控制系统状态机**：
- 状态对应物理系统的模式（safety论文：Climbing、Descending、Holding）
- 状态数量通常较少但逻辑复杂（enhance论文：状态数量少但逻辑复杂的FSM容易误解）
- 状态有物理意义和安全约束

**挑战**：
- LLM容易发生状态漂移（STPA论文：关键状态EXT_H3被移除）
- LLM难以理解状态的物理意义

#### 2.4 时间约束的普遍性

**主流状态机**：
- 时间约束较少
- 主要是超时处理

**控制系统状态机**：
- 时间约束普遍存在（最小/最大停留时间、时间窗口）
- 需要时间自动机表示
- 必须验证时序性质

**挑战**：
- 当前所有论文均未充分支持时间约束
- 这是最大的研究空白

#### 2.5 安全性质的关键性

**主流状态机**：
- 主要关注功能正确性
- 活性性质（最终会到达某状态）

**控制系统状态机**：
- 安全性质至关重要（永远不会到达危险状态）
- 需要满足控制器约束（STPA论文：11个约束）
- 必须通过形式化验证

**挑战**：
- 大多数工作缺乏形式化验证
- 需要自动生成验证性质

### 3. 研究方向建议

基于上述分析，针对"控制系统的基于LLM的状态机建模"，建议以下研究方向：

#### 3.1 核心创新方向

**方向1：时间约束建模与验证**

**问题**：当前所有论文均未充分支持时间自动机

**建议**：
- 扩展LLM生成方法以支持时钟变量、时钟约束和不变式
- 设计专门的提示工程策略，引导LLM生成时间约束
- 集成UPPAAL等时间自动机验证工具
- 自动生成时序性质（LTL/CTL）并验证

**技术路线**：
1. 从需求中识别时间相关的关键词（"within X seconds"、"after Y minutes"）
2. 使用LLM生成时钟变量和约束
3. 将生成的时间自动机转换为UPPAAL格式
4. 使用模型检查验证时序性质
5. 基于反例进行迭代修复

**方向2：形式化验证驱动的生成-验证-修复闭环**

**问题**：大多数工作缺乏形式化验证，迭代修复成功率低

**建议**：
- 构建完整的"生成-验证-修复"自动化闭环
- 使用模型检查反馈指导LLM修复
- 设计基于反例的提示策略
- 引入结构约束防止状态漂移

**技术路线**：
1. LLM生成初始状态机
2. 自动生成验证性质（基于STPA约束或需求）
3. 使用UPPAAL进行模型检查
4. 如果验证失败，提取反例
5. 将反例转换为LLM可理解的提示
6. LLM基于反例修复状态机
7. 重复步骤2-6直到验证通过或达到最大迭代次数

**方向3：领域知识注入与安全约束整合**

**问题**：通用LLM缺乏控制系统特定知识

**建议**：
- 系统化地从安全标准提取约束（扩展safety论文的方法）
- 使用STPA等危害分析方法生成控制器约束（扩展STPA论文的方法）
- 设计领域特定的微调策略（扩展req论文的方法）
- 构建控制系统状态机的知识库

**技术路线**：
1. 从DO-178C、ISO 26262等标准提取安全准则
2. 对目标系统进行STPA分析，生成控制器约束
3. 将安全准则和控制器约束转换为LLM提示
4. 在控制系统需求数据集上微调LLM
5. 使用知识库增强LLM的领域理解

#### 3.2 技术改进方向

**方向4：防止状态漂移的结构保持机制**

**问题**：STPA论文发现递归迭代容易导致状态漂移

**建议**：
- 引入结构约束，限制LLM的修改范围
- 设计锚点状态，保护关键状态不被移除
- 使用非递归迭代策略（基于原始FSM而非前一次迭代结果）
- 引入结构相似度度量，监控状态漂移

**方向5：传感器/执行器语义理解**

**问题**：LLM容易引入不必要变量，难以理解物理约束

**建议**：
- 在提示中明确定义传感器输入和执行器输出
- 使用领域本体（ontology）描述传感器/执行器关系
- 设计专门的提示模板，引导LLM使用现有变量
- 引入物理约束检查（如互斥约束）

**方向6：并发与层次语义支持**

**问题**：llms_emp论文发现并发区域缺失是主要语义错误

**建议**：
- 扩展方法以支持层次化状态机（复合状态、子状态机）
- 支持并发区域和同步机制
- 设计专门的提示策略，引导LLM生成并发结构
- 使用形式化方法验证并发正确性

#### 3.3 评估与基准方向

**方向7：构建控制系统状态机生成基准**

**问题**：缺乏统一的评估基准和数据集

**建议**：
- 构建大规模控制系统需求数据集（扩展现有101条需求）
- 涵盖多个领域（工业自动化、汽车、航空航天、嵌入式系统）
- 包含时间约束、守卫条件、安全性质
- 提供参考状态机和验证性质
- 借鉴LLM-FSM论文的自动化benchmark构建方法

**方向8：多维度评估框架**

**问题**：现有评估方法不统一，难以比较

**建议**：
- 综合req论文的多维度评估（功能正确性、可理解性、需求对齐度）
- 引入形式化验证指标（性质满足率、反例数量）
- 使用STPA论文的变更分类方法（正面/负面/中性）
- 评估时间约束的正确性
- 评估安全性质的满足情况

### 4. 实施路线图

**第一阶段（6个月）：基础能力构建**
1. 构建控制系统需求数据集（扩展到200+需求）
2. 实现基础的LLM状态机生成方法
3. 集成UPPAAL验证工具
4. 建立评估框架

**第二阶段（6个月）：时间约束支持**
1. 扩展方法以支持时间自动机
2. 设计时间约束生成的提示策略
3. 实现时序性质的自动生成
4. 验证时间约束的正确性

**第三阶段（6个月）：验证驱动的迭代修复**
1. 实现"生成-验证-修复"闭环
2. 设计基于反例的修复策略
3. 引入结构保持机制
4. 评估迭代修复的效果

**第四阶段（6个月）：领域知识整合**
1. 从安全标准提取约束
2. 集成STPA危害分析
3. 进行领域特定微调
4. 构建知识库

**第五阶段（6个月）：综合评估与优化**
1. 在多个控制系统案例上验证
2. 与人工建模方法对比
3. 优化提示策略和迭代方法
4. 撰写论文和工具发布

### 5. 预期贡献

**理论贡献**：
1. 首个支持时间自动机的LLM状态机生成方法
2. 形式化验证驱动的迭代修复理论框架
3. 控制系统状态机的特殊性系统化分析

**技术贡献**：
1. 完整的"生成-验证-修复"自动化工具链
2. 控制系统需求到时间自动机的端到端方法
3. 基于STPA的安全约束整合方法

**实践贡献**：
1. 大规模控制系统状态机生成基准
2. 多维度评估框架和工具
3. 在真实工业案例上的验证

### 6. 与现有工作的差异化

**相对于llms_emp**：
- 支持时间约束（llms_emp不支持）
- 更强的迭代修复能力（llms_emp修复率42.14%）
- 专注控制系统而非通用SysML

**相对于fbAssistant**：
- 形式化验证而非仅仿真
- 自动修复而非人工调整
- 支持时间约束

**相对于STPA**：
- 更高的成功率（STPA仅10%）
- 防止状态漂移的机制
- 形式化验证集成

**相对于req**：
- 支持时间约束和守卫条件
- 更好的复杂场景处理能力
- 形式化验证而非仅专家评审

**相对于safety**：
- 更系统化的安全约束提取
- 形式化验证而非仅测试生成
- 更广泛的领域适用性

### 7. 潜在挑战与应对

**挑战1：时间约束的复杂性**
- 应对：从简单的时间约束开始（超时、延迟），逐步扩展到复杂的时间窗口和时钟约束

**挑战2：形式化验证的可扩展性**
- 应对：使用抽象和组合验证技术，分解大规模状态机

**挑战3：LLM的不确定性**
- 应对：多次生成取最佳结果，使用集成方法

**挑战4：数据集构建的成本**
- 应对：结合真实需求和合成数据生成，借鉴req和LLM-FSM的方法

**挑战5：工业界接受度**
- 应对：与工业界合作（如Volvo Cars、Flexbridge AB），在真实案例上验证

### 8. 总结

控制系统的基于LLM的状态机建模是一个具有重要理论和实践价值的研究方向。通过系统分析10篇已收录论文，我们识别了以下关键研究空白：

1. **时间约束建模**：当前最大的空白，所有论文均未充分支持
2. **形式化验证集成**：大多数工作缺乏，是提高可靠性的关键
3. **自动修复机制**：现有方法成功率低或依赖人工
4. **控制系统特殊性**：需要系统化地定义和处理

建议的研究方向聚焦于：
- **核心创新**：时间约束建模、验证驱动的闭环、领域知识注入
- **技术改进**：防止状态漂移、传感器/执行器语义、并发支持
- **评估基准**：构建基准数据集、多维度评估框架

通过这些研究方向，本博士研究有望在控制系统状态机建模领域做出重要贡献，填补现有研究空白，推动LLM在安全关键系统中的应用。

## 更新日志

- 2026-03-05: 添加5篇新论文到状态机生成表格：
  - enhance (Lin et al. 2024)：FSM HDL设计自动化，TOP Patch提示工程
  - I4.0 (Otto et al. 2025)：工业4.0状态图图像识别与代码生成
  - safety (Su et al. 2024)：航空安全状态图扩展与测试生成
  - req (Kurukuri 2025)：汽车软件需求自动状态机生成（Volvo Cars案例）
  - STPA (King & Vyatkin 2025)：STPA约束驱动的FSM迭代优化
- 2026-03-05: 添加umple论文（2025），Llama3生成Umple状态机的硕士论文，系统比较Zero-shot/One-shot/RAG三种方法
- 2026-03-05: 添加fsm-gen-iec-61499论文（2025），基于LLM的工业自动化FSM迭代精化与IEC 61499代码生成
- 2026-03-05: 添加LLM-FSM论文（2026），首个针对FSM推理的自动化benchmark
- 2026-03-05: 重新整理，仅保留从MIG和TTool-AI相关工作中提取的基于LLM的建模工作
