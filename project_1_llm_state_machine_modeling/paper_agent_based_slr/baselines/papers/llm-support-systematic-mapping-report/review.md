# On the Use of a Large Language Model to Support the Conduction of a Systematic Mapping Study: A Brief Report from a Practitioner's View

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | On the Use of a Large Language Model to Support the Conduction of a Systematic Mapping Study: A Brief Report from a Practitioner's View |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Cauã Ferreira Barros、Marcos Kalinowski 等；arXiv:2602.10147; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | LLM 辅助文献综述与证据综合 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM 参与单阶段或少数阶段任务；未形成完整 agent 式 SLR 工作流。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 已有 SMS 的 219 篇 first-selection studies、13 篇 selected articles、预定义 protocol、inclusion/exclusion criteria、questionnaire extraction templates |
| 输出 | ChatGPT-4 的 screening decisions、data extraction answers、manual comparison、time/accuracy estimates、prompt adjustment lessons |
| 方法/系统形态 | 单 LLM prompt-based SMS support experience report；主模型 ChatGPT-4，附加测试 Gemini PRO、Manus、Copilot |
| 覆盖阶段 | protocol/search 仍由人工定义；LLM 支持 title/abstract screening 与 data extraction；analysis/synthesis 被认为不可靠 |
| 不覆盖阶段 | 不覆盖 paper2 设想的完整 agent evidence workflow；主要提供 SE 场景或筛选/方法学边界。 |
| 人审/审计机制 | 每项自动抽取由至少一名 human reviewer 检查；manual vs automated discrepancies 被记录并在 full-text reading 后讨论 |
| 人类角色 | 原文有人类参与线索；角色需在正式写作前复核 |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | manual-vs-automated discrepancy 级；无自动 claim-to-source ledger。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | manual vs LLM time comparison；screening 219 studies，data extraction 13 studies；其他模型用 50 / 10 study subsets |
| 模型/API 设置 | GPT-4、Gemini、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 重复；正式复现前需回原文核对 |
| 主要发现 | ChatGPT-4 screening 约 95% agreement（208/219，11 hallucinations），extraction 约 92.3% agreement（12/13，1 error）；时间从约 30 天降至约 10 小时，但 prompt design time 未计入 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强调 hybrid workflow、manual verification、prompt documentation、task-specific validation；也提醒 paper2 不应把 time saving 当作 methodological quality |
| 受影响主张 ID | C4,C5,C7 |
| 威胁类型 | 局部覆盖 + 背景定位 |
| 威胁的 paper2 主张 | 强调 hybrid workflow、manual verification、prompt documentation、task-specific validation；也提醒 paper2 不应把 time saving 当作 methodological quality |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免声称“首次 LLM/agent 自动化 SLR”“完整覆盖 SLR 生命周期”“PRISMA 合规”，也不得把 arXiv 预印本当作 CCF/peer-reviewed 事实。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 未提及源码；公开对象是 prompts 和 LLM outputs 的 Zenodo 记录 |
| 数据状态 | Prompts 与 LLM outputs 已给 Zenodo DOI；license 与复用条件本轮未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Page 1 Abstract：experience report on conduction of a systematic mapping study with LLM support；Keywords 含 Systematic Review / Mapping | 直接讨论 LLM 支持 SMS/SLR 执行，是 paper2 的直接近邻。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | Page 3 §3：protocol、search/selection、data extraction、verification；Page 4 §4.2：analysis extracted data 超过半数从其他来源取信息，不能可靠自动化 | 实际自动化覆盖 screening 和 data extraction 两个核心环节；protocol/search/analysis/synthesis 仍以人工为主。 |
| D3 LLM/agent 自动化深度 | 🟡 | Page 3：ChatGPT-4 structured prompt；Page 4 §4.3：Gemini PRO、Manus、Copilot subset tests | 有真实 LLM 执行和多模型试测，但不是 agent 工作流，也没有工具链/run record。 |
| D4 人工审计与可追踪性 | 🟡 | Page 3 §Verification and Risk Mitigation：每项自动抽取至少一名 human reviewer 检查，manual/automated discrepancies recorded and discussed | 有人工核验和 discrepancy 记录，但缺少可导出的 source-level provenance、claim trace 或完整审计日志。 |
| D5 评价严谨性 | 🟡 | Page 4 Table 1：219 screening、13 extraction、time/accuracy；Page 5 §5.2：样本和 scope limitations | 有真实 SMS、人工参考、时间/准确率比较；但 single researcher、单 SMS、小抽取样本、非并行对照，故中等。 |
| D6 SE/CCF 相关性 | 🟢 | Page 1 ACM reference：WSESE '26；CCS Software and its engineering；Page 2：Software Engineering systematic reviews/mappings | 直接面向 SE systematic mapping，并有 ACM workshop DOI。 |
| D7 对本文 novelty 的威胁 | 🟡 | Page 6 Conclusion：LLMs support screening and data extraction but require hybrid workflows；Page 5 Lessons：human supervision、structured templates、prompt documentation | 威胁 paper2 的 screening/extraction support 和 human verification claim；不覆盖 agentic multi-stage workflow、claim-to-source 报告生成 和完整 评价基准。 |

## 3. 论文解决的问题与背景

论文指出 SE systematic mappings/reviews 包含筛选大量研究、阅读全文和结构化抽取等耗时步骤，容易受 reviewer inconsistency 和 cognitive fatigue 影响。已有研究多评估单个阶段，例如 screening 或 extraction，但较少报告在一个真实 SMS 中端到端使用 LLM 的实践过程、时间比较、错误和 prompt 调整。作者因此回到一个既有 SMS，报告用 LLM 支持 study selection 和 data extraction 的实践经验。

需要注意：这篇文章不贡献新的 domain findings。正文明确说原 SMS 研究 LLM 支持 qualitative research / qualitative analysis，本篇只分析在该 SMS 中用 LLM 自动化和比较 key stages 的实践影响。

## 4. 方法 / 系统拆解

输入是既有 SMS protocol：研究问题、数据库、inclusion/exclusion criteria 和 extraction procedure。manual procedures 来自作者先前工作，发生在 2024 年 11 月到 2025 年 1 月；LLM-based conduction 发生在 2025 年 7 月到 10 月。作者承认这会带来 manual execution time 的 recall bias。

selection 阶段先由人工按 criteria 筛选 title/abstract，随后用 ChatGPT-4 和 carefully structured prompt 重做相同过程。data extraction 阶段也在两个条件下完整执行：人工用 standardized forms；LLM 用 questionnaire-format extraction templates。每篇 selected article 都做 manual 和 LLM 两套结果，之后人工检查 LLM output 的 consistency 和 accuracy。

风险缓解采用 double-checking：自动抽取的每个数据项至少一名 human reviewer 检查；manual 和 automated discrepancies 记录下来，并在 full-text reading 后讨论。作者还说明 prompt 在 screening 中调整 4 次、extraction 中调整 6 次。analysis of extracted data 被认为无法可靠自动化，因为超过半数案例中模型从 target study 以外的来源取信息。

## 5. 实验 / 评价设计

评价不是 benchmark，而是 practitioner experience report。主要比较 manual execution 与 LLM-assisted execution 的时间和 agreement。manual screening 219 studies 约 23 天，manual extraction 13 studies 约 7 天，共约 30 天，两名研究者完成。LLM-assisted screening 219 studies 约 9 小时，extraction 13 studies 约 1 小时。作者特别说明 manual 30 天并非连续工作，且 prompt design 和 iterative refinement 未计入 LLM time。

准确性以 human reviewer consensus / manual result 作为 reference standard。ChatGPT-4 screening 208/219 correct，约 95%，有 11 个 hallucination cases；data extraction 12/13 correct，约 92.3%，有 1 个 error。其他模型只做 exploratory subset：screening 50 studies 中 Manus 49/50、Gemini PRO 45/50、Copilot 30/50；extraction 10 studies 中 Manus 4/10、Gemini PRO 9/10、Copilot 6/10。作者明确说这不是为了判定哪个模型优于 ChatGPT，而是探索 future investigation。

## 6. 主要结果与结论

主要发现有四点。第一，LLM 可显著减少 repetitive task 时间，但上下文相关，不能当作普遍节省比例。第二，prompt design 很关键；open-ended questions 更容易导致冗长回答和 unsupported additions，option-based answers 更一致。第三，human oversight 仍然必要；11 个 screening hallucinations 和 1 个 extraction error 都是人工核验发现的。第四，hybrid workflow 是当前更可靠路线，LLM 可支持执行，但 interpretation、verification 和 synthesis 仍应由研究者负责。

结论部分将 LLM 定位为支持 systematic reviews 的 promising tools，但必须嵌入 partial automation + critical supervision 的 hybrid workflow。作者明确否认 LLM 能替代 researcher 在 systematic mappings 中的角色。

## 7. 局限与可复现性

局限非常明显。结果来自 single researcher / single SMS，受 expertise、domain、prompt design、interpretation strategy 影响。manual 和 LLM-assisted execution 顺序进行，不是并行受控实验；manual time 估计可能不精确。data extraction 只有 13 studies，其他模型测试更小：50/10。prompt 具体文本在 `paper_content.txt` 中没有完整列出，只有 prompt 调整次数和 structured templates 描述。

可复现性中等偏弱：论文有 DOI 和清楚数值，但没有完整 prompt、原始输出、discrepancy table 或数据包。paper2 若采用其经验，应该吸取其教训：prompt、模型版本、input records、raw outputs、人工核验记录和错误分类都要进入 run record。

## 8. 对 paper2 story / 实验设计的影响

paper2 不能把“LLM 支持 SMS 的筛选和抽取”写成无人做过。该 work 已在 SE SMS 中做了真实流程比较，并报告 time/accuracy/hallucination。paper2 的差异化应是 agentic workflow、阶段间证据链、claim-to-source trace、run record、审计 gate 和更严谨的实验协议。

实验设计上，paper2 应避免只报节省时间。需要把 prompt design time、人工审计时间、错误修复时间、false negative / false positive、unsupported extraction、source drift 都计入成本。作者关于“分析阶段不可靠”的观察也提醒 paper2：开放式 synthesis 应保留人工解释权，或设计更强的证据约束。

## 9. 可用于写作的引用角度

- 作为 SE practitioner evidence：LLM 在 SMS screening/extraction 中可显著减少重复劳动，但仍需持续人工核验。
- 作为风险引用：真实 SMS 中出现 hallucination 和从非目标文献取信息，说明 source-bounded extraction 和 audit trail 很重要。
- 作为 paper2 方法动机：structured templates、prompt documentation、manual verification 和 hybrid workflow 是 agent-based SLR 系统的最低要求。

## 10. 待复核清单

- 回 PDF 核对 Table 1 和 Table 2 的排版及是否有脚注说明。
- 查 DOI/ACM 页面确认 WSESE '26 版本和 arXiv 版本一致。
- 若引用 time reduction，必须同时写 prompt design time 未计入、manual time 有 recall bias、非受控并行比较。
- 需要补充完整 prompt/output 数据是否公开；正文未明确给出。
