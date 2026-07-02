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
