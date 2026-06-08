# PR-M3 codex exec skill 实验报告：path1_cara

## Run identity

- case_key: `path1_cara`
- case_id: `cara-infusion-pump-formal-spec__01`
- path: `path1`
- output_dir: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara`
- status: `completed_valid_candidate`
- provider config seen: `model_provider=airouter`（仅脱敏配置；未读取或写入 raw endpoint/API key）
- final_model_sha256: `d473c81f4c5684da0ecbfcf01b4790eadc93e16f33ca808b0d87803bb035d9db`

## Input

**NL 原文**

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

**NL 中文释义**

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

paper_dir: `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`

## Actual Reads

| 类别 | 路径 | 用途 |
| --- | --- | --- |
| skill_entry_symlink | project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md | PR-M3/E2 skill contract; symlink resolved successfully to AGENT_LOOP_SKILL.md |
| skill_guide | project_1_llm_state_machine_modeling/method/agent_loop_skill/e2e_ref_model_guide.md | E0-E7 workflow, allowed/forbidden calls, grounding and scenario provenance rules |
| skill_guide | project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md | SD deterministic tool API and repair-chain requirements |
| skill_guide | project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md | SL prompt-generator contract and repair review schema |
| skill_guide | project_1_llm_state_machine_modeling/method/agent_loop_skill/nfrr_evaluation_guide.md | NFRR v3 claim, ledger, scoring, tier, cap and allowed_use rules |
| skill_guide | project_1_llm_state_machine_modeling/method/agent_loop_skill/codex_exec_experiment_guide.md | PR-M3 artifact package, report and redaction requirements |
| skill_guide | project_1_llm_state_machine_modeling/method/agent_loop_skill/stages/README.md | stage index policy and PR-E1 repair-chain override |
| paper_metadata | project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/bibtex.bib | confirm paper bibliographic identity |
| paper_derivative | project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/STM.md | identify CARA pump manual/autocontrol EFSM and cuff backManual source |
| paper_derivative | project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/DESC.md | scope and reading-route context |
| paper_text | project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper_content.txt | grounding spans: pump modes, Algorithm/Caregiver Interface, fault release, backManual, Mode_Control_Algorithm |
| redacted_run_context | runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/run_manifest.json | case metadata, input NL/NL_zh, redacted command/config |
| redacted_run_context | runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/env.redacted.json | confirm provider config was seen without raw secrets |
| redacted_run_context | runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/command.redacted.txt | confirm codex exec command shape without secrets |
| input_prompt | runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/prompt.md | confirm task prompt and hard boundaries |
| tool_api | project_1_llm_state_machine_modeling/method/stages/api.py | stable allowed facade for SD/SC/SL functions |
| tool_api | project_1_llm_state_machine_modeling/method/stages/sd_tools.py | SD-2/3/4/5A/6/freeze behavior and warning classification |
| tool_schema | project_1_llm_state_machine_modeling/method/schema.py | StageContext/TestScenario/ScenarioStep/ScenarioSet schema |
| tool_runtime | project_1_llm_state_machine_modeling/method/feedback/sim.py | SD-6 scenario execution semantics |
| dsl_grammar | pyfcstm/pyfcstm/dsl/grammar/GrammarLexer.g4 | confirm token support for def int/float, events, forced transitions and expressions |
| dsl_grammar | pyfcstm/pyfcstm/dsl/grammar/GrammarParser.g4 | confirm actual SD-2 grammar for transitions, guards, effects and aspect actions |
| tool_runtime | pyfcstm/pyfcstm/simulate/runtime.py | debug event path resolution for SD-6 |
| tool_runtime | pyfcstm/pyfcstm/model/model.py | debug transition/event origin and forced transition expansion |
| tool_usage_reference | project_1_llm_state_machine_modeling/method/tests/stages/test_sd_tools.py | confirm legal DSL snippets, scenario freeze/use, and CARA structural repair-review examples |

说明：`paper.pdf` 由 harness 检测并散列，但本 runner 未直接打开 PDF；实际 grounding 使用 `paper_content.txt`、`STM.md`、`DESC.md` 和 `bibtex.bib`。

## Evidence Grounding

| span | 来源 | 位置 | 证据摘要 |
| --- | --- | --- | --- |
| P-1 | paper_content.txt | 231-251 | pump fault alarm/release, shared sensor buffer, pump manual/autocontrol modes |
| P-2 | paper_content.txt | 367-384 | CARA components, Algorithm controls/logs flow, higher BP lower flow, caregiver interface initiates/terminates/displays errors |
| P-3 | paper_content.txt | 490-539 | Pump monitors, occlusion and global backManual expression |
| P-4 | paper_content.txt | 1303-1323 | Mode_Control_Algorithm states and Ask_StartAC StartAC submode semantics |
| P-5 | STM.md | 条目 1 | curated CARA pump manual/autocontrol EFSM extraction |

## Process Summary

| 阶段 | 结果 | 摘要 |
| --- | --- | --- |
| E0 skill discovery | 完成 | 读取 skill 入口与 5 个指定指南，确认禁止一键 runner、允许 method.stages.api。 |
| E1 evidence grounding | 完成 | 从 NL 抽取 10 个 span/obligation，并读取 bibtex、STM、DESC、paper_content 关键行。 |
| E2 initial modeling | 完成 | 生成 pyfcstm DSL；布尔语义统一用 int 0/1；连续 BP/flow 离散为高低档。 |
| E3 deterministic checks | 完成 | 最终 SD-2/3/4 通过；SD-5A 为 mutation 覆盖 advisory；SD-6 8/8 pass。 |
| E4 repair/waiver | 完成 | 修复 leaf during before、Ask_StartAC 子模式退出、forced event 注入路径；advisory 以 waiver ledger 记录。 |
| E5 NFRR | 完成 | NFRR v3: FE/NGF/REC/SCB/BVS 高，GAS/DMR 因抽象和 mutation 部分覆盖为 2。 |
| E6 final audit | 完成 | 写入 final_model/report/metadata/ledgers，检查 forbidden call 与 secret redaction 风险。 |

## Checks / Repair / NFRR Summary

| 检查 | 结果 | 说明 |
| --- | --- | --- |
| SD-2 | pass | 详见 tool_stage_check_ledger.json |
| SD-3 | pass | 详见 tool_stage_check_ledger.json |
| SD-4 | pass_no_blocking | 详见 tool_stage_check_ledger.json |
| SD-5A | advisory_gap | 详见 tool_stage_check_ledger.json |
| SC-5F | pass | 详见 tool_stage_check_ledger.json |
| SD-6 | pass 8/8 | 详见 tool_stage_check_ledger.json |

| 维度 | 分数 | 主要证据/限制 |
| --- | --- | --- |
| FE | 3 | SD-2/3/4 pass；无 unwaived blocking |
| NGF | 3 | 10 个 required obligations 无 critical/major contradiction |
| REC | 3 | weighted_recall=1.0；均 exact/abstract matched |
| GAS | 2 | BP 高则低流量与 release/action 均覆盖；连续控制公式仅离散化 |
| SCB | 3 | scope=full_NL_fragment；cuff handler 仅作为 CB_backManual provenance |
| AAT | 2 | synthetic/helper/output-only ledger 完整，但未人工签核 |
| BVS | 3 | 8 个 obligation-anchored 场景均从默认前缀执行，SD-6 8/8 pass |
| DMR | 2 | SD-5A mutation caught 10/12；wrong target/wrong effect 仍部分覆盖 |

NFRR: `tier_before_cap=T3`，cap=`IND_SINGLE_SELF_ASSESSMENT` + `NO_HUMAN_SIGNOFF`，final=`T2`，allowed_use=`reviewer_queue`。

## Final FCSTM

```fcstm
def int CA_mode = 0;
def int shared_bp_buffer = 80;
def int blood_pressure = 80;
def int target_bp = 80;
def int default_flow_rate = 1;
def int ask_exit_target = 0;
def int pump_speed_source = 0;
def int control_voltage = 0;
def int infusion_rate = 1;
def int log_written = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int software_control = 0;
def int pump_control_released = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;

        >> during before {
            shared_bp_buffer = blood_pressure;
        }

        [*] -> Wait;

        state Wait {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_speed_source = 0;
            }
        }

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_speed_source = 0;
                pump_control_released = 0;
                alarm_signal = 0;
                error_message = 0;
            }
            during {
                infusion_rate = default_flow_rate;
                control_voltage = 0;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitingStart;

            state AwaitingStart;

            enter {
                CA_mode = 1;
                software_control = 0;
                ask_exit_target = 0;
            }

            AwaitingStart -> AwaitingStart :: ChangeSetpoint effect {
                target_bp = target_bp + 1;
            }

            AwaitingStart -> [*] :: StartAC effect {
                ask_exit_target = 1;
            }

            AwaitingStart -> [*] :: TerminateAC effect {
                ask_exit_target = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                software_control = 1;
                pump_speed_source = 1;
                pump_control_released = 0;
                log_written = 1;
            }
        }

        state Autocontrol {
            enter {
                CA_mode = 3;
                software_control = 1;
                pump_speed_source = 1;
                pump_control_released = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
                infusion_rate = (blood_pressure > target_bp) ? 1 : 2;
                control_voltage = infusion_rate;
                log_written = 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
            }
        }

        Wait -> Manual :: BuiltInSwitchSet;
        Manual -> Manual :: SetDefaultFlow effect {
            default_flow_rate = default_flow_rate + 1;
        }
        Manual -> Ask_StartAC :: InitiateAC;

        Ask_StartAC -> AutocontrolInit : if [ask_exit_target == 1];
        Ask_StartAC -> Manual : if [ask_exit_target == 0];

        AutocontrolInit -> Autocontrol :: AutoReady;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFault :: PumpFault effect {
            software_control = 0;
            pump_control_released = 1;
        }

        Autocontrol -> Autocontrol :: ControlTick;
        Autocontrol -> Manual :: TerminateAC;
        Autocontrol -> PumpFault :: PumpFault effect {
            software_control = 0;
            pump_control_released = 1;
        }

        Manual -> PumpFault :: PumpFault effect {
            software_control = 0;
            pump_control_released = 0;
        }

        PumpFault -> Manual :: FaultRemoved;
    }
}
```

## Quality Risks and Limitations

- `ask_exit_target` 是 pyfcstm 可执行化 helper，用于表达 Ask_StartAC 子模式在 StartAC/TerminateAC 后退出到不同父级目标；它不是论文变量。
- 血压、流量和控制电压被离散为整数档位，只验证“血压更高 -> 流量更低”的方向，不还原临床连续控制公式。
- `PumpFault` 聚合 occlusion 等泵并发症；未区分 occlusion/impedance/back-EMF 等子监视器。
- `alarm_signal`、`error_message`、`log_written`、`pump_control_released` 是输出/观测 flag，不是完整 UI、声响、日志文件系统。
- SD-5A mutation coverage 仍有 advisory gap；该模型可进 reviewer queue，但不能称为 signed reference 或 final ground truth。

## Reviewer Queue Decision

可以进入 reviewer queue：`final_tier=T2`、`allowed_use=reviewer_queue`，但需要人工/独立 reviewer 复核 abstraction、scenario oracle 和 mutation gaps 后才能升级为 paper-grounded/signed reference。
