# evidence_ledgers/ — 两份 repair 期资产台账（cold archive）

> **Cold archive / 框架前提已作废 / 事实记录仍可查。**
> 本目录保存原 `evidence/ledgers/` 下的两份台账。它们的**结论框架**已被
> 「paper1 只做 issue discover」覆盖，但它们**记录的事实**（当时仓库里有什么、
> 各自怎么判、依据是哪次讨论）仍是唯一一份可查的来源。
>
> 上级归档导引：[../README.md](../README.md)。`evidence/ledgers/` 剩余的三份 R0/R1
> 历史台账未随本次归档移动，仍在 [../../../evidence/ledgers/](../../../evidence/ledgers/)。

## 0. 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原路径 | `paper_stm_issue_discover/evidence/ledgers/` |
| 内容冻结时间 | `paper1_strategy_asset_map.md` 2026-07-07 19:57:36 起，末次更新 2026-07-07 23:40:00；`legacy_asset_inheritance.md` R0 阶段，无内部更新日志 |
| 归档时间 | 2026-08-11 |
| 归档动作 | `git mv`，内容未改，仅机械调整相对链接深度 |

## 1. 两份是什么、为什么归档

| 文件 | 是什么 | 为什么归档 |
| :-- | :-- | :-- |
| [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) | R0 阶段划定的旧资产继承边界：`paper_v1/`、PR #93/#94/#96 分支局部资产、`baselines/`、`sources/` 各自可复用什么、不可继承什么 | 其 §3「新旧 story 的覆盖关系」把第一篇的 thesis 直接定义成 `<NL, STM_0> -> STM_k / Better STM` 的 **repair / refinement**。这个框架前提已两次被覆盖（先是 07-07 转 source-level issue lifecycle，再是 08-07/08-08 收窄为 discover），留在 active 路径会被读成当前 thesis |
| [paper1_strategy_asset_map.md](./paper1_strategy_asset_map.md) | 2026-07-07 导师讨论后的资产清账地图：A-001 – A-024 逐条给 `decision`、`reason`、`downstream_pr`、`verification_command`，外加下游 PR 聚合视图 | 它是**转向 repair 主线时的施工地图**：§0 把主线写成「source-level behavioral issue discovery **and closure**」，§4 的下游 PR 表含 `PR-repair-runner`、`PR-raw-export`、`PR-eval-rubric`（closure/regression rubric）等 repair 行。这些施工路线已整体不属于本文 |

## 2. ⭐ 里面哪些内容仍然有价值、什么时候该取回来

| 仍有价值 | 精确位置 | 什么时候用 |
| :-- | :-- | :-- |
| **A-001 – A-024 资产逐条判定表** | [paper1_strategy_asset_map.md](./paper1_strategy_asset_map.md) §3 | ⭐ 追溯「某个目录当初为什么被保留 / 改写 / 归档 / 只作历史」时，这是唯一一份逐条记录。每行还带当时用的 `verification_command`，可复算 |
| **四态 decision 口径** | 同上 §2 | 需要给一批资产做保留 / 改写 / 归档分类时，直接沿用 `active` / `update` / `archive` / `historical` 四态及其典型下游定义 |
| **「conversion / normalization / lowering 可作 active infrastructure，但不能计入 method gain」** | 同上 §2 特殊纪律段 | ⭐ 这条纪律至今有效，是当前禁用词表里 `conversion gain` 一条的来源；引用其出处时指这里 |
| **上游事实源与优先级表** | 同上 §1 | 记录了 #100 / #146 / #145 / 两次导师记录各自的 status 与使用纪律；解释「某条结论凭什么采信」时可查 |
| **五条使用规则** | 同上 §6 | 尤其第 2 条「`archive` 决策不等于删除；必须迁入 archive snapshot 并保留原路径映射」——本次归档正是按它执行的 |
| **旧资产不可继承的理由** | [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) §2 | 判断 `paper_v1/`、旧 baseline 台账、旧 sources 池能否作为 provenance 或线索时 |

## 3. ⛔ 已经作废、不得引用的部分

| 内容 | 位置 | 现在的口径 |
| :-- | :-- | :-- |
| 「第一篇是 `<NL, STM_0> -> STM_k / Better STM` repair / refinement」 | [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) §3 | paper1 = issue discover 单独成篇；见 [../../../README.md](../../../README.md) §1–§2 |
| 「主线是 source-level behavioral issue discovery **and closure**」 | [paper1_strategy_asset_map.md](./paper1_strategy_asset_map.md) §0 | closure 与 repair 另立后续论文 |
| 下游 PR 聚合视图（`PR-repair-runner` / `PR-raw-export` / `PR-eval-rubric` / `PR-loop-pilot` …） | 同上 §4 | 已不是施工路线。动态施工状态一律以 GitHub PR / issue 为准，仓库文件不维护 |
| A-005 `story/` 行标 `update`、A-004 root docs 行标 `update` | 同上 §3 | 两处均已另行处理：`story/` 已归档至 [../../r8_story_pre_rebuild/](../../r8_story_pre_rebuild/)；root docs 由另一路 PR 重写 |
| 表中大量 `active` 判定 | 同上 §3 | 只反映 2026-07-07 当时的状态，不代表当前。判断当前状态回 [../../../README.md](../../../README.md) 第 6 节导航 |

## 4. 原路径 → 新路径映射

| 原路径 | 新路径 |
| :-- | :-- |
| `evidence/ledgers/legacy_asset_inheritance.md` | [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) |
| `evidence/ledgers/paper1_strategy_asset_map.md` | [paper1_strategy_asset_map.md](./paper1_strategy_asset_map.md) |

未移动、仍在 [../../../evidence/ledgers/](../../../evidence/ledgers/) 的三份：
`upstream_fact_ledger.md`、`source_coverage_ledger.md`、`artifact_availability_ledger.md`。
配套扫描审计 [../../../evidence/audits/2026-07-07-post-strategy-asset-scan.md](../../../evidence/audits/2026-07-07-post-strategy-asset-scan.md)
也未移动——它是静态扫描证据，不含 thesis 表述。

## 5. 禁止外推

1. 不得把这两份的任何一条 `decision` 当作当前资产状态。
2. 不得把下游 PR 表当作待办清单。
3. 不得从 §3 列出的作废表述中恢复 thesis 措辞。
4. 引用本目录时必须写明它是 2026-07-07 时点的历史清账，不是当前事实源。
