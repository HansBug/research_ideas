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
- 可见文本中不要出现反引号或其他 markdown 痕迹；仓库名、项目名、术语都按正常文本排版。
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
  - `决策 1：主投稿是否先锁定 project_1`
  - `决策 2：论文对象是否先限于离散控制状态层`
  - `决策 3：pyfcstm 与 pyudbm 的分工是否先讲清`
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
  - `结论 1：当前第一优先级是把 project_1 主稿收束成型`
  - `结论 2：project_1 目前真正缺的是问题收束，而不是样本`
  - `结论 3：论文对象应先落到离散控制状态层`
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
- Title: `官方 2026 日程显示：A/B 主窗口已过，近端出口主要是 ESEM 与期刊`
- Subtitle: `main-track full paper 基本结束；近端只剩 ESEM、NIER 与 rolling journal`
- Message: `到 2026-04-14 为止，A 类会议和多数贴题 B 类会议的 main-track research deadline 都已经过去；真正还开着的近端窗口主要是 ESEM technical / emerging 以及 MODELS NIER，而官方期刊主页则显示 TSE、SoSyM、Requirements Engineering、ASE Journal、EMSE 仍可投稿。因此 project_1 更应被当作下一轮主稿来打磨，而不是继续被 deadline 牵着扩题。`
- Visible Text:
  - `前因 / 因果条：CAiSE / FM / RE / ASE / MoDELS research 等 A/B 主窗口都早于 2026-04-14，而 project_1 的准备度又明显最高；因此当前策略应从“抢今年 main-track”改成“把主稿打厚，择机走 ESEM / rolling journal / short-format 后手”。`
  - `已过主窗口：CAiSE = 2025-11-21 / 2025-11-28；FM = 2025-11-25 / 2025-12-02；RE = 2026-02-16 / 2026-02-23；ASE = 2026-03-26；MoDELS research = 2026-03-20 / 2026-03-27`
  - `仍可操作窗口：ESEM technical = 2026-05-11 / 2026-05-18；ESEM emerging / vision = 2026-05-22 / 2026-05-29；MoDELS NIER = 2026-06-24 / 2026-07-01；ISSRE research = 2026-04-10 / 2026-04-17，但若摘要未交基本不算现实窗口`
  - `rolling journals：官方主页已确认 TSE、SoSyM、Requirements Engineering、ASE Journal、EMSE 仍有 submit / CFP 入口`
  - `四个 project readiness bars：project_1 最高；project_3 有后端地基但原型未成；project_4 最不适合先发`
  - `页面结论：若本学期一定要形成外部输出，现实路径应是 ESEM 或 rolling journal；但 project_1 仍应按“下一轮主稿”质量来打，而不是为了赶窗口扩题`
- Visuals:
  - `标题下先放因果条；上半页左侧是 official 2026 时间轴，横跨 2025-11 到 2026-07，既画出已过主窗口，也画出 ESEM / MoDELS NIER 等剩余窗口；右上角独立列出“仍可操作窗口”；下半页左侧保留四条 readiness bars；下半页右侧做 rolling journals 列表。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `如果只看博士全局，四个方向都重要；但从官方 2026 页面看，A 类会议和大多数贴题 B 类会议的 main-track deadline 已经过去，真正还开着的会议主窗口主要只剩 ESEM，而 MoDELS 也已经只剩 NIER 这类短格式。`
  - `所以这页真正要表达的不是“现在没有路了”，而是“现在的路已经从赶 main-track 变成两类后手：一个是 ESEM 这样的剩余会议窗口，另一个是官方主页明确还在收稿的 rolling journals”。`
  - `在这个前提下，project_1 更应该按下一轮主稿质量去打磨，而不是为了抢一个近端窗口把问题定义重新做散。`
- Notes Supplement:
  - `时间统一按官方页面的 AoE 口径；journal 的判断标准不是年度 CFP，而是官方主页明确仍有 submit / author-guidelines 入口。`
- Implementation Notes:
  - `时间轴不要太花；重点是 official 2026 deadline 与当前点的相对位置。月份标签必须放最上排且不能被 chip 盖住；MoDELS research / ASE 日期接近，ESEM technical / emerging 日期接近，必须上下错层布局。`
- Acceptance Checks:
  - `观众能直接看出“main-track 主窗口基本已过，但近端仍有 ESEM 与 rolling journal 这两类出口”。`
  - `时间窗口里必须出现 official 2026 具体日期，不能再用 prior-year proxy。`
  - `rolling journals 必须明确写出具体期刊名，不能只写抽象的 “journal” 一词。`
  - `月份标签必须完整可见，不得被 deadline chip 覆盖。`
- Generator-Ready Instructions:
  - `时间轴放上半页左侧；month strip 在最上排；milestone chip 按时间落点上下错层；current point 单独竖线；右上角做 remaining windows list；下半页左侧做四个水平 readiness bars；右侧做 rolling journals list。`

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
  - `前因 / 因果条：project_1 不是靠单一材料就能站住；因此比较对象、真实样本、状态机选型和可执行落地必须连成一条证据链。`
  - `baseline 比较集：别人现在怎么做，和谁比`
  - `真实样本库：控制系统设计文本长什么样，数据集从哪里来`
  - `状态机家族库：状态机到底有哪些，为什么要主动选型`
  - `pyfcstm 基础设施：目标形式主义 / executable IR / 闭环基座`
  - `汇总判断：三条文库线共同把论文对象压向 control-state problem`
- Visuals:
  - `标题下先放因果条；四张 role cards 围绕中央结论节点；每张卡片带数量与一句职责。`
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
- Title: `绿色 baseline 已经勾出了 5 条可直接讨论的方法线`
- Subtitle: `明天不该只报数量，而要把最值得讲的几篇“怎么做”讲清楚`
- Message: `baseline 文库已经不只是“有几篇可以比”，而是已经能清楚划出结构分解、反馈修复、迭代精化、知识注入工具链、RAG/微调这几条方法线。`
- Visible Text:
  - `总量：62 篇`
  - `状态分布：🟢 14 / 🟡 19 / 🟠 29`
  - `方法概述表：代表论文 / 方法骨架 / 对我们的启发`
  - `五条方法线：Structure/Event-Driven；Prompt + MC Feedback；Iterative FSM + IEC 61499；Knowledge Injection + Toolchain；Umple 的 One-shot / RAG`
  - `页面结论：baseline 已经不是“有没有”，而是“该把哪几类方法差异讲清楚”`
- Visuals:
  - `左侧保留一张紧凑状态分布图；右侧主体换成 5 行方法概述表，每行写清楚代表论文、方法骨架与对 project_1 的启发。`
  - `五行里必须显式点名 Umple baseline，说明 zero-shot 几乎不可用、One-shot 与 RAG 才能把文本 DSL 拉回可用区间。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页我不想再把 baseline 讲成“62 篇里有 14 篇绿色”这么空的话，而是要把最关键的绿色文献到底走了哪些方法路线讲清楚。`
  - `因为我们真正需要的不是更多题目，而是一个清楚的方法地图：别人是靠结构分解、反馈修复、代码生成闭环，还是靠知识注入和工具链集成把效果拉起来。`
- Notes Supplement:
  - `五条方法线最好按从“更直接的 NL -> state machine”到“更强基础设施闭环”来讲。`
  - `讲到 Umple 时，强调“小而稳的文本 DSL 仍需要示例 / schema 支撑”。`
- Implementation Notes:
  - `左侧数字区保持紧凑，右侧方法表必须是主体。每行都要写出论文名缩写与方法骨架，不要退化成抽象类别词。`
- Acceptance Checks:
  - `看完后不会误以为 baseline 文库只是数量堆积。`
  - `至少 4 篇绿色代表论文要能在这一页上被点名。`
  - `必须出现 62、14、19、29 四个数字。`
- Generator-Ready Instructions:
  - `左 30% 放数量与状态分布；右 70% 放 5 行方法概述表；底部放一句 take-home。`

### s08-baseline-evidence

- Target Duration: `1:15`
- Cumulative Time: `7:10`
- Title: `这些 baseline 方法线的共同指向，不是 prompt 花活，而是反馈基础设施`
- Subtitle: `最值得讲的绿色文献在证据上其实相当一致`
- Message: `纯 prompt 可以给出结构草稿，但真正把 guard、action、语义一致性和工程质量拉起来的，越来越是 model checking、仿真、代码生成与工具链反馈。`
- Visible Text:
  - `图 1：Structure/Event-Driven 2026 的 F1 对比：0.7029 / 0.5431 / 0.6559`
  - `图 2：SysML empirical study 的错误修复率：94.6 / 88.0 / 43.1 / 37.3`
  - `图 3：TTool AI 的评分与效率：63 vs 58；15.2x；81 vs 70；67.5x`
  - `证据卡：IEC 61499 不是一次生成，而是 iterative refinement + simulator + code generation`
  - `页面结论：workflow feedback > prompt tricks`
- Visuals:
  - `左中两张小型柱状图；右侧两张 evidence cards，总结 TTool AI 和 IEC 61499 这两种“工具链闭环”路线。`
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
- Title: `sources/ 不是自然分布样本，而是为 project_1 定向治理出来的样例池`
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
- Title: `sources/ 的大数字说明我们已经不缺样例池，只缺问题收束`
- Subtitle: `这些统计首先回答“样例池够不够厚”，而不是“世界真实分布怎样”`
- Message: `sources 现在最重要的作用，是证明 project_1 已经拥有足够厚、足够稳定、足够可治理的样例池来做数据集和评测。`
- Visible Text:
  - `前因 / 因果条：样本主链已经够厚；因此这一页要证明我们不再处在“先去找样本”的阶段。`
  - `四个 big numbers：787 papers / 715 paper-level green / 746 positive cases / 685 core cases`
  - `表 1：论文级总体统计，列为指标 / 定义 / 数量`
  - `表 2：案例级保留角色统计，列为类别 / 定义 / 数量`
  - `底部 take-home：样例池已经够厚，不再是“先去找样本”的阶段`
- Visuals:
  - `标题下先放因果条；上排四个 big-number cards；下排两张解释性表格。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `我这里故意把表格做成“指标加定义”的形式，因为如果只有标题和数字，导师很难判断这些统计到底在说明什么。`
  - `现在这组数字最重要的意义是：样例池已经够厚，真正该做的是围绕它定义论文对象和评测口径，而不是再把时间花在泛扩样上。`
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
- Title: `这些比例不能被读成自然分布，它们只能证明我们已经蓄了足够厚的目标样例池`
- Subtitle: `后期 sources 是按 EFSM / HSM + T0 / T1 主动强筛出来的`
- Message: `我们能从这些数字里稳妥宣称的，不是“控制系统天然大多如此”，而是“project_1 已经拥有足够多的 EFSM/HSM + T0/T1 样例来做数据集与评测”。`
- Visible Text:
  - `前因 / 因果条：如果把这些比例误读成自然分布，后面的结论就会站不住；因此这一页必须明确“能说什么、不能说什么”。`
  - `不能这样说：控制系统天然大多数都是 EFSM / HSM；这些比例不是总体文献分布`
  - `可以这样说：当前已经有 127 FSM / 429 EFSM / 157 HSM，另有 719 条 T0/T1 样例，足以支撑数据集与评测`
  - `底部结论：sources 的价值在于“样例池够厚”，不是“替整个领域做分布统计”`
- Visuals:
  - `标题下先放因果条；主体改成左右两大栏：左侧“不能这样解读”，右侧“可以这样解读”；下方再放一条 sample-pool conclusion ribbon。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页不是在替领域做统计，而是在替我们的论文边界做自我约束。`
  - `我要明确告诉导师：这些数字首先来自定向筛选，所以它们能证明“我们池子里有很多这类样本”，却不能证明“世界上控制系统天然主要就是这类”。`
- Notes Supplement:
  - `把“不能这样说 / 可以这样说”对照着讲，避免观众只记住右边数字。`
- Implementation Notes:
  - `不要再做“分布图 + 结论卡”的逻辑；这一页要明显长得像“口径澄清页”。`
- Acceptance Checks:
  - `观众必须明确听懂“这些统计不是自然分布”。`
  - `右栏必须同时出现 127 / 429 / 157 / 719 这几个数字。`
- Generator-Ready Instructions:
  - `左 45% 做“不能这样说”警示栏；右 55% 做“可以这样说”的样例池证据栏；底部一条结论带。`

### s12-sources-time-structure

- Target Duration: `1:00`
- Cumulative Time: `11:10`
- Title: `这个定向样例池依然不是“简单平面 FSM 池”，它保留了层次、定时和恢复复杂度`
- Subtitle: `收敛对象不等于退化对象`
- Message: `虽然我们主动把对象收束到 control-state layer，但池子内部仍保留了 hierarchy、局部 timer、显式时钟、恢复链等复杂度。`
- Visible Text:
  - `前因 / 因果条：如果把目标收束误读成“只做最简单 FSM”，后面 pyfcstm 的定位也会被说扁；因此这一页要强调池子里的结构复杂度。`
  - `四类主模式：阶段链 / 联锁许可 / 模式层次 / 异常恢复`
  - `结构证据：160 条层次样例；243 条显式时钟；T0 + T1 = 719 / 746`
  - `结论 1：收敛对象 = 离散 control-state，不 = 简单 FSM`
  - `结论 2：目标形式主义至少要能承载 EFSM + HSM + local timing`
- Visuals:
  - `标题下先放因果条；主体改成 2x2 四张模式卡，每张卡写“模式定义 + 代表样本 + 为什么对 project_1 重要”；底部再放两张结论卡。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页是为了防止导师自然地追问一句“那是不是做个普通 FSM 就行了”。`
  - `答案是否定的，因为我们现在这个池子虽然定向筛成了 control-state layer，但里面仍然大量保留了层次、timer、恢复链和联锁条件。`
- Notes Supplement:
  - `四张模式卡按“阶段链 -> 联锁 -> 层次 -> 恢复”顺序讲。`
- Implementation Notes:
  - `不要回退成双图统计页；主体必须是 control-state pattern 解释。`
- Acceptance Checks:
  - `必须同时看到“池子被收窄过”与“池子仍有复杂度”这两个事实。`
- Generator-Ready Instructions:
  - `上方因果条；中间 2x2 pattern cards；底部两张 take-home cards。`

### s13-sources-examples

- Target Duration: `1:05`
- Cumulative Time: `12:15`
- Title: `样例池已经覆盖多类控制语境，因此足够支撑 paper 的案例与评测`
- Subtitle: `这些例子证明的是 coverage，而不是 prevalence`
- Message: `当前样例池并不局限于单一行业，而是已经跨离散制造、楼宇机电、铁路联锁、任务控制等多类语境，足够支撑 project_1。`
- Visible Text:
  - `顶部一句 framing：这里不是在说“哪个行业最常见”，而是在说“我们已经有哪些可用语境”。`
  - `五个代表样本：洗衣机 PLC / 电梯 PLC / 铁路联锁 / UAV supervisor / 自动驾驶 HSM`
  - `表格列：控制语境 / 为什么被纳入池子 / 支持的 control-state 模式 / 对 paper 的作用`
  - `底部总结：这些例子证明我们已有足够的跨语境 coverage 来做实验与叙事`
- Visuals:
  - `顶部 framing sentence；主体仍是一张 5x4 的代表样本解释表；右下角一张 coverage conclusion card。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这页我想强调的是，我们并不是只在一个很窄的离散制造角落里找到样本，而是已经在多个控制语境里都有足够可用的例子。`
  - `所以这些例子不是为了说“世界分布是这样”，而是为了说明“我们现在写 paper 已经不缺可讲、可比、可测的案例”。`
- Notes Supplement:
  - `五个样本重点只讲三行，但要点出“coverage 而非 prevalence”。`
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
- Title: `state_machine_types/ 给出的启发不是“谁最多”，而是贡献点可以落在 profile / DSL / infrastructure`
- Subtitle: `现代状态机研究越来越像“选择并塑造目标对象”，而不是假定唯一标准`
- Message: `因为状态机本来就是家族，而现代研究重心大量落在 DSL、元模型、执行载体与 profile 上，所以 pyfcstm 作为目标形式主义设计是合理贡献。`
- Visible Text:
  - `前因 / 因果条：既然“状态机”本来就是家族，project_1 就不能把目标对象说成天然唯一；因此必须主动选型。`
  - `左侧：状态机家族主分支 = control-state / timed / hybrid / interaction-resource`
  - `右侧：现代贡献形态 = DSL 59 / 标准与元模型 264 / 2010+ 非模型层 82.6%`
  - `结论：project_1 的贡献不一定是再发明一种“全新状态机”，也可以是主动选定并塑造一类更适合任务的 profile`
- Visuals:
  - `标题下先放因果条；主体改成左右两张表。左表写“主分支 / 解决的复杂度 / 代表对象”，右表写“贡献形态 / 当前证据 / 对 project_1 的意义”。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这条文库线最重要的结论不是“哪个家族分支条目最多”，而是今天的状态机研究已经很大程度上转向 profile、DSL、元模型和执行载体。`
  - `这就给了 pyfcstm 一个很清楚的学术位置：它不是在假装覆盖整个状态机宇宙，而是在主动塑造一个更适合 project_1 的 control-state profile。`
- Notes Supplement:
  - `右侧一定要点出“贡献形态”而不是只点类别名。`
- Implementation Notes:
  - `这一页不要再靠一堆方框模拟族谱树；主体必须真的是表格。`
  - `右侧不要只是数字，要写出“为什么这允许 pyfcstm 成为贡献点”。`
- Acceptance Checks:
  - `观众能看出“状态机是家族”而不是一条直线。`
  - `观众还能看出“现代贡献可以落在 profile / DSL / infrastructure”。`
- Generator-Ready Instructions:
  - `左 family tree / band；右 contribution-form cards；底部一句 take-home。`

### s15-control-state-definition

- Target Duration: `1:15`
- Cumulative Time: `14:25`
- Title: `我们要解的是控制系统的离散 control-state layer，而不是所有状态机`
- Subtitle: `模式组织、联锁 guard、异常恢复、事件权限和局部 timer 才是当前主问题`
- Message: `第一篇 paper 最该解决的不是整个控制系统状态机宇宙，而是离散监督控制层这几个最稳定、最可执行、最可验证的语义块。`
- Visible Text:
  - `六类核心语义：模式层次 / 联锁 guard / 故障与恢复链 / 事件作用域 / 生命周期动作 / 局部工程定时`
  - `主体表：语义块 / 工程含义 / 为什么是第一篇 paper 的主问题 / pyfcstm 当前承载`
  - `底部结论条：pyfcstm 现在已经能承载这一层，而不需要先把 DSL 推到 hybrid / TA 那一侧`
- Visuals:
  - `主体改成一张 6 行表格，每行写“语义块 / 工程含义 / 为什么重要 / pyfcstm 当前承载”；底部一条深色 conclusion ribbon。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页要把“控制系统状态机”这个词收成一个更可操作的对象，而不是继续用大口袋式说法。`
  - `我更愿意把第一篇 paper 直接聚焦到模式组织、联锁、恢复、事件权限和局部 timer 这几类语义，因为这正是 pyfcstm 现在最能承载的那层。`
- Notes Supplement:
  - `这页多停留几秒，等导师看六张卡。`
- Implementation Notes:
  - `不要再用 3x2 卡片。`
  - `“pyfcstm 当前是否能承载”要明确写成可读短句，并对“局部工程定时”诚实写成部分承载。`
- Acceptance Checks:
  - `观众必须能明确看到“当前先做这六类 control-state 语义”这个结论。`
  - `不能再退回泛泛的“离散 vs 连续”抽象表。`
- Generator-Ready Instructions:
  - `中部一张 6 行解释表；底部 conclusion ribbon 横跨全页。`

### s16-pyfcstm-progress

- Target Duration: `0:55`
- Cumulative Time: `15:20`
- Title: `在 STM 语境下，pyfcstm 更像一个收窄后的 control-state DSL，而不是大而全状态机工具`
- Subtitle: `最该重点比较的是 Umple / UmpleRun 这条文本状态机生态，而不是泛泛说“它像状态图”`
- Message: `pyfcstm 不是普通 FSM，也不是完整 UML/SCXML/UPPAAL 替代；它更接近 sequential HSM 骨架 + EFSM 数据面 + 确定执行语义的 executable control-state profile。`
- Visible Text:
  - `一句话定位：executable control-state DSL`
  - `对照表：近邻对象 / 它在 STM 文库里做什么 / 与 pyfcstm 的相似点 / 关键差异`
  - `重点近邻：HSM / Statecharts；Umple；UmpleRun；SCXML；Sismic；UPPAAL`
  - `核心差异：sequential hierarchy；EFSM 数据面；abstract action 隔离；cycle/stable-boundary 语义`
  - `页面结论：它的研究辨识度来自“窄 profile + 闭 formal core”，而不是“大而全兼容”`
- Visuals:
  - `顶部先放一句话定位；主体做一张 6 行对照表：近邻对象 / 它在 STM 文库里做什么 / 相似点 / 关键差异；底部一条定位结论带。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `这一页站在状态机语境里讲 pyfcstm 到底是什么，以及它和几类相邻工作的边界差在哪里。`
  - `核心不是说它比别人更大，而是说它在 control-state 这条线上做了一个更窄、更闭、更适合自动生成和闭环反馈的 profile。`
- Notes Supplement:
  - `讲解顺序优先按 HSM -> Umple -> UmpleRun -> SCXML -> Sismic -> UPPAAL。`
  - `Umple 必须重点讲：它最像文本状态机 DSL 近邻，但更偏 UML 复合状态机文本承载与代码生成；UmpleRun 则更偏其动态验证路线。`
- Implementation Notes:
  - `这一页必须以真正的表格为主体，不要再用四张差异卡。`
  - `对照表要明显区分“相似点”和“不能等同的原因”。`
- Acceptance Checks:
  - `观众必须能明确听懂 pyfcstm 在 STM 谱系里属于什么。`
  - `至少 4 个相邻工作要被显式点名比较。`
- Generator-Ready Instructions:
  - `上半页做定位与对照表；下半页放四张核心差异卡和一句 take-home。`

### s17-pyfcstm-role

- Target Duration: `1:00`
- Cumulative Time: `16:20`
- Title: `pyfcstm 的研究价值，在于把目标形式主义、执行语义和闭环接口一起做出来`
- Subtitle: `它不是附属工具，而是 project_1 的核心研究产出之一`
- Message: `pyfcstm 的学术价值不在于“又做了一个状态机工具”，而在于它把目标 profile、可执行语义、形式化边界和 analysis-ready substrate 一起设计了出来。`
- Visible Text:
  - `左表：五个贡献点 = target profile / executable semantics / formal core boundary / executable model output / unified analysis-ready substrate`
  - `右表：当前落地能力 = parser / runtime / symbolic expr / codegen / tooling`
  - `结论：pyfcstm 是 project_1 对“应该生成什么、怎样立刻可用、如何继续进闭环”的研究性回答`
- Visuals:
  - `主体改成左右两张表。左表写“贡献点 / 真正回答的问题”，右表写“当前能力层 / 已有落地 / 为什么重要”；底部一条结论带。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `如果论文里只是把 pyfcstm 当成实现细节，我觉得会浪费掉它最重要的研究意义。`
  - `它真正回答的是三件事：应该生成什么对象、生成结果为什么能立刻执行、以及为什么它能继续接到验证和修复闭环。`
- Notes Supplement:
  - `能力带要被讲成“这不是空口贡献，而是已经有落地基座”。`
- Implementation Notes:
  - `不要再做贡献卡海。`
  - `两张表都要可读，右表里“已有落地”必须写成具体能力而不是抽象形容词。`
- Acceptance Checks:
  - `观众会把 pyfcstm 理解成研究答案，而不是周边工具。`
  - `“贡献点”与“已有落地能力”必须同时出现，避免又变回概念页。`
- Generator-Ready Instructions:
  - `上方一句话定位；中部左右两张表；底部 conclusion ribbon。`

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
- Subtitle: `收束问题对象、拉厚实验、准备 ESEM / rolling journal 后手`
- Message: `现在最需要的不是更多开放问题，而是把主线固定下来并倒排接下来 6 周。`
- Visible Text:
  - `前因 / 因果条：如果前面几项关键判断不能拍板，后面 6 周就会继续分散推进；因此这一页把倒排计划和待确认问题放在一起。`
  - `上方时间线：第 1-2 周收束问题定义与论文主张；第 3-4 周固化样本与 baseline 实验；第 5-6 周完成初稿并锁定 ESEM / rolling journal 后手`
  - `五个待拍板问题：`
  - `1. 主投稿是否锁定 project_1`
  - `2. 论文对象是否先限于离散控制状态层`
  - `3. pyfcstm 是否写成目标形式主义 / executable IR`
  - `4. pyudbm 是否继续沉淀 backend 地基`
  - `5. 主稿写法是否按 feedback infrastructure 组织，并把 ESEM / rolling journal 作为近端出口`
- Visuals:
  - `标题下先放因果条；上半页 6 周时间线；下半页五张 decision cards；右下角一张 closing card。`
- Formula Requirements:
  - `None`
- Symbol Explanations:
  - `None`
- Speaker Notes:
  - `最后我最希望明天讨论能落到这五个具体问题上。`
  - `只要这五件事里有三四件能拍板，后面 6 周其实就可以很明确地按“对象收束、实验拉厚、初稿成型、锁定 ESEM 或 rolling journal 后手”这条线推进。`
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
