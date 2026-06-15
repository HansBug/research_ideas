# Execution of Partial State Machine Models — artifacts / resource 盘点

## 1. 一手资源入口

| 资源对象 | 当前判断 |
|---|---|
| 论文本体 | [IEEE DOI](https://doi.org/10.1109/TSE.2020.3008850)；[arXiv](https://arxiv.org/abs/2103.17194) |
| 作者代码 / 工具 | 论文给出 PMExec repository：`https://moji1@bitbucket.org/moji1/partialmodels.git`；可尝试入口 [Bitbucket partialmodels](https://bitbucket.org/moji1/partialmodels) |
| NL / 输入数据 | 不适用；论文任务没有自然语言需求输入 |
| STM / repair case / 输出 | 论文使用 UML-RT partial HSM / Papyrus-RT models；原文称 scripts and models publicly available，但需后续核验仓库当前可访问性 |
| 原生 repair / refinement case | PMExec use cases 与 partial UML-RT refinement；属于 `STM_0 -> refined/executable STM`，不是 `<NL, STM_0> -> STM_k` |
| 许可 | 待核 |
| 版本 / commit / hash | 待冻结 |

## 2. 本地证据容器

本目录中的 `paper.pdf`、`paper_content.txt` 与 `bibtex.bib` 只作为本仓库审计材料，不等同于论文一手公开资源。资源可获取性判断必须以上表的一手入口为准。

## 3. 可复现阻塞

- 需确认 Bitbucket 仓库当前是否可访问、是否仍包含 PMExec、scripts、models 与 use cases。
- 需冻结 Papyrus-RT、Epsilon、ANTLR、Boost、C++ toolchain 与 PMExec commit。
- 该工作没有 NL 输入和 LLM repair loop，不能直接变成本文实验同构 baseline；若后续使用，只能作为 partial-state-machine execution / refinement 对照。
