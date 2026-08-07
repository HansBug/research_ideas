# RV README

> 信息更新时间：`2026-07-13 10:27:51`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | RV |
| 全称 | International Conference on Runtime Verification |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / P2 邻近观察 |
| CCF 等级 | 🥉 |
| 本库目录 | `conf-c-rv` |
| 出版方 | Springer LNCS / Runtime Verification official pages |
| 官方 series page | [RV series](https://runtime-verification.github.io/events/) |
| 官方当前 / 最新年度主页 | [RV 2026](https://rv2026.smithengineering.queensu.ca/) |
| 官方 CFP / Important Dates 总入口 | [RV 2026 dates](https://rv2026.smithengineering.queensu.ca/cfp/) |
| 官方 proceedings / paper list 总入口 | [DBLP / proceedings fallback](https://dblp.org/db/conf/rv/index.html) |
| DBLP venue page | [DBLP RV index](https://dblp.org/db/conf/rv/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF 🥉 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🔴 | 已检索 Elsevier 官方 Compendex source list，未取得 RV / Runtime Verification 可用官方行级证据；LNCS 泛线索不得写成会议收录事实 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本轮按 `SERIALS` / `NON-SERIALS` 与会议全称、缩写、proceedings title 交叉检索，未获可审计匹配行 | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 Compendex source-list 字段、book-series 线索和缩写碰撞规则完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:45` |

## 2. Scope 与方向

RV 聚焦 runtime verification、monitoring、temporal logic、runtime observers 和形式化验证工具，是 P3 模型检查 / 运行时验证的邻近观察 venue。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 🟡 中：监控器、状态机和运行时模型可为状态机建模提供形式化约束素材。 |
| P2 | 🟢 高 | 🟢 高：runtime properties、monitor synthesis、temporal logic 直接关联待验证性质。 |
| P3 | 🟢 高 | 🟢 高：运行时验证是验证剖面和模型检查补链。 |
| P4 | 🟡 中 | 🟡 中：counterexample / monitor feedback 可作为修复线索。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [RV series](https://runtime-verification.github.io/events/) | 年度事实仍以年度主页 / CFP / committee 为准 | `2026-06-05 17:23` |
| Latest year homepage | [RV 2026](https://rv2026.smithengineering.queensu.ca/) | 2027/2028 已于 2026-07-13 复查；未公布则保留占位 | `2026-07-13 10:27:51` |
| CFP / Important Dates | [RV 2026 dates](https://rv2026.smithengineering.queensu.ca/cfp/) | 历史年度在年度 README 展开 | `2026-06-05 17:23` |
| Submission system | [2026 submission](https://easychair.org/conferences?conf=rv2026) | 投稿系统可能按 track 拆分；年度页保留具体入口 | `2026-06-05 17:23` |
| Program / accepted papers | [2026 program](https://rv2026.smithengineering.queensu.ca/program/) | 已结束年度优先官方 program / accepted；缺失时用 DBLP fallback | `2026-06-05 17:23` |
| Proceedings | [Proceedings入口](https://link.springer.com/book/10.1007/978-3-032-05435-7) | 出版商 / proceedings DOI 优先；受限时记录 WAF / 已检索未获可审计证据 | `2026-06-05 17:23` |
| DBLP venue | [DBLP venue](https://dblp.org/db/conf/rv/index.html) | 仅作论文名录 / 计数 fallback | `2026-06-05 17:23` |

## 5. 核心人员情报

> 核心人员情报优先来自官方 organizing / committee / track 页面；研究方向和代表作入口来自个人主页、机构页、DBLP 或公开学术入口。P2 venue 的人员表只记录投稿分流和研究社区画像所需的代表性 leadership，不扩展为全量 PC roster。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sean Kauffman | 2026 / General Chair | General Chair | Queen’s University | [官方角色来源](https://rv2026.smithengineering.queensu.ca/committees/) | [学术入口](https://dblp.org/search?q=Sean%20Kauffman%20runtime%20verification) | runtime verification / engineering systems line (待补个人主页) | [论文入口](https://dblp.org/search?q=Sean%20Kauffman%20runtime%20verification) | P3：运行时验证组织线索 | 🟡 部分核验 | `2026-06-05 17:53` |
| Giulia Pedrielli | 2026 / General Chair | General Chair | Arizona State University | [官方角色来源](https://rv2026.smithengineering.queensu.ca/committees/) | [学术入口](https://dblp.org/pid/91/3600.html) | simulation, stochastic systems, engineering systems | [论文入口](https://dblp.org/pid/91/3600.html) | P3：系统验证与仿真邻近 | 🟡 部分核验 | `2026-06-05 17:53` |
| Ezio Bartocci | 2025 / General Chair | General Chair | TU Wien | [官方角色来源](https://rv25.isec.tugraz.at/?page_id=12) | [学术入口](https://dblp.org/pid/75/3690.html) | runtime verification, monitoring, cyber-physical systems | [论文入口](https://dblp.org/pid/75/3690.html) | P2/P3：时序性质与监控 | 🟡 部分核验 | `2026-06-05 17:53` |
| Bettina Könighofer | 2025 / Program Chair | Program Chair | Graz University of Technology | [官方角色来源](https://rv25.isec.tugraz.at/?page_id=12) | [学术入口](https://dblp.org/pid/53/7617.html) | formal methods, reactive synthesis, verification | [论文入口](https://dblp.org/pid/53/7617.html) | P2/P3：性质、合成与验证 | 🟡 部分核验 | `2026-06-05 17:53` |
| Hazem Torfah | 2025 / Program Chair | Program Chair | Chalmers / University of Gothenburg | [官方角色来源](https://rv25.isec.tugraz.at/?page_id=12) | [学术入口](https://dblp.org/pid/179/7817.html) | runtime verification, temporal logic, monitoring | [论文入口](https://dblp.org/pid/179/7817.html) | P2/P3：monitor 与 temporal logic | 🟡 部分核验 | `2026-06-05 17:53` |
| Erika Abraham | 2024 / PC Chair | PC Chair | RWTH Aachen University | [官方角色来源](https://cmpe.bogazici.edu.tr/rv24/committees/) | [学术入口](https://dblp.org/pid/a/ErikaAbraham.html) | formal methods, SMT, verification | [论文入口](https://dblp.org/pid/a/ErikaAbraham.html) | P3：形式化验证 | 🟡 部分核验 | `2026-06-05 17:53` |
| Houssam Abbas | 2024 / PC Chair | PC Chair | Oregon State University | [官方角色来源](https://cmpe.bogazici.edu.tr/rv24/committees/) | [学术入口](https://dblp.org/pid/11/1012.html) | cyber-physical systems, runtime verification, monitoring | [论文入口](https://dblp.org/pid/11/1012.html) | P2/P3：CPS monitor | 🟡 部分核验 | `2026-06-05 17:53` |
| Thao Dang | 2022 / Program Committee Chair | Program Committee Chair | CNRS / VERIMAG | [官方角色来源](https://rv22.gitlab.io/committees/) | [学术入口](https://dblp.org/pid/d/ThaoDang.html) | hybrid systems, reachability, verification | [论文入口](https://dblp.org/pid/d/ThaoDang.html) | P3：混成系统和验证 | 🟡 部分核验 | `2026-06-05 17:53` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟣 通知后 | [年度主页](https://rv2026.smithengineering.queensu.ca/) | [CFP / track](https://rv2026.smithengineering.queensu.ca/cfp/) | [Dates](https://rv2026.smithengineering.queensu.ca/cfp/) | [Submission](https://easychair.org/conferences?conf=rv2026) | [Program](https://rv2026.smithengineering.queensu.ca/program/) | 未公布 | 未公布 | 未公布 | 2026-06-16 待补时刻 AoE | 2026-08-01 待补时刻 AoE | 2026-10-06..2026-10-09 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [年度主页](https://rv25.isec.tugraz.at/) | [CFP / track](https://rv25.isec.tugraz.at/?page_id=27) | [Dates](https://rv25.isec.tugraz.at/?page_id=27) | [Submission](https://easychair.org/conferences/?conf=rv25) | [Program / accepted](https://rv25.isec.tugraz.at/program/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-032-05435-7) | [DBLP](https://dblp.org/db/conf/rv/rv2025.html) | 未公布 | 2025-06-06 | 2025-07-12 | 2025-09-15..2025-09-19 | DBLP fallback `inproceedings`=27 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [年度主页](https://cmpe.bogazici.edu.tr/rv24/) | [CFP / track](https://cmpe.bogazici.edu.tr/rv24/call-for-papers/) | [Dates](https://cmpe.bogazici.edu.tr/rv24/call-for-papers/) | [Submission](https://easychair.org/conferences/?conf=rv2024) | [Program / accepted](https://cmpe.bogazici.edu.tr/rv24/program/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-74234-7) | [DBLP](https://dblp.org/db/conf/rv/rv2024.html) | 未公布 | 2024-05-28 | 2024-06-25 | 2024-10-15..2024-10-17 | DBLP fallback `inproceedings`=18 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [年度主页](https://rv23.csd.auth.gr/) | [CFP / track](https://rv23.csd.auth.gr/calls) | [Dates](https://rv23.csd.auth.gr/calls) | [Submission](https://easychair.org/conferences/?conf=rv2023) | [Program / accepted](https://easychair.org/smart-program/RV2023/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-44267-4) | [DBLP](https://dblp.org/db/conf/rv/rv2023.html) | 未公布 | 2023-06-04 | 2023-07-07 | 2023-10-03..2023-10-06 | DBLP fallback `inproceedings`=26 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [年度主页](https://rv22.gitlab.io/) | [CFP / track](https://rv22.gitlab.io/cfp/) | [Dates](https://rv22.gitlab.io/cfp/) | [Submission](https://easychair.org/conferences/?conf=rv2022) | [Program / accepted](https://easychair.org/smart-program/RV2022/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-17196-3) | [DBLP](https://dblp.org/db/conf/rv/rv2022.html) | 未公布 | 2022-05-19 | Week 26（具体日期未公布） | 2022-09-28..2022-09-30 | DBLP fallback `inproceedings`=22 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 本目录属于 PR-9 / P2 邻近观察，只服务于检索扩展、投稿分流和社区画像，不把 RV 升级为 P0/P1 主投目标。
- 论文数量优先使用官方 accepted / proceedings；DBLP 只作 fallback，且不得写成 main / research track count。
- Research、industry、tool、artifact、workshop、special session、virtual / live segment 必须分开记录，不能混算。
- 2027/2028 公开信息已检索；未公布年度保留占位，不预造 deadline / committee / proceedings。
- RV 2022 Notification 官方只给 `Week 26`，不得硬落为某一天；仅在根 README / 年度 README / 待补记录保留，不进入 dated TIMELINE / Mermaid。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的年度表格与 Mermaid Gantt。
- 会议 `Conference dates` 也必须进入 TIMELINE 表格和 Mermaid；无日期或未公布事项不得进入 dated Mermaid。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-07-13 10:27:51` | 常态化刷新 RV 2026：按官方 extended dates 更新为已截稿审稿中；2027/2028 保守复查未见官方年度信息。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-06 11:46` | PR #35 近期窗口复审修复：补齐 RV 2026 tutorial proposal submission 与 paper submission 同为 `2026-06-14` AoE，并同步年度页与 TIMELINE。 |
| `2026-06-05 23:06` | 修复冲突后复审问题：RV 2022 Notification 仅有官方 `Week 26`，根表改为具体日期未公布，并同步 TIMELINE 降级为待补记录。 |
| `2026-06-05 18:03` | 修复 PR-9 根 README 一致性：补回核心人员表 `单位` 列，并按 2026-06-05 当前阶段同步 2026 年度状态。 |
| `2026-06-05 17:23` | PR-9 初始化 RV P2 邻近观察 venue README，覆盖 2022--2028 年度索引、核心链接、人员情报、计数口径和待补记录。 |
