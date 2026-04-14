# 基于有限状态机的微型飞行器自适应任务控制 / A Finite State Machine Based Adaptive Mission Control of Mini Aerial Vehicle

## 论文在讲什么

这篇论文讨论的是微型飞行器在高压输电线路绝缘子巡检任务中的自适应任务控制。作者关心的不是底层飞控本体，而是高层 mission control 如何把起飞、搜目标、变位、悬停、巡检、着陆与应急处置组织成一套可扩展的有限状态机。

论文先用巡检任务场景解释为什么需要自适应任务控制，再把任务步骤映射成状态，并给出高度、距离和安全边界参数表。随后作者把这套任务流程形式化为一个带层次结构和真值表的 mission control FSM，因此控制逻辑并不是点到为止，而是全文主角。

## 控制系统在文中的位置

我们关心的控制系统就是文中所谓的 `Adaptive Mission Control`。第 2 节通过任务步骤和状态定义给出系统语义，第 3 节进一步明确说明 mission control FSM 是一个 hierarchical state machine，并且列出输入事件与表 5 的 current-state / next-state 关系。

这使得论文里的状态机不是抽象概念，而是巡检任务的实际控制骨架。`Flight`、`Inspection` 是父状态，`Take Off`、`Hold Position`、`Change Position`、`Search Object`、`Land`、`Emergency` 则承担具体执行阶段，这种写法对 `sources/` 非常友好。

## 对我们为什么有用

对 `✈️` 方向来说，这篇论文补的是一个非常适合做数据集样本的任务型无人机控制器。相比只讲搜索救援、跟踪或飞行模式切换的文章，它把“视觉巡检任务如何一步步推进”写得更像工程任务脚本，同时又保留了层次状态机结构和显式事件输入。

它特别有价值的一点，是把时间和位置都拉进了控制条件里。`Hold Position` 带预定义时间，`Change Position` 受高度和距离参数控制，`Search Object` 受检测结果控制，`Emergency` 则统一处理危险情况。后续如果要训练模型识别“任务监督层 HSM”，这篇论文很适合作为代表样本。

## 如果需要人工细读，建议怎么读

人工细读时，建议先看第 3-5 页，也就是状态列表、各状态说明、图 2 和表 5 所在部分。先把 `Initial / Flight / Take Off / Inspection / Hold Position / Change Position / Search Object / Land / Emergency` 这些状态和 `I1-I6` 输入对应起来，再去看高度/距离参数表如何约束任务推进。

如果后续需要补更细的上下文，再回头读前两页关于 autonomy taxonomy 的部分。那部分有助于理解作者为何把 mission control 放在决策层，但对 `STM.md` 首轮提取来说，优先级仍然低于状态定义、层次结构和真值表本身。
