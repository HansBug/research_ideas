# 实验设计入口

本目录维护第一篇论文的上游实验约束：研究问题、评价顺序和 Better STM 定义。正式主实验协议尚未冻结；后续真实修正结果不能反向修改这里的核心判定逻辑。

## 1. 当前边界

- 不冻结最终指标阈值。
- 不定义完整评分表。
- 不选择最终实验样本。
- 不跑真实 LLM 或修正循环。
- 不把当前草案写成主实验结论。

Better STM 的五条件单独保留在 [better_stm_definition.md](./better_stm_definition.md)，这是后续 RQ4 和主结果判定的核心依据。

## 2. 研究问题草案

| RQ | 问题 | 需要的证据 | 安全降级写法 |
|---|---|---|---|
| RQ1 | 初始 `STM_0` 的主要缺陷类型是什么？ | parse / semantic / guard / action / hierarchy / behavior 缺陷统计 | 若样本少，写成 pilot characterization |
| RQ2a | 不同反馈来源能发现哪些结构、语义或行为问题？ | diagnostics 类型、feedback source、未闭合缺陷 | 若覆盖有限，写成 feedback coverage 分析 |
| RQ2b | 反馈输入修正循环后，哪些缺陷能被关闭，哪些会引入回归或振荡？ | 修复前后诊断、rejected repair、rollback、oscillation、non-convergence | 若不稳定，重点报告失败模式 |
| RQ3 | 场景 / 仿真反馈是否发现静态检查难以发现的行为缺陷？ | scenario pass/fail、trace mismatch、simulation-only defects | 若证据弱，写为补充反馈来源 |
| RQ4 | 自动修正是否产生相对更优 STM？ | 五条件逐项台账、`STM_0` vs `STM_k`、人工裁决、回归检查 | 任一条件失败，不计入 Better STM，只报告失败 / 局限 |
| RQ5 | seed 来源如何影响修正效果？ | prior artifact、弱 prompt、旧模型、学生 / 人工 seed 分层 | 来源不足时，降级为探索性分析 |
| RQ6 | 转换规范化风险是什么？ | 转换成功率、不可映射字段、转换前 / 后 / 修正后诊断 | 若转换器很薄，写为 artifact limitation |

RQ1--RQ3 支撑“结构化反馈有什么用”；RQ4 支撑或否定 Better STM 主结果；RQ5 支撑来源与泛化讨论；RQ6 防止转换收益与修正收益混淆。

## 3. 评价门顺序

评价门必须先于真实修正预演冻结。不能先看修正结果，再修改指标、阈值、主结果纳入规则或统计表字段。

```text
资产盘点 -> 样本冻结 -> 转换合同 -> 诊断/场景/评价门 v0 -> 修正循环预演 -> 正式协议与对照矩阵 -> 论文写作
```

### 3.1 评价门至少冻结什么

| 项 | 说明 |
|---|---|
| 诊断类别 | parse / semantic / design / scenario 等最小分类 |
| 场景 / 回归套件 | 预演使用的确定性场景和回归入口 |
| 评价量表草案 | 与 Better STM 五条件对应 |
| 主结果纳入规则草案 | 哪些 run 进入 pilot，哪些只能作失败案例 |
| 统计表骨架 | 后续正式协议继承，不允许被结果任意重写 |

### 3.2 正式协议至少冻结什么

| 项 | 说明 |
|---|---|
| 最终 RQ 与指标 | 继承评价门，不得因结果好坏任意替换 |
| 对照 / 消融 | no-repair seed、regenerate-from-NL、no structured feedback、可运行 repair baseline、转换器-aware analysis |
| 人工裁决协议 | 裁决者、blindness、冲突处理、记录方式 |
| 主结果 eligibility | schema-invalid、replay-invalid、partial run、provider failure 的纳入 / 排除规则 |
| 降级写法 | 效果有限、样本不足、失败率高时的安全表述 |
