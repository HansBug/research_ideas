# EviSearch: A Human in the Loop System for Extracting and Auditing Clinical Evidence for Systematic Reviews

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | EviSearch: A Human in the Loop System for Extracting and Auditing Clinical Evidence for Systematic Reviews |
| 年份 | 2026 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验；未人工打开 PDF 图表，不写图表级核对结论 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 输入 | 原生 clinical trial PDF、133 列 ontology-aligned evidence table schema、clinician-curated mCSPC gold attribution |
| 输出 | 结构化 evidence table；每个 cell 的 value、reasoning、page/modality/verbatim quote provenance；reconciler 判断与 reviewer edits |
| 方法/系统形态 | 多阶段双 agent extraction pipeline：PDF Query Agent + Search Agent + Reconciliation Agent + human review web interface |
| 覆盖阶段 | 主要覆盖系统综述中的全文证据抽取、结构化表填充、证据归因和人工审计；不覆盖检索、题摘筛选、meta-analysis 或完整综述写作 |
| 人审/审计机制 | per-cell provenance、disagreement forced page-level verification、low-confidence surfaced to reviewer、reviewer edits logged |
| 实验/指标 | clinician-curated oncology trial benchmark；numeric/free-text correctness、completeness、overall；按 text/table/figure modality 分析；token/API cost |
| 主要发现 | EviSearch overall 91.3%，best parsed baseline GPT-4.1 为 84.1%；667 字段中 46% 以上来自 table/figure；figure evidence 上 EviSearch 86.7%，parsed Gemini 51.6% |
| 对 paper2 的作用 | 对 paper2 的 traceability/evidence package 是强威胁；但它不是完整 SLR agent workflow，paper2 可从 SE 场景、多阶段 run record 和报告级 claim trace 区分 |
## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟢 | 🟢 | 🟡 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 1 Abstract；Page 2 §2 | 题目和摘要直接面向 systematic reviews 的 clinical evidence extraction/auditing，是 evidence synthesis 自动化核心环节。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | Page 2-4 §3；Page 6 Conclusion | 系统只实质覆盖全文 PDF 证据抽取、表格填充和审计，不做检索、筛选、编码综合、报告生成；按 GUIDE 只能给单环节强实现的弱档。 |
| D3 LLM/agent 自动化深度 | 🟢 | Page 3 §3.3-3.5 | 双 agent 并行抽取、tool-based Search Agent、strict JSON/function calling、reconciliation forced tool use，自动化深度很高。 |
| D4 人工审计与可追踪性 | 🟢 | Page 1 Abstract；Page 4 §3.6；Page 7 Ethics Statement | 明确 per-cell provenance、page/modality/verbatim quote、reviewer 可检查/改写、reconciler decisions 和 reviewer edits logging，完全命中 audit/traceability。 |
| D5 评价严谨性 | 🟡 | Page 4-6 §4-5；Page 7 Limitations | 有 clinician-curated benchmark、gold attribution、多个强 baseline 和 modality/cost 分析；但样本规模正文只给 667 fields，评价依赖 LLM judge，未见完整专家裁决统计，因此不是强档。 |
| D6 SE / CCF 相关性 | 🟠 | `bibtex.bib` arXiv cs.CL；Page 1 oncology / clinical evidence setting | 领域是医学 clinical trial evidence synthesis，不是 SE/CCF；对 paper2 是跨域审计机制参考。 |
| D7 novelty 威胁 | 🟢 | Page 3-4 §3.5-3.6；Page 6 §5.3 | 已经把 per-cell provenance、human verification、decision logging 和 reviewer corrections 做成系统核心；直接威胁 paper2 的证据包/审计 claim。 |

## 3. 论文解决的问题与背景

EviSearch 关注的是 clinical trial publication 到 living evidence table 的高精度抽取。作者指出，临床证据分布在文本、复杂表格、Kaplan-Meier plot、caption 和 subgroup result 中，简单 parsed text 或全局 prompt 容易遗漏或误归因。因为这些表格后续会影响 meta-analysis 和 guideline，系统目标不是让 LLM 自主下结论，而是让每个抽取值都能被 clinician 快速追溯和纠正。

## 4. 方法 / 系统拆解

输入是原生 trial PDF 和 133 列 evidence schema。schema 来自 LISR living evidence synthesis platform，按 trial characteristics、population、efficacy outcomes、subgroup、adverse events、demographics 等分组，每列有自然语言定义和缺失 fallback。列会按 clinical section 打包，每批最多 15 列。

系统先用 Landing AI `dpt-2-latest` 解析 PDF，形成带页码和 modality 标签的 chunk，并用 `text-embedding-3-large` 建立检索索引。Agent A 把完整 PDF binary 和列定义交给 Gemini-2.5-Flash，通过 File API 保留原版布局、图和表，并输出 `(value, reasoning, attribution)`。Agent B 在 parsed document 上用 `search_chunks`、`get_chunks_by_page` 和 `submit_extraction` 工具做检索式抽取，适合表格和结果段落。

Reconciliation Agent 接收 A/B 输出。若两者一致或一方是另一方 superset，就直接 resolved；若冲突，则必须调用 `get_page`，读取 parsed text 和 rendered page image 后给出 `both_correct`、`A_correct_B_wrong`、`B_correct_A_wrong` 或 `both_wrong`。Human review 模式中，reviewer 看到两个 agent 答案、reconciler 判断和对应页面内容，可接受候选或写入修正值。

## 5. 实验 / 评价设计

论文没有用 RQ 编号，但实验围绕抽取准确性、modality robustness 和 API cost。数据集是 metastatic castration-sensitive prostate cancer trial papers 的 clinician-curated benchmark。每个 paper 有结构化 schema annotation，并为每个报告值提供 gold source page 和 modality。baseline 包括 Gemini 2.5 Flash native PDF upload、Gemini 2.5 Flash parsed Doc、GPT-4.1 parsed Doc。

评价把列分为 numerical 和 free-text，用 LLM judge 对 prediction 与 ground truth 进行 correctness 和 completeness 评分，overall 是两者均值；numeric field 允许 rounding/format tolerance。这个设计可扩展，但局限也明显：作者在 Limitations 中承认 LLM judge 可能不能捕获所有临床重要差异，不能等同 full expert adjudication。

## 6. 主要结果与结论

Table 1 显示 EviSearch 总体 overall 为 91.3%，其中 correctness 90.9%、completeness 91.6%；最佳 baseline GPT-4.1 parsed Doc overall 为 84.1%，差距 7.2 点。numeric columns 上 EviSearch 为 91.7%，free-text 为 88.7%。证据 modality 分析更关键：667 个 evidence fields 中 53.4% 来自 text，41.8% 来自 tables，4.8% 来自 figures，说明接近一半不能从 plain text 直接恢复。figure-sourced evidence 上 parsed Gemini 只有 51.6%，EviSearch 达 86.7%；table evidence 上 GPT-4.1 从 text 87.3 降到 table 73.5，而 EviSearch 在 text/table/figure 上相对稳定。

成本上，EviSearch 平均每文档 642,798 tokens、79 API calls，高于 native Gemini PDF，但低于 parsed text baselines 约 970k-1M tokens。作者将额外成本解释为审计性和冲突验证的代价。

## 7. 局限与可复现性

局限包括：LLM 输出仍可能有 reasoning error 或临床术语误解；评价依赖 LLM judge；双 agent 架构 token cost 不低；作者明确说 full automation of clinical evidence synthesis 不是目标也不建议。Ethics Statement 说明处理的是公开 peer-reviewed PDFs，不含个人身份信息；每个 value 存 provenance，reviewer edits 作为 structured feedback，软件组件 Apache 2.0 发布，但正文未给出完整代码仓库 URL，只在首页有 demo/code/video 入口线索。

## 8. 对 paper2 story / 实验设计的影响

EviSearch 是 paper2 证据链部分的强近邻。若 paper2 声称“可审计 LLM evidence table / claim-to-source tracing”，必须说明与 EviSearch 的差别：paper2 是 SE SLR/SMS 语境，是否覆盖从检索到报告的多阶段 workflow，是否记录 agent loop/run record，是否处理文献级 claim 而不是 clinical table cell，是否有人工 gate 影响最终结论。实验上，paper2 可借鉴 per-cell provenance 与 disagreement reconciliation，但不能把它当作完整 SLR 流程 baseline。

## 9. 可用于写作的引用角度

- EviSearch 可引用为“clinical evidence table extraction 中以 per-cell provenance 和 human audit 为核心设计”的代表。
- 它说明多模态证据源会显著影响抽取可靠性，table/figure 中的信息不能用纯文本 RAG 假设轻易覆盖。
- 它也提醒 paper2 不应只报告抽取准确率，还应报告 provenance coverage、人工纠错入口和审计成本。

## 10. 待复核清单

- 人工打开 PDF 核对 Figure 1-4 与 Table 1-2 的样本、字段和数值展示。
- 追踪首页的 Code/Demo/Video 链接，确认实际仓库、license、是否有可复现实验脚本。
- 核验 clinician-curated benchmark 的 paper 数量；正文明确 667 fields，但 paper/document 数量没有在已读文本中清楚给出。
- 若正式写评价严谨性，需要复核 LLM judge prompt 和是否有人工 adjudication 附录/补充材料。
