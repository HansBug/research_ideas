# Formal specifications and analysis of the CARA Infusion Pump Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：OCR 后可以把泵控制模式和 cuff auto control 要求链完整还原出来。

## 备注
- 本文件基于 OCR 刷新后的 `paper_content.txt` 二次梳理。引文保持与 OCR 文本一致，因此会保留少量识别噪声。

## 条目 1: Pump manual/autocontrol modes
- 控制对象：CARA 输液泵控制系统中的泵控制方式

### 0. 条目识别与判定

- 一句话说明：这是医疗复苏输液领域的 CARA 输液泵控制系统，用于在人工设定和自动血压闭环控制之间协调泵速控制。
- 判断：算。它直接作用于患者输液过程，包含运行方式切换、故障触发后的控制权释放和人工接管逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Pump / Caregiver / Patient 描述，行 233-269
> --- Page 5 ---
> shows the the driving voltage (and hence the flow rate) as determined by the
> algorithm. Whenever a pump fault occurs (e.g., occlusion in the fluid tubing),
> appropriate alarm signals are activated. The caregiver is responsible for remov-
> ing the pump’s faults, and if they happen when the pump is being controlled by
> CARA, the software releases its control. We have tried to abstract the interface
> so that it can specify what a replacement pump would have to satisfy in order
> to be used instead of the M100.
> 
> Blood Pressure Sensor. The Blood Pressure Sensor is the monitoring device
> which is the source of physiological signals such as arterial blood pressure and
> cuff blood pressure. It will be attached to the patient and communicate the
> signals to CARA. However, the design does not allow for direct interface with the
> algorithm. Instead, all data from the sensor is assumed to be stored in a shared
> buffer that the software will have access to. This allows for a more modular
> design which could enable greater flexibility in using a variety of monitoring
> devices.
> 
> Pump. The infusion pump is the device which moves fluid into the patient.
> It has a variety of sensors and can trigger alarms if fault conditions occur.
> The pump has two modes, manual and autocontrol. In manual mode, the
> pump speed is set with a switch built into the pump. In autocontrol mode, the
> pumping speed is set by a control voltage from an external source.
> 
> Caregiver. The caregiver represents the person that will be in charge of the
> infusion, usually a doctor, nurse, or medic. He or she can interact with the
> actual pumping device via hardware buttons on the pump and with the CARA
> software via messages and soft buttons on a display screen. He or she sets
> the desired blood pressure via soft buttons on the display, and sets a default
> flow rate directly on the pump for use by the pump when it is operating in
> manual mode (not under the control of CARA). The caregiver also takes care
> of potential faults and failures that may occur during infusion.
> 
> Patient. The patient is the object in this system. He or she is connected to the
> pump and the blood pressure sensor. Infusion is carried out depending on the
> patient’s current state, with the aim to rapidly restore his or her intravenous
> volume and blood pressure.

### 2. 基于原文整理后的自然语言描述

The infusion pump can be run locally or under CARA, with the local switch setting the flow in manual operation and an external control voltage setting the pumping speed in autocontrol. If a pump fault occurs while CARA is controlling the pump, alarm signals are activated, the caregiver removes the fault, and the software releases control. The caregiver also sets the desired blood pressure through the display and a default flow rate on the pump for use when the pump stays in manual mode.

### 3. 逐句溯源

1. 句子 1：The infusion pump can be run locally or under CARA, with the local switch setting the flow in manual operation and an external control voltage setting the pumping speed in autocontrol.
   对应摘录：A
2. 句子 2：If a pump fault occurs while CARA is controlling the pump, alarm signals are activated, the caregiver removes the fault, and the software releases control.
   对应摘录：A
3. 句子 3：The caregiver also sets the desired blood pressure through the display and a default flow rate on the pump for use when the pump stays in manual mode.
   对应摘录：A

## 条目 2: Cuff Handler in Auto Control
- 控制对象：CARA 中基于 cuff 血压源的自动控制要求

### 0. 条目识别与判定

- 一句话说明：这是医疗复苏控制领域中利用袖带血压驱动的自动控制子系统，用于根据有效血压读数调整测量频率并在失效时退回人工控制。
- 判断：算。它描述的是实际闭环控制中的输入源管理与降级控制逻辑，条件驱动的行为切换非常明确。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Cuff Handler EFSM OCR 结果，行 787-842
> CB_localTimer >= 60
> AND CB _cuffSource == "Cuff"                                                                       -
> 
> 一> CB_iterations ++;       ~                                                         SS
> CB localfimer= 60 f      atte == "Catt" >
> \Frtanate Cutt] B-erations = 0; CB. ocalTimer = 0
> CB iterations >= 5 AND                                                  \
> curl Ty,     Cult"                                         CB_ctrIType !=\"Cutt”
> 2            CB_ctrlValue < 60 AND CB_ctrValue >= 40
> 
> cuffFrequency = 60; CB_loc
> 
>   
> 
> In Auto Control [==
> 
>  
> 
>  
> 
>  
> 
>  
> 
>  
> 
>                                                                                                                                                    
> 
>  
> 
> In                           7                                                                               \
> Be                   CB_ctrlValue < 70 AND CB_etrlVal                                   cut                        \
> => CB_cuffFrequency = 120; CB_localTimer = 0            Frequency             \
> 
> CB_etrlValue < 90 AND CB_etrlValue >= 70                                                        \
> => CB_cufiFrequency = 300; CB_localTimer = 0
> 
> CB_ctrlValue <= 150 AND CB_ctrlValue >= 90                     |
> = CB_cuffFrequency = 600; CB_localTimer = 0
> 
>   
> 
>  
> 
>  
> 
>  
>  
> 
>  
> 
> / CB localTimer >=
> (CB_cuffValue <= 150 AND CB_cuff$Value >= 40 —>                              /- CB alarm_cufflnv:
> (CB_alarm_cufflnvalid! = false                                 CB_backManual = true
> 
> Cuff Invalid 1

#### 摘录 B
- 出处：第 12 页，Figure 6 “Requirements for the Cuff Handler in Auto Control”，行 888-919
> --- Page 12 ---
> 13. The CARA should be able to use a blood pressure from various sources as the input into
> the CARA algorithm. Blood pressure sources (artial line, cuff, other noninvasive
> pressures [pulse wave, etc.]) will be prioritized based on quality.
> 13.1 A corroborated A-line is use priority 1
> 13.2 A corroborated pulse-wave pressure is use priority 2
> 13.3 A cuff pressure is use priority 3
> 15. During resuscitation CARA should respond to any lost blood pressure sources
> 15.1 With an appropriate message
> 15.2 With a level 1 alarm
> 15.3 With a notation in the resuscitation file
> 18 Mean pressure readings from Propaq must be within 40 - 150 mmHg to be valid throughout resuscitation
> 27. When the cuff pressure is being used for control, CARA should set a cuff reading frequency based on a ta
> In general, blood pressures will be taken more frequently while below the set point.
> If the cuff is already inflating for some other reason when the time arives for another reading,
> an additional cuff reading does not need to be requested.
> 27.1 If the mean BP is 60 or below, cuff pressures will be taken once per minute.
> 27.2 If the mean BP is (60 - 70], cuff pressures will be taken once every 2 minutes.
> 27.3 If the mean BP is (70 - 90], cuff pressures will be taken once every 5 minutes.
> 27.4 If the mean BP is above 90, cuff pressures will be taken once every 10 minutes.
> 28 If CARA can not obtain a valid blood pressure in 3 minutes, it should revert back to manual mode.
> 28.1 An appropriate message should be displayed.
> 28.2 A level 2 alarm should be issued.
> 44 If only the cuff pressure is being used and an expected blood pressure reading is invalid
> 44.1 An appropriate message should be displayed
> 44.2 A level-1 alarm should sound
> 44.3 CARA should then initiate another request for a cuff pressure
> 44.3.1 If this pressure is invalid,
> 44.3.1.1 An appropriate message should be displayed
> 44.3.1.2 A level-2 alarm should sound
> 44.3.1.3 The system will revert to manual mode
> 44.4 Notations should be made to the resuscitation file

#### 摘录 C
- 出处：第 13 页，Figure 7 变量表，行 930-942
> Variable Name           Description                                    Written By
> CA_Mode                CARA’s current mode                        Algorithm
> CB-alarm_cuffInvalid1 Level 1 Alarm                               Cuff Handler
> CB-alarm_cuffInvalid2 Level 2 Alarm                                Cuff Handler
> CB_backManual          Go back to manual mode                       Cuff Handler
> CB-ctrlType             Type of Control BP                          Corroboration
> CB_ctrlValue            Value of Control BP                          Corroboration
> CB-_cuffFrequency       Frequency to read Control BP (seconds)      Cuff Handler
> CB_cuffSource           Source of Cuff BP Reading?                  Corroboration
> CB_cuffValue           Value of Cuff BP Reading                   Corroboration
> CB_driven Voltage        Voltage to drive pump                         Algorithm
> CB_iterations            Number of iterations                          Cuff Handler
> CB_localTimer           Local Timer                                     Cuff Handler

### 2. 基于原文整理后的自然语言描述

When cuff pressure is being used for control, CARA uses it as one of the prioritized blood pressure sources and adjusts the cuff reading frequency so that lower pressures are checked more often. Specifically, cuff readings are taken once per minute at 60 or below, every 2 minutes for (60, 70], every 5 minutes for (70, 90], and every 10 minutes above 90. If CARA cannot obtain a valid blood pressure in 3 minutes, or if repeated cuff readings remain invalid while cuff pressure is being used for control, it issues the prescribed messages and alarms and reverts to manual mode.

### 3. 逐句溯源

1. 句子 1：When cuff pressure is being used for control, CARA uses it as one of the prioritized blood pressure sources and adjusts the cuff reading frequency so that lower pressures are checked more often.
   对应摘录：A, B
2. 句子 2：Specifically, cuff readings are taken once per minute at 60 or below, every 2 minutes for (60, 70], every 5 minutes for (70, 90], and every 10 minutes above 90.
   对应摘录：A, B
3. 句子 3：If CARA cannot obtain a valid blood pressure in 3 minutes, or if repeated cuff readings remain invalid while cuff pressure is being used for control, it issues the prescribed messages and alarms and reverts to manual mode.
   对应摘录：A, B, C
