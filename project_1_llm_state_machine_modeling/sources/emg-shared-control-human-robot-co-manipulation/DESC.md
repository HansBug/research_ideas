# EMG 共享控制的人机共操作框架 / EMG-Based Shared Control Framework for Human-Robot Co-Manipulation Tasks

## 论文在讲什么

这篇论文研究的是一个面向 human-robot co-manipulation 的 shared control architecture。作者用表面肌电信号识别操作者的 `free` 与 `contraction` 两类动作意图，再把分类结果送入有限状态机，自动切换机器人 admittance controller 的参数组。整体目标很明确：既要让操作者在自由空间里轻松拖动机械臂，又要在接近工件表面时保持更高精度和更强阻尼。

这篇文章的好处在于它没有把贡献只停在“EMG 分类很准”或者“admittance 控制可调”。它明确说系统有 `Low-Damping` 和 `High-Damping` 两个 operational mode，并把模式切换条件、持续时间和实验任务都串成一条完整的监督控制链，因此可以直接进入我们关注的状态机样本口径。

## 控制系统在文中的位置

我们关心的控制系统描述是论文的高层控制核心。Low-level layer 负责 inverse kinematics、joint controller 和 variable admittance controller，但真正决定当前该用哪组增益、何时切模式的，是 Section `4.2` 中的 finite state machine。也就是说，EMG classifier 提供的是离散事件信号，FSM 才是把这些信号变成 operational mode 切换的主控部件。

这也让它和很多只讲 EMG 识别或只讲 admittance tuning 的论文区分开。这里不是“识别到肌电后做一点参数调整”那么松散，而是有明确初始状态、进入 `High-Damping` 的 `1.5 s` guard、回到 `Low-Damping` 的 `3 s` guard，以及模式切换后机械臂在路径跟踪和快速回位上的不同控制目标。

## 对我们为什么有用

它对 `sources/` 的价值在于补到了一类非常典型、但并不冗余的人机共操作 mode-switch supervisor 样本。状态数只有两个，但原文交代得很完整：输入类别、模式语义、守卫时长、实验路径、重复切换过程都能直接回溯。这种“状态数少但 guard 和动作语义很强”的样本，对训练模型理解简洁 FSM 很有用。

它也帮我们补到 `FSM + T1` 这类清晰工程定时样本。这里的时间不是严格硬实时，但 `1.5 s / 3 s` 已经是明确的工程 guard。相比一些只写“operator can switch mode”的论文，这篇能直接告诉我们：什么信号维持多久，系统会进入哪个状态，以及进入后控制特性如何变化。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看摘要和 Section `2`，把两种 operational mode 的含义先锁定住，再直接跳到 Section `4.2 Finite State Machine` 读 `1.5 s` 与 `3 s` 两个切换 guard。这样先把状态骨架、输入类别和模式动作建立起来，再回头看 low-level admittance controller 的数学细节，会更容易分清哪些内容属于状态机主链，哪些只是底层实现。

之后再看实验结果部分，尤其是 Figure `5-6` 附近关于 green/blue path、重复 tracing square-wave filament 和时间轴上 mode switching 的描述，用来核对状态转换在真实任务中的时序。至于 SVM 训练、特征提取和分类器指标表，第一次为了重做 `STM.md` 可以后看，因为它们更多是解释输入事件如何被检测，不是主状态机抽取的第一优先级。
