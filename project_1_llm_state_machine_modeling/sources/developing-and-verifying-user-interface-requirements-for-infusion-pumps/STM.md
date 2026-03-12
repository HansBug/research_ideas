# Developing and Verifying User Interface Requirements for Infusion Pumps: A Refinement Approach - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：围绕输液泵数据录入的进入、修改、提交和 entry mode 条件有清楚的离散描述。

## 条目 1: Infusion-pump data entry and programming flow
- 控制对象：输液泵用户界面的数据录入控制逻辑

### 0. 条目识别与判定

- 一句话说明：这是医疗设备控制领域的 infusion pump user-interface control logic，用于让操作者进入数据录入、修改显示值并在满足条件时提交目标参数。
- 判断：算，但属于医疗设备界面控制子系统样本。对象仍是输液泵控制系统的一部分，原文给出了 entry、modify 和 commit 的离散处理步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section 5.1，对 programmable requirement 的抽象描述，行 195-200
> The requirement R1(The ﬂow rate for the pump shall be programmable ) is expressed as the
> following machine in Event-B. This abstract description simply requires that a variable called
> data has the attribute that it is programmable. The requirement asserts that data commences with
> a value named source and describes the event programmable as changing the value to target . The
> possible values of data are given as the set Numbers . All three constants, Numbers ,source and
> target , are deﬁned in the context ReqParams1 below. Nothing is contained in the requirement to

#### 摘录 B
- 出处：第 7 页，Page 7，对 choose / modify / final event 的操作化说明，行 238-244
> initialised to the source value and entry is false, indicating that entry of the target number has
> not commenced. The new requirement decomposes the event representing R1into three events.
> The ﬁrst one ( choose ) is used to elect to enter the target value, while the second one models
> the modiﬁcation of the display value (this is not necessarily the data value). The ﬁnal event is
> triggered when the display and target values are equal. At this step the data value is set to be
> equal to the display value and entry becomes false. This operational requirement indicates more
> about the programming process but says little about how the value is entered.

#### 摘录 C
- 出处：第 8 页，Section 6.1，对 chevron data entry 的说明，行 297-306
> 6.1 Chevron interfaces
> In chevron based interfaces, the current data value is updated by pressing the ‘up’ (increase)
> and ‘down’ (decrease) chevron keys. These interfaces always include at least one ‘up’ and one
> ‘down’ chevron, however more chevrons could be used to speed up data entry. For example, a
> fast ‘up’ chevron may increase the current value by a larger amount compared to a slow ‘up’ one.
> Interface speciﬁcation. An abstract speciﬁcation of the chevron based interface, machine
> Chevron Entry1 deﬁnes two events for updating data values: increase anddecrease . The ﬁrst in-
> creases the current value ( disp) by an unspeciﬁed (non-deterministically chosen) amount, while
> the second similarly decreases it. Both events are only enabled when the pump is in data entry
> mode ( entry=TRUE ). The increase event is speciﬁed as follows:

### 2. 基于原文整理后的自然语言描述

The pump interface requires the target value to be programmable from an initial source value to a target value. In the operationalized programming process, entry starts from the source value, the user chooses to enter the target, modifies the displayed value, and the data value is updated when the display reaches the target. For chevron-based entry, the increase and decrease actions are enabled only when the pump is in data entry mode.

### 3. 逐句溯源

1. 句子 1：The pump interface requires the target value to be programmable from an initial source value to a target value.
   对应摘录：A
2. 句子 2：In the operationalized programming process, entry starts from the source value, the user chooses to enter the target, modifies the displayed value, and the data value is updated when the display reaches the target.
   对应摘录：B
3. 句子 3：For chevron-based entry, the increase and decrease actions are enabled only when the pump is in data entry mode.
   对应摘录：C
