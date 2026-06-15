# nl_datasets — 控制系统纯 NL 数据源文库

## 0. 定位

本目录用于收集控制系统自然语言需求、用例、场景、系统描述、标准片段与教学案例等纯 NL 输入来源，服务于第一篇论文后续构造 `<NL, STM_0>` 的实验入口。

**核心边界**：只有 NL 不等于 seed。只有当某个 NL 来源经过明确流程生成并保留 `STM_0` 之后，生成后的 `<NL, STM_0>` 才能 crosslink 到 [../seed_library/](../seed_library/)；原始 NL 来源仍留在本库。

## 1. 结论速览

- 这是三类文库之一：[../seed_library/](../seed_library/) / [../repair_baselines/](../repair_baselines/) / [./](./)。
- 本库只维护纯 NL 数据源，不维护 repair baseline，也不维护 seed 方法本体。
- 当前 PR-R1.8-D 只做脚手架与字段纪律冻结，不创建具体 `<dataset-slug>/` 子目录，不开展大规模外部检索。
- 后续首批填充锚点包括：9 系统 / 101 功能安全需求、[../../../data/STM_GENERATION_DATASET_ANALYSIS.md](../../../data/STM_GENERATION_DATASET_ANALYSIS.md) 中分析的公开 NL→STM generation 数据集、[../../../sources/](../../../sources/) 真实控制系统 NL 池，以及旧 [../../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md](../../../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md) 中的 `sources/` T0+🟢 线索。

## 2. 阅读顺序

1. 先读本 [README.md](./README.md)：确认定位和边界。
2. 再读 [GUIDE.md](./GUIDE.md)：确认收录 / 排除 / 分级 / 更新规则。
3. 再读 [SUMMARY.md](./SUMMARY.md)：确认当前总账、字段与首批锚点。
4. 后续若有单独 dataset 目录，再进入其 `dataset_card.md -> source_refs.md -> samples/`。

## 3. 单条目结构

每个 dataset 条目后续建议至少包含：

```text
<dataset-slug>/
├── dataset_card.md
├── source_refs.md
└── samples/        # 仅存可公开或可追溯样本；敏感或许可不明数据只存说明、哈希和本地路径指针
```

当前 PR 不创建任何 `<dataset-slug>/` 子目录；具体条目填充留给后续独立 PR。

## 4. 与上游文库的关系

- [../seed_library/](../seed_library/) 负责 `NL -> STM_0` 的 seed 方法 / 来源。
- [../repair_baselines/](../repair_baselines/) 负责 `STM_0 -> STM_k / Better STM` 的修正近邻。
- 本库只负责纯 NL 数据源；不把只有 NL 的对象提前当 seed。
- 若某个 NL 来源后续完成 `STM_0` 构造，应在本库 `SUMMARY.md` 的 `seed_library crosslink` 字段记录对应 seed slug，并在 seed library 反向回链。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 23:20:00 | 初始化 NL-datasets 三件套脚手架，冻结“只有 NL 不等于 seed”、三类文库分工、首批锚点与后续单条目结构。 |
