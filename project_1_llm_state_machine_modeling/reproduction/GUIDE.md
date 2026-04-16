# Reproduction Guide

本文档定义 `reproduction/` 工作区的组织规则。

## 1. 目录职责

`reproduction/` 根目录只保留四类内容：

1. workspace 级入口文件
2. workspace 级说明文档
3. 一级功能子目录
4. 对整个复现工作区都成立的公共模块

不应再把某个专题模块的大量设计文档长期堆在根目录。

## 2. 文档放置规则

### 2.1 根目录文档

根目录只保留与整个复现工作区直接相关的文档，例如：

- `README.md`
- `GUIDE.md`
- `REPRODUCTION_REPORT.md`

### 2.2 模块文档

某个专题模块的设计文档必须放在模块自己的子目录内。

例如：

- `expert_review` 的设计文档统一放在 [`expert_review/designs/`](./expert_review/designs/)

### 2.3 版本化设计文档

设计文档若存在多版本，必须采用版本子目录，而不是继续平铺。

例如：

- [`expert_review/designs/v0/`](./expert_review/designs/v0/)
- [`expert_review/designs/v1/`](./expert_review/designs/v1/)

## 3. 一级子目录要求

`reproduction/` 下的一级专题目录默认都应具备：

1. `README.md`
2. `GUIDE.md`

当前应至少满足：

- [`baselines/README.md`](./baselines/README.md) / [`baselines/GUIDE.md`](./baselines/GUIDE.md)
- [`data/README.md`](./data/README.md) / [`data/GUIDE.md`](./data/GUIDE.md)
- [`results/README.md`](./results/README.md) / [`results/GUIDE.md`](./results/GUIDE.md)
- [`expert_review/README.md`](./expert_review/README.md) / [`expert_review/GUIDE.md`](./expert_review/GUIDE.md)

## 4. 新文件应放在哪里

### 4.1 baseline 运行代码

放在 [`baselines/`](./baselines/)

### 4.2 专题 agent 代码

放在对应模块目录，例如 [`expert_review/`](./expert_review/)

### 4.3 运行数据与中间资产

放在 [`data/`](./data/)

### 4.4 运行结果

放在 [`results/`](./results/)

### 4.5 设计文档

放在对应模块的 `designs/` 下，并用版本子目录组织。

## 5. 保持路径干净的具体标准

判断一个文件是否不该留在 `reproduction/` 根目录，可以用下面的规则：

1. 它是否只服务于某个单独模块，而不是整个 workspace。
2. 它是否属于某个专题的设计演化，而不是 workspace 级入口说明。
3. 它是否已经多到需要版本化收纳。

如果答案是“是”，就不应继续平铺在根目录。

## 6. 代码兼容性原则

本工作区重构组织结构时，优先遵循：

1. 不随意改变可运行代码路径
2. 不破坏现有 CLI 入口
3. 不破坏现有导入路径
4. 文档迁移优先通过修正链接完成，而不是靠保留旧路径副本

## 7. 推荐阅读顺序

1. [README.md](./README.md)
2. [REPRODUCTION_REPORT.md](./REPRODUCTION_REPORT.md)
3. 目标子目录的 `README.md`
4. 目标子目录的 `GUIDE.md`
5. 该子目录下更深层级的版本化文档
