# mdse-modelling-assistants-mapping · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是。已读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`；本审计按 claim-evidence、reviewer risk、unsupported claim 降级口径执行。
- 是否读取 `$research-planning`：是。已读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`；本审计按“先理解研究问题、方法、评价、风险，再输出可执行结构”的口径复原原文 schema。
- 是否读取 `$oh-my-codex:autoresearch`：是。已读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`；本审计未启动 autoresearch loop，只采用其 artifact-gated、validator-gated 的完成意识。
- 是否完整阅读 `paper_content.txt`：是。已按 Page 1--19 连续阅读摘要、引言、相关工作、系统映射设计、RQ1--RQ3 结果、RQ4 实践侧 review、比较分析、validity、conclusion / future work、data availability 和参考文献区；重点核对了 `paper_content.txt` 行 70--100、206--246、340--399、417--450、455--560、568--824、902--1118、1144--1218、1221--1341、1360--1465。
- 是否核对 `paper.pdf`：是，局部核对。使用 `pdfinfo` 确认 PDF 为 19 页；用 `pdftoppm` 在 `/tmp` 渲染并人工查看第 4、6、8、11、14、17 页，确认 Table 1、Table 2、Fig. 5 / Table 4、Table 5、Fig. 13、Fig. 15 的版面和 `paper_content.txt` 抽取大体一致。未逐页视觉核对全部图 1--15 和所有 bubble chart 数值，因此表图精确页码 / 视觉细节仍应留给 A2a。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文目标是理解 MDSE / low-code / no-code 工具中“辅助人类完成软件建模任务”的研究与实践现状。其核心定义是：modelling assistance 是任何旨在辅助人类在 MDSE 工具中完成软件建模任务的 strategy，包括 method、technique、framework、guideline 等。

原文主问题与子问题如下：

| 层级 | 原文问题 | 审计复原 |
|---|---|---|
| MRQ | What proposals exist in the literature and practice to assist humans during modelling tasks in MDSE tools? | 根问题同时覆盖 literature 与 practice，不是单纯文献 SLR。 |
| RQ1 | How is software modelling assisted? | strategy / assistance type 分类。 |
| RQ2 | What goals and limitations do existing modelling assistance proposals report? | goal 与 limitation 双字段，且缺失报告本身进入结果。 |
| RQ3 | Which evaluation metrics and target users do existing modelling assistance proposals consider? | metric 与 target user 双字段，含 NE / U-NS。 |
| RQ4 | What is the state of the practice on modelling assistance? | GMQ 工具文档 review，将 vendor quote 映射到 S/G/L/M/U。 |

贡献不是“提出一个新 assistant”，而是：从 3,176 条 screened records 中系统映射 58 个 research proposals；从 Gartner Magic Quadrant 2023 中 review 17 个 enterprise low-code tools 并抽取 15 个 practice proposals；形成 strategy、goal、limitation、metric、target user clusters；比较 literature 与 practice；指出 limitations / metrics / target users 报告不足，并提出 future unified framework / public repository 的研究议程。

### 2.2 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法不是一个普通 narrative survey，而是 systematic mapping + practice documentation review 的混合结构。

文献侧流程：

1. 基于 Petersen et al. systematic mapping guidelines 组织研究设计。
2. 用 PICO 定义 population 与 intervention；population 包括 MDSE、MDE、MDD、MDA、MBSE、low-code、no-code，intervention 包括 assist/support/help/ease/facilitate/user/developer/tester/architect/assistant 等。
3. 在 IEEE Xplore、ACM Digital Library、Scopus、Springer Link、Web of Science 上检索，时间范围 1985--2024。
4. 使用 inclusion/exclusion criteria：只纳入“专门提出一个 proposal 来辅助 MDSE tools 用户完成 modelling tasks”的同行评审英文全文；排除非 SE、非 modelling assistance 主贡献、全文不可得等。
5. 用 Table 1 的 3-point Likert 质量评价表进行 subjective + objective assessment；subjective 包括 proposal 是否清晰、limitations/goals 是否清晰、tools/sources 是否可下载、case study、empirical evaluation、users、results 等；objective 包括 venue ranking 和 citation count。
6. 从数据库初筛的 possible proposals 中取 quality top 12 作为 snowballing 初始集，执行 4 轮 backward / forward snowballing。
7. 最终 R1/R2 review 3,176 records，得到 77 possible proposals；R3/R4/R1 复核讨论后最终纳入 58 proposals。
8. inclusion reliability K-statistic = 0.634；clustering review 后 K-statistic = 0.651。
9. 原文声明 raw data、data extraction 与 triangulation 信息放在 Zenodo public repository。

数据抽取与编码方式：

| RQ | 原文抽取指令 | 编码 / 分类方式 |
|---|---|---|
| RQ1 | 抽取作者用于描述 proposal strategy 的 keywords。 | 六类 strategy clusters：Tools、Guidelines、Techniques、Methods、Frameworks、Languages；单 proposal 单标签，承认 overlap 风险。 |
| RQ2 | 抽取作者声明的 goals 与 limitations；未声明则留空。 | goals：G1--G7；limitations：L1--L6 与 L-NS。注意正文称 five limitation clusters，但 Table 3 与正文后续实际列出六类 limitation。 |
| RQ3 | 抽取 empirical evaluation metrics 与 target users；未说明则留空；generic “user” 归为 user-not-specified。 | metrics：M1 effectiveness、M2 efficiency、M3 user perception、NE；users：U1 designers/modellers、U2 domain experts、U3 软件开发者、U-NS。 |
| RQ4 | 从 GMQ tools 的 documentation / websites / user guides 中抽取 quote。 | Table 5 把每条 quote 映射到 S/G/L/M/U，同步记录 GMQ class 与 not assistant found。 |

统计与 finding 形成方式：

- 原文先做单轴分布：strategy distribution、goal distribution、limitation distribution、metric distribution、user distribution、documentation found / not found。
- 再做关系型统计：goal-limitation bubble chart、goal-metric-user bubble chart、strategy-goal-limitation bubble chart、literature-vs-practice distribution。
- finding 不是直接来自一个字段，而是由“字段分布 + 关系图 + missingness + discussion”生成：例如 tools 占主导、software-based assistance 占主导、limitations/metrics/users 缺失阻碍比较、practice 文档不足、AI/LLM 可能推动新 assistant framework。
- future work / roadmap 只是一种 design implication：统一框架、公共仓库、Fig. 14 repository visualisation、Fig. 15 research agenda。不能把这些写成已完成 empirical finding。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式结构远大于当前 `review.md` 维度树中的 5 个原文候选叶子。

| 原文结构 | 具体内容 | 证据定位 |
|---|---|---|
| RQ schema | MRQ + RQ1/RQ2/RQ3 + RQ4。 | `paper_content.txt` 行 74--87、211--246、902--906。 |
| Search / selection protocol | databases、PICO、search string、time range、I/E、snowballing、screened / included counts。 | 行 206--208、340--354、417--426。 |
| Quality rubric | Table 1：10 个 3-point Likert 质量评价问题。 | 行 340--374；PDF 第 4 页核对。 |
| Extraction form | RQ1 抽 strategy keywords；RQ2 抽 goals / limitations；RQ3 抽 empirical evaluation / metrics / target users；blank / generic user 有语义。 | 行 355--399。 |
| Strategy taxonomy | Tools、Guidelines、Techniques、Methods、Frameworks、Languages，含定义、关键词、Fig. 4 分布。 | 行 455--559；PDF 第 6 页核对 Table 2 / Fig. 4。 |
| Goal / limitation coding scheme | G1--G7，L1--L6，L-NS，Fig. 5 goal-limitation relation。 | 行 568--763；PDF 第 8 页核对。 |
| Metric / user coding scheme | M1--M3、NE、U1--U3、U-NS，Fig. 6。 | 行 764--824；PDF 第 8 页核对 Table 4。 |
| Practice evidence table | GMQ 17 tools，Table 5 quote-to-code S/G/L/M/U，not assistant found。 | 行 902--1118；PDF 第 11 页核对 Table 5。 |
| Literature-vs-practice comparison | Fig. 11--13；practice 与 literature 在 goals、limitations、metrics、users 上比较。 | 行 1144--1218；PDF 第 14 页核对 Fig. 13。 |
| Validity rubric | internal / construct / external validity；selection, extraction, subjective interpretation, inter-rater, grey literature, search, language bias。 | 行 1221--1334。 |
| Artifact / reproducibility | Zenodo raw data / protocol / bubble charts / data availability。 | 行 253--255、448--450、1210--1216、1463--1465。 |
| Roadmap / future model | Unified framework、public repository、Fig. 14、Fig. 15 research agenda。 | 行 1360--1445；PDF 第 17 页核对 Fig. 15。 |

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding path 可复原为：

```text
RQ / scope
  -> 文献 proposals 和 practice tools 的筛选分母
  -> extraction form: strategy / goal / limitation / metric / user / quote
  -> coding clusters: S, G, L, M, U, NE, NS, NF
  -> 单轴分布 + 交叉分布 + literature-vs-practice 对比
  -> missingness / imbalance / scarcity 观察
  -> discussion: gaps, framework need, repository idea, research agenda
```

关键是 missingness 具有研究意义：limitations 未报告、metrics 未评价、target user 未具体化、practice documentation not found 都不是空单元格，而是支持 gap / recommendation 的证据。该路径对 Paper2 的重要启发是：统计观察不能直接升级为 final finding；必须保留分母、字段版本、支持证据、反证 / 限制、claim strength 和研究者裁决。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但单位对象不完整。 | 根节点抓住了 MDSE modelling assistants landscape，但当前写“primary study / secondary study”，没有显式拆出 literature proposal、screened record、GMQ tool、practice proposal、documentation quote 这些原文单位。原文 MRQ 明确覆盖 literature + practice，实践侧是 17 tools / 15 proposals / documentation quote。 | I |
| 主干分支是否覆盖原文 schema | 未充分覆盖。 | 当前主干是通用 A1 接口：范围、语料、主题、方法、评价/发现。它没有以 RQ1--RQ4 或 literature/practice 双轨为主干，也没有单独保留 quality assessment、extraction form、practice documentation、validity、artifact/repository、roadmap。 | I |
| 叶子维度是否足够具体 | 不足。 | 当前新增了“原文模式候选叶子映射”，这是避免误读的正确方向；但只有 assistant strategy、goal、modeling artifact、metric-user、limitation 五个候选叶子，显著小于原文 schema。缺少 RQ4 practice、quality rubric、data extraction literal text、coding / triangulation、missingness、validity、artifact / Zenodo、roadmap / repository、comparison axes。 | I |
| 取值空间是否可执行 | 局部不可执行。 | strategy 候选取值写成“推荐、生成、补全、检测、修复、可视化、解释”等行为类别，而原文封闭 strategy clusters 是 Tools / Guidelines / Techniques / Methods / Frameworks / Languages。metric 与 user 被合并，缺少 M1--M3 / NE 与 U1--U3 / U-NS 的独立取值空间。goal / limitation 也应保留 G1--G7、L1--L6、L-NS。 | I |
| 关系边是否缺失 | 明显缺失。 | 当前只有 method-evidence 与 taxonomy-finding 两条边。原文至少还有 strategy-goal-limitation、goal-metric-user、literature-vs-practice、quality assessment -> snowballing seed、quote -> S/G/L/M/U code、terminology -> cluster decision、missingness -> gap、artifact / repository -> reproducibility 等关系。 | I |
| 统计用途 / 分母是否正确 | 分母过粗。 | 当前写“本文纳入样本或分类表”“当前 19 篇 survey-of-surveys 样本”等，未把原文分母拆开。原文分母包括 3,176 screened records、77 possible proposals、58 included proposals、top 12 quality seed、17 GMQ tools、7 documented tools、15 practice proposals；metrics / limitation / practice 图表还存在字段级 observation 分母，不能统一成 58 或 19。 | I |
| 候选 finding 路径是否完整 | 不完整。 | `review.md` 正文前半部分描述了 missingness -> gap -> framework need，但“维度树复原”中没有把 missingness、comparison axis、future-framework status 和 candidate finding ledger 独立建模。特别是 Fig. 14 / Fig. 15 只能作 roadmap / design implication，不应与完成型 finding 混写。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，但证据粒度不足。 | A.1--A.4 表头完整，且证据强度统一降为 `not_verified`，避免了错误升级；但 A.2 只有 5 条泛证据，多数写“邻近段落 / 见释义 / 待 A2a”，没有具体行号、页码、表号、图号，也没有覆盖 Table 1、Table 5、Fig. 13、Fig. 15、Zenodo、validity 等关键节点。 | I |
| 是否存在可能误导 A2a 的强主张 | 有轻度风险，但未达到 C。 | 当前已经明确“六个 leaf 是跨论文通用接口，不是原文全集”，且所有原文候选叶子均标 `schema_seed` / `not_verified`，没有把弱证据升级成 statistical synthesis。但 C12 写“已把原文抽取字段、分类项、模型节点或报告叶子列为候选”容易让 A2a 以为 5 个 broad leaf 已覆盖原文候选入口；应改成“仅列出部分高层候选”。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足以视为“原文 schema 完整复原”。建议把通用六叶保留为跨论文接口，但在其下新增一个忠实于原文的“原文 schema 子树”。最小修复骨架如下。

| 叶子标识建议 | 父节点 | 叶子维度 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| `leaf-mdse-orig-rq` | root / RQ branch | 原文研究问题 | MRQ、RQ1、RQ2、RQ3、RQ4 | 否，用作 schema 驱动 | `not_applicable` | 摘要与 §3.1，`paper_content.txt` 行 74--87、211--246、902--906 |
| `leaf-mdse-orig-unit` | scope branch | 分析单位 | screened record、possible proposal、included proposal、quality seed、GMQ tool、documented tool、practice proposal、documentation quote | 是 | `not_reported` / `not_applicable` | §3--§5，行 417--426、902--1118 |
| `leaf-mdse-orig-search-protocol` | corpus branch | 检索协议 | database search、snowballing、PICO terms、time range、search string | 是，支撑分母链 | `not_reported` | §3.2，行 206--208、340--354 |
| `leaf-mdse-orig-ie-criteria` | corpus branch | 纳排标准 | I1、I2、E1--E5 | 是，支撑 eligibility | `not_reported` | §3.3，PDF 第 4 页 / `paper_content.txt` Page 4 |
| `leaf-mdse-orig-quality-rubric` | evidence branch | 质量评价表 | Q1--Q8 subjective；Q9 venue；Q10 citation；取值 1 / 0 / -1 | 是，且影响 top-12 seed | `not_assessed` | Table 1，行 340--374，PDF 第 4 页 |
| `leaf-mdse-orig-reviewer-agreement` | evidence branch | 复核与一致性 | R1/R2/R3/R4；K=0.634 inclusion；K=0.651 clustering | 是 | `not_measured` | §4.1，行 417--440 |
| `leaf-mdse-orig-extraction-form` | evidence branch | 数据抽取表 | RQ1 strategy keywords；RQ2 goals / limitations；RQ3 metrics / users；literal fragments | 是 | blank = author not report；generic user = U-NS | §3.5，行 355--399 |
| `leaf-mdse-orig-strategy` | taxonomy branch / RQ1 | 建模辅助策略 | Tools、Guidelines、Techniques、Methods、Frameworks、Languages；单标签，overlap caveat | 是，分母 58 proposals | `not_classified` | Table 2 / Fig. 4，行 455--559，PDF 第 6 页 |
| `leaf-mdse-orig-goal` | taxonomy branch / RQ2 | 建模辅助目标 | G1 change propagation、G2 consistency checking、G3 compatibility、G4 quality、G5 interaction、G6 evolution、G7 vulnerability detection | 是，分母 58 proposals | `goal_not_specified` 如原文留空时记录 | Table 3，行 568--686 |
| `leaf-mdse-orig-limitation` | taxonomy branch / RQ2 | 限制类别 | L1 accuracy、L2 effort、L3 generality、L4 learnability、L5 scope、L6 usability、L-NS | 是，分母 58 proposals；注意正文 five vs table six 的口径风险 | `L-NS` | Table 3 / Fig. 5，行 687--763，PDF 第 8 页 |
| `leaf-mdse-orig-metric` | taxonomy branch / RQ3 | 评价指标 | M1 effectiveness、M2 efficiency、M3 user perception、NE | 是；分母按 metric observation / proposal 区分 | `NE` / `not_reported` | Table 4 / Fig. 6，行 764--824，PDF 第 8 页 |
| `leaf-mdse-orig-user` | taxonomy branch / RQ3 | 目标用户 | U1 designers/modellers、U2 domain experts、U3 软件开发者、U-NS | 是，分母 58 proposals | `U-NS` / generic user | Table 4 / Fig. 6，行 784--824 |
| `leaf-mdse-orig-practice-tool` | practice branch / RQ4 | GMQ 工具与市场类别 | LE、C、V、NP；17 tools；tool name | 是，分母 17 tools | `not_in_GMQ_scope` | §5.1，行 1052--1080 |
| `leaf-mdse-orig-practice-doc-status` | practice branch / RQ4 | 文档可见性 | documentation found、not assistant found、NF、access / public-doc status | 是，分母 17 tools | `NF` means not found in public documentation, not absence of capability | Fig. 9 / §5.2，行 1094--1115 |
| `leaf-mdse-orig-practice-quote-code` | practice branch / RQ4 | vendor quote 编码 | S:Tool、G1--G7、L1/L3/L5、M1/M2、U3 等 | 是，分母 15 practice proposals 或 coded observations | `not_mentioned` / second-person-hidden | Table 5，行 921--1045，PDF 第 11 页 |
| `leaf-mdse-orig-comparison-axis` | relation branch | 交叉统计轴 | strategy-goal-limitation；goal-metric-user；literature-vs-practice | 是，分母随图表变化 | `not_enough_data` / removed due scarcity | Fig. 11--13，行 1144--1218，PDF 第 14 页 |
| `leaf-mdse-orig-missingness` | finding branch | 缺失值证据 | L-NS、NE、U-NS、NF、not documented、second-person-hidden | 是，是 finding path 的核心输入 | 区分缺失文档、未报告、未评价、泛称 user | §4.3--§6，行 757--762、819--823、1108--1118、1197--1208 |
| `leaf-mdse-orig-validity` | validity branch | 威胁与限制 | internal: selection / extraction / subjective / inter-rater；construct: grey literature / search；external: language | 否或作为方法学统计字段 | `not_reported` | §7.1--§7.3，行 1221--1334 |
| `leaf-mdse-orig-artifact` | evidence branch | 复现与数据资产 | Zenodo protocol / raw data / bubble charts；data availability | 布尔 / 链接状态；需外部核验后统计 | `link_not_checked` / `not_available` | 行 253--255、448--450、1210--1216、1463--1465 |
| `leaf-mdse-orig-roadmap` | finding branch | roadmap / future work | unified framework、public repository、Fig. 14 visualisation、Fig. 15 research agenda | 不进 empirical finding；仅 candidate / boundary | `proposal_only` | §8，行 1360--1445，PDF 第 17 页 |

建议关系边至少包括：

| 关系边 | 源节点 | 目标节点 | 用途 |
|---|---|---|---|
| `edge-mdse-quality-to-snowballing` | quality rubric | top 12 snowballing seed | 说明 quality 不是普通描述字段，而影响语料扩展。 |
| `edge-mdse-extraction-to-cluster` | literal text fragment | S/G/L/M/U clusters | 支撑 quote / source anchor 到 coding 的证据链。 |
| `edge-mdse-strategy-goal-limitation` | strategy | goal / limitation | 复原 Fig. 11 与 Fig. 5 的交叉统计。 |
| `edge-mdse-goal-metric-user` | goal | metric / user | 复原 Fig. 12 / Fig. 6 的评价与用户关系。 |
| `edge-mdse-practice-to-literature` | practice quote codes | literature clusters | 复原 Fig. 13 literature-vs-practice comparison。 |
| `edge-mdse-missingness-to-gap` | L-NS / NE / U-NS / NF | gap / recommendation | 防止缺失值被当作空白而非 evidence。 |
| `edge-mdse-roadmap-status` | roadmap / public repository proposal | candidate finding | 防止 roadmap / future work 被写成完成型统计 finding。 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 扩展“原文模式候选叶子映射” | `review.md` 的 `## 维度树复原` / “原文模式候选叶子映射（A1 种子）” | 将 5 个 broad leaf 扩展为至少 RQ、unit、search protocol、I/E、quality rubric、extraction form、strategy、goal、limitation、metric、user、practice tool/doc/quote、comparison axis、missingness、validity、artifact、roadmap。 | 原文 Table 1--5、Fig. 11--15、§3--§8；本报告 §4。 | I |
| 修正 strategy 取值空间 | 同上 | 把“推荐、生成、补全、检测、修复、可视化、解释”等行为取值降为子关键词或迁移解释；原文 strategy 封闭枚举应为 Tools / Guidelines / Techniques / Methods / Frameworks / Languages，并保留单标签 + overlap caveat。 | `paper_content.txt` 行 455--559；PDF 第 6 页。 | I |
| 拆分 metric 与 user | “原文模式候选叶子映射”与叶子表 | 不应把 metric/user 合并为一个叶子；新增 metric leaf: M1/M2/M3/NE；user leaf: U1/U2/U3/U-NS，并写出 generic user / he/she 的 U-NS 判定。 | 行 764--824；PDF 第 8 页。 | I |
| 新增 RQ4 practice 子树 | 维度树结构与候选叶子表 | 新增 GMQ tool classification、documentation found / NF、practice proposal、documentation quote、S/G/L/M/U quote-code、second-person-hidden target user 等叶子。 | 行 902--1118；PDF 第 11 页。 | I |
| 新增 quality / reviewer agreement / extraction form | 维度树结构、候选叶子表、A.2 | Table 1 是 quality rubric，且 top 12 quality seed 影响 snowballing；K-statistic 和 R1--R4 流程是质量 / validity 证据；RQ-specific extraction form 是 coding scheme 的源头。 | 行 340--399、417--440；PDF 第 4 页。 | I |
| 新增统计分母语义 | “统计与候选发现链路” | 分别记录 screened records=3,176、possible proposals=77、included proposals=58、GMQ tools=17、documented tools=7、practice proposals=15、field observation denominators；不要用“本文纳入样本或分类表”概括全部分母。 | 行 417--426、902--1118、1144--1218。 | I |
| 新增 comparison / relation edges | “关系边表” | 补 strategy-goal-limitation、goal-metric-user、literature-vs-practice、quote-to-code、missingness-to-gap、roadmap-status 等关系边。 | Fig. 5、Fig. 11--13；行 802--812、1144--1218。 | I |
| 新增 validity 与 residual risk leaf | 候选叶子表、A.2、A.3 | 将 selection / extraction / subjective interpretation / inter-rater / grey literature / search / language bias 复原为单独叶子或 validity 子树，并记录 mitigation 与 residual limitation。 | 行 1221--1334。 | I |
| 新增 artifact / repository leaf | 候选叶子表、A.1 / A.2 | Zenodo public repository、raw data、bubble charts、data availability 应作为 artifact / reproducibility 字段；当前只在正文待复核里出现，维度树事实源缺失。 | 行 253--255、448--450、1210--1216、1463--1465。 | I |
| 明确 roadmap / future work 降级 | 候选发现链路、A.3 | Fig. 14 / Fig. 15、unified framework、public repository 是 future work / design implication，只能作为 candidate_finding / boundary_anchor，不得进入 empirical statistical finding。 | 行 1360--1445；PDF 第 17 页。 | M |
| 修正候选叶子父节点 | “原文模式候选叶子映射” | 当前 strategy 挂在 b1 scope、goal 挂在 b2 corpus、metric-user 挂在 b4 method，不符合原文 RQ 对应关系。建议按 RQ1/RQ2/RQ3/RQ4 或 taxonomy/practice/evidence 分支重挂。 | 当前 `review.md` 行 443--447；原文 RQ1--RQ4。 | I |
| 强化 A.2 证据账本定位 | A.2 / A.3 / A.4 | 将泛化“邻近段落 / 见释义”补为页码、表号、图号、`paper_content.txt` 行号和短引；保持 `not_verified` 直到 PDF / Zenodo 精核完成。 | GUIDE §6.3.6--6.3.7；本报告 PDF 抽查。 | I |
| 改弱 C12 表述 | A.3 C12 与维度树说明 | 将“本文已把原文抽取字段、分类项、模型节点或报告叶子列为……”改为“本文仅列出部分高层候选入口，尚未完成原文 schema 全量候选叶子复原”。 | 当前 `review.md` C12；本审计发现候选叶子过小。 | M |

## 6. C/I/M 结论

- C：无。当前 `review.md` 已明确六个通用 `leaf-*` 不是原文 schema 全集，并把新增原文候选叶子降级为 `schema_seed` / `not_verified`；没有发现把 roadmap / proposal 写成完成型统计 finding，或把弱证据直接升级成 `statistical_synthesis` 的 C 级问题。
- I：有。核心 I 级问题是“维度树复原”仍过小，且当前“原文模式候选叶子映射”没有充分复原原文 RQ1--RQ4、extraction form、classification schema、quality rubric、practice quote table、validity、artifact / repository、roadmap 和 field-to-finding path。这会实质影响 Paper2 A2a/A2b 的 schema seed 可用性：后续如果按当前候选叶子精核，会漏掉原文最有价值的 missingness、quality、practice evidence、comparison relation 和 claim-strength 降级字段。
- M：有。当前 C12 和一句话结论中的表述可进一步降级，避免 A2a 误以为 5 个 broad original leaves 已覆盖原文候选入口；roadmap / unified framework 也应继续写成 future / candidate，不写成 empirical result。
- 最终建议：NEEDS FIX。
