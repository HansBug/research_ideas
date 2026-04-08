# Implementation of Automated Double Doors with Programmable Logic - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双开车库门的开门来源、自动关门、夹人保护、故障回退和 `40` 秒照明延时都写进了 PLC 梯形图步骤，足以形成稳定的双 A 自动门样本。

## 条目 1: RFID-and-photoelectric double-door controller

- 控制对象：基于 PLC 的车库双开自动门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的双门自动门控制器，用 `RF-ID` 或遥控开门请求、光电传感器自动关门、障碍回退和故障复位共同管理门机与照明。
- 判断：算。对象是实际门控系统，原文明确给出开门触发、照明延时、自动关门、夹障保护、故障状态和输出控制段。

### 1. 原文摘录

#### 摘录 A

- 出处：第 13 页，`4.2.1 Ohjelman kuvaus`，`paper_content.txt` 第 352-363 行
> Ovien avaus tapahtuu kahden eri vaihtoehdon perusteella, joko auto tunnistetaan RF-ID – tunnisteensa ansiosta tai sitten käyttäjä ohjaa ovikoneistoa kaukosäätimen avulla.
>
> Ovet avautuvat tunnisteen tullessa ja ollessa oikea.
>
> Valot palavat 40 sekuntia sen jälkeen kun liikkeentunnistimelta on tullut viimeisen kerran tieto liikkeestä.
>
> Optinen anturi mittaa ajoneuvon peräpään saapumisen autotalliin ja sulkee ovet kun säde ensimmäisen kerran on jälleen katkeamaton.

#### 摘录 B

- 出处：第 18-20 页，`Ohjelma-osio`，`paper_content.txt` 第 436-461 行
> Kolmas askel on oven sulkemista varten. Samassa askeleessa tehdään valokennon nousevan reunan tarkastelu automaattista sulkemista varten.
>
> Neljännessä askeleessa laitteisto tarkastelee valokennon avulla mahdollisesti ovien väliin kesken sulkemisen tulevaa estettä.
>
> Askeleessa viisi suoritetaan mahdollisesta virhetilasta johtuen moottoreiden sammutus, jolloin ovet ovat ohjattavissa käsin.
>
> Virhetila kuitataan painonapilla. Myös virhetilassa valaistus pysyy päällä.

#### 摘录 C

- 出处：第 23 页，`Output_Ohjaus-osio`，`paper_content.txt` 第 509-514 行
> Osio kolme on ovimoottoreiden kontrollerin ohjausta varten.
>
> Kontrolleri tietää onko ovet auki vai kiinni ja ohjausta varten tarvitaan vain signaalin nouseva reuna avaamista ja sulkemista varten.

### 2. 基于原文整理后的自然语言描述

The automated double-door controller opens the garage doors either when a valid `RF-ID` tag is recognized or when the user issues a remote-control request. Once the opening branch is taken, the PLC also energizes the interior lighting and keeps the lights on for `40` seconds after the last motion-detection event. A photoelectric sensor supervises the vehicle tail position so that the restored beam can trigger the automatic closing step when the vehicle has passed the doorway. If the beam is broken again during closing, the controller interprets that as a possible obstruction, cuts motor power and control, and moves the system into a fault-handling branch where the doors must be operated manually until the reset button is pressed. The output section then sends only rising-edge open and close commands to the door controller, because the motor controller itself already tracks whether the doors are open or closed.

### 3. 逐句溯源

1. 句子 1：The automated double-door controller opens the garage doors either when a valid `RF-ID` tag is recognized or when the user issues a remote-control request.
   对应摘录：A
2. 句子 2：Once the opening branch is taken, the PLC also energizes the interior lighting and keeps the lights on for `40` seconds after the last motion-detection event.
   对应摘录：A
3. 句子 3：A photoelectric sensor supervises the vehicle tail position so that the restored beam can trigger the automatic closing step when the vehicle has passed the doorway.
   对应摘录：A, B
4. 句子 4：If the beam is broken again during closing, the controller interprets that as a possible obstruction, cuts motor power and control, and moves the system into a fault-handling branch where the doors must be operated manually until the reset button is pressed.
   对应摘录：B
5. 句子 5：The output section then sends only rising-edge open and close commands to the door controller, because the motor controller itself already tracks whether the doors are open or closed.
   对应摘录：C
