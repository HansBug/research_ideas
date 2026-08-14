# mde-ml-components-slr · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（对应任务中的 `codex` 学术 reviewer）；未开启 sub-subagent，未修改 `review.md`，未 push，未 gh comment。
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。本审计按 claim-evidence-engineering 口径执行，强主张必须回到原文或仓库证据。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`references/planning-prompts.md`。本审计按“先忠实复原方法/RQ/数据/评价，再规划可执行修复”的口径执行。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本任务未启动 autoresearch loop，只采用其 artifact-gated completion 口径：审计产物必须落盘且可复查。
- 是否完整阅读 `paper_content.txt`：是；已分段阅读 `paper_content.txt` 全文 1--2123 行，覆盖文本抽取的 22 页，包括摘要、引言、方法、RQ、检索/筛选、data extraction、quality assessment、RQ1--RQ4 结果、RQ Answer Summary、Threats、Discussion roadmap、Conclusion、Data availability、Appendix A/B 与参考文献。
- 是否核对 `paper.pdf`：是，局部图表级核对；`pdfinfo` 显示 22 页，已用 `pdftoppm`/截图视觉核对关键版面：PDF p7 的 Fig. 4/5/6/Table 2，p8 的 Table 3，p9 的 Table 4/5，p10 的 Fig. 7/Table 6，p11 的 Fig. 8/RQ1 summary，p12 的 Fig. 9/Table 7，p14 的 Table 8/Fig. 10，p16 的 RQ4 summary/Threats/Discussion 起点，p19 的 Table 9。未逐项复核所有表格数值与外部 GitHub 数据仓库当前可访问性。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是对 Model-driven Engineering for Machine Learning components（MDE4ML）做 SLR，分析 motivations、MDE solutions、evaluation techniques、benefits、limitations，并给出 gaps 与 future research directions。摘要和引言给出的检索规模是 7 个数据库初始 3934 条、最终 46 篇 primary studies；结论处另写 3496，当前应按方法节 3934 作为主证据并记录不一致风险。

原文四个 RQ 是真正的维度树主干，而不是附属背景：

| RQ | 原文对象 | 直接导出的字段族 |
|---|---|---|
| RQ1 | applying MDE to systems with ML components 的 motivation | goal/sub-goal、ML technique、application domain、end user、contribution、ML aspect |
| RQ2 | MDE approaches and tools | model representation、modeling language、model level/type、supported ML aspects、framework/library、transformation、generated artifact、automation、tool availability、meta-tool/framework/transformation language |
| RQ3 | evaluation | target area、evaluation method、ML metrics、MDE metrics、datasets、no metrics / N/A |
| RQ4 | limitations and future work | approach limitation、evaluation limitation、solution-quality limitation、approach enhancement、further evaluation、quality enhancement |

证据：`paper_content.txt:338-360` 给出四个 RQ；`paper_content.txt:499-519` 说明 40-question Google Form 直接对应四个 RQ。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

方法流程遵循 Kitchenham SLR guidelines，分 planning、conducting、reporting。检索和筛选链条为：2023-03 自动检索 7 个数据库得到 3934 条，去重后 3570 条；title/abstract 筛到 72 条；brief full-paper screening 到 55 条；data extraction 阶段到 32 条；再通过三轮 forward/backward snowballing 增补 14 条，最终 46 条。纳入/排除标准见 Table 1，包含全文可得、peer-reviewed、English、MDE for ML；排除 AI4MDE、vision、grey literature、secondary/tertiary studies 等。

数据抽取是原文 schema 的核心：作者建立 40 个问题的 Google Form，分 5 个 section：general information/publication trends、motivations/goals/application domain/users、MDE approaches、evaluation techniques/tools、limitations/future challenges；答案形态为 23 short answers、10 long answers、2 checkboxes、14 radio buttons。第一作者先抽取 6 篇并与其他作者同批结果比对，close match 后由第一作者抽取其余论文；数据综合由图、表和统计分布完成。

质量评价是独立 rubric：QA1--QA5，1--5 分；QA3--QA5 对无 evaluation 研究标 NA；结果为 19/46 good、15/46 average、12/46 poor，未因质量低排除以降低 publication bias。证据：`paper_content.txt:520-540`，Table 9 位于 PDF p19 / `paper_content.txt:1693-1718`。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文有多个显式 schema / taxonomy，不应被压成 5 个泛化候选叶子：

| 原文结构 | 原文证据定位 | 结构性质 |
|---|---|---|
| 40-question Google Form | `paper_content.txt:499-519` | extraction form；5 section；题型和 pilot 机制明确 |
| Fig. 5 feature tree | `paper_content.txt:567-570`，PDF p7 | “MDE Solution for ML” feature tree；第一层含 Goal、Domain、End Users、Modeling、Supported ML Aspects、Tool Support、Evaluation、Scalability、Responsible ML；Modeling 和 Tool Support 还有二级节点 |
| Table 3 goals | `paper_content.txt:611-633`，PDF p8 | Goal/Sub-goal/Studies 分类表；含 effort reduction、quality improvement、stakeholder understanding 及具体 sub-goals |
| Table 4 ML techniques | `paper_content.txt:687-728`，PDF p9 | Generic / supervised / unsupervised / reinforcement learning 分类；supervised 下有 traditional、neural networks、both |
| Table 5 end users | `paper_content.txt:729-742`，PDF p9 | ML-related、software & systems、other roles 的 end-user taxonomy |
| Table 6 contributions | `paper_content.txt:772-843`，PDF p10 | contribution taxonomy；code/text/model generator、DSL、framework、model、approach、extension、knowledge base 等 |
| Fig. 7 relation map | `paper_content.txt:804-813`，PDF p10 | study goal / contribution 与 ML aspect 的关系型统计图；需要关系边表 |
| Fig. 8/9/Table 7/Table 8 | `paper_content.txt:865-1075`，PDF p11--p14 | RQ2 solution/tool schema；modeling、ML aspects、framework/library、transformations、generated artifacts、automation、tool/meta-tool |
| Fig. 10 | `paper_content.txt:1115-1219`，PDF p14 | ML metrics / MDE metrics 分类；含 no metrics 与 N/A |
| RQ Answer Summary | `paper_content.txt:849-864`, `1061-1075`, `1220-1231`, `1322-1331` | 从字段统计生成每个 RQ 的中间结论 |
| Threats to validity | `paper_content.txt:1332-1384` | internal / construct / conclusion / external validity |
| Discussion roadmap | `paper_content.txt:1385-1600` | 从统计观察到 gaps/recommendations 的 finding path |
| Data availability | `paper_content.txt:1636-1638` | SLR data artifact；需后续核验链接、内容、license、是否含 extraction form |

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文形成 finding 的路径是：RQ → extraction form fields → feature tree / 分类表 / 图形统计 → RQ Answer Summary → Discussion roadmap / recommendations。典型例子：

- RQ1 的 Table 3、Fig. 6、Table 4/5/6 与 Fig. 7 支撑“effort reduction 主导、quality/stakeholder understanding 较少、monitoring/documentation 被忽视”的 RQ1 summary。
- RQ2 的 Fig. 8/9、Table 7/8 支撑“PIM/design models、DSL、M2T、full automation、tool availability、generated artifacts、EMF/Sirius/XTend”等 solution/tool 结论。
- RQ3 的 evaluation context/method/metrics/datasets 支撑“industrial/user studies 少、MDE metrics 少、偏 ML aspects”的评价缺口。
- RQ4 的 limitations/future work taxonomy 支撑“>88% 无 industrial evaluation 和 user study、48% 只评价一方面、17% 无 evaluation、future work 多为 enhancement/further evaluation”的 summary。
- Discussion 再把这些统计观察转为 recommendation：data first-class、扩展 requirements/integration/deployment/monitoring/documentation、关注 unsupervised/RL、补 MDE details、提升 tool maturity/open artifacts、domain expert/low-code、统一 terminology、scalability、responsible ML、evaluation rigor。

这条 path 对 Paper2 很关键：它说明 finding 不是频次本身，而是字段统计、缺失/反向证据、解释和建议的组合；Paper2 还需要额外加入 researcher challenge/adjudication。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但不够贴合原文显式 root | 当前 root 写为 “Model driven engineering for machine learning components”，方向正确；但原文 Fig. 5 的显式 root 是 “MDE Solution for ML”，且 RQ1--RQ4 是主干，当前 `review.md:327-345` 用 b1--b5 通用接口替代原文主干。 | M |
| 主干分支是否覆盖原文 schema | 未覆盖 | 当前主干为“范围/语料/主题/方法/评价 finding”五类通用接口；原文主干应至少覆盖 protocol/extraction form、RQ1 motivation、RQ2 solution/tool、RQ3 evaluation、RQ4 limitations/future work、quality/threats/data availability/finding path。`review.md:331-345` 不足以表达 Fig. 5、Tables 3--8、Fig. 7/10、QA 和 roadmap。 | I |
| 叶子维度是否足够具体 | 不足 | `review.md:350-357` 明确只有 6 个跨论文通用 leaf；`review.md:359-369` 另列原文候选叶子，但只有 5 个，遗漏 goal/sub-goal、ML technique、domain、end users、contribution、modeling representation/language/level/type、ML aspect、framework/library、transformation、generated artifacts、automation、tool availability、metrics、dataset、QA、threat、artifact 等。 | I |
| 取值空间是否可执行 | 不足 | 通用 leaf 的取值空间多为“自由文本/完整枚举/层级枚举”等类型说明；5 个原文候选叶子也只给粗略示例，未列原文封闭枚举、分母、not_reported/no evaluation/no metrics/N/A 等缺失语义。 | I |
| 关系边是否缺失 | 缺失 | 原文 Fig. 7 是 goal/contribution 与 ML aspect 的关系型统计；Table 7/8 也有 framework/meta-tool/transformation language 的结构关系。当前没有关系边表，无法表达“哪些 goal/contribution 关联哪些 ML aspects”，也不能把缺失关系作为 gap evidence。 | I |
| 统计用途 / 分母是否正确 | 方向正确但粒度不足 | 当前明确 A1-DT 不进主统计池，这是正确降级；但统计链路只写“本文纳入样本或分类表 / 统计结果 + discussion”，未为每个原文字段绑定分母 46、23/46、17/46、not_applicable 等语义，也未区分 Table/Fig 的分母。 | I |
| 候选 finding 路径是否完整 | 不完整 | 当前 `review.md:371-377` 只保留 generic “统计观察与候选发现”；未把 RQ Answer Summary → Discussion roadmap 的具体路径列出，也未记录 support counts、counter/absence evidence、scope、recommendation 类型。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，但证据过泛 | A.1 存在；A.2 只有 4 条泛证据，EV-002/003 写“方法 / 结果页”“邻近段落”“表 / 图待核验”；A.3 回链存在但多数结论是 generic leaf_definition。符合 not_verified 降级纪律，但不足以支撑“维度树完整复原”。 | I |
| 是否存在可能误导 A2a 的强主张 | 有局部风险，但未升级为统计结论 | 优点是 `review.md:323` 已明确 6 个 leaf 不是原文全集，且 A.3 多为 weak/schema_seed；但快速卡片 `review.md:23` 称“提供一棵非常清楚的维度树”，而正式维度树实际仍是通用接口 + 5 个候选叶子，可能让 A2a 误以为原文 schema 已基本复原。 | I |

总体判断：当前 `review.md` 已经意识到“通用 6 leaf 不是原文 schema”，这一点避免了最严重的误读；但它没有完成原文 schema 复原。当前状态更像“通用接口 + 少量 A2a 待办提示”，不是可直接作为 Paper2 维度模式库种子的全文级维度树。

## 4. 建议维度树骨架

### 根节点与主干

建议 root 改为：

```text
[dim-mde-ml-components-slr-root] MDE Solution for ML / MDE4ML SLR schema
├── [dim-*-p0] SLR protocol and extraction form
├── [dim-*-rq1] RQ1 Motivation / goals / context
├── [dim-*-rq2] RQ2 MDE approaches and tools
├── [dim-*-rq3] RQ3 Evaluation
├── [dim-*-rq4] RQ4 Limitations and future work
├── [dim-*-quality-validity-artifact] Quality / validity / data artifact
└── [dim-*-finding-path] RQ summary to discussion roadmap
```

### 建议叶子表

| 叶子维度 | 父节点 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| RQ set | p0 | RQ1 motivation；RQ2 approaches/tools；RQ3 evaluation；RQ4 limitations/future work | 可作 schema seed；A2a 后可统计 RQ coverage | not_reported 不适用；本文已报告 | `paper_content.txt:338-360` |
| Search database | p0 | IEEE Xplore、ACM DL、Springer、Wiley、Scopus、Web of Science、ScienceDirect | 可统计数据库覆盖 | not_reported / adapted_search | `paper_content.txt:379-390`, `420-430` |
| Screening chain | p0 | 3934 → 3570 → 72 → 55 → 32 → +14 → 46 | 可统计，分母为检索条目和 primary studies | count_conflict（3496 vs 3934） | `paper_content.txt:420-449`, `491-498`, `1605-1609` |
| Inclusion/exclusion criteria | p0 | I01--I04；E01--E10 | 可统计 criteria 类型 | not_reported | Table 1 / `paper_content.txt:397-414` |
| Extraction form shape | p0 | 40 questions；5 sections；23 short answers；10 long answers；2 checkboxes；14 radio buttons | 可统计 extraction form 复杂度 | form_not_available / not_verified | `paper_content.txt:499-519` |
| Pilot / coder process | p0 | first author + coauthor pilot；6 papers；close match；remaining by first author | 可统计 process evidence；不作领域 finding | no_inter_rater_stats / not_reported | `paper_content.txt:510-519`, `1361-1369` |
| Goal category | rq1 | effort reduction；quality improvement；increased stakeholder understanding | 可统计，多选，分母 46 | not_reported | Fig. 6/Table 3；`paper_content.txt:573-599`, `611-633` |
| Goal sub-goal | rq1 | abstraction、automation、integration、monitoring、system management、data management、reusability、extensibility、standardization、responsible ML、interoperability、maintainability、scalability、reliability、support non-ML experts、common language | 可统计，多选，分母 46 | not_reported | Table 3 / PDF p8 |
| ML technique | rq1 | generic；supervised-traditional；supervised-neural networks；supervised-both；unsupervised；reinforcement | 可统计，分母 46 | no_explicit_type / zero_count | Table 4 / `paper_content.txt:687-728` |
| Application domain | rq1 | generic/no specific domain；CPS；manufacturing；autonomous vehicles；smart homes；traffic signal control；satellite communication；network planning；big data analytics；data analytics；social bots | 可统计，分母 46 | domain_not_specific / not_reported | `paper_content.txt:708-752` |
| End user | rq1 | ML engineer；data analyst/engineer/scientist；software engineer；systems engineer；业务分析师；formal methods analyst；domain expert | 可统计，多选，分母 46 | not_reported | Table 5 / `paper_content.txt:729-765` |
| Contribution | rq1/rq2 | code generator；text generator；model generator；DSL；framework；model；modeling approach；language extension；ML knowledge base；data synthesizer；OCL constraints；API；meta-modeling language | 可统计，多选，分母 46 | not_reported | Table 6 / `paper_content.txt:772-843` |
| Goal-contribution-ML aspect relation | rq1/rq2 | relation value：goal × ML aspect；contribution × ML aspect；frequency bubble size | 可统计为关系边 | no_linked_aspect / not_reported | Fig. 7 / `paper_content.txt:804-813` |
| Model representation | rq2 | graphical；textual；both | 可统计，分母 46 | not_reported | Fig. 8(a) / `paper_content.txt:865-881` |
| Modeling language | rq2 | DSL；GPL；language extension | 可统计，分母 46 | not_reported | Fig. 8(b) / `paper_content.txt:882-899` |
| Model level / type | rq2 | CIM；PIM；PSM；requirements-level；design-level；data-representation；feature/process/deployment | 可统计，多选，分母 46 | not_reported | `paper_content.txt:900-918` |
| Supported ML aspect | rq2 | requirements engineering、data preprocessing、design/development、training、evaluation、deployment、integration、inference、monitoring、management、data generation、data storage、data visualization、documentation、ML pipeline development、ML knowledge base development 等 17 类 | 可统计，多选，分母 46 | not_reported / no_supported_aspect | Fig. 9(a) / `paper_content.txt:919-978` |
| ML framework / library | rq2 | TensorFlow、MXNet、PyTorch、Keras、Weka、Scikit-learn、NumPy 等 | 可统计，多选 | not_reported / not_applicable | Table 7 / `paper_content.txt:957-990` |
| Transformation type | rq2 | M2T；M2M；both；forward engineering | 可统计，分母 46 | not_reported | `paper_content.txt:991-1010` |
| Generated artifact | rq2 | ML model/training code；software/intermediate models；deployment configurations；datasets/subsets；text files；API code；recommendation rules/queries；meta-models；generated language Python/Java/C++等 | 可统计，多选，分母 46 | no_generated_artifact / not_reported | `paper_content.txt:1016-1030`, Fig. 9(b) |
| Automation level | rq2 | fully automated；partially automated | 可统计，分母 46 | not_reported | Fig. 8(c) / `paper_content.txt:1031-1038` |
| Tool availability | rq2/artifact | open-source；proprietary；not mentioned | 可统计，分母 46 | not_mentioned | `paper_content.txt:1039-1045` |
| Meta-tool/framework/transformation language | rq2 | EMF、xText、Sirius、Eclipse IDE、XTend、EGL、ATL 等 | 可统计，多选 | absent_from_table = not mentioned | Table 8 / `paper_content.txt:1046-1060`, `1143-1172` |
| Evaluation context | rq3 | academia；industry；both | 可统计，分母 46 | no_evaluation / not_reported | `paper_content.txt:1076-1086` |
| Evaluation method | rq3 | case study；experiment；survey/user study；criteria-based assessment；no evaluation | 可统计，多选，分母 46 | no_evaluation | `paper_content.txt:1087-1114` |
| ML metrics | rq3 | classification；regression；time/resource；fairness；not mentioned；N/A | 可统计，分母 46 | no_metrics / N/A | Fig. 10(a) / `paper_content.txt:1115-1189` |
| MDE metrics | rq3 | quality；time/resource；code；not mentioned；N/A | 可统计，分母 46 | no_metrics / N/A | Fig. 10(b) / `paper_content.txt:1190-1214` |
| Dataset | rq3 | MNIST；Iris；其他 33 个 datasets | 可统计，分母 46 | no_dataset / not_reported | `paper_content.txt:1215-1219` |
| Limitation category | rq4 | approach；evaluation；solution quality；not mentioned | 可统计，分母 46 | not_mentioned | `paper_content.txt:1232-1268` |
| Future-work category | rq4 | improvement/extension of approach；further evaluation；quality enhancement；not mentioned | 可统计，分母 46 | not_mentioned | `paper_content.txt:1269-1317` |
| QA rubric | quality-validity-artifact | QA1--QA5；score 1--5；NA for QA3--QA5 without evaluation；good/average/poor | 可统计，分母 46 | NA / no_evaluation | `paper_content.txt:520-540`, Table 9 |
| Threat category | quality-validity-artifact | internal；construct；conclusion；external validity | 可统计 presence/coverage，不作领域 finding | not_reported | `paper_content.txt:1332-1384` |
| Data availability / SLR artifact | quality-validity-artifact | dataset link present；repository URL；current accessibility；license；contains extraction data/form/scripts | 可统计 artifact availability；当前需人工/联网核验 | not_verified / link_dead / no_license | `paper_content.txt:1636-1638`；当前未复核 GitHub 内容 |
| RQ Answer Summary | finding-path | RQ1--RQ4 summary text + supporting field counts | 可作为 candidate finding input | summary_missing / unsupported_summary | `paper_content.txt:849-864`, `1061-1075`, `1220-1231`, `1322-1331` |
| Discussion roadmap item | finding-path | data first-class、solution focus、ML type、MDE details、maturity/open-source、domain experts、terminology、scalability、responsible ML、real-world evaluation、evaluation rigor | 候选 finding / recommendation；不可直接作 Paper2 final finding | recommendation_without_support / not_verified | `paper_content.txt:1385-1600` |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把正式维度树主干改为原文 RQ/Fig.5 驱动，而不是 b1--b5 通用接口 | `review.md` 的 `## 维度树复原`，尤其 `维度树结构` | 保留通用接口作为跨论文 envelope，但新增或替换为 root = `MDE Solution for ML / MDE4ML SLR schema`，主干为 protocol/extraction form、RQ1、RQ2、RQ3、RQ4、quality/validity/artifact、finding path。 | Fig.5；`paper_content.txt:338-360`, `567-570` | I |
| 扩充“原文模式候选叶子映射” | `review.md:359-369` | 从 5 个候选叶子扩到至少 30 个原文字段叶子，覆盖 Table 3--8、Fig.7/10、QA、Data availability、Threats、RQ summaries 和 Discussion roadmap。 | `paper_content.txt:499-519`, `611-843`, `865-1231`, `1322-1384`, `1636-1638` | I |
| 修复候选取值空间错误/过粗 | `原文模式候选叶子映射` 与叶子表 | 例如“动机/收益”不能写成“自动化、质量、可维护性、可追踪性、复用和合规”；应按 Table 3 的 goal/sub-goal 原样列出 effort reduction、quality improvement、stakeholder understanding 及其 sub-goals。 | Table 3；`paper_content.txt:611-633` | I |
| 增加关系边表 | `维度树复原` 中新增 `关系边表` | 至少加入 Fig.7 的 `goal -> ML aspect`、`contribution -> ML aspect` 关系，记录 bubble frequency、缺失关系语义和候选 finding 用途。 | Fig.7；`paper_content.txt:804-813`，PDF p10 | I |
| 为每个叶子补分母与缺失语义 | `叶子维度表` 与 `统计与候选发现链路` | 对每个字段写明分母 46 或阶段分母，区分 `not_reported`、`not_mentioned`、`no_evaluation`、`no_metrics`、`N/A`、`zero_count`、`not_verified`。 | RQ2/RQ3/RQ4 结果段；Fig.10 | I |
| 补 extraction form / coding scheme 细节 | `维度树复原` 的 protocol 分支 | 明确 40 questions、5 sections、题型数量、pilot 6 papers、first-author remaining extraction、close match 无 kappa 的边界。 | `paper_content.txt:499-519`, `1361-1369` | I |
| 补 quality / QA 字段 | `评价、证据与复现资产` 分支 | 加入 QA1--QA5、score 1--5、NA 规则、good/average/poor 统计、未按 QA 排除的解释。 | `paper_content.txt:520-540`, Table 9 | I |
| 补 data availability / artifact 字段 | `评价、证据与复现资产` 分支与 A.4 | 将 SLR data link 作为一等 artifact leaf，记录 current accessibility、license、是否含原始 Google Form / coding sheet / extraction data / scripts；当前只能写 `not_verified`。 | `paper_content.txt:1636-1638`；PDF首页 Dataset link | I |
| 补 finding path ledger | `统计与候选发现链路` | 将每个 RQ Answer Summary 与 Discussion roadmap item 拆为 candidate finding：supporting counts、absence/counter evidence、scope、recommendation、claim strength、是否需要研究者裁决。 | `paper_content.txt:849-864`, `1061-1075`, `1220-1231`, `1322-1331`, `1385-1600` | I |
| 精化 A.2 证据账本 | A.2 | 将 EV-002/003 拆成多条具体证据：RQ、extraction form、Fig.5、Table 3、Table 4/5、Table 6、Fig.7、Fig.8/9、Table 7/8、Fig.10、Table 9、Threats、Data availability、Conclusion discrepancy。 | 当前 A.2 只有 `review.md:400-403` 的泛定位证据 | I |
| 修正快速卡片中的强表述 | `review.md:16-24` | 将“提供一棵非常清楚的维度树”改为“原文提供清楚 feature tree，但本节当前只完成 envelope + A2a 候选入口”；避免误导 A2a。 | 当前 `review.md:16-24`, `323`, `359-369` | M |
| 保留 3934/3496 数量不一致为风险，不作强统计 | 待复核与 A.2/A.3 | 方法节和摘要使用 3934，结论处 3496 标记为 count_conflict；正式引用前核对 PDF/出版版本。 | `paper_content.txt:34`, `420-430`, `1605-1609` | M |

## 6. C/I/M 结论

- C：0。当前 `review.md` 已显式声明 6 个通用 leaf 不是原文 leaf 全集，并把证据降级为 `weak` / `not_verified` / `schema_seed`，没有把泛定位证据升级为可统计 final finding；因此未达到“直接破坏 Paper2 学术目标”的 C 级。
- I：8。主问题是原文 schema 复原过小：正式维度树仍由通用接口主导，原文候选叶子只有 5 个，遗漏 RQ/extraction form/Fig.5/Table 3--8/Fig.7/Fig.10/QA/validity/data artifact/finding path 的核心字段；A.2/A.3 回链存在但过泛。这会实质影响 A2a 的字段精核任务、维度模式库、统计分母和候选 finding 可靠性。
- M：2。包括快速卡片表述需降强、3934/3496 数量冲突需在证据账本中更明确记录。
- 最终建议：NEEDS FIX。最小修复不是重写全文详读部分，而是把 `维度树复原` 升级为“通用 envelope + 原文 RQ/Fig.5/表图驱动的完整候选叶子表 + 关系边表 + 精细 A.2/A.3 回链”。
