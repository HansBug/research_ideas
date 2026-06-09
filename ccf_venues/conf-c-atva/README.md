# ATVA README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ATVA |
| 全称 | International Symposium on Automated Technology for Verification and Analysis |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 自动验证 / 分析 |
| CCF 等级 | C |
| 本库目录 | `conf-c-atva` |
| 出版方 | Springer LNCS / ATVA official pages |
| 官方 series page | [ATVA official site](https://atva-conference.org/) |
| DBLP venue page | [DBLP ATVA index](https://dblp.org/db/conf/atva/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF C 级；emoji 已按 GUIDE 的 A/B/C 口径编码，不再统一写成黄色 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🔴 | 已检索 Elsevier 官方 Compendex source list，未取得 ATVA 可用官方行级证据；LNCS 泛线索不得写成会议收录事实 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本轮按 `SERIALS` / `NON-SERIALS` 与会议全称、缩写、proceedings title 交叉检索，未获可审计匹配行 | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核 Compendex source-list 字段，尤其不能把 book-series 或缩写碰撞升级为 venue-level EI 事实 | `2026-06-09 16:45` |

## 2. Scope 与方向

ATVA 聚焦自动化验证与分析、模型检查、程序分析、系统验证、工具和 artifact；本轮保守处理 2026 候选入口，未把未独立核验的路径写成正式 CFP。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 自动机和系统建模对状态机建模有参考价值。 |
| P2 | 🟢 高 | 自动验证性质、反例和 benchmark 相关。 |
| P3 | 🟢 高 | model checking、verification、analysis 是核心。 |
| P4 | 🟡 中 | CEGAR/refinement/analysis feedback 可作为修复线索。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [ATVA official site](https://atva-conference.org/) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-06-05 09:15` |
| DBLP venue page | [DBLP ATVA index](https://dblp.org/db/conf/atva/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| 最新年度入口 | ⏳ 已检索未公布 | `2029+` 已检索未公布；未来年度不得伪造 | `2026-06-05 09:15` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Ichiro Hasuo | ATVA 2024 Organization | National Institute of Informatics | [ATVA 2024 Organization](https://atva-conference.org/2024/organization/) | [NII profile](https://www.nii.ac.jp/en/faculty/architecture/hasuo_ichiro/) | category theory、system/program verification、formal methods | [Research page](https://group-mmm.org/~ichiro/research.html) | P2/P3：验证理论、系统验证和 AI/形式化交叉。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Jun Sun | ATVA 2023 Organization | Singapore Management University | [ATVA 2023 Organization](https://atva-conference.org/2023/?page_id=30) | [OpenReview](https://openreview.net/profile?id=~Jun_Sun12) | formal methods、software engineering、security、AI | [DBLP](https://dblp.org/pid/44/905.html) | P1/P2/P3/P4：形式化建模、验证、修复与 LLM4SE。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Doron Peled | ATVA 2024 Program Committee / Steering Committee | Bar-Ilan University | [ATVA 2024 Organization](https://atva-conference.org/2024/organization/) | [DBLP](https://dblp.org/pid/p/DoronPeled.html) | model checking、partial order reduction、formal verification | [DBLP 论文入口](https://dblp.org/pid/p/DoronPeled.html) | P2/P3：模型检查与状态空间约简。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Orna Kupferman | ATVA 2024 Program Committee | Hebrew University of Jerusalem | [ATVA 2024 Organization](https://atva-conference.org/2024/organization/) | [DBLP](https://dblp.org/pid/k/OrnaKupferman.html) | automata theory、temporal logic、formal verification | [DBLP 论文入口](https://dblp.org/pid/k/OrnaKupferman.html) | P1/P2/P3：自动机和时序性质。 | 🟡 部分核验 | `2026-06-05 10:04` |

### 5.1 学术线索 / 官方角色待补

以下条目只作为后续补查 ATVA 官方角色页和领域画像的线索，不计入已核验核心人员表，也不得在 [SUMMARY.md](../SUMMARY.md) 中写成已确认官方角色。

| 人员 | 线索类型 | 单位 | 当前角色来源状态 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Jan Křetínský | probabilistic verification 学术线索 | Technical University of Munich | ATVA 官方角色页待补；当前仅保留学术入口线索 | [DBLP](https://dblp.org/pid/10/394.html) | probabilistic verification、Markov models、automata learning | [DBLP 论文入口](https://dblp.org/pid/10/394.html) | P2/P3：概率验证 profile 和模型学习。 | ⏳ 待核验，非官方角色事实 | `2026-06-05 11:43` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ATVA index](https://dblp.org/db/conf/atva/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ATVA index](https://dblp.org/db/conf/atva/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/atva/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [ATVA 2025](https://conf.researchr.org/home/atva-2025) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/conference/atva) | [DBLP](https://dblp.org/db/conf/atva/atva2025) | 未公布 | 未公布 | 未公布 | 2025-10-27..2025-10-31 | 21 papers / 1 volume | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [ATVA 2024](https://atva-conference.org/2024/) | 未公布 | [Important Dates](https://atva-conference.org/2024/important-dates/) | 未公布 | [Program / Accepted](https://atva-conference.org/2024/program/) | [Proceedings](https://link.springer.com/conference/atva) | [DBLP](https://dblp.org/db/conf/atva/index.html) | 未公布 | 未公布 | 未公布 | 2024 待补精确日期 | 28 papers / 2 volumes | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [ATVA 2023](https://atva-conference.org/2023/) | 未公布 | [Important Dates](https://atva-conference.org/2023/?page_id=47) | 未公布 | [Program / Accepted](https://atva-conference.org/2023/?page_id=34) | [Proceedings](https://link.springer.com/conference/atva) | [DBLP](https://dblp.org/db/conf/atva/index.html) | 未公布 | 未公布 | 未公布 | 2023 待补精确日期 | 38 papers / 2 volumes | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [ATVA 2022](https://atva-conference.org/2022/) | [CFP](https://atva-conference.org/2022/call-for-papers/) | [Important Dates](https://atva-conference.org/2022/important-dates/) | 未公布 | [Accepted Papers](https://atva-conference.org/2022/call-for-papers/accepted-papers/) / [Program](https://atva-conference.org/2022/program/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-19992-9) | [DBLP](https://dblp.org/db/conf/atva/atva2022) | 2022-05-08 待补时刻 AoE | 2022-05-15 待补时刻 AoE | 2022-07-04 待补时刻 AoE | 2022-10-25..2022-10-28 | 21 regular + 5 tool + 1 invited / Springer TOC 27 papers | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 均已做公开入口检索；未公布年度保留占位与核查记录，不预设 CFP。
- 2028 计数口径：未发现 ATVA 2028 官方年页。
- 2027 计数口径：未发现 ATVA 2027 官方年页。
- 2026：命令行访问 atva-conference.org 个别路径可能出现 406 / 证书或 WAF 问题；用户允许忽略证书风险，但 404/未公布仍不能当作有效来源。
- 2026 计数口径：截至 2026-06-05 未检索到独立 ATVA 2026 官方年页 / CFP / dates；researchr APLAS-ATVA 候选入口未作为正式事实写入。
- 2022 计数口径：已核验独立年度页；Springer proceedings 写 21 regular + 5 tool + 1 invited，Springer TOC 显示 27 papers；EasyChair CFP 仅作历史 fallback。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 本 venue 当前未发现可核验的 `2026` 及之后 dated events；若后续新增或修改 dated events，必须直接并入 [TIMELINE.md](../TIMELINE.md) 的正式年度章节与 Mermaid，不另建临时增量事实表。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 11:43` | 将 Jan Křetínský 从已核验核心人员表移入“学术线索 / 官方角色待补”小节，避免把未核验学术线索误读为 ATVA 官方角色。 |
| `2026-06-05 11:12` | 修复 ATVA 2022 年度主页口径：previous-events 仅作历史索引，正式年度主页改为独立 2022 年页，并补 official dates、accepted papers、program 和 Springer proceedings 链接。 |
| `2026-06-05 10:04` | 修正 ATVA 2026 年度主页为已检索未公布，降级 Jan Křetínský 为学术线索，并把 Doron Peled / Orna Kupferman 的官方角色来源落到 ATVA 2024 Organization。 |
| `2026-06-05 09:15` | PR-3 初始化 ATVA venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
