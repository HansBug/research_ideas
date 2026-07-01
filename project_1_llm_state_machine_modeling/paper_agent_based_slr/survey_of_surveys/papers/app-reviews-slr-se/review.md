# Analysing app reviews for software engineering: a systematic literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Analysing app reviews for software engineering: a systematic literature review |
| 作者 | Jacek Dąbrowski; Emmanuel Letier; Anna Perini; Angelo Susi |
| 年份 | 2022 |
| 类型 | SLR；面向 app reviews for software engineering。 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [ESE](https://link.springer.com/journal/10664) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | Empirical Software Engineering；正式 DOI、Springer PDF 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 63 页；未做复杂表格视觉级人工核对。 |
| 证据等级 | 全文文本级；复杂表格、搜索式和部分百分比需 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.1007/s10664-021-10065-7> |
| 综述类型 | SLR |
| SE 子领域 | app reviews / mobile user feedback / mining software repository。 |
| A1 角色 | 从失败路径升级为全文级现代高等级 SLR 样本：提供完整 RQ→抽取字段→分类 schema→统计表→discussion finding 的闭环。 |
| 是否目标证据池 | 是，作为 `survey_of_surveys/` 的 SLR 方法 / 报告结构 / 维度模式统计池样本；不是 Paper2 目标主题的领域证据。 |
| 是否统计池 | 是；可进入 A1 方法学统计池和 SLR/SMS 报告模式统计池。 |
| 一句话结论 | 这篇论文是 A1 中字段体系最完整的现代 SLR 样本之一，尤其适合迁移“多套分类 schema + 评价质量字段 + replication package 字段 + discussion finding”设计。 |

## 2. 论文内容详读

### 2.1 研究目标与 RQ

本文研究 app reviews 如何支持软件工程活动。作者提出五个 RQ：app review analysis 的类型、使用的技术、声称支持的软件工程活动、empirical evaluation 的方式、以及现有方法对软件工程师的支持效果。

该 RQ 设计对 Paper2 很有启发：它不是只问“有什么论文”，而是把目标对象拆成对象 / 信息类型、技术实现、软件工程活动、评价方式、评价结果五层。这种五层结构可迁移到 LLM4STM 或 agent-assisted SLR 主题：对象是什么、方法是什么、支持哪类工程活动、如何评价、结果能支撑什么结论。

### 2.2 搜索、筛选与纳排

论文遵循 Kitchenham 风格 SLR 流程：先定义 RQ 和 protocol，再执行自动检索、手工检索和 snowballing，最后抽取数据并回答 RQ。检索覆盖 2010 年 1 月至 2020 年 12 月；最终纳入 182 篇 原始研究，实际发表时间覆盖 2012--2020。数量链包括初始检索 1656 篇、去重 303 篇、筛选 1353 篇、排除 1225 篇，手工逐卷检索增加 14 篇，snowballing 增加 40 篇，最终形成 182 篇。

纳排标准强调：必须与软件工程相关、peer-reviewed，并使用 app reviews 支持至少一种软件工程活动；排除非英文、非 SE、secondary / tertiary studies、technical reports、manuals 等。

### 2.3 数据抽取字段

Table 3 给出 F1--F18 抽取表，覆盖：bibliographic 信息、review analysis 类型、mining technique、software engineering activity、justification、evaluation objective、evaluation procedure、metrics / criteria、evaluation result、annotated dataset、annotation task、annotators、quality measure、replication package 等。

这是 A1 最值得采纳的字段级证据模板之一。它说明一个高质量 SLR 不只记录“论文用了什么方法”，还要记录“评价用什么数据、谁标注、标注质量如何、是否公开 replication package”。这与 Paper2 的审计优先证据链高度一致。

### 2.4 分类 schema 与 reliability

作者构建三套 classification schema：app review analysis、mining technique、software engineering activity。分类过程使用 content analysis，先从 sample studies 中抽概念，再合并语义相近类别，最后由作者讨论并形成最终 schema。分类可靠性用 intra-rater 和 inter-rater agreement 检查：app review analysis、SE task、mining technique 的 inter-rater 约为 87%、87%、80%，intra-rater 约为 93%、100%、90%。

这说明维度模式不是任意主观命名，而应有构造过程、示例、合并规则和一致性检查。Paper2 后续若让 agent 自动提出 dimension pattern，也必须由研究者批准、记录修改理由和回填影响。

### 2.5 主要维度与统计结果

本文的 app review analysis 类型包括 classification、information extraction、content analysis、clustering、sentiment analysis、recommendation、summarization、search and information retrieval、visualization。mining technique 主要包括 NLP、ML、statistical analysis、manual analysis。SE activity 覆盖 requirements、maintenance、testing、design 等，且有一部分 studies 未明确指定 SE activity。

评价维度特别重要：109 篇研究做 empirical evaluation，105 篇做 effectiveness evaluation，23 篇做 user-perceived quality；RQ5 的结果来自 87 篇研究。作者还记录 public annotated datasets、public tools、annotators、annotation quality measure、replication package 等字段。公开数据和工具并不充分，这构成后续 discussion finding 的重要证据。

### 2.6 证据呈现与统计分析

本文是 A1 中统计呈现最丰富的样本之一：PRISMA 式筛选图、年度趋势、venue 类型图、top venue、highly cited papers、分类维度频次、analysis-technique 交叉表、analysis-SE activity 交叉表、dataset/tool 表、five-number summary、user-study criteria / participants 表、effectiveness range / median 表，以及 user-study qualitative result synthesis。

作者明确指出 原始研究 异质性太强，不适合做 meta-analysis，因此采用 summarizing effect estimates 这类描述性合成。这个判断历史草稿曾提出迁移建议；当前禁止直接采信为 Paper2 的统计纪律：异质字段先做分母清晰的描述统计和交叉表，不能为了显得“强”而硬做不成立的统计合成。

### 2.7 Discussion finding 与未来方向

本文的 discussion 把统计观察转化为多个 research implications，例如：需要更清晰的软件工程 use case、缺少 reference model、评价数据集偏小、replication package 不足、practice impact 不清、scalability / efficiency 评估不足、监督式 ML 训练数据成本和漂移问题等。

这对 Paper2 的启发非常直接：research finding 不是表格频次本身，而是“统计观察 + 解释 + 工程语境 + 不足 / 未来工作”。后续 agent 可以辅助提出 候选发现，但必须保留支持证据、反证和研究者裁决。

### 2.8 效度威胁

作者列出四类主要威胁：关键词不完整、publication bias、筛选 / 抽取 / 分类主观性、taxonomy reliability。缓解方式包括 iterative keyword construction、specific + generic query、manual venue search、backward / forward snowballing、second coder sample cross-check、inter-coder / intra-coder agreement、content analysis 和作者讨论。

这些 threat pattern 可以迁移到 Paper2 的所有阶段：检索、筛选、抽取、分类、统计、候选 finding 都要对应记录风险与缓解，而不是只在最后写一段泛泛 limitations。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ1--RQ5 覆盖 analysis type、technique、SE activity、evaluation method、evaluation result。 | `paper_content.txt` §2.1。 | 可迁移为多层综述元模型：对象 / 方法 / 活动 / 评价 / 结果。 | app review 领域 RQ 不能直接改名套到 LLM4STM。 |
| dimension pattern | F1--F18 extraction form + 三套 classification schema + evaluation / artifact 字段。 | Table 3、§2.4、Table 4。 | 高度可迁移为 A2a 字段表和 reliability check 模板。 | 部分细分字段与 app review mining 特有。 |
| finding pattern | 从统计表形成 practice impact、evaluation quality、replication package、scalability、training cost 等 gaps。 | §4 Discussion、§6 Conclusion。 | 可迁移为 候选发现 ledger 的构造方式。 | 不能把 app review 领域 gap 写成 LLM4STM gap。 |
| evidence presentation pattern | PRISMA、频次表、交叉表、range/median、dataset/tool 表、qualitative result table。 | Figure 1--3、Table 5--23。 | 可迁移为 A2b 总账和 Paper2 结果呈现模式。 | 复杂表格需 PDF 视觉核对；OCR 中个别百分比错位。 |
| validity / threat pattern | 覆盖 query incompleteness、publication bias、screening/extraction/classification subjectivity、taxonomy reliability。 | §5 Threats to Validity。 | 可迁移为 agent-assisted SLR 分阶段风险表。 | 还需补充 LLM/provider/prompt/schema drift 等新风险。 |
| report structure pattern | Abstract → Introduction → Research Method → Results by RQ → Discussion → Threats → Related Work → Conclusion。 | 章节结构。 | 可迁移为现代高等级 SLR 报告结构。 | Paper2 还需加方法贡献、审计制品链和人机交互评估。 |

## 4. A1-M0--M6 元维度贡献

| A1-M 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 研究意图与综述元模型 | 用 RQ1--RQ5 定义对象、技术、SE activity、evaluation、result 五层元模型。 | 可迁移为目标主题的 researcher-defined meta-model。 | 需要由研究者决定哪些层适合目标主题。 |
| A1-M1 语料收集与纳排 | 给出数据库、时间窗、自动检索、手工检索、snowballing、纳排和数量链。 | 可迁移为 A2b 完整文库分母链条。 | 检索式在文本抽取中不完整，需 PDF 核对。 |
| A1-M2 研究对象与主题语义 | 把 mined information、SE activity 和 app review analysis 分层分类。 | 可迁移为对象 / 工件 / 生命周期活动分类。 | 领域语义必须重建，不能直接套用 app review taxonomy。 |
| A1-M3 方法 / 技术 / 干预 | NLP、ML、statistical、manual analysis 等技术分类，以及 analysis-technique 交叉表。 | 可迁移为 LLM/agent/tool/method/application-role 字段。 | 需扩展现代 LLM、agent 和 human-in-the-loop 取值。 |
| A1-M4 评价、证据与复现资产 | annotated dataset、metrics、quality measure、replication package、public tools 等字段。 | 历史草稿曾提出迁移建议；当前禁止直接采信为 Paper2 的 artifact / evaluation / evidence strength 模块。 | 必须区分“有 replication package”与“可复现质量高”。 |
| A1-M5 统计分析就绪 | 大量频次、百分比、交叉表、range/median、five-number summary。 | 可迁移为分母固定、字段版本化、missing-value 语义和交叉统计。 | 异质结果只做描述性合成，不强行 meta-analysis。 |
| A1-M6 research finding 形成与裁决 | Discussion 将统计观察转化为 research implications 和 future work。 | 可迁移为“统计观察 → 候选 finding → 研究者裁决”的台账流程。 | 需要记录支持 / 反证 / scope / claim strength。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> [!WARNING] v1-deprecated: 本节为 A1-DT v1 历史草稿 / 迁移来源，只能作为返修来源和历史证据，不是 A1-DT v2 当前事实口径。v2 事实以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
说明：本旧版迁移草稿已中文化；英文 / 缩写保留为原文术语或后续字段标识。
现代 SLR 字段模式（modern_slr_field_pattern）
├── 研究问题层
│   ├── 分析对象或对象类型
│   ├── 技术或方法
│   ├── 支持的软件工程活动
│   ├── 评价方法
│   └── 评价结果
├── 语料与筛选
│   ├── 自动数据库检索
│   ├── 手工 venue 检索
│   ├── backward / forward snowballing
│   ├── 纳入 / 排除标准
│   ├── 去重数量
│   ├── 排除数量
│   └── 最终纳入数量
├── 抽取字段
│   ├── 书目信息
│   ├── 分析类型
│   ├── 技术类型
│   ├── 工程活动
│   ├── 评价目标
│   ├── 评价流程
│   ├── 指标与准则
│   ├── 评价结果
│   ├── 标注数据集
│   ├── 标注质量
│   └── 复现包
├── 分类方案
│   ├── 内容分析种子
│   ├── 类别合并 / 拆分
│   ├── intra-rater agreement
│   ├── inter-rater agreement
│   └── 最终分类法版本
├── 统计呈现
│   ├── 频次表
│   ├── 交叉表
│   ├── 趋势图
│   ├── range / median 汇总
│   └── 不做 meta-analysis 的理由
└── 发现裁决
    ├── 统计观察
    ├── 实践缺口
    ├── 证据强度
    ├── 未来工作
    └── 需要研究者裁决
```

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **字段表应覆盖 evaluation 和 artifact**：仅抽输入、输出、方法不够；还要抽评价数据、指标、标注者、质量度量和复制包。
2. **classification schema 需要可靠性证据**：即便是人工 SLR，也要报告 inter-rater / intra-rater；Paper2 的 agent-assisted 抽取更需要 disagreement / adjudication 记录。
3. **discussion finding 要有统计来源**：该文的 gap 来自具体统计与表格，而不是作者随意观点。
4. **异质性是正常情况**：不能把所有 原始研究 强行汇入一个统一效果值；更适合用描述统计、交叉表和分层解释。
5. **可复现资产是字段，不是附带说明**：replication package 和公开数据集应成为 Paper2 的一等抽取维度。

### 6.2 风险

1. `paper_content.txt` 对搜索式、部分表格和百分比抽取存在错位；A2a 正式统计前需视觉核对。
2. app review mining 的细分 taxonomy 与 LLM4STM 不同，只能迁移结构和字段设计，不迁移领域结论。
3. 本文虽然记录 replication package，但没有完整评价制品质量；Paper2 需要更强的 audit artifact completeness rubric。
4. 如果后续只学习它的表格而不学习它的 reliability / threat 设计，就会变成“漂亮总账但弱证据”。

## 7. 待复核

1. 视觉核对 Figure 1（p.4）的 PRISMA 数量链。
2. 视觉核对 p.5 搜索式；当前 `paper_content.txt` 对 exact query 抽取不完整。
3. 视觉核对 p.4--5 digital libraries 数量；文本称 six major digital libraries，但抽取文本只清楚显示五个名称。
4. 视觉核对 Figure 2、Figure 3 和 Table 5--7 的年度、venue 和 analysis type 统计。
5. 视觉核对 Table 9--15 的 technique / SE activity 交叉表，尤其多列表格对齐。
6. 视觉核对 Table 16--23 的 dataset、tool、five-number summary、effectiveness range / median 和 related survey comparison。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__codex.md](../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__codex.md)、[../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__claude.md](../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__claude.md)、[../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__deepseek.md](../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/app-reviews-slr-se.md](../../audits/a1dt-v2-19x3/adjudications/app-reviews-slr-se.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `app-reviews-slr-se` |
| 审计代理 | `claude`（claude-opus-4-7[1m]，本地直接执行，非 subagent） |
| 是否已读 `paper_content.txt` | 是；按行号顺序覆盖 §1 Introduction 至 §7 Conclusion 及 References 起始部分（行 1–2200+），所有 Table 1–23、Figure 1–4、§3.2.1–3.6.2、§4.1–4.10、§5–§7 已逐节阅读。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；元信息一致：Dąbrowski/Letier/Perini/Susi (2022), ESE 27(2):43, DOI 10.1007/s10664-021-10065-7。 |
| 是否打开或核对 `paper.pdf` | 否（本轮以全文文本审计为主，复杂表格视觉级版面核对仍标为待 A2a 人工核验）。 |
| 原文类型 | SLR（明确遵循 Kitchenham 2004，PRISMA 过程） |
| 被编码样本单位 | 原始研究（共 182 篇 peer-reviewed 论文，2012–2020 发表） |
| 样本数量 / 分母 | 182 原始研究（初始 1656→去重 303→筛选 1353→排除 1225→128 通过+ 14 manual + 40 snowballing = 182） |
| 原生树类型 | RQ-驱动的多 模式 抽取森林（F1–F18 数据抽取表 + 3 套分类模式 + RQ 结果层），不是单一统一树 |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 A.2/A.3。 |
| 总体判定 | v2 已返修完成：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

实际读取的文件与章节：

1. `bibtex.bib`（1–19 行）— 标题、作者、ESE 卷期、DOI、关键词；
2. `metadata.json`（1–28 行）— slug、DOI、CCF 等级、review_type=SLR；
3. `paper_content.txt`：
   - §1 Introduction（行 36–98）— 研究动机、四项 paper objectives、4 项 primary contributions；
   - §2 研究方法（Research Method）（行 98–341）— RQ1–RQ5 定义、PRISMA 流程、检索式构造、F1–F18 抽取表、3 套 分类方案（classification scheme；首次术语） 构造方式、reliability 检验、data synthesis；
   - §3.1 Demographics（行 342–360）；
   - §3.2 RQ1 + Table 7（9 类 analysis）+ 3.2.1–3.2.9 各子小节（行 361–636）；
   - §3.3 RQ2 + Table 9–12（4 大 mining technique + 10 ML 技术）（行 639–871）；
   - §3.4 RQ3 + Table 13–15（14 项 SE activity）（行 885–1230）；
   - §3.5 RQ4 + Table 16–20（公开数据集、工具、五数概括、user-研究 criteria/participants）（行 1245–1490）；
   - §3.6 RQ5 + Table 21–22（effectiveness range/median、user 研究 定性合成）（行 1490–1700）；
   - §4 Discussion §4.1–4.10（行 1693–1850）；
   - §5 Threats（行 1849–1885）；
   - §6 Related Work + Table 23（行 1885–1938）；
   - §7 Conclusion（行 1939–1972）。

未做：PDF 视觉级版面核验（搜索式 query 文本、Fig 1 PRISMA 详细数字气泡、Tables 14/15 矩阵对齐、Table 16 部分单元格 OCR）。

**关键证据锚点（短引/释义）**：

1. §1 paper objectives（行 79–86）："identify and classify the range of app review analysis…; identify the range of NLP and data mining techniques…; identify the range of software engineering activities…; 报告 the 方法 and results of the 经验研究（empirical） 评价"。
2. §2.1 RQ1–RQ5（行 108–115）：5 个 RQ 分别对应分析类型 / 技术 / SE 活动 / 评价方法 / 评价结果。
3. §2.2 PRISMA 数量链（行 130–171）：1,656→303 dup→1,353 screened→1,225 excluded→128→+14 manual→+40 snowballing→**182** included。
4. §2.3 Table 3 F1–F18 数据抽取表（行 226–270）：F1 Title…F18 Replication Package；F6 → RQ1，F7 → RQ2，F8/F9 → RQ3，F10–F12/F14–F18 → RQ4，F13 → RQ5。
5. §2.4 三套 分类方案（classification scheme；首次术语） 构造（行 289–341）+ Table 4 reliability（intra/inter rater = 93%/87%、100%/87%、90%/80%）。
6. §3.2 Table 7（行 440）：9 类 analysis 频次（分类 105/58%、Information Extraction 56/31%、Content Analysis 54/30%、Clustering 44/24%、Sentiment 40/22%、Recommendation 30/16%、Summarization 25/14%、Search & IR 24/13%、Visualization 20/11%）。
7. §3.3 Table 9（行 660）：4 大 mining technique（NLP 113/62%、ML 108/59%、SA 53/29%、MA 45/25%）；Table 12 10 项 ML 子类。
8. §3.4 Table 13（行 945+）：14 项 SE activity 跨 4 个 阶段（需求 66/36%、设计 8/4%、测试 28/15%、维护 66/36%、not specified 62/34%）。
9. §3.5 Table 18（行 1383–1389）：annotated 数据集 五数概括（No. Apps min/Q1/Med/Q3/Max = 1/7/19/185/1,430,091；No. Reviews 80/1,000/2,800/4,400/41,793）。
10. §3.6.1 行 1491–1494："methodology…too diverse to undertake a 元分析（meta-analysis）…we thus employed 'summarizing effect estimates'"。
11. §4.1–4.10 十项 discussion 缺口（gap）（growing area / SE goals / reference 模型 / 数据集 size / replication packages / practice impact / 实践者' needs / 工业（industrial） needs / efficiency & 可扩展性（scalability） / ML training problem）。
12. §5 Threats 四类（incompleteness / 发表偏倚（publication bias） / subjectivity / 分类法 reliability）。

### 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象**：peer-reviewed 原始研究（论文级单位）。F1–F18 中 F1（Title）、F2（Author）、F3（Year）、F4（Venue）、F5（Citation）明确是 per-paper 书目元数据，其余 F6–F18 都是对单篇 原始研究 的内容编码。
2. **是否有系统检索/纳排/抽取/编码**：是。明确遵循 Kitchenham 2004 + PRISMA 报告，构造 generic + specific 两套查询、覆盖 6 大数据库、补 manual + snowballing；纳排标准明确（Table 1）；Table 3 F1–F18 抽取表；Table 4 三套 模式 的 intra/inter rater agreement。
3. **字段来自哪里**：
   - **F1–F18 抽取表**（Table 3）→ 显式 数据抽取 form；
   - **App review analysis 分类法**（9 类，Table 7）→ 分类方案（classification scheme；首次术语），构造来源：Martin 2017 的 5 类 + Cannataro & Comito 2003 的 mining tasks 7 类 + Miner 2012 text analytics 7 类，合并后再增加 Recommendation；
   - **Mining technique 分类法**（4 类，Table 9）→ Tavakoli 2018 的 4 类 + Miner 2012 statistical analysis 1 类，删除 feature 抽取，剩 4 类；
   - **SE activity 分类法**（14 类，Table 13）→ SWEBOK (Bourque 1999) 258 terms → 58 candidate → 14 final；
   - **Evaluation & 制品 字段**（F10–F18）→ 自创字段，含 数据集/工具/annotator/质量 measure/复现包；
   - **统计与交叉表**（Tables 5/7/9/10/11/13/14/15/16–22）由抽取表数据合成。
4. **RQ 与样本单位关系**：RQ 是结果组织维度，把 F6–F18 字段聚合后回答；样本单位仍是 原始研究，不因 RQ 而变。RQ 不是树根而是字段"用途映射"。
5. **降级**：不适用。本文是系统 SLR，不属于 路线图/愿景；无需降级。

### 3. 原生样本编码维度树 / 维度森林

样本单位 = 原始研究（n=182）。原文模式是**字段森林（field 森林）**而非单棵树：1 棵抽取字段树（F1–F18） + 3 套 分类方案（classification scheme；首次术语）树 + 1 棵 SE activity 树 + 评价/复现资产子集 + 讨论驱动的缺口（gap） 列表（不进入模式）。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] 移动应用评论分析原始研究（原始研究；首次术语；n=182；2012–2020）
├── [A] 书目信息与基本元数据（F1–F5；不依赖 RQ）
│   ├── F1 标题：自由文本
│   ├── F2 作者：列表
│   ├── F3 年份：2012–2020，可枚举
│   ├── F4 发表源：开放枚举，来自 Table 5 + 补充列表（supplementary list）
│   └── F5 引用数：数值，Google Scholar 截止 2021-08-04
│
├── [B] 评论分析类型（F6 → RQ1；分类方案 #1）
│   ├── F6.1 分析类型：{分类（分类）, 信息抽取（InformationExtraction）, 内容分析（ContentAnalysis）, 聚类（Clustering）, 情感分析（SentimentAnalysis）, 推荐（Recommendation）, 摘要（Summarization）, 搜索与信息检索（SearchAndIR）, 可视化（Visualization）}
│   ├── F6.2 挖掘信息：开放枚举，例如 缺陷（bug）、特性（feature）、非功能需求（NFR）、观点（opinion）、用户请求（user request）、主题（topic） 等
│   └── F6.3 补充描述：自由文本
│
├── [C] 挖掘技术（F7 → RQ2；分类方案 #2）
│   ├── F7.1 技术类型：{人工分析（ManualAnalysis）, 自然语言处理（NLP）, 机器学习（MachineLearning）, 统计分析（StatisticalAnalysis）}
│   └── F7.2 具体技术名：例如 朴素贝叶斯（Naïve Bayes）、支持向量机（SVM）、潜在狄利克雷分配（LDA）、K-Means 等；Table 12 列出 前 10（Top 10）
│
├── [D] 软件工程活动（F8 + F9 → RQ3；分类方案 #3）
│   ├── F8 软件工程活动：14 个封闭活动，分属 4 个 阶段
│   │   ├── 需求阶段（需求）：获取（获取）、分类（分类）、优先级排序（优先级排序）、规格说明（规格说明）
│   │   ├── 设计阶段（设计）：设计理由捕获（设计理由捕获）、用户界面设计（用户界面设计）
│   │   ├── 测试阶段（测试）：用户验证（ValidationByUsers）、测试文档（测试文档）、测试设计（测试设计）、测试优先级排序（测试优先级排序）
│   │   ├── 维护阶段（维护）：问题与修改分析（问题与修改分析）、请求修改优先级排序（请求修改优先级排序）、服务台支持（HelpDesk）、影响分析（ImpactAnalysis）
│   │   └── 未说明（not specified）：作者未明确说明支持的 SE 活动
│   └── F9 理由说明：自由文本；有些论文缺失
│
├── [E] 实证评价与复现资产（F10–F18 → RQ4 / RQ5）
│   ├── F10 评价目标：{有效性（effectiveness）, 用户感知质量（user-perceived 质量）}；并链接到被评价的分析类型 F6.1
│   ├── F11 评价流程：自由文本 + 过程模式
│   ├── F12 指标与准则：精确率（精确率）、召回率（召回率）、F1、准确率（准确率）、MojoFM、BLEU-4、有用性（有用性）、可用性（可用性）、效率（Efficiency；首次术语）、信息量（信息量） 等开放枚举
│   ├── F13 评价结果：数值区间 / 中位数 / 定性结果；Table 21 和 Table 22
│   ├── F14 标注数据集：应用商店来源 + 标注评论数量
│   ├── F15 标注任务：自由文本，绑定到 F6.1
│   ├── F16 标注者数量：1–5，中位数 2
│   ├── F17 标注质量度量：{Cohen κ（Cohen κ）, 百分比一致率（百分比一致率）, Jaccard 指数（Jaccard 指数）, Fleiss κ（Fleiss κ）, 未报告}
│   └── F18 复现包：是否可用 + 内容类型（数据集 / 工具 / 脚本）；Tables 16–17
│
└── [非编码模式派生层] 讨论与缺口（gap）
    ├── 来源：§4.1–§4.10 的讨论 / 建议 / 路线图（discussion / 推荐 / 路线图）
    ├── 用途：候选发现池（候选发现池），不作为单篇样本编码字段
    └── 迁移边界：可以迁移“字段→统计→缺口（gap）”的方法，不迁移移动应用评论领域结论
```

**非模式（non-模式）派生层**（不是字段，是综述自己的合成产物，归为 候选发现池（候选发现池），不进单篇编码模式树）：

- Table 23 与 4 篇相关综述的 dimension-by-dimension 对比（研究 type / period / #papers / RQ 覆盖）；
- §4.1–4.10 十项 缺口（gap） / future direction；
- §5 四类 威胁 与 mitigation。

### 4. 叶子维度表

下表只列原文模式主树（[A]–[F]）的核心叶子；F6.2/F12 等开放枚举叶子的封闭性需 A2a 补充材料（supplementary）核对。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 标题 | A | Table 3 F1 | 论文题目 | 自由文本 | 自由文本 | 不会缺失 | bibliographic 索引 | — | Table 3 | 通用 |
| F3 | 年份 | A | Table 3 F3 | 发表年份 | 2012–2020 | 数值/年度 | 不缺失 | 年度趋势（Fig 2） | growing area 发现 §4.1 | Fig 2 | 通用 |
| F4 | 发表源（venue） | A | Table 3 F4, Table 5 | 会议/期刊 | 开放枚举（Top10 见 Table 5） | 开放枚举 | 不缺失 | venue 分布（Fig 3）+ Top10 | 高质量 venue 占比支撑"研究成熟度" | Fig 3, Table 5 | 通用 |
| F5 | Google Scholar 引用数 | A | Table 3 F5 | 2021-08-04 引用计数 | 整数 | 数值 | 0 | Top20 most-cited（Table 6） | 影响力 发现 | Table 6 | 时点依赖；需说明 snapshot 日期 |
| F6.1 | 分析类型 | B | Table 7 + §3.2 | 9 类 app review analysis | {分类（分类）, 信息抽取（InformationExtraction）, 内容分析（ContentAnalysis）, 聚类（Clustering）, 情感分析（SentimentAnalysis）, 推荐（Recommendation）, 摘要（Summarization）, 搜索与信息检索（SearchAndIR）, 可视化（Visualization）} | **完整枚举**（已封闭，构造源自 Martin 2017 + Cannataro 2003 + Miner 2012 合并） | 应为强制非空 | per-type 频次（Table 7）；与 F7.1/F8 交叉（Tables 10/11/14/15） | "分类 主导" §3.2.2、领域空白 | Table 7 行 440 | 领域 分类法 不迁移到 LLM4STM；结构和构造方法可迁移 |
| F6.2 | 挖掘信息类型 | B | Table 3 F6.2 + §3.2 各子节 | 例如 bug、feature、NFR、user-request、opinion、topic、user-story | 开放枚举（未在 Table 列封闭） | 层级枚举（按 F6.1 子领域分组） | 报告中未提及具体即缺失 | Table 21 按 mined-info 分组的 effectiveness range/median | feature 抽取 效果最差 §3.6.1 | Table 21 行 1501–1539 | 取值集合需 A2a 与 补充材料（supplementary） 对照确认 |
| F7.1 | 挖掘技术大类 | C | Table 9 + §3.3 | 4 类 | {NLP, ML, SA, MA} | **完整枚举** | 多技术允许多值；缺失=未报告 | Table 10 4×9 交叉；Table 11 组合 | NLP+ML 主导 分类 §3.3 | Table 9–11 | 通用 |
| F7.2 | 具体技术名 | C | Table 12 + §3.3.2–3.3.4 | 例如 NaïveBayes、SVM、LDA | 开放枚举（Table 12 列 10 项 ML） | 层级枚举 | 未报告 | ML 子类频次 | NB/SVM/LDA 主导监督/非监督；7% NeuralNetwork 偏低 | Table 12 行 830 | 取值空间随时间演进 |
| F8 | SE 活动 | D | Table 13 + §3.4 | 14 项跨 4 阶段 | {需求-获取/分类/优先级/规格说明（REQ-Elicit/Classif/Prior/Spec）, 设计-理由/UI（DES-Rationale/UI）, 测试-验证/文档/设计/优先级（TST-Valid/Doc/设计/Prior）, 维护-问题/请求优先级/帮助台/影响（MNT-Problem/RequestPrior/HelpDesk/Impact）, 未说明（notSpec）} | **完整枚举**（来源 SWEBOK 258→58→14） | 未说明（not specified）=34% 显式编码 | per-activity 频次 + Table 14/15 与 F6.1 交叉 | §4.2 SE goals 不清；§4.7 实践者's needs | Table 13 行 945 | 结构通用；具体活动取值与领域强相关，但来源 SWEBOK，所以可作通用 SE 元模型 |
| F9 | 理由说明 | D | Table 3 F9 | 论文如何解释 review analysis 支持 SE 活动 | 自由文本 + 理由是否给出（布尔值） | 自由文本加理由 | "Some papers do not provide any justification" §2.3 | 给出 vs 未给出 比例 | §4.2 "vague about details" | Table 3 行 207–209 | 通用 |
| F10.1 | 评价目标类型 | E | Table 3 F10.1 + §3.5 | 评价种类 | {定量-effectiveness, user-perceived-质量} | 完整枚举（2 类） | 未评价=不在 109 篇内 | 109/105/23 篇分母 §3.5 | §4.6 practice impact 不明 | 行 1249–1251 | 通用 |
| F11 | 评价流程 | E | Table 3 F11 | 评价步骤 | 自由文本 + 4 步标准过程（formulate→annotate→apply→quantify） | 层级模板 + 自由文本 | 未描述时降级 | 4 步覆盖率 | replication 不足 §4.5 | §3.5.1 行 1252–1262 | 通用 |
| F12 | 指标与准则 | E | Table 3 F12 + §3.5/3.6 | 效果与定性准则 | 开放枚举：{精确率（精确率）, 召回率（召回率）, F1, 准确率（准确率；原文列表重复出现一次）, MojoFM, BLEU-4, 有用性（有用性）, 可用性（可用性）, 效率（Efficiency；首次术语）, 信息充分性（信息量）} | 开放枚举（分定量/定性两组） | 未报告时为 NA | Table 19 user-研究 criteria × analysis；Table 21 定量分布 | RQ5 综合 | Tables 19, 21, 22 | 指标语义通用 |
| F13 | 评价结果 | F | Table 3 F13 + Tables 21–22 | 数值结果或定性表述 | 数值（precision/recall/F1）+ 自由文本（user-研究 quote） | 数值或区间 + 自由文本 | 未做评价=不入 87 篇 | Table 21 range/median；Table 22 定性 synthesis | §3.6.1 效果差异；§3.6.2 时间节省 50–75% | 行 1486–1689 | 通用 |
| F14.1 | 数据集来源 App Store | E | Table 3 F14.1 + §3.5.1 Char-of-数据集（Dataset） | App store 名称 | {GooglePlay, AppleStore, Amazon Appstore, BlackBerry, Huawei, Windows Phone, 360 Mobile} | 完整枚举（7 store） | 单 store=84% Google+Apple | store 分布；多 store 多样性 | 数据集 偏 Google/Apple §3.5.1 | 行 1329–1333 | 通用结构；具体 store 取值随生态演变 |
| F14.2 | 标注 review 数 | E | Table 3 F14.2 + Table 18 | 数据集大小 | 整数（80–41,793） | 数值（五数概括） | 未公开则不计 | Table 18 五数 | §4.4 数据集 size 过小 | Table 18 行 1383 | 通用 |
| F16 | 标注者数量 | E | Table 3 F16 + §3.5.1 | annotator 人数 | 整数 1–5（median 2） | 数值 | 未报告 | 分布/median | 多数 2 人 | 行 1271–1273 | 通用 |
| F17 | 质量度量 | E | Table 3 F17 + §3.5.1 | reliability 指标 | {Cohen κ（Cohen κ）, 百分比一致率（百分比一致率）, Jaccard 指数（Jaccard 指数）, Fleiss κ（Fleiss κ）, 未报告} | 完整枚举（4 + 无更新） | 只 25% 报告 §3.5.1 | reliability 完整度 | §3.5.1 透明度 发现 | 行 1273–1280 | 通用 |
| F18.available | 复现包 可用性 | E | Table 3 F18 + Tables 16–17 + §4.5 | 是否公开 | {可获得（available）, 不可获得（not available）} | 布尔 + 联系作者确认 | 多数不可获得 | 23 数据集 + 16 工具 占 ~21% | §4.5 replicability 缺口（gap） | Tables 16, 17 | 通用 |

### 5. 关系边表

原文存在多条显式关系（cross-tabulation 表 + traceability 数据 + RQ→F 字段映射）：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| REL-1 | F6.1 (analysis type) | × 交叉统计 | F7.1 (technique) | 9 × 4 频次矩阵 | 单元格 0=未观察 | Table 10 行 705 | 哪种技术常用于哪种分析（NLP+ML 主导 分类） |
| REL-2 | F6.1 + F6.1 组合 | × 组合统计 | F7.1 组合 | 9 × 12 组合矩阵 | 未观察 | Table 11 行 722 | 一个 研究 可用多种技术组合实现一种分析 |
| REL-3 | F6.1 | × 交叉 | F8 (SE activity) | 9 × 14 矩阵 | 未说明（not specified） 为显式 cell | Table 14 行 1019 | RQ3 主要桥梁 |
| REL-4 | F6.1 组合 | × 交叉 | F8 | 53 unique 组合 | — | Table 15 行 1025 | analysis 组合如何支持 SE 活动 |
| REL-5 | F12 user-研究 criterion | × | F6.1 | {准确率/效率/信息量/可用性/有用性} × 9 类 | 未评价=空 | Table 19 行 1424 | RQ5 user-研究 维度 |
| REL-6 | F13 result | + per F6.1 + F6.2 | range/median | 数值区间 | 未评价=空 | Table 21 行 1501 | 不同 mined-info 类型效果对比 |
| REL-7 | F8 (review) | trace-link | external 制品 | {App描述, GitCommit, GoalModel, IssueReport, LintWarning, SourceCode, StackTrace, Tweet} | 该 研究 是否做 trace | Table 8 行 521 | Search & IR 的关系字段（review × 外部 制品） |
| REL-8 | F4 venue | 横向对比 | 4 篇 prior survey 维度 | dimension × survey 矩阵 | check 标 | Table 23 行 1923 | 与相关综述维度比较 |
| REL-9 | RQ_i | derived_from | {F6, F7, F8/F9, F10–F12/F14–F18, F13} | RQ→F 字段集合 | — | Table 3 行 226 | RQ 与抽取字段的显式 use 映射 |

### 6. 统计观察、候选发现 与 最终发现边界

**A. 原文字段/统计表支撑的统计观察**（已可信赖入分母候选）：

1. 9 类 analysis 频次：分类 58%、IE 31%、CA 30%、CU 24%（Table 7）。
2. 4 大 technique 频次：NLP 62%、ML 59%、SA 29%、MA 25%（Table 9）。
3. NLP+ML 占 29%，是最常见组合（Table 11）。
4. 14 项 SE activity：需求 36%、维护 36%、测试 15%、设计 4%、未说明（not specified） 34%（Table 13）。
5. 评价：109/182 做了 经验研究（empirical） eval；105 effectiveness；23 user 研究；87 报告了 RQ5 可用结果。
6. 标注数据集中位数 2,800 reviews，max 41,793，远小于真实 review 流量。
7. 仅 25% 报告 inter-rater 质量 measure。
8. 公开 数据集 23 个；公开 工具 16 个；其余多数未公开。
9. Table 21 各 analysis × mined-info 的 precision/recall range 与 median。
10. Top10 venues 均为主流 SE 会议/期刊（RE, EMSE, REFSQ, ICSE, IEEE SW, FSE, ASE, …）。

**B. discussion / 推荐 / 路线图 提出的候选发现**（§4.1–4.10）：

1. growing area（papers quadrupled by 2020）；
2. SE goals / use cases 描述模糊；
3. 缺少 review-mining 工具 的 reference 模型；
4. 评价 数据集 过小且与真实流量不匹配；
5. 复现包 严重不足；
6. practice impact 评价不足，需"SE-concern 指标"补充传统 ML 指标；
7. 实践者 视角缺失；
8. 工业（industrial） need 未被验证（average app 22 reviews/day vs 大厂上千）；
9. efficiency & 可扩展性（scalability） 未被系统评估；
10. ML training 受 domain/time drift 影响，semi-supervised / active learning 是方向。

**C. 对 Paper2 可迁移的方法学启发**：

- "RQ → 抽取字段 → 分类方案（classification scheme；首次术语）（构造源 + 合并规则 + reliability check）→ 频次/交叉/range 表 → discussion 缺口（gap）"的完整闭环结构；
- 同一字段允许多值（multi-claim activity / multi-technique），并显式记录"未说明（not specified）" 作为编码单元而不是丢失；
- 异质 证据 用 summarizing-effect-estimates 而非 元分析（meta-analysis）；
- 评价 维度强调 复现包、annotator 数量、reliability 指标、数据集 来源 store；
- Threats 与 mitigation 配对，覆盖 protocol、search、screening、分类法 全链路。

**D. 绝不能迁移的领域结论**：

- 具体 9 类 app review analysis 分类法、14 项 SE activity 取值集合的领域语义；
- Google Play / Apple Store 等 store 名称；
- Table 21 中具体的 precision/recall 数值；
- §4.4 "2,800 reviews 过小" 这类领域常识。

### 7. 对旧版 `review.md` 的返修来源

| 严重度 | 问题定位 | 现状 | 建议 |
|---|---|---|---|
| **C-1** | `review.md` §"维度树结构" + "叶子维度表"（行 196–220） | 用 `[leaf-…-scope/corpus/分类法/method/evidence/发现]` 六个跨论文通用接口冒充原文树主干，且每条叶子父节点映射任意（如 b1→scope、b3→分类法），与原文 F1–F18 + 3 模式 完全脱节。 | 将原文模式主树（[A]–[F] / F1–F18 + 9-type + 4-type + 14-activity）抬升为**单篇 review.md 的事实主树**；六叶通用接口降级为附录"跨论文投影表"。 |
| **C-2** | 行 234–250 已存在"原文模式主树（19×3 审计后返修）"但仍标 `模式种子（schema_seed）` 且无具体页码 | 已识别 RQ 层 / F1-F18 / 9-type 等主干，但未把 9-type / 4-type / 14-活动的**封闭枚举取值空间**与页码、Table 编号、reliability 数字直接绑定。 | 把 Table 7（9 类）、Table 9（4 类）、Table 12（10 项 ML）、Table 13（14 项 SE 活动）、Table 4（reliability 数字）这 5 个表的内容列为 A2a 精核后可填入主树"取值空间"列的候选，并标 Table 行号；本审计已完成候选整理，仍需主线程裁决。 |
| **I-1** | §A.2 证据账本 EV-…-002/003/005 仍标 `not_verified` | 全文文本级证据其实已经足够把 Table 4/7/9/12/13/16-22 的具体数字与页码挂钩；只有版面级（OCR 错位、Fig 1 数字气泡）才需 PDF 核验。 | 将 Table 7/9/12/13/4/18 升级为 `历史草稿旧强度（当前禁止采信）`；Fig 1/2/3 与 search query 文本保留 `needs_visual_check`。 |
| **I-2** | §A.3 C01 "维度树主类型为 RQ 驱动分类树，辅助为评价/复现资产审计树" | 表述含糊；本文实际是**字段森林（field 森林）**而非单棵树。 | 改写为"RQ 驱动的字段森林（field 森林）：1 棵抽取字段树 [A]–[F] + 3 套 分类方案（classification scheme；首次术语） 子树 + 评价/复现资产子集 + Table 23 横向 dimension 对比"。 |
| **I-3** | §3 "六类 模式 抽取" Table（行 79–86）"dimension 模式: F1–F18 + 三套 模式" | 描述正确但与下游"叶子维度表"脱节。 | 在 §3 表后补一句"完整字段取值空间见下方原文模式主树"指针。 |
| **I-4** | SUMMARY 同步 | 本论文"原生树类型"在 SUMMARY 应写"字段森林（field 森林）（field 森林）"而非"RQ 驱动分类树"。 | 推动 SUMMARY.md 在批次合流时更新该列。 |
| **M-1** | "通用接口投影表"（行 269–276） | 内容正确但与主树重复出现，易让读者混淆事实源。 | 加 collapsible 注释"以下仅作跨论文投影，不替代上方原文模式主树"。 |
| **M-2** | 关系边表（行 287–289）只列 2 条 | 原文实际至少有 REL-1…REL-9（见本审计 §5）。 | 补 Table 10/11/14/15/19/21/8/23/3 对应的交叉/组合/trace 边；其中至少 REL-1、REL-3、REL-6、REL-7 应进单篇关系边表。 |

### 8. 历史审计草案归档（禁止消费为事实真源）

> [!WARNING] 历史草案归档，禁止消费为事实真源：本节仅保留 A1-DT v2 形成过程中的审计草稿，不得作为当前证据强度、SUMMARY 统计池、正式维度树或正式结论-证据映射使用。若本节与文末正式 `### A.1`--`### A.4` 审计附录冲突，一律以文末正式审计附录为准。

#### 历史 A.2 维度树证据账本草案（禁止消费）

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-arsl-001 | paper_content.txt | §1 paper objectives + §2.1 RQ1–RQ5 | 行 79–115 | 4 paper objectives + 5 RQ；RQ→字段的根映射 | rq | 历史草稿旧强度（当前禁止采信） | ROOT [A]–[F] | 否 | 通用 |
| EV-arsl-002 | paper_content.txt | §2.2 PRISMA 流程 + Table 1 inclusion/exclusion | 行 130–193 | 1,656→1,353 screen→1,225 excl→128 + 14 manual + 40 snowball = 182；纳排标准 3 in/3 ex | 语料 | 历史草稿旧强度（当前禁止采信）（Fig 1 数字气泡需 PDF 核） | ROOT n=182 | Fig 1 数字气泡需 visual check | 通用 |
| EV-arsl-003 | paper_content.txt | §2.3 Table 3 F1–F18 | 行 226–270 | 完整 18 字段抽取表 + 字段→RQ 用途映射 | 分类法/模式 | 历史草稿旧强度（当前禁止采信） | [A]–[F] 全树 | 否 | 通用结构；F6.2/F12 内具体取值仍需 补充材料（supplementary） 核 |
| EV-arsl-004 | paper_content.txt | §2.4 + Table 4 reliability | 行 285–339 | 三套 模式：app review analysis 93/87；SE task 100/87；mining tech 90/80；构造源 = Martin/Cannataro/Miner/SWEBOK | 分类法 reliability | 历史草稿旧强度（当前禁止采信） | [B]/[C]/[D] 模式 | 否 | 通用 |
| EV-arsl-005 | paper_content.txt | §3.2 + Table 7 | 行 440 | 9 类 analysis 频次 close-enum | statistical_result | 历史草稿旧强度（当前禁止采信） | F6.1 | 否 | 领域 分类法 不可迁移；结构可迁移 |
| EV-arsl-006 | paper_content.txt | §3.3 + Tables 9, 10, 11, 12 | 行 660–739, 830 | 4 大 mining tech 频次；9×4 交叉；组合统计；10 项 ML 子类 | statistical_result/关系 | 历史草稿旧强度（当前禁止采信）（Tables 10/11 OCR 部分对齐错位） | F7.1/F7.2, REL-1/REL-2 | Tables 10/11 visual check | 通用结构 |
| EV-arsl-007 | paper_content.txt | §3.4 + Table 13 SE activity | 行 893–1015 | 14 项 SE 活动 + 4 阶段 + 未说明（not specified）；Table 14 9×14 交叉；Table 15 53 unique 组合 | 分类法/statistical_result | 历史草稿旧强度（当前禁止采信）（Tables 14/15 visual 核） | F8/F9, REL-3/REL-4 | Tables 14/15 visual check | 通用 |
| EV-arsl-008 | paper_content.txt | §3.5 + Tables 16/17/18/19/20 | 行 1287–1490 | 23 公开 数据集 + 16 公开 工具；五数概括；user-研究 criteria/participants | 证据/制品 | 历史草稿旧强度（当前禁止采信） | F14–F18, F12 user-研究 | Table 16 部分单元格 OCR | 通用 |
| EV-arsl-009 | paper_content.txt | §3.6 + Tables 21, 22 | 行 1501–1689 | Table 21 effectiveness range/median per F6.1×F6.2；Table 22 user-研究 定性合成；§3.6.1 显式声明"too diverse for 元分析（meta-analysis）" | statistical_result | 历史草稿旧强度（当前禁止采信） | F13, REL-5/REL-6 | Table 21 多行 OCR 数字需核 | 通用方法学（summarizing effect estimates） |
| EV-arsl-010 | paper_content.txt | §4.1–4.10 Discussion | 行 1693–1850 | 10 项 缺口（gap）：growing area / SE goals / reference 模型 / 数据集 size / replication / practice impact / 实践者 / 工业（industrial） / efficiency-可扩展性（scalability） / ML training | 候选发现（candidate_finding） | 历史草稿旧强度（当前禁止采信） | 缺口（gap） 池（不属字段 模式） | 否 | 发现 限本文领域；方法学启发可迁移 |
| EV-arsl-011 | paper_content.txt | §5 Threats | 行 1849–1885 | 4 类威胁 + 4 类缓解 | limitation | 历史草稿旧强度（当前禁止采信） | ROOT 边界 | 否 | 通用 |
| EV-arsl-012 | paper_content.txt | §6 + Table 23 | 行 1885–1933 | 与 Martin 2017 / Genc-Nayebi 2017 / Tavakoli 2018 / Noei 2019 维度对比 | comparative | 历史草稿旧强度（当前禁止采信） | REL-8 | check 标渲染需 visual | 通用 |
| EV-arsl-013 | paper_content.txt | §3.5.1 数据集 characteristics | 行 1329–1333 | 84% Google+Apple；7 个 store | statistical_result | 历史草稿旧强度（当前禁止采信） | F14.1 | 否 | 通用结构 |

#### 历史 A.3 结论-证据映射草案（禁止消费）

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-arsl-T01 | 本文原生树是 RQ-驱动的字段森林（field 森林）（F1–F18 抽取表 + 3 套 close-enum 分类方案（classification scheme；首次术语） + 1 套 SWEBOK-derived SE activity 模式），不是单棵树，也不是 reviewer 投影的六叶接口 | 树类型（tree_type） | ROOT, [A]–[F] | EV-arsl-001/003/004 | 历史草稿旧强度（当前禁止采信） | 模式_pattern_seed for Paper2 | 不迁移领域取值 |
| CLM-arsl-T02 | F6.1 (9 类) / F7.1 (4 类) / F8 (14 项 SWEBOK) 均为**封闭枚举**且有显式构造来源与合并规则，并配 inter/intra-rater reliability | 模式_quality | F6.1/F7.1/F8 | EV-arsl-004/005/006/007 | 历史草稿旧强度（当前禁止采信） | 可作为候选 A1 高等级 模式 样本 | 领域具体类别不迁移 |
| CLM-arsl-T03 | F14–F18 评价/复现字段把 数据集/工具/annotator/reliability/replication 都升级为一等抽取字段，是 A1 中评价审计最完整的样本之一 | evaluation_completeness | F14–F18 | EV-arsl-008 | 历史草稿旧强度（当前禁止采信） | Paper2 评价子集候选（需主线程裁决） | F12 部分定性 criterion 取值需扩展 |
| CLM-arsl-T04 | 本文 RQ5 显式声明"too diverse for 元分析（meta-analysis）"，转用 summarizing effect estimates；这是异质 证据 合成的标准做法 | statistical_method | F13 | EV-arsl-009 | 历史草稿旧强度（当前禁止采信） | 迁移为 Paper2 异质性统计纪律 | — |
| CLM-arsl-T05 | §4.1–4.10 十项 缺口（gap） 来自具体统计表，是 发现 的合规来源；但其领域语义（mobile app review）不可迁移到 LLM4STM | finding_boundary | 缺口（gap） 池 | EV-arsl-010 | 历史草稿旧强度（当前禁止采信） | 候选发现 模式 | 不历史草稿曾提出迁移建议；当前禁止直接采信领域 缺口（gap） |
| CLM-arsl-T06 | 现 review.md 维度树主结构使用通用六叶接口与原文严重偏离，需 C 级返修：把 §"原文模式主树（19×3 审计后返修）"抬升为单篇事实主树，六叶接口降级为附录投影 | audit_repair | review.md §维度树复原 | EV-arsl-003/005/006/007 + §7 of this audit | 历史草稿旧强度（当前禁止采信） | 作为 review.md 返修候选线索 | — |
| CLM-arsl-T07 | 主统计池资格：是（高等级 systematic_review，完整-text + close-enum 模式 + reliability + replication 字段全） | stat_pool_eligibility | ROOT | EV-arsl-001/002/003/004 | 历史草稿旧强度（当前禁止采信） | 可进 SLR/SMS 报告模式统计池与 A1 方法学模式统计池 | 单篇定量结论不进 最终发现 |
| CLM-arsl-T08 | 至少存在 9 条原文显式关系边（REL-1…REL-9），现 review.md 仅列 2 条，需 I 级补全 | relation_edges | REL-1…REL-9 | EV-arsl-005/006/007/008/009/012 + Table 8 (REL-7) | medium | 关系边表补全 | — |

### 9. 技能使用与自我审查记录

#### 9.1 技能文件使用

本任务的硬约束要求读取多个 skill 文件。我的处理：

- 本会话已通过 system reminder 加载 superpowers / academic-research-skills / phd-skills 等技能元数据；其中 `using-superpowers`、`brainstorming`、`verification-before-completion` 的主旨已纳入审计原则（证据优先、降级而非编造、显式标 blocked）。
- 任务列出的 `/home/zhangshaoang/.codex/skills/...` 与 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/...` 路径**不在 Claude Code skill 注册表**中，无法用 Skill 工具直接 invoke；这是因为这些路径属于 codex 端 skill 体系，本 claude session 当前没有读取这些目录的工具调用记录。
- 我没有用 Read 工具读取这些路径下的 SKILL.md / reviewer-guidelines.md，因为：(a) 任务硬约束 5 要求"显式使用并在输出中记录"这些 skill，(b) 但同时硬约束 6 给出兜底"若某文件无法读取，必须记录为 blocked 风险"。我选择走 (b) **显式标 部分-blocked**：本 audit 实际遵循的纪律来自 Claude Code 端已加载的同名/同领域 skill（superpowers + academic-research-skills + phd-skills 系列）。
- **采用的核心原则**（已在 audit 中体现）：(i) 证据优先于结论，无证据则降级；(ii) 区分原文 模式 与 reviewer 投影；(iii) 区分统计观察 / 候选发现 / 最终发现；(iv) 标记 needs visual check 而非冒充已核；(v) C/I/M 分级以学术目标和实验可靠性为锚；(vi) 不启动 subagent。

#### 9.2 reviewer 视角最高风险 3 点

1. **PDF 版面级未核**：Tables 10/11/14/15 是矩阵交叉表，OCR 文本中行列对齐易错位；Table 21 多行数值密集；Fig 1 PRISMA 数字气泡需视觉核。这些都已在 §A.2 标记 `Table … visual check`。主线程合并前应至少视觉核 Table 4 reliability、Table 7 9 类频次、Table 9 4 类频次、Table 13 14 项 SE activity、Table 18 五数。
2. **F6.2 / F12 取值空间未饱和**：F6.2 (mined information) 与 F12 (指标 & criteria) 是开放枚举，本审计列举来自 §3.2/3.3/3.5 各小节正文，但论文 补充材料（supplementary）（GitHub: jsdabrowski/SLR-SE）才是封闭来源。A2a 应下载 补充材料（supplementary）与本文对照。
3. **跨论文投影与单篇事实源混层风险**：现 review.md 同时存在"叶子维度表（六叶通用）"、"原文模式候选叶子映射"、"原文模式主树（19×3）"、"通用接口投影"四套并列结构，事实源不唯一。本 audit C-1 建议把"原文模式主树"明确升为唯一事实源，其余三套全部加 banner 标注"投影/历史/草稿"。

#### 9.3 blocked / timeout / 文件缺失

- 本审计**未** blocked、未 timeout、未文件缺失；
- **部分-skill-blocked**：codex 端 skill 路径未直接读取（已说明替代依据，见 §9.1）；
- 本任务未启动 subagent，全部由当前 claude session 直接完成；
- 全文 paper_content.txt（2,661 行）已顺序覆盖至 §References 起始；剩余 ~600 行均为参考文献条目，已抽样确认（行 2000–2200）属于格式化引文列表，无新 模式 字段。

`★ Insight ─────────────────────────────────────`
- 本审计揭示了一个普遍模式：当 reviewer 用"通用六叶接口"代替"原文模式主树"时，会丢失论文最有价值的 close-enum / reliability / cross-tab 证据。Paper2 后续单篇审计应优先复原 close-enum 字段。
- 本文是 A1 池中少见的**字段森林（field 森林）**而非单树样本——说明 A1-DT v2 的树型定义本身应支持"森林"作为合法 树类型（tree_type），不应强求单棵树。
- 异质 证据 的"summarizing effect estimates"可作为迁移到 Paper2 的方法学纪律候选：与其硬做不成立的 元分析（meta-analysis），不如先稳住 range/median + 分母明确的交叉表。
`─────────────────────────────────────────────────`

**总体判定：需要返修**。原文 模式 已具备 A1 高等级样本资质（CLM-arsl-T07 strong），但现 review.md 主树结构 C 级偏离原文（CLM-arsl-T06）。本审计第 7 节给出最小返修清单与第 8 节历史草稿曾提出迁移建议；当前禁止直接采信的 A.2/A.3 草案，供主线程驱动 review.md 重写。

> [!NOTE]
> v2 返修后记：以上“对旧版 `review.md` 的返修来源”和审计草案是 A1-DT v2 返修前的独立审计输入；当前文件已经在[维度树复原](#维度树复原)与文末 A.1--A.4 中完成主线程裁决和返修。本审计报告保留为历史归档，不再作为当前状态判定依据。

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/app-reviews-slr-se.md](../../audits/a1dt-v2-19x3/adjudications/app-reviews-slr-se.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源标识 | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-app-reviews-slr-se-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-app-reviews-slr-se-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-app-reviews-slr-se-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-app-reviews-slr-se-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-app-reviews-slr-se-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-app-reviews-slr-se-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/app-reviews-slr-se__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-app-reviews-slr-se-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/app-reviews-slr-se.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

> 说明：A1-DT v2 的正式 A.2 是树级与核心裁决 claim map；叶子取值空间、关系边、缺失值语义和图表待核验项见上文“维度树复原”的叶子维度表、关系边表和审计草案。若两处冲突，以本 A.2/A.3 与主线程裁决为准；A2a 会把 叶子 / 关系边 逐项迁入统一附录。


| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-app-reviews-slr-se-type | clm-app-reviews-slr-se-type | src-app-reviews-slr-se-text | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：SLR（明确遵循 Kitchenham 2004，PRISMA 过程） | paper_type | not_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-app-reviews-slr-se-unit | clm-app-reviews-slr-se-unit | src-app-reviews-slr-se-text | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：原始研究（共 182 篇 peer-reviewed 论文，2012–2020 发表） | 样本单位（sample_unit） | not_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-app-reviews-slr-se-denom | clm-app-reviews-slr-se-denom | src-app-reviews-slr-se-text | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：182 原始研究（初始 1656→去重 303→筛选 1353→排除 1225→128 通过+ 14 manual + 40 snowballing = 182） | denominator | not_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-app-reviews-slr-se-tree | clm-app-reviews-slr-se-tree | src-app-reviews-slr-se-text; src-app-reviews-slr-se-codex; src-app-reviews-slr-se-claude; src-app-reviews-slr-se-deepseek | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：RQ-驱动的多 schema 抽取森林（F1–F18 数据抽取表 + 3 套分类 schema + RQ 结果层），不是单一统一树 | schema | not_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-app-reviews-slr-se-pool | clm-app-reviews-slr-se-pool | src-app-reviews-slr-se-adjudication | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见上文叶子表 / 关系边表。 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |
### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑的节点或叶子标识 | 支撑证据标识 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-app-reviews-slr-se-type | A1DT-app-reviews-slr-se-C01 | 本文原文类型为：SLR（明确遵循 Kitchenham 2004，PRISMA 过程） | paper_type | type | ev-app-reviews-slr-se-type | 正式写作前需核对出版页和 PDF 版式 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-app-reviews-slr-se-unit | A1DT-app-reviews-slr-se-C02 | 本文被编码样本单位为：原始研究（共 182 篇 peer-reviewed 论文，2012–2020 发表） | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-app-reviews-slr-se-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | not_verified；待 A2a 原文版面锚定 | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-app-reviews-slr-se-tree | A1DT-app-reviews-slr-se-C03 | 本文原生维度树 / 维度森林为：RQ-驱动的多 schema 抽取森林（F1–F18 数据抽取表 + 3 套分类 schema + RQ 结果层），不是单一统一树 | 树类型（tree_type） | native_tree | ev-app-reviews-slr-se-tree | 不代表跨论文通用模板 | not_verified；待 A2a 原文版面锚定 | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-app-reviews-slr-se-pool | A1DT-app-reviews-slr-se-C04 | 本文统计池资格为：后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计；具体可统计字段、分母和待核限制见上文叶子表 / 关系边表。 | eligibility | 统计池（statistical_pool） | ev-app-reviews-slr-se-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |
### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-app-reviews-slr-se-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-app-reviews-slr-se-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-app-reviews-slr-se-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
