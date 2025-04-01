#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = guardian_api_testing
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
# ( \
#     $(PIP) install -q virtualenv virtualenvwrapper; \
#     virtualenv venv --python=$(PYTHON_INTERPRETER); \
# )

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements:# create-environment
	$(call execute_in_env, $(PIP) install pip-tools)
	$(call execute_in_env, pip-compile requirements.in)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Set up dev requirements (bandit, safety, black)
dev-setup: bandit safety black coverage

# Build / Run

## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black:
	$(call execute_in_env, black  ./src/*/*.py ./test/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -vv --testdox)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src test/)

## Run all checks
run-checks: security-test run-black unit-test check-coverage


layer-utility:
	@echo ">>> creating utility layer"
	( \
		cd ~/Documents/github/Guardian_API/; \
		rm -rf utility_layer.zip; \
		rm -rf ./python/lib/python3.13/site-packages/utility/; \
		cp -r utility/ ./python/lib/python3.13/site-packages/; \
		zip -r utility_layer.zip python; \
	)


run-destroy:
	@echo ">>> Running terraform destroy..."
	( \
		cd ~/Documents/github/Guardian_API/terraform/; \
		terraform destroy -auto-approve; \
	)


run-init:
	@echo ">>> Running terraform init..."
	( \
		cd ~/Documents/github/Guardian_API/terraform/; \
		terraform init; \
	)


run-plan:
	@echo ">>> Running terraform plan..."
	( \
		cd ~/Documents/github/Guardian_API/terraform/; \
		terraform plan; \
	)


run-apply:
	@echo ">>> Running terraform apply..."
	( \
		cd ~/Documents/github/Guardian_API/terraform/; \
		terraform apply -auto-approve; \
	)


run-terraform: layer-utility run-destroy run-init run-plan run-apply
	@echo ">>> About to run all terraform tasks..."


git:
	@echo ">>> adding files to github with message"
	( \
		cd ~/Documents/github/Guardian_API/; \
		git commit -am '$(m)'; \
	)
	@echo ">>> pushing files to github"
	( \
		cd ~/Documents/github/Guardian_API/; \
		git push; \
	)
