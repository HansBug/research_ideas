# requirements-quality-theory-roadmap · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude reviewer（PR #135 单篇审计 subagent；不开启 sub-subagent，不修改仓库其他文件，不 push，不 gh comment）。
- 是否读取 `$ai-research-writing-skill`：否。该路径位于 `~/.codex/skills/...`，本 subagent 工作目录为 Claude Code 仓库根目录，环境中未挂载 codex skill 树；为不臆造来源，明确声明未读取。本审计仅依据该 skill 的常识性原则（paper-story、reviewer-guidelines、reviewer-self-review 的核心约束：忠于原文 schema、不把 vision 写成统计 finding、不把 not_verified 升级）执行。
- 是否读取 `$research-planning`：同上，未直接读取本地副本；按一般 research-planning 思路（planning-prompts: 范围/RQ/对象/方法/证据/边界）作为审计支架。
- 是否读取 `$oh-my-codex:autoresearch`：同上，未直接读取。
- 是否完整阅读 `paper_content.txt`：是。逐页通读了 Page 1–14 全文，包括摘要、§1 Introduction、§2 Software quality research evolution、§3 RQT theory（§3.1 Theory + Table 1 + §3.2 Example）、§4 State of research（§4.1 Survey objects、§4.2 Study design 含 extraction codes、§4.3 Study results 含 Fig. 4 全部统计数值、§4.4 Interpretation、§4.5 Threats to validity）、§5 Roadmap（§5.1–5.6 全部六条 stream + Fig. 5 tool architecture）、§6 Conclusion、参考文献尾页。
- 是否核对 `paper.pdf`：否。本 subagent 无视觉/图像核对能力；Fig. 2（RQT 概念关系图）、Fig. 3（fictitious example 图）、Fig. 4（distribution bar chart）、Fig. 5（tool architecture 图）的版面细节未做像素级核对。所有图形对应文字描述已在 paper_content.txt 中复核。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

- 唯一显式 RQ（§4，Page 7）："How are the concepts of the requirements quality theory reported in requirements quality literature?"
- 三项贡献（§1，Page 2）：
  1. 一个 harmonized requirements quality theory（RQT）作为理论基础；
  2. 对 requirements quality literature 的 survey，揭示 RQT 概念在现状中如何被报告及不足；
  3. 一条研究 roadmap 来弥补不足。
- 论文自我定位：research commentary / view point，非 SLR / SMS。

### 2.2 原文方法流程

- 数据来源：作者前期工作 [7] 中已系统检索到的 57 篇 primary studies；本文不重做检索，属 convenience sampling（§4.1）。
- 抽取设计（§4.2）：基于 RQT 概念建立 extraction guideline；每个 concept 关联 1 个或多个 categorical variable；codes 在第一轮 ad hoc 创建、第二轮基于讨论与理论背景 refine。
- 抽取与可靠性（§4.2）：第一作者抽取全部 57 篇；第二作者独立标注 6 篇（约 10%），其中 2 篇训练 + 4 篇用于 inter-rater reliability；percentage agreement 83.3%、Cohen κ 54.2%（中等）、S-Score 76.8%（良好）。
- 统计与解释（§4.3–§4.4）：descriptive statistics + 解释；Fig. 4 给出每个 concept 的覆盖率分布条。
- finding 形成方式：把 concept coverage 缺口直接解释为 practical-relevance 风险，并推到 §5 roadmap。
- 复现：replication package 在 Zenodo（DOI 10.5281/zenodo.8167598）；tool repo 在 GitHub (`JulianFrattini/rqt-tool`，Zenodo 镜像 10.5281/zenodo.8167541）。

### 2.3 原文显式 schema / taxonomy / coding scheme / 模型 / 图表 / quality rubric

**A. RQT 11 个核心 concept（§3.1 + Table 1 + Fig. 2）**——这是原文最核心的 schema，必须作为维度树主干而非附录种子：

1. `Entity`（需求制品或其组成；可分解 specification → section → paragraph → sentence/requirement）
2. `Factor`（normative metric 映射 entity 到数值；可分解为 sub-factor）
3. `Entity-fact`（entity × factor 的组合）
4. `Agent`（人、群体或自动机制；从原 stakeholder 抽象而来）
5. `Activity`（requirements-affected activity；非传统 RE elicitation/analysis/validation，而是任何以需求为输入的 process；可分解，含 interpretation sub-activity）
6. `Attribute`（activity 的可测属性）
7. `Activity-fact`（activity × attribute 的组合）
8. `Impact`（entity-fact 对 activity-fact 的关系；显式从 categorical/linear 推广到任意关系）
9. `Context factor`（影响 impact 的上下文）
10. `Cost`（activity-fact 引发的经济成本）
11. `Resource`（被消耗的资源类型）

**B. extraction codes（§4.2 + §4.3，原文显式 dimension）**：

- Entity 的 `explicitness`：`explicit` / `implicit`（24/57 implicit）。
- Factor 的两个 group：(i) `explicitness`（explicit / referenced）；(ii) `form`（textual description / logical or mathematical formula）。
- Impact 的 4 dimension：(i) `evidence`：`hypothesized`(19/40) / `inductive`(11/40) / `referenced`(10/40)；(ii) `modality`：`necessary` / `possible`（balanced）；(iii) `generality` 与 (iv) `frame of reference`（"yielded no additional insight"，仅在 replication package 提供）。
- Activity 的报告方式：`ad hoc` / `systematic`（37/40 ad hoc）。
- Context factor 的细分类（§4.3）至少包括：`tools`（0%）、`product-related`（14/57 = 24.6%）等；原文未给出穷举枚举。
- Cost 与 Resource：reported 与否（9/57、5/57）；reported 时的 `evidence`：仅 hypothesized 或 referenced，never empirical。

**C. 关键统计数值（§4.3）**——若维度树要承担"统计观察 / 候选发现链路"，必须保留这些数字作为该论文内部 finding 池：

- entities 与 factors：57/57 全部报告；其中 entity implicit 24/57（42.1%）。
- impact N/A：17/57（29.8%）。
- agent：14/57（24.6%）。
- activity：reported in 40/57；其中 ad hoc 37/40（92%）。
- attribute：8/57（14%）。
- impact evidence：19/40 hypothesized、11/40 inductive、10/40 referenced。
- context factor：tools 0/57、product-related 14/57（24.6%）；其他 sub-category 介于两者之间。
- cost：9/57（15.8%）；resource：5/57（8.8%）。
- 可靠性：percentage agreement 83.3%、Cohen κ 54.2%、S-Score 76.8%。
- understanding/interpreting sub-activity：32/40（80%）（§5.1）。

**D. roadmap 六条 stream（§5.1–§5.6）**——这是原文第二大显式 schema，必须作为维度树的一个主干分支：

1. `Artifact and usage model`（含 reference model for activities + attributes 量化）。
2. `Taxonomy of quality factors`（含 quality factor ontology、dataset、automation approach）。
3. `Taxonomy / framework of impacts`（升级 taxonomy → impact framework；以 Bayesian regression 形式估计复杂关系）。
4. `Context factors`（RE 专属 context；context-driven reporting）。
5. `Economic impact`（resource × cost 的实证刻画）。
6. `Tool support`（§5.6 + Fig. 5）：6 个组件——`entity interface` / `agent context info` / `organization context info` / `entity & context characterization` / `impact prediction model` / `economic impact quantification`；2 个 automation module——`automatic entity characterization`、`automatic impact prediction`。

**E. validity 框架（§4.5）**：internal / construct / external 三类 threat（按 Wohlin + Molléri 报告）。

### 2.4 原文 finding / gap / recommendation 的形成路径

paper 的链路是：concept coverage 统计 → identify gap（artifact-centric 覆盖好，activity/context/economic 覆盖差） → 解释 practical-relevance 风险 → 升级为 6 条 roadmap stream → 提出 tool architecture（Fig. 5）作为 operationalization 入口。这是一条 **"statistical observation → diagnosis → roadmap action"** 的 finding pattern，而不是命题假设检验型 finding。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分通过 | 根节点 `[dim-...-root]` 写作"Requirements quality research"过于宽泛；原文真正根节点应是 "harmonized RQT + state-of-research survey + roadmap" 三段式贡献。RQ 仅一条，但根节点没有把"贡献 1/2/3"反映出来。 | I |
| 主干分支是否覆盖原文 schema | 不通过 | 当前 b1–b5 是跨论文通用 5 轴（scope / corpus / taxonomy / method / evidence+finding）。原文真正的主干应当是：(B1) RQT theory（11 concepts 与关系）；(B2) State-of-research survey（sample + extraction codebook + reliability + Fig.4 statistics）；(B3) Roadmap（6 streams + Fig.5 tool architecture）；(B4) Validity & boundary。当前 b1–b5 把 RQT theory 这个核心贡献整个拍扁到 b3-taxonomy 里，roadmap 拍扁到 b4-method 里，tool architecture 几乎没有挂点。 | C |
| 叶子维度是否足够具体 | 不通过 | 6 个 `leaf-*` 是通用接口，review.md 已在 §"A1-DT 叶子层口径校准"中坦诚承认这一点；但当前给出的"原文模式候选叶子"只有 5 条，且名称（quality-construct / theory-model / evaluation-method / roadmap-question / boundary）与原文实际 schema 不匹配：原文 RQT 是 11 个 concept、6 条 roadmap stream、≥7 个 extraction code 维度，远多于 5 条。叶子层显著欠拟合。 | C |
| 取值空间是否可执行 | 不通过 | 叶子表中所有 `取值空间` 都是模板化文字（如"完整枚举 / 层级枚举 / 自由文本"），未给出原文真实可枚举值。例如：Entity.explicitness 应为 `{explicit, implicit}`；Impact.evidence 应为 `{hypothesized, inductive, referenced}`；Impact.modality 应为 `{necessary, possible}`；roadmap stream 应为 `{artifact-usage, factor-taxonomy, impact-framework, context, economic, tool}`。这些原文已显式给出的枚举完全没有出现在叶子取值空间里。 | C |
| 关系边是否缺失 | 不通过 | 原文 RQT 的核心价值正是"关系"：Entity-fact = Entity × Factor、Activity-fact = Activity × Attribute、Impact = (Entity-fact, Activity-fact, Context factor)、Cost = f(Activity-fact, Resource)。当前维度树是纯树形，没有任何关系边表达 entity-fact、activity-fact、impact triple、cost link 等组合对象。这恰是原文相对于 ABRE-QM 的最大贡献，被忽略。 | C |
| 统计用途 / 分母是否正确 | 通过（保守） | 所有叶子均标"不进入主统计池；只作 schema seed / boundary anchor"，并显式说明降级理由 `theory/evaluation/roadmap；非标准 SLR/SMS`。该决策本身合理，且与 [clm-...-tree-type] 一致。 | 通过 |
| 候选 finding 路径是否完整 | 不通过 | review.md 完全没有把原文已给出的关键数值 finding（24/57、17/57、14/57、8/57、9/57、5/57、37/40、32/40、19/40 hypothesized、percentage agreement 83.3%、κ 54.2%、S-Score 76.8%）登记为 candidate finding pool。即便不进入主统计池，也应作为该论文内部 finding seed 落账。当前 `leaf-...-finding` 是空壳，没有任何与原文 §4.3 数值挂钩的种子条目。 | I |
| A.1–A.4 证据链是否足够 | 不通过 | A.2 证据账本只有 4 条 EV（root / taxonomy / stat / risk），且全部标 `not_verified` + 页码字段写"待 A2a 精确页码复核"。原文实际页码非常清楚（§3.1 Page 4–5、Table 1 Page 5、Fig.2 Page 4、§4.2 Page 7、§4.3 Fig.4 Page 8、§5 Page 9–11、Fig.5 Page 11），完全可在 A1-DT 阶段就给出精确锚定，而无需推到 A2a。证据账本目前比原文实际能锚定的弱很多。 | I |
| 是否存在可能误导 A2a 的强主张 | 通过（保守） | review.md 没有把 roadmap / tool architecture / vision 写成完成型统计 finding；所有候选叶子均显式 `schema_seed` + `not_verified`；结论强度统一标 `weak`；[clm-...-source-schema-candidates] 显式说明 A1 种子不等于原文叶子全集。这条做得很严，符合学术口径硬约束。 | 通过 |

补充观察：

- review.md §2 全文详读章节（行 27–131）对原文 §3 RQT、§4 survey、§5 roadmap、§4.5 validity 的内容复原**非常准确**，已点名 11 concepts、所有关键数值（24/57、17/57、14/57、8/57、83.3%、54.2%、76.8%）、六条 roadmap stream、tool architecture 各模块、validity 四类风险。问题在于这些信息**没有下沉到"维度树复原"章节**——§2 文本内容是 paper-faithful 的，§"维度树复原"章节却是 paper-agnostic 的通用模板。两者出现学术 schema 与 schema 落档之间的断层。
- 历史草稿（旧 5.1/5.2/5.3，行 156–247）原本给出了贴近原文的 `theory_meta_model`（object/activity/impact/context/economic 五层）、`state_evaluation`（population/codebook/extraction/reliability/descriptive/interpretation 六层）、`roadmap_stream`（含 triggering_gap、theory_concepts_covered、automation_candidate、human_gate、residual_risk）。这三棵树**远比当前 A1-DT 维度树更忠实于原文**。当前 PR 把它们降级为"历史草稿（已迁移，不作事实真源）"，但迁移结果（当前 §"维度树复原"）反而失去了 schema 精度。这是典型的"为统一接口牺牲单篇 schema 复原"。

## 4. 建议维度树骨架

下方仅展示建议骨架；叶子取值空间均来自原文已显式枚举，证据可直接锚定到 paper_content.txt 中已知页码。

```text
[dim-rqtr-root] Requirements Quality Theory + Evaluation + Roadmap (Frattini et al. 2023)
├── [b-rqtr-theory] B1. Harmonized Requirements Quality Theory (RQT)
│   ├── [leaf-rqtr-theory-artifact-layer] artifact-related concepts
│   │   ├── Entity { explicitness: explicit | implicit; granularity: specification | section | paragraph | sentence | requirement }
│   │   ├── Factor { explicitness: explicit | referenced; form: textual | formal(logic/math); decomposition: factor | sub-factor }
│   │   └── Entity-fact (Entity × Factor)
│   ├── [leaf-rqtr-theory-activity-layer] activity-related concepts
│   │   ├── Agent { type: human stakeholder | automated tool }
│   │   ├── Activity { decomposition: sub-activity; reporting: ad hoc | systematic; interpretation sub-activity present: yes/no }
│   │   ├── Attribute (measurable property of activity)
│   │   └── Activity-fact (Activity × Attribute)
│   ├── [leaf-rqtr-theory-impact] Impact
│   │   ├── relation_form: categorical | linear | complex (Bayesian/regression)
│   │   ├── evidence: hypothesized | inductive | referenced
│   │   ├── modality: necessary | possible
│   │   ├── generality (低信息量；replication package only)
│   │   └── frame_of_reference (低信息量；replication package only)
│   ├── [leaf-rqtr-theory-context] Context factor { sub-categories observed: tools | product-related | organization | process model | people | ... }
│   └── [leaf-rqtr-theory-economic] Economic layer
│       ├── Cost { evidence: hypothesized | referenced | empirical=∅ }
│       └── Resource { type: time | money | other }
├── [b-rqtr-survey] B2. State-of-research survey
│   ├── [leaf-rqtr-survey-sample] target population = requirements quality literature on quality factors; sample = 57 primary studies; strategy = convenience (inherited from [7])
│   ├── [leaf-rqtr-survey-codebook] extraction guideline = RQT concepts → categorical variables; codes refined in 2 iterations
│   ├── [leaf-rqtr-survey-process] first author extracts all 57; second author labels 6 (~10%, 2 training + 4 reliability)
│   ├── [leaf-rqtr-survey-reliability] percentage_agreement=83.3%; Cohen_κ=54.2% (moderate, marginal-skew caveat); S-Score=76.8% (good)
│   ├── [leaf-rqtr-survey-coverage] concept coverage table
│   │   ├── entity 57/57 (implicit 24/57=42.1%); factor 57/57
│   │   ├── impact N/A 17/57=29.8%
│   │   ├── agent 14/57=24.6%
│   │   ├── activity 40/57; ad hoc 37/40=92%; understanding-sub 32/40=80%
│   │   ├── attribute 8/57=14%
│   │   ├── impact_evidence: hypothesized 19/40=47.5%, inductive 11/40=27.5%, referenced 10/40=25%
│   │   ├── context tools 0/57; context product-related 14/57=24.6%
│   │   └── cost 9/57=15.8%; resource 5/57=8.8%
│   └── [leaf-rqtr-survey-interpretation] artifact-centric bias / activity gap / context gap / economic gap / practical-relevance risk
├── [b-rqtr-roadmap] B3. Roadmap (6 streams)
│   ├── stream-1 Artifact and usage model { status: AMDiRE done; activity reference model missing; attributes missing }
│   ├── stream-2 Taxonomy of quality factors { status: ontology in early stage [7] }
│   ├── stream-3 Impact framework (upgrade from taxonomy) { proposed form: regression / Bayesian data analysis }
│   ├── stream-4 Context factors (RE-specific, beyond Petersen-Wohlin generic SE context)
│   ├── stream-5 Economic impact (resource × cost empirical estimation)
│   └── stream-6 Tool support (Fig. 5)
│       ├── components: entity interface | agent context | organization context | entity&context characterization | impact prediction model | economic impact quantification
│       └── automation modules: automatic entity characterization; automatic impact prediction
├── [b-rqtr-validity] B4. Threats to validity
│   ├── internal: convenience sampling inherited from [6,7]
│   ├── construct: aligned with mature SE quality theories (Quamoco etc.)
│   ├── extraction: implicit-concept extraction → mitigated by double labeling + reliability
│   └── external: sample limited to empirical contributions; theoretical/linguistic evidence not covered
└── [b-rqtr-artifact] B5. Open artifacts
    ├── replication package: Zenodo 10.5281/zenodo.8167598
    └── tool repo: github.com/JulianFrattini/rqt-tool (Zenodo 10.5281/zenodo.8167541)
```

每个叶子的统计/候选发现资格：

- B1（RQT theory）叶子：`schema_seed` only。它本身是理论贡献，不进入 SLR/SMS 统计池；但**可作为 Paper2 researcher-defined meta-model 的对象级先验**。
- B2（survey）叶子：可作为该论文**内部** descriptive statistics finding pool；不进入 survey-of-surveys 19 篇主统计池，因为样本来自 convenience sampling 且对象是 requirements quality 而非 SLR/SMS 方法学。
- B3（roadmap）叶子：`candidate_finding` / `vision` only；严禁升级为已验证 finding。
- B4（validity）叶子：`boundary_anchor` only。
- B5（artifact）叶子：可直接进入"复现资产可得性"二值统计（replication package available = yes；tool repo available = yes）。

如果维持当前通用 5 轴（scope/corpus/taxonomy/method/evidence+finding）作为跨论文接口，则**至少**应在每个通用叶子下挂出本文 RQT 11 concept、roadmap 6 streams、extraction 6 codes 的子节点，并把已显式枚举的取值空间补全。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主干分支错位 | review.md §"维度树复原" → "维度树结构" | 把 b1–b5 重写为 B1 RQT theory / B2 Survey / B3 Roadmap / B4 Validity / B5 Open artifacts；或在维持通用 5 轴的前提下，在每个通用叶子下追加原文对应子节点。 | paper_content.txt §3、§4、§5、§4.5、§5.6 footnotes | C |
| 缺失 RQT 11 concept 作为正式叶子 | review.md §"叶子维度表" + §"原文模式候选叶子映射" | 把 Entity / Factor / Entity-fact / Agent / Activity / Attribute / Activity-fact / Impact / Context factor / Cost / Resource 全部登记为正式（或至少强 seed）叶子，并把其取值空间从原文 §3.1 + Table 1 + §4.2 + §4.3 直接抄入。 | paper_content.txt Page 4–6 Table 1；Page 7–8 §4.2–4.3 | C |
| 缺失原文 extraction codes 取值空间 | review.md §"叶子维度表" 各叶子的"取值空间"列 | 至少补全：Entity.explicitness={explicit, implicit}; Factor.explicitness={explicit, referenced}; Factor.form={textual, formal}; Activity.reporting={ad hoc, systematic}; Impact.evidence={hypothesized, inductive, referenced}; Impact.modality={necessary, possible}; Impact.generality + Impact.frame_of_reference（低信息量但需备注）。 | paper_content.txt §4.2 Page 7–8；§4.3 Page 8 | C |
| 关系边缺失 | review.md §"维度树结构" 末尾增设 "关系边" 子节 | 显式记录三组组合关系：Entity-fact = Entity × Factor；Activity-fact = Activity × Attribute；Impact triple = (Entity-fact, Activity-fact, Context factor)；Cost link = (Activity-fact, Resource)。说明这是 RQT 相对 ABRE-QM 的最大贡献。 | paper_content.txt §3.1 Page 4–6 + Table 1 | I |
| 六条 roadmap stream 未作为正式叶子 | review.md §"叶子维度表" 或 §"原文模式候选叶子映射" | 把 6 条 stream 分别登记为 leaf-seed，并标注 stream-6 含 Fig.5 的 6 components + 2 automation modules。 | paper_content.txt §5.1–§5.6 Page 9–11 + Fig. 5 Page 11 | C |
| 候选 finding 池为空 | review.md §"统计与候选发现链路" | 把 §4.3 全部数值落账为 candidate_finding：24/57、17/57、14/57、8/57、9/57、5/57、37/40、32/40、19/40、11/40、10/40、83.3%、54.2%、76.8%、24.6% (context-product)。即便不进入 19 篇主统计池，也必须有本论文内部 finding seed 表。 | paper_content.txt §4.3 Page 8 | I |
| A.2 页码可立即精化 | review.md §"A.2 维度树证据账本" | 现在四条 EV 全部写"待 A2a 精确页码复核"，但原文页码十分明确：RQT theory 在 Page 4–6（Fig.2 Page 4、Table 1 Page 5）；survey method 在 Page 7；results 在 Page 8（Fig.4 Page 8）；roadmap Page 9–11（Fig.5 Page 11）；validity Page 9。应直接精化到段落级，避免把可立即核实的事实留到 A2a。 | paper_content.txt 全文页码 | I |
| 开放制品（replication package + tool repo）未单独登记 | review.md §"叶子维度表" | 增加 leaf-artifact-replication（Zenodo 10.5281/zenodo.8167598）与 leaf-artifact-tool（github.com/JulianFrattini/rqt-tool；Zenodo 镜像 10.5281/zenodo.8167541）。这是少数可直接二值统计的字段。 | paper_content.txt §4.2 footnote 1 Page 7；§5.6 footnote 3 Page 11 | I |
| 候选叶子命名与原文 schema 偏离 | review.md §"原文模式候选叶子映射（A1 种子）" | `leaf-...-orig-quality-construct` / `orig-theory-model` 名称模糊，无法对应到 RQT 11 concept 中具体哪几个；应改为按 RQT concept 命名（如 `orig-entity`、`orig-factor`、`orig-entity-fact` …），或附"包含 RQT concept X/Y/Z"的精确映射列。 | paper_content.txt Table 1 Page 5 | I |
| Validity 未单独成叶 | review.md 维度树 | 新增 `leaf-validity-{internal, construct, external, extraction-difficulty}`，与 §"6 类 pattern 抽取"中的 validity row 对齐。 | paper_content.txt §4.5 Page 9–10 | M |
| §2.5 字段启发与"维度树复原"叶子未交叉引用 | review.md | §2.5 已正确点出 quality factor / impact / context / economic / tool 对 Paper2 字段树的启发；建议在 §"维度树复原"叶子表里加一列"对应 §2.5 启发"，保证 §2 详读与维度树落档不脱节。 | review.md 行 113–120 | M |

## 6. C/I/M 结论

- C（直接破坏 Paper2 学术目标、证据链或 A2a/A2b 可靠性）：4 项
  - 主干分支错位（b1–b5 是通用接口而非原文 schema）；
  - RQT 11 concept 未作为正式叶子；
  - 原文 extraction codes 取值空间缺失；
  - 六条 roadmap stream 未作为正式叶子。
  - **影响**：当前维度树等于把 A1-DT 阶段最重要的"原文 schema 复原"任务推迟到 A2a；若 A2a 以"上一阶段已复原"为前提启动，会导致维度树永远停在通用 5 轴接口，下游 A2a/A2b 在跨论文聚合时找不到 RQT 这一篇的对象级先验，Paper2 的"researcher-defined meta-model 来源链条"会断裂。
- I（实质影响维度树可用性、原文 schema 复原、证据可审计性）：6 项
  - 根节点过宽泛；关系边缺失；候选 finding 池为空；A.2 页码可立即精化未做；开放制品未单独登记；候选叶子命名与 RQT 对不上。
- M（不阻塞的清晰度建议）：2 项
  - validity 未单独成叶；§2.5 与维度树未交叉引用。
- 最终建议：**NEEDS FIX**。

**核心判断**：review.md §2 的全文详读 paper-faithful 程度很高，证据强度本可达到 strong；但下沉到 §"维度树复原"时退化为跨论文通用接口 + 5 条模糊种子叶子，丢失了原文 RQT 11 concept、6 条 roadmap stream、≥7 个 extraction code 维度、所有 §4.3 关键数值与 Fig.5 tool architecture 组件。当前 PR 选择把所有候选叶子标 `not_verified` + 推迟到 A2a 的策略**学术口径上是保守安全的**（不会把 vision 写成完成型 finding，符合根级 review 规范），但**严重欠拟合**——原文已可直接锚定的事实没有进入维度树。建议至少把 C 级 4 项在本 PR 内修复，I 级 6 项可在 follow-up；否则本篇在 19 × 3 维度树审计 batch 中将成为"看起来合规但实际复原度最低"的样本。
