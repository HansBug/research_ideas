SHELL := /bin/sh
LATEXMK ?= latexmk
LATEX_FLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error
OVERLEAF_ZIP ?= build/overleaf-upload.zip

.PHONY: en zh all zip check clean

en:
	@mkdir -p build/en
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/en -auxdir=build/en main.tex

zh:
	@mkdir -p build/zh
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/zh -auxdir=build/zh main-zh.tex

all: en zh

# Build the smallest source archive accepted by Overleaf. Documentation,
# validators, vendor archives, and generated build files stay outside it.
zip:
	@mkdir -p "$(dir $(OVERLEAF_ZIP))"
	@rm -f "$(OVERLEAF_ZIP)"
	@find Makefile main.tex main-zh.tex IEEEtran.cls IEEEtran.bst c70gbsn.fd references.bib config sections figures tables -type f ! -name 'README.md' -print | zip -q -@ "$(OVERLEAF_ZIP)"
	@printf 'Created %s\n' "$(OVERLEAF_ZIP)"

check:
	tools/check-paper

clean:
	rm -rf build
