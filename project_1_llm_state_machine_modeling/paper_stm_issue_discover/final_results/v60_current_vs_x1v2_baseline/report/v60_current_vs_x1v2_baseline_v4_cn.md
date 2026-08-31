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
baseline W。predicate execution usage 与 report-bound predicate-ID presence 分开统计，也不参与 D/A
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
| N reports | 231 | 105 |
| N D2/D1 reports | 38 / 193 | 50 / 55 |
| conservative substantive N groups | 121 | 98 |
| group size distribution | 1:52, 2:31, 3:36, 4:1, 5:1 | 1:92, 2:5, 3:1 |

current N 在 v4 没有迁移。baseline v3 非 K 迁移为
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
| A0 / NOT_A_DEFECT_CLAIM (NADC) | 118 | 0 |
| I reports | 291 | 95 |
| diagnostic clusters | 189 | 95 |

I cluster 只帮助描述 invalid claim 的重复形态，不是实质 defect 数，也不进入
substantive grouped precision。current 的 291 条 I 到 189 个 cluster 的逐条映射见
[current I diagnostic index](../derived/manual_adjudication_v4_current_reaudit/current_i_diagnostic_clusters_v4.json)。
current 的 NADC 是 method-owned 的表示、分析或
归因主张，只有在证据说明报告没有提出作者 source 缺陷时才使用。代表证据包括：
`0014:r3:issue:1` 的 retention receipt 缺口、`0045:r1:issue:4` 的 lowering
guard 归因，以及 `0044:r1:issue:16` 的 route/lowering/runtime 归因。它们支持
“部分 I 与 current conversion/projection/runtime 证据边界有关”，但不能推出
全部 I 都是转换债务。FALSE_POSITIVE 仍单列，例如
`0001:r3:issue:1` 与 `0003:r2:issue:3` 的 source 已存在边。

## W 与 predicate

### Paper-facing predicate summary

| 指标 | v60/current | X1v2 baseline v3 |
| --- | ---: | ---: |
| registry predicates | 19（Structure 6、Topology 4、Trajectory simulation 4、Bounded verification 5） | N/A |
| distinct IDs with terminal receipt | 12/19 | N/A，无同构 schema |
| distinct IDs bound to report-bound findings | 8/19 | N/A，无同构 schema |

v60 的 12 个实际执行 ID 为 `G1, G2, G4, R1, R2, R4, S1, S2, S3, S4, S5, V4`；
8 个 report-bound distinct ID 为 `G1, G2, R2, S2, S3, S4, S5, V4`。这里的
“执行”指至少产生一条 terminal receipt；“report-bound”指至少绑定到一条最终
report-bound finding。两者都是 predicate-ID 统计，不是 finding、W2、hit 或缺陷
类型覆盖率。X1v2 没有同构 predicate binding/receipt schema，因此写作和机器
汇总均使用 N/A，而不是零。

| 指标 | v60/current | X1v2 baseline v3 |
| --- | ---: | ---: |
| FULL-hit max W0/W1/W2 | 0/113/197（分母 310） | 0/227/0（分母 227） |
| report-bound binding rows / all reports | 825/1271 = 64.91% | N/A，baseline 无同构 binding schema |
| legacy `coverage_class=semantic_hit` markers / report-bound rows | 303/825 = 36.73% | N/A |

“N/A”表示该字段在 baseline 运行契约中不存在，不是零。全部 finding 的 W 分布
不能替代 hit 单位的 max-W 分布。上表后两行是 report-level 审计诊断，不能替代
前面的 distinct-ID 指标。

### Predicate usage 与 report-bound presence 的定义

本报告把 distinct-ID 指标和 report-level 诊断分开发布：

- **predicate execution usage**：registry 中至少产生一条 terminal receipt 的
  distinct predicate IDs，v60 为 `12/19`。
- **report-bound predicate IDs**：至少绑定到一条最终 report-bound finding 的
  distinct predicate IDs，v60 为 `8/19`。这不是谓词布尔贡献字段、W2 数或
  finding 数。
- **report-bound binding rows**：最终 finding 保留 registered predicate binding 和
  receipt 的记录，共 `825/1271`；这是逐报告诊断分母，不是完整 method 执行次数。
- **legacy semantic-hit marker**：上述绑定行中继承的 `coverage_class=semantic_hit`
  标记共 `303/825`；该字段不能解释成 terminal-false receipt、W2 数或 8 个谓词
  的贡献数。

谓词是证据生成后端，不是缺陷发现的准入条件。详细的后端能力审计留在内部
evaluation-only 材料，不作为本文方法输入或主结果。

本文聚焦于建立缺陷存在的证据：一个有来源依据的 sound violation 或具体反例已经足够
建立缺陷证据；当静态证据已经闭合时，不需要为形式完整性强行升级到 trajectory
simulation 或 BMC。只有 guard、时序、RTC、变量效果或全局终止等性质无法由静态
证据表达时，才使用这些更强的后端。

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
要求 patch 文本相同；IEEE Std 1044-2009，*IEEE Standard Classification for
Software Anomalies*（DOI `10.1109/IEEESTD.2010.5399061`）给出 anomaly disposition
与 intended behavior 的分类依据。

这些文献分别支持 distinct bug、relatedness、修复等价、false positive 和 anomaly
disposition；“同 side + 同 pair + 同义务 + 同 source/root cause + 同修复意图”是
本项目的 operationalization，不是任何一篇文献逐字给出的完整标准。

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
Manifest、输入输出 hash 和 review 记录位于比较层；历史层和旧报告未被覆盖，
baseline v3 仍是当前冻结对照层。
