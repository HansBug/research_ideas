# research questions（R0 草案）

## 1. 说明

本文件给出第一篇论文的 RQ 草案。R0 只冻结问题结构和证据需求；最终 RQ、指标、阈值和统计表由 PR-R4 / PR-R6 在真实运行前冻结。

## 2. RQ 表

| RQ | 问题 | 需要的证据 | 依赖 PR | 降级写法 |
|---|---|---|---|---|
| RQ1 | 初始 `STM_0` 的主要缺陷类型是什么？ | parse / semantic / guard / action / hierarchy / behavior 缺陷统计。 | R1 / R2 / R4 | 若样本少，写成 pilot characterization。 |
| RQ2a | 不同 feedback source 能发现哪些结构、语义或行为问题？ | diagnostics 类型、feedback source、未闭合缺陷。 | R4 | 若覆盖有限，写成 feedback coverage 分析。 |
| RQ2b | feedback 输入修正循环后，哪些缺陷能被关闭，哪些会引入回归或振荡？ | 修复前后诊断、rejected repair、rollback、oscillation、non-convergence。 | R5 / R6 | 若不稳定，重点报告失败模式。 |
| RQ3 | 场景 / 仿真反馈是否发现静态检查难以发现的行为缺陷？ | scenario pass/fail、trace mismatch、simulation-only defects。 | R4 / R6 | 若证据弱，写为补充反馈来源。 |
| RQ4 | 自动修正是否产生相对更优 STM？ | 五条件逐项台账、`STM_0` vs `STM_k`、人工裁决、回归检查。 | R4 / R6 | 任一条件失败，不计入 Better STM，只报告失败 / 局限。 |
| RQ5 | seed 来源如何影响修正效果？ | prior artifact、弱 prompt、旧模型、学生 / 人工 seed 分层。 | R1 / R2 / R6 | 来源不足时，降级为探索性分析。 |
| RQ6 | 转换规范化风险是什么？ | 转换成功率、不可映射字段、转换前 / 后 / 修正后诊断。 | R3 / R6 | 若转换器很薄，写为 artifact limitation。 |

## 3. 与贡献的关系

- RQ1--RQ3 支撑“结构化 feedback 有什么用”。
- RQ4 支撑或否定“Better STM”主结果。
- RQ5 支撑 seed 来源与泛化讨论。
- RQ6 防止转换器贡献与修正循环贡献混淆。

## 4. 预注册要求

R4/R6 必须在真实修正预演进入主结果前冻结：RQ、指标、阈值、统计表字段、失败纳入规则和降级写法。R5 的预演结果不得反向修改 RQ4 的通过条件。
