# 卡片 · SpecGPT（SECON 2026 poster）

⚠️⚠️ **先说一件影响全卡解读的事：正式发表版是 2 页 poster，而本卡是按 11 页的 arXiv 全文写的。**

- ⭐ SECON 2026 版：[`10.1109/SECON68281.2026.11579014`](https://doi.org/10.1109/SECON68281.2026.11579014)，标题带 `Poster:` 前缀，**pp. 206–207**（⭐ 经 Crossref API 核验）—— ⛔ **两页**。
- ⭐ arXiv 版：[`2510.14348v1`](https://arxiv.org/abs/2510.14348)（2025-10-16），标题**不带** `Poster:`，⭐ 含完整的 §III Design（含 Algorithm 1 与 prompt 模板全文）· §IV Evaluation（4 张表 · 3 个 RQ）· §V Discussion。

⛔⛔ **因此：本卡 B / C / D 三节的绝大多数细节几乎必然不在那 2 页 poster 里。** ⚠️ 若后续要引用其中任何一个数字或机制，**必须引 arXiv 版**，⛔ 引 SECON DOI 会让读者在 2 页里找不到对应内容。⭐ 两个版本都已核验存在，⛔ 但**我未能取到 poster 的实际 2 页内容**（见 F1），⛔ 所以「poster 里到底保留了哪些」无法逐项确认。

⭐ **本卡没有任何一节是「仅据摘要」** —— arXiv HTML（183 KB）与 PDF（11 页）均已通读，⭐ 且 Fig. 2（架构）与 Fig. 3（prompt 模板）的图内文字**已从 PDF 提取成功**。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `secon2026-3gpp-ensembles` |
| `title` | Poster: Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles（工具名 **SpecGPT**） |
| `year` | **2026**（Crossref `issued` = `2026-06-03`）；⚠️ arXiv 预印本是 **2025-10-16** |
| `venue` | SECON 2026 · 2026 22nd Annual IEEE International Conference on Sensing, Communication, and Networking，Pisa, Italy，**pp. 206–207**（⛔ **poster**） |
| `ccf` | ⚠️ **SECON 为 C 类（计算机网络），但本条大概率不计入** —— ⭐ CCF 目录明确只计 full / regular paper，⛔ short / poster / demo 不在考虑范围。⚠️ 本库 [ccf_venues/](../../../../../ccf_venues/) **未收录 SECON**（`grep -i secon` 零命中），⭐ 故整条标 **S** |
| `doi` | [`10.1109/SECON68281.2026.11579014`](https://doi.org/10.1109/SECON68281.2026.11579014) —— ⭐ **已过 Crossref API 核验**（title 含 `Poster:` 前缀、container、event Pisa 2026-06-03、pp. 206–207 全部对得上） |
| `arxiv` | [`2510.14348`](https://arxiv.org/abs/2510.14348)（本卡引用 **v1**） |
| `artifact_type` | ⭐ **协议状态机**（五元组 $\langle Q, \Sigma, q_0, \delta, F\rangle$，⭐ 迁移带 `condition` + `action`，⛔ 无时钟、无并发区、无层次） |
| `task` | ⭐ **生成 / 抽取**（3GPP 规约文本 → FSM）。⛔ 无缺陷检测、⛔ 无一致性检查、⛔ 无修复 |
| `boundary` | ⭐ `邻域`（协议状态机，按 [README.md](../README.md) §2.1） |

⭐ 作者单位：信息工程大学 + 紫金山实验室（**M**，PDF 首页）。

---

## B. LLM 应用形态

### B1 · 流水线阶段

```
[确定性] 文档清洗（正则去目录 / 页眉 / 页脚 / 脚注标记 / 空行 / 碎图表）
  → [确定性] Algorithm 1：解析章节号 → 建 section tree → 叶节点自底向上并入父节点 → merged windows
  → [人] 按协议在「state-oriented / procedure-oriented」二分类里挑一档 → 选 state prompt 或 process prompt
  → [LLM ×5 并行] 逐 window 抽 states
  → [LLM ×5 并行] 逐 window 抽 conditions + actions（迁移）
       ├─ 同一次调用内：prev_paragraph + paragraph 双段上下文
       ├─ 同一次调用内：自查指令（recheck of its rationality）
       └─ 轻量 RAG：以章节号为前缀做跨引用定位
  → [确定性] 后处理：JSON 结构校验（失败则 flag & report）+ 规则删伪状态 / 空状态
  → [人?] manual alignment 去明显不一致（⚠️ 见 B4）
  → [确定性] 跨模型对齐（状态精确相等 + 跨度重叠 ≥ θ=0.75）→ 多数投票
→ FSM
```

⭐ **阶段总数 8（不含下游）· LLM 阶段 2（但每阶段 ×5 个模型 = 10 次调用）· 确定性阶段 4 · 人工阶段 1–2。**

⚠️ Fig. 2 的图内标签逐字（**M**，从 PDF 提取）：`Preprocessing | 3GPP Specifications | Document Cleaning | Text Splitting || Domain-Informed Prompt Engineering | Paragraph Text | State Extraction | Condition and Action Extraction | Post Processing | Chain of Thought Prompting | Prompt Optimization | Collaborative Contextual Reasoning | Implicit Information Integration | Cross-Reference Handling || Model Ensembling | Enhance | Majority Voting | Finite State Machine`。

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 |
| :-- | :-- |
| state extraction | ⭐ **抽取器** |
| condition/action extraction | ⭐ **抽取器**（⚠️ 严格**摘录式**：要求逐字引原文）+ ⭐ **解释者**（被明确要求补出「需逻辑推断的隐含迁移」） |

⛔ **没有独立的评审者调用、没有修复者、没有裁决者、没有规划者。** ⚠️ 自查是**写在同一条 prompt 里的一句指令**（`For every complete transformation, a recheck of its rationality must be conducted.`），⛔ **不是**第二次调用、⛔ 不是第二个 agent。

### B3 · prompt 策略

`CoT`（任务拆成 state extraction → transition extraction → post-processing 三段）· `few-shot`（**M**：`we include few-shot examples to help the model learn and internalize this logical separation`，⭐ 用于教 condition 与 action 的分界）· `结构化输出约束`（prompt 内 `Desired format` 给 JSON 形状 + 事后结构校验）· `RAG`（⭐ **自称轻量**：⛔ 无 embedding、⛔ 无向量库，⭐ 只是允许多份规约同时入 prompt、用章节号做前缀建章级映射）· `多模型集成`（⛔ **不是** self-consistency，见 B4）。

⛔ **无 self-consistency**（⭐ 论文在 §V-A 把它列为**未来工作**：`the integration of emerging techniques such as retrieval-augmented generation and self-consistency to reduce hallucinations`）· ⛔ 无角色扮演 · ⛔ 无工具调用 · ⛔ 无多智能体辩论。

⭐ **Fig. 3「A unified basic prompt model for FSM」全文逐字**（**M**，从 PDF 文本层提取）：

```
Overall design prompt template
Extract state machine information from the combined content of these two parts (context + current).
Context paragraph:[prev_paragraph]
Current paragraph:[paragraph]
Instruction:
1. Covering (a) explicitly stated information and (b) partially described information that requires
   logical inference. However, the reasoning must be based on the original text.
2. State names must correspond to official protocol state machine nodes (e.g., "5GMM-DEREGISTERED").
3. For each transition, "condition" and "action" fields must be distinguished, with content quoted
   verbatim from the original text.
...
Note:
For every complete transformation, a recheck of its rationality must be conducted.
...
Desired format:
{"states": ["STATE1", ...],
 "transitions": [ {"from": "STATE1", "to": "STATE2", "condition": "...", "action": "..."},]}
```

⚠️ 模板里的 `...` 是**原文自己的省略号**（⛔ 论文把中间若干条指令省掉了），⛔ 所以**完整 prompt 并未公开**。

### B4 · ⭐⭐ 循环与裁决者（本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⛔ **无** —— ⭐ 严格单向：清洗 → 切分 → 两次抽取 → 后处理 → 投票。⛔ 全文无 revise / retry / regenerate / iterate-until 类机制 |
| ⭐ **裁决者是谁** | ⭐ **确定性规则**（跨模型对齐 + 多数投票）⚠️ **+ 可能有人** —— 见下 |
| 终止条件 | ⭐ **不适用**（无循环）；⭐ 每个 merged window 恰好被访问一次 |
| 最大轮数 | ⛔ **无轮数概念**（⛔ 不是「原文未提供」，⭐ 是结构上不存在） |
| ⭐ 逐轮边际收益 | ⛔ **不适用 / 原文未提供** —— ⭐ 但**有一个等价物**：跨模型集成的净增益，逐模型给全了（见下） |

⭐⭐ **裁决规则完全确定性、且写成了公式**（**M**，§III-E）。两条迁移 $T_i = (S_i^{init}, A_i, C_i, S_i^{next})$ 与 $T_j$ 判为对齐，当且仅当四条同时成立：$S_i^{init} = S_j^{init}$、$S_i^{next} = S_j^{next}$、$\mathrm{Overlap}(A_i, A_j) \ge \theta$、$\mathrm{Overlap}(C_i, C_j) \ge \theta$，其中

$$
\mathrm{Overlap}(A_i, A_j) = \frac{|\mathrm{span}(A_i) \cap \mathrm{span}(A_j)|}{\min(|\mathrm{span}(A_i)|, |\mathrm{span}(A_j)|)}
$$

⭐ 取 $\theta = 0.75$（**M**：`We set θ as 0.75 in practice, which yielded the best performance in our evaluation.`）。⭐ 状态名要求**精确相等**，⭐ condition / action 按**词级跨度重叠**比，⛔ 不做语义相似度、⛔ 不用 LLM 判等。

⚠️⚠️ **但集成里可能夹了一步人工，原文措辞含糊**（**M** 引文 + **I** 判断）：`Due to architectural and behavioral differences among models, their interpretations and outputs may vary, necessitating manual alignment to remove obvious inconsistencies, such as omissions in state transitions. Additionally, ... To address these discrepancies, we introduce a consensus mechanism based on the principle of state transition completeness, utilizing a correlation matching algorithm as follows.` ⛔ 读不出来「manual alignment」是**已经做了的一步**、还是**被后面那个算法取代了的一个动机陈述**。⚠️ 若是前者，则 SpecGPT 的裁决链是「**人工去明显不一致 → 确定性对齐 → 多数投票**」，⛔ 那么 91.14% 这个 F1 不是全自动结果。⭐ **这是本卡最重要的一条存疑项**（见 F2）。

⭐⭐ **集成的净增益（逐模型全给，这是这篇最可直接引用的数字）**（**M**，Table I，NAS 迁移抽取）：

| 模型 | Precision (%) | Recall (%) | F1 (%) | ⭐ 集成相对本模型的 F1 增益 |
| :-- | --: | --: | --: | --: |
| Claude Sonnet 4 | 80.39 | 87.23 | 83.67 | +7.47 |
| DeepSeek V3 | 68.70 | 84.04 | 75.60 | +15.54 |
| Gemini 2.5 Pro | 70.00 | 89.36 | 78.50 | +12.64 |
| GPT 4o | 79.09 | **92.55** | 85.29 | **+5.85** |
| Qwen Turbo | 61.71 | 77.66 | 68.77 | **+22.37** |
| ⭐ **Ensemble** | **91.86** | 90.43 | **91.14** | — |

⭐ 论文自己给的区间 `ranging from 5.85% to 22.37%` 与上表**逐项复算一致**（⭐ 我算过：$91.14 - 85.29 = 5.85$；$91.14 - 68.77 = 22.37$）。

⭐⭐ **增益的结构（这一点论文没直接点明，我算的）**：⭐ 集成相对**最强单模型** GPT-4o 是 **precision +12.77pp、recall −2.12pp**。⭐ 即**集成几乎全部收益来自砍多报，代价是极小的漏报** —— ⭐ 论文的归因与此一致：`the ensemble method's ability to remove incorrect transitions caused by hallucinations in individual models`（**M**）。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有，五层**（⭐ 比 ProtocolGPT 厚得多） |
| 形态 | ① **协议二分类学**（state-oriented / procedure-oriented）② **section tree + merged windows**（文档结构本身作为遍历单位）③ **JSON schema**（`states` + `transitions{from,to,condition,action}`）④ **摘录式跨度约束**（condition / action 必须是原文逐字片段）⑤ **伪状态黑名单**（`Unknown` / `Undefined` / 空状态） |
| ⭐ 是否闭合 | ① ⭐⭐ **闭合，只有 2 类** ② ⭐ 闭合（由文档章节号机械导出）③ ⭐ 形状闭合、内容开放 ④ ⭐⭐ **闭合到「原文子串」这个集合** ⑤ ⭐ 闭合（规则枚举） |
| ⭐ 谁定的 | ① ⭐⭐ **人预编 + 人挑**（⛔ **不是 LLM 选**）② ⭐ 确定性算法 ③ 人 ④ 人 ⑤ 人 |

⭐⭐ **① 这一格必须说清，因为它直接对位我们的「谁选类」问题**：⭐ 二分类是作者自己从规约里归纳的（**M**：`Based on our in-depth analysis of the 3GPP protocol specifications, we categorize them into two types: state-oriented and procedure-oriented protocols`），⭐ 而**选哪一档是人在协议层面一次性定的**（**M**：`Based on this classification, we divided prompts into state prompts and process prompts during state extraction`，⭐ NAS 归 state-oriented、PFCP 归 procedure-oriented）。⛔ **模型不参与选类**。⭐ 所以：**闭合 + 人挑**，⛔ 而我们是**闭合 + LLM 自动选**。⚠️ 这一带**没有为我们那个组合提供先例**。

⭐⭐ **④ 是这篇对我们最有价值的机制**：⭐ 迁移的 `condition` 与 `action` 被要求**逐字摘自规约原文**（`content quoted verbatim from the original text`）。⭐ 后果有三层：⭐ (a) 每条迁移天然带一个**回指规约文本的锚点**；⭐ (b) 跨模型比对因此可以退化成**纯词法**的跨度重叠，⛔ 不需要语义判等；⭐ (c) 幻觉被限制在「选错跨度」而非「编造措辞」。⭐ 这正是把语义判断挤出裁决器的一种做法，⛔ 与本仓库 §11「只放能完美判定的约束进 validator」是同一个思路的另一种落法。

### B6 · 模型

⭐⭐ **5 个模型 · 全部当代 SOTA · 跨 5 家厂商**（**M**，§IV-A）：`GPT 4o` · `DeepSeek V3` · `Qwen Turbo` · `Claude Sonnet 4` · `Gemini 2.5 Pro`。⭐ 统一 `temperature = 0.2`、⭐ 统一同一份 prompt、⭐ 统一参数。⭐ 硬件：32 GB RAM + Intel Core i7-14700。

⭐⭐ **这是 5 个不同模型各跑一次，不是同一个模型采样多次。** ⚠️ 这一条必须与我们的 `hit@3` 严格区分：

| | SpecGPT 的 ensemble | ⭐ 我们的 `hit@3` |
| :-- | :-- | :-- |
| 变的是什么 | ⭐ **模型**（5 家） | ⭐ **采样**（同模型 3 轮） |
| 聚合方式 | ⭐ **多数投票取交集**（≥3/5） | ⭐ **取并集**（≥1/3 命中即算） |
| 目的 | ⭐ **抑制幻觉、抬 precision** | ⭐ **度量能力上界** |
| 报告形态 | ⭐ 单一共识产物的 P/R/F1 | ⭐ 三口径并列 |

⭐ 论文明确写模型间差异是**架构与行为差异**（`Due to architectural and behavioral differences among models`），⛔ 即它刻意要的是**异质性**；⛔ 同模型重采样得不到这种异质性。⚠️ 这意味着**它的集成收益不能直接推断到我们的多轮设置上**。

⭐ 另一条对模型代次的旁证：⭐ 最弱的 Qwen Turbo（F1 68.77）与最强的 GPT-4o（85.29）差 **16.5pp** —— ⭐ 同一 prompt 下模型间差距很大，⛔ 支持 X1 那条「用旧模型得出的结论要打折」。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | ⭐ 是不是 sound |
| :-- | :-- | :-: |
| 文档清洗 | 正则去目录 / 页眉 / 页脚 / 脚注 / 空行 | ⛔ 否（启发式） |
| Algorithm 1 切分 | 章节号解析 → section tree → 叶节点自底向上并入父节点 | ⭐ **是**（纯结构操作，⛔ 但对「切得对不对」不 sound） |
| 跨引用定位 | 章节号前缀映射（⛔ 无 embedding、⛔ 无向量库） | ⭐ **是**（章节号是精确键） |
| 结构校验 | JSON 解析正确性 | ⭐ 是（⛔ 只判形状） |
| 后处理 | 规则删伪状态 / 空状态 | ⭐ 是（黑名单枚举） |
| 集成对齐 | 状态精确相等 + 词级跨度重叠 ≥ 0.75 | ⭐ **是**（纯词法，⛔ 但 0.75 是拍的） |
| 多数投票 | 计数 | ⭐ 是 |

⛔⛔ **仍然没有 sound oracle。** ⭐ 确定性环节比 ProtocolGPT 多且更干净（⭐ 有两个是真正精确的：章节树与章节号映射），⛔ 但**没有任何一个环节能回答「这个状态机本身合不合法 / 可不可达 / 有没有死锁」** —— ⛔ 无模型检查器、⛔ 无可达性分析、⛔ 无一致性检查、⛔ 无对 3GPP 规约的形式化参照（⭐ 论文 §I 自己说 `3GPP does not provide formal models of the protocols`）。⭐ 论文把形式化验证列为**下游用途**（§V-B），⛔ 不在环内。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **三档**：① **Hermes**（USENIX Security'24，SOTA，⚠️ 见下的可比性问题）② **NEUTREX**（Hermes 的神经成分句法分析器，⭐ 在 Hermes 自己的 ground truth 上做头对头）③ **朴素直问**（⛔ 不用他们的 prompt 设计，直接让模型输出状态机 → F1 **14.87%**） |
| `dataset` | ⭐ 三个 5G 核心网协议的 **Release 17** 规约：NAS（TS 24.501）· NGAP（TS 38.413）· PFCP（TS 29.244）。⭐ NAS ground truth = **18 states / 179 transitions**。⭐ 另用 **R15** 版 NAS 做泛化性检查（抽出 142 条迁移，⭐ 比 R17 少约 20%）。⭐ **分母 = 作者自建的人工 ground truth**（⛔ 无公开可比 ground truth，**M**：`Due to the absence of publicly available ground truth for their complete state machines, we construct manually annotated references`） |
| `metrics` | ⭐ Precision / Recall / F1（标准定义）。⭐ **判对的条件是复合的**：状态名精确相等 **且** condition 与 action 的跨度重叠 ≥ **0.75**（**M**：`a state machine transition is considered correct only if the states match exactly, and both the condition and action spans overlap beyond a specified threshold, which we set as 0.75`）。⛔ **无 `@k` 口径**；⛔ 无部分得分档（⛔ 不像 ProtocolGPT 有 `partially correct`） |
| ⭐ `judged_by` | ⭐ ground truth：**> 210 人时**、**多名领域专家**、含**交叉验证与迭代同行复核**（**M**：`This effort involved over 210 person-hours of work by multiple domain experts, including cross-validation and iterative peer review to ensure protocol type coverage, state completeness, and strict compliance with 3GPP specifications`）。⭐ 判定本身：**自动脚本**（跨度重叠算法）。⛔ **无 $\kappa$、无标注者间一致率**（⭐ 只说 cross-validation + peer review，⛔ 未给可测数字）；⛔ **专家人数未给**（只写 multiple）；⛔ 无 LLM-as-judge |
| `human_baseline` | ⛔ **无**（⭐ 人工只用于建 ground truth。⚠️ 论文 §I 与 §V-B 反复强调现状是「专家手工建模」，⛔ 但**没有把人工建模速度 / 质量做成对照臂**） |
| `runs` | ⛔⛔ **原文未提供** —— ⛔ 未说每个模型跑几次、⛔ 是单次还是均值、⛔ **无方差、无置信区间、无显著性检验**。⭐ 从 Table IV 每个 (协议, 模型) 只有一行 token 数与一个时间数看，**看起来是各跑一次**（**I**，⛔ 不得写成事实） |
| ⭐ `adverse_results` | ⭐ **不利结果基本都留在表里，但归因偏软**（见下） |

⭐ **成本与时间（可直接与我们的 212.6× 对照）**（**M**，§IV-D + Table IV）：⭐ 每次运行约 **$2.7（NAS）/ $1.6（NGAP）/ $1.5（PFCP）**。⭐ 单模型单协议 token 量级：NAS 输入 22–24 万、输出 5–10 万。⭐ 墙钟 **10–202 分钟**（⭐ GPT-4o 最快 10–20 min，⛔ Gemini 2.5 Pro 最慢 113–202 min）。⭐ 论文的成本论证是**一次性摊销**：`protocol state machine extraction is usually performed only once per document`。

⭐ **不利结果的处理（三处，逐条看）**：

1. ⭐ **最差的那一格原样留着**：NGAP-UCM F1 **60.93**、NGAP-all **69.31**（⭐ 而 NAS 是 91.14、PFCP-session 92.30）。⭐ 归因写了：`the NGAP protocol is more complex and exhibits certain ambiguities in its specification`，⛔ 但紧接一句 `its overall extraction performance still satisfies the basic requirements for practical application` —— ⚠️ **「基本满足实用要求」没有任何判据支撑**，⛔ 属于软化措辞。
2. ⭐ **单模型的低 precision 照实说了**：`the models exhibit relatively low precision, ranging from 61.71% to 80.39%`，⭐ 并给出机制归因：`Large language models tend to generate significantly more transition tuples than actually exist, leading to a higher false positive rate`。⭐ 这条归因是**可检验的**（⭐ 与 Table I 的 P 低 R 高格局一致），⭐ 质量比第 1 条高。
3. ⭐ **Limitations 里明确承认残余 FP/FN**：`it still suffers from false positives and false negatives due to inherent limitations such as hallucinations`，⭐ 并给出两条改进方向（⭐ 基座模型进步 + ⭐ 引入 RAG / self-consistency）。⛔ 但**没有给出 FP/FN 的实际条数或分类**，⛔ 只有汇总 P/R。

⚠️ **与 Hermes 的对比不是受控对比**（**M** 引文 + **I** 判断）。⭐ 论文自己交代了两件事：⛔ `Hermes does not provide the actual state machines it constructed`，⭐ 以及 `It is worth noting that the ground truth used by SpecGPT is more comprehensive in terms of both the number of states and transitions`。⛔ 也就是说 **86.41 / 92.94 vs 81.39 / 86.40 这组数字，是「SpecGPT 在自己更大的 ground truth 上的成绩」对「Hermes 论文自报的、在 Hermes 自己 ground truth 上的成绩」** —— ⛔ 两边分母不同、⛔ 判定口径不同、⛔ 没有在同一答案上重跑 Hermes。⚠️ 按本仓库 §3.5 第 4 条的精神，⛔ 这组数字不足以支撑「outperforms the SOTA」。

⭐ **但 Table III 那组是干净的头对头**：⭐ 用 **Hermes 自己提供的 ground truth**（`we use the ground truth provided by Hermes, which includes human-annotated transition components`）比标注子任务：⭐ NEUTREX-Labeled 64.30 / 66.13 / 65.20 · NEUTREX-Unlabeled 66.88 / 68.79 / 67.82 · **LLM 87.46 / 90.40 / 88.90**。⭐ 这一格**同分母、同答案**，⭐ 是这篇最可信的对比结论：**零训练的 LLM 在成分标注上大幅超过专门训练的神经句法分析器（+21pp F1）**。

---

## D. ⭐ 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文（arXiv 全长版） | 🟢 | [arxiv.org/abs/2510.14348](https://arxiv.org/abs/2510.14348) | ⭐ `curl` HTTP 200；HTML **183 568 字节**、PDF **757 408 字节 / 11 页**，⭐ 均已通读；⭐ Fig. 2 / Fig. 3 图内文字**已从 PDF 提取** |
| 论文全文（SECON poster 版） | 🟠 | [ieeexplore.ieee.org/document/11579014](https://ieeexplore.ieee.org/document/11579014) | ⛔ `curl -L` 返回 **HTTP 202 / size=0**（bot 拦截或需鉴权）；⭐ 元数据经 **Crossref API** 核实（**pp. 206–207**，⛔ 即 2 页）。⛔ **poster 的实际内容未取到** |
| ⭐ **实验代码** | ⚪ | — | ⛔ **论文全文无任何代码 / artifact / availability 声明**（⭐ 已 grep `available` / `releas` / `open.?source` / `artifact` 全文，⛔ 零命中相关承诺）。⭐ GitHub Search API：`SpecGPT+3GPP` → **0 结果**；`SpecGPT` → 6 个仓库，⛔ **无一与本文相关**（nvme 规约 chatbot、通用领域 LLM 等） |
| ⭐ **数据集 / ground truth** | ⚪ | — | ⛔ **未公开**。⚠️ 这一项最可惜：⭐ 那是 **> 210 人时**建出来的 NAS 18 states / 179 transitions + NGAP + PFCP 三协议标注，⭐ 论文自己说它 `provid[es] a robust foundation for future research`，⛔ 却**没给获取方式**。⭐ 论文同时指出现有公开 ground truth 覆盖不足 —— ⛔ 于是这个缺口继续存在 |
| 实验结果细则 | ⚪ | — | ⛔ 只有论文内 Table I–IV；⛔ 无逐条抽取结果、⛔ 无 FP/FN 清单、⛔ 无抽出的状态机本体 |
| Artifact / 复现包 | ⚪ | — | ⛔ 无 Zenodo / 4open / OSF DOI；⛔ 无 badge |
| ⭐ **prompt 是否公开** | 🟠 | 论文 Fig. 3 | ⚠️ **部分公开**：⭐ Fig. 3 给了统一模板的骨架（⭐ 已逐字抄进 B3），⛔ **但模板内含两处原文自带的 `...`**，⛔ 中间的指令条目被省略；⛔ few-shot 例子的实际内容**未给**；⛔ state prompt 与 process prompt 的两个变体**未分别给出** |

⭐ **一句话**：⭐ 除了 arXiv 全文，⛔ **什么都没有**。

---

## E. ⭐ 对 M1 的意义

### 1 · ⭐ 可取之处

1. ⭐⭐ **「摘录式跨度 + 词法重叠判等」是把语义判断挤出裁决器的一个可直接搬的做法。** ⭐ 他们要求 `condition` / `action` **逐字引原文**，于是跨模型比对退化成 $\mathrm{Overlap} \ge 0.75$ 这种纯词法运算 —— ⛔ 不需要 LLM 判等、⛔ 不需要语义相似度。⭐ 对我们的直接含义：⭐ 我们的断言若也要求把「它对应需求里的哪一句」以**逐字跨度**形式带出，⭐ 那么「同一条缺陷是否被重复报」「两轮是否命中同一条」这类判定就可以**机械做**，⛔ 而我们现在靠的是 574 位逐位人工判定。⚠️ 这是本卡对我们**最省钱的一条**。
2. ⭐⭐ **异质模型集成的收益结构值得照抄一次实验**：⭐ 相对最强单模型 **precision +12.77pp / recall −2.12pp**、F1 +5.85pp。⭐ 若我们的多报是主要痛点，⭐ 那么「换两个不同厂商的模型各跑一遍、取交集」比「同一个模型多跑几轮」更可能奏效 —— ⚠️ 而且我们**本来就已经在跑两个模型**（`gpt-5.5` + `claude-opus-4-7`），⛔ 只是把它们当**独立对照臂**而不是**集成成员**。⭐ 这是一条**几乎零额外成本**的可试项：拿现有 324 格的数据，直接算「两模型同一 pair 上都报的那些」的 precision。
3. ⭐ **章节树切分（Algorithm 1）比固定窗口切分更值得用在需求侧。** ⭐ 他们的论据很实在（**M**）：固定窗口会截断上下文，纯段落切分会产出大量只有一两句的碎片、造成 `a large number of ineffective queries`。⭐ 于是按**文档自身的层次结构**自底向上合并到父节点。⭐ 对我们的含义：⭐ NL 需求的切分单位如果按结构（章 / 条 / 编号项）而不是按长度，⭐ 既能保证遍历完整（**每个 window 恰好被访问一次**），又能避免碎片。
4. ⭐ **成本与墙钟报得很细，包括最慢的模型。** ⭐ Table IV 逐 (协议 × 模型) 给输入 token / 输出 token / 分钟数，⭐ 并给出美元估算。⭐ 我们报 212.6× 时也应当这样拆开 —— ⭐ 这种颗粒度让「贵」变成可诊断的，⛔ 而不是一个挨批的总数。

### 2 · ⛔ 不可取 / 陷阱

1. ⛔⛔ **判定阈值是在评测集上调出来的，而且这个阈值同时用在裁决器和评分器上。** ⭐ 逐字：$\theta = 0.75$ `which yielded the best performance in our evaluation`；⭐ 而评分时 `we adopt an alignment strategy similar to that used in the ensembling process` 也用 0.75。⛔ 于是**同一个被调过的算子既参与产出、又参与判分**，⛔ 且没有 hold-out。⚠️ 按本仓库 §3.5 第 4、5 条，⛔ 这是我们**不能重复的**：⭐ 我们没有留出集这件事本来就更敏感，⛔ 任何阈值必须**先冻结再跑**（⭐ 事前登记就是为此存在的），⛔ 且不得用产出侧的同一个算子去判分。
2. ⛔⛔ **「manual alignment」这一步的存在性没交代清楚，导致 91.14% 的自动化程度不可判。** ⚠️ 这正是我们自己要极力避免的写法：⛔ 若人工介入了就必须写清介入了什么、多少工时、影响哪些条目。⭐ **教训是防御性的**：⭐ 我们报 `hit@1 = 60.4%` 时必须能一句话说清「这个数字里有没有人手」。
3. ⛔ **与 SOTA 的对比跨了 ground truth，还自己说了自己的 ground truth 更大。** ⛔ 分母不同就不该并排放 P/R 然后写 outperforms。⭐ 我们与 X1 朴素基线比时**必须同分母同判定**（⭐ 这一点我们目前做对了，⛔ 别退化）。
4. ⛔ **prompt 里带着被评测协议的真实状态名做示例，而 state extraction 恰好报 100%。** ⭐ 模板第 2 条逐字：`State names must correspond to official protocol state machine nodes (e.g., "5GMM-DEREGISTERED")`。⚠️ `5GMM-DEREGISTERED` 是 TS 24.501 里的标准 5GMM 状态名，⚠️ **看起来极可能就在那 18 个 NAS ground truth 状态里**（⛔ ground truth 未公开、无法确认，**I**）。⚠️ 与此同时 state extraction 的 F1 是 **100%（五个模型全对）**，⛔ 而分母只有 **18**。⭐ 两件事叠起来，⛔ 这个 100% 的信息量很低：⭐ 它既可能是能力、⛔ 也可能有一部分来自 prompt 里给了命名形态与一个真值样例。⚠️ **对我们的意义是纪律性的**：⭐ 我们 prompt 里的 worked example **绝不能取自被评测 pair**（⚠️ 我们已经在 `occupancy_after` 的 `nl_cue` 上栽过一次形态相近的事故），⛔ 且分母只有十几条的指标不要当结论用。
5. ⛔ **完全没有循环，也完全没有 sound oracle —— 这不是可取之处，只是这一带的现状。** ⚠️ 不要把「他们不做循环也拿到 91%」读成「循环没用」：⭐ 他们的任务是**忠实摘录**（答案就在文本里、有逐字锚点），⛔ 我们的任务是**发现不符**（答案不在任一处文本里，需要跨制品推理）。⛔ **任务难度不同，不能拿他们的无循环成功来论证我们该拆掉循环。** ⭐ 我们拆 reviewer 的理由是自己的实测（⛔ 零收益吃 79% token），⛔ 不是这篇。

### 3 · ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⛔⛔ **C-③ 那一格：有对应关系，但没有覆盖缺口记录。** ⭐ 这篇**确实建立了「规约文本 ↔ 状态机元素」的对应**，而且比我预期的强：⭐ (a) 每条迁移的 condition / action 是**规约原文的逐字跨度**；⭐ (b) 每条迁移绑定在一个具体的 `(prev_paragraph, paragraph)` 窗口上；⭐ (c) 遍历单位由章节树机械导出，**每个 window 恰好访问一次**，⭐ 所以「规约的哪些部分被看过」是有定义的。⛔⛔ **但「规约里说了而状态机里没有」从头到尾没有被记下来**：⛔ 没有「这个 window 我读了但没产出迁移」的诊断、⛔ 没有 unmet / coverage_gap 类结构化输出、⛔ 后处理对 JSON 失败的处理是 `automatically flagged and reported`（⭐ 只报告，⛔ 不回灌、⛔ 不进产物）。⭐ 缺口**只在评测时**以 FN 的形式出现（⭐ 对着 210 人时的 ground truth 数出来），⛔ **流水线自己不知道自己漏了什么**。⭐ 所以这一格对我们仍然是**没有先例**的 —— ⭐ 但它给了我们**一半的零件**：⭐ 逐字跨度锚点 + 机械导出的遍历单位，⭐ 这两样加起来足以支撑「逐 window 记一条 produced / empty」的最小 coverage 台账。⚠️ **这是本卡对 C-③ 最实质的贡献。**
2. ⛔ **任务性质：忠实摘录 vs 发现不符。** ⭐ 他们的真值**在文本里**（⭐ 所以能要求逐字引用、⭐ 所以词法重叠够用、⭐ 所以 recall 天然高）；⛔ 我们要判的是**制品与文本不符**，⛔ 真值不在任何单一位置。⛔ 因此他们的高 recall / 低 precision 格局与我们相反（⭐ 我们的痛点里有「根本没问」这一半，⛔ 那是 recall 侧的结构缺陷，⛔ 不是幻觉造成的多报）。
3. ⛔ **闭合集的「谁选」不同：他们人挑（2 类），我们 LLM 自动选（19 条）。** ⛔ 这一带**没有为我们的组合提供先例**；⚠️ 而且他们只有 2 类，⭐ 人挑成本可忽略，⛔ 这个方案在 19 条 × 每条需求的规模上不可行。⛔ **不能照搬「让人挑」。**
4. ⚠️ **他们的 ensemble 靠的是厂商间异质性，我们的多轮靠采样随机性。** ⛔ 前者的收益机制（不同架构犯不同的错、交集干净）在后者上**不成立或大幅衰减**。⚠️ 若要复用，⭐ 应当用**我们已有的两个模型**做集成而非同模型重采样，⛔ 且必须自己测增益，⛔ 不得引用 +5.85pp 这个数字当预期。
5. ⭐ **ground truth 人时可比，且我们更省**：⭐ 他们 **> 210 人时** / 3 协议（NAS 一家就 18 states + 179 transitions）；⭐ 我们 G1 是 **33–49 人时** / 98 条能力分母。⭐ 量级同阶、⭐ 我们更小 —— ⭐ 这说明我们的人工投入在这一带**不算异常**，⛔ 但也说明**别指望靠加人工把台账做到他们那种规模**。

---

## F. ⛔ 存疑与未核项

1. ⚠️⚠️ **SECON poster 的 2 页实际内容未取到** —— 已试过 `curl -L https://ieeexplore.ieee.org/document/11579014`（**HTTP 202 / 0 字节**）。⭐ 已确认的只有 Crossref 元数据（⭐ 标题带 `Poster:`、**pp. 206–207**）。⛔ 因此**无法逐项确认 poster 保留了哪些内容**；⛔ 本卡全部 **M** 级片段出自 **arXiv v1**。⚠️ 引用时的风险已在卡首标注。
2. ⚠️⚠️ **「manual alignment」到底做没做，无法判定** —— 原文 §III-E 的措辞（`necessitating manual alignment to remove obvious inconsistencies` → 紧接 `To address these discrepancies, we introduce a consensus mechanism ...`）**两种读法都通**：⛔ 要么人工是流水线的一步、⛔ 要么它只是引出算法的动机陈述。⚠️ **这直接决定 91.14% 是不是全自动结果**，⛔ 也决定 B4 裁决者一栏该不该写「人」。⛔ 全文无第二处提及人工介入、⛔ 无工时、⛔ 无介入条目数。⭐ 我已把两种可能都写进 B4，⛔ **不下结论**。
3. ⚠️ **每个模型跑几次、有无重复、有无方差，全部未提供** —— ⛔ 无 runs 说明、⛔ 无标准差、⛔ 无置信区间、⛔ 无显著性检验（⚠️ 对比 ProtocolGPT 至少给了「10 次均值 + p < 0.05」）。⭐ 从 Table IV 每格只有一个 token 数与一个时间数推测是单次（**I**）。⚠️ 后果：**Table I 那些 5–22pp 的集成增益无法排除单次采样波动**。
4. ⚠️ **prompt 未完整公开** —— Fig. 3 里有两处**原文自带的 `...`**（Instruction 第 3 条后、Note 后），⛔ 省掉的指令条目数与内容未知；⛔ few-shot 例子的实际文本未给；⛔ state prompt / process prompt 两个变体未分别列出；⛔ `Prompt Optimization` 三个子机制（collaborative contextual reasoning / implicit information integration / cross-reference handling）**只有散文描述，无对应模板文本**。
5. ⚠️ **NAS 的 18 个 ground truth 状态清单未公开，因此「prompt 示例是否为真值元素」无法确认** —— ⭐ `5GMM-DEREGISTERED` 是 TS 24.501 的标准状态名（⭐ 这一点确定），⛔ 但它是否恰在那 18 条里、⚠️ 以及 state extraction 的 100% 有多少来自这个示例，**无法核**（⛔ ground truth 未公开、⛔ 无消融）。⭐ 已在 E2.4 按 **I** 记录，⛔ 未写成事实句。
6. ⚠️ **NGAP / PFCP 的 ground truth 规模未给** —— ⭐ 只有 NAS 给了 18 states / 179 transitions。⛔ NGAP 与 PFCP 的状态数、迁移数、以及 Table II 里 5 个子层各自的分母**全部未提供**，⛔ 所以 NGAP-UCM 的 60.93 是在多大分母上算的**不知道**。
7. ⚠️ **成本数字的口径不明** —— `$2.7 for NAS` 是**单模型一次**还是**五模型集成一整轮**，⛔ 原文未交代。⭐ Table IV 是逐模型列的，⚠️ 若按五模型加总则实际约为该数的 5 倍。⛔ 我未做换算，⛔ 也不据此推断。
8. ⚠️ **CCF 等级与「poster 是否计入」均未经本库核验** —— [ccf_venues/](../../../../../ccf_venues/) 里 **SECON 无条目**。⭐ 「C 类 · 计算机网络」与「short / poster 不计入目录」两条来自 CCF 官方目录的通行规则，⛔ 我**没有直连 ccf.org.cn 逐条核对**，⭐ 故 A 节整格标 **S**。⚠️ 另注：2026-03 CCF 完成新一轮目录公示修订，⛔ 等级可能已变。
9. ⚠️ **Fig. 1（5G 架构）与 Fig. 4（逐模型逐成分标注效果柱状图）的图内数值未完整读出** —— ⭐ Fig. 4 的文本层只提出了零散数字 `81 86 91 96`（⭐ 疑为 y 轴刻度）与三个成分标签 `<state> <contion>[sic] <action>`，⛔ **逐模型逐成分的具体数值未能确认**。⭐ 因此 §IV-C 「All five models demonstrate strong performance across the annotation of individual components」这一句**只有正文断言、无我方核实的数字支撑**。
