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
compact_response_text class
"""

# Standard imports
import re
# Use deprecated Match, Pattern aliases for backwards compatability
from typing import ClassVar, Match, Optional, Pattern


class compact_response_text:
    """
    Often JSON is "pretty printed" in response text, which is undesirable for our logging.
    This callable class transforms the response text into a single line, stripping leading and
    trailing whitespace from each line, and then returns it. It uses iterators for this,
    to limit memory use when handling large responses. It is implemented as a class because
    this is used with logging, and by implementing the logic in the __str__ method, this
    prevents it from being run at all when the logging level would not require it.
    """
    _SPLIT_PAT: ClassVar[Pattern[str]] = re.compile(r'([^\n]+)(?:$|\n)')

    def __init__(self, response_text: Optional[str]) -> None:
        self._response_text = response_text

    @property
    def response_text(self) -> str:
        """ Return the response text string, or 'None' """
        return self._response_text if self._response_text is not None else "None"

    @classmethod
    def _match_group_one(cls, match_object: Match[str]) -> str:
        """
        Helper function for map iterator inside compact_response_text.
        This gets the first match group, strips the leading and trailing whitespace,
        and returns it
        """
        # There are evidently some weird edge cases regarding the return type of Match.group
        # https://github.com/python/typeshed/issues/12090
        # Thus, if we don't get back a string, we just return an empty string
        g1 = match_object.group(1)
        if isinstance(g1, str):
            return g1.strip()
        return ""

    def __str__(self) -> str:
        """
        finditer returns an iterator of match objects -- returning each instance matching
        the _SPLIT_PAT pattern.
        Creating a map of the _match_group_one method onto this iterator
        acts like an iterable version of the string split() method, called with \n as its
        argument. The one difference is that the _match_group_one method also does a strip()
        on the result.
        Any non-empty lines that come out of the above pipeline are joined by whitespace
        and returned.
        """
        return ' '.join(
            line for line in map(self._match_group_one,
                                 self._SPLIT_PAT.finditer(self.response_text)) if line
        )
