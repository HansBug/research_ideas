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

若文字模式提取异常，再记录 OCR 或人工核验需求。不可获取 PDF 不得假装已读全文，必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。

## 6. 模式字段抽取规则

每篇 `review.md` 至少抽取六类 pattern：

1. RQ pattern。
2. dimension pattern。
3. finding pattern。
4. evidence presentation pattern。
5. validity / threat pattern。
6. report structure pattern。

每类 pattern 必须有：抽取结论、证据锚点、可迁移性、不可迁移点。若某类不适用，写“不适用”并说明是 `guideline`、`metadata-only`、`目标不符` 还是 `原文未报告`。

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
