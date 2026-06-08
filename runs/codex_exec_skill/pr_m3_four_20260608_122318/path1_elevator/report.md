# PR-M3 Codex Exec Skill 实验报告：path1_elevator

## Run Identity

- run_label: `pr_m3_four_20260608_122318`
- case_key: `path1_elevator`
- case_id: `automatic-elevator-controller`
- path: `path1`
- status: `success`
- output_dir: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator`
- provider config: 未调用外部 provider，未读取 `.env`，`model_provider_config_seen=false`
- skill entry: `project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md`（软链接目标 `AGENT_LOOP_SKILL.md` 也已读取）

## Input

- NL source: `project_1_llm_state_machine_modeling/eval/data/sources/automatic-elevator-controller/nl.md`
- paper_dir: `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller`

### NL 原文

```text
# Automatic Elevator Controller — NL Requirement

来源：`sources/automatic-elevator-controller/STM.md` §2

The automatic elevator controller is built as a finite-state machine whose
state space combines floor states `F1`, `F2`, and `F3` with motion states
`MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state (on floor 1),
chooses either the up or down branch according to floor requests, stops at
the requested floor, and then immediately checks the next destination
before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as
sensing inputs for arrival. Transitions:

- From `F1`: `PS2` triggers `MU2`; `PS3` triggers `MU3`.
- From `F2`: `PS3` triggers `MU3`; `PS1` triggers `MD1`.
- From `F3`: `PS1` triggers `MD1`; `PS2` triggers `MD2`.
- Arrival sensors: `MU2 + S2 -> F2`; `MU3 + S3 -> F3`; `MD1 + S1 -> F1`;
  `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop
conditions. A reset signal forces the controller back to floor 1 regardless
of the outstanding request context.
```

### NL 中文翻译/释义

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

## Actual Reads

详见 [`actual_file_reads.json`](./actual_file_reads.json)。关键读取包括 skill 入口、`e2e_ref_model_guide.md`、`tools.md`、`prompts.md`、`nfrr_evaluation_guide.md`、`codex_exec_experiment_guide.md`、当前 pyfcstm grammar、SD 工具示例、`nl.md`、`bibtex.bib`、`STM.md`、`DESC.md`、`paper_content.txt`。`paper.pdf` 已检测但未打开，因为文本抽取结果连贯，且算法/结果分析段已经足够支撑建模。

## Evidence Grounding 摘要

- 状态：`F1/F2/F3/MU2/MU3/MD1/MD2` 来自 NL lines 5-7、`STM.md` lines 71-77、`paper_content.txt` lines 155-163。
- 请求/传感事件：`PS1/PS2/PS3/S1/S2/S3` 来自 NL lines 14-21、`paper_content.txt` lines 169-204。
- 输出：`hbrg` 来自 NL lines 23-25、`paper_content.txt` lines 156-163 和 171-204；模型中使用 `0=stop, 1=up, 2=down` 的 int 抽象。
- reset：来自 NL lines 23-25、`paper_content.txt` lines 207-209；用 root-level forced transition 表达。

## Process Table

| 阶段 | 结果 | 摘要 |
| --- | --- | --- |
| E0 skill discovery | 通过 | 读取 SKILL.md/AGENT_LOOP_SKILL.md 与五个必须指南；确认禁止顶层 runner，允许 method.stages.api。 |
| E1 evidence grounding | 通过 | 读取 NL、bibtex、STM、DESC、paper_content；状态/转移/output/reset 均有 NL+paper 依据。 |
| E2 initial modeling | 通过 | 生成 floor/motion state model；PS/S/reset 为事件；hbrg 为 int 输出。 |
| E3 deterministic checks | 通过 | SD-2/3/4 pass；SD-5A/SC-5F/SD-6 pass；8/8 scenarios pass。 |
| E4 repair/waiver | 通过 | 删除非必要 floor_code；保留 hbrg output-only waiver；SD-10 count drift 已解释。 |
| E5 NFRR | 通过 | FE/NGF/REC/GAS/SCB/AAT/BVS=3，DMR=2；单会话自评 cap 到 T2。 |
| E6 final audit | 通过 | forbidden_runner_used=false；未读取 .env；未写 raw secret。 |

## Checks / Repair / NFRR 表

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| SD-2 parse | pass | 当前 parser 接受 final_model.fcstm。 |
| SD-3 semantic | pass | 语义构建成功。 |
| SD-4 design | pass | blocking=0；advisory=1（hbrg output-only）。 |
| SD-5A coverage | pass | wrong-target 与 missing-forced-transition mutants 被场景捕获；guard/effect 类不适用或受限。 |
| SC-5F freeze | pass | scenario_set_id=scenario-set-24a8916a4111。 |
| SD-6 sim | pass | 8/8 scenarios pass；oracle_weak=False。 |

| Repair/Waiver | 决定 | 依据 |
| --- | --- | --- |
| FR-001 删除 `floor_code` | accept + waiver SD-10 count_drift | 该变量只是初版场景观测 scaffolding；楼层由状态路径表达；最终 SD-6 8/8 pass。 |
| FR-002 保留 `hbrg` | output-only waiver | `hbrg` 是论文/NL 明确输出，不应人为接入 guard 消警。 |

| NFRR 字段 | 值 | 说明 |
| --- | --- | --- |
| claim | NL+paper / full_NL_fragment / single_self_assessment | 同一 agent 会话自评，未独立仲裁。 |
| vector | {'FE': 3, 'NGF': 3, 'REC': 3, 'GAS': 3, 'SCB': 3, 'AAT': 3, 'BVS': 3, 'DMR': 2} | 形式、语义、覆盖、行为验证强；DMR=2 因 mutation 类型覆盖有限。 |
| tier_before_cap | T3 | 证据强度可达 strong candidate 条件。 |
| final_tier | T2 | single_self_assessment hard cap 到 T2。 |
| allowed_use | reviewer_queue | AU-3：T2 + NL+paper。 |

## Final FCSTM

- sha256: `b5029bb2a00886f5da1392ee2506afa4b6aed735eee772bb0ad0ac8f29d4ded7`

```fcstm
def int hbrg = 0;

state ElevatorController {
    event PS1;
    event PS2;
    event PS3;
    event S1;
    event S2;
    event S3;
    event reset;

    state F1 {
        enter {
            hbrg = 0;
        }
    }

    state F2 {
        enter {
            hbrg = 0;
        }
    }

    state F3 {
        enter {
            hbrg = 0;
        }
    }

    state MU2 {
        enter {
            hbrg = 1;
        }
    }

    state MU3 {
        enter {
            hbrg = 1;
        }
    }

    state MD1 {
        enter {
            hbrg = 2;
        }
    }

    state MD2 {
        enter {
            hbrg = 2;
        }
    }

    [*] -> F1;

    F1 -> MU2 : PS2;
    F1 -> MU3 : PS3;
    F2 -> MU3 : PS3;
    F2 -> MD1 : PS1;
    F3 -> MD1 : PS1;
    F3 -> MD2 : PS2;

    MU2 -> F2 : S2;
    MU3 -> F3 : S3;
    MD1 -> F1 : S1;
    MD2 -> F2 : S2;

    ! * -> F1 : reset;
}
```

## Quality Risks And Limitations

1. `hbrg` 的二进制论文输出 `00/01/10` 被抽象为 int `0/1/2`，属于可追溯的编码抽象。
2. 当前模型不保存“未完成请求队列”或多请求调度策略；NL 只要求到达后检查下一目的地，本模型以楼层停靠态上的请求事件继续触发表达。
3. SD-5A mutation 捕获了 wrong target 与 missing forced reset，但没有覆盖 state-entry output mutation，因此 DMR 不是 3。
4. NFRR 为 single self assessment，未经过独立 reviewer/human signoff；因此可进入 reviewer queue，但不是 signed reference。
5. attached tmux runtime 没有单独的 `codex exec --json` 外部事件流；`codex_events.jsonl` 仅记录该事实，不伪造事件。

## Reviewer Queue 结论

可以进入 reviewer queue：`final_tier=T2`，`allowed_use=reviewer_queue`，SD-2/SD-3/SD-4/SD-6 均通过，无 unwaived blocking，无 hot-start 主证据，无 forbidden runner 使用。
