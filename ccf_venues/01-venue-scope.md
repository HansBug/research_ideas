# `ccf_venues/` 01-venue-scope

> 信息更新时间：`2026-06-09 20:50:00`（Asia/Shanghai）

## 1. 文档用途

本文档固定 `ccf_venues/` 的初始收录范围和分批策略。它不是最终完整 CCF 目录，而是围绕本仓库博士研究四个 project 的可执行 venue 情报建设清单。

## 2. 分批原则

1. **P0-A 强相关主线**：LLM4SE、需求到模型、MDE、状态机建模、软工综合顶会 / 顶刊，默认在 P0 阶段优先完成。
2. **P0-B 强相关验证线**：形式化方法、模型检查、测试验证、验证工具化，同样属于 P0 阶段验收目标，但可在 P0-A 后推进。
3. **P1 重要补链**：P0 完成后继续推进，主要补维护、演化、实证、工具化和可靠性链条。
4. **P2 邻近观察**：作为论文检索和分流投稿线索，暂不阻塞 P0/P1；PR-9 已基础建档但不改变其 P2 边界。
5. **暂不纳入**：与四个 project 关系弱、主要是系统/PL/AI 方法本身而非软工建模 / 验证问题的 venue，先不建目录。

## 3. CCF 官方核验说明

本轮范围划分已用 CCF 官方目录做过初步核验：

1. 软件工程 / 系统软件 / 程序设计语言 venue 以 <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/> 为主。
2. CAV 等理论类验证 venue 以 <https://www.ccf.org.cn/Academic_Evaluation/TCS/> 为主。
3. 旧材料中的 `EMSE` 在 CCF 官方页写作 `ESE`；旧材料中的 `TACAS` 在 CCF 官方页归入 `ETAPS`，本库用 `conf-b-etaps` 并在年度页跟踪其主会。
4. **CCF 第七版（2026-03-31 发布 / 2026-04-09 勘误）已成为当前有效版本**，来源与访问方式见 [README.md](./README.md) §3。`2026-08-07` 已按官方 PDF 全量复核本库 42 个 venue，**等级 42/42 全部不变**，本范围文档的 CCF 列无需修改。第七版**不列举 ETAPS 的任何子会议**（全 72 页 PDF 中无 TACAS / FASE / iFS 字样），因此 `conf-b-etaps` 的伞条目口径继续成立。

## 4. PR-5 冻结状态与后续执行合同

截至 PR-5，P0-A 与 P0-B 共 22 个 venue 已完成基础建档与部分核验，后续 P0 只做事实维护与缺口补证，不再作为待建清单管理。P1/P2 扩展必须按下表执行；更完整的执行纪律见 [GUIDE.md](./GUIDE.md) §14.1。SUMMARY 只保留读者查阅总表，不再承载执行合同。

| 子级 PR | 批次主题 | Venue ownership | 数量 | 默认年度 README | 前置条件 | 共享文件边界 |
|---|---|---|---:|---:|---|---|
| PR-6 | P1-Maintenance / Repair | `conf-b-saner`、`conf-b-icsme`、`conf-b-icpc`、`journal-b-jsep` | 4 | 28 | PR-5 ready / 合入上游后可开工；可与 PR-7 并行 | 只增量维护自有 venue 事实，不覆盖 P0 与其他 PR facts |
| PR-7 | P1-Empirical / Quality | `conf-b-esem`、`journal-b-ese`、`journal-b-jss`、`journal-c-sqj` | 4 | 28 | PR-5 ready / 合入上游后可开工；可与 PR-6 并行 | 只增量维护自有 venue 事实，不覆盖 P0 与其他 PR facts |
| PR-8 | P1-Formal / Toolchain | `journal-b-ist`、`journal-b-scp`、`conf-c-qrs`、`conf-c-tase` | 4 | 28 | PR-5 已合入上游后可并行开工；final ready 前必须 merge upstream 并吸收届时已合入 PR-6 / PR-7 的 GUIDE / SUMMARY 踩坑经验 | 只增量维护自有 venue 事实，不覆盖 P0 与其他 PR facts |
| PR-9 | P2 Neighboring Observation | `conf-c-apsec`、`conf-c-seke`、`conf-c-ease`、`conf-c-msr`、`conf-c-rv` | 5 | 35 | PR-6 / PR-7 / PR-8 / PR-9 均已合入上游；PR-9 final ready 前已 merge 最新上游并吸收适用踩坑规则 | 只增量维护邻近观察 venue，不升级为 P0/P1 主线 |
| PR-10 | P1/P2 Global Audit | 不新增 venue；审计 PR-6~PR-9 | 0 | 0 | PR-6 / PR-7 / PR-8 / PR-9 全部合入上游 | 统一复核统计、TIMELINE、Mermaid、更新日志、核心人员与待补项 |

约束：

1. PR-6~PR-9 不得静默新增合同外 venue；若 CCF 官方更名或确有强相关漏项，必须先更新本文档和 PR body，并附官方来源。
2. 每个 PR final ready 前必须 merge upstream staging head；若发生冲突，必须复审双方 facts、TIMELINE、Mermaid、更新日志与待补记录均未被覆盖。PR-8 可按本表修订后的并行合同开工，但 final ready 前必须确认已吸收当时上游已有的 PR-6 / PR-7 经验；PR-9 final ready 前必须吸收已合入 PR-6 / PR-7 / PR-8 的适用踩坑规则；不得只看 venue 清单跳过上游经验。
3. PR-6 / PR-7 / PR-8 作为 sibling PR 同时 open 时，共享文件统计默认是各自 branch-local 口径；任一 sibling 若不是第一个合入上游，必须在 merge upstream 后把统计与 facts 重算为组合口径。
4. [SUMMARY.md](./SUMMARY.md) 是读者查阅总账；本文档冻结范围和 ownership，不把待建 venue 写成已完成事实，也不把执行合同回写到 SUMMARY 正文。

## 5. P0-A 强相关主线 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-a-icse` | ICSE | 会议 | 🏆 | 软工综合最高目标，四个 project 都可对齐。 |
| `conf-a-fse` | FSE | 会议 | 🏆 | 软工综合顶会，适合 LLM4SE、修复、验证、建模。 |
| `conf-a-ase` | ASE | 会议 | 🏆 | 自动化软工主场，P1/P2/P4 强相关。 |
| `conf-a-issta` | ISSTA | 会议 | 🏆 | 测试与分析顶会，P2/P3/P4 强相关。 |
| `journal-a-tse` | TSE | 期刊 | 🏆 | 软工综合顶刊，四个 project 都可对齐。 |
| `journal-a-tosem` | TOSEM | 期刊 | 🏆 | 软工方法顶刊，P1/P2/P4 强相关。 |
| `conf-b-models` | MoDELS | 会议 | 🥈 | 建模与模型驱动核心 venue，P1 核心。 |
| `conf-b-re` | RE | 会议 | 🥈 | 需求工程核心 venue，P1/P2 核心。 |
| `journal-b-re` | Requirements Engineering | 期刊 | 🥈 | 需求工程期刊，P1/P2 直接对口。 |
| `journal-b-sosym` | SoSyM | 期刊 | 🥈 | 软件与系统建模期刊，P1/P3 直接对口。 |

## 6. P0-B 强相关验证线 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-a-fm` | FM | 会议 | 🏆 | 形式化方法主场，P2/P3 强相关。 |
| `conf-a-cav` | CAV | 会议 | 🏆 | 计算机辅助验证顶会，P3 的模型检查与验证剖面核心对口。 |
| `conf-b-etaps` | ETAPS（TACAS + iFS） | 会议 | 🥈 | CCF 目录以单一 `ETAPS` 伞条目收录（第七版 SE 会议 B #2，目录不列子会议）。**自 `2026-08-07` 起，本库跟踪的主会由「仅 TACAS」扩展为「TACAS + iFS」**：iFS 是 FASE 与 iFM 合并后的首届会议（ETAPS 2027 起），官方 scope 明列 requirements engineering、MDE、model learning、CPS/hybrid/real-time、AI-based systems 的 SE 基础，对 P1/P2/P4 的契合度高于偏工具算法的 TACAS；FASE 旧入口已 404。这是**同一 venue 目录内的跟踪范围扩展，不新增 venue 目录**。iFS 继承 ETAPS 的 B 类归属属推论而非目录明文，用于毕业成果认定前需另行确认。TACAS 仍作为 P3 与 pyfcstm / UPPAAL 工具化的主要跟踪分会。 |
| `conf-b-vmcai` | VMCAI | 会议 | 🥈 | 验证、模型检查、抽象解释，P3 核心。 |
| `conf-b-issre` | ISSRE | 会议 | 🥈 | 可靠性与验证，P2/P3 对口。 |
| `journal-b-stvr` | STVR | 期刊 | 🥈 | 测试、验证、可靠性，P2/P3 对口。 |
| `conf-c-icfem` | ICFEM | 会议 | 🥉 | 形式化工程方法，P2/P3 对口。 |
| `conf-c-spin` | SPIN | 会议 | 🥉 | 软件模型检查，P3 直接对口。 |
| `conf-c-atva` | ATVA | 会议 | 🥉 | 自动化验证与分析，P3 直接对口。 |
| `conf-c-icst` | ICST | 会议 | 🥉 | 测试、验证、确认，P2/P3/P4 对口。 |
| `conf-c-refsq` | REFSQ | 会议 | 🥉 | 需求质量与规约，P1/P2 对口。 |
| `journal-c-sttt` | STTT | 期刊 | 🥉 | 软件工具技术迁移，P3/P4 工具化产物友好。 |

## 7. P1 重要补链 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-b-saner` | SANER | 会议 | 🥈 | 演化、维护、重构、修复。 |
| `conf-b-icsme` | ICSME | 会议 | 🥈 | 软件维护与演化，P4 直接对口。 |
| `conf-b-icpc` | ICPC | 会议 | 🥈 | 程序理解，LLM 辅助理解与文档生成相关。 |
| `conf-b-esem` | ESEM | 会议 | 🥈 | 实证研究与评估，适合 LLM4SE 评测。 |
| `journal-b-ese` | ESE | 期刊 | 🥈 | 实证软工，benchmark / human study 对口。 |
| `journal-b-jss` | JSS | 期刊 | 🥈 | 软工综合与系统案例。 |
| `journal-b-ist` | IST | 期刊 | 🥈 | 软工综合，需求、测试、LLM4SE 常见。 |
| `journal-b-scp` | SCP | 期刊 | 🥈 | 形式化、程序与工具链。 |
| `journal-b-jsep` | JSEP | 期刊 | 🥈 | 软件演化与过程，P4 对口。 |
| `conf-c-qrs` | QRS | 会议 | 🥉 | 质量、可靠性、安全。 |
| `conf-c-tase` | TASE | 会议 | 🥉 | 理论软工与形式化。 |
| `journal-c-sqj` | SQJ | 期刊 | 🥉 | 软件质量与评估。 |

## 8. P2 邻近观察 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-c-apsec` | APSEC | 会议 | 🥉 | 区域性软工，常有 LLM4SE / 建模邻近论文。 |
| `conf-c-seke` | SEKE | 会议 | 🥉 | 知识工程与软工交叉。 |
| `conf-c-ease` | EASE | 会议 | 🥉 | 实证评估与研究方法。 |
| `conf-c-msr` | MSR | 会议 | 🥉 | 数据集、仓库挖掘、LLM4SE 实证。 |
| `conf-c-rv` | RV | 会议 | 🥉 | 运行时验证，与 P3 邻近。 |

## 8.4 CCF 第七版新增 / 升级带来的待评估候选（2026-08-07 登记，尚未纳入建档）

> 本节只登记候选与理由，**不等于已纳入 scope**。按 [GUIDE.md](./GUIDE.md) §12.9.4，新增 venue 目录前必须先在本文件与 PR body 中明确范围变更。以下条目均来自官方第七版 PDF 与官方第六版 HTML 分类页的逐行 diff（SE/SS/PL 与 TCS 两类的全部变动已锁定）。

| 名称 | 类型 | 第七版等级 | 变动 | 领域 | 相关 project | 相关度 | 建议 |
|---|---|---|---|---|---|---|---|
| FMCAD — Formal Methods in Computer-Aided Design | 会议 | 🥈 | **由 C 升 B** | TCS | P3 主 / P2 次 | 强 | **建议认真评估纳入**。模型检查 / SAT-SMT / 系统形式化验证与 project_3 主线高度重合，且可与已收录的 CAV(🏆) / VMCAI(🥈) / SPIN(🥉) / ATVA(🥉) 构成完整梯度。第六版时它是 TCS C，落在当时 scope 之外，故本库从未收录。 |
| MEMOCODE — International Conference on Formal Methods and Models for Co-Design | 会议 | 🥉 | **新增** | SE/SS/PL | P1 + P3 主 / P2 次 | 强 | **建议评估纳入**。会议名直接命中「形式化方法 + 模型」交叉定位，且面向嵌入式 / 控制系统协同设计，与本仓库 9 个控制系统数据集语境契合。 |
| CC — International Conference on Compiler Construction | 会议 | 🥈 | 新增 | SE/SS/PL | P4 边缘 | 弱—中 | 暂不纳入；仅登记。 |
| FSCD（原 RTA） | 会议 | 🥉 | 更名 | TCS | P3 边缘 | 弱—中 | 暂不纳入；仅登记更名事实。 |
| TQC — ACM Transactions in Quantum Computing | 期刊 | 🥉 | 新增 | TCS | 无 | 不相关 | 不纳入。 |
| SETTA | 会议 | 🥉 | 全称变更（删去 `Dependable`） | TCS | P3 边缘 | 弱 | 暂不纳入；仅登记。 |

**范围外提示（属「人工智能」大类，不在本库两个主类内，仅作 project_1 参考）**：第七版中 **ICLR 首次收录并直接进入 A 类**，**IJCAI 由 A 降为 B**。project_1 以 LLM 为核心方法，ICLR 进 A 会改变「LLM 方法侧成果」的可投 A 类池，做毕业成果规划时值得单独考虑，但本库不因此扩展 venue scope。

## 8.5 PR #63 LLM4Modeling-SE 扩展候选

PR #63 是在 PR #35 / PR #62 已合入后的用户指定补链，不属于 PR-6~PR-10 原冻结合同。它只补充 SE 大类中与 LLM4Modeling 主线足够贴合且规模可控的漏项，并要求 CCF 官方 / 镜像证据等级显式区分。

| 目录名 | Venue | 类型 | CCF | 相关理由 | 边界 |
|---|---|---|---|---|---|
| `journal-b-ase` | Automated Software Engineering Journal | 期刊 | 🥈 | 自动化软工期刊，P1/P2/P4 强相关；补齐已有 ASE 会议之外的期刊入口。 | 与 `conf-a-ase` 严格消歧；常规投稿 rolling，只有 official collection deadline 进入 TIMELINE。 |
| `conf-b-caise` | CAiSE | 会议 | 🥈 | Advanced Information Systems Engineering、概念建模、需求、MDE、过程与企业建模可承载 LLM-assisted modeling。 | 只作为 IS / conceptual modeling / MDE 分流，不写成泛 SE 主战场。 |
| `conf-c-iceccs` | ICECCS | 会议 | 🥉 | 复杂系统工程、requirements/specification、V&V、formal engineering methods 与 P2/P3 工程案例贴合。 | 🥉 档补充观察；不升级为 P0/P1 主投目标，2024/2027/2028 缺口不得伪造。 |

## 9. 更新日志

> 更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-08-07 20:40:00` | 2026-08 全量刷新：记录 CCF 第七版已成当前有效版本且本库 42/42 等级不变；把 `conf-b-etaps` 的跟踪主会由「仅 TACAS」扩展为「TACAS + iFS」（同目录内范围扩展，不新增 venue 目录）；新增 §8.4 登记第七版带来的待评估候选 FMCAD（C→B）、MEMOCODE（新增 C）等，并提示范围外的 ICLR 进 A / IJCAI 降 B。 |
| `2026-06-09 20:50:00` | 同步 CCF emoji 口径：将扩展候选边界中的旧字母等级表述改为 🥉 档补充观察，避免与正式 CCF emoji 列混淆。 |
| `2026-06-09 20:42:00` | 同步 SUMMARY 单表化纪律：P1/P2 ownership 与执行合同继续由本文和 GUIDE 承载，不再指向 SUMMARY 正文旧小节。 |
| `2026-06-09 18:08:00` | 修复 PR #91 subagent I 级反馈：将范围冻结表中的正式 `CCF` 列从旧式字母等级文本改为 🏆/🥈/🥉 emoji，避免与 SUMMARY / TIMELINE 等总账口径分裂。 |
| `2026-06-07 12:47` | PR #63 增补 LLM4Modeling-SE 扩展候选：新增 Automated Software Engineering Journal、CAiSE、ICECCS 三个 venue，并明确其不回写为 PR-6~PR-10 原冻结合同。 |
| `2026-06-06 00:16` | PR-10 全局审计执行：范围清单不新增 venue，继续确认 P2 邻近观察不升级为 P0/P1，完成状态由 SUMMARY 维护。 |
| `2026-06-05 23:06` | PR-9 冲突后复审修复：保持 PR-6 / PR-7 / PR-8 / PR-9 facts 共存，并由 SUMMARY 记录 PR-9 已完成基础建档状态。 |
| `2026-06-05 22:34` | PR-9 merge 最新上游 PR-8：当前合流后 PR-6 / PR-7 / PR-8 / PR-9 facts 共存，PR-9 仍只作为 P2 邻近观察；完成状态继续由 [SUMMARY.md](./SUMMARY.md) 维护。 |
| `2026-06-05 21:16` | PR-8 merge 最新上游 PR-6 / PR-7：本文继续只冻结范围和 ownership，完成状态由 [SUMMARY.md](./SUMMARY.md) 维护；PR-6 / PR-7 / PR-8 当前均已建档，PR-9 / PR-10 仍按原合同推进。 |
| `2026-06-05 19:16` | 修复 PR-8 实现后 review：补充 PR-6/7/8 sibling PR 的 branch-local 统计与 merge-upstream 组合重算纪律。 |
| `2026-06-05 18:13` | PR-6 收尾复核：明确 PR-6 ownership 当前分支已执行，同时保留 P0 22/154 冻结基线。 |
| `2026-06-05 18:04` | PR-6 当前分支已按 ownership 建立 SANER / ICSME / ICPC / JSEP 目录；本文档继续只维护范围合同，完成状态以 [SUMMARY.md](./SUMMARY.md) 为准。 |
| `2026-06-05 16:58` | PR-8 计划审查修复：同步 PR-8 并行开工合同，明确 PR-5 后可开工但 final ready 前必须 merge upstream 并吸收届时已合入 PR-6/7 经验。 |
| `2026-06-05 15:59` | 实现后 review 修复：为 PR-6~PR-10 合同补充前置条件列，并明确 PR-8 / PR-9 不得跳过上游踩坑经验。 |
| `2026-06-05 15:36` | PR-5 冻结 P0 完成状态与 PR-6~PR-10 P1/P2 ownership：本文档保留范围和执行合同，完成状态继续由 [SUMMARY.md](./SUMMARY.md) 维护。 |
| `2026-06-05 00:36` | 合入期刊试点后确认范围清单不做事实 ownership 记录，P0 完成状态统一由 [SUMMARY.md](./SUMMARY.md) 维护。 |
| `2026-06-04 23:04` | 同步全库更新日志降序口径；PR-1A / PR-1B 并行期间，P0 状态由 SUMMARY 记录具体 owner，本文仅保留范围边界。 |
| `2026-06-04 18:55` | 根据 multi-agent review 拆分 P0-A/P0-B，补入形式化验证强相关 venue，并明确 P1/P2 不阻塞当前 P0 验收。 |
