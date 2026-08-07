# ISSRE README

> 信息更新时间：`2026-08-07 20:25:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ISSRE |
| 全称 | IEEE International Symposium on Software Reliability Engineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 可靠性 / 测试 |
| CCF 等级 | 🥈 |
| 本库目录 | `conf-b-issre` |
| 出版方 | IEEE / ISSRE official annual pages |
| 官方 series page | [ISSRE official GitHub pages / annual sites](https://issre.github.io/) |
| DBLP venue page | [DBLP ISSRE index](https://dblp.org/db/conf/issre/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `2015 IEEE 26th International Symposium on Software Reliability Engineering, ISSRE 2015`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 source-list / proceedings / book-series 证据链完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:20` |

## 2. Scope 与方向

ISSRE 聚焦软件可靠性、测试、质量保障、故障预测、可靠 AI/ML 系统和经验研究；本库必须区分 research、industry、tool、workshop 和 artifact 口径。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 可靠性需求与系统行为建模可为状态机需求建模提供案例。 |
| P2 | 🟢 高 | 可靠性场景、故障模型、测试 oracle 和性质生成相关。 |
| P3 | 🟢 高 | 可靠性评估、验证/测试 profile 与 benchmark 相关。 |
| P4 | 🟢 高 | 缺陷定位、修复、回归测试和可靠性提升与 P4 相关。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [ISSRE official GitHub pages / annual sites](https://issre.github.io/) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-06-05 09:15` |
| DBLP venue page | [DBLP ISSRE index](https://dblp.org/db/conf/issre/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| 最新年度入口 | [ISSRE 2026](https://cyprusconferences.org/issre2026/) | 2027 仅有 future edition / Macau 线索，尚无可写 deadline 的官方 CFP；2028/2029+ 已检索未公布 | `2026-07-13 13:30` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Leonardo Mariani | ISSRE 2026 General Chair | University of Milano-Bicocca | [ISSRE 2026 Organizing Committee](https://cyprusconferences.org/issre2026/organizing-committee/) | [DBLP](https://dblp.org/pid/27/2914.html) | software testing、runtime monitoring、software reliability、program analysis | [DBLP 论文入口](https://dblp.org/pid/27/2914.html) | P2/P3/P4：可靠性场景、运行时监控、缺陷定位与修复验证。 | 🟡 部分核验 | `2026-06-05 11:12` |
| George Papadopoulos | ISSRE 2026 General Chair | University of Cyprus | [ISSRE 2026 Organizing Committee](https://cyprusconferences.org/issre2026/organizing-committee/) | [个人主页](https://www.cs.ucy.ac.cy/~george/) | distributed systems、software engineering、coordination / service-oriented systems | [个人主页 publications / CV 入口](https://www.cs.ucy.ac.cy/~george/) | P2/P3：分布式系统可靠性与验证场景。 | 🟡 部分核验 | `2026-06-05 11:12` |
| Domenico Cotroneo | ISSRE 2026 Research Program Committee Chair | UNC Charlotte | [ISSRE 2026 Research Track Committee](https://cyprusconferences.org/issre2026/research-track-committee/) | [个人主页](https://webpages.charlotte.edu/dcotrone/) / [DBLP](https://dblp.org/pid/c/DomenicoCotroneo.html) | software reliability、dependability、software security、fault injection | [个人主页 publications](https://webpages.charlotte.edu/dcotrone/) / [DBLP 论文入口](https://dblp.org/pid/c/DomenicoCotroneo.html) | P2/P3/P4：可靠性 profile、故障模型、缺陷复现与修复验证。 | 🟡 部分核验 | `2026-06-05 11:43` |
| Jie M. Zhang | ISSRE 2026 Research Program Committee Chair | King's College London | [ISSRE 2026 Research Track Committee](https://cyprusconferences.org/issre2026/research-track-committee/) | [KCL profile](https://www.kcl.ac.uk/people/jie-zhang) | software testing、software engineering for AI、program analysis、ML trustworthiness | [KCL publications / profile](https://www.kcl.ac.uk/people/jie-zhang) | P2/P3/P4：AI 系统测试、性质/场景生成和修复评估。 | 🟡 部分核验 | `2026-06-05 11:12` |
| Fumio Machida | ISSRE 2026 Program Board；Artifact Evaluation Chair | University of Tsukuba | [ISSRE 2026 Research Track Committee](https://cyprusconferences.org/issre2026/research-track-committee/) / [Organizing Committee](https://cyprusconferences.org/issre2026/organizing-committee/) | [DBLP](https://dblp.org/pid/91/9246.html) | software reliability、dependability、cloud/service systems | [DBLP 论文入口](https://dblp.org/pid/91/9246.html) | P2/P3：可靠性 profile、artifact evaluation 与验证/测试场景。 | 🟡 部分核验 | `2026-06-05 11:12` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ISSRE index](https://dblp.org/db/conf/issre/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | 🟦 已有线索 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP ISSRE index](https://dblp.org/db/conf/issre/index.html) | 未公布 | 未公布 | 未公布 | 未公布（Macau 线索待官方 CFP / 年度页确认） | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟣 通知后 | [ISSRE 2026](https://cyprusconferences.org/issre2026/) | [CFP](https://cyprusconferences.org/issre2026/cfp-research/) | [Important Dates](https://cyprusconferences.org/issre2026/dates/) | [Submission](https://easychair.org/conferences/?conf=issre2026) | 未公布 | 未公布 | [DBLP ISSRE index](https://dblp.org/db/conf/issre/index.html) | 2026-04-24 待补时刻 AoE | 2026-04-24 待补时刻 AoE | 2026-07-08 待补时刻 AoE | 2026-10-20..2026-10-23 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [ISSRE 2025](https://issre.github.io/2025/) | [CFP](https://issre.github.io/2025/calls_cfp-research.html) | 未公布 | 未公布 | [Program / Accepted](https://issre.github.io/2025/program_research.html) | 未公布 | [DBLP](https://dblp.org/db/conf/issre/index.html) | 未公布 | 未公布 | 未公布 | 2025 待补精确日期 | 官方 statistics 待拆 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [ISSRE 2024](https://issre.github.io/2024/) | 未公布 | [Important Dates](https://issre.github.io/2024/important-dates.html) | 未公布 | [Program / Accepted](https://issre.github.io/2024/program_full_program.html) | 未公布 | [DBLP](https://dblp.org/db/conf/issre/index.html) | 未公布 | 未公布 | 未公布 | 2024 待补精确日期 | DBLP/IEEE 待拆 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [ISSRE 2023](https://issre.github.io/2023/) | 未公布 | [Important Dates](https://issre.github.io/2023/important-dates.html) | 未公布 | [Program / Accepted](https://issre.github.io/2023/program_research.html) | 未公布 | [DBLP](https://dblp.org/db/conf/issre/index.html) | 未公布 | 未公布 | 未公布 | 2023 待补精确日期 | DBLP/IEEE 待拆 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [ISSRE 2022](https://issre2022.github.io/) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/issre/index.html) | 未公布 | 未公布 | 未公布 | 2022 待补精确日期 | DBLP/IEEE 待拆 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 均已做公开入口检索；2027 仅保留 future edition / Macau 线索，尚无官方年度主页 / CFP / Important Dates 可写 deadline；未公布年度保留占位与核查记录，不预设 CFP。
- 2028 计数口径：未发现 ISSRE 2028 官方年页。
- 2027 计数口径：未发现 ISSRE 2027 官方年页；Macau 线索不等同于 CFP / dates。
- 2026 计数口径：Research track 包含 RES/PER/TAR；industry/tool/workshop 不混入 research count；Research CFP 当前把旧 abstract / paper deadline 延展到 `2026-04-24 AoE`，notification 已于 `2026-07-08` 过去，下一主链节点为 `2026-08-19 待补时刻 AoE` camera-ready。
- 2025 计数口径：已知 official statistics 页面线索，需补 research / industry / tool 拆分。
- 2022 计数口径：CFP/program 子路径待补；当前只把官方年页作为稳定入口。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把 2025--2027 年可核验的主要 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度时间线与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:25:00` | 常态化刷新：2026 行事实无变更（四个主轨日期与官方逐字一致，program / accepted 官方仍为 `TBA`）；同轮在年度页补入此前缺失的三个主链节点（Author Rebuttal Period `2026-06-05..06-09`、Decisions and Early Notification `2026-06-15`、Author Revision Period `2026-06-16..07-03`）与 `cyprusconferences.org` 的 UA 型 bot 过滤陷阱（裸 curl 返回 404、浏览器 UA 返回 200）。 |
| `2026-07-13 13:30:00` | 常态化刷新 ISSRE：将 2026 阶段改为通知后，Important Dates 绑定官方 dates 页并保留 camera-ready `2026-08-19 AoE`；2027 仅记录 Macau future-edition 线索、无 CFP / dates。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 11:43` | 收尾复审后补强 Domenico Cotroneo 学术入口：保留官方 committee 角色源，并把个人主页作为 DBLP author page 的 fallback。 |
| `2026-06-05 11:12` | 修复 ISSRE 2026 复审问题：把 abstract / paper deadline 统一为官方 extended 后的 2026-04-24 AoE，阶段改为复审中，并用官方 organizing / research track committee 页面回填核心人员角色来源。 |
| `2026-06-05 10:04` | 根据复审把 ISSRE 核心人员从“官方角色来源”降级为学术线索 / 官方角色页待补，避免用年度主页或 404/非 committee 页支撑人员角色。 |
| `2026-06-05 09:15` | PR-3 初始化 ISSRE venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
