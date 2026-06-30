### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `da-silva-2011-six-years-slr` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是。已顺读 `paper_content.txt` 全 1625 行，并回查方法、表 2/3/5、限制和结论段。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。已读取 `bibtex.bib` 11 行、`metadata.json` 28 行，用于核对题名、年份、DOI、类型和本地状态。 |
| 是否打开或核对 `paper.pdf` | 是。使用 `pdfinfo` 确认 15 页 PDF，并用 `pdftotext -layout` 核对 PDF 第 3--13 页的 RQ、方法、表 1--13。未做截图式逐格视觉校验，表格细粒度数字仍建议 A2a 复核。 |
| 原文类型 | 更新型三级研究（updated tertiary study）；作者也称其为 review of secondary studies / mapping study of SLRs。 |
| 被编码样本单位 | 软件工程二级研究记录：SLR / mapping study / meta-analysis。主新增样本为 2008-07-01 至 2009-12-31 的 SE 集合；另与 OS/FE 前序集合比较合并。 |
| 样本数量 / 分母 | 原始检索 1455 篇；去重后 154 篇候选；77 篇进入质量评价和数据抽取；67 篇进入后续分析；前序 OS/FE 为 53 篇；合并 OS/FE+SE 为 120 篇。 |
| 原生树类型 | 维度森林：二级研究画像字段树 + DARE 质量评分树 + 外部课程/SWEBOK 映射树 + 前序更新/趋势统计树。 |
| 主统计池资格 | 局部可统计。原文有系统检索、纳排、质量评价和字段抽取，适合作为 A1-DT 原生 schema / tertiary-study pattern；但 2004--2009 EBSE 领域结论不可迁移为 Paper2 领域结论。 |
| 总体判定 | needs repair。论文证据可用，但现有 `review.md` 仍需把六叶通用接口降级为投影，并以原文抽取字段、质量准则和映射表重写维度树。 |

### 1. 原文证据阅读说明

实际读取文件：

- `bibtex.bib`：题名、作者、期刊、页码、年份、DOI。
- `metadata.json`：本地 slug、类型、证据角色、统计资格等机器字段。
- `paper_content.txt`：全文文本，覆盖摘要、引言、前序研究、方法、RQ、检索、纳排、质量评价、数据抽取、结果、讨论、限制、结论、附录。
- `review.md`：现有维度树、A.1--A.4 附录、返修段和旧 v1 审计引用。
- `paper.pdf`：用 PDF 元信息和 layout 文本核对正文表格版面；未做图片截图式人工逐格复核。

关键原文证据锚点：

1. 摘要：目标是扩展并更新两项前序 tertiary studies，覆盖 2008-07-01 到 2009-12-31。
2. 引言：作者明确称本文为 tertiary study，因为研究对象是 secondary studies。
3. Section 2：OS 为 20 篇，FE 追加 33 篇，OS/FE 合计 53 篇。
4. Section 3：作者说明 SE 为 67 篇新增 SLR，OS/FE+SE 合计 120 篇 secondary studies。
5. Section 3.1：RQ1--RQ5 组织数量、主题、活跃作者/机构、前序限制、质量趋势。
6. Section 3.4--3.5 / Fig. 2：自动检索、人工检索、去重、全文筛选、引用追踪构成纳排链。
7. Section 3.6：DARE 四项 QA1--QA4，取值 Y/P/N，分值 1/0.5/0。
8. Section 3.7：作者列出数据抽取字段，包括年份、质量分、review type、review scope、topic、EBSE/guideline 引用、primary-study 数量、practitioner guidelines、source type。
9. Table 2：按 67 个 study ref 展开字段表，是原生编码表核心。
10. Table 5：将部分 SLR 映射到教育、实践、SE Curriculum 与 SWEBOK，是外部分类法引用层。
11. Section 6：作者承认报告质量差导致数据抽取和质量评价可能不准确。
12. Section 7：作者提出 temporal update、search extension、combined update/extension 三类更新关系。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？

原文逐项描述的是软件工程领域的二级研究记录，即作者称为 SLR 的文献综述报告，其中又按研究问题类型区分 conventional SLR、mapping study、meta-analysis。新增 SE 样本为 67 篇；趋势比较时合并前序 OS/FE 的 53 篇，形成 120 篇 OS/FE+SE 数据集。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

有。检索包含六个数字库/索引系统的自动检索、指定期刊会议的人工检索、入选研究参考文献追踪；纳排包含标题摘要初筛、全文阅读、排除非 SLR 或非 SE 主题；编码包含 DCP 双人/多人决策流程、质量评价、数据抽取字段表。Fig. 2 给出数量链，Table 2/3/5 给出主要编码结果。

3. 原文字段来自哪里？

核心字段来自 Section 3.7 的 data extraction process 与 Table 2；质量字段来自 Section 3.6 的 DARE QA1--QA4 与 Table 3；教育/实践影响字段来自 Table 5，并引用 SE Curriculum 与 SWEBOK；趋势统计来自 Table 4、6--13；前序关系来自 Section 2、Section 3 和 Section 7 的 OS/FE/SE 更新叙述。

4. RQ 与样本单位是什么关系？

RQ 不是维度树本身，也不是样本单位。RQ 是结果组织方式和字段用途：RQ1 使用年份/数量/EBSE-positioned 字段；RQ2 使用 topic 与外部课程/SWEBOK 映射；RQ3 使用作者、组织、国家；RQ4 使用 review focus、practitioner guidelines、QA3 等限制字段；RQ5 使用质量分、指南引用、source type、scope 等质量分析字段。

5. 若无系统样本库，如何降级？

本文有系统样本库，不需要降级为 roadmap/guideline seed。但由于表格抽取存在文本错位、现有 `review.md` 证据锚点仍较粗，当前对 Paper2 只能作为 schema_seed / methodological seed；不能迁移具体 EBSE 年代结论。

### 3. 原生样本编码维度树 / 维度森林

```text
根对象：软件工程二级研究记录（secondary study record）
├── A. 样本来源与纳排链
│   ├── 原始检索来源：自动检索 / 人工检索 / 引用追踪
│   ├── 时间窗：2008-07-01 至 2009-12-31；前序 OS/FE 为 2004-01-01 至 2008-06-30
│   ├── 阶段分母：1455 raw → 154 unique candidate → 77 QA/extraction → 67 final analysis
│   └── 去重/多版本规则：多版本均读，时间分析使用首次发表版本
├── B. 二级研究画像字段（Table 2）
│   ├── study ref
│   ├── year
│   ├── quality score
│   ├── review type：SLR / MA / MS
│   ├── review focus：RQ / SERT / RT
│   ├── review topic：24 个 SE topic，自由文本/归并分类
│   ├── cited EBSE paper：Y/N + 引用脚注
│   ├── cited guidelines：Y/N + 引用脚注
│   ├── number primary studies：整数
│   ├── practitioners guidelines：Y/N
│   └── paper type：J / C / WS / BS / short-paper 标记
├── C. DARE 质量评价树（Section 3.6, Table 3）
│   ├── QA1：纳排标准是否描述且合适，Y/P/N → 1/0.5/0
│   ├── QA2：检索是否可能覆盖相关研究，Y/P/N → 1/0.5/0
│   ├── QA3：是否评价 primary study 质量，Y/P/N → 1/0.5/0
│   ├── QA4：基础数据/研究是否充分描述，Y/P/N → 1/0.5/0
│   ├── final score：0--4 数值
│   └── quartile：1st--4th 分位
├── D. 教育与实践影响映射（Table 5）
│   ├── useful for education：Yes / Possibly / No
│   ├── useful for practitioner：Yes / Possibly / No
│   ├── why：自由文本理由
│   ├── SE Curriculum：外部课程分类法条目
│   └── SWEBOK：外部知识体系章节/节
├── E. 作者、组织、国家/地区活动度（RQ3）
│   ├── researcher
│   ├── organisation
│   ├── country / region
│   └── repeat-publication count
└── F. 前序更新与趋势统计层
    ├── cohort：OS / FE / OS-FE / SE / OS-FE+SE
    ├── temporal update：扩展时间窗
    ├── search extension：扩展来源/策略
    ├── topic coverage change
    ├── quality trend
    └── limitation persistence：primary-study quality、practice guideline、synthesis/reporting gaps
```

缺失部分和 A2a 精核任务：作者没有在 Section 3.7 显式列出作者/组织/国家字段，但 RQ3 统计显然使用了这些 bibliographic / affiliation 数据；这部分应标为 derived field，需要 A2a 核对作者是否有单独抽取表或只在分析中派生。Table 2/3/5 的列已用 PDF layout 核对，但还没有逐格截图核验；若后续引用具体数值，应以 PDF 表格视觉复核为准。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | study ref | 二级研究画像 | Table 2 / Appendix A | 每篇入选二级研究的本地编号 | SE01--SE77 中的入选编号 | 标识符枚举 | 不适用；无编号不可入表 | 行级索引、回链到附录 | 无直接 finding | Table 2, Appendix A | 只迁移“稳定样本 ID”做法 |
| L2 | 年份 | 二级研究画像 / 趋势层 | Section 3.7, Table 2, Table 4 | 研究首次发表年份 | 2008 / 2009；合并表含 2004--2009 | 数值/离散年份 | 多版本时用首次发表版本 | 年度增长、时间窗比较 | SLR 数量增长 | Section 3.5, Table 4 | 不迁移具体年份趋势 |
| L3 | 质量分 | 二级研究画像 / DARE 树 | Section 3.6--3.7, Table 2/3 | QA1--QA4 加总得分 | 0--4，步长 0.5 | 数值区间 | 无法评分则不应进入质量统计；Table 2 中零分行需 A2a 复核 | 质量趋势、回归分析 | 质量改善/不足 | Section 3.6, Table 3 | 可迁移质量 rubric 思路，不迁移分数分布 |
| L4 | QA1 | DARE 树 | Section 3.6, Table 3 | 纳排标准是否明确且合适 | Y/P/N，对应 1/0.5/0 | 有序枚举 | 未说明为 N 或需裁决 | 质量构成分析 | 报告规范缺口 | Section 3.6 | DARE 口径需按目标领域适配 |
| L5 | QA2 | DARE 树 | Section 3.6, Table 3 | 检索是否覆盖相关研究 | Y/P/N，对应 1/0.5/0 | 有序枚举 | 检索库/策略不足按规则降级 | 质量构成分析 | 检索覆盖风险 | Section 3.6 | 原文 QA2 修改过，不能机械复用 |
| L6 | QA3 | DARE 树 | Section 3.6, Table 3 | 是否评价 primary study 质量 | Y/P/N，对应 1/0.5/0 | 有序枚举 | 未做或未使用质量数据为 N | 识别 primary-study QA 缺口 | 质量评价不足 | Section 3.6, 5.4.3 | 可迁移为证据质量字段 |
| L7 | QA4 | DARE 树 | Section 3.6, Table 3 | 数据/研究是否可追溯描述 | Y/P/N，对应 1/0.5/0 | 有序枚举 | 仅汇总不可回链为 P，未列 primary studies 为 N | 报告可追溯性分析 | 数据抽取困难 | Section 3.6, Section 6 | 可迁移到可复现证据链 |
| L8 | review type | 二级研究画像 | Section 3.7, Table 2 | 综述类型 | SLR / MA / MS | 完整枚举 | 未能分类需 not_verified | SLR/MS/MA 比例 | MS 增多、综述形态变化 | Section 3.7, 5.4.1 | 迁移类型字段，不迁移比例 |
| L9 | review focus | 二级研究画像 | Section 3.7, Table 2 | 研究关注范围 | RQ / SERT / RT | 完整枚举 | 无法判断需裁决或 not_verified | 实践导向、质量分比较 | 技术问题 vs 趋势/方法研究 | Section 3.7, 5.5 | 可作为目标综述的 focus 字段 seed |
| L10 | review topic | 二级研究画像 | Section 3.7, Table 2 | 软件工程主题 | 24 个主题；如 requirements、testing、product line 等 | 归并枚举/自由文本 | 主题归并不明需说明规则 | 主题覆盖和集中度 | 覆盖扩大/空白主题 | Table 2, 5.2 | 具体 SE topic 不迁移 |
| L11 | cited EBSE papers | 方法锚定 | Section 3.7, Table 2 | 是否显式引用 EBSE 基础论文 | Y/N + 脚注引用 | 布尔 + 关系值 | 未引用为 N；非 EBSE 指南需排除 | EBSE-positioned 数量 | 方法学采用程度 | Section 3.7, Table 4/12 | 只迁移“方法锚定引用”字段 |
| L12 | cited guidelines | 方法锚定 | Section 3.7, Table 2 | 是否引用 SLR/相关指南 | Y/N + 脚注引用 | 布尔 + 关系值 | 未引用为 N；非目标指南需标注 | 指南采用率、质量关联 | 指南使用增加但质量关系有限 | Table 2, Table 12 | 不能当作质量充分条件 |
| L13 | primary studies 数量 | 证据规模 | Section 3.7, Table 2, Table 9 | 每篇 SLR 分析的 primary studies 数量 | 非负整数 | 数值 | 未声明则缺失；作者说可由表格取得 | 中位数、质量相关性 | 证据规模与质量负相关候选 | Table 2, 5.5 | 只迁移“证据规模”字段 |
| L14 | practitioner guidelines | 实践影响 | Section 3.7, Table 2, Table 10 | 是否包含可识别的实践指南 | Y/N | 布尔 | 未显式/隐式可识别为 N | 实践导向统计 | EBSE 未充分实现 | Table 10, 5.4.2 | 不迁移具体比例 |
| L15 | source type / paper type | 发表形态 | Section 3.7, Table 2 | 首次报告来源类型 | J / C / WS / BS；另有 short-paper 脚注 | 完整枚举 + 标记 | 多版本用首次发表版本 | 质量分比较 | 期刊质量分较高候选 | Section 3.5, 5.5 | 目标库需重定义 venue 类型 |
| L16 | useful for education | 教育映射 | Table 5 | 是否适合本科 SE curriculum | Yes / Possibly / No | 完整枚举 | 只面向学术者可能为 No；判断理由需保留 | 教育相关 SLR 数量 | 教育转化潜力 | Table 5, Conclusion | 具体 curriculum 不迁移 |
| L17 | useful for practitioner | 实践映射 | Table 5 | 是否可能对实践者有用 | Yes / Possibly / No | 完整枚举 | 间接相关为 Possibly；无实践相关为 No | 实践相关 SLR 数量 | 实践转化缺口 | Table 5, Conclusion | 迁移判断结构，不迁移领域结论 |
| L18 | why | 教育/实践映射 | Table 5 | 教育/实践判断理由 | 自由文本 | 自由文本加理由 | 缺理由则证据弱 | 解释分类依据 | 形成候选机制解释 | Table 5 | 需要人工一致性审查 |
| L19 | SE Curriculum mapping | 外部分类法 | Table 5/6 | 映射到 SE 2004 Curriculum 节点 | Curriculum 条目或 N/A | 外部分类法引用 | 不适用或无映射为 N/A/空 | 课程覆盖度 | 教育覆盖稀疏 | Table 5/6 | 目标领域需换外部分类法 |
| L20 | SWEBOK mapping | 外部分类法 | Table 5/6 | 映射到 SWEBOK 章节/节 | SWEBOK 章节/节或 N/A | 外部分类法引用 | 不适用或无映射为 N/A/空 | SWEBOK 覆盖度 | topic gap | Table 5/6 | 不迁移 SWEBOK 具体章节 |
| L21 | author / organisation / country | 活动度派生字段 | RQ3, Table 7/8 | 作者、机构、国家/地区参与度 | 人名、机构、国家、region | 关系值/自由文本 | 原文未列完整 extraction field；需 A2a 标 derived | 活跃研究者/组织/地区统计 | SLR 采用扩散 | Section 5.3, Table 7/8 | 只迁移活动度分析模式 |
| L22 | update cohort | 前序更新层 | Section 2/3/7, Table 4/6/10--13 | OS、FE、SE 及合并集合关系 | OS / FE / OS-FE / SE / OS-FE+SE | 关系值/层级枚举 | 不属于前序或新增集合需排除 | 趋势、更新、扩展比较 | temporal update / search extension 方法学 seed | Section 3, Section 7 | 可迁移更新关系字段 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R1 | raw article | 经过检索/筛选成为 | candidate / selected / final SLR | 1455 → 154 → 77 → 67 | 阶段缺失则不能重构分母 | Fig. 2, Section 3.4--3.7 | 分母审计、纳排链 |
| R2 | final SLR | 属于 | update cohort | SE；合并时为 OS/FE+SE | cohort 不明则不能做趋势比较 | Section 3, Table 4 | 更新型 tertiary 统计 |
| R3 | final SLR | classified_as | review type | SLR / MA / MS | 无分类则 not_verified | Section 3.7, Table 2 | 类型分布 |
| R4 | final SLR | focused_on | review focus | RQ / SERT / RT | 无法判定需人工裁决 | Section 3.7, Table 2 | 实践/研究导向分析 |
| R5 | final SLR | addresses | review topic | 24 个 SE topic | 主题归并不明需待核验 | Table 2, 5.2 | 主题覆盖 |
| R6 | final SLR | cites | EBSE/guideline source | 引用 [14][8][20][15][16] 等 | 未引用为 N；非 EBSE 指南需排除 | Table 2 脚注, Table 12 | 方法锚定与质量关联 |
| R7 | final SLR | analyses_count_of | primary studies | 整数 | 未声明或不可追溯为缺失 | Section 3.7, Table 2/9 | 证据规模、质量相关性 |
| R8 | final SLR | assessed_by | QA item | QA1--QA4，每项 0/0.5/1 | 不可评分需排除或标 N | Section 3.6, Table 3 | 质量 rubric |
| R9 | final SLR | maps_to | SE Curriculum | curriculum topic/subtopic | 不适用为空或 N/A | Table 5/6 | 教育覆盖 |
| R10 | final SLR | maps_to | SWEBOK | SWEBOK chapter/section | 不适用为空或 N/A | Table 5/6 | 实践/知识体系覆盖 |
| R11 | final SLR | authored_by / affiliated_with | researcher / organisation / country | 人名、机构、国家、region | 原文未给完整行级表，需 derived 标注 | Section 5.3, Table 7/8 | 活动度与扩散分析 |
| R12 | previous study set | updated_or_extended_by | SE study | temporal update / search extension / combined | 无前序研究则不适用 | Section 7 | Paper2 可迁移的方法学启发 |

本文存在显式关系型 schema：尤其是 SLR→primary studies、SLR→外部指南/EBSE文献、SLR→SE Curriculum/SWEBOK、SE→OS/FE 更新关系。不能写成“未发现显式关系边”。

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段/统计表支持的统计观察：

- 数量链：新增 SE 集合 67 篇；前序 OS/FE 53 篇；合并 120 篇。
- 主题覆盖：SE 集合覆盖 24 个 SE topic，其中 14 个未出现在 OS/FE。
- 类型结构：SE 中 mapping study 比例高于 conventional SLR；原文给出 55/67 与 12/67 的比较。
- 实践/教育：结论称 15 篇与本科教育相关，40 篇可能对实践者有兴趣，26 篇主要面向研究者。
- practitioner guidelines：Table 10 给出 SE 中 24/67。
- primary-study quality：Table 11 给出质量评价相关比例；正文同时指出 full explicit evaluation 仍很低。
- 质量趋势：Table 13 与 Section 5.5 说明 2004--2009 平均质量分总体提高。
- 质量关联：Section 5.5 报告 practitioner guidelines、journal、RQ scope 与质量分回归显著；guideline citation 单因子对全体 N=120 的回归不显著。
- 报告质量风险：Section 6 说明很多 SLR 报告缺少协议、检索和质量评价信息，导致抽取需推断。

原文 discussion / recommendation / roadmap 的候选 finding：

- EBSE/SLR 方法在 SE 社区采用度上升。
- 主题覆盖扩大，但仍存在课程/SWEBOK 覆盖空白。
- 多数 SLR 对 primary studies 的质量评价和结果综合不足。
- 对实践者的指南仍少，EBSE 五步没有完全实现。
- 更新型综述可分 temporal update、search extension、combined update/extension，外部更新有助于发现原综述偏差。
- 系统综述报告需要更一致的结构和更充分的数据呈现。

对 Paper2 可迁移的方法学启发：

- 维护 raw→candidate→selected→final 的分母链，避免把检索数量、抽取数量和统计数量混用。
- 把“前序研究关系”显式编码：是否 temporal update、search extension、combined update、external update。
- 把质量评价拆为可评分 rubric，而不是只写“质量好/坏”。
- 保留外部分类法映射字段，例如目标研究可映射到 state-machine lifecycle、verification property taxonomy、artifact type 等。
- 把 statistical observation、candidate finding、final finding 分层，final finding 需要跨论文反证和研究者裁决。
- 把“缺失/需推断”作为字段语义记录，因为原文明确指出报告不足会影响数据抽取可靠性。

绝不能迁移的领域结论：

- 2004--2009 年 SE SLR 数量增长结论不能代表当前 SE 或 LLM 状态机研究。
- SWEBOK / SE Curriculum 的具体覆盖空白不能直接成为 Paper2 的技术空白。
- 欧洲/美国/亚洲研究者分布不能外推到当前 LLM 或形式化方法社区。
- “mapping study 比例更高”等比例结论不能迁移到目标文献库。
- practitioner guidelines 与质量分的回归关系只能作为该数据集观察，不能作为一般因果结论。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | `review.md` 仍把六个通用接口 leaf 放在“维度树结构”和“叶子维度表”的中心位置，虽然后文说是投影，但读者仍可能误认为这是原文树。 | 重写“维度树复原”：以“二级研究记录”为根，以 Table 2 字段、DARE QA、Table 5 外部映射、OS/FE 更新关系为主树；六叶接口移到“跨论文投影”小节。 |
| C | 样本单位写法不稳，曾出现 primary study / secondary study 混写。 | 统一为“被编码样本单位 = secondary study record / SLR-MS-MA record”；primary studies 只是每个二级研究分析的证据规模字段。 |
| C | 分母需要明确区分 raw 1455、candidate 154、QA/extraction 77、final 67、OS/FE 53、combined 120。 | 在结论卡、A.2 和 SUMMARY 表中写完整分母链；统计用途必须标明分母。 |
| I | “原文模式候选叶子映射”只列 4 个粗粒度候选叶子，少了 Table 2 的实际列。 | 增加 year、quality score、review type、review focus、topic、cited EBSE、cited guidelines、number primary studies、practitioner guidelines、source type 等原文字段。 |
| I | A.2 证据账本过泛，多行只写“方法 / 结果页；待核验”，证据强度却支撑多个节点。 | 按 Section 3.6、3.7、Table 2、Table 3、Table 5、Section 6、Section 7 拆证据行，给出具体章节和表号。 |
| I | A.3 结论强度普遍 weak，但有些节点可因 Section 3.7 / Table 2 升级为 strong。 | 字段存在性可标 strong；具体取值统计在未逐格核验前标 medium；Paper2 迁移结论仍标 weak/schema_seed。 |
| I | SUMMARY 当前“是否目标证据池：否”和 metadata 的 statistical eligibility 可能冲突。 | 改为“局部可统计”：A1-DT schema / tertiary pattern 可统计；EBSE 领域统计不迁移。 |
| M | 旧 v1 审计链接和警告保留过多，容易污染 v2 事实源。 | 将 v1 链接降为历史 provenance，不参与事实口径；v2 审计结果作为当前事实源。 |
| M | Table 2 中零分行与正文“排除零分研究”的关系存在细节疑点。 | A2a 逐格核对 final N=67 表和排除名单，必要时在缺失值语义中标注原文张力。 |

需要补 A.1--A.4：是。现有 A.1--A.4 有框架，但 A.2/A.3 证据锚定太粗，需要按本报告第 8 节替换或补充。

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| E01 | `bibtex.bib`, `metadata.json` | 元数据 | BibTeX / metadata fields | 题名、IST、2011、DOI 与 updated tertiary study 元信息一致 | 元信息核验 | strong | 原文类型、slug、出版信息 | 否 | 不支撑维度树字段 |
| E02 | `paper_content.txt`, `paper.pdf` | Abstract / Introduction | Page 1--2 | 作者目标是更新两项前序 tertiary studies，并称研究对象为 secondary studies | 类型与根对象 | strong | 根对象、原文类型、前序关系 | 否 | 不支撑具体字段全集 |
| E03 | `paper_content.txt`, `paper.pdf` | Section 2 / Section 3 | OS/FE/SE 定义段 | OS 20、FE 33，OS/FE 为 53；SE 为 67；合并为 120 | 分母与 cohort | strong | update cohort、样本数量 | 是，若引用表格细数 | 不迁移领域趋势 |
| E04 | `paper_content.txt`, `paper.pdf` | Section 3.1 | RQ1--RQ5 | RQ 覆盖数量、主题、活跃作者/组织、前序限制、质量趋势 | RQ 到字段用途 | strong | RQ 与字段关系 | 否 | RQ 不是树本身 |
| E05 | `paper_content.txt`, `paper.pdf` | Section 3.4--3.5 / Fig. 2 | 检索和筛选流程 | 自动+人工+引用追踪；1455→154→77→67 | 纳排链 | strong | 样本来源与分母链 | 是，流程图数字需视觉核验 | 不代表现代检索充分性 |
| E06 | `paper_content.txt`, `paper.pdf` | Section 3.3 | Fig. 1 DCP | 两名研究者独立评价，冲突由第三人或全体共识解决 | 编码可靠性流程 | strong | 决策/质量/抽取流程 | 否 | 不说明一致性统计指标 |
| E07 | `paper_content.txt`, `paper.pdf` | Section 3.6 | QA1--QA4 说明 | DARE 四项准则，Y/P/N 评分为 1/0.5/0 | 质量 rubric | strong | QA1--QA4、quality score | 否 | DARE 旧版四问，不可机械复用 |
| E08 | `paper_content.txt`, `paper.pdf` | Section 3.7 | data extraction bullet list | 抽取年份、质量分、type、scope、topic、引用、primary studies、practitioner guidelines、source type | 原生字段清单 | strong | Table 2 字段树 | 否 | 不含作者/组织字段明细 |
| E09 | `paper.pdf` | Table 2 | 67 行 SLR 编码表 | Table 2 展开每篇 SLR 的画像字段 | 行级编码表 | strong | 二级研究画像字段 | 是，逐格数值需 A2a | 只支撑 SE 新增样本 |
| E10 | `paper.pdf` | Table 3 | QA score table | 每篇研究 QA1--QA4、final score、quartile | 质量结果表 | strong | DARE 质量树 | 是，逐格数值需 A2a | 零分行与排除叙述需复核 |
| E11 | `paper.pdf` | Table 5/6 | Curriculum / SWEBOK mapping | 教育/实践有用性、理由、SE Curriculum、SWEBOK 映射 | 外部分类法映射 | strong | 教育/实践影响树 | 是，表格长且跨页 | 具体分类法不迁移 |
| E12 | `paper_content.txt`, `paper.pdf` | Section 5.5 | 回归/相关性段 | practitioner guidelines、journal、RQ scope 与质量分回归显著；primary-study 数量与质量分相关 | 统计观察 | medium | 候选 finding | 是，数值和符号需核验 | 非因果结论 |
| E13 | `paper_content.txt`, `paper.pdf` | Section 6 | Limitations | 报告不足导致抽取和 QA 可能不准确 | 威胁与缺失值语义 | strong | 迁移边界、缺失值语义 | 否 | 只说明本文可靠性风险 |
| E14 | `paper_content.txt`, `paper.pdf` | Section 7 | update/extension 段 | temporal update、search extension、combined update/extension 三类 | 方法学 seed | strong | 前序关系字段 | 否 | 不是样本行级字段 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C01 | 本文是更新型三级研究，根对象是软件工程二级研究记录，不是 primary study。 | tree_type | 根对象 | E01, E02, E03 | strong | A1-DT 类型判定 | 不能将 primary-study 数量误作样本单位 |
| C02 | 本文存在系统样本库和显式字段抽取，具备局部统计资格。 | eligibility | 样本库 | E05, E07, E08, E09 | strong | A1-DT schema / tertiary pattern 统计 | EBSE 领域结论不可迁移 |
| C03 | 原生维度树应以 Table 2 的二级研究画像字段为核心。 | schema_definition | 二级研究画像 | E08, E09 | strong | 重写 `review.md` 维度树 | 作者/组织字段需另标 derived |
| C04 | DARE QA1--QA4 是独立质量评价子树，取值为 Y/P/N 与 1/0.5/0。 | schema_definition | 质量树 | E07, E10 | strong | 质量字段 seed | DARE 版本较旧，目标研究需适配 |
| C05 | Table 5/6 构成教育/实践影响与外部分类法映射层。 | schema_definition | 教育/实践树 | E11 | strong | 外部分类法映射模式 | SE Curriculum/SWEBOK 具体项不迁移 |
| C06 | OS/FE→SE→OS/FE+SE 的前序关系是本文维度森林的重要层，不应丢失。 | relation_schema | 更新关系 | E03, E14 | strong | predecessor/update 字段 | 无前序综述的论文不适用 |
| C07 | 原文统计观察可作为 candidate finding，但不能直接升级为 Paper2 final finding。 | finding_boundary | 统计观察/候选 finding | E12, E13 | medium | 候选发现台账 | 需要跨论文反证和研究者裁决 |
| C08 | 现有 `review.md` 的六叶通用接口只能保留为投影，不能作为原文树事实源。 | repair_action | `review.md` | E08, E09, E10, E11 | strong | 返修依据 | 可保留六叶作为跨论文统一接口 |
| C09 | 本文的分母链必须写全：1455、154、77、67、53、120 分别服务不同用途。 | denominator_policy | 样本数量 | E03, E05 | strong | SUMMARY / 审计卡修正 | Table 2 零分行需 A2a 复核 |
| C10 | Section 6 的抽取困难说明应转化为缺失值语义和证据强度限制。 | limitation_policy | 缺失值语义 | E13 | strong | A.2/A.3 证据强度 | 不应因此否定全部统计，只需分层降级 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence-engineering、证据门、不能发明结论、强结论必须有本地证据支撑。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer 视角，优先指出可执行的返修风险、证据不足和可复现性问题。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 rejection-risk audit 思路，把现有 `review.md` 的 C/I/M 风险和 claims-evidence gaps 显式列出。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先理解研究上下文、再结构化输出 schema、任务依赖和风险的流程。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用“严格跟随原方法、数据、配置，不清楚就标明”的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化字段、风险、依赖和评估口径表达。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 完成观念；本任务禁止写文件和启动循环，因此只作为审计原则使用，未运行 autoresearch。

本输出最高风险的 3 点：

1. Table 2/3/5 是 PDF 长表，`paper_content.txt` 有明显错位。我已用 `pdftotext -layout` 核对列结构，但逐格数字仍需 A2a 视觉复核。
2. “77→67 排除”与 Table 2/Table 3 中零分研究的关系存在原文或抽取张力。主线程合并时应人工数行并核对 Appendix A。
3. 作者/组织/国家字段没有出现在 Section 3.7 的数据抽取 bullet list，但 RQ3 明显使用这些信息。本报告将其标为 derived field；合并时不要把它写成作者显式 extraction form 字段，除非 PDF/补充材料找到证据。

blocked / timeout / 文件缺失情况：未出现 blocked、timeout 或文件缺失。全程只读本地文件和 PDF，没有修改仓库、commit、push、gh comment，也没有启动 subagent 或后台 agent。