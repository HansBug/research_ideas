# MARITACA: From Textual Use Case Descriptions to Behavior Models

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2017 |
| venue | IEEE/IFIP DSN-W |
| URL / DOI | https://doi.org/10.1109/DSN-W.2017.33 |
| strict seed 结论 | 🟢 / strict paper seed |
| 当前角色 | 传统 NLP seed 方法 / paper-only 强证据 |

## 一句话总结

MARITACA 使用 NLP 技术从半结构化 textual use case descriptions 抽取 state machine models，目标是得到可进一步 refined 的 preliminary state model。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 半结构化 textual use case descriptions；论文说明 UC 通常是自然语言，方法要求结构化格式。 |
| P2_T0_STM_FAMILY | state machine / behavior model；T0 基本符合 state machine family。 |
| P3_GENERATION_RELATION | 工具 MARITACA 从 UC 描述自动抽取 state machine，生成关系清楚。 |
| P4_EVIDENCE_POINTER | 本地 PDF/全文；论文称三个产品的完整 UC 和其他 artifacts 在作者网页 [22]，但本轮访问返回 403。 |

## 风险与 caveat

作者网页 artifact 当前 403；代码 / 完整 pair / 来源 / 版本 / hash 未公开冻结。

## 使用建议

可作 strict seed 文献和传统 NLP baseline 证据；缺作者原生 pair，不计 R2 主样本。
