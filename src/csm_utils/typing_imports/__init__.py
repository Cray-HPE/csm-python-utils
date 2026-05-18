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
Centralized place for Python-version-dependent imports
(to simplify the rest of the files)

This assumes Python 3.6+
"""

import sys


# AsyncGenerator, ChainMap, Counter, Deque added to typing in 3.6.1
# Deprecated in 3.9 when collections.ChainMap/Counter/etc became subscriptable
# Same for collections.abc.AsyncGenerator
if sys.version_info >= (3, 9):
    # Python 3.9+
    from collections import (
        ChainMap,
        Counter,
    )
    from collections import deque as Deque
    from collections.abc import AsyncGenerator
elif sys.version_info >= (3, 6, 1):
    # >= Python 3.6.1, < Python 3.9
    from typing import (
        AsyncGenerator,
        ChainMap,
        Counter,
        Deque,
    )
else:
    # < Python 3.6.1
    from typing_extensions import (
        AsyncGenerator,
        ChainMap,
        Counter,
        Deque,
    )


# NoReturn added to typing in 3.6.2
if sys.version_info >= (3, 6, 2):
    # Python 3.6.2+
    from typing import NoReturn
else:
    # < Python 3.7
    from typing_extensions import NoReturn


# AsyncContextManager added to typing in 3.6.2
# typing.AsyncContextManager deprecated in 3.9 when
# contextlib.AbstractAsyncContextManager became subscriptable
if sys.version_info >= (3, 9):
    # Python 3.9+
    from contextlib import AbstractAsyncContextManager
elif sys.version_info >= (3, 6, 2):
    # >= Python 3.6.2, < Python 3.9
    from typing import AsyncContextManager as AbstractAsyncContextManager
else:
    # < Python 3.6.2
    from typing_extensions import AsyncContextManager as AbstractAsyncContextManager


# OrderedDict added to typing in 3.7.2
# deprecated in favor of collections.OrderedDict in 3.9
if sys.version_info >= (3, 9):
    # Python 3.9+
    from collections import OrderedDict
elif sys.version_info >= (3, 7, 2):
    # Python 3.7.2+ or 3.8
    from typing import OrderedDict
else:
    # < Python 3.7.2
    from typing_extensions import OrderedDict


# Literal, Protocol, TypedDict, final, Final, runtime_checkable added to typing in 3.8
if sys.version_info >= (3, 8):
    # Python 3.8+
    from typing import (
        Final,
        Literal,
        Protocol,
        TypedDict,
        final,
        runtime_checkable,
    )
else:
    # < Python 3.8
    from typing_extensions import (
        Final,
        Literal,
        Protocol,
        TypedDict,
        final,
        runtime_checkable,
    )


# Annotated added to typing in 3.9
# Prior to 3.9 there was no way to distinguish between built-in sets and set collections,
# when using parameterized type hints.
if sys.version_info >= (3, 9):
    # Python 3.9+
    from collections.abc import Set as SetCollection
    from typing import Annotated
else:
    # < Python 3.9
    from typing import Set as SetCollection
    from typing_extensions import Annotated


# Concatenate, ParamSpec*, TypeAlias, TypeGuard, is_typeddict added to typing in 3.10
if sys.version_info >= (3, 10):
    # Python 3.10+
    from typing import (
        Concatenate,
        ParamSpec,
        ParamSpecArgs,
        ParamSpecKwargs,
        TypeAlias,
        TypeGuard,
        is_typeddict,
    )
else:
    # < Python 3.10
    from typing_extensions import (
        Concatenate,
        ParamSpec,
        ParamSpecArgs,
        ParamSpecKwargs,
        TypeAlias,
        TypeGuard,
        is_typeddict,
    )


# LiteralString, Never, NotRequired, Required, Self, TypeVarTuple, Unpack,
# assert_never, dataclass_transform, reveal_type added to typing in 3.11
if sys.version_info >= (3, 11):
    # Python 3.11+
    from typing import (
        LiteralString,
        Never,
        NotRequired,
        Required,
        Self,
        TypeVarTuple,
        Unpack,
        assert_never,
        dataclass_transform,
        reveal_type,
    )
else:
    # < Python 3.11
    from typing_extensions import (
        LiteralString,
        Never,
        NotRequired,
        Required,
        Self,
        TypeVarTuple,
        Unpack,
        assert_never,
        dataclass_transform,
        reveal_type,
    )


# Explicitly re-export
__all__ = [
    "AbstractAsyncContextManager",
    "Annotated",
    "AsyncGenerator",
    "ChainMap",
    "Concatenate",
    "Counter",
    "Deque",
    "Final",
    "Literal",
    "LiteralString",
    "Never",
    "NoReturn",
    "NotRequired",
    "OrderedDict",
    "ParamSpec",
    "ParamSpecArgs",
    "ParamSpecKwargs",
    "Protocol",
    "Required",
    "Self",
    "SetCollection",
    "TypeAlias",
    "TypeGuard",
    "TypeVarTuple",
    "TypedDict",
    "Unpack",
    "assert_never",
    "dataclass_transform",
    "final",
    "is_typeddict",
    "reveal_type",
    "runtime_checkable",
]


# After this point, we add in exports that are completely unavailable
# in some earlier Python versions. Attempts to import them on such
# versions will (and should) fail


# Add imports available back to Python 3.7, but not earlier
if sys.version_info >= (3, 7):
    if sys.version_info >= (3, 13):
        # Python 3.13+
        from typing import (
            get_protocol_members,
            is_protocol,
        )
    else:
        # Python 3.7 - 3.12
        from typing_extensions import (
            get_protocol_members,
            is_protocol,
        )

    if sys.version_info >= (3, 12):
        # Python 3.12+
        from typing import (
            TypeAliasType,
            override,
        )
    else:
        # Python 3.7 - 3.11
        from typing_extensions import (
            TypeAliasType,
            override,
        )

    if sys.version_info >= (3, 11):
        # Python 3.11+
        from typing import (
            assert_type,
            clear_overloads,
            get_overloads,
        )
    else:
        # Python 3.7 - 3.10
        from typing_extensions import (
            assert_type,
            clear_overloads,
            get_overloads,
        )

    if sys.version_info >= (3, 8):
        # Python 3.8+
        from typing import (
            SupportsIndex,
            get_args,
            get_origin,
        )
    else:
        # Python 3.7
        from typing_extensions import (
            SupportsIndex,
            get_args,
            get_origin,
        )

    __all__.extend([
        "SupportsIndex",
        "TypeAliasType",
        "assert_type",
        "clear_overloads",
        "get_origin",
        "get_args",
        "get_overloads",
        "get_protocol_members",
        "is_protocol",
        "override"
    ])


# Add imports available back to Python 3.8, but not earlier
if sys.version_info >= (3, 8):
    if sys.version_info >= (3, 14):
        # Python 3.14+
        from typing import evaluate_forward_ref
    else:
        # Python 3.8 - 3.13
        from typing_extensions import evaluate_forward_ref

    if sys.version_info >= (3, 13):
        # Python 3.13+
        from typing import (
            NoDefault,
            ReadOnly,
            TypeIs,
        )
    else:
        # Python 3.8 - 3.12
        from typing_extensions import (
            NoDefault,
            ReadOnly,
            TypeIs,
        )

    __all__.extend([
        "NoDefault",
        "ReadOnly",
        "TypeIs",
        "evaluate_forward_ref"
    ])
