# 2014 版政策 PDF 来源

> 信息更新时间：`2026-06-16 17:20:00`（Asia/Shanghai）

本目录保存 2014 版《北京航空航天大学关于申请博士学位发表论文的规定》的 PDF 形态证据。

| 文件 | 性质 | SHA256 | 用途 |
|---|---|---|---|
| [2014-buaa-phd-publication-requirements-official-attachment.pdf](./2014-buaa-phd-publication-requirements-official-attachment.pdf) | 官方附件 PDF | `8eef9889dc2cca6b7c8b61cfd12914e6dfc9ec0aa6dc1e7616987134350737de` | 当前主依据；从自动化学院官方通知附件经验证码下载，7 页 |
| [2014-policy-photo-bundle-nonofficial.pdf](./2014-policy-photo-bundle-nonofficial.pdf) | 照片合订 PDF（非官方） | `c091fa9d1f582f56eb41de78233d7ab3afe3874fa17f04cccc2b8f39551c6848` | 由 [../source_images/](../source_images/) 12 张照片合成，方便翻阅，不替代官方 PDF |

## 提取命令

官方附件 PDF 文本使用仓库 `venv` 与 [../../../tools/pdf_extractor.py](../../../tools/pdf_extractor.py) 提取：

```bash
source venv/bin/activate
python -m tools.pdf_extractor \
  -i degree_requirements/2014_policy/source_pdfs/2014-buaa-phd-publication-requirements-official-attachment.pdf \
  -o degree_requirements/2014_policy/extracted_text/2014-buaa-phd-publication-requirements-official-attachment.txt \
  -m text
```

维护要求：如果后续取得研究生院官方 `.docx` 或另一个 PDF 原件，应新增加入本目录或新增 `source_docs/`，不得覆盖现有 PDF；同时更新 [../README.md](../README.md)、[../extracted_text/README.md](../extracted_text/README.md) 与根目录 [../../SUMMARY.md](../../SUMMARY.md)。

## 更新日志

| 时间 | 修改 | 说明 |
|---|---|---|
| 2026-06-16 17:20:00 | 新增 PDF 来源说明 | 区分官方附件 PDF 与非官方照片合订 PDF，并记录提取命令 |
