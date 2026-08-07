# REFSQ README

> 信息更新时间：`2026-08-07 20:25:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | REFSQ |
| 全称 | International Working Conference on Requirements Engineering: Foundation for Software Quality |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | 🥉 |
| 出版方 | Springer LNCS / LNBIP；部分 workshop / artifact 入口可能在 CEUR 或 DBLP 分散 |
| 官方 series page | [researchr REFSQ series](https://conf.researchr.org/series/refsq) |
| 官方当前 / 最新年度主页 | [REFSQ 2027](https://2027.refsq.org/) |
| 官方 CFP / Important Dates 总入口 | [Important Dates](https://2027.refsq.org/dates/refsq-2027) |
| 官方 proceedings / paper list 总入口 | 未提供跨年度统一入口；逐年度使用 official program / publisher / DBLP fallback |
| DBLP venue page | [DBLP REFSQ](https://dblp.org/db/conf/refsq/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中 REFSQ 代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `REFSQ 2005 - 11th International Workshop on Requirements Engineering: Foundation for Software Quality...`，Source type `Proceeding` | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 Compendex source-list 字段、book-series 线索和缩写碰撞规则完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:45` |

## 2. Scope 与方向

REFSQ 是需求工程基础与软件质量交叉的小型会议，关注需求质量、需求建模、requirements foundations、empirical RE、industry experience、open science、education / training 与 journal early feedback。相较 RE，REFSQ 更适合作为 P1/P2 的专题深挖入口：需求质量、需求语义、traceability、NLP / LLM for RE 和 early-stage idea 往往更集中。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | 需求质量、概念建模、需求语义和 NLP for RE 可直接支撑需求到状态机元素抽取。 |
| P2 场景与性质生成 | 高 | 软件质量、requirements validation、traceability 与 open science artifact 可支撑验证场景 / 性质生成。 |
| P3 验证剖面与模型检查 | 中 | 形式化 requirements 与质量属性论文可作为待验证性质来源，但不是主验证 venue。 |
| P4 模型修复 | 低-中 | requirements evolution / inconsistency 相关论文可提供上游线索，但会议主轴不是 repair。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [researchr REFSQ series](https://conf.researchr.org/series/refsq) | researchr / 年度独立站点为主 | `2026-06-06 13:16` |
| Latest year homepage | [REFSQ 2027](https://2027.refsq.org/) | Research dates 已公布；2028/2029+ 已复查未见官方年度信息 | `2026-07-13 10:27:51` |
| CFP / Call for Papers | [REFSQ 2027 Research](https://2027.refsq.org/track/refsq-2027-research-papers) | 年度 CFP 分散在 track 页面 | `2026-07-13 10:27:51` |
| Important Dates | [Important Dates](https://conf.researchr.org/dates/refsq-2027) | 官方 dates 页；历史年度在年度 README 展开 | `2026-07-13 10:27:51` |
| Submission system | [EasyChair REFSQ 2026](https://easychair.org/conferences/?conf=refsq2026) | 历史年度入口需逐年复核 | `2026-06-06 13:16` |
| Program / accepted papers | [Program](https://2026.refsq.org/program/program-refsq-2026/) / [Accepted Papers](https://2026.refsq.org/track/refsq-2026-research-papers) | 已结束年度优先官方 program / accepted papers | `2026-06-06 13:16` |
| Proceedings | Springer LNCS / LNBIP 与 CEUR 分散，逐年度待补卷号 | DBLP 仅作论文名录 / 计数 fallback | `2026-06-06 13:16` |
| DBLP venue | [DBLP REFSQ](https://dblp.org/db/conf/refsq/) | 仅作论文名录 / 计数 fallback | `2026-06-06 13:16` |

## 5. 核心人员情报

> 人员角色以官方 organizing / track committee 页面为准；学术入口优先个人主页、机构页与 DBLP。当前初版不展开全量 PC，只保留 chair、track chair、steering / 领域权威线索。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sallam Abualhaija | 2027 / research | PC Co-Chair | University of Luxembourg | [REFSQ 2027 organizing committee](https://2027.refsq.org/committee/refsq-2027-organizing-committee) | [DBLP](https://dblp.org/pid/182/7667.html) | requirements engineering、NLP for RE、regulatory / legal requirements | [DBLP recent publications](https://dblp.org/pid/182/7667.html) | P1/P2 高：AI / NLP 辅助需求抽取、规约质量 | 🟢 已核验入口 | `2026-06-06 13:16` |
| Jan-Philipp Steghöfer | 2027 / research | PC Co-Chair | XITASO GmbH | [REFSQ 2027 organizing committee](https://2027.refsq.org/committee/refsq-2027-organizing-committee) | [DBLP](https://dblp.org/pid/06/9207.html) | traceability、requirements engineering、software process / education | [DBLP recent publications](https://dblp.org/pid/06/9207.html) | P1/P2 中高：traceability 与需求质量数据线索 | 🟢 已核验入口 | `2026-06-06 13:16` |
| Renata Guizzardi | 2026 / research | PC Chair | University of Twente | [REFSQ 2026 organizing committee](https://2026.refsq.org/committee/refsq-2026-organizing-committee) | [DBLP](https://dblp.org/pid/80/134.html) | conceptual modeling、ontology、requirements quality | [DBLP recent publications](https://dblp.org/pid/80/134.html) | P1 高：需求概念建模、质量语义与模型元素抽取 | 🟢 已核验入口 | `2026-06-06 13:16` |
| João Araújo | 2026 / research | PC Chair | NOVA LINCS, Universidade NOVA de Lisboa | [REFSQ 2026 organizing committee](https://2026.refsq.org/committee/refsq-2026-organizing-committee) | [DBLP](https://dblp.org/pid/a/JoaoAraujo.html) | requirements engineering、model-driven engineering、software variability | [DBLP recent publications](https://dblp.org/pid/a/JoaoAraujo.html) | P1/P2 高：RE + MDE 交叉，适合需求到模型相关工作 | 🟢 已核验入口 | `2026-06-06 13:16` |
| Samuel Fricker | 2027 / conference | General Chair；2026 Background Organization Chair | FHNW | [REFSQ 2027 organizing committee](https://2027.refsq.org/committee/refsq-2027-organizing-committee) / [REFSQ 2026 organizing committee](https://2026.refsq.org/committee/refsq-2026-organizing-committee) | [DBLP](https://dblp.org/pid/47/576.html) | requirements engineering、software product management、innovation / industry RE | [DBLP recent publications](https://dblp.org/pid/47/576.html) | P1/P2 中：需求质量、工业需求流程与案例线索 | 🟢 已核验入口 | `2026-06-06 13:16` |

## 6. 年度信息汇总

年度汇总表按年份降序排列。官方仅给日期而未核实具体时刻的 deadline 统一写作 `待补时刻 AoE`；Research / main track 数量不得混入 Industry、RE@Next、artifact、poster / tool 等其他 track。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟢 投稿中 | [REFSQ 2027](https://2027.refsq.org/) | [Research Papers](https://2027.refsq.org/track/refsq-2027-research-papers) | [Important Dates](https://conf.researchr.org/dates/refsq-2027) | [EasyChair `refsq2027`](https://easychair.org/conferences/?conf=refsq2027)（入口已公布，官方逐字 `Submissions will open later this year.`，尚未开放） | 未公布 | 未公布 | ⏳ 已检索未公布 | 2026-11-05 待补时刻 AoE | 2026-11-12 待补时刻 AoE | 2027-01-14 待补时刻 AoE | 2027-04-12..2027-04-15 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | ✅ 已结束/论文名录已公开 | [REFSQ 2026](https://2026.refsq.org/) | [Research Track](https://2026.refsq.org/track/refsq-2026-research-papers) | [Important Dates](https://2026.refsq.org/dates/refsq-2026) | [EasyChair REFSQ 2026](https://easychair.org/conferences/?conf=refsq2026) | [Program](https://2026.refsq.org/program/program-refsq-2026/) / [Accepted Papers](https://2026.refsq.org/track/refsq-2026-research-papers) | 未公布（Springer LNCS / LNBIP 待补卷号） | ⏳ 已检索未公布 | 2025-10-10 待补时刻 AoE | 2025-10-17 待补时刻 AoE | 2025-12-15 待补时刻 AoE | 2026-03-23..2026-03-26 | 官方 Research Track accepted 已公开；数量待脚本复核 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [REFSQ 2025](https://2025.refsq.org/) | [Research Track](https://2025.refsq.org/track/refsq-2025-research-papers) | [Important Dates](https://2025.refsq.org/dates/refsq-2025) | 待补（历史 EasyChair 入口需复核） | [Program](https://2025.refsq.org/program/program-refsq-2025/) / [Research Track](https://2025.refsq.org/track/refsq-2025-research-papers) | 待补（Springer LNCS / LNBIP 卷号） | [DBLP 2025](https://dblp.org/db/conf/refsq/refsq2025.html) | 2024-11-01 待补时刻 AoE | 2024-11-08 待补时刻 AoE | 2025-01-15 待补时刻 AoE | 2025-04-07..2025-04-10 | 待复核（official program / DBLP fallback） | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [REFSQ 2024](https://2024.refsq.org/) | [Research Track](https://2024.refsq.org/track/refsq-2024-papers) | [Important Dates](https://2024.refsq.org/dates/refsq-2024) | 待补（历史入口需复核） | [Program](https://2024.refsq.org/program/program-refsq-2024/) / [Research Track](https://2024.refsq.org/track/refsq-2024-papers) | 待补（Springer LNCS / LNBIP 卷号） | [DBLP 2024](https://dblp.org/db/conf/refsq/refsq2024.html) | 2023-11-03 待补时刻 AoE | 2023-11-10 待补时刻 AoE | 2024-01-15 待补时刻 AoE | 2024-04-08..2024-04-11 | 待复核（official program / DBLP fallback） | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [REFSQ 2023](https://2023.refsq.org/) | [Research Papers](https://2023.refsq.org/track/refsq-2023-papers) | [Important Dates](https://2023.refsq.org/dates/refsq-2023) | 待补（历史入口需复核） | [Program](https://2023.refsq.org/program/program-refsq-2023/) / [Research Papers](https://2023.refsq.org/track/refsq-2023-papers) | 待补（Springer LNCS / LNBIP 卷号） | [DBLP 2023](https://dblp.org/db/conf/refsq/refsq2023.html) | 2022-11-11 待补时刻 AoE | 2022-11-18 待补时刻 AoE | 2023-01-20 待补时刻 AoE | 2023-04-17..2023-04-20 | 待复核（official program / DBLP fallback） | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [REFSQ 2022](https://2022.refsq.org/) | [Research Papers](https://2022.refsq.org/track/refsq-2022-papers) | [Important Dates](https://2022.refsq.org/dates/refsq-2022) | 待补（历史入口需复核） | [Program](https://2022.refsq.org/program/program-refsq-2022/) / [Research Papers](https://2022.refsq.org/track/refsq-2022-papers) | 待补（Springer LNCS / LNBIP 卷号） | [DBLP 2022](https://dblp.org/db/conf/refsq/refsq2022.html) | 2021-10-25 待补时刻 AoE | 2021-11-01 待补时刻 AoE | 2021-12-20 待补时刻 AoE | 2022-03-21..2022-03-24 | 待复核（official program / DBLP fallback） | 🟡 部分核验 |

## 7. 维护备注

- REFSQ 虽在 scope 文件标为 P0-B，但 PR #41 计划纳入 PR-2；本轮只补充 REFSQ 目录事实，不改 [../01-venue-scope.md](../01-venue-scope.md)。
- REFSQ 年度页面使用独立子域 `yyyy.refsq.org`，researchr 系列导航、Springer proceedings、CEUR / DBLP 入口可能分散；不要把 DBLP 当官方 accepted/program，也不要把 LNCS proceedings 卷号未核准时写成既定事实。
- 2027 已有 official home / dates / organizing committee，submission system 未公布；2028 未发现官方主页或 dates。

## 8. TIMELINE.md 同步提示

- 本 venue 当前已记录的 dated events 已同步至 [TIMELINE.md](../TIMELINE.md)；后续新增或修正 important dates 时，必须同步更新对应年度 README 与 `TIMELINE.md` 的事件发生年份章节。
- 本目录不再保留 worker 事件草稿文件；事实源以各年度 README 的“重要时间点”表与 `TIMELINE.md` 为准。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:25:00` | 常态化刷新：2027 行 Submission system 由 `未公布` 升级为 [EasyChair `refsq2027`](https://easychair.org/conferences/?conf=refsq2027)；同轮在年度页闭合地点为 **Basel, Switzerland（FHNW Dreispitz Campus）**，并补入**首次采用双盲**的政策变更（官方逐字 `New this year: REFSQ 2027 will adopt a double-blind review process.`）与 special theme `Aligning RE and AI Velocity`。四个主轨日期逐字复核一致。 |
| `2026-07-13 10:27:51` | 常态化刷新 REFSQ 2026/2027：确认 2026 已结束，升级 2027 Research official dates；2028/2029+ 保守复查未见官方年度信息。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 13:16` | PR #35 近期窗口复审修复：修正 REFSQ 2027 Research Papers 官方 CFP 链接与根表入口，避免使用已 404 的旧 track slug。 |
| `2026-06-05 08:35` | 初始化 REFSQ 根 README，填充 2022-2028 年度核心链接、主要 deadline 草稿、核心人员情报与维护备注。 |
