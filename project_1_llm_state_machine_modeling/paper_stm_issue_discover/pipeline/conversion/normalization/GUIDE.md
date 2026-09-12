# R3.1 normalization/GUIDE.md

## 1. 边界

- 本目录只定义 PlantUML pre-SCXML normalization；不处理 Umple / TTool。
- normalization 只改变进入官方 PlantUML 的候选文件，不改一手 raw assets。
- canonical STM 只能来自官方 PlantUML `-tscxml` 产生的 SCXML，再由 R3 SCXML adapter 解析。
- normalization/recovery 的收益只属于 conversion eligibility，不得计入 Better STM repair loop。

## 2. 规则注册纪律

所有规则必须登记在 [plantuml_rules.json](./plantuml_rules.json)，并包含：

| 字段 | 含义 |
|---|---|
| `rule_id` | 稳定规则编号，格式 `PUML.NORM.*` |
| `description_zh` | 中文说明 |
| `semantic_risk` | `low_medium / medium / medium_high / high` 等语义风险 |
| `risk_tier` | `low_risk` 或 `high_risk` |
| `main_eligibility_default` | 默认是否可进入主 eligibility |
| `loss_types` | 可能损失类型，如 `syntax / guard / action / hierarchy / semantic` |
| `claim_policy` | 论文 claim 使用边界 |

新增规则时必须同步更新 schema、测试与 recovery report 解释，不得只改代码。

## 3. Ledger 字段纪律

[../reports/plantuml_normalization_ledger.jsonl](../reports/plantuml_normalization_ledger.jsonl) 每行记录一次变换，至少包含：

- `run_id / seed_id / pair_id / row_index / change_index`
- `raw_sha256 / normalized_sha256 / normalized_candidate_path`
- `rule_id / line / span / before / after / kind / rationale`
- `semantic_risk / risk_tier / loss_type / needs_manual_review`
- `technical_scxml_pass_all_rules / low_risk_scxml_pass / main_eligibility_included`
- `semantic_preservation_pass / semantic_preservation_audit_status`
- `concurrency_degraded / repair_contribution_allowed=false`

## 4. Eligibility gate

| 条件 | 结果 |
|---|---|
| raw already SCXML-pass | 作为 naturally-converted profile；不计 recovered |
| normalized SCXML-pass + only low-risk rules + source-level semantic audit pass | `low_risk_scxml_pass=true`，可进入 `main_eligibility_included` |
| normalized SCXML-pass + only low-risk rules + semantic audit fail / missing | 只能作为待复核风险，不得进入 `main_eligibility_included` |
| normalized SCXML-pass + high-risk rules | 只计 `technical_scxml_pass_all_rules`，不得默认进入主 eligibility |
| fork/join 降级 | 必须 `concurrency_degraded=true` 且 `main_eligibility_included=false` |
| endpoint 内嵌 `[*]` 伪状态标记 | 必须按 `PUML.NORM.alias_embedded_pseudostate_marker` 记为高风险；即使 source signature 字面保持，也不得进入 `main_eligibility_included` |
| normalized 后仍失败 | 保留失败 preflight，不生成 canonical |

## 5. 测试要求

- normalizer 单元测试必须覆盖 quoted endpoint、多词 endpoint、`stm` heading、高风险 action/guard/dependency/fork 规则。
- recovery report 测试必须验证 schema、三种恢复率字段、高风险排除、semantic preservation gate、LLMS-EMP gate、raw immutability。
- fake PlantUML 测试必须证明 CLI 真调用 `-checkonly` / `-tscxml`，而不是复用 fixture。
- committed report 测试必须证明 `main_eligibility_included=true` 的条目均有 `semantic_preservation_pass=true`，并且高基数 artifact 只以 `workdir.zip` 进入 [../artifacts/](../artifacts/)。

## 6. Artifact 归档纪律

- R3.1 全量 raw / normalized `.puml` 与官方 `.scxml` 必须保存在 [../artifacts/plantuml_recovery/r3_1_committed/workdir.zip](../artifacts/plantuml_recovery/r3_1_committed/workdir.zip)。
- [../artifacts/plantuml_recovery/r3_1_committed/manifest.json](../artifacts/plantuml_recovery/r3_1_committed/manifest.json) 必须记录 file count、目录分布、后缀分布、report / ledger 路径和复验命令。
- 解压态 `workdir/` 只用于本地人工检查，必须被忽略，不得提交。
- 根目录 `runs/` 不再作为 R3.1 committed recovery artifact 路径；若存在旧散文件，应迁移为 archive 或删除。
