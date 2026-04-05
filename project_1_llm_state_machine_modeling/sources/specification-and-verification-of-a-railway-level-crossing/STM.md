# Specification and Verification of a Railway Level Crossing - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文同时建模了二类和三类铁路平交口，其中二类道口的 `7` 态栏杆/红灯/声响控制机连同 `T15 / Ttrans` 时序延迟写得最完整，可直接形成 `🚆` 方向双 A 样本。

## 条目 1: Seven-State Barrier Crossing Supervisor with T15/Ttrans

- 控制对象：轨道交通与铁路控制领域的二类铁路平交口栏杆、红灯与声响控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 Infrabel 新铁路平交口系统的二类道口逻辑控制器，用输入变量、内部命令变量和时钟共同决定红灯、白灯、声响与栏杆的开闭状态。
- 判断：算。对象是实际铁路 level crossing 的安全控制逻辑，原文明确说明系统周期、输入/内部/输出变量、时钟变量以及二类道口的 7 个状态与状态进入条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 14-16 页，Chapter 3 `Modélisation`
> Le passage à niveau peut être dans différents états ... Pour les passages à niveau de 2e catégorie, il y a 7 états possibles, et pour ceux de 3e catégorie, il y a 2 états possibles. ... Les cycles se déroulent de la manière suivante : le système lit l’état des variables d’entrée ; il calcule la nouvelle valeur pour certaines variables internes ... le système définit le nouvel état ; il met à jour les horloges ; il calcule les valeurs des variables de sortie.

#### 摘录 B

- 出处：第 20-21 页，Section 3.4 `Horloges`
> * T15 est une variable entière qui correspond à l’horloge qui permet d’attendre un délai avant la fermeture des barrières ... * Ttrans est le délai qu’il faut attendre avant de commencer à fermer les barrières lorsque le passage à niveau est commandé à la fermeture. Elle est liée à l’horloge T15.

#### 摘录 C

- 出处：第 22-25 页，Section 3.5.2 `2e catégorie`
> Nous avons donc 7 états ... PNouvert ... Avert_techn ... Avert_train ... les feux rouges et le signal sonore sont déjà actifs ... les barrières ne se ferment pas encore (T15 ≤ Ttrans). ... Barrière_fermeture ... T15 > Ttrans. ... PNfermé_correct ... les barrières sont contrôlées fermées ... au moins un feu rouge de chaque poteau-feu est allumé. ... PNfermé_dégradé ... avec une erreur ... Barrière_ouverture ... le passage à niveau est commandé à l’ouverture mais les barrières ne sont pas encore toutes contrôlées ouvertes.

#### 摘录 D

- 出处：第 27-28 页，Section 3.6.2 `Erreurs détectées dans les spécifications`
> Dans le modèle, la condition pour passer de l’état Avert_train à l’état Barrière_fermeture T15 > Ttrans. ... Celle-ci est l’horloge qui est démarrée dans l’état Avert_train et incrémentée tant qu’on reste dans cet état. Lorsqu’elle dépasse la constante Ttrans, le système passe en état Barrière_fermeture.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller is modeled as a cyclic state machine that reads input measurements, updates internal command variables, computes a new crossing state, advances clocks, and then emits barrier, light, and audible-output commands. For second-category crossings, the supervisor has seven explicit states: `PNouvert`, `Avert_techn`, `Avert_train`, `Barrière_fermeture`, `PNfermé_correct`, `PNfermé_dégradé`, and `Barrière_ouverture`, with state membership determined jointly by the open/close command `CLX`, barrier-position feedback, and red-light feedback. The closing sequence is time-gated by the integer clock `T15`: once the crossing is commanded to close, the system enters `Avert_train`, turns on red lights and sound, but keeps barriers stationary while `T15 <= Ttrans`. Only when `T15 > Ttrans` does the controller advance to `Barrière_fermeture`, so barrier descent is explicitly delayed rather than immediate. After that, the machine distinguishes normal closed operation from degraded closed operation according to whether all barriers are confirmed closed and each signal post still shows at least one red light, and it uses `Barrière_ouverture` as a separate reopening branch until all barriers are again confirmed open.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller is modeled as a cyclic state machine that reads input measurements, updates internal command variables, computes a new crossing state, advances clocks, and then emits barrier, light, and audible-output commands.
   对应摘录：A
2. 句子 2：For second-category crossings, the supervisor has seven explicit states: `PNouvert`, `Avert_techn`, `Avert_train`, `Barrière_fermeture`, `PNfermé_correct`, `PNfermé_dégradé`, and `Barrière_ouverture`, with state membership determined jointly by the open/close command `CLX`, barrier-position feedback, and red-light feedback.
   对应摘录：C
3. 句子 3：The closing sequence is time-gated by the integer clock `T15`: once the crossing is commanded to close, the system enters `Avert_train`, turns on red lights and sound, but keeps barriers stationary while `T15 <= Ttrans`.
   对应摘录：B, C
4. 句子 4：Only when `T15 > Ttrans` does the controller advance to `Barrière_fermeture`, so barrier descent is explicitly delayed rather than immediate.
   对应摘录：C, D
5. 句子 5：After that, the machine distinguishes normal closed operation from degraded closed operation according to whether all barriers are confirmed closed and each signal post still shows at least one red light, and it uses `Barrière_ouverture` as a separate reopening branch until all barriers are again confirmed open.
   对应摘录：C
