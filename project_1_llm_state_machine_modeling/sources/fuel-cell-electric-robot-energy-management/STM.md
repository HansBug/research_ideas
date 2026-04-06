# Energy Management of a Fuel Cell Electric Robot Based on Hydrogen Value and Battery Overcharge Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把燃料电池机器人 EMS 写成“机动状态识别 + 电池区间分类 + 燃料电池六模式选择 + BOCC”链路，虽然偏能量管理，但状态、区间、模式选择条件和结果统计都足够明确，可形成双 A 正例。

## 条目 1: Five-state maneuver-aware fuel-cell/battery EMS

- 控制对象：燃料电池电动机器人的燃料电池-电池混合供能能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个根据机器人机动状态、负载功率、燃料电池氢耗值和电池 `SOC` 区间选择燃料电池工作模式并抑制电池过充的能量管理控制器。
- 判断：算。对象是真实机器人动力系统的上层 EMS，不是纯离线优化实验；原文明确给出机器人运动状态、燃料电池工作模式、充放电判定和 overcharge control。

### 1. 原文摘录

#### 摘录 A

- 出处：第 7-8 页，Section `4.1 Robot Maneuver State Identification Strategy`
> The proposed formulation aims to utilize various values of power demand, changes in power demand, and changes in robot movement speed as the fundamental concept for determining different states of the robot's status.
>
> In the above, the 5 different operation states of the robot for different conditions are as follows:
> - Stationary state: OSR = 0;
> - Acceleration state: OSR = 3;
> - Traction state: OSR = 2;
> - Deceleration mode: OSR = 1;
> - Regenerative braking state: OSR = -1.

#### 摘录 B

- 出处：第 13-15 页，Section `4.5 The Proposed Operational Mode Control Strategy`
> The proposed energy management strategy incorporates various states of robot movement, PEMFC production modes, P demand modes, and the LFP battery SOC range as inputs.
>
> the initial strategy has determined six operational modes for a fuel cell electric robot equipped with a LFP battery.
>
> The primary consideration when selecting an operational mode (i) is to obtain the optimal efficiency of the fuel cell with the lowest HCJE H2.

#### 摘录 C

- 出处：第 14-15 页，Section `4.5 The Proposed Operational Mode Control Strategy`
> When the FC produces more power than the robot's demanded power, the excess power charges the LFP battery.
>
> Producing an FC power less than the demanded power results in the discharge of the LFP battery.
>
> Figure 12 identifies 100 distinct scenarios for determining the proposed operational modes.
>
> Among the 20 available scenarios, the FC must operate on maximum power ... in two distinct scenarios ... the fuel cell is deactivated ...
>
> the fuel cell operates at maximum overall efficiency with the lowest equivalent hydrogen consumption rate (PFC mode = 0.4 pu) in 46 scenarios.

#### 摘录 D

- 出处：第 15-19 页，Section `4.6 Battery Overcharge Control Strategy` / `5 Results`
> If the battery's SOC is higher than its initial SOC and the battery can provide enough power on its own, the fuel cell is deactivated (PFC = 0) to prevent fuel consumption.
>
> Figure 15 illustrates the maneuver state of the fuel cell electric robot's status function.
>
> The application of the proposed modes has successfully eliminated the PEMFC output power ripple.
>
> The SOC difference at the end of the robot's maneuver is consistently maintained at a positive level (+0.4%) to ensure that the battery remains unaffected by various operating conditions and does not discharge.

### 2. 基于原文整理后的自然语言描述

The fuel-cell electric robot uses a maneuver-aware energy-management controller that first classifies the robot motion into five discrete operating states, namely `stationary`, `acceleration`, `traction`, `deceleration`, and `regenerative braking`, using the signs of demanded power, power variation, and speed variation. On top of that motion state, the controller also classifies the battery into `SOC` zones through the `SBCE` function and classifies the PEM fuel cell into six operating modes according to hydrogen-consumption-per-joule efficiency. The operational-mode selector then combines robot motion state, fuel-cell mode, demanded-power mode, and battery `SOC` range to choose the appropriate hybrid-power action, allowing battery charging only when the equivalent hydrogen cost is better than the next mode and allowing battery discharge only when the combined equivalent cost remains superior. Across the `100` enumerated scenarios, the controller sends the fuel cell to maximum power in the high-demand cases, fully turns the fuel cell off in two high-charge low-demand cases, and uses the maximum-efficiency `0.4 pu` fuel-cell mode in `46` scenarios, while also deciding whether the battery should charge or discharge. A dedicated battery-overcharge control law further shuts the fuel cell down whenever the battery `SOC` is above its initial level and the battery alone can sustain the load, which is why the simulation ends with only about `+0.4%` `SOC` drift and a ripple-free PEMFC output profile.

### 3. 逐句溯源

1. 句子 1：The fuel-cell electric robot uses a maneuver-aware energy-management controller that first classifies the robot motion into five discrete operating states, namely `stationary`, `acceleration`, `traction`, `deceleration`, and `regenerative braking`, using the signs of demanded power, power variation, and speed variation.
   对应摘录：A
2. 句子 2：On top of that motion state, the controller also classifies the battery into `SOC` zones through the `SBCE` function and classifies the PEM fuel cell into six operating modes according to hydrogen-consumption-per-joule efficiency.
   对应摘录：B
3. 句子 3：The operational-mode selector then combines robot motion state, fuel-cell mode, demanded-power mode, and battery `SOC` range to choose the appropriate hybrid-power action, allowing battery charging only when the equivalent hydrogen cost is better than the next mode and allowing battery discharge only when the combined equivalent cost remains superior.
   对应摘录：B, C
4. 句子 4：Across the `100` enumerated scenarios, the controller sends the fuel cell to maximum power in the high-demand cases, fully turns the fuel cell off in two high-charge low-demand cases, and uses the maximum-efficiency `0.4 pu` fuel-cell mode in `46` scenarios, while also deciding whether the battery should charge or discharge.
   对应摘录：C
5. 句子 5：A dedicated battery-overcharge control law further shuts the fuel cell down whenever the battery `SOC` is above its initial level and the battery alone can sustain the load, which is why the simulation ends with only about `+0.4%` `SOC` drift and a ripple-free PEMFC output profile.
   对应摘录：D
