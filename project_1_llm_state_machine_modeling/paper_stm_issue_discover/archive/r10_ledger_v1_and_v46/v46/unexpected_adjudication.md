# v46 意外发现（unexpected）逐条裁定

对 v46 全量 324 格产出中、**未匹配到任何台账记录**的同质簇逐条人工裁定。

- 桶内 **288 条目 / 124 去重 / 43 个 pair**（去重单元 = `(pair, 根因)`）。
- 分母闭合：`288 + 14 + 2 = 304`。14 条内容已被现有台账记录承载，按定义不属意外发现，物理存放在 [unexpected_verdicts/ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl)；2 条的断言在冻结制品上求值为 **True**（模型满足该义务、正确地不产出 issue），属真阴性，存放在 [unexpected_verdicts/not_produced.jsonl](./unexpected_verdicts/not_produced.jsonl)。

⛔ **全部交叉表只有一个产地**：[unexpected_tables.md](./unexpected_tables.md)（表 0 分母闭合 / 表 1 大类双分母 / 表 2 子类双分母 / 表 3 谓词族×裁定 / 表 4 稳定性 / 表 5 合并规模），由 [../rebuild_unexpected.py](../scripts/rebuild_unexpected.py) 从 `unexpected_verdicts/G*.jsonl` 机器生成。**本文件不保存任何一张交叉表的副本**，只写结论与判据；逐簇判据见 [unexpected_evidence.md](./unexpected_evidence.md)，裁定口径见 [unexpected_taxonomy.md](../../../discover_matrix/docs/protocol/unexpected_taxonomy.md)。

## 一、最重要的两条结论

**第一，净增量是 2 条。** 288 条目里只有 `0014-4` 与 `0010-2` 同时满足「事实为真 + 作者源确实没写 + NL 有逐字依据 + 台账未记」四条判据，见 §三。**论文里能说的是 2，不是 286。**

**第二，占比最大的一块根本不是模型缺陷。** 表示债务 134 条目（46.5%）/ 30 去重（24.2%），是**我们自己的转换管线的表示债务**——作者在源制品上已逐字表达，是中间表示装不下。

支撑这两条的是同一个事实：

**`model.fcstm` 不是作者原件，`stm0.puml` 才是。** R4.5 下沉会把 PlantUML 的整条迁移标签压成一个事件名，该债务在每份制品的 `fcstm_meta.json` → `source_static_reason_codes` 里已声明（`R45.DEBT.opaque_transition_label_semantics`，60 份制品里 58 份带此码，是最高频的债务码）。

最清楚的证据是 pair 0029 的作者源第 33 行：

```
collision_avoidance_deactive --> collision_avoidance_active :
    pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode
```

作者写的是一条**完全合法的析取守卫**，NL 12 的四个激活源一个不缺。发现模型报的「四个激活源被压成一个融合事件、模型无法只凭其中一个激活」，指的是**下沉之后**的形态。[fused_event_policy.md](../../../discover_matrix/docs/protocol/fused_event_policy.md) 对此已有既定裁定：断言阶段必须接受合并事件并记录表示限制，而**「表示限制被如实记录、但记录本身不构成发现」**。

同理，`variable_declared(X)=False` 这一族**没有判别力**：PlantUML 无变量声明语法，全语料 **60 份** `model.fcstm` 中，33 份的唯一 `def` 是转换器注入的 `R45RouteToken`，另 27 份连一行 `def` 都没有，**作者变量 0/60**（`grep -h "^\s*def " */model.fcstm` 可复算）。既定分界是**作者源有没有表达该量**——0036 的 `/ UAV Count Decreased` 判表示债务，0006 的「作者源里连递减文本都没有」才判真缺陷。

## 一之二、⚠️「下沉」指什么——不是置信度分级

**「下沉（lowering）」是数据准备阶段的 PlantUML → FCSTM 编译动作，与 discover 流水线的置信度、降级、成熟度分级毫无关系。** 容易误读，此处钉死：

```
作者手写 stm0.puml  ──R4.5 转换（下沉）──▶  model.fcstm  ──▶  discover 流水线读这一份
   （真正的作者原件）                        （编译产物）
```

R4.5 是 **PlantUML 表达力 > FCSTM 表达力** 时的有损编译。PlantUML 允许在一条迁移标签里写 `a | b & c`、写 `trigger / effect`、写 `trigger [guard]`；FCSTM 的 `event` 是一个原子标识符，装不下这些，于是整条标签被塞进一个事件名。这不是「输出了但不够确信」，而是 **信息在我们自己的编译步骤里被压平了，且压平这件事被如实登记在案**——每份制品的 `fcstm_meta.json` → `source_static_reason_codes` 里写着债务码。

| 债务码 | 带该码的制品数 /60 | 含义 |
| :-- | --: | :-- |
| `opaque_transition_label_semantics` | 58 | 整条迁移标签被压成一个不透明事件名 |
| `composite_source_activation_dispatch` | 28 | 复合态出边的激活派发被改写 |
| `opaque_state_body_semantics` | 27 | 状态体描述行被压进状态名 |
| `missing_explicit_initial` | 16 | 缺显式初始，注入伪初始态 |
| `concurrent_region_semantics` | 9 | 并发区语义被改写 |
| `multiple_initial_fanout` | 9 | 多初始扇出 |
| `composite_source_external_reentry` | 7 | 复合态外部重入 |
| `ambiguous_unlabeled_fanout` | 6 | 无标签扇出歧义 |
| `invalid_source_initial_target` | 5 | 非法初始目标 |
| `explicit_concurrency_pseudostate` | 3 | 显式并发伪态 |
| `invalid_source_final_scope` | 2 | 非法终态作用域 |
| `source_input_normalization` | 1 | 源输入归一化 |

⚠️ 该表是**制品级债务码清点**，不是本桶的交叉表，独立于 `G*.jsonl`，复算命令见 §七。⚠️ **该码是制品级存在标志，不是实例计数**——一份制品里发生了多少处损失不体现在此表。⚠️ 每个码在 `source_static_reason_codes` 与 `simulation_reason_codes` **两个数组里各列一次**，用 `uniq -c` 数会得到恰好 2 倍的数字。正确命令是 `grep -l <code> */fcstm_meta.json | wc -l`。

所以「表示债务」这一裁定的准确含义是：**断言报告的现象在 `model.fcstm` 上客观为真，但它描述的是我们的编译损失，不是作者建模的缺陷。** 发现模型没做错——它看到什么报什么；错的是把这类报告计入「模型缺陷」。完整论述见 [representation_debt.md](../../../discover_matrix/docs/findings/representation_debt.md)。

## 二、终态分布：读表须知

数字一律读 [unexpected_tables.md](./unexpected_tables.md)，逐 pair 分布见 [unexpected_verdicts/by_pair.tsv](./unexpected_verdicts/by_pair.tsv)，逐簇归属见 [unexpected_verdicts/cluster_index.tsv](./unexpected_verdicts/cluster_index.tsv)。本节只写从表里能读出、而表本身不会说的四条结论。

**（1）两套分母给出相反的主要矛盾**（表 1）。按条目读，最大块是编译债务；按去重读，最大块是断言侧的过度规定——因为表示债务的条目/去重比 4.47 远高于无 NL 依据的 1.78，同一处损失被反复重述的程度高得多。**只报一套会得出错误的整改优先级。**

**（2）意外发现不带 A/B/C 分层**（表 4）。A/B/C 只作用于**台账记录的命中位**，而意外发现按定义没匹配台账。这批上真正存在且可比的分级维度是**稳定性**：该簇在 6 个格（2 臂 × 3 轮）中出现了几次，与仓库既定的 `@k` 口径同源。

**（3）多报以单次采样噪声为主**：174/288（60%）只出现在 1 个格里。两条真漏记分别出现在 2 格与 3 格，而仅有的三个 6/6 全满格都是表示债务——这不奇怪：表示债务是制品的确定性属性，每次都能看见；真正的新发现靠的是采样运气。**含义是——即便模型确实找到了台账外的真缺陷，它也找得不稳。**

**（4）子类划分维度各不相同**（表 2），成分分析见 [composition.md](./composition.md)：表示债务按「丢失的是哪一条区分」切（`D1` 析取备选融合 / `D2` 原子子表达式不可寻址 / `D3` 槽位焊死 / `D5` 跨通道打包 / `D4` 结构性下沉债务），无 NL 依据按「相对 NL 真实义务、多要求的那一部分是什么」切，假阳性按「索要形式与实际承载者差在哪一个槽位」切，越界按「越的是哪条边界」切。⛔ **谓词族一律不参与判类**——它是同一条损失的不同说法。

### 关于表 3（谓词族 × 裁定）的读法

⛔ **该表的分母是「未匹配到台账的簇」，不是该谓词的全部产出。** 它度量的是 **「该谓词误触发时，误触发的性质是什么」，不度量该谓词的检出效用**——后者的分母必须是该族的全部已发布断言（命中 + 未命中 + 未匹配），本轮未按此口径统计。

**因此该表不支持「应优先选用某谓词族」这一结论。** 它支持的是一条更窄但成立的结论：

> **存在性谓词的误触发中，编译债务占绝对多数**（`event_declared` 78/158、`variable_declared` 46/48），**而可达性谓词的误触发几乎不含债务成分**（`reaches` 8 条中 6 条越界、1 条债务）。这是「债务沿标识符通道传播」的证据。

⚠️ 反向证据必须一并给出：命中侧的判定理由里，存在性谓词恰恰是主力（`initial_target`、`containment`、`cardinality`、`state_declared` 均在命中判定的 `argument` 中高频出现，而 `reaches` 只对应个位数命中）。**按该表去砍存在性谓词会砍掉绝大部分真实检出。**

⛔ **谓词词表保持不动。** 失真源在编译不在谓词；中途改词表会作废 v37→v46 全部跨代次可比性；且 `variable_declared` 的作者变量 0 产出这一行**本身就是证据**，删掉谓词等于删掉证据。**正确做法是在归因侧对已产出的结果打标**：凡 `*_declared` 返回 False，查该制品的债务码，命中则计入债务报告而非缺陷。该实现**不触及谓词层**。

## 三、两条净增量：`0014-4` 与 `0010-2`

[unexpected_verdicts/final_rootcause.tsv](./unexpected_verdicts/final_rootcause.tsv) 有两行；两条的逐条判据字段（`fact` / `nl` / `note`）分别在 `unexpected_verdicts/G7.jsonl` 与 `G9.jsonl` 的对应簇上，下表与本节文字均以那两处为准。

| 根因 | pair | 缺陷 | 作者源判据 |
| :-- | :-- | :-- | :-- |
| `0014-ROOT` | 0014 | NL 3「发出 Obstacle Detected 信号」被吞进状态名描述串，`EmergencyStopping` 内无任何 `enter`/`during` 动作 | `stm0.puml:26` 写 `EmergencyStopping: Obstacle Detected`（PlantUML **描述行**，不是动作语法）；对照同一份 NL 的 0054:18 `do/Send Obstacle Detected`、0004 `during abstract SendObstacleDetected` —— 该输出动作在 $M$ 内可表达且是参考意图，作者用错了语法 |
| `0010-ROOT` | 0010 | 接管迁移只挂在 `AutonomousActive` 一个子态上，自动驾驶模式的其余每一处都静默丢弃接管信号 | `stm0.puml:15/16` 只写了 `AutonomousActive --> HumanDriving : Human Steering Cmd` 与 `: Brake Pressed`，模式一级与 `AutonomousIdle` 上**根本没写**；编译产物 `model.fcstm:17/18` 与作者源在这点上逐条一致，不存在 R4.5 损失，故不落表示债务 |

**`0014-4` 台账未覆盖，逐条核对**：`EIS-0014-03` 的 `nl_evidence` 只引「Emergency Stop」，`EIS-0014-04` 的 scope 是 `InMotion.Approaching`，二者均不涉及 `EmergencyStopping` 上的 Obstacle Detected 输出动作。⚠️ 正确修法是**动作**而非独立事件，归并时按 $M$ 的 `A` 记。

**`0010-2` 事实与 NL 依据**：`Autonomous`（`model.fcstm:9`）本身是可被占据的叶态，由 `model.fcstm:14` 的 `HumanDriving -> Autonomous : /Power_On;` 进入；`AutonomousIdle`（`model.fcstm:10`）由 `model.fcstm:15` 进入。两者都不消费 `Human_Steering_Cmd` / `Brake_Pressed`，也没有任何出边通向 `HumanDriving`。NL08 第 4 句逐字 `transit to human driving mode when receive human steering cmd, brake pressed`，**未给任何源态限定**；参考模型写在模式一级（`autonomous_mode --> human_mode : human_steering_cmd`）。⚠️ 模式级锚定不是过度指定：同 NL 组 6 个作者里 `0000`(:13)、`0030`(:16)、`0040`(:12)、`0050`(:17) 四个都把该边挂在模式一级——对照 `N-ANCHOR` 的判例 `0022-2`，那里同组 6 个作者无一如此。

**`0010-2` 台账未覆盖，逐条核对**：该 pair 台账 5 条无一覆盖——`EIS-0010-02` 是层次缺失，`EIS-0010-04` 只覆盖 `AutonomousFinal` 是绝对吸收态（其 statement 反而把 human steering cmd 与 brake pressed 拆成两条独立边这件事记为优点，说明台账问的是「三条件是否拆开」而非「作用域是否覆盖整个模式」），`EIS-0010-01/03/05` 分别是 Power On 误置、Power Off 不终止、自动驾驶侧不消费 Power Off。⚠️ 与 `EIS-0010-04` 在 `AutonomousFinal` 这一半上有交叠，论文若引本条，净增量应只记 `Autonomous` 与 `AutonomousIdle` 那一半。

⚠️ **两条都不稳定**：`0014-4` 出现在 6 格中的 2 格，`0010-2` 出现在 3 格（三轮的 claude），见 [unexpected_tables.md](./unexpected_tables.md) 表 4；补入台账会使 `hit@all` 下降，不是「分母不变故无影响」。

### 三之二、越界的两个家族

**`0056-1`（`OOS-REGION`）** —— 决定性事实在作者源 `llms_emp_feedback_final_0056/stm0.puml:10`，那是一个正交区分隔符 `--`：

```
state SearchState {
[*] --> Area1 ; Area1 --> Area2 ; Area2 --> Area3 ; Area3 --> Area1
--                                          ← 正交区分隔符
[*] --> NoIntercept ; NoIntercept --> Intercepted : Intercepted ; ...
}
```

`model.fcstm:9` 的 `[PlantUML concurrent region 0/1]` 标注逐字确认两区划分。**NL 2 的 "three different state areas" 由 region 0 的三个 Area 兑现，义务在作者源上已满足**；`cardinality=5≠3` 只在 R4.5 把两区拍平成兄弟、跨区求和之后才出现。

由此确立的边界规则（**R-REGION**）：

> **含正交区的制品上，`cardinality` 主张在 $M$ 内成立，当且仅当该违规在「区感知读法」下依然存活** —— 即不存在任何区分配使 NL 的计数 / 枚举义务被满足。若存在一个区恰好满足该义务，违规只在把区拍平成兄弟之后才出现，则该主张落在 $M$ 之外。

**这条规则可证伪，且先于本裁定存在**（由 `0007-3` 的第二段判据、`EIS-0046-02` 的 scope 改写、`EIS-0043-02` 的边界裁定三处共同划定）。全语料含区 pair 逐一验算，零例外，且在四处给出**对方法不利**的保留（⚠️ 下表是 R-REGION 的规则验算表，机械可复算，不是本桶的交叉表）：

| pair | `--` 数 | 盈余来源 | 区感知读法下是否仍违规 | 裁定 |
| :-- | --: | :-- | :-- | :-- |
| 0037 | **0** | 单区复合态，7 个子态就是作者源的数 | 是（多出的三个是死端叶） | 保留，并入 `EIS-0037-01` |
| 0002 | 2 | `puml:5` 游离的 `InitialState`，与区无关 | 是 | 保留，`EIS-0002-03` |
| 0013 | 3 | NL 未枚举的克隆态 `PumpStateA/B` | 是 | 保留，`EIS-0013-01` |
| 0007-1 | 3 | 顶层 `InitialState` + 臆造子树，纯层次 | 是 | 保留在桶内 |
| 0007-3 | 3 | 区→子态换算 | **否**（本已三个非空区） | 越界 |
| **0056-1** | 1 | 区 1 被拍平 | **否**（region 0 恰为三个 Area） | **越界** |

⚠️ **风险披露（必须与结论同批出现，不得放脚注）**：这条规则把一条 **4/6 格稳定复现**的多报移出了统计，形式上有「迁就结果」的嫌疑。两条抗辩：(1) 判据由 `0007-3` 等三处**先于本裁定**确立，非为 0056 现造；(2) 可机械复算（`grep -cE "^[[:space:]]*--[[:space:]]*$" stm0.puml`），全语料零例外，且含 4 处对方法不利的保留。

不选假阳性的理由：本仓库对假阳性的定义是「断言所指元素其实存在，主张与制品相反」，而 5 个直接子态在拍平后的制品上**客观为真**，事实不假，假的是把它读成缺陷的资格。把事实为真、义务越界的记录塞进假阳性，会让「存在性谓词的误触发几乎全是编译债务」这个论证失真。

**该过度规约的可断言后果已由 `EIS-0056-01`（`guard_distinguishable`）承担**，再计一条等于用第二件仪器把同一个缺陷数两遍，违反台账的 `counting_conventions.homogeneity_group`。

**`0023`（`OOS-FLATTEN`，6 条目 / 1 去重）** —— 作者用两个 `--` 写了三个并发区，$M$ 无正交区故被展平成三条竞争初始边，「区间零迁移」是**展平之后**才出现的。判据不靠推断：`manual_review/0023-review.json` 判 `correct`——「与参考模型逐字同构……NL 1/2/3/4/5 的全部内容都被满足」，另一条 diff 自带 `out_of_scope: concurrency`；**参考模型同样零事件零迁移**，根源是 NL06 五句话通篇未命名任何触发条件，不可归因于被测模型。

### 三之三、内容已被台账承载的 14 条

明细与 `disposition` 见 [unexpected_verdicts/ledger_accounted.jsonl](./unexpected_verdicts/ledger_accounted.jsonl)，分类见 [unexpected_merged.md §二](./unexpected_merged.md)。

其中 `0036-8` 是同一缺陷换谓词（`terminates` → `persists_until`；`0006-2` 走的是 `state_declared`，同样换了说法）——匹配器按谓词签名归并，换谓词就漏配，这是**匹配环节**的问题，不是台账漏记。

## 四、非发现类 277 条目的可改进性排序

条目 / 去重数一律以 [unexpected_tables.md](./unexpected_tables.md) 表 2 为准，本节不复述。按可改进性排序：

1. **表示债务被当成模型缺陷（134 条目 / 29 去重，按条目最大的一块）** —— 断言锚在下沉后的形态上。根治办法有二：让断言阶段能看到 `stm0.puml`；或在谓词层区分「作者未表达」与「下沉未保留」。前者更彻底，后者改动更小。
2. **要求把复合条件 / 散文析取拆成独立元素（`N-SPLIT` + `N-SPLIT-PROSE`，49 条目 / 15 去重）** —— ⚠️ **这一支不是采样噪声**：`N-SPLIT` 的 ≥4 格簇数是全部子类里最高的，说明它是系统性读法偏差，属 prompt 侧可收敛项。`N-SPLIT-PROSE` 的条目/去重比 8.00 很高（全库最高的正是它），成因明确：NL 只给散文、不给标识符，报告者必须自己造名，**造名空间无上界**。
3. **语境措辞与承载相位被过度指定（`N-CTX` + `N-FORM`，33 条目 / 20 去重）** —— 属 prompt 侧可收敛：NL 的统称词、语境状语、`indicating that…` / `where the … is …` 式语义注解都不构成元素义务。
4. **范畴错置（`N-KIND`，8 条目 / 7 去重）** —— 属谓词选择问题：`dist_to_front` 是被比较的量不是信号，`Send` 是输出动作不是输入事件。
5. **测量链侧待修项** —— 已登记于 [defects_registered.md](../../../discover_matrix/docs/findings/predicates/defects_registered.md)，本桶内涉及 P-1（`0046-8`）、P-2 / P-3（`0044-4`）、P-4（`0054-5` 与 `0026-3`）。⚠️ 与「谓词词表保持不动」不冲突，两者范围不同：**冻结的是谓词词表**（不增删谓词、不改现有谓词族的语义），这些是**求值侧**的缺陷，另案登记于 [defects_registered.md](../../../discover_matrix/docs/findings/predicates/defects_registered.md)，按「已实施 / 未实施」两栏维护，不通过改 prompt 绕过。

## 五、两条裁定规则

### R-CONJ：合取融合按变量框架计，不按事件框架计

判据不是「行为是否等价」，而是**这条断言若被采纳去修，修出来的东西对不对**：

- NL 用 `or` 并列备选触发（NL 12）→ 融合后无法只凭其一激活 → 拆开是正确修法 → 事件框架成立 → 落表示债务（`D1`）。
- NL 用 `and` 连接条件（NL 13）→ 若拆成三个独立事件，任一个都能触发 → **把 AND 变成了 OR，比现状更违反 NL** → 事件框架指向错误修法 → 落无 NL 依据（`N-SPLIT`）。
- 同一处的真实缺口按 $M$ 的 `V` 计（NL 称之为 condition），**同一缺口只计一次**。

这条规则由 NL 自己的措辞推出（称 condition 就归 `V`，称 alternative trigger 就归 `E`），不由「哪种算法更方便」决定。不写死它，同一份 NL 下六个制品的同形簇会按判定组分裂——而作者守卫写法六份完全同形。

### 路径清单不含动作，涉及 `A` 元素的主张必须回读原件

证据包的路径清单只列 `state` / `event` / `variable`，**不列 action**。据此判「模型未声明 X」在三份 train-control 制品（0004 / 0044 / 0054，同一份 NL）上系统性出错：`Send`（`0004/model.fcstm:18`、`0044/model.fcstm:15`、`0054/model.fcstm:14` 的 `during abstract Send`）、`SendObstacleDetected`（`0004/model.fcstm:33`、`0054/model.fcstm:31`）、`EmergencyStopSendObstacleDetected`（`0044/model.fcstm:32`）**全部以状态局部的 `enter` / `during abstract` 声明真实存在**，只是不出现在路径清单里。这类簇落假阳性的 `FP-K`（类别槽差：承载者以 `action` 存在，断言按 `event` 索要）。

## 六、可复算路径

```bash
cd project_1_llm_state_machine_modeling/paper_stm_issue_discover/selected_seed_examples
grep -h "^\s*def " */model.fcstm | sort | uniq -c          # → 33× R45RouteToken，无作者变量
# ⚠️ 债务码必须按【制品数】数——每码在两个数组各列一次，uniq -c 会得到 2 倍
for c in $(grep -ho 'R45\.DEBT\.[a-z_]*' */fcstm_meta.json | sort -u); do
  echo "$(grep -l "$c" */fcstm_meta.json | wc -l)/60  $c"; done | sort -rn
sed -n '33p' llms_emp_feedback_final_0029/stm0.puml         # → 合法析取守卫
sed -n '26p' llms_emp_feedback_final_0014/stm0.puml         # → EmergencyStopping: Obstacle Detected
grep -cE "^[[:space:]]*--[[:space:]]*$" llms_emp_feedback_final_0056/stm0.puml   # → 1，R-REGION
```

桶内统计的重建：改裁定**只能改** `unexpected_verdicts/G*.jsonl`，然后跑 `python3 ../rebuild_unexpected.py`——它会一并重建 [unexpected_tables.md](./unexpected_tables.md) 与全部派生 tsv，并在字段缺失、`merge_key` 跨 `verdict` / `subclass` / `pair` 时拒绝执行。

台账权威源是 [manual_review/expected_issue_set.json](../../../discover_matrix/ledger_v2/provenance/expected_issue_set.json)（126 条）；同目录 `expected_issues_reconstructed.json` 只覆盖 4 个 pair，[hit_criterion.md](../../../discover_matrix/docs/protocol/hit_criterion.md) §7 明令禁止用它算命中。

## 七、本裁定自身的可靠性边界

1. **`grep` 只能定位不能裁定。** 按 `front_distance` 检索 0010 的作者源会得出「作者源亦无、可能真缺陷」，而作者实写 `Front Distance > 10`（`stm0.puml:9,12,18`，大写、有空格）。**必须逐行读原文。** 本文件所有作者源判据都标了行号，可逐条复核。
2. **`D1` / `D2` 分界有一处脆弱点。** `dist_to_front<15` 在本批 pair 里出现两次，清洗名极其形近（`dist_to_front_15_highway` vs `dist_to_front_15_extra_lane_true`），**不可从簇自身文本判定**，必须回读 `stm0.puml` 那一行并确认它对应哪句 NL。受影响 ≤4 条（占表示债务 134 条目的 3.0%），判据见 [unexpected_taxonomy.md](../../../discover_matrix/docs/protocol/unexpected_taxonomy.md)。
3. **不设「待定」。** 证据不足不构成一个裁定类别——取不到证据就去取：静态读不动时直接实跑 `SimulationAPI` 投喂事件看机器动没动（`0044-4`），或用 `FBMCQAPI` 做 bound 扫描取反例 frames（`0044-2`）。⚠️ `FBMCQAPI` 在结构最破的制品上恰恰不可用，遇 `UnsupportedEvidence` 的下一跳按序是「降 bound → 转 `SimulationAPI` → 静态封裁」。
4. **判定层本身是独立误差源，且是单向的。** 裁定越严，越倾向把真发现判成非发现。本文件的每一条非发现裁定都留了可机械复算的作者源行号或命令，正是为了让这个方向的误差可被外部翻案。

## 八、相对上一版的改动


- 全部交叉表统一归口到 [unexpected_tables.md](./unexpected_tables.md)（由 `G*.jsonl` 机器生成），本文件不再保存副本。**理由**：副本与真源分岔过一次，代价是同一目录内两份文件对净增量给出互斥的答案。
- 分母与子类体系切换为清洗后的口径：桶内 288 条目 / 124 去重，另 14 条移入 `ledger_accounted.jsonl`、2 条移入 `not_produced.jsonl`。**理由**：「内容是否已被台账承载」回答的是「该不该在桶里」，与五类回答的「这条产出是什么」不是同一个问题，混在一起会让分母虚高。
- 子类改用 `rebuild_unexpected.py` 校验的 `D*` / `N-*` / `FP-*` / `OOS-*` / `V1` 体系。**理由**：旧体系按谓词族与判定组混切，同形簇会分裂到不同子类；新体系按「丢失/多要的是哪一条区分」切，并由工具层三道硬门（`merge_key` / `merge_reason` / `subclass` 缺失即拒绝重建）保证可审计。
- §三之三 标题与本节的「移入 `ledger_accounted.jsonl` 的条数」按真源 `ledger_accounted.jsonl` 实测行数改写。**理由**：真源是该 jsonl，本文件是叙述性文档；v46r 整块替换改动过该文件的成员集合，而这两处散文未随之更新，与本文件 §开头已经写对的闭合式 `288 + 14 + 2 = 304` 自相矛盾。
- §三 的标题与 §二（3）的真漏记条数改按真源 `final_rootcause.tsv`（两行）叙述，并按 `G9.jsonl` 的 `fact` / `nl` / `note` 补入 `0010-2` 的根因行与逐条判据。**理由**：v46r 新增了 `0010-2`，这两处散文未随之更新，与本文件 §一「净增量是 2 条」自相矛盾。
- §二（3）的 6/6 全满格个数经回真源核对后改为**三个**：`cluster_index.tsv` 里 `cells_of_6 == 6` 的簇是 `0000-2` / `0010-1` / `0050-1`，与 [unexpected_tables.md](./unexpected_tables.md) 表 4「6 格」一列的合计 3 一致；三者仍全部是表示债务，故该句的论点不变，只改数量。
