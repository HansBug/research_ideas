# survey_of_surveys/audits/：审计批次入口

本目录保存 `survey_of_surveys/` 文库的专项审计批次。这里的审计不是普通运行日志，而是用于支撑 Paper2 学术证据链、后续 A2a/A2b 接力和 PR review 复验的可追溯制品。

## 当前批次

> [!WARNING] v1-deprecated: [a1dt-19x3/](./a1dt-19x3/) 是旧批次历史归档；不得把其中结论直接当作 A1-DT v2 当前事实。当前执行入口是 [a1dt-v2-19x3/](./a1dt-v2-19x3/)。


| 批次 | 目标 | 状态 | 入口 |
|---|---|---|---|
| A1-DT v2 19×3 原生维度树审计 | 按 PR #135 v2 纪律重新审计当前 19 篇论文：维度树必须复原“该综述如何描述、编码、分类、统计其样本单位”，并由 codex / `claude -p` / `codex-deepseek exec` 三路独立读取全文。 | 当前执行批次；57 份 prompt 已物化；结果、日志、主线程裁决和 review.md 返修均写入本批次。 | [a1dt-v2-19x3/README.md](./a1dt-v2-19x3/README.md) |
| A1-DT v1 19×3 全文审计 | 对旧版 `review.md` 的维度树复原进行 codex / claude / deepseek 三路全文审计；该批次基于 v1“原文 schema 主树 + 通用接口投影”口径。 | **v1-deprecated：已完成 57/57，但只作为历史归档和返修来源，不是当前事实口径。** | [a1dt-19x3/README.md](./a1dt-19x3/README.md) |

## 维护纪律

1. 新增审计批次必须有独立子目录、批次 README、任务清单、原始 prompt、日志、结果和复验命令。
2. 审计结果可以指出 C/I/M 问题，但不能直接替代原文证据；单篇 `review.md` 的事实真源仍必须回到 `paper_content.txt`、`paper.pdf` 和文末 A.1--A.4 审计附录。
3. 若审计只完成结构返修而未完成页码 / 表号 / 图号精核，必须显式保留 `schema_seed`、`not_verified`、`needs_manual_check` 等降级状态。
4. 任何跨论文 SUMMARY 归纳都必须回链单篇 A.3 结论；批次审计只作为复核证据和返修依据，不得绕过单篇证据链。
