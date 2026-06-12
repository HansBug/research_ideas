# terminology policy：术语、弱化策略与 forbidden wording

## 1. 推荐术语

| 语义 | 推荐写法 |
|---|---|
| 论文主任务 | feedback-driven state-machine repair / refinement from `<NL, STM_0>` to `STM_k` |
| 状态机表示 | semantically enriched state-machine representation；machine-checkable state-machine artifact；executable state-machine representation |
| 检查反馈 | lightweight formal / static diagnostics；semantic diagnostics；scenario simulation feedback |
| 修正循环 | diagnose-repair-regression loop；accept / reject / rollback protocol |
| 结果目标 | relatively better STM；auditable improvement over the same normalized `STM_0` |

中文写作中优先使用“反馈驱动状态机修正”“语义增强、可机检、可执行状态机制品”“相对更优 STM”。

## 2. `fcstm` / `pyfcstm` / DSL 弱化策略

| 位置 | 写法策略 |
|---|---|
| 标题 / 摘要 / Introduction contribution | 不出现 `fcstm` / `pyfcstm` / new DSL。 |
| Method implementation / artifact | 可作为内部实现载体说明，但必须低调。 |
| Reproducibility / artifact appendix | 可写工具名、commit、版本、运行入口。 |
| Related work positioning | 不把本文定位为 DSL 设计论文。 |

## 3. 禁止或需降级的表达

| 高风险表达 | 安全替代 |
|---|---|
| 首个 / 最强 `NL -> STM` 方法 | 本文研究给定初始状态机后的反馈驱动修正任务。 |
| 提出新 DSL | 使用语义增强、可机检、可执行的状态机制品作为实验载体。 |
| 完整形式化验证 / model checking 保证正确 | 使用轻量形式化 / 静态诊断和场景仿真反馈发现并约束缺陷。 |
| 自动修正一定提升质量 | 在预注册评价门下检验是否产生相对更优候选，并报告失败和不收敛。 |
| baseline 不需要比较 | baseline 重排为 seed source、转换压力、有限对照和 related work。 |
| run record 是方法贡献 | run record 是内部实验审计和复现证据链，不写成论文贡献。 |

## 4. 自检建议

实现或写作阶段可用以下 grep 作为人工审查入口。命中不一定错误，但必须确认是否只出现在 forbidden policy 中。

```bash
grep -RIn "首个\|最强\|new DSL\|完整形式化验证\|model checking\|NL -> STM.*主贡献" project_1_llm_state_machine_modeling/paper_stm_repair || true
```

## 5. 写作例句

| 场景 | 建议句 |
|---|---|
| Introduction task | We study feedback-driven repair of an initial state-machine artifact conditioned on natural-language requirements, rather than one-shot state-machine generation from text. |
| Method carrier | We normalize candidate artifacts into a semantically enriched, machine-checkable and executable state-machine representation to support diagnostics and scenario feedback. |
| Evaluation caution | Improvements are counted only against the same normalized `STM_0`; normalization and repair-loop effects are reported separately. |
