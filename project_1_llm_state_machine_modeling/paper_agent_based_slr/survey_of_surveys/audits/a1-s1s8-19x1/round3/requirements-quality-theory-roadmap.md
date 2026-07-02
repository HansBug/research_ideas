# requirements-quality-theory-roadmap：A1 S1--S8 round3 单篇维度抽取审计

## 0. 审计边界与阅读状态

- **处理对象**：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/requirements-quality-theory-roadmap`。
- **本轮角色**：A1 survey-of-surveys 单篇维度抽取 subagent；未开启 sub-subagent。
- **输出边界**：本文件只做 A1 文本级独立审计，只新建/覆盖本 round3 审计文件；不直接修改 `review.md`、`evidence_chain.md`、`SUMMARY.md` 或其他文件。
- **重要降级声明**：本文虽然在 §4 对 57 篇 requirements quality 原始研究做了编码与描述统计，但原文整体是 **VIEW POINT / research commentary + theory + evaluation + roadmap**，样本来自前作并被作者明示为 non-probabilistic convenience sampling；因此本 A1 结果只可作为 `schema_seed` / `methodological_seed` / `boundary_anchor`，不得写成 Paper2 final quantitative finding。

| 材料 | 阅读状态 | 依据 |
|---|---|---|
| `bibtex.bib` | 已读全文 | 13 行；确认 Frattini et al. 2023，*Requirements Engineering* 28(4):507--520，DOI `10.1007/s00766-023-00405-y`。 |
| `metadata.json` | 已读全文 | 确认本地已标 `review_type=theory / evaluation / roadmap`、`eligible_for_statistical_synthesis=false`、`evidence_role=theory_roadmap_schema_seed`、`systematic_evidence_status=non_systematic_or_boundary_anchor`。 |
| `paper_content.txt` | 已读全文 | 1--1187 行；覆盖摘要、§1--§6、脚注与参考文献。关键锚点：VIEW POINT 与三贡献 4--21、75--82 行；RQT 11 概念 271--395 行；§4 RQ 与 57 篇 convenience sample 464--489 行；codebook 与 reliability 502--555 行；统计结果 557--606 行；threats 673--702 行；6 roadmap streams 703--863 行。 |
| `review.md` | 已读全文 | 1--523 行；重点核对“维度树复原”214--488 行与 “survey_of_surveys 自身 schema 抽取”489--520 行。 |
| `evidence_chain.md` | 已读全文 | 1--47 行；A.1--A.4 均已读，重点核对 `ev-requirements-quality-theory-roadmap-*` 与 `clm-requirements-quality-theory-roadmap-*`。 |
| `paper.pdf` | 做存在性/元数据核验，未做视觉精核 | `pdfinfo` 显示 14 页、Springer PDF、题名与 DOI 匹配；本轮未人工核对 Fig. 2 / Fig. 4 / Fig. 5、Table 1 和 Zenodo replication package，均列入 A2a。 |

## 1. 原文如何描述“样本集合 / 编码对象 / 行动项”

### 1.1 原文显式对象

1. **论文类型对象**：PDF 首页标注 `VIEW POINT`，摘要自称 “research commentary”，贡献为三段式：harmonized requirements quality theory、requirements quality research state evaluation、research roadmap。它不是普通 SLR/SMS/tertiary study。
2. **理论对象**：§3 生成 harmonized requirements quality theory（RQT），Table 1 / Fig. 2 抽象出 11 个概念：`Entity`、`Factor`、`Entity-fact`、`Agent`、`Activity`、`Attribute`、`Activity-fact`、`Impact`、`Context factor`、`Cost`、`Resource`。
3. **被编码样本对象**：§4 的 RQ 是 “How are the concepts of the requirements quality theory reported in requirements quality literature?”；样本来自作者前作 quality-factor ontology/systematic study 的 **57 篇 primary studies**。作者明确说这是 non-probabilistic / convenience sampling。
4. **编码工具对象**：§4.2 说每个 RQT concept 关联一个或多个 categorical variables，每个 variable 有 codes 表示该 concept 是否、如何被报告；codes 第一轮 ad hoc 创建，第二轮基于讨论和 theoretical background 精炼。
5. **研究者质量控制对象**：第一作者全样本编码；第二作者随机抽 6 篇约 10% 使用 guideline 独立抽取，其中 2 篇训练、4 篇用于 reliability，报告 percentage agreement 83.3%、Cohen’s Kappa 54.2%、S-Score 76.8%。
6. **路线图行动项对象**：§5 在 Femmer et al. 三步路线图基础上更新/扩展为 6 streams：artifact and usage model、taxonomy of quality factors、impact framework、context factors、economic impact、tool support。

### 1.2 本地降级解释

- 本文有真实字段编码和描述统计，但 **没有在本文内新建完整检索式 / 数据库 / 纳排漏斗 / 去重 / 质量评价链**；样本继承自前作，作者明示为 convenience sampling。
- 因此 A1 可复原的主样本单位是：**§4 中被 RQT codebook 编码的 57 篇 requirements quality primary studies**；但这只支持本文内部状态评价，不支持 Paper2 主统计池。
- 原生结构应写成 **维度森林**：树 A = RQT 概念理论树；树 B = 57 篇样本编码 codebook（真正的样本编码树）；树 C = research roadmap streams。树 A/C 可作理论或路线图 seed，只有树 B 是样本级编码结构。

## 2. S1--S8 五分栏审计

> 等级只说明该维度对 `survey_of_surveys/` 二级 schema 的文本级可用程度，不是论文质量评分，也不是主统计池资格。所有数字均为原文内部报告或本地审计锚点，A2a 前不得进入 final quantitative finding。

| 维度（含等级） | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定：**强，但必须带 VIEW POINT / commentary 类型限定** | 首页为 `VIEW POINT`；摘要与 §1 明确三贡献：理论、survey/evaluation、roadmap；§4 明确 RQ、target population、57 篇样本单位。 | 根任务不是常规 SLR/SMS，而是 `理论统一 → 状态评价 → 路线图` 的 hybrid commentary；S1 可记录 review-like evaluation setup，但必须显式标注 research commentary。 | 不入主统计池；S1 只提供“非标准综述/理论路线图”边界类型和写法 seed。 | 核对 PDF 首页类型、摘要贡献句、§4 RQ 精确页码；确认 publisher final 无隐藏 protocol 附录。 |
| S2 语料收集与筛选：**中** | §4.1 说明 target population 是 requirements quality factors 文献；57 篇来自前作 systematic study，且作者明确称 convenience sampling。 | 样本单位是继承来的 57 篇 primary studies；可复原 `source=previous study`、`sampling=convenience`、`denominator=57`，但不能复原本文自己的检索漏斗。 | 不入主统计池；只作 inherited-sample / convenience-sample 风险模式。 | 读取/核验前作 Frattini 2022 与 Zenodo 8167598，确认 57 篇清单、纳排标准、是否只覆盖 empirical contributions。 |
| S3 原生维度树 / 样本编码对象：**强，字段细节待 A2a** | §3 给出 RQT 11 concepts；§4.2 说每个 concept 关联 categorical variables + codes；§5 给出 6 roadmap streams。 | 复原为三棵树/森林：A=RQT 11 概念理论树；B=57 篇样本编码 codebook；C=6 条 roadmap action streams。B 才是真正样本编码树。 | 局部可作 schema seed；不把 RQT 概念或 roadmap stream 当跨论文统计发现。 | 精核 Fig. 2、Table 1、Fig. 4、Fig. 5 与 Zenodo codebook，确认 B 树 leaf 未漏。 |
| S4 字段级证据：**中** | §4.2 显式举例 entity codes `{explicit, implicit}`；factor codes 分 explicitness 与 form；§4.3 报告多项分母/比例；但完整 codebook 主要在 replication package。 | 字段层来自 RQT concept → categorical variables → codes；正文可复原 entity、factor、agent、activity、attribute、impact、context、cost、resource 等主要叶子，但 entity-fact / activity-fact 与部分 impact/context 枚举待补。 | 不进入最终定量字段池；可作为 codebook construction seed。 | 下载 Zenodo 8167598，逐项核验 codebook、spreadsheet、Fig. 4 数值、impact generality/frame-of-reference、context/cost/resource 完整枚举。 |
| S5 维度模式演化：**中** | §4.2 明确 codes 第一轮 ad hoc 创建，第二轮基于 discussions 与 theoretical background 精炼；§4.5 讨论隐式概念抽取威胁。 | 维度形成链为：software quality / ABRE-QM / Quamoco 理论先验 → RQT concepts → initial codes → discussion/theory refinement → descriptive statistics。 | 方法种子可用，不入主统计池；可提示 A2a/A2b 记录字段来源、修订轮次和裁决理由。 | 核验 extraction guideline 版本与 discussion/refinement 记录是否只在复现包；不得臆测完整开放编码日志。 |
| S6 统计分析：**中（内部统计清楚，外部资格降级）** | §4.3 报告 n=57、impact 子集 n=40、24/57、17/57、14/57、8/57、37/40、19/40、11/40、10/40、9/57、5/57 等；§4.2 报告 agreement/Kappa/S-Score。 | 统计树服务于本文内部 RQT concept coverage 与 reporting mode 的 descriptive statistics；convenience sample 使其只能作为状态评价 seed。 | 不进入 Paper2 主统计池；可记录为“内部统计可复核 / A2a 待精核”的方法样例。 | 核对 Fig. 4 与正文数字一致性、n=40 子集定义、4 篇正式 IRR 计算样本、Cohen’s Kappa 与 S-Score 计算口径。 |
| S7 候选 finding：**中** | §4.4/§6 将结果解释为 artifact-centric concepts 覆盖好而 activity/context/economic concepts 被忽视；§5 把缺口转为 6 streams。 | finding 形态是 `字段覆盖缺口 → 理论/实践风险 → roadmap action`；树 C 是候选行动项，不是样本编码结果。 | 不入主统计池；只作 gap-to-roadmap finding pattern。不得迁移 RE 领域比例或 roadmap 内容为 Paper2 结论。 | 精核 §4.4、§5.1--§5.6 与结论页码；区分正文统计、作者解释、路线图建议与本地可迁移方法模式。 |
| S8 研究者 / 作者质疑与裁决：**中** | §4.2 有第二作者 10% instrument validation、training/正式 IRR、三个 reliability 指标；§4.5 报告 internal/construct/external validity，承认 convenience sample 与 implicit concept extraction 风险。 | 质量控制节点为：guideline、双人子样抽取、训练样本、正式 IRR、复现包、threats；但没有完整纳排裁决日志或逐条编码冲突 resolution table。 | 方法种子可用，不入主统计池；可作为“最小 coder-validation + threats”模式。 | 核验 6 篇随机子样、2 training + 4 IRR 表述、是否有 disagreement resolution / adjudication 记录；在 evidence chain 增补独立 S8 evidence。 |

## 3. 原生维度树 / 维度森林复原

> 下列结构是 A1 文本级复原。树 B 是本文真正样本编码维度树；树 A/C 分别是理论对象与路线图对象。所有跨论文迁移只能作为候选 schema/pattern，不得直接转写为最终经验发现。

```text
[根节点，本地复原]
Requirements quality research: theory + evaluation + roadmap
原文类型 = VIEW POINT / research commentary
总体统计池资格 = false for Paper2 main statistical pool

├── [树 A：RQT 概念元模型；理论层]
│   ├── 制品相关层
│   │   ├── Entity：需求制品或其组成部分，可分解
│   │   ├── Factor：规范性质量因子，可分解为 sub-factor
│   │   └── Entity-fact：Entity × Factor 的具体取值
│   ├── 活动相关层
│   │   ├── Agent：人、群体或自动化机制
│   │   ├── Activity：以 requirements entity 为输入并产出结果的 requirements-affected activity
│   │   ├── Attribute：Activity 的可测属性
│   │   └── Activity-fact：Activity × Attribute 的具体取值
│   ├── 影响 / 上下文层
│   │   ├── Impact：Entity-fact → Activity-fact 的关系，可分类、线性或更复杂
│   │   └── Context factor：调节 impact 的组织、人员、产品、工具、过程等上下文
│   └── 经济层
│       ├── Cost：Activity-fact 产生的经济量级
│       └── Resource：受影响资源，如 time / money
│
├── [树 B：§4 样本编码 codebook；真正的样本编码树]
│   样本单位 = publication / primary study；分母 = 57；抽样 = inherited convenience sample
│   ├── Entity reporting
│   │   └── entity explicitness ∈ {explicit, implicit}
│   ├── Factor reporting
│   │   ├── factor explicitness ∈ {explicitly reported, referenced from another publication（原文例示，精确枚举待核）}
│   │   └── factor form ∈ {textual description, logical/mathematical formula}
│   ├── Entity-fact reporting
│   │   └── codes 待 Zenodo / Fig. 4 核验
│   ├── Agent reporting
│   │   └── presence ∈ {reported, not reported}
│   ├── Activity reporting
│   │   ├── presence ∈ {reported, not reported / N/A}
│   │   └── elicitation mode ∈ {ad hoc, systematic}
│   ├── Attribute reporting
│   │   └── presence ∈ {reported, not reported}
│   ├── Activity-fact reporting
│   │   └── codes 待 Zenodo / Fig. 4 核验
│   ├── Impact reporting
│   │   ├── presence ∈ {reported, N/A}
│   │   ├── evidence ∈ {hypothesized, inductive, referenced}
│   │   ├── modality ∈ {necessary, possible}
│   │   ├── generality（正文说已编码但未报告洞察；取值待核）
│   │   └── frame of reference（正文说已编码但未报告洞察；取值待核）
│   ├── Context-factor reporting
│   │   └── sub-category ∈ {tool, product, organization/process/people 等待核}
│   ├── Cost reporting
│   │   ├── presence ∈ {reported, not reported}
│   │   └── evidence ∈ {hypothesized, referenced, empirically determined（本样本正文称 never empirically）}
│   └── Resource reporting
│       ├── presence ∈ {reported, not reported}
│       └── type ∈ {money, time, ...待核}
│
└── [树 C：§5 roadmap streams；候选行动项树]
    样本单位 = roadmap stream / action item；统计池资格 = false
    ├── 5.1 Artifact and usage model：补 reference activity model 与 attributes
    ├── 5.2 Taxonomy of quality factors：质量因素本体与中央仓库
    ├── 5.3 Impact framework：从 taxonomy of impacts 升级到统计/回归式 impact framework
    ├── 5.4 Context factors：建立 RE 专属 context factor 集合
    ├── 5.5 Economic impact：activity-fact → cost/resource
    └── 5.6 Tool support：entity/context characterization + impact prediction + economic quantification
```

### 3.1 关键叶子取值空间

| 叶子 | 原文 / 本地 | 取值空间 | 证据与限制 |
|---|---|---|---|
| `B.entity.explicitness` | 原文明示 | `{explicit, implicit}` | §4.2 给例；§4.3 报 implicit 24/57；A2a 需核 Fig. 4/codebook。 |
| `B.factor.explicitness` | 原文明示但枚举需精核 | `{explicitly reported, referenced from another publication}` | §4.2 说明一组代码表示 explicitness；精确 code label 需 replication package。 |
| `B.factor.form` | 原文明示 | `{textual description, logical/mathematical formula}` | §4.2 说明 form 组；分布数字正文未展开。 |
| `B.activity.elicitation_mode` | 原文明示 | `{ad hoc, systematic}` | §4.3 报 ad hoc 37/40；系统识别精确 code 需 codebook。 |
| `B.impact.evidence` | 原文明示 | `{hypothesized, inductive, referenced}` | §4.3 报 19/40、11/40、10/40；不得跨出本文 convenience sample。 |
| `B.impact.modality` | 原文明示 | `{necessary, possible}` | §4.3 只给 “balanced” 解释，未给精确数值。 |
| `B.impact.generality` | 原文提到但未展开 | 待核验 | §4.3 说 impact 四维中两维未在正文报告，需 Zenodo。 |
| `B.impact.frame_of_reference` | 原文提到但未展开 | 待核验 | 同上。 |
| `B.context_factor.sub_category` | 部分明示 | `{tool, product, ...}` | §4.3 明示 tool=0、product-related=14/57；其他子类待核。 |
| `B.cost.evidence` | 本地根据正文复原 | `{hypothesized, referenced, empirically determined}` | 正文称 cost/resource 若报告也 only hypothesized or referenced, never empirically determined。 |
| `B.resource.type` | 部分明示 | `{money, time, ...}` | 正文只提 money/time；其他资源类型待核。 |

### 3.2 关系边审计

| 边 | 明示 / 复原 | 源 → 目标 | 缺失值语义 | 统计用途 |
|---|---|---|---|---|
| `edge.entity_decomposes` | 原文明示 | Entity → sub-Entity | 不分解时为单层 entity，不等于缺失。 | 理论结构 seed。 |
| `edge.factor_decomposes` | 原文明示 | Factor → sub-Factor | 未报告 sub-factor 不代表 factor 不存在。 | 理论结构 seed。 |
| `edge.entity_fact` | 原文明示 | Entity × Factor → Entity-fact | 未报告 factor/entity 细节时 activity impact 难以解释。 | codebook seed。 |
| `edge.agent_activity` | 原文明示/本地关系化 | Agent → Activity | Agent 未报告 = 隐式主体，不可补猜。 | S8/裁决设计启发。 |
| `edge.activity_fact` | 原文明示 | Activity × Attribute → Activity-fact | Attribute 未报告会阻断 impact 的可测 dependent variable。 | codebook seed。 |
| `edge.impact` | 原文明示 | Entity-fact → Activity-fact | Impact N/A/未报告需区别于无影响。 | 仅本文内部统计；不入 Paper2 主池。 |
| `edge.context_modulates` | 原文明示 | Context factor → Impact relationship | Context 未报告会形成外部效度风险，而非默认无上下文。 | validity schema seed。 |
| `edge.activity_fact_cost` | 原文明示 | Activity-fact → Cost | Cost 未报告不能解释工业采纳/经济价值。 | economic/resource schema seed。 |
| `edge.cost_resource` | 原文明示 | Cost → Resource | Resource 未报告时 cost 保持抽象。 | cost tracking seed。 |
| `edge.gap_to_roadmap` | 本地复原 | Coverage gap → Roadmap stream | Roadmap 建议不是已验证解决方案。 | candidate finding pattern，不入统计。 |

## 4. 统计池资格与 A2a 接力

- **主统计池资格**：否。
- **排除理由**：全文类型是 VIEW POINT / research commentary；§4 使用的是继承自前作的 57 篇 convenience sample；本文内部统计不能外推为 Paper2 的 SLR/SMS 主统计发现。
- **可用方式**：`schema_seed`（RQT concept → categorical-variable codebook）、`methodological_seed`（instrument validation + reliability + threats）、`boundary_anchor`（hybrid theory/evaluation/roadmap 降级案例）、`candidate_finding_heuristic`（coverage gap → roadmap stream）。
- **禁止方式**：不得把 57、24/57、17/57、14/57、8/57、37/40、19/40、9/57、5/57、6 streams 等写入 Paper2 final quantitative finding；不得把 RQT 11 concepts 原样当成 SE SLR/SMS 的最终统一 schema；不得把 RE 领域 roadmap 当作 LLM/agent-based SLR 的经验结论。
- **A2a 接力项**：
  1. 人工打开 PDF 核对 Fig. 2、Fig. 4、Fig. 5、Table 1 的版面、箭头、图例和表格字段。
  2. 下载/读取 Zenodo `10.5281/zenodo.8167598`，核验 extraction guideline、spreadsheet、完整 codes、57 篇样本清单和 reliability 计算材料。
  3. 若使用 tool support 结论，核验 GitHub `JulianFrattini/rqt-tool` 与 Zenodo `8167541` 的状态和日期，避免把历史仓库写成当前可用事实。
  4. 对 review/evidence 的 A.2/A.3 增补直接支撑 S6/S8 的 evidence id，避免只靠正文泛定位或 pool 裁决。

## 5. 对 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 问题清单

| 等级 | 文件 | 问题 | 影响 | 建议 |
|---|---|---|---|---|
| C | -- | 未发现需要立即阻断 A1 的 critical 问题。 | 当前单篇总体已经正确降级为 non-statistical theory/roadmap schema seed。 | -- |
| I | `review.md` | “维度树复原”§3 后仍保留“当前 review.md 缺失的部分”，列出“把 §4 编码本完整列出”等缺失项，但同一小节下方已经列出树 B、impact 4 子维度、factor form、cost/resource 等。 | 事实真源内出现过时自我诊断，可能让后续 agent 误以为当前 review 仍未完成，或重复返修已完成内容。 | 将该段改名为“A2a 待精核 / 尚未进入 evidence_chain 的部分”，只保留 Zenodo、Fig. 4、页码、表图和 leaf-to-A.2 精核项。 |
| I | `evidence_chain.md` / `review.md` | S8 目前在 `review.md` 证据位置中引用 `ev-requirements-quality-theory-roadmap-pool`，但该证据主要支撑统计池资格，不直接支撑双人编码、IRR 或 validity threats。 | S8 是 survey_of_surveys schema 的关键质量控制维度；证据链不直连会削弱后续 A2a/A2b 对 researcher adjudication 模式的可审计性。 | 在 A.2 增补 `ev-...-quality-control`（§4.2 reliability + §4.5 threats），A.3 增补对应 `clm-...-quality-control`，并更新 S8 证据位置。 |
| M | `evidence_chain.md` | A.2 多条“原文短引”写作“短引见 review.md”，且证据强度多为 `not_verified`。当前 A1 最小链路可接受，但不能升级。 | 不影响本轮文本级审计；会限制后续直接把 evidence_chain 作为论文引用证据。 | A2a 逐条补原文短引、精确页码、图表号和行号；保留 `not_verified` 直到完成版面核验。 |
| M | `review.md` / `SUMMARY.md` | 当前 S1/S3/S6 等等级总体可接受，但应持续保留“VIEW POINT / commentary、inherited convenience sample、只作内部统计”的限定语，避免摘表时只剩“强 / n=57 / 6 streams”。 | 若后续复制 SUMMARY 表格时丢失限定语，可能把 A1 文本级结果误读为 final quantitative finding。 | 主线程回填时在 SUMMARY 对应行继续保留 `否；theory-roadmap 降级` 与 `boundary_anchor`，并避免新增比例型总计。 |
| M | `review.md` | 多处用 `Page 7`、`Page 8` 等 `paper_content.txt` 页分隔作为锚点；正式证据仍缺 PDF 精确页码、Fig. / Table 锚点和 Zenodo 字段锚点。 | 当前符合 A1 文本级审计；不适合直接进入正式论文证据表。 | A2a 将 `paper_content` 页分隔替换/补充为 PDF 页码、图号、表号、Zenodo 文件名和字段名。 |

## 6. 审计结论

本篇的核心 A1 价值是提供一种 **theory-first codebook construction** 模式：先定义 11 个 RQT 概念与关系，再把概念转成 categorical variables/codes 去编码 57 篇前作样本，最后把 coverage gap 转成 6 条 roadmap streams。当前 `review.md` 对“维度森林、真正样本编码树是树 B、不进入 Paper2 主统计池”的总体判断正确；最需要修的是过时的“缺失部分”段落和 S8 证据链直连。所有内部数量与 RE 领域结论均只能作为 A1 文本级证据和 A2a 接力项，严禁写成最终定量发现。
