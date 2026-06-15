# corpora/ — 第一篇论文三类文库入口

## 0. 定位

`corpora/` 是第一篇论文 `<NL, STM_0> -> STM_k / Better STM` 主线下的论文级文库入口。它只负责解释三类文库的分工、阅读顺序、与 project_1 既有长期文库的关系；**不承载事实总账**。

本文件冻结三类文库的入口纪律。PR-R1.8-B 已落地 seed library，当前 seed 事实源为 [seed_library/SUMMARY.md](./seed_library/SUMMARY.md)，其中可复算 `47/47` 候选 / 筛查、`36 dirs` 本地证据目录、旧九 `9/9` crosswalk、R2=4 handoff、人工下载队列与 seed / 资源可用性结论；R1.5--R1.7 旧 ledger / raw search 只作为历史审计快照保存在 [../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../archive/r1_5_to_r1_7_seed_corpus_snapshot/)。R1.8-C 已落地 [repair_baselines/](./repair_baselines/) 三件套，当前 repair baseline 事实源为 [repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md)，其中记录 24 个全文入库条目、检索覆盖、候选池筛查账、人工下载队列清空状态、negative evidence 与最终结论。`nl_datasets/` 子库待后续 PR 落地。三类子库的长期作用如下：

| 子库 | 作用 |
|---|---|
| `seed_library/` | 上游 `NL -> STM_0` seed 方法 / 来源文库。 |
| `repair_baselines/` | 本论文 `STM_0 -> STM_k` 修正任务 baseline / 近邻文库。 |
| `nl_datasets/` | 控制系统纯 NL 数据源文库。 |

## 1. 三类文库一句话边界

| 文库 | 收什么 | 不是什么 |
|---|---|---|
| [seed library](./seed_library/) | 能证明 `STM_0` 由 `NL` 生成、派生或人工构造得到的 `NL -> T0 FSM/HSM/EFSM/statechart` 来源。 | 不是本论文 repair baseline，不是 R2 四例样本集合本身。 |
| [repair baselines](./repair_baselines/) | 状态机 / UML / SysML / model artifact 的 repair、completion、refinement、feedback-guided correction 等近邻工作。 | 不是旧 `NL -> STM` generation baseline 的改名。 |
| NL datasets | 控制系统自然语言需求、用例、场景、系统描述、标准片段、教学案例等纯 NL 输入来源。 | 只有 NL 不等于 seed；只有生成并记录 `STM_0` 后才可 crosslink 到 seed。 |

## 2. 阅读顺序

1. 先读上级 [../README.md](../README.md) 和 [../GUIDE.md](../GUIDE.md)。
2. 再读本文件确认 `corpora/` 的入口边界。
3. 需要 seed 当前事实时，读 [seed_library/README.md](./seed_library/README.md)、[seed_library/GUIDE.md](./seed_library/GUIDE.md)、[seed_library/SUMMARY.md](./seed_library/SUMMARY.md)。
4. 需要 repair baseline 当前事实时，读 [repair_baselines/README.md](./repair_baselines/README.md)、[repair_baselines/GUIDE.md](./repair_baselines/GUIDE.md)、[repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md)。
5. 后续 `nl_datasets/` 落地后，进入对应子库的 `README.md -> GUIDE.md -> SUMMARY.md`。
6. 需要 R1.5--R1.7 旧 ledger / raw search 时，读 [../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 不作为当前事实真源。

## 3. 根层三件套纪律

三类子库根目录横向 Markdown 只允许：

1. `README.md`：定位、范围、阅读顺序、文件说明。
2. `GUIDE.md`：收录标准、字段、证据等级、更新流程、验收门。
3. `SUMMARY.md`：唯一横向事实真源，承载候选矩阵、排除、manual queue、crosswalk、统计、风险、handoff 和更新日志。

不得在三类子库根层新增 `candidate_matrix.md`、`screening_ledger.md`、`manual_queue.md`、`dataset_queue.md`、`crosswalk.md` 等第二事实源。若存在历史宽表或机器可读 dump，应归档并在 `SUMMARY.md` 中说明其审计用途。

## 4. 与 project-level 文库的关系

| project-level 入口 | paper1 `corpora/` 使用方式 |
|---|---|
| [../../baselines/](../../baselines/) | 只登记本论文实际使用 / 复核的 generation baseline 子集或 repair 近邻线索；不整体迁入、不改写为 repair baseline。 |
| [../../sources/](../../sources/) | 只登记被 paper1 选用或候选使用的控制系统 NL 来源；若由 sources 构造 `<NL, STM_0>`，生成后再 crosslink 到 seed library。 |
| [../../data/](../../data/) | 只记录 dataset card、规模、许可、本地路径指针；不复制敏感或大体量数据。 |
| [../../reproduction/](../../reproduction/) | 仅作为可复跑 / artifact 线索；若用于 seed 构造或对照，必须记录版本、命令、风险和证据指针。 |

原则：project-level 文库继续作为长期事实源；paper1 `corpora/` 只维护论文级选用、裁决、实验角色与风险总账。不得让两边同时维护同一统计口径。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 20:55:00 | 同步 [repair_baselines/](./repair_baselines/) 为 24 个全文入库条目，人工下载队列清空，并收紧严格 baseline 仍为 0、`completion-sysml-gwt` 只是 P0 路线近邻 / 条件对照的结论。 |
| 2026-06-15 16:50:00 | 同步 [repair_baselines/](./repair_baselines/) 为首批全文条目并补候选池筛查账。 |
| 2026-06-15 16:20:00 | PR-R1.8-C 落地 [repair_baselines/](./repair_baselines/) 三件套，repair baseline 横向事实以 [repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md) 为准。 |
| 2026-06-14 21:40:00 | PR-R1.8-B 同步 seed library 最新 `36 dirs`、manual queue 与资源结论口径；横向事实仍以 [seed_library/SUMMARY.md](./seed_library/SUMMARY.md) 为准。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 落地 [seed_library/](./seed_library/) 三件套，旧 `seed_corpus/` 迁入 archive。 |
| 2026-06-14 13:34:18 | PR-R1.8-A 创建 `corpora/` 入口 README；本轮不创建三类子库内容本体。 |
