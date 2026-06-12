# evaluation gate：评价门顺序与继承规则

## 1. 核心规则

评价门必须先于真实修正预演冻结。不能先看 R5 的修正结果，再修改指标、阈值、主结果纳入规则或统计表字段。

## 2. 顺序

```text
R1 资产盘点 -> R2 样本冻结 -> R3 转换合同 -> R4 诊断/场景/评价门 v0 -> R5 修正循环预演 -> R6 评价协议与对照矩阵 -> R7 论文骨架
```

## 3. R4 必须冻结

| 项 | 说明 |
|---|---|
| 诊断类别 | parse / semantic / design / scenario 等最小分类。 |
| 场景 / 回归套件 | 四例预演使用的确定性场景和回归入口。 |
| 评价量表草案 | 与 `Better STM` 五条件对应。 |
| 主结果纳入规则草案 | 哪些 run 进入 pilot、哪些只能作失败案例。 |
| 统计表骨架 | 后续 R6 继承，不允许被 R5 结果任意重写。 |

## 4. R6 必须冻结

| 项 | 说明 |
|---|---|
| 最终 RQ 与指标 | 继承 R4，不得因 R5 结果好坏任意替换。 |
| 对照 / 消融 | no-repair seed、regenerate-from-NL、no structured feedback、可运行 repair baseline、converter-aware analysis。 |
| 人工裁决协议 | 裁决者、blindness、冲突处理、记录方式。 |
| 主结果 eligibility | schema-invalid、replay-invalid、partial run、provider failure 的纳入 / 排除规则。 |
| 降级写法 | 效果有限、样本不足、失败率高时的安全表述。 |

## 5. R0 不做的事

R0 不设置最终阈值、不写统计公式、不跑样本、不调用 LLM、不创建 run record。R0 只要求后续 PR 按上述顺序冻结。
