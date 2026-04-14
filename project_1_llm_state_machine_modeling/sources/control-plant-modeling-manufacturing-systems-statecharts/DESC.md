# 制造单元 Statecharts 建模与控制 / Control and Plant Modeling for Manufacturing Systems using Statecharts

## 论文在讲什么

这篇论文讨论的是如何用 `UML/Statecharts` 来建模制造系统的 plant 与 control，并给出一套从场景到控制模型再到 PLC 实现的路线。它本身带有明显的方法论色彩，但并没有停留在“Statecharts 很好用”这类抽象层面，而是用一个 tagged machine 的完整制造单元案例把方法压到真实控制链上。

对样本库最重要的是，作者把这个 tagged machine 写得足够具体：有哪些组件、初始条件是什么、什么时候开始运行、工作件如何被送入模具、按压多久、最后怎么被推出去。这使得这篇论文虽然是方法论文，但其中的制造控制案例本身足够强，完全可以单独作为状态机样本入库。

## 控制系统在文中的位置

控制系统在文中既是方法的承载对象，也是论文最可复用的案例主体。作者的确花了不少篇幅解释 Statecharts 的优点、plant/control modeling methodology 和 validation route，但一到案例部分，正文就立即落到 piece-loader、cylinder、valve、sensor、timer 这些控制部件，以及它们在具体事件下如何切换。

更关键的是，这个案例不是只有一段自然语言叙述，而是同时给出 running scenario、`psOn / s1On / s2On / s3On / fsOn` 事件链、guard 条件、`timerT1` 和 `tm(2s)`。因此我们在这里看到的不是松散的生产线介绍，而是一条相当完整的“组件边界 + 条件触发 + 定时动作 + 结束复位”控制链。

## 对我们为什么有用

这篇论文对 `sources/` 的价值在于补了一个很标准的制造单元顺序控制案例，而且还附带了 Statecharts 语境下的层次、并行和 timer 语义。和常见只给 ladder 截图的 PLC 小论文相比，这里既能看到对象层面的实际工艺步骤，也能看到形式化建模后的 guard/action 表达方式，对后续做结构化状态机建模特别有帮助。

另外，这篇论文还能补一个很重要的表述模式：控制语义并不一定只靠“状态名列表”来给出，也可以通过“场景文本 + event/guard/action chain + timer component”来恢复完整状态机。这对后续从非形式化需求提炼形式化模型尤其有参考价值，因为原始工程文档往往就长成这种样子。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `4` 页 `Definition`，把 seven components、initial configuration 和 running scenario 抄出来，先确认这个 system boundary 到底包含哪些气缸、阀门和传感器。然后直接跳到第 `5-6` 页，专门读 `psOn[c1]=v1On`、`s1On[c2]=v1Off&v2On`、`s2On[c3]=timerT1`、`tm(2s)[c4]/v2Off&v3On` 这些控制关系，把 guard、事件和动作分列整理。

如果后续还要核对实现层，再看文末由 control model 生成 ladder diagram 的部分，确认这些 transition 如何变成 PLC rung。前半部分对 Statecharts 一般语义的介绍、方法流程和工具背景可以放到第二轮再看；对重做 `STM.md` 而言，最优先的仍是 tagged machine 的对象定义、两秒按压 timer、以及送料-压标-取件三段主控制链。
