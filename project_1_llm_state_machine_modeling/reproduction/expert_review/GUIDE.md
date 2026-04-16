# Expert Review Guide

## 1. 目录职责

本目录只放 `expert_review` 模块相关内容：

1. 可运行代码
2. 模块级测试
3. 模块级设计文档

不应把：

1. workspace 级说明
2. 其他 baseline 的实现
3. 运行结果 parquet/json

继续混入本目录。

## 2. 文档组织规则

设计文档统一放到：

- [`designs/`](./designs/)

并继续按版本子目录组织：

- [`designs/v0/`](./designs/v0/)
- [`designs/v1/`](./designs/v1/)

不要再把新的 `EXPERT_*.md` 平铺回 `reproduction/` 根目录。

## 3. 代码组织规则

当前代码入口仍保留在本目录根层，原因是：

1. 现有导入路径与 CLI 已经依赖这一结构
2. 本轮目标是先把文档与导航结构重构干净
3. 代码层更大规模的模块化拆分留给下一轮

## 4. 外部兼容要求

后续即使重构实现，也优先保持：

1. `ExpertReviewRequest`
2. `ExpertReviewResult`
3. `review_artifacts()`
4. `review_model()`
5. `python -m expert_review`

## 5. 测试入口

当前最直接的模块级验证见：

- [test_expert_review.py](./test_expert_review.py)
