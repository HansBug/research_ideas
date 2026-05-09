# `light_control_nimbus/` — Nimbus Light-Control Case Study (2000)

## 论文与上游引用

- **论文**：Thompson, Whalen, Heimdahl, *Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study*, **JUCS** 6(7), 2000. [PDF](https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf)
- **配套挑战题**：[Dagstuhl Light Control System Case Study](https://www.st.cs.uni-saarland.de/edu/seminare/2005/advanced/papers/Light%20Control%20Case%20Study.pdf)
- **baselines 单篇分析**：[`../../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/`](../../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/)
- **可获取性**：🟢（两份 PDF 公开下载；案例规格在论文正文）

## 任务

经典 NL → RSML-e 层次状态机案例。**不是公开的 LLM benchmark**，而是把论文中"Light Control 参考问题 + RSML-e 状态机规格"重建为可实验片段。

## 文件清单

| 文件 | 行数 | 列数 | 内容 |
|------|------|------|------|
| [`simple.parquet`](./simple.parquet) | 4 | 6 | **格式统一表（6 列：id / input / expected / predicted / model / notes）**；本数据集 `predicted` 与 `model` 全为 None（论文非 LLM 工作） |
| [`documents.parquet`](./documents.parquet) | 2 | 8 | 两份原始文档全文（Dagstuhl 挑战题 + Nimbus JUCS 论文） |
| [`fragments.parquet`](./fragments.parquet) | 4 | 11 | 重建后的 4 个可实验 NL→RSML-e 片段 |
| [`variables.parquet`](./variables.parquet) | 17 | 7 | 17 个 monitored / controlled 变量（含 range_or_type） |
| [`states.parquet`](./states.parquet) | 20 | 7 | 20 个层次状态节点（parent_state_name + depth） |
| [`rules.parquet`](./rules.parquet) | 16 | 8 | 16 条 RSML-e 规则（target_variable + assigned_value + condition） |
| [`raw/`](./raw/) | — | — | 2 份 PDF + 2 份 txt 抽取本（已下载） |

## 关键字段

`fragments.parquet`：

- `case_id` / `fragment_id` / `fragment_title`
- `abstraction_level`（REQ / SOFT 等）
- `sample_kind`（state_hierarchy / occupancy_logic / ...）
- `input_requirement_text`（输入 NL 需求 U1-U11）
- `output_fragment_excerpt`（输出 RSML-e 状态名 / 规则）

`states.parquet` 层次结构：

- `state_name` + `parent_state_name` + `depth` —— 完整层次树
- 含 parallel region（如 `Chosen_Light_Scene` / `Failure_Modes` 都是 parallel region）

`rules.parquet`：

- `target_variable`（要赋值的变量）
- `assigned_value`（赋的值）
- `condition`（什么条件下赋值）

## 真实样本（一条）

`room_state_hierarchy_req` 片段：

```
INPUT (input_requirement_text):
  U1: If a person occupies a room, the light has to be sufficient to move safely,
      if nothing else is desired by a chosen light scene.
  U3: If the room is reoccupied within T1 minutes after the last person has left
      the room, the last chosen light scene has to be reestablished.
  U4: If the room is reoccupied after more than T1 minutes since the last person
      has left, the standard light scene has to be established.
  ...

OUTPUT (output_fragment_excerpt 层次状态名):
  Light_Control_System_Room
    ├── Light_Maintenance_Modes (Room_Occupied / Room_Empty / Occupancy_Undetectable)
    ├── Chosen_Light_Scene (parallel: Chosen1_LS / Chosen2_LS / ... / Default_LS)
    └── Failure_Modes (parallel: Ok / Failed)
```

注意 U3/U4 中的 `T1 minutes` —— 控制系统**时间约束**的经典 case。

## 原始资源现状（✅ 已下载）

`raw/` 已包含 4 份资源：

- `light-case-jucs.pdf` + `light-case-jucs.txt` —— Nimbus JUCS 论文（PDF + 抽取文本）
- `Light_Control_Case_Study.pdf` + `light-control-original-case-study.txt` —— Dagstuhl 挑战题（来自 [Semantic Scholar synopsis](https://pdfs.semanticscholar.org/3a2f/1fb69fa1fa109e9a25343c379a81cb3744f2.pdf) 的 4 页 synopsis；原始 1992 年 Dagstuhl 链接 `rn.informatik.uni-kl.de/~recs` 已失效）

parquet 中所有路径字段已迁移到本目录的相对路径（`./raw/...`），可逐字段验证存在。

## 复用性建议

- ❌ **不是公开评分数据集**：0 行人评，仅 2 文档原文 + 4 重建片段
- ✅ **最适合做 V&V 流程参考**：人工 inspection / formal verification / simulation 三联流程的方法学样本
- ✅ **HSM + 时间约束**经典样本：U3/U4 的 `T1 分钟`、平行区域、故障模式都是控制系统建模的常见诉求
- ⚠️ 输入是已被论文重建的 NL 片段，不是开放原文需求；做对比时记得它本质是"案例改写后的样本"
