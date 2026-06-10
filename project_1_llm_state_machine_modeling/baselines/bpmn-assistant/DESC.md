# BPMN Assistant：基于 LLM 的业务流程建模方法 / BPMN Assistant: An LLM-Based Approach to Business Process Modeling

## 基本信息

- **标题**：BPMN Assistant: An LLM-Based Approach to Business Process Modeling
- **中文标题**：BPMN Assistant：基于 LLM 的业务流程建模方法
- **作者**：Josip Tomo Licardo、Nikola Tanković、Darko Etinger
- **单位**：Juraj Dobrila University of Pula, Faculty of Informatics
- **发表**：arXiv:2509.24592v2，2026-01-22 修订版；原稿日期 2026-01-23
- **DOI**：10.48550/arXiv.2509.24592
- **链接**：[arXiv](https://arxiv.org/abs/2509.24592)；[PDF](https://arxiv.org/pdf/2509.24592)；[implementation](https://github.com/jtlicardo/bpmn-assistant)；[GED tool](https://github.com/jtlicardo/bpmn-ged)

**代码/仓库获取方式**：
- 原文明确说明 BPMN Assistant implementation 公开在 `https://github.com/jtlicardo/bpmn-assistant`；本次建档时 GitHub 页面可访问。
- 原文 footnote 还给出 evaluation pipeline / GED implementation：`https://github.com/jtlicardo/bpmn-ged`；本次页面可访问。

**数据集获取方式**：
- 原文构造了 60 个 process descriptions（20 个 business domains，每个 3 条）和 40 个 manual editing requests；描述由 OpenAI gpt-4.1 固定 prompt 生成，再人工筛除歧义/退化样例，ground-truth BPMN 由 BPMN-trained annotators 创建并由作者审校。
- 原文没有明确给出该 evaluation dataset 的单独公开下载链接；是否包含在 GitHub 仓库中需后续人工核验。

## 简报

本文解决的问题是：LLM 直接生成/修改 BPMN XML 冗长、慢且易出现语法错误，尤其在复杂 incremental editing 中不稳定。作者提出 BPMN Assistant，用 JSON-based intermediate representation 和 atomic editing functions 把自然语言创建/编辑请求转成可验证的结构化操作，再转换为 BPMN XML 并自动布局。

- **输入**：用户自然语言建模请求或自然语言编辑指令；编辑任务还输入当前 BPMN intermediate representation。
- **方法**：LLM 输出结构化 JSON process 或 function calls；Python backend 验证 JSON/结构约束并转换为 BPMN XML；layout server 添加 BPMNDI；Vue frontend 展示可交互 BPMN canvas。
- **输出**：BPMN 2.0 XML diagram / renderable BPMN canvas，以及对现有 BPMN 的目标修改结果。

```text
输入层：自然语言生成/编辑请求 + 当前流程状态（编辑时）
  -> 方法层：LLM -> JSON IR / atomic function calls -> Python validation -> BPMN XML -> layout server
  -> 输出层：可视化 BPMN diagram / edited BPMN model
```

实验比较 JSON-based approach 与 direct XML generation/editing。生成任务中 JSON 平均 similarity 0.72、XML 0.70，差异小但 JSON failures 更少；编辑任务中 JSON 明显更好，例如 DeepSeek V3 JSON 成功率 50%、XML 仅 8%。JSON editing 平均 latency 20.35s，相比 XML 35.63s 降低约 43%，output tokens 607 vs 2630，减少超过 75%。本文是 BPMN interactive modeling 强近邻，不是 STM direct baseline。

**可比字段快照**：

- **输入**：自然语言 process generation/editing instructions；editing 时还含当前 BPMN/JSON 状态。
- **输出**：BPMN diagrams / edited BPMN XML。
- **输出模型类型**：BPMN 2.0 process model；非 STM 族。
- **使用的 LLM**：GPT-5.1、GPT-5 mini、GPT-4o、Claude 4.5 Sonnet、Claude 3.5 Sonnet、Gemini 2.0 Flash、Llama 3.3 70B Instruct、Qwen 2.5 72B Instruct、DeepSeek V3。
- **主要方法**：hierarchical JSON IR + atomic process editing functions + validation/self-correction + XML conversion/layout。
- **需求词工程**：中；通过 schema、function calling 和 structured prompts 限制输出。
- **运行仿真/验证**：无仿真；有 syntax/reference/structural validation 和 GED/RGED structural evaluation。
- **形式化验证**：无 Petri-net semantics、conformance checking 或 model checking，原文明确将其列为非目标。

## 研究问题与动机

### 问题背景

BPMN 虽是业务流程建模标准，但非专家创建/编辑流程图存在认知和技术门槛。组织知识常散落在自然语言文档和专家经验中，而业务流程又需要频繁更新。LLM 能理解自然语言，但直接输出 BPMN XML 在格式和修改稳定性上有明显问题。

### 核心问题

论文关注三个 RQ：JSON intermediate representation 相比 XML 在生成可靠性和编辑成功率上如何；function-based editing 是否能让开放权重模型完成复杂建模任务；输入上下文增加但输出复杂度降低对 latency 和效率的影响如何。

### 研究动机

作者认为 BPMN 模型应被视为 mutable process structures，通过 well-defined operations 精细修改，而不是每次 conversational refinement 都整体 regenerate。将 process semantics、editing logic 与 concrete BPMN serialization 分离，是提高交互式建模可靠性的关键。

### 研究意义

对 Project 1 的启发是：状态机编辑/修复也可用中间 JSON/DSL 表示和 atomic operations，而不是让 LLM 每轮输出整张状态机。这样可减少 reference hallucination、局部修改漂移和格式错误。

### 现有方法的局限性

BPMN-Chatbot 和 ProMoAI 等工具虽然使用中间表示或代码，但 refinement 往往仍像 conversational regeneration。本文强调 dedicated intermediate layer 和 function calling，用 targeted deterministic updates 支持 minor edits。

### 研究目标

构建 BPMN Assistant，验证 JSON IR 在 generation/editing accuracy、failure rate、token/latency efficiency 方面的收益。

## 核心方法

### 方法概述

系统由三部分组成：

1. **Python backend**：处理用户请求、调用 LLM、验证 JSON、转换 BPMN XML。
2. **BPMN layout server**：基于 bpmn-auto-layout 为 XML 添加 DI 坐标。
3. **Vue.js frontend**：左侧 chat、右侧 bpmn.io canvas，支持下载和交互。

### JSON intermediate representation

IR 以 `process` array 表达顺序流，支持多种 task types、start/end/intermediate events、timer/message event definitions、exclusive/inclusive/parallel gateways。gateway 通过 `branches` 表达分支，`has_join` 表示是否合流，`next` 支持 loop-back，inclusive gateway 可用 `is_default` 标识默认路径。

### Atomic editing functions

支持以下操作：

- `delete_element`
- `redirect_branch`
- `add_element`
- `move_element`
- `update_element`

LLM 解析自然语言编辑请求，选择函数和参数。系统执行前检查结构完整性，删除/添加/移动时自动保持 process continuity。

### Validation and self-correction

Python validator 在 XML conversion 前拦截 LLM 输出，检查 element IDs 唯一性、flow connectivity、gateway branch hierarchy、exactly one start event 等。违反时把 validation error 反馈给 LLM 进行 self-correction。

### 评估方法

- generation accuracy：60 个描述，比较 JSON vs XML 的 GED/RGED similarity 和 failures。
- editing capability：40 个 modification requests，先自动检查语法和 referential integrity，再由专家做 binary semantic correctness check。
- efficiency：记录 API latency、input tokens、output tokens。

## 实验与评估

### 数据集

- 60 个 process descriptions，20 个 business domains，每域 3 条，7-8 activities，显式避免 BPMN terminology。
- ground truth BPMN 由多个 BPMN-trained annotators 创建，作者审校。
- 40 个 editing requests 覆盖不同 process elements。

### 主要实验结果

#### Generation

JSON 平均 similarity 0.72，XML 0.70；JSON total failures 2，XML 11。生成 latency JSON 13.42s vs XML 24.82s；JSON input tokens 2678 vs XML 474，但 output tokens 688 vs 1832。

#### Editing

编辑成功率 JSON 普遍高于 XML：

- GPT-5.1：0.83 vs 0.75。
- Claude 4.5 Sonnet：0.85 vs 0.85。
- GPT-4o：0.55 vs 0.30。
- DeepSeek V3：0.50 vs 0.08。
- Qwen 2.5 72B：0.38 vs 0.25。

编辑 latency JSON 20.35s vs XML 35.63s，output tokens 607.92 vs 2630.44。

### 方法优势

- JSON IR 显著降低直接 XML 编辑的脆弱性。
- Atomic functions 支持局部修改，避免全模型再生成。
- 对 open-weight models 特别有帮助，有利于 privacy-sensitive enterprise deployment。
- 前后端工具链和实现公开。

### 方法的局限性

- 当前不支持 collaboration diagrams（pools/lanes）和 data objects。
- 缺少 semantic evaluation、Petri nets、process mining conformance、simulation studies 和 comprehensive usability studies。
- 性能强依赖底层 LLM。
- 清晰自然语言输入仍是前提，含糊/多语言/领域术语可能造成问题。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | LLM 用于创建和编辑 BPMN 模型。 |
| NL输入 | 🟢 | 输入为自然语言生成/编辑请求。 |
| LLM方法 | 🟢 | LLM 输出 JSON IR 或 editing functions，是核心组件。 |
| STM族输出 | 🟡 | BPMN 是行为/process 强近邻，但不是 STM-family。 |

不能评为 exact STM direct baseline：输出是 BPMN diagrams，且本文重点是 interactive BPMN editing 而非从需求生成状态机。

### 研究定位与差异化

Project 1 的修复/迭代阶段可借鉴本文，而生成对象不同。BPMN Assistant 证明中间表示和 atomic operations 对模型编辑可靠性有实证价值；这与 Project 4 iterative model repair 也高度相关。

### 可借鉴之处

- **atomic STM edit functions**：如 add_state、delete_transition、update_guard、redirect_transition、rename_event 等。
- **validator-before-renderer**：先验证 IR，再转换为最终模型。
- **局部编辑优先**：修复状态机时避免整图重生成带来的 drift。
- **token/latency trade-off**：把完整当前模型作为输入，限制输出为小 diff/function calls。

### 存在的不足与改进空间

- 未验证业务语义 correctness，Project 1 不能只采用 GED/RGED。
- 不支持多视角 BPMN，功能范围有限。
- dataset 是否公开待核验。
- 不是控制系统场景。

### 对本研究的启发

Project 1/4 可设计 pyfcstm-aware JSON IR 与操作集，让 LLM 输出 repair function calls，并用 parse/semantic/design/sim diagnostics 校验。这样可以把“模型修复”从自然语言重写变成可审计的 edit trace。

## 重要的相关工作

### 1. 重要的前身类工作

- Friedrich text-to-BPMN、Leopold process-to-text、Bellan process extraction survey：构成 NLP/BPMN 自动化背景。

### 2. 直接参与实验的baseline

- Direct XML generation/editing：本文核心对照。
- GPT-5.1、Claude 4.5 Sonnet、DeepSeek V3 等多个 LLM：用于 cross-model comparison。

### 3. 提供了重要论证的工作

- BPMN-Chatbot、ProMoAI、BPMNGen：交互式/LLM BPMN 工具对比。
- Kourani process modeling benchmark：相关 LLM process modeling 基础。

### 4. 在技术上提供了支持的工作

- bpmn-auto-layout、bpmn.io/bpmn-js、NetworkX、GED/RGED literature。

### 5. 其他重要工作

- BPMN quality metrics、process model similarity、process mining 文献用于说明评价维度，但本文未接入语义/仿真评价。

## 文献分类总结

本文是 LLM interactive BPMN generation/editing 强近邻。它满足 LLM4Modeling、NL输入、LLM方法，但输出为 BPMN，因此 `STM族输出=🟡`，总体 `BASELINE评估=🟠`。其最大价值是为 Project 1/4 提供 intermediate representation + atomic edit + validation loop 的工程方法参照。
