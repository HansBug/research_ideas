.PHONY: discover discover-demo discover-pair discover-custom discover-test \
	legacy-discover legacy-discover-demo legacy-discover-pair legacy-discover-custom legacy-discover-test

FEEDBACK_LOOP_DIR := project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/feedback_loop
PYTHON ?= python

# The default discover entry points are the independent paper1 feedback_loop
# pipeline. Legacy commands remain available only under an explicit prefix.
discover: discover-pair

discover-demo:
	$(MAKE) -C $(FEEDBACK_LOOP_DIR) discover-demo PYTHON=$(PYTHON) \
		PROFILE=$(DISCOVER_PROFILE) CONTENT_LANGUAGE=$(DISCOVER_LANGUAGE) \
		OUT=$(DISCOVER_OUT) ARGS="$(DISCOVER_ARGS)"

discover-pair:
	$(MAKE) -C $(FEEDBACK_LOOP_DIR) discover-pair PYTHON=$(PYTHON) \
		PAIR_ID=$(DISCOVER_PAIR) PROFILE=$(DISCOVER_PROFILE) \
		CONTENT_LANGUAGE=$(DISCOVER_LANGUAGE) OUT=$(DISCOVER_OUT) \
		ARGS="$(DISCOVER_ARGS)"

discover-custom:
	$(MAKE) -C $(FEEDBACK_LOOP_DIR) discover-custom PYTHON=$(PYTHON) \
		CASE_ID=$(DISCOVER_CASE) NL_FILE=$(DISCOVER_NL) \
		FCSTM_FILE=$(DISCOVER_FCSTM) SOURCE_TRACE_FILE=$(DISCOVER_SOURCE_TRACE) \
		PROFILE=$(DISCOVER_PROFILE) CONTENT_LANGUAGE=$(DISCOVER_LANGUAGE) \
		OUT=$(DISCOVER_OUT) ARGS="$(DISCOVER_ARGS)"

discover-test:
	$(MAKE) -C $(FEEDBACK_LOOP_DIR) test PYTHON=$(PYTHON)

.PHONY: legacy-discover legacy-discover-demo legacy-discover-pair legacy-discover-custom legacy-discover-test

DISCOVER_SRC := project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/src
DISCOVER_ROOT := $(CURDIR)/project_1_llm_state_machine_modeling
DISCOVER_PYTHONPATH := $(DISCOVER_SRC):$(DISCOVER_ROOT):$(CURDIR)
DISCOVER_OUT ?= runs/paper1/discover/demo
DISCOVER_PAIR ?= llms_emp_feedback_final_0000
DISCOVER_PROFILE ?= gpt-5.5
DISCOVER_LANGUAGE ?= zh-CN
DISCOVER_RENDERER ?= rich
DISCOVER_DEMO_ROOT := $(FEEDBACK_LOOP_DIR)/fixtures/manual_0000_identity
DISCOVER_CASE ?= manual-0000-identity
DISCOVER_NL ?= $(DISCOVER_DEMO_ROOT)/nl.txt
DISCOVER_FCSTM ?= $(DISCOVER_DEMO_ROOT)/STM_0.fcstm

LEGACY_DISCOVER_DEMO_ROOT := project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/fixtures/discover_integrated/0000_hldcs_manual_identity
LEGACY_DISCOVER_CASE ?= llms_emp_stm_results_0000_manual_identity
LEGACY_DISCOVER_NL ?= $(LEGACY_DISCOVER_DEMO_ROOT)/nl.txt
LEGACY_DISCOVER_FCSTM ?= $(LEGACY_DISCOVER_DEMO_ROOT)/STM_0.fcstm

# Legacy real provider demo. The caller must run `source .env` first; the application
# fails before provider dispatch when the selected profile is not configured.
legacy-discover-demo: legacy-discover-custom

legacy-discover-pair:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m paper_stm_repair_loop.discover \
		--pair-id $(DISCOVER_PAIR) \
		--profile $(DISCOVER_PROFILE) \
		--content-language $(DISCOVER_LANGUAGE) \
		--renderer $(DISCOVER_RENDERER) \
		--output-dir $(DISCOVER_OUT) $(DISCOVER_ARGS)

legacy-discover-custom:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m paper_stm_repair_loop.discover \
		--case-id $(LEGACY_DISCOVER_CASE) \
		--nl-file $(LEGACY_DISCOVER_NL) \
		--fcstm-file $(LEGACY_DISCOVER_FCSTM) \
		$(if $(LEGACY_DISCOVER_RAW_SOURCE),--raw-source-file $(LEGACY_DISCOVER_RAW_SOURCE),) \
		$(if $(LEGACY_DISCOVER_SOURCE_TRACE),--source-trace-file $(LEGACY_DISCOVER_SOURCE_TRACE),) \
		--profile $(DISCOVER_PROFILE) \
		--content-language $(DISCOVER_LANGUAGE) \
		--renderer $(DISCOVER_RENDERER) \
		--output-dir $(DISCOVER_OUT) $(DISCOVER_ARGS)

legacy-discover:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m paper_stm_repair_loop.discover $(DISCOVER_ARGS)

legacy-discover-test:
	PYTHONPATH=$(DISCOVER_PYTHONPATH) python -m pytest -q \
		project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/agent_loop/tests
