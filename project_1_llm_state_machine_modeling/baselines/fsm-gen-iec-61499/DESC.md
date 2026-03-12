# 基于LLM的有限状态机迭代需求精化与IEC 61499代码生成 / LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation

## 基本信息

- **标题**：LLM-based Iterative Requirements Refinement in FSM with IEC 61499 Code Generation
- **中文标题**：基于LLM的有限状态机迭代需求精化与IEC 61499代码生成
- **作者**：Valeriy Vyatkin, Sandeep Patil, Dmitrii Drozdov, Anatoly Shalyto
- **单位**：
  - Aalto University (芬兰阿尔托大学)
  - Luleå University of Technology (瑞典吕勒奥理工大学)
  - Flexbridge AB (瑞典)
  - Independent researcher
- **发表**：2025 IEEE 23rd International Conference on Industrial Informatics (INDIN)
- **年份**：2025
- **页码**：1-7
- **DOI/链接**：https://ieeexplore.ieee.org/abstract/document/11279575/

### 代码/仓库获取方式

- **工具演示视频**：https://www.youtube.com/live/aR20KBmZnA4?si=wxyMOcAX4tirRgQf
- **开发方**：Flexbridge AB (Universal Automation)
- **注意**：原文未提供公开代码仓库链接，仅提供了工具演示视频。fbAssistant是Flexbridge AB开发的概念验证工具原型。

### 数据集获取方式

- **使用案例**：
  1. 气动缸（Pneumatic Cylinder）系统 - 论文中详细描述了系统接口和行为规范
  2. 拾取放置机械手（Pick and Place Manipulator）- 论文中提供了系统描述和状态机
- **注意**：原文未提供公开数据集下载链接，案例系统的详细规范在论文正文中描述（第3-6页）。

## 简报

**解决的问题**：从自然语言需求自动生成工业自动化控制逻辑的状态机和IEC 61499功能块代码，通过迭代精化提高开发效率。实验表明该方法显著减少了开发时间，同时保持高准确性。

- **输入**：
  - 自然语言描述的控制需求
  - 系统I/O接口规范（输入/输出信号列表）
  - 用户的迭代修改请求
- **方法**：Function Block Assistant (fbAssistant) - 基于LLM的迭代需求精化框架
- **输出**：
  - 可视化的有限状态机（FSM）
  - IEC 61499标准的功能块代码（含执行控制图ECC）
  - 可部署到EcoStruxure Automation Expert的控制逻辑

┌──────────────────────────────────────────────────────────────────────┐
│                              输入层                                   │
├──────────────────────────────────────────────────────────────────────┤
│ • 自然语言需求描述（NL requirements）                                 │
│ • 系统I/O接口规范（输入/输出信号列表）                                │
│ • 用户迭代修改请求（refinement requests）                             │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                      fbAssistant 迭代精化框架                         │
├──────────────────────────────────────────────────────────────────────┤
│  步骤1: LLM生成初始状态机                                             │
│         ↓                                                             │
│  步骤2: 可视化展示 → 用户验证                                         │
│         ↓                                                             │
│  步骤3: 迭代精化（用户反馈 → LLM修改）                                │
│         ↓                                                             │
│  步骤4: 内置解释器仿真验证                                            │
│         ↓                                                             │
│  步骤5: 生成IEC 61499功能块                                           │
│         ↓                                                             │
│  步骤6: 部署到EAE环境测试                                             │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                              输出层                                   │
├──────────────────────────────────────────────────────────────────────┤
│ • 可视化有限状态机（FSM图）                                           │
│ • IEC 61499功能块代码（含执行控制图ECC）                              │
│ • 可部署的控制逻辑（EcoStruxure Automation Expert格式）               │
└──────────────────────────────────────────────────────────────────────┘
```

**实验结果总结**：在气动缸和拾取放置机械手两个案例中，fbAssistant显著减少了开发时间，同时保持高准确性。工具能够处理多语言需求（包括中文），并成功实现了紧急停止等安全功能的迭代添加。

**研究动机**：工业自动化软件开发是资源密集型过程，传统方法需要大量经验和手动编程。现有方法从自然语言需求到可执行控制逻辑的转化效率低、易出错。状态机是工业控制的核心建模方法，但手动构建状态机耗时且容易遗漏关键迁移或状态。LLM在代码生成方面展现出潜力，但缺乏针对工业自动化领域的系统性方法，特别是缺少与IEC 61499标准的集成和闭环仿真验证能力。

**方法创新**：
1. **迭代精化机制**：支持用户通过自然语言逐步完善状态机，而非一次性生成
2. **闭环仿真集成**：内置解释器可直接连接EcoStruxure Automation Expert进行实时验证
3. **IEC 61499代码生成**：自动将状态机转换为符合工业标准的功能块代码
4. **多语言需求支持**：能够处理不同语言（包括中文）的需求描述

**实验设计**：
- **案例系统**：气动缸系统（简单案例）、拾取放置机械手（复杂案例）
- **开发环境**：EcoStruxure Automation Expert (EAE)
- **验证方法**：闭环仿真验证、虚拟调试、实际硬件部署测试
- **评估维度**：开发时间、生成准确性、迭代次数、最终功能正确性
- **使用模型**：基于LLM（论文未明确指定具体模型）

**结论与不足**：
- **主要结论**：AI辅助方法可行，显著提高开发效率，支持安全功能的迭代添加
- **优势**：减少开发时间、提高准确性、支持多语言、易于迭代修改
- **局限性**：
  1. 仍需少量手动调整状态迁移和UI交互
  2. 存在LLM"幻觉"问题（如创建无前驱状态、误删除动作）
  3. 需要更明确的提示命令来避免歧义
  4. 尚未集成形式化验证和自动化测试
  5. 对复杂系统的可扩展性未充分验证

## 研究问题与动机

### 问题背景

工业自动化软件开发是一个资源密集型过程，面临以下挑战：

1. **开发复杂度高**：需要创建精确的控制逻辑以确保可靠和安全的操作，传统方法需要丰富的经验和大量手动编程工作

2. **需求到实现的鸿沟**：自动化系统开发从自然语言需求开始，需要配合I/O分配表、管道仪表图(P&ID)等辅助文档，从非形式化需求到可执行代码的转化过程耗时且易出错

3. **状态机建模的重要性**：状态机是数字设计和工业自动化的基础概念，提供了结构化的方式来表示顺序逻辑和控制流，但手动构建状态机容易遗漏关键状态或迁移

4. **缺乏自动化工具**：虽然状态机编程的概念已被广泛倡导（作者团队在多篇文献[1]-[4]中提出），但缺少能够自动从自然语言生成状态机并支持迭代精化的实用工具

### 研究动机

论文的核心动机是利用大语言模型(LLM)的能力来自动化和加速工业自动化软件的开发过程：

1. **LLM的潜力**：LLM在自然语言处理、决策制定和自动推理方面展现出强大能力，但其在软件和系统工程中的应用仍处于发展阶段

2. **需求精化的挑战**：AI系统需要超越简单的模式匹配，融入类似人类认知过程的机制，如抽象、层次推理和错误纠正。人类的概念精化通过迭代调整发生，AI工具也应支持这种迭代过程

3. **形式化与AI的结合**：神经符号AI(neurosymbolic AI)结合统计学习和形式逻辑推理，fbAssistant通过将符号状态机表示与AI驱动的精化过程集成，弥合了人类意图与可执行逻辑之间的鸿沟

4. **验证与可解释性**：当前AI驱动的软件生成技术缺乏内在可解释性，工程师难以验证其正确性。检索增强生成(RAG)方法表明，将外部知识源与AI推理结合可以提高系统透明度

5. **工业标准的需求**：工业自动化需要符合IEC 61499等标准的代码，现有LLM工具缺少与这些标准的直接集成

### 现有方法的局限性

1. **传统开发方法**：完全依赖人工，开发周期长，容易出错，需要大量领域专家经验

2. **现有AI工具**：
   - 缺少针对工业自动化领域的专门化方法
   - 不支持迭代精化，通常是一次性生成
   - 缺少与工业开发环境的集成
   - 没有闭环仿真验证能力
   - 不支持IEC 61499等工业标准的代码生成

3. **验证挑战**：传统软件验证技术涉及形式化方法和模型检查，但将这些方法扩展到AI生成的代码仍是一个基本挑战

## 核心方法

### 方法概述：Function Block Assistant (fbAssistant)

fbAssistant是由Flexbridge AB开发的概念验证工具，采用基于LLM的迭代方法来开发自动化逻辑。整体工作流程包含8个步骤：

1. **创建闭环仿真环境**：在IDE中创建包含空控制器功能块的闭环仿真环境，连接到实现过程仿真模型的功能块和实现交互式HMI元素（按钮、指示器）的功能块

2. **准备自然语言需求**：用户准备并输入自然语言描述的控制需求

3. **LLM生成状态机**：LLM处理需求并创建对应的状态机表示，可视化展示供用户检查

4. **迭代精化**：通过多个迭代步骤精化状态机，用户可以用自然语言提交修改请求

5. **仿真验证**：使用内置解释器在闭环环境中验证逻辑正确性，解释器连接到IDE中运行的仿真模型

6. **生成功能块**：生成等效的IEC 61499功能块并"植入"到IDE项目中

7. **部署测试**：将更新的闭环环境部署到softPLC运行时，使用自动生成的控制器FB进行测试

8. **实际部署**：部署到真实PLC

### 关键技术特点

#### 1. 迭代精化机制

**初始化阶段**：
- 从空状态机模块开始
- 应用初始提示描述系统接口，形成模块接口
- 将所有输出初始化为FALSE

**精化过程**：
- 用户通过自然语言逐步添加功能和约束
- LLM理解用户意图并修改状态机
- 支持增量式开发，每次迭代添加新的状态、迁移或动作

**示例**（气动缸案例）：
- 第1步：定义I/O接口（home, end, Start, Stop, Auto, Clear输入；fwd, bkwd, LED输出）
- 第2步：添加基本行为（初始化、移动到home位置、等待Start按钮）
- 第3步：添加前进和后退逻辑
- 第4步：添加紧急停止功能（Stop和Clear按钮）

#### 2. 闭环仿真集成

**架构设计**：
- 采用Cyber-Physical Components架构[15]
- 基于面向对象的Model-View-Controller模式适配到基于组件的自动化
- 功能块应用遵循IEC 61499标准

**仿真环境**：
- 在EcoStruxure Automation Expert (EAE)中并行运行fbAssistant
- 闭环环境包含：HMI功能块 ↔ 控制器功能块 ↔ 过程模型功能块
- 内置解释器直接连接到仿真模型，实现实时验证

**验证流程**：
- 用户可以在状态机生成后立即运行
- 通过HMI交互（按按钮）观察系统行为
- 在虚拟环境中验证预期行为后再部署到实际硬件

#### 3. IEC 61499代码生成

**转换过程**：
- 将验证后的状态机自动转换为IEC 61499功能块
- 生成执行控制图(Execution Control Chart, ECC)
- 保持状态机的语义和行为

**集成方式**：
- 生成的功能块可以直接在EAE等工业自动化工具中打开
- 通过更改控制器的功能块类型，无缝集成到闭环环境中
- 支持部署到虚拟或物理环境进行测试

#### 4. 自然语言理解

**接口定义**：
- 支持基于I/O列表的接口规范
- 理解输入/输出信号的语义（传感器、执行器、按钮、指示灯）

**行为描述**：
- 理解顺序逻辑（"当...时"、"然后"、"等待"）
- 理解状态和迁移条件
- 支持安全约束（紧急停止、互锁）

**多语言支持**：
- 实验证明可以处理不同语言的需求（包括中文）
- 在中文需求下获得与英文相同的结果

### 技术实现细节

#### 状态机表示

状态机包含以下元素：
- **状态(States)**：如INIT, TOLEFT, ATLEFT, GO, GOBACK, ATRIGHT
- **迁移(Transitions)**：带条件的状态间转换
- **动作(Actions)**：状态内执行的操作（设置输出信号）
- **守卫条件(Guards)**：迁移的触发条件（传感器读数、按钮按下）

#### 提示工程策略

**结构化提示**：
1. 系统接口定义（I/O列表）
2. 期望行为描述
3. 状态结构约束（必须包含的状态）
4. 迁移条件规范
5. 安全约束和互锁

**迭代修改提示**：
- 明确指出需要修改的部分
- 描述期望的新行为
- 指定约束条件（如"确保在运动结束时重置控制信号"）

#### 检索增强生成(RAG)

论文提到fbAssistant的方法与RAG研究一致：
- 将预训练模型与外部知识源结合
- 集成工业控制系统的结构化知识
- 通过AI推理产生可验证和安全的自动化逻辑
- 提高AI生成输出的可靠性

## 实验与评估

### 案例一：气动缸系统

#### 系统描述

**物理组成**：
- 双作用气动缸
- 2个位置传感器（home和end）
- 2个执行信号（fwd前进和bkwd后退）

**I/O接口**（共12个信号）：
- **输入**：home(BOOL), end(BOOL), Start(BOOL), Stop(BOOL), Auto(BOOL), Clear(BOOL), Init(BOOL)
- **输出**：fwd(BOOL), bkwd(BOOL), startled(BOOL), stopled(BOOL), autoled(BOOL), clearled(BOOL)

#### 开发过程

**第1步：接口定义**
- 提示：添加I/O信号到模块接口，移除虚拟信号，添加Init输入用于初始化
- 结果：形成完整接口，所有输出初始化为FALSE

**第2步：基本行为**
- 需求：系统启动时初始化，如果不在home位置则自动后退到home，等待Start按钮，按Start前进到end，再按Start返回home
- 要求状态：START, INIT, TOLEFT, ATLEFT, ATRIGHT, GO, GOBACK
- 结果：LLM成功生成包含所有要求状态和正确迁移的状态机

**第3步：HMI逻辑**
- 添加START按钮逻辑
- 添加按钮背后的指示灯及其行为

**第4步：安全功能**
- 添加紧急停止按钮(Stop)功能
- 添加清除/复位按钮(Clear)功能
- 提示分为三部分描述Stop和Clear的行为
- 结果：第一次运行即成功实现

#### 验证结果

- 状态机在仿真环境中验证正确
- 生成的IEC 61499功能块成功部署到EAE
- 确保平滑可靠的气缸操作，状态迁移正确，安全处理改进

### 案例二：拾取放置机械手

#### 系统描述

**物理组成**：
- 处理4个位置：3个输入托盘 + 1个输出托盘
- 多个气缸：水平气缸（多个，用于到达不同托盘）、垂直气缸（用于抓取/放置）
- 真空吸盘系统（带吸力传感器）

**功能目标**：
- 从输入托盘转移工件到输出托盘
- 输入托盘每次可容纳一个工件
- 输出托盘自动处理放置的工件

#### 开发过程

**初始需求**：
```
初始位置：所有气缸收回
期望行为：
1. 如果输入托盘有工件可用
2. 伸出所需数量的水平气缸到达托盘
3. 伸出垂直气缸
4. 打开真空
5. 等待吸力传感器确认工件被吸住
6. 提升垂直气缸
7. 收回水平气缸
8. 移动到输出托盘
9. 如果输出托盘为空，伸出垂直气缸
10. 放下工件
11. 返回初始位置
```

**迭代精化**：
- AI生成初始逻辑
- 基于仿真反馈迭代精化
- 确保状态间迁移（如抓取和释放）按正确顺序执行
- 防止不期望的同时运动

**改进内容**：
- 防止机械手过早放下物体
- 确保安全返回home位置
- 优化运动序列以减少循环时间

#### 验证结果

- 精化后的状态机在仿真中验证通过
- 转换为功能块并部署到EAE
- 实际测试确认AI生成的控制逻辑满足预期功能需求

### 主要实验结果

#### 定性结果

1. **开发效率**：
   - 显著减少开发时间
   - 保持高准确性
   - 初始实验证明了AI驱动方法的可行性

2. **迭代精化效果**：
   - 帮助开发者更好理解自然语言表述的意图
   - LLM能够敏锐处理误解或不精确之处
   - 避免可能导致歧义的问题

3. **多语言能力**：
   - 在处理自然语言需求方面表现稳定
   - 支持不同语言（实验用中文重复气动缸案例，获得相同结果）

#### 发现的问题

1. **需要手动调整**：
   - 需要少量手动调整来微调状态迁移和UI交互

2. **LLM幻觉**：
   - 创建没有前驱状态的状态
   - 在请求删除单个动作时清空状态的所有动作
   - 证明需要更明确的提示命令

3. **提示工程重要性**：
   - 需要精心设计提示以避免歧义
   - 明确的约束和要求能提高生成质量

### 评估维度

虽然论文未提供定量指标，但从案例分析可以看出评估关注：

1. **功能正确性**：生成的状态机是否实现了需求的功能
2. **安全性**：是否正确处理紧急停止等安全功能
3. **完整性**：是否包含所有必要的状态和迁移
4. **可部署性**：生成的代码是否能成功部署到实际系统
5. **迭代效率**：需要多少次迭代才能达到满意结果

## 与本研究的关系

### 相关性分析

本论文与博士研究的"基于控制系统软件需求的LLM状态机结构化建模方法"高度相关，具体体现在：

1. **研究目标一致**：
   - 都关注从自然语言需求生成状态机
   - 都针对控制系统领域
   - 都强调形式化模型的生成

2. **方法路径相似**：
   - 采用LLM作为核心技术
   - 支持迭代精化过程
   - 关注可执行代码的生成

3. **应用场景重叠**：
   - 工业自动化控制系统
   - 安全关键系统
   - 需要形式化验证的场景

### 可借鉴之处

#### 1. 迭代精化机制设计

**优点**：
- 不要求一次性生成完美结果
- 允许用户逐步添加功能和约束
- 符合实际工程实践中的增量开发模式

**可借鉴**：
- 在本研究中也应采用迭代方法，而非追求一次性生成
- 设计清晰的迭代流程和用户交互界面
- 每次迭代后提供可视化反馈

#### 2. 闭环仿真验证

**优点**：
- 在生成代码前就能验证状态机行为
- 降低部署到实际系统的风险
- 提供即时反馈，加速迭代

**可借鉴**：
- 本研究应考虑集成仿真验证环节
- 可以使用UPPAAL等工具进行形式化验证
- 在验证失败时提供反馈用于模型修复

#### 3. 工业标准代码生成

**优点**：
- 生成符合IEC 61499标准的代码
- 可直接部署到工业环境
- 与现有工具链无缝集成

**可借鉴**：
- 本研究应考虑目标代码格式的标准化
- 可以支持多种目标格式（如UPPAAL XML、IEC 61499、Stateflow等）
- 确保生成的模型可以被工业工具直接使用

#### 4. 提示工程策略

**优点**：
- 结构化的提示设计（接口定义 + 行为描述 + 约束）
- 支持增量式需求输入
- 明确的状态和迁移规范

**可借鉴**：
- 设计分层的提示模板
- 将需求分解为接口、行为、约束等不同方面
- 提供提示示例和最佳实践指南

### 存在的不足与改进空间

#### 1. 缺少形式化验证

**不足**：
- 仅依赖仿真验证，未进行形式化验证
- 无法保证安全性质和活性性质
- 对于安全关键系统可能不够充分

**改进方向**（本研究的机会）：
- 集成模型检查工具（如UPPAAL）
- 自动生成验证性质（研究内容二）
- 提供形式化验证报告

#### 2. 缺少时间约束支持

**不足**：
- 论文未提及时间自动机或时间约束
- 对于实时系统可能不够

**改进方向**：
- 本研究应支持时间约束的建模
- 生成时间自动机而非普通状态机
- 验证时序性质

#### 3. 缺少自动化测试

**不足**：
- 主要依赖人工验证
- 未提供自动化测试用例生成

**改进方向**：
- 从需求自动生成测试场景（研究内容二）
- 提供测试覆盖率分析
- 支持回归测试

#### 4. 缺少缺陷修复机制

**不足**：
- 当生成的状态机有问题时，需要人工重新描述需求
- 未提供基于验证反馈的自动修复

**改进方向**（本研究的核心）：
- 实现基于验证反馈的迭代修复（研究内容四）
- 分析验证反例，定位缺陷
- 自动生成修复建议

#### 5. 可扩展性未充分验证

**不足**：
- 仅在两个相对简单的案例上验证
- 未测试大规模复杂系统
- 未提供定量性能数据

**改进方向**：
- 在更大规模数据集上评估（如本研究的101条需求）
- 提供定量指标（准确率、完整性、修复成功率等）
- 测试不同复杂度的系统

#### 6. LLM幻觉问题

**不足**：
- 承认存在幻觉问题（无前驱状态、误删除动作）
- 未提供系统性的解决方案

**改进方向**：
- 设计约束检查机制，拒绝不合法的状态机
- 使用形式化验证检测结构性错误
- 提供修复建议而非直接接受错误输出

### 对本研究的启发

1. **研究定位**：
   - 本研究可以定位为fbAssistant的增强版本
   - 重点解决其未解决的形式化验证和自动修复问题
   - 提供更完整的"生成-验证-修复"闭环

2. **技术路线**：
   - 采用类似的迭代精化框架
   - 增加形式化验证环节
   - 增加基于验证反馈的自动修复

3. **评估策略**：
   - 使用更大规模的数据集
   - 提供定量评估指标
   - 与fbAssistant等工具进行对比

4. **创新点**：
   - 时间约束的支持（时间自动机）
   - 形式化验证的集成
   - 验证场景和性质的自动生成
   - 基于验证反馈的迭代修复
   - 更系统的缺陷分类和修复策略

## 重要的相关工作

### 1. 重要的前身类工作

#### 1.1 Naumov & Shalyto (2003) - 多智能体系统的自动机理论实现

- **标题**：Automata theory for multi-agent systems implementation
- **作者**：L. Naumov, A. Shalyto
- **会议**：IEMC'03 Managing Technologically Driven Organizations
- **主要内容**：提出使用自动机理论实现多智能体系统的方法，为基于自动机的编程奠定理论基础
- **论文中的引用**：
  - 第42行："The concept of direct state-machine programming...has been advocated by the authors in many previous publications, including [1]–[4]"
- **与本论文的关系**：这是作者团队的前期工作，为状态机编程的理念提供了理论基础。本论文继承了这一理念，并通过LLM实现了自动化
- **佐证内容**：为本研究的状态机编程方法提供了理论基础和长期研究脉络

#### 1.2 Yartsev et al. (2005) - 反应式多智能体控制系统的自动机编程

- **标题**：Automata-based programming of the reactive multi-agent control systems
- **作者**：B. Yartsev, G. Korneev, A. Shalyto, V. Kotov
- **会议**：International Conference on Integration of Knowledge Intensive Multi-Agent Systems, 2005
- **主要内容**：将自动机编程应用于反应式多智能体控制系统
- **论文中的引用**：第42行引用为前期工作之一
- **与本论文的关系**：作者团队的前期工作，展示了自动机方法在控制系统中的应用
- **佐证内容**：证明了状态机方法在控制系统中的有效性

#### 1.3 Shalyto et al. (2005) - 基于有限自动机的面向对象反应式智能体实现

- **标题**：Methods of object-oriented reactive agents implementation on the basis of finite automata
- **作者**：A. Shalyto, L. Naumov, G. Korneev
- **会议**：International Conference on Integration of Knowledge Intensive Multi-Agent Systems, 2005
- **主要内容**：提出基于有限自动机实现面向对象反应式智能体的方法
- **论文中的引用**：第42行引用为前期工作之一
- **与本论文的关系**：作者团队的前期工作，将自动机方法与面向对象编程结合
- **佐证内容**：为本研究的方法提供了面向对象的设计思路

#### 1.4 Vyatkin et al. (1996) - Chartware结构化可视化编程方法

- **标题**：Chartware - an approach to structured visual programming for industrial logic control
- **作者**：V. Vyatkin, G. Ivanov, V. Fedorenko, V. Osheter
- **期刊**：Controllers and Control Systems, vol. 3, no. 4, pp. 33–44
- **主要内容**：提出Chartware方法，用于工业逻辑控制的结构化可视化编程
- **论文中的引用**：第42行引用为前期工作之一
- **与本论文的关系**：作者团队的早期工作（1996年），展示了对可视化状态机编程的长期关注。本论文可以看作是这一理念在AI时代的延续
- **佐证内容**：证明了作者团队在状态机可视化编程领域有近30年的研究积累

### 2. 在技术上提供了支持的工作

#### 2.1 Lewis et al. (2020) - 检索增强生成(RAG)

- **标题**：Retrieval-augmented generation for knowledge-intensive nlp tasks
- **作者**：P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. tau Yih, T. Rocktäschel, S. Riedel, D. Kiela
- **会议**：NeurIPS 2020, vol. 33, pp. 9459–9474
- **链接**：https://arxiv.org/abs/2005.11401
- **主要内容**：提出检索增强生成方法，将预训练模型与外部知识源结合，提高知识密集型NLP任务的性能
- **论文中的引用**：
  - 第68-73行："Research on retrieval-augmented generation (RAG) methods has shown that combining pre-trained models with external knowledge sources enhances the reliability of AI-generated output. This aligns with the Function Block Assistant's approach, where structured knowledge from industrial control systems is integrated with AI reasoning to produce verifiable and safe automation logic"
  - 第127-130行："Recent research on retrieval-augmented generation suggests that combining external knowledge sources with AI reasoning improves system transparency, which is crucial for AI-assisted software engineering"
- **与本论文的关系**：RAG方法为fbAssistant提供了技术基础，通过将工业控制系统的结构化知识与AI推理结合，提高生成输出的可靠性和透明度
- **技术使用**：fbAssistant采用了RAG的核心思想，将IEC 61499标准、控制系统知识等外部知识与LLM结合

#### 2.2 Zhabelova et al. (2014) - Cyber-Physical Components架构

- **标题**：Cyber-physical components for heterogeneous modelling, validation and implementation of smart grid intelligence
- **作者**：G. Zhabelova, C.-W. Yang, S. Patil, C. Pang, J. Yan, A. Shalyto, V. Vyatkin
- **会议**：2014 12th IEEE International Conference on Industrial Informatics (INDIN)
- **主要内容**：提出Cyber-Physical Components架构，将面向对象的Model-View-Controller模式适配到基于组件的自动化
- **论文中的引用**：
  - 第186-188行："The function block application follows the Cyber-Physical Components architecture [15] - the adaptation of object-oriented Model-View-Controller pattern for component-based automation"
- **与本论文的关系**：fbAssistant的功能块应用直接采用了这一架构
- **技术使用**：直接采用作为系统架构设计基础

#### 2.3 Schneider Electric - EcoStruxure Automation Expert (EAE)

- **链接**：https://www.se.com/us/en/product-range/23643079-ecostruxure-automation-expert/
- **主要内容**：施耐德电气的工业自动化开发环境，支持IEC 61499标准
- **论文中的引用**：
  - 第182-184行："it is recommended that fbAssistant is run in parallel with the IEC 61499 development environment, such as EcoStruxure Automation Expert (EAE)"
  - 多处提到部署到EAE环境
- **与本论文的关系**：作为fbAssistant的集成开发环境和部署平台
- **技术使用**：直接使用作为开发和部署工具

### 3. 提供了重要论证的工作

#### 3.1 Caruana et al. (2015) - 可解释AI模型

- **标题**：Intelligible models for healthcare: Predicting pneumonia risk and hospital 30-day readmission
- **作者**：R. Caruana, Y. Lou, J. Gehrke, P. Koch, M. Sturm, N. Elhadad
- **会议**：21st ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2015
- **链接**：https://people.dbmi.columbia.edu/noemie/papers/15kdd.pdf
- **主要内容**：提出可解释的AI模型用于医疗预测，强调AI系统需要可解释性
- **论文中的引用**：
  - 第96-98行："One of the main challenges in AI is the development of generalisable reasoning systems that can model complex hierarchical decision-making processes"
- **与本论文的关系**：论证了AI系统需要可解释性和层次推理能力，这是fbAssistant设计的动机之一
- **佐证内容**：论证了AI在工程应用中需要可解释性，支持fbAssistant采用可视化状态机的设计选择

#### 3.2 Guan et al. (2023) - LLM的世界模型构建

- **标题**：Leveraging pre-trained large language models to construct and utilize world models for model-based task planning
- **作者**：L. Guan, K. Valmeekam, S. Sreedharan, S. Kambhampati
- **会议**：33rd International Conference on Automated Planning and Scheduling (ICAPS), 2023
- **链接**：https://arxiv.org/abs/2305.14909
- **主要内容**：研究如何利用预训练LLM构建和使用世界模型进行基于模型的任务规划
- **论文中的引用**：
  - 第102-104行："neurosymbolic AI, which combines statistical learning with formal logical reasoning. The Function Block Assistant aligns with this trend by integrating symbolic state machine representations with AI-driven refinement processes"
- **与本论文的关系**：论证了神经符号AI的重要性，支持fbAssistant将符号状态机与AI结合的方法
- **佐证内容**：论证了LLM可以用于构建结构化模型，为fbAssistant的技术路线提供理论支持

#### 3.3 Hu et al. (2024) - LLM的自我改进学习

- **标题**：Teaching language models to self-improve by learning from language feedback
- **作者**：C. Hu, Y. Hu, H. Cao, T. Xiao, J. Zhu
- **会议**：Findings of ACL 2024
- **链接**：https://aclanthology.org/2024.findings-acl.364/
- **主要内容**：研究如何让语言模型通过语言反馈进行自我改进
- **论文中的引用**：
  - 第110-119行："AI models need to go beyond simple pattern matching and incorporate mechanisms reminiscent of human cognitive processes, such as abstraction, hierarchical reasoning, and error correction. The study of human cognition suggests that conceptual refinement occurs through iterative adjustments, where humans learn by interacting with an environment and refining mental models. Similarly, the Function Block Assistant iteratively refines its generated control logic based on user feedback"
- **与本论文的关系**：论证了迭代精化和错误纠正的重要性，支持fbAssistant的迭代设计
- **佐证内容**：论证了AI系统需要类似人类的迭代学习能力，为fbAssistant的迭代精化机制提供认知科学基础

#### 3.4 Backes et al. (2018) - AI生成代码的验证挑战

- **标题**：Semantic-based automated reasoning for aws access policies using smt
- **作者**：J. Backes, P. Bolignano, B. Cook, C. Dodge, A. Gacek, K. Luckow, N. Rungta, O. Tkachuk, C. Varming
- **会议**：Formal Methods in Computer-Aided Design (FMCAD), 2018
- **主要内容**：使用SMT进行AWS访问策略的语义自动推理
- **论文中的引用**：
  - 第123-124行："Current AI-driven software generation techniques often rely on neural networks that lack intrinsic explainability, making it difficult for engineers to verify their correctness"
  - 第132-138行："Furthermore, AI-driven automation introduces new challenges related to verification and validation. Traditional software verification techniques involve formal methods and model checking, but scaling these approaches to AI-generated code remains a fundamental challenge"
- **与本论文的关系**：论证了AI生成代码的验证挑战，说明fbAssistant需要集成验证能力
- **佐证内容**：论证了形式化验证对AI生成代码的重要性，为未来工作方向提供支持

### 4. 其他重要工作

#### 4.1 Hadsell et al. (2006) - 降维学习

- **标题**：Dimensionality reduction by learning an invariant mapping
- **作者**：R. Hadsell, S. Chopra, Y. LeCun
- **会议**：IEEE CVPR 2006, vol. 2, pp. 1735–1742
- **主要内容**：通过学习不变映射进行降维
- **论文中的引用**：第114-116行引用，讨论人类通过与环境交互精化心智模型
- **与本论文的关系**：提供认知科学背景，支持迭代学习的理念
- **作用**：提供理论背景知识

#### 4.2 Xavier et al. (2024) - LLM驱动的IEC 61499系统分析

- **标题**：LLM-powered multi-actor system for intelligent analysis and visualization of iec 61499 control systems
- **作者**：M. Xavier, T. Laikh, S. Patil, V. Vyatkin
- **会议**：IECON 2024-50th Annual Conference of the IEEE Industrial Electronics Society
- **主要内容**：使用LLM驱动的多智能体系统进行IEC 61499控制系统的智能分析和可视化
- **论文中的引用**：
  - 第150-158行："Recent work on integrating large language models (LLMs) into industrial automation has demonstrated their ability to improve intelligent analysis and visualisation of IEC 61499 control systems. Using AI-powered reasoning, these approaches improve system transparency and facilitate more efficient debugging and optimisation of automation workflows"
- **与本论文的关系**：展示了LLM在IEC 61499领域的其他应用，证明LLM与工业自动化标准结合的可行性
- **作用**：提供LLM在工业自动化领域应用的背景知识

#### 4.3 Ovsiannikova et al. (2024) - 生成式AI协同快速原型开发

- **标题**：Generative ai co-pilot for rapid prototyping of iec 61499 control applications
- **作者**：P. Ovsiannikova, T. Liakh, P. Jhunjhunwala, V. Vyatkin
- **会议**：2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)
- **主要内容**：使用生成式AI作为协同工具快速原型开发IEC 61499控制应用
- **论文中的引用**：
  - 第159-165行："Generative AI has also been explored as a co-pilot for rapid prototyping of IEC 61499 control applications, significantly reducing development time and increasing automation efficiency. These advancements align with the Function Block Assistant's goal of bridging the gap between human intent and executable control logic by automating function block generation and refinement"
- **与本论文的关系**：展示了生成式AI在IEC 61499快速原型开发中的应用，与fbAssistant目标一致
- **作用**：提供相关应用背景，证明AI辅助IEC 61499开发的趋势

### 5. 未来工作中计划使用的工作

#### 5.1 King & Vyatkin (2025) - 基于STPA的LLM迭代精化

- **标题**：LLM-based iterative refinement of finite-state machines with STPA controller constraints and generation of IEC 61499 code
- **作者**：A. King, V. Vyatkin
- **会议**：2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA)
- **主要内容**：使用STPA(系统理论过程分析)控制器约束进行LLM驱动的有限状态机迭代精化
- **论文中的引用**：
  - 第417-420行："Future work plans...One direction of work will focus on improving AI understanding of ambiguous requirements and integrating additional safety constraints as reported in the paper [16]"
- **与本论文的关系**：计划在未来工作中集成安全约束
- **作用**：指明未来研究方向

#### 5.2 Lilli et al. (2023) - IEC 61499控制软件的形式化验证

- **标题**：Formal verification of the control software of a radioactive material remotehandling system based on IEC 61499
- **作者**：G. Lilli, M. Xavier, E. Le Priol, V. Perret, T. Liakh, R. Oboe, V. Vyatkin
- **期刊**：IEEE Open Journal of Industrial Electronics Society, 2023
- **主要内容**：基于IEC 61499的放射性材料远程处理系统控制软件的形式化验证
- **论文中的引用**：
  - 第419-422行："The available formal verification framework described in [17] is planned to be used for formal verification of the autogenerated function blocks"
- **与本论文的关系**：计划在未来工作中使用该框架进行形式化验证
- **作用**：指明未来研究方向，提供验证工具

#### 5.3 Vyatkin & Rumiantcev (2024) - 快于实时的IEC 61499测试框架

- **标题**：Framework for faster-than-real-time testing of IEC 61499 applications with embedded process simulation
- **作者**：V. Vyatkin, R. Rumiantcev
- **会议**：2024 IEEE 22nd International Conference on Industrial Informatics (INDIN)
- **主要内容**：用于IEC 61499应用的快于实时测试框架，嵌入过程仿真
- **论文中的引用**：
  - 第422-423行："while the automated testing from [18] can be used for their extensive testing"
- **与本论文的关系**：计划在未来工作中使用该框架进行自动化测试
- **作用**：指明未来研究方向，提供测试工具

## 文献分类总结

本论文共引用18篇文献，按作用分类如下：

1. **前身类工作（4篇）**：作者团队在状态机编程和可视化建模领域的长期研究积累（1996-2005），为本工作提供了理论基础和研究脉络

2. **技术支持（3篇）**：RAG方法、Cyber-Physical Components架构、EcoStruxure Automation Expert工具，直接用于fbAssistant的实现

3. **论证支持（4篇）**：可解释AI、神经符号AI、迭代学习、验证挑战等研究，论证了fbAssistant设计选择的合理性和必要性

4. **其他支持（4篇）**：认知科学背景、LLM在工业自动化中的其他应用，提供背景知识和相关工作对比

5. **未来工作（3篇）**：安全约束集成、形式化验证框架、自动化测试框架，指明未来研究方向

本论文的核心创新在于：
- 将LLM与工业自动化标准(IEC 61499)深度集成
- 提供完整的迭代精化工作流（需求→状态机→仿真→代码→部署）
- 支持闭环仿真验证和多语言需求处理

实验结果表明，fbAssistant显著减少了开发时间，同时保持高准确性，证明了AI辅助工业自动化软件开发的可行性。未来工作将重点集成安全约束、形式化验证和自动化测试能力。
