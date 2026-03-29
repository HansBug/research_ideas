# UPPAAL 应用文库总账

本文件是 `open_explore/uppaal_apps/` 论文集的总账，用于记录当前已经正式入账的 `UPPAAL` 应用与案例论文、分类分布、更新状态和失败/阻塞历史。

## 文档定位与使用方式

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，了解本论文集定位和与 [uppaal_tech/README.md](../uppaal_tech/README.md) 的边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、回填和一致性检查规范。
3. 再使用本文件查看当前统计、分类、论文表和失败记录。

## 收录边界回顾

1. 这里只收录 `UPPAAL` 被用于具体系统、协议、软件或工业对象上的应用工作。
2. 主贡献是 `UPPAAL` 本体技术的论文，不在这里入账，应进入 [uppaal_tech/README.md](../uppaal_tech/README.md)。
3. 只是在正文中顺带提一下 `UPPAAL` 的条目，不应正式入账。

## 检索关键词簇

### 当前推荐关键词簇

- `UPPAAL + case study + protocol/controller/embedded system/industrial system`
- `UPPAAL + verification/testing/scheduling + 具体系统名`
- `UPPAAL + official case study`

### 已观察到的高命中特征

- 题目或摘要直接出现 `case study`、`industrial`、`protocol`、`controller`
- 官方案例页或官方 tutorial 能反向追到正式论文

### 已观察到的低命中特征

- 只有工具名，没有应用对象
- 只有应用对象，没有 `UPPAAL`

### 检索倾向调整

- 当前优先把边界和总账骨架建好，暂不急于机械扩张条目。
- 后续新增前先做“技术/应用”分流，避免与 `uppaal_tech/` 重叠。

## 当前收录统计

- 已收录顶层条目：**0** 篇
- 本轮新增顶层条目：**0** 篇
- 本轮未纳入/待补证条目：**0** 条
- 已记录环境级阻塞：**0** 条

## 应用分类

当前仍处于初始化阶段，后续建议至少按以下几类维护：

1. 协议与通信系统
2. 控制器与嵌入式系统
3. 工业系统与工程案例
4. 软件系统与其他综合案例

## 论文清单

当前尚无正式入账条目。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal_apps/`，建立 `README.md`、`GUIDE.md`、`SUMMARY.md` 三个核心文件 | 先把应用文库与 `uppaal_tech/` 拆开，固定边界、入口和总账骨架 | 先解决结构拆分，后续再正式扩充应用条目 |

## 失败与阻塞记录

当前无记录。
