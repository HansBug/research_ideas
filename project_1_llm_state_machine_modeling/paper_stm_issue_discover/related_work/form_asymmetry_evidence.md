# 两臂输出形态不同故直接比较不公平 —— 文献佐证（2026-08-12 调研）

**性质**：⭐ 这是一份**文献证据留存**文件。⛔ 不在此处下裁定；⭐ 要用就回这里核，⛔ 不要把数字复述到别处。

⚠️ **核验口径**：每条都读过原文或完整摘要 + 关键结论后才写入；⛔ 只看标题的候选一律未写入。⭐ 逐条标注了「读到什么层级」：**取正文数字** / **仅摘要页** / **⛔ 未独立复核**。

---

## 0. 要论证的命题

一篇论文两个实验臂：

- **方法臂**产出**结构化、可机械求值的断言**（绑定到具体模型元素、有确定真值、可重放）。
- **基线臂**产出**自由文本散文**（「这里语义不清」「命名可能造成歧义」）。

两者用同一指标比较：「有没有指出同一处缺陷」（人工语义判定）。**结果基线臂更高。**

⭐ 要论证：**该指标对两种输出形态系统性不同质 —— 对散文宽容、对形式化断言严格，因此直接比较本身不公平。**

⛔⛔ **命题已被内部实测收窄（2026-08-12 补记）—— ⭐ 读本文件任何一条证据之前先读 **§7.0**。** ⚠️ 简述：（1）⛔ 「基线的发现不可机械求值」**已被我们自己证伪**（可断言率基线 **98.4%** / 主臂 **99.2%**，差 **0.8pp**），⭐ 故能主张的只剩「基线的发现**尚未被**形式化，方法臂的**已经是**」；（2）⛔ 「尺子对散文更宽松」**解释不了**观察到的 14.9pp（⭐ 两臂各有 14.6% 与 29.6% 的独有命中，⭐ 是能力正交的形状）。⛔ **上面那句黑体是本文件的原始出发点，⛔ 不是当前可主张的结论。**

⚠️ **与既有文件的分工**：[assertion_output_form_evidence.md](./assertion_output_form_evidence.md) 已建立「六种输出形态 × 五个维度」证据表，回答的是**「可机械求值断言」这种形态本身有什么已建立的性质**。⛔ 本文件不重复它，⭐ 只回答一件它没回答的事：**把两种形态放到同一把尺子下比较时，那把尺子本身是否偏斜。** ⚠️ 两文件有共引（[3] Zheng NeurIPS 2023、[9] Le ICSE 2019），⭐ 但用途不同：那边用它们证明「散文形态不可复算」/「不要用对称统计评价见证式判据」，⭐ 这边用它们证明「尺子对形态敏感」。⛔ 论文里若同时引，须避免让读者以为是两条独立证据。

⚠️ **边界声明（[README.md](./README.md) 护栏二）**：下文 §2 的 [4][5][6] 对象是 LTL、§4 的 [10][11] 对象是 QA，**均在 project_1 的建模对象** $M = (S, E, V, Tr, A)$ **之外**。⭐ 按护栏二，它们只可用于「**形态层的一般性质（层一）**」并**必须在论文里标明对象不是状态机**；⛔ 不得用于关于我们自己断言的规范性主张。

---

## 1. ⭐⭐ 子命题 A：评判对自由文本比对结构化输出更宽松

### A-1 · Thakur et al. 2025 —— ⭐⭐⭐ **本文件最贴合的一条：「一处绑定错」被抓 98.3%，「说得不完整」只被抓 33.9%**

**引用** [1]：Aman Singh Thakur, Kartik Choudhary, Venkat Srinik Ramayapally, Sankaran Vaidyanathan, Dieuwke Hupkes (2025). *Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges.* Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics (GEM²), ACL 2025, pp. 404–430. ⚠️ **ACL workshop，非主会**（ACL 主会为 CCF A，⛔ workshop 不继承该等级）。ACL Anthology: [2025.gem-1.33](https://aclanthology.org/2025.gem-1.33/) · arXiv: [2406.12624](https://arxiv.org/abs/2406.12624)

**读到什么层级**：⭐ **取正文数字**（自行下载 [2025.gem-1.33.pdf](https://aclanthology.org/2025.gem-1.33.pdf) 并提取，逐格核过下表与 leniency bias 定义段）。

**它实际做了什么**：13 个 judge model 评 9 个 exam-taker model 的答案（短答型事实 QA）。除总体一致性外，⭐ 做了一次**按错误类型分解的 recall 分析** —— 即「当答案确实错了，judge 抓不抓得出来」，按答案**错在哪一种形态**分类。另外形式化了 **leniency bias** $P_+$：judge 以 $P_c$ 给出与 ground truth 相同的判定，⭐ 其余样本它以概率 $P_+$ 判成「correct」。

**关键数字**（逐格取自正文 Table 2）：

| 错误类型 | 说明 | 占比 | GPT-4 Turbo recall | Llama-3 70B recall |
| :-- | :-- | :-- | :-- | :-- |
| **Incorrect entity** | 答案指向了**错误的实体** | 86.9% | ⭐ **98.3%** | ⭐ **96.6%** |
| **Under-specified** | 答案**只说了一部分**（原文举例：答 "December" 而正确答案是 "December 20"） | 37.3% | ⛔ **33.9%** | ⛔ **23.3%** |
| Too few entities | 实体给少了 | 2.47% | 80.0% | 60.0% |
| Too many entities | 实体给多了 | 2.7% | 90.1% | 90.1% |

⭐⭐ **这就是形态不对称本身**：**答案精确但有一处绑定指错 → 98.3% 被判为错；答案含混不全 → 只有 33.9% 被判为错，即约 2/3 蒙混过关。** 原文 §5.3 逐字：*"Underspecified and incorrect answers are more challenging"*，§4 的 takeaway 逐字：judges *"[struggle] with under-specified answers and exhibit leniency."*

⭐ leniency bias 侧：原文 §5.4 逐字 *"We observe that $P_+$ for most models is significantly higher than 0.5 …, indicating a tendency of the judge models to evaluate responses as 'correct' when their evaluation criteria are not completely aligned with the provided instructions."* ⚠️ 具体 $P_+$ 逐模型值在 Figure 16a/16b（⛔ 图，⚠️ 我未从图里读数；⛔ **不要引用逐模型 $P_+$ 数值**）。

⭐ 参照系：人类互评 Scott's π = 96.2 ± 1.07（1200 条 QA、3 名标注者），最强 judge 约 π 0.87–0.88，⭐ 且原文强调**percent agreement 不够** —— judges 一致率高仍可与人类分数**差到 5 分**。

**它支撑哪一句**：⭐⭐ 直接支撑「**同一判定者，对「精确但绑定错一处」的输出严格，对「含混不完整」的输出宽松，且严格 / 宽松的比例约为 3 倍**」。⭐ 这正是我们两臂的处境：方法臂的断言绑定到具体元素，⛔ 一处指错即判错；基线臂的散文不指名任何元素，⛔ 从而落在那个 33.9% 的宽容区。

**强度**：⭐⭐ **直接证据（机制层面）**，⭐ 是本文件唯一一条**在同一判定者、同一批数据上量化出「形态决定严格度」**的证据。

**局限**：⚠️（1）⛔ **workshop 论文**，非主会，引用时不宜标成「ACL 2025」而不加限定。（2）⛔ **「under-specified」的操作定义是「实体答不全」（"December" vs "December 20"），⚠️ 不是「散文式含混表述」** —— ⭐ 从前者推到后者是**我们做的类比**，⛔ 论文里必须写明这一步是类比而非文献结论。（3）领域是短答事实 QA，⛔ 与状态机缺陷发现相距远；⚠️ 该领域被刻意选成人类互评极高（π 0.96）的场景。（4）judge 是 LLM，⛔ 我们的判定是人工。（5）$P_+$ 只在图里，⛔ 无可引数值。

### A-2 · Wu & Aji COLING 2025 —— ⭐ **判定者宁要「有事实错误但写得完整」，不要「正确但简短」**

**引用** [2]：Minghao Wu, Alham Fikri Aji (2025). *Style Over Substance: Evaluation Biases for Large Language Models.* COLING 2025 (Proceedings of the 31st International Conference on Computational Linguistics), pp. 297–312. **COLING = CCF B**。ACL Anthology: [2025.coling-main.21](https://aclanthology.org/2025.coling-main.21/) · 早期预印本 arXiv: [2307.03025](https://arxiv.org/abs/2307.03025)

⚠️ **注意 venue**：早期 arXiv 页把它标为 *"Work in progress"* 且**无 venue**；⭐ 正式发表在 **COLING 2025**。⛔ 不要引成 arXiv preprint。

**读到什么层级**：⭐ **取正文数字**（自行下载 arXiv v3 PDF 提取 Table 1；⚠️ venue 另经 ACL Anthology 页独立确认）。

**它实际做了什么**：让 GPT-4 生成同一批问题的**12 种刻意有缺陷的答案变体** —— 正确 / 正确但短（约 50 词）/ 一处轻微事实错 / 若干轻微事实错 / 若干严重事实错 / 拼写错 / 语法错，以及各自的「+ Short」版本。然后由**四类判定者**（crowd 标注者、专家标注者、GPT-4、Claude-1）两两比较，算每个变体的 Elo。

**关键数字**（逐格取自 Table 1，列序 Crowd / Expert / GPT-4 / Claude-1）：

| 变体 | Crowd | Expert | **GPT-4** | **Claude-1** |
| :-- | :-- | :-- | :-- | :-- |
| Correct | 1091 | 1162 | **1482** | 1320 |
| **Correct + Short** | 970 | 1029 | ⛔ **1096** | ⛔ **1052** |
| **One Minor Factual Error** | 1074 | 1137 | ⭐ **1415** | ⭐ **1265** |
| **Several Minor Factual Errors** | 1032 | 1024 | ⭐ **1206** | ⭐ **1182** |
| Several Major Factual Errors | 1025 | 892 | 861 | 979 |

⭐⭐ **GPT-4 把「一处轻微事实错」（1415）与「若干轻微事实错」（1206）都排在「正确但简短」（1096）之上；Claude-1 同样（1265、1182 vs 1052）。** 原文 §1 逐字：*"we see judges preferring factually incorrect models over grammatically incorrect or short ones"*；另一条逐字：*"Human judges generally do not thoroughly fact-check answers unless the factual error is glaringly evident."*

⭐ 人类判定者则**犹疑**：crowd 的 Elo 全距只 970–1091、expert 892–1162，⛔ 远窄于 LLM judge。

**它支撑哪一句**：⭐ 支撑「**判定分数主要由「说得完整、说得像样」驱动，而非由「说得对」驱动**；一个内容有错但形态饱满的回答，可以稳定地压过一个正确但形态精简的回答」。⭐ 类比到两臂：基线臂的散文形态饱满（一段自然语言总能读起来「有内容」），⛔ 方法臂的断言形态精简（一条谓词调用 + 一个绑定 + 一个真值）。

**强度**：⭐ **强类比证据**。⛔ 它的自变量是「事实错 / 简短 / 语法错」，⚠️ **不是「散文 vs 形式化」** —— ⭐ 我们借的是「形态饱满度压过正确性」这个机制。

**局限**：⚠️（1）缺陷是**人工注入**的合成变体，⛔ 非自然产生。（2）⛔ **"Short" 把「简短」与「信息量减少」混在一起** —— ⚠️ 因此严格说它测的是长度 / 信息量偏置，⛔ 不是「含混被宽容」。（3）只有 2 个 LLM judge，且都是 2023 年模型（gpt-4-0613、Claude-1.3）。（4）⭐ 人类判定者上的效应**弱得多**（expert 把 Correct 1162 排在 One Minor Factual Error 1137 之上）—— ⚠️ ⛔ **而我们的判定是人工，所以这一条对我们的适用性打折**。

### A-3 · Zheng et al. NeurIPS 2023 —— 冗长偏置的经典量化，⚠️ 仅作机制旁证

**引用** [3]：Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023, Datasets and Benchmarks Track. **NeurIPS = CCF A**。[proceedings 页](http://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) · arXiv: [2306.05685](https://arxiv.org/abs/2306.05685)

**读到什么层级**：⚠️ ⛔ **本轮未重取原文** —— ⭐ 该篇的数字已在 [assertion_output_form_evidence.md](./assertion_output_form_evidence.md) §2.3 结论 7 处逐条核过（含 S1/S2 口径之分、冗长攻击失败率、位置一致性）。⛔ 本条不新增数字，⚠️ 引用前回那份文件核。

**它实际做了什么 / 关键数字**（转引自上述已核记录）：**「重复列表」攻击** —— 取 23 条含编号列表的 MT-bench 答案，让 GPT-4 把每项**改写但不新增信息**，再把改写版前置（5 项 → 10 项）。判定者偏好这个「信息量不变、只是更长」的版本的失败率：**Claude-v1 91.3%**、GPT-3.5 91.3%、GPT-4 8.7%。位置一致性（默认 prompt）：Claude-v1 **23.8%**、GPT-3.5 46.2%、GPT-4 65.0%。

**它支撑哪一句**：⭐ 只支撑较弱的一句：「**信息量完全不变、只改变表述形态，就能系统性地改变判定结果**」。

**强度**：⚠️ **仅相关 / 弱类比**。⛔ 冗长 ≠ 含混；被填充的内容是**冗余**而非**模糊**。⛔ 不要拿它当承重引用。

**局限**：⚠️（1）2023 年模型。（2）⛔ 说的是长度，⚠️ 完全不涉及「精确形式化输出被过度惩罚」。（3）⭐ GPT-4 本身只 8.7% 失败 —— ⛔ 即强模型基本免疫，⚠️ 不能写成「LLM judge 普遍被冗长骗到」。

### A-4 · Bharadwaj et al. ICLR 2026 —— ⭐⭐ **含混偏好的机制被点名：「不可证伪，故不被惩罚」**；⭐ 且它是子命题 A 唯一的**正式发表**支撑

**引用** [16]：Anirudh Bharadwaj, Chaitanya Malaviya, Nitish Joshi, Mark Yatskar (2026). *Flattery, Fluff, and Fog: Diagnosing and Mitigating Idiosyncratic Biases in Preference Models.* ICLR 2026（⭐ **Poster，已接收** —— ⭐ 经 OpenReview API 核 `venue = "ICLR 2026 Poster"` / `venueid = ICLR.cc/2026/Conference`，forum [tsfjjfhEz7](https://openreview.net/forum?id=tsfjjfhEz7)）。⚠️ **ICLR 不在 CCF 推荐目录内**（⭐ 机器学习顶会，⛔ 但不得标 CCF A）。arXiv: [2506.05339](https://arxiv.org/abs/2506.05339) v3

**读到什么层级**：⭐ **取正文数字**（读 arXiv v3 HTML 全文 + OpenReview 元数据与 bibtex）。⛔ ⚠️ **逐 bias 的 skew / 相关系数只在 Figure 2/3/4/5 的图片里，⛔ 未取到** —— ⛔ 故**不得引用「vagueness 的人类 vs 模型 skew 差」**这类逐项对比数字。

**它实际做了什么**：针对偏好模型 / reward model 的五种表面特征偏好 —— length、structure、jargon、sycophancy、**vagueness** —— 用**受控反事实对**（同一 query 放大某一特征，⭐ 且改写要求长度大致相等以隔离 verbosity）量化 **skew**（模型偏好被放大侧的比例）与 **miscalibration**（相对人类偏好的失配率）。

**关键数字**（⭐ 仅取正文 / 表格 / 附录 D 中以文字给出的）：

| 量 | 数值 |
| :-- | :-- |
| 五 bias 合计 skew | $> 60\%$ |
| 五 bias 合计 miscalibration | $\approx 40\%$ |
| 与**人类**标签相关 | mean $r_{\mathrm{human}} = -0.12$ |
| 与**强 reward model** 标签相关 | mean $r_{\mathrm{model}} = +0.36$ |
| ⭐ **vagueness** 的 miscalibration | ⭐ **与 jargon 并列最高，$> 50\%$** |
| ⭐ **vagueness** 的 skew（去偏前） | ⭐ **约 61%** |
| **vagueness** 的 CDA 去偏幅度 | skew $-29.8$ 点，95% CI $[-43.2, -16.5]$ —— ⭐ 五者最大 |
| ⛔ **vagueness 的人类 skew** | ⛔ **原文未给数字**（只给 length 33.7% / jargon 20.9%） |

⭐⭐ **本条最有价值的不是数字，是作者给出的机制**，逐字：*"This may stem from vague statements being less falsifiable, and thus less penalized in training data."* ⭐ 即**含混之所以不被惩罚，正因为它不可证伪** —— ⭐ 这恰是子命题 A 需要的因果链，⭐ 且由一个与我们无关的任务上的独立工作提出。

⭐ vagueness 的操作化也贴合：偏好「做出**宽泛陈述、多方面浅覆盖**」而非「具体、针对该 query 的信息」；⭐ 数据是 78 条 KIWI 人写 NLP query + 22 条新造 = 100 条。

**它支撑哪一句**：⭐ 支撑「**判定者可系统性偏爱不可证伪的表述，⭐ 且机制是「不可证伪 → 不被惩罚」**」。⭐⭐ 它与 [1] 互补：[1] 给**量**（98.3% vs 33.9%），⭐ 本条给**因**。

**强度**：⭐ **弱到中等类比证据**，⛔ 不可单独承重。⭐ 但它有两点是 [1] 没有的：（1）⭐ **正式发表**（⛔ [1] 是 workshop、[14][15] 是 arXiv-only）；（2）⭐ 它把 vagueness 与 **falsifiability** 直接挂钩 —— ⭐ 而「可证伪」正是我们方法臂断言的定义性属性。

**局限**：⚠️（1）⛔⛔ **对象是偏好模型对「哪个回答更好」的通用质量排序，⛔ 不是「这条 issue 有没有指出台账那条缺陷」** —— ⚠️ 后者有外部真值，⛔ 前者没有，⛔ 偏斜机制不可假定相同。（2）⛔⛔ **vagueness 一项的标注者是作者本人**（3 名 expert labeler；⛔ 其余四项用 Prolific 300 人众包）—— ⚠️ 它是五项里**唯一无独立标注**的一项，⛔ 而恰是我们唯一想引的那项；⭐ 一致性 85.7%（五项最高）可部分缓解，⛔ 不能消除。（3）⛔ 逐 bias 图表未取到（见上）。（4）判定者是偏好模型，⛔ 我们是人工。（5）⚠️ **它与 [15] 表面冲突**（[15] 说对冲语气**被罚** 25.6%）—— ⭐ 二者可共存：[16] 的 vagueness 是**内容层的宽泛**，[15] 的 hedging 是**语气层的对冲**。⛔ 这正是 §7.3 第 2 行要求的那个区分，⭐ 本条为它提供了正式发表的支撑侧。

---

## 2. ⭐⭐ 子命题 B：「能用自然语言指出问题」与「能把它形式化」之间存在已知的可量化差距

⭐ **这是本论证最重要的一支** —— 它直接支撑「散文命中 ≠ 可执行的发现」。

### B-1 · Greenman et al. 2023 —— ⭐⭐ **全库最干净的方向不对称量化：同一批人、同一批内容，「读懂并用英语说出来」的错误率约为「写成形式化」的一半**

**引用** [4]：Ben Greenman, Sam Saarinen, Tim Nelson, Shriram Krishnamurthi (2023). *Little Tricky Logic: Misconceptions in the Understanding of LTL.* The Art, Science, and Engineering of Programming 7(2), 7:1–7:37. ⚠️ **非 CCF 目录内 venue**（`<Programming>` 期刊；有 artifact evaluation，形式化方法社区高引）。arXiv: [2211.01677](https://arxiv.org/abs/2211.01677) · PDF: [arxiv.org/pdf/2211.01677](https://arxiv.org/pdf/2211.01677)

**读到什么层级**：⭐ **取正文数字**（自行下载 PDF 提取 §7 / §8 / Table 5a / 5b 与摘要）。

**它实际做了什么**：跨两年做四轮研究（三轮书面问卷 + 一轮 talk-aloud），把「理解 LTL」拆成三个方向，其中两个是**同一内容的双向翻译**：`ltl ⊲ Eng`（读一个 LTL 公式，用英语说出它的意思）与 `Eng ⊲ ltl`（读一段英语需求，写出 LTL 公式）。Round 3 的被试是**该领域的 leading researchers**（原文用作 baseline），Round 2 是学习者，Round 4 是 talk-aloud。LTL 答案用**语义等价自动判定**（⛔ 不是字符串比对），英语答案用两名 coder 编码。

**关键数字**（逐字取自 §7 与 §8）：

| 方向 | Round 2（学习者） | Round 3（**领域研究者**） | Round 4（talk-aloud） |
| :-- | :-- | :-- | :-- |
| `ltl ⊲ Eng`（形式化 → 英语） | 23% 错 | **15% 错** | 24% 错 |
| `Eng ⊲ ltl`（英语 → 形式化） | ⭐ **47% 错** | ⭐ **28% 错** | ⭐ **47% 错** |

§8 逐字：*"The error rates are much higher than for the previous questions: 47 % of the Round 2 responses, 28 % of the Round 3 responses, and 47 % of the Round 4 responses were incorrect."* 摘要逐字：*"We also find that the English to ltl direction was the most common source of errors; unfortunately, this is the critical 'authoring' direction in which a subtle mistake can lead to a faulty system."* §7 的 Key Takeaway 反过来说 `ltl ⊲ Eng`：*"In general, subjects did well at this task."*

⭐ **三轮里错误率都恰好约 2 倍，且在领域专家身上依然是 2 倍（15% vs 28%）** —— ⛔ 因此不能归因为「被试不熟练」。

**它支撑哪一句**：⭐⭐ 直接支撑「**同一份语义内容，用自然语言表述与用形式化表述，正确率不是同一个量级**」。即：能用散文正确指出一件事，**不代表**能把同一件事形式化正确；反向失败率约两倍。⭐ 推到两臂：基线臂做的是「低失败率的那个方向」，方法臂做的是「高失败率的那个方向」，⛔ 而指标不区分。

**强度**：⭐⭐ **直接证据（就形态不对称这一点而言）**，⛔ 但对象是人不是 LLM、是翻译任务不是缺陷发现任务。⭐ 它是我找到的**唯一一个把同一内容的两种表述形态放在同一批被试、同一套判定下对比**的研究 —— ⭐ 这正是「同一指标下两种形态不同质」所需要的实验结构。

**局限**：⚠️（1）⛔ **对象是 LTL，越界** —— ⭐ 按护栏二只可用于层一并标明对象。（2）被试是人，⛔ 不是 LLM。（3）⛔ 测的是**翻译**（内容已给定），⚠️ 不是「发现」。（4）英语侧判定靠人工编码，原文自陈可能误标（*"our two-coder method may have mislabeled some written responses"*）。（5）错误分类由单一 coder 完成（原文自陈）。

### B-2 · English et al. 2025（VLTL-Bench）—— ⭐⭐ **「抽象层说对」到「绑定到具体元素说对」之间掉 40–54 个百分点**

**引用** [5]：William H. English, Chase Walker, Dominic Simon, Sumit Kumar Jha, Rickard Ewetz (2025). *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite.* ⛔ **arXiv preprint，无同行评审 venue**（arXiv:2507.00877，v1 2025-07-01 / v2 2025-12-18；eess.SY，cross-list cs.CL）。URL: [arxiv.org/abs/2507.00877](https://arxiv.org/abs/2507.00877)

**读到什么层级**：⭐ **取正文数字**（读 v2 全文 HTML 的 Table 4、grounding 表、end-to-end 表）。⚠️ 引用须钉版本（v1→v2 有修订）。

**它实际做了什么**：指出既有 NL→TL 基准**只测 lifted translation**（公式里原子命题是抽象占位符），从而把 **grounding**（把占位符绑定到真实状态空间里的具体变量）这一步免费送给系统。他们造 VLTL-Bench：4 个状态空间 + 数千条 NL–TL 对 + 用于验证公式的样例 trace，并在 lifting / grounding / translation / verification 四个子步骤上**各给 ground truth**，从而能分段测。评测 NL2LTL / nl2spec / NL2TL / Lang2LTL × GPT-3.5-turbo / GPT-4o-mini / GPT-4.1-mini / GPT-4o / 微调 t5-base。

**关键数字**（三个新数据集 S&R / Traffic Light / Warehouse）：

| 系统 | lifted translation | ⭐ **end-to-end（含 grounding）** |
| :-- | :-- | :-- |
| NL2TL / Lang2LTL（微调 t5-base） | ⭐ **100.0 / 100.0 / 100.0** | ⛔ **54.4 / 60.1 / 46.2** |
| nl2spec（GPT-4.1-mini） | 89.1 / 91.6 / 88.4 | ⛔ 34.8 / 33.6 / 29.6 |
| NL2LTL（GPT-4.1-mini） | 41.6 / 40.0 / 37.4 | 35.4 / 38.4 / 26.2 |
| Lang2LTL（embedding 检索式 grounding） | — | 58.5 / 72.1 / 37.9 |

grounding 单步准确率（few-shot general prompt，「整份 AP 字典全对」口径）低至 **7.0–7.8%**（Warehouse，80 个 COCO 类）；即使 GPT-4o + few-shot CoT 也只到 61.4%。

⭐ 原文自评逐字：既有基准上是 *"near-perfect performance"*，而那些研究 *"only measure the accuracy of the translation of NL logic into formal TL, ignoring a system's capacity to ground atomic propositions"*；Table 4 的高分是 *"an overconfident estimation of translation performance as grounding is not considered."*

⭐⭐ **一个 lifted 上 100% 的系统，一旦要求绑定到具体元素，掉到 46–54%。**

**它支撑哪一句**：⭐ 直接支撑「**「说出问题所在」与「把它绑定到具体模型元素」是两个难度量级**」。我们的方法臂被要求做后者（断言必须绑到具体 state / event / transition / variable），基线臂只需做前者（「这里语义不清」不指名任何元素）。⭐⭐ 这是本论证与「绑定」这个具体要求**最贴合**的一条。

**强度**：⭐ **强类比证据**。⭐ 实验结构（分段给 ground truth、分离 lifted 与 grounded）与我们要说的事高度同构；⛔ 但它测的是 NL→LTL 翻译系统，⛔ 不是缺陷发现，⛔ 也不涉及「人工语义判定同一指标」。

**局限**：⚠️（1）⛔⛔ **arXiv 预印本，无同行评审** —— 引用时必须标明，⛔ 不宜作为唯一支柱。（2）⛔ 对象是 LTL，越界，同 B-1。（3）它是 benchmark 论文，有把既有工作说低的动机；⭐ 但给的是分段 ground truth 下的可复核数字，⛔ 不是主观评断。（4）Warehouse 的 80 类字典难度可能不代表一般情形。

### B-3 · Cosler et al. CAV 2023（nl2spec）—— 仅作方法论旁证：**形式化本身被该社区当作「易错且耗时」的前提，故设计成人在环**

**引用** [6]：Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, Caroline Trippel (2023). *nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models.* CAV 2023 (vol. 2), pp. 383–396. **CAV = CCF A**。DOI [10.1007/978-3-031-37703-7_18](https://doi.org/10.1007/978-3-031-37703-7_18) · arXiv: [2303.04864](https://arxiv.org/abs/2303.04864)

**读到什么层级**：⚠️ **仅摘要页**（venue / 页码 / DOI 另经 DBLP 独立确认 —— ⚠️ arXiv abs 页**不显示** venue，⛔ 只看 arXiv 会误标成 preprint）。⛔ **本条不得引用任何数字。**

**它实际做了什么**：把 LLM 生成的形式化拆成 sub-translation（每个子公式回指它来自哪段自然语言），让用户 *"iteratively add, delete, and edit these sub-translations to amend erroneous formalizations"*。摘要给出的前提是手写形式规约 *"an error-prone and time-consuming manual task."* 另做 user study 造了一个 challenging dataset。

**它支撑哪一句**：⭐ 只支撑一句较弱的：「**形式化环节被形式化方法社区本身当作独立的、易错的难点**，以至于 CCF A 会议上的方法要专门为它设计人在环纠错机制」—— 即形式化不是「把已知的东西写下来」这么廉价的一步。

**强度**：⚠️ **仅相关**。⛔ 不提供两形态对比数字，⛔ 不要当承重引用。

**局限**：⚠️（1）⛔ 只读到摘要，⛔ 未取正文准确率表。（2）对象是 LTL，越界。（3）它的动机陈述是 related-work 式自我论证，⛔ 不是实测。

### B-4 · Endres et al. FSE 2024（nl2postcond）—— ⭐⭐ **干净基准上形式化 81% 有效，真实代码上只 12.2%**；⭐ 且 venue 最硬

**引用** [7]：Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, Shuvendu K. Lahiri (2024). *Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions?* Proc. ACM Softw. Eng. (PACMSE), FSE 2024 issue; FSE'24, Porto de Galinhas, Brazil, July 15–19, 2024. **FSE = CCF A**。arXiv: [2310.01831](https://arxiv.org/abs/2310.01831)

**读到什么层级**：⭐ **取正文数字**（自行下载 arXiv v2 PDF 提取 §4.1 / §4.2 / §4.2.2 / Table 4 / RQ 摘要框；⚠️ venue 由正文页眉 *"FSE'24, July 15–19, 2024, Porto de Galinhas, Brazil"* 确认）。

**它实际做了什么**：定义 `nl2postcond` 问题 —— 把代码旁的**非形式化自然语言**（docstring / Javadoc / 注释）转成**可程序化检查的 assertion（后置条件）**。用两个指标评：**correctness**（是否忠于文档意图）与 **discriminative power / bug-completeness**（能否拒掉错误实现）。跑 GPT-4 / GPT-3.5 / StarChat，两个基准：EvalPlus（164 个干净的 HumanEval+ 问题，docstring 完整描述）与 Defects4J（525 个真实历史缺陷）。

**关键数字**：

| | EvalPlus（干净基准） | ⛔ Defects4J（真实代码） |
| :-- | :-- | :-- |
| 逐条后置条件 test-set-correct | **77%**（最佳 prompt 变体） | accept@10 至 0.75 |
| 至少一条正确的问题占比 | **96%**（158/164） | — |
| 能区分错误实现的比例 | ⭐ **至多 81%** 平均 | ⛔ GPT-4 至多 **47/525 = 9%** |
| 全部模型 × 全部 prompt 变体合起来 | 杀掉全部 mutant 的例子至多 62.2% | ⛔ **70 个 buggy method / 64 个缺陷 = 全部 525 个的 12.2%** |

⭐ **落差约 7 倍：81% → 12.2%。** ⭐ 作者自己给的原因之一逐字：*"(a) the comments not being completely descriptive, and (b) the increased program and object complexity in Defects4J"*。⭐ 另有一个正面案例（Apache Commons CLI）作者明确写 requirement *"is clearly specified in the Javadoc"*，GPT-4 由此生成的后置条件成功抓到该缺陷 —— ⭐ 即「NL 里写清楚了」时形式化能成，⛔ 而这种情形在 525 个里只占一成多。

⭐ 还有一个对方法臂形态直接有用的细节：他们把后置条件拆成九类原子成分，⭐ 发现**最弱的一类（Type Checks）在自然缺陷上只杀掉 14%**、平均只 27%；⛔ 而最强一类平均杀 **89%**。⭐ 即**同为「形式化断言」，谓词选得对不对决定几十个百分点** —— ⭐ 这支撑我们「谓词选择是方法主体」的立场（⚠️ 与 [../story/paper_story.md](../story/paper_story.md) 的 C-③ 差异化落点一致）。

**它支撑哪一句**：⭐ 支撑「**从自然语言描述到可机械求值断言之间，存在被 CCF A 会议实测过的巨大落差；且该落差在真实（而非基准）制品上放大约一个数量级**」。⭐ 推到两臂：基线臂交付的正是「非形式化自然语言」那一端，方法臂交付的是「可程序化检查的断言」那一端，⛔ 而后者的成功率在文献里从来不等于前者。

**强度**：⭐⭐ **强类比证据，且 venue 最硬（CCF A）**。⭐ 它是本论证里**唯一一条同时满足「CCF A」「2022 年后」「直接测 NL → 可机械求值断言」的证据**，⭐ 建议作主引之一。

**局限**：⚠️（1）⛔⛔ **12.2% 有混淆**：作者自陈部分原因是**注释本身没写全**，⛔ 因此不能把 7 倍落差全部归给「形式化难」；⚠️ 引用时必须写清，⛔ 否则是过度解读。（2）对象是程序后置条件，⛔ 不是状态机制品；⭐ 但它不涉及时钟与并发，属护栏二允许的「层一 + 标明对象」。（3）⛔⛔ **它的主结论是乐观的**（摘要说 *"generally correct and able to discriminate incorrect code"*、*"has the potential to be helpful in practice"*）—— ⛔ **不得把它引成「形式化不行」的证据**；⭐ 我们用的是那个**基准 vs 真实的落差**，⛔ 不是它的主结论。（4）Defects4J 的 9% / 12.2% 是「discriminating w.r.t. regression 与 trigger tests」口径，⛔ 不是「人工判定语义等价」口径。

---

## 3. 子命题 C：报告了问题 ≠ 报告可被下游执行（bug report actionability）

### C-1 · Bettenburg et al. FSE 2008 —— ⭐ 奠基性，且给出**负相关**这个极强数字

**引用** [8]：Nicolas Bettenburg, Sascha Just, Adrian Schröter, Cathrin Weiss, Rahul Premraj, Thomas Zimmermann (2008). *What Makes a Good Bug Report?* FSE 2008 (SIGSOFT '08/FSE-16), pp. 308–318. **FSE = CCF A**。DOI [10.1145/1453101.1453146](https://doi.org/10.1145/1453101.1453146) · 全文 PDF: [thomas-zimmermann.com/publications/files/bettenburg-fse-2008.pdf](https://thomas-zimmermann.com/publications/files/bettenburg-fse-2008.pdf)

**读到什么层级**：⭐ **取正文数字**（自行下载 PDF 提取 §3 / Table 1 / Table 2 / Table 3 / §3.3）。

**它实际做了什么**：向 APACHE / ECLIPSE / MOZILLA 的 2,226 名 developer 与 reporter 发问卷，466 份回复；经一致性检查后剩 developer 130 份（剔 26 = 16.7%）、reporter 215 份（剔 95 = 30.6%）。问 developer「哪些内容你用过 / 哪三项最重要」，问 reporter「你提供过哪些 / 哪三项最难提供」。

**关键数字**（逐项取自 Table 2 / Table 3 / §3.3）：

| 项目 | developer 侧重要性 | reporter 侧难度 |
| :-- | :-- | :-- |
| steps to reproduce | **83%** | 51% |
| stack traces | **57%** | 24% |
| **test cases** | **51%** | ⭐ **75%（最难项）** |
| observed behavior | 33% | 2% |
| expected behavior | 22% | 3% |

⭐⭐ **最强的一个数字**：developer 认为重要的东西 与 reporter 实际提供的东西，**Spearman 相关系数 = −0.035**（§3.3 逐字：*"The Spearman correlation of -0.035 between what developers consider as important and what reporters provide shows a huge gap"*）。而「developer 用过什么 vs reporter 提供什么」是 0.321（原文自评 *"far from being ideal"*）。⭐ 且 Figure 3(c) 说明 **reporter 其实知道 developer 需要什么** —— 逐字：*"ignorance of reporters is not a reason for the aforementioned information mismatch."* ⭐ 即差距不来自「不知道」，而来自「提供不出来」。

⭐ **另一个直接可用的细节**：Table 2 的「Problems with bug reports」栏里，developer 报告的问题严重度包括 **incomplete information 74%**（远超其它）、**unstructured text 34%**、too long text 26%、**prose text 18%**、non-technical language 19%。⭐ 即「散文式表述」本身被 developer 列为一类问题，⛔ 但严重度只 18%，⚠️ **不宜夸大**。

**它支撑哪一句**：⭐ 支撑「**能指出一个问题 ≠ 交付一个可被下游执行的发现**；两者之间的缺口被实测过，且大到相关系数为负」。⭐ 也支撑「最有下游价值的形态（test case / steps to reproduce）恰恰是最难产出的形态」—— ⭐ 这正是两臂的关系：方法臂被要求交付难产出的那种形态。

**强度**：⭐ **类比证据（强）**。⛔ 不是关于 LLM、不是关于状态机、⛔ 也不是关于「同一指标比较两种形态」。⭐ 但它是软件工程里对「报告 ≠ 可执行」这个缺口最经典的量化来源，且 75% vs 51% 的「最有用 = 最难给」倒挂关系与我们的处境同构。

**局限**：⚠️（1）2008 年，前 LLM 时代。（2）问卷法，自我报告。（3）一致性检查剔掉了 30.6% 的 reporter 回复，样本有筛选。（4）⛔⛔ 它测的是「reporter 提供了什么」，**不测「评判者如何给分」** —— ⛔ 因此它支撑不了「尺子偏斜」这一步，⭐ 只支撑「形态之间存在难度落差」。

---

## 4. 子命题 D：评测方法学 —— 不同输出形态用同一指标比较会引入偏差

### D-1 · Le et al. ICSE 2019 —— ⭐⭐ **对称一致性统计会结构性地惩罚「可靠但不完备」的那一方，且惩罚到低于随机**

**引用** [9]：Xuan-Bach D. Le, Lingfeng Bao, David Lo, Xin Xia, Shanping Li, Corina Păsăreanu (2019). *On Reliability of Patch Correctness Assessment.* ICSE 2019, pp. 524–535. **ICSE = CCF A**。DOI [10.1109/ICSE.2019.00064](https://doi.org/10.1109/ICSE.2019.00064) · arXiv: [1805.05983](https://arxiv.org/abs/1805.05983) · 作者 PDF: [xin-xia.github.io/publication/icse192.pdf](https://xin-xia.github.io/publication/icse192.pdf)

⚠️⚠️ **作者更正**：是 **Xuan-Bach D. Le**，⛔ **不是** Claire Le Goues（后者不是本文作者）。⚠️ 引用时别写错。

**读到什么层级**：⚠️ **ICSE 会议页 + 检索到的 Table 5 转录**。⛔ **未亲自打开 PDF 逐格核 Table 5** —— ⭐ 引用前应补这一步。⚠️ 该篇也是 [assertion_output_form_evidence.md](./assertion_output_form_evidence.md) 的 [65]，⛔ 那边同样自陈未逐条人工复验。

**它实际做了什么**：对 8 种 APR 工具生成的 189 个补丁，请 **35 名职业开发者**独立标注正确性，建 gold set（152 incorrect / 35 correct）。然后把「用自动生成的独立测试集（ITS，由 DiffTGen 与 Randoop 生成）判定」这种自动判据，与人类 gold set 算**评审者间一致性**。

**关键数字**：

| 判据 | Cohen κ | Krippendorff α |
| :-- | :-- | :-- |
| **人类互评**（35 名职业开发者） | **0.691** | **0.734** |
| DiffTGen ITS vs ALL-AGREE | ⛔ **0.078** | ⛔ **−0.32** |
| Randoop ITS vs ALL-AGREE | 0.073 | −0.30 |
| 两者合并 | 0.158 | −0.057 |

⭐⭐ **本条的要点不是「自动判据不好」，而是那个数字的成因**：ITS 标为 incorrect 的补丁**确实都是 incorrect**（零假阳性），⛔ 而它只能标出不到五分之一的错误补丁 —— ⭐ 即这是一个 **sound but incomplete** 的判据。⭐ 把它压成 correct/incorrect 两值再算**对称的** κ / α，结果必然难看到低于随机（α 为负）。⭐⭐ **难看来自判据形态与统计量形态的不匹配，⛔ 不来自判据质量。**

**它支撑哪一句**：⭐⭐ 直接支撑「**同一把尺子套在形态不同的两方上，会系统性地惩罚其中一方，且惩罚幅度与那一方的真实质量无关**」。⭐ 这是本文件里**唯一一条真正落在「评测方法学」层面、并在 CCF A 会议上给出可复算数字的证据**。

**强度**：⭐⭐ **直接证据（就「指标形态不匹配导致结构性不公」这一点而言）**，⛔ 但它的两方是「人类判定 vs 自动测试判据」，⚠️ 不是我们的「散文 vs 形式化断言」。⭐ 机制同构：**一方给的是有确定真值但覆盖有限的判决，另一方给的是覆盖全但需解释的判断** —— ⭐ 两臂正是这个关系（方法臂只在谓词覆盖到的地方发声，基线臂可以在任何地方发声）。

**局限**：⚠️（1）2019 年，⛔ 早于「2022 年起优先」；⭐ 但属该主题奠基工作。（2）领域是 APR 补丁正确性，⛔ 不是缺陷发现。（3）⚠️ 与 [assertion_output_form_evidence.md](./assertion_output_form_evidence.md) [65] 同篇。（4）⛔ Table 5 未亲核。

### D-2 · Chandak et al. 2025（Answer Matching）—— ⭐⭐ **换一种输出契约，指标效度从 π 0.26 变到 0.97，且模型排名显著改变**

**引用** [11]：Nikhil Chandak, Shashwat Goel, Ameya Prabhu, Moritz Hardt, Jonas Geiping (2025). *Answer Matching Outperforms Multiple Choice for Language Model Evaluation.* ⛔ **arXiv preprint，无同行评审 venue**（arXiv:2507.02856，2025-07-03，34 pp）。URL: [arxiv.org/abs/2507.02856](https://arxiv.org/abs/2507.02856)

**读到什么层级**：⭐ **取正文数字**（摘要经 arXiv abs 页确认；π 数值自行下载 v1 PDF 提取 §正文段落，逐条核过 0.97 / 0.98 / 0.72 / 0.43 / 0.26 与「85% of errors are false positives」）。

**它实际做了什么**：论证选择题（discriminative）评测存在**捷径** —— 摘要逐字：popular benchmarks 的题目 *"can often be answered without even seeing the question."* 提出 **answer matching**：不给选项、让模型自由生成，再用一个带参考答案的语言模型判是否匹配。为比较各评测策略的**效度**，他们人工标注 MMLU-Pro 与 GPQA-Diamond 得到 human grading，再算各方法与人类的一致性。

**关键数字**（Scott's π，与 ground-truth eval 的一致性；MATH Level 5 上 Qwen2.5-7B 的回答）：

| 评测策略 | Scott's π |
| :-- | :-- |
| Answer matching（1.7B Qwen3 matcher） | ⭐ **0.97** |
| Answer matching（DeepSeek-V3 matcher） | ⭐ **0.98** |
| LLM-as-a-judge（DeepSeek-V3，⛔ 无参考答案） | 0.72 |
| MC Verify | 0.43 |
| ⛔ 标准选择题（MCQ） | ⛔ **0.26** |

⭐ MCQ 的失败**主要是假阳性（约 85% 的错误）**。⭐ 摘要另逐字：*"the rankings of several models change significantly when evaluating their free-form responses with answer matching."*

**它支撑哪一句**：⭐⭐ 支撑「**评测的输出契约（要交付什么形态）不是中立的实施细节 —— 换契约会改变指标效度一个量级，并改变系统间的相对排名**」。⭐ 即「同一能力、不同输出形态、同一指标」这个组合本身就不可信。

**强度**：⭐ **强类比证据（就「输出契约决定可比性」这一点）**，⛔ 但 **方向与我们相反** —— ⚠️ 它证明的是**受约束的形态（选择题）被过度给分**，⛔ 不是「受约束的形态被过度惩罚」。⚠️ ⛔ **引用时必须说清这一点**，否则会被 reviewer 反用。

**局限**：⚠️（1）⛔ **无同行评审**。（2）领域是事实 / STEM QA，⛔ 不是形式化制品。（3）⛔ 方向相反（见上）。（4）它的判定者是 LLM matcher，⛔ 我们的是人工。

### D-3 · Bulian et al. EMNLP 2022 —— ⭐ 匹配式指标的判决取决于**表面形态**而非内容，⚠️ 但方向对我们只是半有利

**引用** [10]：Jannis Bulian, Christian Buck, Wojciech Gajewski, Benjamin Börschinger, Tal Schuster (2022). *Tomayto, Tomahto. Beyond Token-level Answer Equivalence for Question Answering Evaluation.* EMNLP 2022, pp. 291–305. **EMNLP = CCF B**。ACL Anthology: [2022.emnlp-main.20](https://aclanthology.org/2022.emnlp-main.20/) · DOI [10.18653/v1/2022.emnlp-main.20](https://doi.org/10.18653/v1/2022.emnlp-main.20)

**读到什么层级**：⭐ **取正文数字**（自行下载 ACL PDF 提取 §3–§5 的 55% / 69.9% / α 0.84 / 87% 与 AE 定义段）。

**它实际做了什么**：论证 QA 里用有限标注答案集 + exact match / token-F1 打分会**低估**系统真实表现。收集 SQuAD 上 **14,170 条人工评级 / 8,565 个 (context, question, reference, candidate) 四元组**（论文另称总计 >23k judgements），人工一致性 Krippendorff **α = 0.84**、多标注样本 >88% 完全一致。据此定义 **asymmetric answer equivalence (AE)**，并训练 BERT matching (BEM) 指标替代 F1。

**关键数字**：⭐ **在「不是 exact match」的候选里，人工评级认为 55% 其实与参考答案等价**（SQuAD train 候选上高达 **69.9%**）。⭐ 即 exact match 把过半数正确答案判错，⛔ 而这完全由表面形态决定。BEM 在 NQ-Open 上与人工独立判定的一致率 **87%**。

⭐ **一个对我们特别有用的设计细节**：他们的 AE 定义是**刻意不对称**的 —— 候选必须「not completely different」且「containing **at least as much** relevant information and **not more** irrelevant information」才算等价。⭐ 也就是说：为了让指标公平，他们不得不**显式承认「更详细」与「更含混」不能同等对待**，并把这一点写进判据定义。

**它支撑哪一句**：⭐ 支撑「**同一指标下判对判错，可以主要由输出的表面形态决定**」，以及「**要让跨形态比较公平，判据必须显式处理形态差异（如 AE 的不对称设计），而不能只问「说的是不是同一件事」**」。⭐ 后半句正是我们的指标（「有没有指出同一处缺陷」）所缺的。

**强度**：⚠️ **类比证据（中等）**，⛔ 且**方向只有一半对我们有利**。⚠️ ⛔ **必须说清**：它证明的是**严格自动匹配会低估自由形态答案**（即严格指标伤自由文本），⛔ **不是**「宽松人工判定会高估自由文本」。⭐ 我们能用的是它的**元层结论**（判决由形态决定 + 公平判据须显式不对称），⛔ 不是它的方向。

**局限**：⚠️（1）⛔ 方向不直接支持我们，若引用不当会**反被用来打我们**。（2）领域是抽取式 QA，⛔ 与缺陷发现相距较远。（3）它的判据是**自动指标 vs 人工**，⛔ 我们的判据本身就是人工。（4）55% 的分母是「非 exact-match 候选」，⛔ 不是全部候选，⚠️ 不要写成「exact match 判错了 55% 的答案」。

### D-4 · Zhang et al. ACL 2025（From Lists to Emojis）—— ⚠️ **⛔ 未独立复核，且方向对我们不利**

**引用** [12]：Xuanchang Zhang, Wei Xiong, Lichang Chen, Tianyi Zhou, Heng Huang, Tong Zhang (2025). *From Lists to Emojis: How Format Bias Affects Model Alignment.* ACL 2025 (Vol. 1: Long Papers), pp. 26940–26961. **ACL = CCF A**。DOI [10.18653/v1/2025.acl-long.1308](https://doi.org/10.18653/v1/2025.acl-long.1308) · arXiv: [2409.11704](https://arxiv.org/abs/2409.11704)

**读到什么层级**：⛔⛔ **仅代理调研的摘要级信息，本轮我未取原文** —— ⛔ **禁引数字**（唯一被代理声明可担保的是「<1% 的有偏训练数据即足以给 reward model 注入显著偏置」）。⚠️ 作者名单亦未经我独立核，⛔ 引用前必须重取。

**它实际做了什么（据摘要）**：人类评估者、GPT-4 与 RewardBench 上的头部 reward model 都对特定格式模式（列表、链接、加粗、emoji）表现出强偏好；模型可利用这一点在 AlpacaEval 与 LMSYS Chatbot Arena 上刷分；结论是必须 *"disentangle format and content."*

**它支撑哪一句 / 为什么仍要登记**：⚠️ ⛔ **它的方向对我们不利** —— 它说的是**富格式（列表、加粗）被奖励**，⛔ 而不是「结构化输出被惩罚」。⭐ 登记它的理由是：（1）它是「形态污染单一质量分」这个元命题的 CCF A 级支撑；（2）⚠️ ⛔ **reviewer 很可能拿它反问我们**：既然判定者偏爱结构化形态，为什么我们的结构化断言反而吃亏？⭐ 我们必须能回答（答案在 A-1：被奖励的是**形态饱满**，被惩罚的是**可被指认为错的精确绑定**；断言两头都不占便宜）。

**强度**：⚠️ **仅相关，且半反向**。⛔ 不得当承重引用。

---

## 5. ⚠️⚠️ 反向证据（对我们不利，必须一并报）

### R-1 · Tam et al. EMNLP 2024 —— ⛔ **结构化输出确实会降低推理能力**

**引用** [13]：Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin, Hung-yi Lee, Yun-Nung Chen (2024). *Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models.* EMNLP 2024 **Industry Track**, pp. 1218–1236. **EMNLP = CCF B**（⚠️ Industry Track，⛔ 非主会）。ACL Anthology: [2024.emnlp-industry.91](https://aclanthology.org/2024.emnlp-industry.91/) · DOI [10.18653/v1/2024.emnlp-industry.91](https://doi.org/10.18653/v1/2024.emnlp-industry.91) · arXiv: [2408.02442](https://arxiv.org/abs/2408.02442)

**读到什么层级**：⭐ **取正文数字**（读 arXiv v3 全文 HTML 的 Table 1 / 2 / 9 / 11；⚠️ venue 另经 ACL Anthology 独立确认 —— ⛔ arXiv abs 页**不显示** venue）。⚠️ arXiv 标题末尾是 *"…on Performance of Large Language Models"*，⭐ ACL 版是 *"…on Large Language Model Performance"*，⚠️ 两者略有差异。

**它实际做了什么**：把「格式约束强度」排成五级 —— natural language → NL-to-Format（先自由生成再转格式）→ Format-Restricting Instructions (FRI) → JSON-mode 约束解码 → JSON-Schema (CFG)。在 3 个推理任务（GSM8K、Last Letter Concatenation、Shuffled Objects）与 4 个分类任务（DDXPlus、MultiFin、Sports Understanding、Natural Instructions Task 280）上，跨 gpt-3.5-turbo-0125 / claude-3-haiku / gemini-1.5-flash / LLaMA-3-8B-Instruct / Gemma-2-9B-Instruct（附录另加 gpt-4o-mini、Mistral-7B）比较。

**关键数字**：

GSM8K，text vs JSON（Table 9，零样本）：GPT-3.5 Turbo ⛔ **76.6 → 49.3**；LLaMA-3-8B ⛔ **74.7 → 48.9**；Claude-3-Haiku ⛔ **86.5 → 23.4**；⭐ Gemini-1.5-Flash 89.3 → 89.2（几乎不变）；Gemma2-9B 86.5 → 84.2。Last Letter，text vs JSON：GPT-3.5 ⛔ 56.7 → 25.2；LLaMA-3-8B ⛔ 70.1 → 28.0；⭐ 但 Gemini-1.5-Flash **65.4 → 77.0（反向变好）**。

JSON-mode（真约束解码，Table 11）上 Last Letter 近乎崩塌：GPT-3.5T **1.78**、Gemini-1.5F **0.67**、LLaMA3-8B 7.56。⭐ 作者给出的机制解释很关键：**100% 的 GPT-3.5-Turbo JSON-mode 回答把 `answer` 键排在 `reason` 键之前**，于是链式思维被结构本身取消，退化成直答。

gpt-4o-mini + CFG Structured Output（Table 2）：GSM8K NL **94.57** / FRI 87.17 / JSON-Mode 86.95 / JSON-Schema 91.71；Shuffle Obj NL **82.85** / 81.46 / 76.43 / 81.77；Last Letter NL 83.11 / 84.73 / 76.00 / **86.07**。⭐ 自由文本 3 项中 2 项领先，⛔ 但 JSON-Schema 把 JSON-mode 的损失基本补回来了。

⭐ **作者排除了「解析失败」这个替代解释**：LLaMA-3-8B 在 Last Letter 上 JSON 解析失败率仅 **0.148%**，而分差约 38 点。他们还做了 "Perfect Text Parser" 分离格式错误与真实推理失败。

⭐ **反向的一半（对我们有利）**：分类任务上格式约束**帮忙**。DDXPlus 上 Gemini-1.5-Flash text **41.6 → JSON 60.3**，JSON-mode 下达 **84.92**；GPT-3.5 44.1 → 55.5；Gemma2-9B 22.9 → 53.0。GPT-3.5 在 Sports 上 67.2 (σ 26.8) → 80.0 (σ 3.3)。作者解释：约束答案空间减少了选择错误，而自由文本 *"may introduce distractions."* ⭐ 结论是**任务依赖**：伤推理、帮结构化分类。

**它支撑哪一句**：⛔ 它支撑**对方**的一句 —— 「你们方法臂表现低，可能不是因为尺子偏斜，而是因为你们逼模型输出结构化，本身就削弱了它的能力」。⚠️ ⭐ **这是对我们论证最直接的替代解释，必须在论文里正面处理。**

**威胁大小与可反驳之处**（⭐ 逐条，均基于上面读到的数字）：

1. ⭐⭐ **它是「能力被削弱」的证据，⛔ 不是「尺子公平」的证据。** ⚠️ 严格说它与我们的命题**不互斥**：完全可以同时成立「结构化削弱了方法臂的能力」与「同一指标对散文更宽容」。⭐ 论文里应当两者并列承认，⛔ 而不是驳倒它 —— ⚠️ 只驳不认会被 reviewer 抓。
2. ⭐ **效应模型依赖且方向不一致**：Gemini-1.5-Flash 在 GSM8K 上几乎无损（89.3 → 89.2）、在 Last Letter 上反向变好（65.4 → 77.0）。⛔ 因此「结构化必然伤能力」不成立。
3. ⭐ **机制可规避**：最大崩塌（JSON-mode Last Letter → 1.78）的原因是**键序把 CoT 取消了**，⭐ 这是 schema 设计缺陷，⛔ 不是形式化本身的代价。JSON-Schema 相对 JSON-mode 的回升（GSM8K 86.95 → 91.71）也说明约束**方式**比约束**存在与否**更重要。⭐ [14] 独立复现并强化了这一点。
4. ⭐ **任务类型不匹配**：它测的是 GSM8K / 字母拼接 / 物体追踪这类**短链数学与符号推理**，⛔ 不是「在一份模型上定位缺陷」。⭐ 而它在**分类**任务上的结论是结构化**帮忙**（DDXPlus 41.6 → 84.92）；「这份模型的这一处是否违反某谓词」在形态上更接近分类而非 GSM8K。
5. ⚠️ **venue 是 Industry Track**，⛔ 不是主会；引用时不宜写成「EMNLP 2024」而不加限定。
6. ⚠️ **它有一份公开的复现失败反驳** [17]（⛔ 厂商博客，⛔ 无同行评审，⚠️ 作者方 dottxt 是结构化生成工具 `outlines` 的开发者，⛔ 有商业利益）：核心指控是**结构化与非结构化用了不同的 prompt**（即「不公平比较」），且论文把 *structured generation* 与 *JSON-mode* 混为一谈；⭐ 用同一 prompt 重跑 Llama-3-8B-Instruct 未能复现 Last Letter 的崩塌（⭐ 自由文本约 70% 复现成功，⛔ JSON-mode 的 <10% 未复现）。⚠️ **原作者已公开回应**（称已跨多 prompt 平均、结论不变）。⭐ **值得登记的客观后续**：JSONSchemaBench（Geng et al. 2025）在 GSM8K 与 Shuffle Objects 上**采用了 [17] 的 prompt 与 schema**，并按 [17] 的意见改掉了 Last Letter 的原 prompt。⛔ **不得把 [17] 当作 [13] 已被推翻的证据** —— ⭐ 它只是把 [13] 的强度从「结构化伤推理」降到「**实现方式**伤推理」，⚠️ 而这与 [14] 的独立结论同向。

### R-2 · Lee, D'Antoni, Berg-Kirkpatrick 2026（The Format Tax）—— ⚠️⚠️ **双刃：它既削弱 [13]，⛔ 又给出本文件最危险的一条负面对照**

**引用** [14]：Ivan Yee Lee, Loris D'Antoni, Taylor Berg-Kirkpatrick (2026). *The Format Tax.* ⛔ **arXiv preprint，无同行评审 venue**（arXiv:2604.03616 v1，2026-04-04；cs.CL；标注 *"Preprint. Under review."*）。URL: [arxiv.org/abs/2604.03616](https://arxiv.org/abs/2604.03616) · 代码 [github.com/ivnle/the-format-tax](https://github.com/ivnle/the-format-tax)

**读到什么层级**：⭐ **取正文数字**（自行下载 v1 PDF 提取摘要 / §1 / §4.1 / Table 2 / Table 3 / 闭源模型表）。

**它实际做了什么**：把 format tax 定义成 $\mathrm{FormatTax} = \mathrm{Perf}_{\mathrm{freeform}} - \mathrm{Perf}_{\mathrm{format\text{-}constrained}}$，并把它**分解**成 prompt-level（要求格式的指令本身）与 decoder-level（grammar-constrained decoding, GCD 的采样偏置）两部分。跨 6 个开源权重模型 + 4 个 API 模型、4 种格式（JSON / XML / Markdown / LaTeX）、数学 / 科学 / 逻辑 / 写作任务。

**关键数字**：

- ⭐ 摘要与 §1 逐字：*"format-requesting instructions alone cause most of the accuracy loss, before any decoder constraint is applied"* —— ⭐ **prompt 层是主因，decoder 层是次因。**
- ⭐ 逐字：*"most recent closed-weight models show little to no format tax, suggesting the problem is not inherent to structured generation but a gap"* open-weight 尚未补上。闭源表里 claude-haiku-4.5 与 grok-4.1-fast 的多数格子是 **正号**（如 +1.1 / +1.2 / +2.5 / +4.3），⛔ 只有 gpt-5-nano / gpt-5.4-nano 有明显负值。
- ⭐ 逐字：把任务与格式**解耦**（2-Turn：先自由生成再重排格式；或允许 extended thinking）*"recovers most lost accuracy."* Table 2 里 nemotron3-nano 的 LaTeX 写作损失从 1-Turn 的 −15.7 降到 2-Turn 的 −7.0。
- 开源侧 tax 是真的：Table 3 里某模型 24 格中 9 格显著（平均 −4.3 pp），另一模型平均 −9.9 pp。

⛔⛔ **本文件最危险的一段（§4.1）**：作者**主动设了一个「判定者是否惩罚形态本身」的对照** —— 逐字：*"A natural concern is that LLM judges penalize markup aesthetics rather than content. We tested this by stripping LaTeX and judging the extracted prose: scores did not meaningfully change. The degradation reflects genuinely worse writing, not judge bias."* ⭐ Table 2 的 `LTX` 列（judge 直接看带标记的文档）与 `PROSE` 列（剥掉标记只看内容）确实非常接近（如 −15.7 vs −16.1、−6.8 vs −7.8）。Wilcoxon 检验在 40 格中 36 格显著（$p < 0.05$）。

**它支撑哪一句**：⛔⛔ **它支撑对方最强的一句** —— 「**有人专门做过「判定者是否因形态而扣分」的对照，结果是没有；分数下降反映的是内容真的变差了，⛔ 不是判定偏置。**」

**威胁大小**：⭐⭐ **这是全文件对子命题 A 威胁最大的一条**，⚠️ 因为它不是间接推论，⭐ 而是一次**针对我们这个假设的显式否证实验**。⭐ 可辩护之处只有一条，⛔ 但必须说得诚实：**它的两个条件里内容都是散文**（带 LaTeX 标记的散文 vs 剥掉标记的散文），⛔ **它从未比较「散文 vs 形式化断言」**；即它否证的是「judge 嫌标记难看」，⛔ **不是**「judge 对含混与精确的严格度不同」（后者由 [1] 的 98.3% vs 33.9% 支持）。⚠️ ⭐ **这两件事必须在论文里明确区分，否则 reviewer 会拿这一段直接否掉我们的整个论证。**

⭐ **它对我们有利的一半**：它把 [13] 的威胁大幅削弱 —— format tax 主要在 **prompt 层**、可通过**解耦**恢复、且**近期闭源模型基本没有**。⭐ 若我们的方法臂用的是近期闭源模型，[13] 的替代解释就更难成立。

**局限**：⚠️（1）⛔ **arXiv 预印本，under review，无同行评审**。（2）⛔ 判定者是 LLM judge，⛔ 我们是人工。（3）判定对象是**写作质量**，⛔ 不是「是否指出了同一处缺陷」。（4）2026-04，⚠️ 很新，⛔ 尚无引用与复现记录。

### R-3 · Kharchenko et al. 2025 —— ⛔ **含混 / 对冲语气被**惩罚**，⛔ 直接否掉「判定者奖励含糊」这种表述**

**引用** [15]：Julia Kharchenko, Tanya Roosta, Aman Chadha, Chirag Shah (2025). *I Think, Therefore I Am Under-Qualified? A Benchmark for Evaluating Linguistic Shibboleth Detection in LLM Hiring Evaluations.* ⛔ **arXiv preprint，无 venue**（arXiv:2508.04939，2025-08-06；cs.CL）。URL: [arxiv.org/abs/2508.04939](https://arxiv.org/abs/2508.04939)

**读到什么层级**：⚠️ **仅摘要页**。⛔ 除下面那个 25.6% 外无可引数字（⛔ 无逐模型分解、⛔ 无置信区间）。

**它实际做了什么（据摘要）**：造一个 benchmark，对**同一份底层答案**生成受控的语言变体，**每次只改一个语言现象、保持语义等价**（逐字：变体 *"isolate specific phenomena while maintaining semantic equivalence"*），用于测 LLM 在模拟面试评估中的语言歧视。基于 100 组经校验的问答对。

**关键数字**：⛔ 逐字：模型 *"systematically penalize certain linguistic patterns, particularly hedging language, despite equivalent content quality"*，**带对冲语气的回答平均评分低 25.6%**。

**它支撑哪一句**：⛔⛔ 它**否证**「判定者奖励含混 / 对冲表述」这种写法。

**威胁大小**：⭐ **中等，但主要是措辞层面的威胁** —— ⚠️ 它迫使我们把子命题 A 写成**窄形式**。⭐ 关键区分：[15] 说的是**语气层面的对冲**（"I think"、"perhaps"）被扣分；[1] 说的是**内容层面的不完整**（只答了一部分）逃过错误判定。⭐ 二者不矛盾，⛔ 但如果我们把 A 写成「判定者对含糊宽容」，[15] 就是现成的反例。⛔ **必须写成「对内容不完整宽容」，不能写成「对含糊语气宽容」。**

**局限**：⚠️（1）⛔ 无同行评审。（2）领域是招聘评估，⛔ 与缺陷判定无关。（3）⛔ 我只读到摘要。（4）判定者是 LLM，⛔ 我们是人工。

---

## 6. ⭐ 可直接用于论文的措辞拟稿

⛔⛔ **下面有两份拟稿。⭐ 用 6.2，⛔ 不要用 6.1。** ⚠️ 6.1 是 §7.0 的内部实测**到位之前**写的，⛔ 它已被那两个数字击穿，⭐ 保留它只为记录口径变化（[../../../CLAUDE.md](../../../CLAUDE.md) §3.6 要求就地更正并说明改了什么）。

### 6.1 ⛔ 作废稿（⛔ 不要使用）

⭐ 原挂 [1][4][7]：

> 需要说明的是，两臂的输出形态并不对等，因而不宜在同一判定口径下直接比较。评审研究已量化出这种不对称：判定者对「内容不完整」的回答远比对「精确但有一处绑定错误」的回答宽容，后者被识别为错误的比例达 98.3%，而前者仅 33.9% [1]。同一份语义内容，用自然语言表述的出错率约为写成形式化表述的一半（23% 对 47%，在领域专家身上亦然）[4]；从自然语言导出可机械求值断言的有效率，也从干净基准上的 81% 掉到真实制品上的 12.2% [7]。因此基线臂的散文与方法臂的可求值断言承担着不同量级的正确性负担，本文报告的两臂差值应理解为形态负担与能力差异的叠加，而非纯粹的能力差距。

⛔ **为什么作废（两条，均来自 §7.0 的内部实测）**：

1. ⛔ 它把 [7] 的「81% → 12.2%」用来暗示**基线的散文难以变成可求值断言** —— ⛔ 而我们实测基线可断言率 **98.4%**。⚠️ 这一步是**被我们自己的数据证伪的过度解读**。
2. ⛔ 末句「两臂差值应理解为形态负担与能力差异的叠加」把 [1] 的判定宽松度当成那 14.9pp 的**共同成因** —— ⛔ 而跨臂逐位数据（14.6% / 29.6% 双向独有命中）显示那是**能力正交**，⛔ 不是一边被放宽。

### 6.2 ⭐ 现行稿（⭐ 中文 **197** 字，⛔ 不含标点与 `[n]`；⭐ 挂 [9][8][4]）

> 两臂交付的制品形态不同：方法臂交付绑定到模型元素且可确定性求值的断言，基线臂交付自由文本；而命中判据只问是否指向同一处缺陷，不区分交付形态。已有工作表明，把形态不同的两方压进同一个对称判据，会系统性惩罚受约束的一方，且与其真实质量无关 [9]；「指出问题」与「交付可被下游消费的发现」之间的缺口亦已被实测：最有下游价值的形态恰最难产出 [8]。即使领域专家，写成形式化的出错率也是反方向的两倍 [4]。故两臂差值只反映该判据下的命中能力，不反映下游可用性。

⭐ **它与 6.1 的三处关键区别**：（1）⛔ 不主张判定宽松度差异，⭐ 改挂**判据与形态不匹配的结构性惩罚** [9]；（2）⛔ 不主张基线不可形式化，⭐ 改挂**下游可消费性缺口** [8]；（3）⭐ [4] 只用于「**authoring 方向更易错**」这一窄义，⛔ 不用于「散文不可形式化」。

⚠️ **写进论文时必须同时保留四处限定**（⛔ 否则不诚实，且会被 reviewer 直接击穿）：

1. ⭐ [1] 的 "under-specified" 操作定义是**实体答不全**，⛔ 不是散文式含混 —— ⚠️ 从前者推到后者是**我们做的类比**。
2. ⭐ [4][5][7] 的对象分别是 LTL 与程序后置条件，⛔ **都不是状态机** —— ⚠️ 按 [README.md](./README.md) 护栏二须标明对象。
3. ⚠️ 若同时讨论「结构化是否本身削弱能力」，⛔ 必须引 [13] 并承认它是**并存的**替代解释，⛔ 不能只说它被 [14] 削弱了。
4. ⛔⛔ **必须同时报出可断言率实测**：基线 **98.4%** / 主臂 **99.2%**（差 0.8pp）—— ⛔ 即**不得**让读者以为基线的发现不可形式化。⭐ 措辞只能是「尚未被形式化」，⛔ 不能是「不可形式化」。⚠️ 这条不是可选的谨慎，⭐ 而是我们自己事前登记、跑后证伪的结果（[../baseline_arm/preregistered_actionability.md](../baseline_arm/preregistered_actionability.md) §9），⛔ 隐去它属选择性报告。

---

## 7. ⛔⛔ 诚实评估：这个论证能撑到多硬

### 7.0 ⛔⛔⛔ 先读这一节：**我们自己的实测比上面任何一条文献都硬，⛔ 而它砍掉了本论证的一半**

⚠️ **2026-08-12 补记（⛔ §7.1–§7.3 成文时不知道这两个数）。** ⛔ 本文件到此为止全部建在**外部文献**上，⛔ 而 X1 对照臂已经产出了两组**我们自己语料上的直接测量**。⭐⭐ **凡内部实测与外部类比冲突，一律以内部实测为准** —— ⛔ 外部文献没有一条是在本语料、本判据、本判定链上做的。

#### 7.0.1 ⛔⛔ 「基线的发现不可机械求值」**是假的** —— 实测两臂差 0.8pp

⭐ 出处：[../baseline_arm/preregistered_actionability.md](../baseline_arm/preregistered_actionability.md) §9（⭐ 事前登记了 10pp 的达标门，⛔ 跑后不成立并已按登记放弃）。

| 臂 | 可断言率 |
| :-- | --: |
| X1 基线（A1–A4，全量 443 位） | $436/443 = \mathbf{98.4\%}$ |
| 主臂（M1，分层抽 120 个命中位） | $119/120 = \mathbf{99.2\%}$ |
| **差** | $\mathbf{0.8}$**pp** |

⛔⛔ **因此论文不得主张下列任何一句**：

1. ⛔ 「基线的发现不可机械求值 / 不可形式化。」—— ⭐ 实测 98.4% 可断言。
2. ⛔ 「方法臂 by construction 100% 可断言。」—— ⛔ 实测 119/120，**不是** 100%。
3. ⛔ 「基线没有发现这些问题。」—— ⭐ 它发现了。

⭐ **能主张的只剩一句**，⚠️ 且它弱得多：

> ⭐ 基线的发现**尚未被**形式化，而方法臂的**已经是**。

⚠️ ⛔ **这句话的性质要认清：它是关于「交付物形态」的陈述，⛔ 不是关于「能力」的陈述。** ⭐ 两臂差的是**谁把形式化这一步做了**，⛔ 不是**谁做得到**。⚠️ 而 A4 判定组给出的**双向夹击**（同上 §9.1 第 4 条）指出：严口径测的是**输出格式**（⛔ 基线从未被要求输出命题），宽口径测出 100% 则等于**承认基线的发现本身可形式化** —— ⛔ **两个方向都不支持用它论证主臂优势。**

⭐⭐ **对本文件的直接后果**：⛔ 子命题 B 的全部证据（[4][5][7]）**不能再用来论证「基线的散文不可形式化」** —— ⭐ 那个命题已被我们自己证伪。⭐ 它们仍然可用，⛔ 但只能用于一个**重定向后**的、更窄的命题：

> ⭐ **「存在一个可求值断言」与「产出者自己产出了正确的那一个」不是同一件事。** ⭐ 98.4% 是**判定者事后构造**出来的可断言性（⭐ 判据逐字是「是否**存在**一个可判定的谓词 $P$ 与一组模型元素 $E$」），⛔ **不是**基线产出者自己交付的断言。⭐ 而 [4] 恰好量化了这个差：即使**领域专家**，在「英语 → 形式化」这个 authoring 方向上的错误率也是反方向的两倍（28% vs 15%）。

⛔ **⚠️ 这条重定向必须写进论文，否则 [4][5][7] 就是被误用的。**

#### 7.0.2 ⛔⛔ 「尺子对散文更宽松」**解释不了那个 14.9pp** —— 我们自己的跨臂数据反对它

⭐ 出处：[../baseline_arm/results/metrics.md](../baseline_arm/results/metrics.md) §2 / §2.1（588 位逐位并列，两臂键格式逐字相同可直接对拍）。

| | 位数 | 占比 |
| :-- | --: | --: |
| 两臂都命中 | 269 | 45.7% |
| ⭐ **仅主臂命中** | **86** | **14.6%** |
| ⭐ **仅 X1 命中** | **174** | **29.6%** |
| 两臂都未命中 | 59 | 10.0% |

⭐⭐ **若「判定对散文更宽松」是那 14.9pp 的成因，我们应当看到 `x1_only` 很大而 `main_only` 趋近 0。** ⛔ 实际两臂各有 14.6% 与 29.6% 的**独有**命中 —— ⭐ 这是**能力正交**的形状，⛔ 不是一边被系统性放宽的形状。

⭐ 更硬的一条：按主臂四池分解，**X1 在主臂满格池的命中率 77.0%（171/222）与在主臂零命中池的 77.5%（107/138）几乎相同** —— ⛔ 即主臂能否稳定命中某条缺陷，与 X1 能否命中它**基本无关**。⛔ 这同时反驳「基线只是把容易的那些捡了一遍」。

⛔⛔ **所以：子命题 A 即使在文献层面成立（[1] 的 98.3% vs 33.9%），⛔ 它也解释不了我们观察到的那个差。** ⚠️ ⛔ **不得**把 [1] 写成「这就是为什么基线数字更高」。

#### 7.0.3 ⭐ 唯一还站得住、且**可在我们自己数据上检验**的形态论点

⭐ 判据本身（[../discover_matrix/docs/protocol/hit_criterion.md](../discover_matrix/docs/protocol/hit_criterion.md) §4、及其在 [../baseline_arm/judging_instructions.md](../baseline_arm/judging_instructions.md) §2.2 的浓缩版）含两条**按证据形态定义**的否决条款：**「更弱的命题」**与**「⛔ 用结构存在性冒充行为验证」**（`transition_exists` 不得代替 `reaches`）。

⭐ **两臂拿到的判定指令里这两条是逐字相同的**（⛔ 故判据在文本上对称）。⚠️ **但它们能否咬到，取决于被判对象有没有承诺一个形态**：⭐ 一条散文发现（「这个状态可能到不了」）**不承诺**任何谓词，⛔ 因此无法被认定为「以次充好」；⭐ 而一条断言 `transition_exists(...)=False` 承诺了形态，⛔ 于是可被这条否决条款击中。

⭐⭐ **这与 [1] 的机制完全同型**：⭐ 精确绑定 → 可被指认为错（98.3% 被抓）；⛔ 内容不完整 → 无从指认（仅 33.9% 被抓）。⭐ **本条是本文件里唯一一处把外部文献机制与我们自己的判据条款对上的地方。**

⚠️ **一次粗测（⛔ 只是代理指标，⛔ 不是结论）**：在判定 argument / note 的长文本里检索这两条条款的措辞（`以次充好` / `结构存在性` / `更弱的命题` / `不能代替` / `不蕴含`）：

| 判定表 | 长文本条数 | 命中条款措辞 | 占比 |
| :-- | --: | --: | --: |
| 主臂 `v46_human.json` | 497 | **17** | **3.4%** |
| X1 基线 `group_verdicts/J*.json` | 621 | 4 | 0.6% |

⛔⛔ **这个数字不得当证据用，理由三条**：（1）它数的是**条款措辞出现**，⛔ 不是**否决发生**；（2）主臂那 17 条里至少有一条是判定者说明该发现**通过**了该条款（逐字：*"证据族为 simulation，非结构存在性冒充"*），⛔ 即方向相反；（3）基线那 4 条经逐条查看**全部是无关用法**（如描述缺陷本身的「stereotype 文本冒充结构」），⛔ 与否决条款无关。

⭐ **要把这条论点变成证据，需要做的测量是**：逐位统计**因 §4 / §2.2 形态条款而被判未命中**的位数，按臂分。⭐ 若主臂显著高于基线，⭐ 那就是**我们自己数据上的直接证据**，⭐ 强度远超本文件全部外部类比。⛔ **本轮未做。**

### 7.1 逐子命题结论

| 子命题 | ⭐ 最强证据 | 结论 |
| :-- | :-- | :-- |
| **A** 判定对自由文本更宽松 | [1]（98.3% vs 33.9%）、[16]（⭐ 机制：不可证伪故不被惩罚） | ⚠️ **只在窄形式下成立**：「内容不完整逃过错误判定」有直接量化；⛔ 「含糊被奖励」**被 [15] 否证**；⛔ 「judge 因形态扣分」**被 [14] 的显式对照否证**；⛔⛔ **且即使成立，它也解释不了我们的 14.9pp（见 **§7.0.2**）** |
| **B** NL 与形式化之间有可量化落差 | [4]（23% vs 47%）、[7]（81% → 12.2%）、[5]（100% → 46–54%） | ⭐⭐ **最硬的一支**：三条独立证据、三个不同领域、一条 CCF A；⛔ 但全部越界（LTL / 程序），⛔ 且全部是**翻译 / 生成**任务而非**发现**任务 |
| **C** 报告 ≠ 可执行 | [8]（Spearman −0.035） | ⭐ **稳，但只到「形态间有难度落差」**；⛔ 完全不触及「尺子偏斜」 |
| **D** 跨形态同指标不可比 | [9]（κ 0.078 vs 0.691）、[11]（π 0.26 vs 0.97） | ⭐ **机制层有直接证据（[9]，CCF A）**；⛔ 但 [11][10][12] **方向都与我们相反**（它们说受约束的形态被**过度给分**） |

### 7.2 ⛔ 总判：**「有文献直接支持」与「只能类比」之间，实情是后者偏多**

⚠️ **⛔ 本节成文时不知道 **§7.0** 的两个内部实测。** ⭐ 下面三条仍然成立（⛔ 它们讲的是文献强度），⛔ 但**结论档位要按 §7.0 再降一级**：⭐ 那里的两组数字不是「文献不够硬」，⭐ 而是**我们自己的数据直接否掉了本论证的两个支柱之一**（可形式化性）并**否掉了另一支柱对本实验的解释力**（判定宽松度）。

⛔ **必须承认三件事**：

1. ⛔⛔ **没有任何一篇论文做过我们这个比较** —— 即「同一批缺陷、同一批判定者、一臂交散文一臂交可机械求值断言、测判定的严格度差」。⭐ 整个论证是**由四条不同领域的类比复合而成**的，⛔ 不是一条现成结论。
2. ⛔⛔ **最关键的那一环（判定者对散文更宽松）恰恰是最弱的一环**。⭐ 它只有 [1] 一条直接量化，⚠️ 而 [1] 是 **workshop 论文**、⚠️ 判定者是 **LLM 而非人工**、⚠️ 「不完整」的操作定义是**实体答不全而非散文含混**。⛔ 更糟的是 [14] 做了一次**针对这个假设的显式对照并得到否证**（虽然它的两侧内容都是散文，⭐ 这是我们唯一的辩护空间）。
3. ⛔ **子命题 D 的三条证据里有两条方向相反**（[10][11][12] 都在说「受约束 / 词法匹配的一方被**过度给分**」）。⭐ 我们能借的只有它们的**元层结论**（判决由形态决定），⛔ 借不到方向。

⭐ **因此这个论证能支撑的最强表述是**：

> ✅ **可以**写成 **threats to validity / 讨论章的一节**：「本文的两臂输出形态不同质，指标对二者的严格度不对称有文献先例（[1][4][7][9]），故两臂差值不应被读作纯粹的能力差距；我们据此在解释结果时加以限定。」

⛔ **不能**写成：

> ⛔ 「基线臂更高的数字是评测伪影，实际上方法臂更强。」

⛔ 这一步文献**撑不住**，⛔ 而且它在方法论上正是 [../../../CLAUDE.md](../../../CLAUDE.md) §3.5 第 4 条禁止的「**评测口径迁就结果**」—— ⚠️ 我们是在拿到「基线臂更高」之后才去找「为什么这个比较不公平」的证据。⭐ 唯一诚实的走法是：**把形态不对称作为一个事前就应当承认的实验设计局限写出来，同时如实保留基线臂更高这个结果**，⛔ 而不是用它去解释掉那个结果。

⚠️⚠️ **一条方法论建议（⛔ 不属文献结论，是我的判断）**：⭐ 与其靠文献论证「比较不公平」，不如**做一次直接测量** —— 把方法臂的断言**降级渲染成散文**（去掉绑定与真值，只留「某处某性质可能有问题」），交同一批判定者重判。⭐ 若同一发现在散文形态下命中率显著上升，⭐ 那就是**我们自己数据上的直接证据**，⭐ 强度远超上面全部类比。⚠️ 这也正是 [14] §4.1 那个对照的做法（剥掉形态、只判内容），⛔ 只是方向相反。

### 7.3 ⚠️ 反向证据的威胁排序

⛔⛔ **最重的两条威胁不在文献里，⭐ 在我们自己的数据里** —— ⭐ 故本表新增 0a / 0b 两行，⛔ 它们压过下面全部文献。

| 排序 | 证据 | 威胁 | 可辩护空间 |
| :-- | :-- | :-- | :-- |
| ⛔⛔ **0a（最重）** | ⭐ **内部实测**：可断言率基线 98.4% / 主臂 99.2%（差 0.8pp） | ⛔⛔ **直接证伪「基线的发现不可机械求值」** —— ⭐ 这是本论证原本的支柱之一 | ⛔ **没有辩护空间，只能改主张**：⭐ 退到「尚未被形式化 vs 已经是」，⛔ 并同时报出该实测 |
| ⛔⛔ **0b** | ⭐ **内部实测**：跨臂双向独有命中 14.6% / 29.6%；满格池 77.0% vs 零命中池 77.5% | ⛔⛔ **子命题 A 即使成立也解释不了那 14.9pp** —— ⭐ 数据形状是能力正交，⛔ 不是一边被放宽 | ⛔ **没有辩护空间**：⭐ 只能把形态不对称写成**设计局限**，⛔ 不得用它解释掉基线更高这个结果 |
| ⛔ **1（文献中最重）** | [14] §4.1 的形态偏置对照（剥标记后分数不变） | ⛔ 它是对子命题 A 的**显式否证实验** | ⭐ 它两侧内容都是散文，⛔ 从未比较散文 vs 形式化断言 |
| ⛔ **2** | [15] 对冲语气被罚 25.6% | ⛔ 否掉「含糊被奖励」的表述 | ⭐ 区分**语气对冲** vs **内容不完整**；⛔ 我们只能主张后者 |
| ⚠️ **3** | [13] 结构化伤推理（GSM8K 86.5 → 23.4 等） | ⚠️ 提供了「方法臂低是因为能力被削弱」的替代解释 | ⭐ 与我们的命题**不互斥**，应并列承认；⭐ 且被 [14] 大幅削弱（prompt 层为主、可解耦恢复、近期闭源模型基本无 tax） |
| ⚠️ **4** | [12] 富格式被奖励 | ⚠️ reviewer 会反问「既然判定者偏爱结构，为何你们吃亏」 | ⭐ 答案在 [1]：被奖励的是**形态饱满**，被惩罚的是**可被指认为错的精确绑定** |
| ⚠️ **5** | [10][11] 受约束形态被过度给分 | ⚠️ 方向相反 | ⭐ 只借元层结论，⛔ 不借方向 |

---

## 8. §References

⚠️ 每条的「读到什么层级」见正文对应小节。⛔ 标 **arXiv-only** 的条目无同行评审，引用时必须标明。

⚠️ **编号只在本文件内有效。** ⛔ 正文若出现 `[65]`，那是 [assertion_output_form_evidence.md](./assertion_output_form_evidence.md) 的编号（⭐ 指 Le et al. ICSE 2019，⭐ 即本文件的 [9]，⭐ 同一篇），⛔ 不是本表的条目。

**子命题 A**

[1] Aman Singh Thakur, Kartik Choudhary, Venkat Srinik Ramayapally, Sankaran Vaidyanathan, Dieuwke Hupkes. *Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges.* Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics (GEM²), ACL 2025, pp. 404–430, Vienna, Austria. ⚠️ ACL **workshop**。<https://aclanthology.org/2025.gem-1.33/> · arXiv <https://arxiv.org/abs/2406.12624>

[2] Minghao Wu, Alham Fikri Aji. *Style Over Substance: Evaluation Biases for Large Language Models.* Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025), pp. 297–312, Abu Dhabi, UAE. **CCF B**。<https://aclanthology.org/2025.coling-main.21/> · 预印本 arXiv <https://arxiv.org/abs/2307.03025>

[3] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023, Datasets and Benchmarks Track. **CCF A**。<http://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html> · arXiv <https://arxiv.org/abs/2306.05685>

**子命题 B**

[4] Ben Greenman, Sam Saarinen, Tim Nelson, Shriram Krishnamurthi. *Little Tricky Logic: Misconceptions in the Understanding of LTL.* The Art, Science, and Engineering of Programming 7(2), 7:1–7:37, 2023. ⚠️ 非 CCF 目录内。arXiv <https://arxiv.org/abs/2211.01677>

[5] William H. English, Chase Walker, Dominic Simon, Sumit Kumar Jha, Rickard Ewetz. *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite.* 2025. ⛔ **arXiv-only**（v1 2025-07-01 / v2 2025-12-18）。<https://arxiv.org/abs/2507.00877>

[6] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, Caroline Trippel. *nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models.* CAV 2023, vol. 2, pp. 383–396. **CCF A**。DOI <https://doi.org/10.1007/978-3-031-37703-7_18> · arXiv <https://arxiv.org/abs/2303.04864>

[7] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, Shuvendu K. Lahiri. *Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions?* Proc. ACM Softw. Eng. (PACMSE), FSE 2024 issue; FSE'24, Porto de Galinhas, Brazil, July 15–19, 2024. **CCF A**。arXiv <https://arxiv.org/abs/2310.01831>

**子命题 C**

[8] Nicolas Bettenburg, Sascha Just, Adrian Schröter, Cathrin Weiss, Rahul Premraj, Thomas Zimmermann. *What Makes a Good Bug Report?* FSE 2008 (SIGSOFT '08/FSE-16), pp. 308–318. **CCF A**。DOI <https://doi.org/10.1145/1453101.1453146> · PDF <https://thomas-zimmermann.com/publications/files/bettenburg-fse-2008.pdf>

**子命题 D**

[9] Xuan-Bach D. Le, Lingfeng Bao, David Lo, Xin Xia, Shanping Li, Corina Păsăreanu. *On Reliability of Patch Correctness Assessment.* ICSE 2019, pp. 524–535. **CCF A**。⚠️ ⛔ 作者是 Xuan-Bach D. Le，⛔ 不是 Claire Le Goues。DOI <https://doi.org/10.1109/ICSE.2019.00064> · arXiv <https://arxiv.org/abs/1805.05983>

[10] Jannis Bulian, Christian Buck, Wojciech Gajewski, Benjamin Börschinger, Tal Schuster. *Tomayto, Tomahto. Beyond Token-level Answer Equivalence for Question Answering Evaluation.* EMNLP 2022, pp. 291–305, Abu Dhabi. **CCF B**。<https://aclanthology.org/2022.emnlp-main.20/> · DOI <https://doi.org/10.18653/v1/2022.emnlp-main.20>

[11] Nikhil Chandak, Shashwat Goel, Ameya Prabhu, Moritz Hardt, Jonas Geiping. *Answer Matching Outperforms Multiple Choice for Language Model Evaluation.* 2025. ⛔ **arXiv-only**。<https://arxiv.org/abs/2507.02856>

[12] Xuanchang Zhang, Wei Xiong, Lichang Chen, Tianyi Zhou, Heng Huang, Tong Zhang. *From Lists to Emojis: How Format Bias Affects Model Alignment.* ACL 2025 (Vol. 1: Long Papers), pp. 26940–26961, Vienna. **CCF A**。⛔⛔ **本轮未取原文，作者名单与数字均待复核**。DOI <https://doi.org/10.18653/v1/2025.acl-long.1308> · arXiv <https://arxiv.org/abs/2409.11704>

**反向证据**

[13] Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin, Hung-yi Lee, Yun-Nung Chen. *Let Me Speak Freely? A Study on the Impact of Format Restrictions on Large Language Model Performance.* EMNLP 2024 **Industry Track**, pp. 1218–1236, Miami, Florida. **EMNLP = CCF B**（⚠️ Industry Track）。<https://aclanthology.org/2024.emnlp-industry.91/> · DOI <https://doi.org/10.18653/v1/2024.emnlp-industry.91> · arXiv <https://arxiv.org/abs/2408.02442>

[14] Ivan Yee Lee, Loris D'Antoni, Taylor Berg-Kirkpatrick. *The Format Tax.* 2026. ⛔ **arXiv-only**（v1 2026-04-04，标注 "Preprint. Under review."）。<https://arxiv.org/abs/2604.03616>

[15] Julia Kharchenko, Tanya Roosta, Aman Chadha, Chirag Shah. *I Think, Therefore I Am Under-Qualified? A Benchmark for Evaluating Linguistic Shibboleth Detection in LLM Hiring Evaluations.* 2025. ⛔ **arXiv-only**（2025-08-06）。<https://arxiv.org/abs/2508.04939>

**2026-08-12 补录**

[16] Anirudh Bharadwaj, Chaitanya Malaviya, Nitish Joshi, Mark Yatskar. *Flattery, Fluff, and Fog: Diagnosing and Mitigating Idiosyncratic Biases in Preference Models.* ICLR 2026 (**Poster**). ⚠️ **ICLR 不在 CCF 目录内**。OpenReview <https://openreview.net/forum?id=tsfjjfhEz7> · arXiv <https://arxiv.org/abs/2506.05339>

[17] Will Kurt (.txt / dottxt). *Say What You Mean: A Response to "Let Me Speak Freely".* dottxt engineering blog, 2024-11-20. ⛔⛔ **厂商博客，⛔ 非论文、⛔ 无同行评审、⚠️ 作者方为结构化生成工具 `outlines` 开发者（有商业利益）。⛔ 只可作为「[13] 存在公开复现争议」的出处，⛔ 不得作为学术结论引用。** <https://blog.dottxt.ai/say-what-you-mean.html>

---

## 9. ⛔ 未收 / 待办

- **Ye et al., *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge*** (arXiv:2410.02736)：⭐ 存在，识别 12 类偏置（CALM 框架），⛔ 但**未取到任何量化结果**，⛔ arXiv-only。⛔ **不得引用数字。**
- **Dubois, Galambosi, Liang, Hashimoto, *Length-Controlled AlpacaEval*** (arXiv:2404.04475, COLM 2024)：⭐ 存在且如标题所述（与 Chatbot Arena 的 Spearman 0.94 → 0.98），⚠️ 但它是**去偏方法**、预设了长度偏置，⛔ 不是关于含混或粒度的证据。⚠️ COLM 不在 CCF 目录。**判定：仅相关，未收。**
- **Zeng et al. LLMBar**：⛔ 未查。
- ⭐ **待补的最有价值一项**：**LLM（而非人类）在「NL 描述 → 形式化」上的方向不对称**。⭐ [4] 是人类，[5][7] 是端到端能力，⛔ **缺一条「同一模型、同一内容、两种输出形态」的对照**。⚠️ 若找不到，⭐ 就该自己做（见 §7.2 末的建议）。
- ⛔⛔ **比上面所有文献都优先的两项测量（⭐ 都在我们自己数据上，⛔ 本轮未做）**：
  1. ⭐ **逐位统计「因形态条款被判未命中」的位数，按臂分** —— ⭐ 即 [hit_criterion.md](../discover_matrix/docs/protocol/hit_criterion.md) §4 的「更弱的命题」与「用结构存在性冒充行为验证」两条。⭐ 若主臂显著高于基线，⭐ 那是**本论证唯一可能的直接证据**（见 **§7.0.3**）。⚠️ 本轮只做了措辞检索的粗测（主臂 3.4% vs 基线 0.6%），⛔ **那不是证据**（数的是条款措辞出现，⛔ 不是否决发生）。
  2. ⭐ **把方法臂的断言降级渲染成散文**（去掉绑定与真值），交同一批判定者重判 —— ⭐ 若同一发现在散文形态下命中率显著上升，⭐ 那就是自有数据上的直接证据。⚠️ 这正是 [14] §4.1 那个对照的做法（剥掉形态、只判内容），⛔ 只是方向相反。
- ⚠️ **口径变更记录（[../../../CLAUDE.md](../../../CLAUDE.md) §3.6）**：2026-08-12 补入 **§7.0**、§0 的收窄声明、§6.1 作废稿与 §6.2 现行稿、§7.3 的 0a/0b 两行、A-4 [16] 与 [17]。⭐ **改动实质**：本文件原以「基线不可形式化 + 尺子对散文更宽松」两条为支柱，⛔ 两条**均已被我们自己的实测削掉**；⭐ 现行可主张的只剩「交付物形态不同、判据不区分形态」，⭐ 且只能写进 threats to validity。⛔ 未删除任何既有核验结论与数字。
