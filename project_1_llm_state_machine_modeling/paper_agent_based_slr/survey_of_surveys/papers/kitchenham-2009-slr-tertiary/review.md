# Systematic literature reviews in software engineering – A systematic literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic literature reviews in software engineering – A systematic literature review |
| 年份 | 2009 |
| 类型 | tertiary-like SLR / SE SLR 状态综述 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 对 SE SLR 的三级/二级综述；文中自称 review of SLRs / tertiary study |
| SE 子领域 | EBSE / SE 二级研究方法学 |
| A1 角色 | 提供 RQ、搜索范围、纳排、质量评价、数据抽取、数据分析、limitations 都较清晰的 tertiary-study 样例。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 历史观察 | 无硬缺口；但 quality score 数值需 原文图表级核对后才能进入正式统计。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖活动规模、主题分布、研究者 / 机构、当前研究限制；属于“领域现状 + 局限”组合。 | `paper_content.txt` Page 2 lines around RQ1--RQ4。 | 可迁移到 Paper2 的 research finding：不仅统计数量，还问主题覆盖与限制。 | 早期 EBSE 样本，不能代表近年 SE/LLM4SE 综述 RQ 全貌。 |
| dimension pattern | 抽取范围包括 search venues、纳排标准、quality assessment、data collection、data analysis、deviation from protocol。 | `paper_content.txt` Page 1 contents；Page 2--3 Method。 | 可迁移为 survey-of-surveys review 表字段。 | 字段反映早期 SLR 生态，现代开放科学字段需 A2a 补充。 |
| finding pattern | 从数量、主题、组织、限制和实践影响形成 findings；结论指出主题覆盖有限、部分 SLR 可为实践提供指南。 | `paper_content.txt` Page 1 abstract；Page 7--8 discussion/conclusion。 | 可迁移为“统计观察 → 研究发现”的桥接模板。 | 只作为“统计到发现”的模板，不能迁移具体领域结论。 |
| evidence presentation pattern | 用 manual search 分母、search results、quality evaluation、quality factors 支撑结论。 | `paper_content.txt` Page 1 abstract；Page 3--5 results。 | 可迁移为字段证据与统计表结构。 | 质量评价和搜索分母可迁移，具体指标需现代样本校准。 |
| validity / threat pattern | 单列 limitations of study，包含搜索范围、术语历史和 protocol deviation。 | `paper_content.txt` Page 1 contents；Page 7 limitations。 | 可迁移到 Paper2 的效度威胁章节。 | 早期 threat 口径可能不足以覆盖 LLM 辅助综述风险。 |
| report structure pattern | 标准结构：Introduction → Method → Results → Discussion → Conclusions，并将每个 RQ 映射到 discussion 小节。 | `paper_content.txt` Page 1 contents。 | 高度可迁移。 | 结构可参考，但后续必须加入人机协同与审计制品链部分。 |

## 3. 对 PR-A1 schema 的启发

1. `RQ pattern` 应允许“规模 / 主题 / 主体 / 局限”四类组合，不只允许 PICO 式技术效果问题。
2. `finding pattern` 需要区分统计观察和可行动结论，例如“SLR 数量增加”与“需要更好实践指导”。
3. `evidence presentation pattern` 应要求每个 finding 对应搜索范围、筛选分母、质量评价或 data extraction 字段。
4. `validity pattern` 需要记录 protocol deviation，而不是只列外部效度。

## 4. 待复核

- Table / quality score 数值正式使用前需回原文核对。
- 该文是早期 SE tertiary study；A2a/A2b 需要补近年样本，避免 pattern 过拟合早期 EBSE。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 把 SE SLR 自身作为研究对象，适合作为 tertiary-like scope 样本。 | 可迁移“二次研究的二次研究”元模型。 |
| A1-M1 语料收集与纳排 | 提供早期 SE SLR 的检索、纳排和质量评价过程。 | 可作为历史 baseline；不代表现代检索生态。 |
| A1-M2 研究对象与主题语义 | 提供早期 SE SLR topic / quality / reporting 分类。 | 可迁移分类方式，不迁移领域覆盖结论。 |
| A1-M3 方法 / 技术 / 干预 | 主要是综述方法和主题分类，不是技术干预 taxonomy。 | 对 A1-M3 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 强调 reporting quality、search bias、质量评价等证据呈现。 | 可迁移到 validity / audit 字段。 |
| A1-M5 统计分析就绪 | 可形成 review 数量、主题、质量等统计观察。 | 分母年代久远；需标注历史边界。 |
| A1-M6 research finding 形成与裁决 | 从早期 SE SLR 质量问题形成方法学改进建议。 | 可迁移 finding 写法，不迁移 2009 年状态结论。 |

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/kitchenham-2009-slr-tertiary__codex.md](../../audits/a1dt-v2-19x3/results/kitchenham-2009-slr-tertiary__codex.md)、[../../audits/a1dt-v2-19x3/results/kitchenham-2009-slr-tertiary__claude.md](../../audits/a1dt-v2-19x3/results/kitchenham-2009-slr-tertiary__claude.md)、[../../audits/a1dt-v2-19x3/results/kitchenham-2009-slr-tertiary__deepseek.md](../../audits/a1dt-v2-19x3/results/kitchenham-2009-slr-tertiary__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/kitchenham-2009-slr-tertiary.md](../../audits/a1dt-v2-19x3/adjudications/kitchenham-2009-slr-tertiary.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `kitchenham-2009-slr-tertiary` |
| 审计代理 | `claude` (Opus 4.7, 1M context) |
| 是否已读 `paper_content.txt` | 是；通读 962 行全文（覆盖 Abstract、§1--§5、Tables 1--5、Tables A1--A3、References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；元信息与 review.md 已交叉核对 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅 text-level 审计；表格 / 公式版式留待 A2a 视觉核验 |
| 原文类型 | tertiary SLR（作者自称 "tertiary literature review"，§2 Method 开头） |
| 被编码样本单位 | 二次研究（系统文献综述 或 元分析（meta-analysis） 论文，每条对应一篇 SLR/MA） |
| 样本数量 / 分母 | 主样本 `N=20`（S1--S20，§4.1 与 Table 2）；候选漏斗分母 `2506`（Table A1 Total），相关候选 `33`，最终选入 `19+2=20`（其中 1 篇通过研究者询问 + 1 篇通过 Simula 网站补入） |
| 原生树类型 | **单树为主 + 双子树并列**：主树为「20 篇 SLR 的抽取编码表」（§2.5 数据抽取项 + Table 2 列），并列子树为「DARE 质量评价 rubric」（§2.4 QA1--QA4 + Table 3） |
| 主统计池资格 | 后续主统计池候选；A1-DT v2 当前仍按模式种子管理，A2a 精核前不进入定量统计。原文内部可统计字段与分母见“维度树复原”和 [evidence_chain.md](./evidence_chain.md) 的 A.2/A.3。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

本轮已读取：

- `bibtex.bib`、`metadata.json`：用于锁定元信息（IST 2009, vol 51, no 1, 7--15, DOI 10.1016/j.infsof.2008.09.009）。
- `paper_content.txt`（行 1--962）：全文文本通读，包括摘要、§1 Introduction、§2 Method（含 §2.1--§2.7 七小节）、§3 Results（§3.1--§3.3）、§4 Discussion（§4.1--§4.5）、§5 Conclusions、Acknowledgements、Tables 1--5、Tables A1--A3（Appendix 1）、References [1]--[42]。
- `review.md`：现有审计版本，含 v1 历史 19×3 审计入口标注。

未独立打开 `paper.pdf`：表格 / 图版式、QA 分数复核、上下标和特殊字符（如 "\C2112008"、"\C15"、"\C14" OCR 残留）建议在 A2a 阶段对照 PDF 视觉核验。

**5--12 个关键证据锚点**：

| # | 锚点 | 位置 | 短引 / 释义 |
|---|---|---|---|
| E01 | 研究目的与对象 | §1 Introduction, paper_content L88--97 | "The purpose of this 研究 is to review the current status of EBSE since 2004 using a tertiary 研究 to review articles related to EBSE and, in particular, we concentrate on articles describing 系统文献综述 (SLRs)." |
| E02 | RQ 树（4 主 RQ + 4 子 RQ） | §2.1, L105--141 | RQ1 SLR 活动量；RQ2 主题；RQ3 主导者；RQ4 限制；RQ4 细分为 RQ4.1--RQ4.4 |
| E03 | 来源清单 | Table 1, L161--177 | 10 期刊 + 4 会议（IST/JSS/TSE/IEEE SW/CACM/ACM Sur/TOSEM/SPE/EMSE/IET SW + ICSE/Metrics/ISESE） |
| E04 | 纳排标准 | §2.3, L186--203 | 纳入：SLR 与 MA（含部分章节为 SLR 的论文）；排除：非正式文献综述、讨论 EBSE/SLR 流程的论文、重复报告 |
| E05 | DARE 质量评价 rubric | §2.4, L204--234 | QA1--QA4 + Y/P/N + 计分 Y=1, P=0.5, N=0, 未知 |
| E06 | **数据抽取字段清单**（关键） | §2.5 数据收集（Data collection）, L243--258 | 10 项明示抽取字段（详见 §3 节叶子表） |
| E07 | 主样本编码表 | Table 2, L335--389 | 20 条 S1--S20，每条 8 列：ID/Author/Date/主题类型（主题类型）/Topic area/Article type/Refs/Include 实践者指南/Num. 原始研究 |
| E08 | 质量评分明细表 | Table 3, L465--489 | 20 条 × QA1--QA4 + Total score + Initial rater agreement |
| E09 | 检索漏斗表 | Table A1, L589--633 | 13 来源 × 4 年 × {Total/Relevant/Selected}；总数 2506→33 相关→19 选入 |
| E10 | 排除候选表 | Table A2, L694--739 | 14 条被排除论文及原因（多为 "Informal literature survey"） |
| E11 | 作者机构 / 国家表 | Table A3, L750--810 | 20 条研究的作者-机构-国家映射 |
| E12 | Protocol deviations | §2.7 + §4.5, L284--295, L639--680 | 4 项偏离声明：搜索范围限制、单人选样、单人抽取-单人核对、术语年代说明 |

### 2. 样本单位与字段来源判定

1. **原文纳入的对象**：peer-reviewed articles 形态的 SLR 与 MA（含其中 SLR 只是文章一部分的情况）。具体单位是「一篇 二次研究」，最终落地为 `S1--S20` 共 20 条编码记录（其中 `S3` = Galin & Avrahami 是 MA，其余 19 条是 SLR）。
2. **作者是否做了系统检索 / 纳排 / 数据抽取 / 编码**：**是**，且高度规范化：
   - 检索：手工 + 10 期刊 + 4 会议 + 个人/网站补检索（§2.2）
   - 纳排：显式标准 + 跨研究者复核（§2.3）
   - 质量评价：DARE 标准 + 双人独立评分 + 分歧讨论（§2.4）
   - 数据抽取：10 项字段 + 单抽取 + 单核对（§2.5）
   - 数据分析：8 个分析维度对应到 RQ1--RQ4.4（§2.6）
3. **字段来源**：本论文的「维度树」由 §2.5 的 10 项抽取字段 + §2.4 的 DARE rubric + Tables 2/3/A1/A2/A3 的列结构共同构成。**这是一份已公开、已操作化、已应用的 抽取 form**，不是 reviewer 重构的 模式。
4. **RQ 与样本单位的关系**：RQ 既是树根的用途锚点，也决定字段抽取的取舍。RQ1↔︎`年份/来源/Refs`；RQ2↔︎`主题类型（主题类型）/Topic area`；RQ3↔︎`Author/Institution/Country`；RQ4↔︎`Quality score/Num 原始研究（原始研究）/Include 实践者（practitioner） 指南`。
5. **若无系统样本库则降级**：不适用——本文恰是「无降级」典范。

### 3. 原生样本编码维度树

> 中文化导读：本维度树描述的是早期软件工程系统综述的三级综述如何编码二次研究。树的核心不是某个工具或模型，而是“二次研究样本—质量评价—检索漏斗—作者机构—主题范围”的证据链。保留 IST、JSS、TSE、ICSE、DARE、SLR 等英文缩写，是为了让读者能回到原文表格和软件工程证据实践传统；中文节点名才是后续 Paper2 维度模式的主要依据。可迁移的是分母链、质量评价、主题与作者/机构分布的组织方式，不是 2009 年的领域状态结论。

#### 3.1 主树：20 篇 二次研究 的抽取编码表

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[根节点] 2004–2007 上半年 SE 二次研究（SLR 或 MA；N=20）
├── L1 书目信息 / 来源
│   ├── L1.1 来源类型：期刊（journal）或会议（conference）；具体发表源包括 IST、JSS、TSE、IEEE SW、CACM、EMSE、ICSE、ISESE、Metrics 等
│   ├── L1.2 完整引用：自由文本 + DOI
│   ├── L1.3 日期：2004..2007；允许 duplicated version 的 “2005&2006”
│   └── L1.4 文章类型标记：{SLR, MA}
├── L2 研究分类（§2.5 “分类 of the 研究”）
│   ├── L2.1 类型：{SLR, MA}
│   ├── L2.2 范围 / 主题类型（主题类型）：{研究趋势（研究趋势）, 技术评价（technology evaluation）}
│   └── L2.3 主题领域：开放枚举；包括 成本估算（cost estimation）、单元测试（unit testing）、捕获-再捕获（capture-recapture）、Web 研究（web research）、软件工程实验（SE experiments）、商用现成软件（COTS）、能力成熟度模型（CMM）、软件架构评价（software architecture 评价）、测试方法（testing 方法）、ICSE 经验研究（empirical studies in ICSE）、CS/IS/SE trends 等
├── L3 作者与机构
│   ├── L3.1 作者：姓名列表
│   ├── L3.2 机构：开放枚举，见 Table A3
│   └── L3.3 机构国家：{挪威（Norway）, 英国（UK）, 美国（USA）, 巴西（Brazil）, 以色列（Israel）, 西班牙（Spain）, 新西兰（NZ）, 瑞典（Sweden）, 意大利（Italy）, 加拿大（Canada）, 澳大利亚（Australia）}
├── L4 内容摘要
│   ├── L4.1 研究摘要：RQ + answers 的自由文本；见 Supplementary Appendix 3
│   └── L4.2 研究问题 / 议题：自由文本
├── L5 质量：见下方 DARE 质量评价子树
├── L6 EBSE / 指南引用
│   └── 是否引用 EBSE / 指南（guidelines）：{指南技术报告（Guideline TR）, EBSE 论文（EBSE paper）, 否}
├── L7 实践影响
│   └── 是否包含面向 实践者 的指南：{是, 否, 是*}
└── L8 原始研究数量
    └── 每篇 SLR 纳入的 原始研究 数：整数；观察范围 6..1485
```

#### 3.2 子树：DARE 质量评价 rubric

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[子根节点] DARE 质量评价（按研究条目）
├── QA1 纳排标准是否描述且合适：{是（Y）=1, 部分（P）=0.5, 否（N）=0, 未知}
├── QA2 检索是否可能覆盖所有相关研究：{是（Y）=1, 部分（P）=0.5, 否（N）=0, 未知}
├── QA3 是否评价纳入研究的质量 / 有效性：{是（Y）=1, 部分（P）=0.5, 否（N）=0, 未知}
├── QA4 基础数据 / 研究是否充分描述：{是（Y）=1, 部分（P）=0.5, 否（N）=0, 未知}
├── QA-total 总分：0..4 浮点数；观察范围 1..4
└── QA-agreement 初始评审一致性：0..4 整数，对应 4 个问题中的一致项数
```

#### 3.3 辅助：检索漏斗子树（Table A1）

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[漏斗] 检索漏斗（按来源 × 年份）
├── F.1 总文章数：整数；总和 2506
├── F.2 相关条目：通过标题 / 摘要初筛的整数；总和 33
└── F.3 入选条目：通过纳入标准的整数；总和 19；另有 2 篇由外部线索补入，最终 N=20
```

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现 用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-orig-source | 来源（期刊/会议） | L1.1 | §2.5 抽取项 1；Table 2 | 论文发表的期刊或会议简称 | IST, JSS, TSE, IEEE SW, CACM, ACM Sur, TOSEM, SPE, EMSE, IET SW, ICSE, Metrics, ISESE + "Conf+期刊" 组合 | 封闭枚举（受 Table 1 限定） | 跨期刊/会议时记为 `Conf+期刊` 双值 | 已用于 §4.1 的来源分布统计 | "IST 鼓励 SLR 失败" 候选 | E03, E07 | 仅适用于 2004--2007 SE 期刊会议；不可外推现代 OA 期刊 |
| leaf-orig-year | 发表年份 | L1.3 | Table 2 col "Date" | 论文发表年份（重复版本写双年） | 2004 / 2005 / 2006 / 2007 / "2005&2006" | 数值 + 关系值（双版本） | 单一年值即可 | 已用于 Table 4 年×质量分均值 | "每年 SLR 数量稳定" 候选 | E07 | 时间窗外不适用 |
| leaf-orig-article-type | 文献类型 | L2.1 | §2.5；Table 2 col "Article type" | 二次研究 子类型 | SLR / MA | 完整枚举 | 必填 | 已用于 §4.1 「19 SLR + 1 MA」 | -- | E07 | 现代分类可能区分 SMS / MLR / rapid review |
| leaf-orig-scope | 研究范围类型 | L2.2 | §2.5；Table 2 col "主题类型（主题类型）" | 研究意图分类 | 研究趋势（研究趋势） / 技术评价（technology evaluation） | 完整枚举 | 必填 | §4.1 "12 tech vs 8 trends" | RQ4.1 限制候选 | E07 | -- |
| leaf-orig-topic-area | 主题领域 | L2.3 | Table 2 col "Topic area" | SE 子领域主题 | 开放枚举：成本估算（Cost estimation）/ 单元测试（Unit testing）/ 捕获-再捕获（Capture-recapture）/ Web 研究（Web research）/ SE 实验（SE experiments）/ 商用现成软件（COTS）/ 能力成熟度模型（CMM）/ 软件架构评价（SW architecture eval）/ 测试方法（测试 方法）/ ICSE 经验研究（Empirical studies in ICSE）/ CS-IS-SE 比较（Comparative CS-IS-SE）/ 计算机科学研究（Computer science research） | 层级开放枚举 | 必填 | §4.2 主题分布；"7 cost estimation, 3 experiments, 3 testing" | "主题覆盖窄" 候选发现 | E07 | 不可视为饱和分类；A2a 应核验 §4.2 出现的 12 个具体主题 |
| leaf-orig-author | 作者 | L3.1 | Table A3 | 作者姓名列表 | 自由文本（人名列表） | 自由文本 | -- | §4.3 "Jørgensen 5 篇, Sjøberg 3 篇" | RQ3 候选 | E11 | 仅适用 EBSE 早期社群 |
| leaf-orig-institution | 机构 | L3.2 | Table A3 | 作者所属机构 | 开放枚举：Simula Research Lab / Keele Univ / Brunel Univ / Lund Univ / Univ Auckland / Politécnica Madrid / NTNU / Indiana Univ / Univ Calgary / NICTA / 等 | 开放枚举 | 多机构时拆行 | §4.3 "Simula 主导 8 篇" | "Simula 数据库策略有效" 候选 | E11 | -- |
| leaf-orig-country | 国家 | L3.3 | Table A3 | 机构所在国家 | 开放枚举：Norway / UK / USA / Brazil / Israel / Spain / NZ / Sweden / Italy / Canada / Australia | 开放枚举 | 多国时拆行 | §4.3 "European 14 篇 vs N.American 4 篇" | RQ3 主导地区候选 | E11 | -- |
| leaf-orig-refs-ebse | EBSE/Guidelines 引用 | L6.1 | §2.5；Table 2 col "Refs" | 是否引用 EBSE 论文 [23,5] 或 Guidelines [22] | 指南技术报告（Guideline TR） / EBSE 论文（EBSE paper） / 否 | 完整枚举 | "否" 表示均未引用 | §4.1 "8 引用 Guidelines, 2 引用 EBSE" | "EBSE 浸润度" 候选 | E07 | -- |
| leaf-orig-实践者-指南 | 实践者指南 | L7.1 | §2.5；Table 2 col | 是否提供面向实践者的指南 | 是 / 否 / 是\* (S17 footnote: 暗示但未显式) | 完整枚举 + 限定值 | "否" 默认 | §4.4 "12 tech 中 4 篇有指南" | RQ4.4 候选 | E07 | -- |
| leaf-orig-num-primary | 一级研究数量 | L8.1 | §2.5；Table 2 末列 | 该 SLR/MA 纳入的一级研究篇数 | 整数；观察范围 6..1485 | 数值 | 必填 | §4.4 "trends 63--1485 vs tech 6--54" | RQ4.2 候选 | E07 | -- |
| leaf-orig-qa1 | QA1 纳排清晰度 | L5/QA1 | §2.4；Table 3 | 纳入排除标准是否描述且适当 | 是（Y）=1 / 部分（P）=0.5 / 否（N）=0 / 未知 | 有序枚举 + 数值映射 | 未知 表示需要邮件作者补 | DARE 评分组成 | -- | E05, E08 | -- |
| leaf-orig-qa2 | QA2 检索覆盖度 | L5/QA2 | §2.4；Table 3 | 检索是否可能覆盖所有相关研究 | 是（Y） / 部分（P） / 否（N） / 未知 | 有序枚举 + 数值 | 同上 | DARE 评分组成 | -- | E05, E08 | -- |
| leaf-orig-qa3 | QA3 主研究质量评估 | L5/QA3 | §2.4；Table 3 | 是否评估了纳入研究的质量/效度 | 是（Y） / 部分（P） / 否（N） / 未知 | 有序枚举 + 数值 | 同上 | DARE 评分组成 | "技术评估类应做质量评估" 候选 | E05, E08 | -- |
| leaf-orig-qa4 | QA4 基础数据描述 | L5/QA4 | §2.4；Table 3 | 是否充分描述了纳入研究/数据 | 是（Y） / 部分（P） / 否（N） / 未知 | 有序枚举 + 数值 | 同上 | DARE 评分组成 | -- | E05, E08 | -- |
| leaf-orig-qa-total | DARE 总分 | L5/QA-total | §2.4；Table 3 末列 | QA1+QA2+QA3+QA4 加总 | 浮点 0..4；观察 1..4 | 数值 | -- | Table 4 (年×均分)、Table 5 (引用 Guidelines×均分)、Spearman ρ=0.51 | "质量随年提升但与 Guidelines 引用无关" 候选 | E05, E08 | -- |
| leaf-orig-qa-agreement | 初始评分者一致性 | L5/QA-agreement | Table 3 末列 | 4 题中两评分者初始一致的题数 | 整数 0..4；观察 2..4 | 数值 | -- | 信效度副指标 | -- | E08 | -- |
| leaf-funnel-total | 漏斗总数 | F.1 | Table A1 | 来源×年份总文章数 | 整数；总和 2506 | 数值 | -- | 检索分母 | -- | E09 | -- |
| leaf-funnel-relevant | 漏斗相关数 | F.2 | Table A1 | 通过题/摘筛选 | 整数；总和 33 | 数值 | -- | 检索召回率分母 | -- | E09 | -- |
| leaf-funnel-selected | 漏斗最终选入 | F.3 | Table A1 | 通过纳排标准 | 整数；总和 19（+2 补入 = 20） | 数值 | "n/a" 表示该年该来源无会议 | 主样本分母 | "ACM Sur/SPE 等期刊零产出" 候选 | E09 | -- |
| leaf-excl-reason | 排除原因 | (A2) | Table A2 | 被排除候选论文的原因 | 开放枚举：非正式文献综述（Informal literature survey）/ 提及文献综述但未描述（Literature survey referenced but not described）/ 非 SE 主题（not a SE topic）/ 无明确检索标准且无数据抽取（no clear search criteria, no 数据抽取） | 开放枚举 | -- | 排除原因分布 | "informal review 仍主流" 候选 | E10 | A2 仅 14 条样本，分布不可外推 |

### 5. 关系边表

本文 模式 主要是「字段表」型而非「图」型，但存在若干**研究者间复核关系**、**重复版本关系**与 **EBSE 引用关系**：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel-duplicate-version | 研究 | is_conference_version_of | 研究 | 仅观察到 2 例（S3 [7]↔[8], S11 [20]↔[21]） | 默认无关系 | E07 footnote, §3.1 L311--313 | 去重 |
| rel-rater-pair | 研究 | assessed_by | 研究者 pair | (Kitchenham, other ∈ {Brereton, Budgen, Turner, Bailey, Linkman}) | 必有 | §2.4 L234--242 | 信效度 |
| rel-extractor-checker | 研究 | extracted_by → checked_by | 研究者 pair | 同上 | 必有 | §2.5 L259--267 | 单抽取-单核对模式 |
| rel-cites-ebse | 研究 | cites | EBSE 论文（EBSE paper） [23,5] OR Guidelines [22] | enum | "否" 默认 | E07 col "Refs" | RQ1 测量 |
| rel-institution-author | 研究者 | affiliated_with | institution / country | Table A3 多对多 | 多机构时拆行 | E11 | RQ3 |
| rel-rq-to-table | RQ | analysed_by | data-tabulation item | §2.6 列出 8 个分析项→4 RQ 映射 | -- | §2.6 L268--283 | 方法学审计 |

说明：**未发现 OWL/UML 式 ontology 或显式 typed graph**；关系边以「字段配对」与「RQ-分析项映射」呈现。

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段/统计表支持的统计观察（可作为 边界锚点，本文已封闭论证）

| 观察 ID | 内容 | 字段支持 | 表/段证据 |
|---|---|---|---|
| OBS-01 | 2004--2007.6 共纳入 20 条 二次研究（19 SLR + 1 MA） | leaf-orig-article-type | Table 2, §4.1 |
| OBS-02 | 12 篇技术评估 / 8 篇研究趋势 | leaf-orig-scope | §4.1 L411--412 |
| OBS-03 | 7 篇 cost estimation 主题集中 | leaf-orig-topic-area | §4.2 L432--441 |
| OBS-04 | 欧洲作者参与 14/20；Simula 实验室参与 8/20 | leaf-orig-country + leaf-orig-institution | §4.3 L515--521 |
| OBS-05 | 8/20 引用 Guidelines；2/20 引用 EBSE 论文（EBSE paper） | leaf-orig-refs-ebse | §4.1 L413--414 |
| OBS-06 | 所有 20 篇 DARE ≥1；仅 3 篇 <2；2 篇满分 4 | leaf-orig-qa-total | §3.2 L326--329 |
| OBS-07 | DARE 均分按年上升；Spearman ρ=0.51, p<0.023 | leaf-orig-qa-total × leaf-orig-year | Table 4 + §3.3 L394--397 |
| OBS-08 | 引用 Guidelines 与否，质量均分差异不显著（F=0.37, p=0.55） | leaf-orig-qa-total × leaf-orig-refs-ebse | Table 5 + §3.3 L398--404 |
| OBS-09 | 检索漏斗：2506 → 33 相关 → 19 入选；ACM Sur/SPE/TOSEM/IET SW 选入 0 | leaf-funnel-* | Table A1 |
| OBS-10 | 12 篇 tech 中仅 4 篇含实践者指南 | leaf-orig-实践者-指南 | §4.4 L587--589 |

#### 6.2 候选发现（作者 discussion / 推荐；本文给出但未硬证）

- 主题覆盖偏窄、未触及主流 SE 实践（§4.4）。
- Simula 「主题级数据库」策略可被其他组复用（§5 conclusion）。
- 主流 系统映射研究 的潜力（§4.4 关于 Jørgensen-Shepperd 的预测）。
- 美国 EBSE 参与不足，需加强（§5 conclusion）。
- 抽取-核对模式可能引入数据误差，复杂大样本下需双人独立抽取（§4.5）。

#### 6.3 对 Paper2 可迁移的方法学启发

- **完整 抽取 form + DARE rubric + 检索漏斗表三件套** 是 tertiary 研究 报告完整性的典范，可作为 Paper2 自审计模板（叶子 字段、QA rubric、Table A1 风格漏斗）。
- **「字段-RQ-分析项三角映射表」**（§2.6）值得直接引入。
- **deviation-from-protocol 单列章节** 可借鉴。
- **「抽取者 + 核对者」与「双独立评分者」分别用于不同负载** 的工程化复核分工。

#### 6.4 绝不能迁移的领域结论

- "EBSE 主要由欧洲/Simula 主导" — 历史观察，不可迁移到 2020s LLM4SE 综述。
- "ACM Computer Surveys 无 SE SLR" — 2008 年快照，已过时。
- "8/20 引用 Guidelines" 等具体计数 — 仅本文窗口。

## 证据链入口

详见 [evidence_chain.md](./evidence_chain.md)；A.1--A.4 证据链与结论-证据映射已迁出，当前证据状态（如 `not_verified`、待 A2a、`schema_seed`）保持原样。
