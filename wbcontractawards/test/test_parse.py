import os

import nose.tools as n
n.assert_dict_equal.__self__.maxDiff = None

import wbcontractawards.parse as p

def test_OP00027656():
    from wbcontractawards.test.fixtures.OP00027656 import text, expected
    observed = list(p.bidders(text))
    n.assert_list_equal(observed, expected)
