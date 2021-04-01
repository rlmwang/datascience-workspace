#################################################################################
# GLOBALS                                                                       #
#################################################################################

VER = temp
PWD = `pwd`

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = datascience

DOCKER_FILE_DEV = .docker/develop.dockerfile
DOCKER_FILE_PRD = .docker/production.dockerfile
DOCKER_FILE_FIN = .docker/release.dockerfile

DOCKER_DEV = $(PROJECT_NAME)-dev
DOCKER_PRD = $(PROJECT_NAME)-prd
DOCKER_FIN = $(PROJECT_NAME)

JUPYTER_PORT = 8888


#################################################################################
# PROJECT COMMANDS                                                              #
#################################################################################




#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Release
release: .docker/image-prd
	rm -f release*.tar
	docker build -t $(DOCKER_FIN):$(VER) -f $(DOCKER_FILE_FIN) .
	docker save $(DOCKER_FIN):$(VER) > release_$(VER).tar
.PHONY: release


## Build dataset from source
data:
	python $(PROJECT_NAME)/build_data.py data/source data/external data/processed
.PHONY: data


## Remove compiled Python files
clean:
	find . -type f -name "*.py[cod]" -delete
	find . -type d -name "__pycache__" -delete
.PHONY: clean


## Format using black and isort
format:
	black .
	isort .
.PHONY: format


## Lint using flake8 and mypy
lint:
	flake8 .
	mypy .
.PHONY: lint


## Run unit test cases
test: 
	python -m unittest discover
.PHONY: test


## Set up conda environment
conda:
	conda env create --force --file environment_dev.yaml
.PHONY: conda


## Build development docker image
.docker/image-dev: $(DOCKER_FILE_DEV) .dockerignore
	docker build -t $(DOCKER_DEV) -f $(DOCKER_FILE_DEV) .
	touch .docker/image-dev


## Run development docker container
docker-dev: .docker/image-dev
	docker run -it --rm \
		--volume $(PWD):/work \
		--publish $(JUPYTER_PORT):$(JUPYTER_PORT) \
		--name $(DOCKER_DEV) $(DOCKER_DEV)
.PHONY: docker-dev


## Build production docker image
.docker/image-prd:
	docker build -t $(DOCKER_PRD) -f $(DOCKER_FILE_PRD) .
.PHONY: .docker/image-prd


## Run production docker container
docker-prd: .docker/image-prd
	docker run -it --rm --name $(DOCKER_PRD) $(DOCKER_PRD)
.PHONY: docker-prd


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
