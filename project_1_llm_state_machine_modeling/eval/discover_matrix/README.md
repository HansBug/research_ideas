# discover 矩阵审计工具

从 `runs/paper1/audit-20260727-claudecode/` 迁来。

## 为什么放在这里

`runs/` 只存运行产物，整个目录被 gitignore。这两个脚本是**审计工具**，不是产物：
它们决定预期缺陷的命中判据，也就是矩阵实验的头号指标怎么算。放在 `runs/` 里的
直接后果已经发生过一次——2026-07-29 重装系统后，`build_gist.py` 因为在加 ignore
之前就被跟踪而幸存，它依赖的 `audit_v4.py` 从未被提交，直接丢失，只能对着已发布
的 matrix-v11 审计包反推重建。

判据本身也不该只活在一个人的机器上：命中判据被修正过三次（关键词匹配 → 路径交集
带一层容差 → 以触发事件为锚），每一次都是因为前一版会把错误的 issue 记成命中。
这种东西必须可追溯。

## 先读裁决原则

[HIT_CRITERION.md](./HIT_CRITERION.md) 是「命中」的定义所在：**语义同一性优先于标签一致**。
`expected_verdicts()` 的路径重叠只是它的机械近似，不是终局；该文件同时列出机械判据已知会
误判的风险面（无-trigger 分支的 family 交集检查，涉及 10 / 47 条台帐条目、9 个 pair），
以及必须人工复核的三种情形。

引用任何命中数字前，先确认用的是 frozen ledger 而非 `expected_issues_reconstructed.json`
——后者仅覆盖 4 个 pair，且已知把 `EXP-0029-SH-001` 写严，据它算出的命中率是错的。

## 文件

- `build_gist.py <matrix_dir> <out_dir>` —— 读一个矩阵运行目录，产出 `readable/`
  与 `audit/` 两套 bundle 以及逐格表格。命中判据在 `expected_verdicts()`。
- `audit_v4.py` —— `build_gist.py` 的两个依赖：`_walk`（按键名递归取值，因为不同
  节点把同名字段写在不同深度）与 `_segment_macro_sources`（从 frozen trace 的排除
  表反推被转换器拆成多段的源迁移）。
- `launch_cells_serial.sh` —— 串行启动单元格的历史脚本，保留作参考。

## 预期缺陷台账：已丢失，已重建，已校准

命中判据需要 `.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`。
该文件从未被 git 跟踪，已在 2026-07-29 重装中丢失，且无法从已发布的 bundle 恢复——
bundle 保留了判定结果，没保留判据所解析的 `eval_assert` 原文。

- `expected_issues_reconstructed.json` 是重建物，覆盖 8 格矩阵用到的 4 对。权威内容
  来自 issue #166（它对这 4 对的记录与丢失台账逐项一致）；机器可核验的路径集是对着
  各 pair 自己的 `fcstm.fcstm` 解析出来的，每条都附上它所指的缺陷边原文。
  `EXP-0006-EA-001` 的 `eval_assert` 是**原件**（在会话记录里幸存），其余四条是重建。
- **重建物不以"看起来合理"被接受。** `test_ledger_reconstruction.py` 要求它在
  matrix-v11（最后一次在真台账下产出的矩阵）上复现该台账给出的 12 条判定、其中 10 条
  命中。判据对"某条预期缺陷究竟点名了哪些路径"高度敏感——无触发事件时要求状态**全
  匹配**，多列一个状态就会把真命中判成漏。0029 的结构缺陷正是这种情形：#166 描述为
  三个兄弟状态，而 v11 的命中项只绑定了两个。
- `calibration_matrix_v11.json` 保存该校准所需的输入。运行目录按设计不被跟踪，上一个
  已经丢了，所以校准的输入必须自己留一份。
- 真台账一旦恢复即自动优先（`_expected_ledger_path()`），且所用来源会写入每个审计制品
  的 `expected_ledger_provenance` 字段——命中率是头号数字，读者必须能自己看出它是不是
  建立在重建物上，而不是听谁说。
