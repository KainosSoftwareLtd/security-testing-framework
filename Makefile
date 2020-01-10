all: help

build:
	@echo "Building docker container..."
	@./bin/build-docker.sh

attack: build
	@echo "Run attacks"
	@./bin/attack.sh

interactive:
	@docker run --rm -it --entrypoint /bin/bash security-testing-framework

help:
	@echo "the help menu"
	@echo "  make build"
	@echo "  make help"
	@echo "  make interactive"

.PHONY: build clean
