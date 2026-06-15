# nl_datasets — 控制系统纯 NL 数据源文库

## 0. 定位

本目录用于收集控制系统自然语言需求、用例、场景、系统描述、标准片段与教学案例等纯 NL 输入来源，服务于第一篇论文后续构造 `<NL, STM_0>` 的实验入口。

**核心边界**：只有 NL 不等于 seed。只有当某个 NL 来源经过明确流程生成并保留 `STM_0` 之后，生成后的 `<NL, STM_0>` 才能 crosslink 到 `seed_library/`；原始 NL 来源仍留在本库。

## 1. 结论速览

- 这是三类文库之一：`seed_library` / `repair_baselines` / `nl_datasets`。
- 本库只维护纯 NL 数据源，不维护 repair baseline，也不维护 seed 方法本体。
- 当前先做脚手架与字段纪律冻结，后续再逐步填充来源条目。

## 2. 阅读顺序

1. [./README.md](./README.md)：先看定位和边界。
2. [./GUIDE.md](./GUIDE.md)：看收录 / 排除 / 分级 / 更新规则。
3. [./SUMMARY.md](./SUMMARY.md)：看当前总账与已知数据源角色。
4. 再根据条目进入单独 dataset 目录。

## 3. 单条目结构

每个 dataset 条目后续建议至少包含：

- `dataset_card.md`
- `source_refs.md`
- `samples/`（仅存可公开或可追溯样本；敏感数据只存说明）

## 4. 与上游文库的关系

- [../seed_library/](../seed_library/) 负责 `NL -> STM_0` 的 seed 方法 / 来源。
- [../repair_baselines/](../repair_baselines/) 负责 `STM_0 -> STM_k / Better STM` 的修正近邻。
- 本库只负责纯 NL 数据源；不把只有 NL 的对象提前当 seed。
