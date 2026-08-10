# 测量链侧缺陷登记：谓词求值实现与断言构造

> **本文件由两份原件合并**：`PREDICATE_DEFECTS_REGISTERED.md`（v46 活登记，P-1…P-4）与
> `OCCUPANCY_HORIZON_BUG.md`（v23 纠出、已修的 `occupancy_after` 视界缺陷，现登记为 **P-0**）。
> 两者同类：谓词求值实现缺陷、带双侧验收判据与影响面复算。合并只调整了标题层级与跨文件链接。

v46 意外发现裁定中，有 4 个簇的 False **不是制品缺陷，而是测量链自身造成的**——
`0054-5`、`0046-8`、`0026-3`（裁定 `NO_NL_BASIS`）与 `0044-4`（裁定 `FALSE_POSITIVE`，
因其主张与制品相反这一条更强更靠前）。裁定口径见
[docs/protocol/unexpected_taxonomy.md](../../protocol/unexpected_taxonomy.md)，逐簇判据见
[unexpected_evidence.md](../../../v46/unexpected_evidence.md)。

## ⛔ 两个「不动」必须分开，不要混用

| 对象 | 状态 | 含义 |
| :-- | :-- | :-- |
| 谓词**词表** | **冻结** | 不增删谓词，不改任何谓词所问的问题。改词表会作废 v37→v46 全部跨代次可比性；且 `variable_declared` 在本语料上的 0 产出**本身就是证据**，删掉谓词等于删掉证据 |
| 谓词**实现** | **可修，且已修** | 求值方式写错时，谓词问的问题没变、答案变对了。这不影响跨代次可比性的定义，只影响该谓词在各代次上的取值——须在报告口径里注明生效代次 |

**本文件按「已实施 / 未实施」两栏登记。**「登记」不蕴含「不修」——
求值实现的缺陷该修就修，登记的作用是让每一条的**状态、判据与生效范围**可查。

| 编号 | 对象 | 状态 | 关联簇 |
| :-- | :-- | :-- | :-- |
| P-0 | `occupancy_after` 视界非单调（`within_cycles` 实为「恰好第 N 轮」） | ✅ 已实施（v23 纠出） | 伪状态族 pair（`0018`/`0038`/`0048`），见 §P-0 |
| P-1 | `persists_until` 求值 | ✅ 已实施 | `0046-8`（`0044-2` 修复后为真阴性） |
| P-2 | `stays_in` 求值 | ✅ 已实施 | `0044-4`（`0054-1` 修复后为真阴性） |
| P-3 | 未消费时的锚点回退 | ⬜ 未实施（判定者须知可防） | `0044-4` |
| P-4 | 断言构造阶段用恒假参数 | ⬜ 未实施 | `0054-5`、`0026-3` |

---

## P-0 `occupancy_after` 的 `within_cycles` 非单调（✅ 已实施）

> 本节原为独立文件 `OCCUPANCY_HORIZON_BUG.md`，标题为
> 「C 级实现缺陷：`occupancy_after` 的 `within_cycles` 非单调」。
> 由第 6 步根因分析纠出，**实跑谓词**验证确认。它同时推翻了此前两处归因。

### 事实

```
occupancy_after(ChargedFlash --Charged_true--> TakePicture, within_cycles=c)
  c=1        True
  c=2..8     False        ← 单调性被违反
```

**名字是「N 轮内」（`within`），实现却是「恰好第 N 轮」**（`_occupies` → `_active` 只读
`view.final`，而 `_reaches_within` 是扫全部 cycle 的）。

### 机制

`Junction3 → join2 → Junction2 → TakePicture` 四条声明边在**同一个 cycle 内**走完 —— 伪状态不是
stoppable successor，所以整条链塌进一帧。**`join2` 没有等任何分支。**

False 的唯一来源是 `within_cycles=5` 多跑了 4 个空 cycle，而 `TakePicture → WriteMemory` 这条无触发
完成边把机器带走了。

而 prompt 又指示生产者把 `within_cycles` 按**声明边数**往上调 —— 于是「按边数」在伪状态密集的模型上
**必然过冲**。这解释了为什么失配只在被标 `pseudo` 的 pair 上密集，**与并发无关**。

### 影响面（机械复算，无需判定）

| 量 | 值 |
| :-- | --: |
| 唯一 `occupancy_after` 调用（v22+v23） | 846 |
| 其中结果为 False | 219 |
| **其中在更小 horizon 上为 True** | **51 = 23.3%** |
| 涉及的唯一 (格, kwargs) | 15 |

形态一律 `[…, True, False, False…]`。而 `_HORIZON_PROBE` 只向**上**搜（`range(asked+1, …)`），其注释
明确假设单调性（「a genuine defect does not become satisfied at a longer horizon」）—— **该假设对无
触发出边不成立**，所以这类下翻永远抓不到。

### 它推翻了此前的两处归因

#### 1. 「并发造成的 False 被标成 safe」——**归因错误**

我写过：「`bind_attribution` 把一条由**正交区并发语义**造成的 False 标成 `safe`…`join2` 是汇合伪状态、
需两条并行分支同时到达」。实跑 trace 显示整条链一个 cycle 走完，`join2` 未同步任何分支。

**那是一条假阳性发现，起因是实现缺陷，不是语义边界。** 把可修的 bug 归因成 paper1 边界外的语义，
会把「该修的东西」永久登记为「不该管的东西」。

📌 我当时读了 NL、读了模型、查了 `_reject_transient_subject` 的实现才下结论 —— **三样都做了仍然错。
缺的是实际跑一遍那个谓词。** 今天已记过「人工读原文也需要先确认原文的约定」，这里再补一层：
**读实现不等于跑实现。**

#### 2. 「92 条 `unsupported_binding`」——**数字错误**

正确数（用 `count_refusals.py`）：v22 **2** / v23 **27**。我裸 grep `record.json` 得 16/92，把同一
消息在 input / output / 多轮修订里的重复都算了。且真正的主门是 `transient_subject`
（137 → 115），不是 `unsupported_binding`。

定性部分成立且更强：v23 的 27 条里 **26 条（96%）**在伪状态族的两个 pair 上。

### 修法（已实施；本节两处首版规定**都是错的**，按 §3.6 就地改写）

**修法：让 `_occupies` 从「触发被消费的那一帧」起扫到 `cycles` 帧。**

⚠️ **首版此处规定「扫全部 cycle」—— 那是错的，已删。** `_simulate` 构造的计划是
`[settle...] + [[trigger]] + [[]...]`，所以 **cycle 0 是触发被 offer 之前的配置**。扫全部帧会让谓词在
「机器本来就在目标里、而触发把它带走了」时返回 True，即**吃掉发现**。实测 pair 0006：

    Attack --Attack_Complete--> AttackingTarget
      cycle 0: [..., Attack, AttackingTarget]   <- 触发之前
      cycle 1: [..., Searching]                 <- 触发之后

11 个 pair 中 10 个有此类翻转，方向一律 False→True。合成全组合扫描下 129 处，真实记录调用下 1/247
（两个分母不同，不可混用）。

⚠️ **首版的验收判据「`_occupies(·, c)` 对 `c` 单调不减」也是错的 —— 它被 `return True` 满足**，已删。
一条只能在「答 False 太多」时失败的判据，永远抓不到「答 True 太多」这一半。1594 项测试正是在这个
判据下对一个吃掉十个 pair 发现的改动全绿。

**正确的验收是双侧的**，三条并用：

1. 单调性（抓「答 False 太多」）—— `test_regression_call_is_true_at_every_horizon` 等
2. **反向配对**（抓「答 True 太多」）—— `test_trigger_must_move_the_machine_there`：触发把机器带离
   目标时必须为 False
3. **窗口起点**（抓两个方向的 off-by-one）—— `test_occupancy_after_from_the_pseudo_initial` 第三条断言

实测 7 个错误变体（`return True` / `return False` / 只读末帧 / 扫全部帧 / 起点 ±1 / 末次消费帧）中
**每一个行为可区分的都至少被一条测试打破**，且「只读末帧」与「扫全部帧」被两组**不相交**的测试抓住。

⚠️ 方向提醒：修它会把 51 条本该为 True 的 False 变回 True，因此会**压低 `over@1`**，同时**可能压低
`hit@k`**（有些命中是靠这些假 False 达成的）。两个方向必须分开报，不能合并成一个数。

### 待重核：12 条 `boundary` 判定

多报核验里 12 条被判 `boundary`（并发/时钟，不在断言对象内）。抽查的一条实测
`_occupies(c=1)` = True、`c=2` = False —— **`boundary` 的结论碰巧对（不算模型缺陷），机制说明是错的**。

建议对这 12 条各跑一次横轴扫描，把「末帧伪影」从「并发边界外」里分出来。**这是机械复算，不需要
人工判定。**

### 修法的影响上界：20 / 249 条已发布发现（8.0%）

⚠️ **首版此节报「10 / 249 = 4.0%」，逐 pair 为 `0029`4 / `0038`3 / `0018`2 / `0000`1，并断言「其余
七个 pair 各 0 条」。这两个数都是错的，已按 §3.6 就地更正。** 复算口径与结果如下。

| 口径 | 总数 | 0035 | 0047 |
| :-- | --: | --: | --: |
| **A：issue 文本中出现 `occupancy_after`**（我可复算） | **20 / 249 = 8.0%** | **3** | **1** |
| B：issue 引用的断言实际调用该谓词（公平性 review 报） | 55 / 249 | 6 | 1 |

口径 A 逐 pair：`0029` 7、`0018` 4、`0035` **3**、`0038` 3、`0000` 2、`0047` **1**。

📌 **「各 0 条」这个断言是假的**，而它是首版给预注册预期第 3 条的**唯一依据**。口径 B 我未能用正确
实现复现（首版尝试给出 249/249，是实现缺陷），故只报公平性 review 的数并标注未独立复算。**两个口径
都不支持「0 条」。**

#### 预注册预期第 3 条的依据已更换

首版依据：「那两个 pair 各 0 条引用，所以序列不变」——**依据不成立**。

正确依据（可直接复跑）：那条记录的 primary 断言是
`occupancy_after(source='…DoorOpen', trigger='…Door_Closed', target='…DoorShut')`，实测在
`within_cycles = 1..5` 上、`只读末帧 / 扫全部帧 / 当前修法`三个实现下**一律 False** —— 因为
`settle(DoorOpen) = 0` 且 `Door_Closed` **从未被消费**，`_consumed` 守卫直接短路。该 pair 的 15 条
真实绑定与另一个 pair 的 23 条，翻转数均为 **0**。

代码正确性 review 的独立重放（247 个唯一调用）给出同一结论：11 条翻转**全部**落在 `0018`/`0038`/
`0048`，其余八个 pair 零翻转。

**结论侥幸成立，但首版的论证过程不成立** —— 而这正是预注册的意义：若序列当真变了，我会拿着「零
曝露」这个假前提去找不存在的「意料外路径」。

#### ⚠️ 这个 4.0% 与 review 报的 42.3% 不矛盾，分母不同

| 数 | 分母 | 含义 |
| :-- | :-- | :-- |
| 4.0%（10/249） | **已发布 issue** | 修法对发布结果的影响上界 |
| 42.3%（69/163） | **合成扫描里新增的 True** | 错误修法引入假阳性的比例 |

`occupancy_after` 被调用 **2529 次**却只支撑 **10 条**已发布发现 —— 绝大多数调用结果被别的机制吸收
（合并进其他发现、被排除、或作为 supporting 证据）。

📌 **一个谓词的调用量与它对发布结果的影响力可以差两个数量级。** 若按调用量估计修法收益，会高估
250 倍。这是「两个数的分母不同」的又一实例，只不过这次在下结论前就认出来了。

#### 对下一轮的预期，写成可否证的形式

修法生效后，相对 v23 应观察到：

1. `occupancy_after` 相关的已发布发现数变化**不超过 ±10 条**（上界由本节给出）
2. `unaccounted_safe_false_assertions` 那条（v23 有 1 条）**应消失** —— 它正是被误记为「并发造成的
   False」的那条
3. `0035` / `0047` 的 `hit@k` 序列**不应改变** —— 依据不是「0 条引用」（那是假的，见上），而是
   它们的相关绑定在三个实现下一律 False（触发从未被消费）+ 独立重放的零翻转

第 3 条最要紧：**若可报带的序列变了，说明修法有我没预料到的路径，必须先查清再报。**

---

## P-1 `persists_until` 在 release 达成后不解除义务（✅ 已实施）

**位置**：`paper_stm_issue_discover/pipeline/feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py`
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
又是拿报错当裁定。按 [CLAUDE.md](../../../../../../CLAUDE.md) §10 记为 coverage gap；
在这种模型上该 until 主张本来也什么都没断言。

**关联簇**：`0044-2` 与 `0046-8` 都源于这条误读（把 NL 的 `continuously` / `remains`
当成状态驻留不变式）。`0044-2` 在修复后的实现上于冻结制品求值为 **True**，
已裁为真阴性并移出多报桶，见
[not_produced.jsonl](../../../v46/unexpected_verdicts/not_produced.jsonl)；
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
[not_produced.jsonl](../../../v46/unexpected_verdicts/not_produced.jsonl)。

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
   **构造性不可满足**。按 [CLAUDE.md](../../../../../../CLAUDE.md) §10，无法机械化的义务应记为
   **`coverage_gap`**，让该格带着残缺产物落盘；改用恒假参数报成缺陷，
   等于**把「测不了」伪装成「测出来了」**。
   按 [CLAUDE.md](../../../../../../CLAUDE.md) §13，它也是「多道门交集为空」的一个实例：
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
F=paper_stm_issue_discover/pipeline/feedback_loop/src/paper_stm_feedback_loop/assertions/predicate_api.py
grep -n "def _occupies" $F             # P-0：应从「触发被消费的那一帧」起扫到 cycles 帧
grep -n "def persists_until" $F        # P-1：案例分解的 for k in range(1, horizon + 1) 循环在其下
grep -n "def stays_in" $F              # P-2：其下应无任何 self._consumed(view) 早退
grep -n "not fired and unconsumed" $F  # P-3：未实施，分支仍在
```

⚠️ **按符号定位，不要按行号**——`predicate_api.py` 仍在演进，行号会漂。
