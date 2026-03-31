问题一句话：本文验证的是电子考试流程系统，核心问题是候选人注册、答题、接收、阅卷、通知等流程在时限和规则约束下是否可靠、无歧义且具备基本防作弊能力。
方法一句话：作者用 `UPPAAL` 建立 candidate、administrator、invigilator、examiner 四个模板，并把注册、提交、接受、阅卷、通知等操作编码为队列与状态公式。
验证收获一句话：在 `2` 名考生、`3` 道题的实例上，论文给出的 `12` 条关键性质全部满足，覆盖死锁、注册合法性、答题唯一性、可用期、答案-分数一致性、作弊检测等方面。

## 基本信息

- 标题：Ensuring Reliability in Electronic Examinations Through `UPPAAL`-Based Trustworthy Design
- 中文标题：通过基于 `UPPAAL` 的可信设计保障电子考试可靠性
- 作者：Wenbo Zhou、Yujiao Zhao、Ye Zhang、Liwen Mu、Yiyuan Wang、Minghao Yin
- 单位：Northeast Normal University；Guangxi Normal University
- 发表：PeerJ Computer Science 2024
- DOI：`10.7717/peerj-cs.2377`
- 链接：[DOI](https://doi.org/10.7717/peerj-cs.2377)
- 应用领域：🧩 软件、架构与组件系统
- 被验证系统：电子考试流程与角色协作系统
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文公开了 [GitHub 仓库](https://github.com/TURTING-BO/An-Electronic-Examination-Model-Based-on-UPPAAL) 和 [Zenodo 归档](https://doi.org/10.5281/zenodo.12787513)。
- 案例/数据获取方式：无真实考试数据集；论文提供的是可执行模型与示例参数。

## 简报

这篇论文验证的不是考试题库本身，而是考试流程规则是否被系统模型正确体现。它把候选人、管理员、监考员、阅卷员之间的操作序列都显式编码，使“谁先做什么、什么条件下才能做下一步”可以被穷举检查。

- 系统：candidate / administrator / invigilator / examiner 四角色电子考试系统。
- 特点：考试规则驱动、队列化操作记录、形式化防作弊检查、可复位流程。
- 规模：示例实例为 `2` 名候选人、`3` 道题、`12` 条性质；参数包括 `MaxT=1000`、`ExpT=10000`、最小允许答案距离 `D=2`。
- 模型：四个 `UPPAAL` 模板 + `Operation` / `Item` / `CandidateType` / `OpQueue` 数据结构。
- 性质：无死锁、注册/提交/接受合法性、答案唯一性、题目顺序、考试可用期、答案与分数一致、作弊检测、mark 完整性。
- 方法：先仿真检验流程合理性，再逐条用 `UPPAAL` verifier 检查 `12` 条公式。
- 结果：全部 `12` 条性质满足，单条验证时间大多小于 `0.35s`，内存开销约 `40MB` 量级。

`考试规则 -> 四角色 timed automata -> 队列与状态公式 -> 12 条可靠性性质验证 -> GitHub/Zenodo 模型归档`

## 论文定位

这是一篇偏“业务流程可信设计”的 `UPPAAL` 应用案例。它不是控制系统文献，但很适合作为“多角色流程系统如何用状态机验证规则一致性”的代表。

## 验证对象与问题背景

### 系统与场景

被验证对象是电子考试系统。作者关心的是：在注册、登录、发题、提交、接受、阅卷、通知等全过程中，系统能否保证基本可靠性和公平性。

### 系统组成与运行机制

系统包含四个核心角色：

1. **Candidate**
   - 注册、登录、接题、答题、接收成绩。
2. **Administrator**
   - 初始化系统、设置正确答案、维护注册信息、负责 reset。
3. **Invigilator**
   - 检查登录、发放题目、接收并确认提交。
4. **Examiner**
   - 设置答案、阅卷、通知成绩。

系统还用 `T/R/S/A` 四类队列分别记录总操作、注册、提交和接受操作。

### 验证边界

本文验证的是**考试流程规则与角色协同逻辑**，不是实际网络安全协议、身份认证实现或大规模真实考试平台性能。

### 核心问题

电子考试的风险不只是系统崩溃，还包括未注册者提交、重复作答被接受、考试开始后答案被篡改、相似答案作弊未被发现等流程性错误。

### 研究动机

作者希望把“可靠电子考试”从自然语言规则提升为可执行、可验证的 timed automata 模型。

## 模型与形式化建模

### 数据结构

论文定义了三个核心结构：

1. `Operation = (id, op, q, a)`
2. `Item = (q, a, s)`
3. `Candidate = (items, total)`

并实现了 `OpQueue`、`MarkScore`、`ComputeSMatrix` 等函数。

### 模板

1. **Candidate template**
   - 从注册到考试结束和成绩通知的完整循环。
2. **Administrator template**
   - 初始化、设置正确答案、记录注册、发出 reset。
3. **Invigilator template**
   - 处理登录、发题、接收提交并确认。
4. **Examiner template**
   - 设置答案、阅卷、计算相似度矩阵并通知成绩。

### 模型边界

作者明确使用了简化假设：

1. 示例只建 `1` 个 administrator / invigilator / examiner；
2. 候选人数可以扩展，但验证实例选择 `2` 人；
3. 防作弊只用“答案相似度过高”这一简化规则。

## 验证目标与性质

### 待验证问题

论文定义了 `12` 条性质，包括：

1. no deadlock
2. candidate registration
3. candidate eligibility
4. answer authentication
5. answer singularity
6. acceptance assurance
7. questions ordering
8. exam availability
9. answer-score integrity
10. cheater detection
11. marking correctness
12. mark integrity

### 性质类型

1. **流程安全性质**
   - 不允许未注册或未提交却被接受。
2. **顺序与唯一性性质**
   - 每题只接受一个答案，题目按正确顺序进行。
3. **完整性性质**
   - 开考后不能再改正确答案；分数必须与答案一致。
4. **防作弊性质**
   - 候选人答案相似度不得超过阈值。

### 查询表达

代表性查询包括：

1. `A[] not deadlock`
2. `A[] forall(i:ID) not (not FindElement(R,i) and FindElement(S,i))`
3. `A[] forall(i:ID) OneAnswerEachQuestion(A, i)`
4. `A[] NoDistanceExceed(sm)`

这些查询分别对应“流程不会卡死”“提交前必须注册”“每题只能接受一个答案”“两名考生的答案相似度不能超过阈值”。

## 核心方法与验证流程

1. 先用 `UPPAAL` 编辑器和 simulator 构造并走通考试流程。
2. 再把自然语言规则翻成 `12` 条性质。
3. 在 `N=2, Q=3` 的实例上逐条运行 verifier。
4. 用 `ComputeSMatrix` 把作弊检测转成显式状态变量约束。

## 案例与结果

### 参数配置

1. `N=2`
2. `Q=3`
3. `MaxSize=50`
4. `MaxT=1000`
5. `ExpT=10000`
6. `D=2`
7. `U=10`

### 验证结果

表 2 显示全部 `12` 条性质都为 `Satisfied`：

1. 最慢的是 `Acceptance assurance`，验证时间约 `0.344s`。
2. 多数性质在 `0.03s-0.26s` 之间完成。
3. resident memory 大致在 `39.7MB-40.2MB` 之间。
4. virtual memory peak 大致在 `105MB-106MB`。

作者据此认为，该模型至少能支撑一个结构清晰、规则一致的基础电子考试系统原型。

## 与本研究的关系

### 相关性分析

尽管不是控制系统，这篇论文对博士研究仍有价值，因为它展示了如何把复杂业务规则拆成多角色状态机并进行一致性验证。

### 可借鉴之处

1. 用统一的 `Operation` 队列连接多角色交互。
2. 把自然语言规则逐条翻译成状态公式。
3. 在单模型里同时表达流程、评分和简化防作弊逻辑。

### 存在的不足与改进空间

实例规模较小，且作弊检测很简化；还没有连接真实考试平台与隐私/认证机制。

### 对本研究的启发

对博士研究而言，它说明“性质生成”完全可以面向业务规则而不只面向控制逻辑，关键是先把角色、操作和队列结构化。

## 重要的相关工作

### 1. 电子考试研究

- 文中对在线考试、作弊与系统设计的相关综述做了较全面回顾。

### 2. `UPPAAL`

- `UPPAAL` 被用于表达多角色并发流程与时间约束。

### 3. 作弊检测

- 论文采用了基于答案相似度的简化 cheating detection 思路。

## 案例、模型与数据公开情况

- 可获取性判断：🟢 可直接获取
- 判断依据：论文明确同时给出 GitHub 仓库和 Zenodo 归档。
- 获取方式/链接：[GitHub 仓库](https://github.com/TURTING-BO/An-Electronic-Examination-Model-Based-on-UPPAAL)；[Zenodo](https://doi.org/10.5281/zenodo.12787513)
- 对后续复用的现实影响：这是当前文库里公开度最高的业务流程类案例之一，适合作为“多角色流程系统如何写 `UPPAAL`”的对照样本。
