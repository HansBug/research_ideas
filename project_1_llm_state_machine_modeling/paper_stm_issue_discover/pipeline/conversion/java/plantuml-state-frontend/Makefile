PLANTUML_VERSION := 1.2024.7
PLANTUML_SHA256 := e34c12bbe9944f1f338ca3d88c9b116b86300cc8e90b35c4086b825b5ae96d24
PLANTUML_URL := https://github.com/plantuml/plantuml/releases/download/v$(PLANTUML_VERSION)/plantuml-$(PLANTUML_VERSION).jar
PLANTUML_JAR ?= $(CURDIR)/.cache/plantuml-$(PLANTUML_VERSION).jar

SRC_DIR := src/main/java
BUILD_DIR := build/classes
SOURCES := $(shell find $(SRC_DIR) -name '*.java' -type f | sort)
MAIN_CLASS := researchideas.plantuml.PlantUmlStateFrontend

.PHONY: all fetch verify compile run clean

all: compile

fetch:
	mkdir -p $(dir $(PLANTUML_JAR))
	curl -fL --retry 3 -o $(PLANTUML_JAR) $(PLANTUML_URL)

verify:
	test -f $(PLANTUML_JAR)
	printf '%s  %s\n' '$(PLANTUML_SHA256)' '$(PLANTUML_JAR)' | sha256sum -c -

compile: verify
	mkdir -p $(BUILD_DIR)
	javac -encoding UTF-8 -cp $(PLANTUML_JAR) -d $(BUILD_DIR) $(SOURCES)

run: compile
	test -n "$(SOURCE)"
	java -cp $(BUILD_DIR):$(PLANTUML_JAR) $(MAIN_CLASS) --source $(SOURCE) --example-id $(or $(EXAMPLE_ID),example)

clean:
	rm -rf build
