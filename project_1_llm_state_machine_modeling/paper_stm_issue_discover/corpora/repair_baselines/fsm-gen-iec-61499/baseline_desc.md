# LLM-based iterative requirements refinement in FSM with IEC 61499 code generation — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `fsm-gen-iec-61499` |
| 标题 | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation |
| 年份 / venue | 2025 / IEEE INDIN |
| 当前角色 | 仿真/用户 refinement 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 控制系统 NL 需求 + I/O 接口 + 用户后续自然语言 refinement request |
| 模型 / STM 输出 | FSM / IEC 61499 Function Block / ECC |
| 修正 / 补全 / refinement 方法 | LLM 生成初始 FSM，用户视觉检查并给 correction/refinement，内置解释器连接 EAE 闭环仿真验证行为 |
| feedback 来源 | 用户自然语言反馈、视觉检查、闭环仿真反馈、部署/测试观察 |
| 自动化程度 | 半自动；问题识别和满意度判断依赖人 |
| LLM / agent 角色 | 核心生成/修改器；具体模型未明确 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

工业控制强近邻，说明 simulation/user feedback refinement 的现实需求；不应写成无人自动 repair baseline。

## 4. 证据位置

`paper_content.txt` 摘要、工作流、用户 correction + simulation、案例 refinement、未来形式化验证；旁路核验材料复核。

## 5. 主要风险与使用边界

少量案例、无定量 benchmark；无公开代码/数据；simulation feedback 未结构化为 machine-readable diagnostics。
