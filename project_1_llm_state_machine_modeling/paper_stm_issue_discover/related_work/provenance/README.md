# 谓词学术来源档案

本目录保存 `four-family-19-core.v1` 的来源 ID、原始落点、三类来源与适用边界。当前已完成 19 个冻结谓词的 source-ID mapping、claim-support 和 boundary 对照；这不是完整书目、DOI 或全文逐字核验。本目录提供可复核的 scholarly provenance，而不是运行时资格判定。

机器目录是 [current_source_catalog.json](current_source_catalog.json)，人工入口是 [CURRENT_SOURCE_AUDIT.md](CURRENT_SOURCE_AUDIT.md)。每个来源记录 `id`、`types`、`title`、`paths`、`supports` 与 `boundary`，并可由 registry 的 `source_ids` 回链。

来源类型的职责互补：

1. `domain` 说明控制系统和工程状态机中的命题背景；
2. `formal` 说明状态机、性质模式或标准中的定义；
3. `technical` 说明 FCSTM、backend、反例和回执的实现边界。

这些 metadata 不参与运行时 W、backend availability、D/publication、route 或 execution coverage。单次 W2 只由当前被检制品的精确 typed inputs、native backend、terminal Boolean result 和 artifact attribution 决定；学术来源继续保留在 registry 和 audit bundle 中供复核。

来源边界必须在论文叙事和实现说明中保留，特别是 timed、parallel、hybrid、无界时序或领域特殊假设。边界用于限制论文声明，不用于降低冻结谓词的运行时资格。
