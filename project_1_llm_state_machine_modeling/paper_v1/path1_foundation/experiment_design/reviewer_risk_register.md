# Path-1 Reviewer Risk Register

## 1. C/I/M 口径

- **C / Critical**：若不处理，会直接破坏论文可信度、实验公平性、oracle 可靠性、主 claim 或 baseline-aware novelty。
- **I / Important**：会显著削弱论文说服力，但可通过限定 claim、补实验、补说明或调整写作位置解决。
- **M / Minor**：影响阅读体验、工程整洁度或局部措辞，不阻塞学术推进。

## 2. S0a 风险总表

| ID | 等级 | 风险 | 典型触发条件 | Gate / 修复策略 | 后续 owner | 当前状态 |
|---|---|---|---|---|---|---|
| R1 | C | Novelty 被 direct baseline 打穿 | Abstract / Intro 暗示首次 NL-to-STM、首次反馈闭环、已有工作只画图 | [`../story/claim_evidence_map.md`](../story/claim_evidence_map.md) 必须逐条列出 baseline coverage、marginal claim、forbidden softened claims；四个 mandatory closest works 必须进入 related work 第一层 | S0a/S1b/S5 | S0a gate，待执行 |
| R2 | C | Baseline fairness 过强 | 声称 same benchmark / same protocol 打赢 prior work，但实际用了 adapted input、private oracle 或不可比输出 | external baseline 分为 same-sample approximate / near / evidence-only；至少 1 个 same-sample approximate 有计划；不强行横向排名 | S1b/S3/S5 | 待执行 |
| R3 | C | Oracle weak | LLM judge 或单作者主观判断成为主结果，或旧 eval protocol 的“不主动声明 LLM 辅助”回潮 | `oracle_protocol.md` 要求 `>=2` human annotator、blind coding、agreement、仲裁；LLM 只能 triage / second-look 且透明披露 | S2/S5 | 待执行 |
| R4 | C | Reference / sample bias | 只用 PR #9 Top-15、成功样本或 reference-ready 样本，并写平均性能 claim | 优先 9/101 或预注册降级样本；stress-test 与 main sample 分开；所有排除写入 sample registry | S2/S3 | 待执行 |
| R5 | C | Formal overclaim | parse/semantic/design/simulation diagnostics 被写成 complete verification、model checking、theorem proving 或 certification | 全文使用 deterministic diagnostics、formal-executable feedback、scenario-level simulation；BMC/LTL/industrial certification 放 future work | S0a/S5/S6 | S0a gate，后续复查 |
| R6 | I | Run-record contribution 回潮 | 把 run record / audit trail 写成 contribution，或用记录完整性替代模型质量证据 | Run record 只作为 reproducibility、debugging、eligibility 与 audit evidence；contribution 不出现 run-record-as-method claim | S0a/S3/S5 | S0a gate |
| R7 | I | `fcstm` / `pyfcstm` naming burden | 标题、摘要、贡献或 related-work 差异把内部载体包装成新 modeling language / DSL novelty | 主文用 machine-checkable / executable state-machine representation；`fcstm` / `pyfcstm` 仅在 implementation、artifact、appendix、run metadata 中说明 | S0a/S5/S6 | S0a gate |
| R8 | C | Soft novelty 回潮 | 不写“first”但写“unique”“unlike prior work”“prior work lacks feedback”“only diagrams”等柔化版本 | grep + 人工 review 双 gate；claim map 的 `forbidden_softened_claims` 每条至少 2 个反例；safe wording 必须有 baseline carve-out | S0a/S5/S6 | 待执行 |
| R9 | I | E1/E2 framing 混乱 | 把自建 agent-loop、Codex/Claude skill route 或 LangGraph 写成独立贡献 | E1/E2 只作为 orchestration condition / RQ5 / appendix analysis；主贡献仍是 diagnostics、simulation、repair decision、baseline-aware evaluation | S0a/S3/S5 | S0a gate |
| R10 | I | External baseline 不足 | 主实验只有 B0-B5 internal ablation，缺 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs carve-out | mandatory closest works 必须全部进入矩阵；优先尝试 Structure/Event SMF 或 LLMs for EMP STM 子集 same-sample approximate | S1b/S3 | 待执行 |
| R11 | I | TTool-AI / Designing FSMs 差异未讲清 | reviewer 认为本文只是重复 tool feedback 或 trace/oracle repair | 对比边际限定为控制系统需求、scenario candidate + deterministic simulator execution、structured repair decision 与 human component protocol 的组合 | S1b/S5 | 待执行 |
| R12 | I | PR #9 historical reference draft 误用 | 把 CARA/CubeSat early ref、expanded NL 或 historical note 当最终 signed oracle | 明确 historical asset；正式复核签字前不得进入主结果 | S2/S3 | foundation 已标注，待执行 |
| R13 | I | Run record 不完整 | 缺 prompt/raw output/provider/usage/stage trace/diagnostics/scenario trace/eligibility | 真实 run 使用仓库 run-record 规范；provider error、schema-invalid、weak-oracle run 不进主统计 | S3/S4 | method 已具备，主实验待执行 |
| R14 | C | 目标投 B 但证据未达 A 类标准 | 因目标是 CCF-B 期刊而降低 novelty、baseline、oracle、artifact 或 threats 标准 | 按 [../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) 做 CCF-A 标准自查；G5 前 C/I 不闭合则不硬投 | S0b/S5/S6 | 待执行 |
| R15 | M | 术语过载 | fcstm、pyfcstm、LangGraph、Codex、SC/SD/SL 等工程名在主文堆叠 | 主文只保留概念术语；工程名移到 implementation / artifact table | S5/S6 | 待写作执行 |
| R16 | M | paper_v1 旧 sprint 口径残留 | 新 session 误读 2026-05 sprint、旧 G0/S0 或 venue-first 路线为当前事实 | execution plan 拆分 S0a/S0b；入口 README 与后续 plan 同步 | S0a/S0b | 本 PR 局部处理 |

## 3. Soft novelty anti-regression examples

下列表述即使没有显式 “first” 也应拦截，并在 claim map 中替换为带 carve-out 的安全表述。

| 风险类型 | 易回潮表述 | 安全写法 |
|---|---|---|
| NL-to-STM novelty | “existing work does not generate state-machine models from requirements” | 承认已有 NL / requirements 到 UML / SysML / FSM-family 工作；本文只讨论可执行、可诊断、可仿真的目标表示如何支撑反馈闭环 |
| Feedback novelty | “prior approaches lack tool feedback” | 承认 EMP / TTool-AI 等已有 tool feedback；本文限定为 deterministic diagnostics、scenario-level simulation feedback 与 structured repair decision 的组合 |
| Trace / repair novelty | “prior repair work lacks execution evidence” | 承认 Designing FSMs 等 trace/oracle repair；本文强调 scenario candidates + deterministic simulator execution + controlled repair log 的实验口径 |
| Formal novelty | “the method verifies generated models” | 写成 parses/checks/simulates generated models under deterministic diagnostics；不宣称 complete verification |
| Artifact novelty | “run records are a main contribution” | 写成 run records support reproducibility, debugging, and eligibility auditing |
| Naming novelty | “we introduce a new state-machine DSL” | 写成 outputs are constrained to a machine-checkable and executable state-machine representation; implementation details appear in artifact/appendix |

## 4. Reviewer mental model

希望 reviewer 形成的理解：

> This paper is not primarily a new DSL paper or a Codex workflow report. It studies whether and how deterministic diagnostics, scenario-level simulation feedback, and structured repair decisions affect LLM-generated state-machine models from control-system requirements under a baseline-aware evaluation protocol. Run records support reproducibility and debugging rather than serving as a contribution; the main claims require human adjudication, ablations, careful baseline positioning, and a venue-ready artifact prepared to CCF-A review standards even if the first submission target is fit-first.

需要避免 reviewer 形成的误解：

1. “作者只是写了一个私有 DSL 和 prompt。”
2. “实验只挑了最适合自己工具的成功例子。”
3. “LLM judge 自评自证。”
4. “formal verification claim 被夸大。”
5. “没有和近期 LLM-for-modeling 工作公平比较。”
6. “作者没有正面处理 Structure/Event SMF、LLMs for EMP、TTool-AI 和 Designing FSMs 这些最接近工作。”
7. “run record / agent framework 才是论文贡献。”

## 5. Ready gate for S0a experiment-design draft

本 PR 只负责计划 / 文档 gate，不负责主实验。Ready 的学术 gate：

- C 级风险均已显式承认，并转化为后续执行 gate / owner。
- RQ 不围绕 first STM generation，而围绕 diagnostics、scenario-level simulation feedback、structured repair decision 与 baseline-aware evaluation。
- E1/E2 被降级为 orchestration condition / RQ dimension，不作为独立 contribution。
- 不存在把 historical assets、pilot 计划或 run-record capability 误写成当前实验结果的表述。
- 不运行四例真实 agent-loop：因为样本、oracle、runtime chain 与 eligibility 尚未冻结，当前只验收文档合同是否能阻断旧 story 回潮。
