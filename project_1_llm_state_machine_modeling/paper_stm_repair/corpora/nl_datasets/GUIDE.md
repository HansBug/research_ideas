# nl_datasets/GUIDE.md

## 0. 定位

本文件定义 [nl_datasets/](./) 的收录与维护规则。其目标是稳定管理控制系统纯 NL 输入来源，为后续构造 `<NL, STM_0>` 提供入口。

## 1. 硬边界

1. **NL 不等于 seed**：只有 NL 但没有 `STM_0` 生成关系的对象，一律只算 NL-dataset。
2. **不混 repair**：任何 repair / completion / refinement / feedback 任务都不属于本库。
3. **不抢 baseline**：seed / repair baselines 的对象不能挪到这里混记。
4. **不复制 project-level 真源**：本库只登记 paper1 选用、裁决、实验角色和回链，不整体搬运 [../../../sources/](../../../sources/)、[../../../data/](../../../data/) 或其他 project-level 长期事实表。
5. **不维护施工真源**：PR / issue 的动态进度只写 GitHub body/comment。
6. **不做大规模外部检索作为 PR-R1.8-D 的验收前提**：本阶段只冻结脚手架、字段和入口纪律。

## 2. 收录对象

| 类别 | 收录口径 | 首批可定位锚点 |
|---|---|---|
| 控制系统需求 | 功能安全需求、系统需求、用例、场景、标准片段 | [../../../../CLAUDE.md](../../../../CLAUDE.md) § 数据集信息中的 9 系统 / 101 功能安全需求；[../../../data/STM_GENERATION_DATASET_ANALYSIS.md](../../../data/STM_GENERATION_DATASET_ANALYSIS.md) 仅作 NL→STM generation 输入特征 dry-run |
| `sources/` 真实控制系统 NL 池 | paper-level 选用或候选使用的真实控制系统论文 NL 来源 | [../../../sources/](../../../sources/)；[../../evidence/source_coverage_ledger.md](../../evidence/source_coverage_ledger.md) |
| 旧 Path-1 线索 | 历史 Path-1 中仍可追溯、但尚未转成当前 seed 的 NL 候选 | [../../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md](../../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md) |
| 弱 seed 入口 | 适合弱模型 / 弱 prompt / 学生人工建模的 NL 来源 | 后续逐条登记 |
| 历史来源回链 | 已知 NL 来源但生成关系尚未闭合的对象 | 后续逐条登记 |

## 3. 排除对象

| 排除对象 | 原因 | 去向 |
|---|---|---|
| 已证明 `STM_0` 由同一 NL 生成的对象 | 已经具备 seed 关系 | [../seed_library/](../seed_library/)；本库只保留原始 NL 来源回链 |
| repair / completion / refinement 论文 | 研究对象是修正任务，不是纯 NL 来源 | [../repair_baselines/](../repair_baselines/) |
| 非控制系统或无法稳定映射到 STM family 的文本 | 不适合作为本论文实验来源 | negative evidence / out-of-scope |
| 许可不明且无法公开样本的文本 | 不能直接放入 `samples/` | 只登记来源说明、哈希、本地路径或待授权状态 |

## 4. `SUMMARY.md` 字段纪律

正式条目表至少包含以下字段。emoji 列只写 emoji，其释义以本文件 §5 的统一口径为准。

| 字段 | 说明 |
|---|---|
| `dataset_id` | 稳定 slug |
| NL 类型 | 需求 / 用例 / 场景 / 系统描述 / 标准片段 / 教学文本 |
| 领域 | 电梯、雷达、Microwave、train、PLC、UAV 等 |
| 规模 | 文本数 / 需求数 / 样例数；未知必须写 `待核` |
| 公开性 | 公开 / 本地可追溯 / 需授权 / 不公开 / 待核 |
| 许可 | 明确许可 / 论文引用 / 仓库内部 / 待核 |
| seed 构造潜力 | 适合弱模型 / 弱 prompt / 学生人工 / 不适合 / 待核 |
| 已有 STM 关系 | 无 STM / 有 STM 但生成关系未闭合 / 生成关系已闭合 |
| `seed_library crosslink` | 对应 seed slug；未闭合则留空或写 `-` |
| 实验角色 | 主来源 / fallback / 教学 seed / 负例 / related data |
| 证据指针 | 论文、repo、dataset card、页面或本地路径链接 |

## 5. emoji / enum 口径

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ |
|---|---|---|---|---|---|
| 公开性 | 可公开下载 / 可公开引用 | 本地可追溯但需说明 | 需申请 / 需授权 | 不可公开 | 待核 |
| seed 构造潜力 | 适合直接构造弱 seed | 需要少量清洗 | 需要大量人工改写 | 不适合 | 待核 |
| 生成关系闭合 | 已有明确 `NL -> STM_0` 关系 | 有 STM 但生成关系需补证 | 只有 NL 或只有弱模型线索 | 与 STM 无关 | 待核 |

## 6. 更新规则

- 只要条目仍然只有 NL，就继续留在 NL-datasets。
- 只有当 `STM_0` 生成关系被明确证明，才 crosslink 到 seed library。
- 单条目证据必须可点击、可追溯；不得只写“见论文”。
- 许可不明的数据默认不把正文样本写入 `samples/`；只写来源说明、哈希、本地路径或待授权状态。
- 后续新增条目后，必须同步更新 [SUMMARY.md](./SUMMARY.md) 的总账、风险和更新日志。

## 7. PR-R1.8-D 阶段验收

本阶段只要求：

1. `README.md / GUIDE.md / SUMMARY.md` 三件套存在且互相可点击。
2. 不创建任何 `<dataset-slug>/` 子目录。
3. `SUMMARY.md` 能说明首批锚点与字段口径。
4. 不把只有 NL 的对象提前计为 seed。
5. 不跑四例、不调用真实 LLM、不读取 `.env`。
