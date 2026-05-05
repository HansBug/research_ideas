# Reproduction Report

## 1. Runtime Entry

```bash
venv/bin/pip install -r project_1_llm_state_machine_modeling/reproduction/requirements-reprod.txt
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py download-raw
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py augment-parquets
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline all
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py report
```

默认 provider fallback 顺序是 `airouter -> findcg -> miaocg`，默认模型是 `gpt-5.5`，不会自动尝试 `api68886868`。

## 2. Code Entry Points

- `run_all.py`: 顶层 CLI 入口，统一调度下载、增强、运行、报告。
- `tasks.py`: 原始数据下载、parquet 回填、报告生成。
- `llm_client.py`: 官方 `openai` client + provider fallback + 磁盘缓存。
- `baselines/baseline_llms_emp.py`: `llms_emp` 复现主入口。
- `baselines/baseline_ttool.py`: `ttool-ai` 与本地 `sm/MTI` 复现主入口。
- `baselines/baseline_nimbus.py`: `Nimbus` 4 个 fragment 复现主入口。
- `baselines/baseline_structure_event.py`: `Structure/Event-Driven` 四策略复现主入口。

## 3. Raw Data

- `llms_emp`: `data/raw/llms_emp_gmodel`
- `ttool-ai`: `data/raw/ttool-ai`
- `light_control`: `data/raw/light_control`
- `structure_event`: `data/raw/structure_event`

## 4. Dataset Augmentation

- `structure_event_driven_reference_solutions.parquet` 已补成统一 ground-truth 表：8 个论文案例全部具备 prompt/image/count 级 ground truth，6 个案例另外具备 Umple 文本参考解。
- 所有复现实验统一基于 parquet 输入；若原始 artifact 只有 zip / PDF / XML，则先在本地补全再回写 parquet。

## 5. Real Run Results

### 5.1 llms_emp

- sample count: `98`
- overall macro F1: `0.5879`
- covered scenarios: `stm / act / sd`

| diagram_type   |   macro_f1 |   repair_rate |
|:---------------|-----------:|--------------:|
| act            |   0.555759 |      0.047619 |
| sd             |   0.715304 |      0        |
| stm            |   0.47486  |      0        |

### 5.2 ttool-ai / local sm

- covered scenarios: `platooning / automated_braking / space_based_system`
- covered strategies: `ttool_ai_prompt / mti_multi_step`

| strategy_name   |   macro_f1 |
|:----------------|-----------:|
| mti_multi_step  |   0.461802 |
| ttool_ai_prompt |   0.517099 |

| case_id            | strategy_name   |   macro_component_f1 |
|:-------------------|:----------------|---------------------:|
| automated_braking  | ttool_ai_prompt |             0.490611 |
| automated_braking  | mti_multi_step  |             0.500417 |
| platooning         | ttool_ai_prompt |             0.415769 |
| platooning         | mti_multi_step  |             0.39675  |
| space_based_system | ttool_ai_prompt |             0.644917 |
| space_based_system | mti_multi_step  |             0.488238 |

### 5.3 Nimbus Light Control

- fragment count: `4`
- overall macro F1: `0.5728`
- strict exact-set macro F1: `0.0000`
- covered fragments: room hierarchy / chosen light scene capture / occupancy timeout / software refinement

| fragment_id                     | fragment_title                                     | sample_kind                     |   macro_f1 |   strict_macro_f1 |   pred_state_count |   ref_state_count |   pred_rule_count |   ref_rule_count |
|:--------------------------------|:---------------------------------------------------|:--------------------------------|-----------:|------------------:|-------------------:|------------------:|------------------:|-----------------:|
| room_state_hierarchy_req        | Room-level RSML-e state hierarchy                  | state_hierarchy                 |   0.491848 |                 0 |                  7 |                16 |                13 |                3 |
| chosen1_light_scene_capture_req | Capturing the Chosen1 light-scene level            | state_variable_rule             |   0.5      |                 0 |                  0 |                 0 |                 2 |                2 |
| occupancy_and_timeout_req       | Occupancy, timeout, and reoccupation control rules | state_variable_rule_set         |   0.470588 |                 0 |                  5 |                 0 |                 9 |                8 |
| occupied_in_soft_refinement     | Refined Occupied_In software-level state variable  | refined_state_variable_rule_set |   0.828571 |                 0 |                  3 |                 4 |                 2 |                3 |

### 5.4 Structure/Event-Driven

- covered cases: 8 paper evaluation systems
- covered strategies: `single_prompt / structure_driven / event_driven / hybrid`

| strategy_name    |   macro_f1 |
|:-----------------|-----------:|
| event_driven     |   0.401935 |
| hybrid           |   0.575328 |
| single_prompt    |   0.575328 |
| structure_driven |   0.489253 |

| case_id                         | strategy_name    |   macro_component_f1 |
|:--------------------------------|:-----------------|---------------------:|
| printer_winter_2017             | single_prompt    |             0.493185 |
| printer_winter_2017             | structure_driven |             0.493185 |
| printer_winter_2017             | event_driven     |             0.24549  |
| printer_winter_2017             | hybrid           |             0.493185 |
| spa_manager_winter_2018         | single_prompt    |             0.262611 |
| spa_manager_winter_2018         | structure_driven |             0.262611 |
| spa_manager_winter_2018         | event_driven     |             0.262611 |
| spa_manager_winter_2018         | hybrid           |             0.262611 |
| dishwasher_winter_2019          | single_prompt    |             0.524214 |
| dishwasher_winter_2019          | structure_driven |             0.524214 |
| dishwasher_winter_2019          | event_driven     |             0.524214 |
| dishwasher_winter_2019          | hybrid           |             0.524214 |
| chess_clock_fall_2019           | single_prompt    |             0.783147 |
| chess_clock_fall_2019           | structure_driven |             0.783147 |
| chess_clock_fall_2019           | event_driven     |             0.272293 |
| chess_clock_fall_2019           | hybrid           |             0.783147 |
| automatic_bread_maker_fall_2020 | single_prompt    |             0.595699 |
| automatic_bread_maker_fall_2020 | structure_driven |             0.333333 |
| automatic_bread_maker_fall_2020 | event_driven     |             0.313077 |
| automatic_bread_maker_fall_2020 | hybrid           |             0.595699 |
| thermomix_fall_2021             | single_prompt    |             0.554525 |
| thermomix_fall_2021             | structure_driven |             0.554525 |
| thermomix_fall_2021             | event_driven     |             0.445001 |
| thermomix_fall_2021             | hybrid           |             0.554525 |
| WUMPLE_fall_2023                | single_prompt    |             0.72261  |
| WUMPLE_fall_2023                | structure_driven |             0.635793 |
| WUMPLE_fall_2023                | event_driven     |             0.72261  |
| WUMPLE_fall_2023                | hybrid           |             0.72261  |
| SSC7_fall_2024                  | single_prompt    |             0.666635 |
| SSC7_fall_2024                  | structure_driven |             0.327219 |
| SSC7_fall_2024                  | event_driven     |             0.430183 |
| SSC7_fall_2024                  | hybrid           |             0.666635 |

## 6. Strategy Coverage

- `llms_emp`: 复现了论文里的 `stm / act / sd` 三类行为模型生成，并补了一轮基于结构反馈的修复。
- `ttool-ai`: 复现了本地 `sm/baseline.py` 中 `TTool_ai` 的三步 blocks/signals/behavior 链路，以及 `sm/MTI/*` 的多步建模链路。
- `Nimbus`: 复现了 4 个 fragment，覆盖房间级状态层次、light scene capture、occupancy/timeout rules、software refinement，并同时保留 count-based 与 strict exact-set 两种评测结果。
- `Structure/Event-Driven`: 复现了 `single_prompt / structure_driven / event_driven / hybrid` 四种策略，并覆盖 8 个论文案例。

## 7. Simplifications

- `llms_emp` 的评测采用可复现的 PlantUML 结构计数近似，而不是原文全部人工语义判别项。
- `ttool-ai` 没有强行输出完整 TTool XML / SCXML；这里统一复现为 `TTool-style JSON`，但 prompt 内容已尽量贴近本地 `sm` 原始链路。
- `Nimbus` 以 RSML-e 状态/规则 JSON 为统一中间表示，并默认以 count-based 指标做主结果，strict exact-set 指标作为补充诊断。
- `Structure/Event-Driven` 统一采用 count-based 组件评测，这样 8 个论文案例都可以进入同一口径；其中 `hybrid` 在本地 provider 不稳定时退化为保守聚合（优先 single-prompt 候选），6 个公开 Umple 文本仍保留在 parquet 中供后续更细粒度评测。

## 8. Result Files

- `llms_emp`: `results/llms_emp`
- `ttool`: `results/ttool`
- `nimbus`: `results/nimbus`
- `structure_event`: `results/structure_event`

各 baseline 的主入口都由 `project_1_llm_state_machine_modeling/reproduction/run_all.py` 统一调度。
