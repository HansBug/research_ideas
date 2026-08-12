# 卡片 · LADEX（EMSE 2026）· critique-refine 五变体消融

⭐ 本卡按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 的 A–F 六节写。⭐ **全文可得**（arXiv v3，头部逐字标 `Journal: Empirical Software Engineering`，即 EMSE 接受版），所以本卡**不是**「仅据摘要」。⛔ Springer 正式排版版被 WAF 拦下（见 D 节与 F 节）。

⚠️ **版本纪律**：⛔ 网上最容易搜到的是 **v2（2025-11-27）**，⭐ 但本卡全部基于 **v3（2026-07-06）**。⛔ 两版的统计口径不同（v2 按数据集聚合报 16/8 组比较，v3 按 `数据集 × LLM` 对报 40/20 组比较），⛔ 且 **v3 才有第 5.4 节的迭代次数统计、§7 Tool Support、§10 Data Availability、附录 D exact matching**。⛔ 引 v2 的数字会与正式版不一致。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `emse2026-ladex-critique-ablation` |
| `title` | The impact of critique on LLM-based model generation from natural language: the case of activity diagrams |
| `year` | ⭐ **2026**（Crossref 逐字 `published: 2026-07-25`；⛔ 不用 arXiv v1 的 2025） |
| `venue` | Empirical Software Engineering **32(1), article 12** |
| `ccf` | ⭐ **B**（本库 [`journal-b-ese`](../../../../../ccf_venues/journal-b-ese/README.md)，🥈；⚠️ CCF 官方页写作 `ESE`，`EMSE` 是旧称） |
| `doi` | [`10.1007/s10664-026-10923-2`](https://doi.org/10.1007/s10664-026-10923-2) —— ⭐ 已实际访问，Crossref API 返回完整记录（题名 / 刊名 / 卷期号 / 7 位作者全部对得上） |
| `arxiv` | [`arXiv:2509.03463`](https://arxiv.org/abs/2509.03463)（v1 2025-09-03 · v2 2025-11-27 · **v3 2026-07-06**），CC BY-NC-ND 4.0 |
| 作者 | Parham Khamsepour, Mark Cole, Ish Ashraf, DaYuan Tan, Sandeep Puri, Mehrdad Sabetzadeh, Shiva Nejati（University of Ottawa + Ciena） |
| `artifact_type` | ⭐ UML 活动图（形式化为 $\mathit{ad} = \langle \mathit{NL}, \mathit{TL}, N, T \rangle$，$N$ 划分为 action / decision / initial / end 四类） |
| `task` | ⭐ **生成**（NL 过程描述 → 活动图）+ **一致性检查**（critique 步骤检查良构性与语义对齐） |
| `boundary` | ⭐ `邻域`（活动图；⛔ 无时钟。⚠️ 有并发：AC4 显式定义 concurrency 与 parallel flows，但 §6.4 Limitations 逐字排除 swimlane 与 composite node：「we treat each action node in an activity diagram as atomic」） |

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐ 论文的图 3 只有 **3 个核心步骤**（Step 1 生成 · Step 2.1 critique · Step 2.2 refine），⭐ 但**五个变体的差别全在 Step 2.1 由谁执行**。⭐ 以最佳变体 `LADEX-Alg-LLM` 为例：

```
[人] 提供 NL 过程描述
  → [LLM] Step 1 生成候选活动图（CSV / Draw.io 编码）
  → Step 2.1 critique 分两路并行：
       [确定性] SC1–SC6 算法检查（形式化谓词，见 B7）
       [LLM]    AC1–AC5 对齐检查
  → [LLM] Step 2.2 refine（吃 critique + 历史被拒版本）
  → 回到 Step 2.1，≤5 轮
  → ⛔ 5 轮不收敛 → 整格丢弃、从 Step 1 冷重启
  → [确定性] CSV → UML 2.5 XMI / PlantUML / Draw.io 三路转换（§7 Tool Support）
```

⭐ **阶段总数 3（+1 个确定性后置转换）· LLM 阶段 2–3（视变体）**。

### B2 · 每次 LLM 调用的角色

| 步骤 | 角色 |
| :-- | :-- |
| Step 1 | ⭐ **生成器**（NL → 活动图 CSV） |
| Step 2.1（`*-LLM` 结构路） | ⛔ **评审者**（LLM 自评良构性） |
| Step 2.1（对齐路，⭐ 所有带对齐检查的变体） | ⛔ **评审者**（LLM 自评语义对齐） |
| Step 2.2 | ⭐ **修复者**（按 critique 改图） |
| L-Match（评测端，⛔ 不在生成流水线内） | ⛔ **裁决者 / LLM-as-judge**（判两图节点是否匹配） |

### B3 · prompt 策略

`one-shot`（Table 2 的元素 V「One-shot Example」，⭐ 只给生成与 refine 步）· `角色扮演`（元素 I「Role Definition」，⭐ 三步都有）· `结构化输出约束`（⚠️ **只是自然语言里的「Output Format Definition」+ CSV 例子，⛔ 不是受限解码、不是 JSON schema 强制**）。⛔ **无 RAG · 无工具调用 · 无 self-consistency 投票 · 无多智能体辩论。**

⭐ 值得记的一条设计理由（M，§7 逐字）：**用 CSV 中间表示是为了避免直接产复杂严格 schema 时的语法幻觉** —— 「This design choice is to mitigate the risk of syntactic hallucinations that occur when LLMs are tasked with generating complex, strict schemas directly.」

### B4 · ⭐⭐ 循环与裁决者（本轨最关键的一格）

⭐⭐ **本篇的全部价值就在这一格：它把「裁决者是算法」与「裁决者是 LLM 自评」做成了受控对照。**

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有**（4 个变体有，`Baseline` 无 —— ⭐ 这就是消融的第 1 组对照） |
| ⭐ **裁决者是谁** | ⭐⭐ **两种，按变体切换**：良构层可以是 ⭐ `确定性规则`（SC1–SC6 算法检查）或 ⛔ `LLM 自评`；⛔ 对齐层**只能是 LLM 自评**（M，§1 逐字：「alignment constraints can only be critiqued using an LLM」） |
| 终止条件 | ⭐ 收敛（critique 报无问题）**或** 最大轮数 |
| 最大轮数 | ⭐ **5** |
| ⛔ 超限怎么办 | ⛔⛔ **整格丢弃、冷重启**（见下方专段） |
| ⭐ 有无报**逐轮**边际收益 | ⚠️ **没有逐轮增量表**，⛔ 但 v3 §5.4 报了**迭代次数分布**，⭐ 那足以回答同一个问题（见下方专段） |

#### ⭐⭐ v3 §5.4 的迭代次数统计（M，逐字）

> For each LADEX variant with a refinement loop, we cap the number of refinement iterations at five. If the loop does not converge within these five iterations, i.e., if the critique step continues to identify issues, we discard the activity diagram and restart the variant from its generation step. In other words, an activity diagram produced by a given LADEX variant is accepted as that variant's output only if it passes the critique check. **Across the 12,800 diagram generation tasks that utilized a refinement loop, this five-iteration cap was reached in only 703 cases (approximately 5.5% of all tasks). Overall, the refinement process required an average of only 1.14 iterations per generated diagram.** Further, for the 703 cases that were restarted, we encountered 14 cases (approximately 1.99% of the tasks that were restarted, and 0.1% of all tasks) in which the generated activity diagrams had to be discarded more than once.

⭐⭐ **这组数字与我们「第 3–5 轮零收益」是同向的第二个证据，但机制不同。** ⭐ 我们的第 3–5 轮**跑了但没产出**；⭐ 他们的第 3–5 轮**基本不发生**（平均 1.14 轮，5.5% 触顶）。⭐ 换句话说：⭐ **当裁决者的判据是形式化可判定的，循环在第 1 轮就收敛，第 3–5 轮自然不存在**；⛔ 当裁决者是 LLM 自评时，`LADEX-LLM-NA` 平均要 4.65 次调用而**仍有 18.34% 的图不合规** —— ⛔ 轮数烧掉了却没换来良构性。

#### ⛔⛔ 超限处理：他们的做法违反本仓库 §10 与 §12

⛔ **「5 轮不收敛就丢弃、从生成步冷重启」正是 [CLAUDE.md](../../../../../CLAUDE.md) §10 与 §12 明令禁止的做法** —— ⛔ 上一次失败的原因一点都不带进下一次，等于换个随机数再赌一次。⭐ 他们能这么做且没出事，是因为触顶率只有 5.5%、且二次触顶只有 14 例（0.1%）—— ⚠️ 也就是说**这条路在收敛率极高时代价可忽略**，⛔ 但它不构成对我们照搬的许可（我们的场景恰好是低收敛率）。

⚠️ **且这个策略有一处口径隐忧（S，从 §5.4 与 §6 的报法推出）**：被丢弃重启的 703 格，其最终结果与一次通过的格**混在同一批均值里**，⛔ 而这 703 格恰是最难的样本；⛔ 原文未说明是否单列。⭐ 好在成本侧未被掩盖：重启消耗的调用数计入了 LLM 调用均值（这是 `LADEX-Alg-LLM` 平均 7.24 次调用的一部分来源）。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有两层** |
| 形态 | ⭐ ① **约束目录**：6 条结构约束（SC1–SC6）+ 5 条对齐约束（AC1–AC5）;⭐ ② **CSV 输出编码**（Draw.io 兼容，每行 `目标节点 ID, 类型, 前驱 ID, 迁移标签`） |
| ⭐ **是否闭合** | ⭐⭐ **闭合** —— ⭐ critique 只报「违反了 SC/AC 里哪一条」，⛔ 不自由生成新缺陷类；⭐ prompt 里逐条列出该变体负责检查的约束（M，§3：「For the critique step (Step 2.1), the prompt includes only the constraints that are assessed by an LLM ... Constraints that are checked algorithmically, or not checked at all, are not included in the critique prompt.」） |
| ⭐ **谁定的** | ⭐ **人预编目录 + 从规范归纳**：SC 从 UML 2.5.1 规约穷举 normative statement 得 17 条，⭐ 再筛成 6 条；AC 从 UML 活动图语义（顺序流 / decision / 并发）+ 既有 LLM 建模工作的 prompt 归纳得 3 条，⭐ 另自加 AC4（并发）与 AC5（排除说明性文字）。⛔ **不是 LLM 生成的，也不是让 LLM 从目录里挑** |

⭐⭐ **SC 的筛法值得逐字记（M，§2）**，⭐ 因为它是一份「哪些规范条目该进机械检查」的现成裁定记录：

> This process yielded 17 constraints. Of these, ten constraints concern syntactic variations or visual notations in UML activity diagrams that do not require explicit enforcement in our work since our formalism unifies different UML syntactic elements; for example, we treat forks and merges uniformly as action nodes. One rule – namely, the exclusion of dangling transitions – is intrinsically enforced in our generation process, as our encoding does not admit transitions without both source and target nodes. The remaining six constraints are listed in Table 1.

⭐ 即 **17 → 剔 10（被形式化吸收）→ 剔 1（被编码内在保证）→ 留 6 条真正需要检查**。

⚠️ **与我们的形状对照**：⭐ 我们是「**19 条闭合谓词 + LLM 自动选**」；⭐ 他们是「**11 条闭合约束 + 全量检查（不选）**」。⛔ **两者的闭合集用途不同**：我们的词表决定**要问什么**（选题），他们的目录决定**要查什么**（校验）。⛔ 所以本篇**不构成**「闭合词表 + LLM 自动选」这个组合的先例 —— ⭐ 它连「选」这一步都没有。

### B6 · 模型

| 用途 | 模型 |
| :-- | :-- |
| 生成 / refine / critique | ⭐ **GPT-4.1 Mini**（instruction-following，temperature **0.0**）· **O4 Mini**（reasoning，⛔ temperature 不可调）· **DeepSeek-R1-Distill-Llama-70B**（本地 Ollama，temperature **0.6**） |
| 数据集覆盖 | ⚠️ Industry 只用 GPT-4.1 Mini + O4 Mini（Ciena 保密政策只许 partner-approved 模型）；Paged 用全部三个 |
| L-Match（评测端） | ⛔ **O4 Mini** |
| 多模型对照 | ⭐ **有**，且给了跨模型汇总：O4 Mini 比 GPT-4.1 Mini 少 **17.54%** 的结构违规图、语义正确性高 **19.28%**、完整性高 **17.51%**、少 **0.71** 次调用 |

⚠️ **模型代次要打折**：⭐ GPT-4.1 Mini 与 O4 Mini 都是 2025 年的**小型 / mini** 档，⛔ 不是 SOTA 前沿档。⭐ 但本篇的核心结论是**流水线形态对照**（算法 vs LLM 裁决），⭐ 且三个模型上趋势一致，⛔ 所以模型代次对这条结论的威胁比对绝对分数的威胁小得多。⚠️ 反过来说：⭐ 「LLM 自评检查不出良构性问题」这条在更强模型上是否仍成立，本篇答不了。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 |
| :-- | :-- |
| ⭐⭐ SC1–SC6 算法检查 | ⭐ 仓库 `LADEX/StructuralConstraintChecking.py`。⭐⭐ **v3 的 Table 1 给出了每条的一阶逻辑形式化**（如 SC3 逐字：$\forall n\in N^i:\nexists x\in N:((x,n)\in T \lor \exists l\in TL:(x,l,n)\in T)$），⭐ SC6 的可达性另有附录 A 的形式定义 |
| B-Match | ⭐ BFS 遍历 + 迹语义相似度（`simLabel` 用 Sentence Transformers v4.1.0 + `Alibaba-NLP/gte-base-en-v1.5` 嵌入余弦） |
| E-Match | ⭐ 严格字符串相等匹配（⛔ 附录 D，见 C 节 `adverse_results`） |
| CSV → XMI / PlantUML / Draw.io | ⭐ 三个转换脚本，XMI 经 Eclipse Papyrus 验证 |
| 统计检验 | ⭐ Wilcoxon Rank-Sum + Vargha-Delaney $\hat{A}_{12}$ + Benjamini-Hochberg 校正 |

⭐⭐ **这一格的关键点**：⭐ 他们的「算法检查器」判的是**产物自身的良构性**（只看 $\langle NL, TL, N, T\rangle$ 就能唯一判定），⛔ **不需要任何外部真值**。⭐ 这与本仓库 §11 的准入判据（「给定字段值、不看上下文、不做语义解释就能唯一判断」）**逐条吻合**：SC1/SC2 是计数，SC3/SC4/SC5 是局部度约束，SC6 是图可达性 —— ⭐ 全部是决定性谓词。⛔ **它不是 sound oracle（不做模型检查 / 求解），而是一个决定性语法-图检查器。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **有，但只是内部消融 baseline**：`Baseline` = 去掉 critique-refine 回路的单遍生成。⭐ 作者给了它叫 baseline 的理由（M，§3 逐字：「it follows the prevailing state-of-the-art approaches, which employ LLMs to generate complete behavioural models directly from a given textual description」）。⛔ **没有外部方法的复现对照**（§8 的 Table 12 只做定性能力对照，不给可比数字） |
| `dataset` | ⭐ ① **Paged**：从公开 PAGED 的 3394 对里**随机抽 200 对**（M，理由逐字：「To keep the cost, time, and resources required for our empirical evaluation manageable」），GT 平均 10.5 节点 / 10.9 迁移；⭐ ② **Industry**（Ciena，⛔ 专有）20 份配置文档，GT 平均 29.15 节点 / 31.35 迁移，⭐ 文本长度是 Paged 的 8.1 倍字符 / 10.6 倍 token。⭐ **分母**：每变体每模型 Industry 生成 **100** 图（20 × 5 次重复）、Paged **1000** 图（200 × 5）；全实验共提交 **16000** 条过程描述 |
| `metrics` | ⭐ ① **structural consistency** = 至少违反一条 SC 的图数（⛔ 不是比例，是计数）；⭐ ② **semantic correctness** = 生成图中被匹配的节点占生成图节点数的比例 $\mathit{cor}=|A|/|\mathit{ad}_{llm}.N|$；⭐ ③ **semantic completeness** = GT 中被匹配的节点占 GT 节点数的比例 $\mathit{com}=|B|/|\mathit{ad}_g.N|$；⭐ ④ **cost** = LLM 调用数 + 每次调用的 input / output / reasoning token 均值。⛔ **无 `@k` 类多轮口径** —— ⚠️ 它们靠「5 次重复报均值 ± 标准差」处理采样，⛔ 而不是像我们那样区分 `hit@1` / `hit@3` / `hit@all` |
| ⭐ `judged_by` | ⭐⭐ **双自动裁决 + 对人类共识做过校准**，⭐ 这是本篇方法论上最值得学的一块：<br>· **B-Match** = 确定性算法（迹语义 + 嵌入相似度）<br>· **L-Match** = ⛔ LLM-as-judge（O4 Mini）<br>· ⭐ **L-Match 的校准**：各数据集抽 5 张图，⭐ **两名标注者**独立标节点对应（Ciena 2 名工程师；公开集 2 名有 UML 经验的研究生），⭐ **报 Cohen $\kappa$ = 0.916（Ciena）/ 0.888（Paged）**，⭐ 分歧讨论后成共识，⭐ 再与 L-Match 比 P/R/F1 = **96.59 / 95.60 / 96.03**（Ciena）与 **90.36 / 94.03 / 91.40**（Paged）<br>· ⭐ **RQ1 专门用一整个研究问题验证「两种裁决器结论是否一致」**：Spearman $\rho$ = 0.8–1.0，⭐ 且 10 组两两比较里**从未给出互相矛盾的显著性结论** |
| `human_baseline` | ⛔ **无**。⚠️ GT 由专家造（Industry 由 Ciena 领域专家造并验证；PAGED 由 3 名独立评估者验证），⛔ 但**没有「人做同一任务」的耗时 / 质量对照** |
| `runs` | ⭐ **5 次重复**，⭐ 报均值 **+ 标准差**，⭐ 并做显著性检验与效应量 |
| ⭐ `adverse_results` | ⭐⭐ **三处不利结果都如实写进正文或附录，且给了机制解释而非掩盖**（详见下方专段） |

### ⭐⭐ 不利结果的处理方式（⭐ 直接可借鉴）

**① RQ4：对齐检查在工业数据集上是「有得有失」，⛔ 不是净正收益。**（M，v3 §6.3 RQ4 逐字）

> When evaluated on the Industry dataset using O4 Mini and L-Match, the results indicate a trade-off: LADEX-Alg-LLM significantly improves completeness over LADEX-Alg-NA with a negligible effect size, while LADEX-Alg-NA yields significantly higher correctness with a small effect size. This suggests that while alignment checking forces the LLM (specifically O4 Mini) to capture more process details, it introduces a higher risk of semantic errors within complex, proprietary domains.

⭐ **注意写法**：⭐ 它把 trade-off 直接写进 **RQ4 的答案句**（不是塞进 threats），⭐ 并给出机制猜想（逼模型抓更多细节 → 语义错误风险上升）。⚠️ v2 在这一处只说「无显著差异」，⛔ **v3 把它改成了对自己更不利的表述** —— ⭐ 这是个值得注意的修订方向。

**② RQ3：算法检查在有对齐检查时反而更贵，⛔ 与作者自己的直觉相反。**（M，§6.3 逐字）

> One might expect that performing structural checks algorithmically would reduce the number of LLM calls ... Our results partially confirm this intuition: when alignment checking is absent, algorithmic structural checks indeed reduce the number of calls – LADEX-Alg-NA uses, on average, 2.49 times fewer calls than LADEX-LLM-NA. However, when alignment checking is present, algorithmic structural checks have the opposite effect, requiring, on average, 1.73 times more calls for LADEX-Alg-LLM compared to LADEX-LLM-LLM.

⭐ **机制解释也给了**：⛔ 当良构与对齐都由同一个 LLM 检查时，它能把「同一处缺陷同时违反 AC3 与 SC5」**合成一条 critique**；⭐ 而算法检查器看不到这个共因，⛔ 于是同一处缺陷在 critique 里**出现两次**，critique 变长，⛔ instruction-following 模型看到长 critique 会「overreact」、一轮改太多、导致更多轮。⭐ 这个机制在 reasoning 模型上几乎不出现。

**③ 附录 D：最严格口径下的分数极差，⛔ 但没藏。**（M，附录 D 逐字）

> the strict string equivalence required by this algorithm results in scores of exactly 0% on the Industry dataset, and severely degraded average scores of below 1% on the Paged dataset, across all LLMs and variants.

⭐ 即 **exact matching 口径下 Industry 全 0%、Paged <1%**，⭐ 并把该算法实现一起放进复现包。⭐ **这是「口径变更同时给出双份数字」的正例。**

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文（预印 = 接受版） | 🟢 | [arxiv.org/abs/2509.03463](https://arxiv.org/abs/2509.03463) | ⭐ `verify_assets` 逐字：`HTTP 200 · text/html; charset=utf-8`；⭐ 实际取到 v3 HTML 全文 149,184 字符，头部逐字含 `Journal: Empirical Software Engineering` 与 `arXiv:2509.03463v3 [cs.SE] 06 Jul 2026` |
| 论文全文（Springer 正式版） | 🟠 | [doi.org/10.1007/s10664-026-10923-2](https://doi.org/10.1007/s10664-026-10923-2) | ⛔ **入口在但内容取不到**：DOI 302 → `link.springer.com` → 303 → `idp.springer.com/authorize`（鉴权）；⭐ 直取 PDF 链接返回 `HTTP/2 200` 但 `content-type: text/html`、`content-length: 3038`，⛔ 内容是 `<title>Client Challenge</title>` 的 WAF 页。⭐ Crossref `license` 字段只有 TDM 条款，⛔ **无 OA 标记** |
| ⭐ **实验代码** | 🟢 | [github.com/parham-box/EMSE-LADEX](https://github.com/parham-box/EMSE-LADEX) | ⭐ `verify_assets` 逐字：`HEAD b515ca1bf2 · 文件 58214（非文档 44192）· release 0 · license 无⚠️ 树被截断`。⭐ 我另实取顶层：`LADEX/`（`Baseline.py`、四个变体 `LADEX-{ALG,LLM}-{LLM,NA}.py`、`StructuralConstraintChecking.py`、`CsvTransformation.py`、`Prompts.py`）、`Evaluation_Code/`（11 个脚本，含 `B-Match.py`、`L-Match.py`、`E-Match.py`、`CountRefinementLoop.py`、`SmallPowerAnalysis.py`）、`Dataset/`、`Results/`、`RQ1/`、`RQ2-RQ3-RQ4 Statistical Tests/`、`constraints.pdf`。⭐ 仓库 17.3 MB，创建 2025-11-27、最后 push 2026-05-12。⛔ **无 LICENSE 文件** |
| ⭐ **数据集 / Benchmark** | 🟢 | 同仓库 `Dataset/` | ⭐ 实取到两个子目录：`Industry_Anonymized_Dataset/`、`PAGED_Dataset/`。⭐ §10 逐字：「contains our implementation, the Paged dataset used in our evaluation, and **an anonymized subset of our Industry dataset**」。⚠️ 工业集只放**匿名子集**，⛔ 不是全量 |
| 实验结果细则 | 🟢 | 同仓库 `Results/` | ⭐ 实取到 **10 个目录 = 2 数据集 × 5 变体**（`Industry-Baseline` … `Public-LADEX-LLM-NA`），⭐ 即逐变体逐数据集的产出可下载，⛔ 不只有论文内表格 |
| Artifact / 复现包 DOI | ⚪ | —— | ⛔ **无 Zenodo / figshare / OSF DOI**；⛔ 只有 GitHub 仓库（⚠️ 无归档快照、无 release，可被改写或删除） |
| ⭐ **prompt 是否公开** | 🟢 | `LADEX/Prompts.py` + `Evaluation_Code/L-Match.py` | ⭐ 论文两处逐字承诺（§3 与附录 C：「The complete set of prompts is available in our replication package」；附录 C 另给 Figure 11 的 prompt 提纲）。⭐ 实际核到 `LADEX/Prompts.py` 存在。⚠️ **README 与实际文件名不一致**：README 写「The prompt for `L-Match` is provided in `Evaluation_Code/LLMMatcher.py`」，⛔ 但目录里实际是 `Evaluation_Code/L-Match.py`，⛔ 没有 `LLMMatcher.py` |

⭐ **终裁说明**：⭐ 代码 / 数据 / 结果 / prompt 四项判 🟢，⭐ 因为不只是「仓库存在」—— ⭐ 我实际列出了目录内容，⭐ 五个变体的实现、算法检查器、两个 matcher、逐变体结果目录、统计检验目录全部在位。⚠️ 扣分项只有两条：⛔ 无 license、⛔ 无归档 DOI。

---

## E. 对 M1 的意义

### 1. ⭐⭐ 可取之处

**⭐⭐ 第一条（本卡最重要的输出）：把良构性检查从 LLM 手里拿走，交给算法。这条有强证据。**

⭐ 证据强度（M，§6.2 + §6.3）：

| 变体 | 结构不合规比例 | 平均 LLM 调用数 |
| :-- | :-- | :-- |
| `Baseline`（无回路） | ⛔ **21.80%** | 基准 |
| `LADEX-LLM-NA`（LLM 查良构） | ⛔ **18.34%** | 4.65 |
| `LADEX-LLM-LLM`（LLM 查良构 + 对齐） | ⛔ **19.48%** | 4.17 |
| ⭐ `LADEX-Alg-NA`（算法查良构） | ⭐⭐ **0%** | ⭐ **1.87** |
| ⭐ `LADEX-Alg-LLM`（算法查良构 + LLM 查对齐） | ⭐⭐ **0%** | 7.24 |

⭐⭐ **两个关键读法**：⛔ ① **LLM 自评回路把不合规率从 21.80% 只压到 18–19%，几乎等于没做** —— ⛔ 花了 4 次多调用换来 2–3 个百分点；⭐ ② **算法检查一次到 0%，且在无对齐检查时调用数反而降到 1.87（比 LLM 路少 2.49 倍）**。⭐ 而且良构性改善**顺带**带来语义收益：⭐ 算法路比 LLM 路平均 correctness **+16.95%**、completeness **+15.12%**。

⭐ **搬到我们这里的落点**：⭐ 我们的 `review_requirements` 与 `review_assertions` 两个 LLM 自评节点里，⭐ 凡是判据能写成「只看 `AssertionScript` / `Requirement` 字段值就唯一判定」的检查，⭐ 一律迁到 `precheck_and_seal`（我们已有的确定性节点）。⭐ 本篇给了这个动作的外部量化背书。

**⭐ 第二条：约束筛选留了一份可复用的裁定记录。** ⭐ 17 → 6 那个过程（剔掉被形式化吸收的 10 条、剔掉被编码内在保证的 1 条）⭐ 正好是我们 §11 需要的那种「哪条该进门、哪条不该」的工作记录范式。⭐ 我们的 19 条谓词也该有一份同构的表：**每条写明「它是被形式化吸收了、被编码保证了、还是真的需要一道检查」**。

**⭐ 第三条：LLM-as-judge 上线前先对人类共识做校准，并报 $\kappa$。** ⭐ 他们的做法是：2 名标注者 → 报 Cohen $\kappa$ → 分歧讨论成共识 → 再与 LLM judge 比 P/R/F1 → **另外再造一个确定性 matcher（B-Match）做交叉验证，并用一整个 RQ 检验两者结论是否冲突**。⭐ 我们的台账判定目前是人工逐位，⭐ 若日后要引入任何自动判定，这套四步校准是现成模板。

### 2. ⛔ 不可取 / 陷阱

**⛔ 第一条：「不收敛就整格丢弃冷重启」不能照搬。** ⛔ 逐字：「we discard the activity diagram and restart the variant from its generation step」。⛔ 这违反本仓库 §10（除 provider 错误与 schema 死活对不上外一律降级）与 §12（结构性死路上重试期望收益为零）。⭐ 他们侥幸的原因是触顶率只有 5.5%；⛔ 我们的 v46 有 22/35 格降级 —— ⛔ 同样的策略在我们这里就是烧钱。⭐ **正确的读法是：他们证明了「当裁决判据形式化后，几乎不会触顶」，⛔ 而不是「触顶时可以冷重启」。**

**⛔ 第二条：LLM 自评的语义对齐检查不是无条件正收益。** ⛔ Industry 上它 completeness 涨（negligible effect）但 correctness 降（small effect）；⛔ Paged 上 6 组比较里只 3 组 correctness 显著改善且效应量 negligible。⭐ 而它的代价是**平均多 5.38 次 LLM 调用**。⭐⭐ **这条与我们「两个 self-review 零收益却吃 79% token」是同一个方向的独立证据** —— ⛔ 但要说清差别：他们的对齐 reviewer 至少不是零收益（Paged 上有统计显著的正效应），⛔ 只是效应量小且成本高；⛔ 我们的是净零。

**⛔ 第三条：`Baseline` 是自建的消融 baseline，不是外部方法复现。** ⛔ 若引本篇当「critique-refine 优于 SOTA」的证据，那是过度解读 —— ⭐ 它证明的是「同一套 prompt 加不加回路的差别」。

**⚠️ 第四条：模型档位偏低。** ⛔ 三个模型全是 mini / distill 档，⛔ 「LLM 查不出良构问题」这条在前沿模型上是否仍成立，本篇答不了。⭐ 但反向也成立：⛔ 若连良构性这种纯语法问题都要靠模型能力去赌，本身就是设计问题 —— ⭐ 这正是他们（与我们）的结论。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

**⚠️ 最要紧的一条：他们的算法检查器判的是「产物自身良构」，我们要判的是「产物 vs NL 是否对齐」。** ⭐ 他们自己把这条界划得极清楚（M，§1 逐字）：

> **(1) Structural correctness** can, due to its formal nature, be captured as machine-verifiable rules and can be enforced by algorithmic checks derived from the Unified Modeling Language (UML) specification.
>
> **(2) Semantic alignment** requires understanding the context, concepts, and relationships described in text and verifying that these are faithfully reflected in the generated models. Bridging heterogeneous modalities (text and model representations) involves interpretive nuances that **resist purely algorithmic checks**.

⛔⛔ **而我们 paper1 的整个任务（「模型是否忠实于 NL 需求」）落在第 (2) 侧。** ⛔ 所以「把检查交给算法」这条在我们这里**只能覆盖良构层**（断言脚本的 schema / 引用完整性 / 谓词取值合法性），⛔ **覆盖不了对齐层**。⭐ **这恰好给出 M1 的分层落点**：⭐ 良构层全归确定性；⭐ 对齐层保留 LLM，但**必须像他们那样把成本单独记账并接受它可能只有小效应**。

**⚠️ 第二条差别：任务方向相反。** ⭐ 他们是**生成 + 自我校验**，评测靠与专家 GT 的节点匹配；⭐ 我们是**缺陷检测**，评测靠台账命中。⛔ 他们的 `hit` 概念根本不存在，⛔ 所以他们的指标口径（correctness / completeness / structural consistency）**不能直接映射**到我们的 `hit@k`。

**⚠️ 第三条差别：他们的「结构化输出」不是受限解码。** ⛔ 只是 prompt 里写格式 + 给一个 one-shot 例子，⛔ 所以他们才需要 CSV 这种宽松编码来防语法幻觉。⭐ 我们已有 Pydantic schema + 解析失败原地重试回灌，⭐ 在这一维上**比他们强**。⚠️ ⛔ 但注意本仓库 §11 的教训：⭐ schema 强不等于门设得对。

---

## F. 存疑与未核项

1. ⚠️ **Springer 正式排版版逐字内容未核** —— 已试过 `https://doi.org/10.1007/s10664-026-10923-2`（302 → link.springer.com → 303 → idp.springer.com 鉴权）与 `https://link.springer.com/content/pdf/10.1007/s10664-026-10923-2.pdf`（返回 `Client Challenge` WAF 页，3038 字节），结果**均为访问受限**。⭐ 本卡全部基于 arXiv v3（自称 EMSE 版），⛔ 无法排除排版版与 v3 有细节差异。⭐ **卷期号 32(1):12 与发表日 2026-07-25 来自 Crossref API，已核。**
2. ⚠️ **逐轮（第 1 / 2 / 3 / 4 / 5 轮）的增量收益表原文未提供** —— ⭐ 只有「平均 1.14 轮」「5.5% 触顶」两个汇总数。⭐ 仓库里有 `Evaluation_Code/CountRefinementLoop.py`，⭐ 理论上可从 `Results/` 复算出分布，⛔ 但本轮未跑。
3. ⚠️ **703 个触顶重启样本是否单列，原文未说明** —— ⭐ 从 §5.4 与 §6 的报法推测是**混入同一均值**，⛔ 但没有明写。⛔ 这会让最难样本的效果被稀释。
4. ⚠️ **`LADEX-Alg-LLM` 平均 7.24 次调用里，有多少来自重启而非正常迭代，原文未拆分。**
5. ⚠️ **仓库无 LICENSE、无归档 DOI** —— ⛔ 引用它作为可复现证据时要注明这一点（仓库可被改写 / 删除；⭐ 本卡已钉 HEAD `b515ca1bf2`）。
6. ⚠️ **README 的 `LLMMatcher.py` 与实际的 `L-Match.py` 文件名不符** —— ⭐ 已实际核过目录列表；⛔ 不影响 prompt 公开性判定，⛔ 但复现时会踩一下。
7. ⚠️ **Industry 数据集只公开匿名子集，20 份文档的全量不可得** —— ⭐ 属正常工业保密，⛔ 但意味着 Industry 侧结论无法完整外部复现。
