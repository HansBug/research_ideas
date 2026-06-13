# baselines/：LLM-based SLR 近邻 baseline 文库

## 1. 定位

本目录服务于第二篇 **agent-based SLR** 论文的 Related Work、novelty gate 与审稿风险控制。它不是最终系统综述结果，而是用于回答一个前置问题：近三年 CCF A/B/C 软件工程及邻近 venue、近两年 arXiv 中，是否已经存在足以打穿本文 story 的 **LLM-based SLR / LLM-assisted evidence synthesis / agentic literature-review workflow**。

当前 PR-B0 的结论必须保守使用：本轮已把 34 篇可得 PDF 条目升级为 `paper_content.txt` 全文文本核验与七维评分，但多数条目尚未人工逐页核对 PDF 图表；正式写入 Related Work / novelty matrix 前，仍需回到单篇 `review.md`、`paper_content.txt` 和关键 PDF 图表做最终复核。

## 2. 当前状态

| 项 | 数量 / 状态 |
|---|---:|
| arXiv 近邻候选 | 34 |
| 本地建库候选 | 34 |
| P0 强 baseline | 10（本地 10，全文文本核验 10） |
| P1 高度关注 | 15（本地 15，全文文本核验 15） |
| P2 背景相关 | 9（本地 9，全文文本核验 9） |
| CCF title-level 命中 | 1 条 CCF-adjacent / ICSE workshop 线索，仍需人工全文 |
| 人工下载清单 | [search/manual-download-needed.bib](./search/manual-download-needed.bib) |

## 3. 文件说明

| 文件 / 目录 | 作用 |
|---|---|
| [GUIDE.md](./GUIDE.md) | 固化检索、筛选、七维评分、PDF 获取、人工下载、SUMMARY 回填与 `review.md` 写作规则。 |
| [SUMMARY.md](./SUMMARY.md) | PR-B0 baseline 总账：候选统计、阅读状态 / 证据等级、输入输出方法主表、D1-D7 七维总表、强 baseline 威胁、story 调整建议和风险。 |
| [search/](./search/) | 检索日志、arXiv query 原始快照、去重候选池、CCF coverage / gap、CCF 粗筛、DBLP title 扫描原始快照与人工下载 BibTeX。 |
| [papers/](./papers/) | 单篇 baseline 目录；每篇至少包含 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`review.md`。 |

## 4. 阅读顺序

1. 先读本 [README.md](./README.md) 明确文库边界。
2. 再读 [GUIDE.md](./GUIDE.md) 明确 D1-D7 与维护规则。
3. 再读 [SUMMARY.md](./SUMMARY.md) 获取当前结论和 story 风险。
4. 需要复核检索证据时进入 [search/](./search/)。
5. 需要写 Related Work 或 novelty matrix 时进入 [papers/](./papers/) 的单篇目录，优先读 `review.md`，再回到 `paper_content.txt` / `paper.pdf` 核验。

## 5. 与其他目录的关系

1. 本目录的 baseline 威胁应回写到 [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) 与 [../story/claim_evidence_map.md](../story/claim_evidence_map.md)。
2. 若某篇 baseline 后续用于正式引用，BibTeX 应同步到 [../evidence/references.bib](../evidence/references.bib) 或论文写作阶段的正式 `references.bib`。
3. 本目录不替代 [../experiment_design/](../experiment_design/)；它只约束后续实验必须比较或讨论哪些近邻能力。

## 6. 禁止误读

- 不得把本轮粗筛写成“已完成系统综述”。
- 不得把 arXiv 版本写成正式 CCF 发表事实，除非已核验正式版本。
- 不得用“没有 CCF 主会命中”支撑强 novelty；当前 CCF 仅 title-level / coverage-gap 粗筛。
- 不得再声称“首次 LLM/agent 自动化 SLR”；P0 baseline 已经覆盖多个强近邻。
