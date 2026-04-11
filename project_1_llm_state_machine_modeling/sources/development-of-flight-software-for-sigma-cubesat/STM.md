# Development of Flight Software for SIGMA CubeSat - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 SIGMA CubeSat 的七模任务软件、时间触发自动科学模式和电源约束写得比较完整，可直接作为 CubeSat 模式管理与任务监督样本。

## 条目 1: SIGMA Seven-Mode Mission Supervisor
- 控制对象：SIGMA CubeSat 的七模任务软件与任务监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 CubeSat 机载软件领域的顶层任务监督器，用于在 `INIT / STABLE / NORMAL / SCIENCE / SCIENCE AUTO / ACS / RECOVERY` 七个运行模式之间切换，并协调天线展开、信标发送、姿态控制与科学载荷执行。
- 判断：算。对象是实际 SIGMA CubeSat 的飞行软件主控制链，原文明确给出了模式集合、时间触发条件、电压 guard、载荷互斥约束和 task/state manager 执行方式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`Table 1. Requirements of SIGMA CubeSat`
> 위성상태정보는 10초마다 수집
>
> TEPC는 배터리 전압이 7V이상에서 실행
>
> MAG와 TEPC는 동시 실행 불가

#### 摘录 B
- 出处：第 3-4 页，`Table 2. List of operation mode / 위성운용시나리오`
> 1 INIT 시스템을 초기화하고 안테나 전개
>
> 2 STABLE 비콘 송신하며 지상국 명령 대기
>
> 3 NORMAL 최근 위성상태정보를 송신하며 지상국 명령 대기
>
> 4 SCIENCE 탑재체 MAG와 TEPC 실행
>
> 5 SCIENCE AUTO 일정시간 동안 지상국 명령을 수신하지 못했을 경우 자동으로 탑재체 실행
>
> 6 ACS 위성자세제어
>
> 7 RECOVERY 시스템 오류 발생시 복구 및 재초기화

#### 摘录 C
- 出处：第 4 页，`위성운용시나리오`
> STABLE모드는 Fig.6과 같이 2주 동안 지상으로 비콘(beacon)을 송신하면서 지상국 명령을 수행한다. 그리고 2주 후에는 자동으로 NORMAL모드가 실행되는데 ... 이 때 만약 3일 동안 지상국으로부터 아무런 명령을 수신하지 못하면 자동으로 SCIENCEAUTO모드를 실행하여 과학 데이터를 수집하고 지상으로 전송하며 데이터 전송이 다 끝나면 자동으로 다시 NORMAL모드로 전환된다.

#### 摘录 D
- 出处：第 5-6 页，`The structure of OPERATION app`
> OPERATION응용 프로그램은 위성 운용 시나리오에 따라 나누어진 7개 모드를 각각의 태스크로 구분하여 태스크 매니저(task manager)가 필요에 따라 적절한 태스크를 선택하여 실행할 수 있도록 하였다.
>
> 각 태스크 내에서는 상태 매니저(state manager)가 무한 반복되면서 태스크의 상태 값을 검사하여 각 상태에 따라 지상국 명령을 실행하거나 자동화된 명령들을 수행하게 된다.

### 2. 基于原文整理后的自然语言描述

The SIGMA flight software is organized as a seven-mode mission supervisor with `INIT`, `STABLE`, `NORMAL`, `SCIENCE`, `SCIENCE AUTO`, `ACS`, and `RECOVERY`, and these modes are implemented as separate tasks selected by a task manager. The supervisor starts in `INIT` to initialize the system and deploy the antenna, then enters `STABLE` to beacon and wait for ground commands during the first two weeks, and automatically transitions to `NORMAL` afterwards. In `NORMAL`, the controller keeps sending recent housekeeping data and monitors command silence, so if no command is received for three days it automatically launches `SCIENCE AUTO`, performs scientific data collection and downlink, and returns to `NORMAL` when transmission finishes. The mission logic is further guarded by operational constraints: housekeeping data are collected every ten seconds, the `TEPC` payload may run only when battery voltage is above `7 V`, and `MAG` and `TEPC` are not allowed to operate simultaneously. Inside each mode, a state manager repeatedly checks current state values to execute ground-commanded or automated actions, so the whole controller combines timed phase progression, voltage-based enabling, payload mutual exclusion, and failure recovery in one centralized flight-software backbone.

### 3. 逐句溯源

1. 句子 1：The SIGMA flight software is organized as a seven-mode mission supervisor with `INIT`, `STABLE`, `NORMAL`, `SCIENCE`, `SCIENCE AUTO`, `ACS`, and `RECOVERY`, and these modes are implemented as separate tasks selected by a task manager.
   对应摘录：B, D
2. 句子 2：The supervisor starts in `INIT` to initialize the system and deploy the antenna, then enters `STABLE` to beacon and wait for ground commands during the first two weeks, and automatically transitions to `NORMAL` afterwards.
   对应摘录：B, C
3. 句子 3：In `NORMAL`, the controller keeps sending recent housekeeping data and monitors command silence, so if no command is received for three days it automatically launches `SCIENCE AUTO`, performs scientific data collection and downlink, and returns to `NORMAL` when transmission finishes.
   对应摘录：B, C
4. 句子 4：The mission logic is further guarded by operational constraints: housekeeping data are collected every ten seconds, the `TEPC` payload may run only when battery voltage is above `7 V`, and `MAG` and `TEPC` are not allowed to operate simultaneously.
   对应摘录：A
5. 句子 5：Inside each mode, a state manager repeatedly checks current state values to execute ground-commanded or automated actions, so the whole controller combines timed phase progression, voltage-based enabling, payload mutual exclusion, and failure recovery in one centralized flight-software backbone.
   对应摘录：B, D
