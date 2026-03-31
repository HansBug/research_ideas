问题一句话：本文验证的是多智能体系统中的知识与承诺状态，核心问题是 `NetBill` 电子交易协议里客户和商家对 `PAY/DELIVER` 承诺的履行与认知是否能保持一致，并最终回到正常交易闭环。
方法一句话：作者先用轻量 actor 模型描述 customer、merchant 和消息对象，再把 actors 归约为 `UPPAAL` 模板，结合经典查询与 `SMC` 做定性和定量分析。
验证收获一句话：论文证明 `NetBill` 模型无死锁，支付与交付承诺的履行最终会被双方共同知晓；在 `SMC` 下，这些关键事件出现的概率区间也保持在较高水平。

## 基本信息

- 标题：Model Checking Knowledge And Commitments In Multi-Agent Systems Using Actors And UPPAAL
- 中文标题：使用 actors 与 `UPPAAL` 对多智能体系统中的知识和承诺进行模型检查
- 作者：Christian Nigro、Libero Nigro、Paolo F. Sciammarella
- 单位：University of Calabria, DIMES, Software Engineering Laboratory
- 发表：ECMS 2018 Proceedings，2018
- DOI：`10.7148/2018-0136`
- 链接：[DOI](https://doi.org/10.7148/2018-0136)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：`NetBill` 电子交易协议中的 customer/merchant 交互与承诺知识状态
- UPPAAL线：`UPPAAL SMC`
- 代码/模型/仓库获取方式：原文未提供独立 actor 模型或 `UPPAAL` 工程仓库。
- 案例/数据获取方式：案例来自 `NetBill` 协议与作者构造的 actor 运行语义，无独立数据集。

## 简报

本文关注的不是传统消息协议安全，而是多智能体系统里“谁知道某项承诺已经成立或履行”。作者用 `NetBill` 电商协议做样本，把 customer 和 merchant 的承诺知识状态通过 actor 模型显式化，再归约到 `UPPAAL` 检查。

- 系统：客户与商家围绕报价、接受、支付、交付、退款等步骤形成的 `NetBill` 会话。
- 特点：显式区分 commitment 状态与 knowledge 状态，并允许非确定性交互。
- 规模：最多可对 `4` 个 agents 做穷尽模型检查；更大规模时转用 `SMC`。
- 模型：`Main`、`Customer`、`Merchant`、`Message`、`TimedMessage` 等 `UPPAAL` 模板。
- 性质：无死锁、承诺最终履行、双方最终知道承诺已履行、状态最终回到初始。
- 方法：actor 到 `UPPAAL` 的归约 + `TCTL` 查询 + `SMC` 概率估计。
- 结果：`NetBill` 模型在文中实验设置下被判定为正确，关键知识/承诺性质均满足。

`NetBill 会话与承诺语义 -> actor 模型 -> actors/messages 归约为 UPPAAL 自动机 -> 承诺与知识查询 -> 正确性与概率分析`

## 论文定位

本文属于 `🧩 + 🌐` 的业务协议/多智能体流程案例。它的核心不在网络传输，而在承诺与知识状态的演化，因此更接近“业务交互状态机”的验证样本。

## 验证对象与问题背景

### 系统与场景

`NetBill` 是用于在线购买和交付加密软件商品的协议。客户与商家之间围绕报价、接受、支付、交付和退款展开交互，并在过程中形成 `PAY` 与 `DELIVER` 两类承诺。

### 系统组成与运行机制

论文中的关键角色包括：

1. `Customer`
2. `Merchant`
3. 异步消息对象 `Message/TimedMessage`
4. 用于全局初始化的 `Main`

客户先请求报价，接受后形成支付意向并通过自发消息 `Commit` 继续推进；商家则根据接收到的 `Accept/Payment` 等消息改变交付与退款行为。

### 验证边界

本文关注的是承诺和知识状态的行为级正确性，不覆盖底层支付系统或真实加密算法实现。

### 核心问题

作者希望回答：

1. customer 支付后，merchant 是否最终知道 `PAY` 已履行
2. merchant 承诺交付后，双方是否最终知道 `DELIVER` 已履行
3. 协议是否会死锁或停在中间状态
4. 当状态空间膨胀时，能否改用 `SMC` 得到概率化结论

## 模型与形式化建模

### 抽象对象

论文把 actors 与 messages 都降为 `UPPAAL` 模板：

1. `Customer`、`Merchant` 对应 actor 行为机
2. `Message`、`TimedMessage` 对应异步消息实例
3. 承诺知识状态记录在 `k[cid][aid]` 等全局结构中

### 建模形式

异步消息先被调度再派发；承诺 `PAY/DELIVER` 的状态通过 `C/Fu/Fail` 等函数更新；知识状态通过 `K(aid, cid)` 查询读取。

### 关键抽象与取舍

1. 使用静态数量的消息实例循环复用，以兼容穷尽模型检查。
2. 保留异步消息的非确定性和定时消息的 `after` 语义。
3. 在 `SMC` 中把非确定性交互视为概率化选择。

## 验证目标与性质

### 待验证问题

论文主要检查：

1. 无死锁
2. customer 付款后，双方最终都知道 `PAY` 已 fulfilled
3. merchant 交付后，双方最终都知道 `DELIVER` 已 fulfilled
4. customer 和 merchant 最终都能回到初始状态

### 查询表达

代表性查询包括：

1. `A[] ! deadlock`
2. `Customer(0).cs==s5 --> K(0,PAY)==Fulfilled && K(CUS,PAY)==Fulfilled`
3. `Merchant(CUS).cs==s6 --> K(CUS,DELIVER)==Fulfilled && K(0,DELIVER)==Fulfilled`
4. `A<> now>0 && Customer(0).cs==s0`
5. `Pr(<>[0,100] (Customer(0).cs!=s0 && (<>[0,2] Customer(0).cs==s0)))`
6. `Pr[<=1000] (<> Customer(0).cs==s5 && K(0,PAY)==Fulfilled)`

## 核心方法与验证流程

1. 先用 actor 模型表达 customer/merchant 及消息交互。
2. 再把 actors 和消息实例分别翻译成 `UPPAAL` 模板。
3. 先做经典模型检查验证安全与活性。
4. 状态空间变大时，用 `UPPAAL SMC` 对关键承诺/知识事件估计概率区间。

## 案例与结果

论文报告：

1. 模型满足 `A[] ! deadlock`。
2. customer 到达 `s5` 后，`PAY` 承诺最终会被 customer 与 merchant 同时知晓为 fulfilled。
3. merchant 到达 `s6` 后，`DELIVER` 承诺最终会被双方知晓为 fulfilled。
4. `Customer(0)` 与 `Merchant(CUS)` 都能最终回到初始状态。
5. 在 `SMC` 下，“customer 离开初始状态后 `2` 时间单位内回到 `s0`”的概率区间约为 `[0.95,1]`。
6. “customer 在 `s5` 且知道 `PAY` 已 fulfilled”在 `1000` 时间界内的概率区间约为 `[0.902606,1]`。

## 与本研究的关系

### 相关性分析

它与博士研究中的“业务/软件状态机 + 承诺性质 + 可追溯查询”直接相关，尤其适合参考如何把高层语义承诺落成可检验状态。

### 可借鉴之处

1. 把 commitment 与 knowledge 分开建模，再通过查询把它们连接起来。
2. 用 actor 风格前端建模，再归约到 `UPPAAL` 后端验证。
3. 在状态空间膨胀时自然切换到 `SMC`。

### 存在的不足与改进空间

实验规模较小，且没有公开工件；其业务语义抽象较强，和真实电商平台仍有距离。

### 对本研究的启发

这篇论文说明，对非传统控制系统对象，仍然可以围绕“状态 + 承诺 + 知识”构造形式化性质，这有助于博士研究扩展到更广的软件状态机对象。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文公开，但未见 actor 模型、`UPPAAL` 工程或查询文件公开仓库。
- 获取方式/链接：[DOI](https://doi.org/10.7148/2018-0136)；[会议 PDF](https://www.scs-europe.net/dlib/2018/ecms2018acceptedpapers/0136_is_ecms2018_0856.pdf)
- 对后续复用的现实影响：适合作为“承诺/知识状态机”样本，但复跑仍需从论文手工重建。
