# terminology policy：术语、弱化策略与 forbidden wording

## 0. 来源与当前性

| 字段 | 值 |
|---|---|
| 原始来源 | R0 `terminology_policy.md`，后在 R5 简化时折叠进 [README.md](./README.md) |
| 本轮恢复目的 | 恢复独立术语与禁用表达入口，方便后续写作 / review 直接 dry-run |
| 当前证据入口 | [paper_story.md](./paper_story.md)、[task_boundary.md](./task_boundary.md)、[claim_evidence_map.md](./claim_evidence_map.md) |

## 1. 推荐术语

| 语义 | 中文推荐写法 | 英文必要写法 |
|---|---|---|
| 论文主任务 | 反馈驱动状态机修正 | feedback-driven state-machine repair / refinement from `<NL, STM_0>` to `STM_k` |
| 状态机表示 | 语义增强、可机检、可执行状态机制品 | semantically enriched, machine-checkable and executable state-machine artifact |
| 检查反馈 | 轻量形式化 / 静态诊断、语义诊断、场景仿真反馈 | lightweight diagnostics / semantic diagnostics / scenario feedback |
| 修正循环 | 诊断-修正-回归-接受/拒绝/回滚协议 | diagnose-repair-regression loop; accept / reject / rollback protocol |
| 结果目标 | 相对更优 STM | relatively better STM; auditable improvement over the same normalized `STM_0` |
| 转换归因 | 转换规范化收益与修正循环收益分离 | converter-aware attribution; separation of normalization and repair-loop effects |
| 负证据 | 阻塞、部分转换、失败和不收敛证据 | negative evidence; blocked / partial / non-convergent cases |

## 2. `fcstm` / `pyfcstm` / DSL 弱化策略

| 位置 | 写法策略 |
|---|---|
| 标题 / 摘要 / Introduction contribution | 不出现 `fcstm` / `pyfcstm` / new DSL。 |
| Method implementation / artifact | 可作为内部实现载体说明，但必须低调。 |
| Reproducibility / artifact appendix | 可写工具名、commit、版本、运行入口。 |
| Related work positioning | 不把本文定位为 DSL 设计论文。 |
| reviewer response / limitations | 可说明该载体限制当前 scope，但不要把 limitation 写成主贡献。 |

## 3. 禁止或需降级的表达

| 高风险表达 | 安全替代 |
|---|---|
| 首个 / 最强 `NL -> STM` 方法 | 本文研究给定初始状态机后的反馈驱动修正任务。 |
| 提出新 DSL | 使用语义增强、可机检、可执行的状态机制品作为实验载体。 |
| `FCSTM-representable` / 以 `fcstm` 定义研究对象 | 本文对象是控制系统离散状态机；`fcstm` 只作为 implementation / artifact / appendix 术语。 |
| 完整形式化验证 / model checking 保证正确 | 使用轻量形式化 / 静态诊断和场景仿真反馈发现并约束缺陷。 |
| 自动修正一定提升质量 | 在预注册评价门下检验是否产生相对更优候选，并报告失败和不收敛。 |
| baseline 不需要比较 | baseline 重排为 seed source、转换压力、有限对照和 related work。 |
| run record 是方法贡献 | run record 是内部实验审计和复现证据链，不写成论文贡献。 |
| R5/R5.5 已经证明 repair 有效 | R5/R5.5 只证明 readiness / seed profile / conversion pressure；真实 repair 结果等待 R6/R8。 |

## 4. 推荐写作例句

| 场景 | 建议句 |
|---|---|
| Introduction task | We study feedback-driven repair of an initial state-machine artifact conditioned on natural-language requirements, rather than one-shot state-machine generation from text. |
| Method carrier | We normalize candidate artifacts into a semantically enriched, machine-checkable and executable state-machine representation to support diagnostics and scenario feedback. |
| Evaluation caution | Improvements are counted only against the same normalized `STM_0`; normalization and repair-loop effects are reported separately. |
| Negative evidence | We report blocked, partial, rejected and non-convergent cases as part of the evidence rather than excluding them from the protocol. |
| Scope limitation | Our current main setting focuses on discrete FSM/HSM/statechart-like artifacts; data-rich EFSM/timed behavior is treated as stress or future work unless explicitly supported by the frozen protocol. |

## 5. 自检 grep

实现或写作阶段可用以下 grep 作为人工审查入口。命中不一定错误，但必须确认是否只出现在 forbidden policy 或 limitations 中。

```bash
grep -RIn "首个\|最强\|new DSL\|完整形式化验证\|model checking\|guarantee\|NL -> STM.*主贡献\|repair.*一定\|outperform all" project_1_llm_state_machine_modeling/paper_stm_repair || true
```

## 6. 与 claim-evidence map 的关系

任何术语升级都必须同步 [claim_evidence_map.md](./claim_evidence_map.md)：

1. 若将 “study / frame” 改成 “solve / demonstrate”，必须有结果证据。
2. 若将 “lightweight diagnostics” 改成 “formal verification”，必须有 soundness 或 model-checking 证据。
3. 若将 “relatively better STM” 改成 “correct STM”，必须有 reference/adjudication 与形式化边界证明；当前不具备。
4. 若写 `fcstm`，必须确认它只出现在 implementation / artifact / appendix 语境。
