# Path 2 — 差异化路线决策报告（v5 outline，待数据填充）

> **状态**：sprint 进行中 — 数据集选样完成（commit `259e6ea7`），run_path2.py + 5-condition 实验未跑；本文件按 [PATH2_DIFFERENTIATION_GUIDE §8](./PATH2_DIFFERENTIATION_GUIDE.md#8-path2_reportmd-产出要求) v5 outline 写出骨架，Phase 6 收口时填数据。
>
> **创建日期**：2026-05-26（v4.1 sprint 开工前占位）
>
> **v5 修订日期**：2026-05-27（categorical-differentiation framing 纠偏 — 删除 ref-free 作为 contribution；§1 重写为论证骨架；feature utilization 作主报道指标；5-condition matrix）

## 接管入口

新 Claude / codex session 进入 `dev/path2-differentiation` branch 后，按以下顺序读：

1. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) — meta-level 路线规划与 §4.1 决策准则
2. [PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md) — Path 2 接管指引（v5：§1 论证骨架 + §4 5-condition 矩阵 + §6 feature utilization + 4 intrinsic + §8 REPORT 产出要求 + §11.3.0 三段论 framing）
3. [../method/STATUS.md](../method/STATUS.md) — method 实装进度
4. [../eval/data/path2_selection/REPORT.md](../eval/data/path2_selection/REPORT.md) — 15+15 选样详细报告（含 30 case 严格溯源扩充 NL + provenance 表）

## Sprint Phase 进度

| Phase | 状态 | 备注 |
| --- | --- | --- |
| 0-3 method/ + eval/ 共同基础 | ✅ 完成（PR #11 merged） | Phase A-G + I 全套实装 |
| 4 — sources_path2.parquet 选样 | ✅ 完成（commit `259e6ea7`） | 15 candidates + 15 backup，30 case 严格溯源扩充 NL 完成 |
| **5 — Path 2 run_path2 实验（5 conditions × 15 candidates = 75 主行）** | 🔁 待开工 | 需先实装 `method/loop.py` 的 `target_dsl` + `modeling_mode="hybrid"` 分支 + 8 个 hybrid prompts |
| 6 — feature utilization + 4 intrinsic 聚合 | 🔁 待 Phase 5 | summary.json + 本文档 §4-§7 填数据 |
| 7 — 收口 + PR | 🔁 待 Phase 6 | 本 branch PR 不自动合并，等用户综合决策 |

---

## §1 控制系统问题定义 + 4 失败模式 + 4 grounding 一对一映射

> **填充指引**：直接复用 [GUIDE §1.1-§1.4](./PATH2_DIFFERENTIATION_GUIDE.md#11-控制系统-nl-to-stm-是一类独立问题) 内容。这是 PATH2_REPORT 的论证骨架，不是只在 §7 才出现的辅助信息。

### §1.1 控制系统作为一类独立问题对象

[ 待填：复用 GUIDE §1.1，含 4 个本质特征 ]

### §1.2 baseline 在 4 个特征上的失败模式

[ 待填：复用 GUIDE §1.2，含失败模式对照表 ]

### §1.3 pyfcstm 4 条 DSL-level feature 一对一覆盖

[ 待填：复用 GUIDE §1.3，含三段论 mapping 表 ]

---

## §2 method overview + 4 contribution 速查表

> **填充指引**：复用 [GUIDE §1.6 + §11.3 + §11.4](./PATH2_DIFFERENTIATION_GUIDE.md#16-4-条-method-contribution-paper-1-直接复用)。明确写 paper §1 contributions 是 **C1-C4 method core**，**不写 ref-free**。

### §2.1 Agent loop architecture overview

[ 待填：method overview pipeline 图 ]

### §2.2 4 条 method contribution

| # | Contribution | 对应 pyfcstm feature | 对应控制系统特征 |
| --- | --- | --- | --- |
| C1 | In-loop deterministic feedback via speculative validation | `SimulationRuntime` DFS validation | 周期执行 + 强 invariant |
| C2 | Language-independent expression IR enables symbolic reasoning | `Expr` IR + `solver/` Z3 集成 | 数值密集 guards / effects |
| C3 | DSL-native aspect AOP + forced fault paths | `>> during before/after` + `!` forced | per-tick invariant + fault recovery |
| C4 | Abstract action + read-only context | `enter abstract` + `@abstract_handler` | 硬件解耦 |

---

## §3 实验配置 + 5 conditions 矩阵

### §3.1 数据集

- 主数据集：[`eval/data/sources_path2.parquet`](../eval/data/sources_path2.parquet) — 15 candidates
- 备选：[`eval/data/sources_path2_backup.parquet`](../eval/data/sources_path2_backup.parquet) — 15 backup
- 选样口径：T0 严格 + 双 🟢A + 💎 数据集角色 + 结构标签 ∈ {`-`, `层次`} + state_count ≤ 20
- 桶分布：HSM-layered 6 / EFSM-interlock 6 / FSM-basic 3
- 领域覆盖：⚙️ ×4 / 🏭 ×2 / 🅿️ ×2 / 🌡️ ×2 / ✈️ ×2 / 🚗 ×1 / 🏢 ×1 / 🚆 ×1（共 7 领域）
- 详细选样过程 / codex 评审 / 30 case 严格溯源扩充 NL 见 [`eval/data/path2_selection/REPORT.md`](../eval/data/path2_selection/REPORT.md)

### §3.2 5 conditions 参数

| Condition | target_dsl | strategy | n_iter | feedback_sources | 用途 |
| --- | --- | --- | ---: | --- | --- |
| `A0_single_umple` | umple | single-prompt | 1 | 空 | DSL expressiveness gap baseline #1（baseline 论文 §III.B 风格） |
| `A0_hybrid_umple` | umple | hybrid 4-step | 4 | 空 | DSL expressiveness gap baseline #2（baseline 论文 §III.D Hybrid 复现，**baseline-of-record**）|
| `A0_single_pyfcstm` | pyfcstm | single-prompt | 1 | 空 | DSL 同源对照 #1 |
| `A0_hybrid_pyfcstm` | pyfcstm | hybrid 4-step | 4 | 空 | DSL 同源对照 #2（**主要比较对照**：与 A_full_ours 同 DSL 同等步数，差异只在 deterministic feedback）|
| `A_full_ours` | pyfcstm | agent loop（MTI 6-step + cascaded repair）| 3 | `["parse","semantic","sim"]` | **method-of-record** |

### §3.3 实际跑的 LLM model + 资源 footprint

- LLM_MODEL: [待填，从 `.env` 实际值]
- 总 LLM calls: [待填，预算 ~345]
- Wall time: [待填，预算 ~25-30 min 并发 -P 6]
- Token 消耗: [待填]

---

## §4 主结果表 — Feature utilization rate（v5 主报道指标）

> **填充指引**：5 conditions × 4 feature 的使用率矩阵。这是 §1.2 失败模式 + §1.3 grounding 一对一映射的**直接实证**。

### §4.1 主表：feature utilization 全量

| Condition | DuringBlock (C1) | MultiVarGuard (C2) | ForcedTransition (C3) | AbstractAction (C4) | 4-feature mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| A0_single_umple | 0% (struct) | N/A | 0% (struct) | 0% (struct) | — |
| A0_hybrid_umple | 0% (struct) | N/A | 0% (struct) | 0% (struct) | — |
| A0_single_pyfcstm | [待填]% | [待填]% | [待填]% | [待填]% | [待填] |
| A0_hybrid_pyfcstm | [待填]% | [待填]% | [待填]% | [待填]% | [待填] |
| A_full_ours | [待填]% | [待填]% | [待填]% | [待填]% | [待填] |

### §4.2 主 lift 对比

#### A_full_ours vs A0_hybrid_pyfcstm — 隔离 deterministic feedback 收益

| Feature | A_full_ours | A0_hybrid_pyfcstm | Lift |
| --- | ---: | ---: | ---: |
| DuringBlock | [待填] | [待填] | +[待填]pp |
| MultiVarGuard | [待填] | [待填] | +[待填]pp |
| ForcedTransition | [待填] | [待填] | +[待填]pp |
| AbstractAction | [待填] | [待填] | +[待填]pp |
| **4-feature mean** | [待填] | [待填] | **+[待填]pp** |

[ 解释：同 DSL target (pyfcstm)，同等步数级别 strategy，差异只在 deterministic feedback。这个 lift 是 paper §4 主报道数字。 ]

#### A0_hybrid_pyfcstm vs A0_hybrid_umple — 直接展示 DSL expressiveness gap

[ 解释：同 strategy (Hybrid 4-step)，差异只在 DSL target。Umple 在 3/4 feature 上结构性为 0；MultiVarGuard 标 N/A。 ]

#### A_full_ours vs A0_hybrid_umple — method-of-record vs baseline-of-record

[ 解释：完整 method 横向对比完整 baseline，作为 paper §4 secondary 主表。 ]

---

## §5 辅助表 — 4 intrinsic lift × 5 conditions × 3 buckets

> **填充指引**：4 intrinsic（ParseRate / SemValidRate / SimRate / ReachabilityRate）作为 sanity 辅助指标。Umple condition 的 SimRate / ReachRate 标 N/A 不是数据缺失，是 §1.2 失败模式"周期执行"的体现。

### §5.1 全量 intrinsic 表

| Condition | ParseRate | SemValidRate | SimRate | ReachabilityRate | 4-intrinsic mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| A0_single_umple | [待填] | [待填] | N/A | N/A | — |
| A0_hybrid_umple | [待填] | [待填] | N/A | N/A | — |
| A0_single_pyfcstm | [待填] | [待填] | [待填] | [待填] | [待填] |
| A0_hybrid_pyfcstm | [待填] | [待填] | [待填] | [待填] | [待填] |
| A_full_ours | [待填] | [待填] | [待填] | [待填] | [待填] |

### §5.2 按桶分层 intrinsic lift（A_full_ours - A0_hybrid_pyfcstm）

| 桶 | n | ParseRate lift | SemValid lift | SimRate lift | Reach lift |
| --- | ---: | ---: | ---: | ---: | ---: |
| HSM-layered (C1+C3 主战场) | 6 | [待填] | [待填] | [待填] | [待填] |
| EFSM-interlock (C2 主战场) | 6 | [待填] | [待填] | [待填] | [待填] |
| FSM-basic (C4 baseline) | 3 | [待填] | [待填] | [待填] | [待填] |

---

## §6 per-C-axis stratified lift（v5 新增 — 直接实证 §1.3 mapping）

> **填充指引**：用 [eval/data/path2_selection/expansions/](../eval/data/path2_selection/expansions/) 里每个 case 的 `axis_coverage` 标签（C1🟢/🟡/🟠/⚪）分组，看 lift 是否真的落在对应 axis 上。这是 §1.3 三段论 mapping 的**最直接**实证。

### §6.1 按 axis_coverage 标签分组的 feature utilization lift

| Axis 暴露强度 | n cases | DuringBlock lift | MultiVarGuard lift | ForcedTransition lift | AbstractAction lift |
| --- | ---: | ---: | ---: | ---: | ---: |
| C1🟢 (高暴露) | 6 (15 candidate 中) | [待填] | — | — | — |
| C2🟢 (高暴露) | 9 | — | [待填] | — | — |
| C3🟢 (高暴露) | 9 | — | — | [待填] | — |
| C4🟢 (高暴露) | 14 | — | — | — | [待填] |

### §6.2 解释

[ 待填：lift 是否落在对应 axis 上？若 C1🟢 cases 上 DuringBlock lift 明显高于 C1🟡 / C1🟠 / C1⚪ cases，说明 method 的 grounding 收益与原文语义需求确实对齐 — 这就是 §1.3 三段论 mapping 的实证证据。 ]

---

## §7 spot-check / confounders / 信号判定

### §7.1 spot-check（可选）

[ 待填：3-5 case 走 [`eval/`](../eval/) LLM-初审 + 人类签字 5-component manual eval；判定 manual eval 与 feature utilization / intrinsic 方向是否一致 ]

### §7.2 confounders

[ 待填：API 失败 / parse 失败样本；Umple parser 不稳；Umple Hybrid strategy 实装稳定性；abstract handler 缺失 → SimRate=0；任何与 GUIDE §9 风险表对应的实际触发 ]

### §7.3 信号判定（v5 修订准则）

按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S1/S2/S3/S4 + **v5 修订阈值**：

- **S2 差异化信号强**（v5 阈值）：feature utilization mean lift (A_full_ours - A0_hybrid_pyfcstm) ≥ 25pp，且 ≥3 个 feature 各自 lift ≥ 15pp
- **S4 信号弱**：feature utilization mean lift < 15pp，或 4 个 feature 中 ≥2 个 lift < 10pp

[ 待填：当前数据落在 S1/S2/S3/S4 哪一档 ]

---

## §8 Claude 的方向建议 + rationale + 后续工作量

### §8.1 方向建议

[ 待填：**Claude 不下结论，最终方向由用户拍板**。本节给依据 + rationale，不强推 ]

### §8.2 若选 Path 2，后续 1-2 个月工作量预估

[ 待填，参考列表：]
- 接 Phase H LLM-as-judge feedback channel（补回 5-intrinsic + 5th feedback source）
- 扩 sources/ 候选池到 ≥60 条（按桶 + 按 C-axis 完整覆盖）
- cross-vendor sanity：Claude 4.7 vs GPT-5.5 对照
- 对照 llms_emp 两阶段框架（NL → PlantUML SysML，与我们 NL → pyfcstm 对比）
- 对照 ttool-ai 自动反馈循环（NL → AVATAR SysML，与我们对比）
- 对照 IEC 61499 iterative refinement（NL → IEC 61499 code，看 fully-automated vs human-in-the-loop 差异）
- formal verification benchmark 集成（UPPAAL / NuSMV 等 backend）
- paper §5 limitations + threats to validity 论述

---

## 参考工件

- 选样工件：[`eval/data/path2_selection/`](../eval/data/path2_selection/) — pool.tsv / selection.json / expansions/*.json / briefs/ / results/*.json / REPORT.md
- 主数据集：[`eval/data/sources_path2.parquet`](../eval/data/sources_path2.parquet)
- 备选数据集：[`eval/data/sources_path2_backup.parquet`](../eval/data/sources_path2_backup.parquet)
- 实验结果（待跑）：`eval/results/sprint_path2/predictions.parquet` + `summary.json`
- GUIDE 主文档：[PATH2_DIFFERENTIATION_GUIDE.md](./PATH2_DIFFERENTIATION_GUIDE.md)（v5）
