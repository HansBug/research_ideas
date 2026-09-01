# Paper1 F1 Overleaf project

This directory is a self-contained, double-anonymous SANER 2027 Research Track submission-manuscript scaffold. `main.tex` is the English submission root; `main-zh.tex` is the Chinese internal companion and is not for submission.

Build locally with the Overleaf default `pdfLaTeX` configuration:

```text
make en       # English PDF in build/en/main.pdf
make zh       # Chinese companion PDF in build/zh/main-zh.pdf
make all      # both
make zip      # minimal Overleaf upload archive: build/overleaf-upload.zip
make check    # deterministic gates and clean builds
make clean
```

Upload `build/overleaf-upload.zip` to Overleaf as-is for the minimal project. It contains only the two roots, byte-identical class/style work copies, CJK fallback, shared config/sections, and figure/table sources or assets; documentation, validators, protected template archives, and build caches are excluded. You may also upload the whole directory, select the appropriate root document, and download the source zip for the same clean-build round trip. Long-term rules and writing-phase entry criteria are in `GUIDE.md`.
