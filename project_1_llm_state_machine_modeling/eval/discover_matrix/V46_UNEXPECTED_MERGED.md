# v46 意外发现归并后的问题清单

⚠️ **本文件的簇级数字由 [unexpected_verdicts/](./unexpected_verdicts/) 的 `G*.jsonl` 汇出，jsonl 是真源。**

簇不是缺陷。同一个缺陷会以不同谓词、不同命名、不同 roll-up 粒度反复产出，
本文件把 293 簇按**根因**归并。逐簇判据见 [V46_UNEXPECTED_EVIDENCE.md](./V46_UNEXPECTED_EVIDENCE.md)，
结论与交叉表见 [V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md)。

## 一、✅ 真实台账漏记（6 条根因 / 26 簇）

归并比 4.3:1。**这 6 条是 v46 相对台账的净增量，也是唯一应当补进台账的部分。**

### `0017-FUSE` — pair 0017　（8 簇归并）

**缺陷**：作者两个区都只写泛化 `collision detected`，NL 2 点名的三种检测被塌缩成一个刺激

**作者源判据**：`stm0.puml:4` `[*] --> F : collision detected`；`:9` `[*] --> R : collision detected`。对照同一份 NL 的 pair 0057，作者分立写全 `Frontend collision detected` / `Rear-end collision detected` / `Pedestrian collision detected`——证明三者可分是该 NL 的通行读法，不是过度指定。0017 台账 0 条。

**并入的簇**：`0017-1`, `0017-2`, `0017-3`, `0017-4`, `0017-5`, `0017-6`, `0017-9`, `0017-11`

**稳定性**：各簇出现 1→2/6, 2→1/6, 3→2/6, 4→2/6, 5→1/6, 6→1/6, 9→1/6, 11→1/6
（最高 2/6 格 —— 未达 ≥4 格，属不稳定发现）

### `0047-FUSE` — pair 0047　（8 簇归并）

**缺陷**：作者三个区都只写泛化 `Collision Detected`，同 0017

**作者源判据**：`stm0.puml:5,12` 均为 `Idle --> Braking : Collision Detected`。CAS 下有三个子态，单一 `Collision_Detected` 无法决定进哪一个。不依赖并发语义，在 M 边界内。

**并入的簇**：`0047-1`, `0047-2`, `0047-3`, `0047-4`, `0047-5`, `0047-6`, `0047-7`, `0047-8`

**稳定性**：各簇出现 1→1/6, 2→1/6, 3→1/6, 4→1/6, 5→3/6, 6→3/6, 7→2/6, 8→1/6
（最高 3/6 格 —— 未达 ≥4 格，属不稳定发现）

### `0023-REGION` — pair 0023　（6 簇归并）

**缺陷**：三个替代子态被写成三个并发区的默认入口，区间零迁移

**作者源判据**：`stm0.puml:4-8` 内 PumpControl 只有 `[*] --> PumpState` / `[*] --> WaterState` / `[*] --> MethaneState` 三条初始迁移，无任何区间迁移，且全模型未声明任何 event。NL 3「first transitions to the PumpState」加 NL 4/5「can also transition to」要求运行期可切换。判定只用 Tr 层事实，不依赖并发语义。台账 0 条。

**并入的簇**：`0023-1`, `0023-2`, `0023-3`, `0023-7`, `0023-8`, `0023-9`

**稳定性**：各簇出现 1→1/6, 2→1/6, 3→1/6, 7→3/6, 8→1/6, 9→1/6
（最高 3/6 格 —— 未达 ≥4 格，属不稳定发现）

### `0022-EXTRA` — pair 0022　（2 簇归并）

**缺陷**：自增顶层态 `PoweredOn`，上电未直达 `Operate`

**作者源判据**：`stm0.puml:2-3` `[*] --> PoweredOn` / `PoweredOn --> Operate: start`。NL 1「Once the device is powered on, the system enters the `Operate` state」要求上电即进 Operate，模型需再吃一个 start。保留意见：NL 2 的 keyOff 隐含需要一个关机去处，但作者把该态命名为 PoweredOn 使矛盾坐实。台账 0 条。

**并入的簇**：`0022-2`, `0022-3`

**稳定性**：各簇出现 2→1/6, 3→1/6
（最高 1/6 格 —— 未达 ≥4 格，属不稳定发现）

### `0014-ACT` — pair 0014　（1 簇归并）

**缺陷**：NL 3「发出 Obstacle Detected 信号」被降级成状态描述行

**作者源判据**：`stm0.puml:26` 写 `EmergencyStopping: Obstacle Detected`（PlantUML 状态描述行），对照同一份 NL 的 pair 0054 作者写 `EmergencyStopping : do/Send Obstacle Detected`（真动作），0004 写 `during abstract SendObstacleDetected`——证明该输出动作在 M 内可表达且是参考意图。台账已记同族 EIS-0014-03（Emergency Stop）与 EIS-0014-04（Send），独漏此第三条。

**并入的簇**：`0014-4`

**稳定性**：各簇出现 4→2/6
（最高 2/6 格 —— 未达 ≥4 格，属不稳定发现）

### `0057-ENTRY` — pair 0057　（1 簇归并）

**缺陷**：CA 入口用作者自造的聚合事件，单一具体检测无法激活 CA

**作者源判据**：`stm0.puml:22` `[*] --> CA : Possible collision detected`。三个具体检测事件只落在 CA 各子区的 Idle→Active 上，CA 自身入口不消费它们，故「只检测到前向碰撞」无法激活 CA，与 NL 2 冲突。⚠️ 保留意见：谓词形式 `event_consumed(source=CA)` 是「进入 CA 的义务」的弱代理（进入 CA 的边源在 CA 之外），形式不精确但实质结论成立。

**并入的簇**：`0057-1`

**稳定性**：各簇出现 1→2/6
（最高 2/6 格 —— 未达 ≥4 格，属不稳定发现）

## 二、🔗 应并入已有台账（10 条根因 / 14 簇）

**这些不是漏记，是匹配环节的问题**：台账已有该缺陷，但产出换了个谓词或换了个命名，
按签名归并的匹配器就对不上了。典型是 `terminates` → `persists_until`。

| 簇 | 应并入 | 理由 |
| :-- | :-- | :-- |
| `0006-2` | EIS-0006-03[terminates] | 同为「无终态、无完成事件、永不可结束」，换谓词表述 |
| `0006-3` | EIS-0006-02[effect_declared] | 台账记效应侧，本簇记声明侧，同一缺陷两面 |
| `0007-1` | EIS-0007-01 / EIS-0007-03 | 直接子数≠3 完全由这两条已记缺陷造成，属计数侧面 |
| `0016-11` | EIS-0016-03[terminates] | 同上 |
| `0016-2` | EIS-0016-03[terminates] | mission-complete 缺失即该条，匹配环节未对上 |
| `0026-4` | EIS-0026-02 | 计数量缺失是该条已记缺陷的变量侧面 |
| `0035-1` | EIS-0035-04[A] | 复核确认其 nl_evidence 逐字引用 NL 5「cooking time is displayed and updated」 |
| `0035-2` | EIS-0035-04[A] | 其 nl_evidence 逐字引用 NL 7「the timer starts」 |
| `0036-8` | EIS-0036-02[terminates] | 换谓词 terminates→persists_until |
| `0037-1` | EIS-0037-01[reaches] | 多出的子状态正是该条所指的死端叶 |
| `0047-9` | EIS-0047-03 | 未激活外部上下文缺失是该条的结构侧面 |
| `0050-2` | EIS-0050-01 | 接管条件融合，签名被标为 state_declared 故未匹配 |
| `0050-3` | EIS-0050-01 | 同上 |
| `0050-4` | EIS-0050-01 | 同上 |

## 三、⚙️ 表示债务（4 个子类 / 111 簇）

**不是模型缺陷，是我们自己 R4.5 编译的信息损失。** 详见 [V46_UNEXPECTED_ADJUDICATION.md §一之二](./V46_UNEXPECTED_ADJUDICATION.md)。

| 子类 | 簇数 | 涉及 pair | 作者源实际写法 |
| :-- | --: | :-- | :-- |
| `D2` 析取守卫被压成单一事件名 | 64 | 0009, 0019, 0027, 0029, 0039, 0049, 0059 | `a \| b & c \| d` 一条合法析取守卫 |
| `D1` 守卫文本未成为变量声明 | 38 | 同上 + 0000 0010 0020 0030 0050 | `Front Distance > 10` 写在守卫里；PlantUML 无变量声明语法 |
| `D3` `trigger / effect` 未切分 | 7 | 0016 0046 0056 | `Attack Complete / UAV Count Decreased` |
| `D4` 注入伪态 / 区语义偏移 | 2 | 0043 等 | 作者写了合法的区内 `[*]`，R4.5 另注入 `UnspecifiedInitial` |

逐 pair 簇数：0000×1、0009×1、0010×1、0016×8、0019×19、0020×1、0027×11、0029×20、0030×1、0039×16、0043×1、0046×5、0049×14、0050×1、0059×11（合计 111）

## 四、其余非发现（142 簇）

`无 NL 依据` 90 + `假阳性` 43 + `越界` 4 + `待定` 5 = 142。子类分布见主文档表 C，逐簇判据见证据附件。

**其中 `N0`（4 簇）需单独跟进**：`0054-1` `0054-5` `0046-8` `0026-3` 的义务来自谓词被操作化的方式而非 NL，
`0054-5` 是构造性不可满足（NL 2/10 恰恰许可该迁移，谓词却禁止），属 CLAUDE.md §13 类缺陷。

**`0056-1` 已裁定 `OUT_OF_SCOPE`**（R-REGION 规则，见 [V46_UNEXPECTED_ADJUDICATION.md §三](./V46_UNEXPECTED_ADJUDICATION.md)）：
作者源 `stm0.puml:10` 是正交区分隔符，region 0 恰为三个 Area，NL 义务已满足；5≠3 系拍平后跨区求和。
