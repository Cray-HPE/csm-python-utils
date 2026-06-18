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
BOS utilities used by both server and operators
"""

# Standard imports
# Use these deprecated aliases in typing for backwards-compatability
from typing import Optional, Pattern, Tuple

from .defaults import DEFAULT_TIME_DURATION_PATTERN


def parse_timestamp_by_pattern(
    timestamp: str,
    pattern: Optional[Pattern[str]] = None,
) -> Tuple[int, str]:
    """
    Use the specified regex pattern and return the two matching groups,
    converting the first to an integer
    """
    if pattern is None:
        pattern = DEFAULT_TIME_DURATION_PATTERN
    match = pattern.search(timestamp)
    if match is None:
        raise ValueError(
                f"Timestamp string does not match expected format: '{timestamp}'")
    timestr, durationstr = match.groups()
    return int(timestr), durationstr
