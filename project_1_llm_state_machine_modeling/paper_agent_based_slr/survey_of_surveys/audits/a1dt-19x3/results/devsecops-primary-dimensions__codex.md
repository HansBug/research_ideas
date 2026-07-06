# devsecops-primary-dimensions · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`references/planning-prompts.md`
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- 是否完整阅读 `paper_content.txt`：是；全文 3158 行已覆盖，包含摘要、引言、相关综述比较、MLR 方法、RQ、检索/纳排/QA、TA、结果表、CPTM 模型、RQ2/GSE 缺口、confirmatory search、implications、threats、conclusion、Data availability 与 appendix
- 是否核对 `paper.pdf`：是，做了关键页视觉核对；`pdfinfo` 显示 33 页，抽查了 PDF 第 7、10、20、24 页，确认 Fig. 2、Tables 2--5、Fig. 5、Table 20、Table 21 等关键结构存在。未逐项核对 Fig. 5--9 的所有连线，也未外部打开 Zenodo 复现实验包。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标有两条：一是 review/document/analyze DevSecOps 在 white + grey literature 中的当前状态；二是调查 DevSecOps 在 Global Software Engineering contexts 中的应用。摘要明确给出 MLR 样本为 white literature 104 篇、grey literature 43 篇，时间范围 2012--2021，并用 Thematic Analysis 形成结果。

原文 RQ 是复合型结构：

| 原文问题 | 真实含义 | 对维度树的约束 |
|---|---|---|
| RQ1 | 当前 DevSecOps 状态，包括 aspects、每个 aspect 的 themes、以及它们之间的 links | 不能只列 topic taxonomy，必须复原 aspect -> text segment/code/theme/category -> model/link |
| RQ1.1 | 有哪些 DevSecOps aspects | 至少包含 Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement |
| RQ1.2 | 每个 aspect 有哪些 themes | 必须包含 TA 表中的 theme/code/frequency/source 信息 |
| RQ1.3 | identified aspects and themes 如何互相链接 | 必须包含 CPTM 关系边和 lifecycle stage |
| RQ2 | DevSecOps 如何在 GSE contexts 中被采用 | 必须包含 search string 2、少量 positive hits、GL absence、alternative explanations 和 claim strength |

贡献声明不是普通 taxonomy：原文说其贡献包括 white/grey 双轨 MLR、五大 aspects、OPC/PC/Technology/Business 分类、Challenge-Practice-Tool-Metric model、GSE 缺口，以及开放材料。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法流程是 MLR + reflexive TA：

1. 研究设计：MLR，覆盖 WL 和 GL；前半段偏 positivist，后半段 synthesis/interpretation 偏 interpretive，整体 pragmatic。
2. 检索源：WL 使用 ACM Digital Library、IEEE Xplore、Scopus；ScienceDirect/Springer 不是主库，但用于 snowballing 与 confirmatory search；GL 使用 Google。
3. 检索式：Search String 1 用于 DevSecOps 全局状态；Search String 2 在此基础上加入 GSE/global/distributed/multi-site/multi-nation/transnational/remote work 等词簇。
4. 纳排与质量：纳入要求 DevSecOps primary aspects、英文、2012 年后、方法/设计清楚、来源可信；排除无全文、领域外、方法不严谨、重复、secondary studies。QA 由 14 个 yes/no 问题加 Literature Type 0--4 分组成，满分 18，阈值 11。
5. 分母链：Search 1 最终 102 WL + 43 GL；Search 2 最终 2 WL + 0 GL；摘要合并为 104 WL + 43 GL。Confirmatory search 另有 13 WL + 7 GL，但明确不进入 TA 和最终 CPTM。
6. 数据抽取：使用 adapted data extraction form；开放材料声明包含 protocol、included papers + QA score、raw text/codes、thematic synthesis、TA tables、full CPTM model。
7. 编码/合成：TA 层级是 text -> code -> theme -> category -> model。WL 先归纳，GL 后续主要按 WL codes/themes 演绎分析；CPTM 用 DevSecOps lifecycle framework 作理论框架投影。
8. 研究者过程：第一作者主导 coding/theming，第二、第三作者 weekly/bi-weekly review；作者明确采用 reflexive TA，不用 inter-rater reliability 作质量标准。
9. finding 形成：不是频次直接等于 finding，而是由 frequency、WL/GL contrast、prior-review validation、lifecycle mapping、missing links、confirmatory search 和 implications 共同形成。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式结构很多，当前 `review.md` 的正式维度树没有充分复原：

| 原文结构 | 真实内容 | 维度树应保留的字段 |
|---|---|---|
| QA rubric / Fig. 2 | Authority、Methodology、Objectivity、Publication Date、Novelty、Impact、Literature Type；14 个 yes/no + type 0--4；阈值 11/18 | QA criterion、question、score type、threshold、pass/fail、source type |
| Search execution / Table 3 | Search 1/Search 2 在 applying string、pre-selection、study selection、QA、snowballing 各阶段的 WL/GL 分母 | search_string_id、source_track、database、stage_count、included_count |
| Aspect taxonomy / Fig. 4 & Table 4 | 五大 aspects 与 WL/GL source lists；实践最多，metrics 最少，WL/GL 关注差异 | aspect、source_track、paper_ids、text_segment_frequency |
| TA summary / Table 5 | definitions 28/15 -> 74 codes -> 21 themes -> 4 categories；challenges/practices/metrics/tools 同理 | extracted_data_count、code_count、theme_count、category_count |
| Definition/challenge/practice/metric/tool tables / Tables 6--19 | Cxx/Pxx/Mxx/Txx 编号、frequency、codes、contributing papers、matched prior reviews、measuring/goal/tool names | item_id、theme、frequency、code、source_id、prior_review_match、measuring、goal、tool_group |
| Lifecycle model / Table 20 | Gartner 十阶段 Plan/Create/Verify/Preproduction/Release/Prevent/Detect/Respond/Predict/Adapt 及定义 | lifecycle_stage、stage_definition |
| CPTM / Fig. 5--9 & Table 21 | Challenge-Practice-Tool-Metric 四列、OPC/PC/Technology/Business 颜色类别、C/P/T/M 到 stage 的映射、连线关系 | challenge_id、practice_id、tool_id、metric_id、stage、category、edge_type、missing_link |
| GSE absence / §4.2 | Search String 2 仅 2 WL + 0 GL，四种可能解释，术语遗漏 threat | context_probe、positive_hits、negative_result、alternative_explanation、claim_strength |
| Threats / §5 | selection/QA/extraction bias、synthesis trustworthiness、search string construction | threat_type、mitigation、residual_risk |
| Artifact / Data availability | Zenodo protocol、QA score、raw data/text/codes、thematic synthesis、TA tables、full CPTM；JSS Open Science Board validated | artifact_type、artifact_link、validation_status、verification_status |

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的 finding path 至少有五条：

1. TA 计数和 source type contrast：Practices 关注最高，Metrics/Measurement 最薄弱；WL 更偏 definitions/challenges/practices，GL 更偏 tools/metrics/business。
2. Theme/category synthesis：OPC/PC/Technology/Business 四类高阶主题解释 challenge/practice/metric 的组织方式。
3. Prior-review validation：用 6 篇 secondary studies 比较 overlap 和匹配项，说明本研究确认、更新、补充既有综述。
4. Lifecycle mapping：C/P/T/M 映射到十阶段，并用连线说明 challenge -> practice -> tool -> metric；missing tool/metric 也是 gap 信号。
5. RQ2 negative finding：Search String 2、GL 100 results absence、2 篇边缘 WL、confirmatory search 和四种竞争解释共同支撑 Global DevSecOps 缺口，原文同时承认术语遗漏风险。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确 | `review.md` 将根节点设为 Identifying the primary dimensions of DevSecOps，并识别主类型为“关系型维度树”。这符合原文 RQ1.3 和 CPTM。 | 通过 |
| 主干分支是否覆盖原文 schema | 未充分覆盖 | 当前主干只有 aspect、theme/category、CPTM item、lifecycle stage、GSE context gap。它漏掉 review protocol/search/QA、TA evidence chain、source track、prior-review validation、confirmatory search、quality/trustworthiness、artifact/open-science、finding path 等主干。 | I |
| 叶子维度是否足够具体 | 不足 | `review.md` 第 342--347 行的六个 leaf 是跨论文通用接口；第 313 行虽已说明它不是原文全集，但第 355--359 行的“原文模式候选叶子”只有 5 个粗粒度入口，未展开 C01--C28、P01--P60、M01--M20、T01--T18、Tables 6--21、Search 1/2、QA、artifact 字段。 | I |
| 取值空间是否可执行 | 部分不可执行 | 当前原文候选叶子多写“原文五大方面”“OPC/PC/Technology/Business”等宽泛描述，缺少完整枚举、布尔/数值字段、缺失值语义和字段级证据要求。A2a 执行时仍需重新读原文建表。 | I |
| 关系边是否缺失 | 明显缺失 | 当前只有两条通用边：method-evidence、taxonomy-finding。原文核心边是 challenge -> practice、practice -> tool、practice -> metric、item -> lifecycle stage、item -> category、WL/GL source -> aspect/theme、prior-review -> matched item、context search -> gap。 | I |
| 统计用途 / 分母是否正确 | 有降级但分母不完整 | 当前正确冻结为 schema_seed，避免进入 SUMMARY 定量统计；但未把原文自己的分母链写入维度树：Search 1/2 各阶段计数、102+43/2+0、104+43 合并口径、confirmatory 13+7 不进 TA、Table 5 text/code/theme/category counts。 | I |
| 候选 finding 路径是否完整 | 不完整 | 现有 finding leaf 只写“统计观察与候选发现”，未复原原文从 frequency/source contrast/prior-review validation/lifecycle mapping/missing links/GSE negative search 到 implications/future work 的路径。 | I |
| A.1--A.4 证据链是否足够 | 不足 | A.1 存在；A.2--A.3 结构存在且全部弱化为 `not_verified`/`weak`，这符合 A1-DT 降级纪律。但 EV-002/003/005 是大包证据，页码、表号、行号、短引、支撑对象都过泛，不能支持 A2a 直接回填。 | I |
| 是否存在可能误导 A2a 的强主张 | 未发现强误导，但有维护风险 | `review.md` 第 313、351、372--374、407--418 行明确声明 schema_seed、not_verified、不得进入统计，避免了最大风险。但正式“维度树结构”仍把六个通用接口摆在主叶子表，后续读者若只看树图，仍可能误以为原文 schema 已足够复原。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为原文 schema 的完整复原。建议保留六个通用接口作为审计 wrapper，但把正式原文树改为下列骨架。

| 层级 | 节点 / 叶子 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| 根节点 | DevSecOps primary dimensions MLR schema | RQ1/RQ2 + MLR + TA + CPTM | 局部可统计 | not_applicable | 摘要、§3.3、§4 |
| 主干 | 研究问题与贡献 | RQ1、RQ1.1、RQ1.2、RQ1.3、RQ2；目标 a/b；贡献：MLR、TA、CPTM、GSE gap | 是，作为 RQ 类型统计 | not_reported | §3.3、摘要 |
| 主干 | 语料收集与纳排链条 | source_track = WL/GL/confirmatory；database = ACM/IEEE/Scopus/Google/ScienceDirect/Springer；search_string_id = S1/S2；stage = applying/preselection/selection/QA/snowballing | 是 | not_reported / not_applicable | §3.4--§3.7、Table 3 |
| 叶子 | Search String 1 | `(devops AND security/secure/safe) OR secdevops OR devsecops` 及数据库变体 | 是 | not_verified for database-specific syntax | §3.4.2 |
| 叶子 | Search String 2 / context probe | S1 + GSE/global/distributed/multi-site/multi-nation/transnational/remote work 词簇 | 是 | no_hits / term_missed_possible | §3.4.2、§4.2 |
| 叶子 | inclusion / exclusion criteria | inclusion a--e；exclusion a--e | 可描述统计 | not_reported | §3.5 |
| 叶子 | quality rubric | 6 criteria、14 yes/no、literature type 0--4、threshold 11/18 | 是 | qa_not_available | Fig. 2、§3.5 |
| 主干 | TA 抽取与编码链 | text segment -> code -> theme -> category -> model；inductive WL + deductive GL；manual notes/tables | 是 | not_reported / coder_note_missing | §3.8.1--§3.8.2 |
| 叶子 | source track | WL、GL、confirmatory | 是 | source_unknown | Table 4、Table 5 |
| 叶子 | coding/trustworthiness process | first-author coding、weekly/bi-weekly consensus、Braun checklist、credibility/confirmability/dependability/transferability | 可作方法字段 | not_reported | §3.8.2--§3.8.3、§5.2 |
| 主干 | Aspect taxonomy | Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement | 是 | no_text_segment | §4.1.1、Fig. 4、Table 4 |
| 叶子 | aspect count by source | Definitions 28/15；Challenges 73/53；Practices 219/137；Tools 18/45；Metrics 7/13 等 | 是 | not_verified before PDF/table check | Fig. 4、Table 5 |
| 主干 | Category schema | OPC、Process Capabilities、Technology、Business；Tools single Technology；Metrics OPC/PC/Technology plus complemented Business metric | 是 | category_unassigned | §4.1.2、Table 5 |
| 主干 | Definition schema | definition text segment、code、theme、category、source_id、common definition author、citation count | 是 | no_definition | Tables 6--7 |
| 主干 | Challenge schema | C01--C28、category、frequency、codes、source IDs、prior-review match、linked practices、stage | 是 | no_linked_practice / no_prior_review_match | Tables 8--11、Table 21 |
| 主干 | Practice schema | P01--P60、category、frequency、codes、source IDs、addresses_challenge、linked_tool、linked_metric、stage | 是 | no_linked_tool / no_linked_metric | Tables 12--15、Table 21 |
| 主干 | Metric schema | M01--M20、category、measuring method、goal、source IDs、mapped DevOps metric、stage | 是 | no_measuring_method / no_goal | Tables 16--18、Table 21 |
| 主干 | Tool schema | T01--T18、function group、tool names、source IDs、complemented prior-review tools、stage | 是 | no_tool_reported | Table 19、Table 21 |
| 主干 | Lifecycle projection | Plan、Create、Verify、Preproduction、Release、Prevent、Detect、Respond、Predict、Adapt | 是 | stage_not_mapped | Table 20、Table 21、Fig. 5--9 |
| 关系边 | CPTM edges | challenge -> practice；practice -> tool；practice -> metric；item -> stage；item -> category | 是，边表可统计 | no_linked_practice / no_linked_tool / no_linked_metric | §4.1.3、Fig. 5--9、Table 21 |
| 主干 | GSE gap / negative evidence | Search 2 hit chain、2 WL positive edge cases、0 GL、four explanations、term-missing threat | 是，但 claim strength 需弱化 | no_hits / alternative_explanation_open | §4.2、§5.3 |
| 主干 | Confirmatory search | 13 WL + 7 GL；not in TA/CPTM；used for validation/trend | 是，必须单独分母 | confirmatory_only | §3.7、§4.3 |
| 主干 | Evidence / artifacts | protocol、included papers + QA score、raw text/codes、thematic synthesis、TA tables、full CPTM、JSS OS board validation | 可统计 artifact availability | not_verified_external / link_dead / by_request | 摘要、Data availability |
| 主干 | Threats / validity | selection bias、QA subjectivity、data extraction bias、synthesis trustworthiness、search string construction | 可作 threat taxonomy | not_reported | §5.1--§5.3 |
| 主干 | Finding path | aspect frequency、WL/GL contrast、prior-review validation、lifecycle concentration、missing links、GSE absence、confirmatory trend、implications/future validation | 候选 finding，不直接 final | no_counterevidence / scope_limited | §4.1.4、§4.2.3、§4.3--§4.4、§6 |

最小修复方案：把 `review.md` 中“原文模式候选叶子映射（A1 种子）”从 5 个粗粒度入口升级为上述正式原文 schema 表；六个通用 leaf 保留为跨论文审计接口，但不要作为“维度树结构”的唯一叶子层。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 扩展正式原文维度树 | `review.md` 的 `## 维度树复原`、`### 维度树结构`、`### 原文模式候选叶子映射` | 将当前 5 个原文候选叶子升级为正式原文 schema：ReviewProtocol、Search/Selection/QA、TA chain、Aspect taxonomy、Definition/Challenge/Practice/Metric/Tool schema、Lifecycle projection、CPTM edges、GSE gap、Confirmatory search、Artifacts、Threats、Finding path。 | 摘要；§3.3--§3.8；§4.1--§4.4；§5--§6；Data availability | I |
| 将六个通用 leaf 降为 wrapper | `### 维度树结构` 与 `### 叶子维度表` | 明确把 scope/corpus/taxonomy/method/evidence/finding 六项放入“跨论文审计接口映射”，不要作为原文树的主叶子全集；正文树图应优先展示原文 schema。 | `review.md` 第 313、323--347 行；GUIDE §6.3.2--§6.3.3 | I |
| 补全 relation edge table | `### 关系边表` | 新增 challenge -> practice、practice -> tool、practice -> metric、item -> lifecycle stage、item -> category、source_track -> aspect/theme、prior_review -> matched item、search2 -> GSE gap 等边；缺失边写 `no_linked_tool` / `no_linked_metric` / `no_hits`。 | §4.1.3、Fig. 5--9、Table 21、§4.2 | I |
| 补全统计分母与样本池资格 | `### 统计与候选发现链路` | 单独记录 Search 1、Search 2、confirmatory search、main TA/CPTM sample、prior review validation pool；明确 13+7 confirmatory 不进入 TA/CPTM。 | §3.7、Table 3、§4.3 | I |
| 补 quality / validity / artifact 字段 | `### 原文模式候选叶子映射` 或新增 `质量与开放制品节点` | 加入 QA rubric、QA threshold、trustworthiness components、threat types、Zenodo artifact list、JSS Open Science Board validation；Zenodo 外部制品若未打开，应写 `not_verified_external`。 | Fig. 2、§3.5、§3.8.3、§5、Data availability | I |
| 拆分 A.2 泛证据 | `### A.2 维度树证据账本` | 将 EV-002/003/005 拆成至少 RQ、search execution、QA、TA summary、aspect taxonomy、CPTM model、Table 21、GSE gap、confirmatory search、threats、data availability 等证据；补行号/页码/表图编号/短释义。 | `paper_content.txt` 行 418--433、539--561、657--665、691--755、796--950、1655--1748、1870--1991、2094--2220；PDF 第 7/10/20/24 页抽查 | I |
| 补 conclusion/finding path ledger | `### 统计与候选发现链路`、A.3 | 用 `observation -> interpretation -> candidate finding -> limitation/future validation` 形式记录 metrics thin、WL/GL complementary、business GL/WL asymmetry、GSE absence、framework-design trend、CPTM open areas。 | §4.1.4、§4.2.3、§4.3--§4.4、§6 | I |
| 保留降级口径 | 全文与 A.3 | 当前 `schema_seed` / `not_verified` / `weak` 口径是正确的；修复时不要把 A1-DT 证据升级为 `statistical_synthesis`，除非完成页码、表图、Zenodo 精核。 | GUIDE §6.3.7；`review.md` 第 351、372--374、407--418 行 | M |

## 6. C/I/M 结论

- C：无。当前 `review.md` 已经显式声明六个通用 leaf 不是原文叶子全集，并将原文候选叶子、A.2 证据和 A.3 结论整体降级为 `schema_seed` / `not_verified` / `weak`，未把 roadmap/vision 或泛定位证据升级为可统计结论。
- I：有。正式“维度树复原”仍过小，不能完整、准确、可追溯地复原原文 schema；缺少 review protocol/search/QA/TA/source track/definition/challenge/practice/metric/tool/CPTM edge/GSE gap/confirmatory/artifact/threat/finding path 的可执行字段。这会实质影响 Paper2 A2a/A2b 的模式复用、字段回填、统计分母和证据审计可靠性。
- M：有。当前降级声明有效，但树图和叶子表的视觉主结构仍容易让后续读者先看到六个通用接口；建议版式上将“原文 schema 树”置于通用接口之前。
- 最终建议：NEEDS FIX
