#
# MIT License
#
# (C) Copyright 2026 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# If you wish to perform a local build, you will need to clone or copy the contents of the
# cms-meta-tools repo to ./cms_meta_tools

NAME ?= csm-utils
MOD_NAME ?= $(echo $NAME | tr - _)
PKG_VERSION := $(cat .version)
PYTHON_BIN := python$(PY_VERSION)
PYLINT_VENV_BASE_DIR ?= pylint-venv
PYLINT_VENV ?= $(PYLINT_VENV_BASE_DIR)/$(PY_VERSION)
PYLINT_VENV_PYBIN ?= $(PYLINT_VENV)/bin/python3
PIP_INSTALL_ARGS ?= --no-cache --trusted-host artifactory.algol60.net --extra-index-url http://artifactory.algol60.net/artifactory/csm-python-modules/simple
WHEEL ?= $(MOD_NAME)-$(PKG_VERSION)-py3-none-any.whl

all : runbuildprep lint pymod
pymod: pymod_build pymod_validate
pymod_build: pymod_build_prep pymod_build_package
pymod_validate: pymod_validate_setup pymod_validate_pylint_error pymod_validate_pylint_full pymod_validate_mypy

runbuildprep:
		./cms_meta_tools/scripts/runBuildPrep.sh

lint:
		./cms_meta_tools/scripts/runLint.sh

pymod_build_prep:
		rm -rf ./dist || true
		$(PYTHON_BIN) --version
		$(PYTHON_BIN) -m pip install --upgrade --user pip build setuptools wheel

pymod_build_package:
		$(PYTHON_BIN) -m build --sdist .
		$(PYTHON_BIN) -m build --wheel .

pymod_validate_setup:
		$(PYTHON_BIN) --version
		mkdir -p $(PYLINT_VENV_BASE_DIR)
		$(PYTHON_BIN) -m venv $(PYLINT_VENV)
		$(PYLINT_VENV_PYBIN) -m pip install --upgrade $(PIP_INSTALL_ARGS) pip
		$(PYLINT_VENV_PYBIN) -m pip install --disable-pip-version-check $(PIP_INSTALL_ARGS) \
			dist/$(WHEEL) \
			$(MOD_NAME)[lint] \
			$(MOD_NAME)[type_check]
		$(PYLINT_VENV_PYBIN) -m pip list --format freeze

pymod_validate_pylint_error:
		$(PYLINT_VENV_PYBIN) -m pylint --errors-only $(MOD_NAME)

pymod_validate_pylint_full:
		$(PYLINT_VENV_PYBIN) -m pylint --fail-under 9 $(MOD_NAME)

pymod_validate_mypy:
		# --no-incremental --cache-dir=/dev/null --no-sqlite-cache
		#    Avoid creating and reading mypy cache
		# --show-traceback
		#    Include context if mypy crashes
		$(PYLINT_VENV_PYBIN) -m mypy \
			--no-incremental \
			--cache-dir=/dev/null \
			--no-sqlite-cache \
			--show-traceback \
			-p $(MOD_NAME)
