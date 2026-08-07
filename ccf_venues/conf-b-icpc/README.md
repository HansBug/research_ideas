# ICPC README

> 信息更新时间：`2026-07-13 13:30:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ICPC |
| 全称 | IEEE/ACM International Conference on Program Comprehension |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| CCF 等级 | 🥈 |
| 出版方 | IEEE / ACM |
| 官方 series page | [ICPC official site](https://www.program-comprehension.org/)；[researchr ICPC series](https://conf.researchr.org/series/icpc) |
| 官方当前 / 最新年度主页 | [ICPC 2027](https://conf.researchr.org/home/icpc-2027) |
| 官方 CFP / Important Dates 总入口 | 逐年度维护；当前最新可核验入口见 §6 年度信息汇总 |
| 官方 proceedings / paper list 总入口 | 逐年度使用 official program / publisher / DBLP fallback |
| DBLP venue page | [DBLP ICPC stream](https://dblp.org/streams/conf/iwpc) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 已检索，未发现可核验官方年度页 / CFP / important dates |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `Proceedings - ICPC 2007: 15th IEEE International Conference on Program Comprehension`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

ICPC 面向程序理解、软件制品理解、代码 / 文档 / 历史理解、开发者认知与辅助工具，是 LLM4SE、LLM-as-Judge、LLM 辅助理解与修复上下文检索的重要 venue。

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
| Series / main site | [ICPC official site](https://www.program-comprehension.org/)；[researchr ICPC series](https://conf.researchr.org/series/icpc) | 年度独立站点 / researchr / 官方组织站点并行 | `2026-06-05 17:35` |
| Latest year homepage | [ICPC 2027](https://conf.researchr.org/home/icpc-2027) | 2027 已有 official home / venue / tracks，但 CFP / Important Dates 未公布；2028 仍未公布 | `2026-07-13 13:30` |
| CFP / Call for Papers | 见 §6 年度信息汇总 | 2027 已有 official home / tracks，但 Research Track CFP 未公布；track 分散时在年度 README 展开 | `2026-07-13 13:30` |
| Important Dates | 见 §6 年度信息汇总 | 2027 Important Dates 未公布；researchr dates / official CFP 优先 | `2026-07-13 13:30` |
| Submission system | 见 §6 年度信息汇总 | 历史系统可能失效，失效时保留待复核 | `2026-06-05 17:35` |
| Program / accepted papers | 见 §6 年度信息汇总 | 已结束年度优先 official program / accepted papers | `2026-06-05 17:35` |
| Proceedings | 见 §6 年度信息汇总 | publisher proceedings 优先，DBLP 仅作 fallback | `2026-06-05 17:35` |
| DBLP venue | [DBLP ICPC stream](https://dblp.org/streams/conf/iwpc) | 仅作论文名录 / 计数 fallback | `2026-06-05 17:35` |

## 5. 核心人员情报

本节记录当前 / 未来年度核心组织者、Program / Research Track chair、Steering / track chair 与强相关领域权威，不展开全量 PC。人员研究方向基于 official profile / DBLP / 个人主页归纳；若角色来源不是同一官方 committee 页，已在 `核验状态` 中显式降级。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Marcelo de Almeida Maia | 2026 / conference | General Chair | Federal University of Uberlândia | [ICPC 2026 organizing committee](https://conf.researchr.org/committee/icpc-2026/icpc-2026-organizing-committee) | [researchr profile](https://conf.researchr.org/profile/conf/marcelodealmeidamaia) | software engineering、machine learning、program comprehension | ICPC 2019 mining crowd knowledge paper 等线索 | P1/P4 强：任务理解、推荐和辅助修复上下文 | 🟢 官方角色核验 | `2026-06-05 17:35` |
| Nicole Novielli | 2026 / research track | Program Co-Chair | University of Bari | [ICPC 2026 organizing committee](https://conf.researchr.org/committee/icpc-2026/icpc-2026-organizing-committee) | [researchr profile](https://conf.researchr.org/profile/icpc-2026/nicolenovielli) | sentiment analysis、MSR、NLP、affective computing | profile / DBLP recent papers | P1/P4 中强：文本理解、人因反馈和 LLM-as-Judge 口径 | 🟢 官方角色核验 | `2026-06-05 17:35` |
| Igor Wiese | 2026 / research track | Program Co-Chair | Federal University of Technology - Paraná | [ICPC 2026 organizing committee](https://conf.researchr.org/committee/icpc-2026/icpc-2026-organizing-committee) | [researchr profile](https://conf.researchr.org/profile/icpc-2026/igorwiese) | MSR、recommendation systems、OSS、human aspects of SE | profile / DBLP recent papers | P1/P4 强：工件检索、上下文补全与修复建议 | 🟢 官方角色核验 | `2026-06-05 17:35` |
| Foutse Khomh | 2026 / Journal First | Journal First Co-Chair | Polytechnique Montréal | [ICPC 2026 organizing committee](https://conf.researchr.org/committee/icpc-2026/icpc-2026-organizing-committee) | [researchr profile](https://conf.researchr.org/profile/foutsekhomh) | software maintenance and evolution、software analytics、trustworthy AI/ML | profile / DBLP recent papers | P1/P4 强：维护演化、可信 AI 和修复评价 | 🟢 官方角色核验 | `2026-06-05 17:35` |
| Anita Sarma | Steering Committee | Chair, term ends 2027 | Oregon State University | [ICPC Steering Committee](https://www.program-comprehension.org/steeringcommittee.html) | [DBLP search](https://dblp.org/search?q=Anita%20Sarma) | software engineering、human / social aspects、program comprehension | DBLP recent papers | P1/P4 中强：开发者协同、理解与维护过程 | 🟡 部分核验 | `2026-06-05 17:35` |

## 6. 年度信息汇总

年度汇总表按年份降序排列。已结束年度的论文数量若来自 DBLP，均标注为 fallback，不等同于 Research Track / main track 精确计数；multi-track、companion、workshop、journal-first、tool、industry 均不得混算。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟢 投稿中 | [ICPC 2027](https://conf.researchr.org/home/icpc-2027) | [Research Track](https://conf.researchr.org/track/icpc-2027/icpc-2027-research-track) | [Important Dates](https://conf.researchr.org/dates/icpc-2027) | [HotCRP `icpc2027-technical`](https://icpc2027-technical.hotcrp.com) | 未公布 | 未公布 | ⏳ 已检索未公布 | 2026-10-29 23:59:59 AoE / UTC-12h | 2026-11-05 23:59:59 AoE / UTC-12h | 2027-01-14 23:59:59 AoE / UTC-12h | 2027-04-25..2027-04-26 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | ✅ 已结束 / proceedings 待补 | [ICPC 2026](https://conf.researchr.org/home/icpc-2026) | [Research Track](https://conf.researchr.org/track/icpc-2026/icpc-2026-research) | [Important Dates](https://conf.researchr.org/dates/icpc-2026) | [HotCRP](https://icpc2026-technical.hotcrp.com) | [Research Track](https://conf.researchr.org/track/icpc-2026/icpc-2026-research) | 未公布 | ⏳ 已检索未公布 | 2025-10-19 待补时刻 | 2025-10-23 待补时刻 | 2026-01-05 待补时刻 | 2026-04-12..2026-04-13 | 未公布 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [ICPC 2025](https://conf.researchr.org/home/icpc-2025) | [Research Track](https://conf.researchr.org/track/icpc-2025/icpc-2025-research) | [Important Dates](https://conf.researchr.org/dates/icpc-2025) | [HotCRP](https://icpc2025-technical.hotcrp.com) | [Research Track](https://conf.researchr.org/track/icpc-2025/icpc-2025-research) | [DBLP 2025](https://dblp.org/db/conf/iwpc/icpc2025.html) | [DBLP 2025](https://dblp.org/db/conf/iwpc/icpc2025.html) | 2024-11-06 待补时刻 | 2024-11-09 待补时刻 | 2025-01-12 待补时刻 | 2025-04-27..2025-04-28 | 59（DBLP inproceedings fallback；track 拆分待复核） | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [ICPC 2024](https://conf.researchr.org/home/icpc-2024) | [Research Track](https://conf.researchr.org/track/icpc-2024/icpc-2024-research) | [Important Dates](https://conf.researchr.org/dates/icpc-2024) | [HotCRP](https://icpc2024.hotcrp.com) | [Research Track](https://conf.researchr.org/track/icpc-2024/icpc-2024-research) | [DBLP 2024](https://dblp.org/db/conf/iwpc/icpc2024) | [DBLP 2024](https://dblp.org/db/conf/iwpc/icpc2024) | 2023-10-30 待补时刻 | 2023-11-03 待补时刻 | 2024-01-10 待补时刻 | 2024-04-15..2024-04-16 | 46（DBLP inproceedings fallback；track 拆分待复核） | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ICPC 2023](https://conf.researchr.org/home/icpc-2023) | [Research Track](https://conf.researchr.org/track/icpc-2023/icpc-2023-research) | [Important Dates](https://conf.researchr.org/dates/icpc-2023) | [HotCRP](https://icpc2023.hotcrp.com) | [Research Track](https://conf.researchr.org/track/icpc-2023/icpc-2023-research) | [DBLP 2023](https://dblp.org/db/conf/iwpc/icpc2023) | [DBLP 2023](https://dblp.org/db/conf/iwpc/icpc2023) | 2022-12-12 待补时刻 | 2022-12-19 待补时刻 | 2023-02-21 待补时刻 | 2023-05-15..2023-05-16 | 38（DBLP inproceedings fallback；track 拆分待复核） | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ICPC 2022](https://conf.researchr.org/home/icpc-2022) | [Research Track](https://conf.researchr.org/track/icpc-2022/icpc-2022-research) | [Important Dates](https://conf.researchr.org/dates/icpc-2022) | 待补 | [Research Track](https://conf.researchr.org/track/icpc-2022/icpc-2022-research) | [DBLP 2022](https://dblp.org/db/conf/iwpc/icpc2022) | [DBLP 2022](https://dblp.org/db/conf/iwpc/icpc2022) | 2022-01-13 待补时刻 | 2022-01-18 待补时刻 | 2022-03-08 待补时刻 | 2022-05-16..2022-05-17 | 68（DBLP inproceedings fallback；track 拆分待复核） | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、industry、tool、journal-first、registered report、artifact、workshop、co-located event 不得混算。
- `2027` 已出现 [ICPC 2027](https://conf.researchr.org/home/icpc-2027) official home，地点 Dublin, Ireland，会期 `2027-04-25..2027-04-26`，co-located with ICSE 2027；截至 `2026-07-13` 仍未公布 CFP / Important Dates / submission。`2028` 与 `2029+` 已做公开入口检索，未公布年度保留占位与核查记录，不预设 CFP。
- 本 venue 的 dated events 已按事件发生年份同步到 [../TIMELINE.md](../TIMELINE.md)；后续修改 deadline 必须同步更新年度 README、根表与 Mermaid。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [../TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [../TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-07-13 13:30:00` | 常态化刷新 ICPC：确认 2026 已结束；升级 2027 official home / venue / 会期占位，CFP 与 Important Dates 仍未公布；复查 2028 仍未公布。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 18:13` | PR-6 收尾复核：同步共享统计与待补口径，确认本 venue 仍按部分核验状态入账。 |
| `2026-06-05 17:35` | PR-6 初始化 ICPC venue 根 README，新增 2022-2028 年度索引、核心 URL、核心人员情报、计数口径与待补记录。 |
