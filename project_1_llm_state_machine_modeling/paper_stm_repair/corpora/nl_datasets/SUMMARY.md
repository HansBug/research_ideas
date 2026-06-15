# nl_datasets/SUMMARY.md

## 0. 当前结论

本目录当前处于 **初始化脚手架阶段**：已冻结 NL-datasets 的边界、入口和字段纪律，但尚未开展大规模外部检索或逐条填充 dataset 目录。

当前阶段最重要的结论是：**9 系统 / 101 功能安全需求、`sources/` 真实控制系统 NL 池、旧 Path-1 `sources/` T0+🟢 线索，都是后续 NL-datasets 首批填充锚点；但在 `STM_0` 生成关系闭合前，它们仍只算 NL 数据源，不算 seed。**

## 1. 三类文库中的角色

| 文库 | 角色 |
|---|---|
| [../seed_library/](../seed_library/) | 上游 `NL -> STM_0` seed 方法 / 来源 |
| [../repair_baselines/](../repair_baselines/) | `STM_0 -> STM_k / Better STM` 修正近邻 |
| [./](./) | 控制系统纯 NL 输入来源 |

## 2. emoji / enum 标准

emoji 列只写 emoji，释义如下。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ |
|---|---|---|---|---|---|
| 公开性 | 可公开下载 / 可公开引用 | 本地可追溯但需说明 | 需申请 / 需授权 | 不可公开 | 待核 |
| seed 构造潜力 | 适合直接构造弱 seed | 需要少量清洗 | 需要大量人工改写 | 不适合 | 待核 |
| 生成关系闭合 | 已有明确 `NL -> STM_0` 关系 | 有 STM 但生成关系需补证 | 只有 NL 或只有弱模型线索 | 与 STM 无关 | 待核 |

## 3. 当前应保留的字段组

| 字段 | 用途 |
|---|---|
| `dataset_id` | 稳定条目标识 |
| NL 类型 | 需求 / 用例 / 场景 / 系统描述 / 标准片段 / 教学文本 |
| 控制系统领域 | 电梯、雷达、Microwave、train、PLC、UAV 等 |
| 规模 | 文本数 / 需求数 / 样例规模 |
| 公开性 | 公开 / 本地可追溯 / 需授权 / 不公开 / 待核 |
| 许可 | 明确许可 / 论文引用 / 仓库内部 / 待核 |
| seed 构造潜力 | 弱模型、弱 prompt、学生人工建模 |
| 与已有 STM 关系 | 是否已有 STM，是否能证明由 NL 生成 |
| `seed_library crosslink` | 生成关系闭合后对应的 seed slug；未闭合则为 `-` |
| 实验角色 | 主来源、fallback、教学 seed、负例、related data |
| 证据指针 | 论文、repo、dataset card、页面或本地路径链接 |

## 4. 首批填充锚点（非正式条目）

本表只是后续填充入口，不等于当前已完成 dataset 总账。

| 锚点 | 来源路径 | 已知规模 / 事实 | 当前角色 | 关键 caveat |
|---|---|---|---|---|
| 9 系统 / 101 功能安全需求 | 仓库级数据集说明；[../../../data/STM_GENERATION_DATASET_ANALYSIS.md](../../../data/STM_GENERATION_DATASET_ANALYSIS.md) | 9 个控制系统、101 条功能安全需求 | 首批 canonical NL 数据集锚点 | 若已有 STM 生成关系未闭合，仍只算 NL-dataset |
| `sources/` 真实控制系统 NL 池 | [../../../sources/](../../../sources/)；[../../evidence/source_coverage_ledger.md](../../evidence/source_coverage_ledger.md) | 787 篇来源；source coverage ledger 记录 337 条 `T0+FSM/HSM/EFSM` 子池 | 后续弱 seed / 学生 seed 的主要 NL 来源池 | `sources/` 中 STM.md 是整理结果，不自动证明 `NL -> STM_0` seed 关系 |
| 旧 Path-1 `sources/` T0+🟢 线索 | [../../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md](../../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md) | 历史 Path-1 曾规划从 `sources/` T0+🟢 子集分层抽样 | 历史回链与后续候选参考 | 旧 Path-1 story 不再作为当前第一篇事实真源，只保留可追溯线索 |
| 公开 NL→STM generation 数据集分析 | [../../../data/STM_GENERATION_DATASET_ANALYSIS.md](../../../data/STM_GENERATION_DATASET_ANALYSIS.md) | `llms_emp`、`ttool_ai`、`light_control_nimbus`、`structure_event_driven` 的 NL 输入特征分析 | 作为 dataset 字段 dry-run 与对照参考 | 其中部分对象已属于 seed 或 baseline 语境，不能混入当前纯 NL 角色 |

## 5. 后续工作边界

- 先基于已有 sources/data 搭建 NL-datasets 入口，不做大规模外部检索。
- 只有 NL 不等于 seed；需要明确 `STM_0` 生成关系后才 crosslink。
- 后续如果确有新数据源，再逐条补充 summary 与单条目目录。
- 许可不明或敏感数据不直接复制正文样本，只登记可追溯指针。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 23:20:00 | 初始化 NL-datasets 三件套脚手架，补充首批填充锚点、字段组、emoji 口径与 seed crosslink 规则。 |
