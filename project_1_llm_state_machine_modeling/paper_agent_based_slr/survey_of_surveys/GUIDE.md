# survey_of_surveys/GUIDE.md：综述之综述脚手架维护规则

## 1. 目标与边界

本目录的目标是建立可维护的综述之综述脚手架，帮助后续 A2a / A2b 从软件工程 SLR/SMS/survey 文献中抽取模式先验。它不追求 A1 阶段数量完备，也不把脚手架样本写成目标领域证据。

所有结论必须回到原文或可靠元数据。若只读题名、摘要或元数据，只能写候选线索，不能写成已核验模式。

## 2. 检索策略

A1 只做种子检索和 dry-run；A2a/A2b 才做大规模闭合。A1 检索记录必须写入 [search/search-log.md](./search/search-log.md)，候选条目写入 [search/candidate-pool.md](./search/candidate-pool.md)。

推荐关键词簇：

1. `software engineering systematic literature review tertiary study`。
2. `software engineering systematic mapping study guidelines`。
3. `software engineering survey systematic review quality assessment`。
4. `evidence based software engineering systematic review guideline`。
5. `SLR SMS software engineering reporting threats validity`。

来源优先级：

1. DOI / 出版商页面 / 官方 PDF。
2. 作者主页或大学技术报告页面。
3. DBLP / ACM / IEEE / ScienceDirect / BCS 等索引。
4. 聚合页只作为发现线索，不能作为已核验事实。

## 3. 筛选标准

纳入必须至少满足一项：

1. 论文自身是 SE SLR / SMS / tertiary study / systematic survey。
2. 论文是 SE SLR/SMS 方法学指南或 guideline。
3. 论文能提供可抽取的 RQ、维度字段、finding、证据呈现、validity threat 或 report structure pattern。

排除或降级：

1. 无法核验题名 / 作者 / 年份 / 来源的条目。
2. 仅普通 narrative survey 且无系统检索或纳排信息。
3. 与 SLR/SMS 方法学无关的自动综述生成工具；这类条目应进入 [../baselines/](../baselines/)。
4. PDF 不可获取但元数据可靠的条目可保留为 `metadata-only`，不得进入已采纳 pattern。

## 4. 证据等级与阅读状态

阅读状态说明“读到哪里”，证据等级说明“能支撑多强的脚手架结论”。二者必须分开记录。

| 阅读状态 | 含义 | 可写边界 |
|---|---|---|
| `未读原文-仅题摘粗筛` | 只读题名、摘要、元数据 | 只能写候选相关性。 |
| `已读全文文本-paper_content核验` | 已读 `paper_content.txt` 的摘要、方法、结果、结论等关键部分 | 可写全文级 pattern，但图表/表格数值需标注待 PDF 核对。 |
| `已回PDF核对图表` | 已人工打开 PDF 核对关键图表、表格、公式或版式 | 可支撑图表级细节。 |
| `全文不可得-待人工下载` | 合法 PDF 未获取 | 只能保留元数据、下载尝试和候选理由。 |

| 证据等级 | 适用条件 | 写作边界 |
|---|---|---|
| `题摘级` | title / abstract / metadata | 不支撑 pattern 采纳。 |
| `全文文本级；图表待人工核对` | 已读 `paper_content.txt` 关键正文 | 支撑 A1 dry-run pattern；正式数字需 PDF 核对。 |
| `PDF图表级` | 已打开 PDF 核对关键图表/表格 | 可支撑图表/数值级 pattern。 |
| `全文不可得` | PDF 未获取或无法合法访问 | 只进入 manual-download / metadata-only。 |

## 4.1 出版形态、Venue 与 CCF 官方字段

后续 [SUMMARY.md](./SUMMARY.md)、[search/candidate-pool.md](./search/candidate-pool.md) 和每篇 `papers/<slug>/review.md` 的快速结论卡片必须显式维护以下来源字段，不能只写泛化的“来源等级”：

| 字段 | 填写规则 |
|---|---|
| `出版形态` | 写 `期刊`、`会议`、`预印本`、`技术报告`、`工作坊` 或其他可审计形态。若同一论文有 arXiv 预印本和正式出版版本，优先按正式出版版本填写，并在备注中说明 arXiv 只作为开放全文来源。 |
| `期刊/会议/预印本` | 写可点击的短名链接，例如 `[IST](https://www.sciencedirect.com/journal/information-and-software-technology)`、`[ESE](https://link.springer.com/journal/10664)`、`[EASE](https://conf.researchr.org/series/ease)`；预印本写 `[arXiv](https://arxiv.org/)`。若不是期刊 / 会议 / 预印本，应写最接近的可审计入口；实在没有稳定入口时写 `--` 并说明原因。 |
| `CCF 官方大类` | 必须从 CCF 官方最新国际推荐目录核验，默认先查 [CCF 推荐国际学术刊物目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/2024-06-28/825349.shtml) 及其各大类页面，例如 [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)。不得只因为本仓库 [../../../ccf_venues/](../../../ccf_venues/) 未建档就写未知；`ccf_venues/` 只能作为本地缓存和二次跳转入口。非 CCF venue 写 `--`。 |
| `CCF 官方等级` | 写 `A` / `B` / `C` / `--`。只有官方目录明确收录时才写等级；预印本、技术报告、非 CCF workshop / conference / journal 写 `--`。若 CCF 官方页面访问异常或需人工核验，临时写 `待核验` 并在失败记录中说明，不能用第三方镜像升级为官方事实。 |
| `CCF 复核状态` / `ccf_verification_status` | 记录该 CCF 字段是“官方页面已人工核验”“本地缓存；官方待人工复核（WAF）”“非 CCF venue”还是“待核验”。若使用本地缓存，必须说明缓存来源与访问异常类型，不能把缓存口径写成实时官方在线核验。 |
| `online_first_date` / `publication_year_basis` | 当 online-first 日期与正式卷期 / BibTeX 年份不一致时必须写入 `metadata.json`，并在 `review.md` 快速卡片说明统计年份采用哪一个口径。默认正式引用和年度统计采用正式卷期 / BibTeX 年份，online-first 只作为时间背景。 |

执行纪律：

1. CCF 大类和等级的范围必须来自 CCF 官方完整目录视角，不局限于当前 [../../../ccf_venues/](../../../ccf_venues/) 已收录的 42 个 venue。
2. 若一个 venue 属于 CCF 官方目录但本库尚未建档，仍应填写官方大类和等级，并把“本库未建档”作为后续情报库补链线索。
3. 第三方 CCF 镜像、博客、个人主页、学校主页或搜索摘要只能作为发现线索；正式字段必须回到 CCF 官方目录或显式标为 `待核验`。
4. [SUMMARY.md](./SUMMARY.md) 的总表、[search/candidate-pool.md](./search/candidate-pool.md) 的候选表和单篇 `review.md` 的快速结论卡片必须使用同一组字段，避免总账与单篇事实脱节。
5. 从 issue #95 或其他外部候选总表批量引入条目时，必须建立来源审计文件；本轮使用 [search/issue95-selection-audit.md](./search/issue95-selection-audit.md) 记录 Gist 来源、选择理由、PDF 状态、统计池资格和年份/CCF 口径。

## 5. 单篇目录规则

单篇目录最低结构：

```text
papers/<slug>/
├── bibtex.bib
├── review.md
├── paper.pdf              # 全文可得时必须有
└── paper_content.txt      # 全文可得时必须由 tools/pdf_extractor.py 生成
```

全文可得时，必须使用仓库工具生成文本：

```bash
source venv/bin/activate
python -m tools.pdf_extractor -i papers/<slug>/paper.pdf -o papers/<slug>/paper_content.txt -m text
```

若文字模式提取异常，再记录 OCR 或人工核验需求。不可获取 PDF 不得假装已读全文，必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。若一轮新增条目全部成功获取 PDF，也必须在 [search/search-log.md](./search/search-log.md) 中记录“无新增人工下载”。

## 6. 模式字段抽取规则

每篇 `review.md` 至少抽取六类 pattern：

1. RQ pattern。
2. dimension pattern。
3. finding pattern。
4. evidence presentation pattern。
5. validity / threat pattern。
6. report structure pattern。

每类 pattern 必须有：抽取结论、证据锚点、可迁移性、不可迁移点。若某类不适用，写“不适用”并说明是 `guideline`、`metadata-only`、`目标不符` 还是 `原文未报告`。


## 6.1 A1-M0--M6 元维度抽取规则

A1 之后，单篇 `review.md` 不得只填六类 pattern，还必须说明该论文对 A1-M0--M6 元维度的贡献。A1-M0--M6 是“如何构建 researcher-defined meta-model 与可审计字段证据链”的脚手架层，不是固定 SE 综述字段表。

| 层级 | 中文名 | 操作化问题 | 最低证据要求 | 典型输出 |
|---|---|---|---|---|
| A1-M0 | 研究意图与综述元模型层 | 论文如何定义 topic、RQ、scope、review type、unit of analysis、researcher gate？ | 题摘级可候选，全文文本级可采纳 | 综述元模型对象、RQ 类型、研究者裁决点 |
| A1-M1 | 语料收集与纳排层 | 论文如何定义数据库、检索式、时间范围、venue、去重、筛选、全文状态、排除理由？ | 全文文本级 | 检索 / 纳排字段、PRISMA 或等价分母、失败路径 |
| A1-M2 | 研究对象与主题语义层 | 论文如何划分 SE 子领域、生命周期阶段、研究对象、工件、任务、场景？ | 全文文本级 | 主题 / 对象 taxonomy、scope tree |
| A1-M3 | 方法 / 技术 / 干预层 | 论文如何分类方法、工具链、LLM / agent 角色、自动化程度、human-in-the-loop 点？ | 全文文本级 | method taxonomy、agent role、intervention field |
| A1-M4 | 评价、证据与复现资产层 | 论文如何记录 metrics、dataset、baseline、artifact、source anchor、replication package、evidence strength？ | 全文文本级；artifact 字段需链接核验 | 评价字段、制品资产字段、证据锚点字段 |
| A1-M5 | 统计分析就绪层 | 字段是否有版本、取值空间、缺失值语义、可交叉统计字段、回填状态？ | 全文文本级 | 可统计字段表、分母定义、missing-value semantics |
| A1-M6 | research finding 形成与裁决层 | 论文如何从统计观察形成 candidate finding、support / counter-evidence、claim strength、scope、researcher adjudication？ | 全文文本级 | finding heuristic、claim strength、裁决日志候选 |

执行规则：

1. 每篇 `review.md` 必须有 “A1-M0--M6 元维度贡献”小节；若某层不适用，写明 `不适用` 和理由。
2. A1-M0--M6 只能记录“模式先验 / 候选字段 / 启发式”，不能直接生成目标领域 finding。
3. Roadmap、vision、research commentary 可以贡献 A1-M0、A1-M3、A1-M6 或 report/finding heuristic，但如果没有系统检索和纳排，不得贡献 A1-M1 的已采纳 SLR/SMS pattern。
4. 若某个字段来自题摘级或自动结构统计，只能标为 `候选` 或 `待全文核验`；不得进入已采纳 pattern。
5. 每个可采纳字段必须同时有来源论文、证据锚点、适用条件、不适用条件和缺失值语义。

## 6.2 #95 现代维度锚点全文阅读规则

issue #95 的 10 篇现代锚点必须遵守“一篇一 subagent”原则：每个 subagent 只能读自己负责的 `bibtex.bib`、`metadata.json`、`paper_content.txt` 和必要 PDF，不得混读多篇，也不得开启 sub-subagent。`review.md` 必须显式写明是否已读全文、是否回 PDF 核对图表、是否只做 metadata-only。

新增锚点的 `review.md` 最低结构：快速结论卡片、论文内容详读、六类 pattern、A1-M0--M6 元维度贡献、可迁移字段树 / 维度锚点、对 Paper2 的启发与风险、待复核。快速卡片必须明确“是否已读全文”“是否回 PDF 核对图表”“是否只做 metadata-only”，避免把粗筛结论误写成全文审查结论。

## 7. schema 回修闭环

`patterns/pattern-field-schema.md` 是 A1 的脚手架字段合同，但不是不可改的先验。dry-run 暴露缺口时必须执行：

1. 在单篇 `review.md` 的“schema 缺口 / 不可迁移点”中记录触发原因。
2. 回修 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 的字段定义、取值空间、证据要求或缺失值语义。
3. 在 [SUMMARY.md](./SUMMARY.md) 的“schema 修订 / 回填日志”记录受影响条目、回填状态和冻结理由。
4. 若不回修，必须说明为什么该缺口留给 A2a/A2b。

## 8. SUMMARY.md 回填规则

[SUMMARY.md](./SUMMARY.md) 必须至少维护：

1. 当前状态和 A1 边界。
2. 证据等级口径。
3. 检索关键词簇分析。
4. 论文列表和相对路径链接。
5. dry-run 覆盖矩阵。
6. 脚手架模式总表。
7. schema 修订 / 回填日志。
8. 失败、阻塞与人工下载清单。
9. 更新时间降序日志，时间格式为 `yyyy-mm-dd hh:mm:ss`。

emoji 列只写 emoji；中文释义放在表格外。

## 9. dry-run 验收规则

A1 的 3--5 篇 dry-run 必须满足：

1. 至少覆盖 SLR / SMS / tertiary review / guideline 中的 2 类。
2. 至少 1 篇高等级来源、1 篇非 A 或非顶级来源。
3. 至少 1 篇非 LLM4SE 的 SE 子领域或泛 SE 方法学样本。
4. 六类 pattern 中至少 4 类被全文样本实际填充。
5. 至少 1 个字段展示“不可填 / 不适用 / 证据不足”的降级记录。
6. 若 schema 暴露缺口，必须完成回修或登记留给 A2a/A2b。

## 10. 禁止写法与拒收检查

禁止写法：

- “首次自动化系统综述”。
- “完整覆盖”。
- “替代专家”。
- “PRISMA-compliant”。
- “100+ 篇完整文库完成”。
- “脚手架样本证明目标领域 finding”。

A1 完成前至少运行：

```bash
git diff --check
rg -n "首次自动化|PRISMA-compliant|完整覆盖|替代专家|100\+ 篇完整文库完成" project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys || true
```
