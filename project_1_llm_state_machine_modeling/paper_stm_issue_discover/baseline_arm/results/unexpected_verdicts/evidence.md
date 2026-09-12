# X1 多报侧逐簇判据（全 212 条）

⚠️ **本文件由 `unexpected_verdicts/X1-*.jsonl` 生成**（[../../analysis/rebuild_unexpected_x1.py](../../analysis/rebuild_unexpected_x1.py)），jsonl 是真源。改裁定请改 jsonl 再跑重建。

⭐ **判事实的基准是作者源 `stm0.puml`**（X1 的输入 `plantuml.puml` 与它逐字节相同），⛔ 不是编译产物 `model.fcstm`。


## pair 0000 — 3 簇　📄 无 NL 依据×2　❌ 假阳性×1

**0000-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 6/6 格 ｜ X1-J1

- **主张**：AutonomousMode 被写成内联复合状态，NL 第2句要求它以 submachine state 呈现。
- **事实**：事实成立。stm0.puml:7-10 逐字为 `state AutonomousMode {` / `[*] --> AutoNavigating` / `AutoNavigating --> AutoFinal : Condition Met` / `}`——确为内联复合状态，未使用任何子机引用语法。但 NL 的实质结构义务（该态含子态）已被满足：AutoNavigating（:8）与 AutoFinal（:9）就是它的子态。
- **NL**：NL S2 逐字：'The autonomous mode has sub-states and is represented by a sub machine state.' 逐字依据确实存在，但它给出的是结构描述（有子态）与一个 UML 图元复用记法名。submachine state 与 composite state 在 $M=(S,E,V,Tr,A)$ 内是同一个对象——M 只有层次状态，没有『子机引用』这一区分，故被指缺陷在建模对象内不可表述；把该短语读成必须使用某种 PlantUML 语法属形态过度指定。
- **去重**：`0000-复合状态写法被要求为子机状态语法` —— 六格同一主张，同指 stm0.puml:7 的 AutonomousMode 声明形态这一处争议点。
- **成员**：run1/0000-claude#1 run1/0000-gpt#2 run2/0000-claude#1 run2/0000-gpt#2 run3/0000-claude#1 run3/0000-gpt#2

**0000-2** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 5/6 格 ｜ X1-J1

- **主张**：HumanDrivingMode 用带花括号的 `state X { }` 写成复合状态壳，NL 第1句要求它是 simple state。
- **事实**：事实不成立。stm0.puml:4-5 为 `state HumanDrivingMode {` 与 `}`，花括号体内为空——零子态。UML 中复合状态的定义是至少含一个带子态的区域；空体不产生任何子态，故该状态本就是 simple state。编译产物 model.fcstm:8 亦为 `state HumanDrivingMode named "HumanDrivingMode";` 这一普通简单状态声明，无内层。所指内容（一个名为 HumanDrivingMode 的简单状态）以另一种合法 PlantUML 语法存在，被判成不存在。
- **NL**：NL S1 逐字：'The human driving mode is represented by a simple state.' 该义务在作者源上已被满足，issue 把词法上的花括号误读成语义上的复合性。
- **去重**：`0000-空花括号状态被误判为复合状态` —— 五格同一主张，同指 stm0.puml:4-5 空花括号写法这一处争议点。
- **成员**：run1/0000-claude#7 run1/0000-gpt#1 run2/0000-gpt#1 run3/0000-claude#7 run3/0000-gpt#1

**0000-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J1

- **主张**：`front_distance > 10` 被当作事件标签，应写成 `[front_distance > 10]` 形式的 guard。
- **事实**：事实成立。stm0.puml:12 逐字为 `HumanDrivingMode --> AutonomousMode : front_distance > 10`——条件文本直接作标签，未加守卫方括号。issue 自己也把它标为『属于轻微形式问题』。
- **NL**：NL S4 逐字：'when front_distance > 10, auto transport to autonomous state'。NL 只陈述条件内容，未规定它必须以守卫括号而非标签文本承载；PlantUML 迁移标签本身是不透明自由文本，加不加方括号不改变作者源所表达的内容。把 NL 的条件陈述读成一条 PlantUML 语法义务属形态过度指定。
- **去重**：`0000-条件标签被要求写成守卫括号` —— 单成员组；根因是 stm0.puml:12 那条标签的记法形态，与本 pair 另两簇（子机语法、空花括号）的争议点各不相同。
- **成员**：run2/0000-claude#6


## pair 0001 — 6 簇　📄 无 NL 依据×5　✅ 真漏记×1

**0001-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J1

- **主张**：ClampingLoseState 及 `OperationalState --> ClampingLoseState` 是 NL 完全未提及的多出状态与迁移。
- **事实**：事实成立。stm0.puml:14-15 逐字为 `OperationalState --> ClampingLoseState : Transition to Clamping Lose State` 与 `ClampingLoseState : Clamping Lose State`；nl.txt 全文无 clamping lose / 夹紧失效 的任何对应表述。
- **NL**：NL 无此义务。NL 1-3 只正面描述初始→制动→夹紧与传输失败→运行态→返回初始，从未使用『只有』『恰好』『不得』一类封闭性或排他性措辞，故 NL 的状态枚举默认不封闭，『NL 没写这个状态』不构成禁止它的出处。合式性层亦无支撑：ClampingLoseState 在作者源上确无出边（仅 :14 作目标、:15 为描述行），但本簇九条 issue 无一条说出该死端后果，只说『无规范依据』『超出规范范围』『扩大行为范围』，按 §4.2(a) 不得由判定者代为补论证。
- **去重**：`0001-NL未提及的夹紧失效状态被判为多余` —— 六格九条，或指该状态、或指那条入边、或指 OperationalState 因它而超范围，同为 stm0.puml:14-15 这一处争议点。
- **成员**：run1/0001-claude#4 run1/0001-gpt#1 run1/0001-gpt#2 run2/0001-claude#1 run2/0001-claude#2 run2/0001-gpt#1 run3/0001-claude#3 run3/0001-claude#4 run3/0001-gpt#2

**0001-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J1

- **主张**：`Signal Transmission Fails` 的源态应是 BrakingState 而非 InitialState，模型把因果顺序改了。
- **事实**：事实成立。stm0.puml:6 逐字为 `InitialState --> OperationalState : Signal Transmission Fails`，源端确是 InitialState。
- **NL**：NL 义务真实存在但未指定该位置。NL S2 逐字：'When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state.' 两个分句是同一次信号接收的两种结局，NL 未指定失败分支的源态；把它读成必须挂在 BrakingState 上是把义务钉死在 NL 未指定的位置。反证：按该读法修好后，只有先进入 BrakingState 才能发现传输失败，与前一分句『收到信号即进入制动态』的并列结构冲突。
- **去重**：`0001-传输失败分支被钉在NL未指定的源态上` —— 与 0001-3 同为一处根因的正反两面（一条说这条边挂错了源，一条说缺了 BrakingState 出发的那条边），指向 stm0.puml:6 同一处争议，故合并计 1。
- **成员**：run1/0001-claude#1 run2/0001-claude#3 run3/0001-claude#1

**0001-3** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J1

- **主张**：缺少 `BrakingState --> OperationalState` 的迁移。
- **事实**：事实成立。stm0.puml 中 BrakingState 的出边只有 :8 `BrakingState --> ClampingState` 与 :12 `BrakingState --> InitialState`，确无到 OperationalState 的边。
- **NL**：NL 义务真实存在但未指定该位置，理由同 0001-2：NL S2 的 'If the signal transmission fails, it proceeds to the operational state' 未给出源态；该缺口已由 0001-2 以『边挂错源』的框架承载，本簇是同一缺口的另一种框架，按流程④与 0001-2 共用同一 merge_key 只计一次。
- **去重**：`0001-传输失败分支被钉在NL未指定的源态上` —— 同上：与 0001-2 是同一处根因的两种表述（多了一条 vs 少了一条），合并计 1。
- **成员**：run1/0001-claude#2

**0001-4** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 4/6 格 ｜ X1-J1

- **主张**：`BrakingState --> InitialState : Signal Feedback Sent` 是 NL 未描述的多余回边——NL 的反馈返回只属于 OperationalState，且它让制动态可绕过夹紧态。
- **事实**：事实成立。stm0.puml:12 逐字为 `BrakingState --> InitialState : Signal Feedback Sent`，与 :11 的 `OperationalState --> InitialState : Signal Feedback Sent` 同事件同目标。
- **NL**：NL 无此禁止。NL S2 末句逐字：'Once the signal feedback is sent, it returns to the initial state.'——该句无任何状态前件，是无源限定的一般陈述；报告者据叙述先后把它读成『只有 OperationalState 才可如此返回』，即把 NL 的叙述次序读成排他义务。同理 NL S3 'After entering the braking state, the system transitions to the brake caliper clamping state' 是正面要求（作者已在 :8 满足），NL 未写『只能』，故并存一条替代出边不违反它。
- **去重**：`0001-制动态的反馈回边被判为NL未授权` —— 四格五条同指 stm0.puml:12 这一条边，只是分别从『NL 未授权该源』与『可绕过夹紧态』两个角度陈述，同一处争议点。
- **成员**：run1/0001-claude#3 run2/0001-claude#4 run2/0001-gpt#2 run2/0001-gpt#3 run3/0001-claude#2

**0001-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J1

- **主张**：`BrakingState --> ClampingState` 的触发名 'Entering Clamping State' 把迁移条件与目标状态描述混为一谈，应为自动/无条件迁移。
- **事实**：事实成立。stm0.puml:8 逐字为 `BrakingState --> ClampingState : Entering Clamping State`，标签文本确实只是目标态名的复述。issue 自己定性为『属于表述层面的偏差，可视为轻微不符』。
- **NL**：NL 无此义务。NL S3 逐字：'After entering the braking state, the system transitions to the brake caliper clamping state.'——NL 既未给该迁移任何触发名，也未规定它必须是无触发的完成迁移；把 NL 对状态含义的叙述读成一条标签命名/迁移形态义务属形态过度指定。
- **去重**：`0001-无触发迁移的标签命名被判为混同` —— 单成员组；根因是 stm0.puml:8 标签文本的命名形态，与本 pair 其余四处争议点无关。
- **成员**：run1/0001-claude#5

**0001-6** ｜ ✅ 真漏记 ｜ `V2` ｜ 1/6 格 ｜ X1-J1

- **主张**：ClampingState 后没有任何后继迁移，进入夹紧态后系统无法按规格复位。
- **事实**：事实成立且属合式性缺陷。ClampingState 在 stm0.puml 全文只出现两次：:8 作为迁移目标、:9 为描述行 `ClampingState : Brake Caliper Clamping State`，无任何出边；本模型是平铺结构（无复合态、`--` 计数为 0），故不存在可下推到它的外层复合态出边（对照 0049/0059 那类被外层出边救回的情形）。编译产物 model.fcstm:10 声明 ClampingState 后同样无任何以它为源的迁移。因此 ClampingState 是一个非终态的吸收态：正常制动流程一旦走到夹紧就永远停在那里。issue 自己说出了该后果（『执行到夹紧状态后无法按规格复位』）。
- **NL**：按合式性层收录，不要求 NL 逐字依据（死端与终态真伪属形式化自身的义务，与台账 32 条 wellformedness 记录同一口径）。需注意：issue 提议的具体修法（ClampingState --> InitialState : Signal Feedback Sent）本身没有 NL 依据——NL S2 未说反馈发生在夹紧阶段；成立的是死端这一事实，不是它提议的那条边。本 pair 台账 0 条，无任何记录覆盖。
- **去重**：`0001-夹紧态无出边不可离开` —— 单成员组；根因是 stm0.puml:8-9 的 ClampingState 无出边，与 ClampingLoseState 那处（0001-1）虽同为无出边，但那一簇无任何 issue 说出死端后果、且争议点是该状态该不该存在，二者不是同一处主张。
- **成员**：run3/0001-gpt#1


## pair 0002 — 2 簇　📄 无 NL 依据×2

**0002-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J5

- **主张**：模型在三个子态内部自造了 NL 未描述的嵌套状态（RunningState / MonitoringWaterFlow / MonitoringMethaneFlow）与具名事件（Activate Pump / Deactivate Pump / Start Monitoring / Stop Monitoring）。
- **事实**：事实成立。stm0.puml:8 `[*] --> RunningState : Activate Pump`、:9 `RunningState --> [*] : Deactivate Pump`、:15-16 `[*] --> MonitoringWaterFlow : Start Monitoring` / `MonitoringWaterFlow --> [*] : Stop Monitoring`、:22-23 同形给出 MonitoringMethaneFlow 与 Start/Stop Monitoring。这些状态与事件在作者源上逐字存在，且 NL 通篇未提及其中任何一个。
- **NL**：NL 无此禁止。NL 2 只逐字给出 PumpControl 的三个直接子态「there are three main substates: PumpState, WaterState, and MethaneState」；NL 3/4/5 只解释这三个子态的含义（"where the pump is activated or controlled" / "indicating that the pump is controlling or monitoring the water flow" 等），对它们的**内部**结构一字未提，全文亦无 only / exactly / must not 一类封闭性表述。台账 EIS-0002-03 能把 InitialState 记成过度规定，靠的是 NL 2 对 **PumpControl 直接子态**的逐个点名，该计数义务不下延到 PumpState 的内部层级。按「NL 没提到它 ≠ NL 禁止它」，本簇无义务出处；本簇也未主张任何合式性后果。
- **去重**：`0002-三个子态内部结构为NL未描述的自造内容` —— 两簇指向同一处建模决定——作者自行设计了 PumpState/WaterState/MethaneState 的内部行为（stm0.puml:7-10 / 14-17 / 21-24 是同一批相邻编辑）：一簇说内部状态与事件多余，一簇说其中的完成边多余，是同一处自造内容的两个切面。
- **成员**：run1/0002-claude#4 run2/0002-claude#4 run3/0002-claude#4

**0002-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J5

- **主张**：三个子态内部各有一条 `--> [*]` 完成边，使子态可自行结束，超出 NL 范围。
- **事实**：事实成立。stm0.puml:9 `RunningState --> [*] : Deactivate Pump`、:16 `MonitoringWaterFlow --> [*] : Stop Monitoring`、:23 `MonitoringMethaneFlow --> [*] : Stop Monitoring` 三条完成边逐字存在。
- **NL**：NL 无此禁止。NL 1-5 通篇只讲进入（"can transition to"），对如何退出 PumpState / WaterState / MethaneState 一字未提，也没有任何禁止性表述。issue 自陈「规范未描述任何退出 PumpState/WaterState/MethaneState 的行为；模型让每个子状态都能返回终止伪状态，超出了规范范围」——即它自己承认依据只是「NL 没写」；且它未说出任何合式性后果（不可达 / 死端 / 非确定 / 抢占初始 / 名字碰撞），故不得按合式性层放行。
- **去重**：`0002-三个子态内部结构为NL未描述的自造内容` —— 两簇指向同一处建模决定——作者自行设计了 PumpState/WaterState/MethaneState 的内部行为（stm0.puml:7-10 / 14-17 / 21-24 是同一批相邻编辑）：一簇说内部状态与事件多余，一簇说其中的完成边多余，是同一处自造内容的两个切面。
- **成员**：run1/0002-claude#5


## pair 0003 — 5 簇　📄 无 NL 依据×5

**0003-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J1

- **主张**：Operate 内三个子态只连成单向环，缺 AcceleratingOrCruising→Idle、Braking→AcceleratingOrCruising、Idle→Braking 等用户动作对应的迁移。
- **事实**：事实成立。stm0.puml:6-8 恰为三条边：`Idle --> AcceleratingOrCruising : Accelerate Signal`、`AcceleratingOrCruising --> Braking : Brake Signal`、`Braking --> Idle : Stop Signal`，确是单向环，所指的那几条反向/跨越边都不存在。
- **NL**：NL 义务真实存在但未指定这些位置。NL S1 逐字：'based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states'；NL S3 逐字：'the system transitions between different substates depending on actions like accelerating, braking, or stopping'。NL 只点名三个动作（accelerating / braking / stopping）与三个子态，从未枚举任何具体的 source→target 对；作者的三条边恰好与 NL 的三个动作一一对应。报告者要求补的那些边来自现实驾驶合理性（reason 逐字：『用户在刹车过程中重新加速是典型的用户动作』『在 Idle 时用户仍可能踩刹车（例如驻车制动）』），是领域常识而非 NL 依据。
- **去重**：`0003-子态间被要求补齐NL未指定的迁移对` —— 三格五条，或整体说『覆盖不全』、或逐条点某一条缺边，同为 stm0.puml:6-8 这批子态迁移的完备性这一处争议。
- **成员**：run1/0003-claude#1 run2/0003-claude#2 run2/0003-claude#3 run2/0003-claude#4 run3/0003-claude#2

**0003-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J1

- **主张**：顶层初始边进入 PoweredOff 而非 Operate，与 NL 1『上电即进入 Operate』不符；PoweredOff 作为初始状态无 NL 依据。
- **事实**：事实成立。stm0.puml:2 逐字 `[*] --> PoweredOff`，:11 `PoweredOff --> Operate : start`——根初始边确不直指 Operate。
- **NL**：NL 义务真实存在但未指定该位置。NL S1 逐字：'Once the device is powered on, the system enters the `Operate` state'——'Once ... powered on' 是时间前件，不是对根初始伪状态目标的规定；NL S2 逐字：'The system can be turned on with the `start` signal and turned off with the `keyOff` signal'，明确要求存在开/关两态与 start 信号，PoweredOff 正是它的落点。二句合起来由 `[*]→PoweredOff→(start)→Operate` 完整兑现。分类学已就同 NL 组的 0022-2 作过同判：『NL 未要求根初始边直指 Operate，同组 6 个作者无一直连』。
- **去重**：`0003-根初始边被要求直指Operate` —— 三格同一主张，同指 stm0.puml:2 那条根初始边的目标这一处争议点。
- **成员**：run1/0003-claude#2 run1/0003-gpt#1 run3/0003-gpt#1

**0003-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J1

- **主张**：`PoweredOff --> [*] : end` 引入了 NL 从未提及的 end 信号与终止行为。
- **事实**：事实成立。stm0.puml:13 逐字 `PoweredOff --> [*] : end`；nl.txt 全文只出现 start 与 keyOff 两个信号名，无 end。
- **NL**：NL 无此禁止。NL S2 逐字：'The system can be turned on with the `start` signal and turned off with the `keyOff` signal.'——用的是 'can be'，未写『只有』『仅限这两个信号』，故 NL 的信号枚举默认不封闭。合式性层亦无支撑：该边不造成不可达、死端、非确定或名字碰撞（恰相反，它是全模型唯一的真正终止路径），且本簇三条 issue 也未主张任何合式性后果。
- **去重**：`0003-NL未提及的end终止迁移被判为多余` —— 三格同一主张，同指 stm0.puml:13 这一条边。
- **成员**：run1/0003-claude#3 run2/0003-claude#1 run3/0003-claude#1

**0003-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J1

- **主张**：Operate 没有历史机制，keyOff 后再 start 会强制回到 Idle 而非上次子态。
- **事实**：事实成立。stm0.puml:5 为 `[*] --> Idle`，Operate 内无任何历史伪状态（`[H]`/`[H*]`），故每次进入 Operate 都落到 Idle。
- **NL**：NL 无此义务。nl.txt 三句均未提及断电重进后是否保留子态；两条 issue 自己都写明了这一点（『规范未明确规定 keyOff 后是否要清除子状态』『这与规范未做明确约束』）。把 NL 的沉默读成必须以 history 伪状态实现，属对实现形态的过度指定。
- **去重**：`0003-上电复位被读成历史伪状态义务` —— 两格同一主张，同指 Operate 的默认进入点（stm0.puml:5）与 :11/:12 那对开关边的组合语义这一处争议。
- **成员**：run1/0003-claude#4 run2/0003-claude#5

**0003-5** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J1

- **主张**：keyOff 未限定只能在安全子态（如 Idle）下发生，模型允许在 Braking / AcceleratingOrCruising 中直接关机。
- **事实**：事实成立。stm0.puml:12 `Operate --> PoweredOff : keyOff` 挂在复合态 Operate 上，按 UML 复合态出边语义对其全部子态生效（编译产物 model.fcstm:17-19 把它下沉成 Idle/AcceleratingOrCruising/Braking 三条，可作旁证）。
- **NL**：NL 义务真实存在但被钉在 NL 未指定的位置上。NL S2 逐字：'The system can be turned on with the `start` signal and turned off with the `keyOff` signal.'——无任何状态前件，作者的写法恰是对该无限定表述的忠实实现。issue 自己承认『规范虽然说 keyOff 关闭系统，但通常应在安全（例如 Idle）状态下允许关机……这一点规范并未明确授权』，其依据是领域安全常识而非 NL。
- **去重**：`0003-关机信号被要求限制在安全子态` —— 单成员组；根因是 stm0.puml:12 那条 keyOff 边的作用范围，与 0003-4（同指该边但争的是再次进入的落点）不是同一处主张。
- **成员**：run3/0003-claude#3


## pair 0004 — 6 簇　📄 无 NL 依据×6

**0004-1** ｜ 📄 无 NL 依据 ｜ `N-MODAL` ｜ 3/6 格 ｜ X1-J4

- **主张**：Approaching 子状态未以自迁移/内部活动/驻留条件显式表达 NL 9-10 的「继续接近并保持在该子状态直到准备停止或减速」
- **事实**：事实成立：stm0.puml:24-26 的 Approaching 体内只有一行 `Approaching: do/Send`，既无自迁移也无驻留守卫；离开 Approaching 的唯一途径是顶层 stm0.puml:29 `InMotion --> Stopping : Arrived/Stop, Send Arrived` 与 :30 的 Obstacle Detected 边。但「保持在某状态直到某迁移触发」是状态机的默认驻留语义，不需要任何显式构造来兑现。⚠️ 本条虽落 N-MODAL，却不是「断言构造问题」：X1 臂根本不构造谓词断言（产出是自由文本评审），把 NL 的 remains 强化成需要显式表达的驻留义务，是报告者自己的读法，不是某个 invariant 谓词族逼出来的。
- **NL**：NL 10 逐字：'The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate.'；NL 9 逐字：'In the Approaching substate, the system sends the "Send" signal and continues to approach the destination.' 两句都是对 Approaching 语义的定性描述（remains / continues），NL 全文未要求任何自迁移、内部循环，也未要求把停止条件绑定到 Approaching——NL 2 恰恰把 Arrived 迁移挂在 InMotion 上：'In the InMotion state, the system can either transition to the Stopping state when it arrives'。
- **去重**：`0004-Approaching驻留语义被要求显式构造` —— 三格讲的是同一处：把 NL 9/10 的 remains/continues 定性描述读成 Approaching 必须有显式的持续/保持构造。
- **成员**：run1/0004-gpt#2 run2/0004-gpt#2 run3/0004-gpt#4

**0004-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J4

- **主张**：Approaching 的 Send 被写成 do-activity，而 NL 的 sends 是一次性发送，应为 entry 或迁移动作
- **事实**：事实成立：stm0.puml:25 逐字为 `Approaching: do/Send`，确为 do 相位而非 entry。但该输出动作本身在作者源上存在（并非缺失），争议只在相位选择。
- **NL**：NL 9 逐字：'In the Approaching substate, the system sends the "Send" signal and continues to approach the destination.' NL 只说「在该子状态中发送」，全文未出现 entry / on entry / once / do 等相位限定词，也未规定该发送是一次性还是持续性。issue 自己也承认「规范没有明确它是 entry 还是 do」——即它索要的义务在 NL 里不存在。
- **去重**：`0004-一次性发送动作被写成do相位` —— 与 0004-3 同一处根因：作者对 NL 的 sends 一律选用 do/ 相位承载（:25 与 :34），报告者把 NL 未规定的相位读成义务。
- **成员**：run2/0004-claude#2

**0004-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J4

- **主张**：EmergencyStopping 把 Send Obstacle Detected 写成 do 行为，而 NL 3 把它与 Emergency Stop 并列为进入动作，应为 entry
- **事实**：事实成立：stm0.puml:32-35 中 :33 为 `EmergencyStopping: entry/Emergency Stop`、:34 为 `EmergencyStopping: do/Send Obstacle Detected`，两个动作确实分属不同相位。两个动作在作者源上都存在，争议只在 :34 的相位。
- **NL**：NL 3 逐字：'When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal.' NL 用 includes the actions … and sends … 作语义说明，未规定二者必须同为 entry 相位，也未出现任何相位词。
- **去重**：`0004-一次性发送动作被写成do相位` —— 与 0004-2 同一处根因：作者对 NL 的 sends 一律选用 do/ 相位承载（:25 与 :34），报告者把 NL 未规定的相位读成义务。
- **成员**：run2/0004-claude#3 run3/0004-gpt#3

**0004-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J4

- **主张**：Stopping 是空状态，既无出口迁移也无进入动作，NL 的 Stop/Send Arrived 被放在迁移标签上而非 Stopping 的 entry 上
- **事实**：事实成立：stm0.puml:37 逐字为 `state Stopping`，体内为空，全文无以 Stopping 为源的迁移。但把 Stop, Send Arrived 放在迁移标签上正是作者源 :29 `InMotion --> Stopping : Arrived/Stop, Send Arrived` 的写法，与 NL 的挂载位置一致；issue 自己也写「语义上可接受」，并未主张任何合式性后果（未称其不可达、未称其破坏确定性），故不走合式性层。EmergencyStopping（:32-35）同样无出边，是 NL 设计的两个终点之一。
- **NL**：NL 2 逐字：'the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal' —— NL 把 Stop, Send Arrived 逐字挂在迁移信号上，作者照办。NL 全文十句从未描述 Stopping 之后发生什么，也未要求 Stopping 有任何 entry/do 动作或出边。
- **去重**：`0004-终态Stopping的到达动作被要求改挂到状态上` —— 单成员组：根因是报告者要求把 NL 挂在迁移标签上的 Stop/Send Arrived 改挂成 Stopping 的状态动作，并据此说该状态「空」。
- **成员**：run2/0004-claude#4

**0004-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J4

- **主张**：InMotion --> EmergencyStopping 的标签只写 Obstacle Detected，未把「检测到障碍」这一触发条件与 EmergencyStopping 内发出的同名信号在语法上区分开
- **事实**：事实成立：stm0.puml:30 逐字为 `InMotion --> EmergencyStopping : Obstacle Detected`，标签确实只有这一串；:34 的输出写作 `do/Send Obstacle Detected`。两者字面并不相同（一个是 `Obstacle Detected`、一个是 `Send Obstacle Detected`），不构成名字碰撞，故无合式性后果可依。
- **NL**：NL 2 逐字：'or to the EmergencyStopping state if an obstacle is detected'；NL 3 逐字：'sends the "Obstacle Detected" signal'。⭐ 触发与信号同名这件事是 NL 自己造成的——它用同一串 Obstacle Detected 既描述检测条件又命名被发送的信号；NL 未要求二者在模型里必须以不同语法形态或不同名字表达。
- **去重**：`0004-标签沿用NL散文串未区分触发与信号` —— 与 0004-6 同一处根因：作者把 NL 的散文串原样当迁移标签与动作标签用，报告者要求一种能区分触发/动作/信号名的记法，而 NL 未规定这种记法。
- **成员**：run2/0004-gpt#1 run3/0004-gpt#2

**0004-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J4

- **主张**：do/Send Obstacle Detected 这一串可能被读成一个名为「Send Obstacle Detected」的动作，而非发送名为「Obstacle Detected」的信号
- **事实**：事实成立：stm0.puml:34 逐字为 `EmergencyStopping: do/Send Obstacle Detected`，动作名与被发信号名确实合写在一串里。该动作在作者源上存在，争议纯在记法。
- **NL**：NL 3 逐字：'includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal'。NL 只给了信号名，未规定发送动作必须用某种「动作名 + 信号名」分离的语法书写；PlantUML 也不提供这种语法区分。
- **去重**：`0004-标签沿用NL散文串未区分触发与信号` —— 与 0004-5 同一处根因：作者把 NL 的散文串原样当迁移标签与动作标签用，报告者要求一种能区分触发/动作/信号名的记法，而 NL 未规定这种记法。
- **成员**：run2/0004-gpt#3


## pair 0005 — 1 簇　📄 无 NL 依据×1

**0005-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J3

- **主张**：DoorOpen→DoorShut 用了规范未出现的触发事件名 “Close Door”，且该边未判断物品是否存在
- **事实**：stm0.puml:7 逐字 `DoorOpen --> DoorShut : Close Door`——该边确实存在、触发名确为 “Close Door”、边上确无物品判断守卫，三点都属实。同 NL 组另两个作者把同一条边写作 “Door Closed”（0045:15、0055:8），可见事件名纯属作者用词。
- **NL**：NL 2 逐字 “The door can be closed to return to the DoorShut state.”——NL 以散文描述该动作，未给任何事件标识符，也未要求命名风格一致；物品在不在由 DoorOpen / DoorOpenWithItem 两个状态承载（NL 3 “In the DoorOpen state, placing an item inside the microwave transitions the system to DoorOpenWithItem”），NL 未要求在关门边上再判一次物品。
- **去重**：`0005-关门事件名与命名风格被当作义务` —— 本簇唯一根因是把 NL 2 的散文动作描述读成对事件命名与命名风格一致性的义务。
- **成员**：run1/0005-claude#2


## pair 0006 — 3 簇　📄 无 NL 依据×3

**0006-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 4/6 格 ｜ X1-J1

- **主张**：Intercepted 是 NL 未描述的多余中间状态——NL 3 要求被拦截时直接转入 FormationAdjustment，模型却先进 Intercepted 再无触发地转入。
- **事实**：事实成立。stm0.puml:7 `Searching --> Intercepted : Interception Detected`、:22 `Intercepted : UAV Swarm Intercepted`、:23 `Intercepted --> FormationAdjustment`（确无触发）。
- **NL**：NL 无此禁止。NL 3 逐字：'When the UAV swarm is intercepted, it transitions to the formation adjustment state.'——只正面要求这条可达关系（作者经 :7+:23 兑现），未使用『只有』『直接』『不得经由中间态』一类封闭性措辞，故 NL 的状态枚举默认不封闭。合式性层亦无支撑：Intercepted 可达（:7）、有出边（:23）、Searching 的两条出边触发互异不构成非确定；无触发出边在 UML 中是合法的完成迁移。四条 issue 也未主张任何合式性后果。
- **去重**：`0006-NL未点名的拦截中间态被判为多余` —— 四格同一主张，同指 stm0.puml:7/22/23 这批 Intercepted 相关行。
- **成员**：run1/0006-claude#4 run2/0006-claude#4 run2/0006-gpt#4 run3/0006-claude#4

**0006-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 4/6 格 ｜ X1-J1

- **主张**：`Task Assignment Received` 只挂在 Searching 上，未覆盖 'During flight' 所含的其他飞行状态（FormationAdjustment / Intercepted 等）。
- **事实**：事实成立。stm0.puml:8 `Searching --> Attack : Task Assignment Received` 是全文唯一带该触发的边；FormationAdjustment（:10-14）与 Intercepted（:22-23）内外都没有同触发的出边。
- **NL**：NL 义务真实存在（任务分配→攻击，作者已在 :8 兑现），但被钉死在 NL 并未指定的那些位置上。NL 4 逐字：'During flight, if task assignment information is received, it enters the attack state.'——'During flight' 是语境状语：本机全程处于飞行，NL 中不存在与之对立的非飞行上下文（分类学以同一句作为 N-CTX 的范例句），因此它不划出一个必须逐一挂载该触发的状态集合，只是场景背景。NL 2 又把搜索确立为常态作业（'continuously performs target search tasks'），作者把该触发挂在常态作业态上是忠实读法。
- **去重**：`0006-任务分配触发被要求覆盖NL未指定的其他状态` —— 四格同一主张，同指 stm0.puml:8 那条边的作用范围这一处争议点。
- **成员**：run1/0006-claude#5 run1/0006-gpt#4 run2/0006-claude#6 run3/0006-claude#5

**0006-3** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J1

- **主张**：Attack 状态下缺少被拦截的处理路径，攻击过程中被拦截无路可走。
- **事实**：事实成立。`Interception Detected` 在 stm0.puml 全文只出现于 :7（源为 Searching）；Attack 复合态（:16-20）内外均无拦截出边。
- **NL**：NL 义务真实存在（拦截→编队调整，作者已在 :7+:23 兑现），但被钉死在 NL 并未指定的位置上。NL 3 逐字：'When the UAV swarm is intercepted, it transitions to the formation adjustment state.'——NL 只描述了这一条迁移，没有说拦截可发生于任意状态；把一条被描述的迁移读成对全部状态的普遍义务，是把义务锚到 NL 未指定的源态上。issue 自己也标注为『（可选问题）』。
- **去重**：`0006-拦截处理被要求覆盖NL未指定的攻击态` —— 单成员组；根因是 stm0.puml:7 那条拦截边的源态范围。与 0006-2 虽同属『要求补全触发覆盖面』，但争的是另一条边（:7 vs :8）、另一个触发，是另一处争议点。
- **成员**：run2/0006-claude#5


## pair 0007 — 4 簇　🚫 越界×3　📄 无 NL 依据×1

**0007-1** ｜ 🚫 越界 ｜ `OOS-REGION` ｜ 5/6 格 ｜ X1-J3

- **主张**：NL 第 1 句的「三个 region」应在顶层以正交区实现，模型却把三部分做成顺序连接的独立复合状态
- **事实**：事实属实：stm0.puml 顶层确有三个平级 state 块（:4 CollisionDetection、:11 CollisionAvoidance、:25 OperationalControls），彼此由 :31 `CollisionDetection -down-> CollisionAvoidance : Collision Mode Active` 与 :32 `CollisionAvoidance --> InitialState : Collision Resolved` 串联；源内 `--` 分隔符共 3 个（:12 :16 :20），全部在 CollisionAvoidance 内部，顶层无任何正交区。
- **NL**：NL 1 逐字 “There are three region in this diagram”。这是一条 region 计数 / 组织义务，M=(S,E,V,Tr,A) 无正交区语义，按分类学属 OOS-REGION（「某复合态下恰好 N 个区」类计数义务），与 v46 主臂 0007-3 同判。
- **去重**：`0007-顶层三区计数与组织义务` —— 五条簇都在要求 NL 1 的「三个 region」落到顶层正交区上，是同一处区组织主张。
- **成员**：run1/0007-claude#2 run1/0007-gpt#1 run2/0007-claude#1 run3/0007-claude#1 run3/0007-gpt#3

**0007-2** ｜ 🚫 越界 ｜ `OOS-REGION` ｜ 3/6 格 ｜ X1-J3

- **主张**：CollisionAvoidance 状态体首行即 `--`，多出一个空的第一区，实际是 4 个区而非 3 个
- **事实**：事实属实：stm0.puml:11-12 逐字为 `state CollisionAvoidance {` 紧接一行 `  --`，首个分隔符之前无任何内容；三个分隔符在 :12 :16 :20。model.fcstm:31 的 named 串自申报 “[PlantUML concurrent region 0] states=-; transitions=-” 与 region 1/2/3 各两态，确为「一个空区 + 三个功能区」。
- **NL**：NL 3 逐字 “The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.”——本簇的主张是区的数量（4 vs 3）与分隔符摆放，属区计数义务，落在 M 之外。
- **去重**：`0007-首行分隔符产生空区使区数为四` —— 三条簇讲的都是同一处写法（:12 的前置分隔符）造成的空区与区数不符。
- **成员**：run1/0007-claude#6 run2/0007-claude#3 run3/0007-claude#2

**0007-3** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 1/6 格 ｜ X1-J3

- **主张**：三个并发控制完成后没有 join/汇合语义，Collision Resolved 与三区的完成态之间无关联
- **事实**：事实属实：stm0.puml:14/18/22 三条区内边分别到 BrakingComplete / SteeringComplete / AlertComplete，源内无 join、无区内 final；离开该复合态只有 :32 `CollisionAvoidance --> InitialState : Collision Resolved` 一条组迁移。
- **NL**：NL 3 只说正交区 “allow for concurrent activation different of collision avoidance controls”，从未要求三区完成后汇合。主张「三个并发控制都完成才退出」依赖正交区并发语义（并发完成与区间同步），M 无此语义。
- **去重**：`0007-并发区完成后的汇合同步义务` —— 单成员组；根因是把并发区的 join/同步语义当成模型义务。
- **成员**：run1/0007-claude#5

**0007-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J3

- **主张**：CollisionAvoidance 只是普通顶层复合态，未以子机器 / active-mode 父状态的形态标出激活边界
- **事实**：事实属实：stm0.puml:11-23 CollisionAvoidance 是一个顶层 state 块，由 :31 从 CollisionDetection 迁入、:32 迁出；源内没有名为 active mode 的父状态，也没有任何 submachine 标记。
- **NL**：NL 2 “This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.” 与 NL 3 “the active mode of collision avoidance”——两句都是在解释该复合态何时活跃，未规定必须以 submachine 或独立 active-mode 父状态这种形态实现；「被检测到就迁入该复合态」在 :31 已被表达。属形态过度指定。
- **去重**：`0007-要求以子机器形态标出active-mode边界` —— 单成员组；根因是把 NL 的语义说明读成必须存在 submachine / active-mode 父状态这一实现形态。
- **成员**：run3/0007-gpt#2


## pair 0009 — 8 簇　📄 无 NL 依据×4　❌ 假阳性×2　🚫 越界×1　✅ 真漏记×1

**0009-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 5/6 格 ｜ X1-J2

- **主张**：enter_hwy --> cruise 的守卫 dist_to_front>=25 是 NL 未给出的额外约束，属模型自行补充的过度推断。
- **事实**：事实成立。作者源 stm0.puml:16 逐字为 enter_hwy --> cruise : dist_to_front>=25，该守卫确由作者补出，NL 未逐字给出它。
- **NL**：NL 3 只写「can transition to cruise or lane_change based on the distance to the front vehicle (dist_to_front<25) and the availability of an extra lane (extra_lane=true)」，仅点名换道支的条件，对巡航支未作规定；NL 全文无封闭性/排他性表述（无 only / exactly / must not），故「NL 没写这个守卫」不构成禁止它的义务，何况 dist_to_front>=25 恰是 NL 所给 dist_to_front<25 的补集。
- **去重**：`0009-巡航入口守卫被补成NL未给的互补条件` —— 五条 issue 指向同一处作者编辑（stm0.puml:16 的守卫），主张完全一致：NL 未授权该守卫。
- **成员**：run1/0009-claude#5 run1/0009-gpt#3 run2/0009-claude#2 run2/0009-gpt#3 run3/0009-claude#1

**0009-2** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 2/6 格 ｜ X1-J2

- **主张**：intersection 子状态未以 state 行显式声明，且没有任何出边、进入后无法离开。
- **事实**：两半都不成立。其一，intersection 由 stm0.puml:34 enter_urban --> intersection : intersection=true 与 :41 straight --> intersection : intersection=true 隐式声明，是 UrbanMode 的合法子状态（model.fcstm:46 亦有 state intersection），缺的只是一行字面 state 声明——元素以另一种合法语法存在。其二，「无法离开」与作者源逐字相反：stm0.puml:46 UrbanMode --> FinishState : auto_finished=true 与 :48 UrbanMode --> HighwayMode : high_way=true 是复合态 UrbanMode 的出边，按 UML 语义对含 intersection 在内的全部子态生效。
- **NL**：NL 7/9 只说何时转入 intersection（if it detects an intersection），既未规定它必须以 state 行显式声明，也未规定它必须有区内出边。
- **去重**：`0009-intersection以隐式声明形式存在被判成缺失` —— 三条 issue 都把 intersection 的隐式声明与「无区内出边」当作同一处缺陷陈述，指向 stm0.puml:34/:41 同一元素。
- **成员**：run1/0009-claude#4 run2/0009-claude#6 run2/0009-claude#7

**0009-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J2

- **主张**：enter_urban --> straight 的守卫 road clear 未被形式化为可判定的变量或比较式。
- **事实**：事实成立。stm0.puml:33 逐字为 enter_urban --> straight : road clear，是一条散文标签，未给出可判定谓词。
- **NL**：NL 7 自己就只写「or straight if the road ahead is clear」，未给任何标识符、变量或比较式（对照同句的 dist_to_front<15 和 intersection=true，NL 是给了形式的）。要求作者把这条散文条件形式化，是 NL 未提出的实现形态义务。
- **去重**：`0009-road-clear散文守卫被要求形式化` —— 两条 issue 指向同一条边（stm0.puml:33）的同一处标签，主张一致。
- **成员**：run1/0009-claude#6 run3/0009-claude#12

**0009-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J2

- **主张**：碰撞避免的激活守卫用布尔量 high_way=true / urban_way=true 判定所处模式，而非引用当前所在的 HighwayMode / UrbanMode 状态。
- **事实**：事实成立。stm0.puml:55 逐字含 (dist_to_front<15 && high_way=true) || (dist_to_front<10 && urban_way=true)。
- **NL**：NL 12 的「in highway mode」/「in urban mode」是语境限定；而 NL 2 逐字把同一对布尔条件指派为选择该模式的判据（high_way=true for HighwayMode / urban_way=true for UrbanMode），NL 11 又逐字称它们为 the conditions。作者用的正是 NL 自己给出的条件串；要求改用状态成员谓词是 NL 未提出的实现形态义务。
- **去重**：`0009-模式判定沿用NL自带布尔条件被要求改为状态成员` —— 三条 issue 指向同一条边（stm0.puml:55）的同一对析取支，主张一致。
- **成员**：run1/0009-claude#7 run2/0009-claude#11 run3/0009-claude#9

**0009-5** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 3/6 格 ｜ X1-J2

- **主张**：CollisionAvoidanceSystem 与 AutonomousMode 应建模为并发/正交区域，二者需并行运行。
- **事实**：事实成立。stm0.puml:4 与 :51 是两个平级顶层状态，源内无任何 -- 分隔符，二者不可能同时活跃。
- **NL**：NL 12/13 描述碰撞避免子系统在行驶期间独立运作；但本簇主张要求两个状态同时活跃、并行演化，位于正交区并发语义之内，而 paper1 的建模对象 M=(S,E,V,Tr,A) 无并发语义。判 OUT_OF_SCOPE 即正确姿态，既不据此说方法未检出，也不反过来说该模型没有并发问题。
- **去重**：`0009-碰撞避免子系统与驾驶模式的并发关系` —— 三条 issue 都主张两个顶层状态之间缺少并发/正交关系，指向同一处顶层结构。
- **成员**：run1/0009-claude#8 run2/0009-claude#10 run3/0009-claude#7

**0009-6** ｜ ✅ 真漏记 ｜ `V2` ｜ 1/6 格 ｜ X1-J2

- **主张**：CollisionAvoidanceSystem 没有任何初始入口或入边，永远不会被激活。
- **事实**：事实成立，且不依赖并发读法。stm0.puml:2 唯一的顶层初始边是 [*] --> AutonomousMode；全文再无任何指向 CollisionAvoidanceSystem 的边（:51 只是它的声明），故该顶层状态在 M 中不可达（model.fcstm:80 同样只有 [*] -> AutonomousMode）。issue 自己说出了这一后果（「没有被任何初始伪状态激活」）。本 pair 台账三条（EIS-0009-01/02/03）全部围绕 FinishState 与 exit_urban，无一覆盖此条；争议元素 CollisionAvoidanceSystem 与三条记录所指语句无引用关系，非同根。
- **NL**：合式性层主张（可达性 / 初始态），不要求 NL 依据。台账自身已收录同 species 的记录——EIS-0032-01 逐字记「AcceleratingState 更是全模型无任何入边」——故本层在本臂成立。NL 12 逐字「The collision avoidance system is initially in the collision_avoidance_deactive state」在该状态不可达时亦无法兑现。
- **去重**：`0009-碰撞避免子系统无入边而不可达` —— 单成员组。根因是作者把碰撞避免子系统写成一个无任何入边的平级顶层状态，使其在 M 中不可达。
- **成员**：run3/0009-claude#8

**0009-7** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J2

- **主张**：HighwayMode 与 UrbanMode 互切会重置目标模式的内部子状态，未用历史伪状态保留进度，不满足 seamless。
- **事实**：事实成立。stm0.puml:47-48 两条切换边的目标是复合态本身，进入后按 :13 [*] --> enter_hwy 与 :29 [*] --> enter_urban 回到入口子态。
- **NL**：NL 11 只写「facilitating seamless mode shifts during the drive」，是定性描述，未要求保留子状态历史，更未指定必须使用历史伪状态；M=(S,E,V,Tr,A) 内亦无历史伪状态这一构造。两名成员自己也用「存疑」「也可以接受」措辞承认 NL 未作规定。
- **去重**：`0009-模式切换未保留子状态被读成历史伪状态义务` —— 三条 issue 指向同一对边（stm0.puml:47-48）与同一后果（回到入口子态），主张一致。
- **成员**：run1/0009-claude#9 run2/0009-claude#9 run3/0009-claude#11

**0009-8** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 1/6 格 ｜ X1-J2

- **主张**：InitialState --> HighwayMode / UrbanMode 未明确说明进入后应落到 enter_hwy / enter_urban。
- **事实**：不成立。落点已由合法的初始伪状态给出：stm0.puml:13 [*] --> enter_hwy、:29 [*] --> enter_urban；issue 自己也承认「语义上可以工作」。NL 要求的入口子态因此已被表达，只是没有重复写在 :9/:10 那两条边上——所指内容以另一种合法形式存在。
- **NL**：NL 3 逐字「the system begins in the enter_hwy substate」、NL 7 逐字「the system begins in the enter_urban substate」——该义务已由复合态的初始伪状态兑现，NL 未要求它必须写在跨层入边上。
- **去重**：`0009-复合态入口经初始伪状态兑现被判成未指向子态` —— 单成员组。根因是把合法的初始伪状态入口读成「未指定进入子态」。
- **成员**：run2/0009-claude#8


## pair 0011 — 5 簇　📄 无 NL 依据×4　✅ 真漏记×1

**0011-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J2

- **主张**：ClampingLoseState 及 OperationalState --> ClampingLoseState 是 NL 未提及的多余状态与迁移。
- **事实**：事实成立。stm0.puml:14-15 逐字含 OperationalState --> ClampingLoseState : Transition to Clamping Lose State 与 ClampingLoseState : Clamping Lose State，NL 1-3 确无「夹紧失效」这一概念。
- **NL**：NL 1-3 只描述初始态、制动态、运行态与制动钳夹紧态，但全文无任何封闭性 / 排他性表述（无 only / exactly / must not），「NL 没提到它」不构成禁止它的义务。八条成员无一指出该状态带来任何合式性后果（例如它自身也无出边），故不得按合式性层判——不能替 issue 补论证。
- **去重**：`0011-ClampingLoseState及其入边被判为NL未授权的多余元素` —— 八条 issue 指向同一处作者编辑（stm0.puml:14-15）：多出的状态与它唯一的入边，粒度不同但主张同一。
- **成员**：run1/0011-claude#1 run1/0011-gpt#2 run2/0011-claude#1 run2/0011-claude#2 run2/0011-gpt#1 run3/0011-claude#1 run3/0011-claude#2 run3/0011-gpt#1

**0011-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 2/6 格 ｜ X1-J2

- **主张**：Signal Transmission Fails 的源不应是 InitialState，应位于「收到制动信号之后」的处理链上。
- **事实**：事实成立。stm0.puml:6 逐字为 InitialState --> OperationalState : Signal Transmission Fails。
- **NL**：NL 2 逐字「When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state.」——第二句只给出目标态 operational state，从未指定该迁移的源态。义务真实存在且已兑现，只是被钉死在 NL 并未指定的源位置上（形态二）。
- **去重**：`0011-传输失败边的源被钉死在制动信号处理之后` —— 两条 issue 指向同一条边（stm0.puml:6），主张一致。
- **成员**：run1/0011-claude#2 run2/0011-claude#4

**0011-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J2

- **主张**：BrakingState --> InitialState : Signal Feedback Sent 是 NL 未要求的迁移，反馈返回应只从 OperationalState 出发。
- **事实**：事实成立。stm0.puml:12 逐字为 BrakingState --> InitialState : Signal Feedback Sent；同名边在 :11 也从 OperationalState 出发。BrakingState 因此有两条出边（:8 与 :12），二者触发不同，不产生非确定性。
- **NL**：NL 2 逐字「Once the signal feedback is sent, it returns to the initial state」——该句未点名源态；NL 3「After entering the braking state, the system transitions to the brake caliper clamping state」所要求的那条边在 :8 已存在，NL 从未声明制动态的出边集合是封闭的。把语序读成「只许从 OperationalState 返回」属封闭枚举误读。
- **去重**：`0011-制动态回初始态的边被判为NL未授权` —— 三条 issue 指向同一条边（stm0.puml:12），主张一致。
- **成员**：run1/0011-claude#3 run2/0011-claude#3 run3/0011-claude#3

**0011-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J2

- **主张**：BrakingState --> ClampingState : Entering Clamping State 把目标状态名当作触发事件，NL 描述的是自动后继。
- **事实**：事实成立。stm0.puml:8 逐字为 BrakingState --> ClampingState : Entering Clamping State，标签即目标态名的动名词形式。
- **NL**：NL 3 逐字「After entering the braking state, the system transitions to the brake caliper clamping state」——它既未给出该迁移的触发标识符，也未逐字规定必须写成无触发的完成迁移；要求改写成完成迁移是 NL 未提出的形态义务。
- **去重**：`0011-进入夹紧的迁移被要求写成无触发完成迁移` —— 两条 issue 指向同一条边（stm0.puml:8）的同一处标签，主张一致。
- **成员**：run1/0011-claude#4 run3/0011-claude#4

**0011-5** ｜ ✅ 真漏记 ｜ `V2` ｜ 3/6 格 ｜ X1-J2

- **主张**：进入 ClampingState 后没有任何返回路径，Signal Feedback Sent 回到 InitialState 的复位行为无法发生。
- **事实**：事实成立。stm0.puml 全文只有 :8 的入边与 :9 的描述行提到 ClampingState，没有任何以它为源的迁移，它是一个死端（model.fcstm 同样只有 BrakingState -> ClampingState）。三名成员都自己说出了这一后果（「一旦到达 ClampingState，模型没有反馈返回 InitialState 的路径」「进入 ClampingState 后没有返回路径」），未由判定者补论证。本 pair 台账 0 条。同 NL 组旁证：0021 写了 ClampingState --> BrakingState，0031 与 0051 写了 ClampingState --> InitialState，0041 写了两条出边——五个兄弟制品中四个给了出边。
- **NL**：合式性层主张（死端），不要求 NL 依据；台账已收录同 species 的记录（EIS-0026-03 记 FormationAdjustmentState 是吸收态）。NL 2 逐字「Once the signal feedback is sent, it returns to the initial state」在进入该状态后永远无法兑现，构成 NL 侧的同向佐证。
- **去重**：`0011-夹紧态无任何出边形成死端` —— 三条 issue 讲同一件事：ClampingState 无出边导致反馈复位不可达。
- **成员**：run1/0011-gpt#1 run2/0011-gpt#2 run3/0011-gpt#2


## pair 0012 — 1 簇　📄 无 NL 依据×1

**0012-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 2/6 格 ｜ X1-J6

- **主张**：Operate 内三个子态只有 Idle→AcceleratingOrCruising→Braking→Idle 的单向环，缺少 NL 暗示的其它切换（如 Braking 再 accelerate 回 AcceleratingOrCruising、AcceleratingOrCruising 时 stop 回 Idle）
- **事实**：事实成立。stm0.puml:6-8 逐字只有三条子态迁移：`Idle --> AcceleratingOrCruising : accelerate`、`AcceleratingOrCruising --> Braking : brake`、`Braking --> Idle : stop`，确实构成单向环，无 Braking--accelerate-->AcceleratingOrCruising 也无 AcceleratingOrCruising--stop-->Idle。三个子态均可达、均有出边，无死端或不可达，故不构成合式性后果（issue 自己也未主张任何合式性后果）。
- **NL**：NL 无此义务。NL 1 逐字 'based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states'，NL 3 逐字 'transitions between different substates depending on actions like accelerating, braking, or stopping'——`like` 明示是举例，NL 只枚举了三个子态与三个动作，从未规定迁移关系必须完备（更未点名 Braking 下 accelerate 这条边）。把「在 A、B、C 之间切换」的枚举读成「三态之间应有完整切换图」属把不封闭枚举升格为结构义务。
- **去重**：`0012-子状态切换关系被读成完整图` —— 两条簇成员指向同一处：作者在 stm0.puml:6-8 只写了三条子态迁移这一处建模选择，被两轮分别报为「覆盖不完整」。
- **成员**：run1/0012-claude#3 run3/0012-claude#2


## pair 0013 — 3 簇　📄 无 NL 依据×3

**0013-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J2

- **主张**：三个主子态之间迁移的事件标签（Water Flow Detected 等）是 NL 未给出的自造事件。
- **事实**：事实成立。stm0.puml:12-19 六条迁移各带一个作者自拟标签（Water Flow Detected / Methane Flow Detected / Water Flow Controlled / Transition to Methane / Methane Flow Controlled / Transition to Water），NL 未给出其中任何一个名字。
- **NL**：NL 1 逐字写「from which it can transition to different substates based on specific conditions」——NL 明说存在具体触发条件却不给标识符，等于授权而非禁止；NL 全文无封闭性表述，「NL 没写这些事件名」不构成禁止它们的义务。
- **去重**：`0013-迁移事件名被当作NL未授权的新增` —— 三条 issue 指向同一批迁移标签（stm0.puml:12-19），主张一致。
- **成员**：run1/0013-claude#2 run2/0013-claude#4 run3/0013-claude#6

**0013-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J2

- **主张**：WaterState 与 MethaneState 之间存在 NL 未描述的直接双向迁移。
- **事实**：事实成立。stm0.puml:16 WaterState --> MethaneState : Transition to Methane 与 :19 MethaneState --> WaterState : Transition to Water 确实存在。
- **NL**：NL 3-5 只逐句说系统可以转入 PumpState / WaterState / MethaneState，未枚举子态之间的迁移集合，也无 only / must not 一类封闭表述；NL 1 反而写 it can transition to different substates based on specific conditions。把这份不完全枚举读成「未列出的迁移即禁止」属封闭计数误读。
- **去重**：`0013-三主态之间的迁移集合被读成NL封闭枚举` —— 本组两簇（0013-2 与 0013-3）都指向第一区域内同一批迁移（stm0.puml:15-19），根因同为把 NL 对子态的枚举读成对迁移集合的封闭约束。
- **成员**：run1/0013-claude#4 run2/0013-claude#5 run3/0013-claude#4

**0013-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J2

- **主张**：WaterState / MethaneState 返回 PumpState 的迁移在 NL 中没有定义。
- **事实**：事实成立。stm0.puml:15 WaterState --> PumpState : Water Flow Controlled 与 :18 MethaneState --> PumpState : Methane Flow Controlled 确实存在，NL 未逐字描述返回路径。
- **NL**：NL 1-5 只给出可转入各子态的方向性描述（transition to the WaterState / MethaneState substate），从未声明迁移集合是封闭的，也未禁止返回边。
- **去重**：`0013-三主态之间的迁移集合被读成NL封闭枚举` —— 与 0013-2 同根：同一批第一区域迁移（stm0.puml:15-19）被按封闭枚举判为越界。
- **成员**：run3/0013-claude#5


## pair 0014 — 1 簇　📄 无 NL 依据×1

**0014-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 6/6 格 ｜ X1-J4

- **主张**：InMotion --> Stopping 的标签写作 Arrived/Stop, SendArrived，与 NL 2 逐字给出的 Arrived/Stop, Send Arrived（Send 与 Arrived 之间有空格）字面不一致
- **事实**：事实成立：stm0.puml:20 逐字为 `InMotion --> Stopping: Arrived/Stop, SendArrived`，确实无空格；NL 2 引号内为 'Arrived/Stop, Send Arrived'，两串字面确有一个空格之差。⭐ 但该输出动作本身在作者源上是在的（就在这条标签的效果槽里），并非缺失；全模型无第二个 SendArrived / Send Arrived 标识符，故不产生名字碰撞、不产生歧义、不影响可达性或确定性——本条无任何合式性后果可依（走 §4.2(b) 分支 2 而非分支 1）。对照同 NL 组的 0004：其 stm0.puml:29 写作 `Arrived/Stop, Send Arrived`（带空格），可见空格与否是作者的记法自由度，两种写法在 M 上是同一个动作。
- **NL**：NL 2 逐字：'the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal'。NL 确实在引号内给出了带空格的串，但它给的是一个散文信号名，NL 全文未规定模型标识符必须与该引号串逐字节相同，也未规定任何词法/命名形态。报告者自己也把这条主张写成条件式——「若按信号名精确匹配，这是不符合项」——即它索要的是一条 NL 未设定的逐字标识符匹配准则。
- **去重**：`0014-NL信号名的空格被读成逐字标识符义务` —— 六格讲的是同一处：stm0.puml:20 那一个空格，被读成 NL 对标识符字面的强制要求。
- **成员**：run1/0014-claude#5 run1/0014-gpt#1 run2/0014-claude#4 run2/0014-gpt#1 run3/0014-claude#5 run3/0014-gpt#1


## pair 0015 — 2 簇　📄 无 NL 依据×2

**0015-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J6

- **主张**：DoorShut 上的 Cancel 自环冗余、且不带任何动作，语义不明
- **事实**：事实成立但方向相反的部分要点明：stm0.puml:12 逐字 `DoorShut -down-> DoorShut : Cancel` 确实存在且确实无动作。但 issue 称「这在状态机中通常不需要显式建成自迁移」——NL 1 逐字要求这条自环存在（见 nl 栏），故「冗余」一说与 NL 相反；剩下可成立的只有「无动作」这一形态观察。自环不影响可达性、不造成死端与非确定（DoorShut 另有 `Door Opened` 出边，stm0.puml:11）。
- **NL**：NL 1 逐字：'From this state, the system can either remain in DoorShut if a Cancel action is performed or transition to the DoorOpen state when the door is opened.'——NL 明确要求 Cancel 时保持在 DoorShut，作者显式建模自环是忠实实现。NL 全文未给 DoorShut 的 Cancel 附加任何动作义务（timer/display 类动作义务集中在 NL 5/6/7/8，全部落在 ReadytoCook / Cooking，见 EIS-0015-01）。要求自环「应附带相应行为」是把 NL 的状态保持描述读成动作实现义务。
- **去重**：`0015-DoorShut自环被要求附带动作` —— 单成员组：根因是 stm0.puml:12 这一处作者编辑（Cancel 自环）被要求附带动作/被判冗余。
- **成员**：run2/0015-claude#5

**0015-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J6

- **主张**：DoorShutWithItem 缺少对 Cancel 的处理（应有 Cancel 出边）
- **事实**：事实成立。stm0.puml:21-22 逐字给出 DoorShutWithItem 的全部出边：`DoorShutWithItem -left-> DoorOpenWithItem : Door Opened` 与 `DoorShutWithItem -left-> ReadytoCook : Time Set`，确无 Cancel 出边。DoorShutWithItem 可达（:18、:24 两条入边）且有出边，无合式性后果。
- **NL**：NL 无此义务。NL 5 逐字只给 DoorShutWithItem 两条行为：'In the DoorShutWithItem state, opening the door transitions the system back to DoorOpenWithItem, while entering cooking time takes the system to ReadytoCook'——恰与作者写的两条出边一一对应。Cancel 义务在 NL 中真实存在，但只出现在 NL 1（DoorShut 保持）与 NL 6（ReadytoCook → DoorShutWithItem），NL 从未把它钉在 DoorShutWithItem 上；issue 自己也承认是「暗示…可能是遗漏」的类推。
- **去重**：`0015-Cancel义务被外推到DoorShutWithItem` —— 单成员组：根因是把 NL 1/6 的 Cancel 义务外推到 NL 未指定的 DoorShutWithItem 出边集合上。
- **成员**：run2/0015-claude#6


## pair 0016 — 5 簇　📄 无 NL 依据×5

**0016-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J2

- **主张**：从 FormationAdjust / AttackState 返回 SearchMission 会经初始伪状态重置到 Region1，丢失搜索进度，应使用历史伪状态。
- **事实**：事实成立。stm0.puml:27 AdjustingFormation --> SearchMission : Finish Adjusting 与 :34 Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count 的目标都是复合态本身，进入后按 :5 [*] --> Region1 回到 Region1。
- **NL**：NL 3/4 只说被拦截时转入编队调整态、飞行中收到任务分配时进入攻击态，对返回后的落点只字未提；NL 2 的 continuously performs 是定性描述，未要求保留中断前的区域上下文，更未指定必须使用历史伪状态（M=(S,E,V,Tr,A) 内亦无该构造）。多名成员自己用「直觉不符」「应使用历史伪状态」措辞，说明这是他们补出的实现形态义务。
- **去重**：`0016-复合态返回未保留区域进度被读成历史伪状态义务` —— 五条 issue 讲同一件事：返回复合态经默认初始入口丢失区域进度；两条返回边（:27 与 :34）是同一处建模写法的两个实例。
- **成员**：run1/0016-claude#3 run1/0016-claude#4 run1/0016-gpt#3 run3/0016-claude#4 run3/0016-claude#5

**0016-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 4/6 格 ｜ X1-J2

- **主张**：「攻击完成后无人机数量减少」只写在迁移标签里，未声明为可观测的数量变量或属性。
- **事实**：一半不成立、一半为真。递减并非「只是注释」：作者在 stm0.puml:34 用 PlantUML 的效果槽逐字写了 Attack Finished / Decrease UAV swarm count，斜杠之后即效果（四条成员中三条自己也承认它是 action，索要的是变量）。为真的只有「没有一个名为 UAV count 的变量声明」——PlantUML 无变量声明语法，本语料作者变量数为零。
- **NL**：NL 4 逐字「After completing the attack, the number of UAVs in the swarm decreases accordingly」——该义务已被作者以动作形式表达；NL 未要求该数量成为一个可被守卫或查询的一等实体。台账自身的分界线同向：EIS-0026-02 之所以成立，理由逐字是 0026 那条迁移「只有 trigger，无 / effect、无 [guard]、无任何计数文本」，而 0016 的作者写了。
- **去重**：`0016-数量递减已写为迁移效果却被索要变量声明` —— 四条 issue 指向同一条边（stm0.puml:34）的同一段效果文本，主张一致。
- **成员**：run1/0016-claude#5 run1/0016-gpt#4 run2/0016-claude#3 run3/0016-claude#6

**0016-3** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 4/6 格 ｜ X1-J2

- **主张**：Task Assignment Received 只在 SearchMission 上有出边，未覆盖 FormationAdjust / AttackState 等同属「飞行期间」的状态。
- **事实**：事实成立。stm0.puml:30 SearchMission --> AttackState : Task Assignment Received 是唯一一条，源内确无以 FormationAdjust 为源的同名边。
- **NL**：NL 4 逐字「During flight, if task assignment information is received, it enters the attack state」。During flight 是语境状语，整台机器全程在飞行，NL 中不存在与之对立的非飞行上下文；NL 从未指定该迁移还须从编队调整态出发。义务真实存在且已在 :30 兑现，只是被钉死在 NL 并未指定的那个位置上（形态二）。
- **去重**：`0016-Duringflight状语被读成攻击边须覆盖其它飞行态` —— 四条 issue 讲同一件事：把 During flight 读成对该迁移源态的覆盖义务。
- **成员**：run1/0016-gpt#2 run2/0016-gpt#2 run3/0016-gpt#3 run3/0016-claude#7

**0016-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J2

- **主张**：SearchMission 的两条外层出边未表明能否从三个 Region 子态触发，应在区层级明确适用性或加注释。
- **事实**：事实成立但无害。stm0.puml:23 SearchMission --> FormationAdjust : Interception Detected 与 :30 的源都是复合态，按 UML 对全部子态生效；run2/0016-claude#5 自己写「模型的写法是正确的」，索要的只是额外标注。
- **NL**：NL 3/4 只说何时进入编队调整态与攻击态，未要求把适用范围重复标注在各区层级，也未要求任何注释；这是文档可读性偏好，不是 NL 义务。
- **去重**：`0016-两条外层出边被追加NL未要求的说明性义务` —— 本组两簇（0016-4 与 0016-5）指向同一对作者编辑（stm0.puml:23 与 :30），根因同为对这两条边追加 NL 未要求的额外说明性义务。
- **成员**：run1/0016-claude#6 run2/0016-claude#5

**0016-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J2

- **主张**：Interception Detected 与 Task Assignment Received 两事件的优先级、互斥与同时触发处理未定义。
- **事实**：事实成立但不构成非确定性。stm0.puml:23 与 :30 是两条从同一复合态出发、触发事件不同的边，M 一次消费一个事件，不存在二者同时使能的配置，谈不上冲突。
- **NL**：NL 全文未提两事件的优先级或互斥关系；要求补守卫、优先级或注释是 NL 未提出的形态义务。
- **去重**：`0016-两条外层出边被追加NL未要求的说明性义务` —— 与 0016-4 同根：对 stm0.puml:23/:30 这同一对边追加 NL 未要求的说明性义务。
- **成员**：run1/0016-claude#7


## pair 0017 — 5 簇　📄 无 NL 依据×2　🚫 越界×2　✅ 真漏记×1

**0017-1** ｜ 📄 无 NL 依据 ｜ `N-SPLIT-PROSE` ｜ 5/6 格 ｜ X1-J2

- **主张**：三个区域的初始触发都写成泛化的 collision detected，未按前端 / 追尾 / 行人三类碰撞分型。
- **事实**：事实成立。stm0.puml:4 / :9 / :14 三条区内初始边的标签逐字都是 collision detected，源内没有任何分型事件名。
- **NL**：NL 2 逐字「This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected」——散文 or 并列三种情形却不给任何标识符，作者自己把它塌缩成一个泛化名；报告者要落地这条主张必须自造三个分型事件名，造名空间无上界。分类学对本 pair 的同形簇已有同向裁定。
- **去重**：`0017-三类碰撞检测塌缩为单一泛化触发` —— 五条 issue 指向同一批标签（stm0.puml:4/:9/:14），主张一致。
- **成员**：run1/0017-claude#1 run1/0017-gpt#2 run2/0017-gpt#1 run3/0017-claude#1 run3/0017-gpt#1

**0017-2** ｜ ✅ 真漏记 ｜ `V2` ｜ 4/6 格 ｜ X1-J2

- **主张**：没有任何进入或激活 Collision_Avoidance_Active_Mode 的入口迁移，激活语义被下放到各区域的初始伪状态。
- **事实**：事实成立。stm0.puml 全文只有一个顶层元素 state Collision_Avoidance_Active_Mode {...}（:2-17），源内不存在任何顶层 [*] --> 边，也没有任何指向它的入边；三处 [*]（:4 :9 :14）全在区内。因此这台机器的起点未定义。旁证：fcstm_meta.json 自申报 R45.DEBT.missing_explicit_initial，投影不得不合成 state UnspecifiedInitial 与 [*] -> UnspecifiedInitial（model.fcstm:4,19）。同 NL 组五个兄弟制品全都写了顶层初始边（0007:2、0027:2、0037:2、0047:25、0057:22），只有本例没有。本 pair 台账 0 条，谈不上同根。
- **NL**：合式性层主张（初始态存在性），不要求 NL 依据；台账已收录同 species 的记录（EIS-0044-01 记 InMotion 漏内部初始伪状态、EIS-0032-01 记三个 Region 均无初始伪态），本条属同层而未被记。NL 2 逐字「This sub-machine becomes active when ... is detected」亦要求存在一个使该模式变为活动的入口。
- **去重**：`0017-顶层无初始伪状态使激活模式无入口` —— 五条 issue 讲同一件事：唯一顶层复合态没有任何入口 / 激活迁移，激活条件只写在区内初始边上。
- **成员**：run1/0017-claude#2 run1/0017-gpt#1 run2/0017-claude#1 run3/0017-claude#2 run3/0017-claude#3

**0017-3** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 4/6 格 ｜ X1-J2

- **主张**：三个区域用同一事件触发会同时激活全部三种控制，未体现按检测到的碰撞类型独立并发激活对应控制。
- **事实**：事实成立。stm0.puml:3 / :8 / :13 三个 -- 分隔符把 Collision_Avoidance_Active_Mode 分成三个正交区，三条区内初始边同用 collision detected；「同时进入三个区」正是正交区的并发进入语义。
- **NL**：NL 3 逐字「The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls」——主张的内容（并行进入、按类型独立并发激活、区间控制彼此独立）位于正交区并发语义之内，而 M=(S,E,V,Tr,A) 无并发语义。边界是双向的：判越界即正确姿态。
- **去重**：`0017-三个正交区的并发进入与终止语义` —— 本组两簇（0017-3 与 0017-4）都落在同一处正交区结构上：一个问并发进入、一个问并发终止合成，根因同为该制品用三个正交区表达 NL 3。
- **成员**：run1/0017-claude#3 run1/0017-gpt#3 run2/0017-claude#2 run2/0017-gpt#2

**0017-4** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 1/6 格 ｜ X1-J2

- **主张**：每个区域各自在 Collision avoided 后到达自己的终止伪状态，区域独立终止与子机整体退出条件如何合成未定义。
- **事实**：事实成立。stm0.puml:6 / :11 / :16 三条 X --> [*] : Collision avoided 分属三个正交区，各自指向本区终态。
- **NL**：该主张问的是「三个区各自到达终态如何合成为复合态的完成」，属正交区之间的同步 / 汇合语义，落在 M 之外；NL 3 本身也只在并发语境下谈这些区。
- **去重**：`0017-三个正交区的并发进入与终止语义` —— 与 0017-3 同根：同一处三正交区结构，此簇问的是终止侧的并发合成。
- **成员**：run2/0017-claude#3

**0017-5** ｜ 📄 无 NL 依据 ｜ `N-SPLIT-PROSE` ｜ 1/6 格 ｜ X1-J2

- **主张**：三个区的退出事件都叫 Collision avoided，无法区分哪一类碰撞被避免。
- **事实**：事实成立。stm0.puml:6 / :11 / :16 的标签逐字都是 Collision avoided。该 issue 另称「单个事件会同时结束所有区域」，那一半依赖正交区独立性；但本簇的主命题是退出事件未分型，本身不依赖并发语义，故不在流程 ② 短路。
- **NL**：NL 全文根本没有提到「碰撞被避免」这一事件——NL 1-3 只讲三个区、激活条件与并发激活。要求三个分型的避撞完成事件，报告者必须完全自造名字，造名空间无上界，且连散文并列的锚点都没有。
- **去重**：`0017-避撞完成事件被要求按碰撞类型分型` —— 单成员组。根因是把 NL 2 的检测三分型平移到 NL 完全未提的避撞侧，索要自造的分型完成事件。
- **成员**：run3/0017-claude#4


## pair 0019 — 6 簇　❌ 假阳性×4　📄 无 NL 依据×2

**0019-1** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 2/6 格 ｜ X1-J3

- **主张**：intersection 子态没有自身出边，进入后无法离开、构成死端
- **事实**：intersection 在 stm0.puml 只于 :27 与 :32 作为目标出现，确无以它为源的具名边；但 :38 `UrbanMode --> HighwayMode: high_way=true` 是以复合态 UrbanMode 为源的组迁移，UML 语义下任一子态（含 intersection）活跃时均可触发，R4.5 也据此下沉出 model.fcstm:54 `intersection -> [*] : /high_way_true`。故「进入后无法离开 / 永久锁定 / 死状态」与作者源逐字相反。弱读法「无法返回 straight、无法靠 auto_finished 结束」属实，但后者正是台账 EIS-0019-03 statement 逐字点名 intersection 所记的内容，不是新内容。
- **NL**：NL 7 “…or intersection if it detects an intersection (`intersection=true`)” 与 NL 9 只规定进入 intersection 的两条路径，全文未规定 intersection 的任何后继迁移，也无「城区各子态之间可任意切换」的表述。
- **去重**：`0019-intersection无自身出边被判为死端` —— 三条簇都在说 intersection 没有后继、构成死端，是同一处主张。
- **成员**：run1/0019-claude#5 run1/0019-claude#6 run2/0019-claude#4

**0019-2** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 3/6 格 ｜ X1-J3

- **主张**：HighwayMode↔UrbanMode 的切换建在复合态层，未说明再入时进入哪个子态、在具体子态处能否触发含糊
- **事实**：stm0.puml:37-38 两条边的源与目标确为复合态；但再入点在源里逐字写明——:11 `[*] --> enter_hwy`、:24 `[*] --> enter_urban`，从外部进入复合态必经该默认初始边；复合态为源的迁移在任一子态活跃时可触发，语义确定，R4.5 亦逐子态下沉（model.fcstm:31-34、:51-55）。故「没说明从哪个子状态开始 / 能否触发含糊」与作者源逐字相反。
- **NL**：NL 11 逐字 “The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively, facilitating seamless mode shifts during the drive.”——只要求可动态切换，未要求历史伪态或保留子态上下文。
- **去重**：`0019-复合态默认入口被判为未明示` —— 本组两簇（:37-38 的模式切换与 :7-8 的 InitialState 出边）指向同一处被指称的建模失误——「进入复合态时落到哪个子态未明示」，而该入口由 :11/:24 逐字给出。
- **成员**：run1/0019-claude#7 run2/0019-claude#5 run3/0019-claude#7

**0019-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J3

- **主张**：InitialState 的两条出边未表达互斥，两个条件同时为真时行为未定义
- **事实**：事实属实：stm0.puml:7-8 `InitialState --> HighwayMode: high_way=true` 与 `InitialState --> UrbanMode: urban_way=true` 并列且无互补守卫。但两条边标签不同，投影为两个不同事件（model.fcstm:5-6 high_way_true / urban_way_true），同一事件下不存在两条候选边，故不构成确定性缺陷（对照台账 EIS-0019-01 记的 enter_hwy 两条边才是逐字同条件）。
- **NL**：NL 2 逐字 “the system can transition to either HighwayMode or UrbanMode based on conditions: `high_way=true` for HighwayMode or `urban_way=true` for UrbanMode.”——NL 只给两个条件，未要求把 either…or 编码成排他守卫或说明互斥。把 NL 的枚举读成排他义务属 N-CLOSED。
- **去重**：`0019-模式选择两条边被要求编码互斥` —— 单成员组；根因是把 NL 2 的 either/or 枚举读成必须显式编码的排他义务。
- **成员**：run1/0019-claude#12

**0019-4** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 1/6 格 ｜ X1-J3

- **主张**：InitialState 的迁移落在复合态而非入口子态 enter_hwy / enter_urban
- **事实**：stm0.puml:7-8 的目标确为复合态；但入口子态由 :11 `[*] --> enter_hwy` 与 :24 `[*] --> enter_urban` 逐字给出，跨层进入复合态必经该默认初始边（issue 自己也承认这两行存在），故「是否重新进入 enter_hwy/enter_urban 未明示」与作者源逐字相反。
- **NL**：NL 3 “the system begins in the enter_hwy substate” 与 NL 7 “the system begins in the enter_urban substate”——这正是 :11 / :24 所写的默认初始边，NL 义务已被满足。
- **去重**：`0019-复合态默认入口被判为未明示` —— 与 0019-2 同一根因：把由 :11/:24 逐字给出的默认入口判成未明示，只是锚在 InitialState 的两条出边上。
- **成员**：run2/0019-claude#9

**0019-5** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 1/6 格 ｜ X1-J3

- **主张**：exit_urban 被声明在 UrbanMode 块之外，层级归属错误
- **事实**：exit_urban 首次出现在 stm0.puml:30 `lane_change_urban --> exit_urban: dist_to_exit<0.7`，该行位于 `state UrbanMode {`（:23）与 `}`（:34）之间，按 PlantUML 首次提及身份它就是 UrbanMode 的子态；model.fcstm:41 `state exit_urban` 也确实在 UrbanMode 块内。:35 只是它的一条出边写在块外，与声明位置无关。故「模型把 exit_urban 声明在 UrbanMode 块之外（在 } 之后）」与作者源逐字相反。
- **NL**：NL 8 逐字 “In the lane_change_urban substate, the system transitions to straight if the lane change is complete or to exit_urban if the distance to the urban exit is less than 0.7 kilometers (`dist_to_exit<0.7`).”——NL 把 exit_urban 当作 UrbanMode 内的子态，作者源正是如此。
- **去重**：`0019-exit_urban层级归属被误判` —— 单成员组；根因是误读 PlantUML 首次提及身份，把块内首现的 exit_urban 判成块外状态。
- **成员**：run3/0019-claude#8

**0019-6** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J3

- **主张**：到 FinishState 之后没有再初始化 / 重新选择模式的机制，模式选择只发生一次
- **事实**：FinishState 在 stm0.puml 只作为 :21 与 :35 的目标出现，确无出边——这一点属实；但「模式选择只发生一次」不成立：:37-38 两条组迁移在 HighwayMode / UrbanMode 活跃时始终可触发，模式切换可反复发生。
- **NL**：NL 6 “The HighwayMode ends when the system transitions to FinishState” 与 NL 10 “The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied”——NL 把 FinishState 当终点，全文未要求从它返回或重新初始化。NL 11 的动态切换义务真实存在，但它由 :37-38 兑现，本簇把它钉在 NL 并未指定的位置（FinishState 之后 / InitialState 重入）上，属 N-ANCHOR 形态二。
- **去重**：`0019-动态切换义务被钉在FinishState之后` —— 单成员组；根因是把 NL 11 的动态切换义务改锚到 FinishState 之后的再初始化上。
- **成员**：run3/0019-claude#10


## pair 0020 — 7 簇　📄 无 NL 依据×5　❌ 假阳性×2

**0020-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J4

- **主张**：AutonomousMode 被写成内联展开的复合状态，而 NL 2 要求用 submachine state 表示
- **事实**：事实成立：stm0.puml:6-15 是 `state AutonomousMode { ... }` 内联块，确无任何 submachine 引用记法。⭐ 但 NL 2 的实质内容「autonomous mode 有子状态」在作者源上是兑现的（:7-:14 共三个子态两条内迁移）；而 submachine state 在 $M=(S,E,V,Tr,A)$ 里根本没有与复合状态相区分的构造——UML 的 submachine state 语义就是把被引用机器内联，两者在 M 上是同一个对象，这条义务在 M 内无法被违反。同 NL 组旁证（md5 b11f6c…，6 份）：0000:7、0030:7、0040:6、0050:8 与 0020:6 都是内联复合块，唯一沾边的 0010:7 写的是 `Autonomous : <<submachine>>`——一条 PlantUML 描述行，同样不是 submachine 引用。6/6 作者无一产出真正的 submachine，可见这是 NL 的记法措辞而非可落地的建模区分。
- **NL**：NL 2 逐字：'The autonomous mode has sub-states and is represented by a sub machine state.' 该句前半（有子状态）是内容义务、已满足；后半（用 sub machine state 表示）是对绘制记法的说明，NL 全文未说明 submachine 与复合状态在行为上有何不同，也未据此提出任何可观察的行为要求。
- **去重**：`0020-内联复合状态被读成必须用submachine记法` —— 与 0020-6 同一处根因：作者用内联复合块承载 NL 2 的子状态要求，报告者把 NL 的 sub machine state 措辞读成强制记法。
- **成员**：run1/0020-claude#1

**0020-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 2/6 格 ｜ X1-J4

- **主张**：模型自造了 NL 未定义的三个自动模式子状态 AutoInitialState / AutoOperationalState / AutoFinalState
- **事实**：事实成立：stm0.puml:8/:10/:12 三条描述行声明了三个 NL 从未点名的子状态。但 NL 2 逐字要求 autonomous mode「has sub-states」，作者必须自己命名它们——⭐ NL 没有枚举子状态，不等于 NL 禁止子状态（§4.2(a)）。同 NL 组 6 份全部自造具体子态名：0000:8-9 AutoNavigating/AutoFinal、0030:8-9 Navigating/Parking、0040:7-9 AutoInitial/AutoFinal、0050:9-12 SubState1/2/3、0010:9-13 AutonomousIdle/AutonomousActive。可见自造子态名是该 NL 的通行读法，而非过度建模。本簇亦未主张任何合式性后果（未称三态不可达、死端或名字碰撞），故不走合式性层。
- **NL**：NL 2 逐字：'The autonomous mode has sub-states and is represented by a sub machine state.' NL 只给出「有子状态」这一存在性要求，全文未列举子状态名、未给数目、未出现「只有」「恰好」「不得」等封闭性/排他性表述。
- **去重**：`0020-自动模式内部结构被读成NL的封闭枚举` —— 与 0020-3 同一处根因：NL 2 只要求存在子状态、未枚举内部结构，报告者把「NL 没写」读成「NL 禁止」。
- **成员**：run1/0020-claude#5 run3/0020-claude#2

**0020-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J4

- **主张**：模型自造了 NL 未定义的自动模式内部迁移及其触发事件 Signal Transmission Succeeds 与 Mission Completed
- **事实**：事实成立：stm0.puml:9 `AutoInitialState -> AutoOperationalState: Signal Transmission Succeeds` 与 :11 `AutoOperationalState -> AutoFinalState: Mission Completed` 中的两个触发串在 NL 全文中不存在。但既然 NL 2 要求 autonomous mode 有子状态，子状态之间就必须有迁移与触发，而 NL 一个都没给，作者只能自造。同 NL 组同样如此：0000:9 `Condition Met`、0030:11-12 `Park Request`/`Parking Complete`、0040:7-8 `Enter Autonomous Mode`/`Auto Process Complete`。本簇未主张任何合式性后果。
- **NL**：NL 全文（5 句）无一处提到自动模式内部的迁移或触发事件；NL 2 只有 'The autonomous mode has sub-states'，NL 3/4/5 讲的都是与 human driving mode 之间的进出与断电。NL 既未枚举内部迁移，也未出现任何封闭性表述禁止它们存在。
- **去重**：`0020-自动模式内部结构被读成NL的封闭枚举` —— 与 0020-2 同一处根因：NL 2 只要求存在子状态、未枚举内部结构，报告者把「NL 没写」读成「NL 禁止」。
- **成员**：run1/0020-claude#3 run1/0020-claude#4 run2/0020-claude#1 run3/0020-claude#3

**0020-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J4

- **主张**：AutoFinalState 只是带描述行的普通命名状态，未用 PlantUML/UML 的 [*] 终态或复合状态完成态表达
- **事实**：事实成立：stm0.puml:12 逐字为 `AutoFinalState: Final State`，确是普通命名状态而非 `[*]`。⭐ 但本条不构成合式性主张，故不走 §4.2(b) 分支 1：机器并非永不终止——stm0.puml:16 `HumanDrivingMode -> [*]: Power Off` 与 :17 `AutonomousMode -> [*]: Power Off` 都通向真正的终态；AutoFinalState 也不是死端，它在 :14 有出边。issue 自己给出的后果是「完成语义未准确表达 / 无法自然触发基于子机完成的返回」，属语义表达偏好，不是可达性/死端/确定性/初始态/名字碰撞中的任何一项。同 NL 组：0000:9 与 0040:9 同样把 auto final 写成普通命名状态（`AutoFinal`），仅 0050:12 用了 `SubState3 --> [*]`。
- **NL**：NL 第 4 条（原文标号 '4.'）逐字：'transit to human driving mode when receive human steering cmd, brake pressed, in (auto final)'。NL 用 `in (auto final)` 作为一个状态成员条件来引用它，只说明存在这样一个自动模式最终状态，未规定它必须以终止伪状态语法书写；NL 全文无 final pseudostate / completion event 之类的记法要求。
- **去重**：`0020-autofinal被读成必须用终态伪状态记法` —— 两格讲的是同一处：stm0.puml:12 这个普通命名状态被读成必须改写为 [*] 终态记法。
- **成员**：run1/0020-gpt#2 run2/0020-gpt#1

**0020-5** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 2/6 格 ｜ X1-J4

- **主张**：Power Off 只在两条顶层出边上，未（显式）覆盖 AutonomousMode 内部各子状态的断电退出，缺少统一的全局断电机制
- **事实**：事实不成立：stm0.puml:17 逐字为 `AutonomousMode -> [*]: Power Off`。这是一条以复合状态为源的组迁移，按 UML/PlantUML 语义，只要 AutonomousMode 的任一子状态活跃它就使能——即三个子态全部被覆盖。R4.5 的展开逐字印证了这一点：model.fcstm:17-19 把它拆成 `AutoInitialState -> [*]`、`AutoOperationalState -> [*]`、`AutoFinalState -> [*]` 三条 `/Power_Off` 边。加上 :16 `HumanDrivingMode -> [*]: Power Off`，两条顶层状态各有一条，全模型不存在任何一个 Power Off 无法触发的状态。「未考虑在 AutonomousMode 内部所有子状态下都应能断电」（run3#5 逐字）因此是纯事实错误；r2c#5 自己也写「复合状态整体到终态可以覆盖 power off…模型的写法可以接受」，其残留主张只是要求冗余地逐子态重写一遍。
- **NL**：NL 第 5 条（原文标号 '5'）逐字：'when power off, it will transit to final state'。NL 只要求断电通向终态，未要求逐状态显式声明，也未要求「统一的全局机制」这种特定写法。
- **去重**：`0020-复合态断电出边被误读为未覆盖子状态` —— 两格讲的是同一处：把 stm0.puml:17 的复合态组迁移读成不覆盖其子状态。
- **成员**：run2/0020-claude#5 run3/0020-claude#5

**0020-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J4

- **主张**：Power Off 写在复合状态层、其对子状态的效力依赖复合状态语义，与 NL 2 要求的 submachine 表达方式不一致
- **事实**：事实成立：stm0.puml:17 `AutonomousMode -> [*]: Power Off` 确实写在复合状态层，其对三个子态的效力确实来自复合状态的组迁移语义。issue 自己写「虽然通常合法」，其残留的规范性主张只剩「与规范要求的 submachine 表达方式不一致」这一条。⭐ 流程 ④：composite-vs-submachine 这一缺口已由本 pair 的 0020-1 以正确框架（直接针对 AutonomousMode 的声明形态）承载，本簇只是同一义务挂在 Power Off 边上的换框架说法；而其覆盖面主张在 0020-5 已被判为事实错误。
- **NL**：NL 2 逐字：'The autonomous mode has sub-states and is represented by a sub machine state.'；NL 第 5 条逐字：'when power off, it will transit to final state'。NL 未把断电迁移的写法与 submachine 记法挂钩，也未要求 Power Off 必须是顶层任何状态皆可触发的统一迁移。
- **去重**：`0020-内联复合状态被读成必须用submachine记法` —— 与 0020-1 同一处根因：作者用内联复合块承载 NL 2 的子状态要求，报告者把 NL 的 sub machine state 措辞读成强制记法。
- **成员**：run1/0020-claude#7

**0020-7** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 1/6 格 ｜ X1-J4

- **主张**：HumanDrivingMode -> AutonomousMode : front_distance > 10 未显式说明进入的是自主模式的哪个子状态
- **事实**：事实不成立：作者在 stm0.puml:7 逐字写了 `[*] -> AutoInitialState`，这就是对「进入 AutonomousMode 后落到哪个子态」的显式声明；R4.5 亦原样保留为 model.fcstm:12 `[*] -> AutoInitialState;`。issue 自己也写「进入子状态由初始伪状态决定，符合规范」「此处基本符合规范…非严重问题」，其事实前提（未说明进入哪个子状态）与作者源第 7 行逐字相反。
- **NL**：NL 第 3 条（原文 '4when front_distance > 10, auto transport to autonomous state'）只要求在 front_distance > 10 时转入自主状态，未要求迁移标签本身指名目标子状态；作者源 :4 已逐字兑现该迁移。
- **去重**：`0020-入口子态已由初始伪状态声明却被判为未说明` —— 单成员组：根因是把 stm0.puml:7 的内部初始伪状态忽略掉，从而认为进入子态未被说明。
- **成员**：run2/0020-claude#6


## pair 0021 — 5 簇　📄 无 NL 依据×5

**0021-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 4/6 格 ｜ X1-J3

- **主张**：`Signal Transmission Fails` 的源应是 BrakingState（收到制动信号之后），模型挂在 InitialState 上，因而也缺 BrakingState→OperationalState
- **事实**：两条陈述都属实：stm0.puml:6 逐字 `InitialState --> OperationalState : Signal Transmission Fails`，源内确无 BrakingState→OperationalState。但同 NL 组六个制品（0001/0011/0021/0031/0041/0051）**6/6 逐字写的都是这同一行**，无一把失败分支挂在 BrakingState 上——这是该 NL 的通行读法。
- **NL**：NL 2 逐字 “When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state.”——NL 未点名该失败分支的源态；「信号传输失败」的自然读法恰是制动信号未送达、系统仍在初始态。义务真实存在但被钉死在 NL 并未指定的源态上，属 N-ANCHOR 形态二。
- **去重**：`0021-失败分支被钉在BrakingState为源` —— 五条簇（含「缺少 BrakingState→OperationalState」这一反面框架）指向同一处：失败分支的源态该挂在哪。
- **成员**：run1/0021-claude#1 run2/0021-claude#1 run3/0021-claude#1 run3/0021-claude#2 run3/0021-gpt#1

**0021-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J3

- **主张**：`BrakingState --> InitialState : Signal Feedback Sent` 是规范未描述的多余边，且绕过了 ClampingState
- **事实**：事实属实：stm0.puml:12 逐字 `BrakingState --> InitialState : Signal Feedback Sent`，从 BrakingState 出发确可不经 ClampingState 回到 InitialState。同 NL 组 6/6 作者都逐字写了这条边（0001/0011/0031/0041/0051 与 0021 完全同形）。
- **NL**：NL 2 “Once the signal feedback is sent, it returns to the initial state.” 未点名反馈边的源态；NL 3 “After entering the braking state, the system transitions to the brake caliper clamping state.” 是一条迁移要求，不含「只有 / 恰好 / 不得」这类封闭或排他表述。把 NL 的枚举读成「恰好这些、不许多」属 N-CLOSED。
- **去重**：`0021-制动态反馈回初始边被判为多余` —— 七条簇都在要求删掉 :12 这条反馈边（或指它破坏 NL 3 的顺序），是同一处多余性主张。
- **成员**：run1/0021-claude#2 run1/0021-gpt#1 run2/0021-claude#2 run2/0021-gpt#1 run3/0021-claude#3 run3/0021-gpt#2 run3/0021-gpt#4

**0021-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J3

- **主张**：`ClampingState --> BrakingState : Clamping Released` 是规范完全未提及的事件与反向迁移
- **事实**：事实属实：stm0.puml:14 逐字 `ClampingState --> BrakingState : Clamping Released`，NL 全文无 release/released 字样。同 NL 组各作者在夹紧态之后各自添加了不同的边（0041 `ClampingState --> BrakingState : Brake Signal Maintained`、0031 `ClampingState --> InitialState : Transition Missing Feedback`、0051 `ClampingState --> InitialState : Braking Complete`），可见 NL 对夹紧态之后一律未作规定。
- **NL**：NL 3 只有 “After entering the braking state, the system transitions to the brake caliper clamping state.”，未给夹紧态的后继，也没有任何封闭 / 排他表述；本簇没有任何成员说出该多余边造成的合式性后果（不可达 / 死端 / 非确定 / 名字碰撞）。按「模型多出规范没要求的元素」默认落 N-CLOSED。
- **去重**：`0021-夹紧释放反向边被判为多余` —— 六条簇都指 :14 这一条自加的反向边，是同一处多余性主张。
- **成员**：run1/0021-claude#3 run1/0021-gpt#2 run2/0021-claude#3 run2/0021-gpt#3 run3/0021-claude#4 run3/0021-gpt#3

**0021-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J3

- **主张**：BrakingState→ClampingState 本是顺序推进，模型却给它贴了 `Entering Clamping State` 触发标签
- **事实**：事实属实：stm0.puml:8 逐字 `BrakingState --> ClampingState : Entering Clamping State`，标签确是对目标状态的描述而非独立刺激。同 NL 组 6/6 作者逐字写的都是这一行。
- **NL**：NL 3 逐字 “After entering the braking state, the system transitions to the brake caliper clamping state.”——NL 只说这一步会发生，既未给触发事件名，也未要求它必须实现成无触发的完成迁移。要求某种迁移形态属 N-FORM。
- **去重**：`0021-顺序推进被要求写成无触发迁移` —— 三条簇都在要求去掉 :8 的触发标签、改成自动推进，是同一处形态主张。
- **成员**：run1/0021-claude#4 run2/0021-claude#5 run3/0021-claude#5

**0021-5** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 2/6 格 ｜ X1-J3

- **主张**：ClampingState 缺少「反馈发送后回到 InitialState」的出口，流程不闭合
- **事实**：事实属实：ClampingState 唯一出边是 stm0.puml:14 到 BrakingState，源内确无 `ClampingState --> InitialState`。但它不是死端——经 :14 离开后可由 :12 回到 InitialState。
- **NL**：NL 2 “Once the signal feedback is sent, it returns to the initial state.” 未点名该反馈边的源态，作者已在 :11（OperationalState）与 :12（BrakingState）为它给了两个源；NL 也未要求闭环必须从夹紧态直接返回。义务真实存在但被钉在 NL 并未指定的源态上，属 N-ANCHOR 形态二。（旁证：同组 0031/0041/0051 虽也给 ClampingState 加了回初始的边，但触发名各不相同，正说明 NL 未指定。）
- **去重**：`0021-反馈回初始义务被钉在夹紧态` —— 两条簇都在要求补 ClampingState→InitialState 的反馈边，是同一处锚点主张。
- **成员**：run2/0021-claude#4 run2/0021-gpt#2


## pair 0022 — 5 簇　📄 无 NL 依据×3　✅ 真漏记×1　❌ 假阳性×1

**0022-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 6/6 格 ｜ X1-J3

- **主张**：NL 说上电即进入 Operate，模型却先停在 PoweredOn、需再收 start 才进 Operate
- **事实**：事实属实：stm0.puml:2-3 逐字 `[*] --> PoweredOn` 与 `PoweredOn --> Operate: start`，根初始边确实不直指 Operate。但同 NL 组（0003/0012/0022/0032/0042/0052）**6/6 作者的根初始边都先落在一个 Operate 之前的状态**（PoweredOff / Off / OffState / Off / Off / PoweredOn），无一直连 Operate；该前置状态叫什么完全是作者用词。
- **NL**：NL 1 “Once the device is powered on, the system enters the `Operate` state” 与 NL 2 “The system can be turned on with the `start` signal”——NL 2 逐字要求一个由 start 触发的开机动作，故 Operate 之前必须有一个状态；NL 从未要求根初始边直指 Operate。与 v46 主臂 0022-2 同判 N-ANCHOR。
- **去重**：`0022-上电义务被钉在根初始边直指Operate` —— 七条簇都在要求根初始边（或 start 的位置）直接把系统放进 Operate，是同一处锚点主张。
- **成员**：run1/0022-claude#1 run1/0022-gpt#1 run2/0022-claude#1 run2/0022-gpt#1 run3/0022-claude#1 run3/0022-gpt#1 run3/0022-gpt#2

**0022-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J3

- **主张**：PoweredOn 是规范中不存在的多余状态
- **事实**：事实属实：stm0.puml:2 引入的 PoweredOn 在 NL 任何一句里都没有出现。
- **NL**：NL 1 只枚举 Operate 与三个子态、NL 2 要求 start / keyOff 两个信号；NL 无「只有 / 恰好 / 不得」这类封闭表述，而 NL 2 的 start 开机动作本身就需要一个 Operate 之前的状态（同组 6/6 作者都设了一个）。「NL 没写这个状态」不等于「NL 禁止它」，落 N-CLOSED。
- **去重**：`0022-前置状态被判为规范外多余状态` —— 单成员组；根因是把 NL 的状态枚举读成封闭清单。
- **成员**：run3/0022-claude#4

**0022-3** ｜ ✅ 真漏记 ｜ `V1` ｜ 2/6 格 ｜ X1-J3

- **主张**：keyOff 被建模为迁到顶层终态，关机后再也无法用 start 重新开启，start/keyOff 不再是可复用的开关
- **事实**：事实属实：stm0.puml:13 逐字 `Operate --> [*] : keyOff`——目标是顶层终态；源内没有任何从终态返回的边，也没有任何边回到 PoweredOn（PoweredOn 只被 :2 的根初始边进入）。故 keyOff 触发一次后整机完成，`start` 永不可能再被消费（model.fcstm:24 `Operate -> [*]` 亦确认顶层终态）。同 NL 组另 5 个制品全部把 keyOff 指回一个可再 start 的关机态：0003 `Operate --> PoweredOff : keyOff` + `PoweredOff --> Operate : start`；0012 与 0052 `Operate --> Off : keyOff` + `Off --> Operate : start`；0032 `OperateState --> OffState : keyOff` + `OffState --> OperateState : start`；0042 `Operate --> Off : keyOff` + `Off --> Operate : start`。5/5 兄弟都给出可复用开关环，只有 0022 走终态，说明这是该 NL 的通行读法而非过度指定。本 pair 台账 0 条，无任何记录覆盖该缺口。
- **NL**：NL 2 逐字 “The system can be turned on with the `start` signal and turned off with the `keyOff` signal.”——两个信号被并列声明为系统的开 / 关能力；模型让其中一个（keyOff）执行一次后另一个（start）永久失效，直接违反该句。属 NL 层逐字义务的真实漏记。
- **去重**：`0022-关机迁到终态使开关环不可复用` —— 三条簇（终态语义、无法再开启、无路径回到 PoweredOn）都出自 :13 这一处建模失误。
- **成员**：run1/0022-claude#2 run3/0022-claude#2 run3/0022-claude#3

**0022-4** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 2/6 格 ｜ X1-J3

- **主张**：keyOff 只在 Operate 下可用，PoweredOn 状态收不到 keyOff
- **事实**：事实属实：stm0.puml 全文只有 :13 一条 keyOff 边，源内确无 `PoweredOn --> ... : keyOff`。
- **NL**：NL 2 “The system can be turned off with the `keyOff` signal.” 未点名可关机的状态集；PoweredOn 是作者自造的前置状态，NL 从未提及它，因此 NL 不可能对它提出 keyOff 义务。义务真实存在但被钉在 NL 并未指定的位置上，属 N-ANCHOR 形态二。
- **去重**：`0022-关机义务被钉在作者自造前置状态上` —— 两条簇都要求给 PoweredOn 补一条 keyOff 出边，是同一处锚点主张。
- **成员**：run1/0022-claude#3 run2/0022-claude#2

**0022-5** ｜ ❌ 假阳性 ｜ `FP-N` ｜ 2/6 格 ｜ X1-J3

- **主张**：NL 第 3 条列出的 stopping 动作未被显式表达，模型用 `user idle` 代替
- **事实**：承载「停止」的迁移在作者源上逐字存在：stm0.puml:8 `AcceleratingOrCruising --> Idle: user idle` 与 :10 `Braking --> Idle: user idle`，投影为 model.fcstm:6 的独立声明 `event user_idle`。缺的只是字面拼写 stop/stopping，元素本身已作为一等 event 存在，属命名变体。
- **NL**：NL 3 逐字 “the system transitions between different substates depending on actions like accelerating, braking, or stopping.”——“like” 是举例，未规定精确拼写。与 v46 主臂 0032-3（同一 NL 组：断言要求 accelerating、制品已声明 event Accelerate）同判 FP-N。
- **去重**：`0022-stopping被判为缺失实为命名变体` —— 两条簇都在说 stopping 没有对应触发词，实为同一处命名变体误判。
- **成员**：run1/0022-claude#4 run2/0022-claude#3


## pair 0023 — 4 簇　🚫 越界×3　📄 无 NL 依据×1

**0023-1** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 6/6 格 ｜ X1-J4

- **主张**：PumpControl 用 `--` 把 PumpState / WaterState / MethaneState 写成三个正交并发区，进入 PumpControl 时三者被同时激活，而 NL 描述的是互斥可选子状态
- **事实**：事实成立：stm0.puml:5 与 :7 是两条单独成行的 `--`，PumpControl 内确被切成三个正交区，:4/:6/:8 三条 `[*] -->` 各属一区；R4.5 亦自申报 `R45.DEBT.concurrent_region_semantics` 与 `R45.DEBT.multiple_initial_fanout`，并在 model.fcstm:2 的 named 串里逐字记下 `[PlantUML concurrent region 0/1/2]` 与两处 `concurrent separator`。⭐ 但本簇索要的内容——三个子态不应同时活跃、应改为互斥择一——整体位于正交区并发语义之内，而 $M=(S,E,V,Tr,A)$ 无并发语义，按 §4.2(c) 越界。⚠️ 本条不用 `OOS-FLATTEN`：X1 读的是未展平的作者源，报告者是正确识别出 `--` 并就正交语义本身提出主张，不是在讲展平产物。⚠️ 双向缄默：既不记为方法未能检出，也不反过来说该模型没有并发问题。
- **NL**：NL 2 逐字：'Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState.'；NL 3 逐字：'The system first transitions to the PumpState substate'；NL 4 逐字：'The system can also transition to the WaterState substate'；NL 5 逐字：'Similarly, the system can transition to the MethaneState substate'。NL 确实读起来更像互斥择一，但「该用 OR 分解还是 AND 分解」这件事本身就是并发语义问题，落在 M 之外。
- **去重**：`0023-三子态被写成正交并发区` —— 与 0023-2、0023-3 同一处根因：作者在 stm0.puml:5 与 :7 写下两条 `--`，把三个子态做成正交分解；三簇分别是这一处决定的三个表现面。
- **成员**：run1/0023-claude#1 run1/0023-gpt#1 run2/0023-claude#1 run2/0023-gpt#1 run3/0023-claude#1 run3/0023-gpt#1

**0023-2** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 3/6 格 ｜ X1-J4

- **主张**：三条并列的初始伪状态迁移无法表达 NL 3 的「首先进入 PumpState」，应只有唯一一条 [*] --> PumpState 作为默认初始迁移
- **事实**：事实成立：stm0.puml:4/:6/:8 确有三条 `[*] -->`，分别指向 PumpState / WaterState / MethaneState，作者源上没有任何写法把 PumpState 标为唯一默认入口。⭐ 但这三条初始边不是并列于同一区的竞争入口——它们各属 :5/:7 分出的三个正交区，每区恰好一条，正是正交分解下**必须**有的写法。所以「应只剩一条」这条主张，等价于要求 PumpControl 不是正交分解；它的真假完全取决于按不按区读，按流程 ② 属越界。⚠️ 与 §4.2(c) 的分界另一侧对照：本簇讲的不是某个区内部与并发无关的普通缺陷，而是 PumpControl 顶层该用 OR 还是 AND 分解。
- **NL**：NL 3 逐字：'The system first transitions to the PumpState substate, where the pump is activated or controlled.' NL 确实给出了「首先进入 PumpState」的先后要求；但要在模型里把它兑现成唯一默认入口，前提是三个子态同属一区——而这个前提正是并发语义问题本身。
- **去重**：`0023-三子态被写成正交并发区` —— 与 0023-1、0023-3 同一处根因：三条初始边是 stm0.puml:5/:7 那两条 `--` 的直接产物，同属那一处正交分解决定。
- **成员**：run1/0023-claude#2 run2/0023-claude#2 run3/0023-claude#2

**0023-3** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 6/6 格 ｜ X1-J4

- **主张**：PumpState 与 WaterState / MethaneState 之间没有任何迁移，无法表达 NL 4、5 的「也可以转到」
- **事实**：事实成立：逐行核 stm0.puml 全文 13 行，除 :2 `[*] --> PumpControl` 与区内三条 `[*] -->` 外没有任何迁移，三个子态之间确为零迁移（:9/:10/:11 只是描述行）。⭐ 但这个零迁移正是正交分解的直接产物：三个子态分处 :5/:7 划出的三个不同区，UML 下同一复合态不同区之间本就不存在普通的区内迁移；本簇索要的「PumpState --> WaterState」只有在三者同属一区时才是一条合法的普通迁移。故该主张的可判定性依赖区语义，按流程 ② 越界。⚠️ 本条不用 `OOS-FLATTEN`：X1 看到的是作者源上原生的正交结构，零迁移在展平之前就已存在，成因是作者的正交分解而不是 R4.5。
- **NL**：NL 4 逐字：'The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow.'；NL 5 逐字：'Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow.' 两句确实用 can transition to 要求可切换；但「可切换」与「三区并行」在 M 内不可兼得，取舍属并发语义问题。
- **去重**：`0023-三子态被写成正交并发区` —— 与 0023-1、0023-2 同一处根因：子态间零迁移是 stm0.puml:5/:7 那两条 `--` 的直接后果，同属那一处正交分解决定。
- **成员**：run1/0023-claude#3 run1/0023-gpt#2 run2/0023-claude#3 run2/0023-gpt#2 run3/0023-claude#3 run3/0023-gpt#2

**0023-4** ｜ 📄 无 NL 依据 ｜ `N-FUSE` ｜ 2/6 格 ｜ X1-J4

- **主张**：NL 1 说子状态切换是「基于特定条件」发生的，而模型所有迁移都没有守卫条件、事件或触发标注
- **事实**：事实成立：逐行核 stm0.puml 全文 13 行，四条迁移（:2、:4、:6、:8）全部无标签，全模型无任何事件名、守卫或触发；R4.5 产出的 model.fcstm 里也一条 `event` 都没有。⭐ 本簇不判越界：它讲的不是区语义，而是「迁移上有没有条件标注」这一与并发无关的普通事实，故按 §4.2(c) 的分界走正常流程。
- **NL**：NL 1 逐字：'The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions.' ⭐ `specific conditions` 是一个上位统称词——它概括「若干具体条件」，而 NL 五句里**没有任何一个条件被命名**：NL 3 只写 'where the pump is activated or controlled'，NL 4/5 只写 'indicating that the pump is controlling or monitoring the water/methane flow'，都是对子状态含义的同位语注解，不是可落地的条件标识符。报告者若要把这条义务落到模型上，必须自造全部守卫名，造名空间无上界。故 NL 层无有效义务出处；合式性层也不要求迁移必须带守卫。
- **去重**：`0023-条件统称词被索要成具体守卫` —— 两格讲的是同一处：NL 1 的上位统称词 `specific conditions` 被索要成模型里必须存在的具体守卫/触发。
- **成员**：run1/0023-claude#4 run2/0023-gpt#3


## pair 0024 — 2 簇　📄 无 NL 依据×1　❌ 假阳性×1

**0024-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J4

- **主张**：DoorsClosing 内没有任何动作或 entry 行为的建模，只有一句描述文字，属于对起始状态语义的最小化实现
- **事实**：事实成立：stm0.puml:3 逐字为 `DoorsClosing: Doors are closing`，这是一条 PlantUML 描述行，确实不是 entry/do 动作；该状态体内无其它内容。⛔ 但它不构成合式性问题：DoorsClosing 有初始入边（:2 `[*] --> DoorsClosing`）与出边（:4 `DoorsClosing --> InMotion: Closed/SendDeparted`），既可达也非死端。issue 自己写「模型对此触发正确」「属于对起始状态语义的最小化实现——如需严格对齐规范建议补充」，即它索要的是一个 NL 未提出的补充。
- **NL**：NL 1 逐字：'The system starts in the DoorsClosing state and transitions to InMotion when the doors are closed, triggered by the "Closed/SendDeparted" signal.' NL 十句中与 DoorsClosing 相关的只有这一句，它只要求「起始于该状态」与「门关闭时经 Closed/SendDeparted 转入 InMotion」两件事，两者在 :2 与 :4 都已兑现。NL 从未给 DoorsClosing 指定任何 entry/do/exit 动作，也没有「Doors are closing」这个串——那是作者自加的描述。
- **去重**：`0024-起始态描述行被读成entry动作义务` —— 单成员组：根因是把 DoorsClosing 的一行自加描述读成「应有动作建模」，而 NL 对该状态只有初始与出边两项要求。
- **成员**：run2/0024-claude#5

**0024-2** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 1/6 格 ｜ X1-J4

- **主张**：Stopping 状态在模型中没有任何声明或描述，只作为迁移目标出现，缺失目标状态定义
- **事实**：事实不成立。逐行核 stm0.puml 全文 20 行：`Stopping` 确实只在 :16 `InMotion --> Stopping: Arrived/Stop, Send Arrived` 出现一次（`EmergencyStopping` 不含独立词 `Stopping`），但**在 PlantUML 里被迁移目标引用即构成合法的隐式状态声明**——它是另一种合法语法，不是缺失。R4.5 亦按此读法产出 model.fcstm:27 `state Stopping named "Stopping";`，即该状态确实进入了 $S$。同源作者的写法可对照：本 pair 的 `EmergencyStopping` 同样从未用 `state` 声明（只有 :17/:18/:19 三次引用），而同 NL 组的 0004:37 则显式写了 `state Stopping`——可见是作者的记法自由度，不是元素缺失。
- **NL**：NL 2 逐字：'the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal'。NL 只要求存在这个目标状态与该条迁移，两者都在 :16 兑现；NL 全文未给 Stopping 任何动作、描述或内部结构，也未要求它必须用显式 `state` 关键字声明。
- **去重**：`0024-隐式声明的Stopping被判为未定义` —— 单成员组：根因是把 PlantUML 中「由迁移目标隐式声明」这一合法形态判成了状态未定义。
- **成员**：run3/0024-claude#4


## pair 0025 — 1 簇　📄 无 NL 依据×1

**0025-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J5

- **主张**：DoorShutWithItem 缺少对 Cancel 的处理（自转移），与 DoorShut 不对称。
- **事实**：事实成立。stm0.puml 中 DoorShutWithItem 只有两条出边——:10 `DoorShutWithItem --> DoorOpenWithItem: Door Opened` 与 :11 `DoorShutWithItem --> ReadytoCook: Cooking Time Entered`，确无任何 Cancel 相关边（Cancel 只出现在 :3 DoorShut 自环、:12 ReadytoCook→DoorShutWithItem、:17 Cooking→ReadytoCook）。
- **NL**：Cancel 义务在 NL 中真实存在，但 NL 逐字只把它放在三个位置：NL 1「the system can either remain in DoorShut if a Cancel action is performed」、NL 6「In the ReadytoCook state, if the Cancel action is performed, the system returns to DoorShutWithItem」、NL 8「A Cancel action transitions the system back to ReadytoCook」。NL 从未把 Cancel 义务放到 DoorShutWithItem 上。issue 自陈「此为可疑项——规范未在 DoorShutWithItem 明确列出 Cancel 行为，但从 DoorShut 状态的类比看可能存在遗漏。仅作提示，非明确违规」，即义务来自类比而非 NL——真实义务被钉死在 NL 并未指定的那个状态上。
- **去重**：`0025-Cancel义务被类比推广到NL未指定的DoorShutWithItem` —— 单成员组。根因是：NL 对 Cancel 逐句限定了三个承载状态，报告按 DoorShut 的对称性把同一义务外推到 NL 未指定的 DoorShutWithItem。
- **成员**：run1/0025-claude#6


## pair 0026 — 1 簇　📄 无 NL 依据×1

**0026-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 2/6 格 ｜ X1-J2

- **主张**：Mission Completed 的终止边只从 TargetSearchingState 出发，任务完成不能发生在其它状态。
- **事实**：事实成立。stm0.puml:14 TargetSearchingState --> [*] : Mission Completed 是全模型唯一指向终态的边。成员之一 run2/0026-claude#5 顺带说「处于编队调整时无法完成任务」，那一半是台账 EIS-0026-03 已记的吸收态后果；但本簇主命题是完成边的来源覆盖，与 EIS-0026-03 不同根——争议元素 TargetSearchingState 在作者源被 :4 :5 :7 :10 :13 :14 多处引用，改掉 EIS-0026-03 所指的语句它依然在。
- **NL**：NL 2 逐字「Before the mission is completed, the UAV swarm continuously performs target search tasks」——它把任务完成置于搜索期之后，并未要求完成可以从编队调整态或攻击态发生。义务真实存在（任务会完成）却被钉死在 NL 并未指定的位置上（形态二）。
- **去重**：`0026-任务完成边的来源被要求覆盖全部状态` —— 两条 issue 指向同一条边（stm0.puml:14）与同一主张：完成边的源态覆盖不足。
- **成员**：run1/0026-claude#5 run2/0026-claude#5


## pair 0027 — 3 簇　📄 无 NL 依据×3

**0027-1** ｜ 📄 无 NL 依据 ｜ `N-SPLIT-PROSE` ｜ 1/6 格 ｜ X1-J6

- **主张**：三类碰撞被 OR 合并进单一迁移标签，应拆成三条并列触发或三个分别命名的事件
- **事实**：事实成立。stm0.puml:4 逐字 `DetectingState --> junction1: Frontend Collision or Rear-end Collision or Collision with Pedestrian detected`——作者确实把三种碰撞写进了一条自由文本标签，模型侧没有三个可分别引用的事件。注意本条不判 REPRESENTATION_DEBT：X1 读的就是这份作者源，主张针对的是作者自己选择的单一融合标签（BRIEF §1 规则 2）。
- **NL**：NL 未给标识符。NL 2 逐字 'This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.'——散文 or 并列三种情形，全句不含任何可作为事件名的标识符（对比 NL 1 的 'three region' 亦无标识符）。要拆成「三条并列触发或分别命名的事件」，报告者必须自造分型事件名，造名空间无上界。
- **去重**：`0027-三类碰撞被要求拆成独立命名事件` —— 单成员组：根因是 stm0.puml:4 这一处融合标签被要求按 NL 散文并列拆分。
- **成员**：run3/0027-claude#5

**0027-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J6

- **主张**：触发标签省略了 NL 的 'possible' 限定，读起来像已检测到碰撞本身而非碰撞风险
- **事实**：事实成立。stm0.puml:4 标签逐字为 'Frontend Collision or Rear-end Collision or Collision with Pedestrian detected'，确无 'possible' 一词。但该标签在 M 中只是一个不透明事件符号（编译产物 model.fcstm:2 把整串作为一个 event 的 named 显示串），其字面措辞不产生任何 S/E/V/Tr/A 层面的差异，也无合式性后果。
- **NL**：NL 2 逐字含 'a possible frontend collision'。但 NL 的 'possible' 是对碰撞风险性质的定性修饰，NL 未就事件命名提出任何义务；要求事件名逐字复现该修饰是对命名形态的过度指定。
- **去重**：`0027-事件名未复现possible修饰` —— 单成员组：根因是 stm0.puml:4 事件名的字面措辞被要求逐字复现 NL 的定性修饰词。
- **成员**：run3/0027-gpt#1

**0027-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J6

- **主张**：第三个正交区的 SensorControlState 不属于「碰撞避免控制」，与需求语义不匹配
- **事实**：事实成立（元素确在）。stm0.puml:14-16 逐字 `[*] --> SensorControlState`、`SensorControlState --> junction4`、`junction4 --> InitialState`。本条不属越界：它讲的是该区内部一个状态的语义归属，不依赖并发语义（BRIEF §4.2(c) 的例外）。issue 自身也是条件式表述「若需求中的三个区域均应为避撞控制…」。
- **NL**：NL 无此义务。NL 3 逐字 'The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.'——NL 既未枚举是哪三种控制，也没有任何「只有／恰好／不得」式的封闭或排他表述。把上位短语 'collision avoidance controls' 读成对每个区内状态的成员资格排他义务，属把不封闭表述升格为排他义务（BRIEF §4.2(a)：NL 没提到它 ≠ NL 禁止它）。
- **去重**：`0027-SensorControl被判定不属避撞控制` —— 单成员组：根因是 stm0.puml:14 引入的 SensorControlState 被判为不符合 NL 的控制类别。
- **成员**：run3/0027-gpt#2


## pair 0029 — 8 簇　📄 无 NL 依据×4　❌ 假阳性×3　🚫 越界×1

**0029-1** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 3/6 格 ｜ X1-J6

- **主张**：exit_urban 是规范外新增的中间态且没有后继迁移，会死锁/停滞在该状态
- **事实**：事实不成立。stm0.puml:26 `lane_change_urban --> exit_urban : dist_to_exit<0.7` 引入 exit_urban 后，作者确实没有再写以 exit_urban 为源的边；但 exit_urban 是 UrbanMode 的子态，而 UrbanMode 自身有两条复合态级出边——stm0.puml:38 `UrbanMode --> HighwayMode : high_way=true` 与 stm0.puml:43 `UrbanMode --> FinishState : auto_finished=true`——按 UML 复合态迁移语义对任一子态（含 exit_urban）均可触发。编译产物逐条展开印证：model.fcstm:79 `exit_urban -> [*] : /high_way_true`、model.fcstm:84 `exit_urban -> [*] : /auto_finished_true`。故「无出边/死锁/停滞」为假，出边以复合态级语法存在而未被看见。
- **NL**：另需纠正 run1/0029-claude#4 的 NL 侧断言：它称「exit_urban 是规范未定义的子状态」，而 NL 8 逐字含 'or to exit_urban if the distance to the urban exit is less than 0.7 kilometers (`dist_to_exit<0.7`)'——exit_urban 是 NL 点名的目标态，作者是忠实实现；run2/0029-gpt#4 自己也正确引了这句。NL 10 要求的 'The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true`' 亦已由 stm0.puml:43 给出。
- **去重**：`0029-UrbanMode子态被误判为无出边死端` —— 0029-1 与 0029-5 是同一处误读：都把 UrbanMode 复合态级出边（:38/:43）看漏，从而把其叶子态判成无出边死端。
- **成员**：run1/0029-claude#4 run2/0029-claude#4 run2/0029-gpt#4

**0029-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J6

- **主张**：straight 子态缺少 dist_to_exit<0.7 时退出（到 exit_urban 或 FinishState）的迁移
- **事实**：事实成立。stm0.puml:27-28 给出 straight 的全部出边：`straight --> intersection : intersection=true`、`straight --> lane_change_urban : dist_to_front<15 & extra_lane=true`，确无 dist_to_exit<0.7 的退出边。straight 可达且有出边，无合式性后果。（本簇附带提到的「exit_urban 无后继」由 0029-1 承载并已判为假。）
- **NL**：NL 无此义务。NL 9 逐字只给 straight 两条行为：'In the straight substate, if the system detects an intersection, it transitions to the intersection substate. If the distance to the front vehicle becomes less than 15 meters (`dist_to_front<15`) and an extra lane is available, it transitions to lane_change_urban.'——恰与作者两条出边一一对应。dist_to_exit<0.7 的退出义务在 NL 8 中真实存在，但 NL 只把它挂在 lane_change_urban 上；issue 自己也承认「虽规范未明确要求…只有 lane_change_urban 能退出显得不一致」。
- **去重**：`0029-退出边义务被外推到straight` —— 单成员组：根因是把 NL 8 挂在 lane_change_urban 的退出义务外推到 NL 未指定的 straight 上。
- **成员**：run1/0029-claude#5

**0029-3** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 3/6 格 ｜ X1-J6

- **主张**：CollisionAvoidance 应与 AutonomousMode 建成并行/正交区域，模型把它建成顶层顺序状态导致二者互斥、无法同时激活
- **事实**：事实层面属实：stm0.puml:31-35 的 `state CollisionAvoidance { ... }` 是与 AutonomousMode 平级的顶层状态，全文无 `--` 正交分隔符（stm0.puml 无任何单独成行的 `--`）。但主张的内容——「碰撞避免应与驾驶模式并行运行、二者应同时活跃」——正位于正交区并发语义之内；run3/0029-claude#6 逐字写「实际上它与 AutonomousMode 互斥，无法同时激活」，即要求多个状态同时保持活跃。$M=(S,E,V,Tr,A)$ 无并发语义，故越界。
- **NL**：NL 12/13 逐字描述碰撞避免子系统的两态与切换条件，未逐字要求并发；但即便 NL 要求，该义务也落在 $M$ 之外。按 CLAUDE.md 的双向缄默：不得据此说方法未能检出，也不得反过来说该模型没有并发问题。
- **去重**：`0029-碰撞避免应与驾驶模式并行` —— 三条簇成员指向同一处：CollisionAvoidance 与 AutonomousMode 的顶层并列结构应否为正交区。
- **成员**：run1/0029-claude#6 run2/0029-claude#7 run3/0029-claude#6

**0029-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：碰撞避免激活守卫混写 | 与 & 且未加括号，运算优先级/分组含糊，应显式分组
- **事实**：事实成立。stm0.puml:33 逐字 `collision_avoidance_deactive --> collision_avoidance_active : pedestrian_detected | dist_to_rear<5 & vel>30 | dist_to_front<15 & highway_mode | dist_to_front<10 & urban_mode`，确无括号。但该标签在 M 中整体塌成一个不透明事件（model.fcstm:14 把整串作为一个 event 的 named 串），根本不存在被求值的运算符优先级，故不产生任何合式性后果；run2/0029-claude#6 自己也承认「虽然巧合上语义正确」。
- **NL**：NL 无此义务。NL 12 逐字以散文 'such as … , … , or …' 并列四种情形，既未给出括号分组要求，也未给出任何形式化写法要求。把 NL 的散文并列读成「必须使用括号显式分组」属对表达形态的过度指定。
- **去重**：`0029-碰撞激活守卫标签写法被过度指定` —— 0029-4 与 0029-7 指向同一处建模失误：stm0.puml:33 这一条融合守卫标签的写法，一条挑括号分组、一条挑自造布尔量，是同一处编辑的两种框架。
- **成员**：run1/0029-claude#7 run2/0029-claude#6

**0029-5** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 1/6 格 ｜ X1-J6

- **主张**：UrbanMode 内 intersection 没有任何出边，是死状态、会锁死
- **事实**：事实不成立。stm0.puml:24 与 :27 以 intersection 为目标，作者确实没写以 intersection 为源的子态级边；但 intersection 是 UrbanMode 子态，UrbanMode 的复合态级出边 stm0.puml:38 `UrbanMode --> HighwayMode : high_way=true` 与 :43 `UrbanMode --> FinishState : auto_finished=true` 对它同样生效，编译产物 model.fcstm:78 `intersection -> [*] : /high_way_true`、:83 `intersection -> [*] : /auto_finished_true` 逐条印证。issue 断言的「缺少从 intersection 出去的任何迁移」与「会造成锁死」均为假；只有「无法回到 straight 或 enter_urban」这半句成立。
- **NL**：NL 无相关义务：NL 7/9 只描述如何进入 intersection（'or intersection if it detects an intersection'、'if the system detects an intersection, it transitions to the intersection substate'），全文未规定离开 intersection 的行为，故即便按成立的那半句也无 NL 依据。
- **去重**：`0029-UrbanMode子态被误判为无出边死端` —— 与 0029-1 同一处误读：把 UrbanMode 复合态级出边（:38/:43）看漏，从而把叶子态判成死端。
- **成员**：run1/0029-claude#11

**0029-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J6

- **主张**：enter_urban --> straight 的触发写作自造标识符 road_clear，规范未定义该变量、与其它条件的书写风格不一致
- **事实**：事实成立。stm0.puml:23 逐字 `enter_urban --> straight : road_clear`，而 NL 对该条件未给任何标识符（对比 NL 7 同句内的 `dist_to_front<15`、`intersection=true` 都带反引号标识符）。附带说明 run3/0029-claude#8 的次要主张「straight 未建成 else 分支、可能与其他两条守卫不确定」：enter_urban 的三条出边在 M 中被投影为三个不同事件（model.fcstm:68/69/70 的 `/dist_to_front_15_extra_lane_true`、`/road_clear`、`/intersection_true`），触发不同故不构成非确定。
- **NL**：NL 只有散文。NL 7 逐字 'or straight if the road ahead is clear'——NL 未给该条件任何标识符，因此作者取什么名字都不受 NL 约束；要求它「与规范其它条件命名风格保持严格一致」是纯形态偏好，run1/0029-claude#12 自己也写「此处虽合理…不算严重问题」。
- **去重**：`0029-road_clear标识符命名风格` —— 三条簇成员指向同一处：stm0.puml:23 作者为 NL 散文条件自取的标识符 road_clear。
- **成员**：run1/0029-claude#12 run2/0029-claude#5 run3/0029-claude#8

**0029-7** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J6

- **主张**：碰撞避免守卫中的 highway_mode / urban_mode 是自造布尔量、无来源，应改为按当前所处的 HighwayMode / UrbanMode 状态判断
- **事实**：事实成立。stm0.puml:33 逐字含 `dist_to_front<15 & highway_mode` 与 `dist_to_front<10 & urban_mode`，两个布尔名确为作者自造（NL 未给标识符）。附带说明：issue 提出的替代实现（在守卫里引用 HighwayMode/UrbanMode 是否活跃）要求碰撞避免与驾驶模式同时活跃，而本模型中二者是互斥顶层态——该替代方案本身预设并发；但本簇的主张只是「标识符无来源」，不依赖并发语义，故仍按流程判而不判越界。
- **NL**：NL 只有语境短语。NL 12 逐字 'or the front distance being less than 15 meters in highway mode or 10 meters in urban mode'——'in highway mode' / 'in urban mode' 是状语式语境限定，NL 未给标识符，也未规定该限定必须以引用状态活跃性的方式实现。要求特定实现形态属形态过度指定。
- **去重**：`0029-碰撞激活守卫标签写法被过度指定` —— 与 0029-4 同一处建模失误：stm0.puml:33 那一条融合守卫标签的写法。
- **成员**：run3/0029-claude#7

**0029-8** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 1/6 格 ｜ X1-J6

- **主张**：HighwayMode 与 UrbanMode 的互切换边没指明触发时机、也没指明可从哪些子状态切出
- **事实**：事实不成立。stm0.puml:37-38 逐字 `HighwayMode --> UrbanMode : urban_way=true` 与 `UrbanMode --> HighwayMode : high_way=true`——两条边都逐字带着触发条件，「没指明触发时机」与作者源逐字相反。「从哪些子状态可以切出」同样已由复合态级迁移语义给出（编译产物 model.fcstm:40-44、:75-79 把两条边逐子态展开），非未定义。issue 自己也写「至少方向是有的，是较轻的建模不完整」。
- **NL**：NL 11 逐字 'The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively'——NL 给出的两个条件与作者写的两条标签逐字一致，NL 义务已被完全满足，NL 也从未要求标注切出子状态。
- **去重**：`0029-模式互切换边被判为无触发` —— 单成员组：根因是 stm0.puml:37-38 两条互切换边被判为无触发/未指定，而它们逐字带着 NL 11 的条件。
- **成员**：run3/0029-claude#10


## pair 0030 — 3 簇　📄 无 NL 依据×2　❌ 假阳性×1

**0030-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 4/6 格 ｜ X1-J1

- **主张**：Autonomous 被写成内联复合状态，NL 第2句要求它以 submachine state 呈现。
- **事实**：事实成立。stm0.puml:7-13 逐字为 `state Autonomous {` / `state Navigating` / `state Parking` / `[*] --> Navigating` / … / `}`，确为内联复合状态，无任何子机引用语法。NL 的实质结构义务（该态含子态）已被满足：Navigating(:8)、Parking(:9)。
- **NL**：NL S2 逐字：'The autonomous mode has sub-states and is represented by a sub machine state.' 逐字依据存在，但 submachine state 与 composite state 在 $M=(S,E,V,Tr,A)$ 内是同一对象（M 只有层次状态，无子机引用这一区分），故被指缺陷在建模对象内不可表述；读成必须使用某种 PlantUML 语法属形态过度指定。与同 NL 组的 0000-1 同判。
- **去重**：`0030-复合状态写法被要求为子机状态语法` —— 四格同一主张，同指 stm0.puml:7 的 Autonomous 声明形态这一处争议点。
- **成员**：run1/0030-claude#1 run2/0030-claude#1 run3/0030-claude#1 run3/0030-gpt#1

**0030-2** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 2/6 格 ｜ X1-J1

- **主张**：HumanDriving 用空花括号 `state HumanDriving { }` 写成复合状态，NL 第1句要求 simple state。
- **事实**：事实不成立。stm0.puml:4-5 为 `state HumanDriving {` 与 `}`，体内为空——零子态，按 UML 定义即 simple state。编译产物 model.fcstm:9 亦为 `state HumanDriving named "HumanDriving";` 这一普通简单状态。所指内容以另一种合法 PlantUML 语法存在而被判成不存在。run2/0030-claude#5 自己写下『虽然空 body 在渲染上接近简单状态，但严格意义上它是复合状态』——后半句正是被作者源否证的那一点。
- **NL**：NL S1 逐字：'The human driving mode is represented by a simple state.' 该义务在作者源上已被满足。
- **去重**：`0030-空花括号状态被误判为复合状态` —— 两格同一主张，同指 stm0.puml:4-5 空花括号写法这一处争议点。
- **成员**：run1/0030-gpt#1 run2/0030-claude#5

**0030-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J1

- **主张**：Navigating↔Parking 之间的 Park Request / Parking Complete 是模型自行引入的、规格未定义的额外子状态与内部迁移。
- **事实**：事实成立。stm0.puml:9 `state Parking`、:11 `Navigating --> Parking : Park Request`、:12 `Parking --> Navigating : Parking Complete`；nl.txt 全文无 park / parking 的任何对应表述。
- **NL**：NL 无此禁止。NL S2 逐字只说 'The autonomous mode has sub-states'——既未枚举是哪些子态，也未给出数量，更无『只有』『恰好』一类封闭性措辞，故 NL 的子态枚举默认不封闭。合式性层亦无支撑：两态互相可达、均有出边，issue 只说『属于模型自行引入的额外行为』，未主张任何合式性后果。
- **去重**：`0030-NL未枚举的停车子状态被判为多余` —— 单成员组；根因是 stm0.puml:9/11/12 这批 Parking 相关行，与本 pair 另两簇（子机语法、空花括号）各不相同。
- **成员**：run1/0030-claude#5


## pair 0031 — 6 簇　📄 无 NL 依据×6

**0031-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J4

- **主张**：InitialState --> OperationalState : Signal Transmission Fails 的源态错了——NL 2 的「传输失败」发生在收到制动信号之后，属制动链路里的失败分支，不应是 InitialState 的平级出边
- **事实**：事实成立：stm0.puml:6 逐字为 `InitialState --> OperationalState : Signal Transmission Fails`，确与 :5 的 `InitialState --> BrakingState : Brake Signal Received` 并列为 InitialState 的两条平级出边，作者源上没有把失败分支挂在制动链路后段的任何写法。⭐ 同 NL 组旁证（md5 22e189b：0001/0011/0021/0031/0041/0051）：`InitialState --> OperationalState : Signal Transmission Fails` 这一行在 6 份作者源里**逐字完全相同**（0001:6、0011:6、0021:6、0031:6、0041:6、0051:7），无一人把它挂到 BrakingState 或别处。可见把失败读成初始态的分支是该 NL 的通行读法，而不是 0031 独有的错置。
- **NL**：NL 2 逐字：'When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state.' ⭐ 第二句的主语是 it（装置），⛔ **NL 从未给这条失败迁移指定源状态**；「制动信号传输失败」既可读成信号未送达故根本没进入 braking（源为 initial），也可读成已进入 braking 后失败。义务本身真实存在，但报告者把它钉死在「必须以 BrakingState/制动链路为源」这个 NL 并未指定的位置上。
- **去重**：`0031-失败分支被钉死在制动链路后段` —— 三格讲的是同一处：stm0.puml:6 这条失败迁移的源态，被要求从 InitialState 挪到 NL 未指定的制动链路后段。
- **成员**：run1/0031-claude#1 run2/0031-claude#1 run3/0031-claude#1

**0031-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 4/6 格 ｜ X1-J4

- **主张**：BrakingState --> InitialState : Signal Feedback Sent 绕过了 ClampingState，与 NL 3「进入制动态后转入夹紧态」的顺序矛盾，属多加的路径
- **事实**：事实成立：stm0.puml:12 逐字为 `BrakingState --> InitialState : Signal Feedback Sent`，与 :8 的 `BrakingState --> ClampingState : Entering Clamping State` 并存，BrakingState 确有两条出边。⛔ 但 run3-claude#3 附加的「非确定的可选路径」这一说不成立：两条出边的触发器不同（`Entering Clamping State` vs `Signal Feedback Sent`），由收到哪个事件决定走哪条，是正常的事件驱动分支，不是非确定性，故本簇不走合式性层。⭐ 同 NL 组旁证：`BrakingState --> InitialState : Signal Feedback Sent` 在 6 份作者源里**逐字完全相同**（0001:12、0011:12、0021:12、0031:12、0041:15、0051:13），6/6 通行；而把该返回边挂到 ClampingState 上的作者是 **0/6**。
- **NL**：NL 2 第三句逐字：'Once the signal feedback is sent, it returns to the initial state.' ⭐ 该句**未指定源状态**；NL 2 前两句点名的状态恰是 BrakingState 与 OperationalState，作者把两条返回边正挂在这两个状态上（:11、:12），是最贴字面的落法。NL 3 逐字：'After entering the braking state, the system transitions to the brake caliper clamping state.'——它给出后继，但未出现「只有」「必须先」「不得」这类排他表述来禁止 BrakingState 另有出边。义务真实存在、位置由报告者自行指定，属 N-ANCHOR 形态二。
- **去重**：`0031-反馈返回边被钉死在ClampingState上` —— 与 0031-4 同一处根因：这两簇是同一个搬迁诉求的两半——把 Signal Feedback Sent 的返回边从 BrakingState 挪到 ClampingState，而 NL 未指定该边的源状态。
- **成员**：run1/0031-claude#2 run2/0031-claude#2 run3/0031-claude#3 run3/0031-gpt#1

**0031-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J4

- **主张**：ClampingState --> InitialState : Transition Missing Feedback 是 NL 未定义的迁移与事件，且其语义与「反馈已发送」相反
- **事实**：事实成立：stm0.puml:14 逐字为 `ClampingState --> InitialState : Transition Missing Feedback`，`Transition Missing Feedback` 这个串在 NL 三句里确实一次都没出现。本簇六格无一说出合式性后果（未称任何状态不可达、死端、非确定或重名）；ClampingState 也不因此产生问题——它本就只有这一条出边。⭐ 同 NL 组旁证：NL 对「夹紧之后怎么办」完全沉默，于是 6 位作者各自补了不同的收尾边——0001:14/0011:14 补 `OperationalState --> ClampingLoseState`、0021:14 补 `ClampingState --> BrakingState : Clamping Released`、0041:11-12 补两条、0051:15 补 `ClampingState --> InitialState : Braking Complete`。⭐ 每人补的都不一样且都不在 NL 里，说明这是 NL 留白处的自由发挥区，不是 0031 独有的越界。
- **NL**：NL 三句全文只写到 'After entering the braking state, the system transitions to the brake caliper clamping state.'（NL 3）为止，对夹紧态之后的行为一字未提；NL 2 第三句 'Once the signal feedback is sent, it returns to the initial state.' 给出了一条返回条件，但未出现「只有」「恰好」「不得」这类封闭性表述，故「NL 只给了一种返回条件」不构成禁止第二条返回边的义务出处。
- **去重**：`0031-ClampingState额外返回边被读成NL禁令` —— 六格讲的是同一处：stm0.puml:14 这条作者自加的收尾边与其事件，被按「NL 未提及即为多余」读成缺陷。
- **成员**：run1/0031-claude#3 run1/0031-gpt#1 run2/0031-claude#3 run2/0031-gpt#2 run3/0031-claude#2 run3/0031-gpt#2

**0031-4** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 4/6 格 ｜ X1-J4

- **主张**：ClampingState 缺少 NL 2 要求的「Signal Feedback Sent 后返回 InitialState」这条边，制动流程的收尾应发生在夹紧态之后
- **事实**：事实成立：stm0.puml 全文 15 行里，带 `Signal Feedback Sent` 触发的返回边只有 :11（源 OperationalState）与 :12（源 BrakingState）两条，ClampingState 确无该触发的出边。⛔ 但 ClampingState 不是死端——:14 给了它一条出边，故本簇无合式性依据。⭐ 同 NL 组旁证：把 `Signal Feedback Sent` 返回边挂在 ClampingState 上的作者是 **0/6**（0001/0011/0021/0031/0041/0051 六份全都只挂在 OperationalState 与 BrakingState 上），可见「收尾应挂在夹紧态之后」是报告者的推断而非该 NL 的通行读法。
- **NL**：NL 2 第三句逐字：'Once the signal feedback is sent, it returns to the initial state.' ⭐ 该句**没有指定源状态**，也没有说这条返回必须发生在整条制动流程走完之后；NL 3 逐字 'After entering the braking state, the system transitions to the brake caliper clamping state.' 只给了 BrakingState 的后继，未把反馈返回义务转移到 ClampingState。义务真实存在，被钉死在 NL 并未指定的位置上，属 N-ANCHOR 形态二。
- **去重**：`0031-反馈返回边被钉死在ClampingState上` —— 与 0031-2 同一处根因：这两簇是同一个搬迁诉求的两半——把 Signal Feedback Sent 的返回边从 BrakingState 挪到 ClampingState，而 NL 未指定该边的源状态。
- **成员**：run1/0031-claude#4 run1/0031-gpt#2 run2/0031-gpt#1 run3/0031-claude#4

**0031-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J4

- **主张**：BrakingState --> ClampingState : Entering Clamping State 把目标状态名写成了触发事件；NL 3 描述的是进入制动态后自动转入夹紧态，该迁移应无外部触发
- **事实**：事实成立：stm0.puml:8 逐字为 `BrakingState --> ClampingState : Entering Clamping State`，触发串确实与目标态语义同名。⛔ 但不构成名字碰撞：模型里的状态标识符是 `ClampingState`（:8/:9/:14），描述行是 `Brake Caliper Clamping State`（:9），与触发串 `Entering Clamping State` 三者字面互不相同，R4.5 也据此产出独立的 `event Entering_Clamping_State`（model.fcstm:4）与 `state ClampingState`（:10），无歧义、无碰撞，故本簇无合式性依据。⭐ 同 NL 组旁证：这一行在 6 份作者源里**逐字完全相同**（0001:8、0011:8、0021:8、0031:8、0041:8、0051:9），6/6 都给这条迁移加了同名触发，无一人写成无触发的完成迁移。
- **NL**：NL 3 逐字：'After entering the braking state, the system transitions to the brake caliper clamping state.' NL 只陈述了「进入制动态之后转入夹紧态」这一顺序关系，⛔ 既未给该迁移指定任何触发事件，也未规定它必须实现为无触发的完成迁移；「应无外部触发」是报告者对实现形态的追加要求。
- **去重**：`0031-自动迁移被要求为无触发形态` —— 两格讲的是同一处：stm0.puml:8 那个触发标签，被读成必须改成无触发的完成迁移形态。
- **成员**：run1/0031-claude#5 run2/0031-claude#4

**0031-6** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J4

- **主张**：OperationalState --> InitialState : Signal Feedback Sent 缺少规格支撑——传输失败后通常无法产生正常的信号反馈
- **事实**：事实成立：stm0.puml:11 逐字为 `OperationalState --> InitialState : Signal Feedback Sent`，该边确实存在。⭐ 同 NL 组旁证：这一行在 6 份作者源里**逐字完全相同**（0001:11、0011:11、0021:11、0031:11、0041:14、0051:12），6/6 通行；本簇是全 J4 组唯一一条要求删掉它的产出。
- **NL**：⛔ 本簇的前提与 NL 逐字相反。NL 2 三句连写：'When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state.' ⭐ 「Once the signal feedback is sent, it returns to the initial state」紧跟在「proceeds to the operational state」之后，最近先行词恰是 operational state——作者把该返回边挂在 OperationalState 上是这三句最贴字面的落法。NL 既未说传输失败后不能再产生反馈，也未出现任何禁止该边存在的封闭性表述，故「缺少规格支撑」这条主张没有 NL 出处。
- **去重**：`0031-OperationalState反馈返回边被读成NL未授权` —— 单成员组：根因是把 NL 2 第三句紧邻支持的那条返回边（:11）读成 NL 未授权的多余路径。
- **成员**：run3/0031-gpt#3


## pair 0032 — 5 簇　📄 无 NL 依据×5

**0032-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J2

- **主张**：AccelerateRegion --> CruisingState : Reach Speed 的源是复合态、目标是其内部子态，属跨层迁移、形式不一致。
- **事实**：事实成立。stm0.puml:24 逐字为 AccelerateRegion --> CruisingState : Reach Speed。这在 UML 中是一条合法迁移（退出复合态后重新进入并直指 CruisingState），并非语法错误，也不产生不可达或非确定。
- **NL**：NL 3 只写「the system transitions between different substates depending on actions like accelerating, braking, or stopping」，全文未提 Reach Speed，更未规定这条边的源必须是 AcceleratingState；要求改写源锚点是 NL 未提出的形态义务。
- **去重**：`0032-迁移边挂在Region包装层被判为跨层与冗余` —— 本组两簇（0032-1 与 0032-3）指向同一批作者编辑（stm0.puml:24-26），根因同为作者把迁移挂在 Region 包装层上而被判为形态不当。
- **成员**：run1/0032-claude#5

**0032-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J2

- **主张**：缺少 Cruising 直接因 stop 回到 Idle 的返回路径，三态之间不能自由切换。
- **事实**：事实成立。CruisingState 的唯一出边是 stm0.puml:26 CruisingState --> BrakeRegion : Brake，回到 Idle 只能经 :27 BrakeRegion --> IdleRegion : Stop。
- **NL**：NL 1 只写「based on user actions, it transitions between Idle, Accelerating or Cruising, and Braking states」，NL 3 同样只给 like accelerating, braking, or stopping 的举例；NL 未逐字要求任何一对状态两两直连，issue 自己也说「规范虽未穷举全部迁移」。义务真实存在却被钉死在 NL 并未指定的 Cruising→Idle 这一对上。
- **去重**：`0032-三态间迁移被读成必须两两直连` —— 单成员组。根因是把 NL 的「在三态之间切换」读成对具体状态对的连通性义务。
- **成员**：run1/0032-claude#6

**0032-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J2

- **主张**：AccelerateRegion --> BrakeRegion : Brake 与 CruisingState --> BrakeRegion : Brake 并存，对 Cruising 而言有两条 Brake 边，冲突且冗余。
- **事实**：事实成立但无歧义。stm0.puml:25 与 :26 确实都覆盖 CruisingState 活动时的 Brake，但二者目标同为 BrakeRegion，且按 UML 内层优先规则由 :26 胜出，观察行为唯一，不产生非确定性。
- **NL**：NL 未规定迁移的书写粒度，也未禁止复合态出边与子态出边并存；要求消除这种书写冗余是形态偏好而非 NL 义务。
- **去重**：`0032-迁移边挂在Region包装层被判为跨层与冗余` —— 与 0032-1 同根：同一批 Region 层迁移（stm0.puml:24-26）被判为形态不当。
- **成员**：run2/0032-claude#5

**0032-4** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J2

- **主张**：上电后系统应直接进入 Operate，模型却把初始态设为 OffState、需 start 才进入 OperateState。
- **事实**：事实成立。stm0.puml:2 [*] --> OffState、:4 OffState --> OperateState : start。四条成员中 run2/0032-claude#7 另提「keyOff 后再 start 落到哪个子态未定义」，但它自己随即写「这本身没错」并把结论落回上电语义，故归本簇。
- **NL**：NL 1「Once the device is powered on, the system enters the Operate state」与 NL 2「The system can be turned on with the start signal and turned off with the keyOff signal」是同一件事的两种说法，作者用 start 边兑现了 NL 1。把它「修好」（令根初始边直指 OperateState）反而与 NL 2 的开关机语义冲突。分类学中同 NL 组的判例同向：NL 未要求根初始边直指 Operate。
- **去重**：`0032-上电即Operate被钉死为顶层初始边直连` —— 四条 issue 都主张顶层初始边应直指 OperateState，指向同一对作者编辑（stm0.puml:2 与 :4）。
- **成员**：run2/0032-claude#6 run2/0032-claude#7 run2/0032-gpt#1 run3/0032-gpt#1

**0032-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J2

- **主张**：事件名与 NL 的信号写法不一致（首字母大写），且 Reach Speed 未被 NL 定义。
- **事实**：事实成立。stm0.puml:4 的 start 与 :30 的 keyOff 与 NL 完全同形；:22-27 的 Accelerate / Brake / Stop / Reach Speed 为首字母大写，其中 Reach Speed 在 NL 中不出现。
- **NL**：NL 3 用「actions like accelerating, braking, or stopping」——like 表明是举例而非精确拼写规定（分类学的命名变体条目对本 pair 已有同向记载）；NL 亦无封闭性表述禁止新增触发名。要求事件标识符与 NL 散文动词逐字同形是形态义务。
- **去重**：`0032-NL散文动作词被读成事件名拼写义务` —— 单成员组。根因是把 NL 的散文动作词读成对事件标识符拼写形态的义务。
- **成员**：run3/0032-claude#6


## pair 0033 — 1 簇　📄 无 NL 依据×1

**0033-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J3

- **主张**：顶层初始迁移的触发标签 `begin` 在规范中未出现，属多报
- **事实**：事实属实：stm0.puml:2 逐字 `[*] -down-> PumpControl : begin`，NL 全文没有把 begin 用作事件名（只有 NL 1 的动词 “The system begins in the PumpControl state”）。零步核对：`begin` 只在 :2 出现一次，台账两条记录分别指 :3-5（EIS-0033-01 的三条顶层边）与 :7-20（EIS-0033-02 的三个重名块），改掉其中任何一条这个标签都仍在，故不同根，留在桶内。
- **NL**：NL 1 逐字 “The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions.”——NL 未给任何事件标识符，也没有「只有 / 恰好 / 不得」这类封闭表述。「NL 没写这个事件」不等于「NL 禁止它」，落 N-CLOSED。
- **去重**：`0033-初始迁移自造begin标签被判为多报` —— 单成员组；根因是把 NL 未给标识符读成禁止给标签。
- **成员**：run2/0033-claude#4


## pair 0034 — 3 簇　📄 无 NL 依据×2　❌ 假阳性×1

**0034-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 4/6 格 ｜ X1-J4

- **主张**：Cruising 被赋予 entry/Cruise 动作，而 NL 5 只把 Cruise 放在 Reached Cruising/Cruise 这条迁移的效果槽上，未给 Cruising 定义任何 entry 动作
- **事实**：事实成立：stm0.puml:19 逐字为 `Cruising : entry/Cruise`，NL 全文确实未把任何 entry 动作授予 Cruising。⭐ 但本条与台账已记的两条动作错置在关键处不同，故不判 V1：EIS-0034-03（DoorsClosing : entry/Accelerate，:4）之所以成立，是因为它让「关门阶段执行加速」——动作落到了 NL 明确排他的另一个状态里，是语义矛盾；EIS-0034-04（Approaching : entry/Decelerate，:23）之所以成立，核心是 NL 第 9 句逐字要求的 `Send` 输出在全模型彻底缺失。Cruising 这一条两者都不沾：Cruise 被放在「进入 Cruising 的那一刻」执行，正是 NL 5 说它发生的时刻（`Accelerating --> Cruising : Reached Cruising/Cruise`，:15），迁移效果与目标态 entry 在 UML 里是同一步内相继执行、可观察输出相同；且没有任何 NL 要求的动作因此缺失。残留的分歧只是「效果槽 vs entry 相位」这一记法位置。本簇四格无一说出合式性后果（r2g#8 最强的表述只是「可能改变行为语义」），故不走合式性层。
- **NL**：NL 5 逐字：'The system begins in the Accelerating substate, moving to the Cruising substate once cruising speed is reached, as indicated by the "Reached Cruising/Cruise" signal.' NL 只给出 `Reached Cruising/Cruise` 这一个信号串，未规定 `Cruise` 必须实现为迁移效果而不得实现为目标态的 entry 动作，也未出现「只有」「不得」这类封闭性/排他性表述来禁止 Cruising 拥有 entry 动作。
- **去重**：`0034-迁移效果与状态entry相位之别被读成禁令` —— 四格讲的是同一处：stm0.puml:19 那一个 entry 相位，被读成 NL 对 Cruise 所在槽位的强制规定。
- **成员**：run1/0034-claude#7 run2/0034-claude#9 run2/0034-gpt#8 run3/0034-claude#8

**0034-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 5/6 格 ｜ X1-J4

- **主张**：EmergencyStopping --> [*] : Obstacle Cleared 是 NL 未定义的退出路径，Obstacle Cleared 事件与「障碍清除后终止状态机」都是模型自加
- **事实**：事实成立：stm0.puml:11 逐字为 `EmergencyStopping --> [*] : Obstacle Cleared`，`Obstacle Cleared` 这个串在 NL 全文（10 句）不存在，NL 也从未描述离开 EmergencyStopping 的任何路径。⭐ 必须说明它与台账已记的 EIS-0034-06 为何不同判：那条记的是 `Approaching --> [*] : Destination Missed`（:25），成立的依据是 NL 10 逐字给出的 remain-until 义务 'The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate'——存在一条被这条边直接违反的显式 NL 义务。EmergencyStopping 侧没有任何对应义务：NL 3 只讲进入时做什么，对停留时长与后续一字未提。所以这条边落在 NL 的沉默区，而不是与 NL 冲突。本簇五格均未说出任何合式性后果（不可达/死端/非确定/名字碰撞都没提）。
- **NL**：NL 3 逐字：'When an obstacle is detected, the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal.' 这是 NL 唯一涉及 EmergencyStopping 的句子，只规定了进入条件与两个动作；NL 全文既未枚举 EmergencyStopping 的出边集合，也未出现「只有」「恰好」「不得」这类封闭性表述，故「NL 没写这条出边」不构成禁止它存在的义务出处。
- **去重**：`0034-EmergencyStopping退出路径被读成NL禁令` —— 五格讲的是同一处：stm0.puml:11 这条出边与其事件，被按「NL 未提及即为多余」读成缺陷。
- **成员**：run1/0034-claude#10 run2/0034-claude#6 run2/0034-gpt#7 run3/0034-claude#6 run3/0034-gpt#8

**0034-3** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 2/6 格 ｜ X1-J4

- **主张**：Stopping 只作为迁移目标出现，模型没有对它的任何状态声明、描述或后续行为
- **事实**：事实不成立。逐行核 stm0.puml 全文 26 行：`Stopping` 出现在 :7 `InMotion --> Stopping : Arrived/Stop, Send Arrived` 与 :24 `Approaching --> Stopping : Ready to Stop`（`EmergencyStopping` 不含独立词 `Stopping`），确无 `state Stopping` 行——⭐ 但在 PlantUML 里被迁移目标引用即构成合法的隐式状态声明，是另一种合法语法而非缺失；R4.5 按此读法产出 model.fcstm:14 `state Stopping named "Stopping";`，该状态确实进入了 $S$。至于「无后续行为/无出边」这半句：本 pair 的 `Stopping` 是 NL 指定的到站终点，NL 从未描述其后发生什么，r3c#9 自己也写「规范也未描述其内部」。
- **NL**：NL 2 逐字：'the system can either transition to the Stopping state when it arrives, indicated by the "Arrived/Stop, Send Arrived" signal, or to the EmergencyStopping state if an obstacle is detected.' 这是 NL 唯一提到 Stopping 的句子，只要求存在该目标状态与那条迁移，:7 已逐字兑现；NL 未给 Stopping 任何动作、内部结构或出边，也未要求它必须以显式 `state` 关键字声明。
- **去重**：`0034-隐式声明的Stopping被判为未定义` —— 两格讲的是同一处：把 PlantUML 中「由迁移目标隐式声明」这一合法形态判成了状态未定义。
- **成员**：run1/0034-claude#11 run3/0034-claude#9


## pair 0036 — 3 簇　📄 无 NL 依据×2　🚫 越界×1

**0036-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 2/6 格 ｜ X1-J1

- **主张**：AttackReady 是 NL 未提及的多余状态（NL 只提目标搜索、编队调整、攻击三种）。
- **事实**：事实成立。stm0.puml:20-21 `[*] --> AttackReady` 与 `AttackReady : Ready for Task Assignment`，:23/:26 以它为端点；nl.txt 无『准备任务分配』一类表述。
- **NL**：NL 无此禁止。NL 2-4 只正面点名搜索、编队调整、攻击三类行为，未使用『只有』『恰好三个状态』『不得』一类封闭性措辞，NL 的枚举默认不封闭。合式性层亦无支撑：AttackReady 在 Region2 内可达（:20 区内初始）且有出边（:23），两条 issue 也只说『属于规范外的多余建模』『并不对应规范中的任何状态』，未说出任何合式性后果。
- **去重**：`0036-NL未点名的攻击就绪状态被判为多余` —— 两格同一主张，同指 stm0.puml:20-21 这处 AttackReady 的引入。
- **成员**：run1/0036-claude#6 run3/0036-claude#5

**0036-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J1

- **主张**：UAV 数量减少只写成迁移标签里的文字，没有以变量 / 计数 / 状态属性的形式建模。
- **事实**：就『无变量』一节事实成立，就『只是文字注释』一节不成立。stm0.puml:26 逐字为 `Attack --> AttackReady : Attack Complete / UAV Count Decreased`——`/` 是 PlantUML 的触发/效果分隔符，`UAV Count Decreased` 写在效果槽里，即作者是以动作（effect）形式表达了递减，不是旁注。作者源确无任何变量声明（PlantUML 无变量声明语法，全语料作者变量 0/60），故『没有变量』属实。注意：递减在编译产物里被并进事件名 `Attack_Complete_UAV_Count_Decreased`（model.fcstm:5,18），但那是 R4.5 的损失，X1 从未见过该产物，按 §1 规则 2 不得据此判债务。
- **NL**：NL 4 逐字：'After completing the attack, the number of UAVs in the swarm decreases accordingly.'——NL 要求的是这一行为，作者已在 :26 的效果槽内逐字写出；NL 未规定它必须以一等变量/计数属性承载。把 NL 的行为要求读成一条『必须声明变量』的实现形态义务属过度指定，且该形态在作者所用记法中根本不存在。
- **去重**：`0036-数量递减被要求以变量形态声明` —— 三格同一主张，同指 stm0.puml:26 那条标签的效果槽承载形态。
- **成员**：run1/0036-claude#8 run2/0036-claude#6 run3/0036-claude#7

**0036-3** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 2/6 格 ｜ X1-J1

- **主张**：拦截→编队调整只在 Region1 内可用，Region2 的 AttackReady/Attack 被拦截时无法转入 FormationAdjustment。
- **事实**：所报违规位于正交区并发语义之内。stm0.puml 顶层有两个 `--` 分隔符（:5、:17，机械计数 2），把模型切成 region0={InitialState}、region1=Region1、region2=Region2；本簇索要的是一条从 Region2 的子态跨到 Region1 的 FormationAdjustment 的迁移，即区间同步/跨区迁移。在区感知读法下 Region1 与 Region2 同时活跃，机器无论在不在攻击流程中都处在 Region1 的某个态上、拦截随时可被处理，义务本已满足；只有把两区拍平成兄弟态之后『攻击时无法被拦截』才出现。$M=(S,E,V,Tr,A)$ 无正交区并发语义，故越界。不判 OOS-FLATTEN：此处的拍平是报告者自己对作者源所作的读法，不是 R4.5 展平的产物（X1 从未见过编译产物）。
- **NL**：NL 3 逐字：'When the UAV swarm is intercepted, it transitions to the formation adjustment state.' 边界是双向的：既不得据此说方法未能检出，也不得反过来说该模型没有并发问题——判越界即正确姿态。
- **去重**：`0036-跨正交区的拦截处理被要求` —— 两格同一主张，同指跨 stm0.puml:5/:17 两个 `--` 槽位的迁移这一处争议。
- **成员**：run1/0036-claude#9 run3/0036-claude#8


## pair 0037 — 3 簇　📄 无 NL 依据×2　🚫 越界×1

**0037-1** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 6/6 格 ｜ X1-J4

- **主张**：ActiveState 未用 `--` 分隔符建模为三个正交并发区域，三个 *CollisionRegion 只是顺序嵌套的互斥子状态容器，无法并发激活不同的避撞控制
- **事实**：事实成立：逐行核 stm0.puml 全文 33 行，无任何单独成行的 `--` 正交分隔符（:9/:16/:23 等处的 `-down->` 是箭头写法，不是分隔符）；:10-14、:17-21、:24-28 三个 `state *CollisionRegion { }` 块确是 ActiveState 内顺序声明的普通嵌套复合态，不构成正交区。⭐ 但本簇索要的内容——三个区同时活跃、不同避撞控制并发激活、进入其一时其余仍独立演化——整体位于正交区并发语义之内，而 $M=(S,E,V,Tr,A)$ 无并发语义，故按 §4.2(c) 一律越界。⚠️ 双向缄默：这既不记为方法未能检出，也不反过来声称该模型没有并发问题。
- **NL**：NL 1 逐字：'There are three region in this diagram'；NL 3 逐字：'The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.' 两句正是并发/区计数义务本身——NL 在这一点上要求的恰恰是 M 边界之外的东西，因此不是「NL 没要求」而是「这条要求不在建模对象内」。
- **去重**：`0037-三区并发激活主张` —— 六格讲的是同一处：ActiveState 下三个 Region 未构成可并发的正交区，主张内容整体落在并发语义内。
- **成员**：run1/0037-claude#1 run1/0037-gpt#1 run2/0037-claude#1 run2/0037-gpt#1 run3/0037-claude#1 run3/0037-gpt#1

**0037-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J4

- **主张**：进入 ActiveState 的触发只写了泛化的 Collision Detected，未体现 NL 2 的三类具体碰撞检测各自都能激活该子机
- **事实**：事实成立：stm0.puml:31 逐字为 `InitialState -up-> ActiveState : Collision Detected`，这是进入 ActiveState 的唯一入边，触发确为一个泛化串；`Collision Detected` 这个名字 NL 里并不存在，是作者自造的。⭐ 但三类具体检测在作者源上都逐字存在——:9 `Frontend Collision Detected`、:16 `Rear-End Collision Detected`、:23 `Pedestrian Collision Detected`——本簇三格自己也都承认这一点（r1g#3 逐字：「虽然内部有三类事件，但它们发生在 ActiveState 内的 Inactive 之后」；r3g#4 逐字：「三种具体检测事件被放在 ActiveState 内从 Inactive 出发」）。所以争的不是这三个事件在不在，而是这条 NL 义务该落在哪条边上。属 N-ANCHOR 形态二：义务真实存在，却被钉死在 NL 并未指定的位置。
- **NL**：NL 2 逐字：'This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.' NL 只说「子机在这三种检测之一发生时变为 active」，⛔ 从未提到 InitialState、从未规定要有一条顶层入边、更未规定这三个触发必须挂在哪一条迁移上；NL 全文（3 句）里没有任何两层/一层结构的规定。作者用「泛化边进入 + 内层具体检测分流」两步兑现该义务，是 NL 未排除的一种落法。
- **去重**：`0037-子机激活义务被钉死在顶层InitialState出边上` —— 三格讲的是同一处：把 NL 2 的激活义务钉死在 stm0.puml:31 这条边上，而 NL 并未指定该位置。
- **成员**：run1/0037-claude#4 run1/0037-gpt#3 run3/0037-gpt#4

**0037-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J4

- **主张**：顶层 InitialState 及其到 ActiveState 的迁移是 NL 未要求的冗余层，ActiveState 内的 Inactive 才是真正等待碰撞事件的初始子状态
- **事实**：事实成立：stm0.puml:2 `[*] -down-> InitialState`、:3 `InitialState: Initial State`、:31 `InitialState -up-> ActiveState : Collision Detected`，NL 全文（3 句）确实从未提到任何名为 InitialState 的状态。⭐ 但「NL 没写这个状态」不等于「NL 禁止它」（§4.2(a)）：本簇未说出任何合式性后果——InitialState 由 :2 的顶层初始边可达、由 :31 有出边、不与任何元素重名、不抢占别人的初始位（它就是根初始目标），issue 给出的最强表述只是「语义重复」「冗余」。⭐ 同 NL 组（md5 a53ac33：0007/0017/0027/0037/0047/0057）的主臂已有同形判例：0007-1 争议元素同为顶层 InitialState，终裁 `NO_NL_BASIS`（`N-CLOSED`），本条与其一致。
- **NL**：NL 三句全文：'There are three region in this diagram' / 'This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.' / 'The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.' NL 只对「区」给了一个计数（三个 region），对顶层状态既未枚举也未计数，更未出现「只有」「恰好」「不得」这类封闭性表述来禁止一个额外的等待态。
- **去重**：`0037-顶层InitialState被读成NL未许可的多余层` —— 单成员组：根因是把 NL 未枚举顶层状态读成禁止存在额外的顶层等待态。
- **成员**：run3/0037-claude#3


## pair 0039 — 9 簇　📄 无 NL 依据×4　❌ 假阳性×2　🚫 越界×2　✅ 真漏记×1

**0039-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 6/6 格 ｜ X1-J5

- **主张**：HighwayMode 把「退出高速」(`dist_to_exit<2`) 承载在复合态的终止伪状态 `[*]` 上，既没有显式的 exit-highway 状态/迁移，又与 NL 6 的 `auto_finished=true → FinishState` 完成语义衔接不明、易混淆。
- **事实**：事实成立，且正是作者的逐字写法。stm0.puml:16 `lane_change --> [*] : dist_to_exit<2`、:18 `cruise --> [*] : dist_to_exit<2`——两个 `[*]` 位于 `state HighwayMode {`（:10）与 `}`（:20）之间，故是 HighwayMode 的终止伪状态；:22 另写 `HighwayMode --> FinishState : auto_finished=true`。所以「退出高速经内层 [*]，而到 FinishState 另需 auto_finished=true」在作者源上确实如此，且作者源里确无任何名为 exit_hwy／exit_highway 的状态。
- **NL**：NL 无此形态义务。NL 4/5 只以散文给出行为：「it can return to cruise once the lane change is completed or **exit the highway** if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`)」——既未指定退出后的去向，也未要求存在一个具名退出状态或某种特定目标形态。NL 6「The HighwayMode ends when the system transitions to FinishState, triggered by the `auto_finished=true` condition」是肯定陈述，NL 并未写「只有 auto_finished 才能结束 HighwayMode」。本簇把 NL 的散文行为读成必须以某种结构形态实现（显式退出状态／与内层 [*] 不同的目标），属形态过度指定。作者源上此处也不构成合式性缺陷：HighwayMode 完成后仍有 :22 这条出边，非死端。
- **去重**：`0039-高速退出被承载在复合态终止伪状态` —— 六格同一主张：都指向 stm0.puml:16/:18 这批「dist_to_exit<2 → 内层 [*]」的编辑，争的是同一处建模决定——作者用复合态完成来承载 NL 的「exit the highway」。run2/0039-claude#8 的「缺少与 exit_urban 对称的显式退出子状态」是同一处决定的另一说法（其后半句「[*] 并不能自动触发 HighwayMode --> FinishState」与本簇完全同题）。
- **成员**：run1/0039-claude#2 run1/0039-gpt#2 run2/0039-claude#8 run2/0039-gpt#4 run3/0039-claude#8 run3/0039-gpt#6

**0039-2** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 5/6 格 ｜ X1-J5

- **主张**：exit_urban 没有任何出边、是死角，且未与 UrbanMode 的完成或 FinishState 衔接。
- **事实**：事实不成立。exit_urban 确实没有以它为源的边（stm0.puml 全文只有 :32 `lane_change_urban --> exit_urban : dist_to_exit<0.7` 引用它），但作者在 :38 写了 `UrbanMode --> FinishState : auto_finished=true`——该行位于 AutonomousMode 体内（:4-:39）、UrbanMode 体外（:24-:36），以复合态 UrbanMode 为源，是一条组级迁移，在 UML 语义下于 UrbanMode 的任意配置（含 exit_urban）都使能。故「exit_urban 出不去 / 没有到达 UrbanMode 完成或 FinishState 的路径」与作者源相反：退出路径以另一种合法语法（复合态出边）存在，被按逐状态出边清单判成不存在。旁证：R4.5 亦按此读法编译出 model.fcstm:64 `exit_urban -> [*] : /auto_finished_true`。另 run1/0039-gpt#5 的「exit_urban 没有定义在 UrbanMode 内部」同样为假——:32 就在 `state UrbanMode {` 的花括号内；run2/0039-claude#10 甚至自陈「虽然 UML 允许组级迁移」，随后仍据死角下结论。
- **NL**：NL 侧不救本条。NL 8 只要求「the system transitions to straight if the lane change is complete or to exit_urban if the distance to the urban exit is less than 0.7 kilometers」，NL 10 把退出义务放在 UrbanMode 整体上（"The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied"）。NL 从未要求 exit_urban 自身另有出边。
- **去重**：`0039-UrbanMode组级出边被漏算致子态被判死端` —— 两簇（exit_urban、intersection）同一根因：报告按「以该状态为源的边」逐状态清点出边，漏算了 stm0.puml:38 以复合态 UrbanMode 为源的组级迁移，于是把两个没有自身出边的子态都判成死端/无退出路径。
- **成员**：run1/0039-claude#3 run1/0039-gpt#5 run2/0039-claude#7 run2/0039-claude#10 run2/0039-gpt#5 run3/0039-gpt#5

**0039-3** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 1/6 格 ｜ X1-J5

- **主张**：intersection 子状态孤立、没有任何出边，成为死状态，也没有到 FinishState 的路径。
- **事实**：事实不成立。intersection 仅在 stm0.puml:29 `enter_urban --> intersection : intersection=true` 与 :34 `straight --> intersection : intersection=true` 作为目标出现，确无以它为源的边；但与 exit_urban 同理，:38 `UrbanMode --> FinishState : auto_finished=true` 是 UrbanMode 的组级出边，在 intersection 配置下同样使能。故 issue 逐字所说「也没有到 FinishState 的路径」与作者源相反（旁证：model.fcstm:63 `intersection -> [*] : /auto_finished_true`）。
- **NL**：NL 侧不救本条。NL 7 只给 intersection 的入口（"or intersection if it detects an intersection (`intersection=true`)"），NL 9 同样只给入口（"if the system detects an intersection, it transitions to the intersection substate"）；NL 未给 intersection 任何出边义务，退出义务由 NL 10 放在 UrbanMode 整体。
- **去重**：`0039-UrbanMode组级出边被漏算致子态被判死端` —— 两簇（exit_urban、intersection）同一根因：报告按「以该状态为源的边」逐状态清点出边，漏算了 stm0.puml:38 以复合态 UrbanMode 为源的组级迁移，于是把两个没有自身出边的子态都判成死端/无退出路径。
- **成员**：run3/0039-claude#5

**0039-4** ｜ ✅ 真漏记 ｜ `V2` ｜ 3/6 格 ｜ X1-J5

- **主张**：FinishState 只作为迁移目标出现，未被声明为状态、也不是终态伪状态，NL 所称的自主驾驶「终止」在模型上未兑现。
- **事实**：承重主张成立。stm0.puml 全文只有 :22 `HighwayMode --> FinishState : auto_finished=true` 与 :38 `UrbanMode --> FinishState : auto_finished=true` 两处引用 FinishState，且都是作为目标；作者从未写 `state FinishState`，也未把它写成 `[*]`；FinishState 没有任何以它为源的边，是吸收态；全模型不存在任何终态伪状态（唯二的 `[*] -->` 是 :2 与 :44 两条初始边），故机器永不 terminate。⚠️ 本簇混有一处弱主张：「未显式声明为状态」若读成「该元素不存在」则为假——PlantUML 由目标位置隐式声明它，编译产物 model.fcstm:77 亦有 `state FinishState`；单独看那半句只能算 FP-K。但三格的 reason 一致把承重点放在「没有将其定义为终止状态（[*]）／未以 [*] 终态表达／语义不完整」，该点在作者源上为真。
- **NL**：合式性层主张，按 §5 的 V2 不要求 NL 逐字依据。NL 6/10 只说「transitions to FinishState」，未规定它必须是 UML 终态，故本簇若按 NL 层读会落 N-FORM；但「NL 称之为终点的那个状态实际上是一个无出边的普通命名状态、机器永不终止」属终态真伪，与台账自己按 layer=wellformedness 收录的 EIS-0010-03（「命名像终态但语义不是终态」「机器永不 terminate」）完全同型——若此处不放行，就是用两把尺子量同一批产出。本 pair 台账仅 2 条（EIS-0039-01 讲 enter_hwy→lane_change 缺边，EIS-0039-02 讲 AutonomousMode 的两条外部边过度规定），均不覆盖 FinishState；:22/:38 的存在也不依赖这两条记录所指的语句，故非同根。
- **去重**：`0039-FinishState只是普通命名状态未兑现终止语义` —— 三格同一主张：都指向 stm0.puml:22/:38 这唯二引用 FinishState 的位置，说的是同一处建模失误——NL 的终点被写成一个既非终态伪状态、又无出边的普通命名状态。
- **成员**：run1/0039-claude#6 run2/0039-claude#4 run3/0039-claude#6

**0039-5** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 2/6 格 ｜ X1-J5

- **主张**：碰撞避免子系统未与 AutonomousMode 建成并行/正交区域，无法与驾驶模式并发运行。
- **事实**：所述事实（作者未用正交区）为真：作者源内无正交分隔符（`grep -cE "^\s*--\s*$" stm0.puml` = 0），碰撞避免的两个状态写在 AutonomousMode 体外、与它同级——:44 `[*] --> collision_avoidance_deactive` 与 :2 `[*] --> AutonomousMode` 是两条平行的顶层初始边，:46/:48 是两条状态间迁移。
- **NL**：NL 12/13 确实描述了碰撞避免子系统的激活与复位。但本簇索要的内容是「两者应同时活跃／应以正交区并发运行」（run1/0039-claude#7 逐字：「运行语义上无法真正与 AutonomousMode 并行」；run2/0039-claude#5 逐字：「无法表达其与 AutonomousMode 并发运行的语义」），位于正交区并发语义之内，而 paper1 的建模对象 M=(S,E,V,Tr,A) 无并发语义。按 CLAUDE.md 的双向缄默口径，判越界即正确姿态。
- **去重**：`0039-碰撞避免与驾驶模式的并发关系` —— 两簇同一根因：碰撞避免子系统与驾驶模式之间的并发关系在 M 内无表示——一簇要求把它写成正交区、一簇要求守卫跨区引用驾驶模式状态谓词，都是同一处并发语义缺口的两个说法。
- **成员**：run1/0039-claude#7 run2/0039-claude#5

**0039-6** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 3/6 格 ｜ X1-J5

- **主张**：碰撞避免激活守卫里的 `dist_to_front<15 in HighwayMode || dist_to_front<10 in UrbanMode` 是自然语言片段，未以状态谓词（如 `in(HighwayMode)`）与当前驾驶模式联动，作为守卫不可执行。
- **事实**：该文本逐字存在于 stm0.puml:46 的标签内。但「是自由文本而非形式化守卫」并不区分此处与别处：作者源全篇标签都是这种写法（:7 `high_way=true`、:14 `dist_to_front<25 && extra_lane=true`、:28 `road ahead is clear`），故本簇的可执行内容只剩「守卫应引用驾驶模式的状态谓词」这一条。
- **NL**：NL 12 本身就是散文「the front distance being less than 15 meters in highway mode or 10 meters in urban mode」，作者是逐字转写。本簇实际索要的修法是让该守卫引用驾驶模式的状态谓词（run3/0039-claude#4 逐字写「未真正引用状态谓词（例如 in(HighwayMode)）」；run2/0039-claude#6 逐字写「没有与驾驶模式所在区域进行联动/条件化」），这要求碰撞避免态与某个驾驶模式态**同时活跃**并跨区取值——正交区并发语义，在 M 之外。
- **去重**：`0039-碰撞避免与驾驶模式的并发关系` —— 两簇同一根因：碰撞避免子系统与驾驶模式之间的并发关系在 M 内无表示——一簇要求把它写成正交区、一簇要求守卫跨区引用驾驶模式状态谓词，都是同一处并发语义缺口的两个说法。
- **成员**：run1/0039-claude#8 run2/0039-claude#6 run3/0039-claude#4

**0039-7** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J5

- **主张**：straight 没有到 exit_urban 或其它退出机制的迁移。
- **事实**：事实成立。straight 的出边只有 stm0.puml:34 `straight --> intersection : intersection=true` 与 :35 `straight --> lane_change_urban : dist_to_front<15 && extra_lane=true`，确无到 exit_urban 或任何退出的边。
- **NL**：NL 9 逐字只给 straight 两个去向（「if the system detects an intersection, it transitions to the intersection substate. If the distance to the front vehicle becomes less than 15 meters ... it transitions to lane_change_urban」），NL 8 把 exit_urban 的入口只挂在 lane_change_urban 上，NL 10 把退出义务放在 UrbanMode 整体。退出义务真实存在，但被钉到 NL 从未指定的 straight 上。issue 自陈「规范第 9 条仅列出 straight -> intersection 与 straight -> lane_change_urban，故此项从规范角度看可接受」，并自行指出 `UrbanMode --> FinishState` 的组级迁移「语义上覆盖此情形，本条仅供参考」。
- **去重**：`0039-UrbanMode退出义务被钉到straight子态` —— 单成员组。根因是：NL 10 的退出义务定在 UrbanMode 整体，报告按流程完整性把它外推到 NL 未指定的 straight 子态。
- **成员**：run1/0039-claude#10

**0039-8** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J5

- **主张**：`enter_urban --> straight : road ahead is clear` 用自然语言而非布尔守卫，未形式化。
- **事实**：事实成立，逐字存在于 stm0.puml:28 `enter_urban --> straight : road ahead is clear`。
- **NL**：NL 7 原文就是散文「or straight if the road ahead is clear」——与同一句里给了标识符的 `dist_to_front<15`、`extra_lane=true`、`intersection=true` 不同，NL 对这一条件未给任何标识符或变量名。issue 自陈「规范中也未给出对应的布尔变量，模型没有明确化」。NL 只是在陈述条件语义，未规定必须以布尔变量／形式化守卫的形态实现。
- **去重**：`0039-NL散文条件被要求形式化为布尔守卫` —— 两簇同一根因：NL 对若干条件只给散文、未给标识符（road ahead is clear / lane change completed），作者原样写进标签，报告要求把它们形式化成布尔守卫；争的是同一处写法决定。
- **成员**：run2/0039-claude#11

**0039-9** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J5

- **主张**：`lane change completed` / `lane change complete` 用自然语言事件而非形式化条件，与其它守卫风格不一致。
- **事实**：事实成立，逐字存在于 stm0.puml:15 `lane_change --> cruise : lane change completed` 与 :31 `lane_change_urban --> straight : lane change complete`。
- **NL**：NL 4「it can return to cruise once the lane change is completed」与 NL 8「the system transitions to straight if the lane change is complete」都是散文，未给任何标识符。issue 自陈「不过与规范措辞（『lane change completed』）一致，仅是形式化一致性问题」——它自己承认这是形态偏好而非 NL 义务。
- **去重**：`0039-NL散文条件被要求形式化为布尔守卫` —— 两簇同一根因：NL 对若干条件只给散文、未给标识符（road ahead is clear / lane change completed），作者原样写进标签，报告要求把它们形式化成布尔守卫；争的是同一处写法决定。
- **成员**：run2/0039-claude#12


## pair 0040 — 5 簇　📄 无 NL 依据×4　✅ 真漏记×1

**0040-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J6

- **主张**：Autonomous 子机内部只有 AutoInitial 与 AutoFinal 两个状态，缺少体现自动驾驶行为分解的中间子状态，子机形同虚设
- **事实**：事实成立。stm0.puml:6-10 内只有 `[*] --> AutoInitial : Enter Autonomous Mode`、`AutoInitial --> AutoFinal : Auto Process Complete`、`AutoFinal : Auto Final State`，确实只有两个子态。两态均可达，AutoFinal 经复合态级 stm0.puml:12 可离开（model.fcstm:15 印证），无合式性后果。
- **NL**：NL 无此义务。NL 2 逐字 'The autonomous mode has sub-states and is represented by a sub machine state.'——NL 只声明「有子状态」（复数，两个即满足），全文未点名任何具体子状态标识符，也未要求子状态必须体现某种行为分解粒度。把「有子状态」读成「必须有体现行为分解的中间态」属对实现形态/丰富度的过度指定。
- **去重**：`0040-子机内容丰富度被过度指定` —— 单成员组：根因是 stm0.puml:6-10 作者只放两个子态这一处建模选择被判为不足。
- **成员**：run1/0040-claude#1

**0040-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：AutoFinal 只是普通命名状态，未用 [*]/final 标记为子机终态，因而无法作为 auto final 被引用、无法自动触发完成迁移
- **事实**：事实成立。stm0.puml:8-9 `AutoInitial --> AutoFinal : Auto Process Complete`、`AutoFinal : Auto Final State`——AutoFinal 是普通命名状态加一行描述行，Autonomous 内确无 `[*]` 终态、也无 `AutoFinal --> [*]`。但 §4.2(b) 点 1 所要求的合式性后果在此不成立：AutoFinal 可达，且经复合态级 stm0.puml:12 的 `Autonomous --> HumanDriving : human_steering_cmd || brake_pressed || in (AutoFinal)` 可离开（model.fcstm:15 `AutoFinal -> [*] : /human_steering_cmd_brake_pressed_in_AutoFinal`），整机也能终止（stm0.puml:13 `HumanDriving --> [*] : Power Off`）——不存在「机器永不终止」。零步同根核验：AutoFinal 在作者源被 :8、:9、:12 三处引用，改掉 EIS-0040-02 所指的 :12 元素仍在，故与该记录不同根。
- **NL**：NL 4 逐字含 'in (auto final)'，但这是对一个状态的指称，NL 未要求它必须以 UML final 伪状态语法实现。issue 所述的实质后果「处于 AutoFinal 也不会自动交还控制权」正是 EIS-0040-02 已逐字记录的内容（该记录 statement 原文即含此句），剩余的「应改用 [*]/final 记法」是记法形态要求。
- **去重**：`0040-AutoFinal被要求用final伪状态实现` —— 两条簇成员指向同一处：stm0.puml:8-9 把 auto final 写成普通命名状态这一处记法选择。
- **成员**：run1/0040-claude#3 run3/0040-claude#1

**0040-3** ｜ ✅ 真漏记 ｜ `V2` ｜ 1/6 格 ｜ X1-J6

- **主张**：顶层初始迁移 `[*] --> HumanDriving : Power On` 带触发事件，不符合 UML 对初始迁移的约束
- **事实**：事实成立。stm0.puml:2 逐字 `[*] --> HumanDriving : Power On`——根初始伪状态的出边带了触发。UML 2.5 §14.2.3.8 规定初始伪状态的出迁移不得带 trigger/guard；后果是上电事件到达前整机无任何活动状态（编译产物 model.fcstm:19 `[*] -> HumanDriving : /Power_On` 保留了该形态）。台账已用同一条规则记录了 stm0.puml:7 的同型违反（EIS-0040-03：'UML 初始迁移不允许带触发，这是结构与行为双重缺陷'，layer=wellformedness、无 nl_evidence），但未记录 :2 这一处。零步同根核验：两处是不同的作者编辑，改掉 :7 不会消除 :2 的触发，故不同根。
- **NL**：合式性层主张，不要求 NL 依据（BRIEF §5 V2：初始态一族）。附带说明 NL 侧：NL 3 逐字 'when power on, the system turn into human driving mode'——NL 确实要求上电进入人驾驶模式，故与 :7 的自造事件 'Enter Autonomous Mode' 不同，本处触发词有 NL 出处；但初始迁移不得带触发是形式化本身的义务，与该触发词是否来自 NL 无关（正确写法是先进入一个上电前状态再由 Power On 迁出）。
- **去重**：`0040-顶层初始迁移带触发事件` —— 单成员组：根因是 stm0.puml:2 这一处根初始迁移带触发，与台账 EIS-0040-03 同规则、不同编辑。
- **成员**：run1/0040-claude#4

**0040-4** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J6

- **主张**：AutoInitial --> AutoFinal 使用了规范未定义的事件 Auto Process Complete，属超出规范的臆造
- **事实**：事实成立。stm0.puml:8 逐字 `AutoInitial --> AutoFinal : Auto Process Complete`，NL 全文确无该事件名，也无对应描述。三条簇成员均未主张任何合式性后果（该边使 AutoFinal 可达，不制造死端或非确定）。
- **NL**：NL 无此义务，但 NL 也未禁止。NL 2 逐字只说 'The autonomous mode has sub-states'，对子机内部如何推进未作任何规定；NL 全文无「只有／恰好／不得」式的封闭或排他表述。按 BRIEF §4.2(a)：NL 没提到它 ≠ NL 禁止它，NL 的枚举默认不封闭，故「模型多出了 NL 没写的事件」本身不构成义务出处。
- **去重**：`0040-子机内部推进事件被判为规范外` —— 三条簇成员指向同一处：stm0.puml:8 这条子机内部推进边及其自造事件名。
- **成员**：run1/0040-claude#7 run2/0040-claude#5 run3/0040-claude#5

**0040-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：Autonomous 被写成就地展开子状态的复合状态，而 NL 要求用 submachine state（子机引用）表示
- **事实**：事实成立。stm0.puml:6-10 是 `state Autonomous { ... }` 就地嵌套，不是对外部独立状态机的引用。但该区分在 $M=(S,E,V,Tr,A)$ 内没有对应物：UML 明确 submachine state 与内容内联的复合状态语义等价，改成子机引用不会改变 $S/E/V/Tr/A$ 中任何一项（编译产物 model.fcstm:9-16 与内联写法完全相同）。run3/0040-gpt#2 自身亦为条件式表述「若严格要求 'sub machine state'，该表示方式不完全符合」。
- **NL**：NL 2 逐字含 'is represented by a sub machine state'。这是对图示记法的规定而非对状态机语义的规定：它索要的差别在 $M$ 内不可表达、也不改变行为，故按 BRIEF §4.2(b) 点 2 判为形态偏好（NL 在解释建模方式，被读成必须采用某种语法）。
- **去重**：`0040-复合态与子机状态的记法之争` —— 两条簇成员指向同一处：stm0.puml:6 用内联复合态而非子机引用这一处记法选择。
- **成员**：run2/0040-claude#1 run3/0040-gpt#2


## pair 0041 — 7 簇　📄 无 NL 依据×7

**0041-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J5

- **主张**：`ClampingState --> BrakingState : Brake Signal Maintained` 是 NL 未描述的多余迁移。
- **事实**：事实成立。stm0.puml:11 逐字 `ClampingState --> BrakingState : Brake Signal Maintained`，该边与该事件名确实存在，且 NL 全文没有 “maintained/保持” 一类措辞。
- **NL**：NL 无此禁止。NL 3 只逐字给出「After entering the braking state, the system transitions to the brake caliper clamping state.」，对夹紧态如何结束一字未提；NL 全文没有任何封闭性/排他性表述（无 only / exactly / must not），也没有枚举夹紧态可以有几条出边。按「NL 没提到它 ≠ NL 禁止它」，无义务出处。本簇亦未主张任何合式性后果——run2/0041-gpt#2 仅说「引入了未规定的循环行为」，而环路不是合式性缺陷。
- **去重**：`0041-夹紧态的退出行为为作者自造且被读成禁止项` —— 两簇指向同一处建模决定——作者自行设计了夹紧态如何结束（stm0.puml:11 与 :12 两条相邻出边，外加两个 NL 中不存在的事件名）；一簇争回到制动态那条、一簇争回到初始态那条，是同一处自造内容的两半。
- **成员**：run1/0041-claude#1 run1/0041-gpt#1 run2/0041-claude#1 run2/0041-gpt#2 run3/0041-claude#3 run3/0041-gpt#1

**0041-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 6/6 格 ｜ X1-J5

- **主张**：`ClampingState --> InitialState : Brake Signal Released` 是 NL 未描述的多余迁移，且其触发与 NL 的「信号反馈发出」返回条件不一致。
- **事实**：事实成立。stm0.puml:12 逐字 `ClampingState --> InitialState : Brake Signal Released`，该边与该事件名存在，NL 全文无 “released/释放” 一类措辞。
- **NL**：NL 无此禁止。NL 2 逐字「Once the signal feedback is sent, it returns to the initial state.」是一条肯定陈述，NL 并未写「返回初始态只能由信号反馈触发」。本簇的论证正是把这句单次陈述读成排他义务——run3/0041-claude#4 逐字：「规范中回到初始态的唯一路径是『信号反馈发送』（Signal Feedback Sent）」；run2/0041-gpt#3 逐字：「引入了不同于规范的返回条件」。NL 的枚举默认不封闭，计数/排他义务需 NL 明写。
- **去重**：`0041-夹紧态的退出行为为作者自造且被读成禁止项` —— 两簇指向同一处建模决定——作者自行设计了夹紧态如何结束（stm0.puml:11 与 :12 两条相邻出边，外加两个 NL 中不存在的事件名）；一簇争回到制动态那条、一簇争回到初始态那条，是同一处自造内容的两半。
- **成员**：run1/0041-claude#2 run1/0041-gpt#2 run2/0041-claude#2 run2/0041-gpt#3 run3/0041-claude#4 run3/0041-gpt#2

**0041-3** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J5

- **主张**：`Signal Transmission Fails` 的源态被放在 InitialState 上，应挂在收到制动信号之后（BrakingState / 信号处理过程）。
- **事实**：事实成立。stm0.puml:6-7 相邻两行 `InitialState --> BrakingState : Brake Signal Received` 与 `InitialState --> OperationalState : Signal Transmission Fails`，失败分支的源态确为 InitialState、且与制动信号那条并列。
- **NL**：NL 2 逐字：「When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state.」——第二句只给了触发（signal transmission fails）与去向（operational state），**没有给源态**。作者的读法（传输失败即未能到达制动态，故从初始态分出）与本簇的读法（应从制动态分出）在 NL 上都无逐字支持。义务真实存在，但被钉死在 NL 并未指定的那个位置上。
- **去重**：`0041-信号传输失败分支的源态被钉到NL未指定的位置` —— 两簇同一根因：NL 2 对「信号传输失败→运行态」只给触发与去向、不给源态，报告各自钉了一个源态——一簇说 InitialState 那条错了、一簇说缺 BrakingState 那条，指的是同一处未被 NL 指定的锚点。
- **成员**：run1/0041-claude#3 run2/0041-claude#3 run3/0041-claude#1

**0041-4** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J5

- **主张**：缺少 BrakingState → OperationalState 的失败分支（运行态应从制动信号处理路径派生）。
- **事实**：事实成立。stm0.puml 中 BrakingState 的出边只有 :8 `BrakingState --> ClampingState : Entering Clamping State` 与 :15 `BrakingState --> InitialState : Signal Feedback Sent`，确无到 OperationalState 的边。
- **NL**：同 0041-3：NL 2 第二句只给触发与去向，未给源态，故「该分支必须从 BrakingState 出发」不是 NL 义务。issue 自陈是「根据规范第2条……应从制动信号处理路径中派生」的推断。
- **去重**：`0041-信号传输失败分支的源态被钉到NL未指定的位置` —— 两簇同一根因：NL 2 对「信号传输失败→运行态」只给触发与去向、不给源态，报告各自钉了一个源态——一簇说 InitialState 那条错了、一簇说缺 BrakingState 那条，指的是同一处未被 NL 指定的锚点。
- **成员**：run3/0041-claude#2

**0041-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 4/6 格 ｜ X1-J5

- **主张**：`BrakingState --> ClampingState : Entering Clamping State` 把目标状态名当成触发事件，NL 3 描述的应是自动/无条件迁移。
- **事实**：事实成立。stm0.puml:8 的标签逐字是 `Entering Clamping State`，与 :9 的状态描述行 `ClampingState : Brake Caliper Clamping State` 指同一个目标状态，确属以目标态命名的触发。
- **NL**：NL 3 逐字「After entering the braking state, the system transitions to the brake caliper clamping state.」——NL 只说明进入制动态之后会到夹紧态，**没有为这条迁移给出任何事件名，也没有说它必须无触发**。要求写成自动/无条件迁移属形态过度指定；run2/0041-claude#5 自陈「虽然功能上等价，但表达不规范」，即它自己承认这是表达形态问题。
- **去重**：`0041-制动到夹紧的迁移被要求写成无触发形态` —— 四格同一主张：都指向 stm0.puml:8 这一条迁移的标签写法，争的是同一处建模决定——NL 未给事件名时该边该不该带触发。
- **成员**：run1/0041-claude#4 run2/0041-claude#5 run2/0041-gpt#1 run3/0041-claude#6

**0041-6** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 2/6 格 ｜ X1-J5

- **主张**：`BrakingState --> InitialState : Signal Feedback Sent` 让制动态跳过夹紧态直接回初始态，破坏 NL「制动态→夹紧态」的必经流程。
- **事实**：事实成立。stm0.puml:15 逐字 `BrakingState --> InitialState : Signal Feedback Sent`，故 BrakingState 同时有到 ClampingState（:8）与到 InitialState（:15）两条出边。
- **NL**：NL 无此排他义务。NL 3「After entering the braking state, the system transitions to the brake caliper clamping state.」是肯定陈述，NL 未写「制动态只能去夹紧态」；NL 2「Once the signal feedback is sent, it returns to the initial state.」也未限定源态。把两句合读成「制动态必经夹紧态、不得有别的出边」是把 NL 的陈述读成封闭计数/排他义务；run1/0041-gpt#3 自陈只是「规范未明确制动态也可通过该事件直接回初始态」——未明确不等于禁止。
- **去重**：`0041-制动态的反馈返回边被读成违反必经流程` —— 两格同一主张：都指向 stm0.puml:15 这一条边，说的是同一处建模决定——制动态能否不经夹紧态直接返回。
- **成员**：run1/0041-claude#5 run1/0041-gpt#3

**0041-7** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J5

- **主张**：夹紧态缺少由 `Signal Feedback Sent` 返回 InitialState 的路径（模型改用 `Brake Signal Released`）。
- **事实**：事实成立。作者在 stm0.puml:12 用 `Brake Signal Released` 承担夹紧态到初始态的返回；`Signal Feedback Sent` 只出现在 :14 与 :15，全文没有以 ClampingState 为源的该事件边。
- **NL**：NL 2「Once the signal feedback is sent, it returns to the initial state.」未指定源态，NL 3 也未说夹紧态之后发生什么。本簇的论证自陈是合理性推断而非 NL 逐字要求——run3/0041-claude#5 逐字：「最合理的信号反馈返回点应包含夹紧态」；run2/0041-claude#4 逐字：「既然规范描述制动态之后要进入夹钳夹紧态，从夹钳态返回初始态的合理触发应为『信号反馈发出』」。真实义务被钉到 NL 未指定的位置。
- **去重**：`0041-信号反馈返回边被钉到夹紧态` —— 三格同一主张：都要求把 NL 2 那条未指定源态的反馈返回义务锚到 ClampingState 上，指的是同一处锚点争议。
- **成员**：run2/0041-claude#4 run3/0041-claude#5 run3/0041-gpt#3


## pair 0042 — 1 簇　📄 无 NL 依据×1

**0042-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J3

- **主张**：Operate 内缺少 Idle --brake--> Braking 的路径，且未体现 Cruising 与 Accelerating 的区分
- **事实**：stm0.puml:7-12 共五条子态边（Idle→AcceleratingOrCruising、AcceleratingOrCruising→Idle、AcceleratingOrCruising→Braking、Braking→Idle、Braking→AcceleratingOrCruising），确无 `Idle --> Braking`——这一点属实。「Cruising 未体现」不成立：NL 1 把该状态整体称作 `Accelerating or Cruising`，作者源 :8 逐字写作 AcceleratingOrCruising。同 NL 组六个制品里有四个（0003 / 0012 / 0052 / 0042）同样没有 Idle→Braking。
- **NL**：NL 1 “based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states” 与 NL 3 “depending on actions like accelerating, braking, or stopping”——NL 只给状态集与动作举例，从未点名任何具体的状态对。义务真实存在但被钉在 NL 并未指定的 Idle→Braking 这一对上，属 N-ANCHOR 形态二。
- **去重**：`0042-子态间迁移义务被钉在Idle直接刹车` —— 单成员组；根因是把 NL 的「按用户动作在三状态间转换」读成必须覆盖某一具体状态对。
- **成员**：run1/0042-claude#2


## pair 0043 — 1 簇　📄 无 NL 依据×1

**0043-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J1

- **主张**：迁移标签上的 [Water Flow Detected] / [Methane Flow Detected] / [Water Flow Completed] / [Methane Flow Completed] / [Activation Signal] / [Deactivation Signal] 是规格未定义、模型自行发明的触发事件与守卫条件。
- **事实**：事实成立。stm0.puml:7-10 与 :15-16 逐字带这六个方括号标签；nl.txt 五句中确无任何具名事件、信号或守卫。
- **NL**：NL 无此禁止，且 NL 反过来预告了条件的存在。NL 1 逐字：'The system begins in the PumpControl state, from which it can transition to different substates **based on specific conditions**.'——NL 明说迁移基于具体条件，只是没给名字；NL 3-5 亦用 'can transition' 描述可达性而不封闭。全文无『只有』『不得引入』一类排他措辞，故 NL 的标识符清单默认不封闭，『NL 没写这个名字』不构成禁止它的出处。合式性层亦无支撑：三条 issue 均未主张任何非确定、不可达或死端后果。
- **去重**：`0043-NL未命名的守卫条件被判为模型自造` —— 三格同一主张（其一只覆盖 Region1 的四个标签、其二覆盖全部六个，属粒度差异），同为 stm0.puml:7-10/15-16 这批标签文本的来源之争。
- **成员**：run1/0043-claude#4 run2/0043-claude#3 run3/0043-claude#3


## pair 0044 — 4 簇　📄 无 NL 依据×4

**0044-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J2

- **主张**：EmergencyStopping 的动作用 do 活动表达，规范描述的是进入时的 entry 动作。
- **事实**：事实成立。stm0.puml:20 逐字为 state EmergencyStopping : do/Emergency Stop, send "Obstacle Detected"，这是一行 PlantUML 描述行，其文本以 do/ 开头。
- **NL**：NL 3 逐字「the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal」——which includes the actions 是对状态含义的说明，未规定必须以 entry 相位实现。
- **去重**：`0044-描述行相位被读成entry动作义务` —— 本组两簇（0044-1 与 0044-2）根因相同：作者用 PlantUML 描述行承载 NL 的动作说明，被读成必须改用 entry 相位。
- **成员**：run1/0044-claude#2

**0044-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J2

- **主张**：Approaching 的 Send 用 do 活动表达，应为 entry 动作。
- **事实**：事实成立。stm0.puml:10 逐字为 state Approaching : do/Send。
- **NL**：NL 9 逐字「In the Approaching substate, the system sends the "Send" signal and continues to approach the destination」——只解释状态含义，未指定动作相位。
- **去重**：`0044-描述行相位被读成entry动作义务` —— 与 0044-1 同根：同一种描述行相位偏好，只是落在另一个状态上。
- **成员**：run1/0044-claude#3

**0044-3** ｜ 📄 无 NL 依据 ｜ `N-MODAL` ｜ 2/6 格 ｜ X1-J2

- **主张**：Approaching 只有 do/Send，未表达「继续接近目的地」与「在接近期间保持在该态直到准备停止或减速」。
- **事实**：事实成立。stm0.puml:10 只有 do/Send，源内确无自循环、额外活动或保持条件。⚠️ 本子类在登记时预判 X1 上不出现，此处出现且不是断言构造问题：X1 不构造任何谓词或断言，这一强化完全发生在报告者对 NL 的读法里，与主臂 N-MODAL 那类「多道门合法解空间交集为空」的成因无关。
- **NL**：NL 9 的 continues to approach the destination 与 NL 10 的「The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate」都是定性描述，被强化为「必须建模一个持续活动或保持条件」的驻留义务；NL 未要求任何自循环、活动或不变式。
- **去重**：`0044-remains与continues被读成驻留活动义务` —— 两条 issue 指向同一处（stm0.puml:10）与同一主张：定性的 remains / continues 被读成需显式建模的驻留行为。
- **成员**：run1/0044-gpt#3 run3/0044-gpt#2

**0044-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J2

- **主张**：InMotion --> EmergencyStopping 的触发标签写成 Obstacle Detected，与状态内发送的同名信号混淆，未表达「检测到障碍物」这一触发条件。
- **事实**：事实成立但无实体缺失。stm0.puml:18 逐字为 InMotion --> EmergencyStopping : Obstacle Detected，:20 的描述行内确有 send "Obstacle Detected"，二者同名。该标签本身已表达检测语义。
- **NL**：NL 2 用散文「if an obstacle is detected」给出触发、未给任何标识符，NL 3 才给出被发送信号的引号名 "Obstacle Detected"；NL 从未要求两者在字面上区分。要求触发名与发送信号名分立是 NL 未提出的命名形态义务。
- **去重**：`0044-触发名与发送信号同名被要求字面区分` —— 两条 issue 指向同一条边（stm0.puml:18）的同一处标签，主张一致。
- **成员**：run1/0044-gpt#2 run3/0044-gpt#3


## pair 0045 — 3 簇　📄 无 NL 依据×2　❌ 假阳性×1

**0045-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J3

- **主张**：`Door Closed [zero time set]` 与 `Cooking Time Entered` 两条边的触发/守卫不对称，缺少「关门且已设时间→ReadytoCook」的对偶分支
- **事实**：事实属实：stm0.puml:19 `DoorOpenWithItem --> DoorShutWithItem : Door Closed [zero time set]` 与 :20 `DoorOpenWithItem --> ReadytoCook : Cooking Time Entered` 逐字如此，源内确无 `Door Closed [time set]` 这一分支。
- **NL**：NL 4 逐字 “From DoorOpenWithItem, the system can transition to DoorShutWithItem if the door is closed with zero time set or to ReadytoCook if cooking time is entered.”——NL 给第二条分支的条件本来就是 “if cooking time is entered”，不是「关门且已设时间」，作者写的正是 NL 的原话。要求改写成同一事件加互补守卫的对偶形态，是 NL 未提出的实现形态义务。
- **去重**：`0045-关门分支被要求与零时间守卫对偶` —— 两条簇都在要求把 :19/:20 改成按 time 值分岔的对偶守卫，是同一处形态主张。
- **成员**：run1/0045-claude#5 run3/0045-claude#5

**0045-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J3

- **主张**：DoorShut 的 Cancel 自环应写成内部迁移，外部自环会重跑 entry/exit
- **事实**：事实属实：stm0.puml:13 逐字 `DoorShut --> DoorShut : Cancel`，是一条外部自环。但 DoorShut 在源内没有任何 entry/exit 动作（:3 只有 `state "DoorShut" as DoorShut` 的别名声明），issue 自述的后果（重跑 entry/exit）在本制品上不会发生。
- **NL**：NL 1 逐字 “the system can either remain in DoorShut if a Cancel action is performed”——NL 只要求「保持在 DoorShut」，未规定用内部迁移还是外部自环这种实现形态。
- **去重**：`0045-自环被要求写成内部迁移` —— 单成员组；根因是把 NL 的行为描述读成对迁移种类（internal vs external）的义务。
- **成员**：run1/0045-claude#6

**0045-3** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 1/6 格 ｜ X1-J3

- **主张**：DoorShut 的 Cancel 自环在规范中未明确要求，疑为多余（issue 自述仅供确认）
- **事实**：该自环在作者源上逐字存在（stm0.puml:13 `DoorShut --> DoorShut : Cancel`），且它正是 NL 1 逐字要求的行为；issue 自己也写明「模型是符合的」。「规范中未明确要求」与 NL 原文逐字相反，是纯事实错误，不是义务越界。
- **NL**：NL 1 逐字 “From this state, the system can either remain in DoorShut if a Cancel action is performed or transition to the DoorOpen state when the door is opened.”——NL 明确要求该保持行为，本簇的前提与之相反。
- **去重**：`0045-Cancel自环被误报为规范外` —— 单成员组；根因是把一条 NL 逐字要求、作者也逐字写了的迁移报成疑似多余。
- **成员**：run3/0045-claude#6


## pair 0046 — 4 簇　📄 无 NL 依据×2　❌ 假阳性×1　✅ 真漏记×1

**0046-1** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 3/6 格 ｜ X1-J6

- **主张**：「UAV 数量减少」只是迁移标签里的一段文字，没有被建模为变量/可观察元素或真正的更新动作
- **事实**：事实不成立。stm0.puml:16 逐字 `Attacking --> Searching : Attack Completed / UAV Count Decreased`——`/` 之后正是 UML/PlantUML 的效果（action）槽位，作者已把「数量减少」写成迁移动作；run3/0046-claude#5 自己也承认「被写成了转移的一个 action 片段」。按 BRIEF 流程 ①「元素以描述行或动作形式存在」即判假阳性。至于「没有变量声明」：PlantUML 根本没有变量声明语法（本批 60 个制品作者变量数为 0），该形态在作者源上不可表达，不能据此说该语义未被建模。零步同根核验：无任何台账记录指向 :16。
- **NL**：NL 4 逐字 'After completing the attack, the number of UAVs in the swarm decreases accordingly.'——NL 确实点名了递减义务，而作者正是在 :16 的效果槽位逐字表达了它，故 NL 义务已被表达，主张与作者源相反。
- **去重**：`0046-UAV数量递减动作被判为未建模` —— 三条簇成员指向同一处：stm0.puml:16 那条已写在 `/` 效果槽位的递减动作被判成未建模。
- **成员**：run1/0046-claude#6 run2/0046-claude#5 run3/0046-claude#5

**0046-2** ｜ ✅ 真漏记 ｜ `V1` ｜ 1/6 格 ｜ X1-J6

- **主张**：拦截只能从 Searching 进入 FormationAdjustment，未覆盖从 Attacking 等其它状态被拦截的情形，作用域过窄
- **事实**：事实成立。stm0.puml:9 `Searching --> FormationAdjustment : Intercepted` 是全模型唯一一条 Intercepted 边；Attacking（:15-16）、FormationAdjustment（:12-13）、Idle（:4-7）均无该事件的出边，编译产物 model.fcstm:17-21 印证 SearchRegion 内仅此一条。台账三条记录（EIS-0046-01 包壳初始子态、-02 三区域计数、-03 Idle/Start Mission 过度规定）均不涉及 Intercepted 的作用域，故未记。
- **NL**：NL 3 逐字 'When the UAV swarm is intercepted, it transitions to the formation adjustment state.'——该句无任何状态前件，构成全局义务；这正是台账 EIS-0040-01 采用的同一读法（'NL 第5句断电义务只覆盖一半作用域…无状态前件，构成全局义务'）。同 NL 组的兄弟 pair 0056 亦把拦截边写在复合态级（0056 的 stm0.puml:16 `SearchState --> FormationAdjustment : Intercepted`，覆盖其全部子态），说明更宽的作用域是该 NL 的通行读法。
- **去重**：`0046-拦截义务只覆盖Searching一处作用域` —— 单成员组：根因是 stm0.puml:9 把 NL 3 的无前件全局义务只挂在 Searching 一个源态上。
- **成员**：run2/0046-claude#3

**0046-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J6

- **主张**：攻击完成后固定回到 Searching，未对「集群消耗殆尽（数量降为 0）」或「恰好任务完成」建立分支
- **事实**：两半分别核验。「未考虑任务已完成」不成立：stm0.puml:27 `SearchRegion --> MissionRegion : Mission Completed` 是复合态级出边，对 Attacking 同样生效（model.fcstm:25 `Attacking -> [*] : /Mission_Completed`）。「未对数量降为 0 建分支」在作者源上成立：stm0.puml:16 是 Attacking 唯一的区内出边，全模型无任何与数量取值相关的分支。
- **NL**：NL 无此义务。NL 4 逐字只有 'After completing the attack, the number of UAVs in the swarm decreases accordingly.'——NL 全文未出现耗尽、归零、终止条件或任何与数量取值相关的分支要求。把「数量相应减少」这一效果描述读成必须按该量分支建模，属对实现形态的过度指定。
- **去重**：`0046-数量耗尽分支被要求建模` —— 单成员组：根因是把 NL 4 的递减描述外推成必须存在按数量取值分支的迁移。
- **成员**：run2/0046-claude#8

**0046-4** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J6

- **主张**：编队调整完成后强制返回 Searching，规范并未指定调整完成后的去向，属过度补全
- **事实**：事实成立。stm0.puml:13 逐字 `FormationAdjustment --> Searching : Formation Adjusted`，NL 全文确无 'Formation Adjusted' 事件、也未描述编队调整之后的行为。issue 未主张任何合式性后果——恰恰相反，若删掉该边 FormationAdjustment 会变成区内死端。
- **NL**：NL 无此义务，但 NL 也未禁止。NL 3 逐字只说 'When the UAV swarm is intercepted, it transitions to the formation adjustment state.'，对其后的返回路径缄默；NL 全文无「只有／恰好／不得」式封闭表述。按 BRIEF §4.2(a)，「模型多出了 NL 没要求的迁移/事件」默认不构成义务出处。
- **去重**：`0046-编队调整返回边被判为规范外补全` —— 单成员组：根因是 stm0.puml:13 这条 NL 未指定的返回边被判为过度补全。
- **成员**：run3/0046-claude#6


## pair 0049 — 9 簇　📄 无 NL 依据×5　❌ 假阳性×2　🚫 越界×1　✅ 真漏记×1

**0049-1** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 6/6 格 ｜ X1-J1

- **主张**：exit_urban 是死状态：进入后没有任何出向迁移，既到不了 FinishState 也离不开 UrbanMode。
- **事实**：事实不成立。exit_urban 在 stm0.puml 只出现于 :25 `lane_change_urban --> exit_urban : dist_to_exit<0.7`，确无以 exit_urban 为字面源的边；但作者写了两条复合态出边覆盖它——:34 `UrbanMode --> HighwayMode : high_way=true` 与 :43 `AutonomousMode --> FinishState : auto_finished=true`。按 UML 复合态出边语义，源为复合态的迁移对其全部子态生效，exit_urban 位于 UrbanMode ⊂ AutonomousMode 之内，故两条都可从它触发。编译产物 model.fcstm:63、68 把它们下沉成 `exit_urban -> [*] : /high_way_true` 与 `exit_urban -> [*] : /auto_finished_true`，可作 pyfcstm 同读法的旁证。所指的出路以复合态出边这一合法语法存在，被判成不存在。另：PlantUML 中迁移目标名即隐式声明状态，run1-gpt#4『exit_urban 未声明为状态』同属此误（model.fcstm:47 有 `state exit_urban`）。
- **NL**：NL 8 逐字：'the system transitions ... to exit_urban if the distance to the urban exit is less than 0.7 kilometers'；NL 10 逐字：'The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied.'——NL 10 要的那条退出路径正由 :43 提供，义务已满足。
- **去重**：`0049-复合态外层出边未被计入导致误判死端` —— 六格同一主张，同为一处根因：报告者未把 stm0.puml:34/:43 的复合态出边下推到 UrbanMode 的子态。
- **成员**：run1/0049-claude#5 run1/0049-gpt#4 run2/0049-claude#5 run2/0049-gpt#3 run3/0049-claude#7 run3/0049-gpt#4

**0049-2** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 4/6 格 ｜ X1-J1

- **主张**：`enter_hwy --> cruise : dist_to_front>=25` 用了规范未写明的守卫，属模型自造条件（并使 dist_to_front<25 且 extra_lane=false 时无路可走）。
- **事实**：事实成立。stm0.puml:10 逐字 `enter_hwy --> cruise : dist_to_front>=25`；nl.txt 全文只出现 `dist_to_front<25`，无 `>=25`。附带主张（<25 且 extra_lane=false 时 enter_hwy 无使能出边）亦属实，但那不是合式性缺陷：enter_hwy 可达、有两条出边、两条守卫互斥不构成非确定，且 :33/:43 的复合态出边随时可离开。
- **NL**：NL 无此禁止。NL 3 逐字：'can transition to cruise or lane_change based on the distance to the front vehicle (`dist_to_front<25`) and the availability of an extra lane (`extra_lane=true`)'——NL 明确把这对分支的判据指派给 dist_to_front，只逐字给出了其中一支的写法；作者用其补集 `>=25` 承载另一支，正是对 NL 所指派判据的实例化。把 NL 逐字给出的条件串读成封闭清单（凡不逐字出现即为自造）是把枚举读成排他义务。
- **去重**：`0049-NL未写出的巡航守卫补集被判为自造条件` —— 四格同一主张，同指 stm0.puml:10 那条守卫的来源之争。
- **成员**：run1/0049-claude#6 run2/0049-claude#1 run3/0049-claude#1 run3/0049-gpt#3

**0049-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J1

- **主张**：`intersection --> straight : road_clear` 这条迁移规范从未描述，是模型自行添加的。
- **事实**：事实成立。stm0.puml:29 逐字 `intersection --> straight : road_clear`；nl.txt 的 NL 7-9 只描述进入 intersection（NL 7 'or intersection if it detects an intersection'、NL 9 'if the system detects an intersection, it transitions to the intersection substate'），确未描述如何离开 intersection。
- **NL**：NL 无此禁止。NL 7-10 未使用『只有』『不得』一类封闭性措辞，故 NL 的迁移枚举默认不封闭。合式性层不但不支持这三条 issue，反而与之相反：若照其主张删除该边，intersection 在 UrbanMode 内就只剩 :30 一条完成边，可用性反而下降；三条 issue 也均未主张任何合式性后果。
- **去重**：`0049-路口回直行这条NL未描述的迁移被判为多余` —— 三格同一主张，同指 stm0.puml:29 这一条边的存在与否。
- **成员**：run1/0049-claude#7 run2/0049-claude#6 run3/0049-claude#6

**0049-4** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 2/6 格 ｜ X1-J1

- **主张**：`road_clear` 是模型自造的信号/条件名，规范只用散文说 'the road ahead is clear'，未给出该符号。
- **事实**：事实成立。stm0.puml:22 `enter_urban --> straight : road_clear`、:29 `intersection --> straight : road_clear`；nl.txt 中不存在字符串 road_clear。
- **NL**：NL 无此禁止。NL 7 逐字含 'or straight if the road ahead is clear'——条件内容 NL 逐字给了，只是没给标识符。NL 未规定守卫必须逐字复用 NL 中出现过的符号，也无『不得引入新名』一类措辞；按该 issue 的读法，任何命名都不可能通过。这是把 NL 的标识符清单读成封闭清单。
- **去重**：`0049-散文条件被作者命名后其标识符被判为自造` —— 两格同一主张，同指 road_clear 这个名字的来源；与 0049-3（争的是 :29 那条边该不该存在）不是同一处争议点。
- **成员**：run1/0049-claude#8 run3/0049-claude#5

**0049-5** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 3/6 格 ｜ X1-J1

- **主张**：CollisionAvoidance 与 AutonomousMode 未建成并发/正交区域，二者不能同时活跃，与 NL 12-13 的并行子系统语义不符。
- **事实**：主张的内容位于正交区并发语义之内。三条 issue 索要的正是『两者同时活跃』（run1-claude#9『二者的并发关系及生命周期不明确』、run2-claude#7『二者应为正交并发区域』、run3-claude#12『导致两者不能同时处于活动状态』），并明确提出用 `--` 分区来实现。作者源确无 `--`（机械计数 `grep -cE "^[[:space:]]*--[[:space:]]*$" stm0.puml` = 0），CollisionAvoidance 是 :37 的顶层兄弟态。$M=(S,E,V,Tr,A)$ 无正交区并发语义，该主张无法在建模对象内表述，越界。不判 OOS-FLATTEN：作者源本就没有区可供展平。
- **NL**：NL 12-13 逐字描述碰撞避免子系统的两态与切换条件，但把它读成一条『必须与驾驶模式并行活跃』的结构义务即落在 M 之外。边界双向：不得据此说方法未能检出，也不得反过来说该模型没有并发问题。
- **去重**：`0049-碰撞规避与自动驾驶的并行区语义` —— 三格同一主张，同指 stm0.puml:37 CollisionAvoidance 与 AutonomousMode 的并行关系这一处争议。
- **成员**：run1/0049-claude#9 run2/0049-claude#7 run3/0049-claude#12

**0049-6** ｜ ✅ 真漏记 ｜ `V2` ｜ 1/6 格 ｜ X1-J1

- **主张**：CollisionAvoidance 永远不会被激活：顶层初始迁移只进入 AutonomousMode，该子机没有任何入边。
- **事实**：事实成立且属合式性缺陷。stm0.puml:2 `[*] --> AutonomousMode` 是全文唯一的顶层初始边；`CollisionAvoidance` 全文只出现一次，即 :37 的 `state CollisionAvoidance {` 声明，无任何以它为目标的迁移；作者源无 `--`（机械计数 = 0），故它不是并发区而是顺序兄弟态。结论：collision_avoidance_deactive / collision_avoidance_active 及 :39/:40 两条边在任何执行下都不可达。编译产物 model.fcstm:83-89 同样只有 `[*] -> AutonomousMode`（:91），无入边，可作旁证。⭐ 与 0049-5 的分界：那一簇索要的是并发语义（在 M 外），本簇断言的是可达性（在 M 内，且在作者自己所用的记法下同样成立——PlantUML 不加 `--` 的兄弟态本就不并行）。
- **NL**：按合式性层收录，不要求 NL 逐字依据（可达性属形式化自身的义务，与台账 32 条 wellformedness 记录同一口径）。NL 12 逐字：'The collision avoidance system is initially in the collision_avoidance_deactive state.'——该初始态在制品中永不被进入。本 pair 台账 3 条（EIS-0049-01 dist_to_exit 合并、-02 FinishState 层次归属、-03 冗余完成边）无一覆盖 CollisionAvoidance；零步同根判据：CollisionAvoidance 在作者源只被 :37 引用，三条台账记录无一引用它，改掉它们该子机仍在。
- **去重**：`0049-碰撞避免子机无入边不可达` —— 单成员组；根因是 stm0.puml:2 唯一初始边与 :37 顶层兄弟态之间缺入边，与 0049-5 的并发主张分属两类（verdict 不同，不得共用 key）。
- **成员**：run1/0049-gpt#5

**0049-7** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J1

- **主张**：HighwayMode↔UrbanMode 的动态切换未指定进入对端后落到哪个子态、也未保留上下文，与 NL 11 的 'seamless' 不符。
- **事实**：事实成立。stm0.puml:33 `HighwayMode --> UrbanMode : urban_way=true`、:34 `UrbanMode --> HighwayMode : high_way=true` 均为复合态到复合态的迁移，模型内无任何历史伪状态（`[H]`/`[H*]`）与显式进入点，故每次切换都落到对端的默认初始子态（:9 enter_hwy / :20 enter_urban）。
- **NL**：NL 无此义务。NL 11 逐字：'The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively, facilitating seamless mode shifts during the drive.'——'facilitating seamless mode shifts' 是对该迁移用途的定性说明，NL 未规定必须以历史伪状态或显式进入点实现；两条 issue 自己也承认（『规范未明确是否要重入初始子状态』『实现意图与规范无缝切换要求可能存在差距』）。把定性说明读成一条实现形态义务属过度指定。注：此处不判 N-MODAL——被强化出的不是时序不变式，而是一个结构记法义务。
- **去重**：`0049-无缝切换被读成历史或进入点义务` —— 两格同一主张，同指 stm0.puml:33-34 这对模式切换边的进入点语义。
- **成员**：run1/0049-claude#11 run3/0049-claude#10

**0049-8** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J1

- **主张**：守卫里的 in(HighwayMode) / in(UrbanMode) 是跨区域引用，不是标准 UML 守卫写法，语义不明。
- **事实**：事实成立（该文本确实存在）：stm0.puml:39 含 `(dist_to_front<15 && in(HighwayMode))` 与 `(dist_to_front<10 && in(UrbanMode))`。但『跨区域引用』这一定性与作者源不符：全文无 `--`（机械计数 = 0），根本不存在区，CollisionAvoidance 与 AutonomousMode 是顺序兄弟态；in(...) 是状态成员谓词，UML/OCL 侧有 inState/oclInState 的对应物，并非无对应的记法。issue 自己定性为『属于表述问题』。
- **NL**：NL 无此义务，且 NL 反过来支持该写法。NL 12 逐字：'the front distance being less than 15 meters **in highway mode** or 10 meters **in urban mode**'——NL 自己就是用『处于某模式』这一状态成员条件表述的，作者的 in(HighwayMode)/in(UrbanMode) 是对它的逐字对译。NL 未规定守卫必须用哪种语法承载，读成语法义务属形态过度指定。
- **去重**：`0049-状态成员守卫写法被判为非标准` —— 单成员组；根因是 stm0.puml:39 守卫中 in(...) 的记法形态，与 0049-7（模式切换的进入点）虽同判 N-FORM 但不是同一处争议点。
- **成员**：run3/0049-claude#11

**0049-9** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 2/6 格 ｜ X1-J1

- **主张**：碰撞规避在高速模式下以 dist_to_front<15 激活，与高速主逻辑的 25 米换道阈值不一致。
- **事实**：事实不成立，且两条 issue 自己已经撤回。stm0.puml:39 逐字含 `(dist_to_front<15 && in(HighwayMode)) || (dist_to_front<10 && in(UrbanMode))`，与 NL 12 的 15 米/10 米逐字一致，不存在所指的不一致。run1-gpt#3 自述『该项经复核与规格第12条一致，因此不是不符；不应报告为问题』；run2-gpt#4 自述『若严格只按第12条，则此项不算不符』。所报内容与作者源及 NL 逐字相反，属纯事实错误，既非命名变体也非形态问题。
- **NL**：NL 12 逐字：'the front distance being less than 15 meters in highway mode or 10 meters in urban mode'。NL 3/5 的 `dist_to_front<25` 是换道判据，与碰撞规避激活判据是两回事，NL 从未要求两者取同一阈值。
- **去重**：`0049-碰撞规避前距阈值被误报为不一致` —— 两格同一主张，同指 stm0.puml:39 那两个阈值与 NL 12 的一致性。
- **成员**：run1/0049-gpt#3 run2/0049-gpt#4


## pair 0050 — 6 簇　📄 无 NL 依据×4　❌ 假阳性×2

**0050-1** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 6/6 格 ｜ X1-J2

- **主张**：AutonomousMode 是普通内联复合状态，未使用 submachine state（子机引用）记法。
- **事实**：不成立。stm0.puml:8-13 以 state AutonomousMode { [*] --> SubState1 ... } 声明了带三个子态的层次状态，NL 2 所要求的「自治模式有子状态」已以合法的复合态语法存在。UML 中 submachine state 与其展开的复合状态语义等价，paper1 的建模对象 M=(S,E,V,Tr,A) 根本不区分二者（model.fcstm:8-25 也只得到一个普通层次状态）。所指内容以另一种合法形式存在，被判成缺失。
- **NL**：NL 2 逐字「The autonomous mode has sub-states and is represented by a sub machine state」——它要求的语义内容（有子态的自治模式）已兑现；submachine 与 composite 的差别是图形记法层面的封装方式，在 M 内无对应区分。
- **去重**：`0050-复合态被判为未使用submachine记法` —— 六条 issue 指向同一处声明（stm0.puml:8-13），主张一致：应改用子机引用记法。
- **成员**：run1/0050-claude#1 run1/0050-gpt#2 run2/0050-claude#1 run2/0050-gpt#1 run3/0050-claude#1 run3/0050-gpt#2

**0050-2** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 2/6 格 ｜ X1-J2

- **主张**：HumanDrivingMode 写成带空状态体的 state X { }，不是简单状态。
- **事实**：不成立。stm0.puml:5-6 的 state HumanDrivingMode { } 体内为空，没有任何子态或区域，因此它就是一个简单状态；model.fcstm:7 也只得到一行叶状态 state HumanDrivingMode named "HumanDrivingMode";。空花括号是合法且语义等价的写法。
- **NL**：NL 1 逐字「The human driving mode is represented by a simple state」——该义务已满足，NL 未规定必须省略花括号。
- **去重**：`0050-空状态体被判为不是简单状态` —— 两条 issue 指向同一处声明（stm0.puml:5-6），主张一致。
- **成员**：run1/0050-gpt#1 run3/0050-gpt#1

**0050-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J2

- **主张**：AutonomousMode 内部子态用 SubState1/2/3 占位命名，相邻迁移无任何触发或守卫，缺乏可执行语义。
- **事实**：事实成立。stm0.puml:9-12 为 [*] --> SubState1、SubState1 --> SubState2、SubState2 --> SubState3、SubState3 --> [*]，四条边均无触发与守卫（UML 中即完成迁移，合法），三个子态名确为占位式。成员未指出任何合式性后果——可达性、死端、非确定在此均不违反。
- **NL**：NL 2 只写「The autonomous mode has sub-states」，既未给出任何子态名字，也未给出子态之间的迁移或其触发；要求有意义的命名与显式触发是 NL 未提出的形态义务。
- **去重**：`0050-子机内部占位命名与无触发迁移被判为语义不完备` —— 两条 issue 指向同一批边（stm0.puml:9-12），主张一致。
- **成员**：run2/0050-claude#2 run3/0050-claude#3

**0050-4** ｜ 📄 无 NL 依据 ｜ `N-KIND` ｜ 3/6 格 ｜ X1-J2

- **主张**：HumanDrivingMode --> AutonomousMode 只有守卫 [front_distance > 10]，缺少触发事件。
- **事实**：事实成立。stm0.puml:15 逐字为 HumanDrivingMode --> AutonomousMode : [front_distance > 10]，只有方括号守卫。
- **NL**：NL 逐字写「when front_distance > 10, auto transport to autonomous state」——NL 把它称为条件（一个比较式），属 M 的 V / 守卫层，作者按条件建模正是对的范畴；索要一个额外的触发事件是把条件当事件的范畴错置。两名成员自己也承认「作为条件驱动迁移可以只有守卫」。
- **去重**：`0050-NL的条件被索要成额外触发事件` —— 三条 issue 指向同一条边（stm0.puml:15），主张一致。
- **成员**：run1/0050-claude#4 run2/0050-claude#5 run3/0050-claude#4

**0050-5** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J2

- **主张**：Power Off 写成两条分别从 HumanDrivingMode 与 AutonomousMode 出发的边，未用全局 / 超状态统一表达，对子态的覆盖语义不明。
- **事实**：事实成立但无覆盖缺口。stm0.puml:19-20 确为两条边；其中 AutonomousMode --> [*] : Power Off 是复合态出边，按 UML 对 SubState1/2/3 全部生效（model.fcstm:20-22 逐个下沉为三条）。成员自己也承认「虽功能等价」「标准 UML 中对所有子状态生效」。
- **NL**：NL 5 只写「when power off, it will transit to final state」，未规定用几条边，也未要求超状态或全局迁移写法。
- **去重**：`0050-PowerOff写成两条出边被判为覆盖不明` —— 三条 issue 指向同一对边（stm0.puml:19-20），主张一致。
- **成员**：run1/0050-claude#5 run2/0050-claude#6 run3/0050-claude#5

**0050-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J2

- **主张**：顶层初始迁移 [*] --> HumanDrivingMode : Power On 带了触发事件，UML 中初始迁移不允许带触发。
- **事实**：事实成立。stm0.puml:3 逐字为 [*] --> HumanDrivingMode : Power On。但这不构成 M 内的合式性问题：目标形式化接受带触发的初始边（model.fcstm:28 保留为 [*] -> HumanDrivingMode : /Power_On;），初始态存在、唯一、可达。
- **NL**：NL 3 逐字「when power on, the system turn into human driving mode」——作者正是用这条边兑现的；把 Power On 降级为注释反而会丢掉 NL 3 的条件。所引「初始迁移不能带触发」是 UML 图形记法约束，既不是 NL 义务，也不是 M 的合式性要求。
- **去重**：`0050-初始边上的PowerOn触发被判为记法不合法` —— 两条 issue 指向同一条边（stm0.puml:3），主张一致。
- **成员**：run1/0050-claude#6 run2/0050-claude#7


## pair 0051 — 7 簇　📄 无 NL 依据×7

**0051-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J5

- **主张**：`Signal Transmission Fails` 的源态被放在 InitialState 上，应挂在收到制动信号之后。
- **事实**：事实成立。stm0.puml:6-7 相邻两行 `InitialState --> BrakingState : Brake Signal Received` 与 `InitialState --> OperationalState : Signal Transmission Fails`，失败分支源态确为 InitialState。
- **NL**：NL 2 逐字：「When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state.」——第二句只给触发与去向，**未给源态**。issue 自陈「该失败迁移的源状态**更合理地**应是 BrakingState」（run3/0051-claude#1），即依据是合理性推断而非 NL 逐字。义务真实存在但被钉到 NL 未指定的位置。
- **去重**：`0051-信号传输失败分支的源态被钉到NL未指定的位置` —— 两簇同一根因：NL 2 对「信号传输失败→运行态」只给触发与去向、不给源态，报告各自钉了一个源态——一簇说 InitialState 那条错、一簇说缺 BrakingState 那条。
- **成员**：run1/0051-claude#1 run2/0051-claude#1 run3/0051-claude#1

**0051-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 1/6 格 ｜ X1-J5

- **主张**：BrakingState 缺少在信号传输失败时迁移到 OperationalState 的路径。
- **事实**：事实成立。stm0.puml 中 BrakingState 的出边只有 :9 `BrakingState --> ClampingState : Entering Clamping State` 与 :13 `BrakingState --> InitialState : Signal Feedback Sent`，确无到 OperationalState 的边。
- **NL**：同 0051-1：NL 2 第二句未给源态，「该分支必须从 BrakingState 出发」不是 NL 义务。
- **去重**：`0051-信号传输失败分支的源态被钉到NL未指定的位置` —— 两簇同一根因：NL 2 对「信号传输失败→运行态」只给触发与去向、不给源态，报告各自钉了一个源态——一簇说 InitialState 那条错、一簇说缺 BrakingState 那条。
- **成员**：run2/0051-claude#2

**0051-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 5/6 格 ｜ X1-J5

- **主张**：`BrakingState --> InitialState : Signal Feedback Sent` 是多余/不一致的边，会绕过 NL 3 要求的夹紧态。
- **事实**：事实成立。stm0.puml:13 逐字 `BrakingState --> InitialState : Signal Feedback Sent`，故 BrakingState 同时有到 ClampingState（:9）与到 InitialState（:13）两条出边。
- **NL**：NL 无此排他义务。NL 3「After entering the braking state, the system transitions to the brake caliper clamping state.」是肯定陈述，NL 未写「制动态的后继只能是夹紧态」；NL 2 的反馈返回句也未限定源态。本簇正是把这两句读成排他——run3/0051-claude#2 逐字：「说明 BrakingState 的后继应当只有 ClampingState」；run1/0051-gpt#1 逐字：「规格没有说明处于 BrakingState 时可以因『Signal Feedback Sent』直接返回 InitialState」——没说明不等于禁止。
- **去重**：`0051-制动态的反馈返回边被读成绕过必经流程` —— 五格同一主张：都指向 stm0.puml:13 这一条边，说的是同一处建模决定——制动态能否不经夹紧态直接返回初始态。
- **成员**：run1/0051-claude#3 run1/0051-gpt#1 run2/0051-claude#3 run3/0051-claude#2 run3/0051-gpt#1

**0051-4** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 5/6 格 ｜ X1-J5

- **主张**：`ClampingState --> InitialState : Braking Complete` 这条迁移与 `Braking Complete` 事件都是 NL 未描述的额外内容。
- **事实**：事实成立。stm0.puml:15 逐字 `ClampingState --> InitialState : Braking Complete`，该边与该事件名存在，NL 全文无 “braking complete/制动完成” 一类措辞。
- **NL**：NL 无此禁止。NL 3 只说「After entering the braking state, the system transitions to the brake caliper clamping state.」，对夹紧态如何结束一字未提；NL 全文没有任何封闭性/排他性表述。issue 的依据一律是「规范没有描述/没有规定」（run1/0051-gpt#2 逐字：「该转移属于模型中额外引入的行为，无法从给定自然语言规格中得到支持」），即把「NL 没写」当成「NL 禁止」。
- **去重**：`0051-夹紧态的完成退出边为作者自造且被读成禁止项` —— 五格同一主张：都指向 stm0.puml:15 这一条边及其自造事件名，争的是同一处建模决定——作者自行设计了夹紧态的结束方式。
- **成员**：run1/0051-claude#2 run1/0051-gpt#2 run2/0051-gpt#2 run3/0051-claude#3 run3/0051-gpt#2

**0051-5** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 2/6 格 ｜ X1-J5

- **主张**：夹紧态返回初始态的触发应统一为 `Signal Feedback Sent`，而不是 `Braking Complete`；模型缺少 ClampingState 上的信号反馈返回。
- **事实**：事实成立。stm0.puml:15 的触发确为 `Braking Complete`；`Signal Feedback Sent` 只出现在 :12（OperationalState→InitialState）与 :13（BrakingState→InitialState），没有以 ClampingState 为源的那一条。
- **NL**：NL 2「Once the signal feedback is sent, it returns to the initial state.」未指定源态，NL 也没有要求所有返回初始态的边共用同一触发。本簇的依据是流程推断——run2/0051-gpt#1 逐字：「因此实际制动路径上的后续状态是 ClampingState。若『信号反馈发送后返回初始状态』用于完成该流程，则模型应能在制动钳夹紧状态……返回初始状态」。真实义务被钉到 NL 未指定的位置。
- **去重**：`0051-信号反馈返回边被钉到夹紧态` —— 两格同一主张：都要求把 NL 2 那条未指定源态的反馈返回义务锚到 ClampingState 上。
- **成员**：run2/0051-claude#4 run2/0051-gpt#1

**0051-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J5

- **主张**：`BrakingState --> ClampingState : Entering Clamping State` 把目标状态名当触发事件，NL 3 描述的应是自动/无条件迁移。
- **事实**：事实成立。stm0.puml:9 的标签逐字是 `Entering Clamping State`，与 :10 的描述行 `ClampingState : Brake Caliper Clamping State` 指同一目标状态。
- **NL**：NL 3「After entering the braking state, the system transitions to the brake caliper clamping state.」未为该迁移给出任何事件名，也未要求它无触发。run3/0051-claude#4 自陈「这本身应表现为一个自动/无条件的迁移，**或**以物理上『开始夹紧』之类的事件表述」——两种形态都由报告者补出，NL 未指定。属形态过度指定。
- **去重**：`0051-制动到夹紧的迁移被要求写成无触发形态` —— 三格同一主张：都指向 stm0.puml:9 这条迁移的标签写法。
- **成员**：run1/0051-claude#5 run2/0051-claude#5 run3/0051-claude#4

**0051-7** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J5

- **主张**：`OperationalState --> InitialState : Signal Feedback Sent` 把 NL 的反馈返回事件复用到运行态返回路径，属对 NL 未明确内容的推断。
- **事实**：事实成立。stm0.puml:12 逐字 `OperationalState --> InitialState : Signal Feedback Sent`，该边与该复用确实存在。
- **NL**：NL 反而最支持这条边。NL 2 三句相邻：「……If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state.」——反馈返回句紧接运行态句，作者的写法是最直接的读法；NL 未把该句限定给任何一条路径，也未禁止运行态使用它。本簇（issue 逐字：「规范说……是描述收到制动信号那条主线的收尾。对 OperationalState……规范并未明确说明用同一『Signal Feedback Sent』事件触发」）是把 NL 的单次陈述读成只属于某一条路径的排他义务。
- **去重**：`0051-运行态的反馈返回边被读成NL未授权` —— 单成员组。根因是：NL 2 那句无源态限定的反馈返回被读成只归属制动主线，于是作者把它用在运行态返回上被判为无依据。
- **成员**：run1/0051-claude#4


## pair 0052 — 3 簇　📄 无 NL 依据×3

**0052-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 4/6 格 ｜ X1-J6

- **主张**：模型引入了规范未提及的 shutdown 事件与 Off --> [*] 终止迁移
- **事实**：事实成立。stm0.puml:15 逐字 `Off --> [*] : shutdown`，NL 全文确无 shutdown 一词，也未描述系统的终止路径。该边带触发，不构成无触发完成迁移（与 0012 的 `Off --> Terminate` 不同型），四条簇成员亦未主张任何合式性后果（Off 仍可经 :4 的 start 迁出）。
- **NL**：NL 无此义务，但 NL 也未禁止。NL 2 逐字 'The system can be turned on with the `start` signal and turned off with the `keyOff` signal.'——只列举了两个信号，未出现「只有／仅／不得」等封闭或排他表述。按 BRIEF §4.2(a)，NL 的枚举默认不封闭，「NL 没写 shutdown」本身不构成义务出处。
- **去重**：`0052-shutdown终止边被判为规范外` —— 四条簇成员指向同一处：stm0.puml:15 这条 NL 未提及的终止边及其 shutdown 事件。
- **成员**：run1/0052-claude#1 run2/0052-claude#2 run3/0052-claude#1 run3/0052-gpt#1

**0052-2** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 5/6 格 ｜ X1-J6

- **主张**：上电后模型先停在 Off、须收到 start 才进 Operate，与「一旦上电即进入 Operate」不符（含「start 应对应通电动作」这一变体）
- **事实**：事实成立。stm0.puml:3-4 逐字 `[*] --> Off`、`Off --> Operate : start`，根初始边确实指向 Off 而非 Operate。无合式性后果：Off 与 Operate 均可达，Off 的出边都带触发。
- **NL**：NL 义务真实存在但未指定落点。NL 1 逐字 'Once the device is powered on, the system enters the `Operate` state'，NL 2 逐字 'The system can be turned on with the `start` signal'——两句把上电与 start 描述为同一开机动作，NL 从未要求根初始边直指 Operate。同 NL 组的兄弟 pair 0012 作者写法完全相同（0012 的 stm0.puml:2-3 `[*] --> Off`、`Off --> Operate : start`），且该 pair 台账 EIS-0012-01 在 statement 里把它逐字称作「NL 第 1、2 句要求的 start→Operate」，即把这一结构当作 NL 的正确实现。本形态与分类学的 N-ANCHOR 判例 0022-2（'NL 未要求根初始边直指 Operate'）同型。
- **去重**：`0052-根初始边被要求直指Operate` —— 六条簇成员（含把它换框架成「start 语义与通电不等价」的 run2/0052-claude#4）指向同一处：stm0.puml:3-4 的上电入口结构。
- **成员**：run1/0052-claude#2 run1/0052-gpt#1 run2/0052-claude#1 run2/0052-claude#4 run2/0052-gpt#1 run3/0052-claude#2

**0052-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J6

- **主张**：Braking 只能经 stop 回 Idle，缺少 accelerate 回到 Accelerating_or_Cruising 的迁移
- **事实**：事实成立。stm0.puml:8-11 给出 Operate 内的全部四条子态迁移：`Idle --> Accelerating_or_Cruising : accelerate`、`Accelerating_or_Cruising --> Braking : brake`、`Braking --> Idle : stop`、`Accelerating_or_Cruising --> Idle : stop`，Braking 确实只有一条出边。三个子态均可达且均有出边，无合式性后果。
- **NL**：NL 无此义务。NL 3 逐字 'the system transitions between different substates depending on actions like accelerating, braking, or stopping'——`like` 明示举例；NL 1 也只是列出三个子态。NL 从未点名 Braking 下的 accelerate 这条边，issue 诉诸的是「现实驾驶语义」与「规范隐含的对称性」。把不封闭的动作/状态枚举读成必须完备的切换关系，属把枚举升格为结构义务。
- **去重**：`0052-子状态切换关系被读成完整图` —— 三条簇成员指向同一处：stm0.puml:8-11 作者给出的子态迁移集合被判为覆盖不全。
- **成员**：run1/0052-claude#3 run2/0052-claude#3 run3/0052-claude#3


## pair 0054 — 7 簇　📄 无 NL 依据×6　✅ 真漏记×1

**0054-1** ｜ ✅ 真漏记 ｜ `V1` ｜ 3/6 格 ｜ X1-J6

- **主张**：InMotion --> EmergencyStopping 只写了守卫 [obstacle detected]、没有触发事件，该迁移在 UML 语义下不会被触发
- **事实**：事实成立。stm0.puml:15 逐字 `InMotion --> EmergencyStopping : [obstacle detected]`——方括号是 UML 的守卫槽位，该边无 trigger，因而是一条带守卫的完成迁移；而 InMotion（:4-11）内没有任何终态，复合态永不完成，故该边永不触发、EmergencyStopping 不可达。run1/0054-claude#1 与 run2/0054-claude#2 都自己说出了这一后果（'在标准 UML 语义下不会被触发'、'会使该转换永远不会自动触发'）。对照：作者在同文件 :13/:14 的其它外层迁移都写了触发词，唯独此条落进守卫槽。台账本 pair 0 条记录；同类「作者把内容放进错误的记法槽位」在台账中是被收录的缺陷型（EIS-0056-02 逐字：'递减被写在 UML 的 guard 槽位 [...] 而不是 effect 槽位 /…本例是作者把动作放进了错误的记法槽位'）。注意编译产物 model.fcstm:7 把整串当成了 event（`_obstacle_detected named "[obstacle detected]"`），那是 R4.5 的宽容读法，不影响作者源上的事实。
- **NL**：NL 2 逐字 'or to the EmergencyStopping state if an obstacle is detected'，NL 3 逐字 'When an obstacle is detected, the system enters the EmergencyStopping state'——NL 两处点名该迁移及其起因，属 NL 层逐字义务（非统称词、非语境状语、非语义注解）；一条永不触发的边不满足该义务。
- **去重**：`0054-障碍检测被写进守卫槽位而非触发` —— 三条簇成员指向同一处：stm0.puml:15 把障碍检测放进守卫槽位、致该迁移无触发这一处建模失误。
- **成员**：run1/0054-claude#1 run2/0054-claude#2 run3/0054-claude#1

**0054-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J6

- **主张**：EmergencyStopping 的 Emergency Stop 与 Send Obstacle Detected 写成 do/ 持续活动，应为 entry 一次性动作
- **事实**：事实成立。stm0.puml:17-18 逐字 `EmergencyStopping : do/Emergency Stop`、`EmergencyStopping : do/Send Obstacle Detected`，确为 do 相位（编译产物 model.fcstm:30-31 投影为 `during abstract`）。两个动作都在，争的只是相位。
- **NL**：NL 未规定相位。NL 3 逐字 'the system enters the EmergencyStopping state, which includes the actions "Emergency Stop" and sends the "Obstacle Detected" signal.'——'which includes…' 是对状态含义的同位说明，未规定必须以 entry 相位实现。反证：分类学在讨论 0014-4 时把本 pair 的这一行当作参考意图的正例逐字引用（'对照 0054:18 作者写 `do/Send Obstacle Detected`…该输出动作在 M 内可表达且是参考意图'），即 do/ 形态本身被认可。
- **去重**：`0054-紧急停止动作相位被要求改为entry` —— 四条簇成员指向同一处：stm0.puml:17-18 两行动作的相位选择（do 而非 entry）。
- **成员**：run1/0054-claude#2 run2/0054-claude#1 run3/0054-claude#2 run3/0054-claude#3

**0054-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：Approaching 的 do/Send 把「发送 Send 信号」建成持续活动，应为一次性发送动作（且信号名 Send 过于模糊）
- **事实**：事实成立。stm0.puml:10 逐字 `Approaching : do/Send`（编译产物 model.fcstm:14 `during abstract Send`）。动作在，争的是相位与命名。
- **NL**：NL 未规定相位与命名。NL 9 逐字 'In the Approaching substate, the system sends the "Send" signal and continues to approach the destination.'——NL 自己就用 "Send" 作信号名，作者是照抄；NL 未说该发送必须以 entry 相位实现。与 0054-2 同型：NL 在解释状态含义，被读成相位实现义务。
- **去重**：`0054-Approaching发送动作相位被要求改为entry` —— 两条簇成员指向同一处：stm0.puml:10 这一行的相位与命名选择。
- **成员**：run1/0054-claude#3 run3/0054-claude#4

**0054-4** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：Approaching 只建了 do/Send，未把「继续接近目的地」建成任何动作/活动/状态语义
- **事实**：事实成立。stm0.puml:10 是 Approaching 的唯一行为行，除 do/Send 外确无其它动作或活动。Approaching 可达（:8、:9 两条入边），并可经 InMotion 级 :14/:15 离开，无合式性后果。
- **NL**：NL 无此义务。NL 9 后半句 'and continues to approach the destination' 是对 Approaching 状态含义的说明（该状态本就叫 Approaching），不是第二个动作义务；NL 未给该行为任何信号名或动作名。把状态语义说明读成必须另建一个动作，属相位/形态过度指定。
- **去重**：`0054-接近行为被要求另建动作` —— 两条簇成员指向同一处：stm0.puml:10 只写 do/Send，未为「继续接近」另建动作。
- **成员**：run1/0054-gpt#1 run2/0054-gpt#2

**0054-5** ｜ 📄 无 NL 依据 ｜ `N-MODAL` ｜ 3/6 格 ｜ X1-J6

- **主张**：Approaching 未用自循环/内部迁移/守卫表达「保持在该状态直到准备停止或减速」
- **事实**：事实成立但无缺陷。stm0.puml:10 之外 Approaching 无自循环、无内部迁移、无退出守卫；其退出由 InMotion 级 :14 `InMotion --> Stopping : Arrived/Stop, Send Arrived` 与 :15 承担（run2/0054-gpt#1 自己也点出了这一点）。UML 状态默认驻留至有使能迁移，run3/0054-gpt#1 亦承认「虽然 UML 状态默认会保持」，故不需要额外元素来表达驻留。说明为什么本条不是断言构造问题：X1 侧无谓词、无 invariant 族、无 `release=false` 之类构造，产出直接来自模型阅读，是报告者自己把 NL 的定性表述强化成必须显式建模的驻留条件。
- **NL**：NL 10 逐字 'The system remains in the Approaching substate while nearing the destination, until it is ready to stop or decelerate.'——'remains … until' 是定性描述，NL 未要求把它落成自循环、内部迁移或守卫；把 remains 强化为必须显式表达的驻留约束正是本子类的形态。
- **去重**：`0054-remains被读成显式驻留条件` —— 三条簇成员指向同一处：Approaching 未显式表达 NL 10 的 remains/until 条件。
- **成员**：run1/0054-gpt#2 run2/0054-gpt#1 run3/0054-gpt#1

**0054-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：Stopping 只是被引用的目标态，既无声明与动作、也无后续迁移，是悬空目标
- **事实**：分两半核验。「未定义/无声明」不成立：PlantUML 中被迁移引用即声明，stm0.puml:14 引入的 Stopping 是一个正规状态（编译产物 model.fcstm:28 `state Stopping named "Stopping"`）。「无动作、无后续迁移」成立：作者未给它任何 entry/do 行为，也未写出边。run2/0054-claude#3 自己也写「这本身不算严格不符…与 EmergencyStopping 有动作说明形成不对等的结构」，即以对称性/完整度作为理由。
- **NL**：NL 无此义务。NL 2 逐字只把 Stopping 作为到达目标点名（'transition to the Stopping state when it arrives'），NL 1-10 全文未描述 Stopping 的内部行为、退出条件或后续路径（NL 描述的行程到停车为止）。要求「目的状态应至少显式定义并给出退出/后续路径」是建模完整度偏好。
- **去重**：`0054-Stopping被要求显式声明与后续路径` —— 两条簇成员指向同一处：stm0.puml:14 引入的 Stopping 未被显式声明/未给后续路径。
- **成员**：run2/0054-claude#3 run3/0054-claude#5

**0054-7** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J6

- **主张**：`Arrived/Stop, Send Arrived` 标签中逗号分隔的两个动作未被显式区分为两个独立动作
- **事实**：事实成立。stm0.puml:14 逐字 `InMotion --> Stopping : Arrived/Stop, Send Arrived`，两段效果 'Stop' 与 'Send Arrived' 未被拆成两个可分别引用的动作（编译产物 model.fcstm:6 把整串收进一个 event 的 named 串）。issue 自己也指出「模型直接照抄」规范原文。
- **NL**：NL 未给可拆分的标识符。NL 2 逐字把它作为一个整体信号名给出：'indicated by the "Arrived/Stop, Send Arrived" signal'——引号内整串就是 NL 提供的全部文本，NL 未把 Stop 与 Send Arrived 声明为两个独立动作。要求模型把 NL 的单一信号串拆成两个显式动作，属对表达形态的过度指定。
- **去重**：`0054-到站标签的两段效果被要求拆开` —— 单成员组：根因是 stm0.puml:14 照抄 NL 的单一信号串这一处写法。
- **成员**：run3/0054-claude#6


## pair 0055 — 2 簇　📄 无 NL 依据×1　❌ 假阳性×1

**0055-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J3

- **主张**：`Door Closed [time = 0]` 守卫覆盖不全——缺少 time≠0 时关门的路径，且 time 的来源未定义
- **事实**：事实属实：stm0.puml:12 `DoorOpenWithItem --> DoorShutWithItem : Door Closed [time = 0]` 与 :13 `DoorOpenWithItem --> ReadytoCook : Enter Cooking Time` 逐字如此，源内确无 `Door Closed [time > 0]` 分支；「time 未被声明」也属实，但 PlantUML 无变量声明语法，该串在 M 内只能作为标签文本存在（投影为 model.fcstm:7 `event Door_Closed_time_0`）。
- **NL**：NL 4 逐字 “…the system can transition to DoorShutWithItem if the door is closed with zero time set or to ReadytoCook if cooking time is entered.”——NL 的第二分支条件就是「已输入烹饪时间」，不是「关门且时间非零」；NL 从未要求把关门事件按 time 值做完备分支，也未要求 time 是一个被声明的量。
- **去重**：`0055-关门守卫被要求覆盖非零时间分支` —— 三条簇都在要求 :12 的守卫按 time 值补全分支，是同一处形态主张。
- **成员**：run1/0055-claude#5 run2/0055-claude#5 run3/0055-claude#5

**0055-2** ｜ ❌ 假阳性 ｜ `FP-H` ｜ 1/6 格 ｜ X1-J3

- **主张**：DoorShut 的 Cancel 自转移在规范中并非明确必需，备注为潜在冗余
- **事实**：该自环在作者源上逐字存在（stm0.puml:5 `DoorShut --> DoorShut : Cancel`），且正是 NL 1 逐字要求的行为；issue 自述「属于模型忠实翻译；此项非不符」。「并非明确必需 / 潜在冗余」与 NL 原文逐字相反，是纯事实错误。
- **NL**：NL 1 逐字 “the system can either remain in DoorShut if a Cancel action is performed”。
- **去重**：`0055-Cancel自环被误报为潜在冗余` —— 单成员组；根因是把一条 NL 逐字要求、作者也逐字写了的迁移报成潜在冗余。
- **成员**：run1/0055-claude#6


## pair 0056 — 5 簇　📄 无 NL 依据×5

**0056-1** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 3/6 格 ｜ X1-J6

- **主张**：Area1→Area2→Area3→Area1 被建成无触发的固定单向环，NL 未规定切换顺序，也未说明切换依据；无触发意味着会自发立即发生
- **事实**：事实成立。stm0.puml:7-9 逐字 `Area1 --> Area2`、`Area2 --> Area3`、`Area3 --> Area1`，三条均无标签。本条不越界：三个 Area 同属 `--` 之前的区 0，主张讲的是该区内部的普通迁移写法，与并发语义无关（BRIEF §4.2(c) 的例外）。为什么不升格为合式性层：issue 说出的后果只是「立即自发发生」，不属 §4.2(a) 列出的合式性后果（不可达、死端、非确定、抢占初始、名字碰撞）——三个 Area 均可达、均有出边、每态区内仅一条无触发出边故不非确定；在 pyfcstm 的周期语义下它表现为每周期轮转一格。真正会构成缺陷的后果（无触发完成迁移按声明顺序优先，可能抢占 Area* 上 Intercepted / Task Assignment Received / Mission Complete 的出边）四条成员无一说出，按纪律不得替它补论证。
- **NL**：NL 无此义务。NL 2 逐字 'the UAV swarm continuously performs target search tasks, during which it operates within three different state areas.'——NL 只说在三个状态区域内运行，既未规定切换顺序、方向，也未规定切换由什么触发。把 NL 对区域的枚举读成「不得规定顺序」或「必须给出触发」都是从 NL 的沉默推导出的义务。
- **去重**：`0056-区域轮转顺序与无触发写法被判为规范外` —— 四条簇成员指向同一处：stm0.puml:7-9 三条无标签轮转边的写法。
- **成员**：run1/0056-claude#2 run2/0056-claude#2 run3/0056-claude#2 run3/0056-claude#3

**0056-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J6

- **主张**：编队调整完成后返回 SearchState 会从 [*] 重新进入 Area1 与 NoIntercept，丢失原先的搜索区域上下文
- **事实**：事实成立。stm0.puml:17 `FormationAdjustment --> SearchState : Adjustment Complete` 指向复合态边界，而 SearchState 的两条默认入口是 :6 `[*] --> Area1` 与 :11 `[*] --> NoIntercept`，无历史伪状态，故返回确实重置到 Area1/NoIntercept。重置本身不构成合式性缺陷：默认进入点是明确定义的。
- **NL**：NL 无此义务。NL 3 逐字只说 'When the UAV swarm is intercepted, it transitions to the formation adjustment state.'，对调整完成后应回到哪个区域缄默；run1/0056-claude#3 自己也承认「规范没有明确说返回后要重置搜索进度，但更自然的解释是继续搜索」。把「继续搜索」的自然解读升格为必须保留区域上下文（历史伪状态）的实现义务，属形态过度指定——历史伪状态亦不属 $M=(S,E,V,Tr,A)$。
- **去重**：`0056-返回SearchState要求保留区域上下文` —— 两条簇成员指向同一处：stm0.puml:17 返回边配合 :6/:11 默认入口导致的上下文重置。
- **成员**：run1/0056-claude#3 run3/0056-claude#4

**0056-3** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 1/6 格 ｜ X1-J6

- **主张**：FormationAdjustment 无条件返回 SearchState，Adjustment Complete 事件与该返回逻辑都是规范未提及的
- **事实**：事实成立。stm0.puml:17 逐字 `FormationAdjustment --> SearchState : Adjustment Complete`，NL 全文确无 'Adjustment Complete' 一词，也未描述编队调整之后的行为。issue 未主张任何合式性后果——反之若无该边，FormationAdjustment 会成为死端。
- **NL**：NL 无此义务，但 NL 也未禁止。NL 3 只规定进入编队调整状态，对其后缄默；NL 全文无「只有／恰好／不得」式封闭表述。按 BRIEF §4.2(a)，NL 没写 ≠ NL 禁止。
- **去重**：`0056-编队调整返回边被判为规范外` —— 单成员组：根因是 stm0.puml:17 这条 NL 未提及的返回边及其自造事件名（与 0056-2 同一行、但主张的是该边不该存在，另立根因）。
- **成员**：run2/0056-claude#3

**0056-4** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 3/6 格 ｜ X1-J6

- **主张**：Mission Complete 的终止边只挂在 SearchState 上，处于 AttackState 或 FormationAdjustment 时任务完成无法结束
- **事实**：事实成立。stm0.puml:22 `SearchState --> [*] : Mission Complete` 是全模型唯一一条 Mission Complete 边；FormationAdjustment（:16-17）与 AttackState（:19-20）确无该事件的出边（编译产物 model.fcstm:38-45 印证两态各只有一条返回 SearchState 的边）。
- **NL**：NL 义务真实存在但落点未被指定。NL 2 逐字 'Before the mission is completed, the UAV swarm continuously performs target search tasks'——这是对搜索期的时间框定从句，NL 全文没有任何「任务完成时应终止」的独立义务句（对照 EIS-0040-01 所依据的 NL 'when power off, it will transit to final state' 那种无前件的显式义务句，本 NL 并不存在）。作者已在 :22 给出终止路径；把它同时钉在 NL 从未点名的 AttackState / FormationAdjustment 上属义务锚点外推。
- **去重**：`0056-任务完成终止边被要求覆盖全部状态` —— 三条簇成员指向同一处：stm0.puml:22 终止边的作用域。
- **成员**：run1/0056-claude#5 run2/0056-claude#6 run3/0056-claude#7

**0056-5** ｜ 📄 无 NL 依据 ｜ `N-CTX` ｜ 3/6 格 ｜ X1-J6

- **主张**：Task Assignment Received 只从 SearchState 触发进入 AttackState，未覆盖「飞行期间」的其它状态（如 FormationAdjustment）
- **事实**：事实成立。stm0.puml:19 `SearchState --> AttackState : Task Assignment Received` 是唯一一条该事件的边，FormationAdjustment 处收到任务分配确无迁移。三条成员均为条件式表述（'若 FormationAdjustment 也属于飞行过程的一部分'）。
- **NL**：NL 依据是语境状语。NL 4 逐字 'During flight, if task assignment information is received, it enters the attack state.'——'During flight' 是状语背景：整台机器全程处于飞行，NL 中不存在与之对立的非飞行上下文，NL 也从未把 flight 作为被操作的对象或状态点名（分类学正是以这同一句作为 N-CTX 的判例）。把该状语读成「所有飞行期状态都必须有此出边」的作用域义务，等于凭状语背景造出一个 NL 未给的范围。
- **去重**：`0056-飞行期间状语被读成任务分配的作用域义务` —— 三条簇成员指向同一处：stm0.puml:19 任务分配边的作用域。
- **成员**：run2/0056-claude#5 run2/0056-gpt#2 run3/0056-gpt#2


## pair 0057 — 2 簇　📄 无 NL 依据×2

**0057-1** ｜ 📄 无 NL 依据 ｜ `N-ANCHOR` ｜ 6/6 格 ｜ X1-J5

- **主张**：进入 CA 的激活触发是一个泛化事件 `Possible collision detected`，未对齐 NL 2 逐字并列的三类检测（frontend / rear-end / pedestrian）。
- **事实**：事实成立。stm0.puml:22 `[*] --> CA : Possible collision detected` 是唯一进入 CA 的边，标签确为单一泛化名。但三类检测事件在作者源里逐字存在，只是挂在各区内部：:5 `FCIdle --> FCActive : Frontend collision detected`、:11 `RCIdle --> RCActive : Rear-end collision detected`、:17 `PCIdle --> PCActive : Pedestrian collision detected`。
- **NL**：NL 2 逐字：「This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.」——散文 or 并列三种情形、未给任何标识符，也未规定这三者必须挂在哪条边上。义务（三类检测使避撞被激活）真实存在，且作者已用三个逐字命名的检测事件在各区内部兑现（分类学对 `0057-6` 的 FP-N 裁定亦确认「制品已声明 `Frontend_collision_detected` —— 正是 NL 2 对应的独立检测事件」）；本簇把该义务钉死在 NL 从未指定的顶层入口边 `[*] --> CA` 上，故落 N-ANCHOR 形态二。⚠️ 同 NL 组的 0017 / 0047（各 8 簇）被主臂判 `N-SPLIT-PROSE`，本簇不沿用该子类：其定义前提是「报告者必须自造分型名、造名空间无上界」，而 0057 的三个分型名由作者自己写出（run2/0057-claude#2 直接引用作者的事件名），该前提在此不成立。
- **去重**：`0057-三类检测的激活义务被钉到顶层入口边` —— 六格同一主张：都指向 stm0.puml:22 这一条入口边的标签，争的是同一处建模决定——NL 2 的三类检测该不该出现在 CA 的激活边上。
- **成员**：run1/0057-claude#3 run1/0057-gpt#2 run2/0057-claude#2 run2/0057-gpt#2 run3/0057-claude#2 run3/0057-gpt#2

**0057-2** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J5

- **主张**：FCActive / RCActive / PCActive 没有 entry/do 动作或输出来体现「碰撞避免控制」，控制只停留在命名上。
- **事实**：事实成立。stm0.puml:2-20 全文没有任何动作语法（无 `entry/`、`do/`、`during`、`/` 效果槽），FCActive（:5-6）、RCActive（:11-12）、PCActive（:17-18）只有名字与进出边。
- **NL**：NL 3 逐字「The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.」——这是在说明各区允许并发激活不同的控制，属语义说明；NL 未规定这些控制必须以状态动作（entry/do/输出）的形态落地。issue 自陈「模型中的 Active 状态没有任何 entry/do 动作或输出来体现相应的避免控制，仅是命名上暗示」，索要的正是一种实现形态。⚠️ 本簇不判越界：它讲的是区内部一个与并发无关的普通形态主张，不依赖任何「多态同时活跃」的读法。
- **去重**：`0057-避撞控制被要求以状态动作形态表达` —— 单成员组。根因是：NL 3 用名词 controls 概括三个 Active 态承载的行为，报告把这一语义说明读成必须以状态动作形态实现。
- **成员**：run2/0057-claude#3


## pair 0059 — 11 簇　📄 无 NL 依据×5　✅ 真漏记×3　❌ 假阳性×2　🚫 越界×1

**0059-1** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J1

- **主张**：HighwayMode↔UrbanMode 的模式切换未指明源子状态与进入对端后的初始子态，与 NL 11 的 'seamless' 不符、会丢失上下文。
- **事实**：事实成立（无历史机制）：stm0.puml:30 `HighwayMode --> UrbanMode : [urban_way=true]`、:31 `UrbanMode --> HighwayMode : [high_way=true]` 是复合态到复合态迁移，模型内无历史伪状态，进入对端即落到 :11 enter_hwy / :20 enter_urban。附带说法『未说明在任意子状态都可以触发』（run2-claude#9）与作者源不符——复合态出边按 UML 语义对全部子态生效（编译产物 model.fcstm:27-30、50-54 把它下沉到每个子态，可作旁证）。
- **NL**：NL 无此义务。NL 11 逐字：'facilitating seamless mode shifts during the drive'——定性说明，未规定必须以历史伪状态或显式进入点实现；run3-claude#4 自己也写『虽然 PlantUML 默认会进入 [*]』。把定性说明读成结构记法义务属形态过度指定。与同 NL 组的 0049-7 同判。
- **去重**：`0059-无缝切换被读成历史或进入点义务` —— 三格同一主张，同指 stm0.puml:30-31 这对模式切换边的进入点语义。
- **成员**：run1/0059-claude#2 run2/0059-claude#9 run3/0059-claude#4

**0059-2** ｜ ✅ 真漏记 ｜ `V2` ｜ 3/6 格 ｜ X1-J1

- **主张**：FinishState 只作为迁移目标出现，既没有 state 声明、也没有终态标记 [*] 与出边，语义上不成其为结束状态。
- **事实**：核心事实成立且属合式性缺陷。FinishState 在 stm0.puml 全文只出现两次，均在 AutonomousMode 体内作目标：:33 `HighwayMode --> FinishState : [auto_finished=true]`、:34 `UrbanMode --> FinishState : [auto_finished=true]`；无任何以它为源的边，AutonomousMode 层级亦无出边可下推（:3 之后再无以 AutonomousMode 为源的迁移）。故它是一个普通命名状态而非终态伪状态，且是吸收态——机器一旦完成自动驾驶就永远停在那里，不会真正 terminate。编译产物 model.fcstm:62 亦为 `state FinishState named "FinishState";` 且无出边。⚠️ 需澄清一点：三条 issue 中『未用 state 关键字声明』这半句不成立——PlantUML 中迁移目标名即隐式声明；成立并承重的是『没有 [*] 终态标记 / 没有出边』这一半（三条 issue 均提到 [*] 终态标记缺失，run3-claude#7 更逐字写出『没有出边』）。台账对同一形状已有先例：EIS-0000-01 逐字记『FinalState 只是普通命名状态、无出边，模型永远不会真正 terminate』，属 layer=wellformedness。
- **NL**：按合式性层收录，不要求 NL 逐字依据（终态真伪、死端属形式化自身的义务）。NL 6 逐字：'The HighwayMode ends when the system transitions to FinishState'；NL 10 逐字：'The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied.'——NL 两处都把 FinishState 立为终结点。本 pair 台账仅 1 条（EIS-0059-01，讲 enter_hwy--&gt;lane_change 分支缺失），零步同根判据：FinishState 只被 :33/:34 引用，该台账记录引用的是 :12 一带，改掉它 FinishState 仍在——不同根。
- **去重**：`0059-完成态是普通命名吸收态而非终态` —— 三格同一主张，同指 stm0.puml:33-34 所指向的 FinishState 的性质这一处争议。
- **成员**：run1/0059-claude#3 run2/0059-claude#3 run3/0059-claude#7

**0059-3** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 3/6 格 ｜ X1-J1

- **主张**：碰撞避免守卫用的 in_highway / in_urban 是模型自造的布尔标志，未与 HighwayMode / UrbanMode 状态建立任何关联，无法真正表达『取决于当前所处模式』。
- **事实**：事实成立。stm0.puml:39 含 `[dist_to_front<15 && in_highway]` 与 `[dist_to_front<10 && in_urban]`；`in_highway` / `in_urban` 在全文仅此一处出现，无任何 entry/exit 赋值，也未与 :10 HighwayMode、:19 UrbanMode 建立形式关联。
- **NL**：NL 要求的区分已被表达，残余诉求无 NL 出处。NL 12 逐字：'the front distance being less than 15 meters in highway mode or 10 meters in urban mode'——它要求的是激活阈值随模式而异，作者在 :39 用两个各带模式限定词的析取支逐字兑现了这一区分。残余的诉求是那两个限定词必须被『形式绑定』（声明为变量、或写成 in(HighwayMode)、或由 entry/exit 赋值）——PlantUML 守卫标签是不透明自由文本、全语料作者变量 0/60，NL 也从未规定绑定机制，故这是对实现形态的过度指定。旁证：同 NL 组的 0049 作者写 in(HighwayMode)、本 pair 作者写 in_highway，两种写法在各自 pair 的台账里都未被记为缺陷。
- **去重**：`0059-模式限定词被要求形式绑定` —— 三格同一主张，同指 stm0.puml:39 那两个模式限定词的承载形态。
- **成员**：run1/0059-claude#4 run2/0059-claude#7 run3/0059-claude#5

**0059-4** ｜ 🚫 越界 ｜ `OOS-CONC` ｜ 3/6 格 ｜ X1-J1

- **主张**：CollisionAvoidanceSystem 未与 AutonomousMode 建成并发/正交区域，二者不能同时活跃。
- **事实**：主张的内容位于正交区并发语义之内。三条 issue 索要的正是同时活跃与 `--` 分区（run1-claude#5『缺少并行区域（--）或正交组合语义，导致两者不能同时活跃』、run2-claude#6『没有在同一并发容器中作为正交区域（如 --）声明』、run3-claude#6『导致两者不能同时处于活动状态』）。作者源确无 `--`（机械计数 = 0），CollisionAvoidanceSystem 是 :37 的顶层兄弟态。$M=(S,E,V,Tr,A)$ 无正交区并发语义，越界。不判 OOS-FLATTEN：作者源本就没有区可供展平。
- **NL**：NL 12-13 逐字描述碰撞避免子系统的两态与切换条件，但把它读成一条『必须与驾驶模式并行活跃』的结构义务即落在 M 之外。边界双向：既不得记为方法未能检出，也不得反过来说该模型没有并发问题。
- **去重**：`0059-碰撞规避与自动驾驶的并行区语义` —— 三格同一主张，同指 stm0.puml:37 CollisionAvoidanceSystem 与 AutonomousMode 的并行关系。
- **成员**：run1/0059-claude#5 run2/0059-claude#6 run3/0059-claude#6

**0059-5** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 3/6 格 ｜ X1-J1

- **主张**：exit_hwy 与 exit_urban 是死端：没有到 FinishState、也没有退出复合态的任何后继迁移。
- **事实**：事实不成立。exit_hwy 只出现于 :15/:16 作目标，exit_urban 只出现于 :25 作目标，确无以它们为字面源的边；但作者写了四条复合态出边覆盖它们——:30 `HighwayMode --> UrbanMode`、:31 `UrbanMode --> HighwayMode`、:33 `HighwayMode --> FinishState : [auto_finished=true]`、:34 `UrbanMode --> FinishState : [auto_finished=true]`。按 UML 复合态出边语义，:30/:33 对 HighwayMode 全部子态（含 exit_hwy）生效，:31/:34 对 UrbanMode 全部子态（含 exit_urban）生效。编译产物 model.fcstm:30、34（exit_hwy）与 :54、:59（exit_urban）把它们逐一下沉，可作旁证。run2-claude#2/#4 甚至自陈『模型虽画了 HighwayMode --> FinishState』『模型对 UrbanMode 整体画了转移』却仍断言子态无出路，是同一份文本内的自相矛盾。所指的出路以复合态出边这一合法语法存在，被判成不存在。
- **NL**：NL 6/10 逐字要求两个模式在 auto_finished=true 时转入 FinishState，该义务正由 :33/:34 兑现，且对 exit_hwy / exit_urban 同样有效。
- **去重**：`0059-复合态外层出边未被计入导致误判死端` —— 与 0059-11 同为一处根因：报告者未把 stm0.puml:30/31/33/34 的复合态出边下推到子态，只是被误判的子态不同（exit_hwy/exit_urban vs intersection），故合并计 1。
- **成员**：run1/0059-claude#6 run2/0059-claude#2 run2/0059-claude#4 run2/0059-claude#8 run3/0059-claude#3

**0059-6** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 1/6 格 ｜ X1-J1

- **主张**：把多个 `[...]` 用 `||` 串起来的复合守卫写法在 UML/PlantUML 迁移标签中不合规范。
- **事实**：事实成立（该写法确实如此）：stm0.puml:39 逐字为 `collision_avoidance_deactive --> collision_avoidance_active : [pedestrian_detected] || [dist_to_rear<5 && vel>30] || [dist_to_front<15 && in_highway] || [dist_to_front<10 && in_urban]`。issue 自己承认『语义上等价但表达不合规范』。
- **NL**：NL 无此义务。NL 12 逐字用 'such as ... , ... , or ...' 并列若干激活条件，未规定它们必须写成单个守卫或拆成多条迁移。PlantUML 的迁移标签是不透明自由文本、并无形式化守卫文法可供违反；在 issue 自认语义等价的前提下，该主张只是一条记法偏好。
- **去重**：`0059-析取守卫的括号写法被判为不合规` —— 单成员组；根因是 stm0.puml:39 标签的括号排布形态，与 0059-3（争的是同一行里模式限定词的绑定）不是同一处主张。
- **成员**：run1/0059-claude#7

**0059-7** ｜ 📄 无 NL 依据 ｜ `N-FORM` ｜ 2/6 格 ｜ X1-J1

- **主张**：`lane_change_complete` 被写成布尔守卫而非完成事件，缺少触发事件语义。
- **事实**：事实成立。stm0.puml:14 `lane_change --> cruise : [lane_change_complete]`、:24 `lane_change_urban --> straight : [lane_change_complete]`，均写在守卫方括号内、无触发槽。两条 issue 自己都作了让步（『虽可接受，但缺少触发事件语义』『虽合理但需要与规格条件表述统一』）。
- **NL**：NL 无此义务。NL 4 逐字 'it can return to cruise once the lane change is completed'、NL 8 逐字 'the system transitions to straight if the lane change is complete'——NL 用散文说『一旦/若换道完成』，既未把它定为事件也未定为条件，更未规定必须以事件声明承载；PlantUML 亦不区分二者（标签皆为不透明文本）。把 NL 的散文表述读成一条『必须是事件』的形态义务属过度指定。
- **去重**：`0059-换道完成被要求以事件而非守卫承载` —— 两格同一主张，同指 stm0.puml:14/:24 那两个标签的范畴形态。
- **成员**：run1/0059-claude#8 run2/0059-claude#11

**0059-8** ｜ 📄 无 NL 依据 ｜ `N-CLOSED` ｜ 2/6 格 ｜ X1-J1

- **主张**：`road_clear` 是模型自造的名字，规范只说 'road ahead is clear'，未给出该布尔变量名。
- **事实**：事实成立。stm0.puml:22 `enter_urban --> straight : [road_clear]`；nl.txt 中不存在字符串 road_clear。
- **NL**：NL 无此禁止。NL 7 逐字含 'or straight if the road ahead is clear'——条件内容 NL 逐字给了，只是没给标识符；NL 未规定守卫必须复用 NL 中出现过的符号，也无『不得引入新名』一类措辞。run2-claude#10 自己写『与规格 road ahead is clear 描述一致但未在规格其他条款中定义 road_clear 变量……虽可接受』。这是把 NL 的标识符清单读成封闭清单。与同 NL 组的 0049-4 同判。
- **去重**：`0059-散文条件被作者命名后其标识符被判为自造` —— 两格同一主张，同指 road_clear 这个名字的来源。
- **成员**：run1/0059-claude#9 run2/0059-claude#10

**0059-9** ｜ ✅ 真漏记 ｜ `V2` ｜ 1/6 格 ｜ X1-J1

- **主张**：enter_urban 的三条出边无优先级也无互斥说明，守卫可同时成立，导致非确定性行为。
- **事实**：事实成立且属合式性缺陷。stm0.puml:21-23 逐字为 `enter_urban --> lane_change_urban : [dist_to_front<15 && extra_lane=true]`、`enter_urban --> straight : [road_clear]`、`enter_urban --> intersection : [intersection=true]`——三条边的标签只有方括号守卫、无任何触发槽，即三条无触发的守卫化完成迁移。三个守卫两两之间无任何互斥关系：最直接的是 `[intersection=true]` 与 `[road_clear]`（前方路况通畅且接近路口完全可以同时成立），`[intersection=true]` 与 `[dist_to_front<15 && extra_lane=true]` 亦然。任一对同时为真时，从 enter_urban 出发的后继不唯一，即非确定。issue 自己说出了该后果（『模型给三条并列迁移无优先级……可能同时成立，导致非确定性行为』）。
- **NL**：按合式性层收录，不要求 NL 逐字依据（确定性属形式化自身的义务，与台账 32 条 wellformedness 记录同一口径）。NL 7 逐字：'From here, it can transition to lane_change_urban if ... , or straight if the road ahead is clear, or intersection if it detects an intersection (`intersection=true`).'——NL 只给出三个条件，未给优先级或互斥保证。本 pair 台账仅 1 条（EIS-0059-01，讲 enter_hwy 分支缺失），零步同根判据：enter_urban 的这三条边与 :12 那处互不引用，改掉台账所指那条这三条仍在——不同根。
- **去重**：`0059-城市入口三条守卫迁移不确定` —— 单成员组；根因是 stm0.puml:21-23 三条无触发守卫迁移的互斥性缺失。
- **成员**：run3/0059-claude#8

**0059-10** ｜ ✅ 真漏记 ｜ `V2` ｜ 1/6 格 ｜ X1-J1

- **主张**：CollisionAvoidanceSystem 不会随系统启动被激活：顶层初始只进入 AutonomousMode，它与顶层初始没有任何连接。
- **事实**：事实成立且属合式性缺陷。stm0.puml:3 `[*] --> AutonomousMode` 是全文唯一的顶层初始边；`CollisionAvoidanceSystem` 全文只出现于 :37 的 `state CollisionAvoidanceSystem {` 声明，无任何以它为目标的迁移；作者源无 `--`（机械计数 = 0），故它是顺序兄弟态而非并发区。结论：collision_avoidance_deactive / collision_avoidance_active 及 :39/:40 两条边在任何执行下都不可达。编译产物 model.fcstm:71-77 同样无入边（唯一初始为 :78 `[*] -> AutonomousMode`），可作旁证。⭐ 与 0059-4 的分界：那一簇索要并发语义（在 M 外），本簇断言可达性（在 M 内，且在 PlantUML 自身语义下同样成立）；issue 也明确把结论条件在非并行读法上（『若按该 PlantUML 语义理解为两个顶层状态而非并行区域，则碰撞避免系统不会随系统初始启动』）。
- **NL**：按合式性层收录，不要求 NL 逐字依据（可达性属形式化自身的义务）。NL 12 逐字：'The collision avoidance system is initially in the collision_avoidance_deactive state.'——该初始态在制品中永不被进入。本 pair 台账仅 1 条（EIS-0059-01）且与 CollisionAvoidanceSystem 无任何引用关系，不同根。
- **去重**：`0059-碰撞避免子机无入边不可达` —— 单成员组；根因是 stm0.puml:3 唯一初始边与 :37 顶层兄弟态之间缺入边，与 0059-4 的并发主张 verdict 不同，不得共用 key。
- **成员**：run1/0059-gpt#2

**0059-11** ｜ ❌ 假阳性 ｜ `FP-K` ｜ 1/6 格 ｜ X1-J1

- **主张**：intersection 子状态在 UrbanMode 中没有任何出向转移，成为死状态；上下文暗示应能回到 straight。
- **事实**：事实不成立。intersection 只出现于 :23、:26 作目标，确无以它为字面源的边；但 :31 `UrbanMode --> HighwayMode : [high_way=true]` 与 :34 `UrbanMode --> FinishState : [auto_finished=true]` 是复合态出边，按 UML 语义对 UrbanMode 全部子态（含 intersection）生效。编译产物 model.fcstm:53、58 把它们下沉为 `intersection -> [*] : /_high_way_true` 与 `intersection -> [*] : /_auto_finished_true`，可作旁证。所指的出路以复合态出边这一合法语法存在，被判成不存在。附带诉求『应能回到 straight』另无 NL 依据——NL 7-10 从未描述如何离开 intersection（同 NL 组的 0049 作者写了 intersection --> straight，而那条边在 0049 又被同一批产出反过来判为『规范未描述的多余迁移』，两说不可同真）。
- **NL**：NL 7 逐字 'or intersection if it detects an intersection (`intersection=true`)'、NL 9 逐字 'if the system detects an intersection, it transitions to the intersection substate'——NL 只描述进入 intersection，未规定其出路；NL 10 要求的 UrbanMode 退出路径由 :34 兑现。
- **去重**：`0059-复合态外层出边未被计入导致误判死端` —— 与 0059-5 同为一处根因：报告者未把 stm0.puml:30/31/33/34 的复合态出边下推到子态，只是被误判的子态不同，故合并计 1。
- **成员**：run2/0059-claude#5

