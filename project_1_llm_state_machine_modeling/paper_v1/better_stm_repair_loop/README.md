# 第一篇新主线：反馈驱动状态机模型修正

## 0. 当前定位

本目录是第一篇论文在 2026-06-12 导师讨论后新建的 R0 工作区，服务于 PR [#102](https://github.com/HansBug/research_ideas/pull/102) / PR-R0「主线与范围冻结」。它从 PR [#100](https://github.com/HansBug/research_ideas/pull/100) 的伞 PR 合同落地，不继承历史 PR [#93](https://github.com/HansBug/research_ideas/pull/93) 的旧 `Path-1 / NL -> STM` 生成主线。

**当前核心任务**：研究给定自然语言需求与初始状态机 `<NL, STM_0>` 后，能否通过无人化、反馈驱动的检查 / 诊断 / 场景仿真 / 修正 / 回归循环得到相对更优的 `STM_k`。

本目录只冻结论文 story、任务边界、claim gate、研究问题草案、评价门原则与后续 PR 接口；它**不**执行四例真实运行、不调用真实 LLM、不冻结样本、不做 baseline 逐篇资产盘点、不写最终论文正文。

## 1. 事实源优先级

| 优先级 | 事实源 | 使用方式 |
|---:|---|---|
| 1 | [PR #100](https://github.com/HansBug/research_ideas/pull/100) | 第一篇新主线伞 PR；定义 R0--R7 依赖与验收门。 |
| 2 | [PR #99 会后定调 comment](https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818) 与 [2026-06-12 导师讨论记录](../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇转向 `<NL, STM_0> -> STM_k / Better STM` 的最高优先级学术约束。 |
| 3 | `main` 已合入的 baseline 线索：[#73](https://github.com/HansBug/research_ideas/pull/73)、[#82](https://github.com/HansBug/research_ideas/pull/82)、[#92](https://github.com/HansBug/research_ideas/pull/92) | 后续 PR-R1 的资产盘点线索；R0 不做逐篇复核。 |
| 4 | 历史分支局部资产：[#93](https://github.com/HansBug/research_ideas/pull/93)、[#94](https://github.com/HansBug/research_ideas/pull/94)、[#96](https://github.com/HansBug/research_ideas/pull/96) | 只作历史结构、baseline 反证和旧 claim gate 线索；不得当作 `main` 已有事实。 |

## 2. 目录结构

```text
better_stm_repair_loop/
├── README.md
├── story/
│   ├── README.md
│   ├── paper_story.md
│   ├── task_boundary.md
│   ├── terminology_policy.md
│   ├── claim_evidence_map.md
│   └── paper_outline.md
├── evidence/
│   ├── README.md
│   ├── upstream_fact_ledger.md
│   └── legacy_asset_inheritance.md
├── experiment_design/
│   ├── README.md
│   ├── research_questions.md
│   ├── better_stm_definition.md
│   └── evaluation_gate.md
└── plan/
    ├── README.md
    ├── progress.md
    └── agent_provenance.md
```

## 3. 推荐阅读顺序

1. 本 [README.md](./README.md)：确认新主线、事实源优先级和目录职责。
2. [story/paper_story.md](./story/paper_story.md)：理解论文 thesis、gap、method insight 与禁止 claim。
3. [story/task_boundary.md](./story/task_boundary.md)：确认 `<NL, STM_0> -> STM_k` 的输入、输出、方法内外边界和 no human-in-the-loop 口径。
4. [story/terminology_policy.md](./story/terminology_policy.md)：确认 `fcstm` / `pyfcstm` / DSL 的弱化策略。
5. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：写作或评审时先查 claim 是否有证据与允许措辞。
6. [experiment_design/better_stm_definition.md](./experiment_design/better_stm_definition.md)：确认 `Better STM` 的最小操作化定义。
7. [experiment_design/research_questions.md](./experiment_design/research_questions.md) 与 [experiment_design/evaluation_gate.md](./experiment_design/evaluation_gate.md)：理解 RQ 草案和后续 R4/R6 必须继承的评价门原则。
8. [evidence/upstream_fact_ledger.md](./evidence/upstream_fact_ledger.md) 与 [evidence/legacy_asset_inheritance.md](./evidence/legacy_asset_inheritance.md)：追溯事实来源和旧 Path-1 资产边界。
9. [plan/progress.md](./plan/progress.md) 与 [plan/agent_provenance.md](./plan/agent_provenance.md)：查看本 PR 的审阅、检查和剩余风险。

## 4. 非目标

R0 明确不做以下工作：

1. 不运行四例真实样例或真实 LLM。
2. 不冻结 `seed_id`、样本 registry 或 rehearsal panel。
3. 不定义多格式转换器 schema、fixture 或转换冒烟。
4. 不冻结诊断代码、场景套件、评价量表终稿或主实验协议。
5. 不实现或重构 `method/`、LangGraph、pyfcstm submodule 或 provider 配置。
6. 不写最终 manuscript；只写论文结构与 story gate。
7. 不把 run record、工程留痕、框架拆分或工具名写成论文方法贡献。

## 5. 与旧 `paper_v1/` 文件的关系

`paper_v1/README.md`、`PATH1_HARD_COMPARISON_GUIDE.md`、`PATH2_DIFFERENTIATION_GUIDE.md` 和 `selection/` 等文件保留历史价值，但其中 2026-05 Direction-Decision Sprint / Path-1 hard comparison 口径已经被 2026-06-12 导师定调和 PR #100 覆盖。后续涉及第一篇论文当前 story 时，应以本目录为入口。

旧 PR [#93](https://github.com/HansBug/research_ideas/pull/93) 分支上的 `path1_foundation/` 只作为历史参考；本目录不会在该路径下新增、移动或修改文件。旧资产继承边界见 [evidence/legacy_asset_inheritance.md](./evidence/legacy_asset_inheritance.md)。
