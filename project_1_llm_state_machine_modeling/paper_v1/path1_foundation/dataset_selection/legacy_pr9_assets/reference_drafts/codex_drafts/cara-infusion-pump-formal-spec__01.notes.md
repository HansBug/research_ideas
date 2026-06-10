# Codex Draft Notes — Case cara-infusion-pump-formal-spec__01

## 1. 设计选择

- mode 列表：
  - `Mode_Control_Algorithm`：来自 STM §1 摘录 C / expansion [E12]，表示 CARA 模式控制层次。
  - `Wait`：来自 STM §1 摘录 C / expansion [E12] 的 four states of CARA。
  - `Manual`：来自 pump manual/autocontrol modes [E4] 与 four states [E12]。
  - `Ask_StartAC`：来自 Ask_StartAC submode [E12]，其内部可修改 setpoint 并通过 StartAC 进入 `AutocontrolInit` [E13]。
  - `AutocontrolInit`：来自 four states [E12] 与 StartAC 进入 AutocontrolInit [E13]。
  - `Autocontrol`：来自 pump autocontrol mode [E4]、four states [E12] 与 normal autocontrol [E14]。
- event 列表：
  - `InitiateAlgorithmicPumpControl`：caregiver initiates algorithmic pump control [E10]。
  - `ChangeSetpoint`：Ask_StartAC 中 setpoint can be changed [E13]，对应 caregiver modifies target blood pressure [E10]。
  - `StartAC`：pressing StartAC enters AutocontrolInit [E13]。
  - `TerminateAlgorithmicPumpControl`：caregiver can terminate algorithm control [E10]。
  - `PumpOperationComplication`：pump complications/faults [E14] [E15] [E16]。
  - `CA_backManual`、`CB_backManual`、`CP_backManual`、`CC_backManual`：四个 back-to-manual 触发源 [E17]。
- variable 列表：
  - 无持久 `def` state variable；本 case 没有数值阈值、计数器或后续 guard 需要读取的变量。
  - transition `effect { ... = 1; }` 中的名称是 pyfcstm block-local action marker，用于让 5-component extractor 捕获 transition actions；它们不是 persistent boolean flag，也不表达 domain threshold。
- transition 设计：
  - `[*] -> Wait` 与 `Wait -> Manual`：对应 Figure 11 的 initial point、wait 和 manual 主链 [E12]。
  - `Manual -> Ask_StartAC : InitiateAlgorithmicPumpControl`：对应 caregiver initiate algorithmic pump control [E10]。
  - `Ask_StartAC -> Ask_StartAC : ChangeSetpoint`：对应 Ask_StartAC 中 setpoint can be changed [E13]。
  - `Ask_StartAC -> AutocontrolInit : StartAC`：对应 pressing StartAC enters AutocontrolInit [E13]。
  - `AutocontrolInit -> Autocontrol`：对应 AutocontrolInit 进入 normal autocontrol [E12]，并在 effect 中标记 external control voltage selected [E7]。
  - `Autocontrol -> Manual : TerminateAlgorithmicPumpControl`：对应 caregiver terminate algorithm control [E10]，并释放 CARA 控制 [E16]。
  - `Autocontrol -> Manual : PumpOperationComplication`：对应 complications/faults cause alarm, caregiver fault removal, release control, and manual fallback [E14] [E15] [E16]。
  - `! * -> Manual : CA_backManual/CB_backManual/CP_backManual/CC_backManual`：对应任一 backManual 触发 CA_mode become Manual [E17]。
- 5-component IR 抽取计数：`{states: 6, transitions: 12, guards: 0, actions: 6, hierarchical: 1}`

## 2. pyfcstm primitive 使用情况（仅说明，不强求覆盖 4 个）

- **forced transition `!`**：用 — [E17] 明确给出四个跨组件 backManual 源共享 Manual recovery target，适合用四条全局 forced event transition。
- **aspect `>> during`**：未用 — 原文没有 per-tick monitor 或 every-cycle invariant；`Autocontrol` 的 `during abstract` 只表达处于 normal autocontrol 时持续控制/记录，不是横切 aspect。
- **abstract action**：用 — sensor buffer、manual switch/default flow、external voltage、rate computation、log files、error/fault 相关动作均是硬件或外部 handler 语义 [E3] [E5] [E6] [E7] [E8] [E9] [E15] [E16]。
- **multivar arith guard**：未用 — 本 case 没有数值阈值、算术条件或复合数值 guard；四源 backManual 是 event/fallback 语义 [E17]。

## 3. 与 NL 的对应关系

- expansion NL [E1] [E2] [E3]: CARA coordinates components, pump moves fluid, sensor readings stored in shared buffer → `state Mode_Control_Algorithm` + `enter abstract CoordinateCaregiverInterfaceBloodPressureMonitorAlgorithmPumpMonitors` + `enter abstract StoreSensorReadingsInSharedBuffer`。
- expansion NL [E4]: pump has manual and autocontrol modes → `state Manual`、`state Autocontrol`。
- expansion NL [E5] [E6]: manual mode uses built-in switch and default flow rate → `Manual.enter abstract UseBuiltInPumpSwitchForManualSpeed`、`UseDefaultFlowRateSetOnPump`。
- expansion NL [E7]: autocontrol speed set by external control voltage → `AutocontrolInit.enter abstract ApplyExternalControlVoltageToPumpSpeed` and `AutocontrolInit -> Autocontrol effect { external_control_voltage_selected = 1; }`。
- expansion NL [E8] [E9]: Algorithm controls infusion rate, logs data, computes rate from blood pressure, and higher pressure produces lower flow rate → `Autocontrol.during abstract ComputeInfusionRateFromBloodPressure`、`ComputeHigherPressureLowerFlowRate`、`ControlInfusionRateWhenNoPumpOperationComplications`、`RecordInfusionRelatedDataInLogFiles`。
- expansion NL [E10]: caregiver modifies target BP, initiates/terminates control → `Manual -> Ask_StartAC : InitiateAlgorithmicPumpControl`、`Ask_StartAC -> Ask_StartAC : ChangeSetpoint`、`Autocontrol -> Manual : TerminateAlgorithmicPumpControl`。
- expansion NL [E11] [E15] [E16]: fault triggers alarms/error messages, caregiver removes fault, software releases control → `Autocontrol -> Manual : PumpOperationComplication effect { alarm_signals_activated = 1; error_messages_displayed_and_sounded = 1; caregiver_removes_pump_fault = 1; CARA_control_released = 1; }`。
- expansion NL [E12] [E13]: Mode_Control_Algorithm hierarchy and Ask_StartAC submode → `Mode_Control_Algorithm` composite with `Wait`, `Manual`, `Ask_StartAC`, `AutocontrolInit`, `Autocontrol`; `Ask_StartAC -> AutocontrolInit : StartAC`。
- expansion NL [E17]: any backManual source causes CA_mode Manual → four forced transitions to `Manual` on `CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual`。

## 4. 迭代历史

- iter 1: 写出初稿，采用 6 states、forced backManual、abstract lifecycle actions、block-local transition action markers → verify: `ALL_OK`。
- iter 2: 将 shared-buffer action 上移到 `Mode_Control_Algorithm`，把 release-control 从 `Manual` entry 收紧到 terminate/fault transitions，并补充 error message 与 caregiver fault-removal action marker → verify: `ALL_OK`；extract: `EXTRACT_OK {'states': 6, 'transitions': 12, 'guards': 0, 'actions': 6, 'hierarchical_states': 1}`。
- iter 3: 补充 `Manual.enter { CA_mode_set_to_Manual = 1; }` 承载 forced backManual 的目标赋值语义，并增加 component coordination 与 higher-pressure/lower-flow abstract actions；随后移除 `CA_mode_set_to_Autocontrol` 这类可由 state/transition 本身表达的过度 marker → verify: `ALL_OK`；extract: `EXTRACT_OK {'states': 6, 'transitions': 12, 'guards': 0, 'actions': 6, 'hierarchical_states': 1}`。

## 5. 与 STM.md 表述的偏差（如有）

- 无偏差，DSL 覆盖 expansion NL 与 STM §1 中可进入 5-component 的 states / transitions / actions / hierarchical structure。
- 本 case 没有原文支持的数值阈值或算术条件，因此 `guards` 数为 0；`PumpOperationComplication` 和四个 backManual 源按 event-driven fallback 编码，避免引入未写入的 guard variable。

## 6. 已知 hallucination / 不确定项（必须自我披露）

- 无 hallucination。
- 编码约定：transition effect 中的 `... = 1` 是 pyfcstm block-local action marker，用来表达 NL 中的 transition action 并被 PATH1 extractor 捕获；它不是持久变量、不是 guard 输入，也不是论文给出的数值阈值。
