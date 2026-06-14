# On the Difficulties of Conducting and Replicating Systematic Literature Reviews Studies Using LLMs in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | On the Difficulties of Conducting and Replicating Systematic Literature Reviews Studies Using LLMs in Software Engineering |
| 年份 | 2025 |
| 作者 / venue / 出版状态 | Katia Romero Felizardo、Anderson Deizepe、Daniel Coutinho、Genildo Gomes、Maria Meireles、Marco Gerosa、Igor Steinmacher；WSESE@ICSE 2025 workshop；IEEE Xplore DOI: 10.1109/WSESE66602.2025.00010；本轮按 CCF-adjacent workshop 处理，不等同 ICSE main track 或 CCF A 主会论文 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；PDF 已本地保存，但图表/版式没有额外逐页人工校验；本文仅 4 页、无复杂实验图表 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)；PDF 由用户从 Zotero/IEEE Xplore 人工下载并于 2026-06-14 存入本目录 |
| 研究脉络 | 软件工程 SLR 方法学、LLM 辅助 SLR 的可复制性与困难总结 |
| 引用角色 | SE 领域直接方法学近邻 / reviewer 风险提示 / 负面证据与开放问题来源 |
| LLM/agent 角色 | 该文不提出新的 LLM/agent 系统；它分析 SE 中两篇已有 LLM 支持 SLR 研究，并讨论 prompt、随机性、输入信息、透明性、模型可用性、成本和数据仓库等困难 |
| 证据溯源粒度 | 论文层面的困难清单和被分析研究描述；无自动 claim-to-source ledger 或 per-record 决策日志 |
| 输入 | Scopus 检索得到的 89 篇候选，筛选至 21 篇 LLM 支持 SLR 候选，再按 SE 语境纳入 2 篇研究；同时抽取研究目标、支持的 SLR 活动、LLM 模型/参数/prompt、指标和样本规模 |
| 输出 | 10 类困难 / 开放问题：prompt sensitivity、LLM randomness、title/abstract 信息不足、排除标准边界、few-shot 选择负担、黑箱/透明性、模型配置不可持续、成本、全流程支持不足、SE SLR 数据仓库稀缺 |
| 方法/系统形态 | 短论文式方法学讨论；先检索/筛选 SE LLM-SLR 研究，再对两个纳入研究做人工抽取与验证，最后归纳困难 |
| 覆盖阶段 | 主要讨论 study selection / title-abstract-keywords screening；也讨论 search string、data extraction、synthesis、全流程支持和 SLR 数据仓库，但不是自己实现这些阶段 |
| 不覆盖阶段 | 不提供 agent workflow、自动抽取/编码/综合/报告生成系统，不提供可运行 baseline，不提供 claim-level provenance 或 run record |
| 人审/审计机制 | 论文方法中一名作者抽取、两名作者验证数据；正文强调 SLR 应产生 auditable/reproducible results，但没有提出自动审计机制 |
| 人类角色 | 人工筛选 / 人工抽取 / 人工验证；属于研究者人工分析，不是运行中 agent 审计 gate |
| 审计时机 | 运行后人工验证；非 production workflow gate |
| 主张追踪状态 | 无自动 claim-to-source trace；困难列表可回到 Page 2--4 的条目证据 |
| 决策日志状态 | 无或仅论文叙述；未提供逐记录筛选日志 |
| 冲突处理机制 | 原文没有说明多研究者分歧如何系统裁决 |
| 审计导出性 | 不可导出或仅论文叙述；不能当作可审计制品 baseline |
| 实验/指标 | Scopus 89 篇 → 21 篇 → 2 篇；两篇被分析研究分别涉及 20 篇 human screening 样本与 5 个 SLR 数据集 / 5144 studies；该文自身没有新 LLM 实验 |
| 模型/API 设置 | 讨论 Study 1 的 GPT-3.5-turbo-0613、GPT-3.5-turbo-16k-0613、GPT-4-turbo-0613，以及 Study 2 的温度 0、seed 128、context/cut-off 信息；该文没有自己调用模型 |
| 提示词状态 | 原文比较两项研究的 prompt 设计差异，但不提供本文自己的可复用 prompt 包 |
| 温度/重复/随机种子 | 仅报告被分析研究中的温度/seed/context/cut-off 细节；本文自身无 LLM 运行设置 |
| 主要发现 | SE 领域使用 LLM 支持 SLR 仍集中在筛选阶段；prompt、随机性、信息不足、透明性、模型漂移/不可用、成本和缺少 SE SLR 数据仓库会直接影响复现性 |
| 关键结果锚点 | Page 2 §Method：检索式、89→21→2、抽取字段；Page 2--4 §III：10 个困难；Page 4 §Final Remarks：贡献和局限 |
| 数值使用许可 | 可文本级引用；若正式论文使用 89/21/2、5144、模型参数或成本数字，建议回 PDF/IEEE 元数据再核对 |
| 对 paper2 的作用 | 强化 paper2 的 SE 直接动机：SE 社区已经明确指出 LLM-SLR 的 prompt、随机性、透明性、成本、模型可得性和数据仓库缺口；paper2 的 story 应把 run record、model/prompt 配置、人工审计、数据集管理和 failure taxonomy 作为核心 |
| 受影响主张 ID | C4,C5,C7 |
| 威胁类型 | 负面证据 + 评价协议约束 + 背景定位 |
| 威胁的 paper2 主张 | 威胁“SE 社区尚未讨论 LLM 辅助 SLR 困难 / 复现性”这类背景 claim；也约束 paper2 不能忽略 prompt 敏感性、模型不可持续和成本 |
| 支持的 paper2 主张 | 支持 paper2 以 SE SLR/SMS 的可审计 evidence workflow、透明 run record、prompt/model/config 记录和复现实验为贡献，而不是只做文本生成工具 |
| paper2 应避免的主张 | 避免写“SE 领域没有 LLM-SLR 方法学讨论”；避免只报告 accuracy/time saving 而不处理 prompt、随机性、成本、模型漂移、数据仓库和透明性 |
| baseline 可用性 | 协议/指标baseline或背景强近邻；不可作为 executable baseline |
| 对比方式 | 作为 Related Work / reviewer-risk / problem-motivation 证据；不做运行对比 |
| 代码状态 | 未提及源码入口；本文不是工具论文 |
| 数据状态 | 未提供新数据仓库；讨论中指出 SE 缺少 Systematic Review Data Repository，并呼吁更开放、可追踪、文档化的 replication packages |
| 许可状态 | PDF 来源为 IEEE Xplore 人工下载；本仓库仅保存本地研究使用副本；不得据此声称可再分发 |
| 制品入口 | 无可运行 artifact；本地仅保存 PDF、抽取文本、BibTeX 和本 review |
| 运行可行性 | 仅 related-work / protocol-risk 背景；不可运行 baseline |
| 可复现资产 / 阻塞项 | 若正式引用，需要核验 IEEE Xplore 页、DOI、WSESE workshop 归属；若使用参考文献 [9]/[10] 的模型参数或数据集数字，需要回对应原文复核 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。本条已从原先 title-level 粗筛升级为全文文本核验。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟠 | 🟠 | 🟠 | 🟢 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Page 1 Abstract / Introduction：明确讨论 LLM 支持 SE SLR 的 conducting 与 replication difficulties | 主题直接落在 LLM + SLR + 软件工程，和 paper2 的研究背景高度贴合。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | Page 2 §Method：纳入研究主要是 title-abstract screening；Page 3--4 §III.9：指出全流程支持仍不足 | 论文讨论多阶段困难，但自身分析集中在 study selection，未实际覆盖检索、抽取、编码、综合和报告工作流。 |
| D3 LLM/agent 自动化深度 | 🟠 | Page 2：描述 Study 1/2 使用 GPT 模型做筛选；本文自身没有新系统 | 该文是困难讨论，不提出新的 LLM/agent 自动化流程，因此自动化深度弱于 P0 工具/benchmark 论文。 |
| D4 人工审计与可追踪性 | 🟠 | Page 2 §Method：one author extracted, two others verified；Page 3 §III.6：指出 LLM 黑箱和缺少透明性 | 有人工验证和透明性问题意识，但没有可执行审计设计、provenance schema 或 claim-to-source 机制。 |
| D5 评价严谨性 | 🟠 | Page 2：Scopus 89→21→2；Page 4 Final Remarks：承认只分析两篇文章、representativeness limited | 作为 short workshop paper，它提供小规模方法学分析和困难清单，但样本只有 2 篇，不能当作强实证评价。 |
| D6 SE / CCF 相关性 | 🟢 | `bibtex.bib`：WSESE@ICSE 2025；Page 1--4 多次定位 SE / SLR | 直接来自软件工程方法学 workshop，且讨论 SE SLR，D6 强；但它是 CCF-adjacent workshop，不是 ICSE main track。 |
| D7 对本文 novelty 的威胁 | 🟡 | Page 2--4 §III：10 个困难覆盖 prompt、随机性、透明性、模型可用性、成本和数据仓库；Page 4：呼吁 SE 社区继续研究 | 不威胁 paper2 的 agent workflow 实现，但强约束 paper2 的 motivation、实验指标、复现性和 claims-to-avoid。 |

## 3. 论文解决的问题与背景

论文从 SE SLR 的人工成本、筛选困难、证据抽取和综合异质性出发，指出 LLM 有潜力降低工作量，但 SE 技术领域还缺少足够证据来证明 LLM 在 SLR 中的准确性和可复制性。作者把问题收窄为：使用 LLM 进行或复制 SE SLR 研究时到底会遇到哪些困难。

这篇论文对 paper2 的意义不是提供一个可运行对手，而是提供了 SE 社区内部的直接问题陈述：如果我们要写 agent-based SLR，不能只说 LLM 可以省时间，而必须回答 prompt 敏感、随机性、输入信息不足、黑箱、模型版本不可持续、成本和数据仓库缺口这些方法学问题。

## 4. 方法 / 系统拆解

作者在 2024 年 9 月使用 Scopus 检索 SE 领域中 LLM 支持 SLR 的文章。检索式包含 systematic literature review / systematic review / SLR、large language model / LLM / ChatGPT / GPT / Llama / Gemini、software engineering，并限制计算机学科。初始得到 89 篇，按“使用 LLM 支持 SLR process”降到 21 篇，再按“SE context”最终纳入两篇。

数据抽取关注六类信息：研究 context 和 objective、LLM 支持的 SLR activity、LLM 如何用于 SLR 的 study design、模型/参数/prompt、评价 metric、样本规模。抽取由一名作者完成，两名作者验证。

纳入的 Study 1 聚焦 title-abstract screening：让人类研究者处理 20 篇文章的原始/简化摘要，并用 GPT-3.5 / GPT-4 系列复制任务，比较 zero-shot、one-shot、few-shot、CoT 等 prompt 技术，指标是 precision 和 recall。Study 2 分析 prompt variations 对 title/abstract/keywords 初始筛选的影响，用五个 SLR 数据集合计 5144 studies，记录 include/exclude 分布并报告 Precision、Recall、NPV、Specificity、Work Saved over Sampling、Balanced Accuracy、MCC 等指标。

## 5. 实验 / 评价设计

本文自身不是实验系统，而是对两篇已有 SE LLM-SLR 研究做方法学归纳。核心评价对象是这些研究的可复制性和困难，不是某个新模型的性能。

作者归纳了 10 个困难：

1. prompt 敏感，轻微 wording 或格式差异可能改变筛选判断；
2. LLM 固有随机性影响 SLR 复现；
3. 仅给 title/abstract/keywords 信息不足；
4. 某些排除标准需要 publication date、study type、language、duplicate version 等元信息；
5. few-shot 负例选择需要人工阅读和判断，成本高；
6. LLM 黑箱，缺少解释 included/excluded 的机制；
7. cloud model / ChatGPT 配置和版本可能随时间消失；
8. GPT-4 等强模型成本高，复制大规模实验会昂贵；
9. SE 现有研究主要集中 study selection，尚未充分支持 SLR 全流程；
10. SE 缺少类似医学领域的 SLR 数据仓库，影响比较、复用和更新。

## 6. 主要结果与结论

本文的主要结论是：LLM 可为 SE SLR 提供机会，但当前证据不足，尤其缺少对 SE 技术语境中不同 SLR 阶段的系统验证。作者强调，负责地引入 LLM 需要同时评估优点与弱点；prompt 设计、模型配置、成本、透明性、数据仓库和复现包是未来研究的关键。

对于 paper2，最重要的不是它提出了新工具，而是它给出了 reviewer 很可能追问的 checklist：是否固定模型版本、是否记录 temperature/seed/context/cut-off、是否记录 prompt、是否解释筛选决策、是否处理 title/abstract 信息不足、是否报告成本、是否有可复用数据包。

## 7. 局限与可复现性

原文明确承认代表性有限：只分析一种 empirical study type，即 SLR，并且最终只有两篇 SE 研究纳入。因此它不能支持“SE 中所有 LLM-SLR 困难已经穷尽”的强结论。

可复现性方面，本文没有发布新代码或新数据仓库；它依赖对两篇已有研究的抽取和讨论。PDF 来自 IEEE Xplore，正式写作时应引用 DOI 和 WSESE@ICSE 2025 workshop 信息，并避免把它写成 CCF A 主会或完整系统综述。

## 8. 对 paper2 story / 实验设计的影响

这篇论文直接支持 paper2 把“可审计性和复现性”作为主线。具体而言，paper2 后续实验和 run record 至少应显式记录：模型 ID、provider、prompt、temperature、seed/repeats、context length、调用日期、成本/token、输入字段、筛选决策、人工复核、错误类型和不可复现风险。

同时，paper2 不应把 time saving 或 screening accuracy 作为唯一贡献。Felizardo 等已经指出，LLM 辅助 SE SLR 的真正挑战在于 prompt 稳定性、输入边界、透明性、模型生命周期和缺少共享 SLR 数据仓库。paper2 如果能提供阶段化 evidence package、claim-to-source trace 和 failure taxonomy，就可以把这些困难转化为正面设计动机。

## 9. 可用于写作的引用角度

- 作为 SE 直接背景：WSESE@ICSE 2025 已明确讨论 LLM 辅助 SE SLR 的 conducting 与 replication difficulties，说明该问题已经进入 SE 方法学社区视野。
- 作为负面证据：已有 SE LLM-SLR 研究主要集中 title/abstract screening，且 prompt、随机性、输入信息、透明性、成本和模型可用性仍是开放问题。
- 作为 paper2 动机：可审计 run record、固定模型/提示词配置、人工审计 gate 和数据仓库式 evidence package 可被定位为回应这些可复制性困难的工程化方案。

## 10. 待复核清单

- 正式写作前核验 IEEE Xplore 页面、DOI、页码 20--23 和 WSESE@ICSE workshop 归属。
- 若使用 Study 1 / Study 2 的具体模型、参数、样本量和指标，需要回到原文 [9] / [10] 复核，而不是只引用本文转述。
- 若引用“GPT-4 成本”数字，必须按正式写作日期重新核验价格；本文价格是当时描述，不适合直接用作当前成本事实。
- 后续可把本文 10 个困难转写进 paper2 的 reviewer-risk table / experiment metric checklist。
