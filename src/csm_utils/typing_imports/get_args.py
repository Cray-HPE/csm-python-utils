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
get_args hack for Python 3.6

Not even typing_extensions has get_args in Python 3.6, so
we have to define a hack version ourselves
"""

# We do not vary these imports based on Python version, because this
# should only be used with Python 3.6
from enum import Enum
from typing import Any, List, Tuple, Union

# This try/except is mainly to make pylint happy, since it runs on
# a Python version where we do not install typing_extensions
try:
    from typing_extensions import TypeAlias
except ImportError:
    from typing import TypeAlias  # type: ignore[attr-defined, no-redef, unused-ignore]  # pylint: disable=ungrouped-imports  # noqa: E501


# These are the valid types that can be used inside a Literal (except
# for another Literal value itself, which is allowed, but not covered
# by this list)
_LiteralValue: TypeAlias = Union[bool, int, str, bytes, Enum, None]


def get_args(literal: Any) -> Tuple[_LiteralValue, ...]:
    """
    Returns the list of items used to create a literal.
    Notes:
    - This preserves the behavior of the actual get_args function
      when it comes to duplicate arguments and nested Literals.
    - This relies on how Literal is implemented internally. I have
      confirmed that it works for all versions of typing_extensions
      available for Python 3.6 that include Literal (3.7.2+).
      They no longer update typing_extensions for Python 3.6,
      so we can assume that this will not change.
    - The type signature for this function is much broader
      than it "should" be, but unfortunately there is no way to
      define it more accurately in a way that mypy will accept.
    """
    assert hasattr(literal, "__values__")
    assert isinstance(literal.__values__, tuple)
    value_list: List[_LiteralValue] = []
    for val in literal.__values__:
        if val in value_list:
            # We do not add duplicates
            continue
        if val is None:
            value_list.append(val)
            continue
        if isinstance(val, (bool, int, str, bytes, Enum)):
            value_list.append(val)
            continue
        # It is possible to have another Literal inside a Literal
        for subval in get_args(val):
            if subval not in value_list:
                value_list.append(subval)
    return tuple(value_list)
