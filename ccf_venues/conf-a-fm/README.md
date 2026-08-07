# FM README

> 信息更新时间：`2026-08-07 20:25:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | FM |
| 全称 | International Symposium on Formal Methods |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 形式化方法 |
| CCF 等级 | 🏆 |
| 本库目录 | `conf-a-fm` |
| 出版方 | Springer LNCS / FM 官方年度页 |
| 官方 series page | [FM Europe / FM official series](https://www.fmeurope.org/) |
| 官方当前 / 最新年度主页 | [FM 2026](https://conf.researchr.org/home/fm-2026)；2027/2028 未发现正式会议主页 / CFP / dates |
| 官方 CFP / Important Dates 总入口 | [FM 2026 Research paper](https://conf.researchr.org/track/fm-2026/fm-2026-research-paper) / [FM 2026 dates](https://conf.researchr.org/dates/fm-2026) |
| DBLP venue page | [DBLP FM index](https://dblp.org/db/conf/fm/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🏆 | CCF 🏆 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟡 | 仅确认 FM 常见 Springer LNCS 出版路径与 LNCS book-series 在 Compendex source list 中；未取得 FM 会议直接 proceedings 行 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），只记录 book-series / publisher-path discovery 线索，不得冒充会议 source-level | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 Compendex source-list 字段、book-series 线索和缩写碰撞规则完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:45` |

## 2. Scope 与方向

FM 是形式化方法主会，覆盖形式化规格、验证、模型检查、精化、证明、工具和工业案例；本库只把稳定官方年度页、Springer proceedings 与 DBLP fallback 写作事实源。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟢 高 | 形式化需求、状态机/自动机建模、精化与规格语言是 FM 的核心素材。 |
| P2 | 🟢 高 | 安全/活性性质、验证任务、场景和反例可从 FM 论文与工业案例中抽取。 |
| P3 | 🟢 高 | 模型检查、定理证明、时序逻辑、工具论文与验证 profile 直接相关。 |
| P4 | 🟡 中 | 反例驱动修复、精化和验证失败诊断可作为修复闭环线索。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [FM Europe / FM official series](https://www.fmeurope.org/) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-07-13 19:13:21` |
| DBLP venue page | [DBLP FM index](https://dblp.org/db/conf/fm/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| Latest year homepage | [FM 2026](https://conf.researchr.org/home/fm-2026) | 2026 已结束；2027/2028 于 2026-07-13 复查仍未发现正式会议主页 / CFP / dates | `2026-07-13 19:13:21` |
| CFP / Important Dates | [FM 2026 Research paper](https://conf.researchr.org/track/fm-2026/fm-2026-research-paper) / [FM 2026 dates](https://conf.researchr.org/dates/fm-2026) | 2027 仅有 organizer call 线索，不等同于正式 CFP | `2026-07-13 19:13:21` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Fuyuki Ishikawa | FM 2026 General Chair | National Institute of Informatics | [FM 2026 Organizing Committee](https://conf.researchr.org/committee/fm-2026/fm-2026-organizing-committee) | [DBLP](https://dblp.org/pid/12/4208.html) | 服务计算、软件工程、形式化/质量保障、AI 系统工程 | [DBLP 近年论文](https://dblp.org/pid/12/4208.html) | P1/P2/P3：面向高可信软件与服务系统的规格、验证和评估。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Augusto Sampaio | FM 2026 Program Co-Chair | Universidade Federal de Pernambuco | [FM 2026 Organizing Committee](https://conf.researchr.org/committee/fm-2026/fm-2026-organizing-committee) | [DBLP](https://dblp.org/pid/06/2085.html) | 形式化方法、CSP、精化、软件工程形式化 | [DBLP 论文入口](https://dblp.org/pid/06/2085.html) | P1/P3/P4：状态机/规约精化与验证驱动修复。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Marielle Stoelinga | FM 2026 Program Co-Chair | University of Twente / Radboud University | [FM 2026 Organizing Committee](https://conf.researchr.org/committee/fm-2026/fm-2026-organizing-committee) | [DBLP](https://dblp.org/pid/s/MarielleStoelinga.html) | 概率风险分析、模型检查、形式化安全与可靠性 | [DBLP 近 5 年论文入口](https://dblp.org/pid/s/MarielleStoelinga.html) | P2/P3：风险/可靠性性质、概率验证场景。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Masaki Waga | FM 2026 Artifact Evaluation Co-Chair | Kyoto University | [FM 2026 Organizing Committee](https://conf.researchr.org/committee/fm-2026/fm-2026-organizing-committee) | [DBLP](https://dblp.org/pid/147/3070.html) | 形式语言、时序逻辑、运行时验证、自动机学习 | [DBLP 论文入口](https://dblp.org/pid/147/3070.html) | P1/P2/P3：自动机、时序性质与验证任务生成。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Anne Haxthausen | FM 2026 Journal-First Track Chair | Technical University of Denmark | [FM 2026 Organizing Committee](https://conf.researchr.org/committee/fm-2026/fm-2026-organizing-committee) | [DBLP](https://dblp.org/pid/h/AnneEHaxthausen.html) | 形式化方法、铁路/控制系统建模、验证 | [DBLP 论文入口](https://dblp.org/pid/h/AnneEHaxthausen.html) | P1/P3：控制系统状态机建模与验证案例。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Étienne André | FM 2026 Artifact Evaluation Co-Chair | Nantes Université | [FM 2026 Organizing Committee](https://conf.researchr.org/committee/fm-2026/fm-2026-organizing-committee) | [DBLP](https://dblp.org/pid/49/2992.html) | 参数时间自动机、模型检查、综合、形式化验证工具 | [DBLP 近 5 年论文入口](https://dblp.org/pid/49/2992.html) | P1/P2/P3/P4：时间自动机、性质生成与验证反馈。 | 🟡 部分核验 | `2026-06-05 10:04` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP FM index](https://dblp.org/db/conf/fm/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | 🟦 主办征集中 | [FM 2027 on researchr（Access denied，正文未取得可审计快照）](https://conf.researchr.org/home/fm-2027) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP FM index](https://dblp.org/db/conf/fm/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | ✅ 已结束 | [FM 2026](https://conf.researchr.org/home/fm-2026) | [CFP](https://conf.researchr.org/track/fm-2026/fm-2026-research-paper) | [Important Dates](https://conf.researchr.org/dates/fm-2026) | [Submission](https://easychair.org/conferences/?conf=fm2026) | [Program / Accepted](https://conf.researchr.org/program/fm-2026/program-fm-2026/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-032-26204-2) | [DBLP](https://dblp.org/db/conf/fm/index.html) | 2025-11-25 待补时刻 | 2025-12-02 待补时刻 | 2026-02-06 待补时刻 | 2026-05-18..2026-05-22 | Part I: 49 full + 2 short | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP FM index](https://dblp.org/db/conf/fm/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-71162-6) | [DBLP](https://dblp.org/db/conf/fm/index.html) | 未公布 | 未公布 | 未公布 | 2024-09-09..2024-09-13 | Springer Part I/II 待拆 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [FM 2023](https://fm2023.isp.uni-luebeck.de/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-27481-7) | [DBLP](https://dblp.org/db/conf/fm/index.html) | 未公布 | 未公布 | 未公布 | 2023-03-06..2023-03-10 | Springer/DBLP 待拆 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP FM index](https://dblp.org/db/conf/fm/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 于 2026-07-13 复查仍未发现正式官方主页、CFP 或重要日期；未公布年度保留占位与核查记录，不预设 CFP。
- 2028：截至 2026-07-13 核查未发现稳定 FM 2028 官方主页、CFP、重要日期或投稿入口。
- 2028 计数口径：未检索到 FM 2028 官方年页 / CFP；只保留年度占位。
- 2027：已检索到官方线索 [FM 2027 organizer call](https://www.fmeurope.org/2025/09/14/fm-2027-call-for-organizers/)；截至 2026-07-13 未发现正式会议主页、CFP、dates、submission、program 或 proceedings。
- 2027 计数口径：FM Europe 只公开 FM 2027 organizer call；不等同于正式 CFP。
- 2026 计数口径：Springer Part I about page count；invited/tutorial/industry 条目不混入 research full/short count。
- 2025：本页保留占位，避免把非主系列或地区性形式化方法活动混作 FM 主会。
- 2025 计数口径：未发现稳定 FM 主系列 2025 edition；不把其他 FM* 活动写作 FM 主会。
- 2024：年度主页待补；已核验到 Springer proceedings 和 DBLP 系列入口。
- 2024 计数口径：当前记录 Springer proceedings 与 DBLP fallback；full/short/industry 精确拆分待补。
- 2023 计数口径：投稿发生在 2022；本页按 edition 记录，会期进入 2023。
- 2022 计数口径：未发现稳定 FM 主系列 2022 edition；保留占位，不伪造年度主页。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把 2025--2027 年可核验的主要 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度时间线与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:25:00` | 常态化刷新：2027 行官方主页由 `⏳ 已检索未公布` 精确化为 **HTTP 200 + `Access denied`**（researchr slug 已建、尚未公开发布，此前为 404），是 CFP 即将放出的强信号，列高频复查；同轮在年度页补入 FM 自 2027 起**改为每年一届、固定秋季**的官方 cadence 变更。仍无正式 CFP / dates / host city。 |
| `2026-07-13 19:13:21` | 常态化刷新：复核 FM 2026 已结束状态；FM 2027/2028 仍无正式 CFP / dates，2027 organizer call 继续保守记录为线索。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 10:04` | 根据复审修正 FM 2026 核心人员官方角色来源为 organizing committee 直达页，并把 FM 2027 organizer call 从“年度主页”降级为官方线索。 |
| `2026-06-05 09:15` | PR-3 初始化 FM venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
