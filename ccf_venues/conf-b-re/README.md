# RE README

> 信息更新时间：`2026-07-13 13:30:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | RE |
| 全称 | IEEE International Requirements Engineering Conference |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | 🥈 |
| 出版方 | IEEE / IEEE Computer Society |
| 官方 series page | [researchr RE series](https://conf.researchr.org/series/RE) |
| 官方当前 / 最新年度主页 | [RE 2026](https://conf.researchr.org/home/RE-2026) |
| 官方 CFP / Important Dates 总入口 | [Important Dates](https://conf.researchr.org/dates/RE-2026) |
| 官方 proceedings / paper list 总入口 | 未提供跨年度统一入口；逐年度使用 official program / publisher / DBLP fallback |
| DBLP venue page | [DBLP RE](https://dblp.org/db/conf/re/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `2014 IEEE 22nd International Requirements Engineering Conference, RE 2014 - Proceedings`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

RE 是需求工程领域核心会议，覆盖 elicitation、analysis、prioritization、documentation、validation、evolution、maintenance、management、traceability、NLP/ML for RE、legal / privacy requirements、industrial RE 和 artifact / open science。对本仓库而言，RE 是 P1/P2 的最核心 venue：既提供需求到模型的上游理论与数据，也提供验证场景 / 性质生成所需的 requirements quality、acceptance criteria、constraints 与 traceability 线索。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | 需求抽取、需求质量、NLP for RE、requirements-to-model 是 LLM 状态机建模的上游核心。 |
| P2 场景与性质生成 | 高 | requirements validation、acceptance criteria、constraint / property mining 可直接支撑验证场景与性质生成。 |
| P3 验证剖面与模型检查 | 中 | formal requirements、safety / compliance requirements 与 CPS requirements 可补充模型检查目标。 |
| P4 模型修复 | 中 | requirements evolution、change impact 与 inconsistency management 可为缺陷定位和修复提供上游依据。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [researchr RE series](https://conf.researchr.org/series/RE) | researchr / 年度独立站点为主 | `2026-06-05 08:35` |
| Latest year homepage | [RE 2026](https://conf.researchr.org/home/RE-2026) | 2027/2028 复查仍未公布；未来年度无官网时写 `⏳ 已检索未公布` | `2026-07-13 13:30` |
| CFP / Call for Papers | [Research Papers](https://conf.researchr.org/track/RE-2026/RE-2026-Research-Papers) | 年度 CFP 分散在 track 页面；2026 camera-ready 已过 | `2026-07-13 13:30` |
| Important Dates | [Important Dates](https://conf.researchr.org/dates/RE-2026) | 可与 CFP 同页；会期 `2026-08-17..2026-08-21` | `2026-07-13 13:30` |
| Submission system | [Research track submission](https://easychair.org/conferences/?conf=re26) | 历史年度入口需逐年复核 | `2026-06-05 08:35` |
| Program / accepted papers | [Accepted Papers](https://conf.researchr.org/track/RE-2026/RE-2026-Research-Papers) | 已结束年度优先官方 program / accepted papers | `2026-06-05 08:35` |
| Proceedings | IEEE Xplore 待补 conference number | DBLP 仅作论文名录 / 计数 fallback | `2026-06-05 08:35` |
| DBLP venue | [DBLP RE](https://dblp.org/db/conf/re/) | 仅作论文名录 / 计数 fallback | `2026-06-05 08:35` |

## 5. 核心人员情报

> 人员角色以官方 organizing / track committee 页面为准；学术入口优先个人主页、机构页与 DBLP。当前初版不展开全量 PC，只保留 chair、track chair、steering / 领域权威线索。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Travis Breaux | 2026 / conference | General Chair | Carnegie Mellon University | [RE 2026 organizing committee](https://conf.researchr.org/committee/RE-2026/RE-2026-organizing-committee) | [CMU faculty page](https://www.cs.cmu.edu/~breaux/) / [DBLP search](https://dblp.org/search?q=Travis%20Breaux) | requirements engineering、privacy / legal requirements、policy compliance | DBLP / personal page 作为近年论文入口；需后续补具体 2022-2026 代表作 | P1/P2 高：需求抽取、合规需求、自然语言需求分析 | 🟡 部分核验 | `2026-06-05 08:35` |
| Sepideh Ghanavati | 2026 / research track | Program Co-Chair | University of Maine | [RE 2026 organizing committee](https://conf.researchr.org/committee/RE-2026/RE-2026-organizing-committee) | [DBLP search](https://dblp.org/search?q=Sepideh%20Ghanavati) | privacy / security requirements、requirements compliance、NLP for RE | DBLP search 作为近年论文入口；具体代表作待补 | P1/P2 高：需求质量、合规和约束抽取 | 🟡 部分核验 | `2026-06-05 08:35` |
| Andreas Vogelsang | 2026 / research track | Program Co-Chair | University of Duisburg-Essen / paluno | [RE 2026 organizing committee](https://conf.researchr.org/committee/RE-2026/RE-2026-organizing-committee) | [DBLP](https://dblp.org/pid/146/2074.html) | requirements engineering、ML / AI requirements、automotive / CPS requirements | [DBLP recent publications](https://dblp.org/pid/146/2074.html) | P1/P2/P3 高：控制系统需求、AI 辅助需求工程、验证场景 | 🟢 已核验入口 | `2026-06-05 08:35` |
| Daniel Amyot | 2026 / conference | New Faculty Symposium Co-Chair；RE 领域权威 | University of Ottawa | [RE 2026 organizing committee](https://conf.researchr.org/committee/RE-2026/RE-2026-organizing-committee) | [DBLP](https://dblp.org/pid/a/DanielAmyot.html) | goal-oriented requirements、URN / GRL、model-based RE | [DBLP recent publications](https://dblp.org/pid/a/DanielAmyot.html) | P1/P2 高：goal / scenario / model-oriented RE 可支撑需求到状态机建模 | 🟢 已核验入口 | `2026-06-05 08:35` |
| Tanmay Bhowmik | 2026 / conference | Tutorial Co-Chair | TCS Research | [RE 2026 organizing committee](https://conf.researchr.org/committee/RE-2026/RE-2026-organizing-committee) | [DBLP search](https://dblp.org/search?q=Tanmay%20Bhowmik) | requirements engineering in industry、software analytics | DBLP search 作为近年论文入口；具体代表作待补 | P1/P2 中：工业需求质量与数据集线索 | 🟡 部分核验 | `2026-06-05 08:35` |

## 6. 年度信息汇总

年度汇总表按年份降序排列。官方仅给日期而未核实具体时刻的 deadline 统一写作 `待补时刻 AoE`；Research / main track 数量不得混入 Industry、RE@Next、artifact、poster / tool 等其他 track。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🔵 会期临近 | [RE 2026](https://conf.researchr.org/home/RE-2026) | [Research Papers](https://conf.researchr.org/track/RE-2026/RE-2026-Research-Papers) | [Important Dates](https://conf.researchr.org/dates/RE-2026) | [Research track submission](https://easychair.org/conferences/?conf=re26) | [Accepted Papers](https://conf.researchr.org/track/RE-2026/RE-2026-Research-Papers) | 未公布 | ⏳ 已检索未公布 | 2026-02-16 待补时刻 AoE | 2026-02-23 待补时刻 AoE | 2026-05-08 待补时刻 AoE | 2026-08-17..2026-08-21 | 未最终公布 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [RE 2025](https://conf.researchr.org/home/RE-2025) | [Research Papers](https://conf.researchr.org/track/RE-2025/RE-2025-research-papers) | [Important Dates](https://conf.researchr.org/dates/RE-2025) | 待补（官方页面曾提供 track submission；历史入口需复核） | [Program](https://conf.researchr.org/program/RE-2025/program-RE-2025/) / [Research Papers](https://conf.researchr.org/track/RE-2025/RE-2025-research-papers) | 待补（IEEE Xplore 需补 conference number） | [DBLP 2025](https://dblp.org/db/conf/re/re2025.html) | 2025-03-03 待补时刻 AoE | 2025-03-10 待补时刻 AoE | 2025-05-23 待补时刻 AoE | 2025-09-01..2025-09-05 | 待复核（Research track 与其他 track 分开） | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [RE 2024](https://conf.researchr.org/home/RE-2024) | [Research Papers](https://conf.researchr.org/track/RE-2024/RE-2024-research-papers) | [Important Dates](https://conf.researchr.org/dates/RE-2024) | 待补（历史入口需复核） | [Program](https://conf.researchr.org/program/RE-2024/program-RE-2024/) / [Research Papers](https://conf.researchr.org/track/RE-2024/RE-2024-research-papers) | 待补（IEEE Xplore 需补 conference number） | [DBLP 2024](https://dblp.org/db/conf/re/re2024.html) | 2024-01-19 待补时刻 AoE | 2024-01-26 待补时刻 AoE | 2024-03-22 待补时刻 AoE | 2024-06-24..2024-06-28 | 待复核（Research track 与其他 track 分开） | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [RE 2023](https://conf.researchr.org/home/RE-2023) | [Research Papers](https://conf.researchr.org/track/RE-2023/RE-2023-research-papers) | [Important Dates](https://conf.researchr.org/dates/RE-2023) | 待补（历史入口需复核） | [Program](https://conf.researchr.org/program/RE-2023/program-RE-2023/) / [Research Papers](https://conf.researchr.org/track/RE-2023/RE-2023-research-papers) | 待补（IEEE Xplore 需补 conference number） | [DBLP 2023](https://dblp.org/db/conf/re/re2023.html) | 2023-03-10 待补时刻 AoE | 2023-03-17 待补时刻 AoE | 2023-05-30 待补时刻 AoE | 2023-09-04..2023-09-08 | 待复核（Research track 与其他 track 分开） | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [RE 2022](https://conf.researchr.org/home/RE-2022) | [Research Papers](https://conf.researchr.org/track/RE-2022/RE-2022-research-papers) | [Important Dates](https://conf.researchr.org/dates/RE-2022) | 待补（历史入口需复核） | [Program](https://conf.researchr.org/program/RE-2022/program-RE-2022/) / [Research Papers](https://conf.researchr.org/track/RE-2022/RE-2022-research-papers) | 待补（IEEE Xplore 需补 conference number） | [DBLP 2022](https://dblp.org/db/conf/re/re2022.html) | 2022-02-17 待补时刻 AoE | 2022-02-24 待补时刻 AoE | 2022-05-09 待补时刻 AoE | 2022-08-15..2022-08-20 | 待复核（Research track 与其他 track 分开） | 🟡 部分核验 |

## 7. 维护备注

- RE 2026 official dates 页面混有 Research、Industry、RE@Next、Artifacts、Workshop 等多类事件；本目录只抽取 Research Papers 的 abstract / full paper / notification / camera-ready。`2026-07-13` 复查时 Research Papers camera-ready `2026-06-08` 已过，会期 `2026-08-17..2026-08-21` 尚未开始，阶段为 `🔵 会期临近`。
- 2027 / 2028 在 researchr 探测 `home/RE-2027`、`home/RE-2028` 均为 404；`2026-07-13` 复查仍未公布，按 `⏳ 已检索未公布` 处理。
- 已结束年度 proceedings 的 IEEE Xplore conference number 未在 45 分钟窗口内稳定核准，因此 publisher proceedings 暂写待补；DBLP 仅作 fallback，不能与 official accepted papers 混作 Research Track count。

## 8. TIMELINE.md 同步提示

- 本 venue 当前已记录的 dated events 已同步至 [TIMELINE.md](../TIMELINE.md)；后续新增或修正 important dates 时，必须同步更新对应年度 README 与 `TIMELINE.md` 的事件发生年份章节。
- 本目录不再保留 worker 事件草稿文件；事实源以各年度 README 的“重要时间点”表与 `TIMELINE.md` 为准。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-07-13 13:30:00` | 常态化刷新 RE：确认 2026 Research Papers camera-ready 已过、会期 `2026-08-17..2026-08-21` 未开始，阶段改为会期临近；复查 2027/2028 仍未公布。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 08:35` | 初始化 RE 根 README，填充 2022-2028 年度核心链接、主要 deadline 草稿、核心人员情报与维护备注。 |
