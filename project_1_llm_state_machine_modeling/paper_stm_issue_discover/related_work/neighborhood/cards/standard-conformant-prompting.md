# 卡片 · Adnyana & Schwung, CoDIT 2026 —— SCP：⭐ 把 IEC 61131-3 符合性「提前到生成期」，⛔ 而实现方式只是 prompt

## ⛔⛔ 开卡四条警告（⭐ 全部先读）

### ⛔ 警告 1 · **全文不可得** —— ⭐ 本卡是「仅据摘要 ＋ 图注 ＋ 参考文献」

⭐ **实际取到的一手材料**（⛔ 全部逐字）：

| 材料 | 来源 | 体量 |
| :-- | :-- | :-- |
| ⭐ **完整摘要** | ⭐⭐ **双源核对一致**：IEEE `rest/document/11630913/abstract` ＋ Semantic Scholar Graph API | ⭐ 1,247 字符（⭐ 完整，⛔ 非截断） |
| ⭐⭐ **全部 7 条图注** | ⭐ IEEE `rest/document/11630913/figures` | ⭐ Fig. 1–7 逐字 |
| ⭐ **全部 15 条参考文献** | ⭐ IEEE `rest/document/11630913/references` | ⭐ 逐字 |
| ⭐ 关键词（三组）· 作者单位 · 页码 · ISBN/ISSN · 插入日期 | ⭐ IEEE `abstract` endpoint | ⭐ 完整 |

⛔ **正文、Tables I–III、图内数值全部不可得。** ⭐ 已试入口（⛔ 逐条记失败原因）：

1. ⛔ IEEE `stamp.jsp` / `iel8` PDF → ⭐ `accessType: {"type": "locked"}`，⭐ `isOpenAccess: false` · `isFreeDocument: false` · `openAccessFlag: "F"`
2. ⛔ Crossref `link` 里的 `xplorestaging.ieee.org/ielx8/…/11630913.pdf` → ⛔ 返回 `200 / 50,338 B / text/html` ＋ Akamai `<APM_DO_NOT_TOUCH>`（⭐ 反爬壳，⛔ 非 PDF）
3. ⛔ Unpaywall / OpenAlex → ⭐ 逐字 `{"is_oa": false, "oa_status": "closed", "any_repository_has_fulltext": false}`
4. ⛔ Semantic Scholar `openAccessPdf` → ⭐ 逐字 `{"url": "", "status": "CLOSED"}`
5. ⛔ arXiv → ⭐ 已试 `all:"Standard Conformant Prompting"` 与 `au:Adnyana AND au:Schwung`，⛔ **零命中**
6. ⛔ SSRN 预印本 → ⭐ 已通过 Crossref 列出该作者组全部 9 条题录（⭐ 见 [F.5](#f-存疑与未核项)），⛔ **SCP 本身无 SSRN 版**；⛔ 同组其它 SSRN 页（`ssrn.6247781` / `ssrn.5600799`）返回 `403` Cloudflare
7. ⛔ ResearchGate → `403`；⛔ `ouci.dntb.gov.ua` → `502`
8. ⛔ 同组开放获取姊妹篇（⭐ 参考文献 [4]，`10.1016/j.mlwa.2025.100804`，**CC-BY gold OA**）→ ⛔ ScienceDirect `403` Cloudflare，⛔ `linkinghub` 只回 `Redirecting`，⛔ `r.jina.ai` 代理也 `403`

⚠️ **因此本卡每一节都标了「仅据摘要 / 仅据图注 / 仅据参考文献」，⛔ 且 [B](#b-llm-应用形态) 节多格只能写「原文未提供」。**

### ⛔⛔ 警告 2 · **它不过 L3 的硬门 2**（⭐ 制品是代码，不是模型）

⭐ [README.md](../README.md) §2 硬门 2 逐字："制品必须是**模型** —— **纯代码**、纯文本需求、纯测试用例**不算**"，⭐ 理由逐字："代码上的 LLM 工作汗牛充栋但形态不可迁移：**代码有编译器和测试当 oracle，行为模型没有**"。

⛔ **SCP 的制品是 IEC 61131-3 Structured Text PLC 代码**（⭐ 面向 Siemens TIA Portal），⛔ **没有任何状态机 / SFC / 行为模型制品**（⭐ 摘要与 7 条图注里零提及）。⭐ 关键词组也印证：⭐ Author Keywords 逐字 `Programmable logic controllers · large language models · industrial automation · prompt engineering`；⭐ Index Terms 逐字 `Code Generation · Large Language Models · Readability · Modularity · Structural Constraints · Evaluation Items · Control Logic · Sequence Of Tokens · Semantic Scores`。

⭐⭐ **所以本卡的定位是「⭐ 方法层参照」，⛔ 不是 L3 的正式条目**：⛔ **不得进 [pipeline_forms.md](../pipeline_forms.md) 的形态对照表**（⛔ 那张表的分母是过了两道硬门的工作），⛔ 也不得计入 L3 的命中统计。⭐ 它进这里的唯一理由是任务书指定的那个问题：⭐ 它对本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §11 的准入边界有什么话要说。

### ⛔⛔ 警告 3 · **参考文献里查实一条伪造引用，⭐ 而它正是"批评 post-hoc 自检"的承重依据**

⭐ 参考文献 [7] 逐字：

> "Z. Liu, Y. Chen, and P. Liu, "**Revisiting Iterative Self-Verification in Large Language Models**," arXiv preprint **arXiv:2501.01234**, 2025."

⭐⭐ **我实际访问了那个 arXiv id。⛔ 它是另一篇完全不相干的论文：**

> ⭐ `https://export.arxiv.org/api/query?id_list=2501.01234` → `<id>http://arxiv.org/abs/2501.01234v1</id>` · `<title>` ⛔ **"Impact of QCD sum rules coupling constants on neutron stars structure"** `</title>`

⭐ **另外两条有 literal 占位符 DOI**（⭐ 逐字，⛔ 不是我的省略）：

- ⭐ [6] "A. Khojah and S. Alsubaie, 'Impact of Large Language Model Code Generation on Industrial Control Software Quality,' *IEEE Access*, vol. 12, pp. 45678 - 45691, 2024, doi: **10.1109/ACCESS.2024.XXXXXXX**."
- ⭐ [8] "Y. Chen, Z. Wang, and S. Li, 'CodeT: Constraint-Aware Code Generation with Large Language Models,' *IEEE Transactions on Neural Networks and Learning Systems*, 2024, doi: **10.1109/TNNLS.2024.XXXXXXX**."

⭐ 这两条在 Crossref 上按题名 ＋ venue 检索**均无匹配**（⭐ 已实跑，⛔ 返回的全是不相干条目）。⭐ [10] "StructPrompt: Structured Prompting for Deterministic Code Generation, SANER 2024" 同样无 DOI 且 Crossref 无匹配。

⭐ **对照组（⭐ 我核过的真条目）**：⭐ [9] `arXiv:2305.13971` = **Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning** ✅ 真 · ⭐ [5] `arXiv:2401.05443` = **LLM4PLC**（⭐ 实际题名 "LLM4PLC: Harnessing Large Language Models for Verifiable Programming of PLCs in Industrial Control Systems"，⭐ 论文引的是一个改写版题名）✅ 真 · ⭐ [3] CoVe = aclanthology `2024.findings-acl.212` ✅ 真 · ⭐ [1] CodeGen `arXiv:2203.13474` ✅ 真。

⭐⭐⭐ **为什么这条警告必须放在开头**：⭐ [7] 是这篇论文**批评迭代式自我验证的唯一文献依据**，⛔ 而它是假的。⭐ 按本仓库 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 纪律 3（⭐ "引用必须真实存在……**裁定层不核验引用真实性**"），⭐⭐ **这直接降低本篇全部主张的证据等级** —— ⭐ 尤其是 [必答②](#-必答--它批评-post-hoc-自检的理由与证据是什么)。

### ⚠️ 警告 4 · 标题在任务书里不全

⭐ 任务书写的是 **"Standard Conformant Prompting"**（⚠️ 已注"标题可能不全"，⭐ 判断正确）。⭐ **完整正式题名**（M，⭐ IEEE ＋ Crossref ＋ Semantic Scholar 三源逐字一致，⭐ 含那个不规范的空格 ＋ 冒号）：

> **Standard Conformant Prompting (SCP): A Reproducible Framework for Compiler-Ready PLC Code Generation with Large Language Models : From Post-Hoc Verification to Standard-Driven Code Synthesis in Industrial Automation**

---

## ⭐⭐ 必答① · 「生成期强制符合性」具体怎么实现（⭐ 约束解码 / 模板 / schema / 多轮）

⭐⭐⭐ **答案：⛔ 四个选项全不是。⭐ 它是一个**固定 prompt 模板** —— ⛔ 纯文本层，⛔ 没有任何装置在生成过程中拦截。**

⭐ 摘要逐字（M）：

> "This paper introduces Standard Conformant Prompting (SCP), a **compliance-driven prompting architecture** that **embeds IEC 61131-3 rules, vendor syntax profiles, declaration discipline, and safety-oriented structural templates directly into the prompt** to constrain first-pass synthesis toward TIA Portal-targeted PLC code."

⭐ Fig. 2 图注逐字（M）：

> "**Fixed SCP prompt** for a complex multi-axis robotic coordination and safety-zone control task. **The template embeds IEC 61131-3 and vendor-specific constraints directly into the generative process** to ensure compiler-ready PLC code."

⭐⭐ Fig. 3 图注逐字（M）—— ⛔ **这一条是决定性的**：

> "Standardized pipeline for evaluating prompting strategies. **Only the prompt layer is replaced; all other components remain constant** to ensure reproducibility."

### ⭐ 逐条排除四个选项

| 候选实现 | 有无 | 依据 |
| :-- | :-: | :-- |
| ⛔ **约束解码 / 受限解码** | ⛔ **无** | ⭐ **S 级（强）**：⭐ Fig. 3 逐字说**只换 prompt 层、其它一切不变**；⭐ 摘要说 "embeds … **directly into the prompt**"。⚠️⚠️ ⭐ **而作者知道这条路存在** —— ⭐ 参考文献 [9] 正是 Geng et al. 的 **Grammar-Constrained Decoding**（⭐ 我已核验为真）。⛔ **引了但没用。** |
| ⛔ **schema / validator** | ⛔ **无**（⭐ 生成期） | ⭐ S 级：⭐ 摘要与 7 条图注里没有任何 parser / validator / schema 环节；⭐ 判定装置全在事后（⭐ 5 个 validator LLM ＋ BLEU ＋ 人） |
| ⛔ **多轮 / 迭代** | ⛔ **无** | ⭐⭐ **M 级**：⭐ 摘要逐字 "**first-pass** synthesis" —— ⭐ SCP 的卖点就是**一遍成**。⭐ Fig. 1 逐字把 CoVe 的多轮事后自检当作被批评对象 |
| ⛔ **编译器在环** | ⛔ **无** | ⭐⭐ **M 级，⛔ 且是自陈**：⭐ 摘要 future work 逐字 "Future work will strengthen industrial applicability by **adding compiler- and simulation-in-the-loop validation**" |
| ⭐ **固定 prompt 模板** | ⭐⭐ **有 —— 就是它** | ⭐ M：⭐ Fig. 2 逐字 "**Fixed SCP prompt**" ＋ "**The template** embeds…" |

### ⭐ 模板里塞了什么（⭐ 四类，⛔ 摘要逐字）

| # | 逐字英文 | 是什么 |
| :-: | :-- | :-- |
| 1 | `IEC 61131-3 rules` | ⭐ 标准规则（⭐ 语言标准） |
| 2 | `vendor syntax profiles` | ⭐ 厂商语法方言（⭐ Siemens TIA Portal） |
| 3 | `declaration discipline` | ⭐ 声明纪律（⭐ 变量/块的声明规范） |
| 4 | `safety-oriented structural templates` | ⭐ 面向安全的结构模板 |

⭐⭐ **归纳：⭐ "生成期强制符合性" 在 SCP 这里的准确含义是「⭐⭐ 把标准与厂商约束写进一份固定 prompt 模板，让第一遍就朝着符合的方向生成」**，⛔ **不是「在生成过程中拦截不符合的输出」。** ⭐⭐ **这个区分是回答 [必答③](#-必答--它强制的那些约束是不是都是-prefix-checkable-的) 的全部关键。**

---

## ⭐⭐ 必答② · 它批评 post-hoc 自检的理由与证据是什么

### ⭐ 理由（⭐ 机理性论证，M）

⭐ 摘要逐字：

> "Verification-centric prompting such as **Chain-of-Verification (CoVe)** can reduce reasoning errors via post-hoc self-checking, **but it does not enforce conformance during generation; consequently, outputs may remain non-compilable or structurally non-compliant.**"

⭐ Fig. 1 图注逐字（⭐ 更直白）：

> "Comparison of prompting workflows. **CoVe applies verification only after code generation, which cannot prevent structural or toolchain violations.** SCP embeds IEC 61131-3 and vendor constraints during generation, enabling first-pass, TIA Portal-targeted PLC code."

⭐⭐ **拆开看，它的论证是两段**：

1. ⭐ **事后自检改不了"结构性"违规** —— ⭐ 逐字关键词是 `structural or toolchain violations`。⭐ 即：⭐ 局部改错（reasoning error）事后能补，⛔ **但"整体结构不对"或"过不了厂商工具链"这类属性，事后打补丁改不动。**
2. ⭐ **符合性必须在第一遍就成立** —— ⭐ 逐字 `constrain first-pass synthesis`。

⭐ **这条机理论证本身是站得住的**，⛔ 而且它与我们的经验一致：⭐ 我们 v46 的两个 LLM 自评 reviewer 零收益，⭐ 也是「事后自检改不了结构性问题」的一个实例。

### ⛔⛔ 证据 —— ⭐ 三条，⛔ **一条查实伪造、一条未能核验、一条没有数字**

| 证据 | 是什么级别 | 状态 |
| :-- | :-- | :-- |
| ⭐ **对照实验 vs CoVe** | ⭐ 实验 | ⭐ **有，⛔ 但数字取不到。** ⭐ 摘要逐字："Across validators, SCP achieves **higher and more stable correctness ratings than CoVe** while **reducing safety-related failure modes and post-hoc correction needs**; BLEU and expert Human-in-the-Loop (HITL) review are additionally reported as secondary comparisons." ⛔⛔ **零具体数字** —— ⭐ 数字在 Tables I–III，⛔ 全文不可得（⭐ Fig. 7 图注逐字提到 "the LITL results in **Tables I–III**"） |
| ⛔⛔ **文献 [7]「Revisiting Iterative Self-Verification in LLMs」** | ⛔ 本该是理论依据 | ⛔⛔ **查实为伪造引用** —— ⭐ `arXiv:2501.01234` 实际是 **"Impact of QCD sum rules coupling constants on neutron stars structure"**（⭐ 见 [警告 3](#-警告-3--参考文献里查实一条伪造引用-而它正是批评-post-hoc-自检的承重依据)） |
| ⚠️ **文献 [11]「On the Limits of Automated Feedback Loops for Code Generation with Large Language Models」EMNLP 2023** | ⭐ 本该是理论依据 | ⚠️ ⛔ **未能核验** —— ⛔ 无 DOI、⛔ 无 arXiv id、⛔ 本轮未查（⭐ 见 [F.3](#f-存疑与未核项)）。⭐⭐ **若这一条是真的，它对我们独立有价值**（⭐ 标题正好是「自动反馈循环的极限」，⭐ 直接对上我们「第 3–5 轮零收益」） |
| ⭐ **CoVe 原文 [3]** | ⭐ 被批评对象的出处 | ⭐ ✅ **真** —— `aclanthology.org/2024.findings-acl.212/`（Dhuliawala et al., Findings of ACL 2024） |

### ⚠️⚠️⚠️ 一个**自反的问题**（⭐ 本卡最重要的独立观察）

⭐ **它批评 CoVe「只在事后验证」，⛔ 而 SCP 自己的验证也是完全事后的 —— ⭐ 而且裁决者是 5 个 LLM。**

⭐ 摘要逐字（M）：

> "SCP is evaluated on a fixed 25-industrial use cases under a reproducible protocol, with **primary validation based on LLM-in-the-Loop (LITL) semantic assessment using five independent validator LLMs.**"

⭐ Fig. 5 图注逐字（M，⭐ 描述得更清楚）：

> "Two-lane LITL workflow for comparing SCP and CoVe under identical conditions. Both prompts generate PLC code using the same code generator model; **the same five validator LLMs then assign semantic-correctness scores and pass/fail outcomes under a fixed scoring prompt**, followed by an **inter-validator agreement analysis**."

⭐⭐ **而标题里的 "Compiler-Ready" 从未被编译器验证过** —— ⭐ 摘要 future work 逐字："Future work will strengthen industrial applicability by **adding compiler- and simulation-in-the-loop validation**"。

⭐⭐⭐ **合起来是一个三重张力**：

1. ⛔ 标题写 **"Compiler-Ready"** —— ⛔ **而没有跑过编译器。**
2. ⛔ 副标题写 **"From Post-Hoc Verification to Standard-Driven Code Synthesis"** —— ⛔ **而它自己的验证 100% 是 post-hoc 的。**
3. ⛔ 批评 CoVe 的 **self-checking**（⛔ LLM 检查 LLM）—— ⛔ **而它的主判定装置正是 5 个 LLM 检查 1 个 LLM。**

⚠️ **公平地说，⭐ 第 2、3 点有一个可辩护的读法**：⭐ 它区分的是**"约束放在哪一端"**（⭐ 生成端 vs 验证端），⛔ 而不是"要不要验证"。⭐ 即：⭐ 它主张**约束前移**，⛔ 但**评测当然只能在事后做**。⭐ 这个读法下第 2、3 点不算自相矛盾。⛔ **但第 1 点没有辩护空间** —— ⭐ "Compiler-Ready" 是一个可被编译器一票判定的属性，⛔ 而它没测。

---

## ⭐⭐⭐ 必答③ · 它强制的那些约束，是不是都是 prefix-checkable 的？

## ⭐⭐⭐ 若有不是的，它怎么处理？

> ⭐⭐ **这一节是任务书要单独拎出来的那条。⭐ 结论先写：⛔ 不都是；⭐ 而这**不重要** —— ⭐ 因为 prefix-checkability 这个约束对 SCP 根本不适用。⭐⭐ **§11 的新判据不需要再改。**

### ⭐ 第一步 · **问题为什么不成立**

⭐ `prefix-checkability` 是 [atlas-layered-constraints](./atlas-layered-constraints.md) 给**约束解码器（decoder-side controller）**定的准入判据，⭐ 逐字：

> "Item (i) states the **admission policy: only prefix-checkable structural fragments are sent to L1**."（⭐ L1 ＝ 生成期约束解码）

⭐ 它约束的是「**什么能做成生成期的门**」—— ⭐ 因为门必须在**只看到半成品**时就做出拦截决定。

⭐⭐⭐ **而 SCP 的生成期里没有门，只有指令。** ⭐ 见 [必答①](#-必答--生成期强制符合性具体怎么实现-约束解码--模板--schema--多轮)：⛔ 无约束解码 · ⛔ 无 validator · ⛔ 无 schema · ⛔ 无多轮 · ⛔ 无编译器。⭐ 模型照不照办，⭐ **没有任何装置在 token 层拦截**。

⭐⭐ **推论：⭐ SCP 塞进 prompt 的约束可以是任意形状 —— ⭐ 包括完全不可前缀判定的、甚至根本不可机械判定的。** ⭐ 因为**它不需要判定，它只需要被读到**。

### ⭐ 第二步 · **它塞进去的四类，逐类判 prefix-checkability**

⭐ 按 ATLAS 的三族划分（M，逐字）："$\mathcal{R}_{\mathrm{struct}}$ contains **prefix-checkable** structural obligations such as containment, field presence, ordering, and local typing patterns; $\mathcal{R}_{\mathrm{sem}}$ contains **graph-level or reference-level obligations that require the completed artifact**; $\mathcal{R}_{\mathrm{log}}$ contains **numeric, temporal, or solver-backed** domain conditions."

| SCP 的四类 | ⭐ 前缀可判定？ | ⭐ 落在 ATLAS 哪一族 | 理由 |
| :-- | :-: | :-- | :-- |
| ⭐ ① `IEC 61131-3 rules` | ⚠️ **部分** | ⭐ struct ＋ sem 混 | ⭐ 词法/语法层（关键字、块结构、类型字面量）**是**前缀可判定的；⛔ 但标准里也有跨块语义要求（⭐ 例如 POU 接口与调用的一致性），⛔ 那些不是 |
| ⭐ ② `vendor syntax profiles` | ⚠️ **部分** | ⭐ struct 为主 | ⭐ 方言关键字与保留标识符是词法层；⛔ 但"能过 TIA Portal 编译"这个整体属性**必须读完整份程序 ＋ 跑编译器** |
| ⛔ ③ `declaration discipline` | ⛔⛔ **不是** | ⭐⭐ **sem（cross-reference）** | ⭐ 声明与使用的一致性是**跨引用**属性 —— ⭐ ATLAS 明确把 "**Cross-reference integrity**" 划到 L2（⭐ 逐字："Cross-reference integrity, graph acyclicity, type compatibility across distant elements, or numeric timing constraints **require the completed artifact and belong in L2**"） |
| ⛔ ④ `safety-oriented structural templates` | ⛔⛔ **不是** | ⭐ sem（⭐ 可能到 log） | ⭐ "面向安全的结构"是**跨块的整体形状**，⛔ 半成品上判不了。⭐ 摘要还提到它意在 "**reducing safety-related failure modes**" —— ⭐ 失败模式是行为属性，⛔ 更判不了 |
| ⭐ 论文自陈的目标属性 `compiler-ready` | ⛔⛔ **绝对不是** | ⭐⭐ **log / 外部 oracle** | ⭐ 需要编译器 —— ⛔ **而这正是论文的 future work** |

⭐⭐ **所以：⛔ 它强制的四类里，⭐ 至少两类（③④）明确不是 prefix-checkable，⭐ 另两类（①②）只有词法子集是。**

### ⭐ 第三步 · **它怎么处理那些不是的**

⭐⭐ **答案：⛔ 生成期不处理，⭐ 全部推到事后。** ⭐ 三层事后装置（M，摘要 ＋ Fig. 5/7）：

| 层 | 装置 | 逐字 |
| :-- | :-- | :-- |
| ⭐ **主判定** | ⛔ **5 个独立 validator LLM**（LITL） | ⭐ "primary validation based on **LLM-in-the-Loop (LITL)** semantic assessment using **five independent validator LLMs**"，⭐ 用**固定评分 prompt**（⭐ Fig. 4 逐字 "Evaluation prompt **issued verbatim** to all validator LLMs for reproducible LITL scoring"） |
| ⭐ 次判定 | ⭐ **BLEU** | ⭐ "BLEU … additionally reported as secondary comparisons" |
| ⭐ 次判定 | ⭐ **人类专家 HITL** | ⭐ "expert **Human-in-the-Loop (HITL)** review are additionally reported as secondary comparisons"；⭐ Fig. 7 逐字 "Expert scores are treated as a **separate validation layer** from the LITL results in Tables I–III" |
| ⛔ **编译器 / 仿真** | ⛔ **无** | ⛔ future work |

⭐⭐⭐ **也就是说：⭐ SCP 把"不可前缀判定的约束"处理成 ——「⭐ 生成端写进 prompt ＋ ⛔ 事后由评审端检查」。** ⭐⭐ **这恰好就是本仓库 §11 规定的那条出路。**

### ⭐⭐⭐ 第四步 · **对 §11 的裁定（⛔ 这是任务书要的那个答案）**

> ⭐⭐⭐ **裁定：⭐ §11 的新判据（含从 ATLAS 加的 prefix-checkability 那一维）⛔ 不需要再改。⭐ SCP 与它不冲突 —— ⭐ SCP 恰好落在 §11 已经指定的那个去处里，⭐ 并且给那个去处补上了 §11 目前缺的"该写什么"。**

⭐ **三条论证：**

**① ⭐ 三者管的是三个不同位置，⛔ 不在同一个位置上竞争。**

| 判据 | 管什么 | 判据内容 |
| :-- | :-- | :-- |
| ⭐ 本仓库 **§11** | ⭐ 什么能进 **schema / validator**（⭐ 确定性一票否决门） | ⭐ **能否只看字段值就唯一判定** |
| ⭐ **ATLAS L1 准入** | ⭐ 什么能进 **约束解码器**（⭐ 生成期 token 级门） | ⭐ **能否只看前缀就判定** |
| ⭐⭐ **SCP** | ⭐⭐ **什么该写进 prompt** | ⛔⛔ **没有准入判据 —— 什么都能写** |

⭐⭐ **而 §11 早已写明第三个位置的用途**（⭐ [CLAUDE.md](../../../../../CLAUDE.md) §11 逐字）：

> "其余一律不许进 validator，改为「**生成端写清纪律 ＋ 评审端负责检查 ＋ 打回修订**」：⭐ 生成端 prompt 与 `Field(description=...)` 明确写出纪律与 worked example；⭐ 评审端 prompt 明确要求检查这一条，不满足就判 revise 并说明要改什么"

⭐⭐ **SCP 做的就是这句话的前半句。** ⛔ **所以它是 §11 的一个实例，不是对手。**

**② ⛔ 唯一要挡住的是一种误读。**

⛔ 「**把符合性提前到生成期**」这句话听起来像在说"约束应该做成生成期的门"。⛔ **但 SCP 没有做门 —— 它做的是更详尽的 prompt。**

⭐⭐ **若有人据 SCP 主张「把 IEC / 元模型规则做成 validator」，那是对它的误读 —— ⛔ 而那正是我们 `named_elements` 事故的成因**（⭐ 一条需要语义判断的约束被实现成词法近似，⭐ 结果 18/18 撞死、⛔ 烧掉约 16 万 output token）。⭐ ATLAS 那一维已经解释了这个机制（⭐ 逐字："当一条约束只在完工后才可判，却被塞进生成期的门里，实现者就必然被迫用词法近似去替代语义判断"）。⭐⭐ **SCP 不但不支持这种误读，⭐ 反而是它的反例：⭐ 一篇明确主张"约束前移"的论文，⭐ 选择的实现方式恰恰是 prompt 而不是门 —— ⭐ 而它引了约束解码的文献却没用。**

**③ ⭐⭐ 但 SCP 确实补上了 §11 缺的一块：⭐ 生成端 prompt 该写什么、写多细、什么形态。**

⭐ §11 目前只说"写清纪律 ＋ worked example"，⛔ **没说结构**。⭐ SCP 给了两样东西：

- ⭐⭐ **一个四层内容结构**：⭐ ① 标准规则 · ② 厂商方言 profile · ③ 声明纪律 · ④ 面向安全的结构模板
- ⭐⭐ **一个形态要求：固定模板**（⭐ Fig. 2 逐字 "**Fixed** SCP prompt"；⭐ Fig. 4 逐字 "issued **verbatim**"）—— ⛔ 不是散落在各处的段落

⭐ **可搬的具体动作（→ M1）**：⭐ 把我们生成端的纪律按四层重组并做成**固定模板**：

| SCP 的层 | ⭐ 我们的对应物 |
| :-- | :-- |
| ⭐ ① 标准规则 | ⭐ pyfcstm 元模型的定义性约束（⭐ 我们 provenance 的 ② 类 6 条） |
| ⭐ ② 厂商语法 profile | ⭐ pyfcstm DSL 方言的具体写法约束 |
| ⭐ ③ 声明纪律 | ⭐⭐ **谓词参数的绑定纪律 ＋ 元素引用必须已声明** —— ⚠️ **我们正是在这一格上踩过雷**（⭐ 引用门 / `blocked_by` / 依赖闭包那四条互斥，⭐ 见 [CLAUDE.md](../../../../../CLAUDE.md) §13） |
| ⭐ ④ 面向安全的结构模板 | ⭐ `AssertionScript` 的结构模板（⭐ 按 `verification_kind` 分族给 worked example） |

### ⛔⛔ 但这条裁定必须带一个很硬的限定

⛔⛔ **SCP 的证据强度极低，⛔ 不得用它去支持任何对 §11 的修改。** ⭐ 六条理由：

1. ⛔ **全文不可得** —— ⭐ 本卡全部据摘要 ＋ 图注 ＋ 参考文献
2. ⛔ **零具体数字** —— ⭐ 全部在取不到的 Tables I–III 里
3. ⛔⛔ **主判定是 LLM-as-judge**（⭐ 5 个 validator LLM），⛔ 无编译器、⛔ 无仿真
4. ⛔⛔ **"Compiler-Ready" 未经编译器验证**
5. ⛔⛔ **制品是代码不是模型** —— ⛔ 不过 L3 硬门 2
6. ⛔⛔ **参考文献里查实一条伪造条目，⛔ 且它正是核心批评的承重依据**

⭐⭐ **所以本卡对 §11 的贡献只有一句：⭐ "有人独立地把符合性约束前移到了生成端 prompt，⭐ 而且形态是固定四层模板" —— ⭐ 这是一个**形态参考**，⛔ 不是证据。**

---

## A. 元信息（⭐ 仅据摘要 ＋ IEEE 题录）

| 字段 | 值 |
| :-- | :-- |
| `id` | `standard-conformant-prompting` |
| `title` | ⭐ **"Standard Conformant Prompting (SCP): A Reproducible Framework for Compiler-Ready PLC Code Generation with Large Language Models : From Post-Hoc Verification to Standard-Driven Code Synthesis in Industrial Automation"**（M，⭐ IEEE ＋ Crossref ＋ Semantic Scholar 三源逐字一致，⭐ 含题名里那个不规范的 ` : `） |
| 作者 | ⭐ **Ketut Adnyana · Andreas Schwung**（M）；⭐ 同属 **Automation Technology and Learning Systems, South Westphalia University of Applied Sciences, Soest, Germany**（M，IEEE `affiliation` 逐字，⭐ Ringgold ID 52787）。⭐ Schwung ORCID [`0000-0001-8405-0977`](https://orcid.org/0000-0001-8405-0977) · Adnyana ORCID [`0009-0003-1091-3313`](https://orcid.org/0009-0003-1091-3313)（M，Crossref） |
| `year` | ⭐ **2026**（M，Crossref `published: 2026-07`；⭐ IEEE `publicationDate: 13 July 2026`；⭐ IEEE 插入日 `2026-08-07`）。⛔ 无 early-access 歧义（⭐ `isEarlyAccess: false`） |
| `venue` | ⭐ **2026 12th International Conference on Control, Decision and Information Technologies (CoDIT)**，⭐ **Bari, Italy**，⭐ **2026-07-13 – 2026-07-16**（M，Crossref `event` ＋ IEEE `confLoc`）。⭐ pp. **124–129**（⭐ 6 页）· Electronic ISBN **979-8-3195-2077-7** · Electronic ISSN **2576-3555** |
| `ccf` | ⭐ **未收录** —— ⭐ 已查本仓库 [ccf_venues/](../../../../../ccf_venues/) 全部 42 个 venue，⭐ 已 grep `CoDIT` 于 [SUMMARY.md](../../../../../ccf_venues/SUMMARY.md) / [01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) / [README.md](../../../../../ccf_venues/README.md)，⛔ **零命中** |
| `doi` | ⭐ [`10.1109/CoDIT70676.2026.11630913`](https://doi.org/10.1109/CoDIT70676.2026.11630913) —— ⭐ **已实际访问核验**：⭐ Crossref `/works/` 返回完整题录（⭐ title / 2 authors / container / event / page `124-129` / `reference-count: 15`）；⭐ OpenAlex 与 Semantic Scholar 双源确认存在（⭐ S2 `CorpusId: 290873655` · `paperId: df01580e…`） |
| `arxiv` | ⛔ **无**（⭐ 已试两个检索式，⛔ 零命中） |
| `url` | ⭐ [ieeexplore.ieee.org/document/11630913](https://ieeexplore.ieee.org/document/11630913/) —— ⛔ **付费墙**（⭐ `accessType: locked` · `isOpenAccess: false`） |
| `artifact_type` | ⛔⛔ **不是模型 —— 是代码**：⭐ **IEC 61131-3 Structured Text PLC 程序**，⭐ 目标平台 Siemens **TIA Portal**（M，摘要逐字 "TIA Portal-targeted PLC code"）。⛔ **无状态机 / SFC / 任何行为模型制品** |
| `task` | ⭐ **生成**（NL 需求 → PLC 代码）＋ ⭐ **评测框架**（⭐ 论文自称 "A Reproducible Framework"，⭐ 且 Fig. 3 是一条标准化评测流水线） |
| `boundary` | ⛔ **`界外`** —— ⛔ **且制品不是模型，⛔ [README.md](../README.md) §2 硬门 2 不过**（⭐ 见 [警告 2](#-警告-2--它不过-l3-的硬门-2-制品是代码不是模型)） |

---

## B. LLM 应用形态（⛔ 仅据摘要 ＋ 图注，⭐ 多格「原文未提供」）

### B1 · 流水线阶段（⛔ 只能据 Fig. 1/3/5 图注重建）

```
┌── 生成侧（⭐ Fig. 3：「只换 prompt 层，其它一切不变」）──────────────────┐
│ [人/确定性] 固定 SCP prompt 模板（⭐ 四层：IEC 规则 · 厂商 profile ·        │
│                                 声明纪律 · 面向安全的结构模板）           │
│    ↓                                                                  │
│ [LLM]      code generator model → IEC 61131-3 ST 代码  ⭐ **first-pass**  │
│            ⛔ 无约束解码 · ⛔ 无 validator · ⛔ 无编译器 · ⛔ 无迭代          │
└───────────────────────────────────────────────────────────────────────┘
   ↓
┌── 评测侧（⭐ Fig. 5 两车道，⭐ SCP 与 CoVe 同条件对跑）──────────────────┐
│ [LLM × 5]  5 个独立 validator LLM，固定评分 prompt（⭐ Fig. 4「verbatim」）│
│              → 语义正确性分数 ＋ pass/fail                              │
│    ↓                                                                  │
│ [确定性]   inter-validator agreement analysis                          │
│ [确定性]   BLEU（⭐ 次要口径）                                            │
│ [人]      expert HITL review（⭐ Fig. 7，⭐ 独立一层）                     │
│ ⛔ 编译器 / 仿真 —— **future work**                                     │
└───────────────────────────────────────────────────────────────────────┘
```

⭐⭐ **可数出的阶段：⭐ 生成侧 2 段（1 确定性 ＋ 1 LLM）· ⭐ 评测侧 4 段（1 LLM 组 ＋ 2 确定性 ＋ 1 人）＝ 6 段；⛔ 其中 LLM 2 段（⭐ 但评测侧那一段是 5 个模型）。**

⚠️⚠️ ⭐ **注意这条流水线的一个结构特征：⛔ 生成侧一个判定装置都没有。** ⭐ 全部判定在评测侧，⛔ 且**不回灌** —— ⛔ **没有循环。**

⛔ **各阶段的实现细节、prompt 全文、代码生成器的具体调用参数：原文未提供**（⭐ 全文不可得）。

### B2 · 每次 LLM 调用的角色（⭐ 仅据摘要 ＋ 图注）

| 环节 | 角色 |
| :-- | :-- |
| ⭐ code generator | ⭐ **生成器**（⭐ NL 需求 → ST 代码） |
| ⛔ 5 个 validator LLM | ⛔⛔ **裁决者（LLM-as-judge）** —— ⭐ Fig. 5 逐字 "assign semantic-correctness scores and **pass/fail outcomes**"。⭐⭐ **注意：它们给的是 pass/fail，⛔ 即真的在裁决，⛔ 不只是打分** |
| ⛔ 修复者 / 评审者（生成侧） | ⛔ **无** —— ⭐ SCP 的卖点是 first-pass，⛔ 无修订环节 |

### B3 · prompt 策略（⭐ 仅据摘要 ＋ 图注）

| 策略 | 有无 | 证据 |
| :-- | :-: | :-- |
| ⭐⭐ **固定模板 ＋ 领域约束注入** | ⭐ **有（⭐ 这就是全部方法）** | ⭐ M，见 [必答①](#-必答--生成期强制符合性具体怎么实现-约束解码--模板--schema--多轮) |
| ⭐ **固定评测 prompt（逐字下发）** | ⭐ **有** | ⭐ M，Fig. 4 逐字 "Evaluation prompt **issued verbatim** to all validator LLMs for reproducible LITL scoring"；⭐ Fig. 5 逐字 "under a **fixed scoring prompt**" |
| ⛔ **受限解码 / 语法约束** | ⛔ **无** | ⭐ S（强），⭐ 见 [必答①](#-第一步--问题为什么不成立)。⚠️ ⛔ **引了 [9] Grammar-Constrained Decoding 但没用** |
| ⛔ **CoVe / 迭代自检** | ⛔⛔ **无 —— 且是被批评对象** | ⭐ M，见 [必答②](#-必答--它批评-post-hoc-自检的理由与证据是什么) |
| ⛔ few-shot / CoT / self-consistency 投票 / RAG / tool calling / 结构化输出 schema | ⛔ **原文未提供** | ⭐ 摘要与 7 条图注均无表述。⚠️ ⭐ **同组另有一篇专做 CoT 扩展的姊妹篇**（⭐ `CoT+`，`10.1016/j.mlwa.2026.100960`），⭐ 说明 CoT 在他们的体系里是**另一条独立技术**，⛔ 不在 SCP 里（S） |
| ⭐ **prompt 是否公开** | ⚠️ **🟠 —— 部分在论文图里** | ⭐ Fig. 2 是一份**完整的 SCP prompt 图**、⭐ Fig. 4 是**完整的评测 prompt 图** —— ⭐⭐ **即 prompt 以图片形式印在论文里**，⛔ **但论文付费墙 ＋ 图内文字不可机械提取** |

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

⭐⭐⭐ **答案很短：⛔ 没有循环。⭐ 而唯一的裁决者是 5 个 LLM。**

| 子字段 | 值 |
| :-- | :-- |
| ⭐ **有无循环** | ⛔⛔ **无** —— ⭐ M，摘要逐字 `first-pass synthesis`；⛔ Fig. 1–7 里没有任何回边 |
| ⭐⭐ **裁决者是谁** | ⛔⛔ **`LLM 自评`（⭐ 严格说是 `LLM 互评`）** —— ⭐ **5 个独立 validator LLM 给 pass/fail**。⛔ `sound oracle` = **无** · ⛔ `parser / 编译器` = **无（⭐ future work）** · ⛔ `测试执行` = **无（⭐ 仿真也是 future work）** · ⭐ `人` = **有，但明确是次要层**（⭐ Fig. 7 逐字 "a **separate validation layer**"；⭐ 摘要逐字 "**additionally reported as secondary comparisons**"）· ⛔ `确定性规则` = 只有 BLEU（⭐ 次要口径） |
| ⭐ 终止条件 | ⛔ **不适用（⭐ 无循环）** |
| ⭐ 最大轮数 | ⭐ **1**（⭐ first-pass） |
| ⭐ **有无报告循环的边际收益** | ⛔ **不适用** —— ⭐⭐ **但它报了一个替代物**：⭐ 摘要逐字 "reducing safety-related failure modes and **post-hoc correction needs**"，⭐ 即**它主张"约束前移能减少事后修正的需要"** —— ⛔ **而这个"减少"没有给数字**（⭐ 数字在取不到的 Tables I–III） |

⭐⭐⭐ **这一格对我们的直接价值（⛔ 也是它与 [ERTS](./erts2026-safe-llm-mde.md) / [AutoSM](./icse2025-autosm.md) 的三方对照）：**

| | ⭐ 裁决者 | ⭐ 循环 | ⭐ 结果 |
| :-- | :-- | :-- | :-- |
| ⭐ [ERTS 2026](./erts2026-safe-llm-mde.md) | ⭐⭐ **sound oracle**（模型检查器）**在裁决端** | ⭐ 有（20 轮） | ⛔ **5/6 撞上限不收敛** |
| ⭐ [AutoSM (ICSE 2025)](./icse2025-autosm.md) | ⭐ **parser 在裁决端**；⭐ sound oracle 在**评测端** | ⭐ 有（人在环） | ⭐ 10/18；⛔ LLM 自评只降 14.74% 错误 |
| ⭐ **SCP（本篇）** | ⛔⛔ **5 个 LLM 在裁决端** | ⛔ **无** | ⛔ **无数字可引** |
| ⭐ 我们（v46） | ⛔ **LLM 自评在裁决端**；⭐ sound oracle 在**求值端** | ⭐ 有 | ⛔ **第 3–5 轮零收益，吃 79% token** |

⭐⭐ **四家排成一条谱：⛔ SCP 最激进地取消了循环（⭐ 靠 prompt 一次成），⛔ ERTS 最激进地加强了裁决者（⭐ 靠模型检查器），⭐ 而两端都没有拿到令人满意的结果。** ⭐ **这本身就是 M1 该注意的信号：⛔ 单靠"取消循环"或"加强裁决者"任一端都不够。**

### B5 · ⭐ 中间表示（⭐ 仅据摘要）

| 子字段 | 值 |
| :-- | :-- |
| ⭐ **有无** | ⚠️ **有一个弱形态的** —— ⭐ 摘要提到 `safety-oriented structural templates`（⭐ 面向安全的结构模板），⭐ 即代码骨架层面的模板。⛔ **但那不是独立的中间制品**（⛔ LLM 直接产出终态 ST 代码，⛔ 中间没有另一层可检查的表示） |
| ⭐ 形态 | ⭐ **prompt 内的结构模板 ＋ 约束清单**（⛔ 不是 DSL / IR / 缺陷类型学 / 谓词族） |
| ⭐ **是否闭合** | ⚠️ **判不出** —— ⭐ 摘要给了四类约束的**类目**（⭐ 闭合到 4 类），⛔ 但每类里具体有多少条规则、是否穷举、能否扩展：⛔ **原文未提供** |
| ⭐ **谁定的** | ⭐ **作者预编**（⭐ 从 IEC 61131-3 标准 ＋ 厂商文档抽）。⭐⭐ **注意出处很干净**：⭐ ① `IEC 61131-3` 是**国际标准**（⭐ 我们 provenance 的 ① 类）· ② 厂商 profile 是**工具规约**（⭐ ① 类）—— ⛔ ③④ 两类（声明纪律 · 安全结构模板）的出处：⛔ **原文未提供** |
| ⛔ **谁来选** | ⛔⛔ **无人选 —— 固定模板，全量注入**（⭐ Fig. 2 逐字 "**Fixed** SCP prompt"）。⭐ **与 LLM 自动选相反** |

⭐⭐ **与我们 19 条闭合谓词的对照**：

| 维度 | ⭐ 它 | ⭐ 我们 |
| :-- | :-- | :-- |
| ⭐ 约束放在哪 | ⭐⭐ **生成端 prompt**（⛔ 全量固定注入） | ⭐ 生成端 prompt ＋ ⛔ **确定性契约门（validator）** |
| ⭐ 谁选 | ⛔ **无人选，全量注入** | ⭐ **LLM 每条需求选一** |
| ⭐ 判定时机 | ⛔ **生成期不判，事后由 LLM 判** | ⭐ 生成期有门 ＋ 求值端有 pyfcstm |
| ⭐ 出处 | ⭐ ①② 挂国际标准与工具规约（⭐ 干净）；⛔ ③④ 未给 | ⭐ **① 12 · ② 6 · ③ 1** |

⚠️ ⭐ **有一条值得注意的反向提示**：⭐ **它把约束全量注入 prompt 而不做筛选。** ⭐ 对照 [SoSyM 那篇](./sosym2026-state-machine-consistency.md) 的实测（⭐ 逐字："when these rules are incorporated into the consistency request (C1), **the LLM tends to exclusively focus on these rules, thus ignoring other consistency aspects**"）—— ⭐⭐ **全量注入有隧道视野的风险，⛔ 而 SCP 没有讨论这一点，⛔ 也没有做只注入部分规则的对照。** ⭐ 这是一个**未被检验的假设**。

### B6 · 模型

⛔⛔ **代码生成器的型号：原文未提供。⛔ 5 个 validator LLM 的型号：原文未提供。**

⭐ 已实际核验：⭐ 摘要、7 条图注、15 条参考文献、三组关键词里**均无任何模型型号**。

| 项 | 值 |
| :-- | :-- |
| ⛔ code generator 型号 | ⛔ **原文未提供**（⭐ Fig. 5 只说 "**the same** code generator model"，⭐ 即两臂共用一个，⛔ 但没说是哪个） |
| ⛔ 5 个 validator 型号 | ⛔ **原文未提供**（⭐ 只知 "**five independent** validator LLMs"） |
| ⭐ **有无多模型对照** | ⚠️ **在判定侧有（5 个 validator），⛔ 在生成侧没有**（⭐ Fig. 5 逐字 "the **same** code generator model"） |

⚠️⚠️ **这使本篇的结论完全无法做代际归因。** ⭐ 且注意一个**更严重的方法学后果**：⛔⛔ **主判定装置（5 个 validator LLM）的型号未知，⛔ 意味着"SCP 比 CoVe 分数高"这个结论的裁决基准是不可复现的** —— ⭐ 尽管论文标题自称 "A **Reproducible** Framework"。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 |
| :-- | :-- |
| ⭐ prompt 模板固定 | ⭐ 固定文本，⭐ 逐字下发（⭐ Fig. 2 / Fig. 4） |
| ⭐ BLEU | ⭐ 词法相似度（⭐ 次要口径） |
| ⭐ inter-validator agreement 分析 | ⭐ 统计（⭐ Fig. 5 逐字，⛔ 具体统计量未提供） |
| ⛔⛔ **编译器** | ⛔⛔ **无 —— future work** |
| ⛔ 仿真 / 测试执行 | ⛔ **无 —— future work** |
| ⛔ parser / 语法检查 / schema validator | ⛔ **无** |

⭐⭐⭐ **这一格的核心发现：⛔ 一篇标题写 "Compiler-Ready" 的论文，⛔ 整条流水线里没有编译器。** ⭐⭐ **它的"可信底座"只有一份固定 prompt ＋ 一个 BLEU** —— ⛔ **判定权 100% 在 LLM 手里。** ⭐ 这是本轨到目前为止**确定性成分最薄**的一篇（⛔ 对照 [ERTS](./erts2026-safe-llm-mde.md) 的 5/7 段确定性 ＋ 模型检查器）。

---

## C. 实验（⭐ 仅据摘要 ＋ 图注，⛔ 数字全部不可得）

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐⭐ **有一条：Chain-of-Verification (CoVe)**（M，⭐ 出处 [3] Dhuliawala et al., Findings of ACL 2024，⭐ 已核验为真）。⭐ 同条件对跑（⭐ Fig. 5 逐字 "under identical conditions … the **same** code generator model"）。⛔ **无 zero-shot 臂、⛔ 无约束解码臂、⛔ 无 LLM4PLC 等已有工作臂**（⭐ 尽管引了 [5] LLM4PLC） |
| `dataset` | ⭐ **固定 25 个工业用例**（M，摘要逐字 "a **fixed 25-industrial use cases** under a reproducible protocol"）。⛔ **用例来源、领域分布、体量、是否公开：原文未提供。** ⭐ 唯一知道具体名字的两个：⭐ Fig. 6 逐字 "on the **Robot Pick and Place** use case" · ⭐ Fig. 2 逐字 "a complex **multi-axis robotic coordination and safety-zone control** task" |
| ⭐ **分母怎么定的** | ⛔ **原文未提供** —— ⭐ 只知有 25 个用例、⭐ 每个用例有 **变体 A–J（⭐ 10 个）**（M，Fig. 6 逐字 "across **variants A-J**"）。⚠️ ⛔ **"变体 A–J" 是什么（⭐ 10 次采样？10 个 prompt 变形？10 个子任务？）：原文未提供** —— ⭐ 见 [F.4](#f-存疑与未核项) |
| `metrics` | ⭐ 三层：⭐ ① **LITL 语义正确性分数 ＋ pass/fail**（⭐ 主）· ② **BLEU**（⭐ 次）· ③ **专家 HITL 评分**（⭐ 次）。⭐ 另有 **inter-validator agreement**。⭐ Index Terms 里出现 `Readability` · `Modularity` · `Semantic Scores` · `Evaluation Items`（⭐ 疑为评分维度，S）。⛔ **具体定义、量表、加权：原文未提供** |
| ⭐ **有无 `@k` 口径** | ⚠️ **可能有，⛔ 判不出** —— ⭐ "variants A–J" **若**是 10 次采样，⭐ 那 Fig. 6 就是一个 `@k` 形态；⛔ **但原文未提供其含义** |
| ⭐⭐ `judged_by` | ⛔⛔ **主判定 ＝ LLM-as-judge（⭐ 5 个独立 validator LLM）** —— ⭐ M，摘要 ＋ Fig. 5 逐字。⭐⭐ **有标注者间一致性分析**（⭐ Fig. 5 逐字 "followed by an **inter-validator agreement analysis**"）—— ⭐ 这一点是加分的；⛔ **但具体统计量（$\kappa$ / 一致率 / 相关系数）：原文未提供**。⭐ **人类专家是独立的第二层**（⭐ Fig. 7 逐字 "Expert scores are treated as a **separate validation layer**"）—— ⚠️ ⛔ 但明确是 **secondary**，⛔ **不是主判定** |
| `human_baseline` | ⛔ **无** —— ⭐ 人只用来**评审 LLM 的产出**（HITL），⛔ 不是"人写一份代码来比"。⚠️ ⭐ 注意别把 HITL 误读成 human baseline |
| `runs` | ⛔ **原文未提供**（⭐ 若 "variants A–J" 是采样则为 10，⛔ 但未证） |
| ⭐ `adverse_results` | ⛔⛔ **无法评估** —— ⭐ 摘要里全部是正向陈述（⭐ "higher and more stable correctness ratings" · "reducing safety-related failure modes and post-hoc correction needs"），⛔ **摘要中没有任何一处不利结果、限制或失败案例**。⭐ 唯一接近的是 future work 那句（⭐ 承认缺编译器与仿真验证）。⚠️⚠️ ⭐ **一份 6 页论文的摘要通篇无不利结果，⛔ 这本身是一个信号** —— ⛔ 但**不能据摘要断定正文里也没有**（⭐ 全文不可得）。⛔ **本格判「不可评估」，⛔ 不判「无」** |

⚠️⚠️ ⭐ **关于 "Reproducible" 这个自称的一条独立观察**：⭐ 论文标题与摘要三次强调可复现（⭐ "A **Reproducible** Framework" · "under a **reproducible** protocol" · Fig. 3 "to ensure **reproducibility**" · Fig. 4 "for **reproducible** LITL scoring"）。⛔⛔ **而实际上：⛔ 代码生成器型号未知 · ⛔ 5 个 validator 型号未知 · ⛔ 25 个用例未公开 · ⛔ 无 artifact 链接 · ⛔ 论文本身付费墙。** ⭐⭐ **它"可复现"的含义似乎只是"协议是固定的"（⭐ 固定 prompt、固定评分 prompt、只换 prompt 层），⛔ 而不是"第三方能复现"。** ⭐ 这两件事必须分清 —— ⭐ **前者是内部一致性，⛔ 后者才是可复现性。**

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| ⭐ **论文全文** | ⛔ **🔒** | [ieeexplore.ieee.org/document/11630913](https://ieeexplore.ieee.org/document/11630913/) | ⛔⛔ **本轮未取到。** ⭐ IEEE 逐字 `accessType: {"type":"locked","message":"Full text access may be available."}` · `isOpenAccess: false` · `isFreeDocument: false` · `openAccessFlag: "F"` · `pdfSize: "1703"`（KB）· `sourcePdf: "022_Paper.pdf"`。⭐ Unpaywall 逐字 `{"is_oa": false, "oa_status": "closed", "any_repository_has_fulltext": false}`。⭐ **已试 8 条路，全部失败**（⭐ 见 [警告 1](#-警告-1--全文不可得--本卡是仅据摘要--图注--参考文献)） |
| ⭐ **摘要 ＋ 图注 ＋ 参考文献** | ⭐ **🟢** | ⭐ IEEE `rest/document/11630913/{abstract,figures,references}` | ⭐ **本轮实际取到**：⭐ `abstract` `200 / 8,359 B`（⭐ 含完整摘要 1,247 字符 ＋ 三组关键词 ＋ 作者单位 ＋ ISBN/ISSN）· ⭐ `figures` `200 / 5,935 B`（⭐ Fig. 1–7 全部图注）· ⭐ `references` `200 / 12,389 B`（⭐ 15 条全文）。⭐ 摘要经 **Semantic Scholar Graph API 独立核对，逐字一致** |
| ⭐ **实验代码** | ⛔ **⚪** | — | ⛔ **摘要与图注中无任何代码 / 仓库 / artifact 链接。** ⛔ **原文（正文）是否有 Data Availability 声明：未知**（⭐ 全文不可得） |
| ⭐ **数据集（25 个工业用例）** | ⛔ **⚪ / 🔒** | — | ⛔ **无公开入口。** ⚠️ ⭐ 用例来源未知；⛔ 若是工业私有则应为 🔒，⛔ 但**原文未提供来源**，⭐ 故本格记 ⚪（⭐ 未见提供）并附此不确定 |
| ⭐ **实验结果细则** | ⛔ **⚪** | — | ⛔ **只有论文内 Tables I–III ＋ Fig. 6**（⭐ 由 Fig. 7 图注确证存在），⛔ **均不可得**；⛔ 无可下载逐条结果 |
| Artifact / 复现包 DOI | ⛔ **⚪** | — | ⛔ 无 Zenodo / 4open / OSF DOI |
| ⭐ **prompt 是否公开** | ⚠️ **🟠** | ⭐ 论文 Fig. 2（⭐ SCP prompt）· Fig. 4（⭐ 评测 prompt） | ⭐⭐ **prompt 以图片形式印在论文里** —— ⭐ Fig. 2 图注逐字 "**Fixed SCP prompt** for a complex multi-axis robotic coordination and safety-zone control task"；⭐ Fig. 4 逐字 "Evaluation prompt **issued verbatim** to all validator LLMs"。⛔ **但：⛔ 论文付费墙 · ⛔ 图是 `.tif`（`adnya2-p6-adnya.tif`）· ⛔ 图内文字不可机械提取。** ⭐ 故判 🟠（⭐ 入口存在但取不到内容），⛔ 不判 ⚪ |
| ⭐ **开放获取的姊妹篇**（⭐ 可作旁证） | ⚠️ **🟠** | ⭐ 参考文献 [4]：[`10.1016/j.mlwa.2025.100804`](https://doi.org/10.1016/j.mlwa.2025.100804) | ⭐⭐ **它是 CC-BY gold OA**（⭐ Crossref `license` 逐字含 `creativecommons.org/licenses/by/4.0/` `content-version: vor`；⭐ Unpaywall 逐字 `is_oa: true, oa_status: gold, license: cc-by, version: publishedVersion`）。⛔⛔ **但本轮未取到**：⛔ ScienceDirect `403` Cloudflare · ⛔ `linkinghub` 只回 `Redirecting` · ⛔ `r.jina.ai` `403` · ⛔ SSRN 版 `10.2139/ssrn.5600799` 也 `403`。⭐⭐ **这是最有价值的可补入口**（⭐ 见 [F.2](#f-存疑与未核项)） |

---

## E. 对 M1 的意义

⚠️ **前置限定（⛔ 每一条都受它约束）**：⛔ 本篇**不过 L3 硬门 2**、⛔ 全文不可得、⛔ 无具体数字、⛔ 主判定是 LLM-as-judge、⛔ 参考文献含伪造条目。⭐⭐ **因此下面每一条都只能当"形态参考"，⛔ 不得作为证据引用，⛔ 更不得进论文**（⭐ [README.md](../README.md) §3 防火墙）。

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **「生成端 prompt 的四层内容结构 ＋ 固定模板」这个形态可以搬。** ⭐ 这是本卡唯一实质可用的东西 —— ⭐ 见 [必答③ 第四步](#-第四步--对-11-的裁定-这是任务书要的那个答案) 的对照表。⭐ **具体动作**：⭐ 把我们生成端散落的纪律重组为四层固定模板（⭐ 元模型定义性约束 · pyfcstm DSL 方言约束 · 声明/绑定纪律 · 按 `verification_kind` 分族的断言结构模板），⛔ 而不是分散在各节点的 prompt 段落里。⭐ **理由不是它有效（⛔ 无数字），⭐ 而是"固定模板"让 prompt 本身成为可版本化、可 diff、可审计的对象** —— ⭐ 这对我们 §3.5 的泄漏审查直接有用（⭐ 一份固定模板比散落段落好审得多）。
2. ⭐⭐ **约束的出处分级做得干净（⭐ 前两类）。** ⭐ `IEC 61131-3 rules`（⭐ 国际标准）＋ `vendor syntax profiles`（⭐ 工具规约）—— ⭐ 都是我们 provenance 的 ① 类。⭐ **这印证了一条纪律**：⭐⭐ **生成期该注入的约束，优先取自标准与工具规约，⛔ 而不是从实验失败里归纳。** ⭐ 这与本仓库 §3.5.-1 的「按领域出处反查」同向。
3. ⭐ **判定侧的多裁决者 ＋ 一致性分析这个形态值得注意。** ⭐ 5 个独立 validator LLM ＋ **inter-validator agreement analysis** ＋ 人类专家作为**独立第二层** —— ⭐⭐ **形态上是对的**（⛔ 尽管它选错了主判定装置，⭐ 见下）。⭐ 我们目前的人工逐位判定是单人，⛔ **无标注者间一致性** —— ⭐ 这一格我们比它弱。⭐ **可搬**：G1 全量重标时，⭐ 抽样做双人复核并报一致率。

### 2. ⛔ 不可取 / 陷阱（⭐ 它踩的坑我们必须避开）

1. ⛔⛔⛔ **它把"标题的主张"和"实际测的东西"脱钩了 —— ⭐ 这是本卡最重的一条负面教训。** ⭐ 标题写 **"Compiler-Ready"**，⛔ 而**整条流水线里没有编译器**，⛔ 编译器验证是 future work。⭐⭐ **对我们的直接映射**：⛔ 我们绝不能在标题或摘要里写「可机械求值」「形式化验证」这类词，⛔ 除非**那个装置真的在流水线里跑过并出了数**。⭐ 我们目前是干净的（⭐ pyfcstm 真的在求值端跑），⭐ **但要守住。**
2. ⛔⛔ **它批评 LLM 自检，⛔ 而自己的主判定装置是 5 个 LLM。** ⭐ 这是一个**位置替换而非问题解决**：⛔ 把 LLM 从"生成后自检"挪到"第三方评分"，⛔ 判定权仍然在 LLM 手里，⛔ 且没有任何 sound oracle 兜底。⭐⭐ **对我们的映射**：⛔ 我们要拆 `adjudicate_results` 的 LLM 裁决时，⛔ **不能换成"更多个 LLM 投票"** —— ⭐ 那只是把单个 LLM 自评换成 LLM 委员会，⛔ 不改变"没有可信底座"这个事实。⭐ **正确方向仍是 [ERTS](./erts2026-safe-llm-mde.md) 那条（⭐ 接 sound oracle）＋ 把 oracle 输出变成可执行反馈。**
3. ⛔⛔ **"Reproducible" 的自称与实际不符。** ⭐ 三处强调可复现，⛔ 而模型型号未报、数据未公开、无 artifact。⭐⭐ **对我们的映射**：⭐ 「协议固定」≠「可复现」。⭐ 我们的 run record 纪律（⭐ 精确 `model_id` · provider · 调用日期 · prompt · raw output · usage）正是为了区分这两件事 —— ⭐ **守住它。**
4. ⛔⛔ **参考文献里有伪造条目，⛔ 而它是核心批评的承重依据。** ⭐⭐ **这是本仓库栽过一次假 DOI 后最该记住的一条**（⭐ [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 纪律 3 逐字："**裁定层不核验引用真实性**，所以引用要由写卡的人自己核"）。⭐ **对我们的映射**：⭐ ① 我们自己的每条引用必须实际访问过；⭐ ② **引用别人的论文时，也要顺手核它的关键引用** —— ⭐ 因为一条伪造引用会顺着我们的 Related Work 传播下去。
5. ⛔ **全量注入约束而不检验隧道视野。** ⭐ [SoSyM 那篇](./sosym2026-state-machine-consistency.md) 实测「注入规则会让 LLM 只盯着规则」，⛔ 而 SCP 全量注入四类约束却没有做部分注入的对照。⭐ **对我们的映射**：⛔ 我们已经在 `occupancy_after` 的 `nl_cue` 上栽过这一跤（⛔ `edge_declared` 被问 0.0%），⭐ **所以扩充生成端 prompt 时必须配一个"注入 vs 不注入"的对照，⛔ 不能假定注入越多越好。**
6. ⛔ **无循环意味着无降级路径。** ⭐ first-pass 一次成的设计里，⛔ 没有"失败了怎么办"这一格。⭐ 对照 [ERTS](./erts2026-safe-llm-mde.md) 的 T5（⭐ 存档 ＋ 打分 ＋ 交最好的 ＋ 告知保证失效）—— ⭐ **那才是 §10 要的降级形态。** ⛔ SCP 在这一格是空的。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⛔⛔ **制品不同层：⭐ 它是代码，⭐ 我们是模型。** ⭐ 这是 [README.md](../README.md) §2 硬门 2 的全部理由 —— ⭐ 逐字："**代码有编译器和测试当 oracle，行为模型没有**"。⭐⭐ **讽刺的是 SCP 恰好证明了这条硬门的必要性从反面成立**：⛔ 它有编译器可用（⭐ TIA Portal 就在那儿），⛔ **却没用**，⭐ 转而用 5 个 LLM 打分。⭐ **教训：⛔ 有 oracle 不等于用了 oracle。** ⭐ 我们有 pyfcstm，⛔ 而它在求值端不在裁决端 —— ⛔ **这是同一类问题的一个更轻的版本。**
2. ⭐ **任务方向不同**：⭐ 它是**生成**（NL → 代码），⭐ 我们是**缺陷检测**（模型 vs NL）。⭐ 它的"符合性"是**产物自身的属性**（⭐ 能不能编译、结构对不对）；⛔ 我们的判定对象是**产物与需求的关系** —— ⛔ 那没有任何"标准"可以注入 prompt 来保证。⭐⭐ **所以"把约束前移到生成期"这条策略在我们这里的适用面窄得多**：⭐ 它只能覆盖断言脚本自身的形式规范（⭐ DSL 合法性、谓词签名、绑定纪律），⛔ **覆盖不了"这条需求该问哪个谓词"** —— ⛔ 而后者正是我们的赤字（⛔ 「根本没问」69 位）。
3. ⭐ **它没有中间表示，⭐ 我们有。** ⭐ 它 LLM 直接产终态代码；⭐ 我们有 19 条闭合谓词 ＋ `AssertionScript` 两层。⭐ **这使它的"一次成"策略在我们这里不可行** —— ⛔ 我们的中间层本来就是为了让判定可机械化而存在的。
4. ⛔ **边界完全不同**：⛔ 制品不是行为模型，⛔ 硬门 2 不过。⛔ **它的任何数字都不能当我们的可比数字**（⭐ 何况它没给数字）。

---

## F. 存疑与未核项

1. ⚠️⚠️⚠️ **全文不可得，⛔ 所有数字缺失** —— ⭐ 已试 **8 条入口**（⭐ IEEE stamp / Crossref 的 xplorestaging link / Unpaywall / OpenAlex / Semantic Scholar openAccessPdf / arXiv 两个检索式 / SSRN / ResearchGate / ouci），⛔ 结果分别为 `locked` · Akamai 反爬壳 · `oa_status: closed` · `CLOSED` · 零命中 · `403` · `403` · `502`。⭐ **缺的关键内容**：⛔ Tables I–III 的全部 LITL 数字 · ⛔ Fig. 6 的 A–J 分数 · ⛔ HITL 一致率 · ⛔ inter-validator agreement 统计量 · ⛔ 模型型号 · ⛔ 25 个用例的来源与清单 · ⛔ 正文的限制与不利结果章节。
2. ⚠️⚠️ **最有价值的可补入口：⭐ 开放获取的姊妹篇** —— ⭐ 参考文献 [4] = Adnyana & Schwung, "Benchmarking and validation of prompting techniques for AI-assisted industrial PLC programming", *Machine Learning with Applications* **23**, Art. 100804, Mar 2026, [`10.1016/j.mlwa.2025.100804`](https://doi.org/10.1016/j.mlwa.2025.100804) —— ⭐⭐ **CC-BY gold OA（已核验 license）**，⭐ 且它很可能定义了 SCP 复用的 **LITL / HITL 协议、25 个用例、以及 21 种 prompting 技术的分类**（⚠️ ⛔ **"21 种"这个数来自搜索摘要，⛔ 未核验，⛔ 不得当事实**）。⭐ 已试：⛔ ScienceDirect `403` · ⛔ `linkinghub` 只回 `Redirecting` · ⛔ `r.jina.ai` `403` · ⛔ SSRN 版 `403`。⭐⭐ **建议下一轮换渠道再取**（⭐ 机构订阅 / 浏览器 / Elsevier TDM API key）。
3. ⚠️⚠️ **参考文献 [11] 未核验** —— ⭐ "R. Pan, T. Zhang, and M. Zhou, 'On the Limits of Automated Feedback Loops for Code Generation with Large Language Models,' in Proc. EMNLP, 2023."（⛔ 无 DOI、⛔ 无 arXiv id）。⭐⭐ **这一条独立于本篇对我们有价值**（⭐ 题名正对我们「第 3–5 轮零收益」），⛔ **但鉴于同一份参考文献表里已查实一条伪造条目，⭐ 必须先核实它存不存在。** ⭐ 已试：⛔ 本轮未查（⭐ 优先级留给 SCP 本身）。
4. ⚠️⚠️ **"variants A–J" 的含义未知** —— ⭐ Fig. 6 图注逐字 "Overall LITL scores for SCP and CoVe prompting **across variants A-J** on the Robot Pick and Place use case"。⛔ **10 个变体是什么：10 次采样？10 个 prompt 变形？10 个子任务？10 个评分维度？—— 原文未提供。** ⭐⭐ **这一格很要紧**：⭐ 若是 10 次采样，⭐ 那本篇实际有 `@k` 口径（⭐ 见 [C](#c-实验仅据摘要--图注-数字全部不可得)）。
5. ⚠️ **该作者组是一个高产的 prompting 系列，⛔ 相互关系未梳理** —— ⭐ 我通过 Crossref 按作者检索到 **9 条题录**（⭐ 逐字，⛔ 未逐篇核验内容）：⭐ ① 本篇 `10.1109/codit70676.2026.11630913` · ② 同届 CoDIT 另一篇 "From Chain-of-Note to Explainable Cognitive Prompting: Reproducible Multi-Layer Validation for Auditable LLM-A…" `10.1109/codit70676.2026.11630927` · ③ benchmark 姊妹篇 `10.1016/j.mlwa.2025.100804`（＋ SSRN `10.2139/ssrn.5600799`）· ④ "CoT+ … for deterministic PLC …" `10.1016/j.mlwa.2026.100960`（＋ SSRN `10.2139/ssrn.6247781`）· ⑤ "Active learning for interactive prompt clarification in safety-critical PLC code generation" `10.1016/j.asoc.2026.116165`（＋ SSRN `10.2139/ssrn.6635083`）· ⑥ "From Active Learning to Inference-Time Governance for LLM-Assisted Code Generation: A Systematic Literature Re…" SSRN `10.2139/ssrn.6770198`。⚠️ ⛔ **SCP 在这个系列里的位置（⭐ 是最早的？被 CoT+ 取代了？）未确定。** ⭐⭐ **注意 ④ 与 ② 的题名里同样出现 "Reproducible"** —— ⭐ 这是一个**系列性的自称**，⛔ 值得整体存疑而非只质疑本篇。
6. ⚠️ **约束 ③④ 的出处未知** —— ⭐ `declaration discipline` 与 `safety-oriented structural templates` 是否有外部依据（⭐ IEC 61508 / PLCopen 编码规范 / 厂商 style guide？），⛔ **原文未提供**（⭐ 摘要层面）。⛔ 故 [B5](#b5--中间表示-仅据摘要) 的出处一栏对这两类只能写「未提供」。
7. ⚠️ **是否真的一次都没有迭代** —— ⭐ "first-pass synthesis" 是摘要的措辞（M），⛔ 但**正文是否有任何重试/回退机制：未知**。⛔ 故 [B4](#b4--循环与裁决者本轨最关键的一格) 的「无循环」是**据摘要的强推断（S）**，⛔ 不是 M。
8. ⚠️ **参考文献 [6][8][10] 是否确为伪造** —— ⭐ 已确证的只有 **[7]**（⭐ arXiv id 指向另一篇论文，⭐ 我实际访问过）。⭐ [6][8] 的 DOI 是 literal `XXXXXXX` 占位符 ＋ Crossref 按题名无匹配，⭐ [10] 无 DOI ＋ Crossref 无匹配 —— ⭐⭐ **这是强嫌疑，⛔ 但"Crossref 检索不到"不等于"不存在"**（⛔ 可能索引缺失）。⛔ **故本卡只对 [7] 下"查实伪造"的定论，⭐ 对 [6][8][10] 记为"强嫌疑、待核"。**
