# v60/current 与 X1v2 baseline v3：公平对照结果

本文只使用 v60/current re-audit v4 和 X1v2 baseline v3。没有重新运行
method、Judge、provider、15x1 或 54x3。current v4 是对既有 pane5
source-first 证据的 raw/source/hash/relation 再验证；baseline v3 对原非 K
报告已完成逐条重审，原有 K 保持冻结。

## 口径

两侧都按同一顺序处理：读作者 source 和原始 report，判事实与 D/A，枚举该
pair 的全部 145 个 expected relation，机械派生 K/N/I，再只对最终 N 做归并。

| 档位/关系 | 定义 | 结果去向 |
| --- | --- | --- |
| D2 | source 中承重事实成立，有明确被违反义务，且没有存活的称职反读法 | K 或 N |
| D1 | 事实成立，至少两种完整、与 source 相容的称职读法仍会改变义务或归因判断 | K 或 N |
| D0 | 事实成立，但没有被违反义务，或设计解释正当 | I |
| A0 | 报告事实或归因在完整作者制品上不成立 | I |
| FULL | 与 expected 是同一缺陷实例和义务 | K，并贡献主 hit |
| PARTIAL | 支持同一较宽义务/家族，但不是同一 expected 实例 | K，进入 supported coverage，不贡献主 hit |
| NO | 没有可接受的该 expected 关系 | D2/D1 全 NO 时进入 N；I 必须全 NO |

W0/W1/W2 只表示证据强度。W2 需要 finding 自带 executable object、typed
input、精确 artifact hash、terminal result 和原始 receipt；Judge 后验不能升级
baseline W。predicate usage 与 predicate contribution 分开统计，也不参与 D/A
或 K/N/I。

## 主结果

| 指标 | v60/current | X1v2 baseline v3 | current - baseline |
| --- | ---: | ---: | ---: |
| reports | 1271 | 512 | +759 |
| K/N/I | 749 / 231 / 291 | 312 / 105 / 95 | +437 / +126 / +196 |
| D2/D1/D0/A0 | 721 / 259 / 120 / 171 | 342 / 75 / 85 / 10 | +379 / +184 / +35 / +161 |
| report precision | 980/1271 = 77.10% | 417/512 = 81.45% | -4.34 pp |
| report I rate | 291/1271 = 22.90% | 95/512 = 18.55% | +4.34 pp |

report precision 是本文主 precision：`(K reports + N reports) / all reports`。
它不把不同实体单位放进同一分母。

## Hit 与 supported coverage

hit@1 使用 145 expected x 3 rounds = 435 个去重 expected-round units；hit@3
按 145 个 expected ID 去重，hit@all 要求三个 round 都有 FULL。重复命中同一
expected ID 不增加 hit。

| 指标 | v60/current | X1v2 baseline v3 | current - baseline |
| --- | ---: | ---: | ---: |
| hit@1 FULL | 310/435 = 71.26% | 227/435 = 52.18% | +83 units; +19.08 pp |
| hit@3 FULL | 119/145 = 82.07% | 106/145 = 73.10% | +13 IDs; +8.97 pp |
| hit@all FULL | 86/145 = 59.31% | 46/145 = 31.72% | +40 IDs; +27.59 pp |
| supported coverage, round units | 337/435 = 77.47% | 264/435 = 60.69% | +73 units; +16.78 pp |
| supported coverage, unique IDs | 128/145 = 88.28% | 119/145 = 82.07% | +9 IDs; +6.21 pp |
| L2 hit@1 FULL | 105/117 = 89.74% | 50/117 = 42.74% | +55 units; +47.01 pp |
| L2 hit@3 FULL | 37/39 = 94.87% | 26/39 = 66.67% | +11 IDs; +28.21 pp |
| L2 hit@all FULL | 33/39 = 84.62% | 8/39 = 20.51% | +25 IDs; +64.10 pp |

为了避免把不同去重单位混成一个“综合分数”，比较层还保留两种诊断性
ledger/group 比值。current 为 `(119 + 121)/(119 + 121 + 189) = 55.94%`，baseline
为 `(106 + 98)/(106 + 98 + 95) = 68.23%`；若 I 不做 diagnostic cluster，分别为
`240/(240 + 291) = 45.20%` 和 `204/(204 + 95) = 68.23%`。这些数只描述
K expected、N substantive group 与 I 诊断单元的组成敏感性，不是论文主 precision，
因为 I 不是 substantive defect unit。

完整分子、分母和 expected ID 投影见
[combined_summary_v4.json](../derived/fair_comparison_v4/combined_summary_v4.json)。

## N：报告与实质问题

| 项目 | v60/current | X1v2 baseline v3 |
| --- | ---: | ---: |
| 原始/当前 N reports | 231 / 231 | 132 / 105 |
| N D2/D1 reports | 38 / 193 | 50 / 55 |
| conservative substantive N groups | 121 | 98 |
| group size distribution | 1:52, 2:31, 3:36, 4:1, 5:1 | 1:92, 2:5, 3:1 |

current N 在 v4 没有迁移。baseline 非 K 迁移为
`N->I=67`、`N->K=3`、`N->N=62`、`I->N=43`、`I->K=30`、`I->I=28`；逐条
记录在 [migration_index_v4.json](../derived/fair_comparison_v4/migration_index_v4.json)。
baseline 非 K 重审产生 33 条 K report，其中 unique expected relation 为：
FULL `DIFF-0032-03, EIS-0000-02, EIS-0002-01, EIS-0002-02, EIS-0002-03,
EIS-0019-02, EIS-0019-03, EIS-0020-02, EIS-0027-01, EIS-0029-02, EIS-0032-01,
EIS-0033-02, EIS-0037-01, EIS-0053-01, EIS-0056-02, EIS-0059-01, VU-0054-01`；
PARTIAL `EIS-0002-02, EIS-0004-01, EIS-0005-02, EIS-0005-03, EIS-0007-02,
EIS-0015-01, EIS-0019-03, EIS-0027-01, EIS-0032-01, EIS-0039-02, INS-0059-03`。
完整逐条 report 映射在 [baseline summary](../derived/manual_adjudication_v3_baseline_ni/summary_v3.json)
的 `non_k_migrations.rows`，同时保存在 comparison layer 的
`migration_index_v4.json`。

group 只允许同 side、同 pair，允许跨 round；成员须共享义务、source locus、
root cause 和最小 repair intent。singleton 是保守的“没有证据支持合并”，不是
“已证明有一个独立 defect”。K 按 unique expected ID 统计，N 按 substantive group
统计，不能把两者或 raw report 混成一个实体数。

## I 的组成与解释

| I 成分 | v60/current | X1v2 baseline v3 |
| --- | ---: | ---: |
| D0 | 120 | 85 |
| A0 / FALSE_POSITIVE | 53 | 10 |
| A0 / NOT_A_DEFECT_CLAIM | 118 | 0 |
| I reports | 291 | 95 |
| diagnostic clusters | 189 | 95 |

I cluster 只帮助描述 invalid claim 的重复形态，不是实质 defect 数，也不进入
substantive grouped precision。current 的 NADC 是 method-owned 的表示、分析或
归因主张，只有在证据说明报告没有提出作者 source 缺陷时才使用。代表证据包括：
`0014:r3:issue:1` 的 retention receipt 缺口、`0045:r1:issue:4` 的 lowering
guard 归因，以及 `0044:r1:issue:16` 的 route/lowering/runtime 归因。它们支持
“部分 I 与 current conversion/projection/runtime 证据边界有关”，但不能推出
全部 I 都是转换债务。FALSE_POSITIVE 仍单列，例如
`0001:r3:issue:1` 与 `0003:r2:issue:3` 的 source 已存在边。

## W 与 predicate

| 指标 | v60/current | X1v2 baseline v3 |
| --- | ---: | ---: |
| FULL-hit max W0/W1/W2 | 0/113/197（分母 310） | 0/227/0（分母 227） |
| method terminal predicate usage | 12/15 个 planned-scope ID；1237 条 terminal receipt | N/A，baseline 无同构 execution schema |
| report-bound predicate binding（诊断） | 8/15 个 ID；825 条 binding row | N/A，baseline 无同构 binding schema |
| report-bound completed receipts（诊断） | 522 条，其中 terminal=false/violation 为 522 条 | N/A |

“N/A”表示该字段在 baseline 运行契约中不存在，不是零。全部 finding 的 W 分布
不能替代 hit 单位的 max-W 分布。

### Predicate usage 与 contribution 的定义

本报告固定使用以下两个定义，不能互换：

- **usage**：谓词有对应的 execution receipt，且 receipt 已到达 terminal
  `pass` 或 `violation` 状态。`pass` 和 `violation` 都计入 usage；只出现在
  prompt、plan、unsupported receipt 或未完成 binding 中的不计入。
- **contribution**：仅当该 execution receipt 的 `terminal_result=false`
  （在当前 receipt schema 中对应 `predicate_verdict=false`、规范化
  `verdict=violation`）时计入。`pass` 不贡献 false。当前 schema 没有独立的
  `terminal_result` 字段；本文用这个概念名指代上述 terminal Boolean 结果。

因此，method 层面的正确结论是 **12/15 个 planned-scope 谓词被实际执行**，共
1237 条 terminal receipt，其中 `608 pass + 629 violation`。`report-bound binding`
是另一层统计：它只统计挂到最终 finding 的绑定记录，不能代替 method usage；当前
共有 8 个 ID、825 条 binding row，其中只有 522 条有 completed terminal receipt，
且这 522 条均为 `terminal_result=false/violation`。原先的 `303/825` 是旧的
`coverage_class=semantic_hit` 标记，不是按本定义得到的 contribution，不能再这样
命名。

本轮 full-scale-15 的 planned scope 为：
`S1,S2,S3,S4,S5,S6,G1,G2,G3,G4,R1,R2,R4,V1,V4`。
因此，未出现 completed terminal receipt 的 planned predicate 是 `S6,G3,V1`。
registry 中另外四个谓词 `R3,V2,V3,V5` 不属于本轮 full-scale-15 operational
scope；它们不能被解释为本轮“漏执行”。

### 19 个 registry predicate 的审计统计

`method terminal receipts` 和 `method false contribution` 来自 v60 raw method
的全部 162 个 round 文件；`report-bound binding rows` 与其对应的
`report-bound false contribution` 来自 predicate witness audit。后两列只作
绑定诊断，不改变前面的 usage 定义。

| ID | family | 台账期望 | method terminal receipts | method false contribution | report-bound binding rows | report-bound false contribution |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| S1 | Structure | 14 | 119 | 0 | 0 | 0 |
| S2 | Structure | 20 | 387 | 235 | 166 | 166 |
| S3 | Structure | 22 | 249 | 96 | 93 | 93 |
| S4 | Structure | 10 | 18 | 6 | 6 | 6 |
| S5 | Structure | 3 | 81 | 81 | 337 | 63 |
| S6 | Structure | 3 | 0 | 0 | 0 | 0 |
| G1 | Topology | 16 | 81 | 81 | 105 | 79 |
| G2 | Topology | 1 | 2 | 2 | 1 | 1 |
| G3 | Topology | 3 | 0 | 0 | 0 | 0 |
| G4 | Topology | 5 | 12 | 0 | 0 | 0 |
| R1 | Trajectory simulation | 9 | 34 | 0 | 0 | 0 |
| R2 | Trajectory simulation | 1 | 162 | 46 | 32 | 32 |
| R3 | Trajectory simulation | 0 | 0 | 0 | 0 | 0 |
| R4 | Trajectory simulation | 3 | 4 | 0 | 0 | 0 |
| V1 | Bounded verification | 4 | 0 | 0 | 0 | 0 |
| V2 | Bounded verification | 0 | 0 | 0 | 0 | 0 |
| V3 | Bounded verification | 0 | 0 | 0 | 0 | 0 |
| V4 | Bounded verification | 4 | 88 | 82 | 85 | 82 |
| V5 | Bounded verification | 0 | 0 | 0 | 0 | 0 |
| **合计** |  | **118** | **1237** | **629** | **825** | **522** |

四个“实际执行但 contribution=0”的 method predicate 是 `S1/G4/R1/R4`：它们
分别有 119/12/34/4 条 terminal receipt，全部为 `pass`。这解释了为什么它们
出现在 12/15 的 method usage 中，却不出现在 8/15 的 report-bound ID 集合中。

## 学术解释与限制

Porter, Votta & Basili（IEEE TSE 1995, DOI `10.1109/32.391380`）支持 true
fault、false positive 与 known-fault 区分；Klees et al.（CCS 2018, DOI
`10.1145/3243734.3243804`）支持使用 distinct bugs 而不是 raw report；Okun,
Delaitre & Black（NIST SP 500-297, DOI `10.6028/NIST.SP.500-297`）支持按
directly related、indirectly related 和 unrelated findings 讨论关联；Ahmed et
al.（MODELS 2025, DOI `10.1109/MODELS67397.2025.00014`）支持 equivalent issue
与人工确认的 new true issue；Pearson et al.（ICSE 2017, DOI
`10.1109/ICSE.2017.62`）说明报告粒度影响 fault 分解；Martinez et al.（EMSE
2017, DOI `10.1007/s10664-016-9470-4`）支持 semantic/repair equivalence 不
要求 patch 文本相同。IEEE 1044-2009、Goodenough et al.、Barr et al.、Zave &
Jackson、Massey et al. 和 Pollock 分别支撑 disposition、oracle、需求推理与
称职 alternative reading 的边界。

这些文献分别支持 distinct bug、relatedness、修复等价、false positive、需求
有效性与歧义裁决；“同 side + 同 pair + 同义务 + 同 source/root cause + 同修复
意图”是本项目的 operationalization，不是任何一篇文献逐字给出的完整标准。

数据直接支持：current 的 FULL hit、supported coverage 和 L2 hit 较高，report
precision 较低；current 的 I 差额由 D0、A0/FP 和 current-only NADC 共同组成。
协议推导：I 不进入 substantive defect grouped precision，且 PARTIAL 不进主 hit。
仍有敏感性：N 的 conservative merge 边界、I cluster 是否合并，以及台账是否覆盖
完整缺陷宇宙；因此本文以 report precision 为主，不用诊断性 group 比值替代它。

## 复算和归档

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation \
python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_fair_comparison_v4.py \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

逐侧入口：[current v4](../derived/manual_adjudication_v4_current_reaudit/README.md)、
[baseline v3](../derived/manual_adjudication_v3_baseline_ni/README.md)、[比较层](../derived/fair_comparison_v4/README.md)。
Manifest、输入输出 hash 和 review 记录位于比较层；旧 v2/v3 目录未被覆盖。
