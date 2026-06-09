# ICFEM README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ICFEM |
| 全称 | International Conference on Formal Engineering Methods |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 形式化工程方法 |
| CCF 等级 | C |
| 本库目录 | `conf-c-icfem` |
| 出版方 | Springer LNCS / ICFEM official annual pages |
| 官方 series page | 待补（未发现独立稳定 series page；当前以 [DBLP ICFEM index](https://dblp.org/db/conf/icfem/index.html) 作索引 fallback，年度事实仍以各年度主页为准） |
| DBLP venue page | [DBLP ICFEM index](https://dblp.org/db/conf/icfem/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF C 级；emoji 已按 GUIDE 的 A/B/C 口径编码，不再统一写成黄色 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `ICFEM 2000 - 3rd IEEE International Conference on Formal Engineering Methods`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

ICFEM 关注形式化工程方法、形式化规格、验证、建模、测试、工具与工业应用，是控制系统状态机建模和验证案例的重要 CCF C venue。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟢 高 | 形式化工程方法与状态机/规约建模高度相关。 |
| P2 | 🟢 高 | 从模型元素提取验证场景和性质是常见议题。 |
| P3 | 🟢 高 | 模型检查、证明和工具论文可支撑验证 profile。 |
| P4 | 🟡 中 | 修复/精化线索需从具体论文中二次筛选。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | 待补 | 未发现独立稳定 series page；当前以 [DBLP ICFEM index](https://dblp.org/db/conf/icfem/index.html) 作索引 fallback，年度信息仍以年度页 / CFP 为准 | `2026-06-05 11:12` |
| DBLP venue page | [DBLP ICFEM index](https://dblp.org/db/conf/icfem/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| 最新年度入口 | ⏳ 已检索未公布 | `2029+` 已检索未公布；未来年度不得伪造；2026 Important Dates 已复核 `23:59 AoE / UTC-12` | `2026-06-06 10:16` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Michael Butler | ICFEM 2026 Steering Committee / General Chair | University of Southampton | [ICFEM 2026 Committee](https://icfem2026.github.io/#committee) | [Southampton profile](https://www.southampton.ac.uk/people/5wy556/professor-michael-butler) | 形式化方法、Event-B、软件工程 | [DBLP](https://dblp.org/pid/b/MichaelJButler.html) | P1/P3：形式化建模、精化与验证。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Étienne André | ICFEM 2026 Program Chair | Nantes Université | [ICFEM 2026 Committee](https://icfem2026.github.io/#committee) | [ORCID](https://orcid.org/0000-0001-8473-9555) | timed automata、model checking、synthesis | [DBLP](https://dblp.org/pid/49/2992.html) | P1/P2/P3：时间自动机与性质验证。 | 🟡 部分核验 | `2026-06-05 10:04` |
| David Basin | ICFEM 2026 Steering Committee | ETH Zurich | [ICFEM 2026 Committee](https://icfem2026.github.io/#committee) | [DBLP](https://dblp.org/pid/b/DavidBasin.html) | formal methods、security protocols、runtime monitoring | [DBLP 论文入口](https://dblp.org/pid/b/DavidBasin.html) | P2/P3：安全性质与监控。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Jin Song Dong | ICFEM 2026 Steering Committee | National University of Singapore | [ICFEM 2026 Committee](https://icfem2026.github.io/#committee) | [DBLP](https://dblp.org/pid/d/JinSongDong.html) | formal methods、model checking、software engineering | [DBLP 论文入口](https://dblp.org/pid/d/JinSongDong.html) | P1/P3：形式化建模与验证。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Kazuhiro Ogata | ICFEM 2026 Steering Committee | Japan Advanced Institute of Science and Technology | [ICFEM 2026 Committee](https://icfem2026.github.io/#committee) | [DBLP](https://dblp.org/pid/o/KazuhiroOgata.html) | algebraic specification、proof score、formal verification | [DBLP 论文入口](https://dblp.org/pid/o/KazuhiroOgata.html) | P2/P3/P4：规约、证明与验证反馈。 | 🟡 部分核验 | `2026-06-05 10:04` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ICFEM index](https://dblp.org/db/conf/icfem/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ICFEM index](https://dblp.org/db/conf/icfem/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟢 投稿中 | [ICFEM 2026](https://icfem2026.github.io/) | [CFP](https://icfem2026.github.io/#call-for-papers) | [Important Dates](https://icfem2026.github.io/#dates) | [Submission](https://icfem2026.github.io/#submission) | 未公布（`#program` 当前 TBA） | 未公布 | [DBLP](https://dblp.org/db/conf/icfem/index.html) | 2026-06-15 23:59 AoE / UTC-12 | 2026-06-22 23:59 AoE / UTC-12 | 2026-08-08 23:59 AoE / UTC-12 | 2026-11-17..2026-11-20 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [ICFEM 2025](https://icfem2025.github.io/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-981-95-4213-0) | [DBLP](https://dblp.org/db/conf/icfem/icfem2025) | 未公布 | 未公布 | 未公布 | 2025-11-10..2025-11-13 | 21 papers / 1 volume | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [ICFEM 2024](https://icfem2024.info/) | [CFP](https://icfem2024.info/ICFEM2024CallforPapers.pdf) | 未公布 | 未公布 | [Program / Accepted](https://icfem2024.info/ICFEM2024_Formatted_Program_VeryFinal.pdf) | [Proceedings](https://link.springer.com/book/10.1007/978-981-96-0617-7) | [DBLP](https://dblp.org/db/conf/icfem/icfem2024) | 未公布 | 未公布 | 未公布 | 2024 待补精确日期 | 22 papers / 1 volume | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [ICFEM 2023](https://formal-analysis.com/icfem/2023/) | 未公布 | 未公布 | 未公布 | [Program / Accepted](https://formal-analysis.com/icfem/2023/ICFEM2023-Program.pdf) | [Proceedings](https://link.springer.com/book/10.1007/978-981-99-7584-6) | [DBLP](https://dblp.org/db/conf/icfem/icfem2023) | 未公布 | 未公布 | 未公布 | 2023 待补精确日期 | 23 papers / 1 volume | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [ICFEM 2022](https://maude.ucm.es/ICFEM22/) | 未公布 | [Important Dates](https://maude.ucm.es/ICFEM22/c_impd.html) | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-17244-1) | [DBLP](https://dblp.org/db/conf/icfem/icfem2022) | 未公布 | 2022-05-07 待补时刻 AoE | 未公布 | 2022-10-24..2022-10-27 | 26 papers / 1 volume | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 均已做公开入口检索；未公布年度保留占位与核查记录，不预设 CFP。
- 2028 计数口径：未发现 ICFEM 2028 官方年页。
- 2027 计数口径：未发现 ICFEM 2027 官方年页。
- 2026 计数口径：2026 不设置 artifact evaluation；`#program` 当前为 TBA，不能写成 accepted papers；论文数量待 accepted/proceedings。
- 2025 计数口径：Springer LNCS 16229 / DBLP 年度页交叉核验。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把可核验的 ICFEM 2026 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度章节与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 10:16` | 根据 PR #35 main-ready review 核验官方 Important Dates，将 ICFEM 2026 根表 abstract / full paper / notification 精确到 `23:59 AoE / UTC-12`。 |
| `2026-06-05 11:12` | 修复 ICFEM 2026 `#program` 过度确认：program 当前 TBA，不写作 accepted papers；同时将根 README 中误作 series page 的 2026 年度页降级为年度页 / DBLP fallback。 |
| `2026-06-05 10:04` | 将核心人员官方角色来源细化到 ICFEM 2026 Committee anchor，并区分 Steering Committee、General Chair 与 Program Chair。 |
| `2026-06-05 09:15` | PR-3 初始化 ICFEM venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
