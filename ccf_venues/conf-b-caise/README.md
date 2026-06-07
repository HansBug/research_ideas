# CAiSE README

> 信息更新时间：`2026-06-07 13:33`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | CAiSE |
| 全称 | International Conference on Advanced Information Systems Engineering |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言（[CCF 官方目录入口](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；CLI 可能触发 WAF，正文待人工浏览器复核） |
| CCF 等级 | B（官方入口已定位；`ccf.atom.im` 仅作非官方机器检索线索） |
| 出版方 | Springer LNCS（主会）；Forum / DC / Workshop 可能为 Springer / CEUR 等独立卷 |
| 官方 series page | [CAiSE long-term site](https://caise-conference.org/)（本次 CLI 访问异常，作长期域名线索） |
| 官方当前 / 最新年度主页 | [CAiSE 2026](https://caise26.polimi.it/) |
| 官方 CFP / Important Dates 总入口 | [CAiSE 2026 full papers CFP](https://caise26.polimi.it/?page_id=60) / [CAiSE 2026 dates](https://caise26.polimi.it/?page_id=60) |
| 官方 proceedings / paper list 总入口 | [Accepted papers](https://caise26.polimi.it/?page_id=948) / [Final program](https://caise26.polimi.it/?page_id=1122) / 未公布 / Springer 待补 |
| DBLP venue page | [DBLP CAiSE](https://dblp.org/db/conf/caise/) |
| 当前默认调查范围 | `2022` 至 `2028`；未公布未来年度不预造 |

## 2. Scope 与方向

CAiSE 聚焦 Advanced Information Systems Engineering，覆盖 requirements engineering、conceptual modeling、ontology / enterprise modeling、business process modeling、process mining / monitoring、low-code / no-code、method engineering、compliance、quality of IS models、knowledge graphs、CPS / IoT / service / cloud / edge information systems 等方向。

本库将 CAiSE 作为 LLM4Modeling 的信息系统 / 概念建模 / MDE 分流 venue，不把它描述成泛 SE 主战场。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 中高 | 适合需求到模型、概念/领域/企业模型、LLM-assisted modeling、模型质量评估；普通 prompt 工具评测不宜强投。 |
| P2 场景与性质生成 | 中 | 适合 requirements / constraints / compliance / process / IS model 语境下的场景与性质生成。 |
| P3 验证剖面与模型检查 | 中低到中 | 需要包装为 IS/CPS/enterprise/process model 的 engineering profile 或 compliance / quality analysis；纯 model checking 技术优先其他 venue。 |
| P4 模型修复 | 中 | 适合 model quality、consistency、evolution、alignment、repair in IS modeling / MDE context。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [CAiSE long-term site](https://caise-conference.org/)（本次 CLI 访问异常，作长期域名线索） | 若长期站访问异常，年度事实以年度 official site 为准 | `2026-06-07 12:47` |
| Latest year homepage | [CAiSE 2026](https://caise26.polimi.it/) | future 年度未公布时写 `⏳ 已检索未公布` | `2026-06-07 12:47` |
| CFP / Call for Papers | [CAiSE 2026 full papers CFP](https://caise26.polimi.it/?page_id=60) | 若分 track，年度页展开 | `2026-06-07 12:47` |
| Important Dates | [CAiSE 2026 dates](https://caise26.polimi.it/?page_id=60) | 可与 CFP 同页 | `2026-06-07 12:47` |
| Submission system | [EasyChair CAiSE 2026](https://easychair.org/my/conference?conf=caise2026) | 只能证明投稿入口，不替代 CFP / dates | `2026-06-07 12:47` |
| Program / accepted papers | [Accepted papers](https://caise26.polimi.it/?page_id=948) / [Final program](https://caise26.polimi.it/?page_id=1122) | 已结束年度优先 official accepted/program | `2026-06-07 12:47` |
| Proceedings | 未公布 / Springer 待补 | publisher / DBLP fallback 分开 | `2026-06-07 12:47` |
| DBLP venue | [DBLP CAiSE](https://dblp.org/db/conf/caise/) | 仅作论文名录 / 计数 fallback | `2026-06-07 12:47` |

## 5. 核心人员情报

> 人员角色以年度 official committee / editorial pages 为准；DBLP / 个人主页只补研究方向与代表作。不要把 invited speaker、guest editor 或普通 PC member 升级为 chair / steering。

| 姓名 | 年度 / 层级 | 会议角色 | 单位 | 官方角色来源 | 主页 / 学术入口 | 主要研究方向 | 代表作 / 近 5 年论文入口 | 与本仓库相关性 | 核验状态 | 核查时间 |
|---|---|---|---|---|---|---|---|---|---|---|
| Carlo Combi | 2026 / conference | General Chair | University of Verona | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Carlo%20Combi) | temporal / process / information systems、healthcare IS | [DBLP 近年论文入口](https://dblp.org/search?q=Carlo%20Combi) | P2/P3：时间约束、流程与 IS 验证语境 | 🟡 部分核验 | `2026-06-07 12:47` |
| Hajo Reijers | 2026 / conference | General Chair | Utrecht University | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Hajo%20Reijers) | business process management、process redesign / mining | [DBLP 近年论文入口](https://dblp.org/search?q=Hajo%20Reijers) | P1/P2/P3：过程模型、场景与流程分析 | 🟡 部分核验 | `2026-06-07 12:47` |
| Lidia Fuentes | 2026 / program | Program Co-Chair | University of Málaga | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Lidia%20Fuentes) | software architecture、MDE、variability、self-adaptive systems | [DBLP 近年论文入口](https://dblp.org/search?q=Lidia%20Fuentes) | P1/P4：MDE / architecture / variability 与模型修复 | 🟡 部分核验 | `2026-06-07 12:47` |
| Pierluigi Plebani | 2026 / program | Program Co-Chair | Politecnico di Milano | [CAiSE 2026 committees](https://caise26.polimi.it/?page_id=71) | [DBLP](https://dblp.org/search?q=Pierluigi%20Plebani) | information systems、services、process / data management | [DBLP 近年论文入口](https://dblp.org/search?q=Pierluigi%20Plebani) | P1/P2：IS modeling 与 service/process requirements | 🟡 部分核验 | `2026-06-07 12:47` |
| John Krogstie | 2025 / program + steering | PC Chair / Steering Chair | NTNU | [CAiSE 2025 committee](https://conferences.big.tuwien.ac.at/caise2025/committee.php) | [DBLP](https://dblp.org/search?q=John%20Krogstie) | conceptual modeling、enterprise modeling、quality of models | [DBLP 近年论文入口](https://dblp.org/search?q=John%20Krogstie) | P1/ex1：模型质量与评审标准 | 🟡 部分核验 | `2026-06-07 12:47` |
| Gerti Kappel | 2025 / conference | General Chair | TU Wien | [CAiSE 2025 committee](https://conferences.big.tuwien.ac.at/caise2025/committee.php) | [DBLP](https://dblp.org/search?q=Gerti%20Kappel) | model engineering、web engineering、conceptual modeling | [DBLP 近年论文入口](https://dblp.org/search?q=Gerti%20Kappel) | P1/P4：MDE / conceptual modeling | 🟡 部分核验 | `2026-06-07 12:47` |

## 6. 年度信息汇总

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | Camera-ready | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2027](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 🟡 部分核验 |
| [2026](./2026/README.md) | 🟡 已公布 / 会前 | [CAiSE 2026](https://caise26.polimi.it/) | [Full papers CFP](https://caise26.polimi.it/?page_id=60) | [CFP / dates](https://caise26.polimi.it/?page_id=60) | [EasyChair CAiSE 2026](https://easychair.org/my/conference?conf=caise2026) | [Accepted papers](https://caise26.polimi.it/?page_id=948) / [Final program](https://caise26.polimi.it/?page_id=1122) | 未公布 / Springer 主会 proceedings 待补 | ⏳ 已检索未公布 | 2025-11-21 待补时刻 AoE | 2025-11-28 待补时刻 AoE | 2026-02-12 待补时刻 | 待补 | 2026-06-08..2026-06-12 | accepted page 可人工计数；proceedings / DBLP 待补 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [CAiSE 2025](https://conferences.big.tuwien.ac.at/caise2025/) | [Full papers CFP](https://conferences.big.tuwien.ac.at/caise2025/cfp_full.php) | [CFP / dates](https://conferences.big.tuwien.ac.at/caise2025/cfp_full.php) | [EasyChair CAiSE 2025](https://easychair.org/my/conference?conf=caise2025) | [Accepted papers](https://conferences.big.tuwien.ac.at/caise2025/accepted_papers.php?type=Main%20Conference) | [Proceedings page](https://conferences.big.tuwien.ac.at/caise2025/proceedings.php) / [Vol.1](https://link.springer.com/book/10.1007/978-3-031-94569-4) / [Vol.2](https://link.springer.com/book/10.1007/978-3-031-94571-7) | ⏳ 已检索未公布 | 2024-11-22 待补时刻 | 2024-12-01 待补时刻 | 2025-02-28 待补时刻 | 2025-04-14 待补时刻 | 2025-06-16..2025-06-20 | 待按 main conference / LNCS 主卷复核 | 🟡 部分核验 |
| [2024](./2024/README.md) | ✅ 已结束 / 归档待补 | 待补（官方年度站当前未定位到可访问归档） | 待补 | 待补 | 待补 | 待补 | [DBLP / Springer proceedings record](https://dblp.org/db/conf/caise/caise2024.html) | [DBLP CAiSE 2024](https://dblp.org/db/conf/caise/caise2024.html) | 待补 | 待补 | 待补 | 待补 | 2024-06-03..2024-06-07（DBLP proceedings record） | DBLP 可计数；待 main conference 口径复核 | 🟡 部分核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [CAiSE 2023](https://caise23.svit.usj.es/) | [Main conference](https://caise23.svit.usj.es/main-conference/) | [Main conference dates](https://caise23.svit.usj.es/main-conference/) | 待补（官方按钮 / EasyChair 历史入口需复核） | [Accepted papers](https://caise23.svit.usj.es/accepted-papers/) / [Program](https://caise23.svit.usj.es/program/) | [Proceedings](https://caise23.svit.usj.es/proceedings/) | [DBLP CAiSE 2023](https://dblp.org/db/conf/caise/caise2023.html) | 2022-11-22 待补时刻 | 2022-11-29 待补时刻 | 2023-03-01 待补时刻 | 2023-04-03 待补时刻 AoE | 2023-06-12..2023-06-16 | DBLP 可计数；待 main conference 口径复核 | 🟡 部分核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [CAiSE 2022](https://caise22.ugent.be/) | [Calls](https://caise22.ugent.be/calls/) | [Homepage / calls key dates](https://caise22.ugent.be/) | 待补 | [Accepted papers](https://caise22.ugent.be/accepted-papers/) / [Program](https://caise22.ugent.be/program/) | [Proceedings](https://caise22.ugent.be/proceedings/) | [DBLP CAiSE 2022](https://dblp.org/db/conf/caise/caise2022.html) | 2021-11-22 待补时刻 | 2021-11-29 待补时刻 | 2022-03-01 待补时刻 | 2022-03-28 待补时刻 | 2022-06-06..2022-06-10 | DBLP 可计数；待 main conference 口径复核 | 🟡 部分核验 |

## 7. 计数口径与维护备注

- CAiSE 主会计数只算 main conference / LNCS main proceedings；Forum、Doctoral Consortium、Journal First、RPE、Workshops、BPMDS、EMMSAD 不混入主会数量。
- 2024 official annual site 当前未定位到可访问归档；只用 DBLP / Springer proceedings record 落会期和 proceedings 线索，不补写 CFP / deadline。
- 2027/2028 未公布，不预造 homepage、committee、CFP、submission system 或 DBLP 年度页。

## 8. 证据与核查记录

| 类型 | 链接 | 核查时间 | 结论 |
|---|---|---|---|
| CCF official entry | [CCF TCSE_SS_PDL](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) | `2026-06-07 12:47` | 官方入口已定位；CLI 可能触发 WAF / 动态页，正文与第七版状态待人工浏览器复核。 |
| 非官方 CCF 镜像线索 | [ccf.atom.im](https://ccf.atom.im/) | `2026-06-07 12:47` | 仅作机器检索 / 差集筛查线索，不作为 CCF 官方事实。 |
| Official annual pages | [CAiSE 2026](https://caise26.polimi.it/) / [CAiSE 2025](https://conferences.big.tuwien.ac.at/caise2025/) / [CAiSE 2023](https://caise23.svit.usj.es/) / [CAiSE 2022](https://caise22.ugent.be/) | `2026-06-07 12:47` | 2022/2023/2025/2026 年度官方站与 main conference chain 已定位。 |
| 2024 fallback | [DBLP CAiSE 2024](https://dblp.org/db/conf/caise/caise2024.html) | `2026-06-07 12:47` | 仅支撑 proceedings record / 会期；2024 official CFP / dates / submission 仍待补。 |
| DBLP fallback | [DBLP CAiSE](https://dblp.org/db/conf/caise/) | `2026-06-07 12:47` | 仅作 bibliographic fallback；主会、Forum、DC、Workshop 需分口径计数。 |

## 9. TIMELINE.md 同步提示

- 本 venue 已核验 dated events 已同步至 [../TIMELINE.md](../TIMELINE.md) 对应年份表格与 PR #63 Mermaid 分片。
- 未公布年度、第三方线索、WAF / 404 / CAPTCHA 候选页不得进入 dated TIMELINE / Mermaid。

## 10. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-07 13:33` | 修复实现后 review：补入 CAiSE 2023 official camera-ready `2023-04-03` AoE 并同步 TIMELINE。 |
| `2026-06-07 12:47` | PR #63 初始化 CAiSE 情报，补充 CCF / official / DBLP 证据、2022--2028 年度索引、核心人员、TIMELINE 同步和待补口径。 |
