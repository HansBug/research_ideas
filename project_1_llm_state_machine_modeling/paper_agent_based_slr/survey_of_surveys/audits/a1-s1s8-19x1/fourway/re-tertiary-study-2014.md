# re-tertiary-study-2014：A1-S1S8 四分栏提取

## 总体统计池裁决

裁决：本文可保留为后续主统计池候选与 `schema_seed`，但 A2a 页码、图表和附录逐项视觉核验前，不进入最终定量统计。主样本单位必须写为 **53 distinct SLR studies / systematic reviews**，并与 **64 publications** 分开；质量评价分母为 51 studies（S3、S8 全文不可得）。`topic group` 只能写成作者基于标题/摘要主题分析得到的约 24 个观察分组，不是封闭、可外推的 RE 全域 taxonomy。S8 仅为中等：有第一作者分组、另外两位作者复核命名和 limitations 自我质疑，但没有完整双人独立筛选/抽取/QA 裁决、分歧日志或 $kappa$。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | `paper_content.txt` 摘要与 §II 明确本文按 EBSE guidelines 做 RE 领域 tertiary study；§II.A 给出 RQ1--RQ3：覆盖领域、SLR 质量、覆盖缺口。 | 根任务是对 RE 相关 SLR/SMS/meta-analysis 的三级映射；RQ 树驱动后续 topic、QA、gap 三组分析。 | 强；可进入“tertiary review task / RQ tree”统计池候选。 | 核对 PDF 中标题、摘要、§II 标题和 RQ1--RQ3 页码；确认 “Systematic Mapping Tertiary Study” 与 “tertiary study” 表述。 |
| S2 语料收集与筛选 | §II.A 描述 5 个数据库、snowball、既有 tertiary studies 参考文献与 RE/SLR venue 手工检索；Table II 给出 `267→91→58→64 publications→53 studies`，正文称 secondary searches found 5 SLR，但 Table II/final arithmetic 为 +6 publications。 | 检索漏斗应分 publication 与 study 两级：primary hits / included papers / duplicate-discarded publications / final distinct studies；纳入标准为英语、SLR/SMS/meta-analysis、RE 主题。 | 强但有内部不一致标注；可作为筛选漏斗候选，不能混淆 distinct reviews 与 publications。 | 视觉核 Table II 数字、secondary search 六行、正文 “5 SLR” 与表格 “6 publications” 的差异；核对 S3/S8/S40 缺失说明。 |
| S3 原生维度树/样本编码对象 | §II.A 说明同一 study 的多 publication 用同一 S-ID 加 A/B/C 后缀；抽取 publication details、citation、#PS、focus；Table III--VI、Appendix A 给出类型、scope、topic、QA/citation 和 S1--S53 名录。 | 原生对象是去重后的 distinct SLR study；维度森林包括 publication metadata、SLR 抽取信息、scope 分类、topic group、DARE QA rubric、citation/impact、gap taxonomy、检索执行聚合。 | 强；可作为原生维度森林/样本编码对象统计池候选。 | 核对 Appendix A 的 S-ID 与 A/B/C 分组、64 publications 到 53 studies 的映射；确认 Table III--VI 是否跨页漏列。 |
| S4 字段级证据 | Table I 给出 QA1--QA4 三档评分；Table III publication type、Table IV scope、Table V topic/#PS/year、Table VI citation/QA；Appendix A 给出完整参考与 citation。 | 叶子层可复原为标题/作者/年份/类型/venue/citation、#PS、focus、SLR subtype、scope、topic group、QA1--QA4/total、gap type、limitations。 | 中到强；字段结构可入候选池，但数值与样本级映射在 A2a 前不得升级为最终定量证据。 | 逐项核对 Table I--VI、Appendix A 的列名、数值、脚注 `NM/NF`、S26/S39 重叠星号和 OCR 断行。 |
| S5 维度模式演化 | §II.A 说明搜索词经过 pilot testing，并参考既有 tertiary studies 和 RE SLR 扩展关键词；limitations 说明 topic 从标题/摘要抽取，由第一作者分组，两位作者复核并同意最终名称。 | 可复原为“关键词扩展/主题分组命名的形成过程”，不是正式 codebook 迭代、开放编码饱和或 schema evolution。 | 中；可作维度形成机制边界样本，不宜并入“显式维度演化”主统计池。 | 核对 §II.A pilot/search-string 段和 §IV topic grouping 段；避免把 QA 年度趋势或 gap analysis 误写成维度演化。 |
| S6 统计分析 | §III 报告 64 publications 的类型分布、53 studies 的 SLR/SMS/meta-analysis 分布；Table IV 给 scope 33/7/7/4/1/1；Table V 给 #PS 极差与 topic；§RQ2/Fig.2--4 给 QA 分布与年度趋势；Table VI 给 Top-10 citation。 | 统计由字段森林派生：publication type、study subtype、scope、topic/#PS、QA、citation、year trend、gap count/类型均有字段来源。 | 强；可作为“字段→统计观察”候选，但所有图表数值仍限 A1 文本级。 | 视觉核 Figure 1--4 柱高/曲线、Table IV--VI 数值，尤其 `42/51 ≥ 2`、Top-10 citation/QA、#PS 极值和区间。 |
| S7 候选 finding | §III RQ3 与 Conclusion 形成候选发现：RE SLR 质量 2009 后下降、高引不等于高 QA、#PS 内部矛盾、低 #PS 可能指向 neglected areas 或检索不足、若干 RE roadmap topic 未被 SLR 覆盖、近半 SLR 忽略 QA3/QA4。 | 应区分可重算统计观察、作者 discussion/gap analysis 与 RE 历史领域结论；finding 只在 RE tertiary 语境内成立。 | 强但限界；可作为“统计观察→候选 finding / gap taxonomy”模式候选，不能迁移具体 RE topic 结论。 | 核对 §RQ3 三类 gap、Conclusion、Cheng/Atlee 与 Nuseibeh/Easterbrook roadmap 对照；标明 2006--2014 与 RE-only 限制。 |
| S8 研究者/作者质疑与裁决 | §IV limitations 记录检索漏检风险、S40 缺 publication details、topic grouping 主观、QA guideline 依赖和 gap analysis 不完整；topic 命名由第一作者分组、另外两位作者复核同意。 | 可复原为作者自我质疑 + topic 命名复核；没有完整多研究者独立筛选/抽取/质量评价、disagreement resolution、inter-rater agreement 或 kappa。 | 中；可作为“复核/limitations 机制”候选，但必须降级，不能按完整 adjudication/coding reliability 统计。 | 核对 §IV 全段、是否存在未被 OCR 标出的 threats/validity 段；确认无独立双人筛选、抽取或 QA 裁决日志。 |

## 建议降级 / 修正

- S2：保留强，但必须显式写清 `53 distinct SLR studies` 与 `64 publications` 两套分母；正文 “secondary searches found 5 SLR” 与 Table II “+6 / total publications 64” 保留为待核内部不一致。
- S5：从“强维度演化”降为“中”；原文只支持 search-term pilot、关键词扩展、主题分组命名与复核，不支持完整 schema evolution。
- S8：保持“中”；有 limitations 和 topic naming review，但无完整双人独立筛选/编码/QA 裁决证据。
- topic group：统一写为约 24 个观察分组，且作者自承分类不 exhaustive/complete；不得作为封闭 RE taxonomy 或跨领域统计口径。
