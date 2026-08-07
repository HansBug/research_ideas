# CAV README

> 信息更新时间：`2026-08-07 20:15:00`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | CAV |
| 全称 | International Conference on Computer Aided Verification |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 形式化验证 |
| CCF 等级 | 🏆 |
| 本库目录 | `conf-a-cav` |
| 出版方 | Springer LNCS / CAV 官方年度页 |
| 官方 series page | [CAV official series](https://conferences.i-cav.org/) |
| 官方当前 / 最新年度主页 | [CAV 2026](https://conferences.i-cav.org/2026/)；2027/2028 于 2026-07-13 复查仍未获正式 CFP / dates |
| 官方 CFP / Important Dates 总入口 | [CAV 2026 CFP](https://conferences.i-cav.org/2026/cfp/) |
| DBLP venue page | [DBLP CAV index](https://dblp.org/db/conf/cav/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🏆 | CCF 🏆 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🔴 | 已检索 Elsevier 官方 Compendex source list，未取得 CAV 可用官方行级证据；检到的 `CAVS/EDCAV` 属于缩写碰撞或其他会议，不能作为 CAV 证据 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本轮按 `SERIALS` / `NON-SERIALS` 与会议全称、缩写、proceedings title 交叉检索，未获可审计匹配行 | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 Compendex source-list 字段、book-series 线索和缩写碰撞规则完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:45` |

## 2. Scope 与方向

CAV 聚焦计算机辅助验证、模型检查、SMT/SAT、程序验证、系统验证、工具、artifact evaluation 与验证 benchmark；本库严格区分 main/research、tool、artifact、workshop 和 co-located events。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 自动机、状态空间建模、验证模型抽象是间接支撑。 |
| P2 | 🟢 高 | 验证性质、反例、benchmark、specification 与验证任务生成高度相关。 |
| P3 | 🟢 高 | 模型检查和计算机辅助验证是 P3 的核心理论/工具来源。 |
| P4 | 🟢 高 | CEGAR、witness、counterexample 与 repair/debugging 相关。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [CAV official series](https://conferences.i-cav.org/) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-07-13 19:13:21` |
| DBLP venue page | [DBLP CAV index](https://dblp.org/db/conf/cav/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| Latest year homepage | [CAV 2026](https://conferences.i-cav.org/2026/) | 2027/2028 于 2026-07-13 复查仍未获正式年度主页 / CFP / dates；未来年度不得伪造 | `2026-07-13 19:13:21` |
| CFP / Important Dates | [CAV 2026 CFP](https://conferences.i-cav.org/2026/cfp/) | main conference paper chain；artifact evaluation 单列，不混入主论文口径 | `2026-07-13 19:13:21` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Anthony W. Lin | CAV 2026 Program Chair | TU Kaiserslautern / RPTU | [CAV 2026 Organization](https://conferences.i-cav.org/2026/organization/) | [DBLP](https://dblp.org/pid/13/5716.html) | 自动机、逻辑、验证、程序分析 | [DBLP 近年论文入口](https://dblp.org/pid/13/5716.html) | P2/P3：自动机和逻辑验证任务。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Eva Darulova | CAV 2026 Program Chair | MPI-SWS / Saarland 相关公开资料 | [CAV 2026 Organization](https://conferences.i-cav.org/2026/organization/) | [DBLP](https://dblp.org/pid/93/9120.html) | 数值程序验证、可靠计算、程序分析 | [DBLP 论文入口](https://dblp.org/pid/93/9120.html) | P3/P4：数值控制软件验证与修复诊断。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Philipp Rümmer | CAV 2026 Organizing / PC leadership | University of Regensburg | [CAV 2026 Organization](https://conferences.i-cav.org/2026/organization/) | [DBLP](https://dblp.org/pid/r/PhilippRummer.html) | SMT、Horn clauses、程序验证、自动化推理 | [DBLP 论文入口](https://dblp.org/pid/r/PhilippRummer.html) | P2/P3/P4：性质约束、验证器与 counterexample。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Corina S. Păsăreanu | CAV / verification community 核心人员 | Carnegie Mellon University / NASA Ames | [CAV 2026 Organization](https://conferences.i-cav.org/2026/organization/) | [DBLP](https://dblp.org/pid/03/4368.html) | symbolic execution、software model checking、autonomous systems verification | [DBLP 近 5 年论文入口](https://dblp.org/pid/03/4368.html) | P1/P2/P3：场景生成、假设生成与学习系统验证。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Dirk Beyer | CAV / TACAS verification tools 核心人员 | LMU Munich | [CAV 2026 Organization](https://conferences.i-cav.org/2026/organization/) | [DBLP](https://dblp.org/pid/b/DirkBeyer1.html) | 软件验证、model checking、SV-COMP/Test-Comp、witness | [DBLP 论文入口](https://dblp.org/pid/b/DirkBeyer1.html) | P2/P3/P4：验证证据链、benchmark 与 witness。 | 🟡 部分核验 | `2026-06-05 09:15` |
| Joost-Pieter Katoen | CAV / model checking 核心人员 | RWTH Aachen University | [CAV 2026 Organization](https://conferences.i-cav.org/2026/organization/) | [DBLP](https://dblp.org/pid/k/JoostPieterKatoen.html) | probabilistic model checking、MDP、quantitative verification | [DBLP 近 5 年论文入口](https://dblp.org/pid/k/JoostPieterKatoen.html) | P2/P3：概率/定量验证 profile。 | 🟡 部分核验 | `2026-06-05 09:15` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP CAV index](https://dblp.org/db/conf/cav/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | 🟢 投稿中 | [CAV 2027](https://conferences.i-cav.org/2027/) | [CFP](https://conferences.i-cav.org/2027/cfp/) | [CFP / Dates](https://conferences.i-cav.org/2027/cfp/) | ⏳ 已检索未公布 | 未公布 | 未公布 | [DBLP CAV index](https://dblp.org/db/conf/cav/index.html) | 未公布 | 2027-01-20 23:59 AoE | 2027-04-23 待补时刻 AoE | 2027-07-19..2027-07-23 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | ✅ 已结束 / 待 proceedings | [CAV 2026](https://conferences.i-cav.org/2026/) | [CFP](https://conferences.i-cav.org/2026/cfp/) | [Important Dates](https://conferences.i-cav.org/2026/cfp/) | [Submission](https://submissions.floc26.org/cav/) | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/cav/index.html) | 未公布 | 2026-01-28 待补时刻 AoE | 2026-04-17 待补时刻；camera-ready 2026-05-15 待补时刻 | 2026-07-26..2026-07-29 | Research Papers 55 + Tool Papers 20 + Industrial Experience Reports or Case Studies 6 = 81（官方 accepted 页分类计数） | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [CAV 2025](https://conferences.i-cav.org/2025/) | [CFP](https://conferences.i-cav.org/2025/cfp/) | [Important Dates](https://conferences.i-cav.org/2025/cfp/) | 未公布 | [Program / Accepted](https://conferences.i-cav.org/2025/accepted) | 未公布 | [DBLP](https://dblp.org/db/conf/cav/index.html) | 未公布 | 2025-01-31 待补时刻 | 2025-04-02 待补时刻 | 2025-07-21..2025-07-25 | 官方 accepted 待拆 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [CAV 2024](https://i-cav.org/2024/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-65627-9) | [DBLP](https://dblp.org/db/conf/cav/index.html) | 未公布 | 未公布 | 未公布 | 2024 待补精确日期 | Springer Part I 待拆 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [CAV 2023](https://www.i-cav.org/2023/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-37706-8) | [DBLP](https://dblp.org/db/conf/cav/index.html) | 未公布 | 未公布 | 未公布 | 2023 待补精确日期 | Springer Part I 待拆 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [CAV 2022](https://i-cav.org/2022/) | 未公布 | 未公布 | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-13185-1) | [DBLP](https://dblp.org/db/conf/cav/index.html) | 未公布 | 未公布 | 未公布 | 2022 待补精确日期 | 40 full + 9 tool + 2 case studies | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 于 2026-07-13 复查仍未发现正式官方主页、CFP 或重要日期；未公布年度保留占位与核查记录，不预设 CFP。
- 2026 当前已过 camera-ready，官方会期为 `2026-07-26..2026-07-29`，阶段按 `🔵 会期临近` 记录。
- 2028 计数口径：未检索到 CAV 2028 官方年页 / CFP。
- 2027 计数口径：未检索到 CAV 2027 官方年页 / CFP。
- 2026 计数口径：2026 proceedings / DBLP 年度页尚未落地；不得用 artifact/workshop 混算。
- 2025 计数口径：accepted 页面可用；full/tool/case/artifact 拆分待补。
- 2024 计数口径：旧站路径 / 证书 / 404 风险未获公开可审计正文；Springer Part I 与 DBLP 为稳定 fallback。
- 2023 计数口径：旧站路径未获公开可审计正文；不要把 workshop 混入主会。
- 2022 计数口径：Springer about：209 submissions；workshops/artifacts 不并入该 count。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把 2025--2027 年可核验的主要 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度章节与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:15:00` | 常态化刷新：CAV 2027 官方站 / CFP / artifact / CFW 已全部上线，年度汇总行由 `⏳ 已检索未公布` 升级为 `🟢 投稿中`（submission `2027-01-20 23:59 AoE`，Amsterdam，会期 2027-07-19..23）；CAV 2026 阶段迁移为 `✅ 已结束 / 待 proceedings` 并补入官方 accepted 分类计数 54/20/6=80；记录 `conferences.i-cav.org/` 根 series 页已退化为占位文本、必须直接 probe `/YYYY/`。 |
| `2026-07-13 19:13:21` | 常态化刷新：复核 CAV 2026 会期与阶段，2027/2028 仍未发现正式官方 CFP / dates，仅保守更新复查记录。 |
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 09:15` | PR-3 初始化 CAV venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
