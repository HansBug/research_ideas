# Guided Synthesis of Control Programs Using Uppaal

- 问题一句话：若 plant model 细到足以合成控制程序，直接用 `UPPAAL` 自动找调度会很快爆炸。
- 方法一句话：在原 timed automata 网络上加入只约束搜索而不改原语义的 guiding variables、额外 guards 和启发式策略。
- 解决点一句话：把可执行控制程序合成从只能处理极小模型推进到可处理几十批次的 plant scheduling。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `⚡ 改进/扩展` 条目，但它同时也是 `UPPAAL` 很早的一篇“**验证驱动合成**”代表作。它和 [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/) 一样，都在尝试把 `UPPAAL` 从“证明模型对错”推进到“从模型中导出更有用的构造性结果”。

区别在于：

1. `behrmann01` 更偏 cost-optimal search；
2. 这篇更偏 scheduling / control-program synthesis。

它的独特价值在于，它不是停留在“从模型得到一条 trace”，而是把这条 trace **投影成 schedule，再翻译成可执行控制程序，并在物理 LEGO plant 上跑起来**。这使它在 `UPPAAL` 技术线中非常像一个早期“model-to-program”实验。

## 立足问题

这篇论文面对的问题非常硬：如果你想从 batch plant 模型里真正合成控制程序，那么模型就必须足够细，细到能区分设备动作、移动时间、资源互斥、批次配方和物理限制。可一旦模型细到这个程度，直接让 `UPPAAL` 在完整状态空间里自动找调度，规模就立刻失控。

作者在引言里把张力说得很清楚：

1. **模型必须够细**
   - 否则从 trace 投影出来的 schedule 不够具体，无法直接转程序。
2. **模型一旦够细就会太大**
   - 自动搜索很快变得 infeasible。

因此，这篇论文真正立足的不是一般意义上的“合成控制程序”，而是一个更具体的问题：

> 当 plant model 已经细到足以导出可执行程序时，怎样仍然让 `UPPAAL` 找到可行 schedule？

这引出三个核心需求：

1. 不能改坏原模型语义，否则得到的 schedule 可能对原 plant 不合法。
2. 必须显著缩小搜索空间，否则只能处理 1-2 个 batch。
3. 最终结果必须能映射回真实控制命令，而不是停在抽象 trace。

这正是论文提出“guiding”技术的背景。

## 核心方法

这篇论文的方法主线很完整：**先建一个足够准确的 plant timed-automata model，再在其上叠加只影响搜索的 guide，最后把 trace 投影成 schedule 和 program。**

### 1. 先把 plant 建模到足以支持 code synthesis 的精度

论文首先并不是直接谈 guiding，而是强调 plant model 必须达到一种“可投影成程序”的精度。其模型由多个 timed automata 并行组成，对应：

1. batches
2. recipes
3. machines
4. cranes
5. tracks
6. casting machine

系统中的关键约束包括：

1. batch 在 plant 中停留总时长上界；
2. machines / tracks / cranes 的互斥占用；
3. cranes 不可相互穿越；
4. 连续浇铸必须连续，不可断流；
5. 不同 steel qualities 由不同 recipe 与 machine path 决定。

这里的一个关键点是：作者主动把模型做得比纯验证模型更细，因为目标不是只证明“可能存在一个 schedule”，而是要让输出 trace 能被直接翻译为控制程序。这等于把建模目标从 verification-only 改成了 synthesis-ready。

### 2. 把调度问题翻译成 time-bounded reachability

在这种模型上，调度问题被写成 time-bounded reachability。也就是说，`UPPAAL` 做的仍然是它最擅长的事情：

1. 检查某个 goal configuration 是否可达；
2. 若可达，返回一条 timed trace。

接下来，作者把这条 trace 投影成与 plant 有关的动作序列，再做文本替换式程序生成。这个工作流大致是：

$$
\text{plant model} \to \text{timed trace} \to \text{schedule} \to \text{control program}
$$

这里最重要的不是投影本身，而是论文明确指出：**只有模型足够准确时，这个链条才成立。**

### 3. 引入 guiding variables，但严格禁止修改原模型变量

这篇论文的核心创新，就是 guiding。作者先给出一个很干净的定义：

1. 原网络有 clocks 集合 $C$ 与 data variables 集合 $D$。
2. 新引入 guiding clocks $C_G$ 与 guiding integer variables $D_G$。
3. guides 通过三种方式起作用：
   - 给原 guards 额外合取新约束；
   - 给 location invariants 额外加约束；
   - 在 resets / assignments 中更新 guiding variables。

关键约束是：

1. guides 可以读取原有 clocks 和 data；
2. 但**不能写原有 clocks 和 data**；
3. 只能写自己新引入的 guiding variables。

这一步至关重要，因为它保证：

1. guided model 生成的每条 trace 仍是 original model 的合法 trace；
2. guide 只是在裁剪搜索空间，而不是改变 plant 物理行为。

论文明确指出，这样可保住一个核心性质：若 guided model 找到 schedule，则该 schedule 对 original plant model 也合法。

### 4. 把启发式策略编码成显式 guide

论文的真正方法亮点，是没有停在“可以加 guides”这一抽象层，而是展示了多类具体策略如何编码进 automata。

#### 4.1 批次顺序策略

作者引入 `nextbatch` 这样的 guiding variable，控制哪个 recipe automaton 允许先启动。其思想非常直接：

1. 已知生产顺序时，就不必在所有批次启动顺序之间盲搜。
2. 用 `nextbatch == number - 1` 之类的 guard 限制下一批何时可放行。

这一步减少的是**组合启动顺序**带来的爆炸。

#### 4.2 批次启动时机策略

不是所有 batch 都同时启动，而是要根据前一批在 plant 中的推进情况延迟后继 batch 的放行。作者通过延后 `nextbatch` 的更新位置，避免多批次过早涌入 plant。

这一步减少的是**拥塞型状态空间**。

#### 4.3 全局 routing 策略

作者为每个 batch 引入 `next` 变量，记录它下一步应去哪个 machine / track。例如在有多条可选路线时，根据当前各轨道 batch 数选择较空的一条。

这一步不是纯局部贪心，而是把 recipe-level knowledge 编码进模型搜索。

#### 4.4 局部 routing 策略

当 batch 已知目标位置时，作者进一步限制它在 plant 内部的移动路径只走“合理直达路线”，而不是在所有物理可行路径上乱跑。

这一步减少的是**中间搬运路径的分支数**。

#### 4.5 crane movement 策略

crane 空载时不再任意移动，而只在以下场景动作：

1. 有 batch 等待被拾取；
2. 它阻碍了另一台 crane。

这通过 `req1 / req2` 等 guiding variables 协调，实现了对空载 crane 行为的强约束。

整体来看，论文做的不是某个抽象“guided search algorithm”，而是把**领域策略编码进 timed automata 本身，但又保持语义保守性**。

### 5. 把 trace 投影成 schedule，再翻译成 central controller program

找到 guided trace 之后，论文并没有停在“证明这条 trace 存在”，而是继续往下做：

1. 从 trace 中投影出与 plant 相关的同步动作和 delays；
2. 生成 schedule；
3. 把 schedule 翻译为发给局部控制单元的命令序列；
4. 用 `gawk` 做模式扫描和文本转换。

在生成的程序里：

1. `Delay(t)` 转换成等待指令；
2. `Load1.Track2Right` 这类动作变成向某个本地单元发送命令；
3. 每行 schedule 对应 central controller program 的一段代码。

这意味着 `UPPAAL` 在这里实际上扮演了“控制程序综合器”的前端搜索引擎角色。

### 6. 用物理 LEGO plant 做闭环验证

最后，作者把生成程序运行到 LEGO MINDSTORMS plant 上，这一步非常关键。它不是花哨 demo，而是验证整个方法链条是否真正闭合：

1. 模型是否足够准确；
2. 投影是否正确；
3. 翻译是否正确；
4. timing information 是否与真实 plant 相符。

实验中作者确实发现了建模错误，例如：

1. crane 提前水平移动；
2. 两台 crane 相邻同向移动导致碰撞；
3. 单 batch 场景下 casting machine 行为不正确。

然后他们修正模型，重新生成程序并再次运行。这个过程非常接近今天所说的 model-based closed loop development。

## 解决了什么问题

这篇论文真正解决的，是 `UPPAAL` 在“合成”方向上的一个实际瓶颈。

### 1. 它让 synthesis-ready 细粒度模型不再立刻失效

没有 guiding 时，论文报告说直接分析基本上只能处理两批次；加入 guides 后，普通机器上就能上到几十批次，内存更多时甚至到 `60` 批次。

### 2. 它提出了一种语义保守的用户引导搜索机制

很多启发式搜索都很强，但难以保证结果对原模型仍合法。这里通过“不改原变量，只加 guiding variables”的约束，把保守性讲清楚了。

### 3. 它打通了 `model -> trace -> schedule -> program -> plant` 的完整链路

这一步使 `UPPAAL` 不再只是 verifier，而成为 control synthesis workflow 的核心搜索引擎。

### 4. 它也诚实保留了边界

论文没有宣称 guides 自动生成，也没有保证 guide preserving schedulability。作者明确承认：

1. guides 需要用户用领域知识设计；
2. 某些 guide 可能会删掉一些原本合法的 schedule；
3. 他们追求的不是最优 schedule，而是可生成、可执行的有效 schedule。

这种边界界定非常清楚。

## 与 UPPAAL 技术线的关系

这篇论文是 `UPPAAL` 在 synthesis / scheduling 方向的一条早期主干。

### 它接在谁之后

它直接接在：

1. [lpy97-uppaal-nutshell](../lpy97-uppaal-nutshell/)
   - 先把工具工作流讲清楚。
2. [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/)
   - 共同说明 `UPPAAL` 已经从纯验证向搜索/优化扩展。

### 它往后影响了谁

它往后影响了：

1. 早期 schedule synthesis / planning with `UPPAAL` 相关工作；
2. `ExUppaal` 这类把 timed automata 往 executable system 方向推进的路线；
3. 更广义上，所有“用反例/trace 直接生成操作方案”的 `UPPAAL` 工作流。

### 它更靠近哪条主线

它最靠近的是：

1. `scheduling / planning`
2. `guided exploration`
3. `trace-to-program synthesis`

而不是后面的 `SMC / Tiga / ECDAR` 这些支线。

## 实现与材料

1. **内容详细程度**
   - 当前总账给它记为 `🟩 较完整`，我认同。
   - 原因是论文不仅讲 guiding 概念，还给出 guide 的注入规则、多个具体策略、实验表格以及从 trace 到程序的后处理流程。
2. **实现可获取程度**
   - 当前总账记为 `🟧 仅可执行/可使用版本可得`，应维持。
   - 论文虽然给出官方 PDF，且明确依赖 `UPPAAL`，但对应的 guided synthesis plant model、转换脚本和控制程序生成工具没有形成公开、稳定的源码线。
3. **材料质量**
   - `paper_content.txt` 足够支撑方法机制的重建。
   - 若后续要复做 LEGO plant translation，仍需回 PDF 附录 automata 与图示核对细节。

## 对本研究的启发

这篇论文对当前博士研究的启发非常强，因为它几乎就是“生成-验证-落地-修正”闭环的早期形式化版本。

至少有五点值得直接吸收：

1. 若模型要服务后续自动生成，就必须在建模阶段保证信息粒度足够细。
2. 搜索空间太大时，可以引入“只约束搜索、不改原语义”的辅助变量层。
3. 领域知识不一定只能写在说明文档里，也可以形式化进 guide variables 和 guards。
4. 从 trace 到可执行程序的投影过程应尽量自动化，否则闭环会断。
5. 真正的模型验证，不该只停在模型内部，最好还能接到外部执行或更真实的系统反馈。
