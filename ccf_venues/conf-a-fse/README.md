# FSE README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | FSE |
| 全称 | ACM International Conference on the Foundations of Software Engineering（2024 起主名称）；历史年度常写 ESEC/FSE |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | A |
| 出版方 | ACM / PACMSE |
| 官方 series page | [FSE series](https://conf.researchr.org/series/fse) |
| 官方当前 / 最新年度主页 | [FSE 2027](https://conf.researchr.org/home/fse-2027)；[FSE 2028](https://conf.researchr.org/home/fse-2028) 当前 404 |
| 官方 CFP / Important Dates 总入口 | 逐年度 Research Papers track 维护 |
| 官方 proceedings / paper list 总入口 | 逐年度 program / proceedings；2024+ Research Papers 说明 PACMSE issue 是主 proceedings 口径 |
| DBLP venue page | [DBLP SIGSOFT/FSE venue](https://dblp.org/db/conf/sigsoft/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🏆 | CCF A 级；emoji 已按 GUIDE 的 A/B/C 口径编码，不再统一写成黄色 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `ESEC/FSE 2018 - Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

- FSE 是软件工程旗舰会议，覆盖软件工程基础、方法、工具、实证与产业实践。
- 与本仓库最相关的方向：AI/LLM for SE、软件建模与规格、测试与分析、软件维护、程序修复、开源科学与 artifact。
- 明显不属于本仓库重点但仍可作背景：教育、会议组织、泛人因与社区议题。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | 可追踪需求到模型、LLM 辅助建模、软件设计与工具论文。 |
| P2 场景与性质生成 | 高 | 可追踪测试生成、规格挖掘、属性 / oracle 生成与评估论文。 |
| P3 验证剖面与模型检查 | 中 | FSE 有程序分析、验证与可靠性论文，但不如 CAV/TACAS 聚焦形式化。 |
| P4 模型修复 | 高 | 自动修复、调试、缺陷定位和 LLM repair 是 FSE 常见主题。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [FSE series](https://conf.researchr.org/series/fse) | researchr 长期入口 | `2026-06-05 08:39` |
| Latest year homepage | [FSE 2027](https://conf.researchr.org/home/fse-2027) | 2028 未公布；2027 已有地点与会期 | `2026-06-05 08:39` |
| CFP / Call for Papers | [FSE 2027 Research Papers](https://conf.researchr.org/track/fse-2027/fse-2027-papers) | 2027 track 已公布；submission site 将临近 deadline 发布 | `2026-06-06 11:46` |
| Important Dates | [FSE 2027 dates](https://conf.researchr.org/dates/fse-2027) | 年度主页侧栏也列出 Research Papers 日期；AoE / UTC-12h | `2026-06-06 11:46` |
| Submission system | 待公布 | FSE 2027 track 说明 submission site 将在临近 deadline 时发布；历年入口见年度页 | `2026-06-06 11:46` |
| Program / accepted papers | [FSE 2026 Program](https://conf.researchr.org/program/fse-2026/program-fse-2026/) | 已结束年度优先官方 program，DBLP fallback | `2026-06-05 08:39` |
| Proceedings | [FSE 2025 proceedings](https://conf.researchr.org/info/fse-2025/proceedings) | 2024+ 注意 PACMSE issue 关系 | `2026-06-05 08:39` |
| DBLP venue | [DBLP SIGSOFT/FSE venue](https://dblp.org/db/conf/sigsoft/) | 仅作论文名录 / 计数 fallback | `2026-06-05 08:39` |

## 5. 核心人员情报

> 人员角色以 FSE 官方年度 organizing / research papers / steering 入口为准；研究方向和代表作基于个人主页、DBLP 或公开学术入口归纳。本表优先记录 General Chair、Research/Program Chair、与 P1-P4 强相关的 track chair / committee 成员和领域权威；不等同于全量 PC roster。

| 人员 | 年度 / 层级 | 会议角色 | 单位 / 主页入口 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Foutse Khomh | FSE 2026 | General Co-Chair | Polytechnique Montréal / 待补 | [FSE 2026 Organizing Committee](https://conf.researchr.org/committee/fse-2026/fse-2026-organizing-committee) | [DBLP](https://dblp.org/pid/21/7138) | ML / AI software engineering, software quality, empirical SE | DBLP 近年论文入口；代表作待逐篇筛选 | P1/P2/P4 高相关：ML-enabled systems 与质量评估 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Shin Hwei Tan | FSE 2026 | General Co-Chair | Southern University of Science and Technology / 待补 | [FSE 2026 Organizing Committee](https://conf.researchr.org/committee/fse-2026/fse-2026-organizing-committee) | [DBLP](https://dblp.org/pid/26/9450) | program repair, software testing, SE automation | DBLP 近年 repair / testing 论文入口；代表作待逐篇筛选 | P4 很高，P2 中高：修复与测试反馈闭环 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Julia Lawall | FSE 2026 | Program Co-Chair | Inria / Sorbonne Université / 待补 | [FSE 2026 Research Papers committee](https://conf.researchr.org/committee/fse-2026/fse-2026-research-papers-program-committee) | [DBLP](https://dblp.org/pid/l/JuliaLawall) | program analysis, Coccinelle, software evolution | Coccinelle / program transformation 线索待逐篇补证 | P4/P3 高相关：规则化修复、程序分析证据链 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Christoph Treude | FSE 2026 | Program Co-Chair | University of Melbourne / 待补 | [FSE 2026 Research Papers committee](https://conf.researchr.org/committee/fse-2026/fse-2026-research-papers-program-committee) | [DBLP](https://dblp.org/pid/42/4730) | AI for SE, developer knowledge, empirical SE | DBLP 近年 AI4SE / LLM4SE 论文入口；代表作待逐篇筛选 | P1/P2/P4 高相关：LLM4SE、开发者知识与实验评估 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Lin Tan | FSE 2024 | Program Co-Chair | Purdue University / 待补 | [FSE 2024 Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | [DBLP](https://dblp.org/pid/t/LinTan) | software reliability, testing, program analysis | DBLP 近年 reliability / testing 论文入口；代表作待逐篇筛选 | P2/P3/P4 高相关 | 🟡 角色已核验，个人主页待补 | `2026-06-05 09:32` |
| David Lo | FSE 2024 | Program Co-Chair | Singapore Management University / 待补 | [FSE 2024 Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | [DBLP](https://dblp.org/pid/39/8119) | software analytics, mining software repositories, testing | DBLP 近年 LLM4SE / analytics 论文入口；代表作待逐篇筛选 | P2/P4 高相关，适合追踪 LLM4SE 实证线索 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| FSE Steering Committee | 长期治理层 | Steering Committee（聚合入口） | 待逐人展开 | [FSE 2026 homepage navigation](https://conf.researchr.org/home/fse-2026)；researchr steering 链接当前为 external path wrapper，需后续手工展开 | [FSE series](https://conf.researchr.org/series/fse) | venue policy, PACMSE / conference naming, research track governance | 逐人 DBLP / 任期待补 | 与投稿制度、PACMSE 计数口径直接相关 | ⚪ 聚合入口已记录，未达逐人情报粒度 | `2026-06-05 09:32` |

## 6. 年度信息汇总

> 年度表按年份降序排列。FSE 冻结口径：目录 slug 固定为 `conf-a-fse`，根 README 主名称为 `FSE`；2022-2023 年度官方写 ESEC/FSE 时仅在年度页补注。PACMSE / proceedings 是 FSE Research Papers 的出版口径，不作为独立额外论文数量重复计数。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract / registration deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 待官网 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟢 投稿中 | [FSE 2027](https://conf.researchr.org/home/fse-2027) | [Research Papers](https://conf.researchr.org/track/fse-2027/fse-2027-papers) | [Important Dates](https://conf.researchr.org/dates/fse-2027) | 待公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 无单独 abstract；full paper 2026-10-02 待补时刻 AoE / UTC-12h | 2026-10-02 待补时刻 AoE / UTC-12h | initial 2027-01-22；final 2027-03-31 | 2027-07-12..2027-07-16 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟡 已通知 / 会前 | [FSE 2026](https://conf.researchr.org/home/fse-2026) | [Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | [HotCRP](https://fse2026.hotcrp.com/) | [FSE Program](https://conf.researchr.org/program/fse-2026/program-fse-2026/) | 未公布；PACMSE Issue FSE 2026 由 Research Papers track 说明 | ⏳ 已检索未公布 | 2025-09-04 23:59 AoE / UTC-12h | 2025-09-11 23:59 AoE / UTC-12h | 2025-12-22 23:59 AoE / UTC-12h；major revision final 2026-03-24 23:59 AoE / UTC-12h | 2026-07-05..2026-07-09 | 未最终核验；program 已有条目 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [FSE 2025](https://conf.researchr.org/home/fse-2025) | [Research Papers](https://conf.researchr.org/track/fse-2025/fse-2025-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2025/fse-2025-research-papers) | [HotCRP](https://fse2025.hotcrp.com/) | [FSE Program](https://conf.researchr.org/program/fse-2025/program-fse-2025/) | [Proceedings](https://conf.researchr.org/info/fse-2025/proceedings) / PACMSE Issue FSE 2025 | [DBLP 2025](https://dblp.org/db/conf/sigsoft/fse2025c.html) | 2024-09-05 23:59 AoE / UTC-12h | 2024-09-12 23:59 AoE / UTC-12h | 2025-01-14 23:59 AoE / UTC-12h（官方页疑似写 2024，按上下文待复核）；major revision final 2025-04-01 23:59 AoE / UTC-12h | 2025-06-23..2025-06-27 | DBLP inproceedings fallback: 259 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [FSE 2024](https://conf.researchr.org/home/fse-2024) | [Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2024/fse-2024-research-papers) | [HotCRP](https://fse2024.hotcrp.com/) | [FSE Program](https://conf.researchr.org/program/fse-2024/program-fse-2024/) | [Proceedings](https://conf.researchr.org/info/fse-2024/proceedings) / PACMSE Issue FSE 2024 | [DBLP 2024](https://dblp.org/db/conf/sigsoft/fse2024c.html) | 2023-09-21 23:59 AoE / UTC-12h | 2023-09-28 23:59 AoE / UTC-12h | 2024-01-23 23:59 AoE / UTC-12h；major revision final 2024-04-16 23:59 AoE / UTC-12h | 2024-07-15..2024-07-19 | DBLP inproceedings fallback: 108 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ESEC/FSE 2023](https://conf.researchr.org/home/fse-2023) | [Research Papers](https://conf.researchr.org/track/fse-2023/fse-2023-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2023/fse-2023-research-papers) | [HotCRP](https://esecfse2023.hotcrp.com/) | [ESEC/FSE Program](https://conf.researchr.org/program/fse-2023/program-fse-2023/) | [Proceedings](https://conf.researchr.org/info/fse-2023/proceedings) | [DBLP 2023](https://dblp.org/db/conf/sigsoft/fse2023.html) | 2023-01-26 23:59 AoE / UTC-12h | 2023-02-02 23:59 AoE / UTC-12h | 2023-05-04 23:59 AoE / UTC-12h；major revision final 2023-07-27 23:59 AoE / UTC-12h | 2023-12-03..2023-12-09 | DBLP fallback 待复核 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ESEC/FSE 2022](https://conf.researchr.org/home/fse-2022) | [Research Papers](https://conf.researchr.org/track/fse-2022/fse-2022-research-papers) | [Research Papers](https://conf.researchr.org/track/fse-2022/fse-2022-research-papers) | [HotCRP](https://fse2022.hotcrp.com/) | [ESEC/FSE Program](https://conf.researchr.org/program/fse-2022/program-fse-2022/) | [Proceedings](https://conf.researchr.org/info/fse-2022/proceedings) | [DBLP 2022](https://dblp.org/db/conf/sigsoft/fse2022.html) | 2022-03-10 23:59 AoE / UTC-12h | 2022-03-17 23:59 AoE / UTC-12h | 2022-06-14 23:59 AoE / UTC-12h | 2022-11-14..2022-11-18 | DBLP fallback 待复核 | 🟡 部分核验 |

## 7. 维护备注

- 2024 起官方说明会议名称调整为 FSE；2022-2023 年度页仍保留 ESEC/FSE 官方名称。
- 2024+ Research Papers 页面说明 PACMSE issue 是主 proceedings 入口；本库不得把 PACMSE 卷期再作为独立会议论文数量重复计数。
- 2025 Research Papers 页面 initial notification 年份疑似官方页笔误；本草稿按上下文记录为待复核，不作为最终 timeline 事实。
- 2022/2023 DBLP 数量本轮未稳定抓取，年度页保留 fallback 待复核。

## 8. TIMELINE.md 同步提示

- 本 venue 当前已记录的 dated events 已同步至 [TIMELINE.md](../TIMELINE.md)；后续新增或修正 important dates 时，必须同步更新对应年度 README 与 `TIMELINE.md` 的事件发生年份章节。
- 本目录不再保留 worker 事件草稿文件；事实源以各年度 README 的“重要时间点”表与 `TIMELINE.md` 为准。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 11:46` | PR #35 近期窗口复审修复：按 FSE 2027 官方主页 / dates / Research Papers track 补齐 full paper submission、author response、initial notification、major revision submission、final notification 和会期，并同步 TIMELINE。 |
| `2026-06-05 10:00` | 补记 PR-2 复审修复日志：核心人员字段已包含核验状态 / 核查时间，FSE 2022-2025 会期已同步至全局 TIMELINE。 |
| `2026-06-05 08:39` | 初始化 FSE venue 根 README 与 2022-2028 年度索引草稿。 |
