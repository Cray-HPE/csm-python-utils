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
Basic sniff test of csm-utils
"""
from typing import Type, Union

import csm_utils


class base_test_cp:
    """ base class """
    def __init__(self) -> None:
        """ Initialize internal counter to 0 """
        self._cp_calls = 0

    @property
    def cp_calls(self) -> int:
        """ Return _cp_calls counter """
        return self._cp_calls


@csm_utils.typing_imports.final
class test_rw_cp(base_test_cp):
    """ Test rw-cached properties """
    @csm_utils.cached_property.cached_property
    def cp(self) -> int:
        """ Increment cp_calls then always return 5 """
        self._cp_calls += 1
        return 5


@csm_utils.typing_imports.final
class test_ro_cp(base_test_cp):
    """ Test ro-cached properties """
    @csm_utils.readonly_cached_property.cached_property
    def cp(self) -> int:
        """ Increment cp_calls then always return 57 """
        self._cp_calls += 1
        return 57


def int_func(i: int) -> str:
    """
    Convert int arg to string
    This function exists so we can verify that
    mypy realizes the cached property is an int
    """
    return str(i)


def test_cached_property(
    tcp_class: Union[Type[test_ro_cp], Type[test_rw_cp]],
    expected_value: int
) -> None:
    """ Test cached_property and readonly_cached_property """
    tcp = tcp_class()
    readonly = isinstance(tcp, test_ro_cp)

    # Call count should initially be 0
    assert tcp.cp_calls == 0

    first_access = tcp.cp
    # Now count should be 1
    assert tcp.cp_calls == 1
    assert first_access == expected_value

    # Make sure mypy does not complain about this
    int_func(first_access)

    second_access = tcp.cp
    # An additional call to the property should hit the cache, so
    # count should still be 1
    assert tcp.cp_calls == 1

    # And just as a sanity check, make sure that we got the right value
    assert second_access == expected_value

    try:
        tcp.cp = 10
        if readonly:
            # We should never get here
            assert False, "We were able to write to the read-only cached property"
        else:
            expected_value = 10
    except AttributeError:
        if not readonly:
            assert False, "Not able to write to readwrite property"

    # Count should still be 1
    assert tcp.cp_calls == 1

    # Make sure the value is as expected_value
    assert tcp.cp == expected_value

    # Count should still be 1
    assert tcp.cp_calls == 1


def main() -> None:
    """ Run test """
    test_cached_property(test_rw_cp, 5)
    test_cached_property(test_ro_cp, 57)
    print("No errors!")


if __name__ == '__main__':
    main()
