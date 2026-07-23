# paper_outline.md — paper1 新主线论文结构草案

本文件是写作结构草案，不是最终正文，不包含最终实验数字。

## 1. Introduction

目标：让读者理解为什么已有状态机制品需要 feedback-driven issue discovery and closure。

要点：

1. LLM 和建模工具可以产生状态机式制品，但已有制品往往存在行为层问题。
2. 问题不只是模型是否 runnable，也不是表达语言是否更强，而是 source-level behavioral issue 是否能被发现、经 Repair-Confirm 处理并最终在 source 层闭合。
3. 描述性状态机、folded event、guard/action/event 混淆等会削弱后续 simulation / verification feedback。
4. 本文提出一个围绕 existing raw/source STM artifact 的 issue lifecycle workflow。
5. 贡献需写成 feedback-driven LLM refinement loop、simulation / formal-verification-enabled executable feedback integration、source-level repair output and evaluation setup；ledger / audit / attribution boundary 只能作为方法和评价纪律，不作为主贡献。

## 2. Background and Motivation

要点：

1. 状态机制品：raw/source STM、intermediate executable semantic representation、trace。
2. 工具反馈：diagnostics / inspect、simulation/probe、verification/check hints。
3. 为什么 simulation / verification 需要更细行为语义，但本文不把中间表示本身作为贡献。
4. 为什么 Better STM / which STM is better 容易滑向 specification quality 或 modeling language 争论。
5. 为什么可信评价仍需要 trace / run record / closure evidence chain。

## 3. Problem Formulation

定义：

```text
Input:  NL + raw/source STM_0
Output: confirmed issue ledger + repair/change ledger + fresh canonical raw/source STM_k + semantic change/correspondence ledger + closure/regression ledger
```

必须区分：

- candidate issue vs confirmed source-level behavioral issue；
- conversion / representation readiness vs repair gain；
- intermediate candidate vs raw/source-level output；
- closure vs regression；
- unsupported / untraceable / unjudgeable。

## 4. Method

建议小节：

1. Source ingestion and trace
2. Intermediate executable semantic representation
3. B-discover once: root assessment and immutable checks
4. B-repair: full-batch `fix/reject` and atomic model publication
5. B-confirm: full-batch `accept/reject` and successor chains
6. Deterministic loop control and B-final evidence gate
7. One-time post-Confirm semantic-root bundle and fresh canonical raw/source `STM_k` export
8. Source-level closure and regression audit
9. Run record and eligibility discipline

写作纪律：

- 不把 fcstm 写成贡献。
- 不把 ledger / audit / evidence infrastructure 写成贡献；它们是 method discipline 与 evaluation protocol。
- 不把 conversion success 写成 repair gain。
- 不把 LLM preference 写成最终 judge。
- 不把 unavailable projection 静默计入 success。

## 5. Experiments

当前只能写 plan，不写 result。

建议实验层次：

1. Pilot feasibility：小规模跑通 issue ledger、trace、repair、post-Confirm semantic-root export、canonical raw/source `STM_k` 与 closure audit。
2. Post-pilot rubric freeze：基于真实 output shape 冻结 closure / partial / regression / unjudgeable 判据。
3. Baseline contract：三层 baseline 可在 pilot 后定义：
   - issue discovery；
   - known confirmed issue repair / closure；
   - black-box end-to-end。
4. Formal experiment：样本、reference issue ledger、eligibility、cost / retry / failure accounting。

## 6. Results

当前尚无正式结果。后续结果应围绕：

- discovered candidate issues；
- confirmed issues；
- closed / partially closed / not closed issues；
- regression-introduced count；
- unsupported / untraceable / unjudgeable cases；
- baseline comparison under frozen contract；
- cost / retry / non-convergence。

## 7. Discussion

要点：

1. 中间表示为什么有必要，但为什么不是本文贡献。
2. diagnostics / simulation / verification feedback 各自优势和局限。
3. source-level projection 的困难。
4. scenario/property generation 过拟合风险。
5. 明确 future work 边界：后续可以研究面向控制系统的建模 DSL / agentic modeling 方向，但这不是 paper1 的贡献。

## 8. Threats to Validity / Limitations

必须包括：

- scope 限制：discrete FSM / HSM / statechart-like subset。
- 不覆盖 arbitrary UML / SysML / timed / hybrid automata。
- baseline fairness 依赖 pilot 后 output shape。
- LLM judge / human adjudication 风险。
- source trace 和 raw export 可能 unsupported。
- 不把 pilot calibration 当正式主结果。

## 9. Conclusion

总结应回到：本文研究现有状态机制品上的 issue discovery and closure，不是建模语言优劣或 Better STM 偏好判断。
