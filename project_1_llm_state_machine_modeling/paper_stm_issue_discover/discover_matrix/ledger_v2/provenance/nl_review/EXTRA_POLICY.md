# `extra` 能否入 E1：判据应是可归因性 + 有害性，不是开/闭世界

复核 NL04/10 时提出一个会同时决定全部 **31 条 `extra`** 的政策问题：`0035`#2 的 `DoorOpen --> DoorOpen : Item Removed` 自环，NL 从未把该事件挂在 `DoorOpen` 上（第 3 句 "If the item is removed, the system returns to DoorOpen" 的 "returns to" 蕴含源态是 `DoorOpenWithItem`，而 gen 已另有一行满足它）。该 diff 是否可入 E1，被表述为取决于：

- **闭世界读法**：NL 八句已穷举全部迁移，多出的自环即违规 → 可入
- **开世界读法**：NL 未禁止追加迁移 → 不可归因 → 不可入

## 两者都不是正确判据

开/闭世界是对 NL 的**语义假设**，而 expected issue 要回答的是另一个问题：**这条差异能否作为「方法应当检出的作者源缺陷」**。

闭世界站不住：原论文的需求模板明确禁止在 NL 里写元素个数与元素间关系（"Requirements must avoid explicitly stating the number of elements or inter-element relations"），所以 NL **在设计上就不穷举**。把它当穷举读，等于假设一个作者刻意避免的性质。

开世界也站不住：它会把**全部 31 条 extra 一律划为不可归因**，而其中包含 `0007`#3 那种「整棵子树 NL 完全未提及、且无任何入边（死代码）」——那显然是生成方的缺陷。

## 正确判据：可归因 ∧ 有害

`extra` 的**可归因性无争议**：参考没有、NL 没点名、只有生成方有它，来源唯一。所以真正要分的是**有害性**——它是否造成可断言的负面后果：

| 类型 | 判据 | 入 E1 |
| --- | --- | :-: |
| **有害的 over-specification** | 造成不可达 / 死端 / 冲突目标 / 抢占已声明分支 / 语义偏移，任一后果**可用 19 谓词写出正面断言** | ✓ |
| **无害的装饰性增补** | 只是多一个可达状态上的自环、或一个不影响任何路径的旁支，写不出「因此坏了什么」 | ✗ |

按此判据，`0035`#2 **不可入**：可达状态上的带触发自环不造成不可达、不抢占任何已声明分支（它带触发，不是 completion 边），写不出有害后果。而 `0007`#3 **可入**：死代码 + 同区三条初始迁移，`reaches` 与 `initial_target` 都能断言。

这个判据的好处是它**与 NL 的世界假设无关**，只依赖生成模型自身可判定的后果——与 `wellformedness` 层同源，因此同样难被反驳。

## 落地方式

`over_specification` 层需按有害性再切一刀。判据可机械近似：该 diff 的 `assertable` 是否给出了一条能表达负面后果的断言（`reaches` / `terminates` / `initial_target` / `occupancy_after` 等行为类），而不只是「该元素存在」（`state_declared` / `edge_declared` 的存在性断言）。

存在性断言只能证明「生成方造了它」，不能证明「因此坏了什么」——对 `extra` 而言前者是前提、后者才是缺陷。
