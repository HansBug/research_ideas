# 倾转旋翼 LQG 状态切换控制 / A Novel Approach to Automated Tracking Control of Hybrid Tilting Rotor UAVs Using LQG Controller and State Machine

## 论文在讲什么

这篇论文讨论的是 hybrid tilting-rotor UAV 在 hover、transition 和 fixed-wing 三种工况间如何自动切换控制器。作者的方法不是直接做在线优化，而是先对若干 trim point 线性化，针对每个工作点设计一组 LQG controller，再用状态机决定当前该启用哪组 observer 和 gain。这样既保住了过渡阶段的非线性适应能力，又避免了 MPC 一类方法在机载算力上的负担。

文中关注的是纵向动力学控制。论文把状态机放在控制架构中间：它读取当前飞行状态，切换 Kalman Filter 参数与 LQ gain，并在 hover 起飞、旋翼倾转和 fixed-wing 飞行之间安排不同的参考值与控制回路配置。尤其在 transition 阶段，作者把 `90° -> 0°` 的倾转、`Kouter` 的关断/重启、rear rotor 的停用，以及 `K1-K9` 的增益切换都写得比较明确。

## 控制系统在文中的位置

这套状态机监督器是论文的核心。虽然文中有不少 LQG 与 Kalman Filter 的数学推导，但这些推导最终都服务于一个实际问题：对于当前这架 tilt-rotor UAV，什么时候该用哪组线性控制器、何时该关外环、何时该重启、何时认为已经进入 fixed-wing 模式。换句话说，状态机并不是一个可有可无的外壳，而是整个 controller switching strategy 的执行中枢。

这也解释了为什么它适合进入 `sources/`。很多 tilt-rotor 或 transition control 论文会把离散逻辑藏在 gain scheduling 说明里，真正的状态集合并不清楚；这篇论文则直接用 `state machine` 来描述 switching logic，并把关键操作条件和参考信号写出来。因此它提供的是一条可追溯的监督控制链，而不仅是“某个控制律在仿真中有效”的结果陈述。

## 对我们为什么有用

这篇论文对样本库的主要价值，是补进一类典型的 `EFSM + T1 + 连续耦合` 飞行控制样本。它的状态机不是只做 mission-level 模式切换，而是直接耦合到实际纵向动力学控制：当前倾转角是多少、当前 `u/w` 属于哪个工作区、外环是否要禁用、观测器和全状态反馈矩阵该怎么切换，这些都属于离散监督层的职责。

同时，它也保住了足够多的工程量级细节，比如 vertical takeoff 时 `0 -> -2 -> -4 -> -2 -> 0` 的垂向参考、transition 的 `32 s` 稳定过渡、`K4` 进入过渡、`K9` 对应固定翼稳态。这些信息很适合后续抽成“状态机 + 连续控制接口”的自然语言数据，而不是被迫只留下 `hover / transition / fixed-wing` 三个过于抽象的状态名。

## 如果需要人工细读，建议怎么读

如果后续需要人工细读，建议先看第 1-3 页的引言和控制框架部分，只确认为什么作者要在若干 trim point 间切换 LQG controller；然后直接跳到第 10-12 页，把 `State Machine`、simulation mission profile 和 gain-switching result 连起来读，优先抓住状态机在 hover、transition 和 fixed-wing 三段里分别改了什么控制变量。

后面的 LQ / Kalman 推导可以放到第二轮再看。第一次重读的目标，是先把状态机的职责、进入条件、参考序列、`Kouter` 和 rear rotor 的开关逻辑读稳；一旦这条离散主链稳定了，再去补连续模型和性能结果会更高效。
