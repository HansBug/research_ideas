# Paper Story

## Thesis

We study feedback-driven source-level behavioral issue discovery and closure for existing state-machine artifacts: given natural-language requirements and a raw/source state machine, the workflow uses an intermediate executable semantic representation to expose candidate issues, confirm source-level behavioral issues, repair confirmed issues, and project the repair evidence back to the source level for closure and regression audit.

中文概括：本文不是证明某种状态机表达语言更好，而是研究如何用可执行语义中间表示和工具反馈，帮助已有 raw/source 状态机发现、确认、修复并闭合行为问题。

## Task Boundary

- Inputs: `NL` and existing raw/source `STM_0`.
- Intermediate artifacts: source trace, intermediate executable semantic representation, diagnostics / inspect / simulation / verification feedback, candidate issue ledger.
- Outputs: confirmed issue ledger, issue-grounded repair/change ledger, raw/source patch bundle or final raw/source `STM_k`, closure/regression ledger.
- Supported settings: discrete control-oriented FSM / HSM / statechart-like models with states, transitions, events, guard-like conditions, variables, actions/effects, and hierarchy when traceable.
- Out-of-scope settings: one-shot `NL -> STM` generation as the main contribution, modeling-language superiority claims, arbitrary UML/SysML coverage, timed/hybrid automata headline claims, and constructed `STM_k` adjudication as method evidence.

## Gap

Existing LLM-based modeling pipelines can produce state-machine-like artifacts, but practical use requires more than producing a diagram-like model. Many artifacts contain source-level behavioral issues: missing conditions, event/guard/action confusion, inconsistent transitions, unsupported abstractions, or behavior that cannot be checked against the natural-language requirement. Purely descriptive representations and raw LLM refinement often provide weak feedback for these issues.

The gap is therefore not “which state-machine representation is better”. The gap is how to build a feedback-driven workflow that can discover and close behavior-level issues in existing artifacts while keeping the final explanation at the raw/source level.

## Technical Challenge

1. **Candidate vs confirmed issue**: tool diagnostics, folded events, or expression debt may indicate a risk, but they are not automatically source-level model issues.
2. **Intermediate vs source attribution**: conversion, normalization, and lowering may make a model executable, but their benefits must not be counted as repair gain.
3. **Repair without over-repair**: an issue-grounded repair should close confirmed issues without rewriting the whole model or introducing regression.
4. **Evaluation timing**: closure, over-repair, regression, and baseline fairness depend on the real raw/source output shape; final rubric and baseline contract must wait until pilot outputs exist.

## Method Insight

Separate semantic reasoning from deterministic feedback and source-level accountability. The intermediate representation is used because diagnostics, simulation/probe, and verification/check feedback need executable semantics. However, the contribution is not the representation itself; the contribution is the issue lifecycle around existing source artifacts: discover, confirm, repair, project back, and audit closure/regression.

## System / Method Stages

1. **Source ingestion and trace**: record raw/source elements and their relation to intermediate elements.
2. **Initial discovery**: use diagnostics, inspect output, simulation/probe, verification/check hints, and LLM reasoning to propose candidate issues.
3. **Strict confirmation**: validate candidate issues against `NL`, raw/source elements, and behavioral evidence.
4. **Issue-grounded repair**: generate repair plans and candidate changes tied to `issue_id`.
5. **Raw/source export**: produce a raw/source patch bundle, raw-level diff/explanation, or final raw/source `STM_k`.
6. **Closure and regression audit**: rediscover/reconfirm after repair and classify issues as closed, partially closed, not closed, over-repaired, regression-introduced, or unjudgeable.

## Contributions

Current contribution wording must remain evidence-aware:

1. **Task framing**: define a source-level issue discovery and closure task for existing state-machine artifacts, rather than one-shot generation or representation comparison.
2. **Workflow architecture**: design a staged feedback loop that separates candidate issue discovery, strict confirmation, issue-grounded repair, source-level projection, and closure/regression audit.
3. **Attribution discipline**: enforce a boundary between conversion / representation infrastructure and repair-loop gains.
4. **Evidence infrastructure**: maintain ledgers and traces that make issues, repairs, unsupported projections, partial closures, and regressions auditable.
5. **Experimental roadmap**: defer final rubric and baseline contract until pilot produces real raw/source `STM_k` or patch bundle examples.

## Evidence

| Claim area | Current evidence | Claim strength |
|---|---|---|
| Strategic framing | [2026-07-07 mentor record](../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) and [asset map](../evidence/ledgers/paper1_strategy_asset_map.md). | task framing supported |
| Existing infrastructure | [pipeline/](../pipeline/) conversion / representation / readiness assets. | infrastructure support |
| Better STM deactivation | [asset map](../evidence/ledgers/paper1_strategy_asset_map.md) and [scan audit](../evidence/audits/2026-07-07-post-strategy-asset-scan.md). | boundary supported |
| Method effectiveness | No real repair-loop pilot yet. | future empirical claim only |
| Evaluation / baseline | To be frozen after pilot. | planning only |

## Related Work Positioning

The intended positioning is an executable feedback workflow for existing state-machine artifacts. Related work should be compared along three axes:

1. LLM-based state-machine or behavioral-model generation: produces candidate artifacts but often lacks source-level issue closure.
2. Modeling / DSL / formal-method tools: provide executable or checkable semantics but are not themselves the contribution of this paper.
3. LLM-assisted repair / verification / test/spec generation: relevant to feedback sources, but baseline fairness must be defined after pilot output shapes are known.

Do not position the paper as a PlantUML-vs-fcstm or SysML-vs-fcstm language paper.

## Claims to Make

- We study source-level behavioral issue discovery and closure for existing state-machine artifacts.
- We use an intermediate executable semantic representation to enable diagnostics, simulation/probe, and verification/check feedback.
- We separate candidate issue discovery from strict source-level confirmation.
- We require repairs to be issue-grounded and auditable through source-level patch / projection evidence.
- We defer final rubric and baseline contract until pilot outputs reveal the actual raw/source output shape.

## Claims to Be Careful About

- “Repair” should mean issue-grounded refinement with closure evidence, not generic model rewriting.
- “Verification” should be framed as one feedback source whose usefulness depends on property/probe quality.
- “fcstm” should be framed as the current intermediate representation, not the scientific contribution.
- “Improvement” should be stated only when closure/regression evidence exists.

## Claims to Avoid

- Better STM is the active headline evaluation framework.
- The paper proves `fcstm` / `pyfcstm` is a better modeling language.
- Conversion, lowering, parse ok, inspect ok, or executable representation success is repair gain.
- Constructed `STM_k` dry-run or blind adjudication demonstrates method effectiveness.
- A folded event or ugly expression is automatically a confirmed source-level issue.
- Baseline, metrics, or judge prompt are already final before pilot.

## Reviewer Risks

| Risk | Why it matters | Mitigation in this story |
|---|---|---|
| Reviewer thinks this is a modeling-language paper. | Would shift burden to proving fcstm superiority. | State fcstm as intermediate medium only and evaluate at raw/source issue level. |
| Reviewer challenges “better STM”. | “Better” is underspecified and may mix expression quality with semantic correctness. | Archive Better STM headline; use issue discovery / closure instead. |
| Reviewer asks how issues are confirmed. | Candidate diagnostics alone are weak. | Require `NL + raw/source element + behavior evidence`. |
| Reviewer asks if repair overfits the model. | Scenario/property generation may overfit source model. | Defer final rubric/baseline until pilot; include regression and unjudgeable states. |
| Reviewer asks for fair baselines. | Baseline input visibility depends on final output form. | Freeze baseline contract only after pilot. |
