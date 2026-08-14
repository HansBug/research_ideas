# requirements-quality-theory-roadmap · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- 是否完整阅读 `paper_content.txt`：是；覆盖 `paper_content.txt` 全部 1187 行，包含正文 Page 1--14、参考文献与图表附近文本。
- 是否核对 `paper.pdf`：是；用 `pdfinfo` 确认 14 页 PDF，并用 `pdftoppm` 临时渲染 Page 4--11，视觉核对 Fig. 2、Table 1、Fig. 4、Fig. 5 的结构与 `paper_content.txt` 一致。未下载 / 打开原文 replication package 与 RQT tool 仓库。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文是 Requirements Engineering 期刊的 research commentary / theory + evaluation + roadmap，不是标准 SLR/SMS。其摘要与引言声明三项贡献：提出 harmonized requirements quality theory，评价 requirements quality research 当前状态，并给出 research roadmap。引言中还说明理论来自 software quality research 演化、ABRE-QM 与 Quamoco 的整合。

原文唯一显式评价 RQ 是：requirements quality literature 如何报告 RQT 中的概念。该 RQ 服务于“用理论概念反向审视 57 篇 requirements quality primary studies”，不是完整 tertiary review 的 RQ。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文流程是三段式：

1. 理论形成：回顾 software quality research 从 guideline / metric 到 quality model、quality meta-model、activity-based model、tool-supported operationalization 的演化，再映射到 requirements quality research，形成 RQT。
2. 状态评价：使用此前 systematic study 中 57 篇 requirements quality factors primary studies 作为 non-probabilistic convenience sample；作者明确该样本满足其本次评价目标，但不是新建完整检索闭环。
3. Roadmap 形成：用 RQT 覆盖统计和解释性缺口，更新 Femmer 等人的三条研究流，并新增 context factors、economic impact、tool support 三条方向。

数据抽取与编码流程很明确：作者基于 RQT concepts 创建 extraction guideline；每个 RQT concept 关联一个或多个 categorical variables；每个变量有 codes 表示该 concept 是否以及如何被报告。第一作者对 57 篇编码；第二作者独立抽取约 10% 样本，其中 2 篇训练、4 篇用于 reliability 计算；报告 percentage agreement 83.3%、Cohen's Kappa 54.2%、S-Score 76.8%；再用 descriptive statistics 解释 RQT concept coverage。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文最核心 schema 不是当前 `review.md` 中的六个通用接口，而是以下结构：

- RQT concept model：Fig. 2 和 Table 1 给出 Entity、Factor、Entity-fact、Agent、Activity、Attribute、Activity-fact、Impact、Context factor、Cost、Resource，并给出关系：decomposes into、characterizes、is used in、is involved in、produces、causes 等。
- RQT example：Fig. 3 用 user story、template conformance、missing role、understanding determinism、programming duration、organizational/process context、cost/resource 展示 entity-fact 到 activity-fact 的 impact 关系。
- Extraction guideline / coding scheme：Sect. 4.2 明确每个 concept 对应 categorical variables 和 codes。例如 Entity 有 explicit / implicit；Factor 的 codes 分 explicitness 与 form；Impact 有 evidence、modality，另有 generality 与 frame of reference 留在 replication package。
- Evidence / result table：Fig. 4 按 RQT model 投影 57 篇研究的 code distribution。正文给出关键数值：entity 与 factor 均在 57 篇中出现，但 24/57 entity 是 implicit；17/57 不报告 activity impact；agent 14/57；activity 40/57，且 37/40 为 ad hoc elicited；attribute 8/57；impact evidence 主要是 hypothesized 19/40，其次 inductive 11/40、referenced 10/40；context、cost、resource 覆盖很弱。
- Validity schema：Sect. 4.5 使用 internal / construct / external validity 组织威胁，特别指出 convenience sampling、implicit concept extraction、样本只限 empirical contributions 的边界。
- Roadmap streams：Sect. 5 不是普通 future work 清单，而是六条研究流：artifact and usage model、taxonomy of quality factors、impact framework、context factors、economic impact、tool support。
- Tool-support architecture：Fig. 5 给出 RQT tool 架构：requirements tracking system、requirements entities、agent assignment、organizational context 进入 entity characterization 与 context characterization，形成 quantified entities / quantified context，再进入 impact prediction，输出 estimated impact on affected activities；正文还列出 automatic entity characterization 与 automatic impact prediction 两个 automation modules。
- Artifact 字段：正文报告 replication package（Zenodo）和 RQT tool GitHub / Zenodo archived version，但本轮未核验其内容和当前可用性。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding path 是：RQT concepts -> extraction guideline / codes -> 57 篇 descriptive statistics -> interpretation -> roadmap streams。其主要解释不是“出现频次最高者即 finding”，而是：

- artifact-centric concepts 覆盖较好；
- activity-related concepts、context factors、economic concepts 覆盖不足；
- 这些缺口削弱 quality factors 的 practical relevance、external validity 和 industrial acceptance；
- 因此需要 reference artifact and usage model、quality factor taxonomy、impact framework、context factors、economic impact、tool support。

这一路径可迁移给 Paper2 的候选 finding ledger，但不能把 roadmap action 写成已验证解决方案，也不能把 57 篇 convenience sample 当作本库主统计池。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确但过粗 | `review.md` 将根节点写为 `Requirements quality research`，并判定为“理论 / 元模型概念树 + roadmap 树”。方向正确；但没有把三项贡献、显式评价 RQ、RQT-driven survey evaluation 放入根节点定义，导致 root 无法约束后续叶子。 | I |
| 主干分支是否覆盖原文 schema | 未覆盖 | 当前主干是“范围 / 语料 / 主题 / 方法 / 评价发现”五类通用接口。原文主干至少应包含 RQT concept model、survey protocol/codebook、code distribution/result evidence、validity、roadmap streams、tool architecture。 | I |
| 叶子维度是否足够具体 | 不足 | `review.md` 明确说六个 `leaf-*` 是通用接口，这降低了误读风险；但“原文模式候选叶子映射”只列 quality construct / theory model / evaluation method / roadmap question / boundary 五个粗粒度占位，没有展开 Entity、Factor、Agent、Activity、Attribute、Impact、Context、Cost、Resource、coding variables、roadmap streams 等真实叶子。 | I |
| 取值空间是否可执行 | 不足 | 当前叶子多写“自由文本”“完整枚举 / 层级枚举 / 自由文本加理由”“布尔、数值、链接状态”等泛类型。原文已经给出 explicit / implicit、ad hoc / systematic、hypothesized / inductive / referenced、necessary / possible、time / money 等可执行取值，但未入树。 | I |
| 关系边是否缺失 | 缺失 | 原文 Fig. 2 是关系型模型：Entity-Factor 形成 Entity-fact，Entity-fact produces Impact，Impact 作用于 Activity-fact，Activity-fact causes Cost，Context factors 影响 Impact 和 Cost。当前没有关系边表，也没有 Fig. 5 工具架构的 input-module-output 关系。 | I |
| 统计用途 / 分母是否正确 | 降级正确，但遗漏内部分母 | `review.md` 正确将该文排除出本库主统计池，避免 roadmap 污染 SUMMARY 定量统计；但原文本身有 57 篇 primary studies 的内部评价分母、6 篇 reliability sample、Fig. 4 concept coverage，这些应作为“原文内部统计字段”保留，并明确不等同于本库主统计池。 | I |
| 候选 finding 路径是否完整 | 不完整 | 当前只说“统计观察与候选发现”，没有复原 RQT concepts -> codes -> Fig. 4 coverage -> interpretation -> six roadmap streams 的链条，也没有记录哪些 roadmap stream 来自哪些缺口。 | I |
| A.1--A.4 证据链是否足够 | 结构有，证据不足 | A.1--A.4 表头齐全，且证据被降级为 `not_verified` / `weak` 是正确的；但 A.2 只有 4 条泛证据，原文页码写“待复核”，原文短引写“见释义”，表 / 图编号待核验，无法支撑全文级维度树复原。另 A.3 中 C12 前有空行，Markdown 渲染上可能脱离表格，影响结论映射闭合。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在中等风险 | `review.md` 的校准段明确“六个 leaf 不是原文叶子全集”，这是正面防护；但 C12 又说“已把原文抽取字段、分类项、模型节点或报告叶子列为候选”，而候选表并未忠实列出原文 schema，可能让 A2a 误以为只需精核五个占位叶子。 | I |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为忠实的原文 schema 复原。建议将正式树从“通用六叶接口”改为“原文 schema 树 + 本库迁移接口”的两层结构。下面是最小修复骨架。

### 4.1 根节点与主干

| 节点标识 | 名称 | 定义 | 取值空间 / 子节点 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| [dim-rq-roadmap-root] | RQT-driven requirements quality evaluation and roadmap | 原文以 RQT 统一理论、评价 57 篇 requirements quality factor 研究、再形成 roadmap。 | B0--B7 | 本库主统计池：否；原文内部评价：局部可统计 | 不适用时写 `not_applicable_to_sos_main_pool` | 摘要、引言贡献列表、Sect. 4 RQ、Sect. 5 roadmap |
| [dim-rq-roadmap-b0-framing] | 研究目标与贡献 | 贡献声明、显式 RQ、research commentary 类型与统计池排除理由。 | 贡献 1--3；RQ；review_type；boundary | 否 | `not_reported` / `not_applicable` | Page 1--2 摘要与贡献列表；metadata |
| [dim-rq-roadmap-b1-rqt-artifact] | RQT artifact-related concepts | Entity、Factor、Entity-fact 及 decomposition / characterization。 | 见叶子表 | 原文内部可统计 | `implicit` / `not_reported` / `not_verified` | Fig. 2、Table 1、Sect. 3.1、Fig. 4 |
| [dim-rq-roadmap-b2-rqt-activity-impact] | RQT activity / impact / context / economics concepts | Agent、Activity、Attribute、Activity-fact、Impact、Context factor、Cost、Resource 及关系边。 | 见叶子表和关系边表 | 原文内部可统计 | `not_reported` / `no_reported_impact` / `not_verified` | Fig. 2、Table 1、Sect. 3.1--3.2、Fig. 4 |
| [dim-rq-roadmap-b3-survey-protocol-codebook] | 状态评价语料与编码方案 | 57 篇样本、convenience sampling、extraction guideline、categorical variables、codes、extractor roles、reliability。 | sample / codebook / reliability | 原文内部可统计 | `not_in_package_checked` / `not_reported` | Sect. 4.1--4.2；replication package footnote |
| [dim-rq-roadmap-b4-evidence-results] | 证据表与统计观察 | Fig. 4 concept coverage、key counts、impact evidence distribution、context/cost/resource weakness。 | coverage table / result counts | 原文内部可统计 | `figure_not_verified` / `not_reported` | Fig. 4、Sect. 4.3--4.4 |
| [dim-rq-roadmap-b5-validity] | 效度与外推边界 | internal / construct / external validity。 | threat categories | 否；用于边界 | `not_reported` | Sect. 4.5 |
| [dim-rq-roadmap-b6-roadmap] | Roadmap streams | 六条 research streams 及其 triggering gap / required artifact / expected action。 | 六条枚举 | 候选 finding，不作完成型统计 finding | `aspirational_action` / `not_verified` | Sect. 5.1--5.6 |
| [dim-rq-roadmap-b7-tool-artifact] | Tool support 与开放制品 | Fig. 5 architecture、automation modules、replication package、RQT tool repo。 | architecture components / artifact status | artifact 字段可记录；当前未核验 | `reported_not_checked` / `link_not_checked` | Fig. 5、Sect. 5.6、footnotes |

### 4.2 叶子维度与候选取值空间

| 叶子标识 | 父节点 | 叶子维度 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| [leaf-rq-roadmap-contribution-type] | B0 | 贡献类型 | `harmonized_theory` / `state_evaluation` / `research_roadmap` | 否 | `not_reported` | 摘要、Page 2 贡献列表 |
| [leaf-rq-roadmap-evaluation-rq] | B0 | 显式评价 RQ | 自由文本：RQT concepts 如何被 requirements quality literature 报告 | 否 | `not_reported` | Sect. 4 开头 |
| [leaf-rqt-entity] | B1 | Entity | concept definition；code 可含 `explicit` / `implicit` | 是，分母 57 | `implicit` / `not_reported` | Fig. 2、Table 1、Fig. 4 |
| [leaf-rqt-factor] | B1 | Factor | explicitness：`explicit` / `referenced`；form：`textual_description` / `logical_or_mathematical_formula` 等 | 是，分母 57 | `not_reported` | Sect. 4.2、Fig. 4 |
| [leaf-rqt-entity-fact] | B1 | Entity-fact | Entity + Factor composition；示例可含 template conformance values | 局部可统计 | `not_reported` | Table 1、Fig. 3 |
| [leaf-rqt-agent] | B2 | Agent | person / group / automatism；reported / not_reported | 是，分母 57 | `not_reported` | Table 1、Fig. 4 |
| [leaf-rqt-activity] | B2 | Activity | reported activity；elicitation mode `ad_hoc` / `systematic`；sub-activity relation | 是，分母 57 或 40 | `not_reported` | Sect. 3.1、Sect. 4.3 |
| [leaf-rqt-attribute] | B2 | Attribute | measurable activity property，如 determinism、duration、agreement、readability | 是，分母 57 | `not_reported` | Table 1、Sect. 3.2、Sect. 4.4 |
| [leaf-rqt-activity-fact] | B2 | Activity-fact | Activity + Attribute composition | 局部可统计 | `not_reported` | Table 1、Fig. 2 |
| [edge-rqt-impact] | B2 | Impact 关系边 | source：Entity-fact；target：Activity-fact；evidence：`hypothesized` / `inductive` / `referenced`；modality：`necessary` / `possible`；另有 `generality` / `frame_of_reference` 待 package 核验 | 是，分母 40 或 57 | `no_reported_impact` / `not_reported` | Sect. 3.1、Sect. 4.2--4.3、Fig. 4 |
| [leaf-rqt-context-factor] | B2 | Context factor | product / process / project / people / organization / tool 等 Fig. 4 类别 | 是，分母 57 | `not_reported` | Fig. 4、Sect. 4.3--4.4 |
| [leaf-rqt-cost-resource] | B2 | Cost / Resource | resource：time / money 等；cost evidence：hypothesized / referenced / empirical_absent | 是，分母 57 | `not_reported` | Table 1、Sect. 4.3、Sect. 5.5 |
| [leaf-rq-roadmap-sample] | B3 | 样本与 sampling | 57 primary studies；non-probabilistic convenience sampling；source previous systematic study | 是，内部评价分母 57 | `sample_not_reconstructed` | Sect. 4.1 |
| [leaf-rq-roadmap-codebook] | B3 | Extraction guideline / codes | concept -> categorical variables -> codes；iteration refinement | 可作为 schema seed | `replication_package_not_checked` | Sect. 4.2、Zenodo footnote |
| [leaf-rq-roadmap-reliability] | B3 | Instrument validation | 6 publications；2 training；4 reliability；agreement 83.3%、Kappa 54.2%、S-Score 76.8% | 是 | `not_reported` | Sect. 4.2 |
| [leaf-rq-roadmap-coverage-results] | B4 | Concept coverage 统计 | Fig. 4 各 concept count 与 code distribution | 是，内部评价分母 57 | `figure_not_verified` | Fig. 4、Sect. 4.3 |
| [leaf-rq-roadmap-interpretation-gap] | B4 | 缺口解释 | artifact-centric covered；activity/context/economic neglected；practical relevance risk | 候选 finding | `author_interpretation_only` | Sect. 4.4 |
| [leaf-rq-roadmap-validity-threat] | B5 | 效度威胁 | internal / construct / external validity；sampling、implicit extraction、empirical-only sample | 否；边界字段 | `not_reported` | Sect. 4.5 |
| [leaf-rq-roadmap-stream] | B6 | Roadmap stream | `artifact_and_usage_model` / `quality_factor_taxonomy` / `impact_framework` / `context_factors` / `economic_impact` / `tool_support` | 否；candidate action | `aspirational_action` | Sect. 5.1--5.6 |
| [leaf-rq-roadmap-tool-architecture] | B7 | Tool-support architecture | inputs：requirements entities、agent assignment、organizational context；modules：entity characterization、context characterization、impact prediction；outputs：estimated impact | 否；tool seed | `reported_not_checked` | Fig. 5、Sect. 5.6 |
| [leaf-rq-roadmap-artifact-status] | B7 | Open artifacts | replication package Zenodo；RQT tool GitHub / Zenodo archive；status：reported / checked / unavailable | artifact 字段可记录 | `reported_not_checked` | Sect. 4 footnote、Sect. 5.6 footnotes |

### 4.3 关系边最小表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| [edge-rqt-entity-decomposes] | Entity | decomposes into | Entity | 层级实体 | `not_reported` | Fig. 2、Sect. 3.1 |
| [edge-rqt-factor-decomposes] | Factor | decomposes into | Factor | sub-factor 层级 | `not_reported` | Fig. 2、Sect. 3.1 |
| [edge-rqt-factor-characterizes-entity] | Factor | characterizes | Entity / Entity-fact | factor evaluation | `not_reported` | Fig. 2、Table 1 |
| [edge-rqt-entity-used-in-activity] | Entity | is used in | Activity | requirements-affected activity | `not_reported` | Fig. 2、Sect. 3.1 |
| [edge-rqt-agent-involved-in-activity] | Agent | is involved in | Activity | person / group / automatism | `not_reported` | Fig. 2、Table 1 |
| [edge-rqt-entity-fact-produces-impact] | Entity-fact | produces | Impact | impact relation | `no_reported_impact` | Fig. 2、Sect. 3.1 |
| [edge-rqt-impact-to-activity-fact] | Impact | affects | Activity-fact | evidence / modality / model form | `no_reported_impact` | Fig. 2、Sect. 4.3 |
| [edge-rqt-context-influences-impact-cost] | Context factor | influences | Impact / Cost | context category | `not_reported` | Fig. 2、Sect. 3.1、Sect. 5.4 |
| [edge-rqt-activity-fact-causes-cost] | Activity-fact | causes | Cost / Resource | time / money / resource | `not_reported` | Fig. 2、Sect. 5.5 |
| [edge-rqt-tool-pipeline] | Requirements entities / context | feeds module | Entity characterization / Context characterization / Impact prediction | architecture component | `reported_not_checked` | Fig. 5 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 将正式维度树从通用五主干 / 六叶子改为原文 schema 树 | `review.md` 的 `## 维度树复原`、`根问题 / RQ 到主干分支映射`、`维度树结构` | 根节点保留 theory/evaluation/roadmap 边界，但主干改为 RQT concept model、survey protocol/codebook、evidence results、validity、roadmap streams、tool architecture；通用六接口可降为“本库迁移接口”而非原文树。 | 摘要 / Page 2 贡献列表；Sect. 3--5；Fig. 2 / Table 1 / Fig. 4 / Fig. 5 | I |
| 展开 RQT 概念叶子和关系边 | `叶子维度表` 与新增 `关系边表` | 至少列 Entity、Factor、Entity-fact、Agent、Activity、Attribute、Activity-fact、Impact、Context factor、Cost、Resource，并记录 Fig. 2 关系边。 | Fig. 2、Table 1、Sect. 3.1 | I |
| 补充 extraction guideline / coding scheme | `原文模式候选叶子映射（A1 种子）` 或新增 `编码方案复原` | 从“评价方法”粗项改为 concept -> categorical variables -> codes；记录 explicit/implicit、factor explicitness/form、impact evidence/modality，以及 generality/frame of reference 在 replication package 待核验。 | Sect. 4.2；replication package footnote | I |
| 保留原文内部 57 篇评价分母，不混入本库主统计池 | `统计与候选发现链路` | 写明本库主统计池为否，但原文内部 survey evaluation 以 57 篇 primary studies 为分母；Fig. 4 数字属于原文内部统计，不是 survey_of_surveys 跨论文统计。 | Sect. 4.1--4.3、Fig. 4 | I |
| 补充 finding path | `统计与候选发现链路`、A.3 | 建立 RQT concept coverage -> interpretation gap -> six roadmap streams 的结论映射；每条 roadmap stream 标注 triggering gap 和“candidate action / not completed finding”。 | Sect. 4.3--4.4、Sect. 5.1--5.6 | I |
| 补充 validity / artifact 字段 | `叶子维度表`、A.2、A.4 | 加 internal / construct / external validity；加 replication package 与 RQT tool repo 的 `reported_not_checked` 状态，避免写成已核验 artifact。 | Sect. 4.5；Sect. 4 footnote；Sect. 5.6 footnotes | I |
| 精化 A.2 证据账本 | `审计附录 A.2` | 将 4 条泛证据拆成 Fig. 2、Table 1、Sect. 4.2、Fig. 4、Sect. 4.5、Sect. 5.1--5.6、Fig. 5 等证据；补精确 PDF 页码、图表编号、短释义；仍未核验 replication package 的证据保持 `not_verified`。 | 本轮 PDF 已核对 Page 510--511、514、516--517；supplementary 未核验 | I |
| 修复 A.3 表格断裂 | `审计附录 A.3` | 删除 C09 与 C12 之间的空行，确保 C12 是同一张结论-证据映射表的行；否则 Markdown 渲染可能破坏 A.3 闭合。 | `review.md` 当前 A.3 C12 前存在空行 | I |
| 更新 PDF 核验状态时保持边界 | `A.4 本地复验命令与人工核验清单` | 可把 Fig. 2、Table 1、Fig. 4、Fig. 5 标为已人工核对；但 replication package、RQT tool repo、Fig. 4 全部细粒度 code 仍需后续核验。 | 本轮 PDF 临时渲染核对；未核验外部 artifacts | M |

## 6. C/I/M 结论

- C：无。当前 `review.md` 已明确将该文降级为 `boundary_anchor` / `schema_seed`，并把证据标为 `not_verified` / `weak`，没有把 roadmap / vision / proposal 写成完成型统计 finding，也没有把该文纳入本库主统计池。
- I：存在多项。最核心 I 是正式“维度树复原”仍以通用六 leaf 接口为主，原文 RQT concept model、extraction guideline / coding scheme、Fig. 4 evidence table、57 篇内部评价分母、validity、six roadmap streams、Fig. 5 tool architecture 和 artifact 状态没有被结构化复原。这会实质影响 Paper2 的维度模式库、A2a 精核任务和后续证据链可靠性。
- M：PDF 核验状态和 A.4 可进一步细化；若维护者接纳本轮审计，可把已核对的 Fig. 2、Table 1、Fig. 4、Fig. 5 与仍未核验的 replication package / tool repo 分开记录。
- 最终建议：NEEDS FIX。
