# 卡片 · Ambiguity Detection and Elimination in Automated Executable Process Modeling

⭐ **本卡基于全文**（本地已有 `paper.pdf` + `paper_content.txt`，⭐ 另实际抓取了 artifact 仓库的完整文件树与 README）。⛔ 图 1 / 4 / 5 / 7 是直方图，⛔ 其中的数值不在 PDF 文字层里，⛔ 故凡涉及"具体熵值"一律记为原文未提供。

⭐⭐ **为什么这张卡对 M1 特别重要**：⛔ 别被它的 BPMN 制品迷惑 —— ⭐ 它是一条**与我们完全不同的缺陷发现范式**。⛔ 我们靠「拿断言去查」，⭐ 它靠「让模型多次生成、看散不散」。⭐ 而且它把「从散到哪里有缺陷」这一跳**完全交给了确定性算法**，⛔ 没让 LLM 碰。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `ambiguity-detection-process-modeling` |
| `title` | Ambiguity Detection and Elimination in Automated Executable Process Modeling |
| `year` | **2026**（⭐ arXiv v1 提交日 2026-04-13，⭐ 稿面日期 2026-04-14） |
| `venue` | ⛔ **arXiv 预印本**（`cs.SE`），⛔ 稿面标 `A PREPRINT`，⛔ 未见投稿目标声明 |
| `ccf` | ⛔ **未收录**（预印本，无 venue） |
| `doi` | [`10.48550/arXiv.2604.10884`](https://doi.org/10.48550/arXiv.2604.10884) |
| `arxiv` | [`2604.10884`](https://arxiv.org/abs/2604.10884) —— ⭐ 本轮实际访问，HTTP `200` |
| `url` | artifact：[github.com/ionmatei/ambiguity-detection](https://github.com/ionmatei/ambiguity-detection) —— ⭐ 本轮实际抓取文件树 |
| 作者 / 单位 | Ion Matei 等 7 人 · Fujitsu Research of America + Fujitsu Limited + University of Maryland |
| `artifact_type` | ⭐ **BPMN 2.0 可执行流程模型**（XML，SpiffWorkflow 可执行） |
| `task` | ⭐⭐ **缺陷检测 + 修复** —— ⛔ 但**修的是自然语言需求文本，不是模型**（⭐ 这一点很关键，见 E3） |
| `boundary` | ⭐ `邻域`（BPMN / 工作流。⛔ 含 gateway 分支语义，⛔ 无时钟；⭐ 按 [README.md](../README.md) §2.1 三档判为邻域） |
| 硬门 1（基于 LLM） | ⭐ **过** —— GPT-5.1 承担生成、翻译、歧义定位、文本修复四个环节 |
| 硬门 2（行为类模型制品） | ⭐ **过** —— BPMN 与工作流在 [README.md](../README.md) §2 表内明列 |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **11 阶段 · 4 个 LLM · 5 个确定性 · 2 个人**）

```
[人] 提供市政 policy PDF（日文）
  → [确定性] PDF 抽取
  → [LLM] 日→英翻译
  → [人] native speaker 复核译文
  → [LLM] 抽取 task/event/gateway/data-dependency 并生成 BPMN XML   ← ⭐ 独立重复 100 次
  → [确定性] SpiffWorkflow 执行 + 执行迹聚合成 5 个 KPI
  → [确定性] KPI 向量经验分布 + 归一化 Shannon 熵
  → [确定性] 从两个 dominant KPI class 各选一个代表模型（reference / target）
  → [确定性] MBD：conflict set 构造 → minimal hitting set → AST 归一化剪枝
  → [LLM] ambiguity detection：把诊断出的 gateway 映射回**逐字**原文片段
  → [LLM] ambiguity elimination：证据支持的最小改写
  → ⟲ 回到 BPMN 生成，重跑 100 次 + 重新仿真
```

⭐ **M**，逐字（§2.1）：`"The pipeline preprocesses the source document, uses an LLM to extract tasks, events, gateways, and data dependencies, generates BPMN XML, executes the model with a workflow engine [3], and aggregates execution traces into policy KPIs."`

⚠️ 前 4 阶段与第 5 阶段的生成器来自作者**前作** [15,18]，⛔ 本文只贡献第 6–11 阶段。⭐ 计数按本文实际描述的整条链算。

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| 日→英翻译 | `翻译器`（⚠️ 自然语言翻译，⛔ 不是形式化转换） |
| BPMN 生成 ×100 | ⭐ `抽取器`（task/event/gateway/数据依赖）+ `生成器`（BPMN XML） |
| ambiguity detection | ⭐ `解释者` + `抽取器` —— ⛔ **注意它不做定位**：⭐ 定位已由 MBD 给出，⭐ LLM 只负责「把 gateway 翻译成原文片段 + 写出两种竞争解释」 |
| ambiguity elimination | ⭐ `修复者` —— ⛔ **修复对象是需求文本** |

⛔⛔ **词表里的 `裁决者` 一格是空的。** ⭐ 本文的 LLM **从不判定对错** —— ⭐ 判定完全由仿真 + 熵 + MBD 做。⭐ 这是本卡最值得 M1 看的一条。

### B3 · prompt 策略

| 策略 | 有无 | 说明 |
| :-- | :-: | :-- |
| ⭐ 多次采样 | ⭐⭐ **有，但语义反转** | ⭐ 机制与 `self-consistency` 同源（同一输入独立采样 100 次），⛔ **但目的完全相反**：⛔ self-consistency 把离散度**投票掉**，⭐ 本文把离散度**当作信号本身** |
| 结构化输出约束 | ⭐ 有 | ⭐ detection 输出 JSON（`ambiguous_elements` 列表，每项含 `ambiguity_id` / `narrative_excerpt` / `ambiguity_analysis`）；⭐ elimination 输出 JSON（`revised_process_narrative` + `ambiguity_revisions`）。**M**，出自 artifact README |
| ⭐ 程序化 CoT | ⭐ 有 | ⭐ elimination prompt 明写四步流程（定位映射 → 证据选解释 → 最小消歧改写 → 全文重组）。**M**，§2.4：`"The ambiguity elimination prompt implements a four-step procedure."` |
| ⭐ 去偏指令 | ⭐ 有 | **M**，§3.1 逐字：`"The prompt explicitly states that "reference" and "target" do not imply that one model is correct and the other is incorrect."` ⭐ 这是一条明确的 anchoring 防护 |
| ⭐ 证据接地约束 | ⭐ 有 | **M**，§2.4 逐字：`"The selected interpretation must be justified by explicit supporting excerpts. Unsupported assumptions are not allowed."` |
| RAG / 工具调用 / 多智能体辩论 / few-shot | ⛔ 原文未提供 | —— |

⭐ **prompt 公开性**：⭐ detection 与 elimination 两个 prompt **以 PDF 形式公开**；⛔ **BPMN 生成 prompt 未公开**（在前作里）。→ D 节。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有** —— 生成×100 → 熵 → MBD → 文本修复 → **重生成×100 + 重仿真** |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **`测试执行`（SpiffWorkflow 仿真）+ `确定性规则`（归一化熵 + MBD minimal hitting set）** —— ⛔ **不是 LLM 自评**，⛔ **也不是 sound oracle** |
| 终止条件 | ⛔ **原文未提供** —— ⛔ 无收敛判据、无最大轮数、无预算规则 |
| 最大轮数 | ⛔ **原文未提供**；⚠️ **实测只跑了 1 轮**（original → repaired，⛔ 没有第二轮修复） |
| ⭐ 有无报循环的边际收益 | ⭐ **有，但只有 1 轮的数字，且只有定性档 + mode share** |

#### ⭐ 逐轮数字（⭐ 逐字抄）

| 案例 | 修复前 | 修复后 | 熵档 |
| :-- | :-- | :-- | :-- |
| City 1 | ⛔ `"The distribution contains several distinct KPI combinations, indicating substantial variability across generated models."`（⛔ **无具体熵值、无具体百分比**） | ⭐ `"More than 90% of the generated models now produce the same outcome."` | ⭐ `very high` |
| City 2 | ⛔ `"The figure again shows substantial output variability."`（⛔ **无数值**） | ⭐ `"with 70% of the generated models now producing the same outcome"` | ⭐ `high` |

⭐ 熵档口径，**M**（§2.2 逐字）：`"we refer to four qualitative ranges certainty: very high(≤0.30), high((0.30,0.50]), moderate((0.50,0.70]), and low(>0.70) consistency."`

⛔⛔ **本文全篇没有报告任何一个具体的 $H_{norm}$ 数值。** ⭐ 只有四档定性标签 + 修复后的 mode share 百分比。⚠️ 这使得「熵降了多少」无法复算 —— ⭐ 而这恰恰是该方法唯一的定量结论。

#### ⭐⭐ 裁决者性质的精确定位（⛔ 别把它当 sound oracle）

⭐ 作者**主动**且**两次**声明这不是正确性证明：

- **M**（§1 / Abstract）：`"Our goal is not to prove that one generated BPMN model is semantically correct, but to detect when a natural-language specification fails to support a stable executable interpretation under repeated generation and simulation."`
- **M**（§1）：`"In this setting, generation consistency is used as a proxy for reliability, not as a proof of semantic correctness."`

⭐ 所以裁决者的准确刻画是：⭐⭐ **一个确定性、可复算、但只测「稳定性」不测「正确性」的裁决者**。⛔ 它比 LLM 自评强（不受生成器同源偏差影响、0 语义判断），⛔ 但比 sound oracle 弱（⚠️ **一致的错也是一致的**，见 E2）。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有，且分三层** |
| 形态 | ① ⭐ **KPI 向量上的经验分布 + 归一化熵**（统计量）· ② ⭐ **MBD 的 conflict set / minimal diagnosis**（gateway 集合）· ③ **结构化 ambiguity report**（JSON） |
| ⭐⭐ **是否闭合** | ⭐⭐ **「看哪里」闭合，「是什么问题」开放** —— ⛔ 这是一个混合形态，⛔ 与我们不同 |
| ⭐ **谁定的** | ⭐ KPI 由**人**从官方政策文件 [12] 定（5 个）· ⭐ component set 由**模型结构机械枚举**（target 的全部 gateway）· ⛔ ambiguity 描述由 **LLM 自由生成** |

⭐ 三层拆开看：

| 层 | 闭合性 | 谁定 | 逐字依据 |
| :-- | :-- | :-- | :-- |
| ⭐ **观测面**（5 个 KPI） | ⭐⭐ **闭合** | ⭐ 人（从 Program for Preventing the Progression of Diabetic Nephropathy [12] 导出） | **M** §3.1：`"evaluates them using five KPIs: Notification Count(NC), Health Guidance Count(HC), Guidance Resource Utilization(RU), Health Improvement Rate(HI), and Medical Cost Savings(CS). These KPIs are derived from the Program..."` |
| ⭐ **可疑元件集**（gateway） | ⭐⭐ **闭合，且机械枚举** | ⭐ 模型结构自身 | **M** §2.3：`"The component set (COMPS) is the set of gateways in the target model."` |
| ⛔ **缺陷描述** | ⛔ **开放** | ⛔ LLM 自由文本 | ⛔ **无缺陷类型学**：`ambiguity_analysis` 是自然语言解释，⛔ 不从任何固定集合里选 |

⚠️⚠️ **与我们的对照，这一格是全卡最有信息量的地方**：⭐ 我们是「**闭合 19 条谓词词表 + LLM 自动选**」；⭐ 它是「**闭合观测面 + 确定性定位 + 开放描述**」。⛔ **它根本没有「选类」这个动作** —— ⭐ 因为「问哪里」由 MBD 算出来，⛔ 不由 LLM 选。⭐⭐ **这意味着我们那 69 位「根本没问」的赤字，在它的形状里结构上不可能出现**：⭐ 该问哪个 gateway 是最小碰集的解，⛔ 不是模型的选择。

### B6 · 模型

⭐ **GPT-5.1 单模型，全链路**。**M**（§3）逐字：`"All steps that involve an LLM use GPT-5.1."` ⭐ 另 §3 明写翻译也是它：`"including PDF extraction and GPT-5.1-based translation"`。

⛔ **无多模型对照。** ⛔ 温度 / top-p / 采样参数**原文未提供** —— ⚠️ 这是一个实质缺口：⛔ 100 次生成之间的差异究竟来自显式温度还是 provider 非确定性，**决定了熵该怎么解释**，⛔ 而原文没说。

⭐ 时效性：GPT-5.1 属当代 SOTA 档，⭐ 按 schema B6 的口径**不打折**。

### B7 · ⭐ 确定性成分（⭐ 本文的「可信底座」很厚）

| 环节 | 是什么 | 逐字依据 |
| :-- | :-- | :-- |
| PDF 抽取 | 文档预处理 | **M** §3：`"including PDF extraction"` |
| ⭐ **BPMN 执行引擎** | ⭐ SpiffWorkflow [3] | **M** §2.1：`"executes the model with a workflow engine [3]"` |
| KPI 聚合 | 执行迹 → 5 个总体 KPI | **M** §2.1：`"aggregates execution traces into policy KPIs"` |
| ⭐ **归一化 Shannon 熵** | ⭐ 见下方公式 | **M** §2.2 |
| ⭐⭐ **MBD** | ⭐ conflict set 构造 + minimal hitting set 枚举 | **M** §2.3 |
| ⭐ **AST 归一化比较** | ⭐ gateway 条件等价性剪枝（Aho 编译原理 [4]） | **M** §2.3：`"This equivalence check is implemented through comparison of normalized abstract syntax trees (ASTs) [4]."` |
| 结构检查（soundness / gateway matching / deadlock freedom） | ⚠️ **S，且存疑** | ⭐ §1 说这类检查 `"remain necessary [9], but they are not sufficient here"`，⛔ **但没说本文实际跑了没有** |

⭐⭐ **对比我们自己**：⭐ 我们有 pyfcstm 当 sound oracle 但**放在求值端**；⭐ 它没有 sound oracle，⛔ 但把「**执行 + 统计 + 最小诊断**」这三件确定性的事全部放在了**裁决端与定位端**。⭐ 换句话说：⛔ 它的底座更薄（无证明能力），⭐ 但**底座的位置比我们对**。

---

## B-补 · ⭐⭐ 三个必答问题（⛔ 逐字回原文）

### ⭐⭐ 问题 1：「行为离散度」的操作化定义

⭐ **M**，§2.2 全段逐字关键句：

> `"Each generated BPMN model is simulated over the same synthetic population, and the resulting aggregate KPI vector is treated as one sample, y = (y_1, y_2, ..., y_d), with d denoting the number of KPIs. From these samples, we construct an empirical distribution over the distinct KPI output vectors observed across generated models. Because the KPI outputs are sparse, we represent this distribution as a discrete probability mass function over the set of unique output combinations. Let Y = {y(1), ..., y(K)} denote the set of unique KPI combinations, and let p_i be the empirical probability of observing y(i). We then compute the normalized Shannon entropy of this distribution as H_norm = − (∑_{i=1}^{K} p_i log_2 p_i) / log_2 |Y|, which takes values in [0,1] and provides a scale-independent measure of output dispersion."`

⭐ 写成公式：

$$H_{\mathrm{norm}} = \frac{-\sum_{i=1}^{K} p_i \log_2 p_i}{\log_2 |Y|}$$

⭐ 三个关键设计点：

1. ⭐⭐ **熵算在「唯一 KPI 输出组合」这个离散集合上**，⛔ **不是**在单个 KPI 的边缘分布上。⭐ 一次仿真的整个 5 维 KPI 向量算**一个原子样本**；⭐ 两个模型只要有任一 KPI 不同就算不同类别。⭐ 作者给的理由是 KPI 输出稀疏（`"Because the KPI outputs are sparse"`）。
2. ⭐ **分母是 $\log_2|Y|$，即实际观测到的唯一组合数的对数**，⛔ 不是理论上限。⭐ 这让它 scale-independent，⛔ **但也意味着分母随观测本身变化** —— ⚠️ 若 100 次全落进 2 个类别，$|Y|=2$，分母 = 1；⛔ 若落进 5 个类别，分母 = $\log_2 5$。⚠️ **同一个 mode share 在不同 $|Y|$ 下会给出不同的 $H_{norm}$**，⛔ 原文没有讨论这个性质。
3. ⭐ 概率 $p_i$ 是**经验频率**（100 次中的占比）。

⭐ **100 次是怎么定的**：⛔⛔ **原文完全没有给理由。** ⭐ 只有一句执行陈述，**M** §3.1：`"For each policy, we independently generate 100 BPMN models, simulate each model on the same synthetic patient population, and aggregate five population-level KPIs."` ⛔ **无样本量论证、无敏感性分析（50 次够不够？）、无熵估计的收敛检查。** ⚠️ 这是本方法一个明显的方法论缺口 —— ⭐ 熵的经验估计在小样本下有已知偏差，⛔ 而 $|Y|$ 本身也随 $N$ 增长。

### ⭐⭐ 问题 2：从「散」到「哪里有缺陷」这一跳怎么走（⛔ 最有价值的一步）

⭐ **答案：它把这一跳做成了一个经典 MBD 的最小碰集问题，⛔ 全程零 LLM。** ⭐ 五步：

**第 1 步 · 选两个代表模型。** **M** §2.3：`"From the empirical distribution of simulation results, we select two representative models from two dominant KPI classes. One is designated as the reference and the other as the target for diagnosis, with no assumption on correctness. Instead, we choose the diagnosis direction that produces the smaller minimum-diagnosis set, since this gives a more localized explanation."`

⭐ 注意两点：⭐ ①「无正确性假设」—— ⛔ reference 不是 ground truth，⭐ 只是对照物；⭐ ②**方向由「谁的诊断集更小」决定**，⛔ 不由谁更对决定。⭐ 这是一个纯粹的可解释性启发式。

**第 2 步 · 把 MBD 三元组填进去。** **M** §2.3：`"the system description (SD) consists of the target-model process structure together with its gateway logic. The component set (COMPS) is the set of gateways in the target model. The observations (OBS) are activity-level KPI outputs obtained by comparing the simulations of the reference and target models. An observation is marked as discrepant when the reference and target outputs differ. Formally, OBS_disc = {o ∈ OBS | o_ref ≠ o_tgt}."`

⭐ **为什么可疑元件只取 gateway** —— **M**：`"We treat gateways as potentially faulty components because they encode the main decision logic and are the most likely source of divergent behavior."` ⚠️ 这是一个**领域先验的强剪枝**：⛔ 它假定分歧只来自决策逻辑，⛔ 不来自 task 集合或数据映射。

**第 3 步 · 用「首次分歧点」把 conflict set 压小。** **M** §2.3：`"For each execution trace τ in such a context, we construct an ordered sequence S(τ) = ⟨(t_1,K_1), ..., (t_n,K_n)⟩, where each pair contains a task and the KPI it produces. We include only KPI-producing tasks, and when multiple KPIs are associated with the same activity, their names are sorted deterministically. We then compare the reference and target sequences and identify the first point at which they diverge. The divergence may appear as a missing output, an extra output, or an incorrect output. Outputs after the first divergence are treated as downstream consequences and are not used to construct conflicts. Let t_last be the last correct task and t_first the first erroneous task for a given divergent trace pair. Here, the ordering relation is the execution order along the target trace under the corresponding input case. We define the corresponding conflict set as CONF_i = {g ∈ COMPS | t_last < g < t_first}. Thus, each divergent input-output case yields one or more conflict sets containing only the target-model gateways between the last correct and first incorrect outputs. This positional restriction reduces conflict size."`

⭐⭐ **这是整跳里最巧的一步**：⭐ 它用**执行顺序上的位置约束**（`t_last < g < t_first`）把 conflict set 从「全部 gateway」压到「首次分歧点前后那一段的 gateway」。⭐ 三种分歧形态（missing / extra / incorrect output）都归一到同一个位置判据。⭐ 首次分歧之后的一切**明确丢弃**为下游后果 —— ⛔ 这避免了错误传播把诊断集炸开。

**第 4 步 · 求最小碰集。** **M** §2.3：`"The full diagnosis problem is built from the collection of conflict sets C obtained across all divergent subsets. We then compute minimal diagnoses as minimal hitting sets over C, following standard MBD theory. Although hitting-set computation is NP-hard in general, the bounded size of the conflict sets makes enumeration practical in our setting."`

⭐ 理论依据是 Reiter [17] 与 de Kleer & Williams [10] 的经典 MBD。⭐ 复杂度自述：$NP$-hard，⭐ 但因第 3 步把 conflict set 压小了所以可枚举。

**第 5 步 · AST 等价性剪枝。** **M** §2.3：`"A target gateway is removed from a diagnosis if its normalized logical condition is identical to a condition exercised in the reference trace for the same input cases. In that case, the gateway does not explain the observed output difference. This equivalence check is implemented through comparison of normalized abstract syntax trees (ASTs) [4]."`

⭐ 另有一条上下文划分：**M**：`"we compare the reference and target models only on input subsets for which their outputs differ. Agreement on other inputs indicates conditional inconsistency, so each divergent subset defines a separate diagnostic context."`

**⭐ 这一跳的实测产出**：⭐ City 1 的最小诊断集是两个 gateway —— **M** §3.2：`"The diagnosis identifies the target-model gateways Check Inclusion Eligibility and Check Health Guidance Acceptance as the main decision points that can explain the observed behavioral differences."` ⭐ City 2 得到 4 个 ambiguity。

⭐⭐ **然后才轮到 LLM**：⭐ LLM 拿到「这两个 gateway 可疑」，负责把它翻译成原文片段 + 两种竞争解释。⭐ City 1 的 AMB-1 结果逐字：`"In the reference model, gateway_3 is interpreted strictly: a patient must satisfy both the receipt-based diabetes criterion and the laboratory thresholds. In the target model, gateway_3 is interpreted more broadly: a patient qualifies if either the laboratory thresholds or the receipt-based diabetes criterion is satisfied."` ⭐ 即：⭐⭐ **AND 还是 OR 的歧义**。

### ⭐ 问题 3：真的不需要 ground truth 吗

⭐ **分两问回答，答案不同。**

**⭐ 检测阶段：⭐⭐ 真的不需要，且这是本文的核心卖点。** ⭐ 三处 **M**：

- Abstract：`"The result is a closed-loop approach for validating and repairing executable process specifications in the absence of ground-truth BPMN models."`
- §1：`"This paper studies that question in a setting where no ground-truth BPMN model is available."`
- §3：`"Because no ground-truth BPMN models were available, we used simulation consistency as a proxy for generation reliability."`

⭐ 机制上确实成立：⭐ 熵、MBD、AST 比较**全部只需要两个模型和一份输入数据**，⛔ 不需要知道哪个对。

**⛔ 评估阶段：⭐⭐ 它用的「对错标准」就是检测信号本身 —— ⛔ 这是一个实质弱点。**

⭐ 具体拆开：

| 想评什么 | 用什么评的 | 有没有独立标准 |
| :-- | :-- | :-- |
| ⭐ 修复是否降低了行为发散 | ⭐ **修复后重生成 100 次的 mode share + 熵档** | ⭐ **有**（确定性、可复算） |
| ⛔ **检出的 ambiguity 是不是真 ambiguity** | ⛔ **作者自述 + 定性举例（Listing 1/2/5）** | ⛔⛔ **没有**。⛔ 无 ambiguity ground truth 台账、⛔ 无第三方标注、⛔ 无一致性系数 |
| ⛔ **改写选的解释是不是政策作者的原意** | ⭐ 权威补充材料（Tokyo Program [21]）当依据 | ⚠️ **半有** —— ⭐ 有外部锚，⛔ 但没有政策作者确认，⛔ 也没有领域专家评分 |
| ⛔ **MBD 定位是否正确** | ⛔ **无** | ⛔⛔ **没有**。⛔ 无「诊断集命中真因」的判定 |

⛔⛔ **最尖锐的一条**：⭐ 被优化的量（熵）与宣告成功的量（熵）**是同一个量**。⚠️ 一个**语义上错但表述明确**的改写同样会降熵 —— ⭐ 因为它同样消除了竞争解释。⭐ 唯一挡住这条的是「必须有权威材料支撑」那条 prompt 约束，⛔ **而那条约束的遵守情况没有被独立核查**。⭐ 按本仓库 §3.5 第 5 条的口径，⭐ 这接近「自证式验证」，⛔ 且原文**没有标注**这是自一致性检查。

⭐ 唯一的人类介入是**译文复核，不是歧义判定** —— **M** §3：`"the translations were reviewed by native speakers and were therefore considered unlikely to be the main source of the observed model-generation and simulation variability."`

### ⭐ 问题 4：代价

| 项 | 数字 | 依据 |
| :-- | :-- | :-- |
| ⭐ 每个 policy 每个条件的生成次数 | ⭐ **100** | **M** §3.1 |
| ⭐ 每个 policy 的完整回路 | ⭐ **200 次生成 + 200 次仿真**（修复前 100 + 修复后 100） | **S**，由 §3.2 / §3.3 两次「generated 100 models」推出 |
| ⭐ 全实验总量 | ⭐ **400 次生成 + 400 次仿真**（2 policy × 2 条件 × 100） | **S** |
| ⛔ token 数 | ⛔ **原文未提供** | —— |
| ⛔ 金额 | ⛔ **原文未提供** | —— |
| ⛔ 墙钟 | ⛔ **原文未提供** | —— |
| ⛔ 仿真本身的成本 | ⛔ **原文未提供**（⭐ 但 SpiffWorkflow 是本地执行，⭐ 非 LLM 成本，量级可忽略） | **I** |

⭐⭐ **与我们的 212.6× 换算（⛔ 这是 `I`，⭐ 不得写成事实）**：

⭐ 关键是**分子的单位不同**，⛔ 别直接比 100 vs 3。⭐ 它的「一次生成」是**一次朴素的 BPMN 生成调用**；⭐ 我们的「一格」是 10 节点带两个修订循环的整条流水线（⛔ 其中修订机器吃 79% token）。⭐ 粗算：⭐ 若把「一次朴素生成」当 1 个单位，我们一格 ≈ 212.6 个单位，⭐ 那么 **100 次朴素生成 ≈ 我们 0.47 格**。

⭐ **推论（`I`）**：⭐⭐ **熵法看起来比我们现在的主臂便宜，不是更贵。** ⭐ 即使给 54 个 pair 各跑 100 次朴素生成（5400 次），⭐ 量级上仍在我们 324 格现有开销的同一个数量级或更低。⚠️ **但这个换算有三处不牢**：⛔ ① 它的 token 成本原文完全没报，212.6× 的分母（我们的朴素基线）与它的「一次生成」不是同一个 prompt；⛔ ② BPMN 生成的输出长度与 pyfcstm DSL 不可比；⛔ ③ 它还有 100 次仿真，我们若照搬需要 pyfcstm sim facade 跑 100 × N 条输入序列，⭐ 那部分不是 LLM 成本但有工程量。⛔ **所以这条只能当「值得实测」的线索，⛔ 不能当结论。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⛔⛔ **无。** ⛔ 未与任何文本层歧义检测工具对比（⭐ QuARS [14] / ACE [11] / LLM 歧义检测 [6] 都只在 §4 讨论，⛔ 没有跑）。⛔ 也没有消融（⭐ 见下方 ⚠️） |
| `dataset` | ⭐ **2 个 policy**，来自两个日本市町村的糖尿病肾病健康指导政策。⭐ 合成患者群体一份（`test_data.csv`）。⭐⭐ **分母 = 2** |
| `metrics` | ⭐ ① 归一化 Shannon 熵（⛔ 只报四档定性标签）· ② ⭐ dominant KPI combination 的 mode share 百分比 |
| ⭐ `judged_by` | ⭐ **自动脚本**（熵 / mode share，确定性可复算）+ ⛔ **作者自述定性举例**（ambiguity 是否为真、诊断是否正确）。⛔ **无第三方判定、⛔ 无 LLM-as-judge、⛔ 无标注者间一致性（$\kappa$ 或一致率）**。⭐ 唯一人类介入是译文复核 |
| `human_baseline` | ⛔ **无** |
| `runs` | ⭐ 每个 policy 每条件 **100 次独立生成**，⭐ 报的是**分布**（mode share + 熵档）。⛔ **但「100 次这个实验」本身没有重复**，⛔ 所以熵估计的跨重复方差**未报**。⛔ 无置信区间 |
| ⭐ `adverse_results` | ⭐ **如实报了，⛔ 但没归因** —— 见下 |

### ⭐ `adverse_results` 细看（⭐ 这一格对我们直接有借鉴价值）

⭐ **它报了三处不利结果，⛔ 一处没归因，⭐ 两处主动写进 Limitations。**

1. ⭐ **City 2 修复后只到 70%，明显弱于 City 1 的 >90%。** ⭐ 作者**如实写出**并如实降档为 `high`（⛔ 而不是 `very high`），⛔ **但完全没有分析为什么 City 2 更差**。⚠️ 线索就在文里而作者没连起来：⭐ City 2 有 **4 个 ambiguity**（City 1 只有 2 个），⭐ 且作者自己写了 `"City 2 is operationally more explicit than City 1 and therefore yields a more branched BPMN structure"` —— ⛔ 但没把「更多分支 + 更多歧义 → 修复后仍更散」这条因果说出来。
2. ⭐ **Limitations 主动写了两条硬限制**，**M** §4 逐字：`"Our method has two main limitations. First, it can detect only ambiguities that affect the monitored KPIs under the sampled input population. Ambiguities that do not change those outputs, or that arise outside the explored input region, may remain undetected. Second, the localization and repair stages still rely on LLM prompting and on the completeness of the supporting evidence. Therefore, the quality of the final revision depends on both prompt design and the quality of the external material used to resolve competing interpretations."`
3. ⭐ **主动承认自家 pipeline 可能是噪声源**，**M** §3：`"The automated pipeline, including PDF extraction and GPT-5.1-based translation, could itself introduce ambiguity."` ⭐ 然后给出缓解（native speaker 复核）与保留判断（`"considered unlikely to be the main source"`）。⚠️ ⛔ 但这只是一句判断，⛔ 没有量化（⛔ 例如：给定同一份译文重跑 100 次，熵是多少）。

⭐⭐ **可借鉴的写法**：⭐ ①**不利数字直接写在正文表述里并如实降档**，⛔ 不藏在附录；⭐ ②**Limitations 用「First / Second」明确编号**，⭐ 每条给出「什么检不出」的具体条件；⭐ ③**主动点名自家 pipeline 的噪声贡献**并说明缓解与残余不确定性。⭐ 这三条对我们写 −15.82pp 直接可用。

### ⚠️ 一个必须记下的实验缺口（⭐ 本轮实际抓 artifact 才发现）

⭐ artifact 仓库的 README 明写 detection prompt 有**两个变体**：

> ⭐ `ambiguity_detection` —— 输入含 MBD 诊断结果
> ⭐ `ambiguity_detection_without_diagnosis` —— ⛔ **不含 MBD**，`"Compares the two models structurally and semantically (no MBD), then traces each structural difference back to ambiguous narrative text"`

⛔⛔ **即：作者手里有「有 MBD vs 无 MBD」的消融装置，⛔ 但论文正文一个字都没报这个对照的结果。** ⭐ 而这恰恰是全文最想知道的数字 —— ⭐⭐ **MBD 这一跳到底贡献了多少？** ⛔ 如果不用 MBD、只让 LLM 直接比两个模型也能找到同样的歧义，⭐ 那本文的核心贡献就退化成「多次生成看熵」这一半。⛔ **原文未提供。**

### ⚠️ 选样效应（⭐ 必须记下）

⭐ **M** §3：`"This section reports results for two policies that exhibited high variability and shows how our method detects and repairs the ambiguities that give rise to that variability."`

⛔ 即：⭐⭐ **这 2 个案例是按「高 variability」筛出来的**。⚠️ 对极值样本做干预后再测同一指标，**天然含回归均值成分**；⛔ 而本文**没有对照组**（⭐ 例如：对同一段落做等长度的**无关**改写，看熵是否也下降）。⛔ 因此从这两个案例**无法区分「修复有效」与「选样效应 + 回归均值」**。⭐ 这不是苛责 —— ⭐ 它是预印本、n=2、定位是 case study；⛔ 但按本仓库 §3.5 第 4 条的口径，⭐ 这一点必须写进对照表的表注。

---

## D. ⭐ 资产（⛔ 本轮实际抓取，⛔ 不是看链接在不在）

⭐ **机械核验输出，逐字**（`python3 -m tools.verify_assets --url https://github.com/ionmatei/ambiguity-detection`）：

```
| https://github.com/ionmatei/ambiguity-detection | 🟢 | HEAD `362fcfbf01` · 文件 25（非文档 24）· release 0 · license 无 |
```

⛔⛔ **但机械建议 🟢 在这里是误导的 —— ⭐ 我按资源类型逐项终裁如下。** ⭐ 理由：⭐ 那 24 个「非文档文件」里**绝大多数是 PDF 与一个 25MB 的 mp4**，⛔ **源码是 0 个**。

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arXiv:2604.10884](https://arxiv.org/abs/2604.10884)；⭐ 本地 [paper.pdf](../../../baselines/ambiguity-detection-elimination-executable-process-modeling/paper.pdf) | ⭐ `curl` abs 页 HTTP **200**；⭐ 本地 `paper.pdf` 1.24 MB + `paper_content.txt` 44.9 KB，⭐ 11 页文字层完整可读 |
| ⭐⭐ **实验代码** | ⛔⛔ **⚪** | ⛔ **不存在** | ⛔⛔ **HEAD `362fcfbf019550592a8ae6b8197e204876dedb1f`，25 个 blob，其中 `.py` / `.ipynb` / `.js` / `.sh` / `.java` = 0 个。** ⭐ 全部文件是：⭐ 15 个 PDF · 4 个 `.bpmn` · 2 个 `.png`×4 · 1 个 `.csv` · 1 个 `README.md` · **1 个 25.4 MB 的 `tool-demo-movie.mp4`**。⛔ **生成 pipeline、熵计算、MBD 求解器、AST 归一化全部无源码。** ⛔ license 无 |
| ⭐ **数据集 / Benchmark** | ⭐ 🟢 | [`input-data/test_data.csv`](https://github.com/ionmatei/ambiguity-detection/blob/main/input-data/test_data.csv) + 4 份 policy PDF | ⭐ 实际下载：**1001 条数据行**，17 列（`Health_Check` / `Fasting_Blood_Glucose` / `HbA1c` / `eGFR` / `Urinary_Protein` / `ID` / `Age` / …）。⚠️⚠️ **与 README 及论文所称的「100 synthetic patient records」不符** —— ⭐ 见 F2。⛔ **无 ground truth**（⭐ 本方法的前提就是没有） |
| ⭐ 代表模型 | ⭐ 🟢 | `city-{1,2}/city_N_{reference,target}.bpmn` | ⭐ 4 个 BPMN 2.0 XML 实际存在：City 1 reference 14198 B / target 13210 B；City 2 reference 23115 B / target 29050 B。⭐ 另有 4 张对应 PNG |
| ⭐ 逐条报告 | ⭐ 🟢 | `city-N_ambiguity_report.pdf` · `city-N_repair_report.pdf` | ⭐ 4 份 PDF 实际存在（74–102 KB）。⭐ **含每条 ambiguity 的原文片段、竞争解释、改写理由与支撑证据摘录** |
| ⭐ 实验结果细则 | ⛔ **🟠** | ⛔ 只有论文内的 4 张直方图 | ⛔⛔ **100 次生成的逐模型 KPI 向量未公开** —— ⭐ 仓库每城只放了 **2** 个代表模型（reference + target），⛔ 不是 100 个。⛔ **因此 $H_{norm}$ 无法被第三方复算。** ⛔ 论文正文也未给任何具体熵值 |
| Artifact / 复现包 | ⛔ **⚪** | ⛔ 无 Zenodo / OSF / 4open DOI | ⛔ 仓库 release 数 = **0**，⛔ 无归档 DOI，⛔ 无 license。⛔ 无 pinned commit 引用 |
| ⭐⭐ **prompt 是否公开** | ⭐ **🟢（部分）** | [`prompt_ambiguity_detection.pdf`](https://github.com/ionmatei/ambiguity-detection/blob/main/prompt_ambiguity_detection.pdf) · [`prompt_ambiguity_elimination.pdf`](https://github.com/ionmatei/ambiguity-detection/blob/main/prompt_ambiguity_elimination.pdf) | ⭐ 两份 PDF 实际存在（165.8 KB / 148.6 KB），⭐ README 逐条描述了输入输出 JSON 结构。⛔⛔ **但 BPMN 生成 prompt 未公开** —— ⭐ 它在前作 [15,18] 里，⛔ 本仓库没有。⛔ 且 prompt 是 **PDF 而非可执行文本**，⛔ 需人工转录 |
| 补充证据材料 | ⭐ 🟢 | `supplemental_material.pdf`（74.5 KB） | ⭐ 实际存在。⭐ 即 repair 阶段当权威依据的 Tokyo Program [21] 相关译段 |
| 演示视频 | ⭐ 🟢 | `tool-demo-movie.mp4` | ⭐ 25 419 976 B（≈25.4 MB）实际在树里 |

⭐⭐ **D 节一句话结论**：⭐ **「结果侧」资产相当扎实**（policy 原文 / 修复后原文 / 逐条 ambiguity 报告 / 修复报告 / 代表模型 / 输入数据 / 两个 prompt / 演示视频都在），⛔⛔ **「过程侧」资产为零**（⛔ 无源码、⛔ 无 100 次的原始结果、⛔ 无归档 DOI、⛔ 无 license）。⭐ 换句话说：⭐⭐ **可以读懂它做了什么，⛔ 不能重跑它。**

⚠️ ⛔ **这正是 schema §D 与简报都点名的那个陷阱的一个新变体** —— ⛔ FlowFSM 那次是「仓库几乎是空的」；⭐ 这次是「**仓库很满但满的全是 PDF**」。⭐ 机械判据看到 24 个非文档文件就给 🟢，⛔ 而源码数是 0。⭐⭐ **建议把「源码文件数」单列为机械判据的一项**（`tools/verify_assets.py` 的 follow-up）。

---

## E. ⭐ 对 M1 的意义

### 1. ⭐ 可取之处（⛔ 具体到哪个设计决定可以搬）

1. ⭐⭐⭐ **「定位这一跳交给确定性算法」这个决定可以直接搬，⭐ 且它比熵本身更重要。** ⭐ 我们的 X1 赤字有 69 位在「**根本没问**」（选题）—— ⭐ 那是 LLM 选谓词选错了目标。⭐⭐ **本文的形状里这个赤字结构上不可能出现**：⭐ 该查哪个元件是最小碰集的**解**，⛔ 不是模型的**选择**。⭐ 可搬的具体形态：⭐ 我们的 `bind_attribution` 目前只做证据绑定，⭐ 完全可以升级为「给定两个（或 $N$ 个）对同一 NL 生成的 pyfcstm 模型 + 同一组输入序列，用位置约束 + 最小碰集算出**哪些迁移 / 守卫**能解释行为分歧」。⭐ pyfcstm 的 sim facade 已经能产出执行迹，⭐ 底座我们有。
2. ⭐⭐ **「多次重生成的行为离散度」当缺陷信号 —— 一条不需要台账、不需要断言的发现路径。** ⭐ 这对我们的战略意义很大：⭐ 我们的台账正在 G1 全量重标，⛔ 而**熵法完全不依赖台账**。⭐ 可搬形态：⭐ 对同一 NL 生成 $N$ 个 pyfcstm 模型 → 用 sim facade 在同一组输入序列上跑 → 把可观测结果向量当原子样本 → 算 $H_{norm}$ → 熵高的 pair 指向需求歧义或建模不稳定。⭐⭐ **这可以作为一条与断言臂并行的独立臂**，⛔ 而且（按上面 `I` 级换算）**可能比现在的主臂便宜**。
3. ⭐ **「位置约束压小 conflict set」这个技巧可以直接搬。** ⭐ 只取「首次分歧点前后那一段」的元件，⭐ 并**明确丢弃首次分歧之后的一切**为下游后果。⭐ 这对我们的状态机同样成立：⭐ 一条迁移错了会让后续整条迹全错，⛔ 若不做首次分歧截断，诊断集会被错误传播炸开。
4. ⭐ **AST 归一化剪枝可以搬到守卫比较上。** ⭐ 「若某迁移的归一化守卫条件与对照迹在同一输入下走过的条件语法等价，则它不解释差异，从诊断集剔除」—— ⭐ 我们的守卫是 pyfcstm 表达式，⭐ 有 parser，⭐ 归一化 AST 比较是现成能力。
5. ⭐ **「改写必须有权威外部材料支撑，不许无依据假设」这条 prompt 约束值得抄进 project_4。** ⭐ 逐字：`"Unsupported assumptions are not allowed."` ⭐ 配套的 traceability metadata（ambiguity id / 改写片段 / 理由 / 支撑证据摘录）是一个可直接复用的修复记录 schema。
6. ⭐ **不利结果的写法可以抄**（见 C 节 `adverse_results`）：⭐ 如实降档、Limitations 编号列举「什么检不出」、主动点名自家 pipeline 的噪声贡献。

### 2. ⛔ 不可取 / 陷阱（⭐ 尤其：它踩了哪些我们已经踩过或将要踩的坑）

1. ⛔⛔ **最致命的一条：⚠️ 一致的错也是一致的。** ⭐ 熵 = 0 意味着 100 次生成落进同一类，⛔ **但同一类可以是同一个错**。⭐ 若 LLM 系统性误读同一句 NL（⭐ 而这在我们的 54 个 pair 里几乎必然存在），⛔ **熵法对它完全失明**。⭐ 作者自己承认这不是正确性证明（`"not as a proof of semantic correctness"`），⛔ 但没有讨论这个失明面有多大。⭐⭐ **对 M1 的直接后果：熵法只能是断言臂的补充，⛔ 绝不能替代它。**
2. ⛔⛔ **可观测面决定可发现面，⭐ 而我们的可观测面比它更窄。** ⭐ 它自己写在 Limitations：只能检出会改变那 5 个 KPI 的歧义。⭐ 对我们更严峻：⛔ 我们台账里大量条目是**结构性缺陷**（缺状态、缺迁移、层次归属错），⛔ 其中不少**根本不改变任何可仿真的可观测量** —— ⭐ 例如一个不可达状态、一个多余的等价迁移。⛔ **这类缺陷熵法一个都看不见。** ⭐ 反过来说，⭐ 我们的谓词族里的**结构族 S 那 10 条**恰恰是熵法的盲区，⛔ 而**仿真族 B 那 6 条**才是熵法的射程 —— ⭐ 这给出了一个清晰的分工判据。
3. ⛔⛔ **评估的对错标准就是检测信号本身。** ⭐ 被优化的量与宣告成功的量是同一个 $H_{norm}$。⚠️ 一个语义上错但表述明确的改写同样降熵。⭐⭐ **若我们做熵法，必须另设一个独立的成功判据**（⭐ 例如：熵降低的同时，断言臂在该 pair 上的命中不下降；⭐ 或人工核验改写后的 NL 仍表达原意）。⛔ 不能只报「熵降了」。
4. ⛔ **$n=2$，⛔ 且样本按「高 variability」筛出，⛔ 无对照组。** ⭐ 回归均值无法排除。⭐ 若我们做熵法实验，**必须有对照臂**（⭐ 最简单的：对同一段落做等长度无关改写，看熵是否也降）。
5. ⛔⛔ **没有报任何具体的 $H_{norm}$ 数值，⭐ 只有四档定性标签。** ⭐ 这是一条明确的反面教材：⭐ 该方法唯一的定量结论无法被复算。⭐ 我们做熵法必须报**数值 + 跨重复方差 + $|Y|$**（⭐ 因为分母是 $\log_2|Y|$，⛔ 不给 $|Y|$ 就无法解释那个数）。
6. ⛔ **「100 次」这个数字没有任何论证。** ⛔ 无样本量分析、⛔ 无收敛检查、⛔ 无敏感性分析。⭐ 而熵的经验估计在小样本下有已知偏差，⛔ 且 $|Y|$ 随 $N$ 增长 —— ⭐ 这意味着**不同 $N$ 下的 $H_{norm}$ 不可直接比**。⭐ 我们若定 $N$，⭐ 必须先做一次 $N$ 敏感性曲线。
7. ⛔ **温度 / 采样参数未报。** ⛔ 这使得「离散度从哪来」不可知 —— ⭐ 是显式温度、还是 provider 非确定性？⭐ 我们做熵法必须固定并报告采样配置。
8. ⛔ **手里有 MBD 消融装置却没报结果。** ⭐ 见 C 节 ⚠️。⭐ 对我们的意义是：⭐⭐ **我们自己做这条臂时必须报 MBD 消融** —— ⭐ 否则无法回答「确定性定位到底贡献了多少 vs 只是多次生成本身有效」。
9. ⛔ **仓库满是 PDF 而源码为零。** ⭐ 见 D 节。⛔ 不可重跑。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⚠️⚠️ **裁决对象根本不同：⭐ 它判「文本是否支持稳定解释」，⭐ 我们判「模型是否有缺陷」。** ⭐ 它**明确拒绝**回答后者（`"Our goal is not to prove that one generated BPMN model is semantically correct"`）。⛔ 所以它不是我们的缺陷发现方法的替代品 —— ⭐ 它发现的是**需求歧义**，⛔ 而我们台账里的条目是**模型缺陷**。⭐ 两者的交集是「因需求歧义导致的模型缺陷」，⭐ 那只是我们台账的一个**子集**（⛔ 且我们目前不知道这个子集有多大 —— ⭐ 这是 G1 重标后可以顺手算出来的一个数）。
2. ⚠️⚠️ **它有一个我们没有的东西：⭐ 权威外部材料。** ⭐ repair 阶段拿 Tokyo Program [21] 当「哪种解释才对」的裁定依据。⛔ **我们的 54 个 pair 没有这种外部权威文档** —— ⭐ NL 就是唯一真源，⛔ 没有更上级的规约可以查。⭐⭐ **所以它的 repair 环节不可直接搬**：⭐ 我们能搬的只到「检出 + 定位 + 报告竞争解释」，⛔ 「选哪个解释」在我们这里无据可依。⭐ 这反而是一个可以写进论文的差异点。
3. ⚠️ **它修文本，⭐ 我们（paper1）只报缺陷。** ⭐ 它的闭环是「缺陷 → 原文片段 → 最小改写 → 重生成复验」；⭐ 我们 paper1 的 discover 到「报缺陷」就结束。⭐ 所以它的第 10–11 阶段与 ⟲ 那条回边**属于 project_4 的范围**，⛔ 不属于 paper1。⭐ 但第 6–9 阶段（执行 → 熵 → 选代表 → MBD）**整段落在 paper1 的射程内**。
4. ⚠️ **制品的「可疑元件集」不同构。** ⭐ 它的 `COMPS` = gateway 集合，⭐ 干净、扁平、机械可枚举。⛔ 我们的状态机有**层次结构** —— ⭐ 迁移的「位置」不是一维执行序，⭐ 而层次归属本身可以是缺陷。⛔ **位置约束 `t_last < g < t_first` 在层次机上不能直接照写**，⭐ 需要先定义层次机执行迹上的「位置」。⭐ 这是搬这条技巧时的第一个实际工程问题。
5. ⚠️ **它的 100 次生成之间没有修订循环。** ⭐ 每次是一次朴素生成。⛔ 我们若把「一格」当采样单位，⭐ 100 格的成本不可接受；⭐ **必须用朴素单次生成当采样单位** —— ⛔ 这意味着熵法臂用的生成器**不是**我们主臂的那条流水线，⭐ 而更接近 X1 朴素基线。⭐ 这在实验设计上是一个必须先定下来的口径。

---

## F. ⛔ 存疑与未核项

1. ⚠️ **原文没有报任何一个具体的 $H_{norm}$ 数值** —— ⭐ 已试过：通读 `paper_content.txt` 全 11 页文字层、检索 `entropy` / `Hnorm` / 数字模式；⭐ 图 1 / 4 / 5 / 7 是直方图，⛔ 数值只在图像里，⛔ PDF 文字层无。⭐ 结果：⛔ **只能拿到四档定性标签 + 「>90%」「70%」两个 mode share**。⚠️ 若需精确熵值，只能人工读图或联系作者。
2. ⚠️⚠️ **`test_data.csv` 的条目数与文档对不上** —— ⭐ 已试过：实际 `curl` 下载 raw 文件并用 `csv.DictReader` 计数，⭐ 得 **1001 条数据行**（1002 行含表头）。⛔ 而 artifact README 明写 `"contains 100 synthetic patient records"`，⛔ 论文 §3.1 也只说 `"the same synthetic patient population"`（未给数）。⛔ **无法判断是 README 笔误、还是数据集在论文提交后被换过。** ⚠️ 这个数字会直接影响 KPI 的量级（⭐ NC / HC 都是计数型 KPI），⛔ 因此也影响熵的解释。
3. ⚠️⚠️ **MBD 消融的结果未公开** —— ⭐ 已试过：读 artifact README 发现存在 `ambiguity_detection_without_diagnosis` prompt 变体；⭐ 全文检索论文正文无任何对照结果。⛔ 结果：⛔ **「MBD 这一跳贡献多少」这个最关键的数字原文未提供。** ⚠️ 两个 prompt PDF 我未逐页转录（⛔ 它们是 PDF，⭐ 需另跑 `tools/pdf_extractor`），⛔ 所以也无法排除「消融结果藏在 prompt PDF 里」这个可能（⭐ 但可能性很低）。
4. ⚠️ **BPMN 生成 prompt 未公开** —— ⭐ 已试过：抓完整仓库文件树（25 个 blob）逐个检查。⛔ 结果：⛔ 只有 detection 与 elimination 两个 prompt，⛔ 生成 prompt 在前作 [15] SysCon 2026 / [18] arXiv:2604.07817 里。⚠️ ⭐ 注意仓库里确实有一个 `2604.07817v1.pdf`（⭐ 即前作全文，1.1 MB），⛔ **本轮未读它** —— ⭐ 若 M1 要真正照搬生成侧，那份 PDF 是下一个入口。
5. ⚠️ **100 次生成的原始逐模型结果未公开** —— ⭐ 已试过：仓库文件树。⛔ 结果：⛔ 每城只有 2 个代表模型（reference + target），⛔ 不是 100 个。⛔ **$H_{norm}$ 不可被第三方复算。**
6. ⚠️ **温度 / top-p / 采样参数原文未提供** —— ⭐ 已试过：全文检索 `temperature` / `sampling` / `seed`。⛔ 结果：⛔ 无。⚠️ 这直接影响「100 次之间的差异从哪来」这个熵的解释基础。
7. ⚠️ **是否实际运行了结构检查（soundness / gateway matching / deadlock freedom [9]）不明** —— ⭐ §1 只说这类检查 `"remain necessary [9], but they are not sufficient here"`；⛔ §2 / §3 均未说本文跑了。⛔ 结果：⛔ **原文未明说。** ⚠️ 只能从「模型都 executable」推出至少通过了 SpiffWorkflow 的可执行性检查（**S**）。
8. ⚠️ **「100」的选取理由未提供** —— ⭐ 已试过：全文检索。⛔ 结果：⛔ 无论证、⛔ 无敏感性分析、⛔ 无收敛检查。
9. ⚠️ **两个 prompt PDF 的正文我未逐字转录** —— ⛔ 本轮只读了 artifact README 对它们的结构化描述（⭐ 输入 / 输出 JSON 字段）。⭐ 若 M1 要照搬 prompt 形态，⭐ 应先跑 `python -m tools.pdf_extractor` 把这两份 PDF 转成文本再细读。
10. ⚠️ **未核验前作 [18]（arXiv:2604.07817）** —— ⭐ 它是本文生成侧的全部依据，⛔ 而本卡的 B1 前 5 阶段是从本文 §2.1 的一句话概述里读出来的。⭐ 仓库里就有它的 PDF，⛔ 但本轮任务范围只到本文。
11. ⚠️ **`year` 字段的处理** —— ⭐ 本卡按 arXiv 提交日记 **2026**。⛔ 它是预印本，⛔ 无正式发表年；⚠️ 若后续被会议接收，`year` 需按 schema A 的口径改为正式发表年。
