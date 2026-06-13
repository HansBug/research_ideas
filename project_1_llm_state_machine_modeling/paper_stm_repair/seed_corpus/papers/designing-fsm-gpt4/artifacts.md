# artifacts: designing-fsm-gpt4

## 核验结论

| 项 | 状态 | 结论 |
|---|---|---|
| PDF | present | 本地 `paper.pdf` 存在；来源为 arXiv:2603.29140。 |
| paper_content.txt | present | 已覆盖正文 Page 1-21、表格、附录和参考文献；本轮未发现需要 OCR 的证据缺口。 |
| BibTeX | present | arXiv preprint；未见 DOI。 |
| Code / artifact | partial | 论文正文未给代码 URL；baseline `ASSETS.md` 额外核到 GitHub 仓库 `Paul3246/nl2fsm`。 |
| Dataset / outputs | partial | GitHub 仓库含示例数据、`generated_text.csv`、Graphviz 输出和若干 score 文本；不是冻结 benchmark。 |
| License / redistribution | blocker | GitHub 仓库无 license；不能默认再分发或纳入自动下载复现包。 |
| URL stability | medium-low | arXiv 稳定；GitHub 无 release/tag，需固定 commit。 |
| Conversion readiness | exploratory | 可手工抽取 Page 4 Listing 1.1 与 CSV 输出格式做 seed；正式 converter 需先冻结样例与 license 策略。 |

## 本地证据文件

| 文件 | 路径 | SHA-256 |
|---|---|---|
| BibTeX | `baselines/designing-fsm-specifications-from-requirements-gpt4/bibtex.bib` | `b76108c18dc429d5cf112672930943de045cdf83e7f1a8abf00073f0210717b5` |
| Full text | `baselines/designing-fsm-specifications-from-requirements-gpt4/paper_content.txt` | `6d90ebc9e302574df1cb4ba033a9a348b1110388109495146956dc478eefb947` |
| PDF | `baselines/designing-fsm-specifications-from-requirements-gpt4/paper.pdf` | `d49fd30733aaa7c7d6dd7aeb9f28f72ecc59d0594dcf7bd9da373bbe9ac1628f` |

## 外部入口

| 类型 | URL / 标识 | 稳定性 | 说明 |
|---|---|---|---|
| Paper | https://arxiv.org/abs/2603.29140 | high | BibTeX 与全文一致；公开预印本。 |
| PDF | https://arxiv.org/pdf/2603.29140 | high | 本地 PDF 的来源入口。 |
| Code repo | https://github.com/Paul3246/nl2fsm | medium-low | baseline `ASSETS.md` 核到 default branch `main` HEAD `354f9aacf51b5121abb8a2e04718232185e71928`；论文正文未直接引用该 URL。 |
| Fault-model bundle | `Paul3246/nl2fsm/Fault_model_approach.zip` | medium-low | 仓库内 zip；未核为正式 release artifact。 |

## Artifact 内容可用性

| 内容 | 可用性 | 证据 / 风险 |
|---|---|---|
| 初始 NL description | high | Page 4 Listing 1.1 给出完整英文 DFSM 描述；Appendix Listing 1.5-1.7 给出描述生成 pattern。 |
| 目标输出 schema | high | Page 6 Listing 1.2 固定 `State,Input,Output,Next_State` CSV。 |
| 生成代码 | medium | GitHub 仓库含 `v1`-`v5` 与 `pipeline.py`，但无 release、license、依赖锁。 |
| 合成数据 | medium | 仓库含 `v5/data`、`generated_text.csv` 等线索；论文只描述随机生成过程，没有冻结 split。 |
| 论文结果复现 | low-medium | 仓库含 score 文本和输出目录，但表格结果与代码版本需人工对齐。 |
| 真实 LLM 调用复现 | low | 需要 OpenAI API 环境；必须按仓库 `.env` 与 run record 规范记录 model_id、日期、usage、prompt 和 raw output。 |

## R2 seed / repair artifact 边界

可冻结为条件 seed 的范围仅限：Page 4 Listing 1.1 的 NL description、Page 6 Listing 1.2 的 CSV schema，以及与初始生成直接相关的输出文件。以下 repair 资产可参考但不可直接冻结为 seed：

1. `v1` / syntactic fault repair：对应论文 Section 5.1。
2. `v4` / distinguishing sequence repair：对应论文 Section 5.2。
3. `v5` / checking sequence repair：对应论文 Section 5.3。
4. `Fault_model_approach.zip` / mutation-machine repair：对应论文 Section 5.4。

限制：

- 多数 repair 需要 oracle DFSM 或专家输出答案。
- fault-model 实验中 repair domain 有时被特定转移增强，以保证 oracle 被包含。
- 这些修复输出不应作为初始 strict seed 的目标模型。

## License / hash / URL 稳定性判断

| 维度 | 判断 | 处理建议 |
|---|---|---|
| Paper license | pending | arXiv 页面可公开访问；若要再分发 PDF，后续仍需查 arXiv license 元数据。 |
| Code license | blocker | GitHub 仓库无 license；仅可作为阅读和手工复现实验线索，不能默认复制代码进入本仓库。 |
| Commit stability | partial | 已记录 HEAD `354f9aacf51b5121abb8a2e04718232185e71928`；后续复现必须固定 commit 或等待 release。 |
| Dataset hash | pending | 仓库数据未本地冻结，本轮未计算逐文件 hash。 |
| URL stability | partial | arXiv 稳定；GitHub main 分支可漂移。 |

## Pending / blocker

| 等级 | 项 | 影响 |
|---|---|---|
| pending | arXiv license 元数据未写入本文件 | 影响 PDF 再分发口径，不影响本地阅读。 |
| pending | GitHub repo 与论文最终版本关系未由作者确认 | 影响正式复现引用。 |
| pending | 未冻结 GitHub 数据和输出文件 hash | 影响 benchmark 复现。 |
| blocker | GitHub repo 无 license | 阻止代码/数据直接纳入正式 artifact 包。 |
| blocker | 无 release/tag/依赖锁 | 阻止标记为 `SA-1` 或 `SS-A`。 |

## initial-generation-only 冻结建议

若 PR-R2 选择该候选，应建立独立 seed 切片：`nl_description.txt`、`initial_generated_dfsm.csv`、`schema.md`、`source_commit.txt` 和 `excluded_repair_sections.md`。不得把 oracle DFSM、distinguishing / checking sequence 答案或 fault-model repaired machine 混入初始 seed 输入输出。
