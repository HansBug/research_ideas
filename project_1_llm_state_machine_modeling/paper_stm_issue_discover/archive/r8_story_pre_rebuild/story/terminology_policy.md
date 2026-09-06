# terminology_policy.md — 术语口径

> 本文件是写作时的术语裁定表。凡本文件与其它 story 文件冲突，以本文件为准；
> 凡本文件与 [../discover_matrix/docs/protocol/](../../../discover_matrix/docs/protocol/) 下的判定
> 口径文档冲突，以后者为准——那里是机器判定的事实源，这里只管论文措辞。

## 1. ⚠️ 四组必须区分的易混术语

这四组一旦混用，读者会得出与数据相反的结论。它们排在最前面。

### 1.1 「作者」= 生成被评审模型的 LLM；「上游论文作者」= 人类

| 术语 | 指谁 | 用在哪 |
| :-- | :-- | :-- |
| **作者** author | 生成被评审模型的那个 LLM，即语料里 6 个生成方之一 | 「作者在 `stm0.puml` 里写了 `A or B`」 |
| **上游论文作者** upstream authors | 提供语料的那篇已发表实证研究的人类作者 | 「上游论文作者为每份需求人工撰写了参考模型」 |

**为什么关键**：一条额外产出算「表示债务」还是「真漏记」，取决于**生成该模型的 LLM 在它写
的 PlantUML 原文里究竟写没写那个东西**。把「作者」读成人类，整条判定链就断了。

### 1.2 生成方（6 个，属语料）vs 执行方（2 个，跑我们的方法）

| 轴 | 是谁 | 数量 | 我们控制吗 |
| :-- | :-- | --: | :-- |
| **生成方** generator | 写出被评审模型的 LLM：GPT-4o、GPT-4、Claude、DeepSeek、Kimi、Llama | 6 | 不控制，属语料 |
| **执行方** executor | 跑本方法的 LLM：`claude-opus-4-7`、`gpt-5.5` | 2 | 控制，是实验变量 |

⛔ 全文任何提到「模型」的地方，若不能立刻分辨是哪一轴，就必须加限定词。
「两个模型相差 4.4pp」指执行方；「6 个 LLM 各生成一份」指生成方。

### 1.3 `over_specification`（被评审模型多写了）vs 过度规定（我们的断言多要了）

**两者主体相反，方向相反，不可混谈。**

| 术语 | 谁多了 | 出现在哪 | v46 数量 |
| :-- | :-- | :-- | --: |
| 台账归因层 `over_specification` | **被评审模型**比需求多要求了东西 | 缺陷台账的四个归因层之一 | 6 条记录 |
| 多报侧「无需求依据」= **断言侧过度规定** | **我们的断言**要得比需求多 | 多报侧五类裁定之一 | 119 条目 / 67 去重 |

英文写作时建议用不同词根避免歧义：前者 `over-specified model`，后者
`over-demanding assertion` 或 `assertion-side over-specification`。

### 1.4 三层计数单位：条目 / 去重 / 逐格

| 单位 | 是什么 | v46 数量 |
| :-- | :-- | --: |
| **逐格 issue** | 方法发布的一条发现，同一条发现在 6 个格里算 6 条 | 1105 |
| **簇（条目）** | 同一 pair 内指向同一元素、陈述同一命题的产出合并为一簇 | 未认领 304，进入分析 288 |
| **去重组** | 同一 pair 内根因相同的多个簇再合并一层 | 124 |

⛔ **1105 与 288 分母不同质，不可相除算「误报率」。** 多报侧全部比例在 288 内部计算。
⛔ **条目份额与去重份额不可互换**，引用时必须写清用的是哪一套；两套给出**相反的主要矛盾**。

## 2. 推荐术语表

### 2.1 任务与对象

| 中文 | English | 口径 |
| :-- | :-- | :-- |
| 状态机模型的问题发现 | state-machine issue discovery | 本文任务。不含修复 |
| 自然语言需求 | natural-language requirement `NL` | 输入之一，义务的来源 |
| 被评审模型 | model under review / `STM_0` | 输入之二，唯一的求值对象 |
| 参考模型 | reference model | 上游论文作者人工撰写。**只在人工标注台账时用过，方法全程不使用** |
| 建模对象 | modeling scope $M = (S, E, V, Tr, A)$ | 见 [model_scope.md](./model_scope.md) |
| 中间表示 | intermediate representation | 带形式语义的状态机 DSL；求值介质，**不是贡献** |
| 表示债务 | representation debt | 编译（PlantUML → DSL）造成的信息损失，非模型缺陷、非方法误判 |

### 2.2 方法内部

| 中文 | English | 口径 |
| :-- | :-- | :-- |
| 义务 | obligation | 从需求原文拆出的一条待验证要求。是断言的上游 |
| 需求条目 | requirement item | 拆分后的一条，带 `verification_kind`、量词、触发、结果、覆盖义务 |
| 闭合谓词词表 | closed predicate vocabulary | 19 个先验定义的谓词，不可自造 |
| 谓词族 | predicate family | 结构（10）/ 仿真（6）/ 有界模型检查（3）。实现里 FBMCQ 指第三族 |
| 断言 | assertion | 一条谓词调用。角色分 `primary` / `supporting` |
| 定向反馈 | targeted feedback | 审查者给出「哪条不合格、缺什么、期望什么形状」；**不是重试** |
| 拒答 | refusal / `UnsupportedEvidence` | 谓词无法给出可靠真值时返回拒答，而不是猜真假 |
| 覆盖缺口 | coverage gap | 某条义务无法用闭合词表表达时的显式记录 |
| 降级 | degradation | 内部配额耗尽时封存已有产物并落盘，**不中止、不丢弃** |
| 归因绑定 | attribution binding | 把每个求值为假挂回它依赖的模型元素 |
| 发现 / issue | published issue | 过了结果裁决、正式发布的一条 |
| 回归防护 | regression guard | 求值为真的那部分断言构成的保护面 |

### 2.3 评测侧

| 中文 | English | 口径 |
| :-- | :-- | :-- |
| 缺陷台账 | expected issue ledger | 人工标注的已知缺陷集，是覆盖率的分母 |
| 归因层 | attribution layer | `nl_named` / `nl_contradiction` / `wellformedness` / `over_specification` |
| 判定位 | verdict bit | (台账记录, 执行模型, 轮) 三元组 |
| 格 | cell | 一次完整运行 = 一个 pair × 一个执行模型 × 一轮 |
| 命中 | hit | 我们的断言所表达的命题与台账那条**指向同一个作者源缺陷** |
| 多报侧 | over-report side | 未被任何台账记录认领的产出 |

## 3. 指标的写法

| 指标 | 定义 | 必须怎么写 |
| :-- | :-- | :-- |
| `hit@1` | 命中位 / 判定位总数 | **必须带 $\le$**：可写的只有 $\mathrm{hit@1} \le 60.4\%$ |
| `hit@3` | 三轮至少命中一次的 (记录, 执行模型) 比例 | 「该缺陷是否在能力范围内」 |
| `hit@all` | 三轮全部命中的比例 | 「稳定性」。说「稳定命中」时指的必须是 `hit@all = 1` |

⛔ **三者必须同时报。** `hit@3` 高而 `hit@all` 低 = 能力够、稳定性不足；两者都低才是能力问题。
⛔ **不得写成点估计或区间估计。** 已知扣除项只给出上界方向，下界取决于尚未做的对称审计；
写成区间等于宣称了一个并不掌握的下界。
⛔ **覆盖率必须与算力代价一起给**（每命中位约 48k 输出 token）。

## 4. 禁用或降级术语

| 术语 | 当前处理 |
| :-- | :-- |
| 多轮 Repair-Confirm、B-final、post-Confirm export | **禁止**出现在本文方法或贡献中。repair 是后续论文 |
| closure audit / regression audit（作为主线） | **禁止**作为本文的方法阶段或评价框架 |
| 「loop + verification feedback 是 headline contribution」 | **禁止**。已被 2026-08-07 / 08-08 定调取代，见 [paper_story.md](./paper_story.md) §Contributions |
| Better STM / which STM is better / relatively better | **禁止**作为 active 框架；只允许在解释历史转向时出现 |
| `fcstm` / `pyfcstm` 是贡献 | **禁止**。中间表示是介质 |
| ledger / audit / 证据簿记是贡献 | **禁止**。属方法支撑与评价纪律 |
| conversion gain | **禁止**。编译只是输入准备，且它自身有损耗（表示债务） |
| 「误报率」 | **禁止**用于多报侧整体。逐条读完后该读法是错的——占比最大的一块既不是模型缺陷也不是方法误判 |
| model runnable = correct | **禁止** |
| 「这些模型没有并发 / 时间问题」 | **禁止**。我们排除的是无法判断的部分 |
| 「谓词 X 不好用」 | **禁止**据 `hit@1` 分层得出。谓词与缺陷类型高度共线，要变成选型建议必须先做词表消融 |
| 「有界模型检查没有用」 | **禁止**。正确说法是「这批语料缺乏足以到达该层面的案例」 |

## 5. 写作替换规则

| 避免写法 | 推荐写法 |
| :-- | :-- |
| 发现并修复模型缺陷 | 发现模型不符合需求之处，并把每条发现落成可机械求值的断言 |
| 我们的方法误报了 N 条 | 未被台账认领的 N 条，逐条裁定后落入五类；最大一块是评审入口的编译损失 |
| 方法找到了 60.4% 的缺陷 | 在一个**已知不完整**的分母（98 条）上，$\mathrm{hit@1} \le 60.4\%$ |
| LLM 直接报缺陷 | 由需求条目转换而来的断言在被评审模型上求值，为假者挂钩 issue |
| 变量未声明是一条发现 | ⚠️ 该谓词在 PlantUML 语料上不具判别力，属上界成因，须单独扣除 |
| folded event 是错误 | 融合事件是编译压缩的结果，需回读作者源判断是表示债务还是真缺陷 |
| 这套流程可以自动修复模型 | 每条发现带可执行判据与闭合证据链，**因而便于后续修复与回归确认**（讨论一节，一小段） |

## 6. 中英一致性

- 首次出现写「已发布的问题（published issue）」，之后可简写 issue。
- `hit@1` / `hit@3` / `hit@all`、`primary` / `supporting`、`nl_named` 一类字段名保留英文原形，
  与判定表和 run record 对齐。
- 「表示债务」（representation debt）首次出现必须附英文，因为它与既有文献的
  spurious counterexample、program representation fault 同构，需要让审稿人挂上钩。
- 谓词名一律保留英文原形（`reaches`、`occupancy_after`……），中文只作括注。

## 7. 相对上一版改了什么、为什么

| 改动 | 为什么 |
| :-- | :-- |
| 新增 §1 四组易混术语，置于最前 | 旧版没有这一节；这四组是实际发生过误读的地方（尤其「作者」与两个方向相反的「过度规定」） |
| 新增 §2.2 方法内部术语（义务、断言角色、拒答、覆盖缺口、降级、回归防护） | 旧版术语表停在 repair 生命周期上，完全没有覆盖当前流水线的概念 |
| 新增 §3 指标写法（含 $\le$ 强制、三口径同报、算力同报） | 旧版无指标口径条款；而 `hit@1` 的上界性质是本文最容易被写错的一处 |
| 删除 raw/source `STM_0`、candidate / confirmed issue、issue-grounded repair、canonical source export、B-confirm、closure / regression audit、untraceable projection 等 repair 期术语 | paper1 收窄为 discover |
| **保留并迁移**：Better STM / `fcstm` contribution / ledger contribution / conversion gain / `model runnable = correct` / `objective metric proves improvement` 六条禁用条款 | 这些禁令与当前口径不冲突，且仍然防的是真实的措辞回流风险 |
| **保留并改写**：「folded event 是错误」这条替换规则 | 旧版理由是「需 source-level 确认」；新版理由更具体——它是编译压缩的结果，判定要回读作者源 |
| 「参考模型」条目新增「方法全程不使用」 | 这是实验公平性的核心事实，必须钉在术语表里 |
