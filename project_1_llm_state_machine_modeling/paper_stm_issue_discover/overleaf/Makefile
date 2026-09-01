SHELL := /bin/sh
LATEXMK ?= latexmk
LATEX_FLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: en zh all check clean

en:
	@mkdir -p build/en
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/en -auxdir=build/en main.tex

zh:
	@mkdir -p build/zh
	$(LATEXMK) $(LATEX_FLAGS) -outdir=build/zh -auxdir=build/zh main-zh.tex

all: en zh

check:
	tools/check-paper

clean:
	rm -rf build
