# Development of a Hierarchical Driver Aid for Parallel Parking Using Fuzzy Biomimetic Approach - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机） / Hybrid（混成状态机）
- 代表时间级别：T0（无关键时间语义） / T3（混成时间 / 连续时间耦合）
- 结构标签概况：层次、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文给出了具体并联泊车辅助系统的感知-HMI-驾驶指令链路，以及 Stage 1 / Stage 2 两阶段控制与触发切换逻辑。

## 条目 1: Vision-based parking advice loop
- 控制对象：并联泊车辅助系统中的视觉感知与驾驶指令生成逻辑
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车载驾驶辅助领域的并联泊车辅助系统，用于从双摄像头图像中提取车辆与车位关系，并通过 HMI 向驾驶员给出实时操作指令。
- 判断：算。对象是实际车辆泊车辅助控制系统，原文直接说明了感知输入、模糊决策和图形化驾驶建议输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，`3. Overview of the System`，行 212-214
> Parallel parking driver aid system, which will
> be referred to as “parking aid” in short, is a system which utilizes visual image coming from
> two strategically located low resolution cameras to generate instant advice for the driver toward
> successful parallel parking maneuver. Human machine interface (HMI) is provided through an
> LCD screen located over the dashboard which provides instructions in graphical form about
> what the driver should do for an acceptable parking. The system is based on fuzzy logic and
> information about the lateral and longitudinal positions of the vehicle acquired through
> processing the visual image provided by the cameras.

#### 摘录 B
- 出处：第 4-5 页，`2. Parallel Parking Problem / 3. Overview of the System`，行 208-220
> In our approach two cameras are placed, one at the front and one at the back to get both views
> simultaneously and feed the distance information to a fuzzy logic system to mimic decisions of
> an expert driver. Low resolution cameras are selected deliberately to reduce the computational
> complexity of image processing algorithms. Since the system is intended as a driver aid, a suitable
> human-machine interface (HMI) system is designed to relay generated advice to the driver.
> The system is designed to operate by relying on visual information received from two cameras
> located on the vehicle. The cameras need to have wide angle of vision, and should be oriented in
> a specific manner in order to extract critical information necessary for generating appropriate
> advice for the driver.

#### 摘录 C
- 出处：第 6-7 页，`3.2. Image Processing`，行 294-318
> The fuzzy parking aid system automatically
> starts capturing images once it is activated by
> the user. Figure 6 shows the simple block di-
> agram of the system design. The video stream
> of images coming from the cameras is fed to
> an image processing unit, which processes the
> image to calculate the distance parameters and
> passes them on to the fuzzy logic unit which
> makes appropriate decisions and presents the
> output as guidance advice to the driver for par-
> allel parking.
> The captured image is processed to acquire dis-
> tances from front and back vehicles as well
> as lateral distances from the curb.
> Images re-
> ceived from the two USB cameras are treated
> as two independent streams of images for real
> time processing. The images in both streams
> first go through two dimensional median filter-
> ing

#### 摘录 D
- 出处：第 7 页，`3.2. Image Processing`，行 320-338
> The second step
> in processing is applying edge detection proce-
> dure to detect edges of the objects in the scene.
> Edge detection step of the process is done by
> using Sobel filter.
> The edge detection process converts the image
> to a binary image with 0’s and 1’s.
> Next step in the image processing
> is measuring the pixel distance of the objects
> in the scene by counting pixels in the specific
> predetermined directions.
> Rear camera images
> are used for getting two distance parameters
> as shown in Figure 7. The straight up vector
> (R), measures the distance of the object or the
> available space behind the vehicle, D
> r,a n dt h e
> 45 degree angled vector (C)measures the dis-
> tance from the curb, Dlf.

#### 摘录 E
- 出处：第 11-12 页，`3.5. HMI of the System / 4. Testing Robustness of the System`，行 557-563, 611-616
> The screen layout has four
> quadrants for forward, backward movement and
> left and right steering. The suggested steer-
> ing position and the movement, including the
> speed of movement, are shown on the screen
> as shown in Figure 12.
> The real time operation speed of
> the system is found to be quite satisfactory with
> 0.4-second update speed. The system evaluated
> current condition of vehicle and distances be-
> tween obstacles continuously and provided new
> instructions to the driver every 0.4 seconds.

### 2. 基于原文整理后的自然语言描述

Once the user activates the parking aid, the system starts capturing image streams from two strategically located low-resolution wide-angle cameras mounted at the front and rear of the vehicle. The two image streams are processed independently in real time: the images are smoothed by two-dimensional median filtering, converted through Sobel edge detection, and then used to count the front, rear, and curb distance parameters needed for parking guidance. These measured distances are passed to a fuzzy-logic decision unit that mimics an expert driver and generates instant parking advice. The resulting guidance is shown on an LCD HMI with quadrants for forward/backward motion and left/right steering, including movement speed, and the system refreshes the driver instructions about every 0.4 seconds.

### 3. 逐句溯源

1. 句子 1：Once the user activates the parking aid, the system starts capturing image streams from two strategically located low-resolution wide-angle cameras mounted at the front and rear of the vehicle.
   对应摘录：A, B, C
2. 句子 2：The two image streams are processed independently in real time: the images are smoothed by two-dimensional median filtering, converted through Sobel edge detection, and then used to count the front, rear, and curb distance parameters needed for parking guidance.
   对应摘录：C, D
3. 句子 3：These measured distances are passed to a fuzzy-logic decision unit that mimics an expert driver and generates instant parking advice.
   对应摘录：A, B, C
4. 句子 4：The resulting guidance is shown on an LCD HMI with quadrants for forward/backward motion and left/right steering, including movement speed, and the system refreshes the driver instructions about every 0.4 seconds.
   对应摘录：A, E

## 条目 2: Two-stage parking maneuver with trigger handoff
- 控制对象：并联泊车辅助系统中的 Stage 1 / Stage 2 分阶段控制逻辑
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车载驾驶辅助领域的分阶段泊车控制器，用于先将车辆倒入中间位置，再触发第二阶段完成姿态修正和最终入位。
- 判断：算。对象是实际泊车辅助系统的阶段切换逻辑，原文明确给出了两阶段的目标位置、切换条件和 HMI 指令接管关系。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7-8 页，`3.3. Fuzzy Inference Systems`，行 363-393
> Fuzzy logic block of the system makes decisions based on the rear, front and curb parameters generated by the image processing block.
> Using approach adapted by most expert drivers, the parking maneuver is done in two distinct
> steps. Expert drivers usually drive the car backwards into the parking bay and then drive the
> vehicle forward to correct the orientation of the vehicle. We have designed the fuzzy logic inference system to mimic this behavior.
> Since expert driver approach is to do the parking in two distinct steps, we have used two different
> fuzzy logic systems to capture actions done in these two steps. First, fuzzy logic system guides
> the driver from the initial position to a halfway position where the rear end of the vehicle is
> placed in the parking space, while the front end of the vehicle is still partially outside the parking bay.
> This part of the process is called Stage 1 operation where the beginning and ending positions
> are shown in Figure 8 as positions A and B.
> The ending position in Stage 1 is not an acceptable orientation for parking, so Stage 2 makes
> the final corrections to put the vehicle completely in the parking position. Position B is
> the beginning position for Stage 2 and position C is the ending position.

#### 摘录 B
- 出处：第 9 页，`3.3. Fuzzy Inference Systems`，行 413-430
> There are three output variables designed for
> the Stage 1 fuzzy inference system, labeled as “movingDirection”, “steeringGuide” and “trigger”.
> “movingDirection” and “steeringGuide” are the two parameters displayed by the Human
> Machine Interface LCD screen of the system to the vehicle driver and can be considered as the
> outputs of the Stage 1 system. The other output
> parameter of Stage 1, which is called “trigger”
> is not displayed to the driver, but it is used for initiating the start of the Stage 2 fuzzy inference
> system.
> Stage 2 fuzzy inference system is initiated by
> the trigger output of the Stage 1 and it is a
> completely independent inference system. The
> variables of this inference system are similar
> to Stage 1 inference system but fuzzy rules are
> completely different from the rules of Stage 1.
> Once the Stage 2 inference system is triggered,
> the driver instructions are generated and HMI
> screen is controlled by this stage.

#### 摘录 C
- 出处：第 9 页，`3.3. Fuzzy Inference Systems`，行 431-447
> The fuzzy rules for the Stage 1 are as follows:
> •If(Curb isfar)then (MovingDirection is
> Reverse )(1)
> •If(Curb isfar)and(RearCar is not close )
> then (SteeringGuide isTurnRight )(Mov-
> ingDirection isReverse )(0.9)
> •If(Curb isMiddleOUT )and (RearCar is
> notclose )then (SteeringGuide isTurnRight )
> (MovingDirection isReverse )(0.9)
> •If(Curb isMiddleIN )and(RearCar is not
> close )then (SteeringGuide isTurnleft )(Mov-
> ingDirection isReverse )(0.9)

#### 摘录 D
- 出处：第 9-10 页，`Stage 2 Fuzzy Inference System`，行 449-457
> Stage 2 uses the same fuzzy variables “ curb”,
> “rearCar ”, and “ frontCar ”.
> Fuzzy rules for Stage 2 are as follows:
> •If(FrontCar is not close )and(Curb isclose )
> then (SteeringGuide isTurnRight )(Mov-
> ingDirection isForward )(1
> )
> •If(FrontCar isclose )and(RearCar is not
> close )then (SteeringGuide isTurnleft )(Mov-
> ingDirection isReverse )(1)

### 2. 基于原文整理后的自然语言描述

The parking maneuver is executed in two distinct stages. In Stage 1, the fuzzy controller drives the vehicle from the initial position A to the intermediate position B where the rear end is already inside the parking space while the front end is still partially outside, and it outputs `movingDirection`, `steeringGuide`, and an internal `trigger` signal. During this stage, the HMI-displayed guidance is produced from the linguistic inputs `frontCar`, `rearCar`, and `curb`, with rules such as reversing while turning right when the curb is far or middle-out and the rear car is not close, and reversing while turning left when the curb becomes middle-in. The internal `trigger` output starts a completely independent Stage 2 inference system at position B, and Stage 2 then takes over the HMI. In Stage 2, the controller uses the same input variables but different rules to generate the final forward/reverse and steering corrections that bring the vehicle to the final parking position C.

### 3. 逐句溯源

1. 句子 1：The parking maneuver is executed in two distinct stages.
   对应摘录：A
2. 句子 2：In Stage 1, the fuzzy controller drives the vehicle from the initial position A to the intermediate position B where the rear end is already inside the parking space while the front end is still partially outside, and it outputs `movingDirection`, `steeringGuide`, and an internal `trigger` signal.
   对应摘录：A, B
3. 句子 3：During this stage, the HMI-displayed guidance is produced from the linguistic inputs `frontCar`, `rearCar`, and `curb`, with rules such as reversing while turning right when the curb is far or middle-out and the rear car is not close, and reversing while turning left when the curb becomes middle-in.
   对应摘录：B, C
4. 句子 4：The internal `trigger` output starts a completely independent Stage 2 inference system at position B, and Stage 2 then takes over the HMI.
   对应摘录：A, B
5. 句子 5：In Stage 2, the controller uses the same input variables but different rules to generate the final forward/reverse and steering corrections that bring the vehicle to the final parking position C.
   对应摘录：A, D
