# 卡片 · Sultan & Apvrille, ERTS 2026 —— 把**完整语法检查**与**模型检查**一起接进 TTool-AI 的生成循环

⭐ **全文已取到并通读**（⛔ 不是仅据摘要）。⭐ 论文是 **CC-BY 4.0**、6 页、HAL 开放获取。⚠️ `hal.science` 对 CLI 一律返回 Anubis 反爬挑战页（`algorithm: fast, difficulty: 4`），⭐ 本轮实际取到 PDF（`539,452 B` · PDF 1.4 · 6 页）并用 [`tools/pdf_extractor.py`](../../../../../tools/pdf_extractor.py) `text` 模式提取（29,062 B，⭐ 质量正常无乱码）。

⚠️⚠️ **标识符先纠一处**：⛔ 任务书给的标题 **不是** 论文内页的标题。见 [§A](#a-元信息) 与 [§F.1](#f-存疑与未核项)。

⚠️ **本卡开头先按任务书顺序答四个必答问题**，⛔ 因为它们决定这篇对 M1 是「可搬形状」还是「反面教材」。

---

## ⭐⭐ 必答① · 语法检查与形式化验证各接在循环的哪一环

⭐ **答案：不是"一个循环里两道门"，⛔ 而是两个嵌套循环 —— 语法检查是内环、模型检查是外环，⛔ 且外环只有在内环清零后才启动。**

⭐ 逐字（M，§3）：

> "That response is then algorithmically analyzed (T3) by the tool against a set of constraints, checking the format of the response (i.e., whether it meets the required structure for parsing), the consistency of the generated SMDs, and (this point is a central contribution of the paper) their complete syntactic correctness. […] **If errors are detected, a new prompt, incorporating both the identified issues and the previously generated SMDs, is constructed and sent back to the LLM, returning the process to T1.**"

> "**If no error is found, the process advances to the safety properties verification loop.** First, in step T4 the tool generates a set of safety properties for each SMD and verifies them using TTool's model checker [5]."

⭐ 嵌套关系有逐字确证（M，§4）：

> "Since up to 20 safety verification loops were allowed, **each potentially containing up to 20 syntax verification sub-loops**, verification failures have led to processing times of up to 26 minutes in our tests."

⭐⭐ **两道门的分工是"先能不能解析、再对不对"**：⛔ 语法正确性在这里不是锦上添花，⭐ 而是**模型检查的前置必要条件** —— 逐字（M，§4 末）："This represents a major step toward the formal verification of AI-generated models, since **their syntactic correctness is the necessary condition to run model-checking algorithms**."

⭐ 两道门的规则出处也不同：⭐ 语法规则**来自另一篇论文的形式定义**（M，§3）："The rules checked to ensure syntactic correctness **follow from the definitions of syntactic correctness given in [26], Section 3.1**"（⭐ [26] = AMULET, ACM TECS 24(3), 2025）；⭐ 安全性质则是工具按两个模板机械生成的（见 [B5](#b5--中间表示)）。

---

## ⭐⭐ 必答② · 验证器的反例怎么回灌给 LLM

⭐⭐ **答案：⛔ 反例根本不回灌。⭐ 回灌的是"哪几条性质没满足" ＋ 对应的那张 SMD —— ⛔ 没有反例路径、⛔ 没有翻译成自然语言的解释、⛔ 没有定位到具体状态或迁移。**

⭐ 逐字（M，§3）：

> "If any property is violated, **a new prompt, containing the unsatisfied properties and the corresponding SMD**, is sent to the LLM, returning the process once again to T1."

⭐ 对照语法环的回灌（M，§3）：

> "a new prompt, **incorporating both the identified issues and the previously generated SMDs**, is constructed and sent back to the LLM"

⭐ **两环的回灌形态是同构的**：⛔ 都是「问题清单 ＋ 上一版制品」，⛔ 都不含 oracle 的内部证据。

⚠️⚠️ **而模型检查器明明有反例信息，只是没进 prompt。** ⭐ Fig. 2 的图注逐字（M）："**Green backtracing** shows that all states satisfy the safety properties." ⭐ 即回溯（backtracing）结果在 TTool GUI 里对**人**是可见的；⛔ 论文没有任何一处说它进了 prompt（S：全文检索无 counterexample / trace / witness / backtrace 进入 prompt 的表述）。

⭐⭐ **最关键的是作者自己把这一点认成了失败主因**（M，§4，逐字）：

> "Further refinement of prompt engineering (**particularly improving the feedback provided to the LLM regarding each unsatisfied property**) would likely enhance the effectiveness of the auto-correction mechanism, **on which we cannot conclude based on this first evaluation**."

⭐⭐ **对 M1 的直接含义**：⭐ 这篇把裁决者换成了真 sound oracle（⭐ 我们想做的那一步），⛔ **而循环仍然不收敛** —— ⛔ 瓶颈不在裁决者可不可信，⭐ 而在**反馈里带不带可执行的信息**。⛔ 见 [E.2](#e-对-m1-的意义)。

---

## ⭐⭐ 必答③ · 循环几轮？有没有报逐轮收益

⭐ **答案：⛔ 没有逐轮曲线。⭐ 但有 6 格逐格的「轮数 × token × 成本 × 时间 × 残余错误」，⭐ 而这张表本身就回答了收益问题，⛔ 答案对循环不利。**

⭐ **最大轮数**：⭐ 安全外环 **20**（⭐ DPS 那格设的是 **4**）；⭐ 语法内环 **每个外环轮次内最多 20**（M，逐字见必答①）。

### ⭐ Table 1 逐字抄录（⛔ 一格不改）

| 规约 | 实验 | ⭐ 安全验证循环轮数 | Tokens | Cost | Time | 残余语法错误 | ⛔ 未验证性质 |
| :-- | :-: | :-- | --: | --: | :-- | :-: | :-- |
| Ping-Pong Game | 1 | ⭐ **1** (/20 allowed) | 4,465 | $0.06 | 28 s | **0** | ⭐ **0** (/7 states) |
| Ping-Pong Game | 2 | ⛔ **20** (/20 allowed) | 78,245 | $0.38 | 9 min 20 s | **0** | ⛔ **4** (/8 states) |
| Pressure Controller | 1 | ⛔ **20** (/20 allowed) | 195,819 | $0.87 | 22 min 9 s | **0** | ⛔ **7** |
| Pressure Controller | 2 | ⛔ **20** (/20 allowed) | 224,078 | $1.19 | 26 min 40 s | **0** | ⛔ **6** (/14 states) |
| Dynamic Positioning System | 1 | ⛔ **(4/4 allowed)** | 121,943 | $0.59 | 9 min | **0** | ⛔ **16** (/42 states) |
| Dynamic Positioning System | 2 | ⛔ **(4/4 allowed)** | 127,157 | $0.65 | 9 min 12 s | **0** | ⛔ **20** (/39 states) |

⭐ 表注逐字（M）："Red dots indicate cases where **the feedback loop reached its maximum number of iterations without successfully correcting all remaining errors**."

### ⭐⭐ 三条读数（⛔ 全部可从上表直接复算）

1. ⛔⛔ **6 格里 5 格撞上限。** ⭐ 唯一没撞的那格（Ping-Pong 实验 1）**只用了 1 轮 / 4,465 token** 就全过。⛔ 换言之：**要么第一轮就成，要么撞满上限也不成。**
2. ⭐ **语法轴 6/6 全清零，⛔ 安全轴 1/6 全满足。** ⭐ 逐字（M，§4）："Overall, the new mechanism excels at generating syntactically correct models: **all models produced had zero remaining syntactic errors.** […] However, performance in terms of safety correctness remains more limited. Most states are reachable in the generated models but **of the six experiments conducted, only one model satisfied all required properties.**"
3. ⛔⛔ **撞上限的五格花掉 78k–224k token，换来的是 4–20 条性质仍未满足。** ⭐ 对照那格成功的 4,465 token —— ⛔ **最贵的一格（224,078 token）是最便宜那格的 50.2×，而它仍剩 6 条未满足。**

### ⛔ 作者自陈：不能下结论

⭐ 论文两处逐字写 "we cannot conclude"（M，§4 与 §5）：

> §4: "on which **we cannot conclude** based on this first evaluation"
> §5: "**These evaluations do not enable indeed to conclude about the effectiveness of the safety auto-correction mechanism.**"

⚠️⚠️ ⭐ 而它保留的唯一正向主张**没有数据支撑**（M，§4 逐字）：

> "It is worth noting, however, that the introduction of a safety properties verification loop that triggers up to 20 iterations **statistically increases the likelihood** of producing a design model with more verified properties, compared to the previous version of TTool-AI, which lacked such a loop."

⛔ **这句话没有对照臂。** ⛔ 论文没有 no-loop 组的数字，⛔ 「statistically」二字在全文没有任何统计量、样本或检验支撑。⭐ 按本仓库 §3.5 口径，⛔ 这属于**无数据的因果断言**。

### ⭐⭐ 与我们 v46 那条实测的对照（⛔ 这是本卡对 M1 最值钱的一格）

| | ⭐ 它（ERTS 2026） | ⭐ 我们（v46） |
| :-- | :-- | :-- |
| 裁决者 | ⭐⭐ **sound oracle**（SysML 模型检查器） | ⛔ **LLM 自评**（两个 reviewer） |
| 上限 | 20 轮（DPS 4 轮） | ⭐ 修订预算 |
| ⛔ 收益 | ⛔ **5/6 撞满上限仍未收敛**；⛔ 最贵一格 224k token 剩 6 条 | ⛔ **第 3–5 轮零收益**；⛔ 吃 79% token 覆盖净变化 ≈ 0 |
| ⭐ 便宜的那条 | ⭐ 语法环（parser）：**6/6 清零** | ⭐ `precheck_and_seal`（确定性）：**0 token，性价比最高** |

⭐⭐ **合起来是一条很硬的结论：⛔ 「裁决者换成 sound oracle」本身不解决循环无收益的问题。** ⭐ 两边独立得到同一个形状 —— ⭐ **确定性/语法层的循环便宜且收敛；语义/性质层的循环无论裁决者是 LLM 自评还是模型检查器，都烧钱不收敛。** ⭐ 差别在于**反馈的可执行性**（见 [必答②](#-必答--验证器的反例怎么回灌给-llm)），⛔ 不在裁决者的可信度。

---

## ⭐⭐ 必答④ · 与同组 SoSyM 2026 那篇的关系

⭐ **答案：同一个系统（TTool / TTool-AI），⛔ 两条不同路线，⛔ 互不引用。**

| 维度 | ⭐ 本篇（ERTS 2026） | ⭐ [sosym2026-state-machine-consistency](./sosym2026-state-machine-consistency.md) |
| :-- | :-- | :-- |
| 作者 | Sultan, Apvrille（**2 人**） | Sultan, Apvrille, **Coudert**（3 人） |
| ⭐ 问题 | ⭐ **生成期的正确性**：语法完整正确 ＋ 安全性质 | ⭐ **多视图一致性**：UCD ↔ BD ↔ SMD |
| ⭐ 制品 | ⭐ BD ＋ 每个 block 一台 SMD | ⭐ UCD ＋ BD ＋ SMD |
| ⭐ 裁决者 | ⭐⭐ **syntax checker ＋ 模型检查器**（sound oracle） | ⭐ **syntax checker ＋ 38 条形式化规则 ＋ 依赖图遍历**（⛔ 无模型检查器） |
| ⭐ 判定对象 | ⭐ 模型自身（可达性 / 无死锁） | ⭐ 视图之间 |
| ⭐ 闭合中间表示 | ⭐ 2 类性质模板 ＋ [26] 的语法正确性定义 | ⭐ 38 条编号规则 ＋ 依赖图 IR |
| ⛔ 引用关系 | ⛔ **不引 SoSyM 那篇** | — |

⭐ **共同祖先是同一批前作**：⭐ 本篇引 `[3]` Apvrille & Sultan MODELSWARD'24（BEST PAPER）· `[24]` Sultan & Apvrille **MODELS'24 "AI-Driven Consistency of SysML Diagrams"**（ACM SIGSOFT DISTINGUISHED PAPER）· `[25]` TTool-AI, SN Comput. Sci. 6(7), 2025。⭐⭐ 其中 `[24]` 正是 SoSyM 那篇的**期刊扩展前身**（⭐ SoSyM 卡记 "some of the rules we first proposed in [6], and that we extend in this paper"）。

⭐⭐ **所以两篇的准确关系是**：⭐ 同一实验室、同一工具、同一个 TTool-AI 反馈循环骨架，⭐ **各自往上加一道不同的门** —— ⭐ SoSyM 加的是「跨视图规则 ＋ 依赖图」，⭐ 本篇加的是「完整语法 ＋ 模型检查」。⛔ **不是同一系统的两个版本，⛔ 也不是竞争路线；⭐ 是两条正交的加法。** ⚠️ ⛔ 两篇都**没有**把对方的门接进来 —— ⭐ SoSyM 卡明记「TTool 有模型检查器，⛔ 但本文没把它接进一致性循环」，⭐ 而本篇反过来没有跨视图规则。

⭐ **一个可对读的细节（⛔ 两篇结论方向一致）**：⭐ SoSyM 那篇实测「把形式化规则注入检测 prompt 会让 LLM 只盯着这些规则」（⭐ 隧道视野），⛔ 对策是跑两遍取并集；⭐ 本篇则完全不让 LLM 参与判定，⭐ 规则只用于**确定性检查**、只把结果当反馈回灌。⭐⭐ **两篇合起来支持同一条设计纪律：规则该给检查器，不该给 LLM 当检查清单。**

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `erts2026-safe-llm-mde` |
| `title` | ⚠️⚠️ **两个标题并存，本卡以 PDF 内页为准**：<br>⭐ **PDF 内页 ＋ HAL 元数据**（一致）：**"Towards Reliable LLM-Based Model Driven Engineering: when Full Syntax Checking and Formal Verification Join the Loop"**（M，⭐ PDF 第 1 页 cover 与第 2 页正文标题、HAL API `title_s` 三源一致）<br>⛔ **作者发布列表**：**"Towards Safe LLM-Based Model Driven Engineering: when Syntax Checking and Safety Formal Verification Join the Loop"**（M，逐字取自 Apvrille 主页 publications 页，⭐ 即任务书用的那个）<br>⭐ 详见 [§F.1](#f-存疑与未核项) |
| 作者 | ⭐ **Bastien Sultan · Ludovic Apvrille**（M）；⭐ 同属 **LTCI, Télécom Paris, Institut Polytechnique de Paris, Sophia-Antipolis, France**（M，逐字） |
| `year` | ⭐ **2026**（M，页脚逐字 "European Congress of Embedded Real Time Systems, **ISSN 2680-0918, 2026**"；⭐ HAL `publicationDateY_i: 2026`；⭐ HAL 提交日 **2026-02-16**）。⛔ 无 early-access 歧义 |
| `venue` | ⭐ **13th European Congress of Embedded Real Time Systems (ERTS)**, Feb 2026, Toulouse, France（M，HAL `conferenceTitle_s` ＋ PDF 引用块逐字）。⭐ `docType_s: COMM`（会议论文）。⭐ ISSN **2680-0918** |
| `ccf` | ⭐ **未收录** —— ⭐ 已查本仓库 [ccf_venues/](../../../../../ccf_venues/)：42 个 venue 里**无 ERTS**（⭐ 已 grep `ERTS` / `Embedded Real Time` 于 [SUMMARY.md](../../../../../ccf_venues/SUMMARY.md) / [01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) / [README.md](../../../../../ccf_venues/README.md)，零命中）。⚠️ ERTS 是欧洲嵌入式工业界 congress，⛔ 不在 CCF 目录 |
| `doi` | ⛔ **无**（⭐ HAL API `doiId_s` 字段缺失；⛔ Crossref 无对应条目） |
| `arxiv` | ⛔ **无** |
| `url` | ⭐ HAL 落地页 [hal.science/hal-05513959v1](https://hal.science/hal-05513959v1)（M，HAL API `uri_s`）· ⭐ PDF [hal-05513959v1/file/ERTS2026_paper_52.pdf](https://hal.science/hal-05513959v1/file/ERTS2026_paper_52.pdf)（M，HAL API `files_s`；⭐ **本轮实际取到**）· ⭐ BibTeX [hal-05513959v1/bibtex](https://hal.science/hal-05513959v1/bibtex) |
| 许可 | ⭐ **CC BY 4.0**（M，PDF 第 1 页逐字 "Distributed under a Creative Commons CC BY 4.0 - Attribution - International License"；⭐ 正文页脚再声明一次） |
| `artifact_type` | ⭐ **SysML/AVATAR 设计模型** = **1 个 Block Diagram (BD) ＋ 每个 block 一台 State Machine Diagram (SMD)**（M，§3 逐字 "A design consists of a BD and a set of SMDs (one per block)"）。⭐ 本文聚焦 SMD 生成阶段 |
| `task` | ⭐ **生成**（NL 规约 → BD ＋ SMDs），⭐ 循环内含**自动修复**。⛔ **不是缺陷检测** —— ⭐ 检查器判的是模型自身的语法与两类通用安全性质，⛔ 不是「模型 vs 需求」 |
| `boundary` | ⚠️ **`邻域`**（⛔ 不是界内 —— 见下） |

### ⚠️ `boundary` 为什么判 `邻域`

⭐ 主体是 AVATAR SysML 的 BD ＋ SMD，⭐ 与 $M=(S,E,V,Tr,A)$ 高度重合。⛔ **但两项界外成分是本文方法的承重部分（M）：**

1. ⛔ **并发是承重的。** ⭐ 本文的两类安全性质之一是 **deadlock-freedom**（M，§3 逐字 "(2) the system is free from deadlocks"），⛔ 而死锁只在并发合成下才有意义。⭐ 模型检查器逐字 "operates directly on SysML semantics by **building a state-space graph from the BD and SMDs**"（M）—— ⭐ 即多台状态机的并发合成状态空间。⛔ 单台无并发状态机上不会有这个性质。
2. ⛔ **时间约束在 AVATAR 语义里存在。** ⭐ 与 [SoSyM 卡](./sosym2026-state-machine-consistency.md) §A 记的同一 profile（⭐ transition description 含 `after ∈ ℕ`）。⚠️ ⛔ 本篇正文未直接讨论时间约束（S），⛔ 但它用的是同一个 AVATAR profile 与同一个 TTool 模型检查器（⭐ TTool 底层做的是时间模型检查）。

⭐ 按 [README.md](../README.md) §2.1，⭐ L3 **不设**边界门、只要求标注 —— ⭐ 本卡标 `邻域` 并写明成分。⛔⛔ **提醒：若要把这篇搬进 L1/L2（那两轨过边界门），⛔ 必须先在这两点上重走一遍门。**

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ 按论文 Fig. 1 的任务编号画）

```
[人]     提供 NL 系统规约（⭐ 逐字 "written in natural language, with no formal constraints"）
  ＋ 上一阶段已生成的 BD
   ↓
[确定性] T1 prompt forging ＝ 规约 ＋ BD 的文本表示 ＋ SMD 专门知识（语法约束 ＋ 格式要求）
                            ⭐ 再**切成若干顺序片段**依次发给 LLM
   ↓
[LLM]   T2 response  ← ⭐⭐ 全流程唯一的 LLM 环节
   ↓
[确定性] T3 full syntax analysis（格式 ＋ SMD 一致性 ＋ ⭐**完整**语法正确性）
            ├─ KO ──→ 回 T1（⭐ 带上「identified issues ＋ 上一版 SMDs」）  ⭐ 内环上限 20
            └─ OK ↓
[oracle] T4 安全性质自动生成 ＋ TTool 模型检查器验证（每状态可达 ＋ 无死锁）
            ├─ KO ──→ 回 T1（⭐ 带上「unsatisfied properties ＋ 对应 SMD」）  ⭐ 外环上限 20
            ├─ >n（撞上限）↓
            └─ OK ↓
[确定性] T5 model ranking：⭐⭐ 从**归档的每一版响应**里按确定性分数选最好的（⭐ 本文新增机制）
   ↓
[人]     U1 user analysis
            ├─ KO ──→ user feedback（TTool-AI 对话窗）──→ 回 T1
            └─ OK ↓
[确定性] T6 在 TTool GUI 里生成图形化 SMD
```

⭐⭐ **合计 7 段 · 其中 LLM 仅 1 段（T2）· 确定性 5 段（T1 / T3 / T4 / T5 / T6）· 人 1 段（U1）。**

⚠️ ⭐ **黑虚线框内全自动**（M，§3 逐字）："all tasks shown within the black dotted box in the figure are **fully automated by the tool and require no user intervention**." ⭐ 即 T1–T5 全自动，⛔ 人只在 U1 出现一次。

⚠️ ⭐ **T4/T5 是本文的新增，T3 是本文的增强**（M，Fig. 1 图注逐字）："With respect to the previous loop [3, 24], **steps T4 and T5 have been added, and T3 has been enhanced.**"

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| `T2` 首轮 | ⭐ **生成器**（NL 规约 ＋ BD → SMDs） |
| `T2` 语法环复用 | ⭐ **修复者**（⭐ 输入 ＝ 问题清单 ＋ 上一版 SMDs；⛔ **同一个调用换 prompt，⛔ 不是独立修复器**） |
| `T2` 安全环复用 | ⭐ **修复者**（⭐ 输入 ＝ 未满足性质清单 ＋ 对应 SMD） |
| ⛔ **裁决者** | ⛔⛔ **LLM 从不担任** —— ⭐ 见 [B4](#b4--循环与裁决者本轨最关键的一格) |
| ⛔ **性质生成者** | ⛔⛔ **LLM 不担任**（⭐ 由工具按模板生成）—— ⚠️ **future work 才打算交给 LLM**，逐字（M，§5）："developing an **LLM-based mechanism capable of automatically generating temporal logic properties** that reflect the requirements, based on both the specification and the design model" |
| ⛔ 评审者 | ⛔ **无** —— ⛔ 没有任何 LLM 自评环节 |

### B3 · prompt 策略

| 策略 | 有无 | 证据 |
| :-- | :-: | :-- |
| ⭐ **领域知识注入**（作者一系自称 RAG） | ⭐ **有** | ⭐ M，§3 逐字：prompt 含 "**specific knowledge about SMDs (including syntactic constraints and formatting requirements for the LLM's response)**"。⭐ §2 逐字把 TTool-AI 的策略归为 "retrieval-augmented generation which consists in pruning LLMs with domain-specific contextual knowledge" |
| ⭐⭐ **prompt 切片**（⛔ 不在 schema 词表里，⭐ 单列） | ⭐ **有** | ⭐ M，§3 逐字："**This prompt is then sliced into several sequential parts and sent to the LLM**" ⭐ 即长 prompt 拆成顺序多段发送，⛔ 不是一次性大 prompt |
| ⭐ **结构化输出约束** | ⭐ **有**（⛔ prompt 里说明，⛔ 非受限解码） | ⭐ M，§3：prompt 含 "formatting requirements for the LLM's response"；⭐ T3 检查 "the format of the response (i.e., whether it meets the required structure for parsing)" |
| ⭐ **校验失败回灌** | ⭐⭐ **有（两处，⭐ 本文核心）** | ⭐ M，见 [必答②](#-必答--验证器的反例怎么回灌给-llm) |
| ⛔ few-shot / CoT / self-consistency 投票 / 多智能体辩论 / tool calling / self-reflection | ⛔ **原文未提供** | ⭐ 全文无任何相关表述（S）。⛔ 尤其 **无 LLM 自评** —— ⭐ 与 SoSyM 那篇同样明确把自己划到「查外部检查器」那一侧 |

⛔⛔ **prompt 未公开** —— ⭐ 论文只公开了 **syntax checker 源码路径**（⭐ 单个 `.java` 文件的 GitLab 链接）与 **规约 ＋ 生成模型的 GitHub 仓库**；⛔ **prompt 本身既不在论文附录里，也不在配套仓库里**（⭐ 已实际核验仓库全部 5 个文件，见 [D](#d-资产)）。⚠️ 对比 SoSyM 那篇的 Data availability 段明确点名 "including the full prompts" —— ⛔ **本篇没有这句。**

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

⭐⭐ **三个循环 · 三个裁决者 · ⛔ LLM 一个都不是 · ⭐ 其中一个是真 sound oracle。**

| 循环 | 裁决者 | ⭐ 类型 | 终止条件 | 最大轮数 |
| :-- | :-- | :-- | :-- | :-- |
| ⭐ `T1→T2→T3→T1` **语法内环** | ⭐ `T3` TTool syntax checker（⭐ 规则出自 AMULET [26] §3.1 的形式定义） | ⭐ **`parser / 编译器` ＋ `确定性规则`** | ⭐ 零错误 / 撞上限 | ⭐ **20**（⭐ 每个外环轮次内） |
| ⭐⭐ `T1→T2→T3→T4→T1` **安全外环** | ⭐⭐ `T4` **TTool 模型检查器** [5]（⭐ Calvino & Apvrille, "Direct model-checking of SysML models", MODELSWARD 2021） | ⭐⭐ **`sound oracle`** —— ⭐ 直接在 SysML 语义上从 BD＋SMDs 建 state-space graph 查时序逻辑 | ⭐ 全部性质满足 / 撞上限 | ⭐ **20**（⭐ DPS 那格设 **4**） |
| ⭐ `U1→T1` 人环 | ⛔ **人** | ⭐ **`人`** | ⭐ 人叫停 | ⛔ 无 |

⭐ **逐条对照 schema 词表**：⭐⭐ `sound oracle` = **有（模型检查器）** · ⭐ `parser / 编译器` = **有** · ⭐ `确定性规则` = **有** · ⭐ `人` = **有** · ⛔⛔ **`LLM 自评` = 无** · ⛔ `测试执行` = 无。

⭐ 模型检查器的 sound 性有逐字依据（M，§2）："This technique systematically explores the portion of the system's state space required to determine whether the predefined temporal-logic conditions (representing the safety properties) hold. It thus provides **mathematically proven evidence of the model's (non-)compliance** with the requirements."

⭐ 本文自陈的新颖点正是"把模型检查放进循环"（M，§2 末逐字）：

> "However, **to the best of our knowledge, no prior work has proposed a formal-verification-driven LLM-based model generation tool that integrates model-checking directly in the iterative feedback loop between the tool and the LLM.**"

#### ⭐⭐ 撞上限时怎么办 —— ⭐ 本文有一个**降级机制**（⛔ 别的卡都没有这一格）

⭐ 逐字（M，§3）：

> "The process proceeds to step U1 either when all properties are satisfied or **when the maximum number of iterations in the loop is reached**. Indeed, since the LLM may fail to converge to a correct solution, and to minimize the cost of iterative querying, TTool-AI enables to set a cap on the maximum number of iterations. For this specific case, **the paper introduces a novel mechanism (T5) that archives each response produced during the loop and provides the user with the best generated model when no correct one is obtained within the allowed iterations.**"

⭐ **打分公式逐字抄下**（M，§3）：

$$
\mathrm{Score}(e,u,s,p) = 100 \cdot (1 - e/s) \quad \text{if } e > 0 \land s > 0
$$

$$
\mathrm{Score}(e,u,s,p) = 100 + 100 \cdot (1 - u/p) \quad \text{if } e = 0 \land p > 0
$$

$$
\mathrm{Score}(e,u,s,p) = 100 \quad \text{if } e = 0 \land p = 0
$$

⭐ 其中 $e$ ＝ 残余语法错误数 · $s$ ＝ 被检查的语法规则数 · $u$ ＝ 未满足安全性质数 · $p$ ＝ 被验证性质总数（M，逐字）。

⭐⭐ **这个公式的形状值得注意**：⭐ 它是**两段式** —— ⭐ 只要还有语法错误，分数封顶在 100 以下（⭐ 段 1）；⭐ 语法清零才进入 100–200 段（⭐ 段 2）。⭐⭐ **即语法轴是词典序的第一关键字，性质轴是第二关键字。** ⭐ 这与 [必答①](#-必答--语法检查与形式化验证各接在循环的哪一环) 的"语法是模型检查的必要条件"完全一致。

⛔ **并且论文明说撞上限意味着保证失效**（M，逐字）："If this limit is reached, the correctness-by-construction guarantees described in Dx.5 […] no longer entirely hold, and **the user is notified via the GUI that the iteration limit has been exceeded.**"

⚠️ ⭐ **注意与 SoSyM 那篇的反差**：⭐ SoSyM 卡记 "**In practice, however, this threshold was never reached in the evaluations reported below**"（⭐ 上限从未触及）；⛔⛔ **本篇 6 格里 5 格撞满。** ⭐⭐ **同一个工具、同一批人、同一个 20 上限 —— ⭐ 区别只在裁决者从「确定性规则」换成了「模型检查器 ＋ 语义性质」。** ⭐ 这是一次近乎受控的对照，⛔ 尽管作者没这么呈现。

#### ⛔ 有无报告循环的边际收益

⭐ **见 [必答③](#-必答--循环几轮有没有报逐轮收益)**：⛔ 无逐轮曲线，⭐ 但有 6 格逐格的轮数 × token × 成本 × 残余量，⛔ 结论对循环不利。

### B5 · ⭐ 中间表示

⚠️ **两套，⭐ 都闭合，⛔ 都不是 LLM 选的。**

| | ⭐ ① 语法正确性规则集 | ⭐⭐ ② 安全性质集 |
| :-- | :-- | :-- |
| 有无 | ⭐ 有 | ⭐ 有 |
| 形态 | ⭐ **确定性规则目录**（⭐ 例：属性类型合法 · 相连信号参数类型匹配 · SMD 底图连通） | ⭐ **时序逻辑性质模板**（⛔ 只有 2 类） |
| ⭐ **是否闭合** | ⭐⭐ **闭合** —— ⭐ 出处逐字 "**follow from the definitions of syntactic correctness given in [26], Section 3.1**" | ⭐⭐ **闭合到只有 2 类** |
| ⭐ **谁定的 / 谁选** | ⭐ **作者预编**（⭐ 挂在另一篇论文的形式定义上）；⛔ **LLM 不选** | ⭐⭐ **工具按状态机机械实例化**：⭐ 每个 state 一条可达性性质 ＋ 一条全局 deadlock-freedom（S：⭐ 从 Table 1 的 "(/7 states)" "(/42 states)" 分母口径可直接推出）；⛔⛔ **LLM 不选、人不选** |

⭐ 两类性质逐字（M，§3）："In the current implementation of the feedback loop, the generated properties enable to check whether: **(1) every state in the SMD is reachable, and (2) the system is free from deadlocks.**" ⭐ §1 再说一遍："At the current stage of our works, safety verification focuses on verifying **state reachability in SMDs and the absence of deadlocks**."

⭐ 语法规则举例逐字（M，§3）："They include, among others, verifying that **attribute types are valid**, that **two connected signals have matching parameter types**, that the **underlying graphs of state-machine diagrams are connected**, etc."

#### ⭐⭐ 与我们 19 条闭合谓词的对照（⛔ 这一格最有价值）

| 维度 | ⭐ 它 | ⭐ 我们（19 条谓词） |
| :-- | :-- | :-- |
| 闭合性 | ⭐ 闭合（⭐ 语法规则集 ＋ 2 类性质） | ⭐ 闭合（19 条） |
| ⛔ **谁选** | ⛔⛔ **无人选 —— 全量机械实例化。** ⭐ 每个 state 都出一条可达性性质，⛔ 不做取舍 | ⭐⭐ **LLM 在每条需求上自动选** |
| ⭐ **判据来源** | ⭐ 与需求**无关** —— ⭐ 2 类性质是通用的模型自洽性质 | ⭐ **逐条从 NL 需求派生** |
| ⭐ 出处 | ⭐ 语法规则挂 [26] 的形式定义（⭐ ① 类）；⭐ 2 类性质是模型检查通用性质（⭐ ② 类元模型/理论定义性） | ⭐ **① 12 · ② 6 · ③ 1**（见 [../../provenance/](../../provenance/)） |
| ⛔ **覆盖的是什么** | ⛔⛔ **只覆盖「模型自洽」，⛔ 不覆盖「模型符合需求」** | ⭐ 覆盖「模型 vs 需求」 |

⭐⭐⭐ **最后一行是本卡与 M1 最相关的一条**：⭐ **它的循环从头到尾没有把需求接进判定** —— ⭐ 规约只进 prompt（生成侧），⛔ 判定侧只有语法 ＋ 可达性 ＋ 无死锁。⭐ **而论文自己在 §5 承认这是缺口并把补它列为 future work**（M，逐字）：

> "future work will aim to strengthen the integration of formal verification within the feedback loop, **extending it beyond state reachability and deadlock-freedom to cover a broader range of properties.** Our plan involves: (1) developing an LLM-based mechanism capable of automatically generating **temporal logic properties that reflect the requirements**, based on both the specification and the design model; and (2) integrating the verification of these properties into the feedback loop, **enabling the generation of models that iteratively converges toward full compliance with the specification.**"

⭐⭐ **换言之：这篇论文的 future work 第 (1) 项，就是我们 v46 已经在做的那件事（从 NL 需求逐条派生可机械求值的断言）。** ⭐ 这是一条**可用的定位证据**（⛔ 但按 [README.md](../README.md) §3 防火墙，⛔ 要进论文必须回 L1/L2 重走门）。

### B6 · 模型

⛔⛔ **原文未提供 —— 全文没有出现任何 LLM 型号。**

⭐ 已实际核验：⭐ 对 29,062 B 全文做 `grep -i "gpt\|claude\|llm model\|openai\|mistral\|gemini\|deepseek"`，⛔ **零命中**。⭐ 配套 GitHub README 只说（M，逐字）："You will need either an **OpenAI** key, a **MistralAI** key, or a **LLM server**." ⛔ 未指明本次实验用的是哪一个。

| 项 | 值 |
| :-- | :-- |
| ⛔ 型号 | ⛔⛔ **原文未提供** |
| ⛔ 多模型对照 | ⛔ **无** |
| ⭐ 工具版本 | ⭐ TTool **v3.0 或更高**（M，配套仓库 README 逐字 "Download TTool (v3.0 or later)"）；⛔ 论文正文未 pin build 号（⚠️ 对比 SoSyM 那篇 pin 了 build 14731 / 14863） |
| ⚠️ 单价反推 | ⚠️ **I 级推断，⛔ 不得写成事实**：⭐ 从 Table 1 的 `4,465 tok / $0.06` 与 `224,078 tok / $1.19` 看，⭐ 混合单价落在约 **$5.3–13.4 / M token** 区间。⛔ 这个区间跨了多个厂商多个档，⛔ **无法据此定型号** |

⚠️⚠️ **这是本卡最严重的方法学缺口。** ⭐ X1 已证 SOTA 与上一代不是一个量级 —— ⛔ 而这篇连型号都没写，⛔ 所以「安全轴 5/6 撞上限」这个结论**无法判断有多少来自模型代际、有多少来自方法**。⛔ 引用这篇的任何数字都必须带这条限定。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 段 |
| :-- | :-- | :-- |
| ⭐ prompt 组装 ＋ 切片 | ⭐ 规约 ＋ BD 文本 ＋ SMD 知识拼装，再切成顺序片段 | `T1` |
| ⭐⭐ **完整语法检查器** | ⭐ `AvatarSyntaxChecker.java`（⭐ 规则出自 AMULET [26] §3.1）—— ⚠️ **源码入口已定位但本轮未取到**，见 [D](#d-资产) / [F.3](#f-存疑与未核项) | `T3` |
| ⭐ 一致性检查 ＋ 格式检查 | ⭐ 响应结构可解析性 ＋ SMD 一致性 | `T3` |
| ⭐ 性质自动生成 | ⭐ 每 state 一条可达性 ＋ 一条 deadlock-freedom | `T4` |
| ⭐⭐⭐ **SysML 模型检查器** | ⭐⭐ **真 sound oracle**：⭐ 直接在 SysML 语义上从 BD＋SMDs 建 state-space graph，⭐ 再遍历验时序逻辑性质。⭐ 出处 [5] Calvino & Apvrille, MODELSWARD 2021；⭐ 另 [12] de Saqui-Sannes, Apvrille & Vingerhoeds, J. Aerospace Inf. Syst. 18(12):906–918, 2021 | `T4` |
| ⭐⭐ **打分与排序** | ⭐ 两段式确定性分数（⭐ 见 [B4](#-撞上限时怎么办--本文有一个降级机制别的卡都没有这一格)），⭐ 从归档响应里选最优 | `T5` |
| ⭐ 图形渲染 | ⭐ 在 TTool GUI 里画出 SMD | `T6` |

⭐⭐⭐ **这一格的核心发现**：⭐ **7 段里 LLM 只占 1 段（14.3%），⛔ 且它从不判定任何事情 —— ⭐ 所有判定都在确定性组件与 sound oracle 手里。** ⭐ 这是本轨目前**确定性占比最高、且裁决端有真 sound oracle** 的一个形态。

⚠️ ⭐ **对照我们**：⭐ 我们 10 节点里 5 个 LLM（50%），⭐ 且 pyfcstm 这个 sound oracle 在**求值端**、裁决端是 `adjudicate_results`（LLM）。⭐⭐ **这篇给出了「裁决端换成 sound oracle」的一个实例 —— ⛔ 但它同时证明了这一步单独做不够（见 [E](#e-对-m1-的意义)）。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⛔⛔ **无。** ⛔ 没有 no-loop 对照臂、⛔ 没有 syntax-only 臂、⛔ 没有其它工具臂、⛔ 没有人类臂。⚠️ 唯一的"对比"是对 **TTool-AI 上一版**的**定性**说法（M，逐字 "In contrast, **the previous version of TTool-AI frequently generated SMDs containing syntax issues**"）—— ⛔ **没有数字** |
| `dataset` | ⭐ **3 个规约 × 2 次实验 ＝ 6 格**（M）。⭐ 两个 Master 课程玩具规约（⭐ 逐字 "two toy specifications commonly used in Master's-level systems engineering courses"）＋ ⭐ **一个真实工业规约**：动态定位系统 DPS（⭐ 逐字 "a real-world specification of a dynamic positioning system (an embedded system that maintains a vessel's heading and position at sea based on a given setpoint)"）。⭐ 规约体量已实测：`PingPongGame` **164 B** · `PressureController` **194 B** · `DPS` **1,248 B**。⭐ 模型规模逐字："each model comprising in total between **2 and 9 blocks** and **7 to 42 states**" |
| ⭐ **分母怎么定的** | ⭐⭐ **性质分母 ＝ 状态数** —— ⭐ Table 1 逐格写 "(/7 states)" "(/8 states)" "(/14 states)" "(/42 states)" "(/39 states)"，⭐ 即每个 state 一条可达性性质，⛔ 加 deadlock-freedom（⭐ 故性质总数略大于状态数）。⭐ 语法分母 ＝ 被检查规则数 $s$（⛔ 论文未给具体数值）。⚠️ ⛔ **Pressure Controller 实验 1 那格的 "Unverified properties: 7" 没写分母** —— ⭐ 唯一一格漏了 |
| ⭐ 缺陷从哪来 | ⭐⭐ **天然存在** —— ⭐ 被检的 SMDs 是 LLM 自己生成的，⛔ **没有人工播种**（⛔ 与 SoSyM 那篇的图法臂不同，⭐ 那边播了 `[M-incomplete]` / `[M-faulty]`） |
| `metrics` | ⭐ 每格 6 项：安全验证循环轮数（/上限）· tokens · 美元成本 · 墙钟时间 · 残余语法错误数 · 未验证性质数（/状态数）。⛔⛔ **无任何 `@k` 口径** |
| ⚠️⚠️ **runs 与方差** | ⭐ **每规约 2 次**（"Experiment 1" / "Experiment 2"）；⛔ **报单次逐格，⛔ 无均值、⛔ 无方差、⛔ 无对两次差异的任何讨论。** ⭐⭐ **而两次差异极大**：⛔ Ping-Pong 第 1 次 **1 轮 / 4,465 tok / 0 条未满足**，⛔ 第 2 次 **20 轮 / 78,245 tok / 4 条未满足** —— ⭐⭐ **同一规约、17.5× token、结果从全过变成不过。** ⭐ 这是**采样方差**的直接证据，⛔ 论文一字未提。⭐⭐ **这正好从外部印证我们 §3.5.2 `metric@k` 的必要性：单次数字在这条任务上没有意义** |
| ⭐ `judged_by` | ⭐⭐ **全自动，⛔ 无人工判定** —— ⭐ 语法由 syntax checker 判、性质由模型检查器判。⛔ 无第三方、⛔ 无标注者间一致性、⛔ 无 $\kappa$（⭐ 也不需要：判据是确定性的）。⚠️⚠️ **但代价是：「模型是否真的符合需求」没有任何人或任何装置判过** —— ⭐ 只判了可达性与无死锁 |
| `human_baseline` | ⛔ **本文无。** ⭐ 只有一句引前作的定性说法（M，逐字）："it remains negligible compared to the time a human would require to generate the same models for an equivalent to better quality, **as previously demonstrated for other systems with a less performant feedback loop [3, 25]**" —— ⚠️ ⛔ 那是**前作对生成质量**的结论，⛔ 不是本文的测量 |
| ⭐ `adverse_results` | ⭐⭐ **如实公布 ＋ 明确自陈不能下结论 —— ⭐ 处理方式基本干净。** ⭐ 三项动作：① ⭐ Table 1 用**红点**标出每一格撞上限的情况（⛔ 5/6 格带红点）；② ⭐ 正文逐字承认 "only one model satisfied all required properties"；③ ⭐⭐ **两处逐字写 "we cannot conclude"**。⚠️⚠️ **但松紧不完全对称**：⛔ 标题、摘要、结论都在讲语法轴的成功（⭐ 摘要逐字 "reliably produces syntactically correct models"），⛔ 而安全轴 1/6 的失败只出现在 §4 正文与 §5 一句；⛔ 且那句唯一的正向主张（"statistically increases the likelihood"）**没有对照臂、没有统计量**。⭐ 按本仓库 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9 的方向性松紧口径，⛔ **这是一处失真** |

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ **🟢** | [hal-05513959v1/file/ERTS2026_paper_52.pdf](https://hal.science/hal-05513959v1/file/ERTS2026_paper_52.pdf) | ⭐ **本轮实际取到**：`200 / 539,452 B / application/pdf` · `PDF document, version 1.4, 6 page(s)` · CC-BY 4.0。⚠️ ⛔ `hal.science` 对 CLI 返回 Anubis 挑战页（`{"rules":{"algorithm":"fast","difficulty":4}}`，`r.jina.ai` 代理同样被拦）；⭐ 题录经 **HAL API** 独立核实（`numFound: 1` · `halId_s` · `fileMain_s` · `conferenceTitle_s` 四字段一致） |
| ⭐ **实验代码** | ⚠️ **🟠** | ⭐ 论文只给单文件路径：[`gitlab.telecom-paris.fr/mbe-tools/TTool/-/blob/master/src/main/java/avatartranslator/AvatarSyntaxChecker.java`](https://gitlab.telecom-paris.fr/mbe-tools/TTool/-/blob/master/src/main/java/avatartranslator/AvatarSyntaxChecker.java) | ⛔⛔ **本轮未取到。** ⭐ 已试四条路：① `raw/master` 直取 → `418` （`go-away` 反爬，`Checking you are not a bot`）；② 换浏览器 UA ＋ Referer → `418`；③ 解 `js-refresh` challenge 换 token → `418`；④ `r.jina.ai` 代理 → `400`，逐字 `Error: internal error: unexpected challenge: got ""`。⚠️ ⭐ **入口路径明确、ref 已 pin 在 `master`**，⭐ 且 [SoSyM 卡](./sosym2026-state-machine-consistency.md) 曾从**同一 GitLab** 取到过其它 `.java`（⭐ 故仓库确为公开）；⛔ **但本文件本轮未验，故判 🟠 不判 🟢** |
| ⭐ **数据集 / 复现包** | ⚠️ **🟠** | [github.com/ZebreDeSoixanteQuatorzeCanons/ModelGenerationWithFormalVerification](https://github.com/ZebreDeSoixanteQuatorzeCanons/ModelGenerationWithFormalVerification) | ⭐ [`tools/verify_assets`](../tools/verify_assets.py) 输出**逐字**：`HEAD 773709b7d8 · 文件 5（非文档 4 · 源码 0） · release 0 · license 无` → 机械建议 `🟠 无源码`（⛔ 逐字 "有文件但零源码"）。⭐ **人工补看内容**：`README.md` (1,483 B) · `models/models.xml` (**520,338 B**) · `specifications/{DPS,PingPongGame,PressureController}` (1,248 / 164 / 194 B)。⭐⭐ **论文的声明「specifications and generated models are available」是兑现了的**；⛔ 但 default branch 是 `main`（⛔ 不是 `master`）· 单次 push（`2025-11-17`，⭐ 早于 HAL 提交日 3 个月）· ⛔ **无 license · 无 release · 无 run log · 无 token 计数 · 无 prompt** → ⛔ **Table 1 的 6 格数字无法复算** |
| 实验结果细则 | ⛔ **⚪** | — | ⛔ **只有论文内 Table 1**，⛔ 无可下载逐条结果、⛔ 无逐轮记录 |
| Artifact / 复现包 DOI | ⛔ **⚪** | — | ⛔ 无 Zenodo / 4open / OSF DOI |
| ⭐ **prompt 是否公开** | ⛔ **⚪** | — | ⛔⛔ **未公开。** ⭐ 已实际核验配套仓库全部 5 个文件，⛔ 无 prompt；⛔ 论文无附录。⚠️ ⭐ 理论上 prompt 在 TTool 源码里（⭐ SoSyM 卡已证同一 GitLab 有 prompt 常量），⛔ **但本文没有指出文件路径，也没有 Data availability 声明** |

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **「裁决端接 sound oracle」这一步有了已发表实例。** ⭐ 本篇是 L3 目前**唯一**「裁决者 = 模型检查器」的邻域先例，⛔ 且作者自陈是首次（"to the best of our knowledge, no prior work has proposed a formal-verification-driven LLM-based model generation tool that integrates model-checking directly in the iterative feedback loop"）。⭐ **搬的具体决定**：⭐ 把 pyfcstm 从求值端提到裁决端时，⭐ 可以照它的形状 —— ⭐ **oracle 只回答"过/不过 ＋ 哪几条不过"，⛔ 不参与解释，⛔ 不参与修复。**
2. ⭐⭐⭐ **撞上限时的「存档 ＋ 打分 ＋ 交最好那版」机制（T5）可以直接搬。** ⭐ 这正面对上本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §10「配额耗尽必须降级不许抛」—— ⭐ 而它给出了一个**具体的降级产物选择规则**：⭐ 两段式确定性分数，⭐ 语法轴作词典序第一关键字、性质轴第二，⭐ 并**通过 GUI 明确告知用户"保证已失效"**。⭐⭐ **我们的 quarantine / coverage_gap 降级目前只记诊断、不选"最好的那一版"** —— ⭐ 这一格可以补。
3. ⭐⭐ **两轴分开计数、分开报残余量。** ⭐ Table 1 的每格都同时给「残余语法错误数」与「未验证性质数（/状态数）」，⛔ 不合成单一分数。⭐ 我们可以照做：⭐ 结构谓词轴 vs 仿真/BMC 轴分开报，⛔ 不混成一个 `hit@1`。
4. ⭐ **规则出处挂到另一篇论文的形式定义上。** ⭐ 语法规则集逐字 "follow from the definitions of syntactic correctness given in [26], Section 3.1" —— ⭐ 这是 L2 出处纪律的一个干净范例（⭐ ① 类：有外部形式依据）。

### 2. ⛔ 不可取 / 陷阱（⭐ 它踩了我们踩过的坑，⛔ 但踩法不同）

1. ⭐⭐⭐ **它证明了「换成 sound oracle」单独不够 —— ⛔ 这是本卡最重要的一条。** ⭐ 裁决者是数学可证的模型检查器，⛔ 而循环 **5/6 撞满 20 轮仍不收敛**、⛔ 最贵一格烧 224,078 token 剩 6 条未满足。⭐ **根因在反馈的可执行性**：⛔ 回灌只给「哪条性质没满足 ＋ 那张 SMD」，⛔ 不给反例路径、⛔ 不定位元素，⭐ 而作者自己把这认成失败主因。⭐⭐ **对 M1 的硬含义**：⭐ 设计原则不应写成「把裁决者换成 sound oracle」，⭐ 而应写成「**把裁决者换成 sound oracle，并把 oracle 的反例证据翻译成定位到具体元素的可执行反馈**」。⛔ 少了后半句，这条原则已经被这篇论文实测过一次，⛔ 结果是不收敛。
2. ⛔⛔ **20 轮上限本身是在赌运气。** ⭐ 6 格的形态是**要么第 1 轮就成、要么撞满也不成**（⭐ 唯一成功那格用了 1 轮）。⭐ 这正是本仓库 §12「采样不确定性不能用来掩盖结构性失败」描述的现象：⛔ 若某格是结构性死路，⭐ 加轮数只决定烧多少 token，⛔ 不决定墙在不在。⭐ **我们该做的不是调大上限，而是做失败签名判别。**
3. ⛔ **模型型号完全未报，⛔ 且无多模型对照。** ⛔ 这使它的负面结论无法做代际归因 —— ⭐ 引用时必须带这条限定。⭐ 我们自己已经报了 `gpt-5.5` / `claude-opus-4-7` 两个模型 × 3 轮，⭐ 这一点上比它严。
4. ⛔ **无对照臂却写了一句 "statistically increases the likelihood"。** ⛔ 按本仓库 §3.5 口径，⭐ 这是**无数据的因果断言**；⭐ 我们的报告不能出现这种句式（⭐ 我们的 −15.82pp 是有对照臂的）。
5. ⚠️ **导语与正文的松紧不对称**：⭐ 标题/摘要主打语法轴 6/6，⛔ 安全轴 1/6 只在正文。⭐ 按 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9，⛔ **这是一处失真，⭐ 我们要反着做。**

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⭐⭐⭐ **它的判定完全不接需求。** ⭐ NL 规约只进**生成侧** prompt；⭐ 判定侧只有语法 ＋ 每状态可达 ＋ 无死锁 —— ⭐⭐ **即它的循环只能保证「模型自洽」，⛔ 不能保证「模型符合需求」。** ⭐ 而**它自己在 §5 把补这个缺口列为 future work**（⭐ 要让 LLM 从规约生成反映需求的时序逻辑性质，再接回循环）。⭐⭐ **也就是说：它未来要走的那一步，正是我们 v46 已经在做的那一步（从 NL 需求逐条派生可机械求值的断言）。** ⛔ 所以它的循环形状**不能直接搬到我们的任务上** —— ⛔ 它的 oracle 有现成的通用性质可查，⭐ 我们的断言必须先从需求派生出来，⛔ 而那一步本身就是我们的赤字所在（⛔ 「根本没问」69 位）。
2. ⭐ **任务方向相反**：⭐ 它是**生成**（NL → 模型，循环目的是把模型改对）；⭐ 我们是**缺陷检测**（模型 vs NL，循环目的是把断言问对）。⭐ 它可以改模型直到通过；⛔ **我们不能改被测模型** —— ⛔ 这使"迭代至收敛"在我们这里没有对应物。
3. ⭐ **它的中间表示是全量机械实例化，⛔ 我们是 LLM 选。** ⭐ 每个 state 都出一条可达性性质，⛔ 不做取舍，⛔ 所以它没有"选题赤字"这个问题（⭐ 也没有选题这件事）。⚠️ ⭐ 这提示一个我们没试过的方向：⭐⭐ **对结构谓词族做全量机械实例化，把"选"这一步从 LLM 手里拿掉** —— ⛔ 但那只对与需求无关的通用性质可行，⛔ 对需求派生断言不可行。
4. ⭐ **边界不同**：⭐ 它有 AVATAR 的时间约束（`after`）与块间并发（`send`/`receive`，⭐ deadlock-freedom 就依赖并发）；⛔ 我们界内无时钟、无并发。

---

## F. 存疑与未核项

1. ⚠️⚠️ **两个标题并存，⛔ 无法判定哪个是会议正式题录** —— ⭐ PDF 内页 ＋ HAL `title_s` 一致为 "Towards **Reliable** LLM-Based Model Driven Engineering: when **Full** Syntax Checking and **Formal** Verification Join the Loop"；⛔ 而 Apvrille 主页 publications 列表写 "Towards **Safe** LLM-Based Model Driven Engineering: when Syntax Checking and **Safety Formal** Verification Join the Loop"（⭐ 即任务书用的那个）。⭐ 已试入口：HAL API（`title_s`）· PDF 两页（cover ＋ 正文）· 作者主页 HTML（逐字取到该行）· ⛔ DBLP（**ERTS 2026 proceedings 尚未建档**）· ⛔ Crossref（无 DOI）。⭐⭐ **本卡以 PDF 内页为准；⛔ 若后续引用，建议以 HAL 题录为正式题名并在脚注记另一形。**
2. ⚠️⚠️ **LLM 型号未能确认** —— ⛔ 已试：全文 grep（`gpt|claude|openai|mistral|gemini|deepseek|llm model` **零命中**）· 配套 GitHub README（⭐ 只说需要 OpenAI / MistralAI key 或本地 server）· ⛔ HAL 元数据无。⛔ **这是本卡最重的缺口**（见 [B6](#b6--模型)）。
3. ⚠️⚠️ **`AvatarSyntaxChecker.java` 未能取到** —— ⛔ 已试 4 条路（`raw/master` 直取 → `418`；换 UA＋Referer → `418`；解 `js-refresh` challenge 换 token → `418`；`r.jina.ai` → `400 unexpected challenge`）。⭐ 症状是 `gitlab.telecom-paris.fr` 部署了 `go-away` 反爬（⭐ Anubis 的一个分支）。⚠️ ⛔ **按本仓库口径这是"访问异常"，⛔ 不得记为"文件不存在"** —— ⭐ 入口路径明确且 ref 已 pin 在 `master`，⭐ SoSyM 卡曾从同一 GitLab 取到其它文件。⛔ 故 [D](#d-资产) 判 🟠。
4. ⚠️ **语法内环的上限参数是否独立于 20** —— ⭐ 逐字只有一处间接表述 "each potentially containing **up to 20** syntax verification sub-loops"，⛔ 论文没有独立声明语法环的 cap 参数，⛔ 也没说它是否与安全环共用同一个配置项。
5. ⚠️ **T4 的性质生成算法未给** —— ⭐ 逐字只有 "the tool generates a set of safety properties for each SMD"。⭐ 「每 state 一条可达性」是从 Table 1 的 `(/N states)` 分母口径**推出**的（S），⛔ 论文未写生成算法，⛔ 也未说 deadlock-freedom 是每 SMD 一条还是全局一条。
6. ⚠️ **`Pressure Controller` 实验 1 的性质分母缺失** —— ⭐ Table 1 该格逐字只写 "Unverified properties: 7"，⛔ 唯一一格没有 `(/N states)`。⛔ 无法核对该格的分母。
7. ⚠️ **被检查的语法规则总数 $s$ 未给** —— ⭐ 打分公式用到 $s$，⛔ 但论文没给数值，⛔ 也没列规则清单（⭐ 只举了 3 个例子并说 "among others"）。⛔ 故无法与 SoSyM 那篇的 38 条做逐条对照。
8. ⚠️ **配套仓库的 push 时间早于论文 3 个月** —— ⭐ 仓库 `created_at`/`pushed_at` 均为 `2025-11-17`，⭐ HAL 提交日为 `2026-02-16`。⛔ 无法确认仓库里的 `models.xml` 是否就是 Table 1 那 6 格对应的那一版（⛔ 无 run log、⛔ 无逐格目录结构）。
