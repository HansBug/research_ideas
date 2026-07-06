我已完成所有必要文件的读取。现在产出完整的 A1-DT v2 单篇审计报告。

`★ Insight ─────────────────────────────────────`
关键发现：这篇论文有两层"树"——RQT 概念元模型（11 concepts, §3）与 §4 evaluation 阶段把 RQT concepts 转成的 categorical codebook。后者才是真正的样本编码维度树，主干就是 11 个 RQT 概念，叶子是每个概念的 categorical codes（如 Entity: explicit/implicit；Factor: explicitness × form；Impact: 4 dimensions × multiple codes）。当前 review.md 的"原文 schema 主树"6 行抽象主干和"原文模式候选叶子映射"5 行 schema_seed 都没有把这套真实 codebook 列出来。
`─────────────────────────────────────────────────`

---

# A1-DT v2 单篇审计报告 — `requirements-quality-theory-roadmap`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `requirements-quality-theory-roadmap` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；通读 14 页全文（Page 1–Page 14 含 References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两份均已读，且交叉核对元信息 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅基于 text 审计，未做 PDF 版面核验（图 Fig. 2/4/5、Table 1 字段对齐留待 A2a） |
| 原文类型 | research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） |
| 被编码样本单位 | primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） |
| 样本数量 / 分母 | n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-reported 子集为 40） |
| 原生树类型 | **维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 |
| 主统计池资格 | **局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` |
| 总体判定 | **needs repair**：现有 `review.md` 已记录 RQT 11 concept 与统计数字，但"维度树复原"部分把 codebook 用六个通用接口叶子（scope/corpus/taxonomy/method/evidence/finding）替代了；"原文 schema 主树"6 行只给主干种子，没有把每个 RQT concept 的 codes / 取值空间显式列叶。需要把 §4 codebook 抬升为原生树主事实源。 |

---

## 1. 原文证据阅读说明

实际读取的本地文件与覆盖范围：

1. `bibtex.bib` 完整 — 锁定 Frattini et al. 2023, *Requirements Engineering* 28(4):507–520, DOI 10.1007/s00766-023-00405-y。
2. `metadata.json` 完整 — 已知 `eligible_for_statistical_synthesis: false`、`evidence_role: theory_roadmap_schema_seed`、`systematic_evidence_status: non_systematic_or_boundary_anchor`，与本审计判定一致。
3. `paper_content.txt` 通读 Page 1–14 全文，含摘要、§1–§6、References。
4. `paper.pdf` 未在本轮打开（Fig. 2 RQT 概念图、Fig. 3 example 实例化、Fig. 4 codes 分布柱状、Fig. 5 tool architecture、Table 1 concept origins 留待 A2a 版面核验）。
5. `review.md` 完整阅读（含 §1–§7 与"维度树复原"与 A.1–A.4 附录）。

关键证据锚点（5–12 条）：

1. **Page 2，§1 contributions**："(1) A harmonized requirements quality theory… (2) A survey of requirements quality research… (3) A consequent research roadmap"。三段式贡献声明，决定森林型结构。
2. **Page 4，§3.1 + Fig. 2 + Table 1**：RQT 概念 = `Entity / Factor / Entity-fact / Agent / Activity / Attribute / Activity-fact / Impact / Context factor / Cost / Resource`，共 11 concepts，每个有 origin 引用。这是**树 A**。
3. **Page 7，§4.1**："a sample of 57 primary studies… non-probabilistic, more specifically convenience sampling"。锁定样本单位、分母与抽样性质。
4. **Page 7，§4.2 instrument design**："Each concept of the RQT was associated with one or more categorical variables, each containing a set of codes that represented if and how the concept was reported. The codes were created ad hoc in the first iteration of extraction and refined based on discussions and theoretical background in the second iteration."。**这是树 B 的存在证据**。
5. **Page 7，§4.2 entity codes 示例**："codes that represent how the concept entity is reported are, for example, explicit and implicit"。
6. **Page 7，§4.2 factor codes 示例**："the codes of the concept Factor were split into two groups, representing both the explicitness… and the form"。
7. **Page 7–8，§4.2 reliability**：percentage agreement 83.3%、Cohen's Kappa 54.2%、S-Score 76.8%；两人编码、6 篇约 10% 验证子样（其中 2 篇训练、4 篇正式计算）。
8. **Page 8，§4.3 results**：分子分母枚举 — Entity implicit 24/57（42.1%）；Impact N/A 17/57（29.8%）；Agent 14/57（24.6%）；Activity ad hoc 37/40（92%）；Attribute 8/57（14%）；Impact evidence hypothesized 19/40、inductive 11/40、referenced 10/40；Context factor 范围 0%–24.6%；Cost 9/57（15.8%）；Resource 5/57（8.8%）。
9. **Page 8，§4.3 impact dimensions**："We grouped the codes classifying how impact is reported into four distinct dimensions, two of which are reported here…"。Impact 有 **4 个子维度**：evidence、modality、generality、frame of reference；其中后两个原文未报告但作者声明编码存在。
10. **Page 9–10，§5 roadmap**：6 streams = artifact/usage model、taxonomy of quality factors、impact framework（升级自 taxonomy of impacts）、context factors、economic impact、tool support。
11. **Page 11，§5.6 + Fig. 5**：tool architecture 含 entity characterization + impact prediction model；并提到 GitHub `JulianFrattini/rqt-tool`（本轮未核验）。
12. **Page 8，§4.5 threats**：external validity = 样本仅 empirical contributions；construct = 隐式 concept 抽取困难。

未做 PDF 版面核验的部分：Fig. 4 柱状图实际数值与文本数字是否一致；Table 1 origin 引用列；Fig. 2 关系箭头方向；replication package（Zenodo 8167598）字段定义。

---

## 2. 样本单位与字段来源判定

**Q1 — 原文逐项编码的对象是什么？**
是 requirements quality 文献中的 primary study（一篇一项）。Page 7 明确："a sample of 57 primary studies"，每篇被 RQT codebook 编码一次。

**Q2 — 作者是否做了系统检索 / 纳排 / 抽取 / 编码方案？**
- 系统检索：**否，未新做**。样本直接借用作者团队前作 Frattini et al. 2022 quality-factor ontology study（arXiv 2206.05959）的 57 篇 sample，作者明确标注为 convenience sampling。
- 抽取方案：**有**。基于 RQT concepts 构建 extraction guideline，每个 concept 关联 ≥1 个 categorical variable，每个 variable 含若干 codes（codes 在第一轮 ad hoc 生成，第二轮基于讨论与理论背景精炼）。
- 编码方案：第一作者全样本编码，第二作者在 6 篇随机子样（2 篇训练 + 4 篇正式）独立编码，计算 percentage agreement / Cohen's Kappa / S-Score。

**Q3 — 字段来源**：来自 §4.2 extraction guideline 与 §4.3 results 中显式提到的 codes、replication package（Zenodo），与 §3 RQT 11 concepts 的对应映射。

**Q4 — RQ 与样本单位的关系**：唯一显式 RQ = "How are the concepts of the requirements quality theory reported in requirements quality literature?"（Page 7）。RQ 把 RQT 概念当作**编码字段集合**，把 57 篇当作**被编码样本**，结果是**字段在样本中的报告频次与方式分布**。RQ 本身不构成树根，而是把树 A（RQT 概念）作为字段、应用到样本上、产出统计观察。

**Q5 — 是否要降级？**
**部分降级**：
- 该文不是新做的 SLR/SMS，而是 viewpoint + 内部 survey + roadmap。
- 但它有真实样本（n=57）、有 codebook、有 reliability、有 descriptive statistics。
- 对本文自身而言：可作内部统计；对 Paper2 而言：仅作 `schema_seed / methodological_seed / boundary_anchor`，不进入跨论文 SLR/SMS 主统计池。这与 metadata.json `eligible_for_statistical_synthesis: false` 一致。

---

## 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**（A + B + C 三树），其中 **树 B = 样本编码维度树**，是 A1-DT v2 关注的真正主树。

### 树 A：RQT 概念元模型（§3, Fig. 2, Table 1）

```text
RQT 概念元模型 (theory layer)
├── artifact-related layer
│   ├── Entity            — 需求制品或其组成（specification/section/paragraph/sentence/requirement）
│   ├── Factor            — 对 entity 的规范性度量；可分解为 sub-factor
│   └── Entity-fact       — entity × factor 的具体取值（如 user story 的 conformance = missing role）
├── activity-related layer
│   ├── Agent             — 人、群体或自动化机制
│   ├── Activity          — 以 entity 为输入并产生输出的 requirements-affected activity
│   ├── Attribute         — activity 的可测属性（determinism、duration、readability …）
│   └── Activity-fact     — activity × attribute 的具体取值
├── impact / context layer
│   ├── Impact            — entity-fact 对 activity-fact 的关系（可分类 / 线性 / 非线性 / 回归）
│   └── Context factor    — 影响 impact 的外部因素（组织、过程模型、产品、工具、人员）
└── economic layer
    ├── Cost              — activity-fact 的经济量级
    └── Resource          — 受影响的资源类型（time / money / …）
```

### 树 B：§4 extraction codebook（**真正的样本编码维度树**）

> 这是 §4.2 extraction guideline 中"每个 RQT concept 关联 ≥1 个 categorical variable + codes"的真实复原。Page 8 §4.3 提到的所有 codes 与分母都来自此树。文本明确列出的 codes 完整列出；文本未展开但暗示存在的 codes 标 `待核验 (Zenodo replication package)`。

```text
[B] Sample coding tree — RQT codebook applied to 57 primary studies
│
├── Entity reporting
│   └── entity.explicitness ∈ {explicit, implicit}
│       — Page 7 显式定义；Page 8 implicit = 24/57 = 42.1%
│
├── Factor reporting
│   ├── factor.explicitness ∈ {explicitly_reported, referenced_from_another_publication}
│   │   — Page 7 §4.2 显式
│   └── factor.form ∈ {textual_description, logical_or_mathematical_formula}
│       — Page 7 §4.2 显式
│
├── Entity-fact reporting     ⟵ 文本未展开 codes（待 Zenodo 核验）
│
├── Agent reporting
│   └── agent.presence ∈ {reported, not_reported}
│       — Page 8 reported = 14/57 = 24.6%
│
├── Activity reporting
│   ├── activity.presence ∈ {reported, not_reported}
│   │   — 当 reported 时分母 = 40
│   └── activity.elicitation_mode ∈ {ad_hoc, systematic}
│       — Page 8 ad_hoc = 37/40 = 92%
│
├── Attribute reporting
│   └── attribute.presence ∈ {reported, not_reported}
│       — Page 8 reported = 8/57 = 14%
│
├── Activity-fact reporting   ⟵ 文本未展开 codes（待 Zenodo 核验）
│
├── Impact reporting          ⟵ 4 dimensions（only 2 reported in paper）
│   ├── impact.presence ∈ {reported, N_A}
│   │   — Page 8 N/A = 17/57 = 29.8%；reported 分母 = 40
│   ├── impact.evidence ∈ {hypothesized, inductive, referenced}
│   │   — Page 8 hypothesized 19/40、inductive 11/40、referenced 10/40
│   ├── impact.modality ∈ {necessary, possible}
│   │   — Page 8 "balanced between necessary and possible"
│   ├── impact.generality          ⟵ 编码存在但 Page 8 "yielded no additional insight"
│   └── impact.frame_of_reference  ⟵ 编码存在但 Page 8 "yielded no additional insight"
│
├── Context factor reporting
│   └── context_factor.sub_category ∈ {tool, product, organization, process, people, …}
│       — Page 8 tool = 0/57；product = 14/57 = 24.6%；其他子类待 Zenodo 核验
│
├── Cost reporting
│   ├── cost.presence ∈ {reported, not_reported}
│   │   — Page 8 reported = 9/57 = 15.8%
│   └── cost.evidence ∈ {hypothesized, referenced, empirical}
│       — Page 8 "only hypothesized or referenced, never determined empirically"
│
└── Resource reporting
    ├── resource.presence ∈ {reported, not_reported}
    │   — Page 8 reported = 5/57 = 8.8%
    └── resource.type ∈ {money, time, …}
        — Page 8 "money and time are mentioned"；其他类型待 Zenodo 核验
```

### 树 C：§5 roadmap streams（候选 finding 树）

```text
[C] Roadmap streams
├── 5.1 Artifact and usage model       — 含 reference activity model & attributes
├── 5.2 Taxonomy of quality factors    — 基于 quality-factor ontology
├── 5.3 Impact framework               — 升级自原 taxonomy of impacts；引入回归 / Bayesian
├── 5.4 Context factors                — RE 专属 context factor 集合
├── 5.5 Economic impact                — 把 activity-fact 关联到 cost/resource
└── 5.6 Tool support                   — entity & context characterization + impact prediction
```

### 当前 review.md 缺失的部分

- 把 §4 codebook（树 B）当作"原文 schema 主树"完整列出。
- 把 Impact 的 4 个子维度（evidence / modality / generality / frame_of_reference）显式列叶。
- 把 Factor 的 explicitness × form 两组 codes 显式列叶。
- 把 Cost 与 Resource 的 sub-codes（evidence、type）显式列叶。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `B.entity.explicitness` | 实体显式性 | Entity reporting | §4.2 显式给出 | 一篇文献是否清晰报告 entity 的 scope 与 form | {explicit, implicit} | 完整枚举 | 不报告时默认 implicit | 分子/57；implicit = 24/57 | "术语模糊"型 gap finding | 可迁移为 Paper2 中字段 explicit/implicit 二分；不迁移 RE 领域结论 |
| `B.factor.explicitness` | 因子显式性 | Factor reporting | §4.2 显式 | 因子是本文显式定义还是引用其他文献 | {explicitly_reported, referenced_from_another_publication} | 完整枚举 | 所有 57 篇都报告 factor，无缺失 | 分子/57 | 引用链型 finding 候选 | 可迁移结构；不迁移 RE factor 具体集合 |
| `B.factor.form` | 因子形式 | Factor reporting | §4.2 显式 | 因子是文字描述还是数学/逻辑公式 | {textual_description, logical_or_mathematical_formula} | 完整枚举 | 默认 textual | 分子/57 | 形式化程度型 finding | 可迁移；Paper2 字段可同构分"文本/形式化" |
| `B.agent.presence` | Agent 报告与否 | Agent reporting | §4.3 | 是否报告活动中的 agent | {reported, not_reported} | 布尔 | not_reported | 14/57 = 24.6% | activity-side gap finding | 可迁移 |
| `B.activity.presence` | Activity 报告与否 | Activity reporting | §4.3 | 是否报告 impacted activity | {reported, not_reported} | 布尔 | not_reported；进入 17/57 N/A | 40/57 reported | gap finding | 可迁移 |
| `B.activity.elicitation_mode` | Activity 识别方式 | Activity reporting | §4.3 | activity 是 ad hoc 引出还是系统性识别 | {ad_hoc, systematic} | 完整枚举 | 仅当 activity reported 时生效，分母 40 | 37/40 = 92% ad_hoc | "非系统性 activity"型 finding | 可迁移 |
| `B.attribute.presence` | Attribute 报告与否 | Attribute reporting | §4.3 | 是否报告 activity 的可测属性 | {reported, not_reported} | 布尔 | not_reported | 8/57 = 14% | measurement gap finding | 可迁移 |
| `B.impact.presence` | Impact 报告与否 | Impact reporting | §4.3 | 是否报告 factor → activity 的 impact | {reported, N_A} | 布尔 | N/A 计 17/57 | reported 分母 = 40 | core gap finding | 可迁移 |
| `B.impact.evidence` | Impact 证据类型 | Impact reporting | §4.3 | impact 关系的证据基础 | {hypothesized, inductive, referenced} | 完整枚举 | 仅当 impact reported；分母 40 | 19 / 11 / 10 of 40 | "证据等级"型 finding | 可迁移为 Paper2 evidence_type 字段 |
| `B.impact.modality` | Impact 模态 | Impact reporting | §4.3 | impact 是必然还是可能 | {necessary, possible} | 完整枚举 | impact reported 子集 | "balanced" 文本表述 | "确定性 vs 可能性"分布 finding | 可迁移 |
| `B.impact.generality` | Impact 普适性 | Impact reporting | §4.3 提到但未展开 | impact 是普遍还是上下文特异 | 待核验（Zenodo） | 待核验 | 文本声明"no additional insight"故未报告 | 不进入本文统计 | A2a 补叶后可作 finding 候选 | 取值空间未核验前不得统计 |
| `B.impact.frame_of_reference` | Impact 参照系 | Impact reporting | §4.3 提到但未展开 | impact 的参照对象 | 待核验（Zenodo） | 待核验 | 同上 | 不进入本文统计 | A2a 补叶后可作 finding 候选 | 同上 |
| `B.context_factor.sub_category` | Context 子类 | Context factor reporting | §4.3 | 报告了哪类 context（tool / product / organization / process / people …） | tool, product (named), other（待 Zenodo 补全） | 层级枚举 | 多数为 0 报告 | tool=0；product=14/57；其他待核 | "context 忽视"型 gap finding | 可迁移为 Paper2 context 多类字段 |
| `B.cost.presence` | Cost 报告与否 | Cost reporting | §4.3 | 是否报告经济成本 | {reported, not_reported} | 布尔 | not_reported | 9/57 = 15.8% | economic gap finding | 可迁移 |
| `B.cost.evidence` | Cost 证据类型 | Cost reporting | §4.3 | cost 的证据基础 | {hypothesized, referenced, empirical(=0 在本样本)} | 完整枚举 | cost reported 子集；分母 9 | "never empirically determined" | empirical-evidence gap | 可迁移 |
| `B.resource.presence` | Resource 报告与否 | Resource reporting | §4.3 | 是否报告 resource 类型 | {reported, not_reported} | 布尔 | not_reported | 5/57 = 8.8% | resource gap finding | 可迁移 |
| `B.resource.type` | Resource 类型 | Resource reporting | §4.3 | 受影响 resource 的具体类型 | {money, time, …待 Zenodo} | 部分枚举 | resource reported 子集；分母 5 | money / time 文本提及 | 资源类型分布 finding | 可迁移；类型空间需 A2a 扩展 |
| `B.entity_fact.codes` | Entity-fact codes | Entity-fact | §3 概念存在；§4 文本未展开 | entity × factor 的取值表达方式 | 待核验（Zenodo） | 待核验 | 视为 entity + factor 联合 | 不进入本文统计 | 复合事实型 finding 入口 | 取值空间未核验前不得统计 |
| `B.activity_fact.codes` | Activity-fact codes | Activity-fact | §3 概念存在；§4 文本未展开 | activity × attribute 的取值表达方式 | 待核验（Zenodo） | 待核验 | 视为 activity + attribute 联合 | 不进入本文统计 | 同上 | 同上 |

---

## 5. 关系边表

本文 RQT 是**显式关系型模型**（Fig. 2 即关系图）。关系边来自树 A（概念模型），而非树 B（codebook）。树 B 是字段-codes 平面表，本身没有关系边。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `R1.entity_compose` | Entity | decomposes_into | Entity (sub-entity) | 递归 entity 类型 | 单层 entity 不报告 sub-entity | §3.1 Page 4 | 表达需求粒度层级 |
| `R2.factor_compose` | Factor | decomposes_into | Factor (sub-factor) | 递归 factor 类型 | 单层 factor 不报告 sub-factor | §3.1 Page 4（Antinyan 例） | 表达复合因子 |
| `R3.entity_fact` | Entity × Factor | composes | Entity-fact | 由 entity 与 factor 联合定义 | 未取值时不存在 entity-fact | Table 1 Page 5 | 编码具体观测 |
| `R4.activity_compose` | Activity | decomposes_into | Activity (sub-activity) | 递归 | 单层 activity 不分解 | §3.1 Page 4–5 | 表达 understanding 等子活动 |
| `R5.activity_fact` | Activity × Attribute | composes | Activity-fact | 由 activity 与 attribute 联合定义 | 未取值时不存在 activity-fact | Table 1 Page 5 | 编码活动观测 |
| `R6.impact` | Entity-fact | impacts | Activity-fact | 关系模型：categorical / linear / regression / Bayesian | impact 不报告 = N/A | §3.1 generalised impact, Page 5 | 核心因果/关系边 |
| `R7.context_modulates` | Context factor | modulates | Impact (Entity-fact→Activity-fact 关系) | 同 impact 取值空间 | context 不报告 = 假设统一上下文 | §3.1 Page 5 + 例 Page 6 | 解释外部效度 |
| `R8.activity_fact_cost` | Activity-fact | incurs | Cost | cost 数值或量级 | 不报告 = 无 economic 维度 | §3.1 Page 5 | 经济关系边 |
| `R9.cost_resource` | Cost | consumes | Resource | money / time / … | 不报告 resource 时 cost 抽象 | §3.1 Page 5 | 资源映射边 |
| `R10.agent_activity` | Agent | performs | Activity | agent 类型 | activity 不报告 agent 时假设隐式 agent | §3.1 Page 5 | 人/工具归属 |

当前 `review.md` 完全没有关系边表（A1-DT v2 schema 要求显式列出）。这是一个 I 级返修项。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 由字段 / 统计表支持的统计观察（仅限本文样本 n=57，convenience）

1. Entity-explicitness：implicit = 24/57 (42.1%)。
2. Factor：所有 57 篇都报告 factor；explicitness 与 form 子分布作者文本未展开数字。
3. Agent：reported = 14/57 (24.6%)。
4. Activity：reported = 40/57；其中 ad_hoc elicited = 37/40 (92%)。
5. Attribute：reported = 8/57 (14%)。
6. Impact：N/A = 17/57 (29.8%)；reported 40/57 中 evidence = hypothesized 19 / inductive 11 / referenced 10；modality "balanced"。
7. Context factor：tool = 0%；product-related = 14/57 (24.6%)。
8. Cost：reported = 9/57 (15.8%)；从未 empirically determined。
9. Resource：reported = 5/57 (8.8%)；types 提及 money、time。
10. Reliability：percentage agreement 83.3%；Cohen's κ = 54.2%（作者标 moderate，并自陈受 uneven marginal 影响）；S-Score = 76.8%。

### 6.2 原文 discussion / recommendation / roadmap 候选 finding

1. requirements quality literature 实现 artifact-centric 偏置，activity / context / economic 覆盖严重不足（§4.4 + §6）。
2. 32/40 reported activities 涉及 understanding/interpretation 子活动 → 暗示 interpretation 是关键 sub-activity（§5.1）。
3. roadmap 6 streams 是 gap → action 的直接映射（§5.1–§5.6）。
4. impact 应升级为 framework 而非 taxonomy（§5.3）。

### 6.3 对 Paper2 可迁移的方法学启发

1. 把 researcher-defined meta-model 当作"第一贡献"，再用 codebook 把 meta-model 转成可统计变量。
2. 用 inter-rater reliability + 双人编码 + replication package 验证 codebook。
3. 把 gap 分布转成 roadmap action 而不是停留在频次。
4. 显式区分 impact 的 4 个子维度（evidence / modality / generality / frame_of_reference）作为字段冗余/正交检验。

### 6.4 绝不可迁移的领域结论

1. RE 领域中 entity-implicit / impact-N/A 等具体比例。
2. RQT 11 个具体 concept 名（Entity、Factor 等不能直接套用到 SLR/SMS 的 Paper、Field 等对象）。
3. roadmap 6 streams 的具体名称与内容（属 RE 领域 future work，不是 Paper2 的）。
4. quality-factor ontology、AMDiRE、Quamoco、ABRE-QM 等被引工具的具体可用性。

---

## 7. 对现有 `review.md` 的返修建议

| 等级 | 位置 | 问题 | 返修建议 |
|---|---|---|---|
| **C** | "维度树复原" → "原文 schema 主树（19×3 审计后返修）" | 仅 6 行抽象主干（construct / rqt / evidence-base / coding / roadmap / boundary），没把 §4 codebook 的 11 concept × 各自 codes 列为叶子；与 metadata.json 已记录的 57 篇分母、§4.3 多条数字脱节。 | 把当前第 3 节的**叶子维度表 17 行**直接落入 review.md，作为"原文 schema 主树（B 树：sample coding codebook）"事实源；保留树 A（RQT 概念）与树 C（roadmap streams）为独立子树；保留通用六叶接口为投影 |
| **C** | "维度树复原" 缺关系边表 | A1-DT v2 schema 要求显式列出关系边，本文 RQT 是关系型理论，必须列。 | 落入本审计第 5 节的 10 条关系边 R1–R10 |
| **I** | §1 快速结论卡片 / "维度树复原" → 一句话结论 | 当前写"不进入主统计池"过早一刀切；实际上 57 篇内部统计对 Paper2 是 schema_seed 可参考。 | 改为"内部 n=57 可作 schema_seed / 局部可统计观察；不进入 Paper2 跨论文 SLR/SMS 主统计池" |
| **I** | "原文模式候选叶子映射（A1 种子）" | 5 行候选叶（quality-construct / theory-model / evaluation-method / roadmap-question / boundary）名称泛、与本文实际 codes 不对应，掩盖了 §4 真实 codebook 的存在。 | 用 17 个 `B.*` 叶替换；保留 5 行旧候选叶作为"已迁移历史草稿，不作事实真源"形式归档 |
| **I** | A.2 证据账本 | 只列 4 行宏观证据（root/taxonomy/stat/risk），全部 `not_verified`；漏掉 Page 7 §4.2 codebook 锚点（最关键的一条）与 Page 8 数字锚点（11 条）。 | 至少新增：EV-…-005 `§4.2 codebook 设计`、EV-…-006 `§4.3 17 个分子分母数字`、EV-…-007 `reliability metrics 83.3/54.2/76.8`、EV-…-008 `§5 roadmap 6 streams`、EV-…-009 `Fig. 2 关系图（待 PDF 核验）` |
| **I** | A.3 结论-证据映射 | C04 `taxonomy` 等结论目前仅指向 EV-002 单一证据；与新增 codebook / numerical / reliability 证据无映射。 | 在 C04–C07 上补 EV-005/006/007 引用；新增 C10 = "57 篇 codebook + reliability 构成本文内部可统计基线但 convenience sampling 限制外推" |
| **M** | "六类 pattern 抽取" 表 | 已整体合格；只是 dimension pattern 行写"RQT concepts"作为维度，可补一句"对应 codebook 实际是 §4.2 categorical variables + codes" | 补一句说明，不必重写 |
| **M** | "待复核" 第 3、4 项 | replication package（Zenodo 8167598）与 rqt-tool GitHub 仓库均未访问 | 标注为 A2a 必访资产；优先核 Zenodo 以补 impact.generality / frame_of_reference、entity_fact codes、activity_fact codes、context sub_categories 完整取值空间 |
| **M** | 元信息 | metadata.json 中 `current_fulltext_status` 已注明"图表级细节按单篇待复核说明处理"；A.4 已记 `cmd-...-visual-check = needs_manual_check` | 保持不变 |

SUMMARY 当前表中字段是否需修正：
- "样本单位 / 样本数量 / 原生树类型 / 统计池资格" 应改为 "样本单位 = primary study（借用 Frattini 2022 样本）；n=57；原生树 = 维度森林（A 概念 / B codebook / C roadmap）；主统计池资格 = 本文内部可统计，跨 Paper2 SLR/SMS 不入主池"。

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-rqtr-005 | paper_content.txt | §4.2 Study design | Page 7 段 "we maintained two artifacts… extraction guideline based on the RQT concepts" | "Each concept of the RQT was associated with one or more categorical variables… containing a set of codes that represented if and how the concept was reported" | codebook_design | confirmed_text | 树 B 全部 17 个 `B.*` 叶 + 父节点 | 否（文本明确） | 仅本文 codebook；具体 codes 完整集合需 Zenodo 8167598 核验 |
| EV-rqtr-006 | paper_content.txt | §4.3 Study results | Page 8 整段含 24/57、17/57、14/57、40/57、37/40、8/57、19/40、11/40、10/40、24.6%、9/57、5/57 | "24/57 = 42.1% implicit"、"17/57 N/A"、"14/57 agents"、"37/40 ad hoc"、"8/57 attributes"、"hypothesized 19/40, inductive 11/40, referenced 10/40"、"product-related 14/57 = 24.6%"、"cost 9/57"、"resource 5/57" | numerical_distribution | confirmed_text | `B.entity.explicitness` / `B.agent.presence` / `B.activity.*` / `B.attribute.presence` / `B.impact.*` / `B.context_factor.sub_category` / `B.cost.presence` / `B.resource.presence` | 是（Fig. 4 柱状对照） | 仅 57 篇 convenience sample；不可跨域外推 |
| EV-rqtr-007 | paper_content.txt | §4.2 Reliability | Page 7–8 "task overlap achieved… 83.3%… Cohen's Kappa 54.2%… S-Score 76.8%" | 同左 | reliability_metric | confirmed_text | 整个 codebook 与 §4.3 结果的可信度边界 | 否 | Cohen's κ 在 uneven marginal 下不可靠，故作者引入 S-Score |
| EV-rqtr-008 | paper_content.txt | §5 Roadmap | Page 9–11 §5.1–§5.6 标题与正文 | "1. Artifact and usage model … 2. Taxonomy of quality factors … 3. impact framework … 4. Context factors … 5. Economic impact … 6. Tool support" | roadmap_action | confirmed_text | 树 C 6 streams | 否 | candidate finding，不可作 final finding |
| EV-rqtr-009 | paper.pdf | §3 Fig. 2 + Table 1 | Page 4–5 概念关系图与 Table 1 origin 列 | RQT 11 concepts 与 origin 引用 | concept_model | needs_visual_check | 树 A 11 concepts + R1–R10 关系边 | 是 | 仅本文 RQT；不可套用至 SLR/SMS |
| EV-rqtr-010 | paper_content.txt | §4.5 Threats | Page 9–10 internal / construct / external validity 段落 | "non-empirical work could contribute theoretical evidence"、"convenience sampling"、"limited to empirical contributions" | validity_boundary | confirmed_text | 整个森林的外推限制 | 否 | 不可在本文样本外推普适规律 |
| EV-rqtr-011 | metadata.json + paper_content.txt | §4.1 + replication package footnote | Page 7 + footnote 1 | Zenodo DOI 10.5281/zenodo.8167598 | replication_asset | not_verified | `B.impact.generality` / `B.impact.frame_of_reference` / Entity-fact / Activity-fact / context sub-categories 完整取值空间 | 是（Zenodo 访问） | 未核验前 A2a 不得宣称 codes 集合饱和 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C10 | 本文样本编码维度树（树 B）由 11 个 RQT 概念关联的 categorical variables + codes 组成，并已通过 inter-rater reliability 验证；构成 Paper2 可借鉴的 codebook 设计先例 | codebook_seed | 树 B（17 叶） | EV-rqtr-005, EV-rqtr-006, EV-rqtr-007 | medium（文本级 confirmed，PDF/Zenodo 仍需核） | Paper2 §Method codebook design 设计参考；不作 final finding | 取值空间在 Zenodo 核验前不饱和 |
| C11 | 本文报告的 17 个分子/分母均在 n=57 convenience sample 内有效；跨 RE 领域、跨综述类型不可外推 | local_statistic | `B.*.presence` 与频次叶 | EV-rqtr-006, EV-rqtr-010 | medium | Paper2 中作为 "RE 领域 evidence 不足" 的脚手架引用 | 不可作 Paper2 跨论文统计 |
| C12 | RQT 11 concepts + 10 关系边（R1–R10）共同构成一个关系型理论树；本文 codebook 实际只编码节点存在与几类属性，未编码关系边的具体取值 | model_vs_codebook_gap | 树 A 与树 B 的对应 | EV-rqtr-005, EV-rqtr-009 | medium | 提示 Paper2：meta-model 关系边也需 codebook 化才能统计 | codebook 未覆盖关系层 |
| C13 | 树 C 6 streams 仅为 candidate finding；roadmap 行动尚未被本文实证 | candidate_finding | 树 C | EV-rqtr-008, EV-rqtr-010 | weak | 仅作 future work 启发 | 不可作已验证方案引用 |
| C14 | replication package（Zenodo 8167598）与 rqt-tool（GitHub Julian Frattini/rqt-tool）是 A2a 必访资产；未访问前 `B.impact.generality / frame_of_reference / entity_fact / activity_fact / context.sub_category` 取值空间为 schema_seed | a2a_blocker | 上述 5 叶 | EV-rqtr-011 | weak | A2a 入口 | 资产可能已更新或下线 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读技能 / 指南文件与采用原则

| 文件 | 是否读取 | 本审计采用要点 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 是 | claim-evidence-engineering 原则：每条统计或叶子必绑定原文证据；证据不足显式标 `not_verified` |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 是 | 五维 reviewer 视角（Originality / Soundness / Clarity / Significance / Reproducibility）用于第 7 节 C/I/M 分级 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 是 | 采用 Five-Dimension Review 与"author-facing analysis"思路，把返修建议落到具体节点 |
| `research-planning/SKILL.md` | 是 | 用 4-stage planning 框架理解本文"Theory / Evaluation / Roadmap"三段式 |
| `research-planning/references/planning-prompts.md` | 是（节选） | 借用 Paper2Code Turn 2 "Architecture Design" 视角识别树 A / B / C 的森林结构 |
| `research-planning/references/output-schemas.md` | 是（首 100 行） | 用 task_list / methodology 结构辅助判定原文 RQ 与 sample unit 关系 |
| `oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 是 | 采用 "Completion is artifact-gated" 思路：本审计完成等于一份自包含报告而非"工作中" |

未出现 `blocked` 风险；全部技能文件成功读取。

### 9.2 Reviewer 视角下本输出的 3 大风险

1. **Zenodo replication package 与 rqt-tool 仓库未核验**：树 B 中 `impact.generality`、`impact.frame_of_reference`、`entity_fact.codes`、`activity_fact.codes`、`context_factor.sub_category` 完整取值空间均依赖 Zenodo 8167598 才能饱和。主线程合并时应在 A.4 增加 `cmd-…-zenodo-fetch` 与 `cmd-…-rqt-tool-fetch` 两条人工核验。
2. **未做 PDF 视觉核对**：Fig. 4（codes 分布柱状）与 Page 8 文本数字是否一致、Fig. 2 关系箭头方向、Table 1 origin 列均只来自 `paper_content.txt` 提取结果。主线程合并时应至少打开 PDF 核对一次（A.4 已有 `cmd-…-visual-check = needs_manual_check`，但范围应扩展到 Fig. 4 数字交叉）。
3. **convenience sampling 边界**：本文 57 篇借用前作样本，作者承认是 convenience；本审计的"局部可统计 / 不入主池"判定如果被下游误读为"本文是 SLR/SMS"，会造成 Paper2 跨论文统计误入。主线程合并 SUMMARY 时应再次显式写"样本来源 = Frattini et al. 2022 quality-factor ontology 的 57 篇 convenience sample，不是新做检索"。

### 9.3 本任务状态

无 blocked、无 timeout、无文件缺失。所有要求的技能文件、论文材料均已读取并在报告中显式引用。本报告为自包含完整审计，未引用"上一条消息"或外部隐藏内容。

---

**报告完结。**
