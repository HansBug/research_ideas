# Synthesizing Statecharts from Multiple Interrelated Scenarios

## R1.5 strict seed 全文核验结论

| 字段 | 结论 |
|---|---|
| candidate_id | `scenarios-statecharts-interrelated` |
| source_batch | baseline / local fulltext |
| local_source | [baselines/synthesizing-statecharts-from-multiple-interrelated-scenarios/](../../../../baselines/synthesizing-statecharts-from-multiple-interrelated-scenarios/) |
| citation | Simona Vasilache and Jiro Tanaka. 2001. *Synthesizing Statecharts from Multiple Interrelated Scenarios*. International Symposium on Future Software Technology. |
| strict_seed_grade | `NN-D` |
| artifact_usability | `SA-3` |
| exclude_code | `EX-P1-STRUCTURED-SCENARIO-NOT-NL` |
| 当前结论 | 不应进入 strict SS-A/SS-B 种子集；可作为“场景图 / event trace diagrams 到 statecharts”的历史背景与规则式合成参考。 |

## P1/P2/P3/P4 核验

| 谓词 | 判断 | 证据指针 |
|---|---|---|
| P1_NL_INPUT | fail | 论文说 scenarios 用于捕获需求，但本文后续明确采用 OMT event trace diagrams；`paper_content.txt` Page 1 lines 49-66 说明场景表示为 event trace diagram，每个对象是竖线、事件是箭头。方法输入不是原始自然语言需求文本。 |
| P2_T0_STM_FAMILY | pass | `paper_content.txt` Page 1 lines 29-36 将 statecharts 定义为带 hierarchy 和 orthogonality 的 finite state machines；Page 2 lines 84-89 说明 statechart 是 states 与 labeled transitions 构成的 graph。 |
| P3_GENERATION_RELATION | partial-pass | `paper_content.txt` Page 1 lines 8-15 与 Page 2 lines 79-114 明确提出从 multiple/single scenarios synthesizing/generating statecharts；但 generation relation 是 structured scenario / event trace diagram -> statechart，不是 NL requirement -> STM。 |
| P4_EVIDENCE_POINTER | pass | 本地全文、PDF、BibTeX 均存在；核心证据可定位到 `paper_content.txt` Page 1-6 与 Fig.1-Fig.9。无机器可读输入输出样例。 |

## SS / SA 判定

| 维度 | 判断 | 理由 |
|---|---|---|
| SS | `NN-D` | P1 失败。论文标题与摘要含 requirements/scenarios，但正式方法从 OMT event trace diagrams / scenario diagrams 出发，不能作为自然语言需求到 STM 的 strict seed。 |
| SA | `SA-3` | 只有 paper-only 证据；PDF、抽取文本、BibTeX 可用，但没有公开代码、数据集、supplementary bundle、机器可读 statechart 或 scenario files。 |
| R2 可用性 | low / not eligible | 不适合直接进入 R2 自动 repair/conversion。若后续需要，只能人工从 Fig.1-Fig.9 重建 ATM scenario/statechart 小例子，并显式标注为人工派生。 |

## 关键证据摘要

论文目标是“从多个互相关联的 scenarios 综合 statecharts”。全文给出了从单个 event trace diagram 到 statechart 的 Rule 1，并进一步给出 succession、disjunction、conjunction、recurrence、cause-effect、generalization 等多场景合并规则。输出模型属于 statechart / hierarchical state machine 家族，且有清晰的 generation/synthesis 关系。

排除原因在于输入侧。论文虽然把 scenario 视为需求捕获手段，但明确采用 OMT event trace diagrams 作为本文表示，ATM 示例也是对象生命线和事件箭头构成的结构化场景图。该输入已经是半形式化/图式化需求表示，不满足 strict seed 对 NL_INPUT 的要求。

## 待补 / 主要阻塞

| 项 | 状态 |
|---|---|
| DOI | 待补；BibTeX 与源 DESC 均未提供 DOI。 |
| Artifact / 数据 | 主要阻塞；论文未给出代码、仓库、数据集或 supplementary。许可 / 再分发不作为额外升绿阻塞。 |
| URL 稳定性 | 待补；BibTeX URL 是筑波大学实验室 PDF 页面，属于机构主页链接，不是 DOI / publisher landing page / archival artifact。 |
| R2 输入输出样例 | 主要阻塞；只有论文图示，缺少机器可读 scenario/statechart 文件。 |

## 复核顺序

本次只读了源目录 `bibtex.bib -> paper_content.txt -> DESC.md`；`paper_content.txt` 已覆盖全文关键证据，未打开 `paper.pdf`。
