# experiment_design/GUIDE.md — 后续实验设计维护规范

## 1. 总原则

本目录只维护 paper1 当前主线的实验设计纪律：**Discover once -> Repair full batch -> Confirm all dispositions -> Repair-Confirm until all chains close -> one-time raw/source closure / regression audit**。

旧 R5.7 / Better STM-facing 规则已经归档到 [../archive/r5_7_better_stm_snapshot/](../../r5_7_better_stm_snapshot/)。它们可以作为 historical / calibration / anti-pattern 参考，但不能直接作为 active guardrail、正式 metric、baseline contract 或 judge prompt。

## 2. Active protocol 必须围绕的对象

| 对象 | 必须回答的问题 | 最低证据 |
|---|---|---|
| candidate issue | 为什么怀疑 raw/source `STM_0` 存在行为问题？ | `NL`、raw/source element、intermediate diagnostics / simulation / check feedback、问题描述；具体字段见 [issue_lifecycle/issue_ledger_contract.md](./issue_lifecycle/issue_ledger_contract.md)。 |
| Discover root assessment | 该 root 是否有足够依据进入 `fix`，还是只能由 Repair reasoned reject？ | Discover 发布的 `confirmed/candidate_only` assessment、immutable checks、证据片段与 attribution boundary；v0 允许 `nl_grounded_behavioral_issue` 与 `raw_internal_inconsistency` 两条 confirmed path。 |
| repair/change | 本轮对每个 pending node 做了 `fix` 还是 `reject`，理由与实际改动是什么？ | 完整 disposition batch、change ledger、source trace、输入输出 hash、模型 diff、LLM / deterministic step 记录。 |
| B-confirm | 本轮每个 disposition 是否可接受；若不可接受，如何在同一 issue chain 上追加 successor？ | typed expected-outcome match、当前模型检查结果、完整自然语言理由、successor linkage 与因果记录。 |
| source trace | confirmed issue 的 raw/source 元素如何对应到中间表示元素？ | [source_trace/source_trace_contract.md](./source_trace/source_trace_contract.md)、trace ledger、negative attribution gate。 |
| canonical source export | accepted repair 如何进入 validated post-Confirm semantic-root bundle，并全量生成 fresh raw/source `STM_k`？ | accepted semantic delta、root correspondence、region/body/lifecycle/order、deletion tombstone、unsupported export 记录；不消费裸 `.fcstm`。 |
| closure / regression | B-final 后生成 canonical source artifact 时，问题是否闭合，是否引入新问题？ | final raw/source `STM_k`、semantic change/correspondence ledger、隐藏/独立审计、失败 / unknown 入账；B-confirm accept 不能单独冒充 source closure。 |

## 3. 禁止直接继承的 archived 内容

| archived 内容 | 为什么不能直接继承 | 若未来要复用怎么办 |
|---|---|---|
| Better STM gate / `can_claim_better_stm` | endpoint 已被战略校准覆盖。 | 在 `PR-eval-rubric` 重新定义为 issue closure / regression verdict。 |
| repair target taxonomy | 旧 taxonomy 面向 Better STM target，不等同 confirmed source-level issue。 | 已由 [issue_lifecycle/source_level_issue_definition.md](./issue_lifecycle/source_level_issue_definition.md) 重建为 v0 issue status / family；后续 pilot 后再扩展。 |
| objective metric framework | 旧指标围绕 Better STM gate。 | pilot 后基于真实 canonical source export / closure ledger 重建。 |
| constructed `STM_k` suite | 候选是人工 / 确定性构造，不是真实 repair-loop 输出。 | 只能作 leakage / anti-gaming calibration 参考。 |
| blind adjudication prompt / schema | 旧 prompt 裁决 Better STM，不裁决 source-level issue closure。 | 若需要 LLM judge，必须另建 source-level closure prompt 并做 blind / leakage 审计。 |
| `pipeline/evaluation/` schemas | 旧 schema 混合 R4/R5.7 gate。 | 若 diagnostic / scenario 字段仍有价值，必须在新 schema 中改名和重定义。 |

## 4. 后续新增文件规则

1. 新增 `README.md` / `SUMMARY.md` / `GUIDE.md` 或 schema 时，必须说明它属于 `draft`、`pilot-only`、`frozen protocol candidate` 还是 `formal experiment`。
2. 不得在 pilot 前冻结 final numeric thresholds、baseline contract、primary endpoint 或 judge prompt。
3. 不得把 archived dry-run 的 score、schema-valid、leakage=0、judge agreement 写成 repair effectiveness。
4. 每条实验 claim 都必须明确分母：pre-registered pool、scope pool、eligible issue、confirmed issue、repair attempt、closure-eligible issue 或 regression-audit unit。
5. partial / failed / unknown / out-of-scope / unsupported projection 必须入账，不能静默丢弃。

## 5. 与 story / pipeline 的分工

| 路径 | 职责 |
|---|---|
| [../story/](../../r8_discover_repair_story/story/) | 论文 thesis、contribution、claims-to-avoid、terminology。 |
| [../pipeline/](../../../pipeline/) | conversion / representation / readiness / future loop runtime 的机器制品。 |
| [../evidence/](../../../evidence/) | 资产清账、审计、trace / ledger 等可复现证据。 |
| [../archive/](../../) | superseded historical snapshots；不是 active truth。 |

若 story、pipeline 与 experiment design 对同一概念发生冲突，优先回到 2026-07-07 导师记录和 [../evidence/ledgers/paper1_strategy_asset_map.md](../evidence_ledgers/paper1_strategy_asset_map.md) 判断；不要用 archived Better STM wording 覆盖当前主线。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-17 00:32:36 | 对齐 Issue #152：区分 Discover root assessment、Repair disposition、B-confirm 决议与 C closure；删除 strict-confirm-before-repair / post-repair rediscovery 旧顺序。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 后同步 GUIDE：source trace v0 已定义，后续 projection / closure 必须消费 trace ledger 并尊重 negative attribution gate。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 后同步 GUIDE：candidate / confirmed issue 已有 v0 字段合同和两条 confirmed path，但仍不冻结 final metrics / baseline。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后重写 GUIDE：移除 active Better STM gate 维护纪律，改为 source-level issue lifecycle protocol 设计纪律。 |
