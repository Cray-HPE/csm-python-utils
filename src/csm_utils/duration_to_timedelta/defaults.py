#
# MIT License
#
# (C) Copyright 2022-2026 Hewlett Packard Enterprise Development LP
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

"""
Default values used for duration_to_timedelta
"""

# Standard imports
import datetime
import re
# Use this deprecated alias in typing for backwards-compatability
from typing import Pattern

from csm_utils.typing_imports import Final

from .type_aliases import StrUnitMap, TDFuncMap

# All defaults annotated as final as they should not be changed
# in-place.

# Default re.pattern
# One or more digits followed by one or more characters
DEFAULT_TIME_DURATION_PATTERN: Final[Pattern[str]] = re.compile(r"^(\d+)(\D+)$")


DEFAULT_TD_FUNC_MAP: Final[TDFuncMap] = {
    "microseconds": lambda x: datetime.timedelta(microseconds=x),
    "milliseconds": lambda x: datetime.timedelta(milliseconds=x),
    "seconds": lambda x: datetime.timedelta(seconds=x),
    "minutes": lambda x: datetime.timedelta(minutes=x),
    "hours": lambda x: datetime.timedelta(hours=x),
    "days": lambda x: datetime.timedelta(days=x),
    "weeks": lambda x: datetime.timedelta(weeks=x),
    "fortnights": lambda x: datetime.timedelta(weeks=x*2),
}


DEFAULT_STR_UNIT_MAP: Final[StrUnitMap] = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}
