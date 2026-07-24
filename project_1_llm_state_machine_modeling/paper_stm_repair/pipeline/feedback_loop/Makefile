.PHONY: help discover-demo discover-pair discover-custom test lint compileall

PYTHON ?= python
REPO_ROOT := $(abspath ../../../..)
SRC := $(CURDIR)/src
RUN_PYTHONPATH := $(SRC):$(REPO_ROOT)
PROFILE ?= gpt-5.5
CONTENT_LANGUAGE ?= zh-CN
PAIR_ID ?= llms_emp_feedback_final_0000
OUT ?= $(REPO_ROOT)/runs/paper1/feedback-loop/discover
RUN_STAMP ?= $(shell date -u +%Y%m%dT%H%M%SZ)
FIXTURE := $(CURDIR)/fixtures/manual_0000_identity

help:
	@printf '%s\n' 'discover-demo discover-pair discover-custom test lint compileall'

discover-demo:
	PYTHONPATH=$(RUN_PYTHONPATH) $(PYTHON) -m paper_stm_feedback_loop.discover \
		--case-id manual-0000-identity \
		--nl-file $(FIXTURE)/nl.txt \
		--fcstm-file $(FIXTURE)/STM_0.fcstm \
		--source-trace-file $(FIXTURE)/source_trace.json \
		--profile $(PROFILE) --content-language $(CONTENT_LANGUAGE) \
		--output-dir $(OUT)/manual-0000-identity-$(PROFILE)-$(RUN_STAMP) $(ARGS)

discover-pair:
	PYTHONPATH=$(RUN_PYTHONPATH) $(PYTHON) -m paper_stm_feedback_loop.discover \
		--pair-id $(PAIR_ID) --profile $(PROFILE) \
		--content-language $(CONTENT_LANGUAGE) \
		--output-dir $(OUT)/$(PAIR_ID)-$(PROFILE)-$(RUN_STAMP) $(ARGS)

discover-custom:
	PYTHONPATH=$(RUN_PYTHONPATH) $(PYTHON) -m paper_stm_feedback_loop.discover \
		--case-id $(CASE_ID) --nl-file $(NL_FILE) --fcstm-file $(FCSTM_FILE) \
		$(if $(SOURCE_TRACE_FILE),--source-trace-file $(SOURCE_TRACE_FILE),) \
		--profile $(PROFILE) --content-language $(CONTENT_LANGUAGE) \
		--output-dir $(OUT)/$(CASE_ID)-$(PROFILE)-$(RUN_STAMP) $(ARGS)

test:
	PYTHONPATH=$(RUN_PYTHONPATH) $(PYTHON) -m pytest -q $(CURDIR)/tests

lint:
	ruff check $(CURDIR)/src $(CURDIR)/tests

compileall:
	PYTHONPATH=$(RUN_PYTHONPATH) $(PYTHON) -m compileall -q $(CURDIR)/src $(CURDIR)/tests
