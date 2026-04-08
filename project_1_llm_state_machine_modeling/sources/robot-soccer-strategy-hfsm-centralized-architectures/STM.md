# Robot Soccer Strategy Based on Hierarchical Finite State Machine to Centralized Architectures - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 robot soccer 团队策略明确分成 tactics、roles、behaviors 三层，并给出战术触发条件、角色分配算法和角色到行为的映射，适合整理成标准 HSM 样本。

## 条目 1: Tactical-role hierarchical soccer-team coordinator

- 控制对象：通用控制与多机器人协同领域的机器人足球战术-角色分层协调器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 centralized robot soccer team 的分层决策控制器，上层选 tactics，中层分配 roles，下层为各角色挑选具体 behaviors。
- 判断：算。对象是真实多机器人协调控制系统，不是泛策略框架；原文明确说明层次状态机如何依据球区和控球状态选择战术，如何由“virtual coach”分配角色，以及每个角色如何执行行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract，行 38-47
> This strategy is divided into tactics, which are selected by a Hierarchical State Machine.
> Once a tactic has been selected, it is assigned roles to players, depending on the game conditions.
> Each role performs defined behaviors selected by the Hierarchical State Machine.
> To carry out the behaviors, robots are controlled by the lowest level of the Hierarchical State Machine.

#### 摘录 B

- 出处：第 3-4 页，Section `III. Arquitectura jerárquica`，行 180-201
> una vez la Máquina de Estado selecciona la táctica, un agente virtual llamado “técnico” asigna un conjunto de roles ... a un número finito de agentes.
> Los jugadores con sus respectivos roles ejecutan un comportamiento ... seleccionado por el segundo nivel de la Máquina de Estado utilizando las condiciones ambientales St como transiciones.
> El control de los comportamientos es realizado por la capa más baja de la Máquina de Estado.
> ... cuando estas condiciones cambian, una nueva táctica es seleccionada y un nuevo conjunto de roles es asignado a los jugadores.

#### 摘录 C

- 出处：第 6-7 页，Section `A. Asignación de roles`，行 348-381
> hay 4 jugadores por equipo. Uno de ellos es el portero ... el único rol constante.
> existe un número finito de agentes A={a1, a2, a3}, que ejecutan un conjunto de roles R={rd, rs, ra}, donde rd corresponde al defensa, rs es el mediocampista y ra corresponde al delantero.
> El técnico C ejecuta el algoritmo de asignación de roles, dependiendo de la táctica previamente seleccionada.
> Táctica defensa: el jugador más cercano al balón se convierte en el defensa rd ... el jugador más cercano a la portería oponente es el delantero ra ... el último jugador es el mediocampista rs.

#### 摘录 D

- 出处：第 7 页，Section `B. Selección de comportamientos`，行 525-540
> Diferentes roles han sido diseñados con el fin de ejecutar distintos comportamientos, dependiendo de la táctica seleccionada.
> ... cada rol en cada táctica posee un comportamiento principal.
> Ir por el balón ... hasta la distancia donde se considera que tiene posesión del mismo (0.08m).
> Bloquear jugador oponente ...
> Ir a la mitad del campo de juego ...

### 2. 基于原文整理后的自然语言描述

The robot-soccer coordination architecture is explicitly organized as a hierarchical finite-state machine in which the top layer selects a team tactic, the middle layer assigns player roles, and the bottom layer executes the role-specific robot behaviors. Tactic selection depends on game conditions such as ball position and ball possession, and whenever those conditions change, the hierarchy can switch to a new tactic and trigger a fresh role reassignment. After a tactic is chosen, a virtual coach assigns the non-goalkeeper agents to the finite role set `rd / rs / ra`, corresponding to defender, midfielder, and attacker, using geometric criteria such as distance to the ball and distance to the opponent goal. The paper spells out those assignments algorithmically, for example in the defense tactic the closest player to the ball becomes defender, the closest player to the opponent goal becomes attacker, and the remaining player becomes midfielder. Once roles are fixed, the lower HSM layer selects behaviors such as `go for the ball`, `block opponent`, or `move to midfield`, so the overall controller combines tactic switching, role reallocation, and behavior execution in one layered decision system.

### 3. 逐句溯源

1. 句子 1：The robot-soccer coordination architecture is explicitly organized as a hierarchical finite-state machine in which the top layer selects a team tactic, the middle layer assigns player roles, and the bottom layer executes the role-specific robot behaviors.
   对应摘录：A, B
2. 句子 2：Tactic selection depends on game conditions such as ball position and ball possession, and whenever those conditions change, the hierarchy can switch to a new tactic and trigger a fresh role reassignment.
   对应摘录：A, B
3. 句子 3：After a tactic is chosen, a virtual coach assigns the non-goalkeeper agents to the finite role set `rd / rs / ra`, corresponding to defender, midfielder, and attacker, using geometric criteria such as distance to the ball and distance to the opponent goal.
   对应摘录：B, C
4. 句子 4：The paper spells out those assignments algorithmically, for example in the defense tactic the closest player to the ball becomes defender, the closest player to the opponent goal becomes attacker, and the remaining player becomes midfielder.
   对应摘录：C
5. 句子 5：Once roles are fixed, the lower HSM layer selects behaviors such as `go for the ball`, `block opponent`, or `move to midfield`, so the overall controller combines tactic switching, role reallocation, and behavior execution in one layered decision system.
   对应摘录：A, D
