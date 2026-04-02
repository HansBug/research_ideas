问题一句话：本文验证的是 SNCF `PSEEL` 电气安装的 `PLC` 程序，核心问题是如何把人工 recipe book 测试自动化，并在工厂测试前离线发现程序与场景规则之间的不一致。
方法一句话：作者把设备、`PLC` 扫描周期、定时器和 recipe book 场景都编码成 `UPPAAL` 模型，让模型检查器自动遍历测试步骤并定位不满足预期效果的指令。
验证收获一句话：结果表明 recipe book 可以在几十毫秒内被自动浏览，并能快速定位修改版程序中两处预期错误；论文还指出现有 recipe book 之外仍可能存在通向危险状态的遗漏场景。

## 基本信息

- 标题：Formal Verification for Validation of `PSEEL`'s `PLC` Program
- 中文标题：用形式化验证进行 `PSEEL` `PLC` 程序确认
- 作者：Mohamed Niang、Alexandre Philippot、François Gellot、Raphaël Coupat、Bernard Riera、Sébastien Lefebvre
- 单位：CReSTIC，University of Reims Champagne Ardenne；SNCF
- 发表：`14th International Conference on Informatics in Control, Automation and Robotics (ICINCO 2017)`
- DOI：`10.5220/0006418705670574`
- 链接：[DOI](https://doi.org/10.5220/0006418705670574)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：SNCF `PSEEL` 电气安装中的 `PLC` 程序与 recipe book 验证流程
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文未公开 `UPPAAL` 工程、`Odil` 生成器或 `STRATON` 程序文件。
- 案例/数据获取方式：案例依赖 SNCF 的 `PSEEL` 结构、`PLC` 程序和 recipe book，均来自工业项目。

## 简报

本文非常像“工业验证流程自动化”案例。SNCF 原本靠系统工程师在工厂里逐条执行 recipe book 场景，既慢又容易漏。作者的目标是把这一套过程前移到办公室里，通过 `UPPAAL` 离线完成。

- 系统：`PSEEL` 电气安装的 `PLC` 程序和对应 recipe book。
- 特点：工业真实对象、`PLC` 扫描周期显式建模、recipe book 逐步执行、还额外讨论危险状态覆盖不足。
- 规模：模型包含开关、断路器、`PLC` cycle、`TON` 定时器与 recipe book 状态机；扫描周期约 `20 ms`。
- 模型：设备行为、`PLC` 循环和测试场景都被建成同步 automata。
- 性质：recipe book 指令是否得到预期效果、步骤超时、危险状态是否可达。
- 方法：先自动执行全部场景，再利用 counterexample 定位不满足指令；后续进一步搜索危险状态。
- 结果：recipe book 在几十毫秒内即可自动遍历；修改版程序中的两个人为错误都能被快速诊断。

`工业电气设备 + PLC 扫描周期 + recipe book 场景 -> UPPAAL 同步模型 -> 自动场景遍历 -> 错误定位与危险状态检查`

## 论文定位

这是一个很有代表性的 `🎛️ + 🚦` 工业铁路控制案例。重点不是一般 PLC 语义，而是“如何把铁路现场确认流程形式化并前移到离线验证阶段”。

## 验证对象与问题背景

### 系统与场景

对象是 SNCF `PSEEL` 电气安装项目中的 `PLC` 程序。该程序必须保证电气安装行为正确，传统做法是在工厂测试阶段人工执行 recipe book 场景。

### 系统组成与运行机制

论文给出了多个设备模型，如开关、断路器、`TON` 定时器和 `PLC` 周期 automaton。recipe book 被翻译为顺序功能图风格的状态机，并与系统模型同步执行。

### 验证边界

验证对象是 `PSEEL` 设备逻辑、`PLC` 程序和 recipe book 测试流程，不覆盖全部接线错误或现场硬件物理实现。

### 核心问题

1. 人工 recipe book 测试太慢，且容易漏测。
2. 现有方法主要验证功能符合性，难以系统性覆盖危险状态。
3. 希望在工厂前就离线发现程序问题，并给系统工程师明确诊断线索。

## 模型与形式化建模

### 抽象对象

系统被拆成设备 automata、`PLC` cycle automaton、定时器 automata 和 recipe book automaton。`PLC` 周期被显式表示为循环结构，时长约 `20 ms`。

### 建模形式

论文使用标准 `UPPAAL` timed automata。定时器 `TON` 用启动输入、预置时间和超时输出建模；recipe book 每个步骤也配一个 elapsed-time 计时器。

### 关键抽象与取舍

1. recipe book 被结构化为可执行状态机，而不再是人工文本。
2. `PLC` 扫描周期中的输入更新、计时器演化和输出刷新被分步表示。
3. 后续危险状态分析依赖专家先定义危险状态集合。

## 验证目标与性质

### 待验证问题

论文至少考虑两类查询：

1. recipe book 步骤是否都在预期时间内得到满足。
2. 是否存在路径进入危险状态。

### 查询表达

文中代表性查询包括：

1. `E<> time_step.timeout`
2. `E<> cycle.fin and TON_fault.timeout`

前者用于发现某条 recipe book 指令迟迟得不到满足；后者用于寻找危险状态相关路径。

### 性质类型

这些性质覆盖有界响应、场景符合性和危险状态可达性。对工程上而言，就是“场景要求是否实现”和“是否仍存在漏掉的危险场景”。

## 核心方法与验证流程

1. 建立 `PSEEL` 设备与 `PLC` 周期模型。
2. 把 recipe book 自动翻译为 `UPPAAL` 状态机。
3. 执行所有场景，检查是否有步骤超时或效果不符。
4. 对错误版本程序查看 counterexample，定位具体步骤和转移条件。
5. 在 recipe book 之外，再搜索危险状态的可达路径，评估测试覆盖不足问题。

## 案例与结果

论文结果很工程化：

1. 对已通过工厂测试的原程序，recipe book 场景自动仿真与人工结论一致。
2. 对刻意删掉条件的修改版程序，`UPPAAL` 能指出 overcurrent 测试中断路器没有打开，以及过流未消失时断路器却错误闭合。
3. recipe book of transformer group 可在几十毫秒内自动浏览，而人工方法至少需要一周。
4. 作者进一步指出：即便 recipe book 全部满足，系统仍可能存在未覆盖的危险状态。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究非常相关，因为它体现了“模型-场景-性质-反例-补测”的完整闭环，而且对象是真实铁路工业系统。

### 可借鉴之处

1. 把测试脚本 recipe book 形式化成可执行状态机。
2. 把 `PLC` 扫描周期和定时器语义显式写入模型。
3. 同时关注“现有测试是否通过”和“是否还有漏掉的危险状态”。

### 存在的不足与改进空间

完整模型和工业程序未公开；危险状态集合仍需依赖领域专家给定。

### 对本研究的启发

对博士研究第二、第三主题特别有启发：验证场景不必完全从零生成，很多时候可以从现有测试脚本结构化提炼，再补足危险状态覆盖。

## 案例、模型与数据公开情况

- 可获取性判断：🔒 难以取得
- 判断依据：论文公开，但 `PSEEL` 结构、`PLC` 源程序、recipe book 和自动生成工具都属于 SNCF 项目资产，未公开下载。
- 获取方式/链接：[DOI](https://doi.org/10.5220/0006418705670574)；[公开 PDF](https://www.scitepress.org/papers/2017/64187/64187.pdf)
- 对后续复用的现实影响：非常适合作为“工业 `PLC` + recipe book 自动验证”方法样本，但真实项目工件难以直接获取。
