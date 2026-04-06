# `manual_review/batches/` README

本目录用于存放 `2025` 年度人工复核的**最终批次文件**。

默认规则：

1. 当前按 **venue 对应的 `metadata/*.json` 文件名** 组织，例如 `ase_conf_a.json`、`tosem_journal_a.json`。
2. 当前只保留与 [../../../CCF_SE_A_B_C.md](../../../CCF_SE_A_B_C.md) 对齐的保留 venue 批次文件。
3. 每个文件都包含完整的 `entries` 数组；数组中的每个对象表示该 venue 下某篇论文的最终人工裁决，字段口径与上级 [../overrides.json](../overrides.json) 一致。
4. 分类器会自动读取本目录下所有 `*.json` 的 `entries` 字段，并覆盖启发式初判。
5. 若后续需要补做或重修某个 venue 的人工终判，直接重写对应文件即可，不需要拆成新的临时任务格式。

推荐流程：

1. 先基于 [../README.md](../README.md) 明确当前批次的字段口径。
2. 逐篇人工检查标题、摘要、官方页；边界不清楚时再看全文。
3. 直接更新对应 venue 文件中的 `entries`。
4. 重跑 [../../../../../tools/ccf_se_classifier.py](../../../../../tools/ccf_se_classifier.py)。
