# 面向工业4.0状态机的代码与测试生成——基于LLM的图样识别技术 / Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition

## 基本信息

- **标题**：Code and Test Generation for I4.0 State Machines with LLM-based Diagram Recognition
- **中文标题**：面向工业4.0状态机的代码与测试生成——基于LLM的图样识别技术
- **作者**：Björn Otto, Assanali Aidarkhan, Marko Ristin, Nico Braunisch, Christian Diedrich, Hans Wernher van de Venn, Martin Wollschlaeger
- **单位**：
  - Otto von Guericke University (Institute for Automation and Communication)
  - Nazarbayev University (Department of Computer Science)
  - Zurich University of Applied Sciences (Institute of Mechatronic Systems)
  - TU Dresden (Institute of Applied Computer Science)
- **发表**：2025 IEEE 21st International Conference on Factory Communication Systems (WFCS), 2025年6月
- **DOI**：10.1109/WFCS63373.2025.11077624
- **链接**：https://ieeexplore.ieee.org/abstract/document/11077624

**代码/仓库获取方式**：
- 论文实现已公开发布在Zenodo平台
- 获取链接：https://zenodo.org/records/14730727
- 包含完整的实现代码和实验数据

**数据集获取方式**：
- 数据集来源于两个工业通信协议标准的PDF规范文档：
  - IEC 61158 (PROFINET)：从1183页的PDF文档中手工裁剪了80个状态图
  - IEC 62541 (OPC UA)：从24个部分共1830页的PDF文档中手工裁剪了15个状态图
- 由于版权原因，论文对图样进行了文本打乱处理（scrambling）后才公开
- 原始规范文档需要从IEC官方购买获取

## 简报

**解决的问题**：从工业4.0规范文档中嵌入的状态图图像自动生成代码和单元测试，减少手工实现工作量。实验结果表明，在PROFINET数据集上LLM能正确识别63%的边，在OPC UA数据集上能正确识别45%的边，自动生成了数千行C++代码和测试用例。

- **输入**：
  - 工业规范PDF文档（如IEC 61158、IEC 62541）
  - 从PDF中裁剪的状态图图像
  - 提示工程设计的识别指令

- **方法**：三步流水线
  - 步骤1：从PDF文档中裁剪状态图图像（手工）
  - 步骤2：使用LLM识别状态图并输出机器可读格式（零样本或少样本）
  - 步骤3：基于识别结果模板化生成C++代码和单元测试

- **输出**：
  - 机器可读的状态机表示（节点和边的列表）
  - C++代码桩（状态枚举、状态处理函数、主循环）
  - 单元测试用例（基于边覆盖准则）

```
┌─────────────────────────────────────────────────────────────────┐
│                           输入层                                 │
├─────────────────────────────────────────────────────────────────┤
│ • 工业规范PDF文档（PROFINET/OPC UA）                             │
│ • 裁剪的状态图图像（80+15个）                                     │
│ • 提示工程指令（零样本/少样本）                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         三步流水线                                │
├─────────────────────────────────────────────────────────────────┤
│  裁剪 → LLM识别 → 模板生成                                        │
│         ↓                                                        │
│  [零样本/少样本学习]                                              │
│  [提示工程优化]                                                   │
│  [机器可读格式输出]                                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          输出层                                  │
├─────────────────────────────────────────────────────────────────┤
│ • 状态机表示（节点和边列表）                                      │
│ • C++代码桩（7017+1614行）                                       │
│ • 单元测试用例（3934+1034行）                                    │
└─────────────────────────────────────────────────────────────────┘
```

实验结果：在PROFINET数据集上，gpt-4o识别准确率达63%（411/657条边），在OPC UA数据集上达45%（57/127条边）。自动生成了PROFINET的7017行代码和3934行测试，OPC UA的1614行代码和1034行测试，生成过程不到1秒。

**研究动机**：工业4.0要求高度互操作性，制造商需要正确实现复杂的通信协议规范。这些规范通常以PDF形式提供，其中状态图以图像形式嵌入。开发者需要手工将状态图转换为代码，这既耗时又容易出错，且难以验证实现的正确性。传统计算机视觉方法需要针对每种图样风格进行标注和训练，泛化能力差且设置复杂。

**方法创新**：
1. 使用LLM进行状态图识别，相比传统计算机视觉方法具有更好的泛化能力和更简单的设置
2. 采用三步流水线（裁剪-识别-生成）而非端到端生成，提高了可审查性和可靠性
3. 通过提示工程优化LLM输出格式，支持零样本和少样本识别
4. 基于识别结果的模板化代码和测试生成，确保高代码覆盖率

**实验设计**：
- 对比对象：gpt-4o、claude-3-sonnet、Llama-3.2-11b（LLM对比）；传统计算机视觉工具（方法对比）；直接端到端生成（消融实验）
- 数据集：IEC 61158 (PROFINET) 80个状态图，IEC 62541 (OPC UA) 15个状态图
- 评估指标：准确率（正确识别的边占真实边的比例）、缺失边数量、幻觉边数量、生成代码行数
- 使用模型：主要使用gpt-4o-2024-08-06，对比claude-3-sonnet-20240229和Llama-3.2-11b-vision-preview
- 实验设置：零样本、一样本、二样本、三样本识别，每个实验重复3次

**结论与不足**：
- 优势：LLM在状态图识别上表现优于传统计算机视觉方法，泛化能力强，设置简单，能显著减少手工工作量（识别63%和45%的边）
- 局限性：
  1. 裁剪步骤仍需手工完成，自动裁剪方法精度不足
  2. LLM会遗漏边（37%）或产生幻觉边（14%），需要人工审查修正
  3. 少样本学习可能"压倒"模型，提供过多样本反而效果变差
  4. 对于复杂图样（如OPC UA的边标签、多重边）识别率下降
  5. 直接端到端生成代码质量不佳，难以发现的细微错误，无法满足覆盖准则

## 研究问题与动机

### 问题背景

工业4.0标志着制造业和工业自动化的数字化转型，要求高度可定制的价值链和跨制造商的无缝数据交换。实现这种互操作性的关键是制造商必须正确实现共同的通信协议标准。然而，这些标准规范通常非常庞大和复杂，导致实现过程耗费大量时间和精力。

在通信协议领域，状态机是描述系统行为的有效抽象方式。许多规范文档中包含状态机的渲染图像（状态图）。例如，IEC 61158标准（PROFINET协议）包含1183页，其中嵌入了80个状态图；IEC 62541标准（OPC UA协议）包含1830页，其中嵌入了15个状态图。

### 核心挑战

1. **手工转换的低效性**：开发者需要花费大量时间将状态图手工转换为代码。如果状态图以形式化、机器可读的形式提供，转换过程会很简单。但实际上，规范文档通常以专有的PDF格式购买，状态图以图像形式嵌入，无法直接提取。

2. **验证的困难性**：手工实现的代码难以验证正确性。审查者需要具备足够的编程能力才能阅读和理解代码，将其与规范中的状态图进行对比。

3. **传统计算机视觉方法的局限性**：
   - **复杂性**：需要组合多个专门的模型（OCR识别文本、线检测器识别边、目标检测器识别形状和箭头等），每个模型需要独立训练和评估，使用不同的技术和指标，将结果组合成完整图样仍然是重大挑战。
   - **泛化能力差**：模型只能识别训练时见过的元素，但训练集规模有限且针对特定应用。对于新的图样风格，需要重新标注数据、重新训练模型、调整超参数，这对最终用户来说不切实际。

### 研究动机

本研究的核心动机是利用大语言模型（LLM）的泛化能力和简单设置来解决上述问题。LLM作为基础模型，在海量数据上训练，能够处理多种模态（文本和图像），具有强大的迁移学习能力。相比传统计算机视觉方法，LLM只需要通过提示工程（prompt engineering）调整输入问题的文本描述，就能适应新的图样风格，无需重新标注数据和训练模型。

此外，通过将识别和生成分为两步（而非端到端生成），可以提高可审查性：审查识别出的边列表比审查生成的代码更容易，不需要编程专业知识，低技能操作员也能完成。

## 核心方法

### 方法概述

本研究提出了一个三步流水线方法，用于从PDF规范文档中的状态图图像自动生成代码和单元测试：

1. **裁剪（Cropping）**：从PDF文档中裁剪状态图图像
2. **识别（Recognition）**：使用LLM识别状态图并输出机器可读格式
3. **生成（Generation）**：基于识别结果模板化生成代码和测试

### 关键技术

#### 1. 提示工程（Prompt Engineering）

提示工程是引导LLM生成高质量输出的关键。研究采用迭代优化的方式设计提示：

**初始尝试（Try 1）**：
```
Infer the nodes and edges of the given graph.
```
结果：LLM返回空列表，因为缺少输出格式指导。

**第二次尝试（Try 2）**：
```
Infer the nodes and edges of the given graph. The output should contain no text, but only edges in the form 'node1 -> node2'
```
结果：LLM成功生成边列表，但包含不期望的字符（如破折号）。

**第三次尝试（Try 3）**：
```
Infer the nodes and edges of the given graph. The output should contain no text, but only edges in the form 'node1 -> node2'. For example:
node1 -> node2
node3 -> node4
```
结果：质量显著提升，但有些边使用了"to"而非"->"。

**最终版本（Final）**：
```
Infer the nodes and edges of the given graph. The output should contain no text, but only edges in the form 'node1 -> node2'. For example:
node1 -> node2
node1 -> node1
Only use directed arrows: ->
```
结果：LLM正确识别节点和边。该提示在整个研究中保持不变。

#### 2. 零样本与少样本识别

**零样本识别（Zero-shot Recognition）**：
- 不提供任何额外的上下文或示例
- LLM仅基于初始指令和图像生成响应
- 适用于简单图样或LLM已有足够先验知识的情况

**少样本识别（Few-shot Recognition）**：
- 提供标注好的示例（"shots"）供LLM参考
- 选择最复杂的图样作为示例（通过边数量衡量复杂度）
- 将示例图像、标注、新图像和指令拼接在提示中

少样本提示模板示例（一样本）：
```
For the first diagram, we know that the edges are:
{annotated edges}
Infer the edges in the same format for the second diagram. Output only edges, no text.
```

#### 3. 代码生成

采用基于事件的架构，系统在任意时刻处于唯一状态，通过事件触发状态迁移。生成的C++代码包含三个部分：

**第一部分：状态枚举**
```cpp
enum class State {
    USB, WWW, ERP, JVM, CDN, LTE
};

std::string format_state(State const state) {
    switch (state) {
        case State::USB: return "USB";
        // ...
    }
    return "?";
}
```

**第二部分：状态处理函数**
为每个状态生成独立的处理函数，开发者需要填充具体的迁移逻辑：
```cpp
State handle_ERP(Event const & event) {
    // Check the event and
    // return one of the following states:
    // - CDN
    // - USB
    // - WWW
    return State::ERP;
}
```

**第三部分：主循环**
```cpp
void handle_state(State const last_state, State const new_state) {
    switch (last_state) {
        case State::ERP: return handle_ERP(new_state);
        case State::JVM: return handle_JVM(new_state);
        // ...
        default: throw std::runtime_error("Unknown state " + format_state(last_state));
    }
}

int main() {
    State state = State::JVM;
    for(;;) {
        auto event = wait_for_event();
        state = handle_event(state, event);
    }
}
```

开发者可以修改每个部分的模板，实现自定义命名空间或异常处理。

#### 4. 测试用例生成

采用基于覆盖率的方法，为每个状态图生成测试用例。测试用例定义为图中的路径，通过选择一组路径来满足预定义的覆盖准则（如边覆盖）。

使用改进的深度优先搜索算法生成覆盖所有边的路径集合。例如，对于图1中的状态图，以下路径集合覆盖所有边：
- RSA → IPX → LVM → IPX → GUI → RSA
- RSA → IPX → LVM → IPX → RSA
- RSA → RSA

生成的单元测试示例（使用Google Test框架）：
```cpp
#include <gtest/gtest.h>

TEST(App, ERP) {
    // Check path ['JVM', 'ERP', 'USB', 'LTE', 'JVM']
    Event event;
    auto state = State::JVM;

    // TODO: fill event appropriately
    state = handle_event(state, event);
    ASSERT_EQ(state, State::JVM);

    // TODO: fill event appropriately
    state = handle_event(state, event);
    ASSERT_EQ(state, State::ERP);

    // ...
    state = handle_event(state, event);
    ASSERT_EQ(state, State::JVM);
}
```

### 方法优势

1. **泛化能力强**：LLM在海量数据上训练，能够处理不同风格的状态图，无需针对每种风格重新训练
2. **设置简单**：只需提示工程，无需标注数据、训练模型、调整超参数
3. **可审查性高**：两步流程（识别+生成）使得审查更容易，识别结果（边列表）比生成的代码更容易验证
4. **自动化程度高**：识别和生成过程完全自动化，生成过程不到1秒
5. **质量保证**：基于覆盖准则的测试生成确保高代码覆盖率

## 实验与评估

### 数据集

#### 1. 图样打乱处理

由于版权原因，研究对图样进行了预处理：使用OCR模型识别文本区域，将其替换为随机的技术术语缩写（如ICQ、DNS、IOT）。打乱后的图样在视觉上与原始图样相似，但不泄露版权信息。

#### 2. IEC 61158 (PROFINET)

- **规范**：国际标准，定义工业自动化中现场总线通信系统的协议
- **文档规模**：IEC 61158-6-10，PDF格式，1183页
- **状态图数量**：80个
- **复杂度**：
  - 节点数量：平均3.5±2.1个，仅2个图样超过7个节点
  - 边数量：平均8.2±6.6条，仅4个图样超过18条边，最复杂的有37条边
- **特点**：图样不算过于复杂，但解析困难，许多边连接在一起，即使人类也难以处理交叉

#### 3. IEC 62541 (OPC UA)

- **规范**：国际标准，定义工业自动化中安全、可靠、平台无关的数据交换协议
- **文档规模**：24个部分，PDF格式，总计1830页
- **状态图数量**：15个
- **复杂度**：
  - 节点数量：平均13.1±8.6个，最多29个
  - 边数量：平均8.5±5.3条，最多18条
- **特点**：包含边标签和节点对之间的多重边，这些对读者有信息价值，但在本研究设置中被视为噪声

### 主要实验结果

#### 1. 不同LLM模型对比（零样本识别，PROFINET数据集）

| 模型 | 准确率 |
|------|--------|
| gpt-4o-2024-08-06 | 68% |
| claude-3-sonnet-20240229 | 40% |
| Llama-3.2-11b-vision-preview | 16% |

结论：LLM选择对性能至关重要，gpt-4o表现远超其他模型。后续实验均使用gpt-4o。

#### 2. 零样本识别详细分析（gpt-4o，PROFINET数据集）

- **完全正确识别**：18个图样（占80个的22.5%）
- **最多3个错误**：53个图样（占80个的66.3%）
- **总体统计**：
  - 真实边总数：657条
  - 正确识别：411条（63%）
  - 缺失边：246条（37%）
  - 幻觉边：92条
- **节点识别**：几乎完美，仅2个图样缺失1个节点，4个图样幻觉1个节点
- **初始状态识别**：所有图样均正确识别（除1个幻觉节点的情况）

**错误分析**：
- 错误数量随图样复杂度（边数量）增长，但呈亚线性增长
- 缺失边比幻觉边更常见
- 边比节点更难识别（边不明显，节点清晰可辨）

#### 3. 少样本识别效果（PROFINET数据集）

| 样本数 | 缺失边 | 幻觉边 | 总错误 |
|--------|--------|--------|--------|
| 零样本 | 245 | 92 | 337 |
| 一样本 | 124 | 121 | 245 |
| 二样本 | 129 | 83 | 212 |
| 三样本 | 130 | 78 | 208 |

**关键发现**：
- 提供示例总体上减少错误（从337降至208）
- 一样本大幅减少缺失边（从245降至124），但增加幻觉边（从92升至121），推测是单个示例过度"启发"了模型
- 二样本和三样本效果相近，提供更多示例似乎"压倒"了模型
- 最佳配置：三样本，总错误208个

#### 4. 跨规范泛化能力（OPC UA数据集）

| 样本数 | 缺失边 | 幻觉边 | 总错误 |
|--------|--------|--------|--------|
| 零样本 | 57 | 59 | 116 |
| 一样本 | 121 | 14 | 135 |
| 二样本 | 60 | 68 | 128 |
| 三样本 | 64 | 83 | 147 |

**关键发现**：
- 零样本表现最好（总错误116个）
- 提供示例反而增加错误，这与PROFINET结果相反
- 原因：OPC UA图样复杂度和多样性更高，边标签导致幻觉，模型难以区分节点标签和边标签
- 尽管如此，零样本仍正确识别45%的边（57/127），大约减半了手工工作量

#### 5. 代码和测试生成统计

| 数据集 | 代码行数 | 测试行数 |
|--------|----------|----------|
| OPC UA | 1614 | 1034 |
| PROFINET | 7017 | 3934 |

- 生成过程（不包括状态机提取）耗时不到1秒
- 相比手工工作流程，效率提升巨大
- 生成的单元测试构造性地覆盖整个代码库，质量高

#### 6. 消融实验

**传统计算机视觉方法对比**：
- 使用公开的最先进的基于神经网络的图样识别工具（在业务流程图上训练）
- 结果：在PROFINET图样上完全失败，无法识别边
- 结论：基于计算机视觉的工具泛化能力不足，无法用于通用图样识别

**直接端到端生成对比**：
- 尝试使用LLM直接从图样生成代码和测试（一样本）
- 结果：
  - 生成的代码乍看合理，但包含难以发现的细微错误（如幻觉状态）
  - 图样识别错误传播到代码和测试生成
  - 测试生成无法满足覆盖准则（LLM无法执行图算法）
- 结论：两步方法（识别+生成）优于端到端方法，可审查性更高

### 评估指标

1. **准确率**：正确识别的边占真实边的比例
2. **缺失边数量**：真实存在但LLM未识别的边
3. **幻觉边数量**：LLM识别但实际不存在的边
4. **生成代码行数**：自动生成的C++代码行数
5. **生成测试行数**：自动生成的单元测试行数

### 方法的优势和局限性

**优势**：
1. LLM在状态图识别上表现优于传统计算机视觉方法
2. 泛化能力强，能处理不同风格的图样（PROFINET和OPC UA）
3. 设置简单，只需提示工程，无需标注和训练
4. 显著减少手工工作量（识别63%和45%的边）
5. 自动生成数千行代码和测试，生成速度快（不到1秒）
6. 两步方法提高可审查性，低技能操作员也能审查识别结果

**局限性**：
1. 裁剪步骤仍需手工完成，自动裁剪方法精度不足
2. LLM会遗漏边（37%）或产生幻觉边（14%），需要人工审查修正
3. 少样本学习效果不稳定，提供过多示例可能"压倒"模型
4. 对于复杂图样（如OPC UA的边标签、多重边）识别率下降
5. 直接端到端生成代码质量不佳，难以发现细微错误，无法满足覆盖准则
6. 当前LLM能力对方法性能构成限制，但随着LLM发展会改善

## 与本研究的关系

### 相关性分析

本论文与博士研究"基于控制系统软件需求的LLM状态机结构化建模方法"高度相关，但关注点不同：

1. **输入形式不同**：
   - 本论文：从PDF规范文档中的状态图图像识别状态机
   - 本研究：从非形式化的自然语言需求文本生成状态机

2. **问题域相似**：
   - 都关注工业控制系统领域（本论文是工业4.0通信协议，本研究是控制系统软件）
   - 都使用LLM处理状态机相关任务
   - 都强调形式化和可验证性

3. **方法理念相通**：
   - 都采用多步流程而非端到端生成，提高可审查性和可靠性
   - 都关注自动化生成后的验证和修复问题
   - 都强调减少手工工作量和提高软件正确性

### 可借鉴之处

1. **提示工程的迭代优化方法**：
   - 本论文展示了如何从简单指令逐步优化到最终版本
   - 通过添加格式说明、示例、显式约束来改进LLM输出
   - 这种方法可应用于本研究的需求到状态机生成任务

2. **零样本与少样本学习的权衡**：
   - 本论文发现少样本学习并非总是更好，可能"压倒"模型
   - 对于复杂多样的数据（如OPC UA），零样本可能更优
   - 本研究在设计提示策略时应考虑这种权衡

3. **两步流程的优势**：
   - 识别+生成的两步方法比端到端生成更可靠、更易审查
   - 中间表示（边列表）比最终代码更容易验证
   - 本研究的"生成-验证-修复"闭环也体现了类似的分步理念

4. **基于覆盖准则的测试生成**：
   - 本论文使用边覆盖准则生成测试路径
   - 这与本研究的"基于模型元素的验证场景生成"思路一致
   - 可借鉴其深度优先搜索算法生成覆盖路径

5. **错误类型分析**：
   - 本论文区分缺失边和幻觉边两类错误
   - 这与本研究的缺陷分类（δ型、τ型、state型）有相似之处
   - 可借鉴其错误分析方法来评估生成的状态机质量

6. **模板化代码生成**：
   - 本论文使用模板生成C++代码，允许开发者自定义
   - 本研究可借鉴这种方法生成状态机的DSL代码（如pyfcstm）

### 存在的不足和改进空间

1. **输入形式局限**：
   - 本论文只处理图像输入，无法处理自然语言需求
   - 本研究需要从需求文本生成状态机，问题更复杂

2. **缺乏时间约束处理**：
   - 本论文生成的状态机不包含时间约束和守卫条件
   - 本研究关注时间自动机，需要处理时钟约束和不变式

3. **缺乏形式化验证**：
   - 本论文只生成代码和测试，不进行形式化验证
   - 本研究强调基于模型检查的验证方法（如UPPAAL）

4. **缺乏迭代修复机制**：
   - 本论文识别错误后需要人工修正，没有自动修复机制
   - 本研究的第四个主题专注于"面向已知缺陷的迭代式模型修复"

5. **评估指标单一**：
   - 本论文主要评估边识别准确率，缺少语义正确性评估
   - 本研究需要评估生成的状态机是否满足安全性质和活性性质

6. **数据集规模有限**：
   - 本论文只使用两个规范（95个图样），泛化能力有待验证
   - 本研究使用101条功能安全需求，涵盖9个控制系统

### 对本研究的启发

1. **多模态输入的可能性**：
   - 如果需求文档中包含状态图草图，可结合图像识别和文本理解
   - 可探索需求文本+参考图样的混合输入方式

2. **中间表示的重要性**：
   - 设计合适的中间表示（如本论文的边列表）能提高可审查性
   - 本研究可设计状态机的中间表示，便于验证和修复

3. **分步生成的必要性**：
   - 端到端生成虽然简单，但质量不佳且难以调试
   - 本研究应采用分步方法：需求分析→状态识别→迁移生成→约束添加

4. **LLM能力的局限性**：
   - LLM无法执行图算法（如覆盖路径生成）
   - 本研究应结合LLM和传统算法：LLM生成结构，算法进行验证和优化

5. **提示工程的关键性**：
   - 精心设计的提示对LLM性能至关重要
   - 本研究应投入足够精力优化提示，可能需要针对不同子任务设计不同提示

6. **评估方法的设计**：
   - 需要设计多维度的评估指标：结构准确性、语义正确性、可验证性
   - 可借鉴本论文的错误分类方法（缺失vs幻觉）

## 重要的相关工作

本论文引用了43篇文献，涵盖图样识别、代码生成、测试生成等多个领域。按照文献在论文中的作用，可分为以下五类：

### 1. 重要的前身类工作

**1.1 Otto et al. (2023) - 从规范到测试用例的基于模型的方法**

- **标题**：From specification to test cases: A model-based approach using image recognition
- **作者**：B. Otto, R. Gröpler, K. Meinecke, T. Kleinert
- **发表**：2023年
- **主要内容**：这是作者团队的前期工作，提出了使用图像识别从规范文档中提取状态机并生成测试用例的方法。该工作使用传统计算机视觉技术（而非LLM）进行图样识别。
- **论文中的引用**：
  - 第770-771行（参考文献[15]）："B. Otto, R. Gröpler, K. Meinecke, and T. Kleinert, 'From specification to test cases: A model-based approach using image recognition,' 2023."
  - 论文在Related Work章节（第137行）提到："Such systems have been successfully applied to...state diagrams [15]"，将其列为计算机视觉方法成功应用于状态图识别的案例
- **局限性**：
  - 使用传统计算机视觉方法，需要组合多个专门模型（OCR、线检测、目标检测等）
  - 泛化能力有限，对新图样风格需要重新训练
  - 设置复杂，需要标注数据和模型训练
- **与本论文的关系**：本论文是该前期工作的直接延续和改进，核心创新在于用LLM替代传统计算机视觉方法，解决了泛化能力差和设置复杂的问题。
- **佐证内容**：为本研究提供了基础框架（从规范提取状态机→生成测试），本论文在此基础上改进了识别方法（从计算机视觉→LLM）并增加了代码生成功能。

**1.2 Otto et al. (2022) - 基于模型的测试用例生成**

- **标题**：Model-Based Test Case Generation for Compliance Checking of Reactive Asset Administration Shells
- **作者**：B. Otto, K. Meinecke, T. Kleinert
- **发表**：2022年，Universitätsbibliothek der RWTH Aachen
- **主要内容**：作者团队的另一项前期工作，关注基于模型的测试用例生成，用于反应式资产管理壳（Asset Administration Shells）的合规性检查。
- **论文中的引用**：
  - 第816-818行（参考文献[31]）："B. Otto, K. Meinecke, and T. Kleinert, Model-Based Test Case Generation for Compliance Checking of Reactive Asset Administration Shells. Universitätsbibliothek der RWTH Aachen, 2022."
  - 论文在Related Work的Model-based Testing章节（第209-211行）引用："In [31] the authors use OpenAPI descriptions to generate test cases for digital twins automatically. They highlight the improved efficiency and coverage of automated test case generation in comparison to manual test case definition."
- **主要发现**：自动化测试用例生成相比手工定义具有更高的效率和覆盖率
- **与本论文的关系**：为本论文的测试生成方法提供了理论基础，强调了自动化测试生成的重要性和基于覆盖准则的必要性。
- **佐证内容**：论证了自动化测试生成的价值，为本论文的测试生成模块提供了方法论支持。

**1.3 Braunisch et al. (2023) - 生成式和模型驱动的SDK开发**

- **标题**：Empowering industry 4.0 with generative and model-driven sdk development
- **作者**：N. Braunisch, M. Ristin-Kaufmann, R. Lehmann, M. Wollschlaeger, H. W. van de Venn
- **发表**：IECON 2023-49th Annual Conference of the IEEE Industrial Electronics Society, IEEE, 2023
- **主要内容**：使用Python子集建模数字孪生的数据结构，利用形式化描述生成多种语言的SDK。这是作者团队（包括本论文的共同作者Braunisch、Ristin、van de Venn、Wollschlaeger）的前期工作。
- **论文中的引用**：
  - 第798-801行（参考文献[26]）："N. Braunisch, M. Ristin-Kaufmann, R. Lehmann, M. Wollschlaeger, and H. W. van de Venn, 'Empowering industry 4.0 with generative and model-driven sdk development,' in IECON 2023-49th Annual Conference of the IEEE Industrial Electronics Society. IEEE, 2023, pp. 1–6."
  - 论文在Related Work的Model-based Code Generation章节（第185-188行）引用："For example, the authors of [26] use a subset of the Python programming language to model data structures of Digital Twins and leverage this formalization to generate SDKs in various languages."
- **与本论文的关系**：展示了模型驱动代码生成在工业4.0中的应用，为本论文的代码生成方法提供了工业4.0背景下的实践经验。
- **佐证内容**：为本研究的模型驱动代码生成提供了工业4.0领域的应用案例和方法论支持。

### 2. 直接参与实验的baseline

本论文没有明确的baseline对比实验，但在消融实验中对比了以下方法：

**2.1 传统计算机视觉方法（Sketch2BPMN工具）**

- **工具**：Sketch2BPMN（https://sketch2bpmn.informatik.uni-mannheim.de/）
- **相关论文**：Schäfer et al. (2023) - Sketch2process: End-to-end BPMN sketch recognition based on neural networks
- **作者**：B. Schäfer, H. van der Aa, H. Leopold, H. Stuckenschmidt
- **发表**：Transactions on Software Engineering, vol. 49, no. 4, 2023
- **主要内容**：基于神经网络的端到端BPMN草图识别系统，在业务流程图上训练。
- **论文中的引用**：
  - 第768-770行（参考文献[14]）："B. Schäfer, H. van der Aa, H. Leopold, and H. Stuckenschmidt, 'Sketch2process: End-to-end BPMN sketch recognition based on neural networks,' Transactions on Software Engineering, vol. 49, no. 4, 2023."
  - 论文在Related Work的Computer Vision章节（第136行）引用："business process diagrams [14]"
  - 论文在Ablations章节（第625-632行）详细描述了对比实验："We evaluated a publicly-available state-of-the-art diagram recognition tool based on neural networks on PROFINET dataset. Trained on business diagrams [14], vastly different from PROFINET diagrams, the tool consistently failed to recognize edges in diagrams like Figure 1. This corroborates that tools based on Computer Vision are not generalizable enough for general diagram recognition."
- **实验结果**：在PROFINET数据集上完全失败，无法识别边
- **与本论文的关系**：作为传统计算机视觉方法的代表，用于对比LLM方法的泛化能力优势。实验证明传统方法在跨领域图样识别上泛化能力不足。
- **佐证内容**：通过对比实验证明了LLM方法相对于传统计算机视觉方法的优越性，特别是在泛化能力和跨领域应用方面。

**2.2 不同LLM模型对比**

论文对比了三个LLM模型作为baseline：

- **gpt-4o-2024-08-06**：准确率68%（最佳）
- **claude-3-sonnet-20240229**：准确率40%
- **Llama-3.2-11b-vision-preview**：准确率16%

相关论文：
- Borji & Mohammadian (2025) - Battle of the wordsmiths: Comparing chatgpt, gpt-4, claude, and bard
- Dubey et al. (2024) - The llama 3 herd of models

### 3. 提供了重要论证的工作

**3.1 Moreno-García et al. (2019) - 复杂工程图样数字化的新趋势**

- **标题**：New trends on digitisation of complex engineering drawings
- **作者**：C. F. Moreno-García, E. Elyan, C. Jayne
- **发表**：Neural Computing and Applications (NCAA), vol. 31, 2019
- **主要内容**：综述了复杂工程图样数字化的趋势和挑战，指出传统计算机视觉方法的局限性。
- **论文中的引用**：
  - 第743-745行（参考文献[6]）："C. F. Moreno-García, E. Elyan, and C. Jayne, 'New trends on digitisation of complex engineering drawings,' Neural Computing and Applications (NCAA), vol. 31, 2019."
  - 论文在Related Work的Computer Vision章节（第126行）引用："Computer vision in its strict sense...has been long used for recognizing different types of diagrams [6]"
  - 论文在第146-150行论证传统方法的泛化问题："Models can only recognize elements seen during training, but training sets are limited since they are tailored to niche applications [6]. Re-training for new diagram types is impractical for end-users, who often lack the expertise and infrastructure for data annotation and model updates."
- **局限性**：指出传统方法训练集有限，针对特定应用，泛化能力差
- **与本论文的关系**：为本论文论证传统计算机视觉方法的局限性提供了理论支持，强调了泛化能力的重要性。
- **佐证内容**：论证了传统计算机视觉方法在图样识别中的泛化问题，为本论文采用LLM方法提供了动机。

**3.2 Eskenazi et al. (2017) - 文档分割算法综述**

- **标题**：A comprehensive survey of mostly textual document segmentation algorithms since 2008
- **作者**：S. Eskenazi, P. Gomez-Krämer, J.-M. Ogier
- **发表**：Pattern recognition, vol. 64, pp. 1–14, 2017
- **主要内容**：综述了文档分割算法，指出自动裁剪方法仍需改进。
- **论文中的引用**：
  - 第827-829行（参考文献[34]）："S. Eskenazi, P. Gomez-Krämer, and J.-M. Ogier, 'A comprehensive survey of mostly textual document segmentation algorithms since 2008,' Pattern recognition, vol. 64, pp. 1–14, 2017."
  - 论文在Methodology的Cropping章节（第236-239行）引用："Although automatic cropping approaches exist, they still require significant improvements in precision and adaptability for diverse documents [34], so this work focuses on recognition, leaving comprehensive cropping methods for future research."
- **与本论文的关系**：论证了自动裁剪方法的局限性，解释了为什么本论文采用手工裁剪。
- **佐证内容**：论证了当前自动裁剪技术的不足，为本论文的手工裁剪选择提供了合理性支持。

### 4. 在技术上提供了支持的工作

**4.1 Vaswani et al. (2017) - Transformer架构**

- **标题**：Attention is all you need
- **作者**：A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, I. Polosukhin
- **发表**：Neural Information Processing Systems (NeurIPS), 2017
- **主要内容**：提出了Transformer神经网络架构和注意力机制，是现代LLM的基础。
- **论文中的引用**：
  - 第738-740行（参考文献[4]）："A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, 'Attention is all you need,' in Neural Information Processing Systems (NeurIPS), 2017."
  - 论文在Related Work的LLM章节（第154-156行）引用："In recent years, LLMs have become widely popular [4]. At their core is a transformer neural network with an attention mechanism, enabling context-aware sequence translation, such as turning a question into an answer."
- **与本论文的关系**：提供了本论文使用的LLM的核心技术基础（Transformer架构）。
- **技术使用**：本论文直接使用基于Transformer架构的LLM（gpt-4o、Claude、Llama）进行图样识别。

**4.2 Dosovitskiy et al. (2021) - Vision Transformer**

- **标题**：An image is worth 16x16 words: Transformers for image recognition at scale
- **作者**：A. Dosovitskiy et al.
- **发表**：Learning Representations, 2021
- **主要内容**：将Transformer架构扩展到图像识别，通过将图像分块编码为序列元素，使Transformer能够处理图像模态。
- **论文中的引用**：
  - 第741-742行（参考文献[5]）："A. Dosovitskiy et al., 'An image is worth 16x16 words: Transformers for image recognition at scale,' in Learning Representations, 2021."
  - 论文在Related Work的LLM章节（第157-158行）引用："Transformers can be adapted for other modalities, such as images, by encoding image patches as sequence elements [5]."
- **与本论文的关系**：提供了LLM处理图像输入的技术基础，使得本论文能够将状态图图像作为LLM的输入。
- **技术使用**：本论文使用的多模态LLM（如gpt-4o）基于Vision Transformer技术处理图像输入。

**4.3 Brown et al. (2020) - Few-shot Learning**

- **标题**：Language models are few-shot learners
- **作者**：T. Brown and many other authors
- **发表**：Neural Information Processing Systems (NeurIPS), 2020
- **主要内容**：提出了少样本学习（few-shot learning）的概念，展示了大语言模型通过少量示例就能学习新任务的能力。
- **论文中的引用**：
  - 第778-779行（参考文献[19]）："T. Brown and many other authors, 'Language models are few-shot learners,' in Neural Information Processing Systems (NeurIPS), 2020."
  - 第830-831行（参考文献[35]，与[19]相同）
  - 论文在Introduction章节（第96-97行）引用："Since there is only one model to capture all the training data, this one model profits from transfer learning effects coming from different domains."
  - 论文在Methodology的Few-shot Recognition章节（第314-316行）引用："In the case of a few-shot recognition, we supply additional annotated examples ('shots') to the LLM so that it can 'reason' not only over the prompt and pre-trained knowledge, but also over the concrete input-output examples, which can substantially increase the performance [35]."
  - 论文在Related Work的LLM章节（第162-163行）引用："They are therefore trained on vast datasets, enabling exceptional generalization [19]."
- **与本论文的关系**：提供了本论文少样本识别方法的理论基础和技术支持。
- **技术使用**：本论文直接采用少样本学习技术，通过提供1-3个标注示例来提高LLM的识别性能。

**4.4 Baek et al. (2019) - OCR技术（CRAFT）**

- **标题**：Character region awareness for text detection
- **作者**：Y. Baek, B. Lee, D. Han, S. Yun, H. Lee
- **发表**：Computer Vision and Pattern Recognition (CVPR), 2019
- **主要内容**：提出了CRAFT（Character Region Awareness For Text detection）方法，用于文本检测和OCR。
- **论文中的引用**：
  - 第836-838行（参考文献[38]）："Y. Baek, B. Lee, D. Han, S. Yun, and H. Lee, 'Character region awareness for text detection,' in Computer Vision and Pattern Recognition (CVPR), 2019."
  - 论文在Experiments的Scrambling章节（第469行）引用："We ran an off-the-shelf OCR model [38], identified the text regions and replaced them with a random techno-babble abbreviations"
- **与本论文的关系**：用于数据预处理，识别状态图中的文本区域并进行打乱处理以保护版权。
- **技术使用**：本论文使用CRAFT OCR模型对状态图进行文本识别和替换。

**4.5 Sedgewick (2001) - 图算法**

- **标题**：Algorithms in C, Part 5: Graph Algorithms (3rd ed.)
- **作者**：R. Sedgewick
- **发表**：Addison Wesley Professional, 2001
- **主要内容**：经典的图算法教材，包含深度优先搜索等算法。
- **论文中的引用**：
  - 第834-835行（参考文献[37]）："R. Sedgewick, Algorithms in C, Part 5: Graph Algorithms, 3rd ed. Addison Wesley Professional, 2001."
  - 论文在Test Case Generation章节（第436-437行）引用："We used a modified depth-first search to generate such paths [37]."
- **与本论文的关系**：提供了测试用例生成中使用的图遍历算法（改进的深度优先搜索）。
- **技术使用**：本论文使用改进的深度优先搜索算法生成覆盖所有边的测试路径。

### 5. 其他重要工作

**5.1 工业标准文档**

**IEC 61158标准（PROFINET）**
- **标题**：Industrial communication networks - fieldbus specifications
- **发布机构**：International Electrotechnical Commission (IEC)
- **年份**：2023
- **论文中的引用**：
  - 第729-731行（参考文献[1]）："'IEC 61158: Industrial communication networks - fieldbus specifications,' International Electrotechnical Commission (IEC), 2023, part 1 to Part 6: Overview, protocol-specific details, and guidelines."
  - 论文在Introduction（第51行）和Experiments（第474-484行）多次引用
- **作用**：提供了本论文的主要数据集来源（80个状态图）

**IEC 62541标准（OPC UA）**
- **标题**：OPC Unified Architecture - Specifications
- **发布机构**：International Electrotechnical Commission (IEC)
- **年份**：2020
- **论文中的引用**：
  - 第839-841行（参考文献[39]）："IEC 62541: OPC Unified Architecture - Specifications, International Electrotechnical Commission (IEC) Std., 2020, available as parts 1–14 covering different aspects of the OPC UA standard."
  - 论文在Experiments（第494-510行）详细描述
- **作用**：提供了本论文的第二个数据集来源（15个状态图），用于验证方法的泛化能力

**5.2 LLM相关工作（工业4.0应用）**

**Koziolek et al. (2024) - 基于LLM和检索增强的控制代码生成**
- **标题**：LLM-based and retrieval-augmented control code generation
- **作者**：H. Koziolek, S. Grüner, R. Hark, V. Ashiwal, S. Linsbauer, N. Eskandani
- **发表**：Large Language Models for Code (LLM4Code), 2024
- **论文中的引用**：
  - 第780-782行（参考文献[20]）
  - 论文在Related Work（第164-165行）引用："In Industry 4.0, LLMs have been used for tasks like generating control code [20], [21]"
- **作用**：展示了LLM在工业4.0控制代码生成中的应用，为本论文提供了领域背景

**Koziolek & Koziolek (2024) - 基于图像识别的LLM控制代码生成**
- **标题**：LLM-based control code generation using image recognition
- **作者**：H. Koziolek, A. Koziolek
- **发表**：Large Language Models for Code (LLM4Code), 2024
- **论文中的引用**：
  - 第789-791行（参考文献[23]）
  - 论文在Related Work（第167行）引用："including recognition of diagrams such as piping and instrumentation diagrams (P&ID) [23]"
  - 论文在第173-176行对比："Unlike prior work [23], which combines recognition and generation in a single step, our approach splits them in two (recognition followed by generation). As shown in Subsubsection IV-F2, this two-step split offers advantages."
- **作用**：提供了LLM图样识别的参考方法，但本论文采用两步方法而非端到端方法

**5.3 测试生成相关工作**

**Chen et al. (2024) - Chatunitest**
- **标题**：Chatunitest: A framework for llm-based test generation
- **作者**：Y. Chen, Z. Hu, C. Zhi, J. Han, S. Deng, J. Yin
- **发表**：Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering, 2024
- **论文中的引用**：
  - 第819-822行（参考文献[32]）
  - 论文在Related Work的LLM-based Test Generation章节（第216-217行）引用："In [32] the authors present Chatunitest, a tool to derive unit tests automatically. Chatunitest is able to cover more lines than other popular traditional or LLM-based tools."
- **作用**：展示了LLM在单元测试生成中的应用，为本论文的测试生成提供了参考

**Ryan et al. (2024) - SymPrompt**
- **标题**：Code-aware prompting: A study of coverage-guided test generation in regression setting using llm
- **作者**：G. Ryan, S. Jain, M. Shang, S. Wang, X. Ma, M. K. Ramanathan, B. Ray
- **发表**：Proceedings of the ACM on Software Engineering, vol. 1, no. FSE, pp. 951–971, 2024
- **论文中的引用**：
  - 第823-826行（参考文献[33]）
  - 论文在Related Work的LLM-based Test Generation章节（第219-223行）引用："Another tool, SymPrompt [33], offers a multi-stage approach for test case generation where each phase is fed with information about execution paths of the previously generated tests. This way, the authors are able to improve coverage compared to single-pass solutions."
- **作用**：展示了基于覆盖率的LLM测试生成方法，与本论文的基于覆盖准则的测试生成理念一致

**5.4 其他图样识别工作**

论文还引用了多篇图样识别相关工作，包括：
- 工程图样识别：Mani et al. (2020), Rahul et al. (2019), Kang et al. (2019)
- UML类图识别：Chen et al. (2022), Karasneh & Chaudron (2013), Koenig et al. (2023)
- 手绘图样识别：Schäfer et al. (2021)
- 软件开发中的LLM应用：Rasnayaka et al. (2024), Lin et al. (2024)

这些工作为本论文提供了图样识别领域的背景知识和技术参考。

## 文献分类总结

本论文共引用43篇文献，按作用分类如下：

1. **前身类工作（3篇）**：作者团队的前期工作，包括基于计算机视觉的状态图识别、基于模型的测试生成、工业4.0的SDK生成，为本论文提供了研究基础和方法框架。

2. **实验baseline（4篇）**：包括传统计算机视觉工具（Sketch2BPMN）和不同LLM模型的对比论文，用于验证本论文方法的优越性。

3. **论证支持（2篇）**：论证了传统计算机视觉方法的局限性（泛化能力差、自动裁剪困难），为本论文采用LLM方法提供了动机。

4. **技术支持（5篇）**：提供了核心技术基础，包括Transformer架构、Vision Transformer、Few-shot Learning、OCR技术、图算法，这些技术被本论文直接采用或启发了方法设计。

5. **其他支持（29篇）**：包括工业标准文档（提供数据集）、LLM在工业4.0的应用（提供领域背景）、测试生成方法（提供参考）、其他图样识别工作（提供背景知识）等。

本论文的核心创新在于：
- 用LLM替代传统计算机视觉方法进行状态图识别，解决了泛化能力差和设置复杂的问题
- 采用两步流程（识别+生成）而非端到端生成，提高了可审查性和可靠性
- 通过提示工程优化LLM输出，支持零样本和少样本识别
- 基于覆盖准则的自动化测试生成，确保高代码覆盖率

实验结果表明，在PROFINET数据集上LLM识别准确率达63%，在OPC UA数据集上达45%，自动生成了数千行C++代码和测试用例，显著减少了手工工作量。
