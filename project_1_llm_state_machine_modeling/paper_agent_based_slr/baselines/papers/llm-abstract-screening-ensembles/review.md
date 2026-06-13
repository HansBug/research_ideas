# High-performance automated abstract screening with large language model ensembles

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | High-performance automated abstract screening with large language model ensembles |
| 年份 | 2024 |
| 作者 / venue / 出版状态 | Rohan Sanghera、Arun James Thirunavukarasu 等；arXiv:2411.02451; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 核对图表 |
| 研究脉络 | SLR/SMS 筛选、语料过滤与规划 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM 主要作为生成器、评价器或被综述对象；非多 agent 执行 workflow。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 23 个 Cochrane systematic reviews 的 replicated search records；小样本 800 条、全量 119,695 条 |
| 输出 | abstract screening 的 include/exclude、precision / recall / balanced accuracy、Kappa、一致性、ensemble 结果 |
| 方法/系统形态 | 6 个 LLM 的 prompt engineering + 人类研究者对照 + LLM-human / LLM-LLM ensemble；非 agent 系统 |
| 覆盖阶段 | 只覆盖 abstract screening；不覆盖检索、全文筛选、抽取、编码、综合或报告生成 |
| 不覆盖阶段 | 不覆盖检索、全文筛选、抽取、编码、综合或报告生成。 |
| 人审/审计机制 | 3 名 human researchers 作对照，提供 repeated screening、Kappa、补充 prompt；无 claim-to-source 或决策日志型审计包 |
| 人类角色 | 无正式人审 gate；若有评价者仅作实验评价 |
| 审计时机 | 运行前 + 运行后复核 |
| 主张追踪状态 | benchmark/gold 级；无 per-record provenance 或 claim trace。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 23 个 review、800 样本子集、119,695 全量记录；sensitivity、precision、balanced accuracy、specificity、F1、Kappa、correlation |
| 模型/API 设置 | GPT-4、GPT-4o、Claude、Sonnet、Gemini、Llama、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | prompt bias 强烈影响表现；LLM 在小样本和全量场景都可达高敏感度，但 precision 在大规模下显著下降；66 个 ensemble 达到完美 sensitivity，最高 precision 为 0.458 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强约束 paper2 的筛选阶段设计、prompt bias、ensemble 组合与“高敏感度优先”叙事；不构成完整 SLR workflow baseline |
| 受影响主张 ID | C5,C7 |
| 威胁类型 | 评价协议约束 |
| 威胁的 paper2 主张 | 强约束 paper2 的筛选阶段设计、prompt bias、ensemble 组合与“高敏感度优先”叙事；不构成完整 SLR workflow baseline |
| 支持的 paper2 主张 | 支持 paper2 把筛选阶段评价扩展到 false negative、模型变异、人工复核路由、成本和决策日志，而不是只报告 accuracy/F1。 |
| paper2 应避免的主张 | 避免把筛选 accuracy/F1 当作完整 SLR 自动化贡献；避免忽视 false negative、模型变异和人工复核成本。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Abstract / Page 2；Introduction / Page 3--4 | 原文直接讨论 systematic review 的 abstract screening 自动化，和 paper2 的证据筛选阶段高度贴合。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | `paper_content.txt` Methods / Page 4--9；Discussion / Page 17--21 | 研究只做 abstract screening 和 ensemble 决策，没有扩展到检索、全文抽取、编码、综合或报告生成，因此只覆盖一个核心环节。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt` Methods / Page 4--9；Supplementary Material 1 / Page 32 | 论文使用 API 化的 LLM 批量筛选、prompt 变体和 ensemble 规则，自动化程度足够高，但仍是单阶段分类器工作流，不是 agent。 |
| D4 人工审计与可追踪性 | 🟠 | `paper_content.txt` Page 8--9、21--22、32 | 论文有 3 名 human researchers 对照、Kappa、一致性比较和 GitHub 代码，但没有 claim-to-source、per-paper provenance、裁决日志或可导出的审计包。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt` Page 6--9、10--17、29--32 | 真实 Cochrane reviews、800 子集、119,695 全量记录、多人对照、ensemble 组合、相关性分析和补充材料，评价密度很高。 |
| D6 SE / CCF 相关性 | 🟠 | `paper_content.txt` Abstract / Page 2；Introduction / Page 3--4 | 任务是临床/医学 evidence synthesis，而非 SE；对本文更多是方法学背景和 screening 评价设计参考。 |
| D7 novelty 威胁强度 | 🟡 | `paper_content.txt` Page 18--21、32 | 它已经覆盖 prompt engineering、human+LLM 组合、series/parallel ensemble 和高敏感度优先策略，对 paper2 的 screening 设计有直接威胁；但缺少 SE 场景、端到端流程和审计链。 |

## 3. 论文解决的问题与背景

作者要解决的是：abstract screening 太费人，且人工筛选本身也有一致性和效率上限。论文把问题放在 Cochrane Library 的 systematic review 场景里，强调 screening 是在检索之后、全文筛选之前的关键门槛，假阴性会永久丢失相关研究，所以敏感度比表面 accuracy 更重要。

与 paper2 的关系在于，这篇工作已经把“自动化 screening”拆成了可操作的工程问题：prompt 如何偏向纳入、不同 LLM 如何比较、LLM 与人类如何并联或串联、什么时候应该宁可多报假阳性也不要漏掉真阳性。它不是端到端 review 生成，而是把 screening 这一步做成了明确的实验对象。

## 4. 方法 / 系统拆解

输入是 23 个 Cochrane systematic reviews 的 replicated search 结果。作者重建每个 review 的检索策略，把 inclusion list 当作 ground truth，再把所有可复现到的记录转换成 RIS / DataFrame。数据清洗后剔除了 8,604 条缺摘要记录，剩下 119,695 条可分析记录；另构造了 800 条小样本，用于较小规模实验和平衡抽样。

LLM 侧使用 6 个模型：GPT-3.5 Turbo、GPT-4 Turbo、GPT-4o、Llama 3 70B、Gemini 1.5 Pro、Claude Sonnet 3.5。方法不是 agent，而是通过 API 批量调用模型做二分类。作者构造了多个 prompt 版本：title only 控制组，以及 title+abstract 的 none/mild/moderate/heavy/extreme inclusion bias。Llama 的 prompt 还做了少量格式适配。CoT 和数值化打分被试过，但没进最终方案。模型返回无效输出或 API 错误时会重试，仍失败则按 include 处理，以最大化敏感度。

人机协作体现在两处：一是 3 名 human researchers 按原始 review criteria 在同一 800 样本上独立筛选；二是把 LLM 和 human decision 组合成 6 种 ensemble（series / parallel 的 LLM-human、LLM-LLM、human-human）。这类组合的目标不是追求单次最优 precision，而是构造更可部署的 screening 策略。

审计与日志方面，论文明确给出 GitHub 代码、Supplementary Material 1 的 prompt 版本，以及各模型的版本号、平台和参数设置；但没有把每条记录的决策理由、证据位置或人工裁决过程做成可回放证据链。

## 5. 实验 / 评价设计

RQ 核心不是很多，而是围绕 screening 工程决策展开：prompt wording 会怎样影响表现、不同模型之间是否稳定、LLM 与 human performance 是否可比、以及在全量检索结果上 precision 会不会崩。实验设计分三部分：小样本 800 条上的 prompt 搜索与模型比较、全量 119,695 条上的最优 prompt 复验、以及 66 个 ensemble 组合的精度/召回评估。

指标非常完整：sensitivity、specificity、accuracy、precision、recall、balanced accuracy、F1、Kappa，以及基于 Cochrane reviewer 数量的 performance ceiling。统计上使用了相关性分析来观察 prompt bias 与 precision / recall 的权衡，并用 review-centric factors 解释不同 review 的表现差异。Table 2、Table 3 和 Supplementary Material 1/2 构成了主要证据包。

baseline 方面，除了 3 名 human researchers，作者还用 Cochrane 原作者报告的结果构造了一个上界式参照。这样做的好处是能显示“模型看起来很好”是否只是因为数据子集更简单。缺点是 ground truth 仍依赖原 review 作者的 included list，因此上界可能偏乐观。

## 6. 主要结果与结论

最重要的结果是 prompt bias 决定了 LLM screening 的阈值。标题+摘要输入下，随着 inclusion bias 加强，recall 上升而 precision 下降；heavy / extreme prompt 往往更接近部署需要的高敏感度策略。GPT-3.5 在 heavy prompt 下对 800 样本和所有 reviews 都能达到 100% sensitivity，但 precision 并不总是高。

在 800 条子集上，LLM 的 best-case sensitivity、precision 和 balanced accuracy 都超过了三名 human researchers 的最高值；在全量 119,695 条上，sensitivity 仍然较高，但 precision 大幅下降到 0.004--0.096，说明大规模低阳性率场景会严重稀释表面表现。作者因此认为，abstract screening 仍适合“高敏感度优先”的自动化，而不是追求高 precision。

ensemble 结果进一步说明，LLM 与人类并联或串联可以更接近可用部署策略。66 个 ensemble 达到完美 sensitivity，最高 precision 为 0.458；其中最佳系统是 GPT-3.5 heavy bias 与 Sonnet extreme bias 的串联组合，sensitivity 约 0.996。作者最终结论是：LLM 可以辅助甚至替代部分 abstract screening 工作，但必须在具体 review 上做 domain-specific validation。

## 7. 局限与可复现性

原文自己承认三类局限。第一，代表性有限：虽然用了 Cochrane 全一卷的 23 个 review，但仍主要是医学/外科主题，不能直接推广到所有领域。第二，优化偏置：prompt engineering 先在 GPT-3.5 上做小规模探索，可能对它更有利。第三，benchmark 可能偏乐观：原作者的 included list 既是 comparator 也是 ground truth，可能高估了上界。

可复现性上，这篇论文比多数 screening 文章更完整：明确写了 Azure OpenAI、Vertex AI、Replicate、Python / R 版本、prompt 策略、GitHub 代码和 Supplementary Material。但 `paper_content.txt` 里仍出现一个小不一致：正文说采用 2023 Issue 8，Table 1 caption 却写成 2023 Issue 7，建议回 PDF 复核原始版式和版本。论文没有代码/数据封装成正式 run record，也没有记录逐条判定理由。

## 8. 对 paper2 story / 实验设计的影响

paper2 如果想谈 screening，不能只说“我们用了 LLM”，而要回答这个工作已经回答过的问题：prompt bias 如何控制阈值、为何要优先保证敏感度、为什么 human+LLM ensemble 可能比单点决策更稳。也就是说，paper2 至少要比较单模型、prompt 变体、并联/串联策略，不能把 ensemble 当成理所当然的新意。

但这篇论文也给了 paper2 一个清晰差异点：它只研究 abstract screening，没有覆盖检索、全文筛选、抽取、编码、综合、报告，也没有把结果写成完整证据链。paper2 可以把贡献放在端到端闭环、阶段间证据传递、错误修复和审计记录，而不是单一分类器本身。

## 9. 可用于写作的引用角度

- 临床/医学领域的 abstract screening 研究表明，prompt bias 会显著改变 LLM 的敏感度-精度权衡，因此自动筛选必须按目标任务调阈值，而不是默认追求平衡 accuracy。
- 该工作显示，LLM 与 human 组合成 series / parallel ensemble 后，可在高敏感度前提下改善抽样筛选表现，这为本文设计 human-in-the-loop 路由提供了先例。
- 23 个 Cochrane reviews 和 119,695 条记录的实验说明，单个小样本上得到的高分不能直接外推到全量检索结果；本文应保留规模、版本和 metadata 条件。
- 论文提供了较完整的 prompt、版本和代码说明，但没有形成 per-record provenance；本文可在审计链上进一步推进。

## 10. 待复核清单

- 人工打开 PDF 核对 Figure 1--3、Table 2--3 和 Supplementary Material 1/2 的最终版式。
- 复核正文里 2023 Issue 7 / Issue 8 的不一致，确认是抽取误差还是原文排版差异。
- 若用于写作，补核 GitHub 仓库是否仍可访问、是否有固定 commit / tag。
- 复核“错误输出按 include 处理”的策略是否与论文其他统计口径完全一致。
