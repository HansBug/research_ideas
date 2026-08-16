# 裁定：`UM-` 一族整批撤出 relabel 工作单

**日期**：2026-08-16　**范围**：`manual_review/relabel/` 的 49 个 `UM-<pair>` 填写块

⛔ **裁定**：`UM-` 一族**全部撤出工作单**。残余部分另存为 [unmatched_residue.json](../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/unmatched_residue.json)，**不进工作单**、不设裁决区、无 D 档判读。

⚠️ 本文记录**为什么** —— 否则日后只能看到「候选数从 269 变成 220」而不知何故。

⛔⛔ **本文里的 `220` 是 2026-08-16 撤 `UM-` 那一刻的数，⛔ 不是当前口径。** ⭐ 当前工作单条目数是 **323**（§2 台账 99 + §3 候选 224）—— 同日又发生两件事：① 撤 `UM-` 使 5 条原本并入 UM 桶的 `INS-` 失去宿主，⭐ 经逐条判重后 4 条自立、1 条并入同伴；② 一度误把未去重的判读包总数 `380` 当成条目数，⛔ 导致 56 条已去重的重复被重新摆出。⭐ 完整账目与每个历史数字的来历见 [DEDUP_ACCOUNTING.md](../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/DEDUP_ACCOUNTING.md)。

## 一、`UM-` 是什么

`UM` = **U**n**m**atched。它不是有人筛出来的候选集，而是**机械匹配器的兜底桶**：两个实验臂（X1 基线臂、v46 主臂）运行中报出的 issue，凡是匹配器没能链到任何台账条目的，全部倒进 [unmatched_issues.json](../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/unmatched_issues.json)。

出处（该文件 `sources` 字段逐字）：

| 侧 | 来源 | 口径 |
| :-- | :-- | :-- |
| X1 | `baseline_arm/results/verdicts_x1.json .unclaimed_issues` + `X1-J*-reclaim.tsv` | post-reclaim 的**未认领** |
| v46 | `discover_matrix/round_variance.py` 的 `_issue_signature/_match` | 匹配器**不返回任何台账条目** |

压缩链：**1089 条原始 issue（X1 334 + v46 755）→ 1063 条**（逐字去重）**→ 619 组**（渲染时按元素集合再并一层）**→ 49 个填写块**（一个 pair 一块）。⛔ 单块最多承载 **35 组**（`0029`），中位 11 组。

## 二、撤除的三条理由，按证据强度排

### 1. ⛔ X1 那一半是在重审已结案的东西 —— 精确证据

X1 侧 334 条里 **333 条（99.7%）的 `adjudicated.cluster` 精确出现在 `sources.other_unexpected()` 的已裁定多报簇表里**。⭐ 这是簇 id 逐一对上，不是模糊匹配。

那些既有裁定判的是：

| 裁定 | 条 | 占 334 |
| :-- | --: | --: |
| `NO_NL_BASIS`（无 NL 依据） | 224 | 67% |
| `FALSE_POSITIVE` | 64 | 19% |
| `OUT_OF_SCOPE` | 34 | 10% |
| `VALID_UNRECORDED`（真漏记） | 12 | 4% |

⛔ 前三种共 **322 条（96%）全部是「不是作者制品的缺陷」**。⭐ 而那 4% 真漏记**早已被提取成 `VU-` 系列**（15 条）——⚠️ 于是它们**同时**以 `VU-` 独立块出现、又躺在 `UM-` 表里，**重复计数**（簇号可逐一核对：`0009-6`、`0039-4` 等）。

### 2. ⛔ v46 那一半的主体是投影债务，按 P2 不算作者缺陷

v46 侧 729 条里 **409 条（56%）**能与该 pair 的 v46 已裁定簇对上元素名。⚠️ **这一步是估算**（元素名重合 ≠ 同一主张），⭐ 但对应的既有裁定分布很说明问题：

| 裁定 | 条 |
| :-- | --: |
| `REPRESENTATION_DEBT`（表示债务） | 174 |
| `NO_NL_BASIS` | 171 |
| `FALSE_POSITIVE` | 52 |
| `OUT_OF_SCOPE` | 12 |

⭐ `REPRESENTATION_DEBT` 是关键。以 `0029-1` 那个簇为例，它的 `merge_reason` 逐字写着：

> 这 8 条各自索要作者**同一条析取守卫**的一个分支，或其 roll-up、或同一分支的不同清洗名。**损失通道唯一——R4.5 把整条标签压成一个原子事件名**。合并依据是 `stm0.puml` 上那**一行**。

⛔ 即那批「独立事件 `pedestrian_inactive` 未声明」「缺少 `dist_to_rear` 条件量声明」全是**编译器把标签压扁**造成的 —— 按 `D_PROTOCOL.md` §P2（判定对象是作者源、不是编译产物），它们不是作者缺陷。

### 3. ⛔ 登记单位从头就不对

[candidate_mapping.json](../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/candidate_mapping.json) 的 `unit_caveat` 逐字：

> ⛔ 三类候选不同构：VU / DIFF 一条 = 一个主张，**UM 一条 = 整张表**（一个 pair 的全部未匹配 issue）。UM 桶内各组座标不一致时一律 `mappable: false` 且 `blocker = unit_of_record`。

实测 **47/49 块**是 `unit_of_record` 卡点。⛔ 而 D 档判定程序判的是**一条可陈述的主张**（相 A 要 ground 一条被违反的义务、相 B 再尝试推翻）——⚠️ 一张 35 组的表**没有单一 statement 可判**，这也是它当初没进三方判读包（380 条）的结构性原因。

## 三、⛔ 一处我方的判断错误，一并记下

撤除前，`UM-` 的 49 条人工 meta review 几乎全给了 `D2-lit`，依据是 [fused_event_policy.md](../protocol/fused_event_policy.md) 里那句「**放开『报告事件融合本身是保真度缺陷』**」。

⛔ **那个依据用宽了。** 那条裁定说的是「**报告事件融合这件事**算一条保真度缺陷」，⚠️ 不是「**每一个被融合掉的分支名**都各算一条缺陷」。⭐ 而 `UM-` 表里那批「独立事件 X 未声明」恰恰是后者 —— 同一条压扁标签被拆成十几条「某分支未声明」。

⭐ 那 49 条 meta review 随本次撤除一并删去（不保留，因为它们的档位判断已不成立）。

## 四、残余清单里剩什么

[unmatched_residue.json](../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/unmatched_residue.json)：**143 条**归一化事实（来自 320 条既对不上已裁定簇、又非 X1 已结案材料的 v46 条目）。

| 项 | 数 |
| :-- | --: |
| 归一后事实 | **143** |
| ⛔ 连元素名都点不出（`element: null`） | 31（22%） |
| ⚠️ 只被单个格报过 | 71（50%） |
| 种类为「未声明 / 缺失」 | 124（87%） |
| 覆盖 pair | 39 |

⚠️ 那 124 条「未声明 / 缺失」**正是 `REPRESENTATION_DEBT` 那一族的同型** —— ⭐ 它们只是恰好没被已裁定簇的元素名覆盖到，⛔ 不代表性质不同。故本清单只作留存，**不作候选**。

## 五、⭐ 门面数字的变化

| 数字 | 撤除前 | 撤除后 |
| :-- | --: | --: |
| `pairs` | 54 | 54 |
| `ledger_records_seen` | 99 | **99** |
| `candidates_seen` | 269 | **220** |

⭐ 台账 99 条一条没动。⛔ 候选由 269 降到 220，差值恰为撤掉的 49 个 `UM-` 块。

## 六、⭐ 若要恢复

⛔ 恢复不该是「把 49 块加回来」。⭐ 正确做法是：从 [unmatched_residue.json](../../../archive/r10_ledger_v1_and_v46/manual_review/relabel/unmatched_residue.json) 里挑出**确实是完整主张**的那些（判据：点得出元素名 · 出现 ≥2 格 · 能陈述一条被违反的义务而不只是「某个分支名没声明」），**逐条拆成独立候选**并送三方判读 —— ⚠️ 粗算符合前两条的约 **46 条**。⛔ 一块对应一张表的形态不许再出现。
