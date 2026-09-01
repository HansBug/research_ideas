# Paper1 当前论文故事

## 问题与范围

本文解决 `<free-form NL requirements, pre-existing source-attributed STM held fixed during analysis> -> localized requirement-relevant issue reports`。source STM 在分析前已存在、具有准确来源归属且不被本文生成或修改；它可以来自人或上游 LLM。方法是通用状态机问题发现架构，FCSTM 是可执行工作表示，不是研究对象限定。能够在声明子集上形成可追溯 FCSTM projection、提供 source attribution、capability contract 和 fail-closed boundary 的状态机语言可以实现为 adapter。本文只实现并评测 PlantUML adapter；54 个 PlantUML pair 是路线可行性的案例研究，不是跨语言效果证据。

## C1 与 C2

**C1。** C1 构造保留来源的 FCSTM 工作表示和确定性 inspect facts，使候选可以引用状态、迁移、守卫、动作、拓扑和运行事实。它不声称全部 source-language 语义保持，也不单独造成已测 coverage gain。

**C2。** C2 将适用候选绑定到四族 19 条类型化义务，并保留 native execution/replay receipt 和 W0/W1/W2。它是 literature-informed, retrospectively consolidated evidence layer，不是由 54 pair 或台账调优的 taxonomy；机械 W 不替代人工 D/A、有效性、relation 或 K/N/I。

## 主张

截至 2026-09-02 的记录检索尚未形成可用作最终 scoped priority wording 的完整直接工作处置集。该范围限定主张由[最接近工作矩阵](../related_work/closest_work_matrix.md)承重。MCeT 排除宽泛行为图优先权；Sultan、GWT、Estivill、FRET、LiSSA 和状态机验证传统限制各自的组件表述。IET 2025 是直接风险候选：其 Gold-OA 元数据和摘要可复核，但正文在本轮取件中受 Cloudflare 阻断，不能把旧本地摘录冒充全文核验，也不能在其四字段裁定前冻结最强优先权主张。

## 研究问题

1. **RQ1：** 在冻结的 PlantUML 案例研究中，完整方法相对同模型 baseline 的 issue-discovery effectiveness 与 coverage--precision trade-off 是什么？单位为 435 round-level expected slots、145 expected issues 和报告级分母；结论是描述性比较。
2. **RQ2：** 类型化证据层在适用 current candidates 上产生何种 typed-plan closure、terminal receipt、replay、polarity、W 分布和 source attribution？单位为 receipt、predicate ID 和 FULL-hit unit；W 不等于 validity。
3. **RQ3：** current reports 的 attribution/failure boundary 和方法费用资格是什么？单位为报告和 invalid reports；NADC 仅为 current-side diagnostic，baseline 小计不得形成成本倍率。

## 已有证据与限制

54 pair 来自 9 个 NL clusters，每个 cluster 有 6 个 artifacts；145 expected issues 在三轮中形成 435 个 round-level units。current/baseline 的 overall FULL `hit@1` 为 `310/435=71.26%` 对 `227/435=52.18%`，L2 FULL `hit@1` 为 `105/117=89.74%` 对 `50/117=42.74%`。current report precision 为 `980/1271=77.10%`，baseline 为 `417/512=81.45%`。current FULL hits 的最高 W0/W1/W2 为 `0/113/197`，但 G2 的 1 条和 V4 的 82 条历史 W2 不作无界/全称论文解释。完整数字、分母和限制以 canonical archive 为准。

实际意义是 STM maintenance/review/audit workflow：工程师可先看高 D、高 W、source-attributed findings，并在需求、模型或工具版本变更后重放同一 evidence plan。本文没有 user study、reviewer-hour、safety certification 或 deployment outcome，因而不声称提高效率、认证或安全收益。
