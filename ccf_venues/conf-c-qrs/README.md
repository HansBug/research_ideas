# QRS README

> 信息更新时间：`2026-06-05 18:05`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | QRS |
| 全称 | IEEE International Conference on Software Quality, Reliability and Security |
| 类型 | 会议 |
| CCF 大类 | [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) |
| CCF 等级 | C（[CCF 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)） |
| 出版方 | IEEE / QRS Conference |
| 官方 series page | [Series / latest](https://qrs.techconf.org/) |
| 官方当前 / 最新年度主页 | [QRS 2026](https://qrs26.techconf.org/) |
| 官方 CFP / Important Dates 总入口 | 逐年度主页 / CFP 分散维护；见 §6 年度信息汇总 |
| 官方 proceedings / paper list 总入口 | 历史年度见 proceedings policy / DBLP fallback；见 §6 |
| DBLP venue page | [DBLP QRS](https://dblp.org/db/conf/qrs/index.html) |
| 当前默认调查范围 | `2022` 至 `2028`；`2029+` 未发现官方 CFP / important dates |

## 2. Scope 与方向

- 官方 scope 摘要：QRS 关注 software quality、reliability、security、testing、verification、dependability 和 industry practice；本库必须区分 regular / short、workshop、industry、fast abstract、poster 与 companion proceedings。
- 与本仓库最相关的方向：质量 / 可靠性 / 形式化方法 / verification / testing / theoretical software engineering。
- 明显不属于本仓库重点的方向：纯管理、纯网络安全运营、与软件工程建模 / 验证无关的泛安全工程条目。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中相关 | 中相关：可靠性需求、质量模型、测试模型可作为状态机建模案例。 |
| P2 场景与性质生成 | 强相关 | 强相关：software testing、quality assurance、reliability 场景和 oracle 直接相关。 |
| P3 验证剖面与模型检查 | 强相关 | 强相关：dependability、verification、安全可靠性证据可支撑验证剖面。 |
| P4 模型修复 | 强相关 | 强相关：debugging、fault localization、可靠性改善和 testing feedback 与修复闭环相关。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [Series / latest](https://qrs.techconf.org/) | 年度事实仍以年度主页 / CFP 为准 | `2026-06-05 18:05` |
| Latest year homepage | [QRS 2026](https://qrs26.techconf.org/) | 最新可核验年度入口 | `2026-06-05 18:05` |
| CFP / Call for Papers | 见 §6 各年度 CFP | 年度 CFP 分散，不能用最新 CFP 替代历史年度 | `2026-06-05 18:05` |
| Important Dates | 见 §6 各年度 important dates | 官方只给日期时写 `待补时刻` | `2026-06-05 18:05` |
| Submission system | 见 §6 各年度 submission / EasyChair / SoftConf | 历史投稿入口可能关闭或需登录 | `2026-06-05 18:05` |
| Program / accepted papers | 见 §6 各年度 program / accepted | 缺失时写 `未公布` / `待补`，不得用 DBLP 冒充官方 accepted list | `2026-06-05 18:05` |
| Proceedings | 见 §6 各年度 proceedings | Springer / IEEE / DOI / DBLP fallback | `2026-06-05 18:05` |
| DBLP venue | [DBLP QRS](https://dblp.org/db/conf/qrs/index.html) | 仅作论文名录与计数 fallback | `2026-06-05 18:05` |

## 5. 核心人员情报

本节记录会议核心人员，不要求全量 PC roster。`官方角色来源` 必须能直接支撑“姓名 + 年度 / 层级 + 角色”；研究方向与代表作由 DBLP / 个人主页补充。

| 姓名 | 年度 / 层级 / 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库 project 的关系 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|
| Andrea Bondavalli | QRS 2026 General Chair；QRS 2022 Program Chair | University of Florence | [官方角色来源](https://qrs26.techconf.org/committee/organizing) | [DBLP](https://dblp.org/pid/14/2752.html) | dependability、resilient systems、safety-critical systems | DBLP 近年论文入口 | P2/P3：可靠性与验证证据链 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Shaoying Liu | QRS 2026 General Chair；QRS 2025 Program Chair | Hiroshima University / Southwest University 线索 | [官方角色来源](https://qrs26.techconf.org/committee/organizing) | [DBLP](https://dblp.org/pid/l/ShaoyingLiu.html) | formal methods、SOFL、software engineering methodology | DBLP 近年论文入口 | P1-P4：形式化建模、验证与修复 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Jin Song Dong | QRS 2026 Program Chair | National University of Singapore | [官方角色来源](https://qrs26.techconf.org/committee/organizing) | [DBLP](https://dblp.org/pid/d/JinSongDong.html) | formal methods、model checking、software verification | DBLP 近年论文入口 | P2/P3：形式化规约与验证 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Felicita Di Giandomenico | QRS 2026 Program Chair | CNR | [官方角色来源](https://qrs26.techconf.org/committee/organizing) | [DBLP](https://dblp.org/pid/49/2584.html) | dependability、fault tolerance、critical systems | DBLP 近年论文入口 | P3：可靠性与验证证据 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| W. Eric Wong | QRS Steering Committee Chair | University of Texas at Dallas | [官方角色来源](https://qrs26.techconf.org/committee/steering) | [DBLP](https://dblp.org/pid/30/5336.html) | software testing、reliability、fault localization | DBLP 近年论文入口 | P2/P4：测试与修复 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |
| Franz Wotawa | QRS Steering Committee Vice Chair | Graz University of Technology | [官方角色来源](https://qrs26.techconf.org/committee/steering) | [DBLP](https://dblp.org/pid/15/1190.html) | debugging、model-based diagnosis、testing | DBLP 近年论文入口 | P2/P4：诊断与修复 | 🟢 官方角色核验；研究方向由 DBLP 补证 | `2026-06-05 18:05` |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量单元格必须携带计数口径；未发布年度写 `未公布` / `⏳ 已检索未公布`，不能留空。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/qrs/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2027`](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | [DBLP](https://dblp.org/db/conf/qrs/index.html) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [`2026`](./2026/README.md) | 🟡 已通知 / 待会期 | [QRS 2026](https://qrs26.techconf.org/) | [CFP](https://qrs26.techconf.org/download/CFP-QRS-2026.pdf) | [Important Dates](https://qrs26.techconf.org/) | [Submission](https://qrs26.techconf.org/submission) | 未公布 | [Proceedings policy](https://qrs26.techconf.org/track/proceeding) | [DBLP](https://dblp.org/db/conf/qrs/index.html) | 2026-04-08 待补时刻 | 2026-04-22 待补时刻 | 2026-06-01 待补时刻 | 2026-07-22..2026-07-25 | 未公布；DBLP 2026 年度页尚未发布；官网只给 submission stats 278，不写 accepted count | 🟡 部分核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [QRS 2025](https://qrs25.techconf.org/) | [CFP](https://qrs25.techconf.org/download/CFP-QRS-2025.pdf) | [Important Dates](https://qrs25.techconf.org/) | [Submission](https://qrs25.techconf.org/submission) | 未发现独立稳定 accepted/program URL；以 proceedings policy / DBLP fallback | [Proceedings policy](https://qrs25.techconf.org/track/proceeding) | [DBLP](https://dblp.org/db/conf/qrs/qrs2025.html) | 未公布 | 2025-04-15 待补时刻 | 2025-05-30 待补时刻 | 2025-07-16..2025-07-20 | DBLP `inproceedings` 72；官网统计 regular acceptance 65/269；二者不是同一口径 | 🟡 部分核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [QRS 2024](https://qrs24.techconf.org/) | [CFP](https://qrs24.techconf.org/download/CFP-QRS-2024.pdf) | [Important Dates](https://qrs24.techconf.org/) | [Submission](https://qrs24.techconf.org/submission) | 未发现独立稳定 accepted/program URL；以 proceedings policy / DBLP fallback | [Proceedings policy](https://qrs24.techconf.org/track/proceeding) | [DBLP](https://dblp.org/db/conf/qrs/qrs2024.html) | 2024-03-18 待补时刻 | 2024-03-25 待补时刻 | 2024-05-07 待补时刻 | 2024-07-01..2024-07-05 | DBLP `inproceedings` 71；DBLP / IEEE proceedings fallback，不等于 main research papers | 🟡 部分核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [QRS 2023](https://qrs23.techconf.org/) | [CFP](https://qrs23.techconf.org/download/01-CFP-QRS-2023.pdf) | [Important Dates](https://qrs23.techconf.org/) | [Submission](https://qrs23.techconf.org/submission) | 官网首页公告 final program / accepted list，但未发现独立稳定 URL；以 proceedings policy / DBLP fallback | [Proceedings policy](https://qrs23.techconf.org/track/proceeding) | [DBLP](https://dblp.org/db/conf/qrs/qrs2023.html) | 2023-07-31 待补时刻 | 2023-08-07 待补时刻 | 2023-09-21 待补时刻 | 2023-10-22..2023-10-26 | DBLP `inproceedings` 70；DBLP / IEEE proceedings fallback，不等于 main research papers | 🟡 部分核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [QRS 2022](https://qrs22.techconf.org/) | [CFP](https://qrs22.techconf.org/download/01-CFP-QRS-2022.pdf) | [Important Dates](https://qrs22.techconf.org/) | [Submission](https://qrs22.techconf.org/submission) | 未发现独立稳定 accepted/program URL；以 proceedings policy / DBLP fallback | [Proceedings policy](https://qrs22.techconf.org/track/proceeding) | [DBLP](https://dblp.org/db/conf/qrs/qrs2022.html) | 2022-08-31 待补时刻 | 2022-09-10 待补时刻 | 2022-11-01 待补时刻 | 2022-12-05..2022-12-09 | DBLP `inproceedings` 107；DBLP / IEEE proceedings fallback，不等于 main research papers | 🟡 部分核验 |

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
| `2026-06-05 18:05` | PR-8 初始化 QRS venue 根 README，新增 2022--2028 年度索引、核心 URL、核心人员情报、计数口径和待补记录。 |
