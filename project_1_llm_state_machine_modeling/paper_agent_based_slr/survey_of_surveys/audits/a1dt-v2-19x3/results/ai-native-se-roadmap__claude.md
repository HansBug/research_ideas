材料已读完，开始撰写完整审计报告。

`★ Insight ─────────────────────────────────────`
- 这篇论文非常清楚地自我定性为 vision/roadmap：摘要直接说"We propose / We outline / We present a roadmap of challenges"，且 §1 列出五类"愿景来源"（非系统综述 surveys+灰色文献、行业 workshop、客户讨论、作者 prototype 经验、OPEA 工业合作）——没有数据库、检索式、纳排、分母、质量评价。
- 它的真正"原生结构"不是六叶 SLR 模板，而是 **{三时代 baseline} × {五层技术栈} × {6+8 个 challenge/OQ}**，并且每个主 challenge 自带 4 字段 schema：`Description / Affects / Open question / Our vision`。这与 SLR 的"样本单位 → 抽取表"是完全不同的对象类型。
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇审计报告 — `ai-native-se-roadmap`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `ai-native-se-roadmap` |
| agent | `claude`（claude-opus-4-7[1m]，本地直接读取，无 subagent / 后台 agent） |
| 是否已读 `paper_content.txt` | 是；分两页读取 1–707、708–1146，覆盖摘要、§1–§5、参考文献 [1]–[117] |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；与本地引文键 `Hassan_2026` 与 DOI `10.1145/3807901`、`publication_date 2026-04-09` 交叉核对一致 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅文本审计，Fig. 1/2/3/4/5/6/7 未做版面核验，留 A2a |
| 原文类型 | **vision / roadmap / proposal**（自我定位）；不是 SLR、SMS、tertiary、MLR、guideline 检索研究 |
| 被编码样本单位 | 不存在系统样本库；原生编码对象是 **{SE 1.0/2.0/3.0 三时代 baseline}**、**{Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next 五层技术栈组件}** 和 **{6 个主 challenge + OQ1–OQ14 共 14 个 open question}** |
| 样本数量 / 分母 | 不适用为统计分母；可记录的"原生项数"：3 个时代、5 个 stack component、6 个主 challenge、14 个 OQ；引用 [1]–[117] 共 117 条，但作者未声明任何检索 / 纳排，因此 117 不是 SLR 分母 |
| 原生树类型 | **降级树（roadmap/challenge 树）+ 辅助"era baseline 对照树"**；不是 SLR 维度森林 |
| 主统计池资格 | **否**；与 `metadata.json` 中 `eligible_for_statistical_synthesis: false`、`evidence_role: roadmap_boundary_anchor`、`systematic_evidence_status: non_systematic_or_boundary_anchor` 一致 |
| 总体判定 | **needs repair**：现有 `review.md` 在 §1 / §2 / §3 / §4 与"通用接口投影"段叙述正确，但"维度树复原"主表的 6 个 `leaf-*` 节点和"原文模式候选叶子映射"5 个 `orig-*` 占位叶子仍是抽象 placeholder，未把论文真实的 5 层 stack、4 字段 challenge schema、14 条 OQ 编号体系作为原文 schema 主树。建议执行下方 §7 的最小返修。 |

## 1. 原文证据阅读说明

**实际读取的文件与范围**：

- `bibtex.bib`：第 1–10 行，确认 `Hassan_2026` / TOSEM / 2026 / DOI `10.1145/3807901`。
- `metadata.json`：第 1–35 行，确认 `review_type=vision/roadmap`、`eligible_for_schema_seed=true`、`eligible_for_statistical_synthesis=false`、`evidence_role=roadmap_boundary_anchor`、CCF=A、TOSEM 期刊、arXiv `2410.06107` 作为开放全文来源。
- `paper_content.txt`：1–1146 行全文文本（分两页读取），包含摘要、§1 Introduction、§2 critical analysis of SE 2.0、§3 Vision of SE 3.0（含 §3.1–§3.6 五个 stack 组件）、§4 Challenges（§4.1–§4.5 五条主 challenge + §4.6 OQ7–OQ14）、§5 Conclusion 与 [1]–[117] 全部参考文献。
- `review.md`：1–428 行全文，含历史草稿、维度树复原、A.1–A.4 审计附录。
- `paper.pdf`：未打开，因此 Fig. 1–7 的版面 / 箭头 / 标签 / Figure 6（NIPS 2015 Sculley 改图）未做版面核验，仅依赖文本里的 Figure 引用句。

**仅基于 text 的局限**：所有 Figure 的视觉布局、表内分类（如 Fig. 1 的 SE 1.0/2.0/3.0 三栏对照、Fig. 3 stack 图的箭头与命名一致性、Fig. 5/Fig. 7 截图取自 GitHub Copilot / OpenAI docs 的具体内容、Fig. 6 中"FM Code" vs "AIware / Compute / Curriculum Engineering" 等组件的精确命名）都需要 A2a 打开 PDF 复核。

**关键原文证据锚点（按出现顺序）**：

1. **摘要 / 自我定位**（Page 1, 行 8–25）："We propose a shift towards SE 3.0 ... We outline the key components ... We also present a roadmap of challenges that must be overcome to realize our vision."
2. **愿景来源声明**（Page 2, 行 61–69）：vision 基于 "(i) surveys of academic and gray literature, (ii) in-depth discussions ..., (iii) meetings with our customers and our own internal development teams ..., (iv) our practical experience with the research and development of FMware, and (v) our close interactions with several industrial partners (40+ leading companies, including Intel, AMD, RedHat, HuggingFace, and SAP) as part of the Open Platform for Enterprise AI (OPEA) alliance"——这是非系统综述声明。
3. **三时代 baseline 对照**（§1 与 Fig. 1, Page 2–3, 行 100–131）：SE 1.0 (code-centric / program analysis) → SE 2.0 (code-centric AI4SE / data-driven FMs) → SE 3.0 (intent-centric / AI-native / knowledge-driven)。
4. **SE 2.0 三类 limitation + 1 类 boundary**（§2.2–§2.3, Page 3–5）：(2.2.1) cognitive overload；(2.2.2) inefficient model training；(2.2.3) suboptimal code quality / additive bias；(2.3) autonomous SE benchmark limitation (SWE-Bench Verified, TRAE 75.2%, 仅 Python、12 项目，~70% 任务来自 3 个项目)。
5. **五层技术栈定义**（§3.2–§3.6 + Fig. 3, Page 7–13）：Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next，每层都自带 `from_state → to_state` 转换、所需 capability 与 companion paper 引用。
6. **Challenge 原文 4 字段 schema**（§4 引言段, Page 13, 行 580–586）："For each challenge, we include a description, what parts of the SE 3.0 stack it affects (Figure 3), one or more open questions, and our vision regarding the solution to those questions." — 这就是 `Description / Affects / Open question / Our vision` 四字段模板。
7. **OQ1–OQ6 主 challenge**（§4.1–§4.5, Page 13–18）：OQ1 ToM 平衡；OQ2 synthesis efficiency；OQ3 runtime > Ray Serve；OQ4 edge routing；OQ5 FM 理解 SE；OQ6 prompt engineering 消除。
8. **OQ7–OQ14 其他开放问题**（§4.6, Page 18, 行 800–823）：教育 / 编程语言 / IDE UI / Compiler benchmark / IP / 就业 / 开放创新 / accessibility & equity & fairness。
9. **Companion / under-review 自引用证据矩阵**（§3.4、§3.5、§4.1、§4.2、§4.3, [28]/[44]/[45]/[85]/[98]/[114]）：Compiler.next [28] 仍在 TOSEM 审稿；FMware [45] preprint；Watson [85]、SPICE [70]、RAR [98] 已被会议接收但仍是 self-citation 生态。
10. **Runtime.next 经验声明**（§4.3, Page 16, 行 696–697）："Preliminary results show a latency improvement in the order of 30% compared to Ray Serve."
11. **RAR 路由经验**（§4.3, Page 17, 行 716–718）："on different subsets of the popular MMLU benchmark [47], our approach routes 50% fewer requests to computationally expensive models while maintaining around 90% of the general response quality."
12. **结论 + 商业 vibe-coding 平台清单**（§5, Page 19–20, 行 851–853）：Lovable / Base44 / Replit / Bolt.new / V0 by Vercel 被列为"很早期的 SE 3.0 苗头"。

## 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象是什么？**
   - 不是一组论文 / 工具 / artifact / 数据集样本，而是一个 **paradigm（SE 3.0）**及其内部的 **5 个 stack component** + **3 个 era baseline 对照** + **14 个 open question / challenge**。每一层 component 是一个抽象架构对象；每一个 OQ 是一个 roadmap 行动项。

2. **作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？**
   - **没有**。§1 (Page 2, 行 61–69) 显式承认愿景来自 "surveys of academic and gray literature + 行业 workshop + 客户讨论 + 作者研发经验 + OPEA 工业互动"，但没有给出搜索数据库、检索式、纳入分母、排除标准、质量评价 rubric、抽取表或数据综合协议。§4 引言段也明确说 "The list of challenges that we present is not meant to be extensive"（Page 13, 行 584）。

3. **原文字段来自哪里？**
   - **stack-component 模板**：来自 Fig. 3 的"SE 2.0 vs SE 3.0"对照（每个 component 都有 `from_state` 子弹列表 + `to_state` 子弹列表），文中再用 §3.2–§3.6 展开。
   - **challenge 4 字段模板**：作者在 §4 引言段（Page 13, 行 580–586）显式给出 `Description / Affects / Open question / Our vision`，并在 §4.1–§4.5 严格执行。
   - **Open Question 编号**：作者显式编号 OQ1–OQ14，每个 OQ 都有自然语言文本与（前 6 个） "Our vision" 段落。
   - **没有 extraction form / classification schema / taxonomy table / quality rubric / mapping table / appendix / replication package**。

4. **RQ 与样本单位是什么关系？**
   - 本文没有 RQ；最接近 RQ 的对象是 §4 的 6 个主 challenge + 14 个 OQ。这些 OQ 是"路线图行动项"，不是"用于编码样本的研究问题"。

5. **若无系统样本库，如何降级？**
   - 按 A1-DT v2 规则，本篇必须降级为 **boundary anchor + methodological seed + candidate heuristic**，不进入主统计池。`metadata.json` 已正确标注。

## 3. 原生样本编码维度树 / 维度森林

本篇的原生结构是 **"era baseline 对照树 + 5 层 stack 树 + challenge/OQ 树"** 三棵子树构成的**维度森林**，而不是一棵 SLR 编码树。

```text
[paper-root] Towards AI-Native SE (SE 3.0) — vision + roadmap

├── [tree-A] SE-era baseline 对照树 （Fig. 1, §1, §2.1, §3.1）
│   ├── era_id              ∈ {SE 1.0, SE 2.0, SE 3.0}     // 完整枚举（封闭，3）
│   ├── era_timeline_anchor ∈ {since 1968 (NATO) ;
│   │                          since mid-2000s (MSR, GitHub'08, SO'08, DL mid-2010s) ;
│   │                          late 2020–early 2030}        // 自由文本 + 时间锚
│   ├── code_orientation    ∈ {code-centric, code-centric AI4SE, intent-centric}   // 封闭，3
│   ├── tooling_engine      ∈ {program analysis, data-driven inefficient FMs, knowledge-driven efficient FMs}  // 封闭，3
│   └── human_role          ∈ {human-central, human-in-loop with copilots, human-AI symbiosis (AI drives code-loop)}  // 封闭，3
│
├── [tree-B] SE 3.0 五层技术栈树 （Fig. 3, §3.2–§3.6）
│   ├── [B1] Teammate.next            // 角色：personalized AI partner
│   │     ├── from_state ∈ {static, impersonal coding assistant}
│   │     ├── to_state   ∈ {self-evolving, personalized mentor}
│   │     ├── required_traits ⊆ {conversational intelligence, social intelligence, personification,
│   │     │                       autonomous self-reflection, recurrent-context learning, mentor role}
│   │     ├── depends_on ⊇ {Compiler.next (§3.4)}
│   │     └── companion_evidence ∈ {[24] CHaves&Gerosa survey, [36] Gallaba et al. ToM multi-agent}
│   ├── [B2] IDE.next                 // 角色：intent-centric IDE
│   │     ├── from_state ∈ {code-centric, editing}
│   │     ├── to_state   ∈ {intent-centric, conversational}
│   │     ├── input_modalities ⊆ {informal NL description, pseudocode, UI sketch, example data}
│   │     ├── code_visibility ∈ {hidden by default, low-level debugging mode}
│   │     ├── conversation_as_asset ∈ {versioned, archived}
│   │     ├── code_definition_scope ⊇ {Python code, ML models, prompts, data}
│   │     └── inspiration_source ∈ {TDD [19,20]}
│   ├── [B3] Compiler.next            // 角色：search-based intent synthesizer
│   │     ├── from_state ∈ {logic-rule realization}
│   │     ├── to_state   ∈ {search-space exploration / multi-objective optimization}
│   │     ├── core_mechanisms ⊆ {code mutation, self-reflection, semantic caching,
│   │     │                       distributed execution, multi-objective optimization,
│   │     │                       goal-tracking (intent→test), iterative synthesis}
│   │     ├── objectives ⊆ {accuracy, latency, cost}
│   │     ├── benchmark_used ∈ {HumanEval-Plus [61]}
│   │     └── companion_evidence ∈ {[28] Cogo Compiler.next under-review TOSEM, [68] Autogen}
│   ├── [B4] Runtime.next             // 角色：SLA-aware uni-cluster runtime + edge
│   │     ├── from_state ∈ {serving models}
│   │     ├── to_state   ∈ {serving compound apps (AIware)}
│   │     ├── qualities  ⊇ {SLA-aware, uni-cluster, edge-computing extension}
│   │     ├── SLA_workload_types ⊆ {real-time / batch / memory-intensive}
│   │     ├── runtime_components ⊆ {profiler, resource provisioner, router, cluster manager,
│   │     │                          per-task slack, DAG workflow}
│   │     ├── reported_metric ∈ {30% latency improvement vs Ray Serve [114]}
│   │     ├── edge_routing_metric ∈ {RAR [98]: 50% fewer expensive requests, ~90% quality on MMLU [47]}
│   │     └── companion_evidence ∈ {[45] FMware preprint, [114] FMArts/Fusion, [98] RAR}
│   └── [B5] FM.next                  // 角色：curriculum-engineered knowledge-driven FM
│         ├── from_state ∈ {data-driven inefficient FMs}
│         ├── to_state   ∈ {curriculum-engineered knowledge-driven efficient FMs}
│         ├── curriculum_recipe ⊆ {define scope, identify domain/subdomain,
│         │                         hierarchical taxonomy, examples/templates/evaluation rules,
│         │                         teacher-FM synthetic data, internal consistency testing,
│         │                         pilot testing, community contribution, data-flywheel refinement}
│         ├── curriculum_root_branches ∈ {knowledge / foundational skills / composition skills} (InstructLab)
│         ├── reference_curriculum ∈ {SWEBOK [106]}
│         ├── SE_competence_axes ⊆ {requirements reasoning, architectural design,
│         │                          implementation, testing, debugging, maintenance}
│         ├── observability_axis ∈ {cognitive observability [85]}
│         └── companion_evidence ∈ {[51,91] InstructLab, [104] curriculum learning survey, [15] phi family, [85] Watson}
│
└── [tree-C] Challenge × OQ 路线图树 （§4.1–§4.6, 含每个 challenge 的 4 字段 schema）
    ├── challenge_template (作者在 §4 引言段显式声明)
    │     ├── Description           : free text
    │     ├── Affects               : multi-select ⊆ {Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next}
    │     ├── Open question (OQ#)   : free text + integer id
    │     └── Our vision            : free text + companion-paper references
    │
    ├── [C1] §4.1 human-AI alignment   → affects = {IDE.next, Teammate.next}   → OQ1
    ├── [C2] §4.2 synthesis efficiency → affects = {Compiler.next, Teammate.next} → OQ2
    ├── [C3] §4.3 runtime performance  → affects = {Runtime.next}              → OQ3, OQ4
    ├── [C4] §4.4 FM understanding     → affects = {Compiler.next, Teammate.next} → OQ5
    ├── [C5] §4.5 prompt engineering   → affects = {Teammate + all FMware layers} → OQ6
    └── [C6] §4.6 其他 OQ (无 Affects/Vision)
          ├── OQ7  good SE in SE 3.0 / next-gen SE training / CS curriculum
          ├── OQ8  programming languages for AI agents / token-efficient PL [114]
          ├── OQ9  IDE.next UI / plugin vs agent / agentic IDE [44]
          ├── OQ10 Compiler.next benchmark / interpretability [75]
          ├── OQ11 AI teammate IP ownership upon developer leaving
          ├── OQ12 SE 3.0 job impact
          ├── OQ13 open innovation / cross-silo collaboration
          └── OQ14 accessibility / equity / fairness [96]
```

**说明**：

- **取值空间封闭性**：tree-A 的 era_id（3 个值）与 tree-B 的 5 个 stack component 是**已封闭枚举**；tree-C 的 14 个 OQ 是**作者声明的当前枚举**，但作者也写明 "not meant to be extensive"，因此 OQ 集合是**开放枚举（snapshot）**。
- **关系边**：tree-B 与 tree-C 之间存在显式 `Affects` 关系（多对多），是本篇里**唯一可机械化的关系型字段**（详见 §5 关系边表）。
- 与 review.md "维度树复原"中六叶通用接口的对比：本树是**原文真实结构**；六叶接口是**跨论文投影层**，二者必须分层维护。

## 4. 叶子维度表

仅列**最关键的叶子字段**（取值空间和证据锚点都来自原文；未观察到原文取值的字段标 `待核验`）。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `era.id` | SE 时代标识 | tree-A | Fig. 1 三栏标题 | 软件工程演化时代 | {SE 1.0, SE 2.0, SE 3.0} | 完整枚举（封闭，3） | 不适用 | schema_seed | 可作"era-baseline 对照模板"启发 | Fig. 1 / §1 / §2.1 / §3.1 (行 27, 91–94, 280–289) | 仅迁移结构，不迁移"SE 3.0 已成立"的领域结论 |
| `era.code_orientation` | 代码取向 | tree-A | Fig. 1 第一行 bullet | 时代主导开发取向 | {code-centric, code-centric+AI4SE, intent-centric} | 完整枚举（封闭，3） | 不适用 | schema_seed | 启发 paper2 的 paradigm 对照轴 | Fig. 1 / §3.1 (行 280–302) | 迁移轴名 |
| `era.tooling_engine` | 工具引擎 | tree-A | Fig. 1 第三行 bullet | 时代主导技术引擎 | {program analysis, data-driven FMs, knowledge-driven FMs} | 完整枚举（封闭，3） | 不适用 | schema_seed | 启发"baseline 模型类型"轴 | Fig. 1 (行 100–124) | 迁移结构 |
| `stack.component_name` | 技术栈组件名 | tree-B | Fig. 3 / §3.2–§3.6 标题 | SE 3.0 stack 的组件 | {Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next} | 完整枚举（封闭，5） | 不适用（作者明确 5 个） | schema_seed；可作 5 项分布的"内部计数" | 候选 layered-architecture 模式启发 | Fig. 3 / §3.2–§3.6 (行 250–278, 307–520) | 仅迁移"分层 vision stack"结构，不迁移层名 |
| `stack.from_state` / `stack.to_state` | 转换前/后状态 | tree-B | Fig. 3 SE2.0/SE3.0 两栏 + §3 各小节 | 每层 component 的转换 | 自由文本，但每个 component 都有 1–N 条 bullet | 自由文本 + 半结构 bullet | 缺失视为非显式宣称 | schema_seed | 启发"component transition pattern" | Fig. 3 (行 258–278) | 迁移结构 |
| `stack.required_traits` | 所需能力子集 | tree-B | §3.2–§3.6 段落正文 | 该层为实现 to_state 需要的能力 | 各层不同的开放集合（见 §3 树） | 层级枚举（开放） | 缺失视为"作者未声明" | schema_seed | 候选 capability/property axis 启发 | §3.2 (行 313–337), §3.3 (行 343–374), §3.4 (行 375–417), §3.5 (行 418–476), §3.6 (行 477–578) | 迁移结构 |
| `challenge.template_field` | challenge 模板字段 | tree-C | §4 引言段 (行 580–586) 显式声明 | challenge 的 4 字段 schema | {Description, Affects, Open question, Our vision} | 完整枚举（封闭，4） | 缺失视为 unstructured challenge | schema_seed；可作"4-tuple roadmap entry"模板 | **高迁移价值**：Paper2 候选发现台账可直接采纳 | §4 引言 (行 580–586) | 完全可迁移结构 |
| `challenge.id` | challenge 编号 | tree-C | §4.1–§4.5 小节标题 + §4.6 列表 | 主 challenge 与附加 OQ | C1–C5 + OQ7–OQ14（OQ1–OQ6 嵌入 C1–C5） | 层级枚举（半开放） | 作者明确 "not exhaustive" | schema_seed | 候选 roadmap-completeness baseline | §4.1–§4.6 (行 587–823) | 迁移编号体系 |
| `challenge.affects` | 影响的 stack 层 | tree-C × tree-B | §4.1–§4.5 每节的 `Affects:` 行 | challenge → stack component 的多对多关系 | ⊆ {Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next}；§4.6 OQ7–OQ14 未填 | 关系值（multi-select） | §4.6 未填默认 unknown | schema_seed；可作"challenge → component 覆盖率"内部计数 | **关键关系字段**：可形成 5×6 影响矩阵 | §4.1 行 594 / §4.2 行 645 / §4.3 行 681 / §4.4 行 728 / §4.5 行 761 | 迁移关系建模方式 |
| `challenge.open_question` | OQ 文本 | tree-C | OQ# 框 | OQ 自然语言 | 自由文本 + 整数 id | 自由文本 + id | -- | schema_seed | 候选 RQ-style finding 启发 | §4.1–§4.5 OQ 框 / §4.6 列表 | 迁移结构 |
| `challenge.our_vision.companion_evidence` | 愿景配套引用 | tree-C | §4.1–§4.5 段尾"complementary work" | 支撑 vision 的 companion paper | 取值为 {[28], [36], [44], [45], [85], [98], [114]} 等作者团队工作 | 引用集合 | 缺失视为 vision-only | schema_seed | **风险字段**：可标记 self-citation 生态 | §4.1 (行 632–636), §4.2 (行 672–676), §4.3 (行 695–697, 714–718) | 迁移"愿景—证据—独立性"链路 |
| `evidence.source_type` | 证据来源类型 | 跨树 | §1 行 61–69 自我声明 | 愿景与 challenge 的证据来源 | {informal literature survey, gray literature, workshop/summit, customer discussion, internal team experience, OPEA industrial interaction, companion paper, peer-reviewed prior work} | 层级枚举（开放） | -- | schema_seed | **关键降级字段**：用于区分 vision claim vs prototype evidence vs peer-reviewed evidence | §1 (行 61–69), §3.4 (行 405–417), §4.3 (行 696–697, 714–718) | 迁移"来源类型 → 主张强度"映射 |

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel.affects` | tree-C 中的 challenge（C1–C5） | `Affects:`（多对多） | tree-B 中的 stack component | ⊆ {Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next} | §4.6 OQ7–OQ14 未填，记为 unknown | §4.1 行 594；§4.2 行 645；§4.3 行 681；§4.4 行 728；§4.5 行 761 | 形成 challenge × component 覆盖矩阵；可量化"哪个 stack 层被最多 challenge 关联" |
| `rel.depends_on` | tree-B 中的 stack component | "depends on / interfaces with" | 同 tree-B 其他 component 或 FMware | 各层不同 | 缺失视为未声明依赖 | §3.2 (Teammate→Compiler, 行 311–312)；§3.3 (IDE→Compiler+Teammate, 行 361–362)；§3.4 (Compiler→FM.next, 行 381)；§3.5 (Runtime→FMware, 行 437)；§3.6 (FM.next→Compiler.next, 行 495–496) + 结论段 (行 848: "IDE.next largely depends on all other components") | 候选"stack 依赖拓扑"启发 |
| `rel.inspired_by` | tree-B / tree-C 的设计选择 | "draws inspiration from / draws analogy" | 外部理论或既有研究 | {TDD [19,20], ToM [17,103], Bloom [21], SBSE [39], continual learning [101], Voyager [100], Sculley [87], InstructLab [51,91], phi family [15], SWEBOK [106]} | 缺失视为纯作者构造 | §3.3 (行 372–374 TDD)；§4.1 (行 599–603 ToM)；§3.2 (行 332–335 Bloom)；§4.2 (行 653 SBSE)；§4.3 (行 708–710 continual learning, Voyager)；§3.6 (行 547–548 Sculley)；§3.6 (行 524 InstructLab)；§3.6 (行 493–494 phi family)；§3.6 (行 495–496 SWEBOK) | 候选"愿景 anchored to 既有理论"链路 |
| `rel.exemplified_by` | tree-C / tree-B | "examples / early glimpses" | 外部商业 / 开源工具 | tree-C: GitHub Copilot [67], Claude Code [11], Codex CLI [74], Gemini Code Assist [3], Q Developer [1], Tabnine [6], Cline [26], Aider [8], Devin [27], SWE-agent [112], OpenHands [105], TRAE [93];  §5: Lovable [62], Base44 [18], Replit [84], Bolt.new [90], V0 [99] | 缺失视为无举例 | §1 行 33–34；§2.3 行 222–225；§5 行 851–853 | **快速漂移风险字段**：必须按官方来源记日期 |

`★ Insight ─────────────────────────────────────`
- `Affects:` 这条关系边是本篇 schema 里**唯一可严格机械化**的关系字段——作者在 §4 引言段已经把它写成模板的第二个字段，而每个 §4.1–§4.5 都严格遵守。这是 Paper2 维度模式可以直接借用的"显式关系字段先例"。
- 反过来，§4.6 的 OQ7–OQ14 故意省略了 `Affects:` 与 `Our vision:`——这本身就是一个"作者降级"信号：尚未成熟的 OQ 不强行填全表。这对 Paper2 的 candidate finding 台账也是好启发：未成熟项允许字段缺失，但缺失语义必须显式（这里是"作者尚未发展完整 vision"）。
`─────────────────────────────────────────────────`

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段 / 统计表支持的"内部统计观察"（极少）

- **5 个 stack component**（封闭枚举，分母=5）
- **6 个主 challenge + 14 个 OQ**（作者声明的 snapshot，分母=20，但 "not exhaustive"，分母不严格）
- **challenge × component 覆盖矩阵**：C1→{IDE,Teammate}，C2→{Compiler,Teammate}，C3→{Runtime}，C4→{Compiler,Teammate}，C5→{Teammate+all FMware}。Teammate.next 被 4/5 主 challenge 影响（明显高频）；Runtime.next 被 1/5。
- **作者引用 [1]–[117]**：共 117 条，其中作者团队 / 同生态 self-citation 至少含 [28]、[36]、[40]、[41]、[42]、[43]、[44]、[45]、[70]、[85]、[92]、[98]、[114]（≈12+/117 ≈ 10%+，**待 A2a 复核**）；这是"愿景—证据生态闭环"的潜在量化信号。

### 6.2 原文 discussion / recommendation / roadmap 提出的"候选 finding"（仅作启发）

- "AI 应主导 code-creation loop，人类聚焦 intent"（§3.1, §3.3）—— vision claim，不是 finding。
- "synthesis 应被建模为 SBSE 风格搜索 + semantic caching + self-reflection"（§3.4, §4.2）—— vision claim + 1 篇 HumanEval-Plus 初步可行性证据 [28]，不是 SLR finding。
- "curriculum > 大规模 unstructured pretraining"（§3.6）—— vision claim + 类比 InstructLab/phi，**没有直接证据**。
- "ToM-enhanced multi-agent 显著提升 intent clarification"（§4.1, 行 632–636，引 [36]）—— 单篇 companion empirical study (150 scenarios)，**不是综述证据**。
- "Runtime.next vs Ray Serve 30% latency improvement"（§4.3，引 [114]）—— 单篇 companion prototype 经验，**不可外推**。
- "RAR 在 MMLU 子集上减少 50% 高成本请求 / 保持 ~90% 质量"（§4.3，引 [98]）—— 同上。

### 6.3 对 Paper2 可迁移的方法学启发（**可迁移**）

1. **4-tuple challenge entry 模板**：`{Description, Affects, Open question, Our vision}` 可直接迁移为 Paper2 候选发现 / 路线图条目台账的字段。
2. **`Affects:` 关系字段**：把候选发现显式挂到维度模式层（component / dimension），形成可量化的覆盖矩阵。
3. **三时代 baseline 对照**：把"被审计对象 vs 替代方案"显式拆成 from_state / to_state，并附"工具引擎 / 角色 / 取向"三轴对照——这对 Paper2 比较综述方法学时是好脚手架。
4. **OQ7–OQ14 字段缺失模式**：未成熟的候选条目允许字段缺失，但缺失必须显式（"作者未发展完整 vision"），不可静默 NULL。
5. **companion-evidence 显式标签**：每条 vision 必须标注配套证据强度（empirical / prototype / industry signal / vision-only / peer-reviewed prior work）。
6. **curriculum-as-asset 类比**：FM.next 把 curriculum 视为可版本化、可观测、可迭代的知识资产——这与 Paper2 把"维度模式"视为可维护资产的论点高度同构。

### 6.4 绝不能迁移的领域结论

1. ❌ "SE 3.0 已被验证为可行" —— 作者明确说 "only time will tell"（§5 行 853）。
2. ❌ "Teammate.next / IDE.next / Compiler.next / Runtime.next / FM.next 5 层 stack 是 AI-native SE 的标准划分" —— 是单一作者团队的 vision，未被独立社区共识。
3. ❌ "RAR / Compiler.next prototype 数据可作为综述证据" —— companion paper、self-citation、prototype 规模。
4. ❌ "TRAE 75.2% SWE-Bench Verified 表示 autonomous SE 已实用" —— 作者本人在 §2.3 已显式降级。
5. ❌ "117 条参考文献是 SLR 分母" —— 没有检索 / 纳排协议。

## 7. 对现有 `review.md` 的返修建议（C/I/M 分级）

### Critical（C）

**C1. "维度树复原"主表的 6 个 `leaf-*` 节点未还原原文原生结构，是 A1-DT v2 明令禁止的"reviewer 主观套上的六叶通用模板"。**
- 位置：review.md 行 282–308（叶子维度表）。
- 现状：六个 `leaf-ai-native-se-roadmap-{scope,corpus,taxonomy,method,evidence,finding}` 全部是抽象 placeholder，且 `证据要求` / `取值空间` / `缺失值语义` 几乎是模板复制；六行内容彼此高度相似，没有反映 5 层 stack、4 字段 challenge schema 或 14 条 OQ。
- 影响：直接违反 A1-DT v2 "禁止把六个通用接口叶子替代原文 schema" 的硬约束。
- 返修动作：把 §维度树复原 / 叶子维度表替换为本审计 §3 + §4 给出的**原生 5 层 stack tree + challenge×OQ tree + era baseline tree** 与对应叶子表；现有六叶接口可保留在末尾"通用接口投影"段（review.md 行 352–363 已存在）作为跨论文投影层，**但不再当主表**。

**C2. "原文模式候选叶子映射（A1 种子）"中的 5 个 `orig-*` 占位叶子仍是抽象名词，不是论文真实节点。**
- 位置：review.md 行 312–320。
- 现状：`orig-vision-object` / `orig-stack-layer` / `orig-challenge` / `orig-roadmap-action` / `orig-boundary-risk` 取值空间写成"自由文本 + A2a 待核"。但论文实际给出了 **{SE 1.0/2.0/3.0}**（3 项封闭枚举）、**{Teammate.next/IDE.next/Compiler.next/Runtime.next/FM.next}**（5 项封闭枚举）、**OQ1–OQ14 + 4 字段 schema**（snapshot 枚举）。这些都是原文已给出的具体取值，不需要等 A2a。
- 返修动作：把 5 个 `orig-*` 升级为 `era.id`、`stack.component_name`、`challenge.id`、`challenge.template_field`、`challenge.affects`、`stack.from_state/to_state` 等具体节点（见本审计 §4），并把"取值空间"列从"自由文本"升级为本审计列出的具体枚举。`schema_seed` 状态可保留，但已可标注"枚举可见于文本，A2a 需做 PDF 版面核验"。

### Important（I）

**I1. SUMMARY 表中"样本单位 / 样本数量"字段需澄清"5 + 6+14 + 3"语义。**
- 现状：metadata.json 与 review.md §1 都正确写明非系统综述、不进入主统计池，但未给出"原生项数"的明确数字。
- 返修：在 review.md §1 快速结论卡片或 SUMMARY.md 中补一行"原生编码项：3 era + 5 stack component + 6 主 challenge + 14 OQ（snapshot, not exhaustive）"，避免读者误解为"完全没有可计量结构"。

**I2. self-citation / 生态闭环风险需量化标注。**
- 现状：review.md §2.10 与 §7.3 都提到 self-citation 风险，但没有数字。
- 返修：在 §2.10 末加一行"117 条参考文献中作者团队 / 同生态 self-citation ≈ 10%+（[28],[36],[40]–[45],[70],[85],[98],[114] 等；A2a 需精核）"。这条对 Paper2 在评估 vision 文献时的降级判定很关键。

**I3. companion evidence 强度未在主表里显式分级。**
- 现状：review.md §维度树主树（行 322–337）的"原文 schema 主树"已经引入 5 个 `dim-*-orig-*` 主干，但仍是 schema_seed；没有把每个主干对应的 companion evidence 强度（empirical / prototype / industry signal / vision-only）列出来。
- 返修：在"原文 schema 主树"表加 `companion_evidence_strength` 一列，至少分级到：(a) peer-reviewed external (e.g. [21] Bloom, [39] SBSE, [101] continual learning)，(b) author-team peer-reviewed ([70] SPICE ASE 2025, [85] Watson ASE 2025, [98] RAR ICSE SEIP 2025)，(c) author-team under-review / preprint ([28] Compiler.next, [44] agentic SE, [45] FMware, [114] Fusion)，(d) industry / commercial signal (GitHub Copilot, TRAE 75.2%, vibe coding platforms)，(e) vision-only。

### Minor（M）

**M1.** review.md 中 §3 与 §4 多处仍写 "证据锚点：`paper_content.txt` §X，Page Y--Z"。本轮全文已抽取到具体行号，建议在 A2a 时补行号锚点（e.g., 行 580–586 是 §4 引言段的 4 字段 schema 声明），便于自动化核验。

**M2.** review.md §维度树主树（行 322–337）使用了 `> [!WARNING] v1-deprecated` 把 19×3 历史审计入口标注为已弃用，这一点处理得很好；可在 v2 结论里显式承接（"本 v2 审计沿用此弃用边界"），避免后续 reviewer 再去查 v1 路径。

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-v2-001 | paper_content.txt | 摘要 + §1 | Page 1 行 8–25 + Page 2 行 61–69 | "We propose a shift... We outline... We also present a roadmap of challenges"；vision 来自 surveys+gray literature+workshop+客户+作者经验+OPEA | self_disclosed_paper_type | strong（作者自我声明 + 全文一致） | tree 类型 = vision/roadmap；非主统计池 | 否 | 仅证明类型，不证明 vision 内容 |
| EV-v2-002 | paper_content.txt | Fig. 1 + §2.1 + §3.1 | Page 2 行 91–94；Page 3 行 100–131；Page 7 行 280–302 | SE 1.0/2.0/3.0 三时代 + code/AI4SE/intent 三取向 + program-analysis/data-driven-FM/knowledge-driven-FM 三引擎 | era_baseline_schema | strong（封闭 3 枚举） | tree-A：era.id / era.code_orientation / era.tooling_engine | 是（Fig. 1 版面） | 仅迁移结构 |
| EV-v2-003 | paper_content.txt | Fig. 3 + §3.2–§3.6 | Page 7 行 250–278 + §3.2 行 313–337 + §3.3 行 343–374 + §3.4 行 375–417 + §3.5 行 418–476 + §3.6 行 477–578 | 5 层 stack：Teammate / IDE / Compiler / Runtime / FM .next，每层 from_state→to_state | stack_schema | strong（封闭 5 枚举 + 每层显式转换） | tree-B：stack.component_name / from_state / to_state / required_traits | 是（Fig. 3 版面 + Fig. 6） | 仅迁移结构 |
| EV-v2-004 | paper_content.txt | §4 引言段 | Page 13 行 580–586 | "For each challenge, we include a description, what parts of the SE 3.0 stack it affects (Figure 3), one or more open questions, and our vision regarding the solution to those questions" | challenge_template_schema | strong（作者显式声明 4 字段模板） | tree-C：challenge.template_field = {Description, Affects, Open question, Our vision} | 否 | 直接迁移 |
| EV-v2-005 | paper_content.txt | §4.1–§4.5 | OQ1: 行 595–596；OQ2: 行 647；OQ3: 行 682；OQ4: 行 699；OQ5: 行 730；OQ6: 行 764 | OQ1–OQ6 共 6 个主 OQ 文本 + Affects 标注 | challenge_instance_schema | strong（结构齐整执行） | tree-C：challenge.id ∈ {C1..C5}, OQ1..OQ6, affects | 否 | 迁移结构 |
| EV-v2-006 | paper_content.txt | §4.6 | Page 18 行 799–823 | OQ7–OQ14 共 8 条；"not meant to be extensive"；省略 Affects / Our vision | challenge_instance_open_set | medium（snapshot, not exhaustive） | tree-C：challenge.id ∈ {OQ7..OQ14} | 否 | 仅作 snapshot 启发 |
| EV-v2-007 | paper_content.txt | §4.1 / §4.3 引用 | 行 632–636 [36] ToM multi-agent；行 695–697 [114] 30% latency vs Ray Serve；行 714–718 [98] RAR 50% / 90% | 单篇 companion empirical 数据（150 scenarios; 30% latency; 50% routing / 90% quality） | companion_prototype_evidence | weak（自引用 / 单点 prototype） | challenge.our_vision.companion_evidence | 否 | 严禁外推为 SLR 证据 |
| EV-v2-008 | paper_content.txt | §1 / §2.3 / §5 | Page 1 行 33–34；Page 5 行 222–225；Page 19 行 851–853 | GitHub Copilot/Claude Code/Codex CLI/.../Devin/SWE-agent/OpenHands/TRAE/Lovable/Base44/Replit/Bolt.new/V0 等 | exemplification_signal | weak（快速漂移） | rel.exemplified_by | 否（需按官方来源记日期） | 严禁直接引用为既定事实，需配快照日期 |
| EV-v2-009 | bibtex.bib + metadata.json | -- | bibtex 行 1–10 + metadata 行 1–35 | Hassan_2026 / TOSEM / DOI 10.1145/3807901 / 2026-04-09 / arxiv 2410.06107 / CCF A / `eligible_for_statistical_synthesis=false` | bibliographic_anchor | strong | tree 根节点元信息 | 否 | -- |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| A1DT-v2-C01 | 本文为 vision/roadmap，非 SLR/SMS/tertiary/MLR/guideline；不进入主统计池，仅作 boundary_anchor + methodological seed | tree_type | tree root | EV-v2-001, EV-v2-009 | strong | boundary_anchor | 仅基于文本与作者自我声明 |
| A1DT-v2-C02 | 原生树是 era-baseline + 5 层 stack + challenge×OQ 三棵树构成的维度森林，**不是**六叶 SLR 编码树 | native_tree_type | tree-A + tree-B + tree-C | EV-v2-002, EV-v2-003, EV-v2-004, EV-v2-005 | strong | schema_seed | 不可迁移层名为领域标准 |
| A1DT-v2-C03 | 作者在 §4 引言段显式给出 challenge 的 4 字段模板 `{Description, Affects, Open question, Our vision}`，可作 Paper2 候选发现台账模板 | reusable_template | challenge.template_field | EV-v2-004, EV-v2-005 | strong | template_seed | 仅迁移结构，不迁移具体 OQ 集合 |
| A1DT-v2-C04 | `Affects:` 是唯一显式机械化的关系字段；challenge × component 形成 5×6 矩阵，Teammate.next 被 4/5 主 challenge 关联（高频中枢） | internal_observation | rel.affects | EV-v2-005 | medium | candidate_finding | 仅本篇内部计数；不可外推 |
| A1DT-v2-C05 | §4.6 OQ7–OQ14 显式省略 Affects / Our vision，是"未成熟项允许字段缺失但语义必须显式"的方法学启发 | methodology_seed | tree-C §4.6 | EV-v2-006 | medium | template_seed | 仅作启发 |
| A1DT-v2-C06 | companion paper evidence（[28]/[36]/[44]/[45]/[85]/[98]/[114]）密集，且多数为作者团队 self-citation，存在生态闭环风险 | risk_signal | challenge.our_vision.companion_evidence | EV-v2-007 | medium | risk_only | 严禁作为综述证据使用 |
| A1DT-v2-C07 | 117 条参考文献中作者团队 / 同生态自引用约 10%+（待 A2a 精核） | quantification_seed | bibliographic_anchor | EV-v2-007, EV-v2-009 | weak | candidate_metric | A2a 复核 |
| A1DT-v2-C08 | 商业 vibe-coding 平台与 frontier FM 名单（[1]–[8],[11]–[12],[26]–[27],[62],[67],[74],[84],[90],[93],[99],[105],[112]）属快速漂移事实，引用时必须配官方来源 + 快照日期 | quality_gate | rel.exemplified_by | EV-v2-008 | strong | citation_protocol | -- |
| A1DT-v2-C09 | 现有 review.md "维度树复原"主表的 6 个 `leaf-*` 与"原文模式候选叶子映射"的 5 个 `orig-*` 是抽象 placeholder，未还原本篇真实 5 层 stack + 4 字段 challenge schema + 14 OQ 结构，应按本审计 §7 C1/C2 返修 | review_repair | review.md §维度树复原 | EV-v2-002, EV-v2-003, EV-v2-004, EV-v2-005, EV-v2-006 | strong | review_repair_obligation | -- |

## 9. 技能使用与自我审查记录

### 9.1 技能文件读取与采纳的原则

- **`ai-research-writing-skill/SKILL.md`** ：采纳 "Evidence gate / Story gate / Citation gate / Claim gate" 等门禁；本审计对每个原文 schema 节点都要求"原文证据锚点 + 短引或释义"，对 companion paper 强度做了分级，符合 `Evidence Policy`。
- **`reviewer-guidelines.md`** ：采纳 "Universal Review Dimensions" 中的 originality / soundness / clarity / significance / reproducibility，转化为对本论文 vision 主张的"作者自我声明 vs 独立证据"的区分。
- **`reviewer-self-review.md`** ：采纳 "Five-Dimension Review + Rejection-Risk Audit"，把对 review.md 的返修建议分为 C/I/M，并显式指出"highest rejection risk = 把六叶通用接口当成原文 schema"。
- **`research-planning/SKILL.md` + `planning-prompts.md` + `output-schemas.md`** ：采纳 4-stage planning（Overall / Architecture / Logic / Configuration）的层级化思路，本审计 §3–§5 把原生树拆为 tree-A/B/C，再下推到叶子表、关系边表、统计观察表，方法学上对齐 "task dependency graph" 的层级分解。
- **`autoresearch/SKILL.md`** ：采纳 "completion is artifact-gated"，本审计明确产出可审计 Markdown，不依赖"模型说完了"判断完工。

### 9.2 reviewer 视角的本输出最高风险（3 点）

1. **未打开 PDF → Fig. 1/3/6 视觉对照未核验**：本审计声明 tree-A 三时代有 3 个完整枚举 + 三个 3 项子轴（取向、引擎、人类角色），但具体 bullet 顺序与 Fig. 1 的视觉对照可能与文本提取有出入；主线程合并时应执行 §A.4 中 `cmd-visual-check`（人工 PDF 复核）后再升级为"已核验"。
2. **OQ 编号体系是 snapshot 而非封闭枚举**：作者明确 "not exhaustive"。本审计把 OQ1–OQ14 写为"snapshot 枚举"，但下游 reviewer 可能误读为封闭分母。主线程在写 SUMMARY 或 paper2 引用时需要保持这个 snapshot 标签。
3. **self-citation 比例 ~10%+ 的定量数字未精核**：本审计基于人工目测 [28]/[36]/[40]–[45]/[70]/[85]/[92]/[98]/[114] 给出约 12+/117。主线程合并前应严格按 author affiliation + Huawei CSE / Queen's / York 团队成员名单精核，再写入 review.md I2 项。

### 9.3 是否 blocked / timeout / 文件缺失

- 无 blocked、无 timeout、所有必需文件可读。
- 唯一未做的动作：未打开 `paper.pdf`（任务允许跳过，已在 §0 与 §1 显式说明，并在 A.4 列为 `needs_manual_check`）。
- 所有 7 个技能 / 指南文件均成功读取并采纳。

---

**审计结论**（本任务自包含，不引用先前消息）：

- paper 类型 = **vision / roadmap**，与 metadata.json 一致；**不进入主统计池**，仅作 `roadmap_boundary_anchor + methodological_seed + candidate_heuristic`。
- 原生维度树 = **维度森林**（era baseline tree + 5 层 stack tree + challenge×OQ tree），而**不是** SLR 编码树；其中 4 字段 challenge 模板与 `Affects:` 关系边是对 Paper2 最有迁移价值的 schema 结构。
- 总体判定 = **needs repair**：现有 review.md 的 §1–§4 与"通用接口投影"段叙述正确，但"维度树复原"主表的 6 个 `leaf-*` 与"原文模式候选叶子映射"5 个 `orig-*` 仍是抽象占位，未还原本篇真实结构，需按 §7 C1 / C2 返修；I1–I3 与 M1–M2 为加固项。
