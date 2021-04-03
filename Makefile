SHELL = /bin/sh
#################################################################################
# GLOBALS                                                                       #
#################################################################################

NAME = datascience
VER = temp

GID = $$(id -g)
UID = $$(id -u)

PWD = $$PWD
PORT = 5000

DOCKER_FILE_DEV = .docker/develop.dockerfile
DOCKER_FILE_PRD = .docker/production.dockerfile
DOCKER_FILE_FIN = .docker/release.dockerfile

DOCKER_DEV = $(NAME)-dev
DOCKER_PRD = $(NAME)-prd
DOCKER_FIN = $(NAME)

VOLUME = $$HOME/docker/$(NAME)


#################################################################################
# PROJECT COMMANDS                                                              #
#################################################################################




#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Build release version of project
release: .docker/image-prd
	rm -f datascience*.tar
	docker build -t $(DOCKER_FIN):$(VER) -f $(DOCKER_FILE_FIN) .
	docker save $(DOCKER_FIN):$(VER) > $(NAME)_$(VER).tar
.PHONY: release


## Build dataset from source data
data:
	cd data/ && $(MAKE) all
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


## Run unit-test cases
test: 
	python -m unittest discover
.PHONY: test


## Setup conda environments (dev & prd)
conda:
	conda env create --force --file requirements_dev.yaml
	conda env create --force --file requirements_prd.yaml
.PHONY: conda


## Build docker image for development
.docker/image-dev: $(DOCKER_FILE_DEV) .dockerignore
	docker build \
		--build-arg GID=$(GID) \
		--build-arg UID=$(UID) \
		-t $(DOCKER_DEV) \
		-f $(DOCKER_FILE_DEV)\
		$(PWD)
	touch .docker/image-dev


## Build docker image for production
.docker/image-prd: $(DOCKER_FILE_PRD) .dockerignore
	docker build \
		--build-arg GID=$(GID) \
		--build-arg UID=$(UID) \
		-t $(DOCKER_PRD) \
		-f $(DOCKER_FILE_PRD) \
		$(PWD)
.PHONY: .docker/image-prd


## Run docker container for development
docker-dev: .docker/image-dev | $(VOLUME)
	@echo "$(GID)"
	docker run -it --rm \
		--volume $(PWD):/work \
		--volume $(VOLUME):/work/share \
		--publish $(PORT):5000 \
		--name $(DOCKER_DEV) \
		$(DOCKER_DEV)
.PHONY: docker-dev


## Run docker container for production
docker-prd: .docker/image-prd | $(VOLUME)
	docker run -it --rm \
		--name $(DOCKER_PRD) \
		--volume $(VOLUME):/work/share \
		--publish $(PORT):5000
		$(DOCKER_PRD)
.PHONY: docker-prd


## Run docker container for release
docker: release | $(VOLUME)
	
	docker run -it --rm \
		--name $(DOCKER_FIN) \
		--volume $(VOLUME):/work/share \
		--publish $(PORT):5000 \
		$(DOCKER_FIN):$(VER)

.PHONY: docker


## Setup docker volume permissions on host
$(VOLUME):
	mkdir -p $(VOLUME)/inputs $(VOLUME)/output


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
