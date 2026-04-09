# 使用 TorXakis 做模型驱动测试：重访 Dropbox 之谜 / Model-Based Testing with TorXakis: The Mysteries of Dropbox Revisited

## 基本信息

- 标题：Model-Based Testing with TorXakis: The Mysteries of Dropbox Revisited
- 中文标题：使用 TorXakis 做模型驱动测试：重访 Dropbox 之谜
- 作者：Jan Tretmans，Piërre van de Laar
- 发表：*Proceedings of the Central European Conference on Information and Intelligent Systems*，pp. 247-258，2019
- DOI：原文未给出 DOI
- 链接：https://archive.ceciis.foi.hr/public/conferences/2019/Proceedings/QSS/QSS3.pdf
- 形式主义：`IOLTS / symbolic transition systems / ioco / TorXakis`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：面向数据化交互系统的 symbolic-`ioco` 在线模型驱动测试工具与建模流程
- 工具/实现获取方式：论文明确给出 `TorXakis` 的公开实现与示例仓库，即 `https://github.com/TorXakis/TorXakis` 与对应 examples 目录。
- 标准/格式获取方式：主承载是 `TorXakis` 自有建模语言、channels、ADT、connections、encodings/decodings，以及 `SMT-LIB` 接口下的 `Z3/CVC4` 约束求解链；不是中立交换标准。

## 简报

这篇论文的重点，不是再解释一遍 `ioco` 理论本身，而是把 `ioco` 推广到带数据的 symbolic transition systems，并把这一整条在线测试链落成 `TorXakis`。相比更早的 `TorX/JTorX`，`TorXakis` 的关键增量在于：模型语言本身更完整，数据保持符号化而不是全部枚举展开，同时用 `SMT` 求解器负责测试数据生成，因此更适合像 Dropbox 这样的分布式、数据化、黑盒同步服务。

- 形式主义定位：基于 `ioco/sioco` 的在线模型驱动测试方法与工具，而不是新的状态机本体。
- 构造方式简述：先用 `TorXakis` 语言写 channels、ADT、process algebra 模型和 adapter 连接关系，再用 symbolic transition systems + `SMT` 求解做 on-the-fly test generation。
- 基础设施与场景简述：依托 `LOTOS` 风格进程代数、ADT、`Z3/CVC4`、socket-based adapter、`ioco/sioco` 一致性关系，服务协议、同步服务和一般交互式黑盒系统测试。

```text
symbolic model + connections/encodings -> STS semantics + SMT solving -> on-the-fly test generation -> adapter-mediated execution -> ioco-based verdict
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTS` 与 `ioco` 一致性理论。
2. `STS` 与 `sioco`，用于处理带数据和数据相关控制流的系统。
3. `TorXakis` 的 process-algebraic modeling language。
4. connections、encodings/decodings 与 sockets/adapter。
5. Dropbox 这类分布式文件同步服务的黑盒测试流程。

### 核心抽象

论文明确把 `LTS` 作为语义底盘。可保守整理为：

$$
M = (S, s_0, L_I, L_O, \to)
$$

上式中的符号逐项解释如下：

1. `$S$` 是状态集合。
2. `$s_0$` 是初始状态。
3. `$L_I$` 是输入动作集合。
4. `$L_O$` 是输出动作集合。
5. `$\to$` 是带标签迁移关系。
6. 这是论文讨论 `ioco` 时所依赖的标准 `LTS/IOLTS` 骨架。

论文给出的核心一致性关系是：

$$
i \mathrel{\mathrm{ioco}} s \iff \forall \sigma \in \mathrm{Straces}(s): \mathrm{out}(i\ \mathrm{after}\ \sigma) \subseteq \mathrm{out}(s\ \mathrm{after}\ \sigma)
$$

上式中的符号逐项解释如下：

1. `$i$` 是 implementation，也就是被测系统。
2. `$s$` 是 specification 模型。
3. `$\sigma$` 是 specification 允许的 suspension trace。
4. `$\mathrm{out}(x\ \mathrm{after}\ \sigma)$` 表示系统 `$x$` 在执行完 `$\sigma$` 后可能给出的输出集合，包括 quiescence。
5. 子集关系表示实现不能产生规格不允许的输出。

对 `TorXakis` 真正新增的 symbolic layer，可保守写成单步转移：

$$
s \xrightarrow{a,\phi,\theta} s'
$$

上式中的符号逐项解释如下：

1. `$a$` 是动作标签。
2. `$\phi$` 是关于数据的 guard/constraint。
3. `$\theta$` 是赋值或数据更新。
4. `$s,s'$` 是抽象状态。
5. 这表示 `STS` 把数据约束和数据更新叠加到了 `LTS` 的控制流骨架上。
6. 论文明确说明 `STS` 只是符号化表示，不增加语义表达力，而是让大或无限状态空间可处理。

Dropbox 模型在文中还给出了非常具体的状态骨架，可整理为：

$$
\mathrm{state}_{dbx} = (serverVal, conflicts, localVal, fresh, clean)
$$

上式中的符号逐项解释如下：

1. `serverVal` 是服务端当前稳定文件值。
2. `conflicts` 是冲突文件值集合。
3. `localVal` 记录各节点的本地文件值。
4. `fresh` 记录各节点是否已下载最新服务端值。
5. `clean` 记录各节点最近的本地改写是否已上传。
6. 这组变量正是论文中 `dropbox` 递归进程的状态参数。

### 一个最小例子与通俗解释

论文中的 Dropbox 例子很适合说明 `TorXakis` 的工作方式：

1. 论文把系统缩成 `3` 个 node 和 `1` 个 server。
2. 测试器对每个 node 只发三类命令：`Read`、`Write(value)`、`Stabilize`。
3. 模型里真正的上传/下载动作 `Up0/Down0/...` 是隐藏动作，因为黑盒用户看不到它们。
4. `TorXakis` 在运行时一边生成下一步测试动作，一边通过 adapter 把抽象命令变成 socket 上的真实消息。
5. 如果某个 node 在“稳定后”给出的文件集合不满足规格，则根据 `ioco/sioco` 直接判 fail。

通俗地说，`TorXakis` 像一个“会边测边想的测试器”。它不是先离线列出整套测试脚本，而是根据当前模型约束、当前观察到的 SUT 响应和 `SMT` 求解结果，实时决定下一步该发什么、期待什么。

### 运行 / 接受 / 转移语义

论文强调 `TorXakis` 是 on-the-fly MBT 工具，也就是测试生成和执行不分离。其运行骨架可保守整理为：

$$
c_{k+1} = \mathrm{step}(c_k, model, sut, solver)
$$

上式中的符号逐项解释如下：

1. `$c_k$` 是第 `$k$` 步测试上下文。
2. `model` 是 `TorXakis` 模型及其当前符号状态。
3. `sut` 是通过 adapter 接入的真实被测系统。
4. `solver` 是 `Z3` 或 `CVC4` 之类的约束求解器。
5. 每执行一步，工具都会立刻消费实际观测并生成下一步。

论文对模型文件结构的描述也可以压成：

$$
\mathrm{ModelFile} = (\mathrm{ChanDef}, \mathrm{TypeDef}, \mathrm{FuncDef}, \mathrm{ProcDef}, \mathrm{Connection}, \mathrm{Encoding})
$$

上式中的符号逐项解释如下：

1. `ChanDef` 定义输入输出通道。
2. `TypeDef` 定义 ADT。
3. `FuncDef` 定义函数与约束。
4. `ProcDef` 定义进程代数模型。
5. `Connection` 规定抽象通道到真实 sockets 的绑定。
6. `Encoding` 规定 ADT 与字符串之间的映射。
7. 这正是论文在 “Model” 小节中给出的建模结构。

### 语义边界

1. `TorXakis` 仍然是黑盒测试框架，默认实现满足 input-enabled 的 testability hypothesis。
2. 它主要处理离散交互和符号化数据，不涉及连续动力学。
3. 实际可测性高度依赖 adapter 质量；GUI 或复杂异步接口往往需要额外包装。
4. sockets 是异步通信，而模型常假定同步交互，因此若模型在输入/输出之间存在 race，用户需要显式把队列或异步层建进模型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `LTS/IOLTS` 骨架 | `$M = (S, s_0, L_I, L_O, \to)$` | `ioco` 理论的基础对象。 |
| 一致性关系 | `$i \mathrel{\mathrm{ioco}} s \iff \forall \sigma \in \mathrm{Straces}(s): \mathrm{out}(i\ \mathrm{after}\ \sigma) \subseteq \mathrm{out}(s\ \mathrm{after}\ \sigma)$` | `TorXakis` 最终判的就是这个关系。 |
| `STS` 单步 | `$s \xrightarrow{a,\phi,\theta} s'$` | 数据与控制流被一起符号化。 |
| Dropbox 状态参数 | `$\mathrm{state}_{dbx} = (serverVal, conflicts, localVal, fresh, clean)$` | 论文示例的真实模型骨架。 |
| on-the-fly 运行 | `$c_{k+1} = \mathrm{step}(c_k, model, sut, solver)$` | 测试生成与执行在同一循环中进行。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 模型根基仍是 `LTS/STS` 状态空间。 |
| 事件 / 触发 | 很强 | 输入、输出、quiescence 与隐藏动作都是核心。 |
| 守卫 / 数据 | 很强 | `STS` 与 `SMT` 让数据约束成为一等对象。 |
| 层次 | 弱支持 | 论文主体不是层次状态机，而是进程代数组合。 |
| 并发 / 同步 | 很强 | 进程代数、并行组合与分布式 Dropbox 模型是重点。 |
| 时间约束 | 不支持 | 本文不是 timed testing 路线。 |
| 连续动态 / 随机性 | 不支持 | 不在主线范围内。 |
| 可执行 / 可验证性 | 很强 | 支持 on-the-fly generation、execution、constraint solving 与 verdict。 |

### 形式化问题与性质

1. 与 `TorX/JTorX` 相比，这篇论文的关键贡献不是 UI，而是把数据保持在符号层，并让 `SMT` 接管 test-data generation。
2. 论文展示 `TorXakis` 可以同时处理 nondeterminism、partial models、under-specification 和 concurrency。
3. 对本文库来说，它很适合挂到 `TorX / JTorX / TESTOR` 这一条 `ioco` 工具链上，作为“数据化、进程代数化”版本的扩展节点。

## 构造方式与承载格式

### 建模入口

论文给出的建模入口包括：

1. `TorXakis` 自有建模语言。
2. channels、ADT、functions、constants 和 processes。
3. connections 与 encodings/decodings。
4. 对真实 SUT 的 adapter。

### 机器可处理承载方式

机器可处理承载方式包括：

1. process-algebraic `TorXakis` 模型文件。
2. symbolic transition systems。
3. `SMT-LIB v2.5` 接口下的约束。
4. line-based socket messages。
5. 由 adapter 暴露的抽象输入输出通道。

### 交换与互操作

这条路线的互操作重点是：

1. 把抽象 channels 绑定到 concrete sockets。
2. 把抽象 ADT 消息编码到字符串，再从字符串解码回来。
3. 通过 adapter 重用现有自动化测试基础设施，而不是要求 SUT 原生支持 `TorXakis`。

## 配套基础设施

- 建模/编辑工具：`TorXakis` 文本建模语言与 examples 仓库。
- 解析/交换/元模型支持：channels、ADT、connections、encodings/decodings、socket bindings。
- 仿真/执行支持：on-the-fly 测试执行、socket 通信、adapter/harness。
- 验证/分析支持：`ioco/sioco` 一致性判定、隐藏动作、nondeterminism、partial/underspecified models。
- 代码生成/转换支持：不是面向部署代码生成，重点是 symbolic unfolding 与 test-step generation。
- 标准化或社区生态：`Haskell` 核心实现，`Z3/CVC4`、`SMT-LIB`、QuickCheck 辅助测试共同构成工具生态。

## 适用场景与需求前提

### 适用场景

适合以下任务：

1. 协议、服务和分布式同步系统的黑盒一致性测试。
2. 需要同时保留控制流和数据约束的模型驱动测试。
3. 已有自动化测试 harness，希望升级为 formal MBT 的系统。

### 需求前提

1. 系统行为要能抽象成输入输出通道与离散动作序列。
2. 数据约束要能表达成一阶逻辑/SMT 可处理形式。
3. 团队能接受 process algebra 风格建模，而不是纯图形状态图。
4. SUT 最终需要能通过 adapter 接到 socket 风格接口上。

### 不适用或高成本场景

1. 若系统核心问题在 dense time 或连续物理演化，这篇论文的 `TorXakis` 版本不是最合适入口。
2. 若 SUT 很难适配到可编程 adapter，落地成本会偏高。
3. 若团队只想要轻量脚本测试而不愿维护 formal model，这条路线的前期投入会偏大。

## 与相邻形式主义的关系

相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，`TorX` 是更早的 `ioco` 在线测试母线，主要围绕 `Explorer/Primer/Driver/Adapter` 骨架；`TorXakis` 则把数据保持在符号层并加入自有建模语言。相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，`JTorX` 更偏开放接口与教学友好的 `IOLTS` 工作台，而 `TorXakis` 更强调 process algebra、ADT 和 `SMT`。相对 [testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md](../testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md)，`TESTOR` 更偏 `CADP` 生态下的模块化 `ioco` 测试生成，而 `TorXakis` 更偏数据化建模与服务接口测试。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明如果 LLM 最终能生成带数据约束的交互模型，那么后续测试不必退回人工脚本，而可以直接走 symbolic MBT。
2. connections/encodings 这套分层也很有启发，因为它把“抽象模型”和“真实接口”明确拆开了。
3. 对闭环研究来说，`TorXakis` 提供的是一类非常实际的失败证据来源：真实 SUT 与形式模型之间的在线不一致。

### 作为目标形式主义还是中间表示

更像测试与验证侧的中间表示及其执行框架，而不是最终交付给领域工程师的状态机语言。

### 对需求到模型生成的启发

1. 若需求天然包含输入输出契约和数据约束，生成模型时应尽早保留 `I/O + guard + data` 结构。
2. 生成阶段最好把 environment assumptions 与 under-specification 显式化，否则测试阶段很难界定 fail/inconclusive。
3. 抽象模型与具体接口之间需要有显式 encoding layer，这一点不能靠测试时临时补。

### 现实限制

`TorXakis` 对 adapter 和形式建模的要求较高，但正因为这层要求存在，它能比“只会录制回放”的测试框架提供更强的可解释性和覆盖能力。

## 重要的相关工作

1. [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：更早的 `ioco` 在线测试母线。
2. [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：开放接口更成熟的 `IOLTS` 在线测试工作台。
3. [testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md](../testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md)：`CADP` 生态下的在线一致性测试工具。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 归类理由：论文主体是 `ioco/sioco` 驱动的 symbolic 在线测试方法与 `TorXakis` 工具链，而不是新的交互模型本体，因此适合归入 `📦/🛠️`。
