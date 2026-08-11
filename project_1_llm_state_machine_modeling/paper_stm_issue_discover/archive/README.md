> **Cold archive / deprecated historical snapshots.** 本目录只保存已经脱离当前主线的历史快照、旧 ledger、旧检索记录和迁移前证据。这里的内容不作为当前 seed、baseline、eligibility、pipeline 结果或论文主实验事实源。

# archive/ — 本工作区内部的冷归档快照入口

> ⚠️ **仓库里有两个 `archive/`，别搞混：**
>
> | 路径 | 内容 |
> | :-- | :-- |
> | **本目录**（`paper_stm_issue_discover/archive/`） | 本论文工作区自己的历史快照：R1.5–R1.7 种子语料、R5.7 Better STM 全树、R7 issue lifecycle 脚手架、R8 论文叙事 |
> | [../../archive/](../../archive/) | project_1 层的**已停用旧路线**：旧 agent loop 基础设施、Path-1 评测链、Path-1/Path-2 指南 |
>
> 两个都不参与本文任何结论。当前入口一律回到 [../README.md](../README.md)。
>
> **本目录有四个快照，各配自己的 README**（按阶段先后排）：
>
> | 快照 | 一句话 | 入口 |
> | :-- | :-- | :-- |
> | [r1_5_to_r1_7_seed_corpus_snapshot/](./r1_5_to_r1_7_seed_corpus_snapshot/) | 旧 `seed_corpus/` 的检索轮次与筛选台账 | [README.md](./r1_5_to_r1_7_seed_corpus_snapshot/README.md) |
> | [r5_7_better_stm_snapshot/](./r5_7_better_stm_snapshot/) | 已废弃的 Better STM 评价框架全树（889 条目），含旧 `pipeline/evaluation/` | [README.md](./r5_7_better_stm_snapshot/README.md) ＋ [PATH_MAPPING.md](./r5_7_better_stm_snapshot/PATH_MAPPING.md) |
> | [r7_issue_lifecycle_scaffold/](./r7_issue_lifecycle_scaffold/) | 2026-07 repair 期实验设计脚手架（25 份）＋ 两份 repair 期资产台账（2 份）。⭐ 其中 `issue_lifecycle/` 约八成是**仍然有效的 discover 材料** | [README.md](./r7_issue_lifecycle_scaffold/README.md) |
> | [r8_discover_repair_story/](./r8_discover_repair_story/) | 2026-08-11 凌晨那一版 `story/`（7 份）。⚠️ **不是 repair 期遗物**——已是 discover 口径，归档是因为要重搭骨架 | [README.md](./r8_discover_repair_story/README.md) |


## 0. 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 来源类型 | R5.5.1 新建 archive 入口页；不是从旧文档迁移来的历史快照。 |
| 时间口径 | N/A；本文件用于索引 cold archive，具体历史内容的 freeze commit 见各子文件头部。 |
| 迁入 / 新建依据 | 当前 R5.5.1 PR 的路径纪律加固；提交 SHA 由本文件 git history 追踪。 |
| 当前事实源替代入口 | [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md)、[../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)、[../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md)、[../reports/SUMMARY.md](../reports/SUMMARY.md) |

## 1. 当前事实源请先读哪里

| 需要判断什么 | 当前事实源 | archive 的角色 |
|---|---|---|
| 当前 `<NL, STM_0>` seed / seed library | [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md) | 只解释 R1.5--R1.7 早期检索和筛选历史。 |
| 当前 repair baseline / near-neighbor | [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md) | 只保留旧 baseline 线索，不决定当前 baseline。 |
| 当前纯 NL 数据源 | [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md) | 只保留旧检索覆盖和 pending 线索。 |
| 当前 R5/R5.5 human-facing conclusions | [../reports/SUMMARY.md](../reports/SUMMARY.md) | 只作为 provenance 或 negative evidence 背景。 |
| R5.7 Better STM historical assets | [r5_7_better_stm_snapshot/README.md](./r5_7_better_stm_snapshot/README.md) | 只解释 superseded Better STM 阶段，不作为当前事实。 |
| 当前实验协议、判定口径、命中判据 | [../discover_matrix/docs/protocol/](../discover_matrix/docs/protocol/) | [r7_issue_lifecycle_scaffold/](./r7_issue_lifecycle_scaffold/) 只解释 2026-07 repair 期的设计意图；其 `issue_lifecycle/` 可作为 issue 状态定义与 fixture 的取材来源。 |
| 论文叙事、contribution、claim 与术语 | 新 `story/`（重搭中）；数字回 [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) | [r8_discover_repair_story/](./r8_discover_repair_story/) 是重搭前那一版的完整快照，口径与当前一致，可作为起草参考。 |

## 2. 快照清单

| 快照 | 内容 | 使用方式 |
|---|---|---|
| [r1_5_to_r1_7_seed_corpus_snapshot/](./r1_5_to_r1_7_seed_corpus_snapshot/) | PR-R1.8-B 从旧 `seed_corpus/` 迁出的历史审计快照；含 legacy ledgers、search rounds、raw search results。 | 只用于追溯早期检索、筛选、排除和迁移哨兵；不要直接引用为当前事实。 |
| [r5_7_better_stm_snapshot/](./r5_7_better_stm_snapshot/) | R5.7 / Better STM / constructed `STM_k` / blind adjudication / repair target taxonomy / objective metric framework cold snapshot；含 moved `experiment_design/`、`pipeline/evaluation/` 和 R5.7 reports。 | 只用于 historical provenance / calibration / anti-gaming 参考；不得作为 active method source、evaluation gate、baseline contract 或 repair effectiveness evidence。 |
| [r7_issue_lifecycle_scaffold/](./r7_issue_lifecycle_scaffold/) | 2026-07 source-level issue lifecycle 脚手架：`experiment_design/`（顶层三件套、`issue_lifecycle/` 11 份、`source_trace/` 11 份、`metrics/` 1 份，共 25 份）＋ `evidence_ledgers/`（2 份 repair 期资产台账）。 | 协议块整体退役，不得恢复为 active 实验设计。但 `issue_lifecycle/` 的六个状态定义、两条 confirmation 路径、conversion artifact 归因边界与 6 个 fixture 仍可作为新规则的取材来源——取用前先读其 README §3。⚠️ 对应的 JSON schema / fixture / pytest **未随之归档**，仍在 [../pipeline/evaluation/](../pipeline/evaluation/) 在线。 |
| [r8_discover_repair_story/](./r8_discover_repair_story/) | 2026-08-11 凌晨重写的那一版 `story/`：thesis、两条 contribution、章节骨架与四个 RQ、C1–C15 claim–证据对照、任务边界、建模对象、术语政策，共 7 份。 | ⚠️ **归档理由是「要重搭骨架」，不是「内容过时」**——其 discover 口径与当前一致。写新 `story/` 或论文任一节前应先读其 README §3。⛔ 不得从中转抄任何实验数字。 |

## 3. 维护纪律

1. 新增到 `archive/` 的 Markdown 必须在文件开头写明 cold / deprecated / historical snapshot。
2. 非入口 `README.md` 的历史文档应使用 `yyyy-mm-dd-hh-mm-ss-短主题.md` 秒级前缀，时间来自原始内容冻结 commit 或迁入 archive commit。
3. 每个 archive Markdown 必须记录原始来源路径、时间依据 commit、迁入 commit 和当前事实源替代入口。
4. archive 内链接可以保留历史上下文；若需要当前可点击事实，必须回到当前事实源入口。
5. **整棵子树迁入时保留原文件名与原目录结构**（`r5_7`、`r7`、`r8` 三个快照均如此），
   第 2 条的秒级前缀只约束零散迁入的单份历史文档。
6. **归档不得改内容。** 允许的唯一机械变换是把相对链接按新深度重算，使其仍能点开；
   结论、数字、措辞、更新日志一律原样保留。每个快照 README 必须写明它做了 / 没做哪些变换。
7. 每个快照 README 必须有「⭐ 里面哪些内容仍然有价值、什么时候该取回来」一节，
   并给出精确路径——**归档的目的是保留可复活的资产，不是把东西扫进角落**。

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-08-11 | 新增两个快照：[r8_discover_repair_story/](./r8_discover_repair_story/)（原 `story/`，7 份）与 [r7_issue_lifecycle_scaffold/](./r7_issue_lifecycle_scaffold/)（原 `experiment_design/` 25 份 ＋ 原 `evidence/ledgers/` 两份 repair 期台账）。34 个文件全部 `git mv` rename，内容未改。同步补第 5–7 条维护纪律，并修正 [r5_7_better_stm_snapshot/](./r5_7_better_stm_snapshot/) 的 README / PATH_MAPPING 中指向 `story/`、`experiment_design/`、`evidence/ledgers/` 的 8 条链接。 |
