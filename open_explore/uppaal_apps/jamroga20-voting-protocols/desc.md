问题一句话：本文验证的是电子投票协议 `Prêt à Voter`，核心问题是如何用 `UPPAAL` 对多角色投票流程及其 receipt-freeness 一类知识性质做初步模型检查。
方法一句话：作者把 voter、coercer、mix teller、decryption teller、auditor 和 voting infrastructure 建成 `UPPAAL` 模型，并提出把部分 `CTLK` 知识性质重写为纯 `CTL` 查询，以在 `UPPAAL` 中近似验证 receipt-freeness。
验证收获一句话：论文证明 `UPPAAL` 足以承载一批流程与审计性质的验证，并能模拟弱 receipt-freeness 与 `Pfitzmann` 攻击；同时也清楚暴露出状态空间和查询语言表达能力的边界，如 `5` 名 voter 场景即出现 `OOM`，强性质还受限于嵌套路径量词。

## 基本信息

- 标题：Model Checkers Are Cool: How to Model Check Voting Protocols in Uppaal
- 中文标题：如何在 `Uppaal` 中模型检查投票协议
- 作者：Wojciech Jamroga、Yan Kim、Damian Kurpiewski、Peter Y. A. Ryan
- 单位：SnT, University of Luxembourg；Institute of Computer Science, Polish Academy of Sciences
- 发表：arXiv preprint 2020
- DOI：`10.48550/arXiv.2007.12412`
- 链接：[DOI](https://doi.org/10.48550/arXiv.2007.12412)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🌐 网络与分布式服务
- 被验证系统：`Prêt à Voter` 电子投票协议及其多角色审计流程
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文公开了 arXiv 论文，但未给独立 `UPPAAL` 模型仓库或工件压缩包。
- 案例/数据获取方式：案例来自 `Prêt à Voter` 协议流程与其角色交互建模，不依赖外部数据集。

## 简报

这篇论文的重点不在“最终证明电子投票绝对安全”，而在说明 `UPPAAL` 这样一个偏 timed automata 的模型检查器，也可以被用来分析多角色投票协议，甚至通过模型改造近似处理知识性质。

- 系统：`Prêt à Voter` 投票流程中的 voter、coercer、mix teller、decryption teller、auditor 和系统基础设施。
- 特点：多角色协作、混洗与解密审计、receipt-freeness 与 voter-verifiability 背景强。
- 规模：实验按 `1-5` 个 voters 配置展开；部分公式在 `5` 个 voters 时已经出现 `Out of memory`。
- 模型：多模板 `UPPAAL` 模型，核心模板包括 voter、coercer、mix teller、decryption teller、auditor。
- 性质：审计失败可达性、voter 是否会被 coercer 惩罚、拿到 ballot 后是否最终标记选择、receipt-freeness 变体。
- 方法：标准 `CTL` 查询 + 通过“real states / reverse states”重构把部分 `CTLK` 性质转成纯 `CTL`。
- 结果：部分流程性质可验证，弱 receipt-freeness 可嵌入到 `UPPAAL`，但更强知识性质和更大规模实例很快碰到表达与状态空间边界。

`Prêt à Voter 多角色流程 -> UPPAAL 模板化建模 -> CTL 查询 + CTLK 到 CTL 重构 -> 流程性质、receipt-freeness 与攻击样例分析`

## 论文定位

这篇论文更偏“业务流程/多角色协议验证方法样例”而非成熟工程案例。虽然对象是投票协议，但真正验证的核心是角色协作流程和知识相关属性，因此比起传统网络协议，它更适合放在 `🧩` 主轴下。

## 验证对象与问题背景

### 系统与场景

被验证对象是 `Prêt à Voter` 电子投票协议。该协议强调 ballot secrecy、receipt-freeness、voter-verifiability 等性质，并包含 ballot form、receipt、web bulletin board、mixing 和 decryption 等环节。

### 系统组成与运行机制

论文把协议主体分成：

1. **Voter**
   - 领 ballot、标记选择、投递 receipt、可执行验证。
2. **Coercer**
   - 试图影响投票并据 receipt 判断 voter 是否服从。
3. **Mix Teller**
   - 对加密票据做 re-encryption mixes。
4. **Decryption Teller**
   - 参与阈值解密。
5. **Auditor**
   - 对 mix 和流程做审计。
6. **Voting Infrastructure**
   - 提供 bulletin board、receipt 处理等基础支撑。

### 验证边界

本文验证的是**协议角色交互与抽象性质**，不是完整密码学证明、真实选举部署或大规模选民统计行为。

### 核心问题

电子投票的困难在于：

1. 参与者多；
2. 性质强依赖“谁知道什么”；
3. 许多性质天然属于 epistemic / knowledge logic，而不是普通时序逻辑。

### 研究动机

作者希望证明：即便 `UPPAAL` 只支持受限的 `CTL` 片段，也仍能作为投票协议的建模和初步验证平台。

## 模型与形式化建模

### 多角色模板

论文为每类角色分别建立模板。以 voter 为例，其局部状态包括：

1. idle；
2. has_ballot；
3. marked_choice；
4. received_receipt；
5. verification；
6. passed / failed；
7. end。

这让协议流程可以被显式观察，而不是只把投票当成黑箱消息交换。

### 知识性质重构

为了在 `UPPAAL` 中表达类似 `¬K_c ¬voted_{i,j}` 的公式，作者引入：

1. real states；
2. reverse states；
3. epistemic transition；
4. persistent Boolean variables。

其核心思想是：把“存在一个不可区分状态”翻译成“存在一条经过 reverse states 回到初始点的路径”。

### 攻击扩展

在 `Pfitzmann` 攻击实验中，作者只需修改第一位 mix teller 的重加密行为，就能在模型里表达 corrupted mix teller。

## 验证目标与性质

### 待验证问题

文中首先验证了三条基础性质：

1. `E<> failed_audit_0`
   - 第一位 mix teller 最终可能 audit fail。
2. `A[] not punished_i`
   - 某 voter 不会被 coercer 惩罚。
3. `has_ballot_i --> marked_choice_i`
   - 拿到 ballot 后最终会标记选择。

### 性质类型

1. 可达性；
2. 安全/无惩罚；
3. 活性；
4. 弱 receipt-freeness；
5. 审计可检测性。

### 判定边界

作者明确指出，`UPPAAL` 的查询语言不支持嵌套路径量词，因此强版本知识性质无法在原生 `UPPAAL` 中完整验证。

## 核心方法与验证流程

1. 先按 `Prêt à Voter` 流程建多角色模板。
2. 对 `1-5` 个 voters 的不同实例运行基础 `CTL` 查询。
3. 观察哪些性质可验证、哪些因状态空间爆炸失败。
4. 再通过 reverse-state 技术把部分知识性质嵌入 `UPPAAL`。
5. 最后加入 corrupted mix teller 以复现实验性攻击路径。

这种方法非常适合说明“如何在工具受限时仍做增量式验证”。

## 案例与结果

### 基础查询

作者报告：

1. `failed_audit_0` 在 `1-4` 个 voters 配置下均可验证为可达；
2. 到 `5` 个 voters 时出现 `Out of memory`；
3. `A[] ¬punished_i` 在所有 `1-5` 个配置上都不满足，并给出反例；
4. `has_ballot_i --> marked_choice_i` 在所有配置上都触发 `Out of memory`。

### receipt-freeness

对弱版本 receipt-freeness，经过模型重构后，`UPPAAL` 报告公式成立。也就是说，论文证明至少有一类知识性质可以被这种技术性方法转写进纯时序模型。

### 攻击样例

在 corrupted mix teller 扩展里，作者验证：

1. `E<> failed_audit_0` 成立；
2. `E<> passed_audit_0` 也成立。

这意味着攻击既可能被审计抓住，也可能逃过审计。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究的关系主要体现在“复杂业务规则和知识性质如何压缩进状态机模型与查询表达”。

### 可借鉴之处

1. 多角色流程系统可以通过模板化方式进入 `UPPAAL`。
2. 原生查询语言不够用时，可以先改模型再改公式。
3. 论文非常诚实地报告了表达边界和 `OOM`，这种边界记录值得保留。

### 存在的不足与改进空间

1. 更像方法学展示，不是成熟可复现的大规模案例。
2. 缺少独立模型仓库。
3. 强知识性质仍需要更强的模型检查器。

### 对本研究的启发

它对“性质生成”很有启发，因为业务流程与知识相关性质并不天然适合普通时序逻辑，但可以通过中间层重构逐步逼近。

## 重要的相关工作

### 1. `Prêt à Voter`

- 这是论文分析的核心协议，也是电子投票里最有代表性的 receipt-based 方案之一。

### 2. Receipt-freeness / voter-verifiability

- 论文重点围绕这些高阶性质组织查询与模型改造。

### 3. `Pfitzmann` attack

- 攻击扩展说明模型不仅能验证正常流程，也能注入已知隐私威胁。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：arXiv 论文当前可获取，但未确认到独立 `UPPAAL` 模型工件公开入口。
- 获取方式/链接：[DOI](https://doi.org/10.48550/arXiv.2007.12412)；[arXiv PDF](https://arxiv.org/pdf/2007.12412)
- 对后续复用的现实影响：适合借鉴多角色建模与性质重构方法，但如果要复跑具体模型，仍需依据正文自行重建。
