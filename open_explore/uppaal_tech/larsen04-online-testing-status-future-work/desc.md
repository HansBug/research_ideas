# Online Testing of Real-time Systems using Uppaal: Status and Future Work

- 问题一句话：`T-UPPAAL` 虽然已经证明在线实时测试可行，但若想真正走向工程化与长期扩展，仍需要把当前实现状态、实际应用经验和下一步技术瓶颈系统记清楚。
- 方法一句话：论文在 relativized online testing 框架基础上，总结 `T-UPPAAL` 的实现状态、实验与工业试用经验，并明确提出 coverage、诊断、环境模拟器/测试 oracle 拆分、时间不确定性和值传递等后续方向。
- 解决点一句话：它把 testing 分支从“算法论文”继续推进成“路线图论文”，为后续 `T-UPPAAL` 的工程深化给出一份非常清晰的研发蓝图。

## 论文定位

这篇论文在 `uppaal_tech/` 中并不是正式理论主条目，而更像一个 `🛠️ 工程/工具链` 的**状态汇报与路线图条目**。它的重要性不在于比 [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/) 新增了一个核心定理，而在于它系统回答了：

1. `T-UPPAAL` 当前到底做到哪里了；
2. 实验与工业接触暴露出哪些真实问题；
3. 下一步最值得投入的改进方向是什么。

这类 paper 很容易被低估，但对技术线梳理非常重要，因为它记录的是研究团队对“接下来要怎么做”的自我判断。

## 立足问题

这篇论文立足的问题，是在线实时测试从“可行”走向“可用”时必然遇到的那些工程瓶颈。

作者已经接受几件事：

1. relativized conformance 有理论基础；
2. symbolic online testing 能跑；
3. `T-UPPAAL` 已经有公开原型；

因此问题不再是“这条线是否成立”，而是：

1. 当前工具真正缺什么。
2. 随机测试为什么有时还不够。
3. 工业接口、时钟同步、数据传递、coverage 与诊断怎样补齐。

这是一篇很典型的“第二阶段问题论文”：不是从零搭框架，而是在真实使用后回头盘点短板。

## 核心方法

这篇论文的方法主要不是新算法，而是**把 testing 框架拆成若干独立改进面向，并给出清晰的工程分解图**。

### 1. 先重申 testing 线的基本结构

论文前半沿用 testing 分支的核心设定：

1. 显式环境模型；
2. 实现规格模型；
3. relativized timed input/output conformance；
4. online randomized testing；
5. `T-UPPAAL` 作为执行引擎。

这一部分的作用不是重复已有理论，而是为后面的状态盘点与未来工作定锚：后续所有改进都围绕这套框架展开，而不是推倒重来。

### 2. 把 environment simulator 与 test oracle 明确区分开

这篇论文最值得注意的一个观点，是作者开始明确地区分：

1. **environment simulator**
   - 负责根据环境模型生成输入、驱动执行；
2. **test oracle / monitor**
   - 负责根据实现规格分析 trace、给出 verdict、收集覆盖与诊断信息。

这一步很关键，因为它意味着 testing 工具不应再被看成一个 monolithic process，而应是两个节奏与职责不同的部件：

1. simulator 更时间敏感；
2. oracle 可以更偏分析、覆盖统计与诊断。

后文提出的许多 future work，正是围绕这两者拆分后才变得自然。

### 3. 把 future work 细分成 test generation 与 test execution 两大类

论文后半把改进方向分得很清楚。

#### 3.1 Test generation improvements

作者指出几个主要缺口：

1. **值传递与数据选择能力不足**
   - 当 `UPPAAL` 只有 handshake channel 和全局变量时，复杂 I/O 数据交互建模不够自然。
2. **随机引导可能遇到 narrow passages**
   - 某些关键行为很窄，纯随机不容易命中。
3. **缺少覆盖度量**
   - 测试跑了很久，仍不知规格哪些部分真正被触及。
4. **失败诊断信息不足**
   - 出现 fail 后，很难快速定位是规格哪一块最可能被违反。

对应地，作者提出：

1. 用更强的数据与值绑定机制增强测试输入生成；
2. 结合 offline generated traces 或 case generators 来辅助 online guiding；
3. 引入 online model coverage analysis；
4. 分析 state-set 演化中的 dead-ends 与 branching points，用于生成诊断线索。

这说明作者已经非常清楚：randomized online testing 只是起点，不是终点。

#### 3.2 Test execution improvements

这里作者关注的是“工具与真实时间世界对接”的麻烦：

1. 真实系统可能既按绝对时间调度，也按相对时间调度；
2. 模型时钟与 `IUT` 时钟之间可能有漂移；
3. state-set 大小时大时小，会影响在线响应；
4. 某些工业接口缺少足够好的 controllability 与 observability。

因此 future work 包括：

1. 把 observation uncertainty 纳入算法；
2. 允许在时间观测上使用区间而非单点；
3. 研究更稳定的 state-set precomputation 或更快算法；
4. 更进一步把 emulator 与 monitor 分离，以利于算力分配。

这些讨论非常工程化，也说明团队已经真正碰到了“理论没问题但实时执行不稳定”的现实问题。

### 4. 用 coverage 与 diagnostic information 形成闭环

论文的一个很强的信号是：作者已经开始把 testing 想成闭环流程，而不只是单次 verdict。

其设想是：

1. monitor 在分析 trace 时，同时产生 coverage facts；
2. coverage facts 反过来转成 guiding hints；
3. failing traces 还应转成 diagnostic information；
4. offline case generator、model checker 与 online tester 之间可以通过 traces / hints 互通。

文中的 Figure 11 实际上已经画出了一个相当完整的数据流图：

1. `MEnv || MImp`
2. adapter
3. emulator
4. monitor
5. selector
6. coverage / diagnostic storage
7. offline tester / model checker

这已经很接近后续许多现代 testing platform 的结构了。

### 5. 用工业接触暴露“真实世界问题”

论文还记录了 Danfoss refrigeration controller 一类工业接触中的经验。这里最重要的不是具体控制逻辑，而是作者从真实接入中学到：

1. model 自己也可能有错误，需要先仿真验证；
2. 现实测试接口往往不够理想；
3. 时钟精度与采样分辨率会产生 seemingly spurious failures；
4. 工业合作会把“工具理论问题”迅速变成“接口与同步问题”。

这让本文的 future work 不再是空想，而是实打实从部署困难里长出来的。

## 解决了什么问题

这篇论文解决的，不是某个 formal theorem 的缺口，而是 testing 线的研发方向不够清晰这个问题。

### 1. 它把 testing 平台下一步要补的关键板块列得很完整

尤其是：

1. guiding；
2. coverage；
3. diagnosis；
4. uncertainty；
5. emulator / monitor split；
6. richer data communication。

这些后来都证明是 testing 平台不可回避的问题。

### 2. 它把原型能力与工业真实短板同时记录下来了

这让后人可以区分：

1. 当前已经跑通了什么；
2. 还卡在哪些工程问题上；
3. 哪些未来工作是“真需求”，而不是泛泛口号。

### 3. 它初步画出了 testing 平台的系统架构图

Figure 11 里对 active components、passive storages、guidance data flow 的组织，很适合作为 testing 分支后续演进的起点结构。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线里扮演的是 testing 分支的“**研发路线图条目**”。

### 它接在谁之后

它直接接在：

1. [mikucionis03-online-on-the-fly-testing-real-time-systems](../mikucionis03-online-on-the-fly-testing-real-time-systems/)
   - 提出 testing 原型。
2. [larsen04-online-testing-real-time-systems-using-uppaal](../larsen04-online-testing-real-time-systems-using-uppaal/)
   - 给出 formalized 框架与证明口径。

### 它往后影响了谁

它往后明显影响：

1. [hessel08-testing-real-time-systems-using-uppaal](../hessel08-testing-real-time-systems-using-uppaal/)
   - testing 工具与方法继续成熟。
2. [mikucionis10-online-testing-real-time-systems](../mikucionis10-online-testing-real-time-systems/)
   - 更系统的 testing 总结。
3. 所有把 coverage / diagnosis / industrial deployment 纳入 testing 的后续工作。

### 它更靠近哪条主线

它最靠近：

1. `T-UPPAAL` 工程化；
2. testing tool architecture；
3. online guidance / coverage / diagnosis；
4. 工业接口与部署问题。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟨 中等偏上`。
   - 理论部分不如正式 FATES 论文系统，但对工具现状、问题分解与未来工作讲得非常细。
2. **实现可获取程度**
   - 适合评为 `🟧 可获得工具版本但源码情况不清`。
   - 论文明确说 `T-UPPAAL` 版本已对外发布、可下载试验脚本，但从当前材料无法确认当时是否也公开了完整源码；因此不能直接写成“源码可得”。
3. **材料质量**
   - 这篇条目很适合用来补 testing 分支的“技术路线与开放问题”维度，而不是当作单纯算法论文来读。

## 对本研究的启发

这篇论文对当前博士研究很有价值，因为它提醒我们：**一个闭环平台一旦真正接近真实系统，难点会迅速从“主算法”转移到 coverage、诊断、接口、时间不确定性和数据通路。**

直接可借鉴的点有：

1. 若将来做 `LLM` 生成模型的在线验证，也应及早把 simulator 和 oracle 分开思考。
2. coverage 与 diagnostic information 不应是“以后再说”的附件，而应设计成闭环的一部分。
3. 工业测试接口与模型时间精度不匹配，会直接影响理论方法的可落地性。
4. 路线图型论文虽然不产出新定理，但非常适合用来把一条技术分支的未竟问题系统入账。
