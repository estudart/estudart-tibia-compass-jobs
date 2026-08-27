.PHONY: deploy build

deploy:
	./deploy.sh

# Usage: make build JOB=creatures-job
build:
	./build.sh $(JOB)
