# 任务：把每条问题写成可执行的 19 谓词断言，并实跑验证

## 你要产出什么

对分配给你的每一条差异，判定它**能否用 19 个封闭谓词写出一条可执行的正面断言**，并**实际跑一遍**。

「可执行的正面断言」定义：一个只用 19 个封闭谓词 + `all`/`any`/`not`/`len` 组成的表达式，描述**正确模型应当满足**的性质，在这个有缺陷的模型上**实测返回 `False`**。

- 返回 `False` → 该缺陷可被断言捕获 ✓
- 返回 `True` → 你的断言写错了（它在缺陷模型上成立，说明它没抓住缺陷），重写
- 返回 `None` 或抛异常 → **不算可表述**。`None` 是「无法判定」，不能当 `False` 用作缺陷证据

## 19 个封闭谓词（唯一可用集合）

| 族 | 谓词 |
| --- | --- |
| S 结构 | `state_declared` `variable_declared` `event_declared` `containment` `initial_target` `edge_declared` `effect_declared` `action_declared` `guard_distinguishable` `cardinality` |
| B 行为 | `occupancy_after` `event_consumed` `stays_in` `variable_delta_after` `reaches` `terminates` |
| P 性质 | `invariant` `response_within` `persists_until` |

**`transition_exists` / `transitions` / `states` / `initial_child` / `effect_deltas` / `path` 不在其中**——它们是台帐当年的底层查询原语，用它们不算「现有谓词可表述」。若某条的现有 `assertable` 用了它们，你必须重写成 19 谓词形式或判为不可表述。

## 已知的坑（都是实测出来的，别重犯）

1. **`any(edge_declared(...))` 抛 `TypeError`** —— `edge_declared` 返回 `bool`，`any` 需要可迭代对象。有 3 条现有 `assertable` 这样写，根本不会执行。
2. **`guard_distinguishable` 在单目标时空集空真返回 `True`** —— 「这条边必须携带区分条件」写不出来。
3. **`initial_target` 看不到带触发的初始边** —— `_initial_child_of` 从单一入口作答即使它带触发，所以 `initial_target(root, X)` 会**正向放过**带触发初始边的缺陷模型。该族要改用 `event_consumed(source='[*]', ...)`。
4. **`occupancy_after` 有 horizon 自检** —— 若更大 cycles 也为 True 会拒答，防止 bound artifact。
5. **`cardinality` 数的是「非伪直接子状态」，会把投影合成的 `UnspecifiedInitial` / `FinalWaittr_*` / `InvalidInitialtr_*` 计入** —— 所以作者源看到的「3 个子态」在谓词层可能是 4 或 7。先看 FCSTM 再写 count。
6. **`variable_declared` 对 converter 的 `R45RouteToken` 按设计返回 False**，且 `EffectAPI` 会丢弃它——全语料唯一被声明的变量就是它，所以 `variable_delta_after` 基本无从验证。
7. **`state_declared(kind=...)` 只有 `leaf`/`composite`/`pseudo`/`any`**，没有 fork/join/junction/choice。

## 实跑方法

```python
import sys, json, pathlib
sys.path.insert(0, "/home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src")
from paper_stm_feedback_loop.assertions import build_eval_environment
R = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/reports/llms_emp_r45_java_60")
stem = f"llms_emp_feedback_final_{case}"
tr = json.loads((R/f"source_traces/{stem}.json").read_text())
env = build_eval_environment(model_text=(R/f"fcstm/{stem}.fcstm").read_text(),
    source_mappings=tr.get("mappings") or [], source_exclusions=tr.get("attribution_exclusions") or [],
    timeout_seconds=60, fbmcq_solver_timeout_ms=5000, fbmcq_max_bound=3, fbmcq_process_wall_seconds=15.0)
r = env.eval_assert("<你的表达式>", "理由")
print(r.value)   # True / False / None
```

**路径必须全限定**（`llms_emp_feedback_final_XXXX.Parent.Child`）。写断言前**先读该 case 的 FCSTM 投影**（`fcstm/<stem>.fcstm`）确认真实的状态名与层次——作者源的名字经投影后可能改变，且会多出合成节点。

用 `/home/zhangshaoang/oo-projects/research_ideas/venv/bin/python`。

## 材料

- 你的清单：`/tmp/predcheck/batch<N>.json`，`items[]` 每条含 `case` / `group` / `llm` / `diff_index` / `verdict` / `stratum` / `assertable`（现有字段，**可能有错，仅作参考**） / `reason_head`
- 完整 reason / ref / gen：`manual_review/<case>-review.json` 的 `diffs[<diff_index>]`（根目录 `/home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/eval/discover_matrix/`）
- NL 原文：`<R>/pairs/<case>/nl.txt`、作者模型 `<R>/pairs/<case>/plantuml.puml`、**FCSTM 投影 `<R>/fcstm/llms_emp_feedback_final_<case>.fcstm`**
- 谓词实现（查签名与语义）：`.../feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py`
- 谓词注册表：`.../feedback_loop/src/paper_stm_feedback_loop/discover/predicates.py` 的 `PREDICATE_ORDER`

## 输出

写 `/tmp/predcheck/result<N>.json`：

```json
{"batch": N, "groups": ["NL0x"],
 "items": [
   {"case":"0002","diff_index":0,"verdict":"problem","stratum":"nl_named",
    "expressible": true,
    "assertion":"initial_target(composite='llms_emp_feedback_final_0002.PumpControl', child='llms_emp_feedback_final_0002.PumpControl.PumpState')",
    "predicates":["initial_target"],
    "measured": false,
    "measured_raw":"False",
    "note":"NL 第 3 句要求 first transitions to PumpState；实测 False，缺陷被捕获",
    "rewrote_from":"现有字段的原样（若你重写了）"},
   {"case":"0035","diff_index":3,"verdict":"problem","stratum":"nl_named",
    "expressible": false,
    "attempted":["guard_distinguishable(...) -> True（空集空真，没抓住缺陷）","edge_declared(...) -> 需要具名 trigger，写不出「必须带条件」"],
    "shape":"「这条边必须携带区分条件」——单目标时 guard_distinguishable 恒 True，信息被静默丢弃",
    "closest_gap":"真词表缺口：缺一个『边必须携带区分条件』谓词"}],
 "totals":{"expressible":0,"not_expressible":0},
 "by_predicate":{"initial_target":0},
 "gap_shapes":["逐个列出不可表述的形态，合并同类"]}
```

## 要求

1. **每条都要实跑**，`measured_raw` 填实际返回值的字符串。没跑的不许标 `expressible: true`。
2. 若现有 `assertable` 能直接跑通且返回 False，沿用它并把 `rewrote_from` 留空；否则重写并填上原样。
3. **不可表述的要写清形态**（`shape`），并列出你尝试过什么（`attempted`）。合并同类形态到 `gap_shapes`。
4. `verdict` 为 `extra` 的条目一样要做——它们的断言应表达**后果**（`reaches`/`terminates`/`occupancy_after` 等），而不是「这个多出的元素存在」（那是前提不是缺陷）。若只能写出存在性，标 `expressible: false` 并说明。
5. 不要修改任何仓库文件。只写 `/tmp/predcheck/` 下的文件。

最后在报告里给：`totals`、按谓词的条数、以及**全部不可表述条目的形态清单**。
