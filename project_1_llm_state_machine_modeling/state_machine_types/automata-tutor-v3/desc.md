# Automata Tutor v3：自动机理论在线教学与自动评分平台 / Automata Tutor v3

## 基本信息

- 标题：Automata Tutor v3
- 中文标题：Automata Tutor v3：自动机理论在线教学与自动评分平台
- 作者：Loris D'Antoni，Martin Helfrich，Jan Kretinsky，Emanuel Ramneantu，Maximilian Weininger
- 发表：*Computer Aided Verification*，`LNCS 12225`，pp. 3-14，2020
- DOI：`10.1007/978-3-030-53291-8_1`
- 链接：https://doi.org/10.1007/978-3-030-53291-8_1
- 形式主义：`Finite Automata / CFG / PDA / TM / Automata Tutor`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：自动机理论课程的自动评分、自动反馈与自动出题基础设施
- 工具/实现获取方式：论文明确说明 `Automata Tutor v3` 是开源工具，并给出在线入口 `https://automata.model.in.tum.de`；后端算法依赖 `https://github.com/AutomataDotNet/Automata`。
- 标准/格式获取方式：前后端以 `XML` objects 通信，内部承载 regular expressions、`NFA`、`CFG`、`PDA`、`TM` 等题型对象；不是面向跨工具交换的中立标准。

## 简报

这篇论文的重点，不在于再讲一次自动机理论，而在于把大班教学里最耗人的那部分工作做成稳定基础设施：自动出题、自动评分、自动生成反例和个性化反馈。相对更早的 `JFLAP` 这类“可视交互实验台”，`Automata Tutor v3` 更强调教师工作流和教学规模化能力。它把 `RE/CFG/PDA` 构造、`RE -> NFA`、Myhill-Nerode、Pumping Lemma、`CNF/CYK`、`While -> TM` 等多类题统一到一个在线平台中，并明确给出 grading 算法、difficulty/quality 指标和可扩展的系统实现。

- 形式主义定位：自动机理论教学、自动评分与题库生成基础设施，而不是新的自动机本体。
- 构造方式简述：教师先定义题型、参考解和难度区间，系统负责 exercise generation、grading 与 feedback generation，学生再通过浏览器端图形画布或文本答案提交解答。
- 基础设施与场景简述：依托 frontend/backend/database 分层、`XML` 消息、`AutomataDotNet` 算法库、自动出题和有限等价检查，服务大班 formal-languages / computation-theory 课程。

```text
teacher-defined exercise + grading rules -> web frontend + backend algorithms -> automatic feedback / random exercise generation -> large-scale course deployment
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 多类自动机理论题型与其参考解。
2. grading algorithm 与 feedback generation。
3. Automatic Problem Generation (APG)。
4. frontend、backend、database 三层工具结构。
5. `AutomataDotNet` 提供的 automata / regex 算法支持。

### 核心抽象

论文明确把系统实现拆成三层，可保守写成：

$$
AT_3 = (Frontend, Backend, Database)
$$

上式中的符号逐项解释如下：

1. `Frontend` 负责网页渲染和图形画布。
2. `Backend` 负责题目检查、评分、反馈和自动出题。
3. `Database` 负责用户、课程和题目数据。
4. 这是论文在实现章节给出的直接系统骨架。

论文新增题型的集合可整理为：

$$
\mathcal{P} = \{\mathrm{RE/CFG/PDA\ Words},\ \mathrm{RE/CFG/PDA\ Construction},\ \mathrm{RE\ to\ NFA},\ \mathrm{MN\ Classes},\ \mathrm{Pumping\ Game},\ \mathrm{Derivation},\ \mathrm{CNF},\ \mathrm{CYK},\ \mathrm{While}\rightarrow \mathrm{TM}\}
$$

上式中的符号逐项解释如下：

1. `\mathcal{P}` 是论文列出的新题型集合。
2. 它覆盖 regular、context-free、pushdown、Turing-complete 这几条典型教学线。
3. 这些题型共同组成 `Automata Tutor v3` 相比旧版最重要的能力扩张。

Automatic Problem Generation 使用 quality 与 difficulty 两个指标。其选择目标可写成：

$$
E^\ast = \arg\max_E \ \mathrm{qual}(E) \quad \text{s.t.} \quad d_{min} \le \mathrm{diff}(E) \le d_{max}
$$

上式中的符号逐项解释如下：

1. `$E$` 是候选练习。
2. `$\mathrm{qual}(E)$` 是论文定义的 quality metric。
3. `$\mathrm{diff}(E)$` 是 difficulty metric。
4. `$d_{min}, d_{max}$` 是教师要求的难度范围。
5. 论文实际做法是先随机生成一批候选，再从满足难度约束者中选质量最高的。

论文对 `CFG/PDA Construction` 的 limited equivalence grading 给出了明确公式：

$$
\mathrm{grade} = \frac{|A \cap B|}{|A \cup B|} \cdot \mathrm{maxScore}
$$

上式中的符号逐项解释如下：

1. `$A$` 是参考解在给定长度上接受的词集合。
2. `$B$` 是学生解在同样测试范围内接受的词集合。
3. `$\mathrm{maxScore}$` 是该题型的满分。
4. 因为 `CFG/PDA` 语言等价不可判定，论文用受限长度下的测试近似评分。

### 一个最小例子与通俗解释

论文里比较直观的最小例子是 `RE -> NFA` 题型：

1. 教师只需要给出一个正则表达式。
2. 学生在画布上构造 `\epsilon`-`NFA`，也可以用 block states 分步做 Thompson-style 构造。
3. 后端根据 block-state 使用情况和最终语言是否正确打分。
4. 如果不正确，系统直接返回反例或指出构造路径的问题。

通俗地说，`Automata Tutor v3` 像“自动机课的在线批改老师”。它不仅知道答案对不对，还能根据题型给出贴近概念的反馈，比如给你一个区分词、提示某个推导不成立，或者自动再生成一题同难度练习。

### 运行 / 接受 / 转移语义

这篇论文不是在定义单一自动机的运行语义，而是在定义平台如何围绕不同对象做 grading。以 `RE/CFG/PDA Construction` 为例，论文的核心判定不是“完全语言等价是否成立”，而是受限测试下的近似语言重合度，即上面的 grade 公式。

对 `RE` 题型，论文使用编辑距离评分。其核心想法可保守整理为：

$$
\mathrm{grade}_{RE} \propto 1 - \mathrm{dist}_{edit}(re_{student}, re_{ref})
$$

上式中的符号逐项解释如下：

1. `$\mathrm{dist}_{edit}$` 是 Levenshtein edit distance。
2. `$re_{student}$` 是学生给出的正则式。
3. `$re_{ref}$` 是教师提供的参考正则式之一。
4. 论文选择 edit distance，是因为一个很小的 RE 拼写错误可能导致语言差异非常大。

### 语义边界

1. 这篇论文的主对象是教学基础设施，而不是工业验证平台。
2. 很多 grading 算法是“教学上足够实用”的近似，而不是理论上的完全判定。
3. 自动出题目前集中在若干 `CFG` 与 `While -> TM` 题型，不是所有题型都已 fully automated。
4. 工具虽然支持多类 formal objects，但并不试图把它们统一成某个单一元模型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统骨架 | `$AT_3 = (Frontend, Backend, Database)$` | 论文的实现分层。 |
| 题型集合 | `$\mathcal{P} = \{\cdots\}$` | 相比旧版新增的能力边界。 |
| APG 目标 | `$E^\ast = \arg\max_E \mathrm{qual}(E)\ \text{s.t.}\ d_{min} \le \mathrm{diff}(E) \le d_{max}$` | 自动出题时如何选题。 |
| `CFG/PDA` 评分 | `$\mathrm{grade} = \frac{|A \cap B|}{|A \cup B|} \cdot \mathrm{maxScore}$` | 受限等价检查的核心公式。 |
| `RE` 近似评分 | `$\mathrm{grade}_{RE} \propto 1 - \mathrm{dist}_{edit}(re_{student}, re_{ref})$` | RE 题型为何使用编辑距离。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 覆盖 `DFA/NFA/PDA/TM` 与多类语言对象。 |
| 事件 / 触发 | 不适用 | 重点是语言与自动机教学，而非反应式事件系统。 |
| 守卫 / 数据 | 弱支持 | 数据主要体现在题目参数，不是运行时富数据模型。 |
| 层次 | 不支持 | 不是层次状态机平台。 |
| 并发 / 同步 | 不支持 | 不在论文主线。 |
| 时间约束 | 不支持 | 与实时系统无关。 |
| 连续动态 / 随机性 | 不支持 | 不在对象范围内。 |
| 可执行 / 可验证性 | 很强 | 自动评分、反馈、自动出题和大规模课程部署都已验证。 |

### 形式化问题与性质

1. 它补的是“自动机理论如何规模化教学”的基础设施，而不是研究新算法本体。
2. APG、limited equivalence grading 和 per-problem feedback 是其最有复用价值的三块。
3. 对本文库而言，它与 `JFLAP` 形成了很好的互补：一个偏交互实验，一个偏课程运营与自动批改。

## 构造方式与承载格式

### 建模入口

论文的建模入口有两类：

1. 教师侧输入参考对象、文字题意和难度范围。
2. 学生侧通过 automata canvas、文本输入或结构化答案提交解答。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `XML` objects 作为前后端通信格式。
2. automata / regex / grammar / TM 的内部对象。
3. `AutomataDotNet` 提供的算法对象。
4. 数据库存储的 users / problems / courses。

### 交换与互操作

这条路线的互操作重点在于：

1. 前端用 `Scala + JavaScript`，后端用 `C#`，中间靠 `XML` objects 交互。
2. 算法层大量复用 `AutomataDotNet`，说明它不是从零硬编码每个题型。
3. 工具的 modular structure 支持多前端、多后端和负载分发扩展。

## 配套基础设施

- 建模/编辑工具：网页前端、automata/TM drawing canvas、题目配置界面。
- 解析/交换/元模型支持：前后端 `XML` 对象、题型内部表示、课程数据库。
- 仿真/执行支持：PDA 模拟、TM 模拟、对学生错误构造给出可观察 counterexample。
- 验证/分析支持：自动评分、语言近似比较、编辑距离、有限长度测试、APG。
- 代码生成/转换支持：重点不是工业代码生成，而是题目生成与教学反馈生成。
- 标准化或社区生态：依托 `AutomataDotNet`、开放源码和大班课程部署经验形成教学工具生态。

## 适用场景与需求前提

### 适用场景

适合以下任务：

1. 自动机理论、形式语言、计算理论课程的大规模在线作业与练习。
2. 需要自动评分和个性化反馈的混合教学场景。
3. 需要持续生成同难度训练题的自学平台。

### 需求前提

1. 教学内容主要围绕 `RE/NFA/CFG/PDA/TM` 等经典对象。
2. 题目能够落成平台支持的结构化输入形式。
3. 教师接受近似但快速的评分机制，而不是每题都追求完全理论判定。
4. 课程规模足够大，自动评分带来的边际收益明显。

### 不适用或高成本场景

1. 若目标是工业级状态机工程，而不是教学，`Automata Tutor` 的定位就不合适。
2. 若题目强依赖开放式证明和长文本解释，平台化评分的收益会下降。
3. 若课程对象不在 automata/computation-theory 范围内，可复用性有限。

## 与相邻形式主义的关系

相对 [a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md](../a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md)，`JFLAP` 更偏个人实验和交互理解，而 `Automata Tutor v3` 更偏教师批改、反馈与课程规模化运营。相对 [tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md](../tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md)，后者是更窄的 `Büchi/LTL` 教学工具线，而这里覆盖面更广。相对 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，`LearnLib` 是研究级主动学习框架，这篇论文则是教学基础设施，不追求同类算法开放性。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒 `project_1`：当状态机生成和验证能力成熟后，如何把它们做成“可教学、可反馈、可规模化”的平台，同样是重要问题。
2. 自动评分中的 counterexample 反馈机制，对“模型生成失败后如何给用户可操作解释”很有启发。
3. APG 也说明结构化状态机对象非常适合再向前走一步，变成题目、任务或 benchmark 自动生成器。

### 作为目标形式主义还是中间表示

它更像围绕经典自动机对象的教学与交互基础设施，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 一旦模型对象足够结构化，就可以自动生成练习、反例和反馈，而不只是做验证。
2. 用户反馈最好跟对象结构直接绑定，比如给出区分词、错误推导或局部模拟，而不是只报一个 fail。
3. 平台层的“难度”和“质量”指标设计，值得迁移到后续 benchmark/data generation 场景。

### 现实限制

它的目标非常明确地偏教学；但正因为目标收得足够窄，这套自动评分和自动反馈机制才做得足够实用。

## 重要的相关工作

1. [a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md](../a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md)：经典自动机教学实验台。
2. [tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md](../tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md)：更窄但更接近 `\omega`-automata 的教学工具线。
3. [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：同样强调算法基础设施，但面向研究和黑盒学习而非教学。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 归类理由：论文主体是自动机理论课程的自动评分、自动反馈与自动出题平台，不是新的自动机本体或新算法家族，因此适合归入 `📦/🏗️`。
