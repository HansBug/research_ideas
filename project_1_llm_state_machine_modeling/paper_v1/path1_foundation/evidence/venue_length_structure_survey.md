# Path-1 CCF-B 期刊篇幅、结构与 LaTeX 模板摸排

更新时间：2026-06-10

本文档服务于 issue #67「Project 1 Path-1：2026 夏季 CCF-B 期刊投稿冲刺计划」。它同时记录三类信息：

1. 各候选期刊的官方篇幅 / 格式约束。
2. 已正式发表论文的真实页数和结构。
3. LaTeX 模板的官方入口、Overleaf 入口和可自动化下载方式。

本文档是初步摸排，不替代最终投稿前对投稿系统和 author guidelines 的浏览器复核。

## 1. 范围

issue #67 中与 2026 夏季首投直接相关的 CCF-B 期刊如下。

| 优先级 | 期刊 | 出版社 | 在 issue #67 中的角色 |
|---:|---|---|---|
| 1 | Software and Systems Modeling (SoSyM) | Springer | 主投路线 |
| 2 | Automated Software Engineering (ASEJ) | Springer | 若 automation / repair-loop 叙事更强，则作为强备投 |
| 3 | Requirements Engineering (REJ) | Springer | 若 requirements-to-model 叙事更强，则作为备投 |
| 4 | Empirical Software Engineering (EMSE / ESE) | Springer | 若转成 empirical / agentic SE 叙事，则作为后续备投 |
| 5 | Journal of Systems and Software (JSS) | Elsevier | 后续备投 |
| 6 | Information and Software Technology (IST) | Elsevier | 保守备投 |

## 2. 官方篇幅与格式约束

| 期刊 | 官方篇幅 / 格式信号 | 模板信号 | 对 Path-1 的实际含义 |
|---|---|---|---|
| SoSyM | 未看到固定页数上限；摘要 150-250 words；single-blind review。 | Springer Nature `sn-jnl`；SoSyM guideline 建议 LaTeX 使用 `[iicol]` 格式选项；Word 也接受。 | 篇幅主要由证据链质量和 reviewer 耐心约束，不是硬页数约束。 |
| ASEJ | 摘要 150-250 words；4-6 keywords；未看到硬页数上限。 | Springer Nature `sn-jnl` 是硬要求；guideline 写明 manuscript must be submitted in LaTeX and generated with `\documentclass{sn-jnl}`。 | 从一开始就用 `sn-jnl`，可以降低 SoSyM 与 ASEJ 之间的模板切换成本。 |
| REJ | 摘要 150-250 words；4-6 keywords；double-blind review，需要匿名主稿和单独 title page。 | LaTeX 可用 Springer Nature `sn-jnl`；Word 也接受。 | 如果保留 REJ 备投，主稿需要从早期就能生成匿名版本。 |
| EMSE | 摘要 150-250 words；structured abstract 可选；未看到硬页数上限。 | Word 是默认描述格式；有数学内容的稿件可用 Springer Nature `sn-jnl`。 | 模板不是主要问题，关键是 empirical protocol 是否足够强。 |
| JSS | Full Length Papers 通常应低于 36 页单栏或 18 页双栏；超出需要解释。 | JSS guide 指向 Elsevier LaTeX template package；当前下载目标是 `els-cas-templates.zip`；Elsevier general LaTeX instructions 也说明 `elsarticle`。 | 若转 JSS，应另建 Elsevier 版，按双栏 `<18` 页检查。 |
| IST | Research paper 上限 15,000 words；SLR / mapping 上限 20,000 words；short communication 上限 2,500 words；references、appendices 计入；每个 figure/table 按 200 words 计。 | IST guide 指向 Elsevier LaTeX template package；只有 LaTeX submission 才允许 double-column format。 | IST 是最硬的篇幅约束，15,000 counted words 是上限，不是目标。 |

## 3. LaTeX 模板获取方式

结论：六个期刊都有可用 LaTeX 模板。Springer 四刊共用 Springer Nature journal template；JSS / IST 走 Elsevier 模板体系。自动化获取优先使用 publisher ZIP / CTAN 镜像，Overleaf 主要作为人工建项目入口。

### 3.1 Springer 四刊：SoSyM / ASEJ / REJ / EMSE

| 项 | 信息 |
|---|---|
| 官方说明页 | https://www.springernature.com/gp/authors/campaigns/latex-author-support |
| 官方模板 ZIP | https://cms-resources.apps.public.k8s.springernature.io/springer-cms/rest/v1/content/18782940/data/v12 |
| Overleaf 人工入口 | https://www.overleaf.com/latex/templates/springer-nature-latex-template/myxmhdsbzkyd |
| 主 class | `sn-jnl.cls` |
| 示例主文件 | `sn-article-template/sn-article.tex` |
| 参考文献样式 | `sn-basic.bst`、`sn-mathphys-num.bst`、`sn-vancouver-num.bst` 等 |
| 本地验证状态 | 2026-06-10 已用 `curl` 验证可下载，ZIP 内含 `sn-jnl.cls`、示例 tex、bst、user manual。 |

可自动化获取命令：

```bash
mkdir -p templates/springer-sn-jnl
curl -L --fail --retry 2 -A 'Mozilla/5.0' \
  -o templates/springer-sn-jnl/springer-sn-jnl.zip \
  'https://cms-resources.apps.public.k8s.springernature.io/springer-cms/rest/v1/content/18782940/data/v12'
unzip -o templates/springer-sn-jnl/springer-sn-jnl.zip -d templates/springer-sn-jnl/
sha256sum templates/springer-sn-jnl/springer-sn-jnl.zip
find templates/springer-sn-jnl -maxdepth 3 -type f | sort
```

期刊特定使用建议：

| 期刊 | 推荐用法 |
|---|---|
| SoSyM | 以 `sn-jnl` 为主模板；最终投稿前按 SoSyM guideline 使用 `[iicol]` 选项复核版式。 |
| ASEJ | 必须使用 `sn-jnl`；不要用 Word-only、LNCS、ACM、IEEE 或 legacy Springer `svjour3`。 |
| REJ | 使用 `sn-jnl` 可以保留和 SoSyM/ASEJ 的兼容性；必须维护匿名版。 |
| EMSE | `sn-jnl` 可作为 LaTeX 工作模板；是否适配 EMSE 主要取决于 empirical study 质量。 |

### 3.2 Elsevier：JSS / IST 的 CAS 模板

| 项 | 信息 |
|---|---|
| Elsevier LaTeX instructions | https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions |
| JSS guide for authors | https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors |
| IST guide for authors | https://www.sciencedirect.com/journal/information-and-software-technology/publish/guide-for-authors |
| 官方 CAS ZIP | https://assets.ctfassets.net/o78em1y1w4i4/5uFmLZJTPDMAUjFnHRpjj8/6f19a979146eb93263763d87a894ab0d/els-cas-templates.zip |
| Overleaf CAS single-column | https://www.overleaf.com/latex/templates/elseviers-cas-latex-single-column-template/rsnbvrmnptyq |
| Overleaf CAS double-column | https://www.overleaf.com/latex/templates/elseviers-cas-latex-double-column-template/hhzpymgjmxfk |
| 主 class | `cas-sc.cls`、`cas-dc.cls` |
| 示例文件 | `cas-sc-template.tex`、`cas-dc-template.tex`、`cas-sc-sample.tex`、`cas-dc-sample.tex` |
| 本地验证状态 | 2026-06-10 已用 `curl` 验证可下载，ZIP 内含 `cas-sc.cls`、`cas-dc.cls`、sample tex、sample PDF、`cas-model2-names.bst`。 |

可自动化获取命令：

```bash
mkdir -p templates/elsevier-cas
curl -L --fail --retry 2 -A 'Mozilla/5.0' \
  -o templates/elsevier-cas/els-cas-templates.zip \
  'https://assets.ctfassets.net/o78em1y1w4i4/5uFmLZJTPDMAUjFnHRpjj8/6f19a979146eb93263763d87a894ab0d/els-cas-templates.zip'
unzip -o templates/elsevier-cas/els-cas-templates.zip -d templates/elsevier-cas/
sha256sum templates/elsevier-cas/els-cas-templates.zip
find templates/elsevier-cas -maxdepth 3 -type f | sort
```

JSS / IST 使用建议：

| 期刊 | 推荐用法 |
|---|---|
| JSS | 优先用 CAS；`cas-sc` 适合审稿阅读，`cas-dc` 用于检查 `<18` 双栏页预算。 |
| IST | 优先用 CAS；模板转换不是主要风险，主要风险是 15,000 counted words。 |

### 3.3 Elsevier `elsarticle` 备用模板

`elsarticle` 仍是 Elsevier LaTeX 生态中的常见模板。JSS / IST 当前 guide 更直接指向 CAS ZIP，因此 Path-1 若转 Elsevier，优先 CAS；`elsarticle` 作为备用。

| 项 | 信息 |
|---|---|
| CTAN 包页 | https://ctan.org/pkg/elsarticle |
| CTAN ZIP 镜像 | https://ctan.math.utah.edu/ctan/tex-archive/macros/latex/contrib/elsarticle.zip |
| Overleaf 人工入口 | https://www.overleaf.com/latex/templates/elsevier-article-elsarticle-template/vdzfjgjbckgz |
| 主 class | `elsarticle.cls` |
| 本地验证状态 | 2026-06-10 已用 `curl` 验证 CTAN Utah 镜像可下载，ZIP 内含模板 tex、bst 和文档 PDF。 |

可自动化获取命令：

```bash
mkdir -p templates/elsevier-elsarticle
curl -L --fail --retry 2 -A 'Mozilla/5.0' \
  -o templates/elsevier-elsarticle/elsarticle.zip \
  'https://ctan.math.utah.edu/ctan/tex-archive/macros/latex/contrib/elsarticle.zip'
unzip -o templates/elsevier-elsarticle/elsarticle.zip -d templates/elsevier-elsarticle/
sha256sum templates/elsevier-elsarticle/elsarticle.zip
find templates/elsevier-elsarticle -maxdepth 3 -type f | sort
```

### 3.4 一键下载三类模板

如果后续要在论文目录里一次性准备所有候选模板，可以直接运行：

```bash
mkdir -p templates/springer-sn-jnl templates/elsevier-cas templates/elsevier-elsarticle

curl -L --fail --retry 2 -A 'Mozilla/5.0' \
  -o templates/springer-sn-jnl/springer-sn-jnl.zip \
  'https://cms-resources.apps.public.k8s.springernature.io/springer-cms/rest/v1/content/18782940/data/v12'
curl -L --fail --retry 2 -A 'Mozilla/5.0' \
  -o templates/elsevier-cas/els-cas-templates.zip \
  'https://assets.ctfassets.net/o78em1y1w4i4/5uFmLZJTPDMAUjFnHRpjj8/6f19a979146eb93263763d87a894ab0d/els-cas-templates.zip'
curl -L --fail --retry 2 -A 'Mozilla/5.0' \
  -o templates/elsevier-elsarticle/elsarticle.zip \
  'https://ctan.math.utah.edu/ctan/tex-archive/macros/latex/contrib/elsarticle.zip'

sha256sum \
  templates/springer-sn-jnl/springer-sn-jnl.zip \
  templates/elsevier-cas/els-cas-templates.zip \
  templates/elsevier-elsarticle/elsarticle.zip \
  | tee templates/template-zip-sha256.txt

unzip -o templates/springer-sn-jnl/springer-sn-jnl.zip -d templates/springer-sn-jnl/
unzip -o templates/elsevier-cas/els-cas-templates.zip -d templates/elsevier-cas/
unzip -o templates/elsevier-elsarticle/elsarticle.zip -d templates/elsevier-elsarticle/
find templates -maxdepth 3 -type f | sort
```

说明：Overleaf 链接适合人工创建项目，不作为稳定自动化下载入口；自动化流程应优先使用上面的出版社 / CTAN ZIP。

## 4. 真实已发表论文样本

Springer PDF 通过官方 Springer `content/pdf/...pdf?download=true` 下载，并用 `pdfinfo` 统计页数。JSS PDF 通过机构仓储中的正式 Journal of Systems and Software 文章副本获取。ScienceDirect 对命令行 PDF 访问有 WAF/403 限制，因此 JSS/IST 的真实 PDF 证据比 Springer 四刊薄，投前仍需浏览器复核。

| 期刊 | 样本论文 | DOI / 正式出处 | PDF 页数 | 结构信号 |
|---|---|---|---:|---|
| SoSyM | Engineering a cognition-based specification method | `10.1007/s10270-026-01392-8`, SoSyM 2026 | 24 | Introduction；problem/contribution；method definition；related work；discussion；conclusion；appendix。 |
| SoSyM | Failure behavior modeling via atomic modeling concepts | `10.1007/s10270-026-01377-7`, SoSyM 2026 | 45 | Background；language/syntax/semantics；industrial evaluation；common modeling patterns；validity/discussion；appendix。 |
| SoSyM | Mu-FRET: a catalogue and tool for requirement refactoring | `10.1007/s10270-025-01355-5`, SoSyM 2026 | 33 | Formal requirements background；refactoring catalogue；tool；engine controller application；further evaluation；threats/discussion。 |
| ASEJ | Large language model based mutations in genetic improvement | `10.1007/s10515-024-00473-6`, ASEJ 2025 | 25 | Approach；明确 RQs；experimental setup；results；threats；related work；conclusion；data availability。 |
| ASEJ | Automated testing of prevalent 3D user interactions in virtual reality applications | `10.1007/s10515-026-00620-1`, ASEJ 2026 | 30 | Background；motivating example；empirical analysis；model abstraction；tool；evaluation；threats；conclusion；replication package。 |
| ASEJ | MoTDeReL: Model-based testing through deep reinforcement learning for software systems specified through graph transformation | `10.1007/s10515-026-00610-3`, ASEJ 2026 | 42 | Background；related work；method；evaluation；results；discussion；conclusion；data availability。 |
| REJ | From issue titles to requirements: an empirical study of large language models and prompt engineering strategies | `10.1007/s00766-026-00462-z`, REJ 2026 | 23 | Introduction；prompt setup/execution；evaluation prompt；data analysis；results；human validation；overall discussion；conclusion；supplement / replication package。 |
| REJ | A collaborative argumentation framework for goal-oriented reasoning | `10.1007/s00766-026-00461-0`, REJ 2026 | 24 | Introduction；framework；proof/event calculus；use case；discussion；conclusion；data availability。 |
| REJ | Ontology-based NLP tool for tracing software requirements and conceptual models: an empirical study | `10.1007/s00766-025-00447-4`, REJ 2025 | 29 | Introduction；traceability / NLP background；tool；empirical study；RQs；results；threats；discussion；conclusion。 |
| EMSE | From brittle to robust: Improving LLM annotations for SE optimization | `10.1007/s10664-026-10823-5`, EMSE 2026 | 29 | Literature review；methods；data；performance measures；prompting strategies；experimental rig；statistical methods；results；threats；conclusion。 |
| EMSE | An empirical analysis of vulnerability detection tools for solidity smart contracts | `10.1007/s10664-026-10867-7`, EMSE 2026 | 47 | Background；related work；motivating survey；study design；RQs；manual analysis；results；threats；conclusion；artifact。 |
| EMSE | An empirical evaluation of white-box and black-box test case prioritization techniques in CPSs modeled in Simulink | `10.1007/s10664-026-10875-7`, EMSE 2026 | 38 | Background；selected techniques；empirical evaluation；research questions；benchmark；metrics；statistical tests；results/discussion；threats；artifact。 |
| JSS | GateLens: A reasoning-enhanced LLM agent for automotive software release analytics | `10.1016/j.jss.2026.112961`, JSS 240 (2026) | 15 | Introduction；background/motivation；system overview；core components；data handling；experimental evaluation；RQs；results；conclusion。 |
| IST | Formal requirements engineering and large language models: a two-way roadmap | `10.1016/j.infsof.2025.107697`, IST 181 (2025) | 暂未本地计数 | DOI 与官方 metadata 已确认；命令行 PDF 访问受限。暂作为 topic-fit 样本，投前需浏览器复核。 |

已统计样本页数：

| 期刊 | 样本数 | PDF 页数范围 | 平均页数 |
|---|---:|---:|---:|
| SoSyM | 3 | 24-45 | 34.0 |
| ASEJ | 3 | 25-42 | 32.3 |
| REJ | 3 | 23-29 | 25.3 |
| EMSE | 3 | 29-47 | 38.0 |
| JSS | 1 | 15 | 15.0 |

## 5. 对 Path-1 有用的结构规律

1. Springer B 类期刊的 regular paper 不是会议短文形态。真实样本常见 25-45 页，尤其是有数据集、工具、工业案例、RQs、threats 和 artifact statement 的论文。
2. ASEJ、REJ、EMSE 以及不少 SoSyM empirical/tool paper 都会显式写 research questions。Path-1 不应只写 contribution bullets，应写 3-4 个 RQs。
3. Threats to validity / validity discussion 基本必须有。Path-1 涉及 LLM、human adjudication、prompt、reference model 和 dataset bias，更不能省略。
4. Artifact / data availability / replication package statement 在样本中很常见。Path-1 应提前规划 artifact statement，而不是最后补格式。
5. SoSyM 样本允许较长的方法定义、建模语言/语义说明和多段 evaluation。这支持 issue #67 中 SoSyM regular 作为主投路线的判断。
6. ASEJ 样本强调 automation、workflow、benchmark 和 measurable improvement。若切 ASEJ，应该真正把 automated feedback / repair loop 与 ablation 写成主线，而不是只换期刊名。
7. REJ 样本强调 requirements artifact、human validation、prompt/evaluation protocol、traceability 和 ambiguity。若切 REJ，requirements-to-model quality 与 human validation 要放到中心。
8. EMSE 样本大篇幅写 study design、data、metrics、statistical methods 和 threats。只有 empirical protocol 足够强时，EMSE 才是好备选。
9. Elsevier JSS/IST 在篇幅上更敏感。JSS 可以容纳紧凑的 15 页双栏 LLM systems paper；IST 有 15,000 words 硬上限，而且 references/appendices/figures/tables 都计入。

## 6. 推荐写作与模板策略

主策略：先用 Springer Nature `sn-jnl` 写 master draft。这样 SoSyM / ASEJ / REJ / EMSE 四条路线都能覆盖。只有真正切到 JSS / IST 时，再另建 Elsevier CAS 版本。

推荐初稿预算：

| 项 | 目标 |
|---|---:|
| 正文，不含 references | 10,000-12,000 words |
| 主文图表 | 8-10 个 |
| Springer publisher PDF 预期 | 约 28-36 页 |
| RQs | 3-4 个 |
| Threats / validity | 约 1.5-2.5 页 |
| Related work | 约 2.5-4 页 |
| Artifact / data availability | 明确 statement + repository README |

SoSyM-first 主文结构建议：

1. Introduction
2. Background and Motivating Example
3. Task Definition and Quality Criteria
4. Feedback-Guided LLM State-Machine Modeling Method
5. Experimental Design
6. Results by RQ
7. Discussion
8. Threats to Validity
9. Related Work
10. Conclusion

适合放 supplement / artifact 的内容：

- 完整 sample registry 与纳入/排除细节。
- prompt variants 与 prompt hashes。
- 完整 rubric 与 human adjudication instructions。
- 额外 per-system result tables。
- 长 failure taxonomy examples。
- raw / redacted LLM responses 与 repair logs。

若切 IST：

- research article 控制在 15,000 counted words 内，references、appendices、figures、tables 都计入。
- 长 prompt/rubric/sample 细节优先移到外部 artifact，而不是 appendix。
- 主文压缩到 RQ table、关键 ablation table、workflow figure、sample/corpus table、failure taxonomy table、artifact table。

若切 JSS：

- 按 Elsevier 双栏 `<18` 页目标压缩。
- 写 highlights 与更紧凑的 abstract。
- 前两页必须让 systems/software 角度明显：architecture、reliability、release-quality 或 software-system evaluation。

## 7. 投稿前仍需复核

1. 用浏览器复核 JSS / IST 的 ScienceDirect guide 和 PDF 样本；命令行访问有 WAF/403 限制。
2. 最终选定投稿期刊后，在投稿前当天重新打开 live author guidelines 和 submission system。
3. 若走 Springer special issue / collection，检查 collection 下拉项是否改变 article type、模板、cover letter 或来源资格。
4. 若走 REJ，专门检查匿名要求、title page、artifact link、acknowledgement、repository URL 和 self-citation。
5. 下载模板 ZIP 后，记录下载日期和 ZIP 文件 hash，便于后续复现投稿包。
