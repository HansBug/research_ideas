# 自动制动告警 TTool XML 条件样例

## 1. 来源

- 原始条目：[ttool-ai-smd-subset](../../corpora/seed_library/ttool-ai-smd-subset/)
- 论文 PDF：[paper.pdf](../../corpora/seed_library/ttool-ai-smd-subset/paper.pdf)
- 论文全文提取：[paper_content.txt](../../corpora/seed_library/ttool-ai-smd-subset/paper_content.txt)
- BibTeX：[bibtex.bib](../../corpora/seed_library/ttool-ai-smd-subset/bibtex.bib)
- 单篇说明：[seed_desc.md](../../corpora/seed_library/ttool-ai-smd-subset/seed_desc.md)
- 一手资产说明：[assets/README.md](../../corpora/seed_library/ttool-ai-smd-subset/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../corpora/seed_library/ttool-ai-smd-subset/seed_resource_registry.json)
- 原始 pair：`ttool-ai-automatedbraking`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | 作者仓库 ZIP 中 `AutomatedBraking/automatedbraking.md` 的系统规格文本。 |
| [stm0.xml](./stm0.xml) | 同一作者工件中 `AutomatedBraking/automatedbraking.xml` 的 TTool/SysML/AVATAR XML。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、ZIP member locator、哈希、生成方式与 trace 字段。 |

## 3. 系统说明

该样例描述车辆在危险情境下通过车车通信广播警告消息的控制 / 安全相关系统。底盘与安全域 ECU 检测危险事件，底盘安全控制器评估情况并向执行器 ECU 和动力总成域发送缓解命令，同时向通信单元发送车辆动态状态和计划动作。通信单元通过 DSRC 向附近车辆广播包含位置、速度、加速度、航向、时间、可靠性、车辆类别、发送者标识、事件代码以及计划动作等信息的紧急消息。生成出的 `STM_0` 文件是完整 TTool XML，包含 SysML/AVATAR 工件，不是已经切干净的纯 T0 状态机。

## 4. NL 中文完整翻译

当发生危险情况，迫使驾驶员或车辆自身执行某种机动动作时，这可能危及其他车辆。为了警告其他车辆，本车会发出警告消息。附近处于危险中的车辆随后可以根据信息作出反应。

底盘与安全域中的一个 ECU 会检测危险；这可能由安全气囊触发、环境传感器发现行驶方向上的障碍物，或由驾驶员或自动系统执行紧急制动所触发。底盘安全控制器（CSC）通过底盘域总线获得危险情况信息。CSC 会评估该情况，并采取措施缓解本车面临的危险。这些措施会产生给底盘与安全域中执行器 ECU 的命令，并额外向动力总成域发送命令，以获得有助于处理危险的驱动力调整。同时，它还会向通信单元（CU）发送信息。这些信息包含当前车辆动态状态的数据，以及关于计划动作（减速或加速、转向等）的详细信息。

CU 将通过 DSRC 接口向附近车辆发出包含这些信息的警告消息。紧急消息包含车辆的经度、纬度、高度、速度、加速度和航向，消息生成时间、消息过期时间、表示信息可靠性的指示符、对车辆进行分类的代码、标识消息发送者的 id、对应急情况进行分类的事件代码，以及计划的加速度和航向。所有这些信息都会打包到一个消息帧中，该消息帧还会添加校验和、协议处理信息，以及在必要时添加安全信息。

功能需求：

- 不允许在没有真实危险的情况下发送警告消息。
- 任何单一单元中的故障都不应导致错误消息。
- 任何单一通信中的故障都不应导致错误消息。
- ECU 中的任何单一故障都必须可检测。
- 关于危险事件的信息必须按照通信拥塞控制算法进行广播。
- 关于危险的信息必须以最高优先级向其他车辆广播。
- 必须保证广播车辆信息的隐私。

技术需求：

- 从危险检测到广播 car2X 消息的最大延迟应小于 150 毫秒。
- 底盘与安全域以及动力总成域中总线上附加安全信息的大小应小于净数据的 15%。

安全方面：

- 必须保证广播车辆信息的隐私。

请使用 4 到 10 个 block。

## 5. STM 文件说明

- 格式：TTool/SysML/AVATAR XML，文件为 [stm0.xml](./stm0.xml)。
- 谱系：完整 TTool 工件，可能包含 block diagram、use-case / class / state-machine 相关信息、attributes、signals、guards/actions 与时间语义。
- 时间特性：存在小于 150 ms 这类需求以及 TTool timing operator 语义线索；后续若要作为 T0 seed，必须先切出状态机子集并记录降级策略。
- 重要 caveat：该样例是条件样例，用于暴露 XML / SysML / TTool 切片压力；不能在未切片和未审计前当作纯 T0 FSM/HSM/EFSM/statechart 输入。
