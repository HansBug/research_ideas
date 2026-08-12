"""NL 规约的**中文严格翻译**。

⭐ 这份译文是给人**判缺陷**用的，⛔ 不是给人读着舒服用的。翻译纪律：

1. ⭐ **严格直译**，⛔ 不意译、⛔ 不润色、⛔ 不补充原文没有的信息。
2. ⛔ **保留原文的模糊性**。原文没说清的（谁是主语、条件之间是「且」还是「或」、
   源状态是哪个），译文**照样不说清**，只在末尾用 `〔译者存疑：…〕` 点出这里含糊，
   ⛔ 不替它消歧 —— 消歧就是替作者做了本轮要他自己做的判断。
3. ⭐ **技术术语保留英文原词**并在括号里给中文，如 `sub machine state`（子机状态）。
4. ⭐ **状态名 / 事件名 / 变量名一律保留英文原样**，⛔ 不翻译。
5. ⚠️ 原文有语法或拼写错误时**照直译**，并在译文后加 `〔原文如此：…〕` 说明错在哪。
6. ⭐ 段首的编号照抄原文（语料里编号本身就有重复与缺空格，那也是信息）。

⛔ **键是 NL 全文的 sha256 前 12 位 + 段 id**，不是 pair 号 —— 60 个 pair 由 10 份
NL 各生成 6 个制品，同一份 NL 的 6 个 pair 共用同一套译文。若 `nl.txt` 的字节变了，
digest 随之变化，译文会**查不到**而不是被静默套用到改动后的文本上；
[test_relabel.py](./test_relabel.py) 的 `test_every_nl_segment_has_a_chinese_translation`
会把这种情况打成失败。

⛔ 本模块只放译文，**不放任何判断**。译文里出现的 `〔译者存疑〕` 只陈述「原文这里没说清」，
⛔ 不得写成「所以模型应该怎样」—— 那是重标时人要填的东西，不是材料该替他填的。

⚠️ `00x8` 组（digest `6af3966c8b0e`）的 NL 要求 fork/join 与秒级时间约束，按
[nl_scope_rule.md](../../docs/protocol/nl_scope_rule.md) 永久排除，⛔ 不生成工作单，
故本模块**不收**它的译文。
"""

from __future__ import annotations

import hashlib

import sources as S

# digest12 -> {seg_id: 中文严格翻译}
TRANSLATIONS = {

    # ================================================== NL08 · 高层驾驶模块
    # pairs 0000 0010 0020 0030 0040 0050（分段来自 overrides.json 人工标注）
    "f1c3dc88371b": {
        "NL-M001":
            "1 human driving mode（人工驾驶模式）由一个 simple state（简单状态）表示。",
        "NL-M002":
            "2 autonomous mode（自主驾驶模式）拥有 sub-states（子状态），"
            "并由一个 sub machine state（子机状态）表示。",
        "NL-M003":
            "3. 当 power on（上电）时，系统 turn into（转入）human driving mode"
            "〔原文如此：`the system turn into` 主谓不一致，动词未随第三人称单数变位〕"
            "〔译者存疑：原文未说明这条迁移的源端是初始伪状态还是某个具体状态〕",
        "NL-M004":
            "4当 front_distance > 10 时，auto transport to（自动运送到）autonomous state"
            "〔原文如此：`4when` 编号与单词之间缺空格；`transport`（运送）在状态机语境下"
            "疑为 `transition`（迁移）之误，此处照字面译，不代为改写〕"
            "〔译者存疑：原文未说明源状态，也未给出 front_distance 的单位〕",
        "NL-M005":
            "4. 当 receive human steering cmd（接收到人工转向指令）、brake pressed"
            "（制动被踩下）、in (auto final)（处于 (auto final) 之中）时，"
            "transit to（迁移到）human driving mode"
            "〔原文如此：本段编号 `4.` 与上一段的 `4` 重复；`when receive` 缺主语〕"
            "〔译者存疑：三项条件之间只用逗号并列，原文未说明是「或」还是「且」，"
            "译文保留该并列形态不作消歧；`(auto final)` 的括号内容原文未定义〕",
        "NL-M006":
            "5 当 power off（断电）时，it（它）将 transit to（迁移到）final state（终态）"
            "〔译者存疑：`it` 指代整个系统还是上一段提到的 human driving mode，原文未明说；"
            "原文也未说明这条迁移的源端〕",
    },

    # ================================================== NL02 · 列车基础制动装置
    # pairs 0001 0011 0021 0031 0041 0051
    "abb20a2187c1": {
        "NL-L001":
            "1 本状态机模型表示列车的 basic braking device（基础制动装置），"
            "它作为列车制动操作的最终执行单元。",
        "NL-L002":
            "2 当 basic braking device 接收到一个 brake signal（制动信号）时，"
            "它从 the initial state（初始状态）迁移到 the braking state（制动状态）。"
            "若 the signal transmission fails（信号传输失败），它进入 the operational state"
            "（工作状态）。一旦 the signal feedback is sent（信号反馈被发出），"
            "它返回 the initial state。"
            "〔译者存疑：后两句的 `it` 指 basic braking device 还是各自承接前一句提到的状态，"
            "原文未明说；`If the signal transmission fails` 的源状态原文也未给出〕"
            "〔译者存疑：`the initial state` 是一个名为 initial 的普通状态还是初始伪状态，"
            "原文未区分〕",
        "NL-L003":
            "3 在进入 the braking state 之后，系统迁移到 the brake caliper clamping state"
            "（制动钳夹紧状态）。",
    },

    # ================================================== NL06 · 泵控制
    # pairs 0002 0013 0023 0033 0043 0053
    "a391765dba93": {
        "NL-L001":
            "1. 系统起始于 the PumpControl state，从该状态出发，"
            "它可以基于 specific conditions（特定条件）迁移到不同的 substates（子状态）。"
            "〔译者存疑：原文未给出这些 `specific conditions` 究竟是什么〕",
        "NL-L002":
            "2. 在 the PumpControl state 内部，有三个 main substates（主要子状态）："
            "PumpState、WaterState 和 MethaneState。",
        "NL-L003":
            "3. 系统首先迁移到 the PumpState substate，"
            "在该子状态中 the pump is activated or controlled（泵被激活或被控制）。"
            "〔原文如此：`activated or controlled` 用「或」并列两个动作，"
            "原文未说明二者何时各自发生〕"
            "〔译者存疑：`first`（首先）是指区域初始子状态，还是仅指叙述次序，原文未明说〕",
        "NL-L004":
            "4. 系统也可以迁移到 the WaterState substate，"
            "这表明 the pump is controlling or monitoring the water flow"
            "（泵正在控制或监测水流）。"
            "〔译者存疑：原文未说明这条迁移的源状态与触发条件〕",
        "NL-L005":
            "5. 类似地，系统可以迁移到 the MethaneState substate，"
            "这表明 the pump is controlling or monitoring the methane flow"
            "（泵正在控制或监测瓦斯流）。"
            "〔译者存疑：同上，原文未说明源状态与触发条件〕",
    },

    # ================================================== NL09 · 车辆运行控制
    # pairs 0003 0012 0022 0032 0042 0052
    "9fe426ba761d": {
        "NL-L001":
            "1. 一旦 the device is powered on（设备上电），系统进入 `Operate` 状态；"
            "并且，基于 user actions（用户动作），它在 `Idle`、`Accelerating or Cruising`、"
            "`Braking` 这些状态之间迁移。"
            "〔原文如此：`Accelerating or Cruising` 自身带一个 `or`，"
            "无法判定它是一个状态名还是两个状态的并列，译文保留该歧义不作拆分〕",
        "NL-L002":
            "2. 系统可以用 `start` 信号 turned on（开启），"
            "用 `keyOff` 信号 turned off（关闭）。"
            "〔译者存疑：`start` 与第 1 句的 `powered on` 是否为同一事件，原文未说明；"
            "`turned off` 之后进入哪个状态，原文也未给出〕",
        "NL-L003":
            "3. 在 `Operate` 状态内部，系统依据 accelerating、braking 或 stopping "
            "之类的 actions（动作）在不同的 substates 之间迁移。"
            "〔原文如此：`actions like ...` 是举例式列举，未给出完整的事件集合〕"
            "〔译者存疑：`stopping` 在第 1 句的状态清单里没有对应状态〕",
    },

    # ================================================== NL01 · 列车运行
    # pairs 0004 0014 0024 0034 0044 0054
    "3110cbcf15bf": {
        "NL-L001":
            "1. 系统起始于 the DoorsClosing state，并在 the doors are closed（车门关闭）时"
            "迁移到 InMotion，由 \"Closed/SendDeparted\" signal 触发。"
            "〔原文如此：`Closed/SendDeparted` 内含 `/`，该记法在 UML 中通常表示"
            "「触发/效应」，而原文整体称其为一个 signal（信号），译文保留原称法〕",
        "NL-L002":
            "2. 在 the InMotion state 中，系统或者在 it arrives（它到达）时迁移到 "
            "the Stopping state，由 \"Arrived/Stop, Send Arrived\" signal 指示；"
            "或者在 an obstacle is detected（检测到障碍物）时迁移到 "
            "the EmergencyStopping state。"
            "〔原文如此：`Arrived/Stop, Send Arrived` 内部同时含 `/` 与逗号，"
            "原文未说明它是一个信号名还是「触发 / 两个效应」的复合写法〕",
        "NL-L003":
            "3. 当检测到障碍物时，系统进入 the EmergencyStopping state，"
            "该状态 includes the actions（包含动作）\"Emergency Stop\" "
            "并 sends the \"Obstacle Detected\" signal（发出该信号）。"
            "〔译者存疑：`sends` 的主语是该状态还是系统，原文未明说；"
            "`actions` 用了复数而只列出一项〕",
        "NL-L004":
            "4. 在 the InMotion state 内部，系统运行于三个 substates："
            "Accelerating、Cruising 和 Approaching，"
            "它们表示列车运动的不同阶段。",
        "NL-L005":
            "5. 系统起始于 the Accelerating substate，一旦 cruising speed is reached"
            "（达到巡航速度）便移动到 the Cruising substate，"
            "由 \"Reached Cruising/Cruise\" signal 指示。",
        "NL-L006":
            "6. 若系统处于 the Accelerating substate 并 approaches its destination"
            "（接近其目的地），它在收到 \"Approached/Decelerate\" signal 时"
            "迁移到 the Approaching substate。"
            "〔译者存疑：`approaches its destination` 与收到该 signal 是两个并列条件，"
            "还是同一件事的两种说法，原文未明说〕",
        "NL-L007":
            "7. 处于 the Cruising substate 的系统，在 it approaches the destination"
            "（它接近目的地）时迁移到 the Approaching substate，"
            "由 \"Approached/Decelerate\" signal 触发。",
        "NL-L008":
            "8. 系统在 motion begins（运动开始）时进入 the Accelerating substate，"
            "以 \"Entry/Accelerate\" action 标记。"
            "〔原文如此：`Entry/Accelerate` 在 UML 记法中通常表示状态的 entry 动作，"
            "而原文把它称为 marked by 的一个 action，译文保留原称法〕"
            "〔译者存疑：`motion begins` 是一个事件还是对第 5 句起始子状态的复述，"
            "原文未明说〕",
        "NL-L009":
            "9. 在 the Approaching substate 中，系统 sends the \"Send\" signal（发出该信号）"
            "并继续接近目的地。"
            "〔译者存疑：signal 名逐字就叫 \"Send\"，原文未说明其内容与接收方；"
            "也未说明该发送是 entry 动作、do 活动还是迁移效应〕",
        "NL-L010":
            "10. 系统在 nearing the destination（接近目的地）期间 remains in（保持在）"
            "the Approaching substate，直到 it is ready to stop or decelerate"
            "（它准备好停车或减速）为止。"
            "〔译者存疑：`ready to stop or decelerate` 未给出可判定的条件，"
            "原文也未说明这句对应哪一条迁移〕",
    },

    # ================================================== NL10 · 微波炉
    # pairs 0005 0015 0025 0035 0045 0055
    "934e19bd4ae2": {
        "NL-L001":
            "1. the microwave（微波炉）起始于 the DoorShut state。从该状态出发，"
            "系统或者在 a Cancel action is performed（执行了一个 Cancel 动作）时 "
            "remain in（保持在）DoorShut，"
            "或者在 the door is opened（门被打开）时迁移到 the DoorOpen state。",
        "NL-L002":
            "2. 当 the Door Opened action（该动作）在 the DoorShut state 中发生时，"
            "系统迁移到 the DoorOpen state。"
            "The door can be closed（门可以被关闭）以返回 the DoorShut state。"
            "〔原文如此：`Door Opened` 中间带空格，与第 1 句的 `the door is opened` "
            "是否为同一事件，原文未说明；原文把它称为 action 而非 event〕",
        "NL-L003":
            "3. 在 the DoorOpen state 中，placing an item inside the microwave"
            "（把一个物品放入微波炉）使系统迁移到 DoorOpenWithItem。"
            "若 the item is removed（物品被取走），系统返回 DoorOpen。",
        "NL-L004":
            "4. 从 DoorOpenWithItem 出发，系统可以在 the door is closed with zero time set"
            "（门被关闭且设定时间为零）时迁移到 DoorShutWithItem，"
            "或在 cooking time is entered（输入了烹饪时间）时迁移到 ReadytoCook。"
            "〔译者存疑：`closed with zero time set` 是「关门」与「时间为零」两个条件的合取，"
            "还是对关门时刻状况的附带说明，原文未明说〕",
        "NL-L005":
            "5. 在 the DoorShutWithItem state 中，opening the door（打开门）"
            "使系统迁回 DoorOpenWithItem；而 entering cooking time（输入烹饪时间）"
            "把系统带到 ReadytoCook，在该状态中 the cooking time is displayed and updated"
            "（烹饪时间被显示并更新）。"
            "〔译者存疑：`displayed and updated` 是该状态的动作还是那条迁移的效应，"
            "原文未明说〕",
        "NL-L006":
            "6. 在 the ReadytoCook state 中，若执行了 the Cancel action，"
            "系统返回 DoorShutWithItem，canceling or updating the cooking time"
            "（取消或更新烹饪时间）。若 the door is opened（门被打开），"
            "系统迁移到 DoorOpenWithItem。"
            "〔原文如此：`canceling or updating` 用「或」并列两个效应，"
            "原文未说明何时取消、何时更新〕",
        "NL-L007":
            "7. 当 the Start action 在 ReadytoCook 中被执行时，"
            "系统迁移到 the Cooking state，在该状态中 the timer starts（计时器启动）。",
        "NL-L008":
            "8. 在 the Cooking state 中，opening the door（打开门）stops the timer"
            "（停止计时器）并使系统迁移到 DoorOpenWithItem；"
            "而若 the timer expires（计时器到期），系统移动到 DoorShutWithItem。"
            "一个 Cancel action 使系统迁回 ReadytoCook。",
    },

    # ================================================== NL03 · 无人机集群
    # pairs 0006 0016 0026 0036 0046 0056
    "a01c022f5380": {
        "NL-L001":
            "1 本状态机模型描述一个 UAV swarm（无人机集群）的状态迁移。",
        "NL-L002":
            "2 在 the mission is completed（任务完成）之前，UAV swarm 持续执行 "
            "target search tasks（目标搜索任务），在此期间它 operates within "
            "three different state areas（在三个不同的状态区域内运行）。"
            "〔译者存疑：`state areas` 既可读作 UML 的正交区（region），"
            "也可读作三个普通状态构成的集合，原文未明说，译文保留原词不作判定〕"
            "〔译者存疑：`the mission is completed` 的判定条件原文未给出〕",
        "NL-L003":
            "3 当 the UAV swarm is intercepted（无人机集群被拦截）时，"
            "它迁移到 the formation adjustment state（编队调整状态）。"
            "〔译者存疑：原文未说明该迁移的源状态；`formation adjustment state` "
            "是散文描述而非标识符，原文未给出状态名〕",
        "NL-L004":
            "4 During flight（在飞行期间），若 task assignment information is received"
            "（接收到任务分配信息），它进入 the attack state（攻击状态）。"
            "在 completing the attack（完成攻击）之后，the number of UAVs in the swarm "
            "decreases accordingly（集群中的无人机数量随之减少）。"
            "〔译者存疑：`During flight` 没有对应任何已命名状态；"
            "`decreases accordingly` 未给出减少量，也未说明它是效应还是外部事实〕",
    },

    # ================================================== NL07 · 避撞子机
    # pairs 0007 0017 0027 0037 0047 0057
    "49854d044ad9": {
        "NL-L001":
            "1. 本图中 There are three region（有三个区）"
            "〔原文如此：`three region` 数与名不一致，应为 `regions`；原句句末无句号〕"
            "〔译者存疑：`region` 指 UML 正交区还是泛指图上的三块，原文未明说〕",
        "NL-L002":
            "2. 当检测到 a possible frontend collision（一次可能的前向碰撞）、"
            "rear-end collision（追尾碰撞）或 collision with pedestrian（与行人碰撞）时，"
            "This sub-machine（本子机）becomes active（变为活跃）。"
            "〔原文如此：`frontend` 通常写作 `front-end`〕"
            "〔译者存疑：`This sub-machine` 指代哪一个子机，原文未明说〕",
        "NL-L003":
            "3. collision avoidance（避撞）的 the active mode（活跃模式）的 "
            "orthogonal regions（正交区）allow for concurrent activation（允许并发激活）"
            "different of collision avoidance controls（不同的避撞控制）"
            "〔原文如此：`concurrent activation different of collision avoidance controls` "
            "语序错乱，通顺写法应为 `concurrent activation of different collision "
            "avoidance controls`，译文照原语序直译；原句句末无句号〕",
    },

    # ================================================== NL05 · 自动驾驶 + 避撞
    # pairs 0009 0019 0029 0039 0049 0059
    "b7425c44960b": {
        "NL-L001":
            "1. 系统起始于 the AutonomousMode state，该状态 transitions into "
            "the InitialState substate（迁移进入该子状态），"
            "标志着 the autonomous driving mode（自动驾驶模式）的起点。",
        "NL-L002":
            "2. 从 the InitialState 出发，系统可以基于条件迁移到 HighwayMode 或 UrbanMode "
            "之一：`high_way=true` 对应 HighwayMode，`urban_way=true` 对应 UrbanMode。",
        "NL-L003":
            "3. 在 the HighwayMode state 中，系统起始于 the enter_hwy substate，"
            "并可以基于 the distance to the front vehicle（与前车的距离，`dist_to_front<25`）"
            "与 the availability of an extra lane（额外车道的可用性，`extra_lane=true`）"
            "迁移到 cruise 或 lane_change。"
            "〔译者存疑：原文未说明两个条件分别对应哪一个目标子状态，"
            "也未说明二者之间是「且」还是「或」〕",
        "NL-L004":
            "4. 若系统处于 lane_change，它可以在 the lane change is completed（变道完成）"
            "之后返回 cruise，或者在与出口的距离小于 2 公里（`dist_to_exit<2`）时 "
            "exit the highway（驶离高速）。"
            "〔译者存疑：`exit the highway` 是一个动作描述还是一个状态名，原文未明说〕",
        "NL-L005":
            "5. 在 the cruise substate 中，若与前车的距离变为小于 25 米"
            "（`dist_to_front<25`）且有一条额外车道可用，系统迁移到 lane_change。"
            "若与出口的距离小于 2 公里（`dist_to_exit<2`），"
            "系统也可以 exit the highway（驶离高速）。"
            "〔原文如此：第 3 句给出 `dist_to_front<25` 时未附单位，此处附的是「米」〕",
        "NL-L006":
            "6. the HighwayMode 在系统迁移到 FinishState 时结束，"
            "由 `auto_finished=true` 条件触发。",
        "NL-L007":
            "7. 在 UrbanMode 中，系统起始于 the enter_urban substate。从这里出发，"
            "若与前车的距离小于 15 米（`dist_to_front<15`）且有一条额外车道可用，"
            "它可以迁移到 lane_change_urban；若 the road ahead is clear（前方道路畅通），"
            "迁移到 straight；若它检测到一个 intersection（`intersection=true`），"
            "迁移到 intersection。"
            "〔译者存疑：`the road ahead is clear` 原文未给出对应的形式化条件〕",
        "NL-L008":
            "8. 在 the lane_change_urban substate 中，若 the lane change is complete"
            "（变道完成），系统迁移到 straight；若与 the urban exit（城区出口）的距离"
            "小于 0.7 公里（`dist_to_exit<0.7`），迁移到 exit_urban。",
        "NL-L009":
            "9. 在 the straight substate 中，若系统检测到一个 intersection，"
            "它迁移到 the intersection substate。若与前车的距离变为小于 15 米"
            "（`dist_to_front<15`）且有一条额外车道可用，它迁移到 lane_change_urban。",
        "NL-L010":
            "10. 一旦 `auto_finished=true` 被满足，"
            "系统通过迁移到 FinishState 而退出 the UrbanMode state。",
        "NL-L011":
            "11. 系统支持 HighwayMode 与 UrbanMode 之间的 dynamic transitions（动态迁移），"
            "respectively（分别）基于 `urban_way=true` 与 `high_way=true` 条件，"
            "以促成行驶过程中的 seamless mode shifts（无缝模式切换）。"
            "〔译者存疑：`respectively` 的配对关系原文未写明 —— 究竟是"
            "「HighwayMode 到 UrbanMode 用 urban_way=true」还是相反，两读都成立〕",
        "NL-L012":
            "12. the collision avoidance system（避撞系统）最初处于 "
            "the collision_avoidance_deactive state。当 certain conditions are met"
            "（某些条件被满足）时，它迁移到 collision_avoidance_active，"
            "such as（例如）检测到行人（`pedestrian_detected`）、"
            "后方距离小于 5 米且速度超过 30 km/h（`dist_to_rear<5 & vel>30`）、"
            "或在 highway mode 下前方距离小于 15 米、在 urban mode 下小于 10 米。"
            "〔原文如此：`deactive` 非标准英文词，通顺写法为 `deactivated` 或 `inactive`，"
            "但它同时是状态标识符，译文保留原拼写〕"
            "〔译者存疑：`such as`（例如）表明这份条件列举并不完整；"
            "最后一项原文未给出形式化条件表达式〕",
        "NL-L013":
            "13. 一旦处于 the collision_avoidance_active state，"
            "当 there is no active danger（不存在活跃危险）时，"
            "避撞系统返回 the collision_avoidance_deactive state，"
            "该情形由条件 `front_inactive`、`rear_inactive` 和 `pedestrian_inactive` 指示。"
            "〔译者存疑：三个条件之间是「且」还是「或」，原文用逗号加 `and` 并列，未明说〕",
    },
}


def digest(pair):
    """该 pair 的 NL 全文 sha256 前 12 位 —— 与 `overrides.json` 的键同口径。"""
    return hashlib.sha256(S.nl_text(pair).encode("utf-8")).hexdigest()[:12]


def translate(pair, seg_id):
    """取译文。⛔ 查不到返回 `None`，⛔ 不返回占位符 —— 缺译必须显形。"""
    return TRANSLATIONS.get(digest(pair), {}).get(seg_id)


def missing(pairs=None):
    """列出缺译文的 `(pair, seg_id)`。⭐ 供测试与 `generate.py --check` 使用。"""
    out = []
    for pair in (pairs if pairs is not None else S.IN_SCOPE_PAIRS):
        segs, _ = S.nl_segments(pair)
        for sid, _txt in segs:
            if not translate(pair, sid):
                out.append((pair, sid))
    return out
