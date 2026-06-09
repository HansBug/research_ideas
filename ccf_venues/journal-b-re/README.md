# Requirements Engineering README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | REJ / Requirements Engineering |
| 全称 | Requirements Engineering |
| 类型 | 期刊 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| CCF 等级 | B（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版商 | Springer / Springer Nature（[Springer journal homepage](https://link.springer.com/journal/766)） |
| ISSN | 0947-3602（print）；1432-010X（online）（[DBLP venue information](https://dblp.org/db/journals/re/index.html)；[Springer journal information](https://link.springer.com/journal/766)） |
| 期刊主页 | [Springer Requirements Engineering](https://link.springer.com/journal/766) |
| Author guidelines | [Springer submission guidelines](https://link.springer.com/journal/766/submission-guidelines) |
| Submission system | [Springer Nature Submit your manuscript](https://submission.springernature.com/new-submission/766/3) |
| Special issues / topical collections | [Springer collections and calls for papers](https://link.springer.com/journal/766/collections) |
| Volume / issue archive | [Springer volumes and issues](https://link.springer.com/journal/766/volumes-and-issues) |
| Articles in press / online first | [Springer online first](https://link.springer.com/journal/766/online-first) |
| DBLP venue page | [DBLP Requirements Engineering](https://dblp.org/db/journals/re/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现官方已公布年度卷期、DBLP 年度页或 2029+ CFP |

### 1.1 索引与分区信息

> 本节在 PR #91 中从 PR #90 占位推进为“证据链优先”的真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。JCR / CAS 若没有可追溯单刊证据，宁可写 `⏳`，不得用第三方站点补成分区事实。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🟡 | 沿用本库 CCF B 级；官方目录入口已定位，单条目仍需浏览器行级复核 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本 PR 不重新定义 CCF scope，只保留可点击官方基线入口 | `2026-06-09 13:52` |
| WoS Collection | ⏳ | 待人工核验 Web of Science Core Collection 收录集合 | [Clarivate Master Journal List](https://mjl.clarivate.com/search-results) 为官方检索入口；本轮命令行仅确认 SPA 入口可访问，未取得可审计单刊 `SCIE/SSCI/AHCI/ESCI` 行级结果；后续用 ISSN / eISSN 通过浏览器或机构入口复核 | `2026-06-09 13:52` |
| JCR Quartile | ⏳ | 待人工核验 2025 JCR 单刊 category / rank / quartile | [JCR 平台](https://jcr.clarivate.com/jcr/home)；[2025 JCR 发布说明](https://clarivate.com/news/clarivate-unveils-the-2025-journal-citation-reports/) 仅证明 release 存在，不证明本刊 quartile；需机构入口导出单刊 category、rank、quartile、percentile 后再改为 `1️⃣`--`4️⃣` | `2026-06-09 13:52` |
| CAS 分区 | ⏳ | 待人工核验中科院历史版分区 | [中国科学院文献情报中心停更公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 证明 2026 起不再更新发布；本轮未获得本刊历史版官方行级分区，后续只可用官方 / 机构历史版证据补写 | `2026-06-09 13:52` |
| EI / Compendex | 🟢 | 官方 Compendex `SERIALS` 精确命中，按 source-level 期刊记录 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本地 snapshot `compendex_source_list_2026-06-09.xlsx`，sheet `SERIALS`，Source title `Requirements Engineering`，Source type `Journal`，ISSN `0947-3602`，EISSN `1432-010X`，Publisher `Springer Science and Business Media Deutschland GmbH` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | EI 已有官方 source-list 证据；WoS / JCR / CAS 仍待人工或机构入口核验 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；后续 reviewer 需复核本节链接与 source-list 字段 | `2026-06-09 13:52` |

## 2. Scope 与栏目

- 官方 scope 摘要：Springer [Aims and scope](https://link.springer.com/journal/766/aims-and-scope) 将期刊定位为传播软件密集型信息系统或应用的需求获取、表示与验证相关新成果。
- 官方 scope 同时要求理论与应用论文都明确说明其对复杂系统设计的实践后果，以及实践者如何评价这些想法，见 [Aims and scope](https://link.springer.com/journal/766/aims-and-scope)。
- Article types：Springer [Aims and scope](https://link.springer.com/journal/766/aims-and-scope) 明确列出 Research articles 与 Research commentary，并要求研究论文给出经验研究、实验、案例、仿真、形式化分析或数学证明等有效性证据。
- 投稿模式：常规稿件按 [submission guidelines](https://link.springer.com/journal/766/submission-guidelines) 与 [Submit your manuscript](https://submission.springernature.com/new-submission/766/3) 处理为 rolling submission；带 deadline 的 collections 按年度页和 [../TIMELINE.md](../TIMELINE.md) 的 dated event 规则维护。

## 3. 核心编辑人员情报

本节记录当前 Springer editorial leadership 与若干和本仓库 P1/P2/P3/P4 强相关的 editorial board 成员，不展开全量 board。角色与单位以 [Springer editorial board](https://link.springer.com/journal/766/editorial-board) 为主证据；学术方向与 project 关系基于 DBLP / 公开学术入口归纳，因此在 `核验等级 / 当前性` 列中显式标明口径。

| 姓名 | 期刊角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验等级 / 当前性 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Fabiano Dalpiaz | Editor-in-Chief | Utrecht University, Utrecht, The Netherlands | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Fabiano%20Dalpiaz) | 需求模型、社会技术系统、合规与 NLP/AI for RE | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Fabiano%20Dalpiaz) | P1/P2 强；P3/P4 中到强 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Peri Loucopoulos | Honorary Editor | Bournemouth University；Harokopio University of Athens；Loughborough University（emeritus / retired 2025） | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Peri%20Loucopoulos) | 需求工程、企业建模、信息系统建模 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Peri%20Loucopoulos) | P1/P2 强；P3/P4 间接 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| John Mylopoulos | Honorary Editor | University of Toronto, Toronto, Canada | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=John%20Mylopoulos) | 目标建模、需求工程、概念建模、信息系统 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=John%20Mylopoulos) | P1/P2 最强；P3/P4 间接 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| William Robinson | Honorary Editor | Georgia State University, Atlanta, United States | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=William%20Robinson) | 需求监控、业务规则、软件工程与信息系统 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=William%20Robinson) | P2/P3 中到强；P1/P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Jane Cleland-Huang | Editorial Board | University of Notre Dame, Notre Dame, United States | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Jane%20Cleland-Huang) | requirements traceability、安全关键系统、ML/AI 需求与责任工程 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Jane%20Cleland-Huang) | P1/P2/P3 强；P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Alessio Ferrari | Editorial Board | CNR / University College Dublin | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Alessio%20Ferrari) | 自然语言需求、NLP/LLM for RE、歧义检测与需求数据集 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Alessio%20Ferrari) | P1/P2 最强；P3/P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Jennifer Horkoff | Editorial Board | Chalmers University of Technology / University of Gothenburg | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Jennifer%20Horkoff) | 目标导向需求、建模、AI 系统需求与质量 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Jennifer%20Horkoff) | P1/P2 强；P3 中；P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Daniel Amyot | Editorial Board | University of Ottawa, Ottawa, Canada | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Daniel%20Amyot) | goal-oriented RE、Use Case Maps、业务流程与系统建模 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Daniel%20Amyot) | P1/P2/P3 强；P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Zhi Jin | Editorial Board | Peking University, Beijing, China | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Zhi%20Jin) | 需求工程、知识工程、软件工程、AI for SE | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Zhi%20Jin) | P1/P2 强；P3/P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |
| Lin Liu | Editorial Board | Tsinghua University, Beijing, China | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | [DBLP](https://dblp.org/search?q=Lin%20Liu) | 目标建模、需求工程、服务与社会技术系统 | [DBLP 代表作 / 近年论文入口](https://dblp.org/search?q=Lin%20Liu) | P1/P2 强；P3/P4 中 | Springer 当前 editorial-board roster 核验；方向基于 DBLP / 公开学术入口归纳 | `2026-06-05 11:57` |

## 4. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 强相关 | 需求获取、表示、验证和需求到模型转换与 [Aims and scope](https://link.springer.com/journal/766/aims-and-scope) 高度吻合。 |
| P2 场景与性质生成 | 强相关 | scenarios、requirements validation、formal / empirical evaluation 等方向可直接支撑验证场景与性质生成。 |
| P3 验证剖面与模型检查 | 中到强 | 若论文强调需求规约验证、traceability、形式化分析或复杂系统评价，可对齐 P3。 |
| P4 模型修复 | 中相关 | repair 本身不是 REJ 核心栏目，但需求缺陷、需求债、traceability 和变更影响分析可支撑 P4。 |

## 5. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核查时间 |
|---|---|---|---|
| Journal homepage | [Springer Requirements Engineering](https://link.springer.com/journal/766) | [DBLP RE](https://dblp.org/db/journals/re/index.html) 作 bibliographic fallback | `2026-06-05 11:57` |
| Aims and scope | [Springer aims and scope](https://link.springer.com/journal/766/aims-and-scope) | Scope 事实以 Springer 为准 | `2026-06-05 11:57` |
| Author guidelines | [Springer submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | 指南页包含 manuscript preparation / online submission 说明 | `2026-06-05 11:57` |
| Submission system | [Springer Nature new submission](https://submission.springernature.com/new-submission/766/3) | 由 Springer journal masthead / submission guidelines 的 Submit manuscript 入口指向 | `2026-06-05 11:57` |
| Special issues / topical collections | [Springer collections](https://link.springer.com/journal/766/collections) | 年度页展开 REFSQ 2026、30th Anniversary、LLM collection、RE 2025、RE 2024 等条目 | `2026-06-05 11:57` |
| Volume / issue archive | [Springer volumes and issues](https://link.springer.com/journal/766/volumes-and-issues) | 2022-2026 另挂具体 volume issue；未来年度未公布时用本入口核验 | `2026-06-05 11:57` |
| Articles in press / online first | [Springer online first](https://link.springer.com/journal/766/online-first) | online-first 与正式卷期可能跨年 | `2026-06-05 11:57` |
| DBLP venue | [DBLP Requirements Engineering](https://dblp.org/db/journals/re/index.html) | 年度计数 baseline / bibliographic fallback | `2026-06-05 11:57` |
| Editorial board | [Springer editorial board](https://link.springer.com/journal/766/editorial-board) | 当前核心编辑人员角色来源 | `2026-06-05 11:57` |

## 6. 年度信息汇总

状态口径：`🟢` 表示常规 rolling 开放；`🟡` 表示当年有或有过 dated collection CFP；`✅` 表示年度已归档；核验列 `🟡` 表示已完成基础链接和 DBLP baseline，但仍需 publisher article type / issue TOC 交叉核验。

| 年份 | 年度状态 | 期刊主页 | Author guidelines | Submission system | Special issue / CFP | 关键截止时间 | Volume / issue | Articles / Online first | DBLP 年度页 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| [`2028`](./2028/README.md) | 🟢 | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | 无已知（[Springer collections](https://link.springer.com/journal/766/collections)） | 滚动投稿 | ⏳ 已检索未公布（[volumes and issues](https://link.springer.com/journal/766/volumes-and-issues)） | [Online first](https://link.springer.com/journal/766/online-first) | ⏳ 已检索未公布（[DBLP RE](https://dblp.org/db/journals/re/index.html)） | ⏳ 已检索未公布 | 🟡 |
| [`2027`](./2027/README.md) | 🟢 | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | 无已知（[Springer collections](https://link.springer.com/journal/766/collections)） | 滚动投稿 | ⏳ 已检索未公布（[volumes and issues](https://link.springer.com/journal/766/volumes-and-issues)） | [Online first](https://link.springer.com/journal/766/online-first) | ⏳ 已检索未公布（[DBLP RE](https://dblp.org/db/journals/re/index.html)） | ⏳ 已检索未公布 | 🟡 |
| [`2026`](./2026/README.md) | 🟡 | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | [REFSQ 2026](https://link.springer.com/collections/gidfjjdijf)；[30th Anniversary](https://link.springer.com/collections/hegaifabjh)（By Invite Only）；[LLM collection](https://link.springer.com/collections/deebijccbh) | [LLM collection](https://link.springer.com/collections/deebijccbh)：2026-04-30 待补时刻；[30th Anniversary](https://link.springer.com/collections/hegaifabjh)：2026-06-20 待补时刻（邀请制）；[REFSQ 2026](https://link.springer.com/collections/gidfjjdijf)：2026-06-29 待补时刻 | [Vol. 31 Issue 1](https://link.springer.com/journal/766/volumes-and-issues/31-1) | [Online first](https://link.springer.com/journal/766/online-first) | [DBLP Vol. 31](https://dblp.org/db/journals/re/re31.html) | 6 | 🟡 |
| [`2025`](./2025/README.md) | ✅ | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | [RE 2025](https://link.springer.com/collections/hbagjecafi) 已关闭 | 滚动投稿 | [Vol. 30 Issue 1](https://link.springer.com/journal/766/volumes-and-issues/30-1) | [Online first](https://link.springer.com/journal/766/online-first) | [DBLP Vol. 30](https://dblp.org/db/journals/re/re30.html) | 9 | 🟡 |
| [`2024`](./2024/README.md) | ✅ | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | [RE 2024 invite-only](https://link.springer.com/collections/djjfgheaej) 已关闭 | 滚动投稿 | [Vol. 29 Issue 1](https://link.springer.com/journal/766/volumes-and-issues/29-1) | [Online first](https://link.springer.com/journal/766/online-first) | [DBLP Vol. 29](https://dblp.org/db/journals/re/re29.html) | 24 | 🟡 |
| [`2023`](./2023/README.md) | ✅ | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | 无已知（[Springer collections](https://link.springer.com/journal/766/collections)） | 滚动投稿 | [Vol. 28 Issue 1](https://link.springer.com/journal/766/volumes-and-issues/28-1) | [Online first](https://link.springer.com/journal/766/online-first) | [DBLP Vol. 28](https://dblp.org/db/journals/re/re28.html) | 26 | 🟡 |
| [`2022`](./2022/README.md) | ✅ | [Springer RE](https://link.springer.com/journal/766) | [Submission guidelines](https://link.springer.com/journal/766/submission-guidelines) | [Submit manuscript](https://submission.springernature.com/new-submission/766/3) | 无已知（[Springer collections](https://link.springer.com/journal/766/collections)） | 滚动投稿 | [Vol. 27 Issue 1](https://link.springer.com/journal/766/volumes-and-issues/27-1) | [Online first](https://link.springer.com/journal/766/online-first) | [DBLP Vol. 27](https://dblp.org/db/journals/re/re27.html) | 25 | 🟡 |

## 7. 2029+ 检索结论与维护备注

| 检索对象 | 官方 / fallback 链接 | 结论 | 核查时间 |
|---|---|---|---|
| Springer collections / calls for papers | [Springer collections](https://link.springer.com/journal/766/collections) | 当前只核到 REFSQ 2026、30th Anniversary、LLM collection、RE 2025、RE 2024 等 collection；未发现 `2029+` Requirements Engineering 官方 CFP 或 dated deadline。 | `2026-06-05 11:57` |
| Springer volume / issue archive | [Springer volumes and issues](https://link.springer.com/journal/766/volumes-and-issues) | 当前只以 2022-2026 已发布卷期和长期 archive 为可核验事实；未发现 `2029+` 年度卷期入口。 | `2026-06-05 11:57` |
| DBLP venue page | [DBLP Requirements Engineering](https://dblp.org/db/journals/re/index.html) | 当前可见年度页到 [Volume 31, 2026](https://dblp.org/db/journals/re/re31.html)；未发现 `2027+` / `2029+` DBLP 年度页。 | `2026-06-05 11:57` |

维护备注：

- 2026 collections 当前口径：1 个公开开放 CFP（REFSQ 2026）+ 1 个邀请制开放 collection（30th Anniversary）+ 1 个已关闭 collection（LLM）；不得把 By Invite Only 写成普通公开 CFP。
- 2022-2026 论文数量采用 DBLP entry article baseline：2026=6、2025=9、2024=24、2023=26、2022=25；该数不是 Springer publisher 最终闭合数，后续需按 Springer issue TOC / online first 交叉核验。
- 常规投稿为 rolling，不进入 Mermaid dated event；Springer collections 中带明确日期的 deadline 按 [../TIMELINE.md](../TIMELINE.md) 的年度事件表和 Mermaid Gantt 维护；只有月份的 revision / final decision 信息只在年度页备注保留，不硬凑具体日期。
- 2027/2028 年度页仅作为 rolling submission 与未来核验占位，不能写成已经公布年度卷期或 CFP。

## 8. TIMELINE.md 同步提示

- Requirements Engineering rolling submission 已同步至 [../TIMELINE.md](../TIMELINE.md) 的“期刊滚动投稿 / 未定日期”表，链接 [submission guidelines](https://link.springer.com/journal/766/submission-guidelines)、[submission system](https://submission.springernature.com/new-submission/766/3)、[volumes and issues](https://link.springer.com/journal/766/volumes-and-issues)、[online first](https://link.springer.com/journal/766/online-first) 和本库年度页。
- 2026 年 Springer collections 中的 [30th Anniversary](https://link.springer.com/collections/hegaifabjh) submission deadline `2026-06-20 待补时刻` 与 [REFSQ 2026](https://link.springer.com/collections/gidfjjdijf) submission deadline `2026-06-29 待补时刻` 已同步至 2026 时间线和 Mermaid Gantt。
- [Rethinking Requirements Engineering in the Age of Large Language Models](https://link.springer.com/collections/deebijccbh) 已关闭，官方页面记录 submission deadline `2026-04-30 待补时刻`，已作为历史 dated event 同步至 2026 时间线；同页 `Revisions Due: July 2026`、`Final Decisions: September 2026` 仅给月份，不写入 dated event。

## 9. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 13:16` | PR #35 近期窗口复审修复：细化 2026 collections 口径，区分 REFSQ 公开开放、30th Anniversary 邀请制开放与 LLM collection 已关闭。 |
| `2026-06-05 12:47` | 专项复核 2026 Springer collections 表述：根年度表补入 LLM collection submission deadline，并明确 LLM revision / final decision 只有月份，不硬凑 dated event。 |
| `2026-06-05 11:57` | 初始化 Requirements Engineering 期刊 README，补齐 2022-2028 年度入口、核心链接、DBLP entry article baseline、2026 collections deadline、2029+ 检索结论与核心编辑人员情报。 |
