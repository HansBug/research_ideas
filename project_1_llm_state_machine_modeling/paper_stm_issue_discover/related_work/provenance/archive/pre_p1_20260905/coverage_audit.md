# 来源与执行覆盖口径

来源覆盖、predicate backend conformance 与实验 execution coverage 是三个不同指标，必须分别报告。

| 指标 | 固定分母 | 含义 |
|---|---:|---|
| 学术来源覆盖 | 19 | 冻结谓词的 registry 来源 ID、类型、落点与边界均可复核 |
| backend conformance | 19 | 每个谓词都有 native callable backend 与 positive/negative/invalid/out-of-fragment/failure fixture |
| 15-pair execution | 12 | S1/S2/S3/S4/S5/S6/G1/G4/R1/R4/V1/V4 的真实 terminal receipt 数 |
| 54x3 planned execution | 15 | 预先固定 planned 谓词的真实 terminal receipt 数 |
| W2/expected | 固定 expected 分母 | 已命中 expected 中由 completed Boolean receipt 支撑的数量 |

来源覆盖不因某个 pair 没有闭合输入而改变；backend conformance 不因 planned count 为零而豁免；execution coverage 不把 schema、preflight、prompt 出现、pass probe 或 unit fixture 计为真实实验使用。任何未闭合 input 必须保留具体 `input_contract_missing` 或 `out_of_fragment` 原因。

W2/expected 与 FULL expected 的 max-W2 占比也不是同一指标：前者使用固定 expected 分母，后者只在独立 Judge 标为 FULL 的 expected 上计算每项最高 W。两项都不得以缩小分母提升数字。
