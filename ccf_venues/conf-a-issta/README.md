# ISSTA README

> 信息更新时间：`2026-08-07 20:15:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ISSTA |
| 全称 | ACM SIGSOFT International Symposium on Software Testing and Analysis |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | 🏆 |
| 出版方 | ACM / PACMSE（2025+ research papers 页面说明） |
| 官方 series page | [ISSTA series](https://conf.researchr.org/series/issta) |
| 官方当前 / 最新年度主页 | [ISSTA 2026](https://conf.researchr.org/home/issta-2026) |
| 官方 CFP / Important Dates 总入口 | 逐年度 Technical / Research Papers track 维护 |
| 官方 proceedings / paper list 总入口 | 逐年度 program / ACM / DBLP fallback |
| DBLP venue page | [DBLP ISSTA venue](https://dblp.org/db/conf/issta/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🏆 | CCF 🏆 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `2014 International Symposium on Software Testing and Analysis, ISSTA 2014 - Proceedings`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

- ISSTA 聚焦软件测试与分析，覆盖测试生成、程序分析、调试、修复、验证、artifact 和 testing for AI / AI for testing。
- 与本仓库最相关的方向：验证场景生成、属性 / oracle、程序分析、模型检查相邻技术、自动修复与 LLM4Testing。
- 明显不属于本仓库重点但可作背景：泛 PL co-location 活动、教育 / sponsorship / 社区活动。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中 | 可追踪测试驱动建模、程序行为抽象与规格推断。 |
| P2 场景与性质生成 | 高 | ISSTA 是测试生成、oracle、fuzzing、analysis 的核心 venue。 |
| P3 验证剖面与模型检查 | 高 | 程序分析、静态 / 动态验证、符号执行与模型检查相关论文密集。 |
| P4 模型修复 | 高 | 调试、fault localization、repair、testing-guided repair 与本仓库强相关。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [ISSTA series](https://conf.researchr.org/series/issta) | researchr 长期入口 | `2026-06-05 08:39` |
| Latest year homepage | [ISSTA 2027](https://conf.researchr.org/home/issta-2027) | ⚠️ **2026-08-07 更正**：ISSTA 2027 官方站已上线（第 36 届 Singapore，mandatory abstract `2027-01-08`、full paper `2027-01-11`，AoE / UTC-12h）；2028 由 [issta.org](http://www.issta.org/) 公布地点 Shanghai, China（`conf.researchr.org/home/issta-2028` 仍 404）。此前「2027/2028 于 2026-07-13 复查仍未公布」已作废 | `2026-08-07 20:25:00` |
| CFP / Call for Papers | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | 2022-2023 为 Technical Papers 命名 | `2026-07-13 19:13:21` |
| Important Dates | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | 与 CFP 同页；2026 官方只给日期 + AoE，未给具体钟点；camera-ready `2026-07-23` | `2026-07-13 19:13:21` |
| Submission system | [ISSTA 2026 HotCRP](https://issta2026.hotcrp.com/) | 历年入口见年度页 | `2026-06-05 08:39` |
| Program / accepted papers | [ISSTA 2025 Program](https://conf.researchr.org/program/issta-2025/program-issta-2025/) | 已结束年度优先官方 program，DBLP fallback | `2026-06-05 08:39` |
| Proceedings | [DBLP ISSTA venue](https://dblp.org/db/conf/issta/) | ACM DL / PACMSE 待逐年补证 | `2026-06-05 08:39` |
| DBLP venue | [DBLP ISSTA venue](https://dblp.org/db/conf/issta/) | 仅作论文名录 / 计数 fallback | `2026-06-05 08:39` |

## 5. 核心人员情报

> 人员角色以 ISSTA 官方年度 research papers / track committee 为准；研究方向和代表作基于个人主页、DBLP 或公开学术入口归纳。本表优先记录 Research Papers Chair、与 P1-P4 强相关的 Area Chair / track chair 和测试分析领域权威；不等同于全量 PC roster。

| 人员 | 年度 / 层级 | 会议角色 | 单位 / 主页入口 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Marcel Böhme | ISSTA 2026 | Research Papers Co-Chair | MPI-SP / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/74/5763) | fuzzing, software testing, debugging, security testing | DBLP 近年 fuzzing / testing 论文入口；代表作待逐篇筛选 | P2/P4 很高：测试生成、缺陷定位和自动修复评估 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Cindy Rubio-González | ISSTA 2026 | Research Papers Co-Chair | UC Davis / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/73/4965) | program analysis, debugging, dynamic analysis | DBLP 近年 analysis / debugging 论文入口；代表作待逐篇筛选 | P3/P4 高相关：分析、调试、修复证据链 | 🟡 角色已核验，个人主页待补 | `2026-06-05 09:32` |
| Lionel Briand | ISSTA 2026 | Area Chair, AI for Analysis and Testing | University of Luxembourg / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/b/LionelBriand) | software testing, verification, model-based testing, AI for SE | DBLP 近年 model-based testing / AI4SE 论文入口；代表作待逐篇筛选 | P1/P2/P3 极高：模型测试、需求/验证和 LLM4SE | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Corina S. Păsăreanu | ISSTA 2026 | Area Chair, AI for Analysis and Testing | NASA Ames / CMU Silicon Valley / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/p/CorinaSPasareanu) | symbolic execution, model checking, program analysis | DBLP 近年 symbolic execution / model checking 论文入口；代表作待逐篇筛选 | P2/P3 很高：性质检查、模型检查和场景生成 | 🟡 角色已核验，主页待补 | `2026-06-05 09:32` |
| Lingming Zhang | ISSTA 2026 | Area Chair, AI for Analysis and Testing | UIUC / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/56/8404) | software testing, debugging, deep learning testing | DBLP 近年 testing / LLM testing 论文入口；代表作待逐篇筛选 | P2/P4 高相关 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Sukyoung Ryu | ISSTA 2026 | Area Chair, Program Analysis & Verification | KAIST / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/r/SukyoungRyu) | programming languages, program analysis, verification | DBLP 近年 PL / analysis 论文入口；代表作待逐篇筛选 | P3 高相关：分析与验证方法 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |
| Andreas Zeller | ISSTA 2026 | Area Chair, Software Test Generation | CISPA / Saarland University / 待补 | [ISSTA 2026 Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [DBLP](https://dblp.org/pid/z/AndreasZeller) | automated debugging, test generation, mining specs | DBLP 近年 debugging / test generation 论文入口；代表作待逐篇筛选 | P2/P4 极高：测试生成、调试和反馈修复 | 🟡 角色已核验，代表作待深挖 | `2026-06-05 09:32` |

## 6. 年度信息汇总

> ISSTA 冻结口径：2024+ co-location / joint week 只作为会期和入口关系；论文数量按 ISSTA 独立 accepted papers / ACM proceedings / DBLP ISSTA entry 计数，不混入 FSE research track。若同一入口出现在联合 proceedings / FSE companion，仅在证据栏说明，不重复计数。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | 🟦 已有预告 | [issta.org](http://www.issta.org/)（`conf.researchr.org/home/issta-2028` 仍 HTTP 404） | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 地点 Shanghai, China（会期未公布） | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | 🟢 投稿中 | [ISSTA 2027](https://conf.researchr.org/home/issta-2027) | [Research Papers](https://conf.researchr.org/track/issta-2027/issta-2027-research-papers) | [Important Dates](https://conf.researchr.org/dates/issta-2027) | ⏳ 已检索未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | mandatory abstract 2027-01-08 待补时刻 AoE / UTC-12h；full paper 2027-01-11 待补时刻 AoE / UTC-12h | 2027-04-20 待补时刻 AoE / UTC-12h（initial）；2027-06-17（final） | 2027-09-07..2027-09-10 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟣 通知后 | [ISSTA 2026](https://conf.researchr.org/home/issta-2026) | [Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [Research papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [HotCRP](https://issta2026.hotcrp.com/) | 未公布 | PACMSE Issue ISSTA 2026（track 说明；未正式发布） | ⏳ 已检索未公布 | 2026-01-29 待补时刻 AoE / UTC-12h | initial 2026-04-16 待补时刻 AoE / UTC-12h；final 2026-06-25 待补时刻 AoE / UTC-12h；camera-ready 2026-07-23 待补时刻 AoE / UTC-12h | 2026-10-03..2026-10-09 | 名录已公布 / 计数待补（页面过长被截断，不得填数字） | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [ISSTA 2025](https://conf.researchr.org/home/issta-2025) | [Research Papers](https://conf.researchr.org/track/issta-2025/issta-2025-papers) | [Important Dates](https://conf.researchr.org/dates/issta-2025) | [HotCRP](https://issta25.hotcrp.com/) | [ISSTA Program](https://conf.researchr.org/program/issta-2025/program-issta-2025/) | PACMSE Issue ISSTA 2025（[proceedings probe](https://conf.researchr.org/info/issta-2025/proceedings) 当前 accessDenied，待 ACM/PACMSE 交叉核验） | [DBLP 2025 companion fallback](https://dblp.org/db/conf/issta/issta2025c.html) | 2024-10-31 23:59:59 AoE / UTC-12h | 2024-12-19 23:59:59 AoE / UTC-12h；final 2025-03-31 23:59:59 AoE / UTC-12h | 2025-06-25..2025-06-28 | DBLP companion fallback: 35 ⚠️ 待 ACM/PACMSE 交叉核验 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [ISSTA 2024](https://conf.researchr.org/home/issta-2024) | [Technical Papers](https://conf.researchr.org/track/issta-2024/issta-2024-papers) | [Important Dates](https://conf.researchr.org/dates/issta-2024) | [HotCRP](https://issta24.hotcrp.com/) | [ISSTA Program](https://conf.researchr.org/program/issta-2024/program-issta-2024/) | 未逐项核验；ACM / DBLP fallback | [DBLP 2024](https://dblp.org/db/conf/issta/issta2024.html) | 2023-12-15 23:59 AoE / UTC-12h；round 2 2024-04-12 23:59 AoE / UTC-12h | 2024-03-02 待补时刻 AoE / UTC-12h；round 2 2024-07-03 待补时刻 AoE / UTC-12h | 2024-09-16..2024-09-20 | DBLP inproceedings fallback: 170 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [ISSTA 2023](https://conf.researchr.org/home/issta-2023) | [Technical Papers](https://conf.researchr.org/track/issta-2023/issta-2023-technical-papers) | [Technical Papers](https://conf.researchr.org/track/issta-2023/issta-2023-technical-papers) | [HotCRP](https://issta2023.hotcrp.com/) | [ISSTA Program](https://conf.researchr.org/program/issta-2023/program-issta-2023/) | 未逐项核验；ACM / DBLP fallback | [DBLP 2023](https://dblp.org/db/conf/issta/issta2023.html) | 2022-11-10 23:59 AoE / UTC-12h；second round 2023-02-16 23:59 AoE / UTC-12h | 2023-01-16 23:59 AoE / UTC-12h；second round 2023-05-03 23:59 AoE / UTC-12h | 2023-07-17..2023-07-21 | DBLP inproceedings fallback: 138 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [ISSTA 2022](https://conf.researchr.org/home/issta-2022) | [Technical Papers](https://conf.researchr.org/track/issta-2022/issta-2022-technical-papers) | [Technical Papers](https://conf.researchr.org/track/issta-2022/issta-2022-technical-papers) | [HotCRP](https://issta22.hotcrp.com/) | [ISSTA Program](https://conf.researchr.org/program/issta-2022/program-issta-2022/) | 未逐项核验；ACM / DBLP fallback | [DBLP 2022](https://dblp.org/db/conf/issta/issta2022.html) | 2022-01-28 23:59 AoE / UTC-12h | 2022-04-11 23:59 AoE / UTC-12h | 2022-07-18..2022-07-22 | DBLP inproceedings fallback: 72 | 🟡 部分核验 |

## 7. 维护备注

- 2026 与 SPLASH/ISSTA co-located，2024 与 ECOOP/ISSTA co-located，2025 与 FSE 同地同周；这些只作为会期/入口关系，不改变 ISSTA 独立计数。
- 2024/2025 official track canonical slug 均为 `issta-YYYY-papers`：2024 页面标题为 Technical Papers，2025 页面标题为 Research Papers；不要再猜 `technical-papers` / `research-papers` 这类会 404 的 slug。
- ISSTA 2026 已过 final notification，下一主链节点为 camera-ready `2026-07-23 待补时刻 AoE / UTC-12h`，会期 `2026-10-03..2026-10-09`。
- ⚠️ **2026-08-07 更正**：ISSTA **2027** 正式年度主页、Research Papers track、dates、venue 与组织委员会均已上线（主轨 mandatory abstract `2027-01-08`、full paper `2027-01-11`，`AoE (UTC-12h)`）；**2028** 已由 [issta.org](http://www.issta.org/) 公布地点 Shanghai, China 与三位 chair，但 researchr 年度页仍 404、会期未公布。此前「2027/2028 于 2026-07-13 复查仍未公布」的结论已作废；仍不伪造未公布的日期。
- 2022-2024 数量暂以 DBLP inproceedings fallback；2025 DBLP `issta2025c.html` 明确为 companion/fallback 入口，35 条不能当作最终主 proceedings 数量，后续必须以 ACM DL / PACMSE Issue ISSTA 2025 和官方 accepted papers 交叉核验。

## 8. TIMELINE.md 同步提示

- 本 venue 当前已记录的 dated events 已同步至 [TIMELINE.md](../TIMELINE.md)；后续新增或修正 important dates 时，必须同步更新对应年度 README 与 `TIMELINE.md` 的事件发生年份章节。
- 本目录不再保留 worker 事件草稿文件；事实源以各年度 README 的“重要时间点”表与 `TIMELINE.md` 为准。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:15:00` | 常态化刷新：2027 行由 `⏳ 待官网` 升级为 `🟢 投稿中`（mandatory abstract `2027-01-08`、full paper `2027-01-11`，AoE / UTC-12h；Singapore，会期 2027-09-07..10）；2028 行由 `⏳ 待官网` 升级为 `🟦 已有预告`（issta.org 官方公布 Shanghai, China）；ISSTA 2026 accepted 名录已上线但页面过长被截断，计数待补。 |
| `2026-07-13 19:13:21` | 常态化刷新：复核 ISSTA 2026 camera-ready `2026-07-23` 与会期；2027/2028 仍未公布，保守更新复查记录。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 13:16` | PR #35 近期窗口复审修复：同步 ISSTA 2026 日期精度、author response 与 camera-ready 口径，避免把官方未给钟点的 AoE 日期写成 `23:59`。 |
| `2026-06-05 10:00` | 根据 PR-2 修复后复审，确认 2022/2023 会期已补入全局 TIMELINE，并补记核心人员字段修复日志。 |
| `2026-06-05 08:39` | 初始化 ISSTA venue 根 README 与 2022-2028 年度索引草稿。 |
