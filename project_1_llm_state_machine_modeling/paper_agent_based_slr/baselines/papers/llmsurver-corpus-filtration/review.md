# Leveraging LLMs for Semi-Automatic Corpus Filtration in Systematic Literature Reviews

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Leveraging LLMs for Semi-Automatic Corpus Filtration in Systematic Literature Reviews |
| 年份 | 2025 |
| 作者 / venue / 出版状态 | Lucas Joos、Daniel A. Keim 等；arXiv:2510.11409; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 核对图表 |
| 研究脉络 | SLR/SMS 筛选、语料过滤与规划 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 来自真实 SLR 的初始候选库；preliminary version 为 8,323 篇，88 relevant / 8,235 irrelevant |
| 输出 | 文献 corpus 的 include / discard、mid-2024 与 fall-2025 多模型评测、consensus 结果、prompt 优化结果 |
| 方法/系统形态 | 多 LLM 并行分类 + consensus voting + human-supervised visual analytics web app `LLMSurver`；不是完整 SLR agent |
| 覆盖阶段 | keyword-based search、去重与预处理、标题/摘要分类、最终过滤；不做全文抽取、综合或报告生成 |
| 不覆盖阶段 | 不覆盖检索策略冻结、全文抽取、编码、综合、报告生成和报告级 claim-to-source。 |
| 人审/审计机制 | 用户可实时检查、修改 prompt、选择模型、比较 consensus、查看 reasonings 并导出结果；有强 human-in-the-loop，但非 claim-to-source 证据链 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 运行前 + 运行后复核 |
| 主张追踪状态 | reasoning 导出与 UI 审查级；无来源位置级 claim trace。 |
| 决策日志状态 | per-record / reasoning 级线索；导出格式待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | mid-2024 5 模型、fall-2025 13 模型、8,323 级大库；accuracy、precision、recall、F1、混淆矩阵、prompt 变体对比 |
| 模型/API 设置 | GPT-5、GPT-4、GPT-4o、Claude、Sonnet、Gemini、Llama、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | consensus 比单模型更稳，尤其能压低 false negatives；open 模型在 2025 年显著进步；小模型 prompt 敏感，prompt 微调可大幅改变 recall/precision |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 对 paper2 的 corpus filtration、consensus 规则、人机监督 UI 和 prompt 敏感性提供强局部 baseline；但不覆盖完整 SLR workflow |
| 受影响主张 ID | C2,C5,C7 |
| 威胁类型 | 局部覆盖 + 评价协议约束 |
| 威胁的 paper2 主张 | 对 paper2 的 corpus filtration、consensus 规则、人机监督 UI 和 prompt 敏感性提供强局部 baseline；但不覆盖完整 SLR workflow |
| 支持的 paper2 主张 | 支持 paper2 把筛选阶段评价扩展到 false negative、模型变异、人工复核路由、成本和决策日志，而不是只报告 accuracy/F1。 |
| paper2 应避免的主张 | 避免把筛选 accuracy/F1 当作完整 SLR 自动化贡献；避免忽视 false negative、模型变异和人工复核成本。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 给出 GitHub 源码且声称 MIT；本轮未打开 URL/commit，license 仍待核验 |
| 数据状态 | 使用 8000+ papers ground-truth 数据；公开程度与 license 待核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Abstract / Page 1；§1 / Page 2--3 | 原文直接研究 SLR 的 corpus filtration / paper pre-selection，且明确使用 LLM、consensus 和 human supervision。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | `paper_content.txt` Figure 1 / Page 2；§3 / Page 3--4 | 覆盖 keyword-based search、preprocessing、LLM classification、final filtration 四段，但只停留在文献入库与筛选，不进入抽取、编码、综合或报告。 |
| D3 LLM/agent 自动化深度 | 🟢 | `paper_content.txt` Abstract / Page 1；§3 / Page 3；§5 / Page 6--10 | 多个 LLM 逐篇分类，再通过 consensus harmonization 得到最终决策，属于明确的多模型自动化工作流，且有 prompt 迭代和模型选择。 |
| D4 人工审计与可追踪性 | 🟢 | `paper_content.txt` Abstract / Page 1；§4 / Page 4；§6.1 / Page 11 | 用户可以实时检查与修改模型输出、reasonings、prompt 和 consensus scheme，导出结果，并通过视觉分析理解歧义和错误；这已经是强 human-in-the-loop 审计，但不是逐条 claim-level provenance。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt` §5 / Page 5--10；Table 2--4 | 使用真实 8k+ corpus、validated human ground truth、mid-2024 与 fall-2025 两轮评测、混淆矩阵、prompt 变体和多种 consensus，评价密度高。 |
| D6 SE / CCF 相关性 | 🟠 | `paper_content.txt` Page 1--2；References [9], [10], [15], [19] | 主题是通用 CS / visual network analysis 的 SLR 工具支持，而不是 SE 直接场景；对本文更多是方法学背景和 corpus filtering 参考。 |
| D7 novelty 威胁强度 | 🟡 | `paper_content.txt` §3--§6 / Page 3--11；Table 2--4 | 它对 paper2 的 corpus filtering、consensus 设计、prompt 敏感性和人监督 UI 构成直接局部威胁，但不覆盖全文抽取、综合、报告或 claim-to-source 链。 |

## 3. 论文解决的问题与背景

作者要解决的是 SLR 里最耗时的前置工作：从大量检索结果中筛掉明显无关的论文。论文指出，keyword-based search 往往产生大量噪声，人工标题/摘要筛选既慢又容易受疲劳影响。对 8,000 量级的候选库，即使经验研究者按每分钟两篇的速度筛选，也会消耗大量时间。

这篇工作的背景不是“LLM 是否能写综述”，而是“LLM 是否能作为第一道文献过滤器”。它把 SLR 结构拆成 keyword search、preprocessing、LLM classification 和 consensus filtration 四段，并坚持人类保留控制权。对 paper2 而言，这正好对应 corpus filtration、模型协同和 human supervision 三个局部设计点。

## 4. 方法 / 系统拆解

输入来自一个真实的 SLR 数据集。preliminary version 中，作者处理了 8,323 篇候选论文，人工 ground truth 标记出 88 篇 relevant 和 8,235 篇 irrelevant。后续又在 fall 2025 阶段复用同一任务，评估更大规模、更多开源与商业模型的表现。

方法流程是四段式。第一段是 keyword-based search，从在线库和仓储里获取候选论文。第二段是 preprocessing，包括 duplicate removal、type filtering、metadata unification。第三段是多个 LLM 基于标题和摘要做逐篇分类，每个模型使用定制 prompt。第四段是 consensus voting，默认采用“只要任一模型建议 include，就保留；只有全部拒绝才 discard”的保守策略。

LLMSurver 是这篇工作的核心系统。它是一个开源、容器化、单页 React 前端，基本都在浏览器内本地运行，只有 LLM API 调用是例外。界面包含 paper table、prompt editor、LLM 选择与执行控制、consensus 与统计视图、以及用于比较模型分歧的可视化图表。用户可以上传 BibTeX、DOI 等元数据，查看单条输出及其 reasoning，导出 CSV，切换模型和 prompt，甚至将局部样本和全量语料分开跑。

审计机制的关键不是静态日志，而是交互式控制。用户可以查看模型 reasoning、发现歧义、调整 prompt 和 consensus scheme，再重新跑样本。这个闭环比单纯“自动化分类”更接近可审计流程，但论文没有把每次决策整理成 claim-to-source 或 page-level provenance。

## 5. 实验 / 评价设计

作者分三轮评测。第一轮是 mid-2024 模型：Llama 3 8B、Llama 3 70B、Gemini 1.5 Flash、Claude 3.5 Sonnet、GPT-4o。第二轮是 fall 2025 模型：8 个开源模型和 5 个商业模型，共 13 个。第三轮是针对 Llama 3.1 8B 的 prompt 优化。

mid-2024 的评测使用 validated human classification 作为 ground truth。Table 2 显示，单模型 accuracy 都在 90% 以上，但 precision 和 recall 差异较大：开源模型更偏向 include，因此 recall 高、precision 低；商业模型更严格，precision 和 F1 较好，但会带来更多 false negatives。Consensus All 与 Consensus Best 都保持了很高 recall，其中 Consensus Best 在只用 3 个较优模型的情况下，TP=87、FN=1、Precision=34.25、Recall=98.86、F1=50.88，且比 all-model consensus 更少误报。

fall 2025 的结果更强。Table 3 表明，所有模型 accuracy 约在 95%--99%，其中较强模型的 precision、recall 和 F1 明显改善。Consensus Best 进一步达到 TP=88、FN=0、Precision=34.65、Recall=100、F1=51.46；Consensus All 也做到 Recall=100，但 false positives 更多。作者由此主张：小而优的模型子集比全量投票更高效，也更利于控制手工复核负担。

prompt 优化是第三个实验块。作者选取 Llama 3.1 8B，针对原始 prompt 设计了 P1--P7 七个变体。原始 prompt 的准确率、precision 和 F1 最好，但 recall 不是最高；更宽松的 prompt 可以把 FN 大幅压低，代价是 FP 爆炸式增长。最极端的 P7 达到 Recall=100，但 Precision 仅 2.18，说明 prompt 规则的微调会强烈移动阈值。

## 6. 主要结果与结论

这篇论文最强的结论是：LLM 不是单独用来“猜对”，而是用来把人工过滤工作缩到可管理范围。mid-2024 中，LLM 已经能比单个人类筛选者更好地维持召回；到 fall 2025，开源模型的表现明显进步，某些组合已经接近或超过商业模型的实用水平。

consensus 是这篇工作的关键发现。单个模型往往会在少量论文上犯错，但不同模型的错误重叠不大，因此保守投票可以显著降低 false negatives。对 corpus filtration 来说，这比追求单次高 precision 更重要，因为漏掉相关论文的代价更高。作者也因此强调，在 early filtering 阶段宁可多保留一些候选，再由后续人工步骤清理。

prompt 敏感性同样被证明非常强。对于小模型，哪怕只改“uncertain 时是 include 还是 discard”这种规则，结果也会明显变化。P6 和 P7 这类由 GPT-5 改写的 prompt 虽然提高 recall，但会让 false positives 迅速上涨。这个结果说明，LLM screening 的性能不是模型大小的单变量函数，prompt 设计和 consensus 规则同样是核心控制点。

## 7. 局限与可复现性

作者自己列出的局限比较明确。第一，评测只针对一个 computer science 主题和一个真实 SLR，外推到其他领域仍未验证。第二，方法依赖 abstract-level 信息，没有引入 full-text 上下文。第三，模型不断演进，API 版本漂移会让复现不稳定。第四，没有正式 user study。第五，LLM 主要用于后续过滤，而不是初始候选搜索，以免引入错误引用。

可复现性方面，这篇比一般工具论文更好：它给出公开 GitHub 代码、MIT License、在线 demo、模型名称、prompt 版本和评价表格。与此同时，`paper_content.txt` 里可以直接看到“no backend”“local within browser”这些工程约束，说明它把 privacy 和可部署性当成设计目标。真正欠缺的是更细粒度的决策日志和可回放的审计包。

## 8. 对 paper2 story / 实验设计的影响

这篇是 paper2 的局部强对照。只要 paper2 涉及 corpus filtration、初筛、consensus、模型分歧分析或人机协作界面，就必须回应它：为什么你的 consensus 规则更合理，为什么你的 prompt 更稳，为什么你的人工监督不会变成不可控的手工补丁。

paper2 可以从它这里借走两点，但要升级。第一，任何筛选系统都应明确“谁保留控制权”，并把 prompt / model / consensus 作为可调对象。第二，低 false negative 的策略往往会产生较高 false positives，paper2 需要说明如何把这种误报控制在可接受范围内，并把人工复核与证据链补上。

## 9. 可用于写作的引用角度

- 该工作表明，SLR corpus filtration 可以通过多 LLM + consensus voting 显著降低手工负担，且保守投票策略有助于控制 false negatives。
- LLMSurver 提供了一个可交互、可本地运行的审计界面，支持 prompt 编辑、模型选择、输出 reasoning 检查和结果导出，适合用来说明 human-in-the-loop 过滤流程。
- 最新开源模型在 2025 年已明显追近商业模型，说明 corpus filtration 的模型选择不应只看闭源旗舰；本文需要把 open/commercial baseline 都纳入。
- prompt 的微调会显著改变 recall/precision 平衡，因此本文若使用 LLM 过滤器，必须把 prompt 版本和决策阈值写入运行记录。

## 10. 待复核清单

- 人工打开 PDF 核对 Figure 1、Figure 3、Table 2、Table 3 和 Table 4 的排版与最终数值。
- 复核 LLMSurver 的 GitHub 仓库和在线 demo 当前是否可访问，以及 MIT License 是否仍然有效。
- 复核 Table 1 中 mid-2024 / fall 2025 模型 tag 的完整版本号，尤其是开源模型名称。
- 若用于 paper2 写作，补核该论文是否有后续扩展版或更多任务场景。
