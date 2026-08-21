# 边界门误排除审计（L2 · 语料侧）

> **历史调研说明**：本文审计的是旧来源语料门，数字是当时快照，不是当前谓词覆盖率
> 或来源普遍率。当前政策和变更门以 [`pipeline/evidence_discovery/`](../../pipeline/evidence_discovery/)
> 为准。

⭐ 审计对象：[tools/build_inscope_corpus.py](./tools/build_inscope_corpus.py) 从 [../../../sources/SUMMARY.md](../../../sources/SUMMARY.md) 的「案例清单」筛出界内案例的那道三条件合取门。⭐ 审计日期 2026-08-12。⛔ 本轮**未修改**该脚本，⛔ 也未修改 `sources/` 下任何文件；全部分析脚本写在 `/tmp/l2audit/`，仓库内只新增本文件。

## 0. 一句话结论

⭐ **边界门的实现层面零缺陷**——433 条排除全部由三个**封闭词表**字段的精确匹配产生，无同义写法漏配、无空值、无列错位、无静默丢弃，因此**因实现或字段匹配问题可回收的案例数是 0**；⚠️ 但门的第 2 条（`时间级别 = T0`）在**口径**上严于 [CLAUDE.md](../../../../CLAUDE.md) 的 $M = (S, E, V, Tr, A)$ 边界，它额外排除了 **139** 条**不带 `显式时钟` 结构标签**的 `T1` 案例（其中 110 条其余标签全部干净、96 条双 A、覆盖 109 个界内从未出现过的论文目录）——⛔ 这是一个**必须由用户按原则裁定的口径问题，不是审计员可以自行放宽的实现瑕疵**。

## 1. 审计方法与可复现命令

⭐ 本轮做了四件事，每件都可机械复算。第一，逐字读 [tools/build_inscope_corpus.py](./tools/build_inscope_corpus.py) 的 `collect_in_scope`，把三个条件的实现方式（精确 / 包含、大小写、去反引号、空值路径）写成下面 §2。第二，跑一遍该脚本取得界内 313 与总数 746，再用一份独立实现（不复用被审代码的函数）重新解析同一张表，把 433 条被排除案例按**排除原因组合**分类，并列出三个标签列的**全部取值**以检查同义写法与空值。第三，把 `sources/*/STM.md` 里的 `## 条目` 标题数逐目录与表行数对拍，确认「案例清单」相对 `STM.md` 无遗漏（否则会有案例根本进不了门）。第四，对最大的一个候选池逐条机械扫描其 `### 1. 原文摘录` 节的计时词元，并抽 11 条读原文摘录做人工核验。

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_stm_issue_discover
python related_work/provenance/tools/build_inscope_corpus.py --out-dir /tmp/l2/corpus   # 案例总数=746 界内=313 唯一论文=310 抽取失败=0
```

⛔ 上面这些数**不得写进任何交付物当作常量**（[../CONTINGENCY_L2.md](../CONTINGENCY_L2.md) §1.4 已写死这条），⭐ 本文件里出现的一切数字都是 2026-08-12 的快照，随扩库变。

## 2. 边界门的实际实现（逐条件，含空值处理）

### 2.1 先看它怎么找到数据行

⭐ `_ROW = ^\|\s*\d+\s*\|\s*\d+\s*\|` 要求行首是管道符、第一列与第二列**都必须是纯数字**（`#` 与 `论文#`）。⭐ 这一条同时充当「表定位」——它不定位章节，而是靠「前两列都是数字」这个形状把「案例清单」的数据行从全文 2213 行里挑出来。⭐ 实测这个形状是**充分且精确**的：`案例清单` 节（第 1315–2069 行）内 `_ROW` 命中 746 行，节内没有任何「以数字开头但第二列非数字」的漏配行，节**外**命中 0 行。⭐ 论文级总表之所以不会被误吞，是因为它的第二列是领域 emoji 而非数字。

⭐ 随后 `_cells` 按 `|` 切分并逐格 `strip()`，`if len(cells) < 14: continue`。⭐ 实测 746 行**全部恰好 14 格**，⛔ 没有任何一行因为单元格内含 `|`（链接、代码、表内竖线）而发生列错位——这是最容易出的一类静默 bug，本轮已排除。⭐ 列映射为 `cells[3]=领域`、`cells[4]=案例`、`cells[5]=控制对象`、`cells[6]=状态机类型`、`cells[7]=时间级别`、`cells[8]=结构标签`、`cells[12]=跳转`，与 [../../../sources/GUIDE.md](../../../sources/GUIDE.md) §4.4.2 规定的 12 列顺序一致。

### 2.2 条件一：`状态机类型 ∈ {FSM, EFSM, HSM}`

⭐ 实现是 `_strip_code(cells[6]) not in frozenset({"FSM","EFSM","HSM"})` → 排除。⭐ `_strip_code` 只去反引号并 `strip()`，⛔ **不做大小写归一、不做同义映射、不做包含匹配**——是严格的精确集合成员判断。

⭐ 这看似脆弱，但在本语料上是安全的，因为 [../../../sources/GUIDE.md](../../../sources/GUIDE.md) §6.2 把该列钉成**互斥封闭词表** `FSM / EFSM / HSM / Protocol / Resource-flow / Hybrid / N/A`，而实测 746 行的取值恰好只有六个：`EFSM 429` / `HSM 157` / `FSM 127` / `Hybrid 16` / `Resource-flow 13` / `Protocol 4`（`N/A` 0 条，与 [../../../sources/SUMMARY.md](../../../sources/SUMMARY.md)「各领域状态机类型分布」合计行逐字一致）。⛔ **没有任何 `Statechart` / `状态图` / `Mealy` / `Moore` / `层次状态机` / 拼写变体 / 大小写变体出现在该列。**

⭐ 我另外从**反方向**查了同义写法漏配：扫「案例」与「控制对象」两列的自由文本，凡出现 `Mealy` / `Moore` / `Statechart` / `Petri` / `Grafcet` / `SFC` / `automat` 字样的行，看它们的类型列被判成了什么。结果全部落在白名单内或按语义正确归类——`Mealy` 9 条（FSM 7 / EFSM 2）、`Moore` 7 条（全 FSM）、`Statechart` 2 条（全 HSM）、`Grafcet` 1 条（EFSM）、`Petri` 与 `SFC` 各 0 条。⭐ 即：**标注者已经把别称归一到了主类型上，门不需要认识别称。**

### 2.3 条件二：`时间级别 = T0`

⭐ 实现是 `_strip_code(cells[7]) != "T0"` → 排除，同样是精确相等。⭐ 实测取值只有 `T1 367` / `T0 352` / `T2 15` / `T3 12`（`N/A` 0 条，与 SUMMARY 的「各领域时间级别分布」合计行一致），⛔ 无 `T0 / T2` 这类多值格（该写法只出现在论文级总表，而论文级总表根本不被 `_ROW` 命中）。

### 2.4 条件三：`结构标签` 不含「并行」

⭐ 实现是 `"并行" in cells[8]` → 排除。⭐ 这一条是**包含匹配**而非精确匹配，且**没有去反引号**（不需要：`并行` 在反引号内部，子串匹配照样成立）。⭐ 该列是多值列，形如 `` `层次, 并行, 显式时钟` ``，所以包含匹配是正确选择。⭐ 假阳性风险为零：封闭词表的六个标签 `层次 / 并行 / 协议交互 / 资源互斥 / 显式时钟 / 连续耦合` 中，⛔ 没有任何一个把「并行」当子串包含。⭐ 实测词元全集与出现次数为 `显式时钟 243` / `层次 160` / `连续耦合 71` / `并行 36` / `协议交互 32` / `资源互斥 26`，与 SUMMARY 的「结构标签覆盖率（多标签口径）」表逐格一致。

### 2.5 第四道隐式门：目录抽取

⭐ 三条件之后还有一步 `_link_dir(cells[12])`，正则 `\(\./([^)]*)/STM\.md\)`；⛔ **拿不到目录就静默 `continue`**——这是一条没有写在判据里的第四道门，若跳转列格式漂移就会**无声**丢样本。⭐ 本轮专门查了它：746 行全部能抽到目录，`跳转` 列没有任何一行出现两个 `STM.md` 链接（否则取第一个可能取错），也没有任何一行的 `STM` 与 `DESC` 指向不同目录，抽到的目录全部真实存在且含 `STM.md`。⭐ 因此这道隐式门当前**没有吞掉任何案例**，但它是脆弱点，值得在 GUIDE 里留一条格式约束。

### 2.6 空值怎么处理：**没有空值**

⭐ 这是本审计最干脆的一条结论。⭐ 三个判据列 `状态机类型 / 时间级别 / 结构标签`，以及 `领域 / 案例 / 控制对象 / 数据集角色 / 原文细节 / 描述细节 / 跳转`，**746 行全部非空**，⛔ 一个空格都没有。⭐ 因此「空值被当成什么处理」这个问题在当前语料上不会被触发；⚠️ 但如果将来出现空值，行为是：空的类型或时间级别一律不等于白名单值 → **被排除**；空的结构标签 → 不含「并行」→ **不阻塞**。⭐ 也就是说门对空值是「类型/时间从严、结构从宽」，这个默认方向是安全的（不会把界外放进来），⛔ 但空的类型/时间会被静默当成界外，未来应改为报错而非静默排除。

### 2.7 案例清单相对 `STM.md` 有没有漏登记

⭐ 门只读 `SUMMARY.md`，所以若某篇 `STM.md` 里有条目**没被登记进案例清单**，它就永远不会被门看到——这是比误排除更隐蔽的一类漏失。⭐ 本轮逐目录对拍：787 个目录 / 787 份 `STM.md`，其中 `## 条目` 标题共 **746** 个，与案例清单的 **746** 行**逐目录数量完全相等**，⛔ 无「表里有行而文件无标题」，⛔ 也无「文件有标题而表里无行」。⭐ 即案例登记是完整的，门的输入没有上游漏失。

## 3. 排除原因分类统计

⭐ 433 条被排除案例按**排除原因组合**的完整分解（原因可并发，故先给互斥组合、再给单因子计数）：

| 排除原因组合 | 条数 | 占 433 | 唯一论文目录 |
| :-- | --: | --: | --: |
| 仅 `时间级别 ≠ T0` | 365 | 84.3% | 355 |
| 仅带「并行」标签 | 24 | 5.5% | 24 |
| `类型` + `时间` 同时越界 | 17 | 3.9% | — |
| 仅 `类型` 不在白名单 | 15 | 3.5% | 13 |
| `时间` + `并行` 同时越界 | 11 | 2.5% | — |
| 三条全越界 | 1 | 0.2% | — |
| **合计** | **433** | **100%** | — |

| 单因子（可重复计） | 命中条数 | 该因子的字段取值分解 |
| :-- | --: | :-- |
| `状态机类型` 不在白名单 | 33 | `Hybrid 16` / `Resource-flow 13` / `Protocol 4` |
| `时间级别 ≠ T0` | 394 | `T1 367` / `T2 15` / `T3 12` |
| 结构标签含「并行」 | 36 | `层次, 并行 18` / `并行 7` / `层次, 并行, 显式时钟 3` / `层次, 并行, 协议交互 3` / `显式时钟, 层次, 并行 2` / 其余单条 3 种 |

⭐ 三个单因子数与 [../../../sources/SUMMARY.md](../../../sources/SUMMARY.md) 的三张分布表（状态机类型 / 时间级别 / 结构标签覆盖率）逐格吻合，⭐ 说明门读到的就是总账写的，⛔ 没有解析偏差。

⭐ **一条对后文关键的交叉事实**：`时间级别` 与 `显式时钟` 结构标签是两个**独立**字段，实测交叉为 `T0 ∧ 显式时钟 = 0`、`T1 ∧ 显式时钟 = 228`、`T1 ∧ ¬显式时钟 = 139`、`T2` 全部 15 条带 `显式时钟`、`T3` 全部 12 条带 `连续耦合`。⭐ 也就是说条件二（`T0`）**已经蕴含**「不带显式时钟」，⚠️ 而它额外还排除了 139 条**语料自己判定为不需要把时钟当显式状态维**的案例。

## 4. 每类的例子与判断

### 4.1 `Hybrid`（16 条，其中 0 条仅因类型排除）→ ⭐ **该排除**

| 目录 | 案例 | 类型 / 时间 / 结构 |
| :-- | :-- | :-- |
| `hytech-hybrid-systems` | Thermostat hybrid automaton | `Hybrid` / `T3` / `连续耦合` |
| `automotive-analysis-thesis` | Brake-by-Wire ABS timed automaton (pABS FL) | `Hybrid` / `T2` / `连续耦合, 显式时钟` |
| `design-and-assessment-of-an-anti-lock-braking-system-controller` | ABS pressure release and re-application logic | `Hybrid` / `T3` / `连续耦合` |

⭐ 判断：16 条 `Hybrid` **全部**同时带 `连续耦合` 标签且全部是 `T2/T3`，即三条判据互相印证。⭐ 连续动力学与连续时间演化明确落在 $M = (S, E, V, Tr, A)$ 之外，⛔ 无争议。⭐ 反向检查也干净：带 `连续耦合` 标签但类型判为 `EFSM/FSM/HSM` 的有 55 条，其中 35 条在界内——这与分类学「若连续控制器完全可视为黑盒，则更适合判 `EFSM/HSM` 并加 `连续耦合` 标签」的规定一致，⭐ 说明 `Hybrid` 这一类**没有被滥用**去多排除高层监督流程。

### 4.2 `Resource-flow` / `Protocol`（15 条仅因类型排除）→ ⚠️ **需人工裁定**

| 目录 | 案例 | 类型 / 时间 / 结构 |
| :-- | :-- | :-- |
| `using-z-specification-for-railway-interlocking-safety` | Component-state view of an interlocking system | `Resource-flow` / `T0` / `资源互斥` |
| `french-railway-interlocking-hcpn` | Route establishment in French railway interlocking | `Resource-flow` / `T0` / `资源互斥` |
| `formal-verification-of-autonomous-vehicle-platooning` | Joining procedure for a follower vehicle | `Protocol` / `T0` / `协议交互` |

⭐ 判断：这 15 条（`Resource-flow` 12 + `Protocol` 3，13 个论文目录）**全部是 `T0` 且不带 `显式时钟` 与 `连续耦合`**，⛔ 即它们被排除的唯一理由是「哪一类形式主义最能代表它」这个**主类型**判断，⛔ 而不是「它需不需要时钟或正交区」。

⚠️ 要看清这里的分层：`状态机类型` 是**互斥、按优先级判定**的「默认推荐用哪类模型」标签（判定优先级见讨论纪要 [../../../discussions/2026-04-02-14-17-AI-讨论-sources文库STM数据集可用性与趋同问题系统分析.md](../../../discussions/2026-04-02-14-17-AI-讨论-sources文库STM数据集可用性与趋同问题系统分析.md) §3.2.5：`Hybrid > Resource-flow > Protocol > HSM > EFSM > FSM`），⭐ 而 `资源互斥` / `协议交互` 是**可叠加**的结构标签。⭐ 关键不对称在于：门排除主类型 `Resource-flow` / `Protocol`，⭐ **却接纳带 `资源互斥` 标签的 5 条与带 `协议交互` 标签的 8 条界内案例**。⭐ 即同一种语义信号，出现在结构标签列就在界内，升格成主类型就在界外。⚠️ 而分类学自己写着「如果只是单条顺序控制链，哪怕论文用了 `Petri Net`，也不必自动判成这一类；那种情况常常仍可落在 `EFSM/FSM`」——⭐ 这说明主类型是一个**程度判断**，⛔ 不是一个可表达性判断。

### 4.3 「并行」标签（24 条仅因此排除）→ ⭐ **该排除（读原文后确认）**

| 目录 | 案例 | 类型 / 时间 / 结构 |
| :-- | :-- | :-- |
| `a-parallel-hierarchical-finite-state-machine-approach-to-uav-control-for-search-and-rescue-tasks` | Search-and-rescue mission flow with parallel safe-flight layer | `HSM` / `T0` / `层次, 并行` |
| `multi-uav-landing-bigraph-digital-twin` | Orthogonally coupled AeroCtrl flight-service state machine | `HSM` / `T0` / `层次, 并行` |
| `real-time-system-for-scheduling-and-managing-uav-delivery-in-urban-areas` | UAV-AGV Delivery Cycle Coordination | `FSM` / `T0` / `并行, 协议交互` |

⭐ 这一类是任务里点名要分辨的：「并行」标签描述的是**系统有并发**还是**模型用了正交区**？⭐ 标签定义本身两者兼收（「存在同时活动的并行子层、正交区、并行子状态或并发执行支路」），⛔ 所以不能只看标签。⭐ 我读了 4 条的 `### 1. 原文摘录` 逐字核验，结论是**这 24 条的并发是真的、且是模型层的**：`real-time-system-for-scheduling-and-managing-uav-delivery-in-urban-areas` 逐字写「All AGVs are managed through a combination of **multithreading** and finite state machines (FSMs). Each AGV is controlled by an **independent FSM thread**」，且案例登记的是 UAV 六态机与 AGV 四态机的**联合**推进周期；`discrete-event-power-management-ac-microgrids` 逐字写「model the n plant components (DERs) as **automata Gi**」并合成「decentralized supervisors ZR_i」，是典型的自动机并行合成；`two-lift-five-floor-plc-rs232-link` 是两台电梯 `duplex-collective` 主从协同，`efficiency-through-automation-single-system-for-multiple-railway-guard-posts` 是一套 PLC 同时驱动五个道口（`R1`–`R5` 伺服 / `R6`–`R10` 蜂鸣器）。⭐ 这四条要保真都需要正交区或乘积构造，⭐ 排除是正确的。⚠️ 唯一要记下的旁注：这些案例的摘录里往往**同时**包含一个完全落在 $M$ 内的单机描述（如 UAV 的六态机本身），⛔ 但案例的登记范围是协同周期，所以按案例粒度排除仍然正确。

### 4.4 `T2 / T3`（27 条）→ ⭐ **该排除**

⭐ 15 条 `T2` **全部**带 `显式时钟`，12 条 `T3` **全部**带 `连续耦合`，⛔ 没有一条 `T2/T3` 是「既无显式时钟也无连续耦合」的。⭐ 强实时时间窗口与连续时间演化落在 $M$ 之外，⛔ 无争议。

### 4.5 `T1`（367 条，其中 365 条仅因时间排除）→ ⚠️ **需人工裁定，且这是全部争议的所在**

| 目录 | 案例 | 类型 / 时间 / 结构 | 原文/描述 |
| :-- | :-- | :-- | :-- |
| `automated-verification-of-signalling-principles-in-railway-interlocking` | Periodic execution logic of a railway interlocking program | `EFSM` / `T1` / `-` | `🟠 C` / `🟠 C` |
| `unified-control-powered-knee-ankle-prosthesis-daily-ambulation` | Two-state unified supervisor for the Utah powered knee-ankle prosthesis | `EFSM` / `T1` / `-` | `🟢 A` / `🟢 A` |
| `muscle-driven-exoskeleton-stepping-paraplegia` | Hierarchical HNP supervisor with stepping submachine and timeout recovery | `HSM` / `T1` / `层次` | `🟢 A` / `🟢 A` |

⭐ 判断分两步。⭐ 第一步是**门的自述理由与事实不符**：[../CONTINGENCY_L2.md](../CONTINGENCY_L2.md) §1.4 逐字写着「`时间级别 = T0`——⛔ `T1` 及以上**带显式时钟**，⛔ 属界外」。⚠️ 但语料另有一个专门表达「时钟应被当成显式状态维或显式 guard/reset 对象」的字段，就是 `显式时钟` 结构标签，⭐ 而 **139 条 `T1` 案例并不带它**（占 `T1` 的 37.9%）。⭐ `T1` 的分类学定义也逐字写着这些时间语义「通常可用**少量 timer 变量**处理，**不必直接上强实时形式主义**」——⭐ 而 timer 变量正是 $M$ 里的 $V$。⛔ 所以门的第 2 条不是「排除带显式时钟的」，而是「排除一切有工程定时的」，⭐ 它比自己声称的判据严一档。

⭐ 第二步是**这一档严格是否仍然正当**。⭐ 正面理由（支持维持现状）：$M$ 没有时间推进机制，`door opens for three seconds` 要么引入时钟、要么把时长抽象成一个事件，⭐ 后者对摘录里的时间事实是**有损**的；⛔ 而学术门在拿不准时应当**保守**。⭐ 反面理由（支持裁定放宽）：门是**案例级**过滤器，而 L2 的用法是**句子级**引用（只取 `### 1. 原文摘录` 的逐字片段去证明某条建模义务在领域内普遍）；⭐ 一条案例在别处有 3 秒门开保持，⛔ 并不影响它的摘录里「每个事件必须被声明」这类义务陈述的可引用性。⛔ 两条理由都成立，⛔ 所以这是裁定问题，⛔ 不是审计员能自己定的。

## 5. 疑似误排除的逐条核验

⭐ 我按任务要求抽读了 11 条被排除案例的 `### 1. 原文摘录`（4 条并行、2 条类型、5 条 `T1`），⭐ 逐条判断如下。

| 目录 · 案例 | 摘录里到底写了什么 | 判断 |
| :-- | :-- | :-- |
| `real-time-system-...-uav-delivery` · UAV-AGV Delivery Cycle Coordination | 「**multithreading** and FSMs … each AGV controlled by an **independent FSM thread**」，登记范围是 UAV 六态机与 AGV 四态机的联合周期 | ⭐ 该排除 |
| `discrete-event-power-management-ac-microgrids` · Decentralized AC-microgrid service supervisor | 「model the n plant components as **automata Gi**」+「reduced **decentralized supervisors** ZR_i」 | ⭐ 该排除 |
| `two-lift-five-floor-plc-rs232-link` · Duplex-Collective Five-Floor Elevator Dispatcher | 两台电梯 `duplex-collective` 主从、经 `RS232` 交换位置/方向/任务数 | ⭐ 该排除 |
| `efficiency-through-automation-...-railway-guard-posts` · Five-post railway crossing supervisor | 一套 PLC/HMI 同时驱动五个道口（`R1`–`R5` 伺服 / `R6`–`R10` 蜂鸣器） | ⭐ 该排除 |
| `using-z-specification-for-railway-interlocking-safety` · Component-state view | 枚举型状态域 `points_position ::= cp\|cm` 等 5 个 + 一组 invariant 条件；⛔ 摘录内**没有**时钟、**没有**并发区 | ⚠️ 需人工裁定（形式上是一台带枚举变量的 EFSM，⛔ 但摘录里没有迁移与事件，是状态空间 + 不变式的 Z 规约） |
| `formal-verification-of-autonomous-vehicle-platooning` · Joining procedure for a follower vehicle | 「a non-member vehicle **sends a joining request** to the platoon leader … the leader **sends back an agreement**」 | ⚠️ 需人工裁定（多角色消息序列需组合；⭐ 但单个 follower 的过程本身是一台顺序机） |
| `automated-verification-of-signalling-principles-in-railway-interlocking` · Periodic execution logic | 摘录逐字只有 PLC 扫描循环 `while(true){output(); input(); x1:=...}` + 不可达组合与 invariant；⛔ **无 timer、无延时、无 timeout、无任何时长数值** | ⛔ **疑似误排除**（`T1` 标签在摘录内找不到任何支撑；⭐ 扫描周期是执行模型，⛔ 不是时间约束） |
| `unified-control-powered-knee-ankle-prosthesis-daily-ambulation` · Two-state unified supervisor | 离散侧是两态机 `Contact` / `No Contact`，迁移判据是地面反力阈值（`>120 N` 进 / `<80 N` 出，即 HS / TO）；⭐ 唯一时长 `tswing 0.45–0.55 s` 是**连续内环最小抖动轨迹的参数**，⛔ 不是任何离散迁移的守卫 | ⛔ **疑似误排除**（离散监督机完整落在 $M$ 内；⭐ 时间语义在被抽象掉的连续控制器里） |
| `design-amp-control-of-an-elevator-control-system-using-plc` · PLC-based elevator car and door control | IR 遮挡阻止关门、限位保位、超载停机、氧气传感器触发就近层开门；⭐ 全篇唯一时间表述是「weight is at or less than set minimum value **for sufficient time**」，⛔ 无数值 | ⚠️ 需人工裁定（`T1` 标签技术上站得住，⛔ 但摘录内无任何需要时钟的内容） |
| `muscle-driven-exoskeleton-stepping-paraplegia` · Hierarchical HNP supervisor | 逐字有「**Timeout** phases were incorporated into the FSM for safety … if the hip or knee angle thresholds during swing were **not achieved within a prescribed time**」 | ⭐ 该排除（保守口径下；⚠️ 若允许把 timeout 抽象成 $E$ 里的一个事件则可回收） |
| `fault-tolerant-control-dual-stator-pmsm-uav` · Mission-phase and fault-driven FEPS mode switching | 逐字有「**250 ms delay** is assumed to achieve the full electric supply」；⚠️ 另外它的模式是两定子模式的乘积（`HSB/FMM`、`FTM/CSB`），⛔ 却**没有**被打 `并行` 标签 | ⭐ 该排除（`T1` 正确；⚠️ 顺带暴露 `并行` 标签在此漏打） |

⭐ 为了不让上表停在「抽样轶事」，我把第 4.5 节那个池子**机械量化**了一遍：对 110 条「`T1` + 无 `显式时钟` + 类型界内 + 不带并行/连续耦合/协议交互/资源互斥」的案例，逐条正则扫描其 `### 1. 原文摘录` 节里的计时词元（`\d+\s*(ms|s|sec|second|min|hour|Hz)`、`timeout` / `timer` / `delay` / `duration` / `deadline` / `refractory` / `within \d` / `定时` / `延时` / `超时` / `periodic` / `sampling period` 等）。⭐ 结果是 **78 条摘录里有计时词元，32 条一个都没有**（其中 26 条是双 A）。⛔ 也就是说这 32 条被排除的理由，**不出现在它们将被引用的那段文本里**。

⚠️ **但必须同时报告对称的一面，否则这份审计就是单边的**：我用同一个正则扫了**界内 313 条**，其中 **37 条**的摘录里有计时词元——例如 `plc-based-railway-level-crossing-gate-control` 的摘录逐字含 `30 sec` / `1 min` / `3 min` / `6 min`，`reusable-and-reliable-flight-control-software-for-a-...` 含 `120 s` / `60 s` / `45 min` / `periodic`，`planning-for-safe-abortable-overtaking-maneuvers-...` 含 `9.9s` / `12.8s` / `23.7s`，⭐ 而这三条的 `时间级别` 都判了 `T0`。⛔ **结论因此是双向的**：`时间级别` 是一个基于全文的**整体性**判断（时间是否构成控制语义核心），⛔ 它既不保证界外案例的摘录里有时间语义，⛔ 也不保证界内案例的摘录里没有。⭐ 门忠实地传播了标签，⛔ 残余误差在标签层，⛔ 且往两个方向都有。

## 6. 可回收的案例数估计

⭐ 必须分三层报，⛔ 混在一起报就会变成「放宽判据凑数字」。

| 层 | 可回收案例数 | 唯一论文目录 | 性质 |
| :-- | --: | --: | :-- |
| ⭐ **实现层 / 字段匹配层** | **0** | 0 | ⭐ 无同义写法漏配、无空值、无列错位、无静默丢弃、无上游漏登记。⛔ **这条路已封死。** |
| ⛔ **标签填写层（真·疑似误排除）** | ⛔ **不给数**，⭐ 已确证存在 ≥ 2 条 | — | ⭐ 抽读 5 条 `T1` 中有 2 条的 `T1` 标签在摘录内找不到支撑（扫描周期 / 连续内环时长）。⚠️ 但同一现象在界内也存在（37 条界内摘录含计时词元却判 `T0`），⛔ 所以纠正标签会**双向移动**案例，⛔ 净增量不可预估，⛔ 不构成一个「回收池」 |
| ⚠️ **口径裁定层** | ⚠️ 上限 **134**，⭐ 洁净子集 **110**，⭐ 洁净且双 A **96** | 133 / 109 / 96 | ⭐ 全部是「`T1` + 无 `显式时钟` + 类型界内 + 无并行」；⛔ 需用户按 $M$ 边界原则裁定，⛔ 审计员无权放宽 |
| ⚠️ **口径裁定层（次要）** | ⚠️ **15**（`Resource-flow` 12 + `Protocol` 3） | 13 | ⭐ 全部 `T0` 且不带显式时钟/连续耦合；⭐ 争点是主类型是「推荐形式主义」还是「可表达性」 |

⭐ 三个池的论文目录与现有界内 310 个目录的**重叠为 0**，⭐ 即任何回收都是净新增来源，⛔ 不是重复计数。⭐ 洁净子集的领域分布为 `🩺 36` / `🚦 15` / `🏢 13` / `🏭 10` / `⚙️ 10` / `🚗 9` / `✈️ 7` / `🌡️ 5` / `🚆 4` / `🅿️ 1`。

⛔⛔ **一条必须写在这里的纪律**：本审计的动因是「14 条谓词的界内真实系统数 ≤ 5」（[SUMMARY.md](./SUMMARY.md) §2），⛔ 而 `界内真实系统` 那一列的分母正是这 313 条案例。⛔ **因此「因为 14 条谓词证据薄，所以放宽边界门」是根 [CLAUDE.md](../../../../CLAUDE.md) §3.5 第 4 条点名的「评测口径迁就结果」。** ⭐ 裁定必须**先于**查看它对那 14 条有何帮助，⭐ 且理由只能是「$M$ 的边界本来就在哪」，⛔ 不能是「回收后数字够不够」。⭐ 若最终裁定放宽，还应配一条**句子级**保险：被引用的那条逐字片段自身不得含计时 / 并发 / 连续量内容——⭐ 这样放宽的是候选池，⛔ 收紧的仍是每一次引用，⛔ 而后者才是论文里真正承重的东西。⭐ 相关口径见 [../../discover_matrix/docs/protocol/method_provenance_policy.md](../../discover_matrix/docs/protocol/method_provenance_policy.md)。

## 6.5 ⛔⛔ 主 session 的裁定（2026-08-12）：**本 PR 内不放宽**

⭐ 按 §6 写死的纪律，⭐ 裁定必须**先于**查看它对那 14 条谓词有何帮助，⭐ 且理由只能是「$M$ 的边界本来就在哪」与工程正当性。⭐ 下列三条**均独立于回收后的数字**。

### ⛔ 裁定内容

⭐ **边界门维持原样**（`状态机类型 ∈ {FSM, EFSM, HSM}` ∧ `时间级别 = T0` ∧ 无「并行」标签），⛔ 本 PR 内**不改**、⛔ 不回收那 134 / 110 / 96 中的任何一条，⛔ 也不回收 `Resource-flow` / `Protocol` 那 15 条。

### ⭐ 三条理由

1. ⭐⭐ **同分母要求是硬约束。** ⭐ 313 是全部 L2 语料侧证据的冻结分母 —— ⭐ 两轮穷尽扫描的 315 条发现、⭐ 对抗裁定后的 143 条、⭐ 以及 19 行分级表的「界内真实系统」列**全部**建立在它之上。⭐ [method_provenance_policy.md](../../discover_matrix/docs/protocol/method_provenance_policy.md) §一.1 逐字要求「⭐ 跨代次的数字比较**仍然必须同分母**（同格集、同判据）」。⛔ 中途换分母而不重跑全部语料扫描，会让新旧数字不可比；⭐ 而重跑的代价是整轮 24 路扫描 + 裁定。⛔ **这条与证据薄厚无关。**
2. ⭐⭐ **标签层误差已确证是双向的，⛔ 单向回收会引入已知噪声。** ⭐ 审计实测：⭐ 110 条洁净候选里 32 条摘录零计时词元；⛔ **但界内 313 条里有 37 条摘录含计时词元却判了 `T0`**（⭐ 逐字例：`plc-based-railway-level-crossing-gate-control` 含 `30 sec` / `3 min` / `6 min`）。⛔ 只往「放进来」一个方向纠，⛔ 等于选择性采纳标签误差。⭐ 正确顺序是先修标签、再谈门 —— ⛔ 而修标签属 `sources/` 的维护范围，⛔ 不在 L2 的 ownership 内。
3. ⚠️ **动机污染：⛔ 时序本身不可读。** ⭐ 即便前两条不成立，⛔ 在「刚得知 14 条谓词证据薄」之后立刻放宽准入门，⭐ 这个**先后次序**在审稿人眼里无法与「迁就结果」区分 —— ⛔ 而根 [CLAUDE.md](../../../../CLAUDE.md) §3.5.-1 的教训正是「⭐ 最可靠的判据是查引入动机」。⭐ 该改动若要做，⭐ 应在一个**与证据厚薄无关的语境**里单独裁定。

### ⭐⭐ 但这条发现必须写进 Limitations，⛔ 不得埋掉

⛔ 审计的实质发现是：**边界门比它的自述理由更严**。⭐ [CONTINGENCY_L2.md](../CONTINGENCY_L2.md) §1.4 写「`T1` 及以上**带显式时钟**，属界外」，⛔ 而语料另有独立的 `显式时钟` 标签，⭐ 实测 `T0 ∧ 显式时钟 = 0` —— ⭐ 即**条件二已经蕴含「无显式时钟」**，⛔ 额外还排除了 139 条不带显式时钟的 `T1`（⭐ 占 T1 的 37.9%）；⚠️ 而 `T1` 自己的定义逐字写着这些时间语义「通常可用**少量 timer 变量**处理」—— ⭐ timer 变量正是 $M$ 的 $V$。

⭐ **可落稿的表述**：

> ⭐ 界内语料由一道**保守**的准入门筛出：⭐ 它以「时间级别 = T0」作为「无显式时钟」的代理，⛔ 而该代理严于目标 —— ⭐ 按 $M = (S, E, V, Tr, A)$ 的定义，⭐ 另有至多 **134** 个案例（⭐ 洁净子集 **110**）可能在界内却被排除。⭐ 我们选择保守：⭐ 这使语料侧证据**可靠**（⛔ 不含边界可疑项），⭐ 代价是**不完整**。

⭐⭐ **这个取舍对证据而言是正确的方向** —— ⭐ 证据宁可少而硬。⛔ 但必须明写，⛔ 否则「界内 313」会被读成「领域里就这么多」。

### ⛔ 何时应当重议（⭐ 写死触发条件，⛔ 以免变成永久搁置）

⭐ 出现下列任一情形，⭐ 本裁定应重议：① ⭐ `sources/` 的 `时间级别` 与 `显式时钟` 标签完成一次**双向**校订；② ⭐ 需要重跑全量语料扫描（⭐ 那时换分母的边际成本降为 0）；③ ⭐ 论文需要对语料覆盖度作定量主张。⛔ 若届时放宽，⭐ **必须**配上 §6 指定的**句子级保险**：被引用的那条逐字片段自身不得含计时 / 并发 / 连续量内容。

### ⚠️ 顺带登记一条上游数据问题（⛔ 不属 L2 ownership）

⭐ 审计发现 `fault-tolerant-control-dual-stator-pmsm-uav` 的模式是两定子模式的**乘积**（`HSB/FMM`、`FTM/CSB`），⛔ 却**漏打**了「并行」标签 —— ⭐ 即它当前**在界内**但按判据应当界外。⛔ 这是 `sources/` 的标注问题，⭐ 已登记；⛔ 本 PR 不改（⭐ 同理由 1：改它同样动分母）。

## 7. 审计自身的局限

⭐ 第一，**只审了门，没有重判标签**。⭐ 本轮把 `状态机类型 / 时间级别 / 结构标签` 当作既定事实核对门的行为，⛔ 没有对 746 条案例逐条回 `paper_content.txt` 重判。⭐ §5 里那两条「疑似误排除」是标签层问题，⛔ 而标签层的全面复核是另一件工作量级完全不同的事。

⭐ 第二，**计时词元扫描是词法代理，不是语义判定**。⭐ 正则会把 `1kHz` 采样率、`duration` 一般名词、`periodic` 执行都算作命中，⛔ 也会漏掉「hold the door until the passenger clears」这类不含数值与关键词的时间表述。⭐ 所以「32 条零词元」与「界内 37 条含词元」都只应读作**分布信号**，⛔ 不应读作逐条裁定。

⭐ 第三，**人工核验只覆盖 11 条**（占 433 条的 2.5%），⭐ 且抽样是**有意向可疑处倾斜**的（4 条并行里挑的是最像「多设备并发而非正交区」的，5 条 `T1` 里挑的是结构标签为 `-` 的洁净样本）。⛔ 因此 §5 的比例**不可外推**；⭐ 它只能支撑存在性结论。

⭐ 第四，**只读了 `### 1. 原文摘录`**。⭐ 这是遵 [../CONTINGENCY_L2.md](../CONTINGENCY_L2.md) §1.4 的取证规则（第 2/3 节是我们自己写的转述与溯源，拿它当外部依据等于自证），⛔ 但代价是：某条案例的时间/并发语义若只写在 `paper_content.txt` 而未被摘进摘录节，本审计看不到它。⭐ 这一点对 §5 的「零计时词元」结论尤其要紧——⛔ 它证明的是**摘录节里没有**，⛔ 不是**论文里没有**。

⭐ 第五，**没有审「误纳入」方向**。⭐ 任务限定审误排除，⛔ 所以界内 313 条只做了几项一致性抽查（`T0 ∧ 显式时钟 = 0`、`Hybrid` 全带连续耦合、37 条摘录含计时词元），⛔ 没有系统性检查是否有本该在界外的案例被放了进来。⚠️ 而 §5 末尾那条对称性说明，误纳入方向**确实存在**同类标签误差。

⭐ 第六，**数字全是 2026-08-12 快照**。⭐ `sources/` 是活语料库，⛔ 本文件的一切计数（746 / 313 / 433 / 139 / 134 / 110 / 96 / 32 / 37）都会随扩库失真；⭐ 复核时应重跑 §1 的命令与 `/tmp/l2audit/` 下的脚本，⛔ 不要引用本文件的数当常量。
