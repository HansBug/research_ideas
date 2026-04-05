# FINITE STATE MACHINE UNTUK PENGENDALI ELEVATOR BERBASIS FIELD PROGRAMMABLE GATE ARRAY - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把 FPGA 电梯控制器写成六状态 Moore FSM，并逐段解释了 `at_fl / start / keep_going` 对各状态跳转的约束，原文细节足够支撑双 A。

## 条目 1: Six-State Moore Elevator Motion Controller
- 控制对象：基于 FPGA 的电梯运动状态控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是楼宇机电与电梯控制领域的 FPGA 电梯控制器，用六个 Moore 状态组织轿厢上下行、等待和停车逻辑，并依赖 `at_fl`、`start`、`keep_going` 完成状态跳转。
- 判断：算。对象是实际电梯运动控制器，原文明确给出状态集合、输入信号、输出信号和关键跳转条件，不是一般性的 FPGA 教学背景。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`HASIL PENELITIAN DAN PEMBAHASAN`，`paper_content.txt` 第 133-162 行
> Prinsip kerja sistem pengendali elevator menggunakan model finite state machine Moore untuk rangkaian logika sekuensial.
>
> ... sinyal keep_going, start, at_flr merupakan sinyal masukan untuk melakukan kegiatan yang digunakan oleh elevator; sinyal flr merupakan sinyal keluaran untuk menunjukkan keberadaan kotak elevator pada suatu lantai tertentu; sinyal brake, dn, up merupakan sinyal keluaran untuk menunjukkan kondisi elevator ...
>
> pr_sreg, next_sreg menggunakan jenis data sreg yang mempunyai state : dn_slow, stop_dn, done, stop_up, wait, dan up_slow; state done dan wait merupakan state yang mempunyai keadaan transisi elevator untuk menunggu adanya sinyal penekanan tombol.

#### 摘录 B
- 出处：第 2-3 页，`HASIL PENELITIAN DAN PEMBAHASAN`，`paper_content.txt` 第 176-214 行
> State awal adalah keadaan dn_slow yang mempunyai syarat untuk melanjutkan ke keadaan berikutnya, yaitu state stop_dn, maka harus memasukkan kondisi at_flr berlogika high. Jika tidak didapatkan logika high pada kondisi at_flr maka state tersebut tidak akan melanjutkan ke state berikutnya.
>
> State stop_dn merupakan state yang mempunyai tugas untuk menunggu masukan start untuk berlogika high. Jika sinyal logika high pada state stop_dn telah terpenuhi maka akan menunggu sinyal masukan logika high dari keep_going. Jika telah terpenuhi logika high pada keep_going, maka state akan berpindah ke keadaan dn_slow, namun jika mendapatkan sinyal masukan low pada keep_going maka state akan berpindah ke state stop_up.
>
> State stop_up ... menunggu sinyal masukan yang berlogika high pada start ... kemudian menunggu keep_going ... menuju ke state berikutnya, yaitu state up_slow. State up_slow ... menunggu sinyal masukan berlogika high pada at_flr. Jika telah terpenuhi sinyal masukan berlogika high pada at_flr, maka state akan berpindah ke state berikutnya, yaitu state stop_up.

### 2. 基于原文整理后的自然语言描述

The elevator controller is implemented as a six-state Moore FSM with states `dn_slow`, `stop_dn`, `done`, `stop_up`, `wait`, and `up_slow`, and it is designed to run on a Xilinx Spartan-3E FPGA. Its key inputs are `start`, `keep_going`, and `at_flr`, while its outputs report floor position and motion conditions through signals such as `flr`, `brake`, `dn`, and `up`. The initial state is `dn_slow`, and the machine does not leave that state until `at_flr` becomes high, indicating that the target-floor condition has been satisfied and the controller may enter `stop_dn`. In `stop_dn`, the controller first waits for `start=1` and then branches on `keep_going`: a high value sends the FSM back to `dn_slow`, while a low value redirects it to `stop_up`. The upward branch mirrors this structure, because `stop_up` waits for `start` and `keep_going` before entering `up_slow`, and `up_slow` remains active until `at_flr=1`, at which point the FSM returns to `stop_up`; meanwhile, `done` and `wait` are documented as button-waiting transition states.

### 3. 逐句溯源

1. 句子 1：The elevator controller is implemented as a six-state Moore FSM with states `dn_slow`, `stop_dn`, `done`, `stop_up`, `wait`, and `up_slow`, and it is designed to run on a Xilinx Spartan-3E FPGA.
   对应摘录：A
2. 句子 2：Its key inputs are `start`, `keep_going`, and `at_flr`, while its outputs report floor position and motion conditions through signals such as `flr`, `brake`, `dn`, and `up`.
   对应摘录：A
3. 句子 3：The initial state is `dn_slow`, and the machine does not leave that state until `at_flr` becomes high, indicating that the target-floor condition has been satisfied and the controller may enter `stop_dn`.
   对应摘录：B
4. 句子 4：In `stop_dn`, the controller first waits for `start=1` and then branches on `keep_going`: a high value sends the FSM back to `dn_slow`, while a low value redirects it to `stop_up`.
   对应摘录：B
5. 句子 5：The upward branch mirrors this structure, because `stop_up` waits for `start` and `keep_going` before entering `up_slow`, and `up_slow` remains active until `at_flr=1`, at which point the FSM returns to `stop_up`; meanwhile, `done` and `wait` are documented as button-waiting transition states.
   对应摘录：A, B
