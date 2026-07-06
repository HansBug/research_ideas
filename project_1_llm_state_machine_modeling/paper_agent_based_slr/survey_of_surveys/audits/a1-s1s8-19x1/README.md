# A1-S1S8-19x1：survey_of_surveys 自身 schema 独立审计

本目录记录 PR-A1 中针对 `survey_of_surveys` 自身 S1--S8 二级 schema 的“一篇论文一个独立 subagent”审计批次。它不同于 [../a1dt-v2-19x3/](../a1dt-v2-19x3/)：后者审计单篇原生维度树 / 维度森林，本文档批次只审计每篇论文投影到 S1--S8 后是否事实准确、证据链充分、等级可辩护。

## 目标

1. 19 篇样本文献分别由独立 subagent 只读审计，不允许一个 agent 混读多篇。
2. 每个 subagent 必须阅读全文材料：`bibtex.bib`、`paper_content.txt`、`review.md`、`evidence_chain.md`，必要时回到 `paper.pdf`。
3. 输出必须覆盖：真实类型、样本单位、主统计池候选资格、S1--S8 建议等级、C/I/M 问题、修改建议、原文证据锚点。
4. 主线程只能在审计报告基础上裁决并同步修改 `review.md`、`evidence_chain.md`、[../../SUMMARY.md](../../SUMMARY.md) 和 [../../GUIDE.md](../../GUIDE.md)。

## 文件说明

- [TASKS.tsv](./TASKS.tsv)：19 篇与 subagent 的一对一任务映射。
- `results/<slug>.md`：subagent 原始报告或压缩归档。
- `adjudications/<slug>.md`：主线程裁决、采纳 / 不采纳理由和同步修改记录。
- [check_s1s8.py](./check_s1s8.py)：结构检查脚本，验证 19 篇 `review.md` 是否保留 S1--S8 表格。

## 当前验收口径

- 19/19 篇均有独立审计结果归档。
- 19/19 篇 `review.md` 均有 `## survey_of_surveys 自身 schema 抽取` 小节，并至少包含 S1--S8 各一行。
- 若审计指出事实错误或过强结论，必须同步修正文献总账和证据链，不得只改单篇正文。
- 所有当前 A1 结论仍是 `schema_seed` / `boundary_anchor` 级别；A2a 精确页码、表图和 supplementary 核验前，不进入最终定量统计或 final research finding。
