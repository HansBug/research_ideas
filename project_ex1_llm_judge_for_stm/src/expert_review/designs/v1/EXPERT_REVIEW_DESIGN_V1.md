# Expert Review 重构设计稿 V1

本文档定义 `expert_review` 的下一版重构设计。该版本不再把系统视为“一个带若干 heuristic 的单轮 LLM 评分器”，而是明确重构为一个基于 LangGraph 的、LLM-first 的、可多智能体协作的真正 agent 系统。

本版设计虽然吸收了真实人类专家评审的若干经验模式，但这些经验在实现时必须被蒸馏进 `expert_review/` 路径内自带的 prompt / policy / rubric 定义中，而不能在运行时依赖任何 `expert_review/` 路径外的本地语料、表格、讨论记录或数据资产。

本设计稿只讨论目标架构和实施边界，不涉及本轮代码实现。

## 1. V1 设计前提

这是本次重构最重要的前提集合。

### 1.1 默认始终有 LLM

`v1` 不再为“没有 LLM 的情况”设计工作流。

这意味着：

1. 不再把 heuristic fallback 当作主设计轴
2. 不再要求整套系统在无 LLM 时仍完整可用
3. 关键分析环节应优先设计成 LLM 主导，而不是 deterministic 主导

### 1.2 外部入口格式保持不变

对外接口必须继续兼容当前请求格式：

- `prompt`
- `input_text`
- `pred_output`
- `ref_output`

即：

- `ExpertReviewRequest` 继续保留
- `review_artifacts()` / `review_model()` 的调用方式继续保留
- CLI 的入参语义继续保留

### 1.3 输出格式尽量保持兼容

`v1` 的内部实现可以大幅重构，但最终外部输出仍应优先兼容 [`schema.py`](../../schema.py) 中的 `ExpertReviewResult` 结构。

### 1.4 大部分流程基于 LLM 完成

包括但不限于：

1. review contract 解析
2. requirement 拆解
3. artifact typing
4. pred/ref 要素提取
5. requirement trace 候选构建
6. extra / missing / conflict 元素判定
7. 分维度审查
8. 最终评分与综合说明

deterministic 工具在 `v1` 中应主要承担：

- I/O
- schema 校验
- 状态持久化
- 缓存
- 结果规整

而不再承担核心语义判断。

### 1.5 它必须是“真正的 agent 系统”

`v1` 不接受“换个 prompt 但本质还是单条线性函数”的伪重构。

至少要具备：

1. 任务分解
2. 条件路由
3. 工具自主选择
4. 多节点协同
5. 必要时的并行子任务
6. 可控的重试与裁决机制

### 1.6 支持多智能体，且可不共享上下文

这是 `v1` 的关键特征。

设计上允许：

1. 不同子智能体只看到与本任务相关的上下文包
2. 子智能体之间不共享完整对话历史
3. 主智能体只接收结构化中间结果，而不是把所有原始上下文完整广播给所有子智能体

### 1.7 `prompt` 是一等公民的 review contract 载体

`v1` 中的 `prompt` 不应被理解为“一小段指令文本”。

它可以承载广义 review contract，包括但不限于：

1. 任务目标与输出要求
2. 详细 rubric / 评分定义
3. 领域知识、术语定义、notation 约定
4. 等价判定原则、排除项、严格度说明
5. 必要的示例、反例或少量评审先验

因此 `prompt` 在设计上必须被当成“泛内容输入”，而不是简单字符串。

### 1.8 内部不得预设封闭的任务类型或模型类型

`v1` 不能把内部流程建立在少数预先写死的任务类别上。

这意味着：

1. 不允许假设“这是某种固定模型类型，所以应该走某个专用评审器”
2. 不允许假设“有 reference 就一定按 exact-match 风格评审”
3. 允许在运行时形成 profile，但该 profile 必须来自本轮输入与观测，而不是代码里的任务白名单
4. 内部真正允许稳定判断的，应是更抽象的证据条件，例如“是否有 reference”“是否有可解析结构”“是否只有汇总评分”“是否只给了 protocol”

### 1.9 已知格式检测只能是加速器，不是前提条件

`v1` 可以尝试检测已知格式并直接 lift 成结构化数据，但必须满足：

1. probe 失败不能阻塞后续评审
2. parser 输出只是证据来源之一，不是唯一 truth
3. 未知格式必须回退到 LLM 主导的通用要素抽取
4. 整个系统的可用性必须建立在“先观察、再抽取、再评审”，而不是“先认出格式才有资格评审”

## 2. V1 的总体目标

`v1` 的目标不是仅仅“提高分数”，而是同时提升以下四件事：

### 2.1 智能体性

系统应表现为：

- 会先识别任务性质
- 会决定先做什么分析
- 会决定何时调用什么工具
- 会决定哪些子任务并行
- 会在中间结果冲突时发起复核

### 2.2 LLM 主导性

大部分结构理解和评审判断应由 LLM 完成，deterministic 模块只做支撑。

### 2.3 结构化可审计性

即使内部变成多智能体协作，最终仍需保留：

- requirement dossier
- artifact dossier
- evidence items
- trace links
- issues
- notes
- score provenance

### 2.4 评审质量与校准能力

新系统应继续保留：

- 面向不同 review contract 的差异化评审能力
- 对 hallucination / unsupported complexity 的识别
- 对人类评审口径的 prompt calibration 能力

### 2.5 真实评审经验内化能力

`v1` 需要吸收真实人类专家评审中已经反复出现的经验模式，例如：

1. 组件级 matching 与整体质量评分是两类不同评审
2. 非同构但语义等价的设计需要给 credit
3. 可读性、命名纪律、未使用结构和复杂度风险是真实会看的维度
4. 某些场景里 manual inspection、formal verification 和 simulation/testing 承担互补角色

但这些经验必须以内置 policy 的方式存在于 `expert_review/` 包内，而不是以运行时外部数据依赖的方式存在。

## 3. V1 的核心设计原则

### 3.1 接口稳定，内部重构

外部接口保持兼容，内部完全允许重构为 graph-based multi-agent runtime。

### 3.2 结构化中间产物先于自由文本

每个子智能体应优先输出结构化 JSON，而不是长文本。

### 3.3 上下文按任务裁剪，而不是全量共享

默认不把完整 request 全量塞给所有子智能体。

### 3.4 评审结果必须有 provenance

最终分数不仅要有值，还要能回答：

1. 哪个 agent 产生了哪些证据
2. 哪些子结论发生过冲突
3. 最终综合器为什么采用当前判断

### 3.5 LLM 不只是 judge，也要承担 analyst / extractor / critic / synthesizer

`v1` 中的 LLM 角色会拆开，而不是让同一个提示词一次性完成所有工作。

### 3.6 `prompt` 先拆 contract，再分发给子智能体

子智能体默认不应直接继承原始 `prompt` 全文。

更合理的方式是：

1. 先由 Contract Router 把 `prompt` 拆成任务说明、领域知识、等价规则、评分口径、禁忌项
2. 再按需向不同子智能体分发最小必要片段
3. 避免所有 agent 都拿一整段混合 prompt 做模糊推理

### 3.7 已知格式 parser 是优化项，不是架构支柱

`v1` 可以利用 JSON / XML / PlantUML / Umple / TTool XML 等已知格式 parser，但这些 parser 的角色必须被严格限制为：

1. 降低 token 成本
2. 提高结构化抽取速度
3. 提供更可审计的表层 observation

而不是：

1. 主导最终语义判断
2. 决定当前任务“是不是可评审”
3. 把未知格式直接排除掉

### 3.8 语义等价优先于表面同形

`v1` 必须把“语义等价/行为兼容判断”设计成一级能力，而不是结果生成后的补丁。

这意味着：

1. 非同构但等价的设计应被明确给予 credit
2. 仅靠名字相似、元素重叠或 set diff 不能完成评审
3. transition / guard / action 等依赖性更强的元素，需要结合其所依附状态或结构一起判定
4. 等价判断规则应可被 prompt 和内置 policy packet 显式注入

### 3.9 对人评校准要以协议和证据形态为中心，而不是只盯分数

真实评审经验已经表明：

1. 有的论文给逐样本 `F1`
2. 有的只给 `/100` 或 `/10` 总分
3. 有的根本没有逐样本分数，只有人工 inspection / formal verification / simulation 的流程说明

因此 `v1` 的校准对象必须是：

1. 评分维度
2. 匹配规则
3. 证据要求
4. 允许的人工判断弹性

而且这些经验必须被固化为包内 prompt / rubric / policy，而不是运行时到包外检索“校准数据”。

## 4. V1 的运行时形态：LangGraph 多智能体图

### 4.1 为什么用 LangGraph

LangGraph 适合 `v1`，因为它天然支持：

1. 显式 state
2. 条件边
3. 循环与重试
4. 并行 fan-out / fan-in
5. 子图
6. 多 agent 协作

相比 `v0` 的线性函数，LangGraph 更适合作为 orchestration runtime。

### 4.2 V1 的顶层图

顶层图建议由一个主调度智能体驱动，并管理多个专用子智能体。

建议的顶层图如下：

```text
ENTRY
-> Contract Router
-> Evidence Regime Estimator
-> Review Policy Builder
-> Analysis Planner
-> parallel fan-out:
     Input Analyst Agent
     Prediction Extraction Agent
     Reference Extraction Agent (optional)
-> Dossier Merger
-> parallel fan-out:
     Traceability Agent
     Equivalence and Difference Agent
     Pragmatic Quality Agent
     Missing-Evidence Critic Agent
-> Disagreement Arbiter
-> Score Composer
-> Final Review Synthesizer
-> Schema Validator
-> EXIT
```

这不是要求每次都走完全相同的路径。

主智能体可以基于 contract、证据形态和可观测性决定：

1. 哪些子图启用
2. 哪些分支跳过
3. 哪些分支需要重跑
4. 是否发起额外 critique 回路

## 5. V1 的角色划分

### 5.1 主智能体：Orchestrator Agent

这是唯一掌握全局流程控制权的 agent。

职责：

1. 读取原始 `ExpertReviewRequest`
2. 基于 contract、artifact probe 和 evidence regime 形成运行时 profile
3. 生成任务计划
4. 决定调用哪些工具
5. 决定派发哪些子智能体
6. 管理重试、复核和仲裁回路
7. 汇总子结果并提交给综合器

它不需要自己做所有细节抽取；它的核心职责是调度。

### 5.2 Contract Router Agent

职责：

1. 解析用户 `prompt`
2. 把 `prompt` 拆成结构化 review contract
3. 产出 `review_contract`

结构化输出应包括：

- `task_statement`
- `comparison_posture`
- `priority_dimensions`
- `domain_knowledge_packet`
- `notation_knowledge_packet`
- `equivalence_policy`
- `evidence_policy`
- `scoring_policy`
- `strictness_profile`
- `forbidden_shortcuts`
- `special_instructions`

这个 agent 的输出将直接影响后续图的路由。

### 5.3 Review Policy Builder Agent

职责：

1. 根据 `review_contract`、artifact 可观测性和 evidence regime，组装当前请求对应的 `policy_packet`
2. 只使用 `expert_review/` 路径内自带的 prompt / rubric / policy 定义
3. 只提供“评审口径先验”，不替代本轮具体评审

`policy_packet` 应优先包含：

- 匹配规则
- 评分维度口径
- 内置等价判定规则
- 证据缺口说明
- 建议 score normalization 方式

### 5.4 Input Analyst Agent

职责：

1. 从 `input_text` 中提取 requirement / constraints / domain entities / exceptional scenarios
2. 对 requirement 进行层次化整理
3. 给后续 trace 和评分提供需求基线

输出应是 `input_dossier`，包括：

- requirement items
- scenario items
- constraints
- domain vocabulary
- ambiguity list

### 5.5 Prediction Extraction Agent

职责：

1. 对 `pred_output` 做非承诺式 known-format probe
2. 若 probe 命中，则调用对应 lift / parser 工具提取表层结构
3. 无论 probe 是否命中，都由 LLM 输出通用化 `prediction_dossier`
4. 在 dossier 中显式记录可观测性限制、未知项和 parser 置信度

该 agent 可以自行决定使用：

- 纯 LLM structured extraction
- 已知格式 lift 工具
- 混合抽取

但主导判断仍由 LLM 负责，parser 只提供 observation scaffold。

`prediction_dossier` 至少应包含：

- `surface_observations`
- `candidate_elements`
- `relations`
- `behavior_claims`
- `observability_limits`
- `format_probe_result`

### 5.6 Reference Extraction Agent

职责与 Prediction Extraction Agent 类似，但作用于 `ref_output`。

如果 `ref_output` 为空，则该 agent 不被创建。

### 5.7 Traceability Agent

职责：

1. 基于 `input_dossier` 和 `prediction_dossier` 建立 requirement-to-model trace
2. 在有 reference 时，补充 requirement-to-reference trace
3. 标出：
   - supported requirements
   - partially supported requirements
   - unsupported requirements
   - unsupported predicted elements

这一步不再局限于 lexical overlap，而是应以 LLM 语义判断为主。

### 5.8 Equivalence and Difference Agent

当存在 `ref_output` 时，它负责：

1. 建立 prediction 与 reference / input 之间的等价假设
2. 判断结构差异是否属于合理变体
3. 识别 missing / extra / conflicting 行为与结构
4. 明确哪些差异只是 harmless structural variation
5. 明确哪些差异是 semantic regression、unsupported complexity 或 dependency-break

它的重点是“等价与差异判断”，不是简单 set diff。

它必须显式支持：

1. exact match
2. near-exact match
3. semantic-equivalent but non-isomorphic
4. behavior-compatible but structurally divergent
5. unsupported divergence
6. evidence-insufficient

并且要吸收真实评审经验中的一个关键规则：

1. 如果某些 state / superstate 本身就不成立，则依附其上的 transition / guard / action 应更严格地下调，而不是孤立给 credit

### 5.9 Pragmatic Quality Agent

职责：

1. 判断可理解性、复杂度、命名纪律、可维护性风险
2. 单独分析 overmodeling / unnecessary complexity
3. 吸收人类专家真实会看的整体质量维度，例如 specification adequacy、readability、unused structure、naming consistency
4. 严格区分“模型看起来很复杂”和“模型真的有合理结构收益”

### 5.10 Missing-Evidence Critic Agent

这是 `v1` 中为了处理真实世界证据缺口而新增的角色。

职责：

1. 检测当前任务是 record-level、summary-only、protocol-only 还是 mixed-evidence
2. 明确哪些结论可以稳定下、哪些只能保留为低置信度 judgement
3. 防止 agent 在只有 aggregate score 或只有 protocol 时伪造 element-level certainty
4. 输出 `missing_evidence_dossier`，供 Arbiter 和 Score Composer 降低过度自信

### 5.11 Disagreement Arbiter Agent

这是 `v1` 中一个很重要的新角色。

职责：

1. 读取多个子 agent 的结果
2. 判断哪些结论冲突
3. 决定是否需要让某个子 agent 重跑
4. 对明显冲突项给出仲裁意见

例如：

- Traceability Agent 说 requirement 被支持
- Equivalence and Difference Agent 说对应行为仍然错误

那么 Arbiter 需要裁决“这是 support 还是伪 support”。

Arbiter 还要处理另一类新冲突：

- 某个分析 agent 给出强结论
- Missing-Evidence Critic 认为公开证据不足以支撑该强结论

### 5.12 Score Composer Agent

职责：

1. 读取已裁决后的结构化证据
2. 在 contract 指定或内置 policy 建议的 rubric 下形成各维度得分
3. 明确每个维度的加分依据和扣分依据
4. 把异构 score unit 映射为统一的内部归一化刻度，同时保留原口径 provenance

这个 agent 应只处理“评分组合”，而不再负责大型抽取工作。

### 5.13 Final Review Synthesizer Agent

职责：

1. 把各维度结果、trace、issues、notes 汇总成最终 `ExpertReviewResult`
2. 输出最终总评文字
3. 生成最终 `evidence_summary`
4. 补齐 provenance、policy profile 和 evidence-limit notes

## 6. 上下文隔离策略

用户特别要求“可以有多个不共享上下文的智能体”，因此 `v1` 的上下文策略必须是显式设计的一部分。

### 6.1 默认策略：最小任务上下文包

每个子智能体不直接继承主线程全部历史，而只接收：

1. 当前任务目标
2. 所需输入材料
3. 该任务输出 schema
4. 必要的评审约束

例如：

- Prediction Extraction Agent 不需要看到 Reference Extraction Agent 的推理过程
- Pragmatic Quality Agent 不需要看到全部 trace 细节
- Score Composer 不需要看到所有抽取时的中间草稿，只需要最后经仲裁的 dossier

### 6.2 共享方式：结构化 blackboard，而不是共享对话

多 agent 之间共享的不是完整聊天上下文，而是写入一个 graph state / blackboard 的结构化结果对象。

共享对象例如：

- `review_contract`
- `evidence_regime`
- `policy_packet`
- `input_dossier`
- `prediction_dossier`
- `reference_dossier`
- `trace_dossier`
- `comparison_dossier`
- `quality_dossier`
- `missing_evidence_dossier`
- `arbiter_decisions`

### 6.3 主智能体是唯一全局视角持有者

只有 Orchestrator 和最终综合节点拥有全局组合视角。

其他 agent 只处理各自局部上下文。

## 7. V1 的工具层设计

`v1` 的工具层不再只是“给 deterministic 函数套个 `@tool` 装饰器”，而应成为 agent 可调度的正式能力集合。

### 7.1 工具层角色

工具层主要承担：

1. 原始文本或 JSON/XML 的装载与规整
2. 大文本切片与摘要
3. schema 校验
4. evidence regime 探测
5. 已知格式 probe 与结构 lift
6. 泛化 artifact semantic extraction
7. 内置 policy 组装
8. execution trace / provenance 记录

### 7.2 建议工具分类

建议至少保留以下工具族：

#### 7.2.1 请求、contract 与 evidence 工具

- `load_request_tool`
- `split_prompt_contract_tool`
- `probe_evidence_regime_tool`
- `artifact_excerpt_tool`

#### 7.2.2 已知格式 lift 工具

- `known_format_probe_tool`
- `lift_json_like_tool`
- `lift_xml_like_tool`
- `lift_known_model_notation_tool`

这些工具是优化项，不是前置依赖。

#### 7.2.3 LLM structured extraction 工具

- `extract_requirements_tool`
- `extract_artifact_observations_tool`
- `extract_prediction_dossier_tool`
- `extract_reference_dossier_tool`
- `extract_trace_candidates_tool`
- `extract_equivalence_hypotheses_tool`

这类工具本质上会调用结构化输出 LLM。

#### 7.2.4 policy 编译工具

- `load_builtin_policy_tool`
- `build_review_policy_packet_tool`
- `load_builtin_domain_knowledge_tool`

#### 7.2.5 规整与校验工具

- `merge_dossiers_tool`
- `schema_validate_tool`
- `normalize_review_result_tool`
- `confidence_check_tool`

#### 7.2.6 诊断与裁决工具

- `compare_dossiers_tool`
- `detect_disagreement_tool`
- `detect_missing_evidence_tool`
- `request_reanalysis_tool`

### 7.3 工具调用策略

`v1` 中不应把工具调用顺序硬编码死。

应允许：

1. 主智能体先决定“是否需要调用 known_format_probe_tool”
2. 提取类智能体决定“先用 known-format lift 还是直接走通用 semantic extraction”
3. Review Policy Builder 决定“是否需要启用额外内置 policy 片段”
4. 仲裁器决定“是否重新调用某个 extraction tool”

也就是说，工具调用策略应成为图中决策的一部分，而不是固定线性步骤。

## 8. V1 的 graph state 设计

LangGraph 要想可维护，state 设计必须清晰。

### 8.1 顶层状态对象

建议顶层状态至少包含：

- `request`
- `review_contract`
- `evidence_regime`
- `policy_packet`
- `planner_decision`
- `input_dossier`
- `prediction_dossier`
- `reference_dossier`
- `trace_dossier`
- `comparison_dossier`
- `quality_dossier`
- `missing_evidence_dossier`
- `arbiter_dossier`
- `dimension_scores`
- `final_result`
- `execution_notes`
- `provenance_log`

### 8.2 每个 dossier 的设计原则

每个 dossier 应具备：

1. `summary`
2. `structured_items`
3. `confidence`
4. `open_questions`
5. `source_evidence`
6. `observability_limits`
7. `agent_id`

### 8.3 provenance log

建议显式记录：

- 哪个 agent 执行了哪个任务
- 用了哪些工具
- 命中了哪些已知格式 probe
- 启用了哪些内置 policy 模块
- 是否发生了重试
- 是否被 Arbiter 推翻

这对后续调试和论文复现实验都非常重要。

## 9. V1 的节点与边设计

### 9.1 节点集合

建议节点大致如下：

1. `ingest_request`
2. `contract_router`
3. `evidence_regime_estimator`
4. `review_policy_builder`
5. `analysis_planner`
6. `input_analyst`
7. `prediction_extractor`
8. `reference_extractor`
9. `dossier_merger`
10. `traceability_agent`
11. `equivalence_agent`
12. `pragmatic_quality_agent`
13. `missing_evidence_critic`
14. `disagreement_detector`
15. `arbiter`
16. `score_composer`
17. `final_synthesizer`
18. `schema_validator`

### 9.2 关键条件边

至少应有这些条件边：

1. `ref_output` 是否为空
2. known-format probe 是否高置信命中
3. 当前任务是 `record-level`、`summary-only`、`protocol-only` 还是 mixed-evidence
4. artifact 可观测性是否过低，需要额外 excerpt / reanalysis
5. 是否需要启用额外内置 policy 模块
6. 子 agent 输出是否低置信度
7. 子结果是否冲突
8. 最终 schema 是否有效

### 9.3 fan-out / fan-in

建议使用 parallel fan-out：

- `review_policy_builder`
- `input_analyst`
- `prediction_extractor`
- `reference_extractor`

以及第二轮 fan-out：

- `traceability_agent`
- `equivalence_agent`
- `pragmatic_quality_agent`
- `missing_evidence_critic`

然后统一 fan-in 到：

- `arbiter`
- `score_composer`

## 10. V1 的推荐执行流程

下面是一条推荐的标准执行流。

### 10.1 阶段 A：建立 review contract 与 evidence regime

1. 读原始请求
2. 把 `prompt` 拆成结构化 contract
3. 判断当前 evidence regime
4. 识别是否存在 reference、raw score、summary score 或仅 protocol
5. 识别优先维度、严格度和等价判定政策

输出 `review_contract` 与 `evidence_regime`

### 10.2 阶段 B：构建 review policy packet

1. 根据 contract 和 evidence regime 选择包内自带的 policy 片段
2. 根据 artifact 可观测性启用对应的 matching rules / score scale / evidence warnings
3. 输出 `policy_packet`

### 10.3 阶段 C：并行建立输入与工件 dossier

并行启动：

1. Input Analyst Agent
2. Prediction Extraction Agent
3. Reference Extraction Agent（可选）

Prediction / Reference Extraction Agent 在内部按以下顺序工作：

1. 先做 known-format probe
2. 如果 probe 命中，则把已知结构 lift 成 observation
3. 无论 probe 是否命中，都要求 LLM 输出通用 dossier
4. 如果 probe 失败或结构不完整，则显式记录 unknown / ambiguity

这一阶段结束后，系统应拥有三份相互独立、结构化、可引用的 dossier。

### 10.4 阶段 D：专用分析

在 dossier 基础上并行启动：

1. Traceability Agent
2. Equivalence and Difference Agent
3. Pragmatic Quality Agent
4. Missing-Evidence Critic Agent

这些 agent 不共享完整上下文，只共享 dossier、contract 与 policy packet。

### 10.5 阶段 E：冲突检测与仲裁

如果出现：

- trace 支持但语义仍冲突
- 比较代理认为结构差异无害，但质量代理认为复杂度过高
- Missing-Evidence Critic 认为公开证据不足
- 某个 agent 低置信度

则进入 `arbiter`。

Arbiter 可以：

1. 直接裁决
2. 要求重跑某个子智能体
3. 要求以更严格 schema 重新提取 dossier

### 10.6 阶段 F：评分与综合

1. Score Composer 产出维度分数
2. Final Synthesizer 组装最终结果
3. Schema Validator 保证结果完全兼容对外输出要求

### 10.7 从真实评审经验内化出的设计硬约束

`v1` 至少要内置下面这些硬约束：

1. 专家评审并不只是“总体印象分”，而是会同时看 format、grammar、semantic rule 和 requirement alignment；因此 `v1` 不能只做单维 overall judgement。
2. 真实专家会允许 `near-exact` 和 `semantic match`，即使名字不同、结构不同，只要表达同一概念仍可计为匹配；因此 `v1` 必须显式支持非同构等价 credit。
3. transition / guard / action 往往会对错误状态依赖采取更严格惩罚；因此 `v1` 不能把这些元素独立于其宿主结构去评分。
4. 真实专家会看 specification adequacy、simulator consistency、diagram readability、naming consistency、unused attributes 和 syntax warnings 等整体设计质量维度；因此 `v1` 不能把“评审”简化为 ref/pred diff。
5. manual inspection、formal verification 与 simulation/testing 在某些安全关键场景里承担互补角色；因此当 prompt 或内置 policy 强调这些角色时，`v1` 应报告 V&V 角色覆盖情况，而不是伪装成只靠文本比对就能完成高置信 assurance。
6. record-level、summary-only、protocol-only 是三种强烈不同的证据形态；因此 `v1` 必须有 Missing-Evidence Critic，而不是默认所有任务都能落到逐元素 certainty。

## 11. V1 的评分机制设计

`v1` 不应再把“评分”视为孤立一步，而应视为一个建立在 dossier 和裁决结果上的最后组合步骤。

### 11.1 评分输入

Score Composer 只读取：

- 已定稿的 dossier
- 已裁决的冲突项
- review contract
- rubric profile
- policy packet
- evidence regime

### 11.2 评分输出

输出应包括：

- 每个维度的 `score`
- 每个维度的 `reason_text`
- 每个维度的 `evidence`
- 每个维度的 `issues`
- 每个维度的 `confidence`

### 11.3 先形成分析判断，再映射到统一分数

`v1` 的评分顺序应是：

1. 先产出 requirement-level / element-level judgement
2. 再产出 dimension-level qualitative judgement
3. 最后才映射到 `ExpertReviewResult` 需要的归一化 numeric score

这样做的原因是，真实评审里同时可能存在：

1. `f1`
2. `semantic_f1`
3. `/100`
4. `/10`
5. 没有逐样本原始分数、只有 protocol 的情况

因此内部不能假设存在单一的原生分数单位。

### 11.4 score normalization 与 provenance 必须分开

总分建议仍使用权重化组合，但必须区分：

1. `normalized_internal_score`
2. `source_score_regime`
3. `policy_basis`
4. `weight_profile`

例如：

1. 若 policy packet 更接近 `component F1` 型评审 doctrine，则 completeness / equivalence 的权重更高
2. 若 policy packet 更接近 `overall software engineering quality` 型评审 doctrine，则 adequacy / readability / discipline 的权重更高
3. 若当前任务只有 protocol 没有 raw scores，则 overall numeric score 仍可输出，但必须下降置信度并在 provenance 中写清原因

### 11.5 总分计算

总分建议仍使用权重化组合，但权重来源应由 contract 与 policy packet 共同决定，而不再固定死。

## 12. V1 的输出兼容策略

尽管内部会大幅重构，最终仍建议保持以下兼容：

### 12.1 请求兼容

继续兼容：

```python
review_artifacts(prompt, input_text, pred_output, ref_output=None)
```

### 12.2 结果兼容

最终仍输出 `ExpertReviewResult`，至少保留：

- `prompt`
- `overall_score`
- `overall_judgement`
- `overall_reason_text`
- `used_review_backend`
- `dimension_results`
- `requirement_trace_results`
- `unsupported_model_elements`
- `evidence_summary`
- `notes`
- `confidence`

其中 `notes` 中建议额外保留：

- `evidence_regime`
- `policy_profile`
- `format_probe_hits`
- `missing_evidence_flags`

### 12.3 backend 标识

建议 `used_review_backend` 在 `v1` 中改成显式值，例如：

- `langgraph_multi_agent_v1`

## 13. V1 的建议目录架构

虽然本轮不改代码，但建议在实现阶段把当前单文件式结构拆开。

推荐代码路径架构如下：

```text
expert_review/
├── __init__.py
├── __main__.py
├── schemas/
│   ├── request.py
│   ├── result.py
│   ├── dossiers.py
│   └── graph_state.py
├── prompts/
│   ├── contract_router.py
│   ├── review_policy.py
│   ├── extraction.py
│   ├── traceability.py
│   ├── equivalence.py
│   ├── quality_review.py
│   ├── missing_evidence.py
│   ├── arbitration.py
│   └── synthesis.py
├── tools/
│   ├── artifact_io.py
│   ├── contract_io.py
│   ├── artifact_probe.py
│   ├── known_format_lift.py
│   ├── structured_extract.py
│   ├── policy_library.py
│   ├── dossier_merge.py
│   └── validation.py
├── agents/
│   ├── orchestrator.py
│   ├── contract_router.py
│   ├── review_policy_builder.py
│   ├── input_analyst.py
│   ├── prediction_extractor.py
│   ├── reference_extractor.py
│   ├── traceability.py
│   ├── equivalence.py
│   ├── pragmatic_quality.py
│   ├── missing_evidence_critic.py
│   ├── arbiter.py
│   ├── score_composer.py
│   └── final_synthesizer.py
├── graph/
│   ├── nodes.py
│   ├── edges.py
│   ├── subgraphs.py
│   └── runtime.py
├── compatibility/
│   └── legacy_api.py
└── designs/
    ├── README.md
    ├── GUIDE.md
    ├── v0/
    │   ├── README.md
    │   ├── GUIDE.md
    │   ├── EXPERT_REVIEW_RESEARCH.md
    │   ├── EXPERT_REVIEW_ARCHITECTURE.md
    │   ├── EXPERT_ALIGNMENT_REPORT.md
    │   └── EXPERT_REVIEW_DESIGN_V0.md
    └── v1/
        ├── README.md
        ├── GUIDE.md
        └── EXPERT_REVIEW_DESIGN_V1.md
```

这个路径架构的核心目的有两个：

1. 把“智能体角色”和“工具能力”分开
2. 把“图编排层”和“具体 agent 实现”分开

## 14. V1 与 V0 的核心差异

| 项目 | V0 | V1 |
|:--|:--|:--|
| LLM 假设 | 可有可无 | 默认恒可用 |
| 主流程形态 | 线性流程 | LangGraph 图 |
| 智能体形态 | 单 agent + heuristic | 真正多智能体协作 |
| 要素提取 | deterministic 主导，LLM 补强 | LLM-first |
| fallback 中心 | heuristic | 不再以无 LLM fallback 为主 |
| 上下文模型 | 基本单上下文 | 主智能体全局 + 子智能体局部上下文 |
| 内部任务建模 | 少量隐含任务类型 | contract / evidence-driven runtime profile |
| 已知格式处理 | 容易落回 parser 视角 | known-format probe 仅为加速器，未知格式仍可评审 |
| 评审口径来源 | 泛 prompt tuning | 当前请求 + `expert_review/` 包内自带 policy 编排 |
| 任务分解 | 很弱 | 显式分解 |
| 工具调用 | 基本固定 | 由 agent 决定 |
| 冲突处理 | 几乎没有专门层 | 引入 Arbiter |
| 输出 | 结构化 | 继续结构化兼容 |

## 15. V1 的迁移策略

`v1` 不能一口气把所有东西重写掉，否则很容易丢掉 `v0` 已验证过的能力。

建议迁移顺序如下：

### 15.1 第一步：保留外壳接口

先保留：

- `ExpertReviewRequest`
- `ExpertReviewResult`
- `review_artifacts()`
- `review_model()`

### 15.2 第二步：先实现 LangGraph runtime、dossier 与 evidence regime

先把 graph state、dossier 结构和 `evidence_regime` 搭起来，再替换旧单流程。

### 15.3 第三步：固化包内 review policy library

把已经认可的评审 doctrine、等价规则、证据限制说明固化进 `expert_review/` 路径内自带 policy。

### 15.4 第四步：先替换 extraction / trace / equivalence / synthesis 四段

因为这四段最能体现“LLM-first + semantic equivalence-first”。

### 15.5 第五步：补 Missing-Evidence Critic 与 Arbiter 闭环

当 runtime 已经能稳定跑通，再加公开证据缺口处理与仲裁闭环。

### 15.6 第六步：最后再移除旧 heuristic 中心地位

如果一开始就把所有 deterministic 能力全删掉，风险太高。

但在架构设计上，`v1` 不再围绕 heuristic 存在。

## 16. V1 的风险与控制点

### 16.1 风险：多智能体导致成本和延迟上升

控制方式：

1. 子智能体尽量只拿最小上下文包
2. 仅在必要时启用 Review Policy Builder、Ref Agent 或 Arbiter 重跑
3. 输出 schema 严格约束，减少无效长回复

### 16.2 风险：多 agent 输出冲突增加

控制方式：

1. 明确 dossier schema
2. 明确 Arbiter 机制
3. 对低置信度结果要求复核

### 16.3 风险：LLM-first 让系统不够稳定

控制方式：

1. 所有关键节点都要求结构化输出
2. 引入 schema validator
3. 引入 provenance log
4. 引入 agent-level retry 和 bounded loop

### 16.4 风险：接口兼容但语义改变

控制方式：

1. 外部 request/result schema 不变
2. notes 中显式记录 backend 与执行路径

### 16.5 风险：过拟合少量内置评审 doctrine

控制方式：

1. Review Policy Builder 只提供内置 policy prior，不直接提供最终结论
2. provenance 中显式记录启用了哪些内置 policy 模块
3. 没有足够相似的内置 policy 时，退回通用 rubric，而不是硬套某一条狭窄 doctrine

### 16.6 风险：未知格式工件导致抽取不稳定

控制方式：

1. known-format probe 失败时不终止，而是回退通用 extraction
2. dossier 中显式记录 observability limits
3. Missing-Evidence Critic 负责拦截过度自信结论

### 16.7 风险：`prompt` 过长、过杂、混合过多知识

控制方式：

1. Contract Router 先拆分 prompt，再按字段路由
2. 子智能体只接收最小必要 prompt 片段
3. 把领域知识、评分规则、等价规则分开存入 contract，避免一次性混喂

## 17. V1 设计结论

`v1` 的本质不是给 `v0` 再加几条 heuristic，也不是把 `llm_primary_review()` 改得更长，而是从系统范式上完成这几个跃迁：

1. 从“LLM 打分器”跃迁为“LLM 驱动的评审 agent 系统”
2. 从“单流程函数”跃迁为“LangGraph 编排图”
3. 从“单上下文单主体”跃迁为“主智能体调度的多智能体协作”
4. 从“把 prompt 当一句话”跃迁为“把 prompt 当泛内容 review contract”
5. 从“deterministic 主导提取”跃迁为“LLM-first 的 dossier 构建与评审”
6. 从“靠格式和任务类型做硬分支”跃迁为“contract / evidence-driven 的通用多智能体运行时”
7. 从“表面相似性比对”跃迁为“语义等价、依赖约束和整体设计质量并重”
8. 从“简单回退”跃迁为“带内置 policy、Missing-Evidence Critic、Arbiter 和 provenance 的结构化推理流程”

在保持现有入口兼容的前提下，这是一条足够激进、但又不会破坏外部使用方式的重构路线。
