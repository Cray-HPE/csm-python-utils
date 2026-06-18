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
    """ Test cached properties """
    def __init__(self) -> None:
        """ Initialize internal counters to 0 """
        self.cprw_calls = 0
        self.cpro_calls = 0

    @csm_utils.cached_property.cached_property
    def cprw(self) -> int:
        """ Increment cprw_calls then always return 5 """
        self.cprw_calls += 1
        return 5

    @csm_utils.readonly_cached_property.cached_property
    def cpro(self) -> int:
        """ Increment cpro_calls then always return 57 """
        self.cpro_calls += 1
        return 57


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
    # Both call counts should initially be 0
    assert tcp.cpro_calls == 0
    assert tcp.cprw_calls == 0

    x_rw = tcp.cprw
    # Now cprw calls should be 1, cpro should be 0
    assert tcp.cpro_calls == 0
    assert tcp.cprw_calls == 1

    x_ro = tcp.cpro
    # Now both should be 1
    assert tcp.cpro_calls == 1
    assert tcp.cprw_calls == 1

    x_ro_str = int_func(x_ro)
    # Make sure we are getting the right value
    assert x_ro_str == "57"

    x_rw_str = int_func(x_rw)
    # Make sure we are getting the right value
    assert x_rw_str == "5"

    y_ro = tcp.cpro
    # An additional call to the property should hit the cache, so
    # both counts should still be 1
    assert tcp.cpro_calls == 1
    assert tcp.cprw_calls == 1

    y_rw = tcp.cprw
    # An additional call to the property should hit the cache, so
    # both counts should still be 1
    assert tcp.cpro_calls == 1
    assert tcp.cprw_calls == 1

    # And just as a sanity check, make sure that we got the same values
    assert y_ro == x_ro
    assert y_rw == x_rw

    # cprw is not a read-only cached property, so let's check that too
    tcp.cprw = 10
    z_rw = tcp.cprw
    # The counts should still be 1, and z_rw should be 10
    assert tcp.cpro_calls == 1
    assert tcp.cprw_calls == 1
    assert z_rw == 10

    # cpro is read-only, so we should get an AttributeError if we try to set it
    try:
        tcp.cpro = 10
        # We should never get here
        assert False, "We were able to write to the read-only cached property"
    except AttributeError:
        pass

    # The counts should still be 1
    assert tcp.cpro_calls == 1
    assert tcp.cprw_calls == 1

    assert tcp.cpro == 57

    # The counts should still be 1
    assert tcp.cpro_calls == 1
    assert tcp.cprw_calls == 1

    print("No errors!")


if __name__ == '__main__':
    main()
