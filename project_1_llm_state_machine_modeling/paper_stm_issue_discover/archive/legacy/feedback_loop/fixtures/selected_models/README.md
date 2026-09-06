# Discover 选择模型夹具

这些 `STM_0.fcstm` 是 Discover 确定性工具测试使用的只读模型夹具。测试运行时只读取本目录，不导入旧 `agent_loop` 的模块、fixture loader 或业务代码。

文件来源与当前副本哈希如下：

| pair | 来源说明 | 副本 SHA-256 |
| --- | --- | --- |
| `0000` | 旧 Discover 集成夹具中的 FCSTM 副本 | `be3cc1fe3bb810e9e909c4ccedb35156e2a363d7e7001b7687891839118b59a4` |
| `0006` | 旧 Discover 集成夹具中的 FCSTM 副本 | `eb7348a871957eb111a2719c27821b5e19076324806ff4797222430f6b011cb3` |
| `0029` | representation reports 中的正式 FCSTM 副本 | `3a3b9a73271981ac6affe133fe4e6cfa4c30a9b66f0d8903596688dc630df166` |
| `0050` | representation reports 中的正式 FCSTM 副本 | `e1ff73267c5acdc5aa29721d4ad1c0e13a3ca756cbbc5b5af819627bf3fc3767` |

来源路径只作为历史 provenance，不是运行时依赖。更新夹具时必须同步更新哈希和测试记录，不能在测试中回到来源目录动态读取。
