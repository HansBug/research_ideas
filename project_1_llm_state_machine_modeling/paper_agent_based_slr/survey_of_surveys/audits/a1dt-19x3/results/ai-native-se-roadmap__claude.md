# ai-native-se-roadmap · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude（PR #135 / paper2-a1 维度树复原子 PR 子代理；仅审计，不修改仓库文件，不 push，不 gh comment）
- 是否读取 `$ai-research-writing-skill`：是。读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`；`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` 仅按需查阅 SKILL.md 内引用的 claim-evidence、reviewer gate、citation-evidence 口径。
- 是否读取 `$research-planning`：是（路径 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`，并按需读取 `references/planning-prompts.md` 中“问题陈述—贡献—评估”三联结构）。
- 是否读取 `$oh-my-codex:autoresearch`：是（路径 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`），采用其“证据链—复核窗口—reviewer C/I 分级”口径与本仓库 CLAUDE.md §“学术研究仓库 Review 口径规范”一致对齐。
- 是否完整阅读 `paper_content.txt`：是。全文 1146 行；覆盖摘要、§1 Introduction、§2 SE 2.0 critique（含 §2.1/§2.2.1/§2.2.2/§2.2.3/§2.3）、§3 SE 3.0 vision（含 §3.1 principles、§3.2 Teammate.next、§3.3 IDE.next、§3.4 Compiler.next、§3.5 Runtime.next、§3.6 FM.next + curriculum recipe + “Are knowledge-driven FMs all we need?”）、§4 Challenges（§4.1--§4.5 完整 Description/Affects/Open Question/Our Vision 四元模板 + §4.6 OQ7--OQ14 + Fig. 7）、§5 Conclusion、References（前若干条交叉核对）。同时核对 Figures 1--7 的文字说明。
- 是否核对 `paper.pdf`：否，仅以 `paper_content.txt` 文本与 `bibtex.bib`、`metadata.json` 交叉核验；Fig. 3 stack 排版、Fig. 5/7 截图细节、表格未通过 PDF 视觉核对。需要 A2a 补 visual_check。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

原文 **没有** SLR/SMS 形式 RQ，也 **没有** 抽取表、检索式、纳排表、coding scheme、质量评价 rubric 或 PRISMA flow。其声明为 vision + challenge roadmap 范式：

- 自我定位（摘要、§1、§5）：提出 SE 3.0 愿景；描述其核心原则；给出 SE 3.0 技术栈五组件；列出实现 SE 3.0 必须克服的挑战路线图；触发社区讨论。
- 五项贡献声明可读为隐式 RQ：
  - C1 SE 1.0/2.0/3.0 历史分期判断（§2.1, Fig.1）。
  - C2 SE 2.0 三类核心局限 + autonomous SE 边界（§2.2.1/§2.2.2/§2.2.3 + §2.3）。
  - C3 SE 3.0 三原则：intent-centric / conversation-oriented / AI-native / knowledge-driven（§3.1）。
  - C4 五组件技术栈（Fig.3 + §3.2--§3.6）。
  - C5 五大挑战 + OQ1--OQ14 路线图（§4.1--§4.6）。

### 2.2 方法 / 证据链组织

原文 §1 page 2 显式给出五类证据来源（属可枚举、闭合的 evidence source 集合）：

1. surveys of academic and gray literature（无 protocol）。
2. in-depth discussions with industrial and academic leaders（SEMLA 2024 / FM+SE Vision 2030 / FM+SE Summit 2024 / AIware 系列 / Ray Summit 2024 / SE 2030 workshop @ FSE 2024）。
3. meetings with customers and internal development teams。
4. authors’ own R&D experience with FMware + SE 3.0 stack。
5. interactions with OPEA alliance partners（Intel、AMD、RedHat、HuggingFace、SAP 等 40+ 公司）。

无 search string、database list、inclusion/exclusion criteria、quality assessment rubric、coder/data extractor 人数、kappa、PRISMA flow、coding scheme。

### 2.3 显式 schema / 模板 / taxonomy / 图表

可被精核的、原文 **明确给出的闭合结构**：

| 原文显式结构 | 闭合值域 | 证据锚点 |
|---|---|---|
| SE era 三段论 | {SE 1.0, SE 2.0, SE 3.0} | Fig.1, §2.1, §3.1 |
| SE 2.0 限制类别 | {High cognitive overload, Inefficient & ineffective model training, Suboptimal code quality / additive bias, Autonomous SE 边界限制} | §2.2.1/§2.2.2/§2.2.3/§2.3 |
| SE 3.0 核心原则 | {intent-centric, conversation-oriented, AI-native, knowledge-driven} | §3.1 |
| SE 3.0 技术栈组件 | {Teammate.next, IDE.next, Compiler.next, Runtime.next, FM.next} | Fig.3, §3.2--§3.6 |
| 每个组件的 from_state → to_state | 二元枚举 | Fig.3 标签 + 各小节首句 |
| Runtime.next 属性 | {SLA-aware, Uni-clusters, Edge-computing extension} | §3.5 |
| Challenge 模板（四元字段） | {Description, Affects (stack components), Open Question id+text, Our Vision} | §4.1--§4.5 反复出现 |
| Open Question 集合 | OQ1--OQ14（14 个，闭合） | §4.1--§4.6 |
| 每个 OQ 的 affected stack component | 五组件中的若干 | §4.1--§4.5 “Affects” 行 |
| Challenge maturity（隐式） | {concept, prototype with companion paper, empirical_initial (HumanEval-Plus / MMLU subset), industry signal, open_question_only} | §3.4, §3.5, §4.2, §4.3 |
| Curriculum recipe 步骤 | {define objectives & scope, identify domain/subdomain, hierarchical taxonomy, leaf examples/templates/evaluation rules, synthetic data via teacher FM, consistency testing, iterative refinement / pilot / community contributions, data-flywheel observability-driven revision} | §3.6 reference recipe |
| Evidence source 类别 | 见 §2.2 五类 | §1 page 2 |
| 图集合 | Fig.1--Fig.7（7 张） | 全文 |

### 2.4 finding / gap / recommendation 的形成方式

不是从字段统计推导，而是 **作者经验 + 引文 + companion works** 直接断言。典型链路：

- limitation → affected stack → open question → our vision → companion paper / prototype evidence（如 Compiler.next [28]、Runtime.next/FMArts [114]、ToM multi-agent [36]、RAR [98]）。
- 部分 vision 由 HumanEval-Plus、MMLU 子集、real-world deployment 提供 “initial / preliminary feasibility evidence”，不是系统综合。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过（弱通过） | `[dim-...-root]` 写为 “Towards AI-Native Software Engineering (SE 3.0) 的研究目标 / RQ / 贡献声明”，与原文标题、摘要、§5 概括一致；但根节点未直接表达“vision/roadmap，无 RQ”这一关键边界，仅在结论卡和 tree_type 中标注。 | M |
| 主干分支是否覆盖原文 schema | 部分覆盖（关键缺失） | 当前 b1--b5 = {SE 3.0 愿景对象 / 技术栈层级 / AI-native challenge / action roadmap / boundary risk}。漏掉了原文中可被精核的两条骨架：(a) **SE era 三段论与 SE 2.0 critique**（§2.1/§2.2 是全文 1/3 篇幅，且明确闭合 4 类 limitation）；(b) **SE 3.0 核心原则 vs. SE 3.0 技术栈** 应是两条不同分支，当前合并到 b1 / b2，把 “原则” 这一具名节点丢失。另外 “action roadmap” 与 “AI-native challenge” 在原文是同一 §4 内的 Open Question/Our Vision，二者并非独立 sibling，强行拆开会造成 OQ 与 vision 被双父节点重复挂载。 | I |
| 叶子维度是否足够具体 | 不足 | 当前 6 个 `leaf-*` 全部是 survey-of-surveys 通用接口（scope / corpus / taxonomy / method / evidence / finding），定义、取值空间、缺失值语义都是模板复制，没有承接原文已闭合的 {3 limitations、4 principles、5 stack components、3 runtime qualities、4-tuple challenge template、14 OQ、8 curriculum recipe 步骤} 等结构。原文模式候选叶子表只给了 5 条 `schema_seed`，且每条取值空间均写成“开放文本 / 待 A2a 核对”，丢弃了原文显式给出的封闭枚举（如 5 个 stack component 名称是原文白纸黑字给出的）。 | I |
| 取值空间是否可执行 | 不可执行 | 通用接口叶子的“取值空间”是元规范文本（如“完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable”），不是原文可统计字段。`schema_seed` 叶子的“取值空间”也全部是“先保持开放文本 / 由 A2a 复核”，违反了即使在 seed 阶段也应把已经可枚举的封闭集合（5 stack components / OQ1--OQ14 / 3 SE eras / 3 Runtime qualities）写明这一可执行性要求。 | I |
| 关系边是否缺失 | 缺失 | 原文存在多条 **强关系边** 但维度树未刻画：(a) `challenge.affects → stack_component`（多对多）；(b) `open_question.id → challenge.id`（多对一）；(c) `stack_component.from_state → component.to_state`（每组件两个端点）；(d) `vision_principle → stack_component`（驱动关系）；(e) `evidence_anchor → companion_paper`（自引用 / 生态闭环风险）。这些关系是 Paper2 A2a/A2b 做 finding-path 时所必需的。 | I |
| 统计用途 / 分母是否正确 | 通过 | 全部维度声明 `不进入主统计池：vision/roadmap` 并标注 boundary_anchor / schema_seed，未误把 OQ1--OQ14 等当成 finding 频次统计；与文库 SUMMARY 和 patterns/pattern-field-schema.md 中 vision/roadmap 不计入主统计池的约束一致。 | 通过 |
| 候选 finding 路径是否完整 | 不完整 | review §3 表（六类 pattern）已经给出 finding 降级口径，但维度树本体的 “统计与候选发现链路” 表只列了 3 行，未把 “limitation → affected stack → OQ → vision → companion evidence → maturity” 这一原文最有迁移价值的候选 finding 路径模板化。这与 §6 第 1/7 条文字描述（OQ 模板可用于候选发现台账）存在自我不一致。 | I |
| A.1--A.4 证据链是否足够 | 部分不足 | A.1 三条来源齐全；A.2 仅 4 条 EV，所有页码字段都是 “摘要 / 引言页；待 A2a 精确页码复核”，未利用 paper_content.txt 已经给出的页码标记（如 Page 2 evidence source 列表、Page 3 Fig.1、Page 9 Runtime.next 三属性、Page 13--19 challenge 四元模板）来锚定。`需要原文版面核验` 字段虽然为 true，但许多事实并不真的需要打开 PDF（如组件名、OQ 编号、SE era 名称），可在本轮就 verified。当前所有 EV 强度都是 `not_verified`，把可文本核验的事实和真正需要图像核验的事实混在一起；A.3 把 7 条 leaf_definition 全部挂到 “weak / not_verified” 上，也是同一问题。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过（边界守住） | tree_type / finding-boundary / transfer 三条结论统一标 weak、boundary_anchor、schema_seed，不含 “该字段已被验证” 或 “可计入领域分布” 这类越权升级；§7 风险表把 “过度升级风险” 列为第 1 风险。无 C 级越权问题。 | 通过 |

## 4. 建议维度树骨架

建议把当前 b1--b5 重新组织为 6 条骨架分支，与原文 §2/§3/§4 顺序对齐，并把已经显式闭合的枚举写入叶子取值空间。骨架如下（仅给结构，不要求 PR 内立刻替换，A2a 必须用此进入精核）：

```text
[dim-ai-native-se-roadmap-root] Towards AI-Native Software Engineering (SE 3.0):
                                A Vision and a Challenge Roadmap
├── B1 SE era 历史分期 (§2.1, §3.1, Fig.1)
│   └── L1.1 era_label ∈ {SE 1.0, SE 2.0, SE 3.0}（闭合）
│       证据：Fig.1 三列；缺失值语义=不适用；统计用途=不进入主池；分母=N/A。
├── B2 SE 2.0 critique (§2.2/§2.3)
│   ├── L2.1 limitation_category ∈ {cognitive_overload, inefficient_ineffective_model_training,
│   │       suboptimal_code_quality_additive_bias, autonomous_SE_boundary}（闭合 4）
│   ├── L2.2 affected_actor ∈ {human_developer, frontier_FM, training_data_pipeline,
│   │       autonomous_SE_benchmark}
│   └── L2.3 supporting_evidence_type ∈ {author_observation, cited_empirical_study,
│           commercial_tool_snapshot, benchmark_limitation_note}
├── B3 SE 3.0 核心原则 (§3.1)
│   └── L3.1 principle ∈ {intent_centric, conversation_oriented, AI_native, knowledge_driven}
│           (闭合 4)
├── B4 SE 3.0 技术栈组件 (Fig.3, §3.2--§3.6)
│   ├── L4.1 component_name ∈ {Teammate.next, IDE.next, Compiler.next,
│   │       Runtime.next, FM.next}（闭合 5）
│   ├── L4.2 from_state（每组件一字符串，例如 Teammate.next: "static / impersonal coding assistant"）
│   ├── L4.3 to_state（每组件一字符串，例如 Teammate.next: "self-evolving personalized mentor"）
│   ├── L4.4 required_capability（开放文本枚举，按各小节抽取）
│   ├── L4.5 Runtime.next 子属性 ∈ {SLA-aware, Uni-clusters, Edge-computing extension}（闭合 3）
│   └── L4.6 companion_evidence_ref（{[28], [114], [45], [36], [98] ...}，闭合于参考文献集合）
├── B5 Challenge / Open Question (§4.1--§4.6)
│   ├── L5.1 challenge_id ∈ {C4.1, C4.2, C4.3, C4.4, C4.5}（5 大挑战，闭合）
│   ├── L5.2 challenge.affects → 多对多映射到 L4.1
│   ├── L5.3 open_question_id ∈ {OQ1, OQ2, ..., OQ14}（闭合 14）
│   ├── L5.4 open_question_text（文本，原文逐字句）
│   ├── L5.5 our_vision_summary（开放文本，按 §4.* "Our vision" 段抽取）
│   ├── L5.6 maturity ∈ {concept_only, companion_prototype, empirical_initial (e.g. HumanEval-Plus,
│   │       MMLU subset, real-world deployment slack), industry_signal, open_question_only}
│   └── L5.7 self_citation_risk ∈ {high (author companion work), medium (related group work),
│           low (independent cited work), none}
└── B6 Evidence base & boundary risk (§1 page 2, §5)
    ├── L6.1 evidence_source ∈ {gray_and_academic_literature_surveys, in_depth_discussions,
    │       customer_team_meetings, authors_R&D_experience, OPEA_alliance_interactions}（闭合 5）
    ├── L6.2 evidence_protocol_present ∈ {no_search_string, no_inclusion_criteria,
    │       no_quality_rubric, no_PRISMA, no_extraction_form}（全部 = no；说明非 SLR）
    ├── L6.3 fast_drift_risk ∈ {model_name_drift, benchmark_leaderboard_drift,
    │       commercial_tool_availability_drift}
    └── L6.4 allowed_use_in_paper2 ∈ {background, schema_candidate, candidate_finding (with
            researcher approval), final_finding_forbidden}
```

补充关系边（应在 A.2 证据账本中显式记录、A2a 精核时验证）：

1. `challenge[i].affects → stack_component[j]`（多对多，来自每个 §4.* "Affects" 行）。
2. `open_question[k] → challenge[i]`（OQ1--OQ6 一一挂到 C4.1--C4.5；OQ7--OQ14 挂到 §4.6 generic）。
3. `stack_component[j] → companion_paper[r]`（如 Compiler.next → [28]，Runtime.next → [114]，FMware → [45]，ToM → [36]，RAR → [98]）。
4. `principle[p] → stack_component[j]`（如 intent-centric 驱动 IDE.next、Compiler.next；knowledge-driven 驱动 FM.next）。
5. `Runtime.next → {SLA-aware, Uni-clusters, Edge-extension}`（一对多，闭合 3）。

为什么必须升级：当前“原文模式候选叶子映射”仅 5 条且全部 `not_verified`，把原文已经白纸黑字给出的闭合枚举（5 stack components、3 SE eras、4 limitation categories、4 principles、3 Runtime qualities、14 OQ id、challenge 四元模板字段）写成了“开放文本 / 待 A2a 复核”，等于把可立即 verified 的事实人为延后。这会让 A2a 在 Paper2 主线上 **无法用 ai-native-se-roadmap 这篇做 roadmap/challenge 字段先验**，浪费 boundary_anchor 价值。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支扩到 6 条，区分 SE era / SE 2.0 critique / SE 3.0 principle / stack components / challenge & OQ / evidence base，并把 “action roadmap” 合并到 challenge.OQ.our_vision 而非独立 sibling | §“维度树结构” / “根问题 / RQ 到主干分支映射” | 用上面 §4 给出的 B1--B6 骨架替换 b1--b5；保留现有 schema_seed 降级口径不变 | §2.1, §2.2, §3.1, §3.2--§3.6, §4.1--§4.6 | I |
| 把已闭合枚举写入候选叶子的取值空间，而不是“开放文本 / 由 A2a 复核” | §“原文模式候选叶子映射（A1 种子）” | 至少 L1.1（SE era 三段）、L2.1（4 limitation）、L3.1（4 principle）、L4.1（5 stack 组件名）、L4.5（3 Runtime 属性）、L5.3（OQ1--OQ14）、L5.1（C4.1--C4.5）、L6.1（5 evidence source）可在本轮就标 `verified_in_text`，而非 `not_verified` | Fig.1, Fig.3, §2.2.1--§2.2.3, §2.3, §3.1, §3.2--§3.6, §4.1--§4.6, §1 page 2 evidence-source 列表 | I |
| 在维度树中显式刻画 5 条关系边（见 §4 关系边表） | §“维度树结构” 下方新增 “关系边表” | 至少包括 challenge.affects→component、OQ→challenge、component→companion_paper、principle→component、Runtime→{SLA-aware/Uni-clusters/Edge-ext} | §4.1--§4.5 “Affects” 行；§3.2--§3.6 companion 引用；§3.5 三属性 | I |
| 新增 “候选发现路径模板” 子节 | §“统计与候选发现链路” 表后新增一段 | 把 “limitation → affected stack → OQ → vision → companion evidence → maturity → self_citation_risk → allowed_use_in_paper2” 作为唯一允许的候选发现路径写明；明确禁止跳过 maturity / self_citation_risk 直接进入候选发现 | §3.4, §3.5, §4.2, §4.3, §5 + §7 风险表 | I |
| A.2 EV 表细化页码与证据强度 | §A.2 维度树证据账本 | (a) EV-001 添加锚点 “Page 1 摘要 + Page 2 §1 evidence source 列表”；(b) 新增 EV 行覆盖 Fig.1 era / Fig.3 stack / §3.5 Runtime 三属性 / §4.1--§4.5 challenge 四元模板 / §4.6 OQ7--OQ14；(c) 把仅基于原文文本即可 verify 的 EV 标 `text_verified`（弱→中），把真正需要 PDF 图像核验的 EV 单列并保留 `needs_pdf_visual_check=true` | paper_content.txt 全文已含明确 Page 标记 | I |
| 在 A.3 结论-证据映射中拆分 “文本可核验结论” 与 “需要 PDF 视觉核验结论” | §A.3 | 当前 7 条 leaf_definition + tree_type 全部挂 weak / not_verified；建议把基于文本即可 verify 的 5 条（leaf_taxonomy、leaf_method、leaf_evidence、tree_type、transfer）升级为 `text_verified` 中等强度，把依赖 Fig.3 / Fig.5 / Fig.6 / Fig.7 的视觉版面结论保留 `needs_pdf_visual_check` | §A.2 同步修改 | I |
| 删除或弱化 “可迁移字段树” 历史草稿中的 `roadmap_item` 大树，与正式维度树合并去重 | §“历史草稿（已迁移，不作事实真源）” | 历史草稿已经标注非事实真源，可保留；但建议加一行注释：“以下字段在新骨架中分别落到 B2 / B4 / B5 / B6，未落到任何主干的字段（如 `temporal_stability`）合并入 L6.3 fast_drift_risk” | §“历史草稿” | M |
| 根节点 metadata 增加 “no_systematic_protocol” 标记 | §“根问题 / RQ 到主干分支映射” | 在 [dim-...-root] 描述中显式加上 `protocol_present=no (no search string / no inclusion criteria / no PRISMA / no extraction form / no quality rubric)`，避免下游误读 | §1 page 2 evidence-source 列表 + §5 “only time will tell” | M |
| 修正 §6 “对 Paper2 story / method 的启发” 第 7 条与维度树结论的不一致 | §6 | 当前 §6 第 7 条说 “OQ 模板可用于候选发现台账”，但维度树中并未把 challenge 四元模板（Description/Affects/OQ/Our Vision）作为叶子；建议把模板字段挂到 B5 的 L5.1--L5.7，保持自洽 | §4.1--§4.5 反复出现的四元模板 | M |

## 6. C/I/M 结论

- C：无。
  - 没有把 vision/roadmap 升级为系统综述结论；
  - 没有把 not_verified 当成可统计 finding；
  - 没有破坏 Paper2 学术目标或证据链根基。
- I：6 条。
  - 主干分支未覆盖原文 schema（SE era / SE 2.0 critique / SE 3.0 principle 三处缺失）；
  - 叶子维度仍为通用接口，未承接原文显式闭合枚举；
  - 候选叶子取值空间全部写为 “开放 / 待 A2a”，把可立即 verified 的事实人为延后，会降低 ai-native-se-roadmap 作为 boundary_anchor 的可迁移价值，可能使后续 A2a 难以基于本 PR 直接精核；
  - 缺关系边（challenge.affects→component / OQ→challenge / principle→component / component→companion_paper / Runtime→3 属性），将影响 A2b finding-path 重建；
  - A.2 证据账本所有页码字段一律 “待 A2a 精确页码复核”，把可文本核验事实与需视觉核验事实混淆；
  - §6 第 7 条与维度树本体不自洽（OQ 模板未真正落入叶子）。
- M：3 条。
  - 历史草稿大树与正式维度树未做字段合并去重；
  - 根节点未显式标记 `no_systematic_protocol`；
  - 6 个通用接口叶子的“迁移边界”“证据要求”等字段全部为模板复制文本，可读性较差，但不影响 boundary_anchor 学术安全。

### 最终建议

**NEEDS FIX（仅需修复 I 级，不阻塞 Paper2 主线，但当前 PR 不应被视为 “维度树复原已完成” 的事实真源）**。

理由（按本仓库 CLAUDE.md §“学术研究仓库 Review 口径规范” 与 autoresearch reviewer 口径）：

1. 当前维度树已经守住了 vision/roadmap 不进入主统计池的最关键学术安全线，因此不存在 C 级。
2. 但若以本 PR 的 b1--b5 骨架进入 A2a，roadmap/challenge 这类对 Paper2 报告结构最有迁移价值的字段（challenge 四元模板、OQ1--OQ14、5 stack components、3 Runtime 属性）将以 “待 A2a 从零核对” 的形态进入下游，意味着本 PR 的 boundary_anchor 学术贡献近乎 0，违反 ai-research-writing-skill 的 Evidence gate 与 autoresearch 的 “可立即 verified 的事实必须在当前轮 verified” 原则。
3. 因此把 I 级 6 条解决后即可 READY；否则建议在 PR body 中显式声明 “本 PR 仅为通用接口层降级骨架，原文 schema 复原推迟到 A2a”，并把这条限制写入 SUMMARY 的待跟进项，避免后续 agent 误把通用接口当成原文 schema 复原完成态。
