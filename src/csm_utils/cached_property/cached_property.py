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
Parameterizable cached_property decorator for use < Python 3.9.
In 3.8, functools.cached_property existed but was not paramaterizable.
Before that, we have to use backports.cached_property, which is also
not parameterizable.
"""

# Standard imports
import sys
from typing import (
    TYPE_CHECKING,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    overload,
)

from csm_utils.typing_imports import Self

if sys.version_info < (3, 8):
    # <= Python 3.7
    from backports.cached_property import cached_property as _cp
else:
    # Python 3.8 (or later, theoretically, but this is only intended
    # for Python < 3.9
    from functools import cached_property as _cp


_S = TypeVar("_S")
_T = TypeVar("_T")


class cached_property(_cp, Generic[_T]):
    """
    This wrapper around cached_property is to make it
    paramaterized by type, like the official one
    in functools starting in Python 3.9

    Note that the class is just an empty wrapper except
    in the context of type-checking, since we don't
    actually want to change the underlying implementation -- we
    only want to make its type signature parameterizable.
    """
    if TYPE_CHECKING:
        # The type signatures below are chosen deliberately to match
        # how mypy interprets functools.cached_property in Python 3.9+
        # We have to calm pylint down on a few things, since this code is not
        # present at runtime, and is just to help mypyp
        def __init__(self, func: Callable[[_S], _T]) -> None: ...  # pylint: disable=super-init-not-called

        # mypy complains that our type signatures conflict with the
        # parent class, but we already know this -- if the parent class
        # was typed the way we wanted, none of this would be
        # necessary
        @overload  # type: ignore[override]
        def __get__(  # pylint: disable=signature-differs
            self,
            instance: None,
            owner: Type[_S],
        ) -> Self: ...  # pylint: disable=signature-differs

        @overload
        def __get__(  # pylint: disable=signature-differs
            self,
            instance: _S,
            owner: Optional[Type[_S]]
        ) -> _T: ...  # pylint: disable=signature-differs

        def __get__(self, instance, owner=None): ...
