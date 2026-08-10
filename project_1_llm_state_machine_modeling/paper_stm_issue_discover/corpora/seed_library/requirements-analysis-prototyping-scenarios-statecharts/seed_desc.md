# Requirements Analysis and Prototyping Using Scenarios and Statecharts

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2002 |
| venue | ICSE Workshop: Scenarios and State Machines |
| URL / DOI | https://www.academia.edu/download/31191491/1.pdf |
| 种子结论 | 🔴 / 方向相反 |
| 当前角色 | co-evolution / reverse-direction sentinel |

## 一句话总结

论文主张从 integrated structured statechart model 生成 scenarios，并用 STAMP 做原型验证；方向不是 NL requirements -> STM，而是 statechart/scenario 协同与 scenario generation。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | scenarios / action descriptions；不是直接自然语言需求文档作为唯一输入。 |
| P2_T0_STM_FAMILY | statecharts / state machines；T0 形式存在。 |
| P3_GENERATION_RELATION | 主要是 statecharts -> scenarios / scenarios 与 statecharts 协同，不满足 seed 方向。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；Academia 下载入口可追踪但访问 403；未发现公开工具或 pair。 |

## 风险与 caveat

已判定为非 `NL -> STM_0`，更接近 statechart / scenario 协同或 reverse-direction sentinel；不是 initial NL -> STM seed。

## 使用建议

保留 hard exclusion / co-exist/reverse sentinel，不计 R2。
