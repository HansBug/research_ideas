# 人工评测 v2 协议冻结记录

版本：`paper1.manual-adjudication.v2`。本文件只冻结评价规则，不提供任何 report label。

## 保护的事实

以下内容是 protected spans：版本名、commit、run ID、hash、路径、命令、issue 编号、模型名、
枚举、指标、分子/分母、输入角色和责任主体。文档改写不得改值、改归属或把历史 Judge
输出写成新的人工事实。

## 规则

- 先在 NL、作者 PlantUML 和必要的 source inventory 上核对承重事实，再裁 D/A。
- `D2` 是事实成立且义务明确；`D1` 是事实成立但存在两个具体、合理且存活的义务/载体读法；`D0` 是事实成立但没有被违反义务或设计正当；`A0` 是事实不成立、归错 work product 或把方法自有表示债务写成作者缺陷。
- A0 只有 `FALSE_POSITIVE` 和 `NOT_A_DEFECT_CLAIM`；X1v2 不得使用后者。
- 每条 report 对全部 145 expected issue 做一次 `FULL_MATCH`、`PARTIAL_MATCH` 或 `NO_MATCH`。invalid report 强制全部 `NO_MATCH`。
- `D0/A0 -> INVALID -> I`；`D2/D1 + FULL/PARTIAL -> VALID_KNOWN -> K`；`D2/D1 + 全部 NO_MATCH -> VALID_NOVEL -> N`。闭合由后端派生，不能信任模型自报。
- `W0/W1/W2` 只描述 finding evidence。W2 必须同时有精确 artifact hash、原始 executable object、terminal result 和 receipt；W 不参与 validity、relation、hit 或 FP。
- K 直接按 expected ledger hit 单元统计；N/I 只在同 side、同 pair 内按人工确认的同质 property、author-source locus、repair obligation 和 substantive cause 跨 round 归并，不能跨 side/pair 或按文本相似度自动合并。
- `hit@1` 分母为 435 个 `(expected_id, round)`，`hit@3`/`hit@all` 分母为 145 个 expected；L2 对应为 117/39。PARTIAL 不计主 hit、不计 FP。L2 ledger precision/FP 为 `not_applicable`。

## 当前状态

本版本已完成双侧逐条人工监督确认：v60/current `1271/1271`、X1v2 `512/512`，并由
`relation_decisions.json` 保存 `258535` 条 dense relation。444 条 frozen N 与 106 条
frozen I 仍只作为 raw-first calibration reference；旧 Judge、`reviews/11`、`reviews/12`
和旧 witness audit 从未直接复制为 FINAL。用户授权的 pane5 主 session 是最终 adjudication
session；independent reviewer 如实保存为 subagent proposal。最终 blocker 列表为空，
所有最终标签均有逐条 raw/source evidence-read、reason、basis、source_refs 和 attestation。
