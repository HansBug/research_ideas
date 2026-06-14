# Modeling and Verification of Natural Language Requirements Based on States and Modes

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2024 |
| venue | Formal Aspects of Computing |
| URL / DOI | https://doi.org/10.1145/3640822 |
| strict seed 结论 | 🟠 / 非 STM 输出 |
| 当前角色 | requirements formalization / model checking related work |

## 一句话总结

论文设计 MoSt DSL 组织 states/modes requirements，并生成 NuSMV 模型进行验证；不是输出 FSM/HSM/EFSM/statechart 作为目标 STM。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 自然语言需求经 MoSt DSL 重写/建模，案例含车状态、洗衣机手册等。 |
| P2_T0_STM_FAMILY | MoSt model / NuSMV model；虽然 NuSMV 描述 transition relation，但不是目标 STM family。 |
| P3_GENERATION_RELATION | NL requirements -> MoSt DSL -> NuSMV；偏形式化验证，不是 seed pair。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；GitHub https://github.com/liuyinling/MoSt-Modeling-Tool 可访问。 |

## 风险与 caveat

输出 formal model / NuSMV，不是 T0 STM family；不应误作 seed。

## 使用建议

作为 formalization/model-checking related work，不计 R2。
