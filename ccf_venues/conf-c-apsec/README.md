# APSEC README

> 信息更新时间：`2026-08-07 20:15:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | APSEC |
| 全称 | Asia-Pacific Software Engineering Conference |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / P2 邻近观察 |
| CCF 等级 | 🥉 |
| 本库目录 | `conf-c-apsec` |
| 出版方 | IEEE / APSEC official researchr pages |
| 官方 series page | [APSEC series](https://conf.researchr.org/series/apsec) |
| 官方当前 / 最新年度主页 | [APSEC 2026](https://conf.researchr.org/home/apsec-2026) |
| 官方 CFP / Important Dates 总入口 | [APSEC 2026 dates](https://conf.researchr.org/dates/apsec-2026) |
| 官方 proceedings / paper list 总入口 | [DBLP / proceedings fallback](https://dblp.org/db/conf/apsec/) |
| DBLP venue page | [DBLP APSEC index](https://dblp.org/db/conf/apsec/) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `Proceedings - 1998 Asia Pacific Software Engineering Conference, APSEC 1998`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

APSEC 是亚太软件工程综合会议，覆盖 empirical / automated / AI-intensive software engineering、程序修复、测试、需求、软件工程实践等主题。本库将其作为 P2 邻近观察 venue，用于扩展区域性 SE、LLM4SE 和工程实践线索，不作为 P0/P1 主投目标。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 🟡 中：区域性 SE / AI-intensive software engineering 可提供需求到模型、LLM4SE 辅助建模线索。 |
| P2 | 🟡 中 | 🟡 中：需求、测试、实证、软件工程实践可为验证场景 / 性质生成提供邻近样本。 |
| P3 | 🟡 中 | 🟡 中：模型检查、formal specification、runtime/monitoring 论文偶有出现，需按年度筛选。 |
| P4 | 🟡 中 | 🟡 中：自动程序修复、defect analysis、maintenance 论文可作为修复相关观察。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [APSEC series](https://conf.researchr.org/series/apsec) | 年度事实仍以年度主页 / CFP / committee 为准 | `2026-06-05 17:23` |
| Latest year homepage | [APSEC 2026](https://conf.researchr.org/home/apsec-2026) | 2026 Technical Track dates 已复查；2027/2028 未发现官方主页 / CFP / dates | `2026-07-13 19:11:00` |
| CFP / Important Dates | [APSEC 2026 dates](https://conf.researchr.org/dates/apsec-2026) | 2026 Technical Track 更新为 optional abstract 2026-07-13、full paper 2026-07-20、notification 2026-09-14、camera-ready 2026-10-19；时区 UTC+8 (Bali time) | `2026-07-13 19:11:00` |
| Submission system | [2026 submission](https://easychair.org/conferences/?conf=apsec2026) | 投稿系统可能按 track 拆分；年度页保留具体入口 | `2026-06-05 17:23` |
| Program / accepted papers | [2026 program](https://conf.researchr.org/program/apsec-2026/program-apsec-2026/) | 已结束年度优先官方 program / accepted；缺失时用 DBLP fallback | `2026-06-05 17:23` |
| Proceedings | 未公布 | 出版商 / proceedings DOI 优先；受限时记录 WAF / 已检索未获可审计证据 | `2026-06-05 17:23` |
| DBLP venue | [DBLP venue](https://dblp.org/db/conf/apsec/) | 仅作论文名录 / 计数 fallback | `2026-06-05 17:23` |

## 5. 核心人员情报

> 核心人员情报优先来自官方 organizing / committee / track 页面；研究方向和代表作入口来自个人主页、机构页、DBLP 或公开学术入口。P2 venue 的人员表只记录投稿分流和研究社区画像所需的代表性 leadership，不扩展为全量 PC roster。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| M. Ali Fauzi | 2026 / General Co-Chair | General Co-Chair | Brawijaya University | [官方角色来源](https://conf.researchr.org/committee/apsec-2026/apsec-2026-organizing-committee) | [学术入口](https://dblp.org/search?q=M.%20Ali%20Fauzi) | software engineering / AI-intensive systems line (role official; research direction via public scholarly index) | [论文入口](https://dblp.org/search?q=M.%20Ali%20Fauzi) | P1/P2：区域性 SE 与 AI-intensive software engineering 入口 | 🟡 部分核验 | `2026-06-05 17:53` |
| Rekyan Regasari Mardi Putri | 2026 / General Co-Chair | General Co-Chair | Brawijaya University | [官方角色来源](https://conf.researchr.org/committee/apsec-2026/apsec-2026-organizing-committee) | [学术入口](https://dblp.org/search?q=Rekyan%20Regasari%20Mardi%20Putri) | software engineering / information systems line (待进一步个人主页核验) | [论文入口](https://dblp.org/search?q=Rekyan%20Regasari%20Mardi%20Putri) | P1/P2：区域性 SE 组织线索 | 🟡 部分核验 | `2026-06-05 17:53` |
| In-Young Ko | 2026 / Program Co-Chair; Steering Chair | Program Co-Chair; Steering Chair | KAIST | [官方角色来源](https://conf.researchr.org/committee/apsec-2026/apsec-2026-organizing-committee) | [学术入口](https://dblp.org/pid/50/1039.html) | software engineering, services, IoT / pervasive systems | [论文入口](https://dblp.org/pid/50/1039.html) | P1/P2：AI/IoT-intensive software 与服务系统建模 | 🟡 部分核验 | `2026-06-05 17:53` |
| Bayu Priyambadha | 2026 / Program Co-Chair | Program Co-Chair | Brawijaya University | [官方角色来源](https://conf.researchr.org/committee/apsec-2026/apsec-2026-organizing-committee) | [学术入口](https://dblp.org/search?q=Bayu%20Priyambadha) | software engineering / SE education / empirical line (待补个人主页) | [论文入口](https://dblp.org/search?q=Bayu%20Priyambadha) | P1/P2：软件工程教育与实证邻近线索 | 🟡 部分核验 | `2026-06-05 17:53` |
| Jacky Keung | 2025 / Program Co-Chair | Program Co-Chair | City University of Hong Kong | [官方角色来源](https://conf.researchr.org/committee/apsec-2025/apsec-2025-organizing-committee) | [学术入口](https://dblp.org/pid/09/5201.html) | empirical software engineering, effort estimation, software analytics | [论文入口](https://dblp.org/pid/09/5201.html) | P2/P4：实证评估、维护与质量数据 | 🟡 部分核验 | `2026-06-05 17:53` |
| Eunjong Choi | 2025 / Program Co-Chair | Program Co-Chair | Kyoto Institute of Technology | [官方角色来源](https://conf.researchr.org/committee/apsec-2025/apsec-2025-organizing-committee) | [学术入口](https://dblp.org/pid/87/6892.html) | software testing, program analysis, automated repair | [论文入口](https://dblp.org/pid/87/6892.html) | P3/P4：测试、分析与修复 | 🟡 部分核验 | `2026-06-05 17:53` |
| Jun Sun | 2024 / Program Chair | Program Chair | Singapore Management University | [官方角色来源](https://conf.researchr.org/committee/apsec-2024/apsec-2024-organizing-committee) | [学术入口](https://dblp.org/pid/75/1386.html) | formal methods, model checking, software verification | [论文入口](https://dblp.org/pid/75/1386.html) | P2/P3：模型检查与验证 | 🟡 部分核验 | `2026-06-05 17:53` |
| Yunja Choi | 2023 / Program Co-Chair; 2022 Program Co-Chair | Program Co-Chair; 2022 Program Co-Chair | Kyungpook National University | [官方角色来源](https://conf.researchr.org/committee/apsec-2023/apsec-2023-organizing-committee) | [学术入口](https://dblp.org/pid/68/575.html) | software testing, verification, model-based testing | [论文入口](https://dblp.org/pid/68/575.html) | P2/P3：测试与验证场景 | 🟡 部分核验 | `2026-06-05 17:53` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟡 已截稿 / 审稿中 | [年度主页](https://conf.researchr.org/home/apsec-2026) | [CFP / track](https://conf.researchr.org/track/apsec-2026/apsec-2026-technical-track) | [Dates](https://conf.researchr.org/dates/apsec-2026) | [Submission](https://easychair.org/conferences/?conf=apsec2026) | [Program / accepted](https://conf.researchr.org/program/apsec-2026/program-apsec-2026/) | 未公布 | 未公布 | 2026-07-13 待补时刻 UTC+8 (Bali time) | 2026-07-20 待补时刻 UTC+8 (Bali time) | 2026-09-14 待补时刻 UTC+8 (Bali time) | 2026-12-07..2026-12-10 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/apsec-2025) | [CFP / track](https://conf.researchr.org/track/apsec-2025/apsec-2025-papers) | [Dates](https://conf.researchr.org/dates/apsec-2025) | [Submission](https://apsec25.hotcrp.com) | [Program / accepted](https://conf.researchr.org/program/apsec-2025/program-apsec-2025/) | 未公布 | [DBLP](https://dblp.org/db/conf/apsec/apsec2025.html) | 2025-07-13 | 2025-07-20 | 2025-09-20 | 2025-12-02..2025-12-05 | DBLP fallback `inproceedings`=117；IEEE proceedings URL 待补 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/apsec-2024) | [CFP / track](https://conf.researchr.org/track/apsec-2024/apsec-2024-technical-track) | [Dates](https://conf.researchr.org/dates/apsec-2024) | [Submission](https://easychair.org/conferences/?conf=apsec2024) | [Program / accepted](https://conf.researchr.org/program/apsec-2024/program-apsec-2024/) | 未公布 | [DBLP](https://dblp.org/db/conf/apsec/apsec2024.html) | 2024-07-13 | 2024-07-20 | 2024-09-13 | 2024-12-03..2024-12-06 | DBLP fallback `inproceedings`=68；IEEE proceedings URL 待补 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/apsec-2023) | [CFP / track](https://conf.researchr.org/track/apsec-2023/apsec-2023-technical-track) | [Dates](https://conf.researchr.org/dates/apsec-2023) | [Submission](https://easychair.org/conferences/?conf=apsec2023) | [Program / accepted](https://conf.researchr.org/program/apsec-2023/program-apsec-2023/) | [Proceedings](https://ieeexplore.ieee.org/xpl/conhome/1000681/all-proceedings) | [DBLP](https://dblp.org/db/conf/apsec/apsec2023.html) | 2023-07-07 | 2023-07-14 | 2023-08-23 | 2023-12-04..2023-12-07 | DBLP fallback `inproceedings`=90；IEEE Xplore CLI 418 已检索未获可审计证据 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [年度主页](https://conf.researchr.org/home/apsec-2022) | [CFP / track](https://conf.researchr.org/track/apsec-2022/apsec-2022-technical-track) | [Dates](https://conf.researchr.org/dates/apsec-2022) | [Submission](https://easychair.org/my/conference?conf=apsec2022) | [Program / accepted](https://conf.researchr.org/program/apsec-2022/program-apsec-2022/) | 未公布 | [DBLP](https://dblp.org/db/conf/apsec/apsec2022.html) | 2022-07-13 | 2022-07-20 | 2022-08-25 | 2022-12-06..2022-12-09 | 官方主页列 Technical 42 / SEIP 5 / ERA 14 / EDU 5 / posters 20；DBLP fallback `inproceedings`=83 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 本目录属于 PR-9 / P2 邻近观察，只服务于检索扩展、投稿分流和社区画像，不把 APSEC 升级为 P0/P1 主投目标。
- 论文数量优先使用官方 accepted / proceedings；DBLP 只作 fallback，且不得写成 main / research track count。
- Research、industry、tool、artifact、workshop、special session、virtual / live segment 必须分开记录，不能混算。
- 2027/2028 已于 2026-07-13 复查；未公布年度保留占位，不预造 deadline / committee / proceedings。
- 2026-07-13 复核：APSEC 2026 Technical Track dates 页当前列 optional abstract `2026-07-13`、full paper `2026-07-20`、author notification `2026-09-14`、camera-ready `2026-10-19`，technical chain 时区为 `UTC+8 (Bali time)`；ERA / SEIP / tutorials 等其他 track 不作为本轮当前投稿机会。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的年度表格与 Mermaid Gantt。
- 会议 `Conference dates` 也必须进入 TIMELINE 表格和 Mermaid；无日期或未公布事项不得进入 dated Mermaid。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:15:00` | 常态化刷新：2026 行阶段由 `🟢 投稿中` 迁移为 `🟡 已截稿 / 审稿中`（full paper `2026-07-20` 已过、未再延期）。⚠️ 同轮修正 Technical Track 时区口径：官方 dates 页 6 行 tooltip 与 CFP 小标题当前均为 `AoE (Anywhere on Earth)`，本库此前记的 `UTC+8 (Bali time)` 相差 20 小时，已按官方现状改回并保留冲突历史。**P2 邻近观察，不升级为 P0/P1 主线。** |
| `2026-07-13 19:11:00` | 常态化刷新：按官方 APSEC 2026 dates 更新 Technical Track optional abstract 2026-07-13、full paper 2026-07-20、notification 2026-09-14、camera-ready 2026-10-19，保留 UTC+8 (Bali time)；复查 2027/2028 未公布。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 13:16` | PR #35 近期窗口复审修复：确认 APSEC 2026 Technical Track 官方 dates tooltip 为 UTC+8 (Bali time)，同时补充 companion tracks 异构时区 caveat。 |
| `2026-06-06 00:04` | PR-10 复核 APSEC 2026 Technical Track timezone：technical chain 使用 UTC+8 (Bali time)，不写 AoE；ERA/SEIP 等其他 track 另行分列。 |
| `2026-06-05 18:40` | 修复实现后复审 M3：同步年度页 P3 相关性口径，明确 APSEC 对验证剖面 / 模型检查工具链的邻近参考定位。 |
| `2026-06-05 18:03` | 修复 PR-9 根 README 一致性：补回核心人员表 `单位` 列，并按 2026-06-05 当前阶段同步 2026 年度状态。 |
| `2026-06-05 17:23` | PR-9 初始化 APSEC P2 邻近观察 venue README，覆盖 2022--2028 年度索引、核心链接、人员情报、计数口径和待补记录。 |
