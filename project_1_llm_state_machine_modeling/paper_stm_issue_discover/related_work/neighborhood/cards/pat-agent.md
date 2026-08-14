# 卡片 · **PAT-Agent**（NL → CSP# → PAT 模型检查 → 反例引导修复）

⭐ **全文可得**：本地 [`baselines/pat-agent-autoformalization-model-checking/`](../../../../baselines/pat-agent-autoformalization-model-checking/) 有 `paper.pdf` + `paper_content.txt`（12 页全文，含 References）。⭐ **另外自取了官方 artifact 里的补充结果 PDF**（`Appendix/RQ1/RQ1.pdf`、`Appendix/RQ2/RQ2.pdf`），⭐ 那两份正是本卡 B4 逐轮数字的来源 —— ⛔ 正文 Table VI 只给 Round 0/1/2/5，⭐ 逐轮全表在 artifact 里。

---

## A. 元信息

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `id` | `pat-agent` | — |
| `title` | PAT-Agent: Autoformalization for Model Checking | M |
| `year` | ⭐ **2025**（正式发表年；arXiv 2025-09-28，ASE 2025 proceedings 2025-11-16） | M |
| `venue` | ⭐ **ASE 2025**（2025 40th IEEE/ACM International Conference on Automated Software Engineering），pp. 2122–2133 | M |
| `ccf` | ⭐ **A**（[ccf_venues/conf-a-ase/](../../../../../ccf_venues/conf-a-ase/)） | M |
| `doi` | ⭐⭐ **`10.1109/ASE63991.2025.00176`** —— ⛔ **这条本卡自己从 Crossref 取回并核过**（title / container / pages / 7 位作者姓氏全部对上）。⚠️ 本地 [`bibtex.bib`](../../../../baselines/pat-agent-autoformalization-model-checking/bibtex.bib) 只有 arXiv DOI `10.48550/arXiv.2509.23675`（也真，已核），⛔ **缺正式出版 DOI** | M |
| `arxiv` | [2509.23675](https://arxiv.org/abs/2509.23675) —— ⭐ 已核：arXiv API 返回 title 完全一致，`published 2025-09-28T06:32:14Z`，⛔ 无 `arxiv:doi` 字段 | M |
| `artifact_type` | ⭐ **CSP# 进程模型 / LTS**（PAT 的建模语言） | M |
| `task` | ⭐ **生成**（NL → 形式模型）+ **修复**（反例引导）。⛔ **不是缺陷检测** —— ⭐ 它是「造一个能过检查的模型」，⛔ 不是「在既有模型里找缺陷」 | M |
| `boundary` | ⛔ **界外** —— ⭐ CSP# 是进程代数，⭐ 文法里显式含并行合成与交错：逐字 `P ∥_A Q` / `P ||| Q`（§II.B「Compositional operators」） | M |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **6 段 · 其中 LLM 3 段**）

```
[人] 提供 NL 系统描述 + NL 性质 + 每条性质的期望结果 (VALID/INVALID)
   → [LLM·Planning] 抽 constants / variables / actions / guards，填进 semantic prompt 槽位
   → [LLM·Planning] 生成逐行 NL 建模计划 P
   → [确定性] RAG 检索最相似 <plan, code> 范例（余弦相似度）+ 注入 syntax cue
   → [LLM·CodeGen] 计划 → CSP# 代码
   → [sound oracle·PAT] 逐条 assertion 跑 deadlock / reachability / LTL，得 verdict 向量 + 最小反例 trace
   → 不全 MATCH ⇒ [确定性] 反例定位启发式生成 repair directives R_k
                 → 回到 [LLM·CodeGen]（⛔ **不重跑 planning**）
```

⭐ 论文自陈四大部件（§III 逐字）：`Planning LLM` · `Code Generation LLM` · `Model Checker (PAT)` · `Repair Loop`。⭐ 形式化写成四个 transformer：`T_plan: L_NL → Π → P`、`T_gen: P → M`、`V: M × Q → {MATCH,MISMATCH}^m × C`、`T_repair: M × C × R → M`。〔M〕

### B2 · 每次 LLM 调用的角色

| 调用 | 角色 |
| :-- | :-- |
| Planning LLM（第一段） | ⭐ **抽取器**（typed variables / constants / guarded actions） |
| Planning LLM（第二段） | ⭐ **规划者**（生成逐行建模计划） |
| Code Generation LLM | ⭐ **翻译器**（plan → CSP#） |
| Code Generation LLM（修复时复用） | ⭐ **修复者** |

⛔⛔ **注意：本流水线里没有任何一次 LLM 调用担任「评审者」或「裁决者」。** ⭐ 裁决全部由 PAT 承担。⭐ 这恰是它与我们 v46 的形态差。〔S，从 §III 四部件列表推出〕

### B3 · prompt 策略

`结构化输出约束`（Planning 输出 JSON-serializable；逐字 `The output is JSON-serializable`）· `RAG`（逐字 `we provide semantic guidance via a retrieval-augmented generation (RAG) mechanism` · `retrieve the most similar example based on plan content`）· `one-shot`（逐字 `If no closely similar plan exists, the retrieved example will serve as a one-shot illustration`）· `syntax cue`（逐字 `a compact documentation excerpt, summarizing PAT syntax and common errors observed during early experimentation (e.g., missing semicolons, incorrect process synchronization, malformed assertions)`）· `角色扮演`（逐字 `A concise role specification`）· ⭐ **自建 semantic prompt 模板库**（参数化槽位）。⛔ **无 self-consistency 投票 · 无多智能体辩论 · 无 CoT 明述。**〔M〕

### B4 · ⭐⭐ 循环与裁决者（⛔ 本卡最重要的一格）

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无循环 | ⭐ **有**，且**只有一个** | M |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **`sound oracle` —— PAT 模型检查器**，⛔ 纯粹、无 LLM 参与判定。⭐ 判据是 verdict 向量与用户给的期望结果逐条比对：逐字 `PAT returns a raw verification outcome for each φi, which is compared against the user-provided expected outcome oi to produce a verdict si ∈ {MATCH, MISMATCH}` | M |
| 终止条件 | ⭐ **收敛**（verdict 向量全 MATCH）**或最大轮数**：逐字 `The loop halts at the first iteration k⋆ where the verdict vector ⃗s_k⋆ indicates that all verification results match the expected outcomes` | M |
| 最大轮数 | ⭐ **`K_max = 5`**。逐字 `We empirically cap k at Kmax = 5; if no satisfactory model is found within this limit, the user is given the latest model and counterexample trace. This choice balances repair effectiveness with computational cost, as increasing Kmax further yields diminishing returns in our experiments.` | M |
| ⭐⭐ 有无逐轮边际收益 | ⭐⭐ **有，而且是本轨目前拿到的最完整的一份** —— 见下面两张表 | M |

#### B4a · ⭐⭐ 逐轮数字（主配置 `<o3, Claude>`，Overall，40 系统）

⭐ 来源：**artifact `Appendix/RQ1/RQ1.pdf` TABLE IV**（⭐ 正文 Table VI 只给 Round 0/1/2/5，⛔ 缺 3、4）。⭐ Δ 列是本卡自己算的减法。

| 阶段 | CSR | FPR | APR | ΔFPR | ΔAPR |
| :-- | :-: | :-: | :-: | :-: | :-: |
| Direct Generation（Round 0） | 1.0000 | 0.7500 | 0.8045 | — | — |
| Refine Round 1 | | 0.7750 | 0.8722 | **+2.50pp** | +6.77pp |
| Refine Round 2 | | 0.8750 | 0.9549 | **+10.00pp** | +8.27pp |
| ⭐ Refine Round 3 | | 0.9500 | 0.9774 | ⭐ **+7.50pp** | +2.25pp |
| ⭐ Refine Round 4 | | 1.0000 | 1.0000 | ⭐ **+5.00pp** | +2.26pp |
| Refine Round 5 | | 1.0000 | 1.0000 | ⛔ **0** | ⛔ **0** |

⭐⭐ **直接对照我们那条实测**：⭐ **第 3、4 轮合计贡献 +12.50pp，占全部 25.00pp 增益的整整一半。** ⭐ 换句话说，⭐ **有 sound oracle 的循环在第 3–4 轮仍然在付钱**，⛔ 与我们「第 3–5 轮零收益」形成明确反差。⭐ 但**第 5 轮确实归零** —— ⭐ 论文的 `K_max = 5` 与「再加会 diminishing returns」是**被这张表支持的**。

#### B4b · ⛔⛔ 但**这条结论有强条件**：循环收不收敛取决于 round-0 的质量

⭐ 同一份 artifact 的 `Appendix/RQ2/RQ2.pdf` TABLE V 给了消融的逐轮 FPR（Overall）：

| 配置 | R0 | R1 | R2 | R3 | R4 | R5 | 5 轮总增益 | ⛔ 零收益轮 |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-- |
| ⭐ Full（`<o3,Claude>`） | .7500 | .7750 | .8750 | .9500 | **1.0000** | 1.0000 | **+25.00pp** | {5} |
| ⛔ **w/o Planning** | .4750 | .5500 | .5750 | .5750 | .5750 | .6000 | ⛔ **+12.50pp** | ⛔ **{3, 4}** |

⭐ 再看 `RQ1.pdf` 六个模型配对（Overall FPR）：

| 配置 | R0 → R5 | 总增益 | ⛔ 零收益轮 |
| :-- | :-- | :-: | :-- |
| `<o3, Claude>` | .7500 → 1.0000 | +25.00pp | {5} |
| `<R1, Claude>` | .6250 → .8500 | +22.50pp | {4} |
| `<o3, o3>` | .6750 → .8000 | +12.50pp | {4, 5} |
| `<o3, R1>` | .6750 → .8000 | +12.50pp | {3} |
| `<R1, o3>` | .4750 → .6750 | +20.00pp | {5} |
| `<R1, R1>` | .4250 → .6750 | +25.00pp | {4} |

⛔⛔ **最刺眼的是 UCS 子集（n=6）**（`RQ1.pdf` TABLE II，FPR）：

| 配置 | R0 → R5 | ⛔ 零收益轮 |
| :-- | :-- | :-- |
| `<o3, Claude>` | .8333 → 1.0000 | {1, 3, 4, 5} |
| `<R1, Claude>` | .6667 → 1.0000 | {3, 4, 5} |
| ⛔ `<o3, R1>` | .8333 → **.8333** | ⛔⛔ **{1,2,3,4,5} —— 5 轮全零** |
| ⛔ `<o3, o3>` | .6667 → **.6667** | ⛔⛔ **{1,2,3,4,5} —— 5 轮全零** |
| ⛔ `<R1, R1>` | .5000 → .6667 | {2,3,4,5} |
| ⛔ `<R1, o3>` | .3333 → .5000 | {2,3,4,5} |

⭐⭐⭐ **这一格的结论（⛔ 论文自己没这么说）**：⭐ **sound oracle 循环不是「一定收敛」，它是「在 round-0 足够好时收敛」。** ⛔ 去掉 planning（round-0 从 .7500 掉到 .4750）之后，同一个 PAT oracle、同一个 5 轮预算，⛔ **循环只买回一半增益并在第 3–4 轮就平掉**，⛔ 最终停在 .6000 而不是 1.0000。⭐ 也就是说 —— ⛔ **换成 sound oracle 并不能救一个差的生成端**；⭐ 它放大好的 round-0，⛔ 不修补坏的 round-0。〔S，逐轮表格逐行减法可复算〕

### B5 · ⭐ 中间表示

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无 | ⭐ **有，两层** | M |
| 形态（第一层） | ⭐ **semantic prompts Π** —— 参数化模板 + 固定的建模元素类型表。逐字 `Π is the space of planning representations—structured semantic prompt templates that are partially instantiated, with placeholders for constants, variables, and actions` | M |
| 形态（第二层） | ⭐ **建模计划 P** —— 逐行自然语言标注，与形式构造一一对应。逐字 `The modeling plan takes the form of a line-by-line natural language annotation that maps directly to formal constructs` | M |
| ⭐ **是否闭合** | ⭐⭐ **元素类型闭合、内容开放**。⭐ 闭合的部分：建模元素只有三类（Constant / Variable / Process），每类的字段也定死（逐字：`Constant: name, value, and description` · `Variable: name, type, possible values, initial value, and description` · `Process: name, actions, guard conditions, and associated state changes`）；⭐ **断言类型是硬闭合的 3 类**（逐字 `We rely on three built-in classes: Deadlock-freedom / Reachability / Linear temporal logic (LTL)`）。⛔ 开放的部分：具体填什么名字、什么守卫、什么 LTL 公式全自由生成 | M |
| ⭐ **谁定的** | ⭐ **预编模板 + LLM 自动填** —— ⭐ 元素类型表与断言类型表由作者预编，⭐ 每个槽位填什么由 LLM 决定；⛔ **人不参与选类**（全自动模式下）。⭐ 交互模式下人可以**改**抽取结果，⛔ 但不是「从目录里挑」 | S |

⭐⭐ **对我们的直接可比性**：⭐ 我们是「**闭合 19 条谓词 + LLM 自动选**」；⭐ 它是「**闭合 3 类断言 + 闭合 3 类元素 + LLM 自动填**」。⭐ 所以「闭合词表 + LLM 自动选」**有先例**，⛔ 但**它的闭合集比我们小一个数量级**（3 vs 19）。

### B6 · 模型

| 角色 | 模型 | 级别 |
| :-- | :-- | :-: |
| Planning LLM（默认） | ⭐ `o3-mini-2025-01-31`（OpenAI，2025-01） | M |
| Code Generation LLM（默认） | ⭐ `claude-3-7-sonnet-20250219`（Anthropic，2025-02） | M |
| 备选 | ⭐ `DeepSeek-R1` | M |

⭐ **有多模型对照**：⭐ 6 种配对（`<o3,Claude>` / `<R1,Claude>` / `<R1,R1>` / `<R1,o3>` / `<o3,R1>` / `<o3,o3>`）全跑。⚠️ **但三个模型都是 2025 年初的一代** —— ⭐ 按 X1 的结论，⛔ 这一代与当前 SOTA 不是一个量级，⛔ **它的绝对数字（尤其 round-0 的 .7500）参考价值要打折**；⭐ 逐轮**形状**的参考价值不受影响。〔I：打折这一句是我方判断，⛔ 论文未讨论模型代际〕

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 级别 |
| :-- | :-- | :-: |
| ⭐⭐ **PAT 模型检查器** | ⭐ state-space exploration + LTL 验证 + deadlock 检测 + reachability。逐字 `an existing extensible model checker that supports state-space exploration and LTL verification` | M |
| ⭐ **反例定位启发式** | ⭐⭐ **确定性的、不是 LLM 做的**。⭐ 两条排序启发式：逐字 `actions appearing later in the violation trace (i.e., closer to the failure point) and actions occurring more frequently` | M |
| ⭐ **修法启发式（按性质类型）** | 逐字 `repair heuristics tailored to the property type of the unsatisfied requirement (e.g., tightening guard conditions for safety or loosening them for liveness)` | M |
| RAG 检索 | 余弦相似度选 `<plan, code>` 范例 | M |
| 编译 / 语法检查 | CSR 指标即编译成功率，⭐ 说明有编译门 | S |
| ⭐ 界面里的 LTL 构造 | 逐字 `Linear temporal logic formulae can also be created without requiring users to manually write formal syntax, as the system translation internally ensures syntactic correctness` | M |

---

## C. 实验

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⭐ **有，但全是自建**：① 三个 LLM 直接生成（o3 / Claude / R1，⭐ **给同样的 RAG 范例与 syntax 文档以求公平** —— 逐字 `These direct generations are provided with the same RAG-extracted exemplars and syntax documentation as our pipeline to ensure a fair comparison`）；② 5 个替代模型配对；③ 消融 4 档。⛔ **无任何外部方法 baseline**，⭐ 且论文明确解释为什么没有：逐字 `To the best of our knowledge, no existing work attempts an automatic NL→CSP# pipeline` · `Establishing such a baseline would therefore require replicating (and fairly re-engineering) the very contribution that PAT-Agent itself introduces` | M |
| `dataset` | ⭐ **40 系统 / 133 断言**，三来源：`PAT`（26，PAT library）· `A4F`（8，改编自 Alloy4Fun）· `UCS`（6，取自 Roscoe 教材 *Understanding Concurrent Systems*）。⭐ **分母口径**：CSR/FPR 的分母是系统数 40；APR 的分母是断言总数（逐字 `APR = Σpi / ΣAi`）。⚠️ **有筛选**：逐字 `We curated the examples that can be formalized in the syntax defined in section II` —— ⛔ **即先按自己支持的语法子集筛过一遍**，⛔ 筛掉多少未报 | M |
| `metrics` | ⭐ `CSR`（编译成功率）· `FPR`（全过率）· `APR`（断言级平均通过率）。⛔ **无 `@k` 类多轮口径** —— ⭐ 它的「轮」是修复轮而非重采样轮，⛔ 两者不可互换 | M |
| ⭐ `judged_by` | ⭐⭐ **自动脚本 + sound oracle**：判定 = PAT 的验证结果与**用户预先给定的期望结果**逐条比对。⛔ **无人工判定、无 LLM-as-judge、无标注者间一致性**（⭐ 主实验不需要，因为期望结果就是 ground truth）。⚠️ **但 user study 的 `Assertion Accuracy`（「语义上是否对齐意图」）必须有人判**，⛔ **论文未说谁判、也未报一致性** | M / ⚠️ 后半段为 S |
| `human_baseline` | ⭐ **有** —— ⭐ 20 人 user study，10 人对照组（可用任何资源含 LLM，⛔ 但不能用 PAT-Agent）vs 10 人实验组。⭐ Mann–Whitney U 检验，⭐ EG 12.85 min / 0.9958 / 0.9688 vs CG 17.11 min / 0.7500 / 0.6633，p 分别 1.16E-02 / 1.85E-07 / 2.66E-05 | M |
| `runs` | ⛔⛔ **单次，无方差**。⭐ 论文自陈：逐字 `like all LLM-based methods, PAT-Agent inherits stochasticity in generation. We mitigate this by fixing LLM versions with timestamps and incorporating multiple repair iterations guided by PAT feedback, but stochasticity remains an inherent limitation` —— ⛔ 即**用「多轮修复」代替「多次重采样」**，⛔ 而这两件事回答的不是同一个问题 | M（自陈）/ S（我方点评） |
| ⭐ `adverse_results` | ⭐ 见下面 C.1、C.2、C.3 三条 | — |

### C.1 ⭐ 它怎么处理「100% 看着太漂亮」这件事

⭐ 论文**主动做了免责**，逐字：`In contrast, our pipeline achieves a 100% full-pass rate across all 40 systems. This result does not indicate flawless first-attempt generations, rather, it highlights the effectiveness of the integrated repair loop` · `showing that multiple repair iterations were often necessary`。⭐ **这个写法可直接借鉴** —— ⭐ 把一个满分数字**主动降解释**为「不是一次做对，是循环补上的」。〔M〕

⛔⛔ **但有一个论文没说的结构性问题：`FPR` 就是这个循环自己的停机条件。** ⭐ 循环在「verdict 向量全 MATCH」时停，⭐ 而 `FPR` 量的正是「多少系统达到了 verdict 向量全 MATCH」。⛔ 所以 `Round 5 FPR = 1.0000` 的准确读法是「**40/40 个系统的循环都收敛了**」，⛔ **不是「40/40 个模型都是 NL 的忠实形式化」**。〔S，从 §III.D 的停机条件定义与 §IV.B 的 FPR 定义并列即得〕

### C.2 ⭐⭐ 同实验室的后续论文给出了一个「过了检查但模型是退化的」实例

⭐ [Event-B Agent](./event-b-agent.md)（FSE 2026，⭐ 与 PAT-Agent 共 2 位作者 + 同一通讯作者）把 PAT-Agent 当 baseline，⭐ 并逐字记下一个案例：`PAT-Agent, a framework specialized for formal model synthesis, produces a stronger model M_PAT-Agent in which the guards of stop enforce valAtJ = minRanF, thereby satisfying FUN–1. Nonetheless, this model contains subtle flaws. ... As a result, the guard of stop implies that the constant minRanF must always be 3. From the perspective of model checking, this system is deemed correct, but the correctness does not generalize beyond the single case minRanF = 3.`

⭐⭐ **这是一条被独立第三方（虽同实验室）书面记录的「向 oracle 过拟合」实例**，⛔ 而不是我方推断。⭐ **对 M1 是最重要的一条警示**：⛔ **把裁决权交给 sound oracle，换来的是「一定过检查」，⛔ 不是「一定正确」。** 〔M，逐字引自 Event-B Agent §2.1〕

### C.3 ⛔⛔ 正文内部有一处**自相矛盾**，必须记下

⭐ §VI Discussion 逐字：`Recent verification studies often contrast their approach with program-repair frameworks that iteratively patch counter-examples. In our context, however, the combination of prompt engineering and large language models already achieves high requirement-satisfaction rates. Empirically, incorporating a separate repair pipeline yielded negligible improvements while adding substantial overhead. We therefore focus our analysis on synthesis quality rather than post-hoc repair, and leave generalized repair strategies as future work.`

⛔ **这段与全文主张正相反。** ⭐ §IV.D 的 Table V 明写去掉 Repair Loop 后 Overall FPR 从 1.0000 掉到 0.7500、APR 从 1.0000 掉到 0.8045；⭐ §I 的贡献列表把 repair loop 列为核心贡献之一。⭐ 我方读法：⛔ 这段**大概率是从别处（rebuttal 或前作）粘过来的残留**，⛔ 说的是「另接一条独立 program-repair 管线没用」而不是「自己的 repair loop 没用」。〔⚠️ **I 级 —— 这是推测，论文没有任何说明**〕

⭐⭐ **为什么必须记**：⭐ 若日后引用 PAT-Agent 来支持「修复循环有效」，⛔ 审稿人可以从这一段反打；⭐ 反之若想引用「迭代修复收益有限」，⛔ 引这一段是**引到了一段与该文数据矛盾的话**。⛔ **两个方向都不要单引这段。**

### C.4 ⭐ 另一条自陈局限：修复启发式是照着自己数据集里见到的违规调出来的

⭐ §VII 逐字：`Our rule-based repair heuristics are tailored to the violations observed in our datasets, primarily safety and liveness errors. While effective in these settings, they may not generalize to other types of failures, where alternative forms of guidance could be required.`

⭐ 这条按本仓库 §3.5 的口径就是**自陈的「按观察到的失败反向调规则」**。⭐ 值得注意的是**论文把它写在 External Validity 里而不是藏起来** —— ⭐ 这个处理方式可直接借鉴（⭐ 我们的 `nl_cue` 修订、门的引入动机同类）。〔M〕

---

## D. ⭐ 资产（⛔ 逐条实际取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | 🟢 | [arXiv:2509.23675](https://arxiv.org/abs/2509.23675) · 本地 `paper.pdf` | ⭐ arXiv API title 完全一致 · 本地 12 页全文已通读 |
| ⭐ **实验代码** | 🟢 | [github.com/ZuoXinyue/PAT-Agent](https://github.com/ZuoXinyue/PAT-Agent) | ⭐ 逐字工具输出：`HEAD 8b5636dee7 · 文件 929（非文档 589）· release 0 · license NOASSERTION`。⭐ 顶层实取：`Appendix/ Automated_Pipelines/ Datasets/ Experiments_Demo/ Interface/ LICENSE PAT.Console/ README.md`。⭐ `Automated_Pipelines/` 下有 `Full_Pipeline/` 与 `No_Planning/`（⭐ **消融配置也放了**）+ `requirements.txt`（3936 B） |
| ⭐ **license** | 🟢 | 同上 `LICENSE`（611 B） | ⭐ 逐字取回：`PAT-Agent Research License (Non-Commercial)` · `experimental research prototype for academic and educational purposes only` · ⛔ `Commercial use, commercialization, sublicensing, or integration into` …（⚠️ 非标准 license，⭐ 这解释了工具为何报 NOASSERTION） |
| ⭐ **数据集** | 🟢 | `Datasets/` | ⭐ 实取：`PAT.json` 88490 B · `A4F.json` 37408 B · `UCS.json` 19838 B + `README.md`。⭐⭐ **有 ground truth**：`README.md` 的结构里每条 assertion 带 `assertionType`（枚举）与 `assertionTruth`（⭐ **期望验证结果**），⭐ 即分母与判据都在数据里 |
| ⭐⭐ **实验结果细则** | 🟢 | `Appendix/RQ1/RQ1.pdf` · `Appendix/RQ2/RQ2.pdf` | ⭐⭐ **本卡实际下载并用 `tools.pdf_extractor` 提取过**（RQ1 2 页 / RQ2 1 页），⭐ **逐轮 FPR/APR 全表已抄进 B4**。⭐ `Appendix/RQ1/README.md` 逐字：`include the evaluation for direct generation and each repair round for the PAT, UCS, and A4F datasets` |
| ⭐ **单次运行完整 trace** | 🟢 | `Experiments_Demo/` | ⭐ `README.md` 逐字列出：`const-history.json` · `action-history.json` · `nl-instruction-claude.json` · `claude-code.json` · ⭐ **`mismatch_traces.json: verification counterexamples used to guide model repair`** · `refine_round_1/ refine_round_2/` · `verifiedCode.csp`。⭐ 覆盖 Car 与 Tesla 两个最复杂系统 |
| ⭐ **prompt 是否公开** | 🟠 | `Appendix/Prompt_Example/` · `Interface/syntax-dataset.json` · `Interface/database-rag-claude.json` | ⛔⛔ **判 🟠 而不是 🟢**：⭐ `Appendix/Prompt_Example/` 里只有**两张 PNG 截图**（`actions.png` 352 KB · `const-and-vars.png` 332 KB）+ 一句 README，⛔ **不是可复制的 prompt 文本**。⭐ 论文正文说 `The complete set of instructions is provided online [1]`（[1] = 仓库根），⭐ 完整 prompt 应在 `Automated_Pipelines/` 源码里，⛔ **本轮未逐文件核到 prompt 常量**。⭐ syntax 文档与 RAG 库确实是 JSON（论文给了直链） |
| Artifact / 复现包 DOI | ⚪ | — | ⛔ 无 Zenodo / 4open / OSF DOI；⭐ 只有 GitHub |
| ⭐ 界面 demo 视频 | 🟠 | `Appendix/Interface_Screenshots/` | ⭐ 论文逐字 `A full demonstration of the interface, along with an illustrative video, is available in our GitHub repository`；⛔ 本轮只核到 `Interface_Screenshots/` 目录存在，⛔ **未核到视频文件本身** |

⭐ **总评**：⭐⭐ **这是本簇资产最好的一家** —— ⭐ 代码、数据、逐轮结果、单次完整 trace（含反例 JSON）、消融配置全都真实可取。⭐ 唯一的缺口是 prompt 以截图而非文本形式呈现。

---

## E. ⭐ 对 M1 的意义

### 1. ⭐⭐ 可取之处

1. ⭐⭐⭐ **「期望结果」这个设计是本簇最该搬的一件东西。** ⭐ 用户对每条性质不只给公式，⭐ 还给**期望的验证结果 `VALID` / `INVALID`**（逐字 `users specify two inputs: properties in natural language and the expected verification outcomes (VALID or INVALID). ... A requirement is satisfied if the two match`）。⭐⭐ **这是一个便宜的反真空装置**：⛔ 一个「什么都禁」的退化模型会让所有 `VALID` 期望落空，⛔ 一个「什么都允许」的退化模型会让所有 `INVALID` 期望落空 —— ⭐ **两侧都被钉住，退化解就不再是廉价的**。⭐ 我们的谓词求值目前只问「是否成立」，⛔ **没有「本该不成立」这一侧**；⭐ 加上它几乎不花钱。
2. ⭐⭐ **反例定位是确定性的，不是让 LLM 自己找。** ⭐ 两条启发式（trace 里越靠后越可疑 · 出现越频繁越可疑）+ 按性质类型给修法方向（safety 收紧守卫 / liveness 放松守卫），⛔ **全在 LLM 之外算完，再作为 directive 注入**。⭐ 我们的契约门报错文案目前更像「说哪条规则不满足」，⛔ 不像「指出哪一处最可能是病灶」。⭐ **把「定位」从 LLM 手里拿走、做成确定性的一层，是可以直接照搬的形状。**
3. ⭐ **修复只回到 CodeGen，不重跑 Planning。** 逐字 `Directives are fed back to T_gen in-context, guiding code-level edits without rerunning the full planning pipeline and ensuring locality of change`。⭐ 对我们即「**修订只回到 `convert_assertions`，不回退到 `split_requirements`**」，⭐ 保证改动局部性、也省 token。
4. ⭐ **满分数字的主动降解释写法**（见 C.1 逐字）—— ⭐ 我们要写 −15.82pp，⭐ 同一个技巧反着用同样成立。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔ **不要把「换成 sound oracle」当成万灵药。** ⭐ B4b 的数字很硬：⛔ 去掉 planning 之后，**同一个 PAT oracle、同一个 5 轮预算，增益从 +25.00pp 掉到 +12.50pp 并在第 3–4 轮就平掉**；⛔ UCS 子集上更有两个配置**5 轮全零**。⭐ **oracle 决定「循环会不会跑偏」，⛔ round-0 决定「循环能爬多高」。**
2. ⛔⛔ **它的 `FPR` 是循环自己的停机条件**（C.1）。⭐ 我们若照此设计指标，⛔ 会造出一个**必然趋于 100% 的指标**，⛔ 那不是能力度量。⭐ **求值端的通过率与能力度量必须分开两套。**
3. ⛔⛔ **向 oracle 过拟合有已记录的实例**（C.2 的 `minRanF = 3`）。⭐ 若 M1 把裁决权交给 pyfcstm，⛔ 必须同时准备一个**「过了但退化了」的检查**，⭐ 否则会复制这个坑。
4. ⛔ **单次运行、无方差、无 `@k`**。⭐ 我们已经在报 `hit@1 / hit@3 / hit@all`，⛔ **这一点上我们比它严格**，⭐ 不要因为它是 CCF-A 就往回退。
5. ⛔ **prompt 只以截图公开** —— ⭐ 记为反面教材；⭐ 我们的 prompt 在源码里是文本，⭐ 保持。

### 3. ⚠️ 与我们的关键差别（⛔ 说明为什么不能直接照搬）

1. ⛔⛔ **任务方向相反。** ⭐ 它是「**造一个能过检查的模型**」（生成 + 修复）；⭐ 我们是「**在给定模型里找出它违背 NL 的地方**」（缺陷检测）。⭐ 后果：⛔ **它的循环有一个天然的、单调的成功判据**（verdict 向量全 MATCH），⛔ **我们没有** —— ⭐ 我们的「找到一条缺陷」不存在一个可让 oracle 判定的收敛点。⛔ **所以它的循环形状不能整体照搬**，⭐ 能搬的是「确定性定位」「期望结果双侧钉」这两个零件。
2. ⛔ **制品界外。** ⭐ CSP# 有并行合成与交错，⛔ 我们的 $M = (S,E,V,Tr,A)$ 无并发。⭐ 按 L3 的规定本卡不设边界门，⛔ **但任何要进论文的引用必须回 L1 重走边界门**。
3. ⚠️ **模型代际。** ⭐ o3-mini / claude-3-7-sonnet / R1 都是 2025 年初一代；⭐ 我们跑的是 `gpt-5.5` / `claude-opus-4-7`。⛔ **绝对数字不可横比。**
4. ⚠️ **规模不可比。** ⭐ 它 40 系统 / 133 断言、单次；⭐ 我们 54 pair × 2 模型 × 3 轮 = 324 格、台账 98 条。

---

## F. ⛔ 存疑与未核项

1. ⚠️ **完整 prompt 未逐文件核到** —— ⭐ 已试过 `Appendix/Prompt_Example/`（⛔ 只有两张 PNG）与 `gh api` 列 `Automated_Pipelines/` 顶层（⭐ 只到 `Full_Pipeline/` / `No_Planning/` 两个目录名），⛔ **未下钻到源码里找 prompt 常量**。⭐ 因此 D 节 prompt 一行判 🟠 而非 🟢。
2. ⚠️ **「curated the examples that can be formalized in the syntax defined in section II」筛掉了多少** —— ⛔ 原文未提供筛前候选数，⛔ 也未提供排除理由分布。⭐ 这意味着 40 这个分母是**筛后**的。
3. ⚠️ **user study 的 `Assertion Accuracy` 谁判的** —— ⛔ 原文未提供；⭐ 「语义上是否对齐意图」必须有人判，⛔ 但论文未说判定者、未报一致性（$\kappa$ 或一致率）。⭐ 已试过通读 §V 全节。
4. ⚠️ **界面 demo 视频未核到文件** —— ⭐ 已试过列 `Appendix/Interface_Screenshots/`（目录存在），⛔ 未下钻到文件级。
5. ⚠️ **C.3 那段自相矛盾的来源是推测** —— ⛔ 我方判断它是别处粘来的残留，⛔ **论文没有任何说明**，⛔ 也没有 erratum。⭐ 已试过在全文与 References 里找呼应，⛔ 未找到。
6. ⚠️ **每次运行的 token / 花费未报** —— ⭐ 只报墙钟（median 4.34 min/system）。⛔ 因此**无法与我们的 212.6× 成本比横比**。
7. ⚠️ **正式出版版本与 arXiv v1 是否有差异未核** —— ⭐ 本地 `paper.pdf` 是 arXiv v1（页脚 `arXiv:2509.23675v1 [cs.SE] 28 Sep 2025`）；⭐ ASE proceedings 版（DOI `10.1109/ASE63991.2025.00176`，pp. 2122–2133）**未取到全文**（⛔ IEEE 需订阅）。⛔ **C.3 那段矛盾是否在正式版被删掉，本轮无法确认。**
