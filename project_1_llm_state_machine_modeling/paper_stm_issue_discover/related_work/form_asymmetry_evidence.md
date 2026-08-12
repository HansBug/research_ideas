# 两臂输出形态不同故直接比较不公平 —— 文献佐证（2026-08-12 调研，进行中）

⚠️ **本文件状态：边查边写，尚未收口。** 每条都必须读过正文或完整摘要 + 关键结论才写进来；⛔ 只看标题的候选一律不写。

---

## 0. 要论证的命题

一篇论文两个实验臂：

- **方法臂**产出**结构化、可机械求值的断言**（绑定到具体模型元素、有确定真值、可重放）。
- **基线臂**产出**自由文本散文**（「这里语义不清」「命名可能造成歧义」）。

两者用同一指标比较：「有没有指出同一处缺陷」（人工语义判定）。**结果基线臂更高。**

⭐ 要论证：**该指标对两种输出形态系统性不同质 —— 对散文宽容、对形式化断言严格，因此直接比较本身不公平。**

⚠️ **与既有文件的分工**：[assertion_output_form_evidence.md](./assertion_output_form_evidence.md) 已经建立了「六种输出形态 × 五个维度」的证据表，回答的是**「可机械求值断言」这种形态本身有什么已建立的性质**。⛔ 本文件不重复它，⭐ 只回答一件它没回答的事：**当把两种形态放到同一把尺子下比较时，那把尺子本身是否偏斜。** 两文件有少量共引（Zheng NeurIPS 2023、Wang ISSTA 2025），⭐ 但用途不同：那边用它们证明「散文形态不可复算」，⭐ 这边用它们证明「评判尺子对形态敏感」。

---

## 1. ⭐⭐ 子命题 A：评判对自由文本比对结构化输出更宽松

（待补，见 §进度）

---

## 2. ⭐⭐ 子命题 B：「能用自然语言指出问题」与「能把它形式化」之间存在已知的可量化差距

⭐ **这是本论证最重要的一支** —— 它直接支撑「散文命中 ≠ 可执行的发现」。

### B-1 · Greenman et al. 2023 —— ⭐⭐ **全库最干净的方向不对称量化：同一批人、同一批内容，「读懂并用英语说出来」的错误率约为「写成形式化」的一半**

**引用**：Ben Greenman, Sam Saarinen, Tim Nelson, Shriram Krishnamurthi (2023). *Little Tricky Logic: Misconceptions in the Understanding of LTL.* The Art, Science, and Engineering of Programming 7(2), 7:1–7:37. ⚠️ **非 CCF 目录内 venue**（`<Programming>` 期刊，有 ACM DL 收录与 artifact evaluation，形式化方法社区高引）。arXiv: [2211.01677](https://arxiv.org/abs/2211.01677) · PDF: [arxiv.org/pdf/2211.01677](https://arxiv.org/pdf/2211.01677)

**它实际做了什么**（读的是上述 PDF 全文，§7 / §8 / Table 5a / Table 5b）：跨两年做四轮研究（三轮书面问卷 + 一轮 talk-aloud），把「理解 LTL」拆成三个方向，其中两个是**同一内容的双向翻译**：`ltl ⊲ Eng`（读一个 LTL 公式，用英语说出它的意思）与 `Eng ⊲ ltl`（读一段英语需求，写出 LTL 公式）。Round 3 的被试是**该领域的 leading researchers**（原文用作 baseline），Round 2 是学习者，Round 4 是 talk-aloud。LTL 答案用**语义等价自动判定**（不是字符串比对），英语答案用两名 coder 编码。

**关键数字**（逐字取自原文 §7 与 §8）：

| 方向 | Round 2（学习者） | Round 3（**领域研究者**） | Round 4（talk-aloud） |
| :-- | :-- | :-- | :-- |
| `ltl ⊲ Eng`（形式化 → 英语） | 23% 错 | **15% 错** | 24% 错 |
| `Eng ⊲ ltl`（英语 → 形式化） | **47% 错** | **28% 错** | **47% 错** |

原文 §8 逐字：*"The error rates are much higher than for the previous questions: 47 % of the Round 2 responses, 28 % of the Round 3 responses, and 47 % of the Round 4 responses were incorrect."* 并在摘要里逐字：*"We also find that the English to ltl direction was the most common source of errors; unfortunately, this is the critical 'authoring' direction in which a subtle mistake can lead to a faulty system."* §7 的 Key Takeaway 反过来说 `ltl ⊲ Eng`：*"In general, subjects did well at this task."*

⭐ **三轮里错误率都恰好约 2 倍**，且**在领域专家身上依然是 2 倍**（15% vs 28%）—— ⛔ 因此不能归因为「被试不熟练」。

**它支撑哪一句**：⭐ 直接支撑「**同一份语义内容，用自然语言表述与用形式化表述，正确率不是同一个量级**」。即：一个人（或模型）能用散文正确指出一件事，**不代表**它能把同一件事形式化正确；反向的失败率约为两倍。⭐ 推到我们的两臂上：基线臂被要求做的是「低失败率的那个方向」，方法臂被要求做的是「高失败率的那个方向」，⛔ 而指标不区分。

**强度**：⭐⭐ **直接证据（就形态不对称这一点而言）**，⛔ 但对象是人不是 LLM、是翻译任务不是缺陷发现任务。⭐ 它是我找到的**唯一一个把同一内容的两种表述形态放在同一批被试、同一套判定下对比**的研究 —— ⭐ 这正是「同一指标下两种形态不同质」所需要的实验结构。

**局限**：⚠️（1）⛔ **对象是 LTL，超出 project_1 的建模对象边界** $M = (S, E, V, Tr, A)$ —— ⭐ 按 [README.md](./README.md) 护栏二，它只能用于「**形态层的一般性质（层一）**」并**必须标明对象不是状态机**，⛔ 不得用于关于我们自己断言的规范性主张。（2）被试是人，⛔ 不是 LLM；LLM 的方向不对称需另证。（3）⛔ 它测的是**翻译**（内容已给定），⚠️ 不是「发现」；我们的两臂里内容不是给定的。（4）英语侧判定靠人工编码，原文自陈可能误标（*"our two-coder method may have mislabeled some written responses"*）。（5）单一 coder 做错误分类（原文自陈）。

### B-2 · English et al. 2025（VLTL-Bench）—— ⭐⭐ **「抽象层说对」到「绑定到具体元素说对」之间掉 40–54 个百分点**

**引用**：William H. English, Chase Walker, Dominic Simon, Sumit Kumar Jha, Rickard Ewetz (2025). *Verifiable Natural Language to Linear Temporal Logic Translation: A Benchmark Dataset and Evaluation Suite.* ⚠️ **arXiv preprint，无同行评审 venue**（arXiv:2507.00877 v1 2025-07-01 / v2 2025-12-18；eess.SY，cross-list cs.CL）。URL: [arxiv.org/abs/2507.00877](https://arxiv.org/abs/2507.00877)

**它实际做了什么**（读的是 v2 HTML 全文，含 Table 4 与 grounding / end-to-end 表）：指出既有 NL→TL 基准**只测 lifted translation**（公式里的原子命题是抽象占位符），从而把 grounding（把占位符绑定到真实状态空间里的具体变量）这一步免费送给系统。他们造 VLTL-Bench：4 个状态空间 + 数千条 NL–TL 对 + 用于验证公式的样例 trace，并在 lifting / grounding / translation / verification 四个子步骤上**各给 ground truth**，从而能分段测。评测了 NL2LTL / nl2spec / NL2TL / Lang2LTL × GPT-3.5-turbo / GPT-4o-mini / GPT-4.1-mini / GPT-4o / 微调 t5-base。

**关键数字**（Table 4 与 end-to-end 表，三个新数据集 S&R / Traffic Light / Warehouse）：

| 系统 | lifted translation | **end-to-end（含 grounding）** |
| :-- | :-- | :-- |
| NL2TL / Lang2LTL（微调 t5-base） | **100.0 / 100.0 / 100.0** | **54.4 / 60.1 / 46.2** |
| nl2spec（GPT-4.1-mini） | 89.1 / 91.6 / 88.4 | 34.8 / 33.6 / 29.6 |
| NL2LTL（GPT-4.1-mini） | 41.6 / 40.0 / 37.4 | 35.4 / 38.4 / 26.2 |
| Lang2LTL（embedding 检索式 grounding） | — | 58.5 / 72.1 / 37.9 |

grounding 单步准确率（few-shot general prompt，「整份 AP 字典全对」口径）低至 **7.0–7.8%**（Warehouse，80 个 COCO 类）；即使 GPT-4o + few-shot CoT 也只到 61.4%。

⭐ 原文自评逐字：既有基准上是 *"near-perfect performance"*，而那些研究 *"only measure the accuracy of the translation of NL logic into formal TL, ignoring a system's capacity to ground atomic propositions"*；Table 4 的高分是 *"an overconfident estimation of translation performance as grounding is not considered."*

⭐ **一个 lifted 上 100% 的系统，一旦要求绑定到具体元素，掉到 46–54%。**

**它支撑哪一句**：⭐ 直接支撑「**「说出问题所在」与「把它绑定到具体模型元素」是两个难度量级**」。我们的方法臂被要求做后者（断言必须绑到具体 state / event / transition / variable），基线臂只需做前者（「这里语义不清」不指名任何元素）。⭐ 而 grounding 恰恰是文献里被量化出来的那个**几十个百分点的落差**。⭐⭐ 这是本论证与「绑定」这个具体要求**最贴合**的一条。

**强度**：⭐ **强类比证据**。⭐ 实验结构（分段给 ground truth、分离 lifted 与 grounded）与我们要说的事高度同构；⛔ 但它测的是 NL→LTL 翻译系统，⛔ 不是缺陷发现，⛔ 也不涉及「人工语义判定同一指标」。

**局限**：⚠️（1）⛔⛔ **arXiv 预印本，无同行评审** —— 引用时必须标明，且不宜作为唯一支柱。（2）⛔ **对象是 LTL，同样越界**，按护栏二只能用于层一并标明对象。（3）它自己是 benchmark 论文，有把既有工作说低的动机；⚠️ 但它给的是分段 ground truth 下的可复核数字，不是主观评断。（4）Warehouse 的 80 类字典难度可能不代表一般情形。（5）v1→v2 有修订，引用须钉版本。

### B-3 · Cosler et al. CAV 2023（nl2spec）—— 仅作方法论旁证：**形式化本身被该社区当作「易错且耗时」的前提，故设计成人在环**

**引用**：Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, Caroline Trippel (2023). *nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models.* CAV 2023 (vol. 2), pp. 383–396. **CAV = CCF A**（形式化方法 A 类会议）。DOI [10.1007/978-3-031-37703-7_18](https://doi.org/10.1007/978-3-031-37703-7_18) · arXiv: [2303.04864](https://arxiv.org/abs/2303.04864)

**它实际做了什么**（读的是 arXiv 摘要页全文 + DBLP 核 venue；⛔ 未取正文表格）：把 LLM 生成的形式化拆成 sub-translation（每个子公式回指它来自哪段自然语言），让用户 *"iteratively add, delete, and edit these sub-translations to amend erroneous formalizations"*。摘要给出的前提是手写形式规约 *"an error-prone and time-consuming manual task."* 他们另做 user study 造了一个 challenging dataset。

**它支撑哪一句**：⭐ 只支撑一个较弱的句子：「**形式化环节被形式化方法社区本身当作独立的、易错的难点**，以至于 CCF A 会议上的方法要专门为它设计人在环纠错机制」—— 即形式化不是「把已知的东西写下来」这么廉价的一步。

**强度**：⚠️ **仅相关**。⛔ 它不提供两形态对比数字。⛔ 不要拿它当承重引用。

**局限**：⚠️（1）⛔ **我只读到摘要，未取正文的准确率表** —— ⛔ 因此本条不得引用任何数字。（2）对象是 LTL，越界，同 B-1/B-2。（3）它的动机陈述是 related-work 式的自我论证，⛔ 不是实测。

### B-4 · Endres et al. FSE 2024（nl2postcond）—— ⭐⭐ **同一件事：干净基准上形式化 81% 有效，真实代码上只 12.2%**；⭐ 且 venue 最硬

**引用**：Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, Shuvendu K. Lahiri (2024). *Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions?* Proc. ACM Softw. Eng. (PACMSE), FSE 2024 issue; FSE'24, Porto de Galinhas, Brazil, July 15–19, 2024. **FSE = CCF A**。arXiv: [2310.01831](https://arxiv.org/abs/2310.01831)

**它实际做了什么**（读的是 arXiv v2 全文 PDF，§4.1 / §4.2 / Table 4 / RQ 摘要框）：定义 `nl2postcond` 问题 —— 把代码旁的**非形式化自然语言**（docstring / Javadoc / 注释）转成**可程序化检查的 assertion（后置条件）**。用两个指标评：**correctness**（是否忠于文档意图）与 **discriminative power / bug-completeness**（能否拒掉错误实现）。跑 GPT-4 / GPT-3.5 / StarChat，两个基准：EvalPlus（164 个干净的 HumanEval+ 问题，docstring 完整描述）与 Defects4J（525 个真实历史缺陷）。

**关键数字**（逐条取自正文）：

| | EvalPlus（干净基准） | Defects4J（真实代码） |
| :-- | :-- | :-- |
| 逐条后置条件 test-set-correct | **77%**（最佳 prompt 变体） | accept@10 至 0.75 |
| 至少一条正确的问题占比 | **96%**（158/164） | — |
| 能区分错误实现的比例 | **至多 81%** 平均 | ⛔ GPT-4 至多 **47/525 = 9%** |
| 全部模型 × 全部 prompt 变体合起来 | 杀掉全部 mutant 的例子至多 62.2% | ⛔ **70 个 buggy method / 64 个缺陷 = 全部 525 个的 12.2%** |

⭐ **落差约 7 倍：81% → 12.2%。** ⭐ 作者自己给的原因之一逐字：*"(a) the comments not being completely descriptive, and (b) the increased program and object complexity in Defects4J"*。⭐ 另有一个正面案例（Apache Commons CLI）作者明确写 requirement *"is clearly specified in the Javadoc"*，GPT-4 由此生成的后置条件成功抓到该缺陷 —— ⭐ 即「NL 里写清楚了」时形式化能成，⛔ 而这种情形在 525 个里只占一成多。

⭐ 还有一个对我们方法臂形态直接有用的细节：他们把后置条件拆成九类原子成分，发现**最弱的一类（Type Checks）在自然缺陷上只杀掉 14%**、平均只 27%；⛔ 而最强一类平均杀 89%。⭐ 即**同为「形式化断言」，谓词选得对不对决定几十个百分点** —— ⭐ 这支撑我们「谓词选择是方法主体」的立场（⚠️ 与 [../story/paper_story.md](../story/paper_story.md) 的 C-③ 差异化落点一致）。

**它支撑哪一句**：⭐ 支撑「**从自然语言描述到可机械求值断言之间，存在被 CCF A 会议实测过的巨大落差；且这个落差在真实（而非基准）制品上放大约一个数量级**」。⭐ 推到我们的两臂：基线臂交付的正是「非形式化自然语言」那一端，方法臂交付的是「可程序化检查的断言」那一端，⛔ 而后者的成功率在文献里从来不等于前者。

**强度**：⭐⭐ **强类比证据，且 venue 最硬（CCF A）**。⭐ 它是本论证里**唯一一条同时满足「CCF A」「2022 年后」「直接测 NL → 可机械求值断言」的证据**，⭐ 建议作为主引之一。

**局限**：⚠️（1）⛔ **12.2% 有混淆**：作者自陈部分原因是**注释本身没写全**，⛔ 因此不能把这 7 倍落差全部归给「形式化难」；⚠️ 论文里引用时必须说清这一点，⛔ 否则是过度解读。（2）对象是程序后置条件，⛔ 不是状态机制品；⭐ 但它在 project_1 的边界外**性质更温和** —— 它不涉及时钟与并发，属于 [README.md](./README.md) 护栏二允许的「层一形态性质 + 标明对象」。（3）它的结论方向是**乐观的**（摘要说 *"generally correct and able to discriminate incorrect code"*、*"has the potential to be helpful in practice"*），⛔ 因此**不得把它引成「形式化不行」的证据**；⭐ 我们要用的是那个**基准 vs 真实的落差**，不是它的主结论。（4）Defects4J 的 9% / 12.2% 是「discriminating w.r.t. regression 与 trigger tests」口径，⛔ 不是「人工判定语义等价」口径。

---

## 3. 子命题 C：报告了问题 ≠ 报告可被下游执行（bug report actionability）

### C-1 · Bettenburg et al. 2008 —— ⭐ 奠基性，且给出**负相关**这个极强数字

**引用**：Nicolas Bettenburg, Sascha Just, Adrian Schröter, Cathrin Weiss, Rahul Premraj, Thomas Zimmermann (2008). *What Makes a Good Bug Report?* FSE 2008 (SIGSOFT '08/FSE-16), pp. 308–318. **CCF A**（软件工程 A 类会议 FSE）。DOI [10.1145/1453101.1453146](https://doi.org/10.1145/1453101.1453146) · 全文 PDF: [thomas-zimmermann.com/publications/files/bettenburg-fse-2008.pdf](https://thomas-zimmermann.com/publications/files/bettenburg-fse-2008.pdf)

**它实际做了什么**（读的是上述 PDF 全文）：向 APACHE / ECLIPSE / MOZILLA 的 2,226 名 developer 与 reporter 发问卷，466 份回复；经一致性检查后剩 developer 130 份（剔 26 份 = 16.7%）、reporter 215 份（剔 95 份 = 30.6%）。问 developer「哪些内容你用过 / 哪三项最重要」，问 reporter「你提供过哪些 / 哪三项最难提供」。

**关键数字**（逐项取自 Table 2 / Table 3 与 §3.3）：

| 项目 | developer 侧重要性 | reporter 侧难度 |
| :-- | :-- | :-- |
| steps to reproduce | **83%** | 51% |
| stack traces | **57%** | 24% |
| test cases | **51%** | **75%**（最难项） |
| observed behavior | 33% | 2% |
| expected behavior | 22% | 3% |

⭐ **最强的一个数字**：developer 认为重要的东西 与 reporter 实际提供的东西，**Spearman 相关系数 = −0.035**（原文 §3.3：*"The Spearman correlation of -0.035 between what developers consider as important and what reporters provide shows a huge gap"*）。而「developer 用过什么 vs reporter 提供什么」的相关系数是 0.321（原文自评 *"far from being ideal"*）。⭐ 且原文 Figure 3(c) 说明 **reporter 其实知道 developer 需要什么** —— 原文：*"ignorance of reporters is not a reason for the aforementioned information mismatch."* ⭐ 即差距不来自「不知道」，而来自「提供不出来」。

⭐ **另一个直接可用的细节**：Table 2 的「Problems with bug reports」一栏里，developer 报告的问题严重度包括 **incomplete information 74%**（远超其它）、**unstructured text 34%**、too long text 26%、**prose text 18%**、non-technical language 19%。⭐ 即「散文式表述」本身被 developer 列为一类问题，⛔ 但严重度只 18%，**不宜夸大**。

**它支撑哪一句**：支撑「**能指出一个问题 ≠ 交付一个可被下游执行的发现**；两者之间的缺口是被实测过的，而且大到相关系数为负」。也支撑「最有下游价值的形态（test case / steps to reproduce）恰恰是最难产出的形态」—— ⭐ 这正是我们两臂的关系：方法臂被要求交付难产出的那种形态。

**强度**：⭐ **类比证据（强）**。⛔ 它不是关于 LLM、不是关于状态机、也不是关于「同一指标比较两种形态」。⭐ 但它是软件工程里对「报告 ≠ 可执行」这个缺口最经典、最常被引的量化来源，且 75% vs 51% 的「最有用 = 最难给」倒挂关系与我们的处境同构。

**局限**：⚠️（1）2008 年，前 LLM 时代；（2）问卷法，自我报告；（3）一致性检查剔掉了 30.6% 的 reporter 回复，样本有筛选；（4）⛔ 它测的是「reporter 提供了什么」，**不测「评判者如何给分」** —— ⛔ 因此它支撑不了「尺子偏斜」这一步，只支撑「形态之间存在难度落差」。

---

## 4. 子命题 D：评测方法学 —— 不同输出形态用同一指标比较会引入偏差

### D-1 · Le et al. ICSE 2019 —— ⭐⭐ **对称一致性统计会结构性地惩罚「可靠但不完备」的那一方，且惩罚到低于随机**

**引用**：Xuan-Bach D. Le, Lingfeng Bao, David Lo, Xin Xia, Shanping Li, Corina Păsăreanu (2019). *On Reliability of Patch Correctness Assessment.* ICSE 2019, pp. 524–535. **ICSE = CCF A**。DOI [10.1109/ICSE.2019.00064](https://doi.org/10.1109/ICSE.2019.00064) · arXiv: [1805.05983](https://arxiv.org/abs/1805.05983) · 作者 PDF: [xin-xia.github.io/publication/icse192.pdf](https://xin-xia.github.io/publication/icse192.pdf)

⚠️ **作者更正**：是 **Xuan-Bach D. Le**，⛔ **不是** Claire Le Goues（后者不是本文作者）。⚠️ 引用时别写错。

**它实际做了什么**（读的是上述搜索命中的 ICSE 页 + arXiv 版内容，Table 5）：对 8 种 APR 工具生成的 189 个补丁，请 **35 名职业开发者**独立标注正确性，建 gold set（152 incorrect / 35 correct）。然后把「用自动生成的独立测试集（ITS，由 DiffTGen 与 Randoop 生成）判定」这种自动判据，与人类 gold set 算**评审者间一致性**。

**关键数字**：

| 判据 | Cohen κ | Krippendorff α |
| :-- | :-- | :-- |
| **人类互评**（35 名职业开发者） | **0.691** | **0.734** |
| DiffTGen ITS vs ALL-AGREE | **0.078** | **−0.32** |
| Randoop ITS vs ALL-AGREE | 0.073 | −0.30 |
| 两者合并 | 0.158 | −0.057 |

⭐⭐ **本条的要点不是「自动判据不好」，而是那个数字的成因**：原文指出 ITS 标为 incorrect 的补丁**确实都是 incorrect**（零假阳性），⛔ 而它只能标出不到五分之一的错误补丁 —— ⭐ 即这是一个 **sound but incomplete** 的判据。⭐ 把它压成 correct/incorrect 两值再算**对称的** κ / α，结果必然难看到低于随机（α 为负）。⭐ **难看来自判据形态与统计量形态的不匹配，⛔ 不来自判据质量。**

**它支撑哪一句**：⭐⭐ 直接支撑「**同一把尺子套在形态不同的两方上，会系统性地惩罚其中一方，且惩罚幅度与那一方的真实质量无关**」。⭐ 这是本文件里**唯一一条真正落在「评测方法学」层面、并且在 CCF A 会议上给出可复算数字的证据**。

**强度**：⭐⭐ **直接证据（就「指标形态不匹配导致结构性不公」这一点而言）**，⛔ 但它的两方是「人类判定 vs 自动测试判据」，⚠️ 不是我们的「散文 vs 形式化断言」。⭐ 机制同构：**一方给的是有确定真值但覆盖有限的判决，另一方给的是覆盖全但需解释的判断**；⛔ 我们的两臂正是这个关系（方法臂只在谓词覆盖到的地方发声，基线臂可以在任何地方发声）。

**局限**：⚠️（1）2019 年，⛔ 早于「2022 年起优先」；⭐ 但它是该主题的奠基工作，符合「更早的只在奠基性时收」。（2）领域是 APR 补丁正确性，⛔ 不是缺陷发现。（3）⭐ ⚠️ **它与 [assertion_output_form_evidence.md](./assertion_output_form_evidence.md) 的 [65] 是同一篇** —— ⚠️ 那边用它警告「不要用对称统计评价见证式判据」，⭐ 这边用它证明「尺子会结构性偏斜」。⛔ 论文里若同时引，须避免让读者以为是两条独立证据。（4）⛔ 我核的是 ICSE 页 + 检索到的 Table 5 转录，⚠️ **未亲自打开 PDF 逐格核 Table 5**；⭐ 引用前应补这一步。

### D-2 · Bulian et al. EMNLP 2022 —— ⭐ 匹配式指标的判决取决于**表面形态**而非内容，⚠️ 但方向对我们只是半有利

**引用**：Jannis Bulian, Christian Buck, Wojciech Gajewski, Benjamin Börschinger, Tal Schuster (2022). *Tomayto, Tomahto. Beyond Token-level Answer Equivalence for Question Answering Evaluation.* EMNLP 2022, pp. 291–305. **EMNLP = CCF B**。ACL Anthology: [2022.emnlp-main.20](https://aclanthology.org/2022.emnlp-main.20/) · DOI [10.18653/v1/2022.emnlp-main.20](https://doi.org/10.18653/v1/2022.emnlp-main.20)

**它实际做了什么**（读的是 ACL Anthology 页 + 上述 PDF 正文 §3–§5）：论证 QA 里用有限标注答案集 + exact match / token-F1 打分会**低估**系统真实表现。收集 SQuAD 上 **14,170 条人工评级 / 8,565 个 (context, question, reference, candidate) 四元组**（论文另称总计 >23k judgements），人工一致性 Krippendorff **α = 0.84**、多标注样本 >88% 完全一致。据此定义 **asymmetric answer equivalence (AE)**，并训练 BERT matching (BEM) 指标替代 F1。

**关键数字**：⭐ **在「不是 exact match」的候选里，人工评级认为 55% 其实与参考答案等价**（SQuAD train 候选上高达 **69.9%**）。⭐ 即 exact match 把过半数正确答案判错，⛔ 而这完全由表面形态决定。BEM 在 NQ-Open 上与人工独立判定的一致率 **87%**。

⭐ **一个对我们特别有用的设计细节**：他们的 AE 定义是**刻意不对称**的 —— 候选必须「not completely different」且「containing **at least as much** relevant information and **not more** irrelevant information」才算等价。⭐ 也就是说：为了让指标公平，他们不得不**显式承认「更详细」与「更含混」不能同等对待**，并把这一点写进判据定义。

**它支撑哪一句**：⭐ 支撑「**同一指标下判对判错，可以主要由输出的表面形态决定**」，以及「**要让跨形态比较公平，判据必须显式处理形态差异（如 AE 的不对称设计），而不能只问「说的是不是同一件事」**」。⭐ 后半句正是我们的指标（「有没有指出同一处缺陷」）所缺的。

**强度**：⚠️ **类比证据（中等）**，⛔ 且**方向只有一半对我们有利**。⚠️ ⛔ **必须说清**：它证明的是**严格自动匹配会低估自由形态答案**（即严格指标伤自由文本），⛔ **不是**「宽松人工判定会高估自由文本」。⭐ 我们能用的是它的**元层结论**（判决由形态决定 + 公平判据须显式不对称），⛔ 不是它的方向。

**局限**：⚠️（1）⛔ 方向不直接支持我们，若引用不当会**反被用来打我们**。（2）领域是抽取式 QA，⛔ 与缺陷发现相距较远。（3）它的判据是**自动指标 vs 人工**，⛔ 我们的判据本身就是人工。（4）55% 的分母是「非 exact-match 候选」，⛔ 不是全部候选，⚠️ 不要写成「exact match 判错了 55% 的答案」。

---

## 5. ⚠️⚠️ 反向证据（对我们不利，必须一并报）

### R-1 · Tam et al. EMNLP 2024 —— ⛔ **结构化输出确实会降低推理能力**，且这是本论证最大的威胁

**引用**：Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin, Hung-yi Lee, Yun-Nung Chen (2024). *Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models.* EMNLP 2024 **Industry Track**, pp. 1218–1236. **EMNLP = CCF B**（⚠️ Industry Track，非主会）。ACL Anthology: [2024.emnlp-industry.91](https://aclanthology.org/2024.emnlp-industry.91/) · DOI [10.18653/v1/2024.emnlp-industry.91](https://doi.org/10.18653/v1/2024.emnlp-industry.91) · arXiv: [2408.02442](https://arxiv.org/abs/2408.02442)

**它实际做了什么**（读的是 arXiv v3 全文 HTML，含 Table 1/2/9/11）：把「格式约束强度」排成五级 —— natural language → NL-to-Format（先自由生成再转格式）→ Format-Restricting Instructions (FRI) → JSON-mode 约束解码 → JSON-Schema (CFG)。在 3 个推理任务（GSM8K、Last Letter Concatenation、Shuffled Objects）与 4 个分类任务（DDXPlus、MultiFin、Sports Understanding、Natural Instructions Task 280）上，跨 gpt-3.5-turbo-0125 / claude-3-haiku / gemini-1.5-flash / LLaMA-3-8B-Instruct / Gemma-2-9B-Instruct（附录另加 gpt-4o-mini、Mistral-7B）比较。

**关键数字**：

GSM8K，text vs JSON（Table 9，零样本）：GPT-3.5 Turbo **76.6 → 49.3**；LLaMA-3-8B **74.7 → 48.9**；Claude-3-Haiku **86.5 → 23.4**；Gemini-1.5-Flash 89.3 → 89.2（几乎不变）；Gemma2-9B 86.5 → 84.2。Last Letter，text vs JSON：GPT-3.5 **56.7 → 25.2**；LLaMA-3-8B **70.1 → 28.0**；⭐ 但 Gemini-1.5-Flash **65.4 → 77.0（反向变好）**。

JSON-mode（真约束解码，Table 11）上 Last Letter 近乎崩塌：GPT-3.5T **1.78**、Gemini-1.5F **0.67**、LLaMA3-8B 7.56。⭐ 作者给出的机制解释很关键：**100% 的 GPT-3.5-Turbo JSON-mode 回答把 `answer` 键排在 `reason` 键之前**，于是链式思维被结构本身取消，退化成直答。

gpt-4o-mini + CFG Structured Output（Table 2）：GSM8K NL **94.57** / FRI 87.17 / JSON-Mode 86.95 / JSON-Schema 91.71；Shuffle Obj NL **82.85** / 81.46 / 76.43 / 81.77；Last Letter NL 83.11 / 84.73 / 76.00 / **86.07**。⭐ 即自由文本在 3 项中 2 项领先，⛔ 但 JSON-Schema 把 JSON-mode 的损失基本补回来了。

⭐ **作者排除了「解析失败」这个替代解释**：LLaMA-3-8B 在 Last Letter 上 JSON 解析失败率仅 **0.148%**，而分差约 38 点；Gemini / GPT-3.5 基本无解析失败。他们还专门做了 "Perfect Text Parser" 来分离格式错误与真实推理失败。

⭐ **反向的一半（对我们有利）**：分类任务上格式约束**帮忙**。DDXPlus 上 Gemini-1.5-Flash text **41.6 → JSON 60.3**，JSON-mode 下达 **84.92**；GPT-3.5 44.1 → 55.5；Gemma2-9B 22.9 → 53.0。GPT-3.5 在 Sports 上 67.2 (σ 26.8) → 80.0 (σ 3.3)。作者解释：约束答案空间减少了选择错误，而自由文本 *"may introduce distractions."* ⭐ 结论是**任务依赖**：伤推理、帮结构化分类。

**它支撑哪一句**：⛔ 它支撑**对方**的一句 —— 「你们方法臂表现低，可能不是因为尺子偏斜，而是因为你们逼模型输出结构化，本身就削弱了它的能力」。⭐ ⚠️ **这是对我们论证最直接的替代解释，必须在论文里正面处理。**

**威胁大小与可反驳之处**（⭐ 逐条，均基于上面读到的数字）：

1. ⭐ **它是「能力被削弱」的证据，⛔ 不是「尺子公平」的证据。** 严格说它与我们的命题**不互斥**：完全可以同时成立「结构化削弱了方法臂的能力」与「同一指标对散文更宽容」。⭐ 论文里应当两者并列承认，⛔ 而不是驳倒它 —— ⚠️ 只驳不认会被 reviewer 抓。
2. ⭐ **效应是模型依赖且方向不一致**：Gemini-1.5-Flash 在 GSM8K 上几乎无损（89.3 → 89.2）、在 Last Letter 上反向变好（65.4 → 77.0）。⛔ 因此「结构化必然伤能力」不成立。
3. ⭐ **机制是可规避的**：最大的崩塌（JSON-mode Last Letter → 1.78）的原因是**键序把 CoT 取消了**，而这是 schema 设计缺陷，不是形式化本身的代价。JSON-Schema 相对 JSON-mode 的回升（GSM8K 86.95 → 91.71）也说明约束方式比约束存在与否更重要。
4. ⭐ **任务类型不匹配**：它测的是 GSM8K / 字母拼接 / 物体追踪这类**短链数学与符号推理**，⛔ 不是「在一份模型上定位缺陷」。⭐ 而它在**分类**任务上的结论是结构化**帮忙**（DDXPlus 41.6 → 84.92）；「这份模型的这一处是否违反某谓词」在形态上更接近分类而非 GSM8K。
5. ⚠️ **venue 是 Industry Track**，不是 EMNLP 主会；⛔ 引用时不宜写成「EMNLP 2024」而不加限定。

---

## 进度与待办

- [x] 子命题 C 首条（Bettenburg FSE 2008，已取原文核数字）
- [x] 反向证据首条（Tam EMNLP 2024 Industry，已取原文核 Table 1/2/9/11）
- [ ] 子命题 A（评判宽松度差异）
- [ ] 子命题 B（NL → 形式化的能力落差）⭐ 最重要
- [ ] 子命题 D（评测方法学）
- [ ] 措辞拟稿 / 诚实评估 / §References
