# survey_of_surveys/GUIDE.md：综述之综述脚手架维护规则

## 1. 目标与边界

本目录的目标是建立可维护的综述之综述脚手架，帮助后续 A2a / A2b 从软件工程 SLR/SMS/survey 文献中抽取模式先验。它不追求 A1 阶段数量完备，也不把脚手架样本写成目标领域证据。

本目录对 Paper2 的长期口径是：**以系统文献综述（systematic literature review，SLR）及类 SLR 证据综合为主目标，以更广义的软件工程二次研究作为方法脚手架**。也就是说，Paper2 最终要优先服务“研究者定义元模型后，如何用 LLM/agent 支撑可审计、可迭代的 SLR”；系统映射、混合文献综述、三级研究、方法指南、路线图和愿景论文可以入库，但它们的角色必须显式降级或分池：系统检索且有纳排、编码、字段抽取、统计观察的论文可作为主统计池候选；指南、路线图、愿景、方案论文（proposal）等主要作为方法学参考、维度模式种子、边界样本或研究发现（finding）启发，不得混入主统计池，也不得被写成目标领域最终发现。

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


## 2.A A2a `corpus/` 语料建设纪律

A2a 以后，大规模候选语料的事实真源从 A1 的 [search/](./search/) 迁移到 [corpus/](./corpus/)。维护规则如下：

1. [corpus/raw/](./corpus/raw/) 只保存原始快照；除统一换行符与行尾空白这类版本控制规范化外，不得人工改字段语义、候选数量或候选内容。
2. [corpus/tables/](./corpus/tables/) 由 [scripts/build_corpus_tables.py](./scripts/build_corpus_tables.py) 复算生成；不得手工改 CSV 后不更新脚本。
3. 主候选、替补和边界池必须互斥；每条记录必须有选择、替补或边界理由。
4. PDF 可得性只影响执行状态，不决定候选资格。未自动取得 PDF 的 core / reserve 条目必须进入 [corpus/manual-download-needed.bib](./corpus/manual-download-needed.bib)。
5. A2a 默认不批量生成正式 `review.md`；若有占位，必须显式标注未全文深读，不得计入 A2b 已完成 review。
6. A1 已有 `review.md` / `evidence_chain.md` / `metadata.json` 不得被 A2a 脚本覆盖。
7. 新增或重算语料后必须运行 [scripts/validate_corpus.py](./scripts/validate_corpus.py)。

## 3. 筛选标准

纳入必须至少满足一项：

1. 论文自身是 SE SLR / SMS / tertiary study / systematic survey，且最好能体现系统检索、纳排、编码、数据抽取、统计分析或研究发现（finding）形成过程。
2. 论文是 SE SLR/SMS 方法学指南（guideline），可用于定义流程、质量评价、报告结构、证据链和研究者关口（researcher gate）。
3. 论文能提供可抽取的 RQ、维度字段、finding、证据呈现、validity threat 或 report structure pattern。

纳入后必须立即判定其角色：`SLR 主目标样本`、`类 SLR 主统计池候选`、`方法学参考`、`维度模式种子`、`边界 / 风险样本` 或 `仅候选线索`。其中 `SLR 主目标样本` 和 `类 SLR 主统计池候选` 是后续统计分析和研究发现支撑的优先对象；其他类型可以保留，但只能按证据角色服务方法设计和边界讨论。

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

## 4.2 主表与快速结论卡片枚举口径

本目录的 [SUMMARY.md](./SUMMARY.md) 主干完整表和每篇 `review.md` 的快速结论卡片，使用受控的“emoji + 短文本”枚举表达关键类型维度。这里是本目录对仓库根级“emoji 列默认只写 emoji”规则的显式 override：只有本节规定的枚举列允许写成 `emoji + 短文本`；普通状态列仍保持 emoji-only。

执行纪律：

1. 枚举列不得临时自造标签；若需要新增类型，必须先更新本节、[SUMMARY.md](./SUMMARY.md) 的枚举说明和必要的门禁 / 总账。
2. `SUMMARY.md` 主干完整表、逐篇覆盖矩阵、维度树总览、pattern 汇总、结论-证据映射等主要分析表只统计 `统计池资格 = 🟢 入池` 的条目。
3. `🟡 待核`、`⚪ 不入`、`🔴 排除` 不得占用主干分析表；只能进入后部风险 / 边界备忘、候选池或失败记录。
4. [SUMMARY.md §2.4](./SUMMARY.md#24-主表与快速结论卡片枚举口径) 必须为每个 enum 维度维护“当前入池子集数量”或等价计数字段；新增、升级或降级论文后必须同步重算。
5. 一篇论文若有多个角色，主表只写“主角色”；次级用途写在 `review.md` 的详细说明中，避免双重计数。
6. `CCF 复核状态` 不作为第一张主表的核心枚举列；它应保留在 CCF / venue 审计说明、单篇快速卡片或后续专门核验表中。
7. 后续新增论文时，至少要同步填写：`综述类型大类`、`本文角色`、`统计池资格`、`证据成熟度`、`样本单位 / 分母链`、`原生维度树类型`。

### 4.2.1 综述类型大类

该维度回答“论文自身是什么类型”。它不等于论文质量，也不直接决定是否入池；最终是否进入 SUMMARY 主干完整表仍由 `统计池资格` 判定。

| 枚举 | 定义 | 判定标准 | 可进入主干完整表的条件 | 不得误用为 |
|---|---|---|---|---|
| 🟩 SLR | 系统文献综述，或以 SLR 为主并兼有映射 / 主题综合的混合综述。 | 原文明确报告系统检索、纳排、质量评价或数据抽取，并以回答证据综合型 RQ 为目标。 | 还必须满足 `🟢 入池`：有可复核样本单位、分母链、字段抽取或统计结果。 | 不能把只写了“review / survey”但无系统流程的叙事综述写成 SLR。 |
| 🟦 SMS | 系统映射研究，重点是研究版图、分类、覆盖度和缺口。 | 原文强调 mapping、classification、keywording、研究类型/主题分布，而非深度效果综合。 | 若有系统语料构造和可统计字段，可作为类 SLR 主统计池候选。 | 不能把方案论文中“计划做 mapping”的方法设想写成已执行 SMS。 |
| 🟪 三级 | 三级研究、综述之综述或 review of reviews。 | 样本单位是 SLR/SMS/survey 等二次研究，而非普通原始研究。 | 若有系统检索和对综述样本的编码 / 统计，可入主干表，但必须标明分母是“综述”。 | 不能把三级研究的统计外推为原始研究层面的频次。 |
| 🟨 MLR | 多声部文献综述，综合白色文献和灰色文献。 | 原文明确 white / grey literature 双轨来源、检索、质量或可信度控制。 | 若白色/灰色文献样本、分母和编码过程可复核，可作为类 SLR 候选。 | 不能混淆 peer-reviewed evidence 与 grey evidence 的证据强度。 |
| 🧰 指南 | 方法指南、报告规范、checklist 或方法论文。 | 原文主要给出如何做 SLR/SMS 的流程、表单、质量标准或报告规范。 | 默认不进主干完整表；若文中另有独立完成的系统样本统计，必须拆分说明。 | 不能把规范性建议当作经验统计 finding。 |
| 🧭 路线图 | vision、roadmap、agenda、challenge map 或开放问题图谱。 | 原文主要提出愿景、挑战、研究议程或 action items，缺少系统检索分母。 | 默认不进主干完整表；只作边界样本或 finding heuristic。 | 不能把作者观点、路线图行动项写成系统综述证据。 |
| 🧪 方案 | solution proposal、framework proposal 或未完成实证评估的方法设想。 | 原文主要提出流程、工具或框架设计，尚未完成系统检索、纳排和证据综合。 | 默认不进主干完整表；只作方法 / 流程种子或边界样本。 | 不能把“可以如何做”写成“已经系统验证”。 |

### 4.2.2 本文角色

该维度回答“这篇论文在 Paper2 中怎么用”。它是本库用途分类，不是原文自称类型。

| 枚举 | 定义 | 判定标准 | 在 SUMMARY 中的位置 | 需要写清的边界 |
|---|---|---|---|---|
| 🟢 主样本 | Paper2 SLR 主目标的核心样本。 | 通常为 SLR，且具备系统流程、字段抽取、统计观察和 finding 形成路径。 | 若统计池资格为 `🟢 入池`，进入主干完整表。 | 只贡献方法模式，不把领域结论外推到 Paper2 目标领域。 |
| 🔵 类SLR | SMS、MLR、tertiary 等类 SLR 证据综合样本。 | 非纯 SLR，但有系统语料、编码字段、统计分母或证据综合。 | 若统计池资格为 `🟢 入池`，进入主干完整表。 | 必须注明样本单位和分母差异。 |
| 🟣 方法 | 方法学参考。 | guideline / 方法论文 / 报告规范，主要定义流程、质量评价、报告结构或审计纪律。 | 不进入主干完整表；进入非入池简表和方法学参考池说明。 | 可支撑方法设计，不能支撑普通领域统计。 |
| 🟠 种子 | 维度树、字段、证据链或 finding heuristic 的启发来源。 | 有可迁移结构，但缺少系统样本库或不能进入普通统计池。 | 不进入主干完整表；进入非入池简表或 schema seed / boundary pool。 | 必须说明是启发，不是 final finding。 |
| ⚫ 边界 | 用于说明哪些文献类型不能混入统计池。 | roadmap / vision / proposal 等高价值但非系统证据综合的论文。 | 不进入主干完整表；进入非入池简表。 | 必须写清阻断入池的原因。 |
| ⚪ 候选 | 只完成题摘或元数据核验的线索。 | PDF / 全文 / 关键元数据尚未核验，或相关性未裁决。 | 不进入主干完整表；进入候选池或 manual-download。 | 不得采纳为已核验 pattern。 |

### 4.2.3 统计池资格

该维度决定论文是否进入 SUMMARY 主干完整表。它是主表治理的最高优先级枚举。

| 枚举 | 定义 | 判定标准 | SUMMARY 处理 | 升级 / 降级规则 |
|---|---|---|---|---|
| 🟢 入池 | 后续可作为主统计池候选的条目。 | 有系统检索或等价语料构造、纳排、编码 / 抽取、可统计字段或统计结果；本地至少全文文本级。 | 唯一允许进入 SUMMARY 主干完整表的资格。 | A2a 完成页码、表图、附录或复制包精核后，才可从候选统计升级为正式统计证据。 |
| 🟡 待核 | 理论上可能入池，但当前证据不足。 | 题摘或全文显示可能有系统流程，但 PDF、表图、附录、复制包、分母链或字段表未核验。 | 不进入主干完整表；进入后部待核 / 候选简表。 | 补齐全文和证据链后可升为 `🟢 入池`；若证实无系统样本库则降为 `⚪ 不入`。 |
| ⚪ 不入 | 不进入主统计池，但可能仍有方法或启发价值。 | guideline、roadmap、vision、proposal，或无系统样本库 / 无可统计分母。 | 不进入主干完整表；进入非入池简表。 | 若发现原文另有独立系统样本统计，必须拆分证据后重新裁决。 |
| 🔴 排除 | 当前文库不再采纳。 | 类型误收、事实不可核验、重复条目、与本目录目标无关，或来源不合规。 | 不进入主干完整表；只留失败 / 排除记录。 | 只能在新增证据推翻排除理由后重新候选。 |

### 4.2.4 证据成熟度

该维度回答“当前证据链能支撑多强的写作”。它不决定是否入池，但限制该条目能在论文中被怎样使用。

| 枚举 | 定义 | 判定标准 | 允许用途 | 禁止用途 |
|---|---|---|---|---|
| 🟢 精核 | PDF、关键表图、页码、附录或复制包已核验。 | 已完成文本 + 版面 / 表图 / supplementary 或 artifact 核验，并回链 `evidence_chain.md`。 | 可支撑较高强度依据和精确数字，但仍需写清范围。 | 不能省略分母、页码或证据限制。 |
| 🟡 全文 | 已读全文文本，但表图页码仍待 A2a 精核。 | `paper_content.txt` 覆盖摘要、方法、结果、讨论、结论等关键部分。 | 可作为 A1 模式种子和主统计池候选判断。 | 不得写成最终定量统计或最终 finding。 |
| 🟠 题摘 | 只读题名、摘要、元数据。 | 尚未获取或阅读全文。 | 只能保留候选相关性和下载 / 检索线索。 | 不得采纳任何维度树、统计或 finding。 |
| ⚪ 待取 | PDF 或正文尚未获取。 | 只有 BibTeX、DOI、题录或待下载路径。 | 进入 manual-download / 候选池。 | 不得假装已读全文。 |
| 🔴 异常 | 来源、PDF 或文本提取有问题。 | PDF 是登录页 / HTML、文本乱码、关键元数据冲突或来源不可核验。 | 先修复来源和提取问题。 | 不得继续写模式结论。 |

### 4.2.5 样本单位类型

该维度回答“原文实际描述和编码的对象是什么”。它是判断统计池资格和分母含义的关键。

| 枚举 | 定义 | 判定标准 | 主表写法 | 统计注意事项 |
|---|---|---|---|---|
| 📄 原研 | 原始研究、primary studies 或研究论文。 | 每个样本是一篇原始研究 / 研究提案 / 研究论文。 | `📄 原研 / N`，必要时补工具或平台分母。 | 不同研究类型、peer-reviewed / arXiv / grey literature 需分层。 |
| 📚 综述 | 二次研究、SLR/SMS/survey 样本。 | 每个样本是一篇综述或系统映射。 | `📚 综述 / N`。 | 不得把综述样本统计外推为原始研究统计。 |
| 🧩 工件 | artifact、dataset、tool、replication package 或链接对象。 | 样本或核心字段围绕研究制品、数据集、工具、仓库、链接状态。 | `🧩 工件 / N` 或说明依附论文分母。 | 需区分 paper-level 与 artifact-level 分母。 |
| 🧰 指南项 | guideline item、checklist item、流程步骤。 | 原文是方法指南或规范，编码对象是条目而非经验样本。 | `🧰 指南项 / 无主分母`。 | 默认不进入普通统计池。 |
| 🧭 行动项 | roadmap action、open question、challenge item。 | 原文组织为挑战、开放问题、行动项或愿景组件。 | `🧭 行动项 / 无系统分母`。 | 只能作启发或边界，不能当 empirical denominator。 |
| ❌ 无分母 | 无系统样本库或无法形成可统计分母。 | 原文没有检索、纳排、样本单位或可统计对象。 | `❌ 无分母`。 | 自动阻断主干完整表资格，除非后续发现独立系统样本部分。 |

### 4.2.6 原生维度树类型

该维度回答“原文如何描述自己的样本集合或证据对象”。它是本库对 Paper2 最重要的 schema 资产。

| 枚举 | 定义 | 判定标准 | 对 Paper2 的用途 | 容易误判点 |
|---|---|---|---|---|
| 🌳 RQ树 | 以 RQ / 子 RQ 为主干组织字段。 | 每个 RQ 对应一组抽取字段、结果表或 finding 段。 | 适合设计 researcher-defined meta-model 的问题层。 | 多个 RQ 若对应不同样本单位，应改写为森林。 |
| 🌲 森林 | 多个 RQ、多个样本单位或多个不共享根对象的编码结构。 | 原文同时有多个字段树、质量表、检索漏斗、评价树等。 | 支撑复杂 SLR/SMS 的多视角 schema。 | 不要为追求简洁强行压成单树。 |
| 🕸️ 关系树 | 重点是对象间关系。 | 字段包括 tool-task-metric、problem-solution、challenge-practice 等边。 | 支撑交叉统计、缺失关系和候选 finding。 | 不能把关系边压成普通枚举列。 |
| 🧱 资产树 | 以制品、数据集、复制包、链接状态等证据资产组织。 | 关注 artifact availability、repository、DOI、dead link、by request 等。 | 支撑 Paper2 的可审计证据链和复现资产设计。 | 需区分制品层和论文层分母。 |
| 🔁 流程树 | 以检索、筛选、编码、报告、质量控制等流程组织。 | 原文主要贡献是方法流程、阶段、输入输出或 researcher gate。 | 支撑 agent-human 协同流程图和 stage contract。 | 流程树不等于已完成系统综述证据。 |
| 🧰 指南树 | 以指南项、checklist、报告规范组织。 | 节点来自 protocol、search、selection、QA、extraction、synthesis、reporting 等规范项。 | 支撑方法学规则库和审计 checklist。 | 不得把指南建议当成领域统计。 |
| 🧭 路线图树 | 以挑战、行动项、开放问题组织。 | 节点来自 roadmap action、vision component、challenge、open question。 | 只作边界和研究发现启发。 | 不得把愿景主张写成经验 finding。 |
| 🧪 理论树 | 以理论概念、构念、评价框架组织。 | 节点来自 theory、concept、construct、taxonomy 或 evaluation framework。 | 支撑 researcher-defined meta-model 的概念层。 | 如果样本来自 convenience evaluation，统计池资格仍需降级。 |

## 5. 单篇目录规则

单篇目录最低结构：

```text
papers/<slug>/
├── bibtex.bib
├── metadata.json          # 机器可读事实、证据角色、统计池资格与年份/CCF口径
├── review.md              # 当前可读、可消费的单篇综述复原结果
├── evidence_chain.md      # 正式 A.1--A.4 证据链与结论-证据映射
├── paper.pdf              # 全文可得时必须有
└── paper_content.txt      # 全文可得时必须由 tools/pdf_extractor.py 生成
```

全文可得时，必须使用仓库工具生成文本：

```bash
source venv/bin/activate
python -m tools.pdf_extractor -i papers/<slug>/paper.pdf -o papers/<slug>/paper_content.txt -m text
```

若文字模式提取异常，再记录 OCR 或人工核验需求。不可获取 PDF 不得假装已读全文，必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。若一轮新增条目全部成功获取 PDF，也必须在 [search/search-log.md](./search/search-log.md) 中记录“无新增人工下载”。

`metadata.json` 是 A1 之后的机器可读事实入口，必须至少包含：`slug`、`title`、`authors`、`year`、`publication_year_basis`、`online_first_date`、`publication_type`、`venue_short_link`、`ccf_official_category`、`ccf_official_rank`、`ccf_verification_status`、`review_type`、`se_subfield`、`current_fulltext_status`、`eligible_for_schema_seed`、`eligible_for_statistical_synthesis`、`evidence_role`、`systematic_evidence_status`、`statistical_pool_exclusion_reason`。若字段不适用，必须显式写 `null`、`--` 或 `待核验`，不能缺键。

### 5.1 `review.md` / `evidence_chain.md` / `audits/` 职责分离

A1-DT v2 之后，单篇目录必须把“当前可消费正文”“正式证据链”和“批次过程证据”分开维护：

| 文件或目录 | 职责 | 必须包含 | 不得包含 |
|---|---|---|---|
| `review.md` | 当前可读、可消费的单篇综述复原结果 | 快速结论、全文详读、原生维度树 / 维度森林、叶子维度表、关系边表、统计观察、候选 finding、对 Paper2 的启发与风险、指向 `evidence_chain.md` 的短链接 | 大段历史审计草案、旧版返修来源、禁止消费的旧 A.2/A.3、技能使用流水账 |
| `evidence_chain.md` | 该单篇论文的正式证据链文件 | `## 审计附录：证据链与结论-证据映射`、A.1 论文与本地文件来源、A.2 维度树证据账本、A.3 结论-证据映射、A.4 本地复验命令与人工核验清单 | 已被正式 A.2/A.3 吸收的历史草稿、无当前证据价值的旧强度说明 |
| `audits/a1dt-v2-19x3/` | 批次级过程证据 | prompts、results、logs、adjudications、结构门禁、测试 | 面向读者的当前正文事实口径 |

执行纪律：

1. 19 篇单篇目录必须同时具备 `review.md` 与 `evidence_chain.md`，并且二者互相用相对路径链接。
2. `review.md` 末尾只保留短小 `## 证据链入口`，链接到 `[evidence_chain.md](./evidence_chain.md)`，不得继续内嵌 A.1--A.4 宽表。
3. 当前仍有证据链价值的 A.1--A.4、待 A2a 风险、claim map、复验清单统一放入 `evidence_chain.md`。
4. 历史 A.2/A.3 草案若有尚未吸收的独特证据，必须先转写进正式 A.2/A.3；若已被正式证据链或 v2 adjudication 吸收，应直接移除。
5. `历史审计草案归档`、`历史草稿旧强度`、`禁止消费为事实真源`、大段 `v1-deprecated` 警示和技能使用流水账不得出现在正式 `review.md` 正文。
6. `review.md` 不得保留本机技能路径、技能读取清单或返修过程流水账，例如 `技能文件`、`/.codex/skills`、`reviewer-self-review`、`autoresearch/SKILL.md`、`codex 插件缓存`、`部分-blocked`、`返修块` 这类过程痕迹；若这些内容有复现价值，应只保留在 `audits/` 批次日志中。
7. `not_verified`、`待 A2a`、`schema_seed`、`boundary_anchor`、`候选` 是当前证据状态，不是历史噪声，应按证据等级保留。
7. 清理正文时不得删除 `audits/a1dt-v2-19x3/` 的 prompts / results / logs / adjudications；这些属于批次复现证据。

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

issue #95 的 10 篇现代锚点必须遵守“一篇一审计进程 / CLI agent”原则：每个审计进程只能读自己负责的 `bibtex.bib`、`metadata.json`、`paper_content.txt` 和必要 PDF，不得混读多篇，也不得开启 sub-subagent。`review.md` 必须显式写明是否已读全文、是否回 PDF 核对图表、是否只做 metadata-only。

新增锚点的 `review.md` 最低结构：快速结论卡片、论文内容详读、六类 pattern、A1-M0--M6 元维度贡献、可迁移字段树 / 维度锚点、对 Paper2 的启发与风险、待复核。快速卡片必须明确“是否已读全文”“是否回 PDF 核对图表”“是否只做 metadata-only”，避免把粗筛结论误写成全文审查结论。



## 6.3 A1-DT v2 维度树 / 维度森林抽取纪律

本节是 PR #135 A1-DT v2 之后长期维护 `review.md`、`audits/` 与 `patterns/` 的强制规则。A1-DT v2 的核心口径是：**统一抽取纪律 + 每篇论文原生样本编码维度树 / 维度森林 + 跨论文投影层**。

> [!WARNING] v1-deprecated: 旧批次 [audits/a1dt-19x3/](./audits/a1dt-19x3/) 只作为历史归档和返修来源保留。A1-DT v2 的新审计、新结果、新结构门禁和新返修产物必须写入 `audits/a1dt-v2-19x3/`。不得把 v1 审计目录继续当作当前事实口径。

### 6.3.1 v2 定义与三层分离

A1-DT v2 把“维度树”定义为单篇论文中从 RQ、贡献声明、抽取表、编码方案、taxonomy、roadmap action、guideline item 或证据呈现结构推导出的**原生样本编码结构**。若一篇论文有多个 RQ、多个样本单位或多个不共享根对象的编码结构，应写成“维度森林”，而不是强行压成单棵树。

三层必须分离：

| 层级 | 事实源 | 允许产物 | 禁止行为 |
|---|---|---|---|
| 统一抽取纪律层 | 本 [GUIDE.md](./GUIDE.md) §6.3 与 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 的字段合同 | 节点字段、证据链、降级规则、结构门禁 | 为某篇论文临时改写全局纪律且不回修 GUIDE / pattern schema。 |
| 单篇原生样本编码层 | `papers/<slug>/paper_content.txt`、`paper.pdf`、附录、supplementary、replication package、`review.md` 文末 A.1--A.4 | 单篇维度树 / 维度森林、叶子取值空间、关系边、降级说明、结论-证据映射 | 用跨论文 pattern 反向套模板；只写六个通用 leaf；把 reviewer 主观分类写成原文 schema。 |
| 跨论文投影层 | 已完成单篇 A.3 回链的可迁移结论 | `patterns/` 中的归纳字段、SUMMARY 归纳、候选 pattern library | 把 `patterns/` 当作单篇原生树模板；绕过单篇 A.2/A.3 直接形成统计结论。 |

`patterns/` 永远是**结果侧跨论文投影 / 归纳层**。它只能在单篇原生树完成后帮助对齐命名、发现可迁移 pattern 和记录 schema 缺口，不能反向决定某篇论文“应该有什么树”。

### 6.3.2 唯一事实源、旧节迁移与多 RQ 规则

1. 每篇 `papers/<slug>/review.md` 必须包含 `## 维度树复原` 小节，并以该小节作为单篇维度树 / 维度森林事实真源。
2. 旧有 `可迁移字段树`、`字段树草案`、`字段树`、`可迁移 roadmap`、`schema 缺口` 等章节必须升级、合并或标注“已迁移至维度树复原”，不得与新小节长期并列为第二事实源。
3. 若旧节与新判断冲突，以原文证据和本 GUIDE 为准，同时在审计附录中记录降级或替代原因。
4. 多 RQ 论文必须先判定 RQ 与样本单位的关系：
   - 多个 RQ 共享同一 primary study / artifact / paper 样本单位和同一编码表时，可写成一棵主树下的多个 RQ 分支。
   - 多个 RQ 对应不同样本单位、不同 evidence object 或不同编码表时，必须写成维度森林，并分别说明每棵树的统计池资格。
   - RQ 与结果章节不一一对应时，必须用关系边表记录 `RQ -> extraction field -> result / finding` 的映射或缺失映射。
5. 节点、叶子、关系边和结论必须有稳定标识：`[dim-{slug}-*]`、`[leaf-{slug}-*]`、`[edge-{slug}-*]`、`[clm-{slug}-*]`；这些标识必须能从叶子表、关系边表、证据账本和结论映射互相回链。

### 6.3.3 从原文推导原生树的优先级

1. 根节点优先来自显式 RQ、总目标、scope、unit of analysis；无 RQ 时按 §6.3.4 的样本单位降级矩阵处理。
2. 主干分支优先来自 extraction form、classification schema、coding scheme、taxonomy、roadmap figure、guideline checklist、CPTM model、质量评价表或报告结构，而不是 reviewer 主观造词。
3. 叶子维度必须对应可抽取字段、稳定分类项、guideline item、roadmap action / vision item 或可复验的缺失事实；仅凭 reviewer 感觉概括的词只能写作候选节点。
4. RQ / 贡献声明 / guideline item / roadmap action 与字段必须显式连接：每个主干分支至少说明服务哪个 RQ、子 RQ、贡献声明、行动项或候选发现方向。
5. 统计用途必须说明分母、样本单位、统计池资格和缺失值处理；无系统样本库、无分母或证据不足时必须写“不进入主统计池”。
6. 候选发现用途必须与最终 research finding 分开；roadmap / proposal / vision / guideline 的建议默认只能作为候选启发、边界锚点或风险提示。

### 6.3.4 样本单位降级矩阵

单篇维度树必须先说明“样本单位”。若原文没有系统样本库，不得假装存在 primary-study 统计池，应按下表降级：

| 原文类型 / 证据形态 | 优先根对象 | 样本单位写法 | 可进入主统计池 | 允许用途 | 必填降级声明 |
|---|---|---|---|---|---|
| SLR / SMS / MLR 且有系统检索、纳排、数据抽取 | RQ / review objective / unit of analysis | primary study / paper / artifact / tool / dataset 等原文定义单位 | 可按证据强度局部进入 | `schema_seed`、`statistical_synthesis` 候选、`candidate_finding` | 写明分母、纳排、缺失值语义和待核验字段。 |
| tertiary study 且有综述样本库 | RQ / included review corpus | included SLR/SMS/survey | 可按证据强度局部进入 | `schema_seed`、`statistical_synthesis` 候选 | 不得把综述样本统计外推为 primary-study 统计。 |
| roadmap / vision / agenda 且无系统样本库 | roadmap action / vision item / challenge item | action item / vision item / challenge item | 否 | `boundary_anchor`、`candidate_finding`、`risk_only` | 明确“无系统样本库；按 roadmap action / vision item 降级”。 |
| solution proposal / framework proposal 且无系统样本库 | contribution / framework component / claim | component / design claim / illustrative example | 否 | `schema_seed`、`boundary_anchor`、`risk_only` | 明确“非系统综述；不可进入统计合成”。 |
| guideline / checklist / reporting standard 且无系统样本库 | guideline item / checklist item / process step | guideline item / checklist item / step | 否 | `methodological_seed`、`schema_seed`、`risk_only` | 明确“按 guideline item 降级；不得当作领域统计 finding”。 |
| guideline 且含系统证据综述 | guideline item + evidence base | guideline item；证据综述另列样本单位 | 仅证据综述部分可候选 | `methodological_seed`、局部 `schema_seed` | 分开写 guideline 建议与 evidence base 统计，不得混合。 |
| commentary / opinion / tutorial | 主张 / 教学模块 / 经验条目 | claim / module / example | 否 | `risk_only`、`boundary_anchor` | 明确作者观点属性和不可外推范围。 |

roadmap + 无系统样本库时，优先按 `roadmap action` / `vision item` 降级；guideline + 无系统样本库时，优先按 `guideline item` 降级。降级后的树仍要有节点、叶子、证据与结论映射，但默认不具备主统计池资格。

### 6.3.5 叶子维度必填字段与取值空间 rubric

每个叶子维度至少包含：节点或叶子标识、名称、父节点、定义、取值空间、证据要求、缺失值语义、样本单位、统计用途、候选发现用途、迁移边界和结论引用。

| 取值空间类型 | 使用条件 | 写法要求 | 统计 / 降级纪律 |
|---|---|---|---|
| 完整枚举 | 原文给出封闭类别集合 | 写出所有类别或指向原文表 / 图；缺失值单列说明。 | 可候选进入统计；图表未核验时标 `not_verified`。 |
| 层级枚举 | 原文给出 taxonomy / 分类树 | 保留父子层级，不压成逗号清单。 | 父子层级不清时只做 `schema_seed`。 |
| 布尔 | 是否存在某制品、字段或特征 | 明确 `true` / `false` / `未报告（not reported）` 的判定证据。 | `false` 必须区分原文否定与未报告。 |
| 数值或区间 | 计数、年份、比例、评分 | 写分母、范围和单位。 | 无分母、图表待核验或抽取不完整时不得进入强统计结论。 |
| 关系值 | 字段表示节点间关系 | 使用关系边表，保留关系类型、目标取值空间和缺失关系。 | 缺失关系可作为 absence evidence，但必须回链证据。 |
| 外部分类法引用 | 原文使用 SWEBOK、CCS、ISO 等外部体系 | 写清外部体系版本或待核验状态。 | 版本不明时只能候选，不得与其他论文直接合并统计。 |
| 自由文本加理由 | 原文本身是开放问题、愿景或叙述性结果 | 说明为什么不能枚举，并默认降级为候选启发。 | roadmap / vision / guideline 无样本库时不得进入主统计池。 |
| 待核验或待补全 | 图表 / 附录 / supplementary 尚未核对 | 标为 `not_verified`。 | 不得进入主统计池或 SUMMARY 定量统计。 |

### 6.3.6 关系型维度：主干树加关系边表

DevSecOps CPTM、生命周期投影、工具-实践-指标链接、RQ-字段-发现链路等关系型 schema 不得强行压平成普通树。应使用主干树表达实体层级，再用关系边表表达横向关系。

关系边表至少包含：关系边标识、源节点、关系类型、目标节点、目标取值空间、缺失值语义、证据引用和结论引用。`no linked metric`、`未报告（not reported）`、`no linked tool`、`no mapped RQ` 等缺失关系也要入账，可在 A.2 中使用 `absence_evidence` 或 `未报告（not reported）` 证据角色。

### 6.3.7 审计附录与最小必填字段简表

每篇 `evidence_chain.md` 必须包含以下固定结构。正式 A.1--A.4 表头必须继续使用纯中文，不得出现 `ID`、`PDF`、snake_case 或中英文对照表头。

执行 agent 可先按下面的“最小必填字段简表”自检；写入 `evidence_chain.md` 时仍必须使用后续正式中文宽表。

| 附录 | 最小必填字段 | 最小合格条件 |
|---|---|---|
| A.1 论文与本地文件来源 | 来源标识、文件或链接、类型、用途、可核验性 | A.2 每条证据的来源标识都能回链到 A.1。 |
| A.2 维度树证据账本 | 证据标识、引用键、来源标识、原文章节或行号范围、原文短引、释义支撑、证据角色、证据强度、支撑的维度节点、需要原文版面核验 | 每个核心节点 / 叶子 / 降级判断至少有一条证据；待核验证据必须写 `not_verified`。 |
| A.3 结论-证据映射 | 引用键、结论标识、结论内容、结论类型、支撑对象标识、支撑证据标识列表、结论强度、允许用于论文的位置 | 正文核心判断和树级判断都有 `[clm-*]`；证据列表能回链 A.2。 |
| A.4 本地复验命令与人工核验清单 | 检查标识、复验对象、命令或人工核验动作、通过条件、当前状态 | A.2 中“需要原文版面核验”为 `true` 的证据都进入 A.4。 |

```markdown
## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
```

执行纪律：

1. 正文核心判断、维度树一句话结论、树类型、样本单位、统计池资格、可迁移 / 不可迁移判断、roadmap / guideline 降级判断均必须有 `[clm-*]` 引用键。
2. A.3 的“支撑证据标识列表”必须回链 A.2；A.2 的“来源标识”必须回链 A.1。
3. `weak` / `not_verified` 证据不得进入主统计池、SUMMARY 定量归纳或 final research finding。
4. A.2 中“需要原文版面核验”为 `true` 的证据，必须在 A.4 的“复验对象”中列出。
5. 旧结论或旧证据被替代时不得删除键，应标记“已废弃”和“替代证据 / 替代结论”。

### 6.3.8 A1-DT v2 证据强度降级与统计用途冻结

A1-DT v2 的目标是先冻结单篇原生维度树 / 维度森林与跨论文投影边界，不要求完成所有 原文页码、表号、图号和 supplementary 的精确核验。因此：

1. A.2 中凡仍写有“待 A2a 精确页码复核”“邻近段落”“表 / 图待核验”“见释义”等泛定位或待核验描述的证据，证据强度必须写 `not_verified`，不得写 `strong` 或 `medium`。
2. A.3 中凡依赖上述 `not_verified` 证据的结论，只能作为 `schema_seed`、`boundary_anchor`、`candidate_finding`、`methodological_seed`、`risk_only` 或 `do_not_use`；不得写 `statistical_synthesis`。
3. SUMMARY 可以记录“后续主统计池候选”，但这不是当前 A1-DT v2 维度树证据已可统计；A2a 完成精确页码 / 表图 / 字段锚定前，不得把 A1-DT v2 的叶子结论用于 SUMMARY 定量统计或 final research finding。
4. 后续若某篇论文完成 PDF / 表图 / supplementary 精核，可在 A.2 新增替代证据并把旧证据标为“已废弃”，再把 A.3 结论从 `schema_seed` 升级为 `statistical_synthesis`；升级必须同步更新 SUMMARY 结论-证据映射和 schema 修订 / 回填日志。

### 6.3.9 v1→v2 过渡规则

1. `audits/a1dt-19x3/` 统一标注为 v1 历史归档；引用该目录时必须使用如下警示格式：

```markdown
> [!WARNING] v1-deprecated: 这里是 A1-DT v1 历史审计归档，只能作为返修来源和历史证据，不是当前 A1-DT v2 事实口径。v2 新产物写入 `audits/a1dt-v2-19x3/`。
```

2. v1 中“原文 schema 主树 + 通用接口投影”的结论必须重新按 v2 三层分离复核：单篇原生树 / 维度森林先成立，才能进入跨论文投影。
3. v1 审计建议只能作为 reviewer input；若与原文、A.2 证据或本 GUIDE 冲突，以原文和本 GUIDE 为准，并在 A.3 记录替代 / 废弃结论。
4. 不得把 v1 的 `schema_seed`、`not_verified`、`needs_manual_check` 状态在 v2 中自动升级。升级只能来自新增原文证据、版面核验或明确的 A2a 复验记录。

### 6.3.10 A1-DT v2 19×3 工作流

A1-DT v2 的 19×3 工作流用于把 19 篇 `review.md` 从 v1 历史返修状态推进到 v2 当前事实口径。工作流产物必须写入 `audits/a1dt-v2-19x3/`，并至少包含批次 README、任务清单、prompt、results、logs、SUMMARY、结构门禁脚本或等价复验说明。

推荐顺序：

1. 先读本 [GUIDE.md](./GUIDE.md) §6.3、[README.md](./README.md) 的 A1-DT v2 说明和 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 的投影边界。
2. 对每篇论文只读取自己的 `bibtex.bib`、`metadata.json`、`paper_content.txt`、必要 PDF / supplementary 和现有 `review.md`；不得混读其他论文来套模板。
3. 先识别原文类型与样本单位，再决定单树、森林或降级树。
4. 再抽取根节点、主干分支、叶子取值空间、关系边和缺失值语义。
5. 最后补齐 A.1--A.4，并把跨论文可迁移内容只写作候选投影，不直接写成最终 pattern。
6. 三路审计结果只作为返修输入；合并时必须保留分歧、降级和替代证据，不得做无证据的多数投票。

### 6.3.11 结构门禁

A1-DT v2 ready 前必须通过结构门禁。若 `audits/a1dt-v2-19x3/` 尚未落地脚本，至少人工检查并记录以下项目；脚本落地后应以脚本输出为准：

1. 19 篇 `review.md` 均包含 `## 维度树复原` 与 `## 证据链入口`；19 篇 `evidence_chain.md` 均包含 `## 审计附录：证据链与结论-证据映射` 与 A.1--A.4。
2. 每篇至少声明树 / 森林类型、样本单位、统计池资格、迁移边界和降级状态。
3. roadmap / vision + 无系统样本库均按 roadmap action / vision item 降级；guideline + 无系统样本库均按 guideline item 降级。
4. `evidence_chain.md` 中 A.1--A.4 表头保持正式中文宽表；A.2 / A.3 / A.4 能互相回链。
5. `patterns/` 没有被写成单篇原生树模板；跨论文归纳均能回链单篇 A.3。
6. `review.md` 不保留大段 v1 历史章节；若 `evidence_chain.md` 或 `audits/README.md` 引用 v1 审计目录，必须带 `v1-deprecated` 警示并说明其只作过程归档。
7. `weak` / `not_verified` / `needs_manual_check` 结论没有进入 SUMMARY 定量统计或 final research finding。

### 6.3.12 维度树 / 维度森林中文化纪律

维度树 / 维度森林是本库最关键的学术资产，必须优先保证人类导师、后续硕士生和后续写作 agent 能直接读懂。因此所有 `review.md` 的 `## 维度树复原` 小节默认采用中文写作，尤其是树干、节点名、叶子名、关系边说明、取值空间解释、统计用途和候选发现用途。

执行规则：

1. 同一篇 `review.md` 中，关键英文术语第一次出现时写成 `中文（English）`；后续正文原则上只写中文。
2. 维度树 / 维度森林的可读标签必须中文化，例如写“样本单位”“发表源”“实证策略”“质量量规”“关系边”，不要只写 `sample_unit`、`venue`、`empirical_strategy`、`quality_rubric`、`edge`。
3. 稳定机器标识必须保留原样，包括 `tree-*`、`leaf-*`、`edge-*`、`clm-*`、`ev-*`、BibTeX 键、JSON 字段、文件名、路径、链接目标和命令。若这些标识需要解释，只在旁边增加中文释义，不得改写标识本身。
4. 原文封闭枚举、论文原题、工具名、模型名、标准名、作者自定义分类名和原文短引可保留英文；若它们承担节点或叶子标签，应在首次出现处补中文释义。
5. 审计附录 A.1--A.4 的正式表头继续使用中文；原文短引、证据标识、结论标识和来源文件名不强行翻译。
6. 后续任何批量中文化只允许在 `## 维度树复原` 小节内做保守编辑；不得机械替换全库路径、链接、`metadata.json`、`paper_content.txt` 或机器字段。
7. **维度树 / 维度森林代码块是优先中文化对象**：树根、分支、节点、叶子、关系边、取值空间类型、缺失值语义和注释说明默认使用中文；英文缩写、原文枚举或工具名可以保留，但必须在同一行或相邻行给出中文解释。
8. 树内若确需保留机器可读短标识，可采用 `中文标签（stable_id: xxx）`、`中文标签 / 原文枚举：...` 或 `中文标签：...` 的写法；不得只留下 `field_name ::= enum<...>` 这类纯英文 schema。
9. 中文化不得改变学术判断、统计池资格、证据强度、分母、页码、表号或结论-证据映射；若发现原文理解问题，必须另起返修记录，而不是借语言清理暗改事实。

最低验收：抽样打开至少 3 篇 `review.md`，只读维度树 / 维度森林代码块和其前后说明时，应能判断该论文“如何描述其样本集合、有哪些维度、哪些维度可统计、哪些只是候选启发”。若还需要先读英文变量名才能理解，则中文化未通过。

机械拒收标准：若单个维度树代码块超过 20 行，且主要节点 / 叶子中仍有超过约 30% 的未解释英文变量名，或出现 `field_name ::= enum<...>` 这类纯英文 schema 写法，则不得判定 ready；必须补同一行中文标签或相邻行中文释义。英文枚举、工具名、模型名可以保留，但所属维度、关系含义和缺失值语义必须中文可读。


## 6.4 survey_of_surveys 自身 schema 抽取规则

本节定义本目录“如果自己也是一篇综述”时使用的二级汇总 schema。它回答的不是某篇论文的领域结论，而是：该论文能为 Paper2 的 researcher-defined meta-model、维度树、证据链、统计分析和 research finding 机制提供什么模式先验。

S1--S8 与 A1-M0--M6 的关系如下：A1-M0--M6 描述 Paper2 方法链的跨论文投影；S1--S8 描述 `survey_of_surveys/` 作为一篇脚手架综述时，对每篇样本论文做二级编码的统一 schema。S1--S8 不替代单篇原生维度树，也不得被当作目标领域最终发现。

| 维度 | 操作化问题 | 强 | 中 | 弱 | 不适用 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 原文是否清楚说明综述 / 映射 / 路线图的对象、RQ、scope、review type 与样本单位？ | 有明确 RQ / 目标 / scope / review type，且能回链原文证据。 | 有明确目标或 scope，但 RQ、样本单位或 review type 需要本地降级解释。 | 仅有愿景、议程或问题陈述，可作边界启发。 | 原文类型完全不支持综述任务设定抽取。 |
| S2 语料收集与筛选 | 原文是否定义数据库、检索式、时间窗、纳排、去重、质量评价与分母链？ | 有系统检索或等价语料构造，且给出可复核分母链。 | 有部分语料来源或筛选说明，但分母、质量评价或裁决机制不完整。 | 只有叙事性来源、参考文献线索或经验来源。 | 原文没有语料收集 / 筛选过程。 |
| S3 原生维度树 / 样本编码对象 | 原文如何描述其样本集合：样本单位、编码对象、分类树、抽取表、路线图 action 或 guideline item？ | 有明确样本单位和可复原的维度树 / 维度森林。 | 可复原树 / 森林，但需按 roadmap、guideline 或 proposal 降级。 | 只有概念结构或叙事分组，可作边界启发。 | 无可审计编码对象。 |
| S4 字段级证据 | 原文是否提供字段、抽取表、编码方案、证据锚点、样本 ID 或制品链接来支撑逐字段结论？ | 字段级证据充分，能回链表格、字段或样本 ID。 | 有字段或分类，但页码、表图、supplementary 或样本 ID 仍需 A2a 精核。 | 只有概念字段或启发式，没有稳定样本级证据。 | 原文无字段级证据。 |
| S5 维度模式演化 | 原文是否说明维度、分类、代码本、模式或路线图如何从先验、开放编码、讨论或迭代中形成？ | 有明确编码 / 分类 / guideline update / open coding / thematic analysis 演化过程。 | 能推断维度演化，但缺少版本、冲突或完整修订记录。 | 只有路线图、愿景或概念链条，可作启发。 | 无维度形成过程。 |
| S6 统计分析 | 原文是否把字段级数据转化为频次、比例、趋势、交叉表、模型或系统观察？ | 有明确分母与统计结果，可支撑后续统计池候选。 | 有局部统计或方法示例，但主统计池资格有限。 | 只有枚举、叙事总结或非系统数量提示。 | 无统计分析。 |
| S7 候选 finding | 原文是否从统计观察、编码结果、讨论或路线图中形成可审计的候选发现、gap、challenge 或 recommendation？ | finding 与字段 / 统计 / 证据链关系清楚。 | 有可迁移 finding 模式，但领域结论需降级或仍缺反证映射。 | 只有愿景、roadmap、proposal 或方法启发。 | 无候选 finding。 |
| S8 研究者 / 作者质疑与裁决 | 原文是否呈现人类研究者如何处理分歧、复查、质量控制、threats、人工覆盖、override 或质疑？ | 有明确多研究者筛选 / 编码 / 质量评价 / 分歧裁决或一致性报告。 | 有复核、会议、threats、pilot、QA 或等价质量控制，但无完整裁决日志。 | 只有限制讨论或一般提醒。 | 无研究者裁决或质量控制信息。 |

执行纪律：

1. 每篇 `papers/<slug>/review.md` 必须包含 `## survey_of_surveys 自身 schema 抽取`，并至少包含两张表：第一张表给出 S1--S8 的判定等级、一句话抽取结果和证据位置；第二张 `### S1--S8 四分栏证据拆分` 表必须使用 `维度 / 原文证据 / 维度树复原 / 统计池资格 / A2a 待核验` 五列，逐行拆清原文事实、本文本地维度树解释、是否影响主统计池候选、以及页码 / 表图 / supplementary / Zenodo / publisher final 等待核验项。
2. **每篇论文的 S1--S8 抽取必须由一个独立 subagent 或等价独立审计进程完成**；该进程只能处理自己负责的一篇论文，不得混读多篇、不得开启 sub-subagent。主线程负责合并、压缩和回填。
3. **独立审计必须落盘**：本批次使用 [audits/a1-s1s8-19x1/](./audits/a1-s1s8-19x1/) 作为证据入口，至少维护 `TASKS.tsv`、`results/<slug>.md` 和 `adjudications/<slug>.md`；后续新增批次可使用新的 `audits/<batch-id>/`，但必须保留同等结构。`TASKS.tsv` 记录论文、agent、状态与结果路径；`results/` 保存独立审计输出或忠实压缩归档；`adjudications/` 保存主线程采纳 / 不采纳裁决、同步修改范围和 A2a 接力项。不得只回填 `review.md` 而丢失审计结果和裁决链。
4. 若 subagent 原始报告过长或只存在于会话通知中，`results/<slug>.md` 至少要保存可复核的长摘要、关键证据、C/I/M 问题和压缩边界；后续优先保存原始报告或日志摘要，避免长期审计依赖仓库外上下文。
5. S1--S8 表格中的等级只说明该维度对本目录二级综述 schema 的可用程度，不等于论文质量评分，也不等于统计池资格；统计池资格必须在四分栏表中单独写清。
6. Roadmap、vision、solution proposal、guideline、commentary 可以在 S1、S3、S5、S7、S8 提供启发，但若 S2 / S6 不成立，必须明确“不进入主统计池”。
7. 每个 S 维度的证据位置至少应指向 `review.md` 的具体小节；若支撑结论已经进入 `evidence_chain.md`，还应指向 A.2 证据标识或 A.3 结论标识。
8. 若某项只基于题摘、泛定位或待 A2a 图表核验，等级不得写“强”；若原文文本级证据较强但最终数字、表图、supplementary 或复制包仍待精核，应写成“中”或在四分栏表中明确“文本级可用，最终统计前需 A2a 复核”，不得让“强”被误读为最终统计证据。
9. [SUMMARY.md](./SUMMARY.md) 必须维护 S1--S8 定义表与 19 篇逐篇覆盖矩阵；新增或修改任何 S 维度后，必须回填所有已入账论文，或在 schema 修订 / 回填日志中明确待回填范围和阻塞原因。
10. S1--S8 当前只服务 A1/A2a/A2b 的模式库建设和 A3 schema 设计；不得直接写成 Paper2 的最终 empirical finding。


## 7. schema 回修闭环

`patterns/pattern-field-schema.md` 是 A1 的脚手架字段合同，但不是不可改的先验。dry-run 暴露缺口时必须执行：

1. 在单篇 `review.md` 的“schema 缺口 / 不可迁移点”中记录触发原因。
2. 回修 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 的字段定义、取值空间、证据要求或缺失值语义。
3. 在 [SUMMARY.md](./SUMMARY.md) 的“schema 修订 / 回填日志”记录时间、触发条目、受影响字段、修订内容、回填状态和冻结理由。
4. 若不回修，必须说明为什么该缺口留给 A2a/A2b。

## 8. SUMMARY.md 回填规则

[SUMMARY.md](./SUMMARY.md) 是长期文库总账，不是 PR 施工记录。后续更新必须优先呈现“当前文库事实、当前规则、当前结论和后续接力入口”，把批次来源、下载失败细节和检索过程主要下沉到 [search/search-log.md](./search/search-log.md)、[search/candidate-pool.md](./search/candidate-pool.md) 或专项审计文件。

[SUMMARY.md](./SUMMARY.md) 必须至少维护：

1. 当前文库状态和总判断：明确当前收录数量、全文状态、manual-download 状态、A1 能支撑什么、不能支撑什么。
2. 核心口径：阅读状态、证据等级、schema seed、主统计池、方法学参考池、schema seed / 边界池（boundary pool）、CCF / venue 字段。
3. 统一论文总表：所有入账论文必须在一个主表中维护，不得按 PR 批次拆成多个主表；本目录显式 override 根级默认排序，主表按年份从高到低排列。
4. 证据池 / 统计池分布：至少区分主统计池、方法学参考池、schema seed / 边界池（boundary pool）、待下载 / metadata-only。
5. A1-M0--M6 元维度定义：解释每层的操作化问题、最低证据和当前主要启发。
6. A1-M0--M6 逐篇覆盖矩阵：每篇论文至少给出 7 个元维度的短语级贡献，并链接到单篇 `review.md`。
7. 当前 pattern 总结与 A2a 接力建议：说明 RQ、dimension、finding、evidence、validity、report structure 的当前观察和下一步处理方式。
8. schema 修订 / 回填日志：只记录会影响后续 A2a/A2b schema、统计池或字段回填的变更；必须包含时间、触发条目、受影响字段、修订内容、回填状态和冻结理由。
9. 当前风险与待复核：只保留影响后续工作的风险，例如图表视觉核对、CCF 官方 WAF、publisher final 差异、统计池误混风险。
10. 更新时间降序日志，时间格式为 `yyyy-mm-dd hh:mm:ss`。

主表建议字段：`状态`、`年份`、`标题`、`出版形态`、`期刊/会议/预印本`、`CCF 大类`、`CCF 等级`、`综述类型大类`、`细分类型 / 原文自称`、`本文角色`、`统计池资格`、`证据成熟度`、`样本单位 / 分母链`、`原生维度树类型`、`Paper2 关键贡献`、`详情`。`CCF 复核状态` 是事实审计字段，但不再建议放入第一张 story 速读表；应在 §2.3、后续 CCF / venue 审计表或单篇 `review.md` 快速卡片中维护。

普通 emoji 状态列只写 emoji；本目录 §4.2 明确列出的类型枚举列允许使用 `emoji + 短文本`，例如 `🟩 SLR`、`🟢 入池`、`🌲 森林`。

### 8.1 三类证据池规则

`eligible_for_statistical_synthesis` 只表示“是否进入主统计池”，不表示论文是否有学术价值。后续维护必须区分以下三类池：

| 池 | 可进入条件 | 当前用途 | 计数规则 |
|---|---|---|---|
| 主统计池 | 论文自身已经执行完成 SLR / SMS / tertiary / MLR / systematic mapping；有系统检索或等价语料构造、纳排 / 编码 / 数据抽取、可统计字段或结果；本地至少全文文本级；其中 SLR 与类 SLR 证据综合是优先样本 | A2a/A2b 统计字段频次、覆盖度、维度饱和度和研究发现支撑 | 以 `eligible_for_statistical_synthesis=true` 为准；同时记录 `综述类型大类`、`细分类型 / 原文自称` 和 `本文角色` |
| 方法学参考池 | guideline、mapping guideline、方法论文；能定义流程、抽取、报告、效度或质量评价规则，但不是普通领域统计样本 | 指导方法设计、schema 设计、证据链设计；不与普通领域统计池混算 | 只计主归属为方法学参考且 `eligible_for_statistical_synthesis=false` 的条目 |
| schema seed / 边界池（boundary pool） | roadmap、vision、solution proposal、theory roadmap、非标准系统综述但有高价值维度或 finding heuristic | 启发维度、方法边界、人机协同和 finding heuristic；不得污染统计池 | 只计主归属为边界 / 启发 seed 且 `eligible_for_statistical_synthesis=false` 的条目 |

三类池在 SUMMARY 的当前数量必须按“主归属”计数，合计应等于入账论文数，避免 Petersen 2015 这类同时有方法学价值和统计样本资格的论文被重复计数。若某论文有次级用途，应在说明文字中标注，不改变主归属计数。

当 `eligible_for_statistical_synthesis=false` 时，`metadata.json` 必须填写 `statistical_pool_exclusion_reason`；若条目仍可作 schema seed，应保留 `eligible_for_schema_seed=true` 并说明其证据角色。

### 8.2 禁止按 PR 批次维护主表

`SUMMARY.md` 的主论文表不得按“初始 dry-run”“#95 十篇”“本轮新增”等来源批次拆分。批次信息可记录在检索日志、候选池、审计文件或更新日志中；长期总账只按文库对象组织。若后续确需展示批次来源，应作为主表中的辅助字段或附录，不得替代统一主表。

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
