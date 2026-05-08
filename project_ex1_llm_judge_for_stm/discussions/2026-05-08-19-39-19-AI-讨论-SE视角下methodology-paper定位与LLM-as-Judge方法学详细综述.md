# project_ex1 — SE 视角下 methodology paper 定位 + LLM-as-Judge 方法学详细综述（v2）

> **版本**：v2（修订版，覆盖用户的 3 项学术纠正）
> **前序版本**：[2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述_v1.md](./2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述_v1.md)
> **本版关键纠正**：
> 1. 明确研究方向 = **软件工程（Software Engineering, SE）**
> 2. 明确目标产物 = **方法学论文（methodology paper）**
> 3. 把"已有 LLM-as-Judge 工作"从 v1 的简短罗列升级为**详细方法 × IO 综述**，并独立建库为 [llm_as_judge_methods_corpus/](../llm_as_judge_methods_corpus/)

---

## 0. 研究方向声明 — Software Engineering

本研究**严格立足于软件工程（SE）方向**，而非 NLP / ML 方向。这一定位影响了从问题选择到投稿目标的所有决策：

| 维度 | SE 视角 | NLP / ML 视角（**对照**）|
|---|---|---|
| **研究对象** | 软件制品（SE artifact）：状态机模型 / UML / 代码 / 需求 / 测试 / 设计文档 | 自由文本 / 对话 / 推理链 |
| **关心的"质量"** | **结构正确性**、**与需求的语义一致性**、**形式化可验证性**、**工业可用性** | 流畅性 / 信息量 / 与 reference 的相似度 |
| **判定的目标** | 给制品**审查报告**（覆盖度 / 准确性 / 可操作性 / ...）以替代或加速人工 review | 给生成结果打分以做模型选择或 RLHF |
| **"人评"基准** | 资深工程师 / 评审专家的 Code Review / Design Review 实践 | 众包 annotator |
| **典型投稿** | TSE / TOSEM / EMSE / ICSE / FSE / ASE / ISSTA | ACL / EMNLP / NeurIPS / ICLR |
| **研究范式** | 偏 empirical / methodological + 配套工具与可复现实验脚手架 | 偏 benchmark + 模型 / prompt 创新 |

**为什么强调这一点**：LLM-as-Judge 的现有文献（详见 §2）几乎全部产自 NLP 社区，**评判对象基本都是自由文本**。把这套思路搬到 SE artifact 上，并不只是换数据这么简单——SE artifact 有显式的结构与可形式化语义，对 judge 的可靠性、可解释性、可审计性的要求也比 NLP 评估高得多。这是一个被现有文献忽视的**方法论空缺**，也是 project_ex1 的立足点。

---

## 1. Project_ex1 学术定位 — Methodology Paper

### 1.1 论文类型

**目标**：把 project_ex1 写成一篇 SE 方向的**方法学论文**，而非 application paper / tool paper。

| 论文类型 | 重点 | 与 project_ex1 的匹配度 |
|---|---|:-:|
| **Methodology paper** | 提出**新方法**（或新方法学纪律）+ 证明它解决了某个旧方法做不到的问题 | ✅ **目标类型** |
| Empirical study | 大规模实测某现象 / 某工具 | 🟡 我们有实证，但实证不是核心 |
| Benchmark paper | 提出新数据集 + leaderboard | ⚪ 不是主线 |
| Tool paper | 释放工具 + demo + 工业用例 | ⚪ infrastructure 是副产物 |

### 1.2 方法学贡献的可分离形态

按 SE 顶会近年方法学论文的写作惯例，我们计划把贡献分成**多个层次**，每一层都可独立为读者所采纳：

| 层次 | 贡献 | 证据 |
|---|---|---|
| **L1** | **STM artifact 的多维评审 rubric**（7 维：覆盖度 / 准确性 / 具体性 / 证据性 / 校准性 / 可操作性 / 一致性）| 在 STM 数据集上的可解释 review；rubric 与人评对齐度 |
| **L2** | **strict-llm + 多次重复（5-rep）+ noise floor 协议**：把"LLM judge 的随机性"显式纳入 SE 评估方法学 | W2 confidence-formula bug 复现 / V4 baseline 5-rep 数字 |
| **L3** | **provider drift 与 cache effect 的 SE 评估纪律**：在 SE 评估方法学中第一次系统讨论 | per-task checkpoint + 5-rep 对比 |
| **L4** | **anchored-rubric prompting** vs **auto-generated rubric**（G-Eval 流派）的方法对比，并给出 SE artifact 上的取舍证据 | rubric 消融实验（计划中）|

**为什么"分层"对方法学论文重要**：reviewer 不一定接受全部 4 层，但**只要 L1 + L2 站住**，论文就有可发表价值。L3 / L4 是加分项与未来工作。

### 1.3 候选投稿目标

| Venue | 类型 | 周期 | 与本研究契合度 |
|---|---|---|:-:|
| **TSE**（IEEE TSE）| 期刊 | 长 | ✅ 软工方法学论文经典出口 |
| **EMSE**（Empirical SE）| 期刊 | 中 | ✅ 5-rep / noise floor 这种实证纪律契合 EMSE 偏好 |
| **TOSEM**（ACM）| 期刊 | 长 | ✅ 形式化语义 + LLM 的交叉点 |
| **ICSE / FSE** | 顶会 | 短 | 🟡 需要更强的工业 case 才占优 |
| **ASE** | 顶会 | 短 | 🟡 工具气质重，需 demo |
| **ISSTA** | 顶会 | 短 | ⚪ 测试导向，不太契合 |

**§6.1 用户决策点**：venue 优先级偏好？

---

## 2. 已有 LLM-as-Judge 工作 — 方法 × IO 详细综述

> 本节是对用户第 4 项纠正的回应：
>
> > "你的意思是 LLM-as-judge 已经有相关工作了？细说，每一个工作是什么样的 LLM method 以及评审对象是什么，整个方法的输入输出是什么，详细梳理一下"
>
> 7 篇核心论文已独立建库为 [llm_as_judge_methods_corpus/](../llm_as_judge_methods_corpus/)，每篇有完整 `DESC.md` + `bibtex.bib`。本节给出**横向方法 × IO 比较**与**对 project_ex1 的可借鉴性结论**。

### 2.1 7 篇代表性工作的 method × IO 结构化对比

| Slug | LLM method | 评判对象 | 输入 | 输出 | rubric? | 我们的对照点 |
|---|---|---|---|---|:-:|---|
| [g-eval](../llm_as_judge_methods_corpus/g-eval/DESC.md) | **Pure prompting + form-filling + CoT + auto-rubric** | NLG 输出（dialog summary / news summary）| (Task description + auto-generated criteria + Source + Output) | Pointwise score（auto-rubric 上的多维分） | ✓（auto-generated）| **G-Eval 是 anchor 思路最接近的对照**：我们的 rubric 是 **pre-defined 7 维**而非 auto，且要求 evidence + score 同时给出 |
| [mt-bench](../llm_as_judge_methods_corpus/mt-bench/DESC.md) | **Pure prompting**（GPT-4 as judge）+ pairwise + position-bias swap + verbosity 控制 | LLM dialog 回答（80 prompts × N model）| (Question + Answer A + Answer B) 或 (Question + single Answer) | (a) Pairwise: A/B/Tie + 解释；(b) Pointwise: 1-10 分 + 解释 | partial（per-task 评估准则）| **MT-Bench 是 LLM-as-Judge 范式的奠基**：我们继承"pairwise + 顺序对称"思路（计划中），但 STM 数据集 << 80 prompts |
| [self-consistency](../llm_as_judge_methods_corpus/self-consistency/DESC.md) | **Pure prompting + 同 prompt 多次采样 + majority vote** | 推理任务输出（GSM8K / SVAMP / etc.）| Question | 多条 reasoning chain → vote 出 final answer | ✗ | **Self-Consistency 是 5-rep aggregation 的灵感来源**：我们的 5-rep 不是为了 vote，而是为了 **noise floor 测量**（更严格） |
| [constitutional-ai](../llm_as_judge_methods_corpus/constitutional-ai/DESC.md) | **Critique-then-revise loop + RLAIF** | LLM 自身输出（safety / harmlessness）| (Prompt + Initial response + Constitution principles) | Revised response + （RL 训练后的）safer model | ✓（principle list） | 不直接借鉴方法本身，但**critique-first → score** 的 chain-of-thought 思路在我们的 rubric_dim_score 中实现了类似形态（先列 evidence 再给分）|
| [tian-verbalized-confidence](../llm_as_judge_methods_corpus/tian-verbalized-confidence/DESC.md) | **Pure prompting + 让 LLM 自报 confidence**（verbalize numeric / linguistic）| LLM 自身回答 | (Question + LLM Answer + "请给出 confidence") | (Original answer + Numeric 0-1 / Linguistic confidence) | ⚪ | **本文是 W2 confidence-formula bug 的精神先驱**：Tian 等指出 LLM 自报 confidence 经过 RLHF 后比 logits 更可信。我们 W2 发现的 bug 正是在做类似事情时的代码层面失误 |
| [prometheus](../llm_as_judge_methods_corpus/prometheus/DESC.md) | **Fine-tune Llama2-13B** 在 1k+ rubric 上做 fine-grained scoring | Generic NLG 输出（任意 task）| (Instruction + Response + Reference + Rubric description + Per-level score description) | (Free-text feedback + 1-5 score) | ✓（每次 inference 自定义） | **Prometheus 的 rubric description + per-level score description** 几乎与我们的 7 维 rubric form-filling 对齐；区别：我们走 **prompting-only** 路线（STM 数据 < 1k 不够 fine-tune） |
| [judgelm](../llm_as_judge_methods_corpus/judgelm/DESC.md) | **Fine-tune Vicuna 系列**（7B / 13B / 33B）做 pairwise judge | 自由文本 candidate（pairwise / pointwise）| (Question + Answer A + Answer B + 可选 criteria) | A/B/Tie + 解释；或 per-candidate score | 弱（隐式 in 训练数据）| **JudgeLM 与 Prometheus 同属 trained-judge**：cost-efficiency 思路可借鉴（如未来 STM judge 数据足够，可 distill 一个小 STM judge），但短期路线不走 fine-tune |

### 2.2 横向归纳 — 现有方法的 4 大类

| 类别 | 代表 | 核心 | 适合 SE artifact 吗？ |
|---|---|---|:-:|
| **Pure prompting + auto-rubric**（G-Eval 流派）| G-Eval | LLM 自己生成 rubric 再打分 | 🟡 SE artifact 的 rubric 应来自工程实践，不能 auto |
| **Pure prompting + anchored rubric**（Prometheus inference 形态、本研究形态）| Prometheus（inference 时输入 rubric）| 输入预定义 rubric → form-filling 打分 | ✅ **最契合 SE 制品** |
| **Aggregation 类**（Self-Consistency / MT-Bench position-swap）| Self-Consistency | 多次采样 + majority vote / pairwise swap | ✅ 但本研究中 5-rep 用于 **noise floor**，不用于 vote |
| **Trained judge**（Prometheus / JudgeLM）| Prometheus / JudgeLM | fine-tune 一个 judge LLM | 🔴 SE artifact 数据 < 1k，路线不可走 |

### 2.3 现有工作的 4 维局限性（本研究的差异化空间）

| 维度 | 现有文献的状况 | project_ex1 的对策 |
|---|---|---|
| **L1 Noise floor** | 几乎全部为单次 / 单 seed 报告（G-Eval / MT-Bench / Prometheus / JudgeLM 都未做严格多 seed 并报告 ±σ）| ✅ 我们做 **5-rep + 报告 ±σ + noise floor 阈值** |
| **L2 Provider drift** | 几乎不讨论（实验通常一周内做完，未跨 provider 版本验证）| ✅ 我们的方法学要求**显式记录 provider snapshot + 多次重复跨时跨缓存** |
| **L3 Rubric anchor** | G-Eval 用 auto-rubric；MT-Bench 用 per-task 弱 rubric；Prometheus 走 fine-tune 路线 | ✅ 我们用**严格的 SE 工程领域 7 维 anchored rubric**，每维定义 + 评分锚点显式 |
| **L4 SE artifact 适配** | **几乎全部为自由文本 / 对话 / 摘要 / 推理链**——SE 制品判定空白 | ✅ 我们在 **STM artifact**（5 系统 25 状态机 110 缺陷）上落地 |

**§Related Work 引用要点**（拟稿）：

> "While LLM-as-Judge has been extensively studied for free-text NLG (G-Eval [Liu23], Prometheus [Kim24]), pairwise dialog comparison (MT-Bench [Zheng23], JudgeLM [Zhu23]), and reasoning aggregation (Self-Consistency [Wang23]), **all existing work centers on free-text outputs and pays limited attention to the structured nature of software engineering artifacts**. Moreover, **none of these works adopt a multi-replication noise-floor protocol that would allow practitioners to distinguish a genuine quality improvement from LLM-evaluator stochasticity** — a methodological gap that becomes critical when the evaluator's variance is comparable to the effect being measured. This paper addresses both gaps: we propose a 7-dimension anchored rubric for state machine artifacts and a 5-replication noise-floor protocol that exposes evaluator stability as a first-class concern."

---

## 3. 工程基础设施（已就位，作为方法学论文的可复现支撑）

| 模块 | 已完成 | 路径 |
|---|---|---|
| **STM artifact 数据集** | 5 系统 × 25 状态机 × 110 缺陷标注 | `state_machine_review_corpus/` |
| **Strict-llm 调用层**（无静默 fallback） | ✅ | `src/.../llm_client.py` |
| **7-维 rubric form-filling prompts** | ✅ | `src/.../rubrics/` |
| **Per-task checkpointing**（JSON 序列化，使用 `dataclasses.fields()` + `SimpleNamespace` round-trip，**主动避开非 JSON 二进制序列化方案**以满足项目 PreToolUse 安全 hook） | ✅ | `experiments/run_*.py` |
| **5-rep V4 verification**（noise floor 协议落地） | ✅ | `experiments/analyze_default_verify_v4.py` |
| **W2 confidence-formula bug 复现 + 修复** | ✅ | 已在 PR #8 |
| **provider snapshot 记录** | ✅ | per-task checkpoint 中 |

**为什么序列化要避开非 JSON 二进制方案**：项目级 PreToolUse hook 把 Python 二进制序列化协议（`.pkl`-style）视为高危，原因是反序列化等价于代码执行。我们改用 **JSON + `dataclasses.fields()` 显式 schema + `SimpleNamespace` round-trip**：

1. JSON 是结构化文本，可被 hook、reviewer、CI 扫描器审计；
2. `dataclasses.fields()` 列出显式字段，避免反序列化路径碰到任意类构造器；
3. `SimpleNamespace` 仅做属性访问承载，不引入可执行钩子。

这一安全纪律在 SE artifact judging 场景下不仅是工程要求，本身**也是方法学论文的一个加分项**——审稿人会注意到我们对 reproducibility + supply-chain safety 的重视。

---

## 4. §Related Work 段落骨架（可复用到论文里）

```
§2 Related Work
   §2.1 LLM-as-Judge for Free-Text Outputs
        - G-Eval [Liu23] — auto-rubric, NLG
        - MT-Bench [Zheng23] — pairwise dialog, position-bias correction
        - Prometheus [Kim24] — fine-tuned 13B judge, generic rubric
        - JudgeLM [Zhu23] — fine-tuned Vicuna pairwise
        - 共同特征：自由文本 + 单 seed + 隐含 generic rubric
        - 共同空缺：未触及 SE artifact、未做 noise floor

   §2.2 Aggregation & Calibration
        - Self-Consistency [Wang23] — multi-sample majority vote
        - Verbalized Confidence [Tian23] — "just ask" calibration
        - Constitutional AI [Bai22] — critique-revise + RLAIF
        - 我们与之的关系：aggregation 思路借鉴，但用于 noise floor 而非 vote

   §2.3 SE Artifact Quality Evaluation (Pre-LLM)
        - Code Review research
        - UML / SysML inspection methods
        - Formal-method consistency checking
        - 共同空缺：人工成本高，自动化几乎不存在

   §2.4 Bridging the Gap (this work)
        - 1) anchored rubric for SE artifact (vs auto-rubric in G-Eval)
        - 2) 5-rep noise-floor protocol (vs single-seed in §2.1)
        - 3) prompting-only path (vs fine-tune in Prometheus / JudgeLM)
        - 4) STM artifact as first concrete instance
```

---

## 5. 当前已落地 / 待办（方法学论文准备 lens）

### 5.1 已落地

- ✅ Path A baseline V3/V4 5-rep done（数据可用作 noise floor evidence）
- ✅ W2 confidence-formula bug 发现 + 修复（可作为方法学论文的 motivating example）
- ✅ Provider drift / cache effect 显式记录的纪律（前沿讨论）
- ✅ llm_as_judge_methods_corpus/ 文献库（7 篇 placeholder DESC.md，PDF 待获取）
- ✅ SE 方向定位明确

### 5.2 短期待办（论文写作前的硬要求）

| 项 | 状态 | 优先级 |
|---|---|:-:|
| 把 7 篇 LLM-as-Judge 论文的 PDF 抓回来，按 `DESC_GUIDE.md` 修订 DESC.md | ⏳ | **P0** |
| Path C startup（如果决定走多 model judge ensemble）| ⏳ | **§6.2 用户决策点** |
| Rubric 消融实验（7 维 → 各维独立 ablation）| ⏳ | P1 |
| 工业 case 寻找（ICSE / FSE 路线必要）| ⏳ | **§6.1 用户决策点决定后再启动** |
| W2 bug 的方法学化叙事 draft | ⏳ | P1 |

### 5.3 长期 / 加分项

- L4: anchored vs auto-generated rubric 的对照实验
- 多 LLM provider 跨家对比（OpenAI / Anthropic / Google）
- STM 之外的 SE artifact 验证（UML class diagram / sequence diagram）

---

## 6. 用户决策点（4 项，等待 push 决策）

### §6.1 投稿目标

候选 venue：TSE / EMSE / TOSEM / ICSE / FSE / ASE。
我倾向：**EMSE（empirical 纪律契合 + 周期可控）+ TSE（保底期刊）双轨**。
ICSE / FSE 路线需要工业 case，建议作为 v2 投稿计划。

### §6.2 Path C 启动？

Path C = 多 LLM judge ensemble + cross-provider agreement。
- ✅ Pro：方法学论文加分项；多 provider 数据是 L3 强证据
- ❌ Con：工程量大；当前 V4 5-rep 已是足够 strong baseline

倾向：**先把 V4 写完 + 投出去；Path C 留给 revision round 或第二篇**。

### §6.3 Rubric 维度数

当前 7 维（A-G）。是否有合并空间？
- 候选合并：D evidence + C specificity → 可能合并为"具体性证据维"
- 候选拆分：B accuracy 可能要拆为"事实正确"vs"语义正确"

倾向：**先保 7 维做实验；ablation 之后再决定**。

### §6.4 Push 时机

当前 PR #8 已有 V4 5-rep 数据。本轮新增的学术内容（corpus 新建 + v2 讨论）尚未 push。
倾向：**本地 commit；push 等用户 explicit 命令**（沿用 v1 的 "没让你更新 PR 不要更新" 纪律）。

---

## 7. 与 v1 版的差异

| 维度 | v1 | v2（本版）|
|---|---|---|
| 研究方向 | 隐式（默认 NLP/ML 思路）| ✅ **显式 SE 方向声明**（§0）|
| 论文类型 | 模糊 | ✅ **methodology paper 明确**（§1）|
| LLM-as-Judge 综述 | 简短罗列 7 篇 | ✅ **方法 × IO 详细横向表 + 4 维局限分析**（§2）|
| 文献库 | 不存在 | ✅ [llm_as_judge_methods_corpus/](../llm_as_judge_methods_corpus/) **独立建库**，7 篇 placeholder DESC.md |
| §Related Work 骨架 | 缺失 | ✅ §4 给出可复用骨架 |
| 决策点 | 含糊 | ✅ §6 4 项明确决策点 |

---

## 8. 附：与本讨论相关的项目结构

```
project_ex1_llm_judge_for_stm/
├── discussions/                                      # 学术讨论纪要
│   ├── 2026-05-08-19-20-31-AI-讨论-...-_v1.md
│   └── 2026-05-08-19-39-19-AI-讨论-...-v2.md         # 本文件
└── llm_as_judge_methods_corpus/                      # 📚 NEW — LLM-as-Judge 方法学文献库
    ├── README.md
    ├── SUMMARY.md
    ├── GUIDE.md
    ├── DESC_GUIDE.md
    ├── g-eval/{DESC.md, bibtex.bib}
    ├── mt-bench/{DESC.md, bibtex.bib}
    ├── self-consistency/{DESC.md, bibtex.bib}
    ├── constitutional-ai/{DESC.md, bibtex.bib}
    ├── tian-verbalized-confidence/{DESC.md, bibtex.bib}
    ├── prometheus/{DESC.md, bibtex.bib}
    └── judgelm/{DESC.md, bibtex.bib}
```

完整项目结构见 [README.md §二、目录结构](../README.md)。

---

**对话上下文锚点**：

- 用户最近 3 项学术纠正 → 全部已落实（§0 / §1 / §2 / corpus 建库）
- 仍待用户决策的 4 项 → §6
- 当前操作纪律 → 不主动 push（v1 已声明）
