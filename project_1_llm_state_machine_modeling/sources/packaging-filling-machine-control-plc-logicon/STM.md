# Development of the Packaging and Filling Machine Control Program Using PLC Logicon - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把散料包装机的主流程写成“主程序 + 若干子程序”的层次控制链，并明确交代了上料、填充、封口、称重剔除、故障等待与复位恢复。

## 条目 1: Hierarchical packaging-machine supervisor with fill-seal-quality cycle

- 控制对象：工业自动化与离散制造领域的散料包装/灌装机主控程序
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 PLC 控制散料包装机的层次化主程序，管理螺旋送料、振动给料、料斗闸门、纵横热刀、输送带、称重质检与故障复位。
- 判断：算。对象是具体包装机主控逻辑，原文按设备链路、操作按钮、主程序/子程序和故障恢复把整条离散控制流程写得很清楚。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，系统构成与工艺过程，`paper_content.txt` 第 67-104 行
> Исследуемая система состоит из шнекового питателя, связанного с вибролотком, и приемного бункера с задвижкой. От бункера ведет труба, вокруг которой оборачивается термосвариваемая пленка.
>
> При накоплении в приемном бункере требуемого количества продукта открывается задвижка, после чего продукт поступает в открытый пакет. В следующем цикле при формировании горизонтального шва верх пакета запаивается и отрезается.
>
> Готовый пакет с продуктом по конвейеру поступает в зону контроля качества ... Пневмотолкатель обеспечивает удаление пакетов с весом, не соответствующим требуемому, с конвейерной линии.

#### 摘录 B

- 出处：第 2 页，操作按钮与主流程起点，`paper_content.txt` 第 105-133 行
> В программе должны обеспечиваться отслеживание аварийных ситуаций и возможность экстренной остановки всей системы в случае возникновения аварии. Активация, возобновление и завершение работы системы осуществляются оператором с помощью кнопок «Пуск», «Стоп» и «Сброс аварии».
>
> При нажатии оператором кнопки «Пуск» включается шнековый питатель ... Вибролоток прекращает работу при достижении необходимого количества продукта в бункере. Затем открывается задвижка и продукт поступает в открытый пакет.
>
> Термоножи начинают запайку швов при наполнении приемного бункера ... После заполнения пакет запаивается и поступает по конвейеру в зону контроля качества.

#### 摘录 C

- 出处：第 3 页，主程序与子程序组织，`paper_content.txt` 第 145-170 行
> Часть функций были вынесены в отдельные подпрограммы (опрос устройств, движение термоножей, контроль качества, запись температуры). В основной программе производится вызов каждой подпрограммы при условии отсутствия аварийной ситуации.
>
> Наполнение приемного бункера с помощью вибролотка производится только при условии срабатывания датчика закрытия задвижки, что предотвращает неправильное дозирование продукта.
>
> Алгоритм последовательной работы термоножей предусматривает строгий порядок перемещения каждого отдельного термоножа ... вводится дополнительное условие заполненности приемного бункера для предотвращения запайки пустых пакетов.

#### 摘录 D

- 出处：第 3 页，故障处理，`paper_content.txt` 第 173-185 行
> В программе предусмотрены аварийные ситуации в приемном бункере (выход из строя вибролотка и заклинивание задвижки), в системе термоножей и зоне контроля качества (выход из строя исполнительных механизмов).
>
> В случае возникновения аварийной ситуации все рабочие процессы останавливаются, и система переходит в режим ожидания. При нажатии оператором соответствующей кнопки осуществляется сброс аварии, после чего упаковочный станок возобновляет работу.

### 2. 基于原文整理后的自然语言描述

The paper describes the packaging machine controller as a hierarchical PLC program in which a main supervisory routine invokes subprograms for device polling, thermoknife motion, quality control, and temperature recording. After the operator presses `Start`, the screw feeder begins supplying product, the vibrating tray meters a single portion into the receiving hopper, and the tray stops once the required amount has accumulated. The hopper shutter then opens so the product drops into the open bag, while the vertical and horizontal thermoknives execute the ordered sealing, pulling, and cutting sequence that forms and closes the package. Finished packages are conveyed to the quality-control zone, where package presence is checked and the weight is compared against the target so that an out-of-spec package is ejected by the pneumatic pusher. If failures such as a broken vibrating tray, jammed shutter, actuator failure, or device-communication loss occur, all running processes stop, the machine enters a waiting state, and production resumes only after the operator issues the fault-reset command.

### 3. 逐句溯源

1. 句子 1：The paper describes the packaging machine controller as a hierarchical PLC program in which a main supervisory routine invokes subprograms for device polling, thermoknife motion, quality control, and temperature recording.
   对应摘录：C
2. 句子 2：After the operator presses `Start`, the screw feeder begins supplying product, the vibrating tray meters a single portion into the receiving hopper, and the tray stops once the required amount has accumulated.
   对应摘录：B
3. 句子 3：The hopper shutter then opens so the product drops into the open bag, while the vertical and horizontal thermoknives execute the ordered sealing, pulling, and cutting sequence that forms and closes the package.
   对应摘录：A, B, C
4. 句子 4：Finished packages are conveyed to the quality-control zone, where package presence is checked and the weight is compared against the target so that an out-of-spec package is ejected by the pneumatic pusher.
   对应摘录：A
5. 句子 5：If failures such as a broken vibrating tray, jammed shutter, actuator failure, or device-communication loss occur, all running processes stop, the machine enters a waiting state, and production resumes only after the operator issues the fault-reset command.
   对应摘录：D
