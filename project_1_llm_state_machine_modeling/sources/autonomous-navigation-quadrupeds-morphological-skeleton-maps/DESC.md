# 四足机器人 POI 巡航与扫描监督控制 / Autonomous navigation of quadrupeds using coverage path planning with morphological skeleton maps

## 论文在讲什么

这篇论文围绕 Unitree Go2 Edu 四足机器人在非结构化环境中的 coverage exploration 展开。作者先用已有 2D map 的 morphological skeleton 生成一串 POI / waypoint，再用 path planner 把它们排成时间更优的访问顺序，最后让四足机器人按顺序去每个点位执行扫描任务。

如果只看我们关心的控制对象，这篇最有价值的不是 skeletonization 算法本身，而是那条把 `map reader -> path planner -> Nav2 -> scan -> manual fallback -> home` 串起来的高层 FSM。它把四足机器人从“读图建点、选点、走点、扫点、超时、人工接管、回家”写成了一条很完整的任务监督链。

## 控制系统在文中的位置

状态机在文中承担的是高层 autonomy glue 的角色。作者明确说 map reader 和 path planner 只负责生成 waypoint 与 route，而真正使机器人“按序导航并完成扫描”的是 Section `3.3` 里的 FSM，所以这条状态链是把规划模块和执行模块接成完整机器人系统的核心。

这也让它和很多 quadruped 论文区分开来。很多四足机器人论文更偏 locomotion policy、避障控制或连续运动控制，而这篇直接公开了 `Load Map / CheckWaypoints / Check Destination / Move / Scan / ManualControl / Home` 这组状态，因此非常适合作为任务级离散控制样本。

## 对我们为什么有用

这篇样本的价值在于它提供了一条很清楚的 flat supervisor。它没有复杂层次结构，但状态职责、切换条件、失败处理和人工接管都明确，而且还有 `δ` 容差和 `Ttimeout` 这样的局部工程时间语义，正好符合 `FSM + T1` 的扩样目标。

同时，它补的是“POI 覆盖巡检 + 扫描 + 人工回退”这一类机器人任务。和库里已有的温室机器人、场地机器人或施工机器人相比，这篇更强调 coverage path planning 驱动的 waypoint visitation，因此在训练集里能形成比较清晰的表达差异。

## 如果需要人工细读，建议怎么读

如果后续要人工重做 `STM.md`，建议先读摘要，把 POI、FSM、reachability 和 overall task 先抓住；然后直接跳到 Section `3.3 State machine` 和 Figure `4`，把每个状态的职责、`δ` 判定、`Ttimeout`、joystick 中断和 `Home` 逻辑都抄清；最后再看 Table `2` 与 `Figure 9`，核对 waypoint reachability、超时和人工介入在实验中的具体表现。

像 map reader、path planner、graph 构造和复杂度分析这些章节，可以留到第二轮再看。第一次人工复核时，只要把 waypoint 变量怎样进入状态机、何时 scan、何时 timeout、何时 manual takeover、何时回 home 读稳，就足够支撑样本重建。
