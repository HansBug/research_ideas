# ml4se-tertiary-study · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。
- 是否完整阅读 `paper_content.txt`：是；按行号完整阅读 1--1774 行，覆盖摘要、引言、相关 tertiary studies、review methods、RQ、search / selection / quality / data extraction、全部 Results、Discussion and Implications、Threats to Validity、Conclusion and Recommendations、References。
- 是否核对 `paper.pdf`：是；用 `pdfinfo` 确认本地 PDF 为 37 页，并抽样视觉核对 Fig. 1（PDF p.5）、Table 2 / Data Extraction（PDF p.10）、Table 5（PDF p.15）、Table 6 / Fig. 6（PDF p.23）、Table 7（PDF p.24）、Implication 1--2（PDF p.25）、Implication 6--7 / Threats 开头（PDF p.27）。未完成所有表格、图和 supplementary / dataset 文件逐项视觉精核。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是对 Machine Learning for Software Engineering 做三级研究：系统收集、质量评价、汇总和分类 2009--2022 年 83 篇 secondary reviews，并追溯其覆盖的 6117 篇 primary studies（`paper_content.txt` 行 5--10、502--505）。引言明确该文要填补“缺少系统汇总和评价 ML4SE secondary studies 的 tertiary review”这一缺口，并提供四轴 ML classification scheme、覆盖观察、研究机会和开放代码数据（行 72--102）。

原文显式 RQ 为三项：

| RQ | 原文问题复原 | 对应原文方法 / 结果 |
|---|---|---|
| RQ1 | 哪些 SE tasks 已经被 ML techniques 处理 | §3.6 对 SWEBOK KA / subarea / SE task 的抽取与 open coding；§4.2 和 Table 5。 |
| RQ2 | 哪些 SE knowledge areas 仍可由 ML techniques 更好覆盖 | §3.6 用 RQ1 覆盖结果加人工抽取 further research / comments / obstacles；§4.3 和 §5 Implications。 |
| RQ3 | 哪些 ML techniques 已经用于 SE | §3.6 四轴 ML classification scheme；§4.4、Table 6、Fig. 6、Table 7。 |

贡献声明不是单一 taxonomy，而是“系统性三级综述 + 质量评价目录 + SWEBOK 覆盖分析 + 四轴 ML technique 分类 + research challenges/actions”。因此维度树不能只复原为“主题 / 挑战树”，也不能只保留通用六个 leaf。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法按 Kitchenham and Charters guidelines 组织为 planning、conducting、reporting 三阶段，并有 formal protocol；protocol 覆盖 search and selection、quality assessment、data extraction、synthesis、analysis。所有需要人工判断的活动采用 data extraction and data checking，第二作者抽取、第一作者检查（行 206--216；Fig. 1 已视觉核对）。

检索流程是四阶段：automated search in digital sources、manual search in digital sources、backward snowballing、forward snowballing（行 237--241）。自动检索选择 2015 年为起点，依据 Scopus 中 ML 和 SE 交叉文献在 2015 后增长；查询 IEEE Xplore、ACM Digital Library 和 Scopus；使用三组关键词：SWEBOK-derived SE keywords、ML keywords、secondary-study keywords（行 242--299；Table 1）。自动检索 1897 条，按 DOI 去重后 1566 条；manual search 加 1 条；backward snowballing 评估 3195 条参考文献并新增 16 条，其中 7 条通过质量评估；forward snowballing 从 Scopus 检索 2461 条 citing studies，新增 84 条，其中 43 条质量通过（行 296--329）。

纳排标准包括：纳入 secondary studies / taxonomies / ML-in-SE results，排除 non-secondary empirical / experimental / workshop summaries / future plans、只提 ML 不描述 technique、不可访问、非英文、informal surveys（行 330--359）。筛选过程先用 15 篇随机样本校准 IC/EC 和 Cohen's Kappa，达到 0.8 后再分工筛选剩余 1552 条，最终 140 distinct secondary studies 进入质量评估（行 361--379）。

质量评估采用 DARE-4：IC/EC、Search space、Quality assessment of primary studies、Information regarding primary studies，Y/P/N 分别计 1/0.5/0，满分 4，低于 2 排除；140 篇中 57 篇被排除，inter-rater agreement 为 82%（行 380--418；Table 2 已视觉核对）。

数据抽取字段是原文 schema 的核心，显式列为：title/source、publication year、venue、authors/institutions/countries、study type、research method、quality score、number of primary studies、SWEBOK KA/subarea/SE tasks、implications/comments、employed ML techniques（行 419--432）。随后每个 RQ 有不同编码策略：

- RQ1：按 SWEBOK KA、subarea 和 SE task 抽取；多 KA / subarea 时保留最 prominent 项；SE task 采用 open coding，代码主要来自 title / keywords / abstract / introduction，再用 qualitative content analysis 合并和泛化；每篇 secondary study 关联 1--3 个 SE tasks（行 435--453）。
- RQ2：用 RQ1 结果找覆盖不足的 SWEBOK KAs，并人工抽取 further research implications、ML4SE comments、issues / obstacles（行 454--459）。
- RQ3：使用四轴 classification scheme，轴包括 role of AI in SE、supervision、incrementality、generalizability；多类别时选最 prominent；另手工抽取 reported ML techniques（行 460--497）。

统计呈现包括 final set 的 bibliographic / quality / method 分布、Table 5 的 SWEBOK KA / subarea / secondary count / percentage / primary count、Table 6 的四轴 ML technique count / percentage、Fig. 6 的 KA × technique percentage heatmap、Table 7 的 technique-by-application-task 长枚举。finding 形成不是简单频次最大项，而是“统计观察 + coverage gap + secondary-study comments + 作者解释 → Implication / Recommendation”。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

| 原文结构 | 真实内容 | 审计判断 |
|---|---|---|
| Review method figure | Fig. 1 包含 generic search string、manual / automated search、15 random studies、IC/EC + Cohen's Kappa、DARE quality assessment、backward / forward snowballing、final selected studies。 | 是原文流程 schema，不能只压成“语料与纳排链条”。 |
| Search keyword schema | Table 1 按 SE / ML / Secondary Studies 三组关键词组织。 | 支撑 corpus_screening_protocol 和 search-string construction 字段。 |
| Inclusion / exclusion criteria | §3.3 显式列出 secondary / taxonomy / ML4SE results 纳入条件和 non-secondary / future plan / inaccessible / non-English / informal survey 排除条件。 | 是统计池资格与 exclusion-code 字段来源。 |
| Quality rubric | Table 2 DARE-4 四项质量标准、Y/P/N 分数与总分门槛。 | 当前 `review.md` 没有作为叶子维度复原，属于遗漏。 |
| Data extraction form | §3.6 显式列出 11 类抽取字段，并逐项映射到 RQ1--RQ3。 | 当前 `review.md` 只保留 5 个原文候选 leaf，严重压缩。 |
| RQ1 taxonomy / coding scheme | SWEBOK KA → subarea → SE task；SE tasks 由 open coding + qualitative content analysis 形成。 | 应作为层级 taxonomy + coding reliability / subjectivity 字段。 |
| RQ2 gap / recommendation scheme | 用 RQ1 覆盖度识别 underrepresented KAs，再抽取 further research、comments、issues、obstacles。 | 当前只写“挑战与建议”，缺 finding path。 |
| RQ3 four-axis ML classification scheme | role of AI in SE、supervision、incrementality、generalizability；另有 application task grouping。 | 当前“ML 技术类别”候选 leaf 没有还原四轴结构。 |
| Result evidence tables | Tables 3--4 overview of secondary studies，Table 5 SWEBOK coverage，Table 6 ML axes，Fig. 6 KA × ML axes，Table 7 application tasks。 | 这些表决定取值空间和统计分母。 |
| Implication / recommendation boxes | §5 给出 7 条 Implications，从 empirical validation 到 hybrid / cross-disciplinary methods。 | 应作为 candidate finding / action recommendation tree，不应写成目标领域 final finding。 |
| Threat model | §6 使用 Study Selection Validity、Data Validity、Research Validity 三类组织威胁。 | 当前 `review.md` 前半仍称 threats 待定位，已过时且不准确。 |
| Artifact / reproducibility | 引言声明 code and data openly available，并有 protocol、search queries、CSV、assessment、knowledge areas、further research、ML techniques 等 dataset file footnotes。 | 应进入 artifact / replication package 字段；当前候选树基本遗漏。 |
| Roadmap figure | 原文没有 roadmap figure。 | 任何 `roadmap branch / action point` 说法只能泛指 discussion / implications，不能写成原文图表 schema。 |

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding path 至少有四条：

1. RQ1 字段链：SWEBOK KA / subarea / SE task coding → Table 5 coverage counts → 软件质量、测试和 SE process 覆盖较多，Software Construction / SE Economics 未覆盖，human-centered KAs 较少 → Implication 3。
2. RQ2 字段链：coverage gap + secondary-study future work / obstacle comments → §4.3 KA-specific recommendations → §5 Implication 1--7 和 Conclusion recommendations。
3. RQ3 字段链：四轴 ML classification → Table 6 / Fig. 6 → classification / learning / prediction、supervised、batch/offline、model-based 占主导；online / incremental 很少 → Implication 6；hybrid / probabilistic / search-based 仍有空间 → Implication 7。
4. Quality / evidence chain：DARE-4 score、83/140 quality accepted、overview tables、data extraction/checking、threats → 控制 tertiary finding 的可信度和外推边界。

因此，维度树应保留 RQ → extraction field → classification / coding → statistical result → implication / recommendation → threat boundary 的路径。只写“统计观察与候选发现”无法支撑 Paper2 后续 A2a/A2b 的字段精核和 candidate finding ledger。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确，但过于笼统 | `review.md` 将根节点设为 Machine Learning for Software Engineering，并写明 primary / secondary study 双单位对象（行 71--73）。方向正确；但原文根目标是三级研究中的 secondary reviews，primary studies 只是被 secondary reviews 覆盖的追溯分母。根节点还应显式绑定 3 个 RQ、83 reviews、6117 primary studies、DARE quality gate 和 protocol / dataset。 | I |
| 主干分支是否覆盖原文 schema | 未覆盖，且树型主张偏窄 | 当前树只有范围、语料、主题、方法、评价/统计/候选发现五个泛分支（`review.md` 行 77--90），实际原文至少有 review method / search / IC-EC / quality / data extraction / RQ1 SWEBOK taxonomy / RQ2 gap-action / RQ3 four-axis ML scheme / artifact / validity 等主干。把主类型称为“tertiary 主题 / 挑战树”（行 63）低估了原文的 protocol + quality + classification + implication 复合结构。 | C |
| 叶子维度是否足够具体 | 不足；当前主要是通用接口 | `review.md` 明确承认六个 `leaf-*` 是跨论文通用接口而非原文全集（行 67），这避免了最危险误读；但“原文模式候选叶子映射”仅 5 个候选 leaf（行 107--113），遗漏 RQ、search counts、IC/EC、DARE-4、11 类 extraction fields、SWEBOK subarea table、open coding、四轴 ML scheme、Table 3--7、Implication 1--7、Threats、artifact / dataset fields。 | C |
| 取值空间是否可执行 | 多数不可直接执行 | 通用 leaf 的取值空间仍是“自由文本”“完整枚举 / 层级枚举 / 自由文本”“布尔、数值、链接状态”等元类型（行 96--101）。原文可执行取值空间包括 DARE-4 Y/P/N、search source stages、SWEBOK KAs / subareas、四轴 ML categories、supervision categories、incrementality categories、generalizability categories、7 类 application tasks / hybrid / miscellaneous、7 条 Implications、validity threat categories。 | I |
| 关系边是否缺失 | 明显缺失 | 当前 `review.md` 没有关系边表。原文需要 RQ1→SWEBOK taxonomy→Table 5→RQ2 gaps，RQ3→four-axis ML scheme→Table 6 / Fig. 6，quality gate→83 accepted reviews，dataset files→artifact reproducibility，statistical observations→Implications，Threats→claim boundary 等关系边。 | I |
| 统计用途 / 分母是否正确 | 降级纪律正确，但分母复原不足 | `review.md` 正确声明 A1-DT 当前仅 schema seed，不进入 SUMMARY 定量统计（行 63、119--121），这是优点；但统计分母没有细化到 1897/1566/1567/3195/2461/140/83/57/6117、Table 5 的 secondary / primary 双层分母、Table 6 的 83 reviews 分母、Table 7 的 technique grouping 分母。 | I |
| 候选 finding 路径是否完整 | 不完整 | 当前只写“挑战与建议”一类候选 leaf（行 113）和“统计观察与候选发现”（行 101、120--121）。原文有 7 条 Implications，并且每条都由 RQ2 / RQ3 统计观察、secondary-study comments 或 cross-domain comparison 支撑。缺少 finding path 会影响 Paper2 对“统计观察不是 final finding”的核心方法目标。 | C |
| A.1--A.4 证据链是否足够 | 结构存在，内容不足 | A.1--A.4 表结构齐全（行 130--171），且 A.2 证据均降级为 `not_verified`（行 144--147），没有把弱证据升级为统计结论；但 A.2 只有 4 条泛证据，原文页码、表号、行号范围几乎都是“待 A2a 精确页码复核”，无法追溯到 Table 1--7、Fig. 1--6、Implication 1--7、Threats 分类和 dataset artifact。 | I |
| 是否存在可能误导 A2a 的强主张 | 有中等风险 | 当前显式写了“六个 leaf 不是原文全集”（行 67）和“不得进入当前 SUMMARY 定量统计”（行 109--113），不是直接强主张；但快速 pattern 表仍说 validity / threat “本轮只读题摘和全文开头，threats 待定位”（行 33），与当前全文阅读状态和原文 §6 不一致；A.4 `structure-check passed`（行 170）也没有给出本次可复验命令输出。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不能视为足够。建议保留通用六 leaf 作为 `interface_layer`，但新增以下忠实于原文的 `source_schema_layer`。所有当前用途仍应是 `schema_seed`；只有 A2a 完成精确页码 / 表号 / dataset 文件核验后，才允许升级为统计合成字段。

| 根 / 主干 / 叶子 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|
| [dim-ml4se-root] ML4SE tertiary study | 83 quality-accepted secondary reviews；6117 non-unique primary studies；2009--2022 reviews；1990--2021 primary works | 是，后续主统计池候选；A1-DT 当前只作 schema_seed | `not_verified` 表示未完成页码 / 表图 / dataset 精核 | 摘要行 5--10；目标行 217--236；结果行 502--505 |
| [dim-ml4se-rq] Research objectives and questions | RQ1 SE tasks；RQ2 under-covered KAs；RQ3 ML techniques | 是，作为 RQ pattern | `not_reported` 不适用；本文有显式 RQ | §3.1 行 217--236 |
| [dim-ml4se-protocol] Review method / protocol | planning / conducting / reporting；search and selection；quality assessment；data extraction；synthesis；analysis；extractor-checker | 是，作为 method/process schema | `not_reported` / `protocol_not_available` | §3 行 206--216；Fig. 1 PDF p.5 |
| [leaf-ml4se-search-stage] Search stages | automated search、manual search、backward snowballing、forward snowballing | 是，流程频次 / 方法字段 | `not_reported` | §3.2 行 237--241；Fig. 1 |
| [leaf-ml4se-search-keywords] Search keyword schema | SE keywords、ML keywords、secondary-study keywords；SWEBOK-derived / CSUR-derived sources | 可统计为 search-string construction pattern | `text_extraction_missing` / `not_verified` | Table 1 行 264--276；PDF p.7 |
| [leaf-ml4se-search-counts] Search / selection counts | 1897 collected、1566 DOI-unique、1567 after manual、3195 backward refs、16 additional、7 accepted, 2461 forward citing studies、84 included、43 accepted、140 selected、83 accepted、57 rejected | 是；需明确每个数值所属阶段 | `not_verified` until PDF / dataset checked | §3.2--3.5 行 296--329、361--418 |
| [leaf-ml4se-ic-ec] Inclusion / exclusion criteria | secondary systematic studies；taxonomy planning characteristics；ML-in-SE results；exclude non-secondary / ML-without-technique / inaccessible / non-English / informal | 是，作为 eligibility field | `not_applicable` 不适用；本文有 IC/EC | §3.3 行 330--359 |
| [leaf-ml4se-quality-rubric] DARE-4 quality assessment | QA1 IC/EC、QA2 search space、QA3 quality assessment、QA4 primary-study information；Y=1/P=0.5/N=0；threshold >=2 | 是；可统计 quality gate / threshold | `quality_not_reported` | §3.5 行 380--418；Table 2 PDF p.10 |
| [dim-ml4se-extraction-form] Data extraction form | title/source、year、venue、authors/institutions/countries、study type、research method、QA score、primary-study count、SWEBOK KA/subarea/tasks、implications/comments、ML techniques | 是；字段表主干 | `not_reported` / `inferred` | §3.6 行 419--432 |
| [leaf-ml4se-rq1-swebok] RQ1 SWEBOK / SE task taxonomy | SWEBOK KAs、subareas、open-coded SE tasks；每 review 1--3 SE tasks | 是；secondary-study count / percentage / primary-study count | `not_classifiable` / `multiple_KA_keep_prominent` | §3.6 行 435--453；Table 5 PDF p.15 |
| [leaf-ml4se-rq2-gap-action] RQ2 under-covered areas and recommendations | uncovered KAs、under-covered KAs、further research、comments、issues、obstacles；general recommendations with n counts | 是，但 Implication 只作 candidate finding | `no_comment_reported` / `candidate_only` | §3.6 行 454--459；§4.3 行 827--849；§5 行 1095--1216 |
| [leaf-ml4se-rq3-four-axis] RQ3 four-axis ML scheme | role of AI in SE: SBSE / fuzzy-probabilistic / classification-learning-prediction；supervision: supervised / unsupervised / semi-supervised / reinforcement；incrementality: online / offline；generalizability: instance / model-based | 是；分母 83 reviews | `not_reported` / `most_prominent_category_only` | §3.6 行 460--497；Table 6 / Fig. 6 PDF p.23 |
| [leaf-ml4se-ml-application-task] ML application task grouping | classification / clustering / regression；pattern discovery；dimensionality reduction；information retrieval；stochastic search；generation；hybrid；miscellaneous | 可统计为 method taxonomy seed；Table 7 长枚举需 A2a 精核 | `not_grouped` / `not_verified` | Table 7 行 1054--1089；PDF p.24 |
| [leaf-ml4se-result-overview] Secondary-study overview | study、venue、year、publisher、QA score、primary covered years；journal/conference split；top authors/institutions; research type and method | 是，demographic / evidence presentation | `not_reported` | §4.1 行 501--528；Tables 3--4 |
| [leaf-ml4se-finding-implication] Implication / recommendation outputs | Implication 1--7；researcher recommendation；practitioner recommendation | 只作 candidate_finding / action heuristic | `candidate_only` / `needs_counterevidence` | §5 行 1095--1216；§7 行 1272--1321 |
| [leaf-ml4se-validity] Threats to validity | Study Selection Validity、Data Validity、Research Validity；DARE-4 limitation；manual-subjectivity threat | 是，validity pattern | `not_reported` | §6 行 1217--1271 |
| [leaf-ml4se-artifact] Open code / data / protocol artifacts | Zenodo DOI；review-protocol.md；search query/results files；DARE assessment; knowledge areas; further research; ML techniques CSVs | 是，artifact / reproducibility field；链接需 A2a 核验 | `link_not_verified` / `not_available` | 引言行 101--102；footnotes 行 223、306--307、392--394、439--440、483--484 |

建议新增关系边：

| 关系边 | 源节点 | 关系类型 | 目标节点 / 取值空间 | 缺失值语义 / 用途 |
|---|---|---|---|---|
| [edge-ml4se-rq1-fields] | RQ1 | answered_by | SWEBOK KA / subarea / SE task / Table 5 | 若无 SWEBOK mapping，则 RQ1 不可统计。 |
| [edge-ml4se-rq2-gap] | RQ2 | derived_from | RQ1 coverage + further research comments + issues / obstacles | gap 不是单纯低频项，必须有 authors' remarks 或 coverage evidence。 |
| [edge-ml4se-rq3-axis] | RQ3 | answered_by | four-axis ML scheme / Table 6 / Fig. 6 | 多类别时原文保留 most prominent category。 |
| [edge-ml4se-quality-gate] | DARE-4 rubric | filters | 140 selected → 83 accepted / 57 rejected | 低于 2 分排除，不能进入结果分母。 |
| [edge-ml4se-stat-implication] | Table 5 / Table 6 / Fig. 6 / §4.3 comments | supports | Implication 1--7 | 只进入 candidate_finding，不进入 Paper2 final finding。 |
| [edge-ml4se-artifact-repro] | Protocol / data files | supports | reproducibility / auditability | `link_not_verified` 时不能升级为 artifact 统计结论。 |
| [edge-ml4se-threat-boundary] | §6 Threats | limits | 所有统计观察与 implications | 外推时必须保留 search / data / research validity 限制。 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把当前“tertiary 主题 / 挑战树”改为复合树 | `review.md` 维度树一句话结论与树结构 | 树类型改为“tertiary review protocol + RQ-driven classification + gap/action recommendation 复合树”；不要只强调 challenge / action。 | 原文 §3--§5；Fig. 1、Table 2、Table 5--7。 | C |
| 扩展原文候选叶子映射 | `原文模式候选叶子映射` | 从 5 个候选 leaf 扩展到 RQ、search protocol、IC/EC、DARE-4、data extraction form、RQ1 SWEBOK taxonomy、RQ2 gap/action、RQ3 four-axis scheme、application-task grouping、validity、artifact。 | `paper_content.txt` 行 217--236、330--359、380--432、435--497、1217--1271。 | C |
| 补 DARE-4 quality rubric | 叶子维度表 / A.2 | 增加 QA1--QA4、Y/P/N score、threshold >=2、57/140 rejection、82% agreement。 | 行 380--418；Table 2 PDF p.10。 | I |
| 补 search / selection 分母链 | `语料与纳排链条` | 写清 1897、1566、1567、3195、2461、140、83、57 等数字属于哪个阶段；A2a 再核对 Fig. 1 / dataset。 | 行 296--329、361--418；Fig. 1 PDF p.5。 | I |
| 补数据抽取字段表 | `dimension pattern` / `A1-M5` / 维度树叶子 | 用 §3.6 的 11 类字段作为原文 extraction form，不要只写“SE 问题类别、ML 技术、数据来源、评价质量、挑战建议”。 | 行 419--432。 | C |
| 补 RQ1 coding scheme | 主题 / 对象分类分支 | 加 SWEBOK KA / subarea / SE task、open coding、qualitative content analysis、1--3 tasks per secondary study、multiple-KA prominent-rule。 | 行 435--453；Table 5 PDF p.15。 | I |
| 补 RQ2 finding path | 统计观察与候选发现分支 | 把 RQ2 的 under-covered KA、further research、comments、issues、obstacles 和 §5 Implications 1--7 建成候选 finding path。 | 行 454--459、827--849、1095--1216。 | C |
| 补 RQ3 四轴 ML classification scheme | 方法 / 技术 / 干预分支 | 不要写成“监督 / 非监督 / 深度学习 / 传统 ML / NLP”等泛分类；按原文四轴与 Table 6 categories 复原。 | 行 460--497、975--1019；Table 6 PDF p.23。 | I |
| 补 Table 7 application-task grouping | 方法分支或关系边 | 增加 classification/clustering/regression、pattern discovery、dimensionality reduction、information retrieval、stochastic search、generation、hybrid、miscellaneous；长枚举不必全抄，但需保留结构。 | 行 1020--1094；Table 7 PDF p.24。 | I |
| 补 artifact / replication 字段 | A1-M4 / evidence leaf / A.2 | 增加 Zenodo code/data、protocol、search query/result、DARE assessment、knowledge areas、further research、ML techniques 文件；标 `link_not_verified`。 | 行 101--102、223、306--307、392--394、439--440、483--484。 | I |
| 修正 validity / threat pattern 的过时描述 | 六类 pattern 表第 5 行 | 当前写“只读题摘和全文开头，threats 待定位”与本次全文审计和原文 §6 冲突；改为 Study Selection / Data / Research Validity 三类。 | 行 1217--1271；PDF p.27--28。 | I |
| 新增关系边表 | 维度树复原小节 | 建 RQ→field、quality gate→accepted corpus、statistics→implications、threats→claim boundary、artifact→reproducibility 的边。 | GUIDE 6.3.4；原文 §3--§6。 | I |
| 精确化 A.2 证据账本 | A.2 | 至少拆出 Fig. 1、Table 1、IC/EC、Table 2、§3.6 extraction fields、Table 5、Table 6 / Fig. 6、Table 7、Implication 1--7、§6 Threats、artifact footnotes 的独立证据行；填行号 / PDF 页码 / 表图编号 / 是否视觉核对。 | 本次已视觉核对 PDF p.5、p.10、p.15、p.23、p.24、p.25、p.27。 | I |
| 统一统计池措辞 | 快速卡片和统计链路 | 写为“后续主统计池候选；A1-DT 当前仅 schema_seed，不进入 SUMMARY 定量统计”。 | SUMMARY 三池规则；`review.md` 行 63、119--121。 | M |
| 给 A.4 passed 状态补证 | A.4 | 若保留 `passed`，补结构检查命令、脚本路径和输出摘要；否则改为 `not_rerun_in_this_audit`。 | `review.md` 行 170 当前仅自然语言。 | M |

## 6. C/I/M 结论

- C：3。当前维度树主干和原文 schema 复原明显过小，未覆盖原文 extraction form、DARE quality rubric、RQ1/RQ2/RQ3 的 coding / classification / finding path；这会直接影响 Paper2 后续 A2a/A2b 的字段精核、统计池准备和 candidate finding ledger 可靠性。
- I：10。主要是取值空间不可执行、关系边缺失、分母链不细、A.2 证据泛定位、artifact / validity / coding reliability 缺漏。它们不一定立即造成错误强主张，但会实质削弱维度树可追溯性。
- M：2。统计池措辞和 A.4 `passed` 复验证据需要清晰化。
- 最终建议：NEEDS FIX。

