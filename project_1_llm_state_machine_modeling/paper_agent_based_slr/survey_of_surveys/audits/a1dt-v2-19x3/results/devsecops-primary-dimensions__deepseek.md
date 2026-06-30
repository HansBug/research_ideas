现在我已完整阅读了所有技能文件和论文材料。以下为自包含的完整 A1-DT v2 审计报告。

---

# A1-DT v2 单篇全文审计报告：`devsecops-primary-dimensions`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `devsecops-primary-dimensions` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。已完整阅读 3158 行全文，逐章节、逐表核验 1--6 节及附录 A.1--A.3。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。已读取并核验元数据一致性。 |
| 是否打开或核对 `paper.pdf` | 否。本轮基于 `paper_content.txt` 全文文本级阅读；未做 PDF 版面逐图逐表视觉核验。Fig. 5--9（CPTM 模型图）的连线细节、Table 1--21 的确切格式需要 PDF 核验确认。 |
| 原文类型 | MLR（multivocal literature review），属于 tertiary / secondary study。不属 primary study。 |
| 被编码样本单位 | 纳入的 white literature 104 篇 + grey literature 43 篇 = **147 个 primary source**。每篇经标题/摘要筛选、全文审查、质量评价（QA 评分 ≥ 11/18），最终进入 Thematic Analysis。另有 confirmatory search 13 篇 WL + 7 篇 GL 未被纳入 TA 和 CPTM 模型。 |
| 样本数量 / 分母 | 147（主 MLR 池）；confirmatory search 的 20 个额外条目未被编码，不计入主统计。 |
| 原生树类型 | **维度森林**。该论文本身是 secondary/tertiary study（对 primary study 的综述），因此其原生维度树是两层：第一层是对 primary source 抽取的 Aspects → Themes（5 aspects，总计 132 themes）；第二层是跨 aspects 的 Categories → Lifecycle stages → CPTM 模型。这是一个多级、多面向的复杂编码框架，而非简单单树。 |
| 主统计池资格 | **局部可统计**。本文的 147 个 primary source 按 aspect 被编码为 themes，theme 频率（frequency count）可统计。但需注意：(1) 一个 primary source 可能跨多个 aspect 贡献多个 themes，分母非独立；(2) Metrics/Measurement 仅 7 WL + 13 GL = 20 themes，指标面薄弱；(3) Business category 主要由 GL 贡献，WL 几乎空白；(4) RQ2（Global DevSecOps）结论为"absence"，无正统计。对该论文本身的维度树统计与对 primary source 的跨论文统计是不同层级操作，必须区分。 |
| 总体判定 | **pass**（可作为 Paper2 维度树 schema seed 和跨论文审计模式先验进入下一阶段）。原文有系统检索、质量评价、编码方案和可审计的全文证据；维度树结构来自原文自身 TA 框架而非外部模板。但当前仍需 A2a 精核以完成页码/表图对应、CPTM 模型图文核验和频率统计的交叉复核。 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取文件清单

| 文件 | 读取范围 | 说明 |
|---|---|---|
| `paper_content.txt` | 全文 3158 行，涵盖 §1 Introduction 到 §6 Conclusion，含 Appendix A.1--A.3 及完整 References | 基于文字模式的 PDF 提取物；未发现显著乱码或缺失。 |
| `bibtex.bib` | 完整 1 条 | 与 metadata.json 一致 |
| `metadata.json` | 完整 | 字段与原文一致 |
| `review.md` | 476 行完整现有 review | 用于返修建议基准 |
| `paper.pdf` | 未打开 | 未做 PDF 版面逐图核验 |

### 1.2 读取方式说明

本轮全部基于 `paper_content.txt` 文本级阅读。以下情况需 PDF 视觉核验：

- Fig. 5、Fig. 6、Fig. 7、Fig. 8、Fig. 9：CPTM 模型的图形化展示，连线方向、节点位置、色彩编码等需要视觉确认。
- Table 1（既有综述比较表）、Table 2（overlap 统计）、Table 3（search execution summary）、Table 4（aspect 对应文献表）、Table 5（TA 结果汇总）等表格的实际排版和数值核对。
- Table 21（CPTM 映射表）中 C/P/T/M 编号到 lifecycle step 的映射关系需要视觉确认是否与文本描述一致。

### 1.3 关键原文证据锚点（12 个）

1. **§1 Introduction**：DevSecOps 定义、研究动机、RQ1/RQ2 完整陈述 → 维度树根节点来源
2. **§3.1--§3.8 Method**：MLR 流程（Fig. 1）、dual-track 检索策略、search strings、纳排标准（inclusion/exclusion criteria）、质量评价（QA checklist，passing score 11/18）、Thematic Analysis 四级抽象（text→code→theme→model） → 样本单位定义与字段来源
3. **§3.4.2 Search strings**：Search String 1（DevSecOps general）、Search String 2（GSE-specific）的完整字面 → 检索范围与方法学证据
4. **Table 4**（§4.1）：各 aspect 对应的 WL/GL 文献 ID 列表 → primary source 到 aspect 的映射证据
5. **Table 5**（§4.1）：TA 结果汇总表，展示各 aspect 的 extracted data 数量、coded data 数量、themes 数量、categories → 编码过程量化证据
6. **§4.1.A Definitions**：28 WL + 15 GL definitions → 74 codes → 21 themes → 4 categories（OPC/PC/Technology/Business） → Aspect→Theme 层级证据
7. **Table 6 + Table 7**：Definitions themes 及"Authors of common definitions"频率表 → 叶子字段值与原文来源的直接对应
8. **§4.1.B Challenges**：73 WL + 53 GL challenges → 85 codes → 23 themes → 28 challenges（含 5 个来自 Myrbakken 补充），Tables 8--11 → 挑战维度完整取值空间
9. **§4.1.C Practices**：219 WL + 137 GL practices → 142 codes → 56 themes → 60 practices（含 1 个补充），Tables 12--15 → 实践维度完整取值空间
10. **Table 21**（§4.1）：CPTM 映射到 Gartner 10-stage lifecycle 的完整 C-P-T-M 表 → 关系边（cross-aspect mapping）核心证据
11. **§4.2 RQ2**：GSE 维度的 absence finding + 四可能解释 → 负结果/缺口维度证据
12. **§4.3 Confirmatory search**：2022 年 13 WL + 7 GL 追加，未进入 TA 和 CPTM → 统计池边界证据

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

原文的纳入对象是 **individual primary studies（单篇一次文献）和 grey literature articles**。纳入标准见 §3.5：

- (a) 提到 DevSecOps 的一个或多个 primary aspect（definition, challenges, practices/activities/solutions, tools/technologies, metrics/measurement, global applications）
- (b) 英文
- (c) 2012 年及以后发表
- (d) 有明确 methodology/research design
- (e) 来源可信

经 title/abstract 筛选、全文审查、QA 评分（≥11/18）后，最终纳入 **104 篇 WL + 43 篇 GL = 147 个 primary source**。这些 primary source 就是被编码的样本单位。

每篇 primary source 被逐项抽取（extracted data segments），然后编码（codes），再译码为主题（themes），最后分类到 category 和映射到 lifecycle stage。原文 Table 4 列出了每个 aspect 对应的文献 ID。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**有。极系统。**

- **检索**：dual-track（white + grey），ACM Digital Library / IEEE Xplore / Scopus（WL）+ Google（GL），Search String 1 + Search String 2，snowballing（backward），数据库检索后不以 forward snowballing 为主
- **纳排**：inclusion criteria (a)--(e) + exclusion criteria (a)--(e)，明确排除 secondary studies
- **质量评价**：14 个 Y/N QA 问题（6 组）+ 1 个 scale 问题（Literature Type 0--4），满分 18，passing score 11（60%），QA scores 公开于 Zenodo
- **数据抽取**：从每篇 primary source 中提取 text segments（数据片段），按 aspect 归类
- **编码方案**：Reflexive Thematic Analysis（Braun & Clarke 方法），四阶段：extracted data → codes（labels）→ themes → model

### 2.3 原文字段来自哪里？

原文字段的来源是多层的：

- **Aspect 层**（5 个）来自 RQ1 的预设分类框架 → extraction form / classification schema
- **Theme 层**（132 个）来自 Thematic Analysis 对 extracted data 的归纳编码 → TA coding output
- **Category 层**（4 个）来自 theme 的进一步归类 → 在分析过程中 emergent 的 cross-cutting taxonomy
- **CPTM 映射**（C/P/T/M 到 lifecycle stages）来自 Gartner 10-stage lifecycle model → external reference framework
- **频率统计**来自每个 theme 的 primary source 计数 → 原文自身的 frequency table
- **Quality scores**来自 QA checklist → quality rubric
- **Supplementary materials**存放于 Zenodo（doi:10.5281/zenodo.7959584），包含 protocol、included papers + QA scores、raw text/codes、thematic synthesis、TA tables、full CPTM model

### 2.4 RQ 与样本单位是什么关系？

- **RQ1**（"What is the current state of DevSecOps?"）是**树根**：它驱动了 5 个 aspects 的选题（Sub-question 1.1--1.3），aspects 是主维度干，themes 是叶子，categories 是跨 aspects 的分类投影，lifecycle stages 是跨 themes 的关系投影。
- **RQ2**（"How is DevSecOps adopted in GSE?"）是一个**独立维度分支**：它被设计为与 RQ1 正交的 global dimension，但因 evidence absence 而降级为缺口发现（gap finding）。
- RQ 即维度树骨架；sub-questions 即维度分叉指令；TA 过程即叶子字段生成过程。

### 2.5 若无系统样本库，如何降级？

**本文有系统样本库，无需降级。** 但需注意以下边界：

- Confirmatory search 的 20 篇追加文献未进入 TA 和 CPTM，属于**统计池外数据**，只作验证用途
- RQ2 的"absence"结论是负结果，可作为 gap anchor 但不可生成正统计

---

## 3. 原生样本编码维度树 / 维度森林

以下是该论文自身的原生编码维度森林。它由两层结构组成：

- **第一层（编码层）**：对 147 个 primary source 进行 TA 编码产生的层级结构
- **第二层（模型层）**：将编码结果通过 categories 和 lifecycle stages 进行跨维度连接产生的 CPTM 模型

### 3.1 编码层：Aspect → Category → Theme 维度树

```
[DevSecOps Primary Dimensions - 根]
│
├── [Aspect: Definitions] ─── 28 WL + 15 GL segments
│   ├── [Category: OPC] → 若干 themes（如 "Collaboration between Dev, Ops, Security"）
│   ├── [Category: PC] → 若干 themes（如 "Integrating security into DevOps lifecycle"）
│   ├── [Category: Technology] → 若干 themes（如 "Automation of security processes"）
│   └── [Category: Business] → 若干 themes（如 "Delivering value securely"）
│   └── [Special Theme: Authors of common definitions] → 含 9 位被引作者及频次
│
├── [Aspect: Challenges] ─── 73 WL + 53 GL segments → 85 codes → 23 themes → 28 challenges
│   ├── [Category: OPC] → 9 challenges（C01--C09），含 C01 文化阻力、C02 协作障碍、C05 安全知识匮乏等
│   ├── [Category: PC] → 8 challenges（C10--C17），含 C10 安全集成不减速、C11 缺乏标准化流程等
│   ├── [Category: Technology] → 7 challenges（C18--C24），含 C18 缺乏成熟自动化工具、C21 云安全复杂性等
│   └── [Category: Business] → 4 challenges（C25--C28），含 C25 成本与投资回报、C27/C28 来自 Myrbakken 补充
│
├── [Aspect: Practices] ─── 219 WL + 137 GL segments → 142 codes → 56 themes → 60 practices
│   ├── [Category: OPC] → P01--P15（如 P02 安全文化、P04 安全培训、P05 安全冠军）
│   ├── [Category: PC] → P16--P32（如 P16 安全左移、P21 风险管理、P28 定义安全需求）
│   ├── [Category: Technology] → P33--P55（如 P33 自动化、P35 威胁建模、P36 持续监控、P40 容器安全）
│   └── [Category: Business] → P56--P60（如 P57 职责分离、P58 业务驱动安全）
│
├── [Aspect: Tools/Technologies] ─── 18 WL + 45 GL → 56 codes → 16 themes → ~18 tool groups
│   └── [Category: Technology] → T01--T18（如 T01 CI/CD 工具、T03 威胁建模工具、T08 SAST、T09 DAST 等）
│
├── [Aspect: Metrics/Measurement] ─── 7 WL + 13 GL → 20 codes → 16 themes → 20 metrics
│   ├── [Category: OPC] → M01（security-trained rate）
│   ├── [Category: PC] → M02--M13（如 M02 vulnerabilities found/fixed、M05 time-to-patch）
│   ├── [Category: Technology] → M14--M19（如 M14 test coverage、M15 automation rate）
│   └── [Category: Business] → M20（business metrics, 来自 Myrbakken 补充）
│
└── [Aspect: Global/GSE Dimension] ─── RQ2 结果
    └── [Finding: Absence] → 无 white/grey literature 覆盖 Global DevSecOps（四可能解释）
```

### 3.2 模型层：CPTM + Lifecycle 投影

这是对编码层的**关系投影**，将 Challenges (C01--C28)、Practices (P01--P60)、Tools (T01--T18)、Metrics (M01--M20) 映射到 Gartner 10-stage lifecycle：

```
[Gartner 10-Stage DevSecOps Lifecycle - 投影根]
│
├── Plan → C01,C03,C05,C06,C10,C11,C14,C15,C25,C26 | P01,P04,P05,P06,P07,P16,P17,P21,P22,P26,P27,P28,P32,P35,P51,P57,P58,P59 | T03,T14,T15 | M01,M03,M05,M08,M09,M10,M18,M20
├── Create → C02,C04,C07,C08,C09,C18,C19,C20 | P02,P03,P08,P09,P10,P11,P12,P13,P14,P15,P33,P34,P37,P50,P54 | T01,T02 | M15
├── Verify → C18 | P42,P46,P47,P48 | T08,T09,T12 | M11,M12,M14,M16
├── Preproduction → C18,C24 | P43,P44 | -- | M13,M19
├── Release → C12,C23,C27,C28 | P20,P29,P52,P55,P56,P60 | T13,T17 | M04,M20
├── Prevent → C17,C21,C22 | P23,P30,P39,P40,P53 | T04,T05,T06 | --
├── Detect → C18,C21,C22 | P36,P38,P39,P40,P41,P45,P53 | T06,T07,T10,T11,T16 | --
├── Respond → C21,C22 | P39,P40,P53 | T04,T05,T06 | --
├── Predict → C13,C16 | P18,P19,P24,P25,P49 | T18 | M17
└── Adapt → C01,C03,C15,C25,C26 | P01,P06,P28,P35,P57,P58,P59 | T03 | M09,M10,M20
```

### 3.3 核心叶子字段取值空间类型

| 叶子字段 | 取值空间类型 | 说明 |
|---|---|---|
| Aspect 归属 | 完整枚举 | 5 个固定值：Definitions/Challenges/Practices/Tools/Metrics |
| Category 归属 | 完整枚举 | 4 个固定值：OPC/PC/Technology/Business |
| Theme 标识（如 C01--C28） | 层级枚举 | 每个 aspect 内的 themes 有穷 ID 编号 + 名称 |
| Theme 频率 | 数值 | 贡献该 theme 的 primary source 计数 |
| Theme 来源文献列表 | 关系值 | 每个 theme 对应的 primary source ID 列表（如 S1-ACM-01 等） |
| Theme 跨 review 验证标记（asterisk） | 布尔 | 星号标记表示该 theme 与 prior reviews (Myrbakken, Akbar, Rajapakse 等) 完全/部分匹配 |
| Theme 补充来源 | 外部分类法引用 | 来自 Myrbakken (2017)、Prates (2019)、Rajapakse (2022) 等既有综述的补充 theme |
| 质量评价得分（QA score） | 数值或区间（0--18） | 每篇 primary source 的 QA 总分 |
| Lifecycle stage 映射 | 外部分类法引用（Gartner 10-stage） | C/P/T/M 到 lifecycle step 的投影关系 |
| Literature type（WL/GL） | 布尔/二值 | 区分学术文献与灰色文献 |
| GSE coverage | 布尔（yes/no）或 absence | RQ2 的负结果 |

### 3.4 缺失部分说明与 A2a 精核入口

当前基于文本的复原中，以下部分需要 A2a 精核：

1. **CPTM 模型图（Fig. 5--Fig. 9）的图形化连线**：Table 21 提供了 C/P/T/M → lifecycle 的文字映射，但图中节点间可能存在跨 step 连线（如一个 challenge 映射到多个 lifecycle step）、虚线/实线区分、颜色编码等，这些在 text 提取中不可见。
2. **Table 1（既有综述比较表）的结构**：文本提取为行列表，但原始 PDF 中可能有合并单元格、多列分组等格式信息。
3. **Zenodo supplementary materials**：原文声明 Zenodo 包含 protocol、included papers + QA scores、raw text/codes、thematic synthesis、TA tables、full CPTM model，这些可作为 A2a 核验的增值来源。
4. **每个 theme 的精确频次**：原文以 "(Freq)" 标记，但在 text 提取中部分 theme 的频率值可能因版面断裂而需要交叉核对。
5. **Definitions themes 内部的频率数据**（Table 6）：21 个 themes 的完整频率表和来源文献列表需逐行核对。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `aspect-definitions` | Definitions（定义） | DevSecOps Primary Dimensions（根） | RQ1 Sub-q 1.1 + §4.1.A | DevSecOps 的定义集合及其来源 | 21 themes，来自 74 codes，来自 28 WL+15 GL definitions | 层级枚举（21 themes） | 无此 aspect 的 primary source 不计入 | 定义共识度、定义来源权威性 | 识别被引用最多的定义（Mohan & Othmane 2016，9次） | Table 5, 6, 7; §4.1.A | 定义层级的 theme/category 分类法是可迁移 schema；具体定义内容不可迁移 |
| `aspect-challenges` | Challenges（挑战） | DevSecOps Primary Dimensions（根） | RQ1 Sub-q 1.1 + §4.1.B | DevSecOps 实施中已知的挑战 | 28 challenges（C01--C28），4 个 categories（OPC 9 / PC 8 / Tech 7 / Business 4） | 层级枚举（28 challenges），含跨 review 验证标记 | 无此 aspect 的 primary source 不计入；Business category GL 无贡献 | 挑战频率排序、category 分布 | OPC 挑战最多（9个），C02 协作障碍最高频 | Tables 8--11; §4.1.B | 挑战→category 的分类框架可迁移；具体挑战内容不可迁移 |
| `aspect-practices` | Practices（实践） | DevSecOps Primary Dimensions（根） | RQ1 Sub-q 1.1 + §4.1.C | DevSecOps 已知的最佳实践与解决方案 | 60 practices（P01--P60），4 个 categories | 层级枚举（60 practices） | 无此 aspect 的 primary source 不计入 | 实践频率排序、category 分布 | P33 自动化最高频（93次），覆盖多 category 的实践分布 | Tables 12--15; §4.1.C | 实践→category 映射模型可迁移 |
| `aspect-tools` | Tools/Technologies（工具/技术） | DevSecOps Primary Dimensions（根） | RQ1 Sub-q 1.1 + §4.1.D | DevSecOps 中使用的工具和技术 | 16 themes → ~18 tool groups（T01--T18），仅 Technology category | 层级枚举（18 tool groups） | 无此 aspect 的 primary source 不计入 | 工具类别分布、GL 贡献偏多 | GL 提供更多工具信息（45 vs 18 WL），学术与实践视角差异 | Table 19; §4.1.D | 工具分类方法可迁移 |
| `aspect-metrics` | Metrics/Measurement（指标/度量） | DevSecOps Primary Dimensions（根） | RQ1 Sub-q 1.1 + §4.1.E | DevSecOps 中使用的度量指标 | 20 metrics（M01--M20），3 个 categories（无 Business 原生贡献） | 层级枚举（20 metrics） | Metrics 面最薄弱（仅 7 WL+13 GL），大量未覆盖；Business 指标全部来自外部补充 | 指标稀缺性识别 | 仅 2 篇 WL 涉及指标，学术界缺乏 DevSecOps metrics 研究 | Tables 16--17; §4.1.E; Table 18（DevOps 对比） | 指标分类框架和缺口模式可迁移 |
| `theme-frequency` | 主题频率 | 各 aspect 下每个 theme | TA coding output（§4.1） | 贡献该 theme 的 primary source 计数 | 非负整数 | 数值 | 频率=0 的 theme 不存在（theme 本身由编码归纳产生） | theme 重要性和关注度的代理指标 | 最受关注的 theme（如 C02、P33）揭示研究热点 | 每个 theme 的 "(Freq)" 标注 + source ID 列表 | 频率统计方法可迁移，具体数值不可迁移 |
| `theme-source-list` | 主题来源文献列表 | 每个 theme | Table 4 + 各 theme 表中的 [Papers contributed to the code] | 贡献该 theme 的 primary source ID 列表 | primary source ID 集合（如 {S1-ACM-01, S1-IEEE-06, ...}） | 关系值 | 无贡献者不出现 | 可审计性和可复现性 | 支持 cross-validation 和 snowballing 追溯 | Table 4 + 每个 theme 表列的 source ID | 来源追溯方法可迁移 |
| `cross-review-validation` | 跨综述验证标记 | 各 challenge/practice/metric theme | §4.1 各节 TA 结果表 | 该 theme 是否与 prior reviews 的发现完全/部分匹配 | 是（asterisked）/ 否（无标记）/ 来自补充（标注来源） | 布尔 + 外部分类法引用 | 无标记 = 本文独有发现或未被 prior reviews 覆盖 | 证据可靠性评估 | 大部分 challenges 被 multiple reviews 验证；部分 practices 为本文独有 | 各表 asterisk 注释 + §4.1 验证叙述 | 跨综述验证方法可迁移 |
| `lifecycle-stage-mapping` | 生命周期阶段映射 | 每个 C/P/T/M theme | §4.1.3 + Table 21（Gartner lifecycle） | 该 theme 在 DevSecOps lifecycle 中对应的阶段 | 10 个 stage（Plan/Create/Verify/Preprod/Release/Prevent/Detect/Respond/Predict/Adapt） | 外部分类法引用（Gartner）+ 一对多关系值 | NA = 该 step 无对应的该类型 theme | CPTM 模型构建、生命周期覆盖分析 | Challenges 集中在 Plan/Create，Practices 覆盖全 lifecycle | Table 20（stage 定义）+ Table 21（映射） | lifecycle 映射方法可迁移 |
| `literature-type` | 文献类型 | 每个 primary source | §3.4 search strategy | primary source 是 white literature 还是 grey literature | WL / GL | 布尔/二值 | 不适用 | WL vs GL 贡献对比 | Business 面全部来自 GL；Tools 面 GL 贡献远超 WL | §4.1 各 aspect 的 WL/GL 分布统计 | 文献类型区分方法可迁移 |
| `qa-score` | 质量评价得分 | 每个 primary source | §3.5 Quality assessment（QA checklist） | primary source 的质量评价得分（0--18） | 0 到 18 的整数 | 数值或区间 | score < 11 的 primary source 被排除 | 研究质量控制和偏倚最小化 | QA threshold（11/18）设定对纳入范围的影响 | §3.5 QA criteria + Zenodo QA scores | QA 方法可迁移，具体 threshold 不可迁移 |
| `gse-coverage` | GSE 覆盖 | RQ2 维度 | §4.2 RQ2 | 该 primary source 是否涉及 Global Software Engineering 情境中的 DevSecOps | Boolean：有 / 无（结论为 absence） | 布尔 | 全 147 primary sources + 126 Search String 2 结果中无覆盖 | RQ2 的负结果发现 | Global DevSecOps 是显著研究空白 | §4.2 + §4.2.1--§4.2.3 | absence finding 的方法学模式可迁移 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `edge-aspect-to-category` | 各 Aspect | 分类归属（classified into） | 各 Category | OPC / PC / Technology / Business 四选一或多选 | Definition 的 category 分布覆盖全部 4 类；Metrics 无原生 Business 贡献 | Table 5; §4.1.A--E | 将扁平 aspect 结构组织为跨 aspect 分类轴 |
| `edge-challenge-to-practice` | 各 Challenge | 应对关系（addressed by） | 各 Practice | Practices 集合（一对多） | 不是所有 challenge 都有 direct practice mapping；原文通过 lifecycle 间接建立关系 | Table 21（CPTM 映射表） | CPTM 模型核心：展示 challenge→practice→tool→metric 链 |
| `edge-practice-to-tool` | 各 Practice | 工具支撑（enabled by） | 各 Tool | Tools 集合（一对多） | 不是所有 practice 都有对应 tool | Table 21 | CPTM 模型 |
| `edge-practice-to-metric` | 各 Practice | 度量关系（measured by） | 各 Metric | Metrics 集合（一对多） | Metrics 整体稀缺，多数 practice 无对应 metric | Table 21 | CPTM 模型 |
| `edge-theme-to-lifecycle` | 各 C/P/T/M theme | 生命周期归属（mapped to） | 各 Lifecycle Stage | 10 个 stage，一对多（一个 theme 可映射到多个 stage） | NA 表示该 stage 无该类型 theme | Table 21 | 将静态分类投影到时序过程 |
| `edge-theme-to-source` | 各 Theme | 证据来源于（derived from） | 各 Primary Source | primary source ID 集合 | 低频 theme = 少 source 支持 | Table 4 + 各 theme 表 source ID 列 | 可追溯性、可复现性 |
| `edge-theme-to-prior-review` | 各 Theme | 跨综述验证（validated by） | 各 Prior Review | {Myrbakken 2017, Akbar 2022, Rajapakse 2022, Prates 2019} | 无标记 = 本文独有 | 各表 asterisk + §4.1 验证叙述 | 证据可靠性评估 |
| `edge-wl-vs-gl` | White Literature | 对比关系（contrasted with） | Grey Literature | WL/GL 对比统计 | 部分 category 仅 GL 贡献 | §4.1 各 aspect WL/GL 分布 | 学术 vs 实践视角差异分析 |

**说明**：原文存在丰富的关系边，但并非传统数据库意义上的关系型 schema。CPTM 模型中的 C→P→T→M 链是通过将四类 theme 同时映射到 lifecycle stage 来实现的**间接关系**，而非显式声明的 challenge→practice 直接映射对。Table 21 是实现这种关系投影的核心接口。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段 / 统计表支持的统计观察（可直接从编码数据中得出）

| # | 统计观察 | 支持证据 | 强度 |
|---|---|---|---|
| SO-1 | DevSecOps 研究集中在 Challenges（126 extracted segments）和 Practices（356 segments），Metrics（20 segments）和 Tools（63 segments）相对较少 | Table 5 extracted data 列 | strong |
| SO-2 | OPC 类别在 Challenges 中占比最高（9/28），反映人员/组织/文化是 DevSecOps 最大障碍 | Table 8 (9 OPC challenges) | strong |
| SO-3 | P33（Automate tools and security processes）是所有 practices 中频率最高的（93 次提及） | Table 14, P33 频率标注 | strong |
| SO-4 | Grey literature 提供了更多的 Tools（45 vs 18 WL）和 Metrics（13 vs 7 WL），但缺少 Business Challenges | §4.1.D, §4.1.E, §4.1.B (Business) | strong |
| SO-5 | 定义"DevSecOps is a necessary expansion to DevOps..."（Mohan & Othmane 2016）被引用最多（9 次） | Table 7 | strong |
| SO-6 | 只有 2 篇 WL 涉及 DevSecOps metrics，学术界在此方面严重缺失 | §4.1.E | strong |
| SO-7 | WL/GL 均无覆盖 Global DevSecOps | §4.2 | strong（作为 absence） |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

| # | 候选 Finding | 原文出处 | 类型 | 对 Paper2 的可迁移性 |
|---|---|---|---|---|
| CF-1 | "The CPTM model provides a breakdown and a broad landscape of DevSecOps, from which researchers and practitioners may select an area of focus" | §6 Conclusion | recommendation | 方法学模式可迁移：如何从编码 schema 构建 landscape model |
| CF-2 | "There is extremely limited literature related to adopting DevSecOps in GSE contexts" → research gap | §4.2.3, §4.4 | gap identification | gap identification 方法可迁移 |
| CF-3 | "Researchers and practitioners have different emphases and strengths...they are complementary" | §4.4 Study implications | comparative finding | WL vs GL 对比框架可迁移 |
| CF-4 | "The SE community needs to be aware of these identified challenges and continue doing research" | §4.1.B | recommendation | 不可迁移（领域特定） |
| CF-5 | "DevSecOps research has been towards the next stage...moving to framework design" | §4.3 | trend observation | 不可迁移（领域特定） |
| CF-6 | 未来方向：Delphi study 验证 CPTM、field study with global vendor、Platform Engineering 的 security 扩展 | §6 | future work | 验证方法学可迁移 |

### 6.3 对 Paper2 可迁移的方法学启发

1. **层级编码框架**：5 aspects × 4 categories → individual themes 的多级编码结构，可用于设计 Paper2 对 primary studies 的 extraction form。
2. **CPTM 式关系投影**：将编码结果通过外部参考框架（如 lifecycle model）进行二次投影以建立跨维度关系，Paper2 可推广为"编码树 → 关系投影"的通用方法。
3. **跨综述验证**：用 prior reviews 的 findings 逐 theme 验证（asterisk 机制），Paper2 可借鉴为证据可靠性分层规则。
4. **WL vs GL 双轨**：学术与实践视角的系统对比，Paper2 在自己的 review 方法学中可引入类似的 dual-source 策略。
5. **Absence 作为 finding**：负结果（GSE 缺失）的系统构建方法，包括 search string 修正、snowballing 复核、confirmatory search 和可能原因的多假设分析。
6. **Confirmatory search 与 statistical pool 的边界管理**：明确哪些数据进入主统计池、哪些仅用于验证。

### 6.4 绝不能迁移的领域结论

- DevSecOps 的 28 个 challenges 的具体内容
- DevSecOps 的 60 个 practices 和 20 个 metrics 的具体枚举
- CPTM 模型中 challenge→practice→tool→metric 的具体映射关系
- "Mohan & Othmane (2016) 的定义被引用 9 次"等具体统计值
- "P33 自动化是最高频 practice" 等具体领域结论

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 总体评估

现有 `review.md` 已经过一轮 `19×3` 修复（见 A.3 中的 `[clm-devsecops-primary-dimensions-a1dt-19x3-repair]`），明确承认了"六叶接口只能作为跨论文投影"的问题。当前 review.md 的 A.1 维度树已包含原文主干的 aspects/categories/CPTM/lifecycle/GSE-gap，方向正确。但仍存在若干需要修正的问题。

### 7.2 C/I/M 分级返修建议

#### C 级（Critical，必须在重写中修复）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| C-1 | review.md §2 中的维度树描述仍以"六个通用 leaf"作为 A1-DT 结构的组织骨架（scope/corpus/classification/method/evidence/finding），而非以原文自身的 aspect→theme→category→lifecycle 结构作为主叙述骨架 | §2.4--§2.8 | **重写 §2**，以原文的 5 aspects → 4 categories → themes → CPTM lifecycle 投影作为主树，将通用六叶降级为附录中的跨论文投影参考。 |
| C-2 | A.1 维度树表（review.md 中的 A.1 节）的 `leaf-devsecops-primary-dimensions-orig-aspect` 等 5 个 candidate leaf 被标记为 `schema_seed`，但它们的取值空间未展开为原文的完整枚举 | A.1 维度树表 | 将每个 aspect leaf 的取值空间展开为原文的完整 theme list（如 Definitions = {21 themes}，Challenges = {C01--C28}），并在"取值空间"列中标注"完整枚举，见原文 Tables 6--19"。 |
| C-3 | 叶子维度表缺少频率字段、source ID 追溯字段和跨综述验证标记字段 | 叶子维度表 | 新增 `theme-frequency`（频率）、`theme-source-list`（来源文献）、`cross-review-validation`（跨综述验证标记）三个叶子维度。 |
| C-4 | 关系边表（A.1 中 `edge-devsecops-primary-dimensions-method-evidence`）将"方法/技术节点与评价/证据节点之间存在可审计关系"写为关系边，但未列出 CPTM 模型中的 challenge→practice→tool→metric→lifecycle 投影关系 | A.1 关系边表 | 新增 `edge-challenge-to-practice`、`edge-practice-to-tool`、`edge-theme-to-lifecycle` 等关系边，以 Table 21 为证据锚点。 |

#### I 级（Important，应在本次修复中完成）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| I-1 | review.md 宣称"本轮未逐图 PDF 细核 Fig. 5--9 的连线细节"，但未给出明确的人工核验清单 | §1 快速结论卡片 | 补充 PDF 核验清单，列出 Fig. 5--9、Table 1--21 的具体校核项。 |
| I-2 | review.md 未明确区分"本文作为 secondary study 的样本库"和"本文研究的 primary sources 的样本库"这两个层次 | §2 全文内容详读 | 在 §2 中显式说明：本文的 sample 是 147 primary sources；本文本身是一个 tertiary source；Paper2 如果要统计，应统计本文的维度树结构（methodology level），而非 primary sources 的领域统计值（domain level）。 |
| I-3 | review.md 的 SUMMARY 表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"字段需要修正 | SUMMARY 表 | 样本单位应为"147 primary sources (104 WL + 43 GL)"；样本数量为 147；原生树类型应为"维度森林（aspects→themes + CPTM lifecycle 投影）"；统计池资格应为"局部可统计（频率统计有效但跨 aspect 分母非独立；Metrics 面薄弱；确认性搜索 20 篇未入池）"。 |
| I-4 | 缺少 Zenodo supplementary materials 的证据引用 | 全局 | 在所有涉及 QA scores、raw codes、thematic synthesis 的证据锚点中，补充 Zenodo DOI（10.5281/zenodo.7959584）。 |
| I-5 | review.md 中 evidence 锚点 EV-devsecops-primary-dimensions-005（"原文 Table 21 提供 C/P/T/M 映射表"）的强度被标记为 weak | A.2 证据账本 | Table 21 是原文的核心 CPTM 映射表，应升为 moderate 或 strong。 |

#### M 级（Minor，可记录为 follow-up）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| M-1 | review.md 的 A.2/A.3 缺少 CPTM 模型映射到每个 lifecycle stage 的频率计数统计 | A.2/A.3 | 可补充"Plan stage 含 10 challenges、17 practices、3 tools、5 metrics"等汇总观察。 |
| M-2 | review.md 未提及原文 §4.3 confirmatory search 作为统计池边界管理的优秀实践 | §2 | 在方法学启发部分补充 confirmatory search / statistical pool boundary 作为一种审计方法。 |
| M-3 | review.md 中 A.4 的视觉检查项仅有 `needs_manual_check`，缺少具体执行步骤 | A.4 | 补充具体核验步骤：打开 PDF → 核对 Fig. 5--9 连线 → 核对 Table 21 映射 → 核对各表频率值 → 记录差异。 |

### 7.3 是否需要重写"维度树复原"

**是。** §2.4--§2.8 应完全重写，以原文的 5 aspects → 4 categories → themes → CPTM lifecycle 作为主叙述线。当前以通用六叶为骨架的写法混淆了"本文原生 schema"和"跨论文投影模板"的层次。

### 7.4 SUMMARY 表当前字段修正

| 字段 | 当前值 | 建议修正值 |
|---|---|---|
| 样本单位 | 模糊（未显式声明） | "147 primary sources (104 WL + 43 GL)" |
| 样本数量 | 未明确 | "147（主 MLR 池）+ 20（confirmatory search，未入 TA/CPTM）" |
| 原生树类型 | 似为"单树" | "维度森林（Aspects→Themes 编码树 + CPTM Lifecycle 关系投影）" |
| 统计池资格 | 未明确标注 | "局部可统计：频率统计有效，跨 aspect 分母非独立；Metrics 面 20 entries 薄弱；GSE 维度为 absence" |

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-v2-001 | paper_content.txt | §1 Introduction | "identifying five major aspects of DevSecOps (Definitions, Challenges, Practices, Tools/Technologies, and Metrics/Measurement)" | 五大 aspect 的完整枚举 | 维度树根节点定义 | strong | `aspect-definitions` 等 5 个 aspect 叶子 | 否 | 不可迁移具体 aspect 枚举 |
| EV-v2-002 | paper_content.txt | §3.1--§3.5 Method | "dual-track strategy including white (104 studies) and grey (43 studies) literature from 2012 to 2021" + inclusion/exclusion criteria + QA checklist | MLR 流程完整描述，含纳排标准和质量评价 | 样本单位定义、纳入标准、质量门控 | strong | 所有叶子维度的数据来源合法性 | 否（QA scores 需 Zenodo 核验） | 不可迁移纳排标准 |
| EV-v2-003 | paper_content.txt | §3.6 Replication and snowballing | Table 2: "Number of overlapping and non overlapping papers" + 6 个 secondary studies 的验证 | 与 Mohan 2016, Myrbakken 2017, Prates 2019, Sanchez-Gordon 2020, Akbar 2022, Rajapakse 2022 的 primary study overlap 统计 | 跨综述验证方法证据 | moderate（Table 2 数据需 PDF 核验） | `cross-review-validation` 叶子 | 需 PDF 核验 Table 2 | 不可迁移 overlap 数值 |
| EV-v2-004 | paper_content.txt | §4.1 + Table 5 | "Table 5: Thematic analysis and synthesis results" + extracted data 数量、codes 数量、themes 数量 | 各 aspect 的 TA 编码过程量化统计 | 编码过程与输出规模证据 | strong | 所有 aspect→theme→category 路径 | Table 5 数字需 PDF 核验 | 不可迁移具体数字 |
| EV-v2-005 | paper_content.txt | §4.1.A--§4.1.E | Tables 6--19 的完整 theme 表，含 theme 名称、频率、contributing papers 列表 | 21 definitions themes, 28 challenges, 60 practices, 16 tool themes, 20 metrics 的完整枚举 | 叶子字段取值空间来源 | strong | 所有 theme 叶子 | Tables 6--19 的频率值和 source ID 需 PDF 逐表核对 | 不可迁移具体 theme 枚举和频率 |
| EV-v2-006 | paper_content.txt | §4.1.3 + Table 20--21 + Fig. 5--9 | "Table 21 maps our identified themes to these steps" + CPTM model figures | C/P/T/M 到 Gartner 10-stage lifecycle 的完整映射 | 关系边（跨维度投影）来源 | strong（文字部分）；待 PDF 核验（图部分） | 所有 `edge-*` 关系边 | Fig. 5--9 需 PDF 视觉核验 | 不可迁移具体映射关系 |
| EV-v2-007 | paper_content.txt | §4.2--§4.2.3 | "the results report a notable absence of the global dimension in the white and grey literature" + 四种可能解释 | RQ2 负结果：无 Global DevSecOps 文献 | GSE absence finding 证据 | strong（作为 absence） | `gse-coverage` 叶子 | 否 | absence finding 方法可迁移，领域结论不可迁移 |
| EV-v2-008 | paper_content.txt | §4.3 Confirmatory search | "2022, 13 academic papers and 7 grey articles have been newly included...were not taken into the thematic analysis, and were not integrated in the final CPTM model" | Confirmatory search 边界说明 | 统计池边界证据 | strong | 所有统计用途叶子的 domain boundary | 否 | 不可迁移边界设定 |
| EV-v2-009 | paper_content.txt | §4.4 Study implications | "researchers could learn about the detailed implementation...practitioners could refer to the CPTM model as a road map" | 研究与实践启示 | 候选 finding 来源 | moderate | CF-1, CF-3 等候选 finding | 否 | 不可迁移具体启示内容 |
| EV-v2-010 | paper_content.txt | §5 Threats to validity | 四类威胁及其缓解策略 | 方法论自评 | 方法论可靠性证据 | moderate | 所有结论的强度校准 | 否 | 不可迁移具体威胁评估 |
| EV-v2-011 | paper_content.txt | Appendix A.1--A.3 | 完整的纳入文献目录（S1-ACM-*, S1-IEEE-*, S1-SC-*, S1-GL-*, S2-*, CS-*）+ 追加文献 | primary source 完整列表 | 可复现性证据 | strong | 所有 `theme-source-list` 的可追溯性 | 否 | 不可迁移具体文献列表 |
| EV-v2-012 | Zenodo | doi:10.5281/zenodo.7959584 | [未直接访问] protocol, included papers + QA scores, raw text/codes, thematic synthesis, TA tables, full CPTM model | 开放科学补充材料 | 全部编码过程的可复现性锚点 | 待核验（未访问 Zenodo） | QA scores, raw codes, 完整 CPTM | 需要单独访问 Zenodo 核验 | 不可迁移 Zenodo 内容 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CL-v2-001 | 本文原生维度树为 5 aspects × 4 categories 的编码框架 + CPTM lifecycle 关系投影的维度森林 | 事实陈述 | 所有 aspect/category/theme 叶子 + 所有关系边 | EV-v2-001, EV-v2-002, EV-v2-004, EV-v2-005, EV-v2-006 | strong | 作为 Paper2 维度树 schema seed 和编码方法论先验 | 不可将具体 theme 枚举视为 Paper2 的叶子字段 |
| CL-v2-002 | 本文样本单位为 147 primary sources (104 WL + 43 GL) | 事实陈述 | 所有 theme→source 叶子 | EV-v2-002, EV-v2-008, EV-v2-011 | strong | 定义统计池边界 | Confirmatory search 的 20 篇不在此池内 |
| CL-v2-003 | 本文可作为 Paper2 统计池的一部分（局部统计） | 方法学判定 | 主统计池资格 | EV-v2-002, EV-v2-008 | moderate | 跨论文频率统计的合法输入 | 跨 aspect 分母非独立；Metrics 面薄弱；仅作为 tertiary source 的方法学参考 |
| CL-v2-004 | CPTM 模型中的 C→P→T→M→Lifecycle 投影是可迁移的关系建模方法 | 方法学启发 | `edge-theme-to-lifecycle` + `edge-challenge-to-practice` 等 | EV-v2-006 | moderate | 设计 Paper2 中的跨字段关系边 | 具体映射内容不可迁移；关系类型（生命周期投影/应对关系/支撑关系）可迁移 |
| CL-v2-005 | 跨综述验证（asterisk 机制）是可迁移的证据可靠性分层方法 | 方法学启发 | `cross-review-validation` 叶子 | EV-v2-003, EV-v2-005 | moderate | Paper2 对跨论文合成结果的可靠性评级 | 不可迁移具体验证结果 |
| CL-v2-006 | "Global DevSecOps is an unexplored area" 是可迁移的 absence finding 构建模式 | 方法学启发 | `gse-coverage` 叶子 | EV-v2-007 | moderate | Paper2 中处理负结果/研究空白的模板 | 不可迁移具体领域结论 |
| CL-v2-007 | 现有 review.md 的通用六叶结构混淆了本文原生 schema 与跨论文投影模板 | 审计判定 | review.md §2 的叙述结构 | 本报告全文阅读结果 + review.md 对比 | strong | 本次返修行动的触发依据 | 需经主线程 A2a 精核确认本文叶子无误后方可重写 review.md |
| CL-v2-008 | 本文对 Paper2 的最高价值是方法论模式（编码框架设计、关系投影、跨综述验证、统计池边界管理），而非领域内容 | 迁移边界声明 | 全部迁移边界列 | 全部 12 个证据锚点 | strong | 指导 Paper2 对本文的使用方式 | 任何将具体 DevSecOps 领域 finding 直接写入 Paper2 或统计表的行为都应阻止 |

---

## 9. 技能使用与自我审查记录

### 9.1 读取的技能文件

| 文件 | 读取状态 | 采用的原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | ✅ 完整 | Claim-evidence engineering 原则：所有 strong claim 必须绑定证据；gates（evidence gate / citation gate）用于质量把关；reviewer mode 的 Reviewer gate 作为返修驱动。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | ✅ 完整 | 通用 reviewer 审查维度（originality/quality/clarity/significance/reproducibility/ethics）；constructive specificity 标准；rebuttal-aware writing。本任务中将这些维度转用于"审计 paper 本身的方法学质量"而非"评判 paper 的发表价值"。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | ✅ 完整 | Five-dimension review（contribution/writing clarity/experimental strength/evaluation completeness/method soundness/responsibility）；claim audit 和 evidence gap 分析；风险分级。本任务中用于评估 review.md 的返修优先级（C/I/M 分级）和写作审计。 |
| `research-planning/SKILL.md` | ✅ 完整 | 4-stage planning（overall plan / architecture / logic design / configuration）；task dependency；risk flagging。本任务中用于理解 Paper2 维度树设计的 plan→implement→validate 路径。 |
| `research-planning/references/planning-prompts.md` | ✅ 完整 | Paper2Code 的 structured planning 方法；AI-Researcher 的 plan agent 结构。间接用于理解本审计任务的结构化输出要求。 |
| `research-planning/references/output-schemas.md` | ✅ 完整 | 结构化输出模板（research plan schema, Mermaid diagrams）。本任务中参考其 JSON 结构化输出思路来设计维度树、叶子维度表、关系边表的格式。 |
| `autoresearch/SKILL.md` | ✅ 完整 | Validator-gated 完成判定原则（completion is artifact-gated，不因模型说"done"就停）；状态持久化原则。本任务中借鉴其"审计必须到达 artifact-gated 完成"的哲学，确保本报告是自包含完整制品。 |

### 9.2 本输出最高风险的 3 点及主线程合并时复核建议

| # | 风险 | 严重度 | 复核建议 |
|---|---|---|
| R-1 | **CPTM 模型图（Fig. 5--9）的连线和结构未经 PDF 视觉核验**。Table 21 提供了文字映射，但图形中可能存在未在 table 中体现的跨 lifecycle step 连线、方向标注或层级分组。如果图形与 Table 21 不完全一致，当前基于 Table 21 的关系边复原可能不完整。 | 高 | 主线程合并时：(1) 人工打开 PDF 逐图核对 Fig. 5--9 与 Table 21 的一致性；(2) 如发现图形中有额外连线或节点，补充到关系边表和 CPTM 投影中；(3) 检查 Zenodo 中的 full CPTM model 是否提供更细粒度的映射。 |
| R-2 | **Tables 6--19 中的频率值和 source ID 列表来自 text 提取，未经 PDF 版面核对**。`paper_content.txt` 通过文字模式提取，在大型表格（如 Table 14 跨多页的 Practices/Technology 表）中可能存在断行、合并不全或频率标注错位。如果频率值有误，基于频率的统计观察（SO-1--SO-7）可能需要修正。 | 中 | 主线程合并时：随机抽样 5--8 个 theme，人工核对 PDF 原表与 text 提取的频率值和 source ID 列表。如发现 2 个及以上差异，全量复核 Tables 6--19。 |
| R-3 | **Zenodo supplementary materials 未访问**。原文声明 Zenodo 包含 protocol、included papers + QA scores、raw text/codes、thematic synthesis、TA tables 和 full CPTM model。如果 Zenodo 中的 full CPTM model 提供了比 Table 21 更细粒度的 C→P→T→M 一对一映射，当前的关系边表可能是不完整的投影。 | 中 | 主线程合并时：(1) 访问 Zenodo DOI 检查文件清单；(2) 如有 full CPTM model（如 JSON/CSV/表格），复核其粒度是否比 Table 21 更细；(3) 如有 raw codes，核对本文的 sample→code→theme 映射是否可追溯。 |

### 9.3 任务状态

- **blocked**：否
- **timeout**：否
- **文件缺失**：无。所有必读文件均已成功读取。
- **未访问的补充材料**：Zenodo（doi:10.5281/zenodo.7959584）、paper.pdf（未做视觉版面核验）。
- **降级项目**：3 项（Fig. 5--9 视觉核验、Tables 6--19 频率值 PDF 核对、Zenodo 访问），均已在相应位置标注 `needs_manual_check` 或 `待核验`。

---

**审计完成。**本报告为自包含完整制品，可直接用于主线程重写 `review.md` 及更新 SUMMARY 表。建议主线程先完成上述三项 PDF/Zenodo 核验后，再基于本报告的叶子维度表和关系边表执行 review.md 的 C/I 级返修。