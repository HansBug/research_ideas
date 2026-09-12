# v25 五格对齐审计

## 审计对象

审计对象是目录内五份 `claude-opus-4-7` record，来源为 `runs/paper1/witness-search/fivecase-v25-basis-contract/`。审计只做人工“同位置 + 同性质”台账匹配和证据完整性检查，不把 method D 当作 reference truth，不使用字符串相似度、embedding 或未匹配即 FP 的规则。

## v25 方法表

这张表只报告本次 `v25-basis-contract` 单次 pilot，不混入 X1v2 的六格历史结果；hit 是人工按“同位置 + 同性质”保守对齐。

| pair | finding facet | report cluster | accepted | confirmed | ledger hit | L2 hit | 明确 semantic FP | 方法 USD | input/output token |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `0004` | 8 | 8 | 6 | 3 | 3/3 | 2/2 | 0 | 0.484172 | 77,705 / 13,048 |
| `0023` | 12 | 12 | 9 | 3 | 3/3 | 3/3 | 0 | 0.622498 | 65,766 / 11,729 |
| `0053` | 13 | 9 | 7 | 2 | 1/3 | 0/2 | 0 | 0.631052 | 79,361 / 13,095 |
| `0046` | 16 | 15 | 12 | 0 | 4/4 | 1/1 | 0 | 0.656107 | 87,857 / 17,895 |
| `0029` | 21 | 20 | 17 | 5 | 7/8 | 3/3 | 0 | 0.991507 | 114,042 / 26,074 |
| 合计 | **70** | **64** | **51** | **13** | **18/21** | **9/11** | **0 个明确** | **3.385336** | **424,731 / 81,841** |

## X1v2 baseline 表

这张表只报告 X1v2：`唯一 hit` 与 `L2 hit` 来自 `discover_matrix/ledger_v2/x1v2_grid.json` 的六格历史网格，即该条目在六次生成中至少命中一次；`cost-only emitted` 来自同日单次运行 `runs/paper1/x1-baseline-cost/*-opus47-current/record.json`，只用于成本和输出规模，不把 emitted 数当 hit。

| pair | 台账条数 | 六格唯一 hit | 六格 L2 hit | cost-only emitted | X1v2 USD | input/output token |
|---|---:|---:|---:|---:|---:|---:|
| `0004` | 3 | 1/3 | 0/2 | 4 | 0.034825 | 2,190 / 955 |
| `0023` | 3 | 1/3 | 1/3 | 4 | 0.028975 | 1,625 / 834 |
| `0053` | 3 | 2/3 | 1/2 | 3 | 0.027000 | 1,660 / 748 |
| `0046` | 4 | 2/4 | 0/1 | 7 | 0.047950 | 1,790 / 1,560 |
| `0029` | 8 | 8/8 | 3/3 | 12 | 0.066800 | 3,120 / 2,048 |
| 合计 | **21** | **14/21** | **5/11** | **30** | **0.205550** | **10,385 / 6,145** |

方法成本相对同日 cost-only X1v2 的逐格倍率为 `0004=13.9030×`、`0023=21.4840×`、`0053=23.3723×`、`0046=13.6831×`、`0029=14.8429×`，总倍率 `16.47×`；五格均低于 `25×`。两张表的运行次数、冻结版本和 matching 角色不同，不能直接当作 paired significance。

## 逐条 ledger checklist

下面仍按同一台账顺序列出两边，但物理上拆成两张表：第一张只记录本次 `v25-basis-contract`，第二张只记录 X1v2 六格历史网格。这样逐条 `✅/❌` 可以对照，而不会把一侧的 finding、成本或命中口径混进另一侧。

### v25 本次五格逐条表

本表只记录本次单次 pilot 的保守 hit；每个 finding key 和 W/D/L 细节都可在同目录 JSON 中追溯。

| pair | ledger item | D/L | v25 本次 |
|---|---|---|---|
| `0004` | `EIS-0004-01` | D2/L0 | ✅ |
| `0004` | `INS-0004-01` | D2/L2 | ✅ |
| `0004` | `INS-0004-02` | D2/L2 | ✅ |
| `0023` | `INS-0023-01` | D2/L2 | ✅ |
| `0023` | `INS-0023-02` | D2/L2 | ✅ |
| `0023` | `INS-0023-03` | D2/L2 | ✅ |
| `0053` | `DIFF-0053-01` | D2/L2 | ❌ |
| `0053` | `EIS-0053-01` | D2/L0 | ✅ |
| `0053` | `INS-0053-02` | D2/L2 | ❌ |
| `0046` | `EIS-0046-01` | D2/L0 | ✅ |
| `0046` | `EIS-0046-02` | D1/L1 | ✅ |
| `0046` | `INS-0046-03` | D2/L2 | ✅ |
| `0046` | `VU-0046-01` | D1/L0 | ✅ |
| `0029` | `DIFF-0029-06` | D1/L0 | ❌ |
| `0029` | `EIS-0029-01` | D2/L1 | ✅ |
| `0029` | `EIS-0029-02` | D1/L1 | ✅ |
| `0029` | `EIS-0029-03` | D2/L1 | ✅ |
| `0029` | `EIS-0029-04` | D2/L0 | ✅ |
| `0029` | `EIS-0029-05` | D2/L2 | ✅ |
| `0029` | `INS-0029-01` | D2/L2 | ✅ |
| `0029` | `INS-0029-05` | D2/L2 | ✅ |

### X1v2 六格 baseline 逐条表

本表只记录该台账条目在 X1v2 六格历史网格中是否至少命中一次；`✅(n/6)` 保留六格命中次数，避免把一次命中误读为稳定命中。

| pair | ledger item | D/L | X1v2 六格 baseline |
|---|---|---|---|
| `0004` | `EIS-0004-01` | D2/L0 | ✅(6/6) |
| `0004` | `INS-0004-01` | D2/L2 | ❌(0/6) |
| `0004` | `INS-0004-02` | D2/L2 | ❌(0/6) |
| `0023` | `INS-0023-01` | D2/L2 | ✅(6/6) |
| `0023` | `INS-0023-02` | D2/L2 | ❌(0/6) |
| `0023` | `INS-0023-03` | D2/L2 | ❌(0/6) |
| `0053` | `DIFF-0053-01` | D2/L2 | ❌(0/6) |
| `0053` | `EIS-0053-01` | D2/L0 | ✅(6/6) |
| `0053` | `INS-0053-02` | D2/L2 | ✅(6/6) |
| `0046` | `EIS-0046-01` | D2/L0 | ❌(0/6) |
| `0046` | `EIS-0046-02` | D1/L1 | ✅(6/6) |
| `0046` | `INS-0046-03` | D2/L2 | ❌(0/6) |
| `0046` | `VU-0046-01` | D1/L0 | ✅(4/6) |
| `0029` | `DIFF-0029-06` | D1/L0 | ✅(2/6) |
| `0029` | `EIS-0029-01` | D2/L1 | ✅(2/6) |
| `0029` | `EIS-0029-02` | D1/L1 | ✅(6/6) |
| `0029` | `EIS-0029-03` | D2/L1 | ✅(6/6) |
| `0029` | `EIS-0029-04` | D2/L0 | ✅(4/6) |
| `0029` | `EIS-0029-05` | D2/L2 | ✅(1/6) |
| `0029` | `INS-0029-01` | D2/L2 | ✅(1/6) |
| `0029` | `INS-0029-05` | D2/L2 | ✅(1/6) |

## 未计入与证据边界

未强行计入 `DIFF-0053-01`、`INS-0053-02` 和 `DIFF-0029-06`；`EIS-0029-05` 的 `tr_0026` scope-route 证据虽更直接，但仍按 exact matching 保守处理。`0023` 的普通 transition/deadlock 重复或语义越界、`0053` 的 parent-entry/compiler entry-deadlock 重叠、`0046` 的 region/count 解释、`0029` 的 D1 guard/exit/finish/scope-route hypothesis 都是需要环外 blind judge 的 FP 风险，而非已经证实的 FP。

W2 的准入是 `typed Evidence Program + 真实 terminal counterexample + FCSTM/assertion hash + source causality certificate + semantic-binding receipt`；W1 只要求具体定位或 unsupported evidence，W0 只保留可审计自然语言假设。`confirmed` 还要求 D2 和安全 source attribution，因此 accepted 与 confirmed 必须分别统计。两张逐条表只提供命中对照，不把 baseline 的结果回灌到 v25 的 finding 或 W/D/L 判定。

## 完整性检查

五格 `semantic_provenance_audit.errors` 均为空，所有真实调用均完成，未发生 provider/schema failure。历史 X1v2 六格网格按这五个 pair 聚合为 `14/21` unique hit、`5/11` L2 hit；同日 cost-only baseline 的 emitted 数依次为 `4/4/3/7/12`，成本依次为 `$0.034825/$0.028975/$0.027000/$0.047950/$0.066800`，合计 `$0.205550`，但这些单次 raw issue 尚未完成环外逐格 hit matching。`basis`、`observed_fact`、D 的 `rationale` 和各阶段 `reason` 只服务于审计、复盘和 debug，不参与 assertion、W/L、D 合同或 dedup 的确定性语义控制；改变这些散文字段而保持 formal Goal、exact binding 和制品不变，不应改变 compiled assertion/hash/verdict/W/L/source certificate。

## 结论

v25 证明的是原型链条可以在五个代表性 pair 上完整运行并保存可重放证据，不能证明完整台账上的 overall hit、precision、false positive 或统计显著性。下一次正式评测必须冻结同一代码和 matching 协议，在所有 54 pair 上同时运行方法与同模型 X1v2，并由 CLI 写入 model-matched eligibility。
