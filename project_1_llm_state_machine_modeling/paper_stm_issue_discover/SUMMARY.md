# SUMMARY.md — 轻量总账与阅读入口

> 本文件只做**入口与索引**，不做第二事实源。⭐ 台账与历史 X1v2 精确网格回 [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/) 核对；当前 gpt-5.6-luna 双臂三轮 raw 运行与生成成本回 [全量报告](./reports/2026-08-19-luna-full-x3-v26.md) 核对，旧 hit/FP 数字已废止，严格人工结果尚未完成；判定口径一律回 [discover_matrix/docs/protocol/](./discover_matrix/docs/protocol/)；动态施工状态一律以 GitHub PR / issue 为准。

## 1. 一句话状态

paper1 已按 2026-08-07 / 08-08 导师定调收窄为 **issue discover 单独成篇**（repair 另立后续论文），一次完整的全量实验（**54 pair × 2 臂 × 3 轮 = 324 格**）已完成，工作重心转入**结果审计与论文写作**；同模型对照报告见 [2026-08-19-luna-full-x3-v26.md](./reports/2026-08-19-luna-full-x3-v26.md)。

**三条** contribution〔用户明确裁定 2026-08-11〕：① **基于模型转换 + 形式化检查 / 仿真 / 验证的错误发现方法**（独有的是**真值封存**）> ② **基于归纳后的谓词逻辑的断言体系**（⚠️ 这一条就是元模型本身）> ③ **issue 证据链体系**。⚠️ 此前本行写「两条」，系 2026-08-08 的旧口径，已被 08-11 裁定取代；真源是 [story/paper_story.md](./story/paper_story.md) §7。

## 2. 事实源索引

| 类型 | 入口 | 作用 |
| :-- | :-- | :-- |
| 论文口径基准 | [README.md](./README.md) | 这篇论文做什么、**三条** contribution、建模对象边界、目录导航 |
| 导师定调 | [../talks/](../talks/) | 最高优先级路线依据。⚠️ 2026-08-07 / 08-08 的收窄定调为口头，原话摘录在 [README.md](./README.md) §2 |
| ⭐ **当前实验事实** | [reports/2026-08-19-luna-full-x3-v26.md](./reports/2026-08-19-luna-full-x3-v26.md) 与 [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/) | 当前报告只提供 54 个 eligible pair 的 Luna v26-dnorm/X1v2 双臂三轮 raw 运行和生成成本；严格 hit/FP 必须按人工协议完成后另发，旧自动数字不是当前结果。 |
| ⚠️ 历史实验事实（v46） | [../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) | 建立在**已归档的第一版台账**上，⛔ 不是当前口径 |
| 判定口径 | [discover_matrix/docs/protocol/](./discover_matrix/docs/protocol/) | 命中判据、多报五类、方法出处、建模对象边界判据、规则出处纪律。**改它们等于改研究规则** |
| 实验产地 | [reports/](./reports/) 与 [discover_matrix/](./discover_matrix/) | reports 保存当前同模型对照和逐条台账导出；discover_matrix 保存唯一台账、历史 X1v2 精确网格、协议与证据链。 |
| 方法实现 | [pipeline/feedback_loop/](./pipeline/feedback_loop/) | 当前活的实现（八阶段 + 定向反馈循环） |
| 语料 | [selected_seed_examples/](./selected_seed_examples/) | 60 个 pair，各含 `nl.txt`、`stm0.puml` 与溯源元数据 |
| 论文叙事 | [story/](./story/) | thesis、章节结构与 RQ、claim-evidence、任务边界、建模对象、术语 |
| 当前状态 | [STATUS.md](./STATUS.md) | 已完成 / 未完成 / 可声称 / 不可声称 / 风险 |
| 工作纪律 | [GUIDE.md](./GUIDE.md) | 事实源优先级、口径纪律、数字纪律、公平性纪律、验收清单、静态检查 |

## 3. 阅读入口（按任务）

| 我要做什么 | 读什么 |
| :-- | :-- |
| 理解这篇论文 | [README.md](./README.md) → 实验报告。两份读完即可完整理解方法与结果 |
| 写论文某一节 | [story/paper_outline.md](./story/paper_outline.md) 找结构 → [story/claim_evidence_map.md](./story/claim_evidence_map.md) 核 claim → [story/terminology_policy.md](./story/terminology_policy.md) 核措辞 |
| 复算某个数字 | [discover_matrix/README.md](./discover_matrix/README.md) 导航页 |
| 改方法 / 谓词 / 提示词 | 先读 [discover_matrix/docs/protocol/](./discover_matrix/docs/protocol/)，再动 [pipeline/feedback_loop/](./pipeline/feedback_loop/) |
| 查某个 pair 的原文 | [selected_seed_examples/](./selected_seed_examples/) |
| 追溯某条结论的来源 | [evidence/](./evidence/) |
| 考古（历史路线） | [archive/](./archive/)（本工作区快照）、[../archive/](../archive/)（已停用旧路线） |

## 4. 资产状态概览

| 类别 | 状态 | 入口 |
| :-- | :-- | :-- |
| 论文叙事（story） | 已按 discover 口径整体改写 | [story/](./story/) |
| 方法实现 | active，已跑通全量 | [pipeline/feedback_loop/](./pipeline/feedback_loop/) |
| 输入准备与表示桥、语料准入检查 | active，作为 infrastructure | [pipeline/conversion/](./pipeline/conversion/)、[pipeline/representation/](./pipeline/representation/)、[pipeline/readiness_audit/](./pipeline/readiness_audit/) |
| 上一版单 Agent 实现 | 已归档（2026-08-11），完整保留可复活 | [archive/r9_agent_loop_pipeline/](./archive/r9_agent_loop_pipeline/) |
| 实验与评测 | active；⭐ 第二版台账、历史 X1v2 精确网格和 Luna 同模型双臂报告均已就位；⛔ v46 主臂已归档 | [reports/](./reports/)、[discover_matrix/](./discover_matrix/) |
| 语料与更广候选集 | active | [selected_seed_examples/](./selected_seed_examples/)、[corpora/](./corpora/) |
| repair 期合同（issue lifecycle、source trace、资产地图） | **已随 repair 搁置**，只作历史背景与后续 repair 论文的迁移输入 | [experiment_design/](./experiment_design/)、[evidence/ledgers/](./evidence/ledgers/) |
| R5.7 / Better STM-facing 资产 | 已归档，只作 historical / superseded / calibration-only 引用 | [archive/](./archive/) |
| Path-1 评测链、旧 agent loop 基础设施、Path-1/Path-2 指南 | 已停用，完整保留可复活，不参与本文任何结论 | [../archive/](../archive/) |
| 阶段性报告 | 历史材料 | [reports/](./reports/) |

## 5. 下一步依赖（按优先级）

1. **完成严格人工重判**——只读取 D1/D2 final clusters，对方法与 X1v2 的每条 issue 和每条台账逐项给出人工理由；严禁脚本或 LLM judge 参与匹配。
2. **台账撰写过程的交代**——台账是能力分母，必须写清谁标的、何时标的、是否在看过方法产出之后标的、与命中判定是否同一人。
3. **人工判定的第二意见**——首轮全人工裁决完成后，对争议项做独立人工复核并保留仲裁理由。
4. **循环各阶段的消融**——两个审查阶段与静态预检占算力大头却无单独收益证据。
5. **若干纯统计项**——命中形态构成、拒答回灌量、命中位按实际支撑族重算。
6. 方法侧改进（模型驱动巡检入口、收断言侧过度规定、补中间表示损失、降方差、收需求集规模）影响下一代次，不阻塞写作。

逐项理由与受阻原因见 [STATUS.md](./STATUS.md) §3。

## 6. 禁止误读

- 不把本文读成 discover + repair 闭环——repair 是后续论文。
- 不把「loop + verification feedback」「中间表示」「ledger / audit」写成 contribution。
- 不把「发现了多少问题」当成贡献。
- 不把覆盖率写成点估计或区间估计——它只能作为上界，且必须与算力代价一起给。
- 不把多报侧读成误报率；不只报一套分母。
- 不把台账当缺陷全集；不把无台账记录的 pair 读作「这些模型无缺陷」。
- 不把两个执行模型的差异读成「某个模型更适合这项任务」。
- 不据谓词分层给出词表选型建议。
- 不声称「这些模型没有并发 / 时间问题」——我们排除的是无法判断的部分。
- 不在本工作区维护 PR / review / CI 等动态施工状态。

## 7. 相对上一版改了什么、为什么

| 改动 | 为什么 |
| :-- | :-- |
| §1 一句话状态从「资产清账完成、active 主线为 source-level issue discovery **and closure**、真实 repair loop 尚未运行」改为「已收窄为 discover 单独成篇、324 格全量实验已完成」 | 旧版写于实验之前，且口径已被 2026-08-07 / 08-08 定调取代 |
| ⚠️（历史，已被 2026-08-17 台账换代取代）§2 事实源表把实验报告标为**全部数字的唯一来源**，并显式声明本文件不做第二事实源 | 旧版的事实源表指向 asset map、scan audit、issue ledger schema 等 repair 期合同；且旧版容易被当成数字来源 |
| 新增 §3 按任务分叉的阅读入口 | 旧版只有一条线性阅读顺序，实际使用中「写论文」「复算数字」「改方法」三类任务读的东西完全不同 |
| §4 资产状态表新增「repair 期合同已搁置但文件仍在」一行 | 那批文件仍在原地，不写清会被后续 agent 当成 active 框架 |
| §5 下一步依赖从「先交付 Discover Agent，再依次交付 Repair / Confirm Agent，最后由确定性 controller 组织闭环」改为「补外部对照与审计」 | Discover 已实现并跑通全量；Repair / Confirm 已移出本文范围；当前真实缺口是对照而非实现 |
| §6 禁止误读全面重写 | 旧版七条中五条针对 Better STM 与 `fcstm`，已两代前作废 |
| 删除全部 GitHub PR / issue 链接（`#100` / `#152`） | 仓库根 §9：动态流程状态只维护在 GitHub |
| **保留并改写**：不把 `fcstm` / ledger / audit 写成 contribution、不把 conversion 算成 gain | 与新口径一致，且仍是真实的措辞回流风险 |
| **保留**：R5.7 / Better STM 资产只作 historical / calibration-only 引用 | 归档结论未变 |
