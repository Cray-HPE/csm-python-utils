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

import csm_utils


class test_cp:
    """ Test cached_property """
    def __init__(self) -> None:
        """ Initialize internal counter to 0 """
        self.harf_calls = 0

    @csm_utils.cached_property.cached_property
    def harf(self) -> int:
        """ Increment harf_calls then always return 5 """
        self.harf_calls += 1
        return 5


def int_func(i: int) -> str:
    """
    Convert int arg to string
    This function exists so we can verify that
    mypy realizes the cached property is an int
    """
    return str(i)


def main() -> None:
    """ Run test """
    tcp = test_cp()

    # harf_calls should initially be 0
    assert tcp.harf_calls == 0

    xvar = tcp.harf
    # Now harf calls should be 1
    assert tcp.harf_calls == 1

    xvar_str = int_func(xvar)
    # Make sure we are getting the right value
    assert xvar_str == "5"

    yvar = tcp.harf
    # An additional call to the property should hit the cache, so
    # harf_calls should still be 1 after that
    assert tcp.harf_calls == 1

    # And just as a sanity check, make sure that we got the same value
    assert yvar == xvar

    # This is not a read-only cached property, so let's check that too
    tcp.harf = 10
    zvar = tcp.harf
    # The harf_count should still be 1, and zvar should be 10
    assert tcp.harf_calls == 1
    assert zvar == 10

    print("No errors!")


if __name__ == '__main__':
    main()
