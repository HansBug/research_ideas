# R7 source-level issue lifecycle 脚手架（cold archive）

> **Cold archive / repair 期脚手架 / 内含大量仍然有效的 discover 材料。**
> 本目录保存 2026-07 「source-level issue discovery → repair → confirm → closure」阶段
> 建立的实验设计脚手架（25 份），以及支撑那次战略转向的两份 evidence ledger（2 份）。
>
> ⚠️ **归档理由是「阶段整体退役」，不是「内容全错」。**
> `experiment_design/issue_lifecycle/` 里约八成是**纯 discover 材料**，与当前论文口径不冲突。
> 逐项清单见 §3——那是本归档最重要的一节。

## 0. 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原路径 | `paper_stm_issue_discover/experiment_design/`（25 份）＋ `paper_stm_issue_discover/evidence/ledgers/{legacy_asset_inheritance.md, paper1_strategy_asset_map.md}`（2 份） |
| 内容冻结时间 | 2026-07-07 至 2026-07-20（各文件末尾的更新日志给出逐份时间） |
| 归档时间 | 2026-08-11 |
| 归档动作 | `git mv`，27 个文件全部为 rename，内容未改；只机械调整了相对链接深度（详见 §7） |
| 退役声明来源 | [experiment_design/README.md](./experiment_design/README.md) 页首已自行宣布「本目录不在当前运行路径上，也不是 paper1 的实验设计真源」 |

## 1. 这是什么

2026-07-07 导师战略讨论后，paper1 从 Better STM 框架转向「source-level behavioral issue
discovery and closure」。本目录是那一轮为**整条 Discover → Repair → Confirm → Closure
生命周期**搭的设计脚手架，外加记录那次转向的两份资产台账。

```
experiment_design/                  25 份
├── README.md / SUMMARY.md / GUIDE.md      顶层协议块清单与设计纪律
├── issue_lifecycle/                 11 份  issue 状态机 v0 合同 ＋ 6 个 fixture
├── source_trace/                    11 份  raw/source ↔ 中间表示 trace v0 合同 ＋ 6 个 fixture
└── metrics/README.md                 1 份  指标占位（当时全部「未冻结」）

evidence_ledgers/                    2 份
├── legacy_asset_inheritance.md            旧资产继承边界（把 thesis 定义成 repair / refinement）
└── paper1_strategy_asset_map.md           07-07 转向的施工地图（A-001 – A-024）
```

## 2. 为什么归档

**三批的理由各不相同：**

1. **`experiment_design/` 顶层（README / SUMMARY / GUIDE / metrics）**——它规划的多数协议块
   *从未实现，也不再计划实现*：Repair dispositions、Confirm decisions、deterministic B loop、
   B-final、post-Confirm export、closure / regression audit。2026-08 paper1 收窄为
   issue discover 单独成篇，这些块整体属于后续 repair 论文。实际落地的只有两份 v0 字段合同。
2. **`source_trace/`**——其 v0 合同的核心产出（`projection_status`、`closure_claim_allowed`）
   服务的是「修完之后能不能声称闭合」，是纯 repair 侧的门。且它自己的页首已声明
   v0 只是 legacy migration contract，active ingress 早已改用 `source_trace_base.v1`。
3. **`evidence_ledgers/` 两份**——`legacy_asset_inheritance.md` §3 把 thesis 直接定义成
   `<NL, STM_0> -> STM_k / Better STM` 的 repair / refinement；`paper1_strategy_asset_map.md`
   是 07-07 转向的施工地图，其下游 PR 聚合视图里含 `PR-repair-runner`、`PR-raw-export`、
   `PR-eval-rubric`（closure/regression rubric）等 repair 行。两份的**框架前提**都已被
   「paper1 只做 issue discover」覆盖，留在 `evidence/ledgers/` 会被后续 agent 当成 active 清账口径。

⛔ **注意 `issue_lifecycle/` 不在上述任何一条理由里。** 它是被整目录一起搬走的，
其内容本身并未作废——见 §3。

## 3. ⭐ 里面哪些内容仍然有价值、什么时候该取回来

### 3.1 `issue_lifecycle/`：约八成是纯 discover 材料

这批东西回答的是「什么算一条问题、什么时候能确认、什么必须排除」，
**与修复无关**，因此不随 repair 一起作废。逐项：

| 仍有价值的内容 | 精确路径 | 是什么 | 什么时候取回来 |
| :-- | :-- | :-- | :-- |
| **六个状态定义** | [experiment_design/issue_lifecycle/source_level_issue_definition.md](./experiment_design/issue_lifecycle/source_level_issue_definition.md) §2 | `candidate_only` / `confirmed` / `rejected_conversion_artifact` / `rejected_other` / `out_of_scope` / `insufficient_evidence`，每个带定义与 eligibility | 需要给「一条产出处于什么状态」建分类时；当前多报侧五类裁定与它有明显对应关系，可作为前身对照 |
| **两条 confirmation 路径** | 同上 §3 | `nl_grounded_behavioral_issue`（须 NL 证据 + source STM 证据 + typed behavior 证据三类齐全）与 `raw_internal_inconsistency`（允许无 NL 证据，但须两侧冲突元素 + 一致性检查 + rationale） | 需要定义「一条发现凭什么算成立」时。⭐ 第二条路径尤其值得取回：它正面处理了「模型自身矛盾但无法绑到具体需求句」这种情形，当前口径里没有等价条款 |
| **conversion artifact 归因边界** | 同上 §5；[experiment_design/issue_lifecycle/issue_ledger_contract.md](./experiment_design/issue_lifecycle/issue_ledger_contract.md) §3 `attribution_boundary` | 来自 raw→canonical 转换、canonical→DSL lowering、normalization / recovery / parser workaround 的问题必须排除，不得计为方法发现 | ⭐ **这是与当前「表示债务」最直接相通的一条**。当前口径把它做成了多报侧的一个可扣除类别；这里的版本是把它做成**准入门**（进入台账之前就排除）。两种处置各有代价，重新设计时应对照 |
| **folded event / expression debt 默认只能 candidate** | 同上 §4 | `Idle --> Alarm : Event("temperature > 80")` 这类写法默认不算缺陷，除非有证据证明行为语义确实错 | 当前它以另一形态存在（表示债务的子类 `D1` 析取备选融合，判定须回读作者源）。取回时注意两者结论一致但机制不同 |
| **timed / hybrid 出界口径** | 同上 §6 | timed-like 需求记为 `out_of_scope` fixture 或风险，不进主分母 | 与当前建模对象边界 $M = (S,E,V,Tr,A)$ 及 `00x8` 系列永久排除是同一条边界的早期表述，可作 provenance |
| **6 个 fixture（人类可读）** | [experiment_design/issue_lifecycle/fixtures/](./experiment_design/issue_lifecycle/fixtures/) | `expression_debt_folded_event` / `confirmed_guard_mismatch` / `raw_internal_inconsistency_confirmed` / `conversion_artifact_rejected` / `out_of_scope_timed_case` / `insufficient_evidence_candidate` | ⭐ 每个 fixture 都是一个「边界情形长什么样」的小例子。需要给新规则写 worked example，或需要一批负例来校准评审条款时，直接从这里取 |
| **ledger 字段语义** | [experiment_design/issue_lifecycle/issue_ledger_contract.md](./experiment_design/issue_lifecycle/issue_ledger_contract.md) §3 | `issue_id` / `confirmation_status` / `confirmation_evidence_path` / `nl_evidence` / `source_stm_evidence` / `behavior_evidence` / `attribution_boundary` 等字段的含义 | 设计新的证据字段时作对照；⚠️ 其中 `downstream_repair_allowed` 与 §4 的 repair eligibility gate 是 repair 侧的，不要一起取 |

🔑 **机器事实源没有跟着搬走。** 上述 fixture 的 JSON 版本、schema 与 pytest 仍在
active 路径上，未受本次归档影响：

- [../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../pipeline/evaluation/schemas/source_issue_ledger.schema.json)
- [../../pipeline/evaluation/fixtures/source_issue_ledger/](../../pipeline/evaluation/fixtures/source_issue_ledger/)
- [../../pipeline/evaluation/tests/test_source_issue_ledger_schema.py](../../pipeline/evaluation/tests/test_source_issue_ledger_schema.py)

也就是说：**文档在冷库，合同还在线上跑测试。** 取回文档内容时要同步确认 JSON 是否仍一致。

### 3.2 `source_trace/`：只有 relation 分类值得取

| 仍有价值 | 精确路径 | 说明 |
| :-- | :-- | :-- |
| 六种 trace relation 的分类 | [experiment_design/source_trace/source_trace_contract.md](./experiment_design/source_trace/source_trace_contract.md)；[experiment_design/source_trace/README.md](./experiment_design/source_trace/README.md) §3 | `exact` / `normalized` / `split` / `ambiguous` / `untraceable` / `conversion_artifact`。当前判定「一条产出是不是表示债务」时，实质上在做同一种分类；这份分类法可作为子类划分的参照 |
| 6 个 trace fixture | [experiment_design/source_trace/fixtures/](./experiment_design/source_trace/fixtures/) | 每种 relation 一个小例子，同 §3.1 的用法 |
| 「不把 `normalized` 造成的语法变化写成 gain」等四条禁止误读 | [experiment_design/source_trace/README.md](./experiment_design/source_trace/README.md) §6 | 与当前「不把 conversion gain 计为方法收益」是同一条纪律 |

⛔ **不要取的**：`projection_status`、`closure_claim_allowed`、`required_future_trace`、
post-Confirm export bundle 相关的一切——它们只在有修复动作时才有意义。

### 3.3 `experiment_design/` 顶层与 `metrics/`：只作历史

| 内容 | 现状 |
| :-- | :-- |
| [experiment_design/README.md](./experiment_design/README.md) §1 的「未来协议块」表 | 除前两项外全部作废；表格保留仅为追溯当时的设计意图 |
| [experiment_design/GUIDE.md](./experiment_design/GUIDE.md) §3「禁止直接继承的 archived 内容」 | ⭐ 这张表本身仍有方法论价值：它示范了「归档资产要复用时，必须先说明为什么不能直接继承、以及要怎么重新定义」 |
| [experiment_design/GUIDE.md](./experiment_design/GUIDE.md) §4 第 4 条「每条实验 claim 都必须明确分母」 | ⭐ 仍然成立，且当前口径里以「两套分母必须同报」的形式活着 |
| [experiment_design/metrics/README.md](./experiment_design/metrics/README.md) | 整份是 pilot 前的占位，六项全部「未冻结」；实验已完成，此文件无残余价值 |

### 3.4 `evidence_ledgers/`：只作转向的历史证据

| 内容 | 精确路径 | 仍有价值的部分 |
| :-- | :-- | :-- |
| 07-07 转向的资产清账地图（A-001 – A-024） | [evidence_ledgers/paper1_strategy_asset_map.md](./evidence_ledgers/paper1_strategy_asset_map.md) §3 | ⭐ 唯一一份把「当时仓库里有哪些资产、各自判 active / update / archive / historical、依据是什么」逐条记下来的表。追溯「某个目录当初为什么被保留 / 归档」时从这里查 |
| 四态 decision 口径的定义 | 同上 §2 | `active` / `update` / `archive` / `historical` 的含义与典型下游；本 README 的写法沿用了它的精神 |
| 「conversion / normalization / lowering 可作 active infrastructure，但不能计入 method gain」 | 同上 §2 特殊纪律 | ⭐ 这条纪律至今有效，且是当前禁用词表里 `conversion gain` 一条的来源 |
| 旧资产继承边界 | [evidence_ledgers/legacy_asset_inheritance.md](./evidence_ledgers/legacy_asset_inheritance.md) §2 | 解释 `paper_v1/`、旧 baseline、旧 sources 为什么不被继承；只作 provenance |

⛔ **两份的 thesis 表述都已作废**：`legacy_asset_inheritance.md` §3 的「第一篇是
`<NL, STM_0> -> STM_k / Better STM` repair / refinement」、`paper1_strategy_asset_map.md`
§0 的「转到 source-level behavioral issue discovery **and closure** 主线」——
当前口径是 **discover 单独成篇，closure 与 repair 另立后续论文**。

## 4. 哪些内容已被取代

| 本目录里的内容 | 被谁取代 | 精确路径 |
| :-- | :-- | :-- |
| 实验协议、判定口径、命中判据 | discover 判定口径文档（当前唯一真源） | [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/) |
| 实验结果与代次对比 | discover 矩阵 | [../../discover_matrix/](../../discover_matrix/) |
| `metrics/` 的全部占位 | 已完成的全量实验报告 | [../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) |
| `source_trace` v0 的 active 角色 | R4.5 `source_trace_base.v1`（identity-only、`closure_claim_allowed=false`） | [../../pipeline/representation/README.md](../../pipeline/representation/README.md) |
| 两份 v0 字段合同的机器形态 | 仍在线，未被取代 | [../../pipeline/evaluation/](../../pipeline/evaluation/)（见 §3.1 末） |
| `paper1_strategy_asset_map.md` 中 A-005 `story/` 行的处置 | 该目录已于同日归档 | [../r8_discover_repair_story/](../r8_discover_repair_story/) |
| Better STM 期的历史资产入口 | 上一代 cold archive | [../r5_7_better_stm_snapshot/](../r5_7_better_stm_snapshot/) |

## 5. 原路径 → 新路径映射

原路径均相对 `paper_stm_issue_discover/`；新路径均相对本 README。

| 原路径 | 新路径 |
| :-- | :-- |
| `experiment_design/README.md` | [experiment_design/README.md](./experiment_design/README.md) |
| `experiment_design/SUMMARY.md` | [experiment_design/SUMMARY.md](./experiment_design/SUMMARY.md) |
| `experiment_design/GUIDE.md` | [experiment_design/GUIDE.md](./experiment_design/GUIDE.md) |
| `experiment_design/metrics/README.md` | [experiment_design/metrics/README.md](./experiment_design/metrics/README.md) |
| `experiment_design/issue_lifecycle/README.md` | [experiment_design/issue_lifecycle/README.md](./experiment_design/issue_lifecycle/README.md) |
| `experiment_design/issue_lifecycle/GUIDE.md` | [experiment_design/issue_lifecycle/GUIDE.md](./experiment_design/issue_lifecycle/GUIDE.md) |
| `experiment_design/issue_lifecycle/source_level_issue_definition.md` | [experiment_design/issue_lifecycle/source_level_issue_definition.md](./experiment_design/issue_lifecycle/source_level_issue_definition.md) |
| `experiment_design/issue_lifecycle/issue_ledger_contract.md` | [experiment_design/issue_lifecycle/issue_ledger_contract.md](./experiment_design/issue_lifecycle/issue_ledger_contract.md) |
| `experiment_design/issue_lifecycle/fixtures/README.md` | [experiment_design/issue_lifecycle/fixtures/README.md](./experiment_design/issue_lifecycle/fixtures/README.md) |
| `experiment_design/issue_lifecycle/fixtures/<6 个子目录>/README.md` | [experiment_design/issue_lifecycle/fixtures/](./experiment_design/issue_lifecycle/fixtures/) 下同名子目录 |
| `experiment_design/source_trace/README.md` | [experiment_design/source_trace/README.md](./experiment_design/source_trace/README.md) |
| `experiment_design/source_trace/GUIDE.md` | [experiment_design/source_trace/GUIDE.md](./experiment_design/source_trace/GUIDE.md) |
| `experiment_design/source_trace/source_trace_contract.md` | [experiment_design/source_trace/source_trace_contract.md](./experiment_design/source_trace/source_trace_contract.md) |
| `experiment_design/source_trace/fixtures/README.md` | [experiment_design/source_trace/fixtures/README.md](./experiment_design/source_trace/fixtures/README.md) |
| `experiment_design/source_trace/fixtures/<6 个子目录>/README.md` | [experiment_design/source_trace/fixtures/](./experiment_design/source_trace/fixtures/) 下同名子目录 |
| `evidence/ledgers/legacy_asset_inheritance.md` | [evidence_ledgers/legacy_asset_inheritance.md](./evidence_ledgers/legacy_asset_inheritance.md) |
| `evidence/ledgers/paper1_strategy_asset_map.md` | [evidence_ledgers/paper1_strategy_asset_map.md](./evidence_ledgers/paper1_strategy_asset_map.md) |

`issue_lifecycle/fixtures/` 的六个子目录：`expression_debt_folded_event`、
`confirmed_guard_mismatch`、`raw_internal_inconsistency_confirmed`、
`conversion_artifact_rejected`、`out_of_scope_timed_case`、`insufficient_evidence_candidate`。
`source_trace/fixtures/` 的六个子目录：`exact_transition_trace`、`normalized_guard_trace`、
`split_transition_trace`、`ambiguous_trace`、`untraceable_element`、`conversion_artifact_trace`。

## 6. 禁止外推

1. 不得把本目录的任何协议块恢复为 active 实验设计——真源是 [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/)。
2. 不得把 `downstream_repair_allowed`、`closure_claim_allowed`、post-Confirm export、
   closure / regression audit 迁回当前论文——它们属后续 repair 论文。
3. 不得把 synthetic fixture 的通过写成 method effectiveness——它们是合同校准，不是实验结果。
4. 不得用 [evidence_ledgers/paper1_strategy_asset_map.md](./evidence_ledgers/paper1_strategy_asset_map.md) 的下游 PR 表当作当前施工路线——
   动态施工状态以 GitHub PR / issue 为准。
5. 若要复用 §3 中任何一条，必须按 [experiment_design/GUIDE.md](./experiment_design/GUIDE.md) §3 的方式**重新定义**并显式引用本 archive 为历史来源，
   不得直接搬运字段名与判据。

## 7. 归档时对内容做了什么 / 没做什么

**做了**：把 27 份文件里的相对链接按新的目录深度机械重算，使它们仍能点开。
其中三类目标发生了路径变化：指向工作区根与 `pipeline/` 的链接加深一层；
指向 `../archive/r5_7_better_stm_snapshot/` 的链接改为同级 `../r5_7_better_stm_snapshot/`；
指向 `story/` 与 `evidence/ledgers/` 的链接改指两处新归档。

**没做**：不改结论、不改字段语义、不改更新日志。文中「当前 / active / 尚未实现」等
时态表述停留在 2026-07 的语境，属正常历史留痕；判断当前状态一律回 §4 的替代入口。
