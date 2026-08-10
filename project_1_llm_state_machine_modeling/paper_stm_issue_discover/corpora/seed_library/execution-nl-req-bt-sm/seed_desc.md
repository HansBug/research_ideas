# Execution of Natural Language Requirements Using State Machines Synthesised from Behavior Trees

## 基本判定

| 字段 | 内容 |
|---|---|
| 年份 | 2012 |
| venue | Journal of Systems and Software |
| URL / DOI | https://doi.org/10.1016/j.jss.2012.06.013 |
| strict seed 结论 | 🟠 / 中间产物边界 |
| 当前角色 | BT 中间产物 related work / 转换链证据 |

## 一句话总结

论文定义 Behavior Tree 到 UML State Machine 的 ATL 转换；BT 捕获自然语言需求，但核心贡献是 BT -> UML SM，不是直接 NL -> STM。

## P1--P4 证据

| 谓词 | 判定与证据 |
|---|---|
| P1_NL_INPUT | 自然语言系统需求；论文安全报警系统案例列出 7 条自然语言需求。 |
| P2_T0_STM_FAMILY | UML state machines，T0 基本可切。 |
| P3_GENERATION_RELATION | NL -> BT -> UML SM；BT 是显式中间建模产物，因此不作为主 seed。 |
| P4_EVIDENCE_POINTER | 本地 `paper.pdf` / `paper_content.txt`；论文提到 BT2SM examples PDF 和 TextBE/ATL/SHIRE 相关工具，但本轮未获得稳定作者原生 pair 包。 |

## 风险与 caveat

中间 BT 使其不满足“STM 必须直接基于 NL 生成”的强口径；BT2SMExamples 链接本轮访问超时。

## 使用建议

作为 formal path / transformation related work，不进 R2。
