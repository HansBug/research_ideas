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
| [`documents.parquet`](./documents.parquet) | 2 | 8 | 两份原始文档全文（Dagstuhl 挑战题 + Nimbus JUCS 论文） |
| [`fragments.parquet`](./fragments.parquet) | 4 | 11 | 重建后的 4 个可实验 NL→RSML-e 片段 |
| [`variables.parquet`](./variables.parquet) | 17 | 7 | 17 个 monitored / controlled 变量（含 range_or_type） |
| [`states.parquet`](./states.parquet) | 20 | 7 | 20 个层次状态节点（parent_state_name + depth） |
| [`rules.parquet`](./rules.parquet) | 16 | 8 | 16 条 RSML-e 规则（target_variable + assigned_value + condition） |
| [`raw/`](./raw/) | — | — | 两份原始 PDF（**当前为空**，详见 §`原始资源现状`） |

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

## 原始资源现状（⚠️ P0 待补）

build 脚本读取的原始资源：

- `raw/light-control-original-case-study.txt` —— Dagstuhl 挑战题 PDF 提取的纯文本
- `raw/light-case-jucs.txt` —— Nimbus 论文 PDF 提取的纯文本

**两份 PDF 在外部链接均可重新下载**：

```bash
# 在本目录的 raw/ 下放：
wget -O raw/Light\ Control\ Case\ Study.pdf \
    "https://www.st.cs.uni-saarland.de/edu/seminare/2005/advanced/papers/Light%20Control%20Case%20Study.pdf"
wget -O raw/light-case-jucs.pdf \
    "https://www-users.cse.umn.edu/~heimdahl/csci8801-fall06/readings/light-case-jucs.pdf"
# 然后用 pdf_extractor 转 txt（或者直接复用 baselines/...nimbus-light-control/paper_content.txt）
```

> 提示：JUCS 论文 PDF 实际就是 [`../../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/paper.pdf`](../../../baselines/requirements-capture-and-evaluation-in-nimbus-light-control/paper.pdf) 的副本，可直接 cp 过来。

## 复用性建议

- ❌ **不是公开评分数据集**：0 行人评，仅 2 文档原文 + 4 重建片段
- ✅ **最适合做 V&V 流程参考**：人工 inspection / formal verification / simulation 三联流程的方法学样本
- ✅ **HSM + 时间约束**经典样本：U3/U4 的 `T1 分钟`、平行区域、故障模式都是控制系统建模的常见诉求
- ⚠️ 输入是已被论文重建的 NL 片段，不是开放原文需求；做对比时记得它本质是"案例改写后的样本"
