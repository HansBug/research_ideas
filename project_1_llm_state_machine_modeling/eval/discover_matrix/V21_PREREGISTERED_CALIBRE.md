# v21 报告口径 —— 在结果产生之前写死

写作时间点：v21 的 33 格已开跑、**尚无任何一格产出可读结果**。代码 `fc25c232`。

这份文件存在的唯一理由是 [CLAUDE.md §3.5 第 4 条](../../../CLAUDE.md)：中途放宽命中判据、更改分母或剔除不利样本，属于「评测口径迁就结果」。v21 引入的 A1 会**系统性地改变分母**，所以它的记账方式必须先于结果确定，否则事后无论怎么选都无法自证清白。

---

## 一、A1 使三个 hold-out 格丧失能力主张资格

**事实**（`measure_rule_surface.py`，真 parser + NL 组归并）：

| | 结果 |
| :-- | :-- |
| A1 触发的 pair | `0018`、`0038`、`0058`（3 / 60）|
| 其中 hold-out | `0018`、`0038` |
| A1 的引入动机 | commit `e85dd257` 正文自陈：看着这两格在 v20 的 17 条恒假发现写的 |
| NL 组 `53d65d24` | `0008 0018 0028 0038 0048 0058` —— hold-out 成员 `0018` `0038` `0048` |
| 样本外触发证据 | **零**。唯一非 hold-out 的触发样本 `0058` 与前两者同需求文本、同参考模型 |

`holdout.py` 规则 3 的原话说明了为什么这里要按组而不按 pair id 算：*同一组意味着同一份需求文本与同一份参考模型，针对其一成员写的规则会作用于每一个成员 —— 这是 pair-id 拼写检查看不见的*。

**口径**：

1. hold-out 的能力主张收缩到 **4 格**：`0032` `0035` `0043` `0047`。
2. `0018` `0038` `0048` 的结果照常全量报出，但归入「**方法 + 样本共演化观测**」，与调优四格并列，**不进入任何能力主张**。
3. A1 的正当性只以两项陈述：机制论证（它是 `_reject_undiscriminating_root` 恒真拒绝的恒假镜像）与单元测试负控。**报告中不得引用任何 pair 数字为 A1 的通用性背书。**
4. 主口径仍按全量 33 格 / 34 条报，分解表须同时给「能力主张 4 格」与「共演化 7 格」两栏。

> 这不是把 hold-out 缩小以让数字好看 —— 收缩后能力主张的样本量下降，对结果只会更不利。

## 二、v20 基线不重算，改为并列双报

**不重算。** 理由：A1 在 `0018` 拒掉 31.6%、在 `0038` 拒掉 19.6% 的最终断言，受影响 requirement 会丢掉全部 primary、`coverage_status` 由 `full` 变 `partial`。用 v21 的排除去重写 v20，等于**用新门控回溯修改旧代次的产出**，那不是同一次运行的结果。

**口径**：历代对比表在 `0018` / `0038` 两行加注 `A1`，并在表下写明：

> v21 起 A1 拒绝以伪状态为主语的占据类断言。`0018` / `0038` 的 v20 数字包含 17 条此类恒假发现，v21 不再产生它们。两代次在这两格上**度量的不是同一件事**，差值不可解读为能力变化。

若 v21 在这两格上 `hit@k` 下降，**照实报，并注明这正是 A1 的预期效果** —— 恒假断言此前若被计为命中，那本就是虚高。

## 三、`over@k` 必须并列拒答率，`unsupported` 必须落盘

**问题**：A1 把原本 `False`（会发布为发现）的断言变成 `UnsupportedEvidence` → `outcome=invalid` → 走修复预算 → quarantine 成 `CoverageGap`。而 `over@1` / `over@any` 的分母是「格 × 轮」，不是发现条数。于是**精度侧指标单调改善而能力毫无提高**。全流程此前没有任何地方计 `unsupported`。

**口径**：

1. `over@1` / `over@any` 旁必须并列 **`refused@1`**：同分母（格 × 轮）下每轮平均被 gate 拒绝的断言条数。精度改善若伴随 `refused@1` 同步上升，则该改善**不得**表述为能力提升。
2. 每格的 `UnsupportedEvidence` 计数与拒绝理由分布写进 audit bundle，字段：

```json
"gate_refusals": {
  "total": 0,
  "by_rule": {"transient_subject": 0, "undiscriminating_root": 0, "vacuous_conjunction": 0},
  "requirements_losing_all_primaries": []
}
```

3. `coverage_status: partial` 的格数与 `coverage_gaps` 条数进总表。**A1 把发现变成缺口，缺口必须和发现一样显眼。**

## 四、`test_holdout_stays_clean.py` 当前为红，不改测试

`holdout.py --verify` 报 `held-out pairs have since been named: {'0018': ['commit_body']}`，测试因此失败。

**不改测试、不改数据让它变绿。** 那个红色是准确的：hold-out 确实被烧了一格，而测试的职责就是让这件事无法被忽略。绿灯只应在 hold-out 重新变干净时出现，而本代次做不到 —— 候选池的第 8 个 `0058` 就在被烧的同一 NL 组里，无替补可选。

报告须在显著位置写明这一红色及其原因。后续若要恢复干净 hold-out，需要从未参与过任何规则编写、且不与 `53d65d24` 同组的 pair 重新冻结一组，那是独立任务。

---

## 复算入口

```bash
eval/discover_matrix/measure_rule_surface.py            # 两条规则的触发面与 NL 组归并
eval/discover_matrix/holdout.py --verify                # hold-out 灼烧状态（当前预期为红）
eval/discover_matrix/present_for_judgment.py v21        # 逐格并列呈现，供人工判定
eval/discover_matrix/metrics_at_k.py <verdicts.json>    # 只做算术，判定由人工给
```
