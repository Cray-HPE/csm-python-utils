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
"""Nox definitions for linting, type checks, and tests"""

from __future__ import absolute_import
from typing import Optional
import nox  # pylint: disable=import-error

PYTHON = ["3"]

INSTALL_ARGS = [ "csm-utils", "--find-links", "./dist" ]

def install(session, keyword: Optional[str] = None) -> None:
    """
    Install csm-utils and (optionally) csm-utils[keyword] from ./dist
    """
    if keyword:
        session.install(f"csm-utils[{keyword}]", *INSTALL_ARGS)
    else:
        session.install(*INSTALL_ARGS)

@nox.session(python=PYTHON)
def lint(session):
    """Run linters.
    Run Pylint against src and tests.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    install(session, "lint")
    session.run("pip","list","--format","freeze")
    session.log("Running pylint...")
    session.run("pylint", "--rcfile=.pylintrc", "csm_utils")
    session.log("Running pylint on test.py...")
    session.run("pylint", "--rcfile=.pylintrc", "test.py")

@nox.session(python=PYTHON)
def style(session):
    """Run linters.
    Run Pycodestyle against src and tests.
    """
    install(session, "style")
    session.run("pip","list","--format","freeze")
    session.log("Running pycodestyle...")
    session.run("pycodestyle", "--config=.pycodestyle", "src")
    session.log("Running pycodestyle on test.py...")
    session.run("pycodestyle", "--config=.pycodestyle", "test.py")

@nox.session(python=PYTHON)
def type_check(session):
    """Run Mypy with config."""
    install(session, "type_check")
    session.run("pip","list","--format","freeze")
    session.log("Running mypy...")
    session.run("mypy", "--strict", "-p", "csm_utils")
    session.log("Running mypy on test.py...")
    session.run("mypy", "--strict", "test.py")
    # Make sure that changes did not break requests_retry_session, which
    # uses this module
    session.install(
        "--trusted-host",
        "artifactory.algol60.net",
        "--extra-index-url",
        "http://artifactory.algol60.net/artifactory/csm-python-modules/simple",
        "requests-retry-session",
        "requests-retry-session[type_check1]",
    )
    session.run("pip","list","--format","freeze")
    session.run("mypy", "--strict", "-p", "requests_retry_session")

@nox.session(python=PYTHON)
def sniff_test(session):
    """Run Mypy with config."""
    install(session)
    session.run("pip","list","--format","freeze")
    session.log("Running test...")
    session.run("python", "./test.py")
