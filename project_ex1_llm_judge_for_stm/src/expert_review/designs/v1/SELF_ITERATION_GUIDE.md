# Expert Review V1 自我迭代指南

本文档定义 `expert_review` 在 `v1` 阶段的**离线自我迭代闭环**。目标不是再写一套独立 judge，而是让当前 `expert_review` 的真实多智能体运行时，持续在真实人工评审基准上回放、对比、分析、改进，直到达到稳定的人类对齐效果。

本指南服务于两个同时成立的约束：

1. `expert_review` **运行时必须自包含**。实际对外评审时，只允许依赖当前请求和 `expert_review/` 路径内自带的 prompt / policy / rubric / code。
2. `expert_review` **离线迭代时可以使用外部 benchmark**。这里的外部 benchmark 指仓库里已经整理好的 `baselines` 双绿人工评审数据集，它只用于测试、分析和迭代，不得成为运行时依赖。

## 1. 文档定位

本指南回答四件事：

1. `expert_review` 应如何在真实人工评审数据上做回放测试。
2. 如何定义“和人类专家对齐”的指标体系。
3. 如何把误差分析转成可执行的 prompt / policy / agent 改进动作。
4. 何时可以认为当前版本已经达到可接受的人类对齐水平。

推荐阅读顺序：

1. 先读 [GUIDE.md](./GUIDE.md)
2. 再读 [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
3. 最后读本文

## 2. 基本边界

### 2.1 运行时与迭代时必须严格分离

运行时：

1. 只调用 `expert_review` 当前公开入口。
2. 不读取 `expert_review/` 路径外的任何 benchmark 文件。
3. 不允许根据 `case_id`、`paper_slug`、固定样本内容等做特判。

离线迭代时：

1. 可以用 `baselines` 双绿人工评审数据集做测试集和分析集。
2. benchmark 只能出现在**外环评测器**里，不能混进被测 runtime。
3. 被测对象始终是“当前真实 `expert_review` 运行时”，而不是某个特供 benchmark 版本。

### 2.2 不允许的做法

1. 把某篇论文的人工评分表 hardcode 到 reviewer prompt 里。
2. 根据 `paper_slug`、`review_record_id`、`record_type` 返回特定答案。
3. 在正式评审阶段直接把人工 `ref/human score/comments` 喂给 reviewer 主体。
4. 用 benchmark 上的人类解释文本直接替代 agent 自己的 reason text。
5. 只在全量 benchmark 上反复调 prompt，不保留 lockbox 集。

## 3. 迭代基准

本轮自我迭代默认使用：

- [baselines 双绿数据集下载解析与 parquet 化记录](../../../../discussions/2026-04-15-01-03-52-AI-%E8%AE%A8%E8%AE%BA-baselines%E5%8F%8C%E7%BB%BF%E6%95%B0%E6%8D%AE%E9%9B%86%E4%B8%8B%E8%BD%BD%E8%A7%A3%E6%9E%90%E4%B8%8Eparquet%E5%8C%96.md)

核心数据文件位于：

- `project_1_llm_state_machine_modeling/discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/`

本指南默认使用以下三类资产：

| 资产 | 作用 |
|---|---|
| `baseline_double_green_human_review_records.parquet` | 逐记录人工评审总表，是主评测输入 |
| `baseline_double_green_human_review_protocols.parquet` | 论文级人工评审方法复原表，用于理解评审 regime |
| `baseline_double_green_human_review_availability.parquet` | 公开性与证据缺口表，用于确定哪些任务允许做强对齐、哪些只能做弱对齐 |

## 4. Benchmark Regime

双绿人工评审数据不是单一同构 benchmark，至少包含三类 regime。

### 4.1 Record-Level Regime

特点：

1. 公开了较细粒度的单条人工评审记录。
2. 往往同时给了 `input_text`、`pred_output_text`、有时还有 `ref_output_text`。
3. 可以做较强的数值对齐、问题对齐和 reason 对齐。

典型记录形态：

1. `sample_level_review`
2. `component_level_review`

### 4.2 Summary-Level Regime

特点：

1. 只有 case 级、overall 级或 raw score row。
2. 有数值，但对单个模型元素的证据不完整。
3. 重点是整体打分口径、排序关系和证据克制。

典型记录形态：

1. `summary_level_run_score`
2. `case_aggregate_stat`
3. `overall_aggregate_stat`
4. `summary`
5. `raw_score_row`

### 4.3 Protocol-Only Regime

特点：

1. 没有逐样本原始分数，甚至没有完整预测输出。
2. 只有人工评审流程、V&V 分工、评审重点和可用性说明。
3. 重点不是 exact score alignment，而是 reviewer 是否知道**什么时候不能过度自信**。

### 4.4 Regime 处理原则

1. `record-level` 允许强对齐。
2. `summary-level` 允许中强度对齐，但必须惩罚 element-level overclaim。
3. `protocol-only` 不做伪精确打分拟合，重点评估 regime detection、证据纪律和 V&V 角色理解。

## 5. 自我迭代总流程

标准闭环如下：

```text
Benchmark Slice Builder
-> Task Replayer
-> 当前 expert_review 多智能体运行时
-> Result Normalizer
-> Human Comparator
-> Alignment Analytics
-> Error Taxonomy Miner
-> Improvement Planner
-> Prompt/Policy/Agent Patch
-> Regression Gate
-> Next Round
```

更细的执行顺序如下：

1. 冻结一个待评测版本 `candidate_vN`。
2. 构造本轮 `train/dev/validation/lockbox` 切片。
3. 用 `Task Replayer` 逐条调用当前真实入口 `review_artifacts()` / `review_model()`。
4. 在运行时阶段屏蔽人工标签、人工解释和任何 benchmark 专用捷径。
5. 把 agent 输出统一规整成可比较的 `normalized_review_records`。
6. 把规整结果与人工记录逐条对齐，产出指标、错误簇和残差分析。
7. 只根据错误模式修改 prompt / policy / agent 分工 / tool 路由。
8. 先在 dev slice 回归，再上 validation，最后看 lockbox。
9. 若达到停止标准，则冻结版本；否则进入下一轮。

## 6. 迭代系统中的多智能体分工

这里的“自我迭代”不是让 reviewer 自己改自己，而是外环再套一层 agent 系统。

### 6.1 Benchmark Slice Builder

职责：

1. 从总表构造切片。
2. 按 regime、论文来源、任务粒度做分层抽样。
3. 保证同一 artifact family 不跨 train/dev/lockbox 泄漏。

### 6.2 Task Replayer

职责：

1. 把 benchmark 记录转成 reviewer 的真实请求格式。
2. 只注入允许暴露给运行时的字段。
3. 严格屏蔽人工标签、人工原文点评和隐藏解释。

### 6.3 Result Normalizer

职责：

1. 统一 reviewer 输出格式。
2. 提取总分、维度分、issue、evidence、confidence、notes。
3. 把输出映射到统一分析 schema。

### 6.4 Human Comparator

职责：

1. 按 regime 选择不同的对齐策略。
2. 计算分数、排序、问题、reason 和证据纪律指标。
3. 输出逐记录残差与聚合统计。

### 6.5 Error Taxonomy Miner

职责：

1. 从差异中识别系统性失败模式。
2. 区分“该更严格”与“该更宽容”。
3. 区分“语义理解错误”与“证据纪律错误”。

### 6.6 Improvement Planner

职责：

1. 把错误模式转成修改 backlog。
2. 说明修改对象是 prompt、policy、agent 分工还是 tool 路由。
3. 给出预期受影响的指标和潜在回归风险。

### 6.7 Regression Gate

职责：

1. 判断修改是否只是在 dev 上过拟合。
2. 阻止 validation / lockbox 上显著退化的 patch 进入主线。
3. 决定是否升级为下一候选版本。

## 7. 数据切片原则

### 7.1 基本切片

默认拆成四层：

1. `train`：只用于观察错误模式，不直接看 lockbox。
2. `dev`：快速试错与 prompt/policy 小步迭代。
3. `validation`：版本晋升门槛。
4. `lockbox`：不得在日常调参中反复查看。

### 7.2 分层字段

至少按以下字段分层：

1. `paper_slug`
2. `record_type`
3. `diagram_type`
4. `review_target`
5. `human_review_score_unit`

### 7.3 分组防泄漏

同一生成 artifact family 必须放在同一切片内。默认分组键建议取：

1. `paper_slug`
2. `case_id`
3. `strategy_name`
4. `llm_name`
5. `review_target`

### 7.4 额外稳健性测试

除常规切片外，还应做一组 leave-one-family-out 测试：

1. 每次完整留出一个 `paper_slug`。
2. 观察 reviewer 是否只会对齐某一论文口径。
3. 该测试不过，则说明 reviewer 只是“学会了 benchmark 风格”，而不是学会了人类评审。

## 8. 对齐指标体系

“对齐程度”不能只看一个分数。至少应分成九类指标。

### 8.1 Regime Detection

衡量 reviewer 是否先判断清楚当前证据形态。

核心指标：

1. `regime_accuracy`
2. `protocol_only_overclaim_rate`
3. `summary_only_element_claim_rate`

目标：

1. 不把 `protocol-only` 任务误判成可做细粒度语义对齐。
2. 不在 `summary-only` 任务里伪造逐元素 certainty。

### 8.2 Numeric Score Alignment

用于所有有可比数值的记录。

先统一到 $[0,1]$：

1. `f1` 与 `semantic_f1` 直接使用。
2. `/100` 除以 `100`。
3. `/10` 除以 `10`。

核心指标：

1. `normalized_mae`
2. `rmse`
3. `spearman_rho`
4. `pairwise_order_accuracy`
5. `hit@0.03`
6. `hit@0.05`
7. `score_bias`

推荐组合指标：

$$
ScoreAlign = 0.4 (1 - MAE) + 0.3 \rho_s^+ + 0.3 Hit@0.05
$$

其中 `$\rho_s^+$` 表示把 `Spearman` 映射到 `[0,1]` 后的值。

### 8.3 Judgement Alignment

当 reviewer 给出 `overall_judgement` 或维度 judgement 时，衡量它与人工口径是否一致。

核心指标：

1. `macro_f1`
2. `weighted_kappa`
3. `judgement_flip_rate`

### 8.4 Issue Alignment

把人类评审和 agent 评审都映射到统一 issue taxonomy，再比较。

建议最少统一到以下类别：

| 类别 | 含义 |
|---|---|
| `syntax_or_notation` | 语法、格式、记法错误 |
| `missing_required_behavior` | 漏掉明确需求 |
| `wrong_guard_or_trigger` | 触发、守卫、方向性错误 |
| `wrong_action_or_effect` | 动作或后果错误 |
| `unsupported_extra_structure` | 无依据附加结构 |
| `equivalence_misjudgement` | 把合理变体错判为错误，或反之 |
| `readability_or_naming` | 命名、可读性、组织性问题 |
| `unused_or_noisy_structure` | 未使用属性、噪声结构、空复杂度 |
| `evidence_overreach` | 在证据不足场景里说得过满 |

核心指标：

1. `issue_precision`
2. `issue_recall`
3. `issue_f1`
4. `critical_issue_recall`

### 8.5 Reason and Evidence Alignment

不是要求 reason text 和人类逐字一致，而是要求 reviewer 抓住了相同的关键点。

核心指标：

1. `human_issue_coverage_recall`
2. `unsupported_claim_rate`
3. `contradiction_rate`
4. `evidence_locator_validity`

解释：

1. `human_issue_coverage_recall`：人类提到的关键问题里，reviewer 覆盖了多少。
2. `unsupported_claim_rate`：reviewer 声称的问题里，有多少在输入 / 输出 / reference 中找不到支撑。
3. `contradiction_rate`：reviewer 的不同维度结论彼此冲突的比例。

### 8.6 Equivalence Judgement Alignment

这是 `v1` 必须重点追的能力。

核心指标：

1. `semantic_match_accept_rate`
2. `equivalence_false_reject_rate`
3. `equivalence_false_accept_rate`
4. `dependency_aware_penalty_accuracy`

解释：

1. `semantic_match_accept_rate`：人类接受的非同构语义等价样本里，reviewer 是否也给了足够 credit。
2. `equivalence_false_reject_rate`：把合理变体误判为错误的比例。
3. `equivalence_false_accept_rate`：把真正错误当成 harmless variation 的比例。
4. `dependency_aware_penalty_accuracy`：当 state 本身错了时，reviewer 是否会对其依附 transition / guard / action 更严格处罚。

### 8.7 Evidence Discipline

这是 summary-only 和 protocol-only regime 的关键。

核心指标：

1. `abstention_quality`
2. `low_evidence_self_awareness`
3. `protocol_role_coverage`
4. `vv_role_precision`

解释：

1. `abstention_quality`：该保留时是否保留，该下结论时是否能下结论。
2. `protocol_role_coverage`：当人工 protocol 明确提到 inspection / formal verification / simulation/testing 时，reviewer 是否识别出这些角色。

### 8.8 Confidence Calibration

reviewer 不能只会说“我很有信心”。

核心指标：

1. `ece`
2. `brier_score`
3. `high_confidence_error_rate`

### 8.9 Stability and Cost

对齐不是一次跑出来就算数。

核心指标：

1. `rerun_score_std`
2. `issue_jaccard_across_runs`
3. `latency_p50`
4. `latency_p95`
5. `token_cost_per_record`

其中成本和延迟不是人类对齐主指标，但必须作为上线前约束。

## 9. 总体对齐指数

为方便版本晋升，建议定义三类 regime 分指数，再合成为总指标。

### 9.1 Record Alignment Score

$$
RAS = 0.30 ScoreAlign + 0.25 IssueF1 + 0.20 ReasonAlign + 0.15 EquivAlign + 0.10 Calib
$$

### 9.2 Summary Alignment Score

$$
SAS = 0.40 ScoreAlign + 0.25 RankAlign + 0.20 EvidenceDiscipline + 0.15 Stability
$$

### 9.3 Protocol Discipline Score

$$
PDS = 0.35 RegimeDetect + 0.25 VVRole + 0.25 OverclaimControl + 0.15 ConfidenceDiscipline
$$

### 9.4 Human Alignment Index

$$
HAI = 0.55 RAS + 0.25 SAS + 0.20 PDS
$$

说明：

1. `RAS` 权重最高，因为它最接近真实逐条人工评审。
2. `SAS` 次之，因为 summary-only 仍有明确人工整体打分口径。
3. `PDS` 不能省，因为它约束 reviewer 不要在证据不足时胡说。

## 10. 每轮迭代的标准产物

每轮至少产出：

1. `round_manifest.json`
2. `normalized_review_records.parquet` 或等价结构化结果
3. `alignment_report.md`
4. `error_taxonomy_report.md`
5. `patch_plan.md`
6. `regression_decision.md`

其中 `alignment_report.md` 至少应包含：

1. 本轮版本号
2. 各 regime 样本数
3. 所有核心指标
4. 前一轮与本轮差值
5. 最主要的三类进步
6. 最主要的三类退化

## 11. 不足分析方法

### 11.1 先按 regime 分析

先问：

1. 是在 `record-level` 上错了？
2. 还是在 `summary-level` 上过度 elementize？
3. 还是在 `protocol-only` 上证据纪律失控？

### 11.2 再按错误来源分层

每个误差必须归到以下五类之一：

1. `contract_understanding_error`
2. `element_extraction_error`
3. `equivalence_reasoning_error`
4. `quality_judgement_error`
5. `evidence_discipline_error`

### 11.3 最后再决定改哪里

推荐映射如下：

| 错误类型 | 优先修改对象 |
|---|---|
| `contract_understanding_error` | Contract Router prompt / schema |
| `element_extraction_error` | extractor agent / known-format lift / dossier schema |
| `equivalence_reasoning_error` | equivalence policy / examples / arbitration rule |
| `quality_judgement_error` | quality rubric / score composer 权重 |
| `evidence_discipline_error` | Missing-Evidence Critic / notes policy / confidence policy |

## 12. 允许的改进动作

1. 重写 system prompt、role prompt、dimension rubric。
2. 增删 agent 节点或调整 fan-out / fan-in。
3. 加强 equivalence examples 和 dependency-aware penalty 规则。
4. 调整 evidence regime 路由逻辑。
5. 调整 confidence policy、abstention policy 和 notes policy。
6. 调整 score composer 的 regime 权重与归一化方式。

## 13. 不允许的改进动作

1. 针对单篇论文写 case-specific prompt 分支。
2. 在 prompt 中直接引用 benchmark 的人工答案。
3. 用某个 benchmark 的固定字段名驱动 reviewer 的核心语义判断。
4. 为了提高某个 regime 分数而破坏另一个 regime 的证据纪律。
5. 只看整体 `HAI` 上升，不看关键子指标退化。

## 14. 停止标准

只有在以下条件同时成立时，才可认为当前版本“已经和人工达到可接受对齐”。

### 14.1 指标门槛

1. `HAI >= 85`
2. `RAS >= 88`
3. `SAS >= 80`
4. `PDS >= 78`
5. `normalized_mae <= 0.08`
6. `issue_f1 >= 0.75`
7. `human_issue_coverage_recall >= 0.80`
8. `equivalence_false_reject_rate <= 0.10`
9. `unsupported_claim_rate <= 0.08`
10. `protocol_only_overclaim_rate <= 0.05`
11. `ece <= 0.08`
12. `rerun_score_std <= 0.03`

### 14.2 稳定性门槛

1. 上述门槛在连续两轮完整验证中都成立。
2. lockbox 集上没有任何核心指标退化超过 `2` 点。
3. 没有出现新的高置信度严重误判簇。

### 14.3 停止后的动作

1. 冻结当前 reviewer 版本。
2. 生成版本级对齐报告。
3. 把当前 prompt / policy / rubric 固化到 `expert_review/` 路径内。
4. 新一轮迭代只能基于新的 benchmark 增量或新的设计版本继续。

## 15. 推荐执行节奏

### 15.1 小循环

适合 prompt / policy 微调：

1. 每次只改 `1-3` 个因素。
2. 先看 dev。
3. 不过 validation 不得晋升。

### 15.2 大循环

适合 agent 结构调整：

1. 先做设计变更。
2. 全量回放所有 regime。
3. 必做稳定性与 lockbox 测试。

## 16. 与 V1 主设计的关系

本文不是运行时架构文档，而是 `v1` 的外环改进手册。

二者关系如下：

```text
SELF_ITERATION_GUIDE
    -> 定义如何测试与改进
EXPERT_REVIEW_DESIGN_V1
    -> 定义被测试与被改进的目标系统
```

因此，后续如果 `v1` 真正落地实现，应同时维护：

1. [EXPERT_REVIEW_DESIGN_V1.md](./EXPERT_REVIEW_DESIGN_V1.md)
2. [SELF_ITERATION_GUIDE.md](./SELF_ITERATION_GUIDE.md)

前者回答“系统是什么”，后者回答“系统怎么被逼近人类专家”。
