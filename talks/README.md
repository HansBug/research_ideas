# talks

`talks/` 是仓库根目录下专门的人类讨论工作区，用来维护我与导师、同门、合作者或其他人的单次讨论目录。

它不是“一个讨论一份 Markdown”那种轻量便签区，而是一个**带准备材料、PPT 工作区、原始碎片和最终纪要**的持续维护目录。

## 它解决什么问题

很多讨论并不是开始前毫无准备、结束后一次写完。更真实的工作流通常是：

1. 讨论前先整理自己的准备材料。
2. 需要时做一套可迭代维护的 PPT。
3. 讨论后把还能记住的原始碎片写下来。
4. AI 基于这些碎片扩写成结构化纪要。
5. 我再纠正、补充、删改。
6. AI 继续重写，直到形成可信、可回看的版本。

`talks/` 就是为这条链路服务的。

## 目录结构

推荐结构如下：

```text
talks/
├── README.md
├── GUIDE.md
└── 2026-04-14-导师-状态机边界/
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

其中：

1. 每次讨论必须使用单独子目录。
2. 子目录名默认使用 `yyyy-mm-dd-对象-主题`。
3. 如果同一天有多次相近讨论，再扩展为 `yyyy-mm-dd-hh-mm-对象-主题`。
4. `prep/` 保存讨论前准备。
5. `ppt/` 保存 deck 的 guide、generator、导出产物与 review 记录。
6. `raw.md` 保存讨论后第一时间写下的原始碎片。
7. `minutes.md` 保存逐轮修订后的正式纪要。
8. `todo.md` 保存后续动作。

## deck-workflow skill 约定

`talks/` 下凡是要做 PPT 的讨论，默认都走本机已安装的 `deck-workflow` skill。

当前本机安装位置是：

```text
~/.codex/skills/deck-workflow
```

默认工作方式：

1. 先检查 `~/.codex/skills/deck-workflow/SKILL.md` 是否存在。
2. 若缺失，使用 skill-installer 从 `HansBug/deck-workflow-skill` 仓库安装。
3. 安装后重启 Codex，让新会话自动拾取该 skill。
4. 在本仓库里，`ppt/` 一律用 Python 的 `generate_ppt.py`，不使用 JavaScript 生成器。
5. Python 依赖统一安装到仓库自己的 `venv` 或当前 conda 环境里，不在 `ppt/` 里额外建局部环境。
6. `PPT_GUIDE.md`、`generate_ppt.py`、`deck.pptx`、`rendered/`、`review/notes.md` 都留在对应讨论子目录里，便于多轮迭代。

## 初始化方式

新建一次讨论目录时，优先使用仓库工具：

```bash
python -m tools.init_talk_workspace 2026-04-14-导师-讨论主题
```

这个命令会自动创建：

1. `prep/notes.md`
2. `prep/materials.md`
3. `ppt/PPT_GUIDE.md`
4. `ppt/generate_ppt.py`
5. `ppt/review/notes.md`
6. `raw.md`
7. `minutes.md`
8. `todo.md`

## AI 工作入口

在 `talks/` 下工作时，默认按以下顺序：

1. 先读 [README.md](./README.md)。
2. 再读 [GUIDE.md](./GUIDE.md)。
3. 进入目标讨论目录，先读 `prep/notes.md` 与 `prep/materials.md`。
4. 若存在 deck，再读 `ppt/PPT_GUIDE.md` 与 `ppt/review/notes.md`。
5. 讨论后处理纪要时，再读 `raw.md`。
6. 最后重写或更新 `minutes.md` 与 `todo.md`。
