# 高层驾驶模块人工 FCSTM identity pilot

## 1. 定位

本目录复用正式 selected seed `llms_emp_feedback_final_0000` 的原始 NL 与最终
PlantUML source pair metadata，但使用一份逐项记录人工裁决的 FCSTM，专门解除
`PR-discover` 的工程 smoke 阻塞。它已经与正式 60 例选择池隔离，只能通过
`discover-custom` 作为工程 fixture 使用，不覆盖正式 0000，也不替代 PlantUML ->
FCSTM 系统转换器的修复。

Discover pair id 固定为：

```text
llms_emp_stm_results_0000_manual_identity
```

## 2. 文件

| 文件 | 说明 |
| --- | --- |
| [nl.txt](./nl.txt) | 与正牌 `0000` 字节一致的原始需求。 |
| [stm0.puml](./stm0.puml) | 与正式 selected seed `llms_emp_feedback_final_0000` 字节一致的 feedback-final PlantUML；hash 必须为 `4fe07b05bdcfaac1c961d1176fb099d8240818160caa6edfb57928c6be2efc8a`。 |
| [phase_i_generation_provenance.puml](./phase_i_generation_provenance.puml) | 人工 FCSTM authoring 实际参考过的 phase-I Generation PlantUML derivation provenance；hash 为 `8fd2f71b338836488e2e29fe19c4e58c4992d4186367f43efc121fae6c36db7f`，不作为 loaded source pair。 |
| [STM_0.fcstm](./STM_0.fcstm) | 人工 canonicalization 后的可执行 FCSTM。 |
| [DECISIONS.md](./DECISIONS.md) | 每个作用域、event、completion 与 source-preservation 裁决的理由和限制。 |
| [source_meta.json](./source_meta.json) | 原始 pair 身份、hash 与 Discover alias。 |
| [fcstm_meta.json](./fcstm_meta.json) | 人工制品身份、输入策略、pyfcstm 身份和学术不适格声明。 |
| [verification/](./verification/) | distance event、brake、steering、completion、power-off 五个 FBMCQ 回归查询。 |

## 3. Discover 输入语义

该 fixture 不进入默认 pair registry。`make discover-demo` 使用现有 custom CLI，
把 [STM_0.fcstm](./STM_0.fcstm) 同时作为 source identity 与 intermediate model：

```text
discover_source_policy = fcstm_identity
```

因此一次运行冻结的输入为：

```text
NL             = llms_emp_feedback_final_0000 NL
raw/source     = STM_0.fcstm
intermediate   = STM_0.fcstm
relation       = exact_identity
source PUML    = stm0.puml，即 llms_emp_feedback_final_0000 selected feedback-final PlantUML
derivation PUML= phase_i_generation_provenance.puml，仅记录人工 authoring provenance
```

这样可以继续验证 Discover Agent 的 guide、tool、scenario/property、structured
submission 与 append-only record 链，同时确定性排除 PlantUML lowering difference
成为 candidate issue。代价是本 pilot 不能回答“是否发现了原始 PlantUML 的问题”。

注意：`source_meta.json` 中的 source pair、locator、selected stage 与 `stm0_sha256`
必须跟正式 selected seed `llms_emp_feedback_final_0000` 保持一致；`8fd2...` 只允许
出现在 phase-I derivation provenance 字段/文件中，不能再被同一路径 `stm0.puml` 声称。

## 4. 运行

仓库根 Makefile 已将该 fixture 设为真实 demo 默认值。正式 `discover-pair` 默认值仍是
`llms_emp_feedback_final_0000`，二者不会在 selected 目录中争用同一 pair ID。真实运行前
仍须遵守 `.env` 规则：

```bash
source .env
make discover-demo DISCOVER_OUT=runs/paper1/discover/manual-0000-identity
```

也可以显式指定同一现有 CLI：

```bash
make discover-custom \
  DISCOVER_CASE=llms_emp_stm_results_0000_manual_identity \
  DISCOVER_NL=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/fixtures/discover_integrated/0000_hldcs_manual_identity/nl.txt \
  DISCOVER_FCSTM=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/fixtures/discover_integrated/0000_hldcs_manual_identity/STM_0.fcstm \
  DISCOVER_OUT=runs/paper1/discover/manual-0000-identity
```

## 5. 验证结果与剩余边界

当前 `STM_0.fcstm` 已通过 parse、semantic validation 与 inspect，并完成以下运行检查：

1. `PowerOn`：`PoweredOff -> HumanDriving`。
2. `Front Distance > 10` event：`HumanDriving -> Autonomous.AutoInitial`。
3. `BrakePressed` / `HumanSteeringCommand`：从 autonomous 任意 active child 返回 `HumanDriving`。
4. `ExitAutonomous`：`AutoInitial -> AutoFinal -> HumanDriving`。
5. `PowerOff`：从 `HumanDriving` 进入 terminated boundary。

`Front Distance > 10` 按正式 selected seed PlantUML / 官方 SCXML 口径保留为 named event。
A 阶段不利用 NL 将其重构为变量或 guard；这种 condition-like label 的表达债只可
作为 Discover 的候选触发信号，不能自动升级为 source-level confirmed issue。

## 6. 学术边界

本目录和由它产生的运行一律满足：

- `academic_eligible=false`；
- 不支撑 PlantUML conversion fidelity claim；
- 不支撑 raw/source issue-discovery effectiveness claim；
- 不支撑 repair gain；
- 只支撑 `PR-discover` 的工程连通性、工具协议和运行记录检查。
