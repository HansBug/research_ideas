# survey_of_surveys/SUMMARY.md：综述之综述脚手架总账

## 1. 当前状态

本目录当前处于 **A1 文库奠基** 状态：已建立 README/GUIDE/SUMMARY/search/papers/patterns 结构，完成 6 篇全文文本级 dry-run 和 3 篇 metadata-only / 需人工下载失败路径记录。A1 的目标是验证脚手架能否工作，不声称完成 100+ 篇完整综述之综述文库。

| 项 | 当前值 |
|---|---:|
| 候选条目 | 9 |
| 全文文本级 dry-run | 6 |
| metadata-only / 需人工下载 | 3 |
| 完成 `review.md` | 9 |
| 完成 `paper.pdf` + `paper_content.txt` | 6 |
| schema 回修记录 | 4 类 |
| 真实 LLM / `.env` | 未运行 / 未读取 |
| 四个真实例子 | 不运行；A1 只做文库 dry-run |

**本节结论**：A1 已证明 `survey_of_surveys/` 能承载真实样本、失败路径、证据等级和 schema 回修闭环。它仍只是脚手架，不是目标领域证据池，也不是完整三级综述。

## 2. 证据等级口径

emoji 口径：🟢 = 已完成全文文本级 dry-run；🟡 = metadata-only / 需人工下载；⚪ = 排除；⏳ = 待补。正式表格中 emoji 列只写 emoji。

| 阅读状态 | 含义 | 可写边界 |
|---|---|---|
| `已读全文文本-paper_content核验` | 已读 `paper_content.txt` 的摘要、方法、结果、结论等关键部分 | 可写 A1 pattern；图表/表格数值待 PDF 核对。 |
| `全文不可得-待人工下载` | 合法 PDF 未获取或下载到 HTML / 登录页 | 只能写候选理由和下载需求。 |
| `未读原文-仅题摘粗筛` | 只读标题 / 摘要 / 元数据 | 不能采纳 pattern。 |
| `已回PDF核对图表` | 已打开 PDF 核对关键图表 / 表格 | 可支撑图表级细节。 |

**本节结论**：当前 6 篇全文样本可以支撑 A1 字段 dry-run；3 篇 metadata-only 样本只用于失败路径和人工下载队列，不进入已采纳 pattern。

## 3. 检索关键词簇分析

### 3.1 当前推荐关键词簇

1. `software engineering systematic literature review tertiary study`。
2. `software engineering systematic mapping study guidelines`。
3. `requirements engineering tertiary study systematic reviews`。
4. `machine learning software engineering tertiary study`。
5. `software engineering systematic review quality assessment evidence based`。

### 3.2 高命中特征

1. 题名含 `tertiary study` 的 SE 文献通常能直接提供 RQ / dimension / finding / validity pattern。
2. Requirements Engineering 和 ML4SE 子领域已有可用 tertiary / mapping 样本，适合 A2a 扩展。
3. IST / ACM Computing Surveys / ESE 等高等级 venue 能提供强方法学样本，但 PDF 获取可能受限。
4. 早期 EBSE guideline 对 protocol 与 reporting 很有价值，但不能代表近年 SE SLR 全貌。

### 3.3 低命中特征

1. 只含 `survey` 的普通综述常缺少系统检索、纳排和质量评价，需谨慎纳入。
2. 聚合 PDF 链接容易返回 HTML / 登录页；必须用 `file` 或 `pdf_extractor` 检查。
3. 单篇领域 SLR 若没有全文，只能作为 metadata-only 候选，不能抽取 pattern。

### 3.4 检索倾向调整

A2a 应优先扩展 2020 年后的 SE tertiary / survey，覆盖 Requirements Engineering、Testing、MDE、SE4AI、LLM4SE、Empirical SE 等子领域；同时保留 guideline 和 SMS 方法学样本，用于校准维度模式而不是支撑领域发现。

**本节结论**：下一步不应继续只读早期 EBSE 文献，而应分层抽样现代高等级 tertiary / SLR / SMS，特别是子领域化综述和近年软件工程综述方法学。

## 4. 论文列表

| 状态 | 年份 | 标题 | 类型 | 来源等级 | 关键价值 | 目录 |
|---|---:|---|---|---|---|---|
| 🟢 | 2007 | Guidelines for performing Systematic Literature Reviews in Software Engineering | guideline | 技术报告 | SLR protocol / search / selection / extraction / synthesis / reporting 基础。 | [review.md](./papers/kitchenham-charters-2007-slr-guidelines/review.md) |
| 🟡 | 2008 | Systematic Mapping Studies in Software Engineering | SMS 方法 | EASE / BCS | mapping study 方法学候选；本轮 PDF 未获取。 | [review.md](./papers/petersen-2008-systematic-mapping/review.md) |
| 🟢 | 2009 | Systematic literature reviews in software engineering – A systematic literature review | tertiary-like SLR | IST | 早期 SE SLR 总览，RQ/finding/report 结构完整。 | [review.md](./papers/kitchenham-2009-slr-tertiary/review.md) |
| 🟢 | 2011 | Six years of systematic literature reviews in software engineering: An updated tertiary study | updated tertiary | IST | update / integration / 前序研究关系 pattern。 | [review.md](./papers/da-silva-2011-six-years-slr/review.md) |
| 🟢 | 2014 | Systematic Reviews in Requirements Engineering: A Tertiary Study | tertiary | EmpiRE | RE 子领域 tertiary，提供领域专门化模式。 | [review.md](./papers/re-tertiary-study-2014/review.md) |
| 🟢 | 2015 | A Mapping Study on Requirements Engineering in Agile Software Development | SMS | SEAA | SMS taxonomy / benefit / problem / solution pattern。 | [review.md](./papers/re-agile-sms-2015/review.md) |
| 🟡 | 2015 | Guidelines for conducting systematic mapping studies in software engineering: An update | guideline update | IST | SMS guideline update；本轮 PDF 未获取。 | [review.md](./papers/petersen-2015-mapping-guidelines-update/review.md) |
| 🟡 | 2022 | Analysing app reviews for software engineering: a systematic literature review | SLR | ESE | 现代高等级 SLR 候选；本轮 Springer 链接返回 HTML。 | [review.md](./papers/app-reviews-slr-se/review.md) |
| 🟢 | 2023 | Machine Learning for Software Engineering: A Tertiary Study | tertiary | ACM Computing Surveys | 现代高等级 tertiary，提供大规模分类、挑战和行动建议 pattern。 | [review.md](./papers/ml4se-tertiary-study/review.md) |

**本节结论**：A1 样本已覆盖 guideline、tertiary、updated tertiary、SMS 和 metadata-only SLR；仍缺正式全文级现代 ESE SLR 和更多 2020 年后 SE 子领域综述，这正是 A2a 的首要补强方向。

## 5. dry-run 覆盖矩阵

| 验收项 | 当前覆盖 | 结论 |
|---|---|---|
| 3--5 篇 dry-run | 6 篇全文文本级 + 3 篇 metadata-only；主 dry-run 取 5 篇，补充 4 篇用于失败/早期样本 | 通过；不声称完整覆盖 |
| 至少 3 篇全文文本级 | ML4SE tertiary、RE tertiary、Agile RE SMS、Kitchenham guideline、Kitchenham 2009、da Silva 2011 | 通过 |
| 至少 2 类综述类型 | guideline、tertiary、updated tertiary、SMS、metadata-only SLR | 通过 |
| 至少 1 篇高等级来源 | ACM Computing Surveys、IST、ESE metadata-only | 通过 |
| 至少 1 篇非 A / 非顶级来源 | EmpiRE、SEAA、EBSE 技术报告 | 通过 |
| 至少 1 篇非 LLM4SE 子领域 | ML4SE、RE、Agile RE、EBSE 方法学 | 通过 |
| 至少 1 个失败 / 降级路径 | app reviews SLR、Petersen 2008、Petersen 2015 | 通过 |
| 六类 pattern 至少 4 类被填充 | 6 篇全文文本级均填充至少 4 类；validity 部分按证据不足降级 | 通过 |
| 至少 1 个“不适用 / 证据不足”记录 | guideline 的 finding 不适用；metadata-only 无法抽取 pattern；modern samples 的 threats 待深读 | 通过 |

**本节结论**：A1 dry-run 不是形式主义样例；它同时压测了现代高等级样本、子领域 tertiary、SMS、guideline 和全文不可得失败路径。

## 6. 脚手架模式总表

| pattern | 当前观察 | 来源样本 | A2a 处理建议 |
|---|---|---|---|
| RQ pattern | SE tertiary 常问规模、主题、主体、质量、限制、实践影响；SMS 常问 taxonomy、benefits、problems、solutions。 | Kitchenham 2009、da Silva 2011、Bano 2014、Heikkilä 2015、Kotti 2023 | 建立 RQ 模式树，区分 tertiary / SMS / SLR / guideline。 |
| dimension pattern | 常见字段包括研究类型、SE 子领域、topic、quality、search/selection、data extraction、classification axis、practice/education relevance。 | 全文样本 | A2a 应把字段树版本化，并记录字段回填状态。 |
| finding pattern | 从统计观察进一步形成质量缺口、实践影响、research challenges 和 action recommendations。 | da Silva 2011、Kotti 2023、Heikkilä 2015 | 与 Paper2 的 candidate finding ledger 对齐。 |
| evidence presentation pattern | 主要使用搜索分母、纳排、quality assessment、topic taxonomy、review/primary-study 数量、分类表。 | Kitchenham guideline、tertiary samples | 后续要求每个字段有 source anchor。 |
| validity / threat pattern | 包含 search bias、inclusion reliability、quality assessment、protocol deviation；现代样本需进一步深读。 | Kitchenham guideline、Kitchenham 2009；现代样本待补 | A2a 应设为强制字段，未报告时明确记录。 |
| report structure pattern | guideline 与 tertiary/SMS 结构不同；tertiary 常有 previous studies / method / RQ discussion；SMS 常有 taxonomy/results。 | 全文样本 | 允许不同 review_type 对应不同报告结构。 |

**本节结论**：A1 已经抽出可执行的模式先验：RQ 不只是 PICO；dimension 需要树状化；finding 必须分统计观察、缺口和行动建议；证据呈现和 validity 是后续审计方法的核心。

## 7. 候选维度模式与采纳状态

emoji 口径：🟢 = A1 已采纳为后续候选字段；🟡 = 候选但需 A2a 扩展；⏳ = 待全文核验。

| 状态 | 字段 | 来源 | 说明 |
|---|---|---|---|
| 🟢 | `review_type` | guideline / tertiary / SMS / metadata-only 样本 | 已采纳，避免把 guideline 当成普通 tertiary study。 |
| 🟢 | `target_se_subfield` | RE、ML4SE、Agile RE | 已采纳，支撑领域专门化综述元模型。 |
| 🟢 | `predecessor_relation` | da Silva 2011、Petersen 2015 metadata | 已采纳，记录 update / extends / integrates 关系。 |
| 🟡 | `challenge_action_pattern` | Kotti 2023 | 候选，A2a 需从更多现代 tertiary 中验证。 |
| 🟡 | `taxonomy_axis` / `problem_solution_pattern` | Heikkilä 2015 | 候选，适合 SMS 样本；A2a 再决定是否拆成更细的 benefit/problem/solution 子字段。 |
| ⏳ | `app_review_slr_dimension` | app reviews SLR 2022 | 待全文下载后核验。 |

**本节结论**：A1 的关键 schema 回修已经发生：从平铺六类 pattern 扩展出 review type、子领域、前序关系、挑战/行动以及 taxonomy / problem-solution 等可执行字段。

## 8. schema 修订 / 回填日志

| 时间 | 触发条目 | 修订 | 回填状态 | 冻结理由 |
|---|---|---|---|---|
| 2026-06-29 02:18:07 | Kitchenham & Charters 2007 | 新增 `review_type=guideline` 与 `guideline不适用` 缺失值语义 | 已回填全部 review 卡片 | guideline 不生成普通领域 finding，必须允许不适用。 |
| 2026-06-29 02:18:07 | da Silva 2011 / Petersen 2015 | 新增 `predecessor_relation` | da Silva 已全文回填；Petersen 2015 作为 metadata-only 待全文 | update/extends/integrates 关系是 tertiary/guideline update 的核心。 |
| 2026-06-29 02:18:07 | Bano 2014 / Heikkilä 2015 | 新增 `target_se_subfield` 与 SMS taxonomy/problem/solution 候选 | 已回填 RE / Agile RE 样本 | 子领域化模式是导师讨论中“meta-model 由 researcher 设定”的关键前提。 |
| 2026-06-29 02:18:07 | app reviews SLR / Petersen 2008/2015 | 明确 `metadata-only` 不得升级已采纳 pattern | 已进入 manual-download-needed | 高等级来源也不能绕过证据等级。 |

**本节结论**：dry-run 已真实触发 schema 回修，不是先验字段表。当前回修足够支撑 A1，但 A2a 仍需用 30--50 篇核心样本继续检验。

## 9. 失败、阻塞与待复核

| 条目 | 问题 | 当前处理 | 后续动作 |
|---|---|---|---|
| app reviews SLR 2022 | Springer PDF 链接返回 HTML，`pdf_extractor` 报 EOF marker not found | 删除伪 PDF；写入 [search/manual-download-needed.bib](./search/manual-download-needed.bib) | 人工下载 PDF 后重写 review。 |
| Petersen 2008 | SciSpace 链接返回 HTML，不是 PDF | 删除伪 PDF；保留 DOI metadata | 人工下载或图书馆访问。 |
| Petersen 2015 | DOI 已有，PDF 本轮未自动获取 | 保留 metadata-only | 人工下载后补全文。 |
| 现代样本 threat sections | A1 只做有限全文文本核验，未逐页核对 PDF 图表 | review.md 标为待复核 | A2a 深读补页码、表号、threat anchors。 |

**本节结论**：失败路径已被显式管理，没有把不可获取 PDF 冒充已读全文。A2a 的第一件事应是补齐 app reviews SLR、Petersen 2008/2015 这类高价值 metadata-only 条目。

## 10. 后续 A2a / A2b 入口

A2a 建议：

1. 从本目录 9 个种子出发，扩展到 30--50 篇核心样本。
2. 优先补 2020 年后 SE tertiary / SLR / SMS / survey。
3. 每个 SE 子领域至少覆盖一批样本：Requirements Engineering、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE。
4. 把 `pattern-field-schema.md` 拆成更正式的 pattern library，并记录每个字段的 source anchors。

A2b 建议：

1. 扩展到预计 100+ 篇完整文库闭合。
2. 形成第一个可引用快照。
3. 明确纳排分母、排除理由、人工下载清单、覆盖/饱和度判断。
4. 把完整文库快照交给 A3 消费，A3 不再混入大规模补文库。

**本节结论**：A1 已建立可接力的脚手架，但学术价值真正成型要依赖 A2a/A2b 的规模化抽取和饱和度判断。

## 11. 更新日志

| 时间 | 更新内容 | 验证 / 备注 |
|---|---|---|
| 2026-06-29 02:18:07 | 建立 `survey_of_surveys/` README/GUIDE/SUMMARY/search/papers/patterns；完成 6 篇全文文本级 dry-run 和 3 篇 metadata-only 失败路径；回修 schema 字段。 | A1 奠基；未运行真实 LLM，未读取 `.env`，不跑四个真实例子。 |
