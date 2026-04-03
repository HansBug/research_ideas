# Developing and Verifying User Interface Requirements for Infusion Pumps: A Refinement Approach - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：围绕输液泵数据录入的变量、事件、entry mode、按键细化和 cursor 行为都可追溯。

## 条目 1: Infusion-pump data entry and programming flow
- 控制对象：输液泵用户界面的数据录入控制逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是医疗设备控制领域的 infusion pump user-interface control logic，用于让操作者进入数据录入、修改显示值并在满足条件时提交目标参数。
- 判断：算，但属于医疗设备界面控制子系统样本。对象仍是输液泵控制系统的一部分，原文给出了具体变量、事件、guard 和不同按键接口下的离散处理步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7-8 页，对 `choose / modify / set` 的操作化说明，行 232-259
> initialised to the source value and entry is false, indicating that entry of the target number has
> not commenced. The new requirement decomposes the event representing R1into three events.
> The ﬁrst one ( choose ) is used to elect to enter the target value, while the second one models
> the modiﬁcation of the display value (this is not necessarily the data value). The ﬁnal event is
> triggered when the display and target values are equal. At this step the data value is set to be
> equal to the display value and entry becomes false.
> ...
> Initialisation begin data :=source disp :=source entry :=FALSE end
> Event choose ... when entry =FALSE then disp :=data entry :=TRUE end
> Event modify ... when entry =TRUE then disp :∈ Numbers end
> Event set ... when disp=target entry =TRUE then data :=disp entry :=FALSE end

#### 摘录 B
- 出处：第 8-9 页，Section 6.1，对 chevron interface 与快慢按键细化的说明，行 289-329
> In chevron based interfaces, the current data value is updated by pressing the ‘up’ (increase)
> and ‘down’ (decrease) chevron keys.
> ...
> Both events are only enabled when the pump is in data entry
> mode ( entry=TRUE ).
> ...
> The slow ‘up’ and fast ‘up’ chevrons are modelled by the upandUPevents, respectively.
> The upevent ... increases the current value by delta at least, whereas UPincreases it by Delta.
> ...
> It is assumed that Delta is greater than delta to guarantee that
> the fast ‘up’ and ‘down’ chevrons are indeed faster than the slow ones.

#### 摘录 C
- 出处：第 9-10 页，Section 6.2，对 five-key interface 的说明，行 333-390
> In the case of ﬁve-key interfaces, numbers are modiﬁed by combining up and down keys with
> movement of the cursor keys. The size of the increment or decrement is measured by the position
> of the cursor that can be manipulated using the left and right keys.
> ...
> Two main variations are to simply wrap the digit ... and to modify the whole number according to the rules of arithmetic.
> ...
> Event left ... when entry =TRUE then cursor :=left(cursor) end
> ...
> The speciﬁcations of the up and down events can potentially be reﬁned into
> both types of ﬁve-key interfaces described earlier: arithmetic and wrapping.
> ...
> both
> events permit the implementations of ﬁve-key interfaces with memory.

### 2. 基于原文整理后的自然语言描述

The abstract programming process initializes `data = source`, `disp = source`, and `entry = FALSE`. The user starts entry with `choose`, which is enabled only when `entry = FALSE` and copies `data` into `disp` while setting `entry := TRUE`; while `entry = TRUE`, the `modify` event may change only the display value, and the `set` event commits `data := disp` and resets `entry := FALSE` only when `disp = target`. In chevron-based interfaces, `increase` and `decrease` are enabled only in data-entry mode, and a more concrete refinement distinguishes slow `up/dn` actions with minimum increment `delta` from fast `UP/DN` actions with minimum increment `Delta`, where `Delta > delta`. In five-key interfaces, `left` and `right` move a cursor position, while `up` and `down` change the digit selected by that cursor and may be refined into wrapping, arithmetic carry/borrow, or memory-based behaviors.

### 3. 逐句溯源

1. 句子 1：The abstract programming process initializes `data = source`, `disp = source`, and `entry = FALSE`.
   对应摘录：A
2. 句子 2：The user starts entry with `choose`, which is enabled only when `entry = FALSE` and copies `data` into `disp` while setting `entry := TRUE`; while `entry = TRUE`, the `modify` event may change only the display value, and the `set` event commits `data := disp` and resets `entry := FALSE` only when `disp = target`.
   对应摘录：A
3. 句子 3：In chevron-based interfaces, `increase` and `decrease` are enabled only in data-entry mode, and a more concrete refinement distinguishes slow `up/dn` actions with minimum increment `delta` from fast `UP/DN` actions with minimum increment `Delta`, where `Delta > delta`.
   对应摘录：B
4. 句子 4：In five-key interfaces, `left` and `right` move a cursor position, while `up` and `down` change the digit selected by that cursor and may be refined into wrapping, arithmetic carry/borrow, or memory-based behaviors.
   对应摘录：C
