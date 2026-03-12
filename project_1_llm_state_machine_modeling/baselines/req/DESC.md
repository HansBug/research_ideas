# 基于人工智能技术的汽车软件工程自然语言需求自动状态机生成 / Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering

## 基本信息

- **标题**：Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering
- **标题（中文）**：基于人工智能技术的汽车软件工程自然语言需求自动状态机生成
- **作者**：Lakshmi Sri Rupa Kurukuri
- **单位**：Chalmers University of Technology, University of Gothenburg
- **发表**：Master's Thesis, 2025
- **导师**：Farnaz Fotrousi (学术导师), Martin Hedström & Mohammad Reza Haghshenas (工业导师, Volvo Cars)
- **审查人**：Jennifer Horkoff (主审), Khan Mohammad Habibhullah (实践审查)
- **链接**：https://odr.chalmers.se/bitstreams/7c06ef2c-d1ae-40b4-b13c-a35087077bce/download

**代码/仓库获取方式**：原文未提供公开代码/仓库获取链接。这是一篇硕士论文，实验在Volvo Cars内部环境中进行，使用Azure OpenAI平台进行模型微调和部署。

**数据集获取方式**：原文未提供公开数据集获取链接。数据集来自Volvo Cars内部的Car Weaver工具，包含20个产品功能需求及其对应的状态机，属于工业专有数据。论文中使用了合成数据生成技术扩充训练集。

## 简报

**解决的问题**

论文解决了如何从非结构化的自然语言需求自动生成状态机（statechart）的问题，特别是在汽车软件工程领域。

- **输入**：非结构化的自然语言文本需求（来自Volvo Cars的产品功能描述）
- **方法**：基于大语言模型（LLM）的微调框架，包括NLP特征提取、数据预处理、合成数据生成和领域特定微调
- **输出**：Mermaid.js格式的状态机代码及可视化状态机图

```
┌─────────────────────────────────────────────────────────────────┐
│                           输入层                                 │
├─────────────────────────────────────────────────────────────────┤
│ • 自然语言文本需求（产品功能描述）                                │
│ • 来自Car Weaver工具的需求规格说明                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         方法框架                                 │
├─────────────────────────────────────────────────────────────────┤
│  数据预处理 → 特征提取(NER/POS) → 合成数据生成                   │
│         ↓                                                        │
│  LLM微调(GPT-3.5/GPT-4/GPT-4o) → 状态机生成                      │
│         ↓                                                        │
│  专家评估(功能正确性/可理解性)                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          输出层                                  │
├─────────────────────────────────────────────────────────────────┤
│ • Mermaid.js格式的状态机代码                                     │
│ • 可视化状态机图                                                 │
│ • 包含状态、事件、迁移和动作的结构化表示                          │
└─────────────────────────────────────────────────────────────────┘
```

**实验结果总结**：微调后的GPT-4模型在功能正确性上平均得分3.52（相比基础模型的2.60），在可理解性上平均得分3.75（相比基础模型的2.96），Wilcoxon检验显示差异显著（p < 0.001）。但与人工创建的状态机相比，LLM生成的状态机在功能正确性上仍有差距（2.81 vs 4.00）。

**研究动机**

前人工作的不足：
- 现有工具（Stateflow、Yakindu、Enterprise Architect）需要大量手工工作
- 从文本需求创建状态机主要依赖人工，耗时且易错
- 现有自动化方法主要集中在结构图（如UML类图），对行为建模（状态机）研究不足
- LLM在状态机生成领域的潜力尚未充分探索

发现的问题：
- 手工创建状态机依赖领域专家，扩展性差
- 汽车系统日益复杂，手工方法难以应对
- 需求工程师和系统架构师通常不是状态机建模专家
- 手工创建的状态机在结构和完整性上存在不一致性

**方法创新**

核心创新点：
1. **领域特定微调**：针对汽车领域需求微调GPT模型，使用Volvo Cars的真实产品功能数据
2. **合成数据生成**：通过受控随机化技术从有限的真实数据生成大量训练样本，解决数据稀缺问题
3. **NLP特征提取**：使用NER和POS标注自动识别状态、事件、迁移和动作
4. **端到端自动化**：从文本需求直接生成Mermaid.js格式的可执行状态机代码

**实验设计**

- **对比对象**：
  - 基础LLM（未微调的GPT-3.5/GPT-4/GPT-4o）
  - 微调LLM（在汽车领域数据上微调的模型）
  - 人工创建的状态机（领域专家手工创建）
- **数据集**：
  - 主数据集：20个Volvo Cars产品功能需求
  - 合成数据集：通过随机化生成的扩充数据
  - 测试集：12个新的产品功能测试用例
- **评估指标**：
  - 功能正确性（Functional Correctness）
  - 可理解性（Understandability）
  - 需求对齐度（Requirement Alignment）
  - 模型性能指标（token准确率、验证损失）
- **使用的模型**：GPT-3.5-turbo、GPT-4、GPT-4o（通过Azure OpenAI平台微调）
- **评估方法**：
  - 定量评估：ANOVA、Tukey HSD检验、Wilcoxon符号秩检验
  - 定性评估：4位Volvo Cars领域专家的半结构化访谈和Likert量表评分

**结论与不足**

主要结论：
- 微调显著提升LLM生成状态机的质量（功能正确性和可理解性均有统计显著提升）
- 对于简单的线性场景（如TC9、TC11），微调模型表现优秀，接近人工水平
- LLM生成的状态机可节省时间，适合用于早期阶段的草图生成

局限性：
1. **复杂场景处理能力不足**：对于包含条件逻辑、嵌套迁移、时序约束的复杂需求（如TC5），模型表现较差
2. **迁移不完整**：生成的状态机存在缺失迁移、事件处理逻辑不完整的问题
3. **循环逻辑不清晰**：难以正确处理循环条件和终止点
4. **术语不一致**：生成的状态机中术语使用不一致
5. **需求对齐度不足**：对需求的解释过于通用，缺乏领域特定的细节
6. **数据集规模有限**：仅使用20个真实需求，可能导致过拟合
7. **泛化能力受限**：模型在汽车领域外的适用性未知
8. **仍需专家验证**：特别是对于安全关键和行为复杂的系统，专家参与仍然必不可少

## 研究问题与动机

### 问题背景

状态机（Statechart）是软件和系统工程中的重要工具，特别是在汽车、航空航天和嵌入式系统等需要建模动态行为的行业中。状态机由David Harel首次提出，扩展了传统有限状态机，增加了层次结构、并发性和事件驱动迁移等特性，使其成为表示复杂系统行为的有效机制。

在汽车行业，状态机被广泛用于建模动力系统控制、信息娱乐系统、高级驾驶辅助系统（ADAS）和自动驾驶算法等功能。在Volvo Cars，状态机被产品仿真团队广泛用于建模和验证系统功能，确保从需求定义到OTA软件更新的整个车辆生命周期中的系统功能稳健性。

### 核心问题

当前，工程师需要解释文本需求并使用专门工具手工创建状态机。随着系统变得越来越复杂和互联，这种手工方法难以有效扩展，导致不一致性、延迟和验证工作增加。具体问题包括：

1. **手工过程耗时且易错**：工程师必须解释文本需求，定义状态和迁移，并确保逻辑正确性
2. **依赖领域专家**：需求工程师、系统架构师和验证团队通常不是状态机建模专家，只有少数专业专家能够有效地将文本需求转换为可执行模型
3. **一致性问题**：手工创建的状态机在结构和完整性上可能存在差异，使验证和调试更加困难
4. **扩展性差**：随着汽车系统复杂性增加，手工方法难以应对

### 研究动机

自动化这一过程有潜力显著提高生产力、降低成本并确保关键系统设计和验证的一致性。近年来，大语言模型（LLM）如GPT-4在处理复杂文本输入和生成UML类图、状态机等输出方面展现出潜力。通过在定制数据集上训练这些模型，AI系统可以从文本描述自动生成状态机，减少手工工作，增强一致性，并最小化错误。

然而，尽管在LLM方面取得了进展，但其在自动化状态机生成方面的潜力尚未在真实世界环境中得到充分探索或使用，特别是在汽车行业。

## 核心方法

### 方法概述

本研究提出了一个基于LLM的解决方案，用于从汽车领域的非结构化自然语言需求自动生成状态机。该方法涉及多个阶段：

1. **数据收集与预处理**：从Car Weaver工具提取产品功能需求
2. **合成数据生成**：克服有限数据可用性的问题
3. **LLM微调**：在领域特定数据上微调GPT-3.5、GPT-4和GPT-4o
4. **状态机生成**：基于输入需求生成Mermaid.js格式的结构化状态机

实现使用Azure OpenAI和Weights & Biases (W&B)等工具支持模型训练和性能监控。

### 关键技术

#### 1. 数据预处理

数据预处理阶段将原始的非结构化文本产品功能转换为适用于机器学习应用的格式。主要步骤包括：

**步骤1：特征提取和分词（使用spaCy）**

使用Python的spaCy库进行高级NLP任务，实现的方法包括：

- **命名实体识别（NER）**：识别和分类文本中对应于状态机元素的关键实体。使用预训练的spaCy模型（en_core_web_sm），为状态机规格的特定词汇领域提供英语语言处理能力。定义状态机特定模式来识别状态（STATE）、动作（ACTION）和事件（EVENT）。

- **词性标注（POS Tagging）**：分析文本中每个词的语法角色。理解词性有助于确定实体之间的关系。例如，状态/事件属于名词，迁移属于动词，状态迁移中的关系属于介词。

**步骤2：数据转换**

将提取的组件（状态、事件、迁移和动作）结构化为JSON格式。JSON结构设计为继承状态机的结构，包括以下键：

- **States**：列出所有识别的状态的数组
- **Events**：规格中识别的事件数组
- **Transitions**：定义迁移的数组，包括from_state、to_state和triggering_event等属性
- **Actions**：指定与状态迁移相关的动作的数组，可能包括执行条件、效果或系统响应

**步骤3：数据标注**

创建提示-完成对（prompt-completion pairs）以实现监督学习：

- **Prompt（输入）**：每个产品功能需求对应状态机的精炼文本规格
- **Completion（输出/标签）**：通过前面的预处理、特征提取和转换步骤生成的产品功能需求对应状态机的结构化JSON表示

#### 2. 合成数据生成

由于主数据集规模有限（仅20个产品功能需求），研究采用合成数据生成策略来扩充训练集。方法包括：

1. **组件池生成**：从主数据集中提取所有唯一的基本组件（状态、事件、迁移、动作）
2. **受控随机化**：使用Python的random库重新组合这些元素，同时保持原始结构格式
3. **数据变异**：通过随机化生成新的提示-完成对，增加数据集多样性

这种方法在保持结构有效性的同时实现了变化，使模型能够学习更广泛的模式。

#### 3. 模型微调

使用Azure OpenAI平台对三个GPT模型进行微调：

- **模型**：GPT-3.5-turbo、GPT-4、GPT-4o
- **训练参数**：
  - Batch size: 16或32
  - Learning rate: 1.01
  - Epochs: 8
  - Seed: 42
- **监控工具**：Weights & Biases (W&B)用于跟踪训练过程和性能指标

每个模型使用相同的训练/验证数据、超参数和实验设置进行微调，以确保公平比较。进行了三次独立的训练运行以评估一致性和稳健性。

#### 4. 状态机生成

微调后的模型接收自然语言需求作为输入，生成Mermaid.js语法的状态机代码。生成的代码可以在Mermaid.js编辑器中可视化为状态机图。

### 形式化定义

虽然论文没有提供严格的形式化定义，但可以从描述中推断出以下结构：

**状态机模型**：
```
Statechart = (S, E, T, A)
其中：
- S = {s₁, s₂, ..., sₙ} 是状态集合
- E = {e₁, e₂, ..., eₘ} 是事件集合
- T ⊆ S × E × S 是迁移关系（from_state, triggering_event, to_state）
- A = {a₁, a₂, ..., aₖ} 是动作集合
```

**提示-完成对**：
```
Dataset = {(p₁, c₁), (p₂, c₂), ..., (pₙ, cₙ)}
其中：
- pᵢ ∈ NaturalLanguage 是文本需求
- cᵢ ∈ JSON(Statechart) 是对应的结构化状态机表示
```

### 系统架构

整个实验流程包括以下阶段：

1. **Scoping（范围界定）**：定义实验目标和评估标准
2. **Planning（规划）**：
   - 上下文选择：Volvo Cars环境
   - 假设制定：RQ1和RQ2的零假设和备择假设
   - 变量选择：独立变量（模型类型）和因变量（功能正确性、可理解性）
   - 主体选择：Volvo Cars的领域专家
   - 实验设计：数据预处理→微调→生成→评估
3. **Operation（操作）**：
   - 数据收集：从Car Weaver工具提取需求
   - 数据预处理：NER、POS标注、JSON转换
   - 合成数据生成：扩充训练集
   - 模型微调：使用Azure OpenAI
   - 模型评估：定量指标和专家评审
4. **Analysis（分析）**：统计检验和结果解释

## 实验与评估

### 研究问题

研究围绕两个核心研究问题展开：

**RQ1：微调LLM是否改善状态机生成？**
- H0：微调不会显著改善性能指标（功能正确性、可理解性）
- H1：微调显著改善性能指标

**RQ2：LLM生成的状态机与手工创建的状态机相比如何？**
- H0：LLM生成的状态机未达到与手工创建的状态机相当的功能正确性水平
- H1：LLM生成的状态机达到相当或更高的功能正确性水平

### 数据集

**主数据集**：
- 20个产品功能需求，从Volvo Cars的Car Weaver工具手工提取
- 每个需求概述系统的特定功能
- 选择标准：清晰性、行为深度、包含明确定义的事件、动作和迁移

**合成数据集**：
- 通过受控随机化从主数据集生成
- 保留原始需求的结构，同时随机化系统状态、事件、迁移和动作
- 用于增强数据集规模，实现更准确的模型性能

**测试集**：
- 12个新的产品功能测试用例，由领域专家创建
- 从训练和合成数据生成阶段中排除
- 涵盖典型的汽车功能：方向指示、镜子调节、引擎盖操作、挡风玻璃清洗等

### 评估指标

#### 定量模型评估

使用Azure AI Foundry平台和Weights & Biases工具进行模型评估，主要指标包括：

1. **train_loss**：训练集上的损失值
2. **train_mean_token_accuracy**：训练集上的平均token准确率
3. **valid_loss**：验证集上的损失值
4. **valid_mean_token_accuracy**：验证集上的平均token准确率
5. **full_valid_loss**：完整验证集上的最终损失
6. **full_valid_mean_token_accuracy**：完整验证集上的最终平均token准确率

模型选择主要基于full_valid_mean_token_accuracy和full_valid_loss，因为它们提供了模型在整个验证数据集上泛化能力的最详细指标。

#### 统计分析方法

**模型选择阶段**：
- **Shapiro-Wilk检验**：验证数据正态性
- **单因素方差分析（ANOVA）**：比较三个模型（GPT-3.5、GPT-4、GPT-4o）的性能
- **Tukey HSD事后检验**：确定哪些特定模型之间存在显著差异，同时控制I类错误

**专家评审比较**：
- **Wilcoxon符号秩检验**：用于比较配对样本和序数数据（Likert量表评分）
- 适用于非正态分布数据和Likert量表响应的序数性质

#### 专家评审

在选择最佳性能模型后，进行专家评审和反馈过程：

**参与者**：
- 4位来自Volvo Cars产品仿真团队的领域专家
- 每位专家在汽车系统设计和基于模型的开发方面有5年以上经验
- 负责创建和验证系统需求和功能状态机

**评审过程**：
- 半结构化访谈，每次持续30-45分钟
- 使用Likert量表（1-5分）评估生成的状态机
- 评估维度：
  - 功能正确性（Functional Correctness）
  - 可理解性（Understandability）
  - 需求对齐度（Requirement Alignment）

**评审重点**：
- 状态迁移的清晰度，特别是对于具有多种交互模式的系统
- 安全相关功能中控制流的逻辑表示
- 处理重复模式的视觉一致性
- 基于事件的行为与汽车用户界面期望的对齐
- 对同时或冲突输入的系统行为的可理解性
- 识别歧义或建模缺口，特别是在基于时间或条件的逻辑中
- 改进模型准确性、可读性或可维护性的建议

### 主要实验结果

#### 1. 模型选择结果

**视觉分析**：
- GPT-4达到最高平均token准确率（0.94728）
- GPT-4达到最低平均验证损失（0.13422）
- GPT-4o和GPT-3.5-turbo表现相似但略低

**统计分析**：

对于平均token准确率：
- ANOVA检验：F(2, 6) = 10.06, p = 0.0121（存在显著差异）
- Tukey HSD事后检验：
  - GPT-4显著高于GPT-3.5（均值差=0.001, p=0.0414）
  - GPT-4显著高于GPT-4o（均值差=0.0013, p=0.0119）
  - GPT-3.5与GPT-4o之间无显著差异（p=0.5543）

对于验证损失：
- ANOVA检验：F(2, 6) = 12.18, p = 0.0077（存在显著差异）
- Tukey HSD事后检验：
  - GPT-4显著低于GPT-3.5（均值差=-0.0065, p=0.0156）
  - GPT-4显著低于GPT-4o（均值差=0.0072, p=0.0102）
  - GPT-3.5与GPT-4o之间无显著差异（p=0.9176）

**结论**：GPT-4在准确率和损失方面均略优于GPT-3.5-turbo和GPT-4o。最终选择batch_size=16的GPT-4版本进行部署，因为它在计算资源和性能之间取得了更好的平衡。

#### 2. 微调模型 vs 基础模型

**定性比较示例（TC6：挡风玻璃清洗）**：

基础模型生成的状态机：
- 遵循线性结构，分支最少
- 使用通用状态标签（如"Washing Enabled"、"Wiper and Washer Active"）
- 迁移抽象，不反映特定用户动作或系统条件
- 可解释性降低

微调模型生成的状态机：
- 更详细和上下文感知
- 包含中间状态（如"WindscreenWashing"、"WindscreenWiping"、"WasherFluidSpraying"）
- 明确定义的迁移，由特定用户输入触发（如"User pulls right stalk for >1 second"）
- 包含多个分支、双向迁移和逻辑排序
- 更好的可追溯性和模型清晰度

**专家评分比较**：

功能正确性：
- 基础模型平均分：2.60（中位数2.5）
- 微调模型平均分：3.52（中位数4.0）
- 平均提升：0.92分
- Wilcoxon检验：统计量=39.5, p=0.00002（显著差异）

可理解性：
- 基础模型平均分：2.96（中位数3.0）
- 微调模型平均分：3.75（中位数4.0）
- Wilcoxon检验：统计量=56.0, p=0.00036（显著差异）

**最佳和最差表现**：
- 最佳：TC9和TC11，微调模型达到4.5分（满分5分）
- 显著改进：TC1（从1.88提升到4.25）、TC5（从1.0提升到3.25）
- 微调模型在所有12个测试用例中均优于或等于基础模型

**RQ1结论**：拒绝H0，接受H1。微调显著改善了LLM在状态机生成方面的性能。

#### 3. 微调模型 vs 人工创建的状态机

**专家评估平均分**：
- 功能正确性：2.88（中性）
- 可理解性：2.5（略不清晰）
- 需求对齐度：2.75（轻度到中度）

**统计比较**：
- Wilcoxon符号秩检验：统计量=0.0, p=9.72×10⁻¹¹（显著差异）
- 人工模型平均分：4.00（中位数4.00）
- 微调模型平均分：2.81（中位数3.00）

**专家反馈识别的问题**：

| 方面 | 识别的问题 | 改进建议 |
|------|-----------|---------|
| 状态迁移 | 不完整或不清晰的迁移 | 更清晰地定义状态迁移 |
| 循环逻辑 | 难以理解循环条件和终点 | 更清晰的循环处理和结束条件 |
| 需求对齐 | 对需求的通用解释 | 适应领域特定需求 |
| 术语一致性 | 状态机之间术语不一致 | 标准化命名约定和术语 |

**性能分析**：
- 对于简单场景（TC9、TC11）：微调模型表现优秀，接近人工水平
- 对于复杂场景（TC5）：模型表现出局限性
  - 不完整的迁移
  - 缺失的事件处理逻辑
  - 不清晰的循环条件
  - 模糊的开始/结束状态

**RQ2结论**：接受H0。LLM生成的状态机目前未达到与人工创建的状态机相当的功能正确性水平。

### 结果总结

1. **微调的有效性**：微调在领域特定数据上显著提升了LLM生成状态机的质量
2. **适用场景**：对于简单的线性场景，微调模型可以生成高质量的状态机
3. **局限性**：对于复杂的条件逻辑、嵌套迁移和时序约束，模型仍有不足
4. **实用价值**：可用于早期阶段的草图生成，节省时间，但仍需专家验证和完善
5. **质量差距**：与人工创建的状态机相比，LLM生成的状态机在功能正确性和清晰度上仍有差距

## 与本研究的关系

### 相关性分析

本论文与博士研究的"基于控制系统软件需求的LLM状态机结构化建模方法"高度相关，具体体现在：

1. **研究目标一致**：都致力于从自然语言需求自动生成状态机模型
2. **应用领域相似**：都关注安全关键系统（汽车vs控制系统）
3. **技术路线相近**：都采用LLM微调的方法
4. **面临相似挑战**：需求的非形式化、模型的正确性验证、复杂逻辑的处理

### 可借鉴之处

#### 1. 数据预处理方法

**NLP特征提取技术**：
- 使用NER识别状态、事件、动作等关键实体
- 使用POS标注分析语法角色和实体关系
- 可以借鉴到控制系统需求的分析中

**结构化转换**：
- 将提取的组件转换为JSON格式的中间表示
- 这种方法可以适配到本研究的状态机DSL（pyfcstm）

#### 2. 合成数据生成策略

**受控随机化方法**：
- 从有限的真实数据中提取组件池
- 通过随机重组生成大量训练样本
- 保持结构有效性的同时增加多样性

**对本研究的启发**：
- 可以应用到控制系统需求数据集的扩充
- 特别适合数据稀缺的工业场景
- 需要注意保持领域特定的约束和模式

#### 3. 评估方法论

**多维度评估框架**：
- 定量指标：token准确率、验证损失
- 定性评估：专家评审、Likert量表
- 统计检验：ANOVA、Tukey HSD、Wilcoxon检验

**可借鉴的评估维度**：
- 功能正确性：状态和迁移的准确性
- 可理解性：模型的清晰度和可读性
- 需求对齐度：与原始需求的一致性

#### 4. 实验设计

**对比实验设计**：
- 基础模型 vs 微调模型
- LLM生成 vs 人工创建
- 多个模型版本的比较（GPT-3.5/GPT-4/GPT-4o）

**对本研究的启发**：
- 可以设计类似的对比实验
- 评估不同LLM在控制系统建模中的表现
- 比较不同微调策略的效果

#### 5. 工业实践经验

**Volvo Cars的实践**：
- 与工业界合作的模式（学术导师+工业导师）
- 使用真实工业数据和工具（Car Weaver）
- 专家参与评估的流程

**对本研究的启发**：
- 可以寻求与控制系统企业的合作
- 获取真实的工业需求数据
- 建立专家评审机制

### 存在的不足与改进空间

#### 1. 复杂逻辑处理能力不足

**论文的局限**：
- 对于包含条件逻辑、嵌套迁移、时序约束的复杂需求处理较差
- 循环逻辑和终止条件不清晰
- 缺失迁移和事件处理逻辑

**本研究的改进方向**：
- 引入时间自动机理论，显式建模时间约束
- 使用层次化状态机表示，处理嵌套结构
- 设计专门的提示工程策略，引导LLM生成守卫条件和时间约束

#### 2. 形式化验证缺失

**论文的局限**：
- 仅依赖专家评审，缺乏形式化验证
- 无法保证生成的状态机满足特定性质
- 没有验证状态机的可达性、活性等属性

**本研究的改进方向**：
- 集成模型检查工具（如UPPAAL）
- 自动生成验证场景和待验证性质
- 建立"生成-验证-修复"的闭环流程

#### 3. 输出格式限制

**论文的局限**：
- 仅生成Mermaid.js格式，主要用于可视化
- 不支持可执行的状态机代码
- 缺乏与现有工具的集成

**本研究的改进方向**：
- 生成可执行的状态机DSL代码（pyfcstm）
- 支持多种输出格式（UPPAAL、Stateflow等）
- 与验证工具无缝集成

#### 4. 数据集规模和多样性

**论文的局限**：
- 仅使用20个真实需求，数据集规模小
- 仅限于汽车领域，泛化能力未知
- 合成数据可能无法覆盖真实场景的复杂性

**本研究的改进方向**：
- 构建更大规模的控制系统需求数据集
- 涵盖多个控制系统领域（BSN、CARA、Elevator等）
- 使用更多样化的合成数据生成策略

#### 5. 缺乏迭代修复机制

**论文的局限**：
- 一次性生成，没有迭代改进机制
- 发现错误后需要人工修复
- 无法从验证反馈中学习

**本研究的改进方向**：
- 设计基于验证反馈的迭代修复方法
- 使用反例引导的模型修正
- 建立从错误中学习的机制

### 对本研究的启发

#### 1. 研究路线验证

本论文的成功证明了以下研究路线的可行性：
- LLM微调在领域特定建模任务中的有效性
- 从自然语言需求生成状态机的技术可行性
- 专家评审与定量指标相结合的评估方法

#### 2. 技术选择参考

**模型选择**：
- GPT-4在状态机生成任务中表现最佳
- 微调显著优于零样本或少样本学习
- 需要在性能和计算资源之间权衡

**数据策略**：
- 合成数据生成是应对数据稀缺的有效方法
- 需要保持合成数据的结构有效性和领域特征

#### 3. 研究重点明确

**需要重点解决的问题**：
- 复杂逻辑的建模能力（条件、嵌套、时序）
- 形式化验证的集成
- 迭代修复机制的设计
- 输出格式的可执行性

**可以简化的方面**：
- 基础的NLP预处理技术已经成熟
- 微调流程和工具链已经完善
- 评估方法论已有成熟框架

#### 4. 创新点定位

本研究相对于该论文的创新点应体现在：
- **时间约束建模**：显式处理时间自动机和时间约束
- **形式化验证集成**：不仅生成模型，还要验证模型
- **迭代修复机制**：建立闭环的生成-验证-修复流程
- **多层次建模**：支持层次化状态机和守卫条件
- **性质生成**：自动生成验证场景和待验证性质

#### 5. 实验设计参考

**可以复用的实验设计**：
- 对比实验框架（基础vs微调、LLMvs人工）
- 评估维度（功能正确性、可理解性、需求对齐）
- 统计检验方法（ANOVA、Wilcoxon等）

**需要扩展的实验**：
- 增加形式化验证的评估维度
- 评估迭代修复的效果
- 测试不同类型的控制系统需求

### 总结

本论文为博士研究提供了重要的参考和启发：

**验证了可行性**：LLM微调在状态机生成任务中是有效的，特别是对于简单到中等复杂度的场景。

**指明了方向**：需要重点解决复杂逻辑处理、形式化验证集成和迭代修复等问题。

**提供了基础**：数据预处理、合成数据生成、评估方法论等技术可以直接借鉴。

**明确了创新点**：本研究应在时间约束建模、形式化验证、迭代修复等方面实现突破，构建完整的"生成-验证-修复"闭环。

## 重要的相关工作

本论文引用了40篇文献，按作用分类如下：

### 1. 重要的前身类工作

本论文没有明确的前身工作，这是一篇探索性的硕士论文，首次在Volvo Cars环境中尝试使用LLM自动生成状态机。

### 2. 直接参与实验的baseline

本论文的实验对比主要是：
- 基础LLM（未微调）vs 微调LLM
- LLM生成 vs 人工创建

没有引用其他已有的自动化状态机生成工具作为baseline。

### 3. 提供了重要论证的工作

**3.1 Harel (1987) - Statecharts: A Visual Formalism for Complex Systems**
- 标题：Statecharts: A Visual Formalism for Complex Systems
- 作者：David Harel
- 会议：Science of Computer Programming, 8(3):231–274, 1987
- 主要内容：首次提出状态机（Statechart）的概念，扩展了传统有限状态机，增加了层次结构、并发性和事件驱动迁移等特性
- 论文中的引用：
  - 第332行："by David Harel [16], extend traditional finite state machines with additional features"
  - 第438-441行："Although Harel et al.[17] introduced the concept of statecharts as an enhancement to finite state machines, their work did not focus on automating statechart generation from textual requirements, but instead focused on providing a better way to represent system behavior."
  - 第1714行："These results are consistent with those of Harel et al.[17], who also noted"
- 与本论文的关系：为状态机的理论基础提供了定义，但没有涉及自动化生成。论文指出Harel的工作专注于提供更好的系统行为表示方式，而非从文本需求自动生成状态机
- 佐证内容：论证了状态机作为建模工具的重要性和理论基础，同时也指出了自动化生成的研究空白

**3.2 Harel et al. (2005) - Synthesis Revisited: Generating Statechart Models from Scenario-Based Requirements**
- 标题：Synthesis Revisited: Generating Statechart Models from Scenario-Based Requirements
- 作者：David Harel, Hillel Kugler, Amir Pnueli
- 会议：Springer Berlin Heidelberg, Berlin, Heidelberg, 2005, pages 309–324
- 主要内容：从基于场景的需求生成状态机模型，但主要关注形式化场景而非自然语言文本
- 论文中的引用：第438-441行、第1714行、第1752行
- 与本论文的关系：虽然涉及状态机生成，但输入是形式化的场景描述，而非非结构化的自然语言需求
- 佐证内容：论证了从需求生成状态机的可行性，但也指出了从非结构化文本生成的挑战

**3.3 Meng & Ban (2024) - Automated UML Class Diagram Generation**
- 标题：Automated UML Class Diagram Generation from Textual Requirements Using NLP Techniques
- 作者：Yang Meng, Ainita Ban
- 发表：Volume 8, 2024
- 主要内容：基于NLP的UML类图自动生成，准确率88.46%。使用NLP技术从文本需求中提取实体和关系
- 论文中的引用：
  - 第454-456行："Researchers, such as Meng & Ban [26] have focused primarily on structural diagrams, such as class diagrams, demonstrating successful extraction of entities and relationships from textual requirements. However, their work does not address the modeling of behavioral logic or dynamic transitions"
  - 第523行："Methods designed for structural model generation, such as class diagrams or use case diagrams, often rely on NLP techniques to extract states and transitions from textual input [26, 36]"
  - 第1752行："and Ban [26], Harel et al.[17], and Zhong et al.[40], contributing to the evo-"
- 局限性：仅限于结构图，无法处理动态行为和系统交互。不涉及行为逻辑或动态迁移的建模
- 与本论文的关系：展示了NLP在图表自动化中的潜力，但也指出了结构图方法不适用于状态机。论文强调状态机需要捕获行为逻辑，而不仅仅是结构
- 佐证内容：论证了状态机自动化比结构图自动化更具挑战性，因为需要理解时序和事件驱动的行为

**3.4 Zhong et al. (2023) - Natural Language Processing for Systems Engineering**
- 标题：Natural Language Processing for Systems Engineering: Automatic Generation of Systems Modelling Language Diagrams
- 作者：Shaohong Zhong, Andrea Scarinci, Alice Cicirello
- 会议：Knowledge-Based Systems, 259:110071, January 2023
- 主要内容：应用NLP技术生成SysML图表，展示了AI在模型构建中的潜力
- 论文中的引用：
  - 第464-466行："For instance, Zhong et al.[40] applied NLP techniques to produce SysML diagrams, a standard system engineering tool, showing the potential of AI in model construction"
  - 第1752行："and Ban [26], Harel et al.[17], and Zhong et al.[40], contributing to the evo-"
- 局限性：主要关注结构图（如UML类图），不涉及状态机
- 与本论文的关系：展示了NLP和AI在自动化图表生成中的潜力，但未解决状态机生成的特定挑战
- 佐证内容：论证了AI技术在模型生成领域的可行性，为本研究提供了技术路线的参考

**3.5 Ferrari et al. (2023) - Model Generation from Requirements with LLMs: An Exploratory Study**
- 标题：Model Generation from Requirements with LLMs: An Exploratory Study
- 作者：A. Ferrari, S. Abualhaija, C. Arora
- 会议：Proceedings of the International Requirements Engineering Conference, 2023
- 主要内容：探索性研究，使用LLM从需求生成模型
- 论文中的引用：参考文献列表第1905-1907行
- 与本论文的关系：探索了LLM在需求工程和模型生成中的应用，为本研究提供了LLM应用的先例
- 佐证内容：论证了LLM在模型生成任务中的潜力

### 4. 在技术上提供了支持的工作

**4.1 OpenAI GPT-4 (2024)**
- 技术使用：直接使用GPT-3.5-turbo、GPT-4和GPT-4o作为基础模型进行微调
- 与本论文的关系：核心技术基础

**4.2 spaCy (Honnibal & Montani, 2017, 2020)**
- 技术使用：用于特征提取阶段的NER和POS标注
- 与本论文的关系：数据预处理的核心工具

**4.3 Azure OpenAI Platform**
- 技术使用：用于模型微调和部署的平台
- 与本论文的关系：实验的基础设施

**4.4 Basili et al. (1999) - Building Knowledge Through Families of Experiments**
- 技术使用：提供了实验设计的方法论框架（GQM框架）
- 与本论文的关系：指导了整个实验设计和评估方法论

**4.5 Weights & Biases (W&B)**
- 技术使用：用于跟踪训练过程和性能监控的工具
- 与本论文的关系：实验监控和结果可视化的基础设施

**4.6 Mermaid.js**
- 技术使用：用于生成和可视化状态机图的JavaScript库
- 与本论文的关系：状态机输出格式的选择，支持代码到可视化的转换

**4.7 Li et al. (2023) - Synthetic Data Generation with Large Language Models**
- 标题：Synthetic Data Generation with Large Language Models for Text Classification: Potential and Limitations
- 作者：Zhuoyan Li, Hangxiao Zhu, Zhuoran Lu, Ming Yin
- 发表：arXiv preprint arXiv:2310.07849, 2023
- 主要内容：使用LLM进行合成数据生成，探索其在文本分类任务中的潜力和局限性
- 论文中的引用：第1699行："previous research, such as Liu et al.[39], which has shown that domain-specific"
- 技术使用：启发了合成数据生成策略的设计，特别是受控随机化方法
- 与本论文的关系：提供了应对数据稀缺问题的技术方案，论文采用了类似的合成数据生成思路

**4.8 Basili et al. (1999) - Building Knowledge Through Families of Experiments**
- 标题：Building Knowledge Through Families of Experiments
- 作者：Victor R. Basili等
- 主要内容：提出了GQM（Goal-Question-Metric）框架，用于系统性的软件工程实验设计
- 论文中的引用：第510-511行："Basili et al.[4] emphasize the need for systematic experimentation to validate software engineering methods, particularly AI-driven solutions"
- 技术使用：提供了实验设计的方法论框架，指导了整个研究的实验设计和评估方法论
- 与本论文的关系：论文的实验设计（Scoping-Planning-Operation-Analysis）遵循了Basili的实验方法论

### 5. 其他重要工作

**5.1 Sandeep et al. (2017) - Automated Use Case Diagram Generation**
- 标题：Automated Use Case Diagram Generation from Textual User Requirement Documents
- 作者：Sandeep Vemuri, Sisay Chala, Madjid Fathi
- 会议：2017 IEEE 30th Canadian Conference on Electrical and Computer Engineering (CCECE), pages 1–4, 2017
- 主要内容：使用概率NLP方法从文本需求中识别参与者和用例，生成用例图
- 论文中的引用：
  - 第483-491行："For example, Sandeep et al.[36] used a probabilistic NLP approach to identify actors and use cases in textual requirements for the generation of use case diagrams. Although their approach demonstrates NLP's potential in automating diagram generation, it does not address the challenges specific to statechart automation"
  - 第523行："Methods designed for structural model generation, such as class diagrams or use case diagrams, often rely on NLP techniques to extract states and transitions from textual input [26, 36]"
  - 第534行："instance, although Sandeep et al. [36] demonstrated the use of probabilistic NLP"
- 与本论文的关系：展示了NLP在自动化图表生成中的潜力，但未解决状态机特定的挑战（如建模系统迁移和状态）
- 作用：提供了NLP技术在需求工程中的应用案例，但也指出了其在行为建模方面的局限性

**5.2 Liu et al. (2024) - ChartifyText**
- 标题：ChartifyText: Automated Chart Generation from Data-Involved Texts via LLM
- 作者：Songheng Zhang, Lei Wang, Toby Jia-Jun Li, Qiaomu Shen, Yixin Cao, Yong Wang
- 发表：arXiv preprint arXiv:2410.14331, 2024
- 主要内容：使用LLM将基于文本的数据描述转换为结构化的可视化图表
- 论文中的引用：
  - 第501-504行："Liu et al.[39] created ChartifyText, an AI that converts text-based descriptions of data into structured visual charts, illustrating the broader potential of LLMs for generating structured models"
  - 第1699行："previous research, such as Liu et al.[39], which has shown that domain-specific"
- 与本论文的关系：展示了LLM在从文本生成结构化模型方面的更广泛潜力，为本研究提供了技术可行性的证据
- 作用：提供了LLM在文本到结构化输出转换任务中的成功案例

**5.3 Schneider et al. (2025) - A Reference Model for Empirically Comparing LLMs with Humans**
- 标题：A Reference Model for Empirically Comparing LLMs with Humans
- 作者：Kurt Schneider, Farnaz Fotrousi, Rebekka Wohlrab
- 会议：IEEE — Accepted to the 47th International Conference on Software Engineering Companion (ICSE-C), Software Engineering in Society Track (SEIS), 2025
- 主要内容：提供了比较LLM与人类表现的参考模型和方法论
- 论文中的引用：第514行："Prior studies have used experimental methodologies to compare AI-generated models with human-created ones, assessing their accuracy, completeness, and usability [32]"
- 与本论文的关系：为本研究的评估方法论提供了理论基础，特别是LLM生成vs人工创建的对比实验设计
- 作用：提供了评估框架和方法论指导

**5.4 工具和标准**

**Yakindu Statechart Tools**
- 作用：商业状态机建模工具，用于对比说明现有工具的手工性质

**MathWorks Stateflow**
- 作用：广泛使用的状态机建模和仿真工具，用于说明工业界的现状

**Sparx Systems Enterprise Architect**
- 作用：企业级建模工具，支持UML和状态机建模

**Car Weaver (Volvo Cars Internal)**
- 作用：Volvo Cars内部的需求管理工具，本研究数据集的来源

**5.5 统计分析方法**

**Geraghty (2022) - Tukey's Honestly Significant Difference (HSD) Test**
- 作用：提供了事后检验方法，用于模型选择阶段的统计分析

**Thombre (2024) - Wilcoxon Signed Rank Test**
- 作用：提供了非参数统计检验方法，用于专家评审数据的分析

**Ross (2017) - One-way ANOVA**
- 作用：提供了方差分析方法，用于比较多个模型的性能

**5.6 背景知识和方法论**

**Wohlin et al. (2012) - Experimentation in Software Engineering**
- 作用：提供了软件工程实验的方法论框架

**Kreinovich (2014) - Why 70/30 or 80/20 Relation Between Training and Testing Sets**
- 作用：为训练集和测试集的划分提供了理论依据

**Huang & Zhao (2024) - Data Collection and Labeling Techniques for Machine Learning**
- 作用：为数据标注过程提供了技术指导

**Fan et al. (2021) - A Review on Data Preprocessing Techniques**
- 作用：为数据预处理阶段提供了技术参考

**5.7 其他相关研究**

**Ferreira et al. (2014) - Reliable Execution of Statechart-Generated Correct Embedded Software**
- 作用：展示了状态机在嵌入式系统中的应用

**Mens et al. (2019) - A Method for Testing and Validating Executable Statechart Models**
- 作用：提供了状态机测试和验证的方法

**He et al. (2024) - Does Prompt Formatting Have Any Impact on LLM Performance?**
- 作用：为提示工程提供了技术参考

**Kaiser et al. (2020) - A Vehicle Telematics Service for Driving Style Detection**
- 作用：展示了汽车领域的相关应用场景

## 文献分类总结

本论文共引用40篇文献，按作用分类如下：

1. **前身类工作（0篇）**：无直接前身工作。这是一篇探索性的硕士论文，首次在Volvo Cars环境中尝试使用LLM自动生成状态机。

2. **实验baseline（0篇）**：实验对比主要是内部的（基础LLM vs 微调LLM，LLM生成 vs 人工创建），没有引用其他已有的自动化状态机生成工具作为baseline。

3. **论证支持（5篇）**：
   - Harel (1987)：状态机理论基础
   - Harel et al. (2005)：从场景生成状态机
   - Meng & Ban (2024)：UML类图自动生成
   - Zhong et al. (2023)：SysML图表生成
   - Ferrari et al. (2023)：LLM模型生成探索

4. **技术支持（8篇）**：
   - OpenAI GPT-4：基础模型
   - spaCy：NLP特征提取
   - Azure OpenAI Platform：微调平台
   - Weights & Biases：实验监控
   - Mermaid.js：状态机可视化
   - Basili et al. (1999)：实验方法论
   - Li et al. (2023)：合成数据生成
   - Schneider et al. (2025)：LLM评估方法论

5. **其他支持（27篇）**：
   - 工具和标准（4篇）：Yakindu、Stateflow、Enterprise Architect、Car Weaver
   - 统计分析方法（3篇）：Tukey HSD、Wilcoxon检验、ANOVA
   - 背景知识和方法论（4篇）：软件工程实验、数据集划分、数据标注、数据预处理
   - 其他相关研究（16篇）：Sandeep et al.、Liu et al.、Ferreira et al.、Mens et al.、He et al.、Kaiser et al.等

本论文的核心创新在于：
- 首次在汽车工业环境（Volvo Cars）中应用LLM微调技术自动生成状态机
- 提出了合成数据生成策略应对数据稀缺问题
- 建立了完整的评估框架，结合定量指标和专家评审
- 通过严格的统计检验验证了微调的有效性

实验结果表明，微调显著提升了LLM生成状态机的质量（功能正确性提升35%，可理解性提升27%），但与人工创建的状态机相比仍有差距（功能正确性2.81 vs 4.00）。

