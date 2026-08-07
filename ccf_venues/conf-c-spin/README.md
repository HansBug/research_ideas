# SPIN README

> 信息更新时间：`2026-08-07 20:25:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | SPIN |
| 全称 | International Symposium on Model Checking of Software |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 模型检查 / 运行时验证 |
| CCF 等级 | 🥉 |
| 本库目录 | `conf-c-spin` |
| 出版方 | Springer LNCS / SPIN official pages |
| 官方 series page | [SPIN official pages](https://spin-web.github.io/) |
| DBLP venue page | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `2014 International SPIN Symposium on Model Checking of Software, SPIN 2014 - Proceedings`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

SPIN 聚焦软件模型检查、运行时验证、验证工具、形式化建模、自动机和工业案例；artifact / tool paper 与 full paper 必须分开。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟢 高 | Promela/SPIN、状态空间和状态机建模是直接素材。 |
| P2 | 🟢 高 | 性质、monitor、counterexample 与场景生成直接相关。 |
| P3 | 🟢 高 | 模型检查与验证工具是 P3 的核心。 |
| P4 | 🟡 中 | 修复线索需从 counterexample / runtime verification 论文筛选。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [SPIN official pages](https://spin-web.github.io/) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-06-05 09:15` |
| DBLP venue page | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| 最新年度入口 | [SPIN 2026](https://spin-web.github.io/SPIN2026/) | 2026 已结束；2027/2028/2029+ 已于 2026-07-13 复查未公布，未来年度不得伪造 | `2026-07-13 10:27:51` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Gidon Ernst | SPIN 2025 Program Chair；SPIN 2026 Program Committee | Ludwig-Maximilians-Universität München | [SPIN 2025 Committees](https://spin-web.github.io/SPIN2025/committees) / [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [Homepage](https://www.gidonernst.de/) | logic and formal methods for reliable software and systems | [DBLP](https://dblp.org/pid/19/1202.html) | P2/P3：形式化逻辑、验证工具和可靠软件。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Kristin Yvonne Rozier | SPIN 2025 Program Chair；SPIN 2026 Program Committee | Iowa State University | [SPIN 2025 Committees](https://spin-web.github.io/SPIN2025/committees) / [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/67/519.html) | temporal logic、runtime observers、safety-critical systems | [DBLP 论文入口](https://dblp.org/pid/67/519.html) | P2/P3：时序性质与 runtime monitor。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Vincenzo Ciancia | SPIN 2026 Program Chair | ISTI-CNR | [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/31/4665.html) | spatial logics、model checking、formal methods | [DBLP 论文入口](https://dblp.org/pid/31/4665.html) | P2/P3：逻辑性质与模型检查。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Arnd Hartmanns | SPIN 2026 Program Chair | University of Twente | [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/77/7997.html) | probabilistic model checking、stochastic systems、tools | [DBLP 论文入口](https://dblp.org/pid/77/7997.html) | P3：概率/定量验证 profile。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Gerard Holzmann | SPIN 2025/2026 Steering Committee | Nimble Research | [SPIN 2025 Committees](https://spin-web.github.io/SPIN2025/committees) / [SPIN 2026 Committees](https://spin-web.github.io/SPIN2026/committees) | [DBLP](https://dblp.org/pid/h/GerardJHolzmann.html) | SPIN model checker、Promela、software model checking | [DBLP 论文入口](https://dblp.org/pid/h/GerardJHolzmann.html) | P1/P3：状态机建模和软件模型检查 foundational。 | 🟡 部分核验 | `2026-06-05 10:04` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP SPIN index](https://dblp.org/db/conf/spin/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | ✅ 已结束 | [SPIN 2026](https://spin-web.github.io/SPIN2026/) | [CFP](https://spin-web.github.io/SPIN2026/cfp) | [Important Dates](https://spin-web.github.io/SPIN2026/cfp) | [EasyChair SPIN 2026](https://easychair.org/conferences/?conf=spin2026) | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/spin/index.html) | 2026-01-22 待补时刻 AoE | 2026-01-29 待补时刻 AoE | 2026-03-05 待补时刻 | 2026-04-15..2026-04-16 | 7 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [SPIN 2025](https://spin-web.github.io/SPIN2025/) | [CFP](https://spin-web.github.io/SPIN2025/cfp) | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/9783032068460) | [DBLP](https://dblp.org/db/conf/spin/spin2025) | 未公布 | 未公布 | 未公布 | 2025 待补精确日期 | 9 full papers / 20 submissions | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [SPIN 2024](https://spin-web.github.io/SPIN2024/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-66149-5) | [DBLP](https://dblp.org/db/conf/spin/spin2024) | 未公布 | 未公布 | 未公布 | 2024 待补精确日期 | 14 papers / 1 volume | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [SPIN 2023](https://spin-web.github.io/SPIN2023/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-32156-6) | [DBLP](https://dblp.org/db/conf/spin/spin2023) | 未公布 | 未公布 | 未公布 | 2023 待补精确日期 | 11 papers / 1 volume | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [SPIN 2022](https://spinroot.com/spin/Workshops/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-15077-7) | [DBLP](https://dblp.org/db/conf/spin/spin2022) | 未公布 | 未公布 | 未公布 | 2022 待补精确日期 | 8 full papers / 9 TOC entries | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 已于 2026-07-13 做公开入口复查；未公布年度保留占位与核查记录，不预设 CFP。
- 2028 计数口径：未发现 SPIN 2028 官方年页。
- 2027 计数口径：未发现 SPIN 2027 官方年页。
- 2026 计数口径：程序 / proceedings 尚未作为闭合 count 纳入。
- 2025 计数口径：Springer count；不混入 artifact/tool 额外项。
- 2022 计数口径：矛盾待解：Springer book page 写 8 full papers selected from 11 submissions；Springer/DBLP TOC 口径可见 9 entries。正式 full-paper 口径优先 8。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把 2025--2027 年可核验的主要 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度时间线与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:25:00` | 常态化刷新：2026 行论文数量由 `未公布` 补为 **7**（官方 program 页 `Accepted papers` 清单逐条统计，含 Best Paper Award）；Springer LNCS 卷与 DBLP `spin2026` 年度页仍未发布（后者复查 HTTP 404）。 |
| `2026-07-13 10:27:51` | 常态化刷新 SPIN 2026：确认会议已结束，2027/2028 保守复查未见官方年度信息。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 10:04` | 根据复审把 SPIN 核心人员来源改为 `/committees` 直达页，明确 Program Chair / Program Committee / Steering Committee 角色。 |
| `2026-06-05 09:15` | PR-3 初始化 SPIN venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
