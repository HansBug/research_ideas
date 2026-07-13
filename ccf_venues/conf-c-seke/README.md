# SEKE README

> 信息更新时间：`2026-07-13 10:27:51`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | SEKE |
| 全称 | International Conference on Software Engineering and Knowledge Engineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / P2 邻近观察 |
| CCF 等级 | 🥉 |
| 本库目录 | `conf-c-seke` |
| 出版方 | KSI Research / SEKE official pages |
| 官方 series page | [SEKE series](https://ksiresearch.org/seke/) |
| 官方当前 / 最新年度主页 | [SEKE 2026](https://ksiresearch.org/seke/seke26.html) |
| 官方 CFP / Important Dates 总入口 | [SEKE 2026 dates](https://ksiresearch.org/seke/seke26main.html) |
| 官方 proceedings / paper list 总入口 | [DBLP / proceedings fallback](https://dblp.org/db/conf/seke/index.html) |
| DBLP venue page | [DBLP SEKE index](https://dblp.org/db/conf/seke/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `Proceedings - SEKE 2012: 24th International Conference on Software Engineering and Knowledge Engineering`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

SEKE 连接 software engineering 与 knowledge engineering，覆盖 requirements、formal specification、knowledge-based systems、LLM / AI agent special sessions 等主题。本库将其作为 P2 邻近观察 venue，用于补充知识工程与软工交叉线索，不作为 P0/P1 主投目标。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 🟡 中：知识工程、需求、SE 方法可为 LLM 状态机建模提供邻近线索。 |
| P2 | 🟡 中 | 🟡 中：需求、知识建模、LLM reasoning special session 可补场景/性质生成素材。 |
| P3 | 🟡 中 | 🟡 中：formal specification / verification / model checking session 可补验证邻近入口。 |
| P4 | 🟡 中 | 🟡 中：software maintenance / testing / AI-based SE 论文需逐年筛选。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [SEKE series](https://ksiresearch.org/seke/) | 年度事实仍以年度主页 / CFP / committee 为准 | `2026-06-05 17:23` |
| Latest year homepage | [SEKE 2026](https://ksiresearch.org/seke/seke26.html) | 2027/2028 已于 2026-07-13 复查；未公布则保留占位 | `2026-07-13 10:27:51` |
| CFP / Important Dates | [SEKE 2026 dates](https://ksiresearch.org/seke/seke26main.html) | 历史年度在年度 README 展开 | `2026-06-05 17:23` |
| Submission system | [2026 submission](https://www.easychair.org/conferences/?conf=seke26) | 投稿系统可能按 track 拆分；年度页保留具体入口 | `2026-06-05 17:23` |
| Program / accepted papers | 未公布 | 已结束年度优先官方 program / accepted；缺失时用 DBLP fallback | `2026-06-05 17:23` |
| Proceedings | [Proceedings入口](http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2025_Proceedings.pdf) | 出版商 / proceedings DOI 优先；受限时记录 WAF / 已检索未获可审计证据 | `2026-06-05 17:23` |
| DBLP venue | [DBLP venue](https://dblp.org/db/conf/seke/index.html) | 仅作论文名录 / 计数 fallback | `2026-06-05 17:23` |

## 5. 核心人员情报

> 核心人员情报优先来自官方 organizing / committee / track 页面；研究方向和代表作入口来自个人主页、机构页、DBLP 或公开学术入口。P2 venue 的人员表只记录投稿分流和研究社区画像所需的代表性 leadership，不扩展为全量 PC roster。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Shi-Kuo Chang | 2022-2026 / Steering Committee Chair | Steering Committee Chair | University of Pittsburgh | [官方角色来源](https://ksiresearch.org/seke/seke26pc.html) | [学术入口](https://dblp.org/pid/c/ShiKuoChang.html) | knowledge engineering, visual languages, software engineering | [论文入口](https://dblp.org/pid/c/ShiKuoChang.html) | P1/P2：知识工程与模型表达 | 🟡 部分核验 | `2026-06-05 17:53` |
| ChingYee Suen | 2026 / General Chair | General Chair | Concordia University | [官方角色来源](https://ksiresearch.org/seke/seke26pc.html) | [学术入口](https://dblp.org/pid/33/4263.html) | pattern recognition / AI systems; SEKE role official | [论文入口](https://dblp.org/pid/33/4263.html) | P2：AI/knowledge engineering 邻近 | 🟡 部分核验 | `2026-06-05 17:53` |
| Angelo Perkusich | 2026 / Program Chair | Program Chair | Federal University of Campina Grande | [官方角色来源](https://ksiresearch.org/seke/seke26pc.html) | [学术入口](https://dblp.org/pid/64/1356.html) | software engineering, embedded systems, empirical SE | [论文入口](https://dblp.org/pid/64/1356.html) | P1/P2：软工方法与实证线索 | 🟡 部分核验 | `2026-06-05 17:53` |
| Stefano Cirillo | 2026 / Program Co-Chair | Program Co-Chair | University of Salerno | [官方角色来源](https://ksiresearch.org/seke/seke26pc.html) | [学术入口](https://dblp.org/pid/201/4222.html) | software engineering, code analysis, AI4SE | [论文入口](https://dblp.org/pid/201/4222.html) | P1/P4：程序理解 / 维护邻近 | 🟡 部分核验 | `2026-06-05 17:53` |
| Xinzhi Wang | 2026 / DMM special session organizer | DMM special session organizer | University of Pittsburgh / official DMM PDF | [官方角色来源](https://ksiresearch.org/seke/seke26proc/seke26DMM.pdf) | [学术入口](https://dblp.org/search?q=Xinzhi%20Wang) | LLM / AI agents special-session line; exact homepage待补 | [论文入口](https://dblp.org/search?q=Xinzhi%20Wang) | P1/P2：LLM / AI agents 与 knowledge-based SE | 🟡 部分核验 | `2026-06-05 17:53` |
| Loredana Caruccio | 2025 / General Chair; 2024 / Program Chair | General Chair; 2024 / Program Chair | University of Salerno | [官方角色来源](https://ksiresearch.org/seke/seke25pc.html) | [学术入口](https://dblp.org/pid/147/3302.html) | data quality, software engineering, information systems | [论文入口](https://dblp.org/pid/147/3302.html) | P2：数据质量与知识工程 | 🟡 部分核验 | `2026-06-05 17:53` |
| Pankaj Kamthan | 2025 Program Co-Chair; 2022 RE/Domain session chair | Program Co-Chair; RE/Domain session chair | Concordia University | [官方角色来源](https://ksiresearch.org/seke/seke25pc.html) | [学术入口](https://dblp.org/pid/k/PankajKamthan.html) | requirements engineering, software engineering education, domain engineering | [论文入口](https://dblp.org/pid/k/PankajKamthan.html) | P1/P2：需求工程和 domain engineering | 🟡 部分核验 | `2026-06-05 17:53` |
| Kazuhiro Ogata | 2022 Conference Chair; formal specification session chair | Conference Chair; formal specification session chair | JAIST | [官方角色来源](https://ksiresearch.org/seke/seke22pc.html) | [学术入口](https://dblp.org/pid/o/KazuhiroOgata.html) | formal methods, algebraic specification, model checking | [论文入口](https://dblp.org/pid/o/KazuhiroOgata.html) | P2/P3：形式化规约与模型检查 | 🟡 部分核验 | `2026-06-05 17:53` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟣 通知后 | [年度主页](https://ksiresearch.org/seke/seke26.html) | [CFP / track](https://ksiresearch.org/seke/seke26main.html) | [Dates](https://ksiresearch.org/seke/seke26main.html) | [Submission](https://www.easychair.org/conferences/?conf=seke26) | 未公布 | 未公布 | 未公布 | 未公布 | 2026-05-10 待补时刻 EST | 2026-06-20 待补时刻 | 2026-10-01..2026-10-02; 2026-10-04..2026-10-10 virtual | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [年度主页](https://ksiresearch.org/seke/seke25.html) | [CFP / track](https://ksiresearch.org/seke/seke25main.html) | [Dates](https://ksiresearch.org/seke/seke25main.html) | [Submission](https://www.easychair.org/conferences/?conf=seke25) | [Program / accepted](https://ksiresearch.org/seke/seke25pgm.html) | [Proceedings](http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2025_Proceedings.pdf) | [DBLP](https://dblp.org/db/conf/seke/seke2025.html) | 未公布 | 2025-05-15 | 2025-06-20 | 2025-09-29..2025-09-30; 2025-10-01..2025-10-06 virtual | DBLP fallback ≈63 paper entries + 1 volume record | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [年度主页](https://ksiresearch.org/seke/seke24.html) | [CFP / track](https://ksiresearch.org/seke/seke24main.html) | [Dates](https://ksiresearch.org/seke/seke24main.html) | [Submission](https://www.easychair.org/conferences/?conf=seke24) | 未公布 | [Proceedings](http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2024_Proceedings.pdf) | [DBLP](https://dblp.org/db/conf/seke/seke2024.html) | 未公布 | 2024-06-07 | 2024-07-20 | 2024-10-26..2024-10-28; 2024-10-29..2024-11-03 virtual | DBLP fallback ≈81 paper entries + 1 volume record | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [年度主页](https://ksiresearch.org/seke/seke23.html) | [CFP / track](https://ksiresearch.org/seke/seke23main.html) | [Dates](https://ksiresearch.org/seke/seke23main.html) | [Submission](https://www.easychair.org/conferences/?conf=seke23) | [Program / accepted](https://ksiresearch.org/seke/seke23pgm.html) | [Proceedings](http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2023_Proceedings.pdf) | [DBLP](https://dblp.org/db/conf/seke/seke2023.html) | 未公布 | 2023-03-15 | 2023-04-20 | 2023-07-01..2023-07-03; 2023-07-05..2023-07-10 virtual | DBLP fallback ≈124 paper entries + 1 volume record | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [年度主页](https://ksiresearch.org/seke/seke22.html) | [CFP / track](https://ksiresearch.org/seke/seke22main.html) | [Dates](https://ksiresearch.org/seke/seke22main.html) | [Submission](https://www.easychair.org/conferences/?conf=seke22) | [Program / accepted](https://ksiresearch.org/seke/seke22pgm.html) | [Proceedings](http://ksiresearchorg.ipage.com/seke/Proceedings/seke/SEKE2022_Proceedings.pdf) | [DBLP](https://dblp.org/db/conf/seke/seke2022.html) | 未公布 | 2022-03-15 | 2022-04-20 | 2022-07-01..2022-07-10 | DBLP fallback ≈117 paper entries + 1 volume record | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 本目录属于 PR-9 / P2 邻近观察，只服务于检索扩展、投稿分流和社区画像，不把 SEKE 升级为 P0/P1 主投目标。
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
| `2026-07-13 10:27:51` | 常态化刷新 SEKE 2026：确认 notification 已过，camera-ready / early registration 2026-07-20 仍待发生；2027/2028 保守复查未见官方年度信息。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 18:03` | 修复 PR-9 根 README 一致性：补回核心人员表 `单位` 列，并按 2026-06-05 当前阶段同步 2026 年度状态。 |
| `2026-06-05 17:23` | PR-9 初始化 SEKE P2 邻近观察 venue README，覆盖 2022--2028 年度索引、核心链接、人员情报、计数口径和待补记录。 |
