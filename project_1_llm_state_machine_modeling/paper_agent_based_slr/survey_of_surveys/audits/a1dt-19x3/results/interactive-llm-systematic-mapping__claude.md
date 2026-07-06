# interactive-llm-systematic-mapping · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude（PR #135 / paper2-a1 维度树复原子 PR 子代理；只审计，不改动仓库文件，不 push，不 gh comment，不开 sub-subagent）。
- 是否读取 `$ai-research-writing-skill`：是。读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`；按需查阅 `references/paper-story.md`（贡献-claim-evidence 三联）、`references/reviewer-guidelines.md`（reviewer gate / claim gate / citation gate）、`references/reviewer-self-review.md`（reviewer self-bias 检查）。
- 是否读取 `$research-planning`：是。`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`，采用其"问题-贡献-评估边界"口径。
- 是否读取 `$oh-my-codex:autoresearch`：是。`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`，与本仓库 CLAUDE.md "学术研究仓库 Review 口径规范" C/I/M 对齐。
- 是否完整阅读 `paper_content.txt`：是。原文仅 4 页（约 280 行），逐页通读：Page 1（abstract + §1 Introduction + 动机与 human-in-the-loop 立场）；Page 2（Fig.1 标题 + §2.1 Establishing a need + §2.2.1 Search 三 agent + §2.2.2 inclusion/exclusion 开篇）；Page 3（§2.2.2 续 + §2.3 inductive/deductive coding + §2.4 Visualization + §2.5 Reporting + §3 Reflections + Data availability）；Page 4（References [1]–[10]）。同时核对 §1 五项动机、§3 两条研究方向。
- 是否核对 `paper.pdf`：本轮未独立打开 PDF；但 `review.md` 自述已回原文核对 Fig. 1（Page 2），且 Fig. 1 内容已被 `paper_content.txt` Page 2 文本以"Fig. 1. The mapping process with LLM support"和 §2.1–§2.5 完整覆盖，可文本级交叉确认。除 Fig. 1 外原文无表、无统计图，无需进一步视觉核验。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文 **没有正式 RQ 表**，且明确把研究定性为 *solution proposal*。其等价问题与贡献声明可从摘要与 §1 末段读出：

- 目标（Abstract Objective）：讨论在 mapping study 流程各步使用 LLM 的可能性与下一步行动方向。
- 方法（Abstract Method）：solution proposal，作者迭代设计并讨论。
- 结果（Abstract Results）：为 mapping process 各步提出 strategies、agents 与 prompting 策略。
- 结论（Abstract Conclusion + §3 末）：呼吁社区共建 holistic solution；提出两条研究方向：(R1) 改进并评估各单步骤；(R2) 构建端到端 prototype。

隐式贡献声明可枚举为：
- C1 把 Petersen 2015 mapping guideline 的 6 个阶段映射到 "user input / LLM output / human refinement" 三元结构（Fig. 1）。
- C2 在 Search 阶段提出三个具名 agent：Keyword Identification Agent / Semantic Search Agent / Search Strategy Agent。
- C3 在 Data extraction & classification 阶段区分 inductive vs deductive coding，并指出 "完整 PDF 作为输入" 的机会。
- C4 在 Reflections 中给出 4 类 validity / 限制（publication bias、LLM 演化漂移、SE 外证据迁移、概念性方案未评估）。
- C5 列出 complementary tools（LangSmith、WebVoyager、LIDA、BERTopic、DSPy）与相关文献支撑。

### 2.2 原文方法流程 / 检索 / 纳排 / 抽取 / 编码 / 统计 / finding 形成方式

- **本文自身不执行系统检索**：无搜索库、无搜索式、无筛选分母、无 PRISMA flow、无质量评价 rubric、无 inter-rater、无 Data availability（明示 "No data was used"）。
- **finding 形成方式**：narrative discussion 直接引用 10 篇相关文献（[1]–[10]）作为可行性或风险旁证；不是由作者自身字段抽取统计得到。例如 Wang et al. [5] 提供 GPT-generated query recall 下降证据；Huotala et al. [6] 提供 GPT-4 vs GPT-3.5 与 One-shot/Few-shot/CoT prompting 证据；Guo et al. [7] 提供 high recall 仍是问题的证据；Wang et al. [8] 提供 BERTopic / interdisciplinary topic modeling 证据；Petersen [9] 提供 case study judging 证据。
- **统计/分析**：无独立统计。

### 2.3 原文显式 extraction form / classification schema / taxonomy / coding scheme / 模型 / 图表 / roadmap / quality rubric

可被精核的、原文**白纸黑字**给出的闭合结构（这些都可以、并且应当在 A1-DT 阶段就写出闭合取值空间，而不是留给 A2a）：

| 原文显式结构 | 闭合取值空间 | 证据锚点 |
|---|---|---|
| Mapping process 阶段（来自 Petersen et al. [4]）| {Establishing a need for the map, Study identification: Search, Study identification: Inclusion & exclusion, Data extraction and classification, Visualization, Reporting} | Fig. 1 + §2.1–§2.5 全部 |
| 每阶段三元字段（Fig. 1 通用结构） | {user_input, interactive_refinement, LLM_output} | Fig. 1 + §1 Introduction 末段（"researcher should have an initial idea … in order to validate the outputs"）|
| Search 阶段三 agent | {Keyword Identification Agent, Semantic Search Agent, Search Strategy Agent} | §2.2.1 Page 2，编号 1/2/3 列表 |
| Search 阶段 search-intent 层级 | {concept_level, subtype_level, supertype_level}（3D printing 例） | §2.2.1 Page 2 末（"conceptual term level … subtypes … supertypes"）|
| Search 阶段 reproducibility 立场 | {Boolean (reproducibility), semantic (RAG), citation pearl growing} | §2.2.1 Page 2 |
| Inclusion/Exclusion 论证组件 | {classification problem, transparency, traceability, human oversight, rationale, citations, evidence fragments, chain-of-thought prompting, continual learning system, DSPy prompt optimization} | §2.2.2 Page 2–3 |
| Data extraction coding mode | {inductive, deductive} | §2.3 Page 3，编号 1/2 列表 |
| Inductive coding pipeline 步骤（封闭顺序） | {generate_embeddings, reduce_dimensions, cluster_embeddings, create_topic_representations} | §2.3 Page 3，"create embeddings, reduce dimensions, cluster embeddings, and create topic representations" |
| Deductive coding 技术 | {one_shot_prompting, few_shot_prompting, RAG_full_pdf, document_splitting} | §2.3 Page 3 |
| Reading depth 转换 | {adaptive_reading_depth → full_paper_input} | §2.3 Page 3 开篇 |
| Visualization 工具/方法 | {ChatGPT source-code-and-chart, LIDA, BERTopic landscape} | §2.4 Page 3 |
| Reporting 任务 | {pattern_spotting, observation_highlight, research_gap_spotting, draft_assistance} | §2.5 Page 3 |
| Reflections / validity 类别（4 类） | {publication_bias_and_limited_studies, rapid_LLM_evolution (Claude.ai / GPT-o1 例), non-SE_evidence_transfer_to_SE, conceptual-framework-without-prototype} | §3 Page 3，"Study validity" 段 |
| Complementary tools | {LangSmith (tracing/debugging/testing), WebVoyager (gray literature / visual web search)} | §3 Page 3，"Complementary Tools" 段 |
| 研究方向（2 条，闭合） | {improve_individual_steps_with_eval, build_end_to_end_prototype} | §3 Page 3 末两条 bullet |
| Motivations for using LLMs in MSs（4 条，闭合） | {increased_paper_volume, larger_scope, additional_research_design_ideas_via_interaction, reduced_effort_for_updates} | §1 Page 1，编号 (1)–(4) |
| Reviewer prerequisites（2 条） | {educated_in_mapping_methodology, topic_expert} | §1 Page 1，"(a)/(b)" |
| 隐式关系边 | challenge↔stage、agent↔stage（search 阶段 3 agent 挂在 search）、tool↔stage、validity↔stage、citation_grounding↔inclusion/exclusion | Fig. 1 + §2 全部 |
| Quality rubric / extraction form | 无（明示 No data；solution proposal） | §3 Data availability |
| 数值结果 / 表 | 无 | 全文 |

### 2.4 finding / conclusion 如何形成

原文不存在 "字段 → 频次 → finding" 路径。其结论形成方式是：
- **design claim**（"我们建议…"、"we propose…"、"we suggest…"），主语是作者；
- **borrowed empirical evidence**（引用 [5]–[9] 的实证结果作旁证）；
- **vision statement**（"work towards a holistic solution"、"two research directions"）。

因此 finding pattern 只能进入 *candidate finding / boundary anchor* 渠道，不允许进入 Paper2 主统计池或目标领域结论池——这一点 review 已守住。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过（弱通过） | `[dim-...-root]` 写为 "On the road to interactive LLM-based systematic mapping studies 的研究目标 / RQ / 贡献声明"，与原文标题一致；但根节点未把"solution proposal / 无 RQ / Fig.1 schema"这一最核心边界刻入节点描述，仅在 tree_type 与一句话结论中标注。 | M |
| 主干分支是否覆盖原文 schema | 部分覆盖（关键缺失） | b1 "SMS 流程阶段" / b2 "LLM/agent 介入点" / b3 "researcher interaction" / b4 "traceability risk" / b5 "proposal boundary"。原文 Fig.1 的真实结构是**单一**"mapping process"骨架，其下 6 个阶段，每阶段 {user_input, LLM_output, human_refinement}。当前把"流程阶段 / 介入点 / 交互"拆成三个并列分支，反而切断了 Fig.1 的三元配对关系，使 A2a 难以重建"哪个 LLM agent 由哪个 researcher 输入触发"。此外 b4 "traceability risk" 仅捕获 inclusion/exclusion 的 rationale/citation 要求，遗漏 §3 Reflections 的 4 类 validity 中其余 3 类（model drift / non-SE transfer / no-prototype）。 | I |
| 叶子维度是否足够具体 | 严重不足 | 维度树主表的 6 个 `leaf-*` 全部是 survey-of-surveys 跨论文通用接口，定义、取值空间、缺失值语义、统计用途、迁移边界文字都是模板复制（除"语料与纳排链条"明确写 not_applicable 外），与本文 Fig.1/§2/§3 的具体 schema 没有任何 verbatim 锚接。原文模式候选叶子表只列了 4 条 `_orig-*` seed（sms-stage / llm-intervention / researcher-interaction / traceability-risk），且每条取值空间均为开放短语；遗漏的原文显式封闭枚举至少包括：(a) 6 个 mapping-process 阶段名；(b) Search 阶段 3 个具名 agent；(c) inductive vs deductive 二元；(d) inductive coding 4 步 pipeline；(e) deductive coding {one-shot, few-shot, RAG} 三元；(f) Fig.1 三元字段 {user_input, llm_output, human_refinement}；(g) §3 Reflections 4 类 validity；(h) §3 两条研究方向；(i) 复合工具集 {LangSmith, WebVoyager, BERTopic, LIDA, DSPy}；(j) §1 LLM 动机 4 条。这些都是 4 页论文白纸黑字可枚举的，不应被推到 A2a。 | **I**（接近 C 的证据链风险） |
| 取值空间是否可执行 | 不可执行 | 6 个通用 leaf 的"取值空间"是元规范文本（如"完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable"），不是 A2a 可直接对原文字段做映射的封闭集合。4 条 `_orig-*` seed 的取值空间用"研究问题、检索、筛选、分类、统计、报告等 SMS 阶段"这种概括短语，未给出 §2.1–§2.5 的 verbatim 阶段名；亦未刻画 Fig.1 三元结构。 | I |
| 关系边是否缺失 | 关键缺失 | 原文存在多条强关系边但维度树未刻画：(a) `stage → {user_input, llm_output, human_refinement}` 三元；(b) `search_stage → {keyword_agent, semantic_search_agent, search_strategy_agent}`；(c) `extraction_stage → {inductive, deductive}`；(d) `inductive → topic_modeling_pipeline (4 ordered steps)`；(e) `deductive → {one_shot, few_shot, RAG, full_pdf}`；(f) `agent / technique → {Boolean, semantic, citation_pearl_growing}` recall/precision 取舍；(g) `validity_category → affected_stage`（如 recall 风险主要影响 search 与 inclusion/exclusion）；(h) `research_direction → stage scope`（individual steps vs end-to-end prototype）。缺这些关系边，A2a 即使把候选叶子升级成已核验，也无法重建 Paper2 finding-path（如"哪一阶段的可追溯性最弱、对哪类 Open Question 影响最大"）。 | I |
| 统计用途 / 分母是否正确 | 通过 | 所有维度声明"不进入主统计池：solution proposal"并标 boundary_anchor / schema_seed；metadata.json 的 `eligible_for_statistical_synthesis=false`、`statistical_pool_exclusion_reason="solution proposal；没有已执行的系统检索、纳排与实证合成"` 与本表一致。未出现把 OQ 或 agent 数当 finding 频次统计的越权。 | 通过 |
| 候选 finding 路径是否完整 | 不完整 | "统计与候选发现链路"只列 3 行 / 仅指向 `root / leaf-taxonomy / leaf-finding`，未把原文最有迁移价值的候选 finding 路径模板化，如：`stage → human_input → llm_output → audit_evidence (rationale + citation + source_fragment) → human_override`（Fig.1 通用追溯路径）；`stage_risk → validity_category → research_direction`；`tool → stage → maturity_signal`。review §6.1 第 4 条已识别"纳排和抽取必须 source-grounded"，但未在维度树主体中固化为候选 finding 路径。 | I |
| A.1--A.4 证据链是否足够 | 部分不足 | A.1 三条来源齐全；A.2 仅 4 条 EV，全部页码字段写"待 A2a 精确页码复核"，但原文只有 4 页且 paper_content.txt 已能直接锚定：摘要+§1 位于 Page 1、Fig.1+§2.1+§2.2.1+§2.2.2 开头位于 Page 2、§2.2.2 续+§2.3+§2.4+§2.5+§3+Data availability 位于 Page 3、References 位于 Page 4。这些事实可在本轮文本级 verified，而非全部留 `not_verified`。`需要原文版面核验` 字段虽 true，但 6 个阶段名 / 3 个 agent 名 / inductive vs deductive / 4 类 validity / 2 条研究方向都是纯文本事实，无需视觉核验。当前把可文本核验的事实和真正需要图像核验的事实混在一起，弱化了 EV 强度信号。A.3 把 7 条 leaf_definition 全部 weak / boundary_anchor / not_verified，与"已回原文核对 Fig.1"自述（review §"阅读状态"）存在内部不一致。`[cmd-...-visual-check]` 标 `needs_manual_check`，但 Fig.1 之外原文没有图表需要视觉核验。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过（边界守住） | tree_type / migration_boundary / candidate_finding / source_schema_candidate 四条结论统一标 weak、boundary_anchor / schema_seed；review §6.2 明确列出 5 条"不能写的强主张"（首创性 / 系统取代专家 / 端到端已实现 / LLM 搜索已可靠覆盖 / 符合 PRISMA）；§6.3 风险表把"概念方案未评估"列入。无 C 级越权。 | 通过 |

## 4. 建议维度树骨架

下骨架忠实反映原文 Fig.1 + §2 + §3 的显式闭合结构。所有取值空间都来自 `paper_content.txt` verbatim，无需 A2a 才能写出。

```text
[root] On the road to interactive LLM-based systematic mapping studies
    type: solution_proposal · vision/roadmap · 不进主统计池
    单位对象: roadmap_action / guideline_step / schema_seed
├── [b1] LLM-supported mapping process（Fig.1 单一骨架；对应 §2 全章）
│   ├── [leaf-stage] mapping process 阶段
│   │     取值空间(闭合): {establishing_need, study_id_search, study_id_inclusion_exclusion,
│   │                     data_extraction_and_classification, visualization, reporting}
│   │     证据: paper_content.txt Page 2–3 §2.1–§2.5；Fig.1
│   │     缺失值: not_applicable(本文是 proposal，每阶段都有，无缺失)
│   │     可统计: 否（仅 schema_seed）
│   ├── [leaf-stage-triple] 每阶段三元字段（Fig.1 通用结构）
│   │     取值空间(闭合): {user_input, llm_output, human_refinement}
│   │     证据: Fig.1 + §2.1 开篇（"we edit the questions as input for the next stage"）
│   ├── [leaf-search-agent] Search 阶段三 agent
│   │     取值空间(闭合): {keyword_identification_agent, semantic_search_agent, search_strategy_agent}
│   │     关系: parent=study_id_search；citation_pearl_growing 由前两 agent 联合驱动
│   │     证据: §2.2.1 编号 1/2/3
│   ├── [leaf-search-strategy] Search 策略类型
│   │     取值空间(闭合): {boolean_query, semantic_search_RAG, citation_pearl_growing}
│   │     备注: 原文优先 Boolean(reproducibility) + RAG 辅助
│   │     证据: §2.2.1
│   ├── [leaf-incl-excl-trace] Inclusion/Exclusion 可追溯组件
│   │     取值空间(枚举): {rationale, cited_evidence_fragments, source_location,
│   │                    chain_of_thought_prompt, continual_learning_signal, DSPy_prompt_optimization,
│   │                    human_override}
│   │     证据: §2.2.2
│   ├── [leaf-coding-mode] Data extraction coding mode
│   │     取值空间(闭合,二元): {inductive, deductive}
│   │     证据: §2.3 编号 1/2
│   ├── [leaf-inductive-pipeline] Inductive coding 4 步流水（有序）
│   │     取值空间(闭合,有序): [embeddings → dim_reduction → clustering → topic_representation]
│   │     工具示例: BERTopic（模块化）
│   │     证据: §2.3 Page 3
│   ├── [leaf-deductive-tech] Deductive coding 技术
│   │     取值空间(闭合): {one_shot, few_shot, RAG_full_pdf, document_splitting}
│   │     输入: full_paper_pdf（非仅 title/abstract）
│   │     证据: §2.3 Page 3
│   ├── [leaf-viz-tool] Visualization 工具/方法
│   │     取值空间(枚举): {ChatGPT_codegen, LIDA, BERTopic_landscape, bar_chart, bubble_plot}
│   │     证据: §2.4 Page 3
│   └── [leaf-reporting-task] Reporting LLM 任务
│         取值空间(枚举): {pattern_spotting, observation_highlight, gap_spotting, narrative_draft}
│         证据: §2.5 Page 3
├── [b2] Researcher prerequisites & motivations（§1）
│   ├── [leaf-reviewer-prereq] reviewer 资格（闭合二元）
│   │     取值空间: {educated_in_mapping_methodology, topic_expert}（两者必备）
│   │     证据: §1 Page 1 (a)/(b)
│   └── [leaf-motivation] 4 条使用动机（闭合）
│         取值空间: {paper_volume, larger_scope, design_ideas_via_interaction, regular_updates}
│         证据: §1 Page 1 (1)–(4)
├── [b3] Validity / Reflections（§3）
│   ├── [leaf-validity-category] 4 类 validity 类别（闭合）
│   │     取值空间: {publication_bias_and_limited_studies, rapid_LLM_evolution,
│   │              non_SE_evidence_transfer, conceptual_framework_no_prototype}
│   │     关系: each → affected_stage(s)
│   │     证据: §3 Reflections, Study validity 段
│   └── [leaf-complementary-tool] complementary tools 与角色
│         取值空间(枚举): {LangSmith(tracing/debugging/testing), WebVoyager(visual web/grey literature),
│                          BERTopic(topic landscape), LIDA(viz), DSPy(prompt opt)}
│         证据: §3 + §2 散布
├── [b4] Research roadmap（§3 末两条 bullet）
│   └── [leaf-research-direction] 研究方向（闭合二元）
│         取值空间(闭合): {improve_individual_steps_with_eval, build_end_to_end_prototype}
│         关系: each → covers_subset_of {mapping_process_stages}
│         证据: §3 Page 3 末
└── [b5] Proposal boundary & artifact status（boundary_anchor）
    ├── [leaf-paper-type] 论文类型（闭合）
    │     取值空间: {solution_proposal}（非 SLR/SMS/tertiary）
    │     证据: Abstract Method + §1
    ├── [leaf-artifact-status] 工件可用性
    │     取值空间: {no_data, no_code, no_prompt_repo, no_benchmark, no_run_record,
    │              supplementary_material_exists_unopened}
    │     证据: §3 Data availability + Appendix A
    └── [leaf-relevant-lit] borrowed empirical anchors（10 篇引文角色）
          取值空间: 引文角色 ∈ {search_eval([5]), screening_eval([6,7]),
                              topic_modeling([8]), case_study_judging([9]),
                              web_agent([10]), HIL_foundation([1]), prior_ML_tools([2,3]),
                              mapping_guideline([4])}
          证据: References Page 4
```

**关系边补充**（A2a 应当显式建模）：

- `R1: stage → triple`：每 stage 必有 {user_input, llm_output, human_refinement} 三元（Fig.1 通用结构）。
- `R2: search_stage ← {keyword_agent, semantic_search_agent, search_strategy_agent}`（多对一）。
- `R3: validity_category → affected_stage(s)`（如 `rapid_LLM_evolution → all_stages`；`publication_bias_and_limited_studies → reflections/extraction/screening`；`non_SE_evidence_transfer → all_stages`；`conceptual_framework_no_prototype → end_to_end`）。
- `R4: research_direction → covered_stages`（R1 = single-stage 评估；R2 = end-to-end prototype）。
- `R5: tool → role → stage`（如 `LangSmith → tracing → all_stages`；`BERTopic → topic_landscape → inductive_coding+visualization`）。
- `R6: recall_precision_tradeoff`：GPT-generated query → recall ↓；refinement → precision ↑/recall ↓（来自引文 [5]）。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 维度树主表把 6 个通用接口当作主体叶子展示，导致原文已闭合枚举（6 阶段、3 agent、二元 coding 等）被掩埋 | review §"叶子维度表" 与 §"原文模式候选叶子映射（A1 种子）" | 将 §4 建议骨架中的 [leaf-stage] / [leaf-stage-triple] / [leaf-search-agent] / [leaf-search-strategy] / [leaf-incl-excl-trace] / [leaf-coding-mode] / [leaf-inductive-pipeline] / [leaf-deductive-tech] / [leaf-viz-tool] / [leaf-reporting-task] / [leaf-validity-category] / [leaf-research-direction] / [leaf-reviewer-prereq] / [leaf-motivation] / [leaf-complementary-tool] / [leaf-artifact-status] / [leaf-relevant-lit] 提升为正式候选叶子，并把 6 个通用 `leaf-*` 改写为"跨论文接口层（不重复原文模式枚举）"，避免和原文模式候选叶子混淆 | `paper_content.txt` Page 1–4；Fig.1 已在 review.md §"阅读状态"中声明已核对 | **I**（边界仍守住，但 A2a 复原链条会严重失锚） |
| 主干分支 b1/b2/b3 把 Fig.1 单一 mapping-process 骨架切成三条并列分支，破坏 Fig.1 三元配对 | review §"维度树结构" | 合并为单一 [b1] LLM-supported mapping process（对应 §2 整章），并在该分支下挂 leaf-stage / leaf-stage-triple / leaf-search-agent 等；把 traceability 收回到 [leaf-incl-excl-trace]（属于 study_id_inclusion_exclusion 而非全局分支）；新增 [b2] Researcher prerequisites、[b3] Validity、[b4] Research roadmap、[b5] Proposal boundary 四条 | Fig.1 + §1 + §2 + §3 | I |
| 4 条 `_orig-*` 候选叶子取值空间用概括短语，未写出原文 verbatim 枚举 | review §"原文模式候选叶子映射" 取值空间列 | 把"SMS 阶段"具体化为 {establishing_need, study_id_search, study_id_inclusion_exclusion, data_extraction_and_classification, visualization, reporting}；把"LLM 介入点"具体化为 §2.2.1/§2.2.2/§2.3 的具名 agent + prompting 技术；把"研究者交互"具体化为 {edit_RQ, override_inclusion, validate_extraction, validate_visualization, accept_or_reject_pattern}；把"可追溯性风险"具体化为 §3 4 类 validity | §1/§2/§3 verbatim | I |
| EV 全部 `not_verified` 与 review.md §"阅读状态"自述"已回原文核对 Fig.1"矛盾 | review §"A.2 维度树证据账本" | 至少把支撑 `[leaf-stage]、[leaf-search-agent]、[leaf-coding-mode]、[leaf-validity-category]、[leaf-research-direction]` 的 EV 升级为 `text_verified`（fulltext-text 等级），并把 `需要原文版面核验` 改为 false（这些都是纯文本事实）；对真正需要 PDF 视觉的留 `needs_pdf_visual`，但本文只有 Fig.1，已在自述中标 verified，可降 `[cmd-...-visual-check]` 为 passed | `paper_content.txt` 全文；Fig.1 已自述核对 | I |
| 关系边未在维度树本体或 A.2 / A.3 中刻画 | review §"维度树结构" 后补关系边小节，或在 A.2 增加 `关系边证据` 列 | 按 §4 骨架的 R1–R6 增补关系边，每条挂证据锚点 | Fig.1 + §2.2.1/§2.3/§3 | I |
| 候选 finding 路径"统计与候选发现链路"只 3 行，未模板化 Paper2 可继承的 finding-path | review §"统计与候选发现链路" | 新增至少三条候选 finding-path：(p1) `stage → triple(user_input, llm_output, human_refinement) → audit_evidence`；(p2) `validity_category → affected_stage → roadmap_direction`；(p3) `tool → role → stage → maturity_status` | Fig.1 + §3 | M（不阻塞主统计池守门，但有助 A2b） |
| 一句话结论 / 根节点描述未把"无 RQ / Fig.1 = 主骨架"刻入 | review §"一句话结论" 与 [dim-...-root] 单位对象列 | 把根节点单位对象由"roadmap action / guideline item / schema seed"改写为"Fig.1 mapping-process schema 的阶段-三元-agent 节点 + roadmap action + boundary anchor"，并在一句话结论补一句"原文 RQ 缺如，Fig.1 三元结构为最强可迁移 schema seed" | Abstract + Fig.1 + §3 末 | M |
| 复合工具集 {LangSmith, WebVoyager, LIDA, BERTopic, DSPy} 散落 review 多处，无统一候选叶子 | review §"叶子维度表" 或新增 §"complementary tools 候选叶子" | 增补 [leaf-complementary-tool]，取值空间见 §4 骨架，每个工具挂 stage 与 role | §2.3/§2.4/§3 | M |

## 6. C/I/M 结论

- **C**：无。当前 review 在统计池守门、boundary anchor、不写强主张三条边界上守得很好（metadata.json 与 review §6.2/§6.3 已显式禁止首创性、自动取代专家、端到端已实现、LLM 搜索已可靠覆盖、PRISMA 符合等强主张），不会直接破坏 Paper2 证据链或后续 A2a/A2b 主统计池。
- **I**（4 条，均涉及 A2a 维度树复原可用性）：
  1. 维度树叶子主表把 6 个跨论文通用接口暴露为本文叶子，导致原文已闭合枚举（6 阶段 / 3 agent / 二元 coding / 4 类 validity / 2 条研究方向等）未在 A1-DT 阶段固化，A2a 起点会变弱。
  2. 主干 b1/b2/b3 切断 Fig.1 三元配对结构，使 "stage ↔ triple ↔ agent" 关系链丢失。
  3. 关系边（stage→triple、search→agents、validity→stage、tool→role→stage、recall/precision tradeoff）在维度树本体未出现。
  4. EV 全部 `not_verified` 与"已回原文核对 Fig.1"自述不一致；可文本级 verified 的事实未被升级，弱化下游 confidence 信号。
- **M**（3 条，不阻塞）：根节点描述未刻入"无 RQ / Fig.1 主骨架"；候选 finding-path 模板化欠缺；complementary tools 未统一叶子化。

**最终建议：NEEDS FIX**（I 级问题需在维度树主表与 A.2/A.3 内修复；可在同一 PR 子提交中完成，无需额外 PR）。建议优先级：修复项 1 → 2 → 4 → 3 → 其余 M 级跟随。修复完成后即可视为 A1-DT 对本篇的可交付门槛达成。
