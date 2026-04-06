# 眼手协同装配状态机 / Human-Robot Collaborative Assembly Based on Eye-Hand and a Finite State Machine in a Virtual Environment

## 论文在讲什么

这篇论文研究的是一个虚拟环境中的 human-robot collaborative assembly system，目标是用 eye-tracking、gesture recognition 和 robot path planning 组合出一种更高效的人机协作装配方式。作者把机器人和场景搭在 Unity 中，用 Simulink 控制六自由度机械臂，再用 PRM 处理自动抓取和搬运阶段的轨迹规划，同时用手势和视线去表达用户意图。整体上它带有明显的方法论文色彩，因为作者既在讲交互模式，也在做实验对比。

不过，对 `sources/` 来说，论文最有价值的地方在于作者没有把这种交互停留在“识别若干手势”的层面，而是明确用 FSM 去切换 `instruction` 与 `mapping` 两种模式，并把协作过程分成 `Recognize`、`Indication`、`Capture`、`Mapping` 几个阶段。也就是说，虽然实验是在 virtual environment 中完成，但被抽出来的控制对象本身仍然是清晰的协作装配 supervisor，而不是单纯 UI 流程。

## 控制系统在文中的位置

这里的控制系统描述不是论文的唯一主角，但确实是方法落地的核心载体。前文会讨论手势分类、眼手指示点和 PRM 的路径规划细节，可真正把“用户给什么提示、机器人何时自动抓取、何时切到人工映射装配”组织起来的，是 FSM 所管理的 interaction mode。换句话说，FSM 不是点缀性的实现模块，而是把整套眼手交互、自动执行和人工精调连起来的中枢。

这篇论文需要如实看待它的边界：它不是现实工厂里的实物装配控制器，而是一个经过 VR 实验验证的人机协作装配方法载体。但即便如此，文中关于 `G1 + E1` 指定对象和目标位置、`G2` 切到 mapping、`G3` 结束 mapping、`G4` 放松 gripper，以及 `Recognize / Indication / Capture / Mapping` 这组状态链，已经足够形成稳定可追溯的状态机样本。

## 对我们为什么有用

这篇论文补的是 `🏭` 方向里一种不太像传统 PLC 顺序控制的 `HSM` 样本。它把粗粒度的自动抓取搬运和细粒度的人工装配校正分层组织起来，既有模式切换，也有阶段推进和手势触发，因此能提供一种不同于输送带、洗衣机、灌装线的工业协作控制表达。对于后续做 `NL -> state machine` 数据集，这种“上层模式 + 下层阶段”的协作装配 supervisor 很有代表性。

它也适合作为一种筛选提醒。很多 HRC 论文会偏用户体验、识别准确率或交互装置，而没有真正可抽的控制对象；这篇能留下来，是因为它明确写出了模式、阶段和触发关系。后续如果继续找 HRC 或 assembly 方向样本，最好优先筛这种“FSM 真正控制 robot mode”的论文，而不是只有感知或实验统计的稿件。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `2-3` 页的 system layout 和 highlights，确认 `instruction / mapping` 两种模式与 PRM 的分工。然后直接跳到第 `9` 页的 `2.4 Finite State Machine for Human-Robot Collaboration`，把 `G1-G4` 分别触发什么、何时从 indication 进入 mapping、何时结束 mapping 先抽出来。接着再看第 `13-14` 页的 `Experimental State Change`，用 `Recognize / Indication / Capture / Mapping` 的阶段说明去核对这套 supervisor 在实验里是怎样实际运行的。

手势识别网络、眼手指示点抖动分析和 PRM 算法细节可以第二轮再看。它们说明为什么系统能工作，但对重建 `STM.md` 里的离散控制链不是第一优先级。第一次阅读只要先把模式层和阶段层读稳，就能比较稳定地把这一类 HRC state supervisor 重新抽出来。
