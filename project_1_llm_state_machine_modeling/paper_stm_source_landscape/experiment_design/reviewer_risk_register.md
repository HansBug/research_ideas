# Reviewer Risk Register

## 1. C/I/M 口径

C/I 只用于影响学术目标、事实准确性、实验可靠性、claim-evidence、可复现证据链的问题；纯工程风格最高 M。

## 2. 当前风险总表

| 风险 | 等级 | 为什么影响学术目标 | 当前缓解 |
|---|---|---|---|
| 漏掉 direct competitor | C | 会打穿 #85 gap / novelty | 69 行初筛 + targeted search audit + P0/P1 下载队列 |
| metadata-only 被写成 verified | C | 会导致 Related Work 和 claim 失真 | relation_level / verification_status 升级规则 |
| 7 条 auto-fulltext Skip 过早排除 | C | 可能漏掉 near neighbor | 独立 gate CSV，复查前不得最终排除 |
| P0/P1 BibTeX 不完整 | I | 用户无法下载，全文核验断链 | `manual_download_needed.bib` 已落地 |
| #95 输入快照不可复验 | I | 438 -> 69 过程无法审计 | `INPUT_SNAPSHOT.md` + `screening_audit.csv` |
| 只建文献清单，不建 paper workspace | C | 无 story / claim / RQ / risk gate | 已复刻 PR #96 同构结构 |
| 版权污染 | C | artifact 不能公开复验 | 本 PR 不提交 PDF/全文，后续 G0 |
| 带顺序含义的版本化命名 命名误导 | I | 暗示与 `paper_v1` 前后置关系 | 固定 `paper_stm_source_landscape/` |
