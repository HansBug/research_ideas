# EASE README

> 信息更新时间：`2026-06-09 18:18:06`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | EASE |
| 全称 | International Conference on Evaluation and Assessment in Software Engineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / P2 邻近观察 |
| CCF 等级 | 🥉 |
| 本库目录 | `conf-c-ease` |
| 出版方 | ACM / EASE official researchr pages |
| 官方 series page | [EASE series](https://conf.researchr.org/series/ease) |
| 官方当前 / 最新年度主页 | [EASE 2026](https://conf.researchr.org/home/ease-2026) |
| 官方 CFP / Important Dates 总入口 | [EASE 2026 dates](https://conf.researchr.org/dates/ease-2026) |
| 官方 proceedings / paper list 总入口 | [DBLP / proceedings fallback](https://dblp.org/db/conf/ease/index.html) |
| DBLP venue page | [DBLP EASE index](https://dblp.org/db/conf/ease/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `10th International Conference on Evaluation and Assessment in Software Engineering, EASE 2006`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

EASE 聚焦 empirical / evidence-based / evaluation and assessment in software engineering，适合作为 LLM4SE benchmark、人因评估、质量评估和研究方法的 P2 邻近观察入口。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 🟡 中：LLM4SE / AI models / empirical design 可支持状态机建模评估。 |
| P2 | 🟢 高 | 🟢 高：场景/性质生成方法需要实验设计、benchmark、人因与评估证据。 |
| P3 | 🟡 中 | 🟡 中：验证 profile 的实证评价可从 EASE 方法论借鉴。 |
| P4 | 🟡 中 | 🟡 中：repair 方法评估、人因和质量指标可提供邻近线索。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [EASE series](https://conf.researchr.org/series/ease) | 年度事实仍以年度主页 / CFP / committee 为准 | `2026-06-05 17:23` |
| Latest year homepage | [EASE 2026](https://conf.researchr.org/home/ease-2026) | 2027/2028 已检索未公布 | `2026-06-05 17:23` |
| CFP / Important Dates | [EASE 2026 dates](https://conf.researchr.org/dates/ease-2026) | 历史年度在年度 README 展开 | `2026-06-05 17:23` |
| Submission system | [2026 submission](https://easychair.org/conferences/?conf=ease2026) | 投稿系统可能按 track 拆分；年度页保留具体入口 | `2026-06-05 17:23` |
| Program / accepted papers | [2026 program](https://conf.researchr.org/program/ease-2026/program-ease-2026/) | 已结束年度优先官方 program / accepted；缺失时用 DBLP fallback | `2026-06-05 17:23` |
| Proceedings | [Proceedings入口](https://dl.acm.org/doi/proceedings/10.1145/3756681) | 出版商 / proceedings DOI 优先；受限时记录 WAF / 已检索未获可审计证据 | `2026-06-05 17:23` |
| DBLP venue | [DBLP venue](https://dblp.org/db/conf/ease/index.html) | 仅作论文名录 / 计数 fallback | `2026-06-05 17:23` |

## 5. 核心人员情报

> 核心人员情报优先来自官方 organizing / committee / track 页面；研究方向和代表作入口来自个人主页、机构页、DBLP 或公开学术入口。P2 venue 的人员表只记录投稿分流和研究社区画像所需的代表性 leadership，不扩展为全量 PC roster。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Tim Storer | 2026 / General Co-Chair | General Co-Chair | University of Glasgow | [官方角色来源](https://conf.researchr.org/committee/ease-2026/ease-2026-organizing-committee) | [学术入口](https://dblp.org/pid/71/3614.html) | empirical software engineering, software engineering practice | [论文入口](https://dblp.org/pid/71/3614.html) | P2：实证评估与研究方法 | 🟡 部分核验 | `2026-06-05 17:53` |
| Ashkan Sami | 2026 / General Co-Chair | General Co-Chair | University of Glasgow | [官方角色来源](https://conf.researchr.org/committee/ease-2026/ease-2026-organizing-committee) | [学术入口](https://dblp.org/search?q=Ashkan%20Sami) | software engineering / education / empirical line (待补个人主页) | [论文入口](https://dblp.org/search?q=Ashkan%20Sami) | P2：实证与教育邻近 | 🟡 部分核验 | `2026-06-05 17:53` |
| Silvia Abrahão | 2026 / Program Co-Chair | Program Co-Chair | Universitat Politècnica de València | [官方角色来源](https://conf.researchr.org/committee/ease-2026/ease-2026-organizing-committee) | [学术入口](https://dblp.org/pid/22/6690.html) | model-driven engineering, empirical SE, software quality | [论文入口](https://dblp.org/pid/22/6690.html) | P1/P2：模型质量与实证评估 | 🟡 部分核验 | `2026-06-05 17:53` |
| Xin Xia | 2026 / Program Co-Chair | Program Co-Chair | Monash University | [官方角色来源](https://conf.researchr.org/committee/ease-2026/ease-2026-organizing-committee) | [学术入口](https://dblp.org/pid/17/9124.html) | software analytics, mining repositories, AI4SE | [论文入口](https://dblp.org/pid/17/9124.html) | P2/P4：数据驱动评估与维护 | 🟡 部分核验 | `2026-06-05 17:53` |
| Triet Le | 2025/2026 / AI Models & Data Co-Chair | AI Models & Data Co-Chair | University of Adelaide / EASE official committees | [官方角色来源](https://conf.researchr.org/committee/ease-2026/ease-2026-ai-models---data-ai-models---data) | [学术入口](https://dblp.org/search?q=Triet%20Le%20software%20engineering) | AI models / empirical SE line (待补个人主页) | [论文入口](https://dblp.org/search?q=Triet%20Le%20software%20engineering) | P1/P2：AI model / data track | 🟡 部分核验 | `2026-06-05 17:53` |
| Jennifer Horkoff | 2026 / Prompt-SE organizing committee | Prompt-SE organizing committee | Chalmers / University of Gothenburg | [官方角色来源](https://conf.researchr.org/committee/ease-2026/prompt-se-2026-papers-organizing-committee) | [学术入口](https://dblp.org/pid/79/1914.html) | requirements engineering, goal modeling, modeling and AI | [论文入口](https://dblp.org/pid/79/1914.html) | P1/P2：需求建模、prompt-SE | 🟡 部分核验 | `2026-06-05 17:53` |
| Muhammad Ali Babar | 2025 / General Co-Chair | General Co-Chair | University of Adelaide | [官方角色来源](https://conf.researchr.org/committee/ease-2025/ease-2025-organizing-committee) | [学术入口](https://dblp.org/pid/62/1515.html) | empirical SE, software architecture, human/AI SE | [论文入口](https://dblp.org/pid/62/1515.html) | P2：实证方法和软件架构评估 | 🟡 部分核验 | `2026-06-05 17:53` |
| Alexander Serebrenik | 2024 / Program Co-Chair | Program Co-Chair | Eindhoven University of Technology | [官方角色来源](https://conf.researchr.org/committee/ease-2024/ease-2024-organizing-committee) | [学术入口](https://dblp.org/pid/60/1211.html) | empirical SE, social aspects, software analytics | [论文入口](https://dblp.org/pid/60/1211.html) | P2/P4：实证与软件仓库数据 | 🟡 部分核验 | `2026-06-05 17:53` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🔵 会期临近 | [年度主页](https://conf.researchr.org/home/ease-2026) | [CFP / track](https://conf.researchr.org/track/ease-2026/ease-2026-research-papers) | [Dates](https://conf.researchr.org/dates/ease-2026) | [Submission](https://easychair.org/conferences/?conf=ease2026) | [Program / accepted](https://conf.researchr.org/program/ease-2026/program-ease-2026/) | 未公布 | 未公布 | 2026-01-16 | 2026-01-23 | 2026-03-13 | 2026-06-09..2026-06-12 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/ease-2025) | [CFP / track](https://conf.researchr.org/track/ease-2025/ease-2025-research-papers) | [Dates](https://conf.researchr.org/dates/ease-2025) | [Submission](https://easychair.org/conferences/?conf=ease2025) | [Program / accepted](https://conf.researchr.org/program/ease-2025/program-ease-2025/) | [Proceedings](https://dl.acm.org/doi/proceedings/10.1145/3756681) | [DBLP](https://dblp.org/db/conf/ease/ease2025.html) | 2025-01-24 | 2025-01-31 | 2025-03-21 | 2025-06-17..2025-06-20 | DBLP fallback entries=126；ACM proceedings DOI candidate CLI 403 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/ease-2024) | [CFP / track](https://conf.researchr.org/track/ease-2024/ease-2024-papers) | [Dates](https://conf.researchr.org/dates/ease-2024) | [Submission](https://easychair.org/conferences/?conf=ease2024) | [Program / accepted](https://conf.researchr.org/program/ease-2024/program-ease-2024/) | [Proceedings](https://dl.acm.org/doi/proceedings/10.1145/3661167) | [DBLP](https://dblp.org/db/conf/ease/ease2024.html) | 2024-01-11 | 2024-01-18 | 2024-03-06 | 2024-06-18..2024-06-21 | DBLP fallback entries=100；ACM proceedings DOI candidate CLI 403 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/ease-2023) | [CFP / track](https://conf.researchr.org/track/ease-2023/ease-2023-research) | [Dates](https://conf.researchr.org/dates/ease-2023) | [Submission](https://easychair.org/conferences/?conf=ease2023) | [Program / accepted](https://conf.researchr.org/program/ease-2023/program-ease-2023/) | [Proceedings](https://conf.researchr.org/info/ease-2023/proceedings) | [DBLP](https://dblp.org/db/conf/ease/ease2023.html) | 2023-01-13 | 2023-01-20 | 2023-03-06 | 2023-06-13..2023-06-16 | DBLP fallback entries=76 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/ease-2022) | [CFP / track](https://conf.researchr.org/track/ease-2022/ease-2022-research) | [Dates](https://conf.researchr.org/track/ease-2022/ease-2022-research) | [Submission](https://easychair.org/conferences/?conf=ease2022) | [Program / accepted](https://conf.researchr.org/program/ease-2022/program-ease-2022/) | [Proceedings](http://dl.acm.org/citation.cfm?id=3530019) | [DBLP](https://dblp.org/db/conf/ease/ease2022.html) | 2022-01-24 | 2022-01-31 | 2022-03-16 | 2022-06-13..2022-06-15 | DBLP fallback entries=66 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 本目录属于 PR-9 / P2 邻近观察，只服务于检索扩展、投稿分流和社区画像，不把 EASE 升级为 P0/P1 主投目标。
- 论文数量优先使用官方 accepted / proceedings；DBLP 只作 fallback，且不得写成 main / research track count。
- Research、industry、tool、artifact、workshop、special session、virtual / live segment 必须分开记录，不能混算。
- 2027/2028 公开信息已检索；未公布年度保留占位，不预造 deadline / committee / proceedings。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的年度表格与 Mermaid Gantt。
- 会议 `Conference dates` 也必须进入 TIMELINE 表格和 Mermaid；无日期或未公布事项不得进入 dated Mermaid。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 18:03` | 修复 PR-9 根 README 一致性：补回核心人员表 `单位` 列，并按 2026-06-05 当前阶段同步 2026 年度状态。 |
| `2026-06-05 17:23` | PR-9 初始化 EASE P2 邻近观察 venue README，覆盖 2022--2028 年度索引、核心链接、人员情报、计数口径和待补记录。 |
