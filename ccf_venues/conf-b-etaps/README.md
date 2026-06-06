# ETAPS / TACAS README

> 信息更新时间：`2026-06-04 22:20`（Asia/Shanghai）

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| 缩写 | ETAPS / TACAS |
| 全称 | European Joint Conferences on Theory and Practice of Software / Tools and Algorithms for the Construction and Analysis of Systems |
| 类型 | 会议；ETAPS 是 umbrella conference，TACAS 是 ETAPS 下的分会之一 |
| CCF 大类 | 软件工程 / 理论与形式化方法相关 |
| CCF 等级 | B |
| 本库目录 | `conf-b-etaps`；不单独创建 `conf-b-tacas` |
| 出版方 | Springer LNCS / ETAPS 官方 proceedings 口径 |
| 官方 series page | [ETAPS](https://etaps.org/) |
| 官方 proceedings info | [ETAPS proceedings information](https://etaps.org/about/proceedings/) |
| DBLP venue page | [DBLP TACAS index](https://dblp.org/db/conf/tacas/) |
| 当前默认调查范围 | `2022` 至 `2028` |

## 2. Scope 与方向

- ETAPS 是覆盖软件科学与工程理论、实践及工具的联合会议 umbrella。
- TACAS 是 ETAPS 下聚焦系统构造与分析工具、算法、模型检查、验证、自动化证明和形式化方法的分会。
- 本目录以 ETAPS 年度主页为 umbrella 入口，同时在每个年度页显式区分 TACAS 分会入口、TACAS 重要日期和 TACAS 论文计数。

## 3. 与本仓库 project 的关系

| Project | 相关性 | 说明 |
|---|---|---|
| P1 状态机建模 | 🟡 中 | TACAS 常包含形式化建模、自动机、工具链与规格建模论文，可作为建模方法相关工作来源。 |
| P2 场景与性质生成 | 🟢 高 | TACAS 与验证性质、反例、模型检查任务高度相关。 |
| P3 验证剖面与模型检查 | 🟢 高 | TACAS 是模型检查、形式化验证、工具论文的重要 venue。 |
| P4 模型修复 | 🟡 中 | 可追踪自动修复、counterexample-guided refinement、验证驱动修复相关工作。 |

## 4. 核心链接索引

| 链接类型 | 官方 / 优先链接 | fallback / 备注 | 核验时间 |
|---|---|---|---|
| Series / main site | [ETAPS](https://etaps.org/) | ETAPS umbrella 长期主页 | `2026-06-04 21:10` |
| Proceedings info | [ETAPS proceedings information](https://etaps.org/about/proceedings/) | 年度 proceedings 缺失时使用该页说明出版口径 | `2026-06-04 21:10` |
| TACAS DBLP venue | [DBLP TACAS index](https://dblp.org/db/conf/tacas/) | 仅作 TACAS 论文名录 / 计数 fallback 与交叉核验 | `2026-06-04 21:10` |
| Latest year homepage | [ETAPS 2028](https://etaps.org/2028/) | 2028 已有年度主页，但 CFP / TACAS / dates 未公布 | `2026-06-04 21:10` |
| 2027 CFP / Important Dates | [ETAPS 2027 CFP](https://etaps.org/2027/cfp/) | important-dates 重定向 CFP | `2026-06-04 21:10` |
| 2027 TACAS track | [TACAS 2027](https://etaps.org/2027/conferences/tacas/) | TACAS 分会页 | `2026-06-04 21:10` |
| 2027 submission system | [EasyChair TACAS 2027](https://easychair.org/conferences/?conf=tacas27) | EasyChair 会重定向到登录页 | `2026-06-04 21:10` |

## 5. 核心人员情报

> ETAPS 是 umbrella venue，本节优先维护 TACAS 分会与形式化验证 / model checking 强相关人员；角色来源以 ETAPS/TACAS 官方分会页和 TACAS Steering 页面为准。若官方拼写与 DBLP 拼写不同，必须保留备注。

| 人员 | 角色 / 年度 | 官方角色来源 | 主要研究方向 | 代表作 / 近年论文线索 | 与本仓库关系 | 待深挖 |
|---|---|---|---|---|---|---|
| Sebastian Junges | TACAS 2026 PC Chair | [TACAS 2026](https://etaps.org/2026/conferences/tacas/) | 概率模型检查、MDP / POMDP、参数综合、运行时监控 | [DBLP](https://dblp.org/pid/115/4386.html)；[Runtime Monitors for MDPs](https://dblp.org/rec/conf/cav/JungesTS20)；[Learning Verified Monitors](https://dblp.org/rec/journals/corr/abs-2504-05963) | P2/P3/P4 很高；可扩展到不确定 / 概率状态机 | 需补控制系统状态机建模 / 修复直接桥接论文。 |
| Guy Katz | TACAS 2026 PC Chair | [TACAS 2026](https://etaps.org/2026/conferences/tacas/) | 神经网络验证、SMT、可证明解释、LLM / 智能系统可靠性 | [DBLP](https://dblp.org/pid/23/10321.html)；[Neural Network Verification Using Residual Reasoning](https://dblp.org/rec/conf/sefm/ElboherCK22)；[Statistical Runtime Verification for LLMs](https://dblp.org/rec/conf/rv/LevyAK25) | P1/P3 与 project_ex1 高相关：AI 系统验证、LLM 可靠性 | 与控制系统状态机主线的直接连接仍需补证。 |
| Christian Schilling | TACAS 2027 PC Chair | [TACAS 2027](https://etaps.org/2027/conferences/tacas/) | 形式化验证、合成、CPS / software systems、safe AI | [个人主页](https://www.christianschilling.net/)；[论文页](https://www.christianschilling.net/publications.html) | P1/P4 高相关：CPS、控制器合成、形式化保障 + AI | 需补传统 model checking / verification 代表作链接。 |
| Naijun Zhan（官方 TACAS 2027 页拼作 Najiun Zhan） | TACAS 2027 PC Chair | [TACAS 2027](https://etaps.org/2027/conferences/tacas/) | CPS 形式化方法、hybrid systems、Simulink / Stateflow、Hybrid CSP、验证与代码生成 | [主页](https://lcs.ios.ac.cn/~znj/)；[DBLP](https://dblp.org/pid/63/1911.html)；[Mars 2.0](https://dblp.org/rec/journals/corr/abs-2403-03035) | P1/P2/P3/P4 很高：控制系统需求到模型、验证、代码生成 / 修复 | 需持续记录官方拼写与 DBLP 拼写差异。 |
| Joost-Pieter Katoen | TACAS Steering Committee Chair | [TACAS Steering](https://etaps.org/about/tacas/) | model checking、probabilistic verification、MDP、quantitative objectives、probabilistic programs | [DBLP](https://dblp.org/pid/k/JoostPieterKatoen.html)；[TACAS 2026 MDP objectives](https://dblp.org/rec/conf/tacas/IdeKMQ26)；[Probabilistic programs verification](https://dblp.org/rec/journals/pacmpl/BatzKKMV23) | P2/P3/P4 很高；P1 中概率 / 时间状态机语义可参考 | 需补 state-machine repair 直接线索。 |
| Dirk Beyer | TACAS Steering Committee Member | [TACAS Steering](https://etaps.org/about/tacas/) | software verification、model checking、SV-COMP / Test-Comp、witness validation、abstraction refinement | [DBLP](https://dblp.org/pid/b/DirkBeyer1.html)；[SV-COMP 2026](https://dblp.org/rec/conf/tacas/BeyerS26)；[Verification Witnesses](https://www.sosy-lab.org/research/pub/2022-TOSEM.Verification_Witnesses.pdf) | P2/P3/P4 很高：benchmark、witness、验证证据链、工具生态 | 需补需求驱动建模 / 状态机修复相关线索。 |
| Corina Păsăreanu | TACAS Steering Committee Member | [TACAS Steering](https://etaps.org/about/tacas/) | symbolic execution、software model checking、autonomous systems、learning-enabled systems | [DBLP](https://dblp.org/pid/03/4368.html)；[Scenario-based Compositional Verification](https://dblp.org/rec/journals/corr/abs-2504-20942)；[Assumption Generation](https://dblp.org/rec/conf/rv/PasareanuMGY23) | P1/P2/P3 很高：场景生成、假设生成、学习系统验证 | 需建立 neural-perception 场景与传统状态机之间的映射。 |
| Christel Baier | TACAS 2027 Area Chair | [TACAS 2027](https://etaps.org/2027/conferences/tacas/) | probabilistic model checking、ω-regular / long-run properties、quantitative verification | [DBLP](https://dblp.org/pid/b/ChristelBaier)；[Model Checking Probabilistic Systems](https://dblp.org/rec/reference/mc/BaierAFK18)；[Long-run Satisfaction](https://dblp.org/rec/conf/lics/Baier0PS19) | P2/P3/P4 高相关：性质建模、长程 / 概率性质验证 | 需补 2023-2026 最新论文或报告。 |

## 6. 年度信息汇总

> 年度表按年份降序排列。论文数量显式拆分为 `ETAPS umbrella: N` 与 `TACAS: N`；未发布年度写 `未公布` / `⏳ 已检索未公布`。

| 年份 | 阶段状态 | 官方主页 | CFP | Important Dates | TACAS 分会 | Submission system | Program / Accepted papers | Proceedings | DBLP TACAS 年度页 | Submission deadline | Notification | 会期 | 论文数量 | 核验状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`2028`](./2028/README.md) | 🟦 已有主页 | [ETAPS 2028](https://etaps.org/2028/) | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | 未公布 | ⏳ 已检索未公布 | 未公布 | 未公布 | 2028-04-02..2028-04-07 | ETAPS umbrella: 未公布；TACAS: 未公布 | ⏳ 已检索未公布 |
| [`2027`](./2027/README.md) | 🟢 投稿中 | [ETAPS 2027](https://etaps.org/2027/) | [CFP](https://etaps.org/2027/cfp/) | [Important Dates](https://etaps.org/2027/cfp/) | [TACAS track](https://etaps.org/2027/conferences/tacas/) | [EasyChair](https://easychair.org/conferences/?conf=tacas27) | 未公布 | 未公布 | ⏳ 已检索未公布 | 2026-10-15 待补时刻 AoE | 2026-12-22 待补时刻 | ETAPS 2027-04-10..2027-04-15；Main conferences/TACAS 2027-04-12..2027-04-15 | ETAPS umbrella: 未公布；TACAS: 未公布 | ⏳ 已检索未公布 |
| [`2026`](./2026/README.md) | ✅ 已结束 | [ETAPS 2026](https://etaps.org/2026/) | [CFP](https://etaps.org/2026/cfp/) | [Important Dates](https://etaps.org/2026/cfp/) | [TACAS track](https://etaps.org/2026/conferences/tacas/) | [EasyChair](https://easychair.org/conferences/?conf=tacas26) | [Program / Accepted](https://etaps.org/2026/programme/) | [Proceedings](https://etaps.org/about/proceedings/) | [DBLP TACAS 2026](https://dblp.org/db/conf/tacas/index.html#2026) | 2025-10-16 待补时刻 AoE | 2025-12-22 待补时刻 | ETAPS 2026-04-11..2026-04-16；TACAS 2026-04-13..2026-04-16 | ETAPS umbrella: 138；TACAS: 56 | 🟢 已核验 |
| [`2025`](./2025/README.md) | ✅ 已结束 | [ETAPS 2025](https://etaps.org/2025/) | [CFP](https://etaps.org/2025/cfp/) | [Important Dates](https://etaps.org/2025/cfp/) | [TACAS track](https://etaps.org/2025/conferences/tacas/) | [EasyChair](https://easychair.org/conferences/?conf=tacas25) | [Program / Accepted](https://etaps.org/2025/past-conference/) | [Proceedings](https://etaps.org/about/proceedings/) | [DBLP TACAS 2025](https://dblp.org/db/conf/tacas/index.html#2025) | 2024-10-10 23:59 AoE | 2024-12-20 待补时刻 | 2025-05-03..2025-05-08 | ETAPS umbrella: 106；TACAS: 46 | 🟢 已核验 |
| [`2024`](./2024/README.md) | ✅ 已结束 | [ETAPS 2024](https://etaps.org/2024/) | [CFP](https://etaps.org/2024/cfp/) | [Important Dates](https://etaps.org/2024/cfp/) | [TACAS track](https://etaps.org/2024/conferences/tacas/) | [EasyChair](https://easychair.org/conferences/?conf=tacas24) | [Program / Accepted](https://etaps.org/2024/past-conference/) | [Proceedings](https://etaps.org/about/proceedings/) | [DBLP TACAS 2024](https://dblp.org/db/conf/tacas/index.html#2024) | 2023-10-12 23:59 AoE | 2023-12-21 待补时刻 | 2024-04-06..2024-04-11 | ETAPS umbrella: 117；TACAS: 53 | 🟢 已核验 |
| [`2023`](./2023/README.md) | ✅ 已结束 | [ETAPS 2023](https://etaps.org/2023/) | [CFP](https://etaps.org/2023/cfp/) | [Important Dates](https://etaps.org/2023/cfp/) | 未找到独立 TACAS 分会页；fallback: [Programme](https://etaps.org/2023/programme/) / [Accepted papers](https://etaps.org/2023/accepted-papers/) | [EasyChair](https://easychair.org/conferences/?conf=tacas2023) | [Program / Accepted](https://etaps.org/2023/accepted-papers/) | [Proceedings](https://etaps.org/2023/proceedings/) | [DBLP TACAS 2023](https://dblp.org/db/conf/tacas/index.html#2023) | 2022-10-13 23:59 AoE | 2022-12-22 待补时刻 | 2023-04-22..2023-04-27 | ETAPS umbrella: 124；TACAS: 62 | 🟢 已核验 |
| [`2022`](./2022/README.md) | ✅ 已结束 | [ETAPS 2022](https://etaps.org/2022/) | [CFP](https://etaps.org/2022/call-for-papers.html) | [Important Dates](https://etaps.org/2022/call-for-papers.html) | [TACAS track](https://etaps.org/2022/tacas.html) | [EasyChair](https://easychair.org/conferences/?conf=tacas2022) | [Program / Accepted](https://etaps.org/user-profile/archive/53-etaps-2022/495-tacas-2022-accepted-papers.html) | [Proceedings](https://etaps.org/2022/proceedings.html) | [DBLP TACAS 2022](https://dblp.org/db/conf/tacas/index.html#2022) | 2021-10-14 23:59 AoE (= GMT-12) | 2021-12-23 待补时刻 | 2022-04-02..2022-04-07 | ETAPS umbrella: 112；TACAS: 50 | 🟢 已核验 |

## 7. 维护备注

- ETAPS umbrella 与 TACAS 分会不要拆目录：本库固定使用 `ccf_venues/conf-b-etaps/`。
- 年度页必须分别记录 ETAPS umbrella official count 与 TACAS official count；不能把 TACAS count 当作 ETAPS 总数。
- 2028 仅官方主页和会期可核验；CFP、dates、TACAS track、submission、program、proceedings 与 count 均未公布。
- 2023 未找到独立 TACAS 分会页时，根表与年度页均显式写作 `fallback`，避免把 ETAPS programme 误读为独立 TACAS track 页。
- 2026 / 2027 CFP 均写明 `All the dates are AoE`；投稿、artifact、rebuttal、notification、final version 等 deadline 默认按 AoE 口径记录，会期日期本身不按 AoE deadline 解释。
- 2027 ETAPS 年度主页 / CFP 给出 umbrella 会期 `2027-04-10..2027-04-15`，CFP 同时注明 Main conferences `2027-04-12..2027-04-15`；本库在根表与年度页同时保留两层日期。
- 2024 TACAS artifact deadline 存在版本差异，当前按已知官方证据记为 `2023-10-26 23:59 AoE`，并在年度页保留矛盾提示。

## 8. TIMELINE.md 同步提示

- 本 venue 的年度汇总表和各年度 README 是 [TIMELINE.md](../TIMELINE.md) 的事实来源之一。
- 若新增或修改本 venue 的投稿相关 important date、会期、论文名录 / proceedings 链接，必须同步更新 [TIMELINE.md](../TIMELINE.md) 的对应年度表格与 Mermaid Gantt。

## 9. 更新日志

> 更新日志按时间降序排列，最新修改在最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-04 22:20` | 统一论文数量单元格为 `ETAPS umbrella: N；TACAS: N` 口径。 |
| `2026-06-04 21:44` | 补充核心人员情报，并按 review 修正 accessDenied、计数或会期等事实口径。 |
| `2026-06-04 21:10` | 初始化 ETAPS / TACAS venue README，并建立 2022--2028 年度索引。 |
