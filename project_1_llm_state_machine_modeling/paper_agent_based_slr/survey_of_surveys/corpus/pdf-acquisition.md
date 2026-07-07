# A2a PDF 获取记录

## 1. 策略

A2a 只使用合法开放来源：原始表中的开放 PDF 链接、OpenAlex 开放获取链接、DOI / 出版商公开 PDF、arXiv、作者主页、大学主页和项目主页。不绕过付费墙，不使用非法下载源，不把 HTML / 登录页 / 错误页伪装为 PDF。

## 2. 当前状态

| 层级 | downloaded | manual_needed | not_applicable | 说明 |
|---|---:|---:|---:|---|
| 主候选 | 63 | 57 | 0 | 13 篇来自 A1；2 篇由 A2a 自动从开放 PDF 链接获取；48 篇由用户本地 Zotero 导出显式复制入仓库。 |
| 替补 / 留出 | 6 | 34 | 0 | 6 篇由用户本地 Zotero 导出显式复制入仓库；其余仍需人工下载或后续合法开放链接补抓。 |
| 边界池 | 0 | 0 | 145 | A2a 不强制获取边界池 PDF。 |

完整表见 [tables/pdf-status.csv](./tables/pdf-status.csv)。需人工下载清单见 [manual-download-needed.md](./manual-download-needed.md) 与 [manual-download-needed.bib](./manual-download-needed.bib)。

## 3. 自动获取脚本

脚本入口：[../scripts/acquire_pdfs.py](../scripts/acquire_pdfs.py) 与 [../scripts/import_zotero_export_pdfs.py](../scripts/import_zotero_export_pdfs.py)。自动开放获取脚本只做两类动作：

1. 如果 `papers/<slug>/paper.pdf` 与 `paper_content.txt` 已经存在，则保留并按仓库内文件重新计算状态，不覆盖 A1 / A2a 已落盘资产。
2. 如果原始候选有 OpenAlex 开放 PDF 链接，则尝试直接下载，并检查文件头是否为 PDF。

前序 `fulltext-audit.csv` 中的 `/tmp/...` 本地临时路径只保留为审计线索，不再被自动复制，也不能让条目在干净 clone 下被计为 `downloaded`。若用户通过 Zotero / 图书馆 / 浏览器合法补齐 PDF，必须使用显式导入脚本或等价人工步骤复制到对应 `papers/<slug>/paper.pdf`，再生成 `paper_content.txt`；只有仓库内真实存在且可提取文本的 `paper.pdf` 才能进入已下载统计。

下载成功后，脚本使用仓库工具生成 `paper_content.txt`：

```bash
python -m tools.pdf_extractor -i papers/<slug>/paper.pdf -o papers/<slug>/paper_content.txt -m text
```

A2a 不批量生成正式 `review.md`。新增候选目录中的 `metadata.json` 只标记 `a2a_review_status = not_started`。本轮 Zotero 导入审计见 [raw/zotero-import-2026-07-07.csv](./raw/zotero-import-2026-07-07.csv)；失败 / 错配附件见 [raw/zotero-import-failed-2026-07-07.csv](./raw/zotero-import-failed-2026-07-07.csv)。

## 4. 失败分类

| 失败类型 | 含义 | 后续动作 |
|---|---|---|
| `paywall` | 未发现合法公开 PDF 或出版商限制访问 | 进入人工 Zotero 下载。 |
| `login_wall` | 需要登录或机构访问 | 进入人工 Zotero 下载。 |
| `captcha_or_waf` | WAF / CAPTCHA 阻断 | 等待人工浏览器核验。 |
| `not_found` | 链接失效或 404 | 记录并寻找作者主页 / arXiv。 |
| `html_only` | 下载结果不是 PDF | 不入库，继续人工核验。 |
| `broken_pdf` | 公开链接返回错误页、文件头不是 PDF、PDF 损坏，或 Zotero 附件无法用仓库工具提取正文 | 重新进入人工下载。 |
| `local_snapshot_only` | 旧审计中有本地临时路径或旧哈希，但仓库内没有真实 PDF；该路径只作线索 | 进入人工下载或后续用公开链接重新获取。 |
| `metadata_missing` | DOI / URL 不足以定位 PDF | 后续补元数据。 |

## 5. 当前结论

A2a 已经完成“对 core + reserve 全部记录获取状态”的门禁，并通过本轮 Zotero 导入把可深读全文从 15 篇提升到 69 篇；但 PDF 实际可得性仍是 A2b 的主要执行风险。A2b 启动前应继续处理剩余 P0 / P1 人工下载条目；不得因为 PDF 暂不可得而把条目从主候选中删除。
