# 渲染与检查命令

## 1. 使用仓库自己的 Python 环境

```bash
source venv/bin/activate
pip install -r requirements.txt
python talks/2026-04-15-导师-进展汇报与思考/ppt/generate_ppt.py
```

## 2. 渲染 review 产物

```bash
python ~/.codex/skills/deck-workflow/scripts/render_review.py \
  talks/2026-04-15-导师-进展汇报与思考/ppt/deck.pptx \
  --output-dir talks/2026-04-15-导师-进展汇报与思考/ppt/rendered
```
