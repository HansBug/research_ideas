# v27 流程对齐合同

本文冻结 `pipeline/evidence_discovery` 的流程基线。参考实现不是当前 legacy
副本，也不是报告中的二次描述，而是 Git 历史中的以下源码：

- 基线提交：`213c0ad0c73fa728be5edd70fc6e1495c996d14d`，即正式归档提交
  `2accd721` 的父提交；
- method：`pipeline/witness_search_prototype/prototype.py` 与 `graph.py`；
- judge：`pipeline/witness_search_prototype/experiments/luna_full_x3_20260819/semantic_judge.py`；
- 运行证据：`runs/paper1/luna-full-x3-20260820-v27-stream/`；
- 正式口径：`discover_matrix/docs/generations/v27/preregistered.md` 和
  `reports/2026-08-20-luna-full-x3-v27-stream/`。

目标实现必须可表述为：**v27 流程 + 冻结四族 19 谓词 compiler/backend +
适配新谓词所必需的 prompt 引导与 W2 审计字段**。prompt 可以根据真实审计结果持续
调优；受约束的是数据流、stage、调用复杂度、裁定边界和评测协议，而不是逐字复刻
v27 文案。表中“目标”是当前正式合同。

## 逐项差异

| 维度 | v27 源码锚点 | 当前偏差 | 目标 |
|---|---|---|---|
| 输入 | `prototype.load_pair`、`build_contract_context`、`build_discovery_grounding_context`、`build_d_context` | 输入闭包已恢复，但 working contract、source trace、inspect/verify/SMT 和 candidate receipt 在多个 prompt 重复展开 | 完整保留编号 NL、PlantUML、canonical source IR、exact inventory、带 mapping 的 FCSTM、owned ModelIR、reference inspect、inspection-equivalent、verify、SMT、working contract 和 source trace；各 stage 仅取 v27 职责所需的最小投影，manifest/hash/path 始终落盘 |
| method stage | `graph.build_prototype_graph` | 将 source/model、逐 candidate binding/compiler/backend 各自提升成新的长期 stage 协议 | 恢复 `prepare -> contract-extraction -> discovery-grounding -> execute-batch -> d-adjudication -> validate-d -> publish`；candidate binding/compiler/backend 是 `execute-batch` 内部审计，不改变图跳转 |
| contract 调用 | `graph.contract_extraction` | 普通 pair 预设 chunk、逐块调用和 exact-ID merge | 正常路径整格一次 contract extraction；不设置主动 token/chunk gate。真实 provider context failure 只能按运行时失败协议记账，不创造新的下游协议 |
| grounding 调用 | `graph.discovery_grounding` 的两个 `FreshDiscoveryGroundingPlan` complementary lens | 将 source/model 固化成不同职责协议，且 source 候选只做归因、不会进入执行，偏离 v27 两个完整候选面的形态 | 一个 `discovery-grounding` stage 内固定 `contract_structure_contrast` 与 `behavior_consequence` 两次同 schema 调用；两者接收同一 compact cross-view closure，均完成 source identity、closed-model binding 和候选输出，结果按 exact typed key 汇入 `execute-batch` |
| round 关系 | v27 三个独立 CLI method cell | round 2/3 prompt 注入上一轮 release | 三轮相互独立；previous release 不进入后续 round method prompt |
| execute | `graph.execute_batch` | binding/compiler/backend receipt 作为下游 prompt 树传播；空候选时制造首个 state/transition issue | 恢复整格 execute-batch；完整 candidate 审计落盘并以 hash/path 引用。空结果或失败只生成诊断，不生成语义 issue |
| D | `graph.d_adjudication`、`validate_d` | D 整体形态接近，但 eligibility 被任一 stage failure 全局否决 | 整格一次 D；validator 冻结合格项，只对缺失/非法项做至多一次定向 repair；D2/D1/D0 按 issue #189，D_UNRESOLVED 显式保留；D0/D_UNRESOLVED 不发布 |
| W | v27 publication state machine；当前 `witness_levels.py` | 19 谓词 W 状态机已实现，但被全局 method eligibility 和 fallback issue 干扰 | W 完全确定性：精确绑定且完整 sound backend false receipt 为 W2；精确绑定但不支持为 W1 并仍可发布；绑定不足为 W0；UNKNOWN/timeout/error 不得成为 W2/violation |
| publish/dedup | `prototype.build_report_issue_clusters` | 逐 candidate 直接 release，重复 issue 进入 judge | 只发布 D1/D2 且 W1/W2 合法的最小原子 cluster；按 exact typed semantic key 合并重复，支撑 facet 进入 evidence，不用文本相似度 |
| method eligibility | `graph.discovery_grounding` 与失败降级路径 | 任一 contract chunk、grounding branch、D correction 失败均可能使整格 `eligible=False` | provider/schema 的关键整格调用失败按协议使格子不可计；单 branch、单 obligation、compiler/backend 或定向 repair 局部失败只降级受影响单元，不抹掉其它闭合 release |
| judge 输入 | `semantic_judge._cell_payload`、`_compact_method_report_issue` | 注入 stage receipt、predicate plan、backend receipt、source attribution、完整 reason 树和 audit 内容 | judge 只读冻结 ledger 与三轮最终 D1/D2 clusters 的最小语义字段；W2 只给 audit hash/path，不给 compiler/backend/stage receipt 树 |
| judge 调用 | `semantic_judge.judge_pair` | 正常路径含 token/release gate、partition、partition correction 和 atomic 矩阵 | 一次 pair-wide judge；机械 shape 不闭合时至多一次定向 correction；仍失败即 `judge_unavailable`，不造 miss/FP。历史 `213c0ad0` 中的 atomic fallback 按本轮明确裁定删除 |
| metrics | v27 `aggregate.py` 与正式报告 | 同时提供额外 eligibility 下界，但 release 资格可能被当前全局 gate 改写 | 只以 D1/D2 release 和独立 judge 关系统计；D0、D_UNRESOLVED、W0、UNKNOWN、judge unavailable 不进入 hit/FP；L 只从 ledger 读取；保留 v27 hit@1/hit@3、L2、D2xL2、FP/precision 与成本口径 |
| runtime/失败 | v27 public responder、LangGraph、usage/pricing | 公共 runtime 已复用；新增外围恢复路径改变语义结果 | 继续复用 `respond`、LangGraph、`utils.agent/utils.llm`。stream 首字 30 秒、总 300 秒；non-stream 仅总 300 秒。provider error 原地重试且失败前序 attempt 免计费；其它重试计费。失败不得改写为业务 miss/FP |
| resume/identity | v27 三轮目录和 judge manifest；当前 run manifest v2 | 当前 identity 更严格但不应改变方法语义 | 保留 commit、registry/schema/input hash 和原子写入等审计增强；它们只防止旧产物混入，不新增 method/judge 资格门或语义分支 |

## 唯一允许保留的新层

1. `four-family-19-core.v1` 注册表、冻结谓词语义和最小输入；
2. owned、无 Python `inspect`/`pyfcstm.inspect`/旧 `inspect_*` 依赖的解析与
   inspection-equivalent facts；
3. 新 19 谓词 lowering/compiler/backend；
4. W2 的完整 logic、binding、formal program/hash、model/input hash、真实 backend
   result、terminal state、counterexample/trace、source attribution、reason/basis、
   retry/usage/cost/environment 审计；
5. 不改变 v27 method/judge 语义的 run identity、原子落盘和审计 hash/path。

这些信息不得扩大 judge 输入，不得新增谓词，不得改变 D/W/L、release 或统计口径。

## Provider-free 对拍门

实现必须用测试证明：

1. 普通 pair 的逻辑调用形态固定为 `1 contract + 2 discovery grounding + 1 D`
   （D 有非法子集时再加一次 targeted repair）；
2. 三轮互不读取前一轮 release；
3. stage 顺序严格为七个 v27 stage，candidate 审计不新增图节点；
4. judge 固定为 `1 pair-wide + 0/1 shape correction`，不存在 partition、token gate
   或 atomic relation 调用；
5. 空候选不制造 issue；单 obligation 失败不抹掉其它合法 release；
6. judge prompt 不含 stage receipt、compiler/backend payload 或完整 W2 bundle；
7. 输入 manifest 能追溯全部 v27 闭包，prompt projection 没有静默截断；
8. 所有 Pydantic 模型对象和模型输出单元都有非空 reason/basis。
