# 独立学术与语义审查

## 范围和方法

审查者只读检查最终中文报告、issue #189、issue #195 protocol、`METHOD_PRINCIPLES.md`、冻结 registry、`current_source_catalog.json`、`CURRENT_SOURCE_AUDIT.md` 和 ground-truth limitation。未调用 provider，未修改实验制品、谓词定义、Judge 或报告以外的实现。

## 结论

未发现高严重度语义错误。报告正确地区分 W、Judge relation、K/N/I、predicate provenance 与 runtime W2；未把 bibliography 当作 W2 gate，未将 `VALID_NOVEL` 写成 FP，也未排除 W1 对 `VALID_KNOWN`/FULL 的支持。

## 发现与修正

- M：原稿只写“publication 依赖 D 判定”，未说明 D 与 Judge validity 不同。已补充：`D2/D1` 进入方法发布面，`D0` 不发布；Judge 独立裁定 validity 与 expected relation。
- M：原稿的 “L1/L2 只来自外置 ledger”可能被读成重定义 L。已改为：报告 L2 子集取 ledger `l_level`；L 是 issue #189 信息需求维度，method 不在运行时输出或裁定 `l_level`。
- M：原稿的泛化限制过于笼统。已明确不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序语义。

registry `source_types` 与 catalog 实际 `types` 在 `G1/G2/G4/R1/R2/R4/V1/V2/V4/V5` 上存在元数据差异。报告没有生成来源类型覆盖统计，也没有断言所有谓词具有同一来源类型组合；该风险不阻断报告，但后续不能直接按 registry `source_types` 统计类型覆盖。

## 交班前独立复核

当前 pane5 session 另行组织只读学术/语义复核，检查最终报告、issue #189/#195 protocol、冻结 registry、`current_source_catalog.json` 和 `CURRENT_SOURCE_AUDIT.md`。复核确认 `D2/D1/D0`、Judge validity/relation、`VALID_KNOWN`/`VALID_NOVEL`/`INVALID`、FULL/PARTIAL/NONE 与 W0/W1/W2 的叙述一致；19/19 谓词均有 source 映射，catalog 的 `28` 个 source ID 可解析。报告没有把 bibliography metadata 设为 runtime W2 gate，也没有将独立 LLM 采样差异表述为单一代码修改的因果结果。除上文已披露的历史 `source_types` 元数据差异外，未发现新的高、中严重度问题。
