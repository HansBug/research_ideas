# A1 S1--S8 Round 3：19 篇一篇一 agent 独立抽取审计

本目录记录 PR-A1 中针对 `survey_of_surveys/` 的第三轮 S1--S8 与原生维度树 / 维度森林独立审计。

## 目标

1. 每篇 survey / secondary study 由一个独立 subagent 处理，禁止一个 agent 混读多篇，也禁止 sub-subagent。
2. 每个 subagent 必须全文阅读对应单篇的 `bibtex.bib`、`paper_content.txt`、`review.md`、`evidence_chain.md`，必要时核对 `paper.pdf`。
3. 输出只写入本目录的单篇审计文件，不直接修改 `review.md`，由主线程统一裁决后回填。
4. 审计口径遵循 [GUIDE.md](../../../GUIDE.md) §6.3/§6.4：优先复原原文自己的样本编码维度树 / 维度森林，区分原文事实、本地复原、统计池资格与 A2a 待核验。

## 使用方式

- `*.md`：每篇单独 subagent 审计结果。
- `TASKS.tsv`：本轮任务映射。
- `round3-main-adjudication.md`：主线程对本轮审计的采纳、拒收与返修记录。

本目录是 A1 文本级审计证据，不是 Paper2 最终定量统计证据。
