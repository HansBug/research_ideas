# SE 文献的私域部署动机：怎么引出的，是不是承重

> ⭐ **本文件回答 [SUMMARY.md](./SUMMARY.md) 的 Q3**：SE / MDE / RE 文献里别人**怎么引出**「数据保密 → 用本地 / 开源模型」这条动机，⭐ 以及那句话**是承重还是装饰**。⛔ 本文件只放证据与逐篇判定，⛔ 结论回写 [SUMMARY.md](./SUMMARY.md)。

## 0. 一句话结论

⭐ **先例充足，但形态高度一致且有一条硬天花板：本轮读到正文的 19 篇里，没有任何一篇的实证结论依赖那句保密动机——保密永远与「成本」「算力」「可复现性」捆绑成三到四条并列理由，抽掉其中的保密那条，论文的测量、比较与数字一个都不会变。** ⭐ 但**动机层与研究问题层的承重是真实存在的**：TOSEM 2025 的 [2505.16590](https://arxiv.org/abs/2505.16590) 把保密写进 abstract 首句当问题陈述并配了专节 §5.3.2，ICSE-SEIP 投稿 [2511.11125](https://arxiv.org/abs/2511.11125) 直接用它决定了「不用云端专有模型」这一实验设计，[2510.21443](https://arxiv.org/abs/2510.21443) 用它论证「掉 2% F1 是可以接受的」。⭐ 按「≥3 篇把类似论证用作承重」这一档位判据，**若把「问题陈述 / RQ 存在理由 / 设计决策 / 可接受性论证」计为承重，落 A（7 篇）；若严格要求「抽掉后某条实证 claim 崩塌」，落 B（0 篇）**。⭐ 我的建议档位是 **A-**，理由与风险见 §6。

⚠️ ⭐ **本轮还捡到一条对 story 更要紧的反例**，⛔ 它不在原任务清单里但必须上交：ABB 的 [Spec2Control](https://arxiv.org/abs/2510.04519) 处理的是**真·专有**控制叙述（原文：「Such control narratives are proprietary, about intellectual properties, and thus, we cannot publish them.」），⛔ 而它用的是 **Azure AI Foundry 上托管的 GPT-5**。⭐ 也就是说，⛔ 在与我们最接近的工业域里，保密约束的既有解法是**企业云 / 私有端点**，⛔ 不是本地开源小模型。⭐ 详见 §3.3 与 §6.2。

## 1. 逐篇表

⭐ 表中「原句」一律逐字摘自我实际下载并解析的全文（arXiv HTML → 纯文本），⛔ 不是转述；⛔ 未读到全文的条目已在「读到什么程度」列写明。⭐ 位置列使用论文自己的节名。⭐ 承重判定的口径见 §1.1。

### 1.1 承重口径（先定死，再判）

| 记号 | 含义 | 判据 |
| :-: | :-- | :-- |
| **承重-C** | claim 层承重 | ⭐ 抽掉这句话，论文的**某条实证结论或规范性主张**不再成立 |
| **承重-D** | 设计层承重 | ⭐ 抽掉这句话，论文的**某个实验设计选择**（选哪个模型、跑哪个消融）失去理由 |
| **承重-Q** | 问题层承重 | ⭐ 抽掉这句话，论文的**研究问题本身**（为什么研究小模型而不是直接用最强的）失去理由 |
| **装饰** | — | ⛔ 抽掉后**全文任何一处主张、设计与数字都不变**，⛔ 通常只在 intro / discussion 出现一次且无下文 |
| **反例** | — | ⛔ 该文承认保密约束存在，⛔ 但**没有**因此改用本地 / 开源模型 |

### 1.2 主表

| 论文 | 年份 | venue | 原句（逐字） | 位置 | 有无引文 | 承重/装饰 | 链接 | 读到什么程度 |
| :-- | :-: | :-- | :-- | :-- | :-- | :-: | :-- | :-- |
| Zhong et al., *Larger Is Not Always Better: Exploring Small Open-source Language Models in Logging Statement Generation* | 2025 | **TOSEM**（CCF A 刊；DOI 10.1145/3773287） | 「Recent methods emphasize using large language models (LLMs) for automated logging statement generation, but these present **privacy and resource issues, hindering their suitability for enterprise use**.」；「**Privacy Risks.** Sending proprietary code to commercial LLM APIs, such as OpenAI's, risks exposing sensitive intellectual property (Yao et al. 2024). For instance, Samsung banned employee use of ChatGPT and other generative AI tools after an engineer accidentally leaked sensitive source code to ChatGPT (Kharpal 2023).」；「These findings highlight SOLMs as a **privacy-preserving**, efficient alternative for automated logging.」 | **Abstract 第 2 句（问题陈述）** + Introduction 的 bullet「Privacy Risks」 + **专节 §5.3.2 Privacy and Security** + Abstract 结论句 | ⭐ **有，且是本轮最实的一处**：Yao et al. 2024（LLM 安全综述）、**Kharpal 2023（CNBC，三星禁用 ChatGPT 事件）**、Yang et al. 2024b、Li et al. 2024a | **承重-Q**（⛔ 非承重-C） | [arXiv:2505.16590](https://arxiv.org/abs/2505.16590) · [ACM DL](https://dl.acm.org/doi/10.1145/3773287) | 全文（HTML v3，154k 字符） |
| Fares & Herbold, *Utilizing LLMs for Industrial Process Automation: A Case Study on Modifying RAPID Programs* | 2025 | ⚠️ **arXiv preprint**；作者自述「Submitted to ICSE SEIP 2026」，⛔ **未见录用证据** | 「We show that few-shot prompting approaches are sufficient to solve simple problems in a language that is otherwise not well-supported by an LLM and that is **possible on-premise, thereby ensuring the protection of sensitive company data**.」；「We selected the Llama 3.1 70B model... **We decided against using a proprietary, cloud-based model due to the sensitive nature of data involved.**」 | Abstract 末句 + **§4.1 Overview（方法：模型选型理由）** | ⛔ **无**，纯断言 | **承重-D** | [arXiv:2511.11125](https://arxiv.org/abs/2511.11125) | 全文（HTML v1，57k 字符） |
| Zadenoori, De Martino, Dabrowski et al., *Does Model Size Matter? A Comparison of Small and Large Language Models for Requirements Classification* | 2025 | ⚠️ **arXiv preprint**（2025-10-24）；⛔ 无 comments 字段，⛔ 录用状态待核验（正文结构含 §4 Conclusion **and Roadmap**，形似 NIER/短文） | 「They are typically closed-source and cloud-hosted, which increases the risk of data exposure, as **company requirements constitute confidential assets [9]** and the cloud operates as an external service.」；⭐⭐「Nevertheless, even if the difference is confirmed to be significant by future studies, **we argue that a loss of 2% can be considered acceptable, given the advantages of SLMs in data privacy and resource efficiency.**」；「This suggests that, at least for this RE tasks, **companies can profit for the advantages of SLMs in terms of data privacy and resource demands**.」 | Introduction §1 + **§3 结果讨论（对 RQ 的回答段）** + §4 Conclusion | ⚠️ **有但对不上**：[9] = Ferrari, Dell'Orletta, Esuli, Gervasi, Gnesi et al., *Natural language requirements processing: a 4D vision*, IEEE Software 34(6), 2017。⛔ 该文是 NLP4RE 愿景文，⛔ **不是**保密性调查，⛔ 支撑力弱 | **承重-C**（⭐ 本轮唯一一条 claim 层） | [arXiv:2510.21443](https://arxiv.org/abs/2510.21443) | 全文（HTML v1，28k 字符） |
| Caumartin, Qin, Chatragadda, Panjrolia, Li, Costa, *Exploring the Potential of Llama Models in Automated Code Refinement: A Replication Study* | 2024 | ⚠️ **arXiv preprint**（2024-12-03）；⛔ 无 comments，⛔ 录用状态待核验 | 「While Guo et al.'s study showed promising results, **proprietary models like ChatGPT pose risks to data privacy** and incur extra costs for software projects.」；「First, **concerns about data ownership and privacy would prevent organizations from using this solution in their code review workflow [19]**.」；「Using a third party hosted solution raises concerns related to data privacy, as any request/information sent to the LLM could be leaked.」；「An open-sourced model hosted on a local machine... **preserves data privacy entirely as the code under review is never transmitted to third-parties**.」 | Abstract + Introduction §I（含引文）+ **专节 §VI-C「Deployment of closed-source vs open-source models」** + Conclusion §IX | ⭐ **有**：[18][19][21]（正文引出「data ownership and privacy」「retain data ownership」）；⛔ 未核这三条具体是什么文献 | **承重-Q**（⛔ 三条并列动机之一：隐私 / 版本不稳定 / 付费） | [arXiv:2412.02789](https://arxiv.org/abs/2412.02789) | 全文（HTML v1，67k 字符） |
| Çelikmasat, Özgövde, Aydemir, *Instruction-Tuning Open-Weight Language Models for BPMN Model Generation*（InstruBPM） | 2025 | ⚠️ **arXiv preprint**（2025-12-12）；自述「Under preparation for journal submission」 | 「We address this barrier by investigating whether open-weight large language models, adapted via instruction tuning, can generate high-quality BPMN process models directly from natural language descriptions **in a cost-effective and privacy-preserving way**.」；「Our approach thus utilizes instruction tuning to internalize domain constraints directly into the model parameters, offering a more efficient and permanent solution **for on-premise deployment**.」；「**For teams operating under privacy or cost constraints**, compact instruction-tuned models can be deployed on-premise with near-full precision quality when using medium-bit PTQ.」 | Abstract + Introduction（贡献列表第一、三条）+ §7.1 Implications | ⛔ **无**，纯断言 | **承重-D**（⭐ 量化 / LoRA-α 消融**因 on-prem 而做**）⛔ 但 H1/H2 两条假设都是效果与实用性，⛔ 与隐私无关 | [arXiv:2512.12063](https://arxiv.org/abs/2512.12063) | 全文（HTML v1，98k 字符） |
| Ahmed, Rahman, Wahab et al., *Secret Leak Detection in Software Issue Reports using LLMs* | 2024/26 | **MSR 2026**（CCF B 会，作者自述已录用） | 「**Many organizations are cautious about using third-party large language models for software development due to compliance, data privacy, and high API costs.**」；「**Local deployment removes reliance on external APIs, eliminates variable usage costs, and ensures full control over sensitive data.**」 | **§4 RQ3 的 Motivation 段（整段）** | ⛔ **无** | **承重-Q**（⭐ RQ3 整条因它存在） | [arXiv:2410.23657](https://arxiv.org/abs/2410.23657) | 全文（HTML v3，66k 字符） |
| Matotek, Cassel, Amiruzzaman, Ngo, *Evaluating the Limitations of Local LLMs in Solving Complex Programming Challenges* | 2025 | **CCSC Eastern 2025**（⛔ 非 CCF，教学类小会） | 「However, their cloud-based and proprietary nature raises concerns such as **data privacy, latency, and cost**.」；「These findings expose a persistent gap between **private, cost-controlled LLM deployments** and state-of-the-art proprietary services.」；「This is especially important in settings where **data privacy or limited computing resources are key concerns**.」 | Abstract + Introduction + Conclusion | ⛔ **无** | **承重-Q**（⛔ venue 弱，⛔ 引用价值低） | [arXiv:2509.15283](https://arxiv.org/abs/2509.15283) | 全文（HTML v1，37k 字符） |
| Zadenoori, Dąbrowski, Alhoshan et al., *LLMs for Requirements Engineering: A Systematic Literature Review* | 2025 | ⚠️ **arXiv preprint**（2025-09-14），⛔ 录用状态待核验 | 「While feasible for research purposes, this approach is less realistic in practical industrial settings, **where companies are unlikely to expose sensitive requirements data to third-party services such as OpenAI or Google**. This highlights a gap between experimental studies and real-world adoption, and suggests **a potential need for smaller, locally deployable models or privacy-preserving solutions for LLM4RE applications**.」；「Many studies rely on very large models (>70B parameters), which raises issues of cost, infrastructure, and privacy, and calls for smaller, locally deployable alternatives.」 | **§5.4.3 RQ4.3（LLM 规模分析的解读段）** + 结论建议清单 | ⛔ **无**（⭐ 但同节给出可引的量化背景：GPT 家族占 **57/74 篇（77%）**，LLaMA 9 篇 12%，Mixtral/Mistral 与 CodeLLaMA 各 3 篇 4%） | **承重-Q**（⭐ 对 SLR 而言「建议」就是产物） | [arXiv:2509.11446](https://arxiv.org/abs/2509.11446) | 全文（HTML v1，149k 字符） |
| Tufano, Mastropaolo, Pepe, Dabić, Di Penta, Bavota, *Unveiling ChatGPT's Usage in Open Source Projects: A Mining-based Study* | 2024 | **MSR 2024**（CCF B 会，已录用） | 「Also, **practitioners may be afraid to prompt ChatGPT with sensitive, market-competition-related information.**」；「...approaches to support the use of **third-party LLMs on private code or other software artifacts**.」；「**Avoid exposing internal artifacts to the outside**, e.g., using Retrieval Augmentation Generation or similar approaches.」 | §3.x 讨论中的一句旁注 + §5 Implications 的 bullet | ⛔ **无** | **装饰** | [arXiv:2402.16480](https://arxiv.org/abs/2402.16480) | 全文（HTML v1，88k 字符） |
| Sun, Chen, Bissyandé et al.（作者名待核）, *The Future of AI-Driven Software Engineering* | 2024 | **TOSEM**（作者自述已发表） | 「**Data Privacy:** LLMs services like OpenAI have the potential to memorize sensitive or proprietary information and expose it to other users.」；「This is a serious risk, **prompting many companies to use local or private LLM instances to ensure data privacy**.」 | §（挑战/障碍章节）Data Privacy 小节 | ⛔ **无**（⭐ 邻近段落有 LLM 隐私综述引用，⛔ 但不挂在这两句上） | **装饰**（⭐ 愿景文本身无实证 claim 可依赖） | [arXiv:2406.07737](https://arxiv.org/abs/2406.07737) | 全文（HTML v2，88k 字符） |
| Siddiq & Santos, *SALLM: Security Assessment of Generated Code* | 2023/24 | **ASYDE @ ASE 2024** workshop | 「Developers are adopting LLMs for software engineering tasks, but to choose an appropriate model, they have to consider **the privacy of their data**, the accuracy of the generated code, and security.」；「**Open-source models can provide privacy of the data, as they are not shared with the closed model with APIs.**」 | Discussion 的「Implication for the Developers and Researchers」一条 | ⛔ **无** | **装饰** | [arXiv:2311.00889](https://arxiv.org/abs/2311.00889) | 全文（HTML v3，88k 字符） |
| Sallou, Durieux, Panichella, *Breaking the Silence: the Threats of Using LLMs in Software Engineering*（作者名待核） | 2023/24 | **ICSE 2024 NIER** | 「Another significant aspect of concern is privacy. **Closed-source models often lack transparency, making it difficult to assess the privacy implications associated with their usage (Al-Kaswan and Izadi 2023) as well as potential copyright infringements.**」 | §（closed-source models 挑战节） | ⭐ **有**（Al-Kaswan & Izadi 2023） | **装饰**（⛔ 且论题是「研究效度」而非「工业部署」，⛔ 严格说不属于本问题） | [arXiv:2312.08055](https://arxiv.org/abs/2312.08055) | 全文（HTML v2，40k 字符） |
| Koziolek et al.（ABB），*Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs* | 2025 | ⚠️ **arXiv preprint**（2025-10-06） | 「**Such control narratives are proprietary, about intellectual properties, and thus, we cannot publish them.**」；「Function block libraries are also proprietary and **carry company-internal IP**.」；⭐⭐ 而实际用的模型是：「**We use OpenAI LLM models hosted on Azure AI Foundry (currently GPT-5).**」 | §（评测数据说明）+ §（实现说明） | ⛔ **无** | ⛔⛔ **反例** | [arXiv:2510.04519](https://arxiv.org/abs/2510.04519) | 全文（HTML v1，69k 字符） |
| *Evaluating LLMs for Functional and Maintainable Code in Industrial Settings: A Case Study at ASML* | 2025 | **ASE 2025 Industry Track**（CCF A 会工业轨，已录用） | 「However, their applicability in **proprietary industrial settings**, where domain-specific constraints and code interdependencies are prevalent, remains largely unexplored.」 | Abstract + Introduction | ⛔ 无 | ⛔ **不属本问题**（⭐「proprietary」指**研究对象是私有代码库**，⛔ 不是「必须本地部署」） | [arXiv:2509.12395](https://arxiv.org/abs/2509.12395) | 全文（HTML v1，64k 字符）；⛔ 未核其所用模型是否云端 |
| *Leveraging LLMs for Multi-File DSL Code Generation: An Industrial Case Study*（BMW Financial Services） | 2026 | ⚠️ **arXiv preprint** | 「We manually constructed the dataset (**no public dataset exists for this proprietary DSL**).」 | §数据集构造 | ⛔ 无 | ⛔ **不属本问题**（⭐ 同上：专有性只用于解释数据不可公开） | [arXiv:2604.24678](https://arxiv.org/abs/2604.24678) | 全文（HTML v1，62k 字符） |
| Karmarkar, Agrawal, Chauhan, Shete（TCS Research / Synopsys），*Navigating Confidentiality in Test Automation: A Case Study in LLM Driven Test Data Generation* | 2024 | **SANER 2024 Industrial Track**（CCF B 会；DOI 10.1109/SANER60148.2024.00041） | ⛔ **未取得原文，故无逐字原句可引** | ⭐ 保密性**写在标题里** | ⛔ 未核 | ⛔ **仅题录，承重性未判定** | [IEEE Xplore](https://ieeexplore.ieee.org/document/10589904/) · [SANER 2024 程序页](https://conf.researchr.org/details/saner-2024/saner-2024-industrial-track/101/Navigating-Confidentiality-in-Test-Automation-A-Case-Study-in-LLM-Driven-Test-Data-G) | ⛔ **仅程序页题录**（⛔ 该页不含 abstract；⛔ IEEE 全文付费墙；⛔ 无 arXiv 预印本） |

## 2. 承重案例细看

### 2.1 ⭐ 唯一的 claim 层承重：用保密来论证「掉 2% 是可以接受的」

⭐ [arXiv:2510.21443](https://arxiv.org/abs/2510.21443) 做的是小模型（SLM）与商业大模型在**需求分类**上的对比。⭐ 它的实测结果对小模型不利：LLM 领先 2% F1，⛔ 且作者自己承认「the consistent directional advantage for LLM type... might indicate a high probability of Type II error」——⛔ 即差距可能是真实的、只是样本量（8 个模型）不够而没测出显著性。⭐ 关键在于它接下来那一句：

> 「Nevertheless, even if the difference is confirmed to be significant by future studies, **we argue that a loss of 2% can be considered acceptable, given the advantages of SLMs in data privacy and resource efficiency.**」

⭐ 这是本轮**唯一**一处「抽掉保密句、某条主张就不成立」的用法：⛔ 去掉「data privacy」，「2% 可以接受」就只剩下资源效率一条腿，⛔ 而资源效率在需求分类这种低频任务上是弱理由。⭐ **这正是我们 story 需要的那个句式**——⛔ 我们的主臂现在也落后朴素基线（见 [route_selection_and_v47_plan.md](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md)），⭐ 而这篇论文示范了如何用私域部署把一个不利差距论证成可接受。

⚠️ ⛔ **但它的证据链是断的**：那句话唯一挂的引文 [9] 是 Ferrari 等人 2017 年发在 *IEEE Software* 的 *Natural language requirements processing: a 4D vision*，⛔ 那是一篇 NLP4RE 愿景文，⛔ **不是**「企业需求属机密资产」的调查或法规依据。⛔ 也就是说，⛔ 即便是本轮最强的 claim 层承重案例，⛔ 它底下也是**假引文式的断言**。⚠️ ⛔ 该文本身还只是 preprint、录用状态未核，⛔ 不宜作为唯一支柱。

### 2.2 ⭐ 设计层承重：保密直接决定了「用哪个模型」

⭐ [arXiv:2511.11125](https://arxiv.org/abs/2511.11125)（ABB RAPID 机器人程序修改）把保密句放在方法节的模型选型段：

> 「We selected the Llama 3.1 70B model... **We decided against using a proprietary, cloud-based model due to the sensitive nature of data involved.** Moreover, a model with 70B parameters can be used for inference on a single A100, i.e., no complex hardware setup is required by an SME who wants to use this locally within a restricted use case and their own inference server.」

⭐ 这是最干净的承重形态：⛔ 抽掉它，「为什么不直接用 GPT-4」这个问题在方法节就没有答案。⭐ 而且它顺带交出了本轮最有用的一条**工程可行性论据**：70B 单卡 A100 可推理，⭐ SME 不需要复杂硬件。⚠️ ⛔ 但它**无引文**，⛔ 且只是 ICSE SEIP 2026 的**投稿**（arXiv comments 自述），⛔ 未见录用。⛔ 另外注意其 HTML 页眉残留着「The 48th ICSE ... April 12–18, 2025 ... Rio De Janieiro」的模板串，⛔ 与 comments 自述的 2026 冲突，⛔ 属模板未改，⛔ **不得据页眉认定录用**。

### 2.3 ⭐ 问题层承重的标准形态：TOSEM 的写法

⭐ [arXiv:2505.16590](https://arxiv.org/abs/2505.16590)（TOSEM，日志语句生成）是本轮**唯一发在 CCF A 刊、且把保密动机写满四处**的论文，⭐ 它的结构与我们想要的 story 几乎同形：小开源模型（≤14B）经 LoRA + RAG 微调后，⭐ 在专门任务上**超过** GPT-4o / Claude 3.7 Sonnet / DeepSeek-coder-v3 等专有 SOTA。⭐ 它的动机段是这样组织的：

> 「Despite their effectiveness, LLM-based logging tools face several limitations in enterprise settings. • **Privacy Risks.** Sending proprietary code to commercial LLM APIs, such as OpenAI's, risks exposing sensitive intellectual property (Yao et al. 2024). For instance, **Samsung banned employee use of ChatGPT and other generative AI tools after an engineer accidentally leaked sensitive source code to ChatGPT (Kharpal 2023).** • **Style Misalignment.** ...」

⭐ 三点值得学：

1. ⭐ **保密不是孤句，而是一条带编号的 limitation**，⛔ 与 style misalignment 并列，⭐ 再由「fine-tuning 开源大模型需要数千 GPU 小时，对资源受限组织不现实」收口到「所以要小模型」。⭐ 这条推理链是**闭合**的：⛔ 保密 → 不能用云 API；⛔ 算力 → 不能自托管大模型；⭐ 因此 → 小开源模型。⭐ 两条约束**共同**逼出结论，⛔ 缺一条都逼不出来。
2. ⭐ **用一个具名的公开事件做锚**（三星禁用 ChatGPT，引 CNBC 报道 Kharpal 2023），⛔ 而不是空喊「企业关心隐私」。
3. ⭐ **在 Discussion 里给保密单开一节 §5.3.2 Privacy and Security**，⛔ 但那一节**只讲优势、不测量任何东西**——⛔ 全文没有任何数字与隐私相关。

⭐ 所以即便是这篇 CCF A，判定仍是**承重-Q 而非承重-C**：⛔ 抽掉保密，它的所有表格与结论一字不改，⛔ 变的只是「为什么值得研究小模型」这个问题的答案（⭐ 而这个答案还剩「算力/成本」一条腿站着）。

### 2.4 ⭐ MDE 侧的同形先例：InstruBPM

⭐ [arXiv:2512.12063](https://arxiv.org/abs/2512.12063) 是**建模领域**最接近我们的一篇：从自然语言描述生成 BPMN 过程模型，⭐ 用 Qwen3-4B 做 instruction tuning，⭐ 与 GPT-5.1 / Claude-4.5 / Gemini-2.5 对打并在结构保真度（R-GED）上胜出。⭐ 它的隐私句只在 abstract 与 implications 出现，⛔ 无引文；⛔ 且它自陈的**问题**是「practitioners often skip modeling because it is time-consuming and demands scarce expertise」——⛔ **不是**保密。⭐ 保密与成本是并列的限定语（「in a cost-effective and privacy-preserving way」）。

⭐ 但它有一处真承重：⛔ 因为目标是 on-prem，⭐ 它做了**量化位宽（HQQ 2/3/4/5/6/8 bit）与 merge-time α 的系统消融**，⭐ 并把结论写成部署建议（「medium-bit PTQ 保近 BF16 精度」）。⭐ 这组消融**只有在 on-prem 前提下才有意义**——⛔ 走 API 的人不关心量化。⭐ 这给我们一条可抄的路径：**让私域部署前提生出一组只有在该前提下才成立的实验**，⭐ 承重就从「口号」变成「设计」。

## 3. 装饰案例的典型形态

### 3.1 三种形态

⭐ 本轮读到的装饰用法高度模式化，⭐ 只有三种：

| 形态 | 典型位置 | 例子 | 特征 |
| :-- | :-- | :-- | :-- |
| **A. Implication bullet** | Discussion / Implications 的项目符号列表 | MSR'24 Tufano et al.：「**Avoid exposing internal artifacts to the outside**, e.g., using RAG or similar approaches.」 | ⛔ 出现一次，⛔ 面向「future researchers」，⛔ 本文不做 |
| **B. Challenge 清单的一项** | 综述 / 愿景文的挑战章节 | TOSEM《Future of AI-Driven SE》：「**Data Privacy:** ... prompting many companies to use local or private LLM instances」 | ⛔ 与 bias / safety / hallucination 并列，⛔ 每项一两句，⛔ 无下文 |
| **C. 选型建议的一个考量维度** | Discussion 的「对开发者的启示」 | SALLM：「to choose an appropriate model, they have to consider **the privacy of their data**, the accuracy..., and security.」 | ⛔ 与 accuracy / security 并列成三元组，⛔ 不影响本文任何实验 |

### 3.2 ⭐ 装饰与承重的可操作分界线

⭐ 读完 19 篇后，⭐ 我发现一个**只看文档结构就能判**的信号，⛔ 比读措辞可靠：

> ⭐ **看这句话有没有「下游」。** ⭐ 承重的保密句，⭐ 在同一篇论文的**后面某处**会再被用一次——⛔ 用来解释某个模型选型（RAPID）、某组消融（InstruBPM）、某个 RQ 的存在（MSR'26 secret leak）、或某个不利结果的可接受性（需求分类）。⛔ 装饰的保密句**在全文只出现一次**，⛔ 后面再也不回来。

⭐ 这条判据在本轮 19 篇上 100% 一致，⛔ 且它不依赖我对措辞的主观解读，⭐ 可作为后续核验一路的机械复核手段（⛔ 但按仓库 §3.8 与「机械代理只能定位不能裁定」，⛔ 命中后仍须回原文人工确认）。

### 3.3 ⛔ 反例形态：承认保密，但不换模型

⛔ 最值得警惕的不是装饰，⛔ 是**反例**。⭐ ABB 的 [Spec2Control](https://arxiv.org/abs/2510.04519) 做的正是「自然语言需求 → PLC/DCS 控制逻辑（FBD）」，⭐ 与我们「自然语言需求 → 状态机」几乎是同一个工业管线上的相邻工序。⭐ 它的保密约束是**真实且被明说的**：

> 「Such control narratives are **proprietary, about intellectual properties, and thus, we cannot publish them**.」；「Function block libraries are also proprietary and **carry company-internal IP**.」

⭐ 它甚至专门造了 10 份**非专有**的控制叙述来做可公开的评测（「The non-proprietary control narratives enable a transparent test setup outside corporate borders」）。⛔ **然而它的模型是**：

> 「**We use OpenAI LLM models hosted on Azure AI Foundry (currently GPT-5).**」

⛔ 也就是说：⛔ 在一个保密约束确凿成立的真实工业场景里，⛔ 一家工业巨头给出的解法是**企业云托管的专有 SOTA**，⛔ 而不是本地开源小模型。⛔ 它连讨论都没讨论本地部署这个选项。⚠️ ⭐ 这是我们 story 面对的**最强反驳的实证形态**，⛔ 而且它出自最相关的域。⭐ 预答见 §6.2。

## 4. ⭐ 实证 / 调查类证据（量化了这件事的）

⭐ 这一节是附带任务的产出。⭐ 结论：**存在，但都不是「企业禁止把需求 / 代码发给公有云 LLM 的比例」这个数**；⛔ 现有实证测的是相邻的量（开发者的担忧、公司有无政策、有无禁用），⛔ 且样本量都不大。⛔ **本轮覆盖内未见**一篇专门量化「工业组织禁止把设计制品发给第三方 LLM 的比例」的 SE 论文。

| 研究 | 年份 | venue | 样本 | 量化结果（逐字或逐字数字） | 对我们的用处 | 链接 | 读到什么程度 |
| :-- | :-: | :-- | :-- | :-- | :-- | :-- | :-- |
| Klemmer, Horstmann, Patnaik, ... Fahl, *Using AI Assistants in Software Development: A Qualitative Study on Security Practices and Concerns* | 2024 | **ACM CCS 2024**（CCF A 会；DOI 10.1145/3658644.3690283） | **27** 名从业者半结构化访谈（2023-07 至 2024-03，均时 55 分钟）+ Reddit 帖分析 | ⭐「The primary concern among most participants was **leaking sensitive data** when using third-party AI assistants」；⭐「participants were mainly concerned about **leaking proprietary information and code, confidential company data, violating non-disclosure agreements, license agreements, or other contracts**」；⭐「**A few even reported that their companies banned AI assistants by policy, but mainly for privacy reasons**」；⭐ 参与者引语：「if you are having your **local model**... that's the only way that your data is not accessed」；⭐ 使用模式：「**secondary use of Llama when dealing with sensitive information or proprietary code that should not be shared with ChatGPT**」；⛔⛔ **但同时**：「**About half of the participants stated their company did not have a policy regulating the use of AI assistants.**」 | ⭐⭐ **本轮最强、最可引的一条**：⭐ CCF A 会、⭐ 有具名场景、⭐ 明确记录了「因保密而改用本地 Llama」的真实实践。⚠️ ⛔ **双刃**：⛔ 一半公司根本没政策，⛔ 审稿人可以拿这句反打 | [arXiv:2405.06371](https://arxiv.org/abs/2405.06371) · [DOI](https://doi.org/10.1145/3658644.3690283) | 全文（扩展版 HTML v2，141k 字符） |
| Santana, Magalhaes, Santos, *Software Testing with Large Language Models: An Interview Study with Practitioners* | 2025 | ⚠️ **arXiv preprint**（2025-10-20），⛔ 录用状态待核验 | **15** 名测试从业者访谈 | ⭐「**Data Privacy and Security in Test Environments (7/15)**: The use of project specifications or production data to generate test inputs created apprehension about exposing confidential information.」；⭐「Testers stressed that **prompts often include details from internal systems, increasing the risk of data leakage to external APIs**.」；⭐「To preserve confidentiality, they **anonymize test data or operate LLMs on restricted servers**.」；⭐「some participants work in environments where **LLM use is discouraged**」 | ⭐ **唯一给出明确分母的比例**：7/15（46.7%）在测试语境下把数据保密列为主要顾虑；⭐ 且明确记录了「在受限服务器上跑 LLM」这一缓解手段。⛔ n=15 太小，⛔ 只能当定性证据 | [arXiv:2510.17164](https://arxiv.org/abs/2510.17164) | 全文（HTML v1，56k 字符） |
| *Developers' Perceptions on the Impact of ChatGPT in Software Development: A Survey* | 2024 | ⚠️ **arXiv preprint**（2024-05-20，31 页），⛔ 录用状态待核验 | 问卷（⛔ 总 n 未核；⭐ 监管态度题分母 60） | ⭐ 受访者 P101 引语：「**Issues with code sharing. Every time it was necessary to remodel my problem to avoid sharing proprietary code on ChatGPT.**」；⭐「Regarding quality, the primary challenges reported by developers include hallucination, security risks, and **concerns about data privacy**.」；⭐ 支持监管的理由分布：「Social impacts 27% (16/60), Job market 20% (12/60), **Data privacy 20% (12/60)**, Copyright 15% (9/60)...」 | ⭐ 提供一条**具体的规避行为**引语（为避免共享专有代码而重构问题描述），⭐ 很适合当 motivation 的具象例证 | [arXiv:2405.12195](https://arxiv.org/abs/2405.12195) | 全文（HTML v1，106k 字符） |
| Zadenoori, Dąbrowski, Alhoshan et al., LLM4RE SLR | 2025 | ⚠️ arXiv preprint | 74 篇一手研究 | ⭐「The GPT family is by far the most prevalent, cited in **57 of 74 studies (77%)**」；LLaMA **9 (12%)**；BERT **8 (11%)**；Mixtral/Mistral 与 CodeLLaMA 各 **3 (4%)** | ⭐ **量化了「学界几乎不用可私域部署的模型」这个事实**，⭐ 可用来支撑「实验研究与工业落地之间存在缺口」这一句 | [arXiv:2509.11446](https://arxiv.org/abs/2509.11446) | 全文（HTML v1，149k 字符） |
| ⛔ Falcão & Canedo (2024)，78 名从业者调查 | 2024 | ⛔ **未知** | ⛔ 自称 78 名从业者 | ⛔ 二手转述称「开发者尤其担心机密或专有信息泄露，常靠临时性匿名化缓解；缺乏正式培训与明确组织指引」 | ⛔ **若属实则很有用** | ⛔ **无** | ⛔⛔ **仅见二手引用（一篇 *Behaviour & Information Technology* 文章中的转述）；⛔ 未找到一手来源、⛔ 未确认标题与 venue、⛔ 未读任何原文。⛔ 全条待核验，⛔ 不得引用** |

### 4.1 ⭐ 非学术但可引的锚点事件

⭐ 三星 2023 年因工程师把源码贴进 ChatGPT 而全面禁用生成式 AI 一事，⭐ **已经被 TOSEM [2505.16590](https://arxiv.org/abs/2505.16590) 正式引用**（引作 Kharpal 2023，CNBC 报道）。⭐ 这意味着「引一条新闻报道做保密动机的锚」在 CCF A 刊上是**有先例、被接受的**。⭐ 另有 CCS'24 [2405.06371](https://arxiv.org/abs/2405.06371) 引用了 Google、Apple、Samsung 三家的禁用事件（Dastin & Tong 2023；Vigliarolo 2023；Gurman 2023）。⛔ 这些新闻链接本身**不在本轮核验范围**，⛔ 但「已被 A 类论文引用过」这一事实本身可核。

## 5. 检索过程

### 5.1 覆盖的 venue 与年份

| 维度 | 实际覆盖 |
| :-- | :-- |
| **年份窗** | 2023-11 至 2026-08（⭐ 命中集中在 2024–2025） |
| **检索入口** | ⭐ Web 搜索（多轮，⭐ 每轮换关键词簇）+ ⭐ arXiv `abs/` 与 `html/` 直取 + ⭐ ar5iv 回退；⛔ arXiv API（`export.arxiv.org/api/query`）**被限流 429，⛔ 全程不可用**，⛔ 因此**没有做过 arXiv 全库的系统枚举** |
| **命中论文的实际 venue 分布** | **TOSEM** ×2（2505.16590、2406.07737）、**ACM CCS 2024** ×1、**ASE 2025 工业轨** ×1、**MSR 2024** ×1、**MSR 2026** ×1、**ICSE 2024 NIER** ×1、**SANER 2024 工业轨** ×1（⛔ 仅题录）、**ASYDE@ASE 2024 workshop** ×1、**CCSC Eastern 2025** ×1、**arXiv preprint（录用状态未核）** ×9 |
| ⛔ **未直接检索的 venue** | ⛔ **FSE、ISSTA、TSE、EMSE、MODELS、RE、REFSQ、ICSME 的 proceedings 页面一次都没直接翻过**；⛔ 全部命中都是经 Web 搜索与 arXiv 间接到达。⛔ 因此对这些 venue 的「未见」**没有任何证据力** |

### 5.2 关键词簇（实际用过的）

1. `"cannot be shared with third-party" + privacy + "locally deployed" + open-source model + code confidentiality`
2. `"open-source LLM" + "data privacy" + "proprietary code" + cannot use ChatGPT + industrial requirements engineering`
3. `survey practitioners + prohibited/not allowed + send code to ChatGPT + company policy + percentage developers`
4. `"model-driven engineering" OR UML OR "state machine" + LLM + local deployment + privacy + industrial + MODELS`
5. `requirements engineering + industrial case study + "locally deployed" + confidential requirements + Llama/Qwen/Mistral`
6. `"on-premise" OR "self-hosted" + LLM + industrial + Ericsson/Bosch/Siemens/ABB + "cannot be shared"`
7. `SoSyM / MODELS 2025 + "open-weight" OR "small language model" + on-premise + modeling assistant`
8. `title 含 "privacy-preserving" OR "confidential" + LLM + code review / bug report / log analysis + SLM outperform GPT-4`
9. ⭐ 定点追题：`"Navigating Confidentiality in Test Automation"`、`"Larger Is Not Always Better" + logging statement generation`、`Falcão Canedo 78 practitioners`

### 5.3 命中数（口径：本轮实际下载并解析全文的篇数）

| 类别 | 篇数 |
| :-: | :-- |
| ⭐ 下载并解析全文 | **19** 篇（⭐ arXiv HTML → 纯文本，⭐ 逐句正则扫 privacy/confidential/proprietary/on-premise/self-host/third-party 等词族） |
| ⭐ 其中判定与本问题**直接相关** | **13** 篇 |
| ⭐ 承重（含 C/D/Q 三型） | **7** 篇 |
| ⭐ 装饰 | **4** 篇 |
| ⛔ 反例 | **1** 篇（Spec2Control） |
| ⛔ 不属本问题（「proprietary」另指他义） | **2** 篇（ASML、BMW DSL） |
| ⛔ 仅题录、承重性未判定 | **1** 篇（SANER'24 保密性测试数据生成） |
| ⭐ 实证/调查类可用条目 | **4** 条（⛔ 另 1 条 Falcão & Canedo 全条待核验） |

## 6. 覆盖边界与待核验项

### 6.1 ⛔ 覆盖边界（「未见 X」的有效范围）

⛔ 按伞 PR §4.2 第 8 条，⛔ 以下陈述**只在本轮覆盖内成立**，⛔ **不得**写成「不存在」或「据我们所知没有」：

1. ⛔ **在本轮覆盖内未见**任何一篇 SE / MDE / RE 论文，⛔ 其**实证结论**依赖保密动机（即承重-C 中「抽掉后数字或比较结论改变」的那种）。⛔ 找到的唯一 claim 层承重（[2510.21443](https://arxiv.org/abs/2510.21443)）依赖的是一条**规范性**主张（「2% 可接受」），⛔ 不是测量结论。
2. ⛔ **在本轮覆盖内未见**任何一篇量化「工业组织禁止把**需求或设计制品**发给第三方 LLM 服务的比例」的研究。⭐ 最接近的是 CCS'24 的 27 人访谈与测试访谈的 7/15，⛔ 二者测的都不是这个量。
3. ⛔ **在本轮覆盖内未见** MODELS / SoSyM / RE / REFSQ 上把私域部署做成承重的论文。⚠️ ⛔ **但这条几乎没有证据力**——⛔ 我根本没有直接翻过这四个 venue 的 proceedings，⛔ 全靠 Web 搜索间接到达。⛔ 若 R1 需要对 MDE / RE 侧下结论，⛔ **必须补一轮直接翻 proceedings 的检索**。
4. ⛔ **在本轮覆盖内未见**任何论文引用**功能安全标准条款**（ISO 26262 / IEC 61508 / DO-178C 等）来支撑保密动机。⭐ 所有引文要么指向 LLM 安全综述，⛔ 要么指向新闻报道，⛔ 要么根本没有。⭐ 这与 [README.md](./README.md) 里 Q1 的先验判断一致，⛔ 但**这不构成对 Q1 的回答**——⛔ Q1 要查的是标准原文，⛔ 不是文献是否引用它。

### 6.2 ⚠️ 必须随结论一起上交 R1 的两条风险

⭐ **风险 1：企业云端点这条路已经被工业界走了。** ⛔ Spec2Control（ABB）在真实专有控制叙述上用 Azure AI Foundry 的 GPT-5，⛔ 说明「保密 → 必须本地开源小模型」这条推理**中间少了一步**。⭐ 完整的推理必须是：⛔ 保密 → 不能用**公有** API → ⭐ 要么企业云私有端点，⭐ 要么本地部署；⭐ 而选后者需要**额外的**理由（⭐ 完全气隙 / 数据出境限制 / 供应商锁定 / 成本 / 无外网的产线环境）。⛔ 如果 story 只写到「保密所以本地」，⛔ 审稿人一句「Azure OpenAI 有数据不用于训练的合同承诺」就能打穿。⭐ 建议 story 显式补上这一步，⭐ 并把差异化落在**「气隙 / 完全离线」而非泛泛的「隐私」**上——⛔ 企业云挡不住的是「完全不联网」这一条。

⭐ **风险 2：最好的实证证据是双刃的。** ⭐ CCS'24 那篇 27 人访谈是本轮最可引的实证来源，⛔ 但它同一节里写着「**About half of the participants stated their company did not have a policy regulating the use of AI assistants**」。⛔ 引它就等于把这句话一起带进 related work 的射程。⭐ 处理办法有二：⭐ 要么只引「因保密而改用本地 Llama」那条**行为**证据（⛔ 回避政策覆盖率），⭐ 要么如实承认「政策覆盖尚不普遍，⭐ 但**受管制行业 / 特定合同**下的约束是硬的」，⛔ 并把 story 的适用面收窄到后者。⭐ 我倾向后者：⛔ 收窄适用面比被审稿人抓到选择性引用便宜得多。

### 6.3 ⛔ 待核验项清单（交给核验一路）

| # | 待核验内容 | 为什么要核 | 优先级 |
| :-: | :-- | :-- | :-: |
| 1 | ⛔ **Falcão & Canedo (2024)，78 名从业者调查**：标题、venue、DOI、是否真实存在 | ⛔ 我**只见到二手转述**，⛔ 一手来源一次都没找到。⛔ 若不存在则本条必须删 | ⛔ **最高** |
| 2 | ⛔ [2412.02789](https://arxiv.org/abs/2412.02789)（Llama code refinement）是否已录用、录用于何处 | ⛔ arXiv 无 comments 字段；⛔ 它是承重-Q 的重要一例，⛔ preprint 与已录用的引用价值差别很大 | ⛔ 高 |
| 3 | ⛔ [2510.21443](https://arxiv.org/abs/2510.21443)（Does Model Size Matter?）是否已录用 | ⛔ 它是**唯一的 claim 层承重案例**，⛔ 若只是 preprint 则不能当主要支柱 | ⛔ 高 |
| 4 | ⛔ [2511.11125](https://arxiv.org/abs/2511.11125)（RAPID）是否真被 ICSE SEIP 2026 录用 | ⛔ arXiv comments 只说「Submitted」；⛔ 页眉的「48th ICSE, April 2025, Rio」是**未改的模板串**，⛔ 不可当录用证据 | ⛔ 高 |
| 5 | ⛔ SANER 2024《Navigating Confidentiality in Test Automation》的**正文**：保密动机的原句、位置、承重性 | ⛔ 保密写在标题里，⛔ 极可能是本轮最强的承重案例，⛔ 但 IEEE 付费墙、⛔ 无预印本、⛔ 程序页无 abstract | ⛔ 高（⭐ 需机构 IEEE 权限） |
| 6 | ⛔ [2406.07737](https://arxiv.org/abs/2406.07737) 的**作者名单**（我只从内容确认它是 TOSEM 已发表的愿景文，⛔ 未逐一核对作者） | ⛔ 表中作者字段我标了「待核」 | ⛔ 中 |
| 7 | ⛔ [2312.08055](https://arxiv.org/abs/2312.08055)（Breaking the Silence）的**作者名单** | ⛔ 同上，⛔ 表中标了「待核」 | ⛔ 中 |
| 8 | ⛔ [2509.12395](https://arxiv.org/abs/2509.12395)（ASML @ ASE'25 工业轨）**实际用了什么模型**（云端还是本地） | ⭐ 若这家做光刻机的公司也用云端 SOTA，⛔ 那它就是**第二个反例**，⛔ 会显著加重 §6.2 的风险 1 | ⛔ 中 |
| 9 | ⛔ [2510.21443](https://arxiv.org/abs/2510.21443) 的引文 [9]（Ferrari et al. 2017, IEEE Software）**是否真的支撑「企业需求属机密资产」** | ⭐ 我据标题与文献类型判断它不支撑，⛔ 但未读原文 | ⛔ 中 |
| 10 | ⛔ TOSEM [2505.16590](https://arxiv.org/abs/2505.16590) 引的 Kharpal 2023（CNBC 三星报道）链接是否有效 | ⭐ 这是「新闻报道可作 A 刊引文」的证据锚 | ⛔ 低 |

## 7. ⭐ 对 Q3 的落档建议

⭐ 按 [SUMMARY.md](./SUMMARY.md) §1 的档位判据（「SE 文献里有 ≥3 篇把类似论证用作**承重**」）：

| 口径 | 承重篇数 | 落档 |
| :-- | :-: | :-: |
| ⭐ **宽口径**（问题层 / 设计层 / claim 层都算承重） | **7**（2505.16590、2511.11125、2510.21443、2412.02789、2512.12063、2410.23657、2509.15283）⭐ 另 2509.11446 作为 SLR 的建议层承重 | ⭐ **A** |
| ⛔ **严口径**（只有抽掉后**实证结论**改变才算承重） | **0** | ⛔ **B** |
| ⭐ **中口径**（要求「该句在全文有下游用途」，⭐ 即 §3.2 的判据） | **7**，⭐ 其中发表于 CCF A/B 正式 venue 的有 **2**（TOSEM 2505.16590、MSR'26 2410.23657），⛔ 其余为 preprint 或弱 venue | ⭐ **A-** |

⭐ **我的建议：落 A-，并附一条硬约束。**

⭐ 理由：⭐ 先例**确实存在且形态清晰**（⛔ 不是 C 档的「无先例」），⭐ 且其中一篇发在 CCF A 刊（TOSEM）上、⭐ 结构与我们想做的 story 同形（⭐ 小开源模型在专门任务上打赢专有 SOTA，⭐ 以私域部署 + 成本为动机）。⛔ 但**没有任何先例把它做成实证承重**，⛔ 所以：

> ⛔ **story 可以把私域部署写成动机层的正式前提并引文献，⛔ 但不得让任何实验结论、指标口径或比较判据依赖它。** ⭐ 承重的正确落点是**研究问题的存在理由**（「为什么研究小模型而不是直接用最强的」）与**实验设计的选择理由**（⭐ 像 InstruBPM 那样，⭐ 让 on-prem 前提生出一组只有在该前提下才有意义的消融），⛔ 而**不是**结论本身。

⚠️ ⛔ 这条约束比 B 档更严的地方在于：⛔ B 档只说「不得让 claim 依赖它」，⭐ 而 A- 额外要求**必须给它配下游**——⛔ 一句写在 intro 就再也不回来的保密句，⛔ 按 §3.2 的判据会被审稿人一眼认成装饰，⛔ 反而不如不写。

---

## §References

⭐ 按本文首次引用顺序编号。⭐ 所有条目均给出可点击链接。⚠️ ⛔ 标「待核验」者见 §6.3。

**承重案例**

[1] Zhong, R., Li, Y., Yu, G., Gu, W., Kuang, J., Huo, Y., Lyu, M. R. (2025). *Larger Is Not Always Better: Exploring Small Open-source Language Models in Logging Statement Generation.* ACM Transactions on Software Engineering and Methodology (TOSEM). DOI: [10.1145/3773287](https://dl.acm.org/doi/10.1145/3773287) · arXiv: [2505.16590](https://arxiv.org/abs/2505.16590)

[2] Fares, S., Herbold, S. (2025). *Utilizing LLMs for Industrial Process Automation: A Case Study on Modifying RAPID Programs.* arXiv preprint（⛔ 作者自述投稿 ICSE SEIP 2026，⛔ 录用状态待核验）. arXiv: [2511.11125](https://arxiv.org/abs/2511.11125)

[3] Zadenoori, M. A., De Martino, V., Dabrowski, J., et al. (2025). *Does Model Size Matter? A Comparison of Small and Large Language Models for Requirements Classification.* arXiv preprint（⛔ 录用状态待核验）. arXiv: [2510.21443](https://arxiv.org/abs/2510.21443)

[4] Caumartin, G., Qin, Q., Chatragadda, S., Panjrolia, J., Li, H., Costa, D. E. (2024). *Exploring the Potential of Llama Models in Automated Code Refinement: A Replication Study.* arXiv preprint（⛔ 录用状态待核验）. arXiv: [2412.02789](https://arxiv.org/abs/2412.02789)

[5] Çelikmasat, G., Özgövde, A., Aydemir, F. B. (2025). *Instruction-Tuning Open-Weight Language Models for BPMN Model Generation.* arXiv preprint（自述 under preparation for journal submission）. arXiv: [2512.12063](https://arxiv.org/abs/2512.12063)

[6] Ahmed, S., Rahman, M. N., Wahab, Z., et al. (2024/2026). *Secret Leak Detection in Software Issue Reports using LLMs: A Comprehensive Evaluation.* Mining Software Repositories (MSR) 2026（作者自述已录用）. arXiv: [2410.23657](https://arxiv.org/abs/2410.23657)

[7] Matotek, K., Cassel, H., Amiruzzaman, M., Ngo, L. (2025). *Evaluating the Limitations of Local LLMs in Solving Complex Programming Challenges.* CCSC Eastern 2025. arXiv: [2509.15283](https://arxiv.org/abs/2509.15283)

[8] Zadenoori, M. A., Dąbrowski, J., Alhoshan, W., et al. (2025). *Large Language Models (LLMs) for Requirements Engineering (RE): A Systematic Literature Review.* arXiv preprint（⛔ 录用状态待核验）. arXiv: [2509.11446](https://arxiv.org/abs/2509.11446)

**装饰案例**

[9] Tufano, R., Mastropaolo, A., Pepe, F., Dabić, O., Di Penta, M., Bavota, G. (2024). *Unveiling ChatGPT's Usage in Open Source Projects: A Mining-based Study.* 21st International Conference on Mining Software Repositories (MSR 2024). arXiv: [2402.16480](https://arxiv.org/abs/2402.16480)

[10] （作者待核）(2024). *The Future of AI-Driven Software Engineering.* ACM Transactions on Software Engineering and Methodology (TOSEM)（arXiv comments 自述已发表）. arXiv: [2406.07737](https://arxiv.org/abs/2406.07737)

[11] Siddiq, M. L., Santos, J. C. S.（作者部分待核）(2023/2024). *SALLM: Security Assessment of Generated Code.* 6th International Workshop on Automated and verifiable Software sYstem DEvelopment (ASYDE) @ ASE 2024. arXiv: [2311.00889](https://arxiv.org/abs/2311.00889)

[12] （作者待核）(2023/2024). *Breaking the Silence: the Threats of Using LLMs in Software Engineering.* ICSE 2024, NIER track. arXiv: [2312.08055](https://arxiv.org/abs/2312.08055)

**反例与边界案例**

[13] Koziolek, H., Braun, T., Ashiwal, V., Linsbauer, S., Hansen, M. A., Grotterud, K. (2025). *Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs — A Multi-Plant Evaluation.* arXiv preprint. arXiv: [2510.04519](https://arxiv.org/abs/2510.04519)（⭐ 作者名单已从 arXiv 元数据核实；⛔ ABB 归属系据正文对 ABB 工具链与专有函数块库的第一人称叙述推断，⛔ 未逐一核对 affiliation 字段）

[14] （作者待核）(2025). *Evaluating Large Language Models for Functional and Maintainable Code in Industrial Settings: A Case Study at ASML.* 40th IEEE/ACM International Conference on Automated Software Engineering (ASE 2025), Industry Track. arXiv: [2509.12395](https://arxiv.org/abs/2509.12395)

[15] （作者待核）(2026). *Leveraging LLMs for Multi-File DSL Code Generation: An Industrial Case Study.* arXiv preprint. arXiv: [2604.24678](https://arxiv.org/abs/2604.24678)

**仅题录**

[16] Karmarkar, H., Agrawal, S., Chauhan, A., Shete, P. (2024). *Navigating Confidentiality in Test Automation: A Case Study in LLM Driven Test Data Generation.* IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER 2024), Industrial Track, pp. 337–348. DOI: [10.1109/SANER60148.2024.00041](https://doi.org/10.1109/SANER60148.2024.00041) · [IEEE Xplore](https://ieeexplore.ieee.org/document/10589904/) · [SANER 2024 程序页](https://conf.researchr.org/details/saner-2024/saner-2024-industrial-track/101/Navigating-Confidentiality-in-Test-Automation-A-Case-Study-in-LLM-Driven-Test-Data-G)

**实证 / 调查类**

[17] Klemmer, J. H., Horstmann, S. A., Patnaik, N., Ludden, C., Burton Jr., C., Powers, C., Massacci, F., Rahman, A., Votipka, D., Lipford, H. R., Rashid, A., Naiakshina, A., Fahl, S. (2024). *Using AI Assistants in Software Development: A Qualitative Study on Security Practices and Concerns.* ACM SIGSAC Conference on Computer and Communications Security (CCS 2024). DOI: [10.1145/3658644.3690283](https://doi.org/10.1145/3658644.3690283) · arXiv（扩展版）: [2405.06371](https://arxiv.org/abs/2405.06371)

[18] Santana, M. D., Magalhaes, C., Santos, R. de S. (2025). *Software Testing with Large Language Models: An Interview Study with Practitioners.* arXiv preprint（⛔ 录用状态待核验）. arXiv: [2510.17164](https://arxiv.org/abs/2510.17164)

[19] （作者待核）(2024). *Developers' Perceptions on the Impact of ChatGPT in Software Development: A Survey.* arXiv preprint（⛔ 录用状态待核验）. arXiv: [2405.12195](https://arxiv.org/abs/2405.12195)

[20] ⛔ **待核验，不得引用。** Falcão, ?, Canedo, E. D.（?）(2024). *（标题未知）* —— 一项自称覆盖 78 名软件从业者的 LLM 风险调查。⛔ 本轮**只见到二手转述**（出现在一篇 *Behaviour & Information Technology* 期刊文章对相关工作的概述中），⛔ 未找到一手来源、⛔ 未确认标题、venue、DOI 或其是否真实存在。
