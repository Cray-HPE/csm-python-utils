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
duration_to_timedelta function
"""

# Standard imports
import datetime
from typing import Optional

from .defaults import (
    DEFAULT_STR_UNIT_MAP,
    DEFAULT_TD_FUNC_MAP,
)
from .parse_timestamp_by_pattern import parse_timestamp_by_pattern
from .type_aliases import (
    ParseTimestampFunc,
    StrUnitMap,
    TDFuncMap,
)


def duration_to_timedelta(
    timestamp: str,
    parse_timestamp: Optional[ParseTimestampFunc] = None,
    str_unit_map: Optional[StrUnitMap] = None,
    td_func_map: Optional[TDFuncMap] = None,
) -> datetime.timedelta:
    """
    Converts a str to a timedelta object:

    1. Calls parse_timestamp function on the timestamp to split it into
       a float value (representing the amount of time) and a string value
       (representing the units of time). For example, by default
       this would parse '90m' and return 90, 'm'

    2. Converts the string by using the str_to_unit map. For example, by
       default this would convert 'm' to 'minutes'.

    4. Looks up the correct time_delta conversion function for these
       units in td_func_map. For example, by default, for 'minutes' it would
       call datetime.timedelta(minutes=<amount of time from step 1>)

    5. Call the function and return the result.
    """
    if parse_timestamp is None:
        parse_timestamp = parse_timestamp_by_pattern
    if str_unit_map is None:
        str_unit_map = DEFAULT_STR_UNIT_MAP
    if td_func_map is None:
        td_func_map = DEFAULT_TD_FUNC_MAP
    time_amount_float, raw_units_str = parse_timestamp(timestamp)

    # Use the str_unit_map to convert the string in the timestamp into
    # the actual units
    try:
        units = str_unit_map[raw_units_str]
    except KeyError as err:
        raise ValueError(f"Invalid unit string in timestamp: '{raw_units_str}'") from err

    try:
        td_func = td_func_map[units]
    except KeyError as err:
        raise ValueError(f"Unsupported time units: '{units}'") from err

    return td_func(time_amount_float)
