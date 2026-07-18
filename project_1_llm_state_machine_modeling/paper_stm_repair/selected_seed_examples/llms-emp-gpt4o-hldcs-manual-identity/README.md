# 高层驾驶模块人工 FCSTM identity pilot

## 1. 定位

本目录复用正牌 `0000` 的原始 NL 与 PlantUML，但使用一份逐项记录人工裁决的
FCSTM，专门解除 `PR-discover` 的工程 smoke 阻塞。它与
[正牌 0000 自动转换快照](../llms-emp-gpt4o-hldcs/README.md) 并列保存，不覆盖原目录，
也不替代 PlantUML -> FCSTM 系统转换器的修复。

Discover pair id 固定为：

```text
llms_emp_stm_results_0000_manual_identity
```

## 2. 文件

| 文件 | 说明 |
| --- | --- |
| [nl.txt](./nl.txt) | 与正牌 `0000` 字节一致的原始需求。 |
| [stm0.puml](./stm0.puml) | 与正牌 `0000` 字节一致的原始 PlantUML，只保留作 provenance，不送入本 pilot 的 Discover source 槽位。 |
| [model.fcstm](./model.fcstm) | 人工 canonicalization 后的可执行 FCSTM。 |
| [DECISIONS.md](./DECISIONS.md) | 每个作用域、event、completion 与 source-preservation 裁决的理由和限制。 |
| [source_meta.json](./source_meta.json) | 原始 pair 身份、hash 与 Discover alias。 |
| [fcstm_meta.json](./fcstm_meta.json) | 人工制品身份、输入策略、pyfcstm 身份和学术不适格声明。 |
| [verification/](./verification/) | distance event、brake、steering、completion、power-off 五个 FBMCQ 回归查询。 |

## 3. Discover 输入语义

`load_pair("llms_emp_stm_results_0000_manual_identity")` 仍使用现有 pair CLI 协议，
但读取 `fcstm_meta.json` 中的：

```text
discover_source_policy = fcstm_identity
```

因此一次运行冻结的输入为：

```text
NL             = 原始 0000 NL
raw/source     = model.fcstm
intermediate   = model.fcstm
relation       = exact_identity
original PUML  = 仅在本目录保留，不进入 Agent 上下文
```

这样可以继续验证 Discover Agent 的 guide、tool、scenario/property、structured
submission 与 append-only record 链，同时确定性排除 PlantUML lowering difference
成为 candidate issue。代价是本 pilot 不能回答“是否发现了原始 PlantUML 的问题”。

## 4. 运行

仓库根 Makefile 已将该 pair 设为默认值。真实运行前仍须遵守 `.env` 规则：

```bash
source .env
make discover-demo DISCOVER_OUT=runs/paper1/discover/manual-0000-identity
```

也可以显式指定同一现有 CLI：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src:project_1_llm_state_machine_modeling:$PWD \
python -m paper_stm_repair_loop.discover \
  --pair-id llms_emp_stm_results_0000_manual_identity \
  --profile gpt-5.5 \
  --content-language zh-CN \
  --renderer rich \
  --output-dir runs/paper1/discover/manual-0000-identity
```

## 5. 验证结果与剩余边界

当前 `model.fcstm` 已通过 parse、semantic validation 与 inspect，并完成以下运行检查：

1. `PowerOn`：`PoweredOff -> HumanDriving`。
2. `Front Distance > 10` event：`HumanDriving -> Autonomous.AutoInitial`。
3. `BrakePressed` / `HumanSteeringCommand`：从 autonomous 任意 active child 返回 `HumanDriving`。
4. `ExitAutonomous`：`AutoInitial -> AutoFinal -> HumanDriving`。
5. `PowerOff`：从 `HumanDriving` 进入 terminated boundary。

`Front Distance > 10` 按原始 PlantUML / 官方 SCXML 口径保留为 named event。
A 阶段不利用 NL 将其重构为变量或 guard；这种 condition-like label 的表达债只可
作为 Discover 的候选触发信号，不能自动升级为 source-level confirmed issue。

## 6. 学术边界

本目录和由它产生的运行一律满足：

- `academic_eligible=false`；
- 不支撑 PlantUML conversion fidelity claim；
- 不支撑 raw/source issue-discovery effectiveness claim；
- 不支撑 repair gain；
- 只支撑 `PR-discover` 的工程连通性、工具协议和运行记录检查。
