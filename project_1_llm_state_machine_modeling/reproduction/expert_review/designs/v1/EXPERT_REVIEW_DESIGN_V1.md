# Expert Review 重构设计稿 V1

本文档定义 `expert_review` 的下一版重构设计。该版本不再把系统视为“一个带若干 heuristic 的单轮 LLM 评分器”，而是明确重构为一个基于 LangGraph 的、LLM-first 的、可多智能体协作的真正 agent 系统。

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

`v1` 的内部实现可以大幅重构，但最终外部输出仍应优先兼容 [`expert_review_schema.py`](../../expert_review_schema.py) 中的 `ExpertReviewResult` 结构。

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

- 面向行为模型与架构模型的差异化评审能力
- 对 hallucination / unsupported complexity 的识别
- 对人类评审口径的 prompt calibration 能力

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
-> Analysis Planner
-> parallel fan-out:
     Input Analyst Agent
     Prediction Extraction Agent
     Reference Extraction Agent (optional)
-> Evidence Merger
-> parallel fan-out:
     Traceability Agent
     Semantic Comparison Agent
     Pragmatic Quality Agent
-> Disagreement Arbiter
-> Score Composer
-> Final Review Synthesizer
-> Schema Validator
-> EXIT
```

这不是要求每次都走完全相同的路径。

主智能体可以基于任务性质决定：

1. 哪些子图启用
2. 哪些分支跳过
3. 哪些分支需要重跑
4. 是否发起额外 critique 回路

## 5. V1 的角色划分

### 5.1 主智能体：Orchestrator Agent

这是唯一掌握全局流程控制权的 agent。

职责：

1. 读取原始 `ExpertReviewRequest`
2. 判断当前任务属于：
   - standalone expert review
   - reference-aware semantic review
   - architecture-oriented review
   - behavior-oriented review
3. 生成任务计划
4. 决定调用哪些工具
5. 决定派发哪些子智能体
6. 汇总子结果并提交给综合器

它不需要自己做所有细节抽取；它的核心职责是调度。

### 5.2 Contract Router Agent

职责：

1. 解析用户 `prompt`
2. 识别评审意图与关注重点
3. 产出 `review_contract`

结构化输出应包括：

- `review_mode`
- `artifact_focus`
- `comparison_mode`
- `priority_dimensions`
- `strictness_profile`
- `special_instructions`

这个 agent 的输出将直接影响后续图的路由。

### 5.3 Input Analyst Agent

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

### 5.4 Prediction Extraction Agent

职责：

1. 对 `pred_output` 做类型识别
2. 选择合适工具完成结构化抽取
3. 输出 `prediction_dossier`

该 agent 可以自行决定使用：

- 纯 LLM structured extraction
- JSON / XML 解析工具
- 混合抽取

但主导判断仍由 LLM 负责。

### 5.5 Reference Extraction Agent

职责与 Prediction Extraction Agent 类似，但作用于 `ref_output`。

如果 `ref_output` 为空，则该 agent 不被创建。

### 5.6 Traceability Agent

职责：

1. 基于 `input_dossier` 和 `prediction_dossier` 建立 requirement-to-model trace
2. 在有 reference 时，补充 requirement-to-reference trace
3. 标出：
   - supported requirements
   - partially supported requirements
   - unsupported requirements
   - unsupported predicted elements

这一步不再局限于 lexical overlap，而是应以 LLM 语义判断为主。

### 5.7 Semantic Comparison Agent

当存在 `ref_output` 时，它负责：

1. 判断 prediction 与 reference 的结构差异是否属于合理变体
2. 识别 missing / extra / conflicting 行为与结构
3. 明确哪些差异只是 harmless structural variation
4. 明确哪些差异是 semantic regression 或 hallucinated complexity

它的重点是“语义比较”，不是简单 set diff。

### 5.8 Pragmatic Quality Agent

职责：

1. 判断可理解性、复杂度、命名纪律、可维护性风险
2. 单独分析 overmodeling / unnecessary complexity
3. 对 architecture-like 和 behavior-like 工件采用不同口径

### 5.9 Disagreement Arbiter Agent

这是 `v1` 中一个很重要的新角色。

职责：

1. 读取多个子 agent 的结果
2. 判断哪些结论冲突
3. 决定是否需要让某个子 agent 重跑
4. 对明显冲突项给出仲裁意见

例如：

- Traceability Agent 说 requirement 被支持
- Semantic Comparison Agent 说对应行为仍然错误

那么 Arbiter 需要裁决“这是 support 还是伪 support”。

### 5.10 Score Composer Agent

职责：

1. 读取已裁决后的结构化证据
2. 在统一 rubric 下形成各维度得分
3. 明确每个维度的加分依据和扣分依据

这个 agent 应只处理“评分组合”，而不再负责大型抽取工作。

### 5.11 Final Review Synthesizer Agent

职责：

1. 把各维度结果、trace、issues、notes 汇总成最终 `ExpertReviewResult`
2. 输出最终总评文字
3. 生成最终 `evidence_summary`
4. 补齐 provenance 与 notes

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
- `input_dossier`
- `prediction_dossier`
- `reference_dossier`
- `trace_dossier`
- `comparison_dossier`
- `quality_dossier`
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
4. 工件类型识别
5. artifact parsing helper
6. execution trace / provenance 记录

### 7.2 建议工具分类

建议至少保留以下工具族：

#### 7.2.1 请求与 artifact 工具

- `load_request_tool`
- `artifact_type_probe_tool`
- `artifact_excerpt_tool`
- `parse_json_or_xml_tool`

#### 7.2.2 LLM structured extraction 工具

- `extract_requirements_tool`
- `extract_prediction_dossier_tool`
- `extract_reference_dossier_tool`
- `extract_trace_candidates_tool`

这类工具本质上会调用结构化输出 LLM。

#### 7.2.3 规整与校验工具

- `merge_dossiers_tool`
- `schema_validate_tool`
- `normalize_review_result_tool`
- `confidence_check_tool`

#### 7.2.4 诊断与裁决工具

- `compare_dossiers_tool`
- `detect_disagreement_tool`
- `request_reanalysis_tool`

### 7.3 工具调用策略

`v1` 中不应把工具调用顺序硬编码死。

应允许：

1. 主智能体先决定“是否需要调用 artifact_type_probe_tool”
2. 提取类智能体决定“先用结构化抽取还是先尝试 parser helper”
3. 仲裁器决定“是否重新调用某个 extraction tool”

也就是说，工具调用策略应成为图中决策的一部分，而不是固定线性步骤。

## 8. V1 的 graph state 设计

LangGraph 要想可维护，state 设计必须清晰。

### 8.1 顶层状态对象

建议顶层状态至少包含：

- `request`
- `review_contract`
- `planner_decision`
- `input_dossier`
- `prediction_dossier`
- `reference_dossier`
- `trace_dossier`
- `comparison_dossier`
- `quality_dossier`
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
6. `agent_id`

### 8.3 provenance log

建议显式记录：

- 哪个 agent 执行了哪个任务
- 用了哪些工具
- 是否发生了重试
- 是否被 Arbiter 推翻

这对后续调试和论文复现实验都非常重要。

## 9. V1 的节点与边设计

### 9.1 节点集合

建议节点大致如下：

1. `ingest_request`
2. `contract_router`
3. `analysis_planner`
4. `input_analyst`
5. `prediction_extractor`
6. `reference_extractor`
7. `evidence_merger`
8. `traceability_agent`
9. `semantic_comparison_agent`
10. `pragmatic_quality_agent`
11. `disagreement_detector`
12. `arbiter`
13. `score_composer`
14. `final_synthesizer`
15. `schema_validator`

### 9.2 关键条件边

至少应有这些条件边：

1. `ref_output` 是否为空
2. 工件是否更像 architecture artifact
3. 工件是否更像 behavior artifact
4. 子 agent 输出是否低置信度
5. 子结果是否冲突
6. 最终 schema 是否有效

### 9.3 fan-out / fan-in

建议使用 parallel fan-out：

- `input_analyst`
- `prediction_extractor`
- `reference_extractor`

以及第二轮 fan-out：

- `traceability_agent`
- `semantic_comparison_agent`
- `pragmatic_quality_agent`

然后统一 fan-in 到：

- `arbiter`
- `score_composer`

## 10. V1 的推荐执行流程

下面是一条推荐的标准执行流。

### 10.1 阶段 A：建立 review contract

1. 读原始请求
2. 识别评审目标
3. 识别工件类型
4. 识别是否为 standalone / with-reference
5. 识别优先维度与严格度

输出 `review_contract`

### 10.2 阶段 B：并行建立输入与工件 dossier

并行启动：

1. Input Analyst Agent
2. Prediction Extraction Agent
3. Reference Extraction Agent（可选）

这一阶段结束后，系统应拥有三份相互独立、结构化、可引用的 dossier。

### 10.3 阶段 C：专用分析

在 dossier 基础上并行启动：

1. Traceability Agent
2. Semantic Comparison Agent
3. Pragmatic Quality Agent

这三个 agent 不共享完整上下文，只共享 dossier 和 contract。

### 10.4 阶段 D：冲突检测与仲裁

如果出现：

- trace 支持但语义仍冲突
- 比较代理认为结构差异无害，但质量代理认为复杂度过高
- 某个 agent 低置信度

则进入 `arbiter`。

Arbiter 可以：

1. 直接裁决
2. 要求重跑某个子智能体
3. 要求以更严格 schema 重新提取 dossier

### 10.5 阶段 E：评分与综合

1. Score Composer 产出维度分数
2. Final Synthesizer 组装最终结果
3. Schema Validator 保证结果完全兼容对外输出要求

## 11. V1 的评分机制设计

`v1` 不应再把“评分”视为孤立一步，而应视为一个建立在 dossier 和裁决结果上的最后组合步骤。

### 11.1 评分输入

Score Composer 只读取：

- 已定稿的 dossier
- 已裁决的冲突项
- review contract
- rubric profile

### 11.2 评分输出

输出应包括：

- 每个维度的 `score`
- 每个维度的 `reason_text`
- 每个维度的 `evidence`
- 每个维度的 `issues`
- 每个维度的 `confidence`

### 11.3 总分计算

总分建议仍使用权重化组合，但权重来源应可以由 contract 决定，而不再固定死。

例如：

- architecture-heavy 任务可上调 interaction / traceability 影响
- behavior-heavy 任务可上调 behavioral consistency / semantic completeness 影响

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
│   ├── extraction.py
│   ├── traceability.py
│   ├── semantic_compare.py
│   ├── quality_review.py
│   ├── arbitration.py
│   └── synthesis.py
├── tools/
│   ├── artifact_io.py
│   ├── artifact_probe.py
│   ├── structured_extract.py
│   ├── dossier_merge.py
│   └── validation.py
├── agents/
│   ├── orchestrator.py
│   ├── contract_router.py
│   ├── input_analyst.py
│   ├── prediction_extractor.py
│   ├── reference_extractor.py
│   ├── traceability.py
│   ├── semantic_compare.py
│   ├── pragmatic_quality.py
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

### 15.2 第二步：先实现 LangGraph runtime 与 dossiers

先把 graph state 和 dossier 结构搭起来，再替换旧单流程。

### 15.3 第三步：先替换 extraction / trace / synthesis 三段

因为这三段最能体现“LLM-first”。

### 15.4 第四步：最后再移除旧 heuristic 中心地位

如果一开始就把所有 deterministic 能力全删掉，风险太高。

但在架构设计上，`v1` 不再围绕 heuristic 存在。

## 16. V1 的风险与控制点

### 16.1 风险：多智能体导致成本和延迟上升

控制方式：

1. 子智能体尽量只拿最小上下文包
2. 仅在必要时启用 Ref Agent 或 Arbiter 重跑
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

## 17. V1 设计结论

`v1` 的本质不是给 `v0` 再加几条 heuristic，也不是把 `llm_primary_review()` 改得更长，而是从系统范式上完成这几个跃迁：

1. 从“LLM 打分器”跃迁为“LLM 驱动的评审 agent 系统”
2. 从“单流程函数”跃迁为“LangGraph 编排图”
3. 从“单上下文单主体”跃迁为“主智能体调度的多智能体协作”
4. 从“deterministic 主导提取”跃迁为“LLM-first 的 dossier 构建与评审”
5. 从“简单回退”跃迁为“带仲裁与 provenance 的结构化推理流程”

在保持现有入口兼容的前提下，这是一条足够激进、但又不会破坏外部使用方式的重构路线。
