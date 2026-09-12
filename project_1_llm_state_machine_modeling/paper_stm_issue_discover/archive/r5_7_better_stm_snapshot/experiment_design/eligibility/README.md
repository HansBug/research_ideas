# eligibility/ — 纳入排除规则职责入口

本目录预留 seed、conversion、run record、schema-invalid、replay-invalid、partial run、provider failure 等 eligibility 规则。

当前状态：仅冻结职责入口，尚未冻结正式 eligibility 协议。

后续新增规则时必须说明：适用对象、纳入条件、排除条件、failure handling、是否进入主结果统计，以及对应 run record 证据字段。

## R5.7.1 已冻结的前置纪律

R5.7.1 已在 [../evaluation_logic.md](../evaluation_logic.md) 中冻结 **A 层 artifact-level 可评价性门槛**：A 层不是 dataset-level 纳入标准，而是单个 `STM_0` 或 `STM_k` 是否有资格进入后续 Better STM 判定的前置门。

| 对象 | A 层作用 | A-fail 去向 | A-pass 不能说明 |
|---|---|---|---|
| `STM_0` | 判断初始制品是否具备足够结构、来源、诊断和证据链，可作为 repair 起点。 | readiness / failure / limitation ledger。 | 初始模型语义正确。 |
| `STM_k` | 判断候选制品是否可解析、可审计、无基础阻塞，可进入 Better STM 语义裁决。 | repair failure / rollback / unknown ledger。 | 候选模型更优。 |

后续正式 eligibility 协议必须继续区分 pre-registered pool、scope pool、evaluation-eligible pool 与 success / failure / unknown 分母；不得把 T0 `8 clusters / 48 pairs` 直接写成最终 eligible 或 success denominator。

## R5.7.2 已冻结的 run validity 输出

R5.7.2 在 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 中把 A 层扩展为 Better STM gate 链的一部分。后续 eligibility 协议必须至少保留三层状态，不得只写一个 `eligible=true/false`：

| 层 | 字段 | 值 | 去向 |
|---|---|---|---|
| scope routing | `scope_routing_status` | `main_t0` / `caveat_t05` / `stress_t1` / `excluded_out_of_scope` | 决定主表、caveat、stress 或排除 ledger。 |
| run validity | `run_validity_status` | `valid_run` / `stm0_readiness_failure` / `stmk_repair_failure` / `protocol_or_provenance_invalid` | 决定是否可进入 Better 语义裁决。 |
| Better outcome | `better_adjudication_outcome` | `better` / `not_better` / `partial` / `unknown` | 只对 `valid_run` 且 scope 合适的对象裁决。 |

关键纪律：

1. `STM_0` A-fail 是 pre-repair readiness / limitation，不是 repair failure。
2. `STM_k` A-fail 是 repair output failure / rollback / unknown，不得进入 Better success denominator。
3. `protocol_or_provenance_invalid` 包括 change ledger 缺失、baseline/candidate hash 缺失、raw -> canonical 收益被混进 repair gain、run record 不完整等情况。
4. 不再把 `not_attributable` 作为常规 Better outcome；不可归因是协议 / provenance invalid 或 attribution ledger 中的禁入原因。
5. `T0 headline main = 8 clusters / 48 pairs` 仍只是 scope / pre-eligibility 上限；最终 eligible / success denominator 必须等待 R7/R8 正式协议和真实 run。
