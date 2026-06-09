# VMCAI README

> 信息更新时间：`2026-06-09 18:52:22`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | VMCAI |
| 全称 | Verification, Model Checking, and Abstract Interpretation |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 程序语言 / 形式化验证 |
| CCF 等级 | 🥈 |
| 本库目录 | `conf-b-vmcai` |
| 出版方 | Springer LNCS / POPL co-located official pages |
| 官方 series page | [VMCAI official pages on researchr](https://conf.researchr.org/series/VMCAI) |
| DBLP venue page | [DBLP VMCAI index](https://dblp.org/db/conf/vmcai/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；若后续发现 `2029+` 官方 CFP / important dates，必须继续新增年度页 |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🔴 | 已检索 Elsevier 官方 Compendex source list，未取得 VMCAI 可用官方行级证据；相近缩写或 LNCS 泛线索不得写成会议收录事实 | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；本轮按 `SERIALS` / `NON-SERIALS` 与会议全称、缩写、proceedings title 交叉检索，未获可审计匹配行 | `2026-06-09 16:45` |
| 索引核验 | 🟡 | JCR / CAS 不适用；WoS / CPCI 已检索未获单会议行级证据；EI 证据按本表 `🟠 proceedings` / `🟡 book-series` / `🔴 未获行级证据` 解释 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；本轮按 Compendex source-list 字段、book-series 线索和缩写碰撞规则完成保守降级，后续仅在取得行级证据时升级 | `2026-06-09 16:45` |

## 2. Scope 与方向

VMCAI 聚焦验证、模型检查、抽象解释、程序分析和相关工具；因为常与 POPL 共址，年度页必须区分 VMCAI papers、artifact 与 POPL umbrella 信息。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 | 🟡 中 | 程序/模型抽象可为状态机结构化建模提供语义线索。 |
| P2 | 🟢 高 | 抽象解释、性质、反例和验证任务生成相关。 |
| P3 | 🟢 高 | 模型检查与验证 profile 直接相关。 |
| P4 | 🟢 高 | 抽象/refinement 与 verification feedback 可支撑修复。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [VMCAI official pages on researchr](https://conf.researchr.org/series/VMCAI) | 长期入口，年度信息仍以年度页 / CFP 为准 | `2026-06-05 09:15` |
| DBLP venue page | [DBLP VMCAI index](https://dblp.org/db/conf/vmcai/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 09:15` |
| 最新年度入口 | ⏳ 已检索未公布 | `2029+` 已检索未公布；未来年度不得伪造 | `2026-06-05 09:15` |
| 论文集 / 出版商入口 | 未公布 | 历史年度优先用年度 proceedings；缺失时用 DBLP fallback | `2026-06-05 09:15` |

## 5. 核心人员情报

> 核心人员情报优先来自官方组织委员会 / track / steering 页面；研究方向、代表作或近 5 年论文入口来自个人主页、机构页、DBLP 或 ORCID 等公开学术入口。`官方角色来源` 不等同于官方评价研究方向，研究方向列是基于公开资料的整理判断。

| 人员 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Yu-Fang Chen | VMCAI 2026 Organizing Committee | Academia Sinica | [VMCAI 2026 Organizing Committee](https://conf.researchr.org/committee/VMCAI-2026/VMCAI-2026-papers-organizing-committee) | [DBLP](https://dblp.org/pid/05/608.html) | 自动验证、程序分析、模型检查、自动机 | [DBLP 论文入口](https://dblp.org/pid/05/608.html) | P2/P3/P4：验证任务与程序/模型修复。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Ondřej Lengál | VMCAI 2026 Organizing Committee | Brno University of Technology | [VMCAI 2026 Organizing Committee](https://conf.researchr.org/committee/VMCAI-2026/VMCAI-2026-papers-organizing-committee) | [DBLP](https://dblp.org/pid/28/7843.html) | 自动机、形式语言、模型检查、工具 | [DBLP 论文入口](https://dblp.org/pid/28/7843.html) | P1/P2/P3：自动机与形式化验证工具。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Viktor Kunčak | VMCAI 2026 Steering Committee | EPFL | [VMCAI 2026 Steering Committee](https://conf.researchr.org/committee/VMCAI-2026/VMCAI-2026-papers-steering-committee) | [DBLP](https://dblp.org/pid/k/ViktorKuncak.html) | 程序验证、合成、SMT、可证明编程 | [DBLP 近 5 年论文入口](https://dblp.org/pid/k/ViktorKuncak.html) | P2/P3/P4：规格、验证条件和修复综合。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Sriram Sankaranarayanan | VMCAI 2026 Steering Committee | University of Colorado Boulder | [VMCAI 2026 Steering Committee](https://conf.researchr.org/committee/VMCAI-2026/VMCAI-2026-papers-steering-committee) | [DBLP](https://dblp.org/pid/69/104.html) | hybrid systems、program analysis、abstract interpretation、verification | [DBLP 论文入口](https://dblp.org/pid/69/104.html) | P1/P3：控制/混成系统建模与验证。 | 🟡 部分核验 | `2026-06-05 10:04` |
| Arie Gurfinkel | verification tools 学术线索 / VMCAI 官方角色页待补 | University of Waterloo | 官方 VMCAI 2026 organizing / program / steering 抽查未匹配；待补直达角色页 | [DBLP](https://dblp.org/pid/75/766.html) | Horn solving、software model checking、verification tools | [DBLP 论文入口](https://dblp.org/pid/75/766.html) | P2/P3/P4：验证器、约束和反例。 | ⏳ 待核验 | `2026-06-05 10:04` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP VMCAI index](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP VMCAI index](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟡 已通知 / 待会期 | [VMCAI 2026](https://conf.researchr.org/home/VMCAI-2026) | [CFP](https://conf.researchr.org/track/VMCAI-2026/VMCAI-2026-papers) | [Important Dates](https://conf.researchr.org/dates/VMCAI-2026) | 未公布 | [Program / Accepted](https://conf.researchr.org/program/VMCAI-2026/program-VMCAI-2026/) | 未公布 | [DBLP](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 2025-09-15 待补时刻 | 2025-11-06 待补时刻 | 2026-01-12..2026-01-13 | 未公布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [VMCAI 2025](https://conf.researchr.org/home/VMCAI-2025) | 未公布 | [Important Dates](https://conf.researchr.org/dates/VMCAI-2025) | 未公布 | [Program / Accepted](https://conf.researchr.org/program/VMCAI-2025/program-VMCAI-2025/) | [Proceedings](https://dblp.org/rec/conf/vmcai/2025-1) | [DBLP](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 2024-10-01 待补时刻 | 2024-11-11 待补时刻 | 2025-01-20..2025-01-21 | DBLP Part I/II 待拆 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [VMCAI 2024](https://conf.researchr.org/home/VMCAI-2024) | 未公布 | [Important Dates](https://conf.researchr.org/dates/VMCAI-2024) | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 2023-09-07 待补时刻 | 2023-10-11 待补时刻 | 2024-01-15..2024-01-16 | Springer/DBLP 待拆 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [VMCAI 2023](https://conf.researchr.org/home/VMCAI-2023) | 未公布 | [Important Dates](https://conf.researchr.org/dates/VMCAI-2023) | 未公布 | 未公布 | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-24950-1) | [DBLP](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 2022-09-15 待补时刻 | 2022-10-21 待补时刻 | 2023-01-16..2023-01-17 | Springer/DBLP 待拆 | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [VMCAI 2022](https://conf.researchr.org/home/VMCAI-2022) | 未公布 | [Important Dates](https://conf.researchr.org/dates/VMCAI-2022) | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/vmcai/index.html) | 未公布 | 2021-09-09 待补时刻 | 2021-10-11 待补时刻 | 2022-01-16..2022-01-18 | Springer/DBLP 待拆 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / main conference、tool、artifact、industry、workshop、co-located event 不得混算。
- `2027`、`2028` 与 `2029+` 均已做公开入口检索；未公布年度保留占位与核查记录，不预设 CFP。
- 2028 计数口径：未发现 VMCAI 2028 官方年页。
- 2027 计数口径：未发现 VMCAI 2027 官方年页。
- 2026 计数口径：2026 proceedings / DBLP 尚未稳定落地。
- 2025 计数口径：Part I/II 需拆 paper category；不与 POPL umbrella 混算。
- 2024 计数口径：artifact 与 research papers 分列待补。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-3 已把 2025--2027 年可核验的主要 dated events 并入 [TIMELINE.md](../TIMELINE.md) 的正式年度时间线与 Mermaid；历史年度未完全补齐的 deadline 留在各年度 README 待后续精查。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 18:52:22` | PR #91 终态收口：将索引核验行从复核动作改为已完成证据链与后续升级条件，避免把本轮证据核验责任留作未闭合动作。 |
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 10:04` | 根据复审修正 VMCAI 核心人员角色来源：Organizing / Steering 分页引用，Arie Gurfinkel 降级为学术线索与官方角色页待补。 |
| `2026-06-05 09:15` | PR-3 初始化 VMCAI venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
