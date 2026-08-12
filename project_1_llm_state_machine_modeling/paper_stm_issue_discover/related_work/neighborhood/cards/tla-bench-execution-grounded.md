# 卡片 · TLA+-Bench（execution-grounded benchmark）

⭐ **全文可得**：arXiv HTML 全文（正文 11 节 + 附录 A1–A12）已完整读过，本卡**不是仅据摘要**。

⚠️ **先说一条硬门问题（留给 M1 裁定）**：本轨 [README.md](../README.md) §2 硬门 1 写「LLM 必须是**方法的核心组件**，⛔ 只把 LLM 当被评测对象的不算」。⭐ 本文是 **benchmark 论文**：LLM 既是被评测对象，⭐ 也确实充当了一个真实的流水线阶段（**写 1300×4 套自然语言描述**）。⛔ 但它**没有**生成侧的多阶段流水线、⛔ 没有循环、⛔ 没有中间表示。⭐ 所以它对本轨的价值**不在「流水线形态」这一格，而在「裁决装置」这一格** —— 建议 M1 按「裁决者 / 判定口径 / 人工标注协议」的样本取用，⛔ 不要把它填进 [pipeline_forms.md](../pipeline_forms.md) 当成一条流水线形态证据。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `tla-bench-execution-grounded` |
| `title` | TLA+-Bench: An Execution-Grounded Benchmark and Dataset for Natural-Language to TLA+ Specification Generation |
| `year` | 2026（arXiv v1，⭐ 2026-07-26 提交；⛔ **未发表**） |
| `venue` | ⛔ **无**（arXiv 预印本）。⚠️ HTML 里 ACM 模板头残留 `Conference: The 33rd ACM SIGKDD Conference on Knowledge Discovery and Data Mining; August 2027`，⭐ 即**目标** venue 是 KDD 2027（datasets-and-benchmarks track，见 Appendix A8），⛔ 但这不等于已接收 |
| `ccf` | ⛔ **未收录** —— KDD 不在本仓库 [ccf_venues/](../../../../../ccf_venues/) 范围内（该库只覆盖 SE / FM 方向）。⭐ KDD 在 CCF 目录里属 A 类（数据挖掘），⛔ 但本文尚未被接收，按 `无 / 未收录` 记 |
| `arxiv` | [arXiv:2607.23425](https://arxiv.org/abs/2607.23425)（⭐ 我实际访问过 abs 页与 `https://arxiv.org/html/2607.23425v1`） |
| `doi` | [10.48550/arXiv.2607.23425](https://doi.org/10.48550/arXiv.2607.23425)（arXiv 自发 DOI） |
| 作者 / 单位 | Bisharat, Spencer, Ortiz, Bhadauria, Nazari, Santos, Ramos, Wang, Thiruvathukal, Läufer, Abuhamad —— 全部 Loyola University Chicago |
| `artifact_type` | ⭐ **TLA+ 模块 + 可跑的 model-checking configuration**（`.tla` + `.cfg`） |
| `task` | ⭐ **生成**（NL → 形式规约）+ ⭐⭐ **评测口径本身**（本文真正的贡献落在后者） |
| `boundary` | ⛔ **界外** —— TLA+ 是并发 / 分布式系统的时序逻辑规约语言，含 temporal property 与 fairness。⭐ 其 basic 档确实是「single-process or state-machine module over simple data」（§4 逐字），⛔ 但语言与语料整体越界。⭐ 按 [README.md](../README.md) §2.1，L3 不设边界门，只须标注 |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ 这是一条**评测流水线**，不是生成方法）

```
[人] 抓 13 个公开仓库（1,614 候选模块，已去精确重复）
  → [确定性] 审计式清洗：SANY parse + TLC + 启发式过滤（剔 314 → 留 1,300）
  → [确定性] gold / silver 分层（判据只有一条：有没有可跑的 cfg）
  → [LLM] 写 4 套 NL 描述（GPT-5 × {declarative, intent} + Claude Opus 4.5 × {declarative, intent}）
  → [人] 难度三档标签（rubric）+ 描述忠实性审计（6 名标注者，κ=0.84）
  → [LLM·被测] 单次采样生成 TLA+ 模块（只给描述，不给 cfg）
  → [sound oracle] SANY parse gate → TLC semantic gate（全可达状态空间）
  → [确定性] 冻结的 8 类失败分类器 + 两道 pass-quality 探针（substantive / mutation）
```

⭐ **8 个阶段 · 2 个 LLM 阶段 · 4 个确定性 · 2 个人工。** ⛔ **无循环。**

⚠️ 两个 LLM 阶段的性质完全不同：一个是**造数据**（写描述），一个是**被测**。⛔ 没有任何一个 LLM 阶段参与判定。

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 | 证据 |
| :-- | :-- | :-- |
| 描述生成（declarative） | ⭐ **解释者 / 翻译器**（TLA+ 源码 → 散文；⭐ 保留模块真实标识符） | **M** · §3「The declarative style keeps the module's real names and describes what it specifies」 |
| 描述生成（intent） | ⭐ **解释者**（⭐ 反向：藏掉标识符，写成 from-scratch 需求） | **M** · A11 逐字 prompt「Do not name the module's variables, operators or PlusCal structure」 |
| 被测生成 | ⭐ **生成器 / 翻译器**（NL → TLA+ 模块） | **M** · A11「You are a TLA+ specification engineer... Produce a complete, syntactically correct TLA+ specification」 |

⛔ **没有评审者、没有修复者、没有裁决者** —— 这是本文**刻意**的选择，见 B4。

### B3 · prompt 策略

`zero-shot`（被测 prompt 只有一段任务说明 + `{description}`，⛔ 无 few-shot 例子）。⛔ **无 CoT、无 self-consistency、无 RAG、无工具调用、无结构化输出约束**（要求「Output only the TLA+ specification」，⛔ 但不是受限解码）。

⭐ **prompt 全文在附录 A11**（三段：Claude 版 declarative、Claude 版 intent、⭐ 六个模型共享的 generation prompt），逐字。⚠️ **但 GPT-5 版描述 prompt 没被记录**，作者自己点明这是重构：**M** · A11「The exact GPT-5 prompts were not recorded in the release scripts. We reconstruct them as the templates below with a length guidance of 80 to 120 words rather than the 120 to 220 issued to Claude.」⛔ **而 GPT-5 declarative 恰好就是全部评测的输入** —— 作者也明说了这一点并标为 limitation。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 | 证据 |
| :-- | :-- | :-- |
| 有无循环 | ⛔ **无** | **M** · §8.1「it produces one output per specification」；A2「Each model was queried once per specification」 |
| ⭐ 裁决者是谁 | ⭐⭐ **sound oracle** —— SANY 解析器（validity gate）+ TLC explicit-state model checker（semantic gate，走**全可达状态空间**） | **M** · §3「First, $m$ must parse under the SANY parser. This is the validity gate. Second, we place the specification's reference configuration beside $m$ and run TLC.」 |
| 终止条件 | ⭐ 不适用（单次） | — |
| 最大轮数 | ⭐ **1** | **M** · A2（同上） |
| ⭐ 逐轮边际收益 | ⛔ **原文未提供**（没有循环）。⭐ **但有一个功能等价物**：把**判定口径**逐档收紧的边际衰减，见下 | — |

⭐⭐ **这一格最值得抄的一句 —— 作者明确拒绝 LLM-as-judge**：

> **M** · §7 逐字：「We grade with the exact model checker rather than an approximate proxy. **In particular, we do not use a language model as a judge. A judge introduces the same biases the resource is meant to avoid**, and prior work reports that ground-truth grading is more reliable」

⭐ **口径收紧的边际表**（⛔ 这不是「循环轮次」，⭐ 但它在结构上回答同一个问题：每加一道更严的门，还剩多少）：

| 档 | 这一档在问什么 | 正确率 | 相对上一档 |
| :-- | :-- | --: | --: |
| Configuration-aware | 把 cfg 的常量名与性质名告诉模型 | **18.7%** | — |
| Default | 模型必须自己把接口名还原对 | **10.0%** | ⛔ −8.7pp |
| Substantive | ⭐ 通过必须**动起来**（>1 个可达状态，且所查性质不是重言式、不是纯类型不变式） | **4.0%** | ⛔ −6.0pp |
| Mutation-surviving | ⭐ 被查的性质本身必须**承重**（把它换成 `TRUE` 后 TLC 仍应失败） | **1.7%** | ⛔ −2.3pp |

⭐ 分母全是 **300**（3 个前沿模型 × 100 条规约）。⭐ 前三档是**同一批 300 份输出**、只换判定规则；⛔ 只有第一档是**重新采样**（把接口名塞进 prompt 再问一遍）。

⭐ 作者管这个区间叫 **correctness envelope**：**M** · Abstract「the correct rate moves sixfold, from 10.0% to 1.7%; adding the interface-supply choice, where the model is told the configuration's names, widens the range to elevenfold, from 18.7% to 1.7%. We call this range the correctness envelope」

### B5 · 中间表示

| 子字段 | 值 | 证据 |
| :-- | :-- | :-- |
| 有无 | ⛔ **无**（生成侧）—— LLM 直接从 NL 描述产出终态 TLA+ 模块，中间没有任何制品 | **M** · §3 任务定义 |
| 形态 | ⭐ **但评测侧有两套闭合分类学**，见下 | — |
| ⭐ 是否闭合 | ⭐⭐ **两套都闭合** | — |
| ⭐ 谁定的 / 谁选类 | ⭐⭐ **失败类型学：预编 8 类 + 冻结的确定性分类器选类（⛔ 不是 LLM，⛔ 也不是人）**；⭐ **难度：预编 3 档 + 人按 rubric 选** | **M** · §7「The recorded category comes from the model checker's own output rather than from an inferred label... The classifier is frozen and deterministic, and it applies one tie-break.」 |

⭐ **闭合的 8 类失败类型学**（Table 4，逐条抄；⭐ 每类都挂了出处，⭐ 3 类自认无先例）：

| 类 | 含义 | 出处 |
| :-- | :-- | :-- |
| Parse failure | Invalid TLA+ grammar | SysMoBench, FormalBench |
| Config-binding | Names do not match the configuration | SysMoBench |
| Malformed temporal | Ill-formed temporal formula | ⭐ **this work** |
| Safety violation | A checked invariant is violated | SysMoBench |
| Liveness violation | A temporal property is violated | SysMoBench |
| Run-time error | Evaluation crashes on some state | SysMoBench |
| Deadlock | No successor state exists | ⭐ **this work** |
| Resource limit | State explosion or memory limit | ⭐ **this work** |

⭐⭐ **这张表的做法直接可搬**：⭐ 闭合类目 + 逐类挂外部出处 + **显式标出哪几类没有先例**。⭐ 这正是本仓库 [../../provenance/](../../provenance/) 三类分级在干的事，⛔ 而他们把它做进了正文表格。

⭐ 唯一的 tie-break 也写死了：**M** · §7「A generation for which the model checker finds no runnable configuration counts as a configuration-binding failure, since a missing configuration is an interface failure.」

⭐ **闭合的 3 档难度 rubric**（§4 逐字）：`basic` = single-process or state-machine module over simple data；`intermediate` = multi-process or multi-module specifications with quantifiers and non-trivial invariants；`advanced` = temporal properties, fairness, refinement, or unbounded structures。

### B6 · 模型

| 组 | 型号 | 调用日期 | 解码 |
| :-- | :-- | :-- | :-- |
| 前沿 | `gpt-5` · `claude-opus-4-5` · `gemini-2.5-pro`（hosted endpoint） | ⭐ 2026 年 7 月 | Gemini temperature 0；GPT-5 用默认（⭐ reasoning 模型拒绝显式 0）；Opus 用 provider 默认 |
| 开放 | `qwen2.5-coder-32b` · `llama-3.3-70b` · `gpt-oss-20b`（⭐ 本地 Ollama） | ⭐ 2026 年 6 月末 | provider 默认 |

⭐ **有多模型对照（6 个）**。⭐ 单样本 / 规约，生成预算 16,000 token。

⚠️ 作者**自己承认两个 provenance 缺口**：**M** · A2「The hosted endpoints were not pinned to dated snapshots, so a later query may return a different underlying model; we release the generated outputs so the graded results do not depend on re-querying.」以及 **M** · §8.1「the cross-model comparison confounds decoding with capability and the frontier ordering should be read as indicative rather than definitive.」

⭐ **这是本卡对我们最直接可用的模型代际数据点**：⭐ 我们主臂用的 `gpt-5.5` 与 `claude-opus-4-7` 比这里的 `gpt-5` / `opus-4-5` 更新一代，⛔ 所以「16% 是天花板」这个数对我们**只能当下界参考**。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 关键参数 |
| :-- | :-- | :-- |
| ⭐ validity gate | **SANY** 解析器 | ⭐ 60 秒上限 |
| ⭐⭐ semantic gate | **TLC** explicit-state model checker，⭐ 走全可达状态空间 | ⭐ 单 worker · Java 默认堆 · **300 秒 / 规约** wall-clock · ⭐ deadlock 检查保持 TLC 默认（开） |
| 语料清洗 | SANY + TLC + 启发式过滤 | 1,614 → 1,300 |
| gold / silver 分层 | ⭐ 纯机械：有可跑 cfg 且 TLC 通过 → gold；只 parse → silver | 403 / 897 |
| 失败分类器 | ⭐ **冻结、确定性**，从 TLC 输出读类别 | 8 类 + 1 条 tie-break |
| substantive-pass 探针 | ⭐ 确定性：>1 可达状态 ∧ 非重言式 ∧ 非纯类型不变式 | — |
| mutation 探针 | ⭐ 确定性：把 cfg 点名的每条 safety invariant 换成字面 `TRUE` 重跑 TLC | — |
| 完整性校验 | ⭐ 每份 released `.tla` 记 SHA-256 | — |

⭐⭐ **状态爆炸怎么处理（parent 明确问的）**：⛔ **没有显式状态数上限**，⭐ 只有时间预算兜底。逐字 **M** · A2：「state explosion is bounded by that time limit rather than an explicit state cap. A user running the released grader reproduces every table on comparable hardware, with the resource-limit category dependent on the stated time and memory budget, since a run that exhausts the 300-second limit on slower hardware or a smaller heap is recorded as a resource limit.」

⭐ **实测爆炸有多严重**：Table A4，`Resource limit` 三个前沿模型各 **1/100**。⭐ 也就是说在这个语料上 **300 秒足够，爆炸只占 1%** —— ⛔ 但这一格是**硬件依赖**的，作者自己标出了这条不可复现性。

⭐⭐ **oracle scope 的边界（⛔ 这一条不能漏）**：TLC 的判决**精确但被 cfg 限定**，⛔ 不是行为等价。逐字 **M** · §3：「Because the second gate visits every reachable state rather than a finite set of test inputs, a correct verdict is exact relative to the reference configuration and its constant bindings... **It is not a proof that $m$ reproduces the reference behavior.**」⭐ 而且 403 条 gold 里只有 **291** 条的 cfg 点了明确的 safety / temporal 性质，⛔ 剩 **112** 条「name only the specification, so they confirm only that the module runs」。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **有，且是同一批作者的前作**：FormalLM（ICSOFT 2026，206 条规约，⛔ 无精确 oracle）+ SysMoBench（ICLR 2026，⭐ 有精确 oracle 但任务是 code→model 且 model in the loop）。⭐ Table 2 是一张 8 benchmark × 7 属性的对照表 |
| `dataset` | ⭐ **1,300 条 TLA+ 规约**（403 gold + 897 silver），13 个公开仓库 / 9 个 GitHub org。⭐ 语料按 non-comment LOC 计：mean 62.3 / median 23 / advanced 档 mean 208.8 |
| ⭐ 分母怎么定的 | ⭐⭐ **一条机械规则，且方向对自己不利**：gold 的 system 类共 146 条，⭐ 剔掉 46 条 trivial fixture（**只有一个可达状态**的合法规约）→ **100 条评测集**。逐字 **M** · §8.1「Because it discards specifications every model would pass, the filter works against a high headline number rather than flattering the results.」⭐ 且被剔的 46 条**在 manifest 里逐条打了 flag**，⭐ 使用者可以自己算未剪枝的率 |
| `metrics` | `parse rate`（SANY 接受比例）· `correct rate`（TLC 通过比例）。⛔ **无 `@k` 口径** —— 单样本，作者明标「pass@k under an exact oracle is left to future work」，⭐ 并给了 ±4–7pp 的二项区间 |
| ⭐ `judged_by` | ⭐⭐ **三层，泾渭分明**（见下表） |
| `human_baseline` | ⛔ **无**（⭐ 没有人写 TLA+ 的对照） |
| `runs` | ⛔ **单次采样 / 规约**，⛔ 无方差，⭐ 但给了二项抽样误差 ±4–7pp，⭐ 并明说「small frontier differences are indicative rather than definitive」 |
| ⭐ `adverse_results` | ⭐⭐ **本文几乎整篇都是不利结果，且处理方式极干净**，见下 |

### ⭐⭐ `judged_by` 三层（⛔ 这是本卡对我们 G1 全量重标最直接的对照）

| 判什么 | 谁判 | 规模 | 一致性 | 盲不盲 |
| :-- | :-- | :-- | :-- | :-- |
| ⭐ **正确性**（主结果） | ⭐⭐ **机器**（SANY + TLC） | 全部 | ⭐ 不适用（确定性） | ⭐ 不适用 |
| ⭐ 描述忠实性 | ⭐ **6 名有 TLA+ 专长的标注者** | ⭐ 四套各抽 100 = **400 条**，⭐ **每条两人独读** | ⭐⭐ **一致率 94% · Cohen $\kappa$ = 0.84** | ⛔ **非盲**（含作者本人，⭐ 作者主动披露两次） |
| ⭐ 难度标签 | ⭐ **2 名 TLA+-literate 标注者**重标 | ⭐ 随机 **50 条**样本 | ⭐ **Cohen $\kappa$ = 0.8**，⭐ 序数加权后 **0.85** | ⛔ **非盲**（close collaborators，已披露） |

⭐ 忠实性结论：评测实际使用的那一套（GPT-5 declarative）**83% fully faithful / 14% partially / 3% unfaithful**；四套合计 **5% outright unfaithful**。

⭐ 难度标签还配了一道**机械 robustness check**：**M** · A10「we repeat the difficulty analysis with a measure derived mechanically from the TLA+ constructs each specification uses, and the same collapse appears, from 22% to 4%」，⛔ 但作者自己指出这个代理与 rubric 同源：「this measure shares a construct family with the labels, so it tests whether the labels were applied consistently rather than supplying a fully independent notion of difficulty」。

⭐⭐ **「gold / silver 各凭什么可信」—— 这是 parent 问的第 3 条，答案与直觉相反**：

- ⭐ **`gold` 不是「人工核过的」**，⭐ 而是「**TLC 判过的**」。逐字 **M** · §6：「the reference verdict for each gold specification is the model checker's verdict **rather than a human judgment**」。⭐ gold 的可信度**全部来自机器**，⛔ 一条人工都没有。
- ⭐ **`silver` 不是「弱标注」，⭐ 而是「明确更弱的保证」**：⭐ 它只声明「SANY 接受」，⛔ 不声明任何语义正确性。⭐ 它的四个用途都不需要语义判定：大规模 parse-rate 研究、⭐ 未来补 cfg 后升 gold 的候选池、⭐ 承载 canary string 让污染可检出、⭐ 支撑不被「可配置模块」偏置的语料级统计。
- ⭐⭐ **所以这一对不是「金标 vs 银标质量高低」，⭐ 而是「两种不同强度的声明，各自只说自己能证的那句话」。** ⭐ 这个设计对我们台账极有借鉴价值：⛔ 与其把 LLM 生成、人类校验 0 条的条目笼统叫「台账」，⭐ 不如按**声明强度**分层，⭐ 每层只写它能证的那句。

### ⭐⭐ 主结果（Table 6，default 档，100 条评测集）

| 模型 | Parse (SANY) | Correct (TLC) | ⭐ 膨胀倍数 |
| :-- | --: | --: | --: |
| Claude Opus 4.5 | 87% | **16%** | ⛔ 5.4× |
| Gemini-2.5-pro | 63% | 10% | ⛔ 6.3× |
| GPT-5 | 89% | 4% | ⛔ **22.3×** |
| qwen2.5-coder-32b | 29% | 1% | ⛔ 29× |
| llama3.3-70b | 23% | **0%** | ⛔ ∞ |
| gpt-oss-20b | 7% | 1% | ⛔ 7× |

⭐ **难度悬崖**（三前沿模型 pooled）：correct 从 basic 的 **25%** 掉到 intermediate 的 **2%** 与 advanced 的 **2%**，⛔ 而 parse 只从 86% 掉到 76%。

⭐ **失败画像**（Table A4）：config-binding 是三个模型的最大类（GPT-5 占其失败的 74%、Opus 73%、⭐ Gemini 只有 47% 而 parse 占 41%）。⭐ 且「At least two of the three models produce the same outcome for 85 of the 100 specifications, and all three fail in the same category on 30 (of which 29 are configuration-binding)」→ ⭐ **失败由样本驱动的程度不低于由模型驱动**。

### ⭐⭐ `adverse_results` —— 逐条可借鉴

1. ⭐ **主动把自己的头条数字打散成一个区间**，⛔ 而不是挑最好看那档报。逐字 **M** · Appendix A8：「A benchmark that leaves these implicit reports one number from a range, and our range is a factor of eleven wide, and sixfold on fixed outputs. **We suggest that resource builders in adjacent settings report the range rather than a point**」
2. ⭐ **报保守档**：「We report the pruned rate throughout, which is the conservative choice, since every excluded fixture would pass for every model.」
3. ⭐ **主动交代与自己前作的重叠，⛔ 不等人发现**：「FormalLM (5), **which is our own earlier benchmark; we state the delta explicitly rather than let the overlap be discovered.**」
4. ⭐ **把对自己不利的自评偏置当证据用**：GPT-5 被拿自己写的描述评测却在三前沿里**最低**（4%），⭐ 作者拿这条反证不存在自描述优势。
5. ⭐ **明说 mutation 那一档是下界**：12 条只查 temporal 性质的通过被判 non-surviving（⭐ 因为 `TRUE` 替换对 temporal 无效），「so the test is a lower bound on vacuity... that 1.7% is a conservative lower bound rather than a direct vacuity measurement」。
6. ⭐ **两次披露标注非盲**（§6 与 A10），⭐ 并在 A1 伦理节再披露一次。
7. ⭐ **披露 prompt 记录缺失**（GPT-5 描述 prompt 是重构的，⛔ 而它正是评测输入）。
8. ⭐ **披露解码不统一会污染跨模型排序**。
9. ⭐ **披露评测集在最难的维度上代表性不足**：「composition and refinement, where modeling is hardest, are under-represented in the evaluation set, which draws only 17 of its 100 from the 178 multi-module gold specifications.」

⭐⭐ **一句方法论总结（作者自己的）**：**M** · §1「An exact oracle is often treated as settling what a model got right. **It does not.**」

---

## D. ⭐ 资产（⛔ 全部实际去取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arxiv.org/html/2607.23425v1](https://arxiv.org/html/2607.23425v1) | ⭐ HTML 全文 476,924 bytes 已下载并通读；⭐ abs 页与 PDF 入口均可达 |
| ⭐ **实验代码 / grader** | ⭐ 🟢 | [github.com/LUC-AI4FM/tla_benchmark/tree/reviewer-release](https://github.com/LUC-AI4FM/tla_benchmark/tree/reviewer-release) | ⭐ HEAD `67f40268de8b0824e1257f111d7c8f6872f0e4a9`（2026-07-26T01:21:38Z，commit msg「TLA+-Bench reviewer release: dataset, grader, outputs, reproduce script」）· ⭐ 树内 7,295 个 blob · ⭐ **有 LICENSE**（906 bytes）· `code/validator.py` + `code/utils.py` + `code/README.md` + `code/generation/`（3 文件）+ `reproduce.py`（2,958 bytes）+ `tla2tools.jar`（4,356,704 bytes）· release 数 0 |
| ⭐ **数据集 / Benchmark** | ⭐ 🟢 | 同上仓库 `specs/` + `descriptions/` + `manifest.json{,l}` | ⭐ 逐类点过：`specs/gold` **403 个 `.tla` + 399 个 `.cfg`**；`specs/silver` **897 个 `.tla` + 45 个 `.cfg`**；`descriptions/{declarative_claude, intent_claude, intent_gpt}` 各 **1,300** 个 `.txt`，⚠️ `declarative_gpt` **1,614** 个（见 F 节）· `manifest.json` 3,833,213 bytes / `manifest.jsonl` 3,766,910 bytes · ⭐ **有 ground truth**（每条 gold 的 cfg 即参考判据；⭐ manifest 记 tier / 难度 / 类别 / 源仓库 URL / path / SHA-256） |
| ⭐ 实验结果细则 | ⭐ 🟢 | 同上仓库 `outputs/` | ⭐⭐ **有可下载逐条结果，⛔ 不只是论文内表格**：`gpt-5.json` · `claude-opus-4-5.json` · `gemini-2-5-pro.json` · `outputs/contamination/`（5 文件，开放模型结果）· `_pass_audit.json` · `all_passes_vacuity.json` · `oracle_scope_proof.json` · `eval_100_ids.json`。⭐ `reproduce.py` 声称「recomputes Table 5, the correctness envelope of Table 6, and the pass-quality counts of Section 8.7 from these verdicts, **with no model queries**」 |
| Artifact / 复现包 | ⭐ 🟡 | DOI [10.5281/zenodo.21310317](https://doi.org/10.5281/zenodo.21310317) | ⛔ **DOI 本身 HTTP 404**（`python3 -m tools.verify_assets --url https://doi.org/10.5281/zenodo.21310317` → `⚪ HTTP 404 · HTTPError 404`；`zenodo.org/records/21310317` 同样 404）。⭐ 论文脚注自己写着 "(resolves on publication)"。⭐⭐ **但脚注同时给了一个 reviewer preview token 链接，我实测 HTTP 200**：记录页标 "You are previewing a new record that has not yet been published"，Version 1.0.0，Published July 11, 2026，⭐ 单个文件 `tla-plus-bench.zip` **8.6 MB · md5 `f73710d3820ce645d5fd506f28ff6fe9`**。⭐ 判 🟡 而非 ⚪：内容确实取得到，⛔ 但走的是非正式入口且随发表状态会变 |
| ⭐ prompt 是否公开 | ⭐ 🟢 | 附录 A11 | ⭐ **三段 verbatim**：Claude 版 declarative 描述 prompt、Claude 版 intent 描述 prompt、⭐ 六模型共享的 generation prompt。⚠️ **GPT-5 版描述 prompt 未公开**，作者明写是按模板重构（80–120 词 vs Claude 的 120–220），⛔ 而 GPT-5 declarative 正是全部评测的输入 |

### ⛔⛔ 核验陷阱（⭐ 这条务必留给后续查同一仓库的人）

⭐ 机械核验工具默认查 **default branch**，⛔ 而这个仓库的 default branch 是 `main`，⛔ **`main` 上放的是他们上一篇（FormalLM）的 206 条语料，不是本文的 1,300 条**。⭐ 实测对比：

| 分支 | 机械输出 | 实际内容 |
| :-- | :-- | :-- |
| `main`（默认） | `🟢 HEAD 8fdd1ce23e · 文件 1396（非文档 1390）· release 0 · **license 无**` | ⛔ **`data/tla_files` 只有 205 个文件、`data/descriptions` 206 个** —— 这是 FormalLM 的规模 |
| ⭐ `reviewer-release`（⭐ 论文引的那个） | ⭐ 7,295 blob · ⭐ **有 LICENSE** | ⭐ 1,300 `.tla` · 444 `.cfg` · 5,514 `.txt` 描述 · 13 个 `.json` 结果 |

⛔ **只跑一次 `--url https://github.com/LUC-AI4FM/tla_benchmark` 会同时报错两件事：漏掉真正的制品、并断言「无 license」。** ⭐ 教训：**核验 GitHub 资产必须核到论文引用的那个 ref**，⛔ 不是仓库根。

---

## E. ⭐ 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐ **「不用 LLM 当 judge」这条有了一个可引的、同期的、明确的先例。** ⭐ 我们 v46 的 `adjudicate_results` 与两个 review 节点全是 LLM，⭐ 而这篇在一个**同样是 NL→形式规约**的任务上明确拒绝了 LLM-as-judge，理由一句话（judge 会引入 benchmark 本要避免的同一批偏置）。⭐ M1 若要把裁决端换成 sound oracle，⭐ 这是最干净的一条外部支撑。
2. ⭐⭐ **「pass ≠ 有内容」这条给了我们一个可搬的两级探针，⭐ 而且我们缺的正是它。** ⭐ 我们的谓词求值只判「该谓词返回 True/False」，⛔ 从不问「这条断言是不是**空转**」。⭐ 实测代价数据现成：30 条通过里只 12 条 substantive、⭐ 只 5 条 mutation-surviving，⭐ 作者一句「The plain correct rate therefore overstates genuine capability by roughly 2.5 times」。⛔ **而我们的 hit@1 60.4% 里有多少是空转，目前完全不知道。** ⭐ 他们的两道探针几乎可以逐字移植到我们的断言脚本上：
   - **substantive 探针**：断言涉及的元素在仿真里**动过**（>1 状态）∧ 所查性质不是重言式 ∧ 不是纯类型 / well-formedness 不变式
   - **mutation 探针**：把断言里的性质换成常真，重跑；⭐ **若结果不变，这条断言什么都没查**
3. ⭐⭐ **报「区间」而不是报「一个数」这个做法，⭐ 恰好对上我们 −15.82pp 的表述困境。** ⭐ 他们的处理是：把所有本来会被默默做掉的判定选择**列出来、逐档量化、明说每一档在回答哪个不同的问题**，⭐ 然后说「不同档不是同一个量的竞争估计」。⭐ 我们的 `hit@1` / `hit@3` / `hit@all` 已经是这个形状的雏形，⭐ 但还缺「口径档」这一维（⭐ 例如：命中判据松紧、多报是否计入、是否要求断言承重）。
4. ⭐ **闭合类目 + 逐类挂出处 + 显式标出「无先例」那几类**（Table 4）—— ⭐ 这与我们 [../../provenance/](../../provenance/) 的三类分级是同一件事，⛔ 但他们把它做成了正文表格的一列。⭐ 我们的 19 条完全可以照这个版式排。
5. ⭐ **人工标注的报告版式可以整套照抄**：⭐ 双读 + Cohen $\kappa$ + 序数加权 $\kappa$（⭐ 因为档位有序）+ 机械代理复验 + **主动披露非盲**。⭐ G1 正在做 33–49 人时的全量重标，⭐ 这套版式直接决定那批工作在审稿人眼里值多少。⚠️ ⭐ 特别注意他们对机械代理的自我限制：**同源的代理只能证「标注是否一致」，⛔ 不能证「难度定义是否独立成立」** —— ⭐ 这句话我们做任何自动化复验时都会用得上。
6. ⭐ **`gold` / `silver` 那个分层思路**：⛔ 不要按「质量高低」分层，⭐ 要按**声明强度**分层，⭐ 每层只写它能证的那一句。⭐ 我们台账「LLM 生成、人类校验 0 条」这个现状，⭐ 与其一口气全部重标，⭐ 不如先按声明强度切开。

### 2. ⛔ 不可取 / 陷阱

1. ⛔ **它没有循环，所以它对「循环该怎么设计」一个字都答不了。** ⭐ 想要那个答案得去看 [synthesizing-protocol-specs.md](./synthesizing-protocol-specs.md)（⭐ RQ25「Can models repair a failing spec from the TLC counterexample trace?」在本文里是**未做的 future work**）。
2. ⛔ **它的 oracle 强但被 cfg 限定，⭐ 而这个限制在我们身上会更严重。** ⭐ 403 条 gold 里 112 条的 cfg「只点了规约本身」，⛔ 即那 112 条的通过只证明「模块跑得起来」。⭐ 我们的 pyfcstm 求值端有完全相同的结构性风险：⛔ **谓词返回 True 只说明这一条谓词在这份制品上成立，⛔ 不说明制品对**。
3. ⛔ **单样本 + 无 `@k`**，⭐ 作者自己把 pass@k 列为 future work。⭐ 我们的三口径反而比它强，⛔ 不要因为它是新 benchmark 就假设它的口径更成熟。
4. ⛔ **`config-binding` 占了 64% 的失败，⭐ 而这一类里混着「建模错」与「只是名字不一样」。** ⭐ 作者自己承认这是 harness-coupled 的（§9），⭐ 靠 configuration-aware 那一档去界定上界。⚠️ ⭐ **我们的命中判定里几乎肯定有同构的问题**：⛔ 一条断言指对了缺陷但绑错了元素名，⭐ 现在算命中还是算多报？⭐ 这篇给的答案是**两档都报**。
5. ⛔ **模型代际**：`gpt-5` / `opus-4-5` / `gemini-2.5-pro` 比我们主臂低一代，⭐ 所以「最强 16%」不能拿来当我们任务难度的标尺。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| 维度 | ⭐ 它 | ⛔ 我们 |
| :-- | :-- | :-- |
| 任务 | ⭐ **生成**（NL → 规约），⭐ 判「生成对不对」 | ⛔ **缺陷检测**（模型 vs NL），⭐ 判「有没有发现缺陷」 |
| 有没有可判定 oracle | ⭐⭐ **有，且判据在制品内部**：cfg 点名的性质要么成立要么被违反，⭐ TLC 给精确判决 | ⛔⛔ **没有** —— 「这是不是一条真发现」的参照物是**台账**，⛔ 而台账是人写的（且正在重标）。⭐ 我们的 pyfcstm 能判「谓词在制品上成立否」，⛔ 判不了「这条发现对不对」 |
| 人工投入在哪 | ⭐ 花在**造标签与验描述**（难度 + 忠实性），⛔ 主判定完全无人 | ⛔ 花在**主判定**（574 位逐位 + 288 簇五类）—— ⭐ 这正是我们最贵的一项 |
| 判定能不能自动化 | ⭐ 能，⭐ 因为参考 cfg 与被判制品在**同一形式语言**里 | ⛔ **不能直接自动化** —— ⭐ 台账条目是自然语言描述的缺陷，⛔ 与断言脚本不同构 |

⭐⭐ **所以本卡对我们的正确读法是**：⛔ 别指望「照它那样换个 sound oracle 就把人工判定省掉」 —— ⭐ 它省得掉是因为它的 ground truth 本身就是可执行的 cfg。⭐ **我们能搬的是它的两道 pass-quality 探针**（⭐ 那两道**不需要** ground truth，⭐ 只需要制品与断言本身），⭐ 以及它报区间、挂出处、披露非盲这套**表述纪律**。

---

## F. ⛔ 存疑与未核项

1. ⚠️ ⭐⭐ **parent 最想要的那个数（「相似度高但其实错」的比例）⛔ 本文没量化。** ⭐ 它对「按与参考答案相似度打分」的批评是**断言 + 借来的证据**，⛔ 不是自测：Abstract 与 §1 只说「grade by resemblance to a reference... neither of which shows correctness」「graders based on textual overlap or a finite test set overstate capability」；⭐ 唯一的数字证据是**引 EvalPlus** 的「dropping pass rates by up to about 19 points and reordering models」（⛔ 那是代码任务，不是 TLA+）。⭐ 而「exact correctness vs surface similarity 到底差多少」在附录 A7 是 **RQ12**，标 `[c]`（可从已发布数据算），⛔ **本文明确没做**（本文只答了 RQ10 / 14 / 17 / 20 与部分 RQ5）。⭐ **好消息**：既然标 `[c]` 且 outputs 已公开，⭐ 这个数我们自己算得出来 —— ⛔ 但那是新工作，不是引用。
2. ⚠️ ⭐ **对「只看能不能 parse」的批评则是硬数字**：Table 6 的 parse 87–89% vs correct 4–16%（⭐ 膨胀 5.4×–22.3×），⭐ 加一句「a benchmark that stopped at parsing would rank these models as broadly capable when the model checker shows they are not」。⭐ **两种坏判据里，只有这一种被本文亲自量化了。** ⛔ 引用时不要混为一谈。
3. ⚠️ **`descriptions/declarative_gpt` 有 1,614 个 `.txt`，⛔ 比另外三套（各 1,300）多 314 个** —— ⭐ 而 314 恰好等于清洗阶段被剔除的模块数（§4 / Table A2）。⭐ 看起来是候选集阶段先给全部 1,614 个候选生成了 declarative/GPT 描述，⛔ 清洗后没同步删。⛔ **原文未提及此点。** ⚠️ 我没有逐文件比对确认这个解释，⛔ 只做到「数目吻合」这一步 —— ⭐ 已试过：GitHub `git/trees?recursive=1` 逐目录计数；⛔ 未做：把 1,614 个文件名与 manifest 的 id 集合求差。
4. ⚠️ **`specs/gold` 只有 399 个 `.cfg`，⛔ 而 gold 是 403 条** —— ⭐ 差 4 条。⭐ 另有 45 个 `.cfg` 落在 `specs/silver` 下，⛔ 而 silver 的定义是「没有可跑 cfg」。⛔ **两处都与正文口径不符，原文未解释。** ⭐ 已试过：`git/trees?recursive=1` 按扩展名分目录计数（gold.tla 403 / gold.cfg 399 / silver.tla 897 / silver.cfg 45）；⛔ 未做：拉 manifest.json（3.8 MB）逐条核 tier 与 cfg 存在性。
5. ⚠️ **Zenodo 正式 DOI 现在取不到**（404），⭐ 只有 preview token 可用。⛔ 若 KDD 2027 未接收，这个 DOI 可能永远不解析。⭐ 已试过：`doi.org/10.5281/zenodo.21310317`、`zenodo.org/records/21310317`（均 404）、⭐ 论文脚注的 preview token 链接（200）。
6. ⚠️ **`category` 标签（system / utility）是谁指派的、按什么判据 —— 原文未提供。** ⭐ 难度标签的 rubric 与信度检查都写了，⛔ 但 category 只说「we also assign... in the gold tier, a category label」与「the system category, which models a system with behavior worth checking」，⛔ 没有 rubric、⛔ 没有信度检查。⚠️ ⭐ 这一点值得注意，⛔ **因为评测集正是靠 category 切出来的**（146 = gold ∩ system）。
7. ⚠️ **`ccf` 归档我按「未收录」写。** ⭐ 判据：论文未发表，⭐ 且 KDD 不在本仓库 [ccf_venues/](../../../../../ccf_venues/) 的 30 个 venue 目录里（⭐ 我 grep 过 `KDD|SIGKDD`，⭐ 0 命中）。⛔ 若主 session 认为应按 KDD = CCF A 记，⭐ 请自行改并在 [pipeline_forms.md](../pipeline_forms.md) 注明「目标 venue，未接收」。
8. ⚠️ **本卡未核 FormalLM（ICSOFT 2026）与 SysMoBench（ICLR 2026）原文。** ⭐ 关于它们的一切陈述都是**本文的转述**（⭐ 尤其「SysMoBench grades a different task with a model in the loop」这句 —— ⛔ 若 M1 要引「别人的裁决端有 model in the loop」，⛔ 必须回 SysMoBench 原文核，⛔ 不能引这句转述）。⭐ 它们的 id：`arXiv:2509.23130`（SysMoBench）与 ICSOFT 2026（FormalLM，⛔ 无 arXiv id）。
