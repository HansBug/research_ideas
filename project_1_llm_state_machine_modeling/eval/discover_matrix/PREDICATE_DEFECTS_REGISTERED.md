# 已登记的谓词侧缺陷（只登记，不修）

v46 意外发现裁定过程中，有 6 个簇的 False **不是制品缺陷，而是谓词被操作化的方式造成的**——
其中 5 条属 `N0` 子类（`0054-1` `0054-5` `0046-8` `0026-3` `0044-2`，裁定为 `NO_NL_BASIS`），
另 1 条 `0044-4` 属 `F3`（裁定为 `FALSE_POSITIVE`，因其主张与制品相反这一条更强更靠前）。

⛔ **谓词逻辑本轮保持不动。** 本文件只做登记，不含任何修改。理由见
[V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md) 表 B 下方：
中途改谓词会作废 v37→v46 全部跨代次可比性，而这些缺陷不影响本轮结论的方向
（它们只制造多报，不制造漏检）。

⚠️ **登记 ≠ 承认可以拖。** 下面第 1 条的影响面很大：**对任何有终止路径的模型恒为 False。**
在它修复前，`persists_until` 的 False 不能作为缺陷证据使用。

---

## P-1 `persists_until` 在 release 达成后不解除义务

**位置**：`paper_stm_repair/pipeline/feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py:1802-1806`

**实现逐字**：

```python
query = (
    f"{head}"
    f"check invariant <= {_budget(bound, 'bound', DEFAULT_BOUND)}: "
    f'({release}) || active("{state}");'
)
```

**缺陷**：这是一条覆盖**整个 horizon** 的有界不变式，**不是真正的 until**。
`release` 一旦达成，义务并不解除；于是只要 release 状态**不是吸收态**，下一帧必然违反。

**实测证据**（pair 0044，`0044-2`，用 `FBMCQAPI` 实跑而非推断）：

| bound | 结果 | 反例 frames |
| --: | :-- | :-- |
| 1 | holds / unsat | — |
| 2 | 首次失败 | `[0:Approaching, 1:EmergencyStopping, 2:terminated]` |
| 3 | 失败 | `[0,1:Approaching, 2:Stopping, 3:terminated]` |
| 4 | 失败 | `[0:Approaching, 1:Approaching, 2:EmergencyStopping, 3:terminated, 4:terminated]` |

**三次反例的首个违反帧无一例外都在 release 达成之后的 terminated 帧。**

**为什么不是制品缺陷**：作者在 `stm0.puml:22-23` 明写 `Stopping --> [*]` / `EmergencyStopping --> [*]`
——该不变式在**作者原件上同样不可满足**，与 R4.5 编译无关（反例里 token 两阶段路由被折叠成单步，
`composite_source_activation_dispatch` 债务码未参与）。

**影响面**：**全语料凡 release 状态非吸收态的 pair 都会中招。** 这是本文件里最要紧的一条。

**修法方向**（未实施）：在 `release` 首次成立后解除义务，或至少豁免 `terminated` 帧。

**关联簇**：`0044-2`、`0046-8`（同形：把 NL 的定性描述「continuously」/「remains」
误读成状态驻留不变式）。

---

## P-2 `stays_in` 把「事件被忽略」与「离开了状态」压成同一个 False

**位置**：`predicate_api.py:1407-1408`（注释在 1404-1406）

**实现逐字**：

```python
# Both halves matter.  Without the consumption check an ignored event
# looks identical to a declared self-loop, so the missing-self-loop
# defect this predicate advertises could never be observed.
if trigger not in self._consumed(view):
    return False
```

**缺陷**：注释自陈这是**有意设计**——为了让「缺自环」可观测。代价是
**「事件被忽略、机器原地未动」也返回 False**，与「机器真的离开了该状态」不可区分。

**实测证据**（pair 0044，`0044-4`，用 `SimulationAPI` 实跑）：

| 钉住的状态 | 投喂事件 | consumed | fired | 结果 active |
| :-- | :-- | :-- | :-- | :-- |
| `InMotion.Approaching` | `Reached_Cruising_Cruise` | `[]` | `[]` | `[root, InMotion, InMotion.Approaching]` ← **原地未动** |
| `InMotion.Accelerating` | 同上 | `[该事件]` | 有 | `[root, InMotion, InMotion.Cruising]` |

**后果**：生产者据此写出「运行离开了 Approaching」——**与制品完全相反**。

**修法方向**（未实施）：区分「未消费」与「已消费且离开」，或让报错文案指明是哪一种。

---

## P-3 未消费时的锚点回退，会被误读成执行轨迹

**位置**：`predicate_api.py:664-672` 的 `if not fired and unconsumed:` 分支

**缺陷**：什么都没发生时，锚点回退到**声明该事件的**那条迁移。于是 `model_refs` 里出现一条
与断言主体不相邻的 `transition:N`，看上去像执行轨迹，实际是静态查表结果。

**实测证据**（`0044-4`）：`model_refs` 里出现 `transition:7`，其原文是
`model.fcstm:19 Accelerating -> Cruising : /Reached_Cruising_Cruise` ——
**不是 `Approaching` 的出边**（`Approaching` 只有 index 12 与 15）。
旁证：同一记录里 `occupancy_after(source=Accelerating, target=Cruising, ...)` 的 `model_refs`
与它**逐字相同**却 `result=True`，证明该锚点是静态查表而非执行轨迹。

**判定者须知**（本条不修也能防）：
> **凡 `model_refs` 里出现的元素与断言主体不相邻，都要回查是不是这条回退分支。**

---

## P-4 谓词操作化产生 NL 未要求的义务（`N0` 家族其余项）

`0054-1`、`0054-5`、`0026-3`。其中 **`0054-5` 是构造性不可满足**——
NL 2/10 恰恰**许可**该迁移，谓词却禁止它。按 [CLAUDE.md](../../../CLAUDE.md) §13 属
「多道门交集为空」类缺陷。

---

## 复算命令

```bash
cd project_1_llm_state_machine_modeling
F=paper_stm_repair/pipeline/feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py
sed -n '1798,1808p' $F   # P-1：1802-1806 是 query，check invariant <= N: (release) || active(state)
sed -n '1398,1410p' $F   # P-2：1407-1408 是那两行，1404-1406 是自陈用意的注释
```
