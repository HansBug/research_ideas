# Results Guide

## 1. 职责

本目录只存放运行产物。

典型产物包括：

1. `predictions.parquet`
2. `summary.json`
3. 评审输出 parquet/json
4. 对齐实验缓存与统计

## 2. 组织原则

结果应按任务或 baseline 分目录管理，不应把所有 parquet/json 平铺在 `results/` 根层。

## 3. 维护原则

### 自动生成优先

优先通过脚本生成，不手工维护结果文件。

### 分层清晰

如果某项结果属于某个专题模块，应作为该 baseline 或模块的子目录结果，而不是放到上层混在一起。

例如：

- `results/ttool/expert_alignment/...`
- `results/structure_event/expert_review/...`

## 4. 关联入口

- 统一调度见 [../run_all.py](../run_all.py)
- 评审入口见 [../run_expert_review.py](../run_expert_review.py)
- 对齐实验见 [../align_ttool_expert_review.py](../align_ttool_expert_review.py)
