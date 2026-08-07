# C 级实现缺陷：`occupancy_after` 的 `within_cycles` 非单调

由第 6 步根因分析纠出，我**实跑谓词**验证确认。它同时推翻了我此前两处归因。

## 事实

```
occupancy_after(ChargedFlash --Charged_true--> TakePicture, within_cycles=c)
  c=1        True
  c=2..8     False        ← 单调性被违反
```

**名字是「N 轮内」（`within`），实现却是「恰好第 N 轮」**（`_occupies` → `_active` 只读
`view.final`，而 `_reaches_within` 是扫全部 cycle 的）。

## 机制

`Junction3 → join2 → Junction2 → TakePicture` 四条声明边在**同一个 cycle 内**走完 —— 伪状态不是
stoppable successor，所以整条链塌进一帧。**`join2` 没有等任何分支。**

False 的唯一来源是 `within_cycles=5` 多跑了 4 个空 cycle，而 `TakePicture → WriteMemory` 这条无触发
完成边把机器带走了。

而 prompt 又指示生产者把 `within_cycles` 按**声明边数**往上调 —— 于是「按边数」在伪状态密集的模型上
**必然过冲**。这解释了为什么失配只在被标 `pseudo` 的 pair 上密集，**与并发无关**。

## 影响面（机械复算，无需判定）

| 量 | 值 |
| :-- | --: |
| 唯一 `occupancy_after` 调用（v22+v23） | 846 |
| 其中结果为 False | 219 |
| **其中在更小 horizon 上为 True** | **51 = 23.3%** |
| 涉及的唯一 (格, kwargs) | 15 |

形态一律 `[…, True, False, False…]`。而 `_HORIZON_PROBE` 只向**上**搜（`range(asked+1, …)`），其注释
明确假设单调性（「a genuine defect does not become satisfied at a longer horizon」）—— **该假设对无
触发出边不成立**，所以这类下翻永远抓不到。

## 它推翻了我此前的两处归因

### 1. 「并发造成的 False 被标成 safe」——**归因错误**

我写过：「`bind_attribution` 把一条由**正交区并发语义**造成的 False 标成 `safe`…`join2` 是汇合伪状态、
需两条并行分支同时到达」。实跑 trace 显示整条链一个 cycle 走完，`join2` 未同步任何分支。

**那是一条假阳性发现，起因是实现缺陷，不是语义边界。** 把可修的 bug 归因成 paper1 边界外的语义，
会把「该修的东西」永久登记为「不该管的东西」。

📌 我当时读了 NL、读了模型、查了 `_reject_transient_subject` 的实现才下结论 —— **三样都做了仍然错。
缺的是实际跑一遍那个谓词。** 今天已记过「人工读原文也需要先确认原文的约定」，这里再补一层：
**读实现不等于跑实现。**

### 2. 「92 条 `unsupported_binding`」——**数字错误**

正确数（用 `count_refusals.py`）：v22 **2** / v23 **27**。我裸 grep `record.json` 得 16/92，把同一
消息在 input / output / 多轮修订里的重复都算了。且真正的主门是 `transient_subject`
（137 → 115），不是 `unsupported_binding`。

定性部分成立且更强：v23 的 27 条里 **26 条（96%）**在伪状态族的两个 pair 上。

## 修法（下一轮，可从产物直接复算）

**首选：让 `_occupies` 扫全部 cycle**，与 `_reaches_within` 对齐。这同时让 `_HORIZON_PROBE` 的单调性
假设真正成立，向上探测才有意义。

验收是一条**布尔恒等式级**的 property test：`_occupies(·, c)` 对 `c` 单调不减。预期观测量：
`horizon_down_flip` 计数从 51 降到 **0**，且 `refuse@1` 的 `horizon_probe` 桶不上升。

⚠️ 方向提醒：修它会把 51 条本该为 True 的 False 变回 True，因此会**压低 `over@1`**，同时**可能压低
`hit@k`**（有些命中是靠这些假 False 达成的）。两个方向必须分开报，不能合并成一个数。

## 待重核：12 条 `boundary` 判定

多报核验里 12 条被判 `boundary`（并发/时钟，不在断言对象内）。抽查的一条实测
`_occupies(c=1)` = True、`c=2` = False —— **`boundary` 的结论碰巧对（不算模型缺陷），机制说明是错的**。

建议对这 12 条各跑一次横轴扫描，把「末帧伪影」从「并发边界外」里分出来。**这是机械复算，不需要
人工判定。**

---

## 修法的影响上界：10 / 249 条已发布发现（4.0%）

下一轮报告必需的数字，且**无需重跑即可算**。

| 量 | 值 |
| :-- | --: |
| v23 已发布 issue | 249 |
| **其中引用 `occupancy_after` 的** | **10 = 4.0%** |
| `occupancy_after` 总调用数（v23） | 2529 |

逐 pair：`0029` 4、`0038` 3、`0018` 2、`0000` 1，其余七个 pair **各 0 条** ——
**两个可报 pair（`0035` / `0047`）各 0 条**，与代码 review 的独立结论（两条可报记录未被波及）一致。

### ⚠️ 这个 4.0% 与 review 报的 42.3% 不矛盾，分母不同

| 数 | 分母 | 含义 |
| :-- | :-- | :-- |
| 4.0%（10/249） | **已发布 issue** | 修法对发布结果的影响上界 |
| 42.3%（69/163） | **合成扫描里新增的 True** | 错误修法引入假阳性的比例 |

`occupancy_after` 被调用 **2529 次**却只支撑 **10 条**已发布发现 —— 绝大多数调用结果被别的机制吸收
（合并进其他发现、被排除、或作为 supporting 证据）。

📌 **一个谓词的调用量与它对发布结果的影响力可以差两个数量级。** 若按调用量估计修法收益，会高估
250 倍。这是「两个数的分母不同」的又一实例，只不过这次在下结论前就认出来了。

### 对下一轮的预期，写成可否证的形式

修法生效后，相对 v23 应观察到：

1. `occupancy_after` 相关的已发布发现数变化**不超过 ±10 条**（上界由本节给出）
2. `unaccounted_safe_false_assertions` 那条（v23 有 1 条）**应消失** —— 它正是被误记为「并发造成的
   False」的那条
3. 两个可报 pair 的 `hit@k` 序列**不应改变** —— 它们各 0 条 `occupancy_after` 引用

第 3 条最要紧：**若可报带的序列变了，说明修法有我没预料到的路径，必须先查清再报。**
