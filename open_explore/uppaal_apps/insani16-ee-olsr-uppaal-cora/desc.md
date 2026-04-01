问题一句话：本文验证的是 `EE-OLSR` 自组织网络路由协议，核心问题是该协议在考虑能耗成本后，是否真的比原始 `OLSR` 更节能，且这种节能在什么阶段成立。
方法一句话：作者把 `EE-OLSR` 建模为 `Linearly Priced Timed Automata`，再用 `UPPAAL CORA` 与 `WCTL` 公式检查邻居发现、两跳邻居建立、拓扑发现、最优路由、包投递和 energy-efficient 等性质。
验证收获一句话：验证结果显示多条协议性质在给定时间界内均满足，但“更节能”这一性质只在实际数据包传输发生时成立；当节点仅处理控制消息时，`EE-OLSR` 与原协议的能耗相同。

## 基本信息

- 标题：Pemodelan dan Verifikasi Formal Protokol EE-OLSR dengan UPPAAL CORA
- 中文标题：使用 `UPPAAL CORA` 对 `EE-OLSR` 协议进行形式化建模与验证
- 作者：Rachmat Wahid Saleh Insani、M. Reza M.I Pulungan
- 单位：Universitas Gadjah Mada
- 发表：IJCCS (Indonesian Journal of Computing and Cybernetics Systems)，2016
- DOI：`10.22146/ijccs.11192`
- 链接：[DOI](https://doi.org/10.22146/ijccs.11192)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：`MANET` 场景中的 `EE-OLSR` 路由协议
- UPPAAL线：`UPPAAL CORA`
- 代码/模型/仓库获取方式：原文未提供 `UPPAAL CORA` 模型文件或查询脚本。
- 案例/数据获取方式：案例基于 `OLSR/EE-OLSR` 协议机制，需按正文中的 `PTA/LPTA` 结构和性质表重建。

## 简报

本文非常明确地把 `EE-OLSR` 作为一个需要验证的具体协议对象，而不是只做仿真。作者关注的是：`EE-OLSR` 通过在 `MPR` 选择和路由选择中引入能量因素，是否能在不牺牲协议功能的前提下实现 energy-efficient。

- 系统：`MANET` 中的 `EE-OLSR` 路由协议。
- 特点：主动式、基于 link-state、显式考虑电池能量和 `MPR` 选择。
- 规模：协议流程被拆成多个阶段，正文给出 `2000-7000 ms` 的性质验证时间界。
- 模型：`Linearly Priced Timed Automata`。
- 性质：邻居发现、两跳邻居构建、拓扑发现、最优路由、包投递、能量效率。
- 方法：`UPPAAL CORA` + `WCTL`。
- 结果：全部阶段性质满足，但能效优势只在数据包传输阶段显现。

`EE-OLSR 协议机制 -> LPTA / PTA 模型 -> WCTL 性质 -> UPPAAL CORA 自动验证`

## 论文定位

这是一篇标准的 `🛰️ + 🌐` 协议应用论文。协议对象、模型类型、性质和结论都很清楚，也确实使用了 `UPPAAL CORA` 做自动验证，因此虽然篇幅不长，仍然是比较干净的应用条目。

## 验证对象与问题背景

### 系统与场景

对象是 `MANET` 中的 `OLSR` 及其节能变体 `EE-OLSR`。在移动自组网里，节点靠电池供电，因此能量效率直接影响网络寿命。

### 系统组成与运行机制

`OLSR` 是 proactive、table-driven 协议，基于 link-state algorithm。`EE-OLSR` 的关键变化在于：

1. 在 `MPR` 选择中加入 energy-aware metric；
2. 在路由选择中考虑能量因素；
3. 目标是在不明显降低性能的前提下延长网络寿命。

### 验证边界

论文验证的是**协议层行为与能耗成本**，不是无线物理层或大规模网络仿真。

### 核心问题

1. 传统仿真和测试难以保证不存在 subtle error。
2. 需要自动化方法验证协议逻辑和能耗性质。
3. “更节能”不能只靠口头声称，必须写成形式性质。

## 模型与形式化建模

### 模型形式

论文使用 `Priced Timed Automata` / `Linearly Priced Timed Automata`，使：

1. `location` 带有 cost rate；
2. `edge` 带有执行 cost；
3. 可以直接表达能量消耗。

### 关键对象

从正文可以确定作者至少建模了：

1. `OLSR` / `EE-OLSR` 节点行为；
2. 消息处理流程；
3. 消息队列；
4. `HELLO` 与 `TC` 控制消息处理；
5. `MPR` 选择和转发逻辑。

### 模型边界

论文把协议核心阶段拆开验证，重点不在大规模节点数，而在协议逻辑和 cost 是否满足设计意图。

## 验证目标与性质

### 待验证问题

表 1 给出的主要性质包括：

1. `Neighbor Detection`
2. `Populating 2 Hop Neighbor`
3. `Topology Discovery`
4. `Optimal Route`
5. `Packet Delivery`
6. `Energy Efficient`

### 性质类型

1. 协议功能正确性。
2. 可达性/阶段完成性。
3. 成本与能效性质。

### 查询表达

论文将性质写入 `Weighted Computation Tree Logic (WCTL)`，并交给 `UPPAAL CORA` 自动验证。原文没有像英文会议论文那样逐条展开公式文本，但明确说明使用 `WCTL` 语法表达。

### 时间界

表 1 同时给出各性质的检查时界：

1. `2000 ms`：Neighbor Detection
2. `4000 ms`：Populating 2 Hop Neighbor
3. `5000 ms`：Topology Discovery
4. `7000 ms`：Optimal Route / Packet Delivery / Energy Efficient

## 核心方法与验证流程

1. 先用 `PTA/LPTA` 形式化协议。
2. 对 `HELLO` 和 `TC` 等控制消息处理过程单独建模。
3. 将功能与能量性质写成 `WCTL`。
4. 用 `UPPAAL CORA` 自动检验是否满足。

## 案例与结果

### 主要结果

论文表 1 给出 `6` 条核心验证结果，全部标记为 `Satisfy`。

### 关键解释

不过作者在结论中特别指出：

1. `EE-OLSR` 的 energy-efficient 性质在“有数据包传输流量”时成立；
2. 如果节点只是在处理协议控制消息，则 `EE-OLSR` 与普通 `OLSR` 的能耗相同；
3. 因而节能收益主要来自实际转发业务流，而不是控制消息本身。

这条结论很重要，因为它避免了把“协议全程都更节能”说得过满。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究有价值，因为它展示了如何把“功能性质 + 成本性质”同时压进同一套协议模型。

### 可借鉴之处

1. 对协议不同阶段做分组性质验证。
2. 用 `priced timed automata` 把 energy cost 并入模型。
3. 对“节能”这类定量需求做边界化解释，而不是只给总标签。

### 存在的不足与改进空间

1. 正文没有公开完整公式和模型文件。
2. 案例规模较小，偏协议核心机制。
3. 结论主要针对给定时间界和所建模型，不宜直接外推到大规模网络。

### 对本研究的启发

对博士研究中的“性质模型生成”来说，这篇论文说明：像能耗、成本、资源消耗这类要求完全可以和功能正确性并列，成为一组正式性质簇。

## 重要的相关工作

### 1. `OLSR` 协议研究

- 论文把 `EE-OLSR` 明确定位为传统 `OLSR` 的节能变体。

### 2. `UPPAAL CORA`

- `UPPAAL CORA` 在此承担核心作用，用于分析 cost-optimal / priced timed automata 模型。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文正文公开，但未给出 `UPPAAL CORA` 模型与 `WCTL` 查询文件下载入口。
- 获取方式/链接：[DOI](https://doi.org/10.22146/ijccs.11192)
- 对后续复用的现实影响：适合作为 `UPPAAL CORA` 协议能耗验证模板，但复跑仍需手工重建模型和性质。
