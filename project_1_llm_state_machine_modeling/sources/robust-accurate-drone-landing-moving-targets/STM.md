# A Robust and Accurate Landing Methodology for Drones on Moving Targets - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 moving-target visual sliding landing 组织成 `Stage 1-3 + Fail-safe` 的分层任务机，并把搜索、贴靠、居中、进近、gimbal 调节和 touchdown 主链写得很清楚。

## 条目 1: Three-stage visual-sliding-landing mission supervisor

- 控制对象：航空航天与飞行/空管控制领域的移动目标无人机视觉滑降监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于多旋翼无人机在移动目标上执行 visual sliding landing 的高层任务状态机，按 `Stage 1-3` 组织起飞、目标搜索、贴靠跟踪、最终下落和 fail-safe 恢复。
- 判断：算。对象是实际无人机 landing supervisor，而不是单独的视觉识别或 PID 调参模块；原文直接列出了各阶段和子状态名，并给出 1 m 起飞高度、`1.5 m -> 1 m` 距离收缩和 `-45° -> 0° -> 20°` gimbal 调节链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 9-10 页，`4.2 Controlling Algorithms / Figure 12`，`paper_content.txt` 第 354-368 行
> Informally the VSL use-case contains the following four steps: (a) At ﬁrst, the drone tries to detect the helipad which is relatively horizontal and large and can be detected from a signiﬁcant distance. (b) Then the drone approaches the helipad, while maintaining it in the center of the camera’s FoV. While approaching, the drone gimbal camera is tilted with respect to the distance between the drone and the helipad. (c) Once the drone can robustly detect the guiding target ... the drone position itself at a ﬁxed distance and angle relative to the guiding target. (d) In the ﬁnal stage, the drone descends on the helipad vertically, while maintaining a ﬁxed distance to the guiding target.
>
> Before presenting the algorithm, we deﬁne several possible modes for the drone state machine (see Figure 12).

#### 摘录 B

- 出处：第 10-11 页，`4.3 VSL Algorithm`，`paper_content.txt` 第 369-402 行
> The visual sliding landing (VSL) algorithm is based on the states deﬁned above and state machine (see Figure 12).
>
> • Disarmed ... • Arm ... • Take Off : The drone starts ﬂying upwards and reaches a predeﬁned altitude (e.g., 1 m). • Mission ... • Search Target ... • Leash Tracking ... • Centering ... • Helipad Approach ... • Guiding Target Tracking ... • Gimbal Adjustment : The camera angle is moved according to the drop (e.g., distance 3 m, angle –45°). • Final Approach ... • Touchdown ... • Fail-safe : The drone detects some kind of abnormality or risk ... and will return to a “safe-stage” according to the type of error and its fail-safe policy.

#### 摘录 C

- 出处：第 11-13 页，`Hover and Landing / Safe Landing`，`paper_content.txt` 第 411-420、466-479 行
> After ﬁxing the orientation we would like to shift the focus from the big target to the small target and keep a "leash" of 1.5m from it while changing the gimbal angle to 0°. The next step will be landing, so to accomplish this we close the distance to 1m and change the gimbal angle to 20°.
>
> The parameters can be divided into three groups: (i) Drone parameters ... (ii) Helipad parameters ... (iii) Drone to helipad parameters: e.g., drone to helipad relative speed, or marker tracking conﬁdence ... The credibility factor is the overall combined parameter which takes into consideration all the parameters above and also checks for abnormality or risk.

### 2. 基于原文整理后的自然语言描述

The drone landing controller is organized as a three-stage HSM for visual sliding landing on moving targets, with a global `Fail-safe` branch that can pull the system back to a safe stage whenever hardware faults, RC link loss, or target loss is detected. In `Stage 1`, the vehicle moves through `Disarmed`, `Arm`, `Take Off`, and `Mission`, so the landing routine is embedded in a larger flight task rather than being treated as an isolated terminal action. `Stage 2` contains the target-acquisition and pre-approach chain `Search Target -> Leash Tracking -> Centering -> Helipad Approach`, where the UAV first finds the large helipad marker, keeps it inside the camera field of view, and reaches an approach funnel with fixed distance and angle. `Stage 3` then refines the landing on the smaller guiding target through `Guiding Target Tracking -> Gimbal Adjustment -> Final Approach -> Touchdown`. During this terminal chain the controller first maintains a `1.5 m` leash while moving the gimbal to `0°`, then closes the distance to `1 m` and changes the gimbal to `20°` before descending vertically onto the helipad. The safe-landing envelope additionally checks drone limits, helipad slope, relative speed, and marker-tracking confidence, so the discrete stage logic is explicitly tied to operational landing risk.

### 3. 逐句溯源

1. 句子 1：The drone landing controller is organized as a three-stage HSM for visual sliding landing on moving targets, with a global `Fail-safe` branch that can pull the system back to a safe stage whenever hardware faults, RC link loss, or target loss is detected.
   对应摘录：A, B
2. 句子 2：In `Stage 1`, the vehicle moves through `Disarmed`, `Arm`, `Take Off`, and `Mission`, so the landing routine is embedded in a larger flight task rather than being treated as an isolated terminal action.
   对应摘录：B
3. 句子 3：`Stage 2` contains the target-acquisition and pre-approach chain `Search Target -> Leash Tracking -> Centering -> Helipad Approach`, where the UAV first finds the large helipad marker, keeps it inside the camera field of view, and reaches an approach funnel with fixed distance and angle.
   对应摘录：A, B
4. 句子 4：`Stage 3` then refines the landing on the smaller guiding target through `Guiding Target Tracking -> Gimbal Adjustment -> Final Approach -> Touchdown`.
   对应摘录：B
5. 句子 5：During this terminal chain the controller first maintains a `1.5 m` leash while moving the gimbal to `0°`, then closes the distance to `1 m` and changes the gimbal to `20°` before descending vertically onto the helipad.
   对应摘录：C
6. 句子 6：The safe-landing envelope additionally checks drone limits, helipad slope, relative speed, and marker-tracking confidence, so the discrete stage logic is explicitly tied to operational landing risk.
   对应摘录：B, C
