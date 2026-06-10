# Path-1 Experiment Inventory and Protocol Plan

## 1. Research questions

| RQ | 问题 | 主要证据 | 当前状态 |
|---|---|---|---|
| RQ1 | Formal-feedback-guided LLM loop 是否比 direct / structured prompting 生成更有效的状态机？ | validity、component-level quality、human adjudication | 待正式实验 |
| RQ2 | parse / semantic / design / simulation feedback 各自贡献是什么？ | B2/B3/B4/B5 ablation、repair rounds、failure reduction | 待正式实验 |
| RQ3 | 相比 9 个五绿 direct baseline，本方法的边际贡献在哪里？ | 9 篇逐篇吸收报告、external baseline matrix、same-sample / approximate / evidence-only comparison | S1a 必须完成 blocking absorption 后冻结 |
| RQ4 | 方法失败在哪里，失败是否可解释和可修复？ | failure taxonomy、repair logs、scenario history、FixLog | method run record 已具备，主实验待做 |
| RQ5 | 自建 agent-loop 与成熟 coding-agent skill route 在质量、稳定性、成本和失败模式上有何差异？ | E1/E2 representative runs、run record completeness、human review | 作为 implementation analysis / appendix，不能喧宾夺主；run record 完整性只作复核支撑 |

## 2. Benchmark / dataset plan

### 2.1 样本层级

| 层级 | 目标规模 | 来源 | 用途 | 当前状态 |
|---|---:|---|---|---|
| Pilot sample | `>=3` 个系统 / `>=30` 条需求 | Path-1 9 系统 / 101 需求或 sources/ stress-test 子集 | G1 可行性、pipeline smoke | 待冻结 |
| Main sample 首选 | 9 系统 / 101 需求 | BSN、CARA、Elevator、Microwave、PBA、Radar、Stopwatch、TCS、VHL | 主实验 | 待确认 reference / oracle 成本 |
| Main sample 降级 | `>=6` 个系统 / `>=60` 条需求 | 预注册分层抽样 | 若全量成本不可控 | 必须记录排除原因 |
| Stress-test extension | Top-15 / Backup-15 或其子集 | PR #9 selection assets | 诊断 guard/action/hierarchy/fault-recovery 弱项 | 已有历史资产，需复核 |
| Diagnostic failures | 所有失败样本 | 正式 runs 自动产生 | failure taxonomy / limitations | 待正式实验 |

### 2.2 样本选择原则

1. 主结果默认优先 Path-1 9/101 或预注册降级样本，而不是只用 PR #9 Top-15。
2. PR #9 Top-15 / Backup-15 更适合当 stress-test 或 ref-model construction pool。
3. 所有排除必须写明原因：parallel/history unsupported、too-thin NL、reference unavailable、provider failure、oracle insufficient 等。
4. 如果使用 expanded NL，必须冻结原始 NL、扩充 NL、source evidence 和人工复核状态。

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
4. 每个样本保留 source path、input hash、reference/oracle 状态和 eligibility。

## 4. Baseline / condition matrix

| ID | condition | 目的 | 最低可接受实现 | 是否主结果 |
|---|---|---|---|---|
| B0 | Direct prompting | LLM 直接生成下限 | 同模型、同输入、同输出表示、无结构化反馈 | 是 |
| B1 | Structured prompting | 分解 / schema prompt 的收益 | 固定 prompt template，输出同一 formal representation | 是 |
| B2 | No-feedback agent | 分离 agent orchestration 与 deterministic feedback | 多轮/agent loop，但不接 parse/semantic/simulation feedback | 是 |
| B3 | Parse + metamodel feedback | 测 syntax / metamodel feedback 边际贡献 | 只反馈 parser、schema、basic semantic | 是 |
| B4 | Parse + semantic + simulation feedback | 测 simulation feedback 边际贡献 | 加 scenario / trace / execution feedback，但不额外人工修复 | 是 |
| B5 | Full method | 主方法 | 完整 generate-check-simulate-repair-review loop | 是 |
| E2 | Mature coding-agent skill route | 上限/实现形态分析 | skill + stage tools + full run record / report | 可选，建议 appendix / RQ5 |
| EXT | Closest prior work approximate baseline | 回答外部可比性 | 先完成 9 个 direct baseline 阻塞吸收；`Structure/Event SMF`、`llms_emp`、`TTool-AI`、`Designing FSMs` 四个 mandatory closest works 必须全部进入矩阵；至少 1 个 same-sample approximate，争取 2 个，优先从 `Structure/Event SMF` 或 `llms_emp` STM 子集落地 | 是，若能复现 |

## 5. Metrics and adjudication

### 5.1 Deterministic validity

| metric | 含义 | 来源 |
|---|---|---|
| parse validity | DSL 是否可解析 | method deterministic parser / pyfcstm |
| semantic validity | 模型能否构建语义对象 | pyfcstm semantic / method stage API |
| inspect validity | design diagnostics 是否无阻塞问题 | inspect / SD checks |
| simulation pass rate | scenario 是否可执行并达到期望 | simulator trace / scenario result |
| eligibility | run 是否能进入主统计 | run record eligibility policy |

### 5.2 Component-level quality

按 [../../../eval/PROTOCOL.md](../../../eval/PROTOCOL.md) 的 5 类组件执行：

1. states
2. transitions
3. guards
4. actions
5. hierarchical states

核心公式：$P = TP / (TP + FP)$，$R = TP / (TP + FN)$，$F1 = 2PR / (P + R)$。

注意：forced transition 按 DSL declaration-level 计数，不按 runtime descendant expansion 膨胀分母。

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

## 6. Run record requirements

每条真实 run 必须记录：

- input NL、source path、sample id、sample registry hash。
- code commit、dependency / pyfcstm submodule version。
- provider、model ID、run date、endpoint 脱敏标识。
- prompt hash、raw output 或脱敏 raw output、usage、retry、timeout、provider error。
- stage trace、scenario trace、fix request、repair decision、diff、SL-10 review、final artifact。
- eligibility verdict：eligible / provider_error / schema_invalid / non_converged / weak_oracle 等。

## 7. Current caveats

| caveat | 影响 | 缓解 |
|---|---|---|
| PR #9 selection 是 stress-test，不是随机代表性样本 | 平均性能 claim 易被 challenge | 区分 main sample 与 stress-test extension |
| reference model 成本高 | 影响主样本规模 | 先 pilot，冻结降级标准 |
| external baseline 可复现性不一 | 影响公平对比 | 先做 9 个 direct baseline 阻塞吸收；分类为 strict executable / approximate / near / evidence-only |
| E2 skill route 容易被认为只是 Codex/Claude 强 | 影响贡献归因 | 做 no/partial/full skill ablation 或作为 appendix RQ |
| Formal feedback 容易被误解为 complete verification | 影响相关工作和 reviewer 信任 | 全文统一写 formal feedback / executable simulation，不写 complete model checking |
| 目标是投 CCF-B 但按 CCF-A 标准准备 | 若门禁不硬，容易写成“降低标准投 B” | 按 [../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) 执行 novelty / baseline / oracle / artifact / threats / writing 完整性门禁；G5 前未闭合 C/I 则不硬投 |
