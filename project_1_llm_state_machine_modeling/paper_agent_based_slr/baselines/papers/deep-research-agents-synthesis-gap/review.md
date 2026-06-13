# Can Deep Research Agents Retrieve and Organize? Evaluating the Synthesis Gap with Expert Taxonomies

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Can Deep Research Agents Retrieve and Organize? Evaluating the Synthesis Gap with Expert Taxonomies |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Ming Zhang、Jiabao Zhuang 等；arXiv:2601.12369; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | 文献综述的检索、组织与来源归因 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 72 篇高引用 LLM survey topic、专家 taxonomy tree、3815 篇 cited papers；Deep Research mode 输入 topic，Bottom-Up mode 输入 expert paper set |
| 输出 | retrieval Recall/Precision/F1、leaf-level ARI/V-Measure、hierarchy-level US-TED/US-NTED/Sem-Path、reference-independent defect diagnostics |
| 方法/系统形态 | TaxoBench benchmark + evaluation framework；评估 7 个 Deep Research Agents 和 12 个 frontier LLMs；含 LLM-as-Judge 与 human baseline |
| 覆盖阶段 | 聚焦 survey 生成 的 retrieval 和 organization/taxonomy 两个基础环节；不覆盖 SLR screening/extraction/coding/report writing 全流程 |
| 不覆盖阶段 | 不覆盖SLR screening/extraction/coding/report writing 全流程。 |
| 人审/审计机制 | Ph.D.-level annotators 抽取专家 taxonomy 并映射 paper categories；3 组 independent human annotator taxonomy baseline；GPT-4o judge 与 human evaluators Cohen's κ=0.8909 |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | taxonomy/gold 评价级；不等同生产期 claim-to-source trace。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 72 surveys、8 AI/ML subdomains、3815 papers；7 DR agents、12 LLMs、1000 generated taxonomies、3-run robustness、embedding sensitivity、multi-category sensitivity |
| 模型/API 设置 | GPT-5、GPT-4、GPT-4o、Claude、Sonnet、Gemini、DeepSeek、Qwen；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | seed；正式复现前需回原文核对 |
| 主要发现 | best agent Recall 20.92%；Bottom-Up LLM Sem-Path 28-29%，低于 human groups 47.32%/52.14%/57.74%；reference-free defects 包括 sibling overlap 75.9%、MECE violations 51.2%、imbalance 83.4% |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 约束 paper2 的 automated synthesis/report organization claim：必须评估检索覆盖、taxonomy/编码结构和 reference-free defects，不能只看文本流畅度或 citation correctness |
| 受影响主张 ID | C3,C5,C6 |
| 威胁类型 | 评价协议约束 + 负面证据 |
| 威胁的 paper2 主张 | 约束 paper2 的 automated synthesis/report organization claim：必须评估检索覆盖、taxonomy/编码结构和 reference-free defects，不能只看文本流畅度或 citation correctness |
| 支持的 paper2 主张 | 支持 paper2 把 retrieval coverage、来源归因 和长尾文献遗漏作为 evidence workflow 的关键风险。 |
| paper2 应避免的主张 | 避免声称“首次 LLM/agent 自动化 SLR”“完整覆盖 SLR 生命周期”“PRISMA 合规”，也不得把 arXiv 预印本当作 CCF/peer-reviewed 事实。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Page 1 Abstract：Deep Research Agents automate survey 生成；Page 2：retrieving essential papers and organizing expert-like taxonomies | 直接研究 agentic/deep research systems 在 survey 生成 中能否检索和组织文献，和 paper2 的自动综述生成/综合质量直接相关。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | Page 2 Figure 2 / §Introduction：Deep Research mode 测 retrieval + taxonomy construction；Bottom-Up mode 隔离 organization | 只覆盖检索和组织/taxonomy，不覆盖筛选、全文抽取、编码决策、证据综合和报告 claim 生成的完整 SLR/SMS 流程。 |
| D3 LLM/agent 自动化深度 | 🟢 | Page 7 §4：7 Deep Research Agents 和 12 frontier LLMs；Page 5-6：Deep Research mode、Bottom-Up mode、metrics | 明确评估 end-to-end DR agents 和 LLM taxonomy construction，不是概念讨论。 |
| D4 人工审计与可追踪性 | 🟡 | Page 3 §Taxonomy extraction：Ph.D.-level annotators 读取全文映射 cited papers；Page 7 §3.4：LLM-as-Judge 与 human evaluators κ=0.8909；Page 35-36 human baseline | 有人工 benchmark、annotation 和 judge validation，但不是 human-in-the-loop SLR workflow，也未展示 stage decision log。 |
| D5 评价严谨性 | 🟢 | Page 3-4 Table 1：72 surveys / 3815 papers；Page 7-10 Tables 2-4：多模型、多指标；Appendix G：3-run、embedding、multi-category、cross-domain checks | benchmark 规模、指标设计、human baseline 和 robustness checks 都较充分，属于强评价。 |
| D6 SE/CCF 相关性 | 🟠 | `bibtex.bib`：arXiv cs.CL；Page 11 Limitations：benchmark 来自 AI/ML surveys，cross-domain pilot 仅 finance/medical 各一类 | 方法学强相关，但不是 SE/CCF，也不是软件工程 SLR。 |
| D7 对本文 novelty 的威胁 | 🟡 | Page 10 Related Work：TaxoBench isolates Information Acquisition and structural organization；Page 10 Conclusion：dual bottleneck | 它强约束 paper2 的 retrieval/synthesis evaluation，但未覆盖 agent-based SLR workflow、人工审计 gate 和 SE setting 的完整 novelty 组合。 |

## 3. 论文解决的问题与背景

论文针对 deep research agents 生成 survey 的两个基础能力：能否找回专家会引用的核心论文，以及能否把论文组织成专家式 taxonomy。作者指出已有 benchmark 多关注 writing quality、factuality、citation correctness 或 report rubric，较少直接检查 retrieval coverage 和 hierarchical organization。标准 clustering 指标又无法捕捉 taxonomy 的父子结构和路径语义，因此需要新的 benchmark 和结构指标。

这篇论文不是 SLR 自动执行系统，而是 evaluation paper。它的价值在于把“自动 survey 写得像不像”拆成可量化的必要条件：检索召回、paper-to-category assignment、taxonomy hierarchy、reference-independent defects。对 paper2 来说，它提供了比普通生成质量更严格的 synthesis evaluation 口径。

## 4. 方法 / 系统拆解

TaxoBench 由 72 篇高引用 LLM-related surveys 构成，平均引用 354.5，覆盖 8 个 AI/ML 子域，总计 3815 篇 cited papers。构建流程包括 taxonomy figure filter、impact filter、scope filter 和 Ph.D.-level expert verification。taxonomy extraction 并不是重新设计分类法，而是抽取 survey 作者发表的 taxonomy figure，再通过阅读全文把 cited papers 映射到 paper categories。最终 taxonomy 以目录树形式保存，topics 是 folders，papers 是 files。

Evaluation Framework 有两个模式。Deep Research mode 给 agent 一个 survey topic，让 agent web research、retrieve papers 并构造 taxonomy，评估端到端检索与组织。Bottom-Up mode 提供专家 paper set，隔离组织能力，避免 retrieval failure 掩盖 taxonomy construction。retrieval 用 Recall、Precision、F1；leaf-level 用 ARI 和 V-Measure；hierarchy-level 用 US-TED、US-NTED 和 Sem-Path。

US-TED 用 unordered semantic tree edit distance 处理 sibling 无序性，避免把 taxonomy 中兄弟节点排列顺序当作错误。Sem-Path 对每个 aligned paper 比较 root-to-leaf ancestor chain，衡量论文是否被放在语义一致的路径下。作者还把 diagnostics 分成 alignment-based 和 capability-based：前者依赖专家 reference，后者包括 retrieval Recall ceiling、sibling semantic overlap、MECE violation、structural imbalance、inconsistent classification criteria 等 reference-free 缺陷。

## 5. 实验 / 评价设计

RQI 问 current agents 能否复现 expert-level literature discovery；RQII 问 agents 能否组织已检索子集；RQIII 问在 perfect retrieval 下 LLM 能否组织 taxonomy。Deep Research mode 评估 o3、Grok、Gemini、Perplexity、DeepSeek、Qwen、Doubao 7 个 agents。Bottom-Up mode 评估 12 个 frontier LLMs，包含 Claude-4.5-Sonnet、GPT-5、Gemini-3-Pro、DeepSeek-V3.2、Qwen3-Max、Kimi-K2 及 thinking variants。输入粒度包括 Title+Abstract、+Summary、+Core-task&Contributions。

人工基线由三组 independent non-author human annotators 在相同 paper sets 上构造 taxonomy，作为判断“taxonomy 本身有主观性”是否能解释模型低分的参照。LLM-as-Judge 使用 GPT-4o 从 Coverage、Organization for MECE、Logic、Topology 四维评分，并报告与 human evaluators 的 Cohen's κ=0.8909。Appendix 还提供 temporal filtering、3-run error bars、embedding sensitivity、multi-category paper sensitivity 和 cross-domain pilot。

## 6. 主要结果与结论

Deep Research mode 的核心结果是 retrieval bottleneck：best agent o3 Recall 20.92%、Precision 29.29%、F1 24.41%；四个 agent F1 低于 10%。作者强调这是 capability-based finding，因为任何下游 synthesis pipeline 都受专家核心论文召回上限限制。

组织能力方面，Deep Research mode 的 global ARI 都低于 5%，但在 retrieved intersection 上 ARI 可到 28-42%，说明 retrieval failure 掩盖了一部分 clustering potential。retrieval F1 与 Sem-Path 强相关，Spearman ρ=0.89，p=0.007。

Bottom-Up mode 下，即使给定 expert paper set，模型仍有明显 hierarchy gap。best ARI 为 Qwen3-Max 31.24%；Sem-Path 在所有 12 个 LLM 上收敛到 28.13-29.16%，而三组 human annotators 达到 47.32%/52.14%/57.74%。reference-free defects 也很高：1000 个 model-generated taxonomies 中 sibling overlap 75.9%、MECE violations 51.2%、inconsistent classification criteria 66.0%、structural imbalance 83.4%。这些结果说明问题不只是 reference taxonomy 主观，而是模型 taxonomy 结构本身常有缺陷。

## 7. 局限与可复现性

作者明确区分 alignment 与 capability：Sem-Path、US-TED 等衡量的是与某个专家 taxonomy 的一致性，不等于 taxonomy 的绝对合理性。每篇 survey 只有一个 published expert taxonomy，可能存在多个同样合理的分类法；作者用三组 human baseline 和 reference-free defects 缓解这一点，但仍建议未来做 multi-reference 扩展。领域范围局限于 AI/ML surveys，虽然有 finance/medical 的小型 cross-domain pilot，但绝对数值不应直接外推到 SE。

可复现性较强：摘要给出 GitHub `https://github.com/KongLongGeFDU/TaxoBench`；正文提供数据构建、指标公式、prompt、模型列表、robustness 表。需要注意的是，paper_content 中部分模型名和年份明显依赖未来/preview 语境；正式写作时应按本地文本和核验日期保守引用。

## 8. 对 paper2 story / 实验设计的影响

paper2 如果要做 agent-based SLR 报告生成，不能只评估最终报告的 fluency、citation correctness 或 human preference。TaxoBench 证明 retrieval 和 organization 是必要条件：如果 agent 没找回核心论文，后续 synthesis 再流畅也不可信；如果 taxonomy/编码结构 sibling overlap、MECE violation 或 path inconsistency 很高，报告结构也不能视为可靠。

paper2 可以借鉴两类指标。第一类是 retrieval coverage：对 known relevant studies、seed set、expert set 计算 Recall/Precision/F1。第二类是结构组织：对 coding taxonomy、theme hierarchy 或 evidence map 计算 tree/path/cluster 指标，并补充 reference-free defects。若 paper2 强调 人工审计 gate，则可把人工裁决后的 coding hierarchy 当作参考，但要像本文一样区分 alignment-based 与 capability-based 结论。

## 9. 可用于写作的引用角度

- 作为 deep research agent 评价背景：已有 benchmark 显示当前 agents 在 survey-oriented retrieval 和 taxonomy organization 上存在明显瓶颈。
- 作为 synthesis evaluation 方法参照：TaxoBench 提供 retrieval metrics、leaf-level clustering metrics 和 hierarchy-level path/edit metrics，可启发 paper2 的 evidence map / coding quality 评价。
- 作为谨慎措辞依据：自动 survey 生成的关键风险不只 hallucination，还包括核心文献遗漏和 taxonomy 结构缺陷。

## 10. 待复核清单

- 回 PDF 核对 Figure 2、Tables 2-4、Figures 5-6 的版式和数值，当前只读了提取文本。
- 复核 GitHub 仓库是否实际公开 TaxoBench 数据、评价基准 和 prompt。
- 若引用 GPT-5、Claude-4.5、Gemini-3 等模型结果，应标注为原文 benchmark 设置，避免和本仓库模型情报库混写。
- 不把 AI/ML survey 数值直接外推到 SE SLR；只能作为方法学警示和评价设计启发。
