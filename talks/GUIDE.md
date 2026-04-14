# talks 工作指南

本文档规定 `talks/` 下单次讨论工作区的维护方式。

## 1. 目标与边界

`talks/` 的目标是把这条链路稳定下来：

`讨论前准备 -> PPT 生成与 review -> 会后原始碎片 -> AI 扩写 -> 人工纠偏 -> 纪要定稿`

它不是论文集，不服务于 PDF 收录、`paper_content.txt` 提取或 `desc.md` / `STM.md` 生产。遇到论文类任务，应回到对应论文集或单论文目录处理，而不是混入这里。

## 2. 命名规则

每次讨论使用一个单独目录，默认命名为：

1. `yyyy-mm-dd-对象-主题`
2. 若同一天有多次相近讨论，再扩展为 `yyyy-mm-dd-hh-mm-对象-主题`

其中：

1. `对象` 尽量稳定，如 `导师`、`组会`、`同门`、`合作者`。
2. `主题` 只保留短关键词，避免写成长句。
3. 不要在目录名里混入“纪要”“讨论稿终版”之类阶段性词语，目录名应该稳定可长期维护。

## 3. 固定目录结构

每个讨论子目录默认包含以下内容：

```text
yyyy-mm-dd-对象-主题/
├── prep/
│   ├── notes.md
│   └── materials.md
├── ppt/
│   ├── PPT_GUIDE.md
│   ├── generate_ppt.py
│   ├── deck.pptx
│   ├── assets/
│   ├── rendered/
│   └── review/
│       └── notes.md
├── raw.md
├── minutes.md
└── todo.md
```

### 3.1 `prep/`

`prep/` 是讨论前准备层。

默认职责：

1. `prep/notes.md`
   - 记录这次讨论想解决什么。
   - 记录我当前的判断、假设和想确认的问题。
2. `prep/materials.md`
   - 记录会前需要回看的论文、路径、图表、代码、数据或文档。

如果材料较多，可以在 `prep/` 下继续加文件，但不应把这些内容直接混进 `minutes.md`。

### 3.2 `ppt/`

`ppt/` 是讨论配套 deck 工作区。

默认职责：

1. `PPT_GUIDE.md`
   - deck 的上游真源。
   - 负责写清目标、受众、页结构、页内主信息、备注和验收标准。
2. `generate_ppt.py`
   - 唯一生成入口。
   - 负责从 `PPT_GUIDE.md` 对应实现到 `deck.pptx`。
3. `deck.pptx`
   - 生成产物。
   - 不是唯一真源，不应只在这个文件上做手工改动。
4. `assets/`
   - 存放图表、截图、裁剪图和中间素材。
5. `rendered/`
   - 存放 review 用的 PDF / PNG 渲染结果。
6. `review/notes.md`
   - 记录视觉检查问题，以及这些问题应回写到 guide、generator 或两者。

### 3.3 `raw.md`

`raw.md` 是讨论后原始输入层，默认用于保存：

1. 片段化回忆。
2. 当时记下的关键词。
3. 不完整判断。
4. 明确标有问号或待确认的模糊点。

默认要求：

1. 优先保留原始语气和顺序。
2. 可以很短，可以不成句。
3. 不要为了“好看”提前抹平不确定性。

### 3.4 `minutes.md`

`minutes.md` 是结构化输出层，默认用于保存：

1. 讨论背景。
2. 已确认结论。
3. 展开说明。
4. 待确认点。
5. 后续动作。

### 3.5 `todo.md`

`todo.md` 只在讨论直接产生待办事项时使用。典型内容包括：

1. 需要回查的论文、目录或文档。
2. 需要补写的章节、图表或实验。
3. 需要后续再次确认的问题。

## 4. `deck-workflow` skill 使用规则

`talks/` 下只要涉及 PPT，默认必须使用 `deck-workflow` skill 的 guide-first 工作流。

### 4.1 开始前检查

先检查本机是否已安装：

```bash
test -f ~/.codex/skills/deck-workflow/SKILL.md
```

若未安装，直接安装：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HansBug/deck-workflow-skill \
  --path deck-workflow
```

安装后需要重启 Codex，让后续新会话自动识别该 skill。

### 4.2 后端与依赖约束

在本仓库中，PPT 工作流有以下硬约束：

1. 一律使用 Python 后端。
2. 生成器文件名固定为 `generate_ppt.py`。
3. 使用仓库根目录已有 `venv` 或当前 conda 环境，不新建子目录 `.venv`。
4. Python 依赖统一维护在仓库根目录 `requirements.txt`。
5. 若缺 `python-pptx`、`PyMuPDF`、`Pillow`、`pdf2image` 等依赖，直接装到仓库环境里。
6. 若缺 `soffice`、`pdftoppm`、字体等系统依赖，直接安装，不要强行绕开 review。

### 4.3 默认生产链

默认必须遵循以下链路：

1. 先写或修 `ppt/PPT_GUIDE.md`
2. 再写或修 `ppt/generate_ppt.py`
3. 生成 `ppt/deck.pptx`
4. 渲染到 `ppt/rendered/`
5. 把问题记到 `ppt/review/notes.md`
6. 再决定回写 guide、generator 或两者
7. 重新生成并重新 review

不要把 `.pptx` 当成唯一编辑入口。

### 4.4 常用命令

检查环境：

```bash
python ~/.codex/skills/deck-workflow/scripts/detect_deck_environment.py
```

生成 deck：

```bash
source venv/bin/activate
pip install -r requirements.txt
python talks/yyyy-mm-dd-对象-主题/ppt/generate_ppt.py
```

渲染 review：

```bash
python ~/.codex/skills/deck-workflow/scripts/render_review.py \
  talks/yyyy-mm-dd-对象-主题/ppt/deck.pptx \
  --output-dir talks/yyyy-mm-dd-对象-主题/ppt/rendered
```

## 5. 扩写与修订规则

AI 根据 `raw.md` 扩写 `minutes.md` 时，必须遵守以下规则：

1. 先忠实恢复原始意思，再考虑文字组织，不要为了流畅度改写掉原意。
2. 遇到明显依赖上下文才能成立的句子时，可以做最小必要补全，但不能无依据发明新结论。
3. 如果某个判断只是从零散片段推出来的，应明确标注为“待确认”或“根据上下文推测”。
4. 用户后续口头或书面纠正一旦出现，应以最新纠正为准，回写到 `minutes.md`。
5. `raw.md` 原则上不替换成扩写版，除非用户明确要求把原稿也一并整理。

## 6. 多轮修订规则

多轮修订时，默认采用“覆盖式重写正式文件 + 保留原始证据”的策略：

1. 讨论理解变化，重写 `minutes.md`。
2. deck 叙事变化，先改 `ppt/PPT_GUIDE.md`。
3. deck 版式变化，先改 `ppt/generate_ppt.py`。
4. 视觉 bug 先记到 `ppt/review/notes.md`，修完后再关闭。
5. 后续任务变化，同步更新 `todo.md`。

## 7. 推荐工作顺序

一轮完整工作建议按以下顺序执行：

1. 先用 `python -m tools.init_talk_workspace ...` 初始化目录。
2. 先写 `prep/notes.md` 与 `prep/materials.md`。
3. 若需要 PPT，先写 `ppt/PPT_GUIDE.md`。
4. 再实现 `ppt/generate_ppt.py`。
5. 生成并 review `ppt/deck.pptx`。
6. 讨论结束后立即写 `raw.md`。
7. 基于 `raw.md` 扩写 `minutes.md`。
8. 最后更新 `todo.md`。

## 8. 质量要求

在 `talks/` 下，质量判断标准不是“写得像正式论文”，而是：

1. 是否把准备、讲解和纪要三个阶段分开维护了。
2. 是否把 PPT 真正作为可迭代工作区维护，而不是一次性导出文件。
3. 是否忠实反映了原始讨论意思。
4. 是否清楚区分了已确认内容与待确认内容。
5. 是否把真正需要落地的后续动作写清楚了。
