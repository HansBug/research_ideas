# 意外发现裁定分类学：六类的定义、判定标准与典型例子

**未匹配到台账的产出，必须落入且只落入下面六类之一。没有第七类，也不设「待定」。**

「待定」曾短暂存在过 5 条，全部因为判定者手里的证据包不含迁移表 / 动作块 / 比较符。
那不是判据不足，是**取证不足**——回读 `model.fcstm` 与 `stm0.puml` 原件后全部可裁。
**证据不足不构成一个裁定类别**；取不到证据就去取，取到了就裁。

本文件是裁定规范；实测分布见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md)，
逐簇判据见 [V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)。

## 〇、判定前必须取齐的证据

⚠️ **顺序不能颠倒，颠倒会系统性判错**（v46 八个判定组里七组栽在第 2 步没做）：

| # | 材料 | 回答什么 | 不看的后果 |
| --: | :-- | :-- | :-- |
| 1 | `model.fcstm` **全文** | 事实在编译产物上成不成立 | 只看路径清单会漏掉 `action`——清单不列动作，`Send` 因此被误判为不存在 |
| 2 | `stm0.puml` **作者原件** | 作者到底写没写 | **把编译损失当成建模缺陷**，v46 最大的一类误判（123/293） |
| 3 | `fcstm_meta.json` 的 `source_static_reason_codes` | 编译器认不认这笔损失 | 无法区分「作者没写」与「编译没留」 |
| 4 | `nl.txt` **逐句** | NL 到底要求什么 | 把统称词、语境状语、语义注解当成元素义务 |
| 5 | `manual_review/expected_issue_set.json` | 台账记没记 | 把已记缺陷当成新发现，分子虚高 |
| 6 | 同 NL 组的其他 pair（`md5sum */nl.txt` 分组） | 参考意图是什么 | 把参考读法当成异类，或反之 |

⚠️ **`grep` 只能定位，不能裁定。** 实测反例：按 `front_distance` 检索 0010 的作者源得出
「作者源亦无」，作者实写 `Front Distance > 10`（大写、有空格）。**必须逐行读原文。**

## 一、判定流程（按序短路，先命中先判）

```
事实在 model.fcstm 上成立吗？
├─ 否（元素其实存在，哪怕名字不同字面 / 以 action 形式存在） ──▶ ❌ FALSE_POSITIVE
└─ 是
   └─ 主张依赖正交并发 / 不变式 / 时钟吗？
      ├─ 是 ──▶ 🚫 OUT_OF_SCOPE
      └─ 否
         └─ 作者在 stm0.puml 里已逐字表达该义务吗？
            ├─ 是（且 meta 有对应债务码） ──▶ ⚙️ REPRESENTATION_DEBT
            └─ 否
               └─ NL 真的要求这件事吗？
                  ├─ 否 ──▶ 📄 NO_NL_BASIS
                  └─ 是
                     └─ 台账已有记录覆盖同一缺陷吗？
                        ├─ 是 ──▶ 🔗 MERGE_INTO_LEDGER
                        └─ 否 ──▶ ✅ VALID_UNRECORDED
```

**短路顺序是有意的**：先判事实、再判边界、再判归属（作者 vs 编译）、最后才判 NL 与台账。
颠倒顺序会把编译债务混进 NL 判断，而那正是 v46 的主要误判路径。

---

## ✅ 1. `VALID_UNRECORDED` —— 真实的台账漏记

### 定义
事实在编译产物上为真，**且作者源本身就缺该元素**，**且 NL 有明确依据**，**且台账未记**。
这是**唯一**应当补进台账的类别，也是方法相对台账的净增量。

### 判定标准（四条全中）
1. 事实在 `model.fcstm` 上客观为真（含 action，须读全文）。
2. `stm0.puml` 里作者**没有**以任何形式表达该义务（不只是名字不同，是根本没写）。
3. `nl.txt` 有逐字依据，且该依据**不是**统称词 / 语境状语 / 语义注解。
4. `expected_issue_set.json` 中无任何记录覆盖同一缺陷（含换谓词、换说法的情形）。

### 加强判据（推荐做，能显著降低误判）
**查同 NL 组的其他 pair**：若多数作者把这件事写对了，说明它是该 NL 的通行读法而非过度指定。

### 典型例子

**`0017-1`（8 簇同源，该 pair 台账 0 条）**
> 事实：制品事件只有 `collision_detected` 与 `Collision_avoided`，NL 2 点名的三种具体检测一个都没有。
> 作者源 `stm0.puml:4,9,14` 三处都只写泛化的 `collision detected`——**作者本人塌缩了三种刺激**。
> NL：NL 2 逐字并列「a possible frontend collision, rear-end collision **or** collision with pedestrian is detected」。
> 加强判据：同一份 NL（md5 `a53ac335`）的 6 个作者里 **4 个**把三者写成可分刺激
> （0007、0037、0057 分立三事件，0027 显式析取）→ 可分是通行读法。

**`0023-7`（6 簇同源，台账 0 条）**
> 事实：`PumpControl` 内三个子状态之间**零迁移**，模型连一个 `event` 都没声明，无从触发子态切换。
> NL：NL 4 / NL 5 均以「can transition to」要求运行期可切换。
> ⚠️ 措辞刻意写成 **Tr/E 层**（`E=∅`、`V=∅`、非初始迁移数 = 0）。
> 若写成「三个并发区的默认入口」就依赖区语义，会按 R-REGION 落入 `OUT_OF_SCOPE`。

**`0014-4`（同族漏记）**
> 事实：`EmergencyStopping` 内无任何 `enter`/`during` 动作，NL 要求发出的信号被吞进状态名描述串。
> 作者源 `stm0.puml:26` 写 `EmergencyStopping: Obstacle Detected`——PlantUML **描述行**，不是动作。
> 对照 0054:18 作者写 `do/Send Obstacle Detected`、0004 写 `during abstract SendObstacleDetected`
> → 该输出动作在 M 内可表达且是参考意图，**作者用错了语法**。
> 台账：已记同族 `EIS-0014-03`（Emergency Stop）与 `EIS-0014-04`（Approaching 的 Send），
> 但前者 `nl_evidence` 只引「Emergency Stop」、后者 scope 是 `InMotion.Approaching`，**均不覆盖此条**。

---

## 🔗 2. `MERGE_INTO_LEDGER` —— 台账已记，只是没匹配上

### 定义
与 `VALID_UNRECORDED` 的前三条完全相同，**只差第四条**：台账其实已有一条记录覆盖同一缺陷，
但因为**换了谓词**或**换了说法**，按签名归并的匹配器没对上。

### 判定标准
1. 前三条同 `VALID_UNRECORDED`。
2. 台账中存在一条记录，其 `statement` / `nl_evidence` / `reference_side` **指向同一处缺陷**
   ——判据是「修复它能否同时消除本条」，不是「谓词名是否相同」。

### ⚠️ 这不是台账的问题，是匹配环节的问题
把它计入新发现会让分子虚高，违反台账的 `counting_conventions.homogeneity_group`。

### 典型例子

**`0036-8` —— 换谓词**
> 事实：制品无任何 mission-complete 事件，也无顶层终态。
> 台账 `EIS-0036-02` 用 `terminates` 记的正是这件事；本条用 `persists_until` 表达。
> **同一缺陷、两个谓词，签名匹配器必然漏配。**

**`0050-2/3/4` —— 换签名类别**
> 事实：`human_steering_cmd` 只作融合事件名的子串。
> 台账 `EIS-0050-01` 已记该接管条件融合，但本条签名被标为 `state_declared` 而非 `event_declared`，故未匹配。

**`0035-1/2` —— 台账 `nl_evidence` 已逐字覆盖**
> 事实：`ReadytoCook` 无 `during` 动作、`Cooking` 无 `entry` 动作，全模型零动作零变量。
> 台账 `EIS-0035-04`（`element_of_M=A`）的 `nl_evidence` **逐字引用了 NL 第 5、7 句**
> （"cooking time is displayed and updated"、"the timer starts"），覆盖面明确包含这两处。

---

## ⚙️ 3. `REPRESENTATION_DEBT` —— 我们自己编译链的信息损失

### 定义
事实在编译产物上为真，**但作者在 `stm0.puml` 里已逐字表达该义务**，失真发生在
R4.5 的 PlantUML → FCSTM 有损编译。**不是模型缺陷。**

完整论述见 [REPRESENTATION_DEBT.md](./REPRESENTATION_DEBT.md)。

### 判定标准（三条全中）
1. 事实在 `model.fcstm` 上客观为真。
2. 该义务在 `stm0.puml` 上**已被作者逐字表达**（⚠️ 需人工逐行读，词法检索不可靠）。
3. `fcstm_meta.json` → `source_static_reason_codes` 有对应债务码
   （⚠️ 仅在自申报编译器下可用；每码在两个数组各列一次，数制品数请用 `grep -l ... | wc -l`）。

### 与「真漏记」的分界线
**只看第 2 条**：0036 的 `/ UAV Count Decreased` 作者写了 → 债务；
0006 的作者源里**连递减文本都没有** → 真缺陷。

### 四个子类

**`D2` 析取守卫被压成单一事件名（70 类，最大一块）** —— 例 `0029-1`
> 作者源 `stm0.puml:33` 写的是一条**完全合法的析取守卫**：
> `pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode`
> NL 12 的四个替代激活源**一个不缺**。下沉后压成一个巨型事件名，于是
> 「独立的 `pedestrian_detected` 不存在」——对 IR 字字属实，对作者完全冤枉。

**`D1` 守卫文本未成为变量声明（42 类）** —— 例 `0000-1`
> **PlantUML 没有变量声明语法**，量只能写进守卫文本。作者写 `front_distance > 10`，
> 下沉为 `event front_distance_10 named 'front_distance > 10'`。
> 后果：`variable_declared` 在全语料 **60 份制品上恒为 False**（作者变量 0/60），不携带判别信息。

**`D3` `trigger / effect` 标签未被切分（9 类）** —— 例 `0016-4`
> 作者写 `Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count`。
> UML 记法里 `/` 前是触发、后是效果，**作者分得清清楚楚**。下沉未切分 `/`，
> 产出 `event Attack_Finished_Decrease_UAV_swarm_count`。

**`D4` 注入伪态 / 区语义偏移（2 类）**
> 作者写了合法的区内 `[*]`，R4.5 另注入 `UnspecifiedInitial`（债务码 `missing_explicit_initial`）。

---

## 📄 4. `NO_NL_BASIS` —— 事实为真，但 NL 不要求

### 定义
事实在编译产物上为真，作者源确实没写，**但 NL 并不要求这件事**。属过度规定。

### 判定标准
1. 事实为真（否则是 `FALSE_POSITIVE`）。
2. 回到 `nl.txt` 逐句读，确认 NL **没有**提出该义务。
3. ⚠️ **重点排查四种误读**（见下六个子类）。

### 六个子类

**`N1` 命名字面主义（27 类）** —— 例 `0016-3`
> 把 NL 的**统称词 / 语境状语**当成必须存在的同名元素。
> 「During flight, if task assignment information is received」——`During flight` 是**状语背景**，
> 整台机器全程在飞行，NL 中不存在与之对立的非飞行上下文。要求一个名为 `Flight` 的状态属过度规定。
> 同类：`user_actions`（"based on user actions"）、`region`（"three region"）、`collision_avoidance_controls`。

**`N2` 相位过度指定（20 类）** —— 例 `0033-2`
> NL 只在**解释状态含义**，却被读成 `during`/`entry` 动作义务。
> 「where the pump is activated or controlled」是对子状态含义的说明，未规定必须以 `during` 相位实现；
> 模型另行声明了 `Activate_Pump` / `Pump_Deactivated` 承载该行为。
> 识别信号：NL 用 `indicating that…` / `where the … is …` 这类同位语或定语从句。

**`N4` 合取项被要求拆成独立事件（19 类，规则 R-CONJ）** —— 例 `0049-11`
> 判据不是「行为是否等价」，而是**这条断言若被采纳去修，修出来的对不对**：
> - NL 用 `or` 并列备选触发 → 融合后无法只凭其一激活 → **拆开是正确修法** → 成立。
> - NL 用 `and` 连接条件 → 拆成独立事件后任一个都能触发 → **把 AND 变成 OR，比现状更违反 NL**。
>
> 同一处的真实缺口按 M 的 `V` 计（NL 称之为 condition），**同一缺口只计一次**。

**`N3` 范畴错置（19 类）**
> 把变量当事件、把动作当事件。`dist_to_front` 是被比较的**量**不是信号；
> `Send` 是**输出动作**不是输入事件。

**`N0` 谓词操作化产生的义务（4 类）**
> 义务来自**谓词被操作化的方式**而非 NL。`0054-5` 是构造性不可满足——
> NL 2/10 恰恰**许可**该迁移，谓词却禁止它。按 [CLAUDE.md](../../../CLAUDE.md) §13 属
> 「多道门交集为空」类缺陷，**另案登记**。
> ⚠️ 登记 ≠ 本轮修改：冻结的是**谓词词表**，`N0` 是**求值侧**的约束交集缺陷，两者范围不同。

**`N5` 断言锚在不存在的元素上（4 类）** —— 例 `0057-2`
> 制品里根本不存在名为 `Inactive` 的状态，因此「`Inactive --X--> CA` 这条边缺失」是
> **断言自造前提导致的空洞真**。NL 也未点名任何 `Inactive` 前置状态。
> 识别信号：断言的 scope 或 source 绑定到一个模型里查不到的路径。

---

## ❌ 5. `FALSE_POSITIVE` —— 元素其实存在

### 定义
断言所指的元素**其实存在**（哪怕名字不同字面、或以 `action` 形式存在），主张与制品相反。

### 判定标准
**事实为假**——这是与 `NO_NL_BASIS` 的唯一分界：事实为真 → `NO_NL_BASIS`；事实为假 → 本类。

⛔ **不要把「事实为真但义务越界 / 已被政策许可」塞进本类。** 那会污染本类的语义，
而多报口径的成分划分依赖它。

### 四个子类

**`F2` 命名变体：元素已在，仅字面不同（21 类）** —— 例 `0057-6` / `0032-3`
> `0057-6`：断言要求 `possible_frontend_collision`，制品已声明 `Frontend_collision_detected`
> ——正是 NL 2 对应的独立检测事件，只是字面名不同。
> `0032-3`：断言要求 `accelerating`，制品已声明 `event Accelerate`；NL 3 用 `like` 举例，未规定精确拼写。
> ⚠️ 同一主张在不同 pair 上可能一真一假：0017 只有泛化 `collision_detected`（真漏记），
> 0057 已分立三事件（假阳性）。**命名类断言必须逐 pair 核对，不能按 NL 归并结论。**

**`F4` 作者源已表达，主张与制品相反（5 类）**
> 与 `REPRESENTATION_DEBT` 的差别：那类是「IR 上确实没有」，本类是「rationale 声称没有但其实有」。

**`F1` 元素以 `action` 存在，路径清单看不见（4 类）** —— 例 `0004-1`
> 制品有 `state Approaching { during abstract Send; }`——`Send` 已作为**动作**声明。
> 路径清单只列状态与事件、**不列动作**，据此判「未声明」必然出错。
> ⚠️ v46 因此翻转 5 条，其中 `0054-3` 由「真漏记」翻成假阳性。**涉及 A 元素的主张必须读原件全文。**

**`F3` 谓词锚点错置（1 类）**
> 触发只能锚在源态，断言却锚到了目标态。

---

## 🚫 6. `OUT_OF_SCOPE` —— 在 M 边界外

### 定义
主张依赖**正交区并发语义**、**不变式**或**时钟**，落在 paper1 建模对象
`M = (S, E, V, Tr, A)` 之外。

### 判定标准
命中任意一条即越界：
1. 谓词族是 `invariant`，或主张要求多个状态**同时**保持活跃。
2. 主张的内容是「某复合态下恰好有 N 个**区**」。
3. 主张涉及时钟变量或状态不变式。
4. **R-REGION**：含正交区的制品上，`cardinality` 类主张在 M 内成立
   **当且仅当该违规在「区感知读法」下依然存活**——即不存在任何区分配使 NL 的计数 / 枚举义务被满足。
   若存在一个区恰好满足该义务，违规只在把区拍平成兄弟之后才出现，则越界。

**R-REGION 的机械判据**：`grep -cE "^[[:space:]]*--[[:space:]]*$" stm0.puml` 查分隔符数，
再看盈余是不是区拍平造成的。

### ⚠️ 边界是双向的
[CLAUDE.md](../../../CLAUDE.md) 明确：**不得**把并发 / 时间类问题记为方法未能检出，
也**不得**反过来声称这些模型没有并发 / 时间问题。论文的正确姿态是**双向缄默**。

### 典型例子

**`0027-6` —— invariant + 并发保持（双重越界）**
> 断言以 `invariant + active('ActiveState.BrakeControlState')` 等形式要求三个控制态**同时活跃**。
> 谓词族与并发语义两项都在建模对象之外。

**`0007-3` —— 区数量义务**
> 「`CollisionAvoidance` 下恰好三个区」。且按区计数制品**本已是三个非空区**，
> 「不是三个」只在把区换算成子状态时才成立。

**`0056-1` —— R-REGION 的判例**
> 作者源 `stm0.puml:10` 是正交区分隔符 `--`，`SearchState` 实为两区：
> `region0={Area1,Area2,Area3}`、`region1={NoIntercept,Intercepted}`。
> **NL 2 的「three different state areas」由 region 0 的三个 Area 兑现，义务在作者源上已满足**；
> `cardinality=5≠3` 只在 R4.5 拍平、跨区求和后才出现。

### R-REGION 的可证伪性（必须与结论同批披露）
该规则在**四处给出对方法不利的保留**，说明它不是为某一条现造的：

| pair | `--` 数 | 盈余来源 | 区感知读法下仍违规 | 裁定 |
| :-- | --: | :-- | :-- | :-- |
| 0037 | **0** | 单区复合态，7 个子态就是作者源的数 | 是 | **保留在 M 内** |
| 0002 | 2 | 游离的 `InitialState`，与区无关 | 是 | **保留在 M 内** |
| 0013 | 3 | NL 未枚举的克隆态 | 是 | **保留在 M 内** |
| 0007-1 | 3 | 顶层 `InitialState` + 臆造子树，纯层次 | 是 | **保留在 M 内** |
| 0007-3 | 3 | 区→子态换算 | 否 | 越界 |
| 0056-1 | 1 | 区 1 被拍平 | 否 | 越界 |

---

## 七、常见误判速查

| 症状 | 多半应判 | 为什么 |
| :-- | :-- | :-- |
| 「模型未声明信号 X」而 X 是输出动作 | `FALSE_POSITIVE` | 路径清单不列 `action`，须读原件全文 |
| 「量 X 未声明为变量」 | `REPRESENTATION_DEBT` | PlantUML 无变量声明语法，作者变量 0/60 |
| 「融合事件应拆成 N 个独立事件」 | 先查作者源 | 作者写了析取守卫 → 债务；作者自己塌缩了 → 真漏记 |
| 「应存在名为 `<NL 里的统称词>` 的状态」 | `NO_NL_BASIS` | 命名字面主义 |
| 「状态 X 应有 `during` 动作」 | `NO_NL_BASIS` | NL 的 `indicating that…` 是语义注解不是动作义务 |
| 「某复合态下应恰好三个区」 | `OUT_OF_SCOPE` | 区数量义务在 M 外 |
| 断言的 scope 在模型里查不到 | `NO_NL_BASIS`（`N5`） | 自造前提导致的空洞真 |
| 台账里有条记录讲的好像是同一件事 | `MERGE_INTO_LEDGER` | 判据是「修复它能否同时消除本条」，不是谓词名 |
