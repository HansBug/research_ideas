# Can Agents Judge Systematic Reviews Like Humans? Evaluating SLRs with LLM-based Multi-Agent System

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Can Agents Judge Systematic Reviews Like Humans? Evaluating SLRs with LLM-based Multi-Agent System |
| 年份 | 2025 |
| 作者 / venue / 出版状态 | Abdullah Mushtaq、Muhammad Rafay Naeem 等；arXiv:2509.17240; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | LLM-as-Judge 与 SLR 质量评价 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | decision-log / trace 级 provenance；需核验是否能导出完整证据包。 |
| 输入 | 用户上传的 SLR PDF、PRISMA 清单、arXiv 检索工具、专家 SLR reviewer 的 PRISMA 评分 |
| 输出 | 各 PRISMA section / item 的 0-5 分、定性反馈、统一评估结果、follow-up 对话支持 |
| 方法/系统形态 | GPT-4.1 驱动的 MAS evaluation copilot；27 个 PRISMA item agent + coordinator / task agent + PDF parsing / follow-up agent |
| 覆盖阶段 | 主要覆盖 SLR 报告质量评估：protocol validation、methodological assessment、topic relevance、duplication detection、citation checks、editorial feedback；不执行正式检索、筛选、抽取、编码和综合 |
| 不覆盖阶段 | 不覆盖阶段需按全文方法章节复核；当前不得据此写“完整覆盖 SLR 生命周期”。 |
| 人审/审计机制 | 以 3 位 expert SLR reviewers 的 PRISMA item 评分作 benchmark；系统本身给 item score 和 qualitative feedback，但未见 claim-to-source / decision-log 级证据包 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 运行中 + 运行后复核 |
| 主张追踪状态 | item score / qualitative feedback 级；无来源证据链或报告级 claim trace。 |
| 决策日志状态 | per-record / reasoning 级线索；导出格式待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 5 篇已发表 SLR；agent 与专家按 0-5 PRISMA item 评分比较；总体 agreement 84%，section-level agreement、MAE、ICC、Krippendorff's alpha、Pearson ρ |
| 模型/API 设置 | GPT-4、GPT-4.1、Opus、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | 初步结果显示 MAS 与专家评分有较高一致性，但样本仅 5 篇 SLR，作者明确称结果 preliminary；GitHub 链接在正文中仍是 publication 后补充的占位 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 约束 paper2 的 reviewer/audit gate：不能只说 agent 能评审 SLR，而要说明 paper2 是否保存来源级证据、阶段级 run record 和 人工审计 裁决 |
| 受影响主张 ID | C2,C5,C6 |
| 威胁类型 | 评价协议约束 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 约束 paper2 的 reviewer/audit gate：不能只说 agent 能评审 SLR，而要说明 paper2 是否保存来源级证据、阶段级 run record 和 人工审计 裁决 |
| 支持的 paper2 主张 | 支持 paper2 将 reviewer/audit gate 设计为有来源证据和人工裁决的机制，而不是只用 LLM-as-Judge 总分。 |
| paper2 应避免的主张 | 避免把 LLM-as-Judge 评价等同人工审计；不能声称 agent 评审无需来源证据或专家复核。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 占位承诺；原文写 publication 后补 GitHub，本轮无可核验入口 |
| 数据状态 | 未提及可复用数据集入口；评估 SLR 文档与输出数据待核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` §Abstract / Page 1：系统定位为 SLR evaluation copilot，自动做 protocol validation、methodological assessment、topic relevance checks | 直接面向 SLR 质量评估，且核心方法是 LLM-based multi-agent system，主题与 paper2 的 SLR 自动化审计层高度相关。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | Page 2 Introduction：支持 protocol critique、methodological assessment、relevance checking、duplication detection、collaborative drafting；Page 3 Table 1：Abstract/Title、Introduction、Methods、Results、Discussion、Other Information societies | 覆盖的是 SLR 报告各 section 的质量评估，不是从检索到综合的完整 SLR 执行链；可算多个评估环节，但不能当作完整 workflow baseline。 |
| D3 LLM/agent 自动化深度 | 🟢 | Page 3 §3.1：27 specialized agents、six PRISMA-aligned societies、two utility agents；Coordinator / Task Agent 分发任务；GPT-4.1、OCR parsing、arXiv Toolkit | 不是单 prompt demo，而是多 agent 分工、PDF 解析、工具检索、评分和汇总的明确输入输出链。 |
| D4 人工审计与可追踪性 | 🟡 | Page 4 §3.2：3 位 expert SLR reviewers 给 PRISMA item 评分；agent 和 human 都按 0-5 scale；Page 3：agent 提供 qualitative feedback | 有专家 benchmark 和 item-level 评分反馈，但未见可导出的 claim-to-source、per-cell provenance、人工裁决日志或 run record，因此只能中等。 |
| D5 评价严谨性 | 🟡 | Page 4 §4：5 篇 SLR，overall agreement 84%；Page 7 Appendix：ICC 0.924、Krippendorff's alpha 0.889、Pearson ρ 0.898 | 有真实 SLR 和专家评分，统计指标较完整；但样本很小，作者在 conclusion/limitations 明确称 preliminary，尚不足以给强实证分。 |
| D6 SE/CCF 相关性 | 🟠 | `bibtex.bib`：arXiv cs.AI；Page 2：称可跨 health sciences 到 software engineering | 不是 SE venue，也不是面向 SE SLR；只作为跨域方法学和 audit gate 参考。 |
| D7 对本文 novelty 的威胁 | 🟡 | Page 5 Conclusion：multi-agent system aligned with PRISMA protocol；Page 5 Limitations：当前只支持 evaluation，不支持 real-time drafting or collaboration | 威胁 paper2 的 reviewer/evaluation 模块，但没有覆盖 paper2 的全阶段 agent 工作流、证据链、claim-source 绑定和 SE evaluation。 |

## 3. 论文解决的问题与背景

论文指出 SLR 对 evidence-based research 很重要，但人工评审 SLR 质量耗时且不一致。作者关注的不是“如何生成一篇 SLR”，而是“如何用多 agent LLM 辅助判断一篇 SLR 的 PRISMA 报告质量”。背景部分把 Rayyan、Covidence 等工具定位为仍依赖大量人工的筛选/抽取工具，并认为 monolithic LLM 在结构化 SR 任务中存在性能上限。因此作者提出把 PRISMA checklist 拆成 item-level agent，由专业 agent 分别评价各 section，再汇总为可交互反馈。

## 4. 方法 / 系统拆解

输入侧包括上传的 SLR PDF、PRISMA checklist、原稿文本、arXiv Toolkit 和用户 follow-up 问题。PDF 先由 OCR-enabled Vision-Language Model 转成结构化文本；Coordinator Agent 和 Task Agent 将 PRISMA checklist 拆为任务；每个 specialized agent 用 few-shot prompt 给出 0-5 分和定性反馈；低于阈值时 coordinator 可重新分配任务或生成新 agent；最后把各 agent 输出合成为 web UI 可读结果，并交给 SLR-GPT Agent 做 follow-up。

agent 组织是本文最核心的方法证据：27 个 specialized agents 被分入 Abstract & Title、Introduction、Methods、Results、Discussion、Other Information 六个 PRISMA-aligned societies，另有 PDF Parsing 与 Follow-up Conversation 两个 utility agents。Methods section 有 11 个 agent，因为 protocol requirements 更细；Discussion 只有一个 agent。作者还说明早期把多个 checklist item 交给同一 agent 会导致 overloaded agent 和不稳定行为，所以改为 one-agent-per-item。

人机协作主要体现为专家评分 benchmark 和后续 interactive interface 设想。系统没有清楚说明每个 agent 反馈如何绑定到 PDF 页码、原文句子或引用来源；arXiv Toolkit 可辅助检索和 citation cross-check，但正文没有给出可复验证据包格式。

## 5. 实验 / 评价设计

RQ1 问 multi-agent LLM system 如何支持 SLR protocol validation 和 compliance steps；RQ2 问系统输出与 PRISMA standards / expert evaluations 的一致程度，以及是否能改善效率或一致性。数据集为 5 篇已发表 SLR，来自 Medical、E-commerce、AI、Metaverse、IoT 等不同领域。baseline 是 3 位 expert SLR reviewers 对原稿和 PRISMA guideline 的人工评分。

指标包括 MAE、agreement percentage、section-level agreement 和 inter-expert reliability。agreement 按 $100\% - (MAE / 5 \times 100)$ 计算。Appendix 报告 ICC、Krippendorff's alpha 和 Pearson ρ。作者还给出运行时间：系统按论文长度和复杂度约 15-20 分钟完成分析；但没有给出与人工专家逐篇计时的严格对照实验。

## 6. 主要结果与结论

主要数值包括 overall agreement 84%；Introduction 97%、Discussion 94%、Methods 93%、Results 84%、Other Information 81%。Appendix 报告 per-paper MAE 从 0.05 到 0.44；专家间可靠性为 ICC 0.924、Krippendorff's alpha 0.889、average Pearson ρ 0.898。作者据此认为 MAS 能较好复现专家在核心 review components 上的判断，并可用于 early-stage insights。

这些结果必须保守使用。全文只支持“小样本初步可行性”和“与专家评分相对一致”，不支持系统已经可替代人工 SLR reviewer，也不支持它能自动完成系统综述。

## 7. 局限与可复现性

作者明确列出当前评价只覆盖 5 篇 SLR，后续需要增加论文数量。agent 能力受当前 LLM 限制，可能漏掉技术领域的细粒度知识。arXiv 集成提升 open-access coverage，但排除了 PubMed、Scopus 等数据库。系统当前只支持 evaluation，不支持 real-time drafting 或 collaboration。正文两处 GitHub 链接仍写作“will be added here upon publication”，所以代码可用性在本文版本中不可核验。

可复现性方面，方法细节给出了 agent societies、模型 GPT-4.1、0-5 PRISMA score 和指标，但缺少 prompt、完整数据、专家评分表和运行日志。paper2 不能把它当作完整可复现实验 harness，只能作为 reviewer gate 和 PRISMA item decomposition 的方法参照。

## 8. 对 paper2 story / 实验设计的影响

paper2 应正面承认：已有工作把 SLR 报告质量评估拆成 PRISMA-aligned multi-agent societies，并用专家 PRISMA 评分做初步对照。因此 paper2 的 novelty 不能写成“agent 可以评估 SLR”或“多 agent 可用于 SLR 质量检查”。

paper2 的差异化应落在更具体的证据链：它是否覆盖从检索、筛选、抽取、编码、综合到报告的 run record；是否把报告 主张绑定到 paper source、screening decision、extraction record 和 coding decision；是否有 人工审计 gate 的裁决记录；是否在 SE / LLM4SE / MDE 场景做可复现实验。

## 9. 可用于写作的引用角度

- 作为“LLM/MAS 用于 SLR 质量评估”的近邻工作：已有研究将 PRISMA checklist 分解为 item-level agents，并用专家评分初步检验一致性。
- 作为“报告级审计不等于证据链审计”的反例：该系统提供 PRISMA item score 和 qualitative feedback，但未展示 claim-to-source provenance。
- 作为评价设计参照：paper2 可借鉴 expert SLR reviewer、MAE/agreement、inter-rater reliability，但要扩展到阶段级证据和错误分类。

## 10. 待复核清单

- 人工打开 PDF 核对 Figure 1、Figure 2、Figure 3、Appendix Figure 4/5 的具体图表内容。
- 复查是否已有正式出版版本或可用 GitHub 仓库；当前正文仍是占位。
- 若写 Related Work，补充核验专家评分原始表、prompt 和数据是否公开。
- 不得把 84% agreement 写成跨领域充分验证；只能写 small-scale preliminary evaluation。
