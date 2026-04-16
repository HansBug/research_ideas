# Expert Review Agent 架构与工作流说明

本文档面向“代码太长，不想直接读实现”的场景，系统说明当前 [`expert_review`](../../README.md) agent 的整体架构、模块分工、单次评审流程、启发式细节、LLM 交互方式，以及它在 TTool 对齐实验中的接入方式。

相关文件：

- 设计调研与理论依据见 [`EXPERT_REVIEW_RESEARCH.md`](./EXPERT_REVIEW_RESEARCH.md)
- 对齐实验结果见 [`EXPERT_ALIGNMENT_REPORT.md`](./EXPERT_ALIGNMENT_REPORT.md)
- 主实现见 [`agent.py`](../../agent.py)

## 1. 一句话结论

当前 `expert_review` 不是一个会自主规划、多轮调用工具、再自己整理结论的复杂 agent。它本质上是一个“**确定性预处理器 + 可选 LLM 主评审器 + 启发式兜底评审器 + 少量后处理校准**”的单轮评审系统。

更具体地说：

1. 先把输入需求、预测工件、参考工件整理成统一的结构化 inventory。
2. 再生成 requirement trace、extra state/transition 等中间证据。
3. 如果有可用 LLM，就让 LLM 基于 prompt、rubric 和预计算上下文输出结构化 JSON 评审结果。
4. 无论 LLM 是否成功，系统都保留一条纯 Python 启发式评分路径。
5. LLM 失败时直接回退到 heuristic；某些架构型工件下还会把 LLM 结果和 heuristic 结果混合。

## 2. 这个 agent 解决什么，不解决什么

### 2.1 它解决什么

它要解决的是：给定

- `prompt`
- `input_text`
- `pred_output`
- 可选 `ref_output`

输出一个结构化专家评审结果 [`ExpertReviewResult`](../../schema.py)，其中包括：

- 总分 `overall_score`
- 总体文字判断 `overall_judgement`
- 分维度评分 `dimension_results`
- requirement trace 结果 `requirement_trace_results`
- 不受支持的模型元素 `unsupported_model_elements`
- 证据摘要 `evidence_summary`
- 备注 `notes`

### 2.2 它不解决什么

当前版本并不做这些事：

1. 不做真正的形式化语义等价证明，例如 bisimulation 或 trace refinement。
2. 不做真实的 UML/TTool/PlantUML 语法解析器级验证。
3. 不做 LangGraph/ReAct 风格的多轮工具调用和自反思。
4. 不把不同 baseline 通过隐藏分派逻辑硬编码进 agent 内部。
5. 不直接使用人类对齐分数作为打分规则的一部分；对齐实验是 agent 外部脚本做的。

## 3. 包结构与模块分工

当前实现主要分成下面几层：

| 文件 | 作用 |
|:--|:--|
| [`schema.py`](../../schema.py) | 定义所有输入输出 dataclass，以及序列化辅助函数 |
| [`legacy/prompts.py`](../../legacy/prompts.py) | 定义系统 prompt、评审指导语、示例、校准说明、维度模板 |
| [`legacy/rubrics.py`](../../legacy/rubrics.py) | 把当前评审 profile 固定为 5 个维度，并返回 `comparison_policy` |
| [`inventory.py`](../../inventory.py) | 需求拆分、inventory 抽取、集合匹配、trace 构建等可复用工具函数 |
| [`utils.py`](../../utils.py) | provider 配置、环境变量解析、JSON 提取、machine 归一化、计数等基础函数 |
| [`agent.py`](../../agent.py) | 主控制器。负责 provider 选择、预计算、LLM 主评审、heuristic 评审、回退与混合 |
| [`__init__.py`](../../__init__.py) | 暴露 `review_artifacts()`、`review_model()` 等简化 API |
| [`__main__.py`](../../__main__.py) | 提供单次 CLI 入口 |
| [`run_expert_review.py`](../../../run_expert_review.py) | 面向 baseline 数据集的批量评审入口 |
| [`align_ttool_expert_review.py`](../../../align_ttool_expert_review.py) | 面向 TTool-AI 的专家评分对齐实验入口 |
| [`test_review.py`](../../test_review.py) | 当前最小测试集，主要覆盖 heuristic 路径 |

一个很重要的事实是：

`inventory.py` 里虽然把若干函数包装成了 LangChain `@tool`，但当前 `ExpertReviewAgent` 并没有进入 tool-calling agent 模式，它只是**直接调用这些 Python 函数**。所以“工具层”在当前版本更像是“可复用函数层”，而不是“智能体外设”。

## 4. 输入输出数据模型

### 4.1 输入对象

入口请求对象是 [`ExpertReviewRequest`](../../schema.py)：

- `prompt`
- `input_text`
- `pred_output`
- `ref_output`

其中：

1. `prompt` 表示用户要求如何评审。
2. `input_text` 一般是需求描述、任务描述或论文输入文本。
3. `pred_output` 是待评审模型。
4. `ref_output` 是可选参考模型；没有它时，系统走“独立专家评审”模式。

### 4.2 输出对象

核心输出对象是 [`ExpertReviewResult`](../../schema.py)，字段含义如下：

- `overall_score`：`0.0` 到 `1.0`
- `overall_judgement`：通过 `judgement_from_score()` 离散化得到
- `overall_reason_text`：总评说明
- `used_review_backend`：`llm_primary` 或 `heuristic`
- `dimension_results`：每个维度的详细评分
- `requirement_trace_results`：需求到模型元素的 trace 结果
- `unsupported_model_elements`：与参考输出相比，多出来且暂不受支持的元素
- `evidence_summary`：证据摘要
- `notes`：补充说明、异常说明、校准备注
- `llm_model_name` / `llm_provider`：仅 LLM 路径会填
- `confidence`：总体置信度

### 4.3 当前启用的评分维度

默认 profile 由 [`resolve_review_profile()`](../../legacy/rubrics.py) 固定返回 5 个维度：

1. `notation_syntax`
2. `semantic_completeness`
3. `behavioral_consistency`
4. `requirement_traceability`
5. `pragmatic_clarity`

每个维度都是 [`DimensionDefinition`](../../schema.py)，包含：

- 名称
- 标题
- 描述
- 权重
- 正例
- 反例
- 评分注释

当前权重默认都为 `1.0`。

## 5. 总体执行流程

可以把单次 `review()` 理解成下面这条主线：

```text
review_artifacts / review_model / CLI
    -> ExpertReviewAgent()
    -> _build_llm()
    -> review(request)
        -> 如果没有可用 LLM:
             heuristic_expert_review()
        -> 如果有可用 LLM:
             llm_primary_review()
             heuristic_expert_review()
             _blend_architecture_result()
        -> 如果 LLM 路径任一步异常:
             heuristic_expert_review() + notes 记录异常
```

真正最关键的是 `_precompute()`，因为它同时服务于 LLM 路径和 heuristic 路径。

## 6. Provider 选择与 LLM 初始化

LLM 初始化逻辑在 [`ExpertReviewAgent.__init__()`](../../agent.py) 和 `_build_llm()` 中。

### 6.1 默认模型与 provider 顺序

定义在 [`utils.py`](../../utils.py)：

- 默认模型：`gpt-5.4`
- 默认 provider 顺序：`airouter -> findcg -> miaocg`

### 6.2 provider 配置

每个 provider 有：

- `base_url`
- 可接受的 API key 环境变量名

当前配置是：

- `airouter`: `AIROUTER_API_KEY`
- `findcg`: `FINDCG_API_KEY`
- `miaocg`: `MIAOCG_API_KEY` 或 `FINDCG_API_KEY`

### 6.3 环境变量来源

`resolve_api_env()` 会按下面方式解析：

1. 先读取当前进程环境变量。
2. 再尝试读取：
   - `~/.codex/findcg.env`
   - `~/.codex/api68886868.env`
3. 只在当前环境变量不存在时，才用文件里的值补上。

所以系统环境变量优先级高于本地 `.env` 文件。

### 6.4 没有可用 LLM 时的行为

如果遍历所有 provider 后都没有拿到可初始化的 `ChatOpenAI`，那么：

- `self._llm = None`
- `review()` 会直接走 `heuristic_expert_review()`

## 7. `_precompute()`：两条评审路径共享的前处理核心

`_precompute()` 是当前实现最重要的公共阶段。它负责把原始文本变成“可评审上下文”。

它做 6 件事：

1. 解析评审 profile
2. 解析 requirement 列表
3. 提取 prediction/reference inventory
4. 在 inventory 太稀疏时，用 LLM 做辅助抽取
5. 生成 requirement trace
6. 生成 unsupported extra elements

### 7.1 解析评审 profile

调用 [`resolve_review_profile()`](../../legacy/rubrics.py) 后返回三样东西：

- `rubric_text`
- `comparison_policy`
- `dimensions`

当前代码中的一个事实是：

`resolve_review_profile()` 虽然接收 `prompt`，但它现在并不会根据不同 prompt 动态生成不同维度集合，而是始终返回同一套 5 维 profile，`comparison_policy` 也固定是 `component_semantic_match`。

也就是说：

- `prompt` 会影响后续 LLM 提示词和某些 heuristic 打分偏置；
- 但它目前不会改变维度集合本身。

### 7.2 解析 requirements

需求解析由 [`parse_requirement_items()`](../../inventory.py) 完成，规则是：

1. 如果调用者显式提供了结构化 requirement 列表，优先使用它。
2. 否则尝试按行匹配 requirement 编号模式，如 `R1:`、`REQ_2:`、`FM3-...`。
3. 如果没有显式编号，再按段落、句号、分号、列表项等启发式拆句。

最终输出是 `RequirementItem(requirement_id, text)` 列表。

### 7.3 提取 inventory

inventory 提取由 [`extract_model_inventory()`](../../inventory.py) 完成。

它会同时处理 `prediction` 和 `reference` 两侧，每侧都做两件事：

1. 尝试把输入当作 JSON payload 解析。
2. 同时从自由文本中抽取 states / transitions / blocks / signals / rules。

然后把两路结果合并。

#### 7.3.1 JSON payload 路径

如果文本本身是 JSON，或者内嵌了一段 JSON，那么：

- `parse_json_payload()` 会尽量把它读出来。
- `machine_elements_from_payload()` 会把 machine/block/state/transition/signal/rule 归一化。
- `count_machine_components()` 会统计状态数、迁移数、guard 数、action 数等。

#### 7.3.2 自由文本路径

如果输入不是规整 JSON，系统会用 [`extract_generic_inventory_from_text()`](../../inventory.py) 做弱结构抽取：

- 从 `state X`、`block Y` 之类模式抽名字
- 从 `A -> B` 之类模式抽迁移
- 从 XML/JSON 风格字段抽 `name/source/target/event/guard`
- 从 TTool 风格 `<infoparam>` / `<Signal>` 片段抽块和信号

这条路径是“尽量保守地抓元素”，不是严格解析器。

### 7.4 稀疏 inventory 时的 LLM 辅助抽取

如果：

- 当前有 LLM
- artifact 文本非空
- 当前 inventory 项总数少于 3

那么 `_maybe_llm_augment_inventory()` 会触发一个额外的 LLM 调用，把原始工件文本规范化成一个保守 JSON 结构。

这个辅助抽取有几个特点：

1. 用的是单独的系统 prompt `ARTIFACT_EXTRACTION_SYSTEM_PROMPT`。
2. 输出 schema 是统一的 machine/block/state/transition/signal/rule JSON。
3. 规则要求“宁缺毋滥”，不能臆造行为。
4. LLM 抽出的 payload 只用于**补强 inventory**，不会直接替代原始文本。

所以当前系统在 LLM 模式下，实际上可能发生多次 LLM 调用：

1. prediction 辅助抽取
2. reference 辅助抽取
3. 主评审
4. 如有需要再做 JSON 修复或重试

### 7.5 requirement trace 生成

trace 生成分两层：

1. [`build_requirement_trace()`](../../inventory.py) 做最底层 lexical overlap 匹配
2. `_requirement_results()` 把它包装成 [`RequirementTraceResult`](../../schema.py)

当前 trace 逻辑是：

- 先把 prediction inventory 中所有元素标准化成可搜索文本
- 再把 requirement 文本标准化并切词
- 如果 requirement token 和某个元素的 normalized text 有重叠，就认为存在候选匹配

状态定义：

- `matched`
- `partial`
- `missing`

这里的 `partial` 不是深层语义推断，只是“词面支持较弱，需要人工确认”。

### 7.6 unsupported extra elements 生成

如果提供了 `ref_output`，系统会额外做：

- prediction state 集合 vs reference state 集合
- prediction transition 集合 vs reference transition 集合

然后把 prediction 中多出来的元素记成 [`ElementIssue`](../../schema.py)：

- `element_kind`: `state` 或 `transition`
- `issue_type`: `extra`

注意这里有两个局限：

1. 当前只显式记录 `state` 和 `transition` 的 extra，不记录 `block` 和 `signal` 的 extra。
2. 它只记录“prediction 比 reference 多了什么”，不直接记录“prediction 少了什么”；缺失更多体现在 requirement trace 和 match 结果里。

## 8. LLM 主评审路径

如果 `ExpertReviewAgent` 成功初始化了 LLM，`review()` 会优先尝试 [`llm_primary_review()`](../../agent.py)。

### 8.1 这条路径的基本思路

不是把原始文本原封不动扔给 LLM，而是先把 deterministic 证据整理好，再让 LLM 做“语义裁判”。

它给 LLM 的内容包括：

1. 系统 prompt `AGENT_SYSTEM_PROMPT`
2. 用户原始 `prompt` 加上统一的 `render_request_prompt()` 包装
3. 固定 rubric 文本
4. 固定 comparison policy
5. 维度说明 `render_dimension_guidance()`
6. 输入需求全文
7. reference/prediction 的截断摘要
8. 一个紧凑版 `compact_context`
9. 一个严格 JSON schema hint

### 8.2 为什么要有 `compact_context`

这个设计是为了避免“把整个 artifact 原文、整个 inventory、整个 trace 一股脑塞给 LLM”的大 prompt 失败模式。

当前压缩策略是：

- 只保留 prediction/reference 各侧的计数和前若干个元素
- 单独统计状态名和块名质量
- 只保留 trace 摘要
- 只保留前若干个 unsupported elements

这正对应对齐报告中说的“compact precomputed context instead of huge raw dumps”。

### 8.3 LLM 被要求输出什么

LLM 被要求返回严格 JSON，至少包含：

- `overall_score`
- `overall_judgement`
- `overall_reason_text`
- `dimension_results`
- `notes`
- `confidence`

每个 dimension 最多：

- 2 条 evidence
- 2 个 issues

同时 prompt 明确要求：

1. 分数要用开，不要全部挤在 `0.8` 左右。
2. heuristic precomputed trace 只是辅助，不要被它绑死。
3. 结构差异如果合理，要明确给 credit。

### 8.4 LLM 响应的鲁棒性处理

`_invoke_llm_text()` 的策略是：

1. 先正常 `invoke()`
2. 如果拿到空内容或异常，再走 `stream()` 拼接文本

当 `json_mode=True` 时，会给 `ChatOpenAI` 绑定 `response_format={"type":"json_object"}`。

此外还有两层 JSON 兜底：

1. 如果 LLM 输出不是合法 JSON，就发起一次“只做 JSON 修复”的补救请求。
2. 如果 `dimension_results` 为空，或者分数全是 `0.0`，就再发起一次带重试约束的请求。

### 8.5 LLM 结果回填成结构化对象

LLM JSON 最终会被解析成：

- `DimensionReviewResult`
- `EvidenceItem`
- 其他标量字段

有两个实现细节值得注意：

1. prompt 中的 JSON schema hint 并没有显式要求 `trace_links`，因此 LLM 路径下的 `trace_links` 往往是空的。
2. prompt 中的 JSON schema hint 也没有显式要求 `evidence_summary`，因此若未返回，系统会自动从每个维度摘取第一条 evidence 形成摘要。

## 9. heuristic 评审路径

`heuristic_expert_review()` 是没有 LLM 时的主路径，也是有 LLM 时的 fallback 路径。

它不是简单打默认分，而是对每个维度有明确的可解释规则。

### 9.1 `notation_syntax`

规则非常直接：

- 如果 prediction 中至少有 states / blocks / transitions 之一，则初始分 `0.9`
- 否则 `0.2`
- 如果 prompt 明确强调 syntax/grammar/格式，再最多加 `0.05`

本质上它判断的是“像不像一个可解释的模型工件”，不是严格 parser 级验证。

### 9.2 `semantic_completeness`

得分近似公式是：

`(matched + 0.5 * partial) / total_requirements`

如果 prompt 明确强调“遗漏”或 `focus on missing`，还会按缺失 requirement 数做额外扣分。

### 9.3 `behavioral_consistency`

如果有参考模型：

- 分别计算 state 集合 match 的 F1
- 再计算 transition 集合 match 的 F1
- 两者平均

当前代码明确承认：这只是行为一致性的 proxy，不是真正的行为语义验证。

如果没有参考模型：

- 依据 requirement trace 支撑度
- 再看 prediction 是否至少有明确的结构

得分是一个经验公式，最低不会低于 `0.2`，最高裁到 `0.95`。

### 9.4 `requirement_traceability`

得分近似公式是：

`(matched + 0.4 * partial) / total_requirements`

它同时会在 `issues` 里把未追踪 requirement 标成 warning。

### 9.5 `pragmatic_clarity`

这个维度主要看结构膨胀和维护压力。

有 reference 时：

- 默认 `0.8`
- 如果 prediction state 数超过 reference 的 `1.8` 倍，扣 `0.2`
- 如果 prediction transition 数超过 reference 的 `1.8` 倍，再扣 `0.2`
- 最低到 `0.15`

没有 reference 时：

- 默认 `0.82`
- 如果 state 数大于 `25`，扣 `0.15`
- 如果 transition 数大于 `50`，再扣 `0.15`
- 最低到 `0.2`

### 9.6 heuristic 路径的 trace_links

heuristic 结果会主动为 `semantic_completeness` 和 `requirement_traceability` 等维度补 `TraceLink`：

- `supports`
- `partially_supports`
- `untraced`

这使得 heuristic 路径在“结构化 trace 输出”上反而比当前 LLM 路径更完整。

## 10. 统一后处理：grounding 校准

无论是 LLM 路径还是 heuristic 路径，最终都会执行 `_apply_generic_grounding_calibration()`。

这是当前版本最关键的“通用领域校准器”。

### 10.1 状态机型工件的语义锚定校准

当 prediction 显式状态数和迁移数都至少为 `6` 时，系统会分析状态名质量。

分析方法：

1. 从模型里尽量精确提取状态名
2. 把状态名切词
3. 检查这些词是否和 `input_text` 中的领域词汇对齐
4. 区分“领域特定状态名”和“通用占位状态名”

如果：

- 领域特定状态很多
- 占位状态较少

就给以下维度加分：

- `semantic_completeness`
- `behavioral_consistency`
- `requirement_traceability`
- `pragmatic_clarity`

如果反过来模型大量依赖 `Idle / Processing / State1 / State2` 这类名字，就做对称扣分。

### 10.2 架构型工件的锚定校准

当：

- block 数至少为 `4`
- 同时显式 state/transition 很少

系统会把它识别为“更像架构图而不是状态机”的工件，并分析块名质量和 signal 数量。

如果：

- 块名中很多词能和需求领域词对齐
- 同时存在显式 signal / interaction

就对多个维度做 architecture-grounding boost。

如果：

- block 很多
- 但几乎没有交互

就施加 architecture penalty。

## 11. 架构型工件的 LLM/heuristic 混合

这部分逻辑在 `_blend_architecture_result()`。

设计意图是：

1. 一般情况下直接相信 LLM 主评审结果。
2. 但如果工件明显是高层架构图，就把 LLM 分数和 deterministic heuristic 分数做稳定性混合。

当前判定条件大致是：

- block 数不少
- state/transition 数不高
- 看 signal 数和 block grounding 质量

由此决定：

- `llm_weight = 0.75 / 0.50 / 0.25`
- `heuristic_weight = 1 - llm_weight`

然后把总体分数线性混合，并在 `notes` 里记录。

### 11.1 一个当前实现注意点

按当前代码阅读，[`_architecture_blend_weight()`](../../agent.py) 里有一处明显的调用参数不匹配风险：

- `_block_name_quality_summary()` 需要 `input_text, artifact_text, inventory`
- 但 `_architecture_blend_weight()` 当前只传了两个参数

这说明：

1. 设计上确实存在“架构型结果混合”这一层。
2. 但按当前源码静态阅读，这一段存在实现风险。
3. 如果这里真的在运行时触发异常，最外层 `review()` 会捕获异常并回退到 heuristic 结果，同时把异常写进 `notes`。

所以这部分要区分：

- “设计意图”是 LLM/heuristic 混合稳定化
- “当前实现”存在一处值得注意的代码级风险

## 12. 单次 `review()` 的真实返回策略

`ExpertReviewAgent.review()` 的返回逻辑非常重要：

### 12.1 没有 LLM

直接返回 heuristic 结果。

### 12.2 有 LLM 且 LLM 路径成功

执行顺序是：

1. `llm_primary_review()`
2. `heuristic_expert_review()`
3. `_blend_architecture_result()`

也就是说，即使 LLM 成功，heuristic 结果也还是会算一遍。

### 12.3 有 LLM 但任一步报错

会：

1. 再跑一次 heuristic
2. 把异常写到 `notes`
3. 返回 heuristic 结果

因此这个系统的鲁棒性来自于：

- LLM 不是唯一评分器
- 所有 LLM 失败都会被统一兜底

## 13. Prompt 层是怎么组织的

Prompt 层在 [`legacy/prompts.py`](../../legacy/prompts.py)。

它不是只靠一个长 system prompt，而是由几块拼出来：

1. `AGENT_SYSTEM_PROMPT`
2. `PROMPT_GUIDANCE`
3. `REVIEW_EXAMPLES`
4. `REVIEW_CALIBRATION_GUIDANCE`
5. `render_dimension_guidance(dimensions)`
6. `render_request_prompt(request)`

### 13.1 Prompt 的核心约束

系统显式要求 LLM：

1. 不要把任务偷换成自己的隐藏任务。
2. 不能因为 prediction 和 reference 结构不同就直接判错。
3. 不能因为模型更大就默认更好。
4. 每个维度都必须同时解释加分和扣分依据。

### 13.2 当前 prompt 的理论来源和实现差距

[`EXPERT_REVIEW_RESEARCH.md`](./EXPERT_REVIEW_RESEARCH.md) 里提出的理论框架比当前代码更丰富，涉及：

- syntactic / semantic / pragmatic
- completeness / consistency / soundness
- traceability
- understandability / maintainability
- hallucination 风险

但当前实现实际上只收缩成了 5 个维度，并通过 prompt 文本把剩余意图折叠进去。

所以现状是：

- 理论框架比实现更宽
- 实现是一个可运行、可对齐、可回退的收缩版

## 14. `inventory.py` 里的关键函数到底有什么用

### 14.1 `parse_requirement_items()`

把原始需求文本拆成统一 requirement 列表。

### 14.2 `extract_model_inventory()`

这是所有后续分析的结构化入口。很多逻辑都建立在它的输出上。

### 14.3 `compute_set_match()`

用于做 prediction/reference 的集合匹配，返回：

- `matched`
- `missing`
- `extra`
- `precision/recall/f1`

### 14.4 `build_requirement_trace()`

给 requirement 和 prediction inventory 之间建立 lexical trace 候选。

### 14.5 `@tool` 包装函数

这些函数虽然有 LangChain `@tool` 包装，但当前主流程并不通过 tool-calling 使用它们。它们更像：

- 可单独复用的工具层 API
- 未来如果要做真正多轮 agent，可直接复用

## 15. CLI 与外部调用方式

### 15.1 Python API

最简单入口在 [`__init__.py`](../../__init__.py)：

- `review_artifacts()`
- `review_model()`

这两个函数最终都会构造 `ExpertReviewRequest`，再调用 `ExpertReviewAgent().review()`。

### 15.2 单次 CLI

[`__main__.py`](../../__main__.py) 提供：

```bash
python -m expert_review \
  --prompt "..." \
  --input "..." \
  --pred-output "..." \
  --ref-output "..."
```

输出是整个 `ExpertReviewResult` 的 JSON。

### 15.3 baseline 批量运行

[`run_expert_review.py`](../../../run_expert_review.py) 支持两种模式：

1. `review-file`
2. `review-baseline`

它会把 baseline 数据转成统一的 `ExpertReviewRequest`，再批量调用 agent。

## 16. TTool 对齐实验是怎么接入这个 agent 的

[`align_ttool_expert_review.py`](../../../align_ttool_expert_review.py) 并不改 agent 内部逻辑，它做的是 agent 外部的数据准备和评估。

### 16.1 它做了什么

1. 读取 TTool-AI 人类专家分数 `results.ods`
2. 从 TTool XML / parquet 中构造两类工件摘要：
   - block diagram summary
   - state machine diagram summary
3. 为不同 prompt variant 生成不同评审提示词
4. 对每个样本调用 `ExpertReviewAgent`
5. 把预测分数和人类分数对齐，输出 parquet/json/cached payload

### 16.2 为什么这里的 `pred_output` 不是原始 XML

因为对齐脚本会先把 TTool 工件整理成一个紧凑 JSON 摘要，再送给 agent。

例如：

- block diagram 会抽出 blocks、attributes、signals、connector exchanges
- smd 会抽出 panel、state、transition、unused attribute 候选、若干统计量

所以在 TTool 对齐场景中，agent 看到的并不是“原始模型文件”，而是“为评审而整理过的 artifact summary”。

### 16.3 prompt variant 的作用

对齐脚本里维护了 `paper_rubric_v1` 到 `paper_rubric_v5` 多套 prompt 文案，核心区别是：

1. 对 block diagram 的宽严程度不同
2. 对 state-machine set 的保守/宽松程度不同
3. 对 architecture-level credit 与 behavior-level strictness 的口径不同

这是 agent 外部做 calibration 的主要手段之一。

## 17. 测试与当前可验证结论

当前测试文件是 [`test_review.py`](../../test_review.py)。

它主要验证：

1. heuristic 路径能返回结构化结果
2. reference 存在时能标出额外结构
3. reference 缺失时仍能工作
4. 未知自由文本格式也能走通

需要注意的是：

1. 当前测试覆盖重点是 heuristic 路径，而不是完整 LLM 路径。
2. LLM 路径的可靠性更多依赖运行时 provider、网络和 JSON 修复逻辑。

## 18. 读代码时最值得抓住的主线

如果你后面还想回去读代码，建议按这个顺序：

1. 先看 [`schema.py`](../../schema.py)
2. 再看 [`agent.py`](../../agent.py) 的 `review()`、`_precompute()`、`llm_primary_review()`、`heuristic_expert_review()`
3. 不明白 inventory/trace 时，再回看 [`inventory.py`](../../inventory.py)
4. 最后看 [`legacy/prompts.py`](../../legacy/prompts.py) 和 [`align_ttool_expert_review.py`](../../../align_ttool_expert_review.py)

只要抓住下面这个骨架，整套系统就不会迷路：

```text
输入请求
-> requirement 解析
-> inventory 抽取
-> requirement trace / extra element 生成
-> LLM 主评审或 heuristic 评审
-> grounding 校准
-> 可选架构稳定性混合
-> 结构化结果
```

## 19. 最后总结

当前 `expert_review` 的真实形态不是“黑盒 LLM 裁判”，而是：

1. 先用 deterministic 方法尽量把模型元素、需求元素和对应关系抽出来。
2. 再把这些中间证据交给 LLM 做高层语义判断。
3. 同时始终保留一条可回退的 heuristic 路径。
4. 对某些典型误差模式，再用少量领域启发式做后校准。

它的优点是：

- 接口稳定
- 结构化输出完整
- 无 reference 时也能工作
- 有 fallback，不至于完全依赖一次 LLM 响应

它的代价是：

- 许多“语义判断”仍然依赖词面匹配和 prompt 校准
- 真正形式化的行为等价没有进入实现
- 理论框架比当前代码更宽，现实现仍是收缩版
- 某些细节实现还存在值得继续打磨的空间

如果后续你要继续扩这个 agent，最关键的三个切入点通常会是：

1. 强化 inventory 抽取和 requirement trace 的语义性，而不只是 lexical overlap
2. 让 `resolve_review_profile()` 真正根据任务切换维度与权重
3. 把当前“函数式工具层”升级成真正可控的 tool-calling 评审 agent
