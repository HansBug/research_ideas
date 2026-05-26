# Path 2 — 差异化路线（Differentiation）接管指引

> **本文件目标**：任何新 Claude / codex session 进入 `dev/path2-differentiation` branch 后，按本指引可直接接管，把 Path 2 quick experiment 推进到 sprint 末。
>
> **前置阅读**：先读 [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（meta-level 路线规划与决策准则），再读本文件。
>
> **版本**：v5（2026-05-27 — **categorical-differentiation framing 纠偏**：删除 "reference-free" 作为 contribution；§1 重写为"控制系统作为对象 + 4 本质特征 + baseline 4 类失败模式 + pyfcstm 4 条 grounding 一对一映射"；§5 实验从 2 conditions 扩到 **5**（Umple × {single, hybrid} + pyfcstm × {single, hybrid, agent-loop}），其中 Umple 两条用来直接展示"控制系统所需的 4 类 grounding feature 在 Umple DSL 层面表达不出来"的 expressiveness gap；§6 新增 **feature utilization rate** 为主报道指标；§11.3 v4.1 framing 提升为正文主线根基）

## 1. 路线定位与论证骨架

**Path 2 = 差异化路线**。但"差异化"不是 evaluation 方法学层面的（不是"我们做了 reference-free"），而是**问题对象层面**：

> **核心主张**：我们论证存在一类独立的 NL-to-STM 任务对象 — **真实工业控制系统** — 它的 4 个本质特征恰好是现有 LLM-based STM 生成 baseline 的盲区。我们提出 agent loop + pyfcstm 协同方案，pyfcstm 的 4 条 DSL-level grounding feature 一对一覆盖这 4 个特征，agent loop 把这 4 个 grounding 在 generation 阶段就回灌为 deterministic 反馈信号。在 15 个真实工业控制系统 case（来自 9 个工业领域）上跑 5-condition matrix，按桶 + 按 C-axis 分层报告 lift 与 feature utilization rate，证明 baseline 在 4 个特征上各自的失败模式和我们方法的 grounding 收益。

完整论证链由下面 7 步组成（每步对应 §1.X 一节）：

1. **§1.1 控制系统 NL-to-STM 是一类独立问题对象**（不是 generic reactive system 的子集）
2. **§1.2 这类问题有 4 个本质特征**（周期执行 / 数值密集 / 硬件解耦 / 强 invariant + fault recovery）
3. **§1.3 现有 baseline 在这 4 个特征上有可枚举的失败模式**（每个特征对应一种生成 DSL 层面的具体 failure pattern）
4. **§1.4 pyfcstm 4 条 DSL-level feature 一对一覆盖这 4 个特征**（三段论 mapping）
5. **§1.5 仅靠 DSL 表达力不够 — 还需要 agent loop 把 grounding signal 回灌**（parse + sem + sim + scenariogen mutation coverage）
6. **§1.6 我们是首个 fully-automated 把 pyfcstm 4 条 grounding capability 接入 LLM-based 控制系统 STM 生成的工作**
7. **§1.7 6 baseline 方法学全景**（保留 v4 表格作为 paper §2 related work 直接复用素材）

下面逐节展开。

### 1.1 控制系统 NL-to-STM 是一类独立问题

控制系统建模相对一般 reactive system（家电 / 办公设备 / UML 教学题 / 系统级 spec）有以下 4 个本质区别：

1. **周期执行范式（cycle-based execution）**：控制系统跑在 control cycle 上（PLC 扫描周期 / 嵌入式 superloop / ROS spin 周期），每个 cycle "读传感器 → 决策 → 写执行器"；状态机停在某个 mode 时**每个 tick 都要做事**（积分、滤波、监控、watchdog）。一般 reactive system 是事件驱动 — 状态机停下来等下次事件。
2. **数值密集的守卫 / 效果**：控制系统 transition guard 含大量**复合数值条件**（温度阈值 / 距离阈值 / 流量约束 / 时序去抖 / 边沿检测）；effect 含 PID 计算 / 状态变量更新 / 累积量推进。
3. **硬件解耦需求**：控制系统 STM 在生成阶段**无法决定 target deployment**（PC 仿真 / RTOS / PLC / 嵌入式 MCU / ROS 节点），必须符号占位 + 后期注入；不能在 DSL 里直接写宿主语言代码。
4. **强 safety invariant + fault-recovery**：任何 mode 下都要 enforce 安全不变式（"温度 ≤ 最大值"、"距离 ≥ 最小值"、"流量 ∈ 允许区间"）；任何 mode 下 Error 事件触发都必须强制切到 fault-recovery 路径，不能依赖具体 mode 内部的逻辑接收。

这 4 个本质特征不是"工业控制系统比 reactive system 更复杂一点"的程度问题 — 而是 **categorical 区别**。一个生成 STM 的方法如果不在这 4 个维度上提供 grounding 机制，对控制系统建模就是结构性失败而不是性能问题。

### 1.2 现有 baseline 在 4 个特征上的失败模式

我们 surveyed 6 个主力 LLM-based NL-to-STM baseline（完整表见 §1.7）。它们的训练数据集和目标 DSL 都不为控制系统设计 — structure_event_driven 是 8 个家电 reactive system，llms_emp 是混合通用模型，req 是 Volvo 产品功能需求，umple/ttool-ai 是 UML/SysML 教学风格 spec。即便我们把它们的 generation strategy 复用到控制系统 NL 上，**生成的 STM 在 4 个特征上各自呈现可枚举的失败模式**：

| 控制系统特征 | baseline 典型失败模式（具体到生成 DSL 层面） |
| --- | --- |
| **周期执行** | 生成的 STM 是 event-driven：transition only on external events；进入状态后**完全静默**（没 `during {}` 块或等价的 per-tick action），或者塞一段不可执行的伪代码 |
| **数值密集 guards / effects** | 生成的 guard 退化为单 boolean (`if pressure_high`) 或塞 host-language 代码片段；多变量复合算术 guard（如 `if abs(temp - target) < epsilon AND debounce_count > 5`）**写不出来或写错** |
| **硬件解耦** | Umple-like baseline 把动作绑死在 Java/PHP/Python；切换部署目标得**重写整个 STM**；或干脆把 hardware-specific code（GPIO 调用 / motor 驱动）直接塞进 action body |
| **强 invariant + fault recovery** | 要么**漏掉 fault path**；要么为每个叶子状态**重复抄一遍 fault transition**（O(N) 复制）；invariant 检查塞进每个 state 的 entry action（同样 O(N) 复制） |

这 4 类失败模式都可以在生成的 DSL 文本里直接 spot — 这意味着实验可以**直接统计**"生成 STM 是否用了对应 grounding feature"作为 differentiation 的硬证据，而不只是间接的 intrinsic lift。详见 §6 feature utilization rate 定义。

### 1.3 pyfcstm 4 条 DSL-level feature 一对一覆盖 4 个特征

pyfcstm 不是"通用 statechart DSL 再加几个 control-system-friendly feature"；它的 4 条核心 feature 各自对应上面 4 个特征中的一个，是有意识为控制系统建模设计的。三段论 mapping：

| 控制系统特征 | pyfcstm DSL-level feature | LLM agent loop 中获得的能力 |
| --- | --- | --- |
| 周期执行 | `during { ... }` per-cycle action block + aspect `>> during before / after` (root→leaf→root cascade per cycle) | agent 可生成跨所有叶子的 cross-cutting per-tick 行为（监控、日志、安全断言），无需为每个 leaf 复制 |
| 数值密集 guards / effects | `Expr` IR (`pyfcstm/model/expr.py`) + `pyfcstm/solver/` Z3 集成（`expr_to_z3` / `execute_operations` / `solve`），支持算术 / 比较 / 逻辑 / 位运算 / 22 个 math 函数 | agent 在每轮 repair 前能拿到 "这条 guard 是否可达 (SAT)"、"effect 后变量空间是否满足下一 invariant" 的 SMT-grade 反馈 |
| 硬件解耦 | `enter abstract` / `during abstract` / `exit abstract` DSL 占位 + Python 侧 `@abstract_handler` decorator + `ReadOnlyExecutionContext` (frozen) | agent 可在 generation 阶段产出 hardware-effector 占位符不需要决定 deployment target；handler 在 runtime 反射注入；frozen context 防止 handler 修改 vars；两档错误处理把 handler 异常落到 structured field 供 agent 消费 |
| 强 invariant + fault recovery | `>> during after` aspect action（每 cycle root→leaf→root cascade）+ `!` forced transition（模型层递归展开到所有 descendant，`_recursive_finish_states`） | 一行 `>> during after abstract AssertSafetyInvariant` 表达"任意 mode 下每周期都要检查安全上限"；一行 `! * -> ErrorHandler :: Error` 表达"任意工作 mode 下 Error 都强制切到安全状态" |

这张表是 paper §3 method 的根基，也是 §11.3.0 三段论 framing 的核心 mapping。

### 1.4 仅靠 DSL 表达力不够 — 还需要 agent loop

pyfcstm DSL 提供的是**表达力**：把上述 4 类 grounding 写成代码的能力。但 LLM 单 prompt 生成 STM 时，**即使 target DSL 是 pyfcstm**，依然倾向于退化为简单 event-driven flat FSM，不主动用上 4 类 feature。

我们的 agent loop 把 4 类 pyfcstm grounding capability 在 generation 阶段就转化为 **deterministic feedback signal** 回灌给 LLM：

- **Parse feedback**（`pyfcstm.dsl.parse_with_grammar_entry`）：grammar 合法性
- **Semantic feedback**（`pyfcstm.model.parse_dsl_node_to_state_machine`）：missing states / dangling transitions / undefined vars / type mismatches
- **Sim feedback**（`pyfcstm.simulate.SimulationRuntime`）：speculative DFS validation 检测 dead-end + scenariogen self-managed 6-mutation coverage 作为 in-loop bug-finding probes（PR #11 Phase E v3 (f) 实装的 `method/scenariogen_validate.py`）
- **Cascaded Repair**：按 earliest-failing channel 路由的 4 个 fix sub-prompt，共享 pyfcstm grammar reference

迭代上限 $N = 3$ 轮 fully automated（不需要人类介入），与 IEC 61499 baseline 的人类评论式迭代精化形成对比。

### 1.5 我们是首个 fully-automated 接入这套 grounding 的工作

把 §1.3 的 pyfcstm DSL-level grounding 加上 §1.4 的 agent loop deterministic feedback 看作一个整体，我们是**首个** fully-automated 把这套"控制系统 4 特征对应的 grounding"接入 LLM-based STM 生成 pipeline 的工作。证据：

1. **没有任何 baseline 把 4 类 grounding 同时接入 in-loop feedback**：llms_emp 只做 grammar/semantics rule-based check (a+b)，ttool-ai 只做 JSON/syntax/constraint check (a+b)，IEC 61499 主做 simulation 但需人类评论介入，Llama3 Umple 只做 pass@k 可执行性检查。
2. **没有任何 baseline 做 speculative DFS validation from runtime**：pyfcstm `SimulationRuntime._validate_transition` 用 deepcopy-snapshot DFS 验证 transition 触发后下游 init/pseudo 链能否 reach stoppable boundary，并抛出 structured `SimulationRuntimeDfsError`。Umple/PlantUML/Mermaid/TTool 不直接给。
3. **没有任何 baseline 做 scenariogen self-managed mutation coverage in loop**：PR #11 Phase E v3 (f) 实装的 `method/scenariogen_validate.py` 在 scenariogen 之后自动对 model 应用 6 类典型 LLM bug 突变跑 sim 自检覆盖率，覆盖率不足时 directive 反馈让 scenariogen 补 probes。
4. **没有任何 baseline 做 fully automated 控制系统 NL-to-STM**：IEC 61499 是唯一做控制系统 + simulation feedback，但需要人类评论；其他 baseline 不做控制系统对象。

### 1.6 4 条 method contribution（paper §1 直接复用）

> **v5 修订说明**：原 v4 含 5 条 contribution，其中 C5 是"reference-free 4-intrinsic + audit-trail calibration evaluation protocol"。v5 删除 C5 — reference-free 不是我们的方法学创新，只是控制系统域固有约束的结果。Evaluation methodology (4 intrinsic + feature utilization + per-bucket / per-C-axis stratified analysis) 在 §6 描述为 **enabling tooling**，不进 paper §1 contributions 列表。

paper §1 contributions（与 §11.3 v4.1 / §11.4 表格同源）：

1. **C1 — In-loop deterministic feedback via speculative validation**：pyfcstm `SimulationRuntime` per-cycle deepcopy-snapshot speculative DFS validation 作为 deterministic in-loop feedback source，对应**周期执行**与**强 invariant** 两个控制系统特征。
2. **C2 — Language-independent expression IR enables symbolic reasoning without code generation**：`Expr` IR + `solver/` Z3 集成提供 guard SMT satisfiability + symbolic effect propagation 作为 in-loop feedback，对应**数值密集 guards / effects**。
3. **C3 — DSL-native aspect AOP + forced fault paths align with control-system idioms**：`>> during before/after` aspect + `!` forced transition 是 Umple/PlantUML 没有 DSL 级对应物的原语，对应**强 invariant + fault recovery**。
4. **C4 — Abstract action + read-only context decouples symbolic STM from physical effectors**：`enter abstract` / `@abstract_handler` decorator / `ReadOnlyExecutionContext` 实现硬件 effector 解耦，对应**硬件解耦**。

详细 contribution narrative 与控制系统场景对应见 §11.3.0（三段论 framing）、§11.3（每条 contribution 的 paper-ready 段落）、§11.4（contribution × pyfcstm feature × 控制系统场景价值速查表）。

### 1.7 6 个主力 baseline 方法学全景（paper §2 related work 复用）

完整 6-baseline 对照表（与 [discussion §4.4](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md#44-6-个主力-baseline-方法学全景v3-新增) 同源）：

| # | baseline | 任务 / 输出 | LLM | 方法核心 | prompt-eng | simulation 反馈 | formal verification 反馈 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [structure_event_driven](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) (2026) | NL → UML statechart (Umple) | GPT-4o / Claude 3.5 Sonnet | 4 strategy: Single-Prompt / Structure-Driven / Event-Driven / Hybrid | 高（分步提示 + Hybrid 草稿迭代） | **无** | **无**（仅规则后处理 + 参考解比对） |
| 2 | [llms_emp](../baselines/llms_emp/DESC.md) (2025) | NL → SysML STM/ACT/SD (PlantUML) | GPT-4 / 4o / Kimi / Claude 3 Haiku / Llama3.1 / DeepSeek-v3 | **两阶段框架：提示生成 + 模型检查反馈修复** | 高（五段 prompt + RAG） | **低**（论文将 sim traces 视为未来反馈，**未真正接入**） | **中-**（PlantUML / SysML grammar / semantics / consistency **rule-based check**，不是完整 formal verification） |
| 3 | [LLM-based iterative refinement (IEC 61499)](../baselines/fsm-gen-iec-61499/DESC.md) (2025) | NL + I/O spec → FSM + IEC 61499 code | 未明确 | **迭代精化 + 仿真 + 代码生成** | 中（人类评论式增量修订） | **高**（EAE / softPLC 闭环仿真，**主反馈来源**） | 低-中（人工 / 可视化检查 + 计划接 formal，**未实装**） |
| 4 | [Automated Statechart (Automotive)](../baselines/req/DESC.md) (2025) | NL 产品功能需求 → Mermaid statechart | GPT-3.5 / 4 / 4o (微调) | NLP 特征提取 + 合成数据扩充 + 领域微调 | 中（prompt-completion 对 + 数据增广） | 低（Mermaid 渲染 + 专家评审） | **无** |
| 5 | [Llama3 Umple](../baselines/umple/DESC.md) (2025) | NL → Umple state machine | Llama 3 (8B) | Zero-shot / One-shot / RAG 提示策略对比 | 高（系统消息 + RAG 选例） | **中**（Umple 可执行性 / pass@k 检查） | **低**（依赖 Umple 编译 / 语义可执行性，非独立 formal proof） |
| 6 | [ttool-ai](../baselines/ttool-ai/DESC.md) (2024) | NL 系统规范 → SysML 块图 + 内部块图 + 状态机图 (AVATAR) | GPT-4 | **知识注入 + 自动反馈循环 + TTool 工具链** | 高（约束化 JSON 输出 + 自动反馈问答） | **中**（TTool simulator 观察行为，**评分支撑，非连续仿真闭环**） | **中-**（TTool 支持 model-checker，**反馈环主要检查 JSON / 语法 / 约束**，formal capability 是工具背景非主验证机制） |

**关键观察（与 §1.2 失败模式 + §1.5 automation gap 同源，但从 baseline survey 角度复述一遍）**：

1. 6 个 baseline 中**没有一个把控制系统作为对象**：1, 5 是家电 / UML 教学，2, 6 是混合通用 / 系统级 spec，3 是控制系统但需人介入，4 是 Volvo 产品功能需求。
2. 6 个 baseline **没有一个 target 控制系统所需的 4 类 grounding feature**：Umple/Mermaid/PlantUML/SysML/AVATAR 在 DSL 层面都不提供 aspect AOP / forced transitions / abstract action / Expr IR + Z3 backend 这一整套。
3. 因此即使把 baseline 的 generation strategy（Hybrid prompting / 两阶段 + RAG / 自动反馈循环）复用到控制系统 NL 上，**生成 STM 在 §1.2 4 个失败模式上仍会全面体现** — 这正是 §5 实验的 5-condition matrix 要直接验证的。

### 1.8 与 Umple 的差异化（paper §3 用）

完整 Umple rebuttal 口径见 [2026-04-14 讨论稿](../discussions/2026-04-14-23-03-54-AI-讨论-pyfcstm作为LLM建模论文目标形式的必要性与Umple-rebuttal口径.md) §7。v5 立场：**与 Umple 的差异不是 DSL 表达力的 "我有你也可以加"，而是控制系统 4 特征的 grounding 机制必须配套设计**。Umple guards 是 host-language code → 无法 Z3 求解；Umple 无 speculative validation runtime → 死锁/不可达只在 codegen 后暴露；Umple 无 DSL-native aspect AOP → 控制系统 invariant 要手抄；Umple 无 DSL-level abstract action → lifecycle hook 直接写宿主语言代码。这 4 条不是 Umple 的"轻微遗憾"，而是它**不为控制系统建模设计**的结构性体现。详见 §11.3.0.3。

## 2. 接管前自检

进入 `dev/path2-differentiation` branch 后，按以下顺序验证 sprint 状态：

```bash
# 1. 确认 branch
git branch --show-current
# 应该输出: dev/path2-differentiation

# 2. 确认 method/ + eval/ 共同基础已 fork 自 main
ls project_1_llm_state_machine_modeling/method/ project_1_llm_state_machine_modeling/eval/ 2>/dev/null
# method/: agents/ feedback/ loop.py schema.py prompts/ gpt_client.py scenariogen_validate.py
# eval/:   PROTOCOL.md extract/ annotate/ review/ aggregate.py report.py demo/ data/

# 3. 确认 pyfcstm 已安装
python -c "from pyfcstm.dsl import parse_with_grammar_entry; print('ok')"
python -c "from pyfcstm.simulate import SimulationRuntime; print('ok')"

# 4. (Phase H 跳过) 原 v3 要求 ex1 ExpertReviewAgent 自检 — sprint 不做，跳过此步
#    若方向定后补 Phase H 时再 verify:
#    python -c "import sys; sys.path.insert(0, 'project_ex1_llm_judge_for_stm/src'); from expert_review.agent import ExpertReviewAgent; print('ok')"

# 5. 确认实验主路 LLM env 三件套已 source
# 调用前必须先：source .env（仓库根，已 gitignore）
# 代码绝不直接读取 .env 文件本身，只读 os.environ
[ -n "$LLM_ENDPOINT" ] && [ -n "$LLM_API_KEY" ] && [ -n "$LLM_MODEL" ] && echo "env ok"
# 若 ok 不出现，shell 里跑：source .env  然后重试
# 该 proxy 是 OpenAI-compatible，sprint 实验主路 (method/loop) 走这一个 endpoint；
# 切换 model 只改 LLM_MODEL 环境变量，不动 client 代码

# 6. (可选) 确认评测 annotator CLI — 仅在跑 §6 audit-trail 抽查时需要
[ -n "$CLAUDE_CMD" ] && [ -n "$CLAUDE_MODEL" ] && [ -n "$CODEX_CMD" ] && [ -n "$CODEX_MODEL" ] && echo "annotator env ok"
which claude codex

# 7. 查 sprint 进度
cat project_1_llm_state_machine_modeling/method/STATUS.md 2>/dev/null || echo "no STATUS yet"
```

若 1-3、5 任一不通过，**停下来**，先确认 main 上 PR #11 是否已合入 + 本 branch 是否已 rebase 到 main — Path 2 branch 不应当独立做共同基础。第 6 步仅在跑可选 audit-trail 抽查时是阻塞条件。

## 3. 数据规则（T0 硬约束 + 3 桶分层）

### 3.1 T0 子集筛选

**T0 定义**：sources/ 样本的 STM.md §2 自然语言描述中**不含显式时间约束**。判定规则同 [PATH1 §3.1](./PATH1_HARD_COMPARISON_GUIDE.md#31-t0-子集筛选)，但应用于 sources/ STM.md §2 而非 baseline parquet。

实际 sources/ 池子里已经标过 T0/T1 标签（见 [sources/SUMMARY.md](../sources/SUMMARY.md) 与历史 PR #7），优先复用已有标签；标签不齐时按上述规则补判。

### 3.2 3 桶分层选样

| 桶 | 样本数 | 定义 |
| --- | --- | --- |
| `FSM-basic` | 6 | 状态数 $\le 10$、无层次、无并发的简单 reactive 控制器 |
| `EFSM-interlock` | 8 | 含变量更新 / 守卫 / 联锁条件的 EFSM，状态数中等 |
| `HSM-layered` | 6 | 含层次状态 / composite state / 子机的层次状态机 |

总计 20 条。从 sources/ 双 A T0 子集中按桶随机抽（seed 固定，可复现）。

### 3.3 选样落盘

筛完后落到：

```text
project_1_llm_state_machine_modeling/eval/data/sources_path2.parquet
```

schema：

```text
columns:
- case_id: str  # sources/<dir-name> slug
- source_dir: str  # sources/<dir-name>/
- nl_text: str  # 取 STM.md §2 整理后的自然语言描述
- stm_md_path: str  # 反向到 sources/<dir>/STM.md 的指针
- bucket: str  # "FSM-basic" | "EFSM-interlock" | "HSM-layered"
- rating: str  # 🟢
- time_level: str  # T0
- meta: dict  # {domain, n_states_estimate, has_hierarchy, ...}
```

## 4. 实验设计 — 5 条件矩阵

> **v5 设计依据**：要论证 §1.2 4 个失败模式 + §1.3 pyfcstm 4 条 grounding 的差异化效果，必须把"DSL 选择"与"generation strategy"两个变量分开测。Umple 两条 condition 用来直接 surface "控制系统所需 4 类 grounding 在 Umple DSL 层面表达不出来"的 expressiveness gap（feature utilization 在 Umple 下结构性为 0，因为 Umple 没这套 DSL 语义）；pyfcstm 三条 condition 在同 DSL target 下隔离 generation strategy 的 grounding 收益。

### 4.1 5 conditions 矩阵

| Condition ID | 生成 DSL target | Generation strategy | iter | feedback_sources | 用途 |
| --- | --- | --- | ---:| --- | --- |
| `A0_single_umple` | Umple | Single-prompt | 1 | 空 | **DSL expressiveness gap baseline #1**：复用 baseline_structure_event paper §III.B Single-Prompt strategy，target 改为我们对照的工业控制系统。Umple 无 `during`/`!`/`abstract`/Expr IR + Z3 → feature utilization 4 项结构性为 0；intrinsic 中 SimRate/ReachRate 因 Umple 缺 runtime 无法计算（标 N/A） |
| `A0_hybrid_umple` | Umple | Hybrid (4-step) | 4 | 空 | **DSL expressiveness gap baseline #2**：复用 baseline_structure_event paper §III.D Hybrid strategy（先 Single-Prompt 草稿，再 Structure-Driven + Event-Driven 迭代细化），target 仍是 Umple。证明即使用 baseline 论文最强 strategy，Umple DSL 层面仍缺 4 类 grounding。**这是 baseline 论文原始 setup 的忠实复现。** |
| `A0_single_pyfcstm` | pyfcstm | Single-prompt | 1 | 空 | **DSL 同源对照 #1**：target 改为 pyfcstm，同 single-prompt strategy。pyfcstm DSL 提供 4 类 feature 但单 prompt 不主动用 → 看 feature utilization 默认水平 + intrinsic |
| `A0_hybrid_pyfcstm` | pyfcstm | Hybrid (4-step) | 4 | 空 | **DSL 同源对照 #2**：target 仍是 pyfcstm，但用 baseline §III.D Hybrid strategy 替代 single-prompt（无 deterministic feedback）。隔离 "多步 prompting 本身的收益" 与 "deterministic feedback 的收益" 两个变量 |
| `A_full_ours` | pyfcstm | Agent loop (MTI 6-step + cascaded repair) | 3 | `["parse", "semantic", "sim"]` | **我们的方法**：MTI 6-step modeler + parse/sem/sim 三路 deterministic feedback + scenariogen self-managed 6-mutation coverage（Phase H judge 跳过）|

实验主对比方向：

- **`A_full_ours` vs `A0_hybrid_pyfcstm`**：同 DSL target (pyfcstm)，同等步数级别的 strategy，差异只在 deterministic feedback。**主 lift 来源即 §1.5 fully-automated grounding loop 的纯收益。**
- **`A_full_ours` vs `A0_hybrid_umple`**：完整 method-of-record (我们) vs 完整 baseline-of-record（structure_event_driven paper 最强 strategy + Umple DSL）。**这是 paper §4 主表的横向对比。**
- **`A0_hybrid_pyfcstm` vs `A0_hybrid_umple`**：同 strategy (Hybrid)，同等步数 prompting，差异只在 DSL target。**直接 surface DSL expressiveness gap 的 evidence。**
- **`A0_single_*` 系列**：作为 strategy-strength floor，验证 Hybrid 比 single-prompt 在 baseline setup 里确实更强（与 baseline 论文 §IV reported macro-F1 趋势对齐）

### 4.2 各 condition 的具体调用

各 condition 通过 `method.loop.run_agent_loop(nl=..., config=LoopConfig(...))` 统一接口分发。LoopConfig 关键字段：

```python
# A0_single_umple
LoopConfig(condition="A0_single_umple", n_iter=1, feedback_sources=[],
           modeling_mode="single_prompt", target_dsl="umple")

# A0_hybrid_umple
LoopConfig(condition="A0_hybrid_umple", n_iter=4, feedback_sources=[],
           modeling_mode="hybrid", target_dsl="umple")

# A0_single_pyfcstm
LoopConfig(condition="A0_single_pyfcstm", n_iter=1, feedback_sources=[],
           modeling_mode="single_prompt", target_dsl="pyfcstm")

# A0_hybrid_pyfcstm
LoopConfig(condition="A0_hybrid_pyfcstm", n_iter=4, feedback_sources=[],
           modeling_mode="hybrid", target_dsl="pyfcstm")

# A_full_ours
LoopConfig(condition="A_full_ours", n_iter=3, feedback_sources=["parse","semantic","sim"],
           modeling_mode="multi_step", target_dsl="pyfcstm")
```

实装侧需要在 PR #11 共同基础之上**新增**：

1. **`method/loop.py` 加 `modeling_mode="hybrid"` 分支** — 复用 baseline_structure_event paper §III.D 的 4-step strategy（Single-Prompt draft → Structure-Driven refinement → Event-Driven refinement → 最终合并），但目标 DSL 由 `target_dsl` 字段决定
2. **`method/loop.py` 加 `target_dsl` 字段** — 取值 `"umple"` 或 `"pyfcstm"`；影响 modeler / repair prompt 的 grammar reference 与 output validator
3. **`method/prompts/modeler/hybrid_*.txt`** — 4 个新 prompt：`single_draft.txt` / `structure_review.txt` / `event_review.txt` / `merge.txt`，每个有 umple / pyfcstm 双版本（共 8 个文件）
4. **Umple 输出层 intrinsic 计算适配** — Umple parse 走 `umple` CLI 或现有 reproduction/baselines 工具（已实装）；SimRate / ReachRate 在 Umple 下标 N/A，**这是 evidence 不是 bug**

### 4.3 `method/gpt_client.py` 统一 LLM client（Phase 0 已实装于 PR #11）

实验主路所有 LLM 调用（spec / model / repair / hybrid sub-prompts）**全部走这一个 client**。

**评测 annotator 例外**：[`../eval/annotate/{claude,codex}.py`](../eval/annotate/) 走 `claude` / `codex` CLI subprocess，不经 `gpt_client`；仅在 §6 可选 audit-trail 抽查时用到。

**约束**：代码绝不直接读 `.env`，只读 `os.environ`。运行前 shell `source .env`。

```python
# method/gpt_client.py 骨架
import os
from openai import OpenAI

def get_llm_client():
    return OpenAI(
        base_url=os.environ["LLM_ENDPOINT"],
        api_key=os.environ["LLM_API_KEY"],
    )

def get_default_model() -> str:
    return os.environ["LLM_MODEL"]
```

切换实验主路模型只改 `.env` 的 `LLM_MODEL` 后 `source`，代码不动。当前 `LLM_ENDPOINT` 提供的 OpenAI-compatible 代理只挂 GPT 系列；cross-vendor sanity 跑 Claude 不在 sprint 范围。
## 5. 实验脚本 `method/run_path2.py`

CLI 接口（Phase 5 开工时由 Path 2 branch 实现，本指引固定接口规范）：

```bash
# 先在 shell source 仓库根 .env 把三件套加载到环境变量
source .env

# 然后跑 5 conditions × 15 candidates
python -m method.run_path2 \
  --samples project_1_llm_state_machine_modeling/eval/data/sources_path2.parquet \
  --conditions A0_single_umple,A0_hybrid_umple,A0_single_pyfcstm,A0_hybrid_pyfcstm,A_full_ours \
  --out project_1_llm_state_machine_modeling/eval/results/sprint_path2/predictions.parquet \
  --resume
```

condition 字段分发（在 run_path2.py 内部）：

- `A0_single_umple` → `LoopConfig(n_iter=1, feedback_sources=[], modeling_mode="single_prompt", target_dsl="umple")`
- `A0_hybrid_umple` → `LoopConfig(n_iter=4, feedback_sources=[], modeling_mode="hybrid", target_dsl="umple")`
- `A0_single_pyfcstm` → `LoopConfig(n_iter=1, feedback_sources=[], modeling_mode="single_prompt", target_dsl="pyfcstm")`
- `A0_hybrid_pyfcstm` → `LoopConfig(n_iter=4, feedback_sources=[], modeling_mode="hybrid", target_dsl="pyfcstm")`
- `A_full_ours` → `LoopConfig(n_iter=3, feedback_sources=["parse","semantic","sim"], modeling_mode="multi_step", target_dsl="pyfcstm")`

实现要点：

1. **断点恢复（checkpoint per (case_id, condition) row）**：predictions.parquet 增量 append；run_path2 启动时跳过 already-done 行
2. **失败容忍**：单 case × condition 失败（API 失败 / parse 失败 / sim handler 失败）记 status 不阻塞其他 case
3. **token tracking**：每 row 含 `token_usage = {prompt, completion, total}`，summary.json 含按 condition × bucket aggregate
4. **资源预算估计**：5 conditions × 15 cases ≈ 75 主实验；A_full_ours 含 3 iter × ~6 LLM calls/iter ≈ 270 calls；A0_hybrid_* 含 4 step ≈ 60 calls；A0_single_* 含 1 call。**总计 ~345 LLM calls × 平均 ~20s + sim 验算 ~5s = ~2.5 hr wall time (单线程)** / **~25-30 min (并发 -P 6)**

## 6. 评测指标 — VGC（主）+ 4 intrinsic（辅）+ Reference STM 对照（spot-check）

> **v5.1 修订（基于"reference-free 不是创新点"+ FUR tautology 修正讨论）**：原 v5 用 FUR (Feature Utilization Rate) 作主指标，但 FUR 测的是"生成 DSL 里有没有出现 pyfcstm-specific 语法"，对 Umple 的对照存在 tautology 嫌疑（Umple 当然不出现 `! * -> Error`，因为它没这个语法）。v5.1 把主指标改为 **VGC (Verifiable Grounding Coverage)** — 测的是"以可被 deterministic verifier 检查的方式表达 grounding semantic 的覆盖率"，把 differentiation 锚定在 **verifier 能力**而不是字面语法上。Umple 即使用 `do` activity / per-state fault transition / hook 表达了对应 semantic，VGC 也不满分，因为没有对应的 in-loop verifier 能 ground 这些 semantic 在 generation 阶段就回灌。

### 6.1 `VerifiableGroundingCoverage`（主报道指标）— 把 differentiation 锚到 verifier 能力

对每个生成 DSL，按下面 4 个 grounding semantic 各自判定：**(A) semantic 是否被表达；(B) 表达方式是否可被对应 toolchain 的 verifier 静态检测**。两者同时满足才算该 semantic "verifiably grounded"。

| Grounding Semantic | pyfcstm 表达 + verifier | Umple 等价表达 + verifier | 对应控制系统特征 | 对应 contribution |
| --- | --- | --- | --- | --- |
| Per-cycle behavior | `during {}` / `>> during` aspect → `SimulationRuntime._run_cycle_on_context` 静态展开 + cycle-level execution check | `do` activity → **无 cycle-level verifier**（host language hook）| 周期执行 | C1 |
| Numerical guard reasoning | `Expr` IR 含 ≥2 vars + 算术/比较 → `pyfcstm/solver/expr.py:expr_to_z3` SMT check | host-language guard code → **无 SMT translation 路径** | 数值密集 | C2 |
| Forced fault path | `! * -> Error :: Event` → `_recursive_finish_states` 静态展开到 descendant + 完备性 check | per-state `to Error :: Event` × N → 可数但**无层次自动展开** | 强 invariant + fault recovery | C3 |
| Hardware effector decoupling | `enter/during/exit abstract` + `@abstract_handler` reflection → `simulate/runtime.py` handler-binding check | host-language action body → **无 abstract / reflection 层** | 硬件解耦 | C4 |

**指标定义**：

$$\text{VGC}_{\text{condition}} = \frac{1}{4 \times N} \sum_{i=1}^{N} \sum_{g \in \{C1, C2, C3, C4\}} \mathbb{1}[\text{semantic } g \text{ is verifiably grounded in } \text{dsl}_i]$$

每个 case × 每个 grounding semantic 给一个二元 score (1 = verifiably grounded / 0 = not)，对 N case × 4 semantic 取均值。

**判定流程**（per case × per semantic）：

1. **表达检测**：grep 出该 semantic 在 DSL 中的候选表达（pyfcstm 语法 / Umple 等价构造）
2. **verifier 适用性**：对应 toolchain 的 verifier 能否对该表达做静态 grounding check
3. 同时 ✓ → score = 1，否则 score = 0

**关键 framing**：Umple 在 C1/C3/C4 上即使写了 `do` / per-state `to Error` / inline action，VGC score 依然 0 —— 不是因为没表达，而是因为**没有 in-loop verifier 把这些 semantic 转成 deterministic feedback signal**。这把 differentiation 锚定到 verifier 能力（= C1-C4 contribution 的核心）而非字面语法。这同时解决了 v5 草案里 FUR 的 tautology 嫌疑（reviewer 不能再说"你只是测了 pyfcstm syntax 出现率"）。

**预期结果（v5.1 sprint 期望）**：

| Condition | C1 VGC | C2 VGC | C3 VGC | C4 VGC | mean VGC |
| --- | ---:| ---:| ---:| ---:| ---:|
| A0_single_umple | 0 (no cycle verifier) | 0 (no SMT) | 0 (no layered fault verifier) | 0 (no abstract layer) | 0% |
| A0_hybrid_umple | 0 | 0 | 0 | 0 | 0% |
| A0_single_pyfcstm | ~low (LLM 默认不主动用) | ~low | ~low | ~mid | low-mid |
| A0_hybrid_pyfcstm | mid (Hybrid 引导可识别周期需求) | mid | low | mid | mid |
| A_full_ours | **high** (sim feedback push) | **high** (Z3 grounding push) | **high** (sem+sim 暴露 fault path) | **high** (multi-step modeler 主动占位) | **high** |

**A_full_ours vs A0_hybrid_pyfcstm 的 VGC mean lift** 是 paper §4 主报道数字 — 它隔离了"DSL 选 pyfcstm 但单靠 prompting 还是用不上"vs"加了我们 agent loop 的 deterministic feedback 后 grounding 真正生效"两件事。

### 6.1.1 与 Reference STM 比对的强化判定（v5.1）

对每个 case，**A 判定**（"semantic 是否被表达"）需要参照该 case 的 reference STM（见 §6.6）：

- reference STM 里如有该 semantic（如原文支持 C3 forced fault）→ A 判定关注 method 输出是否**正确**实现了该 semantic（同 event / 同 target state / 同语义）
- reference STM 里无该 semantic（如原文不支持 C1）→ method 输出的对应 semantic 不算分（防止"硬塞 feature"过拟合 VGC 指标）

这样 VGC 同时 capture "差异化能力"和"语义正确性"两件事，避免单纯 grep 的 false-positive。

### 6.2 `ParseRate`（辅 intrinsic）

$$\text{ParseRate} = \frac{|\{i : \texttt{parse}(\text{dsl}_i) \text{ succeeds}\}|}{N}$$

- pyfcstm condition：用 `pyfcstm.dsl.parse_with_grammar_entry`
- Umple condition：用 reproduction/baselines 已实装的 Umple parser wrapper（或 fallback regex 检查）

ParseRate 在 5 conditions 间应大致相近（≥ 0.9），如不是说明该 condition 的 prompt strategy 有 systematic issue。

### 6.3 `SemValidRate`（辅 intrinsic）

$$\text{SemValidRate} = \frac{|\{i : \texttt{sem-parse}(\text{ast}_i) \text{ succeeds}\}|}{N_{\text{Parse-ok}}}$$

- pyfcstm：`pyfcstm.model.parse_dsl_node_to_state_machine` 不抛 missing state / dangling transition / undefined var
- Umple：reproduction/baselines 的 Umple model load + 同类 sanity check

### 6.4 `SimRate`（辅 intrinsic — pyfcstm only）

$$\text{SimRate} = \frac{|\{i : \texttt{SimulationRuntime}(\text{sm}_i).\texttt{run\_until\_stable}() \text{ completes}\}|}{N_{\text{Sem-ok, pyfcstm}}}$$

跑一个完整 cycle 不触发 safety limit（1000 steps / 64 stack depth）。

**Umple condition 标 N/A** — Umple 无 speculative validation runtime，这本身是 §1.2 失败模式 "周期执行" 的体现（不是 evaluation bug）。

### 6.5 `ReachabilityRate`（辅 intrinsic — pyfcstm only）

$$\text{ReachRate}_i = \frac{|\{s \in S_i : s \text{ reachable from initial}\}|}{|S_i|}$$

调用 `pyfcstm.topology` reachability API。**Umple condition 同样 N/A**。

### 6.6 Reference STM 起草 pipeline（v5.1 — 全 15 case 全做 + AI 辅助 + 人工签字）

> **paper 口径**：reference STMs are **expert-authored** — author 在 AI 辅助起草基础上**逐 case 审阅签字**。AI 起草工具仅承担"机械化合规检查 + 草稿初稿"，**所有 ref 必须经过人工 audit 才进入 final set**。这是与 expansion NL pipeline 同源的"AI-assisted, expert-signed"流程。

**Pipeline 设计**（4 阶段，全 15 case 适用）：

```
Stage A: codex 起草 + 自验证
  ├─ input: STM.md §1 摘录 + §2 NL + expansion NL + paper.pdf + pyfcstm grammar + DSL examples
  ├─ codex 通过 Bash tool 调用 pyfcstm.dsl.parse / model.parse / simulate 自检
  ├─ 自检失败 → codex 内部 retry（max 5 iter）
  └─ output: codex_drafts/<id>.fcstm + codex_drafts/<id>.notes.md
        ↓
Stage B: claude 交叉评审
  ├─ input: Stage A 输出 + 同样的 source materials
  ├─ claude 评审 (semantic correctness / faithfulness to NL / C-axis grounding 合理性 / 无 hallucination)
  └─ output: claude_reviews/<id>.json
        {verdict: APPROVE | REVISE, comments: [...]}
        ↓
Stage C: 共识 + 修订 loop（若 REVISE）
  ├─ feedback claude comments → codex 修订
  ├─ codex 修订后再 self-validate
  ├─ revised draft → claude 再评审
  └─ max 3 轮 outer loop；若仍 REVISE 标 status=needs_human_intervention
        ↓
Stage D: bundle 生成
  ├─ 整合 NL（英文扩充）+ Chinese NL 译文 + ref pyfcstm DSL + verifier results + iteration history
  └─ output: bundles/<id>.md（per-case 一份，**用户审阅的入口文件**）
        ↓
Stage E: 用户 audit（人工签字）
  ├─ 用户逐 case 读 bundles/<id>.md
  ├─ 签字 / 标修订建议 / 必要时重写 DSL
  └─ output: audited/<id>.fcstm + audited/<id>.audit.md（user signed）
```

**Stage A codex 起草约束**：

1. 必须读 STM.md §1 原文摘录 + §2 NL + paper.pdf + expansion NL 四源
2. 必须通过 Bash 调用 pyfcstm 工具自检（parse + sem + sim 三关全过）
3. 必须只用原文出现过的 mode / event / variable / threshold 名（**禁止无中生有**）
4. 在原文支持的 C-axis 上**恰当**使用 pyfcstm grounding feature（不强行堆砌）
5. 规模匹配 codex 评审时的 scale 估计（不过度膨胀）

**Stage B claude 评审 rubric**（输出 JSON）：

```json
{
  "verdict": "APPROVE | REVISE",
  "semantic_correctness": {"score": "🟢/🟡/🟠/🔴", "evidence": "..."},
  "nl_faithfulness": {"score": "🟢/🟡/🟠/🔴", "evidence": "..."},
  "c_axis_grounding_appropriateness": {"score": "🟢/🟡/🟠/🔴", "evidence": "..."},
  "hallucination_check": {"found": [], "comment": "..."},
  "specific_revision_suggestions": ["..."],
  "overall_comment": "..."
}
```

**Stage D bundle 文件结构（用户审阅入口）**：

```markdown
---
case_id: 097
paper_slug: ...
case_name: ...
bucket: FSM-basic
domain: ✈️
generation:
  codex_iter: 2
  claude_iter: 1
  claude_verdict: APPROVE
  pyfcstm_verifier:
    parse_ok: true
    sem_ok: true
    sim_ok: true (1 cycle, no deadlock)
    reach_rate: 6/6
---

# Case <id>: <case_name>

## 1. 英文 NL（扩充版，含 inline [E] 溯源 markers）

[expanded_nl 原文，含 [E1] [E2] 等 markers]

## 2. 中文 NL 译文

[逐句中文翻译，便于审阅]

## 3. Reference pyfcstm STM

```pyfcstm
... DSL ...
```

## 4. C-axis grounding 使用情况

- **C1 (Per-cycle behavior)**: 用 / 未用，原因 ...
- **C2 (Numerical guard)**: ...
- **C3 (Forced fault)**: ...
- **C4 (Abstract action)**: ...

## 5. AI 起草 + 评审过程记录

### 5.1 codex 起草笔记
[codex_drafts/<id>.notes.md 内容]

### 5.2 claude 交叉评审
[claude_reviews/<id>.json 内容]

### 5.3 迭代历史
- iter 1: codex draft → parse 失败 line 23 → 修复
- iter 2: parse OK / sem OK / sim OK → claude APPROVE → bundle 生成

## 6. 用户审阅区（待填）

- [ ] 签字 approve
- [ ] 修订建议：
- [ ] 重写：
```

**落盘结构**：

```
eval/data/path2_selection/ref_stms/
├── codex_drafts/<id>.fcstm           # codex 一阶段起草
├── codex_drafts/<id>.notes.md
├── claude_reviews/<id>.json          # claude 评审结果
├── verifier_logs/<id>.log            # pyfcstm 验证输出
├── bundles/<id>.md                   # **用户审阅入口**（自动生成）
├── audited/<id>.fcstm                # 用户签字后 final ref
├── audited/<id>.audit.md             # 用户审阅笔记
└── BUILD_STATUS.md                   # 15 case 进度总账
```

### 6.7 可选 spot-check（complement to VGC，仅做 manual eval 的 case）

> **v5 重写 rationale**：原 v4 §6.6 把 audit-trail 抽查包装成 "reference-free intrinsic 与 manual gold 相关性证据"，作为 C5 contribution 的可信度桥。v5 删除 C5 后 + v5.1 加入 reference STM 后，spot-check 单纯定位为 "5-component 手工评测"作为 VGC + reference STM 之外的第三方独立信号。

从 15 候选抽 3-5 case 走 [`../eval/`](../eval/) LLM-初审 + 人类签字 5-component manual eval：

```bash
PYTHONPATH=. python eval/demo/run_demo.py \
  --cases case_a,case_b,case_c \
  --conditions A_full_ours,A0_hybrid_pyfcstm \
  --component-kinds states,transitions,guards,actions,hierarchical_states

# 你签字 eval/review/packs/<case>/<condition>/{states,...}.md
PYTHONPATH=. python eval/demo/finalize_after_signoff.py
```

判定：spot-check 这 3-5 case 上，`A_full_ours` 是否在 manual eval 上对 baseline 有同方向 lift（不要求 Pearson，只要 sign-aligned）。如果 manual eval 与 feature utilization / intrinsic 方向**不一致**，在 PATH2_REPORT §7 confounder 中显式披露。**不是 sprint 强制项。**

## 7. 结果落盘 schema

### 7.1 `predictions.parquet`

每行 = 1 (case_id, condition) 组合。15 candidates × 5 conditions = 75 行（备选另存为 backup_predictions.parquet）。

```text
columns:
- case_id: str           # source_dir 的 slug
- source_dir: str
- bucket: str            # FSM-basic | EFSM-interlock | HSM-layered
- domain: str            # 领域 emoji，与 sources/SUMMARY.md 同口径
- condition: str         # A0_single_umple | A0_hybrid_umple | A0_single_pyfcstm | A0_hybrid_pyfcstm | A_full_ours
- target_dsl: str        # umple | pyfcstm
- model: str             # 实际跑的 LLM_MODEL 值
- final_dsl: str         # 最终生成的 DSL 文本（Umple 或 pyfcstm，按 target_dsl 决定）
- iter_traces: list[dict]
- scenariogen_coverage: list[dict]   # Phase E v3 (f) 6-mutation 覆盖率（仅 A_full_ours 非空）
- token_usage: dict      # {prompt, completion, total}
- status: str            # ok | partial | failed (含具体失败阶段)
- feature_utilization: dict   # 主报道指标 — {during_block: bool, multi_var_guard: bool|None, forced_transition: bool, abstract_action: bool}
- intrinsic_scores: dict # {parse_ok: bool, sem_ok: bool, sim_ok: bool|None, reach_rate: float|None}
```

### 7.2 `summary.json`

```json
{
  "path": "path2",
  "data": "sources_path2_candidates_15",
  "n_samples": 15,
  "n_per_bucket": {"FSM-basic": 3, "EFSM-interlock": 6, "HSM-layered": 6},
  "conditions": ["A0_single_umple", "A0_hybrid_umple", "A0_single_pyfcstm", "A0_hybrid_pyfcstm", "A_full_ours"],
  "per_condition": {
    "A0_single_umple": {
      "target_dsl": "umple",
      "feature_utilization": {"during_block": 0.0, "multi_var_guard": null, "forced_transition": 0.0, "abstract_action": 0.0},
      "intrinsic": {"parse_rate": 0.XX, "sem_valid_rate": 0.XX, "sim_rate": null, "reach_rate": null},
      "token_total": 12345
    },
    "...同结构 4 个 condition...": null
  },
  "primary_comparisons": {
    "A_full_ours_vs_A0_hybrid_pyfcstm": {
      "feature_utilization_lift": {"during_block": "+XXpp", "multi_var_guard": "+XXpp", "forced_transition": "+XXpp", "abstract_action": "+XXpp"},
      "intrinsic_lift": {"parse_rate": "+Xpp", "sem_valid_rate": "+Xpp", "sim_rate": "+Xpp", "reach_rate": "+Xpp"},
      "interpretation": "isolates deterministic feedback contribution (same DSL target, same step count)"
    },
    "A_full_ours_vs_A0_hybrid_umple": {
      "feature_utilization_lift": "structural (Umple has 0% by construction)",
      "intrinsic_lift": {"parse_rate": "+Xpp", "sem_valid_rate": "+Xpp"},
      "interpretation": "method-of-record vs baseline-of-record (different DSL)"
    },
    "A0_hybrid_pyfcstm_vs_A0_hybrid_umple": {
      "feature_utilization_lift": {"during_block": "+XXpp (Umple cannot)", "...": "..."},
      "intrinsic_lift": {"sim_rate": "Umple N/A", "reach_rate": "Umple N/A"},
      "interpretation": "isolates DSL expressiveness gap (same strategy)"
    }
  },
  "per_bucket_lift": {
    "FSM-basic": {"A_full_ours_vs_A0_hybrid_pyfcstm": {...}},
    "EFSM-interlock": {...},
    "HSM-layered": {...}
  },
  "per_c_axis_stratified_lift": {
    "C1_exposed_cases": {"n": 6, "A_full_ours_vs_A0_hybrid_pyfcstm": {...}},
    "C2_exposed_cases": {"n": 9, "...": "..."},
    "C3_exposed_cases": {"n": 9, "...": "..."},
    "C4_exposed_cases": {"n": 14, "...": "..."}
  },
  "spot_check_subset": {
    "sampled_cases": ["case_a", "case_b", "case_c"],
    "manual_macro_f1_per_case_per_condition": {},
    "sign_aligned_with_feature_utilization": null,
    "sign_aligned_with_intrinsic": null
  },
  "confounders": []
}
```

## 8. `PATH2_REPORT.md` 产出要求

sprint 末 Phase 6 必须产出，**Claude 整理不下结论**。v5 新 outline：

1. **§1 控制系统问题定义 + 4 失败模式 + 4 grounding 一对一映射**：直接复用 GUIDE §1.1-§1.4 内容（categorical 框架）；这是 PATH2_REPORT 的论证骨架，不是只在 §7 里出现
2. **§2 method overview + 4 contribution 速查表**：复用 GUIDE §1.6 + §11.3 + §11.4；明确写 paper §1 contributions 是 C1-C4 method core（**不写 ref-free**）
3. **§3 实验配置 + 5 conditions 矩阵**：sources_path2 数据集组成（3 桶 × 9 领域）、LLM_MODEL 实际值、5 conditions 详细参数（n_iter / strategy / target_dsl / feedback_sources）
4. **§4 主结果表 — Feature utilization rate**：5 conditions × 4 feature 的使用率矩阵；高亮 A_full_ours vs A0_hybrid_pyfcstm 的 lift（隔离 deterministic feedback 收益）+ A0_hybrid_pyfcstm vs A0_hybrid_umple 的 gap（DSL expressiveness gap）
5. **§5 辅助表 — 4 intrinsic lift × 5 conditions × 3 buckets**：Umple condition 在 SimRate / ReachRate 上的 N/A 不是数据缺失，是 §1.2 失败模式的体现
6. **§6 per-C-axis stratified lift**：按 expansion axis_coverage 标签（C1🟢/C2🟢/C3🟢/C4🟢）分组，看 lift 是否真的落在对应 axis 上 — 这是 §1.3 三段论 mapping 的直接实证
7. **§7 spot-check / confounders / 信号判定**：3-5 case manual eval 结果（如做了 §6.6）；API 失败 / parse 失败样本；按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S1/S2/S3/S4 信号判定（**注意 v5 lift 算法不同**：S2 阈值改为"feature utilization mean lift ≥ 25pp"而非"4-intrinsic mean lift ≥ 20pp"）
8. **§8 后续工作量预估**：若选 Path 2，1-2 个月内要补的工作 — 接 Phase H judge 补 LLM-as-judge 通道、扩 sources/ 到 60 条、跨 vendor sanity (Claude vs GPT-5.5)、对照 llms_emp 两阶段 / IEC 61499 / ttool-ai 等更强 baseline、formal verification benchmark 集成等

**关键差异与 v4 outline 对比**：

- v4 §1 是 "实验配置 + meta info"；v5 §1 直接讲控制系统问题定义，是论证骨架
- v4 §2 主表是 4-intrinsic；v5 §4 主表是 feature utilization
- v5 新增 §6 per-C-axis stratified — 把 30 case 扩充 NL 的 axis_coverage 标签反向用于 lift 分组，是 §1.3 mapping 的直接验证
- v5 §7 信号判定从"intrinsic mean lift"改为"feature utilization mean lift"

## 9. 风险与回退（Path 2 特有 — v5 修订）

| 风险 | 触发 | 回退 |
| --- | --- | --- |
| Umple parse 出错率高 | reproduction/baselines 的 Umple parser wrapper 不稳 | 用 fallback regex 检查；在 PATH2_REPORT §7 confounder 显式披露 |
| pyfcstm `SimulationRuntime` 缺 abstract handler 报错 | A0_*_pyfcstm 大量样本 SimRate=0 | 用 no-op handler，sim 只检 reachability 不验业务逻辑（在 PATH2_REPORT §7 confounder 披露） |
| `ReachabilityRate` wrapper 未实装 | Phase 2 没补 reachability 接口 | 临时降到 3-intrinsic mean（parse / sem / sim），在 PATH2_REPORT §3 明确披露 |
| **Feature utilization 在 A0_*_pyfcstm 上意外高** | 单 prompt / Hybrid 已经主动用 4 类 feature | 这本身是有意义发现（"prompt-only 已经能 push pyfcstm grounding"），不必回退；在 PATH2_REPORT §4 讨论收益归因 |
| **Feature utilization lift 过低**（A_full_ours - A0_hybrid_pyfcstm mean lift $< 15$pp）| deterministic feedback 贡献不显著 | 按 discussion §4.1 S4 处理；可能需要补 LLM-as-judge feedback (Phase H) 才能拉开差距 |
| **A0_hybrid_pyfcstm 与 A0_hybrid_umple feature utilization 都接近 0** | 说明 LLM 即使 target pyfcstm 也不主动用 4 类 feature | 这是核心 differentiation 论证：feature utilization gap 完全来自我们的 agent loop deterministic feedback；在 PATH2_REPORT §4 明确写 |
| Umple Hybrid strategy 复现失败 | baseline_structure_event.py 的 Hybrid 4-step 行为不稳定 | 用 reproduction/baselines/baseline_structure_event.py 实装作为参考；若 reproduction 也跑不稳，标 confounder 不阻塞 |
| 可选 spot-check 双 LLM 一致率过低 | `eval/review/packs/` 中 🔴 / 🟡 行占比 $> 30\%$ | 仅影响该 case，不阻塞主指标；在 PATH2_REPORT §7 confounder 披露 |
| `LLM_API_KEY` / `LLM_ENDPOINT` 未 source | KeyError on `os.environ["LLM_ENDPOINT"]` | shell `source .env` 后重新执行 |

## 10. 完成度自检 checklist（v5 修订）

sprint Phase 7 收口前用此 checklist 核验：

- [x] `eval/data/sources_path2.parquet` 已落盘 = 15 candidates（commit `259e6ea7`）
- [x] `eval/data/sources_path2_backup.parquet` 已落盘 = 15 backup（commit `259e6ea7`）
- [ ] `method/loop.py` 加 `target_dsl` + `modeling_mode="hybrid"` 分支
- [ ] `method/prompts/modeler/hybrid_*.txt` × {umple, pyfcstm} 两版（共 8 prompt 文件）
- [ ] `method/run_path2.py` 实装 5-condition 分发 + checkpoint resume
- [ ] `eval/results/sprint_path2/predictions.parquet` 已落盘，含 15 × 5 = 75 主行
- [ ] `eval/results/sprint_path2/summary.json` 含 §7.2 全字段（feature utilization 主表 + 4 intrinsic 辅表 + per-bucket lift + per-C-axis stratified lift）
- [ ] `paper_v1/PATH2_REPORT.md` 写出 v5 §1-§8 全 outline
- [ ] `method/STATUS.md` 更新 Path 2 进度行
- [ ] GitHub PR #10 update（PR 描述含 PATH2_REPORT 关键 lift 数字）
- [ ] Confounder 样本数 $\le$ 总样本数 30%

## 11. Method + Contribution 详述（paper writing 直接复用素材）

> 本节集中讲清楚 Path 2 视角下我们的 method 是什么、contribution 是什么；既给 sprint 末 PATH2_REPORT.md §7 (Claude 方向建议) 提供 anchored framing，也给方向定后正式 paper §1 contributions + §3 method 提供直接可复用的写作素材。

### 11.1 Method overview — Agent loop with externally-grounded in-loop feedback

```text
NL input (sources/ T0+🟢 case from real industrial control system paper)
      |
      v
  [Multi-step Modeling]  走 method/gpt_client.py (LLM_MODEL from env)
      |  6 步 MTI 流水 (identify_state → identify_event → identify_variable →
      |                identify_transition → identify_action → build_pyfcstm)
      v
  current_model (pyfcstm DSL text)
      |
      +----+ Feedback Sources (gated cascade) +----------+
      |    |  ParseFeedback   (pyfcstm.dsl)              |
      |    |  SemanticFeedback (pyfcstm.model)           |
      |    |  SimFeedback     (pyfcstm.simulate         |
      |    |                   + scenariogen 自管 mutation|
      |    |                   coverage as bug probes)   |
      |    |  [JudgeFeedback   — Phase H 跳过，sprint 不用] |
      |    +----+--------------------------------+       |
      |         |
      v         v
  feedback_bundle (JSON schema)
      |
      v
  [Cascaded Repair]      走 method/gpt_client.py
      |  4 个 fix sub-prompt：fix_parse / fix_sem / fix_sim / fix_judge(占位)
      |  按 earliest-failing channel 路由 + 共享 pyfcstm grammar reference
      v
  next_model --> 回到 Feedback Sources, iterate N=3 rounds
      |
      v
  final_model (pyfcstm DSL) --> 进入 §6 4 个 intrinsic 指标计算（+ 可选 audit-trail 抽查）
```

### 11.2 Method 各组件细节

#### 11.2.1 LLM agent 链

1. **MTI 6-step Multi-step Modeler**（PR #11 Phase F 实装）：NL → 6 步流水（identify_state → identify_event → identify_variable → identify_transition → identify_action → build_pyfcstm）→ pyfcstm DSL
   - **设计目的**：把"自由文本"压成 5 个结构化 list 后再 assemble DSL，避免单 prompt 直接面对控制系统 NL（含传感器 / 执行器 / 联锁 / 故障恢复等多重信息）时陷入语言细节歧义；与 sprint plan v3 "Spec-driven LLM" 概念一致
   - **prompt 全英文**（paper 投稿英文，统一）；共享 pyfcstm grammar reference (`method/prompts/_pyfcstm_grammar.md`)
   - 替代方案 single_prompt（同代码内 `LoopConfig.modeling_mode="single_prompt"`）作 A0_single_pyfcstm；Hybrid 4-step 同代码（`modeling_mode="hybrid"`）作 A0_hybrid_pyfcstm
2. **ScenarioGen**（PR #11 Phase G+E v3 实装）：NL + 模型 → 多 step BDD scenarios + 6 mutation 覆盖率自检
   - **scenariogen self-validation**：scenariogen 后自动跑 6-mutation 覆盖率检查；任一类未被 catch → 用 `extra_directive` retry 直到覆盖
3. **Cascaded Repair**（PR #11 Phase E 实装）：(current DSL, feedback_bundle) → new DSL
   - 4 个 fix sub-prompt：`fix_parse.txt` / `fix_sem.txt` / `fix_sim.txt` / `fix_judge.txt`（占位）
   - 按 earliest-failing channel 路由；fix_sim 含 passing-scenarios 显式 preservation 段

#### 11.2.2 三个 deterministic feedback sources（externally grounded）+ scenariogen 自管

| Source | pyfcstm 入口 | 输出 schema 核心字段 | 在 paper §3 method 里是哪一条 contribution |
| --- | --- | --- | --- |
| Parse | `pyfcstm.dsl.parse_with_grammar_entry` | `{ok, line, col, expected_tokens, got, snippet}` | C3 (deterministic verifier) |
| Semantic | `pyfcstm.model.parse_dsl_node_to_state_machine` | `{ok, missing_states, dangling_transitions, undefined_vars, type_mismatches}` | C3 |
| Sim | `pyfcstm.simulate.SimulationRuntime` + scenariogen 多 step BDD probes（含 6-mutation 自检）| `{ok, scenario_violations, per_step_var_mismatches, runtime_error}` | **C3 + C4 + scenariogen self-managed mutation coverage** |
| ~~Judge~~ | ~~ex1 `ExpertReviewAgent`~~ | **Phase H 跳过，sprint 不接入；留作正式 paper 阶段补**  | ~~C6~~ → future work |

#### 11.2.3 Feedback 合并策略 + 迭代控制

- **gated cascade**：Parse 过 → Semantic 过 → Sim 过
- **scenariogen frozen-once**：scenarios 在 iter 循环外生成一次 + mutation 覆盖率自检；model 适配 scenarios 不反向
- **迭代上限 $N=3$**：feedback_bundle 全 ok 时提前 break，标记 `status="converged"`
- **不收敛回退**：3 轮仍有 feedback 不空时，取 iter_3 final_model 进评测，标 `status="not_converged"`

### 11.3 Contribution 详述（**Path 2 视角：method 为主 + 强化 pyfcstm → 控制系统价值论证**）

> **v4 修订（含 v4.1）**：原 v3 把 "Reference-free intrinsic + judge protocol" 与 "control system NL benchmark" 作 C1/C2 主 contribution，已撤销。v4.1 进一步根据用户反馈**删除原 C5 (Four-level event scoping + DSL-native module composition)**（理由：太侧重工程，不构成 paper-level method contribution），同时**新增 §11.3.0 三段论 framing 论证**（pyfcstm feature → LLM agent loop 能力 → 控制系统价值），把"为什么 pyfcstm 特性更贴合控制系统"这一论证链显式写清楚。

#### 11.3.0 pyfcstm feature → LLM 能力 → 控制系统价值（**Path 2 核心 framing**）

本子节回答：**为什么 pyfcstm 的差异化能力特别贴合控制系统 NL-to-STM 任务？只列特性不够 — 必须论证 pyfcstm feature 在 LLM agent loop 中给模型带来的具体能力，以及这些能力如何转化为控制系统场景的实际价值**。三段论：**pyfcstm feature → LLM agent capability → control system modeling value**。

##### 11.3.0.1 控制系统 NL-to-STM 与一般 reactive system 的 4 个本质区别

控制系统建模相对一般 reactive system（家电 / 办公设备 / 教学题）有 4 个本质区别：

1. **周期执行范式**：控制系统跑在 control cycle 上（PLC 扫描周期 / 嵌入式 superloop / ROS spin 周期），每个 cycle "读传感器 → 决策 → 写执行器"；状态机停在某个 mode 时**每个 tick 都要做事**（积分、滤波、监控、watchdog）。一般 reactive system 是事件驱动 — 状态机停下来等下次事件
2. **数值密集的守卫 / 效果**：控制系统 transition guard 含大量**复合数值条件**（温度阈值 / 距离阈值 / 流量约束 / 时序去抖 / 边沿检测）；effect 含 PID 计算 / 状态变量更新 / 累积量推进
3. **硬件解耦需求**：控制系统 STM 在生成阶段**无法决定 target deployment**（PC 仿真 / RTOS / PLC / 嵌入式 MCU / ROS 节点），必须符号占位 + 后期注入；不能在 DSL 里直接写宿主语言代码
4. **强 safety invariant + fault-recovery**：任何 mode 下都要 enforce 安全不变式（"温度 ≤ 最大值"、"距离 ≥ 最小值"、"流量 ∈ 允许区间"）；任何 mode 下 Error 事件触发都必须强制切到 fault-recovery 路径，**不能依赖具体 mode 内部的逻辑接收**

这 4 个本质区别决定了"通用 LLM-based STM 工具链（Umple / PlantUML / Mermaid / SysML / TTool）在控制系统场景下不胜任"的根本原因 — 不是工具链不能"画"控制系统状态机，而是**它们不在 generation loop 中暴露上述 4 类需求所需的 grounding signal**。

##### 11.3.0.2 三段论 mapping 表（4 行覆盖 4 条 method core）

下面 4 行对应 §11.3 中 C1-C4 四条 method core 各自的 **"(a) pyfcstm 给了什么 feature → (b) 这个 feature 在 LLM agent loop 中带来什么能力 → (c) 这个能力在控制系统场景的实际价值"** 论证链：

| pyfcstm feature | LLM agent loop 能力 | 控制系统场景价值 |
| --- | --- | --- |
| `SimulationRuntime` 内 deepcopy-snapshot speculative DFS validation + structured `SimulationRuntimeDfsError` (`pyfcstm/simulate/runtime.py:_validate_transition`) | agent 在每轮 repair 前能拿到"这条 transition 触发后该 mode 的子状态机能否 reach stable boundary"的 ground-truth 反馈，及具体 dead-end 模式（init 全失败 / pseudo 不停 / guard 互锁 / exit-vs-parent 循环） | 控制系统**多模式切换**（mode A → mode B）中"切过去后 mode B 子状态机无合法 init"这类 critical bug 在 generation 阶段就被识别，无需等到 deploy 后 runtime 死机；agent 拿到诊断后能定向修复 |
| `Expr` IR + `pyfcstm/solver/` Z3 集成（`expr_to_z3` / `execute_operations` / `solve`） | agent 在每轮 repair 前能拿到"这条 transition 的 guard 是否可达 (SAT)" / "effect 后变量空间是否满足下一 invariant" 的 SMT-grade 反馈，覆盖 22 个数学函数闭包 | 控制系统**数值密集 guard** (温度阈值、流量约束、传感器去抖、PID 计算后续条件) 可被符号求解；agent 能发现"这条 guard 在变量定义域内永不为真"或"effect 后违反 safety invariant"这类静态可证伪逻辑错误 |
| `>> during before/after` aspect actions (root→leaf→root cascade) + `!` forced transition (模型层递归展开到所有 descendant) | agent 可生成**跨所有叶子的 cross-cutting 行为**（监控、日志、安全断言）无需为每个 leaf 复制；可一行声明 fault-recovery escape 自动展开到所有适用子状态 | 控制系统**周期执行范式 + 强 safety invariant**：一行 `>> during after abstract AssertSafetyInvariant` 表达"任意 mode 下每周期都要检查安全上限"；**强 fault-recovery**：一行 `! * -> ErrorHandler :: Error` 表达"任意工作 mode 下 Error 都强制切到安全状态"；Umple 都需要在每一 mode level 手抄 |
| `enter abstract` / `during abstract` / `>> during before abstract` + `@abstract_handler` decorator + `ReadOnlyExecutionContext` (frozen) | agent 可在 generation 阶段产出**hardware-effector 占位符**不需要决定 deployment target；handler 在 runtime 反射注入，frozen context 防止 handler 修改 vars；两档错误处理（raise / log）把 handler 异常落到 structured field 供 agent 消费 | 控制系统**硬件解耦需求**：同一 STM 模型在 PC 仿真 / RTOS / 嵌入式 MCU 之间无修改部署；测试时 mock handler、deploy 时实硬件 handler；STM 模型保持"语义骨架"不动 |

##### 11.3.0.3 为什么 baseline 工具链（Umple / PlantUML / Mermaid / TTool / SysML）不胜任

不是这些工具不能"画"出控制系统状态机；问题在于它们**不能给 LLM agent loop 提供上述 4 行的 grounding signal**：

1. **Umple**：guard 是 host-language 代码片段，没有 language-independent IR → 无法 SMT 求解；no speculative validation → 死锁 / 不可达 transition 只在 codegen 后运行时暴露；no DSL-native aspect AOP → 控制系统 invariant 要手抄；no DSL-level abstract action → lifecycle hook 直接写宿主语言代码
2. **PlantUML / Mermaid**：纯渲染工具，**没有 runtime / simulation / verification 能力** — 在控制系统 LLM agent loop 中只是"画状态机的工具"，无 grounding signal
3. **ttool-ai**：有 JSON syntax check 但**没有 speculative validation**、**没有 Z3 solver**、**没有 aspect AOP**；TTool simulator 是 post-hoc 评分支撑，**不在 generation loop 内**
4. **IEC 61499 iterative refinement**：有 softPLC simulation 但**需要人类评论介入**驱动迭代；不是 fully automated
5. **SysML（标准而非工具）**：标准上有 statechart 表达力，但**没有特定 reference runtime 提供 in-loop grounding**

因此，**pyfcstm 在 LLM-based control system STM synthesis 任务中的不可替代性，不是"它有什么独家 feature"，而是"它把控制系统建模所需的 4 类 grounding signal（dead-end check / SMT 可达性 / cross-cutting + forced escape / hardware decoupling）全部做在了一个 fully-automated DSL toolchain 之内"**。这是 Path 2 paper 的 method core 的真正立论基础，也是 §11.3 下面 4 条 C1-C4 contribution 的统一 framing 锚点。

---

Path 2 视角下我们的 5 条 contribution（前 4 条 method core，第 5 条 evidence + enabling tooling）。**Path 2 与 Path 1 的差异**：method core (C1-C4) 是 paper-wide 一致的 4 条；但 Path 2 强化每条 method core 与控制系统具体场景的对应关系；evidence section 用 sources/ 真实工业控制系统 NL 而非家电 benchmark。

#### C1 — In-loop deterministic feedback via speculative validation（**method core**）

> "We integrate pyfcstm's cycle-based simulation runtime — featuring per-cycle deepcopy-snapshot speculative DFS validation bounded by 1000 steps, 64 stack frames, and structural-and-value signature pruning (`pyfcstm/simulate/runtime.py:_validate_transition`) — as a deterministic in-loop feedback source. The runtime rejects transitions whose downstream init / pseudo / parent-continuation chains cannot reach a stoppable boundary, and surfaces a structured `SimulationRuntimeDfsError` whose docstring enumerates pathological STM patterns."

**控制系统场景对应**：当 LLM 生成包含**多模式切换的控制器**时（如电梯模式切换、PLC 阶段控制、自动驾驶 supervisor mode 转换），speculative validation 能识别"某条 mode transition 触发后该 mode 的子状态机没有合法 init"这类病态。这对 Umple/PlantUML/Mermaid 这些**不在 runtime 层做 dead-end 检测**的工具链是无法替代的 grounding。

#### C2 — Language-independent expression IR enables symbolic reasoning without code generation（**method core，控制系统场景的关键 enabler**）

> "The DSL ships a unified `Expr` IR (`pyfcstm/model/expr.py`) supporting arithmetic / bitwise / logical / ternary / 22-function math closure required by state-machine guards and effects. The same IR is simultaneously (a) evaluable, (b) AST-round-trippable, (c) Z3-translatable via `pyfcstm/solver/expr.py:expr_to_z3`, and (d) renderable into 9 target languages. We exploit it to provide LLM agents with **guard SMT satisfiability** (`pyfcstm/solver/solve.py:solve`) and **symbolic effect propagation** (`pyfcstm/solver/operation.py:execute_operations`) as in-loop feedback — without ever leaving the DSL toolchain."

**控制系统场景对应**：控制系统状态机大量依赖**数值变量 + 复杂守卫条件**（温度阈值、距离阈值、流量约束、传感器去抖、PID 计算）。pyfcstm DSL 内可直接表达这类逻辑：

```fcstm
def int debounce_count = 0;
def float temp = 25.0;
def float threshold = 80.0;
state Wait {
    during {
        if [pressed >= 1] { debounce_count = debounce_count + 1; }
        else              { debounce_count = 0; }
    }
}
Wait -> Triggered : if [debounce_count >= 5 && abs(temp - target) < threshold] effect { debounce_count = 0; };
```

Z3-backed solver 让 agent loop 可以问"这条 transition 的 guard 是否可达？""effect 后变量空间满足下一 invariant 吗？" — Umple 的 host-language-bound guards 做不到。

#### C3 — DSL-native aspect AOP and forced fault paths align with control-system idioms（**method core，控制系统直接对应**）

> "We design our method around two pyfcstm DSL-level primitives that Umple, PlantUML, and Mermaid lack: (i) **aspect actions** `>> during before / after` cascading from root to leaf states at every cycle (`pyfcstm/model/model.py:iter_on_during_aspect_recursively`); and (ii) **forced transitions** `!` recursively expanded to every applicable descendant substate (`pyfcstm/model/model.py:_recursive_finish_states`)."

**控制系统场景对应**：

**Aspect actions** = 控制系统"每个周期都要做的事"的第一类原语：

```fcstm
state MotorControl {
    >> during before { tick = tick + 1; }              // 每周期递增 watchdog
    >> during after abstract AssertSafetyInvariant;    // 每周期注入 safety invariant 检查
    state Running { during { command_torque = kp * (target - position); } }
    state Stopped { during { command_torque = 0; } }
}
```

`>> during after` 在任意活跃叶子状态后都自动注入（root→leaf→root cascade），对应"任意 mode 下 invariant 都必须 hold"。Umple 要在每个叶子的 `do` 内手抄一遍。

**Forced transition** `!` = 控制系统"任何模式下 Error 触发必须切到 ErrorHandler"的一行 declarative encoding：

```fcstm
state Plant {
    ! * -> ErrorHandler :: Error;   // 任何子状态下 Error 都强制 escape
    state Idle;
    state Running { state Phase1; state Phase2; [*] -> Phase1; }
    state ErrorHandler { enter abstract NotifyOperator; }
}
```

Umple 需要手写每一层 escape 或借助 nested state 隐含规则（agent report §6.3）。

#### C4 — Abstract action + read-only context decouples symbolic STM from physical effectors（**method core，控制系统硬件解耦**）

> "Combining DSL-level abstract action declarations with Python-side `@abstract_handler` decorator and `ReadOnlyExecutionContext` (`pyfcstm/simulate/decorators.py` + `context.py`) lets the LLM synthesize STMs without committing to a deployment target."

**控制系统场景对应**：控制系统 STM 在生成阶段**不应该决定 deployment target**（PC 仿真 / RTOS / PLC / 嵌入式 MCU / ROS 节点）。pyfcstm 通过 DSL 级 abstract action 占位 + 反射式 handler 注入实现彻底解耦：

```fcstm
state CalibrationMode {
    enter { offset = 0; samples = 0; }
    enter abstract OpenValve;                          // hardware-specific, placeholder
    during { offset = offset + read_sensor(); samples = samples + 1; }
    exit { offset = offset / samples; }
    exit abstract CloseValve;                          // hardware-specific, placeholder
}
```

Python 侧：

```python
class HardwareHandlers:
    @abstract_handler('Plant.CalibrationMode.OpenValve')
    def open_valve(self, ctx):  # ctx is frozen ReadOnlyExecutionContext
        gpio.set_pin(VALVE_OUT, HIGH)
runtime.register_handlers_from_object(HardwareHandlers())
```

测试时 mock handler、部署时实硬件 handler — **STM 模型不变**。两档错误处理（`abstract_error_mode={raise, log}`）把 handler 异常落到 `error_info` / `abstract_handler_errors` 供 agent loop 消费。Umple 的 lifecycle hook 是 host-language-bound 代码，没有此抽象层（agent report §6.4 / §6.7）。

> **v5 修订**：原 v4 含 C5 "Empirical demonstration on real industrial control system NL + reference-free evaluation enabling tooling"，v5 删除。Evaluation methodology + sources/ benchmark 在 §6 描述为 sprint enabling tooling，不进 paper §1 contributions。Paper §1 contributions 是 **C1-C4 四条 method core**，全部对应 §11.3.0 三段论 framing。

### 11.4 paper §1 contributions 列表（Path 2 视角）

按 paper §1 排序，前 4 条都是 method core，每条都对应 pyfcstm 一个 control-system-specific 能力 + §11.3.0 三段论 framing 论证的一行：

| # | 类别 | contribution | 对应 pyfcstm feature | 控制系统场景价值 |
| --- | --- | --- | --- | --- |
| 1 | **method** | In-loop deterministic feedback via speculative validation | `SimulationRuntime` DFS validation + `SimulationRuntimeDfsError` | 多模式切换 dead-end 识别 |
| 2 | **method** | Language-independent expression IR enables symbolic reasoning | `Expr` IR + `solver/` Z3 集成 + 跨 9 语言渲染 | 复杂数值守卫 + Z3 可达性 + 跨部署目标 |
| 3 | **method** | DSL-native aspect AOP + forced fault paths | `>> during before/after` + `!` forced transition | per-tick invariant + 强制 fault-recovery escape |
| 4 | **method** | Abstract action + read-only context for effector-agnostic STM synthesis | `enter abstract` + `@abstract_handler` + `ReadOnlyExecutionContext` | 硬件解耦 + handler 反射注入 |

> 完整 LaTeX 模板 + 引用 key 等 paper drafting 阶段再具体写。

### 11.5 与 6 个 baseline 的方法学定位（速查表，paper §2 related work 直接复用）

完整 6-baseline 对照表见 §1.1。下面是 Path 2 视角的精简表：

| baseline | 方法学共同点 | 与我们的关键区别 |
| --- | --- | --- |
| structure_event_driven (#1) | 多步 prompting | **无 in-loop feedback**；reference-based eval；家电而非控制系统 |
| llms_emp (#2) | 多步 + in-loop feedback | feedback 仅 rule-based grammar/semantics，**无 sim/reach/judge**；reference-based eval；混合领域非纯控制系统 |
| IEC 61499 (#3) | 控制系统 + sim feedback | **需要 human-in-the-loop comments**；输出 IEC 61499 code 而非 STM |
| Automated Statechart Auto (#4) | 控制系统 | **微调而非 prompt-based**；Volvo 内部数据 + reference-based eval |
| Llama3 Umple (#5) | Umple 可执行性 check | 小模型 (8B)；**无 control system 语义**；reference-based eval |
| ttool-ai (#6) | 自动反馈循环 | feedback 是 JSON/syntax/约束 + post-hoc TTool simulator；**无 reachability witness**；系统级 spec 而非单 STM |

**v5 关键 framing 点**：Path 2 与 baseline 的差异 = **(i) 任务对象**：我们是**真实工业控制系统**（不是 generic reactive system / domain model / 系统级 spec / UML 教学）+ **(ii) DSL 选择**：我们用 pyfcstm（不是 Umple/PlantUML/Mermaid/SysML/AVATAR），因为只有 pyfcstm 在 DSL 层面提供 4 类控制系统 grounding feature + **(iii) feedback 机制**：我们用 fully-automated agent loop 把 4 类 grounding 在 generation 阶段就回灌。这三个差异共同构成 paper §1 contributions 的**单锚点 — 控制系统的 4 类 grounding 必须在 NL-to-STM pipeline 全链路（任务对象 + DSL + feedback）一致**。
