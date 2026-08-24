# 历史参考实现流程对齐合同

本文冻结 `pipeline/evidence_discovery` 的流程基线。参考实现不是当前 legacy
副本，也不是报告中的二次描述，而是 Git 历史中的以下源码：

- 基线提交：`213c0ad0c73fa728be5edd70fc6e1495c996d14d`，即正式归档提交
  `2accd721` 的父提交；
- method：`pipeline/witness_search_prototype/prototype.py` 与 `graph.py`；
- 历史 Judge：`pipeline/witness_search_prototype/experiments/luna_full_x3_20260819/semantic_judge.py`，
  仅用于解释旧结果，不再属于现行 method runner；
- 运行证据与正式口径保存在版本化实验 provenance 中；具体运行别名不构成公开方法术语。

当前正式评测唯一入口是独立冻结的 `pipeline.semantic_judge` /
`semantic-judge.two-stage.v3.2`。`evidence_discovery` 只导出不可变 D1/D2 release reports、
D/W 与 W2 audit，不读取 ledger，不写 Judge receipt/cost/metrics。下表涉及旧 Judge 的行只说明
迁移前差异；目标实现一律按这个物理边界理解。

目标实现必须可表述为：**历史参考实现流程 + 冻结四族 19 谓词 compiler/backend +
适配新谓词所必需的 prompt 引导与 W2 审计字段**。prompt 可以根据真实审计结果持续
调优；受约束的是数据流、stage、调用复杂度、裁定边界和评测协议，而不是逐字复刻
历史文案。表中“目标”是当前正式合同。

## 逐项差异

| 维度 | 历史参考源码锚点 | 当前偏差 | 目标 |
|---|---|---|---|
| 输入 | `prototype.load_pair`、`build_contract_context`、`build_discovery_grounding_context`、`build_d_context` | 输入闭包已恢复，但 working contract、source trace、inspect/verify/SMT 和 candidate receipt 在多个 prompt 重复展开 | 完整保留编号 NL、PlantUML、canonical source IR、exact inventory、带 mapping 的 FCSTM、owned ModelIR、reference inspect、inspection-equivalent、verify、SMT、working contract 和 source trace；各 stage 仅取自身职责所需的最小投影，manifest/hash/path 始终落盘 |
| method stage | `graph.build_prototype_graph` | 将 source/model、逐 candidate binding/compiler/backend 各自提升成新的长期 stage 协议 | 恢复 `prepare -> contract-extraction -> discovery-grounding -> execute-batch -> d-adjudication -> validate-d -> publish`；candidate binding/compiler/backend 是 `execute-batch` 内部审计，不改变图跳转 |
| contract 调用 | `graph.contract_extraction` | 普通 pair 预设 chunk、逐块调用和 exact-ID merge | 正常路径整格一次 contract extraction；不设置主动 token/chunk gate。真实 provider context failure 只能按运行时失败协议记账，不创造新的下游协议 |
| grounding 调用 | `graph.discovery_grounding` 的两个 `FreshDiscoveryGroundingPlan` complementary lens | 将 source/model 固化成不同职责协议，且 source 候选只做归因、不会进入执行，偏离参考实现两个完整候选面的形态 | 一个 `discovery-grounding` stage 内固定 `contract_structure_contrast` 与 `behavior_consequence` 两次同 schema 调用；两者接收同一 compact cross-view closure，均完成 source identity、closed-model binding 和候选输出，结果按 exact typed key 汇入 `execute-batch` |
| round 关系 | 历史参考实现的三个独立 CLI method cell | round 2/3 prompt 注入上一轮 release | 三轮相互独立；previous release 不进入后续 round method prompt |
| execute | `graph.execute_batch` | binding/compiler/backend receipt 作为下游 prompt 树传播；空候选时制造首个 state/transition issue | 恢复整格 execute-batch；完整 candidate 审计落盘并以 hash/path 引用。空结果或失败只生成诊断，不生成语义 issue |
| D | `graph.d_adjudication`、`validate_d` | D 整体形态接近，但 eligibility 被任一 stage failure 全局否决 | 整格一次 D；validator 冻结合格项，只对缺失/非法项做至多一次定向 repair；D2/D1/D0 按冻结语义裁定合同执行，D_UNRESOLVED 显式保留；D0/D_UNRESOLVED 不发布 |
| W | 历史参考实现的 publication state machine；当前 `witness_levels.py` | 19 谓词 W 状态机已实现，但被全局 method eligibility 和 fallback issue 干扰 | W 完全确定性：精确绑定且完整 sound backend false receipt 为 W2；精确绑定但不支持为 W1 并仍可发布；绑定不足为 W0；UNKNOWN/timeout/error 不得成为 W2/violation |
| publish/dedup | `prototype.build_report_issue_clusters` | 逐 candidate 直接 release，重复 issue 进入旧 Judge | 只发布 D1/D2 且 W1/W2 合法的最小原子 cluster；按 exact typed semantic key 合并重复，支撑 facet 进入 evidence，不用文本相似度 |
| method eligibility | `graph.discovery_grounding` 与失败降级路径 | 任一 contract chunk、grounding branch、D correction 失败均可能使整格 `eligible=False` | provider/schema 的关键整格调用失败按协议使格子不可计；单 branch、单 obligation、compiler/backend 或定向 repair 局部失败只降级受影响单元，不抹掉其它闭合 release |
| Judge 输入 | 历史 `_cell_payload`、`_compact_method_report_issue` | 旧 runner 内部注入 method 审计树 | method runner 完全不构造 Judge 输入；外置 v3.2 adapter 只投影最终 release 的匿名最小语义字段，W/D/predicate/audit 不泄漏给 provider |
| Judge 调用 | 历史 `semantic_judge.judge_pair` | 旧 runner 内部执行并写 `judge/*.json` | 只由独立 `pipeline.semantic_judge` 在独立 run root 按冻结 batch/concurrency/protocol 执行；method 终态不依赖 Judge |
| metrics | 历史参考实现的 `aggregate.py` 与正式报告 | method summary 混入旧 Judge hit/FP/cost | method summary 只含 method 状态、release、D/W、诊断与 method cost；FULL/supported/K/N/I/FP/precision 和 Judge cost 只来自外置 v3.2；L 只从 ledger 读取 |
| runtime/失败 | 历史参考实现的 public responder、LangGraph、usage/pricing | 公共 runtime 已复用；新增外围恢复路径改变语义结果 | 继续复用 `respond`、LangGraph、`utils.agent/utils.llm`。stream 首字 30 秒、总 300 秒；non-stream 仅总 300 秒。provider error 原地重试且失败前序 attempt 免计费；其它重试计费。失败不得改写为业务 miss/FP |
| resume/identity | 历史参考实现的独立运行目录和 Judge manifest；当前 method run manifest v3 | 当前 identity 更严格但不应改变方法语义 | method 与 Judge 各自冻结 commit/schema/prompt/input hash 和原子写入；两者通过不可变 release source hash 关联，不共享 resume identity |

## 唯一允许保留的新层

1. `four-family-19-core.v1` 注册表、冻结谓词语义和最小输入；
2. owned、无 Python `inspect`/`pyfcstm.inspect`/旧 `inspect_*` 依赖的解析与
   inspection-equivalent facts；
3. 新 19 谓词 lowering/compiler/backend；
4. W2 的完整 logic、binding、formal program/hash、model/input hash、真实 backend
   result、terminal state、counterexample/trace、source attribution、reason/basis、
   retry/usage/cost/environment 审计；
5. 不改变 method 或外置 Judge 语义的独立 run identity、原子落盘和审计 hash/path。

这些信息不得扩大外置 Judge 输入，不得新增谓词，不得改变 D/W/L、release 或统计口径。

## Provider-free 对拍门

实现必须用测试证明：

1. 普通 pair 的逻辑调用形态固定为 `1 contract + 2 discovery grounding + 1 D`
   （D 有非法子集时再加一次 targeted repair）；
2. 三轮互不读取前一轮 release；
3. stage 顺序严格为七个已冻结 stage，candidate 审计不新增图节点；
4. method fixture 终态不需要任何 Judge response、receipt 或 ledger；
5. 空候选不制造 issue；单 obligation 失败不抹掉其它合法 release；
6. 外置 v3.2 adapter 输出不含 stage receipt、compiler/backend payload 或完整 W2 bundle；
7. 输入 manifest 能追溯全部输入闭包，prompt projection 没有静默截断；
8. 所有 Pydantic 模型对象和模型输出单元都有非空 reason/basis。
