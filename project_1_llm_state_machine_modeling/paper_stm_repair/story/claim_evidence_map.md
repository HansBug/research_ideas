# claim_evidence_map.md — paper1 claim-evidence map

## 1. Claim strength 口径

| 强度 | 含义 |
|---|---|
| `task framing supported` | 可用于说明本文研究什么问题，但不说明方法效果。 |
| `infrastructure supported` | 有代码 / pipeline / artifact 支撑基础设施存在，但不说明 repair gain。 |
| `method design supported` | 有导师讨论、story、pipeline 资产和 PR contract 支撑方法设计方向，但尚未证明效果。 |
| `protocol planning supported` | 有计划、contract 或审计纪律支撑后续协议，但尚非结果。 |
| `future empirical claim only` | 需要 pilot / 正式实验后才可写强 claim。 |
| `forbidden` | 当前证据不支持或已被战略转向否定。 |

## 2. Active claims

| ID | Claim | 当前证据 | 强度 | 可写方式 | 禁止写法 |
|---|---|---|---|---|---|
| C1 | 本文研究 existing raw/source STM artifact 上的 source-level behavioral issue discovery and closure。 | [paper_story.md](./paper_story.md), [task_boundary.md](./task_boundary.md), [../evidence/ledgers/paper1_strategy_asset_map.md](../evidence/ledgers/paper1_strategy_asset_map.md), [../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md](../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md)。 | task framing supported | “We study / frame ...” | “We solve all STM correctness problems.” |
| C2 | paper1 的主贡献应是 feedback-driven LLM refinement loop，而不是状态机表达语言、ledger 或 audit protocol。 | [paper_story.md](./paper_story.md), [../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md](../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md)。 | method design supported | “We contribute a feedback-driven loop for discovering, repairing, and closing source-level behavioral issues.” | “We contribute an audit ledger / evidence bookkeeping framework.” |
| C3 | 中间可执行语义表示用于把 diagnostics / inspect、simulation / probes、formal verification / checks 接入 loop。 | [../pipeline/](../pipeline/) conversion / representation / readiness assets。 | infrastructure supported | “We use an intermediate executable semantic representation to enable executable feedback in the loop.” | “fcstm is the contribution / better language.” |
| C4 | candidate issue 与 confirmed issue 必须分离。 | [task_boundary.md](./task_boundary.md), [terminology_policy.md](./terminology_policy.md), asset map attribution boundary。 | protocol planning supported | “The workflow separates candidate discovery from strict confirmation.” | “Diagnostic hit equals confirmed issue.” |
| C5 | issue-grounded repair 应回到 raw/source 层输出 patch bundle 或 final raw/source `STM_k`。 | [paper_story.md](./paper_story.md), [task_boundary.md](./task_boundary.md), [#100 umbrella PR](https://github.com/HansBug/research_ideas/pull/100) downstream map, and [paper1_strategy_asset_map.md](../evidence/ledgers/paper1_strategy_asset_map.md)。 | protocol planning supported | “The planned loop requires source-level projection before final evaluation.” | “Intermediate model repair alone proves closure.” |
| C6 | 方法能发现并闭合更多 source-level behavioral issues。 | 目前无真实 pilot / main experiment。 | future empirical claim only | 只能写成 future RQ 或 planned evaluation。 | 当前写成已证明 result。 |
| C7 | baseline / rubric 应等 pilot 后冻结。 | [paper1_strategy_asset_map.md](../evidence/ledgers/paper1_strategy_asset_map.md) and [#100 umbrella PR](https://github.com/HansBug/research_ideas/pull/100)。 | protocol planning supported | “We defer final rubric and baseline contract until pilot output shapes are known.” | “Baseline contract is finalized in story reset.” |

## 3. Forbidden claims

| Forbidden claim | 为什么禁止 | 替代表述 |
|---|---|---|
| Better STM 是 active headline evaluation framework。 | 2026-07-07 战略转向已 supersede 该主框架。 | source-level issue discovery and closure。 |
| 本文贡献是 ledger / audit / evidence bookkeeping。 | ledger 和 audit 是可信评价与可复现证据链，不是导师确认的 headline contribution。 | contribution is the feedback-driven loop plus executable feedback integration. |
| 本文证明 `fcstm` / `pyfcstm` 比 PlantUML / SysML-like 表达更好。 | paper1 contribution 是 loop + simulation / verification feedback，不是 modeling language。 | `fcstm` is an intermediate executable semantic representation. |
| conversion / normalization / lowering success 是 repair gain。 | 这属于输入准备和表示桥，非 repair-loop 内贡献。 | 只作为 infrastructure readiness。 |
| constructed `STM_k` dry-run 证明方法有效。 | constructed cases 是 calibration / anti-gaming，不是真实 repair-loop 输出。 | historical calibration only。 |
| folded event / ugly expression 自动等于模型错误。 | expression debt 可能只是表示限制或建模风格，需 source-level confirmation。 | candidate symptom requiring confirmation。 |
| final metrics / baseline / judge prompt 已冻结。 | 必须等 pilot 真实输出形态。 | post-pilot freeze。 |

## 4. Reviewer challenge 对照

| Reviewer challenge | 当前回答 |
|---|---|
| 你是不是在证明 fcstm 更好？ | 不是。fcstm 是中间执行介质，贡献是 feedback-driven LLM refinement loop 与 simulation / formal-verification-enabled feedback integration。 |
| 你是不是把审计表 / ledger 当贡献？ | 不是。ledger / audit 只用于评价、可复现和防止错误归因；主贡献仍是 loop 与 executable feedback 如何驱动 issue discovery / repair。 |
| 如果 PlantUML 表达不了 guard，怎么比较？ | 不比较语言优劣；我们回到 raw/source 层说明原模型行为问题和修复证据。 |
| folded event 算不算问题？ | 只算 candidate symptom；必须经 `NL + source + behavior evidence` 确认。 |
| 评价和 baseline 怎么公平？ | 等 pilot 产出 raw/source `STM_k` 或 patch bundle 后冻结 rubric / baseline contract。 |
| 现在有什么实验证据？ | 目前只有 infrastructure / protocol / asset map；method effectiveness 仍是 future empirical claim。 |

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 21:20:00 | claim map 从 Better STM 改为 source-level issue lifecycle；method effectiveness 降为 future empirical claim。 |
