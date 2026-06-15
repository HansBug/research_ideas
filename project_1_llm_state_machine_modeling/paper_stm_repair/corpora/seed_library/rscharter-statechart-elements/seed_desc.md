# RSCharter: A Framework for Extracting Statechart Diagram Elements from the Requirements Specification

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2024 |
| venue | SSRN preprint |
| URL / DOI | https://doi.org/10.2139/ssrn.4964857 |
| 种子结论 | 🟡 / 条件种子 |
| 当前角色 | statechart-element extraction related work |

## 一句话总结

RSCharter 从 RUPP/EARS 风格 NL SRS 中抽取 statechart diagram elements，转为 FOPL 并由 State Diagram Generator 生成 statechart；当前为未同行评审预印本。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | PuRE dataset 中的 SRS 文档 / NL requirements。 |
| P2_T0_STM_FAMILY | statechart diagram elements / state diagram；T0 取决于 SDG 输出，论文更强调 elements 与 FOPL。 |
| P3_GENERATION_RELATION | NL SRS -> FOPL -> state diagram；生成关系存在但含 FOPL 中间层。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；SSRN 页面和 DOI 可访问；论文称 augmented dataset 将在接收后开源，当前未公开。 |

## 风险与 caveat

preprint not peer reviewed；增强数据未公开；代码/完整 pair/license/hash 未公开。

## 使用建议

作为近期 rule-based/NLP 相关工作与条件种子 / 方法证据，不计当前 R2 四例。PuRE 的许可 / 版本只覆盖原始来源数据，不覆盖 RSCharter 增强 pair / code。
