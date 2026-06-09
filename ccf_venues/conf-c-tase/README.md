# TASE README

> 信息更新时间：`2026-06-09 13:52`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | TASE |
| 全称 | International Symposium on Theoretical Aspects of Software Engineering |
| 类型 | 会议 |
| CCF 大类 | [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) |
| CCF 等级 | C（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版方 | Springer LNCS / TASE official annual sites |
| 官方 series page | 未发现稳定独立官方 series page；使用最新年度主页与 DBLP index 共同作为入口 |
| 官方当前 / 最新年度主页 | [TASE 2026](https://tase2026.github.io/) |
| 官方 CFP / Important Dates 总入口 | 逐年度主页 / CFP 分散维护；见 §6 年度信息汇总 |
| 官方 proceedings / paper list 总入口 | 历史年度见 proceedings / DBLP fallback；见 §6 |
| DBLP venue page | [DBLP TASE](https://dblp.org/db/conf/tase/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 未发现官方 CFP / important dates |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥉 | CCF C 级；emoji 已按 GUIDE 的 A/B/C 口径编码，不再统一写成黄色 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `Proceedings - 11th International Symposium on Theoretical Aspects of Software Engineering, TASE 2017`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

- 官方 scope 摘要：TASE 聚焦 theoretical aspects of software engineering、formal methods、software dependability、CPS、AI-embedded systems、security / privacy、specification、verification 和 program analysis。
- 与本仓库最相关的方向：质量 / 可靠性 / 形式化方法 / verification / testing / theoretical software engineering。
- 明显不属于本仓库重点的方向：纯管理、纯网络安全运营、与软件工程建模 / 验证无关的泛安全工程条目。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中相关 | 中相关：形式化 DSL、状态机语义、建模工具与可执行规约可作为理论支撑。 |
| P2 场景与性质生成 | 强相关 | 强相关：规约、性质、逻辑与验证条件生成直接相关。 |
| P3 验证剖面与模型检查 | 强相关 | 强相关：model checking、formal verification、CPS verification 是核心方向。 |
| P4 模型修复 | 强相关 | 强相关：verification-guided repair、program synthesis 和 proof / counterexample feedback 可作为修复方法线索。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | 未发现稳定独立官方 series page；使用最新年度主页与 DBLP index 共同作为入口 | 年度事实仍以年度主页 / CFP 为准 | `2026-06-05 18:05` |
| Latest year homepage | [TASE 2026](https://tase2026.github.io/) | 最新可核验年度入口 | `2026-06-05 18:05` |
| CFP / Call for Papers | 见 §6 各年度 CFP | 年度 CFP 分散，不能用最新 CFP 替代历史年度 | `2026-06-05 18:05` |
| Important Dates | 见 §6 各年度 important dates | 官方只给日期时写 `待补时刻` | `2026-06-05 18:05` |
| Submission system | 见 §6 各年度 submission / EasyChair / SoftConf | 历史投稿入口可能关闭或需登录 | `2026-06-05 18:05` |
| Program / accepted papers | 见 §6 各年度 program / accepted | 缺失时写 `未公布` / `待补`，不得用 DBLP 冒充官方 accepted list | `2026-06-05 18:05` |
| Proceedings | 见 §6 各年度 proceedings | Springer / IEEE / DOI / DBLP fallback | `2026-06-05 18:05` |
| DBLP venue | [DBLP TASE](https://dblp.org/db/conf/tase/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 18:05` |

## 5. 核心人员情报

本节记录会议核心人员，不要求全量 PC roster。`官方角色来源` 必须能直接支撑“姓名 + 年度 / 层级 + 角色”；研究方向与代表作由 DBLP / 个人主页补充。

| 姓名 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Geguang Pu | TASE 2026 General Chair | East China Normal University | [官方角色来源](https://tase2026.github.io/c_chair.html) | [DBLP](https://dblp.org/pid/80/5539.html) | formal methods、model checking、software verification | DBLP 近年论文入口 | P2/P3：模型检查与形式化验证 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Giuseppe De Giacomo | TASE 2026 Program Co-Chair | University of Oxford / Sapienza 线索 | [官方角色来源](https://tase2026.github.io/c_chair.html) | [DBLP](https://dblp.org/pid/16/4220.html) | logic in AI、planning、formal methods | DBLP 近年论文入口 | P2/P3：逻辑规约与验证 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Jianwen Li | TASE 2026 Program Co-Chair | Chinese Academy of Sciences 线索 | [官方角色来源](https://tase2026.github.io/c_chair.html) | [DBLP](https://dblp.org/pid/87/9388.html) | formal verification、automata、model checking | DBLP 近年论文入口 | P2/P3：自动机与验证 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Jifeng He | TASE 2026 Steering Committee | East China Normal University / Oxford 线索 | [官方角色来源](https://tase2026.github.io/c_chair.html) | [DBLP](https://dblp.org/pid/h/JifengHe.html) | formal methods、theoretical CS、software engineering theory | DBLP 近年论文入口 | P1/P2/P3：理论软工与形式化方法 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Michael Hinchey | TASE 2026 Steering Committee | University of Limerick 线索 | [官方角色来源](https://tase2026.github.io/c_chair.html) | [DBLP](https://dblp.org/pid/h/MichaelGHinchey.html) | formal methods、autonomous systems、software engineering | DBLP 近年论文入口 | P1/P3：可靠软件与工具链 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Shengchao Qin | TASE 2026 Steering Committee | Teesside University 线索 | [官方角色来源](https://tase2026.github.io/c_chair.html) | [DBLP](https://dblp.org/pid/77/1982.html) | program verification、formal methods、separation logic | DBLP 近年论文入口 | P3/P4：验证与修复线索 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/tase/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/tase/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟡 已通知 / 待会期 | [TASE 2026](https://tase2026.github.io/) | [CFP](https://tase2026.github.io/c_cfp.html) | [Important Dates](https://tase2026.github.io/c_impd.html) | [Submission](https://tase2026.github.io/c_subins.html) | [Program / Accepted](https://tase2026.github.io/c_ap.html) | 未公布；官网说明 planned Springer LNCS | [DBLP](https://dblp.org/db/conf/tase/index.html) | 2026-03-01 待补时刻 | 2026-03-07 待补时刻 | 2026-04-18 待补时刻 | 2026-07-04..2026-07-06 | 官方 accepted 表 28 papers；Springer / DBLP 2026 入口尚未发布 | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [TASE 2025](https://cyprusconferences.org/tase2025/) | [CFP](https://cyprusconferences.org/tase2025/call-for-papers/) | [Important Dates](https://cyprusconferences.org/tase2025/call-for-papers/) | [Submission](https://cyprusconferences.org/tase2025/submission/) | [Program / Accepted](https://cyprusconferences.org/tase2025/accepted-papers/) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-98208-8) | [DBLP](https://dblp.org/db/conf/tase/tase2025.html) | 2025-03-01 待补时刻 AoE | 2025-03-08 待补时刻 AoE | 2025-04-05 待补时刻 AoE | 2025-07-14..2025-07-16 | 官方 accepted list：21 contributed papers；Springer about：20 full + 1 short + 2 invited papers from 66 submissions；DBLP `inproceedings`：22；Springer TOC 是否排除 invited abstract / front matter 待逐项复核 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [TASE 2024](https://tase2024.github.io/) | [CFP](https://tase2024.github.io/c_cfp.html) | [Important Dates](https://tase2024.github.io/c_impd.html) | [Submission](https://tase2024.github.io/c_subins.html) | [Program / Accepted](https://tase2024.github.io/c_ap.html) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-64626-3) | [DBLP](https://dblp.org/db/conf/tase/tase2024.html) | 2024-02-27 待补时刻 AoE | 2024-03-05 待补时刻 AoE | 2024-04-10 待补时刻 | 2024-07-29..2024-08-01 | 官方 accepted 表 26 contributed papers；Springer TOC 28 papers，含 invited / invited abstract，需标明口径 | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [TASE 2023](https://plrg-bristol.github.io/tase2023/) | [CFP](https://plrg-bristol.github.io/tase2023/cfp.html) | [Important Dates](https://plrg-bristol.github.io/tase2023/cfp.html) | [Submission](https://plrg-bristol.github.io/tase2023/submit.html) | [Program / Accepted](https://plrg-bristol.github.io/tase2023/accepted-papers.html) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-35257-7) | [DBLP](https://dblp.org/db/conf/tase/tase2023.html) | 2023-02-17 待补时刻 | 2023-02-24 待补时刻 | 2023-04-10 待补时刻 | 2023-07-04..2023-07-06 | 官方 accepted 表 21 行；Springer TOC 21 papers；Springer about 写 19 full + 2 short from 49 submissions | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [TASE 2022](https://www.cs.ubbcluj.ro/tase2022/) | [CFP](https://www.cs.ubbcluj.ro/tase2022/c_cfp.html) | [Important Dates](https://www.cs.ubbcluj.ro/tase2022/c_impd.html) | [Submission](https://www.cs.ubbcluj.ro/tase2022/c_subins.html) | [Program / Accepted](https://www.cs.ubbcluj.ro/tase2022/c_ap.html) | [Proceedings](https://link.springer.com/book/10.1007/978-3-031-10363-6) | [DBLP](https://dblp.org/db/conf/tase/tase2022.html) | 2022-02-14 待补时刻 AoE | 2022-02-27 待补时刻 AoE | 2022-04-10 待补时刻 | 2022-07-08..2022-07-10 | 官方 accepted 表 27 行；Springer TOC 27 papers；Springer about 写 21 regular + 5 short，另含 invited，需标明口径 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- 已结束年度优先使用官方 accepted papers / program / proceedings；若只能用 DBLP，必须显式标注 fallback。
- Research / regular、short、industry、workshop、fast abstract、poster、invited、companion proceedings 不得混算。
- 2027、2028 与 2029+ 均已做公开入口检索；未公布年度保留占位与核查记录，不预设 CFP。
- 会议 dated events 已同步 [../TIMELINE.md](../TIMELINE.md)；若后续修改任何 deadline / 会期，必须同步 TIMELINE 表格与 Mermaid。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [../TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [../TIMELINE.md](../TIMELINE.md) 的对应事件表与 Mermaid Gantt。
- 当前 PR-8 已把 2022--2026 年可核验的主要 dated events 并入 [../TIMELINE.md](../TIMELINE.md) 的正式年度时间线与 Mermaid；2027/2028 未公布，不造日期。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-05 18:05` | PR-8 初始化 TASE venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
