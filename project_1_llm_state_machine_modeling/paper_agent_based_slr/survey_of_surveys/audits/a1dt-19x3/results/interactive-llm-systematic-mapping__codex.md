# interactive-llm-systematic-mapping · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`。本审计按 claim-evidence、story gate、reviewer gate 和 unsupported claim 降级口径执行。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`。本审计按“严格贴合原文目标 / 方法 / 结构，缺失处显式标记，不补造配置或字段”执行。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本审计采用 artifact-gated completion 口径：只以写入本审计报告作为完成制品，不以口头判断替代可检查输出。
- 是否完整阅读 `paper_content.txt`：是；完整阅读 `paper_content.txt` 1--280 行，覆盖摘要、Introduction、§2 LLM-supported mapping process、§2.1--§2.5、§3 Reflections、Data availability 和 References。
- 是否核对 `paper.pdf`：是；使用 `pdfinfo` 确认 PDF 为 4 页，并用 `pdftoppm` 渲染第 2 页后视觉核对 Fig. 1 “The mapping process with LLM support”。未打开 DOI supplementary material，所以下划线术语定义和补充材料内容不作为已核验证据。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

- 原文没有正式 RQ 表，也没有执行一项新的 SMS / SLR。摘要明确目标是讨论在 mapping study process 中使用 LLM 的可能性与下一步工作：`Objective: To discuss possibilities and next steps for using LLMs ... in the mapping study process`（`paper_content.txt:17`）。
- 方法类型是 solution proposal：作者基于自身 LLM 与 literature review 经验迭代设计和讨论方案（`paper_content.txt:18-19`）。这意味着本文是方法设想 / roadmap seed，不是完成型系统综述。
- 贡献声明是提出 mapping process 各步骤的 agent / prompting strategy，并呼吁社区共同构建和评估 holistic solution（`paper_content.txt:20-23`、`33-44`）。
- 原文强边界：研究者仍必须懂 mapping study 方法并是主题专家，才能判断 LLM-system 输出（`paper_content.txt:50-55`）。因此本文不支持“取代专家”“全自动系统综述”“已验证端到端解决方案”等强主张。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

- 本文自身没有检索数据库、搜索式、筛选分母、纳排清单、quality assessment、primary-study corpus、数据抽取表或统计合成。Data availability 明确写明该研究没有使用数据（`paper_content.txt:243-247`）。
- 原文方法流程是“按 Petersen 2015 mapping guideline 的流程阶段讨论 LLM 如何介入”。`paper_content.txt:63-71` 明确 Fig. 1 展示 review process 的每一步、用户输入 / 动作和 LLM 输出；研究者应有初始 search terms、inclusion criteria、extraction items 以验证输出。
- Fig. 1 是本文最显式的 schema / model：五个阶段分别为 Establish a need for the review、Study identification、Data extraction、Visualization、Reporting。每个阶段有 user input、interactive refinement 和 LLM-output。
- §2.2.1 search 进一步提出三 agent 架构：Keyword Identification Agent、Semantic Search Agent、Search Strategy Agent；并强调 Boolean search、透明性、可复现性、citation pearl growing、RAG 和 graph database（`paper_content.txt:87-122`）。
- §2.2.2 inclusion / exclusion 把筛选定义为 classification problem，但强调只给 include/exclude 不够，LLM 必须给出 reasons、citations 和可验证论据以保证 traceability（`paper_content.txt:136-157`）。
- §2.3 data extraction and classification 区分 inductive coding 与 deductive coding：inductive coding 使用 titles/abstracts、embedding、dimension reduction、clustering、topic representations；deductive coding 使用既有 extraction scheme、one/few-shot prompting、full PDF、document splitting 与 RAG（`paper_content.txt:171-191`）。
- §2.4 visualization 与 §2.5 reporting 是工具 / 输出阶段：可用 ChatGPT/LIDA/BERTopic 生成图表或文献 landscape；reporting 阶段把 tables / visualizations 给 GPT，让其突出 patterns、observations 和 gaps（`paper_content.txt:200-211`）。
- Finding 形成方式不是实证统计，而是 proposal argument：阶段化流程 + 相关文献示例 + validity reflections -> 两条研究方向，即改进 / 评估单步骤策略，构建整体 prototype 以收集端到端 mapping support 想法（`paper_content.txt:212-234`）。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

- 显式模型 / 图：Fig. 1 “The mapping process with LLM support”。它是本文的核心 schema，应作为维度树事实源，而不是只作为泛证据。
- 显式流程阶段：Establish a need for the review、Study identification、Data extraction、Visualization、Reporting。Study identification 覆盖 search and study selection；Data extraction 覆盖 article classification 和 data extraction form。
- 显式人机交互字段：每一列都有 user input、interactive refinement、LLM-output。该三元组是本文最重要的可迁移 schema。
- 显式 agent schema：search 阶段三 agent：Keyword Identification Agent、Semantic Search Agent、Search Strategy Agent。
- 显式 coding scheme seed：inductive coding / deductive coding；inductive 使用 topic model，deductive 使用 data extraction scheme / extraction form / RAG。
- 显式 traceability / validity 字段：transparent and reproducible search、Boolean search、citations indispensable、publication bias、limited reliability evidence、model evolution、non-SE evidence transfer、SE-specific evaluation need（`paper_content.txt:91-100`、`150-157`、`212-223`）。
- 不存在的结构：没有本文自己的 extraction form、closed taxonomy、质量评分 rubric、PRISMA 图、evidence table、实验指标表、artifact repository、prompt set、run record 或 prototype。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

- 原文没有本文内部统计观察，因此不能形成 empirical finding。
- 原文把外部文献结果作为 risk / feasibility evidence：GPT-generated queries 可能 recall 更低，refinement 可能降低 recall、提高 precision（`paper_content.txt:123-135`）；GPT screening 对 irrelevant paper exclusion 有帮助但 high recall 仍不足（`paper_content.txt:158-170`）。
- 原文把这些观察降级为 future directions：优化单步骤策略并评估 prompting，构建整体 prototype 收集端到端支持 mapping studies 的进一步想法（`paper_content.txt:230-234`）。
- 对 Paper2 的可迁移路径应是：proposal schema / Fig. 1 / risk reflection -> schema_seed 或 boundary_anchor -> 研究者裁决；不得写成“LLM 已被证明能可靠完成 mapping study”。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但仍需收紧 | `review.md:279` 正确判断主类型是方法流程树、辅助类型是 human-in-the-loop boundary 树，并正确排除主统计池。问题在于 `review.md:287-289` 的单位对象写成 `roadmap action / guideline item / schema seed`，而原文更直接的单位对象应是 mapping-process stage、user action、LLM output、agent role、risk / research direction。 | M |
| 主干分支是否覆盖原文 schema | 未充分覆盖 | `review.md:289` 的主干为 SMS 流程阶段、LLM / agent 介入点、researcher interaction、traceability risk、proposal boundary，方向合理但太抽象；正式树 `review.md:293-305` 没有把 Fig. 1 的五个流程列、每列三元组，以及 search / selection / extraction 内部结构列为主干和子节点。 | I |
| 叶子维度是否足够具体 | 不足，当前事实真源过小 | `review.md:283` 已正确声明六个 `leaf-*` 是跨论文通用接口，不是原文 leaf 全集；但正式叶子表 `review.md:310-317` 仍只列 scope、corpus、taxonomy、method、evidence、finding 六个通用 leaf。原文真正可执行的叶子，如 research objective、candidate RQs、search terms、inclusion/exclusion criteria、article metadata、final verdict/confidence、inductive topic model、deductive extraction item、data tables、visualization correctness、pattern/gap suggestions，未进入正式叶子表。 | C |
| 取值空间是否可执行 | 关键取值空间不可执行 | 通用 leaf 的取值空间多为“自由文本 / 完整枚举 / 层级枚举 / 布尔”等接口说明，不能直接指导 A2a 抽取。`review.md:325-328` 的原文候选叶子只有 4 个粗类，且 `SMS 阶段` 写成“研究问题、检索、筛选、分类、统计、报告等”并未忠实保留 Fig. 1 的 stage 名称和 stage 内三元组。 | I |
| 关系边是否缺失 | 缺失核心关系边 | 当前维度树没有关系边表。原文需要至少保留 `stage -> user input`、`stage -> interactive refinement`、`stage -> LLM-output`、`search -> three agents`、`inductive/deductive coding -> outputs`、`risk -> affected stage`、`external literature result -> limitation / future direction` 等关系。 | I |
| 统计用途 / 分母是否正确 | 降级正确，但缺少 proposal-specific 统计口径 | `metadata.json` 和 `review.md:279` 正确写明不进主统计池，`review.md:334-336` 也没有把本文写成 statistical_synthesis。缺口是没有把“只能在 survey-of-surveys 中统计为 solution proposal / boundary_anchor / schema_seed，不可统计原文内部效果”写进每个原文叶子的统计用途。 | M |
| 候选 finding 路径是否完整 | 不完整 | `review.md:334-336` 只写“识别可迁移的维度模式类型”和“candidate finding / risk”，没有复原原文的 proposal finding path：外部研究风险（search recall、screening recall、model drift、非 SE 证据外推）-> 需要 SE-specific conceptual framework / single-step evaluation / end-to-end prototype。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，证据粒度不足且状态不一致 | A.1 有 PDF/text/bib，但缺 `metadata.json`；A.2 `review.md:359-362` 全部是“待 A2a 精确页码复核 / 见释义 / 邻近段落”，证据强度降为 `not_verified` 是合规的，但不足以支撑“Fig. 1 已核对”的正式树。A.4 `review.md:386` 仍为 `needs_manual_check`，而快速卡片 `review.md:16-17` 声称已回原文核对 Fig. 1，存在轻微不一致。 | I |
| 是否存在可能误导 A2a 的强主张 | 有结构性误导风险，但未出现强统计误用 | `review.md:283` 的降级声明避免了“通用 6 leaf = 原文 schema”的直接强主张，也没有把 `not_verified` 证据升级为 `statistical_synthesis`。但因为 `维度树复原` 被声明为事实真源，正式树仍只有通用 leaf + 4 个粗候选叶子，A2a 可能误以为后续只需补页码，而不是重建 Fig. 1 / §2 的原文 schema。 | I |

## 4. 建议维度树骨架

当前 `review.md` 尚不足够。建议把六个通用 `leaf-*` 降为跨论文检查接口，把以下原文 schema 作为该单篇 `维度树复原` 的正式事实源。

根节点：`[dim-interactive-llm-sms-root] interactive LLM-supported systematic mapping process`

树类型：方法流程树 + human-in-the-loop / LLM-output 关系型树。

统计池资格：不进入主统计池；只能作为 `schema_seed`、`boundary_anchor`、`candidate_finding`、`risk_only`。缺失值语义必须区分 `not_applicable_no_empirical_sms`、`not_reported`、`not_verified_supplementary`、`proposal_only`、`external_literature_claim`。

| 节点 / 叶子 | 父节点 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| [dim-llm-sms-stage] 流程阶段 | [dim-interactive-llm-sms-root] | Establish a need for the review；Study identification；Data extraction；Visualization；Reporting | 不统计原文效果；可在 survey-of-surveys 中统计为 stage schema seed | not_applicable_no_empirical_sms | Fig. 1；`paper_content.txt:63-71` |
| [leaf-llm-sms-stage-need] Establish a need | [dim-llm-sms-stage] | gap / research goals / research questions；research objective；contextual information；candidate RQs；additional objectives；edited questions | schema_seed | not_reported；proposal_only | Fig. 1；§2.1；`paper_content.txt:80-84` |
| [leaf-llm-sms-stage-identification] Study identification | [dim-llm-sms-stage] | search；study selection；search terms；inclusion criteria；exclusion criteria；article metadata；include / exclude verdict；confidence value | schema_seed | not_reported；proposal_only | Fig. 1；§2.2；`paper_content.txt:85-170` |
| [leaf-llm-sms-stage-extraction] Data extraction | [dim-llm-sms-stage] | classify articles；data extraction form；inductive classification；deductive classification；topic model；extraction items；structured CSV/JSON output | schema_seed | not_reported；proposal_only | Fig. 1；§2.3；`paper_content.txt:171-199` |
| [leaf-llm-sms-stage-visualization] Visualization | [dim-llm-sms-stage] | data tables；frequencies within categories；bar charts；bubble plots；tabular summaries；representation correctness / quality | schema_seed | not_reported；proposal_only | Fig. 1；§2.4；`paper_content.txt:200-206` |
| [leaf-llm-sms-stage-reporting] Reporting | [dim-llm-sms-stage] | data tables；objectives / RQs associated with tables；interesting patterns；insights；research gaps；adjusted suggestions | candidate_finding seed，不作 final finding | not_reported；proposal_only | Fig. 1；§2.5；`paper_content.txt:207-211` |
| [dim-llm-sms-human-loop] 人机交互三元组 | [dim-interactive-llm-sms-root] | user input；interactive refinement；LLM-output | 可统计为 schema pattern，不统计效果 | no_human_loop_reported；proposal_only | Fig. 1；`paper_content.txt:63-71` |
| [leaf-llm-sms-user-input] User input | [dim-llm-sms-human-loop] | objectives；questions；criteria；metadata；data tables；extraction scheme；topic model configuration | schema_seed | not_reported | Fig. 1 |
| [leaf-llm-sms-interactive-refinement] Interactive refinement | [dim-llm-sms-human-loop] | edit questions；pilot / iterate / update searches and criteria；adjust topic model; pilot extraction forms; verify visualization; adjust reporting suggestions | schema_seed；human gate seed | not_reported | Fig. 1；§2.1--§2.5 |
| [leaf-llm-sms-llm-output] LLM output | [dim-llm-sms-human-loop] | RQ candidates；search terms；screening suggestions；CSV/JSON screening output；topic model outputs；extraction item suggestions；structured extracted information；tables / charts；pattern / insight suggestions | schema_seed；candidate_finding seed | not_reported；not_verified_supplementary | Fig. 1 |
| [dim-llm-sms-search-agent] Search agent architecture | [dim-interactive-llm-sms-root] | Keyword Identification Agent；Semantic Search Agent；Search Strategy Agent | schema_seed；不作已验证 architecture | proposal_only | §2.2.1；`paper_content.txt:96-122` |
| [leaf-llm-sms-keyword-agent] Keyword Identification Agent | [dim-llm-sms-search-agent] | relevant terms；semantically similar terms；historical terms；concept / subtype / supertype focus | schema_seed | not_reported | `paper_content.txt:101-110` |
| [leaf-llm-sms-semantic-agent] Semantic Search Agent | [dim-llm-sms-search-agent] | RAG；semantic similarity；candidate documents；graph database；citation links；strategy adjustment not final selection | schema_seed | not_reported | `paper_content.txt:111-118` |
| [leaf-llm-sms-strategy-agent] Search Strategy Agent | [dim-llm-sms-search-agent] | Boolean expression；database query；transparent and reproducible strategy | schema_seed | not_reported | `paper_content.txt:87-100`、`119-120` |
| [dim-llm-sms-screening] Inclusion / exclusion support | [dim-interactive-llm-sms-root] | continual learning；DSPy prompt optimization；classification; rationale; citations; seed papers / prior SLRs | schema_seed；risk_only | no_evidence_span；not_reported | §2.2.2；`paper_content.txt:136-170` |
| [leaf-llm-sms-screening-traceability] Screening traceability | [dim-llm-sms-screening] | reason / rationale；text fragment；citation；include/exclude/uncertain；human oversight | schema_seed；risk_only | no_citation；no_rationale；not_reported | `paper_content.txt:150-157` |
| [dim-llm-sms-coding] Coding and extraction strategy | [dim-interactive-llm-sms-root] | inductive coding；deductive coding | schema_seed | not_reported | §2.3；`paper_content.txt:171-191` |
| [leaf-llm-sms-inductive-coding] Inductive coding | [dim-llm-sms-coding] | titles/abstracts；embeddings；dimension reduction；clustering；topic representation；BERTopic; hierarchy; temporal analysis | schema_seed | not_reported | `paper_content.txt:177-184`、`192-198` |
| [leaf-llm-sms-deductive-coding] Deductive coding | [dim-llm-sms-coding] | data extraction scheme；SWEBOK example；one-shot / few-shot；full PDF；document splitting；RAG chunks；OpenAI API | schema_seed | not_reported | `paper_content.txt:185-191` |
| [dim-llm-sms-evidence-risk] Evidence and validity boundary | [dim-interactive-llm-sms-root] | search recall risk；screening recall risk；publication bias；limited reliability evidence；model evolution；non-SE transfer risk；SE-specific evaluation need；no data used；supplementary not checked | risk_only / boundary_anchor | not_reported；not_verified_supplementary | §2 relevant literature；§3 Reflections；Data availability |
| [leaf-llm-sms-research-directions] Research directions | [dim-llm-sms-evidence-risk] | improve individual steps and evaluate strategies；build prototype for overall process | candidate_finding；not final finding | proposal_only | `paper_content.txt:230-234` |
| [leaf-llm-sms-artifact-status] Artifact / data status | [dim-llm-sms-evidence-risk] | no data used；supplementary available but not checked；no code / prompt / run record reported | risk_only | not_verified_supplementary | `paper_content.txt:243-247` |

建议关系边：

| 关系边 | 源节点 | 关系类型 | 目标节点 / 取值 | 缺失值语义 | 证据定位 |
|---|---|---|---|---|---|
| [edge-llm-sms-stage-user-input] | [dim-llm-sms-stage] | has_user_input | [leaf-llm-sms-user-input] | not_reported | Fig. 1 |
| [edge-llm-sms-stage-refinement] | [dim-llm-sms-stage] | has_interactive_refinement | [leaf-llm-sms-interactive-refinement] | no_refinement_reported | Fig. 1 |
| [edge-llm-sms-stage-output] | [dim-llm-sms-stage] | has_llm_output | [leaf-llm-sms-llm-output] | no_output_reported | Fig. 1 |
| [edge-llm-sms-search-agents] | [leaf-llm-sms-stage-identification] | decomposes_into | keyword / semantic / strategy agents | no_agent_architecture | §2.2.1 |
| [edge-llm-sms-search-reproducibility] | [leaf-llm-sms-strategy-agent] | constrained_by | transparent reproducible Boolean search | not_reported | §2.2.1 |
| [edge-llm-sms-screening-evidence] | [dim-llm-sms-screening] | requires_traceability | reasons + citations + source fragments | no_citation / no_rationale | §2.2.2 |
| [edge-llm-sms-coding-mode-output] | [dim-llm-sms-coding] | produces | topic model / extraction items / structured extracted information | not_reported | Fig. 1；§2.3 |
| [edge-llm-sms-risk-future-work] | [dim-llm-sms-evidence-risk] | motivates | single-step evaluation / end-to-end prototype | proposal_only | §3 Reflections |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 重建 `维度树复原` 正式事实源 | `review.md` `## 维度树复原` 的树结构、叶子维度表、原文候选叶子映射 | 把六个通用 leaf 降为跨论文检查接口；正式树应以 Fig. 1 五阶段、user input / interactive refinement / LLM-output 三元组、search 三 agent、inductive/deductive coding、risk/reflection 为核心。 | Fig. 1；`paper_content.txt:63-71`、`80-211` | C |
| 修正主干与叶子的父子错配 | `review.md:293-305`、`310-317` | 不应把“语料与纳排链条”挂在 LLM / agent 介入点下、把“主题与维度分类”挂在 researcher interaction 下、把“方法分类”挂在 traceability risk 下。应改为 process stage -> stage-specific fields，另设 human-loop、agent、risk 分支。 | Fig. 1；§2.1--§2.5 | I |
| 展开 Fig. 1 stage-level schema | 原文模式候选叶子映射 | 增加 Establish a need、Study identification、Data extraction、Visualization、Reporting 五个 stage leaf，并逐一列出 user input、interactive refinement、LLM-output 的取值空间。 | PDF Page 2 Fig. 1 视觉核对 | I |
| 展开 search 三 agent 结构 | 叶子维度表 / 关系边表 | 增加 Keyword Identification Agent、Semantic Search Agent、Search Strategy Agent；取值包括 semantically similar terms、RAG、graph database、citation links、Boolean query、citation pearl growing 等。 | `paper_content.txt:87-122` | I |
| 展开 inclusion / exclusion traceability 字段 | 叶子维度表 / evidence-risk 分支 | 增加 include/exclude/uncertain、rationale、citation、source fragment、human oversight、continual learning / DSPy optimization、seed papers / prior SLRs。 | `paper_content.txt:136-170` | I |
| 展开 data extraction / classification 字段 | 叶子维度表 | 增加 inductive coding 与 deductive coding；inductive 取值包括 embeddings、dimension reduction、clustering、topic representations、BERTopic；deductive 取值包括 extraction scheme、SWE-BOK example、one/few-shot、full PDF、document splitting、RAG chunks。 | `paper_content.txt:171-199` | I |
| 建立关系边表 | `维度树复原` 叶子表后 | 增加 `stage -> user input/refinement/output`、`search -> agent`、`screening -> traceability evidence`、`coding mode -> output`、`risk -> future research direction` 等关系边。 | Fig. 1；§2.2--§3 | I |
| 重建 proposal finding path | 统计与候选发现链路 | 记录外部 literature signals 与 validity reflections 如何转化为两条 research directions；禁止写成本文独立实证 finding。 | `paper_content.txt:123-135`、`158-170`、`212-234` | I |
| 补精确证据锚点 | A.2 | 把 EV-001--EV-004 拆成 objective/method、Fig. 1、search agents、screening traceability、coding strategy、visualization/reporting、validity reflections、data availability 等证据；写明 page、section、`paper_content.txt` 行号和 Fig. 1。 | `paper_content.txt` 全文；PDF Page 2 | I |
| 修正 PDF / supplementary 核验状态 | 快速卡片与 A.4 | Fig. 1 已可标为 PDF Page 2 visual checked；A.4 中 visual-check 不应笼统 `needs_manual_check`，应拆成 `Fig. 1 checked` 与 `supplementary not checked`。 | `review.md:16-17`、`386`；本次 PDF 核对 | M |
| 增加 `metadata.json` 到 A.1 | A.1 | A.1 当前缺 `metadata.json` 来源；应补入，用于年份、online_first、solution proposal、statistical exclusion reason、CCF 状态等元数据核验。 | `metadata.json` | M |

## 6. C/I/M 结论

- C：1 项。当前 `维度树复原` 的正式事实源过小：它把六个通用 leaf 放在正式叶子表中，而原文 Fig. 1 / §2 的 stage-level schema、三元人机接口、search 三 agent、screening traceability、inductive/deductive coding 和 research-direction path 没有成为一等叶子与关系边。这会直接破坏 Paper2 A2a 对该文“维度模式如何从原文 schema 复原”的证据链。
- I：8 项。包括主干覆盖不足、父子关系错配、取值空间不可执行、关系边缺失、candidate finding path 不完整、A.2 泛定位、PDF 核验状态不一致、metadata/source 不完整。这些会实质影响维度树可用性和后续 schema 回填。
- M：2 项。主要是根节点单位对象表述和 A.1 / A.4 维护性修正。
- 最终建议：NEEDS FIX。

总体判断：当前 `review.md` 的全文详读部分质量较好，且已经明确该论文是 solution proposal、不得进入主统计池，也没有把 `not_verified` 证据升级为统计结论。但 `## 维度树复原` 仍没有达到“完整、准确、可追溯”的事实真源标准；它目前更像“通用接口 + 粗候选索引”。最小修复是把 Fig. 1 和 §2 的真实流程 schema 重建为正式树、叶子表、关系边表和 A.2/A.3 证据映射，六个通用 leaf 只能保留为跨论文检查接口。
