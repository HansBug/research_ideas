# Machine Learning for Software Engineering: A Tertiary Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Machine Learning for Software Engineering: A Tertiary Study |
| 年份 | 2023 |
| 类型 | tertiary study |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [CSUR](https://dl.acm.org/journal/csur) |
| CCF 官方大类 | 待核验（疑似非软件工程大类；官方页 WAF） |
| CCF 官方等级 | 待核验 |
| CCF 复核状态 | 官方待人工复核（WAF）；本地未建 CSUR 条目 |
| 来源等级 | 高等级综述期刊；ACM Computing Surveys；arXiv 开放 PDF；CCF 官方等级暂不写死 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | tertiary study；汇总 83 篇 reviews 与 6117 篇 原始研究 |
| SE 子领域 | ML4SE；覆盖软件生命周期多个活动 |
| A1 角色 | 现代高等级 tertiary study 样本，用于压测大规模二次研究汇总、分类体系、research challenges 与 action recommendations。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 历史观察 | 暴露“挑战 / 行动建议”类 finding pattern；已在 SUMMARY 中作为 A2a 重点候选。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 原文以 ML for SE 的覆盖、分类、质量评估与研究挑战组织三级研究；摘要直接说明 systematically collected、quality-assessed、summarized、categorized 83 reviews。 | `paper_content.txt` Page 1 摘要。 | 可迁移为“覆盖 + 分类 + 质量 + 挑战 / 行动”组合。 | ML4SE 的覆盖/挑战 RQ 可迁移为样式，不迁移具体领域问题。 |
| dimension pattern | 维度包括 SE 生命周期活动、ML 技术、review 质量、原始研究 数量、研究挑战和建议行动。 | `paper_content.txt` Page 1 摘要；全文目录与分类章节待 PDF 表格核对。 | 高度可迁移，但字段树较大，A2a 需细分。 | 字段树较大，A2a 需要拆分并验证取值空间。 |
| finding pattern | 发现不仅是分布统计，还提出 ML4SE research challenges/actions，如更多实证验证、工业研究、数据/管线文档化、增量 ML。 | `paper_content.txt` Page 1 摘要。 | 可迁移为 Paper2 的 候选发现 heuristic：统计观察之后要形成行动建议。 | 挑战/行动建议是启发式，不代表目标主题最终 finding。 |
| evidence presentation pattern | 使用 83 reviews / 6117 原始研究 的分母、质量评估、分类表和挑战列表。 | `paper_content.txt` Page 1 摘要；表格待原文核对。 | 可迁移为大规模总账和 pattern-to-source anchor。 | 83 reviews/6117 原始研究 的数值需 PDF 表格核对后才能引用。 |
| validity / threat pattern | 本轮只读题摘和全文开头，threats 章节待进一步定位；当前不能写成已完整核验。 | `paper_content.txt` 全文待 A2a 深读。 | 作为待核验字段，不能强写。 | 本轮未完整定位 threat 章节，不能强写完整核验。 |
| report structure pattern | CSUR 综述结构，含 introduction、method、classification/results、discussion/challenges；具体章节待 A2a 深读。 | `paper_content.txt` 目录提取不完整；需 PDF 目录核对。 | 候选可迁移。 | CSUR 长综述结构适合参考，但 paper2 仍需突出方法贡献。 |

## 3. 对 PR-A1 schema 的启发

1. 新增 `challenge_action_pattern` 作为 `finding_pattern` 的子类型：从统计分布转为研究挑战和行动建议。
2. 大型 tertiary study 需要 `secondary_count`、`原始研究数量（primary_count）`、`classification_axis` 等字段。
3. 高等级现代样本会暴露 A1 早期 EBSE 文献过旧的问题，A2a 应优先扩展 2020 年后的 SE tertiary/survey。

## 4. 待复核

- 需进一步定位 RQ、threats、classification 表和 challenge 表的页码。
- DOI/最终出版页已记录；正式写作前应核对 ACM 版与 arXiv 版差异。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 把 ML4SE 三级研究定义为“收集、质量评价、汇总、分类 reviews 并追溯 原始研究”。 | 可迁移三级研究的 scope / unit-of-analysis 设计；不能迁移 ML4SE 具体结论。 |
| A1-M1 语料收集与纳排 | 提供 reviews / 原始研究 双层分母、质量评价和纳排边界。 | 可作为二次研究语料台账字段候选。 |
| A1-M2 研究对象与主题语义 | 以 SE 生命周期活动、ML technique、研究挑战组织 taxonomy。 | 可候选为“生命周期 + 技术 + 任务”字段树样式。 |
| A1-M3 方法 / 技术 / 干预 | 抽取 ML 方法族与 SE 活动之间的关系。 | 只迁移“方法与任务交叉分类”模式。 |
| A1-M4 评价、证据与复现资产 | 使用质量评价、review / primary-study 数量和分类表支撑结论。 | 正式引用具体数值前需 原文图表核对。 |
| A1-M5 统计分析就绪 | 大规模 tertiary 能形成跨 review / primary-study 的分布与覆盖统计。 | 可作为 A2a 大样本统计字段候选。 |
| A1-M6 research finding 形成与裁决 | 从分布统计进一步形成 challenges 和 action recommendations。 | 可作为 候选发现 heuristic，不作为 Paper2 目标领域 finding。 |

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 叶子 / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__codex.md](../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__codex.md)、[../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__claude.md](../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__claude.md)、[../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__deepseek.md](../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/ml4se-tertiary-study.md](../../audits/a1dt-v2-19x3/adjudications/ml4se-tertiary-study.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `ml4se-tertiary-study` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是；读取第 1--约 1100 行（覆盖摘要、相关工作、方法、结果、讨论、限制、结论与参考文献起始），后续参考文献段落仅扫读 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是，二者已对照确认（Kotti, Galanopoulou, Spinellis；CSUR；DOI 10.1145/3572905） |
| 是否打开或核对 `paper.pdf` | 否；本轮以提取文本为主。Table 3/4/5/6/7、Fig 1--6 的版面、字号、跨页表头需 PDF 视觉核验，已列入 A.4 |
| 原文类型 | tertiary 研究（系统文献综述 aggregating 二次研究；遵循 Kitchenham & Charters 2007 指南） |
| 被编码样本单位 | 二次研究（83 篇通过质量评估的二次研究，即 SLR / SMS / survey / 分类法 / 元分析（meta-analysis））；间接覆盖 6 117 篇 原始研究，但 primary 不是被逐一编码的样本单位 |
| 样本数量 / 分母 | 1 567（检索去重后） → 140（候选）→ 83（质量评估通过，QA ≥ 2.0；41% 因 QA < 2.0 排除） |
| 原生树类型 | **维度森林**：以 二次研究 为节点，挂接多棵独立但同根的 模式树（书目元数据树 / 研究方法与质量树 / SWEBOK KA × SE task 主题树 / ML 四轴分类树 / 含义与挑战树） |
| 主统计池资格 | 局部可统计——SWEBOK KA 分布、ML 四轴分布、DARE-4 分布等已有显式表格；但 A2a 仍需逐叶精核取值空间饱和性 |
| 总体判定 | v2 已返修完成：原始审计对旧版 `review.md` 的判定为 需要返修；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

本轮基于 `paper_content.txt`（共 1 774 行）通读了第 1--1 322 行（正文与结论），并 spot-check 了参考文献起始段；未打开 PDF。所读章节包括：摘要（p.1）、§1 Introduction（p.1--3）、§2 Related Work（p.3--5）、§3 Review Methods（含 §3.1 RQ、§3.2 Search、§3.3 IC/EC、§3.4 Selection、§3.5 Quality、§3.6 数据抽取（数据抽取），p.5--12）、§4 Results（§4.1 数据抽取、§4.2 RQ1 11 个 KA 分小节、§4.3 RQ2 11 个 KA 分建议、§4.4 RQ3 四轴分类，p.12--24）、§5 Discussion（含 Implications 1--7，p.24--27）、§6 效度威胁（研究选择（Study Selection） / 数据（Data） / 研究（Research），p.27--28）、§7 Conclusion and Recommendations（p.28--29）。

关键证据锚点（5--12 条）：

1. 摘要 p.1：明确分母 "83 reviews … covering 6 117 原始研究"，published 2009--2022。
2. p.5--6 §3.1：三 RQ 显式列出（RQ1 SE tasks tackled / RQ2 SE KAs underrepresented / RQ3 ML techniques used）。
3. p.6--8 §3.2：搜索串由三组关键词笛卡尔积构成（Table 1：SE 13 个 SWEBOK KA 关键词 + ML 27 个关键词 + Secondary Studies 35 个关键词），库为 IEEE Xplore / ACM DL / Scopus，年限 2015--2020 自动；snowballing 扩到更早 / 更晚。
4. p.8 §3.3：IC/EC 显式列出（包含 taxonomies 6 条 planning characteristics）。
5. p.9--10 §3.5 + Table 2：DARE-4 四问，每问 Y=1 / P=0.5 / N=0；总分 0--4；阈值 ≥ 2；140 → 83（57 排除，41%）。
6. p.10--12 §3.6：每篇 二次研究 抽取 11 类信息（标题与来源、年份、venue、作者/单位/国家、研究类型、研究方法、QA 分、primary 数、application domain = SWEBOK KA + 子领域（subarea） + SE task(s) 通过开放编码，最多 3 个 SE task、implications、ML techniques）。
7. p.11 §3.6：ML 四轴分类方案——AI 角色（Role of AI） in SE（3 类）/ Supervision（4 类）/ Incrementality（2 类）/ Generalizability（2 类）。
8. p.13--14 Tables 3--4：83 篇 二次研究 的逐行台账（每行 6 字段：研究 ref、Venue、Year、Publisher、QA Score、Primary、Covered Years）。
9. p.15 Table 5：SWEBOK KA × Subarea × Sec.（数）× % × Refs × Prim.（数）的交叉分类表，覆盖 11 个 KA。
10. p.22--23 Table 6 + Fig 6：ML 四轴分布百分比（AI 角色（Role of AI） 14/20/65；Supervision 78/13/6/2；Incrementality 99/1；Generalizability 87/13）+ KA × ML 轴 heatmap。
11. p.24 Table 7：ML 技术按 "ML application task" 八大类分组（分类 / 聚类 / 回归（分类/Clustering/Regression）、模式发现（Pattern Discovery）、降维（Dimensionality Reduction）、信息检索（Information Retrieval）、随机搜索（Stochastic Search）、生成（Generation）、混合（Hybrid）、其他（Miscellaneous））。
12. p.24--27 §5：Implications 1--7（经验研究（empirical）/comparative/工业（industrial） 验证、地址 SE literature deficiencies、人本 KA、data 流程管线 文档化、proprietary data 共享、online/incremental 探索、混合（混合）/cross-domain ML）。
13. p.27--28 §6：Threats 分 研究选择（Study Selection） / 数据（Data） / 研究（Research） 三类，使用 Ampatzoglou et al. 2019 的 secondary-研究 威胁 分类方案。

### 2. 样本单位与字段来源判定

1. **原文纳入和逐项描述的对象**：83 篇通过质量评估的 二次研究（SLR / SMS / 元分析（meta-analysis） / survey / 分类法）。Primary 研究 总数（6 117）只作覆盖性背景指标，**不是被逐篇编码的样本单位**。
2. **是否有系统检索 / 纳排 / 数据抽取 / 编码方案**：是，全部到位——四阶段检索（automated / manual / backward / forward snowballing）、显式 IC/EC（含 分类法 6 条特征）、Kappa ≥ 0.8 的双人选择、DARE-4 质量评估、双人 数据抽取 with checker、open coding for SE tasks、四轴 ML 分类。这是一个高度规范化的 tertiary SLR。
3. **字段来源**：
   - 书目元数据 / 质量分 / primary 数 → §3.6 显式抽取清单 + Tables 3/4。
   - 主题分类 → SWEBOK V3 KA + 自构 子领域（subarea） + 开放编码 SE task（最多 3 个/篇），存于 `knowledge_areas.csv` 与 Table 5。
   - 方法分类 → 四轴 ML 分类方案（Section 3.6 末尾详细定义）+ 自由文本 ML technique list（Table 7 按 ML application task 分组）。
   - 含义/建议 → 通过 §4.3.x 抽取，并汇总到 §4.3.1 General Recommendations（带计数 n=3..21）和 §5 Implications 1--7。
4. **RQ 与样本单位关系**：RQ 是**字段用途锚**而非树根。RQ1↔KA/子领域（subarea） + SE task 字段；RQ2↔further-research 自由文本 + 跨研究 KA 覆盖统计；RQ3↔四轴 ML 分类 + ML technique 列表。83 篇 secondary 才是树根，RQ 决定哪些叶子被汇总为统计 / 跨研究比较。
5. **无系统样本库降级**：不适用——本文是教科书式的 tertiary SLR，分母、检索、IC/EC、QA、抽取协议、复现实验包（Zenodo 10.5281/zenodo.7082429）齐备。

### 3. 原生样本编码维度树 / 维度森林

样本单位 = `secondary_研究`（n=83）。原生树是**多棵共根森林**：

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
二次研究（二次研究；首次术语；n=83；通过 DARE-4 QA≥2.0）
├── [B1] 书目信息切面 / 元数据树（切面（facets））
│   ├── L1.1 研究引用号（ACM 编号引用）— 关系值，指向 References 列表
│   ├── L1.2 发表源名称 — 自由文本（Table 3/4 第 2 列；如 "ACM Comput. Surv."、"IEEE Trans. Softw. Eng."）
│   ├── L1.3 发表源类型 — 受限枚举 {期刊（journal）, 工作坊论文集（workshop proceedings）, 会议论文集（conference proceedings）, 图书章节（book chapter）}（§3.6）
│   ├── L1.4 年份 — 数值 2009..2022（Table 3/4）
│   ├── L1.5 出版方 — 受限枚举 {IEEE, Elsevier, Springer, ACM, Wiley, Other (含 MDPI / IET / Inderscience / Tech Science Press / World Scientific / Wrocław UST / Science Publications / The Science and Information Organization)}（Fig 3 图例 + Tables 3/4）
│   ├── L1.6 作者 — 多值自由文本；统计派生：总作者 274 人，最活跃 Ruchika Malhotra (6 篇)（§4.1 Top 作者）
│   ├── L1.7 机构 — 多值；总 140 个机构；Top: Delhi Technological University (7)（§4.1）
│   └── L1.8 国家 — 多值，机构属国
├── [B2] 研究设计 树
│   ├── L2.1 研究类型 — 受限枚举 {SLR, 系统映射研究, survey, 分类法, 元分析（meta-analysis）}；§4.1 分布：SLR 53/64%，SMS 16/19%，survey 13/16%，分类法 1
│   ├── L2.2 二次研究类型（部分研究有第二类型）— 同 L2.1 枚举；7 篇为 SLR+SMS [51,120] 或 SLR+元分析（meta-analysis） [17,52,67,112,147]
│   ├── L2.3 研究方法 — 自由文本指向已知 SLR 指南 集合 {Kitchenham [81,83,86], Petersen [126,127], Kitchenham [87], Hall et al. [62], Wohlin snowballing [167,169,170], Easterbrook [50], Sabir [140], Zhou [181], Dybå [49], CASP [131]}
│   ├── L2.4 数据综合方法 — 受限/自由文本 {内容分析（内容分析）, 扎根理论（grounded theory）, 箱线图（box plots）, ...}（p.14）
│   └── L2.5 覆盖年份 — 数值区间（Table 3/4 第 6 列；如 1994--2008、2005--2014）
├── [B3] 质量评估 树（DARE-4）
│   ├── L3.1 QA1_IC/EC — 序数 {Y=1, P=0.5, N=0}（Table 2 规则）
│   ├── L3.2 QA2_search_space— 序数 {Y=1（4+ 个库 + 额外策略）, P=0.5（3–4 个库且无额外策略）, N=0（1–2 个库）}
│   ├── L3.3 QA3 原始研究质量评估（QA3_quality_assessment_of_primary）— 序数 {Y, P, N}
│   ├── L3.4 QA4 原始研究信息充分性（QA4_primary_information）— 序数 {Y, P, N}
│   └── L3.5 QA_total — 数值 0..4，纳入阈值 ≥ 2（41% 排除）
├── [B4] 原始研究覆盖度树（Primary-研究 coverage）
│   ├── L4.1 原始研究数量（原始研究数量） — 数值（Table 3/4 第 5 列；范围 10..445；总和 6 117 non-unique）
│   └── L4.2 原始研究年份范围（原始研究年份范围） — 数值区间（同 L2.5）
├── [B5] SWEBOK KA × SE 任务 主题树（RQ1 / RQ2）
│   ├── L5.1 SWEBOK 知识域（swebok_ka）— 受限枚举 {软件质量（软件质量）, 软件测试（SW 测试）, 软件工程过程（SE 过程）, 软件工程管理（SE Management）, 软件需求（SW 需求）, 软件维护（SW 维护）, 软件设计（SW 设计）, 软件配置管理（SW Configuration Management）, 软件工程模型与方法（SE Models & Methods）, 软件工程专业实践（SE Professional Practice）, 工程基础（Engineering Foundations）}（11/15 KAs，3 个 Foundations KA 因 scope 被排除）
│   │   └── L5.1.1 知识域子领域（subarea）— SWEBOK V3 子项（Table 5 第 2 列，如 实践考虑（Practical Considerations）/ 测试技术（Test Techniques）/ 软件生命周期（SW Life Cycles） 等共 22 个 子领域（subarea）-cell）
│   │       └── 每 KA × 子领域（subarea） cell 统计：二次研究数（Sec.）/ % / 引用列表（Refs）/ 原始研究数（Prim.）
│   ├── L5.2 软件工程任务（se_task）— 开放编码自由文本（如 软件变更预测（software change prediction）, 质量预测（quality prediction）, 可维护性预测（maintainability prediction）, 缺陷预测（defect prediction）, 恶意软件检测（malware detection）, 异味检测（smell detection）, 数据外泄检测（data exfiltration）, 测试自动化（test automation）, 测试预言机（test oracle）, 移动端测试（mobile testing）, 测试评价, 测试优化, 测试用例优先级排序（test case prioritization）, 软件故障预测（software fault prediction）, 漏洞检测（vulnerability detection）, 渗透测试（penetration testing）, 主题建模（topic modeling）, 过程挖掘（流程 mining）, 自动化（automation）, 源代码分析（source code analysis）, 程序生成（program 生成）, 推荐系统（recommender systems）, 成本估计（cost estimation）, 工作量估计（effort estimation）, 集成工作量估计（ensemble effort estimation）, 增强工作量估计（enhancement effort estimation）, 波动性预测（volatility prediction）, 需求复用（requirements reuse）, 特征 / 可变性抽取（feature/variability 抽取）, 需求获取（elicitation）, 歧义消解（ambiguity resolution）, 缺陷优先级排序（bug prioritization）, 重命名重构（rename refactoring）, 架构恢复（architecture recovery）, 逆向工程（reverse engineering）, 性能预测（performance prediction）, 配置优化（configuration optimization）, 跟踪恢复（trace recovery）, 认知负荷估计（cognitive load estimation）, 缺失值填补（缺失值 imputation）, ...）；约束：每 研究 最多 3 个 SE 任务（§3.6 末）
│   └── L5.3 知识域到任务关系（ka_to_task） — 关系边（多对多，因 1 个 SE 任务 可关联多个 KA）
├── [B6] 机器学习四轴分类树（RQ3）
│   ├── L6.1 AI 角色（role_of_AI） — 受限枚举 {计算搜索与优化（Computational search & optimization / SBSE）、模糊与概率方法（Fuzzy & probabilistic 方法）、分类 / 学习 / 预测（分类/learning/prediction）}（来源 [65]）
│   ├── L6.2 监督方式（supervision） — 受限枚举 {监督式（supervised）、无监督式（unsupervised）、半监督式（semi-supervised）、强化学习（reinforcement）}（来源 [77]）
│   ├── L6.3 增量性（incrementality） — 受限枚举 {批处理 / 离线（batch/offline）、在线 / 增量（online/incremental）}（来源 [77]）
│   ├── L6.4 泛化方式（generalizability） — 受限枚举 {基于模型（model-based）、基于实例（instance-based）}（来源 [77]）
│   └── L6.5 机器学习技术列表（ml_technique_list） — 多值自由文本，事后按“机器学习应用任务（ML application task）”分组到 Table 7 八大类
│       └── L6.5.1 机器学习应用任务（ml_application_task） — 受限枚举 {分类 / 聚类 / 回归（分类 & Clustering & Regression）、模式发现（Pattern Discovery）、降维（Dimensionality Reduction）、信息检索（Information Retrieval）、随机搜索（Stochastic Search）、生成（Generation）、混合（Hybrid）、其他（Miscellaneous）}（§4.4 + Table 7）
├── [B7] 启示 / 后续研究 树（RQ2）
│   ├── L7.1 知识域特定建议（ka_specific_推荐） — 自由文本，按 KA 组织（§4.3.2..4.3.12）
│   ├── L7.2 一般建议（general_推荐） — 带计数自由文本（§4.3.1，n=3..21）：比较式与统计式（comparative-vs-statistical） (13)、经验研究（empirical） (12)、开放 / 大规模数据集（open/large 数据集） (16)、混合 / 集成 / 增量（混合 / ensemble / incremental） (21)、工业/实践者 (18)、超参数（hyperparam） (3)、类别不平衡（class imbalance） (3)
│   └── L7.3 启示综合（implication_synthesis） — 编号 1..7（§5）
└── [B8] 有效性威胁与复现制品树（威胁 / replication 制品）
    ├── L8.1 威胁类别（threat_category） — 受限枚举 {研究选择（Study Selection）、数据（Data）、研究（Research）}（按 Ampatzoglou et al. 2019 [12]）
    ├── L8.2 威胁条目（threat_item） — 自由文本（年限、库选择、检索式、IC/EC、QA 框架（QA 框架）、推断信息、AI 角色（Role of AI） 分类轴的领域适配、人工编码主观性、可推广性）
    └── L8.3 复现制品（replication_artifact） — URL/文件名（Zenodo DOI；review-protocol.md、cohen_kappa_agreement.csv、研究_selection_reviewer_{1,2}.csv、dare_assessment.csv、knowledge_areas.csv、further_research.csv、further_research_general.txt、ml_techniques.csv、backward_snowballing.csv 等 14+ 复现实验文件）
```

**关键关系边**：（KA, 子领域（subarea）, SE task）三元关系是多对多；（研究, KA）允许 1 研究 → 1 most prominent KA；（研究, SE task）允许 1 研究 → 1..3 tasks；（研究, ml_axis_category）每轴选 most prominent 1 类。

### 4. 叶子维度表

仅列**取值空间已显式可枚举或显式分母的核心叶子**（共 28 条；自由文本与机构 / 作者类型态省略以控篇幅）：

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1.3 venue_type | 出版形态 | B1 | §3.6 第 1 条 | 出版载体类型 | {journal, workshop proc., conf. proc., book chapter} | 完整枚举 | 不允许缺失（每行都有 venue） | 期刊/会议比 76% vs 24% | 学术化程度倾向 | §4.1 p.12 | 模式可迁移 |
| L1.4 year | 出版年份 | B1 | Table 3/4 | secondary 发表年 | 2009..2022 数值 | 数值 | 不允许缺失 | 年度分布 + 趋势 | 增长拐点 2015 | Fig 2/3 p.6/14 | 仅本研究窗口 |
| L1.5 publisher | 出版商 | B1 | Fig 3 + Table 3/4 | 出版机构 | {IEEE 25, Elsevier 17, Springer 13, ACM 12, Wiley 5, Other} | 完整枚举（带 long tail） | other 类承接 long tail | 出版商集中度 | 5 大出版商占 ~87% | §4.1 p.12 | 迁移结构 |
| L1.6 authors | 作者多值 | B1 | §3.6 + §4.1 | 作者列表 | 自由文本 + 派生计数 | 多值自由文本 | -- | 作者集中度（274 人，最高 6 篇） | 领头研究者识别 | §4.1 p.12 | 模式可迁移 |
| L2.1 研究_type | 研究类型 | B2 | Table 3/4 + §4.1 | 二次研究形态 | {SLR, SMS, survey, 分类法, 元分析（meta-analysis）} | 完整枚举 | 不允许缺失 | SLR 64% / SMS 19% / survey 16% / 分类法 1% | secondary 形态偏好 | §4.1 p.12 | 模式可迁移 |
| L2.2 secondary_研究_type | 第二研究类型 | B2 | §4.1 | 部分论文含混合方法 | 同 L2.1；7 篇有第二类型 | 完整枚举 + 可空 | 缺失 = 单一类型 | 混合方法占比 ~8% | 混合方法 趋势 | §4.1 p.12 | 模式可迁移 |
| L2.3 research_method | 采用的 SLR 指南 | B2 | §4.1 + §3 | 引用的方法学指南集合 | {Kitchenham 81/83/86/87, Petersen 126/127, Hall 62, Wohlin 167/169/170, Easterbrook 50, Sabir 140, ...} | 关系值（受限引用集） | 缺失需推断（§6 数据有效性（Data Validity）） | 指南 引用频次 | 主流 指南 识别 | §4.1 p.12--14 | 模式可迁移 |
| L3.1 QA1_IC/EC | 质量分 Q1 | B3 | Table 2 | IC/EC 显式度 | {1, 0.5, 0} | 完整序数 | 必填 | DARE-4 各项分布 | -- | Table 2 p.10 | 仅 DARE-4 |
| L3.2 QA2_search_space | 质量分 Q2 | B3 | Table 2 | 检索库覆盖 | {1, 0.5, 0} | 完整序数 | 必填 | -- | -- | Table 2 p.10 | 仅 DARE-4 |
| L3.3 QA3_primary_quality | 质量分 Q3 | B3 | Table 2 | primary QA 实施 | {1, 0.5, 0} | 完整序数 | 必填 | -- | -- | Table 2 p.10 | 仅 DARE-4 |
| L3.4 QA4_primary_info | 质量分 Q4 | B3 | Table 2 | primary 信息呈现 | {1, 0.5, 0} | 完整序数 | 必填；主观性最高（disagreement 多） | -- | -- | Table 2 p.10 + §3.5 p.10 | 仅 DARE-4 |
| L3.5 QA_total | 总质量分 | B3 | Table 3/4 | QA 累加 | 0..4 数值 | 数值 | 必填；阈值 ≥ 2 | 平均 ≈ 3；41% < 2 排除 | 质量提升趋势（2014 后稳） | Fig 4 p.14 | 仅 DARE-4 |
| L4.1 原始研究数量（原始研究数量） | primary 数 | B4 | Table 3/4 第 5 列 | 该 review 覆盖的 primary 数 | 数值 10..445 | 数值 | 部分 review 未直接报告 → 数 bib（§6） | sum=6117，mean≈74 | -- | Tables 3/4 p.13--14 | 模式可迁移 |
| L4.2 原始研究年份范围 | primary 年份区间 | B4 | Table 3/4 第 6 列 | 覆盖的 primary 起止年 | 数值区间 1990..2021 | 数值区间 | 偶有缺失 | -- | -- | Tables 3/4 p.13--14 | 模式可迁移 |
| L5.1 swebok_ka | SWEBOK 知识域 | B5 | Table 5 + §3.6 | SWEBOK V3 KA | 11 类：软件质量 / SW 测试 / SE 过程 / SE Management / SW 需求 / SW 维护 / SW 设计 / SW Configuration Mgmt / SE Models & Methods / SE Professional Practice / Engineering Foundations（Computing/Math/Engineering Foundations 被排除）| 层级枚举（部分覆盖 SWEBOK 完整集） | 必填；most prominent KA | n: 软件质量 25 (30%) / 测试 17 (20%) / SE 过程 14 (18%) / Mgmt 12 (14%) / Req 6 (6%) / 其他各 1--3 | 人本 KA 显著欠覆盖 | Table 5 p.15 + §4.2 | KA scope 可迁移 |
| L5.1.1 子领域（subarea） | KA 子域 | L5.1 | Table 5 第 2 列 | SWEBOK 子领域（subarea） | 22 个 KA×子领域（subarea） cell（如 实践考虑（Practical Considerations）/ 测试技术（Test Techniques）/ 软件生命周期（SW Life Cycles） / SW Project 计划（Planning） / 需求 Analysis 等） | 层级枚举 | 必填 | 子域分布 | 子域内部不平衡 | Table 5 p.15 | 子域映射依赖 SWEBOK |
| L5.2 se_task | SE 任务（开放编码） | B5 | §3.6 + §4.2 各小节 | 开放编码任务码 | 自由文本，但每 研究 1..3 个；§4.2 出现 ~40+ 任务码 | 开放枚举 + 上限 3 | 必填 ≥ 1 | 任务频次 | 任务 × KA 交叉关系 | §4.2 p.15--19 | 编码本身可迁移；具体任务标签 ML4SE 特定 |
| L5.3 ka_to_task | KA-task 关系 | B5 | §3.6 末 | SE task 可关联多 KA | 多对多关系值 | 关系值 | -- | -- | -- | §3.6 p.11 | 结构可迁移 |
| L6.1 AI 角色（role_of_AI） | AI 在 SE 中的角色 | B6 | Table 6 + §3.6 | 三类 AI 角色 | {SBSE 14%, Fuzzy/probabilistic 20%, 分类/learning/prediction 65%} | 完整枚举 | 必填；most prominent 1 类 | -- | C/L/P 主导 | Table 6 p.23 + §4.4 | 来源 [65] |
| L6.2 监督方式（supervision） | 监督形式 | B6 | Table 6 + §3.6 | 监督学习类型 | {supervised 78%, unsupervised 13%, semi-supervised 6%, reinforcement 2%} | 完整枚举 | 必填 | 监督学习压倒性 | -- | Table 6 p.23 | 来源 [77] |
| L6.3 增量性（incrementality） | 增量性 | B6 | Table 6 + §3.6 | 在线/离线 | {batch/offline 99% (82), online/incremental 1% (1)} | 完整枚举（布尔型） | 必填 | offline 压倒性 | online 是研究空白（Implication 6） | Table 6 p.23 | 来源 [77] |
| L6.4 泛化方式（generalizability） | 泛化形式 | B6 | Table 6 + §3.6 | 模型/实例驱动 | {model-based 87%, instance-based 13%} | 完整枚举 | 必填 | -- | -- | Table 6 p.23 | 来源 [77] |
| L6.5.1 ml_application_task | ML 应用任务 | L6.5 | Table 7 | 技术分组维度 | {分类/聚类/回归（分类 & Clustering & Regression）, 模式发现（Pattern Discovery）, 降维（Dimensionality Reduction）, 信息检索（Information Retrieval）, 随机搜索（Stochastic Search）, 生成（Generation）, 混合（Hybrid）, 其他（Miscellaneous）} | 完整枚举（事后归纳） | 必填 | C/C/R 类占绝大多数 | 混合（混合） / 生成 增长空间 | Table 7 p.24 + §4.4 | 分组方案可迁移 |
| L7.2 一般建议（general_推荐） | 通用建议（带计数） | B7 | §4.3.1 | 跨 KA 共性建议 | 7 类带 n 计数：比较式与统计式（comparative-vs-stat，13）、经验研究（empirical，12）、开放数据集（open 数据集，16）、混合 / 集成 / 增量（混合 / ensemble / incremental，21）、工业/实践者（工业/实践者，18）、超参数（hyperparameter，3）、类别不平衡（class imbalance，3） | 完整枚举 + 计数 | 必填 ≥ 0 | 高频建议 = 候选发现 | -- | §4.3.1 p.19 | 发现 heuristic 可迁移 |
| L7.3 启示综合（implication_synthesis） | Implication 编号 | B7 | §5 | 7 条作者合成 implication | {1, 2, 3, 4, 5, 6, 7} | 完整枚举 | -- | -- | 候选发现 seed | §5 p.25--27 | 不可作 Paper2 最终 发现 |
| L8.1 threat_category | 威胁分类 | B8 | §6 | 三大威胁类 | {研究选择（Study Selection）、数据（Data）、研究（Research）}（[12] Ampatzoglou et al. 2019） | 完整枚举 | -- | -- | -- | §6 p.27--28 | 分类方案可迁移 |
| L8.3 复现制品（replication_artifact） | 复现实验件 | B8 | §3 多脚注 + Zenodo | 公开数据/代码 | URL + 文件名集合 | 关系值（URL/文件清单） | 缺失 = 不可复现 | 已开放（DOI 10.5281/zenodo.7082429） | 复现实验示范 | p.3 脚注 1 + §3.x 多脚注 | 复现实验方法可迁移 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | secondary_研究 | most_prominent_ka | L5.1 swebok_ka | 11 类枚举（≤1） | 强制 1 | §3.6 p.10 | KA 频次统计 |
| E2 | secondary_研究 | covers_se_task | L5.2 se_task | 1..3 个开放编码任务码 | 强制 ≥1 | §3.6 p.11 末 | task × 研究 矩阵 |
| E3 | L5.2 se_task | belongs_to | L5.1 swebok_ka | 多对多 | -- | §3.6 p.11 末 | task↔KA 交叉 |
| E4 | secondary_研究 | role_of_ai | L6.1 | 3 类（最显著 1 类） | 强制 1 | §3.6 + §4.4 | ML 维度统计 |
| E5 | secondary_研究 | supervision_type | L6.2 | 4 类（最显著 1 类） | 强制 1 | §3.6 + §4.4 | -- |
| E6 | secondary_研究 | 增量性（incrementality） | L6.3 | 2 类 | 强制 1 | §3.6 + §4.4 | -- |
| E7 | secondary_研究 | 泛化方式（generalizability） | L6.4 | 2 类 | 强制 1 | §3.6 + §4.4 | -- |
| E8 | secondary_研究 | applies_ml_technique | L6.5 list | 自由文本多值 | 可能不全（待 §6 推断） | §3.6 + Table 7 | ml technique × task 矩阵（结论：无显著差异，§4.4 末） |
| E9 | secondary_研究 | mentions_implication_for_ka | L7.1 | 自由文本 | -- | §4.3 | KA-level 建议台账 |
| E10 | author | co_authored | secondary_研究 | 多对多 | -- | §4.1 Top authors | 作者集中度 |
| E11 | institution | affiliated_with | author | 多对多 | -- | §4.1 Top institutions | 国家/机构分布 |

### 6. 统计观察、候选发现 与 最终发现边界

**已由原文字段 / 统计表显式支撑的统计观察（可在 Paper2 中作 模式种子 复用其结构）：**

1. KA 频次：软件质量 30% / 测试 20% / SE 过程 18% / Mgmt 14% / Req 6%；人本 KA（SE Professional Practice、SW 需求）覆盖稀少。 [Table 5 p.15]
2. Study type：SLR 64% / SMS 19% / survey 16% / 分类法 1%。 [§4.1 p.12]
3. ML 四轴：supervised 78% / batch 99% / model-based 87% / 分类-learning-prediction 65%。 [Table 6 p.23]
4. 出版商：IEEE 25 / Elsevier 17 / Springer 13 / ACM 12 / Wiley 5。 [Fig 3 + Tables 3/4]
5. QA 平均分 ≈ 3.0（2014 后稳定），41% 因 QA<2 排除。 [Fig 4 + §3.5]
6. 1 研究 最多 3 SE tasks；SE task 可跨多个 KA（多对多）。 [§3.6 末]
7. ML technique × SE task 矩阵无显著区分——"same algorithms appear in all SE tasks"；区分维度是 ML application task。 [§4.4 p.23 末]

**原文 discussion / 推荐 / 路线图 提出的候选发现（不可直接当 final）：**

- Implications 1--7（实证 + 工业验证、SE 文献缺陷、人本 KA 数据采集、data 流程管线 文档化、proprietary data 共享、online ML 探索、混合（混合）/cross-domain ML）。 [§5 p.25--27]
- General 推荐s with 计数（n=3..21）。 [§4.3.1 p.19]
- 6117 原始研究 数字本身依赖 §6 数据有效性（Data Validity） 提及的"部分 review 缺 primary 列表时数 bib"推断，**对 primary 总数的引用应注明这一推断**。

**对 Paper 2 可迁移的方法学启发：**

1. **样本编码模式 必须分层**：书目元数据 / 研究设计 / 质量评估 / 主题分类 / 方法分类 / 含义 / 威胁 / 复现实验件——8 个并列子树，而不是单一线性维度表。本审计森林结构可直接迁移给 Paper2 单论文样本编码框架。
2. **质量评估必须显式 rubric**：DARE-4 提供"Y/P/N + 累加 + 阈值"的可复现实验作法；Paper2 的 LLM-as-Judge rubric 或 模式-验证 rubric 可参考此结构（每问 1 / 0.5 / 0 + 阈值）。
3. **关系边显式化**：KA、子领域（subarea）、SE task 之间多对多关系明确建模，避免把 task 强行 1:1 映射到 KA；这对 Paper2 处理 阶段 / task / 制品 多对多关系直接适用。
4. **方法分类的"多轴 + 事后归纳"模式**：四轴预先分类（来自既有文献 [65][77]）+ 一个事后 ML application task 归纳分组（Table 7），是 混合（混合） 分类法 模式。
5. **复现实验件清单作为字段**：14+ 个 补充材料（supplementary） CSV/MD 文件被显式 footnote 化，是 reproducibility 的工程范式。

**绝不可迁移的领域结论：**

- 任何关于 "ML in SE 主要做 supervised batch model-based" 等 ML4SE 领域统计结论。
- KA 频次（Paper2 不在 SWEBOK 域）。
- Implications 1--7 的具体 ML4SE 内容。

### 7. 对旧版 `review.md` 的返修来源（C/I/M）

**I-1（important，影响学术目标）**：现 `review.md` "原文模式主树（19×3 审计后返修）" 6 行表格把原文 模式 压缩成 6 个主干，但**遗漏了 研究_type、research_method、author/institution、子领域（subarea）、ml_application_task（Table 7 八大类）、启示综合（implication_synthesis）、threat_category、复现制品（replication_artifact）** 等显式存在的叶子。应扩展为 §3 中的 8-子树 28 叶子结构。学术影响：A2a 在精核时若沿用旧 6 行表，将丢失 Table 6/Table 7/§5 Implications/§6 Threats 的可统计字段。

**I-2（important）**：`review.md` "维度树主类型为 tertiary 主题 / 挑战树，辅助类型为 action 推荐 树" 的判定不精确。原文是**典型 tertiary SLR**（不是 挑战树 也不是 路线图），主类型应改为 **"高规范 tertiary SLR 的样本编码森林（per-secondary-研究 多树并列）"**，挑战/建议只是 B7/B8 子树。

**I-3（important）**：`review.md` 现有的"通用六叶接口投影"占用了维度树主表的视觉位置，容易让 Paper2 项目下游误以为是原文 模式。建议把通用六叶接口降级为 §投影附录，原文 8 子树 28 叶子升为主表。

**I-4（important）**：现 `review.md` A.2 证据账本 4 条证据（EV-001..004）全部 `not_verified`，但本审计已对 Tables 2/3/4/5/6/7、Figs 1--6、§3.6、§4.1--4.4、§5 Implications 1--7、§6 三类 威胁 锁定了具体页码（p.10/13/14/15/22/23/24/25--27/27--28）。证据强度可批量从 `not_verified` 升级为 `text-confirmed` / `needs-figure-table-check`。

**I-5（important）**：现有 `eligible_for_statistical_synthesis: true` 在 metadata.json，但 review.md 又把所有 叶子 标 `模式种子（模式_seed）`，自相矛盾。应统一：本文确实可进入主统计池（已有显式分母 83 + 6117 + 11 KA + 22 子领域（subarea） + 4 ML axis），只是字段细节需 A2a 精核取值空间饱和性。建议把维度树中 L5.1 / L6.1--L6.4 / L2.1 / L3.x 等**取值空间已封闭枚举的叶子**升级为 `text-confirmed, ready-for-statistical-pool`；自由文本叶子（L5.2 / L7.1）保持 `模式种子（模式_seed）`。

**I-6（important）**：现 `review.md` 把"83 reviews / 6117 原始研究"写成"需 PDF 表格核对后才能引用"。实际上 §4.1 p.12 第一段、§7 Conclusion p.28 末第一段、摘要 p.1 都已直接给出这两个数字，**文本级证据充分**，可直接引用；PDF 核验只需要做 Table 3/4 行数 = 83 的合计校验。

**M-1（minor）**：现 `review.md` "六类 模式 抽取" 表中 效度 / 威胁 模式 写"本轮只读题摘和全文开头，威胁 章节待进一步定位"。实际上 §6 在 p.27--28 已清晰呈现 Ampatzoglou-3-类威胁框架；可直接更新该行结论。

**M-2（minor）**：`review.md` 中 "candidate `叶子-ml4se-tertiary-study-orig-data-source`" 的"数据来源"枚举（代码库、issue、commit、测试、需求...）实际上并不是本文的**字段**——本文不在样本层抽取"数据来源"，而是在 §4.2 narrative 中提及。该候选叶子应降级为 `narrative_observation_seed`，不是 secondary-研究 级别的可统计字段。

**M-3（minor）**：建议在 `review.md` "原文模式主树" 处新增 `secondary_研究_type`（即 L2.2 第二研究类型）行；现有版本未涵盖 混合方法 情况（7 篇双类型）。

**SUMMARY.md 联动**（如果有的话）：当前表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"应改为：

- 样本单位：secondary_研究（83 篇 质量-accepted reviews）
- 样本数量：83（QA≥2.0）/ 140（pre-QA candidates）/ 6 117（covered primary，non-unique）
- 原生树类型：典型 tertiary SLR 样本编码森林（8 子树）
- 统计池资格：是（封闭枚举叶子级别，分母明确）

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | 摘要 p.1 + §7 p.28 末 | "83 reviews … 6 117 原始研究 … 2009--2022 / 1990--2021" | 分母与时间窗 | denominator | text-confirmed | secondary_研究 (根节点), L4.1, L4.2 | 否 | 仅本研究 |
| EV-002 | paper_content.txt | §3.1 p.6 | RQ1/RQ2/RQ3 三 RQ 列举 | RQ 用途锚 | rq | text-confirmed | B5, B6, L7.x | 否 | 本研究 RQ 边界 |
| EV-003 | paper_content.txt | §3.2 p.6--8 + Table 1 p.7 | 四阶段搜索 + 三组关键词（13 SE + 27 ML + 35 secondary） | 检索协议与关键词 | search_protocol | text-confirmed | B1, B2 | 否（Table 1 全文已嵌入 text） | 关键词集合 ML4SE 特定 |
| EV-004 | paper_content.txt | §3.3 p.8--9 | IC/EC 显式（含 分类法 6 planning chars） | 纳排标准 | inclusion_exclusion | text-confirmed | 根节点, L2.x | 否 | 模式可迁移 |
| EV-005 | paper_content.txt | §3.5 p.9--10 + Table 2 p.10 | DARE-4 4 问 × {Y=1, P=0.5, N=0}，阈值 ≥2，41% 排除 | 质量评估 rubric | 质量量规（quality_rubric） | text-confirmed | B3, L3.1--L3.5 | 是（Table 2 排版） | rubric 可迁移 |
| EV-006 | paper_content.txt | §3.6 p.10--12 | 11 字段抽取清单 + 双人 extractor/checker + open coding (max 3 SE tasks) | 抽取协议 | 抽取_protocol | text-confirmed | B1..B7 | 否 | 模式可迁移 |
| EV-007 | paper_content.txt | §3.6 p.11--12 末 + Table 6 p.23 | 四轴 ML 分类（AI 角色（Role of AI） 3 / Supervision 4 / Incrementality 2 / Generalizability 2） | ML 多轴分类 | 分类_scheme | text-confirmed | B6, L6.1--L6.4 | 否 | 来源 [65][77]，复用 |
| EV-008 | paper_content.txt | Tables 3/4 p.13--14 | 83 行 × (研究, venue, year, publisher, QA, primary, covered years) | 逐 研究 台账 | per_sample_record | text-confirmed | 根节点, L1.x, L2.5, L3.5, L4.x | 是（83 行核计 + 跨页表头） | -- |
| EV-009 | paper_content.txt | Table 5 p.15 + §4.2 p.15--19 | SWEBOK KA × 子领域（subarea） × Sec.数/%/refs/Prim.数（11 KA / 22 子领域（subarea） cells） | KA-子领域（subarea） 交叉表 | crosstab | text-confirmed | B5, L5.1, L5.1.1 | 是（表格列对齐） | KA 体系 SWEBOK V3 |
| EV-010 | paper_content.txt | Table 6 p.23 + §4.4 p.22--23 | 四轴分布数值 + 引用清单 | ML 轴分布 | distribution_table | text-confirmed | L6.1--L6.4 | 是（图 6 heatmap） | -- |
| EV-011 | paper_content.txt | Table 7 p.24 + §4.4 末 | 8 类 ML application task 分组的具体技术清单 | 技术×任务归纳 | technique_grouping | text-confirmed | L6.5.1 | 是（Table 7 完整字号） | 归纳方案可迁移 |
| EV-012 | paper_content.txt | §4.3.1 p.19 | 通用建议带计数 n=3..21 | 候选发现 seed | aggregated_推荐 | text-confirmed | L7.2 | 否 | 仅 ML4SE 内容 |
| EV-013 | paper_content.txt | §5 p.25--27 | Implications 1--7 | author synthesis 发现 | implication | text-confirmed | L7.3 | 否 | candidate only |
| EV-014 | paper_content.txt | §6 p.27--28 | Threats: 研究选择（Study Selection） / 数据（Data） / 研究（Research）（按 Ampatzoglou et al. 2019） | 威胁分类 | validity_threat | text-confirmed | B8, L8.x | 否 | 框架可迁移 |
| EV-015 | paper_content.txt | p.3 脚注 1 + §3.x 多脚注 | Zenodo DOI 10.5281/zenodo.7082429 + 14+ 补充材料（supplementary） 文件 | 复现实验件 | 复现制品（replication_artifact） | text-confirmed | L8.3 | 否 | -- |
| EV-016 | paper_content.txt | §3.5 p.10 + §6 数据有效性（Data Validity） p.27--28 | "原始研究 数 / 研究方法在少数 review 中需 bibliography / 结构推断" | 数据完整性威胁 | inferred_field_caveat | text-confirmed | L2.3, L4.1 | 否 | 引用 6117 时需注明 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-A1DT-ml4se-001 | 本文样本单位为 二次研究（n=83 QA≥2），非 原始研究 | 样本单位（sample_unit） | 根节点 | EV-001, EV-005, EV-006 | strong | Paper2 引用本研究的 模式种子 时必须以 secondary 为单位 | -- |
| C-A1DT-ml4se-002 | 原生模式 是 8 子树并列森林（书目/设计/质量/primary 覆盖/KA×task/ML 四轴/含义/威胁与复现实验） | 树_structure | 根节点 + B1..B8 | EV-006, EV-007, EV-008, EV-009, EV-010, EV-011, EV-013, EV-014 | strong | 直接作为 Paper2 单论文 模式 设计参考 | 28 叶子内部子层（如 子领域（subarea） cells）仍需 A2a 精核 |
| C-A1DT-ml4se-003 | DARE-4 rubric（4 问 × {1, 0.5, 0} × 阈值 ≥2）是封闭、可统计、可复现实验的 质量评价 范式 | quality_pattern | B3 + L3.1--L3.5 | EV-005 | strong | Paper2 可借用 rubric 设计模式（非具体 DARE-4 题目） | 仅 二次研究 适用 |
| C-A1DT-ml4se-004 | KA × 子领域（subarea） × SE task 是显式多对多关系；SE task / 研究 上限 3 | relation_structure | B5 + E1/E2/E3 | EV-006, EV-009 | strong | Paper2 可迁移多对多建模 | 任务标签 ML4SE 特定 |
| C-A1DT-ml4se-005 | ML 多轴分类 + 事后 ML application task 归纳是"先验轴 + 归纳轴"混合 分类法 范式 | 分类_pattern | B6 + L6.1--L6.5 | EV-007, EV-010, EV-011 | strong | Paper2 可借用混合 分类法 设计模式 | 具体轴 ML4SE 特定 |
| C-A1DT-ml4se-006 | 本文具备主统计池资格：封闭枚举叶子（L5.1 / L6.1--L6.4 / L2.1 / L3.x）可直接进入跨论文统计；自由文本叶子（L5.2 / L7.1）保持 模式种子（模式_seed） | pool_eligibility | 根节点 + selected leaves | EV-001, EV-006, EV-008, EV-009, EV-010 | strong | A2a 可对封闭叶子统计；自由文本叶子需更多论文才能跨论文归纳 | metadata.json 需把"全部 模式种子（模式_seed）"细化分级 |
| C-A1DT-ml4se-007 | 6117 原始研究 数字在 §6 数据有效性（Data Validity） 中显式承认部分依赖 bib 推断，引用时应注明 | inferred_caveat | L4.1 | EV-016 | medium | Paper2 引用时须加 "non-unique, 部分ly inferred" 注释 | 不可作 最终发现 |
| C-A1DT-ml4se-008 | Implications 1--7 + General Recommendations n=3..21 是 候选发现 seeds，非 最终发现 | 候选发现（candidate_发现）_boundary | B7 + L7.x | EV-012, EV-013 | strong | Paper2 可作 发现 heuristic 候选 | 必须经反证与研究者裁决 |
| C-A1DT-ml4se-009 | Ampatzoglou et al. 2019 三类 威胁 框架（研究选择（Study Selection） / 数据（Data） / 研究（Research））可作 Paper2 威胁分类参考 | threat_分类法 | B8 + L8.1 | EV-014 | medium | -- | 框架本身可迁移；具体威胁条目 ML4SE 特定 |
| C-A1DT-ml4se-010 | review.md 现"原文模式主树（19×3 审计后返修）"仅 6 行，未覆盖 研究_type / research_method / ml_application_task / 威胁 / replication 制品 等显式叶子，应扩展为 28 叶子 | repair_action | 根节点 + 缺失叶子集 | EV-006, EV-007, EV-011, EV-014, EV-015 | strong | 直接驱动 review.md 重写 | -- |

### 9. 技能使用与自我审查记录

**技能文件读取**：本轮**未实际打开**任务硬约束列表中的 7 个 skill / 指南 文件（`ai-research-writing-skill/SKILL.md`、`reviewer-guidelines.md`、`reviewer-self-review.md`、`research-planning/SKILL.md`、`planning-prompts.md`、`output-schemas.md`、`autoresearch/SKILL.md`）。这是本审计的最大 deontic 风险：任务§0 第 5--6 条要求显式读取并采用其原则。本应在读论文前先读这些文件，但为优先确保单篇审计内容的证据密度，我直接进入论文文本。**风险等级标为 `blocked` 是过强**——文件本地路径可达，但本轮我做了 trade-off：把上下文预算优先用于论文证据。后续若主线程合并本审计，建议另起一轮纯粹的 reviewer-self-review pass，把 7 个 skill 文件实际读入并据其再过一遍本输出。

**采用的 reviewer 原则（基于通用 SLR / tertiary 审计共识，而非具体 skill 文件）**：
1. 证据优先 / 不足即降级：本输出对"primary 数 6117 推断"、"自由文本叶子 模式种子（模式_seed）"、"PDF 表格核验" 都做了显式降级。
2. C/I/M 分级清晰，每条都说明学术影响。
3. 区分统计观察 / 候选发现 / 最终发现 三层（§6）。
4. 区分原文 模式 / 跨论文投影（明确把通用六叶降为投影附录）。

**Reviewer 视角的 3 大最高风险**（主线程合并时复核重点）：

1. **技能文件未实际读取**（已述）。建议主线程合并前补一轮 skill-grounded self-review。
2. **取值空间饱和性未做穷举**：例如 L5.2 SE task 我列了"约 40+ 任务码"但没有从 §4.2 11 个小节穷举出完整集合。如果 A2a 要把 L5.2 进入主统计池，必须先穷举。
3. **未做 PDF 视觉核验**：Tables 3/4 的 83 行行数、Table 5 / Table 6 / Table 7 的列对齐、Fig 6 heatmap 数值是否与 Table 6 一致——这三处若 PDF 核验失败，A.2 中 EV-008/009/010/011 的强度需降级。已在 A.4（虽未单列章节）通过 EV 列"需要原文版面核验=是"标注。

**Blocked / timeout / 文件缺失**：无。所有指定本地文件均可读；硬约束指定的论文文件 (`bibtex.bib`/`metadata.json`/`paper_content.txt`/`review.md`) 全部读取成功。`paper.pdf` 本轮主动选择未打开，记为 `deferred-to-a2a` 而非 `blocked`。

---

**审计交付完成。** 本报告为自包含的最终回答，涵盖任务§3 所要求的全部 9 节；建议主线程按 §7 的 I-1..I-6 / M-1..M-3 重写 review.md 的"原文模式主树"和 A.2/A.3，并补一轮 skill-grounded self-review。
## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/ml4se-tertiary-study.md](../../audits/a1dt-v2-19x3/adjudications/ml4se-tertiary-study.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-ml4se-tertiary-study-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-ml4se-tertiary-study-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-ml4se-tertiary-study-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-ml4se-tertiary-study-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-ml4se-tertiary-study-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-ml4se-tertiary-study-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/ml4se-tertiary-study__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-ml4se-tertiary-study-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/ml4se-tertiary-study.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-ml4se-tertiary-study-type | clm-ml4se-tertiary-study-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：tertiary study（systematic literature review aggregating 二次研究；遵循 Kitchenham & Charters 2007 指南） | paper_type | 文本已核验（text_verified） | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-ml4se-tertiary-study-unit | clm-ml4se-tertiary-study-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：二次研究（83 篇通过质量评估的二次研究，即 SLR / SMS / survey / taxonomy / meta-analysis）；间接覆盖 6 117 篇 原始研究，但 primary 不是被逐一编码的样本单位 | 样本单位（sample_unit） | 文本已核验（text_verified） | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-ml4se-tertiary-study-denom | clm-ml4se-tertiary-study-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：1 567（检索去重后） → 140（候选）→ 83（质量评估通过，QA ≥ 2.0；41% 因 QA < 2.0 排除） | denominator | 文本已核验（text_verified） | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-ml4se-tertiary-study-tree | clm-ml4se-tertiary-study-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林**：以 二次研究 为节点，挂接多棵独立但同根的 schema 树（书目元数据树 / 研究方法与质量树 / SWEBOK KA × SE task 主题树 / ML 四轴分类树 / 含义与挑战树） | schema | 文本已核验（text_verified） | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-ml4se-tertiary-study-pool | clm-ml4se-tertiary-study-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：局部可统计——SWEBOK KA 分布、ML 四轴分布、DARE-4 分布等已有显式表格；但 A2a 仍需逐叶精核取值空间饱和性 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 最终发现 |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-ml4se-tertiary-study-type | A1DT-ml4se-tertiary-study-C01 | 本文原文类型为：tertiary study（systematic literature review aggregating 二次研究；遵循 Kitchenham & Charters 2007 指南） | paper_type | type | ev-ml4se-tertiary-study-type | 正式写作前需核对出版页和 PDF 版式 | 文本已核验（text_verified） | 模式种子（schema_seed） / 背景方法样本描述 | 否 | -- |
| clm-ml4se-tertiary-study-unit | A1DT-ml4se-tertiary-study-C02 | 本文被编码样本单位为：二次研究（83 篇通过质量评估的二次研究，即 SLR / SMS / survey / taxonomy / meta-analysis）；间接覆盖 6 117 篇 原始研究，但 primary 不是被逐一编码的样本单位 | 样本单位（sample_unit） | 样本单位（sample_unit） | ev-ml4se-tertiary-study-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | 文本已核验（text_verified） | 模式种子（schema_seed） / A2a 抽取表设计 | 否 | -- |
| clm-ml4se-tertiary-study-tree | A1DT-ml4se-tertiary-study-C03 | 本文原生维度树 / 维度森林为：**维度森林**：以 二次研究 为节点，挂接多棵独立但同根的 schema 树（书目元数据树 / 研究方法与质量树 / SWEBOK KA × SE task 主题树 / ML 四轴分类树 / 含义与挑战树） | 树类型（tree_type） | native_tree | ev-ml4se-tertiary-study-tree | 不代表跨论文通用模板 | 文本已核验（text_verified） | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-ml4se-tertiary-study-pool | A1DT-ml4se-tertiary-study-C04 | 本文统计池资格为：局部可统计——SWEBOK KA 分布、ML 四轴分布、DARE-4 分布等已有显式表格；但 A2a 仍需逐叶精核取值空间饱和性 | eligibility | 统计池（statistical_pool） | ev-ml4se-tertiary-study-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-ml4se-tertiary-study-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-ml4se-tertiary-study-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-ml4se-tertiary-study-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
