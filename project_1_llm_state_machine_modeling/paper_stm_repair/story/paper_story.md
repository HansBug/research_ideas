# Paper Story

## Thesis

We study feedback-driven source-level behavioral issue discovery and closure for existing state-machine artifacts: given natural-language requirements and a raw/source state machine, the workflow uses an intermediate executable semantic representation to discover issue roots and immutable checks once, iteratively repair and confirm issue dispositions until every chain is closed, and project the final repair evidence back to the source level for closure and regression audit.

中文概括：本文不是证明某种状态机表达语言更好，而是研究如何用可执行语义中间表示和工具反馈，对已有 raw/source 状态机执行一次问题发现、多轮修复-确认，并在源层闭合行为问题。

## Task Boundary

- Inputs: `NL` and existing raw/source `STM_0`.
- Intermediate artifacts: source trace, intermediate executable semantic representation, diagnostics / inspect / simulation / verification feedback, Discover roots/checks, Repair dispositions, Confirm decisions/successors, and immutable run records.
- Outputs: final fcstm `STM_k`, issue-grounded repair/change chains, raw/source patch bundle or final raw/source `STM_k`, and closure/regression ledger.
- Supported settings: discrete control-oriented FSM / HSM / statechart-like models with states, transitions, events, guard-like conditions, variables, actions/effects, and hierarchy when traceable.
- Out-of-scope settings: one-shot `NL -> STM` generation as the main contribution, modeling-language superiority claims, arbitrary UML/SysML coverage, timed/hybrid automata headline claims, and constructed `STM_k` adjudication as method evidence.

## Gap

Existing LLM-based modeling pipelines can produce state-machine-like artifacts, but practical use requires more than producing a diagram-like model. Many artifacts contain source-level behavioral issues: missing conditions, event/guard/action confusion, inconsistent transitions, unsupported abstractions, or behavior that cannot be checked against the natural-language requirement. Purely descriptive representations and raw LLM refinement often provide weak feedback for these issues.

The gap is therefore not “which state-machine representation is better”. The gap is how to build a feedback-driven workflow that can discover and close behavior-level issues in existing artifacts while keeping the final explanation at the raw/source level.

## Technical Challenge

1. **Candidate vs repair-eligible root**: tool diagnostics, folded events, or expression debt may indicate a risk, but they are not automatically source-level model issues or valid fix targets; Discover must make this assessment before publishing roots.
2. **Intermediate vs source attribution**: conversion, normalization, and lowering may make a model executable, but their benefits must not be counted as repair gain.
3. **Repair and confirmation without over-repair**: Repair must process the complete pending batch, while Confirm must accept or reject every disposition against immutable checks without rediscovery, model rollback, or silent regression.
4. **Evaluation timing**: closure, over-repair, regression, and baseline fairness depend on the real raw/source output shape; final rubric and baseline contract must wait until pilot outputs exist.

## Method Insight

Separate semantic reasoning from source-level accountability. The intermediate representation is used because diagnostics, simulation/probe, and formal-verification/check feedback need executable semantics. However, the contribution is not the representation itself; the contribution is the feedback-driven refinement loop that injects these executable feedback signals into LLM-based issue discovery and repair, then projects repair evidence back to the raw/source artifact.

## System / Method Stages

1. **A: source ingestion and trace**: record raw/source elements, produce fcstm `STM_0`, and freeze issue-neutral trace/provenance.
2. **B-discover once**: derive issue checks, use executable feedback and LLM reasoning to publish the complete initial root batch with `confirmed/candidate_only` assessments, or publish zero-root.
3. **B-repair**: process every pending node in one batch with a reasoned `fix` or `reject`, then atomically publish the complete fcstm `STM_{i+1}` and model diff.
4. **B-confirm**: inspect every disposition on the published model, issue a reasoned `accept` or `reject`, and append successor nodes for rejected dispositions; successors return only to Repair until all chains close.
5. **B-final**: deterministically validate record integrity, evidence coverage, and accepted-fix support; this gate only establishes eligibility to attempt source projection.
6. **C: raw/source export and closure/regression audit**: project once to a raw/source patch bundle or final raw/source `STM_k`, then classify source-level closure, partial closure, non-closure, over-repair, regression, or unjudgeable outcomes.

## Contributions

Current contribution wording must follow the 2026-07-07 mentor guidance: paper1 contributes the loop plus simulation / formal-verification-enabled feedback, not a new state-machine language and not an audit ledger by itself.

1. **Feedback-driven LLM refinement loop for existing STM artifacts**: formulate and implement a loop over `NL + raw/source STM_0` with one Discover stage, iterative Repair-Confirm rounds over issue-linked dispositions, and final source-level closure/regression assessment.
2. **Executable-feedback integration into the loop**: use an intermediate executable semantic representation to bring diagnostics / inspect output, simulation/probe results, and formal-verification/check feedback into the LLM refinement process, so that the loop is not only free-form textual rewriting.
3. **Source-level repair output and evaluation setup**: require repair evidence to be projected back to raw/source-level patches, diffs, or final raw/source `STM_k`, and set up the eventual evaluation around issue discovery, issue closure, partial closure, non-closure, regression / over-repair, and direct raw/source LLM baselines.

The following are important method and evaluation disciplines, but they must not be written as main contribution bullets: candidate/confirmed issue ledgers, attribution boundary, traceability records, closure/regression audit tables, run-record evidence, and the post-pilot timing of final metric / baseline / judge-prompt freeze.

## Evidence

| Claim area | Current evidence | Claim strength |
|---|---|---|
| Strategic framing | [2026-07-07 mentor record](../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) and [asset map](../evidence/ledgers/paper1_strategy_asset_map.md). | task framing supported |
| Existing infrastructure | [pipeline/](../pipeline/) conversion / representation / readiness assets. | infrastructure supported |
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
- We separate Discover-time root assessment, post-repair disposition confirmation, and final source-level closure assessment.
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
| Reviewer asks how issues become repair-eligible and how repairs are confirmed. | Candidate diagnostics alone are weak, while a runnable patch may still be wrong. | Discover requires `NL/source/behavior` or source-internal evidence for repair eligibility; B-confirm then evaluates every disposition on the published model using immutable checks and explicit reasons. |
| Reviewer asks if repair overfits the model. | Scenario/property generation may overfit source model. | Defer final rubric/baseline until pilot; include regression and unjudgeable states. |
| Reviewer asks for fair baselines. | Baseline input visibility depends on final output form. | Freeze baseline contract only after pilot. |
