# ai-native-se-roadmap：A1 S1--S8 round3 单篇维度抽取审计

## 0. 审计边界与阅读状态

- **处理对象**：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/ai-native-se-roadmap`。
- **本轮角色**：A1 survey-of-surveys 单篇维度抽取；未开启 sub-subagent。
- **输出边界**：本文件只做 A1 文本级审计，不修改 `review.md`；不得把本文的 roadmap 枚举、内部计数或 companion work 数字写成 Paper2 final quantitative finding。
- **总体判定**：该文是 **vision / roadmap / proposal**，不是 SLR / SMS / tertiary / MLR / guideline 检索研究；可作为 `roadmap_boundary_anchor`、`schema_seed` 和候选方法启发，不进入主统计池。

| 材料 | 阅读状态 | 依据 |
|---|---|---|
| `bibtex.bib` | 已读全文 | 10 行；确认 `Hassan_2026`、TOSEM、2026、DOI `10.1145/3807901`。 |
| `metadata.json` | 已读全文 | 确认本地已标 `review_type=vision / roadmap`、`eligible_for_statistical_synthesis=false`、`evidence_role=roadmap_boundary_anchor`。 |
| `paper_content.txt` | 已读全文 | 1--1146 行；覆盖摘要、§1--§5 与参考文献 [1]--[117]。关键锚点：摘要 8--21 行；愿景来源 61--69 行；挑战模板 580--586 行；OQ7--OQ14 798--823 行；结论降级 851--856 行。 |
| `review.md` | 已读全文 | 1--469 行；重点复核“维度树复原”194--433 行与 “survey_of_surveys 自身 schema 抽取”435--466 行。 |
| `evidence_chain.md` | 已读全文 | 1--47 行；A.1--A.4 均已读，重点核对 A.2/A.3 中 `clm-ai-native-se-roadmap-*`。 |
| `paper.pdf` | 仅做元数据/存在性核验，未做视觉精核 | `pdfinfo` 显示 25 页；本轮未人工核对 Fig. 1--7 的版面、箭头和截图内容，全部列为 A2a。 |

## 1. 原文如何描述“样本集合 / 行动项 / 证据对象”

### 1.1 原文显式对象

1. **愿景对象**：SE 3.0 / AI-native SE。摘要明确说作者提出从 SE 2.0 转向 SE 3.0，并概述技术栈和挑战路线图（`paper_content.txt` 8--21 行）。
2. **证据来源对象**：作者称愿景来自学术与灰色文献 surveys、社区活动、客户与内部团队会议、作者研发 FMware / SE 3.0 stack 的实践经验，以及 OPEA 40+ 工业伙伴互动（61--69 行）。这些是来源线索，不是系统检索语料链。
3. **时代对照对象**：SE 1.0 / SE 2.0 / SE 3.0 三时代对照（98--131 行，Fig. 1 文本抽取）。
4. **技术栈对象**：Teammate.next、IDE.next、Compiler.next、Runtime.next、FM.next 五层 stack（250--279 行，§3.2--§3.6）。
5. **挑战 / 行动项对象**：§4 明确每个 challenge 包含 description、affected stack parts、open questions、作者 vision（580--582 行）；作者同时说明列表不是 exhaustive（584--586 行）。§4.1--§4.5 给出 5 个主挑战和 OQ1--OQ6；§4.6 另列 OQ7--OQ14（798--823 行）。

### 1.2 本地降级解释

- 原文没有 primary-study 样本库，没有检索式、数据库、纳排、去重、质量评价、抽取表、编码一致性或 synthesis protocol。
- 因此，本文的“样本单位”不能写作论文样本；A1 可复原的原生编码对象应降级为：**时代 baseline 项、技术栈组件项、challenge / OQ 路线图项、证据来源类型项**。
- 117 条参考文献不是 SLR 分母；3 个时代、5 个 stack component、5 个主挑战、14 个 OQ 也只能作为本文内部结构枚举，不是跨论文统计池分母。

## 2. S1--S8 逐项审计

| 维度 | 等级 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 弱 | 摘要与 §1 说明本文提出 SE 3.0 vision、technology stack 与 challenge roadmap（8--21、51--73 行）；但没有 RQ-driven review 设定。 | 根对象是“SE 3.0 愿景 + 路线图”，不是 review RQ 树；本地降级为 roadmap/proposal 根节点。 | 否；只作边界锚点和 schema seed。 | 核对 ACM final / PDF 页码；确认不存在隐藏 method/protocol 附录。 |
| S2 语料收集与筛选 | 弱 | §1 只列出 academic/gray literature surveys、workshop、客户讨论、内部经验、OPEA 伙伴互动（61--69 行）；无数据库、检索式、纳排、分母链或 QA。 | 可把 `evidence.source_type` 复原为开放枚举，但不能复原系统语料链。 | 否；117 references 不是 SLR 分母。 | 复核参考文献总数、作者团队 companion/self-citation 标记；确认无 supplementary 检索协议。 |
| S3 原生维度树 / 样本编码对象 | 中 | Fig. 1 抽取三时代对照（98--131 行）；Fig. 3 与 §3.2--§3.6 给出 5 层 stack；§4.1--§4.6 给出 5 个主挑战与 OQ1--OQ14。 | 可复原为“时代 baseline 对照树 + 五层技术栈树 + challenge/OQ 路线图树”的维度森林；属于 roadmap 降级树。 | 否；结构枚举可作 schema seed，不作跨论文统计样本。 | 打开 PDF 核对 Fig. 1、Fig. 3、Fig. 4--7 的图形结构、箭头和组件命名。 |
| S4 字段级证据 | 弱 | §4 显式声明 challenge entry 的 4 字段：description、affects、open question、our vision（580--582 行）；§4.1--§4.5 有 `Affects` 行（594、645、681、728、761 行）。 | 可复原 `challenge.template_field` 与 `edge.affects` 关系边；但这是 roadmap 字段，不是样本级抽取表或 QA 表。 | 否；字段可迁移为候选 schema，不进入主统计。 | 精核每个 challenge 的 `affects` 取值、OQ 编号、vision 段落与 companion evidence 引用。 |
| S5 维度模式演化 | 弱 | 原文呈现 SE 2.0 局限 → SE 3.0 stack → challenges/OQ 的叙事链；§3.6 的 curriculum recipe（521--543 行）是 FM.next 设想，不是本文 roadmap 的编码形成过程。 | 本地只能复原“愿景链条”和“curriculum-as-asset 类比”；不能复原开放编码、分类迭代、coder discussion 或 guideline update 过程。 | 否；仅方法启发。 | 区分 InstructLab / curriculum learning 引文与作者自己的 roadmap 形成过程，避免把 FM.next recipe 误写成本文方法。 |
| S6 统计分析 | 不适用 / 弱 | 原文有内部枚举与 companion 数字：3 个时代、5 个 stack component、5 个主挑战、14 个 OQ；另有 Runtime/RAR 等 companion work 数字，如 30%、50%、90%（696--718 行）。 | 这些是 roadmap 内部枚举或外部 companion work 局部结果，不是本文完成的系统统计 synthesis。 | 否；不进入主统计池，也不得进入 SUMMARY 定量 finding。 | A2a 如需使用 [28]/[98]/[114] 数字，必须分别读取 companion paper 并记录实验对象、发表状态、独立性和外推边界。 |
| S7 候选 finding | 中（仅结构启发） | §4 把 challenge 组织成 description → affected component → OQ → our vision；§5 又说 IDE.next 依赖其他组件，SE 3.0 只能在全 stack prototype 后整体评估（840--850 行），并欢迎 opposing views（853--856 行）。 | 可迁移的是候选 finding ledger 结构：limitation / challenge → stack component → open question → proposed vision → evidence type；领域主张全部降级为 vision claim。 | 否；只可作 candidate heuristic，需后续 A2a/A2b 研究者裁决。 | 为每条候选 finding 标注证据类型：vision-only、prototype、industry signal、peer-reviewed prior work、self-citation / companion。 |
| S8 研究者 / 作者质疑与裁决 | 弱 | 原文没有多研究者筛选、编码分歧、一致性或 QA；仅有 `not exhaustive`（584--586 行）、ToM 非银弹（637--640 行）、§4.6 未发展完整 vision（798--800 行）、`only time will tell` 与欢迎反对观点（851--856 行）。 | 可作为“缺少裁决日志”的反面样本：roadmap 文献必须显式记录人工质疑、override 和降级链。 | 否；不支持质量控制统计。 | 复核是否存在独立 threats/limitations section；精确定位上述降级语句页码。 |

## 3. 原生维度树 / 维度森林复原

> 说明：下列“原文明示”指原文以标题、图、段落模板或 OQ 编号明确呈现；“本地复原”指 A1 审计为便于 Paper2 schema 设计而结构化出的节点、取值空间或关系边。所有本地复原均不得升级为原文声称的系统综述发现。

```text
[根节点，本地复原]
AI-native SE / SE 3.0 愿景与挑战路线图
样本单位 = roadmap item / stack component / era baseline / evidence-source cue
统计池资格 = false

├── [树 A，原文明示 + 本地表格化] 软件工程时代 baseline 对照
│   ├── 时代标识（原文明示，封闭枚举）= {SE 1.0, SE 2.0, SE 3.0}
│   ├── 时间锚（原文明示，图中文字；A2a 核图）= {since 1968, since mid-2000s, late 2020 / early 2030}
│   ├── 开发取向（原文明示）= {code-centric, code-centric + AI4SE, intent-centric / conversation-oriented}
│   ├── 技术引擎（原文明示）= {program analysis, data-driven inefficient FMs, knowledge-driven efficient FMs}
│   └── 人机角色（本地复原）= {human drives process, human with AI assistants, AI teammate drives code loop with human intent alignment}
│
├── [树 B，原文明示 + 本地层级化] SE 3.0 五层技术栈
│   ├── Teammate.next（原文明示）
│   │   ├── transition（原文明示）= static/impersonal coding assistant → self-evolving personalized mentor
│   │   ├── traits（原文明示开放集合）= {conversational intelligence, social intelligence, personification, self-reflection, recurrent context learning, mentor role}
│   │   └── depends_on（本地关系边）= Compiler.next
│   ├── IDE.next（原文明示）
│   │   ├── transition（原文明示）= code-centric/editing → intent-centric/conversations
│   │   ├── input modalities（原文明示开放集合）= {informal description, pseudocode, UI sketches, example data}
│   │   ├── asset（原文明示）= conversations should be archived/version-controlled
│   │   └── depends_on（本地关系边）= Teammate.next + Compiler.next；结论段称 IDE.next largely depends on all other components
│   ├── Compiler.next（原文明示）
│   │   ├── transition（原文明示）= logic-rule realization → search-space exploration / multi-objective optimization
│   │   ├── objectives（原文明示）= {accuracy, latency, cost}
│   │   ├── mechanisms（原文明示开放集合）= {code mutation, self-reflection, semantic caching, distributed execution, goal tracking intent→tests}
│   │   └── companion evidence（原文明示）= [28] HumanEval-Plus feasibility claim；A2a 需读原文
│   ├── Runtime.next（原文明示）
│   │   ├── transition（原文明示）= serving models → serving compound apps / FMware
│   │   ├── properties（原文明示）= {SLA-aware, uni-clusters, edge-computing extension}
│   │   ├── runtime components（原文明示开放集合）= {profiler, resource provisioner, router, cluster manager, per-task slack, DAG workflow}
│   │   └── companion numbers（原文明示但非本文统计）= {30% latency improvement, 50% fewer expensive requests, ~90% quality}
│   └── FM.next（原文明示）
│       ├── transition（原文明示）= data-driven inefficient FMs → curriculum-engineered / knowledge-driven efficient FMs
│       ├── curriculum recipe（原文明示开放集合）= {scope/domain/subdomain, hierarchical taxonomy, examples/templates/evaluation rules, synthetic data, consistency testing, pilot testing, community contribution, data-flywheel refinement}
│       └── reference axes（原文明示）= {SWEBOK-inspired SE competence, cognitive observability, InstructLab branches: knowledge / foundational skills / composition skills}
│
└── [树 C，原文明示 + 本地关系边化] Challenge / OQ 路线图
    ├── challenge template（原文明示封闭字段）= {description, affected stack parts, open question, our vision}
    ├── C1 human-AI alignment（原文明示）→ affects = {IDE.next, Teammate.next} → OQ1
    ├── C2 code synthesis efficiency（原文明示）→ affects = {Compiler.next, Teammate.next} → OQ2
    ├── C3 runtime performance（原文明示）→ affects = {Runtime.next} → OQ3, OQ4
    ├── C4 FM understanding of code and SE（原文明示）→ affects = {Compiler.next, Teammate.next} → OQ5
    ├── C5 eliminating prompt engineering（原文明示）→ affects = {AI teammate + all FMware layers} → OQ6
    └── OQ7--OQ14 other open questions（原文明示但字段缺失）
        ├── 缺失 affects 字段（本地复原缺失语义）= not reported / not yet developed
        └── 缺失 our vision 字段（本地复原缺失语义）= 作者明示尚未发展 thorough vision
```

### 3.1 叶子取值空间审计

| 叶子 | 原文 / 本地 | 取值空间 | 证据与限制 |
|---|---|---|---|
| `era.id` | 原文明示 | `{SE 1.0, SE 2.0, SE 3.0}` | Fig. 1 文本抽取 98--131 行；需 PDF 核图。 |
| `stack.component` | 原文明示 | `{Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next}` | Fig. 3 与 §3.2--§3.6；封闭于本文 vision，不代表社区标准分类。 |
| `challenge.template_field` | 原文明示 | `{description, affects, open question, our vision}` | 580--582 行；高价值 schema seed。 |
| `challenge.affects` | 原文明示关系字段 | 多选自五层 stack；OQ7--OQ14 缺失 | 594、645、681、728、761 行；§4.6 缺失应写 `not reported`。 |
| `open_question.id` | 原文明示 | `OQ1--OQ14` | OQ 集合是 snapshot；作者明示 challenge list 非 exhaustive。 |
| `evidence.source_type` | 本地复原 | `{literature survey cue, gray literature cue, workshop/summit, customer/internal meeting, practical experience, OPEA industry interaction, companion work, prior peer-reviewed work}` | 来自 61--69 行；不能当系统检索来源链。 |
| `claim.evidence_strength` | 本地复原 | `{vision-only, prototype/companion, industry signal, prior work, not_verified}` | 用于 A2a 区分主张强度；当前大多需 PDF/companion 精核。 |

### 3.2 关系边审计

| 边 | 明示 / 复原 | 源 → 目标 | 缺失值语义 | 统计用途 |
|---|---|---|---|---|
| `edge.affects` | 原文明示 | challenge / OQ1--OQ6 → stack component | §4.6 OQ7--OQ14 未报告 affected component；不得补猜。 | 仅本文内部结构矩阵；不进入主统计池。 |
| `edge.depends_on` | 本地复原 | stack component → stack component | 原文没说则 `not reported`；结论段仅说明 IDE.next largely depends on all other components。 | 方法启发；不作定量 finding。 |
| `edge.inspired_by` | 本地复原 | design choice → external theory/prior work | 缺失表示作者未挂外部理论；不是反证。 | 可作证据强度/来源类型字段。 |
| `edge.exemplified_by` | 本地复原 | vision/challenge → tool/platform/example | 快速漂移风险；需官方来源日期。 | 不进入统计池；只作背景例子。 |

## 4. 统计池资格与 A2a 接力

- **主统计池资格**：否。
- **排除理由**：非系统综述；无系统检索、纳排、质量评价、数据抽取、编码协议或分母链。
- **可用方式**：`boundary_anchor`、`schema_seed`、`candidate_finding_heuristic`、`risk_only`。
- **禁止方式**：不得把 117 条参考文献、3 个时代、5 个 stack component、5 个主挑战、OQ1--OQ14、Teammate.next 被 4/5 主挑战关联、Runtime/RAR companion 数字等写成 Paper2 final quantitative finding。
- **A2a 接力项**：
  1. 人工打开 PDF 核对 Fig. 1--7 的图形布局、箭头、标签和截图内容。
  2. 精确页码/表图锚定 §4.1--§4.6 每个 OQ、`Affects` 行和 `our vision` 段落。
  3. 若使用 [28]、[36]、[45]、[85]、[98]、[114] 等 companion work，必须单篇读取并标注发表状态、实验对象、是否作者团队自引用、是否独立复现。
  4. 快速变化工具、模型、benchmark、vibe-coding 平台示例须按官方来源和核验日期重查。

## 5. 对 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 问题清单

| 等级 | 文件 | 问题 | 影响 | 建议 |
|---|---|---|---|---|
| C | -- | 未发现需要立即阻断 A1 的 critical 问题。 | 当前单篇大方向已正确降级为 non-statistical roadmap boundary anchor。 | -- |
| I | `SUMMARY.md` | S1--S4 覆盖矩阵中该文 S4 仍写作“中：可抽取技术栈组件、挑战模板、影响范围、开放问题和证据来源类型等路线图字段……”。这与 `review.md` S4=弱、adjudication“采纳 S4 降为弱”的口径不一致。 | 可能让后续 A2a/A2b 把 roadmap 字段误读为系统综述字段级证据。 | 将 SUMMARY 中该文 S4 降为“弱：有 roadmap 字段模板和 `affects` 关系边，但无样本级抽取表 / QA / sample ID；只作 schema seed”。 |
| M | `SUMMARY.md` | S5--S8 矩阵中该文 S6 写“弱”，而 `review.md` 写“不适用 / 弱”。 | 不一定污染主统计池，因为同表已标 `否`；但口径不够精确。 | 改成“不适用 / 弱：无系统统计；仅有内部结构枚举和 companion 数字，均不得进入主统计池”。 |
| M | `review.md` | §6.1 将 challenge × component 覆盖矩阵写成“内部统计观察”，并列出 Teammate.next 4/5、Runtime.next 1/5。虽然上下文已说明不进统计池，但仍有被摘录成定量 finding 的风险。 | 若后续摘表不带上下文，可能违反 A1 不产出 final quantitative finding 的纪律。 | 可在该小节首句再加“以下仅为本文内部结构枚举，不进入 SUMMARY 定量统计或 final finding”。 |
| M | `evidence_chain.md` | A.2 中多数证据强度为 `not_verified` 是正确的；`ev-ai-native-se-roadmap-pool` 的证据强度写 `adjudicated`，不是常规 strong/medium/weak/not_verified 口径。 | 对人类读者可理解；若后续脚本严格枚举证据强度，可能产生兼容风险。 | 可改为 `not_verified; adjudicated boundary` 或在 GUIDE/脚本中明确允许 adjudicated。 |
| M | `evidence_chain.md` | A.2 多处以“短引见 review.md”代替原文短引；当前符合 A1 最小链路，但 A2a 前不能升级。 | 不影响 A1，但限制精确证据复用。 | A2a 将核心 evidence 逐条补原文短引、页码、图号和行号。 |

## 6. 审计结论

本篇的 A1 价值不在统计，而在复原一种 **roadmap / vision 文献的原生维度森林**：时代 baseline、未来技术栈、challenge/OQ、`affects` 关系边和证据来源类型。当前 `review.md` 的总体降级方向正确；最需要同步的是 `SUMMARY.md` 中 S4/S6 口径与单篇审计保持一致。任何从本文抽出的数量都只能标为“本文内部结构枚举 / A2a 待核验”，不得进入 Paper2 最终定量发现。
