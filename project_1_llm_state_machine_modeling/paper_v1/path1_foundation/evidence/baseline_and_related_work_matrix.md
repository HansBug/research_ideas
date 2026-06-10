# Baseline and Related Work Matrix

## 1. 口径

本文件用于把 [../../../baselines/SUMMARY.md](../../../baselines/SUMMARY.md) 中的近邻工作压缩成 Path-1 paper 可执行 baseline / related work 矩阵。这里的分类不是最终 Related Work 文本，而是实验对齐计划。

分类：

- **Direct executable / approximate baseline**：尽量同输入、同模型预算、同输出表示、同 human rubric。
- **Near baseline**：任务接近，但输出、输入、artifact 或模型约束不完全可比。
- **Evidence-only comparison**：不能复现或不适合重跑，只用于说明 prior work 能力边界。
- **Background**：支撑 problem setting、classical requirements-to-model 或 formal modeling 背景。

## 2. Closest prior works currently tracked

| 候选 | 年份 | 内部路径 | citation / read status | 关系 | 当前对齐计划 | 风险 |
|---|---:|---|---|---|---|---|
| Structure- and Event-Driven Frameworks for State Machine Modeling with LLMs | 2026 | [../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/](../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | corpus-read；manuscript citation 待核验 | 最直接 NL→UML state machine prompt baseline | 优先 same-sample approximate baseline；若原 case 不兼容 history/parallel，则在 frozen sample 上复刻策略 | 公平性 C：不能声称 same benchmark 打赢 |
| Generating SysML Behavior Models via LLMs | 2025 | [../../../baselines/llms_emp/](../../../baselines/llms_emp/) | corpus-read；manuscript citation 待核验 | SysML behavior model + checking feedback repair | 对齐 feedback types、repair loop、quality dimensions；若可行做 approximate baseline | 输出与工具不同，需明确不可比处 |
| TTool-AI / Automatic System Modeling with AI | 2024 | [../../../baselines/ttool-ai/](../../../baselines/ttool-ai/) | corpus-read；manuscript citation 待核验 | NL→SysML blocks/state machine + tool feedback | evidence-based comparison + small approximate case if feasible | 复现成本和 artifact 可用性 |
| Exploring Llama3 for Umple State Machines | 2025 | [../../../baselines/umple/](../../../baselines/umple/) | corpus-read；manuscript citation 待核验 | NL→Umple state machine prompt/RAG baseline | structured / RAG prompt baseline 参照 | 模型和数据差异 |
| Automotive statechart generation from NL requirements | 2025 | [../../../baselines/req/](../../../baselines/req/) | corpus-read；manuscript citation 待核验 | 汽车需求到 statechart，领域近 | automotive subset / expert rubric 对齐 | 数据和微调细节可能不可复现 |
| IEC 61499 FSM iterative refinement | 2025 | [../../../baselines/fsm-gen-iec-61499/](../../../baselines/fsm-gen-iec-61499/) | corpus-read；manuscript citation 待核验 | 控制需求 + FSM + simulation/code generation refinement | iterative refinement / simulation feedback related work | 输出与系统边界不同 |
| Executable State Machines Derived from Structured Textual Requirements | 2019 | [../../../baselines/executable-state-machines-derived-from-structured-textual-requirements/](../../../baselines/executable-state-machines-derived-from-structured-textual-requirements/) | corpus-read；manuscript citation 待核验 | structured requirements → executable FSM | classical background for executable model derivation | 非 LLM，不作 direct baseline |
| Coq timed DFRS from controlled NL | 2019/2020 | [../../../baselines/modelling-timed-reactive-systems-from-natural-language-requirements/](../../../baselines/modelling-timed-reactive-systems-from-natural-language-requirements/) / [../../../baselines/validating-verifying-and-testing-timed-data-flow-reactive-systems-in-coq/](../../../baselines/validating-verifying-and-testing-timed-data-flow-reactive-systems-in-coq/) | corpus-read；manuscript citation 待核验 | CNL→formal reactive model + verification/testing | background for stronger formal methods | 不能混同本稿 lighter formal feedback |

## 3. Minimal external baseline contract

正式实验前必须满足：

1. `>=3` 个 closest prior work 进入 baseline / related-work matrix。
2. `>=1` 个 closest prior work 进入 same-sample approximate baseline；目标争取 `>=2` 个。
3. evidence-only comparison 必须说明不可复现原因、缺失工件、不可比输出或 license/API 限制。
4. 主结果不能只展示内部 ablation；至少一张表必须把 full method 与 closest executable / approximate prior baseline 放在同一样本、同一输出 representation、同一 rubric 下。
5. 如果 external baseline 用不同 input context，例如 paper directory / examples / RAG，必须写入预算表，避免隐性信息不公平。

## 4. Contribution positioning

本稿相对 prior work 的主张应控制为：

| 维度 | Prior work 常见情况 | 本稿可主张的差异 | 证据需求 |
|---|---|---|---|
| 输出表示 | UML/SysML/Umple/Mermaid 等状态机或行为模型 | formalized executable state-machine representation | parser / semantic / simulator / component extraction |
| Feedback | prompt refinement、schema/grammar checking、人工评审 | parse + semantic + design diagnostics + simulation trace as in-loop feedback | ablation B2/B3/B4/B5 |
| Repair | regenerate / iterative prompting | structured fix request、accept/reject、FixLog、SL-10 review | run record / repair trace |
| Evaluation | manual slot F1、expert score、render/compile validity | component-level human adjudication + deterministic validity + failure taxonomy | human protocol + agreement |
| Auditability | often prompt/output only | run record with raw outputs, stage trace, scenario, diff, eligibility | artifact package |

## 5. Claims to avoid in Related Work

- 不要说 prior work “没有形式化” 除非已核验其工具反馈/verification 细节。
- 不要把 PlantUML/TTool/Umple 的语法或一致性检查称为完整 model checking。
- 不要把 classical CNL→formal model work 降低成“无 LLM 所以不相关”；它们是 formal rigor background。
- 不要把 inability to reproduce 写成 prior work weakness；应写 artifact / assumption / output mismatch。

## 6. Required literature / citation artifacts before Related Work

当前 foundation 只建立 baseline matrix，不等于 manuscript citation gate 已通过。进入 Related Work / Introduction 写作前必须新增或维护以下 manuscript-level artifacts：

| Artifact | 目的 | Ready gate |
|---|---|---|
| `literature/paper_inventory.md` | 记录 manuscript 级引用候选、官方 URL/DOI、本地 corpus 状态 | 每个核心引用有 verified metadata |
| `literature/related_work_matrix.md` | 按主题归类 closest prior works、差异和可比性 | direct / near / evidence-only 分类清楚 |
| `literature/positioning.md` | 固定本稿相对 closest work 的 task / assumption / evidence 差异 | 不夸大 novelty，不误述 prior work |
| `references.bib` | manuscript BibTeX 真源 | 从权威来源获取，不手写猜测 |
| `citation_verification.md` | 每条引用支持哪一句 claim | sentence-level claim 有来源 |

上述文件尚未创建，因此当前 foundation 不能直接进入 Related Work 成稿，只能作为 related-work planning 入口。
