# v25 提案：两处改动，各有独立可观测签名

前两次 v25 尝试都被运行前 review 判禁止开跑（见
[V25_SYNTHESIZED_PLACEHOLDER_PROPOSAL.md](./V25_SYNTHESIZED_PLACEHOLDER_PROPOSAL.md) 开头）。
本提案的两处改动都**不在**上次被否的那条通路上。

## 零、先给上限：为什么这两处是当前最大的杠杆

按层拆当前覆盖（干净装置两标注者保守合并，204 位）：

| 层 | 命中 | 位数 | `hit@1` |
| :-- | --: | --: | --: |
| `nl_named` | 62 | 102 | 60.8% |
| `wellformedness` | 28 | 72 | 38.9% |
| `over_specification` | 6 | 12 | 50.0% |
| `nl_contradiction` | 14 | 18 | 77.8% |
| **合计** | **110** | **204** | **53.9%** |

9 条记录全 0（54 位）= 当前词表下的能力上限之外，故**天花板 = 150/204 = 73.5%**。

我逐条人工读了这 9 条与 12 条部分命中记录，并把三个候选杠杆量化到位：

| 候选杠杆 | 实测位数 | 结论 |
| :-- | --: | :-- |
| 判据：合并 issue 造成的低估 | ~1–3 | 改动 ① 针对它 |
| 判据：`boundary` 过宽 | **2**（9 条候选里 7 条是计时主张，**判对了**） | 小，本轮不改判据 |
| **词表：无触发边不可断言** | **12（≈6pp）**，且解锁语料 **134/290 = 46%** 的迁移 | 改动 ② |

## 一、改动 ①：`prompts.py` L104 消歧（issue 粒度）

### 实测依据

追踪 `EIS-0043-02` 在 pair 0043 的 claude/R1 与 R3：**同一条封存断言逐字相同**，但

| 轮 | 发布的 issue |
| :-- | :-- |
| R1 | ① 三个业务子状态被错误嵌入 Region1 并发区域层<br>② PumpControl 的初始目标不是 PumpState，而是 UnspecifiedInitial |
| R3 | ① 引入了多余的 Region 层级…**且默认入口被替换为 UnspecifiedInitial** ← 两条并入一条 |

**R3 报了这个缺陷，只是打包了。** 一标签制度下另一条被记漏检。

### 这是一处真的跨阶段矛盾（三条都读了完整原文）

| 行 | 阶段 | 逐字 |
| --: | :-- | :-- |
| 360 | Splitter | Split independently violable mixed modalities into separate Requirements… **"X is a substate of Y and entering Y starts at X" is two claims (`containment`, `initial_target`) and must become two Requirements** |
| 437 | Adjudicator | a False assertion whose role is `primary`… may create a confirmed issue — **and must** |
| 104 | Adjudicator | **group evidence that reports the same underlying model defect** |

L360 的例子**逐字就是 0043 那一对**。L437 用 `must`，L104 用 `group`，**没有任何一处调和它们**。
R3 的合并是在遵守 L104。

⚠️ **与前两次「跨阶段矛盾」主张的区别**：那两次我漏读了 L379 的析取支，矛盾是我造的；
**这三条都是无条件祈使句，且我读了各自的完整行文。**

### 改法：改 L104 自己那一句，不新增第六处

> …supporting evidence is routed by the deterministic layer and must not appear in an issue.
> **Grouping operates on the evidence inside one issue; it never merges two False primaries into
> one issue. Requirements were split upstream precisely because their claims are independently
> violable, so two such primaries stay two issues even when a single model edit would repair
> both: a shared root cause is not the same claim.**

**是消歧，不是改政策** —— L437 已用 `must` 要求每个 False primary 建 issue。

## 二、改动 ②：新增谓词 `untriggered_edge_declared(source, target)`

### 实测依据

| 检查 | 结果 |
| :-- | :-- |
| `edge_declared` 签名 | `(source, trigger, target)`，**三者必填** |
| 无触发哨兵 `""` / `None` | `UnsupportedEvidence: must be a non-empty path` |
| `"[*]"` | 保留给伪初始，拒 |
| `"-"` / `"None"` | 名字不合式，拒 |
| 省略参数 | `TypeError` |
| **矩阵语料无触发迁移** | **134 / 290 = 46%** |
| 19 谓词中不需 trigger 又能定位单条边的 | **无**（`reaches` 是传递可达，表达不了「哪条边」） |

即：**声明里近一半的迁移不能成为任何声明类谓词的主体。**

### ⛔ 为什么不给 `edge_declared` 传 `event=None`（那是更小的改动，也是错的）

`structure.transitions` 把 `None` 过滤器当作**未设置**，于是该调用会匹配**任意**触发的边 ——
把 False 变成 True，**静默撤回当前成立的发现**。这正是上一轮 review 的 C2 那一类。
**新名字使现有调用一字不动。**

### 极性写死（上一轮 C1 的直接回应）

docstring 逐字：「As with every declaration predicate the **False** is the finding」。
三个对照已实测：

    真实无触发边            -> True   （正对照）
    未声明的边              -> False  （负对照，即发现）
    存在但**带触发**的边     -> False  （⭐ 关键负对照：不得把带触发边算进来）

### 五个登记点全部落实（仓库合同测试逐个逼出）

`predicate_api.py` 实现 → `PREDICATE_FAMILIES`（求值命名空间）→ `predicates.py` 词表 →
`capability.py` 归因 → 三份合同 fixture。

**`make test`：1645 passed / 4 skipped**（基线 1599，新增 46 条含合同参数化）。

## 三、公平性自审

### 抽象化测试

- 改动 ① 陈述的是**两个已有阶段之间的契约**（拆开的义务不得在裁决时并回），不含 pair 号、状态名、
  期望缺陷、期望真值、判定结论。
- 改动 ② 是一个**谓词签名**，其 docstring 讲的是工具行为与极性，**不讲任何缺陷在哪**。

### ⛔ 按引入动机反向标注

| 改动 | 动机 | 不可计入能力的记录 |
| :-- | :-- | :-- |
| ① | pipeline **自相矛盾**（R1 做对、R3 做错，同模型同断言）—— 不是「某条记录没被发现」 | 保守起见排除 `EIS-0043-02` |
| ② | 探测 `edge_declared` 哨兵处理时测出 46% 缺口；但**探测由 `EIS-0048-04` / `EIS-0038-02` 引起** | 排除 `EIS-0048-04`、`EIS-0038-02` |

**这三条记录在 v25 的结果不计入发现能力**，只作「方法 + 样本共同演化」观测。
改动 ② 的能力主张落在其余无触发边上（134 条迁移横跨全部 11 pair）。

### 激活面（⚠️ 回测，测误伤面不测通用性）

无触发迁移逐 pair：`0000` 2/8、`0006` 7/11、`0018` 13/22、`0029` 15/70、`0032` 16/37、`0035` 1/16、
`0038` 13/21、`0043` 4/10、`0047` 9/26、`0048` 48/52、`0050` 6/17 —— **11/11 个 pair 都有**。
按记忆纪律，这只说明它不会只在一个 pair 上生效，**不证明通用**；通用性只能由活体运行判定。

## 四、⚠️ 这是**两变量**运行，但两个变量的可观测签名互斥

| 变量 | 独立签名 | 归因方式 |
| :-- | :-- | :-- |
| ① L104 消歧 | **每格 issue 数上升**，且新增 issue 与已有 issue 共享根因 | 比对 v24/v25 同格 issue 数与引用的 primary id |
| ② 新谓词 | **`untriggered_edge_declared` 出现在断言脚本中** | 计数该谓词的调用；v24 为 0（谓词不存在） |

**若覆盖率上升而该谓词调用数为 0，则增益全部归 ①；反之可分离。**

## 五、预注册判读条件（跑之前写死，含上一轮漏掉的那一行）

| 观察 | 判读 |
| :-- | :-- |
| ⭐ **任何当前命中的记录变为漏检** | **净负面**，须逐条定位；上一轮预注册漏了这一行 |
| `untriggered_edge_declared` 调用数仍为 0 | 改动 ② **未生效**，是词表说明或 prompt 引导问题，非能力问题 |
| 三条动机记录命中上升 | **不计入能力证据**（动机已烧掉） |
| 非动机记录出现新命中 | 弱正面信号 |
| 每格 issue 数上升而多报（`fabricated` / `grounded-extra`）同步上升 | 改动 ① **过宽**，拆得太碎，须收窄 |
| 修订轮数显著上升 | 规则制造了 reviewer 争议，净负面 |
| 覆盖率上升但集中在 1 个 pair | 疑特化，须逐 pair 报 |

## 六、不在本轮范围内（已定位，留待后续）

| 项 | 需要什么 |
| :-- | :-- |
| `wellformedness` 层 8/12 属「工具已报」 | 收窄能力分母，见 [WELLFORMEDNESS_ATTRIBUTION_RULING.md](./WELLFORMEDNESS_ATTRIBUTION_RULING.md)；需独立核验 + 双份口径 |
| 伪状态 join/junction 类型错配（`EIS-0038-07` / `EIS-0048-05`） | `state_declared` 的 kind 词表扩张 |
| 事件粒度（`EIS-0000-02`） | `event_cardinality`，见 [FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md) §四 |
| over-specification 的存在性否定（`EIS-0018-03`） | 词表只有正向存在性谓词 |
| `boundary` 过宽 2 位 | 判据措辞，本轮不动判据以免与运行结果混淆 |
