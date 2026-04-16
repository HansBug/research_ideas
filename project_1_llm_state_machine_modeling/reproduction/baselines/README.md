# Baselines

本目录存放各 baseline 的复现实现。

## 当前文件

- [baseline_llms_emp.py](./baseline_llms_emp.py)
- [baseline_ttool.py](./baseline_ttool.py)
- [baseline_nimbus.py](./baseline_nimbus.py)
- [baseline_structure_event.py](./baseline_structure_event.py)

## 角色

这些文件负责：

1. 读取对应 baseline 的输入数据
2. 调用统一的 LLM client 或辅助模块
3. 生成规范化输出
4. 把结果写入 [`../results/`](../results/)

## 导航

如果你想了解这些 baseline 在整个工作区里的位置，先读：

1. [../README.md](../README.md)
2. [../GUIDE.md](../GUIDE.md)
3. [GUIDE.md](./GUIDE.md)
