# 谓词来源与边界审计

本目录记录 `four-family-19-core.v1` 的来源、语义和论文写作边界。[谓词来源审计](./predicate_provenance.md)是 19 条当前谓词的唯一人读事实源，承载完整书目、逐字引文、页码、legacy/current crosswalk、三类责任、方法片段和逐 polarity 发表资格。`current_source_catalog.json` 只保存冻结 source-ID mapping 与 R1 结构化 audit metadata，不复制书目或引文。

三类来源承担不同责任：

1. 领域来源（`domain`）说明控制或工程状态机中相关义务的实际动机，不能证明普遍正确性。
2. 形式来源（`formal`）说明元模型、图性质或性质模式的精确定义，不能证明某条 NL 义务已经成立。
3. 技术来源（`technical`）说明类型化绑定、后端、回执或重放的技术边界，不能单独赋予业务规则合法性。

R1 按三类责任分别审计：外部领域/形式来源说明 requirement-relative obligation，版本化的方法说明、代码与测试说明 FCSTM 执行语义，pair-level NL/source binding 说明实例 authority。registry 与 backend 不同形时，不改写冻结运行记录，而是以 supported fragment、sound proxy 或逐 polarity publication exclusion 给出论文解释边界。

W2 是一次报告的执行见证，不是文献资格：它需要精确制品、合法类型化输入、声明片段、编译对象、当前制品归因、原生后端终止布尔结果和完整回执。仍在全局范围内的失败、输入缺失或能力边界可保留为 W1/W0；全局范围外的语言或模型语义按失败关闭隔离。人工完成 D/A、有效性、关系和成分分析，程序据此确定性派生 K/N/I；本目录不改变运行路径、后端、W、分母或任何冻结结果。

机器目录 [`current_source_catalog.json`](./current_source_catalog.json) 与方法包中的同名资源不同，不能反向修改运行时注册表。它只保存 R1 所需的 status、relation、impact 和 source-ID closure；完整外部引文仍只在审计文档中维护。
