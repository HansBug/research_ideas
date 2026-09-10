# 面向自然语言描述的状态机问题发现：模型事实、结构化引导与执行反馈

**Evidence-Guided LLM Discovery of Issues in State Machines against Natural-Language Descriptions**

## 摘要

状态机（state machine）中的行为偏差常涉及多条迁移（transition）和事件响应（event response），仅核对元素是否存在难以发现这类问题。本文研究如何依据自然语言描述（natural-language description）发现既有状态机中的问题，并给出可定位、可复核的报告。我们提出一种结合大语言模型（large language model，LLM）、模型检查事实（model inspection facts）、结构化中间引导（structured intermediate guidance）和执行反馈（execution feedback）的方法。检查事实揭示模型关系，中间引导将描述中的义务（obligation）与候选问题（candidate issue）联系起来，类型化谓词（typed predicate）及后端（backend）的执行结果支持最终报告判断。我们公开了由博士生人工标注的、面向 54 个描述与模型制品对的 145 条参考问题（reference issue）数据集。在三轮重复运行中，完整方法（full method，Full）相对同模型直接发现基线（direct-discovery baseline）的平均覆盖率（mean coverage）提高 11.49 至 22.53 个百分点，其中行为层问题提高 24.79 至 44.44 个百分点。三项消融实验（ablation study）分别表明检查事实和中间引导有助于扩大问题覆盖，执行反馈则在固定候选与既定评价政策下提高报告精确率（precision）0.72 至 4.03 个百分点。

## 1. 引言

状态机通过状态（state）、迁移（transition）和事件（event）描述控制软件的模式切换与运行过程。无论模型由开发者编写还是由 LLM 生成，复核者都需要判断它是否实现了自然语言描述要求的行为，并将发现定位到具体的模型元素。已有行为模型生成研究表明，获得语法正确的模型只是建模过程的一部分；理解模型中遗漏的响应、无法完成的流程以及不符合描述的交互，仍然需要分析描述与行为之间的关系。[^wang2025][^uml_survey]

这种分析超出了元素对应检查的范围。例如，描述要求设备接收停止事件后返回空闲状态。模型即使包含停止事件和空闲状态，也可能在停止后进入一个没有出口的状态；另一种情形是返回迁移已经存在，但其守卫（guard）在相关路径上始终不成立。前者需要检查跨迁移可达性（reachability），后者还需要结合变量（variable）更新判断路径是否可行。复核报告既要指出模型事实，也要解释该事实为何违反描述中的义务。

LLM 能够解释自由文本并提出问题，但直接询问模型“哪里有问题”并不能保证它系统地检查上述行为关系。Li 与 Zheng 已研究自然语言需求与既有模型之间的一致性检查（consistency checking），行为模型正确性评价方法（Behavioral Model Correctness Evaluation，MCeT）则使用 LLM 评价行为模型的正确性。与此同时，模型检查（model checking）能在给定模型和形式性质后提供精确结果。两类能力之间仍有一个发现过程需要组织：哪些描述应转化为检查义务，哪些模型事实值得追踪，以及一项可执行检查的结果能否支撑完整的问题主张。[^li_zheng][^mcet][^baier_katoen]

本文将模型事实、候选组织和执行证据结合起来。方法首先将源制品（source artifact）投影为带来源映射（source mapping）的分析表示，提取结构和行为事实；随后围绕描述义务生成并扩充候选；对适用候选完成谓词绑定与执行后，再结合返回结果复核候选并形成报告。源制品在整个分析过程中保持固定。图 1 以停止后无法返回的示例说明这三个环节如何衔接。

本文有以下四项贡献：

1. **C-1：模型事实支持的问题发现。** 将可追溯的结构、拓扑（topology）和运行事实接入候选发现，使发现过程能够直接引用并检查跨迁移行为信息。
2. **C-2：围绕义务的结构化中间引导。** 通过义务组织、多视角发现、候选扩充和语义复核（internal semantic assessment），连接描述要求与模型行为，扩大有依据的候选范围。
3. **C-3：基于类型化谓词与后端求值的执行反馈。** 将候选中的可检查命题绑定到明确对象和执行范围，并将返回结果用于最终报告的保留、反驳和修订。
4. **C-4：人工标注的状态机问题数据集。** 公开面向 54 个描述与状态机制品对、由博士生人工标注的 145 条参考问题，以及逐条来源定位、问题分类和判定依据，为后续问题发现研究提供固定评价材料。

实验首先在 gpt-5.6-luna 上分析完整方法的效果和问题层级（problem level）差异，再考察另外三种模型配置；三项消融分别检验检查事实、中间引导和执行反馈。结果显示，发现组织主要扩大覆盖，执行反馈主要改善固定候选下的报告选择。这些结果为如何结合 LLM 的语义分析与确定性执行提供了经验依据。

## 2. 背景与相关工作

### 2.1 问题层级与证据强度

问题层级（problem level）描述陈述一个问题所需的信息范围。本文将问题分为点状或表面对齐问题（surface-alignment issue，L0）、结构或局部状态问题（structural or local-state issue，L1）和行为或全局问题（behavioral or global issue，L2）。L0 例如描述中点名的元素缺失；L1 例如层次归属或触发槽位错误；L2 则涉及跨迁移路径、可达性、终止（termination）、响应或全局交互。

这一分类综合了既有模型分析中的不同信息范围。统一建模语言（Unified Modeling Language，UML）一致性研究区分句法约束与需要考虑动态行为的约束；模型检查理论进一步区分单状态命题与必须考察路径片段的性质。[^torre][^knapp][^baier_katoen] L0/L1/L2 是本文据此定义并在参考集合上冻结的操作化分类，不是这些文献原有的三级枚举。分类依据是问题本身：图遍历和 LLM 都可能发现 L2 问题，使用某种后端也不自动提高问题层级。

证据强度（witness strength）描述报告提供的依据。无精确定位的主张记为 W0；具有源制品定位但没有合格执行结果的报告记为 W1；在 W1 的基础上，具有满足对象绑定、来源和执行资格要求的可执行证据（executable evidence）时记为 W2。需求异味（requirements smell）研究强调具体定位和检测机制，模型检查中的反例（counterexample）则进一步提供可检查的行为证据；抽象上的反例仍可能无法在源模型中成立。[^femmer][^baier_katoen][^clarke_cegar] 本文用 W0/W1/W2 将这些证据区别操作化，并不将 W2 等同于完整自然语言主张已经得到证明。L 与 W 因而相互独立：行为问题可以只有 W1 证据，局部结构问题也可以具有 W2 证据。

### 2.2 需求解释、模型分析与问题发现

需求与模型的一致性检查首先需要建立跨制品对应关系。Li 与 Zheng 将需求结构化，检查业务对象、过程和状态关系，并输出可定位的不一致；LiSSA 研究追踪关系恢复（traceability link recovery），帮助连接语义相关的制品；MCeT 进一步让 LLM 评价行为模型并报告问题。[^li_zheng][^lissa][^mcet] 这些工作为本文提供了任务与评价基础，但对应关系本身不足以确定路径可行性、终止或事件响应是否满足描述。本文关注如何把模型分析得到的行为事实引入发现过程，并让检查结果影响报告决定。

形式化方法（formal methods）为这一步提供了明确的分析能力。状态机的形式化与自动验证已有系统研究，层次状态需求的完整性（completeness）和一致性也有成熟检查方法。[^uml_survey][^heimdahl][^heitmeyer] 性质模式（property pattern）与语法约束的性质生成研究帮助将需求转化为形式性质。形式化需求获取工具（Formal Requirements Elicitation Tool，FRET）也支持这一转换。[^dwyer][^fret][^estivill] 这些方法通常需要先给出待验证的对象和性质；对于自由文本与既有模型，发现哪些问题值得检查、正确绑定模型对象，以及解释结果对描述的意义，仍然是必要环节。测试预言问题（oracle problem）说明，执行一个查询与判断软件是否满足用户意图具有不同的证据要求。[^barr]

本文围绕这一衔接过程组织方法：模型检查事实为候选提供具体依据，中间引导将事实与描述义务联系起来，类型化谓词把其中可检查的部分交给确定性后端，语义复核再判断结果对完整主张的支持程度。与单独生成性质或直接评价模型相比，该组织方式同时关心候选覆盖与报告证据；其作用由同模型基线和三项消融检验。

行为模型生成与补全则为本文提供上游应用场景。Wang 等研究 LLM 生成模型及反馈，de Biase 等研究从“给定—当—则”（Given–When–Then）需求补全状态机。[^wang2025][^gwt] 本文接收这些流程可能产生的既有模型，输出问题而不修改输入。实验使用同模型直接发现基线：现有受控自然语言检查器需要改变输入形式，模型内部检查工具则不直接回答自由文本与既有 PlantUML 制品之间的问题，因此不作为本实验的可运行同任务基线。

## 3. 问题定义与分析范围

### 3.1 输入、输出与义务

给定自然语言描述 $d$ 和既有源状态机制品 $m$，问题发现任务输出报告集合 $\mathcal{R}$。每份报告包含问题主张、描述引文、源位置、推理依据，以及适用时的执行证据。报告需要建立两个联系：主张中的关键事实确实属于 $m$，该事实与 $d$ 所要求的行为存在冲突。

义务可以来自描述中的明确语句、实现所述行为必需的隐含条件，或有依据的领域要求。报告须说明义务来源及其与模型事实的关系；一个没有出边的状态只有在应当继续响应或返回的条件下，才能据此形成问题。领域知识参与需求满足关系的解释，符合 Zave 与 Jackson 对需求、规约和环境知识的区分。[^zave_jackson] 本文通过第 5 节的评价协议判断报告是否建立了这种关系。

### 3.2 有限控制状态机及其执行

方法使用有限控制状态机（finite control state machine，FCSTM）作为分析表示。对当前支持的单区层次片段（single-region hierarchical fragment），本文采用如下抽象记法：

$M=(S,H,I,F,E,V,\nu_0,T,A)$。

其中，$S$ 为有限状态集合；$H$ 为无环的父子关系，形成单根状态层次；$I$ 指定根和复合状态（composite state）的初始入口；$F$ 记录终止位置；$E$ 为事件集合；$V$ 为带类型的持久变量集合，$\nu_0$ 为初始赋值；$A$ 包含状态进入、退出、驻留及迁移动作（action）；$T$ 为迁移集合。每条迁移写为 $t=(s,e,g,a,s')$，其中 $s,s'$ 为源和目标位置，$e\in E\cup\{\varepsilon\}$ 表示显式事件或无触发事件，$g$ 为布尔守卫，$a\in A^*$ 为有序动作序列。入口和终止标记参与层次进入与完成处理，不作为普通业务事件。

运行配置（configuration）写为 $c=(q,\nu)$，其中 $q$ 为当前活动状态及其祖先形成的控制配置，$\nu$ 为变量赋值。运行时依据活动层次、事件输入和守卫选择迁移，并按规定顺序执行相关动作；一个可观察的宏步（macro-step）记为 $c\xrightarrow{u}_M c'$，$u$ 为本步事件输入。宏步也涵盖未发生迁移时适用的驻留处理。由此得到的有限轨迹（finite trace）是 $c_0,u_0,c_1,\ldots,u_{k-1},c_k$。有限控制只要求 $S$ 有限，不要求变量取值域有限；有界验证（bounded verification）针对明确的宏步上界编码和求解。

当前 PlantUML 适配器保留声明范围内的层次、事件、变量、守卫和动作。适配器将不支持的时钟（clock）、时间事件（time event）、正交区域（orthogonal region）、历史伪状态（history pseudostate）和分叉/汇合（fork/join）记录为能力限制。新的源语言需要相应适配器及独立评测，本文实证范围为当前 PlantUML 片段。

### 3.3 投影与来源归属

适配器将源制品投影为 FCSTM，并维护源位置与分析对象之间的映射 $\pi$。转换中补出的辅助元素与源元素分别标记；报告引用源位置，执行记录同时保存用于求值的工作表示及其范围。这样，复核者可以区分源模型中的行为与表示转换引入的现象。

投影失败、对象绑定缺失或执行未完成产生分析诊断（analysis diagnostic），方法仍保存已有候选和证据。这些诊断用于说明检查未闭合的原因；只有回溯后建立了源事实与描述义务的冲突，才能形成针对源制品的问题报告。

## 4. 方法

### 4.1 总体流程

图 1 展示从源制品到最终报告的流程。确定性程序负责投影、事实提取和谓词求值，LLM 负责描述解释、候选发现及语义复核。三个环节通过来源位置、义务引用和候选身份（candidate identity）关联：检查事实回答模型中有什么关系，中间引导决定追踪哪些关系，执行反馈帮助判断最终应报告哪些主张。

![Method overview and illustrative example](./figures/method.svg)

**Figure 1. Evidence-guided issue discovery. Model inspection facts support candidate generation; structured intermediate guidance links candidates to obligations; predicate execution informs report decisions. The lower panel is an illustrative example, excluded from the evaluation corpus.**

### 4.2 模型检查事实

适配器解析源制品后，提取声明与槽位、状态层次、迁移关系、可达集合、出边集合、事件消费者和有界运行前沿（bounded execution frontier）。这些事实连同源映射进入发现流程，候选可以引用已计算的对象关系，而不必仅从文本重复推断。例如，“停止后的状态没有出口”可以直接关联相应状态和出边集合，再由描述判断该状态是否仍有返回义务。

源记法与投影结果也可能存在差异：解析器可能将自由文本标签中的动作识别为触发事件，将复合标签识别为一个事件。方法因此同时保留源索引并检查两种表示的分歧。候选需说明分歧怎样影响描述义务，避免把一次规范化本身当成缺陷。

事实提取和后续执行使用既有图分析、仿真（simulation）及可满足性模理论（satisfiability modulo theories，SMT）求值能力。Stateflow、Sismic 和状态图可扩展标记语言（State Chart XML，SCXML）等工具或标准同样提供状态机分析与执行基础。[^baier_katoen][^stateflow][^sismic][^scxml] 本方法的作用在于把这些能力生成的事实与描述解释、候选和报告连通，检查事实消融用于检验这种接入对发现覆盖的影响。

### 4.3 结构化中间引导

方法先从描述中提取带引文的义务，并补全尚未覆盖的描述片段。发现过程采用互补视角：一类核对结构、契约和对应关系，另一类追踪跨迁移行为后果。每个候选记录主张、来源位置和依据，从而把宽泛的审查任务转化为可追踪的检查对象。

随后，方法针对未覆盖义务、行为前沿和领域不变量（domain invariant）扩充候选，并使用确定性候选补充和执行探测处理相应缺口。一次发现得到的候选因而可以继续沿相关状态、事件和行为关系展开。此处的中间引导包含 LLM 处理和确定性处理，是一组共同组织发现的机制。

语义复核综合源文本、候选依据和已有执行结果，检查事实是否成立、义务是否适用，以及是否存在证据相容的合法替代解释。复核结果决定保留、反驳或受限修订（bounded revision）。预算耗尽时，方法保留已有产物并记录未满足的检查义务，使困难样本仍进入最终评价。

以图 1 为例，检查事实只能说明 Halt 没有出口；义务组织将其与“停止后返回 Idle”联系起来，行为分析据此提出响应问题。另一候选可能误称模型缺少 Stop 迁移。两者都可以进入具体检查，但最终是否形成报告取决于各自主张与证据的关系。

### 4.4 类型化谓词与执行反馈

类型化谓词规定可检查命题的参数、对象类型和求值范围。LLM 选择谓词并绑定状态、迁移、事件或行为窗口；程序核对来源引用与实例身份，再编译和执行查询。当前接口包括结构检查（structural check）、拓扑检查（topological check）、轨迹检查（trace check）和有界验证四类，共 12 种谓词，定义依据包括 UML 元模型（metamodel）与性质模式。[^uml251][^dwyer]

结构检查用于元素存在性、迁移、触发、动作挂接和守卫关系；拓扑检查分析图上的路径与进展；轨迹检查观察声明刺激下的事件消费、状态到达和保持；有界验证分析指定窗口内的行为。对于图 1，`may_reach(Halt, {Idle})` 返回 false，表明所检查拓扑中不存在返回路径；精确迁移存在性检查则返回 true，反驳“缺少 Stop 迁移”的同一主张。拓扑上的路径存在只说明连接关系，不能单独保证守卫可行。

执行返回值（verdict）为 true、false 或 unknown。true 表示绑定命题成立，方法据此拦截与它相反的同一缺陷主张；false 表示该命题不满足，语义复核继续判断它是否违反描述义务；unknown、超时或不支持表示尚未取得确定结果。具有充分来源依据的报告可以保留为 W1，而无需把执行未完成解释为问题。

满足 W2 要求的执行回执（execution receipt）保存模型和计划身份、参数、来源引用、分析范围、返回值及可用轨迹。复核者据此能够在同一工作表示上重复查询。抽象和有界窗口限制了证据含义：执行成立的是绑定命题，完整报告仍包含义务解释与来源归属。[^clarke_cegar] 第 6.5 节通过固定上游候选、屏蔽执行反馈的比较，分析这些结果对最终报告的作用。

### 4.5 发布与评价隔离

发布阶段按精确检查身份去重，将规则可识别的关联主张组织为根报告（root report）和子主张（subclaim），并汇总同类守卫模式。子主张保留各自证据，根报告的 W 等级由根自身决定。报告数、子主张数和回执数分别统计。

方法输入仅包含描述、源制品及其派生分析材料，不含参考问题或外部标签。外部评价（external evaluation）在最终报告形成后执行，与方法内部语义复核分开。直接发现基线和 Full 使用同一描述与源制品，区别在于 Full 增加事实、义务、谓词和阶段结构。

## 5. 研究设计

### 5.1 研究问题

实验通过五个研究问题（research question，RQ）评价整体效果、模型适用性与三个技术机制。

- **RQ1：整体有效性。** 在 gpt-5.6-luna 上，Full 相对直接发现基线提高了多少问题覆盖，尤其是 L2 行为问题覆盖？
- **RQ2：跨模型适用性。** 在四种固定模型配置上，Full 相对各自基线的覆盖和报告精确率如何变化？
- **RQ3：检查事实的作用。** 关闭检查事实及其派生链后，问题覆盖如何变化，哪些行为问题不再进入候选？
- **RQ4：中间引导的作用。** 保留检查事实和谓词执行、移除中间引导后，有效报告产出、覆盖和精确率如何变化？
- **RQ5：执行反馈的作用。** 固定 Full 上游候选并屏蔽执行结果后，最终报告精确率和覆盖如何变化？

RQ1 和 RQ2 评价完整方法；RQ3、RQ4、RQ5 分别对应 C-1、C-2、C-3。C-4 为所有比较提供公开的输入对（input pair）和参考问题。

### 5.2 数据集与模型配置

输入来自 Wang 等公开的行为模型生成研究。我们按固定阶段选择经过上游反馈的状态机；语义反馈输出缺失时，采用已登记的生成回退。一个描述要求当前适配器不支持的并发与时间行为，因此排除它对应的六个制品。最终语料包含九个描述簇（description cluster），每簇六个上游模型制品，共 54 个输入对；上游参考模型不进入发现方法。[^wang2025]

语料涉及汽车、轨道交通、泵控制、设备操作模式、微波炉和无人机集群。博士生基于描述与源制品人工标注 145 条参考问题（reference issue），保存逐条来源定位、分类和依据。问题分布在 46 对制品上，其余八对仍参与全部实验。参考集合用于衡量已知问题覆盖，集合外报告则单独判断有效性。表 1 汇总语料规模和模型结构。

**表 1：评价语料与人工标注参考集合。结构统计基于全部 54 个制品；层级深度按归档的结构统计口径计算。**

| 项目 | 数量或范围 | 中位数 |
| --- | ---: | ---: |
| 描述簇 / 每簇制品 / 输入对 | 9 / 6 / 54 | — |
| 含参考问题的输入对 / 无参考问题的输入对 | 46 / 8 | — |
| 参考问题总数 | 145 | — |
| L0 / L1 / L2 参考问题 | 71 / 35 / 39 | — |
| 状态数 | 5–20 | 8 |
| 复合状态数 | 1–7 | 2 |
| 层级深度 | 1–5 | 2 |
| 迁移数 | 5–70 | 13.5 |
| 事件数 | 0–14 | 6 |
| 变量数 | 0–1 | 1 |
| 守卫数 | 0–14 | 1 |
| 迁移动作数 | 0–44 | 3.5 |

实验模型为 gpt-5.6-luna、claude-sonnet-5、qwen3.8-27b 和 muse-glimmer-30b。前两者采用托管服务，后两者采用固定权重与部署配置；名称对应冻结记录中的请求身份。每模型每条件分析相同的 54 对并重复三轮，共 162 次运行。gpt-5.6-luna 的 Full 与基线复用历史结果，另三种模型为后续扩展。历史注册表有 19 项定义，后续注册表为 12 项；实际谓词与历史映射随材料保存。模型调用日期、权重版本、服务参数和输出预算保存在可复核配置中，本文按同模型条件配对比较，不将四模型绝对指标作能力排名。

### 5.3 基线与消融条件

直接发现基线通过单次提示（prompt）生成定位报告，不使用工具或独立复核循环。Full 使用完整流程。三项消融分别关闭检查事实、中间引导和末端执行反馈，保留范围见表 2。

**表 2：比较条件与干预范围。各条件共享描述和源制品。无检查事实仅在 gpt-5.6-luna 上运行，其余条件覆盖四种模型配置。**

| 条件 | 发现输入与组织 | 谓词执行 | 最终语义复核 | 回答问题 |
| --- | --- | --- | --- | --- |
| 直接发现基线 | 描述与源文本；单次生成定位报告 | 无 | 无独立复核阶段 | RQ1、RQ2 |
| Full | 检查事实、义务与分阶段候选组织 | 保留 | 保留 | 共同对照 |
| 无检查事实 | 关闭检查事实及派生生产、消费链；保留投影、来源及普通语义发现 | 保留 | 保留 | RQ3 |
| 无中间引导 | 保留检查事实与谓词定义；一次直接生成候选 | 保留 | 关闭；保留确定性发布 | RQ4 |
| 无执行反馈 | 冻结 Full 的义务、候选、绑定和计划 | 复用原执行；向末端隐藏结果及关联证据 | 重放受影响判断；保留其他规则 | RQ5 |

无检查事实条件同时关闭相关事实的生产、消费及派生候选，保留投影、来源追踪和候选专属谓词执行。它与历史 Full 在注册表、调用渠道、日期和恢复历史上存在差异，作为检查事实及派生链的历史对照解释。

无中间引导条件保留检查事实、谓词定义和执行，但以一次候选生成代替义务组织、多视角发现、扩充、确定性补充与探测、内部语义复核及纠错。该条件测量整组机制的联合效果；基线与 Full、中间引导消融与 Full 均未匹配调用预算。

无执行反馈条件冻结 Full 的义务、候选、绑定和计划，将 true、false、unknown 统一遮蔽为中性的 unknown，移除关联轨迹、反例、理由及依赖结果的自动拦截，再进行末端重放（terminal replay），重新完成受影响的判断。其余校验和发布规则保留，上游模型与后端不重新运行。因此，该条件分析既定候选下执行反馈对报告选择的影响，上游候选已吸收的历史反馈可能仍然存在。

### 5.4 报告判定

报告评价同时考察源事实、违反义务的依据及参考关系。缺陷状态（defect status）D2 表示关键事实和违反义务成立，且没有证据相容的合法替代解释；D1 表示仍存在这样的替代解释；D0 表示违反义务未建立或设计解释正当。A0 标记关键源事实不成立。参考关系分为充分匹配（full match，FULL）、部分匹配（partial match，PARTIAL）和无匹配（no match，NO）。FULL 要求能够识别同一问题，PARTIAL 表示有关联但不足以建立完整命中，NO 表示未建立关系。

这一评价采用 MCeT 的同根因问题匹配与新增真实问题思路，并参考静态分析工具评测（Static Analysis Tool Exposition，SATE）对相关发现、真实缺陷和不完备参考真值（ground truth）的区分。[^mcet][^sate] 据此，本文使用已知有效报告（valid known report，K）、集合外有效报告（valid novel report，N）和无效报告（invalid report，I）作为操作化类别。N 不因未进入参考集合而成为误报，也不等同于去重后的新缺陷数；W 等级不参与关系匹配门槛，基线定位报告可以获得 FULL。

图 2 给出产生本文冻结数字的关系优先规则（relation-first policy）：A0 报告计 I；其余报告具有 FULL/PARTIAL 关系时计 K；无关系时，D1/D2 计 N，其余计 I。该规则允许部分 D0 报告因参考关系计为 K，因此第 5.5 节同时给出严格精确率，以单独考察具有 D1/D2 语义支持的有效报告。

![Frozen report adjudication policy](./figures/adjudication.svg)

**Figure 2. Report adjudication under the frozen relation-first policy. The evaluator records reference matching and semantic status separately. The execution-feedback ablation first applies its frozen accounting rules, then uses the same evaluator for residual reports.**

外部评价器（external evaluator）固定为 gpt-5.6-luna，按冻结协议进行两次判读和分歧仲裁；语义判断与参考匹配的调用角色及输入材料分开。人工构建参考数据集与逐报告评价是两个过程：历史 gpt-5.6-luna Full 的 903 份报告已有作者确认，新增实验的逐报告人工确认数为 0。本文报告的新增结果来自该固定评价协议，统计复算保持原标签。

执行反馈消融还使用已冻结的核算规则。3675 份报告中，130 份重新发布原 true 候选的同一缺陷主张，按规则计 I；3240 份与 Full 内容等价（content equivalent），复用原标签；305 份交由同一评价协议新判。原 true 可能只确认完整主张中的较窄命题，因此这些指定为 I 的报告并非全部经过独立语义反证。RQ5 的精确率以该政策为条件，不将其扩大为完整谓词系统的端到端因果效果。

### 5.5 指标与统计分析

令 $\mathcal{E}$ 为 145 条参考问题，$H_r$ 为第 $r$ 轮至少获得一份 K 类报告 FULL 匹配的问题集合。同一问题在同轮最多计一次，PARTIAL 不进入主命中。平均覆盖率（mean coverage）、三轮并集覆盖率（union coverage）和三轮稳定覆盖率（stable coverage）分别定义为：

$\mathrm{hit@1}=\frac{\sum_{r=1}^{3}|H_r|}{3|\mathcal{E}|},\qquad \mathrm{hit@3}=\frac{|H_1\cup H_2\cup H_3|}{|\mathcal{E}|},\qquad \mathrm{hit@all}=\frac{|H_1\cap H_2\cap H_3|}{|\mathcal{E}|}$。

它们的分母分别为 435、145、145。分层平均覆盖的 L0/L1/L2 分母为 213/105/117。令 $k,n,i$ 为全部发布报告中的 K/N/I 计数，$\ell(x)$ 和 $D(x)$ 分别为报告 $x$ 的外部类别和缺陷状态。普通报告精确率与严格报告精确率（strict precision）定义为：

$P=\frac{k+n}{k+n+i},\qquad P_{\mathrm{strict}}=\frac{\sum_{x\in\mathcal{R}}\mathbf{1}[\ell(x)\in\{K,N\}\land D(x)\in\{D1,D2\}]}{|\mathcal{R}|}$。

两种精确率均以全部发布报告为分母。结果先合并三轮计数再计算比例，同时报告有效数量、无效数量和覆盖，避免将少报造成的较高比例理解为发现能力提高。零报告运行仍保留，其单次精确率未定义。W2 的报告比例与参考问题命中比例分别计算，根报告与子主张的证据也分别统计。

比较按同模型、同制品、同轮次配对。同一描述下的制品和重复运行存在相关性，因此整体比较和中间引导分析采用九个描述簇的配对簇重采样（paired cluster bootstrap），并检查逐轮结果。95% 区间反映当前案例集的簇间不确定性；本文不将报告数当作独立样本量。末端重放没有额外重复随机化，本文据合并结果描述其效应方向和幅度。

## 6. 结果

### 6.1 RQ1：完整方法的有效性

在 gpt-5.6-luna 上，Full 的平均覆盖从基线的 225/435（51.72%）提高到 323/435（74.25%），增加 22.53 个百分点；三轮并集覆盖从 105/145 提高到 130/145，三轮稳定覆盖从 47/145 提高到 82/145。按描述簇重采样，平均覆盖差值的 95% 区间为 16.67 至 28.33 个百分点。

主要收益来自行为问题。L2 平均覆盖从 45/117（38.46%）提高到 97/117（82.91%），增加 44.44 个百分点，差值区间为 23.08 至 68.63 个百分点。L0 从 108/213 提高到 153/213，L1 从 72/105 小幅提高到 73/105。图 3 将这些变化与其他模型并列，表明模型事实和分阶段发现能够补充直接语义发现容易遗漏的跨迁移关系。

![Coverage by problem level and model](./figures/coverage.svg)

**Figure 3. Mean coverage by problem level and model. Each panel compares the direct-discovery baseline with Full on the same inputs. Denominators for L0, L1, and L2 are 213, 105, and 117 issue-round units. Lines connect the paired conditions.**

gpt-5.6-luna 的普通精确率从 83.40% 变为 84.05%，严格精确率从 78.71% 降至 75.08%（表 3）。完整方法在这组配置上的主要优势因而是覆盖，尤其是 L2 覆盖。它产生的 323 个命中单位中，127 个由根报告提供 W2，计入子主张后为 137 个；报告级 W2 为 267/903。执行证据支持一部分发现，其余报告依靠来源定位与语义依据。

### 6.2 RQ2：跨模型适用性

**表 3：四种模型的基线与完整方法结果。R 为报告数；P 和 P_strict 为普通与严格精确率。hit@1 分母为 435，hit@3 和 hit@all 分母为 145。每个模型内部的两行构成配对比较。**

| 模型 | 条件 | R | K/N/I | hit@1 | hit@3 | hit@all | P | P_strict |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| gpt-5.6-luna | 基线 | 512 | 293/134/85 | 225/435（51.72%） | 105/145 | 47/145 | 83.40% | 78.71% |
| gpt-5.6-luna | Full | 903 | 561/198/144 | 323/435（74.25%） | 130/145 | 82/145 | 84.05% | 75.08% |
| claude-sonnet-5 | 基线 | 715 | 340/151/224 | 241/435（55.40%） | 110/145 | 48/145 | 68.67% | 53.43% |
| claude-sonnet-5 | Full | 823 | 536/183/104 | 291/435（66.90%） | 122/145 | 69/145 | 87.36% | 78.98% |
| qwen3.8-27b | 基线 | 455 | 247/122/86 | 225/435（51.72%） | 95/145 | 53/145 | 81.10% | 74.51% |
| qwen3.8-27b | Full | 958 | 599/256/103 | 311/435（71.49%） | 125/145 | 81/145 | 89.25% | 81.52% |
| muse-glimmer-30b | 基线 | 681 | 347/184/150 | 247/435（56.78%） | 95/145 | 69/145 | 77.97% | 70.04% |
| muse-glimmer-30b | Full | 910 | 544/229/137 | 322/435（74.02%） | 124/145 | 88/145 | 84.95% | 78.24% |

四种配置的平均、并集和稳定覆盖点估计均提高。平均覆盖增幅为 11.49 至 22.53 个百分点，L2 增幅为 24.79 至 44.44 个百分点；L0 也全部提高。L1 的变化则较小且方向不一，claude-sonnet-5 下降 8.57 个百分点。不同模型的收益幅度仍有差异，例如 claude-sonnet-5 总体覆盖差值的簇重采样区间为 −1.67 至 25.37 个百分点。

claude-sonnet-5、qwen3.8-27b 和 muse-glimmer-30b 的普通与严格精确率均高于各自基线。结合 gpt-5.6-luna 的结果，四种配置共同支持完整方法对问题覆盖、尤其是行为层覆盖的帮助；报告精确率的改善幅度及严格口径下的方向与模型有关。这里的适用性证据覆盖所测四种配置，尚不外推为所有 LLM 均有相同收益。

### 6.3 RQ3：模型检查事实的作用

**表 4：三项消融的合并结果。Full 见表 3。V 为 K+N；P 与 P_strict 以 V+I 为分母。各条件的保留范围和评价政策见第 5.3–5.4 节。**

| 条件 | 模型 | hit@1 | V | I | P | P_strict |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 无检查事实 | gpt-5.6-luna | 233/435（53.56%） | 654 | 160 | 80.34% | 77.40% |
| 无中间引导 | gpt-5.6-luna | 245/435（56.32%） | 494 | 176 | 73.73% | 68.36% |
| 无中间引导 | claude-sonnet-5 | 230/435（52.87%） | 554 | 130 | 80.99% | 74.27% |
| 无中间引导 | qwen3.8-27b | 193/435（44.37%） | 318 | 40 | 88.83% | 86.59% |
| 无中间引导 | muse-glimmer-30b | 175/435（40.23%） | 303 | 192 | 61.21% | 55.96% |
| 无执行反馈 | gpt-5.6-luna | 314/435（72.18%） | 749 | 187 | 80.02% | 71.05% |
| 无执行反馈 | claude-sonnet-5 | 285/435（65.52%） | 701 | 140 | 83.35% | 74.91% |
| 无执行反馈 | qwen3.8-27b | 312/435（71.72%） | 852 | 133 | 86.50% | 78.68% |
| 无执行反馈 | muse-glimmer-30b | 319/435（73.33%） | 769 | 144 | 84.23% | 78.09% |

关闭检查事实后，gpt-5.6-luna 平均覆盖从 323/435 降至 233/435。L2 覆盖从 97/117 降至 50/117，L2 稳定覆盖从 28/39 降至 10/39；L1 则从 73/105 增至 76/105。普通精确率下降而严格精确率上升，显示这项干预的主要损失集中在发现覆盖。

候选追踪进一步表明，55 个 Full 独有的 L2 命中单位中，46 个在无检查事实条件下缺少相应根性质候选。在制动装置案例中，夹紧状态没有后续出口，而描述要求反馈后恢复；关闭检查事实及其派生候选后，候选生成阶段可能尚未提出这类问题。该历史对照支持检查事实及派生链对行为发现的作用，追踪结果同时指出了损失发生的候选阶段。

### 6.4 RQ4：结构化中间引导的作用

移除中间引导后，四种模型的平均覆盖和有效报告数全部下降，四模型三轮的 12 组逐轮覆盖比较也均下降。模型等权平均覆盖从 71.67% 降至 48.45%，有效报告总数从 3106 降至 1669。该总数反映四种配置的报告产出，相同参考问题可以在不同模型中重复出现。

qwen3.8-27b 的变化说明为什么需要同时考察比例与产出：其严格精确率由 81.52% 升至 86.59%，但有效报告从 855 份减至 318 份，覆盖从 311/435 降至 193/435。muse-glimmer-30b 则同时减少有效报告并增加无效报告。按性质分析，非终止与守卫问题损失较大，不可达问题仍能保留，与该条件继续提供检查事实一致。

因此，中间引导的共同收益在于扩大有依据的候选和有效发现范围，而非使每个模型的所有比例指标都提高。该结果支持整组义务组织、扩充、探测和语义复核机制；各内部阶段的独立增益仍需要进一步分离。

### 6.5 RQ5：执行反馈对报告精确率的作用

固定上游候选并屏蔽执行反馈后，gpt-5.6-luna、claude-sonnet-5、qwen3.8-27b 和 muse-glimmer-30b 的普通精确率分别下降 4.03、4.01、2.75 和 0.72 个百分点，无效报告分别增加 43、36、30 和 7 份（表 4）。四种配置的合并结果方向一致，支持类型化谓词与后端结果对报告选择的帮助。

覆盖变化相对较小，qwen3.8-27b 还净增一个命中单位。语义复核仍拒绝多数原 true 候选，末端重放也会撤下部分旧无效报告，因此执行反馈与语义复核共同影响最终集合。muse-glimmer-30b 的变化最弱，第二轮普通精确率方向相反，严格精确率合并后仅下降 0.15 个百分点。

给定第 5.4 节的固定核算政策，执行反馈提高了四种配置的合并报告精确率。效果大小和逐轮方向提示其收益依赖候选及语义判断；这些数字刻画的是末端执行反馈的作用，不能分解为每种谓词或每个后端的独立效果。

## 7. 讨论

三项消融显示，扩大问题覆盖与约束报告承担互补职责。检查事实让行为关系进入候选，中间引导把这些关系与描述义务联系起来并持续扩充，执行反馈则影响既定候选中的报告选择。前两类机制主要改变发现覆盖，后一类机制主要改变主张的保留结果。这为设计 LLM 辅助分析工具提供了一个具体方向：在提升语义推理能力的同时，为候选提供可引用的模型事实，并在报告阶段检查证据的含义。

来源定位与可执行证据也为人工复核提供不同入口。定位支持对照描述和源制品，执行回执支持重查绑定命题。两者共同使用尤其适合解释抽象表示与源模型之间的差异。历史 gpt-5.6-luna 的 144 份无效报告中有 15 份涉及将内部表示或分析状态归给源制品，说明来源责任仍是报告质量的重要环节。公开数据集保留这些判断所需的输入与问题依据，便于后续研究使用同一参考集合比较不同发现与复核方法。

## 8. 局限与未来工作

当前方法面向单区层次状态机的声明片段。含时间约束、正交区域或更丰富数据语义的控制系统，需要扩展投影与执行能力，并验证来源映射是否保留相关行为。未来可按特征逐步增加适配器和后端，在每个支持片段上建立对应案例与证据检查，而不是仅扩大可解析语法。

自由文本中的隐含义务与合法设计选择仍需要语义判断。类型化谓词能够回答边界明确的查询，但不能覆盖所有描述意图；扩展谓词族、改进义务解释和识别抽象反例，是进一步提高报告质量的方向。公开参考集合有助于持续检验这些能力，也可以随新增领域材料扩充。

本研究使用九个描述簇、四种固定模型配置及三轮重复运行。后续研究需要在人工设计的工业模型、更大规模的制品及更多模型配置上检验效果，并开展独立人工报告复核。中间引导各阶段的作用和调用成本也值得通过预算匹配实验进一步分离。最终，工程师使用报告的效果还需要用户研究（user study）衡量，包括复核时间、问题理解和修复决策；本文尚未测量这些使用收益。

## 9. 结论

本文提出一种依据自然语言描述发现既有状态机问题的方法，将模型检查事实、结构化中间引导和类型化谓词执行反馈连接起来。54 个输入对上的实验表明，完整方法在四种固定配置中均提高问题覆盖，行为层收益最为一致；三项消融分别说明检查事实、中间引导和末端执行反馈的作用。本文同时公开博士生人工标注的 145 条参考问题及其来源依据，为后续研究提供可复用评价材料。

## 10. 数据可得性

[公开研究仓库](https://github.com/HansBug/research_ideas/tree/paper1/o2-outline-rebuild/project_1_llm_state_machine_modeling/paper_stm_issue_discover)提供输入来源、54 个输入对、145 条参考问题、逐条判定依据、冻结实验结果和无需调用模型的指标复算入口。[参考问题台账](https://github.com/HansBug/research_ideas/tree/paper1/o2-outline-rebuild/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2)保留来源与问题级标注；上游语料归属 Wang 等的公开研究。[^wang2025] 冻结结果的复算可重现本文统计，真实模型调用的随机性和人工判断过程则由各自记录说明。

## 参考文献


[^wang2025]: Yuan Wang, Ning Ge, Jiangxi Liu, Zhilong Cao, Zheping Chen, and Chunming Hu. “Generating SysML Behavior Models via Large Language Models: an Empirical Study.” *Proceedings of the 16th International Conference on Internetware*, ACM, 2025, pp. 366--377. https://doi.org/10.1145/3755881.3755926.

[^uml_survey]: Étienne André, Shuang Liu, Yang Liu, Christine Choppy, Jun Sun, and Jin Song Dong. “Formalizing UML State Machines for Automated Verification -- A Survey.” *ACM Computing Surveys*, 55(13s), 2023. https://doi.org/10.1145/3579821.

[^li_zheng]: Haibo Li and Lixiao Zheng. “Enhancing Requirements via Structured Formalization and Process-State Consistency Validation: An LLM-Assisted Test-Driven Framework.” *IET Software*, 2025, 2025(1), Article 6714956. https://doi.org/10.1049/sfw2/6714956.

[^mcet]: Khaled Ahmed, Jialing Song, Ou Wei, Bingzhou Zheng, and Boqi Chen. “MCeT: Behavioral Model Correctness Evaluation using Large Language Models.” *MODELS*, 2025, pp. 84--95. https://doi.org/10.1109/MODELS67397.2025.00014.

[^lissa]: Fuchß et al. “LiSSA: Toward Generic Traceability Link Recovery Through Retrieval-Augmented Generation.” *ICSE*, 2025. https://doi.org/10.1109/ICSE55347.2025.00186.

[^dwyer]: Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. “Patterns in Property Specifications for Finite-State Verification.” *ICSE*, 1999. https://doi.org/10.1145/302405.302672.

[^heimdahl]: Mats P. E. Heimdahl and Nancy G. Leveson. “Completeness and Consistency in Hierarchical State-Based Requirements.” *IEEE TSE*, 1996. https://doi.org/10.1109/32.508311.

[^heitmeyer]: Constance Heitmeyer, Robert Jeffords, and Bruce Labaw. “Automated Consistency Checking of Requirements Specifications.” *ACM TOSEM*, 1996. https://doi.org/10.1145/234426.234431.

[^fret]: Dimitra Giannakopoulou, Anastasia Mavridou, Julian Rhein, Thomas Pressburger, Johann Schumann, and Nija Shi. “Formal Requirements Elicitation with FRET.” *REFSQ 2020 Workshops*, 2020. https://ntrs.nasa.gov/api/citations/20200001989/downloads/20200001989.pdf.

[^estivill]: Vladimir Estivill-Castro and René Hexel. “Grammar-Prompted Synthesis of Verification Properties from Natural Language Requirements for Multiple Model Checkers.” *ENASE*, 2026. https://www.scitepress.org/Papers/2026/147167/147167.pdf.

[^barr]: Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. “The Oracle Problem in Software Testing: A Survey.” *IEEE TSE*, 41(5):507--525, 2015. https://doi.org/10.1109/TSE.2014.2372785.

[^gwt]: Maria Stella de Biase et al. “Completion of SysML State Machines from Given--When--Then Requirements.” *Software and Systems Modeling*, 2024. https://doi.org/10.1007/s10270-024-01228-3.

[^zave_jackson]: Pamela Zave and Michael Jackson. “Four Dark Corners of Requirements Engineering.” *ACM TOSEM*, 6(1), 1997. https://doi.org/10.1145/237432.237434.

[^baier_katoen]: Christel Baier and Joost-Pieter Katoen. *Principles of Model Checking*. MIT Press, 2008. Def. 3.20, §3.3.2, Def. 3.33, §3.2--3.3.

[^stateflow]: MathWorks. *Stateflow Edit-Time Checks* and *Simulink Design Verifier: Detect Dead Logic*. [Edit-Time Checks](https://www.mathworks.com/help/stateflow/ug/stateflow-edit-time-checks.html); [Detect Dead Logic](https://www.mathworks.com/help/sldv/ug/detect-dead-logic.html). Accessed 2026-09-04.

[^sismic]: Alexandre Decan. “Sismic — A Python library for statechart execution and testing.” *SoftwareX*, 12:100590, 2020. https://doi.org/10.1016/j.softx.2020.100590.

[^scxml]: W3C. *State Chart XML (SCXML): State Machine Notation for Control Abstraction*. W3C Recommendation, 1 September 2015. https://www.w3.org/TR/scxml/.

[^uml251]: Object Management Group. *Unified Modeling Language (UML), Version 2.5.1*. 2017. https://www.omg.org/spec/UML/2.5.1/PDF.

[^clarke_cegar]: Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. “Counterexample-Guided Abstraction Refinement.” *CAV*, 2000. https://doi.org/10.1007/10722167_15.

[^sate]: Vadim Okun, Aurelien Delaitre, and Paul E. Black. *Report on the Static Analysis Tool Exposition (SATE) IV*. NIST SP 500-297, 2013. https://doi.org/10.6028/NIST.SP.500-297.

[^torre]: Damiano Torre, Yvan Labiche, and Marcela Genero. “UML Consistency Rules: A Systematic Mapping Study.” *EASE*, 2014. https://doi.org/10.1145/2601248.2601292.

[^knapp]: Alexander Knapp and Till Mossakowski. “Multi-view Consistency in UML.” In *Graph Transformation, Specifications, and Nets*, LNCS 10800, 2018. https://doi.org/10.1007/978-3-319-75396-6_3. Author manuscript: https://arxiv.org/abs/1610.03960.

[^femmer]: Henning Femmer, Daniel Méndez Fernández, Stefan Wagner, and Sebastian Eder. “Rapid Quality Assurance with Requirements Smells.” *Journal of Systems and Software*, 123:190–213, 2017. https://doi.org/10.1016/j.jss.2016.02.047.
