# paper1（STM issue discover）待办总清单

> ⭐ **需要人拍板的事项另见 [PENDING_DECISIONS.md](./PENDING_DECISIONS.md)**（2026-08-11 整理，9 条，分 🔴 必须定 / 🟡 建议定 / 🟢 确认即可 三档，每条含前因后果、全部可选方案与代价、我的建议）。⛔ 那份是**给人读的决策简报**，本文件仍是待办的唯一入口。

> **这是本论文所有待办的唯一入口。** 每一项都是 `* [ ]` 复选框，做完打勾并注明在哪个 PR 完成。
>
> 建立于 2026-08-11，由一轮全目录踩点产出。踩点范围：`story/` 与 `outline`、文献与 baseline 考据、`pipeline/` 与实验设计里的 repair 假设。
>
> **优先级口径**：
> - **P0** —— 不做会让论文的某条 claim 站不住，或会误导下一个动手的人
> - **P1** —— 论文成稿必须有，但不阻塞其它工作
> - **P2** —— 提升质量，可延后
> - **P3** —— 工程整洁，与论文结论无关

---

## A. 论文骨架与叙事

* [ ] **P0 · 重建 `story/` 的实质内容。** 当前是 placeholder（结构在、细节缺）。十节骨架（`TODO-O2` 裁定后由九节顺延而来，§编号已冻结）、三条 contribution、4 个 RQ 的结构已立起来，要逐节填实。材料：`story/README.md` 的 TODO 区块、归档在 `archive/r8_story_pre_rebuild/` 的上一版（那一版内容质量不低，是在时间压力下赶的，可大量借鉴）。
* [ ] **P0 · 调研后再裁定 contribution 2 的 claim 形状。** 【用户裁定 2026-08-11：先调研，不先裁定】导师原话是「现有 detection 方法报告错误，**缺少错误的上下文信息**」，但按字面写会被反驳（反例轨迹本身就是上下文、有文献把状态图改动反向映射回需求、有工作给 provenance）。**用户给出的调研口径**：前 LLM 时代**肯定有人做过证据链之类的**，这一点不必再论证；要查的是 **LLM 之后是否有人做过类似的、做到了什么程度**。⚠️ 所以这条的产出**不是**一句措辞，而是一份「LLM 时代的错误上下文 / 证据链工作」调研结论，据此才能定 claim 落在哪一档。⛔ 在调研出结论之前，不得把「别人没有上下文」写进正文的任何位置。卡住：Intro 攻击面、Related Work 组织方式、C-III 措辞。
* [ ] **P1 · 裁定 RQ 的数量与边界（被阻塞，暂不可裁定）。** 【用户裁定 2026-08-11】「**这个现在没法裁定，得先设定好 paper story / outline / contribution 后来决定**」。⛔ 因此**不要在本轮或下一轮尝试定 RQ**——先出 story / outline / contribution 的实质内容。⚠️ contribution 三条已定（见 A 组），但三条的**claim 强度**仍待文献调研，所以 RQ 的边界仍然浮动。当前 placeholder 按 4 个 RQ 立结构，那只是占位。
* [ ] **P1 · 「回归防护」这条贡献留不留。** `regression_guards` 是活字段、每格必写（smoke 里 16 条）、**零消费者**（全库只出现 2 次：`schemas.py:1143` 定义、`nodes.py:5703` 写入）。而 `README.md` 已把「为真的部分构成回归防护」写进 contribution 1。三选一：① 保留并标为「方法性质-未测」；② 保留并补一个消费者（ref 翻转率实验正好是它）；③ 字段与那句话一起删。
* [x] **✅ 已裁定（2026-08-11）· contribution 三条。** 【用户明确裁定】三条并列：**① 基于模型转换 + 模型形式化检查 / 仿真 / 验证的模型错误发现方法**；**② 基于归纳后的谓词逻辑的断言体系**；**③ issue 证据链体系**。⚠️ **② 就是谓词逻辑元模型本身**【用户澄清 2026-08-11】——「这个就是元模型啊，只不过是谓词逻辑元模型用于构建断言了而已」。⛔ 不要把它读成「元模型被降格」或「元模型与断言体系是两个东西」。**相对旧的 A 分法（①元模型 ②断言体系 ③证据链），本裁定做了两件事**：把 A 的 ① 与 ② 合并为一条（元模型即断言体系的构造依据），并**新增「方法整体」为第一条**——即模型转换 + 形式化检查 / 仿真 / 验证这条完整链路本身。⛔ 旧的 A / B 两套分法作废，不得再作为候选出现。⚠️ **三条各自的 claim 强度尚未定**——用户明示「得调研过文献后再进一步调整」，由 C 组的文献考据任务解锁。当前正文只能按三条排结构，**不得对任何一条给出强度断言**。
* [x] **✅ 已裁定（2026-08-11，PR [#180](https://github.com/HansBug/research_ideas/pull/180)）· 骨架里已有独立的 Problem Formulation 节。** ⚠️ 本条与下面 `TODO-O2` 那条**是同一个问题的两次登记**，一并关闭：裁定为**加一节**（新 §3 问题形式化），不在 §1 与 §3 之间二选一，全篇由九节变十节。详见 `TODO-O2` 条。
* [ ] **P2 · 「覆盖」一词在本文有三个互不相同的含义**：构造覆盖性（断言由全覆盖需求条目转换而来）/ `hit@k` 缺陷覆盖率 / 元模型表达力覆盖。中文尚可靠上下文区分，**英文写作会撞车**，需一并给出三者的英文区分。
* [x] **✅ 已裁定（2026-08-11）· fork/join 在定义层面排除。** 【用户明确裁定】「**这东西现在不在问题定义范围内，我建议直接定义层面排除，顶多 limitation 这边提一嘴**」。落法：在**问题定义**处给出建模对象边界 $M = (S, E, V, Tr, A)$，fork/join 与并发自然落在界外；**Limitations 一句话带过**即可。⛔ 不展开、不做 RQ、不做专门分析、不写成 finding。⚠️ session 7de1b210 里那套「fork/join 的四层写法」提案**已被本裁定取代**，不得复活。

* [x] **✅ 已裁定（2026-08-11）· 永久不设留出集。** 论证结构是：谓词逻辑元模型**来自领域调研**（文献、标准、技术资料），**不来自这批 pair**；既然方法的由来与 pair 无关，就不存在「在训练样本上评测」这个问题，因此 hold-out **没有任何存在必要**。⛔ 这**不是**「我们选择不用 hold-out」——按 [docs/protocol/method_provenance_policy.md](./discover_matrix/docs/protocol/method_provenance_policy.md) 的口径，**「为什么不留出」这个问题在本方法的论证结构里根本不出现**，论文里一笔带过即可，**不要专门辩护**。⚠️ 由此 BLUEPRINT 那版依赖 10-pair 留出集的 RQ2 设计**作废**，RQ2 的证据来源就是已有的 v46 全量（54 pair × 2 模型 × 3 轮）。
* [x] **✅ 已裁定（2026-08-11）· T1/T2 分层作废。** 【用户明确裁定】「**老的说法可以丢了，现在不谈人工的事情**」。T1 的动机是省人工判定成本，而 v46 已跑完 324 格全量，该动机不再成立。⛔ 正文**不谈人工判定成本**，也不按 T1/T2 分层组织实验节。⚠️ 冲突 X2 就此关闭。
* [ ] **P1 · 「裸给工具效果差」缺可引用证据（`TODO-S5`）。** 它是 §1.3 反面立论与 reviewer challenge 第 1 条的弹药，但目前只有我方的实践观察，没有可引用的公开证据。导师那句「业务建模的重要性」是对它的背书，不是它的证据。
* [x] **✅ 已裁定（2026-08-11，PR [#180](https://github.com/HansBug/research_ideas/pull/180)）· 恢复独立的 Problem Formulation 节（`TODO-O2`）。** 裁定为**加一节**，不在 §1 与 §3 之间二选一：[story/paper_outline.md](./story/paper_outline.md) 新增 **§3 问题形式化**（建模对象 / 任务 / 什么算一条合格的发现），三小节从 `archive/r8_story_pre_rebuild/story/paper_outline.md` 的旧 §3 **取回、未重写**。由此**现行版**原本的第 3 节（**领域分析与谓词元模型**）起**全部顺延一位，全篇十节**；§编号自本次交付起**冻结**，旧→新对照表见该文件〈§编号冻结〉一节。⚠️ 建模对象边界那句话的**唯一落点是 §3.1**，⛔ §1、§8、§9 都不得重复讲 fork/join。
* [ ] **P2 · 三条 contribution 的英文措辞（`TODO-T1`）。** 与「覆盖」三义的英文区分一并做。
* [ ] **P2 · 投稿 venue 与排期（`TODO-O9`）。** BLUEPRINT 里那份锚定 SANER 2027（09-21 abstract），**已过期**，需重做。

## B. 领域考据（导师点名要重点展开）

* [ ] **P0 · 补齐 19 个谓词的领域出处。** 实测：**只有 3 个**挂了 `provenance` 注释（`occupancy_after` / `stays_in` / `persists_until`），**16 个空白**。全库 15 条标注里 6 条不可引用——「形式语义中的预设」×2、「需求工程通则」、「需求可追溯性通则」、以及 **2 条指向本仓库自己的 `CLAUDE.md`**。而 `docs/protocol/method_provenance_policy.md` R1 要求出处必须是**可查证的外部文献、标准或工具规约**，为空则「补出处或从方法章节移除」。
* [ ] **P0 · 修 `method_provenance_policy.md` R1 自己的漏洞。** 它的示例里就写了「`#: provenance: 需求工程通则 —— …`」这种不可查证的写法，难怪实际标注里出现了 4 条同类。规范自身要先自洽。
* [ ] **P1 · 建 19 行谓词→领域来源映射表。** ⚠️ **本条与上面「补齐 19 个谓词的领域出处」是同一件事的两面，应一并做**——出处注释是代码侧的落地，映射表是论文侧的呈现，分开做会漂。 列：`谓词 | 族(S/B/P) | 归纳自哪类领域来源 | 具体文献/标准锚点 | 在 $M$ 上如何实例化 | 该来源类下未实例化的部分`。最后一列是 RQ1「表达力边界」的直接输入。候选来源类（**AI 凭记忆给出，必须自己核**）：Dwyer/Avrunin/Corbett ICSE 1999 property specification patterns、Autili et al. TSE 2015、Konrad & Cheng ICSE 2005 real-time patterns（⚠️ 整族未实例化，因 $M$ 无 $C$ 与 $Inv$）、OMG UML superstructure 状态机约束、Egyed 一系 model consistency rules、IEC 61131-3 / 61499、ISO 26262。
* [ ] **P1 · 查 OMG PSSM（Precise Semantics of UML State Machines）。** 它是 6 个仿真族谓词最正当的规范出处，**全库一次未提**。
* [ ] **P2 · 处理 4 个「台账侧 primary 计数为 0」的谓词。** `variable_declared` / `variable_delta_after` / `invariant` / `response_within`——它们的共同点是**台账从未把它们用作 primary**，⛔ **不是「从未被激活」**。实际使用情况差别极大（v46 报告 §6.6 谓词表）：

  | 谓词 | 台账侧 | 其中 primary | 产出侧已发布 | 产出侧生成 | 发布率 |
  | :-- | --: | --: | --: | --: | --: |
  | `variable_declared` | 2 | **0** | **197** | 240 | **82%**（全表最高） |
  | `variable_delta_after` | 2 | **0** | 6 | 43 | 14% |
  | `invariant` | 0 | **0** | 4 | 8 | 50% |
  | `response_within` | 1 | **0** | **0** | **0** | — |

  ⚠️ **`variable_declared` 的高发布率恰恰是坏消息**：PlantUML 没有变量声明语法，所以它对**任何**模型都为真、不具判别力——它是 `hit@1` 上界的**头号成因**（51 个命中位的判据引用了它，见报告 §6.2）。补出处时要把这一点写进去，而不是把它当成「好用的谓词」。⛔ **只有 `response_within` 是真正零使用。** 但也**不要**据此退役——见 D 组「查清 BMC 为什么用得少」，三个候选原因指向相反的行动。

## C. 文献与 baseline 考据

* [x] **✅ 已裁定（2026-08-11）· 新建一套 baseline 文库，旧库搁置但不归档。** 【用户明确裁定】「**完全按照新论文的口径调查 baseline 以及相关工作，之前的那部分暂时搁置，文库不要 archive 还可能有用，但是 baseline 得新建一套文库了**」。⛔ **不要 archive 现有 `baselines/`**——它是为 NL→STM 生成建的，与新口径不符但仍可能有用。⛔ 也不要改它的口径（改了就丢了它原本的用途）。✅ 新建一套面向 **issue discover** 口径的 baseline 文库，按仓库论文集规范配`README.md` / `GUIDE.md` / `SUMMARY.md`，写清收录范围与纳入 / 排除标准。⚠️ 这条解锁 C 组的三条补检索任务，它们应落进新库而不是旧库。
* [ ] **P0 · 补检索：断言 / 契约 / 可执行规约。** `baselines/` 匹配 `assert|contract|ocl|invariant` 的目录数 **= 0**。contribution 1 是一套断言体系，而它的**整片 related work 在仓库里不存在**。⚠️ **必须正面对照 OCL/USE/Epsilon(EVL) 与 Dwyer 的 property specification patterns，否则 C-I 会被质疑成「重造 OCL」。** 关键词簇：`"OCL" + ("well-formedness" | "constraint checking")`、`"design by contract" + model`、`("executable specification" | "runtime verification") + statechart`、`("specification pattern" | "property specification language")`、`("assertion generation" | "invariant inference" | "specification mining")`。
* [ ] **P1 · 补检索：错误定位与上下文 / 回归防护。**（服务 contribution 2）关键词簇：`("counterexample explanation" | "error explanation" | "fault localization") + model checking`、`("error report" | "diagnostic message") + ("usability" | "actionability")`、`("false positive" | "triage" | "review burden") + static analysis`、`("regression verification" | "proof reuse" | "incremental verification")`。⚠️ 「**静态分析告警的复核成本与误报代价**」这一族是 contribution 2 最硬的实证证据来源，三个库里**一篇都没有**。价值高于再多找几篇 detection 方法论文。
* [ ] **P1 · 补检索：状态机上的 detection。** `baselines/` 里一篇都没有；`state_machine_types/`（679 篇）里有 **172 篇**命中 model-check / verify / conform / diagnos / debug / test，但那个库按「形式主义地图」的轴写的，DESC 字段不记「输出带不带需求侧归因」。
* [ ] **P2 · 给 `state_machine_types/` 加一层 paper1 面向的派生视图。** 逐条记录：能担哪些谓词 / 输出物形态（反例 trace / 布尔 / 状态集）/ **输出带不带需求侧上下文**。⚠️ 但该库 README 明写「纯验证算法论文不应在这里扩张」——加视图前先定 owner。替代方案：只把最相关的 20–30 篇复制条目引用进 paper1 的 related work 工作区，不动原库。
* [ ] **P2 · 给 `corpora/repair_baselines/` 加 detection/repair 标注列。** 24 篇里 **13 篇是 detection-bearing**，尤其 Egyed 那条线的四篇正是 contribution 2 的 **靶子文献**。⛔ **不要整体移走**——移走等于把 Intro 的引文移走。⚠️ 目录名带 `repair` 而论文不做 repair，改名要动 29 处链接，与标注列一起做。
* [ ] **P3 · 修 `reproduction/` 的死链。** 它的 README/GUIDE 仍引用 5 个已被拆去 `project_ex1` 的路径（commit `67b4997a`）。

## D. 实验与测量

* [ ] **P0 · 补对照实验，⛔ 分两类。** 【用户明确裁定 2026-08-11】「直接自由 LLM 使用对照我们的 feedback loop」+「得看用途：整体性证明方法有效性就直接换全套朴素 LLM；证明某一个环节或 contribution work 才只改那一部分，这叫消融实验」。⭐ **两类分工**：**实验一·方法有效性对照**比的是两个不同方法，对照臂是**全套朴素 LLM**（⛔ **不**要求由删除派生，那会造出不自然的基线），回答 **C-①**；**实验二·消融**比的是同一方法去掉一个零件，⭐ **必须由删除派生**保唯一变量，逐条回答 contribution。**实验一先做**：1 轮 × 54 pair × 2 模型 = 108 格 → 196 位人工（全量 1/3）、墙钟 ~20 分钟；**消融首选 AB-1**（去闭合词表 → C-②，⭐ 人工成本 0，走 ref 翻转率）。⛔ **前置不可颠倒**：台账撰写时序必须先查清——若台账晚于方法产出，`60.4%` 是自相关量，两类实验一起塌。⛔ 两类都落在 588 冻结**之外**。完整口径见 [PENDING_DECISIONS.md](./PENDING_DECISIONS.md) §A2。
* [ ] **P0 · 补朴素基线。** 当前**没有任何外部对照**，60.4% 缺参照系。同两个执行模型、同 54 pair，不走八阶段循环，单提示直接列不符之处。⚠️ **成本被低估过**：算力上确实小（324 次单提示 vs 3621 次多阶段），但它同样需要**一整轮 588 位判定**——那是本项目最贵的人工投入；且基线产出是自由文本、无断言，`verdict_tiers.py` 的 A/B 层大概率整体失效。跑之前必须先选定减负路径。⚠️ **朴素基线 ≠ M0–M3 稻草人消融**：前者是**外部参照系**，后者是对手臂。M1/M2/M3 已被降为 future work，但基线不能跟着一起砍。
* [ ] **P0 · 交代台账的撰写时序。** 谁标的、什么时候标的、**是否在看过方法产出之后标的**、与命中判定是否同一人。⚠️ **若时序上晚于方法产出，60.4% 就不是覆盖率而是自相关。**
* [ ] **P1 · ref 翻转率实验。** 把为 pair X 生成的整套断言，拿去在同一份 NL 的**参考模型**上重新执行。预期：在错误模型上为 False 的断言应在参考模型上翻成 True。三个指标全部**零人工判定**：翻转率（判别效力）/ 残留 False / 参考侧误报。价值：`EIS-0029-05` 那条改判的理由逐字是「这条在参考模型上同样为 False——一个无法区分合规与不合规制品的断言不构成该缺陷的证据」，人工在 132 个位上发现 1 例，**这个检查能自动化到全部断言**。它同时是「回归防护」那条贡献的实证支撑。⚠️ 引用该例时注意：「132 个位」是 **v35 口径**，不是 v46 的 588 位；引用前必须回 v46 裁定记录核对，且不要与报告 §3.3 那条 boundary-ruled 记录（`EIS-0043-02`）混谈。⚠️ 「残留 False」这一格**二义**（断言写错 or 参考模型也有该问题），用作判别效力指标前必须先约定读法。⚠️ **风险已重新定位**：参考模型**不是**阻塞——实测 `Experiment Results.xlsx / STM Results` 第 D 列（表头 `PlantUML`）**60/60 行非空**，`source_meta.json` 的 `source_cells.reference_plantuml` 直接给出单元格，`pairs.jsonl` 带 sha256 可校验；规范化后恰好 10 份、在用 9 份。**真正未测的是 PlantUML → DSL 的编译成功率**——而参考模型是人写的、写法分布与 LLM 生成的不同，且这条链已被证明有损（46.5%），**参考侧的编译损失会直接污染「残留 False」这个指标**。
* [ ] **P1 · 定义 RQ3 的其余指标（`TODO-O7`）：需求覆盖率、断言密度、残留 False。** ⚠️ **需求覆盖率有自证风险**：若分母取方法自己拆出的义务条数，就是用产物量自己度量自己；取 NL 句子数则需人工清单，那就不再是零判定成本。跑之前必须先定分母。
* [ ] **P1 · 先估噪声底，再谈消融效果。** 它是「循环各阶段消融」的前置尺子——差小于代次内方差就不可归因。现成工具：`discover_matrix/instrument_ablation.py`（跨条件位移 vs 组内分歧的三档判据）。
* [ ] **P1 · 表示债务 46.5% 的归属需导师裁定。** 三种处置各有后果：从多报侧分母扣除（藏起工具链缺陷、precision 虚高）/ 计入误报（低估方法在作者原文层面的准确性）/ 单独成类报告（当前做法，代价是读者要理解中间表示）。
* [ ] **P1 · 表示债务的第二判定者盲判。** 46.5% 那一整块靠「人工回读作者源」认定，而该步不可机械复现、目前单人判定。抽 30 簇给第二人盲判、报一致率。
* [ ] **P1 · 命中形态的构成。** 四种等价形态中「蕴含更根本的原因」最宽。355 位按四形态拆开各多少？若相当比例靠最宽那一档，这个数的性质就变了。
* [ ] **P2 · 拒答文案回灌量的量化。** 同一机制在方法一节是设计优点、在上界一节是虚高成因，且尚未量化。从逐次调用记录里数：多少条已发布 issue 的断言是在收到拒答反馈之后才改成现在形状的。
* [ ] **P2 · 查清有界模型检查为什么用得这么少。** 只有 4 条记录用到、占命中 4.2%；3 个谓词里 `response_within` 零生成、`invariant` 台账零引用。三个候选原因**指向相反的行动**：① 建模边界不含不变式（那 `invariant` 该退役）；② 语料确实少这类义务（那是语料问题）；③ 生成侧从未识别这类句式（那该补生成路径）。判别方法：人工通读 9 份需求，找出全部「响应性 / 持续性」义务，看两侧各表达了多少。⛔ **在这件事做完之前，论文不得主张 BMC 必要，也不得据零使用就退役。**
* [ ] **P2 · 把命中位按「实际由哪一族断言支撑」重算。** 当前族归属来自**台账侧标注**，而**产出侧 86.6% 的已发布断言是结构族**，两者不一致。⚠️ **阻塞**：逐位判据是自由文本、无结构化 issue 引用，算不出来。要做需先改判定记录格式。
* [ ] **P2 · 循环各阶段的消融。** 八个阶段哪些必要？尤其两个审查阶段与静态预检——它们占算力大头却没有单独的收益证据。
* [ ] **P3 · 补齐 20 位缺逐位判据的判定。** 588 位中 568 位有判据、20 位无（15 位命中、5 位未命中），不可逐格复核。

## E. 口径与规范

* [x] **✅ 已查证（2026-08-11）· `wellformedness_attribution.md` 未生效。** 【用户要求当场查证】⛔ 结论不是「数据不足」，是**可证伪且已证伪**，且**只用 v46 单代数据**得出（符合「正文只讲 v46」口径）：该裁定主张把「上游可检出」缺陷移出能力分子与分母，但 **v46 被它移出的记录数 = 0**——`REPORTABLE` 的 98 条只扣了 `00x8` 越界 27 条与逐条边界裁定 1 条（`EIS-0043-02`），没有第三个来源；裁定文档自己点名的 9 条里仍有 **4 条在分母内**（`EIS-0035-01` / `0032-01` / `0047-01` / `0047-02`，占 24 判定位 / 11 命中位）；「上游可检出」与其强制要求并列报的双份数字在 v46 全部产物中出现 **0 次**。`hit@1 = 355/588 = 60.4%` 逐位复算与官方一致，说明**没有任何隐式扣除**。⛔ `discover_matrix/README.md` 此前两处写「生效中」是文档错误，已改为「已裁定、未落地」。
* [ ] **P0 · 裁定：运行时 `representation_debt` 门与台账侧分母裁定互相打架。** 【2026-08-11 查证时撞出，非计划内发现】存在一个**同名不同物**的机制确实在 v46 活体运行：`attribution_status` 门在证据踩到编译器合成元素时把 finding 标为 `representation_debt` 并**不发布**（v46-full 实测 103 项 / 49 格，其中 8 项提及 `UnspecifiedInitial`）。⛔ **它不是 `wellformedness_attribution` 裁定的实现**：作用侧不同（前者压制模型产出，后者改台账分母）、引入早 13 天、且该裁定明确否决过运行时方案。⚠️ **两者当前互相打架**：运行时门在 `0032` / `0047` 上压制了踩占位符的产出（这两条 v46 均为 **0/6**），而台账侧仍把同一批记录留在能力分母里**当漏检算**。也就是说我们一边不让模型报，一边因为它没报而扣分。这直接影响 `hit@1` 的解释，必须裁定，不能带着进论文。
* [ ] **P0 · 正文不得声称能力口径已排除「上游可检出」缺陷。** 【2026-08-11 查证导出的硬约束】v46 的 **60.4% 是「未剔除上游可检出缺陷」口径下的数字**——pyfcstm 投影阶段自己就会标出的占位符缺陷（`UnspecifiedInitial` 等）**仍算在我们的发现里**。⚠️ 审稿人一定会问「`initial_target` 判 `UnspecifiedInitial` 算不算你们的发现」，当前数字站在「**算**」这一侧，且至少 `EIS-0035-01`（5/6）与 `EIS-0047-02`（6/6）共 **11 个命中位**落在这个争议区内。⛔ 不得写「本方法的发现均为上游工具无法检出的」这类表述。两条出路：要么落地该裁定并重算（反事实为 `344/564 = 61.0%`，+0.6pp），要么在正文显式交代口径并给出争议区规模。
* [ ] **P1 · 「一条 issue = 一个缺陷」的操作化定义要不要改。** 代码里写的是「**一次模型编辑**能否同时解决」——`schemas.py:1008` 的 `a single model edit resolves all of them`、`prompts.py:143` 的 `would fixing that one place make both False results go away?`、`:151`。而 `docs/protocol/hit_criterion.md:60-62` **明令禁止**用同一句话当命中判据（理由：会误杀「合取项之一」与「蕴含更根本的原因」两种形态）。两者判的不是同一件事，不算矛盾，但**论文得解释为什么一处禁用一处依赖**。⚠️ 现成的替代措辞就在 `hit_criterion.md:62`：「两者陈述的是不是同一处建模失误」。⛔ 但改它属于**会影响模型行为的 prompt 改动**，按 `CLAUDE.md` §3.5.0 必须先过运行前 review，不能算文档整理。
* [ ] **P2 · `unexpected_taxonomy.md` 的 `N-SPLIT` 判据去 repair 化。** `:348-350` 把「这条断言若被采纳去修，修出来的对不对」立为**唯一判据**，还专门排除了不依赖修复的替代判据。`:169-173` 的分叉表列名就是「拆开是不是正确修法」。⚠️ 好消息：`:350` 已经把不依赖修复的等价理由写出来了——「把 AND 变成 OR，比现状更违反 NL」。所以改写是**纯措辞、不改任何判定结果**的。
* [ ] **P2 · `hit_criterion.md:86-88` 的一处 affirmative 用法。**「模型给的**修法**会把它一并搬走或删掉」——真正的判据是「严格超集且超出项是台账认定的正确元素」，改写掉「修法」二字不改结论。但它泄露了一个假设：**发布的 issue 里带有可供检视的修法**。

* [ ] **P2 · `invariant` 谓词的三选一处置（`TODO-M3`）。** 它在台账里零引用、产出侧只发布 4 次；而 $M$ 不含不变式，它最自然的用法按定义出界。三选一：保留但在论文里说明它为何存在 / 退役 / 重新定义其在 $M$ 内的语义。⚠️ 依赖 D 组「查清 BMC 为什么用得少」的结论，**不要先于它决定**。

## F. 工程与结构

* [x] **✅ 已结案（2026-08-11）· `wellformedness` 层口径：不动数字、论文不提。** 六路独立交叉核查后裁定。**查实**：`UnspecifiedInitial` / `InvalidInitial*` 由**本仓库自己的** `plantuml_source_lowering.py` 合成，pyfcstm 全库零命中、且交付给模型的制品上 `INIT` 家族诊断为 **0 条**（反事实：删掉占位符行再跑，`E_INITIAL_TRANSITION_INVALID` 立刻出现——**是我们的投影在它看到模型之前把缺陷补掉了**）。故 `wellformedness_attribution` 裁定的承重前提为假，**已作废**，且它本来从未落地。**裁定**【用户 2026-08-11】：转换是方法的一环（contribution ① 即「模型转换 + 形式化检查 / 仿真 / 验证」这条完整链路），缺陷在转换阶段暴露、中间表示如实反映、断言据此报出，**是方法按设计工作，主张没有越界**。⛔ **588 冻结**，不改分母 / 不改门 / 不重跑；⛔ **论文不提这件事**；⛔ 只有两句不能写：不写「pyfcstm 报了 X」、不写「我们发现的是工具查不出的缺陷」。
* [ ] **P2 · 修豁免门的判据依据：应看证据角色，不看需求声明的谓词。** 【2026-08-11 六路核查时发现，属下一代次的工程问题，⛔ 不进论文】`bind_attribution` 的豁免只覆盖**声明类**谓词（`initial_target` / `containment` / `*_declared`）；**行为类**谓词（`reaches` / `occupancy_after` / `stays_in`）的证据必然穿过投影插入的元素（`FinalWait*` / `R45RouteToken`），落到 `representation_debt` 而不发布。⚠️ 同一格里证据**逐字相同**的两条断言会因挂在不同需求下得到相反判决（`run1/0047-claude` 的 `AST-REQ-002-1` safe vs `AST-REQ-007-1` debt）。**实测影响**：全 324 格里，模型写出过与台账 primary 逐字同形断言、而台账仍判 0/6 的**只有 1 条**（`EIS-0002-02`，`run1/0002-claude`），即 1 个判定位 / 588，**远在噪声底（代次内极差 2.04pp）之下**。⚠️ 这是下界——语义等价但不逐字同形的被压制断言数不到。⛔ 修它需要重跑，故**不在 588 冻结期内做**；留给下一代次，且修的时候要连同「豁免读 role 而非 predicate」一并改。
* [ ] **P1 · 修 A 类仍坏的功能性路径指针（三处联动，必须同批改）。** 【2026-08-11 盘点】非 archive 下仍有 452 个 `.json` 含旧路径 `paper_stm_repair/`，其中**绝大多数是无 reader 的历史记录，按纪律不动**；下面三处是真·功能性指针，且**互相通过 hash 绑定，单独改任何一处都会炸**：**① `representation/reports/llms_emp_r45_java_60/manifest.json`** 的 `output_dir` / `pairs_path` 被 `plantuml_working_bundle.py` 真实解析。⚠️ 同目录 `PUBLICATION_SEAL.json` 记的 `manifest_sha256` **在改名之前就已漂移**，改 manifest 必须连带更新 seal；`implementation_tree_sha256` 亦已失效（该摘要含路径串）。**② `representation/schemas/working_fcstm_contract.schema.json` 的 `pattern`** 写死 `^…/paper_stm_repair/…`，与仍写旧路径的 `working_contracts/*.json` 目前自洽——**任何一侧单独改都会炸**。**③ 5 个 schema 的 `$id`**（URL 命名空间，功能无害），其中 3 个在 `IMPLEMENTATION_ROOTS` 内，改动牵动 ① 的摘要。⛔ 因此这三处**要么一起改、要么一起不动**，且改完必须重算两级摘要并跑全套。
* [ ] **P2 · 派生聚合体与成员不一致：`representation/reports/lowering_inventory.json`。** 【2026-08-11 发现】它是 4 份 per-example `lowering_inventory.json` 的聚合；per-example 那 4 份已在本轮改为新路径，聚合体 32 处仍是旧路径。它只被 schema 校验、不被 resolve，故按「无 reader 就不动」的纪律未改，但**聚合体与成员当前互相矛盾**。已验证无 hash 覆盖，改它零风险。
* [ ] **P1 · 两个静默掩盖机制，会让路径失效伪装成业务结论。** 【2026-08-11 从修 8 个测试时挖出】**① `conversion/cli.py:_replay_r31_normalized_preflight`**：读不到归档路径时**静默 `return None`**，于是 R3.1 归一化重放拿不到 → syntax preflight 失败 → 结果降级为 `partial`。症状是 `assert 'partial' == 'converted'`，⚠️ **看上去完全像业务结论，实际是一个字段的路径失效**。**② `readiness_audit/src/paper_stm_smoke/cli.py` 的 `load_index_payloads`**：对缺失文件 `if p and p.exists()` **静默跳过**，所以 `test_validate_reports_no_llm_or_env_boundary` 在 **1094 条记录全部指向不存在路径**时，仍以「0 条 payload 全部合规」通过——整个改名期间它一直是绿的。⛔ 这两处都属「缺文件 → 静默降级 → 检查消失」，与 `pytest.skip` 那类是同一族危险（绿灯比红灯危险）。修法：缺文件应报错或至少计数并断言计数非零。
* [x] **✅ 已完成（2026-08-11）· 死链扫描器入库并补齐三个覆盖缺口。** 此前它只存在于 `/tmp`（⛔ 会随重启消失，且 TODO 指向它等于指向不存在的文件），现已入库为 [tools/check_md_links.py](../../tools/check_md_links.py) 并配 17 项测试。补的三个缺口：**① 绝对 GitHub blob URL**——指向本仓库的 `blob/<ref>/<path>` 现在会对着工作区校验（`manual_review/eis_issue/` 那批停在旧路径的 URL，旧版一条都报不出来）；**② 行号越界**——`见 x.md 第 N 行` 且 N 超过文件行数的会被报出（⚠️ 只能查越界这一半，「在界内但指错内容」查不了，所以纪律仍是别用行号）；**③ 行内代码误报**——反引号里引用链接语法本身（如 `` `[X.md](...x.md)` ``）不再被当成真链接。⚠️ **这三个缺口的共同后果是「零死链」被反复误读为「引用都有效」**，本轮已因此误判多次。
* [ ] **P3 · 建立「改真源后必须重跑生成器」的检查。** 【2026-08-11 实测发现】`render_eis_issue.py` 的路径在文档树化那次（`df7ae9e5`）就已改对，**漏的是重跑这一步**，于是真源已新、派生物停在旧路径，持续误导了若干轮。⛔ 这不是「改了派生物」，是「改了真源没落地」——与既有纪律是互补的另一半。修法：给这类生成器加一个 `--check` 模式（重新渲染到临时目录并与现存产物对拍，有差异则退出码 1），接进 CI 或写进 GUIDE 的收尾检查。
* [ ] **P2 · 决定 `pipeline/evaluation/` 的去留。** 两份 v0 schema 是死的（`feedback_loop` 零 import），`source_issue_ledger.schema.json` 必填 `downstream_repair_allowed`，且 schema 层强制「`confirmed` ⟺ 允许下游修」——这是「issue 分级按可修复性分」的最赤裸形态。⚠️ **阻塞**：`pipeline/conversion/src/paper_stm_repair_conversion/evidence_integrity.py:17` 把它列在 `IMPLEMENTATION_ROOTS` 里，其 SHA-256 汇总就是 60-pair 表示层证据的 `generator_cli_sha256`。**移动或删除会改变一份已冻结证据的哈希。** 先查：那个 `generator_cli_sha256` 有没有被写进已发布 gist / PR comment / publication seal？
* [x] **✅ 已裁定并执行（2026-08-11）· 归档。** 【用户明确裁定】「归档」。落点 `archive/r9_agent_loop_pipeline/`，224 文件全部 rename、内容不改，配复活导引。前提已复验：`feedback_loop` 与 `discover_matrix` **零 import** agent_loop（只有 docstring 提到「从 legacy agent_loop 移植而来」）。
* [x] **✅ 已处理（2026-08-11）· 改 3 个，第 4 个随归档不再改名。** 【用户裁定：现在就解决】`paper_stm_repair_conversion` / `_representation` / `_smoke` 三个 live 包去掉 `repair` 字样。⚠️ **`paper_stm_repair_loop` 不改名**——它现在在 [archive/r9_agent_loop_pipeline/agent_loop/](./archive/r9_agent_loop_pipeline/agent_loop/) 内（原 `pipeline/agent_loop/`），该目录已按同日裁定归档，而**归档内容一律不改**（改归档等于篡改冻结件，本轮已有前车之鉴）。
* [x] **✅ 已处理（2026-08-11）· 改真源 + 重跑生成器。** 【用户裁定：现在就解决】⛔ **没有手改派生 md**——改的是 `render_eis_issue.py` 一侧的路径映射，再重跑生成器重建。⚠️ 重跑前后核对了人工签字 `- [x]` 计数不减少（本仓库有过 re-render 静默清空 6 行签字的事故）。

---

## 已完成（2026-08-11 本轮）

* [x] PR 链从四层塌成一层，两个被自动 merged 的 PR 各留说明状况 + 指路 comment
* [x] `paper_stm_repair/` → `paper_stm_issue_discover/`，实验资产收归论文目录
* [x] 三条旧路线归档（旧 agent loop / Path-1 评测链 / Path-1&2 指南），各配复活导引
* [x] 43 份平铺 md 树化为 `protocol/` `judges/` `findings/` `generations/` 四类
* [x] 补建 2026-08-08 导师讨论正式记录；`talks/SUMMARY.md` 同步新定调
* [x] 重构后 e2e smoke 验证（`0000` × 双模型，输入哈希与搬迁前逐字节相同）
* [x] 更正 `CLAUDE.md` §5 与根 `README.md` 的 LLM 配置机制描述（真源是 `.llmconfig.yml` 不是 `.env`）
* [x] 修正 v46r 替换后遗留的旧分母数字（41.3/54.0/16.1/4.0）与两处事实错误（净增量 2 条、九个判定组全部回读作者源）
* [x] 修复重构造成的 82 条净增死链，净增归零
* [x] `story/` 与 `experiment_design/` 归档并留 placeholder（本清单即其产物）
* [x] **裁定：永久不设留出集**（见 A 组首条）——冲突 X1 就此关闭
