# PR-M3 Codex Exec Skill 实验报告：path2_lng_ems

## 0. Run identity

| 字段 | 值 |
|---|---|
| run_label | `pr_m3_four_20260608_122318` |
| case_key | `path2_lng_ems` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| Path | `path2` |
| 输出目录 | `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems` |
| 状态 | `success / reviewer_queue candidate` |
| provider config | 仅见非敏感默认标签 `model_provider=airouter`；未读取 `.env`，未输出 key/endpoint/token |
| forbidden runner | 未调用 `method.loop.run_agent_loop(...)`、PR-D runner、PR-E1 runner 或一键 full staged runner |

## 1. 输入

NL source: `https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890799`

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

中文释义：

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

paper_dir: `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`

## 2. 实际读取文件

| 类型 | 路径 | 用途 |
|---|---|---|
| skill | `project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md` -> `AGENT_LOOP_SKILL.md` | skill 入口与禁止边界 |
| guide | `e2e_ref_model_guide.md`, `tools.md`, `prompts.md`, `nfrr_evaluation_guide.md`, `codex_exec_experiment_guide.md` | E0-E6 流程、工具、NFRR 和产物规范 |
| paper | `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/bibtex.bib` | 论文元信息 |
| paper | `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/STM.md`, `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/DESC.md` | 人工整理的状态机索引与阅读指南 |
| paper | `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper_content.txt` lines 420-500, 520-650 | Table 1/2/3：输入、输出、12 状态、状态条件和动作 |
| grammar/tool | `_pyfcstm_grammar.md`, `method/stages/api.py`, `sd_tools.py`, `schema.py`, stage tests | 当前 parser/runtime/API 约束 |

完整清单见 `actual_file_reads.json`。

## 3. 过程摘要

| 阶段 | 结果 | 摘要 |
|---|---|---|
| E0 Skill discovery | 通过 | 读取 SKILL.md 软链接及 5 份必读指南；确认禁止顶层 runner。 |
| E1 Evidence grounding | 通过 | 读取 bibtex/STM/DESC/paper_content；Table 1/2/3 支撑输入、输出、12 状态和 illegal state。 |
| E2 Initial modeling | 通过 | 构造 table-driven EFSM：Root.Select 根据外部输入守卫选择 12 个状态。 |
| E3 Deterministic checks | 通过 | SD-2/3/4 pass；SD-5A ok；SD-6 12/12 pass。 |
| E4 Repair/waiver | 通过 | 修正一个场景 oracle；删除冗余 synthetic command flags；记录 external-input/output-only waivers。 |
| E5 NFRR | 通过 | NFRR v3 final_tier=T2，allowed_use=reviewer_queue。 |
| E6 Final audit | 通过 | forbidden_runner_used=false；redaction pass；hash 已写入 metadata。 |


## 4. 检查 / 修复 / NFRR 摘要

| 项 | 结果 | 说明 |
|---|---|---|
| SD-2 parse | pass | 当前 DSL 语法通过 |
| SD-3 semantic | pass | build ok，无 undefined var / dangling transition |
| SD-4 design | pass | 无 blocking；external-input/output-only/large-composite 均为 advisory/waiver |
| SD-5A coverage | pass | coverage_gap=false |
| SC-5F freeze | pass | scenario_set_id `scenario-set-ee12cd43ee53`，12 个场景冻结 |
| SD-6 sim | pass | 12/12 场景通过，oracle_weak=false |
| mutation checks | pass | 5 个定向 mutant 全部被场景抓住 |
| repair | pass | 修正一个场景 oracle，并删除冗余 synthetic command flag |
| NFRR | T2 | FE=3, NGF=3, REC=3, GAS=2, SCB=3, AAT=3, BVS=2, DMR=2 |
| allowed_use | reviewer_queue | NL+paper + T2 -> AU-3 |

关键 waiver：

| warning | 处理 | 依据 |
|---|---|---|
| `W_UNWRITTEN_READ_VAR` / `W_GUARD_VARS_NEVER_CHANGE` | 接受为 external input advisory | NL 和 Table 1 明确 `PL/Ppv/Pw/SoC/eng*_Pmax` 是控制器读取的外部输入/容量边界 |
| `W_UNREFERENCED_VAR` / output-only | 接受为输出变量 advisory | Table 2 和 NL 明确 `Pgr/Pd1r/Pd2r/Pbr/Pbc/Ps/EMS_State` 是返回/命令量 |
| `W_LARGE_COMPOSITE` | 接受为表驱动 EFSM 抽象 | 论文 Table 3 本身给出 12 个同级有限状态 |

## 5. Final FCSTM

sha256: `c91fcc5861ba5c8f9a08aa4dbc5630acd045e23ff4f1c376cff07b26ea9bade8`

```fcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float eng1_Pmax = 0.0;
def float eng2_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def int ems_state = 0;
def float Pgr = 0.0;
def float Pd1r = 0.0;
def float Pd2r = 0.0;
def float Pbr = 0.0;
def float Pbc = 0.0;
def float Ps = 0.0;
state Root {
    event SampleInputs;
    pseudo state Select;
    state State1_1;
    state State1_2;
    state State2_1;
    state State2_2;
    state State2_3;
    state State2_4;
    state State2_5;
    state State2_6;
    state State2_7;
    state State3_1;
    state State3_2;
    state State3_3;
    [*] -> Select;
    Select -> State1_1 : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95] effect { ems_state = 11; Pgr = 0.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = 0.0; Pbc = Ppv + Pw - PL; Ps = 0.0; };
    Select -> State1_2 : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95] effect { ems_state = 12; Pgr = 0.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = 0.0; Pbc = 0.0; Ps = Ppv + Pw - PL; };
    Select -> State2_1 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax > PL - Ppv - Pw && SoC > 0.5] effect { ems_state = 21; Pgr = 0.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = PL - Ppv - Pw; Pbc = 0.0; Ps = 0.0; };
    Select -> State2_2 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax > PL - Ppv - Pw && SoC <= 0.5] effect { ems_state = 22; Pgr = PL - Ppv - Pw + eng3_Pmax / 5.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = 0.0; Pbc = eng3_Pmax / 5.0; Ps = 0.0; };
    Select -> State2_3 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng3_Pmax > PL - Ppv - Pw && SoC > 0.5] effect { ems_state = 23; Pgr = eng3_Pmax; Pd1r = 0.0; Pd2r = 0.0; Pbr = PL - Ppv - Pw - eng3_Pmax; Pbc = 0.0; Ps = 0.0; };
    Select -> State2_4 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng3_Pmax > PL - Ppv - Pw && SoC <= 0.5] effect { ems_state = 24; Pgr = eng3_Pmax; Pd1r = PL - Ppv - Pw - eng3_Pmax + eng1_Pmax / 10.0; Pd2r = 0.0; Pbr = 0.0; Pbc = eng1_Pmax / 10.0; Ps = 0.0; };
    Select -> State2_5 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng2_Pmax + eng3_Pmax > PL - Ppv - Pw && SoC > 0.5] effect { ems_state = 25; Pgr = eng3_Pmax; Pd1r = eng1_Pmax; Pd2r = 0.0; Pbr = PL - Ppv - Pw - eng3_Pmax - eng1_Pmax; Pbc = 0.0; Ps = 0.0; };
    Select -> State2_6 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng2_Pmax + eng3_Pmax > PL - Ppv - Pw && SoC <= 0.5] effect { ems_state = 26; Pgr = eng3_Pmax; Pd1r = eng1_Pmax; Pd2r = PL - Ppv - Pw - eng3_Pmax - eng1_Pmax + eng1_Pmax / 10.0; Pbr = 0.0; Pbc = eng1_Pmax / 10.0; Ps = 0.0; };
    Select -> State2_7 : if [PL > 0.0 && Ppv + Pw < PL && eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng3_Pmax < PL - Ppv - Pw && eng1_Pmax + eng2_Pmax + eng3_Pmax <= PL - Ppv - Pw] effect { ems_state = 27; Pgr = eng3_Pmax; Pd1r = eng1_Pmax; Pd2r = eng2_Pmax; Pbr = PL - Ppv - Pw - eng3_Pmax - eng1_Pmax - eng2_Pmax; Pbc = 0.0; Ps = 0.0; };
    Select -> State3_1 : if [PL == 0.0 && SoC < 0.5] effect { ems_state = 31; Pgr = 0.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = 0.0; Pbc = Ppv + Pw; Ps = 0.0; };
    Select -> State3_2 : if [PL == 0.0 && SoC >= 0.5 && SoC < 0.95] effect { ems_state = 32; Pgr = 0.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = 0.0; Pbc = Ppv; Ps = Pw; };
    Select -> State3_3 : if [PL == 0.0 && SoC >= 0.95] effect { ems_state = 33; Pgr = 0.0; Pd1r = 0.0; Pd2r = 0.0; Pbr = 0.0; Pbc = 0.0; Ps = Ppv + Pw; };
    State1_1 -> Select : SampleInputs;
    State1_2 -> Select : SampleInputs;
    State2_1 -> Select : SampleInputs;
    State2_2 -> Select : SampleInputs;
    State2_3 -> Select : SampleInputs;
    State2_4 -> Select : SampleInputs;
    State2_5 -> Select : SampleInputs;
    State2_6 -> Select : SampleInputs;
    State2_7 -> Select : SampleInputs;
    State3_1 -> Select : SampleInputs;
    State3_2 -> Select : SampleInputs;
    State3_3 -> Select : SampleInputs;
}
```

## 6. 质量风险和限制

1. 这是 single self-assessment，尚无独立 reviewer/human signoff，因此 NFRR 被限制在 T2，不能称 signed reference。
2. `PL/Ppv/Pw/SoC/eng*_Pmax` 被建模为外部输入；SD-6 场景通过 `initial_vars` 注入这些值。当前 runtime 未做 step-level 外部输入刷新，所以动态再采样只由 `SampleInputs` 结构表达，未作为强 BVS 主证据充分仿真。
3. `State3_2` 的提取文本中存在“Battery charges using Pw”和正文描述“PV charging, wind spare”的轻微张力；本模型采用 paper_content 中 Table 3 描述段的 PV charging / wind spare 解释，并在 NFRR alignment 中标为 abstract/risk。
4. 模型保留状态表逻辑和功率请求骨架，不覆盖论文中的连续发电机效率、燃料、稳定性分析或低层物理方程。
5. `ems_state` 是 Table 2 的 `EMS_State` 离散编码，用于审计/场景断言；不是额外控制输入。

## 7. Reviewer queue 结论

可以进入 reviewer queue。理由：SD-2/3/4 通过，无 unwaived blocking；12 个 obligation-anchored 场景全部通过；5 个定向 mutant 全部被抓住；NFRR final_tier=`T2`，allowed_use=`reviewer_queue`。进入 reviewer 后仍需人工确认 Table 3 边界等号、`State3_2` PV/WEC 分配解释，以及动态再采样是否需要更强场景 runtime 支持。
