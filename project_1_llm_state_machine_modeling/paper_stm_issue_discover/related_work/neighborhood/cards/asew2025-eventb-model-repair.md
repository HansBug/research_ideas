# 卡片 · On Effectiveness of Formal Model Repair by Large Language Models

⛔⛔ **全文不可得。⭐ 本卡的每一节都只据摘要 + 参考文献表 + 会议 ToC 写成。**

⭐ 三条**我实际访问过**的证据源（⛔ 别的都拿不到）：

| 来源 | 我实际做了什么 | 拿到了什么 |
| :-- | :-- | :-- |
| ⭐ DOI 解析 | `WebFetch https://doi.org/10.1109/ASEW67777.2025.00033` | ⭐ **302 → `ieeexplore.ieee.org/document/11334438/`**，⭐ DOI **真实存在**。⛔ 目标页 WAF 拦截，正文 0 字节 |
| ⭐ Crossref API | `curl https://api.crossref.org/works/10.1109/ASEW67777.2025.00033` | ⭐ 标题 / 页码 `121-128` / 会议全称 / 地点 Seoul / 三位作者与单位 / **完整 11 条参考文献表** |
| ⭐ Semantic Scholar API | `curl .../graph/v1/paper/DOI:...` | ⭐⭐ **完整出版方摘要**（⭐ 本卡 B / C 两节的全部 M 级依据）。⭐ `isOpenAccess: false`，`openAccessPdf.url: ""` |
| ⭐ ASEW 2025 ToC | ⭐ 实际下载 `proceedings.com/content/084/084000webtoc.pdf`（**378 559 B**）并用 `tools.pdf_extractor` 抽成 10 页文本 | ⭐⭐ **独立确认所属 workshop = ASYDE 2025**，⭐ 起始页 121（⭐ 下一篇 129，故 121–128 无误），⭐ 三位作者单位逐字 |
| ⭐ OpenAlex | `curl https://api.openalex.org/works/doi:...` | ⭐ `oa_status: "closed"` · `best_oa_location: null` · `any_repository_has_fulltext: false` |

⚠️ **摘要的传递链要说清楚**：⛔ 我**没能**直接读 IEEE Xplore 的页面（WAF 返回空）；⭐ 摘要是从 **Semantic Scholar API 镜像的出版方摘要**取得的。⭐ 逐字文本见下方 §B-补。⛔ 我未能拿到第二个独立来源交叉核对摘要文本。

⛔⛔ **因此：⭐ 本卡凡标 **M** 的只能是摘要原句；⭐ 凡涉及数据集规模、模型型号、裁决机制、最大轮数、逐轮数字、失败类型分布 —— ⛔ 一律「原文未提供（全文不可得）」。⛔ 我不会为了把卡填满而猜。**

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `asew2025-eventb-model-repair` |
| `title` | On Effectiveness of Formal Model Repair by Large Language Models |
| `year` | ⭐ **2025**（⭐ `published-print` = `2025-11-16`，⭐ 即会议首日；⛔ 非 early-access 年） |
| `venue` | ⭐⭐ **ASYDE 2025** —— 7th International Workshop on Automated and Verifiable Software sYstem DEvelopment，⭐ 收录于 *2025 40th IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW)*，⭐ pp. **121–128**，⭐ Seoul, Korea，⭐ 2025-11-16 ~ 11-20 |
| `ccf` | ⛔ **无。** ⭐ 主会 ASE 是 CCF A（[ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 的 `conf-a-ase` 🏆），⛔ **但 CCF 目录收录的是主会，⛔ 不收 workshop**；⭐ ASEW / ASYDE **不在 CCF 目录内** |
| `doi` | [`10.1109/ASEW67777.2025.00033`](https://doi.org/10.1109/ASEW67777.2025.00033) —— ⭐ **本轮实际解析，302 → `document/11334438`，真实存在** |
| `arxiv` | ⛔ **无**（⭐ 已用 arXiv API 按标题与三位作者名分别检索，⛔ 0 命中） |
| `url` | ⭐ [ieeexplore.ieee.org/document/11334438](https://ieeexplore.ieee.org/document/11334438/)（⛔ 付费墙 + WAF） |
| 作者 / 单位 | ⭐ **Sebastião Carvalho**（Instituto Superior Técnico, Portugal）· **Tsutomu Kobayashi**（⭐ **Japan Aerospace Exploration Agency, Japan** —— ⚠️ **不是 NII**）· **Fuyuki Ishikawa**（National Institute of Informatics, Japan）。⭐ 单位逐字出自我抽取的 ASEW ToC 第 207–209 行 |
| `artifact_type` | ⭐ **Event-B 形式化模型**（⭐ machine / event / guard / action / invariant） |
| `task` | ⭐⭐ **修复**（⛔ **不是**缺陷检测 —— ⭐ 缺陷位置由变异工具构造性给定） |
| `boundary` | ⛔ **`界外`** —— ⭐ 依据用户在本轮任务中的明确裁定「**Event-B 精化属界外**」。⚠️ 但见下方注 |
| 硬门 1（基于 LLM） | ⭐ **过** —— LLM 是修复建议的产生者，⭐ 是方法的核心组件 |
| 硬门 2（行为类模型制品） | ⭐ **过** —— Event-B 在 [README.md](../README.md) §2 硬门 2 的合格制品表里**明列** |

### ⚠️ 关于 `界外` 这个标注

⭐ 按 [README.md](../README.md) §2.1 的三档字面定义，⛔ `界外` 举的例是「时间自动机 / 混成 / Petri / 进程代数 / 正交并发语义」，⛔ Event-B 不在其中任何一项的字面里。⭐ 但用户在本轮任务中明确裁定 Event-B **精化**属界外，⭐ 本卡遵从该裁定。

⭐ **精确的刻画应当是分层的**（⭐ 这对 E3 的可迁移性判断很重要）：

| Event-B 的成分 | 与 $M=(S,E,V,Tr,A)$ 的关系 |
| :-- | :-- |
| ⭐ 单层 machine 的 event = guard + action + 变量 | ⭐⭐ **与 EFSM 高度同构** —— ⭐ 这一层的经验可迁移 |
| ⛔ **refinement（精化层级）** | ⛔⛔ **界外** —— ⭐ $M$ 里没有精化关系 |
| ⛔ 集合论 + 一阶逻辑的不变式与表达力 | ⛔ **超出** $M$ 的守卫 / 动作表达力 |
| ⛔ 证明义务（proof obligations） | ⛔ ⭐ 不是制品成分，⭐ 但它是**裁决能力**上的根本差异（⭐ 见 E3） |

⭐ **L3 不设边界门**（[README.md](../README.md) §2.1：`界外` 只要标注、不排除），⭐ 故本条正常成档。

---

## B. LLM 应用形态（⛔⛔ **本节全部仅据摘要** —— ⭐ 这是本卡最残缺的一节）

### B1 · 流水线阶段（⛔ 仅据摘要，⭐ 证据级别 **S**）

⭐ 摘要能支撑的骨架（⛔ 阶段执行者有一处标 `?` 因为摘要没说）：

```
[语料] 已有的正确 Event-B 模型
  → [确定性] 变异工具：删除单个 action 或单个 guard predicate  ⟶ mutant
  → [LLM] 产出修复建议（受 System Prompt 的语法 / 规则约束）
  → [?]   把建议应用回模型（"After modifying the model according to the suggestions"）
  → [?]   判定修改后模型的正确性   ⛔⛔ 机制原文未提供
  → [LLM] Retry Prompt：指出上一轮回答里的错误，要求精化  ⟲ 回到修复建议
```

⛔⛔ **我不给「共 N 阶段 · 其中 M 个 LLM」的计数。** ⭐ 理由：⛔ 判定环节（第 5 步）的执行者未知，⛔ 应用建议（第 4 步）是自动还是手工也未知 —— ⛔ 在两个执行者未知的情况下报一个「确定性阶段数」是编造。

⭐ 能说的只有：⭐ **LLM 环节至少 2 个**（⭐ 首次修复建议 + Retry 精化），⭐ 且**很可能是同一个调用点的多轮**而非两个不同角色（**I**，⛔ 未明说）。

### B2 · 每次 LLM 调用的角色（⛔ 仅据摘要）

| 环节 | 角色 | 依据 |
| :-- | :-- | :-- |
| 修复建议 | ⭐ **`修复者`** | **M**：`"We studied the use of LLMs to generate repairs for faulty formal models of the Event-B formalism."` |
| Retry 精化 | ⭐ **`修复者`**（⭐ 同一角色的第 $k$ 轮） | **M**：`"Retry Prompts, a type of prompt that aims to refine a repair suggested by an LLM"` |

⭐⭐ **词表里其余各格全空**：⛔ 无 `生成器`（⭐ 模型是既有的，⛔ 不从 NL 生成）· ⛔ 无 `抽取器` · ⛔ 无 `分类器` · ⛔ 无 `评审者` · ⛔ 无 `规划者` · ⛔⛔ **无 `裁决者`**。

⭐ **最后这一条是 S 级但相当稳**：⭐ 摘要把判定写成一个**与 LLM 分开的独立步骤** —— `"After modifying the model according to the suggestions from the LLM, we evaluate the correctness of the modified model."` ⭐ 主语是 `we`（⭐ 方法 / 工具），⛔ 不是 LLM。⭐ 即：⭐⭐ **LLM 不判自己对不对。** ⛔ 但**判的人是谁 / 是什么** —— ⛔ 见 B4。

### B3 · prompt 策略（⛔ 仅据摘要）

| 策略 | 有无 | 依据 |
| :-- | :-: | :-- |
| ⭐⭐ **规则约束写进 System Prompt** | ⭐ **有，且是本文的命名贡献之一** | **M**：`"we propose a System Prompt that contains constraints on how to suggest repairs that respect the syntax and rules of the Event-B language"` |
| ⭐⭐ **错误反馈回灌（Retry Prompts）** | ⭐ **有，且是本文的第二个命名贡献** | **M**：`"We also propose Retry Prompts, a type of prompt that aims to refine a repair suggested by an LLM by highlighting errors in previous responses."` |
| `few-shot` / `CoT` / `self-consistency` / `RAG` / 工具调用 / 结构化输出约束 / 角色扮演 / 多智能体辩论 | ⛔ **原文未提供** | ⛔ 摘要一字未提 |

⭐⭐ **`Retry Prompts` 的形状值得单独记下**：⭐ 「把**上一轮回答里的错误**指名道姓地写进下一轮 prompt」—— ⭐⭐ **这与我们 `convert_assertions` 的契约反馈回灌、以及本仓库 CLAUDE.md §10 要求的「把解析错误作为反馈回灌给同一次调用的下一轮，指名哪个字段、缺什么、期望什么形状」是同一个形状。** ⭐ 即：⭐ 它为我们已经在用的那个机制提供了一条外部同形先例。

⭐ **prompt 是否公开** → D 节。⚠️ ⭐ 注意 System Prompt 与 Retry Prompt 是本文**命名的贡献**，⭐ 所以正文几乎必然给出其内容或模板（**I**），⛔ 但全文不可得，⛔ 事实上取不到。

### B4 · ⭐⭐ 循环与裁决者（⛔⛔ **本轨最关键的一格，⭐ 而它恰好是本卡缺得最狠的一格**）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有** —— ⭐ Retry Prompts 就是循环机制。**M** |
| ⭐⭐ **裁决者是谁** | ⛔⛔ **原文未提供。** ⭐ 只知道**存在**一个判定步骤、⭐ 且**不是 LLM 自评**（见 B2）。⛔ **是什么，摘要没说。** ⭐ 见下方「⭐ 关于裁决者的 S 级推断」 |
| 终止条件 | ⛔ **原文未提供** |
| 最大轮数 | ⛔⛔ **原文未提供** —— ⭐ 连「Retry 最多几次」这个最基本的数都没有 |
| ⭐ 有无报循环的边际收益 | ⚠️⚠️ **有方向，⛔ 无逐轮数字，⛔ 且基线缺失** —— ⭐ 见下方 |

#### ⭐ 唯一的定量结论（⭐ 逐字）

**M**：`"The results demonstrate that using Retry Prompts significantly increases the success rate of the suggested repairs, with over 80% of the faulty models in our dataset being successfully repaired."`

⛔⛔ **这个数字对我们几乎不可用，⭐ 原因是分子有、⛔ 分母与基线都没有：**

| 想知道 | 摘要给了吗 |
| :-- | :-- |
| ⭐ 用了 Retry 之后的成功率 | ⭐ **给了** —— `> 80%` |
| ⛔⛔ **不用 Retry 的成功率（基线）** | ⛔⛔ **没给** |
| ⛔ `significantly increases` 的幅度 | ⛔ **不可知** —— ⚠️ 可能是 40%→80%，⭐ 也可能是 75%→80%，⭐ 两者的方法学含义完全不同 |
| ⛔ 逐轮边际（第 1 轮 / 第 2 轮 / 第 3 轮各多少） | ⛔⛔ **没给** |
| ⛔ 分母（`our dataset` 里有几个 mutant） | ⛔⛤ **没给** |

⭐⭐ **所以它不能回答我们「第 3–5 轮零收益」那条实测。** ⭐ 它报的对照是「**有 Retry vs 无 Retry**」（0 轮 vs $\ge 1$ 轮），⛔ **不是**「第 $k$ 轮的边际收益」。⭐ 二者是不同的问题：⭐ 前者只说明「至少来一轮比不来好」，⛔ 完全不排除「第 2 轮之后就零收益」。

#### ⭐ 关于裁决者的 S 级推断（⛔ 明确标记为推断，⛔ 不是事实）

⭐ 我能拿到的间接证据有三条，⭐ 全部来自**我实际取得的 Crossref 参考文献表**（⭐ 11 条，⭐ 已逐一解析 DOI 核实标题）：

| 参考文献 | 是什么 | 指示什么 |
| :-- | :-- | :-- |
| `ref3` = [`10.1007/s10009-010-0145-y`](https://doi.org/10.1007/s10009-010-0145-y) | ⭐ **Rodin: an open toolset for modelling and reasoning in Event-B**（Abrial, Butler, Hallerstede, Hoang, Mehta, Voisin；STTT 2010） | ⭐ Rodin 在其技术背景内 |
| ⭐⭐ `ref8` | ⭐⭐ **How to interpret failed proofs in Event-B**（Hoang 2010） | ⭐⭐ **指示性最强的一条** —— ⭐ 这篇整文讲的就是「**证明失败了怎么读**」。⭐ 引用它强烈暗示流水线里有**证明失败信号**在流动，⭐ 且很可能正是 Retry Prompt 里那个 `"errors in previous responses"` 的来源 |
| `ref11` = [`10.1007/978-981-96-0617-7_2`](https://doi.org/10.1007/978-981-96-0617-7_2) | ⭐ **Repairing Event-B Models Through Quantifier Elimination**（Kobayashi, Ishikawa；ICFEM 2024） | ⭐ 作者自己的**sound 形式化修复**前作 |
| `ref9` = [`10.1007/978-3-319-98938-9_20`](https://doi.org/10.1007/978-3-319-98938-9_20) | Repair and Generation of Formal Models Using Synthesis（Schmidt, Krings, Leuschel；iFM 2018） | 形式化模型修复的既有路线 |
| `ref10` = [`10.1145/3536430`](https://doi.org/10.1145/3536430) | Fast Automated Abstract Machine Repair…（Cai et al.；FAC 2022） | B machine 修复的既有路线 |

⭐ **推断（`S`）**：⭐ 看起来判定与 Retry 反馈很可能建立在 **Rodin 的良构性检查 + 证明义务**之上 —— ⛔ 但**摘要没有一个字说这件事**，⛔ 所以这只是从「引用了 Rodin 论文 + 引用了一篇专讲失败证明如何解读的论文 + 制品是 Event-B」推出来的，⛔ **不得写成事实句**。

⚠️⚠️ **而且有一条反向线索必须一起看**，**M**（摘要末句）：`"The results also indicated directions of possible future improvements, such as combining Generative AI with formal approaches to repair failing cases."`

⭐ **这句话的存在本身削弱了「证明器已是全流程裁决者」这个读法**（**I**）：⛔ 若形式化方法已经贯穿全程，「**结合**生成式 AI 与形式化方法」就不会被列为**未来工作**。⭐ 更可能的读法是：⭐ **形式化检查用于判定与产生 Retry 反馈，⛔ 但「把修不好的那些 case 修好」需要形式化合成（⭐ 例如作者自己 `ref11` 的 quantifier elimination），⭐ 而那部分还没做。** ⛔ **这仍是 `I`。**

#### ⭐⭐ 这一格对 M1 的净价值（⛔ 说清楚它现在能给什么、不能给什么）

⭐ 我们 M1 的第二条设计原则是「**裁决者换成 sound oracle**」。⭐ 这篇**看起来**是一个现成先例 —— ⛔ **但我们需要的恰恰是「怎么接」，⭐ 而「怎么接」正是全文里的那部分。**

⭐ 可以说的（⭐ 且这一条有真价值）：⭐ 它的 Retry 循环报**显著有效**，⭐ 而它的裁决者**明确不是 LLM 自评**（B2 的 S 级证据相当稳）。⭐⭐ **这与我们 [`_ours-v46.md`](./_ours-v46.md) B4 那格的结论方向一致** —— ⭐ 我们的实测是「⛔ LLM 自评 reviewer 零收益却吃 79% token；⭐ 确定性裁决者（`precheck_and_seal`）0 token 且性价比最高」。⭐ 若它的裁决者确为确定性检查器 / 证明器，⭐ 这就是**一条外部独立证据**支持我们那条内部受控对照的结论。

⛔⛔ **但这条支持的成立与否，完全悬在那个未核的裁决者上。** ⭐ 结论：⭐⭐ **这是一条高价值但当前不可兑现的线索。⛔ 必须拿到全文才能用。** ⭐ 见 F 节的行动建议。

### B5 · 中间表示（⛔ 仅据摘要）

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **看起来无**（**S**）—— ⭐ LLM 直接在 Event-B 制品上产出修复建议，⛔ 摘要未提任何 DSL / 缺陷类型学 / 谓词族 / 中间 IR |
| 形态 | ⛔ **原文未提供** |
| ⭐ 是否闭合 | ⚠️ **要分清两件事，⛔ 别混** —— ⭐ 见下 |
| ⭐ 谁定的 | ⭐ 变异算子由**作者的工具**定（⭐ 闭合、⭐ 只有两个位点）；⛔ 修复内容由 LLM **自由生成** |

⚠️⚠️ **这一格有一个容易搞错的地方，⭐ 必须写清**：

| 对象 | 闭合性 | 谁定 |
| :-- | :-- | :-- |
| ⭐ **注入的缺陷种类** | ⭐⭐ **闭合，⭐ 且只有 2 个位点**（⭐ 删 action / 删 guard predicate） | ⭐ **变异工具**（⭐ 作者预定） |
| ⛔ **修复的内容** | ⛔ **完全开放** —— ⭐ LLM 自由产出 Event-B 片段 | ⛔ LLM |

⭐⭐ **关键**：⭐ 那个闭合的两元素集合是**评测集的构造参数**，⛔ **不是方法的中间表示** —— ⭐ 它在**注入端**，⛔ 不在**修复端**。⛔ 而修复端**是否被告知「缺的是 action 还是 guard」摘要没说**（⭐ 若被告知，那是一个相当强的提示，⭐ 会实质拉高成功率；⛔ 若没告知，任务难度高得多）。⛔⛔ **这是一个会直接改变 `>80%` 解释的关键未知项。**

⭐ **与我们的对照**：⭐ 我们是「⭐ **闭合 19 条谓词词表 + LLM 自动选**」；⭐ 它在修复端**没有任何闭合中间表示**。⛔ 所以这篇**不为我们那个组合提供先例**（⭐ 简报第二优先想数的那个格，⭐ 这篇是空的）。

### B6 · 模型

⛔⛔ **原文未提供。⭐ 摘要通篇只写 `"an LLM"` / `"LLMs"`，⛔ 没有任何型号、版本、日期、provider。⛔ 也无法知道有无多模型对照。**

⚠️⚠️ **按 schema B6 的口径，⭐ 这是一个足以让其定量结论大幅打折的缺口**：⭐ 一篇 **2025-11** 发表的 LLM 实证工作不报模型 ID，⛔ 后果是 ① 结论无法定位在能力曲线上（⭐ X1 已证明 SOTA 与上一代不是一个量级）；⛔ ② 不可复现；⛔ ③ 无法评估 provider drift。⭐ 全文里大概率有（**I**），⛔ 但取不到。

### B7 · 确定性成分（⛔ 仅据摘要）

| 环节 | 是否确定性 | 依据 |
| :-- | :-- | :-- |
| ⭐ **变异工具**（生成 mutant） | ⭐⭐ **是** —— ⭐ 机械删除单个 action / guard predicate | **M**：`"we developed a tool that generates faulty models (mutants) from existing correct models by removing a single action or guard predicate"` |
| 把修复建议应用回模型 | ⚠️ **原文未提供**（⭐ 自动还是手工未说） | ⭐ 只有 `"After modifying the model according to the suggestions from the LLM"` |
| ⛔⛔ **正确性判定器** | ⭐ **存在**，⛔⛔ **是什么未提供** | **M**：`"we evaluate the correctness of the modified model"` |
| ⭐ 与 LLM 交互的驱动 | ⭐ **是**（工具化） | **M**：`"The tool then interacts with an LLM to obtain a suggested repair for the mutant model."` |

⭐⭐ **可以说的**：⭐ 它的**评测集构造侧是完全确定性的**（⭐ 变异工具），⭐ 这是本卡最扎实的一条 —— ⭐ 也是 E1 第一条可搬点的来源。⛔ **裁决侧的确定性成分则完全不可知。**

---

## B-补 · ⭐⭐ 四个必答问题

### ⭐ 摘要全文（⭐ 逐字，⭐ 出自 Semantic Scholar API 镜像的出版方摘要）

> `"The use of formal methods is a significant contribution to developing trustworthy software; however, it can be a complex task. For this, automation with generative artificial intelligence models, such as Large Language Models (LLMs), is considered a promising approach. We studied the use of LLMs to generate repairs for faulty formal models of the Event-B formalism. To repair faulty Event-B models, we propose a System Prompt that contains constraints on how to suggest repairs that respect the syntax and rules of the Event-B language. We also propose Retry Prompts, a type of prompt that aims to refine a repair suggested by an LLM by highlighting errors in previous responses. To evaluate our method, we developed a tool that generates faulty models (mutants) from existing correct models by removing a single action or guard predicate. The tool then interacts with an LLM to obtain a suggested repair for the mutant model. After modifying the model according to the suggestions from the LLM, we evaluate the correctness of the modified model. The results demonstrate that using Retry Prompts significantly increases the success rate of the suggested repairs, with over 80% of the faulty models in our dataset being successfully repaired. The results also indicated directions of possible future improvements, such as combining Generative AI with formal approaches to repair failing cases."`

### ⭐⭐ 问题 1：「faulty model → repair」的实验骨架（⭐⭐ 这直接对照我们的台账构造方式）

| 子问 | 答 | 级别 |
| :-- | :-- | :-: |
| ⭐⭐ **缺陷怎么注入的？** | ⭐⭐ **变异（mutation），⭐ 由作者自建工具自动生成，⭐ 从「已有的正确模型」出发** | ⭐ **M** |
| ⭐ 变异算子是什么？ | ⭐⭐ **单一「删除」算子，⭐ 作用于两类元素：`action` 或 `guard predicate`。⭐ 每个 mutant 只删一个（`"a single"`）** | ⭐ **M** |
| ⭐ 有多少个？ | ⛔⛔ **原文未提供。** ⭐ 摘要只说 `"our dataset"` / `"the faulty models in our dataset"`，⛔ 无源模型数、⛔ 无 mutant 数 | ⛔ — |
| ⭐ 源模型从哪来？ | ⛔ **原文未提供**（⭐ 只说 `"existing correct models"`） | ⛔ — |
| ⭐ 分类学是什么？ | ⛔⛔ **没有缺陷分类学。** ⭐ 只有 **2 个变异位点**，⭐ 且都是**同一种形态（omission / 缺失）** | ⭐ **M** |

#### ⭐⭐ 与我们台账构造方式的正面对照（⛔ 这是本卡最有实用价值的一节）

| 维度 | ⭐ 他们（机械变异） | ⭐ 我们（LLM 生成台账） |
| :-- | :-- | :-- |
| ⭐ **真值怎么来的** | ⭐⭐ **构造性成立** —— ⭐ 真值就是「被删掉的那个元素」 | ⛔ **LLM 生成**，⛔ **人类校验 0 条**，⭐ 正在 G1 全量重标 |
| ⭐ 标注成本 | ⭐⭐ **0** | ⛔⛔ **本项目最贵的人工投入**（⭐ 574 位逐位 + 288 簇五类） |
| ⭐ 标注误差 | ⭐⭐ **0**（⭐ 定义上不可能错） | ⚠️ **未知** —— ⭐ 这正是 G1 要解决的 |
| ⭐ 可扩量性 | ⭐⭐ **任意扩**（⭐ 每多一个可删元素就多一个 mutant） | ⛔ **受人工产能硬约束** |
| ⭐ 可复现性 | ⭐⭐ **完全**（⭐ 确定性工具） | ⚠️ 台账本身可复现，⛔ 但其**正确性**依赖判定者 |
| ⛔⛔ **生态效度** | ⛔⛔ **低** —— ⭐ 人造、单点、只有缺失型 | ⭐⭐ **高** —— ⭐ 是**真实 LLM 建模缺陷** |
| ⛔ 缺陷形态覆盖 | ⛔ **1 种**（omission） | ⭐ **多种**（⭐ 含守卫写错、⭐ 层次归属错、⭐ 要素压并等 commission 型） |
| ⭐ 缺陷是否成簇 | ⭐ **不成簇**（⭐ 每 mutant 恰 1 个缺陷）→ ⭐ 归因唯一 | ⛔ **成簇**（⭐ 一个 pair 常有多条并存）→ ⛔ 归因困难 |

⭐⭐ **一句话结论**：⭐⭐ **变异法把「标注问题」变成了「生成问题」，⭐ 代价是生态效度。** ⭐ 两者不是替代关系而是**互补关系** —— ⭐ 详见 E1 第 1 条与 E2 第 1 条。

### ⭐⭐ 问题 2：修复对不对由谁判？有没有用证明器当 sound oracle？

⛔⛔ **答案：⭐ 摘要说存在一个独立判定步骤，⛔⛔ 但没说它是什么。⭐ 这是本卡最想要而拿不到的一格。**

⭐ 摘要里**唯一**相关的一句，**M**：`"After modifying the model according to the suggestions from the LLM, we evaluate the correctness of the modified model."`

⭐ 从这一句能确定的：

1. ⭐ **判定是一个独立步骤**，⛔ 不是 LLM 的自述。（**S**，⭐ 主语是 `we`）
2. ⭐ 判定的对象是「**修改后的整个模型**」，⛔ 不是「修复建议的文本」。（**M**）
3. ⭐ 判据被称为 `correctness`，⛔ 而不是 `similarity to the original` —— ⚠️ ⭐ 这是一个有意义的区别（⭐ 见下）。

⛔ **不能确定的（⛔ 且是关键的）**：

| 问题 | 状态 |
| :-- | :-- |
| ⛔⛔ 是否用了 **Rodin 证明器 / 证明义务** | ⛔⛔ **原文未提供** —— ⭐ 只有 `S` 级间接证据（⭐ 见 B4） |
| ⛔ `correctness` 的操作化定义是什么 | ⛔⛔ **原文未提供**。⚠️ 这是 `>80%` 那个数字的**判据本身** —— ⛔ 判据不明则数字不可解释 |
| ⛔ 是「⭐ 恢复出被删的那个元素」还是「⭐ 满足全部证明义务」 | ⛔⛔ **原文未提供**。⚠️ ⭐ 这两个判据**差别极大**：⭐ 前者是句法等价（严格但可能过严 —— ⭐ 等价的不同写法会被误判为失败）；⭐ 后者是语义正确（⭐ 允许与原模型不同但同样正确的修复）。⭐ 摘要用词是 `correctness` 而不是 `recovery`，⭐ **倾向**后者（**I**），⛔ 但不能定 |
| ⛔ 证明失败时的反馈是否直接进 Retry Prompt | ⛔ **原文未提供** —— ⭐ 只知道 Retry 用的是 `"errors in previous responses"`，⛔ 而「error」的来源未说 |

⭐⭐ **对 M1 第二条设计原则的意义（⛔ 诚实版）**：

⭐ 任务里的判断是「⭐ 若它用证明器当 sound oracle，⭐ 那正是我们 M1 第二条设计原则的现成先例，⭐ 务必查清它怎么接的」。⭐ **我的结论：⛔ 前提无法确认，⛔ 因此先例无法兑现。**

⭐ 但有两条**不依赖那个未知项**的收获，⭐ 值得记下：

1. ⭐ **它的裁决者明确不是 LLM 自评**（**S**，稳）。⭐ 而它的 Retry 循环报**显著有效**。⭐ 我们的实测是 **LLM 自评 loop 零收益**。⭐⭐ **两者合起来，方向上支持「裁决者的类型决定 loop 是否有收益」这个假设** —— ⛔ 但这不构成证明，⛔ 因为它的裁决者类型未知（⭐ 只知道「不是 LLM 自评」这一个否定信息）。
2. ⭐⭐ **Event-B 领域**是「⭐ 有 sound oracle 可用」的典型环境（⭐ 证明义务是形式化定义的），⭐ 而这篇**没有把 sound 修复能力用满** —— ⭐ 它把「⭐ 结合形式化方法修剩下的 failing cases」列为**未来工作**（**M**）。⭐⭐ **这本身是一条有用的情报**：⭐ 即使在 sound oracle 唾手可得的形式化领域，⭐ 当前的 LLM 修复工作也还停在「⭐ LLM 出建议 + 检查器判对错」，⛔ **而没有做到「求解器直接参与构造修复」**。⭐ 对我们的启示：⭐ M1 若把 pyfcstm 从求值端搬到裁决端，⭐ 那已经和这条线上的当代工作同档；⛔ **想更进一步（让 oracle 参与构造）在文献里也还是空地。**

### ⭐ 问题 3：有没有报「LLM 修复失败」的分布？失败类型是什么？

| 子问 | 答 | 级别 |
| :-- | :-- | :-: |
| ⭐ 失败集非空吗 | ⭐ **非空。** ⭐ `>80%` 成功 ⟹ 失败 $<20\%$ | ⭐ **S** |
| ⭐ 作者是否分析了失败集 | ⭐⭐ **是，⭐ 且分析产出了一个具体方向** | ⭐ **M** |
| ⭐ 那个方向是什么 | ⭐⭐ **「结合生成式 AI 与形式化方法来修 failing cases」** —— ⭐ **M** 逐字：`"The results also indicated directions of possible future improvements, such as combining Generative AI with formal approaches to repair failing cases."` | ⭐ **M** |
| ⛔⛔ **失败类型的分布** | ⛔⛔ **原文未提供** | ⛔ — |
| ⛔ 失败类型的分类学 | ⛔⛔ **原文未提供** | ⛔ — |

⭐ **能推的（`I`，⛔ 不得写成事实）**：⭐ 「⭐ 修不好的那些需要**形式化方法**」这个方向指向一类特定失败 —— ⭐ 看起来是**那些修复需要解约束 / 反推守卫条件、⛔ 而不是靠模式补全就能写出来的 case**（⭐ 这与作者前作 `ref11` 用 **quantifier elimination** 修 Event-B 正好对得上：⭐ QE 解决的正是「⭐ 该写什么守卫才能让不变式保持」这类需要**求解**而非**生成**的问题）。⛔ **但这是我从参考文献连出来的读法，⛔ 摘要没这么说。**

⭐⭐ **这一条对我们直接有用**：⭐ 若这个读法成立，⛔ 那么它意味着 **LLM 修复的能力边界落在「需要求解的缺陷」上** —— ⭐ 而我们 X1 的赤字之一「⛔ 问了没答对」52 位，⭐ 很可能有一部分属于同一性质（⭐ 需要求解而非生成）。⛔ **这值得在 G1 重标后单独查一次。**

### ⭐ 问题 4：边界 —— 哪些能搬，哪些不能

⭐ **判断原则**：⭐ 任务里的提法是对的 —— ⭐⭐ **实验骨架与裁决机制与制品类型无关，⭐ 因此可迁移；⛔ 制品特有的语义（精化、集合论表达力、证明义务）不可迁移。** ⭐ 具体逐项：

| 成分 | 能否搬到 project_1 | 理由 |
| :-- | :-: | :-- |
| ⭐⭐ **机械变异构造评测集** | ⭐⭐ **能，⭐ 且是本卡最值得搬的一条** | ⭐ 与制品类型完全无关。⭐ 需要的只是「⭐ 一批公认正确的模型 + 一个能删单个元素的工具」 |
| ⭐ **单点变异（一次只删一个）** | ⭐⭐ **能** | ⭐ 让归因唯一，⭐ 与制品无关 |
| ⭐ **错误反馈 Retry 的形状** | ⭐ **能**（⭐ 但我们已经在做） | ⭐ 与制品无关。⭐ 见 B3 |
| ⭐ **「规则约束写进 System Prompt」** | ⭐ **能**（⭐ 我们已经在做） | ⭐ 与制品无关 |
| ⭐ 单层 machine 的 guard / action 结构 | ⭐ **能** | ⭐ 与 EFSM 同构（⭐ 见 A 节的分层表） |
| ⛔⛔ **refinement 相关的一切** | ⛔⛤ **不能** | ⛔⛔ **界外**（⭐ 用户裁定）。⭐ $M=(S,E,V,Tr,A)$ 里没有精化关系 |
| ⛔⛔ **证明义务当裁决者** | ⛔⛔ **不能直接搬** | ⛔⛔ ⭐ 我们**没有证明器**。⭐ pyfcstm 有 parse / semantic / design / sim facade —— ⭐ 那是**检查器**，⛔ 不是**证明器**。⭐ 详见 E3 第 2 条 |
| ⛔ 集合论 / 一阶逻辑表达力带来的修复空间 | ⛔ **不能** | ⛔ 超出 $M$ 的守卫 / 动作表达力 |

---

## C. 实验（⛔⛔ **本节全部仅据摘要** —— ⭐ 缺口极大）

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **有一个内部对照：⭐ 用 Retry Prompts vs 不用**（**M**，⭐ 由 `"using Retry Prompts significantly increases the success rate"` 推出对照存在）。⛔⛔ **无外部 baseline** —— ⭐ 摘要未提与 `ref9`（Schmidt et al. 2018 synthesis 修复）、`ref10`（Cai et al. 2022 B machine 修复）或 ⭐⭐ **`ref11`（作者自己 2024 的 QE 修复）** 中任何一条对比。⚠️ ⭐ 最后那条尤其可惜：⭐ 「LLM 修复 vs 我们自己的 sound QE 修复」是最自然的对照 |
| `dataset` | ⛔⛔ **规模未提供。** ⭐ 来源：`"existing correct models"`（⛔ 哪些、多少、出自何处全未提供）。⭐ 分母的口径是 `"the faulty models in our dataset"`，⭐ 即**以 mutant 为分母**（**M**） |
| `metrics` | ⭐ **success rate**（⭐ 成功修复的 mutant 占比）。⛔⛔ **判据的操作化定义未提供**（⭐ 见问题 2）。⛔⛔ **无 `@k` 口径** —— ⭐ 摘要未提任何多次采样 |
| ⭐ `judged_by` | ⛔ **未明说。** ⭐ **S**：看起来是**自动脚本**（⭐ 摘要把它写成工具化流水线的一步：`"The tool then interacts with an LLM..."` + `"we evaluate the correctness"`）。⛔ 无第三方判定、⛔ 无 LLM-as-judge 的迹象、⛔ 无标注者间一致性（⭐ 若确为自动判定则本不需要） |
| `human_baseline` | ⛔ **无**（⭐ 摘要未提） |
| `runs` | ⛔⛤ **完全未提供** —— ⛔ 跑几次、⛔ 报均值还是单次、⛔ 有无方差、⛔ 有无置信区间，⭐ 一个都没有。⚠️⚠️ **对 LLM 实验这是硬伤**：⛔ 若 `>80%` 是单次跑出来的，⛔ 其不确定性未知 |
| ⭐ `adverse_results` | ⭐⭐ **处理得体** —— ⭐ 见下 |

### ⭐ `adverse_results` 细看

⭐ **它没有把 `>80%` 说成「解决了」。** ⭐ 摘要的收尾把剩下那不到 20% **明确点名**为一个需要**不同技术手段**（形式化方法）才能解的子集，**M**：`"The results also indicated directions of possible future improvements, such as combining Generative AI with formal approaches to repair failing cases."`

⭐⭐ **值得借鉴的写法**：⭐ ①**在摘要里就承认能力边界**，⛔ 不留到 Limitations 才说；⭐ ②**把失败集刻画成一个有性质的类**（⭐「⭐ 需要形式化方法的」），⛔ 而不是笼统说「⭐ 还有提升空间」；⭐ ③**给出的改进方向与失败性质对应**（⭐ 缺求解能力 → 上形式化方法），⛔ 不是「⭐ 换更大的模型」。⭐ 这第三条对我们写 −15.82pp 的归因段直接可用。

⛔ **但缺口也在这里**：⛔⛔ **失败分布本身没给**（⛔ 见问题 3），⛔ 所以「⭐ 那不到 20% 是什么」只能靠推。

### ⛔ 按本仓库口径的合格性评估

⭐ 按 CLAUDE.md §3.5.2（`metric@k`）与 §3.7（迭代型实验报告须自包含）的口径，⭐ 这篇的报法**在几个点上不合格**：

| 我们的要求 | 它做到了吗 |
| :-- | :-: |
| ⭐ 逐轮边际收益 | ⛔ **无**（⭐ 只有「有 vs 无」） |
| ⭐ `@k` 多轮口径 | ⛔ **无** |
| ⭐ 方差 / 多次运行 | ⛔ **无** |
| ⭐ 模型精确 ID | ⛔ **无** |
| ⭐ 分母明确 | ⛔ **口径明确（mutant），⛔ 但数值未提供** |
| ⭐ 基线数字 | ⛔ **无**（⭐ 只有「significantly increases」这个定性词） |

⭐⭐ **反向价值**：⭐ 这份不合格清单恰好说明**我们坚持 `hit@1 / hit@3 / hit@all` 三口径同报、坚持记模型精确 ID 是对的** —— ⭐ 邻域里同期的 workshop 工作并没有做到这些，⛔ 而这正是它的数字对我们不可用的原因。

---

## D. ⭐ 资产（⛔ 全文不可得 ⟹ ⭐ 除元数据外基本全部不可核验）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| ⭐ **论文全文** | ⛔⛔ **🔒** | [ieeexplore.ieee.org/document/11334438](https://ieeexplore.ieee.org/document/11334438/) | ⛔⛔ **IEEE 付费墙 + WAF。** ⭐ 逐字核验证据：⭐ OpenAlex `oa_status: "closed"` · `best_oa_location: null` · `any_repository_has_fulltext: false`；⭐ Semantic Scholar `isOpenAccess: false` · `openAccessPdf.url: ""`；⭐ DOI 302 解析成功但目标页返回 **0 字节**（WAF）。⭐ arXiv API 按标题与三位作者分别检索 **0 命中** |
| ⭐ **摘要** | ⭐ 🟢 | Semantic Scholar API | ⭐ **完整摘要已取得**（⭐ 逐字见 §B-补）。⚠️ ⛔ 单一来源，⛔ 未能交叉核对 |
| ⭐ **会议 ToC / 页码 / 单位** | ⭐ 🟢 | [proceedings.com ASEW 2025 webtoc](https://www.proceedings.com/content/084/084000webtoc.pdf) | ⭐ **本轮实际下载 378 559 B 并抽取 10 页文本**。⭐ 第 199–209 行逐字确认：⭐ `ASYDE 2025 - 7th International Workshop on Automated and Verifiable Software sYstem DEvelopment` → ⭐ `On Effectiveness of Formal Model Repair by Large Language Models  121` → ⭐ 三位作者单位。⭐ 下一篇起始页 129 ⟹ **121–128 无误** |
| ⭐ **参考文献表** | ⭐ 🟢 | Crossref API | ⭐ **11 条全部取得**，⭐ 其中 5 条 DOI 已逐一解析核实标题（⭐ 见 B4 表） |
| ⭐⭐ **实验代码**（⭐ 变异工具 + LLM 交互工具） | ⛔ **🟠** | ⛔ **未知** | ⭐⭐ **工具明确存在**（**M**：`"we developed a tool that generates faulty models (mutants)"`），⛔⛔ **但是否公开不可知** —— ⭐ 全文不可得，⛔ 无法看有无 artifact 声明。⭐ 已查第一作者 GitHub（`SebastiaoCarvalho`，⭐ 实际拉取 **24 个仓库**列表）：⛔ **无任何 Event-B / 形式化修复 / LLM 相关仓库**（⭐ 最相关的只有课程作业 `QS-P1`(Dafny) / `QS-P2`(Alloy) / `pl-p1,pl-p2`(Coq)）。⭐ 其个人站 `sebastiaodcarvalho.com` 抓取后**无发表列表** |
| ⭐ **数据集 / Benchmark** | ⛔ **🟠** | ⛔ **未知** | ⛔⛔ **规模、来源、是否公开全部不可知。** ⭐ 唯一已知：⭐ 由「已有的正确模型」经单点删除变异而来，⭐ **ground truth 构造性成立**（⭐ 真值 = 被删元素） |
| ⭐ 实验结果细则 | ⛔ **🟠** | ⛔ **未知** | ⛔ ⭐ 我手上只有摘要里的 `>80%` 一个数。⛔ 逐 mutant 结果、⛔ 逐轮数字、⛔ 失败清单**全部不可得** |
| Artifact / 复现包 | ⛔ **🟠** | ⛔ **未知** | ⛔ ⭐ 无法确认有无 Zenodo / OSF / 4open DOI —— ⛔ **因为读不到论文。** ⚠️ ⛔ 这里**不能判 ⚪**：⭐ `⚪` 的口径是「⭐ 原文明确未提供」，⛔ 而我根本没读到原文 |
| ⭐⭐ **prompt 是否公开** | ⛔ **🟠** | ⛔ **事实上取不到** | ⚠️⚠️ ⭐ **System Prompt 与 Retry Prompts 是本文的两个命名贡献**，⭐ 所以正文几乎必然给出模板或内容（**I**）。⛔⛤ **但全文付费墙 ⟹ 事实上取不到。** ⭐ 这是本卡对 M1 最实际的损失：⭐ 我们最想看的就是那个 Retry Prompt 具体怎么把错误回灌 |
| ⛔ 模型型号 | ⛔ **⚪（摘要层）** | —— | ⛔ **摘要明确未提供任何型号**（⭐ 通篇只有 `"an LLM"` / `"LLMs"`）。⭐ 全文里大概率有（**I**） |

⭐⭐ **D 节一句话结论**：⭐ **元数据层齐全且已多源核验**（⭐ DOI / 页码 / workshop / 单位 / 参考文献 / 摘要），⛔⛔ **研究层资产全部不可获取**（⛔ 全文 🔒、⛔ 代码 / 数据 / prompt / 逐条结果一律 🟠 因不可核验）。

⚠️ ⭐ **注意本卡与 [ambiguity-detection-process-modeling.md](./ambiguity-detection-process-modeling.md) 的 D 节是两种不同的失败模式**：⭐ 那篇是「⭐ 入口开放、⭐ 内容满、⛔ 但满的全是 PDF 而源码为 0」（⭐ 可读懂不可重跑）；⭐ 这篇是「⛔ 入口关闭、⛔ 什么都判不了」（⛔ 连「有没有资产」都答不出）。⭐ **后者在对照表里应当与「明确没有资产」区分开** —— ⛔ 前者是事实，⭐ 后者是我方的核验缺口。

---

## E. ⭐ 对 M1 的意义

⚠️ **前置声明**：⛔ 本节的每一条都建立在**摘要**之上。⛔ 凡依赖未核裁决机制的推论，⭐ 我都标了条件。

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **机械变异构造 ground truth —— ⭐ 这个骨架可以直接搬来做一条「校准臂」，⭐ 且对我们当前处境（⭐ 台账正在 G1 全量重标、⛔ 人类校验 0 条）价值极高。**
   ⭐ 具体形态：⭐ 从**已经人工确认正确**的 pyfcstm 模型出发（⭐ 候选见下方 E3 第 4 条），⭐ 机械删除单个迁移 / 单个守卫合取项 / 单个动作，⭐ 得到一批**真值构造性成立**的 mutant。⭐ 然后用 discover 流水线去跑，⭐ 看它能不能找出被删掉的那个东西。
   ⭐⭐ **三条好处直接对上我们的痛点**：⭐ ① **0 人工标注成本**（⛔ 而台账是本项目最贵的人工投入）；⭐ ② **可任意扩量**（⛔ 而台账受人工产能硬约束）；⭐ ③ ⭐⭐ **不依赖台账，⭐ 因此可以在 G1 重标完成之前就先跑起来** —— ⭐ 给流水线改动提供一个**独立的快速回归信号**。⭐ 这最后一条尤其要紧：⭐ 我们现在改流水线（⭐ 例如拆掉两个 LLM 自评 reviewer）**没有不依赖台账的验证手段**，⛔ 而台账本身正在被重标。
2. ⭐⭐ **「单点变异 —— 一次只删一个」这个约束值得照抄。**
   ⭐ 它让「⭐ 哪个元件是真因」**唯一确定**，⛔ 避免多缺陷交互把归因搞糊。⭐ 我们台账里的条目常常成簇（⭐ 一个 pair 多条缺陷并存），⛔ 归因困难 —— ⭐ 而单点变异集结构上没有这个问题。⭐ 副产品：⭐ 它给出一个干净的「⭐ 每格恰好 1 条期望发现」的分母，⭐ `hit@k` 的语义比在成簇台账上更清晰。
3. ⭐ **「把形式化语言的语法与规则约束写进 System Prompt」+「把上一轮的错误指名回灌」这两个形状，⭐ 是我们已在用机制的外部同形先例。**
   ⭐ 我们的 `AssertionScript` schema + 契约门 + 解析失败原地重试（⭐ CLAUDE.md §10 要求的那个形状）与它的 System Prompt + Retry Prompts 同形。⭐ 价值不在「⭐ 学到新东西」，⭐ 而在**可引用性**：⭐ 若论文要说这个形状不是我们自创，⭐ 这是一条 2025 年的邻域先例。
4. ⚠️ **（⭐ 条件性）若其裁决者确为确定性检查器 / 证明器，⭐ 则这篇是一条外部独立证据，⭐ 支持我们「⭐ 确定性裁决者付钱、⛔ LLM 自评裁决者不付钱」那条内部受控对照。**
   ⭐ 已知的是：⭐ 它的裁决者**明确不是 LLM 自评**（⭐ B2，**S**，稳），⭐ 而它的 Retry 循环报**显著有效**；⭐ 我们的 LLM 自评 loop 是**零收益**。⛔⛔ **但「⭐ 它的裁决者是什么」未核，⭐ 所以这条只能记为待兑现。**

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔⛔ **变异缺陷 ≠ 真实 LLM 建模缺陷。⭐ 生态效度是这条路线的根本代价，⛔ 且它不可通过扩量弥补。**
   ⭐ 删一个 guard predicate 得到的缺陷，⭐ 与 LLM 从 NL 建模时**真实**犯的错（⭐ 误读语义、⭐ 层次归属错、⭐ 状态遗漏、⭐ 把多个要素压成一个名字）**分布完全不同**。
   ⛔⛔ **硬纪律：⭐ 变异集的数字只能当「⭐ 仪器校准」，⛔ 绝不能当「⭐ 能力证明」，⛔ 更不能替代台账数字对外表述。** ⭐ 若论文里出现变异集的成功率，⭐ 必须与台账数字**并列且分别标注口径**，⛔ 不得混为一个分母。
2. ⛔⛔ **它只有「缺失」一种缺陷形态。⭐ 若我们照搬，⛔ 测出的仪器精度只覆盖一种形态。**
   ⭐ 删除算子只产生 omission。⛔ 而我们台账里有大量 **commission 型**缺陷（⭐ 守卫写错、⭐ 迁移接错目标、⭐ 动作赋错值、⭐ 层次归属错）。⭐⭐ **若建变异集，必须扩算子族** —— ⭐ 至少要有：⭐ 删除 · ⭐ 替换（⭐ 换运算符 / 换目标状态）· ⭐ 边界扰动（⭐ `<` ↔ `<=`、⭐ 阈值 ±1）· ⭐ 层次重挂。⛔ 只做删除等于只测了一个角。
3. ⛔⛔ **`>80%` 这个数字对我们几乎不可用，⭐ 因为基线缺失。**
   ⛔ 摘要没给「⭐ 不用 Retry 的成功率」，⛔ 所以 `significantly increases` 的**幅度不可知**。⛔ 也没有逐轮边际、⛔ 没有分母数值、⛔ 没有方差、⛔ 没有模型 ID。⚠️ ⭐ 按 §3.5.2 与 §3.7 的口径这是不合格的报法 —— ⭐ **而这恰好反证我们三口径同报的做法是对的**（⭐ 见 C 节末表）。
4. ⛔⛔ **模型型号完全未提供（摘要层）。**
   ⭐ 一篇 2025-11 的 LLM 实证工作，⛔ 摘要不给模型 ID。⭐ 后果：⛔ 结论无法定位在能力曲线上、⛔ 不可复现、⛔ 无法评估 provider drift。⭐ 按 schema B6 的口径，⛔ 这足以让其定量结论**大幅打折** —— ⛔ 而我们连打多少折都判断不了，⭐ 因为读不到全文。
5. ⛔ **无多次采样、无方差。**
   ⛔ 摘要未提任何重复运行。⭐ 我们做变异集实验时**必须**多轮并报 `@k` —— ⛔ 否则会重复它的问题。
6. ⛔ **无外部 baseline，⭐ 尤其没跟作者自己的 sound 修复方法比。**
   ⭐ `ref11` 是同一批作者 2024 年的 **quantifier elimination** Event-B 修复 —— ⭐⭐ 「⭐ LLM 修复 vs 我们自己的 QE 修复」是**最自然、最有价值**的对照，⛔ 而摘要没说做了。⚠️ ⭐ 对我们的提醒：⭐ 我们有 pyfcstm 这个确定性底座，⭐ 「⭐ LLM 臂 vs 纯确定性臂」同样是一个我们**应该做而目前没做**的对照。
7. ⛔ **修复端是否被告知「⭐ 缺的是 action 还是 guard」摘要没说。**
   ⛔ 若被告知，⭐ 那是一个相当强的提示，⭐ 会实质拉高成功率，⛔ 而 `>80%` 的含义随之改变。⭐ **我们建变异集时必须显式定这条口径并写进事前登记** —— ⛔ 否则会产生一个隐蔽的信息泄漏面（⭐ 参照 CLAUDE.md §3.5 第 1 条）。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⚠️⚠️ **任务方向相反：⭐ 它是修复，⭐ 我们 paper1 是发现。**
   ⭐ 它的输入是「⭐ 已知有缺陷的模型」，⭐ 且缺陷位置对评估者而言**构造性已知**；⭐ 我们的输入是「⛔ 不知道有没有缺陷的模型」，⭐ 要自己找。⭐⭐ **所以它的骨架能搬的是「⭐ 怎么造一个已知真值的评测集」，⛔ 不是「⭐ 怎么发现缺陷」。** ⭐ 修复环节本身属 **project_4** 的范围，⛔ 不属 paper1。
2. ⚠️⚠️⚠️ **Event-B 的裁决条件比我们强得多，⛔ 这条差别会直接限制 M1 第二条设计原则的可行上限。**
   ⭐ Event-B 有**证明义务** —— ⭐ 不变式保持、⭐ 精化正确性、⭐ 良构性都是形式化定义的义务，⭐ 可交给证明器。
   ⛔⛔ **pyfcstm 没有这套东西。** ⭐ 我们有 parse / semantic / design / sim facade —— ⭐⭐ **那是检查器，⛔ 不是证明器。**
   ⭐⭐ **所以「⭐ 裁决者换成 sound oracle」这条原则在我们这里的可行上限是「⭐ 确定性求值 + BMC」，⛔ 不是「⭐ 证明不变式」。** ⛔⛔ **这一点必须在 M1 的设计文档里说清，⛔ 不能把 Event-B 的先例照抄成我们的目标** —— ⭐ 否则会定一个我们的工具链根本达不到的目标。
3. ⚠️ **Event-B 精化属界外，⭐ 相关机制一律不可迁移。**
   ⭐ 精化层级不在 $M=(S,E,V,Tr,A)$ 内（⭐ 用户本轮明确裁定）。⭐ 可迁移 / 不可迁移的逐项清单见 §B-补 问题 4 的表。
4. ⚠️⚠️ **它的语料是「⭐ 已有的正确模型」，⭐ 我们的语料是「⭐ LLM 生成的、⛔ 正确性未知的模型」。⭐⭐ 这是搬变异法的第一个实际阻塞。**
   ⭐ 变异法的**前提**是手上有一批**公认正确**的模型。⛔⛔ **我们有 54 个 pair，⛔ 但没有一份公认正确的参考模型** —— ⭐ 那正是台账要解决的问题本身。
   ⭐⭐ **所以若要建变异集，第一步不是写变异工具，⭐ 而是先定「从什么正确模型出发」。** ⭐ 候选两条：⭐ ① **pyfcstm 自带示例 / 官方测试用例**（⭐ 优点：正确性有工具作者背书、⭐ 与我们的 DSL 天然对齐；⛔ 缺点：可能过于简单、⛔ 与我们 pair 的复杂度不匹配）；⭐ ② **少量人工修正后的 pair 模型**（⭐ 优点：复杂度匹配；⛔ 缺点：⚠️ **人工修正本身要花 G1 那样的成本，⛔ 且会引入与台账相同的标注依赖**）。
   ⛔⛔ **这个选择必须在动工前定下来并写进事前登记** —— ⭐ 因为它直接决定变异集的结论能覆盖多大范围。
5. ⚠️ **它的失败集指向「⭐ 需要求解而非生成的缺陷」（`I`），⭐ 而我们可能有一个同性质的赤字。**
   ⭐ 若 §B-补 问题 3 那个读法成立，⭐ 那么 LLM 修复的能力边界落在「⭐ 需要解约束 / 反推守卫」这类 case 上。⭐ 我们 X1 的「⛔ 问了没答对」52 位里，⭐ 可能有一部分属同一性质。⛔ **这值得在 G1 重标后单独查一次** —— ⛔ 但目前只是假设。

---

## F. ⛔ 存疑与未核项

⭐ **本卡的未核项远多于已核项。⭐ 逐条列出，⛔ 不藏。**

### ⛔ 一等未核项（⭐ 全都因为同一个原因：⛔ 全文不可得）

1. ⚠️⚠️⚠️ **⛔ 裁决机制是什么 —— 本卡最想要而拿不到的一格。** ⭐ 已试过：⛔ IEEE Xplore（⭐ DOI 302 解析成功 → `document/11334438`，⛔ 页面返回 **0 字节**，WAF）· ⛔ OpenAlex（`oa_status: closed`，`best_oa_location: null`）· ⛔ Semantic Scholar（`openAccessPdf.url: ""`）· ⛔ arXiv API（⭐ 按标题 + 三位作者分别查，⛔ 0 命中）· ⛔ Unpaywall（`is_oa: false`，`oa_locations: []`）· ⛔ CORE（**403**）· ⛔ scholar.archive.org（⭐ API 超时）· ⛔ CiNii（⭐ 1 条命中但**纯元数据**，⛔ 无正文链接）· ⛔ JAXA 机构库（⭐ WEKO3 SPA 壳，⛔ 无匹配项）· ⛔ Ishikawa NII 主页（⭐ `research.nii.ac.jp/~f-ishikawa/en/record.html` 只有 "Selected 10 Publications"，⛔ **无任何 PDF**，⭐ 全量列表只外链 DBLP）· ⛔ `f-ishikawa.github.io`（**404**）· ⛔ `group-mmm.org/~tkobayashi/`（**404**）· ⛔ researchmap（⭐ **502**，⭐ 三次重试，⭐ 站点侧故障 ⟹ **值得改日重试**）· ⛔ computer.org CSDL（⭐ SPA 壳，⛔ API 两条路径均 404）· ⛔ ULisboa / IST 机构库与 fenix 学位论文（⛔ 无匹配；⭐ scholar.tecnico API **502**）· ⛔ INESC-ID 发表库（⭐ 2.8 MB 全量检索，⛔ 无此条目、⛔ 无该作者）· ⛔ ORCID 扩展检索（`num-found: 0`）· ⛔ ResearchGate / Google Scholar（⛔ 仅经搜索摘要露出，⛔ 从未带 PDF）。⭐ **结果：⛔ 无任何开放获取副本存在。**
2. ⚠️⚠️ **⛔ 数据集规模** —— ⛔ 源模型几个、⛔ mutant 几个、⛔ 源模型出自哪里，⭐ 全部未提供。⚠️ ⭐ 这使 `>80%` 的**分母未知** —— ⛔ 若 mutant 只有十几个，⭐ 那个百分比的稳定性很低。
3. ⚠️⚠️ **⛔ `correctness` 的操作化定义** —— ⭐ 是「⭐ 恢复出被删的那个元素（句法等价）」还是「⭐ 满足全部证明义务（语义正确）」？⚠️ ⭐ 两者差别极大（⭐ 见 §B-补 问题 2）。⛔ **判据不明 ⟹ `>80%` 不可解释。**
4. ⚠️⚠️ **⛔ 不用 Retry 的基线成功率** —— ⛔ 未提供 ⟹ `significantly increases` 的幅度不可知。
5. ⚠️⚠️ **⛔ 最大 Retry 轮数与逐轮边际** —— ⛔ 全部未提供。⛔ **这直接导致本篇无法回答我们「第 3–5 轮零收益」那条实测。**
6. ⚠️⚠️ **⛔ 模型型号 / 版本 / provider** —— ⛔ 摘要通篇只有 `"an LLM"` / `"LLMs"`。⛔ 也不知有无多模型对照。
7. ⚠️⚠️ **⛔ 失败类型的分布与分类学** —— ⭐ 已知失败集非空且作者分析过（⭐ 因为给出了具体改进方向），⛔ 但分布未提供。
8. ⚠️ **⛔ 是否多次采样 / 有无方差** —— ⛔ 未提供。
9. ⚠️ **⛔ 修复端是否被告知缺失元素的类别**（⭐ action 还是 guard）—— ⛔ 未提供。⚠️ ⭐ 这是一个会改变结果含义的口径问题。
10. ⚠️ **⛔ System Prompt 与 Retry Prompt 的实际内容** —— ⭐ 它们是本文的命名贡献，⭐ 正文几乎必然有（`I`），⛔ 但取不到。⭐⭐ **这是本卡对 M1 最实际的损失。**
11. ⚠️ **⛔ 有无 artifact / 代码 / 数据公开** —— ⛔ **无法判断**（⛔ 读不到论文）。⭐ 已旁证：⛔ 第一作者 GitHub 24 个仓库中无相关项、⛔ 个人站无发表列表。⚠️ ⛔ 但**不能据此判「⚪ 明确未提供」** —— ⭐ 那是两回事。
12. ⚠️ **⛔ 是否与作者自己的 QE 修复（`ref11`）做过对照** —— ⛔ 摘要未提。⭐ 这是最自然的对照，⛔ 无法确认做了没做。

### ⚠️ 二等存疑（⭐ 方法论 / 判断层）

13. ⚠️ **⭐ 摘要文本只有单一来源。** ⛔ 我从 Semantic Scholar API 取得，⛔ **未能**用第二个独立来源交叉核对（⛔ IEEE 页面 WAF、⛔ CSDL SPA、⛔ colab.ws 无参考表）。⭐ 虽然 Semantic Scholar 镜像出版方摘要的可靠性通常很高，⛔ 但严格说这是一条未做的核验。
14. ⚠️ **⭐ 关于裁决者的 `S` 级推断依赖参考文献表，⛔ 而参考文献表证明的是「⭐ 作者知道 Rodin」，⛔ 不是「⭐ 实验用了 Rodin」。** ⛔ 我已在 B4 明确标记，⛔ 但这条推断的强度必须被后续读者正确理解 —— ⛔⛔ **它不能当事实用。**
15. ⚠️ **⭐ 「失败集是需要求解而非生成的 case」这个读法是 `I`**，⭐ 从摘要末句 + `ref11`（QE 修复）连出来的。⛔ 摘要没这么说。
16. ⚠️ **⭐ `boundary` = `界外` 是遵从用户裁定。** ⛔ 按 [README.md](../README.md) §2.1 的三档**字面**定义，⭐ Event-B 不在 `界外` 举例的任何一项里；⭐ 我在 A 节给出了分层刻画。⚠️ ⭐ 若后续要在对照表里用这个标注做统计，⭐ 建议先确认统计口径是按字面三档还是按用户裁定。
17. ⚠️ **⛔ ASYDE 2025 的 CCF 归属我按「⭐ 主会 A、⭐ workshop 不在目录」处理。** ⭐ 已查 [ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 确认 `conf-a-ase` 存在且为 🏆；⛔ 但我**未**逐字复核 CCF 第七版 PDF 关于「workshop 是否随主会收录」的表述。⭐ 按通行理解 workshop 不随主会计入，⛔ 但这条未做原始核验。
18. ⚠️ **⛔ 未核作者前作 `ref11`（Kobayashi & Ishikawa 2024, ICFEM, QE 修复 Event-B）。** ⭐ 我只解析了它的 DOI 与标题。⭐⭐ **它可能比本篇更有价值** —— ⭐ 因为它是一条 **sound 的形式化修复**路线，⭐ 而 M1 第二条设计原则关心的正是 sound oracle 怎么接。⭐ **建议单独立项调研。**
19. ⚠️ **⭐ 一条相关但未纳入本卡的工作**：⭐ **Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair**，[arXiv:2605.17475](https://arxiv.org/abs/2605.17475) —— ⭐⭐ **该 arXiv id 本轮已实际核验**：`curl https://arxiv.org/abs/2605.17475` 返回 **HTTP 200**，⭐ 页面 `<title>` 逐字为 `[2605.17475] Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair`。⛔ **但我未读其正文**；⭐ 下面这些据搜索摘要露出、⛔ **未经我核验**：⭐ 它似乎**集成进了 Rodin IDE**、⭐ 用**验证反馈**迭代修复、⭐ 并报了 `74.45 分钟/系统` 与 `0.24 分钟/证明义务` 的效率数字。⭐⭐ **若这些成立，它可能正是本篇拿不到的那些答案的替代来源**（⭐ Rodin 怎么接、⭐ 循环怎么终止、⭐ 代价多少）。⭐⭐ **强烈建议 L3 补一张这篇的卡** —— ⭐ 它开放获取，⛔ 性价比远高于继续撞本篇的付费墙。

### ⭐ 若要继续推进的三条路（⭐ 按性价比排序）

1. ⭐⭐ **优先做 `arXiv:2605.17475`（Event-B Agent）的卡** —— ⭐ 它开放获取、⭐ 且看起来覆盖同一问题域但信息量大得多。⛔ **性价比远高于继续撞这篇的付费墙。**
2. ⭐ **改日重试 researchmap**（⭐ 本轮 502 是站点侧故障）—— ⭐ 日本作者常在 researchmap 挂 PDF。
3. ⭐ **写信问第一作者** —— ⭐ Carvalho 在 Unpaywall 中标 `is_corresponding: true`。⚠️ ⛔ 邮箱我不在本卡里落地（⛔ 避免把个人联系方式写进仓库文档）；⭐ 需要时从 Unpaywall 记录或其公开 GitHub 资料取。
