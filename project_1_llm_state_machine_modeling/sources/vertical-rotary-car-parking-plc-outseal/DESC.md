# 立体旋转车位选择与取车控制 / Pengendalian Sistem Parkir Mobil Putar Vertikal Otomatis Menggunakan PLC Outseal dan HMI Android

## 论文在讲什么

这篇论文讨论的是一个立体旋转式停车系统原型。作者用 PLC Outseal、Android HMI、Bluetooth 通信、进出口栏杆、proximity/infrared 传感器和旋转电机，实现了一个带 `8` 个车位的垂直 rotary parking system，让操作员可以为进车指定车位，也可以按编号把车旋转到取车位并完成放行。

它的重点不是停车轨迹规划，而是停车设施自身的离散控制。论文从系统结构、HMI 页面、车位号选择、进车检测、旋转对位、取车确认、应急界面、计数器复位一路写下来，控制对象边界非常清晰，因此比只写车位检测或门禁模块的停车论文更接近我们要的系统级控制样本。

## 控制系统在文中的位置

控制系统是这篇论文的核心内容。作者在实现部分直接按“系统启动”“车辆进入”“车辆准备停车”“HMI 选位”“旋转停车”“取车校验”“应急操作”来说明系统工作方式，后面还用 HMI screen table 和 data table 把每个页面、按钮、slot 编号、indicator 和 motor 旋转结果列得很细。

这意味着我们关心的控制链不是附属说明，而是论文主体。尤其是 `Parkir Mobil`、`Ambil Mobil`、`BENAR/SALAH`、`DARURAT ON/OFF`、`Reset Jumlah`、`Reset Counter` 这些界面动作，都不是 UI 花哨细节，而是和旋转停车设备行为直接耦合的控制命令。

## 对我们为什么有用

这篇论文对 `🅿️` 方向的价值在于，它补的是“旋转立体车位 + HMI 选位/取车校验”这类和传统地面停车场完全不同的控制对象。当前停车类样本里虽然已经有门禁、空位提示、代客泊车或自动泊车高层流程，但这种 vertical rotary parking 的编号对位和取车确认链仍然比较少。

另外，它还是一个很好的系统级 `EFSM + T0` 样本。这里的关键不是秒级 timer，而是状态分支和变量信息，如车位编号、车位占用数、红绿黄指示、`CW/CCW` 旋转方向、停车/取车确认和应急人工操作，这对训练模型理解“带编号和操作输入的停车设备控制器”很有帮助。

## 如果需要人工细读，建议怎么读

人工回读时，建议先看第 `3-5` 页的实现部分，把 `sensor proximity`、`sensor infrared 1/2`、barrier gate、rotary motor、Android HMI 之间的关系读顺。然后直接读 `Parkir Mobil` 和 `Ambil Mobil` 的叙述段，这两段基本就覆盖了停车与取车的主控制链。

第二轮再看 HMI 页面说明和 `Data Mobil Parkir` 表，把每个 screen、button、slot 编号、校验按钮和 emergency/reset 功能与主链对上。关于 Bluetooth 距离实验的段落可以后看，它更像部署约束，不是系统状态机骨架本身。
