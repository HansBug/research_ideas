# `Umple` 本地工具链复现实验：优先打通 `Umple -> Python` 与 `Umple -> NuSMV` 直链，再补 `Alloy`

## 1. 这份讨论要回答什么

这份讨论不是继续做“纸面上的相关工作比较”，而是记录一次**真正本地跑通**的 `Umple` 工具链复现实验，目标是回答下面几个具体问题：

1. 当前这台机器上，`Umple` 命令行环境能不能配起来。
2. 能不能基于官方例子，得到一个**直接实现** `Umple -> Python` 和 `Umple -> NuSMV -> verification` 的样例。
3. 在这个基础上，能不能再补一个更接近 `project_1` 需求的 richer 样例，把层次状态、guard、effect、结构约束以及 `Alloy` 也接起来。
4. `NuSMV` / `Alloy` 的原始导出各自卡在哪里，哪些地方可以直接用，哪些地方必须做后处理。
5. 能不能把所有环境、命令、文件、性质、输出、坑点都记录清楚，后面直接照着复现。

## 2. 最终结论

先给结论：

1. `Umple` 本地命令行环境已经在这台机器上跑通，采用的是**用户态安装**而不是系统级安装。
2. `Java` 按要求使用了 `jenv` 管理，实验目录固定到 `Temurin 17.0.18`。
3. 我最终采用了**两个例子**而不是一个例子来分别回答不同问题。
4. 例子 A 使用官方 `Basic Garage Door Example`，它已经实现了真正的**直接链路**：
   `Umple -> Python` 可运行，`Umple -> NuSMV` 的**原始导出**可直接检查 `CTL`，再通过 `NuSMV` 命令脚本对**同一个 raw `.smv`** 追加 `CTL/LTL` 检查，不需要语义修补。
5. 例子 B 使用官方 `RequirementsExamples` 中的 `Drivers Licence` 需求改写模型，它更适合承载层次状态、guard、effect、恢复路径、结构关系和 `Alloy` 检查。
6. 例子 B 的 `Python` 导出可以直接运行，`Alloy` 原始导出也能直接被读入，但 `NuSMV` 原始导出**不是 verification-ready**，需要补一个 verification wrapper。
7. 因而，这次实验的稳定结论不是“`Umple` 不行”，而是：
   `Umple` 作为可执行建模 DSL 和多后端导出入口是可用的，但如果要把它接成 `project_1` 所需的稳定“生成-验证闭环”，必须区分：
   一个较小的可直接链路子集；以及一个 richer 但需要 profile/后处理的子集。

## 3. 这次实验使用了哪些来源

### 3.1 仓库内材料

1. 最新相关讨论：[2026-04-14-23-03-54-AI-讨论-pyfcstm作为LLM建模论文目标形式的必要性与Umple-rebuttal口径.md](./2026-04-14-23-03-54-AI-讨论-pyfcstm作为LLM建模论文目标形式的必要性与Umple-rebuttal口径.md)
2. `Umple` baseline 单篇分析：[../baselines/umple/DESC.md](../baselines/umple/DESC.md)
3. `Umple` baseline 原文目录：[../baselines/umple/](../baselines/umple/)

### 3.2 官方资料

1. `Umple Tools`: <https://cruise.umple.org/umple/UmpleTools.html>
2. `Python` 生成器说明: <https://cruise.umple.org/umple/Python.html>
3. `NuSMV` 生成器说明: <https://cruise.umple.org/umple/NuSMV.html>
4. `Alloy` 生成器说明: <https://cruise.umple.org/umple/Alloy.html>
5. 官方基础状态机例子页 `BasicStateMachines`: <https://cruise.umple.org/umple/BasicStateMachines.html>
6. 官方需求例子页 `RequirementsExamples`: <https://cruise.umple.org/umple/RequirementsExamples.html>

## 4. 为什么这次要拆成两个例子

一开始我只做了一个 richer 的 `Drivers Licence` 样例，但后面发现这样有一个表达问题：

1. 它很适合说明 `Umple` 能建比较像样的状态机模型。
2. 它也适合说明 `Python` 和 `Alloy` 能接起来。
3. 但它恰好又暴露了 `NuSMV` 原始导出的限制。

如果只保留它，那么最后讨论很容易退化成“`Umple -> NuSMV` 不太行”。这不够准确。

所以我又补了一个更小的官方例子 `GarageDoor`，专门用来回答另一个更基础的问题：

> 能不能找到一个官方状态机样例，让 `Umple -> Python` 和 `Umple -> NuSMV -> verification` 作为**直接链路**真正跑通？

答案是：**可以**。

于是现在的实验分成两层：

1. **例子 A：`GarageDoor`**
   用来证明 raw direct chain 可以成立。
2. **例子 B：`Drivers Licence`**
   用来证明 richer state machine + structure + `Alloy` 可以成立，同时暴露 raw `NuSMV` 导出的真实边界。

## 5. 实验资产放在哪里

本次实验所有资产都收敛在一个单独目录里：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/](../baselines/umple/reproduction-2026-04-15-local-toolchain/)

其中关键文件分两组。

### 5.1 例子 A：`GarageDoor` 直链样例

1. 模型文件：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/garage_door_direct.ump](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/garage_door_direct.ump)
2. 生成的 `Python` 类：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/generated/python/Reproduction/DirectGarageDoor/GarageDoor.py](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/generated/python/Reproduction/DirectGarageDoor/GarageDoor.py)
3. 原始 `NuSMV` 导出：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/garage_door_direct.smv](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/garage_door_direct.smv)
4. `Python` demo 脚本：[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_garage_door_python_demo.py](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_garage_door_python_demo.py)
5. `NuSMV` 命令脚本：[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/garage_door_direct_nusmv_commands.txt](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/garage_door_direct_nusmv_commands.txt)

### 5.2 例子 B：`Drivers Licence` richer 样例

1. 官方需求改写版：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_requirements.ump](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_requirements.ump)
2. 主模型文件：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.ump](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.ump)
3. 生成的 `Python` 类：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/generated/python/Reproduction/DriverLicense/Applicant.py](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/generated/python/Reproduction/DriverLicense/Applicant.py)
4. 原始 `NuSMV` 导出：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.smv](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.smv)
5. 可验证版 `NuSMV` 文件：[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/driver_license_verified.smv](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/driver_license_verified.smv)
6. 原始 `Alloy` 导出：[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.als](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.als)
7. `Alloy` 检查文件：[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/alloysrc/driver_license_check.als](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/alloysrc/driver_license_check.als)
8. `Python` demo 脚本：[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_driver_license_python_demo.py](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_driver_license_python_demo.py)

### 5.3 统一入口

1. 一键复现脚本：[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/reproduce.sh](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/reproduce.sh)
2. 日志目录：[../baselines/umple/reproduction-2026-04-15-local-toolchain/logs/](../baselines/umple/reproduction-2026-04-15-local-toolchain/logs/)

## 6. 本地环境是怎么配起来的

### 6.1 总体策略

一开始尝试系统级安装，但当前机器 `sudo` 需要交互式密码，因此最后采用了**用户态安装**。这样反而更适合复现实验，因为版本都固定在实验目录中。

### 6.2 Java：按要求使用 `jenv`

用户额外要求“`java` 用 `jenv` 安装”，所以这次 Java 环境是这样处理的：

1. 安装 `jenv` 到 `~/.jenv`
2. 在 `~/.bashrc` 中追加 `jenv` 初始化
3. 下载 `Temurin 17.0.18`
4. 通过 `jenv add` 纳管
5. 在实验目录下写入 `.java-version`

实验目录实际使用的 Java 版本如下：

```text
openjdk version "17.0.18" 2026-01-20
OpenJDK Runtime Environment Temurin-17.0.18+8
OpenJDK 64-Bit Server VM Temurin-17.0.18+8
```

### 6.3 本次实际使用的版本

1. `Umple`: `1.36.0.8155.852949be7`
2. `FreeTXL`: `10.8b`
3. `NuSMV`: `2.6.0`
4. `Alloy`: `6.2.0`

### 6.4 这里最重要的两个环境坑

1. `Python` 生成器确实依赖 `FreeTXL`
   如果没有 `txl`，`Python` 生成链不会完整工作。
2. 官方 `NuSMV 2.7.1` Linux 二进制在这台 `Ubuntu 20.04` 上不能直接用
   它依赖更高版本的 `GLIBC` 和 `libedit.so.0`，所以这次最终使用的是 `NuSMV 2.6.0`。

## 7. 例子 A：官方 `GarageDoor` 直链样例

### 7.1 为什么选它

我最终把它作为“直链样例”的原因非常简单：

1. 它是官方 `BasicStateMachines` 页面上的标准例子，不是我自己编的。
2. 它只有纯控制状态和事件，没有额外数据语义，非常适合测试 raw `NuSMV` 导出能不能直接用。
3. 它足够小，方便直接看清 `CTL/LTL` 结果和 counterexample。

### 7.2 实际使用的 `Umple` 模型

模型文件在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/garage_door_direct.ump](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/garage_door_direct.ump)

实际模型如下：

```umple
namespace Reproduction.DirectGarageDoor;

class GarageDoor
{
  status {
    Open {
      buttonOrObstacle -> Closing;
    }

    Closing {
      buttonOrObstacle -> Opening;
      reachBottom -> Closed;
    }

    Closed {
      buttonOrObstacle -> Opening;
    }

    Opening {
      buttonOrObstacle -> HalfOpen;
      reachTop -> Open;
    }

    HalfOpen {
      buttonOrObstacle -> Opening;
    }
  }
}
```

### 7.3 导出命令

```bash
cd project_1_llm_state_machine_modeling/baselines/umple/reproduction-2026-04-15-local-toolchain
java -jar tooling/umple.jar -g Python --path generated/python models/garage_door_direct.ump
java -jar tooling/umple.jar -g NuSMV models/garage_door_direct.ump
```

### 7.4 `Python` 运行结果

`Python` demo 脚本在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_garage_door_python_demo.py](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_garage_door_python_demo.py)

运行命令：

```bash
python3 verification/run_garage_door_python_demo.py
```

实际输出如下：

```text
initial: state=Open
after_close_start: state=Closing
after_closed: state=Closed
after_open_start: state=Opening
after_halfopen: state=HalfOpen
after_reopen: state=Opening
after_open: state=Open
garage_python_demo_ok
```

这说明 `Umple -> Python` 对这个官方例子是直接可执行的。

### 7.5 原始 `NuSMV` 导出已经自带的 `CTL` 性质

这里有一个很重要的发现：

`garage_door_direct.smv` 的**原始导出文件**本身就已经自带了若干 reachability `CTLSPEC`，即检查非 symbolic state 是否可达。

也就是说，下面这个命令就已经是一个成立的“直接链路”：

```bash
./tooling/nusmv-2.6.0-linux64/bin/NuSMV models/garage_door_direct.smv
```

实际输出如下：

```text
-- specification EF garageDoorStatus_Machine.garageDoorStatus.state = Status_Open  is true
-- specification EF garageDoorStatus_Machine.garageDoorStatus.state = Status_Closing  is true
-- specification EF garageDoorStatus_Machine.garageDoorStatus.state = Status_Closed  is true
-- specification EF garageDoorStatus_Machine.garageDoorStatus.state = Status_Opening  is true
-- specification EF garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen  is true
```

这五条都是 raw generated model 自带的 `CTL` 检查结果，不需要我手改模型语义。

### 7.6 在 raw `.smv` 上追加 `CTL/LTL` 检查

为了证明不仅能跑通“默认 reachability”，也能在**同一个 raw `.smv`** 上继续做自定义验证，我又写了一个 `NuSMV` 命令脚本：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/garage_door_direct_nusmv_commands.txt](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/garage_door_direct_nusmv_commands.txt)

脚本内容如下：

```text
go
check_ctlspec -p "EF (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen)"
check_ctlspec -p "AG !(garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen)"
check_ltlspec -p "G (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen -> X (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen | garageDoorStatus_Machine.garageDoorStatus.state = Status_Opening))"
check_ltlspec -p "G (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen -> F (garageDoorStatus_Machine.garageDoorStatus.state = Status_Open))"
quit
```

执行命令如下：

```bash
./tooling/nusmv-2.6.0-linux64/bin/NuSMV -source verification/garage_door_direct_nusmv_commands.txt models/garage_door_direct.smv
```

### 7.7 `GarageDoor` 的 `CTL/LTL` 检查输出

实际输出如下：

```text
-- specification EF garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen  is true
-- specification AG !(garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen)  is false
-- as demonstrated by the following execution sequence
Trace Description: CTL Counterexample
Trace Type: Counterexample
  -> State: 1.1 <-
    garageDoorStatus_Machine.garageDoorStatus.state = Status_Open
  -> State: 1.2 <-
    garageDoorStatus_Machine.garageDoorStatus.event = ev_buttonOrObstacle
  -> State: 1.3 <-
    garageDoorStatus_Machine.garageDoorStatus.state = Status_Closing
  -> State: 1.4 <-
    garageDoorStatus_Machine.garageDoorStatus.event = ev_buttonOrObstacle
  -> State: 1.5 <-
    garageDoorStatus_Machine.garageDoorStatus.state = Status_Opening
  -> State: 1.6 <-
    garageDoorStatus_Machine.garageDoorStatus.event = ev_buttonOrObstacle
  -> State: 1.7 <-
    garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen
-- specification  G (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen ->  X (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen | garageDoorStatus_Machine.garageDoorStatus.state = Status_Opening))  is true
-- specification  G (garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen ->  F garageDoorStatus_Machine.garageDoorStatus.state = Status_Open)  is false
-- as demonstrated by the following execution sequence
Trace Description: LTL Counterexample
Trace Type: Counterexample
  -> State: 2.7 <-
    garageDoorStatus_Machine.garageDoorStatus.state = Status_HalfOpen
  -- Loop starts here
  -> State: 2.8 <-
    garageDoorStatus_Machine.garageDoorStatus.event = ev_reachBottom
  -> State: 2.9 <-
    garageDoorStatus_Machine.garageDoorStatus.event = ev_null
  -> State: 2.10 <-
    garageDoorStatus_Machine.garageDoorStatus.event = ev_reachBottom
```

### 7.8 这些结果应该怎么解释

这里有四条最关键的信息：

1. `CTL` 性质 `EF(HalfOpen)` 为真
   说明 `HalfOpen` 的确可达。
2. `CTL` 性质 `AG !HalfOpen` 为假
   `NuSMV` 给出的 counterexample 正好对应
   `Open -> Closing -> Opening -> HalfOpen`。
3. `LTL` 性质
   `G(HalfOpen -> X(HalfOpen | Opening))`
   为真
   说明从 `HalfOpen` 出发，下一步状态只可能保持 `HalfOpen` 或进入 `Opening`。
4. `LTL` 性质
   `G(HalfOpen -> F(Open))`
   为假
   反例里存在 `HalfOpen` 后不断遇到 `reachBottom` 这样的“无效事件”循环，因此并**不是所有路径**都会最终回到 `Open`。

这一段实验回答了一个非常重要的问题：

> `Umple` 是否存在一个官方状态机子集，可以直接实现 `Umple -> Python` 和 `Umple -> NuSMV -> verification`？

答案是：**存在，而且已经在本机跑通。**

## 8. 例子 B：`Drivers Licence` richer 样例

### 8.1 为什么还要保留这个 richer 样例

虽然 `GarageDoor` 已经证明 direct chain 存在，但它太简单了，缺少：

1. 层次状态
2. guard
3. effect
4. 结构关联
5. `Alloy` 上可看的结构命题

而 `project_1` 真正关心的并不是“任何一个有限状态机都能跑”，而是：

1. 能不能建比较像样的控制模型
2. 能不能让运行语义和结构语义一起落地

所以我保留了 richer 的 `Drivers Licence` 模型作为第二条实验线。

### 8.2 这个模型包含什么

模型文件在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.ump](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.ump)

它包含三个类：

1. `Applicant`
2. `DrivingLicense`
3. `TestRecord`

主状态机 `licenseLifecycle` 放在 `Applicant` 上，核心状态结构是：

1. 顶层状态：`NoLicense`、`Licensed`、`Suspended`、`ExpiredG`
2. `Licensed` 的子状态：`G1`、`G2`、`G`
3. 事件：`payFee`、`passG1Test`、`passG2Test`、`passGTest`、`suspend`、`expire`、`renewG`、`reinstateAsG1`、`reinstateAsG2`、`reinstateAsG`
4. guard：`feePaid == 1`、`suspensionCode == 1/2/3`
5. effect：更新 `feePaid`、`lastScore`、`suspensionCode`

### 8.3 `Python` 运行结果

运行脚本在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_driver_license_python_demo.py](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/run_driver_license_python_demo.py)

执行命令：

```bash
python3 verification/run_driver_license_python_demo.py
```

实际输出如下：

```text
initial: state=NoLicense, feePaid=0, lastScore=0, suspensionCode=0, currentLicense=None, testRecords=0
after_g1: state=Licensed.G1, feePaid=0, lastScore=80, suspensionCode=0, currentLicense=5001, testRecords=1
after_g2: state=Licensed.G2, feePaid=0, lastScore=82, suspensionCode=0, currentLicense=5001, testRecords=2
after_g: state=Licensed.G, feePaid=0, lastScore=88, suspensionCode=0, currentLicense=5001, testRecords=3
after_suspend: state=Suspended, feePaid=0, lastScore=88, suspensionCode=3, currentLicense=5001, testRecords=3
after_reinstate: state=Licensed.G, feePaid=0, lastScore=88, suspensionCode=0, currentLicense=5001, testRecords=3
after_expire: state=ExpiredG, feePaid=0, lastScore=88, suspensionCode=0, currentLicense=5001, testRecords=3
after_renew: state=Licensed.G, feePaid=0, lastScore=88, suspensionCode=0, currentLicense=5001, testRecords=3
python_demo_ok
```

这说明 `Umple -> Python` 对 richer model 也是直接可执行的，而且层次状态、guard、effect 都在运行轨迹中可观察。

### 8.4 raw `NuSMV` 导出的真实问题

原始导出文件在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.smv](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.smv)

它的问题不是“完全没东西”，而是“只有控制骨架，还不够验证完备”。

raw file 的一段典型片段如下：

```smv
VAR
  state : { LicenseLifecycle_NoLicense , LicenseLifecycle_Licensed , LicenseLifecycle_Suspended , LicenseLifecycle_ExpiredG };
  event : { ev_suspend , ev_renewG , ev_reinstateAsG , ev_payFee , ev_passGTest , ev_expire , ev_passG1Test , ev_reinstateAsG2 , ev_reinstateAsG1 , ev_passG2Test , ev_null };
  applicantId : integer;
  nameCode : integer;
  birthYear : integer;
  addressCode : integer;
  feePaid : integer;
  lastScore : integer;
  suspensionCode : integer;
```

同时它对这些数据变量只给了 `init(...)`，没有把 effect 的 `next(...)` 明确写出来，例如：

```smv
ASSIGN
  init( feePaid ) := 0;

ASSIGN
  init( lastScore ) := 0;

ASSIGN
  init( suspensionCode ) := 0;
```

这意味着：

1. raw `NuSMV` 文件有控制状态结构
2. 但 effect 驱动的数据语义没有完整落地
3. 所以它不适合作为这个 richer 例子的最终验证模型

### 8.5 verification-ready `NuSMV` 文件

因此我基于 raw skeleton 写了一份 verification-ready 文件：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/driver_license_verified.smv](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/driver_license_verified.smv)

这份文件只补了两类东西：

1. 将相关变量收窄为有限整数域
2. 将 `feePaid`、`lastScore`、`suspensionCode` 的 `next(...)` 逻辑按 `Umple` effect 显式编码

### 8.6 本次实际验证的 `CTL` 性质

我放入的 `CTL` 性质如下：

```smv
CTLSPEC EF(applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Licensed)
CTLSPEC EF(applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G)
CTLSPEC AG(applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G2 -> applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Licensed)
CTLSPEC AG(applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Suspended -> (applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.suspensionCode = 1 | applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.suspensionCode = 2 | applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.suspensionCode = 3))
CTLSPEC AG(applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_ExpiredG -> applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = null)
CTLSPEC AG(applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_ExpiredG -> EF(applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G))
CTLSPEC AG(applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state != LicenseLifecycle_Suspended)
```

其中最后一条是故意写错的，用来拿 counterexample。

执行命令：

```bash
./tooling/nusmv-2.6.0-linux64/bin/NuSMV verification/driver_license_verified.smv
```

### 8.7 `Drivers Licence` 的 `CTL` 输出

实际输出如下：

```text
-- specification EF applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Licensed  is true
-- specification EF applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G  is true
-- specification AG (applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G2 -> applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Licensed)  is true
-- specification AG (applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Suspended -> ((applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.suspensionCode = 1 | applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.suspensionCode = 2) | applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.suspensionCode = 3))  is true
-- specification AG (applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_ExpiredG -> applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = null)  is true
-- specification AG (applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_ExpiredG -> EF applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G)  is true
-- specification AG applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state != LicenseLifecycle_Suspended  is false
```

对应的 counterexample 片段如下：

```text
Trace Description: CTL Counterexample
Trace Type: Counterexample
  -> State: 1.1 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_NoLicense
  -> State: 1.2 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.event = ev_payFee
  -> State: 1.3 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.feePaid = 1
  -> State: 1.4 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.event = ev_passG1Test
  -> State: 1.5 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Licensed
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycleLicensed.state = LicenseLifecycleLicensed_G1
  -> State: 1.6 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.event = ev_suspend
  -> State: 1.7 <-
    applicantLicenseLifecycle_Machine.applicantLicenseLifecycle.state = LicenseLifecycle_Suspended
```

这说明 richer 样例下 `NuSMV` 这条链也确实完成了：

1. 正性质验证通过
2. 反性质失败
3. counterexample 回放

只是这里的验证模型不是 raw export，而是 raw export 上补了一层语义完整化。

## 9. `Alloy` 导出与结构检查

### 9.1 为什么 `Alloy` 在这个 richer 样例上更合适

`GarageDoor` 基本没有结构对象关系，不太适合拿来做 `Alloy`。

而 `Drivers Licence` 里有：

1. `Applicant`
2. `DrivingLicense`
3. `TestRecord`
4. 关联 `currentLicense`
5. 关联 `testRecords`

所以它天然适合补结构断言。

### 9.2 raw `Alloy` 导出与 wrapper

raw `Alloy` 文件在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.als](../baselines/umple/reproduction-2026-04-15-local-toolchain/models/driver_license_system.als)

这个 raw file 能被 `Alloy 6.2` 正常读入，但它只包含：

1. `sig`
2. `fact`

它没有自带实验所需的：

1. `run`
2. `check`
3. 断言命题

因此我保留 raw export 不动，再额外写一个 wrapper：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/alloysrc/driver_license_check.als](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/alloysrc/driver_license_check.als)

### 9.3 本次实际使用的 `Alloy` 命题

wrapper 文件内容如下：

```alloy
open Reproduction/DriverLicense

pred ExampleInstance {
  #Applicant = 1
  #DrivingLicense = 1
  #TestRecord = 3
}

assert SingleCurrentLicense {
  all a : Applicant | lone a.currentLicense
}

assert TestRecordBackReference {
  all t : TestRecord | t in t.applicant.testRecords
}

assert EveryApplicantHasALicense {
  all a : Applicant | one a.currentLicense
}

run ExampleInstance for 12 Int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
check SingleCurrentLicense for 12 Int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
check TestRecordBackReference for 12 Int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
check EveryApplicantHasALicense for 12 Int, exactly 1 Applicant, exactly 0 DrivingLicense, exactly 0 TestRecord
```

执行命令：

```bash
./tooling/alloy-6.2.0-linux-amd64/bin/alloy commands verification/alloysrc/driver_license_check.als
./tooling/alloy-6.2.0-linux-amd64/bin/alloy exec verification/alloysrc/driver_license_check.als
```

### 9.4 `Alloy` 的结果

`Alloy commands` 输出如下：

```text
0 . Run ExampleInstance for 12 int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
1 . Check SingleCurrentLicense for 12 int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
2 . Check TestRecordBackReference for 12 int, exactly 1 Applicant, exactly 1 DrivingLicense, exactly 3 TestRecord
3 . Check EveryApplicantHasALicense for 12 int, exactly 1 Applicant, exactly 0 DrivingLicense, exactly 0 TestRecord
```

结合 [../baselines/umple/reproduction-2026-04-15-local-toolchain/driver_license_check/receipt.json](../baselines/umple/reproduction-2026-04-15-local-toolchain/driver_license_check/receipt.json) 中的执行结果，可得到：

1. `ExampleInstance`: `SAT`
2. `SingleCurrentLicense`: `UNSAT`
3. `TestRecordBackReference`: `UNSAT`
4. `EveryApplicantHasALicense`: `SAT`

也就是：

1. 存在满足结构约束的实例
2. “每个申请人至多一张当前驾照”在给定 scope 下没有反例
3. “测试记录能回指到申请人的 `testRecords`”在给定 scope 下没有反例
4. “每个申请人都必须有驾照”这个命题能被反例打破

正例实例摘要里可以直接看到 1 个 `Applicant`、1 个 `DrivingLicense`、3 个 `TestRecord` 的结构：

```text
Command                                  ExampleInstance
Solution index                           0
Trace length                             1
Loop state                               0
```

反例摘要里可以直接看到 `EveryApplicantHasALicense` 的 skolem 目标是一个没有 `currentLicense` 的申请人：

```text
Command                                  EveryApplicantHasALicense
Solution index                           0
Trace length                             1
Loop state                               0

skolem                      value
$EveryApplicantHasALicense_a {DriverLicense/Applicant$0}
```

这说明 `Alloy` 这条链不只是“文件导出了”，而是已经完成了：

1. 正例实例搜索
2. 结构断言验证
3. 结构反例构造

## 10. 一键复现方法

最简单的复现方式是：

```bash
cd project_1_llm_state_machine_modeling/baselines/umple/reproduction-2026-04-15-local-toolchain
./verification/reproduce.sh
```

当前脚本会顺次完成：

1. 固定 `jenv` / `Java 17`
2. 导出 `Drivers Licence` 的 `Python` / `NuSMV` / `Alloy`
3. 运行 `Drivers Licence` 的 `Python` demo
4. 运行 verification-ready `Drivers Licence` `NuSMV`
5. 运行 `Alloy commands`
6. 运行 `Alloy exec`
7. 导出 `GarageDoor` 的 `Python` / `NuSMV`
8. 运行 `GarageDoor` 的 `Python` demo
9. 运行 raw `GarageDoor` `NuSMV`
10. 在 raw `GarageDoor` `.smv` 上追加 `CTL/LTL` 检查

脚本文件在：

[../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/reproduce.sh](../baselines/umple/reproduction-2026-04-15-local-toolchain/verification/reproduce.sh)

脚本默认优先使用实验目录下的本地缓存路径，但也支持下面三个环境变量：

1. `UMPLE_JAR`
2. `NUSMV_BIN`
3. `ALLOY_BIN`

因此如果后续不想保留我这次本地下载的 `tooling/` 缓存，也可以在外部自行安装对应版本，然后通过这三个变量把脚本接回去。

## 11. 复现时最值得注意的坑

这里集中记录后面最容易踩的坑。

1. 不要用系统自带的 `Java 8` 跑 `umple.jar`
   官方文档要求 `Java 11+`，本实验实际使用 `Java 17`。
2. `Python` 导出必须保证 `txl` 在 `PATH` 中
   否则生成链不完整。
3. `Umple` 的 `-r` 配合 `--path` 在这次实验里会触发 `deletePreviouslyGenerated` 的 `NullPointerException`
   所以复现脚本没有用 `-r`，而是自己先删输出目录。
4. `--path generated/python` 的实际解释是**相对输入 `.ump` 文件所在目录**
   不是相对当前 shell 工作目录。
5. `NuSMV 2.7.1` 官方二进制在这台 `Ubuntu 20.04` 上不可直接用
   复现时优先直接使用实验目录里的 `NuSMV 2.6.0`。
6. `GarageDoor` 这样的较小纯控制样例，raw `NuSMV` 导出可以直接验证
   但 `Drivers Licence` 这样带数据 effect 的 richer 样例，raw `NuSMV` 导出不等于 verification-ready。
7. raw `Alloy` 导出本身更像结构骨架
   真正要做实验性质检查，仍然需要额外的 wrapper 文件来放 `run/check/assert`。

## 12. 对 `project_1` 的直接启发

这次实验对 `project_1` 最直接的启发，我认为有七条。

1. `Umple` 不是只能停留在“相关工作名字”，它确实是一个可以被本地真实跑通的文本建模基线。
2. `Umple` 里确实存在一个较小的、可直接实现 `Umple -> Python` 和 `Umple -> NuSMV -> verification` 的官方状态机子集。
3. 但一旦进入 richer 的层次状态 + guard + effect + 结构关联场景，后端一致性问题就明显出现了。
4. 这说明 `Umple` 更像“宽生态建模入口”，而不是天然为 `NL -> analysis-ready control model` 收敛过的目标 DSL。
5. 这也支持了 [2026-04-14-23-03-54-AI-讨论-pyfcstm作为LLM建模论文目标形式的必要性与Umple-rebuttal口径.md](./2026-04-14-23-03-54-AI-讨论-pyfcstm作为LLM建模论文目标形式的必要性与Umple-rebuttal口径.md) 里的判断：
   `Umple` 很重要，但它并不自动替代一个更收敛、更 profile-driven 的 target formalism。
6. 从 rebuttal 或 related work 角度看，这次实验已经足够支撑一个很强的说法：
   我们不是“只读过 Umple 论文”，而是**本地亲手把官方例子和 richer 样例都跑通了**。
7. 从方法学角度看，`project_1` 后面如果真要把“生成模型直接接验证”写稳，必须明确区分：
   哪些语法构造属于“直链可验证子集”，哪些构造进入 richer 模式后必须经过 profile 收窄或后处理。

## 13. 一句话总结

这次本地复现实验已经证明：

> `Umple` 既存在一个可以直接实现 `Umple -> Python` 与 `Umple -> NuSMV -> verification` 的官方状态机子集，也能承载 richer 的层次状态与结构模型；但 richer 子集要想稳定接入 `NuSMV` / `Alloy` 验证闭环，仍然需要额外的 profile 收窄和后处理层。
