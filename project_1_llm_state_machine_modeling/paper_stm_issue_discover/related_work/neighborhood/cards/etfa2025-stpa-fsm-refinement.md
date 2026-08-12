# 卡片 · King & Vyatkin, ETFA 2025 —— STPA controller constraint 驱动的 LLM 迭代式 FSM 演化

⭐ **全文已取到**，本卡按 9 页 accepted author manuscript（Aalto green OA post-print）逐节抽取，⛔ 不是仅据摘要。⚠️ 取到的是 **post-print**（作者接受稿），⛔ 不是 IEEE Xplore 排版版 —— 见 F §6。

⚠️ **标题比任务书给的更长**：⭐ 正式标题含尾巴 **"and Generation of IEC 61499 Code"**（M，逐字见 A 节），⛔ 任务书的短标题不是原题。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `etfa2025-stpa-fsm-refinement` |
| `title` | ⭐ **LLM-based Iterative Refinement of Finite-State Machines with STPA Controller Constraints and Generation of IEC 61499 Code**（M，逐字取自 PDF 首页与 p.2 标题行） |
| 作者 | Akira King（Aalto University，Dept. of Electrical Engineering and Automation）· Valeriy Vyatkin（Aalto University ＋ Luleå Tekniska Universitet）（M） |
| `year` | ⭐ **2025**（正式发表年；Crossref `published-print` = `2025-09-09`，⛔ 无 early-access 年歧义） |
| `venue` | 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA), pp. 1–8（M ＋ Crossref `page: 1-8`） |
| `ccf` | ⛔ **未收录** —— 本仓库 [ccf_venues/](../../../../../ccf_venues/) 无 ETFA 建档，ETFA 属 IEEE IES 系列会议，不在 CCF 推荐目录（S） |
| `doi` | [`10.1109/ETFA65518.2025.11205687`](https://doi.org/10.1109/ETFA65518.2025.11205687) —— ⭐ **已核**：Crossref API `status: ok`，题录、作者、页码、reference-count 11 全部返回；`doi.org` 解析链返回 202（IEEE 侧）。⛔ **DOI 真实存在** |
| `arxiv` | ⛔ **无**（⭐ 已试 arXiv 检索与直链构造，无对应条目） |
| `url`（全文） | ⭐ [aaltodoc bitstream](https://aaltodoc.aalto.fi/bitstreams/9ab39cdd-e8af-4769-a1e6-974595dc7412/download) —— ⭐ 实测 `HTTP 200`，2 380 312 bytes，PDF 1.5，9 页，`sha256 = 001dadabc196b5342573110071cd5fa30800ee02038b0742bf7bc97e22de145d` |
| `url`（落地页） | [research.aalto.fi/en/publications/a5d441e5-…](https://research.aalto.fi/en/publications/a5d441e5-15d5-41ed-a536-07c8ad80250d)（200）· [aaltodoc handle 123456789/141539](https://aaltodoc.aalto.fi/handle/123456789/141539)（200） |
| `artifact_type` | ⭐ **IEC 61499 Function Block 内的 Execution Control Chart（ECC）**，即一台 FSM；⭐ **LLM 侧的载体是 JSON**（M，见 B5） |
| `task` | ⭐ **修复 / 约束驱动的模型演化**（把安全约束灌进去改已有 FSM）＋ 附带 **生成**（初始 FSM 起草、IEC 61499 可执行代码产出）。⛔ **不是缺陷检测** —— 它从不产出「这里有个缺陷」这种判定 |
| `boundary` | ⭐ **界内** —— 被改的制品是单个 FB 的 ECC，变量是布尔 I/O，⛔ 无时钟、无不变式、无正交并发区（S：从 §II-B 的 ECC 描述与 §II-C 的 I/O 清单推出）。⚠️ 外层 IEC 61499 Function Block Diagram 是事件驱动分布式的，⛔ 但那一层不是被 LLM 改的对象 |

⭐ **同组姊妹工作**（论文 ref [7]，⛔ 不是本篇）：V. Vyatkin, S. Patil, D. Drozdov, A. Shalyto, *LLM-based iterative requirements refinement in FSM with IEC 61499 code generation*, INDIN 2025。⭐ 它是 `fbAssistant` 工具本身的论文，全文可取（[is.ifmo.ru 镜像 PDF](https://is.ifmo.ru/research/llm_based_iterative_requirements_refinement_in_fsm_with_iec_61499_code_generation.pdf)，实测 200，7 页）。⛔ **本卡的一切断言只来自 ETFA 那篇**；INDIN 只在 F 节被用来记录「型号仍未报」这一否证。

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐ 按**实验里真正执行的环节**画（⛔ 不按论文的章节分段）：

```
[人] STPA step 1–3 手工分析
        → 3 Losses / 4 Hazards（Table I） / Control Structure（Fig 1） / 33 UCA（Table II 只印 4 条） / 11 controller constraints（Table III）
   → [LLM] 用 NL prompt 在 fbAssistant 里起草初始 FSM（Fig 5）  ⇄  [人] 看可视化后改文字再提交
   → ┌─ 循环 ×20（⛔ 无条件、固定轮数）────────────────────────────┐
     │ [LLM] 套固定模板 + 1 条 controller constraint 改写 FSM（输出 JSON） │
     │    → [确定性] JSON 解析（⛔ 失败则由人把该轮重跑一次，实测 4 次）      │
     │    → [确定性] fbAssistant：JSON → IEC 61499 function block ＋ 可视化 │
     │    → ⛔ 【此处没有门】上一轮结果直接成为下一轮输入                   │
     └────────────────────────────────────────────────────────────┘
   → [人] 事后主观把每轮改动标 positive / negative / neutral（⛔ 不回灌、不控流）
```

⭐ **整链 6 段 · 其中 LLM 2 段**（起草、迭代改写）。⭐ **循环内 3 个环节 · 其中 LLM 1 个**。

⭐ 递归式而非重放式，逐字（M，§III）：**"Each prompt was applied to the result of the previous iteration in a recursive manner, instead of the original finite-state machine."** ⭐ 作者自己在 §V 把「迭代原始代码 vs 递归迭代上一轮」列为**待探索的替代设计**：**"such as those iterating on the original code compared to iterating recursively with the previous iteration of code."**

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| 初始 FSM 起草 | ⭐ **生成器**（NL → FSM），⭐ 人在环内看图纠偏 |
| 循环内改写 | ⭐ **修复者**（拿一条 NL 安全约束去改 FSM） |

⛔⛔ **全流水线没有任何一次 LLM 调用扮演 `评审者` / `裁决者` / `分类器`。** ⭐ 这与我们（v46 有两个 LLM 自评 reviewer ＋ 一个 LLM 裁决者）形成直接对照：⭐ **他们的问题不是「LLM 自评没收益」，而是「压根没有评」**。

### B3 · prompt 策略

⭐ `zero-shot` ＋ **单一固定模板**。⭐ 模板逐字（M，§III）：**"If the following constraints do not hold for the state machine, modify it such that the constraints hold:"** 后接一条 controller constraint。

⭐ 其余口径：**JSON 输出**（⛔ 但显然**没有**受限解码 / schema 强约束 —— 否则不会有 4 次 unparseable，见 B7）· ⛔ **无** few-shot · ⛔ **无** CoT · ⛔ **无** self-consistency 投票 · ⛔ **无** RAG · ⛔ **无**工具调用 · ⛔ **无**多智能体。

⭐ **一条值得记的 prompt 语言学纪律**（M，§V）：**"Prompts in this paper were formatted so as to not undermine the ''confidence'' of the LLM, as such prompts have been identified as detrimental to the outcomes of iterative prompting [8]."** ⭐ 即他们刻意避免「你上一版错了」这类削弱措辞 —— ⚠️ 这与我们把契约门报错文案原样回灌的做法**方向相反**，值得 M1 注意。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本卡最重要的一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有** |
| ⭐⭐ **裁决者是谁** | ⛔⛔ **无裁决者。** ⭐ 循环是**固定轮数、无条件**跑满的 —— ⛔ 没有任何东西决定「要不要再来一轮」（M：§III 逐字 **"the finite-state machine was iterated using 9 different prompts and 20 iterations for each prompt, resulting in a total of 180 iterations"**，⛔ 全文无任何终止判据描述） |
| ⭐ 唯一的确定性检查 | ⭐ **JSON 可解析性**，⛔ 且它触发的是**人工把该轮重跑一次**，不是循环控制（M，§IV-A：**"In four instances, the LLM returned an unparseable JSON file. In these cases the iteration was run a second time which led to a parseable output in all four instances."**） |
| ⛔ 评分者的位置 | ⭐ **事后、离线、人工主观** —— ⛔ **不回灌、不控流**（M，§III：**"The changes made during each iteration were documented and tracked according to a subjective evaluation of whether the changes made in the iteration were positive, negative, or neutral."**） |
| 终止条件 | ⭐ **最大轮数**（第一轮 20，第二轮 10）。⛔ 无收敛判据、⛔ 无预算判据、⛔ 无人叫停 |
| 最大轮数 | ⭐ **20**（主实验）· **10**（第二轮合并约束实验） |
| ⭐⭐ 有无报告循环的边际收益 | ⭐⭐ **有，且这是本篇对我们最有价值的一格。** 逐轮柱状图 Fig 6 覆盖 9 个 prompt 全部 20 轮 |

#### ⭐⭐ 逐轮边际收益 —— 逐字抄下（全部 M）

⭐⭐ **总体成功率**（§V）：**"the prompting method was only applied successfully in 1 of 10 prompts tested in this paper."** ⭐ 唯一成功的是 **C-7** 那组。

⭐⭐ **唯一成功那组的收益曲线**（§IV-A）—— ⭐ **这一条与我们「第 3–5 轮零收益」是同型现象**：

> **"The iterations in this set introduced a total of 10 positive changes, 3 negative changes, and 12 neutral changes."**
>
> **"The best-behaved versions of the finite-state machine with controller constraint C-7 were reached in iteration 11."**
>
> **"The LLM was also hesitant to introduce changes to this version of the finite-state machine, with no changes being introduced for the following 5 iterations."**

⭐ 即：**最优版本在第 11 轮达到，第 12–16 轮零改动**（S：由上面两句直接推出；⭐ Fig 7 图注自称 "The finite-state machine from iteration 16"，与「12–16 无改动」一致）。⭐⭐ **20 轮里至少 5 轮（25%）纯烧钱，⛔ 而流水线里没有任何机制能察觉这件事。**

⭐ **改动量的跨约束方差**（§IV-A）：

> **"with some controller constraints generating a maximum of 3 changes in one iteration, while others introduced up to 12 changes in one iteration."**
>
> **"Over the course of 20 iterations, some controller constraints generated roughly 20 changes, while others generated up to 69 changes."**

⛔⛔ **振荡（本卡最该被 M1 记住的机制）**（§IV-A）：

> **"In many instances, positive changes introduced in later iterations were considered positive due to addressing or reversing negative changes made in earlier iterations. For example, in one instance, the value of an output variable in a specific state was changed back and forth between TRUE and FALSE for several iterations."**

⭐ 即：**「positive 改动数」这个指标被自我撤销污染** —— ⛔ 一半的正分只是在还上一轮的债。⭐⭐ 这给我们「修订机器吃 79% token 而覆盖净变化 ≈ 0」提供了一条**可引用的机制解释**：不是没动，是动了又撤回来。

⛔ **漂移 / 迁移**（§IV-A）：

> **"These iterations could perhaps be best described as the finite-state machine migrating or drifting. Through migration, the FSM can evolve into an entirely different structure over the course of just a few iterations."**

⭐ 漂移的典型形态（M，§IV-A）：**"the state describing how to reach the 3rd input tray would first be altered to mimic the state describing how to reach the 2nd input tray, and then eventually be removed entirely."** ⭐ 即**状态被逐步同质化然后删除**；⭐ 也有反例（状态断连数轮后又被以不同顺序接回，Fig 8）。

⭐ **第二轮（两条约束合并进一个 prompt，10 轮）**（§IV-B）：

> **"The number of changes introduced in this set of iterations was similar to the earlier sets despite the set spanning only 10 iterations, with 19 positive, 20 negative, and 6 neutral changes over the course of 10 iterations."**
>
> **"Combining the two controller constraints into one prompt appears to improve the results. Most notably, new variables were not introduced, and the iterations did not drift towards removing the ''EXT H3'' state unlike iterations conducted with each of the controller constraints C-1 and C-2 separately."**

⚠️ **这组的数字自相矛盾感很强**：19 positive vs **20 negative** —— ⛔ 作者仍称 "appears to improve"，理由是**两类具名失效模式消失了**（不再造新变量、不再删 `EXT H3`），⛔ 而不是靠计数占优。⭐ 这正好印证他们自己承认的「计数不反映严重性」（见 C 节 `metrics`）。

⭐ **语法错误的持续期**（§IV-A）：**"Similarly, the LLM produced outputs with syntactical errors in a few instances, including missing spaces or incorrect notation. These errors never persisted for more than 3 iterations."**

### B5 · ⭐ 中间表示

⭐⭐ **有，而且是三层，⛔ 必须分开看 —— 混着看会得出错误结论。**

| 层 | 形态 | ⭐ 是否闭合 | ⭐ 谁定的 |
| :-- | :-- | :-- | :-- |
| ① **UCA 四类** | ⭐ 缺陷 / 不安全模式**类型学** | ⭐⭐ **闭合（恰好 4 类）** | ⛔ **人**（作者手工做 STPA Step 3），⛔ **LLM 完全不参与选类** |
| ② **11 条 controller constraint** | ⭐ 自然语言祈使句（Table III 逐字全给） | ⛔ **开放**（人手写的散文，⛔ 不是从模板集合里选） | ⛔ **人**手写 |
| ③ **FSM 本身** | ⭐ **JSON**（LLM 的实际输出格式），由 fbAssistant 转成 IEC 61499 ECC | ⛔ 原文未提供 JSON schema | fbAssistant（Flexbridge AB） |

⭐⭐ **UCA 四类的逐字定义**（M，§II-A）—— ⭐ **这是与我们 19 条谓词最直接的对照物**：

> **"The ''how'' is categorized into four distinct types: provided, not provided, provided too early/too late, provided for too long/too short."**

⭐ 规模（M，§III）：**33 条 UCA**（**"a total of 33 Unsafe Control Actions"**，⛔ Table II 只印了 4 条）→ **11 条 controller constraint**（Table III 全给）。

⭐ controller constraint 的构造纪律（M，§II-A）：**"Controller constraints are derived from the UCAs, and are statements that outline the only kind of behavior allowed by the controller."** ⭐ 而他们做了一个**刻意的表述反转**：**"in this work, rather than outlining each unsafe context in the Controller Constraints, the only safe context is often specified due to being more intuitive and efficient in the case of this specific system."** ⭐ 即从「禁止 X」翻成「当且仅当 Y 时才允许」（Table III 里大量出现 "when and only when"）。

⭐⭐ **对 Q-c 的答案：本篇是「闭合类型学 ＋ 人套用」，⛔ 不是「闭合 ＋ LLM 自动选」。** ⛔ LLM 在本篇里从不做分类，它只被动接受人写好的一条约束去改模型。⭐ **我们那个「闭合 19 条 ＋ LLM 自动选」的组合，本篇给不出先例。**

### B6 · 模型

⛔⛔ **原文只写 "OpenAI's GPT models"，没有型号、没有版本、没有日期、没有温度、没有多模型对照。** 逐字（M，§II-D）：

> **"In the current work, the tool is mainly used as an interface for OpenAI's GPT models and to provide a visual means of checking the code generated by the LLM."**

⭐ 核验方式：全文 9 页 grep `gpt|openai|o1|o3|claude|gemini|temperature|model version` —— ⛔ **只命中上面这一处** ＋ 参考文献里的 "ChatGPT for PLC/DCS"。⭐ 姊妹 INDIN 论文同样未报型号（F §2）。

⚠️ **按 schema B6 的口径，这是一个硬缺口**：⛔ 连是哪一代 GPT 都不知道，所以「LLM 会让 FSM 漂移」这个结论**该打多少折扣无法估**。⭐ ⛔ **不得把本篇的失败率当作当代模型的能力上界引用。**

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | ⭐ 强度 |
| :-- | :-- | :-- |
| JSON 解析 | ⭐ 语法层可解析性检查 | ⛔ **纯语法**，⛔ 且失败时靠人重跑，不进循环控制 |
| fbAssistant 转换器 | ⭐ JSON → IEC 61499 function block（可下到 soft PLC 与真 PLC） | ⭐ 确定性翻译，⛔ 不做语义判定 |
| 可视化 | ⭐ 给人看的状态图渲染 | ⛔ 判定还是人做 |
| EcoStruxure Automation Expert 虚拟调试 | ⭐ 仿真 / 虚拟 commissioning | ⚠️ **在 180 轮实验里是否逐轮使用，原文未明说** —— 见 F §1 |

⛔⛔ **没有模型检查器、没有求解器、没有类型检查器，⛔ 也没有对 STPA 约束的任何形式化求值。** ⭐⭐ **11 条 controller constraint 从头到尾是英文句子** —— 于是「这条约束到底满足了没有」这个问题，**在整条流水线里从来没有被回答过**。⭐ 循环在优化一个**没有度量的目标**。

⭐⭐ **这是对 Q-a 的答案，而且是个否定答案**：⛔ 本篇**一个 sound oracle 都没有**（我们至少有 pyfcstm 在求值端）。⭐ 所以它给 M1 的贡献不是「先例」，是**反面证据：不放 oracle 的后果长什么样**。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⛔⛔ **无。** ⛔ 无非迭代 baseline、⛔ 无多模型对照、⛔ 无人类工程师对照、⛔ 无「不给 STPA 约束只给自然语言需求」的对照。⭐ 唯一的内部对照是**单约束（9 组 × 20 轮）vs 合并约束（1 组 × 10 轮）**，⚠️ `n = 1` 且轮数不等（20 vs 10），⛔ 不构成受控比较（S） |
| `dataset` | ⭐ **1 个案例系统**：pick-and-place 机械手（4 执行器：两个水平线性 ＋ 一个垂直线性 ＋ 真空吸盘；4 个托盘：3 进 1 出），1 个 controller function block（M，§II-C）。⛔ 无公开数据集、⛔ 无多系统 |
| ⭐ 分母怎么定的 | ⭐ **迭代分母** = `9 prompt × 20 轮 = 180` ＋ `1 prompt × 10 轮 = 10` → **190 轮**（M）。⭐ **成功率分母** = **10 个 prompt**（"1 of 10 prompts"）。⚠️ Table III 有 **11** 条约束而 Fig 6 只画了 **9** 条（C1 C2 C3 C4 C7 C8 C9 C10 C11）—— ⛔ **C-5 / C-6 为什么没做，原文未解释**（见 F §3） |
| `metrics` | ⛔⛔ **只有「每轮的改动计数」，按 positive / negative / neutral 三分。** ⛔ 无正确率、⛔ 无覆盖率、⛔ 无形式化 pass/fail、⛔ **无任何 `@k` 类多轮口径**（⭐ 虽然它逐轮报了数，⛔ 但它报的是「改了几处」而不是「达标了没有」） |
| ⭐ 指标的自陈缺陷 | ⭐⭐ **作者自己把口径的问题写清了**（M，§IV-A）：**"the numbers of positive and negative changes do not communicate the severity of the changes, and therefore the numbers of changes do not directly reflect a successful or unsuccessful outcome. The absolute number of changes also does not capture the number of types of changes introduced."** |
| ⭐ `judged_by` | ⛔⛔ **作者主观人工判定。** 逐字见 B4（**"a subjective evaluation"**）。⛔ **无第二标注者 · 无 $\kappa$ · 无一致率 · 无判定手册 · 无 LLM-as-judge**（M / S） |
| `human_baseline` | ⛔ **无** |
| `runs` | ⛔ 每个 prompt **只跑 1 条 20 轮序列**，⛔ 无重复采样、⛔ 无 seed、⛔ 无方差、⛔ 无置信区间。⭐ 唯一的重跑是 4 次 JSON 解析失败时把该轮重跑一次（M） |
| ⭐⭐ `adverse_results` | ⭐⭐ **处理得非常坦白 —— 本卡认为这是可直接借鉴给我们 −15.82pp 的现成写法**，见下 |

### ⭐⭐ 不利结果的处理方式（⭐ 逐字，全 M）

⭐ **摘要里就把期望调低**，不留到 limitations：

> **"The results indicate that while the approach may be successful in some instances, more work is required to mitigate the issues arising from its application."**

⭐ **conclusion 第一段直接给失败率**，⛔ 不藏在正文中段：

> **"While the results shed light on the characteristics that may be desirable in prompts used to iterate control software, the prompting method was only applied successfully in 1 of 10 prompts tested in this paper."**

⭐ **第一条 key finding 就是「方法常常达不到目标」**：

> **"As implemented in this paper, iteratively evolving the controller with controller constraints often falls short of the intended outcome."**

⭐ **主动写出方法的核心弱点并给出机制**：

> **"A key weakness of the approach explored in this paper is its susceptibility to introducing unwanted drift to the generated code over the course of several iterations. This may lead to the correct parts of the existing code to be altered significantly."**

⭐⭐ **主动披露自己实验制品里的错误，⛔ 而不是悄悄修掉重跑**（⭐ 这一条尤其值得学）：

> **"Control Action 11 was mistakenly introduced, but kept in the diagram due to the experiments already having taken place."**（Fig 1 图注）
>
> **"Unfortunately, Control Action 11 was later determined slightly inaccurate, as no explicit ''retract'' command is sent to the vertical actuator, and retraction is rather accomplished through the absence of an ''extend'' command. However, the controller constraints relating to UCAs derived from the retract command were adjusted, and the experiments were conducted with the adjusted controller constraints: C-8, C-9, and C-10."**（§III）

⭐⭐ **主动承认实验设置对自己有利，⛔ 并把它列为 future work**：

> **"future work should identify the stages of code generation in which iterating the code with requirements provides the best results, as the finite-state machine used as the starting point for each set of iterations was already in a rather mature stage compared to the true starting point of an empty FSM."**

---

## D. 资产

⚠️ **`tools.verify_assets` 本篇不适用** —— ⛔ 全文没有任何仓库 / artifact / DOI 型数据链接可以喂给它。⭐ 替代核验用 `curl` 直取 ＋ GitHub Search API，逐条证据见下表。

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [aaltodoc bitstream](https://aaltodoc.aalto.fi/bitstreams/9ab39cdd-e8af-4769-a1e6-974595dc7412/download) | ⭐ `HTTP 200`，`size 2380312`，`PDF 1.5`，**9 页**，`sha256 001dadabc196b5342573110071cd5fa30800ee02038b0742bf7bc97e22de145d`；⭐ 首页自陈 **"Peer-reviewed accepted author manuscript, also known as Final accepted manuscript or Post-print"**。⛔ **注意**：Pure 直链 `research.aalto.fi/files/202973848/…pdf` 实测 **403**（带 UA / cookie / referer 三种组合均 403），⛔ 必须走 aaltodoc bitstream |
| ⭐ 实验代码 | ⚪ | ⛔ 无 | ⛔ 全文 grep `github|available|open.?source|repositor` —— ⛔ **零命中**（除版权声明与参考文献里的 GitHub Copilot 论文）。⭐ `fbAssistant` 是 **Flexbridge AB 的 proof-of-concept 商用工具**（M，§II-D：**"a proof-of-concept tool developed by Flexbridge AB"**）。⭐ GitHub Search API：`q=fbassistant` → **`total_count = 0`**；`q=iec+61499+llm` → **`total_count = 0`**。[flexbridge.se](https://www.flexbridge.se/) 返回 200，⛔ 但未见工具下载入口（未逐页穷举，见 F §7） |
| ⭐ 数据集 / Benchmark | ⚪ / ⭐ 部分在论文内 | ⛔ 无可下载物 | ⭐ **论文内可直接抄用的**：Table I（3 Losses ＋ 4 Hazards 全）· Table III（**11 条 controller constraint 全文逐字**）· Fig 1（Control Structure）· Fig 5（初始 FSM 图）。⛔ **不可得的**：33 条 UCA 里**只印了 4 条**（Table II 标题逐字 **"4 of 33 Unsafe Control Actions"**），⛔ 余 29 条未公开；⛔ 初始 FSM 的 JSON 未公开 |
| 实验结果细则 | 🟠 | ⛔ 仅论文内 | ⭐ 只有 **Fig 6 的 9 张逐轮柱状图** ＋ 正文聚合值（20 / 69 改动、max 3 / 12、C-7 的 10/3/12、第二轮 19/20/6）。⛔ **无逐轮逐改动的可下载表**，⛔ 每轮改动的原始记录（那份「subjective evaluation」台账）未公开 —— ⛔ 于是**判定不可复核** |
| Artifact / 复现包 | ⚪ | ⛔ 无 | ⛔ 无 Zenodo / 4open / OSF / 附录包；⛔ ETFA 无 artifact evaluation 轨（S） |
| ⭐ prompt 是否公开 | 🟠 | ⭐ 用户侧公开 / ⛔ 工具侧未公开 | ⭐ **用户侧 prompt 实际可完整重建**：模板逐字给出（§III）＋ 11 条约束逐字给出（Table III）。⛔ **但 fbAssistant 注入的 system prompt、FSM 的 JSON schema、以及它如何把当前 FSM 序列化进上下文，全部未提供** —— ⛔ 所以**不可完整复现** |

---

## E. ⭐ 对 M1 的意义

### 1. ⭐ 可取之处（⛔ 具体到哪个决定可以搬）

1. ⭐⭐ **不利结果的写法可以整套照搬。** ⭐ 三个动作值得逐一学：**abstract 就下调期望**（"more work is required to mitigate the issues"）· **conclusion 第一句给失败率**（"only applied successfully in 1 of 10 prompts"）· **主动披露自己制品的错误而不是重跑掉**（CA-11 那两段）。⭐ 我们手上的 **−15.82pp** 完全可以按这个骨架写：先在摘要把期望摆平，再在结论第一句给差值，再主动说明我们自己的口径缺口（比如台账正在 G1 重标）。
2. ⭐⭐ **「drift / migration」这个命名可以借。** ⭐ 它给「反复修订让制品整体漂走」这个现象一个**已发表、可引用的名字**，⛔ 而且是**在别人的系统、别人的模型、别人的制品格式上独立复现的同一现象**。⭐ 我们「修订机器零收益」的叙事因此从「我们这次没调好」升格为「这是迭代式 LLM 修订的一个已知失效模式」。
3. ⭐⭐ **它给我们的「零收益」补上了机制。** ⭐ 逐字：**"positive changes introduced in later iterations were considered positive due to addressing or reversing negative changes made in earlier iterations"** —— ⭐ 即**净收益 ≈ 0 不是因为没动，而是因为动了又撤回来**（甚至观察到 `TRUE ↔ FALSE` 连续来回）。⭐ 这条假设我们可以在自己的 v46 记录上直接去验：⭐ **查修订轮之间是否存在同一字段的反向翻转对**。若成立，那就是一条我们能拿数据支撑的机制发现。
4. ⭐ **「把约束按被控部件写全」这条 prompt 纪律有实测支撑。** ⭐ 他们把 C-1、C-2 合并进一个 prompt 后，**两类具名失效模式消失了**（不再凭空造 `aboveTray` / `vacant_tray` 变量、不再漂向删除 `EXT H3`）。⭐ 这对我们「一条需求 → 一条断言」的切分粒度是一个**反向证据点**：⚠️ **切得太细可能反而给模型留下补全空间**。
5. ⭐⭐ **「用制品里已有的变量表述约束」这条纪律，他们放在 prompt 端而不是 validator 端 —— ⭐ 与本仓库 §11 的边界纪律一致。** 逐字：**"Controller constraints should likely be formulated such that they describe the context in terms of the variables existing in the FSM, in order to limit the generation of superfluous variables."** ⭐ 这与我们 `named_elements` 引用门想解决的问题**是同一个问题**，⛔ 而他们没有把它做成门。⭐ 考虑到我们那道门的误伤事故（190/2928 行被拒、某 pair 18/18 撞死），⭐ **本篇是「这类约束就该待在 prompt 里」的一条外部支持**。

### 2. ⛔ 不可取 / 陷阱（⭐ 尤其是它踩了我们哪些坑）

1. ⛔⛔ **循环完全没有裁决者，固定 20 轮无条件跑满。** ⭐ 后果是可量化的：⭐ 唯一「成功」的那组，最优版本在第 11 轮，⛔ **第 12–16 轮零改动** —— ⛔ 至少 25% 的轮次纯烧钱，⛔ **而且没有任何机制能察觉**。⭐ 这就是我们「第 3–5 轮零收益」的同型病，⛔ **且他们比我们更严重**：我们至少有 `precheck_and_seal` 这个 0-token 的确定性门在挡。⭐⭐ **M1 该记的结论：即使不上 sound oracle，只要有一个「本轮无改动 / 无进展」的确定性计数器就能省掉 25% 的轮次 —— 这是零成本的。**
2. ⛔⛔ **安全约束只是 prompt 里的英文句子，全程没有任何机械求值。** ⭐ 33 条 UCA、11 条 constraint，⛔ 没有一条被翻成可判定的东西。⭐ 于是「约束满足了吗」这个问题**从头到尾没人回答**，循环在优化一个**没有度量的目标**。⭐⭐ **这是「无 sound oracle 的自由迭代」的教科书式反例，⛔ 也正好是 M1 第二条设计原则（把裁决者换成 sound oracle）的最强论据。**
3. ⛔ **指标退化成「改动计数」而非「是否正确」。** ⭐ 作者自己承认计数不反映严重性、不反映类型数。⛔ **我们绝不能退到这个口径** —— ⭐ 我们的 `hit@1 / hit@3 / hit@all` ＋ 五类多报，比本篇严格得多，⭐ **这一点在对照表里应该明确写出来**。
4. ⛔ **模型型号未报。** ⭐ 只有 "OpenAI's GPT models"。⛔ **不得把本篇的失败率当作当代模型的能力上界引用**；⛔ 引用时必须注明型号缺失。
5. ⛔ **`n = 1` 案例 ＋ 无 baseline ＋ 无重复采样。** ⭐ 于是无法区分「方法不行」与「这一次采样不行」（⭐ 对照本仓库 §12：⛔ 采样不确定性不能用来掩盖结构性失败 —— ⛔ **反过来也成立，单次运行也不能用来断言结构性失败**）。⭐ 他们那 9 组各只有一条轨迹，⛔ 若换个 seed 结论可能变。
6. ⚠️ **判定不可复核。** ⭐ 唯一的判定是「作者主观三分类」，⛔ 无第二标注者、⛔ 无 $\kappa$、⛔ 原始台账未公开。⭐ **对照之下我们的 574 位逐位判定 ＋ 288 簇五类裁定是本篇的数量级之外的投入** —— ⭐ 这条在 Q-f 上是一个明确的「别人没做」。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⛔⛔ **任务方向相反。** ⭐ 他们做**修复 / 演化**（把约束灌进去改 FSM），我们做**缺陷检测**（判断 FSM 是否违反需求）。⭐ 差别的后果很实：⛔ **修复任务不需要判定装置也能出图**（改了就是改了），⛔ **检测任务不行**（不判定就没有输出）。⭐ 所以「他们没有 oracle 也发了论文」**不能**被读作「我们也可以不要 oracle」。
2. ⛔ **闭合词表的选类者不同。** ⭐ 他们：**闭合 4 类 UCA ＋ 人套用**，中间的 11 条约束是**人手写的散文**。⭐ 我们：**闭合 19 条 ＋ LLM 自动选**。⭐⭐ **所以 Q-c 在本篇上的答案是「闭合但人选」，⛔ 不是我们那个组合的先例。**
3. ⛔ **prompt 反馈的措辞方向相反。** ⭐ 他们刻意**避免**削弱模型 "confidence" 的措辞；⛔ 我们把契约门报错文案**原样回灌**（那些文案本质上就是「你上一版错了，错在这个字段」）。⚠️ **这一点值得 M1 单独想一次**：⛔ 若他们引的 [8] 那条效应真实，⛔ 我们的门反馈可能在同时做两件相反的事 —— 给出正确的结构信息，⛔ 同时压低后续输出质量。⭐ **这是一条可以在我们自己数据上验的假设，⛔ 不是可以直接采信的结论。**
4. ⚠️ **制品格式与工具链不同。** ⭐ 他们的 FSM 是 IEC 61499 的 ECC（带 output event 与 algorithm，布尔 I/O），载体是 JSON，下游能直接下到 soft PLC 做虚拟调试；⭐ 我们是 pyfcstm DSL ＋ 求值 facade。⭐ **他们的「可执行性」来自工具链而不是来自方法**，⛔ 所以那部分不可迁移。

---

## F. ⛔ 存疑与未核项

1. ⚠️⚠️ **180 轮里到底有没有逐轮跑仿真 —— 这一格决定 B4 / B7 的定性，⛔ 而我判不了。** ⭐ Fig 2 图注写仿真环境**"used when simulating the system in an IEC 61499 development environment"**，§II-D 说工具工作流含 **"deployed to a virtual or physical environment for testing"**、**"simulating the generated control logic within a virtual commissioning environment"**；⛔ 但 §III / §IV 描述**这次实验的评分**时只提 "subjective evaluation"，⛔ 从未说每轮跑了仿真。⛔ 若逐轮跑了，那循环里其实存在一个**测试执行型 oracle**（只是没被用来控流）；⛔ 若没跑，评分就纯靠看状态图。⭐ 已通读 9 页全文并 grep `simul|test|commission|deploy`，⛔ **未找到能定性的句子**。⭐ **本卡按「未明说」处理，B7 里已标注。**
2. ⚠️ **GPT 型号不可得。** —— 已试：ETFA 全文 grep（`gpt|openai|model version|temperature` 仅命中 §II-D 那一处）· 姊妹 INDIN 论文全文 grep（同样无型号，只有 "Large Language Models (LLM)" 与 fbAssistant 描述）· Crossref / OpenAlex / S2 题录（不含型号）。⛔ **结果：型号无从确认。**
3. ⚠️ **C-5 / C-6 为什么没做实验，原文未解释。** ⭐ Table III 有 11 条，⛔ Fig 6 只画了 9 条（C1 C2 C3 C4 C7 C8 C9 C10 C11）。⭐ 我方推测（**I**，⛔ 不得当事实）：⛔ C-5/C-6 与 C-3/C-4 结构对称（1 号 vs 2 号水平执行器），⛔ 看起来像是被当成冗余而省略；⛔ **原文对此一字未提。**
4. ⚠️ **"1 of 10 prompts" 里合并那组算成功还是失败，原文未明确表态。** ⭐ 分母 10 = 9 单约束 ＋ 1 合并（S）。⛔ §IV-B 说合并 "appears to improve the results"，⛔ 但同一段给的是 **19 positive vs 20 negative**；⛔ §V 又说唯一成功的是 C-7。⛔ **两处未被作者显式对齐。**
5. ⚠️ **Fig 6 的逐轮逐点数值不可得。** ⭐ post-print 里只有 9 张柱状图，⛔ 无数据表、⛔ 无补充材料。⭐ 正文只给聚合值（20 / 69 总改动、单轮 max 3 / 12、C-7 的 10/3/12、第二轮 19/20/6）。⛔ **所以「第 N 轮各类改动数」这一层无法逐字抄，本卡只抄到了 C-7 的「第 12–16 轮零改动」（那是正文文字给的）。**
6. ⚠️ **IEEE 官方排版版未取。** ⭐ 手上是 Aalto 的 accepted author manuscript（9 页，含 1 页 Aalto 封面 → 正文 8 页，与 Crossref `page: 1-8` 一致）。⛔ 已试 `doi.org` 跳转（202，落到 IEEE 需鉴权）、⛔ Pure 直链（403）。⭐ 图号 / 表号 / 逐字措辞**理应**与刊出版一致（作者接受稿），⛔ 但**不保证**；⛔ 引逐字片段时应注明来源为 post-print。
7. ⚠️ **fbAssistant 的 FSM JSON schema 与 system prompt 未公开。** —— 已试：全文 grep（无）· GitHub Search API 两组查询（均 `total_count = 0`）· [flexbridge.se](https://www.flexbridge.se/) 首页（200）。⛔ **未逐页穷举 Flexbridge 站点与 INDIN 论文里提到的 YouTube 演示**（INDIN ref 里有一条 `youtube.com/live/aR20KBmZnA4` 链接，⛔ 本轮未打开）—— ⭐ 若后续要复现，那条演示可能是唯一的 schema 线索。
8. ⚠️ **STPA 分析本身由谁做、花了多久、有没有第二人复核，原文未提供。** ⛔ 33 条 UCA 与 11 条 constraint 的产出成本未报 —— ⚠️ 这在与我们做成本对比时是缺的一格（⭐ 我们那边 574 位人工判定的成本是明账）。
