# 「可机械求值断言」作为输出形态的文献证据（2026-08-12 调研）

**性质**：⭐ 这是一份**文献证据留存**文件，服务后续把结论写进论文口径。⛔ 不在此处下裁定，⛔ 也不复述数字到别处——⭐ 要用就回这里核。

⚠️ **核验口径**：调研要求每个数字都取自**实际取到的原文**（arXiv / ACL / 出版方 PDF 或开放全文）；⛔ 凡只在检索摘要里出现、取原文核不到的，一律标 **⛔ 原文未核到并禁引**。⭐ 四条并行检索共揪出 **9 处 snippet 与原文不符**，集中在 §5。

⚠️ **本文件是代理调研产出**。⭐ 其中最承重的两处数字（CheckEval 的 ACL PDF Table 2、Infer 的 CACM 全文段落）由调研方自述独立复核过；⛔ 本仓库尚未逐条人工复验。⭐ 引用进论文前须逐条取原文。

---

## 1. ⭐ 六种输出形态 × 五个维度

维度定义（⛔ 全文一致）：**D1 可判定性**（能否不经人类解释得出唯一布尔真值）· **D2 可复算性**（第三方能否独立重算出同一裁定）· **D3 是否锚在需求条目** · **D4 能否作回归防护** · **D5 对下游修复的可用性**。

| 输出形态 | D1 | D2 | D3 | D4 | D5 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **A. 散文式评语** | ⛔ 反面：换序即翻转 [1][2]；SE 场景换序一致性 **&lt;25** [4] | ⛔ 反面：温度 0 仍不确定 [7][8]；改措辞即改结论 [9][10][3]；快照消失 [11] | ⚠️ **无文献**（形态不强制） | ⚠️ **无文献** | ⛔ 反面：无外部判据时自纠使结果**下降** [12]；模型自诊断 33.3% vs 人类 52.6% [13]；⭐ 抽掉报错文本修复增益**全部消失** [14] |
| **B. 只给定位（lint 式）** | ⛔ 反面：判据在人脑里——Google 把 FP 定义成「用户选择不处理」[16] | 形态支持，⚠️ 但无实测 | ⛔ 反面：⭐ 同一分析、同一 FP 率，批量投递修复率≈0，绑到 diff 上 **&gt;70%** [17] | ⚠️ 部分（规则会再触发，⛔ 但无「这条缺陷是否消失」的判据） | ⛔ 反面：「告警文案差」痛点排名**高于**误报 [19]；缺「显然的理由」则行为完全不变 [20] |
| **C. 只给性质公式** | ✅ 支持 | ✅ 支持 | ⛔ **反面：真空性**——首轮约 **20%** 公式平凡为真 [22]；通过不说明覆盖了什么 [23] | ⚠️ 部分（⛔ 真空通过是**静默**的 [22][26][27]） | ⚠️ 部分/反面（无定位，须转反例，继承 D 行全部问题） |
| **D. 反例轨迹** | ✅ 支持 | ✅ 支持，⭐ witness 可被**独立**验证 [28][29][30] | ⛔ **反面：无任何绑定** [31][32] | ⚠️ 部分 [29] | ⛔ 反面：轨迹是症状不是原因 [34]；实测轨迹长至 248 步而原因仅 0–7 步 [34]；⚠️ 116 篇原始研究只 **6 篇（6%）**做过用户实验 [35] |
| **E. 测试用例** | ⭐ **强支持** | ✅ 支持 | ⛔ 反面：不绑需求，⚠️ 且判的是行为而非规约符合性 [36][37] | ⭐ **强支持** [38][39][40]，⛔ 但内含反面：回归 oracle 钉住**当前行为**，若当前行为有缺陷则把缺陷固化成期望 [38] | ⚠️ 支持但**上限明确**：弱 oracle 下过拟合 [41][42][43][44]；⭐ 自动生成测试能消回归型过拟合、⛔ 对「修不全」型**几乎无效，原因就是 oracle problem** [45] |
| ⭐ **F. 可机械求值断言 + 需求绑定（本文形态）** | ✅ 构造性；⭐ **有实测**：把散文判断拆成二值可核项，评审者间一致性 α **0.09 → 0.48**（Top-3 模型 0.07→**0.65**）[47] | ✅ [47]，⚠️ 但生成环节本身仍不可复现 [11]，⛔ 须分层陈述 | ✅ 构造性；锚定价值有实证 [17][48][49][50] | ⚠️ 部分：DbC / RV 的框架性支持 [51][52][53] + Orstra [38]；⛔ **人手写断言在演化中捕获回归的实测：未找到**（见 §3.5） | ✅ ⭐ 同一合成器只换 oracle，正确率由「不到一半」升到 **12/12** [54]；测试稀薄时约束驱动 **16 正确 vs 测试驱动 0–4** [55]；契约驱动修复 **59%** 达「专业程序员水平」[56]；强规约使发现缺陷数**翻倍** [57] |

### ⭐ 表里最强的两格

**① D3 那格的 [17]** —— ⭐ **全库唯一把「锚定」从「准确率」中分离出来的自然实验**。Facebook 的 Infer 先做批量夜跑，逐字：*"We assigned 20–30 issues to developers, and almost none of them were acted on. We had worked hard to get the false positive rate down to what we thought was less than 20%, and yet the fix rate… was near zero."* 改到 diff time 后：*"the fix rate rocketed to over 70%. **The same program analysis, with same false positive rate**, had much greater impact when deployed at diff time."*

⭐ **分析不变、误报率不变，只改变发现挂在哪里，处置率从 ≈0 到 &gt;70%。**

**② D1/D2 那格的 [47] CheckEval（EMNLP 2025）** —— ⭐ 唯一直接测「散文式判定 vs 二值可核项」可靠性的论文。ACL PDF Table 2 全表：12 个评审模型上，SummEval 的评审者间一致性（Krippendorff α / Cohen κ）G-Eval **0.09 / 0.19**、SEEval 0.08 / 0.14、⭐ CheckEval **0.48 / 0.48**；Large 组（70–123B）CheckEval **0.67/0.67** vs G-Eval 0.05/0.16。

⚠️ ⛔ **但必须同时说清代价**：它对**人类相关性**的提升只是小幅（GPT-4o SummEval ρ 0.32→0.50）。⭐ **结构化带来的是可靠性约 5 倍，⛔ 不是效度。** ⚠️ 这个区分若不写清，reviewer 一定会抓。

---

## 2. ⭐ 逐条已建立结论（⛔ 每条附文献做了什么实验）

### 2.1 可判定 oracle 对自动修复的价值 —— ✅ 已建立，且有**受控对照**

**结论 1：弱 oracle 不只是不完备，⛔ 而是不可靠（unsound），失败率极高。**

- **Qi, Long, Achour, Rinard（ISSTA 2015）**[41]：把已发表的 GenProg / RSRepair / AE 补丁下载回来重跑并**与正确输出逐一比对**。105 缺陷上 GenProg 只 **2/105** 正确、RSRepair **2/24**、AE **3/105**；⭐ **110 个 plausible GenProg 补丁中 104 个语义上等价于一次纯删功能的修改**。
- **Long &amp; Rinard（ICSE 2016）**[43]：穷尽刻画搜索空间。⭐ **45/69 的空间里根本不存在正确补丁**；plausible 比正确多**数百到一千倍**。⭐ php 是唯一例外（只多几十倍），⭐ **论文把原因直接归给 oracle 强度**（测试集多一个数量级）——⭐ **这是文献里最接近「oracle 强度」自然实验的一段**。
- **Smith, Barr, Le Goues, Brun（FSE 2015）**[42]：998 个学生程序，每个配**两套独立开发**的测试集，一套训练一套留出。GenProg 补丁训练集 100% 通过、留出集中位数只过 **75.0%**。⭐ 训练集覆盖率越高、过拟合显著越少（$p &lt; 0.001$）。
- **Le, Thung, Lo, Le Goues（EMSE 2018）**[44]：语义型修复同样过拟合（Angelix **75%**、CVC4 80%、SemFix 90%）。⚠️ ⛔ **重要区别**：采样到 25/50/75% 时 Angelix 过拟合率 84%/94%/78% —— ⭐ 「覆盖率换质量」这条在**语义型修复上不成立**。

**结论 2：oracle 强度是主导变量 —— ⭐ 三个受控对照，⛔ 不是相关性。**

- ⭐ **SemGraft（ICSE 2018）**[54] **全库最干净**：复用 Angelix 的合成器，并**刻意构造 Angelix′**（喂同一份规约）使搜索空间完全相同，⭐ **唯一差别是 oracle**。论文原话：*"Angelix′ that relies only on tests repaired **less than half** of the defects correctly."* ⚠️ 从表逐行数出 **4/12 vs 12/12**（⛔ 该计数是调研方从表格计数，正文只给「不到一半」，⛔ 引用须分层）。代价：平均 45 min vs 15 min。
- ⭐ **ExtractFix（TOSEM 2021）**[55] 第二强，⭐ 分层结果是关键：在测试充足的 ManyBugs 上 Prophet 7 / Angelix 5 / ExtractFix 12；⭐ 在**测试稀薄**基准上 Prophet 2 / ⛔ **Angelix 全部过拟合（0）** / ExtractFix **16**。⭐ **测试驱动的塌了，判据驱动的没塌。**
- ⭐⭐ **Baldur（FSE 2023）**[14] 是**因果证明，且最适合本文引用**：6,336 条 Isabelle/HOL 定理。逐字：*"we trained another repair model that is **given** the same information, **except that it does not see** the error message… while it **is able to prove additional theorems**, it does not surpass the performance of the **generate** model when normalized for inference cost. This suggests that the information in the error message is **crucial** for the observed gains of the repair approach."* ⭐ **pass/fail 判决与采样预算都不变，只抽掉 oracle 的诊断输出，全部修复增益消失。** ⭐⭐ **这直接支持「判据要带证据链，不能只给真值」——即 C-③。**
- 契约侧 **AutoFix（TSE 2014）**[56]：204 个缺陷，86 (42%) 得 valid fix，其中 **51/86 (59%)** 是 *proper*（「质量可与专业程序员相比」）。⚠️ ⛔ **59% 与结论 1 的 2/105 不可直接比**（语言、基准、分母全不同），⭐ 只能定性对照。
- 强规约收益独立测量：**Polikarpova et al.（ICSE 2013）**[57] 逐字 *"testing against strong specifications detects **twice as many bugs** as standard contracts."*

**结论 3：⭐ 有一条生成更多测试无法突破的硬天花板。** **Yu et al.（EMSE 2019）**[45] 决定性：把过拟合分解成「修不全」与「引入回归」。⭐ **引入回归**：18 个受影响版本中缓解 16、彻底消除 6；⛔ **修不全**：只影响 4 个版本、缓解 2 恶化 2。摘要逐字：自动测试生成 *"is effective in alleviating one kind of overfitting issue — regression introduction, but **due to oracle problem**, has minimal positive impact on… incomplete fixing."* ⭐ **机制清楚：修补前的程序本身就是免费的回归 oracle，⛔ 但对程序从来没做对过的行为，它根本不提供 oracle。** ⚠️ 该论文 RQ2 答案框写「16/19」与正文 18 个版本不一致，⛔ 引正文分解、不要引 16/19。

**结论 4（LLM 语境）：⭐ 有无可判定检查会改变自修复的量级。** **Self-Debugging（ICLR 2024）**[59] 最干净：**同一方法**跑在有/无可判定检查的基准上 —— Spider（无单测）提升 **2–3%**，TransCoder / MBPP（有单测）提升至 **12%**。⭐ 作者把无测试的变体直接叫 *"rubber duck debugging"*。⚠️ **Olausson et al.（ICLR 2024）**[13] 给反向边界：可执行判据在场时，若诊断由模型自产，⛔ 等预算下自修复可以**比不修复更差**（APPS 0.97×）；⭐ 人类反馈 52.60% vs GPT-4 反馈 33.30%；⚠️ 参与者 7/80 次表达不确定，⛔ **GPT-4 0/80**。

### 2.2 可执行判据对回归确认的价值 —— ✅ 已建立，⭐ 且有反向量化

**结论 5：⛔ 没有可执行判据时，修复确认退化为人类判断，⚠️ 而人类判断被实测为约 10% 错误。** ⛔ **文献里没有一句话直接这么说**（见 §3.3），⭐ 必须复合引用：

- ⭐ **Ye, Martinez, Monperrus（EMSE 2021）**[60]：638 个补丁，在**开发者修好的正确版本上**生成 **4,477,707** 个 RGT 测试。⭐ **97 个此前被人工判为「语义等价正确」的补丁中，10 个（10%）其实过拟合 —— 全部经原作者确认。** 该判据自身假阳性率 6/257 = **2.3%**、对已知过拟合召回 **274/381 (72%)**。作者自评：这是 *"a key result for convincing the community to switch from manual patch assessment to automatic patch assessment."*
- **Böhme et al.（FSE 2017）**[61]：27 个真实缺陷、12 名专业开发者（共 29 个工作日）提交 290 个补丁。⭐ **282/290 (97%) plausible 且通过测试，⛔ 但只 182 (63%) 实际正确** —— 而这 63% 靠两名研究者花约两天代码评审定下。108 个错误补丁中 **60 个引入回归**。
- **Xiong et al.（ICSE 2018）**[62] 给出最好引用的一句：*"test oracles cannot be automatically generated in general, known as the oracle problem. As a result, existing approaches either **require human to determine test results, which is too expensive in many scenarios**, or rely on inherent oracles such as crash-free."*
- ⭐ **同一补丁集上的三级阶梯**（⚠️ 唯一真正同分母的对比）：**39.4%**（静态分类、零执行 [63]）→ **56.3%**（动态启发式、无 oracle [62]）→ 72%（可执行判据 + 正确参考 [60]，⛔ 但集合更大、不可比）。⭐ 前两级同分母可比。
- **Shamshiri et al.（ASE 2015）**[64]：Randoop/EvoSuite/AgitarOne 在 357 个 Defects4J 缺陷上找到 199 (55.7%)，⛔ 但**只有 19.9% 的执行检出缺陷**。⭐ 要论证「单次生成测试不足以作修复确认判据」，⛔ 该引 19.9%。

⚠️⚠️ **一条方法论警告，⭐ 直接适用于本文的评测设计**：**Le et al.（ICSE 2019）**[65] 测出人类互评 $\kappa = 0.691$，⛔ 而 DiffTGen 作为判据 $\kappa = 0.078$、Krippendorff $\alpha = -0.32$（⛔ 比随机还差）。⭐ **这不是「可执行判据不好」的证据，而是评价方式的伪影**：一个见证式判据是 **sound but incomplete**（找到测试证明缺陷在，⛔ 找不到什么都不证明），⛔ 把它压成 correct/incorrect 再算对称一致性统计，**结构上保证难看**。⭐ **正确做法是像 [60] 那样分两个数报：已知坏样本上的召回 + 已知好样本上的假阳性率（72% 与 2.3%）。**

### 2.3 散文式输出的已知缺陷 —— ✅ 大量已建立，⚠️ 但要小心分母

**结论 6：换序即翻转，⭐ 且恰在判断困难处最严重。** **Wang et al.（ACL 2024）**[1]：GPT-4 判 Vicuna-13B vs ChatGPT 时冲突率 **46.3%**，ChatGPT 判同一对时 **82.5%**。⛔ **GPT-4 偏第一、ChatGPT 偏第二 —— 方向不一致，故无法用统一偏置修正。** ⭐ 关键性质：**冲突率与质量差距负相关**，⚠️ 即差距越小偏置越致命。对人类多数的准确率：GPT-4 **52.7%，κ = 0.24**；人类互评 71.7%，κ = 0.54。⚠️ ⛔ **判定 prompt 里已经写了「避免顺序影响判断」—— 指令无效。**

**结论 7：⚠️ 那个被反复引用的「80% 一致」是 S2 子集口径。** **Zheng et al.（NeurIPS 2023）**[2]：**S2**（只算非平局票、随机基线 50%）GPT-4 vs 人 **85%**、人 vs 人 81%；⛔ **S1**（含平局与位置偏置不一致票、随机基线 33%）GPT-4 vs 人 **66%**、人 vs 人 63%。⭐ **可辩护的说法是「GPT-4 达到人类互评上限」（两口径都成立），⛔ 不是「与人一致 85%」。** 位置一致性 Claude-v1 **23.8%**；冗长攻击（信息量不变）失败率 Claude-v1 **91.3%**。⚠️ ⛔ **自增强偏置的 10%/25% 被广泛当成既定结论，而原文明确拒绝确立**：*"our study cannot determine whether the models exhibit a self-enhancement bias."* ⭐ 另一条与本文最相关：**一致性随质量差距从 70% 单调升到近 100%** —— ⚠️ **评审在不需要评审的地方才可靠。**

**结论 8：与人类专家的一致性（chance-corrected）低，⚠️ 且在技术制品上更低。**
- **Judge-Bench（ACL 2025）**[3]：20 数据集、&gt;70,000 条人类判断。⭐ **17 个类别型任务上平均 Cohen κ：GPT-4o 0.28 ±0.32、Llama-3.1-70B 0.28、Command-R+ 0.10**，⛔ 个别行为负（DICES-990 **−0.24**）。⚠️ 两条对本文直接有用：⭐ 模型与**非专家**的一致性高于与专家；⛔ *"Chain-of-Thought prompting, few-shot prompts, and prompt paraphrases… none of these strategies leads to systematic improvements."*
- ⭐⭐ **Wang R. et al.（ISSTA 2025）**[4] 是 **SE 专属、最该引的一篇**：⭐ 人类互评天花板很高（Spearman ρ 83.07/75.42/74.20），⛔ 所以后面的失败不是标注噪声。逐字：*"methods with the highest accuracy on code translation and generation yield extremely low Agreement **below 25**"*；代码生成上「即使最好的方法也难达到 50 Accuracy」；⛔ 代码摘要上 *"all methods become completely unusable."*

**结论 9：⭐ 可复算性在温度 0 下也不成立。** **Ouyang et al.（TOSEM 2025）**[7]：829 个问题各请求五次。⭐ **已发表 TOSEM 数字**：五次里测试输出无一相同的任务占比 **75.76% / 51.00% / 47.56%**；⛔ CodeContests 在**温度 0** 下最坏 43.64%。逐字：*"Contrary to the widely held belief (and common practices), setting the temperature to 0 does not guarantee determinism in code generation."* ⚠️⛔ **arXiv v1 是 72.73/60.40/65.85，与已发表版不同，⛔ 务必引 TOSEM。**

**结论 10：⭐ 措辞是混淆变量，⛔ 不是实现细节。** **FormatSpread（ICLR 2024）**[9]：只动分隔符/大小写/空格这类**保义**扰动，⛔ **LLaMA-2-13B 上准确率跨度达 76 个百分点**，⛔ **模型排名会反转**。**Mizrahi et al.（TACL 2024）**[10]：⛔ **25 个任务中 15 个存在使模型排名负相关的改写对**。⭐ 以及 [3] 直接改写**评审 rubric**：Llama-3.1-70B 的 κ 由 −0.13 变 **−0.36** —— ⛔ **改写引入的方差超过信号本身。**

**结论 11：⭐ 可复现性在 SE 论文层面已经实测失败。** **Angermeir et al.（ICSE 2026）**[11]：85 篇 → 18 篇提供制品且用 OpenAI → ⛔ **只 5 篇可执行 → 5 篇全部无法完全复现**。⭐ 一篇报 79.9% 成功率，15 次重跑的 95% 区间是 **45.6%–55.3%**。⚠️ 反直觉：⛔ **ACM 制品徽章、固定次版本、多模型对比、pass@k 都与可复现性无相关。**

**结论 12：散文式理由不是产生该结论的推理的证据。** **Turpin et al.（NeurIPS 2023)**[66]：注入偏置特征 *"causing accuracy to drop as much as 36%, **despite the biasing features never being referenced in the explanations**."* ⭐ 风格压倒实质：[67] 测到 **Style 与总体裁定 Spearman = 1.000、标准差 0**，⛔ 而 Correctness 只 0.906；[68] 用控制质量的答案测出 GPT-4 给「含一处事实错误」**1415** Elo、给「事实正确但语法非母语」**771**。

**结论 13：LLM 代码评审意见，⚠️ 开发者归因的错误率聚在 15–33%。** ⚠️⛔ **先看分母**：文献里有五种不同构造都叫「acceptance」，⭐ **7%–74% 的跨度几乎全是分母造成的**。⭐ 最干净的误报设计是 **SWR-Bench（FSE 2026）**[71]：500 Change-PR + 500 Clean-PR，⭐ **Clean-PR 上任何意见按构造即误报**；最好成绩 **Precision 16.65% / Recall 23.18%**，⛔ 五种技术里四种精度 **&lt;10%**。作者结论：*"not yet ready for real-world code review deployment."*

**结论 14（⭐⭐ 最锋利的一对引用）：生产者不能做自己的检查者。** ⭐ 两个相隔十年的文献用不同方法给出同一结论：

- **Beyer et al.（FSE 2015）**[28]：3,964 个 SV-COMP 任务，两个工具互为生产者与验证者。⭐ **CPAchecker 对自己的误报只否掉 21%、对另一工具的否掉 93%；Ultimate Automizer 分别是 7% 与 97%。**
- **Huang et al.（ICLR 2024）**[12]：⭐ **有** oracle 标签时 GPT-3.5 在 CommonSenseQA 上 75.8 → **89.7**；⛔ **无** oracle 的内在自纠 75.8 → **38.1**；GPT-4 GSM8K 95.5 → **89.0**。逐字：*"after self-correction, the accuracies of all models drop across all benchmarks."*

⭐⭐ **这一对同时论证了「必须有外部机械验收步骤」与「该步骤不能由生成方自己实现」—— ⭐ 正是 C-① 真值封存与「可机械求值断言 + 独立求值器」这一形态的存在理由。**

配套 **Tyen et al.（Findings ACL 2024）**[72] 定位瓶颈在**找错**而非改错：整体找错准确率 GPT-4 **39.80–52.87**、Gemini Pro 16.14；⭐ 喂入 ground-truth 位置后改错全面提升；⛔ 且一个用域外数据训的**小分类器胜过 prompt 大模型**。

### 2.4 锚定 / traceability 的价值 —— ✅ 有实证，⚠️ 但要区分「制品锚定」与「发现锚定」

**结论 15：制品级 traceability 的收益有受控实验。** **Mäder &amp; Egyed（EMSE 2015）**[48]：**71 名被试**、真实维护任务、被试内设计。逐字：有 traceability 的被试 *"on average **24%** faster… and created on average **50%** more correct solutions."* ⚠️⛔ **广为流传的 461 任务 / 889s→678s / 50%→74% 全部原文未核到（付费墙），⛔ 不要引。** ⚠️ 会议前身 **ICSM 2012**[49] 是**另一项研究**（52 名被试，21% / 60%）—— ⛔ 检索摘要反复把两者混成一项。

**结论 16：把制品挂到需求上改善下游定位。** **Rath, Lo, Mäder（MSR 2018)**[50]：在 **&gt;13,000 个缺陷报告**上把检索性能按 MAP 提升 **49%**。

**结论 17：⭐ 真正把「锚定」与「准确性」分离的证据只有 §1 那条 Infer 自然实验 [17]。** ⭐ 其余全部指向同一命题的另一面：**可处置性（actionability）而非准确性是约束条件**。
- **Tricorder（ICSE 2015）**[16]：⭐ 比 10% 门限更重要的是定义 —— *"We define an **effective false positive** as any report from the tool where a **user chooses not to take action**."* ⭐ 准入标准第 1 条即形态要求：*"The warning should be easy to understand and the fix should be clear."*
- **Sadowski et al.（CACM 2018）**[18]：⭐ 同一问题出现在哪个环节改变它被认定为真的比例 —— 编译期 **74%** vs 已入库代码 **21%**。
- **Christakis &amp; Bird（ASE 2016）**[19]：375 份回应。⭐ 痛点排序：1 默认规则不对、**2 告警文案差**、3 误报太多、4 太慢、5 无修复建议 —— ⭐ **文案质量排在误报之前**。⚠️ ⛔ 图 1 的条形权重不可文本提取，⛔ **只引序数排名。**
- **Lewis et al.（ICSE 2013）**[20]：Google 全面部署缺陷预测，⛔ *"found **no identifiable change in developer behavior**."* ⭐ 第二条必要特征标题就是 **"Obvious reasoning"**：*"**The burden of proof is always on the tool to precisely elucidate why it has come to the conclusion it has.**"*
- **Barik et al.（ICSE 2017）**[73]：**56 人眼动实验**，⭐ 读错误消息的难度 *"comparable to the difficulty of reading source code"*，⭐ 且**显著预测任务表现**，占任务总时间 13%–25%。

### 2.5 断言/契约作为可复用制品 —— ⚠️ 框架性支持强，⛔ 因果性证据弱

⭐ **可以引的**：Orstra [38] 最对题 —— *"later when the class is changed, the augmented test suite is executed to check whether assertion violations are reported"*，11 个类上故障暴露率 **12% → 62%**；Daikon [74] 的定位。⚠️ **Meyer 1992**[51] ⛔ 纯立场论文、**无任何实证数字，⛔ 不要当证据引**；⚠️ **Leucker &amp; Schallhart**[52] 那句经典 RV 定义 ⛔ **原文未核到，⛔ 不要加引号引用**。

⛔ **不能引成因果的**：**Casalnuovo et al.（ICSE 2015）**[75] 摘要说「有断言的函数缺陷显著更少」，⛔ 但正文远为保守：*"The effect size is **small but highly significant in the hurdle model**, accounting… for about 10% of the deviance of the developers variable, and **1% of that of the total data**."* ⚠️ ⭐ **且他们自己报出反向因果通道**：*"**Asserts tend to be added to methods by developers with a higher ownership** of that method."* ⛔ **这是相关性研究，⛔ 不能引作「写断言导致缺陷更少」。**

---

## 3. ⛔ 找不到文献支撑的说法（⭐ 这一节决定哪些话只能写成「我们的设计选择」）

⚠️ 以下每条都经多路检索确认为**未找到**，⛔ 不是检索失败的猜测。⭐ 论文里凡涉及这些命题，**只能写成设计理由，⛔ 不能写成「已知更好」**。

1. ⛔ **没有任何人体实验比较「结构化/可机械求值的缺陷发现」与「散文式缺陷发现」的理解度或处置率。** ⚠️ Witnesses 2.0 [30] 的「readability」被操作化成**文件大小**，⛔ 没有人类被试；Tricorder / CACM 测的是**采取的行动**，⛔ 不是**达成的理解**；⭐ 而反例解释领域自己的 SLR [35] 把「缺乏用户研究」列为头号缺口。⭐ **这是本文能诚实主张的空白，⛔ 也是不能主张已有结论的地方。**
2. ⛔ **没有受控实验测出「带解释/理由的告警比不带的更常被处置」的效应量。** ⚠️ 存在的全是观察性与需求获取型证据。⚠️⛔ 一个流传的「56% 的 SAST 告警从未被处理」归给 Aloraini et al.（JSS 2019）—— ⛔ **该数字原文未核到，正是 snippet 传播模式，禁止使用。**
3. ⛔ **没有一句文献原话说「没有可执行判据就无法确认修复」。** ⭐ 该命题由 [62][61][65][60] **复合支持，⛔ 不能假托单一出处。**
4. ⚠️⛔ **没有把「一条发现是否锚在需求条目上」作为自变量的实验。** traceability 文献测的是**制品之间**的链接 [48][49][50]，⛔ 不是**缺陷发现**是否绑定需求。⭐ 唯一方法论等价的是 Infer [17]，⚠️ 而它的自变量是「挂在哪个变更上」，⛔ 不是「挂在哪条需求上」。⭐⭐ **跨越这一步是我方的类推，⛔ 必须显式标为类推。**
5. ⛔ **没有测量人手写断言在后续演化中真实捕获了一次回归的研究。** ⚠️ 存在的全是工具生成的回归 oracle（Orstra [38]、DSpot [77]）。⭐ 若这条对论文承重，⛔ 按**未找到**处理，⭐ 从构造上论证，⛔ 不要从测量上论证。
6. ⛔ 没有主会同行评审论文以 SARIF 结构化结果为核心贡献。SARIF 2.1.0 [78] 是 OASIS 规范而非研究。
7. ⛔ **没有可核实的、SE 或形式化方法场景下 LLM-judge 与人类的 Cohen κ。** ⚠️ 若干 preprint 报了 0.75 / 0.57 / 0.07，⛔ **四条检索均未能核到原文，禁止引用。** ⭐ [4] 报的是 Spearman/Agreement 而非 κ；[3] 的 κ = 0.28 是 NLP 任务而非 SE。
8. ⛔ **没有以可判定行为准则为验收、对未定时层次状态机做 LLM 修复的工作（2020–2026）。** ⭐ 两轮独立检索在该交叉点上**零命中**。⚠️ CTL/Kripke 传统有强判据但只在 ≤80 状态玩具模型上评测（[79] 最大 38 状态）；⚠️ MDE 传统有真实规模（[82]：24 个 UML 模型、31 条规则、**39,683 个不一致**）⛔ 但**从不测量生成的修复是否是开发者想要的那个**。⭐⭐ **这既是本文的机会，⛔ 也意味着没有直接先例可引。**
9. ⭐ **若需要「协议模板」，[83] Maoz, Ringert, Shalom（ICSE 2019）是最该模仿的一篇**：可判定准则 + 人写语料 + 系统性故障合成（136 个变体）+ 固定超时 + 10 次平均 + ⭐ **独立复核而非信任修复引擎**（*"by independently checking that the repaired specification is indeed satisfiable and realizable"*）。

---

## 4. ⛔ 反面材料：本形态的代价与局限（⭐ 必须写进论文，否则 reviewer 会替我们写）

### 4.1 ⭐ 写断言本身容易写错，⛔ 且错在「更弱」的方向 —— 因此**静默通过**

⭐ 这是最硬的一条反面证据。

- ⭐ **Little Tricky Logic（Programming 2023）**[84]：四轮、两年。**读**方向（LTL→英语）错误率 23%（学生）/ ⭐ **15%（29 名有 LTL 经验的研究者）**；⛔ **写**方向（英语→LTL）**47% / 28% / 47%**。逐字：*"the Eng ⊲ ltl direction was fraught with errors… Unfortunately, this task is perhaps the most important of the three."* ⭐ 主导误解是 `WeakU`（把 U 当弱 until）—— ⛔ **Round 4 有 9/11 中招，连研究者组也有两人。**
- **Greenman et al.（FM 2024）**[85]：五次部署、&gt;3,000 份回应，含 ⭐ **24 名有限迹时序逻辑研讨会参会者（「world-class researchers」）**。「写公式」错误率：⛔ **专家组 33.68%**、β1 66.13%。⚠️ ⛔ 作者明确警告 *"percentages are not comparable across columns"*，⛔ **不要连成趋势线。**
- **Czepa et al.（SoSyM 2019）**[86]：**215 名被试**随机分组。⛔ 自撰规约**平均语义正确率：LTL 28.49–30.85%**、PSP 46.93–50.19%。⭐ **响应时间无显著差异 —— LTL 的低准确率不是用速度换来的。**
- ⭐⭐ **失效方向是关键**：主导误解产出的公式比意图**更弱**，⛔ 于是**通过**。[87]（⚠️ preprint）在 93,283 份提交上测到欠约束公式占比从 RL/PL 的约 7% 升到 FOL 与 LTL 的约 **15%** —— ⛔ **通过却允许本应禁止的行为。**
- **Siu et al.（IROS 2023）**[88]：**62 名成人**（含形式化方法专家）做规约验证，⛔ **准确率 45% ± 20%，等于或低于随机**；⚠️ *"Participants exhibited an affirmation bias"*，⛔ 且 *"particularly those familiar with formal methods, tended to be **overconfident**."*

### 4.2 ⛔ 真空性：断言可以在无意义的前提下通过

**Beer et al.（FMSD 2001）**[22] 逐字：*"typically **20%** of formulas are found to be trivially valid, and that trivial validity **always** points to a real problem."* ⚠️⛔ **这是「several years of experience」的经验报告，无 N、无时间窗、无方法**；范围是硬件、新设计首轮。⛔ **只能引作「工业经验报告」，⛔ 绝不能引作实测率。**

### 4.3 ⛔ 人只写便宜的断言

**Contracts in Practice（FM 2014）**[90]：21 个**已在用契约**的项目、&gt;2.6 亿行 —— ⚠️ 注意这是**最好情况样本**。⛔ *"**The overwhelming majority of contracts involves Void/null checks**"*（C# 前置条件 80%–96%、Java **88%–100%** 含 null 检查），⛔ 量词 *"very rarely used: **practically never in pre- or postconditions**"*。⭐ 作者自己的解释：null 检查 *"simple to write, and hence cost-effective."*

### 4.4 ⛔ 写形式化标注是被点名的昂贵环节

**Woodcock et al.（CSUR 2009）**[92] 受访者原话：*"**The one expensive part of the code verification process was the annotation of the code with pre- and postconditions.**"* ⚠️ 且反面证据在这篇亲形式化方法的调查内部：⛔ *"in a **majority of projects surveyed, there is no data available on relative time and costs**"*。⚠️⛔ **版本陷阱**：流传的 2008-12 preprint 是 **54 个项目**且成本净负面；已发表 CSUR 版是 **62 个项目**。⛔ **引用必须点明版本。** ⭐ 工作量锚点：**seL4**[93] 的 8,700 行 C 对 200,000 行 Isabelle、约 20 人年，⭐ 且「第一次 refinement 有 **80%** 的工作量花在建立不变式上」；**CompCert**[94] 的 42,000 行 Coq 中 **76% 是正确性证明本体**。**Garavel et al.（FMICS 2020）**[95] 的 130 名专家调查：⛔ 只有 **15.4%** 认为立刻能盈利。

### 4.5 ⛔ 表达力与「规约本身对不对」的缺口，⭐ 工业界自己承认

**AWS TLA+**[96] 有一节标题就是 **"What Formal Specification Is Not Good For"**；⛔ 关于规约到代码的缺口逐字：*"engineers usually ask, 'How do we know that the executable code correctly implements the verified design?' **The answer is that we don't.**"* ⭐ 并记录了一次真实漏检。⚠️ ⛔ 数字来自 **2014-09 preprint**（CACM 返 403）。⭐ LLM 版最好引的一句是 **Lahiri（FMCAD 2024）**[97]：*"there is **no algorithmic way** of ensuring the correctness of the user-intent formalization for programs."* ⚠️ 且他审计 MBPP-DFY 中 64 份**人写** Dafny 规约，⛔ 发现 ≥3 份标为 STRONG SPEC 的其实更弱、另 3 份直接不对。

### 4.6 ⛔ 正确性与完备性存在明确取舍 —— ⚠️ 断言可以既对又没用

- ⭐ **nl2postcond（FSE 2024）**[98]：⚠️⛔ **先看分母** —— **77%** 是**逐条**、**96%** 是**逐题在 k=10**。⭐⭐ **关键取舍**：使正确率最大化的 prompt（77% accept@1）⛔ **把缺陷完备性压到 9.2%**；⭐ 缺陷完备性最好的一行是 35.1%。⭐ 他们自做的假阳性审计：900 条人工标注，**1.1%** 是「测试集判对但实际错」。⛔ Defects4J 上 33,600 条后条件只能区分 **47/525 (9%)** 缺陷。
- ⭐⭐ **AutoSVA2**[100] 的两句话应当**直接进本文的 limitation**：GPT-4 *"prone to create buggy SVA for correct RTL but also to create correct SVA for buggy RTL"*，以及 ⭐ *"**Having SVA with full RTL coverage does not imply that the assertions or the RTL are correct.**"*
- ⚠️ LLM 生成形式化性质的实测正确率**普遍很低**：nl2spec [101] 全自动 **44.4%**，⛔ 且 **36 条中至少 9 条（25%）自然语言本身有歧义、无唯一正确形式化**；FVEval [102] gpt-4o 语法 **0.911 vs 形式等价 0.456**，⛔ 且 **BLEU 与功能正确性相关仅 0.056–0.093** —— ⭐ **表面相似度度量根本不测性质正确性。**

### 4.7 ⛔⛔ 强制结构化输出本身有代价 —— ⭐ 任何「结构化更可靠」的主张都必须先过这篇

**Tam et al.（EMNLP 2024 Industry）**[105]：加 schema 约束不仅降低均值还**放大 prompt 间方差** —— ⛔ claude-3-haiku 的 GSM8K 由 86.99 掉到 **23.44**，标准差 0.2 → **22.9**。⭐ **不是解析问题**：LLaMA-3-8B 的 JSON 解析错误率 **0.148%** 而性能差距 **38.15%**。⭐ **机制已定位**：GPT-3.5-Turbo 的 JSON 模式 **100%** 把 `answer` 键放在 `reason` 键之前，⛔ 把 zero-shot CoT 悄悄变成直接作答。⚠️ ⭐ 作者结论是**任务相关**：严格格式伤害推理密集任务，⭐ 但**提升**分类任务。 ⚠️ ⛔ **注意任务归属**：`0.148% / 38.15%` 出自 **Last Letter Concatenation**，⛔ 与上句 `86.99 → 23.44` 所在的 **GSM8K** 不是同一任务 —— ⭐ 并列陈述时须标注（⛔ 不影响论证：该对数字用于否证「这是解析问题」这个假说）。

### 4.8 ⚠️ 一条对 APR 论证的正面反驳，⭐ 应当承认它存在

**Petke et al.（FSE 2024 IVR）**[106]：⭐ **每缺陷需筛查的 plausible 补丁中位数 = 2**。⭐ 所以「不正确/正确」的**比率**很糟，⛔ 但人需要过目的**绝对数**很小 —— ⭐ 他们据此认为过拟合「might not be as bad as previously thought」。

### 4.9 ⛔ 可判定验证器仍可被利用

**AlphaVerus（ICML 2025）**[107] 记录了 verifier exploitation：⛔ Verus 的 `assume(false)` 之类构造让平凡程序通过，⚠️ 且**在无 critique 阶段时模型会收敛到这个 hack 并雪球式扩散**。⭐ **Ahmed et al.**[108]（⚠️ preprint）测到 ⛔ **对可见 oracle 做迭代精化反而抬高了过拟合率**：Claude-3.7-Sonnet 21.8% → 25.5%；⛔ 220 对精化产出 22 个新通过补丁，⚠️ 其中 **14 个在隐藏测试上失败**。

---

## 5. ⛔ Snippet 与原文不符的九处（⛔ 务必不要引）

⚠️ 其中三处正是本仓库已登记过的那种失效模式（检索摘要造数字）。

| 流传的说法 | ⛔ 核验结论 |
| :-- | :-- |
| Ouyang 非确定性 72.73 / 60.40 / 65.85 | ⛔ 那是 arXiv v1；⭐ **已发表 TOSEM 是 75.76 / 51.00 / 47.56** |
| Chen/Zaharia/Zou「97.6% → 2.4%」 | ⛔ 来自被取代的 arXiv v1（测试集 500 素数、0 合数）；⭐ v3/HDSR 是 **84.0% → 51.1%** |
| Zheng「GPT-4 自增强 10% / Claude 25%」 | ⛔ **原文明确拒绝确立** |
| Zheng「80% 一致」 | ⛔ 是 S2 子集（去平局、随机基线 50%）；⭐ S1 口径下是 66% |
| Mäder &amp; Egyed 2015 的 461 任务 / 889s→678s / 50%→74% | ⛔ **原文未核到**（付费墙）；⚠️ 且 52 名被试 / 21% / 60% 是 **ICSM 2012 的另一项研究** |
| Aloraini「56% 的 SAST 告警从未处理」 | ⛔ **原文未核到**，纯 snippet 传播 |
| Autili TSE 2015「40 个新增 pattern」 | ⛔ **无法核实**；⚠️ 作者自建目录站只列 **15 个** |
| Utting/Pretschner/Legeard「七个维度」 | ⛔ **已发表 2012 STVR 说六个**；「七」只对 2006 working paper 成立 |
| AssertLLM「89% 语法与功能准确」 | ⛔ 四个版本三个不同头条数字；⚠️ **v2 = ASP-DAC'25 camera-ready 摘要里根本没有百分数** |

⛔ **其他 原文未核到 项（禁引）**：Rempel &amp; Mäder TSE 2017 的任何效应量；Nilizadeh et al. ICST 2021 的「547 buggy versions / 4.15%」；SemFix ICSE 2013 的全部实验数字；Leucker &amp; Schallhart 那句 RV 定义的逐字表述。⚠️ **三处作者/标题勘误**：LLM 补丁正确性评估的作者**不是** "Zhou, Bui, Le Goues" 而是 Xin Zhou … **Bach Le**, David Lo（TSE 2024）；DiffTGen 是 **ISSTA 2017** 不是 ICSE 2017；CTL 修复的 "Attie, Cherri, Bab, Sistla" ⛔ **这个作者列表不存在**。

---

## 6. ⭐⭐ 三条建议直接写进论文的论证骨架

### ① ⛔ 不要论证「断言比散文好」，⭐ 论证「散文不可复算」

⭐ 散文侧的实测证据**极强且全在可复算性上**：换序翻转 [1][2][4]、温度 0 不确定 [7][8]、改措辞改结论 [9][10][3]、快照消失 [11]。⚠️ 而唯一直接比较两种形态的 [47] 给出的是**可靠性提升约 5 倍、⛔ 效度提升有限**。

⭐⭐ **把主张限制在可复算性与可审计性上，它就是站得住的；⛔ 扩张到「判得更准」立刻失去支撑。**

### ② ⭐ 锚定的最强证据是 Infer 那条自然实验 [17]，⚠️ 而它证明的是「可处置性而非准确性是约束」

⭐ 配合 [16] 把 false positive 定义成「用户选择不处理」、[19] 把「文案差」排在「误报多」之前、[20] 的 *"burden of proof is always on the tool"*、[73] 的读消息难度显著预测任务表现 —— ⭐ 四条同向。

⚠️⛔ **但从「挂在哪个变更上」到「挂在哪条需求上」是我方类推，⛔ 必须标明。**

### ③ ⭐⭐「生产者不能做自己的检查者」是本文最有力的一对引用

⭐ [28] 的 **21%/7% vs 93%/97%** 与 [12] 的**有 oracle 75.8→89.7 / 无 oracle 75.8→38.1**。⭐ 两个相隔十年、不同领域、不同方法，指向同一结论。

⭐⭐ **它同时论证了「必须有外部机械验收步骤」与「该步骤不能由生成方自己实现」—— ⭐ 这正是 C-① 真值封存与「可机械求值断言 + 独立求值器」这一形态的存在理由。**

### ⭐ 补一条：[14] Baldur 直接支撑 C-③，⛔ 不只是 C-②

⭐ 抽掉 oracle 的**诊断输出**（保留 pass/fail 判决与采样预算不变）→ ⛔ **按推理成本归一后，增益不再超过纯生成基线**。⭐⭐ **这说明「只给真值不够，必须带证据链」—— 即 C-③ 的价值有独立文献支撑。**

---

## 7. 完整参考文献

⚠️ 编号沿用调研报告，⭐ 便于回溯；⛔ 编号 [5][77] 为重复项已并入 [47][39]。

[1] Peiyi Wang, et al. Large Language Models are not Fair Evaluators. **ACL 2024**, 9440–9450. DOI [10.18653/v1/2024.acl-long.511](https://doi.org/10.18653/v1/2024.acl-long.511) [2] Lianmin Zheng, et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. **NeurIPS 2023 D&amp;B**. arXiv:[2306.05685](https://arxiv.org/abs/2306.05685) [3] Anna Bavaresco, et al. LLMs instead of Human Judges? **ACL 2025 (Short)**, 238–255. DOI [10.18653/v1/2025.acl-short.20](https://doi.org/10.18653/v1/2025.acl-short.20) [4] Ruiqi Wang, et al. Can LLMs Replace Human Evaluators? An Empirical Study of LLM-as-a-Judge in Software Engineering. **PACMSE 2(ISSTA)**, art. ISSTA086, 2025. DOI [10.1145/3728963](https://doi.org/10.1145/3728963) [6] Rickard Stureborg, et al. Large Language Models are Inconsistent and Biased Evaluators. arXiv:[2405.01724](https://arxiv.org/abs/2405.01724)（⚠️ preprint）[7] Shuyin Ouyang, Jie M. Zhang, Mark Harman, Meng Wang. An Empirical Study of the Non-Determinism of ChatGPT in Code Generation. **ACM TOSEM 34(2)**, art. 42, 2025. DOI [10.1145/3697010](https://doi.org/10.1145/3697010) [8] Berk Atil, et al. Non-Determinism of "Deterministic" LLM Settings. arXiv:[2408.04667](https://arxiv.org/abs/2408.04667)（⚠️ preprint）[9] Melanie Sclar, et al. Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design. **ICLR 2024**. arXiv:[2310.11324](https://arxiv.org/abs/2310.11324) [10] Moran Mizrahi, et al. State of What Art? A Call for Multi-Prompt LLM Evaluation. **TACL 12**:933–949, 2024. DOI [10.1162/tacl_a_00681](https://doi.org/10.1162/tacl_a_00681) [11] Florian Angermeir, et al. Reflections on the Reproducibility of Commercial LLM Performance in Empirical Software Engineering Studies. **ICSE 2026**. DOI [10.1145/3744916.3773207](https://doi.org/10.1145/3744916.3773207) [12] Jie Huang, et al. Large Language Models Cannot Self-Correct Reasoning Yet. **ICLR 2024**. arXiv:[2310.01798](https://arxiv.org/abs/2310.01798) [13] Theo X. Olausson, et al. Is Self-Repair a Silver Bullet for Code Generation? **ICLR 2024**. arXiv:[2306.09896](https://arxiv.org/abs/2306.09896) [14] Emily First, Markus N. Rabe, Talia Ringer, Yuriy Brun. Baldur: Whole-Proof Generation and Repair with Large Language Models. **ESEC/FSE 2023**, 1229–1241. DOI [10.1145/3611643.3616243](https://doi.org/10.1145/3611643.3616243) [15] Nitya Thakkar, et al. A large-scale randomized study of large language model feedback in peer review. **Nature Machine Intelligence 8(3)**:326–336, 2026. DOI [10.1038/s42256-026-01188-x](https://doi.org/10.1038/s42256-026-01188-x) [16] Caitlin Sadowski, et al. Tricorder: Building a Program Analysis Ecosystem. **ICSE 2015**, 598–608. DOI [10.1109/ICSE.2015.76](https://doi.org/10.1109/ICSE.2015.76) [17] Dino Distefano, Manuel Fähndrich, Francesco Logozzo, Peter W. O'Hearn. Scaling static analyses at Facebook. **CACM 62(8)**:62–70, 2019. DOI [10.1145/3338112](https://doi.org/10.1145/3338112) [18] Caitlin Sadowski, et al. Lessons from building static analysis tools at Google. **CACM 61(4)**:58–66, 2018. DOI [10.1145/3188720](https://doi.org/10.1145/3188720) [19] Maria Christakis, Christian Bird. What developers want and need from program analysis. **ASE 2016**, 332–343. DOI [10.1145/2970276.2970347](https://doi.org/10.1145/2970276.2970347) [20] Chris Lewis, et al. Does bug prediction support human developers? **ICSE 2013**, 372–381. DOI [10.1109/ICSE.2013.6606583](https://doi.org/10.1109/ICSE.2013.6606583) [21] Brittany Johnson, et al. Why don't software developers use static analysis tools to find bugs? **ICSE 2013**, 672–681. DOI [10.1109/ICSE.2013.6606613](https://doi.org/10.1109/ICSE.2013.6606613) [22] Ilan Beer, Shoham Ben-David, Cindy Eisner, Yoav Rodeh. Efficient Detection of Vacuity in Temporal Model Checking. **FMSD 18(2)**:141–163, 2001. DOI [10.1023/A:1008779610539](https://doi.org/10.1023/A:1008779610539) [23] Hana Chockler, Orna Kupferman, Moshe Y. Vardi. Coverage Metrics for Temporal Logic Model Checking. **TACAS 2001**, 528–542. DOI [10.1007/3-540-45319-9_36](https://doi.org/10.1007/3-540-45319-9_36) [24] Kristin Y. Rozier, Moshe Y. Vardi. LTL Satisfiability Checking. **SPIN 2007**, 149–167. DOI [10.1007/978-3-540-73370-6_11](https://doi.org/10.1007/978-3-540-73370-6_11) [25] Dimitra Giannakopoulou, et al. Formal Requirements Elicitation with FRET. **REFSQ 2020 Workshops**. NASA NTRS [20200001989](https://ntrs.nasa.gov/citations/20200001989) [26] Orna Kupferman, Moshe Y. Vardi. Vacuity Detection in Temporal Model Checking. **STTT 4(2)**:224–233, 2003. DOI [10.1007/s100090100062](https://doi.org/10.1007/s100090100062)（⛔ 全文未取到）[27] Roy Armoni, et al. Enhanced Vacuity Detection in Linear Temporal Logic. **CAV 2003**, 368–380. DOI [10.1007/978-3-540-45069-6_35](https://doi.org/10.1007/978-3-540-45069-6_35) [28] Dirk Beyer, Matthias Dangl, Daniel Dietsch, Matthias Heizmann, Andreas Stahlbauer. Witness Validation and Stepwise Testification across Software Verifiers. **ESEC/FSE 2015**, 721–733. DOI [10.1145/2786805.2786867](https://doi.org/10.1145/2786805.2786867) [29] Dirk Beyer, et al. Verification Witnesses. **ACM TOSEM 31(4)**, art. 57, 2022. DOI [10.1145/3477579](https://doi.org/10.1145/3477579) [30] Paulína Ayaziová, et al. Software Verification Witnesses 2.0. **SPIN 2024**, 184–203. DOI [10.1007/978-3-031-66149-5_11](https://doi.org/10.1007/978-3-031-66149-5_11) [31] Alex Groce, Willem Visser. What Went Wrong: Explaining Counterexamples. **SPIN 2003**, 121–135. DOI [10.1007/3-540-44829-2_8](https://doi.org/10.1007/3-540-44829-2_8) [32] Alex Groce, et al. Error Explanation with Distance Metrics. **STTT 8(3)**:229–247, 2006. DOI [10.1007/s10009-005-0202-0](https://doi.org/10.1007/s10009-005-0202-0) [33] Edmund Clarke, et al. Counterexample-Guided Abstraction Refinement. **CAV 2000**, 154–169. DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15) [34] Thomas Ball, Mayur Naik, Sriram K. Rajamani. From Symptom to Cause: Localizing Errors in Counterexample Traces. **POPL 2003**, 97–105. DOI [10.1145/604131.604140](https://doi.org/10.1145/604131.604140) [35] Arut Prakash Kaleeswaran, et al. A Systematic Literature Review on Counterexample Explanation. **IST 145**:106800, 2022. DOI [10.1016/j.infsof.2021.106800](https://doi.org/10.1016/j.infsof.2021.106800) [36] Jan Tretmans. Model Based Testing with Labelled Transition Systems. **LNCS 4949**:1–38, 2008. DOI [10.1007/978-3-540-78917-8_1](https://doi.org/10.1007/978-3-540-78917-8_1) [37] Robert M. Hierons, et al. Using Formal Specifications to Support Testing. **ACM CSUR 41(2)**, art. 9, 2009. DOI [10.1145/1459352.1459354](https://doi.org/10.1145/1459352.1459354) [38] Tao Xie. Augmenting Automatically Generated Unit-Test Suites with Regression Oracle Checking. **ECOOP 2006**, 380–403. DOI [10.1007/11785477_23](https://doi.org/10.1007/11785477_23) [39] Benoit Danglot, et al. Automatic test improvement with DSpot. **EMSE 24(4)**:2603–2635, 2019. DOI [10.1007/s10664-019-09692-y](https://doi.org/10.1007/s10664-019-09692-y) [40] Benoit Danglot, et al. A snowballing literature study on test amplification. **JSS 157**:110398, 2019. DOI [10.1016/j.jss.2019.110398](https://doi.org/10.1016/j.jss.2019.110398) [41] Zichao Qi, Fan Long, Sara Achour, Martin Rinard. An analysis of patch plausibility and correctness for generate-and-validate patch generation systems. **ISSTA 2015**, 24–36. DOI [10.1145/2771783.2771791](https://doi.org/10.1145/2771783.2771791) [42] Edward K. Smith, Earl T. Barr, Claire Le Goues, Yuriy Brun. Is the cure worse than the disease? Overfitting in automated program repair. **ESEC/FSE 2015**, 532–543. DOI [10.1145/2786805.2786825](https://doi.org/10.1145/2786805.2786825) [43] Fan Long, Martin Rinard. An analysis of the search spaces for generate and validate patch generation systems. **ICSE 2016**, 702–713. DOI [10.1145/2884781.2884872](https://doi.org/10.1145/2884781.2884872) [44] Xuan-Bach D. Le, Ferdian Thung, David Lo, Claire Le Goues. Overfitting in semantics-based automated program repair. **EMSE 23(5)**:3007–3033, 2018. DOI [10.1007/s10664-017-9577-2](https://doi.org/10.1007/s10664-017-9577-2) [45] Zhongxing Yu, Matias Martinez, Benjamin Danglot, Thomas Durieux, Martin Monperrus. Alleviating patch overfitting with automatic test generation. **EMSE 24**:33–67, 2019. DOI [10.1007/s10664-018-9619-4](https://doi.org/10.1007/s10664-018-9619-4) [46] Benedikt Stroebl, Sayash Kapoor, Arvind Narayanan. Inference Scaling fLaws. arXiv:[2411.17501](https://arxiv.org/abs/2411.17501)（⚠️ preprint）[47] Yukyung Lee, et al. CheckEval: A reliable LLM-as-a-Judge framework for evaluating text generation using checklists. **EMNLP 2025 (Main)**, 15771–15798. DOI [10.18653/v1/2025.emnlp-main.796](https://doi.org/10.18653/v1/2025.emnlp-main.796) [48] Patrick Mäder, Alexander Egyed. Do developers benefit from requirements traceability when evolving and maintaining a software system? **EMSE 20(2)**:413–441, 2015. DOI [10.1007/s10664-014-9314-z](https://doi.org/10.1007/s10664-014-9314-z) [49] Patrick Mäder, Alexander Egyed. Assessing the effect of requirements traceability for software maintenance. **ICSM 2012**, 171–180. DOI [10.1109/ICSM.2012.6405269](https://doi.org/10.1109/ICSM.2012.6405269) [50] Michael Rath, David Lo, Patrick Mäder. Analyzing requirements and traceability information to improve bug localization. **MSR 2018**, 442–453. DOI [10.1145/3196398.3196415](https://doi.org/10.1145/3196398.3196415) [51] Bertrand Meyer. Applying "Design by Contract". **Computer 25(10)**:40–51, 1992. DOI [10.1109/2.161279](https://doi.org/10.1109/2.161279)（⛔ 无实证）[52] Martin Leucker, Christian Schallhart. A brief account of runtime verification. **JLAP 78(5)**:293–303, 2009. DOI [10.1016/j.jlap.2008.08.004](https://doi.org/10.1016/j.jlap.2008.08.004)（⛔ 定义未逐字核到）[53] Ezio Bartocci, Yliès Falcone, Adrian Francalanza, Giles Reger. Introduction to Runtime Verification. **LNCS 10457**:1–33, 2018. DOI [10.1007/978-3-319-75632-5_1](https://doi.org/10.1007/978-3-319-75632-5_1) [54] Sergey Mechtaev, Manh-Dung Nguyen, Yannic Noller, Lars Grunske, Abhik Roychoudhury. Semantic Program Repair Using a Reference Implementation. **ICSE 2018**, 129–139. DOI [10.1145/3180155.3180247](https://doi.org/10.1145/3180155.3180247) [55] Xiang Gao, et al. Beyond Tests: Program Vulnerability Repair via Crash Constraint Extraction. **ACM TOSEM 30(2)**, art. 14, 2021. DOI [10.1145/3418461](https://doi.org/10.1145/3418461) [56] Yu Pei, Carlo A. Furia, Martin Nordio, Yi Wei, Bertrand Meyer, Andreas Zeller. Automated Fixing of Programs with Contracts. **IEEE TSE 40(5)**:427–449, 2014. DOI [10.1109/TSE.2014.2312918](https://doi.org/10.1109/TSE.2014.2312918) [57] Nadia Polikarpova, et al. What good are strong specifications? **ICSE 2013**, 262–271. DOI [10.1109/ICSE.2013.6606572](https://doi.org/10.1109/ICSE.2013.6606572) [58] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, Shin Yoo. The Oracle Problem in Software Testing: A Survey. **IEEE TSE 41(5)**:507–525, 2015. DOI [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785) [59] Xinyun Chen, Maxwell Lin, Nathanael Schärli, Denny Zhou. Teaching Large Language Models to Self-Debug. **ICLR 2024**. arXiv:[2304.05128](https://arxiv.org/abs/2304.05128) [60] He Ye, Matias Martinez, Martin Monperrus. Automated Patch Assessment for Program Repair at Scale. **EMSE 26**, 2021. DOI [10.1007/s10664-020-09920-w](https://doi.org/10.1007/s10664-020-09920-w) [61] Marcel Böhme, Ezekiel O. Soremekun, Sudipta Chattopadhyay, Emamurho Ugherughe, Andreas Zeller. Where Is the Bug and How Is It Fixed? **ESEC/FSE 2017**, 117–128. DOI [10.1145/3106237.3106255](https://doi.org/10.1145/3106237.3106255) [62] Yingfei Xiong, Xinyuan Liu, Muhan Zeng, Lu Zhang, Gang Huang. Identifying Patch Correctness in Test-Based Program Repair. **ICSE 2018**, 789–799. DOI [10.1145/3180155.3180182](https://doi.org/10.1145/3180155.3180182) [63] Haoye Tian, et al. Evaluating Representation Learning of Code Changes for Predicting Patch Correctness in Program Repair. **ASE 2020**, 981–992. DOI [10.1145/3324884.3416532](https://doi.org/10.1145/3324884.3416532) [64] Sina Shamshiri, et al. Do Automatically Generated Unit Tests Find Real Faults? **ASE 2015**, 201–211. DOI [10.1109/ASE.2015.86](https://doi.org/10.1109/ASE.2015.86) [65] Xuan-Bach D. Le, Lingfeng Bao, David Lo, Xin Xia, Shanping Li, Corina Păsăreanu. On Reliability of Patch Correctness Assessment. **ICSE 2019**, 524–535. DOI [10.1109/ICSE.2019.00064](https://doi.org/10.1109/ICSE.2019.00064) [66] Miles Turpin, Julian Michael, Ethan Perez, Samuel R. Bowman. Language Models Don't Always Say What They Think. **NeurIPS 2023**, 36:74952–74965. arXiv:[2305.04388](https://arxiv.org/abs/2305.04388) [67] Benjamin Feuer, et al. Style Outweighs Substance: Failure Modes of LLM Judges in Alignment Benchmarking. **ICLR 2025**. arXiv:[2409.15268](https://arxiv.org/abs/2409.15268) [68] Minghao Wu, Alham Fikri Aji. Style Over Substance: Evaluation Biases for Large Language Models. **COLING 2025**, 297–312. [ACL](https://aclanthology.org/2025.coling-main.21/) [69] Doriane Olewicki, et al. Impact of LLM-based Review Comment Generation in Practice. arXiv:[2411.07091](https://arxiv.org/abs/2411.07091)（⚠️ preprint）[70] Hong Yi Lin, et al. arXiv:[2607.03316](https://arxiv.org/abs/2607.03316)（⚠️ preprint；⛔ 仅约 297 条人工标注，其余由 GPT-5.1 标注）[71] Zhengran Zeng, et al. SWR-Bench: Assessing LLM Performance in Real-World Code Review Comment Generation. **PACMSE 3(FSE)**, art. FSE137, 2026. DOI [10.1145/3808144](https://doi.org/10.1145/3808144) [72] Gladys Tyen, et al. LLMs cannot find reasoning errors, but can correct them given the error location. **Findings of ACL 2024**, 13894–13908. DOI [10.18653/v1/2024.findings-acl.826](https://doi.org/10.18653/v1/2024.findings-acl.826) [73] Titus Barik, et al. Do Developers Read Compiler Error Messages? **ICSE 2017**, 575–585. DOI [10.1109/ICSE.2017.59](https://doi.org/10.1109/ICSE.2017.59) [74] Michael D. Ernst, et al. Dynamically discovering likely program invariants to support program evolution. **ICSE 1999**, 213–224. DOI [10.1145/302405.302467](https://doi.org/10.1145/302405.302467) [75] Casey Casalnuovo, et al. Assert Use in GitHub Projects. **ICSE 2015**, 755–766. DOI [10.1109/ICSE.2015.88](https://doi.org/10.1109/ICSE.2015.88)（⛔ 相关性，不可引作因果）[76] Pavneet Singh Kochhar, David Lo. Revisiting Assert Use in GitHub Projects. **EASE 2017**, 298–307. DOI [10.1145/3084226.3084259](https://doi.org/10.1145/3084226.3084259) [78] SARIF Version 2.1.0. **OASIS Standard**, 2020-03-27（含 Errata 01, 2023-08-28）。[OASIS](https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html) [79] George Chatzieleftheriou, et al. Abstract Model Repair. **LMCS 11(3:11)**, 2015. DOI [10.2168/LMCS-11(3:11)2015](https://doi.org/10.2168/LMCS-11(3:11)2015) [80] Paul Attie, Jad Saklawi. **ACM TECS 17(2)**, art. 32, 2018. DOI [10.1145/3147426](https://doi.org/10.1145/3147426) [81] Yan Zhang, Yulin Ding. CTL Model Update for System Modifications. **JAIR 31**:113–155, 2008. DOI [10.1613/jair.2420](https://doi.org/10.1613/jair.2420) [82] Luciano Marchezan, Roland Kretschmer, Wesley K. G. Assunção, Alexander Reder, Alexander Egyed. Generating repairs for inconsistent models. **SoSyM 22(1)**:297–329, 2023. DOI [10.1007/s10270-022-00996-0](https://doi.org/10.1007/s10270-022-00996-0) [83] Shahar Maoz, Jan Oliver Ringert, Rafi Shalom. Symbolic Repairs for GR(1) Specifications. **ICSE 2019**, 1016–1026. DOI [10.1109/ICSE.2019.00106](https://doi.org/10.1109/ICSE.2019.00106) [84] Ben Greenman, Sam Saarinen, Tim Nelson, Shriram Krishnamurthi. Little Tricky Logic: Misconceptions in the Understanding of LTL. **Programming 7(2)**, art. 7, 2023. DOI [10.22152/programming-journal.org/2023/7/7](https://doi.org/10.22152/programming-journal.org/2023/7/7) [85] Ben Greenman, et al. Misconceptions in Finite-Trace and Infinite-Trace Linear Temporal Logic. **FM 2024**, 579–599. DOI [10.1007/978-3-031-71162-6_30](https://doi.org/10.1007/978-3-031-71162-6_30) [86] Christoph Czepa, Amirali Amiri, Evangelos Ntentos, Uwe Zdun. Modeling compliance specifications in LTL, EPL and PSP. **SoSyM 18(6)**:3331–3371, 2019. DOI [10.1007/s10270-019-00721-4](https://doi.org/10.1007/s10270-019-00721-4) [87] Ana Jovanovic, Allison Sullivan. Right or Wrong — Understanding How Novice Users Write Software Models. arXiv:[2402.06624](https://arxiv.org/abs/2402.06624)（⚠️ preprint；⛔ PDF 内 DOI 为占位符）[88] Ho Chit Siu, Kevin Leahy, Makai Mann. STL: Surprisingly Tricky Logic (for System Validation). **IROS 2023**, 8613–8620. DOI [10.1109/IROS55552.2023.10342290](https://doi.org/10.1109/IROS55552.2023.10342290) [89] Isabelle Hurley, et al. STL: Still Tricky Logic. **NeurIPS 2024**. arXiv:[2407.02632](https://arxiv.org/abs/2407.02632) [90] H.-Christian Estler, Carlo A. Furia, Martin Nordio, Marco Piccioni, Bertrand Meyer. Contracts in Practice. **FM 2014**, LNCS 8442:230–246. DOI [10.1007/978-3-319-06410-9_17](https://doi.org/10.1007/978-3-319-06410-9_17) [91] Yi Wei, Carlo A. Furia, Nikolay Kazmin, Bertrand Meyer. Inferring better contracts. **ICSE 2011**, 191–200. DOI [10.1145/1985793.1985820](https://doi.org/10.1145/1985793.1985820) [92] Jim Woodcock, Peter Gorm Larsen, Juan Bicarregui, John Fitzgerald. Formal Methods: Practice and Experience. **ACM CSUR 41(4)**, art. 19, 2009. DOI [10.1145/1592434.1592436](https://doi.org/10.1145/1592434.1592436)（⚠️ 注意版本）[93] Gerwin Klein, et al. seL4: Formal Verification of an OS Kernel. **SOSP 2009**, 207–220. DOI [10.1145/1629575.1629596](https://doi.org/10.1145/1629575.1629596) [94] Xavier Leroy. Formal Verification of a Realistic Compiler. **CACM 52(7)**:107–115, 2009. DOI [10.1145/1538788.1538814](https://doi.org/10.1145/1538788.1538814) [95] Hubert Garavel, Maurice H. ter Beek, Jaco van de Pol. The 2020 Expert Survey on Formal Methods. **FMICS 2020**, LNCS 12327:3–69. DOI [10.1007/978-3-030-58298-2_1](https://doi.org/10.1007/978-3-030-58298-2_1) [96] Chris Newcombe, et al. How Amazon Web Services Uses Formal Methods. **CACM 58(4)**:66–73, 2015. DOI [10.1145/2699417](https://doi.org/10.1145/2699417)（⚠️ 数字核自 2014-09 preprint）[97] Shuvendu K. Lahiri. Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages. **FMCAD 2024**. arXiv:[2406.09757](https://arxiv.org/abs/2406.09757) [98] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, Shuvendu K. Lahiri. Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions? **PACMSE 1(FSE)**, art. 84, 2024. DOI [10.1145/3660791](https://doi.org/10.1145/3660791) [99] Wenji Fang, et al. AssertLLM2. arXiv:[2605.27472](https://arxiv.org/abs/2605.27472)（⚠️ preprint；⛔ 引表不引正文）[100] Marcelo Orenes-Vera, Margaret Martonosi, David Wentzlaff. Using LLMs to Facilitate Formal Verification of RTL. arXiv:[2309.09437](https://arxiv.org/abs/2309.09437)（⚠️ preprint）[101] Matthias Cosler, et al. nl2spec. **CAV 2023**, LNCS 13965:383–396. DOI [10.1007/978-3-031-37703-7_18](https://doi.org/10.1007/978-3-031-37703-7_18) [102] Minwoo Kang, et al. FVEval. arXiv:[2410.23299](https://arxiv.org/abs/2410.23299)（⚠️ preprint）[103] Vaishnavi Pulavarthi, Deeksha Nandal, Soham Dan, Debjit Pal. AssertionBench. **Findings of NAACL 2025**. arXiv:[2406.18627](https://arxiv.org/abs/2406.18627) [104] Rahul Kande, et al. (Security) Assertions by Large Language Models. **IEEE TIFS**, 2024. DOI [10.1109/TIFS.2024.3372809](https://doi.org/10.1109/TIFS.2024.3372809) [105] Zhi Rui Tam, et al. Let Me Speak Freely? **EMNLP 2024 Industry Track**, 1218–1236. DOI [10.18653/v1/2024.emnlp-industry.91](https://doi.org/10.18653/v1/2024.emnlp-industry.91) [106] Justyna Petke, Matias Martinez, Maria Kechagia, Aldeida Aleti, Federica Sarro. The Patch Overfitting Problem in Automated Program Repair. **FSE Companion 2024 (IVR)**, 452–456. DOI [10.1145/3663529.3663776](https://doi.org/10.1145/3663529.3663776) [107] Pranjal Aggarwal, Bryan Parno, Sean Welleck. AlphaVerus. **ICML 2025**, PMLR v267. arXiv:[2412.06176](https://arxiv.org/abs/2412.06176) [108] Toufique Ahmed, et al. Investigating Test Overfitting on SWE-bench. arXiv:[2511.16858](https://arxiv.org/abs/2511.16858) v3（⚠️ preprint）[109] Sergey Mechtaev, Jooyong Yi, Abhik Roychoudhury. Angelix. **ICSE 2016**, 691–701. DOI [10.1145/2884781.2884807](https://doi.org/10.1145/2884781.2884807) [110] Matthew B. Dwyer, George S. Avrunin, James C. Corbett. Patterns in Property Specifications for Finite-State Verification. **ICSE 1999**, 411–420. DOI [10.1145/302405.302672](https://doi.org/10.1145/302405.302672)（555 条规约中 **511 (92%)** 匹配 pattern；⚠️ 约 10 条明显有误）[111] Frits Vaandrager, Ivo Melse. New Fault Domains for Conformance Testing of Finite State Machines. **CONCUR 2025**. arXiv:[2410.19405](https://arxiv.org/abs/2410.19405) [112] Laura Inozemtseva, Reid Holmes. Coverage is not strongly correlated with test suite effectiveness. **ICSE 2014**, 435–445. DOI [10.1145/2568225.2568271](https://doi.org/10.1145/2568225.2568271) [113] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, Lingming Zhang. Is Your Code Generated by ChatGPT Really Correct? **NeurIPS 2023**. arXiv:[2305.01210](https://arxiv.org/abs/2305.01210)（测试扩 80×，pass@k 降 19.3–28.9%，⭐ 且模型排名反转）[114] Xin Zhou, et al., Bach Le, David Lo. Leveraging Large Language Model for Automatic Patch Correctness Assessment. **IEEE TSE 50(11)**:2865–2883, 2024. DOI [10.1109/TSE.2024.3452252](https://doi.org/10.1109/TSE.2024.3452252) [115] T. S. Chow. Testing Software Design Modeled by Finite-State Machines. **IEEE TSE SE-4(3)**:178–187, 1978. DOI [10.1109/TSE.1978.231496](https://doi.org/10.1109/TSE.1978.231496)（⛔ 全文未取到）[116] David Lee, Mihalis Yannakakis. Principles and Methods of Testing Finite State Machines — A Survey. **Proc. IEEE 84(8)**:1090–1123, 1996. DOI [10.1109/5.533956](https://doi.org/10.1109/5.533956)（⛔ 全文未取到）

---

## 8. 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-12 | 建立。调研 agent 产出，116 条引用。⭐ 调研方自述独立复核了两处最承重数字（CheckEval 的 ACL PDF Table 2、Infer 的 CACM 全文段落）。⛔ 本仓库尚未逐条人工复验，引用进论文前须逐条取原文。⭐ §5 记录 9 处 snippet 与原文不符 + 3 处作者/标题勘误。 |
