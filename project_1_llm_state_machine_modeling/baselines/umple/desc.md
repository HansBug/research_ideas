# 探索Llama3生成以Umple表示的状态机的性能 / Exploring How Well Llama3 can Generate State Machines Represented in Umple

## 基本信息

- **标题（中文）**：探索Llama3生成以Umple表示的状态机的性能
- **标题（英文）**：Exploring How Well Llama3 can Generate State Machines Represented in Umple
- **作者**：Parva Pathak
- **单位**：University of Ottawa / Université d'Ottawa
- **发表**：硕士学位论文（Master's Thesis），2025年
- **类型**：PhD Thesis
- **链接**：https://ruor.uottawa.ca/items/b3679a91-5445-45ce-b289-bfddba3010f6
- **代码/仓库获取方式**：原文未提供公开代码/仓库获取链接
- **数据集获取方式**：论文中使用的5个测试系统（Blackjack, Course Section, Credit Card Transaction, Driver License, Hotel Stay）在论文正文中有详细描述和需求说明，但未提供独立的公开数据集下载链接

## 简报

**解决的问题**：使用Llama 3大语言模型从自然语言需求自动生成Umple建模语言表示的状态机代码，以减少手工编写状态机的时间成本。

- **输入**：自然语言需求描述（包含系统描述和功能需求列表）
- **方法**：Llama 3 (8B参数模型) + 三种提示工程策略（Zero-shot / One-shot / RAG）
- **输出**：Umple建模语言的状态机代码

```
┌─────────────────────────────────────────────────────────────────┐
│                           输入层                                 │
├─────────────────────────────────────────────────────────────────┤
│ • 自然语言系统描述                                                │
│ • 功能需求列表                                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         方法框架                                 │
├─────────────────────────────────────────────────────────────────┤
│  Llama 3 (8B) + 提示工程策略                                      │
│         ↓                                                        │
│  Zero-shot → One-shot → RAG (多示例检索增强)                      │
│         ↓                                                        │
│  [Nomic嵌入模型 + 余弦相似度检索]                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          输出层                                  │
├─────────────────────────────────────────────────────────────────┤
│ • Umple状态机代码                                                 │
│ • 编译状态（可编译/不可编译）                                      │
│ • 质量评估指标（ICP/EUCP/归一化Levenshtein距离）                   │
└─────────────────────────────────────────────────────────────────┘
```

**实验结果总结**：RAG方法在5个测试系统上的归一化Levenshtein距离范围为0.07-0.32，显著优于Zero-shot（完全失败）和One-shot（0.13-0.46）方法。Credit Card Transaction系统表现最佳（0.07），Blackjack系统表现最差（0.32）。

**研究动机**：状态机是软件规范和实现的重要形式化工具，但从需求手工创建状态机耗时且容易出错。虽然Umple等工具简化了建模过程，但开发者仍需将需求翻译为状态机。现有研究已探索LLM生成代码和模型的能力，但尚无针对状态机生成的研究。

**方法创新**：
1. 首次将LLM应用于Umple状态机自动生成
2. 提出针对状态机生成的专用评估指标（ICP、EUCP、归一化Levenshtein距离）
3. 系统比较Zero-shot、One-shot和RAG三种方法的有效性
4. 使用Nomic嵌入模型和余弦相似度进行RAG示例检索

**实验设计**：
- **对比对象**：Zero-shot vs One-shot vs RAG
- **数据集**：5个测试系统（Blackjack、Course Section、Credit Card Transaction、Driver License、Hotel Stay）
- **评估指标**：
  - Invalid Code Percentage (ICP)：无效代码百分比
  - Extraneous Unparsed Code Percentage (EUCP)：额外未解析代码百分比
  - 归一化Levenshtein距离：衡量生成代码与参考代码的编辑距离
  - Pass@K：K次尝试中生成正确解决方案的概率
  - CodeBLEU：代码语义相似度
- **使用的模型**：Llama 3 (8B参数模型)

**结论与不足**：
- **主要结论**：RAG方法显著优于Zero-shot和One-shot，能为简单系统节省大量时间
- **方法优势**：RAG通过检索相似示例有效指导LLM生成符合Umple语法的状态机
- **局限性**：
  1. 仅测试5个相对简单的系统，可扩展性未充分验证
  2. 使用较小的8B参数模型（受本地机器限制），性能可能不如更大模型
  3. 未涉及时间约束、守卫条件等高级状态机特性
  4. 缺乏形式化验证集成，无法自动检查生成状态机的正确性
  5. Umple是小众建模语言，LLM训练数据中相关示例较少

## 研究问题与动机

### 问题背景

状态机是软件规范和实现中的重要形式化工具，广泛应用于系统行为建模。状态机通过状态（states）和迁移（transitions）描述系统行为：状态定义系统在某一时刻的唯一特征集合，迁移定义系统从一个状态转换到另一个状态所需的动作。

然而，从需求手工创建状态机是一个耗时且容易出错的过程。虽然Umple等建模工具简化了状态机的创建和代码生成过程，但开发者或业务分析师仍需将自然语言需求翻译为形式化的状态机模型。这一翻译过程需要：
- 深入理解需求的语义
- 识别系统的状态和事件
- 确定状态之间的迁移关系
- 掌握建模语言的语法

### 研究动机

近年来，大语言模型（LLM）在代码生成领域展现出强大能力。现有研究已探索LLM在生成传统编程语言代码（如Java、Python）方面的表现，但针对建模语言（特别是状态机建模语言）的研究仍然缺乏。

具体而言，现有工作存在以下不足：
1. **缺乏针对状态机生成的研究**：大多数LLM代码生成研究聚焦于功能性编程问题，而非行为建模
2. **缺乏针对小众建模语言的评估**：Umple作为一种嵌入式建模语言，在LLM训练数据中的示例较少
3. **缺乏专用评估指标**：传统代码生成评估指标（如Pass@K）依赖测试用例，但状态机代码无法直接运行测试
4. **缺乏提示工程策略的系统比较**：不同提示策略（Zero-shot、One-shot、RAG）对状态机生成效果的影响尚不明确

### 研究目标

本研究旨在探索使用Llama 3大语言模型从自然语言需求自动生成Umple状态机代码的可行性，具体目标包括：
1. 评估LLM在无示例（Zero-shot）情况下生成Umple状态机的能力
2. 评估提供单个示例（One-shot）对生成质量的影响
3. 评估基于检索增强生成（RAG）的多示例方法的有效性
4. 设计适用于状态机生成的专用评估指标
5. 为用户提供节省时间的自动化建模工具

### 研究意义

本研究的意义在于：
- **填补研究空白**：首次系统性研究LLM在状态机建模语言生成中的应用
- **实用价值**：为简单系统提供快速生成状态机的工具，节省手工建模时间
- **方法论贡献**：提出适用于建模代码的评估指标体系
- **开放未来研究方向**：为更复杂的状态机生成和其他建模语言的研究奠定基础

## 核心方法

### 方法概述

本研究采用Llama 3 (8B参数模型)作为基础模型，结合三种提示工程策略生成Umple状态机代码：
1. **Zero-shot学习**：仅提供需求描述，不提供任何示例
2. **One-shot学习**：提供单个状态机示例作为参考
3. **RAG（检索增强生成）**：根据需求相似度检索多个相关示例

整体流程为：用户提供自然语言需求 → LLM生成Umple代码 → 编译验证 → 质量评估。

### Umple建模语言

**Umple简介**

Umple是一种开源建模技术，允许用户创建UML模型（包括状态机），并可生成传统编程语言代码（如C++、Java）。Umple解决两个主要问题：
1. 允许开发者使用高级文本和可视化表示进行系统开发
2. 减少描述复杂系统所需的代码量

**Umple状态机语法**

基本状态机语法：
```umple
class ClassName {
    StateMachineName {
        State1 {
            event -> State2;
        }
        State2 {
            event -> State1;
        }
    }
}
```

嵌套状态机语法（支持子状态）：
```umple
class ClassName {
  StateMachineName {
    State1 {
      event1 -> Substate2b;
    }
    State2 {
      event2 -> State1;
      Substate2a {
        event2 -> Substate2b;
      }
      Substate2b {
        event3 -> Substate2a;
      }
    }
  }
}
```

**Umple特殊特性**

Umple具有一个独特特性：当遇到无法识别为状态机、关联、属性或方法的代码时，Umple会将其标记为"extra code"（额外代码），并假设这可能是目标编程语言的有效特性，直接在生成的代码中输出。这意味着轻微的语法错误可能被误认为是额外代码，而不会导致编译失败。

### 提示工程策略

**系统消息设计**

所有提示都包含统一的系统消息：
```
You are a helpful AI assistant that designs state machines in the 'Umple'
modeling language based on a set of requirements. You will not describe
or explain the code you have written.
```

**Zero-shot学习**

直接提供需求描述，不提供任何示例：
```
Write a state machine for [系统描述] with the following requirements:
- [需求1]
- [需求2]
...
```

**One-shot学习**

提供一个模拟对话示例，展示理想的输入输出：
```
<user>
Write a state machine for [示例系统描述] with the following requirements:
- [示例需求]
</user>

<assistant>
[示例Umple代码]
</assistant>

<user>
Write a state machine for [目标系统描述] with the following requirements:
- [目标需求]
</user>
```

**RAG方法**

RAG方法包含以下步骤：

1. **构建文档数据库**：收集5个状态机示例，每个示例包含系统描述、需求列表和Umple代码

2. **生成嵌入向量**：
   - 使用Nomic嵌入模型为每个示例生成嵌入向量
   - 为用户需求生成嵌入向量

3. **计算相似度**：使用余弦相似度计算用户需求与每个示例的相似度

4. **选择示例**：按相似度降序排列，选择最相关的N个示例（N=1,2,3,4）

5. **构建提示**：将选中的示例附加到系统消息中，形成多示例提示

6. **生成代码**：LLM基于多个示例生成目标状态机代码

**相似度计算策略**

论文实验了两种相似度计算方式：
- **方式1**：比较用户需求与示例的完整内容（需求+代码）
- **方式2**：仅比较用户需求与示例的需求部分

实验结果显示两种方式差异不大，最终采用方式1。

### 嵌入模型选择

**Nomic嵌入模型**

本研究使用Nomic作为嵌入模型，原因包括：
- 开源且性能优异
- 在多个基准测试中表现出色（MTBE、LoCo benchmark）
- 专门设计用于生成高质量嵌入向量

**嵌入生成过程**

1. **分词（Tokenization）**：将文本分解为token（基于单词和标点符号）
2. **向量化**：将token转换为多维向量
3. **语义编码**：相似含义的token在向量空间中距离更近

### 评估指标设计

本研究设计了一套专门针对状态机生成的评估指标体系：

**1. Invalid Code Percentage (ICP) - 无效代码百分比**

定义：导致Umple代码无法编译的代码行数百分比

计算公式：ICP = (无效代码行数 / 总代码行数) × 100%

意义：衡量生成代码的语法正确性

**2. Extraneous Unparsed Code Percentage (EUCP) - 额外未解析代码百分比**

定义：被Umple标记为"extra code"的代码行数百分比

计算公式：EUCP = (额外代码行数 / 总代码行数) × 100%

意义：衡量生成代码中无法被Umple识别的部分，这些代码通常需要删除或修正

**3. 归一化Levenshtein距离**

定义：生成代码与参考代码之间的编辑距离，归一化到[0,1]区间

计算公式：归一化距离 = Levenshtein距离 / 参考代码长度

Levenshtein距离计算三种编辑操作：插入、删除、替换

意义：衡量用户需要多少"努力"才能将生成代码修正为满足需求的版本

**关键设计决策**：
- 不与"ground truth"比较，而是与生成代码的"修正版本"比较
- 原因：变量名、状态顺序可能不同但功能相同，与ground truth比较会引入不必要的距离
- 归一化的原因：消除系统复杂度的影响，使不同系统的结果可比

**通过阈值**：
- 0.0：完美状态机
- 0.2：优秀（需要少量修改）
- 0.3：良好（需要中等修改）
- 0.5：可接受边界（需要大量修改）

**4. Additional Features (AF) - 额外特性百分比**

定义：LLM尝试添加需求中未提及的额外特性的代码行数百分比

意义：中性指标，取决于用户偏好（有些用户欢迎额外特性，有些用户希望严格遵循需求）

**5. Pass@K**

定义：在K次尝试中生成满足阈值要求的状态机的概率

计算公式：Pass@K = 1 - C(n-c, k) / C(n, k)

其中：n=总生成次数，c=成功次数，k=尝试次数

意义：衡量用户生成K次后获得可用状态机的概率

**6. CodeBLEU**

定义：代码语义相似度的加权平均，包含四个子指标：
- BLEU Score（n-gram匹配）
- Weighted n-gram Match（关键字加权匹配）
- Syntactic AST Match（抽象语法树匹配）
- Semantic Dataflow Match（数据流匹配）

**局限性**：CodeBLEU不支持Umple，论文使用Java作为替代语言，导致除BLEU Score外的三个子指标不准确

### 测试系统

论文使用5个测试系统，涵盖不同复杂度和领域：

**1. Blackjack（21点游戏）**
- 复杂度：中等
- 特点：标准化游戏规则，LLM训练数据中可能有大量相关信息
- 需求数：7条
- 挑战：理解玩家和庄家的轮流机制

**2. Course Section（课程选课）**
- 复杂度：简单
- 特点：来自Umple官方文档，LLM可能见过
- 需求数：7条
- 挑战：需求较模糊，非标准化系统

**3. Credit Card Transaction（信用卡交易）**
- 复杂度：简单
- 特点：需求开放，给LLM较大发挥空间
- 需求数：3条
- 挑战：需求明确指定状态名称

**4. Driver License（驾照系统）**
- 复杂度：复杂
- 特点：安大略省特定规则（G1→G2→G），使用嵌套状态机
- 需求数：8条
- 挑战：地域特定规则，LLM可能混淆不同国家的规则

**5. Hotel Stay（酒店预订）**
- 复杂度：简单
- 特点：线性流程，步骤明确
- 需求数：8条
- 挑战：可选登录步骤

### 实验设计

**实验1：Zero-shot学习**
- 目标：测试LLM在无示例情况下的生成能力
- 方法：仅提供需求描述
- 每个系统生成4次

**实验2：One-shot学习**
- 目标：测试单个示例的影响
- 方法：为每个目标系统提供一个不同的示例
- 每个系统×每个示例组合生成5次迭代
- 总计：5系统 × 4示例 × 5迭代 = 100次生成

**实验3：RAG**
- 目标：测试多示例检索增强的效果
- 方法：根据相似度提供1-4个示例
- 每个系统×每个示例数量生成5次迭代
- 总计：5系统 × 4示例数量 × 5迭代 = 100次生成

**模型选择**

使用Llama 3 (8B参数模型)，原因：
- 在通用、常识、知识、数学推理、阅读理解和代码生成等基准测试中表现优异
- 可在本地机器运行（较大模型需要云端资源）
- 虽然性能不如70B和405B版本，但结合提示工程技术可获得良好效果

## 实验与评估

### 实验1：Zero-shot学习

**实验设置**
- 仅提供需求描述，不提供任何示例
- 每个系统生成4次
- 总计20次生成

**实验结果**

| 系统 | 运行1 | 运行2 | 运行3 | 运行4 |
|------|-------|-------|-------|-------|
| Blackjack | Error | Error | NSF | NSF |
| Course Section | Error | NSF | NSF | NSF |
| Credit Card Transaction | NSF | Error | NSF | Error |
| Driver License | Compiled | NSF | Error | NSF |
| Hotel Stay | Error | Error | NSF | Error |

注：NSF = No State Machine Found（未找到状态机）

**结果分析**

Zero-shot学习完全失败：
- 没有任何运行产生可用的状态机
- 生成的代码主要是嵌入在基本Umple语法中的Java代码
- LLM尝试使用Java风格的逻辑和函数，而非Umple状态机语法
- 即使技术上编译通过的代码，大部分行也被标记为"extra code"
- 生成的状态机充满不可达状态和死胡同状态

**典型错误示例**（Blackjack系统）：
- 使用Java风格的while循环、if语句
- 尝试在状态中定义onEntry函数
- 状态机只有单个迁移和10个状态
- 大量不可达状态

**结论**：Zero-shot方法对用户毫无价值，生成的代码需要完全重写，无法节省时间。

### 实验2：One-shot学习

**实验设置**
- 为每个目标系统提供一个不同的示例
- 每个系统×每个示例组合生成5次迭代
- 总计100次生成

**语法分析结果**

| 指标 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| 平均ICP | 2% (σ=0.11) | 0% (σ=0.00) | 0% (σ=0.00) | 0% (σ=0.00) | 0% (σ=0.01) |
| 平均EUCP | 5% (σ=0.12) | 1% (σ=0.01) | 1% (σ=0.01) | 0% (σ=0.00) | 1% (σ=0.01) |
| 归一化Levenshtein距离 | 0.46 (σ=0.46) | 0.18 (σ=0.18) | 0.13 (σ=0.17) | 0.29 (σ=0.16) | 0.17 (σ=0.28) |
| 平均AF | 0.85 (σ=0.36) | 0.50 (σ=0.50) | 0.80 (σ=0.40) | 0.35 (σ=0.48) | 0.55 (σ=0.50) |

**关键发现**：

1. **编译质量显著提升**：ICP和EUCP都非常低，大多数生成的代码可以编译

2. **系统性能排名**（按归一化Levenshtein距离）：
   - 最佳：Credit Card Transaction (0.13) - 需求开放，系统简单
   - 第二：Hotel Stay (0.17) - 线性指令流程
   - 第三：Course Section (0.18) - 简单教学示例
   - 第四：Driver License (0.29) - 安大略特定规则
   - 最差：Blackjack (0.46) - 未能理解轮流机制

3. **额外特性分析**：
   - Blackjack和Credit Card Transaction的AF最高（0.85和0.80）
   - LLM倾向于添加常见的安全检查和游戏规则
   - 简单特性通常实现正确，不会增加修正负担

**Pass@K分析**

Pass@1（生成1次的成功率）：

| 阈值 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| 0.0 | 0% | 5% | 25% | 0% | 25% |
| 0.2 | 20% | 60% | 75% | 40% | 85% |
| 0.3 | 65% | 95% | 85% | 60% | 85% |
| 0.5 | 85% | 95% | 90% | 80% | 85% |

Pass@5（生成5次的成功率）：

| 阈值 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| 0.0 | 0% | 25% | 81% | 0% | 81% |
| 0.2 | 72% | 100% | 100% | 95% | 100% |
| 0.3 | 99% | 100% | 100% | 100% | 100% |
| 0.5 | 100% | 100% | 100% | 100% | 100% |

**语义分析（CodeBLEU）**

| 指标 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| BLEU Score | 0.75 (σ=0.04) | 0.65 (σ=0.09) | 0.86 (σ=0.09) | 0.71 (σ=0.22) | 0.59 (σ=0.02) |
| CodeBLEU | 0.47 (σ=0.06) | 0.42 (σ=0.05) | 0.48 (σ=0.05) | 0.35 (σ=0.05) | 0.37 (σ=0.04) |

**重要发现**：BLEU Score排名与归一化Levenshtein距离排名几乎完全相反（除Credit Card Transaction外），暗示可能存在负相关关系。

**结论**：One-shot学习对简单系统有效，可以节省用户时间，但对复杂系统（如Blackjack）效果较差。

### 实验3：RAG（检索增强生成）

**实验设置**
- 根据余弦相似度选择1-4个最相关示例
- 每个系统×每个示例数量生成5次迭代
- 总计100次生成

**相似度分析**

示例平均相似度排名（从高到低）：
1. Credit Card Transaction - 0.60
2. Hotel Stay - 0.59
3. Driver License - 0.58
4. Blackjack - 0.54
5. Course Section - 0.53

**语法分析结果**

| 指标 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| 平均ICP | 0% (σ=0.03) | 0% (σ=0.00) | 0% (σ=0.00) | 0% (σ=0.01) | 0% (σ=0.00) |
| 平均EUCP | 2% (σ=0.02) | 0% (σ=0.01) | 0% (σ=0.01) | 0% (σ=0.00) | 0% (σ=0.00) |
| 归一化Levenshtein距离 | 0.31 (σ=0.15) | 0.31 (σ=0.11) | 0.25 (σ=0.26) | 0.32 (σ=0.13) | 0.07 (σ=0.09) |
| 平均AF | 0.70 (σ=0.50) | 0.35 (σ=0.48) | 0.50 (σ=0.50) | 0.25 (σ=0.43) | 0.35 (σ=0.48) |

**关键发现**：

1. **编译质量进一步提升**：
   - ICP和EUCP显著低于One-shot
   - 更多示例帮助LLM更好理解Umple语法

2. **额外特性减少**：AF普遍降低，说明更多示例使LLM更"保守"，更严格遵循需求

3. **系统性能排名变化**（按归一化Levenshtein距离）：
   - 最佳：Hotel Stay (0.07) - 相比One-shot的0.17大幅改进
   - 第二：Credit Card Transaction (0.25) - 相比One-shot的0.13有所退步
   - 第三：Course Section (0.31) - 相比One-shot的0.18有所退步
   - 第四：Blackjack (0.31) - 相比One-shot的0.46显著改进
   - 最差：Driver License (0.32) - 相比One-shot的0.29略有退步

4. **性能不一致性**：
   - Hotel Stay和Blackjack显著改进
   - Credit Card Transaction和Course Section反而退步
   - 说明RAG不是对所有系统都有效

**Pass@K分析**

Pass@1（生成1次的成功率）：

| 阈值 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| 0.0 | 0% | 0% | 25% | 0% | 30% |
| 0.2 | 40% | 25% | 55% | 10% | 85% |
| 0.3 | 50% | 50% | 70% | 45% | 95% |
| 0.5 | 75% | 95% | 80% | 90% | 95% |

Pass@5（生成5次的成功率）：

| 阈值 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| 0.0 | 0% | 0% | 81% | 0% | 87% |
| 0.2 | 95% | 81% | 99% | 45% | 100% |
| 0.3 | 98% | 98% | 100% | 97% | 100% |
| 0.5 | 100% | 100% | 100% | 100% | 100% |

**语义分析（CodeBLEU）**

| 指标 | Blackjack | Course Section | Credit Card Transaction | Driver License | Hotel Stay |
|------|-----------|----------------|-------------------------|----------------|------------|
| BLEU Score | 0.74 (σ=0.17) | 0.60 (σ=0.15) | 0.84 (σ=0.12) | 0.65 (σ=0.12) | 0.54 (σ=0.18) |
| CodeBLEU | 0.47 (σ=0.07) | 0.38 (σ=0.05) | 0.44 (σ=0.05) | 0.34 (σ=0.03) | 0.35 (σ=0.05) |

**重要发现**：BLEU Score排名与One-shot完全一致，再次确认BLEU Score与归一化Levenshtein距离无相关性。

**示例数量影响分析**

不同系统对示例数量的敏感度不同：
- Blackjack：1个和4个示例效果最好，2-3个示例反而较差
- Driver License：示例数量越多，性能越好（呈单调改进趋势）
- 其他系统：示例数量影响不明显

### 三种方法对比总结

| 方法 | 平均归一化Levenshtein距离 | 方差 | 优势 | 劣势 |
|------|---------------------------|------|------|------|
| Zero-shot | N/A（完全失败） | N/A | 无需示例 | 完全不可用 |
| One-shot | 0.246 | 较高 | 简单易用 | 性能不稳定 |
| RAG | 0.244 | 较低 | 更一致 | 需要示例库，性能提升有限 |

**关键结论**：
1. Zero-shot完全不可行
2. One-shot和RAG平均性能接近（0.246 vs 0.244）
3. RAG方差更小，更一致可靠
4. 对于简单系统（如Hotel Stay），RAG显著优于One-shot
5. 对于某些系统（如Credit Card Transaction），One-shot反而更好

### 研究问题答案

**RQ1：LLM能否在无示例情况下生成Umple状态机？**

答案：**不能**。Zero-shot学习完全失败，生成的代码无法使用，对用户毫无价值。

**RQ2：LLM能否使用单个示例生成Umple状态机？**

答案：**部分可以**。归一化Levenshtein距离范围0.13-0.46，4/5系统低于0.30。对于愿意编辑代码的用户，可以节省时间。

**RQ3：LLM能否使用RAG方法生成Umple状态机？**

答案：**可以，且更一致**。归一化Levenshtein距离范围0.07-0.32，方差更小。对于简单系统效果显著，但对所有系统的平均改进有限。

## 与本研究的关系

### 相关性分析

本论文与博士研究"基于控制系统软件需求的LLM状态机结构化建模方法"高度相关，具体体现在：

**1. 研究目标的一致性**

两者都聚焦于使用LLM从自然语言需求自动生成状态机模型：
- 本论文：从需求生成Umple状态机代码
- 博士研究：从控制系统需求生成带时间约束和守卫条件的层次化状态机

**2. 核心挑战的共通性**

- **需求理解**：如何让LLM准确理解自然语言需求的语义
- **形式化转换**：如何将非形式化需求转换为形式化状态机模型
- **语法正确性**：如何确保生成的状态机符合目标语言语法
- **语义正确性**：如何确保生成的状态机满足功能需求

**3. 方法论的可借鉴性**

- **提示工程策略**：Zero-shot、One-shot、RAG的系统比较
- **示例检索机制**：基于嵌入向量和余弦相似度的示例选择
- **评估指标设计**：针对无法直接测试的建模代码设计专用指标

**4. 应用场景的差异**

- 本论文：通用状态机（游戏、业务流程等），简单系统
- 博士研究：控制系统状态机，涉及时间约束、安全性质、形式化验证

### 可借鉴之处

**1. 评估指标体系**

本论文提出的评估指标对博士研究具有重要参考价值：

**归一化Levenshtein距离**：
- 优点：直观衡量"修正努力"，适用于无测试用例的场景
- 可借鉴：用于评估生成状态机与参考模型的结构差异
- 改进方向：结合状态机语义等价性判断，避免仅基于字符串编辑距离

**ICP和EUCP指标**：
- 优点：分别衡量语法错误和无法识别的代码
- 可借鉴：设计针对时间自动机的语法正确性指标
- 改进方向：增加时间约束语法、守卫条件语法的专项检查

**Pass@K指标**：
- 优点：衡量多次生成的成功概率，符合实际使用场景
- 可借鉴：评估迭代生成策略的有效性
- 改进方向：结合形式化验证结果定义"成功"

**2. 提示工程策略**

**RAG方法的有效性**：
- 发现：RAG相比One-shot平均性能提升有限（0.246 vs 0.244），但方差更小
- 启示：对于控制系统状态机，RAG可能更适合，因为控制系统需求更规范、更结构化
- 改进方向：
  - 构建控制系统领域的状态机示例库
  - 设计领域特定的相似度计算方法（考虑时间约束、安全性质等）
  - 探索动态示例数量选择策略

**示例检索策略**：
- 发现：不同系统对示例数量的敏感度不同
- 启示：需要根据需求复杂度动态调整示例数量
- 改进方向：
  - 基于需求复杂度（状态数、事件数、时间约束数）预测最优示例数量
  - 探索示例多样性与相似度的平衡

**3. 模型选择与资源约束**

- 发现：8B参数的Llama 3结合提示工程可获得可用结果
- 启示：不一定需要最大模型，中等规模模型+精心设计的提示可能更实用
- 改进方向：
  - 测试不同规模模型（8B、70B、405B）在控制系统状态机生成中的性能
  - 探索模型规模与提示复杂度的权衡

**4. 失败案例分析**

**Zero-shot完全失败的原因**：
- Umple是小众语言，LLM训练数据中示例极少
- 启示：对于时间自动机等更专业的形式化语言，Zero-shot可能更不可行
- 应对策略：必须提供示例，考虑Few-shot或RAG

**复杂系统性能下降**：
- Blackjack（轮流机制）和Driver License（地域特定规则）表现较差
- 启示：控制系统的时间约束、并发状态等复杂特性可能导致类似问题
- 应对策略：
  - 将复杂需求分解为子任务
  - 为复杂特性（如时间约束）设计专门的提示模板
  - 引入迭代修复机制

### 存在的不足

**1. 测试系统的局限性**

- **规模小**：仅5个系统，状态数5-27，不足以验证可扩展性
- **复杂度低**：未涉及时间约束、守卫条件、并发状态等高级特性
- **领域单一**：缺乏控制系统领域的测试案例
- **对博士研究的影响**：需要在更大规模、更复杂的控制系统数据集上验证方法

**2. 评估指标的局限性**

- **缺乏语义验证**：归一化Levenshtein距离仅衡量结构差异，无法验证功能正确性
- **缺乏形式化验证**：未集成模型检查工具验证生成状态机的性质
- **CodeBLEU不适用**：使用Java替代Umple导致结果不准确
- **对博士研究的影响**：必须引入形式化验证（如UPPAAL）作为评估手段

**3. 模型能力的局限性**

- **小模型限制**：8B参数模型性能有限，论文承认更大模型可能表现更好
- **无迭代修复**：生成后无法根据编译错误或验证反馈进行修复
- **无结构化输出**：依赖LLM直接生成代码，缺乏结构化引导
- **对博士研究的影响**：需要探索更大模型、迭代修复机制、结构化生成方法

**4. 方法论的局限性**

- **缺乏任务分解**：将整个状态机生成视为单一任务，未分解为子任务（如状态识别、迁移生成）
- **缺乏领域知识注入**：未利用控制系统领域的先验知识
- **缺乏验证反馈循环**：生成后无法根据验证结果迭代改进
- **对博士研究的影响**：需要设计多阶段生成方法、领域知识库、验证驱动的迭代修复

**5. 实验设计的局限性**

- **缺乏消融实验**：未单独测试提示各组成部分的贡献
- **缺乏人类评估**：仅依赖自动指标，未进行用户研究
- **缺乏错误分析**：未系统分类和分析生成错误的类型
- **对博士研究的影响**：需要更严格的实验设计和更全面的评估

### 对本研究的启发

**1. 研究方法启发**

**分阶段生成策略**：
- 借鉴：不要一次性生成完整状态机，而是分阶段生成
- 具体方案：
  - 阶段1：从需求识别状态和事件
  - 阶段2：生成状态迁移关系
  - 阶段3：添加时间约束和守卫条件
  - 阶段4：验证和修复

**示例库构建**：
- 借鉴：构建高质量的控制系统状态机示例库
- 具体方案：
  - 收集101条功能安全需求对应的状态机模型
  - 为每个示例标注领域特征（如时间约束类型、安全性质类型）
  - 设计领域特定的相似度计算方法

**评估指标设计**：
- 借鉴：结合语法指标和语义指标
- 具体方案：
  - 语法指标：时间约束语法正确性、守卫条件语法正确性
  - 结构指标：状态覆盖率、迁移覆盖率、归一化编辑距离
  - 语义指标：形式化验证通过率、性质满足率
  - 实用指标：人工修正时间、用户满意度

**2. 技术路线启发**

**提示工程优化**：
- 设计控制系统领域的专用提示模板
- 引入Chain-of-Thought引导LLM逐步推理
- 探索Self-Consistency等提高生成质量的技术

**检索增强优化**：
- 不仅检索完整示例，还检索状态机片段（如时间约束模式、守卫条件模式）
- 设计多层次检索策略（系统级、特性级、模式级）
- 探索动态示例选择和组合策略

**迭代修复机制**：
- 集成形式化验证工具（如UPPAAL）
- 根据验证反馈生成修复提示
- 设计验证驱动的迭代生成循环

**3. 研究创新点启发**

本论文的不足正是博士研究的创新机会：

**创新点1：面向控制系统的领域适配**
- 本论文：通用状态机，无领域知识
- 博士研究：注入控制系统领域知识，设计领域特定提示

**创新点2：时间约束和守卫条件的生成**
- 本论文：仅生成基本状态机
- 博士研究：生成带时间约束和守卫条件的时间自动机

**创新点3：形式化验证集成**
- 本论文：仅评估语法和结构
- 博士研究：集成UPPAAL进行性质验证，形成闭环

**创新点4：迭代修复机制**
- 本论文：一次性生成，无修复
- 博士研究：基于验证反馈的迭代修复

**创新点5：多阶段结构化生成**
- 本论文：端到端单阶段生成
- 博士研究：分阶段生成（状态识别→迁移生成→约束添加→验证修复）

**4. 实验设计启发**

**数据集构建**：
- 使用9个控制系统的101条功能安全需求
- 确保数据集涵盖不同复杂度和领域特征
- 标注每个需求的难度级别和特性类型

**基线方法选择**：
- 包含本论文的方法（Zero-shot、One-shot、RAG）作为基线
- 对比传统方法（基于规则、基于模板）
- 对比其他LLM方法（GPT-4、Claude等）

**评估维度**：
- 语法正确性（编译通过率）
- 结构正确性（状态/迁移覆盖率）
- 语义正确性（验证通过率、性质满足率）
- 实用性（修正时间、用户满意度）

### 总结

本论文为博士研究提供了重要的方法论基础和实证参考：

**可直接借鉴的**：
- 归一化Levenshtein距离等评估指标
- RAG方法的基本框架
- 提示工程的设计思路

**需要改进的**：
- 扩展到更复杂的状态机特性（时间约束、守卫条件）
- 引入形式化验证作为评估手段
- 设计迭代修复机制
- 注入控制系统领域知识

**创新机会**：
- 多阶段结构化生成方法
- 验证驱动的迭代修复
- 领域特定的提示工程
- 时间自动机的专用评估指标

本论文证明了LLM在状态机生成中的可行性，但也揭示了在复杂控制系统场景下需要解决的关键挑战，这些挑战正是博士研究的核心创新点。


## 重要的相关工作

本论文共引用32篇文献，按作用分类如下：

### 1. 重要的前身类工作

本论文没有明确的前身工作，这是一项探索性研究，首次将LLM应用于Umple状态机生成。

### 2. 直接参与实验的baseline

本论文没有使用其他方法作为实验对比基线，而是对比了三种提示工程策略（Zero-shot、One-shot、RAG）的效果。

### 3. 提供了重要论证的工作

**3.1 Liu et al. (2024) - ChatGPT代码生成质量评估**

- **标题**: No Need to Lift a Finger Anymore? Assessing the Quality of Code Generation by ChatGPT
- **作者**: Zhihan Liu, Yangtian Tang, Xiaohong Luo, Yifan Zhou, Lingming Zhang
- **发表**: IEEE Transactions on Software Engineering, 2024
- **DOI**: 10.1109/TSE.2024.3392499

**主要内容**:
- 研究ChatGPT在生成传统编程语言代码（C, C++, Java, Python, JavaScript）方面的能力
- 使用公开的编程问题数据集，包含明确的测试用例和错误信息
- 定义了功能性分类：Accepted、Wrong Answer、Compile Error、Time Limit Exceeded、Runtime Error
- 定义了错误类型分类：Wrong Detail、Misunderstanding Certain Content、Misunderstanding Problems

**论文中的引用**:
- 第651-654行："Since their code returned specific errors, their results can be fed back into the prompt they used. In the context of this thesis though, since there is no way to automatically check the output of a state machine (besides checking if the results are compilable) a transformer cannot improve on its output without human intervention."
- 第656-659行："Liu used well known programming languages (C, C++, Java, Python, and JavaScript), of which ChatGPT has learned countless examples. This contrasts with the work of this thesis where we are attempting to generate state machine code written in Umple."
- 第664-667行："ChatGPT had a poor success rate in completing the questions asked by Liu's team. The most successful language (Python3) had a total success rate of 23.93% on problems it had not seen before."

**主要发现**:
- ChatGPT在传统编程语言上的成功率较低（Python3最高仅23.93%）
- 简单问题成功率57.30%，中等问题18.13%，困难问题2.20%
- 使用GPT-3.5（175B参数）

**与本论文的关系**:
- 论证了即使在训练数据丰富的传统编程语言上，LLM的代码生成能力也有限
- 对比说明Umple作为小众语言面临更大挑战
- 启发本论文不能依赖自动测试反馈，需要设计专用评估指标

**佐证内容**:
- 论证了LLM代码生成的局限性，为本研究设定合理预期
- 说明了测试用例驱动评估的局限性，支持本论文设计归一化Levenshtein距离等指标

**3.2 Liu et al. (2023) - LLM代码生成的严格评估**

- **标题**: Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation
- **作者**: Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, Lingming Zhang
- **发表**: Advances in Neural Information Processing Systems, 2023
- **arXiv**: 2305.01210v3

**主要内容**:
- 提出严格评估LLM代码生成质量的方法
- 讨论代码覆盖率（code coverage）和变异测试（mutant killings）等指标
- 指出经典NLP指标（如BLEU score）在代码生成评估中不再可靠

**论文中的引用**:
- 第691-693行："These functionality metrics are related to the results of functional tests. In our work in this thesis, we do not have a comprehensive set of test cases, so we are not able to use the above approach without adaptation."
- 第781-783行："As stated in the evaluation of LLMs for code generation paper, 'classic NLP metrics like BLEU score are no longer reliable in the context of program synthesis'."

**与本论文的关系**:
- 论证了传统NLP指标（BLEU score）在代码生成评估中的局限性
- 支持本论文设计专用评估指标（ICP、EUCP、归一化Levenshtein距离）
- 说明了测试用例方法不适用于状态机生成的原因

**佐证内容**:
- 论证了本研究需要创新评估方法的必要性
- 解释了为什么不能直接使用传统代码生成评估指标


**3.3 Iyer et al. (2018) - 程序化上下文中的语言到代码映射**

- **标题**: Mapping Language to Code in Programmatic Context
- **作者**: Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, Luke Zettlemoyer
- **发表**: EMNLP 2018
- **DOI**: 10.18653/v1/D18-1192

**主要内容**:
- 早期使用Transformer生成Java代码的研究
- 提出简单的严重性描述符来评估生成代码质量
- 分类：Totally Wrong、Marginally Correct、Mostly Correct、Exact Match、Semantically Equivalent

**论文中的引用**:
- 第718-724行（Section 2.12.1）：论文引用其评估分类方法

**与本论文的关系**:
- 提供了早期代码生成评估的分类思路
- 启发本论文设计ICP、EUCP等分类指标

**佐证内容**:
- 为代码质量评估提供了定性分类的参考框架

**3.4 Corso et al. (2024) - AI代码助手生成Java方法的实证评估**

- **标题**: Generating Java Methods: An Empirical Assessment of Four AI-Based Code Assistants
- **作者**: Valerio Corso, Leonardo Mariani, Daniela Micucci, Oliviero Riganelli
- **发表**: ICPC 2024
- **DOI**: 10.1145/3643916.3644402

**主要内容**:
- 评估四种AI代码助手生成Java方法的能力
- 定义了明确的评估标准：Correct（通过所有测试+人工审查）、Plausible（通过测试但未通过审查）、Incorrect（未通过测试）、Invalid（无法编译）
- 与本论文不同，有明确的测试用例

**论文中的引用**:
- 第725-732行（Section 2.12.1）：引用其评估分类方法

**与本论文的关系**:
- 提供了更严格的代码质量评估标准
- 对比说明本论文缺乏测试用例的挑战

**佐证内容**:
- 论证了有测试用例和无测试用例评估方法的差异

**3.5 Millam & Bakke (2024) - AI助手生成简洁代码的能力**

- **标题**: Coding with AI as an Assistant: Can AI Generate Concise Computer Code?
- **作者**: Andrew Millam, Cory Bakke
- **发表**: Journal of Information Technology Education: Innovations in Practice, 2024
- **DOI**: 10.28945/5362

**主要内容**:
- 评估AI代码助手的实用性
- 提出评估指标：Extraneous code（无用代码行数和字符数）、Major modifications（需要重大修改）、Minor modifications（需要轻微修改）
- 设定阈值判断AI助手是否"通过"

**论文中的引用**:
- 第733-743行（Section 2.12.1）：引用其评估指标，特别是"extraneous code"概念

**与本论文的关系**:
- 直接启发本论文设计EUCP（Extraneous Unparsed Code Percentage）指标
- 提供了代码实用性评估的思路

**佐证内容**:
- 为本论文的EUCP指标提供了理论依据
- 说明了评估"无用代码"的重要性

**3.6 Odu et al. (2024) - 使用LLM自动实例化保证案例**

- **标题**: Automatic Instantiation of Assurance Cases from Patterns Using Large Language Models
- **作者**: Olusola Odu, Alvine Belle, Shuai Wang, Segla Kpodjedo, Timothy Lethbridge, Hadi Hemmati
- **发表**: Journal of Systems and Software, 2024
- **DOI**: 10.1016/j.jss.2025.112353

**主要内容**:
- 使用LLM生成保证案例（assurance cases）
- 面临与本论文类似的问题：输出是自然语言而非可测试代码
- 使用NLP指标评估：Exact Match、BLEU Score、Semantic Similarity（余弦相似度）

**论文中的引用**:
- 第757-776行（Section 2.12.2）：详细引用其评估方法

**与本论文的关系**:
- 面临类似的评估挑战（无法直接测试输出）
- 提供了使用NLP指标评估建模输出的参考
- 但论文指出这些指标对代码生成不够可靠

**佐证内容**:
- 论证了NLP指标在建模输出评估中的局限性
- 支持本论文设计专用指标的必要性

### 4. 在技术上提供了支持的工作

**4.1 Lethbridge et al. (2021) - Umple建模工具**
- 标题: Umple: Model-driven development for open source and education
- 作者: Timothy Lethbridge, Andrew Forward, Omar Badreddin et al.
- 发表: Science of Computer Programming, 2021
- DOI: 10.1016/j.scico.2021.102665
- 论文中的引用: 第319-325行，详细描述Umple的功能和目标
- 与本论文的关系: 本论文的核心技术基础，定义了生成目标
- 技术使用: 直接使用Umple作为目标建模语言，使用Umple编译器验证生成代码

**4.2 Grattafiori et al. (2024) - Llama 3模型族**
- 标题: The Llama 3 Herd of Models
- arXiv: 2407.21783v3
- 论文中的引用: 第410-413行、第800-803行
- 与本论文的关系: 本论文使用的核心LLM模型
- 技术使用: 直接使用Llama 3 (8B)作为生成模型

**4.3 Brown et al. (2020) - Few-Shot学习**
- 标题: Language Models are Few-Shot Learners
- arXiv: 2005.14165v4
- 与本论文的关系: 提供了提示工程的理论基础
- 技术使用: 直接采用Few-shot学习范式，设计One-shot和Multi-shot提示策略

**4.4 Gao et al. (2024) - 检索增强生成综述**
- 标题: Retrieval-Augmented Generation for Large Language Models: A Survey
- arXiv: 2312.10997v5
- 论文中的引用: 第597-606行
- 与本论文的关系: 提供了RAG方法的理论框架
- 技术使用: 直接采用RAG方法，构建状态机示例数据库

**4.5 Nussbaum et al. (2024) - Nomic嵌入模型**
- 标题: Nomic Embed: Training a Reproducible Long Context Text Embedder
- arXiv: 2402.01613v2
- 论文中的引用: 第387-390行
- 与本论文的关系: 提供了高质量的嵌入生成能力
- 技术使用: 直接使用Nomic生成嵌入向量，用于计算需求与示例的相似度

**4.6 Vaswani et al. (2017) - Transformer架构**
- 标题: Attention is All you Need
- arXiv: 1706.03762v7
- 论文中的引用: 第393-396行，Figure 3展示了Transformer架构图
- 与本论文的关系: 提供了Llama 3的理论基础
- 技术使用: Llama 3基于Transformer架构（decoder-only）

**4.7 Chen et al. (2021) - Pass@K评估指标**
- 标题: Evaluating Large Language Models Trained on Code
- arXiv: 2107.03374v2
- 论文中的引用: 第527-550行
- 与本论文的关系: 提供了多次生成成功率的评估方法
- 技术使用: 直接采用Pass@K指标，计算Pass@1、Pass@5、Pass@10

**4.8 Ren et al. (2020) - CodeBLEU评估指标**
- 标题: CodeBLEU: a Method for Automatic Evaluation of Code Synthesis
- arXiv: 2009.10297v2
- 论文中的引用: 第557-559行、第1440-1448行
- 与本论文的关系: 提供了代码语义相似度评估方法
- 技术使用: 使用CodeBLEU评估生成代码与ground truth的相似度

**4.9 Papineni et al. (2002) - BLEU评估指标**
- 标题: BLEU: a method for automatic evaluation of machine translation
- DOI: 10.3115/1073083.1073135
- 论文中的引用: 第560-562行
- 与本论文的关系: 提供了文本相似度评估的基础方法
- 技术使用: 作为CodeBLEU的一部分使用

**4.10 Han et al. (2012) - 余弦相似度**
- 标题: Data Mining: Concepts and Techniques
- DOI: 10.1016/B978-0-12-381479-1.00002-2
- 论文中的引用: 第513-516行
- 与本论文的关系: 提供了相似度计算的数学基础
- 技术使用: 使用余弦相似度计算需求与示例的相似度

**4.11 Mikolov et al. (2013) - Word2Vec嵌入方法**
- 标题: Efficient Estimation of Word Representations in Vector Space
- arXiv: 1301.3781v3
- 论文中的引用: 第385-387行
- 与本论文的关系: 提供了嵌入生成的早期方法
- 技术使用: 作为嵌入方法的背景知识（未直接使用）

### 5. 其他重要工作

**5.1 Harel (1987) - Statecharts形式化**
- 标题: Statecharts: a visual formalism for complex systems
- DOI: 10.1016/0167-6423(87)90035-9
- 与本论文的关系: 提供状态机的理论基础和形式化定义
- 作用: 理论基础

**5.2 Hou et al. (2024) - LLM软件工程系统综述**
- 标题: Large Language Models for Software Engineering: A Systematic Literature Review
- DOI: 10.1145/3695988
- 与本论文的关系: 提供LLM在软件工程中应用的背景知识
- 作用: 背景知识

**5.3 Hey et al. (2020) - NoRBERT需求分类**
- 标题: NoRBERT: Transfer learning for requirements classification
- DOI: 10.1109/RE48521.2020.00028
- 与本论文的关系: 提供Transformer在需求工程中应用的参考
- 作用: 背景知识

**5.4 Lewis et al. (2020) - RAG原始论文**
- 标题: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- arXiv: 2005.11401v4
- 与本论文的关系: RAG方法的原始提出
- 作用: 理论基础

**5.5 Li et al. (2022) - AlphaCode竞赛级代码生成**
- 标题: Competition-Level Code Generation with AlphaCode
- DOI: 10.1126/science.abq1158
- 与本论文的关系: 展示LLM在复杂代码生成中的能力
- 作用: 背景知识

**5.6 Merseguer et al. (2002) - UML状态机语义**
- 标题: A compositional semantics for UML state machines aimed at performance evaluation
- DOI: 10.1109/WODES.2002.1167702
- 与本论文的关系: 提供UML状态机的形式化语义
- 作用: 理论基础

**5.7 Muennighoff et al. (2023) - MTBE嵌入基准测试**
- 标题: MTBE: Massive Text Embedding Benchmark
- DOI: 10.18653/v1/2023.eacl-main.148
- 与本论文的关系: Nomic模型的评估基准
- 作用: 评估方法

**5.8 Saad-Falcon et al. (2024) - LoCo长上下文检索基准**
- 标题: Benchmarking and Building Long-Context Retrieval Models with LoCo and M2-BERT
- DOI: 10.5555/3692070.3693819
- 与本论文的关系: Nomic模型的评估基准
- 作用: 评估方法

**5.9 Shehata et al. (2024) - 使用LLM创建UML类图**
- 标题: Creating UML Class Diagrams with General-Purpose LLMs
- DOI: 10.1109/VISSOFT64034.2024.00031
- 与本论文的关系: LLM在UML建模中的应用
- 作用: 相关研究

**5.10 Sveidqvist (2024) - Mermaid AI图表生成**
- 标题: Mermaid AI Is Here to Change the Game For Diagram Creation
- 与本论文的关系: 论文在未来工作中提到可以使用Mermaid进行类似研究
- 作用: 未来工作方向

**5.11 Tang et al. (2023) - 开发者验证和修复AI生成代码的行为**
- 标题: An Empirical Study of Developer Behaviours for Validating and Repairing AI-Generated Code
- arXiv: 2405.16081
- 与本论文的关系: 提供AI代码生成实用性的参考
- 作用: 背景知识

**5.12 Touvron et al. (2023) - Llama 2模型**
- 标题: Llama 2: Open Foundation and Fine-Tuned Chat Models
- arXiv: 2307.09288v2
- 与本论文的关系: Llama 3的前身模型
- 作用: 背景知识

**5.13 Yenduri et al. (2024) - GPT综合综述**
- 标题: Generative Pre-trained Transformer: A Comprehensive Review on Enabling Technologies
- DOI: 10.1109/ACCESS.2024.3389497
- 与本论文的关系: 提供GPT技术的全面背景
- 作用: 背景知识

**5.14 Wang et al. (2024) - 使用LLM改进文本嵌入**
- 标题: Improving Text Embeddings with Large Language Models
- DOI: 10.18653/v1/2024.acl-long.642
- 与本论文的关系: 提供嵌入生成的理论支持
- 作用: 理论基础

**5.15 Rabbi et al. (2024) - ChatGPT Python代码分析**
- 标题: AI Writes, We Analyze: The ChatGPT Python Code Saga
- DOI: 10.1145/3643991.3645076
- 与本论文的关系: LLM代码生成的相关研究
- 作用: 背景知识

**5.16 Shen et al. (2024) - SlimPajama数据集**
- 标题: SlimPajama-DC: Understanding Data Combinations for LLM Training
- arXiv: 2309.10818v3
- 与本论文的关系: LLM训练数据的研究
- 作用: 背景知识

**5.17 Awais et al. (2025) - 基础模型综述**
- 标题: Foundation Models Defining a New Era in Vision: A Survey and Outlook
- DOI: 10.1109/TPAMI.2024.3506283
- 与本论文的关系: 提供基础模型的背景知识
- 作用: 背景知识

**5.18 Adler-Nissen & Drieschova (2019) - Track-Change外交**
- 标题: Track-Change Diplomacy: Technology, Affordances, and the Practice of International Negotiations
- DOI: 10.1093/ISQ/SQZ030
- 与本论文的关系: 关于技术如何改变工作流程的参考
- 作用: 背景知识

**5.19 David (2024) - OpenAI GPT商标**
- 标题: OpenAI can't register 'GPT' as a trademark — yet
- 与本论文的关系: GPT术语的背景信息
- 作用: 背景知识

**5.20 Meta (2024) - Llama 3提示格式文档**
- 标题: Llama 3 | Model Cards & Prompt formats
- 与本论文的关系: 提供Llama 3的官方提示格式规范
- 作用: 技术文档

**5.21 OpenAI (2025) - Tokenizer工具**
- 标题: Tokenizer
- 与本论文的关系: 提供分词示例（Figure 2）
- 作用: 技术文档

**5.22 Umple (2025) - Umple用户手册**
- 标题: Umple User Manual
- 与本论文的关系: 提供Umple语法和特性的详细文档
- 作用: 技术文档

## 文献分类总结

本论文共引用32篇文献，按作用分类如下：

1. **前身类工作（0篇）**：本研究是探索性工作，无直接前身
2. **实验baseline（0篇）**：对比三种提示策略，无外部baseline
3. **论证支持（6篇）**：Liu 2024、Liu 2023、Iyer 2018、Corso 2024、Millam 2024、Odu 2024
4. **技术支持（11篇）**：Lethbridge 2021、Grattafiori 2024、Brown 2020、Gao 2024、Nussbaum 2024、Vaswani 2017、Chen 2021、Ren 2020、Papineni 2002、Han 2012、Mikolov 2013
5. **其他支持（15篇）**：理论基础、背景知识、评估方法、技术文档等

本论文的核心创新在于：
- 首次将LLM应用于Umple状态机生成
- 设计了专用评估指标（ICP、EUCP、归一化Levenshtein距离）
- 系统比较了Zero-shot、One-shot和RAG三种方法

实验结果表明，RAG方法在简单系统上表现最佳（Hotel Stay归一化距离0.07），但对所有系统的平均改进有限（0.244 vs 0.246）。Zero-shot方法完全失败，One-shot方法对简单系统有效。
