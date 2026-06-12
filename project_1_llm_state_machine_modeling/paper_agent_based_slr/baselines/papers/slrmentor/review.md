# SLRMentor: An LLM-Based Tool Supporting Learning of SLR in Software Engineering

## 1. 元数据

| 字段 | 内容 |
|---|---|
| 标题 | SLRMentor: An LLM-Based Tool Supporting Learning of SLR in Software Engineering |
| 年份 | 2026 |
| 作者 | Rodolfo Gil-Pereira、Ronnie de Souza Santos、Cleyton Magalahes、Italo Santos |
| arXiv | [2606.07831](https://arxiv.org/abs/2606.07831) |
| PDF | [paper.pdf](./paper.pdf) |
| 正文提取 | [paper_content.txt](./paper_content.txt) |
| BibTeX | [bibtex.bib](./bibtex.bib) |
| 初步分层 | P1 |
| 核验阶段 | arXiv title / abstract 粗筛 + PDF 自动获取 + `paper_content.txt` 文字模式提取；还不是最终全文细读结论。 |

## 2. 七维初筛评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟡 | 🟡 | 🟠 | 🟢 | 🟡 |

## 3. 纳入理由与证据链

- 初步判断：面向软件工程 SLR 学习与 planning 的 LLM assistant，SE 场景强相关但偏教育/planning。
- title / abstract 证据（中文转述）：题名或摘要明确处在 SLR / SMS / systematic review 语境。
- title / abstract 证据（中文转述）：题名或摘要与软件工程 / 软件开发场景直接相连。
- 本地证据入口：PDF、BibTeX 与 `paper_content.txt` 已放在本目录，后续写 Related Work 时必须回到这些文件做逐段核验。
- 粗筛限制：本文件只固定 baseline triage；未人工逐页核验表格、指标、实验设计和工具可复现性。

## 4. 逐维判定理由

| 维度 | 评分 | 判定理由 |
|---|---:|---|
| 主题贴合度 | 🟢 | 主题贴合度强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| SLR/SMS 流程覆盖度 | 🟠 | SLR/SMS 流程覆盖度弱：当前更像局部、跨领域或背景参照，不能直接支撑强对照结论。 |
| LLM/agent 自动化深度 | 🟡 | LLM/agent 自动化深度中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |
| 人工审计与可追踪性 | 🟡 | 人工审计与可追踪性中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |
| 评价严谨性 | 🟠 | 评价严谨性弱：当前更像局部、跨领域或背景参照，不能直接支撑强对照结论。 |
| SE/CCF 相关性 | 🟢 | SE/CCF 相关性强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| 对本文 novelty 的威胁 | 🟡 | 对本文 novelty 的威胁中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |

## 5. `paper_content.txt` 定位线索

以下只是关键词页级定位线索，便于后续全文细读；不替代人工核验。

| 页码 | 命中关键词 |
|---:|---|
| 2 | `agent`, `human`, `evaluation` |
| 3 | `agent`, `synthesis` |
| 4 | `agent`, `evaluation` |
| 9 | `extraction`, `evaluation` |
| 10 | `agent`, `evaluation` |
| 11 | `evaluation` |

## 6. 对本文 story 的影响

- 会威胁本文某个局部模块或评价维度，不能只作为普通背景一笔带过。
- 后续需要明确本文相对该工作的差异：是否覆盖更多 SLR 环节、是否有更强审计链、是否面向 SE 场景或是否有更可复验的证据包。

## 7. 后续全文细读清单

- 核验其实际覆盖的 SLR/SMS 环节：检索、筛选、全文抽取、编码、综合、报告分别到什么程度。
- 核验 human-in-the-loop 是否只是用户反馈，还是有可复查审计协议、裁决日志和错误分类。
- 核验是否保存 claim-to-source / cell-to-source / page-level provenance，以及是否可导出为论文证据包。
- 核验评价数据集、金标、样本规模、指标、消融、失败案例和成本统计。
- 核验是否已有 SE / CCF 版本或 peer-reviewed 版本；arXiv 版本不得直接等同正式出版。
