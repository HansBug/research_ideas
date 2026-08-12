# 卡片 · Mao, Wang, Sun, Qin & Xiong, ICSE 2025 —— AutoSM：⭐ 把符号模型生成**拆成四段**，⛔ 每段边界都放在能证 sound 的地方

⭐ **全文已取到并通读**（⛔ 不是仅据摘要）。⭐⭐ **本仓库早已收录过这篇** —— ⭐ 它在 [`baselines/llm-aided-security-protocol-verification/`](../../../../baselines/llm-aided-security-protocol-verification/) 有完整四件套（`paper.pdf` 999 KB · `paper_content.txt` 75 KB · `bibtex.bib` · `DESC.md` 35 KB）。⭐ 本卡按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 重抽，⭐ 聚焦 L3 关心的**流水线形态**（⛔ 而 `DESC.md` 是 baseline 视角）。

⚠️⚠️ **标识符先纠一处**：⛔ **论文标题里没有 "AutoSM" 这三个字。** ⭐ 正式题名是 **"LLM-aided Automatic Modeling for Security Protocol Verification"**；⭐ `AutoSM` 只是**工具/仓库名**（⭐ 逐字来源：参考文献 [1] 的 URL `https://github.com/zerrymore/AutoSM`）。⭐ 详见 [§A](#a-元信息)。

⚠️ **本卡开头先按任务书顺序答三个必答问题。**

---

## ⭐⭐ 必答① · 「直接生成失败」是实验对照还是设计理由？数字是多少？

⭐⭐ **答案：两者都是 —— ⭐ 既写成设计理由（§III-A 给了机理），⭐ 也有一组正面对照实验（Fig. 8）。⛔ 但对照的粒度很粗：只有一张柱状图 ＋ 正文一句数字，⛔ 没有逐模型逐案例的表。**

### ⭐ ① 作为设计理由（⭐ 摘要 ＋ §III-A）

⭐ 摘要逐字（M）：

> "Although LLMs are powerful in various code generation tasks, **it is shown to be ineffective in generating symbolic models (according to our empirical study).** Therefore, rather than applying LLMs naively, we carefully decompose the symbolic protocol modeling task into several stages"

⭐ §I 逐字（M，⭐ 给出两条机理）：

> "we observe (with empirical evidence based on our preliminary study) that **LLMs cannot be naively adopted to solve the problem directly** (i.e., generating symbolic models of security protocols based on their natural language documents). Compared with tasks such as generating natural language text or Python code, generating symbolic protocol models are considerably more challenging as **(1) there are limited samples that LLMs can learn from**, and **(2) unlike natural language texts, such symbolic models must be precise, as they are used for formal analysis.**"

⭐ §III-A 有专门的小标题（M，逐字）：**"Intuitive code generation is infeasible and untrustworthy."**

> "LLMs have demonstrated their impressive capabilities in code generation. It may seem intuitive to treat the modeling task as a form of code generation. However, unlike common programming languages such as Python, **LLMs are unfamiliar with formal specification languages (due to the missing of dedicated datasets).** On the other hand, it is vital to ensure the correctness of the symbolic model as the model is intended for formal verification."

⭐ §VIII 还专门用一段解释"为什么数据没法对齐"（M，逐字，⭐ 这条对我们有独立价值）：

> "While papers ([4], [5]) and open-source models ([44], [45]) could serve as potential pretraining data for LLMs, directly using such datasets remains challenging due to **the difficulty of perfectly aligning the documents with the symbolic model.** Take TLS 1.3 paper [4] as an example, the authors provide a modeling note with side-by-side comparison of the specification and the model to show how a symbolic model is constructed from the document, which includes certain key 'simplifications' and 'assumptions'. **In most cases, such notes are not available, but are the key to align the document with the human-written models. Even with these notes, there is no perfect alignment between them.**"

### ⭐⭐ ② 作为实验对照（⭐ Fig. 8）—— ⛔ **数字在这里**

⭐ 逐字（M，§VII-C "Summary of Comparisons"）：

> "**We take the few-shot learning as the baseline.** As shown in Figure 8, while **3-shot learning generates a maximum of 4 cases**, our method shows superior performance, **automatically generating correct models in 10 out of 18 cases.**"

⭐ Fig. 8 图注逐字（M）："Comparison of few-shot learning with our method"，⭐ 横轴 `0-shot / 1-shot / 2-shots / 3-shots / ours`，⭐ 四条模型序列 **GPT-4 · GPT-4o · GPT-3.5-turbo · Gemini-Pro**，⭐ 纵轴 `Success cases (n)`，⭐ 刻度 `0 2 4 6 8 10`。

⭐⭐ **可引用的数字（⛔ 只有这一组）**：

| 臂 | 成功案例数 | 分母 | 换算 |
| :-- | :-: | :-: | :-- |
| ⛔ **few-shot 直接生成（最好的一档 3-shot，最好的模型）** | ⛔ **≤ 4** | 18 | ⛔ **≤ 22.2%** |
| ⭐ **AutoSM 四段式** | ⭐ **10** | 18 | ⭐ **55.6%** |
| ⭐ **差** | ⭐ **+6 例** | — | ⭐ **+33.3 pp** |

⚠️⚠️ **三条必须带上的限定：**

1. ⛔ **逐模型逐档的确切数字只在柱状图里，正文只给了"maximum of 4"。** ⭐ 即 `0/1/2/3-shot × 4 模型 = 16` 个数据点，⛔ **正文只披露了它们的上界**。⛔ 不能引用任何"某模型某档 = N"的数字。
2. ⛔ **baseline 是"直接生成到最终目标语言"** —— ⭐ 即让 LLM 直接产出 SAPIC⁺/Tamarin 模型。⛔ **不是"少一个阶段"的消融**。⭐⭐ **所以这组数字证明的是"分阶段 vs 不分阶段"，⛔ 不是"分成四段 vs 分成两段"** —— ⛔ **论文没有任何逐阶段消融。**
3. ⛔ **两臂的 ground truth 与判定装置相同**（⭐ 见 [C](#c-实验)），⭐ 这一点是公平的；⛔ 但 ground truth 的 λ 表达式与 SAPIC⁺ 模型都是**作者自己手工构造**的，⭐ 而 λ-DSL 也是作者设计的 —— ⚠️ **自证风险，见 [C](#c-实验) 的 `judged_by`。**

### ⭐ ③ 还有第二条对照：与 correct-by-construction 方法比

⭐ §VII-D 逐字（M）：⭐ 与 Alice&Bob 记号输入的 correct-by-construction 方法 [8] 比，⭐ 取 **4 个协议案例**，⛔ 结论是**等价而非胜出**：

> "According to experiment data in [1], given a set of properties Φ, **both the symbolic models generated from [8] and our approach can be successfully verified, which demonstrates their equivalence under our definition.**"

⚠️ ⭐ **这条对照的意义要看清**：⛔ 它不是「我们更好」，⭐ 而是「我们的输出与一个已被接受的确定性方法**在性质上等价**」—— ⭐ 即**用它当交叉验证**。⭐⭐ **而 [8] 的输入是 Alice&Bob 记号（已经半形式化），⭐ AutoSM 的输入是 NL 文档** —— ⭐ 差别在输入端，⛔ 不在输出质量。⭐ **这个论证形状可以搬**（⭐ 见 [E.1](#e-对-m1-的意义)）。

---

## ⭐⭐ 必答② · 分成几个阶段？分阶段的判据是什么？

⭐ **答案：4 段。⭐⭐ 而判据非常明确 —— ⛔ 不是"任务看起来该怎么切"，⭐ 而是「⭐⭐ 切在能建立形式化执行模型、并能证明相邻两段之间变换 sound 的地方」。**

### ⭐ 四段（M，§III-B 逐字编号）

| # | 阶段 | 执行者 | 输入 → 输出 |
| :-: | :-- | :-- | :-- |
| **S1** | ⭐ **L-CCG**（LLM-powered CCG parser） | ⭐ **LLM** | ⭐ 协议文档 → **λ-DSL 表达式** |
| **S2** | ⭐ **L-REPAIR** | ⭐ **LLM ＋ 确定性静态分析 ＋ 人** | ⭐ λ → **well-formed λ** |
| **S3** | ⭐ **Rewriter** | ⭐⭐ **纯确定性**（⭐ 规则 T1–T8，⭐ **证明 sound**） | ⭐ wf-λ → **SAPIC⁺ 规约 $\mathcal{P}$** |
| **S4** | ⭐ **Compiler** | ⭐⭐ **纯确定性**（⭐ SAPIC⁺ 现成编译器，⭐ soundness 引自 [12]） | ⭐ $\mathcal{P}$ → **Tamarin / ProVerif / DeepSec 模型** |

⭐ 逐字（M，§III-B）："our approach, illustrated in Figure 3, consists of four stages: (1) L-CCG: a LLM-powered CCG parser […] (2) L-REPAIR: which repairs the broken specifications with static analysis techniques and user interaction to make it well-formed. (3) Rewriter: which transforms the lambda expressions into a SAPIC⁺ specification 𝒫. (4) Compiler: which takes the well-formed SAPIC⁺ process 𝒫 as input and compiles it into models ℛ accepted by verifiers: Tamarin, DeepSec, and ProVerif directly."

### ⭐⭐⭐ 切点判据（⛔ 这一格是本卡对 M1 最值钱的东西）

⭐ **判据有三条逐字表述，⭐ 三条说的是同一件事：**

**① 「LLM 只负责从 NL 里抽要素，形式对象之间的变换交给可证 sound 的算法」**（M，§III-B 逐字）：

> "**Our insight is to only use LLMs for extracting necessary ingredients for the final model while relying on a series of formal models to establish layered correctness for the final symbolic model.**"

**② 「每一段都定义在一个形式化执行模型上，相邻段之间建立 refinement / trace inclusion 关系」**（M，摘要 ＋ §X 逐字）：

> 摘要："To ensure the correctness of the generated symbolic model, **each stage is designed based on a formal execution model and the model transformations are proven sound.**"
> §X："The insight of our framework is that **we break down the entire process into multiple steps, where each defined within a formal model and refinement relations are established between them.**"

**③ 「中间对象要选在人能直观校验的那一层」**（M，§VIII "Guarantee for trustworthiness" 逐字）：

> "**we need to validate some intermediate results that are intuitive and easy to understand.** Meanwhile, we design algorithms and construct proofs to ensure the consistency between these intermediate results and the final output. We believe this effort is inevitable (and hopefully minimal) to ensure the overall correctness as **this is the most intuitive representation for humans to understand (compared to validating the symbolic model directly).**"

⭐⭐ **归纳成一句可搬的判据**：

> ⭐⭐ **切点应当落在「⭐ 上游是 LLM 能可靠产出的、⭐ 下游是能被确定性算法 sound 地变换的、⭐ 而这一层本身是人/工具能校验的」那个位置。**

⭐ **这个判据在论文里是被兑现的，⛔ 不只是说法**：⭐ 它真的给出了 soundness 链条 —— ⭐ Lemma 1（$\mathcal{P} \models \phi \Rightarrow \Lambda \models \phi$，⭐ 靠 $\mathrm{traces}(\Lambda) \subseteq \mathrm{traces}(\mathcal{P})$）· ⭐ Theorem 1（⭐ 引自 [12]）· ⭐ Corollary 1 串起三层。

### ⭐ 中间语言为什么是 λ 演算（⛔ 这是切点判据的第二半）

⭐ 逐字（M，§IV 开头）：

> "In this section, we introduce a dedicated lambda calculus ($\lambda$-DSL) to specify security protocols in an intuitive manner, **so that it is easier to be generated by LLMs.**"

⭐ 并且给了一条**语言学观察**当依据（M，§IV-B 逐字）：

> "From the perspective of lambda calculus, we observed that **a sentence in a protocol's document is often an application**, i.e., instantiating arguments of the key predicate with ground terms (e.g., role name, explicit message)."

⭐ 脚注还交代了 CCG 的来历（M，逐字）："CCG: combinatory categorial grammar [23], which is a rule-based system coupling syntax and semantics. It can take the natural language sentence as input and output a lambda expression. **Here we use the LLM to serve as a CCG parser.**"

⭐⭐ **即：⭐ 中间语言的选择不是随手定的，⭐ 而是"从 NL 到形式对象"这条路上一个有语言学理论背书的中继站（CCG → λ），⭐ 且刻意设计成 LLM 好生成、人好读。**

---

## ⭐⭐ 必答③ · 制品是什么？边界？

### ⭐ 制品链（⛔ 四层，⭐ 每层都是制品）

| 层 | 是什么 |
| :-- | :-- |
| ⭐ **λ-DSL** | ⭐ 专用 λ 演算，⭐ **带完整操作语义**：配置 $c = (\mathcal{E}, \mathcal{I}, \sigma)$，⭐ 迁移规则 `GEN` / `SEND` / `RECV` / `SIGNAL` / `ADV`，⭐ trace 定义（Def 4） |
| ⭐ **SAPIC⁺ 规约** | ⭐ applied-$\pi$ 演算的一个方言（⭐ 出处 [12]），⭐ 一份规约可喂三个后端 |
| ⭐ **Tamarin MSR 模型** | ⭐ multiset rewriting rules，⭐ 状态编码为 facts，⭐ 构成迁移系统 |
| ⭐ **ProVerif / DeepSec 模型** | ⭐ 同一 SAPIC⁺ 编译的另两个后端 |

### ⚠️ `boundary` ＝ **`界外`**

⭐ 按 [README.md](../README.md) §2.1 的三档，⛔ **这篇明确落在 `界外`**，⭐ 三条理由都是承重的（M）：

1. ⛔⛔ **它是进程代数，不是状态机。** ⭐ λ-DSL 的语法是 $P ::= E; P \mid \mathbf{cond}\ \alpha\ P\ \mathbf{else}\ Q$，⭐ 事件 $E ::= e(\overline{a}, \overline{t}) \mid \bot$ —— ⭐⭐ **没有显式状态集 $S$，⛔ 没有 $Tr \subseteq S \times \dots \times S$。** ⭐ 状态是**隐式的**（⭐ 配置 $(\mathcal{E}, \mathcal{I}, \sigma)$ 里的 continuation）。⭐ 下游 SAPIC⁺ 是 applied-$\pi$，⭐ Tamarin 是 MSR —— ⛔ 三层没有一层是 $M = (S,E,V,Tr,A)$。
2. ⛔⛔ **无界并发是问题定义的一部分。** ⭐ 逐字（M，§IV-C）："A protocol is executed by agents who can play any role of the protocol **arbitrary times** [25], e.g., multiple authenticated clients can establish an **unbounded number of sessions** with the server." ⭐ $\mathcal{I}$ 逐字定义为 "a multiset representing the protocol instances **executing in parallel**"。⭐ Fig. 6 专门画了两种执行模型（⭐ $\Lambda$ 里线程受全局序约束、$\mathcal{P}$ 里线程并行）并给出 $\mathrm{traces}(\Lambda) \subsetneq \mathrm{traces}(\mathcal{P})$。
3. ⛔ **Dolev-Yao 攻击者是语义的一部分。** ⭐ 迁移规则里有 `[ADV]`（M，Fig. 4），⭐ §V-C 逐字 "The threat model is Dolev-Yao [33], where an adversary can inject, modify and intercept messages on the network."

⭐ ⛔ **无时钟无时间约束**（⭐ 这一点与 $M$ 一致），⛔ 但上面三条足以判界外。

⭐ **与本仓库既有记录一致**：⭐ [`baselines/SUMMARY.md`](../../../../baselines/SUMMARY.md) 第 24 行把它归为 **"邻近形式化建模"**，⭐ 并逐字注 "SAPIC+/Tamarin/ProVerif/DeepSec 形式验证链路，模型变换有 soundness 论证｜**但输出非 STM**"；⭐ 更新日志逐字 "**Event-B / PAT / SAPIC+ 属异构形式模型近邻，不作为同构 STM baseline**"。⭐ 本卡的 `界外` 与这两条不冲突。

⛔⛔ **提醒：⭐ L3 [不设](../README.md) 边界门，⭐ 但这篇要进 L1/L2 会被边界门挡住。** ⭐ 它在本轨的价值是**流水线形态**（⭐ 尤其"分阶段的判据"），⛔ 不是可比数字。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `icse2025-autosm` |
| `title` | ⭐ **"LLM-aided Automatic Modeling for Security Protocol Verification"**（M，⭐ PDF 第 1 页标题、`bibtex.bib` `title` 字段、IEEE 题录三源一致）。⚠️ ⛔ **"AutoSM" 不在标题里** —— ⭐ 它是工具名，⭐ 逐字出处是参考文献 [1] 的 URL：`https://github.com/zerrymore/AutoSM` |
| 作者 | ⭐ **Ziyu Mao¹ · Jingyi Wang¹\*** · **Jun Sun²** · **Shengchao Qin³** · **Jiawen Xiong⁴**（M）。⭐ ¹ Zhejiang University, Hangzhou · ² Singapore Management University · ³ Xidian University · ⁴ East China Normal University。⭐ `*` ＝ 通讯作者 ＝ Jingyi Wang |
| `year` | ⭐ **2025**（M，⭐ PDF 页边逐字 "2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)"；⭐ `bibtex.bib` `year = {2025}, month = apr`）。⛔ 无 early-access 歧义 |
| `venue` | ⭐ **ICSE 2025**（⭐ IEEE/ACM 47th International Conference on Software Engineering），⭐ **主会 Research Track**，⭐ pp. **642–654**（M，`bibtex.bib` `pages = {642--654}`；⭐ PDF 页脚页码 642–652 与之一致）。⭐ ISSN 1558-1225 · ISBN 979-8-3315-0569-1 |
| `ccf` | ⭐⭐ **A** —— ⭐ 已查本仓库 [ccf_venues/](../../../../../ccf_venues/)：⭐ [`conf-a-icse`](../../../../../ccf_venues/conf-a-icse/README.md) 建档，⭐ [SUMMARY.md](../../../../../ccf_venues/SUMMARY.md) 逐字 "软工综合最高目标，四个 project 都可对齐"，⭐ [01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 标 `🏆` |
| `doi` | ⭐ [`10.1109/ICSE55347.2025.00197`](https://doi.org/10.1109/ICSE55347.2025.00197) —— ⭐ **已实际访问核验**（⭐ 本仓库 `bibtex.bib` 已记；⭐ IEEE 文档号 [11029741](https://ieeexplore.ieee.org/document/11029741/)） |
| `arxiv` | ⛔ **无**（⭐ 已试 arXiv 检索，⛔ 无对应条目） |
| `url` | ⭐ [ieeexplore.ieee.org/document/11029741](https://ieeexplore.ieee.org/document/11029741/) · ⭐ 本地全文 [`baselines/llm-aided-security-protocol-verification/paper.pdf`](../../../../baselines/llm-aided-security-protocol-verification/paper.pdf) |
| `artifact_type` | ⭐ **符号协议模型**：λ-DSL → SAPIC⁺ → Tamarin MSR / ProVerif / DeepSec（⭐ 四层制品链，见 [必答③](#-必答--制品是什么边界)） |
| `task` | ⭐ **生成**（NL 文档 → 符号模型）＋ ⭐ **修复**（S2 的 L-REPAIR）。⛔ **不是缺陷检测**（⭐ 下游 Tamarin 找的是协议漏洞，⛔ 不是模型缺陷） |
| `boundary` | ⛔ **`界外`**（⭐ 进程代数 ＋ 无界并发 ＋ Dolev-Yao 攻击者，⛔ 无显式状态集）—— ⭐ 见 [必答③](#️-boundary--界外) |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ 按论文 Fig. 3 的 S1–S4 ＋ Algorithm 1/2 展开）

```
[人]     手工把协议文档切成 chunks（⭐ 逐字 "we manually segment each document into a list of chunks"）
   ↓
┌── S1 · L-CCG（Algorithm 1）───────────────────────────────────────────┐
│ [确定性] Segment(nl) → chks = [k₁ … k_M]                              │
│ [确定性] 为每个 chunk 组装上下文 ctx ＝ 相邻 N 个 chunk ＋ 它们已产出的 λ  │
│ [LLM]   Parse(ctx, kᵢ) → λ 表达式（⭐ few-shot in-context）  ⭐ 逐 chunk 顺序 │
└──────────────────────────────────────────────────────────────────────┘
   ↓ lambda
┌── S2 · L-REPAIR（Algorithm 2）────────────────────────────────────────┐
│ [LLM]   ① Validate(P, nl)  ⛔ **LLM 自评**（对着 NL 复审并改错）          │
│ [LLM]   ② View(P)          ⭐ 用 diff 格式的例子教它把 recv 消息改成局部可读 │
│ [确定性] ③ Analysis(P) ＝ Lark parser 建 AST → 找未绑定变量集 V           │
│            ├─ V = ∅ → 返回                                            │
│            └─ V ≠ ∅ ↓                                                │
│ [确定性] ④ Graphviz(P) → MSC 消息序列图（⭐ 给人看的）                     │
│ [人]    ⑤ Interact(msc, V, /user) → 人直接改 λ ──→ 回 ③  ⭐ **人在环循环**  │
└──────────────────────────────────────────────────────────────────────┘
   ↓ wf-lambda
[确定性] S3 · Rewriter：规则 T1–T8 → SAPIC⁺ 规约  ⭐⭐ **证明 sound（Lemma 1）**
         ＋ [LLM] top specification 合成（⭐ few-shot，⭐ 产出 𝒫_t 初始化部分）
   ↓ SAPIC+
[确定性] S4 · Compiler：SAPIC⁺ → Tamarin MSR / ProVerif / DeepSec  ⭐⭐ **sound（Theorem 1，引自 [12]）**
   ↓
[⭐ sound oracle] Tamarin 1.8.0 验性质  ⛔⛔ **只在评测时用，⛔ 不回灌进任何循环**
```

⭐⭐ **合计 11 段（⭐ 按上图的可数环节）· 其中 LLM 4 段**（⭐ S1 的 `Parse` · S2 的 `Validate` · S2 的 `View` · S3 的 top spec 合成）· ⭐ **确定性 6 段** · ⭐ **人 2 段**（⭐ 手工分块 · S2 的 `Interact`）。

⚠️⚠️ ⭐ **评测时人环被关掉**（M，两处逐字）：⭐ §V-B "When evaluating our overall approach for automatic modeling in Section VII-C, **we do not allow any user interaction for repairing.**" ⭐ §VII-B "we do not introduce any user-interaction."
⭐⭐ **所以自动化评测下的实际流水线是：S1（LLM）→ S2 只跑 ①②（两次 LLM）→ ③ 检测但不修 → S3 → S4。** ⛔ **修复循环在自动模式下退化成"检测到就放弃"。**

⚠️ ⭐ **top specification 由 LLM 合成这一点很容易漏**（M，§V-C 逐字）："We first collect all of the signatures of the local process $\mathcal{P}_r$, then **incorporate in-context few-shot learning to teach LLMs how to give a top specification** $\mathcal{P}_t$." ⭐ 即 S3 **不是纯确定性** —— ⛔ 角色进程的重写是确定性的（T1–T8），⭐ 但**顶层进程（协议初始化、角色实例化、`!` 复制）是 LLM 生成的**。⚠️ ⛔ **而这一部分没有 soundness 证明覆盖** —— ⭐ Lemma 1 证的是 $T$ 的 soundness，⛔ 不是 $\mathcal{P}_t$ 的正确性。

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| ⭐ `S1 · Parse` | ⭐⭐ **翻译器**（⭐ NL chunk → λ 表达式，⭐ 形式化转换）＋ **抽取器** |
| ⛔ `S2 · Validate` | ⛔⛔ **评审者（LLM 自评）** —— ⭐ 逐字 "**we introduce a self-validation method (Line 1) following [30]. Without introducing extra information, we instruct a LLM to review the specification alongside the given protocol description, finding and correcting the mistakes generated during the parsing stage.**" ⭐ **兼修复者** |
| ⭐ `S2 · View` | ⭐ **修复者**（⭐ 把 `recv` 消息从全局视角改写成角色局部可读形式，⭐ 用 diff 格式的 worked example 教） |
| ⭐ `S3 · top spec` | ⭐ **生成器**（⭐ few-shot 产出 SAPIC⁺ 顶层进程） |
| ⛔ **裁决者** | ⛔⛔ **LLM 从不担任** —— ⭐ 循环的判定权在 Lark parser 手里，⭐ 见 [B4](#b4--循环与裁决者本轨最关键的一格) |

### B3 · prompt 策略

| 策略 | 有无 | 证据 |
| :-- | :-: | :-- |
| ⭐⭐ **few-shot in-context learning** | ⭐ **有（三处都是）** | ⭐ M：S1 `Parse` 逐字 "Utilizing **few-shot in-context learning** (Line 11)" ＋ "We implement the Parse function (Line 11) with in-context few shots learning. Following [28], [29], we design prompts to instruct the LLM in writing lambda expressions, all of which are provided in [1]."；⭐ S2 `View` 逐字 "we encode a set of examples **in the diff [31] format** to teach the LLM how to transform a message into a correct form in the role specification step-by-step"；⭐ S3 逐字 "incorporate in-context few-shot learning" |
| ⭐⭐ **滑动窗口分块 ＋ 已产出结果进上下文** | ⭐ **有** | ⭐ M，Algorithm 1 逐字：⭐ 上下文 `blk ← k_{i−N+j} + L_{i−N+j}`，⭐ 即**相邻 N 个 chunk 的原文 ＋ 它们已经产出的 λ 表达式**一起进 prompt。⭐ 理由逐字："Recent research [27] shows that '**LLMs may get lost in the middle**' […] This chunk-by-chunk approach allows the LLM to concentrate on the immediate context, thereby minimizing the risk of missing intermediate details" |
| ⛔ **LLM 自评（self-validation）** | ⛔ **有** | ⭐ M，见 [B2](#b2--每次-llm-调用的角色) 的 `Validate` |
| ⭐ **diff 格式作为教学与输出形式** | ⭐ **有** | ⭐ M，Example 2 完整给出了一个 diff（⭐ `- @send(C,k) // Ambiguity of 'it'` / `+ @send(@aenc(k, pkS))`） |
| ⛔ 结构化输出约束（JSON schema / 受限解码）· CoT · self-consistency 投票 · 多智能体辩论 · tool calling · RAG 检索 | ⛔ **原文未提供** | ⭐ 全文无相关表述（S）。⚠️ ⛔ **λ-DSL 的 BNF 是拿来做事后 parse 的（Lark），⛔ 不是拿来约束解码的** |
| ⭐ 温度 | ⭐ **0.4** | ⭐ M，§VII 逐字 "with a **temperature setting of 0.4** for both semantic parsing and automated repairing" |

⭐⭐ **prompt 公开**（M，§V-A 逐字）："we design prompts to instruct the LLM in writing lambda expressions, **all of which are provided in [1]**." ⭐ [1] ＝ `github.com/zerrymore/AutoSM`（⭐ 已机械核验可取，见 [D](#d-资产)）。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

⭐⭐ **有一个循环，⭐ 裁决者是确定性 parser，⛔ 修复动作是人做的 —— ⭐ 而自动模式下这个循环被关掉了。**

| 循环 | 裁决者 | ⭐ 类型 | 修复者 | 终止条件 | 最大轮数 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| ⭐ `Analysis → Interact → Analysis`（⭐ Algorithm 2 Lines 3–9） | ⭐⭐ **`Analysis(P)` ＝ Lark parser 建 AST 后查未绑定变量** | ⭐⭐ **`parser / 编译器`** | ⛔ **人**（`Interact(msc, V, /user)`） | ⭐ **$V = \emptyset$**（⭐ 收敛，⛔ 无别的出口） | ⛔ **原文未提供**（⭐ `while true`，⛔ 无 cap） |
| ⛔ `Validate`（⭐ Line 1） | ⛔ **LLM 自评** | ⛔ **`LLM 自评`** | ⭐ 同一次调用 | ⭐ **单次，⛔ 不迭代** | ⭐ **1** |
| ⛔ **模型检查器进循环** | ⛔⛔ **没有** | — | — | — | — |

⭐ **逐条对照 schema 词表**：⭐ `parser / 编译器` = **有（裁决者就是它）** · ⛔ `LLM 自评` = **有（但不迭代）** · ⛔ **`人` = 有（且是唯一的修复者）** · ⛔⛔ **`sound oracle` = 不在循环上** · ⛔ `确定性规则` = 有（well-formedness Def 5）· ⛔ `测试执行` = 无。

#### ⭐⭐⭐ Tamarin 在哪里？—— ⛔ **只在评测端，⛔ 不在循环里**

⚠️⚠️ **这一点必须说清，⛔ 因为很容易误读成"有模型检查器闭环"。** ⭐ Tamarin 1.8.0 的作用只有两个：⭐ ① 评测时判"生成的模型对不对"（⭐ Def 7 语义等价：把参考模型上已验证的性质集 $\Phi$ 拿到生成模型上跑，⭐ 全过才算对）；⭐ ② 论文的下游应用演示。⛔ **它的输出从不回灌给 LLM，⛔ 也不驱动任何重试。**

⭐⭐ **与 [ERTS 那篇](./erts2026-safe-llm-mde.md) 恰好相反**：⭐ ERTS 把模型检查器**接进循环当裁决者**（⛔ 结果 5/6 撞上限不收敛）；⭐ AutoSM 把它**留在循环外当评测装置**（⭐ 而靠 soundness 证明来保证"变换不引入错误"）。⭐⭐ **两条路的对照对 M1 直接有用，见 [E](#e-对-m1-的意义)。**

#### ⭐⭐ 有无报告循环的边际收益 —— ⭐⭐ **有！⭐ 而且是一个可直接引用的数字**

⭐ **LLM 自评修复的收益：⛔ 平均只降 14.74% 的错误。** ⭐ 逐字（M，§VII-B "Different LLMs for repairing"）：

> "We evaluate the repairing with different models. The result (included in [1]) shows that the effectiveness of repairing relies on advanced LLMs. **For most complex cases, automatic repairing is not enough to resolve all the issues (reduce error average 14.74% with GPT-4). That's the reason why it is necessary to introduce user-interaction when deploying our tool in practice.**"

⭐⭐⭐ **这是一条对我们极有价值的外部实测**：⭐ **一个 ICSE 主会的工作，⭐ 用 GPT-4 做 LLM 自评修复，⭐ 平均只把错误降低 14.74%，⛔ 并据此把人拉回环里。**

⚠️ **两条限定：**
1. ⛔ **逐案例数字在仓库里，不在论文里**（⭐ 逐字 "The result (included in [1])"）—— ⭐ 论文只给了这一个平均数。
2. ⛔ **它是"跑一次自评"的收益，不是"逐轮"的收益** —— ⭐ `Validate` 只跑一次不迭代，⛔ 所以这个 14.74% 是**单轮**数字，⛔ 无法与我们「第 3–5 轮零收益」逐轮对齐；⭐ **但它与我们「LLM 自评 reviewer 净收益 ≈ 0」在方向上一致，⭐ 且量级上给了一个上界参考。**

#### ⭐ 另有一个 `@k` 形态的多次运行口径（⭐ 见 [C](#c-实验)）

⭐ 逐字（M，§VII-C）："we set the **run iterations as 5** for each protocol case […] with **success ratio ranging from 2/5 to 5/5**." ⭐⭐ **Table IV 的 `Success Ratio` 列就是逐案例的 `n/5`** —— ⭐ 这实质上是 `hit@k` 的一个早期形态（⛔ 论文没这么命名）。

### B5 · ⭐ 中间表示

⚠️ **三套，⭐ 各自闭合程度不同 —— ⛔ 这一格与我们的 19 条谓词对照最紧。**

| | ⭐⭐ ① λ-DSL 事件符号表 | ⭐ ② 缺陷类型学 | ⭐ ③ well-formedness 定义 |
| :-- | :-- | :-- | :-- |
| 有无 | ⭐ 有 | ⭐ 有 | ⭐ 有 |
| 形态 | ⭐ **DSL / 中间 IR**（⭐ 带操作语义与 trace 定义） | ⭐ **缺陷类型学**（⭐ 3 类） | ⭐ **确定性谓词**（⭐ 3 条） |
| ⭐ **内容** | ⭐⭐ **$e ::= \mathbf{gen} \mid \mathbf{send} \mid \mathbf{recv} \mid \mathbf{know} \mid \mathbf{op}$ —— ⛔ 只有 5 个事件符号** | ⭐ **Inconsistency**（⭐ 幻觉/随机导致偏离 NL）· **Ambiguity**（⭐ NL 有歧义 → 未绑定变量）· **Unreadability**（⭐ `recv` 消息用了全局视角、角色本地拿不到） | ⭐ Def 5（⭐ 引自 [25]）：⭐ ① $P$ 中任何变量都被绑定 · ② 任何收到的消息对该角色可读 · ③ 任何事件的执行者是 $R$ 中的角色 |
| ⭐ **是否闭合** | ⭐⭐ **本文内闭合，⭐ 但明说可扩展** —— ⭐ 逐字 "In this work, we consider the symbol set $e$ presented in the above syntax, **which can be extended to other event symbols.**" | ⭐ **闭合到 3 类** | ⭐ **闭合到 3 条** |
| ⭐ **谁定的 / 谁选** | ⭐⭐ **作者预编词表 ＋ LLM 在每个 chunk 上自由组合** —— ⭐ LLM 不能自造事件符号，⛔ 但可自由嵌套 $\Sigma$ 里的密码原语与项 | ⭐ **作者从实测归纳**（⭐ 逐字 "According to our observation" / "we summarize three kinds of problems that mainly occur in the initial generated model"） | ⭐ **引自已有文献 [25]**（⭐ ① 类出处） |
| ⭐ **每类怎么处理** | — | ⭐⭐ **三类三种机制，一一对应**：⭐ Inconsistency → **LLM 自评**（`Validate`）· Unreadability → **LLM ＋ diff 例子**（`View`）· Ambiguity → ⭐⭐ **确定性静态分析 ＋ 人**（`Analysis` ＋ `Interact`） | ⭐ Def 5 的 ① 就是 `Analysis` 查的东西 |

⭐ 另有**类型系统**（M，§IV-B）：⭐ supersort `msg`，⭐ 两个 subsort `agent` / `nonce`（⭐ 出处 [24]）。

#### ⭐⭐⭐ 与我们 19 条闭合谓词的对照

| 维度 | ⭐ 它（5 事件符号 ＋ 3 类缺陷 ＋ 3 条 wf） | ⭐ 我们（19 条谓词） |
| :-- | :-- | :-- |
| 闭合性 | ⭐ **闭合**（⭐ 且明说可扩展） | ⭐ **闭合**（⛔ 未明说可扩展） |
| ⭐ **谁选** | ⭐⭐ **LLM 在每个 chunk 上自由组合闭合符号** —— ⭐⭐ **与我们「LLM 自动选」是同一形状** | ⭐⭐ **LLM 在每条需求上自动选** |
| ⭐ 粒度 | ⭐ **一个 chunk 一组 λ 表达式** | ⭐ **一条需求一个谓词 ＋ 一个断言脚本** |
| ⭐ **闭合词表的大小** | ⭐ **5**（⭐ 事件符号）—— ⛔ 极小 | ⭐ **19** |
| ⭐ **缺陷类型学的用途** | ⭐⭐ **每一类挂一个专门机制** —— ⭐ 且**语义类交给人、词法类交给 LLM** | ⚠️ 我们的五类多报分类只用于**事后归因**，⛔ 不驱动不同机制 |
| ⭐ 出处分级 | ⭐ wf 定义引 [25]（① 类）· 类型系统引 [24]（① 类）· ⛔ 3 类缺陷是从实测归纳（③ 类，⛔ 但作者如实标了 "According to our observation"） | ⭐ **① 12 · ② 6 · ③ 1**（见 [../../provenance/](../../provenance/)） |

⭐⭐⭐ **两条可直接搬的做法**：

1. ⭐⭐ **「闭合词表 ＋ LLM 自动选」这个组合有了 ICSE 主会的先例。** ⭐ 这回答了 [DEEPREAD_BRIEF.md](#) 里那个问题（⭐ 逐字："我们自己是「闭合 19 条 + LLM 自动选」，⛔ 想知道这个组合有多少先例"）—— ⭐⭐ **本篇是一个，⭐ 且词表只有 5 个符号。** ⭐ 它的做法值得注意：⭐ **词表极小 ＋ 组合自由**（⭐ 5 个事件符号但可任意嵌套密码原语），⛔ 而我们是 **词表较大 ＋ 组合受限**（⭐ 19 条谓词，每条需求选一条）。
2. ⭐⭐⭐ **缺陷类型学不该只用来事后归因，⭐ 应该用来路由到不同机制。** ⭐ 它的 3 类是「幻觉 / NL 歧义 / 视角错位」，⭐ 而**分派原则非常清楚**：⛔ **NL 本身的歧义（Ambiguity）交给确定性检测 ＋ 人，⛔ 因为 LLM 补不出文档里没有的信息**；⭐ 而**格式/视角类错误（Unreadability）交给 LLM ＋ worked example，⭐ 因为那是机械改写**。⭐⭐ **这条分派原则我们可以直接搬到多报的五类上。**

### B6 · 模型

| 项 | 值 |
| :-- | :-- |
| ⭐ **模型集** | ⭐ **GPT-3.5-turbo · GPT-4 · GPT-4o · Google Gemini-pro**（M，§VII 逐字 "The LLMs we used to conduct experiments include GPT-3.5-turbo, GPT-4, GPT-4o and Google Gemini-pro"） |
| ⭐ 主结果用哪个 | ⭐ **GPT-4**（M，⭐ Fig. 7 图注 "Parsing results for 8 protocols with **GPT-4 model**"；⭐ Table III 标题 "Parsing results with **GPT-4 model**"） |
| ⭐ **有无多模型对照** | ⭐⭐ **有（⭐ 三处）** | ⭐ ① 解析：逐字 "advanced LLMs are less likely to construct incorrect terms […] Among them, **GPT-4 performs the best, with an average EC of 56.36% and an average BER of 80.47%** across all cases"；⭐ ② 修复：逐字 "the effectiveness of repairing **relies on advanced LLMs**"（⛔ 逐模型数字在 [1]）；⭐ ③ Fig. 8 的 few-shot baseline 四模型并列 |
| ⭐ 温度 | ⭐ **0.4** |
| ⭐ 工具版本 | ⭐ **Tamarin prover 1.8.0**（M，逐字 "All of the generated symbolic models run on a Tamarin prover in **version 1.8.0**, which includes a SAPIC⁺ platform"）· ⭐ Lark parser（⛔ 未 pin 版本） |

⚠️⚠️ **代际折扣要打，⛔ 但打法要分清**：⭐ 主结果来自 **GPT-4（2023–2024 代）**，⛔ 故「10/18」这个绝对成绩参考价值有限。⭐⭐ **但两条结论不受代际影响**：⭐ ① **"LLM 直接生成符号模型不行"这一条本身**在 4 个模型上都成立（⭐ 含当时最强的 GPT-4o）；⭐ ② **"LLM 自评修复只降 14.74%"** —— ⚠️ ⛔ 这一条**会**受代际影响（⛔ 更强的模型自评可能更好），⛔ 引用时必须带模型限定。⭐ 作者自己把这列为外部效度威胁（M，§VIII 逐字）："A key threat to external validity is **our reliance on GPT-4**. […] the reproducibility of our results depends on an advanced closed-source LLM (GPT-4), which may undergo updates over time."

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 段 |
| :-- | :-- | :-- |
| ⭐ 文档分块 | ⭐ `Segment(nl)` —— ⚠️ ⛔ **评测里是人工分的**（M，逐字 "**we manually segment** each document into a list of chunks"）；⭐ chunk 大小与上下文长度 $N$ 是可配参数 | S1 |
| ⭐⭐ **Lark parser ＋ 未绑定变量分析** | ⭐ 逐字 "The function **Analysis** (Line 5) is implemented using the **Lark parser [32]**. Given a BNF syntax, the abstract syntax tree (AST) of the specification can be readily obtained and analyzed." ⭐⭐ **这是循环的裁决者** | S2 |
| ⭐ MSC 渲染 | ⭐ `Graphviz(P)` → 消息序列图，⭐ 给人做修复决策用 | S2 |
| ⭐⭐⭐ **重写规则 $T$（T1–T8）** | ⭐ λ → SAPIC⁺ 的 8 条递归重写规则（⭐ Fig. 5 全给出）。⭐⭐ **证明 sound**：Lemma 1，$\mathcal{P} \models \phi \Rightarrow \Lambda \models \phi$，⭐ 靠 $\mathrm{traces}(\Lambda) \subseteq \mathrm{traces}(\mathcal{P})$ | S3 |
| ⭐⭐ **SAPIC⁺ 编译器** | ⭐ SAPIC⁺ → Tamarin MSR / ProVerif / DeepSec。⭐ **soundness 引自 [12]**：Theorem 1，$\mathcal{P} \models \phi \Leftrightarrow [\![\mathcal{P}]\!] \models [\![\phi]\!]$ | S4 |
| ⭐⭐ **Tamarin / ProVerif / DeepSec** | ⭐⭐ **真 sound oracle** —— ⛔ **但只在评测端**（见 [B4](#--tamarin-在哪里--只在评测端不在循环里）) | 评测 |
| ⭐ 类型系统 | ⭐ supersort `msg` ＋ subsort `agent` / `nonce`（⭐ 出处 [24]） | S1–S3 |

⭐⭐⭐ **这一格的核心发现**：⭐ **它的"可信底座"不是一个检查器，⭐ 而是一条 soundness 证明链** —— ⭐ Lemma 1 → Theorem 1 → Corollary 1，⭐ 把 λ-DSL、SAPIC⁺、Tamarin 三层用 trace inclusion 串起来。⭐⭐ **即：它不靠"每次都检查"，⭐ 而靠"变换一次证明、永久有效"。** ⭐ 论文自己把这个设计哲学写清了（M，§VIII 逐字）：

> "At a high-level, we aim to achieve a goal that is similar to that of **correct-by-construction model synthesis** [43]. The difficulty is however **the lack of a formal-enough requirement to start with**, and without such requirement it is difficult to ensure the strict correctness of the overall process (i.e., from natural language to generated model). **That is why we employ LLM to give us some starting point, and then employ an approach similar to that of correct-by-construction model synthesis (i.e., the subsequent transformation).**"

⚠️⚠️ ⛔ **但这条链有一个缺口**：⭐ S3 的 top specification 是 **LLM 生成的**（见 [B1](#b1--流水线阶段-按论文-fig-3-的-s1s4--algorithm-12-展开)），⛔ **而 Lemma 1 只覆盖重写规则 $T$，不覆盖 $\mathcal{P}_t$**。⛔ 论文没有讨论这个缺口（⭐ 本卡的一条独立观察，S/I）。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐⭐ **有两条（⛔ 都是自建）**：⭐ ① **few-shot 直接生成**：`0-shot / 1-shot / 2-shots / 3-shots` × 4 模型（⭐ Fig. 8）—— ⛔ **最好 ≤ 4/18**；⭐ ② **correct-by-construction 方法 [8]**（⭐ Alice&Bob 记号输入 → Tamarin），⭐ 4 个协议案例，⛔ 结论是**等价**而非胜出。⛔ **无逐阶段消融** |
| `dataset` | ⭐⭐ **两套（⛔ 别混）**：<br>⭐ **① 解析评测：9 个协议**（⭐ Table II 逐字给了来源与体量）：`NSPK`(210, Online Teaching Assignment) · `Toy`(226, Tamarin 练习) · `NSSK`(392, **Wikipedia**) · `NAXOS`(234, Tamarin Manual p36) · `Otway-Rees`(351, GIAC Certification Paper) · `SSH`(991, **RFC 4253** §7.2/§8) · `IKEv2`(379, **ACSAC'21** §3 p3) · `KEMTLS`(659, **CCS'20** §3) · `EDHOC`(1029, **draft-ietf-lake-edhoc-02** p20)<br>⭐⭐ **② 整体评测 benchmark：18 个协议**（⭐ 逐字 "the **first** new benchmark for such non-trivial automatic symbolic modeling task"）：`example` `Toy` `NSPK` `NSSK` `SigFox` `LAKE` `NAXOS` `X509.1` `SSH` `EDHOC` `KEMTLS` `Yahalom` `Kao Chow` `SPLICE/AS` `Otway Rees` `Woo and Lam` `Denning-Sacco` `Stubblebine`。⭐ 输入 **51–639 token**，⭐ SAPIC⁺ 30–163 LoC / Tamarin 44–722 LoC，⭐ 性质数 2–10 |
| ⭐⭐ **分母怎么定的（⭐ benchmark 构造）** | ⭐ **三步，逐字（M，§VII-C）**：⭐ ① "We start from $\mathcal{R}_i$ which has been available at **Tamarin GitHub repository**"（⭐ 从已有的人写 Tamarin 模型出发）；⭐ ② "To get their corresponding $N_i$, we **read these protocols' original documents e.g., RFCs, extract and reform the core parts** corresponding to the model"（⭐ 反向从模型去找 NL）；⭐ ③ "For the given model $\mathcal{R}_i$, there are a set of safety properties $\Phi$ which have been verified on $\mathcal{R}_i$. **We manually build SAPIC⁺ model $\mathcal{P}_i$**, ensuring that $\mathcal{P}_i \approx_\phi \mathcal{R}_i$"。⭐⭐ **注意方向：⛔ 不是从 NL 找模型，⭐ 而是从模型倒推 NL** —— ⚠️ **这使 NL 天然"够用"，⛔ 属乐观偏置** |
| ⭐ 明确排除了什么 | ⭐ 逐字 "we focus on protocol cases of **manageable scale, excluding extremely large-scale protocols like TLS 1.3 and 5G AKA**"（⭐ 而 Table I 恰好说这两个是最贵的：TLS 1.3 = 143 页文档 → 2000+ LoC；5G AKA = 722 页 → 7 模型 4000+ LoC）。⭐ 排除标准与结果无关，⭐ 判据是规模，⛔ 不是难度 |
| `metrics` | ⭐ **解析侧三指标（⭐ 定义逐字）**：⭐ **EC**（Exact Coverage）$= n_g / N$ · **BER**（Bounded expressions rate）$= n_b / N$ · **ER**（Error Rate）$= 1 - EC$，⭐ 其中 $N$ ＝ 生成表达式总数、$n_g$ ＝ 落在 ground truth 内的数、$n_b$ ＝ 无未绑定变量的数。⭐ 误差再分两型：`#1` ground truth 之外的多余表达式 · `#2` ground truth 里被表达错的。⭐⭐ **另有一个自造派生量 $\delta_e = EC/BER$**，⭐ 逐字 "reflects the degree of abstraction in natural language descriptions relative to symbolic models […] **the greater the value of $\delta_e$ is, the more specific the natural language descriptions are indicated**"<br>⭐ **整体侧**：`Success Ratio` = `n/5` · LoC_S / LoC_M · 性质数 · Tamarin 耗时 |
| ⭐⭐ **有无 `@k` 口径** | ⭐⭐ **有，且是本轨少见的** —— ⭐ 逐字 "we set the **run iterations as 5** for each protocol case"，⭐ Table IV 的 `Success Ratio` 列逐案例给 `5/5 · 4/5 · 3/5 · 2/5 · 1/5 · 0/5`。⭐⭐ **这实质是 `hit@k`（⛔ 论文没这么命名，⛔ 也没报 `hit@1` 均值或方差）** |
| ⭐ `judged_by` | ⭐⭐ **自动判定 ＋ 作者手工构造 ground truth**：⭐ 判定是自动的（⭐ Def 7 语义等价：`✓` iff 生成模型能通过参考模型上全部性质 —— ⭐ 逐字 "Similar to program testing where a program is considered correct if it can pass all test cases, we take the property $\phi$ as the test case here"）。⛔ **但 ground truth 全由作者手工构造**（⭐ 逐字 "if a corresponding SAPIC⁺ model $\mathcal{P}$ is not available in [18], **we manually construct it**. We then **provide lambda expressions as the ground truth**"）。⛔ **无第三方、⛔ 无标注者间一致性、⛔ 无 $\kappa$**<br>⚠️⚠️ **自证风险要写明**：⭐ **λ-DSL 是作者设计的、λ ground truth 是作者写的、prompt 是作者写的、判据（Def 7 语义等价）也是作者定的** —— ⭐ 且作者自己承认 Def 7 是 "an **approximate and non-strict** equivalence relation"。⛔ 这不影响「分阶段 > 直接生成」这个**相对**结论（⭐ 两臂同判据），⛔ 但会影响 `EC/BER` 这类**绝对**数字 |
| `human_baseline` | ⛔ **无**。⭐ 只有一处**人写模型的规模对照**（⭐ 不是质量对照，M 逐字）："the ratio of code size (lines of code) in the generated model to that in reference human-created model roughly **ranges from 1.3 to 5.4**" |
| `runs` | ⭐ **每案例 5 次**；⭐ 报 `Success Ratio = n/5`，⛔ **不报均值、⛔ 不报方差**。⭐ 解析评测（Table III）⛔ 未说跑几次（⭐ 疑似单次，S） |
| ⭐⭐ `adverse_results` | ⭐⭐⭐ **本卡最值得学的一格。⭐ 三层处理，⛔ 第三层有争议。**<br>⭐ **① 如实全列**：⭐ Table IV 逐案例列出，⛔ **8/18 是 `✗ 0/5`**（`NAXOS` `SSH` `EDHOC` `KEMTLS` `SPLICE/AS` `Stubblebine` 等）；⭐ 解析评测同样如实（⭐ 逐字 "**every parsing results contain errors** and the exact coverage ranges from **9.09%** (case Toy) to 87.56% (case EDHOC)"）<br>⭐ **② 定位根因并归给数据而非方法**：⭐ #Finding 2 逐字 "for those complex protocols, **a singular protocol document is not always self-contained enough to derive a symbolic model from it**"，⭐ 并给了 KEMTLS 的**具体例子**（⭐ `transcript` 变量未绑定，⭐ 逐字 "[35] does not provide further description for variable transcript, which confuses LLM to make a correct modeling choice"）<br>⭐⭐ **③ 把失败重新解释成可靠性证据（⚠️ 有争议）**：⭐ 逐字 "It is not surprising that some cases failed. As discussed in our two findings […] **these failed cases demonstrate the reliability of our approach: it aims to avoid generating seemingly correct but misleading results from a document that lacks sufficient information.**"<br>⚠️ **这一层要分开评**：⭐ **它不是纯粹的话术** —— ⭐ 因为它有**机制支撑**（⭐ `Analysis` 的未绑定变量检测能把"文档不够"这件事**定位到具体变量**），⭐ 且 $\delta_e$ 指标就是为量化这件事造的。⛔ **但它仍然是把"没做到"改述成"选择不做"**，⛔ 而论文**没有区分**「因文档不足而拒绝」与「因方法不足而失败」的两类 `0/5`。⭐⭐ **对我们的启示见 [E.1.3](#e-对-m1-的意义)** |
| ⭐ 其它自陈限制 | ⭐ 逐字：⭐ ① 内部效度 —— "The protocol cases used in this work primarily involve **classic symmetric and asymmetric cryptographic primitives, which are well-understood by LLMs**"；⭐ ② 外部效度 —— 依赖 GPT-4；⭐ ③ 局限 —— "the gap between evaluation cases and real-world large scale protocols like TLS 1.3" ＋ "**we only cover a core subset of** [SAPIC⁺] **features**"；⭐ ④ 模型膨胀 1.3–5.4× |

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ **🟢** | [ieeexplore.ieee.org/document/11029741](https://ieeexplore.ieee.org/document/11029741/) · ⭐ **本地** [`baselines/llm-aided-security-protocol-verification/paper.pdf`](../../../../baselines/llm-aided-security-protocol-verification/paper.pdf) | ⭐ 本地 PDF **999,407 B** · `paper_content.txt` **75,491 B**（⭐ 12 页，⭐ 提取质量正常）。⚠️ ⛔ IEEE 页面本身需订阅（⭐ 本地副本水印逐字 "Authorized licensed use limited to: **BEIHANG UNIVERSITY**. Downloaded on **June 07, 2026**"），⛔ **故对外部读者是 🟡 而非 🟢** |
| ⭐⭐ **实验代码 ＋ benchmark ＋ prompt ＋ 扩展版** | ⭐ **🟢** | [github.com/zerrymore/AutoSM](https://github.com/zerrymore/AutoSM) | ⭐ [`tools/verify_assets`](../tools/verify_assets.py) 输出**逐字**：`HEAD c0fd24320c · 文件 2136（非文档 2098 · ⭐ 源码 1505） · release 0 · license GPL-3.0` → ⭐ 机械建议 **🟢**。⭐⭐ **人工终裁维持 🟢**：⭐ 1505 个源码文件、⭐ 有 license（GPL-3.0）；⛔ 但 **release 0** —— ⛔ **无冻结版本、无 tag** |
| ⭐ **数据集 / Benchmark** | ⭐ **🟢** | 同上 | ⭐ 论文声明逐字（三处）："Our **benchmark, tool implementation and all the experiment data** are available at [1]" · "**Our benchmark and tool implementation are released on [1]**" · "All of the baseline models $\mathcal{R}_{anb}$ are also included in [1]"。⭐ 条目数 **18 个协议**，⭐ 格式 3-元组 $(N_i, \mathcal{P}_i, \mathcal{R}_i)$ ＝ NL 文档 ＋ SAPIC⁺ 规约 ＋ Tamarin 模型 —— ⭐⭐ **有 ground truth**（⭐ 且带每个模型上已验证的性质集 $\Phi$）。⚠️ ⛔ **未逐目录核对条目数是否真为 18**（见 [F.4](#f-存疑与未核项)） |
| ⭐ **实验结果细则** | ⭐ **🟢**（⭐ 声明层面） | 同上 | ⭐⭐ **论文把三样东西明确推给仓库**：⭐ ① 逐模型的**修复效果**（逐字 "The result (included in [1])"）· ⭐ ② Lemma 1 的**完整证明**（逐字 "The detailed proof of Lemma 1 is included in our extended paper version in [1]"）· ⭐ ③ 操作语义**完整规则表**（逐字 "The comprehensive elaboration of the rules is provided in the extended version in [1]"）· ⭐ ④ correct-by-construction **对照数据**（逐字 "According to experiment data in [1]"）。⚠️ ⛔ **这四样本轮未逐一在仓库里定位** |
| ⭐ **prompt 是否公开** | ⭐ **🟢**（⭐ 声明层面） | 同上 | ⭐ 逐字 "we design prompts to instruct the LLM in writing lambda expressions, **all of which are provided in [1]**"。⚠️ ⛔ 本轮未在仓库里逐一定位 prompt 文件 |
| Artifact DOI / 复现包 | ⛔ **⚪** | — | ⛔ 无 Zenodo / 4open / OSF DOI；⛔ **无 GitHub release** |

⚠️ ⭐ **与本仓库既有记录对齐**：⭐ [`baselines/SUMMARY.md`](../../../../baselines/SUMMARY.md) 第 270 行已记 `🟢` ＋ 逐字 "论文声明 tool implementation、benchmark、experiment data 和 extended paper version 均公开；本轮 GitHub `git ls-remote` 可访问"。⭐⭐ **本卡把它从"`ls-remote` 可访问"升级为"内容已机械核验"**（⭐ HEAD `c0fd24320c` · 1505 源码文件 · GPL-3.0），⛔ 但**仍未做"内容够不够复现"的人工核对**。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **「分阶段的判据」有了一条可搬的通用原则。** ⭐ 这是本卡最值钱的东西 —— ⭐ 我们的 10 节点流水线**从来没有外部证据说明为什么在这里切**。⭐ 它给的判据是：⭐⭐ **切点落在「上游 LLM 能可靠产出、下游能被确定性算法 sound 变换、且这一层人能校验」的位置**（⭐ 三条逐字见 [必答②](#-必答--分成几个阶段分阶段的判据是什么)）。⭐ **具体可搬的动作**：⭐ 逐个审我们的 10 个节点，⭐ 问三句 —— ⭐ ① 这一节的输出是 LLM 能可靠产出的形态吗？⭐ ② 下一节对它的处理是确定性且可论证正确的吗？⭐ ③ 这一层的中间产物人能直接读懂并纠错吗？⛔ **三问有一个答不上，切点就该挪。**
2. ⭐⭐⭐ **「LLM 只抽要素，形式变换交给可证 sound 的算法」这条分工可以直接对照我们的 5 个 LLM 节点。** ⭐ 按它的口径：⭐ `split_requirements`（NL → 原子需求）✅ 属于"抽要素"；⛔ `convert_assertions`（需求 → 断言脚本）⚠️ **是形式化变换，⭐ 按它的原则本该尽量确定性化**；⛔ `adjudicate_results`（求值结果 → 是不是发现）⚠️ **同理**。⭐⭐ **这给 M1 提供了一条明确的减法方向：把 LLM 从形式变换环节往"抽要素"环节收缩。**
3. ⭐⭐⭐ **「LLM 自评修复只降 14.74%，因此把人拉回环里」是一条可引用的外部实测。** ⭐ 它在方向上独立印证我们「两个 LLM 自评 reviewer 零收益」，⭐ 且给了一个量级上界。⭐ **更可搬的是它的结论动作**：⛔ 它没有加轮数、没有换 prompt，⭐ 而是**改变了分工** —— ⭐ 把 LLM 自评保留为单次廉价过滤（⭐ 不迭代），⭐ 把真正的判定权交给确定性 parser，⭐ 把修复权交给人。
4. ⭐⭐⭐ **缺陷类型学要驱动机制路由，⛔ 不只做事后归因。** ⭐ 它的 3 类缺陷各挂一个专门机制，⭐ 分派原则是：⛔ **NL 本身信息不足（Ambiguity）→ 确定性检测 ＋ 人**（⭐ 因为 LLM 补不出文档里没有的东西）；⭐ **机械改写类（Unreadability）→ LLM ＋ worked example**；⛔ **幻觉类（Inconsistency）→ LLM 自评（⭐ 而这一路正是收益最低的那条）**。⭐⭐ **我们的五类多报分类目前只用于归因 —— 这一格可以升级成路由表。**
5. ⭐⭐ **「与确定性方法比等价，而不是比更好」这个论证形状可以搬。** ⭐ §VII-D 拿一个 correct-by-construction 方法做**交叉验证**（⭐ 输入端不同、输出性质等价），⛔ 而不是宣称胜出。⭐⭐ **对我们直接有用**：⭐ 我们的 `hit@1` 主臂 **60.4%** vs 朴素基线 **76.2%**（⛔ Δ = −15.82pp）—— ⭐ 这个形状下"我们更好"讲不通，⭐ **但"我们与朴素基线在某个子集上等价、而我们额外产出了可机械求值的断言与逐位证据"是可以讲的**，⭐ 且有 ICSE 主会的先例。
6. ⭐⭐ **`Success Ratio = n/5` 逐案例列出**，⭐ 而不是只报聚合成功率 —— ⭐ 这与我们 §3.5.2 的 `metric@k` 纪律同向，⭐ 是一个可引的先例（⛔ 尽管它没给 `@1` 均值与方差）。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔ **benchmark 是从模型倒推 NL 造的，⭐ 这是乐观偏置。** ⭐ 逐字流程是「先拿 Tamarin GitHub 上的人写模型 → 再回文档里 extract and reform 出对应的核心部分」—— ⭐⭐ **即 NL 输入是"为这个模型挑出来的"，⛔ 不是"工程师手上真实拿到的那份文档"。** ⚠️ ⛔ **我们的 60 个 pair 反过来是从 NL 生成模型，⭐ 方向是对的，⛔ 但要警惕同类偏置在台账构造上重演**（⭐ 尤其 G1 全量重标时：⛔ **不要因为"这条缺陷好判"而反向调整 NL 或期望**）。
2. ⛔⛔ **失败被重新解释成"可靠性"，⛔ 而没有区分两类 `0/5`。** ⭐ 它有机制支撑（⭐ 未绑定变量检测能定位到具体变量），⛔ **但论文没有把 8 个 `0/5` 逐个归类成「文档不足」还是「方法不足」**。⭐⭐ **我们不能照搬这个动作**：⭐ 若我们要说"某条缺陷未命中是因为台账/NL 的问题而非方法的问题"，⛔ **必须逐条给出定位证据**（⭐ 就像它给了 `transcript` 那个例子），⛔ 不能整体归因。⚠️ ⭐ 这与我们「15/19 谓词使用率归因未定」是同一类风险。
3. ⛔ **soundness 链有一个未被覆盖的缺口。** ⭐ S3 的 top specification 是 LLM 生成的，⛔ 而 Lemma 1 只证重写规则 $T$。⭐⭐ **教训：⛔ 别让"整条链都证过了"这句话盖住链上仍有 LLM 的那一节。** ⭐ 我们自己也有同形风险：⛔ pyfcstm 求值是确定性的，⛔ 但**断言脚本本身是 LLM 产出的** —— ⛔ 求值可信 ≠ 断言问对。
4. ⛔ **主结果依赖 GPT-4（2023–2024 代）**，⛔ 且作者自陈为外部效度威胁。⭐ 引用 `10/18` 与 `14.74%` 时必须带模型限定。
5. ⛔ **无逐阶段消融。** ⭐ Fig. 8 证的是"分阶段 vs 完全不分阶段"，⛔ **不能用来支持"分成四段比分成两段好"**，⛔ 更不能用来支持我们的 10 节点。⚠️ ⭐ **我们自己若要主张 10 节点的必要性，仍然缺消融** —— ⛔ 这篇给不了。
6. ⛔ **人工分块是隐藏的人工成本。** ⭐ 逐字 "we **manually** segment each document into a list of chunks" —— ⛔ 而 `Segment(nl)` 在 Algorithm 1 里写成一个函数，⛔ 读起来像是自动的。⭐ **我们报成本时要避免这类隐藏项。**

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⭐⭐⭐ **它的下游有一条现成的、已证 sound 的确定性变换链；⛔ 我们没有。** ⭐ 它能把 LLM 收缩到"抽要素"，⭐ 前提是 λ → SAPIC⁺ → Tamarin 这两跳**本来就存在且可证**（⭐ 第二跳直接引 [12] 的定理）。⛔⛔ **而我们从「NL 需求」到「可机械求值的断言脚本」之间没有这样一条链** —— ⛔ 那一跳目前只能由 LLM 做（`convert_assertions`）。⭐⭐ **所以"把 LLM 收缩到抽要素"这条原则我们只能部分照搬；⭐ 要完全照搬，⭐ 得先造出那条确定性链（⭐ 例如：把需求→断言做成模板实例化而非自由翻译）。** ⭐ 这是 M1 一个具体可评估的方向。
2. ⭐ **任务方向不同**：⭐ 它是**生成**（NL → 形式模型），⭐ 我们是**缺陷检测**（模型 vs NL）。⭐ 它可以反复改产物直到通过；⛔ 我们不能改被测模型。
3. ⭐ **它的 sound oracle 在评测端而不在循环端** —— ⭐ 与我们把 pyfcstm 放在**求值端**其实更接近（⭐ 都不是裁决端）。⭐⭐ **而 [ERTS 那篇](./erts2026-safe-llm-mde.md) 把 oracle 放进裁决端、结果不收敛。⭐ 三家合起来的图景是：⛔ oracle 放哪一端不是关键，⭐ 关键是它的输出能不能变成可执行的反馈。**
4. ⭐ **边界差得远**：⛔ 进程代数 ＋ 无界并发 ＋ Dolev-Yao 攻击者，⛔ 无显式状态集。⛔ **它的任何数字都不能当我们的可比数字**（⭐ 按 [README.md](../README.md) §3 防火墙，⭐ L3 产物本来也不进论文）。
5. ⭐ **词表规模与选法都不同**：⭐ 它 **5 个事件符号 ＋ 自由嵌套**，⭐ 我们 **19 条谓词 ＋ 每需求选一**。⚠️ ⭐ 值得一想：⭐⭐ **我们 15/19 的使用率问题，⭐ 会不会部分是"词表太大、每条只能选一"造成的？** ⛔ 这篇给不出答案，⭐ 但它的反例（⭐ 5 个符号却能表达全部协议语义）提示**小词表 ＋ 组合**可能是另一个设计点。

---

## F. 存疑与未核项

1. ⚠️⚠️ **"AutoSM" 不是论文标题的一部分** —— ⭐ 正式题名是 "LLM-aided Automatic Modeling for Security Protocol Verification"，⭐ `AutoSM` 只出现在参考文献 [1] 的仓库 URL 里（⭐ `github.com/zerrymore/AutoSM`）。⭐ 已试入口：⭐ 全文 grep `AutoSM` → ⛔ **正文零命中，只命中参考文献 [1] 的 URL**；⭐ Crossref / IEEE 题录 → ⛔ 无 "AutoSM"。⭐⭐ **本卡 `id` 沿用任务书给的 `icse2025-autosm`，⛔ 但引用时必须用正式题名。**
2. ⚠️⚠️ **Fig. 8 的逐模型逐档数字未取到** —— ⭐ 那是一张柱状图，⭐ `paper_content.txt` 只保留了轴标签（`0-shot 1-shot 2-shots 3-shots ours` / `0 2 4 6 8 10` / 四个模型名）。⛔ **正文只给了 "3-shot learning generates a maximum of 4 cases" 这一个数。** ⭐ 已试：⛔ 文本提取（图内数值不可得）· ⛔ 未回 `paper.pdf` 目视读图。⭐⭐ **可补动作：⭐ 回 PDF 第 10 页目视 Fig. 8，⭐ 读出 20 个柱子的高度。** ⛔ 在此之前**不得引用任何逐模型逐档数字**。
3. ⚠️⚠️ **`14.74%` 的逐模型分解在仓库里，⛔ 本轮未取** —— ⭐ 逐字 "The result (**included in [1]**)"。⭐ 已试：⛔ 全文（只有这一个平均数）。⭐ **可补动作**：去 `github.com/zerrymore/AutoSM` 找修复评测的结果文件。
4. ⚠️ **仓库内容未做"够不够复现"的人工核对** —— ⭐ 机械核验已过（`HEAD c0fd24320c` · 2136 文件 · 1505 源码 · GPL-3.0 · release 0），⛔ 但**未逐一确认**：⭐ ① benchmark 是否真有 18 个协议的完整 3-元组；⭐ ② prompt 文件在哪；⭐ ③ extended paper version（含 Lemma 1 证明）在哪；⭐ ④ correct-by-construction 对照数据在哪。⚠️ ⛔ **按 [tools/verify_assets](../tools/verify_assets.py) 自己的警告，⭐ 机械 🟢 不等于人判 🟢。**
5. ⚠️ **解析评测跑了几次未说** —— ⭐ Table III / Fig. 7 未声明运行次数（⭐ 整体评测明确是 5 次）。⛔ 疑似单次（S），⛔ 但原文未提供。
6. ⚠️ **被检查的语法规则总数与 well-formedness 的实现范围** —— ⭐ Def 5 有 3 条，⛔ 但 `Analysis` 只查第 ① 条（未绑定变量）。⛔ 第 ② ③ 条（消息可读性、执行者是合法角色）由谁查、什么时候查，⛔ 原文未明说（⭐ `View` 处理 ② 的一部分，⭐ 但那是 LLM 改写不是检查）。
7. ⚠️ **top specification 的 LLM 生成不在 soundness 覆盖内** —— ⭐ 这是本卡的一条**推断（S/I）**，⛔ 论文既没承认也没否认。⛔ 不得写成"论文有此缺陷"的事实句。
8. ⚠️ **Table II 与 Table IV 的协议集合不完全一致** —— ⭐ Table II（解析评测，9 个）里的 `NAXOS` `Otway-Rees` `SSH` `IKEv2` `EDHOC` `KEMTLS` `NSPK` `NSSK` `Toy`；⭐ Table IV（整体评测，18 个）少了 `IKEv2`、多了 `example` `SigFox` `LAKE` `X509.1` `Yahalom` `Kao Chow` `SPLICE/AS` `Woo and Lam` `Denning-Sacco` `Stubblebine`。⛔ **`IKEv2` 为什么进了解析评测却没进 benchmark，原文未说明。**
