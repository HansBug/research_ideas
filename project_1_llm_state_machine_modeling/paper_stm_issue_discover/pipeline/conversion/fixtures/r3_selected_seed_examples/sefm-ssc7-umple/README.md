# 自助结账系统 Umple 样例

## 1. 来源

- 原始条目：[sefm-llm-state-machine](../../../../../corpora/seed_library/sefm-llm-state-machine)
- 论文 PDF：[paper.pdf](../../../../../corpora/seed_library/sefm-llm-state-machine/paper.pdf)
- 论文全文提取：[paper_content.txt](../../../../../corpora/seed_library/sefm-llm-state-machine/paper_content.txt)
- BibTeX：[bibtex.bib](../../../../../corpora/seed_library/sefm-llm-state-machine/bibtex.bib)
- 单篇说明：[seed_desc.md](../../../../../corpora/seed_library/sefm-llm-state-machine/seed_desc.md)
- 一手资产说明：[assets/README.md](../../../../../corpora/seed_library/sefm-llm-state-machine/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../../../../corpora/seed_library/sefm-llm-state-machine/seed_resource_registry.json)
- 原始 pair：`sefm_ssc7_single_prompt_claude_sonnet35_0001`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | 4open ZIP 中 `SSC7_fall_2024` 的自助结账系统自然语言描述。 |
| [stm0.ump](./stm0.ump) | Claude Sonnet 3.5 single-prompt 生成的 Umple 状态机文本。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、ZIP locator、哈希、生成方式与 trace 字段。 |
| [model.fcstm](./model.fcstm) | R4.5 表示桥导出的 pyfcstm smoke 快照；同步自 [pipeline/representation/reports/fcstm_exports/sefm-ssc7-umple/model.fcstm](../../../../representation/reports/fcstm_exports/sefm-ssc7-umple/model.fcstm)，不是一手资源或 repair 后模型。 |
| [fcstm_meta.json](./fcstm_meta.json) | `model.fcstm` 的同步来源、hash、parse/inspect 状态、上游 NL / 原始 STM_0 / canonical / loss 归因记录。 |

## 3. 系统说明

该样例描述超市自助结账机 SSC7。顾客可以扫描条码、输入无条码商品的四位产品码、称重商品或自带购物袋、发起支付、取消当前操作或请求工作人员 override。系统与条码扫描器、触摸屏、两个秤、支付终端、打印机和工作人员提示灯交互。生成出的 `STM_0` 是 Umple 状态机，包含 `Ready`、`WeighingItem`、`WeighingBag`、`SecurityCheck`、`Payment`、`Override`、`Timeout` 等状态。

## 4. NL 中文完整翻译

自助结账机 SSC7 由超市使用，使顾客能够扫描购买的商品并付款，通常不需要超市工作人员帮助。

如右侧图所示，SSC7 包含以下部分：（i）左侧用于放置尚未扫描商品的区域，（ii）条码扫描器，（iii）触摸屏，（iv）触摸屏前方用于给商品称重的秤，（v）右侧带集成安全秤的区域，用于放置已经扫描的商品，（vi）用于信用卡付款的支付终端，（vii）打印账单的打印机，以及（viii）用于提示工作人员需要前来处理的指示灯。

SSC7 软件（SSC7S）与第（ii）到第（viii）部分交互。条码扫描器向 SSC7S 提供扫描到的编号。SSC7S 使用触摸屏向顾客显示所有信息，顾客通过按按钮并输入无条码商品的四位产品码向 SSC7S 提供信息。触摸屏前方的秤和安全秤都会向 SSC7S 提供重量。SSC7S 向支付终端发送付款请求，支付终端会返回带授权码的成功消息、因为付款失败而产生的失败消息，或者因为顾客取消交易而产生的取消消息。此外，SSC7S 会把账单发送到打印机，并控制工作人员指示灯的开关。

顾客可以扫描商品条码，也可以为无条码商品输入四位产品码。如果条码或产品码在系统中不存在，则向顾客显示错误消息。当扫描到正确条码时，商品显示在触摸屏上。当输入正确产品码时，需要先称重该商品，之后在触摸屏上显示商品及其重量。在这两种情况下，也就是有条码商品和无条码商品，商品随后都必须放到右侧区域进行安全重量检查。如果重量与期望重量匹配，则系统准备处理下一件商品。如果不匹配，则必须呼叫工作人员执行 override，以便从账单中清除该商品。当可以扫描商品且账单中至少有一件商品时，顾客也可以表示想从账单中移除某件商品，这同样需要呼叫工作人员执行 override 来清除该商品。

顾客也可以表示自己带了购物袋。每个购物袋都必须用安全秤称重。只要当前也允许扫描商品，就可以进行这一操作。购物袋称重后，触摸屏上显示购物袋数量，系统准备处理下一件商品。

顾客通过按触摸屏上的 Pay 按钮开始付款流程。如果账单中至少有一件商品，系统会向支付终端发送付款请求并等待付款结果。如果付款成功，系统打印账单并准备服务下一位顾客。如果付款不成功，系统准备处理下一件商品；如果付款失败，则显示错误消息。

顾客可以取消商品或购物袋的称重，此时系统准备处理下一件商品。当可以扫描商品，或顾客需要把商品（不是购物袋）放到右侧区域进行安全重量检查时，顾客也可以请求取消全部内容并重新开始，这需要呼叫工作人员执行 override 以清除所有内容。

当需要 override 时，系统打开指示灯并等待工作人员输入 override 代码。如果代码错误，则显示错误消息。否则，指示灯关闭，并清除该商品或清除全部内容。

当系统空闲一段时间后，SSC7S 会收到超时警告信号。只有在尚未呼叫工作人员执行 override 且付款流程尚未开始时，才会发生这种情况。超时警告信号会在触摸屏上启动 60 秒倒计时。如果顾客按 Continue 按钮，则从离开的位置继续。如果倒计时到 0，系统清除全部内容并准备服务下一位顾客。

## 5. STM 文件说明

- 格式：Umple，文件为 [stm0.ump](./stm0.ump)。
- 谱系：UML statechart / HSM-capable 的 textual state machine。
- 时间特性：整体按 T0 离散状态机处理，但生成文本含 `after(60)` 这类 timer-like transition，后续转换时必须显式标注或降级。
- 重要 caveat：该论文制品中当前只有 SSC7 有 generated output；另外 8 个 NL 不能当作 generated `<NL, STM_0>` pair 使用。


## 6. R4.5 FCSTM 派生快照

- 派生文件：[model.fcstm](./model.fcstm)。
- 元数据：[fcstm_meta.json](./fcstm_meta.json)。
- 上游 R4.5 输出：[pipeline representation model.fcstm](../../../../representation/reports/fcstm_exports/sefm-ssc7-umple/model.fcstm)、[name_mapping.json](../../../../representation/reports/fcstm_exports/sefm-ssc7-umple/name_mapping.json)、[lowering_inventory.json](../../../../representation/reports/fcstm_exports/sefm-ssc7-umple/lowering_inventory.json)、[parse_inspect_report.json](../../../../representation/reports/fcstm_exports/sefm-ssc7-umple/parse_inspect_report.json)。
- 当前状态：`fcstm_meta.json` 中 `parse_status=ok`、`inspect_status=ok`、`repair_contribution_allowed=false`。
- 口径说明：R4.5 从 Umple 官方 SCXML canonical 导出可被 pyfcstm parse/inspect 的 smoke `.fcstm`；event+guard 经 pseudo relay 降低，`after(60)` 等 timing loss 继续只作 caveat。
- 维护纪律：若 R3 canonical、R4.5 exporter 或 [../../pipeline/representation/reports/fcstm_export_report.json](../../../../representation/reports/fcstm_export_report.json) 变化，必须先重新生成 R4.5 reports，再运行 `python -m paper_stm_representation.cli sync-selected-fcstm` 同步本目录；不得手工只改本目录 [model.fcstm](./model.fcstm)。

### 6.1 哈希差异说明

[source_meta.json](./source_meta.json) 同时记录两组哈希：`source_stm0_sha256` 是 [pairs.jsonl](../../../../../corpora/seed_library/sefm-llm-state-machine/assets/extracted/pairs.jsonl) 中作者一手生成文本的原文哈希，`stm0_sha256` 是本目录 [stm0.ump](./stm0.ump) 当前文件的 UTF-8 字节哈希。二者不同的原因仅是空白规范化：从 `pairs.jsonl` 原文落盘为 `stm0.ump` 时，将若干只含缩进空格的空白行规范化为空行，并去掉文件末尾额外空行；状态、迁移、guard、action、事件名、`after(60)` 等语义字符未改动。后续若需要逐字节复核来源，应以 `source_stm0_sha256` 和原始 `pairs.jsonl` 为准；若需要复核本 smoke 输入文件，应以 `stm0_sha256` 为准。
