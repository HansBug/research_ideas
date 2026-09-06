# 谓词层的实测观测与已发布判定

从 `assertions/predicate_api.py` 的 docstring / 注释里移出的**计数与判定**。移出理由见 [docs/protocol/rule_provenance.md](../../protocol/rule_provenance.md)「结果邻接类文件」一节：那些文件是公理推导的必读项，含实验结果会污染规则编写侧。

## 判别标准（本次执行时修正过一次）

| 类别 | 处置 | 例 |
| :-- | :-- | :-- |
| **计数** | **移出** | 「60 of 60 pairs」「22 of the corpus's 169 composites」「51 of 219 False」 |
| **判定** | **移出** | 「matrix-v16 published one as a confirmed defect」「EXP-0000-IT-001」 |
| **定位** | **保留在 docstring** | 「measured on pair 0018」「pinned at pair 0000's root」 |

⚠️ **原标准是「保留为什么这样实现、移出在哪些样本上观测到多少」，执行时发现它会把定位一起移走。**

定位类（16 行）兼有机制说明作用：它告诉后来者**去哪里能重现这个行为**。移走它会降低可维护性 ——下一个改 `_occupies` 的人失去了「在 0018 上能看到」这个入口。

**修正后的标准是：移出计数与判定（多少个、发布了没有），保留定位（在哪能看到）。** 前者是结果，后者是复现指引。

## 移出的 9 处

### `_require_well_formed_names`（原 L331）

第三条 seal path 的实测约束面：**60 / 60 个 pair 上都不构成约束**（即它从未拦下任何东西）。

### `_reject_transient_subject`（原 L465）

v20 hold-out 集上，同一形状（对瞬时伪状态发问）**产生了 17 条已发布发现**，落在 `0018` 与 `0038`。

⚠️ 该函数 docstring 里另一条**保留**的观测更重要且属于定位类：语料对 `pseudo` 关键字的标注**不一致**（`0018` 标了九个路由结点、`0048` 标了两个、`0038` 一个没标）。它是「用规则检测语料自身不一致」这类错误的实证，[docs/generations/v25/wellformedness_axioms.md](../../generations/v25/wellformedness_axioms.md) §二③ 据此剔除了一条候选公理。

### `_settle_cycles`（原 L511）

**matrix-v16 把其中一个 settle 链发布为确认缺陷**：`0050` 的 `AutonomousMode` 沿 `SubState1 -> SubState2 -> …` settle 2 到 7 条边深。

### `_initial_child_of` 的 `field` 内联（原 L945、L976）

- 谓词曾在 **22 / 169 个语料复合态**上拒答。
- 绑定回报 `safe` 而 **matrix-v16 发布了两条**，同时把 `0029` 的同形态排除为表示债 —— 口径不一致。

### `occupancy_after`（原 L1242、L1251）

- 「这道门本该拦下的失败」没有任何门拦下，而 **matrix-v17 在第一个完成的格上就发布了一条**（`0006`）。
- 两条已发布发现 **`EXP-0000-IT-001`** 与 **`EXP-0029-IT-001`** 在每个 horizon 上都是 False。

### `_occupies`（原 L1299）

横轴非单调这个缺陷被发现前的两项代价：跨 **v22+v23** 共 **51 / 219** 个 False 结果（**23.3%**）在更小的 horizon 上为 True，每一个都作为发现发布了。

📌 该缺陷的完整分析（含它曾被误归类为语义边界）见 [docs/generations/v24/predicate_bottleneck.md](../../generations/v24/predicate_bottleneck.md) 与 `defects_registered.md`。

### `terminates`（原 L1665）

**matrix-v16 的 `terminates` 调用未受那次顺序缺陷影响。**

## 与其他文档的分工

| 文档 | 内容 |
| :-- | :-- |
| 本文件 | 谓词层的**计数与已发布判定**（从 docstring 移出） |
| [docs/generations/v24/predicate_bottleneck.md](../../generations/v24/predicate_bottleneck.md) | 逐谓词诊断、三个被推翻的假设、两条廉价判据 |
| [docs/generations/v25/wellformedness_axioms.md](../../generations/v25/wellformedness_axioms.md) | 公理表、三项裁决、冻结条件 |
| `predicate_api.py` 的 docstring | **机制说明 + 定位**（为什么这样实现、在哪能重现） |
