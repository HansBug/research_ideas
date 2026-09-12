# corpora/ — 语料与文献库入口

> **导航页。** 本目录下有**四个**子库，职责互不重叠。它只解释分工与阅读顺序，**不承载事实总账**。
>
> | 子目录 | 是什么 | 在运行路径上？ | 入口 |
> | :-- | :-- | :-- | :-- |
> | [seed_library/](./seed_library/) | 上游 `NL -> STM_0` seed 方法 / 来源文献库。**论文语料的实际出处在这里**（`llms-emp-stm-subset`） | 🟢 | [SUMMARY.md](./seed_library/SUMMARY.md) |
> | [nl_segmentation/](./nl_segmentation/) | **需求边界人工标注（数据，不是文献）**。决定 discover 的 `nl_segments` 键空间 | 🟢 | [README.md](./nl_segmentation/README.md) |
> | [repair_baselines/](./repair_baselines/) | 模型修复 / 补全 / refinement 近邻工作文献库 | 🟡 | [SUMMARY.md](./repair_baselines/SUMMARY.md) |
> | [nl_datasets/](./nl_datasets/) | 控制系统纯 NL 数据源文献库；仅脚手架，尚未逐条填充 | 🔴 | [SUMMARY.md](./nl_datasets/SUMMARY.md) |
>
> 口径：🟢 当前运行路径 ｜ 🟡 服务相关工作与后续论文 ｜ 🔴 脚手架 / 未启用
>
> ⚠️ **[repair_baselines/](./repair_baselines/) 的定位已随论文收窄而变。** paper1 已收窄为 **issue discover 单独成篇**，repair 另立后续论文；因此本子库不再是 paper1 的 baseline 对照，而是**相关工作 + 后续论文的 baseline 储备**。其内部 README / GUIDE / SUMMARY 仍按「repair / closure 主线」措辞书写，那是文献库自身的收录口径，**不代表 paper1 的主张**。
>
> ⚠️ **[nl_segmentation/](./nl_segmentation/) 不是文献库**，因此没有 `GUIDE.md` / `SUMMARY.md` 三件套，只有 `README.md` + `overrides.json` + `PROVENANCE.md`。10 份 NL 中有 1 份的需求编号在机器层面无唯一解（编号不在行首、点号混用、编号重复、同句有裸数值），故由人工标注一次作为**数据**；该标注只回答「这份规格分成几条需求」，不回答「模型有什么缺陷」，**不构成 oracle 泄漏**。

## 0. 定位

`corpora/` 是第一篇论文当前 **source-level issue discover** 主线下的论文级文库入口。它只负责解释三类文库的分工、阅读顺序、与 project_1 既有长期文库的关系；**不承载事实总账**。

📌 本文件下文（以及 [repair_baselines/](./repair_baselines/) 内部）多处沿用 `source-level issue discovery / repair / closure` 这个长串。**那是 2026-08 收窄之前的主线名**。paper1 现在只做 **issue discover**，`repair` / `closure` 不是本文的任务，也不是本文的评测终点。凡下文出现该长串，一律按「**该文库自身的收录口径**」理解，不得读作 paper1 的主张。

本文件冻结三类文库的入口纪律。PR-R1.8-E 后，后续 R2 的 seed 冻结入口统一为 [seed_library/SUMMARY.md](./seed_library/SUMMARY.md)，repair baseline 与 NL dataset 只分别提供对照/近邻和纯 NL 来源，不替代 seed 入口。PR-R1.8-B 已落地 seed library，当前 seed 事实源为 [seed_library/SUMMARY.md](./seed_library/SUMMARY.md)，其中可复算 `47/47` 候选 / 筛查、`36 dirs` 本地证据目录、旧九 `9/9` crosswalk、R2=4 handoff、人工下载队列与 seed / 资源可用性结论；R1.5--R1.7 旧 ledger / raw search 只作为历史审计快照保存在 [../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../archive/r1_5_to_r1_7_seed_corpus_snapshot/)。R1.8-C 已落地 [repair_baselines/](./repair_baselines/) 三件套，当前 repair baseline 事实源为 [repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md)，其中记录 24 个全文入库条目、检索覆盖、候选池筛查账、人工下载队列清空状态、negative evidence 与最终结论。R1.8-D 已落地 [nl_datasets/](./nl_datasets/) 初步脚手架，当前只冻结入口、字段与边界，尚未逐条填充数据。注意：smoke 用代表性样例不放在 `seed_library/` 内，而放在上级 [selected_seed_examples/](../selected_seed_examples/)；它只保存少量静态 `<NL, STM_0>` 输入用于工具连通性自检，不是第四类文库，也不是最终实验集合。

三类子库的长期作用如下：

| 子库 | 作用 |
|---|---|
| `seed_library/` | 上游 `NL -> STM_0` seed 方法 / 来源文库。 |
| `repair_baselines/` | 模型修正 / 补全 / refinement 近邻工作文库。**已不是 paper1 的实验 baseline**（本文不做 repair，无从对照）；现在的两个用途是 paper1 的 §Related Work 靶子文献，以及后续 repair 论文的 baseline 储备。 |
| `nl_datasets/` | 控制系统纯 NL 数据源文库。 |

## 1. 三类文库一句话边界

| 文库 | 收什么 | 不是什么 |
|---|---|---|
| [seed library](./seed_library/) | 能证明 `STM_0` 由 `NL` 生成、派生或人工构造得到的 `NL -> T0 FSM/HSM/EFSM/statechart` 来源。 | 不是本论文 repair baseline，不是 R2 四例样本集合本身。 |
| [repair baselines](./repair_baselines/) | 状态机 / UML / SysML / model artifact 的 repair、completion、refinement、feedback-guided correction 等近邻工作。 | 不是旧 `NL -> STM` generation baseline 的改名。 |
| [nl_datasets](./nl_datasets/) | 控制系统自然语言需求、用例、场景、系统描述、标准片段、教学案例等纯 NL 输入来源。 | 只有 NL 不等于 seed；只有生成并记录 `STM_0` 后才可 crosslink 到 seed。 |

## 2. 阅读顺序

1. 先读上级 [../README.md](../README.md) 和 [../GUIDE.md](../GUIDE.md)。
2. 再读本文件确认 `corpora/` 的入口边界。
3. 需要 seed 当前事实时，读 [seed_library/README.md](./seed_library/README.md)、[seed_library/GUIDE.md](./seed_library/GUIDE.md)、[seed_library/SUMMARY.md](./seed_library/SUMMARY.md)。
4. 需要 smoke 用静态样例时，读上级 [selected_seed_examples/README.md](../selected_seed_examples/README.md)；不要把它误读成 seed registry 全量事实源或最终实验集合。
5. 需要 repair baseline 当前事实时，读 [repair_baselines/README.md](./repair_baselines/README.md)、[repair_baselines/GUIDE.md](./repair_baselines/GUIDE.md)、[repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md)。
6. 需要控制系统纯 NL 数据源当前入口时，读 [nl_datasets/README.md](./nl_datasets/README.md)、[nl_datasets/GUIDE.md](./nl_datasets/GUIDE.md)、[nl_datasets/SUMMARY.md](./nl_datasets/SUMMARY.md)。
7. 需要 R1.5--R1.7 旧 ledger / raw search 时，读 [../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 不作为当前事实真源。

## 2.1 R2 读取链路

后续 R2 / R3 / R4 默认按以下链路读取事实：

| 需求 | 当前入口 | 禁止误读 |
|---|---|---|
| 冻结 `<NL, STM_0>` seed 候选 | [seed_library/SUMMARY.md](./seed_library/SUMMARY.md) | 不从旧 `seed_corpus/` 或 `evidence/baseline_*` 直接冻结样本。 |
| 查修正任务 baseline / 近邻 | [repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md) | 不把 near-neighbor 或 completion-style 工作写成严格 baseline。 |
| 查纯 NL 数据源 | [nl_datasets/SUMMARY.md](./nl_datasets/SUMMARY.md) | 不把只有 NL 的数据源提前计为 seed。 |
| 追溯旧检索 / ledger | [../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../archive/r1_5_to_r1_7_seed_corpus_snapshot/) 与 [../evidence/README.md](../evidence/README.md) | archive / evidence 只作审计，不是当前横向事实源。 |

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
| 2026-06-24 10:25:00 | 补充上级 [selected_seed_examples/](../selected_seed_examples/) 定位：smoke 用静态样例不放入 seed registry 文库，不作为最终实验集合。 |
| 2026-06-16 23:08:00 | PR-R1.8-E 补充 R2 读取链路：seed 从 [seed_library/SUMMARY.md](./seed_library/SUMMARY.md) 读取，repair / NL / archive / evidence 均只按各自角色使用。 |
| 2026-06-15 23:20:00 | PR-R1.8-D 落地 [nl_datasets/](./nl_datasets/) 三件套脚手架，明确当前只登记纯 NL 数据源入口与字段纪律；来自 [../../../CLAUDE.md](../../../CLAUDE.md) § 数据集信息的 9 系统 / 101 需求、`sources/` 真实控制系统 NL 池、旧 Path-1 `sources/` T0+🟢 线索作为后续填充锚点。 |
| 2026-06-15 20:55:00 | 同步 [repair_baselines/](./repair_baselines/) 为 24 个全文入库条目，人工下载队列清空，并收紧严格 baseline 仍为 0、`completion-sysml-gwt` 只是 P0 路线近邻 / 条件对照的结论。 |
| 2026-06-15 16:50:00 | 同步 [repair_baselines/](./repair_baselines/) 为首批全文条目并补候选池筛查账。 |
| 2026-06-15 16:20:00 | PR-R1.8-C 落地 [repair_baselines/](./repair_baselines/) 三件套，repair baseline 横向事实以 [repair_baselines/SUMMARY.md](./repair_baselines/SUMMARY.md) 为准。 |
| 2026-06-14 21:40:00 | PR-R1.8-B 同步 seed library 最新 `36 dirs`、manual queue 与资源结论口径；横向事实仍以 [seed_library/SUMMARY.md](./seed_library/SUMMARY.md) 为准。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 落地 [seed_library/](./seed_library/) 三件套，旧 `seed_corpus/` 迁入 archive。 |
| 2026-06-14 13:34:18 | PR-R1.8-A 创建 `corpora/` 入口 README；本轮不创建三类子库内容本体。 |
