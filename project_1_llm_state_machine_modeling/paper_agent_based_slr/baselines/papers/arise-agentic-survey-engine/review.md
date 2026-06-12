# ARISE: Agentic Rubric-Guided Iterative Survey Engine for Automated Scholarly Paper Generation

## 1. 元数据

| 字段 | 内容 |
|---|---|
| 标题 | ARISE: Agentic Rubric-Guided Iterative Survey Engine for Automated Scholarly Paper Generation |
| 年份 | 2025 |
| 作者 | Zi Wang、Xingqiao Wang、Sangah Lee、Xiaowei Xu |
| arXiv | [2511.17689](https://arxiv.org/abs/2511.17689) |
| PDF | [paper.pdf](./paper.pdf) |
| 正文提取 | [paper_content.txt](./paper_content.txt) |
| BibTeX | [bibtex.bib](./bibtex.bib) |
| 初步分层 | P1 |
| 核验阶段 | arXiv title / abstract 粗筛 + PDF 自动获取 + `paper_content.txt` 文字模式提取；还不是最终全文细读结论。 |

## 2. 七维初筛评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 |

## 3. 纳入理由与证据链

- 初步判断：agentic rubric-guided iterative survey engine，覆盖主题扩展、引用整理、摘要/草稿生成和同行评审式评价，对报告生成与质量控制阶段有威胁。
- title / abstract 证据（中文转述）：题名或摘要直接出现 multi-agent、agentic、agent-based 或 agents 工作流线索。
- title / abstract 证据（中文转述）：摘要强调人工参与、审计、provenance、verification 或可追踪机制。
- title / abstract 证据（中文转述）：摘要覆盖综合、总结、综述生成或 survey generation 环节。
- 本地证据入口：PDF、BibTeX 与 `paper_content.txt` 已放在本目录，后续写 Related Work 时必须回到这些文件做逐段核验。
- 粗筛限制：本文件只固定 baseline triage；未人工逐页核验表格、指标、实验设计和工具可复现性。

## 4. 逐维判定理由

| 维度 | 评分 | 判定理由 |
|---|---:|---|
| 主题贴合度 | 🟢 | 主题贴合度强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| SLR/SMS 流程覆盖度 | 🟡 | SLR/SMS 流程覆盖度中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |
| LLM/agent 自动化深度 | 🟢 | LLM/agent 自动化深度强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| 人工审计与可追踪性 | 🟡 | 人工审计与可追踪性中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |
| 评价严谨性 | 🟡 | 评价严谨性中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |
| SE/CCF 相关性 | 🟠 | SE/CCF 相关性弱：当前更像局部、跨领域或背景参照，不能直接支撑强对照结论。 |
| 对本文 novelty 的威胁 | 🟡 | 对本文 novelty 的威胁中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |

## 5. `paper_content.txt` 定位线索

以下只是关键词页级定位线索，便于后续全文细读；不替代人工核验。

| 页码 | 命中关键词 |
|---:|---|
| 1 | `agent`, `human`, `evaluation`, `synthesis` |
| 2 | `agent`, `human`, `evaluation` |
| 3 | `agent`, `screening`, `trace` |
| 4 | `agent`, `synthesis`, `trace` |
| 5 | `agent`, `human`, `evaluation`, `trace` |
| 6 | `agent`, `human`, `audit`, `evaluation`, `trace` |
| 7 | `agent`, `human`, `evaluation` |
| 8 | `agent`, `extraction`, `human`, `audit`, `evaluation` |

## 6. 对本文 story 的影响

- 会威胁本文某个局部模块或评价维度，不能只作为普通背景一笔带过。
- 后续需要明确本文相对该工作的差异：是否覆盖更多 SLR 环节、是否有更强审计链、是否面向 SE 场景或是否有更可复验的证据包。

## 7. 后续全文细读清单

- 核验其实际覆盖的 SLR/SMS 环节：检索、筛选、全文抽取、编码、综合、报告分别到什么程度。
- 核验 human-in-the-loop 是否只是用户反馈，还是有可复查审计协议、裁决日志和错误分类。
- 核验是否保存 claim-to-source / cell-to-source / page-level provenance，以及是否可导出为论文证据包。
- 核验评价数据集、金标、样本规模、指标、消融、失败案例和成本统计。
- 核验是否已有 SE / CCF 版本或 peer-reviewed 版本；arXiv 版本不得直接等同正式出版。
