# Mixture of Knowledge Minigraph Agents for Literature Review Generation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Mixture of Knowledge Minigraph Agents for Literature Review Generation |
| 年份 | 2024 |
| 作者 / venue / 出版状态 | Zhi Zhang、Yan Liu 等；arXiv:2411.06159; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 近邻强度备注 | 结构化综合 / related-work generation 近邻；SUMMARY 归 P1，主要用于 synthesis/report-generation 定性对照。 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | 自动 survey / literature review 生成与评价 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | query paper abstract、被引用 reference abstracts；实验数据为 Multi-Xscience、TAD、TAS2 |
| 输出 | related work / literature review 段落摘要，带 `@cite_id` 引用 |
| 方法/系统形态 | CKMAs：Knowledge Minigraph Construction Agent + Multiple Path Summarization Agent；prompt-based graph extraction + multi-path summary routing |
| 覆盖阶段 | 给定参考文献后的关系建模与综合写作；不做检索、筛选、人类审计、完整报告生成 |
| 不覆盖阶段 | 不覆盖 SLR/SMS 的双人筛选、纳入/排除审计、抽取表、编码协议、质量评价和系统综述级报告审计。 |
| 人审/审计机制 | 输出 JSON minigraph、ROUGE/FineSurE/case study；无 human-in-the-loop audit 或 claim-level provenance |
| 人类角色 | 无正式人审 gate；若有评价者仅作实验评价 |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | minigraph 结构级；无人工审计或 claim-level provenance。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 3 个 MSDS 数据集；graph/PLM/LLM baselines；ROUGE-1/ROUGE-2；ablation；reference-number 分组；FineSurE faithfulness/completeness/conciseness |
| 模型/API 设置 | GPT-4、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | CKMAs 在三数据集 ROUGE-1/2 上超过 graph、PLM、GPT-3.5/GPT-4、3A-COT、SumBlogger；ablation 显示 KMCA 和 MPSA 均贡献性能 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 可作为 综合 / 相关工作段落生成 的结构化 LLM baseline；对完整 agent 式 SLR 工作流 威胁有限，但其 minigraph 思路可用于 evidence relation representation |
| 受影响主张 ID | C3,C5,C6 |
| 威胁类型 | 局部覆盖 |
| 威胁的 paper2 主张 | 可作为 综合 / 相关工作段落生成 的结构化 LLM baseline；对完整 agent 式 SLR 工作流 威胁有限，但其 minigraph 思路可用于 evidence relation representation |
| 支持的 paper2 主张 | 支持 paper2 把报告生成 claim 收窄为“生成必须可审计”，并把 citation validity、unsupported claim 和 有证据支撑的断言 纳入评价。 |
| paper2 应避免的主张 | 避免声称自动 survey / review generation 尚无人研究；避免把文本流畅度、引用准确率或 LLM-as-Judge 总分等同于 SLR/SMS 方法学可靠性。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 给出项目页；是否含源码入口待打开核验 |
| 数据状态 | 使用三个 benchmark datasets；数据入口与 license 本轮未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径：🟢 强，🟡 中，🟠 弱，⚪ 无 / 背景。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟢 | 🟠 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Abstract；Introduction；Method | 论文明确面向 literature review generation / MSDS，任务是从多篇科学文献生成 related work summary。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | Introduction 两阶段定义；Method KMCA/MPSA | 作者把自动文献综述分成 selecting references 和 summarizing references，但本文只处理第二阶段 summarization；不覆盖检索和筛选。 |
| D3 LLM/agent 自动化深度 | 🟢 | Fig. 2；KMCA；MPSA | 使用两个 agent 模块、迭代 minigraph 构建、多路径专家式 summarization 和 router，自动化链条明确。 |
| D4 人工审计与可追踪性 | 🟠 | Table 1 JSON constraints；Case Studies；Discussion | 有结构化 JSON minigraph 和引用标记，但没有人工复核、审计日志、claim-to-source 验证或可导出 evidence packet。 |
| D5 评价严谨性 | 🟢 | Experiments；Tables 2-3；Figures 3/5 | 三个公开数据集、大量 baselines、ablation、case study 和 FineSurE 补充评价，评价扎实；但主要是自动指标。 |
| D6 SE / CCF 相关性 | 🟠 | bibtex: arXiv cs.CL；数据集为 MSDS/科学文献 | 泛 NLP/科学文献摘要，不是 SE SLR 或 CCF SE venue。 |
| D7 对本文 novelty 的威胁强度 | 🟡 | Method；Experiments；Conclusions | 威胁 paper2 的“结构化综合/关系建模辅助 related work 生成”局部模块；不覆盖多阶段 SLR workflow、人工审计 或 SE evidence synthesis。 |

## 3. 论文解决的问题与背景

该文认为自动 literature review 通常包含两个阶段：选择相关 reference documents，以及总结这些 references 形成领域演化叙述。它选择后半段，即 multiple scientific document summarization。作者指出 LLM 虽然能生成流畅文本，但不自然建模文献中的复杂关系，例如方法、材料、任务之间的并列、比较和使用关系，因此容易得到浅层或平铺事实的相关工作段落。

核心动机是给 LLM 提供结构化知识。作者没有使用通用 knowledge graph，而是动态从给定 reference abstracts 中抽取小规模 knowledge minigraph，强调与具体 research topic 相关的概念和关系。对 paper2 来说，它提供了“把文献证据转成显式结构再生成综合文本”的相关思路，但任务边界比 SLR/SMS 自动执行窄得多。

## 4. 方法 / 系统拆解

CKMAs 包含两个模块。KMCA 接收 reference abstracts，先按 chunk 拆分以避免长上下文问题，再用 prompt 让 LLM 抽取 JSON 格式关系。Prompt 有三类约束：输出必须是包含 head、head_type、relation、tail、tail_type 的 JSON；实体类型限定为 Task、Method、Metric、Material、Other-Scientific-Term、Generic；关系类型限定为 Compare、Used-for、Feature-of、Hyponym-of、Evaluate-for、Part-of、Conjunction；还用 volume constraint 只保留最重要的 `m` 条关系。中间 minigraph 会转换成文本格式，在后续 chunk 中迭代更新。

MPSA 在已构建的 knowledge minigraph、query abstract 和 reference abstracts 上生成 summary。先对 chunks 进行 summarization，再进行 path-aware summarization：作者观察 LLM 对 prompt 中 reference 顺序敏感，因此随机采样多个 chunk summary permutation 作为不同“路径”，让多个 expert 生成候选 summary。最后用 summarization router 计算每个候选与其他候选的 ROUGE-1 重叠，选择 agreement 最高的 summary 作为最终输出。

人机协作和审计不是该文重点。它的可追踪性主要来自 JSON minigraph 和 `@cite_id` 输出格式，但没有人工 audit 或错误裁决机制。

## 5. 实验 / 评价设计

实验使用 Multi-Xscience、TAD 和 TAS2 三个公开 MSDS 数据集。每个样本包含 query paper abstract、cited reference abstracts，以及 query paper 中的 related work paragraph 作为 gold summary。主干模型使用 GPT-3.5-turbo，temperature=0.0；chunk size `k=3`，专家数 `E=3`，volume constraint `m=32`。

指标主要是 ROUGE-1 和 ROUGE-2。Baseline 覆盖 graph-based methods，如 LexRank、TextRank、HeterSumGraph、GraphSum、TAG、KGSum；PLM/LLM methods，如 Pointer-Generator、BertABS、SciBertABS、HiMAP、BART、MGSum、PRIMERA、GPT-3.5-turbo、GPT-4；以及 3A-COT、SumBlogger。Ablation 分别移除 KMCA、MPSA、scientific constraint、volume constraint、iterative construction、chunk summary、path permutation 和 router。Discussion 中又用 FineSurE 比较 faithfulness、completeness、conciseness。

## 6. 主要结果与结论

Table 2 显示 Proposed 在 Multi-Xscience 上 ROUGE-1/2 为 36.41/8.78，在 TAD 为 34.16/6.22，在 TAS2 为 32.31/5.36，均为表中最佳。它超过 GPT-4、GPT-3.5-turbo、KGSum、SumBlogger 等强 baseline。Table 3 的 ablation 表明，去掉 KMCA 或 MPSA 都会下降；作者总结 MPSA 带来约 4% 性能增益，KMCA 带来约 2% 性能增益；KMCA 内部 iterative construction 贡献最大，MPSA 内部 router 贡献最大。

Figure 3 按 reference paper number 分组，显示 CKMAs 在不同 reference 数量下均优于 GPT-3.5-turbo，且 reference 越多差距越大。Case study 中，GPT-3.5 遗漏 citation，GPT-4 有并列事实但逻辑连接弱，CKMAs 更能按概率方法、统计方法、exemplar-based learning 等组织叙述。Figure 5 的 FineSurE 结果显示 CKMAs 在 faithfulness 和 conciseness 上优于 GPT-3.5-turbo，completeness 两者都中等。

## 7. 局限与可复现性

论文没有独立 Limitations 小节，但从方法和实验可见几类限制。第一，输入只用 query abstract 和 reference abstracts，不处理全文证据、筛选标准或 SLR protocol。第二，evaluation 以 ROUGE 为主，FineSurE 是自动 LLM 评价，缺少人类专家审查。第三，router 用候选 summary 间 ROUGE-1 agreement 选择输出，这可能偏向共识文本而非真实 factual correctness。第四，prompt-based minigraph 抽取本身可能出错，论文没有系统报告 JSON invalid、relation hallucination 或人工关系标注准确率。

可复现性相对较好：数据集公开、参数设置清楚、主干模型和 temperature 给出，并提供 project URL。但 `paper_content.txt` 没有展开代码可用性、完整 prompt 文件或运行日志。写作时应谨慎表述为“在 MSDS benchmark 上自动指标强”，不要扩大为“生成高可信完整 SLR”。

## 8. 对 paper2 story / 实验设计的影响

CKMAs 对 paper2 的最大启发是结构化中间表示。paper2 如果需要把多篇 SE 研究中的 task/method/evidence/metric 关系组织成 narrative synthesis，可以借鉴 minigraph 或 typed relation schema。但 paper2 应避免只停留在 summarization；必须把结构表示与筛选、抽取、审计和人类复核挂钩。

实验设计上，CKMAs 可作为 related-work generation 或 evidence synthesis 模块 baseline，尤其在“给定 reference set 生成综合段落”任务中。但如果 paper2 评估完整 SLR workflow，应把它列为局部 synthesis baseline，而不是 end-to-end baseline。指标也不能只沿用 ROUGE，应增加 claim support、citation correctness、evidence coverage 和 auditability。

## 9. 可用于写作的引用角度

可引用为“LLM-based literature review generation 中，显式抽取概念-关系 minigraph 能提升多文档科学摘要的组织性和自动指标表现”。也可引用为“给定 references 后的 synthesis 子任务已有结构化中间表示和多路径生成策略，但仍缺少人工审计和完整 SLR 流程覆盖”。

不应引用为“agent-based SLR 自动化系统”。该文的 agent 是 minigraph construction/summarization agent，不执行 SLR 检索、筛选、数据抽取或报告全流程。

## 10. 待复核清单

- Project URL 是否仍可访问，代码和 prompt 是否公开。
- 是否有正式 AAAI 版本，与 arXiv v3 是否一致。
- KMCA 抽取的 relation JSON 是否有人工标注准确率或 schema-invalid 统计。
- FineSurE 评价的 prompt、模型和样本范围是否可复验。
- 若 paper2 使用 minigraph 思路，需设计 SE-specific relation types 并验证其人工可审计性。
