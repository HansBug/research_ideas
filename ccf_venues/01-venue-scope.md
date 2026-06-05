# `ccf_venues/` 01-venue-scope

> 信息更新时间：`2026-06-05 19:16`（Asia/Shanghai）

## 1. 文档用途

本文档固定 `ccf_venues/` 的初始收录范围和分批策略。它不是最终完整 CCF 目录，而是围绕本仓库博士研究四个 project 的可执行 venue 情报建设清单。

## 2. 分批原则

1. **P0-A 强相关主线**：LLM4SE、需求到模型、MDE、状态机建模、软工综合顶会 / 顶刊，默认在 P0 阶段优先完成。
2. **P0-B 强相关验证线**：形式化方法、模型检查、测试验证、验证工具化，同样属于 P0 阶段验收目标，但可在 P0-A 后推进。
3. **P1 重要补链**：P0 完成后继续推进，主要补维护、演化、实证、工具化和可靠性链条。
4. **P2 邻近观察**：作为论文检索和分流投稿线索，暂不阻塞 P0/P1。
5. **暂不纳入**：与四个 project 关系弱、主要是系统/PL/AI 方法本身而非软工建模 / 验证问题的 venue，先不建目录。

## 3. CCF 官方核验说明

本轮范围划分已用 CCF 官方目录做过初步核验：

1. 软件工程 / 系统软件 / 程序设计语言 venue 以 <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/> 为主。
2. CAV 等理论类验证 venue 以 <https://www.ccf.org.cn/Academic_Evaluation/TCS/> 为主。
3. 旧材料中的 `EMSE` 在 CCF 官方页写作 `ESE`；旧材料中的 `TACAS` 在 CCF 官方页归入 `ETAPS`，本库用 `conf-b-etaps` 并在年度页重点跟踪 TACAS。

## 4. PR-5 冻结状态与后续执行合同

截至 PR-5，P0-A 与 P0-B 共 22 个 venue 已完成基础建档与部分核验，后续 P0 只做事实维护与缺口补证，不再作为待建清单管理。P1/P2 扩展必须按下表执行；更完整的验收规则见 [SUMMARY.md](./SUMMARY.md) §9。

| 子级 PR | 批次主题 | Venue ownership | 数量 | 默认年度 README | 前置条件 | 共享文件边界 |
|---|---|---|---:|---:|---|---|
| PR-6 | P1-Maintenance / Repair | `conf-b-saner`、`conf-b-icsme`、`conf-b-icpc`、`journal-b-jsep` | 4 | 28 | PR-5 ready / 合入上游后可开工；可与 PR-7 并行 | 只增量维护自有 venue 事实，不覆盖 P0 与其他 PR facts |
| PR-7 | P1-Empirical / Quality | `conf-b-esem`、`journal-b-ese`、`journal-b-jss`、`journal-c-sqj` | 4 | 28 | PR-5 ready / 合入上游后可开工；可与 PR-6 并行 | 只增量维护自有 venue 事实，不覆盖 P0 与其他 PR facts |
| PR-8 | P1-Formal / Toolchain | `journal-b-ist`、`journal-b-scp`、`conf-c-qrs`、`conf-c-tase` | 4 | 28 | PR-5 已合入上游后可并行开工；final ready 前必须 merge upstream 并吸收届时已合入 PR-6 / PR-7 的 GUIDE / SUMMARY 踩坑经验 | 只增量维护自有 venue 事实，不覆盖 P0 与其他 PR facts |
| PR-9 | P2 Neighboring Observation | `conf-c-apsec`、`conf-c-seke`、`conf-c-ease`、`conf-c-msr`、`conf-c-rv` | 5 | 35 | PR-6 与 PR-7 已合入上游；建议等待或同步阅读 PR-8 形式化 / 工具链踩坑记录 | 只增量维护邻近观察 venue，不升级为 P0/P1 主线 |
| PR-10 | P1/P2 Global Audit | 不新增 venue；审计 PR-6~PR-9 | 0 | 0 | PR-6 / PR-7 / PR-8 / PR-9 全部合入上游 | 统一复核统计、TIMELINE、Mermaid、更新日志、核心人员与待补项 |

约束：

1. PR-6~PR-9 不得静默新增合同外 venue；若 CCF 官方更名或确有强相关漏项，必须先更新本文档和 PR body，并附官方来源。
2. 每个 PR final ready 前必须 merge upstream staging head；若发生冲突，必须复审双方 facts、TIMELINE、Mermaid、更新日志与待补记录均未被覆盖。PR-8 可按本表修订后的并行合同开工，但 final ready 前必须确认已吸收当时上游已有的 PR-6 / PR-7 经验；不得只看 venue 清单跳过上游经验。
3. PR-6 / PR-7 / PR-8 作为 sibling PR 同时 open 时，共享文件统计默认是各自 branch-local 口径；任一 sibling 若不是第一个合入上游，必须在 merge upstream 后把统计与 facts 重算为组合口径。
4. [SUMMARY.md](./SUMMARY.md) 是完成状态总账；本文档只冻结范围和 ownership，不把待建 venue 写成已完成事实。

## 5. P0-A 强相关主线 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-a-icse` | ICSE | 会议 | A | 软工综合最高目标，四个 project 都可对齐。 |
| `conf-a-fse` | FSE | 会议 | A | 软工综合顶会，适合 LLM4SE、修复、验证、建模。 |
| `conf-a-ase` | ASE | 会议 | A | 自动化软工主场，P1/P2/P4 强相关。 |
| `conf-a-issta` | ISSTA | 会议 | A | 测试与分析顶会，P2/P3/P4 强相关。 |
| `journal-a-tse` | TSE | 期刊 | A | 软工综合顶刊，四个 project 都可对齐。 |
| `journal-a-tosem` | TOSEM | 期刊 | A | 软工方法顶刊，P1/P2/P4 强相关。 |
| `conf-b-models` | MoDELS | 会议 | B | 建模与模型驱动核心 venue，P1 核心。 |
| `conf-b-re` | RE | 会议 | B | 需求工程核心 venue，P1/P2 核心。 |
| `journal-b-re` | Requirements Engineering | 期刊 | B | 需求工程期刊，P1/P2 直接对口。 |
| `journal-b-sosym` | SoSyM | 期刊 | B | 软件与系统建模期刊，P1/P3 直接对口。 |

## 6. P0-B 强相关验证线 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-a-fm` | FM | 会议 | A | 形式化方法主场，P2/P3 强相关。 |
| `conf-a-cav` | CAV | 会议 | A | 计算机辅助验证顶会，P3 的模型检查与验证剖面核心对口。 |
| `conf-b-etaps` | ETAPS / TACAS | 会议 | B | CCF 目录列为 ETAPS，实际维护时重点跟踪 TACAS 等验证相关分会，P3 与 pyfcstm / UPPAAL 工具化相关。 |
| `conf-b-vmcai` | VMCAI | 会议 | B | 验证、模型检查、抽象解释，P3 核心。 |
| `conf-b-issre` | ISSRE | 会议 | B | 可靠性与验证，P2/P3 对口。 |
| `journal-b-stvr` | STVR | 期刊 | B | 测试、验证、可靠性，P2/P3 对口。 |
| `conf-c-icfem` | ICFEM | 会议 | C | 形式化工程方法，P2/P3 对口。 |
| `conf-c-spin` | SPIN | 会议 | C | 软件模型检查，P3 直接对口。 |
| `conf-c-atva` | ATVA | 会议 | C | 自动化验证与分析，P3 直接对口。 |
| `conf-c-icst` | ICST | 会议 | C | 测试、验证、确认，P2/P3/P4 对口。 |
| `conf-c-refsq` | REFSQ | 会议 | C | 需求质量与规约，P1/P2 对口。 |
| `journal-c-sttt` | STTT | 期刊 | C | 软件工具技术迁移，P3/P4 工具化产物友好。 |

## 7. P1 重要补链 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-b-saner` | SANER | 会议 | B | 演化、维护、重构、修复。 |
| `conf-b-icsme` | ICSME | 会议 | B | 软件维护与演化，P4 直接对口。 |
| `conf-b-icpc` | ICPC | 会议 | B | 程序理解，LLM 辅助理解与文档生成相关。 |
| `conf-b-esem` | ESEM | 会议 | B | 实证研究与评估，适合 LLM4SE 评测。 |
| `journal-b-ese` | ESE | 期刊 | B | 实证软工，benchmark / human study 对口。 |
| `journal-b-jss` | JSS | 期刊 | B | 软工综合与系统案例。 |
| `journal-b-ist` | IST | 期刊 | B | 软工综合，需求、测试、LLM4SE 常见。 |
| `journal-b-scp` | SCP | 期刊 | B | 形式化、程序与工具链。 |
| `journal-b-jsep` | JSEP | 期刊 | B | 软件演化与过程，P4 对口。 |
| `conf-c-qrs` | QRS | 会议 | C | 质量、可靠性、安全。 |
| `conf-c-tase` | TASE | 会议 | C | 理论软工与形式化。 |
| `journal-c-sqj` | SQJ | 期刊 | C | 软件质量与评估。 |

## 8. P2 邻近观察 venue

| 目录名 | Venue | 类型 | CCF | 相关理由 |
|---|---|---|---|---|
| `conf-c-apsec` | APSEC | 会议 | C | 区域性软工，常有 LLM4SE / 建模邻近论文。 |
| `conf-c-seke` | SEKE | 会议 | C | 知识工程与软工交叉。 |
| `conf-c-ease` | EASE | 会议 | C | 实证评估与研究方法。 |
| `conf-c-msr` | MSR | 会议 | C | 数据集、仓库挖掘、LLM4SE 实证。 |
| `conf-c-rv` | RV | 会议 | C | 运行时验证，与 P3 邻近。 |

## 9. 更新日志

> 更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-05 19:16` | 修复 PR-8 实现后 review：补充 PR-6/7/8 sibling PR 的 branch-local 统计与 merge-upstream 组合重算纪律。 |
| `2026-06-05 16:58` | PR-8 计划审查修复：同步 PR-8 并行开工合同，明确 PR-5 后可开工但 final ready 前必须 merge upstream 并吸收届时已合入 PR-6/7 经验。 |
| `2026-06-05 15:59` | 实现后 review 修复：为 PR-6~PR-10 合同补充前置条件列，并明确 PR-8 / PR-9 不得跳过上游踩坑经验。 |
| `2026-06-05 15:36` | PR-5 冻结 P0 完成状态与 PR-6~PR-10 P1/P2 ownership：本文档保留范围和执行合同，完成状态继续由 [SUMMARY.md](./SUMMARY.md) 维护。 |
| `2026-06-05 00:36` | 合入期刊试点后确认范围清单不做事实 ownership 记录，P0 完成状态统一由 [SUMMARY.md](./SUMMARY.md) 维护。 |
| `2026-06-04 23:04` | 同步全库更新日志降序口径；PR-1A / PR-1B 并行期间，P0 状态由 SUMMARY 记录具体 owner，本文仅保留范围边界。 |
| `2026-06-04 18:55` | 根据 multi-agent review 拆分 P0-A/P0-B，补入形式化验证强相关 venue，并明确 P1/P2 不阻塞当前 P0 验收。 |
