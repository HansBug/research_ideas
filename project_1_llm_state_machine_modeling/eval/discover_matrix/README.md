# discover 矩阵审计工具

从 `runs/paper1/audit-20260727-claudecode/` 迁来。

## 为什么放在这里

`runs/` 只存运行产物，整个目录被 gitignore。这两个脚本是**审计工具**，不是产物：它们决定预期缺陷的命中判据，也就是矩阵实验的头号指标怎么算。放在 `runs/` 里的直接后果已经发生过一次——2026-07-29 重装系统后，`build_gist.py` 因为在加 ignore 之前就被跟踪而幸存，它依赖的 `audit_v4.py` 从未被提交，直接丢失，只能对着已发布的 matrix-v11 审计包反推重建。

## 先读裁决原则与已知缺口

[HIT_CRITERION.md](./HIT_CRITERION.md) 定义什么算命中；[GROUND_TRUTH_LIMITATIONS.md](./GROUND_TRUTH_LIMITATIONS.md) 记录分母**系统性不覆盖**什么，以及每处缺口是问题定义边界还是待补欠账——引用召回率前必须读后者，否则会把「问题定义不做的类」误报成「方法没检出」。

引用任何命中数字前，先确认用的是 frozen ledger 而非 `expected_issues_reconstructed.json` ——后者仅覆盖 4 个 pair，且已知把 `EXP-0029-SH-001` 写严，据它算出的命中率是错的。

⛔ **引用任何多报 / over-report 数字前，必读 [REPRESENTATION_DEBT.md](./REPRESENTATION_DEBT.md)。**
v46 实测：未匹配台账的 278 类去重产出里 **129 类（46.1%）不是模型缺陷，而是我们自己 R4.5 编译
（PlantUML → FCSTM）的信息损失**——作者在 `stm0.puml` 里已逐字写全，`model.fcstm` 装不下才被压平，
且压平已由 `fcstm_meta.json` 的债务码如实登记。**把它们计入多报会同时高估模型的乱报程度、
又掩盖编译链的问题。** 该文件给出定义、三条操作化判据、实例与论文表述口径。

⚠️ 判定表示债务必须回读**作者源 `stm0.puml`**，只读 `model.fcstm` 必然看不出来——
v46 的八个独立判定组里有七组栽在这一点上。

## 文件

- `build_gist.py <matrix_dir> <out_dir>` —— 读一个矩阵运行目录，产出 `readable/` 与 `audit/` 两套 bundle 以及逐格表格。命中判据在 `expected_verdicts()`。
- `audit_v4.py` —— `build_gist.py` 的两个依赖：`_walk`（按键名递归取值，因为不同节点把同名字段写在不同深度）与 `_segment_macro_sources`（从 frozen trace 的排除表反推被转换器拆成多段的源迁移）。
- `launch_cells_serial.sh` —— 串行启动单元格的历史脚本，保留作参考。

## 预期缺陷台账：已丢失，已重建，已校准

命中判据需要 `.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`。该文件从未被 git 跟踪，已在 2026-07-29 重装中丢失，且无法从已发布的 bundle 恢复—— bundle 保留了判定结果，没保留判据所解析的 `eval_assert` 原文。

- `expected_issues_reconstructed.json` 是重建物，覆盖 8 格矩阵用到的 4 对。权威内容来自 issue #166（它对这 4 对的记录与丢失台账逐项一致）；机器可核验的路径集是对着各 pair 自己的 `fcstm.fcstm` 解析出来的，每条都附上它所指的缺陷边原文。`EXP-0006-EA-001` 的 `eval_assert` 是**原件**（在会话记录里幸存），其余四条是重建。
- **重建物不以"看起来合理"被接受。** `test_ledger_reconstruction.py` 要求它在 matrix-v11（最后一次在真台账下产出的矩阵）上复现该台账给出的 12 条判定、其中 10 条命中。判据对"某条预期缺陷究竟点名了哪些路径"高度敏感——无触发事件时要求状态**全匹配**，多列一个状态就会把真命中判成漏。0029 的结构缺陷正是这种情形：#166 描述为三个兄弟状态，而 v11 的命中项只绑定了两个。
- `calibration_matrix_v11.json` 保存该校准所需的输入。运行目录按设计不被跟踪，上一个已经丢了，所以校准的输入必须自己留一份。
- 真台账一旦恢复即自动优先（`_expected_ledger_path()`），且所用来源会写入每个审计制品的 `expected_ledger_provenance` 字段——命中率是头号数字，读者必须能自己看出它是不是建立在重建物上，而不是听谁说。

## v46 全量矩阵（2026-08）

⛔ **v46 的全部材料集中在 [v46/](./v46/)，唯一入口是 [v46/README.md](./v46/README.md)**
——核心结论、覆盖侧与多报侧统计都在那里，细节引向各 sub md。

跨代次通用的裁定口径留在本目录：
[UNEXPECTED_TAXONOMY.md](./UNEXPECTED_TAXONOMY.md)（多报侧五类定义与判定流程，**判任何一条
未匹配产出前必读**）、[REPRESENTATION_DEBT.md](./REPRESENTATION_DEBT.md)（表示债务，
**引用多报数字前必读**）、[PREDICATE_DEFECTS_REGISTERED.md](./PREDICATE_DEFECTS_REGISTERED.md)。

派生物由 [rebuild_unexpected.py](./rebuild_unexpected.py) 从 `v46/unexpected_verdicts/G*.jsonl`
一键重建（`--check` 可用于 CI）。
