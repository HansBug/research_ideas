# LLM状态机与UML/SysML建模文献检索指南

**创建日期**: 2026-03-05
**目标**: 检索2023-2025年LLM生成状态机（含Petri网等广义状态机）及UML/SysML建模的高相关性文献

---

## 📋 检索执行清单

### 立即行动项
- [ ] Google Scholar搜索核心关键词组合
- [ ] 检查MODELS 2024/2025会议论文集
- [ ] 检查ASE 2024/2025会议论文集
- [ ] 追踪MIG和TTool-AI论文的前向引用
- [ ] 检查arXiv cs.SE分类的2024-2025论文
- [ ] 检查ICSE 2025和FSE 2024论文集
- [ ] 追踪关键作者的最新工作

---

## 🎯 一、核心检索方向（按优先级排序）

### 方向1: LLM直接生成状态机 ⭐⭐⭐⭐⭐

**研究现状**: 这是最直接相关但文献较少的领域，存在明显研究空白

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT-4" OR "ChatGPT" OR "generative AI") AND
("state machine" OR "statechart" OR "state diagram" OR "finite state machine" OR "FSM" OR "behavioral model") AND
("generation" OR "synthesis" OR "automated" OR "automatic" OR "modeling")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- MODELS 2024/2025 (ACM/IEEE International Conference on Model Driven Engineering)
- ASE 2024/2025 (Automated Software Engineering)
- ICSE 2025 (International Conference on Software Engineering)
- FSE 2024/2025 (Foundations of Software Engineering)
- SoSyM (Software and Systems Modeling Journal)
- arXiv cs.SE

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=%22large+language+model%22+%22state+machine%22+generation+2024+2025

arXiv:
https://arxiv.org/search/?query=%22state+machine%22+LLM&searchtype=all&order=-announced_date_first

DBLP MODELS 2024:
https://dblp.org/db/conf/models/models2024.html

DBLP ASE 2024:
https://dblp.org/db/conf/kbse/ase2024.html
```

**预期研究主题**:
- 从自然语言需求生成状态机
- 基于Few-shot/Chain-of-Thought的状态机生成
- 状态机的增量式生成和迭代优化
- 控制系统状态机的自动建模

---

### 方向2: LLM生成Petri网及其他形式化模型 ⭐⭐⭐⭐⭐

**研究现状**: Petri网是广义状态机的重要形式，在并发系统建模中广泛应用

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT-4") AND
("Petri net" OR "Petri nets" OR "process model" OR "BPMN" OR "workflow model") AND
("generation" OR "synthesis" OR "automated modeling")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- ICPM (International Conference on Process Mining)
- BPM (Business Process Management Conference)
- Petri Nets Conference
- MODELS 2024/2025
- arXiv cs.SE

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=%22large+language+model%22+%22Petri+net%22+generation

DBLP Petri Nets:
https://dblp.org/db/conf/apn/

DBLP BPM 2024:
https://dblp.org/db/conf/bpm/bpm2024.html
```

**预期研究主题**:
- 从业务流程描述生成Petri网
- LLM辅助的工作流建模
- 并发系统的自动化建模
- BPMN到Petri网的转换

---

### 方向3: LLM生成UML行为图 ⭐⭐⭐⭐⭐

**研究现状**: UML行为图（状态图、活动图、序列图）是状态机的标准表示

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT-4" OR "ChatGPT") AND
("UML" OR "unified modeling language") AND
("state diagram" OR "statechart" OR "activity diagram" OR "sequence diagram" OR "behavioral model") AND
("generation" OR "automated" OR "synthesis")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- MODELS 2024/2025
- UML Conference
- SoSyM Journal
- ICSE 2025
- ASE 2024/2025

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=LLM+UML+behavioral+diagram+generation+2024

DBLP MODELS:
https://dblp.org/db/conf/models/

Semantic Scholar:
https://www.semanticscholar.org/search?q=GPT%20UML%20generation
```

**预期研究主题**:
- ChatGPT生成UML状态图
- 从用例到序列图的自动生成
- UML活动图的LLM生成
- 多视图UML模型的一致性

---

### 方向4: LLM生成SysML模型 ⭐⭐⭐⭐⭐

**研究现状**: SysML是系统工程的建模语言，包含状态机图

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT-4") AND
("SysML" OR "systems modeling language") AND
("state machine" OR "block diagram" OR "requirement diagram" OR "automated modeling")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- MODELS 2024/2025
- INCOSE (International Council on Systems Engineering)
- IEEE ISSE (Systems Engineering Symposium)
- SoSyM Journal

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=LLM+SysML+generation+2024+2025

DBLP INCOSE:
https://dblp.org/search?q=venue%3AINCOSE%3A

IEEE Xplore:
https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=LLM%20SysML
```

**已知重要工作**:
- **TTool-AI (Apvrille & Sultan, 2024)**: SysML块图和状态机生成 [已在BASELINE.md]
- 需要追踪TTool-AI的后续工作和引用

**预期研究主题**:
- 从需求文档生成SysML状态机
- SysML块图的自动生成
- 需求图到设计模型的转换
- MBSE工具链中的LLM集成

---

### 方向5: LLM生成时间自动机和形式化模型 ⭐⭐⭐⭐

**研究现状**: 时间自动机是带时间约束的状态机，用于实时系统验证

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT") AND
("timed automata" OR "temporal logic" OR "formal specification" OR "model checking") AND
("generation" OR "synthesis" OR "automated")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- CAV (Computer Aided Verification)
- TACAS (Tools and Algorithms for Construction and Analysis of Systems)
- FORMATS (Formal Modeling and Analysis of Timed Systems)
- FM (Formal Methods)
- ICSE 2025

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=LLM+timed+automata+generation

DBLP CAV:
https://dblp.org/db/conf/cav/

DBLP TACAS:
https://dblp.org/db/conf/tacas/
```

**预期研究主题**:
- LLM生成UPPAAL时间自动机
- 从需求生成时序逻辑规约
- LTL/CTL性质的自动生成
- 形式化规约的LLM辅助建模

---

## 🎯 二、UML/SysML类图和结构建模（中高优先级）

### 方向6: LLM生成UML类图 ⭐⭐⭐⭐

**研究现状**: 这是目前研究最多的领域，已有多篇重要工作

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT-4" OR "ChatGPT") AND
("UML class diagram" OR "domain model" OR "object model") AND
("generation" OR "automated modeling")
AND (2023 OR 2024 OR 2025)
```

**已知重要工作**:
- **Cámara et al. (2023)**: ChatGPT生成UML类图评估 [已在BASELINE.md]
- **Chen et al. (2023)**: 单步领域建模 [已在BASELINE.md]
- **MIG (Yang et al., 2024)**: 多步迭代生成 [已在BASELINE.md]

**预期发表渠道**:
- MODELS 2024/2025
- ICSE 2025
- SoSyM Journal
- ASE 2024/2025

**具体检索链接**:
```
Google Scholar - 引用追踪Cámara et al.:
https://scholar.google.com/scholar?cites=XXX (需要获取citation ID)

Google Scholar - 引用追踪MIG:
https://scholar.google.com/scholar?q=related+MIG+domain+modeling

DBLP MODELS 2024:
https://dblp.org/db/conf/models/models2024.html
```

**需要追踪的工作**:
- Cámara et al. (2023)的前向引用（2024-2025年引用它的工作）
- Chen et al. (2023)单步建模的后续改进
- MIG的后续工作和改进

---

### 方向7: LLM生成其他UML图 ⭐⭐⭐

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT") AND
("use case diagram" OR "component diagram" OR "deployment diagram" OR "package diagram") AND
("generation" OR "automated")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- MODELS 2024/2025
- RE (Requirements Engineering) 2024/2025
- MODELSWARD 2024/2025

---

## 🎯 三、相关技术方向（中优先级）

### 方向8: LLM辅助的模型驱动工程 ⭐⭐⭐⭐

**检索关键词组合**:
```
("large language model" OR "LLM" OR "generative AI") AND
("model-driven engineering" OR "MDE" OR "model-based systems engineering" OR "MBSE") AND
(2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- MODELS 2024/2025
- MODELSWARD 2024/2025
- SoSyM Journal

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=LLM+model-driven+engineering+2024

DBLP MODELSWARD:
https://dblp.org/db/conf/modelsward/
```

---

### 方向9: LLM生成目标模型和需求模型 ⭐⭐⭐⭐

**研究现状**: 目标模型是高层次的需求建模方法

**检索关键词组合**:
```
("large language model" OR "GPT-4") AND
("goal model" OR "i* model" OR "KAOS" OR "requirements model") AND
("generation" OR "automated")
AND (2023 OR 2024 OR 2025)
```

**已知重要工作**:
- **Chen et al. (2023)**: GPT-4创建目标模型 [已在BASELINE.md]
- **Nakagawa & Honiden (2023)**: MAPE-K循环目标模型生成 [已在BASELINE.md]

**预期发表渠道**:
- RE (Requirements Engineering) 2024/2025
- REW (Requirements Engineering Workshops)
- MODELS 2024/2025

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=GPT-4+goal+model+generation

DBLP RE Conference:
https://dblp.org/db/conf/re/
```

---

### 方向10: LLM与形式化验证结合 ⭐⭐⭐⭐

**研究现状**: 这是一个新兴领域，与本研究的验证主题高度相关

**检索关键词组合**:
```
("large language model" OR "LLM" OR "GPT") AND
("formal verification" OR "model checking" OR "theorem proving" OR "property verification") AND
(2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- CAV 2024/2025
- TACAS 2024/2025
- FM 2024/2025
- ICSE 2025
- FSE 2024/2025

**具体检索链接**:
```
Google Scholar:
https://scholar.google.com/scholar?q=LLM+formal+verification+2024

DBLP CAV:
https://dblp.org/db/conf/cav/

arXiv:
https://arxiv.org/search/?query=LLM+model+checking
```

**预期研究主题**:
- LLM生成验证性质
- LLM辅助的反例分析
- LLM驱动的模型修复
- 形式化规约的自动生成

---

### 方向11: Prompt工程和Few-shot Learning在建模中的应用 ⭐⭐⭐

**检索关键词组合**:
```
("prompt engineering" OR "few-shot learning" OR "chain-of-thought") AND
("software modeling" OR "UML" OR "model generation") AND
(2023 OR 2024 OR 2025)
```

**已知重要工作**:
- **Chaaben et al. (2023)**: Few-shot prompt learning模型补全 [已在BASELINE.md]
- **MIG (2024)**: 使用Few-shot和CoT进行领域建模

**预期发表渠道**:
- ICSE-NIER 2024/2025
- MODELS 2024/2025
- ASE 2024/2025

---

### 方向12: LLM生成软件架构模型 ⭐⭐⭐

**检索关键词组合**:
```
("large language model" OR "ChatGPT" OR "GPT") AND
("software architecture" OR "architectural model" OR "component model") AND
("generation" OR "automated")
AND (2023 OR 2024 OR 2025)
```

**已知重要工作**:
- **Ahmad et al. (2023)**: ChatGPT协作软件架构 [已在BASELINE.md]

**预期发表渠道**:
- ICSA (International Conference on Software Architecture)
- EASE (Evaluation and Assessment in Software Engineering)
- MODELS 2024/2025

---

## 🎯 四、作者和研究组追踪（高优先级）

### 4.1 关键作者追踪

**必须追踪的作者（2024-2025年最新工作）**:

1. **Javier Cámara** (University of Málaga)
   - 已知工作: ChatGPT UML评估 (2023)
   - Google Scholar: https://scholar.google.com/citations?user=XXX
   - 检索: "Javier Cámara" AND (LLM OR "generative AI") AND (2024 OR 2025)

2. **Kua Chen** (McGill University)
   - 已知工作: MIG单步建模 (2023), 目标模型 (2023)
   - 检索: "Kua Chen" AND "domain modeling" AND (2024 OR 2025)

3. **Yujing Yang** (McGill University)
   - 已知工作: MIG (2024)
   - 检索: "Yujing Yang" AND LLM AND modeling

4. **Gunter Mussbacher** (McGill University)
   - 已知工作: MIG (2024)
   - 检索: "Gunter Mussbacher" AND LLM

5. **Ludovic Apvrille** (Télécom Paris)
   - 已知工作: TTool-AI (2024)
   - 检索: "Ludovic Apvrille" AND (AI OR LLM) AND (SysML OR modeling)

6. **Aamir Ahmad**
   - 已知工作: ChatGPT软件架构 (2023)
   - 检索: "Aamir Ahmad" AND ChatGPT AND architecture

### 4.2 研究组追踪

**McGill University - Software Engineering Lab**
- 网站: 需要查找
- 成员: Gunter Mussbacher, Kua Chen, Yujing Yang
- 研究方向: 模型驱动工程、LLM建模
- 行动: 查看实验室网站的Publications页面

**Télécom Paris - COMET Lab**
- 网站: 需要查找
- 成员: Ludovic Apvrille
- 研究方向: 系统建模、MBSE、TTool工具
- 行动: 查看TTool项目页面和相关发表

**University of Málaga - Software Modeling Group**
- 网站: 需要查找
- 成员: Javier Cámara
- 研究方向: UML建模、生成式AI
- 行动: 查看研究组网站

---

## 🎯 五、引用追踪策略（极高优先级）

### 5.1 前向引用追踪（谁引用了这些工作）

**必须追踪的论文**:

1. **Cámara et al. (2023) - ChatGPT UML评估**
   - 在Google Scholar查找"Cited by"
   - 筛选2024-2025年的引用
   - 重点关注MODELS、ICSE、ASE会议的引用

2. **Chen et al. (2023) - 单步领域建模**
   - 这是MIG的前身工作
   - 查找后续改进和扩展工作
   - 重点关注MODELS 2024的相关工作

3. **MIG (Yang et al., 2024)**
   - 查找2024-2025年的引用
   - 关注改进和对比工作

4. **TTool-AI (Apvrille & Sultan, 2024)**
   - 查找SysML建模的后续工作
   - 关注MBSE领域的引用

### 5.2 后向引用追踪（这些工作引用了谁）

**行动**:
- 获取上述论文的完整参考文献列表
- 识别其中与LLM建模相关的工作
- 特别关注2022-2023年的工作（可能被遗漏）

---

## 🎯 六、会议论文集系统检索（高优先级）

### 6.1 MODELS 2024

**检索链接**: https://dblp.org/db/conf/models/models2024.html

**检索策略**:
- 浏览完整论文列表
- 搜索关键词: LLM, GPT, ChatGPT, generative AI, automated modeling
- 重点关注: Research Papers track

**预期主题**:
- LLM生成UML/SysML模型
- 模型驱动工程中的AI应用
- 自动化建模工具

### 6.2 ASE 2024

**检索链接**: https://dblp.org/db/conf/kbse/ase2024.html

**检索策略**:
- 浏览完整论文列表
- 搜索关键词: LLM, model generation, automated software engineering
- 重点关注: Technical Papers

### 6.3 ICSE 2025

**检索链接**: https://conf.researchr.org/home/icse-2025

**检索策略**:
- 查看已接收论文列表（如果已公布）
- 搜索关键词: LLM, model generation, formal methods
- 重点关注: Technical Track, NIER Track

### 6.4 FSE 2024

**检索链接**: https://dblp.org/db/conf/sigsoft/fse2024.html

**检索策略**:
- 浏览完整论文列表
- 搜索关键词: LLM, software modeling, automated generation

### 6.5 RE 2024

**检索链接**: https://dblp.org/db/conf/re/re2024.html

**检索策略**:
- 重点关注需求建模相关工作
- 搜索关键词: LLM, requirements, goal model, use case

### 6.6 CAV 2024

**检索链接**: https://dblp.org/db/conf/cav/cav2024.html

**检索策略**:
- 重点关注形式化验证相关工作
- 搜索关键词: LLM, formal verification, model checking, synthesis

---

## 🎯 七、arXiv预印本检索（中高优先级）

### 7.1 cs.SE (Software Engineering)

**检索链接**:
```
https://arxiv.org/search/?query=LLM+state+machine&searchtype=all&source=header&order=-announced_date_first

https://arxiv.org/search/?query=GPT+UML+modeling&searchtype=all&source=header&order=-announced_date_first

https://arxiv.org/list/cs.SE/recent
```

**检索策略**:
- 按时间倒序浏览2024-2025年的论文
- 搜索关键词: LLM, GPT, state machine, UML, SysML, modeling
- 每周检查一次新提交

### 7.2 cs.AI 和 cs.LG

**检索链接**:
```
https://arxiv.org/search/?query=large+language+model+formal+model&searchtype=all

https://arxiv.org/list/cs.AI/recent
```

**检索策略**:
- 关注LLM在形式化方法中的应用
- 搜索关键词: LLM, formal specification, model synthesis

---

## 🎯 八、特定工具和系统相关工作

### 8.1 UPPAAL相关

**检索关键词**:
```
("UPPAAL" OR "timed automata") AND ("LLM" OR "GPT" OR "automated generation")
AND (2023 OR 2024 OR 2025)
```

**说明**: UPPAAL是时间自动机验证工具，与本研究高度相关

### 8.2 TTool相关

**检索关键词**:
```
"TTool" AND ("AI" OR "LLM" OR "automated")
```

**说明**: 追踪TTool-AI的后续工作和改进

### 8.3 其他建模工具

**检索关键词**:
```
("Papyrus" OR "Enterprise Architect" OR "MagicDraw" OR "Cameo") AND
("LLM" OR "AI" OR "automated modeling")
```

---

## 🎯 九、领域特定建模（中优先级）

### 9.1 控制系统建模

**检索关键词组合**:
```
("large language model" OR "LLM") AND
("control system" OR "embedded system" OR "cyber-physical system" OR "CPS") AND
("state machine" OR "behavioral model" OR "modeling")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- EMSOFT (Embedded Software)
- RTAS (Real-Time and Embedded Technology and Applications)
- RTSS (Real-Time Systems Symposium)
- MODELS 2024/2025

**说明**: 这与本研究的应用领域（控制系统）直接相关

### 9.2 安全关键系统建模

**检索关键词组合**:
```
("large language model" OR "LLM") AND
("safety-critical" OR "ISO 26262" OR "IEC 61508" OR "functional safety") AND
("modeling" OR "state machine")
AND (2023 OR 2024 OR 2025)
```

**预期发表渠道**:
- SAFECOMP (Computer Safety, Reliability, and Security)
- DSN (Dependable Systems and Networks)
- MODELS 2024/2025

---

## 🎯 十、多模态LLM和建模（新兴方向）

### 10.1 视觉-语言模型生成图表

**检索关键词组合**:
```
("multimodal" OR "vision-language model" OR "GPT-4V" OR "Claude") AND
("diagram generation" OR "UML" OR "state machine diagram")
AND (2024 OR 2025)
```

**预期发表渠道**:
- NeurIPS 2024
- ICLR 2025
- CVPR 2024/2025
- MODELS 2025

**说明**: 这是一个新兴方向，可能在2025年出现相关工作

---

## 📊 检索记录模板

### 检索记录 [日期]

**检索式**:
**数据库**:
**结果数量**:
**筛选后数量**:
**发现的重要工作**:
1.
2.

**备注**:

---

## ✅ 下一步具体行动

### 本周内完成（优先级1）

1. **引用追踪**:
   - [ ] 在Google Scholar搜索Cámara et al. (2023)，获取完整引用信息和citation ID
   - [ ] 追踪Cámara et al.的前向引用（2024-2025）
   - [ ] 在Google Scholar搜索Chen et al. (2023)单步建模工作
   - [ ] 追踪MIG (2024)的引用情况

2. **会议论文集检索**:
   - [ ] 检查MODELS 2024完整论文列表
   - [ ] 检查ASE 2024完整论文列表
   - [ ] 检查ICSE 2025已接收论文（如果已公布）

3. **作者追踪**:
   - [ ] 在Google Scholar搜索Javier Cámara的2024-2025年工作
   - [ ] 在Google Scholar搜索Kua Chen的2024-2025年工作
   - [ ] 在Google Scholar搜索Ludovic Apvrille的2024-2025年工作

### 本月内完成（优先级2）

4. **系统性检索**:
   - [ ] 执行方向1的检索（LLM直接生成状态机）
   - [ ] 执行方向2的检索（Petri网生成）
   - [ ] 执行方向3的检索（UML行为图）
   - [ ] 执行方向4的检索（SysML模型）
   - [ ] 执行方向10的检索（LLM与形式化验证）

5. **arXiv检索**:
   - [ ] 浏览arXiv cs.SE 2024-2025年的相关论文
   - [ ] 搜索arXiv中的状态机生成相关预印本

6. **研究组追踪**:
   - [ ] 查找McGill University Software Engineering Lab网站
   - [ ] 查找Télécom Paris COMET Lab网站
   - [ ] 查找University of Málaga相关研究组

### 持续进行

7. **定期检查**:
   - [ ] 每周检查arXiv cs.SE新提交
   - [ ] 每月检查主要会议的论文接收情况
   - [ ] 设置Google Scholar alerts for关键词组合

---

## 📝 预期发现总结

基于研究趋势分析，预期在以下领域发现高相关性文献：

### 极高相关性（⭐⭐⭐⭐⭐）
1. **LLM直接生成状态机**: 研究空白，可能有2-5篇2024-2025年的工作
2. **LLM生成SysML状态机**: TTool-AI的后续工作，预期2-3篇
3. **LLM生成UML行为图**: 预期5-10篇2024-2025年的工作
4. **LLM与形式化验证结合**: 新兴领域，预期3-5篇

### 高相关性（⭐⭐⭐⭐）
5. **LLM生成Petri网**: 预期2-4篇
6. **LLM生成UML类图**: 已有多篇，预期发现10-15篇2023-2025年的工作
7. **LLM生成目标模型**: 预期3-5篇
8. **控制系统建模**: 预期2-3篇

### 中等相关性（⭐⭐⭐）
9. **LLM辅助MDE/MBSE**: 预期5-8篇
10. **Prompt工程在建模中的应用**: 预期3-5篇
11. **LLM生成软件架构**: 预期3-5篇

---

## 🔄 文档更新日志

- **2026-03-05**: 创建文档，制定详细检索策略
  - 定义10个核心检索方向
  - 制定作者和研究组追踪计划
  - 制定引用追踪策略
  - 制定会议论文集检索计划
  - 制定具体行动清单

