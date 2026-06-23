# pairs_preview

- raw workbook：`assets/raw/drive_download/Experiment Results.xlsx`
- sheet：`STM Results`
- 可回溯生成 pair：60
- LLM 分布：Claude=10、DeepSeek=10、GPT-4=10、GPT-4o=10、Kimi=10、Llama=10

## 示例 0

```text
pair_id: llms_emp_stm_results_0000
LLM: GPT-4o
Model Source: HLDCS
Model Name: high-level driving module
NL: 1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
STM_0: @startuml | [*] --> HumanDriving |  | state HumanDriving { |     [*] --> InitialState : Power On |     InitialState : Initial State |     InitialState --> Autonomous : Front Distance > 10 |     Autonomous --> HumanDriving : Human Steering Cmd or Brake Pressed |     HumanDriving --> FinalState : Power Off |     FinalState : Final State | } |  | state Autonomous { |     [*] --> InitialState : Enter Autonomous |     InitialState : Initial State |     InitialState --> FinalState : Exit Autonomous | } | @enduml
```
