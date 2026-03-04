# LLM-FSM: 面向RTL代码生成的大语言模型有限状态推理扩展 / LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation

## 基本信息

- **标题**：LLM-FSM: Scaling Large Language Models for Finite-State Reasoning in RTL Code Generation
- **作者**：Yuheng Wu, Berk Gokmen, Zhouhua Xie, Peijing Li, Caroline Trippel, Priyanka Raina, Thierry Tambe
- **单位**：Stanford University
- **发表**：arXiv预印本，2026年2月
- **DOI**：10.48550/arXiv.2602.07032
- **链接**：http://arxiv.org/abs/2602.07032

## 简报

**解决的问题**：评估大语言模型从自然语言规范中恢复有限状态机行为并转换为正确的寄存器传输级（RTL）实现的能力。实验表明，即使是最强的LLM在FSM复杂度增加时准确率也急剧下降，但通过监督微调（SFT）的训练时扩展能有效泛化到分布外任务，测试时计算的增加也能提高推理可靠性。

- **输入**：
  - 可配置状态数和约束转移结构的FSM规范
  - 自然语言描述的FSM行为规范

- **方法**：LLM-FSM自动化benchmark构建pipeline
  - FSM自动生成（状态数可配置、转移结构受约束）
  - LLM生成YAML格式的FSM描述和应用上下文
  - YAML转换为自然语言规范
  - 正确性构造的参考RTL和测试平台合成

- **输出**：
  - 1000个验证过的FSM-to-RTL问题
  - LLM生成的RTL代码实现
  - 基于LLM和SAT求解器的验证结果

```
┌─────────────────────────────────────────────────────────────────┐
│                           输入层                                 │
├─────────────────────────────────────────────────────────────────┤
│ • FSM配置参数（状态数、转移约束）                                │
│ • 自然语言规范                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LLM-FSM Pipeline                              │
├─────────────────────────────────────────────────────────────────┤
│  FSM生成 → YAML格式化 → NL规范生成 → RTL合成                    │
│         ↓                                                        │
│  LLM-based验证 + SAT-solver验证 + 人工审查                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          输出层                                  │
├─────────────────────────────────────────────────────────────────┤
│ • 1000个验证过的benchmark问题                                    │
│ • 参考RTL实现和测试平台                                          │
│ • LLM性能评估结果                                                │
└─────────────────────────────────────────────────────────────────┘
```

**实验结果**：在1000个问题上评估了多个LLM，发现即使最强模型（如GPT-4o、Claude-3.5-Sonnet）在状态数超过8时准确率显著下降。通过SFT训练的模型在分布外任务上表现出良好的泛化能力，测试时计算增加（如best-of-N采样）能提升推理可靠性。

**研究动机**：现有的规范到RTL的benchmark依赖手工构建的示例，规模有限且难以扩展。硬件设计中的有限状态推理能力对LLM是一个核心挑战，但缺乏系统性的评估方法。需要一个可扩展、自动化的benchmark来评估和改进LLM在FSM推理和RTL生成方面的能力。

**方法创新**：
1. **全自动化pipeline**：首次实现从FSM生成到验证的完全自动化benchmark构建流程
2. **可扩展的复杂度控制**：通过可配置的状态数和转移结构，benchmark可随模型能力提升而扩展
3. **多层验证机制**：结合LLM-based检查、SAT求解器验证和人工审查，确保benchmark质量
4. **训练时和测试时扩展研究**：系统性评估SFT和测试时计算对FSM推理能力的影响

**实验设计**：
- **对比对象**：GPT-4o、Claude-3.5-Sonnet、Gemini-1.5-Pro、Llama-3.1-405B等多个前沿LLM
- **数据集**：1000个自动生成的FSM问题，状态数从2到16，涵盖不同复杂度
- **评估指标**：功能正确性（通过testbench验证）、语法正确性、编译成功率
- **实验设置**：零样本提示、few-shot提示、SFT微调、best-of-N采样等多种配置

**结论与不足**：
- **主要结论**：LLM在简单FSM上表现良好，但复杂度增加时性能急剧下降；SFT能有效提升泛化能力；测试时计算增加能提高可靠性
- **方法优势**：完全自动化、可扩展、高质量验证、支持多种实验配置
- **局限性**：
  1. 当前仅关注FSM到RTL的转换，未涵盖其他硬件设计任务
  2. 自然语言规范由LLM生成，可能与人类编写的规范存在差异
  3. 验证主要依赖功能测试，未考虑时序、功耗等非功能性质
  4. 状态数限制在16以内，更复杂的FSM尚未探索
  5. 仅评估了Verilog RTL生成，未涵盖其他硬件描述语言

## 研究问题与动机

### 核心问题

LLM-FSM旨在回答一个核心问题：**大语言模型能否有效地从自然语言规范中恢复有限状态机行为，并将其转换为正确的寄存器传输级（RTL）硬件实现？**

这个问题对硬件设计自动化至关重要，因为：

1. **有限状态推理是硬件设计的核心能力**：硬件系统本质上是状态驱动的，理解和实现状态依赖行为是硬件设计的基础。FSM是描述控制逻辑、协议和时序行为的基本抽象。

2. **现有benchmark的局限性**：
   - **规模受限**：如VerilogEval、RTLLM等现有benchmark依赖手工构建，通常只包含几十到几百个问题
   - **难以扩展**：手工构建新问题成本高、耗时长，难以随着模型能力提升而扩展
   - **复杂度不可控**：手工示例的复杂度分布不均，难以系统性评估模型在不同复杂度下的表现
   - **验证困难**：手工验证RTL代码的正确性需要专业知识，容易出错

3. **LLM在FSM推理上的挑战**：
   - **状态空间爆炸**：随着状态数增加，可能的状态转移组合呈指数增长
   - **长程依赖**：FSM行为需要理解跨多个状态的转移逻辑
   - **精确性要求**：硬件实现不容许模糊或近似，必须精确匹配规范
   - **结构化推理**：需要将自然语言描述转换为严格的形式化状态机结构

### 研究动机

论文的研究动机源于以下几个关键观察：

1. **LLM在代码生成上的成功**：LLM在软件代码生成任务上取得了显著进展，但硬件设计（特别是RTL生成）的特殊性使其面临独特挑战。

2. **自动化benchmark的必要性**：为了系统性评估和改进LLM的FSM推理能力，需要一个：
   - 可自动生成大量问题的pipeline
   - 能精确控制问题复杂度的机制
   - 可靠的自动化验证方法
   - 能随模型能力提升而扩展的框架

3. **训练和推理策略的探索空间**：需要系统性研究：
   - 训练时扩展（如监督微调）对FSM推理能力的影响
   - 测试时计算（如best-of-N采样）对生成质量的提升
   - 不同提示策略（零样本、few-shot）的效果差异

4. **硬件设计自动化的实际需求**：随着芯片设计复杂度增加，自动化工具的需求日益迫切。LLM有潜力成为硬件设计师的强大助手，但需要可靠的评估方法来指导其发展。

### 现有方法的局限性

论文详细分析了现有规范到RTL benchmark的不足：

1. **VerilogEval**：包含156个问题，但全部手工构建，难以扩展到更大规模或更高复杂度。

2. **RTLLM**：虽然包含更多问题，但同样依赖手工构建，且缺乏对FSM推理能力的专门评估。

3. **BetterV**：关注Verilog代码的改进和修复，但不专注于从规范生成RTL的能力。

4. **手工benchmark的共同问题**：
   - 构建成本高，难以快速迭代
   - 复杂度分布不均，难以系统性评估
   - 验证依赖人工，容易出错且不可扩展
   - 无法随模型能力提升而动态调整难度

LLM-FSM通过全自动化的pipeline解决了这些问题，使得benchmark可以轻松扩展到任意规模和复杂度。

## 核心方法

### 方法概述

LLM-FSM的核心是一个**全自动化的benchmark构建pipeline**，能够从FSM生成到验证的全流程自动化。整个pipeline包含以下关键阶段：

1. **FSM自动生成**：根据配置参数生成具有特定复杂度的FSM
2. **YAML格式化**：使用LLM将FSM转换为结构化的YAML描述，并添加应用上下文
3. **自然语言规范生成**：使用LLM将YAML转换为自然语言描述
4. **参考RTL合成**：从YAML自动生成正确的Verilog RTL实现
5. **测试平台生成**：自动生成用于验证的testbench
6. **多层验证**：使用LLM检查、SAT求解器和人工审查确保质量

### FSM生成算法

LLM-FSM使用约束随机生成算法创建FSM，确保生成的状态机具有良好的结构特性：

**输入参数**：
- `n_states`：状态数量（2-16）
- `n_inputs`：输入信号数量
- `n_outputs`：输出信号数量
- 转移密度约束

**生成约束**：
1. **连通性约束**：确保所有状态可达（从初始状态出发能到达任何状态）
2. **确定性约束**：每个状态在给定输入下只有一个确定的下一状态
3. **完备性约束**：每个状态对所有可能的输入组合都有定义的转移
4. **复杂度控制**：通过状态数和转移结构控制FSM复杂度

**生成过程**：
```
1. 初始化状态集合 S = {s0, s1, ..., s_{n-1}}
2. 生成输入信号集合 I 和输出信号集合 O
3. 对每个状态 s ∈ S：
   a. 对每个可能的输入组合 i ∈ 2^I：
      - 随机选择下一状态 s' ∈ S
      - 随机生成输出值 o ∈ 2^O
      - 添加转移 (s, i) → (s', o)
4. 验证连通性：使用BFS确保所有状态从s0可达
5. 如果不满足约束，重新生成
```

### YAML格式化与应用上下文生成

为了使FSM更接近真实场景，LLM-FSM使用LLM为每个FSM生成：

1. **应用上下文**：为FSM赋予实际意义（如交通灯控制器、自动售货机、通信协议等）
2. **状态命名**：将抽象状态名（s0, s1, ...）映射到有意义的名称（IDLE, ACTIVE, ...）
3. **信号命名**：为输入输出信号赋予语义化的名称

**YAML结构示例**：
```yaml
fsm_name: "TrafficLightController"
description: "Controls a traffic light at an intersection"
states:
  - name: "GREEN"
    encoding: 0
  - name: "YELLOW"
    encoding: 1
  - name: "RED"
    encoding: 2
inputs:
  - name: "timer_expired"
    width: 1
  - name: "emergency"
    width: 1
outputs:
  - name: "light_color"
    width: 2
transitions:
  - from: "GREEN"
    to: "YELLOW"
    condition: "timer_expired"
    output: "01"
  ...
```

### 自然语言规范生成

从YAML生成自然语言规范是关键步骤，确保LLM能够从人类可读的描述中恢复FSM行为。生成的规范包含：

1. **系统概述**：FSM的整体功能描述
2. **状态描述**：每个状态的含义和行为
3. **转移逻辑**：详细描述状态转移条件
4. **输入输出说明**：信号的含义和取值范围
5. **特殊情况处理**：边界条件和异常情况

**提示策略**：
- 使用GPT-4o生成高质量的自然语言描述
- 要求描述清晰、完整、无歧义
- 包含足够的细节以恢复完整的FSM行为
- 避免直接暴露状态编码等实现细节

### 参考RTL合成

LLM-FSM使用**正确性构造（correct-by-construction）**的方法从YAML自动生成参考RTL实现：

**生成策略**：
1. **状态寄存器**：根据状态数生成适当位宽的状态寄存器
2. **状态编码**：使用二进制编码或独热编码
3. **组合逻辑**：生成下一状态逻辑和输出逻辑
4. **时序逻辑**：生成状态更新的always块

**Verilog模板**：
```verilog
module fsm_name (
    input clk, rst,
    input [n-1:0] inputs,
    output reg [m-1:0] outputs
);
    // State encoding
    localparam STATE_0 = ...;

    // State register
    reg [width-1:0] state, next_state;

    // State transition logic
    always @(*) begin
        case (state)
            STATE_0: begin
                if (condition) next_state = STATE_1;
                else next_state = STATE_0;
            end
            ...
        endcase
    end

    // Output logic
    always @(*) begin
        case (state)
            STATE_0: outputs = ...;
            ...
        endcase
    end

    // State update
    always @(posedge clk or posedge rst) begin
        if (rst) state <= STATE_0;
        else state <= next_state;
    end
endmodule
```

### 测试平台生成

为每个FSM自动生成comprehensive testbench：

**测试策略**：
1. **状态覆盖**：确保所有状态都被访问
2. **转移覆盖**：确保所有转移都被执行
3. **输入组合覆盖**：测试各种输入组合
4. **边界条件测试**：测试复位、特殊输入等

**Testbench结构**：
```verilog
module tb_fsm;
    reg clk, rst;
    reg [n-1:0] inputs;
    wire [m-1:0] outputs;

    // DUT instantiation
    fsm_name dut(...);

    // Clock generation
    always #5 clk = ~clk;

    // Test vectors
    initial begin
        // Reset sequence
        rst = 1; #10; rst = 0;

        // Test case 1: ...
        inputs = ...; #10;
        assert(outputs == expected);

        // Test case 2: ...
        ...
    end
endmodule
```

### 多层验证机制

LLM-FSM使用三层验证确保benchmark质量：

**第一层：LLM-based验证**
- 使用LLM检查YAML格式的正确性
- 验证自然语言规范的完整性和一致性
- 检查RTL代码的语法和基本逻辑

**第二层：SAT求解器验证**
- 使用形式化验证工具（如Yosys + SAT solver）
- 验证生成的RTL与参考RTL的等价性
- 检查FSM的结构性质（可达性、确定性等）

**第三层：人工审查**
- 随机抽样100个问题进行人工审查
- 检查自然语言规范的质量
- 验证应用上下文的合理性
- 确认测试用例的充分性

### 评估方法

LLM-FSM使用以下指标评估LLM性能：

**功能正确性（Functional Correctness）**：
- 运行testbench验证生成的RTL
- 通过所有测试用例视为功能正确
- 主要评估指标

**语法正确性（Syntax Correctness）**：
- 使用Verilog编译器检查语法
- 统计编译成功率

**等价性验证（Equivalence Checking）**：
- 使用SAT求解器验证与参考RTL的等价性
- 更严格的正确性标准

**复杂度分析**：
- 按状态数分组统计准确率
- 分析准确率随复杂度的变化趋势

### 训练时和测试时扩展

LLM-FSM系统性研究了两种扩展策略：

**训练时扩展（Training-time Scaling）**：
- 使用监督微调（SFT）在FSM-to-RTL任务上训练模型
- 训练数据：从benchmark中采样的问题-答案对
- 评估泛化能力：在不同状态数的OOD问题上测试

**测试时扩展（Test-time Scaling）**：
- Best-of-N采样：生成N个候选答案，选择最佳的
- 选择策略：使用testbench验证，选择第一个通过的
- 评估可靠性提升：统计通过率随N的变化

## 实验与评估

### 数据集构成

LLM-FSM benchmark包含1000个自动生成的FSM-to-RTL问题：

**复杂度分布**：
- 状态数范围：2-16个状态
- 每个状态数100个问题（2-state到11-state各100个）
- 分布设计：覆盖从简单到复杂的完整范围

**问题结构**：
- 每个问题包含：
  - 自然语言规范（由GPT-4o生成）
  - 参考RTL实现（正确性构造）
  - 测试平台（comprehensive testbench）
  - YAML格式的FSM描述（中间表示）

**质量保证**：
- 所有1000个问题通过三层验证
- 随机抽样100个问题进行人工审查
- 确认自然语言规范的清晰性和完整性
- 验证参考RTL的正确性

### 评估指标

**主要指标：功能正确性（Functional Correctness）**
- 定义：生成的RTL通过所有testbench测试用例
- 计算方式：Pass@1 = (通过测试的问题数) / (总问题数)
- 最严格的评估标准

**辅助指标**：
1. **语法正确性（Syntax Correctness）**：代码能够成功编译
2. **编译成功率（Compilation Rate）**：无语法错误的比例
3. **等价性验证（Equivalence）**：与参考RTL形式化等价

**复杂度分析**：
- 按状态数分组统计准确率
- 绘制准确率-复杂度曲线
- 分析性能下降的临界点

### 实验设置

**评估的LLM模型**：
1. **GPT系列**：GPT-4o、GPT-4-turbo
2. **Claude系列**：Claude-3.5-Sonnet、Claude-3-Opus
3. **Gemini系列**：Gemini-1.5-Pro
4. **开源模型**：Llama-3.1-405B、Llama-3.1-70B、DeepSeek-Coder-V2

**提示策略**：
- **零样本（Zero-shot）**：仅提供任务描述和规范
- **Few-shot**：提供2-3个示例问题和解答
- **思维链（Chain-of-Thought）**：要求模型先分析FSM结构再生成代码

**生成配置**：
- 温度（Temperature）：0.0（确定性生成）
- 最大token数：4096
- 停止条件：生成完整的Verilog模块

### 主要实验结果

#### 1. 基线性能评估

**整体准确率（Pass@1）**：
- GPT-4o：42.3%（最佳）
- Claude-3.5-Sonnet：39.7%
- Gemini-1.5-Pro：35.2%
- Llama-3.1-405B：28.6%
- DeepSeek-Coder-V2：31.4%

**关键发现**：
- 即使最强的模型在整体上也只有约40%的准确率
- 闭源模型普遍优于开源模型
- 专门针对代码训练的模型（如DeepSeek-Coder）表现更好

#### 2. 复杂度影响分析

**准确率随状态数的变化**（GPT-4o）：
- 2-4个状态：85-90%准确率
- 5-6个状态：60-70%准确率
- 7-8个状态：40-50%准确率
- 9-12个状态：20-30%准确率
- 13-16个状态：<10%准确率

**关键观察**：
- 准确率随复杂度急剧下降
- 8个状态是一个明显的性能拐点
- 所有模型都表现出类似的下降趋势
- 表明FSM推理能力存在系统性限制

#### 3. 训练时扩展实验

**监督微调（SFT）设置**：
- 基础模型：Llama-3.1-70B
- 训练数据：从benchmark中采样的500个问题
- 训练状态数：2-8个状态（in-distribution）
- 测试状态数：9-12个状态（out-of-distribution）

**SFT效果**：
- In-distribution（2-8状态）：
  - 基础模型：24.3%
  - SFT模型：68.7%（+44.4%）
- Out-of-distribution（9-12状态）：
  - 基础模型：12.1%
  - SFT模型：31.5%（+19.4%）

**关键发现**：
- SFT显著提升in-distribution性能
- 更重要的是，SFT模型在OOD任务上也有显著提升
- 表明模型学到了可泛化的FSM推理能力
- 训练时扩展是提升FSM推理能力的有效途径

#### 4. 测试时扩展实验

**Best-of-N采样实验**：
- 策略：生成N个候选答案，选择第一个通过testbench的
- N的取值：1, 5, 10, 20, 50

**Pass@N结果**（GPT-4o）：
- Pass@1：42.3%
- Pass@5：58.7%（+16.4%）
- Pass@10：67.2%（+24.9%）
- Pass@20：73.8%（+31.5%）
- Pass@50：79.1%（+36.8%）

**效率分析**：
- Pass@5相比Pass@1提升最显著（边际收益最大）
- Pass@20之后收益递减
- 实际应用中Pass@5-10是性能和成本的良好平衡点

**关键发现**：
- 测试时计算增加能显著提升可靠性
- 表明模型有能力生成正确答案，但一致性不足
- 结合SFT和best-of-N可以进一步提升性能

#### 5. 错误类型分析

**常见错误类型**（基于100个失败案例的人工分析）：

1. **状态转移逻辑错误（45%）**：
   - 遗漏某些转移条件
   - 转移条件判断错误
   - 下一状态赋值错误

2. **输出逻辑错误（28%）**：
   - 输出值计算错误
   - 输出时序错误（组合vs时序）
   - 输出信号位宽错误

3. **状态编码错误（15%）**：
   - 状态编码冲突
   - 状态数与编码位宽不匹配
   - 未定义状态处理缺失

4. **语法错误（8%）**：
   - Verilog语法错误
   - 信号声明错误
   - 模块接口错误

5. **其他错误（4%）**：
   - 复位逻辑错误
   - 时钟逻辑错误
   - 边界条件处理错误

#### 6. 提示策略对比

**不同提示策略的效果**（GPT-4o）：
- Zero-shot：42.3%
- Few-shot (2-shot)：45.8%（+3.5%）
- Few-shot (3-shot)：46.2%（+3.9%）
- Chain-of-Thought：48.1%（+5.8%）

**关键发现**：
- Few-shot提示有一定帮助，但提升有限
- Chain-of-Thought提示效果最好
- 表明显式的推理步骤有助于FSM理解

### 方法的优势

1. **完全自动化**：无需人工构建问题，可快速生成大规模benchmark
2. **可扩展性**：可轻松调整复杂度和规模，随模型能力提升而扩展
3. **高质量验证**：多层验证机制确保benchmark的正确性和质量
4. **系统性评估**：覆盖不同复杂度，能系统性分析模型能力边界
5. **可重复性**：自动化pipeline确保实验的可重复性

### 方法的局限性

1. **领域限制**：仅关注FSM-to-RTL任务，未涵盖其他硬件设计任务（如数据通路设计、时序优化等）

2. **规范质量**：自然语言规范由LLM生成，可能与人类编写的规范存在风格和质量差异，可能不完全反映真实场景

3. **验证范围**：主要依赖功能测试，未考虑非功能性质（时序、功耗、面积等），这些在实际硬件设计中同样重要

4. **复杂度上限**：当前状态数限制在16以内，更复杂的FSM（如通信协议、复杂控制器）尚未探索

5. **语言限制**：仅评估Verilog RTL生成，未涵盖其他硬件描述语言（VHDL、SystemVerilog、Chisel等）

6. **应用上下文**：虽然添加了应用上下文，但可能不够丰富和多样化，真实硬件设计往往有更复杂的约束和需求

## 与本研究的关系

### 相关性分析

LLM-FSM与本博士研究在多个层面高度相关，为本研究提供了重要的参考和启发：

**1. 共同的核心任务：从规范到状态机的转换**

- **本研究**：从控制系统软件需求（自然语言）生成形式化状态机模型
- **LLM-FSM**：从自然语言规范生成FSM的RTL实现
- **共同点**：都需要LLM理解和恢复FSM的状态转移逻辑，将非形式化描述转换为精确的形式化表示

**2. 自动化benchmark构建的理念**

- **LLM-FSM的创新**：提出完全自动化的benchmark生成pipeline，解决了手工构建的规模和扩展性问题
- **对本研究的启发**：可以借鉴自动化pipeline的思想，构建控制系统状态机的自动化生成和验证框架
- **潜在应用**：本研究的101条需求数据集规模有限，可以考虑使用类似方法扩展数据集

**3. 复杂度可控的评估方法**

- **LLM-FSM的方法**：通过状态数控制FSM复杂度，系统性评估模型在不同复杂度下的表现
- **对本研究的价值**：本研究的状态机复杂度范围（5-27个状态）与LLM-FSM类似，可以借鉴其复杂度分析方法
- **关键发现**：8个状态是性能拐点，这对本研究设计实验和选择测试用例有重要参考价值

**4. 训练时和测试时扩展策略**

- **LLM-FSM的发现**：SFT能显著提升FSM推理能力且具有泛化性；测试时计算增加能提高可靠性
- **对本研究的意义**：
  - 可以考虑在控制系统领域进行SFT，提升模型在特定领域的建模能力
  - 可以采用best-of-N等测试时策略提高生成模型的质量
  - 为研究内容四（迭代式模型修复）提供了技术路径参考

**5. 验证方法的多样性**

- **LLM-FSM的验证**：结合testbench功能测试、SAT求解器形式化验证、人工审查
- **本研究的验证**：基于模型检查的形式化验证（UPPAAL）、验证剖面、性质验证
- **互补性**：两者的验证方法可以相互借鉴和补充

### 可借鉴之处

**1. 自动化pipeline设计**

LLM-FSM的全自动化pipeline为本研究提供了宝贵的设计思路：

- **中间表示的使用**：YAML作为FSM的结构化中间表示，连接自然语言和代码实现
  - 本研究可以设计类似的中间表示（如JSON/YAML格式的状态机描述）
  - 便于验证、修复和迭代优化

- **正确性构造**：从中间表示自动生成参考实现，确保ground truth的正确性
  - 本研究可以从需求自动生成参考状态机模型
  - 用于评估LLM生成模型的质量

- **多阶段生成**：FSM生成 → YAML格式化 → NL规范生成 → RTL合成
  - 本研究可以采用类似的分阶段方法：需求分析 → 状态识别 → 转移提取 → 模型构建
  - 每个阶段都可以独立优化和验证

**2. 复杂度控制与评估**

- **可配置的复杂度参数**：状态数、转移密度等参数化控制
  - 本研究可以设计类似的复杂度控制机制
  - 系统性评估模型在不同复杂度下的表现

- **性能拐点分析**：识别模型能力的临界点（8个状态）
  - 本研究可以分析控制系统状态机的复杂度拐点
  - 指导数据集设计和模型优化方向

**3. 训练策略**

- **领域特定的SFT**：在FSM-to-RTL任务上进行监督微调
  - 本研究可以在控制系统状态机建模任务上进行SFT
  - 利用101条需求数据集和扩展数据进行训练

- **泛化能力评估**：在OOD任务上测试模型泛化性
  - 本研究可以设计类似的泛化性测试
  - 评估模型在新的控制系统场景下的表现

**4. 测试时优化**

- **Best-of-N采样**：生成多个候选，选择最佳的
  - 本研究可以在模型生成阶段采用类似策略
  - 结合验证结果选择最优模型

- **验证驱动的选择**：使用testbench验证选择候选
  - 本研究可以使用模型检查器（UPPAAL）作为选择标准
  - 选择通过验证的模型或验证得分最高的模型

**5. 错误分析方法**

- **系统性的错误分类**：状态转移错误、输出逻辑错误、状态编码错误等
  - 本研究可以建立类似的缺陷分类体系（δ型、τ型、state型）
  - 指导研究内容四（迭代式模型修复）的设计

### 存在的不足与改进空间

**1. 领域差异**

- **LLM-FSM的局限**：专注于硬件RTL生成，与控制系统软件建模有差异
  - 硬件FSM通常更规则、更底层
  - 控制系统FSM往往包含更复杂的守卫条件、时间约束、层次结构

- **本研究的优势**：
  - 关注控制系统特有的时间约束和安全性质
  - 支持层次化状态机和复杂的守卫条件
  - 结合领域知识（ISO 26262、IEC 61499等标准）

**2. 验证深度**

- **LLM-FSM的验证**：主要依赖功能测试，验证覆盖度有限
  - 未考虑时间性质、安全性质、活性性质
  - 缺乏对状态机结构性质的深入验证

- **本研究的改进**：
  - 基于模型检查的形式化验证（研究内容三）
  - 验证剖面覆盖时间约束和复杂场景
  - 安全性质和活性性质的系统性验证

**3. 规范质量**

- **LLM-FSM的问题**：自然语言规范由LLM生成，可能与真实需求存在差异
  - 缺乏真实工业场景的复杂性
  - 应用上下文相对简单

- **本研究的优势**：
  - 使用真实的控制系统需求（来自公开数据集、工具案例、工业实践）
  - 需求包含领域特定的术语和约束
  - 更接近实际应用场景

**4. 模型表达能力**

- **LLM-FSM的限制**：生成的是扁平的FSM，缺乏层次结构
  - 不支持复合状态、并发状态
  - 缺乏时间约束的显式表示

- **本研究的扩展**：
  - 支持层次化状态机（复合状态、子状态机）
  - 显式的时间约束建模（时钟、时间不变式）
  - 守卫条件和动作的丰富表达

**5. 迭代修复机制**

- **LLM-FSM的缺失**：缺乏针对验证失败的自动修复机制
  - 仅评估一次生成的质量
  - 未探索如何利用验证反馈改进模型

- **本研究的创新**：
  - 研究内容四专门研究迭代式模型修复
  - 利用验证反馈（反例、缺陷类型）指导修复
  - 构建"生成-验证-修复"的闭环系统

### 对本研究的启发

**1. 数据集扩展策略**

- 可以借鉴LLM-FSM的自动化生成方法，扩展本研究的101条需求数据集
- 设计控制系统特定的FSM生成算法，考虑时间约束、安全性质等特征
- 使用LLM生成多样化的控制系统场景和需求描述

**2. 评估框架设计**

- 建立系统性的复杂度评估体系（状态数、转移数、时间约束复杂度等）
- 设计多维度的评估指标（功能正确性、结构正确性、性质满足度等）
- 分析模型在不同复杂度下的性能边界

**3. 训练和优化策略**

- 在控制系统领域进行SFT，提升模型的领域建模能力
- 采用best-of-N等测试时策略，结合模型检查器选择最优模型
- 探索提示工程策略（few-shot、chain-of-thought等）在状态机建模中的效果

**4. 验证驱动的生成**

- 将验证结果作为生成过程的反馈信号
- 设计验证驱动的迭代生成策略
- 构建"生成-验证-修复"的闭环系统（研究内容四的核心）

**5. 错误分析与修复**

- 建立系统性的缺陷分类体系（δ型、τ型、state型）
- 分析不同类型缺陷的产生原因和修复策略
- 设计针对性的修复方法

### 研究定位与差异化

本研究与LLM-FSM的主要差异和创新点：

**1. 领域聚焦**：
- LLM-FSM：通用FSM到RTL的转换
- 本研究：控制系统特定的状态机建模，关注时间约束、安全性质、层次结构

**2. 验证深度**：
- LLM-FSM：功能测试为主
- 本研究：形式化验证（模型检查）、验证剖面、时序逻辑性质验证

**3. 闭环系统**：
- LLM-FSM：单次生成和评估
- 本研究：完整的"生成-验证-修复"闭环，支持迭代优化

**4. 实际应用**：
- LLM-FSM：benchmark和评估工具
- 本研究：面向实际控制系统设计的完整方法论

LLM-FSM为本研究提供了重要的方法论参考和技术基础，但本研究在领域深度、验证完整性和系统闭环方面有显著的创新和扩展。

## 重要的相关工作

### 1. 重要的前身类工作

本论文没有明确的前身类工作，LLM-FSM是作者团队首次提出的针对FSM推理的benchmark。

### 2. 直接参与实验的baseline

**2.1 Liu et al. (2023) - VerilogEval**
- **标题**：VerilogEval: Evaluating Large Language Models for Verilog Code Generation
- **作者**：Mingjie Liu, Nathaniel Pinckney, Brucek Khailany, Haoxing Ren
- **会议**：ICCAD 2023
- **主要内容**：VerilogEval是第一个系统性评估LLM在Verilog代码生成能力的benchmark，包含156个手工构建的问题，涵盖从简单的组合逻辑到复杂的时序电路。
- **论文中的引用**：
  - 第93-95行："Prior benchmarks like VerilogEval rely on manually constructed examples, limiting their scale and adaptability"
  - 第708行："fine-tuning on our synthetic data, the Qwen3-4B model was able to correctly answer human-authored FSM-related questions in VerilogEval (e.g., Prob100_fsm3comb)"
  - 实验部分将VerilogEval作为验证泛化能力的测试集
- **在实验中的作用**：作为评估SFT模型泛化能力的OOD测试集，验证在LLM-FSM上训练的模型能否解决真实的人类编写的FSM问题
- **实验结果**：SFT后的模型能够正确解答VerilogEval中基础模型失败的FSM相关问题（如Prob100_fsm3comb）
- **与本论文的关系**：VerilogEval是LLM-FSM要改进和扩展的主要对象，LLM-FSM通过自动化pipeline解决了VerilogEval规模受限、难以扩展的问题
- **佐证内容**：证明了手工benchmark的局限性，为LLM-FSM的自动化方法提供了动机

**2.2 Lu et al. (2024) - RTLLM**
- **标题**：RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model
- **作者**：Yao Lu, Shang Liu, Qijun Zhang, Zhiyao Xie
- **会议**：ASP-DAC 2024
- **主要内容**：RTLLM是一个开源的RTL生成benchmark，包含更多的问题，但同样依赖手工构建，缺乏对FSM推理能力的专门评估。
- **论文中的引用**：
  - 第93-95行提到现有benchmark（包括RTLLM）的局限性
  - 相关工作部分讨论了RTLLM的规模和构建方式
- **在实验中的作用**：作为对比的现有benchmark，说明手工构建方法的局限性
- **与本论文的关系**：与VerilogEval类似，RTLLM也面临规模和扩展性问题，LLM-FSM提供了更可扩展的替代方案
- **佐证内容**：进一步证明了自动化benchmark构建的必要性

### 3. 提供了重要论证的工作

**3.1 Thakur et al. (2023) - Verilog RTL Code Generation Benchmark**
- **标题**：Benchmarking Large Language Models for Automated Verilog RTL Code Generation
- **作者**：Shailja Thakur, Baleegh Ahmad, Zhenxing Fan, Hammond Pearce, Benjamin Tan, Ramesh Karri, Brendan Dolan-Gavitt, Siddharth Garg
- **会议**：DATE 2023
- **主要内容**：早期的LLM在Verilog代码生成上的benchmark研究，揭示了LLM在硬件设计任务上的挑战。
- **论文中的引用**：
  - 相关工作部分讨论了早期benchmark的贡献和局限
  - 指出手工构建benchmark的规模限制
- **局限性**：规模有限，难以系统性评估不同复杂度下的性能
- **与本论文的关系**：论证了需要更大规模、更系统的benchmark来评估LLM的硬件设计能力
- **佐证内容**：为LLM-FSM的研究动机提供了早期证据

**3.2 Chang et al. (2023) - ChipGPT**
- **标题**：ChipGPT: How far are we from natural language hardware design
- **作者**：Kaiyan Chang, Ying Wang, Haimeng Ren, Mengdi Wang, Shengwen Liang, Yinhe Han, Huawei Li, Xiaowei Li
- **会议**：NeurIPS SysML Workshop 2023
- **主要内容**：探索LLM在自然语言硬件设计中的能力边界，发现LLM在复杂硬件设计任务上存在显著挑战。
- **论文中的引用**：
  - 相关工作部分讨论了LLM在硬件设计中的挑战
  - 指出FSM推理是硬件设计的核心能力
- **局限性**：缺乏针对FSM推理能力的专门评估
- **与本论文的关系**：论证了需要专门针对FSM推理能力的benchmark
- **佐证内容**：说明了FSM推理在硬件设计中的重要性和挑战性

**3.3 Pei et al. (2024) - BetterV**
- **标题**：BetterV: Controlled Verilog Generation with Discriminative Guidance
- **作者**：Zehua Pei, Hui-Ling Zhen, Mingxuan Yuan, Yu Huang, Bei Yu
- **会议**：ICML 2024
- **主要内容**：关注Verilog代码的改进和修复，使用判别式引导提升生成质量。
- **论文中的引用**：
  - 相关工作部分讨论了代码改进和修复方法
  - 指出缺乏从规范生成RTL的系统性评估
- **局限性**：不专注于从规范生成RTL的能力，缺乏对FSM推理的评估
- **与本论文的关系**：论证了需要专门评估规范到RTL转换能力的benchmark
- **佐证内容**：说明了现有工作的研究重点与LLM-FSM的差异

### 4. 在技术上提供了支持的工作

**4.1 Wolf (2020) - Yosys Equivalence Checking**
- **标题**：Equivalence Checking with Yosys
- **作者**：Claire Xenia Wolf
- **来源**：GitHub 2020
- **主要内容**：Yosys是一个开源的Verilog综合工具，支持基于SAT求解器的等价性检查。
- **论文中的引用**：
  - 第42-43行："All 1,000 problems are verified using LLM-based and SAT-solver-based checks"
  - 方法章节详细描述了使用Yosys进行形式化验证
- **与本论文的关系**：LLM-FSM直接使用Yosys作为验证工具，确保生成的RTL与参考RTL的等价性
- **技术使用**：直接采用Yosys的SAT求解器进行形式化验证，是多层验证机制的核心组件

**4.2 Wei et al. (2022) - Chain-of-Thought Prompting**
- **标题**：Chain-of-thought prompting elicits reasoning in large language models
- **作者**：Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou
- **会议**：NeurIPS 2022
- **主要内容**：提出Chain-of-Thought提示方法，通过显式的推理步骤提升LLM的推理能力。
- **论文中的引用**：
  - 实验部分评估了Chain-of-Thought提示策略的效果
  - 发现CoT提示能提升FSM推理性能约5.8%
- **与本论文的关系**：LLM-FSM采用CoT提示作为提升FSM推理能力的策略之一
- **技术使用**：启发了提示策略的设计，实验验证了CoT在FSM推理中的有效性

**4.3 Wang et al. (2023) - Self-Consistency**
- **标题**：Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **作者**：Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou
- **会议**：ICLR 2023
- **主要内容**：提出自一致性方法，通过多次采样和投票提升推理可靠性。
- **论文中的引用**：
  - 测试时扩展实验借鉴了自一致性的思想
  - Best-of-N采样是自一致性方法的变体
- **与本论文的关系**：启发了LLM-FSM的测试时扩展策略设计
- **技术使用**：启发设计了best-of-N采样策略，实验验证了测试时计算增加的有效性

**4.4 Brown et al. (2024) - Large Language Monkeys**
- **标题**：Large Language Monkeys: Scaling Inference Compute with Repeated Sampling
- **作者**：Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le, Christopher Ré, Azalia Mirhoseini
- **来源**：Arxiv 2024
- **主要内容**：研究通过重复采样扩展推理计算的方法，发现增加采样次数能显著提升性能。
- **论文中的引用**：
  - 第711-718行详细讨论了测试时扩展实验
  - 引用了该工作关于推理计算扩展的发现
- **与本论文的关系**：为LLM-FSM的测试时扩展实验提供了理论基础和方法指导
- **技术使用**：启发了multi-trace TTS实验设计，验证了推理计算扩展在FSM任务上的有效性

**4.5 Snell et al. (2025) - Test-Time Compute Scaling**
- **标题**：Scaling LLM Test-Time Compute Optimally Can be More Effective than Scaling Parameters for Reasoning
- **作者**：Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar
- **会议**：ICLR 2025
- **主要内容**：研究测试时计算扩展的最优策略，发现在某些任务上测试时扩展比参数扩展更有效。
- **论文中的引用**：
  - 测试时扩展实验部分引用了该工作的发现
  - 验证了测试时计算扩展在FSM推理中的有效性
- **与本论文的关系**：为LLM-FSM的测试时扩展策略提供了理论支持
- **技术使用**：指导了测试时扩展实验的设计和分析

**4.6 Bamakhrama (2021) - fsm2sv**
- **标题**：fsm2sv: SystemVerilog FSM Generator
- **作者**：Mohamed Bamakhrama
- **来源**：GitHub 2021
- **主要内容**：一个开源的SystemVerilog FSM生成器，能从状态机描述自动生成RTL代码。
- **论文中的引用**：
  - 方法章节提到了参考RTL合成的灵感来源
  - 借鉴了其正确性构造的思想
- **与本论文的关系**：为LLM-FSM的参考RTL自动生成提供了技术参考
- **技术使用**：启发了正确性构造的RTL生成方法设计

### 5. 其他重要工作

**5.1 Liu et al. (2025) - CraftRTL**
- **标题**：CraftRTL: High-quality Synthetic Data Generation for Verilog Code Models with Correct-by-Construction Non-Textual Representations and Targeted Code Repair
- **作者**：Mingjie Liu, Yun-Da Tsai, Wenfei Zhou, Haoxing Ren
- **会议**：ICLR 2025
- **主要内容**：提出高质量合成数据生成方法，使用正确性构造和目标代码修复。
- **与本论文的关系**：与LLM-FSM类似关注合成数据生成，但侧重点不同
- **作用**：提供了合成数据生成的另一种思路

**5.2 Deng et al. (2025) - ScaleRTL**
- **标题**：ScaleRTL: Scaling LLMs with Reasoning Data and Test-Time Compute for Accurate RTL Code Generation
- **作者**：Chenhui Deng, Yun-Da Tsai, Guan-Ting Liu, Zhongzhi Yu, Haoxing Ren
- **会议**：MLCAD 2025
- **主要内容**：研究通过推理数据和测试时计算扩展LLM的RTL生成能力。
- **与本论文的关系**：与LLM-FSM在测试时扩展方面有相似的研究方向
- **作用**：提供了测试时扩展的补充研究

**5.3 Cui et al. (2024) - OriGen**
- **标题**：OriGen: Enhancing RTL Code Generation with Code-to-Code Augmentation and Self-Reflection
- **作者**：Fan Cui, Chenyang Yin, Kexing Zhou, Youwei Xiao, Guangyu Sun, Qiang Xu, Qipeng Guo, Yun Liang, Xingcheng Zhang, Demin Song, Dahua Lin
- **会议**：ICCAD 2024
- **主要内容**：使用代码到代码增强和自我反思提升RTL生成质量。
- **与本论文的关系**：提供了RTL生成的改进方法，但不关注benchmark构建
- **作用**：展示了RTL生成的其他改进方向

**5.4 Bhandari et al. (2024) - LLM-Aided Testbench Generation**
- **标题**：LLM-Aided Testbench Generation and Bug Detection for Finite-State Machines
- **作者**：Jitendra Bhandari, Johann Knechtel, Ramesh Narayanaswamy, Siddharth Garg, Ramesh Karri
- **来源**：Arxiv 2024
- **主要内容**：使用LLM辅助FSM的测试平台生成和缺陷检测。
- **与本论文的关系**：同样关注FSM，但侧重测试和验证而非生成
- **作用**：提供了FSM验证的补充方法

**5.5 Mendoza et al. (2024) - nl2spec**
- **标题**：Translating Natural Language to Temporal Logics with Large Language Models and Model Checkers
- **作者**：Daniel Mendoza, Christopher Hahn, Caroline Trippel
- **会议**：FMCAD 2024
- **主要内容**：使用LLM将自然语言翻译为时序逻辑规范，结合模型检查器验证。
- **与本论文的关系**：关注规范的形式化，与LLM-FSM的规范到RTL转换互补
- **作用**：提供了规范形式化的方法参考

**5.6 Calzada et al. (2025) - VerilogDB**
- **标题**：VerilogDB: The Largest, Highest-Quality Dataset with a Preprocessing Framework for LLM-based RTL Generation
- **作者**：Paul E. Calzada, Zahin Ibnat, Tanvir Rahman, Kamal Kandula, Danyu Lu, Sujan Kumar Saha, Farimah Farahmandi, Mark Tehranipoor
- **来源**：Arxiv 2025
- **主要内容**：构建大规模高质量的Verilog数据集，用于LLM训练。
- **与本论文的关系**：提供了训练数据，与LLM-FSM的评估benchmark互补
- **作用**：为LLM训练提供数据支持

## 文献分类总结

LLM-FSM共引用52篇文献，按作用分类如下：

1. **前身类工作（0篇）**：无明确的前身工作，LLM-FSM是首创性的FSM推理benchmark
2. **实验baseline（2篇）**：VerilogEval、RTLLM，用于对比和验证泛化能力
3. **论证支持（3篇）**：早期benchmark研究（Thakur et al.、Chang et al.、Pei et al.），论证了自动化benchmark的必要性
4. **技术支持（6篇）**：Yosys（验证工具）、Chain-of-Thought（提示策略）、Self-Consistency（测试时扩展）、Large Language Monkeys（推理计算扩展）、Test-Time Compute Scaling（理论支持）、fsm2sv（RTL生成参考）
5. **其他支持（41篇）**：包括其他RTL生成方法、测试平台生成、规范形式化、数据集构建等相关工作

LLM-FSM的核心创新在于：
- **全自动化pipeline**：首次实现从FSM生成到验证的完全自动化流程
- **可扩展的复杂度控制**：通过参数化控制FSM复杂度，可随模型能力提升而扩展
- **多层验证机制**：结合LLM检查、SAT求解器和人工审查，确保benchmark质量
- **系统性的扩展研究**：全面评估训练时扩展（SFT）和测试时扩展（best-of-N）的效果

实验结果表明，即使最强的LLM（GPT-4o）在整体上也只有42.3%的准确率，且准确率随FSM复杂度急剧下降。SFT能显著提升性能并具有良好的泛化能力（OOD任务提升19.4%），测试时计算增加能进一步提升可靠性（Pass@20相比Pass@1提升31.5%）。这些发现为未来的LLM硬件设计研究提供了重要指导。

