# Smart Car Parking System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `RFID` 认证、入口开闸、车位占用更新和出场计费这四段链路都写在同一个 IoT 停车系统里，是停车方向比较完整的双 A `EFSM + T0` 样本。

## 条目 1: RFID-Authenticated Entry and Slot-Occupancy Parking Controller

- 控制对象：智慧停车与车位管理领域的 RFID 门禁、车位占用同步与出场计费控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个结合 `NodeMCU`、`RFID`、`IR` 传感器、移动应用和 `Firebase` 的停车场控制器，用于组织车辆进场认证、闸门放行、空位状态更新和出场计费。
- 判断：算。对象是实际停车控制系统，原文明确给出了进场触发、身份校验、开闸放行、车位占用写回和出场收费规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`3.1 Theoretical framework`，`paper_content.txt` 第 170-204 行
> Every user availing the services provided by this proposed system will be required to register with the agency, will have to take an RFID Tag analogous to the FASTag currently in use. Each RFID Tag will have a unique ID that the users should use to log into their account on the Smart Car Parking system application on their mobile.
>
> The RFID Tag affixed to the vehicle's windshield is scanned by the RFID EM-18 reader module installed near the parking premises as soon as the car approaches the proximity of the entry gate. The parking setup includes an IR sensor that detects the presence of the car at the entry gate, furthermore, it prompts the RFID EM-18 reader ... Following this, the servo motor drives the gate to open, permitting the vehicle within the parking area. the time of entry is noted in the real-time database.
>
> The parking slot setup includes an IR sensor which is used to detect the occupancy of that particular slot. This data is sent to the real-time database, which updates the mobile application accordingly. While checking out from the parking area the same procedure is followed, the time of exit is noted and the parking fare is calculated based on the hours of usage.

#### 摘录 B

- 出处：第 3 页，`3.2 Implementation`，`paper_content.txt` 第 206-239 行
> When a car is detected by the IR sensor and the RFID card being read is valid, a servo motor opens the entrance gate, allowing the car to occupy the vacant slot.
>
> Only the RFID tag will allow the user to access this application.
>
> The app redirects the user to a page where one can check the slot availability while parking.
>
> The slot in the mobile app is represented with green color indicating vacancy, and stored as “0” in the real-time database. It turns red when the slot is occupied and subsequently updates the real-time database as “1”. When the respective car vacates the parking slot, it is simultaneously updated as "0" in the real-time database to indicate that the parking spot is free.
>
> If the user exits the parking premises before the expiry of a designated time period set by the organization employing this facility; they’ll be charged a fixed base price for the same. Additional charges are assessed on an hourly basis when the user exceeds the allotted time.

### 2. 基于原文整理后的自然语言描述

The parking controller begins with an identity-gated entry branch: when the entry-side IR sensor detects a car, the system prompts the `RFID EM-18` reader, validates the windshield tag, and opens the entrance gate with a servo only if the credential is accepted. Once the vehicle is admitted, the controller records the entry time in the real-time database and lets the driver use the authenticated mobile application to locate a vacant slot. Each parking slot is then supervised by its own IR occupancy sensor, and the backend keeps the slot state synchronized as `0` for vacant and `1` for occupied while the mobile app mirrors that state as green or red. During exit, the system records the leaving time, computes the parking fee from the duration of use, and applies either a fixed base price or additional hourly charges when the allowed duration is exceeded. This makes the sample more than a simple barrier gate: it is an EFSM whose guards and outputs span authentication, gate actuation, occupancy-state updates, and fee-calculation branches.

### 3. 逐句溯源

1. 句子 1：The parking controller begins with an identity-gated entry branch: when the entry-side IR sensor detects a car, the system prompts the `RFID EM-18` reader, validates the windshield tag, and opens the entrance gate with a servo only if the credential is accepted.
   对应摘录：A, B
2. 句子 2：Once the vehicle is admitted, the controller records the entry time in the real-time database and lets the driver use the authenticated mobile application to locate a vacant slot.
   对应摘录：A, B
3. 句子 3：Each parking slot is then supervised by its own IR occupancy sensor, and the backend keeps the slot state synchronized as `0` for vacant and `1` for occupied while the mobile app mirrors that state as green or red.
   对应摘录：A, B
4. 句子 4：During exit, the system records the leaving time, computes the parking fee from the duration of use, and applies either a fixed base price or additional hourly charges when the allowed duration is exceeded.
   对应摘录：A, B
5. 句子 5：This makes the sample more than a simple barrier gate: it is an EFSM whose guards and outputs span authentication, gate actuation, occupancy-state updates, and fee-calculation branches.
   对应摘录：A, B
