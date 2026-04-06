# Fuzzy logic-PLC-based controller for water treatment simulator system - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把酸/碱储液、过程槽、`1` 分钟混合、再次测量、正常后排出，以及五档 pH 模糊规则和泵响应时长都写成了可追溯控制链，是 `🌡️` 方向少见的双 A 连续耦合样本。

## 条目 1: Fuzzy pH-neutralization batch controller

- 控制对象：过程与环境控制领域的模糊逻辑 PLC 水处理 pH 中和批处理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `Outseal PLC` 的水处理 pH 中和控制器，利用模糊规则控制酸液泵、碱液泵、混合电机、输出泵和电磁阀完成批处理循环。
- 判断：算。对象是实际水处理控制器，原文既给出顺序工艺链，也给出 `very small / small / normal / big / very large` 五档 pH 规则与 `0 / 60 / 70 / 120 / 150` 的泵时长映射，控制链和时间语义都很充分。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`2 Materials and Methods`，`paper_content.txt` 第 113-129 行
> The prototype initiates the process by pumping the input from the acid and base reservoirs into the process tank, followed by the DC motor carrying out the blending process. If the pH value is less than 6, the base solution pump adds the base solution ... If the detected pH value exceeds 7, the acid solution pump injects the acid solution ... After adding the acid or base solution to the tank, we blend it for 1 minute, and then the pH sensor measures the pH concentration in the tank again. If the pH value falls between 6-7 ... the output pump and solenoid valve ... will turn on and flow water into the reservoir/output tank until the process tank is empty.

#### 摘录 B

- 出处：第 3 页，`2. Design rule base`，`paper_content.txt` 第 255-262 行
> The design of the fuzzy logic controller rule base is:
> a. If (pH is very small) Then (pH UP is long) (pH DOWN is still)
> b. If (pH is small) Then (pH UP is medium) (pH Down is still)
> c. If (pH is normal) Then (pH UP is still) (pH DOWN is still)
> d. If (pH is large) Then (pH UP is still) (pH DOWN is medium)
> e. If (pH is very large) Then (pH UP is still) (pH DOWN is long)

#### 摘录 C

- 出处：第 3-4 页，`3. System inference`，`paper_content.txt` 第 272-304 行
> [R1]: If (pH is very small) Then (pH UP = 120) (pH DOWN = 0)
>
> [R2]: If (pH is Small) Then (pH UP = 60) (pH DOWN = 0)
>
> [R3]: If (pH is normal) Then (pH UP = 0) (pH DOWN = 0)
>
> [R4]: If (pH is big) Then (pH UP = 0) (pH DOWN = 70)
>
> [R5]: If (pH is very large) Then (pH UP = 0) (pH DOWN = 150)

#### 摘录 D

- 出处：第 5 页，`3.2 Simulation Results`，`paper_content.txt` 第 410-418 行
> Testing the control system on a prototype that has been made with a batch control type where the control process is carried out sequentially ... If the pH value of the water is less or more than neutral, then the pH UP and pH DOWN solution pumps will flow the solution in the process tank to re-neutralize the pH of the water.

### 2. 基于原文整理后的自然语言描述

The water-treatment simulator runs a sequential batch controller over acid and base reservoirs, a process tank, a pH sensor, a mixing motor, and an output pump plus solenoid valve. After the input water and correction solutions enter the process tank, the controller checks the measured pH: if `pH < 6`, the base pump adds alkaline solution; if `pH > 7`, the acid pump injects acidic solution. After either correction action, the system blends for `1` minute and then measures the pH again. Once the measured value returns to the normal `6-7` range, the controller turns on the output pump and solenoid valve so the tank drains into the output reservoir until empty, after which the batch process continues with the next input. The correction duration is not fixed by a single threshold but by a five-level fuzzy rule base that maps `very small / small / normal / big / very large` pH conditions to concrete `pH UP` and `pH DOWN` pump durations such as `120`, `60`, `70`, and `150`.

### 3. 逐句溯源

1. 句子 1：The water-treatment simulator runs a sequential batch controller over acid and base reservoirs, a process tank, a pH sensor, a mixing motor, and an output pump plus solenoid valve.
   对应摘录：A, D
2. 句子 2：After the input water and correction solutions enter the process tank, the controller checks the measured pH: if `pH < 6`, the base pump adds alkaline solution; if `pH > 7`, the acid pump injects acidic solution.
   对应摘录：A
3. 句子 3：After either correction action, the system blends for `1` minute and then measures the pH again.
   对应摘录：A
4. 句子 4：Once the measured value returns to the normal `6-7` range, the controller turns on the output pump and solenoid valve so the tank drains into the output reservoir until empty, after which the batch process continues with the next input.
   对应摘录：A, D
5. 句子 5：The correction duration is not fixed by a single threshold but by a five-level fuzzy rule base that maps `very small / small / normal / big / very large` pH conditions to concrete `pH UP` and `pH DOWN` pump durations such as `120`, `60`, `70`, and `150`.
   对应摘录：B, C
