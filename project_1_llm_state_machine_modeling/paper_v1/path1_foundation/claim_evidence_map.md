# Path-1 Claim-Evidence Map

## 1. 使用方式

本文件控制后续 Abstract / Introduction / Contribution 中所有强 claim。任何新 claim 在进入 manuscript 前必须落到下表之一：

- **Strong**：已有或计划中能够直接支撑的证据，适合摘要/引言。
- **Careful**：证据部分存在、依赖条件较多，必须限定语气。
- **Planned**：研究计划需要完成后才能使用。
- **Forbidden**：当前证据不支持，禁止写入论文主线。

## 2. Strong / careful / planned claims

| Claim | 强度 | 当前证据 | 仍需补强 | 允许写法 |
|---|---|---|---|---|
| 本研究面向 NL 控制系统需求到状态机模型生成任务。 | Strong | project_1 研究定位、sources / Path-1 / Path-2 资料、导师讨论文档 | 正式 manuscript 中定义输入输出和范围 | “we study NL-to-state-machine modeling for control-system requirements” |
| 方法使用可解析、可执行的形式化状态机表示承载 LLM 输出。 | Strong | [../../method/README.md](../../method/README.md)、pyfcstm / method stage API、run evidence | paper 中弱化 `fcstm` 名称，说明表示能力而非 DSL novelty | “a formalized/executable state-machine representation” |
| 方法将 deterministic checks 与 simulation feedback 放入 LLM 建模闭环。 | Strong | [../../method/README.md](../../method/README.md)、[../../method/STATUS.md](../../method/STATUS.md)、LG-M1 run records | 主实验 ablation 支撑边际贡献 | “combines formal checking and executable simulation feedback” |
| run record / FixLog 提供可审计证据链。 | Strong | method run-record contract、LG-M1 final evidence、仓库 run record 规范 | artifact package 中给最小复现命令 | “records stage traces, repairs, and eligibility for auditability” |
| PR #9 提供了可复用的 Path-1 sample selection assets。 | Strong | [sample_assets.md](./sample_assets.md)、PR #9 分支资产 | 正式 sample registry 重核 | “historical candidate pool and stress-test assets” |
| 当前已有最终论文实验结果。 | Forbidden | 无；PR #9 `PATH1_REPORT.md` 仍有 TODO | 需要主实验完成 | 禁止写 |
| 我们在同一 benchmark 上超过所有 prior work。 | Forbidden | 当前没有 strict same benchmark | 需要可复现 baseline 和同协议实验 | 禁止写 |
| Formal feedback 等于完整形式化验证 / model checking。 | Forbidden | 当前主要是 parse / semantic / inspect / simulation | 若未来接入 BMC/LTL 需另写 | 禁止写 |
| LLM-as-Judge 是主 oracle。 | Forbidden | issue #67 和导师讨论都要求 human adjudication 为主 | LLM judge 只可辅助 | 禁止写 |
| E1/E2 构成 Hybrid 方法贡献。 | Forbidden | 导师讨论已明确不主打 Hybrid | E1/E2 作为 agent orchestration conditions | 禁止写 |

## 3. Contribution-to-evidence map

| Contribution | Evidence already available | Evidence required before manuscript result claim | Risk if missing |
|---|---|---|---|
| Formalized executable state-machine representation | method / pyfcstm / parser / simulator / examples | representation definition、syntax subset、component extraction、limitations | 被质疑只是私有 DSL |
| Feedback-guided modeling loop | LangGraph runtime、stage API、run record、four-case retained evidence | ablation B2-B5、failure taxonomy、representative successful and failed runs | 被质疑只是 prompt engineering |
| Auditable repair evidence chain | FixLog / run record design、LG-M1 docs | artifact package、example trace、eligibility filter | 被质疑不可复现 |
| Controlled evaluation protocol | eval protocol、Path-1 5-component口径 | frozen samples、human annotators、agreement、baseline runners | 被质疑 oracle weak |
| External baseline comparison | baselines corpus 72 papers | same-sample / approximate / evidence-only matrix and results | 被质疑缺少相关工作或 cherry-pick |

## 4. Abstract / introduction claim guardrails

### 可以进入摘要的句式

- “We introduce an LLM-agent workflow that iteratively generates, checks, simulates, and repairs executable state-machine models.”
- “The workflow records deterministic feedback, simulation traces, and repair decisions for auditability.”
- “We evaluate the approach through a frozen control-system benchmark, component-level human adjudication, and ablations.”

### 暂时只能进入计划或 future work 的句式

- “We will compare against recent LLM-based modeling baselines once the sample registry and runner are frozen.”
- “BMC/LTL-level verification is outside the first paper and remains future work.”

### 禁止句式

- “Our method solves state-machine modeling from natural language.”
- “We outperform prior work on the same benchmark.”
- “The LLM judge proves model correctness.”
- “The DSL itself is the main contribution.”
