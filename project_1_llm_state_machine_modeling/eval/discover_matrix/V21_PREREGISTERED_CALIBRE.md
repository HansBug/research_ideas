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

## 二、v20 基线必须机械重导出，并与原值并列双报

> ⚠️ **本节相对初版已反转。** 初版写「不重算」，理由是「用新门控回溯改写旧代次不是同一次运行」。经独立裁决推翻：不重算，v21 与 v20 就跑在两套断言可采性规则上，`hit@k` 的差值把「方法变好」与「判据变了」混在一起 —— 那正是 §3.5 条款 4 直指的 C 级形态。改写发生在**分析层**，不回写 `runs/`，所以「不是同一次运行」的顾虑不成立。

**口径**：

1. v20 的命中表与多报表各出两列：`v20 as published` 与 `v20 re-derived under v21 predicates`。**不静默替换。**
2. 重导出走 `build_gist.py <round_dir> <out>` → `detect_fabrications.py <out>/audit`（后者有 SystemExit 守卫，直接指向 raw round dir 会拒跑）。被击落条目按 `issue_id` + 断言表达式**逐条列出**，不给汇总数。
3. **重导出结果标为 v20 的下界。** §3.5 条款 3：回测量的是误伤面，不是通用性。它只回答「A1 会击落 v20 多少条已发布发现」，不回答「v20 在 A1 之下会不会改写出一条正确断言」—— 被拒的断言本会进入修订预算，producer 可能补出对的。不标注就等于让 v21 白占便宜。
4. 被击落的每一条按 [`HIT_CRITERION.md`](./HIT_CRITERION.md) §1 做**三分人工裁决**：(a) 捏造，从来不是命中；(b) **缺陷定位对、编码成了恒假谓词**，v20 仍记命中，且它是 A1 将付出召回代价的证据；(c) 存疑。**(b) 必须单独立账** —— 这是这次重算不至于自利的唯一保证。
5. `coverage_status` full→partial 只在分析层重算，**不回写 `runs/`**：§3.6 管的是已发布结论，不是原始运行记录。
6. ⚠️ **`62/196 = 31.6%` 与 `36/184 = 19.6%` 这两个数当前不可复算** —— 全仓不存在产生它们的脚本。在 `count_refusals.py` 落库并复现出来之前，报告里不得出现。

**另一处必须先说清的事实**：v20 **不是 33 格基线**。实测 `v20run1` 10 格、`v20run2` 8 格、`v20run3` 8 格 = **26 格**。历代对比必须逐格标出有效轮数；`n=1` 的格上 `hit@all` 不构成稳定性证据。

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

## 四、烧毁记账落成可执行事实，而不是一份文档

> ⚠️ **本节相对初版已改。** 初版说「接受测试为红」。经裁决推翻：报告要诚实解释为什么排除 `0018`，就必然写下 `0018`，于是拼写检测器会永远翻红 —— 那个红色随即不再表示「有新情况」，检测器等于报废。更根本的是，一份文档挡不住 `metrics_at_k.py` 继续把三个烧毁格算进能力主张带；**口径必须是代码读得到的事实，不是散文**。

已落地：

| 位置 | 内容 |
| :-- | :-- |
| `holdout.json` | 新增 `burned`（逐 pair 记 mechanism / since_commit / evidence / records）、`reportable_holdout`、`reportable_judgeable_total`、`reportable_layer_coverage`、`reportable_layers_at_k`、`replacement_available` / `replacement_note`。**已冻结字段一字未动** —— 移动已冻结分母本身就是口径迁就 |
| `holdout.py --verify` | 改为与 `burned` 对账：已记录的烧毁通告后 exit 0，**未记录的命名仍 exit 1**；另加反向检查「burned 不得同时在 reportable_holdout 中」 |
| `test_holdout_stays_clean.py` | 命名检查主语改 `reportable_holdout`；新增 4 条 —— 二者划分冻结集、缩小后的分母可加和、每条烧毁必须有机制与证据、**未记录的烧毁必须 exit 1**（正控用已知被点名的 `0018`，否则绿灯与「检测器坏了」无法区分）|
| `metrics_at_k.py` | 两带改三带：能力主张 / **已烧毁 hold-out（共演化观测）** / 历史四格 |
| `cli.py` | A1 写入 `gate_ablation.non_ablatable_pair_motivated_gates`，附注它为何在措辞通用的前提下仍属 pair-motivated |

**代价如实记录**：hold-out 可判定条目 **23 → 9**，分层为 `wellformedness` 5、`nl_contradiction` 2、`nl_named` 1、`over_specification` 1 —— 按 `layers_reportable_at_k` 的 ≥4 阈值，**只有 `wellformedness` 一层仍可报，`nl_named` 从 10 条掉到 1 条，直接掉出报告资格**。

**无替补，且是结构性的**：候选池重算后只剩 `0058`，而它就属同一 NL 组；`--freeze` 会以 undersized 拒绝。本语料内不存在可用的替补 hold-out —— 这要写成方法学限制，不是本轮的运气问题。

---

## 复算入口

```bash
eval/discover_matrix/measure_rule_surface.py            # 两条规则的触发面与 NL 组归并
eval/discover_matrix/count_refusals.py <matrix_dir>     # 每格每轮的 gate 拒答计数与分桶（待建）
eval/discover_matrix/holdout.py --verify                # 与 burned 对账；已记录的烧毁通告后 exit 0
eval/discover_matrix/present_for_judgment.py v21        # 逐格并列呈现，供人工判定
eval/discover_matrix/metrics_at_k.py <verdicts.json>    # 只做算术，判定由人工给
```
