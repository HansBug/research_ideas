# 小模型 + 方法学补偿：他们怎么把 story 讲圆的

> 本文件是 N1a 调研「小模型族」一路的产出。目标是回答：**用小模型 / 开源模型 / 本地模型 + 方法学设计来补偿模型能力不足的 SE 论文，是怎么处理「我比 SOTA 弱」这件事的。**
>
> ⛔ 本文件**不是** systematic review。检索是关键词驱动的机会性检索，覆盖有明显缺口，见 §5 与 §6。每条论文都标注了「读到什么程度」；标「仅摘要」的条目，其关于修辞策略的判断不可作为定论使用。

## 0. 一句话结论

**这类论文几乎没有一篇真的把小模型和云端 SOTA 放进同一条流水线里公平比过一次**——主流做法是让对照本身在逻辑上变得不必要（「前人用了云模型，所以没解决隐私场景，所以存在缺口」），然后换一个自己必赢的分母（跟微调前的自己比、跟 zero-shot 的自己比、跟同族更弱的开源模型比）。真正做了正面对比的只有 SANER 2025 那一篇，而它的「打平」完全建立在**一个指标上的 Mann-Whitney U 检验不显著**，在它真正输的指标上（EM 16.70 vs 8.94，约一半）它坦承并归因于 25 倍参数差——**这个下限在 CCF B 过审了**，说明社区当前可接受的门槛就在这里。

同时，一条对我们**非常有利**的证据链已经成立：**脚手架的收益随模型能力上升而单调衰减**。ICLR 2024 的 self-repair、TOSEM 2025 的 prompt engineering 再评估、FSE 2025 的 Agentless、2026 年那篇本地模型 + 符号验证器的工作（直接给出「同一套符号脚手架给最弱模型 +35、给最强模型 +3」的逐模型消融），以及 2026 年单测生成上「朴素提示胜过四条带执行反馈的流水线、而调用量只有一半」的复现研究，从五个角度指向同一件事。

⭐⭐ **其中最重要的一条：有一篇论文的任务域与 project_1 完全相同**——[arXiv:2604.00275](https://arxiv.org/abs/2604.00275)（McGill，2026-03）做 NL → UML 状态机生成，发现**朴素单提示基线在较强模型上（Claude 3.5 Sonnet, $F_1$ 0.7029）打败了它自己所有的多阶段框架（0.3052–0.6336）**，而在较弱模型上（GPT-4o）多阶段框架反而更好。**同任务域、同现象、同方向。** 它既是我们「不是我们做错了什么」的最强外部佐证，也直接构成一个我们必须回应的先例。⚠️ 它同时警示了两件事：它自己也承认「多步流水线更差」里有一部分是**自家的严格后处理门误伤了合法输出**（正是根 CLAUDE.md §11 那条纪律的外部案例）——**我们必须先排除这一项再下结论**；而且它只有 8 个本科课程样本。

⚠️ 最不利的一句话来自本地模型 + 符号验证器那篇：**模型裸能力造成的差距（89 题）大于任何脚手架策略造成的差距（最大 35 题）。** 我们动笔前必须先把自己的 Δ（方法增益）和 G（Qwen-32B 与云端 SOTA 的裸能力差）量出来，再决定讲哪一种 story。

## 1. 逐篇表

⚠️ 本表只收「小模型 / 开源模型 + 方法学补偿」这一类；§4 涉及的负面结果文献（Abdulkarim、Wang/TOSEM、Konstantinou、Olausson、Agentless、Sepidband、Gao、Steenhoek、Li）不在本表内，其完整 bibliographic 信息写在 §4 各小节里。

「读到什么程度」口径：**全文** = 拿到完整正文并逐节读过；**部分正文** = 抓到并读了关键章节（结果表 / 动机段 / 威胁效度），未通读；**仅摘要** = 只读了 abstract / arXiv listing，正文未验证。

| 论文 | 年份 | venue | 用的什么模型 | motivation 主打 | 怎么处理「比 SOTA 弱」 | 有无 parity claim | 链接 | 读到什么程度 |
|---|---|---|---|---|---|---|---|---|
| Caumartin, Qin, Chatragadda, Panjrolia, Li, Costa, *Exploring the Potential of Llama Models in Automated Code Refinement: A Replication Study* | 2025 | **IEEE SANER 2025**, pp. 681–692（CCF B） | CodeLlama-Instruct 7B、Llama 2 7B（GGUF 4-bit，跑在 Mac Mini M1/16GB 与 RTX 3050 4GB 笔记本上）；附加 Llama 3.1-8B | **隐私为首**，其次可控性（闭源模型隐式版本漂移）、成本 | ⭐ **换指标 + 用「统计不显著」定义打平**：EM 上输一半（16.70 vs 8.94）时坦承并归因于 25× 参数差；BLEU-T 上做 Mann-Whitney U 检验、95% 置信下无显著差异，据此宣称 comparable。再叠「只在纯代码变更子任务上表现 reasonable」 | **有，但限定词写进句子**："often comparable to ChatGPT … **as measured by BLEU-T scores**" | [arXiv:2412.02789](https://arxiv.org/abs/2412.02789) · [DOI](https://doi.org/10.1109/SANER64311.2025.00070) | 全文 |
| Su & McMillan, *Distilled GPT for Source Code Summarization* | 2024 | Automated Software Engineering (Springer) 31(1):22 | jam 350M（自研，从 GPT-3.5 蒸馏）；对照 starcoder，规模扫 38M–15.5B | **隐私（数据保管权）为主**，可复现性为辅，成本第三 | ⭐ **非劣性框架**：人评三维度「未观察到统计显著差异」；直接偏好 52% vs 46% 如实报出但称为 "slight preference" | **有**，措辞是 "mimic" / "replicate"，不是 "outperform" | [arXiv:2308.14731](https://arxiv.org/abs/2308.14731) | 全文 |
| Pirzada, Parsert, Wang, Korovin, Cordeiro, *Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale*（系统名 VerIbmc） | 2026 | 无（arXiv preprint，无 venue 标注） | GPT-OSS-120B / GPT-OSS-20B / Qwen2.5-32B / Qwen2.5-7B / Llama-3.1-8B，本地 Ollama + 4×A6000；后端 ESBMC v8.2 | **隐私 + 可复现性 + 能耗/成本**三条并列，隐私打头 | ⭐ **承认落后 + 立刻绑定约束**："competitive with – though slightly below – Clause2Inv (356) and LORIS (351)"，紧接着指出那两个 "require state of the art expensive frontier models run on external servers"；再补覆盖面优势 | **有，是「约束下的 parity」**："competitive running only on a single local machine" | [arXiv:2606.16886](https://arxiv.org/abs/2606.16886) | 部分正文（引言、模型表、结果表、消融表） |
| Hasan, Islam, Khan, Senjik, Iqbal, *Automatic High-Level Test Case Generation using Large Language Models* | 2025 | **MSR 2025**（CCF B） | LLaMA 3.1 8B + Mistral 7B（QLoRA 4-bit 微调）；对照 GPT-4o、Gemini | **保密 + 成本**，且是**问卷实证**：46.2% 受访者所在公司限制外部服务器工具（保密 34.6%、成本 11.6%） | 自动指标赢（BERTScore F1 90.14 vs 88.43）；**人评输**（correctness 4.15 vs 4.23，completeness 3.61 vs 3.91）→ **重述为取舍**（completeness 与 relevance 负相关） | **有，outperform**（自动指标口径） | [arXiv:2503.17998](https://arxiv.org/abs/2503.17998) | 全文 |
| Tai, Nie, Golab, Wong, *NL in the Middle: Code Translation with LLMs and Intermediate Representations* | 2025 | 无（arXiv preprint，dblp 记 CoRR；是否被接收**待核验**） | Open Gpt4 8X7B（HuggingFace 开源 MoE，**不是** OpenAI GPT-4）、StarCoder、CodeGen | 主线是 prompt 工程；**隐私只在 §V-B Limitations 里作为模型选型的事后辩护** | ⭐ **限定场景反将一军**（本批最凝练的模板段）：承认 GPT-4 显著更好 → 宣布对方赛道不是企业真实赛道 → 把贡献重定义为「在可部署模型上的相对提升」 | **明确没有**，并明说打不平 | [arXiv:2507.08627](https://arxiv.org/abs/2507.08627) | 全文 |
| Kumar & Chimalakonda, *Code Review Automation Via Multi-task Federated LLM — An Empirical Study* | 2024 | 无（arXiv preprint；是否发表**待核验**） | LLaMA-3 8B + LoRA 联邦微调（可训练参数 0.016%–0.104%） | **隐私（专有代码不能出企业）**，且直接决定选型："**we avoided using any closed-source models**" | ⭐ **坦承 + 一句话用隐私正当化**："the central model performs better … **However, we choose FL because it offers privacy**"，并提前把差距定义为已知 trade-off。同时**把被牺牲的那一侧（集中训练上界）真的跑了并报数** | **没有**，原则性回避与闭源模型比较 | [arXiv:2412.15676](https://arxiv.org/abs/2412.15676) | 全文 |
| Sirin, Sami, Granlund, Rasku, Zhang, Abrahamsson, *Enhancing Regulation-Adherent Requirement Engineering with Contextual AI: An Industrial Study* | 2025 | PROFES 2025, LNCS 16362, pp. 69–85（industry/workshop 分册，**非主会 research track**；CCF 未列级） | Llama 3.2 3B、Qwen 2.5 14B、Mistral Small 3 24B、DeepSeek-R1-Distill-Qwen 32B、Llama 3.3 70B，全部 Ollama 本地；真实医疗器械需求数据 | **隐私 / 法规合规**，唯一主打，摘要第一段即是 | ⭐ **干脆不比，并把「不比」包装成研究缺口**：Related Work 点名前人用 GPT-4 的工作，一句 "their approach overlooks data privacy concerns due to the use of cloud-based models" 判其不适用。内部基线是人写的需求（SBERT 余弦 0.446–0.632），无阈值，改用「需 RE 专家密切监督」的定性说法 | **没有**，claim 是「可行性」不是「平手」 | [Springer](https://link.springer.com/chapter/10.1007/978-3-032-12092-2_5) · [同题硕士论文全文](https://trepo.tuni.fi/bitstream/handle/10024/228218/SirinAzizOrhan.pdf?sequence=2&isAllowed=y) | 会议版仅摘要（付费墙）；**同题硕士论文全文已读** ⚠️ 数字可能有出入 |
| Çelikmasat, Özgövde, Aydemir, *Instruction-Tuning Open-Weight Language Models for BPMN Model Generation*（InstruBPM） | 2025 | 无（arXiv preprint，"under preparation for journal submission"，**未经同行评审**） | Qwen3-4B-Instruct-2507 + LoRA + HQQ 量化；对照 GPT-5.1、Claude-4.5 Haiku/Sonnet、Gemini-2.5 Flash/Pro | **成本 + 隐私（on-prem）** | **不需要处理——它全面赢**（BLEU 83.06 vs GPT-5.1 12.64；R-GED 99.44 vs 40.95）。⚠️ 这个量级主要来自**目标格式（DOT 约定）一致性**，是它最大的可攻击面 | **有，强 claim** | [arXiv:2512.12063](https://arxiv.org/abs/2512.12063) | 全文 |
| Silva, Fang, Monperrus, *RepairLLaMA: Efficient Representations and Fine-Tuned Adapters for Program Repair* | 2025 | **IEEE TSE**（DOI 10.1109/TSE.2025.3581062，CCF A） | CodeLlama-7B + LoRA adapter（4M 可训练参数，比底座小 1600×） | **效率/成本**（"does not scale to frontier models"），隐私不是主打 | 它赢，无需处理："clearly outperforms non-fine-tuned baselines, incl. GPT-4" | **有** | [arXiv:2312.15698](https://arxiv.org/abs/2312.15698) | 仅摘要 ⚠️ |
| Bappy, Mustafa, Saha, Salehat, *Case Study: Fine-tuning Small Language Models for Accurate and Private CWE Detection in Python Code* | 2025 | 无（arXiv preprint，cs.CR） | codegen-mono **350M**，指令微调；训练数据由 gemini-2.0-flash 合成 500 条；推理在**无 GPU 的 i5-13500** 上 | **隐私 / 数据治理合规**（金融、医疗、政府） | ⭐ **最激进的回避**：连一次 GPT-4 实验都没做，基线是未微调的自己（0% → 99%），并把「跟 SOTA 比」整体推给 future work | 有隐含 claim（"comparable to or exceeding more resource-intensive methods"）但**零实验支撑** | [arXiv:2504.16584](https://arxiv.org/abs/2504.16584) | 全文 ⚠️ **质量提示**：非 CCF venue，测试集仅 100 条**合成**样本，报 99% accuracy——**只当修辞语料，不当性能证据** |
| Wolfe et al., *Laboratory-Scale AI: Open-Weight Models are Competitive with ChatGPT Even in Low-Resource Settings* | 2024 | ACM FAccT 2024（DOI 10.1145/3630106.3658966）⚠️ 非 SE venue | 小开源权重模型（摘要页未列名）vs GPT-4-Turbo，单张低价 GPU | **透明性 / 隐私 / 可适配性 / 证据标准**（面向 "under-resourced yet risk-intolerant" 的政府、科研、医疗） | **限定作用域**：parity 只在 "domain-adapted tasks" 上，**明确让出** zero-shot SOTA 给闭源；再补三项闭源做不到的维度（bias / privacy / abstention） | **有，重度对冲**（"competitive"，非 "better"） | [arXiv:2405.16820](https://arxiv.org/abs/2405.16820) | 仅摘要 ⚠️ |
| Lu, Yu, Li, Yang, Zuo, *LLaMA-Reviewer* | 2023 | IEEE ISSRE 2023, pp. 647–658（CCF B） | LLaMA + PEFT（<1% 可训练参数） | **资源约束/成本** | 只与 CodeReviewer / AUGER 等**领域专用基线**比，不与 GPT-4 比 | 无 | [arXiv:2308.11148](https://arxiv.org/abs/2308.11148) | 仅摘要 ⚠️ |
| Jambigi, Bogacz, Mueller, Bach, Felderer, *Fault Localization via Fine-tuning LLMs with Mutation Generated Stack Traces* | 2025 | 无（arXiv preprint；提交者自述尚未取得机构发布许可） | 微调开源 LLM（型号/参数量**待核验**），工业对象 SAP HANA | 摘要口径是**数据可得性**（生产崩溃只有 stack trace），不是隐私 | 根因定位 66.9% vs 基线 12.6% / 10.6% | 摘要中无 GPT-4o 对比 | [arXiv:2501.18005](https://arxiv.org/abs/2501.18005) | 仅摘要 ⚠️ |
| Belcak et al. (NVIDIA), *Small Language Models are the Future of Agentic AI* | 2025 | 无（arXiv position paper） | 立场论文，不做实验 | **经济性**："sufficiently powerful, inherently more suitable, and necessarily more economical" | 不适用；但提供了可引框架句：agentic 场景中模型反复执行少数专门化任务，通用对话能力是多余的 | 不适用 | [arXiv:2506.02153](https://arxiv.org/abs/2506.02153) | 仅摘要 |

⚠️ **关于「读到什么程度」的自我约束**：上表中标「仅摘要」的四条（RepairLLaMA、Laboratory-Scale AI、LLaMA-Reviewer、SAP HANA 故障定位），其「怎么处理比 SOTA 弱」一列的判断**只应作为线索**，不得作为论文写作时的引用依据。任务的硬性要求第 2 条要的是正文证据，这四条没有。

## 2. ⭐ 处理不利结果的策略分类（本调研对我们最有用的部分）

从读到正文的九篇里抽出**六种彼此正交的手法**。成熟的样本都叠用三种以上。按「对我们的可用性」而非出现频率排序。

### 策略 A：承认落后 + 立刻绑定约束条件（"competitive under X"）

**样本：VerIbmc（arXiv:2606.16886, 2026）、Tai et al.（arXiv:2507.08627, 2025）。**

VerIbmc 的句式模板值得逐字记下：

> "outperforms LaM4Inv (338), and is competitive with – though slightly below – Clause2Inv (356) and LORIS (351)"

紧跟着的下一句就是约束绑定：那两个更强的系统 **"require state of the art expensive frontier models run on external servers"**；再强调 **"competitive running only on a single local machine"**。要点是**差距的绝对值留在原地不动，改变的是分母**——不是「我们只差 10 题」，而是「我们在单机、无外部调用的前提下差 10 题」。约束不是借口，是**新的比较维度**，因为对方在该维度上是 0 分。它还叠了第三层：两个赢它的 API 工具前端只吃单循环标量整数程序（SV-COMP 可比子集缩到 43 题），而 VerIbmc 支持数组、指针、嵌套循环——**把「弱」重新描述为「宽」**。

Tai et al. 把同一动作压缩成一段，几乎可以直接当模板（三步都在里面）：

> "One limitation of our work is the focus on open-source LLMs. As shown in [3], **the proprietary GPT-4 model achieved significantly better results compared to the other approaches. However, we find our work to be more reflective of enterprise use cases for code translation as many companies have policies against using proprietary LLMs with sensitive data (such as company code).** Our study shows that leveraging an open-source LLM could be beneficial …"

三步是：① 承认输了 → ② 宣布对方的赛道不是真实赛道 → ③ 把贡献重定义为「在**可部署**的模型上做出的相对提升」。这招不否认差距，只否认差距的相关性，因而**很难被反驳**；代价是论文贡献被压缩成「可部署性」而不是「能力」。

**对我们的可迁移性：最高。** 但⚠️ 有一个生死攸关的前提：**我们的 SOTA baseline 也必须是云端才行**。如果朴素单提示同样能在 Qwen-32B 上跑出高分，约束就不构成差异，这个策略立刻失效。**所以必须补一格实验：朴素单提示 + Qwen-32B。** 这一格是整条 story 的生死线，缺了它，审稿人一句「那你为什么不在小模型上也用朴素提示」就把论证打穿。

### 策略 B：非劣性替代优越性（把「谁更好」换成「有没有显著差异」）

**样本：Su & McMillan（Automated Software Engineering 2024）、Caumartin et al.（SANER 2025）。**

Su & McMillan 执行得最干净。RQ3 的问句本身就放弃了争胜：**"How closely does the distilled model mimic GPT-3.5 for code summarization, as measured by human experts?"**——问「模仿得多像」而不是「谁更好」。结果句同样：**"we do not observe a statistically-significant difference between the 350m parameter jam model and GPT-3.5 in terms of accuracy, completeness, or conciseness."** 他们**没有隐瞒不利数**：直接偏好投票 52% GPT-3.5 / 46% jam / 2% 未决白纸黑字写在 Discussion 里，措辞是 "a slight preference favoring GPT-3.5"，随后用一句话兜住：**"an inexpensive model such as 350m jam can replicate a very large model such as GPT-3.5 … when provided sufficient examples."**

Caumartin et al. 是**在真正输了的情况下**用这一招的样本，值得细看：他们在 EM 上输了近一半（16.70 vs 8.94），但换到 BLEU-T 上做检验——

> "CodeLlama obtained the same BLEU-T mean score as ChatGPT, i.e., **the Mann-Whitney U test showed no significant difference under 95% confidence level.**"

——据此在摘要里写 "often comparable to ChatGPT"，在结论里把限定词写进句子："compares with ChatGPT 3.5 … **as measured by BLEU-T scores**"。而对输掉的那个指标，他们坦承并归因：

> "We infer that the model's large parameter size, **25x larger than the Llama models under study**, enables ChatGPT to infer the writing style from the provided original code in a way that is more similar to the original developer."

⚠️ **「未拒绝原假设」不等于「证明了等价」。** 这是审稿人一定会挑的点，而它在 SANER 过审了——说明这是社区当前可接受的下限，但不是可靠的下限。**如果我们要走这条路，应当用正式的等价性/非劣性检验（如 TOST）并预先声明边界值 δ**，而不是靠「p > 0.05」。

**对我们的可迁移性：中。** 我们现在是 60.4% vs 76.2%，**差 15.82 个点，不可能通过任何非劣性检验**。策略 B 单独用不了——除非能找到一个**分层子集**，在其上差距落进噪声范围。这需要先测代次内方差（见根 CLAUDE.md「先测噪声底再谈效果」）。

### 策略 C：⛔ 换分母——不跟强者比，跟「方法之前的自己」比

**样本：Bappy et al.（0% → 99%）、Kumar & Chimalakonda（vs 未微调的 Fed 0，+18% / +3% / +53%）、Tai et al.（vs zero-shot，+13.8% / +6.7%）。**

三篇的主结果**全部是相对增益**，而基线是各自能选的最弱那一个。Bappy 走到了极端：未微调的 codegen-mono **"failed to detect a single CWE"**，于是叙事变成「0 → 99%」，SOTA 对照被挤出了画面；他们在 Limitations 里承认对照缺失是待办——**"conducting rigorous comparative benchmarks against SAST tools and LLMs are also crucial next steps"**。

⚠️⚠️ **这条我单列出来不是推荐，是警告。** 这是本批出现频率最高的手法，也是**我们最需要主动防守的一点**：审稿人只要问一句「跟一个像样的基线比呢」，整段就塌了。而我们的处境比他们更危险——**我们已经知道朴素单提示是 76.2%**，知情不报属于选择性报告，按仓库 §3.5 是 C 级问题。

### 策略 D：把损失重述为取舍，而不是缺陷

**样本：Hasan et al.（MSR 2025）。**

人评里微调 LLaMA 在 correctness（4.15 vs 4.23）与 completeness（3.61 vs 3.91）上都输给 GPT-4o。处理方式不是淡化，而是**给出机制解释，把两个指标绑成此消彼长的一对**：

> "A negative correlation is observed between completeness and relevance: GPT-4o compromises dearly on relevance to achieve completeness, often including unnecessary details, while LLaMA prioritizes relevance, which might lead to incomplete scenario coverage."

于是「LLaMA 更不完整」变成「LLaMA 更不啰嗦」的同一件事的另一面。他们还配了一个有利数据点（relevance 上 LLaMA 4.02 略高于 GPT 3.98）坐实这个对偶关系。

**对我们的可迁移性：中等偏高，但有学术风险。** 取舍叙事只有在**两端都有真实数据**时才成立；只有「覆盖率低」而拿不出对应的「多报少」，那就是修辞而非发现。⛔ 按仓库 §3.5，无数据支撑的取舍叙事属于「评测口径迁就结果」。我们手上是否有多报侧对照数据（`over@1` / `over@any`）决定这条能不能用。

### 策略 E：换评价维度（不比准确率，比别的）

**样本：Wolfe et al.（FAccT 2024）、NVIDIA 立场论文。**

Wolfe 等人明确让出 zero-shot SOTA 给闭源模型，把 parity 限定在 "domain-adapted tasks"，然后追加三个闭源模型结构性劣势的维度（bias、privacy、abstention）。NVIDIA 立场论文整段绕开效果比较，只论 "sufficiently powerful … and necessarily more economical"。

**对我们的可迁移性**：这正是我们那句「附带可断言、可追溯的结构化产出」的所在位置。但⚠️ 换维度必须**换到一个能被测量的维度**上；「可追溯」若没有量化指标（例如：产出中可被自动核验的断言比例、每条发现能否定位到需求原句），就只是宣传语。⛔ 我们目前没有这个指标，**需要先定义再测**。

### 策略 F：干脆不跟通用 SOTA 比，并把「不比」包装成研究缺口

**样本：Sirin et al.（PROFES 2025）、Kumar & Chimalakonda、Bappy et al.、LLaMA-Reviewer。**

Sirin 的做法最完整：在 Related Work 里点名前人用 GPT-4 的工作，然后一句话判其不适用——

> "**Although they employed LLMs to generate requirements, their approach overlooks data privacy concerns due to the use of cloud-based models, and the regulated industry was not within the scope of their study.**"

——缺口于是成立，SOTA 对照在逻辑上变得不必要。句式在三篇里高度一致：「前人用了云模型，**因此**没有解决隐私场景，**因此**存在缺口」。Kumar 更进一步，把它写成方法学原则：**"To maintain the privacy-aware aspect of this study, we avoided using any closed-source models."**

**这一招把「我没比」变成「我不该比」**，是本批最有效也最需要警惕的修辞。

**对我们的可迁移性：低到不可用。** 2023–2025 年这样做还行，2026 年审稿人一定会问「和 GPT-5.5 直接问一遍比呢」，而我们**已经知道**答案。

### ⭐ 最诚实的一条做法（建议我们采用）：把被约束牺牲掉的那一侧真的跑出来报数

**Kumar & Chimalakonda 是本批唯一这么做的。** 他们的不利结果不是「输给 GPT-4」，而是「联邦版输给集中训练版」——同一个模型、同一份数据，只因隐私约束而降级。他们把这个上界**真的跑了并报了数**，然后一句话收尾：

> "the central model performs better because it can access and train on the entire dataset at once, rather than through multiple federated rounds. **However, we choose FL because it offers privacy.**"

并在方法学层面提前定义：**"we include its metrics to illustrate the trade-off in performance when opting for a privacy-aware federated approach over a central model."**

**对我们的直接含义**：我们应当把「云端 SOTA + 我们的方法」和「云端 SOTA + 朴素提示」都跑出来当作**上界**如实报告，而不是回避。这比任何修辞都更能挡住「你在藏结果」的指控，代价只是承认我们不是最强——而我们本来就不是。

### ⚠️ 一个反面教训：不要把 parity 建在格式一致性上

InstruBPM（Qwen3-4B）在 BLEU 上 83.06 vs GPT-5.1 的 12.64，看起来是碾压。但这个量级几乎**必然**主要来自「微调模型学会了目标 DOT 书写约定」，而不是「它更懂业务流程」。他们自己间接承认了：给未微调基线加上语法参考与示例后，基线分数**翻倍**（正文说不加这些的话 "untuned models performed substantially worse—approximately half the scores reported in Table 2"）。

**教训**：如果我们的方法输出结构化制品而 baseline 输出自由文本，任何基于形状的指标都会给我们不当加分。**指标必须锚在语义命中上，不能锚在形式合规上。**

### ⚠️ 另一个空白：没有任何一篇给出质量维度的「够用阈值」

这一点值得单独指出，因为它是这批文献的共同短板，也是我们可以在 Related Work 里指出的空白：**所有论文对「够用」的定义几乎全部落在成本与部署侧**——Caumartin 是「假设每天约 100 次代码评审，现有硬件就够，因而 cost-effective」；Bappy 是「无 GPU 的 i5 台式机上 6 tokens/s」；Su & McMillan 是「单张 16GB 消费级 GPU」。**没有一篇说「F1 达到 X 就可以上生产」。** Sirin 甚至只能给定性说法：模型 "usually **miss coverage or introduce out-of-scope lower-level requirements**"，因而 "requires close supervision from RE professionals"。

## 3. ⭐ 防稻草人的做法（他们怎么给大模型设计 prompt）

**先给总评：整批的水平很低。** 五篇隐私动机族里，唯一做了实质努力的是 Caumartin（SANER 2025），其余要么根本没跑大模型（Sirin、Bappy、Tai 引用他人数字），要么原则性拒绝跑（Kumar）。**多次采样与方差报告：这五篇全部缺失**（Caumartin 用温度 0 规避，Sirin 明确写了「所有结果只跑一次」）。做得较好的样本反而来自非隐私动机的那几篇。

按防守强度从弱到强排列。

### 3.1 最弱：只交代 prompt 并把它列入威胁效度

**Su & McMillan** 给 GPT-3.5 的是一句极简 prompt：`Write a one sentence description of this Java method:`，后面直接跟方法源码，没有 few-shot、没有格式约束、没有角色设定。他们**没有辩称这是最优 prompt**，而是写进 Threats to Validity：

> "The GPT-3.5 version and prompt are threats to validity because GPT-3.5 is a commercial product and subject to change without notice, and also may give different answers with different prompts."

然后两条兜底：一是**降级 claim 的作用域**——"we view this paper as still valid as a framework for distilling knowledge from large models"（贡献是蒸馏框架，不是某个分数）；二是**发布 GPT-3.5 原始响应作为独立数据集**供复核。

⚠️ 这在 2024 年勉强够用，2026 年不够。但那个「降级 claim 作用域」的动作值得学：**当基线配置可能被质疑时，把主张从「我们更好」退到「我们提供了一个框架/一套证据」，质疑就打不到承重墙上。**

### 3.2 中等：复用被复现论文的 prompt 网格，并声明公平意图

**Caumartin et al.（SANER 2025）** 直接复用被复现论文（Guo et al., ICSE'24）的 5 套 zero-shot 模板与温度网格：

> "To ensure fairness in model comparison, we directly applied the zero-shot templates provided by Guo et al. in our study."

并给 Llama 侧同等的调参预算：5 prompts × 3 temperatures × 每配置 2 次 = **7500 次推理**；温度 0 下输出确定，声明可复现；Threats 里承认双方都只有 zero-shot、没做 few-shot/CoT。

⛔ **但有硬伤，必须一起记住**：ChatGPT 的数字**不是自己重跑的**，是照抄 Guo et al. 的报告值；同时 Llama 侧做了适配改造（INST 标签、要求三重反引号包裹、禁止写语言名），ChatGPT 侧无法同步这些改造。**双方并非同一次实验里的同一条流水线。** 这是我们不能照抄的部分。

### 3.3 中等偏强：给基线额外脚手架，并量化脚手架的贡献

**InstruBPM** 做得最明确。给未微调基线（含 GPT-5.1、Claude-4.5、Gemini-2.5）的是**加强版 zero-shot**：

> "For untuned baselines, we use a strengthened zero-shot prompt to ensure fairness: rather than only requesting a BPMN model, the prompt includes syntax conventions and a small illustrative example."

并**量化了这个加强的效果**：不加脚手架时基线约为表中分数的**一半**。另有两条细节值得抄：**给闭源模型开推理模式**（"we evaluated them using their respective reasoning variants configured with a medium thinking-effort setting"）；**采样参数全模型统一**（temperature 0.1、top_p 1.0、max 2048，"held constant across all models and strategies to isolate the prompting effects"）。

### 3.4 强：主动尝试强化基线并报告「强化无效」

**Hasan et al.（MSR 2025）** 做了两次强化基线的尝试，两次都报了负结果：

1. **加项目描述的增强 prompt**：GPT-4o 从 F1 88.01 → 87.95（不升反降）。结论逐字："it is evident that the enhanced prompts do not make any significant difference in the performance of the models."
2. **加 RAG**：GPT-4o 88.01 → 88.49（+0.48），微调模型反而略降。解释是跨项目的用例-测试用例对相似度低，检索到的示例不够相关。

**这是最实用的防守形态**：不是声称「我们的 baseline 已经最优」，而是**展示「我们试图让它更强，它没变强，这里是数字」**。审稿人要求「你应该给大模型也加上你那套流水线」时，能拿出的最好回应就是「加过，附表 IX 和表 X」。

### 3.5 最强：完全不自己配置基线，全部引用官方最优数

**Agentless（FSE 2025 / PACMSE vol.2:801–824, DOI [10.1145/3715754](https://doi.org/10.1145/3715754)；preprint [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)）**：

> "For baseline tools, we directly use the reported results either from the official leaderboard or from the tool's official paper/repository."

26 个 agent 基线的分数全部来自各自作者或官方榜单自报的**最佳配置**，Agentless 团队没有动过任何超参、prompt 或工具定义。**没有可供调低的旋钮，指控就无从落脚。** 他们还主动交代了这个做法的反向代价："the majority of the closed-source baselines do not provide any trajectories, just the submission patches. Therefore, we cannot verify the steps taken to arrive at the final patches." 补强还有第三方独立复算：OpenAI 独立在 SWE-bench Lite / SWE-bench / Verified 上评测并确认了结论。

⚠️ 它有一处没有正面回应的质疑：**双方调优努力量不对等**——拿基线的官方最优数去比自己**精心调过**的 pipeline（40 patches/bug、40 reproduction tests/issue、4 组 edit locations）。这不构成不公，但照抄这招要预判这个问题。

### 3.6 给我们的可执行清单

综合上面五档，一篇 2026 年的论文若要做 parity claim，**基线侧至少要交代**：

1. 精确 model id + 调用日期 + 采样参数，且**全模型统一**（InstruBPM 做法）。
2. 基线 prompt 的**完整原文**（附录或 artifact），并说明它为什么是这个形状。
3. **至少一次强化基线的尝试及其结果**——few-shot、结构化输出约束、推理模式、RAG 任选，报告 delta，哪怕是负的（MSR 2025 做法）。
4. **多次采样**而非单次，报告方差。⚠️ 隐私动机族五篇**全部缺失**这一项；做了的只有 TOSEM 那篇（每个实验跑三次取平均）。这是最容易做到、也最容易成为我们相对优势的一项。
5. 把 prompt 与版本列入 Threats to Validity（Su & McMillan 做法），并公开 raw output 供复核。
6. ⭐ **把被约束牺牲掉的那一侧（云端上界）真的跑出来报数**（Kumar 做法）。

另有一份专门的报告规范可直接引：**Korn, Zaruchas, Arora, Metzger, Smolka, Wang, Vogelsang, *Reporting LLM Prompting in Automated Software Engineering: A Guideline Based on Current Practices and Expectations*, FORGE 2026, [arXiv:2601.01954](https://arxiv.org/abs/2601.01954)**。它分析了三大 SE 会议自 2022 年以来约 300 篇论文的 prompt 报告实践，并调查 105 位 PC 成员的期望，发现三处主要错位：**版本披露、prompt 论证、威胁效度**。⚠️ 我只读到摘要页，具体的 essential/desirable/exceptional 分级清单未读到，引用前需补读正文。

**这批论文里没有一篇把上面 6 条都做到**——这本身就是我们相关工作段落可以指出的空白，也是我们做全之后可以主张的方法论贡献。

## 4. ⭐ 「复杂流水线在强模型上反而更差」的文献证据

**结论先行：有，而且证据链比预期强得多。** 九篇从不同角度指向同一组机制，其中六篇给了逐格数字；**其中一篇的任务域与 project_1 完全相同**。

### 4.1 ⭐⭐ 同一任务域的直接同形证据：NL → UML 状态机上，朴素单提示在强模型上打败流水线

**Abdulkarim, Boyd, Bridi, Tufenkjian, Chen, Mussbacher (McGill), *Structure- and Event-Driven Frameworks for State Machine Modeling with LLMs*, [arXiv:2604.00275](https://arxiv.org/abs/2604.00275)（2026-03-31）。venue 待核验。**

任务是**从非结构化自然语言生成 UML 状态机**（states / transitions / guards / actions / parallel regions / hierarchical / history states）。四种策略：单提示基线、Structure-Driven SMF、Event-Driven SMF、Hybrid（单提示出草稿再迭代精化）。

| 策略 | GPT-4o overall $F_1$ | Claude 3.5 Sonnet overall $F_1$ |
|---|---|---|
| Single-Prompt Baseline | 0.5431 | **0.7029** ← 全实验最优 |
| Structure-Driven SMF | 0.6260 | 0.5026 |
| Event-Driven SMF | 0.3735 | 0.3052 |
| Hybrid Approach | **0.6559** | 0.6336 |

⭐ **一个干净的 crossover**：在较弱模型（GPT-4o）上脚手架 **+0.11**，在较强模型（Claude 3.5 Sonnet）上脚手架 **−0.07 到 −0.40**。机制陈述逐字：

> "These findings suggest that while non-reasoning LLMs benefit from multi-step generation strategies, **such strategies may interfere with the inherent step-by-step reasoning process of reasoning LLMs.**"

弱模型上脚手架为什么有用，它也说清楚了——**精度换召回**：Structure-Driven 相对基线精度 −0.0568（0.7130 → 0.6562）而召回 **+0.1767**（0.4501 → 0.6268）。

**这篇是本调研对我们最重要的单条发现**：任务域相同（状态机建模）、现象相同（我们 60.4% vs 朴素 76.2%）、方向相同（强模型上流水线更差）。它既是我们「不是我们做错了什么」的最强外部佐证，也**直接构成一个我们必须回应的先例**。

⛔ **但有五条必须一起写的限定，否则会被反打：**

1. **样本只有 8 个**，且来自本科建模课：`our dataset of eight examples is a limitation. While these examples vary in complexity, they come from an undergraduate modelling course and may not generalize`。
2. **shot 数不对等，基线被有意加强**：`For our single-prompt strategy we employ 3-shot prompting, adding another ground truth state machine, ChessClock, to our pool, aiming to improve upon the baseline accuracy`（多步策略是 2-shot）。⚠️ 论文内部还自相矛盾：框架定义节写的是 `Single-Prompt Baseline is a generation strategy with a 2-shot technique`——两处口径不一致，**待核验**。
3. ⭐ **输出格式 + 后处理器混淆**：单提示直出 Umple 代码，多步策略产 HTML 表并过一个 `strict rule-based post-processor module`。作者自陈 `the strict post-processor module for HTML tables may suppress valid LLM outputs that are not fully compliant, hence influencing the final result`。**这正是根 CLAUDE.md §11「确定性门一票否决、模型没有合法写法能通过」的现成外部案例**——「多步流水线更差」里有一部分可能是自家的门吃掉了合法输出，而不是流水线思路有害。⭐ **我们自己也必须先排除这一项再下结论。**
4. **「Claude 3.5 Sonnet = reasoning LLM」是作者自造口径**，与业界通行分类不符（该模型无 extended thinking）。引用时应改述为「在两个模型上呈相反趋势」，不要照搬标签。
5. 无 token / 成本数据；评测是**单作者人工判定、无双人复核**（按仓库「判定层是独立误差源」口径，这是单向误差源）。

### 4.2 最直接的一击：同一技术在强弱模型上符号反转（TOSEM 2025）

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

**token 成本这一侧同样有数**：最刺眼的一格是 o1-mini + UniTrans（Python→Java），994.69 message tokens + **9507.75 reasoning tokens**、**174.92 秒**，是 zero-shot（8.85s）的约 **19.8 倍**，而准确率**反而更低**：

> "the time cost relative to zero-shot prompting increases from 2.0 to **19.8 times, without any corresponding improvement in performance**."

> "this increased computational overhead **does not necessarily translate into better performance**, indicating that more complex prompts may inadvertently prolong reasoning, leading to greater costs without proportional benefits."

⭐ **对我们最有价值的一条是它的消融**：剥掉执行反馈与迭代（`-no-iter`）后，**AgentCoder 在 GPT-4o 上从 96.3 掉到 87.8，低于 zero-shot 的 90.4**。也就是说，AgentCoder 相对 zero-shot 的 +5.9 分**几乎全部来自真实执行反馈，而不是 multi-agent 的提示词结构**：

> "the useful part of each approach's prompt is the **test execution information and the fix phase during the iteration** instead of the **formulation of prompts**."

**机制解释（四条，逐字）：**

1. 基线高度决定改进空间："the sophisticated built-in reasoning capabilities of o1-mini yield **diminishing returns** when further enhanced with prompt engineering, whereas **GPT-4o, with a lower baseline, benefits more significantly from the same techniques**."
2. 外部提示词干扰内建 CoT："Inputting all information simultaneously, without considering its relevance, can **disrupt the internal Chain-of-Thought logic**."
3. 无执行验证的补充信息会误导强模型："without execution feedback that can reflect the ground truth, the supplemental information extracted from the input may not enhance performance and can even hinder it."
4. **任务所需推理深度决定脚手架还有没有位置**：随机抽 300 例统计 o1-mini 的 CoT 步数——generation 3.52、translation 4.35、summarization 1.38；**CoT 步数 ≥ 5 的题目上 o1-mini 比 GPT-4o 好 16.67%，< 5 步的题目上只好 2.89%**。

⚠️ **三条不能越界**：(a)「收益变负」集中在 summarization 与 translation，**code generation 上只是收窄不是变负**（AgentCoder/Self-collaboration/LDB 在 o1-mini 上仍为正）；(b) summarization 的指标是 **GPT 打分 1–5**，不是硬指标；(c) 它测的七个技术标签里**没有 self-consistency，也没有 Tree-of-Thoughts**。

### 4.3 单测生成：朴素提示胜过四条带执行反馈的流水线，且调用量只有一半

**Konstantinou, Degiovanni, Papadakis (SnT Luxembourg + LIST), *How well LLM-based test generation techniques perform with newer LLM versions?*, [arXiv:2601.09695](https://arxiv.org/abs/2601.09695)（v1 2026-01-14, v2 2026-07-29）。venue 待核验。**

Java 单测生成，393 类 / 3,657 方法。复现 **HITS、SymPrompt、TestSpark、CoverUp**（四者**全都带编译/执行反馈迭代修复**）与 `Plain-LLM`（zero-shot + 最多 5 轮修复）对比。模型 GPT-4o-mini（主）、Llama 3.3 70B、DeepSeek V3。逐字：

> "Plain-LLM obtains, in total, 49.95%, 35.33%, and 33.82% on line/branch/mutation coverage, while HITS obtains 42.43%, 29.49%, and 27.97%, SymPrompt 40.95%, 27.19%, and 28.40%, TestSpark 23.65%, 16.48%, and 13.88%, and CoverUP 38.85%, 25.11%, and 26.26%, respectively. **This indicates that with new, relatively strong LLMs, test generation methods provide a limited or no advantage to the generation process.**"

绝对差：朴素提示比最佳流水线高 **+7.52 / +5.84 / +5.42 个百分点**（mutation 一列对最佳基线 SymPrompt 28.40 计）。成本侧逐字：

> "**Finding 2**: […] Interestingly, the second most effective approach, HITS, requires nearly twice as many LLM queries as Plain-LLM does."

HITS 16,735 次调用 vs Plain-LLM 11,815（**1.42×**），覆盖率还低 7.5 个点。规模趋势逐字：**"stronger (newer) LLMs may obviate any advantage these techniques bring."**

⭐ **这是「成本上升、收益为负」最干净的一组数字，且被比较的四条流水线都带真实执行反馈**——也就是说，§4.8 那条「有外部可验证信号就还有救」的共识**在这里失效了**。这一点对我们是坏消息：不能简单地把「我们的 loop 没接外部验证器」当成唯一根因。

⚠️ **两条纠偏**：(a) 摘要里的 **20.92%** 是相对提升且对着 HITS 27.97 算的；对真正的最佳基线 SymPrompt 28.40 算只有 **19.1%**——引绝对百分点更稳。(b)「差距随模型变强而扩大」这条**与数据泄漏混淆**：DeepSeek V3 上差距最大，作者自己归因于数据集可能已进其训练语料，**不可当干净的规模趋势引用**。

### 4.4 成本归一化后自我修复的收益消失（ICLR 2024）

**Olausson, Inala, Wang, Gao, Solar-Lezama, *Is Self-Repair a Silver Bullet for Code Generation?*, ICLR 2024，[arXiv:2306.09896](https://arxiv.org/abs/2306.09896)（v5, 2024-02-02，comments 字段标明 "Accepted to ICLR 2024"）。**

在 Code Llama、GPT-3.5、GPT-4 上评测 HumanEval 与 APPS 的自我修复。核心结论（摘要逐字）：把修复的代价计入之后，**"performance gains are often modest, vary a lot between subsets of the data, and are sometimes not present at all."**

机制解释直指要害：**"bottlenecked by the model's ability to provide feedback on its own code"**——把反馈换成更强模型产生的反馈后收益显著变大；小规模人类反馈实验进一步说明即便最强模型也远不及人类水平的调试。

⭐ **这一条对我们的意义**：我们的 loop 吃掉 79% 的 token 而覆盖率净变化约等于零，与这篇的诊断**完全同形**。它给了一个现成的、可引的因果解释：**自我批判的上限是模型自评的质量，而不是循环的次数或结构。** 同时它指出了下一步方向——**把自评换成外部可验证信号**（这与 §4.2 的 `-no-iter` 消融是同一结论的两次独立观测）。

⚠️ 读到程度：摘要 + 检索摘要（含 pass@t、1.05×、10%/3%、1.58× 等数字）。**arXiv 摘要页未确认 1.58× 与 pass@t 的具体表述**，正文未通读，这几个数字标为**待核验**。

### 4.5 同模型下复杂 agent 既更差又更贵（FSE 2025）

**Xia, Deng, Dunn, Zhang, *Agentless: Demystifying LLM-based Software Engineering Agents*；正式版 *Demystifying LLM-Based Software Engineering Agents*, Proc. ACM Softw. Eng. (PACMSE) vol. 2 (2025) 801–824, DOI [10.1145/3715754](https://doi.org/10.1145/3715754)（= FSE 2025）；preprint [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)。**

SWE-bench Lite 上、**同一个 GPT-4o**：

| Tool | LLM | % Resolved | Avg. $ | Avg. tokens |
|---|---|---|---|---|
| **Agentless** | GPT-4o | **32.00%** | **$0.70** | **78,166** |
| SWE-agent | GPT-4o | 18.33% | $2.53 | 498,346 |
| AutoCodeRover | GPT-4 | 19.00% | $0.45 | 38,663 |
| Moatless | GPT-4o | 24.67% | $0.14 | – |

高 **13.67 个百分点**，成本 **1/3.6**，token **1/6.4**。SWE-bench Verified 复现同一格局（Agentless 38.80% vs SWE-agent GPT-4o 23.20%）。

它对复杂度的三条机制批判（皆逐字）：工具设计易出错且 "incur additional cost in wasted LLM queries"；决策不可控，"an agent can take upwards of 30 or 40 turns, which makes it extremely difficult to both understand the decisions made by the agents and also debug"；自反思能力有限，"an **incorrect step can be easily amplified** and negatively affect all future decisions"。

⚠️ **三条必须一起引的限定**：(a) 它**不是榜首**（CodeStory Aide 43.00%、Bytedance MarsCode 39.33% 都更高），"highest performance" 只在 **open-source** 范围内成立；(b) 它**不是最便宜**（Moatless $0.14），原文措辞是 "less than **most** prior agent-based approaches"；(c) 它**只用了 GPT-4o 一个模型**，**没有模型强度这一维的对照**——所以它支撑的是「同模型下 agent 不如流水线」，**支撑不了**「强模型上 agent 才失效」。后者只有 §4.2 能撑。

### 4.6 ⭐ 逐模型消融：同一套符号脚手架，给最弱模型 +35、给最强模型 +3（2026）

**VerIbmc（[arXiv:2606.16886](https://arxiv.org/abs/2606.16886)）** 给了本调研里**最贴合我们处境的一张表**。它对同一套三阶段流水线做 Basic（完整流水线）vs LLM-Only（跳过符号先验）的对照：

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

**推论（我们必须自己面对的算术）**：如果我们的方法在 Qwen-32B 上的增益是 Δ，而 Qwen-32B 与云端 SOTA 的裸能力差是 G，那么 story 成立的必要条件是 **Δ ≳ G**。VerIbmc 那个任务上 Δ_max ≈ 35 而 G ≈ 89，**它做不到，所以它老老实实用了策略 A（承认落后 + 绑定约束）而不是宣称打平。**

### 4.7 补充证据（三条，分量弱一档但机制各不相同）

**(a) 上下文脚手架的边际收益在前沿模型上大面积为负。** Sepidband, Pham, Hemmati, *On the Role of Fault Localization Context for LLM-Based Program Repair*, [arXiv:2604.05481](https://arxiv.org/abs/2604.05481)（2026-04-07，venue 待核验）。SWE-bench Verified 全 500 实例、**GPT-5-mini**、61 个配置全因子消融 + Wilcoxon 检验。逐字：

> "**Across all 177 comparisons, 61 violate our RQii.1 and RQii.2 hypotheses, meaning that providing additional context degraded repair performance.**"

> "Negative impacts occur in the majority of configurations for both 'code slicing' (8/12) and 'context window' expansion (7/12)"

⭐ 它给了一个可以直接借用的机制词——**噪声稀释**："Additional lines introduce noise (irrelevant code paths, error handling, logging) that **dilutes the repair signal**"；以及 "irrelevant information **alters the model's reasoning trajectory**"。质性案例：给了几何相关函数后，模型错误推断维度不匹配应抛 `ValueError`，而正解是补零升维——`unrelated abstractions bias the model toward an overly restrictive interpretation`。⚠️ 它测的是**上下文粒度**，不是 self-refine / 多智能体，**不能当同一种消融引**。

**(b) 多智能体相对单智能体的优势随模型变强而缩小。** Gao, Li, Liu, Yu, Wang, Lin, Lai, *Single-agent or Multi-agent Systems? Why Not Both?*, [arXiv:2505.18286](https://arxiv.org/abs/2505.18286)（2025-05-23，无 venue）。摘要逐字：**"the benefits of MAS over SAS diminish as LLM capabilities improve"**，理由是前沿模型（点名 OpenAI-o3、Gemini-2.5-Pro）在长上下文推理、记忆与工具使用上的进步侵蚀了 MAS 最初的立论基础。⚠️ 仅摘要。

**(c) 中间指标改善不等于端到端改善。** Steenhoek et al., *To Err is Machine: Vulnerability Detection Challenges LLM Reasoning*, [arXiv:2403.17218](https://arxiv.org/abs/2403.17218)。⚠️ **未独立核验，转述自子调研，标待复核。** C/C++ 函数级漏洞检测，14 个模型 × 6 种 prompt 脚手架，据报 `none of the models or prompts exceeded the random-guessing baseline (Balanced Accuracy = 50) by more than 5%`。⭐ 最有用的一条：`CoT-Annotations reduced the errors of bounds/NULL checks recognition by 15-70% […] We also observed that the improvement of understanding bounds/NULL checks did not significantly improve the models' performance`——**中间能力提升了，端到端没动。** ⚠️ 方向要当心：此文说的是「**任何**手段都不涨（含扩大模型）」，**不是**「模型越强脚手架越无用」；作者结尾反而把推理模型 + 脚手架当希望，**不能引成反脚手架**。

### 4.8 这条证据链怎么用

**共识机制有三条，彼此独立：**

1. **收益来自可验证的外部信号，不来自脚手架的组织形式。** Agentless 的 Table 4（majority voting 77 → +regression test 81 → +reproduction test 96）与 TOSEM 的 `-no-iter` 消融（AgentCoder GPT-4o 96.3 → 87.8）是两次独立佐证；Olausson 从反面说明外部信号缺席、只能靠自评时收益为什么消失。
2. ⭐ **噪声稀释 / 推理轨迹被改道。** 这是**单智能体多阶段**的机制，与「多智能体的协调开销」不是一回事——**对我们更相关，因为我们做的是流水线不是多智能体**。见 §4.7(a) 的 `dilutes the repair signal` / `alters the model's reasoning trajectory`，以及 §4.1 的 `may interfere with the inherent step-by-step reasoning process`。
3. ⭐ **脚手架的收益可能被脚手架自己的确定性门吃掉。** §4.1 的作者亲口承认 `the strict post-processor module for HTML tables may suppress valid LLM outputs that are not fully compliant`。这意味着「多步流水线更差」的观测里有一部分是**流水线自带的严格校验门误伤**，而非流水线思路有害。这既是引用时的诚实限定，也正好是根 CLAUDE.md §11 那条纪律的外部佐证。

⭐ **对我们的直接含义（三条自查，写之前必须做完）：**

- 我们那句「loop 吃掉 79% token 而覆盖率净变化约等于零」**不是丑闻，而是一个已被文献反复确认的现象**。但⚠️ **不能直接拿机制 1 挡枪**：§4.3 那四条被打败的流水线**全都带真实执行反馈**，说明「有外部信号就还有救」并不总成立。
- ⛔ **先排除机制 3 再下任何结论**：我们的契约门 / 致命门 / 谓词拒答有没有在吃掉本来正确的产出？这与仓库 §11、§13 是同一件事，且 §4.1 提供了「别人也栽在这里」的先例。
- 机制 2（噪声稀释）意味着一个具体的可测假设：**我们的 loop 在后续轮次注入的反馈文本，是否把模型从第一轮已经正确的判断上带偏了**。这可以用「首轮命中但末轮丢失」的条目数直接量出来，不需要新实验。

### 4.9 ⭐ 一条文献真空（可直接写进 motivation）

**在 2026 年前沿模型（Claude 4.x / GPT-5.x / Gemini 3.x 一级）上，对 self-refine / 多智能体 / 迭代反馈做逐组件消融、并同时报告 token 成本倍数的 SE 实证研究——本次检索一篇都没找到。**

最接近的三个都各差一环：**2604.05481** 用了 GPT-5-mini，但测的是上下文粒度而非循环；**2604.00275** 有干净的 crossover，但只有 8 个本科课程样本、模型是 2024 年的、且有输出格式与后处理器的混淆；**2601.09695** 有完整的调用量记账，但模型主力是 GPT-4o-mini，且规模趋势与数据泄漏混淆。

⭐ 我们手上的 v46 全量矩阵（54 pair × 2 模型 × 3 轮、逐阶段降级诊断、逐格 token 记账）**恰好就是填这个空缺的形状**。⚠️ 但要主张这个空缺，必须先做 §6.1 第 2 条说的 venue 级扫库——「检索没找到」不等于「不存在」。

## 5. 检索过程

**时间**：2026-08-13。**工具**：WebSearch + WebFetch（arXiv abs / HTML）；PDF 走 `python -m tools.pdf_extractor -m text` 本地提取后逐段读。本路调研另派了两个并行子调研（隐私动机族、负面结果族），其检索式一并计入下表。

| # | 关键词 | 有效命中 |
|---|---|---|
| 1 | small open-source LLM matches GPT-4 SE fine-tuning pipeline ICSE 2025 | 0 直接命中；引出 AwesomeLLM4SE 索引与 Su & McMillan 线索 |
| 2 | open-source LLM privacy on-premise GPT-4 comparable requirements engineering | 0 SE 命中（结果偏向通用 open vs proprietary 对比与医疗领域） |
| 3 | agentless simple pipeline outperforms complex agent LLM SE | 1（Agentless） |
| 4 | small language models SE empirical 7B match GPT-4 | 1 弱命中（Assessing SLMs for Code Generation，arXiv:2507.03160，明确未测 GPT-4，未纳入） |
| 5 | advanced prompting CoT self-refine do not improve stronger models negative result | 2（TOSEM 2411.02093；CodePromptEval 2412.20545 未深读） |
| 6 | RepairLLaMA fine-tuned LLaMA program repair outperforms GPT-4 | 1 |
| 7 | Distilled GPT for source code summarization Su McMillan | 1 |
| 8 | LLaMA-Reviewer PEFT code review ISSRE 2023 | 1 |
| 9 | Small Language Models are the Future of Agentic AI | 1（NVIDIA 立场论文） |
| 10 | Qwen open-weight requirements/UML state machine local deployment MODELS | 0 直接命中；引出 InstruBPM（BPMN） |
| 11 | structured output / constrained decoding compensates small model capability gap | 若干 2026 年 arXiv 条目，**均未核验**，仅作线索 |
| 12 | fine-tuned small model unit test generation / fault localization beats GPT-4 privacy | 2（MSR 2025 高层测试用例；SAP HANA 故障定位） |
| 13 | LLM formal specification / model checking open small model verifier feedback loop | 1（VerIbmc，与我们最同构的样本） |
| 14 | SE LLM weak baselines straw man unfair comparison | 0 直接命中；引出 FORGE 2026 prompt 报告规范 |
| 15 | self-repair silver bullet cost analysis | 1（Olausson et al. ICLR 2024） |
| 16 | industrial open-weight LLM static analysis cannot send code self-hosted | 弱命中，多为 2026 年 arXiv 条目，**未核验** |
| 17 | multi-agent vs single agent no significant improvement cost overhead | 1（arXiv:2505.18286） |
| 18 | open-weight small LLM comparable to GPT-5 scaffolding ICSE 2026 | 0 |
| 19–30 | 子调研 A：on-premise / locally deployed / self-hosted + code review / requirements / CWE / federated；regulated industry（automotive, medical device）+ local LLM；replication study Llama vs ChatGPT | 5 篇（Caumartin、Sirin、Kumar、Bappy、Tai），其中 4 篇读到全文 |
| 31–42 | 子调研 B：self-refine / self-repair negative results；multi-agent vs single agent；"does not help" / "fails to improve"；agentic overhead / token cost vs accuracy；state machine modeling with LLMs multi-step vs single prompt；test generation techniques newer LLM versions | 5 篇（Abdulkarim、Konstantinou、Sepidband、Steenhoek、Li），其中 3 篇由子调研独立回原文核验 |

**venue 覆盖情况（读到正文者）**：**SANER 2025**（CCF B）、**MSR 2025**（CCF B）、**Automated Software Engineering 期刊**（Springer）、**FSE 2025 / PACMSE**、**ACM TOSEM**、**ICLR 2024**、PROFES 2025（workshop 分册，非 CCF），外加 8 篇无 venue 的 arXiv preprint。**ICSE、ASE 会议、ISSTA、EMSE、MODELS、RE 仍然零命中**；TSE 只有 RepairLLaMA 一条且仅摘要。

⚠️ **一条必须写明的分量提示**：§4 里与我们契合度最高的三篇（Abdulkarim 状态机、Konstantinou 单测、Sepidband 修复上下文）**全部是 2026 年的 arXiv preprint，无 journal-ref，是否已有同行评议版本待核验**。它们与命题的契合度高于其它篇目，但**引用分量弱一档**，不能当作已被社区确认的结论使用。

**语料规模**：约 42 条检索式，浏览标题/摘要级候选约 300 条，进入本文件**去重后 24 篇**（§1 表 14 篇 + §3 独有 2 篇 + §4 独有 8 篇），其中**读到正文（全文或关键章节）14 篇**。

## 6. 覆盖边界与待核验项

### 6.1 覆盖边界（诚实交代）

1. ⛔ **这不是 systematic review。** 没有预注册检索协议、没有 PRISMA 流程、没有双人筛选、没有覆盖 ACM DL / IEEE Xplore / Scopus 的系统检索。检索完全是关键词驱动的机会性检索，命中受搜索引擎排序影响很大。
2. ⛔ **CCF A 会议的正文覆盖为零。** ICSE / ASE / ISSTA / MODELS / RE 一篇正文都没读到。**下一步应当直接翻 conf.researchr.org 的 ICSE 2025/2026、ASE 2025、ISSTA 2025 accepted papers 列表，而不是继续用关键词搜。**
3. ⛔ **「小模型 + 推理时方法学补偿」这个精确形态的 SE 论文，样本量极小。** 大量命中其实是「小模型 + 微调」（RepairLLaMA、LLaMA-Reviewer、MSR 2025、InstruBPM、Kumar、Bappy），而**不是**「不微调、靠推理时的多阶段结构补偿」。真正与我们同构的只有 **VerIbmc 一篇**。这本身是个信号：**要么这个 niche 确实空着（对我们是机会），要么它被证明不 work 所以没人发（对我们是警告）。** 目前证据（§4.6 那张表）两种解读都支持，需要更多样本才能分辨。⭐ 有一条可直接引的空白佐证：[arXiv:2509.11446 — LLMs for RE: A Systematic Literature Review](https://arxiv.org/html/2509.11446v1) 明确指出「本地可部署模型」是 LLM4RE 的公认空白（**该 SLR 本身未核验，仅由子调研在检索中命中**）。
4. ⛔ **中文 / 非英文文献、工业界白皮书、工具报告完全未覆盖。**
5. ⛔ **时间窗**：主要覆盖 2023-06 至 2026-06。2026 年上半年的 arXiv 条目很多只有摘要级验证。
6. ⚠️ **样本的质量方差极大。** 本文件里既有 TSE / TOSEM / FSE / SANER / MSR，也有测试集只有 100 条合成样本的 arXiv preprint。**修辞策略的归纳跨越了这个质量带**——低质量样本的修辞不代表它能过 CCF A/B 的评审。

### 6.2 待核验项（按优先级）

| # | 事项 | 为什么重要 | 怎么核 |
|---|---|---|---|
| 1 | **TOSEM 正式版（DOI 10.1145/3771933）的模型集与数字** | §4.2 全部数字取自 arXiv v1（GPT-4o + o1-mini）；正式版扩到了 Claude 3.5 Sonnet 与 o1，Critique 的符号反转在正式版是否仍成立**未知**。这是我们最想引的一条 | ACM DL 对自动抓取返回 403，需人工下载 PDF |
| 2 | **Olausson et al. 的 pass@t 定义与 1.58× 人类反馈实验** | §4.4 这两个数字来自检索摘要而非正文 | 读 [ICLR 2024 proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/9ddc141bdbf9d1db510cefff56c586ad-Paper-Conference.pdf) |
| 3 | **Sirin et al. PROFES 2025 会议版的数字** | §1/§2 的引用来自**同题硕士论文**而非会议版，两者可能有出入 | Springer 付费墙，需机构访问 |
| 4 | **RepairLLaMA 正文里 GPT-4 baseline 的 prompt 配置** | 它是 parity claim 的重要样本，但只读到摘要，不知道给 GPT-4 的是什么 prompt、几次采样 | 读 [arXiv HTML](https://arxiv.org/html/2312.15698v1) 或 TSE 正式版 |
| 5 | **Wolfe et al.（FAccT 2024）用的具体开源模型型号** | 摘要页未列名 | 读正文 |
| 6 | **Jambigi et al. 的模型型号 + 「GPT-4o 在混淆 stack trace 上 0% 准确率」这个实验是否真实存在** | 检索摘要提到它，但 arXiv abs 页**没有**这段。若真实，它是隐私动机最有力的一条证据（说明「混淆后再发给云端」这条退路走不通） | 读 [arXiv HTML v3](https://arxiv.org/html/2501.18005v3) |
| 7 | **VerIbmc 的 venue** | arXiv 页无 venue 标注，2026-06 提交，可能在投 | 查 DBLP / 作者主页 |
| 8 | **Kumar & Chimalakonda、Tai et al.、Bappy et al. 是否已正式发表** | 三篇均为 arXiv preprint，dblp 仍记 CoRR | 查 DBLP |
| 9 | **InstruBPM 的同行评审状态** | 标注 "under preparation for journal submission"，即**未经同行评审** | 引用时必须标明是 preprint |
| 10 | **FORGE 2026 prompt 报告规范的 essential/desirable/exceptional 清单** | §3.6 想直接引它的清单，但只读到摘要 | 读 [arXiv](https://arxiv.org/abs/2601.01954) 正文 |
| 11 | **§5 检索式 11 与 16 引出的 2026 年 arXiv 条目** | 一条都没核验，标题与结论均来自搜索摘要 | 逐条回 arXiv 核对是否存在、ID 是否正确 |
| 12 | **Agentless 的 FSE 2025 归属** | 经 DBLP API 核验为 PACMSE vol.2 (2025) 801–824，DOI 10.1145/3715754。⚠️ arXiv v2 的数字与 FSE 正式版可能有差异 | 若要引具体数字，用正式版复核 |
| 13 | **arXiv:2509.11446（LLM4RE SLR）中「本地可部署模型是公认空白」这句话** | §6.1 第 3 条拿它当空白佐证，但未核验 | 读正文 |
| 14 | ⭐⭐ **arXiv:2604.00275 的 venue + 那处 shot 数自相矛盾（3-shot vs 2-shot）** | 它是 §4.1、与我们同任务域的最重要一条。若基线其实是 2-shot，则「基线被有意加强」这个限定不成立，结论的分量反而更重；反之亦然。**这个矛盾必须解开才能引** | 读全文 §框架定义节与 §实验设置节，比对；venue 查 DBLP |
| 15 | ⭐ **arXiv:2601.09695 的 venue，以及 v1 与 v2（2026-07-29）之间数字是否变化** | §4.3 的数字取自子调研抓取的版本，未标明是 v1 还是 v2 | 比对两版 |
| 16 | **arXiv:2604.05481 的 venue** | §4.7(a)，2026-04 提交 | 查 DBLP |
| 17 | ⭐ **arXiv:2403.17218（Steenhoek et al.）与 arXiv:2601.19239（Li et al.）** | §4.7(c) 与成本线索，**子调研亦未独立核验**，全部转述自检索摘要 | 读正文 |
| 18 | ⛔ **arXiv:2607.03691, *Don't Blame the Large Language Model: How Scaffolding Evolution Shapes Coding Agent Quality*** | **方向可能与 §4 全部结论相反**（主张脚手架才是主因）。若属实，这是我们必须正面处理的反方证据，不能装作没看见 | 仅从检索摘要看到，**优先补读** |

### 6.3 未收获的方向（记录下来避免重复劳动）

1. **RE / MODELS 会议 + 开源小模型 + 需求/状态机建模**：多次检索接近零命中。最接近的是 InstruBPM（BPMN，preprint）与 Sirin（PROFES workshop 分册），以及搜索摘要中出现的 Ferrari/Abualhaija/Arora MODRE 2024 requirements-to-UML（**未核验**）。
2. **「SE 论文明确批评弱基线 / 稻草人」这一体裁**：没找到。FORGE 2026 那篇 prompt 报告规范是最接近的替代品，但它谈的是报告透明度而不是基线强度。
3. **明确用「非劣性检验」（non-inferiority test）这一统计框架的 SE 论文**：没找到。Su & McMillan 与 Caumartin 都是「未发现显著差异」而不是正式的非劣性设计——⚠️ **「未拒绝原假设」不等于「证明了等价」**。如果我们要走这条路，应当用正式的等价性/非劣性检验（如 TOST）并预先声明边界值 δ。
4. **给出质量维度「够用阈值」的 SE 论文**：一篇都没有（见 §2 末尾）。所有「够用」论证都落在成本与部署侧。
5. **在 2026 年前沿模型上做 self-refine / 迭代反馈逐组件消融 + token 成本记账的 SE 实证**：一篇都没有（见 §4.9）。⚠️ 但「没找到」不等于「不存在」，主张这个空缺之前必须先做 venue 级扫库。
6. ⛔ **反方证据尚未处理**：[arXiv:2607.03691](https://arxiv.org/abs/2607.03691) 可能主张脚手架才是决定因素，与 §4 的整体方向相反。**本次未读，下一轮必须优先补读**——只收集支持己方的证据是选择性报告。
