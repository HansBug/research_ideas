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
- title / abstract 证据（中文转述）：题名 / 摘要把论文定位为：Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews。
- title / abstract 证据（中文转述）：流程线索：可识别 抽取、综合/总结 等环节，需全文确认实际实现深度。
- title / abstract 证据（中文转述）：自动化线索：出现 agent / multi-agent、LLM、workflow / pipeline，说明不是单纯人工综述。
- title / abstract 证据（中文转述）：评价线索：出现 摘要给出数量级或样本规模、benchmark、dataset、metrics、F1，后续需核验指标、样本与可复现性。
- title / abstract 证据（中文转述）：领域线索：医学/临床 evidence synthesis；D6 评分据此区分 SE 直接近邻和跨域方法学 baseline。
- 本地证据入口：PDF、BibTeX 与 `paper_content.txt` 已放在本目录，后续写 Related Work 时必须回到这些文件做逐段核验。
- 粗筛限制：本文件只固定 baseline triage；未人工逐页核验表格、指标、实验设计和工具可复现性。

## 4. 逐维判定理由

| 维度 | 评分 | 证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | 题名：Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews | title / abstract 直接把任务放在 SLR、systematic review、evidence synthesis 或 literature review 自动化语境。 |
| D2 SLR/SMS 流程覆盖度 | 🟢 | abstract 阶段词：抽取、综合/总结 | 已能从 abstract 识别 2 类环节：抽取、综合/总结；完整覆盖度仍需全文核验。 |
| D3 LLM/agent 自动化深度 | 🟢 | abstract 自动化词：agent / multi-agent、LLM、workflow / pipeline | 自动化机制包含 agent / multi-agent、LLM、workflow / pipeline，足以作为 agent/LLM 工作流对照。 |
| D4 人工审计与可追踪性 | 🟡 | expert annotated dataset / reference annotations by domain experts | 摘要说明 reference annotations 来自 peer-reviewed studies 并由 domain experts produced，说明有专家标注参考集，但未见 reviewer edit log 或 claim-level provenance。 |
| D5 评价严谨性 | 🟢 | abstract 评价词：摘要给出数量级或样本规模、benchmark、dataset、metrics、F1 | 评价线索包括 摘要给出数量级或样本规模、benchmark、dataset、metrics、F1；需全文核验样本、指标和金标。 |
| D6 SE/CCF 相关性 | 🟠 | 领域：医学/临床 evidence synthesis | 领域是医学/临床 evidence synthesis，方法学相关但不是 SE/CCF 直接 baseline。 |
| D7 对本文 novelty 的威胁 | 🟢 | P0：AgentSLR evaluation harness 面向 AI-based scientific knowledge synthesis，含专家标注数据和分阶段评测，强约束本文 | 同时触及 SLR/evidence workflow、LLM/agent 自动化、评价或审计中的多个核心点，足以强约束本文 novelty。 |

## 5. `paper_content.txt` 定位线索

以下只是关键词页级定位线索，便于后续全文细读；不替代人工核验。

| 页码 | 命中关键词 |
|---:|---|
| 1 | `systematic`, `screening`, `extraction`, `synthesis`, `agent`, `evaluation` |
| 2 | `systematic`, `screening`, `extraction`, `synthesis`, `agent`, `human` |
| 3 | `systematic`, `screening`, `extraction`, `synthesis`, `agent`, `human` |
| 4 | `screening`, `extraction`, `synthesis`, `agent`, `human`, `evaluation` |
| 5 | `screening`, `extraction`, `synthesis`, `agent`, `human`, `evaluation` |
| 6 | `screening`, `extraction`, `synthesis`, `agent` |
| 7 | `screening`, `extraction`, `agent`, `human`, `audit`, `evaluation` |
| 8 | `systematic`, `screening`, `extraction`, `synthesis`, `agent`, `provenance` |
| 9 | `systematic`, `screening`, `extraction`, `synthesis`, `agent`, `human` |
| 10 | `screening`, `agent`, `benchmark` |

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
