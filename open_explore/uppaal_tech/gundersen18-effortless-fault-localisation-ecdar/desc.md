# Effortless Fault Localisation: Conformance Testing of Real-Time Systems in Ecdar

- 问题一句话：`Ecdar` 已能做 timed specification refinement，但若不能把它直接变成对真实实现的 conformance testing 与 fault localisation 工作流，工业落地仍然不够。
- 方法一句话：论文把 model-based mutation testing 集成进新版 `Ecdar` IDE，继续使用 `TIOA` refinement / angelic-demonic completion 生成 adaptive test cases，并新增 primary fail、并行生成执行与 real-time / simulated-time 双模式测试。
- 解决点一句话：它把 `Ecdar` 从“只会做规约验证”推进成“建模、验证、测试、定位故障一体化”的工具环境。

## 论文定位

这篇论文在 `uppaal_tech/` 中更适合归到 `🛠️ 工程/工具链`。它并不是重新发明 `ECDAR` 的 specification theory，而是把已有 timed refinement / mutation-based testing 能力正式接进一个 IDE 级工具工作流。

与 [nyman17-mutation-based-test-case-generation-ecdar](../nyman17-mutation-based-test-case-generation-ecdar/) 的关系尤其紧密：

1. 后者更偏“如何用 `ECDAR` 的 unbounded refinement 生成 adaptive mutation tests”；
2. 本文则继续把这件事整合进 `Ecdar` 新 IDE，并把 fault localisation、并行执行和 real-time testing 一起做进来。

所以它是一篇典型的“方法工程化与工具一体化”论文。

## 立足问题

对于 safety-critical real-time systems，仅有“模型已验证正确”是不够的。论文在引言中很清楚地区分了两件事：

1. design correctness
2. implementation correctness

`Ecdar` 之前更偏前者，即基于 timed I/O automata 做 compositional verification、refinement、quotient 等分析。但如果要进入真实开发流程，人们还需要一种高生产率、低手工负担的测试方式，去检查 SUT 是否真的符合那个已验证的模型。

这里的问题不是简单的“做一些 test cases”，而是：

1. 希望只提供 test model 和 SUT，不再额外写 environment model、TCTL property 或 monitoring automata；
2. 希望测试不仅能发现 fault，还能帮助**定位 fault**；
3. 希望既支持真实时间执行，也支持模拟时间快速回放；
4. 希望工具不只给理论方法，而是放进一个 IDE 工作流里。

因此，本文真正盯住的是：**如何把 `Ecdar` 的 refinement-based mutation testing 变成一套实际可操作、能帮助 fault localisation 的完整工具体验。**

## 核心方法

论文的方法大致沿着 mutation -> test-case generation -> test execution 三段推进，但重点在于把这些步骤都收进同一个 `Ecdar` 工具环境里。

### 1. 继续以 `TIOA` / `TIOTS` / refinement 作为理论底盘

文章没有换掉 `ECDAR` 的形式化核心，依旧以 `Timed I/O Automata` 和其语义 `TIOTS` 为基础。它回顾了：

1. determinism
2. input-enabledness
3. refinement

这意味着 testing 不是一条与 verification 平行、互不相干的支线，而是继续建立在 `Ecdar` 原有 specification theory 上。

### 2. 以 `MBMT` 组织测试工作流

与前一篇 `nyman17` 一样，本文仍然把 model-based mutation testing 作为主框架：

1. 从 test model 出发生成 mutants；
2. 检查 mutant 是否 refinement 于 test model；
3. 若不 refinement，则从反例中提取 test case；
4. 把 test case 跑在 SUT 上。

但本文更进一步，直接把这件事集成进 `Ecdar` 界面，让使用者不必在多个工具之间来回切换。

### 3. 在 mutation operators 上继续扩展，使 fault detection / localisation 更强

论文列出了相当丰富的一批 mutation operators，不只继承旧操作，还新增若干对 timing、guard operator、input/output、variable update 更敏感的变异方式。例如：

1. 把 action 改成另一输入 `M_i`
2. 改 guard constant `M_gc`
3. 改 guard operator on clock `M_goc`
4. 改 guard operator on variable `M_gov`
5. 改 variable update `M_vu`

新增这些 operator 的目的不是“种类越多越好”，而是让模型中的 fault space 更贴近真实实现中的常见错误，并在 case study 里提高 fault detection 与 localisation 的能力。

### 4. 对 test model / mutant 分别做 demonic 与 angelic completion

在 test-case generation 阶段，作者继续沿用 `ECDAR` 系列一贯的 completion 规则：

1. test model 做 demonic completion；
2. mutant 做 angelic completion。

这一步的直觉是：

1. 规格中未写出来的输入行为，不应默认一律判错，因为那可能只是模型没有覆盖到；
2. mutant 这边则应尽量不因为“少了某个输入边”而无谓地阻断测试。

完成这一步后，再用 `Ecdar` engine 做 refinement check。若 `T \nleq S`，引擎会返回 strategy。由于 `Ecdar` 的 refinement check 本身就是 timed game，所以得到的 test case 也天然是 adaptive 的。

### 5. 引入 primary fail，把“发现错误”进一步升级成“定位错误”

本文最有辨识度的新增点之一，是 primary fail。

普通 testing 里，`fail` 只告诉你“实现不符合规格”；但对调试来说，人更希望知道：

1. 这个 fail 是否正好与某个具体 mutant 对应；
2. 能否据此快速猜到 fault 的位置和类型。

论文的做法是：

1. 在测试时同时模拟 test model 与 mutant；
2. 若 test model 不能跟随 SUT 行为而 mutant 可以，则这是普通 fail；
3. 若 fail 还能明确对应到某个 mutant 所代表的 fault，则标成 primary fail。

这就让测试从单纯“抓 bug”推进到了“给 debug 提供指向性线索”。

### 6. 把 test execution 做成 real-time 与 simulated-time 双模式

为了覆盖真实物理系统和快速软件回放两类场景，论文给 test driver 提供了两种时间模式：

1. **real-time**
   - 真正等待物理时间流逝，适合测试实体系统。
2. **simulated-time**
   - 由 driver 告诉 SUT 允许模拟多长 delay，SUT 返回实际模拟的 delay，显著加速执行。

这一步很重要，因为许多 testing 论文只给理论方法，真正落地时却卡在“物理时间太慢”。本文则把这件事显式纳入工具设计。

### 7. 并行化 test-case generation 与 test execution

论文还明确讨论了性能问题：

1. generation 端可多线程并行调用 `Ecdar` engine；
2. execution 端在允许时也可并行跑多个 SUT 实例。

这说明作者在把方法真正往 IDE 产品化推进，而不是只停留在 demo 级实现。

## 解决了什么问题

这篇论文最重要的贡献，是把 `Ecdar` 从 specification-theory 工具推进成了真正的“建模 + 验证 + 测试 + fault localisation”一体化环境。

第一，它显著降低了测试配置负担。用户只要给 test model 与 SUT，不必再额外写复杂环境模型或监控自动机。

第二，它通过 primary fail 把测试结果和具体 fault 类型更紧地连接起来，使 `Ecdar` 不只是告诉你“错了”，而是更接近告诉你“错在哪一类地方”。

第三，它支持 real-time 与 simulated-time 两种执行模式，使工具既能对接物理系统，也能快速做软件回归。

第四，它证明 mutation operators 的扩展不是装饰：case study 中新 operators 确实提升了 fault detection 与 localisation 效果。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [david10-timed-io-automata-complete-specification-theory](../david10-timed-io-automata-complete-specification-theory/)
2. [david12-compositional-verification-ecdar](../david12-compositional-verification-ecdar/)
3. [nyman17-mutation-based-test-case-generation-ecdar](../nyman17-mutation-based-test-case-generation-ecdar/)

前两者提供 `ECDAR` 的规约理论和环境，第三者提供 refinement-based mutation testing 主线，本文则把它们收进实际工具。

### 它往后影响了谁

它往后影响：

1. `ECDAR` IDE 工作流本身；
2. 更系统的 fault localisation / testing automation；
3. `UPPAAL` / `ECDAR` 生态里“verification 与 testing 一体化”的实践方向。

### 它更靠近哪条主线

它最靠近：

1. `ECDAR`
2. mutation-based testing
3. IDE-level testing integration

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - `TIOA`、mutation operators、generation / execution workflow、parallelization 和 case study 都讲得比较具体。
2. **实现可获取程度**
   - 更适合评为 `🟩 核心实现源码线直达`。
   - 论文明确写到 `Ecdar` 是 open-source IDE，并给出工具与 sample projects 入口；当前还能沿 [ECDAR](https://github.com/Ecdar/ECDAR) 与相关 org 仓库继续追源码线。
3. **材料价值**
   - 它是理解 `ECDAR` 如何从 verification 环境扩成 testing 平台的关键条目。

## 对本研究的启发

对当前博士研究，这篇论文的启发主要在“工具闭环”上。

第一，验证工具若要走向真实工作流，迟早要把 testing 与 debugging 拉进来。只停在 model checking 是不够的。

第二，测试结果最好尽量带 fault localisation 线索，而不是只给 yes/no。对未来做模型修复，这一点尤其重要，因为修复器最需要的正是“哪类元素最可疑”。

第三，simulated-time 与 real-time 双模式非常值得借鉴。很多闭环研究在原型阶段都依赖模拟，等落地时才补真实执行接口；本文说明这两者最好从一开始就在工作流里并列考虑。
