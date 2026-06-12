# Claim-Evidence Map

## 1. 使用规则

任何后续摘要、引言、贡献句、Related Work 定位和实验结论都应先查本文件。R0 阶段只允许写任务、协议和证据需求；结果型 claim 必须等待 R4/R6 评价门和实验结果。

## 2. 当前允许 claim

| Claim | 当前证据 | 允许写法 | 不允许写法 |
|---|---|---|---|
| 第一篇任务已转向 `<NL, STM_0> -> STM_k` 修正 | [2026-06-12 导师讨论记录](../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)、[PR #100](https://github.com/HansBug/research_ideas/pull/100) | “本文研究给定 `NL` 与初始 `STM_0` 后的反馈驱动修正。” | “本文提出新的 `NL -> STM` 生成方法。” |
| `NL -> STM_0` 不作主贡献 | 同上 | “种子构造只记录来源和配置。” | “我们的主要贡献是从 NL 生成 `STM_0`。” |
| 语义增强 / 可机检 / 可执行表示是必要载体 | 导师记录 §5、PR #100 §1.4 | “为支撑诊断、仿真和修正反馈，需要可机检、可执行状态机制品。” | “提出 `fcstm` 新 DSL 是核心贡献。” |
| baseline 角色需要重排 | 导师记录 §6、PR #100 §3 | “prior artifacts 将作为 seed、converter pressure、error taxonomy、limited comparison 和 related work。” | “已有 baseline 不相关 / 已被排除。” |
| `Better STM` 需要操作化 | PR #100 §2、本目录 [better_stm_definition.md](../experiment_design/better_stm_definition.md) | “R0 定义最小必要条件，R4/R6 冻结评价门。” | “自动修正必然提升模型质量。” |

## 3. 需要后续证据的 claim

| 待证 claim | 需要证据 | 负责 PR | 当前状态 |
|---|---|---|---|
| 结构化反馈能关闭部分缺陷 | 诊断前后、拒绝修复、回归、振荡和不收敛统计 | R5/R6 | 未运行，不能写结果。 |
| 场景仿真能发现静态诊断难以发现的问题 | frozen scenario suite、trace mismatch、simulation-only defect | R4/R6 | 未冻结，不能写结果。 |
| 修正循环产生相对更优 `STM_k` | 五条件逐项台账、人工裁决、转换归因 | R6 | 未闭合，不能写结果。 |
| 不同 seed 来源影响修正效果 | R1/R2 seed registry、分层统计 | R2/R6 | 未冻结，不能写结果。 |
| converter 风险可控 | 转换成功率、信息损失、不可映射字段 | R3/R6 | 未定义，不能写结果。 |

## 4. Forbidden claims

| Forbidden claim | 风险等级 | 处理方式 |
|---|---:|---|
| 首个 / 最强 `NL -> STM` 方法 | C | 禁止出现在标题、摘要、引言和贡献。 |
| 首个 feedback loop / 首个 tool feedback | C | 禁止；已有 close works 可能涉及 feedback、trace、oracle 或 tool constraints。 |
| `fcstm` / `pyfcstm` / DSL 是论文核心创新 | C | 禁止；仅实现层出现。 |
| 完整形式化验证、soundness、model checking guarantee | C | 禁止，除非后续真实引入并验证。 |
| baseline 无需对照 | I | 禁止；PR #100 要求有限对照 / 消融。 |
| 只报成功，不报 rejected / rollback / non-convergence | I | 禁止；失败模式必须进入结果或局限。 |
| converter 清洗收益算作 repair-loop 收益 | I | 禁止；必须用三阶段台账分开。 |

## 5. 降级写法模板

| 强 claim | 安全降级 |
|---|---|
| “我们的系统提升状态机质量。” | “我们评估修正循环是否在预注册条件下得到相对更优的候选，并报告失败模式。” |
| “我们提出新的状态机 DSL。” | “我们将制品约束到一种可机检、可执行的状态机表示，以支撑诊断和仿真反馈。” |
| “我们击败已有 NL-to-STM baseline。” | “我们比较修正路线与无修正种子、从 NL 重新生成、自修正和可运行近似基线。” |
| “我们的验证保证正确性。” | “我们使用确定性诊断、轻量形式化 / 静态检查、场景仿真和回归约束提供可审计反馈。” |
