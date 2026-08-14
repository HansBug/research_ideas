# 卡片 · LLM-guided Predicate Discovery and Data Augmentation for Learning Likely Program Invariants

⭐ **本卡的一句话结论**：⛔ **这不是「闭合词表 + LLM 自动选」的先例，它是那个组合的镜像** —— LLM 负责**造**谓词集合（开放生成），**选**哪条谓词进最终表达式的是**决策树的信息增益**（纯确定性）。⭐ 循环内一次 LLM 调用都没有；LLM 只在循环外被调用一次。

⚠️ **术语警告（本卡最容易被错位对照的一格）**：这里的「predicate」是**程序分析 / SyGuS 意义上的原子谓词**——即对**程序状态**求值的布尔表达式（`ncrit <= 1`、`flag[1] == 0`），是不变式表达式的**叶子**。⛔ 它**不是**我们那种「对模型提问的检查算子」，也不是时序性质的原子命题（论文明确把时序性质列为它学不了的类别）。⛔ **同名不同物，任何「他们 N 条 / 我们 19 条」的直接比较都是错位的。**

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `llm-guided-predicate-discovery` |
| `title` | LLM-guided Predicate Discovery and Data Augmentation for Learning Likely Program Invariants |
| 作者 | Yuan Xia, Aabha Shailesh Pingle, Deepayan Sur, Jyotirmoy V. Deshmukh, Mukund Raghothaman, Srivatsan Ravi（University of Southern California） |
| `year` | **2025**（正式发表年；SAC '25, March 31–April 4, 2025, Catania, Italy） |
| `venue` | SAC 2025 · The 40th ACM/SIGAPP Symposium on Applied Computing |
| `ccf` | ⚠️ **未收录** —— 本仓库 [ccf_venues/](../../../../../ccf_venues/) 全目录 grep `SIGAPP` / `Applied Computing` / `SAC` **零命中**；⛔ 本轮未独立核对官方 CCF 目录，故不断言「不在 CCF 名单」 |
| `doi` | [10.1145/3672608.3707984](https://doi.org/10.1145/3672608.3707984) —— ⭐ 已在 Crossref / OpenAlex / Unpaywall / Semantic Scholar **四处**取到同一条记录；⚠️ `doi.org` 直连 **HTTP 403**（ACM Cloudflare），非 DOI 无效 |
| `arxiv` | ⛔ **无**（arXiv API 检索标题与 `all:"Learning Likely Program Invariants"` 均零命中） |
| `url` | ⭐ **实际全文来源**：[https://r-mukund.github.io/pdf/2025-SAC.pdf](https://r-mukund.github.io/pdf/2025-SAC.pdf)（作者主页，706,111 bytes，9 页，本轮已下载并全文提取） |
| 工具名 | **RunVS** |
| `artifact_type` | ⚠️ **不变式表达式**（原子谓词的布尔组合），被分析对象是 **Promela 分布式协议模型** |
| `task` | ⭐ **不变式合成 / 断言性质生成** —— ⛔ **不是**缺陷检测、不是模型生成 |
| `boundary` | ⛔ **界外** —— 分布式并发协议、交错语义、消息传递 |

### ⚠️ 硬门核对（⛔ 必须如实登记）

| 硬门 | 判定 | 理由 |
| :-- | :-: | :-- |
| 1 · 基于 LLM | ⭐ **过** | LLM 是方法的一个**署名贡献**（贡献 iv：`LLM-aided predicate prompting`），⛔ 但只占流水线 1/8 个阶段 |
| 2 · 行为类模型制品 | ⚠️ **勉强 / 存疑** | 被处理的对象是 Promela 协议模型（LTS 类，算模型），⛔ **但 LLM 的产出物是逻辑表达式而非模型本身**。⭐ 收录理由是它正面回答本轨 B5 那一格（词表从哪来、谁选类），⛔ 不是因为它过了门 |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **8 个阶段 · 其中 LLM 仅 1 个**）

```
[人/工具] Promela 协议源码
  → [LLM ×1] 谓词发现（吐一串具体谓词）
  → [确定性] 模板抽象（抽掉具体常量）+ 模板实例化 → 有限 atoms 集合（此后冻结）
  → [确定性] SampleTrace（Spin 模拟采样有限长 trace）
  → [确定性] 反例判定（trace 里有状态 ∉ φ？或落在 speculated 里？）
  → [确定性] speculated 负例随机采样（数据增强，受 α 比例约束）
  → [确定性] Learner = 子采样 + 决策树（Shannon 熵 / 信息增益）+ SyGuS 语法
  ⇄ 回到 SampleTrace，直到 n ≥ MonitorBudget 或 m ≥ MaxTraces
  ── 评测端（⛔ 不在循环里）──
  → [sound oracle] Spin model checker 查 soundness
  → [sound oracle] SMT solver 查 safety（φ ∩ Unsafe = ∅ ?）
  → [确定性] model counting 估 tightness
```

⭐⭐ **形状要点**：LLM 在**入口**被调用一次就退场，⛔ 循环内**零 LLM 调用**；sound oracle 存在但被**故意**放在循环外（见 B4）。

### B2 · 每次 LLM 调用的角色（⭐ 全流水线只有一次调用）

| 调用 | 角色 |
| :-- | :-- |
| 谓词发现 | ⭐ **抽取器**（从源码抽变量 / 分支条件 / 断言）+ **生成器**（产出候选谓词列表） |

**M** 逐字（§3 `Predicate Discovery using an LLM`）：`"The LLM is prompted with the text of the distributed protocol and it extracts useful information such as variables, branch conditions, and assertions from the code."`

⛔ **没有**：评审者 · 修复者 · 裁决者 · 分类器 · 规划者 · 解释者。

### B3 · prompt 策略

| 项 | 值 |
| :-- | :-- |
| 策略 | ⭐ `few-shot`（严格说是 **one-shot**）+ **输出格式约束**（自然语言方式，⛔ 不是 JSON schema / 受限解码） |
| **M** 逐字 | `"To help the LLM produce syntactically correct expressions, we include a one-shot example in the prompt."`（§3） |
| **M** 逐字（Fig. 3 完整 prompt） | `"Task: Give me a list of all possible predicates using only the following variables [global_variables] respectively that could appear in the program's invariant/specification. For example, one predicate could be lock_available == true. Program: [... code ... ] Constraints: Provide only the predicates in a list and no explanation."` |
| ⛔ 无 | RAG · 工具调用 · CoT · self-consistency 投票 · 多智能体 · 结构化 schema 约束 · 解析失败回灌重试 |
| prompt 是否公开 | ⭐ **是**（Fig. 3 全文在论文里），⚠️ `[global_variables]` 与 `[... code ...]` 是占位符 |

⚠️ **一条对我们直接相关的观察**：这个 prompt **极短**（3 行），⛔ 没有任何谓词族说明、没有 `nl_cue`、没有选类纪律。⭐ 对照我们 19 条词表每条都带 `nl_cue` 且其中一条的 `nl_cue` 逐字在教模型别用某个谓词（324 格里 `edge_declared` 被问 0.0%）—— **他们的 prompt 简单到不可能产生这类泄漏，代价是完全放弃对谓词形态的引导。**

### B4 · ⭐⭐ 循环与裁决者（⛔ 本卡最重要的一格）

⭐⭐ **两个嵌套循环，裁决者全是确定性的，一个 LLM 自评都没有。**

| 循环 | 裁决者 | 类型 | 终止条件 |
| :-- | :-- | :-- | :-- |
| **外层** CEGIS（Algorithm 1 Lines 2–13） | 状态是否满足 φ 的**成员判定**（trace 里出现 `s ⊭ φ`，或出现被 speculated 为不可达却真的到达的 `s`） | ⭐ **确定性规则** | `n ≥ MonitorBudget`（连续无反例轮数）**或** `m ≥ MaxTraces` |
| **内层** Learner 子采样 | 候选 ψ 的 **precision / recall** 达标判定（precision > δ 且 recall 完整则接受，否则重采样） | ⭐ **确定性规则** | 收敛 |

⭐ **M** 逐字（Abstract）：`"Validation of the learned invariant is performed by sampling program runs and states; any run that invalidates the invariant results in counterexamples used to revises the invariant."`

⭐⭐ **最值得抄的一句：他们把 sound oracle 从循环里「故意拿掉」并给了理由。**

- **M** 逐字（Abstract）：`"we propose a counterexample-guided inductive synthesis approach called RunVS which learns invariant expressions from program runs, but without information such as target safety properties, and without invoking a model checker/theorem prover for validation."`
- **M** 逐字（§1）：`"most existing approaches invoke a model checker (or a theorem prover) within the synthesis loop, which makes these approaches depend on the scalability of the verification tools."`
- ⭐ Spin + SMT 只在**评测端**出现，用来事后核 soundness / safety。⚠️ **这与我们「有 pyfcstm 这个 sound oracle 却把它放在求值端而不是裁决端」是同一个拓扑** —— ⛔ 区别在于**他们是论证过的设计选择，我们是历史漂移**。

| 子字段 | 值 |
| :-- | :-- |
| 最大轮数 | ⭐ 实验里 **500 runs / 系统**（`MaxTraces`；`MonitorBudget` 具体值原文未提供） |
| ⭐ **有无报循环边际收益** | ⭐⭐ **有，而且方向与我们一致** |

⭐ **M** 逐字（§5.3）：`"the average number of revision runs throughout 500 system iterations is less than 10, indicating the effectiveness of our revision process. While the initial likely invariant learned by RunVS frequently necessitates revision, subsequent iterations yield likely invariants with improved persistence"`

⭐ **Table 2 逐字抄**（`⌈r⌉` = 500 次运行里触发修订的平均次数；`⌈f⌉` = 最后一次修订之后仍未被推翻的运行数；`T_r` = 每次修订的平均执行时间/秒）：

| 系统 | 可达状态数 | 已访问/可达比 | `⌈f⌉` | `⌈r⌉` | `T_r`(s) |
| :-- | --: | --: | --: | --: | --: |
| Peterson (Binary Processes) | 16 | 1 | 499 | **2** | 0.012 |
| Bakery | 8 | 1 | 494 | **5** | 0.084 |
| Manna Pnueli | 18 | 0.61 | 498 | **3** | 0.015 |
| Hajek | 256 | 0.13 | 498 | **3** | 0.015 |
| Traffic Lights | 200 | 0.065 | 499 | **2** | 0.004 |
| Producer Consumer | 1.03M | 0.00044 | 497 | **3** | 0.049 |
| Peterson (N Processes) | 19.5M | 0.00018 | 496 | **4** | 0.070 |
| Alternating Bit Protocol | ∞ | ≈0 | 499 | **1** | 0.013 |
| Leader Election | 26K | 0.0024 | 459 | **9** | 0.015 |
| UPPAAL train/gate | 16.8M | 0.000024 | 490 | **8** | 0.021 |
| Salesman | ∞ | ≈0 | 302 | **4** | 0.033 |
| Distributed Lock Server | 12.2K | 0.015 | 355 | **6** | 0.024 |
| Smart Contract (Ethereum Tx) | ∞ | ≈0 | 499 | **1** | 0.022 |
| P Until Q | 4 | 1 | 499 | **1** | 0.366 |
| Starvation Freedom | 2 | 1 | 499 | **1** | 0.374 |
| Eventually | ∞ | ≈0 | 499 | **1** | 0.672 |

⭐⭐ **这张表读出来的东西正是我们那条「第 3–5 轮零收益」的同构版本**：500 轮里真正产生修订的只有 **1–9 次**，且 `⌈f⌉` 普遍在 459–499（即最后一次修订之后 90%+ 的轮次都白跑）。⭐ **差别在成本**：他们白跑的每一轮只花 `T_r ≈ 0.004–0.672 s` 的确定性计算，⛔ 我们白跑的每一轮花的是 LLM token（79%）。⭐ **同一个「收益早期就见底」的现象，在确定性裁决者下几乎免费，在 LLM 自评裁决者下极贵。**

### B5 · ⭐⭐ 中间表示（⛔ 本卡第二重要的一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有** |
| 形态 | ⭐ **原子谓词集 `atoms`** + SyGuS 语法 `G`（M，§4）：$\phi ::= \mathrm{atom}(p) \mid \lnot \phi \mid \phi \land \phi \mid \phi \lor \phi$ |
| ⭐ **是否闭合** | ⚠️⚠️ **必须分两层说，否则会得出错误结论** |
| ⭐ **谁选类** | ⭐⭐ **不是 LLM，是决策树的信息增益** |

**第一层 · 集合从哪来 → 开放（LLM 自由生成）**

- **M** 逐字（§1，与前作 LIDO 的差别）：`"(1) we do not require the user to provide the set of predicates that may appear in the likely invariant, instead discover these predicates using a large language models (LLM)"`
- **M** 逐字（§3）：`"When the LLM suggests concrete predicates, we extract predicate templates from these examples by abstracting away concrete numeric values for constants. These templates are used to ensure coverage over the space of potential predicates."`
- ⭐ 即：**LLM 生成 → 确定性抽象成模板 → 确定性实例化**。⛔ 不存在任何预编目录。

**第二层 · 生成完之后 → 闭合（冻结成有限集）**

- **M** 逐字（§3）：`"the resulting set is denoted by atoms. These predicates form a finite collection of instantiated atomic predicates."`
- ⛔ 一旦冻结，**循环里没有任何机制回来改这个集合** —— 修订只改 `reached` / `speculated` 两个样本集和学出来的 φ，⛔ 不改 `atoms`。

**第三层 · 谁从集合里选 → ⭐⭐ 确定性算法**

- **M** 逐字（§4 `Decision Tree Learner`）：`"The choice of predicate is guided by the concept of information gain, a metric based on Shannon entropy[45] … The predicate with the highest information gain is selected to maximize this separation at each decision point."`
- ⛔ **LLM 完全不参与选类。**

⭐⭐ **所以「闭合 + LLM 自动选」这一格，本篇不填。** ⭐ 它填的是一个**新格子**：

| | 集合来源 | 选类者 |
| :-- | :-- | :-- |
| **我们（v46）** | ⭐ 预编 19 条（人写） | ⭐ **LLM** |
| ⭐ **本篇（RunVS）** | ⭐ **LLM 生成** | ⭐ **确定性算法（信息增益）** |

⛔ **两者恰好互为镜像。** ⚠️ 这本身是 L3 至今最干净的一条对照结果 —— 它说明「LLM 该放在词表的哪一端」在文献里**存在与我们相反的选择**，且那个选择是被论证过的。

### B6 · 模型

| 项 | 值 |
| :-- | :-- |
| 型号 | ⛔⛔ **`gpt-3.5-turbo`**（M 逐字，§4 末：`"We adopt the gpt-3.5-turbo LLM and use API calls to obtain predicates in our experiments."`） |
| 版本 / 快照 | ⛔ **原文未提供**（无 `-0125` 一类快照标识，无调用日期） |
| 多模型对照 | ⛔ **无** |

⚠️⚠️ **这一条必须重重打折。** `gpt-3.5-turbo` 是 2023 年的模型，比 X1 用的 `gpt-5.5` / `claude-opus-4-7` 差**至少两个世代**。⭐ 推论方向要小心：他们「不敢让 LLM 做选类」这个设计决定，⛔ **可能只是 2023 年模型能力的产物，而不是一条仍然成立的设计原则**。⭐ 反过来说，`gpt-3.5-turbo` 生成的谓词集就已经足够支撑 13/16 系统的安全性证明 —— **这说明「造词表」这个任务对模型能力的要求不高**（S，从「用最弱模型也拿到该结果」推出）。

### B7 · ⭐ 确定性成分（⛔ 几乎全部）

| 环节 | 是什么 |
| :-- | :-- |
| `SampleTrace` | ⭐ **Spin 模拟器**采样有限长 trace |
| 谓词模板抽象 / 实例化 | 常量抽象 + 枚举实例化 |
| 反例判定 | 状态集合成员判定 |
| `speculated` 负例采样 | 从 `S \ (speculated ∪ reached)` 随机采 `ℓ` 个，受 $\vert speculated\vert / \vert reached\vert < \alpha$ 约束 |
| `Learner` | ⭐ 决策树（Shannon 熵 / 信息增益，深度上限 `k`）+ 子采样 + signature 位向量运算 |
| 语法 `G` | ⭐ SyGuS 强类型规则（`"The syntactic rules for atomic predicates ensure strongly typed expressions."`，M） |
| ⭐ Soundness 判定 | ⭐⭐ **Spin model checker** |
| ⭐ Safety 判定 | ⭐⭐ **SMT solver**（M：`"Safety of the invariant is verified by an SMT solver to check if φ∩Unsafe is empty for some user-provided Unsafe set."`） |
| Tightness 估计 | model counting |

⭐⭐ **8 个阶段里 7 个确定性，且两个 sound oracle 都在评测端。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **有 · Daikon\*（multi-run）** —— ⭐ 口径设计干净：把 Daikon **塞进他们自己的框架替换 `Learner`**，其余不变。**M**：`"In our experiments, Daikon is used to substitute Learner, while the operational framework of RunVS remained unchanged."` + `"we ensured that both Daikon* and RunVS generated invariants using the same traces simulated from Spin"` |
| `dataset` | ⭐ **16 个 Promela 分布式系统**（13 个「条件不变式」类 + 3 个时序性质类），来源 Spin 相关资源与分布式系统文献；⭐ 含一个 **962 LoC / 21 共享变量**的以太坊智能合约。⭐ 分母口径：Table 1 的 16 行就是分母，⛔ 无抽样、无剔除 |
| `metrics` | ⭐ 三个质量指标：**Tightness**（满足 φ 的状态总数，model counting 估）· **Soundness**（Spin 确认）· **Safety**（SMT 查 `φ ∩ Unsafe = ∅`）；⭐ 三个效率指标：`⌈f⌉` · `⌈r⌉` · `T_r`。⛔ **无 `@k` 之类多轮口径** —— ⚠️ 但 `⌈f⌉` / `⌈r⌉` 在功能上就是「稳定性 vs 能力」的分离报告（S） |
| ⭐ `judged_by` | ⭐⭐ **全自动 sound oracle** —— Spin（soundness）+ SMT（safety）+ model counting（tightness）。⛔ **无人工判定 · 无 LLM-as-judge · 无标注者一致性**（也不需要：判定对象是集合包含关系，有唯一正确答案） |
| `human_baseline` | ⛔ **无** |
| `runs` | ⭐ 每系统 **500 runs**，`⌈f⌉` / `⌈r⌉` / `T_r` 报**平均**（且取上界）。⛔ **无方差 · 无置信区间 · 无重复实验 · 无 seed 说明 · Table 1 的 ✓/✗ 是单次结果还是多次一致未说明** |
| ⭐ `adverse_results` | ⭐⭐ **主动买一个必败类进来，并把失败写在正文里** |

⭐⭐ **`adverse_results` 这一格是本篇最值得学的地方**（⛔ 与 L3 另一篇形成尖锐对照）：

1. ⭐ **主动纳入一个已知会失败的子类，并说明纳入目的就是展示局限**。**M** 逐字（§5.1）：`"We further tested on 3 systems with temporal properties, Eventually, P Until Q, and Starvation Freedom, to demonstrate the boolean expression learning's limitation on temporal properties."` ⭐ Table 1 里这 3 行的 Safety 列 **RunVS 与 Daikon\* 双方全 ✗**。
2. ⭐ **主结果如实带分母**：Safety 列 RunVS **13/16 ✓**（⛔ 不是「全部成功」），Daikon\* **1/16 ✓**。
3. ⭐ **Limitations 段落写的是可验证的具体缺陷，不是套话**：**M** 逐字：`"it does not guarantee the soundness of them, since a model checker is not employed during the synthesis process"` · `"As the number of subsampled positive states increases, memory explosion may occur."` · `"The current system state extractor, based on log information, is not sufficiently general to handle all possible log information formats."`

⚠️ **但有一处不利结果他们**没有**报**：⛔ **LLM 谓词发现本身的贡献没有被测量**。论文支持「LLM 生成」与「用户指定」两条路，⛔ 却**没有做 ablation** 对比二者产出的不变式质量。⭐ 也就是说，署名贡献 (iv) 在实验里**没有单独的证据**。⚠️ 这一点对我们直接相关：我们「15/19 谓词使用率」那个问题，在他们的框架里对应「LLM 生成的 `atoms` 里有多少真被决策树选中」—— ⛔ **他们同样没报。**

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据（⭐ `tools.verify_assets` 输出逐字） |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [r-mukund.github.io/pdf/2025-SAC.pdf](https://r-mukund.github.io/pdf/2025-SAC.pdf) | `🟢 HTTP 200 · application/pdf` ⭐ 已下载 706,111 bytes，`tools.pdf_extractor -m text` 成功提取 **9 页**，标题 / 作者 / DOI / ACM Reference Format 与 Crossref 记录一致 |
| 论文全文（出版社） | ⚠️ 🟠 | [doi.org/10.1145/3672608.3707984](https://doi.org/10.1145/3672608.3707984) | `🟠 HTTP 403 · HTTPError 403` ⛔ ACM DL Cloudflare 拦截（`curl` 与 `WebFetch` 双双 403）。⚠️ 论文是 **CC BY 4.0 Gold OA**（Unpaywall `is_oa=True, oa_status=gold, license=cc-by`），⛔ 但入口实际取不到 |
| ⭐ **实验代码（RunVS）** | ⛔ ⚪ | —— | ⛔ **原文未提供** —— 全文 grep `github` / `available` / `artifact` / `zenodo` / `repositor` **零命中**（唯一 GitHub 链接是参考文献 [35] 的第三方 benchmark）。⭐ GitHub Search API `RunVS invariant` → `total_count: 0` |
| ⭐ **数据集 / Benchmark** | ⚠️ 🟠 | [github.com/gagansh7171/SPIN-Model-Checker-Programs](https://github.com/gagansh7171/SPIN-Model-Checker-Programs) | `🟢 HEAD 9cefbf616a · 文件 8（非文档 7）· release 0 · license 无` —— ⚠️ **我下调为 🟠**：这是参考文献 [35] 的**第三方** Promela 仓库，仅覆盖 3 个时序性质系统；⛔ 其余 13 个系统的 Promela 源码**原文未提供获取入口**，⛔ 且 16 个系统里哪一个对应哪个来源无逐条映射 |
| 实验结果细则 | ⚠️ 🟠 | 论文 Table 1 / Table 2 | ⭐ Table 1（16×6 的 ✓/✗）与 Table 2（16×7 数值）已逐字抄入本卡 B4 与 C；⛔ **无可下载逐条结果**、⛔ 无学出的不变式表达式清单（只有正文里 Peterson 的 `φ₁ ≡ flag[1]=0` 一个例子） |
| Artifact / 复现包 | ⛔ ⚪ | —— | ⛔ **原文未提供**（无 Zenodo / 4open / OSF / AE badge） |
| ⭐ **prompt 是否公开** | ⭐ 🟢 | 论文 Fig. 3 | ⭐ **完整 3 段 prompt 在论文正文内**（Task / Program / Constraints，含 one-shot 示例 `lock_available == true`），⚠️ `[global_variables]` 与 `[... code ...]` 为占位符 |

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐ **「LLM 只在入口调用一次，循环内全确定性」这个拓扑，是我们 5 个 LLM 节点的极端反面，且它跑得通。** ⭐ 具体可搬的设计决定：**把 LLM 的职责压缩到「造中间表示」这一件事上，选类与判定全交给确定性算法**。⭐ 对照我们：`split_requirements` 同时干抽取 + 选谓词两件事，⛔ 而「选谓词」这一半在他们那里是信息增益干的。
2. ⭐⭐ **他们把 sound oracle 移出循环，并给出了一条可复用的论证**：把 model checker 放进合成循环，会让方法的可扩展性被验证工具的可扩展性绑死（M 逐字见 B4）。⚠️ **这对 M1 的第二条设计原则（「裁决者换成 sound oracle」）是一条反向证据**，⛔ 必须正面处理：我们要么论证 pyfcstm 的求值成本远低于 model checking（很可能成立，它不做穷尽搜索），要么承认这条原则在他们的语境下不成立。⭐ 无论哪种，这是 M1 论证里**必须引的一篇**。
3. ⭐ **`⌈f⌉` / `⌈r⌉` 这对指标可以直接搬**：`⌈r⌉` = 总共触发过几次修订（≈ 能力用了几次），`⌈f⌉` = 最后一次修订之后白跑了几轮（≈ 收益何时见底）。⭐ 我们那条「第 3–5 轮零收益」如果用这对指标报，会比现在的表述更硬，⛔ 而且是有文献先例的报法。
4. ⭐ **`adverse_results` 的做法可直接照搬**：**主动买一个已知必败的子类进实验，并在方法学层面解释它为什么必败**（他们买了 3 个时序性质系统，理由是布尔表达式学不了时序）。⭐ 这与我们的 `00x8` 永久排除形成有意思的对照 —— ⚠️ **他们的选择是「留下来并解释」，我们的选择是「排除并解释」。** ⛔ 两条路都合法，但他们那条在读者眼里更难被质疑成剔除不利样本。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔ **署名贡献没有对应的 ablation。** 贡献 (iv) 是「LLM-aided predicate prompting」，⛔ 但实验里**从未把「LLM 生成的 atoms」与「用户指定的 atoms」对比过**。⭐ 我们不能重复这个错：M1 若把「LLM 自动选谓词」列为贡献，就必须有一个「人挑谓词」的对照臂。
2. ⛔ **谓词集冻结后没有反馈回路。** 若 LLM 漏了一条关键谓词，外层循环跑满 500 轮也学不出正确的不变式，⛔ 而**这个失败模式在论文里既没有被测量也没有被讨论**。⚠️ 这正是我们「15/19 使用率」问题的镜像风险：⛔ **词表的完备性缺陷会伪装成学习失败。**
3. ⛔ **`gpt-3.5-turbo` 的结论不可外推。** ⚠️ 「不敢让 LLM 选类」这个决定，⛔ 很可能只是 2023 年模型能力的产物。⭐ 引用本篇时必须同时标注模型代次，⛔ 不得写成「文献表明 LLM 不适合选类」。
4. ⛔ **无方差、无重复。** Table 1 的 ✓/✗ 是单次还是多次一致没说；⛔ 我们不要学这个（我们已有 `hit@1/@3/@all` 三口径，比它严）。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⛔⛔ **判定对象根本不同，这是最硬的一条。** 他们的裁决问题是「这个状态在不在 `⟦φ⟧` 里」—— ⭐ **有唯一正确答案，且判定成本是 O(表达式求值)**。⛔ 我们的裁决问题是「这份制品有没有违背这条 NL 需求」—— ⛔ **没有可枚举的 ground truth 集合**，这正是我们要花 574 位人工逐位判定的原因。⭐ **所以「裁决者做成纯确定性」在他们那里是免费的，在我们这里不是。** ⛔ 能搬的是**拓扑**（LLM 靠前、判定靠后），⛔ 不是他们的裁决器。
2. ⚠️ **「谓词」二字同名不同物**（见卡首警告）。⛔ 论文里绝不可写「文献中的谓词词表有 N 条而我们有 19 条」这类句子；⭐ 若要引，必须写清「其 predicate 指对程序状态求值的原子布尔表达式，与本文的检查算子不同层」。
3. ⛔ **边界外**：分布式并发协议、交错语义。⭐ 按本轨规则可读可抄形态，⛔ 但按 L1 / L2 的边界门它**不能进论文的出处或对照**（防火墙见 [README.md](../README.md) §3）。
4. ⚠️ **他们的中间表示是「表达式的原子」，我们的是「提问的算子」。** ⭐ 他们的 atoms 越多越好（决策树会挑），⛔ 我们的谓词越多越糟（模型要选，选错就白问）。⛔ **「开放生成词表」这条不能照搬到我们这边**：我们没有信息增益那样的自动筛选器兜底。

---

## F. 存疑与未核项

1. ⚠️ **ACM DL 出版版全文未取到** —— 已试 `curl -A Mozilla https://dl.acm.org/doi/pdf/...`（403）、`WebFetch` 同一 URL（403 Forbidden）、`doi.org` 跳转（403）。⭐ 改用作者主页 PDF，⛔ **两版未逐页对拍**（已核标题 / 6 位作者 / DOI / ACM ISBN / SAC '25 页眉 / CC BY 声明一致）。
2. ⚠️ **页码 1721–1729 未亲自核验** —— 来自 WebSearch 摘要转述 dblp；⭐ 论文 ACM Reference Format 自称 `9 pages`（与区间宽度一致），⛔ 但我没有打开 dblp 页面读该字段。⛔ **写 BibTeX 时须先核 `pages`。**
3. ⚠️ **`atoms` 集合的实际规模原文未提供** —— 每个系统 LLM 生成多少条谓词、实例化后有多少条、决策树实际用上多少条，⛔ 全部未报。⭐ 全文 grep 数字与 `atoms` 上下文无命中。
4. ⚠️ **`MonitorBudget` / `δ` / `k` / `α` / `ℓ` 的实验取值原文未提供** —— Algorithm 1 把它们列为输入，⛔ §5 未给具体数值。⛔ **本篇不可复现。**
5. ⚠️ **Table 1 的 ✓/✗ 是单次还是多次一致未说明**；⛔ Tightness 列的「✓」判据（多紧才算 ✓）也未给阈值。
6. ⚠️ **LLM 调用日期与 `gpt-3.5-turbo` 快照未提供** —— ⛔ 无法定位是哪个版本，provider drift 不可复核。
7. ⚠️ **后续工作是一条重要线索但本轮未读** —— FMCAD 2025 `Guiding Likely Invariant Synthesis on Distributed Systems with Large Language Models`，PDF 入口已机械核验可取（[repositum.tuwien.at](https://repositum.tuwien.at/bitstream/20.500.12708/219559/1/Xia%20Yuan%20-%202025%20-%20Guiding%20Likely%20Invariant%20Synthesis%20on%20Distributed%20Systems%20with...pdf)，`🟢 HTTP 200 · application/pdf`）。⛔ **据 WebSearch 摘要**它把 LLM 推进到 `Learner` 的位置（`ISyn`，用 LLM 替换决策树学习器）—— ⛔ **这是搜索摘要转述，不是我核过的事实**，⚠️ 但若成立，它意味着**同一批作者在一年内从「LLM 造词表 + 确定性选」走向「LLM 全包」**，⭐ 那对 M1 的价值高于本篇。⭐ **建议单独抽卡。**
8. ⚠️ **CCF 等级未定** —— 本仓库 [ccf_venues/](../../../../../ccf_venues/) 零命中，⛔ 本轮未查官方 CCF 目录，故记「未收录」而非「无」。
9. ⚠️ **前作 [41]（VMCAI 2025, LIDO）未读** —— 本篇多处把细节推给它（`"Examples of parameterized atoms and algorithms can be referred to [41]."`），⛔ 即**参数化谓词的具体形态在本篇里是缺失的**。⭐ PDF 入口存在（[r-mukund.github.io/pdf/2025-VMCAI.pdf](https://r-mukund.github.io/pdf/2025-VMCAI.pdf)，来自作者主页链接列表），⛔ 本轮未下载未读。
