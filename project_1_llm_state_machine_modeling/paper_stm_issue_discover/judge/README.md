# Paper STM 人工裁定：冻结协议与审计接口

Paper1 当前结果中的 validity、relation、D/A、K/N/I 和成分分析均由人工完成。本目录保留 issue #195 的冻结协议、输入投影和审计接口，供历史实现与 provenance 对照；它不是当前结果的第二事实源。人工裁定接收 arm-neutral method report 和只读状态机制品闭包，并把 reason、basis、source refs、validity 与 relation 写入审计制品；method 不读取人工裁定输出。

## 两阶段判定

第一阶段为 validity：人工裁定者对单个 report 作证据和主张审查，产生 expected-isolated `FrozenValidityCertificate` 及其 `core_truth`。只有证书冻结为 valid 的 report 才进入第二阶段。第二阶段为 relation：人工裁定者在冻结 certificate 的约束下将 report 与显式提供的 expected issue 比较，给出 `FULL`、`PARTIAL` 或 `NONE`。最终 backend 依据 validity 与 relation closure materialize `VALID_KNOWN`、`VALID_NOVEL` 或 `INVALID`。两轴不能互相替代：`FULL/PARTIAL/NONE` 是 expected relation，`VALID_KNOWN/VALID_NOVEL/INVALID` 是 report validity，只有 `INVALID` 进入 report-level ordinary FP。

人工裁定使用调用方以受控输入投影提供的 expected material，不会回传给 method，也不构成 method 包的依赖或答案泄漏。人工裁定不控制 method 的 candidate、predicate、W、D 或发布路径；W 是 arm-generated finding 的证据形态，事后人工核验不会自动创造 W2。

## 协议、输入与输出

包内的 issue #195 snapshot 与冻结 protocol snapshot byte-identical，运行前由 SHA-256 校验。输入包含方法发布 report、状态机制品闭包和人工裁定所需的明确定义投影；输出是带 prompt/schema/provenance hash、certificate、relation/validity decision 和 reason/basis 的审计制品。当前 paper 只把人工完成并审核过的制品作为裁定依据。

## 安装与命令

发布构建脚本和冻结资源仅用于技术 provenance；本次 current v4 没有重新运行该实现或 provider，也没有重新进行人工裁定。

发布树只包含冻结人工裁定接口、稳定 protocol resource 和 manifest 列出的中立 `utils` 子模块；不包含 method、evaluation、ledger、baseline、final_results、run 或 legacy 数据。该技术树不改变 current v4 的人工裁定口径，也不构成新的 provider 实验授权。

issue #195 的两阶段人工裁定先区分作者源承重事实是否成立，再判断是否存在存活的被违反义务；D0/A0 都派生为 I，只有 D2/D1 能按 relation 进入 K/N。当前谓词或 backend 不支持只影响 W，不设 scope 出口。

## v3.4 起：显式 D/A 与作者源基准（校准中）

HEAD 上的实现是 `semantic-judge.two-stage.v3.8`（prompt v12；v3.4 至 v3.7 分别是校准第一至五轮的版本）。v3.8 把 K/N/I 的闭合顺序改为 **relation-first**（`--k-closure relation_first`，默认）：先判 hit，再对未命中的报告分 N / I。具体地，所有非 FALSE_POSITIVE 的报告都进入 relation 阶段；FULL_MATCH 把任何这样的报告闭合为 K（包括 validity 判为 D0 / NOT_A_DEFECT_CLAIM 的报告——这是人工实践：有台账命中的报告留 K，不再追问它是不是缺陷）；D2 / D1 报告的 PARTIAL_MATCH 也算 K（沿用 v3.2 口径），而 D0 / NOT_A_DEFECT_CLAIM 报告的 PARTIAL_MATCH 只记为 support、仍为 I；FALSE_POSITIVE 永不进入 K。`--k-closure validity_first` 保留 v3.2 的顺序（INVALID 一律全 NO）以便复现历史。prompt v12 相对 v11：FALSE_POSITIVE 锚定在报告引用位置上的事实（周边计数、命名、包含关系说错不构成假报告）；D1 要求缺陷读法至少与作者设计读法同样忠实；启动经 Off/Idle 再 start 进入工作态、组合态行为由子态迁移实现、事件名标签旁「缺守卫」、NL 要求的动作写成标签或状态体文字、UML 记法良构性抱怨五类改为范畴式 D0；契约或预期记录的缺项归 NOT_A_DEFECT_CLAIM；relation 定义恢复 v10（同根因、直接可归因症状、修复消除或实质缓解都算 FULL），因为 v11 的收紧在第三→第四轮上把 current 的漏匹配从 4 条抬到 12 条而过匹配只减 3 条。v3.7 曾只收紧 relation 阶段（FULL 限同 locus 同义务或预期文本点名的 facet，不同元素/层级/载体/修复义务为 NO），并对单报告批次的裸 item 响应做后端归一化。relation 阶段的 certificate 哈希自 v3.6 起由后端持有，模型不再需要回显。相对实跑的 v3.2 与从未实跑的 v3.3，它做了四件事：承重事实只以作者 NL 与 PlantUML 原文为准，派生表示只能佐证；validity 响应显式输出 `defect_adjudication.defect_class ∈ {D2, D1, D0, A0_FALSE_POSITIVE, A0_NOT_A_DEFECT_CLAIM}`，后端由它确定性派生 minimum-evidence gate 并把 `defect_class / d_tier / a0_subtype` 写进 `report_outcomes`；INDISPENSABLE_MECHANISM 收窄为「去掉它结论就不成立」的前提；载体纪律写成通用原则并由测试禁止 pair 编号、台账 ID 与臂名称进入提示词。CLI 新增 `--report-filter` 本地 allowlist，用于只判定选中的已发布报告。这一版的定位是后续实验的**初筛**，之后仍由人工逐条确认；对外口径不变。校准子集、事前登记与逐次结果见 [calibration/](./calibration/README.md)。它不重跑、不改写任何已冻结的 v60 / X1v2 结果。

v60/current 的冻结人工裁定实验提交为 `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`，协议标识为 `github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2`。完整输入、输出和独立复算见 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md)；该历史标识不得改写成 v3.3。
