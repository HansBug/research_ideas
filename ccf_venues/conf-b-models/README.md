# MoDELS README

> 信息更新时间：`2026-06-09 18:18:06`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | MoDELS |
| 全称 | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems |
| 类型 | 会议 |
| CCF 大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 等级 | 🥈 |
| 出版方 | ACM / IEEE（年度 proceedings 以当年官方页面为准） |
| 官方 series page | [researchr MoDELS series](https://conf.researchr.org/series/models) |
| 官方长期主页 | [models-conf.com](https://www.models-conf.com/) |
| 官方当前 / 最新年度主页 | [MoDELS 2026](https://conf.researchr.org/home/models-2026) |
| 官方 CFP / Important Dates 总入口 | [MoDELS 2026 dates](https://conf.researchr.org/dates/models-2026) |
| 官方 proceedings / paper list 总入口 | 未提供统一官方总入口；fallback: [DBLP MoDELS venue page](https://dblp.org/db/conf/models/) |
| DBLP venue page | [DBLP MoDELS](https://dblp.org/db/conf/models/) |
| 当前默认调查范围 | `2022` 至 `2028` |

### 1.1 索引与分区信息

> 本节为 PR #91 外部索引真实核验记录。表格的 `emoji` 列只写单个 emoji；解释、证据链接和 access note 放在相邻列。会议 venue 不写作 SCI/JCR/CAS 期刊，也不得继承同名期刊的分区。

| 索引项 | emoji | 当前结论 | 主证据 / 待补动作 | 最后核验 |
|---|---|---|---|---|
| CCF | 🥈 | CCF 🥈 等级；emoji 已按 GUIDE 的三档等级口径编码，不再回退为单色编码 | [CCF TCSE/SS/PDL 官方目录](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)；本库 CCF 等级仍以 [01-venue-scope.md](../01-venue-scope.md) 与 CCF 官方入口共同维护，镜像只作发现线索 | `2026-06-09 16:20` |
| WoS / CPCI | 🔴 | 已检索 Clarivate / Web of Science 官方入口，未取得单会议 CPCI-S / CPCI-SSH 行级证据；当前不写成 SCI 期刊 | [Web of Science Core Collection 说明](https://webofscience.help.clarivate.com/Content/wos-core-collection/wos-core-collection.htm) 与 [Clarivate MJL](https://mjl.clarivate.com/search-results) 为官方入口；会议需按具体年度 proceedings / ISBN / publisher 卷次证明 CPCI，未获行级证据时只能记录为已检索未获证据 | `2026-06-09 16:20` |
| JCR Quartile | ⚪ | 不适用 | 会议 venue 不适用 [JCR](https://jcr.clarivate.com/jcr/home) 期刊分区；若存在同名期刊，必须在独立 `journal-*` 目录核验 | `2026-06-09 13:52` |
| CAS 分区 | ⚪ | 不适用 | CAS 分区仅记录期刊历史版；[中科院文献情报中心公告](https://www.las.cas.cn/news/tzgg/202603/t20260327_8178738.html) 同时要求不得写 2026 实时分区，会议 venue 不填 CAS 区 | `2026-06-09 13:52` |
| EI / Compendex | 🟠 | 官方 Compendex `NON-SERIALS` 命中代表性 proceedings 条目；只按 proceedings-level 记录，不代表整个会议 series 长期 source-level | [Elsevier Compendex 页面](https://www.elsevier.com/en-au/products/engineering-village/databases/compendex)；[官方 source list xlsx](https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx)；官方 source list xlsx（2026-05 snapshot；2026-06-09 查询，未提交本地副本），sheet `NON-SERIALS`，代表行 Source title `2015 ACM/IEEE 18th International Conference on Model Driven Engineering Languages and Systems, MODELS 2015 - Proceedings`，Source type `Proceeding` | `2026-06-09 13:52` |
| 索引核验 | 🟡 | JCR / CAS 不适用；EI 证据按本表 source-list / proceedings / book-series 级别解释；WoS / CPCI 已检索未获单会议行级证据 | 已同步到 [SUMMARY.md](../SUMMARY.md) 的外部索引风险表；reviewer 需复核本节链接与 source-list 字段，尤其不能把 book-series 线索升级为 venue-level EI 事实 | `2026-06-09 16:20` |

## 2. Scope 与方向

MoDELS 是模型驱动工程（Model-Driven Engineering, MDE）核心会议，关注建模语言、模型转换、模型分析、模型验证、模型演化、工具链与工业应用。本仓库主要使用 MoDELS 跟踪需求到模型、状态机 / UML / SysML 建模、模型分析与验证、模型修复和工具评估相关工作。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 高 | MoDELS 直接覆盖模型驱动工程、UML/SysML、建模语言和工具链，是 LLM 状态机结构化建模的核心 venue。 |
| P2 场景与性质生成 | 中 | 部分论文涉及模型分析、trace、requirements-to-model、模型约束和性质工程，可作为验证场景生成线索。 |
| P3 验证剖面与模型检查 | 中 | MoDELS 常出现模型验证、模型分析、形式化方法与工具论文，可补充模型检查应用证据。 |
| P4 模型修复 | 中 | 模型演化、consistency repair、transformation repair 与维护类论文可为迭代式模型修复提供相关工作。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [researchr MoDELS series](https://conf.researchr.org/series/models) | [models-conf.com](https://www.models-conf.com/) 当前返回 `522`，保留作长期域名线索 | `2026-06-04 21:10` |
| Latest year homepage | [MoDELS 2026](https://conf.researchr.org/home/models-2026) | 2027/2028 探测未发布 | `2026-06-04 21:10` |
| CFP / Call for Papers | [MoDELS 2026 Research Papers](https://conf.researchr.org/track/models-2026/models-2026-research-papers) | 年度 CFP 分散在 track 页面 | `2026-06-04 21:10` |
| Important Dates | [MoDELS 2026 dates](https://conf.researchr.org/dates/models-2026) | 历年 dates 页见年度表 | `2026-06-04 21:10` |
| Submission system | [EasyChair MoDELS 2026](https://easychair.org/conferences/?conf=models2026) | EasyChair 会跳转登录页 | `2026-06-04 21:10` |
| Program / accepted papers | 未公布 | 已检索 [MoDELS 2026 program probe](https://conf.researchr.org/program/models-2026/program-models-2026/)，当前跳转 Access denied；不把该 URL 记作已公开论文名录 | `2026-06-04 21:10` |
| Proceedings | [MoDELS 2022 proceedings](https://conf.researchr.org/info/models-2022/conference-proceedings) | 2024 proceedings 当前 accessDenied；DBLP 作计数 fallback | `2026-06-04 21:10` |
| DBLP venue | [DBLP MoDELS](https://dblp.org/db/conf/models/) | 仅作论文名录 / 计数 fallback | `2026-06-04 21:10` |

## 5. 核心人员情报

> 人员角色以 MoDELS 官方 committee / steering 页面为准；研究方向为根据个人主页、DBLP 与近年论文线索归纳。MoDELS 人员情报重点服务 P1 的 MDE / UML / SysML / 状态机建模，也服务 P4 的模型变换、演化与修复。

| 人员 | 角色 / 年度 | 官方角色来源 | 主要研究方向 | 代表作 / 近年论文线索 | 与本仓库关系 | 待深挖 |
|---|---|---|---|---|---|---|
| Lola Burgueño | 2026 General Chair；2026 Steering Committee | [2026 Organizing Committee](https://conf.researchr.org/committee/models-2026/models-2026-organizing-committee)；[2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | MDE、AI for MDE、模型变换质量、模型测试 | [个人主页](https://lolaburgueno.github.io/)；[DBLP](https://dblp.org/pid/116/5369)；[ESE 2026 modelling tasks](https://dblp.org/rec/journals/ese/ChakrabortyTBL26)；[few-shot model completion](https://dblp.org/rec/journals/corr/abs-2212-03404) | P1/P4 很高：LLM 辅助建模、模型评审、模型修复 | 需核验是否有直接 state machine / UML 级案例。 |
| Shaukat Ali | 2025 Program Co-Chair；2026 Steering Committee | [2025 Organizing Committee](https://conf.researchr.org/committee/models-2025/models-2025-organizing-committee)；[2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | Verification & Validation、SBSE、模型测试、CPS、digital twins | [Simula 主页](https://www.simula.no/people/shaukat)；[DBLP](https://dblp.org/pid/25/5352-1)；[AV collision configuration learning](https://dblp.org/rec/journals/tse/LuSZZWYA23)；[Uncertainty-wise CPS testing](https://dblp.org/rec/journals/jss/ZhangAY19) | P2/P3/P4 高相关：测试生成、验证、闭环修复 | DBLP 同名需继续用机构 / ORCID 消歧。 |
| Houari Sahraoui | 2025 Program Co-Chair；2026 Steering Committee | [2025 Organizing Committee](https://conf.researchr.org/committee/models-2025/models-2025-organizing-committee)；[2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | MDE、模型变换、软件质量、形式化验证、LLM / PLM for modeling | [UdeM 教授页](https://diro.umontreal.ca/english/departement-directory/professors/professor/in/in15076/sg/Houari%20Sahraoui/)；[DBLP](https://dblp.org/pid/s/HouariASahraoui)；[domain modeling with LLMs](https://dblp.org/rec/journals/corr/abs-2410-12577)；[metamodel concept recommendation](https://dblp.org/rec/journals/sosym/WeyssowSS22) | P1/P2/P3/P4 高相关：建模、验证、修复全链路 | 需判断近年重点更偏 LLM4MDE 还是传统 verification。 |
| Esther Guerra | 2026 PC Chair；2026 Steering Committee | [2026 Organizing Committee](https://conf.researchr.org/committee/models-2026/models-2026-organizing-committee)；[2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | metamodeling、model transformation、model management、low-code MDE、metamorphic testing | [个人主页](https://arantxa.ii.uam.es/~eguerra)；[DBLP](https://dblp.org/pid/75/4962)；[domain-specific metamorphic testing](https://dblp.org/rec/journals/infsof/GomezAbajoCNGL23)；[model sensemaking](https://dblp.org/rec/conf/models/Martinez-Lasaca23) | P1/P4 很高：模型变换语义、低代码建模、模型修复 | 需补 2024-2026 low-code vs M2M 变换重心。 |
| Mehrdad Sabetzadeh | 2026 PC Chair；2026 Steering Committee | [2026 Organizing Committee](https://conf.researchr.org/committee/models-2026/models-2026-organizing-committee)；[2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | requirements engineering、合规 / legal requirements、NLP / ML for requirements、MDE safety compliance | [UOttawa 页面](https://www.uottawa.ca/faculty-engineering/school-electrical-engineering-computer-science/directory/Mehrdad-Sabetzadeh)；[DBLP](https://dblp.org/pid/25/6367)；[LLM-generated algebraic specs](https://dblp.org/rec/journals/corr/abs-2601-00469)；[LLM Simulink slicing](https://dblp.org/rec/journals/corr/abs-2405-01695) | P1/P2/P3/P4 很高：需求抽取、合规验证、LLM 处理需求文本 | 需区分 RE/NLP 线与 MDE/compliance 线。 |
| Daniel Varró | 2026 Steering Committee Chair | [2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | model transformation、graph transformation、MBSE、CPS、ML | [McGill 页面](https://www.mcgill.ca/miae/daniel-varro)；[DBLP](https://dblp.org/pid/53/1883)；[Model Transformation by Example](https://dblp.org/rec/conf/models/Varro06)；[MTBE with ILP](https://dblp.org/rec/journals/sosym/BaloghV09) | P1/P4 很高：模型生成、转换、修复基础方法 | 需追踪 2024-2026 是偏基础工具还是 MBSE/CPS 应用。 |
| Manuel Wimmer | 2026 Steering Committee Vice-Chair | [2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | MDE foundations / applications、model evolution、model versioning、digital twins、language customization | [JKU 页面](https://se.jku.at/manuel-wimmer/)；[DBLP](https://dblp.org/pid/20/4565.html)；[LLM-enhanced model versioning](https://dblp.org/rec/conf/models/EisenbergKWW25)；[MDE in Practice](https://dblp.org/rec/series/synthesis/2017Brambilla) | P1/P4 高相关：建模语言、模型演化、自动化修复 | 需确认当前重点是否转向 language customization / digital twins。 |
| Gabriele Taentzer | 2026 NIER Co-Chair；2026 Steering Committee | [2026 Organizing Committee](https://conf.researchr.org/committee/models-2026/models-2026-organizing-committee)；[2026 Steering](https://conf.researchr.org/committee/models-2026/models-2026-steering-committee) | graph / model transformation、formal foundations、visual languages、repair / consistency | [Marburg 页面](https://www.uni-marburg.de/de/fb12/arbeitsgruppen/swt/team/prof-dr-gabriele-taentzer)；[DBLP](https://dblp.org/pid/t/GabrieleTaentzer)；[Empowering Model Repair](https://dblp.org/rec/conf/models/LauerKT23)；[Change-Preserving Model Repair](https://dblp.org/rec/conf/fase/TaentzerOLR17) | P1/P4 很高：模型一致性、图变换修复、变换语义 | 需补更贴近 state-machine repair / consistency 的最新工作。 |

## 6. 年度信息汇总

年度汇总表按年份降序排列；官方仅给日期而未核实具体时刻的 deadline 统一写作 `待补时刻 AoE`。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | Submission system | Program / Accepted papers | Proceedings | DBLP 年度页 | Abstract deadline | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| [2028](./2028/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 待核验 |
| [2027](./2027/README.md) | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 待核验 |
| [2026](./2026/README.md) | 🟡 审稿中 | [MoDELS 2026](https://conf.researchr.org/home/models-2026) | [Research Papers track](https://conf.researchr.org/track/models-2026/models-2026-research-papers) | [Important Dates](https://conf.researchr.org/dates/models-2026) | [Submission](https://easychair.org/conferences/?conf=models2026) | ⏳ 已检索未公布（[program probe](https://conf.researchr.org/program/models-2026/program-models-2026/) 为 Access denied） | 未公布 | ⏳ 已检索未公布 | 2026-03-20 待补时刻 AoE | 2026-03-27 待补时刻 AoE | 2026-06-17 待补时刻 AoE | 2026-10-04..2026-10-09 | 未最终公布 | 🟡 部分核验 |
| [2025](./2025/README.md) | ✅ 已结束 | [MoDELS 2025](https://2025.models-conf.com/) | [Research Papers track](https://2025.models-conf.com/track/models-2025-research-papers) | [Important Dates](https://conf.researchr.org/dates/models-2025) | [Submission](https://easychair.org/conferences/?conf=models2025) | [Program](https://2025.models-conf.com/program/program-models-2025/) | 未公布 | [DBLP 2025](https://dblp.org/db/conf/models/models2025.html) | 2025-03-27 待补时刻 AoE | 2025-04-03 待补时刻 AoE | 2025-06-24 待补时刻 AoE | 2025-10-05..2025-10-10 | DBLP inproceedings: 27 | 🟢 已核验 |
| [2024](./2024/README.md) | ✅ 已结束 | [MoDELS 2024](https://conf.researchr.org/home/models-2024) | [CfP PDF](https://conf.researchr.org/getImage/models-2024/orig/CfP.pdf) | [Important Dates](https://conf.researchr.org/dates/models-2024) | [Submission](https://easychair.org/conferences/?conf=models24) | [Program](https://conf.researchr.org/program/models-2024/program-models-2024/) | [Proceedings](https://conf.researchr.org/info/models-2024/conference-proceedings) | [DBLP 2024](https://dblp.org/db/conf/models/models2024.html) | 2024-03-21 待补时刻 AoE | 2024-03-28 待补时刻 AoE | 2024-06-17 待补时刻 AoE | 2024-09-22..2024-09-27 | DBLP inproceedings: 26 | 🟢 已核验 |
| [2023](./2023/README.md) | ✅ 已结束 | [MoDELS 2023](https://conf.researchr.org/home/models-2023) | [Research Papers track](https://conf.researchr.org/track/models-2023/models-2023-technical-track) | [Important Dates](https://conf.researchr.org/dates/models-2023) | [Submission](https://easychair.org/conferences/?conf=models23) | [FT accepted papers](https://conf.researchr.org/info/models-2023/accepted-papers---ft) / [PT accepted papers](https://conf.researchr.org/info/models-2023/accepted-papers---pt) | 未公布 | [DBLP 2023](https://dblp.org/db/conf/models/models2023.html) | 2023-04-07 待补时刻 AoE | 2023-04-14 待补时刻 AoE | 2023-06-26 待补时刻 AoE | 2023-10-01..2023-10-06 | Official FT/PT accepted: 30 | 🟢 已核验 |
| [2022](./2022/README.md) | ✅ 已结束 | [MoDELS 2022](https://conf.researchr.org/home/models-2022) | [Research Papers track](https://conf.researchr.org/track/models-2022/models-2022-technical-track) | [Important Dates](https://conf.researchr.org/dates/models-2022) | [Submission](https://easychair.org/conferences/?conf=models2022) | [Program](https://conf.researchr.org/program/models-2022/program-models-2022/) | [Proceedings](https://conf.researchr.org/info/models-2022/conference-proceedings) | [DBLP 2022](https://dblp.org/db/conf/models/models2022.html) | 2022-05-18 待补时刻 AoE | 2022-05-18 待补时刻 AoE | 2022-07-12 待补时刻 AoE | 2022-10-23..2022-10-28 | DBLP inproceedings: 35 | 🟢 已核验 |


## 7. 维护备注

- 2028 / 2027：官方 home、dates、Research track URL 已检索，均返回 `404`；按“未发布”处理，不伪造年度主页或 deadline。
- 2026：official home、dates、submission、Research Papers track 可访问；截至 `2026-06-04` submission 与 rebuttal 已过但 notification 尚未到达，因此整体阶段写作 `🟡 审稿中`；program URL 当前跳转 accessDenied，论文数量未最终公布。
- 2025 / 2024 / 2023 / 2022：论文数量使用 DBLP `inproceedings` 或官方 accepted paper 口径记录；年度页逐项说明计数口径。
- ACM DL DOI 页面在本次 curl 核查中返回 `403`，但 DOI 链接仍按官方 proceedings 页给出的 main / companion proceedings 入口记录。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应年度表格与 Mermaid Gantt。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-09 18:18:06` | 修复 PR #91 CCF emoji 一致性复查：将根 README `CCF 等级` 元信息行改为 🏆/🥈/🥉 单 emoji，具体 CCF 官方证据继续落在 §1.1 索引表 CCF 行。 |
| `2026-06-09 11:13` | 新增外部索引与分区信息占位入口，后续按 GUIDE 逐项补证 WoS/JCR/CAS/EI。 |
| `2026-06-04 22:20` | 统一 MoDELS 2026 当前阶段、根表会期分隔符、论文数量计数口径和 EasyChair 链接。 |
| `2026-06-04 21:44` | 补充核心人员情报，并按 review 修正 accessDenied、计数或会期等事实口径。 |
| `2026-06-04 21:10` | 初始化 MoDELS 根 README，并创建 2022-2028 年度索引与核心 URL 表。 |
