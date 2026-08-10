# discover 矩阵审计工具

从 `runs/paper1/audit-20260727-claudecode/` 迁来。

## 为什么放在这里

`runs/` 只存运行产物，整个目录被 gitignore。这两个脚本是**审计工具**，不是产物：它们决定预期缺陷的命中判据，也就是矩阵实验的头号指标怎么算。放在 `runs/` 里的直接后果已经发生过一次——2026-07-29 重装系统后，`build_gist.py` 因为在加 ignore 之前就被跟踪而幸存，它依赖的 `audit_v4.py` 从未被提交，直接丢失，只能对着已发布的 matrix-v11 审计包反推重建。

## 先读裁决原则与已知缺口

[HIT_CRITERION.md](./HIT_CRITERION.md) 定义什么算命中；[GROUND_TRUTH_LIMITATIONS.md](./GROUND_TRUTH_LIMITATIONS.md) 记录分母**系统性不覆盖**什么，以及每处缺口是问题定义边界还是待补欠账——引用召回率前必须读后者，否则会把「问题定义不做的类」误报成「方法没检出」。

引用任何命中数字前，先确认用的是 frozen ledger 而非 `expected_issues_reconstructed.json` ——后者仅覆盖 4 个 pair，且已知把 `EXP-0029-SH-001` 写严，据它算出的命中率是错的。

⛔ **引用任何多报 / over-report 数字前，必读 [REPRESENTATION_DEBT.md](./REPRESENTATION_DEBT.md)。**
v46 实测：未匹配台账的 **278 个同质簇（去重到 117 处不同内容）**里，
**129 簇 / 27 处（条目 46.4% / 去重 23.1%）不是模型缺陷，而是我们自己 R4.5 编译
（PlantUML → FCSTM）的信息损失**——作者在 `stm0.puml` 里已逐字写全，`model.fcstm` 装不下才被压平，
且压平已由 `fcstm_meta.json` 的债务码如实登记。**把它们计入多报会同时高估模型的乱报程度、
又掩盖编译链的问题。** 该文件给出定义、三条操作化判据、实例与论文表述口径。

⚠️ **条目份额与去重份额不可互换**，引用时必须写清用的是哪一套分母；两套数字的机器产地是
[v46/unexpected_tables.md](./v46/unexpected_tables.md) 表 1。同一批产出的净增量（真实台账漏记）
**只有 1 条**。

⚠️ 判定表示债务必须回读**作者源 `stm0.puml`**，只读 `model.fcstm` 必然看不出来——
v46 的八个独立判定组里，只有回读了作者源的那一组识别出了编译债务。

## 文件

- `build_gist.py <matrix_dir> <out_dir>` —— 读一个矩阵运行目录，产出 `readable/` 与 `audit/` 两套 bundle 以及逐格表格。命中判据在 `expected_verdicts()`。
- `audit_v4.py` —— `build_gist.py` 的两个依赖：`_walk`（按键名递归取值，因为不同节点把同名字段写在不同深度）与 `_segment_macro_sources`（从 frozen trace 的排除表反推被转换器拆成多段的源迁移）。
- `launch_cells_serial.sh` —— 串行启动单元格的历史脚本，保留作参考。

## 预期缺陷台账：原件，已校验

命中判据读 `.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`。
当前装着的是**原件**：370994 字节，SHA-256
`03d8756650c079229dacb7fc2d7700ca98fda44f3c4648fd308e4f8e24ac955e`，与 issue #166 正文
「机器总账 SHA-256」逐字符一致；来源记录见同目录 `PROVENANCE.md`，找回过程见
[HIT_CRITERION.md](./HIT_CRITERION.md) §7。

复核命令：

```bash
L=../../../.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json
wc -c "$L" && sha256sum "$L"
```

- 该文件**不被 git 跟踪**（体积与来源所限），所以每台机器都要自己装一份并核 SHA。
  它丢失过一次（2026-07-29 重装），因此这条校验不是形式主义。
- `_expected_ledger_path()` 优先取原件；实际所用来源写入每个审计制品的
  `expected_ledger_provenance` 字段——命中率是头号数字，读者必须能自己看出它建立在
  什么之上，而不是听谁说。
- `expected_issues_reconstructed.json` 与 `calibration_matrix_v11.json` 是原件缺席时的
  退路（覆盖 8 格矩阵用到的 4 对），`test_ledger_reconstruction.py` 要求它在 matrix-v11
  上复现该台账给出的 12 条判定、其中 10 条命中。**v46 未使用退路**。

## v46 全量矩阵（2026-08）

⛔ **v46 的全部材料集中在 [v46/](./v46/)，唯一入口是 [v46/README.md](./v46/README.md)**
——核心结论、覆盖侧与多报侧统计都在那里，细节引向各 sub md。

跨代次通用的裁定口径留在本目录：
[UNEXPECTED_TAXONOMY.md](./UNEXPECTED_TAXONOMY.md)（多报侧五类定义与判定流程，**判任何一条
未匹配产出前必读**）、[REPRESENTATION_DEBT.md](./REPRESENTATION_DEBT.md)（表示债务，
**引用多报数字前必读**）、[PREDICATE_DEFECTS_REGISTERED.md](./PREDICATE_DEFECTS_REGISTERED.md)
（测量链侧缺陷，已实施 / 未实施两栏；**「谓词词表冻结」不等于「谓词实现冻结」**，该文件写清了分界）。

派生物由 [rebuild_unexpected.py](./rebuild_unexpected.py) 从 `v46/unexpected_verdicts/G*.jsonl`
一键重建（`--check` 可用于 CI）。

## 历代材料索引

事前登记与历代分析结果不被正文引用，但删不得——事前登记的全部价值来自它写在运行之前。

| 文件 | 内容 |
| :-- | :-- |
| [V40_PREREGISTERED.md](./V40_PREREGISTERED.md) ｜ [V41](./V41_PREREGISTERED.md) ｜ [V43](./V43_PREREGISTERED.md) ｜ [V44](./V44_PREREGISTERED.md) ｜ [V45](./V45_PREREGISTERED.md) ｜ [v46](./v46/preregistered.md) | 各代次事前登记（判据、达标档位、回归红旗） |
| [V23_MOTIVE_AUDIT.md](./V23_MOTIVE_AUDIT.md) | 引入动机溯源——泄漏审查（CLAUDE.md §3.5.-1）的材料 |
| [V24_REPORT_DETERMINED.md](./V24_REPORT_DETERMINED.md) | v24 与判定无关的已定部分 |
| [V25_ABLATION_RESULT.md](./V25_ABLATION_RESULT.md) | 判定装置消融结果 |
| [OVERREPORT_ADJUDICATION_V23.md](./OVERREPORT_ADJUDICATION_V23.md) | v22 数据的多报核验 |
| [OBLIGATION_SOURCE_GAP.md](./OBLIGATION_SOURCE_GAP.md) | `wellformedness` 漏检的构造性根因 |
| [DENOMINATOR_EXHAUSTION.md](./DENOMINATOR_EXHAUSTION.md) | ⛔ hold-out 时代，结论已作废，仅供追溯 |

⛔ 纯施工台账（进度、试跑计划、变更清单、已撤销提案）不入库——它们属 GitHub PR / issue，
见 [CLAUDE.md](../../../CLAUDE.md) §9。
