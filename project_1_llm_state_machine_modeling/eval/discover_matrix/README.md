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

## 文件

- `build_gist.py <matrix_dir> <out_dir>` —— 读一个矩阵运行目录，产出 `readable/`
  与 `audit/` 两套 bundle 以及逐格表格。命中判据在 `expected_verdicts()`。
- `audit_v4.py` —— `build_gist.py` 的两个依赖：`_walk`（按键名递归取值，因为不同
  节点把同名字段写在不同深度）与 `_segment_macro_sources`（从 frozen trace 的排除
  表反推被转换器拆成多段的源迁移）。
- `launch_cells_serial.sh` —— 串行启动单元格的历史脚本，保留作参考。

## 外部依赖（不在本仓库内）

命中判据需要预期缺陷台账：
`.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`。
该文件从未被 git 跟踪，且已在 2026-07-29 重装中丢失。缺失时 `_expected_paths()`
会抛 `FileNotFoundError`——这是**有意的**：没有 ground truth 就不该产出命中数字。
