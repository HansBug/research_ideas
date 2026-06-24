# 合成点餐菜单 PlantUML 样例

## 1. 来源

- 原始条目：[unified-uml-multimodal-validation](../../corpora/seed_library/unified-uml-multimodal-validation/)
- 论文 PDF：[paper.pdf](../../corpora/seed_library/unified-uml-multimodal-validation/paper.pdf)
- 论文全文提取：[paper_content.txt](../../corpora/seed_library/unified-uml-multimodal-validation/paper_content.txt)
- BibTeX：[bibtex.bib](../../corpora/seed_library/unified-uml-multimodal-validation/bibtex.bib)
- 单篇说明：[seed_desc.md](../../corpora/seed_library/unified-uml-multimodal-validation/seed_desc.md)
- 一手资产说明：[assets/README.md](../../corpora/seed_library/unified-uml-multimodal-validation/assets/README.md)
- 资源 registry：[seed_resource_registry.json](../../corpora/seed_library/unified-uml-multimodal-validation/seed_resource_registry.json)
- 原始 pair：`unified_uml_state_train_0000`

## 2. 文件

| 文件 | 说明 |
|---|---|
| [nl.txt](./nl.txt) | Hugging Face parquet 第 0 行 `input` 字段中的 synthetic feature description。 |
| [stm0.puml](./stm0.puml) | 同一行 `uml_code` 字段中的 PlantUML state diagram。 |
| [source_meta.json](./source_meta.json) | 从 `pairs.jsonl` 抽出的 pair id、parquet locator、哈希、生成方式与 trace 字段。 |

## 3. 系统说明

该样例描述一个餐厅或在线点餐软件中的“统一菜单”功能。用户希望把汉堡、配菜、沙拉和饮料集中在一个菜单里选择，查看价格，并一次性完成支付。生成出的 `STM_0` 是简单 PlantUML 状态图，覆盖创建菜单、添加条目、查看菜单、编辑菜单和支付。

## 4. NL 中文完整翻译

想象你在一家餐厅，正在尝试点餐。你想点一个汉堡，同时还想点一份配菜、一份沙拉和一杯饮料。你希望分别为所有内容付款，但又不想为了点每一项而在多个菜单或标签页之间来回导航。你希望能够一次性点完所有内容，这样就能在一个地方看到所有选项及其价格。

为了实现这一点，我希望软件允许我为所有想点的项目创建一个单一“菜单”，然后我可以逐项选择每个项目。软件还应该允许我查看菜单以及每个项目的价格，并且能够一步完成全部付款。当我修改菜单项目时，菜单也应该能够自动更新。

这个功能对于喜欢外出就餐的人，或者不方便在多个菜单或标签页之间导航的人特别有用。对于想在线点餐或通过移动应用点餐的人也会很有用。

## 5. STM 文件说明

- 格式：PlantUML，文件为 [stm0.puml](./stm0.puml)。
- 谱系：UML state diagram / PlantUML statechart。
- 时间特性：未见显式时钟，按 T0 离散状态图处理。
- 重要 caveat：这是 synthetic / non-control-domain 样例，只能用于批量读取、格式转换和简单结构诊断，不得在论文中包装成真实控制系统需求。
