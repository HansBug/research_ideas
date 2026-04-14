# 双输送带选料与装配状态图控制 / Ladder Diagram based on State Diagram for Selection and Assembling Part on Dual Conveyor

## 论文在讲什么

这篇论文关注的不是抽象 PLC 编程技巧，而是一个具体的双输送带工作单元。作者把上、下两段输送带当成一个需要完成“检测工件高度和材质，再做分流和装配”的离散制造控制对象，用 `state diagram -> primitive flow table -> merged flow table -> ladder diagram` 的链路来压缩 PLC 程序规模，并明确说明最后得到的是 `32` 个 rung、`3 KB` 程序容量的实现。

系统本身带有比较完整的工程语义。文中不是只画一个框图，而是先交代 dual conveyor workcell 的物理目标，再给出 `Opt1-Opt6`、`Flag1/Flag2`、`T1-T6`、`CONV1/CONV2`、`Sol2/Sol3/Sol4`、`Chute1/Chute2` 等输入输出位和中间定时位，随后把这些位组织进不同 subprocess 的状态序列，因此论文主体一直围绕真实分拣/装配链展开。

## 控制系统在文中的位置

控制系统就是这篇论文最核心的对象。所谓“state diagram based ladder design”不是附属说明，而是作者描述双输送带控制器的主要方式。无论是 I/O bit 表、subprocess 状态序列表、primitive flow table，还是 relay/output 状态图和 ladder 转换，都是在围绕同一套 conveyor controller 的状态推进与输出动作展开。

对我们来说，这篇论文的价值在于它保留了很强的离散控制痕迹。很多 PLC 短文只会给出流程图或器件清单，但这里把状态、输入位变化、输出位开闭和定时触发写得相当显式，所以后续做 `STM.md`、数据集抽样或状态机建模时，不需要再从散乱段落里硬拼主链。

## 对我们为什么有用

这篇论文补的是 `🏭` 领域里比较扎实的顺序制造控制样本，而且和已有“灌装、包装、门控、洗衣机”类 PLC 样本不完全同构。它的特色在于把同一个工作单元拆成多个 subprocess，再用 flow-table 和 merged-flow-table 保住状态压缩逻辑，这对后续研究“LLM 如何从原文恢复更结构化的状态图”尤其有帮助。

另外，这篇论文对 `FSM + T1` 工业控制样本也有补差异价值。文中有扁平状态链，也有显式定时接点和分支动作，但没有明显层次结构，因此它既不像一些 elevator/traffic controller 那样以门控或相位切换为主，也不同于更方法化的 IEC/ECC 语义论文，正适合拿来补工业 PLC 的另一种写法。

## 如果需要人工细读，建议怎么读

人工回看原文时，建议先读第 `1` 页 `Dual Conveyor Workcell Systems`，确认控制对象、工件差异和 top/bottom conveyor 的系统边界；再直接跳到第 `2` 页 `Table 1 / Table 2` 看 `X/Z/T` 位和各 subprocess 状态序列，把上游检测、定时、金属/塑料分流以及下游装配动作连起来。

第二轮再看第 `3-4` 页的 primitive flow table、merged flow table 和 `State Diagram (R/O)`，目标不是重学状态压缩理论，而是确认“哪些状态在合并、哪些输入触发迁移、哪些 relay/output 对应 ladder rung”。至于文中关于 flow-table 规则的解释性段落，可以放到最后读，因为它们更多是实现方法说明，不是控制对象边界本身。
