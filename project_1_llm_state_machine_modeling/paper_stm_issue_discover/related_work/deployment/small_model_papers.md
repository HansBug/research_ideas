# 小模型 + 方法学补偿：他们怎么把 story 讲圆的

> 本文件是 N1a 调研「小模型族」一路的产出。目标是回答：**用小模型 / 开源模型 / 本地模型 + 方法学设计来补偿模型能力不足的 SE 论文，是怎么处理「我比 SOTA 弱」这件事的。**
>
> ⛔ 本文件**不是** systematic review。检索是关键词驱动的机会性检索，覆盖有明显缺口，见 §5 与 §6。每条论文都标注了「读到什么程度」；标「仅摘要」的条目，其关于修辞策略的判断不可作为定论使用。

## 0. 一句话结论

这类论文**几乎从不用「我们更准」来立论**，而是把比较的坐标系整个换掉：**把「谁分高」换成「在什么约束下能达到什么」**——约束是单机、开源权重、数据不出域、无 API 调用；然后用三种手法处理残余差距（承认落后但绑定约束条件 / 换成非劣性而非优越性 / 把损失重述为取舍而非缺陷）。与此同时，一条对我们**非常有利**的证据链已经成立：**脚手架的收益随模型能力上升而单调衰减**——ICLR 2024 的 self-repair、TOSEM 2025 的 prompt engineering 再评估、FSE 2025 的 Agentless、以及 2026 年那篇本地模型 + 符号验证器的工作，四者从四个不同角度指向同一件事，其中最后一篇甚至直接给出了「同一套符号脚手架给最弱模型 +35、给最强模型 +3」的逐模型消融。⚠️ 但同一篇也给出了对我们最不利的那句话：**模型能力本身造成的差距（89 题）大于任何脚手架策略造成的差距。**

## 1. 逐篇表

「读到什么程度」口径：**全文** = 拿到完整正文并逐节读过；**部分正文** = 抓到并读了关键章节（结果表 / 动机段 / 威胁效度），未通读；**仅摘要** = 只读了 abstract / arXiv listing，正文未验证。

| 论文 | 年份 | venue | 用的什么模型 | motivation 主打 | 怎么处理「比 SOTA 弱」 | 有无 parity claim | 链接 | 读到什么程度 |
|---|---|---|---|---|---|---|---|---|
| Su & McMillan, *Distilled GPT for Source Code Summarization* | 2024 | Automated Software Engineering (Springer) 31(1):22 | jam 350M（自研，从 GPT-3.5 蒸馏）；对照 starcoder，规模扫 38M–15.5B | **隐私（数据保管权）为主**，可复现性为辅，成本第三 | **非劣性框架**：人评三维度「未观察到统计显著差异」；直接偏好 52% vs 46% 如实报出但称为 "slight preference" | **有**，但措辞是 "mimic" / "replicate"，不是 "outperform" | [arXiv:2308.14731](https://arxiv.org/abs/2308.14731) | 全文 |
| Pirzada, Parsert, Wang, Korovin, Cordeiro, *Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale*（系统名 VerIbmc） | 2026 | 无（arXiv preprint，无 venue 标注） | GPT-OSS-120B / GPT-OSS-20B / Qwen2.5-32B-Instruct / Qwen2.5-7B-Instruct / Llama-3.1-8B，本地 Ollama + 4×A6000；后端 ESBMC v8.2 | **隐私 + 可复现性 + 能耗/成本**三条并列，隐私打头 | **承认落后 + 立刻绑定约束**："competitive with – though slightly below – Clause2Inv (356) and LORIS (351)"，紧接着说那两个 "require state of the art expensive frontier models run on external servers"；再补一条覆盖面优势（对方前端只吃单循环标量整数程序） | **有，且是「约束下的 parity」**："competitive running only on a single local machine" | [arXiv:2606.16886](https://arxiv.org/abs/2606.16886) | 部分正文（引言、模型表、结果表、消融表） |
| Hasan, Islam, Khan, Senjik, Iqbal, *Automatic High-Level Test Case Generation using Large Language Models* | 2025 | MSR 2025 | LLaMA 3.1 8B + Mistral 7B（QLoRA 4-bit 微调）；对照 GPT-4o、Gemini | **保密 + 成本**，且是**问卷实证**出来的：46.2% 的受访者所在公司限制外部服务器工具（保密 34.6%、成本 11.6%） | 自动指标上赢（BERTScore F1 90.14 vs GPT-4o 88.43）；**人评上输**（correctness 4.15 vs 4.23，completeness 3.61 vs 3.91）→ **重述为取舍**："GPT-4o compromises dearly on relevance to achieve completeness … while LLaMA prioritizes relevance" | **有，且是 outperform**（自动指标口径） | [arXiv:2503.17998](https://arxiv.org/abs/2503.17998) | 全文 |
| Çelikmasat, Özgövde, Aydemir, *Instruction-Tuning Open-Weight Language Models for BPMN Model Generation*（方法名 InstruBPM） | 2025 | 无（arXiv preprint，标注 "under preparation for journal submission"） | Qwen3-4B-Instruct-2507 + LoRA/QLoRA + HQQ 量化；对照 GPT-5.1、Claude-4.5 Haiku/Sonnet、Gemini-2.5 Flash/Pro | **成本 + 隐私（on-prem 部署）** | **不需要处理——它全面赢**（BLEU 83.06 vs GPT-5.1 12.64；R-GED 99.44 vs 40.95）。⚠️ 但这个量级的差距主要来自**目标格式（DOT 约定）的一致性**，微调模型天然占便宜，这是它最大的可攻击面 | **有，强 claim** | [arXiv:2512.12063](https://arxiv.org/abs/2512.12063) | 全文 |
| Silva, Fang, Monperrus, *RepairLLaMA: Efficient Representations and Fine-Tuned Adapters for Program Repair* | 2025 | IEEE TSE（DOI 10.1109/TSE.2025.3581062） | CodeLlama-7B + LoRA adapter（4M 可训练参数，比底座小 1600×） | **效率/成本**（"does not scale to frontier models" 是它的问题陈述），隐私不是主打 | 它赢，无需处理："clearly outperforms non-fine-tuned baselines, incl. GPT-4" | **有** | [arXiv:2312.15698](https://arxiv.org/abs/2312.15698) | 仅摘要 ⚠️ |
| Wolfe et al., *Laboratory-Scale AI: Open-Weight Models are Competitive with ChatGPT Even in Low-Resource Settings* | 2024 | ACM FAccT 2024（DOI 10.1145/3630106.3658966）⚠️ 非 SE venue | 小开源权重模型（正文未在摘要页列名）vs GPT-4-Turbo，单张低价 GPU | **透明性 / 隐私 / 可适配性 / 证据标准**（面向 "under-resourced yet risk-intolerant" 的政府、科研、医疗） | **限定作用域**：parity 只声称在 "domain-adapted tasks" 上，并**明确让出** zero-shot SOTA 给闭源模型；再补三项闭源模型做不到的维度（bias / privacy / abstention） | **有，重度对冲**（"competitive"，不是 "better"） | [arXiv:2405.16820](https://arxiv.org/abs/2405.16820) | 仅摘要 ⚠️ |
| Lu, Yu, Li, Yang, Zuo, *LLaMA-Reviewer: Advancing Code Review Automation with LLMs through Parameter-Efficient Fine-Tuning* | 2023 | IEEE ISSRE 2023, pp. 647–658（DOI 10.1109/ISSRE59848.2023.00026） | LLaMA + PEFT（<1% 可训练参数） | **资源约束/成本**（避免从头预训练领域模型） | 与 CodeReviewer / AUGER 等**领域专用基线**比，而**不与 GPT-4 比**——即「干脆不跟 SOTA 比」这一策略的样本 | 无（不做与通用大模型的 parity claim） | [arXiv:2308.11148](https://arxiv.org/abs/2308.11148) | 仅摘要 ⚠️ |
| Jambigi, Bogacz, Mueller, Bach, Felderer, *Fault Localization via Fine-tuning LLMs with Mutation Generated Stack Traces* | 2025 | 无（arXiv preprint；提交者自述尚未取得所在机构发布许可） | 微调开源 LLM（具体型号/参数量**待核验**），工业对象为 SAP HANA | 摘要口径是**数据可得性**（生产崩溃只有 stack trace），不是隐私 | 报告微调模型胜过未微调 LLM；根因定位 66.9% vs 基线 12.6% / 10.6% | 未在摘要中出现 GPT-4o 对比 | [arXiv:2501.18005](https://arxiv.org/abs/2501.18005) | 仅摘要 ⚠️ |
| Belcak, Heinrich, Diao, Fu, Dong, Muralidharan, Lin, Molchanov (NVIDIA), *Small Language Models are the Future of Agentic AI* | 2025 | 无（arXiv position paper） | 立场论文，不做实验 | **经济性**为主，"sufficiently powerful, inherently more suitable, and necessarily more economical" | 不适用（不做效果比较），但给了一个可引的**框架句式**：agentic 场景里模型反复执行少数专门化任务，通用对话能力是多余的 | 不适用 | [arXiv:2506.02153](https://arxiv.org/abs/2506.02153) | 仅摘要 |

⚠️ 关于「读到什么程度」的自我约束：上表中标「仅摘要」的五条，**其「怎么处理比 SOTA 弱」一列的判断只应作为线索**，不得作为论文写作时的引用依据。硬性要求第 2 条要的是正文证据，这五条没有。

## 2. ⭐ 处理不利结果的策略分类（本调研对我们最有用的部分）

从上面读到正文的四篇里，可以抽出**五种彼此正交的手法**。它们可以叠用，实际上最成熟的那两篇（Su & McMillan、VerIbmc）都同时用了三种以上。

### 策略 A：非劣性替代优越性（把「谁更好」换成「有没有显著差异」）

**样本：Su & McMillan（Automated Software Engineering 2024）。**

这是最干净的一次执行。他们的 RQ3 问句本身就已经放弃了争胜：**"How closely does the distilled model mimic GPT-3.5 for code summarization, as measured by human experts?"**——问的是「模仿得多像」，不是「谁更好」。结果句同样：**"we do not observe a statistically-significant difference between the 350m parameter jam model and GPT-3.5 in terms of accuracy, completeness, or conciseness."**

关键在于他们**没有隐瞒不利数**：直接偏好投票是 52% GPT-3.5 / 46% jam / 2% 未决，白纸黑字写在 Discussion 里，措辞是 "a slight preference favoring GPT-3.5"。然后立刻用一句结论把它兜住：**"an inexpensive model such as 350m jam can replicate a very large model such as GPT-3.5 for the task of code summarization when provided sufficient examples."**

**对我们的可迁移性**：高。我们目前是 60.4% vs 76.2%，**差 15.82 个点，这不可能通过非劣性检验**。所以策略 A 单独用不了——除非我们能找到一个**分层的子集**，在该子集上差距落进噪声范围内（这需要先测代次内方差，见根 CLAUDE.md 「先测噪声底再谈效果」）。

### 策略 B：承认落后 + 立刻绑定约束条件（"competitive under X"）

**样本：VerIbmc（arXiv:2606.16886, 2026）。**

句式模板值得逐字记下来：

> "outperforms LaM4Inv (338), and is competitive with – though slightly below – Clause2Inv (356) and LORIS (351)"

紧跟着的下一句就是约束绑定：那两个更强的系统 **"require state of the art expensive frontier models run on external servers"**。再一次强调：**"competitive running only on a single local machine"**。

这个手法的要点是**差距的绝对值被留在原地不动，改变的是分母**——不是「我们只差 10 题」，而是「我们在单机、无外部调用的前提下差 10 题」。约束不是借口，是**新的比较维度**，因为对方在该维度上是 0 分（他们根本做不到本地运行）。

**它还叠了第三层**：覆盖面。两个赢它的 API 工具前端只接受单循环标量整数程序，所以在 SV-COMP 上可比子集缩到 43 题；VerIbmc 支持数组、指针、嵌套循环。**「你赢的那部分题目是你能做的全部，我输的那部分只是我能做的一小块」**——这是把「弱」重新描述为「宽」。

**对我们的可迁移性**：**最高**。我们完全可以说「私域部署 + 结构化可断言产出」这两条是朴素单提示 baseline 的 0 分维度。但⚠️ 要成立必须满足一个前提：**我们的 SOTA baseline 也得是云端的**。如果朴素单提示同样能在 Qwen-32B 上跑，那约束就不构成差异，这个策略立刻失效——所以**必须补一格实验：朴素单提示 + Qwen-32B**。这一格是整条 story 的生死线。

### 策略 C：把损失重述为取舍，而不是缺陷

**样本：Hasan et al.（MSR 2025）。**

他们的人评里微调 LLaMA 在 correctness（4.15 vs 4.23）和 completeness（3.61 vs 3.91）上都输给 GPT-4o。处理方式不是淡化，而是**给出一个机制解释，把两个指标绑成一对此消彼长的量**：

> "A negative correlation is observed between completeness and relevance: GPT-4o compromises dearly on relevance to achieve completeness, often including unnecessary details, while LLaMA prioritizes relevance, which might lead to incomplete scenario coverage."

于是「LLaMA 更不完整」就变成了「LLaMA 更不啰嗦」的同一件事的另一面。他们还配了一个有利数据点（relevance 上 LLaMA 4.02 略高于 GPT 3.98）来坐实这个对偶关系。

**对我们的可迁移性**：中等偏高，但**有学术风险**。取舍叙事只有在**两端都有真实数据**时才成立；如果我们只有「覆盖率低」而拿不出对应的「精确率高 / 多报少」，那这就是修辞而非发现。⛔ 按仓库 §3.5 的口径，无数据支撑的取舍叙事属于「评测口径迁就结果」。我们手上是否有多报侧的对照数据（`over@1` / `over@any`），决定这条能不能用。

### 策略 D：换评价维度（不比准确率，比别的）

**样本：Wolfe et al.（FAccT 2024）** 与 **NVIDIA 立场论文**。

Wolfe 等人明确让出 zero-shot SOTA 给闭源模型，把 parity 限定在 "domain-adapted tasks"，然后追加三个闭源模型结构性劣势的维度（bias、privacy、abstention）。NVIDIA 的立场论文则整段绕开效果比较，只论 "sufficiently powerful … and necessarily more economical"，把讨论锚在经济性上。

**对我们的可迁移性**：**这正是我们那句「附带可断言、可追溯的结构化产出」的所在位置。** 但要注意，换维度必须**换到一个能被测量的维度**上；「可追溯」如果没有对应的量化指标（例如：产出中可被自动核验的断言比例、每条发现能否定位到需求原句），就只是宣传语。⛔ 我们目前没有这个指标，需要先定义再测。

### 策略 E：干脆不跟通用 SOTA 比

**样本：LLaMA-Reviewer（ISSRE 2023）** 只与 CodeReviewer、AUGER 等领域专用基线比。

**对我们的可迁移性**：**低到不可用。** 2023 年这样做还行，2026 年审稿人一定会问「和 GPT-5.5 直接问一遍比呢」。而且我们已经**知道**答案是 76.2%——知情不报属于选择性报告。

### ⭐ 一个反面教训：不要把 parity 建在格式一致性上

InstruBPM（Qwen3-4B）在 BLEU 上 83.06 vs GPT-5.1 的 12.64，看起来是碾压。但这个量级几乎**必然**主要来自「微调模型学会了目标 DOT 书写约定」，而不是「它更懂业务流程」。他们自己也间接承认了这点：给未微调基线加上语法参考与示例后，基线分数**翻倍**（正文说不加这些的话 "untuned models performed substantially worse—approximately half the scores reported in Table 2"）。

**教训**：如果我们的方法输出的是结构化制品而 baseline 输出的是自由文本，任何基于形状的指标都会给我们不当加分。评审侧会看穿。**指标必须锚在语义命中上，不能锚在形式合规上。**

## 3. ⭐ 防稻草人的做法（他们怎么给大模型设计 prompt）

按「防守强度」从弱到强排列。

### 3.1 最弱：只交代 prompt 并把它列入威胁效度

**Su & McMillan** 给 GPT-3.5 的是一句极简 prompt：

> `Write a one sentence description of this Java method:`

后面直接跟方法源码，没有 few-shot、没有格式约束、没有角色设定。他们**没有辩称这是最优 prompt**，而是把它写进 Threats to Validity：

> "The GPT-3.5 version and prompt are threats to validity because GPT-3.5 is a commercial product and subject to change without notice, and also may give different answers with different prompts."

然后给了两条兜底：一是**降级 claim 的作用域**——"we view this paper as still valid as a framework for distilling knowledge from large models"（论文的贡献是蒸馏框架，不是某个具体分数）；二是**发布 GPT-3.5 的原始响应作为独立数据集**，让别人能复核。

⚠️ 这在 2024 年勉强够用，2026 年不够。但那个「降级 claim 作用域」的动作值得学：**当 baseline 配置可能被质疑时，把论文的主张从「我们更好」退到「我们提供了一个框架/一套证据」，质疑就打不到承重墙上。**

### 3.2 中等：给基线额外脚手架，并量化脚手架的贡献

**InstruBPM** 做得最明确。它给未微调基线（含 GPT-5.1、Claude-4.5、Gemini-2.5）的是**加强版 zero-shot**，逐字：

> "For untuned baselines, we use a strengthened zero-shot prompt to ensure fairness: rather than only requesting a BPMN model, the prompt includes syntax conventions and a small illustrative example."

而且**量化了这个加强的效果**："Without this scaffolding, baseline models produced incoherent or incomplete diagrams, and their evaluation scores dropped substantially"，正文另一处给了倍数：不加脚手架时基线约为表中分数的**一半**。

还有两条细节值得抄：
- **给闭源模型开推理模式**："Since all proprietary baselines support dedicated thinking modes, we evaluated them using their respective reasoning variants configured with a medium thinking-effort setting."
- **采样参数全模型统一**：temperature 0.1、top_p 1.0、max 2048 tokens，"held constant across all models and strategies to isolate the prompting effects"。

### 3.3 中等偏强：主动尝试强化基线并报告「强化无效」

**Hasan et al.（MSR 2025）** 做了两次强化基线的尝试，两次都报了负结果：

1. **加项目描述的增强 prompt**：GPT-4o 从 F1 88.01 变成 87.95（不升反降 0.06）。结论逐字："it is evident that the enhanced prompts do not make any significant difference in the performance of the models."
2. **加 RAG**：GPT-4o 88.01 → 88.49（+0.48），微调模型反而略降。解释是知识库中的用例-测试用例对跨项目相似度低，检索到的示例不够相关。

**这是最实用的防守形态**：不是声称「我们的 baseline 已经最优」，而是**展示「我们试图让它更强，它没变强，这里是数字」**。审稿人要求「你应该给大模型也加上你那套流水线」时，能拿出的最好回应就是「加过，附表 IX 和表 X」。

### 3.4 最强：完全不自己配置基线，全部引用官方最优数

**Agentless（FSE 2025 / PACMSE vol.2:801–824, DOI 10.1145/3715754；preprint [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)）** 用的是这一招，逐字：

> "For baseline tools, we directly use the reported results either from the official leaderboard or from the tool's official paper/repository."

26 个 agent 基线的分数全部来自各自作者或官方榜单自报的**最佳配置**，Agentless 团队没有动过任何超参、prompt 或工具定义。**没有可供调低的旋钮，指控就无从落脚。** 而且他们主动交代了这个做法的反向代价："the majority of the closed-source baselines do not provide any trajectories, just the submission patches. Therefore, we cannot verify the steps taken to arrive at the final patches."

补强还有第三方独立复算：OpenAI 独立在 SWE-bench Lite / SWE-bench / SWE-bench Verified 上评测了 Agentless 与其它开源方案，确认了结论。

⚠️ 但它有一处没有正面回应的质疑：**双方调优努力量不对等**。它拿基线的官方最优数去比自己**精心调过**的 pipeline（40 patches/bug、40 reproduction tests/issue、4 组 edit locations，并配了大量 ablation）。这不构成不公，但如果我们照抄这一招，要预判这个问题。

### 3.5 给我们的可执行清单

综合上面四档，一篇 2026 年的论文若要做 parity claim，**基线侧至少要交代**：

1. 精确 model id + 调用日期 + 采样参数，且**全模型统一**（InstruBPM 做法）。
2. 基线 prompt 的**完整原文**（附录或 artifact），并说明它为什么是这个形状。
3. **至少一次强化基线的尝试及其结果**——few-shot、结构化输出约束、推理模式、RAG 任选，报告 delta，哪怕是负的（MSR 2025 做法）。
4. **多次采样**而非单次，报告方差；这一点上面四篇里只有 TOSEM 那篇明确做了（每个实验跑三次取平均）。
5. 把 prompt 与版本列入 Threats to Validity（Su & McMillan 做法），并公开 raw output 供复核。

另有一份专门的报告规范可以直接引：**Korn, Zaruchas, Arora, Metzger, Smolka, Wang, Vogelsang, *Reporting LLM Prompting in Automated Software Engineering: A Guideline Based on Current Practices and Expectations*, FORGE 2026, [arXiv:2601.01954](https://arxiv.org/abs/2601.01954)**。它分析了三大 SE 会议自 2022 年以来约 300 篇论文的 prompt 报告实践，并调查了 105 位 PC 成员的期望，发现三处主要错位：**版本披露、prompt 论证、威胁效度**。⚠️ 我只读到摘要页，具体的 essential/desirable/exceptional 分级清单未读到，引用前需补读正文。

## 4. ⭐ 「复杂流水线在强模型上反而更差」的文献证据

**结论先行：有，而且证据链比预期强得多。** 四篇从四个不同角度指向同一个机制，其中两篇给了逐格数字。

### 4.1 最直接的一击：同一技术在强弱模型上符号反转（TOSEM 2025）

**Wang, Sun, Gong, Ye, Chen, Zhao, Liang, Hao, *Do Advanced Language Models Eliminate the Need for Prompt Engineering in Software Engineering?*, ACM TOSEM（DOI [10.1145/3771933](https://dl.acm.org/doi/10.1145/3771933)，Just Accepted 2025-10-16）；preprint [arXiv:2411.02093](https://arxiv.org/abs/2411.02093)。**

⚠️ 下列数字全部取自 **arXiv v1**（模型为 GPT-4o 与 o1-mini）。TOSEM 正式版把模型集扩到了 GPT-4o、Claude 3.5 Sonnet、o1，**对应数字待核验**；引用具体数值时应标明版本或回正式版复核。

**Critique（自我批判）prompting 在代码摘要任务上，GPT-4o 正收益、o1-mini 负收益——同一技术符号反转：**

| 技术 | Java GPT-4o | Java o1-mini | Python GPT-4o | Python o1-mini |
|---|---|---|---|---|
| Zero-shot | 4.14 | **4.23** | 3.71 | **4.12** |
| CoT | 4.26 | 3.98 | 4.31 | 4.09 |
| **Critique** | **4.42** | **3.76** | **4.46** | **3.71** |
| Expert | 4.44 | 3.98 | 4.26 | 4.04 |
| ASAP | 4.34 | 4.11 | 4.41 | 4.08 |

Critique 在 GPT-4o 上 Java +0.28、Python +0.75；同一个 Critique 在 o1-mini 上 Java **−0.47**、Python **−0.41**。而且不是孤例：**o1-mini 那两列里，5 个技术在两种语言上全部低于 zero-shot**。原文断言：

> "the basic zero-shot prompt not only competes with but typically **exceeds** the results of more complex prompt engineering strategies when using o1-mini."

代码翻译上更惨烈：S&G 在 o1-mini 的 Python→Java 上塌到 **0.099**，而 1-shot 是 **0.803**；UniTrans 在 GPT-4o 上是正收益（0.817 > 0.776），在 o1-mini 上变负（0.682 < 0.803）——又一次符号反转。

**token 成本这一侧同样有数**：最刺眼的一格是 o1-mini + UniTrans（Python→Java），994.69 message tokens + **9507.75 reasoning tokens**、**174.92 秒**，是 zero-shot（8.85s）的约 **19.8 倍**，而准确率**反而更低**。作者逐字：

> "the time cost relative to zero-shot prompting increases from 2.0 to **19.8 times, without any corresponding improvement in performance**."

> "this increased computational overhead **does not necessarily translate into better performance**, indicating that more complex prompts may inadvertently prolong reasoning, leading to greater costs without proportional benefits."

⭐ **对我们最有价值的一条是它的消融**：剥掉执行反馈与迭代（`-no-iter`）后，**AgentCoder 在 GPT-4o 上从 96.3 掉到 87.8，低于 zero-shot 的 90.4**。也就是说，AgentCoder 相对 zero-shot 的 +5.9 分**几乎全部来自真实执行反馈，而不是 multi-agent 的提示词结构**。原文：

> "the useful part of each approach's prompt is the **test execution information and the fix phase during the iteration** instead of the **formulation of prompts**."

**机制解释（四条，逐字）：**

1. 基线高度决定改进空间："the sophisticated built-in reasoning capabilities of o1-mini yield **diminishing returns** when further enhanced with prompt engineering, whereas **GPT-4o, with a lower baseline, benefits more significantly from the same techniques**."
2. 外部提示词干扰内建 CoT："Inputting all information simultaneously, without considering its relevance, can **disrupt the internal Chain-of-Thought logic**."
3. 无执行验证的补充信息会误导强模型："without execution feedback that can reflect the ground truth, the supplemental information extracted from the input may not enhance performance and can even hinder it."
4. **任务所需推理深度决定脚手架还有没有位置**：随机抽 300 例统计 o1-mini 的 CoT 步数——generation 3.52、translation 4.35、summarization 1.38；**CoT 步数 ≥ 5 的题目上 o1-mini 比 GPT-4o 好 16.67%，< 5 步的题目上只好 2.89%**。

⚠️ **三条不能越界**：(a) 「收益变负」集中在 summarization 与 translation，**code generation 上只是收窄不是变负**（AgentCoder/Self-collaboration/LDB 在 o1-mini 上仍为正）；(b) summarization 的指标是 **GPT 打分 1–5**，不是硬指标；(c) 它测的七个技术标签里**没有 self-consistency，也没有 Tree-of-Thoughts**。

### 4.2 成本归一化后自我修复的收益消失（ICLR 2024）

**Olausson, Inala, Wang, Gao, Solar-Lezama, *Is Self-Repair a Silver Bullet for Code Generation?*, ICLR 2024，[arXiv:2306.09896](https://arxiv.org/abs/2306.09896)（v5, 2024-02-02，comments 字段标明 "Accepted to ICLR 2024"）。**

在 Code Llama、GPT-3.5、GPT-4 上评测 HumanEval 与 APPS 的自我修复。核心结论（摘要逐字）：把修复的代价计入之后，**"performance gains are often modest, vary a lot between subsets of the data, and are sometimes not present at all."**

机制解释直指要害：**"bottlenecked by the model's ability to provide feedback on its own code"**——把反馈换成更强模型产生的反馈后，收益显著变大；小规模人类反馈实验进一步说明即便最强模型也远不及人类水平的调试。

⭐ **这一条对我们的意义**：我们的 loop 吃掉 79% 的 token 而覆盖率净变化约等于零，与这篇的诊断**完全同形**。它给了我们一个现成的、可引的因果解释：**自我批判的上限是模型自评的质量，而不是循环的次数或结构。** 同时它也给了下一步的方向——**把自评换成外部可验证信号**（这与 §4.1 的 `-no-iter` 消融是同一结论的两次独立观测）。

⚠️ 读到程度：摘要 + 检索摘要（含 pass@t、1.05×、10%/3%、1.58× 等数字）。**arXiv 摘要页未确认 1.58× 与 pass@t 的具体表述**，正文未通读，这几个数字标为**待核验**。

### 4.3 同模型下复杂 agent 既更差又更贵（FSE 2025）

**Xia, Deng, Dunn, Zhang, *Agentless: Demystifying LLM-based Software Engineering Agents*；正式版 *Demystifying LLM-Based Software Engineering Agents*, Proc. ACM Softw. Eng. (PACMSE) vol. 2 (2025) 801–824, DOI [10.1145/3715754](https://doi.org/10.1145/3715754)（= FSE 2025）；preprint [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)。**

SWE-bench Lite 上、**同一个 GPT-4o**：

| Tool | LLM | % Resolved | Avg. $ | Avg. tokens |
|---|---|---|---|---|
| **Agentless** | GPT-4o | **32.00%** | **$0.70** | **78,166** |
| SWE-agent | GPT-4o | 18.33% | $2.53 | 498,346 |
| AutoCodeRover | GPT-4 | 19.00% | $0.45 | 38,663 |
| Moatless | GPT-4o | 24.67% | $0.14 | – |

高 **13.67 个百分点**，成本 **1/3.6**，token **1/6.4**。SWE-bench Verified 复现同一格局（Agentless 38.80% vs SWE-agent GPT-4o 23.20%）。

它对复杂度的三条机制批判（皆逐字）：工具设计易出错且"incur additional cost in wasted LLM queries"；决策不可控，"an agent can take upwards of 30 or 40 turns, which makes it extremely difficult to both understand the decisions made by the agents and also debug"；自反思能力有限，"an **incorrect step can be easily amplified** and negatively affect all future decisions"。

⚠️ **两条必须一起引的限定**：(a) 它**不是榜首**（CodeStory Aide 43.00%、Bytedance MarsCode 39.33% 都更高），"highest performance" 只在 **open-source** 范围内成立；(b) 它**不是最便宜**（Moatless $0.14），原文措辞是 "less than **most** prior agent-based approaches"。另外它**只用了 GPT-4o 一个模型**，**没有模型强度这一维的对照**——所以它支撑的是「同模型下 agent 不如流水线」，**支撑不了**「强模型上 agent 才失效」。后者只有 §4.1 能撑。

### 4.4 ⭐ 逐模型消融：同一套符号脚手架，给最弱模型 +35、给最强模型 +3（2026）

**VerIbmc（[arXiv:2606.16886](https://arxiv.org/abs/2606.16886)）** 在这一点上给了本调研里**最贴合我们处境的一张表**。它对同一套三阶段流水线做 Basic（完整流水线）vs LLM-Only（跳过符号先验）的对照：

| Model | Basic | LLM-Only | Δ |
|---|---|---|---|
| Llama-3.1-8B | 342 | 307 | **+35** |
| Qwen2.5-7B | 352 | 328 | +24 |
| GPT-OSS-20B | 424 | 409 | +15 |
| Qwen2.5-32B | 382 | 380 | **+2** |
| GPT-OSS-120B | 431 | 428 | **+3** |

另有一张 Phase-1（符号枚举，可独立解 75 题）净贡献表：Llama-3.1-8B **+36**、Qwen2.5-7B +22、GPT-OSS-20B +15、**GPT-OSS-120B 0**——最强模型净收益为零，原因是它 "independently derives the same provable atoms"（自己就能推出同样的可证原子）。

**这是「脚手架收益随模型能力单调衰减」最干净的一次直接测量**，而且是在**形式化验证**这个与我们高度同构的任务上。

⚠️ **但同一篇给了对我们最不利的那句话**：作者的结论是**模型能力占主导**——最强到最弱的差距是 **89 题，大于任何策略造成的差距**（最大 +35）。另外 Llama 的 342 取自三次运行的最好一次（均值 336.0，σ=5.3），所以 +35 落在采样方差的乐观端。

**推论（这是我们必须自己面对的算术）**：如果我们的方法在 Qwen-32B 上的增益是 Δ，而 Qwen-32B 与云端 SOTA 的裸能力差是 G，那么 story 成立的必要条件是 **Δ ≳ G**。VerIbmc 的数据说在它那个任务上 Δ_max ≈ 35 而 G ≈ 89，**它做不到，所以它老老实实用了策略 B（承认落后 + 绑定约束）而不是宣称打平。** 我们在动笔之前应当先把自己的 Δ 和 G 量出来，再决定讲哪一种 story。

### 4.5 补充：多智能体相对单智能体的优势随模型变强而缩小

**Gao, Li, Liu, Yu, Wang, Lin, Lai, *Single-agent or Multi-agent Systems? Why Not Both?*, [arXiv:2505.18286](https://arxiv.org/abs/2505.18286)（2025-05-23，无 venue）。** 摘要逐字：**"the benefits of MAS over SAS diminish as LLM capabilities improve"**，理由是前沿模型（点名 OpenAI-o3、Gemini-2.5-Pro）在长上下文推理、记忆与工具使用上的进步，侵蚀了 MAS 最初的立论基础。他们据此提出请求级联的混合范式，报称准确率 +1.1–12%、部署成本 −20%。⚠️ 仅摘要，任务级与逐模型数字未读到。

### 4.6 这条证据链怎么用

四篇合起来给出的**共识机制**是：**在强模型上，结构复杂度本身不产生收益；收益来自可验证的外部信号。** Agentless 的 Table 4（majority voting 77 → +regression test 81 → +reproduction test 96）与 TOSEM 的 `-no-iter` 消融（AgentCoder GPT-4o 96.3 → 87.8）是这一点的两次独立佐证；Olausson 从反面说明了当外部信号缺席、只能靠自评时，收益为什么消失。

⭐ **对我们的直接含义**：我们那句「loop 吃掉 79% token 而覆盖率净变化约等于零」**不是我们方法的丑闻，而是一个已被文献反复确认的现象**——但**前提是我们的 loop 里没有可验证的外部信号**。如果我们的 loop 已经接了外部验证器（如 pyfcstm 的 parse/semantic 诊断）而仍然无收益，那就落在文献解释之外，需要另找根因，不能直接引这几篇挡枪。这一点必须先自查清楚再写。

## 5. 检索过程

**时间**：2026-08-13。**工具**：WebSearch + WebFetch（arXiv abs / HTML）；PDF 走 `python -m tools.pdf_extractor -m text` 本地提取后逐段读。

**检索式（按发起顺序，含命中情况）**：

| # | 关键词 | 有效命中 |
|---|---|---|
| 1 | small open-source LLM matches GPT-4 software engineering fine-tuning pipeline ICSE 2025 | 0 直接命中；引出 AwesomeLLM4SE 索引与 Su & McMillan 线索 |
| 2 | open-source LLM privacy on-premise GPT-4 comparable requirements engineering | 0 SE 命中（结果偏向通用 open vs proprietary 对比与医疗领域） |
| 3 | agentless simple pipeline outperforms complex agent LLM SE | 1（Agentless） |
| 4 | small language models SE empirical 7B match GPT-4 | 1 弱命中（Assessing SLMs for Code Generation，arXiv:2507.03160，明确未测 GPT-4，未纳入） |
| 5 | advanced prompting CoT self-refine do not improve stronger models negative result | 2（TOSEM 2411.02093；CodePromptEval 2412.20545 未深读） |
| 6 | RepairLLaMA fine-tuned LLaMA program repair outperforms GPT-4 | 1（RepairLLaMA） |
| 7 | Distilled GPT for source code summarization Su McMillan | 1（jam-cgpt，本调研最有用的样本之一） |
| 8 | LLaMA-Reviewer PEFT code review ISSRE 2023 | 1 |
| 9 | Small Language Models are the Future of Agentic AI | 1（NVIDIA 立场论文） |
| 10 | Qwen open-weight requirements/UML state machine local deployment MODELS | 0 直接命中；引出 InstruBPM（BPMN） |
| 11 | structured output / constrained decoding compensates small model capability gap | 若干 2026 年 arXiv 条目，**均未核验**，仅作线索 |
| 12 | fine-tuned small model unit test generation / fault localization beats GPT-4 privacy | 2（MSR 2025 高层测试用例；SAP HANA 故障定位） |
| 13 | LLM formal specification / model checking open small model verifier feedback loop | 1（VerIbmc，本调研与我们最同构的样本） |
| 14 | SE LLM weak baselines straw man unfair comparison | 0 直接命中；引出 FORGE 2026 prompt 报告规范 |
| 15 | self-repair silver bullet cost analysis | 1（Olausson et al. ICLR 2024） |
| 16 | industrial open-weight LLM static analysis cannot send code self-hosted | 弱命中，多为 2026 年 arXiv 条目，**未核验** |
| 17 | multi-agent vs single agent no significant improvement cost overhead | 1（arXiv:2505.18286） |
| 18 | open-weight small LLM comparable to GPT-5 scaffolding ICSE 2026 | 0 |

**venue 覆盖情况**：实际读到正文的四篇分别落在 **Automated Software Engineering 期刊（Springer）**、**MSR 2025**、以及**两篇无 venue 的 arXiv preprint**。此外通过子调研读到正文的两篇落在 **FSE 2025（PACMSE）** 与 **ACM TOSEM**。**ICSE、ASE 会议、ISSTA、TSE、EMSE、MODELS、RE、SANER 没有一篇是读到正文的**——TSE 只有 RepairLLaMA 一条且仅摘要，其余 venue 零命中。

**语料规模**：18 条检索式，浏览标题/摘要级候选约 130 条，进入本文件的 15 篇左右，**读到正文的 6 篇**。

## 6. 覆盖边界与待核验项

### 6.1 覆盖边界（诚实交代）

1. ⛔ **这不是 systematic review。** 没有预注册检索协议、没有 PRISMA 流程、没有双人筛选、没有覆盖 ACM DL / IEEE Xplore / Scopus 的系统检索。检索完全是关键词驱动的机会性检索，命中受搜索引擎排序影响很大。
2. ⛔ **CCF A/B 会议的正文覆盖近乎空白。** ICSE / ASE / ISSTA / MODELS / RE / SANER 的会议论文一篇正文都没读到。这是最大的缺口——很可能有大量相关工作躺在这些会议的 program 里而搜索没有召回。**下一步应当直接翻 conf.researchr.org 的 ICSE 2025/2026、FSE 2025、ASE 2025 accepted papers 列表，而不是继续用关键词搜。**
3. ⛔ **「小模型 + 方法学补偿」这个精确形态的 SE 论文，样本量很小。** 大量命中其实是「小模型 + 微调」（RepairLLaMA、LLaMA-Reviewer、MSR 2025、InstruBPM），而**不是**「小模型 + 推理时流水线补偿」。真正与我们同构（不微调，靠推理时的多阶段结构补偿）的只有 **VerIbmc 一篇**。这本身是个信号：**要么这个 niche 确实空着（对我们是机会），要么它被证明不 work 所以没人发（对我们是警告）。** 目前的证据（§4.4 那张表）两种解读都支持，需要更多样本才能分辨。
4. ⛔ **中文 / 非英文文献、工业界白皮书、工具报告完全未覆盖。**
5. ⛔ **时间窗**：主要覆盖 2023-06 至 2026-06。2026 年上半年的 arXiv 条目很多只有摘要级验证。

### 6.2 待核验项（按优先级）

| # | 事项 | 为什么重要 | 怎么核 |
|---|---|---|---|
| 1 | **TOSEM 正式版（DOI 10.1145/3771933）的模型集与数字** | §4.1 全部数字取自 arXiv v1（GPT-4o + o1-mini）；正式版扩到了 Claude 3.5 Sonnet 与 o1，Critique 的符号反转在正式版是否仍然成立**未知**。这是我们最想引的一条 | ACM DL 对自动抓取返回 403，需人工下载 PDF |
| 2 | **Olausson et al. 的 pass@t 定义与 1.58× 人类反馈实验** | §4.2 这两个数字来自检索摘要而非正文 | 读 [ICLR 2024 proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/9ddc141bdbf9d1db510cefff56c586ad-Paper-Conference.pdf) |
| 3 | **RepairLLaMA 正文里 GPT-4 baseline 的 prompt 配置** | 它是 parity claim 的重要样本，但我只读到摘要，不知道它给 GPT-4 的是什么 prompt、几次采样 | 读 [arXiv HTML](https://arxiv.org/html/2312.15698v1) 或 TSE 正式版 |
| 4 | **Wolfe et al.（FAccT 2024）用的具体开源模型型号** | 摘要页未列名 | 读正文 |
| 5 | **Jambigi et al. 的模型型号 + 「GPT-4o 在混淆 stack trace 上 0% 准确率」这个实验是否真实存在** | 检索摘要提到它，但 arXiv abs 页**没有**这段。若真实，它是隐私动机最有力的一条证据（说明「混淆后再发给云端」这条退路走不通） | 读 [arXiv HTML v3](https://arxiv.org/html/2501.18005v3) |
| 6 | **VerIbmc 的 venue** | arXiv 页无 venue 标注，2026-06 提交，可能在投 | 查 DBLP / 作者主页 |
| 7 | **InstruBPM 的 venue 与同行评审状态** | 标注 "under preparation for journal submission"，即**未经同行评审** | 引用时必须标明是 preprint |
| 8 | **FORGE 2026 prompt 报告规范的 essential/desirable/exceptional 清单** | §3.5 想直接引它的清单，但只读到摘要 | 读 [arXiv HTML](https://arxiv.org/abs/2601.01954) 正文 |
| 9 | **§5 检索式 11 与 16 引出的 2026 年 arXiv 条目**（结构化输出补偿小模型、本地 LLM 缺陷检测等） | 一条都没核验，标题与结论均来自搜索摘要 | 逐条回 arXiv 核对是否存在、ID 是否正确 |
| 10 | **Agentless 的 FSE 2025 归属** | 经 DBLP API 核验为 PACMSE vol.2 (2025) 801–824，DOI 10.1145/3715754；PACMSE vol.2 即 FSE 2025 论文载体。⚠️ arXiv v2 的数字与 FSE 正式版可能有差异 | 若要引具体数字，用正式版复核 |

### 6.3 未收获的方向（记录下来避免重复劳动）

1. **RE / MODELS 会议 + 开源小模型 + 需求/状态机建模**：多次检索零命中。最接近的是 InstruBPM（BPMN，preprint）与 Ferrari/Abualhaija/Arora 的 MODRE 2024 requirements-to-UML（**未核验**，仅在搜索摘要中出现）。
2. **「SE 论文明确批评弱基线 / 稻草人」这一体裁**：没找到。FORGE 2026 那篇 prompt 报告规范是最接近的替代品，但它谈的是报告透明度，不是基线强度。
3. **明确用「非劣性检验」（non-inferiority test）这一统计框架的 SE 论文**：没找到。Su & McMillan 是「未发现显著差异」而不是正式的非劣性设计——⚠️ 两者不等价，**「未拒绝原假设」不等于「证明了等价」**，这是审稿人会挑的点。如果我们要走这条路，应当用正式的等价性/非劣性检验（TOST 之类）并预先声明边界值 δ。
