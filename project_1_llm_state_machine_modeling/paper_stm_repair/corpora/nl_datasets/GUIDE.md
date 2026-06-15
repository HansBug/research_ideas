# nl_datasets/GUIDE.md

## 0. 定位

本文件定义 `nl_datasets/` 的收录与维护规则。其目标是稳定管理控制系统纯 NL 输入来源，为后续构造 `<NL, STM_0>` 提供入口。

## 1. 硬边界

1. **NL 不等于 seed**：只有 NL 但没有 `STM_0` 生成关系的对象，一律只算 NL-dataset。
2. **不混 repair**：任何 repair / completion / refinement / feedback 任务都不属于本库。
3. **不抢 baseline**：seed / repair baselines 的对象不能挪到这里混记。
4. **不维护施工真源**：PR / issue 的动态进度只写 GitHub body/comment。
5. **不做大规模外部检索作为本 PR 的验收前提**：本 PR 只冻结脚手架、字段和入口纪律。

## 2. 收录对象

| 类别 | 收录口径 |
|---|---|
| 控制系统需求 | 功能安全需求、系统需求、用例、场景、标准片段 |
| 旧 Path-1 线索 | 之前收集过但尚未生成 seed 的 NL 候选 |
| 弱 seed 入口 | 适合弱模型 / 弱 prompt / 学生人工建模的 NL 来源 |
| 历史来源回链 | 已知 NL 来源但生成关系尚未闭合的对象 |

## 3. 排除对象

| 排除对象 | 原因 |
|---|---|
| 已证明 `STM_0` 由同一 NL 生成的对象 | 应进入 seed library |
| repair / completion 论文 | 应进入 repair baselines |
| 非控制系统或无法稳定映射到 STM family 的文本 | 不适合作为本论文实验来源 |

## 4. `SUMMARY.md` 字段纪律

至少保留以下字段组：

- `dataset_id`
- NL 类型
- 控制系统领域
- 规模
- 公开与许可
- seed 构造潜力
- 与已有 STM 关系
- 实验角色
- 证据指针

## 5. 更新规则

- 只要条目仍然只有 NL，就继续留在 NL-datasets。
- 只有当 `STM_0` 生成关系被明确证明，才 crosslink 到 seed library。
- 单条目证据必须可点击、可追溯。
