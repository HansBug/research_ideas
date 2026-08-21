# v25 五格 pilot 报告

## 1. 定位

本报告记录 `v25-basis-contract` 五格真实运行的工程证据和保守台账对齐，不承担完整 54 pair、145 条台账的正式效果结论。方法语义来自领域来源和 UML/状态机/测试预言机研究，真实 pair 只用于检查冻结实现能否执行、留证和降级；不得用本轮结果反向定义 obligation、Goal 或 prompt。

## 2. 运行边界

冻结 profile 是 `claude-opus-4-7`，五份原始 record 的审计副本位于 `runs/paper1/witness-search/final-pilot-v25-opus47/`，来源运行目录是 `runs/paper1/witness-search/fivecase-v25-basis-contract/`。每格均完成 LLM-A、两个互补 LLM-B、整格一次 LLM-C D 裁决以及必要的定向 D repair；没有 provider error 或 schema failure。每份 record 保存 prompt、raw/parsed output、call id、usage、价格、formal execution receipt、source certificate、D/W/L、accepted/confirmed 列表和 provenance audit。

## 3. 本次 v25 方法表

本表只负责本次 `v25-basis-contract` 单次 pilot，不放入 X1v2 字段。

| pair | finding facet | report cluster | accepted report | strict confirmed report | ledger hit | L2 hit | 方法成本（美元） | input/output token | provenance audit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `0004` | 8 | 8 | 6 | 3 | 3/3 | 2/2 | 0.484172 | 77,705 / 13,048 | `[]` |
| `0023` | 12 | 12 | 9 | 3 | 3/3 | 3/3 | 0.622498 | 65,766 / 11,729 | `[]` |
| `0053` | 13 | 9 | 7 | 2 | 1/3 | 0/2 | 0.631052 | 79,361 / 13,095 | `[]` |
| `0046` | 16 | 15 | 12 | 0 | 4/4 | 1/1 | 0.656107 | 87,857 / 17,895 | `[]` |
| `0029` | 21 | 20 | 17 | 5 | 7/8 | 3/3 | 0.991507 | 114,042 / 26,074 | `[]` |
| 合计 | **70** | **64** | **51** | **13** | **18/21** | **9/11** | **3.385336** | **424,731 / 81,841** | 五格均通过 |

## 4. X1v2 baseline 表

本表只负责 X1v2，不放入 v25 finding/accepted/confirmed 字段。六格唯一 hit 来自 `discover_matrix/ledger_v2/x1v2_grid.json`；成本和 emitted 数来自同日 cost-only record，emitted 不是 hit。

| pair | 台账条数 | 六格唯一 hit | 六格 L2 hit | cost-only emitted | X1v2 成本（美元） | input/output token |
|---|---:|---:|---:|---:|---:|---:|
| `0004` | 3 | 1/3 | 0/2 | 4 | 0.034825 | 2,190 / 955 |
| `0023` | 3 | 1/3 | 1/3 | 4 | 0.028975 | 1,625 / 834 |
| `0053` | 3 | 2/3 | 1/2 | 3 | 0.027000 | 1,660 / 748 |
| `0046` | 4 | 2/4 | 0/1 | 7 | 0.047950 | 1,790 / 1,560 |
| `0029` | 8 | 8/8 | 3/3 | 12 | 0.066800 | 3,120 / 2,048 |
| 合计 | **21** | **14/21** | **5/11** | **30** | **0.205550** | **10,385 / 6,145** |

`accepted report` 的准入是 `D1/D2` 且没有明确 source certificate 反证；`confirmed report` 是其严格子集，必须同时满足 `D2 ∧ W2 ∧ safe source attribution`。因此 accepted 可以包含 W1/W0 provisional issue，confirmed 不是唯一发布集合。五格共有 190,744 cache-read token 和 59,203 cache-write token；美元计价使用配置中的 input/output/cache-read/cache-write 四类价格，非 provider 错误的 repair attempt 均计费，只有确实触发下一次调用的 typed provider retry 前序 attempt 才可豁免。

## 5. W2 证据形状

每个 W2 facet 都要求真实执行的 Evidence Program、确切 FCSTM/source artifact hash、compiled assertion hash、terminal counterexample、observed values/trace/path/cut/SCC/SMT model（按后端适用）、source causality certificate 和 semantic-binding receipt。`causal_dual_certificate` 表示 FCSTM 反例与作者源 cause 之间存在记录的 compiler bridge；`source_localized` 只表示定位到源/制品元素，最高是 W1；`unattributed` 表示执行后果没有安全作者源归因，不能进入 confirmed。程序只在预条件成立且 primary assertion 失败时发布，满足或 exception 只保留 attempt/coverage-gap，不通过改写 Goal 追逐 W2。

本轮 strict confirmed 的代表性 W2 类型包括：`0004` 的 `Stopping`/`EmergencyStopping` reachable deadlock 和 `DoorsClosing` initial target；`0023` 的三个正交 region deadlock；`0053` 的 `PumpControl` entry deadlock 和三个初始可达性义务合并报告；`0029` 的 `HighwayMode`/`UrbanMode` initial contract、`AutonomousMode` containment、`HighwayMode.FinishState` stable termination 和 `CollisionAvoidance` unreachable component。每条具体 facet 的 assertion、hash、terminal verdict、source certificate 和自然语言理由都在对应 JSON 的 `finding_records`、`outcomes` 与 `accepted_report_issues` 中，不能以本表的计数替代原始证据。

## 6. 保守台账对齐

目前人工逐项对齐口径是 Overall `18/21`、L2 `9/11`；逐 pair 为 `0004=3/3`（L2 2/2）、`0023=3/3`（L2 3/3）、`0053=1/3`（L2 0/2）、`0046=4/4`（L2 1/1）、`0029=7/8`（L2 3/3）。未强行计入 `DIFF-0053-01`、`INS-0053-02`，以及 `DIFF-0029-06` 与 v25 的 `wrong_scope_route` 证据性质不完全相同的情况。`EIS-0029-05` 虽有更直接的 `tr_0026` scope-route 证据，本轮仍按 exact matching 保守计数，不把 related property 当作 exact hit。

这些数字是当前人工审计的方向性结果，不是环外 blind judge 的正式 precision。没有发现明确 semantic false positive，只能记为“观测到 0 个明确 FP”；0023 的 ordinary transition/deadlock 重复或语义越界、0053 的 parent-entry 与 compiler entry-deadlock 重叠、0046 的 region/count 解释、0029 的 D1 guard/exit/finish/scope-route hypothesis 仍需环外 judge。未匹配 report 不能仅凭未匹配自动判为 false positive。

## 7. 成本与资格

历史 X1v2 六格台账网格的逐条真值来自 `discover_matrix/ledger_v2/x1v2_grid.json`，按 pair 聚合得到上表的 `14/21` unique item 和 `5/11` L2 item；它是六次 X1v2 生成的“是否至少命中一次”上界式描述，不是本轮单次 baseline 的同 run 对照。为提供成本同口径，本轮另保存了同日、同模型、单次 X1v2 cost-only record：`0004/0023/0053/0046/0029` 分别输出 4/4/3/7/12 条 issue，成本分别为 `$0.034825/$0.028975/$0.027000/$0.047950/$0.066800`，合计 `$0.205550`；这些 raw issue 尚未用环外 blind judge 做逐格正式 hit matching，不能把 emitted 数直接当 hit。v25 方法逐格成本倍率依次为 `13.9030×/21.4840×/23.3723×/13.6831×/14.8429×`，均低于 `25×`，总倍率为 `16.47×`。本轮 CLI 没有传入 `--matched-x1v2-record`，所以每份 JSON 的内置 `model_matched_x1v2_comparison` 仍标为 `eligible=false`；在下一轮冻结 benchmark 中必须由 CLI 自动写入匹配记录后才能把资格置为 true。成本达标不等于效果达标，五格不能宣称整体显著超过 X1v2。

## 8. 方法状态与下一步

v25 已验证 basis/observed_fact/rationale 审计字段、整格 D、局部 D repair、精确 dedup、source-entry compiler bridge、W2/W1/W0 降级和四类美元计价能共同落盘；自然语言理由不参与 deterministic semantic control flow。仍未完成的是同一冻结版本上的完整 54 pair 评测、环外 blind matching/precision、逐条 145-item feasibility audit 和正式 pair-clustered uncertainty。论文只能在这些门通过后报告整体 hit、L0/L1/L2、D×L、W2 fraction、false positive 和显著性。
