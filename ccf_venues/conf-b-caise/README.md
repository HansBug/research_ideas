# CAiSE README

> 信息更新时间：`2026-08-07 20:25:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | CAiSE |
| 全称 | International Conference on Advanced Information Systems Engineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录入口](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；CLI 可能触发 WAF，正文未获公开可审计正文） |
| CCF 等级 | 🥈 |
| 出版方 | Springer LNCS（主会）；Forum / DC / Workshop 可能为 Springer / CEUR 等独立卷 |
| 官方 series page | [CAiSE long-term site](https://caise-conference.diag.uniroma1.it/) |
| 官方当前 / 最新年度主页 | [CAiSE 2027 Seville announcement](https://caise-conference.diag.uniroma1.it/) |
| 官方 CFP / Important Dates 总入口 | [CAiSE 2026 full papers CFP](https://caise26.polimi.it/?page_id=60) / [CAiSE 2026 dates](https://caise26.polimi.it/?page_id=60) |
| 官方 proceedings / paper list 总入口 | [Accepted papers](https://caise26.polimi.it/?page_id=948) / [Final program](https://caise26.polimi.it/?page_id=1122) / [LNCS 16558 / Part I](https://link.springer.com/book/10.1007/978-3-032-28110-4) / [LNCS 16559 / Part II](https://link.springer.com/book/10.1007/978-3-032-28117-3) |
| DBLP venue page | [DBLP CAiSE](https://dblp.org/db/conf/caise/) |
| 当前默认调查范围 | `2022` 至 `2028`；未公布未来年度不预造 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟡 | 仅确认 CAiSE 常见 Springer LNCS / LNBIP 出版路径与相关 book-series 在 Compendex source list 中；未取得 CAiSE 直接会议行 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），只记录 book-series / publisher-path discovery 线索，不得冒充会议 source-level | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 Compendex source-list 字段、book-series 线索和缩写碰撞规则完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:45` |

## 2. Scope 与方向

CAiSE 聚焦 Advanced Information Systems Engineering，覆盖 requirements engineering、conceptual modeling、ontology / enterprise modeling、business process modeling、process mining / monitoring、low-code / no-code、method engineering、compliance、quality of IS models、knowledge graphs、CPS / IoT / service / cloud / edge information systems 等方向。

本库将 CAiSE 作为 LLM4Modeling 的信息系统 / 概念建模 / MDE 分流 venue，不把它描述成泛 SE 主战场。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中高 | 适合需求到模型、概念/领域/企业模型、LLM-assisted modeling、模型质量评估；普通 prompt 工具评测不宜强投。 |
| P2 场景与性质生成 | 中 | 适合 requirements / constraints / compliance / process / IS model 语境下的场景与性质生成。 |
| P3 验证剖面与模型检查 | 中低到中 | 需要包装为 IS/CPS/enterprise/process model 的 engineering profile 或 compliance / quality analysis；纯 model checking 技术优先其他 venue。 |
| P4 模型修复 | 中 | 适合 model quality、consistency、evolution、alignment、repair in IS modeling / MDE context。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [CAiSE long-term site](https://caise-conference.diag.uniroma1.it/) | 当前官方 long-term series 入口可访问 | `2026-07-13 19:13:21` |
| Latest year homepage | [CAiSE 2027 Seville announcement](https://caise-conference.diag.uniroma1.it/) | CAiSE long-term site announces 2027 Seville `2027-06-07..2027-06-11` but no public CFP / dates page yet; 官方 long-term site 可访问 | `2026-07-13 19:13:21` |
| CFP / Call for Papers | [CAiSE 2026 full papers CFP](https://caise26.polimi.it/?page_id=60) | 2027 CFP / dates 未公布；2026 已结束，历史 CFP 仅作归档 | `2026-07-13 19:13:21` |
| Important Dates | [CAiSE 2026 dates](https://caise26.polimi.it/?page_id=60) | 2027 仅公告会期；无 CFP / submission / notification dates | `2026-07-13 19:13:21` |
| Submission system | [EasyChair CAiSE 2026](https://easychair.org/my/conference?conf=caise2026) | 只能证明投稿入口，不替代 CFP / dates | `2026-06-07 12:47` |
| Program / accepted papers | [Accepted papers](https://caise26.polimi.it/?page_id=948) / [Final program](https://caise26.polimi.it/?page_id=1122) | 已结束年度优先 official accepted/program | `2026-06-07 12:47` |
| Proceedings | [LNCS 16558 / Part I](https://link.springer.com/book/10.1007/978-3-032-28110-4) / [LNCS 16559 / Part II](https://link.springer.com/book/10.1007/978-3-032-28117-3) | 两卷共 46 篇 main conference full papers；DBLP fallback 分开 | `2026-07-13 19:13:21` |
| DBLP venue | [DBLP CAiSE](https://dblp.org/db/conf/caise/) | 仅作论文名录 / 计数 fallback | `2026-06-07 12:47` |

## 5. 核心人员情报

> 人员角色以年度 official committee / editorial pages 为准；DBLP / 个人主页只补研究方向与代表作。不要把 invited speaker、guest editor 或普通 PC member 升级为 chair / steering。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Carlo Combi | 2026 / conference | General Chair | University of Verona | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Carlo%20Combi) | temporal / process / information systems、healthcare IS | [DBLP 近年论文入口](https://dblp.org/search?q=Carlo%20Combi) | P2/P3：时间约束、流程与 IS 验证语境 | 🟡 部分核验 | `2026-06-07 12:47` |
| Hajo Reijers | 2026 / conference | General Chair | Utrecht University | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Hajo%20Reijers) | business process management、process redesign / mining | [DBLP 近年论文入口](https://dblp.org/search?q=Hajo%20Reijers) | P1/P2/P3：过程模型、场景与流程分析 | 🟡 部分核验 | `2026-06-07 12:47` |
| Lidia Fuentes | 2026 / program | Program Co-Chair | University of Málaga | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Lidia%20Fuentes) | software architecture、MDE、variability、self-adaptive systems | [DBLP 近年论文入口](https://dblp.org/search?q=Lidia%20Fuentes) | P1/P4：MDE / architecture / variability 与模型修复 | 🟡 部分核验 | `2026-06-07 12:47` |
| Pierluigi Plebani | 2026 / program | Program Co-Chair | Politecnico di Milano | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Pierluigi%20Plebani) | information systems、services、process / data management | [DBLP 近年论文入口](https://dblp.org/search?q=Pierluigi%20Plebani) | P1/P2：IS modeling 与 service/process requirements | 🟡 部分核验 | `2026-06-07 12:47` |
| John Krogstie | 2025 / program + steering | PC Chair / Steering Chair | NTNU | [CAiSE 2025 committee](https://conferences.big.tuwien.ac.at/caise2025/committee.php) | [DBLP](https://dblp.org/search?q=John%20Krogstie) | conceptual modeling、enterprise modeling、quality of models | [DBLP 近年论文入口](https://dblp.org/search?q=John%20Krogstie) | P1/ex1：模型质量与评审标准 | 🟡 部分核验 | `2026-06-07 12:47` |
| Gerti Kappel | 2025 / conference | General Chair | TU Wien | [CAiSE 2025 committee](https://conferences.big.tuwien.ac.at/caise2025/committee.php) | [DBLP](https://dblp.org/search?q=Gerti%20Kappel) | model engineering、web engineering、conceptual modeling | [DBLP 近年论文入口](https://dblp.org/search?q=Gerti%20Kappel) | P1/P4：MDE / conceptual modeling | 🟡 部分核验 | `2026-06-07 12:47` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | Camera-ready | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟦 已有主页 / 会期 | [CAiSE 2027 Seville announcement](https://caise-conference.diag.uniroma1.it/) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 2027-06-07..2027-06-11 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | ✅ 已结束 | [CAiSE 2026](https://caise26.polimi.it/) | [Full papers CFP](https://caise26.polimi.it/?page_id=60) | [CFP / dates](https://caise26.polimi.it/?page_id=60) | [EasyChair CAiSE 2026](https://easychair.org/my/conference?conf=caise2026) | [Accepted papers](https://caise26.polimi.it/?page_id=948) / [Final program](https://caise26.polimi.it/?page_id=1122) | [LNCS 16558 / Part I](https://link.springer.com/book/10.1007/978-3-032-28110-4) / [LNCS 16559 / Part II](https://link.springer.com/book/10.1007/978-3-032-28117-3) | [Part I](https://dblp.org/db/conf/caise/caise2026-1.html) / [Part II](https://dblp.org/db/conf/caise/caise2026-2.html) | 2025-11-21 待补时刻 AoE | 2025-11-28 待补时刻 AoE | 2026-02-12 待补时刻 | 待补 | 2026-06-08..2026-06-12 | main conference full papers: 46（official × publisher × DBLP 三方闭合） | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [CAiSE 2025](https://conferences.big.tuwien.ac.at/caise2025/) | [Full papers CFP](https://conferences.big.tuwien.ac.at/caise2025/cfp_full.php) | [CFP / dates](https://conferences.big.tuwien.ac.at/caise2025/cfp_full.php) | [EasyChair CAiSE 2025](https://easychair.org/my/conference?conf=caise2025) | [Accepted papers](https://conferences.big.tuwien.ac.at/caise2025/accepted_papers.php?type=Main%20Conference) | [Proceedings page](https://conferences.big.tuwien.ac.at/caise2025/proceedings.php) / [Vol.1](https://link.springer.com/book/10.1007/978-3-031-94569-4) / [Vol.2](https://link.springer.com/book/10.1007/978-3-031-94571-7) | ⏳ 已检索未公布 | 2024-11-22 待补时刻 | 2024-12-01 待补时刻 | 2025-02-28 待补时刻 | 2025-04-14 待补时刻 | 2025-06-16..2025-06-20 | 待按 main conference / LNCS 主卷复核 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 / 归档待补 | 待补（官方年度站当前未定位到可访问归档） | 待补 | 待补 | 待补 | 待补 | [DBLP / Springer proceedings record](https://dblp.org/db/conf/caise/caise2024.html) | [DBLP CAiSE 2024](https://dblp.org/db/conf/caise/caise2024.html) | 待补 | 待补 | 待补 | 待补 | 2024-06-03..2024-06-07（DBLP proceedings record） | DBLP 可计数；待 main conference 口径复核 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [CAiSE 2023](https://caise23.svit.usj.es/) | [Main conference](https://caise23.svit.usj.es/main-conference/) | [Main conference dates](https://caise23.svit.usj.es/main-conference/) | 待补（官方按钮 / EasyChair 历史入口需复核） | [Accepted papers](https://caise23.svit.usj.es/accepted-papers/) / [Program](https://caise23.svit.usj.es/program/) | [Proceedings](https://caise23.svit.usj.es/proceedings/) | [DBLP CAiSE 2023](https://dblp.org/db/conf/caise/caise2023.html) | 2022-11-22 待补时刻 | 2022-11-29 待补时刻 | 2023-03-01 待补时刻 | 2023-04-03 待补时刻 AoE | 2023-06-12..2023-06-16 | DBLP 可计数；待 main conference 口径复核 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [CAiSE 2022](https://caise22.ugent.be/) | [Calls](https://caise22.ugent.be/calls/) | [Homepage / calls key dates](https://caise22.ugent.be/) | 待补 | [Accepted papers](https://caise22.ugent.be/accepted-papers/) / [Program](https://caise22.ugent.be/program/) | [Proceedings](https://caise22.ugent.be/proceedings/) | [DBLP CAiSE 2022](https://dblp.org/db/conf/caise/caise2022.html) | 2021-11-22 待补时刻 | 2021-11-29 待补时刻 | 2022-03-01 待补时刻 | 2022-03-28 待补时刻 | 2022-06-06..2022-06-10 | DBLP 可计数；待 main conference 口径复核 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- CAiSE 主会计数只算 main conference / LNCS main proceedings；Forum、Doctoral Consortium、Journal First、RPE、Workshops、BPMDS、EMMSAD 不混入主会数量。
- 2024 official annual site 当前未定位到可访问归档；只用 DBLP / Springer proceedings record 落会期和 proceedings 线索，不补写 CFP / deadline。
- CAiSE 2026 已于 `2026-06-12` 结束；Springer 两卷主会 proceedings 已发布，后续只补 DBLP 年度页与 publisher / DBLP 计数交叉核验，不再作为当前投稿机会。
- CAiSE 2027 已有 Seville `2027-06-07..2027-06-11` 官方公告，但截至 2026-07-13 未公布 CFP、submission、notification 或 camera-ready dates。
- CAiSE 2028 未公布，不预造 homepage、committee、CFP、submission system 或 DBLP 年度页。

## 8. 证据与核查记录

| 类型 | 链接 | 核查时间 | 结论 |
|---|---|---|---|
| CCF official entry | [CCF TCSE_SS_PDL](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) | `2026-06-07 12:47` | 官方入口已定位；CLI 可能触发 WAF / 动态页，正文与第七版状态未获公开可审计正文。 |
| 非官方 CCF 镜像线索 | [ccf.atom.im](https://ccf.atom.im/) | `2026-06-07 12:47` | 仅作机器检索 / 差集筛查线索，不作为 CCF 官方事实。 |
| Official annual pages | [CAiSE 2026](https://caise26.polimi.it/) / [CAiSE 2025](https://conferences.big.tuwien.ac.at/caise2025/) / [CAiSE 2023](https://caise23.svit.usj.es/) / [CAiSE 2022](https://caise22.ugent.be/) | `2026-06-07 12:47` | 2022/2023/2025/2026 年度官方站与 main conference chain 已定位。 |
| 2024 fallback | [DBLP CAiSE 2024](https://dblp.org/db/conf/caise/caise2024.html) | `2026-06-07 12:47` | 仅支撑 proceedings record / 会期；2024 official CFP / dates / submission 仍待补。 |
| DBLP fallback | [DBLP CAiSE](https://dblp.org/db/conf/caise/) | `2026-06-07 12:47` | 仅作 bibliographic fallback；主会、Forum、DC、Workshop 需分口径计数。 |

## 9. TIMELINE.md 同步提示

- 本 venue 已核验 dated events 已同步至 [../TIMELINE.md](../TIMELINE.md) 对应年份表格与 PR #63 Mermaid 分片。
- 未公布年度、第三方线索、WAF / 404 / CAPTCHA 候选页不得进入 dated TIMELINE / Mermaid。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:25:00` | 常态化刷新：2026 行补入已上线的 DBLP 年度页（[Part I](https://dblp.org/db/conf/caise/caise2026-1.html) 22 条 + [Part II](https://dblp.org/db/conf/caise/caise2026-2.html) 24 条），与官方 accepted 页 46 篇、Springer LNCS 两卷完全吻合，计数口径升级为 **official × publisher × DBLP 三方闭合**。 |
| `2026-07-13 19:13:21` | 常态化刷新：将 CAiSE 2026 标记为已结束并补入 LNCS 16558 + 16559 共 46 篇主会 full papers；升级 CAiSE 2027 Seville `2027-06-07..2027-06-11` 占位但不伪造 CFP / dates；2028 仍未公布。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-07 13:33` | 修复实现后 review：补入 CAiSE 2023 official camera-ready `2023-04-03` AoE 并同步 TIMELINE。 |
| `2026-06-07 12:47` | PR #63 初始化 CAiSE 情报，补充 CCF / official / DBLP 证据、2022--2028 年度索引、核心人员、TIMELINE 同步和待补口径。 |
