# Statistical Model Checking for Networks of Priced Timed Automata

- 问题一句话：`NPTA` 的 reachability 与性能分析大多不可判定，经典实时模型检查无法同时表达概率、时间和代价性能。
- 方法一句话：为 `NPTA` 定义基于组件竞速的随机语义，提出 `PWCTL` 查询与随机运行生成算法，并以统计模型检查近似求解。
- 解决点一句话：把 `UPPAAL SMC` 从工具原型推进到以 `NPTA + race semantics + PWCTL` 为核心的正式理论与算法框架。

## 论文定位

这篇论文在 `uppaal_tech/` 里属于 `⚡ 改进与扩展`，而且是 `UPPAAL SMC` 支线中的**核心理论条目**。如果说 [david11-statistical-model-checking-real-time](./../david11-statistical-model-checking-real-time/) 更像是宣布 `UPPAAL` 已经开始支持统计模型检查的工具/方向论文，那么本文则把这一方向推进到更严整的对象、语义、逻辑和算法层。

它的核心对象是 `Networks of Priced Timed Automata`，这比普通 timed automata 更强，因为：

1. 时钟或连续变量可以具有位置相关速率。
2. 成本可以通过 observer clock 或 rate 自然表示。
3. 多组件网络通过输入/输出广播组合。

文章的位置可以概括为：它把 `UPPAAL SMC` 从“能做一些概率实验”推进成了“对 `NPTA` 进行概率-时间-代价联合分析的正式框架”。

## 立足问题

这篇论文面对的问题比上一年的 `SMC` 工具展示文更尖锐。作者选择的对象 `NPTA` 非常强大，甚至在表达能力上可达到一般 linear hybrid automata 的水平。因此很多经典问题，包括 reachability，本身就是不可判定的。

但工程上，人们真正关心的常常不是单纯的“最坏情形能否在边界内到达”，而是更细的性能问题：

1. 某目标在时间上界 `c` 内达到的概率是多少。
2. 以资源/能耗为 observer cost 时，预算内成功的概率是多少。
3. 两个设计虽然 worst-case 一样，但谁在常见运行下更快、更省、更可靠。

经典 `UPPAAL` 的 timed model checking 路线，擅长给出硬保证，却不擅长回答这些 refined performance questions。另一方面，若只是把系统乘成一个大 product，再套已有 timed/probabilistic semantics，又会丢掉组件独立性的关键信息，尤其是“谁先发出输出”这种 race 行为。

因此，这篇论文真正盯住了三个技术瓶颈：

1. 如何为由多个 priced timed 组件组成的网络定义一个**忠实反映组件独立竞速**的随机语义。
2. 如何在此语义下表达同时涉及概率、时间和代价的性质。
3. 当判定问题本身不可判定时，如何通过 `SMC` 给出可控置信度的近似答案，并且保持与 `UPPAAL` 既有建模方式兼容。

## 核心方法

这篇论文的方法主轴，可以拆成“建模对象层、随机语义层、逻辑层、采样算法层、统计比较层”五层。

### 1. 建模对象层：从 `PTA` 到 `NPTA`

作者先定义 `Priced Timed Automaton`：

$$
A = (L, \ell_0, X, \Sigma, E, R, I).
$$

其中最重要的新点是 `R`：

$$
R : L \to \mathbb{N}^{X}
$$

它给每个 location 上的每个 clock 指定演化速率。因此 valuation 在延时 `d` 后的变化不再是简单的 `\nu + d`，而是：

$$
\nu + R(\ell) \cdot d.
$$

这意味着 clock 不只是“每单位时间加 1”的标准时钟，也可以拿来编码成本、能耗或其他线性累积量。多个 `PTA` 再通过输入/输出广播组合成 `NPTA`。这一步继承了作者在 `TIOA` 方向上对 input-enabled、deterministic、broadcast communication 的习惯。

### 2. 随机语义层：不是给 product 随机化，而是给组件 race 随机化

这是全文最关键的方法点。作者没有把随机性简单附加在 product automaton 上，而是先在**单个组件**层面定义：

1. 延时分布 `\mu_s`
2. 输出选择分布 `\gamma_s`

然后在网络层面通过 race 组合。

具体地说，对状态 `s = (\ell, \nu)`：

1. 若 invariant 给出了有限上界，则延时在允许区间上按 uniform 选择。
2. 若延时上界不存在，则采用 exponential distribution。
3. 输出动作则在当前可用输出集合上按 uniform 选择。

随后，每个组件独立选择自己下一次输出前要等待多久，最终系统执行最小延时对应的那个组件输出；其余组件只被动接收该广播并更新状态。

这一步的本质是：**概率不是在全局 product 上事后指定，而是由各组件独立选择延时与输出后，通过最小延时竞赛诱导出来。**

这使得网络语义保留了组件独立性，而不是把一切都糊成单一 product 后失去结构信息。

### 3. 概率逻辑层：用 `PWCTL` 表达概率-时间-代价约束

在随机语义之上，论文引入非嵌套的 `PWCTL` 查询。其代表形式是：

$$
P(\Diamond_{C \le c} \varphi) \sim p
$$

以及

$$
P(\Box_{C \le c} \varphi) \sim p.
$$

这里：

1. `C` 是 observer clock，可以是时间，也可以是代价。
2. `c` 是边界。
3. `\varphi` 是状态谓词。
4. `\sim p` 表示与阈值比较。

论文特别强调，这个逻辑是对经典加权实时逻辑的保守概率扩展。也就是说，原先非随机系统里能表达的 hard real-time bounded property，在这里不是被推翻，而是被细化成“在边界内以多大概率满足”。

### 4. 采样算法层：给 `NPTA` 设计与随机语义一致的随机运行生成算法

有了网络随机语义后，必须真能按该语义抽样。作者因此给出随机运行生成算法。其基本过程是：

1. 从当前网络状态出发。
2. 对每个组件按 `\mu_s` 采样候选延时。
3. 取其中最小值 `d` 作为下一次全局延时。
4. 若 observer clock 在这之前就会撞上边界，则截断运行。
5. 否则由赢得 race 的组件执行输出，广播给其他组件，同步更新网络状态。
6. 重复直到达到时间/代价边界。

这套算法并不是普通随机仿真小技巧，而是整篇论文的 operational core，因为后面的所有统计推断都建立在“采样分布与正式语义一致”之上。

### 5. 统计判定层：在不可判定前提下做 qualitative、quantitative 与 comparison

既然 `NPTA` 的许多问题本身不可判定，作者明确转向 `SMC`。这里依然保留了 `UPPAAL SMC` 主线的三类任务，但做得更系统。

#### 5.1 定性阈值检验

判断：

$$
P(\Diamond_{C \le c} \varphi) \ge \theta
$$

是否成立。方法依旧是 Wald 序贯假设检验，用误判参数与 indifferent region 控制决策质量。

#### 5.2 定量概率估计

通过 Chernoff-Hoeffding 边界确定所需样本数，给出：

$$
[p - \varepsilon, p + \varepsilon]
$$

形式的置信区间。

#### 5.3 概率比较与参数化比较

这是本文很有特色的一部分。作者不满足于“先分别估计两个概率，再拿两个区间比较”，而是直接比较：

$$
p_1 = P_A(\Diamond_{C_1 \le c_1} \varphi_1), \qquad p_2 = P_A(\Diamond_{C_2 \le c_2} \varphi_2).
$$

并引入相对优势比：

$$
u = \frac{p_2 (1 - p_1)}{p_1 (1 - p_2)}.
$$

再通过扩展的 Wald 测试直接判断谁更优。更进一步，论文还提出参数化比较，把同一批运行复用于多个时间/代价边界，从而显著减少总采样成本。这一点对画出整条性能曲线尤其重要。

### 6. 一个特别关键的差异层：timed bisimilar 不等于 probabilistically equivalent

这篇论文里一个很值得记住的洞见是：在其网络随机语义下，两个 timed bisimilar 的模型也可能在概率意义上不同。原因不是语义出错，而是 network race semantics 保留了组件独立性，而 product semantics 会把这种独立性压扁。

也就是说，本文方法强调的不是“随机化任何 timed automata”，而是“在保持组件结构与竞速机制的前提下做随机化”。这正是它比普通 product-based 概率解释更强的地方。

## 解决了什么问题

这篇论文解决的是 `UPPAAL SMC` 支线从“可用”到“成体系”的关键问题。

第一，它给 `NPTA` 提供了正式、自然且结构保持的随机语义。没有这一步，后续概率查询就很容易变成 ad hoc 仿真，而不是严整的 formal analysis。

第二，它定义了 `PWCTL`，从而把时间边界、代价边界与概率比较统一进一个查询层。这使 `UPPAAL` 不再只问 reachability / safety 是否成立，而能问“以多大概率、在多大成本下成立”。

第三，它给不可判定问题提供了系统性的 `SMC` 替代方案，并把运行生成、阈值检验、概率估计、概率比较、参数化重用一整套流程接了起来。

第四，它清楚说明了为何网络级随机语义不能简单替换成 product 级随机语义，从理论上守住了组件化建模的独立性。

当然，边界也很明确：

1. 结果是统计近似，不是精确判定。
2. 查询主要还是 bounded、非嵌套性质。
3. 模型虽强，但越强也意味着采样与置信收敛成本可能更高。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系非常直接。

向前，它建立在：

1. 经典 `UPPAAL` 的 timed automata 建模与分析传统。
2. [david11-statistical-model-checking-real-time](./../david11-statistical-model-checking-real-time/) 提出的早期 `SMC` 工具方向。
3. `TIOA`/广播组合等更强调组件交互的建模习惯。

向后，它对后续几条线都有直接影响：

1. [david12-statistical-model-checking-stochastic-hybrid-systems](./../david12-statistical-model-checking-stochastic-hybrid-systems/) 这类更广的随机混杂系统扩展。
2. [david15-uppaal-smc-tutorial](./../david15-uppaal-smc-tutorial/) 等系统化整理 `UPPAAL SMC` 的教程和综述。
3. 后续关于策略、期望代价、学习与优化的工作，也都能从这里的 observer cost 与概率比较视角找到源头。

若从 `UPPAAL` 的主线分类，它最靠近：

1. `SMC`
2. `priced / cost-aware timed models`
3. `network-level stochastic semantics`

## 实现与材料

这篇论文的材料整体很强，尤其适合做技术梳理，因为它同时给出：

1. `PTA/NPTA` 的形式定义
2. 网络随机语义的构造思路
3. `PWCTL` 的查询语义
4. 随机运行生成算法
5. 多类 `SMC` 统计算法
6. `UPPAAL` 工具实现与多个案例

从内容详细程度看，它已经接近“可据此重建主要方法框架”的档位。虽然仍不是完整代码级说明，但语义对象、算法输入输出和关键统计步骤都讲得比较清楚。

从实现可获取角度看，论文明确依托 `UPPAAL` 的随机扩展实现。也就是说，工具层面是明确存在的；但若要求源码级完全复现，仍需结合具体版本代码与后续文档。

## 对本研究的启发

对当前博士研究，这篇论文最重要的启发有三点。

第一，它说明“形式验证”不必只围绕离散真值，而可以自然扩展到“时间-代价-概率”三维联合分析。这对控制系统状态机尤其重要，因为很多工程问题真正关心的是是否**大概率及时完成且成本可控**。

第二，它非常强调结构保持的语义。对我们以后用 LLM 生成多组件状态机时，这一点很关键：如果把所有结构都拍扁成一个大 product，再做分析，很多交互责任和并发机制会被掩盖。

第三，它的参数化比较思路值得借鉴。对自动建模系统来说，比较“原模型与修复模型谁更好”通常比孤立计算一个概率更有价值，而本文已经提供了直接比较两种性质/两种设计的技术范式。
