# SANER README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | SANER |
| 全称 | IEEE International Conference on Software Analysis, Evolution and Reengineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| CCF 等级 | B（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版方 | IEEE / IEEE Computer Society |
| 官方 series page | [researchr SANER series](https://conf.researchr.org/series/saner)；[DBLP SANER index](https://dblp.org/db/conf/saner/index) |
| 官方当前 / 最新年度主页 | [SANER 2027](https://conf.researchr.org/home/saner-2027) |
| 官方 CFP / Important Dates 总入口 | 逐年度维护；当前最新可核验入口见 §6 年度信息汇总 |
| 官方 proceedings / paper list 总入口 | 逐年度使用 official program / publisher / DBLP fallback |
| DBLP venue page | [DBLP SANER](https://dblp.org/db/conf/saner/index) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现可核验官方年度页 / CFP / important dates |

### 1.1 索引与分区信息

> 本节在 PR #91 中从 PR #90 占位推进为“证据链优先”的真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🟡 | 沿用本库 CCF B 级；官方目录入口已定位，单条目仍需浏览器行级复核 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本 PR 不重新定义 CCF scope，只保留可点击官方基线入口 | `2026-06-09 13:52` |
| WoS / CPCI | ⏳ | 待人工核验 CPCI / proceedings 收录；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate Master Journal List](https://mjl.clarivate.com/search-results) 为官方入口；本轮未取得可审计单会议 CPCI-S / CPCI-SSH 行级结果，后续需按年度 proceedings / ISBN / publisher 卷次复核 | `2026-06-09 13:52` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本地 snapshot `compendex_source_list_2026-06-09.xlsx`，sheet `NON-SERIALS`，代表行 Source title `Proceedings - 2023 IEEE International Conference on Software Analysis, Evolution and Reengineering, SANER 2023`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用，EI 已有官方 source-list 级证据或线索；WoS / CPCI 仍待人工核验 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；后续 reviewer 需复核本节链接与 source-list 字段 | `2026-06-09 13:52` |

## 2. Scope 与方向

SANER 面向软件分析、逆向工程、演化、维护、重构、程序理解、软件质量与再工程，是 P4“已知缺陷驱动的迭代式模型修复”最直接的 CCF B 维护 / 修复 venue 之一。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中 | 中：从程序理解、维护历史、工件分析中抽取结构化上下文，可辅助需求 / 代码 / 模型到状态机的建模。 |
| P2 场景与性质生成 | 中 | 中：缺陷报告、回归测试、维护历史和负结果可作为场景与性质生成线索。 |
| P3 验证剖面与模型检查 | 中 | 中：工具、trace、profile、reproducibility 和质量证据可为验证剖面提供经验输入。 |
| P4 模型修复 | 高 | 高：维护、演化、重构、程序理解和过程改进与迭代式模型修复闭环直接相关。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [researchr SANER series](https://conf.researchr.org/series/saner)；[DBLP SANER index](https://dblp.org/db/conf/saner/index) | 年度独立站点 / researchr / 官方组织站点并行 | `2026-06-05 17:35` |
| Latest year homepage | [SANER 2027](https://conf.researchr.org/home/saner-2027) | 未公布年度写 `⏳ 已检索未公布` | `2026-06-05 17:35` |
| CFP / Call for Papers | 见 §6 年度信息汇总 | track 分散时在年度 README 展开 | `2026-06-05 17:35` |
| Important Dates | 见 §6 年度信息汇总 | researchr dates / official CFP 优先 | `2026-06-05 17:35` |
| Submission system | 见 §6 年度信息汇总 | 历史系统可能失效，失效时保留待复核 | `2026-06-05 17:35` |
| Program / accepted papers | 见 §6 年度信息汇总 | 已结束年度优先 official program / accepted papers | `2026-06-05 17:35` |
| Proceedings | 见 §6 年度信息汇总 | publisher proceedings 优先，DBLP 仅作 fallback | `2026-06-05 17:35` |
| DBLP venue | [DBLP SANER](https://dblp.org/db/conf/saner/index) | 仅作论文名录 / 计数 fallback | `2026-06-05 17:35` |

## 5. 核心人员情报

本节记录当前 / 未来年度核心组织者、Program / Research Track chair、Steering / track chair 与强相关领域权威，不展开全量 PC。人员研究方向基于 official profile / DBLP / 个人主页归纳；若角色来源不是同一官方 committee 页，已在 `核验状态` 中显式降级。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Rodrigo Spinola | 2027 / conference | General Co-Chair | VCU | [SANER 2027 organizing committee](https://conf.researchr.org/committee/saner-2027/saner-2027-organizing-committee) | [DBLP search](https://dblp.org/search?q=Rodrigo%20Spinola) | software engineering、empirical / industrial SE（待 DBLP 精查） | DBLP / official profile 待补具体代表作 | P4 中：维护 / 演化 venue 治理与工业化视角 | 🟡 部分核验 | `2026-06-05 17:35` |
| Kostadin Damevski | 2027 / conference | General Co-Chair | VCU | [SANER 2027 organizing committee](https://conf.researchr.org/committee/saner-2027/saner-2027-organizing-committee) | [DBLP search](https://dblp.org/search?q=Kostadin%20Damevski) | software engineering、code analysis、maintenance（公开资料推断） | DBLP / profile 待补具体代表作 | P4 强：代码演化、维护与问题定位邻近 | 🟡 部分核验 | `2026-06-05 17:35` |
| Yuanfang Cai | 2027 / research track | Program Co-Chair | Drexel University | [SANER 2027 organizing committee](https://conf.researchr.org/committee/saner-2027/saner-2027-organizing-committee) | [DBLP](https://dblp.org/search?q=Yuanfang%20Cai) | software design、architecture、modularity、technical debt | DBLP recent publications | P4 强：架构级缺陷、技术债和修复影响分析 | 🟡 部分核验 | `2026-06-05 17:35` |
| Denys Poshyvanyk | 2027 / research track | Program Co-Chair | William & Mary | [SANER 2027 organizing committee](https://conf.researchr.org/committee/saner-2027/saner-2027-organizing-committee) | [DBLP](https://dblp.org/search?q=Denys%20Poshyvanyk) | software maintenance、program comprehension、MSR、reverse engineering | DBLP recent publications | P1/P4 强：程序理解、维护和修复证据链 | 🟡 部分核验 | `2026-06-05 17:35` |
| Fabio Palomba | 2027 / MIP | MIP Award Co-Chair | University of Salerno | [SANER 2027 organizing committee](https://conf.researchr.org/committee/saner-2027/saner-2027-organizing-committee) | [researchr profile](https://conf.researchr.org/profile/conf/fabiopalomba1) | software maintenance and evolution、empirical SE、source code quality、MSR | profile / DBLP recent papers | P4 强：维护、重构、代码质量和修复评价 | 🟡 部分核验 | `2026-06-05 17:35` |

## 6. 年度信息汇总

年度汇总表按年份降序排列。已结束年度的论文数量若来自 DBLP，均标注为 fallback，不等同于 Research Track / main track 精确计数；multi-track、companion、workshop、journal-first、tool、industry 均不得混算。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟢 投稿中 | [SANER 2027](https://conf.researchr.org/home/saner-2027) | [Research Track](https://conf.researchr.org/track/saner-2027/saner-2027-papers) | [Important Dates](https://conf.researchr.org/dates/saner-2027) | 未公布 | [Research Track](https://conf.researchr.org/track/saner-2027/saner-2027-papers) | 未公布 | ⏳ 已检索未公布 | 2026-09-21 待补时刻 AoE / UTC-12h | 2026-09-25 待补时刻 AoE / UTC-12h | 2026-12-01 待补时刻 AoE / UTC-12h | 2027-03-09..2027-03-12 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | ✅ 已结束 / 待 proceedings | [SANER 2026](https://conf.researchr.org/home/saner-2026) | [Research Track](https://conf.researchr.org/track/saner-2026/saner-2026-papers) | [Important Dates](https://conf.researchr.org/dates/saner-2026) | 未公布 | [Program](https://conf.researchr.org/program/saner-2026/program-saner-2026/) / [Research Track](https://conf.researchr.org/track/saner-2026/saner-2026-papers) | 未公布 | [DBLP SANER index](https://dblp.org/db/conf/saner/index) | 2025-10-09 待补时刻 | 2025-10-16 待补时刻 | 2025-12-09 待补时刻 | 2026-03-17..2026-03-20 | 未公布 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [SANER 2025](https://conf.researchr.org/home/saner-2025) | [Important Dates](https://conf.researchr.org/dates/saner-2025) | [Important Dates](https://conf.researchr.org/dates/saner-2025) | 未公布 | [Program](https://conf.researchr.org/program/saner-2025/program-saner-2025/) | [DBLP 2025](https://dblp.org/db/conf/saner/saner2025.html) | [DBLP 2025](https://dblp.org/db/conf/saner/saner2025.html) | 2024-10-04 待补时刻 | 2024-10-13 待补时刻 | 2024-11-29 待补时刻 | 2025-03-04..2025-03-07 | 89（DBLP inproceedings fallback；track 拆分待复核） | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [SANER 2024](https://conf.researchr.org/home/saner-2024) | [Important Dates](https://conf.researchr.org/dates/saner-2024) | [Important Dates](https://conf.researchr.org/dates/saner-2024) | 未公布 | [Research Papers](https://conf.researchr.org/track/saner-2024/saner-2024-papers) / [Program](https://conf.researchr.org/program/saner-2024/program-saner-2024/) | [DBLP 2024](https://dblp.org/db/conf/wcre/saner2024) / [Companion](https://dblp.org/db/conf/wcre/saner2024c) | [DBLP 2024](https://dblp.org/db/conf/wcre/saner2024) | 2023-10-13 待补时刻 | 2023-10-29 待补时刻 | 2023-12-15 待补时刻 | 2024-03-12..2024-03-15 | 105（DBLP inproceedings fallback；companion 分卷另计） | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [SANER 2023](https://saner2023.must.edu.mo/) | [EasyChair CFP](https://easychair.org/cfp/SANER_2023) | [EasyChair CFP](https://easychair.org/cfp/SANER_2023) | [EasyChair](https://easychair.org/conferences/?conf=saner2023) | [Program Overview](https://saner2023.must.edu.mo/programOverview) | [IEEE proceedings](https://ieeexplore.ieee.org/xpl/conhome/10123438/proceeding) | [DBLP 2023](https://dblp.org/db/conf/wcre/saner2023) | 2022-10-14 待补时刻 | 2022-10-21 待补时刻 | 2022-12-16 待补时刻 | 2023-03-21..2023-03-24 | 109（DBLP inproceedings fallback；track 拆分待复核） | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [SANER 2022](http://saner2022.uom.gr/) | 待补（未恢复官方 CFP；第三方 deadline 仅作线索） | 待补（未恢复官方 dates） | 待补 | [IEEE proceedings](https://ieeexplore.ieee.org/xpl/conhome/9825713/proceeding) | [IEEE proceedings](https://ieeexplore.ieee.org/xpl/conhome/9825713/proceeding) | [DBLP 2022](https://dblp.org/db/conf/wcre/saner2022) | 待补（第三方线索为 2021-10-14） | 待补（第三方线索为 2021-10-21） | 待补 | 2022-03-15..2022-03-18 | 144（DBLP inproceedings fallback；workshop/companion 待拆） | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、industry、tool、journal-first、registered report、artifact、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 均已做公开入口检索；2027 Research Track dates 页已标注 AoE / UTC-12h，未公布年度保留占位与核查记录，不预设 CFP。SANER 2022 HTTPS 证书主机名不匹配，当前年度页使用 HTTP 官方站入口。
- 本 venue 的 dated events 已按事件发生年份同步到 [../TIMELINE.md](../TIMELINE.md)；后续修改 deadline 必须同步更新年度 README、根表与 Mermaid。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [../TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [../TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 00:41` | PR-10 实现后 review 修复：同步 SANER 2027 Research Track AoE / UTC-12h 时区到根表与维护备注。 |
| `2026-06-05 18:13` | PR-6 收尾复核：修正 SANER 2022 官方站为 HTTP 可访问入口，并显式记录 HTTPS 证书主机名不匹配风险。 |
| `2026-06-05 17:35` | PR-6 初始化 SANER venue 根 README，新增 2022-2028 年度索引、核心 URL、核心人员情报、计数口径与待补记录。 |
