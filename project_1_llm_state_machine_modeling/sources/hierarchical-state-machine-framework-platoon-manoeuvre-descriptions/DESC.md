# 车队 JoinTail 机动的分层状态机描述框架 / A Hierarchical State-Machine-Based Framework for Platoon Manoeuvre Descriptions

## 论文在讲什么

这篇论文讨论的是自动驾驶车队机动如何用分层状态机统一描述。作者的出发点是：现有 platoon manoeuvre 文献大多用多个相互同步的状态机分别描述不同车辆角色，结果导致可读性差、细节层级不统一、相同行为的叫法也不统一。为了解决这些问题，论文提出了 `SEAD` 框架，用层次化、可复用的方式来组织 platoon layer 中的 manoeuvre。

虽然整篇论文带有明显的方法框架色彩，但它不是空泛地讲“可以这样建模”。论文用 `JoinTail` 这样的具体机动作示例，从 join request、leader 应答、移向队尾、attach、切入 `CACC` 跟驰，到 join-complete 回报与 leader 更新 platoon information，都给出了可追溯的流程说明。再往后，作者又把这些流程拆成 stable / unstable idle state、sub-manoeuvre、idle super-state、`RSM` 和 `PME` 等层次结构，使得这个样本既有具体机动逻辑，也有清晰的 HSM 组织方式。

## 控制系统在文中的位置

我们关心的控制系统描述在这篇论文里既是研究对象，也是方法载体。也就是说，论文整体确实在做 manoeuvre-description framework，但它不是通过一个模糊例子来演示框架，而是把 platooning manoeuvre 本身当作需要被规范化、模块化和稳定化的控制对象来写。`JoinTail` 不是装饰性案例，而是验证框架合理性的核心样例之一。

对 `sources/` 来说，这一点很重要。很多“框架论文”最后只能留下概念层背景材料，但这篇文章之所以能收进来，是因为它已经把车辆角色、状态、消息原语、成功/中止路径和 timeout 触发后的稳定落点写得足够具体。换句话说，它虽然是方法论文，但其中的 `JoinTail` 控制描述已经足够独立，能直接支持状态机数据集抽取。

## 对我们为什么有用

这篇论文最大的价值，是补了 `🚗` 领域里很少见的 `HSM + T1 + 协议交互` 样本。现有车队编入流程里常见的是较平面的 protocol 描述，而这篇论文把角色状态机、层次 idle state、sub-manoeuvre 封装、`RSM/PME` 分离以及 timeout-abort 稳定化链条都放到了同一个案例里，因此结构丰富度明显更高。

它还帮助我们覆盖“方法论文中的高质量控制案例”这一类边界情况。后续如果模型只学会处理那种纯工程实现文献，遇到这种既有框架组织又有具体协同行为的文本时可能会丢失层次结构；而这篇论文正好能提供一条很清楚的示范，让数据集同时覆盖平面 FSM 和真正的 hierarchical manoeuvre description。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `3-4` 页围绕 `JoinTail` 的说明和 `Figure 2 / Figure 3`，先把“单次车队编入到底发生了什么”读清楚。第一轮只需要抓 join request、ack/reject、移动到 platoon tail、attach、切入 `CACC`、join-complete 回报这条主链，不必一上来就钻进 `SEAD` 全部术语。

然后再跳到第 `7-10` 页，重点读 `Framework overview`、`Formulating sub-manoeuvres`、`Formulating manoeuvres`、`Idle states and super-states`、`RSM` 和 `PME` 这些部分。这里的阅读目标是确认三件事：层次结构怎么搭起来；消息原语和角色子状态机如何同步；timeout/abort 如何把车辆带回稳定 idle state。`MDL` 语法、未来工作和更泛的 mixed traffic 讨论都可以放到第二轮再看。
