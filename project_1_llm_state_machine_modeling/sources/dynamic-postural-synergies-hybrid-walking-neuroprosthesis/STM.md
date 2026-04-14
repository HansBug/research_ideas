# A Control Scheme That Uses Dynamic Postural Synergies to Coordinate a Hybrid Walking Neuroprosthesis: Theory and Experiments - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把混合神经假体写成“顶层步态 FSM + 双边 synergy controller + 明确刺激时间参数”的层次控制结构，状态、触发、输出和脉冲时间语义都比较完整，可直接入账为 `HSM + T1` 样本。

## 条目 1: Hierarchical step-sequencing supervisor for the hybrid walking neuroprosthesis
- 控制对象：混合 walking neuroprosthesis 的 step-sequencing FSM 与双边 synergy-based gait controller
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向混合步行神经假体的层次监督控制器，顶层 FSM 负责选择半步/整步状态，底层两个 adaptive synergy-based controller 分别驱动双腿的 hip/knee motor 与 FES stimulation。
- 判断：算。对象是真实神经假体控制器而非实验流程；原文明确给出了离散状态、按钮触发、腿间角色切换、输出轨迹/协同激活以及刺激频率和脉宽。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Section `2.4. Finite State Machine`，行 13-25
> 2.4. Finite State Machine
> The hybrid neuroprosthesis used for experimental
> demonstration uses 4 electric motors; one on each hip joint
> and knee joint, and 4 stimulation channels; the quadriceps and
> hamstrings of each leg. The hybrid neuroprosthesis is controlled
> using two of the adaptive synergy-based PID-DSC controller
> with delay compensation working in tandem to produce gait,
> one for each leg. The Finite State Machine, shown in Figure 6,
> is used to determine which trajectories and synergy activations
> of the gait sequence are used; i.e., either half right step (State 1),
> full left step (State 2), or full right step (State 3). In between the
> active states; State 1–3, the standby state (State 0) is activated by
> default, in which the motors at the joints hold their positions and
> the synergy activations are set to zero.

#### 摘录 B
- 出处：第 12 页，Section `2.4. Finite State Machine`，行 4-12
> in a state, it becomes the swing leg and its counterpart becomes
> the stance leg. When a leg becomes the stance leg the controller
> only uses feedback to track the stance hip trajectory and hold
> the position of the knee joint. The progression of the FSM is
> determined by the progression button, in which the ﬁrst time it
> is pressed State 1 is activated, then each time it is pressed after
> that the even transitions activate State 2 and the odd transitions
> activate State 3. In addition to the progression button, there is a
> safety button which turns oﬀ all inputs when pressed.

#### 摘录 C
- 出处：第 12 页，Section `2.5. Experimental Demonstration`，行 27-42
> Nm. A RehaStim 8-channel stimulator (Hasomed Inc., DE) was
> used to generate the current modulated biphasic pulse trains used
> to elicit muscle contractions. A set of transcutaneous electrodes
> was placed on the quadriceps and hamstring muscle groups. The
> current modulated pulse train with a frequency of 35Hz and
> a 400µs pulse width is typically used for all experiments. An
> assistive support device, called an E-Pacter (Rifton, USA), is used
> for the experiments to help the subjects maintain their balance
> and propel themselves forward. An xPC target ... was used to
> interface with the diﬀerent sensors and motor drivers
> and implement the controller in real-time at 1 kHz. The control
> algorithms were coded in Simulink ...
> The hybrid neuroprosthesis is controlled using a
> button to control the progression of gait and an emergency stop
> button to stop all the inputs.

#### 摘录 D
- 出处：第 12 页，Section `2.5. Experimental Demonstration`，行 47-58
> these experiments it is assumed that the behavior of the right and
> left leg are similar, therefore, both States 2 and 3 use the same
> synergies and activations computed in the previous sections. The
> optimizations to compute the synergies, their activations, and
> the trajectories they produce were performed using the subject’s
> height and weight, but the model used the muscle parameters
> reported in Popović et al. (1999) for an able-bodied subject and
> person with SCI, respectively. If this system is to be implemented
> on a subject with a condition in which one leg’s response is much diﬀerent than the other, it would probably
> be more beneﬁcial to use multiple subject-speciﬁc models, one
> for each leg.

### 2. 基于原文整理后的自然语言描述

The hybrid walking neuroprosthesis is organized as a hierarchical controller in which two adaptive synergy-based PID-DSC gait controllers operate at the leg level while a top-level finite-state machine decides which step template is active. The discrete supervisor contains `State 0` standby, `State 1` half right step, `State 2` full left step, and `State 3` full right step; when one leg is activated it becomes the swing leg, while the opposite leg is reassigned as the stance leg whose controller only tracks the stance hip trajectory and holds the knee position. State progression is event driven by a progression button, with the first press entering `State 1`, even subsequent transitions selecting `State 2`, odd subsequent transitions selecting `State 3`, and a dedicated safety button shutting off all inputs. The state outputs are the trajectories and synergy activations loaded for each leg, and the implementation adds explicit engineering-time semantics because the stimulation layer uses biphasic pulse trains at `35 Hz` with `400 µs` pulse width and runs in real time at `1 kHz`.

### 3. 逐句溯源

1. 句子 1：The hybrid walking neuroprosthesis is organized as a hierarchical controller in which two adaptive synergy-based PID-DSC gait controllers operate at the leg level while a top-level finite-state machine decides which step template is active.
   对应摘录：A
2. 句子 2：The discrete supervisor contains `State 0` standby, `State 1` half right step, `State 2` full left step, and `State 3` full right step; when one leg is activated it becomes the swing leg, while the opposite leg is reassigned as the stance leg whose controller only tracks the stance hip trajectory and holds the knee position.
   对应摘录：A, B
3. 句子 3：State progression is event driven by a progression button, with the first press entering `State 1`, even subsequent transitions selecting `State 2`, odd subsequent transitions selecting `State 3`, and a dedicated safety button shutting off all inputs.
   对应摘录：B, C
4. 句子 4：The state outputs are the trajectories and synergy activations loaded for each leg, and the implementation adds explicit engineering-time semantics because the stimulation layer uses biphasic pulse trains at `35 Hz` with `400 µs` pulse width and runs in real time at `1 kHz`.
   对应摘录：A, C, D
