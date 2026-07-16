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

"""
IntervalTimer class
"""

import logging
import os
import time
from typing import Callable, Optional, Union


LOGGER = logging.getLogger(__name__)
DEFAULT_MAX_SLEEP_SECONDS = 60


class IntervalTimer:
    """
    Used to track when an interval has elapsed, based on the time the
    last interval started and the interval_duration value
    """

    def __init__(
        self,
        get_interval_duration: Callable[[], Union[int, float]],
        max_sleep_seconds: Union[int, float] = DEFAULT_MAX_SLEEP_SECONDS,
    ):
        self._last_interval_time: Optional[float] = None
        self._max_sleep_seconds = max_sleep_seconds
        self._get_interval_duration = get_interval_duration

    def _calculate_time_remaining(self) -> float:
        """
        If we have never completed an interval before (meaning last_interval_time is None),
        then we should do so now --> return 0.
        Otherwise, the time remaining is equal to the interval duration - time elapsed.
        This function returns the maximum of that value and 0, so that 0 is returned if the
        interval has been exceeded.
        """
        if self._last_interval_time is None:
            return 0
        # The time elapsed is equal to the current time - last_interval_complete_time
        time_elapsed = time.monotonic() - self._last_interval_time
        # Return 0 if we have exceeded the interval duration
        return max(self._get_interval_duration() - time_elapsed, 0)

    def wait_for_interval(self) -> None:
        """
        Sleep until the interval duration has elapsed
        """
        while (time_remaining := self._calculate_time_remaining()) > 0:
            # Sleep up to max_sleep_seconds seconds
            time.sleep(min(self._max_sleep_seconds, time_remaining))
        self._last_interval_time = time.monotonic()


def get_max_sleep_seconds(
    default_max_sleep_seconds: Union[float, int] = DEFAULT_MAX_SLEEP_SECONDS,
    min_max_sleep_seconds: Union[float, int] = 5,
    max_sleep_seconds_env_var_name: Optional[str] = None,
) -> Union[float, int]:
    """
    Return the max_sleep_seconds value based on the specified parameters
    """
    max_sleep_seconds: Optional[Union[float, int]] = None
    if max_sleep_seconds_env_var_name is not None:
        try:
            max_sleep_seconds = float(os.environ[max_sleep_seconds_env_var_name])
            LOGGER.info(
                "%s environment variable = '%s'",
                max_sleep_seconds_env_var_name,
                max_sleep_seconds
            )
        except KeyError:
            LOGGER.info(
                "%s environment variable not set",
                max_sleep_seconds_env_var_name,
            )
        except ValueError as exc:
            LOGGER.warning(
                "Invalid %s environment variable (%s)",
                max_sleep_seconds_env_var_name,
                exc,
            )

    if max_sleep_seconds is None:
        max_sleep_seconds = default_max_sleep_seconds
        LOGGER.info("Using default max_sleep_seconds value: '%s'", default_max_sleep_seconds)

    if max_sleep_seconds >= min_max_sleep_seconds:
        return max_sleep_seconds

    LOGGER.warning(
        "max_sleep_seconds value (%s) too low, using '%s' instead",
        max_sleep_seconds,
        min_max_sleep_seconds,
    )
    return min_max_sleep_seconds
