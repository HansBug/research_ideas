# R5.7 Better STM 历史快照（cold archive）

> **Cold archive / superseded / historical calibration only.** 本目录保存 R5.7 阶段围绕 **Better STM / which STM is better / constructed `STM_k` / blind adjudication / repair-target taxonomy** 形成的历史资产。它们已被 2026-07-07 导师战略讨论覆盖，不再作为 paper1 的 active headline evaluation framework、method result、baseline contract 或正式实验协议。

## 1. 为什么归档

⚠️ **本节下面这句「当前 paper1 主线」写于 2026-07，已经过期。** 2026-08 导师定调把 paper1
**收窄为 issue discover 单独成篇**，repair 另立后续论文；因此其中的 `issue-grounded repair /
refinement`、`issue closure 与 regression` 都**不再属于 paper1**。当前口径以
[../../README.md](../../README.md) §2 为准。原句保留如下以供追溯：

> 当前 paper1 主线已经重置为：给定 `NL + raw/source STM_0`，通过中间可执行语义表示、diagnostics / inspect、simulation / probe、formal verification / check feedback 与 agent loop，发现并确认 source-level behavioral issues，围绕 confirmed issues 做 issue-grounded repair / refinement，并最终回到 raw/source 层说明 issue closure 与 regression。

R5.7 的 Better STM 框架在阶段性上有价值：它暴露了 attribution boundary、candidate-only、no-regression、blind judge 与 anti-gaming 等风险。但若继续放在 active 主路径，会让后续工作误以为本文要证明“哪个 STM 更好”或“`fcstm` 表达更强”。因此本 PR 将这些资产整体迁入本 snapshot。

## 2. 本快照包含什么

| 子树 | 文件 / 链接数 | 历史内容 | 当前使用方式 |
|---|---:|---|---|
| [experiment_design/](./experiment_design/) | 42 | R5.7.1 evaluation logic、R5.7.2 Better STM definition / repair target taxonomy、R5.7.3 objective metrics、R5.7.4 static adjudication、R5.7.5 constructed / blind adjudication prompt 与 schema、旧 scope / eligibility。 | 只能作为 historical / calibration / negative reference；不能直接迁回 active protocol。 |
| [pipeline/evaluation/](./pipeline/evaluation/) | 818 | R4/R5.7 evaluation gate、schemas、dry-run examples、constructed `STM_k` bundles、blind judge outputs、tests。 | 整体归档；若 diagnostic / scenario schema 未来仍有价值，必须由后续 issue lifecycle PR 重新定义字段。 |
| [pipeline/representation/](./pipeline/representation/) | 19 regular files + 4 symlinks | R5.7.4 为 static adjudication / R5.7.5 constructed `STM_k` handoff 物化的 standalone baseline `.fcstm` bundle 与 symlink fan-in。 | 只作 historical baseline evidence；active representation 仍以主路径 R4.5 selected smoke exports 为准。 |
| [reports/](./reports/) | 6 | R5.7.1--R5.7.5 六份 human-facing reports。 | 历史报告链；不证明真实 repair-loop effectiveness。 |

本 snapshot payload 当前共包含 **889** 个条目（885 个 regular files + 4 个 symlinks）；若计入本 archive 入口 [README.md](./README.md) 与 [PATH_MAPPING.md](./PATH_MAPPING.md)，总计 **891** 个条目。

### 2.1 representation symlink 说明

[pipeline/representation/](./pipeline/representation/) 中的 4 个 symlink 是 R5.7.4 / R5.7.5 历史 logical bundle fan-in 的一部分。其中 `0001` / `0018` 指向本 archive 内物化的 R5.7.4 standalone exports；`0000` / `0045` 指向仍在 active 主路径维护的 R4.5 selected-smoke representation exports。当前这 4 个 symlink 已由测试覆盖且均可解析；若后续重构 active R4.5 representation 路径，必须同步保持这些 historical symlink 可读，或在新的 archive-maintenance PR 中将对应目标物化进本 snapshot。

## 3. 禁止外推

从本目录不得推出以下结论：

1. 已经证明真实 repair loop 有效。
2. constructed `STM_k` 是 agent loop 输出。
3. blind adjudication judge agreement 可作为正式方法效果。
4. Better STM gate / objective metric framework / repair target taxonomy 仍是 active evaluation endpoint。
5. `fcstm` / `pyfcstm` 是 paper1 contribution。

## 4. 当前替代入口

| 需要判断什么 | 当前入口 |
|---|---|
| paper1 当前任务与贡献口径 | [../../README.md](../../README.md), [../../story/README.md](../../story/README.md) |
| 资产清账和归档决策依据 | [../../evidence/ledgers/paper1_strategy_asset_map.md](../../evidence/ledgers/paper1_strategy_asset_map.md), [../../evidence/audits/2026-07-07-post-strategy-asset-scan.md](../../evidence/audits/2026-07-07-post-strategy-asset-scan.md) |
| 后续 source-level issue lifecycle protocol | [../../experiment_design/README.md](../../experiment_design/README.md) |
| 后续 evaluation placeholder | [../../pipeline/evaluation/README.md](../../pipeline/evaluation/README.md) |
| active reports 总账 | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |

## 5. 路径映射

完整资产级映射见 [PATH_MAPPING.md](./PATH_MAPPING.md)。archive 内部旧文档的相对链接可能仍反映迁移前布局；阅读历史材料时应先回到本 README 和 [PATH_MAPPING.md](./PATH_MAPPING.md)，不要把旧链接误当 active 入口。

## 6. 迁移纪律

1. 本目录内容原则上保持历史原样，不为了当前 story 改写历史报告结论。
2. 后续若确需复用某条 discipline（如 no-regression、anti-gaming、blind prompt consistency），必须在新的 `PR-<short-slug>` 中重新定义为 source-level issue lifecycle 规则，并显式引用本 archive 为历史来源。
3. 不允许从 archive 中直接恢复 Better STM headline、`can_claim_better_stm` gate 或 constructed `STM_k` answer key 到 active 主路径。
