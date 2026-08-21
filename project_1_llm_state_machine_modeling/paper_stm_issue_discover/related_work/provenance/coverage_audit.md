# 当前覆盖审计入口

旧覆盖审计已归档到 [`archive/legacy_20260821/coverage_audit.md`](archive/legacy_20260821/coverage_audit.md)。

当前只冻结设计可表达性快照：台账 `118/145 = 81.4%`、L2 `35/39 = 89.7%`、v27
`603/741 = 81.4%`。这是核心谓词对需求义务的映射，不是新代码运行后的 W2 命中率。

实测报告必须分开统计：精确语义绑定的 `semantic_hit`（包括 W1）、W2 可执行回执、
W0 coverage gap，以及后端 `UNKNOWN`。W1 不得因没有谓词而丢失，UNKNOWN 不得转成
violation。任何覆盖率提升建议都不能绕过学术来源、命题匹配和变更门。
