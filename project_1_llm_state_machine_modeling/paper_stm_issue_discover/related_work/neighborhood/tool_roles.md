# 确定性成分的角色:逐项分类

> ⭐ **本文件是分类结果。** ⛔ 判据与协议在 [`TOOL_ROLE_TAXONOMY.md`](./TOOL_ROLE_TAXONOMY.md),⛔ **本文件不重复定义,也不修改判据。**
>
> ⛔⛔ **防火墙照旧**:本目录一切是**方法素材**,⛔ **不是论文证据**。
>
> **分类单位**:一次 **(成分 × 位置)** 三元组,⛔ 不是一篇论文。⭐ 同一成分在不同阶段占不同角色则拆成多行。

---

## 1. ⭐⭐ 我们自己(v46)—— **从源码分类,不是从卡**

⭐ 这一格用源码而非卡片作依据,⛔ 因为卡是摘要。⭐ 若某 agent 从卡分类的结果与本节不一致,**以本节为准并把差异记入 §1.2**。

### 1.1 逐项表

| 成分 | 它算出什么 | 输出到哪一步 | **角色** | 处置 | 有无对照 | 级别 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-: |
| `renderer._model_vocabulary()` | 已声明 states / events / variables · `-> [*]` 终止边(带 `ends_run`)· 复合退出边按 scope 计数 · 复合态声明入口(带 `converter_generated`)· 编译器自造变量 | `split_requirements` · `review_requirements` · `convert_assertions` | ⭐⭐ **表示变换 + 规则建立**(双重,§7 边界 4) | — | ⛔ **无对照** | M |
| pyfcstm `inspect_digest.diagnostics` | `parse_status` / `semantic_status` / `inspect_status` / `diagnostics` / `metrics` / `model_type` | `split_requirements` · `convert_assertions` | ⛔⛔ **零角色** | — | ⛔ **无对照** | M |
| NL 分段(`nl_segments`) | 把 NL 切成段 | `split_requirements` | ⭐ **表示变换** | — | ⛔ 无对照 | M |
| `renderer._source_context()` | `source_trace` 的 `attribution_boundary` 投影(`source_level_claim_allowed` / `representation_related` / `conversion_or_lowering_related`) | 三个 LLM 角色 | ⭐ **表示变换**(⚠️ 含少量规则性字段) | — | ⛔ 无对照 | M / S |
| Pydantic `StrictBaseModel` | 结构合规 | 解析失败原地重试 | ⭐ **求值** | **回灌** | ⛔ 无对照 | M |
| 断言契约门(`assertion_checker`) | 断言**可执行性** | `precheck_and_seal` → `review_assertions` | ⭐ **求值** | ⭐⭐ **回灌(可执行性)+ 封存(真值)** | ⛔ 无对照 | M |
| **19 条谓词求值**(pyfcstm parse / semantic / design / sim facade) | 每条断言的 `truth_value` | ⛔⛔ **不进任何 LLM** | ⭐ **求值** | ⭐⭐⭐ **封存 → 解封后记录** | ⛔ 无对照 | M |
| `bind_attribution` | 归因边界 `status` | 闭合 issue 集 | ⭐ **求值** | **拦截** | ⛔ 无对照 | M |
| `adjudicate_results` 的闭合 | issue 集对已发布结果闭合(`truth_value is False` ∩ `role ∈ {primary, precondition}` ∩ 归因 `safe`) | 限制裁决者的权限 | ⭐ **求值** | **拦截** | ⛔ 无对照 | M |

### 1.2 ⭐⭐⭐ 三条从源码读出的结论

1. ⛔⛔ **我们没有任何一个「信息探索」角色。** ⭐ 唯一的候选(pyfcstm 诊断)被 prompt 框成零角色 —— ⭐ 三处逐字:`orientation evidence only` · `never turn a tool warning into a requirement` · `inspect diagnostics alone are not sufficient evidence`。
2. ⭐⭐⭐ **「封存」是类型系统保证的,不是约定。** ⭐ 放给审查者的 `AssertionExecutionPublic` 字段只有 `status: Literal["executable", "invalid", "blocked"]` 与 `error` —— ⛔ **结构上没有 `truth_value`**;真值只在 `AssertionResult` 上,⭐ 经 `SealedAssertionReceipt`(只含 `sealed_hash` / `result_count` / `sealed_payload_ref`)间接引用。
3. ⭐⭐ **有一处「记录 vs 回灌」的显式取舍**,源码注释逐字:`blocked means a prerequisite did not hold... It is not an execution failure and **must not send the script back for repair -- the prerequisite's own False is the finding**.`

### 1.3 ⛔ 一个必须一起说的事实:**九项全部无对照**

⭐ 上表 9 行,**「有无对照」列全部是「无对照」**。⛔ 即我们**从未测过任何一个成分的有无**。⚠️ 这不是本轮的疏忽,⭐ 是既有状态 —— ⛔ 但它意味着**我们对自己流水线里每个确定性成分的贡献都没有数字**。

---

## 2. ⭐⭐ 已核实的角色 × 效果证据(⛔ 逐条带分母)

### 2.1 ⛔⛔ 规则建立:三个独立团队报负面

⭐ 三个团队、三种不同制品、同一现象:**往发现阶段注入规则目录,召回被重新分配而非增加**。

| 团队 | 逐字 | 级别 |
| :-- | :-- | :-: |
| **Télécom Paris**(MODELS 2024 + SoSyM 2026,⚠️ **同团队算 1 次独立观察**) | `when these rules are incorporated into the knowledge database injected in the consistency request, **the LLM tends to exclusively focus on these rules, thus ignoring other consistency aspects**`。⭐ 期刊版给的对策:`it is beneficial to run the detection process **twice, once with formal rules embedded and once without**, to take advantage of a broader detection basis` | M |
| **北航**(Internetware 2025) | `As rule complexity increases, **LLMs may lose focus on the original requirements**, and fixing one issue can introduce new ones` | M |
| **RFSeek** | 见 §2.2 逐条 | M |

### 2.2 ⭐⭐⭐ RFSeek 的四条 prompt 变更:按本分类学**恰好 2-2 分裂,且两类行为模式不同**

⭐ 这是本文件最强的一条 —— ⭐ **单篇论文内部的自然对照**,⛔ 不是跨篇拼的。

| # | 改了什么 | ⭐ **改的是哪个角色** | 逐字结果 | ⭐ 召回怎么变 |
| :-: | :-- | :-- | :-- | :-- |
| **1** | 只喂「最相关」的章节 | ⭐⭐ **信息探索 ↓** | `it reproduced the transitions already depicted in the diagrams and **did not yield any new or implicit protocol behaviors**` | ⛔ **下降** |
| **2** | 去掉 RFC 自带的 ASCII 图 | ⭐⭐ **信息探索 ↓**(去掉一个**模态 / 视角**) | `When the diagram was absent, **certain transitions were missing**... transitions described exclusively in diagrams **may be overlooked**` | ⛔ **下降** |
| **3** | 要求抽「**precise and accurate** FSM」 | ⭐⭐ **规则建立** | `it **completely omitted some edges it had previously identified**`(⛔ 删掉的正是促成 **RFC 9293 errata** 的那条边) | ⛔ **重排** |
| **4** | 加「抽出摘要提到的**所有**迁移」 | ⭐⭐ **规则建立** | `**this did not increase the total number** of transitions identified; **rather, the set of extracted transitions shifted**` | ⛔ **总数守恒,集合重排** |

⭐⭐⭐ **两类的行为模式不同**:⭐ 信息探索**减少** → 召回**真的下降**;⭐ 规则建立**变更** → **总数守恒、集合重新分配**。

### 2.3 ⭐⭐ 它顺手排除了一个竞争机制

⛔ 本来最可能的替代解释是**上下文预算**:也许失败来自 context 被占,⭐ 那 信息探索 也会受害,⛔ 角色区分就没意义。

⭐⭐⭐ **变量 1 / 2 把它排除了**:它们是**减少**输入而召回**下降**。⛔ 若机制是「context 稀缺、越少越好」,减少输入应当**改善**;⭐ 结果相反 —— **所以机制是角色特异的,不是预算通用的**。

### 2.4 ⚠️ 信息探索的加法:唯一形态无测量 + 一条异构加法

| 项 | 内容 | 级别 |
| :-- | :-- | :-: |
| ⭐ **唯一做了这个形态的工作** | ⭐ MBD(conflict set + minimal hitting set + 执行序位置约束 + AST 归一化剪枝)算出 **2 个 gateway** → **定位到元素后进 prompt** → LLM 只负责「把 gateway 翻译成原文片段 + 写两种竞争解释」。⭐ 主结果模型 `GPT-5.1`,**与我方同代** | M |
| ⛔⛔ **它的对照** | ⭐ **artifact 里有装置**(prompt 两个变体:含 MBD / `_without_diagnosis`),⛔ **正文一字未提结果**。⛔ 另:全文**无任何 $H_{norm}$ 数值**、$n=2$、⭐ 样本按「高 variability」筛出且无对照组、⛔ **被优化量与宣告成功量是同一个** | M |
| ⭐ **一条异构加法** | ⭐ 把配置的常量名与性质名告诉模型:**18.7%** vs 让模型自己还原 **10.0%** = **+8.7pp**,⭐ 当代模型。⛔ **但该档是重新采样(不同批)**,⛔ 且测的是「产出正确规约」不是「发现缺陷」 | M |

---

## 3. ⛔ 语料逐项分类(⏳ **进行中**)

⭐ 三路上下文独立 agent 正在按 [`TOOL_ROLE_TAXONOMY.md`](./TOOL_ROLE_TAXONOMY.md) 对 30 张卡逐项分类(各 10 张)。⭐ 结果回来后并入本节,⭐ 并与 §1 做卡-源码对拍。

⛔ **在此之前本节为空,⛔ 不填占位数字。**

---

## 4. ⭐⭐ 用本分类学查出的新缺陷

⭐ 见 [`discover_matrix/docs/findings/predicate_routing_defects.md`](../../discover_matrix/docs/findings/predicate_routing_defects.md)。

⭐ 一句话:**`occupancy_after` 的 `trigger` 字段说明宣称「本谓词也验证事件被消费」,⛔ 而它的签名有必填的 `target` 而 `event_consumed` 没有** —— ⭐ 故该主张只在完整指定的迁移上成立,⛔ 对「点名刺激但不点名去向」的句子不可表达。⭐ `event_consumed` 被问 **0.0%**、Δ **+55.6pp**,⛔ 而已有的修法只覆盖 `edge_declared`。

⭐⭐ **该条有独立的领域出处**(⛔ 两个函数签名的事实,只读 `predicates.py` 可核,⛔ 不引用台账),⭐ 故与那个 oracle-informed 的四扫描块**性质不同**。

---

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。⭐ §1 从**源码**给我们自己的 9 个确定性成分分类(⛔ 不是从卡),⭐ 查出「封存」是类型系统保证的、以及一处「记录 vs 回灌」的显式取舍;⛔ 并记下**九项全部无对照**这个既有状态。⭐ §2 落三团队负面证据与 RFSeek 的 2-2 分裂(⭐ 后者是单篇内部的自然对照,⛔ 且排除了上下文预算这个竞争机制)。⭐ §4 记用本分类学查出的新缺陷。⏳ §3 语料逐项分类进行中。 |
