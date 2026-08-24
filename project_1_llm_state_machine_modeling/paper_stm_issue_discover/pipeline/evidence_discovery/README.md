# 证据发现方法

本目录是当前证据发现方法的规范入口。正式配置为
`four-family-19-core.v1`，包含四个按证据形态划分的谓词族和 19 个公开原子谓词。
注册表见 [`predicate_registry.json`](predicate_registry.json)，人读版见
[`PREDICATE_REGISTRY.md`](PREDICATE_REGISTRY.md)。

本轮口径审计见 [`POLICY_REVIEW.md`](POLICY_REVIEW.md)。它记录旧材料的归档位置、迁移期
代码的隔离边界和当前尚不能声称的实测结论。

这里记录的是方法契约和重构目标，不把当前冻结的设计映射冒充成新实现的实测结果。
旧的 `witness_search_prototype` 已退出现行方法表面，仅在
`pipeline/archive/` 中作为历史复现材料保存。

## 方法与评测边界

`pipeline.evidence_discovery` 只负责发现候选、发布 D1/D2 issue、确定性裁定 W 等级并
保存证据审计和 method cost。method runner 不读取缺陷台账，不调用 Judge，也不生成
hit、FP 或 precision；W2 audit 在 method 阶段以 `pending_independent_judge` 终态化。

L0/L1/L2 只来自冻结台账。正式 technical validity、expected relation、FULL hit、
supported、semantic FP/precision 及其费用，唯一来源是独立冻结的
`pipeline.semantic_judge` / `semantic-judge.two-stage.v3.2` 及其冻结 validity/relation
与指标口径。
历史 method run 中若存在 `llm/judge`、`judge/*.json`、旧 Judge cost 或旧 hit/FP，均只作
历史协议审计，不能与 v3.2 结果静默混用，也不能作为新实验正式指标。

## 方法原则

1. **学术优先。** 谓词必须先有独立、命题匹配的领域或形式方法依据，再考虑台账覆盖；不能为了提高覆盖率从 benchmark 反向制造谓词。
2. **四族按证据形态划分。** 结构族表达封闭源模型事实，拓扑族表达图投影上的路径性质，轨迹仿真族表达一条完全落地的执行轨迹，有界验证族表达带量化或界限的可检查性质。四族不是按台账类别切分。
3. **19 个核心谓词冻结。** 宏可以组合已有谓词，但不能借宏名增加新的公开语义。
4. **谓词不是问题提出门槛。** 需求条目先经过语义绑定和裁决；没有 sound 谓词或后端时，仍要提出问题并降级为 W1。
5. **W1 是合法发布证据。** W1 表示需求和模型已精确绑定到可复现位置，但当前没有注册的 sound 判定器。W1 可以被外置 Judge 判为 FULL；W 等级本身不是 relation 或 validity 门。W2 是更高一级的、终止且带来源归因的可执行证据。W0 则连精确绑定都没有，不进入 release。
6. **未知不等于违反。** 任何后端返回 `UNKNOWN` 的结果都不能改写成 violation。
7. **D 由方法自裁，W 由确定性逻辑计算。** 方法按本目录冻结的语义裁定合同自行给出 D2/D1/D0，只有
   D2/D1 进入 release；是否 hit 或 FP 由外置 v3.2 Judge 决定。W2/W1/W0 由绑定、计划、
   后端状态和终止回执计算，不能由模型口头指定。L 是台账侧属性，方法不生成 L。
8. **每条模型输出都可调试。** 每一步、每一条结构化结果必须带非空 `reason` 或 `basis`；
   每条 W2 还必须带完整谓词逻辑、编译源码、哈希、真实运行结果和来源归因。
9. **后端和基础设施有边界。** 后端不使用 Python `inspect`；新入口复用公共
   `utils.agent`/`utils.llm` 与现有 respond/LangGraph。19 个谓词冻结，谓词不支持时仍发
   issue 并降级 W1，不得静默丢弃或擅自新增谓词。

## 输入闭包与阶段入口

正式 method 入口是 pipeline/evidence_discovery。它接收版本化的完整
ContextManifest，而不是只接收 nl.txt、plantuml.puml、fcstm.fcstm 和 ModelIR。
闭包至少包含编号 NL、PlantUML、canonical source IR、exact source/transition
inventory、working contract/mapping、source trace、FCSTM/ModelIR、reference inspection-derived
facts、owned inspection-equivalent facts、verify facts 和 SMT summary；每项都要有哈希、
版本、来源、reason 和 basis。

完整闭包不会被删除，但 prompt 按阶段展开权限范围：contract 阶段接收编号 NL 和工作契约
摘要；两个互补 grounding lens 接收同一份 compact cross-view closure，其中包含 PlantUML、
canonical source IR、exact source inventory、mapping/source trace、FCSTM/ModelIR、reference
inspection facts、自有 inspection-equivalent/verify/SMT facts；D 只接收带完整 manifest 身份的
候选 dossier。所有阶段都接收完整 artifact refs、hash/version 和 source-role policy。工作契约
中重复的 eligibility exclusion 序列只在 prompt 中以 count/hash receipt 表示，exact element
mapping 保留；原始文件仍由 manifest hash 定位。这是上下文压缩，不是删除输入闭包，也不允许
把 source/model/fact 角色混用。

PlantUML/source 与 canonical IR 只用于作者源定位，FCSTM 只用于闭合模型绑定与执行，
inspection-equivalent/verify/SMT facts 只用于确定性事实输入。新包自己实现并版本化
inspection-equivalent.fcstm-graph.v2、verify-equivalent.finite-graph.v2 和
smt-input-normalization.v1，不调用 Python inspect、pyfcstm.inspect 或旧 inspect_* 后端。

方法固定以下阶段边界：

prepare -> contract extraction -> discovery grounding -> execute batch ->
D adjudication -> validate D -> publish

`discovery grounding` 内固定执行 structure/contrast 与 behavior/consequence 两个同 schema 互补 lens；exact binding、19-predicate
compiler/backend 和 execution receipt 都留在 `execute batch` 内部审计。每轮正常逻辑调用
形态为 `1 contract + 2 grounding + 1 D`，D 结构不闭合时至多再做一次 targeted repair。
三个 method round 相互独立；每轮在 release reports 与 W2 audit 完整落盘后即成为终态。
正式评测由独立进程和独立输出目录中的冻结 v3.2 Judge 读取这些不可变 release reports，
不属于 method runner 的 stage、receipt、resume identity 或费用。

生成 prompt 不包含台账答案、baseline hit/FP、Judge 示例或历史 release 输出。完整
case report 只作为哈希 receipt 保存，prompt 仅接收身份/状态白名单投影。LLM 的每个
结构化对象和每个阶段 receipt 都由 Pydantic schema 约束并要求非空 reason/basis；
W/D/L 不由模型自报。

## 当前可表达性快照

冻结设计的映射为：

| 范围 | 可由核心谓词承载 | 分母 | 比例 | 解释 |
|---|---:|---:|---:|---|
| 当前台账 | 118 | 145 | 81.4% | 设计映射中的直接可表达条目 |
| L2 子集 | 35 | 39 | 89.7% | L2 中的直接可表达条目 |
| 历史参考实现映射 | 603 | 741 | 81.4% | 仅作设计覆盖参照 |

这三个数字是**可表达性快照**，不是新模块化实现的 W2 实测命中率，也不是 v3.2 Judge
的 FULL hit。W1 可正常发布且可被判为 FULL，因此不能把上述比例当作最终命中的硬上限；
正式结果必须同时报告外置 Judge 指标以及 method 的 W0、W1、W2 分布。

## 来源与学术边界

每个核心谓词都必须记录命题、最小输入、后端声称的 soundness fragment 和来源 ID。
来源 ID 的逐条落点和审查状态见
[`related_work/provenance/CURRENT_SOURCE_AUDIT.md`](../../related_work/provenance/CURRENT_SOURCE_AUDIT.md)
及机器目录 [`current_source_catalog.json`](../../related_work/provenance/current_source_catalog.json)。
来源 ID 指向 `related_work/provenance/` 或 `sources/` 中的领域文献、形式语义/标准资料或
技术资料档案。来源数量只说明命题存在及其来源多样性，不能当作普遍率分母，也不能用台账
使用量冒充学术证据。

当前来源门是“部分核验、其余显式保守”：部分候选集合仍含 timed、parallel 或 hybrid
材料，尚未全部满足项目规定的 T0、非并发、命题匹配和多来源门槛。因此现阶段只能说
“命题有候选依据且已登记”，不能宣称 19 个谓词已经全部通过严格来源门。来源不足时的
正确动作是保留 W1-only 状态，而不是放宽谓词含义或新增覆盖专用谓词。UML 2.5.1 对守卫
互斥的反向证据也已记录，不能把 `guards_disjoint` 写成标准强制要求。

## 允许与禁止的演进

除非同时满足下列条件，否则禁止新增谓词或修改现有谓词定义：

- 有独立于本台账的领域或形式方法证据，且来源与命题严格匹配；
- 能明确写出新命题、最小输入、适用边界、soundness 条件及 `UNKNOWN` 处理；
- 完成学术叙事审查，证明不是把 containment、cardinality、并发运行时或单个 benchmark 案例换名包装；
- 提供兼容性迁移说明、注册表校验、W1/W2 回归、来源审计和既有结果不被静默改写的测试；
- 经过独立 review 批准，并以新的注册表版本发布。

覆盖不足本身不是新增谓词的理由。对于低频、边界或需要额外外部参照的条目，优先
保留清晰的 W1 语义命中和显式 coverage gap。

## 施工状态边界

当前代码已完成输入闭包、分阶段 method 闭环、19 谓词编译/后端、确定性 W、typed LLM
semantic D、公共 runtime、W2 audit 和 method-only terminal receipt。live runner 对诊断子集
与 54-pair 全量保留不同的显式安全门；method runner 已与正式评测物理解耦。既有 Luna/audit
快照不被覆盖或冷重跑，旧实现只能用于历史复现，不能作为现行方法或新论文结果来源。

实验特定的诊断 case 集、运行路径、比较臂和历史代次只记录在实验 provenance 中，不属于
公开方法术语，也不得进入 method prompt、schema、类名、变量名或审计解释。局部诊断用于
小步调试和回归验收，不改变冻结评测分母，也不把短测结果写成方法达标结论。

## 确定性边界

现行规则采用可审计的职责边界：开放语义判断由具名 LLM 节点承担，形式事实由自有
parser、typed binding、图算法、SMT 输入规范化和后端承担。LLM 负责 NL 同义/指代、
义务是否成立、语义 grounding、条件作用域和最强反驳；确定性代码只能验证 exact ID、
枚举、引用闭包、公开语法 AST、图/轨迹/公式的声明 soundness fragment、hash、预算和
终止状态。不得用关键词、substring、正则、词干、编辑距离、embedding 或字符串相似度
替代语义判断；自由文本只进入 prompt、报告和审计，不进入 D/W 或 assertion 的语义裁定。

因此，`expected`、`observed` 和 `strongest_rebuttal` 等散文字段不会被确定性层比较。
D 阶段由 LLM 输出 typed grounding/defeater facts 及 `reason`/`basis`，方法代码只将
这些封闭枚举映射为 D2/D1/D0；W 仍完全由确定性状态机根据 binding、plan、backend
receipt 计算。归档的 predecessor design records 只保留历史 provenance，不构成公开方法
词汇，也不会被运行时 prompt 或 schema 读取。

## 当前代码状态

当前文件、注册表和 method-only runner 已可作为正式配置与接口契约。正式重构记录见
[`METHOD_PRINCIPLES.md`](METHOD_PRINCIPLES.md) 和 [`REFACTOR_PLAN.md`](REFACTOR_PLAN.md)。
旧实现只能用于历史复现，不能以 `prototype` 名义作为现行方法或新论文结果来源。

## 迁移后的效果目标

新代码使用本注册表和新规则，在相同台账、54 个 pair、最终发布边界、冻结 v3.2 Judge 和统计
分母下，目标是取得与冻结历史参考实现**大体相当或更好**的 hit 与 FP/precision。参考实现是量级参照，
不是逐格相等或绝对完美的硬门；达到大体相当即可，超过则记录改进。目标不能通过放宽
学术来源、把 W1 冒充 W2、把 `UNKNOWN` 改成 violation 或新增覆盖专用谓词来实现。
