> **Cold archive / deprecated historical snapshots.** 本目录只保存已经脱离当前主线的历史快照、旧 ledger、旧检索记录和迁移前证据。这里的内容不作为当前 seed、baseline、eligibility、pipeline 结果或论文主实验事实源。

# archive/ — 冷归档历史快照入口


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

## 2. 快照清单

| 快照 | 内容 | 使用方式 |
|---|---|---|
| [r1_5_to_r1_7_seed_corpus_snapshot/](./r1_5_to_r1_7_seed_corpus_snapshot/) | PR-R1.8-B 从旧 `seed_corpus/` 迁出的历史审计快照；含 legacy ledgers、search rounds、raw search results。 | 只用于追溯早期检索、筛选、排除和迁移哨兵；不要直接引用为当前事实。 |

## 3. 维护纪律

1. 新增到 `archive/` 的 Markdown 必须在文件开头写明 cold / deprecated / historical snapshot。
2. 非入口 `README.md` 的历史文档应使用 `yyyy-mm-dd-hh-mm-ss-短主题.md` 秒级前缀，时间来自原始内容冻结 commit 或迁入 archive commit。
3. 每个 archive Markdown 必须记录原始来源路径、时间依据 commit、迁入 commit 和当前事实源替代入口。
4. archive 内链接可以保留历史上下文；若需要当前可点击事实，必须回到当前事实源入口。
