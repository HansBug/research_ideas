.PHONY: discover discover-demo discover-pair discover-custom discover-test

DISCOVER_SRC := project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/src
DISCOVER_ROOT := $(CURDIR)/project_1_llm_state_machine_modeling
DISCOVER_PYTHONPATH := $(DISCOVER_SRC):$(DISCOVER_ROOT):$(CURDIR)
DISCOVER_OUT ?= runs/paper1/discover/demo
DISCOVER_PAIR ?= llms_emp_stm_results_0000_manual_identity
DISCOVER_PROFILE ?= gpt-5.5
DISCOVER_LANGUAGE ?= zh-CN
DISCOVER_RENDERER ?= rich

# Real provider demo. The caller must run `source .env` first; the application
# fails before provider dispatch when the selected profile is not configured.
discover-demo: discover-pair

discover-pair:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m paper_stm_repair_loop.discover \
		--pair-id $(DISCOVER_PAIR) \
		--profile $(DISCOVER_PROFILE) \
		--content-language $(DISCOVER_LANGUAGE) \
		--renderer $(DISCOVER_RENDERER) \
		--output-dir $(DISCOVER_OUT) $(DISCOVER_ARGS)

discover-custom:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m paper_stm_repair_loop.discover \
		--case-id $(DISCOVER_CASE) \
		--nl-file $(DISCOVER_NL) \
		--fcstm-file $(DISCOVER_FCSTM) \
		$(if $(DISCOVER_RAW_SOURCE),--raw-source-file $(DISCOVER_RAW_SOURCE),) \
		$(if $(DISCOVER_SOURCE_TRACE),--source-trace-file $(DISCOVER_SOURCE_TRACE),) \
		--profile $(DISCOVER_PROFILE) \
		--content-language $(DISCOVER_LANGUAGE) \
		--renderer $(DISCOVER_RENDERER) \
		--output-dir $(DISCOVER_OUT) $(DISCOVER_ARGS)

discover:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m paper_stm_repair_loop.discover $(DISCOVER_ARGS)

discover-test:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m pytest -q \
		project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/tests
