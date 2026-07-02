# protocols/ — 实验协议职责入口

本目录预留真实修正循环、对照 / 消融、人工裁决、回滚、重试和审计协议。

当前状态：仅冻结职责入口，尚未冻结主实验协议，也未声明任何真实 LLM 运行已完成。

后续协议必须先于真实结果冻结，并记录输入输出、模型配置、失败处理、redaction、run record 和复验方式。

## R5.7.1 已冻结的后续协议接口

R5.7.1 已在 [../evaluation_logic.md](../evaluation_logic.md) 中冻结以下接口，供 R5.7.5 / R6 / R7 / R8 继承：

1. repair gain 只能从 canonical `STM_0 -> STM_k` 开始计算；raw -> canonical 的 conversion / normalization / representation lowering 不计 repair gain。
2. 每个 repair run 必须保留 change-level attribution ledger，至少能说明 source artifact、canonical baseline hash、candidate hash、change type、证据来源、是否可计 repair gain 和禁止归因理由。
3. failure、partial、unknown、out-of-scope、rollback、oscillation、non-convergence 必须进入可审计 ledger；不能只保存 success。
4. 真实 LLM 调用仍需遵守仓库 `.env`、provider、model id、prompt、raw output、usage、redaction 与 run record 纪律；当前 R5.7.1 不调用真实 LLM。
