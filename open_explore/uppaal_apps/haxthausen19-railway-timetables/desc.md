问题一句话：本文验证的是铁路时刻表本身，核心问题是给定线路拓扑、站场/区间容量、最小运行时间和 headway 约束后，列车按表运行是否会进入非法状态。
方法一句话：作者构建可重配置 `UPPAAL` 模型，把铁路网络、时刻表和运行约束参数化输入到 train / initializer 等模板中，再用统一查询检查容量、headway 和时刻表合法性。
验证收获一句话：论文在丹麦 `Nørumbanen` 真实案例上成功验证了 `12` 列车、`9` 车站的时刻表，并能通过故意制造非法时刻表快速定位容量冲突。

## 基本信息

- 标题：Formal Verification of Railway Timetables - Using the UPPAAL Model Checker
- 中文标题：使用 `UPPAAL` 模型检查器形式化验证铁路时刻表
- 作者：Anne E. Haxthausen、Kristian Hede
- 单位：Technical University of Denmark
- 发表：`From Software Engineering to Formal Methods and Tools, and Back`，2019
- DOI：`10.1007/978-3-030-30985-5_25`
- 链接：[DOI](https://doi.org/10.1007/978-3-030-30985-5_25)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：铁路网络上的列车时刻表与容量/headway 约束
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文 PDF 公开，但未给出独立模型仓库。
- 案例/数据获取方式：正文给出可重配置的线路、车站、区间与 timetable 参数；真实案例来自丹麦 `Nørumbanen`。

## 简报

这篇论文验证的对象不是单个 interlocking 或车载控制器，而是铁路时刻表本身。作者希望证明“按这张表运行”不会导致非法铁路状态，因此把 timetable、线路容量和运行约束一起放进 `UPPAAL`。

- 系统：铁路网络上的 timetable + trains + station/open-line 约束。
- 特点：时刻表驱动、容量与 headway 共同约束、模型可重配置。
- 规模：真实案例包含 `12` 列车、`9` 车站。
- 模型：`Train` 与 `Initialiser` 模板，加全局配置表描述 station/open line 参数。
- 性质：站场容量、区间容量、站场 headway、区间 headway、非法状态不可达。
- 方法：将 timetable 参数装入可配置模型，再用查询检查运行合法性。
- 结果：真实案例在 `UPPAAL` 中可在 `4` 分钟内验证完成；降低站场容量等非法修改会触发诊断反例。

`铁路网络与时刻表 -> 可配置 UPPAAL 模型 -> 容量/headway/非法状态查询 -> 合法 timetable 证明或非法案例反例`

## 论文定位

这是很纯粹的 `⏱️ + 🚦` 条目。论文主线是时刻表验证应用，而不是 `UPPAAL` 技术本体，适合作为“铁路运行规则如何进入形式模型”的代表案例。

## 验证对象与问题背景

### 系统与场景

被验证对象是铁路时刻表。背景是时刻表通常通过经验和仿真设计，但要严格保证容量、间隔和运行安全约束，形式化方法能提供更强的静态保证。

### 系统组成与运行机制

模型里每列车按照时刻表驱动，在站场和区间之间运行。系统同时记录：

1. station capacity
2. open line capacity
3. minimum running time
4. station / line headway

### 验证边界

论文主要验证 timetable 的运行合法性，不展开 interlocking、信号设备实现或复杂乘客行为。

### 核心问题

1. timetable 是否会导致某站或区间超容量。
2. 两列车之间的最小间隔是否总被满足。
3. 非法 timetable 是否能被快速诊断。

## 模型与形式化建模

### 抽象对象

核心抽象是：

1. 列车实例
2. 站场与区间表
3. timetable 条目
4. 容量与 headway 参数

### 建模形式

模型采用可重配置 `UPPAAL` 结构：

1. `Train` 模板负责列车运行。
2. `Initialiser` 负责根据配置创建初始场景。
3. 配置表给出 station/open line 的容量、headway 和运行时间。

### 关键抽象与取舍

1. 重点保留时刻表合法性所需参数，而非细粒度设备实现。
2. 非法状态通过 error location 显式表示，便于诊断。
3. 同一模型既可跑合法 timetable，也可故意注入非法参数做反例测试。

## 验证目标与性质

### 待验证问题

论文把性质明确分成四类：

1. station capacity
2. open line capacity
3. station headway
4. open line headway

### 性质类型

这些性质属于安全和有界时序约束。

### 查询表达

代表性查询包括：

1. `A[] forall(i: t_id) not Train(i).ERROR_S`
2. 与区间/站场容量、headway 对应的一组错误位置不可达查询

## 核心方法与验证流程

1. 将铁路网络和时刻表编码为配置数据。
2. 生成对应 `UPPAAL` 实例模型。
3. 逐项检查容量与 headway 约束。
4. 对非法 timetable 运行失败查询，获取诊断轨迹。

## 案例与结果

论文给出的结果相当具体：

1. 真实 `Nørumbanen` 时刻表案例覆盖 `12` 列车和 `9` 车站。
2. 使用 `UPPAAL` 符号模型检查器可在不到 `4` 分钟内完成验证。
3. 通过把某站容量从 `2` 改到 `1` 之类的非法修改，模型会触发对应容量冲突反例。

这说明模型既能证明合法 timetable，也能作为诊断工具定位不合法配置。

## 与本研究的关系

### 相关性分析

它展示了如何把运行规则、结构参数和时间约束组织成可重配置状态机模型，这和博士研究中的“需求到模型”转换非常贴近。

### 可借鉴之处

1. 将场景参数与模型骨架解耦。
2. 把多类约束统一组织成 error-state 查询。
3. 允许合法与非法场景共用同一模型做诊断。

### 存在的不足与改进空间

论文主要关注 timetable 约束，不处理更细的 interlocking 或列车控制设备实现。

### 对本研究的启发

这篇论文说明，对大型控制系统不一定要先从完整控制器入手，也可以先验证“约束化运行方案”本身是否自洽。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文可公开获取，但未见独立 timetable 数据包或 `UPPAAL` 模型仓库。
- 获取方式/链接：[DOI](https://doi.org/10.1007/978-3-030-30985-5_25)；[公开 PDF](https://backend.orbit.dtu.dk/ws/files/197983400/main_timetable_mc2019.pdf)
- 对后续复用的现实影响：适合复用其 timetable 参数化建模方式，但若要复跑仍需按论文重建配置数据。
