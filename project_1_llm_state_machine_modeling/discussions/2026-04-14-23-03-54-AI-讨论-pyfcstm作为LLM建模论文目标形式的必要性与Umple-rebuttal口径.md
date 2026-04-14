# `pyfcstm` 作为 LLM 建模论文目标形式的必要性、特殊性与 `Umple` rebuttal 口径

## 1. 这份讨论稿要回答什么

这份讨论稿只回答一个聚焦问题：

> 如果后续要以 `pyfcstm` 作为 `project_1` 中“从自然语言到状态机模型”的目标形式，并将其写进软件工程会议论文，那么 `pyfcstm` 的必要性、特殊性和学术贡献到底应该怎么讲；一旦 reviewer 或 rebuttal 把问题打到 `Umple` 上，应该如何稳定回应。

这里不再展开 `timeline`、连续时间场景验证等旁支，也不再把讨论重心放在“状态机家族全景比较”上。那些内容已经分别在以下讨论稿中展开：

1. [2026-04-05-22-39-29-AI-讨论-pyfcstm-形式化定位-差异化与工具链比较.md](./2026-04-05-22-39-29-AI-讨论-pyfcstm-形式化定位-差异化与工具链比较.md)
2. [2026-04-06-02-10-04-AI-讨论-状态机主要类型详细综述-历史沿革与近年趋势.md](./2026-04-06-02-10-04-AI-讨论-状态机主要类型详细综述-历史沿革与近年趋势.md)

本文的目标是把前面的分析收束成一套**论文可直接使用**的定位话术与 rebuttal 口径。

## 2. 先给总答案

最重要的结论只有一句：

> 论文里不应该把 `pyfcstm` 讲成“世界上不存在 `Umple` 这类工具，所以我们必须重新发明一门语言”；而应该把 `pyfcstm` 讲成一种**面向自然语言到层次控制模型任务的、文本优先、语义收敛、工具链闭环的目标形式**，它使 `LLM-based modeling from natural language` 从“表面文本生成”变成了“可解析、可执行、可验证、可评测的软件工程任务”。

换句话说：

1. `pyfcstm` 的必要性，不在于“别的工具完全做不了状态机建模”。
2. `pyfcstm` 的必要性，在于它为 `NL -> executable / verifiable control model` 提供了一个**任务形状匹配**的目标表示。
3. `Umple` 是重要相关工作，但它不自动替代 `pyfcstm` 在这个研究设置中的角色。

## 3. 论文到底应该怎么定位

### 3.1 不该怎么定位

最危险的写法是把论文定位成下面几种东西：

1. “我们提出了一门比 `Umple` 更强、更通用的 executable modeling language。”
2. “现有工作都做不了 executable modeling，所以我们必须做 `pyfcstm`。”
3. “`pyfcstm` 的形式化验证能力理论上超过 `NuSMV/nuXmv/Alloy`。”
4. “我们的主要贡献是重新发明状态机 DSL 本身。”

这些写法都不稳，因为 reviewer 很容易指出：

1. `Umple`、`SCXML`、`Sismic`、`P`、`itemis CREATE` 等都已经说明“可执行状态机建模语言/工具链”并不稀缺。
2. `NuSMV/nuXmv` 在通用形式化验证能力上限上显然更强。
3. 如果论文主问题是 `LLM-based modeling from natural language`，那么“又造一门语言”不是最自然的主要贡献。

### 3.2 应该怎么定位

更稳妥的定位方式是：

> 我们研究的不是“再造一个通用 executable modeling language”，而是“如何把自然语言中的控制逻辑稳定转化为可执行、可验证、可生成代码的形式模型”。为此，我们需要一个文本优先、语义明确、输出空间收敛、且能直接进入统一工程闭环的目标形式。`pyfcstm` 正是这个任务中的 target formalism / intermediate formal representation。

这一定义有四个关键词：

1. **文本优先**
2. **语义明确**
3. **输出空间收敛**
4. **工程闭环**

后文所有必要性和特殊性，本质上都围绕这四点展开。

## 4. `pyfcstm` 的必要性到底在哪里

### 4.1 这篇论文需要的不是“任意状态机语言”，而是“适合 LLM 生成的目标形式”

如果研究问题只是“人手建模时用什么工具舒服”，那么 `Umple`、`SCXML`、图形化 statechart 工具都可以讨论。  
但 `project_1` 的核心问题不是这个，而是：

> 如何让 `LLM` 从自然语言控制系统描述中，稳定地产出一个可以继续进入验证和代码生成链路的模型对象。

这时，目标语言必须同时满足下面四个条件：

1. **文本载体稳定**
   - 目标形式必须天然适合 LLM 逐 token 生成，而不是强依赖图形编辑器、坐标布局或复杂元模型编辑环境。
2. **语义边界明确**
   - 语言内部必须有足够清楚的语法和执行语义，使“生成是否正确”可以通过 parser、semantic validation、runtime replay 来判定。
3. **工程链路贯通**
   - 生成的对象不能只是“看起来像状态机”，而要能继续进入 simulation、bounded verification 和 code generation。
4. **反馈可回流**
   - 当模型不对时，系统最好能返回结构错误、可达性错误、concrete witness 或 counterexample，而不是只给一张“图长得不对”的印象反馈。

`pyfcstm` 的必要性，就在于它是一种同时满足这四条要求的目标形式。

### 4.2 `pyfcstm` 为何比更通用的 `UML/Umple` 更适合做 target

这里不是说 `Umple` 不好，而是说：

> 对 `LLM-based natural-language-to-model` 任务而言，过于宽的元模型空间往往不是优势，而是负担。

`Umple` 的语义面比 `pyfcstm` 更宽，它牵连到类、属性、关联、状态机、事件参数、history、region、timed transition 等更大的 UML-like 空间。  
而 `pyfcstm` 的优势在于它**主动收窄了输出空间**：

1. 它把目标聚焦在**单根层次控制状态机**上。
2. 它把模型核心聚焦在**状态、事件、变量、guard、effect、生命周期动作**这些对象上。
3. 它没有默认把论文问题推向“完整 UML 生态生成”。
4. 它把问题从“LLM 能否生成很宽很复杂的通用模型”收敛到“LLM 能否生成一类工程上可闭环处理的控制模型”。

这对论文来说非常关键，因为这意味着：

1. 生成空间更可控。
2. 错误类型更可枚举。
3. 自动评测更可操作。
4. 后续修复链路更容易建立。

### 4.3 `pyfcstm` 的必要性还体现在“同一 DSL 主线上的闭环”

当前 `pyfcstm` 的实际价值，不只是“能写状态机 DSL”，而是它已经形成了单源链路：

1. `DSL parsing`
2. `semantic validation`
3. `simulation runtime`
4. `bounded symbolic verification / reachability`
5. `template-based code generation`

这条链路的意义在于：

1. 论文不再只是输出一段文本。
2. 论文也不再只是输出一张图。
3. 论文输出的是一个**后续可继续处理的工程对象**。

所以在论文中最该强调的，不是 `pyfcstm` 某个单点语法，而是：

> `pyfcstm` 使 `NL-to-model` 成为一个可以通过可执行性、可验证性和代码生成一致性来评价的工程问题。

## 5. `pyfcstm` 的特殊性到底是什么

### 5.1 特殊性不是“最通用”，而是“任务形状匹配”

`pyfcstm` 的特殊性，不应该写成“覆盖面最大”。

更好的说法是：

> `pyfcstm` 是一个 task-shaped DSL。它并不追求覆盖整个 UML state machine 语义面，而是围绕层次控制逻辑、离散模式切换、guard/effect 数据语义，以及后续验证与代码生成闭环，构造了一个更收敛的文本 target。

这点可以直接作为 paper positioning：

1. `pyfcstm` 不是 general-purpose modeling language 的竞争者。
2. `pyfcstm` 是 `NL -> hierarchical control model` 任务的 target formalism。

### 5.2 它的元模型中心和 `Umple` 不同

即使两者都可以归到 `HSM + EFSM` 范畴，元模型中心也不同：

1. `Umple` 的中心是 model-oriented programming。
   - 它把类模型和状态机放在一起组织。
   - 它更像一个面向通用软件建模的大语言。
2. `pyfcstm` 的中心是控制逻辑状态机。
   - 它没有把论文问题导向类、关联、对象结构的大空间。
   - 它把表达能力集中在状态切换、变量更新和生命周期控制上。

因此，两者不是“谁完全覆盖谁”的关系，而是：

1. `Umple` 更宽、更通用。
2. `pyfcstm` 更窄、更任务化。

而在 `LLM-based modeling from natural language` 里，后者恰恰可能更适合做 target。

### 5.3 它的执行语义是你们自己掌控的

`pyfcstm` 的另一个特殊点是：它不是把语义完全托管给外部标准或黑盒运行器，而是你们自己掌控了这套执行语义。

这意味着：

1. 模型如何进入 stable boundary，是明确的。
2. 子状态与父状态之间的边界语义，是明确的。
3. `during before/after` 和 `>> during before/after` 的触发时机，是明确的。
4. declaration order 的优先级语义，是明确的。

对于论文而言，这个点非常重要，因为：

> 只有当目标语言的执行语义可控时，LLM 生成结果才可能被稳定评测，错误也才可能被稳定定位。

### 5.4 它支持 witness-driven 的工程评测

这一点是最值得在论文里讲清楚的工程价值。

当前 `pyfcstm` 的 reachability / verify 能力虽然不是完整 CTL/LTL 模型检验，但它已经有一个很强的特点：

1. 能做 bounded symbolic reachability。
2. 能返回 concrete witness path。
3. witness 包含状态、变量、事件、cycle。
4. witness 还能和 runtime replay 对齐。

这意味着论文可以设计出比“文本 BLEU / 结构相似度”更强的指标：

1. 语法成功率
2. 语义成功率
3. 可仿真率
4. reachability 正确率
5. witness 可回放率

这正是 `pyfcstm` 在 `project_1` 中最有研究价值的地方。

## 6. 学术贡献应该怎么写

### 6.1 主贡献不要写成“我们发明了一门比 `Umple` 更好的语言”

如果论文主问题是 `LLM-based modeling from natural language`，那 `pyfcstm` 本身更适合作为：

1. 目标表示
2. 研究基础设施
3. 统一评测载体

而不是论文唯一或主要的新颖点。

因此，论文里的贡献应当按下面四类来写。

### 6.2 推荐的贡献结构

#### 贡献一：问题定义贡献

> 我们将自然语言到状态机的自动生成，定义为“自然语言到可执行、可验证控制模型”的软件工程问题，而不是仅仅输出一份结构化文本或图形草图。

这一步把论文从“prompt engineering demo”拉回到软件工程问题空间。

#### 贡献二：表示与目标形式贡献

> 我们采用 `pyfcstm` 作为层次控制逻辑的文本目标形式。它提供了一个比通用 UML-like 表示更收敛、更适合 LLM 生成、且能直接进入统一工程闭环的 target formalism。

这一贡献的重点不在“语言多新”，而在“目标形式选型与任务适配性”。

#### 贡献三：系统贡献

> 我们构建了从自然语言到 `pyfcstm`，再到 parsing、semantic validation、simulation、bounded verification 与 code generation 的端到端链路。

这一步把模型生成和后续验证、执行真正接起来了。

#### 贡献四：评测贡献

> 我们提出了一套以可执行性、可验证性和 witness-based feedback 为核心的评测方式，使 `LLM-based modeling` 可以通过工程结果而不是表面文本相似度进行评价。

这通常是 reviewer 最容易买账的点，因为它直接回答“为什么这篇是 SE paper，而不是 NLP demo”。

## 7. 面对 `Umple` 时，真正稳的回应是什么

### 7.1 核心回应原则

当 reviewer 把问题打到 `Umple` 上时，不要正面去打“谁更强”。  
最稳的回应结构是：

1. 承认 `Umple` 是重要相关工作。
2. 明确它证明了 executable modeling language 是一条成熟路线。
3. 但指出：这不消解 `pyfcstm` 在你们这个任务设定里的必要性。
4. 原因不是“`Umple` 做不到状态机”，而是“我们的任务需要一个更收敛、更文本优先、更语义闭环的 target formalism”。

### 7.2 中文版稳定回应

可以直接写成下面这个结构：

> `Umple` 是重要的相关工作，它表明 executable modeling language 与 model-oriented programming 已经形成成熟路线。  
> 但我们的论文目标并不是提出又一个通用 executable modeling language，也不是覆盖完整 UML-like 元模型空间。  
> 我们关注的是自然语言到层次控制模型的自动生成，因此更需要一个文本优先、语义边界明确、输出空间收敛，并且能够直接进入 parse / validate / simulate / bounded verify / code generation 闭环的目标形式。  
> `pyfcstm` 在本文中的角色正是这样一种 task-shaped target formalism。  
> 因此，`Umple` 是重要 baseline 和参照物，但它并不替代 `pyfcstm` 在本研究设置中的方法学角色。

### 7.3 英文版短 rebuttal 模板

下面这段可以直接进入 rebuttal：

> We do not claim that pyfcstm replaces general-purpose executable modeling languages such as Umple.  
> Our contribution is different in scope and purpose.  
> This paper studies natural-language-to-model generation for hierarchical control logic, which requires a target formalism that is text-first, semantically explicit, and tightly connected to parsing, simulation, bounded verification, and code generation within a single workflow.  
> Pyfcstm serves this role as a task-shaped formal target.  
> In this sense, Umple is important related work, but it does not remove the need for a narrower, semantically closed target representation in our setting.

### 7.4 英文版更强一点的 rebuttal 模板

如果 reviewer 明确质疑“为什么不用 `Umple`”，可以再进一步写：

> The key issue in our setting is not whether executable modeling languages already exist, but whether the target representation is suitable for NL-to-model generation and evaluation.  
> Compared with more general UML-like modeling ecosystems, pyfcstm intentionally narrows the output space to hierarchical control-state models with an explicit execution semantics and a closed engineering pipeline.  
> This reduction is methodologically important for LLM-based modeling: it makes the generated artifacts parsable, simulatable, and verifiable under a consistent semantics, and allows us to evaluate models by executable outcomes rather than by surface similarity alone.

## 8. 论文里应该明确讲的“必要性”口径

下面这些句子是可以直接写进论文里的。

### 8.1 中文版一句话定位

> 本文使用 `pyfcstm` 作为目标形式，并不是因为不存在其他可执行建模语言，而是因为自然语言到控制模型的自动生成任务，需要一个文本优先、语义收敛、且能直接进入统一工程闭环的目标表示。

### 8.2 英文版一句话定位

> We use pyfcstm not as a claim against existing executable modeling languages, but as a task-shaped target formalism for NL-to-hierarchical-control-model generation.

### 8.3 中文版稍长定位段

> 在本文中，`pyfcstm` 的价值不在于取代所有状态机建模语言，而在于为自然语言到层次控制模型的自动生成提供一个更受控的目标空间。  
> 相比语义面更宽的 UML-like 建模生态，`pyfcstm` 以文本 DSL 的形式收敛了输出对象，并将解析、语义校验、仿真、有限可达性验证和代码生成组织在同一条工具链上。  
> 这使得 `LLM-based modeling from natural language` 可以通过可执行性、可验证性和 witness-based feedback 进行评测，而不再停留在表层文本或图形生成层面。

## 9. 论文里应该避免的说法

为了减少被 reviewer 一下击穿的风险，下面这些说法应明确避免：

1. “现有工作都做不了 executable modeling。”
2. “`Umple` 不支持形式化验证。”
3. “`pyfcstm` 的形式化能力比 `nuXmv` 更强。”
4. “我们的主要贡献是提出一门全新的通用建模语言。”
5. “只要有 `pyfcstm`，自然语言状态机建模问题就解决了。”

更合适的替代说法是：

1. “我们关注的是更受控的 target formalism，而不是更大的元模型覆盖面。”
2. “贡献在于任务适配性与工具链闭环，而不是单纯语言覆盖面。”
3. “`pyfcstm` 让生成结果能够进入统一的工程评测链路。”

## 10. 最稳的最终结论

如果要把整件事压成一句论文层面的判断，那么最稳的一句是：

> `pyfcstm` 在这篇论文中的必要性，不来自“它比 `Umple` 更通用”，而来自“它更适合作为自然语言到层次控制模型自动生成任务的目标形式”。它的特殊性不在于覆盖整个 UML-like 建模生态，而在于提供了一个文本优先、语义收敛、可执行、可验证、可生成代码的统一工程闭环，从而使 `LLM-based modeling from natural language` 能以软件工程方式而不是表层文本方式被研究和评测。

这也是最推荐在 introduction、discussion 和 rebuttal 中反复保持一致的主口径。

## 11. 可直接复用的 contribution bullets

下面给一版更适合软件工程论文的 contribution bullet 草稿：

1. We formulate NL-to-model generation as a software engineering problem whose outputs must be executable and analyzable, rather than as a surface-level structured text generation task.
2. We use `pyfcstm` as a task-shaped target formalism for hierarchical control logic, providing a text-first and semantically explicit representation for model generation.
3. We build an end-to-end pipeline from natural language to `pyfcstm` models and further to parsing, semantic validation, simulation, bounded verification, and code generation.
4. We evaluate generated models using executable outcomes, including parsability, simulability, verification success, and witness-based feedback, instead of relying solely on textual similarity.

## 12. 可直接复用的 rebuttal 结尾段

如果需要一个更短的 rebuttal 结尾段，可以直接用下面这段：

> In short, the role of pyfcstm in this paper is methodological rather than competitive with general-purpose executable modeling languages.  
> It provides a narrower and semantically closed target space that is better aligned with NL-to-hierarchical-control-model generation, and enables evaluation through execution and verification outcomes.  
> This is why Umple is relevant background, but not a drop-in substitute for our setting.
