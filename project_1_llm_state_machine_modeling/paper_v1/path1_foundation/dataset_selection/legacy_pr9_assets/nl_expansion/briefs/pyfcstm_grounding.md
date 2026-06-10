# pyfcstm C1-C4 Grounding 模式调研

> 用途：让 `path2_selection` 的扩充 NL 有意识暴露能 trigger pyfcstm 这 4 条特性的语言模式。
> 调研基于 submodule `pyfcstm/` 当前主分支源码，所有引用文件路径相对 `pyfcstm/pyfcstm/`。

---

## C1 — Speculative validation 触发模式

- **pyfcstm 源**：
  - `simulate/runtime.py:1486` `SimulationRuntime._validate_transition`：deepcopy `stack` + `vars`，在 `is_validation_mode=True` 下重放 `_execute_transition_on_context` + `_run_cycle_on_context`，要求最终能到达 `is_stoppable` 配置（`model/model.py:811`：`is_leaf_state and not is_pseudo`）或干净 terminate
  - `simulate/runtime.py:1470` 在每次 `cycle()` 选迁移前，对 `is_stoppable` 源状态的候选迁移调用 `_validate_transition`，失败则**整轮回滚**
  - DFS 有结构深度上限（max_structural_depth），并通过 `_create_execution_signature` 在 search path 上做剪枝
- **核心机制**：transition 不是"语法可发"就接受，而是要先**符号执行式预演**到下游 `init pseudo → child enter → 父级 during after / exit → ...` 整条链上能落到一个 stoppable leaf，否则视作 dead-end 拒绝并回滚副作用
- **NL 应包含**（扩充 NL 里要出现的语言模式）：
  - 显式**层次化 / 嵌套模式**：`Mode Active is divided into sub-modes Heating and Cooling`、`Within Operational mode there are two phases ...`
  - **复合状态的初始子状态**线索：`entering Active starts in Heating`、`when System powers up, the controller enters the Idle phase first`
  - **跨层级 transition 终点**：`from Heating, on overheat, the controller leaves the Operational mode entirely and goes to ShutDown`（暴露 child → parent exit → 兄弟复合 init 这种长链）
  - **历史/复位回到初始模式**：`a reset returns the system to the top-level Idle state`
- **DSL 受益例子**：

  ```fcstm
  def int t = 20;
  state Sys {
      [*] -> Idle;
      state Idle;
      state Operational {
          [*] -> Heating;            // 没有这条 init pseudo，speculative validation 就会把 Idle->Operational 判 dead-end
          state Heating;
          state Cooling;
          Heating -> Cooling : if [t > 80];
      }
      Idle -> Operational : if [t > 30];
      Operational -> Idle :: Reset;  // 验证链：Heating.exit → Operational.during_after → Operational.exit → Idle.enter
  }
  ```
- **反例**（让 C1 用不上）：NL 里只描述**平铺的 N 个状态 + 转移**，没有任何层级 / sub-mode / phase / 初始进入语义；整篇没有任何"进入某个 mode 后默认从哪个 sub-state 开始"这种暗示

---

## C2 — Z3 数值守卫 + symbolic effect 触发模式

- **pyfcstm 源**：
  - `model/expr.py`：Expr IR（`Integer / Float / Boolean / Variable / BinaryOp / UnaryOp / ConditionalOp / UFunc`）
  - `solver/expr.py:47` `expr_to_z3`：递归把 Expr 翻成 Z3，覆盖算术 (`+ - * / ** %`)、位运算 (`& | ^ << >>`)、比较 (`< <= > >= == !=`)、布尔 (`&& || !`)、三元 `?:`，以及 22 个 math 函数符号。Z3 **原生支持**的子集：`abs / sign / floor / ceil / trunc / round / sqrt`；其余 `exp / log / log10 / log2 / log1p / cbrt / sin / cos / tan / asin / acos / atan / sinh / cosh / tanh / asinh / acosh / atanh` 当前 raise `NotImplementedError`（见 `solver/expr.py:317-343`）
  - `solver/operation.py:135` `_execute_operation_statements_symbolically`：把 `enter/during/exit/effect` 里的 `var = expr` 顺序展开成 Z3 表达式映射，实现 effect 的 symbolic execution
  - `solver/solve.py:150` `solve`：在守卫 + 路径约束下解 satisfiability
- **核心机制**：所有数值变量 + 算术/比较/逻辑/位运算/三元/支持的 math 函数 → Z3 约束；effect 块被符号执行，可以静态判 guard 可达性
- **NL 应包含**：
  - 至少 1-3 个**带物理量纲的连续/整型变量**（温度、压力、电压、流量、计数、距离、阈值、超时计数器）
  - **数值阈值比较**：`when pressure exceeds 5.0 bar`、`if the rpm reading is below 200`、`within the range [pmin, pmax]`、`for at least 3 consecutive cycles`
  - **复合守卫**：`AND / OR / 同时 / 并且 / 或者 / 但不包括`（`x > a && y < b`）
  - **算术 / 累加 effect**：`each cycle the retry counter increments by one`、`reset the integrator to zero on entering Idle`
  - **safe math**：`round / floor / ceil / abs / sqrt` 在工程场景的口径（`绝对偏差 |T - T_target| < 0.5`）
- **DSL 受益例子**：

  ```fcstm
  def float p = 0.0;
  def float p_max = 5.0;
  def int override = 0;
  def int retry = 0;
  state Pump {
      state Idle;
      state Running {
          during { retry = retry + 1; }
          exit  { retry = 0; }
      }
      Idle -> Running   : if [p >= 1.0 && p <= p_max && override == 0];
      Running -> Idle   : if [abs(p - p_max) < 0.1 || retry >= 100];
  }
  ```
- **反例**（让 C2 用不上）：NL 全是布尔标志位 / 字符串状态名，没有数值变量；或者只写"系统会监控状态"这种**没给阈值、没给关系、没给量纲**的抽象描述；又或者只用 `sin / log / exp` 这类 Z3 当前不支持的函数（会被 solver 主动拒绝）

---

## C3 — Aspect AOP + forced transitions 触发模式

- **pyfcstm 源**：
  - `model/model.py:1242` `iter_on_during_aspect_recursively`：每个 cycle 在 leaf `during` 周围**root→leaf 顺序展开 `>> during before`，leaf→root 顺序展开 `>> during after`**；pseudo 状态被跳过
  - `model/model.py:2478` `_recursive_finish_states`：处理 `!from -> to :: Event` 的递归展开。`!*` 会把守卫/事件/condition 沿着**所有 descendant substates**复制一份 transition，并把 `ALL → EXIT_STATE` 形式递归再下传一层（2570-2578）
  - DSL 入口：`>> during before/after` (aspect)、`during before/after`（仅复合状态自进 / 自出时触发）、`!X -> Y :: E` 和 `!* -> Y :: E` 强制转移
- **核心机制**：
  - **Aspect**：把"每个 tick 不管在哪个 leaf 都要跑一遍的逻辑"（safety invariant、watchdog tick、log、metric）从单个状态里抽出来挂到父复合状态上
  - **Forced transition**：把"无论现在在哪个子状态，只要事件 E 发生就强制跳转"语义编译成所有 descendant 共享同一 event 对象的多条转移
- **NL 应包含**：
  - **横切（cross-cutting）描述句式**：`while the system is operating, each cycle the watchdog must be kicked / the safety invariant temp < tmax must hold / a heartbeat counter is incremented`
  - **"无论处于哪个子状态都要 ..." / "任意状态下"**：`regardless of the current operating phase, a fatal alarm forces the controller to ShutDown`、`from any sub-state of Active, a power-loss event aborts the cycle and returns to Idle`
  - **"中止 / 取消 / 紧急" + 全局事件**：`an Emergency Stop button immediately halts all motion`、`any sensor fault during operation aborts the cycle`
  - 注意：aspect 通常对应"每 cycle 都要做的小动作"；forced 对应"任何状态突然要跳出来"
- **DSL 受益例子**：

  ```fcstm
  def int wd = 0;
  def float temp = 25.0;
  state Plant {
      >> during before { wd = wd + 1; }                 // aspect: 每 tick 自增看门狗
      >> during after abstract LogSafetyInvariant;      // aspect: 每 tick 跑安全断言（C4 同时触发）
      !* -> SafeShutdown :: EmergencyStop;              // forced: 任何子状态 → SafeShutdown
      [*] -> Operating;
      state Operating {
          state Heating;
          state Cooling;
          [*] -> Heating;
          Heating -> Cooling : if [temp > 60.0];
      }
      state SafeShutdown;
  }
  ```
- **反例**（让 C3 用不上）：NL 全是"在状态 X 下，若条件 C，则跳到 Y"这种**点对点本地转移**，没有任何 "每个 cycle"、"任意状态"、"无论何时"、"全局应急"等横切语义

---

## C4 — Abstract action + 硬件解耦 触发模式

- **pyfcstm 源**：
  - DSL 关键字：`enter abstract <Name>` / `during abstract <Name>` / `exit abstract <Name>` / `>> during before|after abstract <Name>`
  - `simulate/decorators.py:42` `abstract_handler(action_path)`：装饰 Python 方法，绑定到形如 `'System.Active.InitializeHardware'` 的 action path；`simulate/decorators.py:39` 元数据存于 `__abstract_handler_metadata__`
  - `simulate/context.py:25` `ReadOnlyExecutionContext`：handler 调用时收到的只读 snapshot，含 `state_path / vars (deep-copied) / action_name / action_stage`；不能写回，强制"读传感器、写执行器"全部走外部 callback
  - `simulate/runtime.py:1504-1505`：speculative validation 阶段**不调用** abstract handler（避免副作用），只在 real cycle 才触发
- **核心机制**：把"必须落到具体硬件 / 平台 / 外部库"的副作用从模型抽出，模型层只声明 abstract action 名字；不同代码生成 target（Python、C、ROS、PLC）各自实现对应 handler。模型本身保持**平台无关 + 副作用可信封装**
- **NL 应包含**：
  - **物理执行器名字**：`Valve V1 / Pump P2 / Motor M3 / Relay K1 / Heater HX1 / ContactorC1 / Solenoid S1`，以及"open / close / engage / disengage / energize / arm / disarm / latch / unlatch"
  - **传感器读取语义**：`sample the pressure transducer PT-102`、`read the encoder count`、`acquire the thermocouple reading T1`
  - **外部 IO / 显示 / 日志 / 通信**：`raise an alarm on the HMI`、`log the fault to non-volatile memory`、`publish the status over CAN`、`assert the BMS contactor line`
  - **enter / exit 时刻的硬件动作**：`upon entering S1, ValveV1 is opened; upon leaving S1, ValveV1 is closed`
  - **每 cycle 的硬件查询**（搭配 aspect）：`each cycle, the watchdog timer must be petted`、`periodically refresh the IO scan`
- **DSL 受益例子**：

  ```fcstm
  state Press {
      enter abstract OpenValveV1;          // 平台无关：模型只声明"要开 V1"
      during abstract SamplePressurePT102; // 平台无关：每 cycle 读 PT102
      exit  abstract CloseValveV1;
      enter abstract LogPhaseStart /* writes to NVM */;
  }
  ```

  对应 Python 实现 (示意)：

  ```python
  class PressHandler:
      @abstract_handler('Sys.Press.OpenValveV1')
      def open_v1(self, ctx: ReadOnlyExecutionContext): hw.v1.open()
      @abstract_handler('Sys.Press.SamplePressurePT102')
      def sample(self, ctx): self.last_p = hw.pt102.read()
  ```
- **反例**（让 C4 用不上）：NL 全是抽象数学/逻辑变量（counter / flag / mode），没有任何物理设备、IO、传感器、执行器、报警、通信通道名

---

## 综合启发（给 codex 扩充 NL prompt 用）

要让 4 条 C-axis 都有机会被触发，扩充 NL 应当：

1. **C1**：至少声明 1 个明确的 mode / phase / composite boundary，并指明"进入该 mode 时默认从哪个 sub-mode 开始"（暴露 init pseudo 语义）。
2. **C2**：至少含 2 个连续/整型物理变量 + 至少 1 个复合数值守卫（`AND / OR / 区间 / 绝对偏差`）；优先选可被 Z3 原生支持的算子（算术 / 比较 / 逻辑 / 位运算 / `abs sign floor ceil trunc round sqrt`），避免 `sin/cos/log/exp` 这类目前 raise NotImplementedError 的函数。
3. **C3**：至少 1 条 cross-cutting 语义 — 要么是"每 cycle 都要 ..."的 aspect 风格，要么是"任意状态下、紧急/故障/全局事件强制跳到 X"的 forced 风格；最好两者各有一个。
4. **C4**：至少 2 个具体的硬件 actuator / sensor / IO / 通信通道命名，并把"进入/退出某状态时该硬件做什么"或"每 cycle 该读哪个传感器"明确写出来。

硬约束：

- 上述补充**必须可由原文已有要素自然延伸**。若 case 原始描述里就是纯逻辑控制（无物理 IO），不要硬塞 Valve/Pump；若原文没有任何安全/异常路径，不要凭空发明 forced fault。
- 若原文用了 Z3 不支持的数学函数（log/exp/三角），保持原意但**不要在守卫里直接出现该函数**，可以重述为阈值比较 / 查表 / 状态切换。
- 扩充以"暴露语义"为目标，不以"堆砌特性"为目标 — 每条 C-axis 的钩子保持 **1-2 处**就够，不要让 NL 变成 spec dump。
