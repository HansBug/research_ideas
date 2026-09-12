# 人工评测 v2 数据模型

正式审计数据使用 `paper_stm_evaluation.manual_adjudication` 中的 Pydantic 模型。每个模型
有 docstring；每个字段使用 `Field(description=...)`。JSON 是 canonical source，TSV 只是
固定列的镜像。

## 核心实体

- `RawInventory` / `RawReportRef`：从冻结 raw 机械枚举 `162` cells、`1271` v60 reports 和
  `512` X1v2 findings。baseline raw 没有 report ID，inventory 使用既有 archive witness 的
  `case/round/index` 身份交叉核对，不使用语义标签。
- `ReportDecision`：一条 raw report/finding 的人工最终裁定。它保存 raw path/pointer/index/hash、
  fact status、D/A、validity、dense relation、W witness、reason、basis、source refs 和三方
  人工 review attestation。
- `RelationDecision`：每个 report 对每一个 expected issue 的一次 `FULL_MATCH`、
  `PARTIAL_MATCH` 或 `NO_MATCH`。relation 不能只用跨 expected 的总理由替代。
- `RelationAuditSet`：`relation_decisions.json` 的 archive-level dense projection；必须逐行
  与 `ReportDecision.relations` 的 report、expected、relation、reason、basis 和 source refs
  相同，不能只保存汇总计数。
- `GroupDecision`：人工确认的 substantive group。identity 至少由 `side`、`pair_id` 和
  `canonical_group_key` 组成；不会由文本相似度、状态名或 expected ID 自动生成。
- `GroupDecisionSet`：`group_decisions.json` 的集合 envelope；只允许同一 side、同一 pair
  内的最终 `N/I` decision 归组，每条 N/I decision 必须恰好属于一个 group。
- `ReviewBlocker` / `HumanReview`：记录证据不足、冲突、blind 首轮、解盲、二审和仲裁。
  `FINAL` 必须没有 blocker，并且 `human_confirmation=true`。

## 确定性闭合

后端只从 D/A 与 dense relation 派生 validity 和 K/N/I：

| 条件 | validity | K/N/I |
| --- | --- | --- |
| `D2/D1` 且存在 `FULL/PARTIAL` | `VALID_KNOWN` | `K` |
| `D2/D1` 且全为 `NO_MATCH` | `VALID_NOVEL` | `N` |
| `D0/A0` | `INVALID`，relation 强制全 `NO_MATCH` | `I` |

`A0` 只能使用 `FALSE_POSITIVE` 或 `NOT_A_DEFECT_CLAIM`；X1v2 不能使用后者。W2 必须
有原始 executable object、精确 artifact hash、terminal result 和 execution receipt；W
不参与 validity、relation、hit 或 FP。`PARTIAL_MATCH` 是 known coverage，但不计主 hit，
也不计 FP。`ledger_ids` 只列 `FULL_MATCH` 的 expected ID；PARTIAL-only 的 `K` decision
合法地保持空 `ledger_ids`，由关系明细保留其 supported coverage。

`ExecutableObject` 以带 hash 的 typed serialization 保存原始 executable witness：typed
inputs、program、完整 payload、artifact 和 backend 都必须可核对，不能用无 schema 的任意
dict 替代。`relation_decisions.json`、`group_decisions.json`、汇总、predicate audit 和
review log 都必须包含非空 `schema` 及其声明的集合字段；validator 会读取并校验这些 envelope，
而不是只检查文件是否存在。

支持文件的集合字段固定如下：`hit_max_witness.json` 使用 `witnesses`，覆盖两侧每个
`(expected_id, round)`；`summary.json` 使用 `sides`，每侧必须回报 report、D/A、validity、
K/N/I、W 和 relation 计数；`reference_ledger_aggregate.json` 使用 `aggregates`；
`predicate_witness_audit.json` 使用 `sides`，current 的 `planned_scope` 必须来自冻结
evaluator summary，且 `predicate_rows` 覆盖 registry 的全部 19 个 ID；每行分开保存
`planned_in_frozen_scope` 与 `report_bound_plan_count`，不能用逐报告 usage 冒充 planned scope。
X1v2 必须显式标记 `not_applicable`；`review_log.json` 使用
`entries`，每个 report 恰好一条，并与 decision 中的三方人工 attestation 一致。

`reviewer_input_projection.jsonl` 不是 canonical decision。它是 raw-first independent
proposal 的 sealed input：每行只含 arm/pair token、round、slot、规范化 claim/reason/location
和共同作者源。`location_text` 在两侧固定为空，避免 current `element_refs` 与 baseline `where`
的 producer schema 泄露。它不得含 report index、raw JSON Pointer、raw target hash、
producer-specific location、provider/model/prompt、expected、predicate、receipt、W 或任何 semantic label。每个
pair/round 的两臂 slot 集合必须完全相同；空 padding slot 仅表示该臂没有 frozen report，
不对应 report、finding、decision 或任何统计分母。validator 同时检查 allowlist、row hash、
source hash 和 slot 对称性。`reviewer_unblind_mapping.json` 是 raw-first 不可见的 final audit
provenance，独立 proposal 提交后才恢复 raw target hash 和 identity。

## FINAL 准入

`validate_manual_adjudication.py` 先重新枚举 raw archive，核对 `1271/512`、每个 report
index、JSON Pointer、side/pair/round 和 SHA-256，再读取双侧 decision set、relation、witness、
group、summary、reference aggregate、predicate audit、review log、schema、README 和 MANIFEST。
任一文件缺失、JSON/TSV 不一致、report ID 缺失、dense relation 不完整、source ref 不可定位、
blocker 未关闭或没有真实人工确认，命令都必须失败。
