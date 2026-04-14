# PPT Guide

## Deck Brief

- Title: `2026-04-15-讨论`
- Goal: `让导师在会后明确同意、修正或否决三件事：本学期先收束 project_1；论文对象先限定在离散 control-state layer；pyfcstm 与 pyudbm 在博士主线里的角色分工。`
- Audience: `导师；默认熟悉博士研究总体方向，但未必跟进到最近 6 周的文库整理、仓库推进与问题收束判断。`
- Duration Minutes: `18-20`
- Slide Budget: `20`
- Aspect Ratio: `16:9`
- Style Constraints: `正式学术汇报风格；中文为主；代码、仓库名和术语使用 monospace；标题使用 Noto Serif CJK SC，正文使用 Noto Sans CJK SC；配色以 deep navy、teal、rust、sand 为主；避免“标题 + 一个数字”式空页；尽量用图表、表格、关系图和结论卡片。`
- Tooling Backend: `Python + python-pptx`
- Notes Policy: `最终 deck 必须嵌入 speaker notes；notes 等于可直接念的完整台词，加上显式标明的 notes supplement。`
- Audience Language: `中文`
- Source Materials:
  - `../prep/briefing.md`
  - `../prep/materials.md`
  - `../../../TARGET.md`
  - `../../../project_1_llm_state_machine_modeling/README.md`
  - `../../../project_1_llm_state_machine_modeling/baselines/SUMMARY.md`
  - `../../../project_1_llm_state_machine_modeling/sources/SUMMARY.md`
  - `../../../project_1_llm_state_machine_modeling/state_machine_types/SUMMARY.md`
  - `../../../project_1_llm_state_machine_modeling/discussions/*.md`
- Acceptance Criteria:
  - `必须严格生成 20 页。`
  - `至少 10 页以图表、表格或关系图为主，不允许全 deck 退化成 bullet list。`
  - `所有关键数字都能回溯到 briefing 或其引用源。`
  - `每页必须有 speaker notes。`
  - `必须明确回答“为什么这学期先做 project_1”“为什么对象先收束到离散 control-state”“pyfcstm 与 pyudbm 各自处于什么位置”三件事。`
  - `最后一页必须落到可讨论、可拍板的问题，而不是泛泛总结。`

## Document Purpose And Usage

- 这份 guide 是该 deck 的上游事实源；叙事、页序、讲稿、结论口径优先改这里。
- `generate_ppt.py` 负责把这里的页级意图落成具体版式、图表、表格和 notes。
- 如果后续导师要求增删页，先改本文件的 slide plan，再改 generator。
- 如果只需要局部调布局、缩放图表、改颜色或间距，先改 generator。

## Timing Plan

- `s01-cover`: `0:25`
- `s02-agenda`: `0:35`
- `s03-summary`: `1:10`
- `s04-why-project1-now`: `1:00`
- `s05-four-project-map`: `0:55`
- `s06-project1-evidence-chain`: `0:55`
- `s07-baselines-overview`: `0:55`
- `s08-baseline-evidence`: `1:15`
- `s09-sources-curation`: `0:55`
- `s10-sources-stats`: `1:05`
- `s11-sources-main-types`: `1:00`
- `s12-sources-time-structure`: `1:00`
- `s13-sources-examples`: `1:05`
- `s14-sm-family`: `0:55`
- `s15-control-state-definition`: `1:15`
- `s16-pyfcstm-progress`: `0:55`
- `s17-pyfcstm-role`: `1:00`
- `s18-pyudbm-progress`: `1:00`
- `s19-infra-feedback`: `1:05`
- `s20-decisions-next-steps`: `1:20`

## Global Production Principles

- 每页只讲一个主要判断，标题必须是结论句，而不是泛泛栏目名。
- 表格里凡是统计项，必须配定义或解释列；不能只写名词和数字。
- 需要用显式视觉层级区分：事实、判断、结论、待讨论项。
- `sources/` 相关页必须明确说明“这是治理后的样本主集，不是领域自然分布”。
- `project_1` 相关页必须把三条文库线和 `pyfcstm` 的关系说清楚，而不是平铺堆料。
- `project_3` 页必须既说明 `pyudbm` 已经做了什么，也说明为什么它还不足以支撑这学期主投稿。
- `pyfcstm` 页不能把它写成“最近写了一个工具”，必须写成目标形式主义与基础设施。
- 所有页都保留小号 evidence footer，标明主要依据来源编号。
- 关键证据页必须显式写出“前因 / 因此”或等价因果条，避免只剩结论和数字。
- internal slide id 只出现在 guide、code 和 review notes 中，不出现在可见幻灯片里。

## Slide Plan

### s01-cover

- Target Duration: `0:25`
- Cumulative Time: `0:25`
- Title: `2026-04-15-讨论`
- Subtitle: `当前进展、问题收束与下一步投稿判断`
- Message: `这是一场为收束问题对象和投稿主线服务的进展对齐，而不是一次平均铺开的阶段汇报。`
- Visible Text:
  - `日期：2026-04-15`
  - `三枚主题 chips：project_1 优先级 / pyfcstm vs pyudbm / control-state 定义`
  - `右侧四个 project 状态卡：建模、性质生成、verification、repair`
- Visuals:
  - `左侧大标题；右侧四个纵向 status cards；底部放主题 chips。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `今天我想把最近已经落地的材料、现在真正卡住的问题，以及我对下一步投稿主线的判断放在一条线上讲。`
  - `重点不是把四个 project 都平均展开，而是想和您先对齐本学期应该先收束哪一个问题。`
- Notes Supplement:
  - `开场控制在 25 秒，先把讨论目的说清楚。`
- Implementation Notes:
  - `封面不要塞正文；右侧 status cards 只放一句话标签和成熟度。`
- Acceptance Checks:
  - `三秒内看懂主题、日期和汇报焦点。`
  - `封面有正式学术汇报感，不像课程作业首页。`
- Generator-Ready Instructions:
  - `使用 blank layout；左侧标题占约 55% 宽度；右侧放四个竖向卡片；底部三枚圆角 chips。`

### s02-agenda

- Target Duration: `0:35`
- Cumulative Time: `1:00`
- Title: `明天这次讨论，我最希望先对齐三个决策`
- Subtitle: `先拍板问题边界，再决定论文如何写和接下来 6 周怎么推`
- Message: `整场讨论的目标是形成可执行决策，而不是继续把信息摊得更散。`
- Visible Text:
  - `决策 1：这学期主投稿是否明确锁定 project_1`
  - `决策 2：论文对象是否先限定为离散 control-state layer`
  - `决策 3：pyfcstm 与 pyudbm 是否分别承担建模基座和验证后端地基`
  - `下方一条四段式流程：结论 -> project_1 证据 -> 基础设施 -> 待拍板事项`
- Visuals:
  - `上方三张大决策卡；下方一条 agenda band。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `所以我这次不会按目录顺序把所有事情轮流过一遍，而是按三个需要拍板的决策组织材料。`
  - `后面的每一页都服务于这三个问题中的至少一个，不会单独做信息堆砌。`
- Notes Supplement:
  - `指出三张卡时，从左到右念。`
- Implementation Notes:
  - `三卡片上方用大号序号；agenda band 用四段不同 accent。`
- Acceptance Checks:
  - `看完这一页后，观众知道后面不是泛汇报，而是带着问题来。`
  - `三项决策足够明确，后面内容能自然映射到它们。`
- Generator-Ready Instructions:
  - `三列决策卡占上半页；下半页放四段流程带和一句总括。`

### s03-summary

- Target Duration: `1:10`
- Cumulative Time: `2:10`
- Title: `当前最缺的不是材料，而是把问题对象收束清楚`
- Subtitle: `一页结论先给出来，后面逐页用文库与仓库证据补强`
- Message: `已经积累的材料足以支撑一篇会议论文，但前提是把“控制系统状态机”界定得更稳。`
- Visible Text:
  - `结论 1：这学期第一优先级应先把 project_1 发出去`
  - `结论 2：project_1 目前真正缺的是问题收束，而不是样本`
  - `结论 3：论文对象应先落到离散 control-state layer`
  - `结论 4：pyfcstm 应被写成 executable control-state infrastructure`
  - `结论 5：project_3 的实质推进主要在 pyudbm，但还缺 verifyta 核心搜索`
  - `结论 6：LLM-based modeling 的真正杀手锏是基础设施反馈`
- Visuals:
  - `六张 2x3 conclusion cards；底部一条 take-home banner：先收束对象，再拉厚实验。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `如果先把这一页压缩成一句话，就是现在材料并不少，真正决定论文能不能站住的，是问题边界能不能先收紧。`
  - `后面我会分别用 project_1 的三条文库线、pyfcstm 和 pyudbm 的现状，以及几篇 baseline 的结果，把这六点判断展开。`
- Notes Supplement:
  - `六张卡逐张不要展开太多，每张一句即可。`
- Implementation Notes:
  - `每张卡只保留一句短结论，不要把整段 briefing 原文搬上来。`
- Acceptance Checks:
  - `整页在 10 秒内能读出 6 个判断。`
  - `底部 take-home banner 必须显眼。`
- Generator-Ready Instructions:
  - `做成 2x3 结论卡网格；每卡左上角有序号，右下角留一行极短解释。`

### s04-why-project1-now

- Target Duration: `1:00`
- Cumulative Time: `3:10`
- Title: `站在本学期投稿窗口看，只有 project_1 适合先冲出去`
- Subtitle: `近端会议时间窗口 + 当前准备度 两条线必须同时看`
- Message: `project_1 既有问题定义基础，又赶得上最近端的 conference-style 写法；其余项目当前更适合作为支撑线。`
- Visible Text:
  - `时间窗口参考：RE 2025 = 2025-03-10；MoDELS 2025 = 2025-04-03；ASE 2025 = 2025-05-30`
  - `当前判断：RE / MoDELS 节奏已基本过去，ASE-style 表达仍是近端最现实窗口`
  - `四个 project readiness bars：project_1 最高；project_3 有后端地基但原型未成；project_4 最不适合先发`
  - `页面结论：先拿下一篇 focused paper，不追求一次覆盖四个问题`
- Visuals:
  - `上半页时间轴，标出 2026-04-14 当前点和若干 prior-year 参考 deadline；下半页四条 readiness bars。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `如果只看博士全局，四个方向都重要；但如果加上这学期必须先发出第一篇会议论文这个约束，当前只有 project_1 同时具备问题、材料、baseline 和基础设施落点。`
  - `我这里故意把 prior-year 的具体日期写上来，是为了说明这是按现实投稿节奏倒推出来的判断，而不是抽象偏好。`
- Notes Supplement:
  - `强调 2026 官方 CFP 仍要临投稿前回官方页面再核对。`
- Implementation Notes:
  - `时间轴不要太花；重点是当前点与 prior-year 窗口的相对位置。`
- Acceptance Checks:
  - `观众能直接看出 project_1 是近端唯一合理主线。`
  - `时间窗口里必须出现具体日期，不能只有“最近”或“快到了”这类词。`
- Generator-Ready Instructions:
  - `时间轴放上半页；deadline band 用 5 个 venue cards；下半页用四个水平 readiness bars。`

### s05-four-project-map

- Target Duration: `0:55`
- Cumulative Time: `4:05`
- Title: `四个 project 是一条闭环，但近端主线必须先落在 project_1`
- Subtitle: `先把建模对象和目标形式主义立住，后面的 scenario、verification、repair 才有共同基座`
- Message: `博士研究仍然是“生成-验证-修复”闭环，只是当前最先要打实的是第一段。`
- Visible Text:
  - `闭环流程：需求/描述 -> 建模 -> 性质/场景 -> 验证 -> 修复`
  - `project_1：目标对象、baseline、样本与 pyfcstm`
  - `project_2：性质与场景生成接口层`
  - `project_3：profile-based verification 与 timed backend`
  - `project_4：缺陷驱动迭代修复`
- Visuals:
  - `横向闭环流程图；四个 project cards 依次挂到对应节点；project_1 高亮。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `我并不是要把 project_2 到 project_4 否掉，而是想强调这几条线现在是前后依赖关系，不是并列比赛。`
  - `只要 project_1 的对象和目标形式主义没有先立稳，后面的验证和修复就很难围绕同一个模型对象做。`
- Notes Supplement:
  - `指流程图时按左到右。`
- Implementation Notes:
  - `流程图比文字更重要；每个 project card 只放一句角色说明。`
- Acceptance Checks:
  - `能看出闭环关系，也能看出 project_1 被高亮而不是被孤立。`
- Generator-Ready Instructions:
  - `用 5 节点流程带 + 4 张 project cards；project_1 卡片面积略大。`

### s06-project1-evidence-chain

- Target Duration: `0:55`
- Cumulative Time: `5:00`
- Title: `project_1 的说服力来自三条文库线加上一条基础设施线`
- Subtitle: `不是平行摆设，而是共同回答“该建什么、凭什么、如何落地”`
- Message: `baselines、sources、state_machine_types 和 pyfcstm 分别承担比较、数据、类型选型和可执行落地。`
- Visible Text:
  - `baselines：别人现在怎么做，和谁比`
  - `sources：真实控制系统设计文本长什么样，数据集从哪里来`
  - `state_machine_types：状态机家族到底有哪些，为什么要主动选型`
  - `pyfcstm：目标形式主义 / executable IR / 闭环基础设施`
  - `汇总判断：三条文库线共同把论文对象压向 control-state problem`
- Visuals:
  - `四张 role cards 围绕中央结论节点；每张卡片带数量与一句职责。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页是 project_1 的整体索引。三条文库线加上一条仓库线，分别回答比较对象、真实样本、类型选型和落地基座。`
  - `也正因为这四件事现在都已经有基础，我才认为 project_1 已经具备先写成论文的条件。`
- Notes Supplement:
  - `中央结论节点最后再读一次。`
- Implementation Notes:
  - `中央用一个深色 conclusion node，四周四卡片用不同 accent。`
- Acceptance Checks:
  - `四条线各自的任务边界清楚，不会被误读成“都在做文献堆积”。`
- Generator-Ready Instructions:
  - `中央圆角大节点；四角四张卡；用箭头指向中央。`

### s07-baselines-overview

- Target Duration: `0:55`
- Cumulative Time: `5:55`
- Title: `baselines/ 解决的是“该和谁比，以及差距究竟在哪里”`
- Subtitle: `这不是领域均匀采样，而是围绕 project_1 可比性刻意筛出的比较集`
- Message: `baseline 文库已经足够支撑“直接比较对象 + 邻近任务对象 + 方法启发对象”的分层讨论。`
- Visible Text:
  - `总量：62 篇`
  - `状态分布：🟢 14 / 🟡 19 / 🟠 29`
  - `筛选口径：优先保留 direct baseline 与任务邻近条目`
  - `页面结论：baseline 已经够用，关键是挑最有说服力的绿色条目来讲`
- Visuals:
  - `左侧一张状态分布图；右侧三张 role cards：direct baseline / 邻近任务 / 方法启发。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `我不打算明天把 62 篇 baseline 都摊开，而是想把它说成一个经过筛选的比较集。`
  - `这里更重要的不是总数，而是我们已经能清楚地区分哪几篇能直接比、哪几篇提供邻近任务证据、哪几篇提供 workflow 启发。`
- Notes Supplement:
  - `强调不是自然分布。`
- Implementation Notes:
  - `分布图可以是 donut 或 column，但必须能清楚看出绿色条目数量有限而关键。`
- Acceptance Checks:
  - `看完后不会误以为 baseline 文库只是数量堆积。`
  - `必须出现 62、14、19、29 四个数字。`
- Generator-Ready Instructions:
  - `左 40% 放 chart；右 60% 放三张 role cards 与一句 take-home。`

### s08-baseline-evidence

- Target Duration: `1:15`
- Cumulative Time: `7:10`
- Title: `baseline 的共同趋势不是更花的 prompt，而是更强的工具反馈`
- Subtitle: `几篇最值得讲的绿色条目给出的实证指向相当一致`
- Message: `纯 prompt 可以做出骨架，但真正把质量拉起来的，越来越是 workflow、model checking、仿真和工具链反馈。`
- Visible Text:
  - `图 1：2026 direct baseline 的 F1 对比：0.7029 / 0.5431 / 0.6559`
  - `图 2：SysML empirical study 的错误修复率：94.6 / 88.0 / 43.1 / 37.3`
  - `图 3：TTool AI 的评分与效率：63 vs 58；15.2x；81 vs 70；67.5x`
  - `页面结论：workflow feedback > prompt tricks`
- Visuals:
  - `左中两张小型柱状图；右侧两张 evidence cards，总结 TTool AI 与 IEC 61499 论文结论。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这页我想用几组最硬的数字把一个趋势说明白：一次生成当然有用，但它很快会卡在 action、复杂约束和语义一致性这些地方。`
  - `一旦工作流里引入模型检查、格式校验、仿真或工具链反馈，结果就会明显更稳，所以我越来越不相信纯 prompt 会是长期答案。`
- Notes Supplement:
  - `提及 IEC 61499 那篇时，用一句话说明“接上仿真和代码生成后，方法性质就变了”。`
- Implementation Notes:
  - `三个 evidence 区要同一视觉系统；数字必须大，解释尽量短。`
- Acceptance Checks:
  - `这页必须至少出现两张图和两张数据卡，避免文字过密。`
  - `观众能一眼抓到“反馈闭环更重要”这个结论。`
- Generator-Ready Instructions:
  - `左 2/3 放两个 chart；右 1/3 放 evidence cards；底部放一句总括带。`

### s09-sources-curation

- Target Duration: `0:55`
- Cumulative Time: `8:05`
- Title: `sources/ 不是自然分布样本，而是面向数据集建设的治理后主集`
- Subtitle: `如果不先说明这一点，后面的统计就很容易被误读`
- Message: `sources 文库当前的分布首先反映的是收录策略和数据集治理目标，其次才是领域文献现象本身。`
- Visible Text:
  - `前因 / 因果条：如果不先讲治理口径，后面所有分布都会被误读成自然分布；因此这一页先解释筛选逻辑。`
  - `三阶段流程：广撒网检索 -> 标准化治理 -> 主集保留`
  - `治理目标：优先保留 EFSM/HSM、T0/T1、细节充实度高、不过度强趋同的案例`
  - `五套口径：论文级可用性 / 案例级角色 / 细节充实度 / 主类型 / 时间级别`
  - `警告条：不要把当前分布读成“控制系统天然如此”`
- Visuals:
  - `顶部一条 warning ribbon；其下再放一条前因/因此因果条；左侧 funnel；右侧 standards table。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `sources 这一块我觉得必须先把方法论讲清楚，因为后面的 EFSM、HSM、T0、T1 占比很容易被误会成领域自然分布。`
  - `实际上它已经是一个治理后的样本主集，目标就是服务后续数据集和论文对象收束。`
- Notes Supplement:
  - `warning ribbon 要点出来。`
- Implementation Notes:
  - `warning ribbon 用 rust accent；右侧 table 要短而清楚。`
- Acceptance Checks:
  - `这一页必须明确说明“不是自然分布”。`
  - `五套治理口径至少出现名称，不可只给 funnel。`
- Generator-Ready Instructions:
  - `上方 warning ribbon；左 45% funnel；右 55% standards table。`

### s10-sources-stats

- Target Duration: `1:05`
- Cumulative Time: `9:10`
- Title: `sources/ 的总体统计已经足以支撑数据集和问题边界判断`
- Subtitle: `统计项必须带定义列，否则数字没有解释力`
- Message: `不仅数量大，而且统计口径已经足够稳定，能直接支撑对样本主链的判断。`
- Visible Text:
  - `前因 / 因果条：样本主链已经够厚；因此这一页要证明我们不再处在“先去找样本”的阶段。`
  - `四个 big numbers：787 papers / 715 paper-level green / 746 positive cases / 685 core cases`
  - `表 1：论文级总体统计，列为指标 / 定义 / 数量`
  - `表 2：案例级保留角色统计，列为类别 / 定义 / 数量`
  - `底部 take-home：样本主链已经足够厚，不再是“先去找样本”的阶段`
- Visuals:
  - `标题下先放因果条；上排四个 big-number cards；下排两张解释性表格。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `我这里故意把表格做成“指标加定义”的形式，因为如果只有标题和数字，导师很难判断这些统计到底在说明什么。`
  - `现在这组数字最重要的意义是：样本主链已经够厚，真正该做的是围绕它定义论文对象和评测口径。`
- Notes Supplement:
  - `先念 big numbers，再看下方两张表。`
- Implementation Notes:
  - `big-number cards 的单位和标签要清楚；表格字号不能小于 10pt。`
- Acceptance Checks:
  - `必须出现定义列。`
  - `不能把 paper-level 和 case-level 混成一张糊表。`
- Generator-Ready Instructions:
  - `上 35% 放 4 卡；下 65% 放 2 张表，左右各一张。`

### s11-sources-main-types

- Target Duration: `1:00`
- Cumulative Time: `10:10`
- Title: `主类型分布说明真实样本主链是 FSM / EFSM / HSM`
- Subtitle: `713 / 746 条正例都落在离散控制状态层附近`
- Message: `当前最稳的建模对象不是 protocol、resource-flow 或 hybrid，而是离散控制状态层主链。`
- Visible Text:
  - `前因 / 因果条：主类型分布不只是数字，它直接决定论文对象如何收束；因此要把这页读成“control-state 主链占绝对主体”。`
  - `柱状图类别：FSM 127 / EFSM 429 / HSM 157 / Protocol 4 / Resource-flow 13 / Hybrid 16`
  - `右侧说明表：每种主类型的定义`
  - `结论卡：713 / 746 = 95.6% 落在 FSM + EFSM + HSM`
- Visuals:
  - `标题下先放因果条；左侧横向柱状图；右侧 definitions table；底部 conclusion card。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页其实是在回答“为什么我想把论文对象先收束到 control-state layer”。`
  - `因为当前主集里绝大多数正例都还是围绕离散阶段、guard、变量和层次结构展开，真正需要 hybrid 语义的只是很小的一部分。`
- Notes Supplement:
  - `念 713/746 这个比例时停顿一下。`
- Implementation Notes:
  - `横向柱状图类别名保持简短；定义表只写一行定义。`
- Acceptance Checks:
  - `EFSM 必须显著高于其他类别。`
  - `结论卡清楚强调 95.6% 这个比例。`
- Generator-Ready Instructions:
  - `左 50% chart；右 50% 定义表和结论卡。`

### s12-sources-time-structure

- Target Duration: `1:00`
- Cumulative Time: `11:10`
- Title: `时间级别与结构标签说明“离散控制”不等于“扁平简单 FSM”`
- Subtitle: `T0/T1 占主导，但显式时钟与层次结构都不是小噪声`
- Message: `本学期论文可以先做离散 control-state，但绝不能把目标对象退化成最简单的平面 FSM。`
- Visible Text:
  - `前因 / 因果条：离散主链并不意味着简单模型；因此必须把 timer 与 hierarchy 一起保留下来。`
  - `时间级别：T0 352 / T1 367 / T2 15 / T3 12`
  - `结构标签：显式时钟 243 / 层次 160 / 连续耦合 71`
  - `结论 1：T0 + T1 = 719 / 746`
  - `结论 2：显式时钟与层次关系必须保留`
- Visuals:
  - `标题下先放因果条；左侧时间级别图；右侧结构标签图；底部双结论卡。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `如果只看前一页，很容易把它误解成“那我们就做最普通的 FSM 就行了”。`
  - `这一页要强调的是，主链虽然是离散 control-state，但里面大量样本仍然带有局部 timer、显式时钟和层次关系，所以目标形式主义必须比扁平 FSM 更强。`
- Notes Supplement:
  - `先看左侧时间，再指右侧结构标签。`
- Implementation Notes:
  - `两个图的尺度不同，避免放进同一张坐标系；用底部两张结论卡收束。`
- Acceptance Checks:
  - `必须同时看到 T0/T1 主导与显式时钟/层次显著存在这两个事实。`
- Generator-Ready Instructions:
  - `左右双图并排；底部两张 take-home cards。`

### s13-sources-examples

- Target Duration: `1:05`
- Cumulative Time: `12:15`
- Title: `代表样本显示：真实控制系统里至少并存五类不同建模难点`
- Subtitle: `同样都叫“状态机”，但它们的主难点并不相同`
- Message: `样本例子能更直观地说明为什么论文对象必须主动收束，而不能把所有“状态机”一股脑并进来。`
- Visible Text:
  - `顶部一句 framing：这些样本不是用来“凑例子”，而是用来说明“状态机”一词背后其实罩着不同问题。`
  - `五个代表样本：洗衣机 PLC / 电梯 PLC / 铁路联锁 / UAV 分层任务 / 外骨骼步态控制`
  - `表格列：场景 / 标签 / 关键建模难点 / 对论文对象的启发`
  - `底部总结：离散顺序控制、门控联锁、层次任务、连续耦合至少是四种不同问题`
- Visuals:
  - `顶部 framing sentence；主体是一张 5x4 的代表样本解释表；右下角一张结论卡。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这页我想用几个很具体的系统把抽象统计落地。`
  - `它们之所以重要，不是因为每个例子都要拿去做实验，而是因为它们把“状态机”这个词背后其实罩着几类不同问题，展示得非常直观。`
- Notes Supplement:
  - `五个样本只挑两三个展开说，不要每行都讲。`
- Implementation Notes:
  - `表格不能太密；最后一列用一句判断，不要写成长段。`
- Acceptance Checks:
  - `例子必须覆盖离散顺序控制、层次任务和连续耦合至少三类。`
  - `表格仍然可读，不应缩成论文附录字体。`
- Generator-Ready Instructions:
  - `大表格占主体；底部右侧附结论卡。`

### s14-sm-family

- Target Duration: `0:55`
- Cumulative Time: `13:10`
- Title: `state_machine_types/ 证明“状态机”是一整个家族而不是单对象`
- Subtitle: `问题不在于有没有状态机，而在于我们到底主动选择其中哪一支`
- Message: `状态机家族谱系已经足够清楚，这恰好给论文对象收束提供了理论依据。`
- Visible Text:
  - `前因 / 因果条：既然“状态机”本来就是家族，project_1 就不能假装目标对象天然唯一；因此必须主动选 control-state + infrastructure 这条分支。`
  - `柱状图类别：经典离散状态机 160 / 时间自动机 96 / 混成随机 46 / Petri 网 28 / 接口契约 31 / DSL 59 / 标准与元模型 264`
  - `右侧 family tree：control-state / timed / hybrid / interaction-resource / infrastructure`
  - `结论：现代状态机研究越来越多地落在 profile、DSL、元模型与执行载体上`
- Visuals:
  - `标题下先放因果条；左侧分布图；右侧分支图，突出 control-state 与 infrastructure 两支。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这条文库线给我的最大启发是，现代状态机研究早就不是只在发明新形式主义，而是在发明 profile、DSL、元模型和执行基础设施。`
  - `这也正是 pyfcstm 为什么在学术叙事里可以有位置，因为我们其实是在主动选择并塑造一个适合 LLM 的 control-state profile。`
- Notes Supplement:
  - `右侧分支图最后落到 control-state + infrastructure。`
- Implementation Notes:
  - `family tree 要简洁；不要做成过度复杂的 taxonomy 海报。`
- Acceptance Checks:
  - `观众能看出“状态机是家族”而不是一条直线。`
  - `要明确把 infrastructure 这一支画出来。`
- Generator-Ready Instructions:
  - `左 chart 右 branch diagram；highlight control-state branch。`

### s15-control-state-definition

- Target Duration: `1:15`
- Cumulative Time: `14:25`
- Title: `这篇论文更稳的对象应是控制系统的离散 control-state layer`
- Subtitle: `离散监督 / 顺序控制 与 连续 / 混成控制 在建模视角上其实是两类问题`
- Message: `最稳妥的第一篇论文对象不是所有控制系统状态机，而是模式、阶段、互锁、恢复和局部工程定时这一层。`
- Visible Text:
  - `左列：离散监督 / 顺序控制 / 模式管理`
  - `右列：连续 / 混成控制中的模式切换`
  - `对比维度：典型系统 / 状态含义 / 核心难点 / 更自然模型 / 更自然反馈基础设施`
  - `底部结论条：project_1 先解左列问题，右列作为后续延展`
- Visuals:
  - `一张双色 2 列比较表；底部一条深色 conclusion ribbon。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页是整场汇报最关键的定义页。`
  - `我现在越来越不想把“控制系统状态机”当成一个大口袋，因为 sources 和 state_machine_types 已经证明，这个词至少罩着离散监督控制和连续混成控制两类完全不同的问题。`
  - `如果第一篇论文先把左边这列讲透，我觉得问题会更稳，也更容易做出可执行实验。`
- Notes Supplement:
  - `这页多停留几秒，等导师看表。`
- Implementation Notes:
  - `两列配色必须明显对比；左列用 project_1 accent，高亮为当前 focus。`
- Acceptance Checks:
  - `观众必须能明确看到“先做左列”这个结论。`
  - `表格不能只有名词，要写清楚五个维度。`
- Generator-Ready Instructions:
  - `整页大比较表；底部 conclusion ribbon 横跨全页。`

### s16-pyfcstm-progress

- Target Duration: `0:55`
- Cumulative Time: `15:20`
- Title: `pyfcstm 从 2 月底到现在已经具备可执行基础设施的骨架`
- Subtitle: `它已经不是单文件 demo 级 DSL，而是在往工程可维护对象走`
- Message: `pyfcstm 已经在模块化、执行语义、代码生成、工具支持和验证预备上形成一条连续能力带。`
- Visible Text:
  - `main HEAD：dcf1f70`
  - `五层能力：import / 模块化；执行语义；Python/C 模板；PlantUML + VS Code；solver/verify groundwork`
  - `页面结论：这不是“又写了个小工具”，而是一条 executable control-state infrastructure`
- Visuals:
  - `五列 capability cards + 一条从 2026-02-28 到 2026-04-14 的 progress rail。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `我想把 pyfcstm 的叙事从“最近写了不少功能”换成“已经形成了一个可执行控制状态基础设施骨架”。`
  - `现在它至少已经把模块化、运行语义、代码生成、工具支持和后续验证接口这些关键层都搭起来了。`
- Notes Supplement:
  - `main HEAD 可以快速带一下，不用停留。`
- Implementation Notes:
  - `进展页强调 capability layers，不做细碎 commit 列表。`
- Acceptance Checks:
  - `五层能力清楚可见。`
  - `观众能看出这是结构性推进，而不是零散 feature list。`
- Generator-Ready Instructions:
  - `顶部放 HEAD 与时间 rail；下方五张 capability cards。`

### s17-pyfcstm-role

- Target Duration: `1:00`
- Cumulative Time: `16:20`
- Title: `pyfcstm 在论文里应被写成目标形式主义与闭环基座`
- Subtitle: `把“自然语言生成状态机”提升成“自然语言生成可执行形式模型”`
- Message: `pyfcstm 的学术价值不在于工具实现，而在于它同时回答了目标对象、执行语义、行为隔离和后续闭环如何接入。`
- Visible Text:
  - `中央流程：需求文本 -> LLM -> pyfcstm control-state DSL -> parser/runtime -> simulation/codegen/verification hooks`
  - `四个贡献点：target profile / executable semantics / formal core vs abstract action / cross-project base`
  - `结论：pyfcstm 是 project_1 的研究答案之一`
- Visuals:
  - `中央管线图；左右两侧各两张更大的 contribution cards。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `如果论文里只是把 pyfcstm 当成实现细节，我觉得会浪费掉它最重要的研究意义。`
  - `它真正回答的是：我们到底让 LLM 生成什么对象，这个对象为什么既可执行、可校验，又适合作为后续验证和修复的共同基座。`
- Notes Supplement:
  - `指管线图时强调 parser/runtime 是第一层反馈。`
- Implementation Notes:
  - `中央管线图要一眼能看懂；贡献点每张卡只放短语，不放长句。`
- Acceptance Checks:
  - `观众会把 pyfcstm 理解成研究答案，而不是周边工具。`
- Generator-Ready Instructions:
  - `中心流程图横向铺开；左右各三张贡献卡。`

### s18-pyudbm-progress

- Target Duration: `1:00`
- Cumulative Time: `17:20`
- Title: `project_3 的实质推进主要在 pyudbm，但核心搜索仍缺`
- Subtitle: `backend 不是空白，只是还没长成第一版 profile-guided verifier`
- Message: `pyudbm 已在 UDBM、UTAP、query、官方样本和文献基础上推进很深，但 verifyta 级搜索与 witness 仍缺。`
- Visible Text:
  - `前因 / 因果条：project_3 容易被看成“还没动”；因此这一页要区分“backend 地基已经做了很多”和“完整 verifier 还没做出来”。`
  - `main HEAD：a8d0649`
  - `已具备：符号核 / 模型前端 / query + official corpus / 文献与路线`
  - `仍缺：symbolic reachability / A[] E<> 求值 / witness / verifyta 核心搜索`
  - `结论：project_3 应继续沉淀，但不应抢走本学期主投稿节奏`
- Visuals:
  - `标题下先放因果条；左侧 4 层 capability stack；右侧更疏朗的 gap table。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这页的目标是把 project_3 讲得既诚实又准确。`
  - `诚实的部分是它还没有完整验证器；准确的部分是它并不是空白，而是大量 timed backend 和文献整理工作已经集中在 pyudbm 里做了。`
- Notes Supplement:
  - `指出 178 个 official files 是样本地基。`
- Implementation Notes:
  - `左侧 stack 用绿色到黄色渐变；右侧 gap table 用一列红色突出“仍缺”。`
- Acceptance Checks:
  - `必须同时看到“已有很多”和“关键还没做完”这两点。`
- Generator-Ready Instructions:
  - `左 45% capability stack；右 55% gap table。`

### s19-infra-feedback

- Target Duration: `1:05`
- Cumulative Time: `18:25`
- Title: `我越来越相信基础设施反馈才是 LLM-based modeling 的真正杀手锏`
- Subtitle: `parser、runtime、simulation、model checking 和 regression traceability 会把问题性质彻底改变`
- Message: `与其继续拼 prompt，不如把模型输出放进能持续打分和回传反例的环境里。`
- Visible Text:
  - `前因 / 因果条：单次生成很快会碰到 action、语义一致性和可执行性瓶颈；因此真正把质量拉高的是反馈基础设施。`
  - `中央闭环：LLM -> control-state DSL -> parser/runtime -> simulator / checker / tests -> structured feedback -> LLM`
  - `四张 evidence cards：F1 对比 / 修复率 94.6 88.0 43.1 37.3 / 63 vs 58 & 15.2x / workflow principles`
  - `底部结论：quality grows with feedback infrastructure, not only prompting`
- Visuals:
  - `标题下先放因果条；中央循环箭头图；四周围绕四张 evidence cards。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `我现在最想强调的一点其实在这里。`
  - `这些 baseline 的共同证据都在提示同一个方向：让 LLM 单次想得更聪明当然有帮助，但真正把质量拉上去的，是 parser、仿真器、model checker 和 regression trace 这些基础设施提供的连续反馈。`
  - `这也是为什么我会越来越看重 pyfcstm 这类可执行目标对象。`
- Notes Supplement:
  - `中央闭环先念一圈，再看四张 evidence cards。`
- Implementation Notes:
  - `闭环图要比文字更醒目；四张 evidence cards 不要一样大，形成中心聚焦。`
- Acceptance Checks:
  - `必须一眼看到“反馈闭环”而不是“四篇论文拼贴”。`
  - `页面上要出现至少三组硬数字。`
- Generator-Ready Instructions:
  - `中心做循环图；四角做 evidence cards；底部一条强结论 ribbon。`

### s20-decisions-next-steps

- Target Duration: `1:20`
- Cumulative Time: `19:45`
- Title: `如果明天拍板这五件事，后续 6 周的推进路径会更稳`
- Subtitle: `收束问题对象、拉厚实验、准备 conference-style 论文`
- Message: `现在最需要的不是更多开放问题，而是把主线固定下来并倒排接下来 6 周。`
- Visible Text:
  - `上方时间线：第 1-2 周收束问题定义与论文主张；第 3-4 周固化样本与 baseline 实验；第 5-6 周完成初稿与 venue 策略`
  - `五个待拍板问题：`
  - `1. 本学期主投稿是否锁定 project_1`
  - `2. 论文对象是否先限定为离散 control-state layer`
  - `3. pyfcstm 是否正面写成 target formalism / executable IR`
  - `4. pyudbm 是否继续做 backend 地基而不抢主线`
  - `5. 近端写法是否按 ASE-style automation + feedback infrastructure 组织`
- Visuals:
  - `上半页 6 周时间线；下半页五张 decision cards；右下角一张 closing card。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `最后我最希望明天讨论能落到这五个具体问题上。`
  - `只要这五件事里有三四件能拍板，后面 6 周其实就可以很明确地按“对象收束、实验拉厚、初稿成型”这条线推进。`
  - `如果您觉得其中某个判断有问题，我也希望优先把那个问题挑出来，而不是继续平均铺开。`
- Notes Supplement:
  - `最后一句停顿，进入讨论。`
- Implementation Notes:
  - `closing card 要明显，但不要像感谢页；它应该更像“请拍板”的决策页。`
- Acceptance Checks:
  - `观众离开时知道自己要回答什么。`
  - `必须同时有 timeline 和 decision cards，不能只剩总结话术。`
- Generator-Ready Instructions:
  - `上 40% 时间线；下 60% 五张决策卡 + closing card。`
