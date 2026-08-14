# issue #95 十篇现代维度锚点来源审计

## 1. 审计目的

本文件记录 PR-A1 将 issue [#95](https://github.com/HansBug/research_ideas/issues/95) 中 10 篇现代 survey / SLR / SMS / roadmap 条目纳入 `survey_of_surveys/` 的来源、选择理由、全文状态和统计池资格。它只服务 A1 scaffold hardening，不表示 A2a/A2b 的完整 `survey_of_surveys` 文库已经完成。

## 2. 来源与时间

| 项 | 内容 |
|---|---|
| 上游讨论入口 | issue [#95](https://github.com/HansBug/research_ideas/issues/95) |
| 候选总表 | <https://gist.github.com/HansBug/2310896ff4921f3d4809001571228820> |
| 相关审计表 | `issue95_fulltext_download_audit_438papers.csv`、`issue95_fulltext_structure_analysis_87papers.csv`（来自上述 Gist / issue 线索；本 PR 不把 CSV 原件整体入库） |
| 本轮纳入时间 | 2026-06-29 |
| 本轮处理目标 | 选出 10 篇与“综述之综述维度 scaffold / 研究者定义元模型 / 字段证据链 / research finding 裁决”高度相关或互补的现代锚点 |

## 3. 选择原则

1. **现代性**：优先 2023--2026 年，能反映近期 CCF-A/B SE 综述、LLM4SE、MDE、RE、DevSecOps 与开放制品研究的写法。
2. **维度贡献**：必须至少能启发 A1-M0--M6 中若干层，例如研究意图、纳排、主题语义、方法干预、证据资产、统计就绪、finding 裁决。
3. **类型多样性**：同时覆盖 SLR、SMS、systematic mapping、multivocal literature review、vision / roadmap、solution proposal、theory/evaluation/roadmap，避免只学习一种报告模板。
4. **统计池分离**：可作为 schema seed 不等于可进入统计合成池；roadmap / vision / solution proposal 即使很有启发，也必须机器可读排除出统计池。
5. **证据可追溯**：优先能自动获取公开 PDF 或开放预印本的条目；无法获取时进入统一 [manual-download-needed.bib](./manual-download-needed.bib)。本轮 10 篇均已获取 PDF 或开放预印本，因此没有新增人工下载条目。

## 4. 十篇条目审计表

| 标题 | 年份口径 | 出版形态 / venue | PDF 状态 | schema seed | 统计池资格 | 选择理由 | 目录 |
|---|---:|---|---|---|---|---|---|
| On the road to interactive LLM-based systematic mapping studies | 2025；online first 2024 | 期刊 / IST | 已获取 | 是 | 否 | LLM-supported mapping study 流程、人机交互、agent 角色与 traceability 风险；作为 solution proposal 边界锚点。 | [review.md](../papers/interactive-llm-systematic-mapping/review.md) |
| Research artifacts in secondary studies: A systematic mapping in software engineering | 2025 | 期刊 / IST | 已获取 | 是 | 是 | secondary study artifact、repository、DOI、dead link、复现资产字段锚点。 | [review.md](../papers/research-artifacts-secondary-studies/review.md) |
| The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study | 2026 | 期刊 / TOSEM | 已获取开放预印本 | 是 | 是 | 现代 CCF-A SLR+SMS；RQ0--RQ3、SPACE mapping、benefit/risk、质量评价与主题综合写法。 | [review.md](../papers/llm-assistants-developer-productivity/review.md) |
| Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap | 2026 | 期刊 / TOSEM | 已获取开放预印本 | 是 | 否 | AI-native SE roadmap、challenge、vision 与研究议程；作为 roadmap 边界锚点，不进统计池。 | [review.md](../papers/ai-native-se-roadmap/review.md) |
| Large Language Models for Software Engineering: A Systematic Literature Review | 2024 | 期刊 / TOSEM | 已获取开放预印本 | 是 | 是 | 大规模 LLM4SE SLR 字段体系、SDLC/task tree、artifact 与 evidence practices。 | [review.md](../papers/llm4se-systematic-review/review.md) |
| Formal requirements engineering and large language models: A two-way roadmap | 2025 | 期刊 / IST | 已获取 | 是 | 否 | Formal RE + LLM 双向 roadmap、trustworthiness concern 与交互边界；不进统计池。 | [review.md](../papers/formal-re-llm-roadmap/review.md) |
| Understanding the landscape of software modelling assistants for MDSE tools: A systematic mapping | 2024 | 期刊 / IST | 已获取 | 是 | 是 | 最贴近 LLM4modeling / STM generation 的 strategy-goal-limitation-metric-user 树状维度样本。 | [review.md](../papers/mdse-modelling-assistants-mapping/review.md) |
| Model driven engineering for machine learning components: A systematic literature review | 2024 | 期刊 / IST | 已获取 | 是 | 是 | MDE4ML SLR 的 motivation / solution / evaluation / limitation 字段与统计综合样本。 | [review.md](../papers/mde-ml-components-slr/review.md) |
| Identifying the primary dimensions of DevSecOps: A multi-vocal literature review | 2024 | 期刊 / JSS | 已获取 | 是 | 是 | MLR 的 primary dimensions、CPTM 模型、灰色文献 / 学术文献合并边界。 | [review.md](../papers/devsecops-primary-dimensions/review.md) |
| Requirements quality research: a harmonized theory, evaluation, and roadmap | 2023 | 期刊 / Requirements Engineering | 已获取 | 是 | 否 | requirements quality theory / evaluation / roadmap 元模型；适合 A1-M0/A1-M6，不进统计池。 | [review.md](../papers/requirements-quality-theory-roadmap/review.md) |

## 5. CCF 与年份口径

- CCF 大类 / 等级字段目标上应以 CCF 官方最新国际推荐目录为准；本轮 2026-06-29 访问官方 [软件工程 / 系统软件 / 程序设计语言目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) 时，HTTP/CLI 均返回 Aliyun WAF 壳，无法从页面正文自动核验 TOSEM / IST / JSS / Requirements Engineering 等 venue。当前字段采用本地 `ccf_venues/` 已建档缓存作为工作口径，并统一标注“本地缓存；官方待人工复核”。
- `On the road to interactive LLM-based systematic mapping studies` 的 DOI 年份与 online-first 时间横跨 2024/2025；本 PR 在总账和候选池中按正式 IST 卷期 / BibTeX 年份 2025 统计，并在单篇 `metadata.json` 与 `review.md` 保留 online-first 日期。

## 6. CSV 未整体入库原因

issue #95 的 CSV 审计表服务于更大候选池筛查，体量与字段均超过 A1 当前 scaffold 的必要证据范围。本 PR 仅把十篇纳入条目的可追溯选择结果、PDF 状态、统计池资格和单篇证据链入库；若 A2a/A2b 需要重建完整候选池，应另建 `search/raw/` 或 `runs/` 级别的完整检索记录。

## 7. 当前结论

这 10 篇使 A1 从“早期方法学 dry-run”升级为“现代维度 scaffold 压测”：既能学习系统综述 / 映射研究如何设计字段和统计，也能通过 roadmap / proposal 样本明确哪些内容只能启发 schema、不能进入统计池。后续 A2a 应基于这些锚点扩展 30--50 篇核心样本，并继续验证 A1-M0--M6 的字段饱和度与缺失值语义。
