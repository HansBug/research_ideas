# Paper1 唯一论文大纲

本文件是 Paper1 唯一的规范论文大纲，按 [overleaf/sections/index.tex](../overleaf/sections/index.tex) 的十节顺序组织，给出可直接扩写的论文正文骨架、图表内容、证据落点与边界。数字来自[规范结果归档](../final_results/v60_current_vs_x1v2_baseline/README.md)的 v4 公平对照层；谓词资格来自[当前谓词审计](../related_work/provenance/predicate_provenance.md)；直接工作处置来自[最接近工作矩阵](../related_work/closest_work_matrix.md)；L/W/D 与对应关系的定义与学术锚点来自 issue [#189](https://github.com/HansBug/research_ideas/issues/189) 与 [#195](https://github.com/HansBug/research_ideas/issues/195)。上一版大纲保留在 [paper_outline.md.backup](./paper_outline.md.backup)，其事实仍可用，其论述顺序不再沿用。

投稿目标为 SANER 2027 Research Track：IEEE 双栏 10 页正文另加 2 页参考文献，全轨双盲，摘要截止 2026-09-21，正文截止 2026-09-25。英文为投稿语言，中文为内部伴生稿。

## 写作纪律

1. 术语首次出现写「中文（English，缩写）」，之后只用中文或缩写；英文全称只出现一次，可机检合同见 [terminology_policy.md](./terminology_policy.md)。
2. 自然语言输入一律称「自然语言描述」，不称「需求」。上游数据集作者把它叫 requirement description，但它是按模板写出的设计层描述，部分还是从模型反推而来；论文在 §5.1 交代这一点，其余地方统一口径。
3. L 与 W 在 §2 定义；D/A、对应关系与 K/N/I 是测量仪器，只在 §5 定义，§1 到 §4 不出现。
4. 建模对象边界（无时钟、无不变式、无正交区）的唯一定义落点是 §2.1；§5.1 只做推论，§1、§8、§9 不重复讲 fork/join。
5. 所有比较均为案例研究内的描述性比较，不写显著性，不写普遍优越性，不写跨语言效果。
6. 成本只以一段话报告，不设研究问题，不算倍率。
7. 页预算：§0–1 共 1.5 页，§2 共 1.5 页，§3 共 0.5 页，§4 共 2.5 页，§5 共 1.25 页，§6 共 2 页，§7–8 共 0.75 页，§9–10 共 0.25 页。

<a id="outline-0"></a>
## 题目与摘要

**题目（英文投稿，中文伴生）。** 主题目承载全文的一句话论点：状态机是可执行对象，在大语言模型发现问题之前用它提供事实、之后用它确认发现，问题发现就从表面对齐走到了行为层。候选如下，首选第一条：

1. `Beyond Surface Alignment: Evidence-Augmented LLM Discovery and Executable Confirmation of Behavioral Issues in State Machines` —— 超越表面对齐：状态机行为级问题的证据增强 LLM 发现与可执行确认。
2. `Beyond Surface Alignment: Discovering Behavioral Issues in State Machines against Natural-Language Descriptions with Executable Evidence` —— 超越表面对齐：面向自然语言描述的状态机行为级问题发现与可执行证据。
3. `From Claims to Witnesses: LLM-Based Discovery of Behavioral Issues in State Machines against Natural-Language Descriptions` —— 从主张到见证：面向自然语言描述的状态机行为级问题 LLM 发现。

**摘要。** 状态机是离散控制逻辑从自然语言（natural language，NL）描述走向实现的承重设计制品，如今越来越多地由大语言模型（large language model，LLM）生成；一台机器在被信任之前，必须先被复核是否做到了描述所说的事。最难复核的偏差是行为性的：目标状态是否可达、进入后能否离开、事件是否被消费、反馈能否使系统回到规定状态。逐元素比对能看出缺了哪个状态，看不出守卫沿任何轨迹都为假。本文研究给定一段自然语言描述和一台既有、在分析期间固定不变的状态机（state machine，STM），发现并定位机器不满足描述之处。我们把问题按陈述它所需的信息深度分为 L0/L1/L2，把报告按证据强度分为 W0/W1/W2，并指出既有的一致性检查停在 L0/L1 与 W1。方法把状态机当作可执行对象而非文本：C1 通过 PlantUML 适配器（PlantUML adapter）把源制品转换为保留来源归属（provenance）的有限控制状态机（finite control state machine，FCSTM），从中导出确定性检查事实（deterministic inspect facts），在大语言模型寻找问题之前送入其上下文；C2 把发现编译为四族 19 条类型化谓词（typed predicate）之一，在同一表示上执行并附上回放回执（replay receipt），使发现从 W1 的主张提升为 W2 的见证。在 54 个 PlantUML 输入对、145 条人工标注预期问题、3 轮共 435 个单元的案例研究中，方法与同模型朴素基线的 L2 FULL `hit@1` 为 `105/117=89.74%` 对 `50/117=42.74%`，整体为 `310/435=71.26%` 对 `227/435=52.18%`；310 个命中单元中 168 个携带 W2 回执，基线为 0；代价是报告级精确率低 `4.34 pp`，其中约四成无效报告落在方法内部的表示与证据边界，我们对此给出机制分解。[^fair][^wang2025][^input_selection]

<a id="outline-1"></a>
## 1. 引言

引言按六步走：利害关系 → 任务 → 两个观察给出三个结构性缺口 → 核心想法与设计直觉 → 贡献 → 结果预告。七个段落的 topic sentence 连起来自成论证。

**P1 · 利害关系。** 状态机是离散控制逻辑在描述与实现之间的承重设计制品，覆盖装备制造、轨道交通、物联网与航空航天等领域。随着从自然语言描述生成状态机成为常规做法，机器在被信任之前必须先被复核：它是否做到了描述所说的事。这把本文的任务从「生成」切到「复核」——本文不生成、不修改机器。[^wang2025][^structure_event][^gwt]

**P2 · 任务。** 给定一段自然语言描述和一台既有状态机，找出机器不满足描述之处并定位到具体元素。现有做法三类：元素级一致性规则（如 Li 与 Zheng 的业务对象规则）、让大语言模型当审稿人读两份文本（如 MCeT 与朴素提示）、形式验证（前提是一份没人写过的形式规约）。[^li_zheng][^mcet][^uml_survey]

**P3 · 观察一：问题有深浅。** 用一个小例子。描述三句：上电后处于 `Idle`；收到 `Start` 进入 `Running`；操作员按下 `Stop` 后设备应回到 `Idle`。模型写了 `Running --Stop--> Cooldown / temp := 100` 与 `Cooldown --[temp < 40]--> Idle`，而没有任何动作修改 `temp`。表面对齐检查全部通过：`Idle` 在、`Stop` 在、`Stop` 触发的迁移在、到 `Idle` 的边在。行为层的问题却真实存在：沿任何进入 `Cooldown` 的轨迹守卫恒假，按下 `Stop` 后 `Idle` 不可达。这条问题不对应描述的任何一句原话，却确实违反了描述。判定它所需的信息不在两份文本的表面上——可达性、守卫可满足性、事件后的响应都要跨迁移推理。由此得两个结构性缺口。**缺口 ①**：规则式一致性检查比较元素的存在与顺序，从不构造或排除一条执行，所以到不了这一层。**缺口 ②**：大语言模型审稿人能谈行为，但行为事实不在它的输入里，它只能在脑中模拟；我们的同模型基线恰好在这一层崩塌（L2 FULL `hit@1` 为 42.74%，而 L0/L1 为 49.77%/67.62%）。[^hilken][^baier_katoen]

**P4 · 观察二：报告有强弱。** 「`Cooldown` 回不到 `Idle`」是一句主张，复核者要自己重推一遍才能信。测试与验证文献区分未经判定的主张与在制品上求值过的反例：前者是一条 smell，后者是一条 error trace。现有的自然语言对模型检查器输出的全是前者——MCeT 的 issue、Li 与 Zheng 的 `AbnStepPair` 有定位但未执行、朴素提示的三个自由文本字段。**缺口 ③**：发现上没有附着任何可执行对象，什么都无法回放。[^femmer][^debbi][^barr]

**P5 · 核心想法与设计直觉。** 把状态机当作可执行对象，而不是一段文本，并在大语言模型的前后各用一次。之前：把源制品转换为保留来源归属的 FCSTM，从它确定性地导出结构、拓扑与运行事实，作为发现阶段的输入——C1，证据增强发现（evidence-augmented discovery）。之后：把大语言模型提出的每条发现编译为一个小词表中的类型化谓词，在同一表示上执行并附上可回放回执——C2，可执行确认（executable confirmation）。三个缺口与设计一一对应：①② 由 C1 回应，③ 由 C2 回应。图 1 用 P3 的小例子把这条链画成一页。

**P6 · 贡献。** 三条，每条指向一个结果小节。
- **C1 · 证据增强发现。** 提出保留来源归属的 FCSTM 工作表示与确定性检查事实，并把它们作为发现阶段的输入。在 PlantUML 案例研究中，方法相对同模型基线的 L2 FULL `hit@1` 为 89.74% 对 42.74%，L2 `hit@all` 为 84.62% 对 20.51%（§6.1）。
- **C2 · 可执行确认。** 从领域学术普查归纳四族 19 条类型化谓词及其 FCSTM 后端语义，对适用发现执行断言并记录可回放回执。310 个 FULL 命中单元中 168 个达到 W2，基线按构造为 0（§6.3）。
- **C3 · 案例研究与可复算制品（条件性）。** 54 个输入对上 145 条带 D/L 分层的人工预期问题台账、两维人工裁定协议与最小复算包。是否公开待定，公开则按 §10 的最低标准。

**P7 · 结果预告。** 54 个输入对、145 条预期问题、同模型基线。整体 FULL `hit@1` 71.26% 对 52.18%；L2 提升最大，L0 次之，L1 略低于基线，§6.1 给出机制解释；报告级精确率低 4.34 pp，其中 118 条无效报告落在方法内部的表示与证据边界（§6.2）。只给数字，不写「显著」。[^fair]

<a id="outline-2"></a>
## 2. 背景与相关工作

顺序固定为：对象 → L → W → 相关工作。L 依赖对象（「跨迁移的行为性质」要先有迁移语义），相关工作依赖 L（IET 用 L 定位）。

### 2.1 建模对象：离散控制逻辑的层次化扩展有限状态机

研究对象是离散控制逻辑的层次化扩展有限状态机 $M=(S,E,V,Tr,A)$：带层次的状态集 $S$、事件集 $E$、变量集 $V$、带守卫与动作的迁移集 $Tr$、动作集 $A$。这是 UML/SysML 状态机与绝大多数控制器设计共享的核心片段，UML 2.5.1 的状态、迁移、触发、守卫、动作槽位语义与 Dwyer 等的有限状态性质模式在此片段上定义良好。实时时钟与不变式、正交区并发不在对象内：它们引入另一套验证理论（时间自动机、区域抽象），是独立的问题。这里只定义对象，不提数据集，不提任何 pair。[^uml251][^dwyer][^heimdahl][^heitmeyer]

### 2.2 问题深度 L

问题深度（problem depth，L）描述陈述一条问题所需的信息范围，与用什么算法、后端或见证形式无关。

| 档 | 定义 | 例 |
| --- | --- | --- |
| L0 · 表面对齐 | 比对描述词项与模型词项即可陈述 | 描述点名 `Emergency`，模型没有这个状态 |
| L1 · 结构导出 | 需从模型结构导出一个事实，静态可判 | 某守卫在单个状态上恒假；某叶态出度为 0；同源同触发两条守卫重叠 |
| L2 · 行为/全局性质 | 涉及跨迁移、路径、可达性、终止、响应或全局交互的行为关系 | 进入 `ActiveState` 后永久困住；§1 例中 `Stop` 后 `Idle` 不可达 |

学术锚点借用形状，不引用定义：Hilken 等把 UML/OCL 验证任务分为考虑单个系统状态的 structural 任务与考虑状态序列及迁移的 behavioral 任务；Baier 与 Katoen 指出不变式可由可达状态集判定，而路径片段上的安全性质不能，活性性质更是有限迹无法判定；Engels 等与 Knapp、Mossakowski 指出句法规则查不出动态一致性问题。先例分的是分析手段的能力，本文分的是陈述该问题所需的信息，两者在本语料上重合但概念不同，论文必须写明。`structural inconsistency` 采 Hilken 口径而非 Van Der Straeten 口径。[^hilken][^baier_katoen][^engels][^knapp][^torre]

### 2.3 证据强度 W

见证强度（witness strength，W）描述一条报告被证到什么程度。

| 档 | 定义 | 例（沿用 §1 小例） |
| --- | --- | --- |
| W0 · 断言 | 散文主张，既无定位也无可执行对象 | 「可能有死锁」 |
| W1 · 定位 | 点到具体元素或路径，但没有可执行对象 | 「`Cooldown` 回不到 `Idle`」 |
| W2 · 见证 | 一个可执行对象，在被求值的那份制品上被判过真值 | 「从初始态执行 `Start, Stop` 抵达 `Cooldown`，`temp=100`，唯一出边守卫 `[temp<40]` 求值为假，没有任何动作写 `temp`；`must_reach(Idle)` 在界内为假」 |

W1 的构件对应 Femmer 等对 requirements smell 的刻画：有具体定位与具体检测机制，但仍不是见证。W2 对应 Debbi 综述中的 counterexample / error trace：由分析它可定位错误来源。W 小于 2 的裁决对应 Tretmans 的 `inconclusive`：没有找到不合规的证据，但测试目的也没有达成。W0 与 W1 的档名是本文自设，内容有出处。[^femmer][^debbi][^tretmans]

**为什么 W2 的价值远高于 W1。** 这里接到 Barr 等的 oracle problem：自然语言描述是一份部分的、非形式的预言。W1 报告把预言的求值留给人；W2 报告自带一次在制品上完成的求值，复核者只需回放，不必重推。同时给出 W2 的上界：见证在抽象模型上成立而在具体模型上不成立时是 spurious counterexample。本文的见证在 FCSTM 而非 PlantUML 原文上求值，因此存在这一风险；§6.2 用无效报告的归因把它量化，并给它起名「表示债务」。[^barr][^clarke_cegar]

### 2.4 相关工作

三类，每类一个结构性局限，最后一句定位。相关工作前置的理由：IET 是任务合同的直接先例，读者必须在看方法之前知道它做到了哪一层。

**A 类：自然语言与模型的一致性检查。** Li 与 Zheng（IET Software 2025）是本文任务合同的直接先例：原始自然语言经结构化与用例规约（use-case specification，UCS）转换进入流程，Algorithm 3 以 UCS 和既有状态机为输入，输出定位的 `AbnStepPair`，并在一个 Web Store 项目的状态机制品上评测。按本文的 L 口径作分析性映射（IET 原文未使用 L）：Semantic Consistency 比较业务对象在活动图与 UCS 中的存在，为 L0；Process Consistency 要求输入对象先于输出对象出现，为 L1 的局部顺序；State Consistency 检查触发迁移的动作是否出现及相对顺序是否保持，为 L1，至多位于 L1/L2 边界。三条规则均未构造或排除执行路径，未分析可达性、死端、终止、事件响应或全局交互。MCeT（MODELS 2025）保留了「自由文本描述 + 既有图 → 定位问题」的形态，但对象是顺序图，没有持久状态、层次与迁移语义，输出是散文 issue。Wang 等自己的 requirements semantic checking 对参考模型算 F1——它需要一份参考模型，而实践中正是没有它才需要复核。Sultan 等做多视图一致性并修正，Liu 等做需求与异构模型的可观测一致性并用 SMT 求解，二者对象都不是一台固定的状态机。**结构性局限**：比较的是元素的存在与顺序，或输出散文；没有一项在被审的机器上执行过任何东西，所以到不了 L2，也到不了 W2。[^li_zheng][^mcet][^wang2025][^sultan][^liu]

**B 类：自然语言到模型的生成、补全与修复。** de Biase 等从 Given–When–Then 需求补全 SysML 状态机；Abdulkarim 等比较结构驱动与事件驱动的生成框架；King 与 Vyatkin 用 STPA 约束递归修改既有有限状态机并生成 IEC 61499 代码。**结构性局限**：输出是一台新机器，输入模型被改动；没有一个固定不动的被审制品，因此不产生定位在该制品上的发现。[^gwt][^structure_event][^king_vyatkin]

**C 类：自然语言到形式性质与验证。** FRET 把受限自然语言需求形式化；nl2postcond 用大语言模型生成后置条件；Estivill-Castro 与 Hexel 用语法提示为轻量级有限状态机（Lightweight Finite State Machine，LLFSM）合成多个模型检查器可接受的性质；André 等综述了 UML 状态机的形式化与自动验证。**结构性局限**：假定要验的性质已经知道，由人写或由人选；它们给可执行证据，但不做发现，且性质合成的评测停在合成而非 verdict。LiSSA 表明追溯链接恢复是独立问题；LLM-as-a-Judge 的自评限制说明人工有效性判断不能由模型自报替代。[^fret][^nl2postcond][^estivill][^uml_survey][^lissa][^judge]

**定位句。** 本文不在 B 类竞争，也不做 C 类的性质合成；它保持制品固定，做 A 类的任务，同时把 C 类的证据形态接到发现之后——A 类没有一项工作提供后者。IET 是任务合同的直接先例，本文不主张该合同的优先权；本文的增量是该合同下 L2 问题的证据增强发现与可执行确认。

**表 2：承重工作的定位。** 行为六篇承重工作与本文；列为「输入含固定制品？」「输出是定位发现？」「检查深度（按本文 L）」「证据形态（散文 / 定位 / 执行）」「评测对象」。IET 行承认任务形态重叠；L 列只按本文口径分析其已发表规则。

| 工作 | 固定制品输入 | 定位发现输出 | 检查深度 | 证据形态 | 评测对象 |
| --- | --- | --- | --- | --- | --- |
| Li 与 Zheng（IET） | 是 | 是 | L0/L1 | 定位 | 一个 Web Store 项目的状态机 |
| MCeT | 是（顺序图） | 是 | 不适用（无状态语义） | 散文 | FBench 顺序图 |
| Sultan 等 | 多视图，非单一固定 | 不一致列表并修正 | 视图间关系 | 规则 + LLM | SysML 案例 |
| de Biase 等（GWT） | 部分状态机，被补全 | 否 | 不适用 | 生成元素 | 两个案例 |
| Estivill-Castro 与 Hexel | LLFSM | 否（合成性质） | 不适用 | 性质文本 | 22 个 SEG 示例 |
| Liu 等 | 异构模型 | 一致性判断 | 可观测关系 | SMT | 合成需求与汽车案例 |
| 本文 | 是 | 是 | L0/L1/L2 | 定位 + 执行 | 54 个 PlantUML 输入对 |

<a id="outline-3"></a>
## 3. 问题定义与范围

### 3.1 任务合同

输入对写为 $(d, m)$：$d$ 是一段自由文本的自然语言描述，$m$ 是分析开始前已经存在、在分析中保持不变且具有来源归属的状态机制品。输出是一组定位的问题报告 $f=(d\_ref, m\_ref, obligation, location, evidence)$：引用描述中的句子、引用源制品中的位置、陈述被违反的义务、给出定位，并在适用时附上可执行证据。方法不生成、不修改 $m$；$m$ 可以来自人，也可以来自上游大语言模型流程。

### 3.2 适配器契约

方法面向能投影为 §2.1 中 $M$ 的状态机类模型。一种具体建模语言只有在声明的子集上给出到 $M$ 的可追溯投影、保留源载体到投影元素的映射、写明规则相关能力、对不能可靠映射的特征失败关闭，才可作为适配器接入。本文只实现并评测 PlantUML 适配器；其支持片段与不支持项（正交区、时钟、fork/join）在 §4.2 列出。

### 3.3 范围声明

方法产生的报告分三种证据状态：W2 的可执行见证、W1 的精确定位、W0 的未定位主张。L 是台账侧对预期问题的分类，方法不输出 L；D/A、报告有效性与对应关系由独立人工评测完成（§5）。投影、编译器、运行时或证据闭合的失败须与源制品问题分开记录。

<a id="outline-4"></a>
## 4. 方法

### 4.1 总览

**图 2：方法架构。** 四条责任泳道：源制品与描述 → 确定性程序（适配器、FCSTM、检查事实、谓词编译、后端）→ 大语言模型（契约提取、双 lens 发现、语义筛选）→ 人工评测（§5）。C1 覆盖泳道二到泳道三的前半：转换与检查事实进入发现阶段；C2 覆盖泳道三到泳道二的后半：发现被绑定为类型化谓词，回到后端执行并产出回执。图中标出每类失败的归因位置：投影边界、编译器边界、运行时失败、人工裁定。

**图 1：运行示例。** 用 §1 的小例子走完整条链：描述第三句授权「`Stop` 后回到 `Idle`」的义务；源制品中 `Running --Stop--> Cooldown` 与 `Cooldown --[temp<40]--> Idle` 提供定位；确定性检查事实给出 `temp` 无写者；发现阶段提出候选；类型化计划绑定 `must_reach(Idle)` 的起点、目标与界；原生回放给出 `false` 与轨迹。输入片段不受支持、绑定不完整、原生加载失败、超时或回放失败时，系统保留来源定位与失败阶段，以 W1/W0 表示证据尚未闭合。

### 4.2 C1（上）：适配器、FCSTM 与来源映射

适配器把 PlantUML 源文本解析为规范化的源中间表示，再投影为 FCSTM。FCSTM 是 $M$ 的可执行实现：层次状态、事件、变量、带守卫与效果的迁移、进入/退出/驻留动作，运行语义为宏步（`macrostep`）。投影全程保留源行号、具名载体、所有者路径、伪状态、生命周期动作与迁移来源；每个 FCSTM 元素都能回指源文本位置，每条报告与每份回执因此都能定位回作者写的那一行。支持片段：单区层次、初始/终止伪状态、事件触发、有限域守卫、变量赋值效果。失败关闭项：正交区、历史伪状态、时钟与时间事件、fork/join。不能投影的特征不会被静默丢弃，而是记为投影边界并进入 §6.2 的归因。

### 4.3 C1（下）：确定性检查事实

在 FCSTM 上运行确定性检查，产出结构、拓扑与运行三类事实：结构事实（声明清单、槽位占用、叶态出度、守卫重叠）、拓扑事实（从初始配置的可达集、无退出叶态如 `W_LEAF_NO_OUTGOING_TRANSITION`、跨层路由）、运行事实（有界宏步前沿、事件消费者集合）。这些事实不产生新的义务——义务只来自描述——它们只把源文本里不稳定呈现的信息变成可引用的对象。事实随来源映射一起进入发现阶段的上下文。

### 4.4 大语言模型阶段

五个阶段顺序执行，每阶段写清输入、输出与禁读项（不读台账、不读评测、不读历史报告，不输出 L/W/D）。

1. **契约提取。** 从描述中提取可追溯的义务契约，每条契约引用描述原句；仅在固定条件满足时做一次有界补全。
2. **双 lens 发现与定位。** 两个互补 lens 共享同一响应 schema：`contract_structure_contrast` 优先审契约完整性、结构与对照一致性（遗漏或压缩的契约、所有者/根默认入口、迁移组守卫冲突、错误的局部退出目标、未授权的边）；`behavior_consequence` 优先审行为后果（根可达性、可达的事件消费者覆盖、禁入范围、死端/前沿事实、跨包装器可达性、稳定终止、有界响应）。每条候选带 `reason` 与 `basis`，且必须完成精确的源与闭合模型绑定。
3. **执行批。** 确定性前沿、路由、类型化输入绑定、谓词编译与原生后端执行（§4.5、§4.6）。
4. **语义筛选与受限修正。** 内部阶段只做候选筛选与审计信息保留，不构成论文的 D/A 裁定。
5. **发布。** 按精确类型身份去重，输出方法发现与全部证据。

### 4.5 C2（上）：四族 19 条类型化谓词

**表 3：19 条谓词。** 列为 ID、名称、命题形状、族、主要输入、后端、极性资格。谓词来源是领域文献普查：UML 2.5.1 给元素槽位与 Constraint 的二值后果，Dwyer 等给响应/缺失/全称的性质形状，Heimdahl 与 Leveson、Heitmeyer 等给守卫覆盖、互斥与事件响应的分析义务，Baier 与 Katoen 给不变式、可达与死锁自由。必须写明：19 条从文献归纳，不是从 54 个输入对或台账调参而来；每条的学术资格、方法执行语义、实例授权三类责任分开记录，附录 A 逐条给出。[^uml251][^dwyer][^heimdahl][^heitmeyer][^baier_katoen][^predicate]

| 族 | 谓词 | 主要输入 | 后端与解释范围 |
| --- | --- | --- | --- |
| 结构（6） | S1 `element_exists`、S2 `transition_exists`、S3 `trigger_set_equals`、S4 `state_action_attached`、S5 `transition_guard_equals`、S6 `transition_effect_attached` | 源载体、元素引用、触发/守卫/效果 AST | 声明片段上的静态检查 |
| 拓扑（4） | G1 `may_reach`、G2 `must_reach`、G3 `route_avoids`、G4 `coaccessible_to` | 来源/目标集合、节点或边、界 | 图路径及其明确的终止条件；G2 为有界必达 |
| 轨迹（4） | R1 `event_consumed`、R2 `state_reached_after`、R3 `behavior_occurs`、R4 `state_retained` | 事件序列、状态、所有者、有限轨迹窗口 | 宏步与回放定义的运行片段 |
| 有界验证（5） | V1 `guards_disjoint`、V2 `guards_complete`、V3 `response_within`、V4 `deadlock_free`、V5 `state_invariant` | 守卫组、有限域、步数、稳定配置、期望占据值 | 有限域、界限与极性限定的查询；V4 为叶状态探测 |

### 4.6 C2（下）：执行、回执与 W2 条件

回执记录程序、模型、查询、绑定输入、范围、界、布尔结果、轨迹或失败阶段，并以哈希绑定回放。W2 的发表解释为：

$W2(f) \iff F(f) \land B(f) \land I(f) \land Q(f) \land E(f)$

其中 $F$ 是受支持片段，$B$ 是精确实例绑定，$I$ 是 pair/obligation/plan/model/program/receipt 的精确身份链，$Q$ 是非空且可核验的描述引文、源引用与绑定引用，$E$ 是完成的原生布尔回执。任一条件缺失时，定位明确的候选保留为 W1；`unknown`、`failure`、超时一律不算机械证实，这就是 Tretmans 的 `inconclusive`。极性资格另限定可写的最强命题：G2 的有界 `must_reach` 只支持声明界内的必达；V4 的叶状态探测只覆盖它探测的片段；V5 的有界 `false` 是不变式的单向反例，有界 `true` 只说明界内通过。**证据充分性原则**：路由选最弱的健全见证——一个有来源依据的 `false` 或一条具体反例已足以建立缺陷证据；静态证据闭合时不为形式完整性升级到轨迹仿真或有界验证。这条原则在 §6.3 解释谓词的使用分布。[^predicate][^tretmans]

<a id="outline-5"></a>
## 5. 研究设计

### 5.1 案例研究数据

上游是 Wang 等（Internetware 2025）对大语言模型生成 SysML 行为模型的实证研究：作者按一份需求规约模板为每个案例写自然语言描述（无文档案例从模型反推），用 Claude、DeepSeek、GPT-4、GPT-4o、Kimi、Llama 各生成状态机，并经格式、语法、语义三道检查反馈。原论文把描述称为 requirement description；本文统一称自然语言描述。状态机部分为 10 份描述 × 6 个模型 = 60 个 `<描述, PlantUML>` 对；本文取其 feedback-final 输出（58 个语义检查输出与 2 个生成回退）。十份描述中有一份要求 fork/join 与秒级执行时间约束，其忠实模型不在 §2.1 的 $M$ 内，对应六个输入对在任何运行之前仅凭描述文本排除。余下 **9 个描述簇、每簇 6 个制品、54 个输入对**。脚注写代价：被排除的 pair 中有表现高于均值者，其台账里有 27 条范围内的结构主张随描述一并排除。原论文的参考模型隔离不用。[^wang2025][^input_selection]

**表 4：分析单位与嵌套。**

| 描述簇 | 每簇制品 | 输入对 | 预期问题 | 轮次 | 轮次级单元 | 嵌套 |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 9 | 6 | 54 | 145 | 3 | 435 | 单元嵌套于输入对、制品与描述簇 |

### 5.2 什么算一条问题：人工裁定 D/A

人工裁定（human adjudication，D/A）先判事实，再判义务。D2：源中承重事实成立，有可陈述的被违反义务，且没有站得住的称职反读法；三个子类按义务出处分——D2-lit 有成文条文可引，D2-impl 免领域知识即可判为失效（如死锁），D2-norm 描述不会写但缺了在本领域不可接受。D1：事实成立，存在一种与结构事实相容的第二种称职读法。D0：事实成立，但没有被违反义务或设计读法正当。A0：承重事实在作者源上不成立，分两个出口——`FALSE_POSITIVE`（虚构路径、误读守卫/事件/效果）与 `NOT_A_DEFECT_CLAIM`（方法内部的表示或分析状态被归给作者源）。**只有 D2/D1 是有效发现。** 学术锚点：IEEE 1044 的 defect 定义（不采用「需修复」合取项）；Krogstie 等的 validity/completeness；Barr 等的 implicit oracle；Kano 的 must-be requirement；Pollock 的 undercutting defeater 对应 D1，rebutting defeater 对应 D0；Zave 与 Jackson 的领域知识入册条件。[^ieee1044][^krogstie][^barr][^kano][^pollock][^zave_jackson][^sei_defeaters]

### 5.3 报告与预期问题的对应关系与报告有效性

两维分开裁。维度 A 是对应关系（relation）：`FULL_MATCH` 表示候选与预期问题描述同一缺陷实例、根因或被违反义务，允许措辞、抽象层级与证据形式不同，复合台账中一个独立且有诊断性的核心 facet 即可；`PARTIAL_MATCH` 表示真实但局部或间接的关系，不足以确定同一缺陷身份；`NO_MATCH` 表示不属于同一缺陷。维度 B 是报告有效性：先裁核心主张成立与否，成立且至少有一个 FULL/PARTIAL 为 `VALID_KNOWN`，成立且全部 NO 为 `VALID_NOVEL`，不成立为 `INVALID`。执行顺序：先裁有效性；`INVALID` 的全部关系直接闭合为 NO；有效者再逐条预期问题裁 FULL/PARTIAL/NO；程序据此确定性派生记账类别（bookkeeping category，K/N/I）。W 不进入匹配函数：W1 自由文本只要有具体 `where` 与可审计 `reason/basis` 就可以 FULL，这是基线可以公平参评的必要条件。学术锚点：MCeT 的 same-root-cause equivalence 与 new true issue；NIST SATE 的 directly/indirectly related finding；Pearson 等的 best-case 故障定位；Martinez 等的语义/修复等价；Porter 等的 known-fault 与 false positive；Klees 等的 distinct bug。写明这套两维枚举是本文综合先例形成的操作化，不是某篇文献逐字给出的。[^mcet][^sate][^pearson][^martinez][^porter][^klees]

**表 5：测量仪器。**

| 维度 | 取值 | 决定什么 |
| --- | --- | --- |
| D/A | `D2/D1/D0/A0` | 报告是否是有效发现（D2/D1） |
| 对应关系 | `FULL/PARTIAL/NO` | 预期问题是否被命中（仅 FULL） |
| 报告有效性与归属 | `K/N/I` | 报告级精确率分子与分母 |
| 证据强度 | `W0/W1/W2` | 命中单元的机械证据；不进入命中门槛 |

### 5.4 预期问题台账

由一名博士生在 54 个输入对上逐条人工标注，共 145 条，每条有来源依据（引用描述原句与源制品行号）、D 档与 L 档：D2/D1 为 98/47，L0/L1/L2 为 71/35/39。它是参考而非 ground truth：MCeT 与 SATE 都警告 oracle 不完整时不能把未匹配报告当假阳性，§5.3 的 `VALID_NOVEL` 正是为此设置。单标注者、无一致性统计，进 §8。[^ledger_v2][^l_tier][^mcet][^sate]

### 5.5 基线

X1v2：同模型 `gpt-5.6-luna`、同 54 个输入对、同 3 轮、单 prompt、无循环、无工具，输入为描述与 PlantUML 原文，输出 schema 只有 `issue / where / reason` 三个自由文本字段。因此它按构造只能到 W1；后续人工核验不倒灌为基线的 W2。两臂使用同一套人工裁定口径。[^fair]

### 5.6 指标

- `hit@1` = FULL 命中的轮次级单元 / 435；按 L 分层时分母为该层条目数 × 3。
- `hit@3` = 三轮中至少一次 FULL 的预期问题 / 145。
- `hit@all` = 三轮全部 FULL 的预期问题 / 145。
- 报告级精确率 = (K + N) / 全部报告。
- 有支撑覆盖 = 被 FULL 或 PARTIAL 覆盖的单元或条目，单列，不进主指标。
- W-on-hits = FULL 命中单元的最高 W 分布。
- 谓词使用 = 有终止回执的不同谓词 ID 数；报告绑定谓词 = 至少绑定一条最终报告的不同谓词 ID 数。

### 5.7 成本口径

按 `gpt-5.6-luna` 的官方 list price（uncached input $0.20、cache read $0.02、cache creation $0.25、output $1.20，每百万 token，2026-08-18 核验），用 API 返回的 usage 分项相乘求和；output 含 reasoning token；只计方法侧推理调用，不计评测、人工与基础设施。同时报 token 数。[^cost]

### 5.8 研究问题与统计立场

- **RQ1（发现覆盖）。** 相对同模型基线，方法在 145 条预期问题上的 FULL `hit@1/@3/@all` 如何？按 L0/L1/L2 分层后，差异落在哪一层？→ C1。
- **RQ2（报告有效性）。** 方法的报告级精确率如何？无效报告由哪些成分构成，其中多少落在方法内部的表示与证据边界？→ 覆盖的代价。
- **RQ3（证据强度）。** C2 把多少 FULL 命中提升到 W2？19 条谓词中哪些产生了回执、哪些绑定到了报告，为什么？→ C2。

<a id="outline-5-2"></a>
- **RQ4（条件性：仅当 `TODO-EXPERIMENT-01` 完成时进入正文）。** 保持 PlantUML 到 FCSTM 的转换、模型、提示词、输入对、轮次与 C2 不变，确定性检查事实的开/关带来多大的发现能力增益？单位为成对的预期问题轮次槽位，指标为 FULL `hit@1/@3` 与报告级精确率的成对差异。未完成时本条不出现，C1 只作为整体机制陈述，组件分离写入 §8；本案例的冻结端到端结果不估计确定性检查事实的独立作用。RQ2 的精确率分解不替代本条。

人工协议：两侧复核不完全对称——方法侧 1271 条报告经源制品优先复审，基线侧由 233 条 non-K 复核与 279 条 K 复核组成；无独立双人标注与一致性统计。统计立场：435 个单元来自 145 条预期问题的三轮重复并嵌套于 54 个制品与 9 个描述簇，全部比较为案例研究内的描述性比较，不作显著性推断。

<a id="outline-6"></a>
## 6. 结果

### 6.1 RQ1：发现覆盖与 L 分层

**表 6：主结果（整体与按 L 分层）。** L0/L1 分层数由 [combined_report_index_v4.json](../final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_report_index_v4.json) 的 K 报告 FULL 台账集合按轮重算，整体与 L2 数与 canonical summary 逐项一致；写论文前把 L0/L1 行补进[结果处置清单](./paper_result_inventory.md)。

| 层 | n | FULL `hit@1` 方法 / 基线 | FULL `hit@3` 方法 / 基线 | FULL `hit@all` 方法 / 基线 |
| --- | ---: | --- | --- | --- |
| 整体 | 145 | `310/435=71.26%` / `227/435=52.18%` | `119/145=82.07%` / `106/145=73.10%` | `86/145=59.31%` / `46/145=31.72%` |
| L0 | 71 | `142/213=66.67%` / `106/213=49.77%` | `56/71=78.87%` / `50/71=70.42%` | `37/71=52.11%` / `21/71=29.58%` |
| L1 | 35 | `63/105=60.00%` / `71/105=67.62%` | `26/35=74.29%` / `30/35=85.71%` | `16/35=45.71%` / `17/35=48.57%` |
| L2 | 39 | `105/117=89.74%` / `50/117=42.74%` | `37/39=94.87%` / `26/39=66.67%` | `33/39=84.62%` / `8/39=20.51%` |

**图 3：按 L 分层的 FULL `hit@1` 与 `hit@all`。** 两组柱，每柱标分子分母；不作显著性推断。

**阅读。** 提升集中在 L2：`hit@1` 高 47 pp，`hit@all` 高 64 pp，基线在 39 条 L2 里只有 8 条三轮稳定命中。L0 高 17 pp。**L1 反而略低于基线**（`hit@1` 低 7.6 pp，`hit@3` 少 4 条），不能藏，它有一个与 §6.2 同源的机制解释——表示层的两面：

- FCSTM 投影**暴露**原始文本里看不出的结构事实：复合态实际为空、层次整体丢失、同源同触发守卫重叠（3 条）、`Entry: Emergency Stop` 被解析成状态、区块被作用域规则建成三层嵌套。方法在这些 L1 条目上赢，在全部 L2 条目上赢。
- 投影也**抹平**只存在于记法层的事实：「三个条件被压成单一事件名」出现 4 次，「递减写进 guard 槽位而非 effect」「输出动作被反转成输入事件」「子状态被声明为顶层同级」各 1 次。缺陷活在 PlantUML 标签文本里；投影把一条杂乱的标签规范化成一个干净的事件 token，缺陷就不见了；基线读原文，反而看得见。
- L0 的收益来自同一机制的正面：声明清单与来源映射让「描述点名而模型没有」的对比稳定可做。

给两三个基线漏掉的 L2 实例：`EIS-0002-02` 要排除从初始状态到三个目标状态的全部路径；`INS-0029-05` 是可重复进入终态的非终止行为；`EIS-0037-01` 是三个控制态的可达性与进入后被困。说明它们为什么在源文本层面看不出来、检查事实如何让它们可见。[^fair][^l_tier][^ledger_v2]

### 6.2 RQ2：报告有效性与无效报告的构成

方法输出 1271 条报告，基线 512 条；报告级精确率 `980/1271=77.10%` 对 `417/512=81.45%`，差 `-4.34 pp`。K/N/I 为 `749/231/291` 对 `312/105/95`；D2/D1/D0/A0 为 `721/259/120/171` 对 `342/75/85/10`。

**表 7：无效报告的构成。**

| 成分 | 方法 | 基线 | 解释 |
| --- | ---: | ---: | --- |
| D0（事实成立但不构成缺陷） | `120/1271=9.44%` | `85/512=16.60%` | 方法更少把非缺陷报成缺陷 |
| A0 / `FALSE_POSITIVE`（源级事实不成立） | `53/1271=4.17%` | `10/512=1.95%` | 源级误读 |
| A0 / 非缺陷主张（not-a-defect claim，NADC） | `118/1271=9.28%` | 不适用 | 方法内部表示与证据边界，基线无同构类别 |
| I 合计 | `291/1271=22.90%` | `95/512=18.55%` | 与精确率互补 |

NADC 的 118 条再分为编译器产物 38、投影/追踪边界 24、运行时/证据闭合 48、不可归因 8；已确认的仅由 lowering 导致的语义错误为 0。措辞必须准确：这些是方法内部的表示、归因与证据闭合边界产生的、对作者源不成立的主张——§2.3 埋下的 spurious counterexample 在这里兑现为表示债务——不是「转换引入了语义错误」。基线没有同构分类，NADC 只报方法侧比率，不做跨臂成分比较，不扣掉 NADC 重算「校正精确率」。可写的结论：在共同的 435 个单元上覆盖高 19 pp，同时承担 4.34 pp 的报告级精确率代价；这是一个覆盖与有效性之间的运行点，不是全指标优越。N 报告的 D2/D1 组成（`38/193` 对 `50/55`）与保守实质性 N 组（121 对 98）进附录。[^fair][^attribution][^clarke_cegar][^troya]

**成本（一段）。** 方法侧 54 × 3 共 162 格，总计 `$7.18`，每格约 `$0.044`，每输入对三轮约 `$0.13`；基线记录小计 `$0.225`，缺一条 schema 重试的 usage 回执，只能作为下界。同时给两侧 token 数。不算倍率，读者自己会算。人工复核成本不在三个 RQ 内，W2 回执的设计目的是降低它，这只能作为 §7 的假设。[^cost]

<a id="outline-6-3"></a>
### 6.3 RQ3：证据强度与谓词使用

310 个 FULL 命中单元的最高 W 为 W0/W1/W2 `0/142/168`，即 54.2% 的命中携带 W2 回执；基线 `0/227/0`。报告级伴随分布 `0/854/417`（分母 1271）。19 条谓词中 12 条有终止回执（G1、G2、G4、R1、R2、R4、S1–S5、V4），8 条绑定到最终报告（G1、G2、R2、S2、S3、S4、S5、V4）；报告绑定行 `825/1271=64.91%`。这些是不同谓词 ID 的使用统计，不是缺陷覆盖、边际贡献或基线的等价零值。

**表 8：W 与谓词使用。** 上半为 FULL 命中单元与报告级的 W 分布；下半为「谓词 × 极性 × 绑定行数」，从 825 条绑定行直接统计，写论文前补算。

| 项目 | 方法 | 基线 |
| --- | ---: | ---: |
| FULL 命中单元 W0/W1/W2 | `0/142/168`（分母 310） | `0/227/0`（分母 227） |
| 报告级 W0/W1/W2 | `0/854/417`（分母 1271） | 不适用 |
| 有终止回执的谓词 ID | `12/19` | 不适用 |
| 绑定到报告的谓词 ID | `8/19` | 不适用 |
| 谓词 × 极性 × 行数 | 待补算 | 不适用 |

**为什么 19 条只用到 8 条。** 三层解释，不引入任何台账侧的可表达性审计：

1. **证据充分性原则**（§4.6）：路由选最弱的健全见证。精确命题是 $O \Leftrightarrow P$，证伪只需一个 $P \Rightarrow O$ 的充分条件。
2. **两个 worked example**，从真实报告取：可达性义务的精确表达在轨迹层（R 族），但 G1 `may_reach` 为假已足以证伪，于是 R 族被拓扑替代；全局响应义务（某事件后全体状态跳到目标态）的精确表达是 V3 对所有状态的全称命题，但一个状态做不到已足以证伪，于是 V3 被单点反例替代。
3. **语料性质**：未使用谓词对应的义务在这批 PlantUML 里稀少——守卫多为简单条件（V1/V2 的互斥与完备少有用武之地）、描述几乎不给步数界（V3）、禁行路径义务罕见（G3）、变量后值义务未进入词表。

W 描述机械确认，不决定 D/A、对应关系或 K/N/I；G2、V4、V5 的极性资格限定最强命题，不把已完成的执行降为 W1。[^fair][^predicate]

### 6.4 RQ4（条件性）

仅当 `TODO-EXPERIMENT-01` 完成时写本节：成对开/关条件下 FULL `hit@1/@3` 与报告级精确率的差异，按 L 分层，以描述簇为重采样单位给出描述性不确定性。未完成时删除本节，§8 保留组件分离的威胁。

<a id="outline-7"></a>
## 7. 讨论

**7.1 表示层的两面。** §6.1 与 §6.2 是同一机制的两个方向：可执行表示暴露了文本里看不出的结构与行为事实（L2 与一半 L1 的收益），也抹平了只在记法层存在的事实（另一半 L1 的损失），并产生对源不成立的主张（NADC）。后两者都可由适配器工程消除——保留标签原文作为事实、在投影边界失败关闭——但它们是这类方法的固有代价，必须写在方法节而非事后找台阶。

**7.2 证据充分性与谓词词表。** 8/19 的使用分布是设计结果，不是词表缺陷：发现问题只需要健全的充分条件，未使用的谓词大多对应「精确但过强」的形态。这也界定了 C2 的角色——它确认发现，不替代发现；没有适用谓词的发现仍以 W1 发布。

**7.3 实践含义。** 工程师可先看高 D、W2、来源清楚的发现，回执支持在描述、模型或工具版本变化后回放同一计划。本文没有用户研究、审查工时或部署结果，不声称效率、认证或安全收益。[^li_zheng][^predicate]

**7.4 对 C1 的整体陈述。** 端到端差异不能分解为转换与检查事实的独立贡献，冻结结果无法识别确定性检查事实的独立增量；若 RQ4 完成则在此引用其结果，否则写明组件分离留待成对对照。

<a id="outline-8"></a>
## 8. 有效性威胁

**构念与内部。** 报告级精确率、FULL 对应关系、W 与 K/N/I 对应不同对象；人工协议可审计但无独立双人盲标与一致性统计；145 条台账不是缺陷全集，`VALID_NOVEL` 的 231 条说明台账外仍有真实问题；C1 的端到端差异包含转换、检查事实与 C2 的耦合，未做成对分离。**统计。** 435 个单元嵌套于 54 个制品与 9 个描述簇，只作描述性比较。**语义。** W2 在 FCSTM 上求值，存在 spurious 风险，已由 NADC 量化；G2、V4、V5 的有界解释不得写成无界证明。**外部。** 单适配器（PlantUML）、单上游数据源、单模型；不外推到其他建模语言或其他大语言模型。**相关工作。** IET 的 L 映射是本文的分析口径，只界定问题深度，不评价其学术价值。[^fair][^predicate][^li_zheng]

<a id="outline-9"></a>
## 9. 结论

回到两个观察。问题有深浅：在 L2 上基线崩塌而方法稳定（`hit@all` 84.62% 对 20.51%）。报告有强弱：一半以上的命中从主张变成了见证（168/310 达 W2，基线 0）。代价是 4.34 pp 的报告级精确率，其主要来源是可执行表示的固有边界，我们已把它分解到可归因的位置。IET 是任务合同的直接先例；本文的增量是该合同下 L2 问题的证据增强发现与可执行确认。[^fair][^li_zheng]

<a id="outline-10"></a>
## 10. 数据可得性

若公开（C3），按最低标准：一个匿名仓库，包含（i）54 个输入对的描述与 PlantUML 原文及来源行定位；（ii）145 条台账，每条只保留 `id, pair, D, L, summary, detail` 六个字段——一句话概述与完整自然语言详述来自原 JSON，不加多余字段；（iii）两臂逐报告的有效性、对应关系与 D/A 决定；（iv）从 (ii)(iii) 复算表 6–8 全部数字的脚本与一条命令。不含凭据、人工身份与未获许可的外部全文。若不公开，一段话写明原因与是否计划在录用后公开。SANER 鼓励制品但不强制。[^fair][^ledger_v2]

<a id="outline-appendix"></a>
## 附录

**附录 A：19 条谓词的证据与语义边界。** 按 S1–S6、G1–G4、R1–R4、V1–V5 给出 19 行完整表：精确命题、外部依据与逐字引文定位、方法执行语义、实例授权、支持片段、逐极性 W2 条件与发表资格。[^predicate]

**附录 B：输入、适配器与执行合同。** 输入闭包、PlantUML 适配器支持片段与失败关闭项、来源映射、类型化绑定与失败处置；图 B.1 从描述一句义务走到类型化计划、W1/W2 回执与回放轨迹。

**附录 C：完整结果。** 按 L、轮次、预期问题与报告单位的完整分层表；N 报告组成与保守实质性 N 组；NADC 四路 overlay；谓词 × 极性 × 绑定行；成本逐项与 token 数。每张表含分子、分母、来源指针与解释范围。[^fair][^cost][^attribution]

<a id="outline-references"></a>
## 参考文献

[^fair]: v60/current versus X1v2 baseline v3 canonical summary. `final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json` and `combined_report_index_v4.json`, 2026-09-02. Stable repository artifacts.
[^cost]: Paper1 method cost audit v1. `final_results/v60_current_vs_x1v2_baseline/derived/final_talk_cost_section7_v1/cost_summary_v1.json`, 2026-09-01. Stable repository artifact.
[^attribution]: Paper1 conversion-attribution audit v1. `final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/i_attribution_summary_v1.json`, 2026-09-01. Stable repository artifact.
[^predicate]: Paper1 predicate provenance audit. `related_work/provenance/predicate_provenance.md`, 2026-09-02. This points to the audited external primary sources, not to a local citation substitute.
[^input_selection]: Paper1 input provenance: `corpora/seed_library/llms-emp-stm-subset/assets/extracted/feedback_final_validation_summary.json` fixes the 60-row stage/fallback pool; `selected_seed_examples/README.md` and `discover_matrix/docs/protocol/nl_scope_rule.md` fix the six out-of-scope exclusions and the 54-pair grid. Accessed 2026-09-02.
[^l_tier]: Paper1 L-tier definition and classification. `discover_matrix/ledger_v2/l_tier.json`, 2026-09-02.
[^ledger_v2]: Paper1 expected-issue ledger. `discover_matrix/ledger_v2/README.md` and `discover_matrix/ledger_v2/ledger.json`, 2026-09-02.
[^wang2025]: Yuan Wang, Ning Ge, Jiangxi Liu, Zhilong Cao, Zheping Chen, and Chunming Hu. “Generating SysML Behavior Models via Large Language Models: an Empirical Study.” *Proceedings of the 16th International Conference on Internetware*, ACM, 2025, pp. 366--377. https://doi.org/10.1145/3755881.3755926.
[^li_zheng]: Haibo Li and Lixiao Zheng. “Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework.” *IET Software*, 2025, 2025(1), Article 6714956. https://doi.org/10.1049/sfw2/6714956.
[^mcet]: Khaled Ahmed, Jialing Song, Ou Wei, Bingzhou Zheng, and Boqi Chen. “MCeT: Behavioral Model Correctness Evaluation using Large Language Models.” *MODELS*, 2025, pp. 84--95. https://doi.org/10.1109/MODELS67397.2025.00014.
[^sultan]: Bastien Sultan, Ludovic Apvrille, and Sophie Coudert. “On the Consistency of State Machines, Use Cases and Block Diagrams Using Dependency Graphs and Large Language Models.” *Software and Systems Modeling*, 2026, online first. https://doi.org/10.1007/s10270-026-01388-4.
[^liu]: Tianhai Liu, Shmuel Tyszberowicz, and Bernhard Beckert. “Observable Consistency Checking across Requirements and Models.” *ENASE*, 2026. https://doi.org/10.5220/0014719400004015.
[^gwt]: Maria Stella de Biase et al. “Completion of SysML State Machines from Given--When--Then Requirements.” *Software and Systems Modeling*, 2024. https://doi.org/10.1007/s10270-024-01228-3.
[^structure_event]: Samer Abdulkarim et al. “Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models.” arXiv:2604.00275v1, 2026. https://arxiv.org/abs/2604.00275. Preprint, not peer-reviewed as of 2026-09-02.
[^king_vyatkin]: Akira King and Valeriy Vyatkin. “LLM-based Iterative Refinement of Finite-State Machines with STPA Controller Constraints and Generation of IEC 61499 Code.” *ETFA*, 2025. https://doi.org/10.1109/ETFA65518.2025.11205687.
[^fret]: Dimitra Giannakopoulou, Anastasia Mavridou, Julian Rhein, Thomas Pressburger, Johann Schumann, and Nija Shi. “Formal Requirements Elicitation with FRET.” *REFSQ 2020 Workshops*, 2020. https://ntrs.nasa.gov/api/citations/20200001989/downloads/20200001989.pdf.
[^nl2postcond]: Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K. Lahiri. “Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions?” *Proceedings of the ACM on Software Engineering*, FSE 2024. https://doi.org/10.1145/3660791.
[^estivill]: Vladimir Estivill-Castro and René Hexel. “Grammar-Prompted Synthesis of Verification Properties from Natural Language Requirements for Multiple Model Checkers.” *ENASE*, 2026. https://www.scitepress.org/Papers/2026/147167/147167.pdf.
[^uml_survey]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification -- A Survey.” *ACM Computing Surveys*, 55(13s), 2023. https://doi.org/10.1145/3579821.
[^lissa]: Fuchß et al. “LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation.” *ICSE*, 2025. https://doi.org/10.1109/ICSE55347.2025.00186.
[^judge]: Wang et al. “LLM-as-a-Judge in Software Engineering.” *ISSTA*, 2025. https://doi.org/10.1145/3728963.
[^uml251]: Object Management Group. *Unified Modeling Language (UML), Version 2.5.1*. 2017. https://www.omg.org/spec/UML/2.5.1/PDF.
[^dwyer]: Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. “Patterns in Property Specifications for Finite-State Verification.” *ICSE*, 1999. https://doi.org/10.1145/302405.302672.
[^heimdahl]: Mats P. E. Heimdahl and Nancy G. Leveson. “Completeness and Consistency in Hierarchical State-Based Requirements.” *IEEE TSE*, 1996. https://doi.org/10.1109/32.508311.
[^heitmeyer]: Constance Heitmeyer, Robert Jeffords, and Bruce Labaw. “Automated Consistency Checking of Requirements Specifications.” *ACM TOSEM*, 1996. https://doi.org/10.1145/234426.234431.
[^hilken]: Frank Hilken, Philipp Niemann, Martin Gogolla, and Robert Wille. “Towards a Catalog of Structural and Behavioral Verification Tasks for UML/OCL Models.” Venue and year to be confirmed before submission; quoted definitions verified in issue #189.
[^baier_katoen]: Christel Baier and Joost-Pieter Katoen. *Principles of Model Checking*. MIT Press, 2008. Def. 3.20, §3.3.2, Def. 3.33, §3.2--3.3.
[^engels]: Gregor Engels, Jan Hendrik Hausmann, Reiko Heckel, and Stefan Sauer. “Testing the Consistency of Dynamic UML Diagrams.” *IDPT*, 2002.
[^knapp]: Alexander Knapp and Till Mossakowski. “Multi-view Consistency in UML: A Survey.” *LNCS* 10800, 2018. https://doi.org/10.1007/978-3-319-75396-6_3; arXiv:1610.03960.
[^torre]: Damiano Torre, Yvan Labiche, and Marcela Genero. “UML Consistency Rules: A Systematic Mapping Study.” *EASE*, 2014. https://doi.org/10.1145/2601248.2601292.
[^femmer]: Henning Femmer, Daniel Méndez Fernández, Stefan Wagner, and Sebastian Eder. “Rapid Quality Assurance with Requirements Smells.” *Journal of Systems and Software*, 2017.
[^debbi]: Hichem Debbi. “Counterexamples in Model Checking -- A Survey.” *Informatica*, 42(2):145--166, 2018.
[^tretmans]: Jan Tretmans. “An Overview of OSI Conformance Testing.” 2001. §3.4--3.5.
[^barr]: Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. “The Oracle Problem in Software Testing: A Survey.” *IEEE TSE*, 41(5):507--525, 2015. https://doi.org/10.1109/TSE.2014.2372785.
[^clarke_cegar]: Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. “Counterexample-Guided Abstraction Refinement.” *CAV*, 2000. https://doi.org/10.1007/10722167_15.
[^troya]: Javier Troya, Sergio Segura, Lola Burgueño, and Manuel Wimmer. “Model Transformation Testing and Debugging: A Survey.” *ACM Computing Surveys*, 55(4), 2022. https://doi.org/10.1145/3523056.
[^ieee1044]: IEEE Std 1044-2009. *IEEE Standard Classification for Software Anomalies*. https://doi.org/10.1109/IEEESTD.2010.5399061.
[^krogstie]: John Krogstie, Odd Ivar Lindland, and Guttorm Sindre. “Defining Quality Aspects for Conceptual Models.” *IFIP ISCO3*, Springer, 1995. https://doi.org/10.1007/978-0-387-34870-4_22.
[^kano]: Elmar Sauerwein, Franz Bailom, Kurt Matzler, and Hans H. Hinterhuber. “The Kano Model: How to Delight Your Customers.” *IX. International Working Seminar on Production Economics*, 1996, pp. 313--327.
[^pollock]: John L. Pollock. “Defeasible Reasoning.” *Cognitive Science*, 11(4):481--518, 1987.
[^zave_jackson]: Pamela Zave and Michael Jackson. “Four Dark Corners of Requirements Engineering.” *ACM TOSEM*, 6(1), 1997. https://doi.org/10.1145/237432.237434.
[^sei_defeaters]: John B. Goodenough, Charles B. Weinstock, and Ari Z. Klein. *Eliminative Argumentation: A Basis for Arguing Confidence in System Properties*. CMU/SEI-2015-TR-005, 2015.
[^sate]: Vadim Okun, Aurelien Delaitre, and Paul E. Black. *Report on the Static Analysis Tool Exposition (SATE) IV*. NIST SP 500-297, 2013. https://doi.org/10.6028/NIST.SP.500-297.
[^pearson]: Spencer Pearson et al. “Evaluating and Improving Fault Localization.” *ICSE*, 2017. https://doi.org/10.1109/ICSE.2017.62.
[^martinez]: Matias Martinez et al. “Automatic Repair of Real Bugs in Java: A Large-Scale Experiment on the Defects4J Dataset.” *Empirical Software Engineering*, 2017. https://doi.org/10.1007/s10664-016-9470-4.
[^porter]: Adam A. Porter, Lawrence G. Votta, and Victor R. Basili. “Comparing Detection Methods for Software Requirements Inspections: A Replicated Experiment.” *IEEE TSE*, 21(6), 1995. https://doi.org/10.1109/32.391380.
[^klees]: George Klees, Andrew Ruef, Benji Cooper, Shiyi Wei, and Michael Hicks. “Evaluating Fuzz Testing.” *CCS*, 2018. https://doi.org/10.1145/3243734.3243804.
