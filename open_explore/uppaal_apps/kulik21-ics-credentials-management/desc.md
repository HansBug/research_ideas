问题一句话：本文验证的是工业控制系统中的凭证管理子系统，核心问题是如何在 operations terminal、keyvault 和 network switch 之间保证凭证不泄露、票据只发给管理员且登录会话不会无限期存活。
方法一句话：作者把登录、发 token、申请 switch ticket、打开 session 的级联认证流程建成 `UPPAAL` timed automata，并对 confidentiality、authentication 和 freshness 三类安全性质做符号模型检查。
验证收获一句话：结果表明所设计的 keyvault-based 凭证管理协议能够保证 ticket 唯一性、管理员独占 switch 票据发放和 token/ticket/session 过期机制，工业合作方据此决定继续推进原型实现。

## 基本信息

- 标题：Formally Verified Credentials Management for Industrial Control Systems
- 中文标题：工业控制系统的形式化验证凭证管理
- 作者：Tomas Kulik、Jalil Boudjadar、Diego F. Aranha
- 单位：Aarhus University
- 发表：`FormaliSE 2021`
- DOI：`10.1109/FormaliSE52586.2021.00014`
- 链接：[DOI](https://doi.org/10.1109/FormaliSE52586.2021.00014)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🏭 工业与基础设施
- 被验证系统：工业控制网络中的 operations terminal (`OT`) / keyvault / switches 凭证管理与访问流程
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文参考文献给出了公开 `UPPAAL` 模型入口，可跳转到 `GitHub` 仓库。
- 案例/数据获取方式：案例来自工业合作方的控制系统架构；正文给出了 `OT`、switch 和 keyvault 的行为与三类账号配置。

## 简报

这篇论文验证的不是现场控制器，而是工业控制系统中的“谁能登录、何时能拿到凭证、多久后凭证失效”这一安全关键支撑流程。它把 access control 从工程经验问题，变成了一个可验证的状态机协议。

- 系统：`OT`、network switches 和 centralized keyvault 组成的凭证管理系统。
- 特点：多阶段认证、一次性 ticket、管理员角色约束、token/ticket/session 都有有效期。
- 规模：验证实例含 `1` 个 `OT`、`2` 个 switches、`1` 个 keyvault、`3` 组 credentials 和 `1` 个 time discretization process。
- 模型：`UPPAAL` timed automata 网络，手工建模协议交互和时间推进。
- 性质：ticket 唯一性、只有管理员能得到 switch ticket、token/ticket/session 必须过期。
- 方法：以 CTL 形式写 confidentiality / authentication / freshness 查询，并对最小工业配置做验证。
- 结果：核心性质全部通过；机密性验证约 `57 s`，认证验证约 `65 s`，freshness 验证约 `6 s`。

`工业 ICS 访问流程 -> OT / keyvault / switch 自动机 -> CTL 安全性质 -> UPPAAL 模型检查 -> 协议可部署性判断`

## 论文定位

这篇论文更像“工业控制系统里的安全支撑服务”案例，而不是物理控制回路本身。因此它在主轴上更适合归入 `🧩` 而非 `🛰️`。它验证的是一个具有明确角色流转和生命周期约束的认证工作流。

## 验证对象与问题背景

### 系统与场景

现代工业控制系统需要允许工程师或维护人员通过 `OT` 本地终端访问网络交换机和控制子系统。随着远程监控、配置和模块集成能力增强，凭证管理本身成了新的攻击面。

### 系统组成与运行机制

系统包含三类核心部件：

1. `OT`
   - 用户进入控制网络的入口。
2. `Switch`
   - 连接工业控制器的关键网络设备，错误配置可能影响整个控制过程。
3. `Keyvault`
   - 集中式凭证服务器，负责验证用户、发 token，并给目标 switch 生成一次性 ticket。

认证工作流大致为：

`user credential -> OT -> keyvault validation -> token -> switch selection -> one-time ticket -> switch validation -> session`

### 验证边界

论文重点验证凭证管理协议本身，不涉及完整控制器逻辑，也没有在本轮分析 availability of redundant keyvault，因为工业方当时优先关心的是单 keyvault 配置。

### 核心问题

1. 用户不能直接学到 switch 的真实 credential；
2. 只有管理员角色才能获得 switch access ticket；
3. 已发放的 token、ticket 和 session 必须在短时间后过期，降低 replay attack 面。

## 模型与形式化建模

### 抽象对象

作者定义了 `OT`、`switch` 和 `keyvault` 三类 timed automata，并用共享动作和参数化 channel 描述登录、验证、发票据和打开会话的过程。

### 建模形式

系统行为写成多个组件实例的并行组合。关键时间戳如 `issue_time`、`expiry_time` 通过离散时间进程统一维护，从而让 token / ticket / session 的生命周期可在模型中直接比较。

### 关键抽象与取舍

1. 使用一次性 ticket，而不是把长期 switch credential 暴露给用户；
2. 实际密码学细节被抽象成状态和 guard，重点验证流程逻辑；
3. availability 性质虽然形式化定义了，但未在本文实例中真正验证。

## 验证目标与性质

### 待验证问题

论文定义了三类核心性质：

1. **Confidentiality**
   - 所有生成的 tickets 必须唯一，不能重用；
2. **Authentication**
   - 非管理员即使持有有效 token，也不能得到 switch ticket；
3. **Freshness**
   - tokens、tickets、sessions 到期后必须失效。

### 性质类型

这些性质覆盖：

1. 机密性；
2. 认证正确性；
3. 新鲜性 / 生命周期安全；
4. 会话时效性。

### 查询表达

文中给出的代表性查询包括：

1. `A[] ticketsHaveUniqueIdentities()`
2. `A[] (canGenerateTicket()==false) imply !kv.gen_ticket`
3. `A<> (issuedTokensExpire() && issuedTicketsExpire() && issuedSessionsExpire())`

这些查询直接对应了系统的三类安全目标。

## 核心方法与验证流程

1. 明确工业控制系统中的认证流程和角色约束；
2. 把 `OT`、`keyvault`、`switch` 各自建成 `UPPAAL` 模板；
3. 利用 time discretization process 管理离散时间和过期时间；
4. 在最小部署实例上执行符号模型检查；
5. 根据验证结论判断协议组合方式是否适合工业合作方部署。

## 案例与结果

### 验证配置

实验配置为：

1. `1` 个 `OT`；
2. `2` 个 switches；
3. `1` 个 keyvault；
4. `3` 组 credentials：
   - 管理员；
   - 有效但非管理员；
   - 无效凭证。

最大执行时间窗口设为 `16` 个 time units，以控制状态空间。

### 结果

1. 机密性性质验证耗时约 `57 s`，内存约 `1.4 GB`；
2. 认证性质验证耗时约 `65 s`，内存约 `1.6 GB`；
3. freshness 性质验证耗时约 `6 s`，内存约 `0.1 GB`；
4. 其余性质也都在一分钟内完成。

论文明确说明，这些结果已经足以回答工业合作方最关心的问题：这套协议组合在其场景下是否可行。合作方随后决定继续做原型实现。

## 与本研究的关系

### 相关性分析

这篇论文虽然不直接验证控制回路，但它非常适合作为“控制系统外围软件服务如何形式化”的案例。对博士研究的系统级建模边界很有参考价值。

### 可借鉴之处

1. 用少量核心安全性质就能对部署可行性给出强结论。
2. 将 ticket / token / session 的生命周期显式建模，避免把安全性留给实现细节。
3. 把工业合作方的需求转成有限、可检查的性质簇。

### 存在的不足与改进空间

1. availability / 冗余 keyvault 尚未真正验证。
2. 密码学原语被抽象掉，主要验证流程而非密码学安全证明。
3. 物理攻击与更复杂网络威胁未纳入。

### 对本研究的启发

它说明控制系统研究不必只盯着 plant 和 controller。像 credential、session、role 这类外围服务，同样可以变成明确的状态机对象，并直接服务系统可信性论证。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 直接可用
- 判断依据：论文给出了公开模型入口，当前可跳转到 `GitHub` 上的 `UPPAAL` 模型文件。
- 获取方式/链接：[DOI](https://doi.org/10.1109/FormaliSE52586.2021.00014)；[模型入口](https://tinyurl.com/ycwt7pcj)；[GitHub 文件](https://github.com/kuliktomas/CredentialManagementICS/blob/master/KeyvaultCredentialsv2.xml)
- 对后续复用的现实影响：这是公开度较高的 ICS 安全服务案例，适合直接复用其 token / ticket / session 建模方式。
