# ESEM README

> 信息更新时间：`2026-06-09 18:18:06`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ESEM |
| 全称 | International Symposium on Empirical Software Engineering and Measurement |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | 🥈 |
| 出版方 | ACM / IEEE / Dagstuhl LIPIcs（逐年度以官方页面为准；2026 官方说明转向 Dagstuhl LIPIcs / open by default） |
| 官方 series page | [researchr ESEM series](https://conf.researchr.org/series/esem) |
| 官方当前 / 最新年度主页 | [ESEIW 2026](https://conf.researchr.org/home/eseiw-2026) |
| 官方 CFP / Important Dates 总入口 | [ESEIW 2026 Important Dates](https://conf.researchr.org/dates/eseiw-2026) |
| 官方 proceedings / paper list 总入口 | 未提供跨年度统一入口；逐年度使用 official program / proceedings / [DBLP ESEM](https://dblp.org/db/conf/esem/) fallback |
| DBLP venue page | [DBLP ESEM](https://dblp.org/db/conf/esem/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `ESEM 2010 - Proceedings of the 2010 ACM-IEEE International Symposium on Empirical Software Engineering and Measurement`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

ESEM 是实证软件工程与度量核心会议，通常与 ESEIW 同周组织，覆盖 empirical study、measurement、benchmark、replication、open science、registered reports、industry / practice evidence、human / developer study、software analytics 与研究方法论。对本仓库而言，ESEM 不是状态机建模或形式化验证的专门 venue，而是 LLM4SE、LLM-as-Judge、状态机制品质量评估、baseline 对照、human / expert study、实验设计与可复现性论证的重要方法论支撑。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | 适合发表 LLM 生成状态机的实验评测、prompt / model / dataset 对比、公开证据评审一致性与误差分析。 |
| P2 场景与性质生成 | 中 | 可支撑 verification scenario / property generation 的实证评估、benchmark 设计与度量指标。 |
| P3 验证剖面与模型检查 | 中 | 可作为验证工具链实验设计、用户研究和可复现实验报告的投稿补链 venue。 |
| P4 模型修复 | 中 | 可支撑 repair loop 的 ablation、human-in-the-loop 评估、缺陷分类和修复成效度量。 |
| project_ex1 LLM-as-Judge | 高 | 评审 rubric、inter-rater reliability、noise floor、provider drift 和 judge validity 都需要 ESEM 风格的实证方法。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [researchr ESEM series](https://conf.researchr.org/series/esem) | ESEM 年度主页常以 ESEIW umbrella 形式发布 | `2026-06-05 17:23` |
| Latest year homepage | [ESEIW 2026](https://conf.researchr.org/home/eseiw-2026) | `home/esem-2026` 会跳转到 `home/eseiw-2026` | `2026-06-05 17:23` |
| CFP / Call for Papers | [ESEM - Technical Track 2026](https://conf.researchr.org/track/eseiw-2026/eseiw-2026-esem---technical-track) | 2022-2025 使用 `esem-YYYY` track URL；2026 使用 `eseiw-2026` track URL | `2026-06-05 17:23` |
| Important Dates | [ESEIW 2026 dates](https://conf.researchr.org/dates/eseiw-2026) | 2022-2025 使用 `dates/esem-YYYY` | `2026-06-05 17:23` |
| Submission system | [HotCRP esem26](https://esem26.hotcrp.com) | 2022-2025 历史投稿入口已在年度页记录为 EasyChair；归档登录状态仍未获公开可审计正文 | `2026-06-05 17:23` |
| Program / accepted papers | 逐年度 program 页面；当前最新已结束年度见 [ESEIW 2025 Program](https://conf.researchr.org/program/esem-2025/program-esem-2025/) | 已结束年度优先 official program；数量仍需 DBLP / proceedings 复核 | `2026-06-05 17:23` |
| Proceedings | [Dagstuhl LIPIcs FAQ 2026](https://conf.researchr.org/info/eseiw-2026/dagstuhl-lipics---faq-for-authors) / [Open Science Policy](https://conf.researchr.org/info/eseiw-2026/open-science-policy) | 2026 官方说明出版和开放科学口径发生变化；正式 proceedings 尚未公布 | `2026-06-05 17:23` |
| DBLP venue | [DBLP ESEM](https://dblp.org/db/conf/esem/) | 仅作论文名录 / 计数 fallback；2026 DBLP 年度页未公开 | `2026-06-05 17:23` |

## 5. 核心人员情报

> 人员角色以 researchr 官方 committee / track committee 页面为准；研究方向和代表作入口为基于 DBLP / 公开主页的归纳，不代表会议官方评价。本节只保留 chair、track chair、ISERN / open science / PC 代表人物和与本仓库评测方法强相关的领域权威，不展开全量 PC。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Daniel Mendez | 2026 / ESEIW；2023 / ESEM | 2026 General Co-Chair；2023 Open Science | Blekinge Institute of Technology and fortiss | [2026 General organization](https://conf.researchr.org/committee/eseiw-2026/esem-2026-general-organization)；[2023 Organizing Committee](https://conf.researchr.org/committee/esem-2023/esem-2023-organizing-committee) | [DBLP search](https://dblp.org/search?q=Daniel%20Mendez) | empirical SE、requirements engineering、open science、research methodology | DBLP search 作为近年论文入口 | P1/P2/ex1 高：需求与实证评估方法、open science policy 可支撑论文实验设计 | 🟡 部分核验 | `2026-06-05 17:23` |
| Stefan Wagner | 2026 / ESEIW | General Co-Chair | Technical University of Munich | [2026 General organization](https://conf.researchr.org/committee/eseiw-2026/esem-2026-general-organization) | [DBLP search](https://dblp.org/search?q=Stefan%20Wagner%20software%20engineering) | software quality、empirical SE、software analytics、AI for SE | DBLP search 作为近年论文入口 | P1/P4/ex1 高：质量评估、缺陷 / 质量度量和实验设计 | 🟡 部分核验 | `2026-06-05 17:23` |
| Robert Feldt | 2026 / ESEM Technical Track | PC Chair | Chalmers / University of Gothenburg | [2026 Technical Track contact](https://conf.researchr.org/committee/eseiw-2026/eseiw-2026-esem---technical-track-contact) | [DBLP search](https://dblp.org/search?q=Robert%20Feldt) | empirical SE、testing、search-based SE、AI / ML for SE、human factors | DBLP search 作为近年论文入口 | P2/P3/P4/ex1 高：测试生成、评测方法、AI4SE 实证 | 🟡 部分核验 | `2026-06-05 17:23` |
| Maria Paasivaara | 2026 / ESEM Technical Track；2025 / ISERN | 2026 PC Chair；2025 ISERN Chair | LUT University / Aalto University | [2026 Technical Track contact](https://conf.researchr.org/committee/eseiw-2026/eseiw-2026-esem---technical-track-contact)；[2025 Organizing Committee](https://conf.researchr.org/committee/esem-2025/esem-2025-organizing-committee) | [DBLP search](https://dblp.org/search?q=Maria%20Paasivaara) | global software engineering、agile / team studies、empirical methods | DBLP search 作为近年论文入口 | ex1/P1 中高：human evaluation、team / expert study 和 qualitative analysis 方法 | 🟡 部分核验 | `2026-06-05 17:23` |
| Valentina Lenarduzzi | 2025 / ESEM | Program Chair / Technical Track Chair | University of Oulu | [2025 Organizing Committee](https://conf.researchr.org/committee/esem-2025/esem-2025-organizing-committee)；[2025 Technical Track contacts](https://conf.researchr.org/committee/esem-2025/esem-2025-technical-track-contacts) | [DBLP search](https://dblp.org/search?q=Valentina%20Lenarduzzi) | software quality、technical debt、empirical SE、software analytics | DBLP search 作为近年论文入口 | P1/P4/ex1 高：质量维度、技术债和 empirical evaluation 设计 | 🟡 部分核验 | `2026-06-05 17:23` |
| Fabio Q. B. da Silva | 2025 / ESEM；2023 / Registered Reports | Program Chair / Technical Track Chair；Registered Reports Chair | Federal University of Pernambuco | [2025 Organizing Committee](https://conf.researchr.org/committee/esem-2025/esem-2025-organizing-committee)；[2025 Technical Track contacts](https://conf.researchr.org/committee/esem-2025/esem-2025-technical-track-contacts)；[2023 Organizing Committee](https://conf.researchr.org/committee/esem-2023/esem-2023-organizing-committee) | [DBLP search](https://dblp.org/search?q=Fabio%20Q.%20B.%20da%20Silva) | empirical SE、research methods、software engineering education / practice | DBLP search 作为近年论文入口 | ex1/P1 高：registered reports、评测有效性与实证研究设计 | 🟡 部分核验 | `2026-06-05 17:23` |
| Xavier Franch | 2024 / ESEIW；2026 / ESEM Technical PC | General Chair；Technical Track PC member | Universitat Politècnica de Catalunya | [2024 Organizing Committee](https://conf.researchr.org/committee/esem-2024/esem-2024-organizing-committee)；[2026 Technical Track contact](https://conf.researchr.org/committee/eseiw-2026/eseiw-2026-esem---technical-track-contact) | [DBLP search](https://dblp.org/search?q=Xavier%20Franch) | requirements engineering、software architecture、quality models、empirical SE | DBLP search 作为近年论文入口 | P1/P2 高：需求、质量模型与评估指标体系 | 🟡 部分核验 | `2026-06-05 17:23` |
| Per Runeson | 2023 / ESEM；2025 / Technical PC | Program Co-Chair；Technical Track PC member | Lund University | [2023 Organizing Committee](https://conf.researchr.org/committee/esem-2023/esem-2023-organizing-committee)；[2025 Technical Track contacts](https://conf.researchr.org/committee/esem-2025/esem-2025-technical-track-contacts) | [DBLP search](https://dblp.org/search?q=Per%20Runeson) | empirical SE、case study methodology、software testing / quality、open source studies | DBLP search 作为近年论文入口 | ex1/P1/P4 高：case study 方法、实证设计与结果有效性论证 | 🟡 部分核验 | `2026-06-05 17:23` |

## 6. 年度信息汇总

年度汇总表按年份降序排列。官方仅给日期而未核实具体时刻的 deadline 统一写作 `待补时刻`；ESEM 技术主 track 与 Emerging Results、Registered Reports、SEIP / IGC、Journal First、IDoESE、ISERN 等 track 不混入同一论文数量口径。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟡 审稿中 | [ESEIW 2026](https://conf.researchr.org/home/eseiw-2026) | [ESEM - Technical Track](https://conf.researchr.org/track/eseiw-2026/eseiw-2026-esem---technical-track) | [Important Dates](https://conf.researchr.org/dates/eseiw-2026) | [HotCRP esem26](https://esem26.hotcrp.com) | 未公布 | [Dagstuhl LIPIcs FAQ](https://conf.researchr.org/info/eseiw-2026/dagstuhl-lipics---faq-for-authors) / [Open Science Policy](https://conf.researchr.org/info/eseiw-2026/open-science-policy)（论文集未公布） | ⏳ 已检索未公布 | 2026-05-11 待补时刻 | 2026-05-18 待补时刻 | 2026-07-10 待补时刻 | 2026-10-04..2026-10-09 | 未最终公布 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [ESEIW 2025](https://conf.researchr.org/home/esem-2025) | [ESEM - Technical Track](https://conf.researchr.org/track/esem-2025/esem-2025-technical-track) | [Important Dates](https://conf.researchr.org/dates/esem-2025) | [EasyChair esem25](https://easychair.org/conferences/?conf=esem25) | [Program](https://conf.researchr.org/program/esem-2025/program-esem-2025/) | 待补（DBLP 年度页作论文名录 fallback） | [DBLP ESEM 2025](https://dblp.org/db/conf/esem/esem2025.html) | 2025-04-18 待补时刻 | 2025-04-25 待补时刻 | 2025-06-16 待补时刻 | 2025-09-28..2025-10-03 | DBLP 年度页已定位；数量待复核 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [ESEIW 2024](https://conf.researchr.org/home/esem-2024) | [ESEM Technical Papers](https://conf.researchr.org/track/esem-2024/esem-2024-technical-track) | [Important Dates](https://conf.researchr.org/dates/esem-2024) | [EasyChair esem24](https://easychair.org/conferences/?conf=esem24) | [Program](https://conf.researchr.org/program/esem-2024/program-esem-2024/) | 待补（DBLP 年度页作论文名录 fallback） | [DBLP ESEM 2024](https://dblp.org/db/conf/esem/esem2024.html) | 2024-05-02 待补时刻 | 2024-05-06 待补时刻 | 2024-06-20 待补时刻 | 2024-10-20..2024-10-25 | DBLP 年度页已定位；数量待复核 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ESEIW 2023](https://conf.researchr.org/home/esem-2023) | [ESEM Technical Papers](https://conf.researchr.org/track/esem-2023/esem-2023-technical-track) | [Important Dates](https://conf.researchr.org/dates/esem-2023) | [EasyChair esem2023](https://easychair.org/my/conference?conf=esem2023) | [Program](https://conf.researchr.org/program/esem-2023/program-esem-2023/) | 待补（DBLP 年度页作论文名录 fallback） | [DBLP ESEM 2023](https://dblp.org/db/conf/esem/esem2023.html) | 2023-04-24 待补时刻 | 2023-05-02 待补时刻 | 2023-06-16 待补时刻 | 2023-10-22..2023-10-27 | DBLP 年度页已定位；数量待复核 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ESEIW 2022](https://conf.researchr.org/home/esem-2022) | [ESEM Technical Papers](https://conf.researchr.org/track/esem-2022/esem-2022-technical-track) | [Important Dates](https://conf.researchr.org/dates/esem-2022) | [EasyChair esem22](https://easychair.org/my/conference?conf=esem22) | [Program](https://conf.researchr.org/program/esem-2022/program-esem-2022/) | [ACM DL proceedings](https://dl.acm.org/doi/proceedings/10.1145/3544902) / [DBLP fallback](https://dblp.org/db/conf/esem/esem2022.html) | [DBLP ESEM 2022](https://dblp.org/db/conf/esem/esem2022.html) | 2022-04-25 待补时刻 | 2022-05-02 待补时刻 | 2022-06-17 待补时刻 | 2022-09-18..2022-09-23（ESEM 2022-09-22..2022-09-23） | DBLP 年度页已定位；数量待复核 | 🟡 部分核验 |

## 7. 维护备注

- 2026：researchr 年度页采用 `eseiw-2026` slug；`esem-2026` URL 会重定向。官方公布 ESEIW Munich 会期为 `2026-10-04..2026-10-09`，Technical Track abstract / submission / notification / camera-ready 分别为 `2026-05-11`、`2026-05-18`、`2026-07-10`、`2026-08-17`；投稿系统为 [HotCRP esem26](https://esem26.hotcrp.com)；Technical Track 明确 double-anonymous review、open by default，并说明 selected strong papers 可被邀请扩展投稿到 Empirical Software Engineering special issue。
- 2025-2022：使用 researchr 年度主页、Important Dates 与 DBLP 年度页作为基础入口；论文数量待后续逐年计数复核，统一标注为“DBLP 年度页已定位；数量待复核”。
- 2027 / 2028：已检索 researchr `home` / `dates` 的 `esem` 与 `eseiw` slug，均未公布；本目录显式写 `⏳ 已检索未公布`，不伪造 deadline 或地点。
- 2022-2026 ESEM Technical Track dated events 已同步到 [../TIMELINE.md](../TIMELINE.md) 的全局时间线与 Mermaid。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 2022-2026 abstract / submission / notification / camera-ready / conference dates 已补入 [../TIMELINE.md](../TIMELINE.md) 对应事件发生年份章节与 Mermaid Gantt。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 17:23` | 初始化 ESEM 根 README，填充 2022-2028 年度核心链接、Technical Track dates、2026 LIPIcs / HotCRP 信息、核心人员情报与待补风险。 |
