# PR-M3 codex exec skill 实验报告：path1_elevator

## 0. Run identity

| 字段 | 值 |
|---|---|
| run_label | `pr_m3_four_clean_20260608_133322` |
| case_key | `path1_elevator` |
| case_id | `automatic-elevator-controller` |
| Path | `path1` |
| 输出目录 | `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator` |
| 状态 | `valid_run`，可进入 reviewer queue |
| provider config | 只记录脱敏标签；未读取或输出 `.env` secret / endpoint / token |
| forbidden runner | 未调用 `method.loop.run_agent_loop(...)`、PR-D runner、PR-E1 runner 或一键 full staged runner |

## 1. Input

NL 来源：`project_1_llm_state_machine_modeling/eval/data/sources/automatic-elevator-controller/nl.md`

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

中文释义：

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

paper_dir：`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller`

## 2. Actual reads

| 类型 | 路径 | 用途 |
|---|---|---|
| skill_entry | `project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md` | repo-local skill entry; symlink resolved by shell |
| skill_guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/e2e_ref_model_guide.md` | E2 modeling/check/repair/report boundary |
| skill_guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md` | SD tool facade and stage order |
| skill_guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md` | SL prompt generator and repair ledger contract |
| skill_guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/nfrr_evaluation_guide.md` | NFRR v3 claim/vector/tier/cap schema |
| skill_guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/codex_exec_experiment_guide.md` | PR-M3 artifact/report contract |
| tool_doc | `project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md` | actual parser-compatible FCSTM syntax and event scope rules |
| tool_source | `project_1_llm_state_machine_modeling/method/stages/api.py` | stable method.stages.api import surface |
| tool_source | `project_1_llm_state_machine_modeling/method/stages/sd_tools.py` | SD-2/3/4/5A/6/8/10 implementation behavior |
| tool_source | `project_1_llm_state_machine_modeling/method/schema.py` | ScenarioStep/TestScenario/ScenarioSet schemas |
| tool_source | `project_1_llm_state_machine_modeling/method/feedback/sim.py` | SD-6 runtime execution semantics |
| tool_doc | `project_1_llm_state_machine_modeling/method/stages/docs/SD-5A-scenario-coverage.md` | scenario coverage stage contract |
| tool_doc | `project_1_llm_state_machine_modeling/method/stages/docs/SD-6-sim.md` | simulation stage contract |
| tool_fixture | `project_1_llm_state_machine_modeling/method/stages/fixtures/SD-6.json` | SD-6 output shape example |
| tool_test | `project_1_llm_state_machine_modeling/method/tests/experiments/test_scenario_normalization.py` | event injection/default dispatch behavior reference |
| tool_test | `project_1_llm_state_machine_modeling/method/tests/stages/test_sd_tools.py` | SD facade examples and forced transition checks |
| case_input | `project_1_llm_state_machine_modeling/eval/data/sources/automatic-elevator-controller/nl.md` | authoritative case NL source |
| paper_material | `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/bibtex.bib` | paper metadata |
| paper_material | `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/STM.md` | human-extracted STM evidence and NL provenance |
| paper_material | `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/DESC.md` | paper/case overview and reading guidance |
| paper_material | `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper_content.txt` | paper text spans for algorithm/result/reset evidence |

说明：未读取 `paper.pdf`，因为 `paper_content.txt` 与 `STM.md`/`DESC.md` 已覆盖状态机、算法、结果与 reset 证据，且没有发现需要回 PDF 核对的提取异常。

## 3. Evidence grounding 摘要

| 元素 | 证据 | 建模处理 |
|---|---|---|
| 楼层态 | NL-1；`paper_content.txt` 155-156 | 直接建成 `F1/F2/F3` |
| 上行运动态 | NL-1；`paper_content.txt` 156-157 | 直接建成 `MU2/MU3`，entry 设置 `hbrg=1` |
| 下行运动态 | NL-1；`paper_content.txt` 162-163 | 直接建成 `MD1/MD2`，entry 设置 `hbrg=2` |
| 请求事件 | NL-3 到 NL-6；`paper_content.txt` 169-203 | `PS1/PS2/PS3` 按事件触发转移 |
| 到位事件 | NL-3/NL-7；`paper_content.txt` 170-203 | `S1/S2/S3` 按事件完成运动到楼层转移 |
| 输出 | NL-8；`paper_content.txt` 156-163、171-203 | `hbrg` 用 int 编码：0=stop, 1=up, 2=down |
| reset | NL-9；`paper_content.txt` 207-208 | root event `/reset` + forced transition `! * -> F1 : /reset` |

## 4. Process table

| Stage | 结果 | 获取的信息 / 反馈 | DSL 修改 |
|---|---|---|---|
| E0 Skill discovery | pass | 读取 skill 入口、E2/M3/NFRR/tool/prompt 文档；确认禁止顶层 runner。 | 无 DSL 修改 |
| E1 Evidence grounding | pass | 从 NL、STM、DESC、paper_content 120-210 抽取楼层态、运动态、请求事件、到位事件、hbrg、reset。 | 形成 obligation ledger |
| E2 Initial modeling | partial | 生成 v0 FCSTM：楼层/运动态 + hbrg 输出 + reset forced fallback。 | v0 使用 `! * -> F1 :: reset` |
| E3 Checks v0 | fail | SD-2/3/4 pass；SD-6 reset 场景因裸 reset 在 MU3/F2 无法解析而 fail；SD-5A 未捕获 missing forced transition。 | 进入 repair |
| E4 Repair | pass | 按可迁移事件作用域规则声明 root event reset，并改为 `! * -> F1 : /reset`；场景注入 `/reset`。 | v1 final |
| E3 Checks final | pass | SD-2/3/4/5A/SC-5F/SD-6 pass；8 条主场景全部通过。 | 无 blocking |
| E5 NFRR | pass | NFRR vector 全 3，但 single_self_assessment + no human signoff cap 到 T2；allowed_use=reviewer_queue。 | 写 nfrr_report.json |
| E6 Final audit | pass | 写 final_model/report/metadata/ledgers，并计算 SHA-256。 | 完成 |

## 5. Checks / repair / NFRR

| 检查 | 结果 | 摘要 |
|---|---|---|
| SD-2 parse | pass | 无 parse diagnostics |
| SD-3 semantic | pass | 无 semantic diagnostics |
| SD-4 design | pass | 无 blocking；`hbrg` W_UNREFERENCED_VAR 按 output-only waiver 记录 |
| SD-5A coverage | pass | M2 wrong target 与 M4 missing forced transition 均 caught；guard/effect mutation N/A 或由自定义 DMR 覆盖 |
| SC-5F freeze | pass | scenario-set-elevator-pr-m3-final, 8 scenarios |
| SD-6 sim | pass | 8/8 obligation-anchored scenarios pass；无 hot-start、无 model-derived oracle |
| SD-8/SD-10 repair | pass | reset event-scope repair resolved；no regression/drift |


NFRR 摘要：

| 字段 | 值 |
|---|---|
| evidence_mode | `NL+paper` |
| scope_type | `full_NL_fragment` |
| obligation_independence | `single_self_assessment` |
| scores | FE=3, NGF=3, REC=3, GAS=3, SCB=3, AAT=3, BVS=3, DMR=3 |
| tier_before_cap | `T3` |
| cap_reasons | `IND_SINGLE_SELF_ASSESSMENT`, `NO_HUMAN_SIGNOFF` |
| final_tier | `T2` |
| allowed_use | `reviewer_queue` |
| signed_reference | `false` |

## 6. Final FCSTM

SHA-256: `sha256:3029f80ff8b3a0b00fdacfbdc2817daae4c0e63c53d996a7ccf3225dd925f54c`

```fcstm
def int hbrg = 0;

state ElevatorController {
    event reset;
    ! * -> F1 : /reset;

    [*] -> F1;

    state F1 {
        enter { hbrg = 0; }
    }

    state F2 {
        enter { hbrg = 0; }
    }

    state F3 {
        enter { hbrg = 0; }
    }

    state MU2 {
        enter { hbrg = 1; }
    }

    state MU3 {
        enter { hbrg = 1; }
    }

    state MD1 {
        enter { hbrg = 2; }
    }

    state MD2 {
        enter { hbrg = 2; }
    }

    F1 -> MU2 :: PS2;
    F1 -> MU3 :: PS3;
    F2 -> MU3 :: PS3;
    F2 -> MD1 :: PS1;
    F3 -> MD1 :: PS1;
    F3 -> MD2 :: PS2;

    MU2 -> F2 :: S2;
    MU3 -> F3 :: S3;
    MD1 -> F1 :: S1;
    MD2 -> F2 :: S2;
}
```

## 7. Quality risks and limitations

- `hbrg` 是论文/NL 明确输出，但在 FCSTM 中不参与 guard；SD-4 的 `W_UNREFERENCED_VAR` 已按 output-only waiver 记录。下游不应把它误解为控制决策变量。
- `hbrg` 原文是位串 `00/01/10`，本模型用 int `0/1/2` 做可执行抽象；该编码已在 NFRR abstraction/waiver ledger 中说明。
- 模型覆盖给定 NL 与 paper 中明确列出的三层主链、到位、reset；不建模门传感、队列调度、按钮去抖、门开闭时间、VHDL/FPGA 时序和未给出的优先级策略。
- NFRR 为 producer 自评，没有独立 reviewer 或人工签核；因此即使证据向量达到 T3 形态，最终仍按规则 cap 到 T2，只能进入 reviewer queue，不能称为 signed reference。

## 8. Reviewer queue 判断

结论：可以进入 reviewer queue。理由是 SD-2/SD-3/SD-4 无 unwaived blocking，8 条 obligation-anchored SD-6 场景全部通过，reset 修复有 SD-8/SD-10 式 ledger，NFRR final_tier=`T2` 且 allowed_use=`reviewer_queue`。
