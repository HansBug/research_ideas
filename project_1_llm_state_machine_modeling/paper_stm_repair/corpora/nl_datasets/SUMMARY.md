# nl_datasets/SUMMARY.md

## 0. 当前结论

本目录当前处于 **初始化脚手架阶段**：已冻结 NL-datasets 的边界、入口和字段纪律，但尚未开展大规模外部检索或逐篇入账。

## 1. 三类文库中的角色

| 文库 | 角色 |
|---|---|
| seed_library | 上游 `NL -> STM_0` seed 方法 / 来源 |
| repair_baselines | `STM_0 -> STM_k / Better STM` 修正近邻 |
| nl_datasets | 控制系统纯 NL 输入来源 |

## 2. 当前应保留的字段组

| 字段组 | 用途 |
|---|---|
| `dataset_id` | 稳定条目标识 |
| NL 类型 | 需求 / 用例 / 场景 / 系统描述 / 标准片段 / 教学文本 |
| 控制系统领域 | 电梯、雷达、Microwave 等 |
| 规模 | 文本数 / 需求数 / 样例规模 |
| 公开与许可 | 是否公开、是否可复用、引用要求 |
| seed 构造潜力 | 弱模型、弱 prompt、学生人工建模 |
| 与已有 STM 关系 | 是否已有 STM，是否能证明由 NL 生成 |
| 实验角色 | 主来源、fallback、教学 seed、负例 |
| 证据指针 | 论文、repo、dataset card、页面链接 |

## 3. 当前已知来源入口（待后续逐步填充）

- `project_1_llm_state_machine_modeling/sources/`
- `project_1_llm_state_machine_modeling/data/`
- `project_1_llm_state_machine_modeling/paper_v1/`

## 4. 后续工作边界

- 先基于已有 sources/data 搭建 NL-datasets 入口，不做大规模外部检索。
- 只有 NL 不等于 seed；需要明确 `STM_0` 生成关系后才 crosslink。
- 后续如果确有新数据源，再逐条补充 summary 与单条目目录。
