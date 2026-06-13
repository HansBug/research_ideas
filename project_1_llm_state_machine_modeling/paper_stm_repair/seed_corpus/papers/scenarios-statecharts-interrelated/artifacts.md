# artifacts: scenarios-statecharts-interrelated

## 本地文件核验

| Artifact | 状态 | SHA256 | 说明 |
|---|---|---|---|
| `bibtex.bib` | present | `b1fbe997e07c624e87f2abc4bffefb38e085e21290fa04801ae544d56001a12d` | 含官方/机构 PDF URL；未提供 DOI。 |
| `paper_content.txt` | present | `f05d2860e40acb832b6d3cfbcae57ce803106badfd7ff64600e24e9f359496c4` | 448 lines；全文文本足以支持 P1/P2/P3/P4 判定，存在少量 PDF 抽取乱码。 |
| `paper.pdf` | present | `5bec09030159dedfe68424baa1dc24b3422c10b93d8a081f46d0e8163166c5bf` | 本地 PDF 已复制；本轮未因证据不足打开 PDF。 |

## 外部 artifact / license / URL 稳定性

| 项 | 判定 | 证据与风险 |
|---|---|---|
| Paper URL | found | BibTeX URL: <https://www.iplab.cs.tsukuba.ac.jp/paper/international/simona-isfst2001.pdf>。机构实验室 PDF 链接，稳定性中等；非 DOI、非 publisher landing page、非归档 artifact。 |
| Code / tool | not found | 论文 Page 6 lines 379-381 说集成规则的 system 仍处于 early phases of development；Page 6 lines 399-401 将 automatic generation/testing system 作为 future work。 |
| Dataset / examples | paper-only | 论文只有 ATM event trace diagrams 与 statechart 图示；未给出机器可读 scenario/statechart 文件或 benchmark。 |
| Supplementary bundle | not found | 全文、BibTeX、源 DESC 均未出现 supplementary / repository / dataset bundle。 |
| License / redistribution | unknown | PDF 页面与论文文本未声明开源或再分发 license；只能记录本地研究副本，不应视作可再发布数据集。 |

## R2 转换可用性

| 维度 | 判定 |
|---|---|
| 机器可读输入 | no |
| 机器可读输出 STM | no |
| 可直接 replay | no |
| 可人工重建 | limited |
| R2 eligibility | not eligible without manual derivation |

R2 只能把本文作为背景论文或人工重建示例来源。若后续强行使用，需要新建人工派生记录，明确说明输入来自论文 Fig.1/Fig.3/Fig.8，输出来自 Fig.2/Fig.4/Fig.5/Fig.6/Fig.7/Fig.9，且不得把人工重建样例冒充作者发布 artifact。
