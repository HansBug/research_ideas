# Web Tool for Goal Modelling and Statechart Derivation

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2015 |
| venue | IEEE RE |
| URL / DOI | https://doi.org/10.1109/RE.2015.7320444 |
| strict seed 结论 | 🔴 / 非 NL 直接输入 |
| 当前角色 | goal-model -> statechart sentinel |

## 一句话总结

GATO 从 goal/design model 中 derivation statecharts；输入是 goal model / flow expressions，不是自然语言需求直接生成 STM。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | goal model / requirements view，非原始 NL-only 输入。 |
| P2_T0_STM_FAMILY | statecharts；当前工具仅生成 atomic states。 |
| P3_GENERATION_RELATION | goal model -> statechart；不是 NL -> STM。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；论文 supplement http://www.cin.ufpe.br/~ler/supplement/re2015/ 可访问；未确认可直接拿到 pair。 |

## 风险与 caveat

输入不是 NL；只能作为 goal-to-statechart 相关工作或边界。

## 使用建议

保留 sentinel / related work，不计 R2。
