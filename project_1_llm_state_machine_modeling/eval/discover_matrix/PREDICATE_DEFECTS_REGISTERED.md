# 测量链侧缺陷登记：谓词求值实现与断言构造

v46 意外发现裁定中，有 4 个簇的 False **不是制品缺陷，而是测量链自身造成的**——
`0054-5`、`0046-8`、`0026-3`（裁定 `NO_NL_BASIS`）与 `0044-4`（裁定 `FALSE_POSITIVE`，
因其主张与制品相反这一条更强更靠前）。裁定口径见
[UNEXPECTED_TAXONOMY.md](./UNEXPECTED_TAXONOMY.md)，逐簇判据见
[unexpected_evidence.md](./v46/unexpected_evidence.md)。

## ⛔ 两个「不动」必须分开，不要混用

| 对象 | 状态 | 含义 |
| :-- | :-- | :-- |
| 谓词**词表** | **冻结** | 不增删谓词，不改任何谓词所问的问题。改词表会作废 v37→v46 全部跨代次可比性；且 `variable_declared` 在本语料上的 0 产出**本身就是证据**，删掉谓词等于删掉证据 |
| 谓词**实现** | **可修，且已修** | 求值方式写错时，谓词问的问题没变、答案变对了。这不影响跨代次可比性的定义，只影响该谓词在各代次上的取值——须在报告口径里注明生效代次 |

**本文件按「已实施 / 未实施」两栏登记，不再声称「只登记不修」。**

| 编号 | 对象 | 状态 | 关联簇 |
| :-- | :-- | :-- | :-- |
| P-1 | `persists_until` 求值 | ✅ 已实施 | `0046-8`（`0044-2` 修复后为真阴性） |
| P-2 | `stays_in` 求值 | ✅ 已实施 | `0044-4`（`0054-1` 修复后为真阴性） |
| P-3 | 未消费时的锚点回退 | ⬜ 未实施（判定者须知可防） | `0044-4` |
| P-4 | 断言构造阶段用恒假参数 | ⬜ 未实施 | `0054-5`、`0026-3` |

---

## P-1 `persists_until` 在 release 达成后不解除义务（✅ 已实施）

**位置**：`paper_stm_repair/pipeline/feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py`
的 `persists_until`（`grep -n "def persists_until" $F`）。

**缺陷**：原实现是一条覆盖**整个 horizon** 的有界不变式
`check invariant <= N: (release) || active(state)`，**不是真正的 until**。
`release` 一旦达成，义务并不解除；于是只要 release 状态**不是吸收态**，下一帧必然违反。

**影响面**：全语料凡 release 状态非吸收态的 pair 都会中招——本语料每个模型都有终止路径。

**判据（构造性反例，与语料无关）**：手工模型 `S -rel-> R -go-> T` 按构造满足「S until R」，
原实现在 `bound>=2` 上返回 False，反例为 `S, R, T`，**首个违反帧落在 release 帧之后**。
一个在「按构造满足它的模型」上返回 False 的谓词，其 False 不能作为任何东西的证据。

**已实施的修法**：改为**按 release 首次成立的帧做案例分解**——对每个 `k`，假设 `release`
在 `k` 之前都不成立，再要求义务保持到 `k`；任何一个 `k` 失败即 False。
首次 release 在第 `m` 帧的路径被所有 `k <= min(m, N)` 覆盖，最紧的是 `k = m`，
**没有任何查询看过那一帧之后**——正是原实现越过的那段窗口。
这是**弱 until**（永不释放但也不离开该状态时答 True），有界 horizon 下只有这一种读法可用。

**同批去掉的一道守门**：前置的空真守卫 `check reach <= N: !(release)`（意在「若无任何运行能让
`release` 为假则拒答」）**只会把正确的 True 变成 False**——该条件所描述的情形恰恰就是答案为
True 的情形。真正的空真由 `assume` 不可行时引擎的非终止退出承担，经 `_formal_holds`
转成 `UnsupportedEvidence`（拒绝作答），**永远不会变成静默的 True**。

**已知残留（一处 coverage gap，不是错误答案）**：`release` 在每条运行的第 0 帧就成立时，
所有 `k >= 1` 的假设都不可行，谓词**拒绝作答**，而真值是 True。
`check invariant <= 0` 被文法拒绝（bound 从 1 起），从引擎的失败消息反推「假设不可行」
又是拿报错当裁定。按 [CLAUDE.md](../../../CLAUDE.md) §10 记为 coverage gap；
在这种模型上该 until 主张本来也什么都没断言。

**关联簇**：`0044-2` 与 `0046-8` 都源于这条误读（把 NL 的 `continuously` / `remains`
当成状态驻留不变式）。`0044-2` 在修复后的实现上于冻结制品求值为 **True**，
已裁为真阴性并移出多报桶，见
[not_produced.jsonl](./v46/unexpected_verdicts/not_produced.jsonl)；
`0046-8` 仍留在桶内，裁定 `NO_NL_BASIS · N-MODAL`——它的问题在 NL 读法，不在求值。

---

## P-2 `stays_in` 把「事件被忽略」与「离开了状态」压成同一个 False（✅ 已实施）

**位置**：同一文件的 `stays_in`（`grep -n "def stays_in" $F`）。

**缺陷**：原实现在 `trigger not in self._consumed(view)` 时直接 `return False`，
把「事件被忽略、机器原地未动」与「机器真的离开了该状态」压成同一个 False。

**判据（实测，`SimulationAPI`）**：

| 钉住的状态 | 投喂事件 | consumed | fired | 结果 active |
| :-- | :-- | :-- | :-- | :-- |
| `InMotion.Approaching` | `Reached_Cruising_Cruise` | `[]` | `[]` | `[root, InMotion, InMotion.Approaching]` ← **原地未动** |
| `InMotion.Accelerating` | 同上 | `[该事件]` | 有 | `[root, InMotion, InMotion.Cruising]` |

生产者据此写出「运行离开了 Approaching」——**与制品完全相反**。

**已实施的修法**：**消费与否不再参与本谓词的判断**。该谓词只问占用：
运行后 `source` 是否仍活跃。没动 → 仍活跃 → True。

⚠️ **反向的写法同样错，不要「改回去」**：在未消费时返回 True 也不对——「未消费」不蕴含
「未改变」，完成迁移与守卫边在同一周期照样触发。实测：三节点完成链 `A1 -> A2 -> A3` 上投喂
一个不被消费的 `ping`，`A1` 已不活跃，而按「未消费即 True」的写法本谓词答 True、
`occupancy_after` 答 False——**两个谓词对同一次运行断言相反的事实**。

**同批恢复生效的两道拒绝门**：原来的早退分支坐在 `[*]` 与复合态两道门**之上**，
使它们只在事件恰好被消费时才生效；去掉早退后两道门恢复常态：

- `source="[*]"` 时按冷启动落定的**最深叶**比较，而不是整条 root..leaf 链（比整条链会近乎恒 True）；
  运行在该 trigger 之前不进入任何状态时，`UnsupportedEvidence` 拒答。
- 复合态作 `source` 不具判别力（前缀匹配会被整棵子树满足），拒答。

**「缺自环」这个问题归谁**：不再归本谓词。行为侧问 `event_consumed(source, trigger)`，
结构侧问 `edge_declared`。

**关联簇**：`0044-4` 仍留在桶内，裁定 `FALSE_POSITIVE · FP-0`（它同时受 P-3 影响）。
`0054-1` 在修复后的实现上于冻结制品求值为 **True**，已裁为真阴性并移出多报桶，见
[not_produced.jsonl](./v46/unexpected_verdicts/not_produced.jsonl)。

---

## P-3 未消费时的锚点回退，会被误读成执行轨迹（⬜ 未实施，判定者须知可防）

**位置**：同一文件中 `if not fired and unconsumed:` 分支（`grep -n "not fired and unconsumed" $F`）。

**缺陷**：什么都没发生时，锚点回退到**声明该事件的**那条迁移。于是 `model_refs` 里出现一条
与断言主体不相邻的 `transition:N`，看上去像执行轨迹，实际是静态查表结果。

**判据**（`0044-4`）：`model_refs` 里出现 `transition:7`，其原文是
`model.fcstm:19 Accelerating -> Cruising : /Reached_Cruising_Cruise` ——
**不是 `Approaching` 的出边**（`Approaching` 只有 index 12 与 15）。
旁证：同一记录里 `occupancy_after(source=Accelerating, target=Cruising, ...)` 的 `model_refs`
与它**逐字相同**却 `result=True`，证明该锚点是静态查表而非执行轨迹。

**判定者须知**（不修也能防）：
> **凡 `model_refs` 里出现的元素与断言主体不相邻，都要回查是不是这条回退分支。**

**修法方向**：给回退锚点打标（如 `formal:examined_only` 那样的显式标记），
让归因侧能区分「执行轨迹」与「静态查表」。

---

## P-4 词表无法表达该义务时，断言用「恒假参数」替代（⬜ 未实施）

**这一条不是谓词实现缺陷，而是断言构造阶段的缺陷**，因此不受「谓词词表冻结」约束，
可以独立整改。

**实例**：`0054-5`（`NO_NL_BASIS · N-MODAL`）。断言的 rationale **自陈**：

> 「由于 readiness 释放条件**未能在当前闭合谓词中机械化**，断言以 `release=false`、`bound=5`
> 检查未释放情况下的有限保持」

**两层问题**：

1. **词表缺口**：闭合谓词无法表达 NL 10 的「ready to stop or decelerate」。
   这是词表的表达力边界；是否补谓词需另行评估，**本轮词表冻结**。
2. **断言构造错误**：`release=false` 使 `persists_until` 退化为「必须永远停留」——
   **构造性不可满足**。按 [CLAUDE.md](../../../CLAUDE.md) §10，无法机械化的义务应记为
   **`coverage_gap`**，让该格带着残缺产物落盘；改用恒假参数报成缺陷，
   等于**把「测不了」伪装成「测出来了」**。
   按 [CLAUDE.md](../../../CLAUDE.md) §13，它也是「多道门交集为空」的一个实例：
   NL 2/10 恰恰**许可**该迁移，而这样构造出来的断言禁止它。

**可立即执行的整改（不动谓词）**：在断言构造阶段禁止「用恒假参数替代无法表达的条件」，
并要求此种情形改产出 `coverage_gap`。判据可机械化：**若某参数取值使断言与被测模型无关地恒假，
拒绝该断言。**

**为什么它比看上去严重**：这类断言产出的 False **必然**被下游读成「模型有缺陷」，
而它实际只说明「我们没能表达这条义务」。它是一条**系统性把词表缺口转化为伪缺陷**的通道。

**同类簇**：`0026-3`（`NO_NL_BASIS · N-ANCHOR`）——义务真实存在，但被断言钉死在
NL 并未指定的作用域上；NL 2 的真实违反已由台账 `EIS-0026-03` 记录。

---

## 复算命令

```bash
cd project_1_llm_state_machine_modeling
F=paper_stm_repair/pipeline/feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py
grep -n "def persists_until" $F        # P-1：案例分解的 for k in range(1, horizon + 1) 循环在其下
grep -n "def stays_in" $F              # P-2：其下应无任何 self._consumed(view) 早退
grep -n "not fired and unconsumed" $F  # P-3：未实施，分支仍在
```

⚠️ **按符号定位，不要按行号**——`predicate_api.py` 仍在演进，行号会漂。
