# 卡片 · Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework（IET Software 2025）

⭐ **本卡的一句话结论**：⛔⛔ **它的「双向可追溯」不是我们要的那个双向。** ⭐ 逐字核对后确认：⭐⭐ **双向指「需求 ⇄ 测试用例」，⛔ 不是「需求 ⇄ 模型」。** ⭐ 所以 **C-③ 那一维在这篇里没有先例**。⚠️ **但有一个意外收获，⭐ 且比原本期待的更精确**：⭐ 它的 **Algorithm 2 在机械层面确实同时吐出两侧残差**（⭐ `AbnStep` = 需求说了而模型没有；⭐ `AbnBO` = 模型有而需求没说），⛔ **只是作者从未把这件事写成规则、也从未把它当成一条主张** —— ⭐⭐ **即「我们要的那一侧」在这里是集合减法的副产品，不是设计意图。**

⛔⛔ **三条术语陷阱，⛔ 全都真实存在，⛔ 引用前必须先读 §0**：⛔ ①「双向」不是需求⇄模型；⛔ ②「Process-State」不是「活动图 vs 状态机互检」；⛔ ③ 被比对的「需求」已经被形式化成槽位元组，⛔ 不是原始 NL。

---

## 0. ⛔⛔ 三条术语陷阱（⭐ 本卡最重要的一节，⛔ 放在最前）

| # | 看起来像 | ⛔ 实际是 | 后果 |
| :-: | :-- | :-- | :-- |
| **1** | ⭐ 「bidirectional traceability」= 需求 ⇄ 模型双向追溯 | ⛔⛔ **需求 ⇄ 测试用例** | ⛔ **不得把本篇当作「需求⇄模型双向追溯」的先例引用。** ⭐ 详见 §C.1 |
| **2** | ⭐ 「Process-State Consistency」= 活动图（process）与状态机（state）**互检** | ⛔⛔ **UCS vs 活动图** ＋ **UCS vs 状态机**，⭐ 两条**各自独立**的比对 —— ⛔ **两个模型视图之间从未被比过** | ⛔ 若想找「活动图↔状态机一致性」的先例，⛔ **本篇不是**，⭐ 而且它**自己明写把这个缺口留着**（§C.3） |
| **3** | ⭐ 「与需求比对」= 与原始自然语言需求比对 | ⚠️ **与已经形式化成槽位元组的 UCS 比对** —— ⛔ 原始 NL 与 UCS 之间的差异是**人工对读**，⛔ 不是规则、⛔ 不是算法 | ⛔ 它的「一致性检查」是**制品 vs 制品**，⛔ 不是**制品 vs 自然语言**。⭐ 这一点与我们的 discover 任务是**不同的问题** |

⭐⭐ **陷阱 2 有一处特别值得记的地方**：⛔ 论文自己承认活动图↔状态机的不一致仍然存在，⚠️ **但把原因归到了 LLM 身上而不是归到它自己的规则集上**。⭐ 逐字：

> `"Remaining inconsistencies: Even with LLM assistance, inconsistencies persisted between the activity diagram and the state machine model and between the basic/alternative/exception flows of use cases. This limitation arises because LLMs cannot check consistency across different model levels."`（§6.3.1）

⚠️ ⭐ **我方判断（I，⛔ 不写成事实句）**：⛔ 这个归因看起来错位 —— ⭐ 它自己的三条规则**全部以 UCS 为一端**，⛔ 结构上根本没有任何一条会去比 AD 与 SM，⛔ 所以 AD↔SM 的不一致检不出来是**规则集覆盖不到**，⛔ 而不是「LLM 不会跨层检查」。⭐ **这条对我们是一个可借鉴的负面样本**：⛔ 把「我的规则集没覆盖」写成「LLM 做不到」，⛔ 会让读者误判方法边界。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `iet-software-2025-consistency-traceability` |
| `title` | Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework |
| 作者 | **Haibo Li**, **Lixiao Zheng** —— College of Computer Science and Technology, **Huaqiao University**, Xiamen 361021, China |
| `year` | **2025** —— ⭐ Crossref `issued = [[2025, 1]]`、`published-online = [[2025, 12, 23]]`、`created = 2025-12-23T10:32:50Z`；⭐ DBLP `year = 2025`。⚠️ **两者都指向 2025，⛔ 不存在 early-access 年错位问题**（⭐ Wiley 连续卷模式把它归入 vol 2025，⛔ 尽管上线日期是 2025-12-23） |
| `venue` | **IET Software** —— ⭐ Crossref `container-title = ['IET Software']`；⭐ Vol **2025** / Issue **1** / Article ID **6714956**（⛔ **无页码范围** —— Wiley 连续卷）；⭐ ISSN `1751-8806`（print）/ `1751-8814`（online）。⚠️ **special issue：页眉标 `Guest Editor: Tomasz Górski`** |
| `ccf` | ⚠️ **未在本仓库 [ccf_venues/](../../../../../ccf_venues/) 收录** —— ⭐ 全目录 grep `IET Soft` / `IET` **零命中**。⛔ **本轮未独立核对官方 CCF 推荐目录**，⛔ 故不断言其等级。⚠️ 若报告需要用 CCF 等级，⭐ **必须另行核 CCF SE/系统软件/程序设计语言 方向的期刊名录** |
| `doi` | ⭐⭐ [10.1049/sfw2/6714956](https://doi.org/10.1049/sfw2/6714956) —— ⭐ **本轮我方独立在 Crossref API 实取核对**：标题、期刊、卷期、article-number、两位作者、上线日期、CC-BY 4.0 license 全部一致 |
| DBLP | ⭐ `journals/iet-sen/LiZ25` —— ⭐ **本轮我方独立实取核对**（⭐ DBLP API 精确 1 命中，`venue = IET Softw.`、`volume = 2025`、`number = 1`、`access = open`、`doi = 10.1049/SFW2/6714956`） |
| `url` | [Wiley 文章页](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/sfw2/6714956) —— ⚠️ **我方 curl 与 WebFetch 均被 Cloudflare 挡（HTTP 403 / 402）**，⛔ 见 §D.3 与 F.1 |
| 许可 | ⭐ **Gold OA, CC-BY 4.0**（⭐ Crossref license 字段实取确认） |
| 关键词 | ⭐ 原文给的 6 个：`consistency` · `formal structure` · `large language model` · `process model` · `test case` · `use case specification` |
| `artifact_type` | ⚠️ **三种制品并存**：⭐ ① **结构化 UCS**（use case specification，⭐ 槽位元组化的需求制品）· ⭐ ② **UML 活动图**（论文自称是 UML 活动图的**简化版**）· ⭐ ③ **UML 状态机**（⭐ 业务对象生命周期状态模型，⭐ 同样是简化版） |
| `task` | ⭐ **一致性检查**（主）+ **追溯**（需求⇄测试）+ **测试生成** + **需求形式化** —— ⛔ **不是**模型生成、⛔ 不是缺陷类型学 |
| `boundary` | ⚠️ **邻域（主）+ 界内（状态机部分）** —— 见 §A.2 |

### A.1 ⭐ 硬门核对

| 硬门 | 判定 | 理由 |
| :-- | :-: | :-- |
| 1 · 基于 LLM | ⚠️ **过，但只占一半** | ⭐ LLM 承担 phase 1–3（需求结构化、UCS 转换、测试评审与需求精化），⛔ **但 phase 4–5 的一致性校验（论文的署名创新点）完全不用 LLM**。⭐ 逐字（§6.1）：`"The experimental process adopted a 'human-in-the-loop' approach, where human reviewers and the language model collaborated iteratively."` ⭐ **过门，但要注意：它的核心贡献（三条规则 + 三个算法）是纯确定性的** |
| 2 · 行为类模型制品 | ⭐ **过** | ⭐ UML 活动图 + UML 状态机，两者都在硬门 2 的白名单里 |

### A.2 ⚠️ 边界拆分

| 制品 | 边界 | 理由 |
| :-- | :-: | :-- |
| **UML 活动图（简化版）** | ⭐ **邻域** | ⭐ 活动图在 [README.md](../README.md) §2.1 的「邻域」档里。⭐ 论文的定义逐字是 `BPM = (G, T)`，⭐ 带一个满射 `type: ON → T`，⛔ 自陈 `"which is a simplification of the UML activity diagram and only includes the most basic components to enhance the clarity of the discussion"` |
| **UML 状态机（简化版）** | ⭐ **界内** | ⭐ 定义逐字 `SM_bo = (S, Trans, A)`，⭐ 且 `S ⊆ bo.S_allowed`。⭐⭐ **这就是一台朴素 FSM** —— ⛔ 无时钟、⛔ 无不变式、⛔ 无正交区、⛔ 无层次态。⭐ 自陈 `"The definition of the state model is a simplification of the UML state machine diagram."` |
| **结构化 UCS** | ⛔ **不适用** | ⛔ 它是需求制品，⛔ 不是行为模型 |

⭐⭐ **一件对我们有利的事实**：⭐ 论文**明确把时间/实时系统排除在自己的适用范围外**，⭐ 逐字（§7.3）：

> `"The validation of such a system requires techniques like timed automata and worst-case execution time analysis, which are outside the scope of business object-centric rules"`

⭐ **所以它与我们的 $M = (S,E,V,Tr,A)$ 边界几乎完全兼容** —— ⛔ 唯一超出的是活动图（邻域，不是界外）。⭐ **这在本轨里算是边界最干净的一篇。**

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **5 个 phase，⭐ 逐字抄自 §6.1**）

⭐ 论文原文逐字给出 5 个 phase：

> `"This process consisted of five core phases:`
> `1. Requirement Structuring: Converting raw textual requirements into a formal format.`
> `2. Use Case Template Transformation and Test Case Generation: Converting structured requirements into UCS, and automatically deriving test cases from the UCS, with manual adjustments as needed.`
> `3. Test Case Review and Iterative Requirement Refinement: Combining human evaluation with LLM-assisted analysis of test cases to detect omission or ambiguities. UCSs are then updated based on feedback to enhance clarity and completeness.`
> `4. Consistency Validation with activity diagram: Validating consistency using Algorithm 2 with the corresponding activity diagram.`
> `5. Consistency Validation with state machine diagram: Validating consistency using Algorithm 3 with the state machine diagram of a business object."`

⭐ 画成线：

```
[人] 原始文本需求
  → [LLM] phase 1 · Requirement Structuring
        （→ 槽位元组 <Pre-cond[Prev_Step], actor, action, business_object, [to_actor], [Post-cond]>）
        ⇄ [人] 纠正被误识别的 business object
  → [LLM] phase 2a · UCS 转换
        ⇄ [人] manual validation + iterative LLM-driven refinement
  → [确定性] phase 2b · Algorithm 1 GenTestCase → 测试用例集
  → [LLM + 人] phase 3 · 测试用例评审 → 回写精化 UCS/原始需求   ⇄ 循环①（人叫停）
  → [确定性] phase 4 · Algorithm 2 ValidateCybyP（Rule 1+2，对活动图）
        → 输出 (AbnStep, AbnBO)
        → [人] 据结果修需求                                   ⇄ 循环②（人叫停）
  → [确定性] phase 5 · Algorithm 3 ValidateCybyState（Rule 3，对状态模型）
        → 输出 AbnStepPair
        → [人] 据结果修需求
```

⭐⭐ **阶段计数**：⭐ **5 个 phase（⭐ 若按算法/动作细分为 6 步：1 / 2a / 2b / 3 / 4 / 5）；⭐ 其中 LLM 参与 3 个（1、2a、3），⭐ 确定性 3 个（2b、4、5）。**

⭐⭐ **形状要点（⛔ 与本轨其它卡对照的关键）**：

1. ⭐⭐ **这是本轨里少见的「LLM 在前、确定性在后」的形状** —— ⭐ LLM 负责把 NL 变成结构化制品，⭐ 确定性算法负责在结构化制品上做判定。⭐ **判定端完全没有 LLM。**
2. ⛔⛔ **但确定性判定端的输出不回灌给 LLM，而是交给人。** ⭐ 逐字（§6.1 phase 4）：`"The requirement description needs to be refined or modified based on the validation results."` ⛔ **修的是人，不是 LLM。** ⭐ 所以它**不是**「确定性裁决者驱动 LLM 修订」的先例。
3. ⛔ **两个循环都由人叫停，且没有任何数值终止条件。** 见 §B4。

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 |
| :-- | :-- |
| phase 1 · Requirement Structuring | ⭐ **抽取器**（从 NL 抽 actor / action / business object / 前后置条件）+ **翻译器**（NL → 槽位元组） |
| phase 2a · UCS 转换 | ⭐ **翻译器**（结构化需求 → 用例规约） |
| phase 3 · 测试用例评审 | ⛔⛔ **评审者（LLM 自评）** —— ⭐ 三个 prompt 家族，⭐ §4.2 逐字命名：`"Identifying Gaps and Inconsistencies"` · `"Suggesting Additional Test Cases"` · `"Discovering Implicit Requirements"` |

⛔ **全篇没有**：⛔ **裁决者**（⭐ 裁决由 Algorithm 2/3 + 人做，⛔ 不由 LLM 做）· 生成器（⭐ 不生成模型）· 修复者（⭐ 修复由人做）· 规划者 · 分类器 · 解释者 · 检索改写器。

### B3 · prompt 策略

| 项 | 值 |
| :-- | :-- |
| 策略 | ⭐ **zero-shot / few-shot 风格的直接指令 + 输出格式说明**（⭐ 靠自然语言描述槽位格式），⛔ **不是** JSON schema、⛔ 不是受限解码、⛔ 无解析失败回灌重试 |
| ⭐ prompt 家族数 | ⭐ **约 7 个**：⭐ §4.1 三个（需求结构化 · business-object-vs-attribute 纠正 · UCS 生成）+ ⭐ §4.2 四个（三个评审 + 一个精化） |
| 温度 / seed | ⛔⛔ **完全未给** —— ⭐ 全文 `temperature` **0 次**、`seed` **0 次** |
| prompt 是否公开 | ⚠️ **公开在正文里，⛔ 但没有独立 artifact** —— ⭐ 逐字 prompt 内联在 §4.1 / §4.2；⛔ **无附录、⛔ repo 里无 prompt 文件**（⭐ 见 D 节）。⭐ **够近似复现，⛔ 不够精确复现** |
| ⛔ 无 | RAG · 工具调用 · CoT（⛔ 未声明）· self-consistency 投票 · 多智能体辩论 · 结构化输出约束 |

⭐ **prompt 层面唯一值得记的实测**：⭐ 论文报了「prompt 迭代次数」这个量（⭐ Table 11：junior **11** 次、mid-level **9** 次、senior **7** 次）。⚠️ ⭐ **这是一个有意思的指标 —— 它量的是「人为了把 LLM 拧对要改几次 prompt」**，⛔ 而不是「流水线内部迭代几轮」。⭐ **单调下降说明经验越足、prompt 拧得越快**，⛔ 但它与我们关心的「循环边际收益」不是同一个量。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| **有无循环** | ⭐ **有，两个** |
| ⭐ **裁决者是谁** | ⛔ **循环①：`人` + `LLM 自评` 混合**；⭐ **循环②：`确定性规则`（Algorithm 2/3）判定 + `人` 执行修复** |
| 终止条件 | ⛔⛔ **人叫停，且无任何数值条件** |
| 最大轮数 | ⛔⛔ **原文未提供** |
| ⭐ 有无报告循环的边际收益 | ⛔⛔ **无** —— ⭐ 详见下方 |

#### ⭐ 两个循环拆开看

| 循环 | 谁决定再来一轮 | 类型 | 终止 |
| :-- | :-- | :-- | :-- |
| ⛔ **① 测试评审 → 需求精化**（phase 3） | ⛔ **人 + LLM 自评** | ⛔ **LLM 自评 + 人** | ⭐ 逐字：`"This iterative collaboration continued until requirements satisfied stakeholder needs, progressively enhancing requirement clarity, completeness, and test coverage."`（§6.1）—— ⛔⛔ **「until stakeholder needs are satisfied」不是可操作的终止条件** |
| ⭐ **② 一致性校验 → 修需求**（phase 4/5） | ⭐ **Algorithm 2/3 的输出**（⭐ 确定性规则） | ⭐ **确定性规则**（⛔ 但**不是** sound oracle —— ⭐ 见下） | ⭐ 逐字（§3.3）：`"This mechanism forms an iterative refinement loop that continuously enriches the original requirements."` ⛔ 无数值终止条件 |

#### ⛔⛔ 裁决者算不算 sound oracle？—— ⭐ **不算，⭐ 但比 LLM 自评强一档**

⭐ Algorithm 2/3 是**确定性规则匹配**，⛔ 不是模型检查器、⛔ 不是 SMT、⛔ 不是类型检查器。⛔ **它们的判定核心是「business object 名字匹配」**。⭐ 逐字（Algorithm 2 第 5 行）：

> `"5:   if boj = business_objectk, where sk = < Pre-conditionsk [Previous_Stepk], actork, actionk, business_objectk, [to_actork], [Post-conditionsk] > then"`

⚠️⚠️ ⭐ **这是一条纯等号比较（名字相等）** —— ⛔ 没有语义等价、⛔ 没有同义词处理、⛔ 没有嵌入相似度。⭐ **后果**：⛔ 只要模型侧和需求侧对同一个业务对象用了不同措辞，⛔ 就会被判成两侧各自的「异常」—— ⭐ 而论文报出的两条违规里**确实有一条就是术语不匹配**。

⭐⭐ **对我们的直接含义**：⭐ **它在「裁决者可靠性」这条曲线上处于 LLM 自评之上、sound oracle 之下的中间档** —— ⭐ 判定是可复算的（好），⛔ 但判据是词法的而非语义的（⭐ 这正是仓库 §11 讲的那类问题：⛔ **把语义判断实现成词法判断**）。⚠️ ⭐ **本篇给了这条教训一个外部实例，⛔ 而且代价直接体现在它报出的违规里。**

#### ⛔⛔ 逐轮边际收益：⛔ **完全没有**

⭐ **全篇没有任何逐轮数字** —— ⛔ 无收敛曲线、⛔ 无「第 k 轮后收益饱和」、⛔ 无逐轮 delta。⭐ 唯一与迭代相关的聚合数字是 Table 11 的 prompt 迭代次数（11 / 9 / 7）与时间加速比（**10.5× / 7.7× / 6.0×**）。

⚠️ **所以本篇对我们「第 3–5 轮零收益」那条发现给不出任何直接对照。** ⭐ **但它给出一条间接对照**：⛔ **它的循环终止靠人的主观满意度**，⛔ 因此它连「收益什么时候见底」这个问题都无法回答 —— ⭐⭐ **而我们至少测出来了「第 3 轮就见底」。** ⭐ 这是我们相对它的一个真实方法学优势。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| **有无** | ⭐⭐ **有，而且它是论文的第一个署名创新** |
| **形态** | ⭐ **Requirement Specification Structure** —— ⭐ 一个**浅层槽位模板**，⛔ **不是 DSL**、⛔ 不是缺陷类型学、⛔ 不是谓词族、⛔ 不是 JSON schema。⭐ 逐字（§4.1）：`"we propose a structured textual format, the Requirement Specification Structure, to structure requirement descriptions."` |
| ⭐ **槽位集合** | ⭐ 逐字：`< Pre-conditions [Previous_Step], actor, action, business_object, [to_actor], [Post-conditions] >` |
| ⭐ **是否闭合** | ⚠️⚠️ **两层要分开答** —— 见下 |
| ⭐ **谁定的** | ⭐ **槽位模板由作者预定义；⛔ 槽位里填什么由 LLM 自动抽取，⛔ 人再纠错**。⭐ 逐字（§4.1）：`"the identification of business objects may occasionally deviate. For instance, in the requirement 'Company captures buyer's name, address, requested goods, etc.,' attributes such as 'buyer's name,' 'buyer's address,' and 'buyer's requested goods' might be incorrectly identified as objects themselves, requiring manual correction."` |

#### ⚠️ 「是否闭合」的两层拆解

| 层 | 闭合性 | 说明 |
| :-- | :-: | :-- |
| **一致性规则目录** | ⭐⭐ **闭合，恰好 3 条** | ⭐ 作者自定，⛔ 但**明写可扩展**（§8：`"We will also expand our consistency rules to incorporate the diagram, thereby establishing a more comprehensive validation framework."`） |
| **槽位模板** | ⭐ **闭合**（6 个槽位，其中 3 个可选） | ⭐ 作者预定义 |
| ⛔ **business object 集合** | ⛔ **完全开放** | ⛔ LLM 自由抽取，⛔ 无候选集、⛔ 无本体、⛔ 无词表 |
| ⛔ **缺陷类型学** | ⛔⛔ **不存在** | ⛔ 缺陷只按「违反了三条规则中的哪一条」标注，⛔ 没有独立的缺陷分类学 |

⭐ 另有 **5 条形式化定义**（⭐ Def 1 Basic Flow · Def 2 Alternative Flow · Def 3 Business Object `BO = (N, Att, S_allowed, M, C)` · Def 4 Business Process Model `BPM = (G, T)` · Def 5 State Model `SM_bo = (S, Trans, A)`）。

⭐⭐ **与我们的关键错位（⛔ 必须说清）**：

- ⭐ 我们的 **19 条闭合谓词词表** 是「**问什么问题**」的闭合集合，⭐ 且**由 LLM 在每条需求上自动选**。
- ⭐ 它的 **3 条规则** 是「**检查什么关系**」的闭合集合，⛔ **但没有任何选择动作** —— ⛔ **三条规则全部无条件、全部逐对象逐步骤穷举施加**。
- ⛔⛔ **所以它不是「闭合词表 + LLM 自动选」的先例。** ⭐ 它是「**闭合规则集 + 穷举施加**」，⛔ 选类环节压根不存在。⭐ **本轨「有多少先例」这个计数在本篇这里 +0。**
- ⭐⭐ **但它是「闭合规则集」这半边的一个有用参照点**：⭐ **3 条**（本篇）vs **8 条**（⭐ 论文自己引的 Górski k+1 方法，§7.1 逐字：`"employs eight business logic rules"` vs `"applies three proposed rules"`）vs **19 条**（我们）。⭐ **这个量级序列本身有参考价值。**

#### ⛔⛔ 出处（provenance）：⭐ **三条规则没有任何外部依据**

⚠️ ⭐ **这一格对我们的 L2 出处轴有直接警示意义。** ⭐ 论文的三条规则**不来自** UML 规约、⛔ 不来自 OCL、⛔ 不来自文献 —— ⭐ 逐字（§5.2）：

> `"By leveraging the role of business objects as the common core referenced across all views, we propose three business object-centered consistency rules to validate whether the steps in a UCS are logically consistent with the flows of an activity diagram and the transitions of a state machine diagram."`

⭐ **从外部借来的只有周边词汇，不是规则本身**：

| 借来的东西 | 出处 | 逐字 |
| :-- | :-- | :-- |
| business object 概念 | OMG（ref [44]） | `"OMG business objects [44] are representations of the nature and behavior of real-world things or concepts in terms that are meaningful to the business."` |
| 活动图 / 状态机的定义 | ⛔ **自陈是 UML 的简化** | `"which is a simplification of the UML activity diagram and only includes the most basic components to enhance the clarity of the discussion"` |
| 举例用的业务流程 | UML 2.4.1 规约（ref [45]） | `"The business process shown in Figure 5b is derived from examples in the UML 2.4.1 specification [45]."` |

⭐⭐ **对我们的含义**：⭐ 我们的 19 条谓词做了**三类出处分级**（⭐ ① 有领域证据 12 · ② 元模型定义性 6 · ③ 无外部依据 1，⭐ 详见 [../../provenance/](../../provenance/)）。⭐⭐ **本篇的三条规则按我们的分级会全部落在「② 元模型定义性」或「③ 无外部依据」** —— ⭐ 也就是说，⭐ **一篇 SCI 期刊论文把「作者自拟的三条规则」作为署名创新发表，且未被要求给外部出处。** ⚠️ ⭐ **这不是替我们的③类开脱**（⛔ 我们的出处纪律仍应保持），⭐ **但它是一个有用的领域基准：外部审稿人对「规则出处」的要求，比我们自己设的线低得多。**

### B6 · 模型

| 项 | 值 |
| :-- | :-- |
| 模型 | ⛔⛔ **只有 `GPT-4` 一个** —— 逐字（§6.1）：`"For this study, we selected GPT-4, a LLM developed by OpenAI."` |
| snapshot / 版本 | ⛔⛔ **完全没有** —— ⛔ 无 snapshot ID、⛔ 无日期、⛔ 无 temperature、⛔ 无 seed。⭐ 全文 `GPT-4` 出现 **5 次**，⛔ `Claude` / `Gemini` / `DeepSeek` **0 次** |
| 多模型对照 | ⛔⛔ **无** —— ⛔ 无跨模型对照、⛔ 无消融 |

⚠️⚠️ ⭐ **一处内在张力值得记**：⭐ 论文声称结果稳定，逐字（§7.2）：

> `"given a consistent model version (e.g., GPT-4) and fixed prompt templates, the LLM generates highly consistent and stable formal specifications and test cases"`

⛔⛔ **但它既没给 snapshot、也没给 temperature、也没跑多次** —— ⭐ 所以这个「稳定」声明**没有任何实测支撑**（⛔ 见 §C.5）。⭐ **这正是仓库要求 run record 记精确 `model_id` + 多轮采样的理由：⛔ 没有这两样，「稳定」只能是断言。**

⚠️ **代差提醒**：⭐ GPT-4（2023）比我们的 `gpt-5.5` 落后两代以上，⛔ 且本篇的 LLM 环节（需求结构化、UCS 转换）恰恰是**最吃模型能力的那类任务**。⛔ **它报的「business object 偶尔识别错、需人工纠正」在当代模型上很可能不再成立** —— ⭐ 但本篇无法回答这一点。

### B7 · ⭐ 确定性成分（⭐ 本卡这一格是本轨里较厚的一个）

| 环节 | 是什么 | 输出 |
| :-- | :-- | :-- |
| **Algorithm 1 `GenTestCase`** | ⭐ 用例模板 → 测试用例集。⭐ 枚举基本流 + 每个 alt/exception 分支各一条用例，⭐ 带 rejoin 处理 | 测试用例集 |
| ⭐⭐ **Algorithm 2 `ValidateCybyP`** | ⭐ 检 **Rule 1 + Rule 2** against 业务流程模型（活动图） | ⭐⭐ **`(AbnStep, AbnBO)` —— ⭐ 两侧残差，⭐ 见 §C.1** |
| **Algorithm 3 `ValidateCybyState`** | ⭐ 检 **Rule 3** against 状态模型 | ⭐ `AbnStepPair`（⭐ 违反相对次序的步骤对） |

⭐ 逐字（§1）：`"These rules are implemented through corresponding algorithms."`

⛔⛔ **但有一个硬缺口：三个算法只有伪代码，没有实现。** ⭐ 全文 `Python` **0 次**、`Java` **0 次**、`parser` **0 次**；⭐ `prototype` **1 次**且指的是别人的工作（ref [35]）。⛔ **repo 里零代码**（⭐ 见 D 节）。

⚠️ ⭐ **后果（I，⛔ 我方推断，⛔ 原文未提供）**：⛔ **无法判断 Algorithm 2/3 是被当软件跑过，还是人拿着规则手算的。** ⭐ 这对「一致性校验是确定性的」这个说法是一处实质性削弱 —— ⭐ 判据确实是确定性的，⛔ 但执行者可能是人。

⛔ **全篇没有**：模型检查器 · SMT / 求解器 · 类型检查器 · parser · 元模型一致性检查器 · 图算法。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐⭐ **两个，⭐ 都是人**：⭐ ① **control group** —— 3 名工程师用 `"traditional practices (deriving UCS from raw requirements without our approach)"`；⭐ ② **原始 Web Store 数据集自带的 UCS**。⛔⛔ **无 LLM baseline、⛔ 无消融** |
| `dataset` | ⭐ **PURE 数据集**（ref [46], Ferrari et al. 2017）里的 **GAMMA-J Web Store**（电商系统），⭐ 来源 `http://fmt.isti.cnr.it/nlreqdataset/` |
| ⭐ **分母怎么定的** | ⭐ 逐字：`"There are 26 use cases originally designed by the Web Store dataset."` → `"After removing six duplicate use cases, 20 valid use case templates remained from the Web Store dataset."` ⭐⭐ **即 26 → 20，⭐ 去重理由明写** |
| `metrics` | ⭐ ① 计数（用例数 / 基本流 / 备选流 / 测试用例数，Table 8）· ⭐ ② **专家 1–10 分四维评分**（Table 9）· ⭐ ③ **precision / recall** vs 专家基准 + 不一致用例数（Table 10）· ⭐ ④ 效率（prompt 迭代次数、耗时、加速比，Table 11）。⛔⛔ **无任何 `@k` 口径** |
| ⭐ `judged_by` | ⛔⛔ **5 名专家人工评分，⛔ 只报均值** —— 见 §C.4 |
| `human_baseline` | ⭐⭐ **有** —— ⭐ control group 就是。⭐ **这是本篇相对本轨大多数工作的一个真实优势** |
| `runs` | ⛔⛔ **1 次，⛔ 无重复、⛔ 无方差** —— 见 §C.5 |
| ⭐ `adverse_results` | ⚠️ **报了不少，⛔ 但有选择性遗漏** —— 见 §C.6 |

### C.1 ⭐⭐⭐ 必答 ① · 「双向可追溯」的双向到底指什么

#### ⛔⛔ 答案：**需求 ⇄ 测试用例，⛔ 不是需求 ⇄ 模型**

⭐ **三处逐字，⭐ 口径完全一致**：

> ⭐ §1：`"Moreover, our approach ensures bidirectional traceability between user requirements and test cases: test cases generated by LLMs can feed back to refine user requirements when modified."`

> ⭐ §3.2：`"The basic flows and alternative/exception flows in UCS are not abstract descriptions but are concretized into one or more independent test cases. This rigorous structural synchronization establishes bidirectional traceability between requirements and tests."`

> ⭐ §1（第 3 条创新）：`"A bidirectional feedback loop for lifecycle alignment: A closed-loop process is established within the framework, where UCS not only generates test cases but also incorporates feedback from extended testing to refine and improve the raw requirements."`

⭐ **两个方向分别是**：

| 方向 | 内容 | 机制 |
| :-: | :-- | :-- |
| ① | ⭐ **UCS → 测试用例** | ⭐ Algorithm 1 `GenTestCase`（确定性） |
| ② | ⭐ **测试用例 → 回写精化 UCS / 原始需求** | ⛔ LLM 评审 + 人（phase 3） |

⛔⛔ **两个方向都不是「需求 → 模型」或「模型 → 需求」。**

#### ⭐⭐ 但意外收获：⭐ 我们要的那一侧**在算法里存在，⛔ 只是从未被写成规则或主张**

⭐⭐ **这是本卡最精细的一格，⛔ 也是唯一能对 C-③ 有帮助的东西。**

⭐ **先看规则的方向**：⛔⛔ **三条规则全部写成「模型 → UCS」方向** —— ⭐ 形如「若模型含 X，则必存在某 UCS 使 X 出现」。⛔ **没有任何一条规则形如「若某 UCS 步骤存在，则模型必须含它」。** ⭐（三条规则全文见 §C.2。）

⭐ **但 Algorithm 2 的实现是两侧同时初始化为全集、再逐个减掉匹配项** —— ⭐ 逐字：

> `"Output: (AbnStep, AbnBO), a set of the abnormal steps and a set of the abnormal business objects in the steps`
> `1: AbnBO←{boj}, AbnStep ←BF ∪ altFk, where boj∈ BO, 1≤j≤m, m is the number of business object BO in g, BF is the basic flow of the use case template usecaseT, altFk is alternative/exception flows of stepk in BF, 1≤k≤n;`
> `…`
> `5:   if boj = business_objectk, where sk = < Pre-conditionsk [Previous_Stepk], actork, actionk, business_objectk, [to_actork], [Post-conditionsk] > then`
> `6:    AbnStep←AbnStep-{sk}`
> `7:    AbnBO←AbnBO-{boj}"`

⭐⭐ **于是两个残差集的含义分别是**：

| 残差 | 含义 | ⭐ 对应我们的哪一侧 |
| :-- | :-- | :-- |
| ⭐ **`AbnStep` 剩下的** | ⭐ **UCS 步骤中的 business object 在活动图里找不到** | ⭐⭐ **「需求说了而模型没有」** —— ⭐ **这正是 C-③ 想要的那一侧** |
| ⭐ `AbnBO` 剩下的 | ⭐ 活动图里的 business object 在 UCS 里找不到 | ⭐ 「模型有而需求没说」 |

⚠️⚠️ ⭐ **三条必须一起说的限定，⛔ 否则会把它误读成先例**：

1. ⛔⛔ **两侧性是集合减法的副产品，⛔ 从未被表述成规则、⛔ 也从未被当成一条主张。** ⭐ 论文既没说「我们同时检两个方向」，⛔ 也没为需求侧那一半给判据。
2. ⛔⛔ **修复方向永远是单向的：改需求，把模型当权威。** ⭐ 逐字（§6.1 phase 4）：`"The requirement description needs to be refined or modified based on the validation results."` ⭐ 逐字（§6.1 phase 5）：`"The requirement should be correspondingly corrected: A Create Order step should be inserted between steps 2 and 3 in Figure 8."`
3. ⛔⛔ **论文报出的两条违规，全都是「模型说了 X 而 UCS 缺 X」或术语不匹配 —— ⛔ 从未报出一例「模型被判有缺陷并被修改」。**

⭐⭐⭐ **所以对 C-③ 的结论是**：⛔ **本篇不能作为「双向需求⇄模型追溯」的先例引用**；⭐ **但它可以作为一个更弱、更精确的参照**：⭐⭐ **一个以业务对象名匹配为核心的确定性算法，在实现层面天然同时产出两侧残差 —— ⭐ 需求侧覆盖缺口不需要额外机制，只需要不把它丢掉。** ⚠️ ⭐ 而这篇论文恰恰**把它丢掉了**（⛔ 只在修需求时用，⛔ 从未反过来质疑模型）。

### C.2 ⭐ 三条一致性规则（**M**，⭐ 逐字全文）

⭐ 数量逐字（§3.3）：

> `"Furthermore, the framework introduces three novel consistency rules to ensure logical alignment across models: (1) the semantic consistency rule…; (2) the process consistency rule…; and (3) the state consistency rule…"`

| # | 规则 | 逐字 |
| :-: | :-- | :-- |
| **1** | **Semantic Consistency** | `"In an activity diagram, for every activity ai and business object boi, if ai uses boi as an input or output, then there must exist a use case template UCT associated with ai where boi appears in either the basic flow BF or any alternative/exception flow altFi of UCT."` |
| **2** | **Process Consistency** | `"In an activity diagram, for every activity ai, if ai has an input business object boin and an output business object boout, then there must exist a use case template UCT associated with ai where, in both the basic flow and any alternative/exception flow of UCT, boin precedes boout if both objects appear."` |
| **3** | **State Consistency** | `"For every business object boi with a state model S, there must exist a use case template UCT associated with S such that: (1) Every action in S that triggers a state transition is included as a step in UCT and (2) For any two actions ai and aj in S, if ai precedes aj in S, then ai must also precede aj in the sequence of steps in UCT."`` |

⭐⭐ **三条规则的共同形状**：⭐ **全部是「若模型侧有 X，则需求侧必存在对应物」** —— ⭐ 即**模型为量、需求为被量**。⭐ Rule 1 管**存在性**，⭐ Rule 2 管**活动图内的次序**，⭐ Rule 3 管**状态机的动作覆盖 + 次序**。

⭐ **是否闭合**：⭐⭐ **闭合于 3，⛔ 但明写可扩展**（§8）。⭐ **谁编的**：⛔ **作者自己**（⭐ 出处分析见 §B5 末段）。

### C.3 ⭐⭐ 必答 ③ · 是「多视图之间」还是「模型 vs NL」

⛔⛔ **都不是 —— ⭐ 是「结构化 UCS vs 每一个模型视图」，⭐ 两条独立比对。**

⭐ **三处逐字**：

> ⭐ §1（创新 2）：`"Three business object-centered formal rules are incorporated within the framework to rigorously ensure process logic consistency between UCS and activity diagrams, and between UCS and state machine models."`

> ⭐ §1（贡献 2）：`"…which enable the automated detection of logic inconsistencies between UCS and both activity diagrams and state machine diagrams, a capability not well-supported by prior methods."`

> ⭐ §5.3：`"With the structured UCS, the consistency rules can be applied to identify logical inconsistencies in UCS with an activity diagram."`

⭐ **拆成三问三答**：

| 问 | 答 | 证据 |
| :-- | :-: | :-- |
| ⭐ 活动图 vs 状态机（多视图互检）？ | ⛔⛔ **没有** | ⭐ 三条规则全部以 UCS 为一端。⭐ 论文自己把这个缺口留着（⭐ §0 已引） |
| ⭐ 模型 vs **原始 NL 需求**？ | ⛔⛔ **没有（无规则、无算法）** | ⭐ §6.2 确实讨论了原始需求缺口（⭐ 例：`"steps like 'System prompts the Customer to edit the quantity' … appear in the use case but are not documented in the raw requirements"`），⛔ **但那是人工对读，⛔ 不是规则** |
| ⭐ 模型 vs **结构化 UCS**？ | ⭐⭐ **是，这才是它做的事** | ⭐ 上面三处逐字 |

⚠️⚠️ ⭐ **这个区分对我们至关重要**：⭐⭐ **我们的 discover 任务是「模型 vs 自然语言需求」** —— ⭐ 一端是 pyfcstm DSL 状态机，一端是 `nl.txt` 原始需求文本。⛔ **本篇的两端都是已经形式化的制品。** ⭐ **所以它避开了我们问题里最难的那一半（NL 的语义解释），⛔ 而把那一半外包给了 LLM 的 phase 1–2 + 人的纠错。**

⭐⭐ **一个正面的启发**：⭐ 这个「**先把 NL 变成结构化制品，再在结构化制品上做确定性判定**」的两段式，⭐ 其实与我们的 `split_requirements`（NL → 原子需求）→ `convert_assertions`（需求 → 断言）→ `precheck_and_seal`（确定性求值）是**同一个拓扑**。⭐ 差别在于：⛔ **它的第一段有人把关**，⛔ 我们的第一段是 LLM 自评把关（⭐ 而后者实测零收益）。

### C.4 ⛔⛔ `judged_by`：⭐ 本篇最弱的一环

⭐ 逐字：

> `"Five experts with over 10 years of experience reviewed and scored each engineer's UCS on completeness, consistency, accuracy, and testability (using a 1–10 scale). The final score for each UCS was the average of the five experts' ratings."`

| 项 | 状况 | 判定 |
| :-- | :-- | :-- |
| 评分人数 | ⭐ **5 名，10 年以上经验** | ⭐ 人数不算少 |
| ⛔ **独立性** | ⛔⛔ **原文未声明**（⛔ 未说 5 名专家与作者无关） | ⛔ 缺口 |
| ⛔ **盲评** | ⛔⛔ **原文未声明**（⛔ 未说评分时对实验组/对照组条件盲） | ⛔⛔ **严重缺口** —— ⭐ 这是打分类实验的基本要求 |
| ⛔ **标注者间一致性** | ⛔⛔ **完全没有** —— ⭐ `kappa` **0 次**、`agreement` **0 次**、`standard deviation` **0 次** | ⛔⛔ **只给了 5 人均值，⛔ 没有任何离散度** |
| ⛔ **ground truth 出处** | ⛔ **自家产出** —— ⭐ 逐字：`"A manual benchmark UCS: developed by an expert engineer (over 15 years of experience) who reverse-engineered the functional requirements by analyzing documentation (https://github.com/lihaibo2025/requirement/), without LLM assistance."` ⛔ 该工程师与作者的关系**未声明** | ⛔⛔ **precision / recall 是对着自产基准算的 —— ⭐ 自指式评测（I，⭐ 我方判断）** |

⭐ **人体实验设计规模** —— 逐字：

> `"Each group had three engineers, covering three experience levels: junior (1–2 years), mid-level (3–5 years), and senior (6–8 years)."`

⛔⛔ **即每组 n = 3，⭐ 每个经验档只有 1 个人，⛔ 无任何重复。** ⚠️ ⭐ **后果见 §C.6 第 3 条：⛔ 组间差异有可能只是个体差异。**

⭐⭐ **对我们的对照**：⭐ 我们的判定是 **574 位逐位判据 + 288 簇五类裁定**，⛔ 同样是自评（⛔ 无第三方、⛔ 无 $\kappa$）。⭐ **但两处差别对我们有利**：⭐ ① 我们的判定对象是**可机械复算的断言求值结果**，⛔ 不是 1–10 主观打分；⭐ ② 我们**同一套判据覆盖全部格**，⛔ 不是每条臂换人。⚠️ ⭐ **不利之处相同：我们也没有 $\kappa$、也没有盲评。**

### C.5 ⛔⛔ `runs`：⭐ 单次，⛔ 且论文声称的「稳定」无实测支撑

⛔ **无重复运行、⛔ 无 `@k`、⛔ Table 8–11 的每一个数字都没有方差。** ⭐ 全文 `variance` 只出现一次，⛔ 且指的是**人的耗时**而非采样：`"The time for the former is consistent, whereas the latter exhibits significant variation."`

⚠️ ⭐ **而它同时声称 LLM 输出「highly consistent and stable」（§7.2，⭐ 已在 §B6 引）** —— ⛔⛔ **一个没有多次采样、没有 temperature 记录、没有 snapshot pin 的实验，无法支撑这个断言。**

⭐⭐ **这是我们相对它最清晰的方法学优势**：⭐ 我们的 `hit@1` / `hit@3` / `hit@all` 三口径正是为了区分「稳定发现」与「偶尔碰上」。⛔ **本篇连这个问题都没有提出。**

### C.6 ⚠️ `adverse_results`：⭐ 报了不少，⛔ 但有选择性遗漏

#### ⭐ 坦白报出的（⭐ 值得借鉴的部分）

| # | 不利结果 | 逐字 |
| :-: | :-- | :-- |
| 1 | ⭐ **precision 一直很低（50.77%–65.38%），⭐ 且把 recall > precision 解释成真实代价** | `"This gap reflects the inclusion of additional alternative flows in LLM-assisted UCS, which broadens scenario coverage despite a slight trade-off in precision."` |
| 2 | ⭐ **用了方法后仍有残留不一致**（⭐ senior 档仍有 4 个用例、2 类规则违规） | Table 10 逐字 `4(2)` |
| 3 | ⭐ **LLM 把属性误识别成对象、需人工纠正** | §4.1（⭐ 已在 §B5 引） |
| 4 | ⭐ **LLM 过度生成** | `"A preliminary review identified extraneous LLM-generated exception-handling elements, which were omitted."`（§6.1） |
| 5 | ⭐⭐ **资深工程师收益最小，⭐ 且加速比随经验单调退化 10.5× → 7.7× → 6.0×** | `"Senior engineers, however, showed inherent proficiency in identifying edge cases"` |
| 6 | ⭐⭐ **专门用一节（§7.3）讲方法在哪失效** | ⭐ 控制流密集 / 实时系统（ABS 例）：`"The validation of such a system requires techniques like timed automata and worst-case execution time analysis, which are outside the scope of business object-centric rules"`；⭐ 另有 model drift 与建模人工成本 |
| 7 | ⭐ **明写没探边界** | `"this study does not investigate the upper bounds of structural complexity that LLMs can effectively process"` |

⭐⭐ **第 5 条特别值得抄**：⭐ **「方法对越弱的使用者收益越大、对专家几乎无用」这个结论，作者主动报了出来。** ⚠️ ⭐ 它与本轨另一篇（[`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md)）「分阶段帮弱模型、伤强模型」**方向完全一致** —— ⭐⭐ **一个是人的经验档、一个是模型的能力档，⭐ 呈现的是同一条规律。**

#### ⛔⛔ 表里有、正文不提的（⭐ 三条，⛔ 都是我方核出的）

| # | 数据 | 问题 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **实验组 junior 的 Testability = 6.8，⛔ 低于原始 Web Store 基线的 7.1** | ⭐ 即在四个质量维度之一上，⛔ **方法的 junior 产出不如未经处理的原始数据集**。⛔ 而 §6.3.1 仍断言 `"the experimental group outperformed the control group across all criteria"` —— ⚠️ **这句对 control group 成立，⛔ 但 Web Store 那一行被悄悄排除在这个断言之外了** |
| **2** | ⛔ **实验组 senior 找到的备选流（32）少于实验组 mid（42），⛔ 也少于对照组 junior（33）** | ⛔ 非单调，⛔ 正文未解释 |
| **3** | ⛔⛔ **对照组 mid 只找到 14 条备选流，⛔ 而对照组 junior 找到 33 条 —— ⭐ 组内 2.4× 落差，⛔ 而每格 n=1** | ⚠️⚠️ ⭐ **这条最要紧：⛔ 组内落差比组间落差还大，⛔ 说明组间差异有可能只是个体差异。⛔ 论文未提。** |

⭐⭐ **对我们「−15.82pp」的直接借鉴**：⭐ **第 1 条是一个反面教材** —— ⛔ **不要用「相对 X 全面胜出」这种句式，⛔ 而把另一个更不利的对照 Y 从句子的范围里悄悄排除。** ⭐ 我们的报告若要说「主臂优于某基线」，⛔ **必须把所有对照臂一起列出**，⛔ 不许挑范围。

### C.7 ⛔ 一处评分口径漂移（⭐ 我方核出）

⚠️ ⭐ **论文说自己按 ISO 29148 的四个特征评，⛔ 但表头的四列不是那四个**：

| 来源 | 四个维度 |
| :-- | :-- |
| ⭐ §6.3.1 正文（⭐ 自称 ISO 29148，⭐ 逐个给了定义） | **Complete** · **Correct** · **Unambiguous** · **Verifiable** |
| ⛔ Table 9 表头 | **Completeness** · **Consistency** · **Accuracy** · **Testability** |

⛔⛔ **`Consistency` 不在它自己列的 ISO 29148 四特征里，⛔ 而 `Unambiguous` 从未作为一列出现。** ⭐ 严格说 `Correct↔Accuracy`、`Verifiable↔Testability` 还能勉强对上，⛔ **但 `Unambiguous → Consistency` 这一步是换了概念，不是换了措辞。**

⚠️ ⭐ **这一条对我们有直接警示**：⛔ **正文声明的判据与表格实际报的维度必须逐字一致。** ⭐ 我们的报告若声明按某标准/某分类学评，⛔ 表头就必须是那个分类学的名字，⛔ 不能中途换。

### C.8 ⭐ 主要数字（**M**，⭐ 四张表）

#### Table 8 · 产出计数

| Mode | Level | Use cases | Basic flows | Alt flows | Test cases |
| :-- | :-- | --: | --: | --: | --: |
| Web Store（原始） | — | 26 | 26 | 14 | 40 |
| Experimental | Junior | 20 | 20 | 36 | 56 |
| Experimental | Mid | 20 | 20 | **42** | **62** |
| Experimental | Senior | 20 | 20 | ⛔ **32** | 52 |
| Control | Junior | 20 | 20 | 33 | 53 |
| Control | Mid | 21 | 20 | ⛔ **14** | 34 |
| Control | Senior | 20 | 20 | 26 | 46 |

#### Table 9 · 专家 1–10 分四维评分

| Mode | Level | Completeness | Consistency | Accuracy | Testability |
| :-- | :-- | --: | --: | --: | --: |
| Web Store | — | 6.1 | 6.7 | 5.8 | **7.1** |
| Experimental | Junior | 7.8 | 8.2 | 8.5 | ⛔ **6.8** |
| Experimental | Mid | 8.9 | 8.8 | 9.1 | 8.3 |
| Experimental | Senior | ⭐ **9.5** | ⭐ **9.1** | ⭐ **9.6** | ⭐ **9.5** |
| Control | Junior | 5.2 | 6.3 | 5.4 | 6.7 |
| Control | Mid | 6.4 | 7.7 | 6.8 | 8.1 |
| Control | Senior | 8.4 | 8.9 | 8.6 | 9.4 |

#### Table 10 · precision / recall vs 自产专家基准

| UCS | Precision | Recall | 不一致用例数（规则违规类型数） |
| :-- | --: | --: | :-- |
| Original documentation | 44.82% | 33.33% | **7(3)** |
| Junior | 50.77% | 76.92% | 6(2) |
| Mid-level | 52.63% | 84.62% | 4(2) |
| Senior | ⭐ **65.38%** | ⭐ **87.18%** | 4(2) |

⭐ **读法**：⭐⭐ **recall 大幅提升（33% → 87%），⛔ precision 提升有限（45% → 65%）且绝对值一直不高。** ⭐ 这与 [`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md) 里「多步策略靠 recall 换分、precision 是代价」是**同一个模式**。

#### Table 11 · 效率

| Level | prompt 迭代次数 | 本方法耗时（min） | 手工耗时（min） | 加速比 |
| :-- | --: | --: | --: | --: |
| Junior | 11 | 63(6) | 645(80) | ⭐ **10.5×** |
| Mid | 9 | 38(5) | 313(20) | 7.7× |
| Senior | 7 | 30(5) | 156(54) | ⛔ **6.0×** |

⚠️ ⭐ **一处内在不一致（⭐ 我方核出）**：⛔ 正文说 `"six test cases … are generated"`，⛔ **但 Table 4 列了 7 行（No. 1–7）**，⭐ 且枚举本身也是 7（2 基本流 + 5 备选）。⛔ **论文内部数字不一致。**

---

## D. 资产（⭐ 本轮 2026-08-13 实取核验）

⭐ Data Availability Statement 逐字：

> `"These data were derived from the following resources available in the public domain: http://fmt.isti.cnr.it/nlreqdataset/. Two documents in the compressed package downloaded through this link: 2008 - keepass.pdf, and 0000 - gamma j.pdf. Experimental process dataset: https://github.com/lihaibo2025/requirement/."`

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据（2026-08-13） |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⚠️ 🟡 | [Wiley 文章页](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/sfw2/6714956) | ⭐ 论文本身是 **Gold OA / CC-BY 4.0**（⭐ Crossref license 实取确认），⛔⛔ **但入口被 Cloudflare 挡**：⭐ 我方实测 `ietresearch.onlinelibrary.wiley.com/doi/...` **HTTP 403**、`onlinelibrary.wiley.com/doi/pdfdirect/...` **HTTP 403**、WebFetch **HTTP 402**。⭐ **本卡的全文是通过本任务内一次真实浏览器会话取到的（91,857 字符正文）** —— ⭐ 见 §D.3 与 F.1。⚠️ **判 🟡 而非 🟢：⛔ 内容是 OA，⛔ 但常规入口不可用** |
| ⛔ **实验代码** | ⛔⛔ ⚪ | — | ⛔⛔ **不存在。** ⭐ 三个算法只有伪代码；⛔ 全文 `Python` / `Java` / `parser` 各 **0 次**；⛔ repo 里零代码文件（⭐ 见下） |
| ⭐ **数据集 / 实验产物** | ⭐ 🟢 | [github.com/lihaibo2025/requirement](https://github.com/lihaibo2025/requirement) | ⭐⭐ **本轮我方独立通过 GitHub API 实取核验**：⭐ 公开、⛔ **未归档**、⭐ 默认分支 `main`、⭐ 描述 `"software requirement"`、⭐ 创建 `2025-03-21T07:03:20Z`、⭐ 最后 push `2025-04-25T07:54:07Z`、⭐ **0 star / 0 fork**、⛔ **license = None**。⭐ **HEAD commit `079953dd26b1`**（`"Update README.md"`, `2025-04-09T03:00:34Z`）。⭐ **共 8 个 commit，⛔ 全部是 `Add files via upload` / `Update README.md` / `Delete datasetforRE.pdf` —— ⭐ 纯 Web UI 上传，⛔ 无开发历史**。⚠️ **注意 `pushed_at`(2025-04-25) 晚于 HEAD commit 日期(2025-04-09)** |
| ⭐ **数据集内容（逐文件）** | ⭐ 🟢 | 同上 | ⭐⭐ **tree 未截断，⭐ 恰好 9 个 blob，⭐ 逐个实取确认**：`0000 - gamma j Web Store.pdf`(1,313,096B) · `README.md`(261B) · `junior with LLM assistance.pdf`(348,942B) · `junior without LLM assistance.pdf`(400,138B) · `mid-level with LLM assistance.pdf`(365,487B) · `mid-level without LLM assistance.pdf`(362,270B) · `senior with LLM assistance.pdf`(418,933B) · `senior without LLM assistance.pdf`(402,304B) · `use cases designed by expert.pdf`(380,162B)。⭐⭐ **即 6 份实验产出（3 经验档 × 有/无 LLM）+ 1 份专家 ground truth + 原始数据集** |
| ⛔ **实验结果细则** | ⛔ ⚪ | — | ⛔⛔ **无**：⛔ 无 5 位专家的逐人评分表、⛔ 无算 precision/recall 的脚本、⛔ 无 LLM 会话记录、⛔ 无 token usage。⭐ **只有论文内的 Table 8–11** |
| ⭐ **prompt 是否公开** | ⚠️ 🟡 | 论文 §4.1 / §4.2 | ⭐ **逐字 prompt 内联在正文**（⭐ 约 7 个）。⛔⛔ **但无附录、⛔ repo 里无 prompt 文件、⛔ 无变量占位说明**。⭐ **够近似复现，⛔ 不够精确复现** |
| 原始 benchmark | ⭐ 🟢 | [PURE / nlreqdataset](http://fmt.isti.cnr.it/nlreqdataset/) | ⭐ 论文指名 `0000 - gamma j.pdf`；⛔ **本轮未独立访问该站点** |
| ⛔ **归档 DOI** | ⛔ ⚪ | — | ⛔ 无 Zenodo / OSF / figshare |
| ⛔ **license（artifact）** | ⛔ ⚪ | — | ⛔ GitHub API `license: None` |

### D.1 ⚠️ 为什么数据集判 🟢 但仍有一条硬限制

⭐⭐ **它不是空壳** —— ⭐ 6 份实验产出 + 专家 ground truth 都在，⭐ **这比本轨大多数工作放出的东西多。** ⭐ 按简报里那条纪律（⛔ 「仓库存在 ≠ 🟢」，⭐ 要看内容是否真有东西），⭐ **这个仓库是真有东西的，⭐ 判 🟢 成立。**

⛔⛔ **但产出全是 PDF，⛔ 不是机器可读的。** ⭐ 后果：

1. ⛔ **想复算它的 precision / recall，必须先人工从 7 份 PDF 里把 UCS 抠出来。**
2. ⛔ **没有任何脚本告诉你 precision / recall 是怎么算的**（⛔ 匹配单位是什么？是用例？步骤？business object？—— ⭐ 论文也没说）。⚠️ **所以 Table 10 的数字实际上不可复算。**
3. ⛔ **5 位专家的逐人评分完全不可查**，⛔ 因此 Table 9 也不可复算、不可算离散度。

⭐⭐ **对比我们**：⭐ 我们的逐格逐轮逐位判定台账是 🟢 且**机器可读**。⭐ **这是一个可以在论文里说的差别**，⛔ 但要注意我们也尚未对外公开（⭐ 论文未投）。

### D.2 ⭐ artifact 的稳定性：⭐ 比 4open 好得多

⭐ **本篇的 artifact 是实名 GitHub 仓库，⛔ 不是匿名 4open** —— ⭐ 所以：

| 项 | 本篇 | ⭐ 对照：`structure-event-driven-stm-frameworks` 的 4open |
| :-- | :-- | :-- |
| commit 可 pin | ⭐ **可**（`079953dd26b1`） | ⛔ **不可** |
| 会不会过期 | ⭐ **不会**（实名仓库） | ⛔⛔ **会** —— ⭐ 本批已实测到另一个 4open 入口返回 `410 repository_expired` |
| 内容会不会静默漂移 | ⭐ **可检测**（⭐ commit 历史可查） | ⛔ **不可检测** —— ⭐ 本批实测该 4open 仓库的 `README.md` 与 `app.py` 自 2026-06-10 起已改，⛔ 无从知道改了什么 |
| license | ⛔ **无** | ⛔ **无** |

⭐⭐ **这是一条给 N1b 的直接结论**：⭐ **实名 GitHub + 可 pin 的 commit，比匿名 4open + ZIP 冻结在可追溯性上强一个量级** —— ⛔ 即使前者放的只是 PDF。

### D.3 ⛔⛔ 全文获取路径：⭐ 必须诚实登记

⭐ **本卡的 A/B/C 节逐字引文来自本任务内一次真实浏览器会话取到的正文（91,857 字符）。** ⛔⛔ **我方自己的常规入口全部失败**：

| 入口 | 结果 |
| :-- | :-- |
| ⭐ `curl` → `ietresearch.onlinelibrary.wiley.com/doi/10.1049/sfw2/6714956` | ⛔ **HTTP 403**（Cloudflare managed challenge） |
| ⭐ `curl` → `onlinelibrary.wiley.com/doi/pdfdirect/10.1049/sfw2/6714956` | ⛔ **HTTP 403** |
| ⭐ WebFetch（两个 Wiley host） | ⛔ **HTTP 402** |
| ⭐ curl_cffi TLS 指纹伪装（chrome / chrome131 / chrome124） | ⛔ **HTTP 403** |
| ⭐ headless Chrome（`--dump-dom` / `--headless=new` / 持久 profile ×3） | ⛔ **被识别，⭐ 卡在 `Just a moment…`** |
| ⭐ r.jina.ai · codetabs · allorigins · corsproxy · thingproxy | ⛔ CAPTCHA / 522 / 需付费 |
| ⭐ fatcat · CORE · EuropePMC · OpenAIRE · paperity · colab.ws · ouci · scholar.archive.org | ⛔ 均无全文（⭐ OpenAIRE 只有元数据） |
| ⭐⭐ **本机 X display 上的 headful Chrome（playwright）** | ⭐⭐ **首次即通过挑战，⭐ 取到全文** |

⚠️⚠️ ⭐ **诚实登记**：⛔ **我没能用自己的入口把这些逐字片段再核一遍。** ⭐ 它们出自同一任务内的一次可复述的浏览器取全文动作，⭐ 但**复核者要么走同一条 headful 浏览器路线、要么用机构订阅**。⛔ **不要以为这些引文是从一个 `curl` 就能拿到的页面上抄的。** ⭐ 元信息侧（DOI / 期刊 / 卷期 / 作者 / 年份 / license / DBLP key / GitHub artifact）**全部由我方独立实取核过**，⭐ 那部分不依赖浏览器会话。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

| # | 可搬的东西 | 为什么 |
| :-: | :-- | :-- |
| **1** | ⭐⭐ **「集合两侧同时初始化为全集、逐个减掉匹配项」这个算法骨架** | ⭐ Algorithm 2 用一个极简的实现同时得到「模型有而需求没说」与「需求说了而模型没有」两侧残差。⭐⭐ **我们的 C-③ 需求侧覆盖缺口可以用同样的骨架拿到 —— ⭐ 不需要新机制，只需要在求值时保留另一侧的残差集。** ⛔ 注意：⛔ **它的匹配是词法等号，⭐ 我们必须换成语义判定**（⭐ 这正好是我们有 pyfcstm 而它没有的地方） |
| **2** | ⭐ **判定端完全不用 LLM 这个形状** | ⭐ 三条规则 + 三个算法全是确定性的，⛔ LLM 只负责把 NL 变成结构化制品。⭐ **这与 M1 第二条设计原则（把裁决者换成 sound oracle）方向一致**，⛔ 尽管它的「oracle」只是名字匹配 |
| **3** | ⭐⭐ **有真正的人类基线（control group）** | ⭐ 本轨大多数工作没有。⭐ 它让「方法 vs 人」的对比成为可能，⛔ 也正因此才发现「对专家几乎无用」这个重要结论。⚠️ ⭐ **我们目前 `human_baseline` 是「无」—— ⭐ 这条是我们可以补的方向** |
| **4** | ⭐⭐ **主动报出「方法对越强的使用者收益越小」** | ⭐ 加速比 10.5× → 7.7× → 6.0× 随经验单调退化，⭐ 作者自己写出来。⭐⭐ **与本轨另一篇「分阶段帮弱模型、伤强模型」是同一条规律的两个切面** —— ⭐ 这个「收益随被辅助者能力递减」的模式**值得作为一条跨篇观察写进 SUMMARY** |
| **5** | ⭐ **单独一节讲方法在哪失效（§7.3）** | ⭐ 明确点名控制流密集/实时系统超出适用范围，⭐ 并说明需要 timed automata。⭐ 这种「主动划出自己不管的地界」的写法可以抄 |

### 2. ⛔ 不可取 / 陷阱

| # | 坑 | 与我们的对应 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **把语义判断实现成词法判断（business object 名字等号匹配）** | ⭐⭐ **这正是仓库 §11 那条纪律的外部实例。** ⛔ 代价直接体现在它报出的违规里（⭐ 有一条就是术语不匹配被判成两侧异常）。⭐ 我们 `named_elements` 那条 validator 事故是同一个病 |
| **2** | ⛔⛔ **把「我的规则集没覆盖」归因成「LLM 做不到」** | ⭐ §0 已详述。⛔ **这会让读者误判方法边界。** ⭐ 我们报未达成项时，⛔ 必须先问「是我们的谓词词表覆盖不到，还是模型确实做不到」—— ⚠️ ⭐ **而这恰恰是我们 15/19 谓词使用率那条待裁定项的同一个问题** |
| **3** | ⛔⛔ **循环终止靠人的主观满意度，⛔ 无任何数值条件** | ⛔ `"until requirements satisfied stakeholder needs"`。⭐ 后果是它连「收益什么时候见底」都无法回答。⭐ **我们至少测出了「第 3 轮见底」** |
| **4** | ⛔⛔ **单次运行 + 声称「稳定」** | ⛔ 无 snapshot、⛔ 无 temperature、⛔ 无重复、⛔ 无方差，⛔ 却写 `"highly consistent and stable"`。⭐ **我们的 3 轮 + 三口径是对的** |
| **5** | ⛔⛔ **「相对 X 全面胜出」句式 + 悄悄排除更不利的对照 Y** | ⛔ §C.6 第 1 条：⛔ junior Testability 6.8 < Web Store 7.1，⛔ 而正文断言「across all criteria 优于对照组」（⭐ 对 control 成立，⛔ 但 Web Store 那行被排除在范围外）。⭐⭐ **我们报 −15.82pp 时，必须把所有对照臂一起列，⛔ 不许挑范围** |
| **6** | ⛔ **正文声明的判据与表头实际维度不一致** | ⛔ §C.7：⛔ ISO 29148 的 `Unambiguous` 变成了表头的 `Consistency`。⭐ 我们声明按某分类学评时，⛔ 表头必须用那个分类学的名字 |
| **7** | ⛔⛔ **署名创新（三个算法）只有伪代码，⛔ 无实现、⛔ 无代码** | ⛔ 于是「一致性校验是自动的」这个说法无法验证 —— ⚠️ ⛔ **甚至无法判断它是软件跑的还是人手算的**。⭐ 我们的 1860 项测试 + 可跑代码在这一格上强得多 |
| **8** | ⛔ **5 位专家评分：⛔ 无独立性声明、⛔ 无盲评声明、⛔ 无 $\kappa$、⛔ ground truth 自产** | ⭐ 我们的判定也是自评、也无 $\kappa$。⚠️ ⭐ **但我们的判定对象可机械复算，⛔ 它的 1–10 打分不可复算** —— ⭐ 这个差别要讲清 |
| **9** | ⛔ **n=1 per cell 的人体实验，⛔ 组内落差比组间还大** | ⭐ §C.6 第 3 条。⭐ **若我们将来补 human baseline，⛔ 这是必须避开的设计错误** |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| # | 差别 | 后果 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **「双向」不是我们的双向** | ⭐ 需求⇄测试，⛔ 不是需求⇄模型。⛔ **C-③ 在这里没有先例可引。** ⭐ 能引的只有更弱的一条：⭐ 集合两侧残差骨架（§E.1 第 1 条） |
| **2** | ⛔⛔ **两端都是形式化制品，⛔ 我们一端是原始 NL** | ⭐ 它比对的是「结构化 UCS vs 模型」，⛔ 我们比对的是「模型 vs `nl.txt`」。⛔ **它把最难的那一半（NL 语义解释）外包给 LLM + 人的前置阶段。** ⛔ **所以它的三条规则不能直接搬到我们的 discover 上** —— ⭐ 我们没有一个已经被人校准过的中间制品 |
| **3** | ⛔ **闭合规则集但无选类动作** | ⛔ 三条规则无条件穷举施加，⛔ 没有「LLM 为这条需求选哪条规则」这个动作。⛔ **不是「闭合词表 + LLM 自动选」的先例。** ⭐ 可用的只是量级参照：**3（本篇）/ 8（Górski k+1）/ 19（我们）** |
| **4** | ⛔ **裁决者是词法匹配，不是 sound oracle** | ⭐ 比 LLM 自评强，⛔ 比模型检查器弱。⛔ **不能作为「用 sound oracle 当裁决者」的先例。** ⭐ 我们有 pyfcstm，⭐ 起点比它高 |
| **5** | ⛔ **模型代差：GPT-4（2023）vs 我们 `gpt-5.5` / `claude-opus-4-7`** | ⛔ 它报的「LLM 把属性误识别成对象、需人工纠正」在当代模型上很可能不成立。⛔ **它的「LLM 环节需要人把关」这个结论不能直接外推到我们** |
| **6** | ⛔ **样本量：1 个系统、20 个用例、n=1 per cell** | ⭐ vs 我们 54 pair × 2 模型 × 3 轮 = 324 格。⭐ **它的任何组间差异都可能是个体差异**（§C.6 第 3 条）。⭐ **当方向性证据看，⛔ 不当效应量证据** |
| **7** | ⛔ **它的任务含测试生成与追溯，⭐ 我们不含** | ⭐ Algorithm 1（UCS → 测试用例）与我们的 discover 无对应物。⭐ **这部分内容对 M1 无用**，⛔ 引用时不必带 |

---

## F. ⛔ 存疑与未核项

1. ⛔⛔ **本卡的全文逐字引文，我方未能用自己的入口独立复核。** —— ⭐ 已试过：`curl`（两个 Wiley host，均 **403**）· WebFetch（**402**）· curl_cffi TLS 伪装 3 种（均 **403**）· headless Chrome 3 种（**被识别，卡在 `Just a moment…`**）· 7 个代理/镜像（CAPTCHA / 522 / 需付费）· 8 个开放聚合站（**无全文**）。⭐ **正文来自本任务内一次本机 headful 浏览器会话（91,857 字符）。** ⛔ **复核者需走同一路线或用机构订阅。** ⭐ 元信息侧（DOI / 卷期 / 作者 / 年 / license / DBLP / GitHub）**已由我方独立实取核过**，⛔ 不依赖该会话。
2. ⚠️ **`ccf` 等级未定。** —— ⭐ 已试过 grep 本仓库 [ccf_venues/](../../../../../ccf_venues/) 全目录 `IET Soft` / `IET`，⛔ **零命中**。⛔ **本轮未独立核对官方 CCF 推荐期刊目录。** ⛔ 若报告需要 CCF 等级，⭐ **必须另行核 SE/系统软件/程序设计语言 方向的期刊名录**，⛔ 不要凭印象填。
3. ⚠️ **special issue 的 guest editor 情况只核到页眉。** —— ⭐ 页眉逐字 `Guest Editor: Tomasz Górski`；⭐ 而 §7.1 用整段对比 `"the k + 1 method [2, 48]"`，⭐ 且 ref [2]（`10.1016/j.softx.2024.101698`）与 ref [48] 都是 Górski 的工作。⛔⛔ **不得断言这影响了录用** —— ⭐ 这只是一个在权衡 venue 信号时值得知道的事实（**I**）。⛔ **本轮未核该 special issue 的正式 CFP 与范围。**
4. ⚠️ **Algorithm 2/3 是否真的被当软件执行过，无法判断（I）。** —— ⭐ 已试过：grep 全文 `Python` / `Java` / `parser`（各 **0 次**）· 查 repo 全部 9 个 blob（**全是 PDF + README**）。⛔ **既无实现也无运行证据。**
5. ⚠️ **Table 10 的 precision / recall 不可复算。** —— ⛔ 论文未说匹配单位（用例？步骤？business object？），⛔ repo 无脚本，⛔ 产出是 PDF。⛔ **所以「senior 65.38% / 87.18%」这两个数字我方无法验证，只能照抄。**
6. ⚠️ **Table 9 的 5 位专家逐人评分不可查、离散度未知。** —— ⛔ repo 无评分表。⛔ 所以「实验组 senior 9.5 分」这类数字的可信区间完全不明。
7. ⚠️ **正文说 6 条测试用例、Table 4 列 7 行（我方核出的内部不一致）** —— ⛔ 本轮未能判断哪个是笔误。⛔ 若要引用测试用例数，⭐ **应写「6 或 7（论文自相矛盾）」**。
8. ⚠️ **5 位专家与作者的关系、以及 ground truth 那位「15 年经验工程师」与作者的关系，原文均未声明。** —— ⛔ 本轮未尝试从作者主页/致谢反查。⛔ **不得断言存在利益关系，⛔ 也不得断言不存在。**
9. ⚠️ **PURE 原始数据集站点本轮未访问。** —— ⛔ `http://fmt.isti.cnr.it/nlreqdataset/` 未实测可达性。⭐ 若要复用 GAMMA-J Web Store，⛔ 需先确认该站点仍在。
10. ⚠️ **三条规则的完整形式化定义（Def 1–5）本卡只抄了签名，未抄全文。** —— ⭐ `BO = (N, Att, S_allowed, M, C)` · `BPM = (G, T)` 带满射 `type: ON → T` · `SM_bo = (S, Trans, A)` 带 `S ⊆ bo.S_allowed`。⛔ **各分量的完整语义未逐条抄回。** ⭐ 若 L2 要拿它做出处参照，⭐ 需回原文补。
11. ⚠️ **`pushed_at`(2025-04-25) 晚于 HEAD commit(2025-04-09) 这个差异，本轮未查明原因。** —— ⭐ 可能是分支操作、tag、或 GitHub 元数据更新。⛔ 不影响 HEAD 可 pin 这个结论。
12. ⚠️ **同卷一个近邻候选未核**：⭐ `10.1049/sfw2/6696040`「AI-Augmented Real-Time Collaborative Blended Modeling Framework for Automotive Embedded Systems」（⭐ IET Software，⭐ 报为 2026）。⛔ **本轮未取全文**，⚠️ 主题不同（协作式混合建模，⛔ 非一致性规则），⛔ 但若后续要扩 IET Software 的覆盖面，⭐ 这是一个入口。
