# v46 意外发现逐簇判据（全 278 条）

[unexpected_adjudication.md](./unexpected_adjudication.md) 的证据附件。
裁定口径见 [UNEXPECTED_TAXONOMY.md](../UNEXPECTED_TAXONOMY.md)。

⚠️ **本文件由 `unexpected_verdicts/G*.jsonl` 生成（`../rebuild_unexpected.py`），jsonl 是真源。**
改裁定请改 jsonl 再跑重建；直接编辑本文件会在下次重建时静默丢失。

| 裁定 | 簇数 |
| :-- | --: |
| ✅ 真漏记 | 1 |
| ⚙️ 表示债务 | 129 |
| 📄 无 NL 依据 | 116 |
| ❌ 假阳性 | 22 |
| 🚫 越界 | 10 |
| **合计** | **278** |

---

## pair 0000 — 1 簇　`表示债务×1`

**0000-1** ｜ ⚙️ 表示债务 ｜ 5/6 格 ｜ `variable_declared` ｜ 判定组 G7

- **事实**：制品把量与阈值一起压进事件名：event front_distance_10 named 'front_distance > 10'，并以 HumanDrivingMode -> AutonomousMode : /front_distance_10 使用；全模型除工具生成的 def int R45RouteToken 外无任何变量声明
- **NL**：NL 第 4 句逐字写 'when front_distance > 10'，是显式的量加数值阈值，而非信号名
- **说明**：变量 V 在 M 边界内；与台账 EIS-0000-02（三个接管条件被压成单一事件标签 Human_Steering_Cmd_Brake_Pressed_in_AutoFinal）同缺陷家族，台账枚举了事件融合却未枚举变量被压入事件名这一条。

## pair 0002 — 2 簇　`无×2`

**0002-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G3

- **事实**：无 WaterState during 动作；但已用子态 MonitoringWaterFlow 与 Start/Stop_Monitoring 承载
- **NL**：NL 4 indicating 是含义说明，未要求 during 动作
- **说明**：谓词只认 action_declared(during) 一种形态

**0002-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G3

- **事实**：无 MethaneState during 动作；已用子态 MonitoringMethaneFlow 承载
- **NL**：NL 5 同为含义说明
- **说明**：与 0002-1 同源

## pair 0003 — 4 簇　`假阳性×2 无×2`

**0003-1** ｜ ❌ 假阳性 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：model.fcstm 有 event start 与 PoweredOff -> Operate : /start
- **NL**：NL 2 逐字规定 start 信号；NL 1 的 powered on 是同一刺激的散文表述
- **说明**：NL 无依据支持两个开机刺激

**0003-2** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `edge_declared/event_declared` ｜ 判定组 G1

- **事实**：入口边存在；断言为假全因触发名 power_on 是虚构的
- **NL**：NL 1+2 合起来正是 PoweredOff --start--> Operate
- **说明**：与 0003-1 同源

**0003-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `initial_target` ｜ 判定组 G1

- **事实**：根层为 [*] -> PoweredOff
- **NL**：NL 1 说上电后才进 Operate；NL 2 要求存在关机态
- **说明**：要求根初始为 Operate 会与 NL 2 冲突

**0003-4** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：模型声明三个具体动作信号，无 user_actions
- **NL**：NL 1 based on user actions 是泛称，NL 3 展开为三个具体动作
- **说明**：过度规定

## pair 0004 — 2 簇　`假阳性×1 无×1`

**0004-1** ｜ ❌ 假阳性 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：制品有 state Approaching named 'Approaching' { during abstract Send; }——Send 已作为动作声明；路径清单看不到它只是因为清单只列状态与事件、不列动作
- **NL**：NL 9 'the system sends the \\'Send\\' signal' 已由该 during 动作承载（参考用 Entry/Send，仅相位差异，issue 并未主张相位问题）
- **说明**：断言 event_declared(Send)=False 只说明它不是 event；issue 措辞 '模型未声明 Send 信号' 与制品相反。这是路径清单不含动作导致的系统性误判风险点，同类断言需回原件核验

**0004-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：制品以 InMotion 内 [*] -> Accelerating 加 state Accelerating { enter abstract Accelerate; } 承载 NL 8，无名为 motion_begins 的事件
- **NL**：NL 8 'when motion begins, marked by the \\'Entry/Accelerate\\' action' 点名的是 entry 动作，'when motion begins' 描述的是进入 InMotion 的默认初始语义，未要求独立事件
- **说明**：本 pair 恰是全语料少数把 entry 动作写对的制品（对比 0014 把整串降级成 event Entry_Accelerate，即 EIS-0014-02）；此处要求 motion_begins 事件属过度规定

## pair 0006 — 2 簇　`无×2`

**0006-1** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `state_declared` ｜ 判定组 G5

- **事实**：声明表确无 UAVSwarmStateMachine.flight（状态只有 Searching、Intercepted、Attack/AttackingTarget、FormationAdjustment/AdjustingFormation、UnspecifiedInitial）——事实成立
- **NL**：NL 4 『During flight』为语境状语，NL 未把 flight 命名为状态或范围
- **说明**：与簇 0006-4 同源（同一主张的根级与包壳级两种路径写法），也与 0046-5/0046-7 同一误报模式

**0006-4** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G5

- **事实**：声明表确无根级 flight 状态——事实成立
- **NL**：NL 4 『During flight』为语境状语，未命名状态
- **说明**：与簇 0006-1 完全同源（仅路径前缀不同：根级 flight vs UAVSwarmStateMachine.flight），去重时合并

## pair 0007 — 3 簇　`无×2 越界×1`

**0007-1** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `cardinality` ｜ 判定组 G7

- **事实**：根 scope 直接子为 CollisionDetection / CollisionAvoidance / OperationalControls / InitialState 共 4 个，issue 四者并列枚举、未指认哪一个多余。与 0037 的关键差别：InitialState 在 model.fcstm:59 有**独立 state 声明**，`[*] -> InitialState`（:62）是**另一条语句**，二者可各自变动；而 0037 的三个死端叶在 stm0.puml 中无独立声明。
- **NL**：NL 1「There are three region in this diagram」未规定根直接子恰为 3；且台账自陈 Phase-I 中 InitialState 在根层「语义连通」，其出现在根层本身不是缺陷
- **说明**：A 组 8 格裁定：「根层多一个子」与「初始迁移落在死端」是同一元素上的**两处不同失误**——保留 4 个根子但让 InitialState 带出边，台账缺陷即消失而本主张仍为 False；删掉 OperationalControls 使计数变 3，则 `[*] -> InitialState` 分毫未动而台账缺陷完整保留。落 NO_NL_BASIS：计数义务本身无 NL 依据。

**0007-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G7

- **事实**：全模型无任何名为 region 的状态或事件；'region' 只出现在 CollisionAvoidance 名字串里的 [PlantUML concurrent region 0..3] 工具注记中
- **NL**：NL 1 的 'three region' 是结构量词，NL 未要求存在一个名为 region 的元素
- **说明**：named_elements 过度字面化抽取导致的加戏；参考模型同样不会有名为 region 的元素

**0007-3** ｜ 🚫 越界 ｜ 1/6 格 ｜ `cardinality` ｜ 判定组 G7

- **事实**：CollisionAvoidance 的 named 串记录 [PlantUML concurrent region 0..3]：region1=AutomaticBraking+BrakingComplete、region2=SteeringControl+SteeringComplete、region3=AlertSystem+AlertComplete（region0 为空），作者确实写了三个非空并发区；谓词数的是 6 个直接子状态
- **NL**：NL 3 只说 active mode 有 orthogonal regions 未给数；NL 1 的 'three' 指整张图而非 CollisionAvoidance 作用域
- **说明**：'CollisionAvoidance 下恰好三个区' 是正交区数量义务，落在 M 边界外；且按区计数制品本已是三个非空区，'不是三个' 只在把区换算成子状态时才成立。与簇 0027-6 同型。

## pair 0009 — 17 簇　`表示债务×14 无×3`

**0009-1** ｜ ⚙️ 表示债务 ｜ 5/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：路径里有 pedestrian_detected_dist_to_rear_5_vel_30_... 这一融合事件，独立的 pedestrian_detected 确不存在
- **NL**：NL 9 逐字点名 'a pedestrian is detected' 为独立触发条件
- **说明**：与台账 EIS-0030-03 同缺陷类（融合事件），台账对本 pair 未枚举。

**0009-2** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：dist_to_rear<5 && vel>30 是上述融合事件 named 串的第二个析取支，作者在 stm0.puml 的 collision_avoidance_deactive --> collision_avoidance_active 守卫里逐字写出
- **NL**：NL 12 把它列为 'or' 备选之一，未要求独立事件声明
- **说明**：与簇 0009-1 同源；同属 opaque_transition_label_semantics 表示债务。

**0009-3** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：dist_to_front<15 && high_way=true 是该融合事件 named 串的第三个析取支（注意路径里的 dist_to_front_15_extra_lane_true 是 NL 7/9 的城区变道条件，属另一条边），作者源已逐字表达
- **NL**：NL 12 'the front distance being less than 15 meters in highway mode' 为 'or' 备选之一
- **说明**：与簇 0009-1 同源；簇 0009-14/16 是同一主张的重复表述。

**0009-4** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：dist_to_front<10 && urban_way=true 是该融合事件 named 串的第四个析取支，作者源逐字写出
- **NL**：NL 12 'or 10 meters in urban mode' 为备选之一
- **说明**：与簇 0009-1 同源；簇 0009-15/17 是同一主张的重复表述。

**0009-5** ｜ 📄 无 NL 依据 ｜ 5/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：front_inactive_rear_inactive_pedestrian_inactive 的 named 串是 'front_inactive && rear_inactive && pedestrian_inactive'，作者在 collision_avoidance_active --> collision_avoidance_deactive 上写的是一条合法合取守卫，front_inactive 逐字在内
- **NL**：NL 13 'as indicated by the conditions front_inactive, rear_inactive, and pedestrian_inactive' 是合取，一条合取守卫即为忠实编码
- **说明**：与簇 0009-6/7 同源；事件名融合同属 R4.5 opaque_transition_label_semantics 降级。

**0009-6** ｜ 📄 无 NL 依据 ｜ 5/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：rear_inactive 是同一合取守卫 'front_inactive && rear_inactive && pedestrian_inactive' 的第二个合取项
- **NL**：NL 13 同上
- **说明**：与簇 0009-5 同源。

**0009-7** ｜ 📄 无 NL 依据 ｜ 5/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：pedestrian_inactive 是同一合取守卫的第三个合取项
- **NL**：NL 13 同上
- **说明**：与簇 0009-5 同源。

**0009-8** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：model.fcstm 仅有 def int R45RouteToken = 0（转换器路由变量），但 dist_to_front 在作者源 stm0.puml 中以 dist_to_front>=25 / dist_to_front<25 && extra_lane=true / dist_to_front<15 && extra_lane=true 等守卫文本逐字出现；PlantUML 本身无变量声明语法，全语料 60 份制品（33 份只含注入的 R45RouteToken，另 27 份无任何 def）无一声明任何作者变量（grep 'def ' 只命中 R45RouteToken）
- **NL**：NL 3/5/7/9/12 使用 `dist_to_front<25` 等条件，但要求的是条件本身，作者源已表达
- **说明**：与 0036 人工复核 diff#4 判定同类：作者源已表达即属表示债务（E3），不得记为模型缺陷；对照 0006 的真缺陷是『作者源里连递减文本都没有』。与簇 0009-9/10/11/12 同源。

**0009-9** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：extra_lane 在作者源守卫 'dist_to_front<25 && extra_lane=true'、'dist_to_front<15 && extra_lane=true' 中逐字出现；制品内唯一 def 为 R45RouteToken
- **NL**：NL 3/7/9 的 `extra_lane=true` 已被守卫文本承载
- **说明**：与簇 0009-8 同源，表示债务而非缺陷。

**0009-10** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：dist_to_exit 在事件 dist_to_exit_2 named 'dist_to_exit<2' 与 dist_to_exit_0_7 named 'dist_to_exit<0.7' 中逐字出现
- **NL**：NL 4/5/8 的 `dist_to_exit<2` / `<0.7` 已被守卫文本承载
- **说明**：与簇 0009-8 同源。

**0009-11** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：dist_to_rear 在融合守卫的析取支 '(dist_to_rear<5 && vel>30)' 中逐字出现
- **NL**：NL 12 的 `dist_to_rear<5` 已被守卫文本承载
- **说明**：与簇 0009-8 同源。

**0009-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：vel 在同一析取支 '(dist_to_rear<5 && vel>30)' 中逐字出现
- **NL**：NL 12 的 `vel>30` 已被守卫文本承载
- **说明**：与簇 0009-8 同源。

**0009-13** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：rationale 关于 dist_to_front_25 语义为 '>=25' 的核对属实（named 串确为 'dist_to_front>=25'），但 dist_to_front<25 本身以 dist_to_front_25_extra_lane_true named 'dist_to_front<25 && extra_lane=true' 逐字存在于制品；且作者源 enter_hwy --> cruise : dist_to_front>=25 是对 NL 3 歧义的互补守卫消歧
- **NL**：NL 3 只给出一个联合条件却指向 cruise 与 lane_change 两个目标，本身有歧义；rationale 主张的『enter_hwy 应在 dist_to_front<25 单独触发下转入 cruise』与 NL 5（dist<25 且有邻道时进 lane_change）相矛盾
- **说明**：0009 人工复核 diff#1 判该互补守卫 similar 并称『语义上说得通且判定性更强，甚至优于参考』。

**0009-14** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：同簇 0009-3：dist_to_front<15 && high_way=true 是融合守卫的第三析取支，作者源逐字写出
- **NL**：NL 12 列为 'or' 备选之一
- **说明**：与簇 0009-3 同源，仅断言签名的清洗名不同（dist_to_front_15_highway）

**0009-15** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：同簇 0009-4：dist_to_front<10 && urban_way=true 是融合守卫的第四析取支
- **NL**：NL 12 列为 'or' 备选之一
- **说明**：与簇 0009-4 同源，仅清洗名不同（dist_to_front_10_urban）

**0009-16** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：同簇 0009-3/14；路径里形近的 dist_to_front_15_extra_lane_true 属 NL 7/9 的城区变道条件，不是本条主张的高速危险条件
- **NL**：NL 12 列为 'or' 备选之一
- **说明**：与簇 0009-3 同源，第三种清洗名（dist_to_front_15_high_way_true）

**0009-17** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：同簇 0009-4/15
- **NL**：NL 12 列为 'or' 备选之一
- **说明**：与簇 0009-4 同源，第三种清洗名（dist_to_front_10_urban_way_true）

## pair 0010 — 1 簇　`表示债务×1`

**0010-1** ｜ ⚙️ 表示债务 ｜ 6/6 格 ｜ `variable_declared` ｜ 判定组 G8

- **事实**：冻结路径中不存在任何变量声明，数值条件被改建成两个事件名 Front_Distance_10 与 Front_Distance_10_2（后者的 _2 后缀说明同一条件被复制成两个事件），front_distance 变量确不存在
- **NL**：NL 第 4 句『when front_distance > 10, auto transport to autonomous state』逐字给出变量名 front_distance 与数值比较守卫
- **说明**：6/6 格稳定命中，hit@all=1。落在 M=(S,E,V,Tr,A) 的 V 与 Tr 守卫上，未涉时钟/不变式/并发。台账 5 条（occupancy_after / state_declared / terminates / reaches / event_consumed）无一覆盖变量与守卫缺失，属真漏记；实质危害是数值守卫不可求值，front_distance 的取值无法影响迁移。

## pair 0011 — 1 簇　`无×1`

**0011-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：NL 3 要求的边存在：BrakingState -> ClampingState : /Entering_Clamping_State
- **NL**：NL 3 After entering the braking state 是指明源状态的时间状语
- **说明**：把状语从句误读成事件名

## pair 0012 — 2 簇　`假阳性×1 无×1`

**0012-1** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中已声明 start；NL 自己就把上电激励命名为 start，模型的 start 即该事件，并非缺失或融合
- **NL**：NL 2『The system can be turned on with the `start` signal and turned off with the `keyOff` signal』用反引号给出信号名，与 NL 1『Once the device is powered on』指同一次开机迁移
- **说明**：rationale 自称『上电语义融合到 start』不成立——那是 NL 指定的名字，不是模型的融合。台账 EIS-0012-01 记录的是 Off 出边无触发导致 start 不可达，与本簇的存在性主张无关

**0012-2** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中已声明 accelerate / brake / stop 三个具体动作事件，确无聚合事件 user_actions
- **NL**：NL 1『based on user actions』是集合名词，NL 3 随即把它展开为『actions like accelerating, braking, or stopping』，NL 要求的是这几个具体动作而非一个聚合事件
- **说明**：与 0016-8 同型的范畴错误：把 NL 的统称词要求成一个模型元素；此处方向恰好相反于融合缺陷——要求把已正确拆分的事件再聚合回去

## pair 0013 — 3 簇　`无×3`

**0013-1** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `action_declared` ｜ 判定组 G1

- **事实**：model.fcstm 全文零 action
- **NL**：NL 3 where the pump is activated or controlled 是同位语解释，未命名 action
- **说明**：与 0013-2/3 同源；相位选择也无 NL 依据

**0013-2** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `action_declared` ｜ 判定组 G1

- **事实**：WaterState 无任何相位 action
- **NL**：NL 4 indicating that 明确是解释状态名所指
- **说明**：同源

**0013-3** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `action_declared` ｜ 判定组 G1

- **事实**：MethaneState 无任何相位 action
- **NL**：NL 5 同构
- **说明**：同源

## pair 0014 — 8 簇　`无×5 假阳性×2 真漏记×1`

**0014-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G7

- **事实**：全模型只有工具生成的 def int R45RouteToken，无任何作者变量；巡航速度由 event Reached_Cruising_Cruise named 'Reached Cruising/Cruise' 承载并用于 Accelerating -> Cruising
- **NL**：NL 5 明说 'as indicated by the \\'Reached Cruising/Cruise\\' signal'，是信号而非数值比较，NL 未出现任何 cruising speed 的量或阈值
- **说明**：对比 pair 0000 的 NL 才有 'front_distance > 10' 这种显式量加阈值；此处要求变量属过度规定

**0014-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G7

- **事实**：制品无 ready_to_stop 元素；NL 10 的内容以描述行形式落在 Approaching named 'Approaching' 后的 [PlantUML body] Nearing Destination 与 [PlantUML body] Ready to Stop/Decelerate
- **NL**：NL 10 'until it is ready to stop or decelerate' 是散文式释放条件，未要求声明同名状态或条件元素
- **说明**：与簇 0014-3/0014-7/0014-8 同源；参考 PlantUML 同样只用 state description 行表达这句

**0014-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G7

- **事实**：制品无名为 decelerate 的状态；相关文本以 event Approached_Decelerate named 'Approached/Decelerate' 与 Approaching 名字串中的 'Ready to Stop/Decelerate' 描述行存在
- **NL**：NL 10 'until it is ready to stop or decelerate'，未要求把 decelerate 声明成状态
- **说明**：与簇 0014-2 同源

**0014-4** ｜ ✅ 真漏记 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：EmergencyStopping named 'EmergencyStopping' 后接 [PlantUML body] Obstacle Detected——NL 要求发出的信号被吞进状态名描述串，该状态内无任何 enter/during 动作；模型里唯一的 Obstacle_Detected 是输入触发，用在 Accelerating/Cruising/Approaching -> [*] : /Obstacle_Detected 上
- **NL**：NL 3 'enters the EmergencyStopping state, which includes the actions \\'Emergency Stop\\' and sends the \\'Obstacle Detected\\' signal'
- **说明**：同一 NL 的 pair 0004 用 EmergencyStopping { enter abstract EmergencyStop; during abstract SendObstacleDetected; } 正确承载，证明该输出动作在 M 内可表达且是参考意图；与 EIS-0014-03/04 同属 PlantUML body 降级家族，台账枚举了 Emergency Stop 与 Send 却漏了这一条。正确修法是动作而非独立事件，归并时按 A 类记

**0014-5** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：制品声明了 event Arrived_Stop_SendArrived named 'Arrived/Stop, SendArrived'，并以它驱动 Accelerating/Cruising/Approaching -> [*] 与随后的 InMotion -> Stopping : if [R45RouteToken == 6]；与断言所求名字只差 Send 与 Arrived 之间一个分隔符
- **NL**：NL 2 的 'Arrived/Stop, Send Arrived' 信号已被该事件承载
- **说明**：'缺少该事件、且无法验证收到后转入 Stopping' 与制品直接相反；剩下的只是原文转写少一个空格的保真度细节

**0014-6** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：制品声明了 event Obstacle_Detected named 'Obstacle Detected'，并用于 InMotion 内三条 -> [*] : /Obstacle_Detected 迁移，障碍检测刺激确已独立存在
- **NL**：NL 2 'if an obstacle is detected' 与 NL 3 'When an obstacle is detected' 均已被该事件承载
- **说明**：断言只是换了 an_obstacle_is_detected 这一措辞，属命名变体导致的假阳性

**0014-7** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G7

- **事实**：制品无 Ready_to_stop 状态；对应文本在 Approaching 名字串的 [PlantUML body] Ready to Stop/Decelerate 描述行里
- **NL**：NL 10 'until it is ready to stop or decelerate'，未要求声明该状态或条件元素
- **说明**：与簇 0014-2 是同一发现的大小写变体

**0014-8** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G7

- **事实**：制品无 Ready_to_decelerate 状态；相关文本同样只存在于 Approaching 名字串的 [PlantUML body] Ready to Stop/Decelerate 中
- **NL**：NL 10 同句，未要求声明该状态或条件元素
- **说明**：与簇 0014-3/0014-7 同源

## pair 0016 — 10 簇　`表示债务×8 无×2`

**0016-1** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G8

- **事实**：路径里有 pedestrian_detected_dist_to_rear_5_vel_30_... 这一融合事件，独立的 pedestrian_detected 确不存在
- **NL**：NL 9 逐字点名 'a pedestrian is detected' 为独立触发条件
- **说明**：与台账 EIS-0030-03 同缺陷类（融合事件），台账对本 pair 未枚举。

**0016-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G8

- **事实**：路径中确无 flight 状态；顶层只有 SearchMission / FormationAdjust / AttackState 三个运行态
- **NL**：NL 4『During flight, if task assignment information is received』中的 During flight 是状语背景，NL 未把 flight 列为需单独命名的状态；整台机器本身即处于飞行上下文，NL 中不存在非飞行上下文与之对立
- **说明**：命名字面主义：要求为背景状语单独造一个同名状态，属过度规定

**0016-4** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有融合名 Attack_Finished_Decrease_UAV_swarm_count，把『攻击完成』刺激与『减少 UAV 数量』效果压进同一个事件名；不存在任何仅承载攻击完成刺激的独立事件
- **NL**：NL 4『After completing the attack, the number of UAVs in the swarm decreases accordingly』把完成攻击（刺激）与数量减少（效果）分述为两件事
- **说明**：实质危害是减量只存在于事件名里，模型无变量亦无 effect 表达式承载它。台账 3 条均未覆盖。与簇 0016-6/12 同源。

**0016-5** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G8

- **事实**：路径中无 number_of_UAVs_in_the_swarm，也无任何作者声明变量；仅有编译器路由变量 R45RouteToken
- **NL**：NL 4『the number of UAVs in the swarm decreases accordingly』
- **说明**：与簇 0016-1/7/9/10 同源（同一缺失变量的不同命名）

**0016-6** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：Attack_Finished 是路径中 Attack_Finished_Decrease_UAV_swarm_count 的子串，融合成立；独立的 Attack_Finished 事件确未声明
- **NL**：NL 4『After completing the attack, ...』
- **说明**：与簇 0016-4/12 同源。

**0016-7** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G8

- **事实**：路径中无 uav_count；唯一变量 R45RouteToken 是编译器路由变量，不承载 UAV 语义
- **NL**：NL 4『the number of UAVs in the swarm decreases accordingly』要求一个可递减的数量
- **说明**：与簇 0016-1/5/9/10 同源。

**0016-8** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G8

- **事实**：路径中确无 UAV_swarm 状态；UAV_swarm 只作为片段出现在事件名 Attack_Finished_Decrease_UAV_swarm_count 中
- **NL**：NL 1『This state machine model describes the state transitions of a UAV swarm』把 UAV swarm 作为整台机器的建模主体，根 llms_emp_feedback_final_0016 即该主体；NL 未要求主体本身成为一个状态
- **说明**：范畴错误式的命名字面主义：把建模主体要求成模型内的一个状态

**0016-9** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `effect_declared/variable_declared` ｜ 判定组 G8

- **事实**：无作者声明变量（仅 R45RouteToken），且 AttackState.Attacking 上由 Attack_Finished_Decrease_UAV_swarm_count 触发的迁移未声明任何负向效果
- **NL**：NL 4『After completing the attack, the number of UAVs in the swarm decreases accordingly』同时要求变量与其递减效果
- **说明**：与簇 0016-1/5/7/10 同源；本簇把变量缺失与效果缺失合并为同一处修复，表述最完整。

**0016-10** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `effect_declared` ｜ 判定组 G8

- **事实**：AttackState.Attacking 上 Attack_Finished_Decrease_UAV_swarm_count 触发的迁移无对任何数量变量的负向效果，模型仅有 R45RouteToken 路由变量
- **NL**：NL 4『the number of UAVs in the swarm decreases accordingly』
- **说明**：与簇 0016-9 同源（效果侧）

**0016-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中不存在 attack_completed；唯一相关事件是融合名 Attack_Finished_Decrease_UAV_swarm_count
- **NL**：NL 4『After completing the attack, ...』
- **说明**：与簇 0016-4/6 同源。

## pair 0017 — 11 簇　`无×10 越界×1`

**0017-1** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中事件仅有 collision_detected 与 Collision_avoided，frontend/rear_end/pedestrian 三个具体检测事件一个都不存在——三种刺激被塌缩成一个泛化事件
- **NL**：NL 2 逐字并列点名三种检测：『a possible frontend collision, rear-end collision or collision with pedestrian is detected』
- **说明**：该 pair 台账为 0 条，属真漏记。可与 pair 0057 对照：同一份 NL 下 0057 确实分别声明了 Frontend_collision_detected / Rear_end_collision_detected / Pedestrian_collision_detected，说明三事件可分是该 NL 的通行读法而非过度指定。本簇为 0017-2/3/4/5/6/9/11 的合并表述。

**0017-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有泛化事件 collision_detected，无任何承载前向碰撞的独立事件
- **NL**：NL 2『a possible frontend collision ... is detected』
- **说明**：与簇 0017-1/4/11 同源（前向刺激的不同命名）

**0017-3** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有 collision_detected，无行人碰撞的独立事件
- **NL**：NL 2『... or collision with pedestrian is detected』
- **说明**：与簇 0017-1/6/9 同源。

**0017-4** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有 collision_detected，frontend_collision_detected 未声明
- **NL**：NL 2『a possible frontend collision ... is detected』
- **说明**：与簇 0017-1/2/11 同源。

**0017-5** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有 collision_detected，rear_end_collision_detected 未声明
- **NL**：NL 2『rear-end collision ... is detected』
- **说明**：与簇 0017-1 同源；追尾刺激在本 pair 只被本簇单独点出。

**0017-6** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有 collision_detected，pedestrian_collision_detected 未声明
- **NL**：NL 2『... or collision with pedestrian is detected』
- **说明**：与簇 0017-1/3/9 同源。

**0017-7** ｜ 🚫 越界 ｜ 1/6 格 ｜ `invariant` ｜ 判定组 G8

- **事实**：Collision_Avoidance_Active_Mode.F / .P / .R 确为同一区域下的互斥子状态而非并行区域
- **NL**：NL 3『The orthogonal regions ... allow for concurrent activation』确有依据
- **说明**：主张完全依赖正交区并发语义，且断言族为 invariant；两者都在 project_1 建模对象边界之外（M=(S,E,V,Tr,A) 排除不变式与正交并发），按边界判越界，不计为方法未检出也不计为发现

**0017-8** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G8

- **事实**：路径中确无名为 region 的状态；Collision_Avoidance_Active_Mode 下有 F / P / R 三个子状态
- **NL**：NL 1『There are three region in this diagram』说的是三个区域这一结构事实，未要求存在一个名为 region 的单数状态元素
- **说明**：命名字面主义；且其实质读法（三个正交区域）落在 NL 3 的并发语义上，按边界同样越界。两条路都不支持把它计为 M 内发现

**0017-9** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有 collision_detected，collision_with_pedestrian_detected 未声明
- **NL**：NL 2『... or collision with pedestrian is detected』
- **说明**：与簇 0017-1/3/6 同源。

**0017-10** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `state_declared` ｜ 判定组 G8

- **事实**：路径中确无 collision_avoidance_controls；但 Collision_Avoidance_Active_Mode.F / .P / .R 就是三个避撞控制本身
- **NL**：NL 3『concurrent activation different of collision avoidance controls』把 collision avoidance controls 用作对 F/R/P 的统称，未要求另设一个同名容器元素
- **说明**：命名字面主义；与 0057-5 同型

**0017-11** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中只有泛化的 collision_detected，possible_frontend_collision 未声明
- **NL**：NL 2『a possible frontend collision ... is detected』
- **说明**：与簇 0017-1/2/4 同源。注意与 0057-6 判定相反：0057 实际声明了 Frontend_collision_detected，本 pair 没有。

## pair 0019 — 23 簇　`表示债务×19 无×4`

**0019-1** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：路径中无独立 pedestrian_detected；仅有融合事件 pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_hwy_mode_or_10_in_urban_mode
- **NL**：NL 12 反引号逐字点名 pedestrian_detected，句式为析取式独立触发
- **说明**：析取融合，NL 的任一即可变成模型的须全满足。

**0019-2** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无 dist_to_rear_5_vel_30 独立事件
- **NL**：NL 12 第二析取项
- **说明**：与 0019-1 同源。

**0019-3** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无高速模式前距独立事件
- **NL**：NL 12 第三析取项
- **说明**：与 0019-1 同源；与 0019-8/23 同一元素不同拼法。

**0019-4** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无城市模式前距<10 独立名字
- **NL**：NL 12 第三析取项后半
- **说明**：与 0019-9 同一元素。

**0019-5** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：只有 front_inactive_rear_inactive_pedestrian_inactive
- **NL**：NL 13 逐个点名三者
- **说明**：合取融合，弱于析取融合。

**0019-6** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无独立 rear_inactive
- **NL**：NL 13
- **说明**：与 0019-5 同源。

**0019-7** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无独立 pedestrian_inactive
- **NL**：NL 13
- **说明**：与 0019-5 同源。

**0019-8** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：dist_to_front_15_in_highway_mode 不存在
- **NL**：NL 12
- **说明**：与 0019-3 同一元素。

**0019-9** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：dist_to_front_10_in_urban_mode 不存在
- **NL**：NL 12
- **说明**：与 0019-4 同一元素。

**0019-10** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无单独 extra_lane 名字
- **NL**：NL 3 extra_lane=true
- **说明**：与 0019-11/16 同一元素。

**0019-11** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无 extra_lane_is_available
- **NL**：NL 7/9
- **说明**：与 0019-10 同源。

**0019-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无单独 dist_to_front_15
- **NL**：NL 7/9
- **说明**：与 0019-22 同一元素。

**0019-13** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：8 个名字逐一核对均不存在
- **NL**：NL 3/5/7/9/12/13
- **说明**：roll-up，归并时作父条目不独立计数。

**0019-14** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：四个碰撞激活触发均无独立名字
- **NL**：NL 12 三项析取
- **说明**：roll-up；析取融合中语义后果最硬的一条。

**0019-15** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G3

- **事实**：全部路径无任何变量声明；R45RouteToken 是投影注入的路由令牌
- **NL**：NL 3/5/7/9/12 同一量三个阈值
- **说明**：V 是 M 的一员，整模型 V 为空，台账三条均未涉及。

**0019-16** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G3

- **事实**：无 bare extra_lane
- **NL**：NL 3
- **说明**：谓词选 variable_declared 比 0019-10/11 更贴合 NL。

**0019-17** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G3

- **事实**：只有阈值事件 dist_to_exit_2/0_7，无变量
- **NL**：NL 4/5/8
- **说明**：V 缺失同类。

**0019-18** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G3

- **事实**：dist_to_rear 只作融合事件名片段
- **NL**：NL 12
- **说明**：V 缺失同类。

**0019-19** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G3

- **事实**：vel 只作融合事件名片段
- **NL**：NL 12
- **说明**：V 缺失同类。

**0019-20** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：三个单独名字均不存在
- **NL**：NL 13
- **说明**：是 0019-5/6/7 的 roll-up。

**0019-21** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无 dist_to_front_lt_25
- **NL**：NL 3/5
- **说明**：该融合事件正是台账 EIS-0019-01 论证守卫不可区分的同一对象——台账承认后果却未记融合本身。

**0019-22** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：无 dist_to_front_lt_15
- **NL**：NL 7/9
- **说明**：与 0019-12 同一元素。

**0019-23** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：该串只作长融合事件后缀
- **NL**：NL 12 第三析取项整句
- **说明**：与 0019-3+0019-4 是同一元素两种切法。

## pair 0020 — 2 簇　`表示债务×1 假阳性×1`

**0020-1** ｜ ⚙️ 表示债务 ｜ 5/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：唯一变量是注入的 R45RouteToken；阈值折叠成 event front_distance_10
- **NL**：NL 4 逐字命名 front_distance 并给阈值比较
- **说明**：台账 EIS-0020-01/02 均为 event_declared 类，未覆盖变量缺失。

**0020-2** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `containment/state_declared` ｜ 判定组 G1

- **事实**：AutonomousMode 内已声明 state AutoFinalState，且有到 [*] 的边
- **NL**：NL 4 提及 in (auto final)，未规定标识符字面形式
- **说明**：断言钉死 auto_final 路径；真缺陷已由台账 EIS-0020-02 记录

## pair 0022 — 3 簇　`无×2 假阳性×1`

**0022-1** ｜ ❌ 假阳性 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：rationale 断言『没有任何名字承担 powered on 语义』与制品相反：声明表中有事件 start，且模型还有顶层状态 PoweredOn，其中 PoweredOn --/start--> Operate 正是上电入 Operate 的承载
- **NL**：NL 2 明确把开机信号定名为 `start`（『The system can be turned on with the `start` signal』），故 NL 不要求另立一个 power_on 事件；NL 1 的 'powered on' 与 NL 2 的 start 指同一刺激
- **说明**：要求独立 power_on 事件是把 NL 1 与 NL 2 当成两个不同刺激；本 pair 台账为 0 条，但这一条不应补入

**0022-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `initial_target` ｜ 判定组 G5

- **事实**：根级初始边指向 PoweredOn 而非 Operate 属实，但同一份 NL（md5 c74d44e9）下 6 个作者**全部**加了顶层前置态：0003 PoweredOff、0012 Off、0032 OffState、0042 Off、0052 Off、0022 PoweredOn，无一直连 Operate
- **NL**：NL 1「Once the device is powered on, the system enters the Operate state」+ NL 2 的 start 与 keyOff——参考读法是「上电→前置态→start→Operate」，NL 不要求根初始直指 Operate
- **说明**：残留的只是命名保真度瑕疵（叫 PoweredOn 却仍需 start），属 S 层一个名字的措辞，不构成元素级缺陷。另：同组 0022-1 已判 FALSE_POSITIVE，理由是「NL 1 的 powered on 与 NL 2 的 start 指同一刺激」，而原 0022-2 的成立前提恰是把两者当两个刺激——同一文件不能既判 A 又判 ¬A，此矛盾随本次推翻消解。⚠️ 不判 FALSE_POSITIVE：事实在制品上为真，不符合「主张与制品相反」的定义。

**0022-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G5

- **事实**：PoweredOn 是根下顶层状态属实；但 6/6 同组作者均有此形态，非 0022 独有的自增结构
- **NL**：NL 1/2 的参考读法含前置态
- **说明**：与 0022-2 同源，一并推翻。原援引的 EIS-0046-03 类比不成立——那条是「额外增加 Idle 态**与 Start Mission 事件**」，而 0022 未增加任何事件，start 是 NL 2 逐字点名的。

## pair 0023 — 9 簇　`越界×6 无×3`

**0023-1** ｜ 🚫 越界 ｜ 1/6 格 ｜ `reaches` ｜ 判定组 G7

- **事实**：PumpControl 内除 [*] -> PumpState、[*] -> WaterState、[*] -> MethaneState 三条初始迁移外没有任何迁移，全模型未声明任何 event；PumpControl 的 named 串记录 [PlantUML concurrent region 0/1/2] 分别只装一个子态
- **NL**：NL 4 'The system can also transition to the WaterState substate'、NL 5 'the system can transition to the MethaneState substate'
- **说明**：实质缺陷是三个替代子态被写成三个并发区各自的默认入口、区间零迁移；判定只用 Tr 层事实，不依赖并发语义。与簇 0023-2/3/7/8/9 同源；本 pair 台账 0 条。

**0023-2** ｜ 🚫 越界 ｜ 1/6 格 ｜ `reaches` ｜ 判定组 G7

- **事实**：制品中 PumpState 没有任何出边（PumpControl 内只有三条 [*] -> 子态 的初始迁移），到 WaterState 无任何路径
- **NL**：NL 3 'first transitions to the PumpState' 加 NL 4 'can also transition to the WaterState substate'
- **说明**：与簇 0023-1 同源。

**0023-3** ｜ 🚫 越界 ｜ 1/6 格 ｜ `reaches` ｜ 判定组 G7

- **事实**：制品中 PumpState 没有任何出边，到 MethaneState 无任何路径；PumpControl 内不存在 tr 连接三个子态
- **NL**：NL 3 加 NL 5 'Similarly, the system can transition to the MethaneState substate'
- **说明**：与簇 0023-1/0023-2 同源。

**0023-4** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `action_declared` ｜ 判定组 G7

- **事实**：PumpState named 'PumpState' 后接 [PlantUML body] Pump Activated 描述行，制品内确无 during 动作声明（全模型无任何 enter/during abstract）
- **NL**：NL 3 'where the pump is activated or controlled' 是对状态含义的描述，未点名任何动作或相位
- **说明**：参考 PlantUML 本身就用 state description 行承载这句，制品已忠实转写；对比 0014 的 NL 8 才是全语料少数逐字点名 'Entry/Accelerate' 相位的句子。要求 during 动作属过度规定，与簇 0023-5/6 同源

**0023-5** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `action_declared` ｜ 判定组 G7

- **事实**：WaterState named 'WaterState' 后接 [PlantUML body] Water Flow Monitored，无 during 动作
- **NL**：NL 4 'indicating that the pump is controlling or monitoring the water flow' 是状态语义说明，未要求动作声明
- **说明**：与簇 0023-4 同源

**0023-6** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `action_declared` ｜ 判定组 G7

- **事实**：MethaneState named 'MethaneState' 后接 [PlantUML body] Methane Flow Monitored，无 during 动作
- **NL**：NL 5 'indicating that the pump is controlling or monitoring the methane flow'，同样只是状态语义说明
- **说明**：与簇 0023-4/0023-5 同源

**0023-7** ｜ 🚫 越界 ｜ 3/6 格 ｜ `reaches` ｜ 判定组 G7

- **事实**：PumpControl 内三个子状态之间零迁移，仅有 [*] -> PumpState / [*] -> WaterState / [*] -> MethaneState；模型连一个 event 都没声明，无从触发子态切换
- **NL**：NL 4 与 NL 5 均以 'can transition to' 要求运行期可切换到 WaterState / MethaneState
- **说明**：与簇 0023-1/2/3 同源，是该缺陷覆盖面最完整的表述。

**0023-8** ｜ 🚫 越界 ｜ 1/6 格 ｜ `reaches` ｜ 判定组 G7

- **事实**：从 PumpControl 出发只有三条并列初始迁移，无任何后续迁移可抵达 WaterState（若初始落在 PumpState 或 MethaneState 则永不可达）
- **NL**：NL 4 'The system can also transition to the WaterState substate'
- **说明**：与簇 0023-1 同源。

**0023-9** ｜ 🚫 越界 ｜ 1/6 格 ｜ `reaches` ｜ 判定组 G7

- **事实**：从 PumpControl 出发无任何迁移可抵达 MethaneState；PumpControl 内没有任何非初始迁移
- **NL**：NL 5 'the system can transition to the MethaneState substate'
- **说明**：与簇 0023-1 同源。

## pair 0024 — 4 簇　`假阳性×2 无×2`

**0024-1** ｜ ❌ 假阳性 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：路径已声明 Obstacle_Detected
- **NL**：NL 2 要求该输入触发，模型已有
- **说明**：因谓词要求精确标识符 obstacle_is_detected 而判缺失

**0024-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G3

- **事实**：路径无 ready_to_stop；模型已声明 Stopping 与 Arrived_Stop_Send_Arrived
- **NL**：NL 10 是散文描述，未把 ready to stop 命名为状态
- **说明**：与 0024-3 同源

**0024-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G3

- **事实**：无名为 decelerate 的状态；Approached_Decelerate 信号已声明
- **NL**：NL 6/7/10 中 Decelerate 为动作/信号语义
- **说明**：要求把动作声明成状态，元素类型即错

**0024-4** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：NL 命名的 Obstacle Detected 在路径中有两处载体；缺的只是谓词自造的 Obstacle_Detected_signal
- **NL**：NL 3 要求该输出，模型中存在（方向被写反）
- **说明**：底层真缺陷已由台账 EIS-0024-04 记录

## pair 0026 — 4 簇　`无×3 假阳性×1`

**0026-1** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G2

- **事实**：路径里存在 SearchingState.FinalWaittr_0006，簇 0026-3 自己把它当完成边界用
- **NL**：NL 2 只要求存在完成边界，未要求名为 Mission_Completed 的状态
- **说明**：强形式被证伪，弱形式无 NL 依据

**0026-2** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `state_declared` ｜ 判定组 G2

- **事实**：无 Flight 状态
- **NL**：NL 4 During flight 是描述整机运行语境的散文
- **说明**：与 0026-5 同源；rationale 自承下游断言归因 unattributed

**0026-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `persists_until` ｜ 判定组 G2

- **事实**：观察属实但 NL 3/4 正是要求那两条出边存在
- **NL**：NL 2 的持续性针对 SearchingState 复合态，不是子态
- **说明**：NL 2 的真实违反已由台账 EIS-0026-03 记录

**0026-5** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G2

- **事实**：无 flight 状态
- **NL**：NL 4 During flight 为语境散文
- **说明**：与 0026-2 同源

## pair 0027 — 13 簇　`表示债务×11 越界×1 假阳性×1`

**0027-1** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `cardinality` ｜ 判定组 G7

- **事实**：路径里有 pedestrian_detected_dist_to_rear_5_vel_30_... 这一融合事件，独立的 pedestrian_detected 确不存在
- **NL**：NL 9 逐字点名 'a pedestrian is detected' 为独立触发条件
- **说明**：与台账 EIS-0030-03 同缺陷类（融合事件），台账对本 pair 未枚举。

**0027-2** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：全模型只声明一个事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected named 'Frontend Collision or Rear-end Collision or Collision with Pedestrian detected'，再无任何其他 event，三个独立碰撞事件确不存在
- **NL**：NL 2 逐字并列 'a possible frontend collision, rear-end collision or collision with pedestrian is detected'
- **说明**：同一 NL 的 pair 0007 声明了 Frontend_Detected / Rear_end_Detected / Pedestrian_Detected 三个独立事件，证明拆分是参考意图且在 M 内可表达；与台账 EIS-0000-02（多条件压成单一事件标签）同缺陷类，台账对本 pair 未枚举。

**0027-3** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G7

- **事实**：唯一激活路径是 DetectingState -> junction1 : /Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected 加 junction1 -> ActiveState；以 frontend_collision_detected 为触发的边不存在，该独立事件本身也未声明
- **NL**：NL 2 把 frontend collision 列为使子机激活的触发之一
- **说明**：与簇 0027-2 同源（融合事件派生）；'直达边' 这一形式要求偏严——经 junction 路由本身合法，实质缺陷是独立触发不存在。

**0027-4** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G7

- **事实**：制品中不存在任何以 rear_end_collision_detected 为触发的迁移，也未声明该事件；唯一检测触发是融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected
- **NL**：NL 2 把 rear-end collision 列为使子机激活的触发之一
- **说明**：与簇 0027-2/0027-3 同源。

**0027-5** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G7

- **事实**：制品中不存在任何以 collision_with_pedestrian_detected 为触发的迁移，也未声明该事件；仅有融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected
- **NL**：NL 2 把 collision with pedestrian 列为使子机激活的触发之一
- **说明**：与簇 0027-2/0027-3/0027-4 同源。

**0027-6** ｜ 🚫 越界 ｜ 1/6 格 ｜ `invariant` ｜ 判定组 G7

- **事实**：断言以 invariant + active('ActiveState.BrakeControlState') 等形式要求三个控制态在 ActiveState 内同时保持活跃
- **NL**：NL 3 'allow for concurrent activation different of collision avoidance controls'
- **说明**：invariant 与正交区并发语义两项都在建模对象之外，按边界规则一律越界

**0027-7** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：模型未声明 possible_frontend_collision；唯一事件是融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected，其名字包含 'Frontend Collision' 作为子串，属融合
- **NL**：NL 2 'a possible frontend collision ... is detected'
- **说明**：与簇 0027-2 同源，是融合事件的一个分量侧面。

**0027-8** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：模型未声明 collision_with_pedestrian；融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected 把它作为子串吞并
- **NL**：NL 2 'collision with pedestrian is detected'
- **说明**：与簇 0027-2/0027-7 同源。

**0027-9** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_consumed` ｜ 判定组 G7

- **事实**：制品为 DetectingState -> junction1 : /Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected 与 junction1 -> ActiveState，激活确实以检测事件为条件；触发只能锚在源态 DetectingState，目标态 ActiveState 本就不应消费该事件
- **NL**：NL 2 要求检测到碰撞时子机激活——该条件化激活在制品中已成立
- **说明**：谓词锚点错置产生的假阳性，'激活转换锚定错位' 与制品相反；不涉及新缺陷

**0027-10** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：模型未声明 possible_frontend_collision_is_detected；只有融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected
- **NL**：NL 2 'a possible frontend collision ... is detected'
- **说明**：与簇 0027-7 是同一发现的措辞变体，与簇 0027-2 同源。

**0027-11** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：模型未声明 collision_with_pedestrian_is_detected；只有融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected
- **NL**：NL 2 'collision with pedestrian is detected'
- **说明**：与簇 0027-8 是同一发现的措辞变体，与簇 0027-2 同源。

**0027-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `edge_declared/event_declared` ｜ 判定组 G7

- **事实**：三个 event_declared 分量成立：制品只有融合事件 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected；但 edge_declared 分量要求 ActiveState -> ActiveState 自环，制品中 ActiveState 根本没有任何出边
- **NL**：NL 2 要求三类碰撞各自可使子机激活
- **说明**：融合部分成立且与簇 0027-2 同源；ActiveState 自环这一分量无 NL 依据——NL 2 要的是从检测态进入 ActiveState，不是 ActiveState 上的自触发，归并时应剥离该分量。

**0027-13** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G7

- **事实**：possible_frontend_collision_detected 与 collision_with_pedestrian_detected 均未声明；制品 stm_text 中唯一事件声明是 Frontend_Collision_or_Rear_end_Collision_or_Collision_with_Pedestrian_detected
- **NL**：NL 2 分别点名 frontend collision 与 collision with pedestrian 两个检测刺激
- **说明**：与簇 0027-2/0027-7/0027-8 同源。

## pair 0029 — 27 簇　`表示债务×20 无×7`

**0029-1** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：融合事件 display name 用 | 析取四项，无独立 pedestrian_detected
- **NL**：NL 12 用 or 逐字列出四个替代激活原因
- **说明**：与 0029-2/3/4/22/23/25/26 同源。

**0029-2** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：第二析取项无独立事件
- **NL**：NL 12
- **说明**：同源。

**0029-3** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：第三析取项无独立事件
- **NL**：NL 12
- **说明**：与 0029-22 同一主张不同拼写。

**0029-4** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：第四析取项无独立事件
- **NL**：NL 12
- **说明**：与 0029-23 同一主张。

**0029-5** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：融合事件 display 为 front_inactive & rear_inactive & pedestrian_inactive（合取）
- **NL**：NL 13 用 and 合取，且称其为 conditions（守卫谓词）
- **说明**：拆成独立事件会把 AND 变 OR，反违反 NL；正确缺口是 V，见 0029-16

**0029-6** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：无独立 rear_inactive
- **NL**：NL 13 合取
- **说明**：同源；正确框架见 0029-17

**0029-7** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：无独立 pedestrian_inactive
- **NL**：NL 13 合取
- **说明**：同源；正确框架见 0029-18

**0029-8** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：全模型唯一变量是注入的 R45RouteToken
- **NL**：NL 2/11 写成变量取值比较
- **说明**：与 0029-9~18/24 同源，可归并为一条 V 缺失；台账 5 条无一涉及变量。

**0029-9** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：无 urban_way 变量
- **NL**：NL 2/11
- **说明**：同源。

**0029-10** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：dist_to_front 只在事件名中
- **NL**：NL 3/5/7/9/12 同一量四个阈值
- **说明**：同源；危害最重，四阈值互不相关。

**0029-11** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：extra_lane 只作事件名后缀
- **NL**：NL 3/5/7/9
- **说明**：同源。

**0029-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：无 auto_finished 变量
- **NL**：NL 6/10
- **说明**：同源。

**0029-13** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：无 intersection 变量
- **NL**：NL 7
- **说明**：同源。

**0029-14** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：dist_to_rear 只在融合事件名内
- **NL**：NL 12
- **说明**：同源。

**0029-15** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：vel 只在融合事件名内
- **NL**：NL 12
- **说明**：同源。

**0029-16** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：front_inactive 只在融合事件名内，无变量
- **NL**：NL 13 明确称之为 condition，对应 M 的 V
- **说明**：取变量框架，弃 0029-5。

**0029-17** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：rear_inactive 无变量
- **NL**：NL 13
- **说明**：取变量框架，弃 0029-6。

**0029-18** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：pedestrian_inactive 无变量
- **NL**：NL 13
- **说明**：取变量框架，弃 0029-7。

**0029-19** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：只有 dist_to_front_25_extra_lane_true（display 含 &）
- **NL**：NL 5 显式合取
- **说明**：拆开会把 AND 变 OR；真正缺口是变量 0029-10

**0029-20** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：extra_lane 只作合取分量
- **NL**：NL 3/5/7/9 均用 and
- **说明**：正确缺口是变量 0029-11

**0029-21** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：无独立 dist_to_front_15 事件
- **NL**：NL 7/9 合取
- **说明**：正确缺口是变量 0029-10

**0029-22** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：析取项无独立事件
- **NL**：NL 12
- **说明**：与 0029-3 同一主张。

**0029-23** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：析取项无独立事件
- **NL**：NL 12
- **说明**：与 0029-4 同一主张。

**0029-24** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G1

- **事实**：pedestrian_detected 无变量声明
- **NL**：NL 12 把它归为 condition
- **说明**：与 0029-1 合为一条，勿双计。

**0029-25** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：四项确因融合缺失
- **NL**：NL 12 四项 or 并列
- **说明**：聚合越界纳入了合取分量；归并时只保留析取子集。

**0029-26** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：四目标恰为融合事件四个 | 分量
- **NL**：NL 12
- **说明**：表述最准确的一条。

**0029-27** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G1

- **事实**：三目标只存在于合取融合事件中
- **NL**：NL 13 合取
- **说明**：元素种类判错，应为 V

## pair 0030 — 1 簇　`表示债务×1`

**0030-1** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `variable_declared` ｜ 判定组 G2

- **事实**：唯一变量是 R45RouteToken；阈值折叠成事件名 front_distance_10
- **NL**：NL 4 逐字点名 front_distance 并做数值比较
- **说明**：0030 台账三条均未覆盖变量侧。

## pair 0032 — 5 簇　`假阳性×3 无×2`

**0032-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：制品事件为 start、Accelerate、Brake、Reach_Speed、Stop、keyOff，确无 user_actions；但这些正是 NL 所指的具体用户动作
- **NL**：NL 1 'based on user actions' 是对后续具体动作的集合性指代，未点名一个叫 user_actions 的刺激
- **说明**：要求一个通用刺激入口属过度规约

**0032-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：确无 power_on 事件，但制品有 OffState --start--> OperateState（event start named 'start'），即 NL 1 的上电进入 Operate 已被承载
- **NL**：NL 2 'The system can be turned on with the `start` signal' 直接把开机信号命名为 start，NL 1 的 powered on 与之同指
- **说明**：0032 人工复核 diff#0 判该顶层骨架 correct；同 pair 家族的 0052-1 主张相同。注意另一份 NL（0010/0020/0040 族）里 power on 才是独立点名刺激，不可跨 NL 套用

**0032-3** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：制品声明了 event Accelerate named 'Accelerate'，即本条所指的加速动作刺激已存在，只是形态为 Accelerate 而非 accelerating
- **NL**：NL 3 'actions like accelerating, braking, or stopping' 用 like 举例，未规定事件的精确拼写
- **说明**：纯命名形态差异；与簇 0032-4/5 同源

**0032-4** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：制品声明了 event Brake named 'Brake'
- **NL**：NL 3 同上
- **说明**：与簇 0032-3 同源

**0032-5** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：制品声明了 event Stop named 'Stop'
- **NL**：NL 3 同上
- **说明**：与簇 0032-3 同源

## pair 0033 — 4 簇　`无×4`

**0033-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G8

- **事实**：路径中确无 PumpControl.substates；PumpControl 下只有投影插入的 InvalidInitialtr_0005 / 0007 / 0009
- **NL**：NL 1『it can transition to different substates』中的 substates 是普通名词，NL 2 随即把三个子状态具名为 PumpState / WaterState / MethaneState，NL 从未要求一个名为 substates 的元素
- **说明**：命名字面主义。真正的层次缺陷已由台账 EIS-0033-01（三者被声明为 PumpControl 的兄弟）记录，本簇不是它的有效表述

**0033-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G8

- **事实**：PumpState 确为无 during 动作的状态声明；但模型另行声明了事件 Activate_Pump 与 Pump_Deactivated 承载泵的启停行为
- **NL**：NL 3『where the pump is activated or controlled』是对该子状态含义的说明，未规定该行为必须以 during 相位动作实现（entry 动作或触发事件同样满足）
- **说明**：相位过度指定。与簇 0033-3/4 同源

**0033-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G8

- **事实**：WaterState 无 during 动作；但模型声明了事件 Monitor_Water_Flow 与 Water_Flow_Stabilized 承载水流监控行为
- **NL**：NL 4『indicating that the pump is controlling or monitoring the water flow』是对状态语义的注解，未要求 during 相位动作
- **说明**：与簇 0033-2/4 同源

**0033-4** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G8

- **事实**：MethaneState 无 during 动作；但模型声明了事件 Monitor_Methane_Flow 与 Methane_Flow_Stabilized 承载甲烷流监控行为
- **NL**：NL 5『indicating that the pump is controlling or monitoring the methane flow』是对状态语义的注解，未要求 during 相位动作
- **说明**：与簇 0033-2/3 同源

## pair 0034 — 2 簇　`假阳性×1 无×1`

**0034-1** ｜ ❌ 假阳性 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：台账 EIS-0034-03 逐字确认 FCSTM 有 Accelerating { enter abstract Accelerate; }
- **NL**：NL 8 明确称其为 action，未要求名为 Entry_Accelerate 的事件
- **说明**：真缺陷是动作错置到 DoorsClosing，已由 EIS-0034-03 记录

**0034-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：无 motion_begins 事件
- **NL**：NL 8 when motion begins 是散文；NL 1 已把该时机具名为 Closed/SendDeparted
- **说明**：字面短语被误当具名信号

## pair 0036 — 8 簇　`无×4 表示债务×4`

**0036-1** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `state_declared` ｜ 判定组 G6

- **事实**：顶层子为 InitialState/Region1/Region2，无 Flight 状态；Region2.AttackReady（body: Ready for Task Assignment）对应参考 region2 的待命/飞行态
- **NL**：NL 4 During flight 是环境性时段限定，未点名为可占据状态
- **说明**：0036 人工复核 diff#6 判 Region2 与参考同构为 correct；与 0036-4/5/9 同源

**0036-2** ｜ ⚙️ 表示债务 ｜ 5/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：model.fcstm 无任何作者变量（全语料 60 份制品（33 份只含注入的 R45RouteToken，另 27 份无任何 def）的 def 只有 R45RouteToken），但作者源 stm0.puml 写的是 'Attack --> AttackReady : Attack Complete / UAV Count Decreased'，递减以 UML 标准 trigger / effect 槽位表达；FCSTM 未切分 / 是前端 lowering 债务
- **NL**：NL 4 'the number of UAVs in the swarm decreases accordingly' 要求递减，作者源已表达
- **说明**：0036 人工复核 diff#4 逐字判『作者源已表达…属表示债务。台帐判 E3 正确』，台账 status=representation_boundary；对照 0006 的真缺陷（EXP-0006-EA-001）是作者源里连递减文本都没有。与簇 0036-6/7 同源。

**0036-3** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：作者源 stm0.puml 的标签 'Attack Complete / UAV Count Decreased' 在 UML 记法上已把触发与效果分开，正是本条 rationale 要求的修法；融合成单一事件名 Attack_Complete_UAV_Count_Decreased 发生在 FCSTM lowering（fcstm_meta 声明 R45.DEBT.opaque_transition_label_semantics），不是作者把效果嵌进事件名
- **NL**：NL 4 'After completing the attack' 确点名该刺激，但制品已在 / 前给出该触发
- **说明**：与簇 0036-2 同源，同属 E3 表示债务；本条主张与制品相反。

**0036-4** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `state_declared` ｜ 判定组 G6

- **事实**：无小写 flight 状态，与簇 0036-1 同一事实
- **NL**：NL 4 'During flight' 未要求独立状态
- **说明**：与簇 0036-1 同源，仅大小写不同

**0036-5** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G6

- **事实**：制品确无 source=flight 的边；但存在 Region2.AttackReady -> Region2.Attack : /Task_Assignment_Received，NL 4 的行为义务已由它承载
- **NL**：NL 4 只要求『收到任务分配信息则进入攻击状态』，未规定源状态必须叫 flight
- **说明**：该断言的 source 绑定依赖簇 0036-1 虚构的 flight 状态；0036 人工复核 diff#6 判该边 correct。与簇 0036-9 同源

**0036-6** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `effect_declared` ｜ 判定组 G6

- **事实**：Attack -> AttackReady : /Attack_Complete_UAV_Count_Decreased 确无 effect{} 块，但该 effect 在作者源里写在 / 之后（'Attack Complete / UAV Count Decreased'），缺失来自前端未切分 /
- **NL**：NL 4 要求攻击完成后数量减少，作者源已在 effect 槽位表达
- **说明**：与簇 0036-2 同源；此谓词在 0006/0026/0046 是真缺陷断言，区别在那几例作者源无任何递减文本，0036 有。

**0036-7** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G6

- **事实**：与簇 0036-2 同一事实，仅变量命名换成 number_of_UAVs_in_the_swarm
- **NL**：NL 4 同上
- **说明**：与簇 0036-2 同源，属同一 E3 表示债务的重复表述。

**0036-9** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G6

- **事实**：与簇 0036-5 同一事实，仅 source 大写为 Flight
- **NL**：NL 4 未规定源状态名
- **说明**：与簇 0036-5 同源

## pair 0037 — 1 簇　`无×1`

**0037-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G5

- **事实**：声明表确无 ActiveState.collision_avoidance_controls——事实成立；但同层已声明三个具体控制 FrontendCollisionRegion.BrakingControl、RearEndCollisionRegion.SteeringControl、PedestrianCollisionRegion.EmergencyStop
- **NL**：NL 3 『concurrent activation different of collision avoidance controls』中 'collision avoidance controls' 是指代这些具体控制的复数普通名词，NL 未要求存在一个与该短语整体同名的状态或集合元素
- **说明**：字面抽名导致的过度规定，与 0046-7/0006-1 的 Flight 同一模式

## pair 0039 — 21 簇　`表示债务×16 无×5`

**0039-1** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：pedestrian_detected 只作融合名子串
- **NL**：NL 12 析取列举
- **说明**：与 0039-2/3/4/6/7/8/17/19 同源。

**0039-2** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：dist_to_rear_5_vel_30 仅子串
- **NL**：NL 12
- **说明**：同源。

**0039-3** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：HighwayMode 前距无独立事件
- **NL**：NL 12
- **说明**：与 0039-7/17 同一元素。

**0039-4** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：UrbanMode 前距仅尾段
- **NL**：NL 12
- **说明**：与 0039-8 同一元素。

**0039-5** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：只有 front_inactive_rear_inactive_pedestrian_inactive
- **NL**：NL 13 逐个点名
- **说明**：合取融合 ｜【R-CONJ】NL 13 合取，事件框架指向错误修法；归入变量缺口。

**0039-6** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：四触发全为子串
- **NL**：NL 12
- **说明**：roll-up，与 0039-19 重复。

**0039-7** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无独立 dist_to_front_15_in_HighwayMode
- **NL**：NL 12
- **说明**：与 0039-3/17 同一缺陷。

**0039-8** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无独立 dist_to_front_10_in_UrbanMode
- **NL**：NL 12
- **说明**：与 0039-4 同一缺陷。

**0039-9** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无独立 front_inactive
- **NL**：NL 13
- **说明**：同源 ｜【R-CONJ】NL 13 合取，事件框架指向错误修法；归入变量缺口。

**0039-10** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无独立 rear_inactive
- **NL**：NL 13
- **说明**：同源 ｜【R-CONJ】NL 13 合取，事件框架指向错误修法；归入变量缺口。

**0039-11** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无独立 pedestrian_inactive
- **NL**：NL 13
- **说明**：同源 ｜【R-CONJ】NL 13 合取，事件框架指向错误修法；归入变量缺口。

**0039-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：只有 dist_to_front_25_extra_lane_true；除 R45RouteToken 外无变量
- **NL**：NL 3/5 分别命名两条件
- **说明**：合取压合后 NL 3 分支不可表达。

**0039-13** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：extra_lane_true 仅子串
- **NL**：NL 3/5/7/9
- **说明**：同源。

**0039-14** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：只有 dist_to_front_15_extra_lane_true
- **NL**：NL 7/9
- **说明**：与 0039-3/7/17 的 NL 依据不同。

**0039-15** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 dist_to_front_lt_25
- **NL**：NL 3/5
- **说明**：与 0039-12 同一缺陷。

**0039-16** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 dist_to_front_lt_15
- **NL**：NL 7/9
- **说明**：与 0039-14 同一缺陷。

**0039-17** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 dist_to_front_15_highway
- **NL**：NL 12
- **说明**：与 0039-3/7 同一缺陷。

**0039-18** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `initial_target/state_declared` ｜ 判定组 G4

- **事实**：事实为真：model.fcstm:94/95 两状态声明在根状态直属层，与 model.fcstm:16 的 AutonomousMode 平级，无复合容器。作者源同样没有——stm0.puml 全文仅三处 `state X {`（4/10/24 行），碰撞避免部分在 44/46/48 行以顶层裸迁移写出，故非表示债务。对照 0049 作者在 stm0.puml:37 写了 `state CollisionAvoidance {`，可见是作者写法差异
- **NL**：NL 12/13 只逐字点名两个状态名；『the collision avoidance system』是指代子系统的统称词，NL 未要求存在同名复合状态，也未规定其层次归属
- **说明**：把 NL 的统称词当被点名元素，是 N1 命名字面主义的典型形态。⚠️ 不判越界：`grep -cE '^[[:space:]]*--[[:space:]]*$' stm0.puml` = 0，源内无正交区，按 R-REGION 与 0037-1/0007-1 先例走单区读法；且本簇主张的是 containment/层次，属 M 内对象，未主张区数量义务或 invariant。

**0039-19** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：四者均子串
- **NL**：NL 12
- **说明**：与 0039-6 重复。

**0039-20** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：两条件均无独立声明
- **NL**：NL 3/5
- **说明**：roll-up。

**0039-21** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：两条件均不存在
- **NL**：NL 7/9
- **说明**：同源。

## pair 0043 — 1 簇　`表示债务×1`

**0043-1** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `reaches` ｜ 判定组 G4

- **事实**：PumpControl.UnspecifiedInitial 存在，PumpState 在更深一层 Region1 下
- **NL**：NL 1+3 要求 PumpState 为首个进入的子态
- **说明**：台账 EIS-0043-01 审 containment，本条审初始入口与冷启动可达，未覆盖。

## pair 0044 — 3 簇　`假阳性×2 无×1`

**0044-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G2

- **事实**：路径列表不含动作声明，无法核验 EmergencyStopping 相位
- **NL**：NL 3 未逐字规定 entry 相位
- **说明**：需 FCSTM 动作块。

**0044-3** ｜ ❌ 假阳性 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：无独立事件 Send
- **NL**：NL 9 要求的是输出动作不是输入事件
- **说明**：同句在 0034 被台账 EIS-0034-04 按输出动作缺失记录。

**0044-4** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `stays_in` ｜ 判定组 G2

- **事实**：`transition:7` 原文是 model.fcstm:19 `Accelerating -> Cruising : /Reached_Cruising_Cruise;`——**不是 Approaching 的出边**（Approaching 只有 index 12 与 15）。实跑 SimulationAPI 钉在 Approaching 投喂 Reached_Cruising_Cruise：consumed=[]、unconsumed=[该事件]、fired=[]、active=[root,InMotion,InMotion.Approaching]——**机器原地未动，仍在 Approaching**。对照钉在 Accelerating 投同一事件则 consumed 并进入 Cruising
- **NL**：NL 5 把该信号绑死在 Accelerating→Cruising；NL 未要求 Approaching 上有该事件的自环
- **说明**：断言主张「运行离开了 Approaching、trace 指向 transition:7」与制品完全相反：没有任何迁移被触发，事件被忽略，Approaching 持续活动。两个谓词侧成因：① `predicate_api.py:1404-1405` 的 `if trigger not in self._consumed(view): return False` 按设计把「事件被忽略」直接判 False；② `predicate_api.py:664-672` 的 `if not fired and unconsumed:` 分支在「什么都没发生」时把锚点落到**声明该事件的**迁移上，于是 model_refs 出现 transition:7，被生产者误读成 fired trace。旁证：同一记录里 occupancy_after 的 model_refs 与它逐字相同却 result=True，说明该锚点是静态查表不是执行轨迹。取假阳性而非无 NL 依据，因「主张与制品相反」这一条更强更靠前。⚠️ 谓词侧待修：stays_in 把「事件被忽略」与「离开了状态」压成同一个 False。与 0044-2 不同源。

## pair 0046 — 9 簇　`表示债务×5 无×4`

**0046-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G5

- **事实**：证据包只给出路径表（状态/事件/变量），不暴露 during/entry/exit 动作，无法从中核验 UAVSwarmStateMachine.SearchRegion.Searching 是否声明了 during 动作；路径表中该状态名也未带 rationale 所述的 '[PlantUML body] Target Search State' 注解
- **NL**：NL 2 『continuously performs target search tasks』——是否必须落成 during 动作、还是由驻留 Searching 状态本身表达，NL 未明示
- **说明**：缺的是动作声明清单（或制品源文本）与参考模型的动作承载方式；补上任一即可裁定。

**0046-2** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表中唯一变量是编译器路由变量 R45RouteToken，不存在 uav_count 或任何语义等价的作者变量
- **NL**：NL 4 『the number of UAVs in the swarm decreases accordingly』明确点名一个可跟踪数量
- **说明**：V 属 M 边界内；与簇 0046-6（同一变量的另一命名）、0046-3（该变量上的效应）同源；姊妹 pair 0006 的台账以 EIS-0006-02 记录了同一 NL 句的缺口，0046 台账遗漏。

**0046-3** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `effect_declared` ｜ 判定组 G5

- **事实**：uav_count 变量在声明表中根本不存在（仅 R45RouteToken），故 Attacking 上以 Attack_Completed_UAV_Count_Decreased 触发的迁移不可能带对 uav_count 的负向效应
- **NL**：NL 4 『After completing the attack, the number of UAVs in the swarm decreases accordingly』
- **说明**：与姊妹 pair 台账 EIS-0006-02[effect_declared] 同缺陷类；0046 台账未枚举；与簇 0046-2/6 同根，去重时应合并为一条『计数量与其递减效应整体缺失』。

**0046-4** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：声明表只有 Attack_Completed_UAV_Count_Decreased，无独立 Attack_Completed；事件名把触发（攻击完成）与效应（数量减少）焊在一起
- **NL**：NL 4 把二者明确分成触发与后果两段：『After completing the attack, the number of UAVs ... decreases』
- **说明**：效应被编码进事件名是 0046 的核心融合缺陷；与簇 0046-9 同源（同一事件的另一命名）

**0046-5** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G5

- **事实**：声明表中根本没有名为 Flight 的状态（只有 UAVSwarmStateMachine.SearchRegion.{Idle,Searching,Attacking,FormationAdjustment} 与 MissionRegion.{MissionActive,MissionComplete}），故以 Flight 为源的边不可能存在——事实成立
- **NL**：NL 4 『During flight』是叙事性运行语境，NL 全文未把 flight 命名为状态；NL 只要求 Task_Assignment_Received 时进入 attack 状态，未限定源状态名
- **说明**：断言把源钉死在一个 NL 未要求的状态上，属过度规定；若改判源为 Searching 才是可核验的关系义务，但本包无迁移表，无法核验该弱化版本。与簇 0046-7 同源

**0046-6** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表无任何表示集群规模的作者变量，仅 R45RouteToken
- **NL**：NL 4 『the number of UAVs in the swarm』
- **说明**：与簇 0046-2 是同一缺失的两种命名（uav_count / number_of_UAVs_in_the_swarm），去重时必须合并，不得计两次。

**0046-7** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `state_declared` ｜ 判定组 G5

- **事实**：声明表确无 Flight 状态——事实成立
- **NL**：NL 4 『During flight』为语境状语，NL 未把飞行命名为一个状态；NL 命名的状态语义只有 search / formation adjustment / attack
- **说明**：字面抽名导致的过度规定；与簇 0046-5、以及 pair 0006 的簇 0006-1/0006-4 同一模式，建议按同一误报模式统一处理

**0046-8** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `persists_until` ｜ 判定组 G5

- **事实**：persists_until(Searching, release=active(MissionComplete), bound=5) 为 False 事实成立：模型确有经 Intercepted / Task_Assignment_Received 在 MissionComplete 之前离开 Searching 的路径
- **NL**：NL 3、NL 4 恰恰明确要求这些离开（被拦截→formation adjustment；收到任务分配→attack），故 NL 不要求 Searching 持续占用到任务完成
- **说明**：该性质与 NL 3/4 直接冲突，是断言把 NL 2 的『continuously』误读成状态驻留不变式；不是制品缺陷

**0046-9** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：声明表无 Completing_the_attack，也无任何只表示『攻击完成』的事件；只有融合事件 Attack_Completed_UAV_Count_Decreased
- **NL**：NL 4 『After completing the attack』
- **说明**：与簇 0046-4 是同一缺失的两种命名，去重时必须合并。

## pair 0047 — 8 簇　`无×8`

**0047-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：事件仅 Brake_Applied/Collision_Avoided/Collision_Detected
- **NL**：NL 2 并列点名三种检测
- **说明**：CAS 下有三子态，单一 Collision_Detected 无法决定进哪个；不依赖并发。

**0047-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 RearEnd_Collision_Detected
- **NL**：NL 2
- **说明**：同源。

**0047-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 Pedestrian_Collision_Detected
- **NL**：NL 2
- **说明**：同源。

**0047-4** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 possible_frontend_collision
- **NL**：NL 2
- **说明**：与 0047-1/7 同一缺陷。

**0047-5** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无追尾专用检测事件
- **NL**：NL 2
- **说明**：绑定名 rear 是截断标识符，但缺陷实体成立。

**0047-6** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 collision_with_pedestrian
- **NL**：NL 2
- **说明**：同源。

**0047-7** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：无 frontend_collision
- **NL**：NL 2
- **说明**：同源。

**0047-8** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G4

- **事实**：三个分型检测一个都没有
- **NL**：NL 2
- **说明**：roll-up。

## pair 0049 — 25 簇　`表示债务×14 无×11`

**0049-1** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：四者均只作融合事件子串
- **NL**：NL 12 析取列举
- **说明**：析取融合语义损失确凿。

**0049-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：只有 front_inactive_rear_inactive_pedestrian_inactive
- **NL**：NL 13 三者反引号点名（and 合取）
- **说明**：⚠️G2 判 VALID，G1 对同形 0029-5/6/7 判 NO_NL_BASIS——待主判裁决。

**0049-3** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：pedestrian_detected 仅前缀子串
- **NL**：NL 12
- **说明**：同源。

**0049-4** ｜ ⚙️ 表示债务 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：dist_to_rear_5_vel_30 仅中段子串
- **NL**：NL 12
- **说明**：同源。

**0049-5** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：front_inactive 仅前缀子串
- **NL**：NL 13
- **说明**：同 0049-2。

**0049-6** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：HighwayMode 前距仅子串
- **NL**：NL 12
- **说明**：与 0049-24 同源。

**0049-7** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：UrbanMode 前距仅末段
- **NL**：NL 12
- **说明**：与 0049-25 同源。

**0049-8** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：rear_inactive 仅中段子串
- **NL**：NL 13
- **说明**：同 0049-2。

**0049-9** ｜ 📄 无 NL 依据 ｜ 4/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：pedestrian_inactive 仅末段子串
- **NL**：NL 13
- **说明**：同 0049-2。

**0049-10** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：model.fcstm:5 `event dist_to_front_25 named "dist_to_front>=25";` —— 比较符在编译产物里逐字保留，与作者源 stm0.puml:10 `enter_hwy --> cruise : dist_to_front>=25` 完全一致；互补分支同样在场：model.fcstm:6 `event dist_to_front_25_extra_lane_true named "dist_to_front<25 && extra_lane=true"`
- **NL**：NL 3/5 要求的 `<25 && extra_lane` 恰好落在通往 lane_change 的边上，制品已满足
- **说明**：断言主张「无法判定是 <25 还是 >=25 的投影」，而 discover 所读的同一份 model.fcstm 第 5 行 named 串就写着 `dist_to_front>=25`，主张与制品相反 → 事实为假 → 假阳性（表示债务的首要条件「事实为真」不成立）。旁证：台账 EIS-0019-01 自述「0009/0049 靠互补守卫消歧」——这条 >=25 正是台账认定的正确写法，被本簇当缺陷报。

**0049-11** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：extra_lane_true 只作后缀子串
- **NL**：NL 3/5/7/9 每次出现都与距离阈值合取
- **说明**：真正缺口是变量，见 0049-15

**0049-12** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：无裸 dist_to_front_15
- **NL**：NL 7/9 始终与 extra lane 合取
- **说明**：与 0049-23 同源；实质缺口见 0049-14

**0049-13** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：七个条件全为子串
- **NL**：NL 12+13
- **说明**：是 0049-1 与 0049-2 的并集，归并时合为一条。

**0049-14** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G2

- **事实**：唯一变量是 R45RouteToken，阈值烘焙进事件名
- **NL**：NL 3/5/7/9/12 同一量多阈值
- **说明**：属 M 的 V，在边界内。

**0049-15** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G2

- **事实**：无 extra_lane 变量
- **NL**：NL 3/7/9
- **说明**：同源；是 0049-11/20 的正确刻画。

**0049-16** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G2

- **事实**：无 dist_to_exit 变量
- **NL**：NL 4/5/8
- **说明**：同源。

**0049-17** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G2

- **事实**：无 dist_to_rear 变量
- **NL**：NL 12
- **说明**：同源。

**0049-18** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G2

- **事实**：无 vel 变量
- **NL**：NL 12
- **说明**：同源。

**0049-19** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：无名为 dist_to_front 的事件
- **NL**：NL 中它一律是被比较的数值量，对应 V 而非 E
- **说明**：正确形态见 0049-14

**0049-20** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：无名为 extra_lane 的事件
- **NL**：NL 3 写成条件
- **说明**：正确形态见 0049-15

**0049-21** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：模式限定前距危险只埋在融合事件里
- **NL**：NL 12 独立析取触发源
- **说明**：事件名系模型自拟但实质主张成立。

**0049-22** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：确无标识符为 dist_to_front_lt_25 的独立事件；但 NL 要求的条件本身在场：model.fcstm:6 的 `dist_to_front<25 && extra_lane=true`，挂在 model.fcstm:27/30 两条通往 lane_change 的边上；作者源 stm0.puml:11/14 逐字同形
- **NL**：NL 3 与 NL 5 两处出现 `dist_to_front<25` 时都与 `extra_lane=true` 合取，NL 全文无一处把它作为独立触发源
- **说明**：实质诉求是把合取式拆成裸事件，适用 R-CONJ：拆开会把 AND 变 OR，指向错误修法。与同 pair 的 15 米孪生簇 0049-12/0049-23 同口径。⚠️ 与同源的 0049-10 分裁：0049-10 断言「比较符不可判定」被 named 串直接证伪（事实为假→假阳性），本簇陈述的「无该标识符」字面为真（事实为真→无 NL 依据）

**0049-23** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：无裸 dist_to_front_15 事件
- **NL**：NL 7/9 恒与 extra lane 合取
- **说明**：与 0049-12 同源

**0049-24** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：只作融合事件子串
- **NL**：NL 12
- **说明**：与 0049-6 同源。

**0049-25** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G2

- **事实**：只作融合事件末段
- **NL**：NL 12
- **说明**：与 0049-7 同源。

## pair 0050 — 1 簇　`表示债务×1`

**0050-1** ｜ ⚙️ 表示债务 ｜ 6/6 格 ｜ `variable_declared` ｜ 判定组 G4

- **事实**：只有事件 _front_distance_10，无变量 front_distance
- **NL**：NL 4 逐字命名该量并与阈值 10 比较
- **说明**：台账 EIS-0050-01 未涉及，属真漏记。

## pair 0052 — 2 簇　`无×2`

**0052-1** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：制品事件为 start、accelerate、brake、stop、keyOff、shutdown，确无 power_on；但 Off -> Operate : /start 已承载 NL 1 的上电进入 Operate
- **NL**：NL 2 'The system can be turned on with the `start` signal' 把开机信号命名为 start
- **说明**：0052 盲审 blindB 逐句核对写明 NL 1『满足——Off --start--> Operate』；该 pair 人工复核 problem_count=0、台账 no_supported_finding。与簇 0032-2 同源

**0052-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `initial_target` ｜ 判定组 G6

- **事实**：Operate 复合态确有已声明的默认入口 [*] -> Idle（三个子态 Idle、Accelerating_or_Cruising、Braking 齐备），入口不指向 AoC/Braking 属实但并非缺省缺失
- **NL**：NL 1 列举 Idle、Accelerating or Cruising、Braking 三态之间按用户动作迁移，未规定进入 Operate 的默认子态必须是 AoC 或 Braking
- **说明**：0052 人工复核 diff#2 判『复合态、默认子态 Idle 与 NL 第 1 句点名的三个子态齐备』为 correct；盲审亦将 [*] --> Idle 列为良构性通过项

## pair 0053 — 2 簇　`无×2`

**0053-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G3

- **事实**：WaterRegion.WaterState 无 during 动作也无子态
- **NL**：NL 4 含义说明；NL 2 只要求三个子态存在，模型已满足
- **说明**：NL 全文未对任何状态提出动作声明义务

**0053-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `action_declared` ｜ 判定组 G3

- **事实**：MethaneRegion.MethaneState 无 during 动作也无子态
- **NL**：NL 5 含义说明
- **说明**：与 0053-1 同源

## pair 0054 — 5 簇　`假阳性×3 无×2`

**0054-2** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：路径已声明 _obstacle_detected，与所求 obstacle_detected 仅差前导下划线
- **NL**：NL 2/3 要求该输入触发，模型已有
- **说明**：纯精确名匹配假阳性

**0054-3** ｜ ❌ 假阳性 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：只有输入触发 _obstacle_detected，无任何承载 Obstacle Detected 输出信号的名字（对比 0024 有两个）
- **NL**：NL 3 sends the Obstacle Detected signal
- **说明**：同类在 0024 已被台账记为 EIS-0024-04，0054 台账 0 条故为漏记。

**0054-4** ｜ ❌ 假阳性 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：路径确无名为 Send 的事件；但 rationale 自陈 Approaching 声明了 during 动作，无法判断该动作是否即 Send
- **NL**：NL 9 要求输出动作而非输入事件
- **说明**：需补取 InMotion.Approaching 的 during 动作原文后重判。

**0054-5** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `persists_until` ｜ 判定组 G3

- **事实**：断言以 `release=false` 执行，语义为「必须永远停留在 Approaching」。模型有终止路径，故求值为 False——事实成立。
- **NL**：NL 10「remains ... until it is ready to stop or decelerate」是**定性描述**且明确带释放条件；NL 2/10 恰恰许可 Approaching → Stopping。NL 从未要求无限驻留。
- **说明**：定性表述被强化为时序不变式：`release=false` 把「保持到某条件」读成「永远保持」。

**0054-6** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G3

- **事实**：路径无 motion_begins；进入 InMotion 的触发 Closed_SendDeparted 已声明
- **NL**：NL 8 when motion begins 是描述性状语，唯一点名的元素是 Entry/Accelerate 动作
- **说明**：过度规定

## pair 0055 — 1 簇　`无×1`

**0055-1** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表确无 zero_time 变量（唯一变量为 R45RouteToken）；零时间条件被烧进事件名 Door_Closed_time_0
- **NL**：NL 4 『if the door is closed with zero time set』中 'zero time' 是烹饪时间量的一个取值，不是一个独立被跟踪的量；NL 5 要求跟踪的量是 cooking time（『the cooking time is displayed and updated』）
- **说明**：断言把取值误当量。真正的缺口（无 cooking time 量、timer 启停与显示更新缺失）已由台账 EIS-0055-01 记录，故此处也不构成台账漏记

## pair 0056 — 3 簇　`越界×1 无×1 表示债务×1`

**0056-1** ｜ 🚫 越界 ｜ 4/6 格 ｜ `cardinality` ｜ 判定组 G6

- **事实**：作者源 stm0.puml:10 是正交区分隔符 `--`：SearchState 实为两个区，region0={Area1,Area2,Area3}、region1={NoIntercept,Intercepted}（model.fcstm:9 的 [PlantUML concurrent region 0/1] 标注逐字确认）。NL 2 的 three different state areas 由 region0 的三个 Area 兑现，义务在作者源上已满足；5≠3 只在 R4.5 把两区拍平成兄弟、跨区求和之后才出现。
- **NL**：NL 2 'it operates within three different state areas' —— 按区数读，制品本已是三个
- **说明**：判 OUT_OF_SCOPE，与 0007-3 同型同判。判据：含正交区的制品上，cardinality 主张在 M 内成立当且仅当该违规在『区感知读法』下依然存活。该判据可证伪且先于本裁定存在——0037（源内无 --，7≠3 是单区真实计数）、0002（盈余是游离 InitialState）、0013（盈余是 NL 未枚举的克隆态）三处均按此判据保留在 M 内，方向对方法不利。原 diff#0 与 diff#3 并不真冲突：diff#0 问『三个区够不够』并自带 out_of_scope:concurrency，diff#3 问『多出的两个该不该在』且判 extra；产出主张把 diff#3 的结论挂到了 diff#0 已判无表达力的仪器上。该过度规约的可断言后果已由 EIS-0056-01（guard_distinguishable）承担，再计一条等于同一缺陷数两遍。

**0056-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G6

- **事实**：确无名为 Mission_Complete 的状态，但制品有 event Mission_Complete named 'Mission Complete'，且 Area1/2/3、NoIntercept、Intercepted 均有 -> [*] : /Mission_Complete effect{R45RouteToken=13}，配 SearchState -> [*] : if [R45RouteToken == 13]，完成语义由事件加 final 伪态承载
- **NL**：NL 2 'Before the mission is completed' 预设完成条件，但未要求它是一个状态
- **说明**：0056 人工复核 diff#4 判该编码为 correct，并称『用事件而非 count==0 表达完成条件，比参考更贴 NL 原文』

**0056-3** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G6

- **事实**：作者源 stm0.puml 写的是 'AttackState --> SearchState : Attack Complete [Decrease UAV Count]'，触发 Attack Complete 与方括号内容在 UML 记法上是分开的；融合成 Attack_Complete_Decrease_UAV_Count 发生在 FCSTM lowering（R45.DEBT.opaque_transition_label_semantics）
- **NL**：NL 4 'After completing the attack' 确点名该刺激，制品已在方括号前给出该触发
- **说明**：本 pair 的真缺陷是递减被放进 guard 槽位而非 effect 槽位，已记为 EIS-0056-02（人工复核 diff#2）；本条主张的『事件名融合』是其下游的表示债务，不构成独立新发现。

## pair 0057 — 6 簇　`无×5 假阳性×1`

**0057-1** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_consumed` ｜ 判定组 G8

- **事实**：作者源 stm0.puml:22 `[*] --> CA : Possible collision detected` 只有一条边、一个响应（进 CA）；三个具名事件 :5/:11/:17 分别驱动各区 Idle→Active。事件名是 NL 2 从句去掉三个并列项后的逐字压缩，非自造
- **NL**：NL 2「becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected」——三项析取，期望响应相同（子机变 active）
- **说明**：命中仓库自身 FUSED_EVENT_POLICY.md L379 的许可条件：「合并事件代表多个 NL 备选，只当 source trace 支持同一析取且**期望响应相同**」——两条都满足，故属许可的合并。该判据同时把 0017/0047 干净分开：那两处是同一事件名导向三个**不同**目标（F/R/P），响应不同，不在许可内。0057 反而是该 NL 组里唯一按 L379 正确分工的模型（响应不同处用具名事件，响应相同处用聚合事件）。⚠️ 不判 FALSE_POSITIVE：事实为真，只是义务已被政策许可的形态履行。

**0057-2** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G8

- **事实**：冻结路径中根本不存在名为 Inactive 的状态（顶层只有 CA、Collision_avoided 及四个事件），因此该边的缺失是断言自造前提导致的空洞真
- **NL**：NL 2 只说 sub-machine becomes active，未点名任何 Inactive 前置状态，更未要求 Inactive --X--> CA 这一具体三元组
- **说明**：实质关切与簇 0057-1 同源且 0057-1 已判成立；本簇因锚在不存在的源状态上，作为已发布结论是空洞的，不应单独计为发现。与 0057-3/4 同源

**0057-3** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G8

- **事实**：路径中无 Inactive 状态，边 Inactive --Rear_end_collision_detected--> CA 的缺失系断言自造前提所致
- **NL**：NL 2 未点名 Inactive 状态，也未要求该具体边
- **说明**：与簇 0057-2/4 同源

**0057-4** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `edge_declared` ｜ 判定组 G8

- **事实**：路径中无 Inactive 状态，边 Inactive --Pedestrian_collision_detected--> CA 的缺失系断言自造前提所致
- **NL**：NL 2 未点名 Inactive 状态，也未要求该具体边
- **说明**：与簇 0057-2/3 同源

**0057-5** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `state_declared` ｜ 判定组 G8

- **事实**：路径中确无 CA.collision_avoidance_controls；但 CA.Frontend / CA.RearEnd / CA.Pedestrian 及其 FCActive / RCActive / PCActive 就是三个避撞控制本身
- **NL**：NL 3『collision avoidance controls』是对这三个控制的统称，NL 未要求再设一个同名中间状态
- **说明**：命名字面主义；与 0017-10 同型

**0057-6** ｜ ❌ 假阳性 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G8

- **事实**：路径中已声明 Frontend_collision_detected，它正是 NL 2『a possible frontend collision ... is detected』对应的独立检测事件；断言只因要求的字面名为 possible_frontend_collision 而判 False
- **NL**：NL 2 确有依据，但该义务已被 Frontend_collision_detected 履行
- **说明**：纯命名不匹配导致的假阳性。与 0017-11 判定相反正是因为两 pair 制品不同：0017 只有泛化 collision_detected，0057 已分立三事件

## pair 0059 — 18 簇　`表示债务×11 无×7`

**0059-1** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：路径里有 pedestrian_detected_dist_to_rear_5_vel_30_... 这一融合事件，独立的 pedestrian_detected 确不存在
- **NL**：NL 9 逐字点名 'a pedestrian is detected' 为独立触发条件
- **说明**：与台账 EIS-0030-03 同缺陷类（融合事件），台账对本 pair 未枚举。

**0059-2** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：无独立 _dist_to_rear_5_vel_30；该串仅作为子串出现在四合一融合事件 _pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_highway_dist_to_front_10_in_urban 中
- **NL**：NL 12 逐字给出 `dist_to_rear<5 & vel>30` 作为并列的激活触发之一
- **说明**：与簇 0059-1 同源（同一融合事件的第二个分支）

**0059-3** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：无独立 _dist_to_front_15_in_highway；仅作为子串存在于四合一融合事件中（注意 _dist_to_front_15_extra_lane_true 是城市换道条件，非此触发）
- **NL**：NL 12 『the front distance being less than 15 meters in highway mode』
- **说明**：与簇 0059-1 同源（第三个分支）

**0059-4** ｜ ⚙️ 表示债务 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：无独立 _dist_to_front_10_in_urban；仅作为子串存在于四合一融合事件中
- **NL**：NL 12 『... or 10 meters in urban mode』
- **说明**：与簇 0059-1 同源（第四个分支）

**0059-5** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：声明表只有 _front_inactive_rear_inactive_pedestrian_inactive，无独立 _front_inactive
- **NL**：NL 13 逐字点名 `front_inactive` 为解除条件之一
- **说明**：NL 13 为合取，故该条返回迁移行为等价，缺陷在声明层（三个 NL 逐字点名的信号无一被单独声明）；强度弱于 0059-1~4；与 0059-6/7/14 同源。

**0059-6** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：无独立 _rear_inactive，仅存在于 _front_inactive_rear_inactive_pedestrian_inactive
- **NL**：NL 13 逐字点名 `rear_inactive`
- **说明**：与簇 0059-5 同源；合取融合，行为等价，声明层缺陷。

**0059-7** ｜ 📄 无 NL 依据 ｜ 2/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：无独立 _pedestrian_inactive，仅存在于 _front_inactive_rear_inactive_pedestrian_inactive
- **NL**：NL 13 逐字点名 `pedestrian_inactive`
- **说明**：与簇 0059-5 同源；合取融合，行为等价，声明层缺陷。

**0059-8** ｜ ⚙️ 表示债务 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：四个断言对应的 _pedestrian_detected / _dist_to_rear_5_vel_30 / _dist_to_front_15_in_highway / _dist_to_front_10_in_urban 均不在声明表中，只有四合一融合事件
- **NL**：NL 12 用『or』并列四个激活触发
- **说明**：与簇 0059-1/2/3/4 完全同源，只是打包成一条 issue；去重时应合并为一条。

**0059-9** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：整份声明表中唯一的变量是编译器路由变量 R45RouteToken，不存在作者变量 dist_to_front；该量只以子串形式烧进事件名 _dist_to_front_25_extra_lane_true / _dist_to_front_15_extra_lane_true
- **NL**：NL 3/5 给出 `dist_to_front<25`，NL 7/9 给出 `dist_to_front<15`，均为对数值量的比较
- **说明**：本 pair 作者变量数为 0 是系统性缺陷，簇 9-13 是它的五个投影；V 属 M 边界内。若判定政策认为参考模型同样不带变量，需另行核对参考侧再决定归属。

**0059-10** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表无 extra_lane 变量，仅 R45RouteToken；extra_lane 只作为 _dist_to_front_25_extra_lane_true / _dist_to_front_15_extra_lane_true 的名字片段存在
- **NL**：NL 3 『the availability of an extra lane (`extra_lane=true`)』
- **说明**：与簇 0059-9 同源（作者变量词表为空）

**0059-11** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表无 dist_to_exit 变量；只有事件 _dist_to_exit_2 与 _dist_to_exit_0_7
- **NL**：NL 4/5 `dist_to_exit<2`，NL 8 `dist_to_exit<0.7`
- **说明**：与簇 0059-9 同源。

**0059-12** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表无 dist_to_rear 变量，仅 R45RouteToken
- **NL**：NL 12 `dist_to_rear<5`
- **说明**：与簇 0059-9 同源。

**0059-13** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `variable_declared` ｜ 判定组 G5

- **事实**：声明表无 vel 变量，仅 R45RouteToken
- **NL**：NL 12 `vel>30`
- **说明**：与簇 0059-9 同源。

**0059-14** ｜ 📄 无 NL 依据 ｜ 3/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：_front_inactive / _rear_inactive / _pedestrian_inactive 三者均不在声明表中，只有 _front_inactive_rear_inactive_pedestrian_inactive
- **NL**：NL 13 逐字并列三个条件名
- **说明**：与簇 0059-5/6/7 完全同源，打包版；合取融合行为等价，缺陷在声明层。

**0059-15** ｜ ⚙️ 表示债务 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：_pedestrian_detected、_dist_to_rear_5_vel_30、_dist_to_front_15_in_highway_dist_to_front_10_in_urban 三者均未单独声明，只有四合一融合事件
- **NL**：NL 12 的析取分支
- **说明**：与簇 0059-8 同源，只是把前距两档并成一条；去重时合并。

**0059-16** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：声明表有 _dist_to_front_25_extra_lane_true，无独立 _dist_to_front_25
- **NL**：NL 3 括注 `dist_to_front<25` 为一个独立命名条件；NL 5 同名复用
- **说明**：NL 中该条件始终与 extra_lane 合取出现，故行为等价，属声明层/粒度缺陷，强度最弱；根因与簇 0059-9/10（无作者变量，守卫烧进事件名）相同。

**0059-17** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：extra_lane=true 只出现在 _dist_to_front_25_extra_lane_true 与 _dist_to_front_15_extra_lane_true 两个合取事件名内，无独立 _extra_lane_true
- **NL**：NL 3 括注 `extra_lane=true`
- **说明**：与簇 0059-16 同源；NL 从未单独使用该条件，强度弱。

**0059-18** ｜ 📄 无 NL 依据 ｜ 1/6 格 ｜ `event_declared` ｜ 判定组 G5

- **事实**：无独立 _dist_to_front_15；只有 _dist_to_front_15_extra_lane_true（城市换道）与四合一融合事件中的 dist_to_front_15_in_highway 片段
- **NL**：NL 7/9 `dist_to_front<15`
- **说明**：与簇 0059-16/17 同源；合取融合，声明层缺陷。
