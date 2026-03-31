问题一句话：本文验证的是 `SIP/ZRTP` 语音通信握手协议，核心问题是呼叫建立、`ZRTP` 密钥协商和 `SAS` 认证这些阶段在配置不匹配或中间人迹象出现时，是否会正确终止并进入断开状态。
方法一句话：作者把 `Caller`、`SIPServer`、`Callee` 三个角色分别建成 `UPPAAL` 自动机，并用时序逻辑查询检查 deadlock prevention、liveliness、安全性和多类 mismatch detection。
验证收获一句话：论文在一个小规模三角色模型上证明了基本握手流程可达，也证明多类配置不匹配、`Hello` 拒绝、`DH` 确认失败和 `MITM` 检测都会把系统导向断开状态，给出了一个很轻量但结构完整的语音协议验证样例。

## 基本信息

- 标题：Simulation and Formal Verification of SIP/ZRTP Protocol using UPPAAL
- 中文标题：使用 `UPPAAL` 对 `SIP/ZRTP` 协议进行仿真与形式化验证
- 作者：Aishwarya Raghavan、Amritha P. P.、M. Sethumadhavan
- 单位：Amrita School of Engineering / TIFAC-CORE in Cyber Security
- 发表：International Journal of Recent Technology and Engineering 2019
- DOI：`10.35940/IJRTE.B1029.0982S1119`
- 链接：[DOI](https://doi.org/10.35940/IJRTE.B1029.0982S1119)
- 主轴分类：🛰️ 协议与通信机制
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：基于 `SIP` 建立会话并使用 `ZRTP` 完成密钥协商的语音通信协议
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未提供公开 `UPPAAL` 模型仓库，仅公开论文 PDF。
- 案例/数据获取方式：案例来自 `SIP/ZRTP` 协议流程与 `RFC 6189` 描述，不依赖实验数据集。

## 简报

这篇论文规模不大，但结构很完整。它把 `SIP` 预握手、`ZRTP` 发现与密钥协商、`SAS` 认证这些阶段全部显式串起来，因此可以检查“流程能否走通”和“走不通时是否会安全地停下”。

- 系统：`Caller`、`SIPServer`、`Callee` 三方语音呼叫与 `ZRTP` 密钥协商。
- 特点：先 `SIP` 再 `ZRTP`，包含 `Hello`、`Commit`、`Diffie-Hellman`、`Conf2Ack`、`SAS` 认证等阶段。
- 规模：`3` 个核心自动机模板，覆盖配置不匹配、`Hello` 拒绝、`DH` 错误确认、`MITM` 检测等失败路径。
- 模型：基于 timed automata 的三角色交互模型。
- 性质：无死锁、握手活性、正常清理、mismatch detection、`MITM` 检测后安全断开。
- 方法：用 `A[]`、`E<>` 形式的时序逻辑查询逐条检查协议场景。
- 结果：正常流程可达；多类异常路径均会把系统导向 disconnected 状态。

`SIP 预握手 -> ZRTP 发现与密钥协商 -> SAS 认证 -> 时序逻辑查询 -> 验证正常流程与异常断开行为`

## 论文定位

这是一个偏教学型、结构清楚的协议应用案例。它不追求大规模状态空间，而是把 `VoIP` 安全通信的关键阶段组织成一个完整 `UPPAAL` 验证样例，因此更适合归入 `🛰️` 主轴下的轻量协议验证案例。

## 验证对象与问题背景

### 系统与场景

被验证对象是 `VoIP` 语音通信中的 `SIP/ZRTP` 协议流程。`SIP` 负责初始呼叫建立，`ZRTP` 在媒体路径上完成会话密钥协商，以支持安全 `SRTP` 通信。

### 系统组成与运行机制

论文把协议拆成三方：

1. **Caller**
   - 发起邀请、参与 `Hello`/`DH`/`SAS` 过程。
2. **SIPServer**
   - 只参与会话建立前的 `SIP` 握手。
3. **Callee**
   - 接收邀请并参与后续 `ZRTP` 验证。

协议主流程分成：

1. `SIP Handshake`
2. `ZRTP Discovery`
3. `Diffie-Hellman Key Agreement`
4. `SRTP/SAS Authentication`

### 验证边界

本文验证的是**协议离散交互逻辑与异常分支处理**，不是密码学证明、真实网络延迟建模或实际音频媒体流。

### 核心问题

对作者来说，关键不是重新证明 `ZRTP` 的密码学安全，而是验证：

1. 正常流程是否能从邀请走到安全会话建立；
2. 多类 mismatch 和异常是否会被及时识别；
3. 识别后系统是否进入安全的断开状态而不是卡住。

### 研究动机

`VoIP` 广泛使用而且容易受窃听或中间人攻击，因此需要一个形式化样例来说明协议状态机本身没有明显逻辑缺陷。

## 模型与形式化建模

### 模型结构

作者为 `Caller`、`SIPServer`、`Callee` 分别建立模板。模型中显式出现了论文给出的关键同步事件，例如：

1. `caller_invite!`
2. `try_connection!`
3. `zCallerHello!`
4. `zCalleeAck_Hello!`
5. `Commit!`
6. `send_DH1! / send_DH2!`
7. `Conf2Ack!`
8. `SAS_Callee! / SAS_Caller!`

### 异常分支

模型同时显式保留若干失败路径：

1. `caller_config_mismatch!`
2. `callee_config_mismatch!`
3. `caller_hello_denied! / callee_hello_denied!`
4. `caller_wrong_confirmation! / callee_wrong_confirmation!`
5. `MITM` 检测状态

这些分支最终都通向 disconnected commit states。

## 验证目标与性质

### 待验证问题

论文的查询集中在以下几组：

1. **Deadlock Prevention**
   - 系统整体不能死锁。
2. **Liveliness / Reachability**
   - 某阶段触发后，后续阶段应可达。
3. **正常清理**
   - 通信结束后 caller/callee/server 应进入对应清理状态。
4. **Mismatch Detection**
   - 配置、`Hello`、`DH`、`MITM` 异常时应断开连接。

### 查询表达

文中直接给出典型查询，例如：

1. `A[] not deadlock`
2. `E<> (Caller.Sent_Invite imply SIPServer.Invite_Callee)`
3. `E<> (Caller.send_clear imply Callee.clear_rcv)`
4. 多条 `E<> (...) imply ... disconnected` 查询

### 性质类型

1. 安全性质；
2. 活性/可达性；
3. 异常处理正确性。

## 核心方法与验证流程

1. 先把 `SIP` 与 `ZRTP` 的多阶段交互流程画成三方自动机。
2. 用 `UPPAAL` simulator 检查基本流程是否可走通。
3. 再用 verifier 对每个目标性质写时序逻辑查询。
4. 对正常流程、配置不匹配、`Hello` 阶段拒绝、`DH` 阶段错误确认和 `MITM` 检测分别验证。

这种方法虽然简单，但很适合做协议流程级 sanity check。

## 案例与结果

### 正常流程

论文表明：

1. `Caller` 发出 invite 后；
2. `SIPServer` 可进入 `Invite_Callee`；
3. `Callee` 能进入 connecting；
4. 后续 `Hello`、`DH`、`Conf2Ack` 和 `SAS` 流程都可达。

### 异常流程

更重要的是，论文验证了以下异常都会导向 disconnected：

1. caller/callee 配置不匹配；
2. `Hello` 标识符不匹配；
3. `DH` 生成后的错误确认；
4. `MITM` 检测触发。

### 结果解读

因此，这篇论文的收获主要是“协议状态机层面的逻辑完整性检查”，而不是更强的密码学不可区分性或大规模攻击概率分析。

## 与本研究的关系

### 相关性分析

它对博士研究的价值在于：虽然对象不是控制器，但非常适合作为“如何把一段自然语言协议流程拆成多模板状态机”的轻量样本。

### 可借鉴之处

1. 三角色模板化建模方式很清晰。
2. 异常分支被显式编码为状态迁移，而不是只在文字里讨论。
3. 适合用来对照“性质簇”写法：正常可达、异常断开、无死锁。

### 存在的不足与改进空间

1. 模型规模较小，更多是流程级样例。
2. 论文未提供独立 `UPPAAL` 工程。
3. 对攻击者的表达较弱，仍偏“检测后断开”而非深入安全证明。

### 对本研究的启发

它说明：即使是小论文，只要系统、阶段和异常边界写得清楚，也很适合作为状态机结构化建模样本。

## 重要的相关工作

### 1. `ZRTP`

- 论文明确以 `ZRTP` 的 `SAS` 认证和会话密钥新鲜性为背景。

### 2. `UPPAAL`

- `UPPAAL` 在这里承担协议流程 sanity check 和异常分支验证的角色。

### 3. `RFC 6189`

- 文中将 `RFC 6189` 作为 `ZRTP` 协议参考来源之一。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文 PDF 可获取，但原文未提供独立 `UPPAAL` 模型或实验工件下载入口。
- 获取方式/链接：[DOI](https://doi.org/10.35940/IJRTE.B1029.0982S1119)；[论文 PDF](https://www.ijrte.org/wp-content/uploads/papers/v8i2S11/B10290982S1119.pdf)
- 对后续复用的现实影响：适合当成协议状态机结构化建模样本，不适合期待“拿到现成模型直接复跑”。
