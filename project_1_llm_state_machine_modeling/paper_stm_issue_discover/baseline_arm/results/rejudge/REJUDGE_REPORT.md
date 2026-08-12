# 在 X1 判定条件下重判主臂：判定仪器不对称能解释多少 pp？

> **一句话结论：解释不了。** 点估计是 **−4.1pp**（负号 = 把判定仪器对齐后，两臂差距**变大**而不是变小），95% CI **[−11.1pp, +1.2pp]**。⛔ 即使取 CI 上界，判定仪器不对称最多只能解释 14.9pp 里的 **1.2pp**。⭐ 原因是双向翻转都存在，且**反向翻转（hit→miss）比正向翻转（miss→hit）更多**：11.1% vs 6.7%。

---

## 一、要回答的问题

主臂（八阶段 feedback loop + 19 闭合谓词 + 形式断言）hit@1 = 355/588 = 60.4%；X1（单次朴素提示、自然语言输出）= 443/588 = 75.3%，高 14.9pp。已查明两臂的**命中判定不是同一套仪器**：主臂判定者看不到 NL 原文、看不到 PlantUML 作者源、issue 文本被截断、且没有「倾向命中」排序规则。

本实验问：**在与 X1 完全相同的判定条件下重判主臂的 `hit: false` 位，miss→hit 的翻转率是多少？** 若显著大于零，那 14.9pp 里就有一部分是判定伪影。

⭐ 关键设计决定：**必须同时做反向对照**。只重判 miss 位会系统性高估——重判本身会同时纠正两个方向的判定误差，只测一个方向等于只收不付。本报告把两个方向都报，并另列「只做单向」的数字以量化这一偏差有多大。

---

## 二、判定仪器的差异（本实验改变了什么）

| | 主臂 v46 原判定者看到的 | X1 判定者看到的 | 本次重判给的 |
| :-- | :-- | :-- | :-- |
| NL 原文 | ⛔ 没有 | 完整 | ⭐ 完整 |
| PlantUML 作者源 | ⛔ 没有 | 完整 | ⭐ 完整 |
| 台账 `statement` | 截断到 170 字符 | 完整 | ⭐ 完整 |
| 产出文本 | 截断到 230 字符；`--compact` 模式下**只有 title、完全不打 rationale** | 完整未截断 | ⭐ 完整未截断 |
| 「倾向命中」排序规则（§2.3） | ⛔ 没有（`7dc1cefe` 15:06 才加，而 `v46_human.json` 建于 `71e6d90d` 11:27） | 有 | ⭐ 有 |
| 「数作者源引用次数」硬判据（§2.4） | ⛔ 没有（`d9e6bb0d` 18:39 才加） | 有 | ⭐ 有 |
| 台账 `primary_predicate` / `layer` / `direction` | 有 | ⛔ 没有 | ⛔ 没有（与 X1 对齐） |
| 原判定的 `hit` / 论证 | — | — | ⛔ 不给（判定者盲于原判、也盲于该位属哪个样本） |

截断线的存在见 [present_for_judgment.py:84-88](/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/present_for_judgment.py)（`LIM_LED = 170`、`LIM_MOD = 230`，`--full` 才解除）；`--compact` 下不打 rationale 见同文件第 140 行 `if det and not args.compact`。

**命中承载规则保持不变**（⛔ 不能连这个也改，否则混淆）：沿用主臂自己的 A 层定义（[verdict_tiers.py](/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/verdict_tiers.py) docstring）——「**只看已发布 issue 引用的断言。被排除的发现不算命中 —— 它没有进入产物。**」这与 X1 侧「只有 `issues` 承载命中、`analysis` 不承载」是同一条规则。

---

## 三、抽样（机械可复现，判定之前落盘）

种子写死 `20260812`，脚本 [sample.py](./sample.py) / [sample_ext.py](./sample_ext.py)，样本清单 [sample.json](./sample.json) / [sample_ext.json](./sample_ext.json)。分层维度为 primary 谓词（比例分配 + 四个「主臂最弱谓词」保底），层内按 (model, run) 六桶轮转以平衡机型与轮次。

| 样本 | n | 覆盖 |
| :-- | --: | :-- |
| **miss 样本**（从 233 个 `hit: false` 抽） | 60 | 14 个谓词层；`reaches` 8、`edge_declared` 8、`guard_distinguishable` 5、`event_consumed` 3（四个最弱谓词全覆盖）；claude 30 / gpt 30；run 21/21/18；30 个 pair |
| **反向对照 · 阶段 1**（从 355 个 `hit: true` 抽） | 20 | 15 个谓词层；claude 8 / gpt 12；15 个 pair |
| **反向对照 · 阶段 2**（补样，见下） | 25 | 14 个谓词层；claude 13 / gpt 12；15 个 pair |

⚠️ **为什么补样。** 按预登记的 60/20 跑完后，主结果的 95% CI 是 [−14.5pp, +2.5pp]——宽到没有信息量，而方差几乎全部来自反向对照：它的权重是 355/588 = 0.604，样本却只有 20。⭐ **反向对照抽样不足恰恰是偏向主臂的方向**（少抽反向翻转 = 少扣分），所以补样是收紧而不是放宽。⛔ 第一阶段的 60/20 未作任何改动，预登记口径的数字照旧在下面单列。补样用同一套机械分层器、不同 tag 种子，从剩余 335 个 hit 位中抽，判定组同样盲。

---

## 四、判定流程

1. **重建判定材料**：33 + 15 = 48 份 per-pair 材料（`materials/`（⛔ 判定材料为中间产物、未入库；⭐ 可用 `build_materials.py` 重建）、`materials_s2/`（⛔ 判定材料为中间产物、未入库；⭐ 可用 `build_materials_s2.py` 重建）），每份含 NL 全文、PlantUML 作者源全文、涉及的台账 `statement` 全文（含 `nl_evidence` 与 `basis_superseded_by_ruling`）、以及被审格的**完整未截断**产出（issues 的 title + rationale + assertion_ids、已发布断言表、以及四类「落空」区块并明确标注不计入命中）。生成器 [build_materials.py](./build_materials.py)。
2. **判定**：13 个并行判定组（R1–R8 判 80 位、S1–S5 判 25 位），全部收到**物理同一份**指令 [rejudge_instructions.md](./rejudge_instructions.md)，其 §2 与 §3 逐字取自 [baseline_arm/judging_instructions.md](/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/baseline_arm/judging_instructions.md)。另加 §四反自利纪律：「只有当该格产出明确指向同一个模型元素与同一个缺陷事实、且你能把蕴含链一句话说清时，才判 `hit: true`。说不清就判 `hit: false`。」
3. **对抗性回读复核**（对应主臂 v46 的「一组回读原件复核」）：V1 复核全部 miss→hit 翻转、V2 复核全部 hit→hit 维持位，任务是**尽力推翻**。两组各自只读材料，不读仓库。
4. **主 session 裁定**：我逐位回读了全部 27 个第一阶段 `hit: true` 的原文，并做了两类机械核查（载体是否在 `excluded_findings` 内、同一条 issue 是否已被别的台账记录认领）。⭐ 裁定**只在收紧方向发生**，共收紧 5 位，全部在 miss 样本侧（即全部降低翻转率）。

---

## 五、结果

### 5.1 主结果

| 口径 | miss→hit | hit→miss | 主臂 hit@1 | Δ(X1−主臂) | 判定仪器可解释的 pp |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **主结果**（对照 n=45） | **4/60 = 6.7%** [2.6%, 15.9%] | **5/45 = 11.1%** [4.8%, 23.5%] | 60.4% → **56.3%** | 14.9pp → **19.0pp** | **−4.07pp**，95% CI **[−11.10, +1.17]** |
| 预登记口径（对照 n=20） | 4/60 = 6.7% | 2/20 = 10.0% [2.8%, 30.1%] | 60.4% → 57.0% | 14.9pp → 18.3pp | −3.40pp，95% CI [−14.47, +2.45] |
| 敏感性 A：判定组原始输出（未经主 session 收紧） | 9/60 = 15.0% [8.1%, 26.1%] | 5/45 = 11.1% | 60.4% → 59.6% | 14.9pp → 15.7pp | −0.76pp，95% CI [−8.21, +5.11] |
| 敏感性 B：**只做单向重判**（不含反向对照） | 4/60 = 6.7% | （不测，记 0） | 60.4% → 63.0% | 14.9pp → 12.3pp | +2.64pp，95% CI [−0.94, +5.55] |

比例的 CI 用 Wilson；「可解释 pp」的 CI 用 Beta(Jeffreys) 后验的 20 万次蒙特卡洛（脚本 [analyze.py](./analyze.py)，种子写死）。正号 = 缩小两臂差距。

⭐ **敏感性 B 就是「只重判对我方有利的那一侧」会得到的数字：+2.6pp。** 它比主结果高 6.7pp，且符号相反。这正是必须做反向对照的理由。

### 5.2 逐条：4 个 miss→hit 翻转

| 位 | 谓词 | 形态 | 复核强度 | 依据 |
| :-- | :-- | :-- | :-- | :-- |
| `EIS-0010-05\|run3/0010-gpt` | `event_consumed` | 直接对应 | clear | 已发布 issue [7][8][9] 逐字对应台账点名的 AutonomousIdle / AutonomousActive / AutonomousFinal 三态「Power_Off 未结束运行」，一一齐全 |
| `EIS-0010-05\|run1/0010-gpt` | `event_consumed` | 合取项之一 | defensible | issue [10]「Autonomous 和 auto final 中 Power_Off 未终止运行」证到台账三态合取里的 AutonomousFinal 一项，rationale 逐字给出同一根因「只声明了从 HumanDriving 发出的 Power_Off 边」 |
| `EIS-0014-04\|run1/0014-gpt` | `action_declared` | 直接对应 | clear | issue [5] 的 rationale 逐字写「不能承载在 Approaching 中发送 **Send** 信号」+ issue [6]「Send 事件未声明」，与台账「Send 动作在全模型任何相位都不存在」同指 |
| `EIS-0014-03\|run2/0014-gpt` | `state_declared` | 合取项之一 | defensible | issue [4]「EmergencyStopping 未声明 entry 动作」证到台账二元合取的前一项；[hit_criterion.md §4.2](/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/hit_criterion.md) **逐字把这个 case 当作同源判据的实例**（`Entry` 在状态命名空间只出现一次） |

### 5.3 逐条：5 个 hit→miss 反向翻转

| 位 | 谓词 | 依据 |
| :-- | :-- | :-- |
| `EIS-0030-02\|run1/0030-gpt` | `event_consumed` | 台账要的是「Autonomous 侧缺 power off 终止边」；该格唯一涉断电的断言 `terminates:HumanDriving:Power_Off` 结果为 **True**，全格无任何 Autonomous 侧断电主张 |
| `EIS-0040-03\|run1/0040-claude` | `occupancy_after` | 台账指 `[*] --> AutoInitial : Enter Autonomous Mode`（初始迁移带触发）；3 条 issue 全在 front_distance 变量与事件融合，且其命题「进不了 Autonomous」与台账「已进入但内部无激活」方向相反 |
| `EIS-0040-03\|run2/0040-claude` | `occupancy_after` | 同上；`AutoInitial` / `Enter Autonomous Mode` 在该格全部 issue、rationale 与断言表中一次都没出现 |
| `EIS-0042-01\|run2/0042-gpt` | `occupancy_after` | 台账记 `[*] --> Off : keyOff` 上的**触发**误挂；唯一 issue 主张的是初始迁移**目标**错，且与台账方向相反（台账认可 Off 作初始目标） |
| `EIS-0007-03\|run1/0007-claude` | `NONE` | 台账记 `OperationalControls` 整棵子树为臆造；该格唯一沾边的 cardinality 论证把多出的那个判为 `InitialState`，等于把 `OperationalControls` 当成合法区域，方向相反 |

### 5.4 分层

**按 primary 谓词（miss 样本，翻转数/样本数）**

| 谓词 | 翻转 | 谓词 | 翻转 |
| :-- | :-- | :-- | :-- |
| `event_consumed` | **2/3** | `reaches` | **0/8** |
| `state_declared` | 1/5 | `edge_declared` | **0/8** |
| `action_declared` | 1/4 | `initial_target` | 0/7 |
| | | `guard_distinguishable` | **0/5** |
| | | `NONE` | 0/8 |
| | | 其余 6 个谓词层 | 0/11 |

⭐⭐ **这是本实验最有结构意义的发现**：主臂最弱的两个谓词 `reaches`（32 个 miss 位）与 `edge_declared`（29 个 miss 位）**一个都没翻**，`guard_distinguishable` 也是 0/5。**主臂在这三类上的低命中不是判定伪影，是真实的能力缺口。** 翻转全部集中在 `event_consumed` / `action_declared` / `state_declared` 这类「动作与事件声明」缺陷上。

**按 model**：claude 0/30，gpt 4/30。**按 run**：run1 2/21、run2 1/21、run3 1/18。**按 pair**：仅 `0010`（2/2）与 `0014`（2/2）——4 个翻转集中在 2 个 pair。

---

## 六、机制：这 4 个翻转是怎么产生的

⭐ 逐位回读原判定论证后，四个翻转的成因都能被具体指认，而且**都不是「判据放宽」，是「原判定读错了材料」**。

### 6.1 `EIS-0014-04`：判定翻转在 **title 措辞**上，与能力无关（最干净的伪影）

同一轮（run1）、同一 pair、同一个缺陷，两条臂被判成相反结论：

| 格 | issue [5] 的 **title** | rationale 是否点名 Send | 原判定 |
| :-- | :-- | :-- | :-- |
| `run1/0014-claude` | 「Approaching 未声明 during 动作**以承载持续接近与 Send 信号**」 | 是 | **hit** |
| `run1/0014-gpt` | 「Approaching 缺少 during 动作声明」 | **是**（「不能承载在 Approaching 中发送 Send 信号…」） | **miss** |

原判定对 gpt 位的论证逐字是：「该格的 Approaching 动作类 issue **未点名 Send**（只说「缺少 during 动作声明」）」——⛔ 这句话只对 **title** 成立，对 rationale 不成立。这与 `present_for_judgment.py --compact` 下不打印 rationale 的行为吻合。⭐ **两条臂的产出在实质上完全一样，判定差异 100% 来自标题措辞。**

### 6.2 `EIS-0010-05` 两位：原论证描述的**不是这一格**

原判定对 `run1/0010-gpt` 的论证写「该格 **6 条** issue 中唯一涉及 Power_Off 的是 issue[6]…全部释放断言里与 Power_Off 相关的只有 `AST-REQ-012-1`（terminates(HumanDriving, Power_Off)=False）与 `AST-REQ-012B-1`」。

实际核对：`run1/0010-gpt` 有 **10 条** issue，其中 **issue [10]「Autonomous 和 auto final 中 Power_Off 未终止运行」**（`AST-REQ-014-1` / `AST-REQ-015-1` 均为 False）正是台账所指；该格的 HumanDriving-terminates 断言 id 是 `AST-REQ-013-1` 而非 `AST-REQ-012-1`，且 `AST-REQ-012B-1` 在该格不存在。同 pair 的其余 5 个格也没有一个符合「6 条 issue + AST-REQ-012-1」的签名。`run3/0010-gpt` 同理：原论证说「Power_Off 相关主张只有 issue[6]」，实际有 5 条（issues [5]–[9]），其中三条逐字点名 AutonomousIdle / AutonomousActive / AutonomousFinal。

⛔ 这是**事实性错误**，不是判据分歧。

### 6.3 `EIS-0014-03`：原论证与 `hit_criterion.md` §4.2 直接冲突

原论证：「台账主张多出虚假子状态 EmergencyStopping.Entry；该格报的是缺 entry 动作，**多与缺方向相反**。」

但 [hit_criterion.md §4.2](/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/hit_criterion.md) 把**这个 case 本身**当作同源判据的工作实例：「`0014` 的 `Entry` 作为状态同样只有第 25 行一处（第 7 行的 `Entry/Accelerate` 是迁移标签，属事件命名空间……）（`Entry: Emergency Stop`，一条语句同时隐式声明了状态、又没声明 entry 动作），故「多出虚假子状态」与「缺 entry 动作」**同样同源**。」⭐ 该条款于 `d9e6bb0d`（18:39）写入，而 `v46_human.json` 建于 11:27——**判定发生在判据存在之前**。

### 6.4 判定沿用的证据面

对全部 228 条有论证的 miss 位做的统计：

- **56.1%（128/228）的 miss 位共享逐字相同的论证**，最大一簇覆盖 14 位。
- 只有 **4.4%（10/228）** 的论证点到了具体 issue 编号或 id。
- **11.4%（26/228）** 的论证明写「与 v37/v41/v44 同形态判定一致」「历代 0/6」这类沿用措辞——`EIS-0014-03` 与 `EIS-0014-04` 两个翻转位都在此列，即它们的 miss 判定是从更早代次**继承**的，而 v46 的 gpt 产出与那些代次已经不同。

---

## 七、主 session 收紧掉的 5 位（都在降低翻转率的方向）

判定组原始输出是 9 个 miss→hit；我裁定掉 5 个，理由都是机械可核的：

| 位 | 判定组 | 裁定理由 |
| :-- | :-- | :-- |
| `EIS-0002-02\|run2/0002-claude` | R6 判 hit（carrier=assertion） | 载体 `AST-REQ-009-1`/`010-1` 在 `excluded_findings` 内，且**无任何已发布 issue 引用** |
| `EIS-0005-01\|run1/0005-gpt` | R6（assertion） | 载体 `AST-REQ-002-1` 同上 |
| `EIS-0005-01\|run2/0005-claude` | R6（assertion） | 载体 `AST-REQ-002-1` 同上 |
| `EIS-0035-03\|run1/0035-gpt` | R5（assertion） | 载体 `AST-REQ-019-2` 同上 |
| `EIS-0033-02\|run2/0033-gpt` | R7（issue） | ⛔ **一果两记**：所援引的 `ISSUE-substates-outside-PumpControl` 逐字对应 `EIS-0033-01`（「三子态被声明成 PumpControl 的兄弟」，primary = `containment(PumpControl, PumpState)`），而 `EIS-0033-01` 在该格**已判命中且全语料 6/6**；同一条发现不得再认领 `-02` |

前四条依据的是主臂自己的 A 层定义（「被排除的发现不算命中」），与 X1 侧「`analysis` 不承载命中」是同一条规则——⭐ 我在指令 §3.1 里给判定组开了「已发布断言可承载」的口子，事后核查发现这四条全部落在被排除区块内，因此按两臂共同的规则收回。第五条是我在对抗性复核组 V1 提示「有一果两记风险」后回台账查证的（V1 本身被禁止读台账，无法自证）。

⚠️ 对称性说明：反向对照侧的 22 个「维持命中」我做了同样的机械核查（载体全部为已发布 issue、样本内无同格多记录重复计入），未发现需要收紧的位；对抗性复核组 V2 对第一阶段 18 位逐位尝试推翻，0 位被推翻。

---

## 八、局限

1. **反向对照仍偏小**（n=45 对 355 个 hit 位）。它贡献了主结果方差的约 82%。CI 上界 +1.17pp 依赖于反向翻转率不低于约 4.8%（Wilson 下界）。
2. **补样是看到第一阶段结果之后决定的**。理由（方差被对照支配、且欠采样偏向主臂）写在补样脚本里、抽样机械且判定组盲，但它终究不是预登记的；因此预登记口径（60/20，−3.40pp）单列在结果表里，两者结论方向一致。
3. **判定者是 LLM 判定组，不是原来那批人**。因此本实验测的是「同一套判定条件下、同一套指令下的重判结果差异」，⛔ 不能排除判定者本身的能力差异贡献了一部分翻转。缓解措施：判定组盲于原判与样本归属；对抗性复核组尝试推翻；主 session 逐位回读全部 `hit: true`。
4. **只重判了 `hit` 侧的判定，没有重判 X1 侧**。若把同一批判定组放到 X1 材料上，X1 的 75.3% 也可能变动。本实验测的是「主臂在 X1 条件下会变成多少」，⛔ 不是「两臂在第三套条件下各是多少」。
5. `EIS-0014-03` 的翻转依赖 `hit_criterion.md` §4.2 对 `0014` 的裁定；该条款同时说 `0037` 的同型结构因另一理由（严格超集且超出部分点到正确元素）不算命中。若有人把 §4.2 读成「0014 与 0037 都不算命中」，该位应退回 miss，主结果变为 3/60 = 5.0%，可解释 pp 变为 **−4.77pp**（更负）。

---

## 九、⭐ 结论

> **这 14.9pp 里，判定仪器不对称能解释 −4.1pp（点估计），95% CI [−11.1pp, +1.2pp]。**
>
> ⛔ **它解释不了这个差距，方向上甚至是反的。** 把两臂的判定仪器对齐之后，主臂的 hit@1 从 60.4% 降到 **56.3%**，两臂差距从 14.9pp **扩大到 19.0pp**。
>
> ⭐ 即便取 95% CI 的最有利上界，判定仪器不对称最多只能解释 **1.2pp**，占 14.9pp 的 8%。⭐ 即便用「只重判对我方有利的一侧」这种已知偏高的设计，也只有 +2.6pp（CI 上界 +5.6pp）。

**为什么点估计是负的**：判定仪器不对称确实造成了主臂的漏判（miss→hit 6.7%，且其中至少两位是可指认的纯伪影——title 截断、原论证描述了别的格），⛔ **但它同时也造成了主臂的误判为命中**（hit→miss 11.1%）。后者数量更大，因为它作用的基数更大（355 vs 233）。原判定的**论证质量普遍偏低**（56.1% 的 miss 位共享逐字相同论证、只有 4.4% 点到具体 issue）——这种低质量在两个方向上都会出错，而不是单向地压低主臂。

**对方法结论的实质影响**：⭐ 主臂在 `reaches`（0/8）、`edge_declared`（0/8）、`guard_distinguishable`（0/5）三类上**零翻转**。这三类合计占 233 个 miss 位中的 80 个（34%）。**主臂在这些类别上的低命中是真实的能力缺口，⛔ 不能用判定伪影解释掉。**

---

## 十、产物清单（全部可复核）

| 文件 | 内容 |
| :-- | :-- |
| [sample.py](./sample.py) / [sample.json](./sample.json) | 第一阶段抽样器与样本清单（60 miss + 20 hit），种子 `20260812` |
| [sample_ext.py](./sample_ext.py) / [sample_ext.json](./sample_ext.json) | 反向对照补样（+25） |
| [build_materials.py](./build_materials.py) / `materials/`（⛔ 判定材料为中间产物、未入库；⭐ 可用 `build_materials.py` 重建） | 33 份第一阶段判定材料 |
| [build_materials_s2.py](./build_materials_s2.py) / `materials_s2/`（⛔ 判定材料为中间产物、未入库；⭐ 可用 `build_materials_s2.py` 重建） | 15 份第二阶段判定材料 |
| [rejudge_instructions.md](./rejudge_instructions.md) | 发给全部 13 个判定组的**物理同一份**指令 |
| [verdicts/R1..R8.json](./verdicts/) · [verdicts/S1..S5.json](./verdicts/) | 13 个判定组的原始输出（105 位，含逐位论证） |
| [verdicts/V1_recheck.json](./verdicts/) · [verdicts/V2_recheck.json](./verdicts/) | 两个对抗性复核组的输出 |
| [positions_final.json](./positions_final.json) / [positions_final.md](./positions_final.md) | 105 位的 original / regroup / final 三栏对照 + 变化位的论证全文 |
| [analyze.py](./analyze.py) / [stats.json](./stats.json) | 统计脚本与四种口径的完整数字 |

⛔ 两个仓库 clone 均未被修改（本实验只读）。
