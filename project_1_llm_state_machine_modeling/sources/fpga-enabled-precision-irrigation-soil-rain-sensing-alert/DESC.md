# 土壤-雨量感知 FPGA 精准灌溉 / Revolutionary FPGA-Enabled Precision Irrigation Framework with Integrated Soil-Rain Sensing and Real-Time Alert Mechanisms

## 论文在讲什么

这篇论文设计了一套 FPGA 精准灌溉控制系统，目标是在雨天、土壤湿润和土壤干燥等环境条件变化下自动决定是否启动水泵。系统由雨量传感器、土壤湿度传感器、FPGA、继电器、水泵、七段显示和蜂鸣器组成。

论文的控制核心是二值传感器组合逻辑：雨量或湿度为 high 表示检测到雨或湿土；只有在土壤干燥且没有雨时，FPGA 才允许水泵动作。雨天时系统停灌，并通过蜂鸣器和 `r-on` 显示提醒用户；非雨状态则显示 `rOFF`。正文还给出继电器 2 秒动作、1000 ms 去抖和蜂鸣器 1 kHz 输出等局部定时。

## 控制系统在文中的位置

灌溉控制器是论文的主体，不是传感器背景的附属例子。`System Architecture`、`Flow Chart`、`Working Principle`、`Control Logic` 和 `RTL Implementation` 逐步说明从传感器输入到水泵、显示和蜂鸣器输出的完整链条。

这篇文献没有画出传统 FSM 状态图，但它的输入组合、guard 和输出动作足够明确，适合按 EFSM 口径整理。对本论文集来说，它比早期只有一两句阈值控制的灌溉短文更有价值，因为这里能同时保住雨天停灌、干土开泵、告警显示、继电器定时和测试场景。

## 对我们为什么有用

它补充了 `🌡️` 过程与环境控制方向里较完整的 `sensor-guarded actuator` 样本。后续可以把自然语言需求写成“读取 `rain_in` 和 `soil_in`，根据组合进入雨天告警、干土灌溉或正常监测分支，并驱动 `relay_out`、`buzzer` 与七段显示”。

另一个价值是它把离散控制和局部时间语义结合得比较清楚。`2 s` 继电器动作、`1000 ms` 去抖、`1 kHz` 蜂鸣器和 `sub-1 ms` 响应都能帮助构造 `T1` 样本，避免过程控制样本全部退化成无时间语义的阈值 if-else。

## 如果需要人工细读，建议怎么读

建议先看第 1 页摘要，确认雨量、湿度、水泵、显示和蜂鸣器的整体关系。然后读第 5 页 `Flow Chart`、`Working Principle` 和 `Control Logic`，把“雨天停灌告警”和“干土无雨开泵”两个主要分支抽出来。

第二轮重点读 `RTL Implementation` 与测试章节，核对 `clk/reset/soil_in/rain_in`、`relay_out/buzzer/an/cath`、`alarm_trigger/pump_on`、继电器去抖和 2 秒动作参数。文献综述和未来工作可后看；如果要重做 `STM.md`，应优先从这些 RTL 与测试段落恢复 guard、动作和定时。
