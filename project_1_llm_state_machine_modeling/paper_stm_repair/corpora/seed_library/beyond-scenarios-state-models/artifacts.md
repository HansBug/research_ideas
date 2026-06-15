# artifacts: beyond-scenarios-state-models

## 本地制品核验

| 项 | 状态 | 证据 / 哈希 |
|---|---|---|
| PDF | present | `paper.pdf` sha256 `03d784d8b9f8233e1c720f2478944d3ffb31d3d7903d1f655bf9caecbd54d586`；与源 baseline PDF 哈希一致。 |
| paper_content.txt | present / degraded | sha256 `069279b997ec140a7af017f573f51f3a10c1a64c1edd71a3cd72029470360ce0`；与源 baseline 文本一致，但含 NUL 字节且正文大面积乱码，不能作为主要全文证据。 |
| BibTeX | present | `bibtex.bib` sha256 `e7a53a88114e17194aebc7ad7b2257cdbdb123a609eff33d0715d4394a20c887`；与源 baseline BibTeX 一致。 |
| PDF metadata | checked | `pdfinfo`: 5 pages, not encrypted, PDF 1.2, Producer `GNU Ghostscript 6.51`, file size 175728 bytes。 |

## 外部 URL 与稳定性

| 项 | 结论 |
|---|---|
| paper_url | `https://www.site.uottawa.ca/~ssome/UCEdWeb/publis/ICSE02_Scenario_Workshop.pdf` |
| URL 类型 | 作者/学校页面托管 PDF，非 DOI / ACM DL canonical page。 |
| URL 稳定性 | medium-low：个人/课题组路径可读性风险高于 publisher DOI；当前本地 PDF 已冻结 sha256。 |
| DOI | 未在 BibTeX、PDF 正文或源 `DESC.md` 中发现。 |
| Publisher license | PDF p.1 底部为 ACM workshop copy notice；允许 personal/classroom copy，其他复制/发布需 permission/fee。 |
| Repository / code | 未发现公开仓库、源码包或 release URL。 |
| Dataset / benchmark | 未发现公开 benchmark；论文只给 Patient Monitoring System 的说明性 use case 示例。 |

## 论文内 artifact

| Artifact | 可用性 | 证据指针 |
|---|---|---|
| Login use case | paper-only | PDF p.2 Figure 1：结构化 use case，含 precondition、steps、exceptions、postcondition。 |
| Behavior sequence graph | paper-only | PDF p.2 Figure 2：User login 对应的 behavior sequence graph。 |
| Domain model | paper-only | PDF p.3 Figure 3：PM system partial domain model，含 operations/effects。 |
| DCG excerpt | paper-only | PDF p.3 Figure 4：conditions 的 partial DCG。 |
| Generated FSM | paper-only | PDF p.4 Figure 5：finite state transition machine generated from use case User login。 |
| UCEd tool | described-only | PDF p.5 Figure 7 截图；Section 4 称正在实现 UCEd，包含 Writing Tool、Domain Model Editor、Composition Module、Simulator，但没有下载/源码/版本包。 |

## R2 / 转换准备度

| 项 | 判断 |
|---|---|
| R2 可直接运行 | no |
| R2 可手工转录 | yes |
| 转换建议 | 仅在需要历史 seed 时，手工转录 Figure 1、Figure 3、Figure 5；输出标注 `manual_transcription_from_pdf`。 |
| 统计资格 | 不进入需要公开 artifact、license 明确、机器可读输入输出的主结果统计。 |
| blocker | 缺公开 UCEd 工具、缺机器可读 use case/domain model/FSM、缺 artifact license、`paper_content.txt` 不可读。 |

## 复核日志

| 日期 | 记录 |
|---|---|
| 2026-06-14 | 按 strict seed reader 边界核验 `bibtex.bib -> paper_content.txt -> paper.pdf -> DESC.md`；OCR 因缺 `tesseract` 未执行；结论为 `SS-B / SA-3 / R2 low`。 |
