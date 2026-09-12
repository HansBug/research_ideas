# Completion of SysML state machines from Given-When-Then requirements

## R1.6 strict seed 全文核验结论

| 字段 | 结论 |
|---|---|
| bibliographic_id | DOI `10.1007/s10270-024-01228-3`，Software and Systems Modeling 2024 |
| strict_seed_grade | `NN-D` |
| artifact_usability | `SA-3` |
| 排除码 | `X_REPAIR_ONLY` |
| 是否计入主 seed | 不计入。该文是 partial SysML model + GWT requirements 的 state-machine completion，不是从 NL 生成 `STM_0`。 |

## P1/P2/P3/P4 核验

| 谓词 | 判定 | 证据 |
|---|---|---|
| `P1_NL_INPUT` | 部分通过 | 输入包含 Given-When-Then / Gherkin 风格需求。 |
| `P2_T0_STM_FAMILY` | 通过 | 输出为 SysML state machines transitions / triggers / guards / effects。 |
| `P3_GENERATION_RELATION` | strict 失败 | 方法从 partial SysML model / pre-existing states 出发补全迁移，不是 `NL -> initial STM_0`。 |
| `P4_EVIDENCE_POINTER` | 通过 | 本地 `paper_content.txt` 开头摘要明确从 partial SysML model 和 GWT requirements 完成 state machines。 |

## SS / SA 解释

- `NN-D` + `X_REPAIR_ONLY`：对本论文“修正/补全/feedback”概念有启发，但不能作为 strict seed 的初始生成来源。
- `SA-3`：论文和案例描述公开，未见公开代码 / 数据 / 模型文件。

## R2 使用建议

保留为 completion boundary / related work；可用于提醒 reviewers：我们不是把“已有 partial model 补全”误当作 `NL -> STM_0` seed。
