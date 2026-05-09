# Expert Review 设计基线 V0

本文档将当前 `expert_review` 系统的三类已有材料整合为一个统一的 `v0` 版本描述：

1. 理论与评审口径来源见 [`EXPERT_REVIEW_RESEARCH.md`](./EXPERT_REVIEW_RESEARCH.md)
2. 当前实现结构见 [`EXPERT_REVIEW_ARCHITECTURE.md`](./EXPERT_REVIEW_ARCHITECTURE.md)
3. 与 TTool-AI 人类评分的对齐结果见 [`EXPERT_ALIGNMENT_REPORT.md`](./EXPERT_ALIGNMENT_REPORT.md)

该文档的作用不是重复全文，而是给后续 `v1` 重构提供一个可引用的基线。

## 1. V0 的系统定位

`v0` 的 `expert_review` 是一个“单次请求 -> 单次评审结果”的结构化评审系统，用来模拟软件行为建模领域的人类专家评审。

它解决的问题是：

- 输入 `prompt`
- 输入 `input_text`
- 输入 `pred_output`
- 可选输入 `ref_output`
- 输出一个结构化的 [`ExpertReviewResult`](../../schema.py)

这个结果里包含：

- 总分 `overall_score`
- 总体判断 `overall_judgement`
- 分维度评分 `dimension_results`
- requirement trace 结果
- 不受支持的模型元素
- 证据摘要
- 备注与置信度

## 2. V0 的硬约束

从现有实现和实验过程可以归纳出以下 `v0` 约束：

1. 外部入口格式固定为 `prompt / input_text / pred_output / ref_output`
2. 支持“有参考输出”和“无参考输出”两种模式
3. 输出必须是结构化 JSON 风格结果，而不是自由文本评论
4. 评审不能退化为 `pred/ref` 的表面字符串比较
5. 评审需要显式覆盖语法、语义完整性、行为一致性、需求可追踪性、可理解性等维度
6. 最终结果必须能落地到 parquet/json 等批处理产物

## 3. V0 的理论评审口径

`v0` 的理论来源主要来自三条线：

### 3.1 建模质量框架

来自 [`EXPERT_REVIEW_RESEARCH.md`](./EXPERT_REVIEW_RESEARCH.md) 的核心结论是：

1. 评审不能只看“像不像参考答案”
2. 至少要分开看：
   - syntax / notation
   - semantic completeness / validity
   - behavioral adequacy / consistency
   - traceability
   - pragmatic clarity / maintainability

### 3.2 行为模型评审不等于图形相似

研究说明明确强调：

1. 两个状态机不应仅凭结构差异判定优劣
2. 结构不同但行为合理时，应给 credit
3. 额外元素如果没有 requirement 依据，应视为 hallucination 或 unsupported complexity

### 3.3 需求到模型的追踪是核心能力

`v0` 假设一个高分模型必须回答：

1. 哪些 requirement 被模型中的哪些元素支持
2. 哪些 requirement 没有落到模型里
3. 哪些模型元素没有 requirement 支撑

## 4. V0 的实际实现形态

从实现角度看，`v0` 不是一个真正意义上的复杂智能体系统，而是一个“**确定性预处理 + 可选 LLM 主评审 + heuristic 回退 + 少量后处理校准**”的单轮流程。

主模块如下：

- [`agent.py`](../../agent.py)
- [`inventory.py`](../../inventory.py)
- [`schema.py`](../../schema.py)
- [`legacy/prompts.py`](../../legacy/prompts.py)
- [`legacy/rubrics.py`](../../legacy/rubrics.py)
- [`utils.py`](../../utils.py)

## 5. V0 的外部接口

`v0` 对外接口保持简单稳定：

### 5.1 Python API

通过 [`__init__.py`](../../__init__.py) 暴露：

- `review_artifacts()`
- `review_model()`

### 5.2 CLI

通过 [`__main__.py`](../../__main__.py) 提供单次命令行入口。

### 5.3 请求对象

请求对象是 [`ExpertReviewRequest`](../../schema.py)：

- `prompt`
- `input_text`
- `pred_output`
- `ref_output`

### 5.4 返回对象

返回对象是 [`ExpertReviewResult`](../../schema.py)。

## 6. V0 的默认维度

`v0` 当前固定采用 5 个维度：

1. `notation_syntax`
2. `semantic_completeness`
3. `behavioral_consistency`
4. `requirement_traceability`
5. `pragmatic_clarity`

这些维度由 [`legacy/rubrics.py`](../../legacy/rubrics.py) 的 `resolve_review_profile()` 返回。

当前实现中，虽然 `resolve_review_profile(prompt)` 接收 `prompt`，但它并不会真正因 prompt 不同而切换不同维度组合，实际仍然是固定 profile。

## 7. V0 的主流程

可以把 `v0` 的一次评审简化为：

```text
request
-> 解析 review profile
-> 解析 requirement 列表
-> 抽取 prediction/reference inventory
-> 生成 requirement trace
-> 生成 unsupported extra elements
-> LLM primary review 或 heuristic review
-> grounding calibration
-> 可选 architecture stability blend
-> 返回 ExpertReviewResult
```

其中最核心的公共步骤是 `_precompute()`。

## 8. V0 的 inventory 与 trace 机制

### 8.1 inventory 抽取

`v0` 的 inventory 抽取由 [`inventory.py`](../../inventory.py) 提供，主要有两条路径：

1. JSON payload 路径
2. 自由文本启发式路径

可提取的元素包括：

- `states`
- `transitions`
- `blocks`
- `signals`
- `rules`

### 8.2 requirement trace

`v0` 的 trace 主要依赖 lexical overlap：

1. 标准化 requirement 文本
2. 标准化模型元素文本
3. 看 token 是否重叠

最终产出：

- `matched`
- `partial`
- `missing`

这种 trace 机制能快速给出结构化支持，但本质上仍偏词面。

### 8.3 unsupported extra elements

当存在 `ref_output` 时，`v0` 会把 prediction 中相对 reference 多出来的：

- `state`
- `transition`

标记为 `extra`。

当前局限是：

1. 不记录 `block` 和 `signal` 的 extra
2. 缺失元素主要通过 match/trace 间接体现

## 9. V0 的 LLM 角色

`v0` 的 LLM 不是整个系统的 orchestrator，而更像“单次结构化裁判器”。

它的职责是：

1. 读取系统 prompt、请求 prompt、rubric、维度说明
2. 读取压缩后的 deterministic precomputed context
3. 给出结构化 JSON 评审结果

`v0` 的 LLM 主要由 [`llm_primary_review()`](../../agent.py) 驱动。

它具备：

1. JSON mode 调用
2. streaming fallback
3. JSON repair retry
4. dimension_results 缺失时重试

## 10. V0 的 heuristic 角色

`v0` 中的 heuristic 并不是“边角功能”，而是一个完整的后备评审器。

它负责：

1. 在无 LLM 时直接完成整次评审
2. 在 LLM 异常时兜底
3. 在某些架构型工件场景下给 LLM 结果提供稳定性混合

heuristic 对各维度均有明确规则，例如：

- requirement coverage 比例
- state/transition F1
- state/transition 复杂度膨胀惩罚

## 11. V0 的 grounding calibration

`v0` 的一个重要经验性增强是 grounding calibration。

### 11.1 状态机型工件

如果模型具有：

- 足够多的显式状态
- 足够多的显式迁移

系统会根据状态名是否和 `input_text` 领域词对齐，来区分：

- domain-specific state names
- generic placeholder states

然后做加减分。

### 11.2 架构型工件

如果工件更像 block diagram，则系统会基于：

- block 名称是否有领域锚定
- 是否存在显式 signal / interaction

做 architecture-grounding boost 或 penalty。

## 12. V0 的对齐实验结论

从 [`EXPERT_ALIGNMENT_REPORT.md`](./EXPERT_ALIGNMENT_REPORT.md) 可以提炼出 `v0` 的关键对齐结果。

### 12.1 最终采用的 prompt 变体

- `paper_rubric_v5`

### 12.2 总体对齐指标

最终对齐结果中：

- `overall` 评审数：`30`
- `MAE`：`11.98`
- `RMSE`：`15.22`
- `Pearson`：`0.662`
- `Spearman`：`0.594`
- `within_10`：`0.567`

### 12.3 分工件类型表现

- `bd`：`MAE = 13.04`
- `smd`：`MAE = 10.92`

### 12.4 分案例家族表现

- `automated_braking`：平均绝对误差 `9.56`
- `platooning`：平均绝对误差 `12.49`
- `space_based_system`：平均绝对误差 `13.89`

### 12.5 对齐上已经证明有效的改动

对齐报告明确指出，以下改动对 `v0` 有效：

1. `airouter` 流式回退
2. 紧凑预计算上下文替代大体量原始转储
3. 从解析后的 payload 中精确提取状态/块名称
4. 通用语义锚定校准
5. 通用架构锚定校准
6. 架构型结果的 LLM/heuristic 稳定性混合
7. LLM JSON 错误时重试

## 13. V0 的主要优点

`v0` 的优点是明确的：

1. 接口非常稳定，易于批处理接入
2. 输出结构化程度高，便于存表、对齐和审计
3. 没有 reference 时也能给出独立专家评审
4. 有 heuristic fallback，不会把整套系统的可用性完全押在单次 LLM 响应上
5. 已经在 TTool-AI 人类评分对齐实验中得到过实证验证

## 14. V0 的结构性不足

这也是 `v1` 重构的直接动机。

### 14.1 它不是“真正的智能体系统”

当前流程本质上仍是线性的：

1. 预处理
2. 一次主评审
3. 一次回退/混合

不存在真正的：

- 任务分解
- 工具自主调用策略
- 多轮反思
- 多智能体并行协作

### 14.2 大量关键逻辑仍是 deterministic heuristic

包括：

- requirement trace
- inventory 抽取的大部分主路径
- unsupported extra element 判断
- 分维度打分规则

这导致系统虽然稳定，但“智能体性”较弱。

### 14.3 LLM 在系统中更像后端评分器，而不是工作流主导者

LLM 当前更多是在 deterministic context 上做一次结构化打分，而不是驱动整个分析流程。

### 14.4 `prompt` 影响评审口径，但不真正决定流程结构

当前 `prompt` 会影响提示词和少量 heuristic 偏置，但不会让系统切换出真正不同的工作流。

### 14.5 context sharing 和任务隔离设计很弱

`v0` 中没有明确的 agent-to-agent 边界，也没有“不同子任务不同上下文包”的编排机制。

### 14.6 当前实现仍带有代码级设计债

例如现有架构说明中已经指出，某些与 architecture blending 相关的实现细节存在继续打磨空间。

## 15. V0 需要保留到 V1 的东西

尽管 `v1` 会重构范式，但 `v0` 里有一些东西不应丢。

### 15.1 外部接口

必须继续保持：

- `prompt`
- `input_text`
- `pred_output`
- `ref_output`

### 15.2 输出 schema

不应轻易推翻 [`ExpertReviewResult`](../../schema.py) 的核心字段，因为它已经和批处理、对齐脚本、实验产物耦合。

### 15.3 结构化中间产物意识

即使未来采用真正多智能体系统，也仍应保留：

- requirement dossier
- artifact dossier
- evidence items
- trace links
- issue lists

### 15.4 对齐中被证明有效的经验

以下经验应被视为 `v1` 的继承资产，而不是历史包袱：

1. 紧凑上下文优于粗暴全量上下文
2. 精确状态/块名提取很重要
3. 行为模型和架构模型需要不同校准方式
4. JSON 鲁棒性处理必须保留

## 16. V0 基线结论

`v0` 已经证明：一个结构化的专家评审系统是可行的，而且可以在 TTool-AI 上得到不差的对齐结果。

但 `v0` 仍然明显停留在“**单流程、弱 agent 性、强 heuristic 支撑**”的阶段。

因此，后续 `v1` 的方向应当是：

1. 默认始终有 LLM，不再围绕“无 LLM 也能跑”做设计
2. 用 LangGraph 把工作流从线性流程升级为真正的 agent graph
3. 让 LLM 主导要素提取、证据整合、评审计划和结果综合
4. 支持多个上下文隔离的子智能体，由主智能体调度
5. 保留接口稳定性和结构化输出能力
