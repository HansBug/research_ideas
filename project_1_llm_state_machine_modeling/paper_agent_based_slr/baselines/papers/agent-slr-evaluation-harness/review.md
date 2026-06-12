# Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews

## 1. 元数据

| 字段 | 内容 |
|---|---|
| 标题 | Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews |
| 年份 | 2026 |
| 作者 | Shreyansh Padarha、Ryan Othniel Kearns、Tristan Naidoo、Lingyi Yang 等 |
| arXiv | [2603.22327](https://arxiv.org/abs/2603.22327) |
| PDF | [paper.pdf](./paper.pdf) |
| 正文提取 | [paper_content.txt](./paper_content.txt) |
| BibTeX | [bibtex.bib](./bibtex.bib) |
| 初步分层 | P0 |
| 核验阶段 | arXiv title / abstract 粗筛 + PDF 自动获取 + `paper_content.txt` 文字模式提取；还不是最终全文细读结论。 |

## 2. 七维初筛评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 |

## 3. 纳入理由与证据链

- 初步判断：AgentSLR evaluation harness 面向 AI-based scientific knowledge synthesis，含专家标注数据和分阶段评测，强约束本文评价协议。
- title / abstract 证据（中文转述）：题名或摘要明确处在 SLR / SMS / systematic review 语境。
- title / abstract 证据（中文转述）：题名或摘要直接出现 multi-agent、agentic、agent-based 或 agents 工作流线索。
- title / abstract 证据（中文转述）：摘要覆盖抽取 / extraction 环节。
- title / abstract 证据（中文转述）：摘要覆盖综合、总结、综述生成或 survey generation 环节。
- 本地证据入口：PDF、BibTeX 与 `paper_content.txt` 已放在本目录，后续写 Related Work 时必须回到这些文件做逐段核验。
- 粗筛限制：本文件只固定 baseline triage；未人工逐页核验表格、指标、实验设计和工具可复现性。

## 4. 逐维判定理由

| 维度 | 评分 | 判定理由 |
|---|---:|---|
| 主题贴合度 | 🟢 | 主题贴合度强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| SLR/SMS 流程覆盖度 | 🟢 | SLR/SMS 流程覆盖度强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| LLM/agent 自动化深度 | 🟢 | LLM/agent 自动化深度强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| 人工审计与可追踪性 | 🟡 | 人工审计与可追踪性中：有明确相关线索，但覆盖范围、机制细节或证据链仍需全文核验。 |
| 评价严谨性 | 🟢 | 评价严谨性强：title / abstract 已给出直接线索，足以进入强核验路径。 |
| SE/CCF 相关性 | 🟠 | SE/CCF 相关性弱：当前更像局部、跨领域或背景参照，不能直接支撑强对照结论。 |
| 对本文 novelty 的威胁 | 🟢 | 对本文 novelty 的威胁强：title / abstract 已给出直接线索，足以进入强核验路径。 |

## 5. `paper_content.txt` 定位线索

以下只是关键词页级定位线索，便于后续全文细读；不替代人工核验。

| 页码 | 命中关键词 |
|---:|---|
| 1 | `agent`, `screening`, `extraction`, `evaluation`, `synthesis` |
| 2 | `agent`, `screening`, `extraction`, `human`, `evaluation` |
| 3 | `agent`, `screening`, `extraction`, `human`, `evaluation` |
| 4 | `agent`, `screening`, `extraction`, `human`, `evaluation` |
| 5 | `agent`, `screening`, `extraction`, `human`, `evaluation` |
| 6 | `agent`, `screening`, `extraction`, `synthesis` |
| 7 | `agent`, `screening`, `extraction`, `human`, `audit` |
| 8 | `agent`, `screening`, `extraction`, `provenance`, `evaluation` |

## 6. 对本文 story 的影响

- 不能再使用“首次 agent-based / LLM-based SLR 自动化”这类宽泛 claim。
- 后续 story 必须证明本文的差异化组合：软件工程场景、阶段化 run record、claim-to-source 不可断链证据包、human audit gate、透明报告与失败分类。
- Related Work 必须逐段核验其流程覆盖、人审机制、provenance / evidence package 与评价设计。

## 7. 后续全文细读清单

- 核验其实际覆盖的 SLR/SMS 环节：检索、筛选、全文抽取、编码、综合、报告分别到什么程度。
- 核验 human-in-the-loop 是否只是用户反馈，还是有可复查审计协议、裁决日志和错误分类。
- 核验是否保存 claim-to-source / cell-to-source / page-level provenance，以及是否可导出为论文证据包。
- 核验评价数据集、金标、样本规模、指标、消融、失败案例和成本统计。
- 核验是否已有 SE / CCF 版本或 peer-reviewed 版本；arXiv 版本不得直接等同正式出版。
