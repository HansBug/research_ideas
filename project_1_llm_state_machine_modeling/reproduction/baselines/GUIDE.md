# Baselines Guide

## 1. 目录职责

本目录只放 baseline 级复现实现，不放：

1. 生成结果
2. 设计文档
3. 大量数据文件
4. 与 baseline 无关的通用评审模块

## 2. 文件命名

baseline 实现默认采用：

- `baseline_<name>.py`

这样可以让入口角色一眼可见。

## 3. 新增 baseline 时

建议顺序：

1. 先在本目录新增 `baseline_<name>.py`
2. 再在 [`../README.md`](../README.md) 与 [`../REPRODUCTION_REPORT.md`](../REPRODUCTION_REPORT.md) 中补充说明
3. 保证结果仍统一落到 [`../results/`](../results/)

## 4. 依赖关系

baseline 文件可以依赖：

- [`../llm_client.py`](../llm_client.py)
- [`../config.py`](../config.py)
- [`../io_utils.py`](../io_utils.py)
- [`../eval_utils.py`](../eval_utils.py)

但不应把 baseline 特定逻辑偷偷塞回这些公共模块里，导致职责变混。
