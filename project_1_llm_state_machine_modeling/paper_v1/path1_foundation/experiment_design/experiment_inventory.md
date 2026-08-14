# Path-1 Experiment Inventory and Protocol Plan

## 0. S0a 定位与边界

本文件是 PR #96 / S0a 的 experiment-design 草案，只把实验问题、条件矩阵、oracle 与 baseline fairness gate 写成可执行合同；它不运行真实 agent-loop、不生成新实验结果、不修改 method runtime，也不冻结最终样本或投稿 venue。S0a 的实验叙事必须继承 [`../baselines/SUMMARY.md`](../baselines/SUMMARY.md) §11：九大 baseline 已经覆盖泛化的 NL-to-state-machine 生成空间，因此本文不能围绕“首次生成 STM”立论，只能围绕 **deterministic diagnostics、scenario-level simulation feedback、structured repair decision 与 baseline-aware evaluation** 对控制系统状态机模型质量、可执行性和修复稳定性的边际作用来设计 RQ。

> 本 PR 不跑四例真实 agent-loop 的原因：当前阶段是 story / experiment-design / reviewer-risk 的计划文档 gate，目标是阻止旧 novelty、旧 S0 和 venue-first 路线回潮；真实运行会触碰 provider 配置、runtime、sample registry、oracle protocol 和 运行纳入 / 排除规则，属于后续 S3/S4 实验链路，不能用未冻结样本和未冻结 oracle 产出伪结果。

## 1. Research questions

| RQ | 问题 | 主要证据 | 关键对照 / 条件 | 当前状态 |
|---|---|---|---|---|
| RQ1 | **Deterministic diagnostics** 是否能减少 LLM 输出中的 parse、metamodel、semantic 与 design-level 缺陷，并改变可进入后续仿真 / 人工裁决的 有效模型比例？ | parse validity、semantic validity、inspect diagnostics、纳入 / 排除状态、diagnostic failure taxonomy | B0/B1/B2 vs B3/B4/B5 | 待正式实验 |
| RQ2 | **Scenario-level simulation feedback** 是否能发现仅靠静态诊断或 post-hoc rubric 难以暴露的行为缺陷，并改变需求相关 scenario 的执行通过率与 trace 可解释性？ | scenario pass/fail、trace evidence、scenario-to-requirement link、behavioral failure types | B3 vs B4/B5；scenario coverage audit | 待正式实验 |
| RQ3 | **Structured repair decision** 是否能把 diagnostics / simulation feedback 转化为可复盘的 accept/reject、fix request、diff 与 regression-check 决策流，以及它们如何影响修复稳定性？ | FixLog、repair decision、diff、post-repair regression、non-converged cases | B4 vs B5；repair rounds / regression outcomes | 待正式实验 |
| RQ4 | 在 **baseline-aware evaluation** 下，本文相对 direct / structured prompting、no-feedback orchestration、closest-work approximate baselines 的可防守边际是什么？ | B0-B5 / EXT matrix、same-sample approximate / near / evidence-only 分层、human adjudication | PR #94 / S1a 九大 baseline 反证；mandatory closest works carve-out | S1b 后冻结 |
| RQ5 | E1/E2 等 orchestration condition 在质量、稳定性、成本、失败模式与复现负担上有何差异？ | representative runs、cost/latency、failure mode、复现负担 | E1/E2 作为 implementation dimension / appendix analysis | 可选；不作为贡献 |

RQ 写作红线：不得把 RQ 写成“LLM 是否首次能生成状态机”“是否提出新 DSL”“agent framework 是否贡献主要效果”。E1/E2 只能帮助解释 orchestration 的实现影响，不能变成 contribution bullet。

## 2. Benchmark / dataset plan

### 2.1 样本层级

| 层级 | 目标规模 | 来源 | 用途 | 当前状态 |
|---|---:|---|---|---|
| Pilot sample | `>=3` 个系统 / `>=30` 条需求 | Path-1 9 系统 / 101 需求或 sources/ stress-test 子集 | G1 可行性、pipeline smoke、oracle 成本估计 | 待冻结 |
| Main sample 首选 | 9 系统 / 101 需求 | BSN、CARA、Elevator、Microwave、PBA、Radar、Stopwatch、TCS、VHL | 主实验与 RQ1-RQ4 | 待确认 reference / oracle 成本 |
| Main sample 降级 | `>=6` 个系统 / `>=60` 条需求 | 预注册分层抽样 | 若全量成本不可控 | 必须记录排除原因与降级规则 |
| Stress-test extension | Top-15 / Backup-15 或其子集 | PR #9 selection assets | 诊断 guard/action/hierarchy/fault-recovery 弱项 | 已有历史资产，需复核 |
| Diagnostic failures | 所有失败样本 | 正式 runs 自动产生 | failure taxonomy / limitations / repair ceiling | 待正式实验 |

### 2.2 样本选择原则

1. 主结果默认优先 Path-1 9/101 或预注册降级样本，而不是只用 PR #9 Top-15。
2. PR #9 Top-15 / Backup-15 只能作为 stress-test、reference construction candidate 或 failure probing，不代表平均性能。
3. 所有排除必须写明原因：parallel/history unsupported、too-thin NL、reference unavailable、provider failure、oracle insufficient 等。
4. 如果使用 expanded NL，必须冻结原始 NL、扩充 NL、source evidence、人工复核状态和 input hash。
5. 样本冻结前不得把 historical reference draft、early human note 或 LLM draft 当作 signed oracle。

## 3. Candidate pools reconciliation

当前仓库同时存在多个历史 / 当前样本口径。正式冻结前不得混用。

| Pool | 来源 | 数量 | 当前性 | 可否直接作为 main sample | 处理原则 |
|---|---|---:|---|---|---|
| Path-1 9 systems / 101 requirements | 仓库级数据集说明与 issue [#67](https://github.com/HansBug/research_ideas/issues/67) | 9 系统 / 101 需求 | 当前论文目标候选 | 否，需 reference / oracle 成本核验 | 优先作为 main-sample target；若降级需预注册规则 |
| `sources/` T0+🟢 historical protocol pool | [../../../eval/PROTOCOL.md](../../../eval/PROTOCOL.md) 历史协议 | 约 332 条（历史协议口径） | 历史 / 待重算 | 否 | 用于理解 2026-05 sprint 选样来源；正式冻结前重算 |
| PR #9 selection pool | PR #9 `dev/path1-hard-comparison` 分支 selection | 323 条，305 合格，18 排除 | historical sprint evidence | 否 | 只作为 stress-test candidate pool 和抽样纪律证据 |
| PR #9 Top-15 / Backup-15 | [sample_assets.md](../dataset_selection/sample_assets.md) | 15 + 15 | historical selected candidates | 否 | 可作为 stress-test extension / ref construction candidate；不能代表平均性能 |
| PR #9 30 expansions | [sample_assets.md](../dataset_selection/sample_assets.md) | 30 | historical expanded NL assets | 否 | 可作为 NL input/provenance 候选；必须人工复核，不作 oracle |

冻结样本前的强制动作：

1. 选择唯一 main-sample frame：优先 9/101；若改用 sources pool 或 Top/Backup subset，必须在 `sample_registry.csv` 中写明理由。
2. 重算或核验数量、commit、来源路径和排除规则，不能混用 323 / 332 两种历史统计。
3. 区分 main result sample、stress-test sample、diagnostic/failure sample。
4. 每个样本保留 source path、input hash、reference/oracle 状态和纳入 / 排除状态。

## 4. Baseline / condition matrix

### 4.1 Internal condition matrix

| ID | condition | 目的 | 最低可接受实现 | 是否主结果 |
|---|---|---|---|---|
| B0 | Direct prompting | LLM 直接生成同一 machine-checkable representation 的下限 | 同模型、同输入、同输出表示、无结构化反馈 | 是 |
| B1 | Structured prompting | 分解 / schema prompt 的收益 | 固定 prompt template，输出同一 representation | 是 |
| B2 | No-feedback orchestration | 分离 agent orchestration 与 deterministic feedback 的影响 | 多轮/agent loop，但不接 parse/semantic/simulation feedback | 是 |
| B3 | Diagnostics-only feedback | 测 deterministic diagnostics 的边际贡献 | 反馈 parser、schema、basic semantic、design diagnostics，不使用 scenario simulation | 是 |
| B4 | Diagnostics + scenario simulation feedback | 测 scenario-level simulation feedback 的边际贡献 | 加 scenario candidates、trace、pass/fail、behavior evidence，但不启用 structured repair decision | 是 |
| B5 | Full feedback + structured repair decision | 主方法条件 | 完整 generate-check-simulate-repair-review loop，记录 fix request、accept/reject、diff、regression | 是 |
| E1 | Self-built agent-loop orchestration | 实现路径 / orchestration condition | 使用自建 agent-loop 与同一 stage contract / 内部执行摘要格式 | 可选；仅作 RQ5 / appendix |
| E2 | Mature coding-agent skill route | 上限 / 实现形态分析 | skill + stage tools + 脱敏执行摘要 / report | 可选；仅作 RQ5 / appendix |

E1/E2 不是独立 contribution；若资源不足，主论文可以只报告 B0-B5，E1/E2 放入 appendix、threats 或 artifact note。

### 4.2 External baseline-aware comparison

| 层级 | 对象 | 作用 | 最低要求 |
|---|---|---|---|
| Same-sample approximate | 优先尝试 `Structure/Event SMF` external 8-case approximate 或 `LLMs for EMP` STM 子集 | 回答“最接近公开方法在同/近样本上如何比较” | 至少 1 个可解释映射；清楚披露输入、输出、oracle、预算差异 |
| Mandatory closest-work carve-out | `Structure/Event SMF`、`LLMs for EMP`、`TTool-AI`、`Designing FSMs` | 约束 novelty 与 contribution wording | 全部进入 related-work / risk / claim gate；不能缺席 |
| Near baseline | protocol FSM、Umple、SysML / MBSE、process model、formal specification generation | 防止遗漏邻域 | 说明为何不是 strict executable same-sample comparison |
| Evidence-only related work | code / data / prompt / GT 不可得或任务不等价的工作 | 支撑边界讨论 | 不强行横向排名；不把 private GT / missing prompt 写成 prior-work weakness |

## 5. Metrics and adjudication

### 5.1 Deterministic validity and feedback evidence

| metric | 含义 | 来源 | 支撑 RQ |
|---|---|---|---|
| parse validity | representation 是否可解析 | deterministic parser / pyfcstm-backed implementation | RQ1 |
| semantic validity | 模型能否构建语义对象 | semantic facade / method stage API | RQ1 |
| inspect validity | design diagnostics 是否无阻塞问题 | inspect / SD checks | RQ1 |
| scenario executability | scenario 是否能在 simulator 中执行 | simulator trace / scenario result | RQ2 |
| scenario pass rate | 执行结果是否满足需求相关期望 | scenario pass/fail + trace evidence | RQ2 |
| repair convergence | 修复轮是否收敛且不引入回归 | FixLog / regression check | RQ3 |
| 纳入 / 排除状态 | 某次运行是否能进入主统计 | 预注册样本与运行纳入 / 排除规则 | RQ1-RQ4 |

### 5.2 Component-level quality

按 [../../../eval/PROTOCOL.md](../../../eval/PROTOCOL.md) 的 5 类组件执行：

1. states
2. transitions
3. guards
4. actions
5. hierarchical states

核心公式：$P = TP / (TP + FP)$，$R = TP / (TP + FN)$，$F1 = 2PR / (P + R)$。

注意：forced transition 按 declaration-level 计数，不按 runtime descendant expansion 膨胀分母。

### 5.3 Human adjudication and LLM-assistance transparency

> **正式 paper protocol supersede 旧 eval 口径**：当前 [../../../eval/PROTOCOL.md](../../../eval/PROTOCOL.md) 是 2026-05 sprint 的历史基础协议，其中“LLM 初审 + 单人签字”和“不主动声明 LLM 辅助”的口径不得直接进入正式 paper。Path-1 第一篇正式实验必须在后续 `oracle_protocol.md` 中覆盖该旧口径。

正式 protocol 只能采用以下两类之一，且必须在论文与 artifact 中透明披露：

1. **human-only double-blind adjudication**：LLM 不参与主标签生成；至少两名独立人类 annotator 盲审并报告 agreement。
2. **LLM-assisted triage + human final adjudication**：LLM 只做 draft / second-look / triage；最终标签由至少两名独立人类 annotator 盲审确认；论文必须披露 LLM 的辅助角色、模型版本、prompt、agreement / disagreement 与人工仲裁方式。

| 项 | 最低要求 | 不满足时处理 |
|---|---|---|
| Annotator | 冻结样本主质量评分至少 `>=2` 名独立 human annotator | 不得作为主结果表依据 |
| Blind coding | 不暴露 method condition / model name / iteration label | threats 中降级说明，必要时降级为 diagnostic result |
| Disagreement | 记录 disagreement 与仲裁 | G5 不通过 |
| Agreement | 报告 percent agreement + Cohen $\kappa$ 或 Krippendorff $\alpha$ | 若低于阈值，降级相应 claim |
| LLM-as-Judge | 只作辅助 triage / second-look，且必须披露 | 不得作为主 oracle；不得写“不主动声明 LLM 辅助” |
| Protocol versioning | `oracle_protocol.md` 必须显式写明 supersede 的旧协议段落和生效日期 | 不得进入 G2/G3 |

## 6. 内部运行管理与正文披露边界

真实实验阶段需要另行维护内部执行材料，用于团队排障、成本核算和不可用运行的筛除；这些材料不进入 Method 章节，也不作为论文贡献。论文正文或补充材料只按 venue / artifact 要求披露必要信息：样本来源、模型与工具版本、提示词摘要或哈希、预算口径、脱敏输出摘要、诊断 / 场景结果、人工裁决协议，以及纳入 / 排除判定规则。

## 7. Current caveats and gates

| caveat | 影响 | 缓解 |
|---|---|---|
| PR #9 selection 是 stress-test，不是随机代表性样本 | 平均性能 claim 易被 challenge | 区分 main sample 与 stress-test extension |
| reference model 成本高 | 影响主样本规模 | 先 pilot，冻结降级标准 |
| external baseline 可复现性不一 | 影响公平对比 | 分类为 same-sample approximate / near / evidence-only，不强行排名 |
| E1/E2 skill route 容易被认为只是 Codex/Claude 强 | 影响贡献归因 | 降级为 orchestration condition / RQ5 / appendix，不列 contribution |
| Formal feedback 容易被误解为 complete verification | 影响相关工作和 reviewer 信任 | 全文统一写 deterministic diagnostics、formal-executable feedback、scenario-level simulation，不写 complete model checking |
| 目标是投 CCF-B 但按 CCF-A 标准准备 | 若门禁不硬，容易写成“降低标准投 B” | 按 [../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) 执行 novelty / baseline / oracle / artifact / threats / writing 完整性门禁；G5 前未闭合 C/I 则不硬投 |
| S0a 只是文档 gate | 可能被误解为已有实验结果 | 所有 RQ 与指标均标注待正式实验；本 PR 不新增 result 数字、不跑四例 agent-loop |
