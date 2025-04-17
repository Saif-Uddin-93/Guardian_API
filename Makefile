#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = guardian_api
REGION = eu-west-2
PYTHON_INTERPRETER = python
SHELL := /bin/bash
WD=$(shell pwd)
# PYTHONPATH=$(shell echo $PYTHONPATH | cut -d':' -f1)
PYTHONPATH=${WD}

PROFILE = default
PIP:=pip

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> Setting up VirtualEnv."
	( \
		python -m venv venv; \
	)
	@echo ">>> Activate VirtualEnv."
	( \
		$(ACTIVATE_ENV); \
	)

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
		cd $(PYTHONPATH)/; \
		rm -rf utility_layer.zip; \
		rm -rf ./python/lib/python3.13/site-packages/utility/; \
		mkdir -p ./python/lib/python3.13/site-packages/; \
		cp -r utility/ ./python/lib/python3.13/site-packages/; \
		zip -r utility_layer.zip python; \
	)


run-destroy:
	@echo ">>> Running terraform destroy..."
	( \
		cd $(PYTHONPATH)/terraform/; \
		terraform destroy -auto-approve; \
	)


run-init:
	@echo ">>> Running terraform init..."
	( \
		cd $(PYTHONPATH)/terraform/; \
		terraform init; \
	)


run-plan:
	@echo ">>> Running terraform plan..."
	( \
		cd $(PYTHONPATH)/terraform/; \
		terraform plan; \
	)


run-apply:
	@echo ">>> Running terraform apply..."
	( \
		cd $(PYTHONPATH)/terraform/; \
		terraform apply -auto-approve; \
	)


run-terraform: layer-utility run-init run-destroy run-plan run-apply
	@echo ">>> About to run all terraform tasks..."


git:
	@echo ">>> adding files to github with message"
	( \
		cd $(PYTHONPATH)/; \
		git commit -am '$(m)'; \
	)
	@echo ">>> pushing files to github"
	( \
		cd $(PYTHONPATH)/; \
		git push; \
	)


add-aws-cred:
	@echo ">>> Setting up AWS credentials..."
	( \
		echo "[default]" > ~/.aws/credentials; \
		echo "aws_access_key_id = $(aws-id)" >> ~/.aws/credentials; \
		echo "aws_secret_access_key = $(aws-key)" >> ~/.aws/credentials; \
	)


show-aws-cred:
	@echo ">>> AWS credentials are set up in ~/.aws/credentials"
	( \
		cat ~/.aws/credentials; \
	)


print-variables:
	@echo ">>> PYTHONPATH is set to: $(PYTHONPATH)"
	@echo ">>> Current working directory is: $(WD)"
	@echo ">>> Current shell is: $(SHELL)"
	@echo ">>> Current profile is: $(PROFILE)"
	@echo ">>> Current region is: $(REGION)"
	@echo ">>> Current python interpreter is: $(PYTHON_INTERPRETER)"
	@echo ">>> Current pip is: $(PIP)"