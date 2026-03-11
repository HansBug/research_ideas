# Formal specifications and analysis of the CARA Infusion Pump Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：OCR 后可稳定提取泵模式与 cuff handler 的状态/回退逻辑。

## 备注
- 本目录下的 `paper_content.txt` 已按仓库规范用 OCR 结果刷新，因为原文字提取严重失真。以下定位均基于刷新后的 OCR 文本。

## 条目 1: Pump manual/autocontrol modes
- 控制对象：CARA 输液泵控制系统中的泵控制模式
- 整理后的英文描述：The pump has two operating modes: `manual` and `autocontrol`. In manual mode the pump speed is set locally on the device; in autocontrol mode the speed is set by an external control voltage from CARA. If a pump fault occurs while CARA is controlling the pump, the software releases control, which implies a transition back out of autocontrol.
- 要素 1：模式显式给出为 `manual` 和 `autocontrol`。
- 要素 2：`manual` 下速度由泵本地开关设定。
- 要素 3：`autocontrol` 下速度由外部控制电压设定。
- 要素 4：泵故障时，若 CARA 正在控制，则 `software releases its control`，可整理为从自动控制退出。
- 定位 1：`paper_content.txt` 第 5 页，系统组件说明，行 233-264。
- 证据 1：`The pump has two modes, manual and autocontrol.`
- 证据 2：`In manual mode, the pump speed is set with a switch built into the pump.`
- 证据 3：`In autocontrol mode, the pumping speed is set by a control voltage from an external source.`
- 证据 4：`if they happen when the pump is being controlled by CARA, the software releases its control`

## 条目 2: Cuff Handler in Auto Control
- 控制对象：CARA 中基于 cuff 血压源的自动控制子状态机
- 整理后的英文描述：In auto control, the cuff handler stays in an `In Auto Control` state, selects a cuff reading frequency from blood pressure ranges, and keeps requesting readings. If repeated readings are invalid or a valid blood pressure cannot be obtained in time, it raises alarms and sets `CB_backManual = true`, i.e. it falls back to manual mode.
- 要素 1：状态/标识在 OCR 文本中可见：`In Auto Control`, `Cuff Invalid 1`, `Cuff InACWait`。
- 要素 2：根据 `CB_ctrlValue` 所在区间，转移到不同的 cuff 频率设置：60s / 120s / 300s / 600s。
- 要素 3：若血压读数持续无效，则触发 level-1 / level-2 alarm。
- 要素 4：当无法及时获得有效血压时，设置 `CB_backManual = true`，回退到 manual mode。
- 定位 1：`paper_content.txt` 第 11 页，Cuff Handler EFSM 图的 OCR 文本，行 787-840。
- 定位 2：`paper_content.txt` 第 12 页，Figure 6 “Requirements for the Cuff Handler in Auto Control”，行 899-923。
- 定位 3：`paper_content.txt` 第 13 页，Figure 7 变量表，行 930-944。
- 证据 1：`In Auto Control`
- 证据 2：`CB_ctrlValue < 60 ... -> CB_cuffFrequency = 60`
- 证据 3：`CB_ctrlValue < 70 ... -> CB_cuffFrequency = 120`
- 证据 4：`CB_ctrlValue < 90 ... -> CB_cuffFrequency = 300`
- 证据 5：`CB_ctrlValue <= 150 ... -> CB_cuffFrequency = 600`
- 证据 6：`CB_backManual = true`
- 证据 7：`If CARA can not obtain a valid blood pressure in 3 minutes, it should revert back to manual mode.`
