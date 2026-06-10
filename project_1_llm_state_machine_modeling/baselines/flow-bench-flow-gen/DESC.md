# FLOW-BENCH 与 FLOW-GEN：面向企业工作流会话式生成 / FLOW-BENCH: Towards Conversational Generation of Enterprise Workflows

## 基本信息

- **标题**：FLOW-BENCH: Towards Conversational Generation of Enterprise Workflows
- **中文标题**：FLOW-BENCH：面向企业工作流会话式生成
- **作者**：Evelyn Duesterwald、Siyu Huo、Vatche Isahagian、K. R. Jayaram、Ritesh Kumar、Vinod Muthusamy、Punleuk Oum、Debashish Saha、Gegi Thomas、Praveen Venkateswaran
- **单位**：IBM Research AI
- **发表**：arXiv:2505.11646，2025-05-16 预印本
- **DOI**：10.48550/arXiv.2505.11646
- **链接**：[arXiv](https://arxiv.org/abs/2505.11646)；[PDF](https://arxiv.org/pdf/2505.11646)；[FLOW-BENCH GitHub](https://github.com/IBM/Flow-Bench)

**代码/仓库获取方式**：
- 原文脚注说明 FLOW-BENCH dataset 可在 `https://github.com/IBM/Flow-Bench` 获取；本次建档时该 GitHub 页面可访问。
- 原文主要声明公开 dataset；是否包含完整 FLOW-GEN 实现代码与生产部署组件，需要后续人工核验仓库内容，不能仅凭论文断言完整开源。

**数据集获取方式**：
- FLOW-BENCH 由 GitHub 仓库提供，包含自然语言 instructions、Python IR、BPMN 表示、API catalog/description 等。
- 数据集规模为 101 个 incremental build step tests；每个 test 包含 Prior Sequence、Utterance、Expected Sequence，并带 BPMN 引用。

## 简报

本文解决的问题是：企业 business process automation 工具需要把自然语言 workflow instructions 转成结构化流程工件，但缺少标准 benchmark，也不宜让 LLM 直接生成冗长 BPMN。作者提出 FLOW-BENCH 数据集和 FLOW-GEN 方法：先让 LLM 生成 Python-syntax intermediate representation，再由确定性模块转换为 BPMN/DMN 等 process definition languages。

- **输入**：自然语言 workflow instruction；增量编辑任务还输入当前 workflow 的 Python IR/BPMN。
- **方法**：从 activity catalog 检索相关 API/activity descriptions，从 demo set 检索 few-shot examples；LLM 生成受限 Python IR；PY2BPMN 转 BPMN；增量更新时 BPMN2PY 与 DIFF2BPMN 计算并应用更新。
- **输出**：Python IR、BPMN representation / updated BPMN workflow，面向 enterprise workflow automation。

```text
输入层：自然语言 workflow utterance + API catalog + prior workflow（可选）
  -> 方法层：activity retrieval + demo retrieval + LLM Python IR generation + PY2BPMN / DIFF2BPMN
  -> 输出层：structured business process artifact（Python IR + BPMN/DMN）
```

FLOW-BENCH 包含 101 个 incremental build step tests，覆盖 add/delete/replace、linear/conditional/loop/user task 等场景。FLOW-GEN 在 8 个 LLM 上评测，Mistral-large 达到最高 exact match（in-domain 0.83、cross-domain 0.79），Syntax F1 0.90/0.86。本文是 enterprise workflow / BPMN 强近邻，不是 STM direct baseline。

**可比字段快照**：

- **输入**：自然语言 workflow instructions；增量编辑时包括 prior sequence / prior BPMN。
- **输出**：Python IR、BPMN workflow definition，可能扩展到 DMN。
- **输出模型类型**：BPMN / business process automation workflow；强 process-model 近邻，非 STM 族。
- **使用的 LLM**：mixtral-8x7b-instruct-v0.1、granite-8b-code-instruct、llama-3.1-8b-instruct、Granite-20b-code-instruct-v2、codellama-34b-instruct-hf、llama-3.3-70b-instruct、Mistral-large、llama-3-405b-instruct。
- **主要方法**：retrieval-grounded few-shot prompting + Python IR generation + deterministic BPMN conversion。
- **需求词工程**：高；活动检索、demo 检索、few-shot in-context examples 和 API grounding 是核心。
- **运行仿真/验证**：无真实流程仿真；评测 exact match、Syntax F1、activity recall、hallucination rate。
- **形式化验证**：无 model checking；Python syntax/IR correctness 是主要约束。

## 研究问题与动机

### 问题背景

Business Process Automation 平台通常依赖可视化拖拽、模板和 API 配置。对 novice/citizen developers 来说，配置 API 调用、条件、循环和人工任务仍然复杂。LLM 可以从自然语言生成代码，但 BPMN 本身冗长且 boilerplate 多，直接生成容易出错。

### 核心问题

论文要解决两件事：构建 NL-driven workflow generation benchmark；设计一种让 LLM 先生成紧凑 Python IR、再自动转换为 BPMN/DMN 的 workflow generation 方法。

### 研究动机

作者观察到 BPMN 输出平均比等价 Python IR 长 25 倍。LLM 通常更擅长 Python code generation，因此让 LLM 生成 Python-like IR 可降低语法/语义错误，并便于后续多目标 process languages 转换。

### 研究意义

对 LLM4Modeling，本文强调中间表示和 API grounding 对减少 hallucination 的作用。对 Project 1，Python IR 对应可借鉴为“更符合 LLM 训练分布的 STM DSL/IR”，但必须注意 BPMN workflow 与控制系统状态机语义不同。

### 现有方法的局限性

现有 BPA/workflow generation 方法要么 fine-tune 特定 grammar、灵活性不足；要么 agent workflow code 不显式 grounding APIs，容易 hallucinate nonexistent actions；一些数据收集局限于 Apple Shortcuts/RoutineHub。FLOW-GEN 用 API retrieval + in-context learning 提高跨域泛化。

### 研究目标

目标是提供可公开使用的 FLOW-BENCH，并证明 FLOW-GEN 能在不同大小 LLM 上完成 initial generation 和 incremental workflow updates。

## 核心方法

### FLOW-BENCH 数据集构建

作者从 IBM App Connect 和 Zapier 等商业 workflow automation templates 收集真实企业工作流，进行三步处理：

1. **Quality Control**：去除过复杂、多层 nested conditions、单 API call、无公开 OpenAPI spec 的样例；移除 event triggers。
2. **Manual Labeling**：人工添加/修正 user utterance，手工编写 Python IR，并生成 BPMN specification；整理 API names/descriptions。
3. **Data Augmentation**：加入 user tasks，并构造 incremental add/delete/replace edits。

每个 build step 包含 Prior Sequence、Utterance、Expected Sequence。dataset 还提供 API catalog 及 descriptions，供 LLM grounding。

### Python Intermediate Representation

IR 使用受限 Python syntax：assignment、function calls、if-statements、for/while loops。API activities 以 Python function calls 表示，user tasks 表示无对应 API 的人工活动。Python IR 的紧凑性是本文关键假设。

### Initial Flow Generation

对新建 workflow：

1. 用户 utterance 触发 activity retriever，选择相关 API/activity descriptions。
2. demonstration retriever 选择最相关 few-shot samples。
3. LLM 根据 utterance、activities、demos 生成 Python code snippet。
4. PY2BPMN 将 Python IR 转为 BPMN。

### Incremental Flow Updates

对已有 workflow：

1. BPMN2PY 把当前 BPMN 转为 Python IR。
2. retrievers 同时考虑 utterance 和 prior code。
3. LLM 生成 updated Python IR。
4. DIFF2BPMN 计算 Python IR 差异，并对原 BPMN 应用 update operations。

### Retrieval 组件

- Activity retrievers：edit-distance、embedding retriever、Activities_Search custom model。
- Demo retrievers：TopKRetriever bi-encoder 与 CE_Retriever cross-encoder。
- embedding 使用 all-MiniLM-L6-v2；cross-encoder 使用 stsb-distilroberta-base。

### LLM/agent 设置

FLOW-GEN 使用 pre-trained LLM + retrieval + few-shot prompting，不做模型微调。论文没有多智能体架构；核心是检索增强和中间代码生成。

## 实验与评估

### 数据集

FLOW-BENCH 共 101 个 incremental build step tests，含 BPMN prior/output references、Python IR sequence 和 metadata tags。场景来自 enterprise workflow templates，含 API-based tasks 和 user tasks。

### 评估指标

- Activities Recall：retrieved/generated activities 与 ground truth 重合。
- Exact Match：生成 IR 与 ground truth 在语法和语义上的匹配。
- Hallucination Rate：生成 workflow 中不在 catalog 的 activities 比例。
- Syntax F1：生成 IR 代码语法正确性。

### 实验设置与结果

#### Activity retrieval

Activities_Search TopK=50 表现最好：Activities Recall 0.9926、Exact Match 0.7723、Hallucination Rate 0.0102。embedding retrieval 明显优于 edit distance。

#### Demonstration retrieval

CE_Retriever 通常比 TopKRetriever 提高 exact match；示例数超过 5 后性能反而下降。后续整体实验使用 Activities_Search TopK=50 和 CE_Retriever TopK=5。

#### Overall evaluation

表 3 中 Mistral-large 最好，in-domain exact match 0.83、syntax F1 0.90；cross-domain exact match 0.79、syntax F1 0.86。Codellama-34b-instruct-hf 次之，in-domain exact match 0.76、syntax F1 0.93；cross-domain 0.72、0.91。llama-3.1-8b-instruct 表现最差，exact match 0.19。

### Deployment

FLOW-GEN 作为 technical preview 部署到 IBM Watsonx Orchestrate 的 Unified Automation Builder，作为集群内 first-class component，结合 Watsonx.ai inference 与 Watsonx Assistant 用户接口。

### 方法优势

- 提供公开 workflow generation benchmark。
- Python IR 大幅降低 BPMN 生成长度和复杂性。
- API grounding 降低 hallucination。
- 支持增量编辑，不仅是一轮生成。
- 部署到真实企业自动化平台技术预览，工程相关性强。

### 方法的局限性

- FLOW-BENCH 规模 101，仍较小。
- 不覆盖 BPMN swimlanes/roles 等更复杂元素，原文明确说这些 BPMN-specific concepts out of scope。
- 评估主要是 IR exact/syntax/API grounding，没有 BPMN 语义仿真或形式化验证。
- 输出为 workflow/BPMN，不是状态机族。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | LLM 生成结构化 workflow/process artifacts。 |
| NL输入 | 🟢 | 主输入是自然语言 workflow instructions。 |
| LLM方法 | 🟢 | LLM + retrieval/few-shot 是核心生成组件。 |
| STM族输出 | 🟡 | BPMN/workflow 是强行为/process 近邻，但不是 STM-family。 |

它不能作为 direct STM baseline，因为生成对象是 enterprise workflow/BPMN/DMN 工件，不涉及状态、事件、迁移、守卫条件的 STM 输出。

### 研究定位与差异化

本文与 Project 1 共享“自然语言到结构化模型工件”的建模目标，但 workflow automation API sequence 与控制系统状态机不同。它更适合作为中间表示、检索增强、增量编辑 benchmark 的强近邻。

### 可借鉴之处

- **IR 选择**：选择 LLM 熟悉的代码式 IR，可降低生成难度。
- **catalog grounding**：Project 1 可对事件、变量、动作库做 retrieval grounding。
- **incremental update benchmark**：对 Project 4 修复任务可设计 prior STM + edit instruction + expected STM。
- **hallucination rate**：状态机生成也应统计未定义事件/变量/动作 hallucination。

### 存在的不足与改进空间

- 无状态机语义、无形式化验证、无控制系统场景。
- 不覆盖复杂 BPMN collaboration 或 data objects。
- GitHub 是否含完整 FLOW-GEN 代码待核验。
- Exact Match 对合理替代流程可能过严/过松，需结合语义执行评测。

### 对本研究的启发

Project 1 可把状态机生成拆为“NL -> typed Python-like STM IR -> pyfcstm DSL/XML/diagram”，并为每个样例提供 prior model / expected model / edit instruction，从而构建 agent-loop 修复 benchmark。FLOW-BENCH 的 add/delete/replace metadata 也可迁移为状态机 defect repair tags。

## 重要的相关工作

### 1. 重要的前身类工作

- BPMN/DMN standards：业务流程自动化工件的输出目标。
- IBM App Connect / Zapier templates：FLOW-BENCH 样本来源。

### 2. 直接参与实验的baseline

- 8 个 LLM：Mixtral、Granite、Llama、CodeLlama、Mistral-large 等，用于 FLOW-GEN evaluation。
- Activity retrievers 与 demo retrievers 的不同配置，是直接消融对象。

### 3. 提供了重要论证的工作

- AutoFlow、WorkflowLLM、Agentic Process Automation：相关 workflow generation/agent automation 工作。
- CodeJudge、CoRE 等 structured workflow / code generation 相关文献。

### 4. 在技术上提供了支持的工作

- all-MiniLM-L6-v2、ChromaDB、stsb-distilroberta-base：检索组件。
- OpenAPI specs：API grounding 的基础。

### 5. 其他重要工作

- Watsonx Orchestrate / UAB deployment 提供工程落地背景，但不是学术 baseline。

## 文献分类总结

本文是自然语言到企业 workflow/BPMN artifact 的强近邻，数据集和增量编辑设定对 Project 1/4 很有启发。正式评价应为 `🟠` BPMN/process 强近邻，四条件为 `🟢/🟢/🟢/🟡`。
