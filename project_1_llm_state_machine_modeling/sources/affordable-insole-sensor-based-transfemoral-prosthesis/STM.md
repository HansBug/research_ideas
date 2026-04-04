# An Affordable Insole-Sensor-Based Trans-Femoral Prosthesis for Normal Gait - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 `plantar insole -> gait segment classifier -> finite-state damping supervisor -> PI current loop` 两层控制链，并把 `loading response / mid-stance / terminal stance / pre-swing / swing` 五段 gait state 与 state-specific damping 写得很细，可直接作为 `HSM + T0` 样本。

## 条目 1: Two-level insole-driven damping supervisor for an MR-damper transfemoral prosthesis
- 控制对象：基于 plantar insole 的 transfemoral prosthesis gait-phase damping supervisor
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 MR-damper 股骨假肢的两层控制器，用 plantar insole 的四组开关状态识别五段 gait cycle，再由外层 finite-state controller 生成阻尼电流参考、内层 PI controller 跟踪执行。
- 判断：算。对象是真实 transfemoral prosthesis 控制系统；原文不仅给出 gait segments 与 sensor-state mapping，还给出 state-specific damping strategy 和外层/内层控制职责分工。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-6 页，Sections `2.2` 与 Table `1`，行 174-213
> It is composed of 24 switches strategically placed on the heel (`S1`), mid-foot (`S2`), metatarsal (`S3`), and toe (`S4`) of the plantar insole ... ROSs are formed for various biomechanical events corresponding to different phases of a gait cycle ... loading response, mid-stance, terminal stance, pre-swing, and swing.
>
> Table 1. Sensor states during different phases of gait.
> `Loading Response 1 0 0 0`
> `Mid-Stance 1 1 0 0`
> `Terminal-Stance 0 1 0 0 / 0 1 1 0 / 0 1 1 1`
> `Pre-Swing 0 0 1 1 / 0 0 0 1`
> `Swing 0 0 0 0`

#### 摘录 B
- 出处：第 7 页，Section `2.4. Control Approach`，行 248-259
> A two-level control scheme was employed to achieve able-bodied gait kinematics ... The control approach involves a finite state controller as a secondary controller and a conventional PI controller as a primary controller. The secondary controller generates the required current references for the MR damper using a finite state machine that ultimately modulates the impedance of the gait, depending on the gait event segment. The primary controller is a closed loop PI controller for MR damper current, which compensates for the load transfer dynamics, thus enabling the faithful tracking of current references ...

#### 摘录 C
- 出处：第 7 页，Section `2.4. Control Approach`，行 261-274
> The states of the finite state machine were determined by considering various demanded requirements; here we intend to achieve the flexion-extension of the knee during the stance phase with a high degree of stability and a suitably damped swing phase to adjust the walking speed. ... a gait cycle with five segments/phases ... loading response, mid-stance, terminal stance, pre-swing, and swing. ... the introduction of a foot plantar insole with four sensor groups provides a total of 16 states, out of which 15 belong to stance phase and one to swing phase. ... only 7 states of stance can be assigned to four phases as tabulated in Table 1, whereas the remaining 8 states of stance do not represent any of the ROS segments.

#### 摘录 D
- 出处：第 8 页，Section `2.4. Control Approach`，行 278-290
> In state 0, the knee flexes near to the maximum stance flexion. A relatively high damping was applied during this state to prevent buckling at the knee due to the user’s weight. During state 1, the knee begins to extend after maximum flexion ... requiring a high damping.
>
> State 2 involves the flexion-extension while the heel is off the ground and the sound limb is sharing the body weight, a moderate damping shall serve the purpose here. State 3 encounters the extension with a high rate of change and low body weight bearing; a low damping will provide the desired profile. The final state (state 4) represents a large knee flexion and associated extension after flexing to its maximum ... a very small damping ...
>
> All states can be tuned to suitable current references which can be accurately followed by a well-designed PI controller.

### 2. 基于原文整理后的自然语言描述

The affordable transfemoral prosthesis is organized as a two-level hierarchical controller in which a plantar-insole event recognizer first converts four sensor-group states (`S1` heel, `S2` mid-foot, `S3` metatarsal, `S4` toe) into gait segments, and a secondary finite-state controller then issues MR-damper current references that are tracked by an inner closed-loop PI current controller. The outer supervisor models walking with five gait phases, namely `loading response`, `mid-stance`, `terminal stance`, `pre-swing`, and `swing`, using the sequential insole patterns listed in Table 1, including `1000` for loading response, `1100` for mid-stance, `0111/0110/0100` for terminal stance, `0011/0001` for pre-swing, and `0000` for swing. Although the insole can theoretically generate sixteen sensor combinations, the controller explicitly keeps only the seven stance combinations that correspond to real roll-over-shape events plus one swing pattern, and ignores the remaining stance combinations as non-segment states. At the actuation level, state `0` and state `1` both demand high damping to prevent buckling and control slow post-flexion extension, state `2` uses moderate damping for heel-off shared-weight motion, state `3` lowers damping for rapid extension under reduced load, and state `4` applies very small damping during the large-flexion swing state. This preserves both the hierarchical controller split and the full gait-segment-to-damping mapping, making the paper a detailed `HSM + T0` prosthesis-control case.

### 3. 逐句溯源

1. 句子 1：The affordable transfemoral prosthesis is organized as a two-level hierarchical controller in which a plantar-insole event recognizer first converts four sensor-group states (`S1` heel, `S2` mid-foot, `S3` metatarsal, `S4` toe) into gait segments, and a secondary finite-state controller then issues MR-damper current references that are tracked by an inner closed-loop PI current controller.
   对应摘录：A, B
2. 句子 2：The outer supervisor models walking with five gait phases, namely `loading response`, `mid-stance`, `terminal stance`, `pre-swing`, and `swing`, using the sequential insole patterns listed in Table 1, including `1000` for loading response, `1100` for mid-stance, `0111/0110/0100` for terminal stance, `0011/0001` for pre-swing, and `0000` for swing.
   对应摘录：A, C
3. 句子 3：Although the insole can theoretically generate sixteen sensor combinations, the controller explicitly keeps only the seven stance combinations that correspond to real roll-over-shape events plus one swing pattern, and ignores the remaining stance combinations as non-segment states.
   对应摘录：C
4. 句子 4：At the actuation level, state `0` and state `1` both demand high damping to prevent buckling and control slow post-flexion extension, state `2` uses moderate damping for heel-off shared-weight motion, state `3` lowers damping for rapid extension under reduced load, and state `4` applies very small damping during the large-flexion swing state.
   对应摘录：D
5. 句子 5：This preserves both the hierarchical controller split and the full gait-segment-to-damping mapping, making the paper a detailed `HSM + T0` prosthesis-control case.
   对应摘录：A, B, C, D
