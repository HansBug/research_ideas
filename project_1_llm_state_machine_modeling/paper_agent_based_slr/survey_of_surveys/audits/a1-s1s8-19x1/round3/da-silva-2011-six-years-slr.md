# da-silva-2011-six-years-slr：A1 survey-of-surveys S1--S8 单篇维度抽取审计（round3）

## 0. 审计边界与阅读状态

- 角色：A1 `survey_of_surveys` 单篇维度抽取 subagent；本轮只处理 `papers/da-silva-2011-six-years-slr`，未开启 sub-subagent。
- 已先读并遵循：`ai-research-writing-skill` 的 claim-evidence-engineering 要求、`research-planning` 的明确风险/依赖要求、以及本目录 [GUIDE.md](../../../GUIDE.md) §6.3/§6.4。
- 已读取本地材料：
  - `bibtex.bib`：确认题名、IST 53(9):899--913、2011、DOI `10.1016/j.infsof.2011.04.004`。
  - `paper_content.txt`：已按页序通读 1--1625 行，覆盖摘要、Previous studies、Method、RQ1--RQ5、DCP、search/selection、QA rubric、data extraction、Table 2/3/5/6/7/8/9/10/11/12/13、Limitations、Conclusions、Appendix A。
  - `review.md`：已通读现有卡片、A1-M0--M6、维度树复原、叶子表、关系边表、S1--S8 表与四分栏。
  - `evidence_chain.md`：已通读 A.1--A.4；当前证据链多为树级 `not_verified` / A2a 待页码表图精核。
- 未核对 `paper.pdf` 版面：本轮文本抽取足以复原 S1--S8 与维度森林；表图页码、OCR 换行、Table 6/8 分母等仍必须留给 A2a。以下所有判断均为 **A1 文本级审计**，不得写成 final quantitative finding。

## 1. 总体裁决

本文是一篇更新型三级研究（updated tertiary study）：作者把 2008-07-01 至 2009-12-31 新增的 SE 二级研究，与 OS/FE 两个前序 tertiary study 合并比较，形成 2004-01-01 至 2009-12-31 的纵向观察。主样本单位是已发表二级研究（原文广义称 SLR，内部又分 conventional SLR / mapping study / meta-analysis），本轮新增 SE 样本最终为 67，整合 OS/FE 后为 120 个 secondary studies。

统计池资格：**后续主统计池候选，A2a 前不得进入最终定量统计**。理由是原文有系统检索、纳排、DCP、QA、抽取字段、样本级表格和统计分析；但本地证据链仍未完成 PDF 页码、表图、分母链和表格视觉精核。

## 2. S1--S8 审计表

| 维度 | 等级 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 强 | 摘要说明目标是扩展并更新两项前序 tertiary studies，覆盖 2008-07-01--2009-12-31；§1 明确本文是 review of secondary studies；§3.1 列 RQ1--RQ5（数量、主题、作者/机构、既有限制、质量提升）。证据：`paper_content.txt` L15--24、L114--120、L217--248。 | 根对象为“更新型三级研究任务”；RQ 是统计聚合视角，服务 OS/FE + SE 比较。 | 支持主统计池候选的任务边界；不构成领域最终发现。 | 精核摘要、§1、§3.1 页码与 OS/FE/SE 定义。 |
| S2 语料收集与筛选 | 强 | §3.4 定义 6 个自动数据库、完整检索式、OS/FE 回测；手工搜索 13 个源；§3.5 给出 154 unique papers 全文筛选、参考文献回溯、77 进入 QA/data extraction、最终排除 10 得 67。Fig.2 给出 1389→157→154→75→77→67。证据：L281--332、L333--386、L523--572、L469--476。 | 语料树：自动检索 / 手工检索 / 去重 / 全文纳排 / 回溯 / QA+抽取 / 最终 SE set / integrated OS-FE-SE set。 | 强支持候选统计池；分母链待 A2a 前不可直接用于 final quantitative。 | 核 Fig.2、Table 1、Appendix A；核 1455 articles、1389、157、154、75、77、67、120 是否同口径。 |
| S3 原生维度树 / 样本编码对象 | 强 | §3.7 明示抽取字段；Table 2 按 SE ID 展示 67 行；§3.6 QA1--QA4；Table 5 映射 curriculum/SWEBOK；§7 给 update 类型。证据：L448--468、L575--585、L903--910、L1343--1356。 | 原生结构应复原为维度森林：抽取表树、QA 量规树、主题/课程/SWEBOK 树、作者/机构/国家关系图、前序更新关系树、教育/实践相关性树。 | 支持候选统计池的编码对象定义；具体叶子进入统计前需逐表核。 | 核 Table 2/3/5/6/7/8 与 Appendix A；核 SE01--SE77 中缺号、排除项、短文注脚。 |
| S4 字段级证据 | 强 | §3.6 给 QA1--QA4、Y/P/N 与 1/0.5/0；§3.7 给 Year、Quality Score、Review Type、Review Scope、Topic Area、Cited EBSE/Guidelines、#Primary Studies、Practitioner Guidelines、Source Type；Table 2/3/5 实例化样本级字段。证据：L392--439、L448--476、L575--894、L903--1138。 | 字段级证据足以支撑核心叶子；EBSE/Guideline 不是普通布尔，而是带文献子引用的多值关系字段。 | 文本级字段池强；最终字段统计需 A2a 视觉核验。 | 核表格列名、注脚 a--i、OCR 粘连、SE ID 与行数。 |
| S5 维度模式演化 | 中 | 原文说明沿用 FE protocol、独立执行以避免 bias；RQ4 有改写；QA2 评分标准有修改并为保持 OS/FE 可比保留旧 DARE 四题；§7 提出 temporal update / search extension / both。证据：L199--216、L242--248、L400--438、L1343--1356。 | 可复原“前序综述关系 / 更新类型 / protocol 继承与局部修订”子树；但没有完整 codebook 版本演化、开放编码过程或冲突修订日志。 | 只作模式演化候选，不应按强证据进入统计。 | 核 QA2 修改的粗体原文、§6 咨询 OS/FE 作者、§7 三类 update 精确措辞。 |
| S6 统计分析 | 强（文本级） | 原文从字段转化为频次、比例、趋势、回归和相关：Table 4 年度增长与 EBSE positioned；Table 6 curriculum/SWEBOK 分布；Table 10/11 practitioner guideline 与 primary-study QA；Table 13 quality trend；§5.5 回归与 Pearson。证据：L502--512、L671--678、L807--816、L1141--1218、L1291--1322。 | 字段→统计路径清楚：年份/类型/范围/主题/QA/指南/来源类型/primary count → 频次、比例、均值、回归、相关。 | 主统计池候选强；A2a 前只可称“文本级可统计”，不得沉淀为最终跨论文定量结论。 | 核 Table 4/6/10/11/12/13 的列对齐、N、百分比、p 值、回归系数。 |
| S7 候选 finding | 强（文本级候选） | 结论与 discussion 把统计观察形成候选 finding：SLR 数量与主题覆盖增长；研究者/组织扩散；MS 比例变化；primary QA 仍不足；meta-synthesis 少；实践者指南仍少；120 篇中未发现 update/extension；报告不一致导致抽取困难。证据：L1261--1289、L1329--1363、L1364--1388。 | 可复原“统计观察 → gap/limitation/recommendation/future work”的 finding 路径；其中领域结论严格限定在 2004--2009 SE SLR 生态。 | 可作 finding 形成机制与候选 finding 模式；不得写成 Paper2 目标领域 final finding。 | 核每条 finding 与 Table/§5 的支撑关系；区分数据支撑结论与作者解释/建议。 |
| S8 研究者 / 作者质疑与裁决 | 强 | §3.3 定义 DCP：双人独立评估、ADT、不一致由第三研究者裁决或全员共识；QA 使用 DCP 并用 10 篇 blind reassessment 校准；§6 说明 QA4 主观、QA2 不一致、数据抽取可能受报告不足影响。证据：L257--280、L438--447、L1226--1259。 | 可复原 human-in-the-loop 裁决树：selection / QA / data extraction 三类决策，研究者角色 R1--R6，第三方裁决，全员共识，限制/质疑。 | 支持方法学模式入库；不直接增加统计分母。 | 核 Fig.1 DCP 版面、§3.3、§3.6、§6 的角色与流程细节。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 森林总览

本文不应被压成通用六叶模板。它的原生结构是围绕 secondary studies 样本的多根维度森林：

```text
森林根：软件工程二级研究样本（secondary studies；SE 新增 67；OS/FE+SE 整合 120）
├─ T1 抽取表树（原文明示：§3.7 + Table 2）
├─ T2 质量评价树（原文明示：§3.6 + Table 3）
├─ T3 主题外部映射树（原文明示：Table 5/6；本地复原为三层分类树）
├─ T4 作者-机构-国家关系图（原文明示：§5.3 + Table 7/8；本地复原为关系图）
├─ T5 前序综述与更新类型树（原文明示：§2/§7；本地复原为 predecessor/update 关系树）
└─ T6 教育与实践相关性树（原文明示：Table 5；本地复原为 relevance 子树）
```

### 3.2 树干、叶子与取值空间

| 子树 | 原文 / 本地属性 | 叶子或节点 | 取值空间 | 说明 |
|---|---|---|---|---|
| T1 抽取表树 | 原文明示 | Year | 2004--2009 | 纵向统计；SE 窗口与 OS/FE 窗口需分开。 |
| T1 抽取表树 | 原文明示 | Quality Score | 0--4，步长 0.5 | 来自 QA1--QA4 求和。 |
| T1 抽取表树 | 原文明示 | Review Type | SLR / MA / MS | conventional SLR、meta-analysis、mapping study。 |
| T1 抽取表树 | 原文明示 | Review Scope | RQ / SERT / RT | 技术问题、SE 主题趋势、研究方法。 |
| T1 抽取表树 | 原文明示 | Topic Area | 24 个 SE topics（SE 新增集合） | 部分开放标签；后续映射到 curriculum/SWEBOK。 |
| T1 抽取表树 | 原文明示但本地需关系化 | Cited EBSE papers | N 或 Y + 引用 [14]/[8]/[20]/[24] 等 | 不是单纯布尔；存在多文献子引用。 |
| T1 抽取表树 | 原文明示但本地需关系化 | Cited Guidelines | N 或 Y + 指南 [15]/[16]/[13]/[4]/[12] 等 | 不是单纯布尔；用于质量相关分析。 |
| T1 抽取表树 | 原文明示 | Number of Primary Studies | 正整数 | 部分从表格/正文抽取。 |
| T1 抽取表树 | 原文明示 | Included Practitioner Guidelines | Y / N | 是否有可识别 section/table 等。 |
| T1 抽取表树 | 原文明示 | Source Type | J / C / WS / BS | 期刊、会议、工作坊、丛书。 |
| T2 质量评价树 | 原文明示 | QA1--QA4 | Y=1 / P=0.5 / N=0 | DARE 四题，QA2 有本研究修改。 |
| T2 质量评价树 | 原文明示 + 本地复原 | Final Score / Quartile | 0--4；1st--4th quartile | Table 3 结果；quartile 是展示/分析层。 |
| T3 主题外部映射树 | 原文明示 + 本地复原 | SE Curriculum section/subsection | SE2004 curriculum 章节/子节 | Table 5/6；外部分类体系版本需保留。 |
| T3 主题外部映射树 | 原文明示 + 本地复原 | SWEBOK chapter/section | SWEBOK 2004 章节/小节 | Table 5/6；后续不可直接与新版 SWEBOK 混算。 |
| T4 人员关系图 | 原文明示 + 本地复原 | Author / organisation / country / region | 人名实体、机构实体、国家/地区枚举 | 关系型节点，不宜压成普通叶子。 |
| T5 更新关系树 | 原文明示 + 本地复原 | Update type | temporal update / search extension / both / none | §7 明示前三类；“none”是对 120 studies 的缺失关系复原。 |
| T6 教育实践相关性树 | 原文明示 + 本地复原 | Useful for education / practitioner / why | Yes / No / Possibly + 自由文本原因 | Table 5；“why”是自由文本解释字段。 |

### 3.3 关系边

| 边 | 原文 / 本地属性 | 源节点 | 关系 | 目标节点 | 取值空间 / 缺失值 |
|---|---|---|---|---|---|
| E1 | 本地复原，原文表支撑 | secondary study | has_extraction_field | T1 叶子 | 字段值来自 Table 2；缺失需 A2a 核。 |
| E2 | 原文明示 | secondary study | assessed_by | QA1--QA4 | Y/P/N；final score 为求和。 |
| E3 | 原文明示 | secondary study | maps_to | SE Curriculum / SWEBOK | Table 5/6；N/A 或 academic-only 需单列。 |
| E4 | 本地复原，原文表支撑 | secondary study | authored_by | researcher | Table 7/Appendix A；作者名规范化待核。 |
| E5 | 本地复原，原文表支撑 | researcher/organisation | located_in | country/region | Table 8；country count 的 N=121 OCR/口径需核。 |
| E6 | 原文明示 + 本地关系化 | secondary study | cites | EBSE paper / SLR guideline | 多值引用；N 表示未引用相应集合。 |
| E7 | 原文明示 + 本地复原 | SE study / FE / OS | updates_or_extends | predecessor review | temporal / search extension / both。 |
| E8 | 原文明示 | secondary study | useful_for | education/practitioner | Yes / No / Possibly + why。 |
| E9 | 原文明示的缺失关系，本地入账 | 120 secondary studies | updates_or_extends_prior_slr | prior SLR | 0 例；这是缺失关系，不能当普通空值。 |

## 4. 统计池资格与 A2a 接力

- 可作为后续主统计池候选的原因：系统检索 + 纳排 + QA + data extraction + 明确 RQ + 样本级表格 + 统计分析完整。
- 当前不得进入 final quantitative finding 的原因：`evidence_chain.md` A.2 仍是粗粒度 `not_verified`，页码、表号、OCR 换行、Fig.2 分母链、Table 6/8 列对齐尚未精核。
- A2a 最小接力：核 `paper.pdf` 中 Fig.1、Fig.2、Table 1--13、Appendix A；把当前 `review.md` 的行号锚点迁入 `evidence_chain.md` A.2；对 67/77/120/121/1455 等数字建立口径说明。

## 5. 需要修改 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 问题清单

### C（critical）

- 暂未发现必须立即阻断的 C 级问题。当前文本总体没有把 A1 结果写成 Paper2 final quantitative finding；但下列 I 级问题若在后续写作中被误用，可能升级为 C。

### I（important）

1. **`review.md` §6.A 标题“high confidence，可入主统计池”容易被误读为已经可进入最终统计。**
   - 影响：违反 §6.3/§6.4 的 A1/A2a 边界，可能让 Table 4/6/10/11/13 数字在 A2a 前进入 SUMMARY 定量或论文 final finding。
   - 建议：改为“文本级统计观察（A2a 主统计池候选；精核前不可作最终定量）”。
2. **S7 等级口径与 rubric/既有裁决存在不一致风险。**
   - 当前 `review.md`/`SUMMARY.md` 将 S7 写为“中”，但原文 candidate findings 与字段/统计链关系清楚，按 S7 操作化可判为“强（文本级候选）”。
   - 建议二选一：要么升级为“强（文本级；A2a 前不得 final）”，要么保留“中”但明确降级原因只是表图未精核，而不是 finding 关系弱。
3. **`evidence_chain.md` A.2 仍过粗，缺少本轮可定位的行号/表号细化。**
   - 影响：A.3 结论虽能回链树级证据，但 A2a 前很难自动核每个 S 维度、叶子和关系边。
   - 建议：A2a 把本审计中的 L15--24、L217--248、L281--386、L392--476、L575--894、L903--1322、L1343--1388 等关键锚点拆成多条 A.2。

### M（minor）

1. **`review.md` 快速卡片“是否目标证据池：否；只作为脚手架模式先验”与 `metadata.json` / SUMMARY 的 `eligible_for_statistical_synthesis=true` 容易混淆。**建议改写为“不是目标领域证据池；是 A1 survey-of-surveys 后续主统计池候选”。
2. **Table 8 的国家/区域口径存在 `N=121` OCR/统计口径疑点。**不影响当前 S1--S8，但 A2a 引用地区统计前需核对是否因多国合作导致计数超过 120。
3. **SUMMARY 主表中“new SLRs in update window / 67”可进一步写成“新增 secondary studies（SLR/MS/MA，原文广义 SLR）/ 67”。**这样能避免把 mapping study 和 meta-analysis 误压成 conventional SLR。

## 6. 明确禁止事项

本审计只给出 A1 文本级 S1--S8 与维度森林复原。任何数字（如 67、77、120、1455、15/67、40/67、36%、51%、回归系数、Pearson 相关、质量均值）在 A2a 完成 PDF 表图和分母链精核前，都只能作为“文本级候选统计观察”或“schema/finding 形成模式”，**不得写成 final quantitative finding**。
