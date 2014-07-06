import pickle
import os

import nose.tools as n
n.assert_dict_equal.__self__.maxDiff = None

import wbcontractawards.parse as p

def test_OP00027656():
    from wbcontractawards.test.fixtures.OP00027656 import text, expected
    observed = list(p.bidders(text))
    n.assert_list_equal(observed, expected)

def test_methods():
    prc = '''
Scope of Contract: Development of a Performance Information and Management System for the Ministry of Labour and Social Protectionof the Population of Azerbaijan Republic
Method of Selection: QCBS - Quality And Cost-Based Selection
Duration of Contract: 12Month(s)
Contract Signature Date: 18-Feb-2011
'''
    expected = {
        'method.selection': 'QCBS - Quality And Cost-Based Selection',
    }
    n.assert_dict_equal(p.methods(prc), expected)

def test_OP00016891():
    from wbcontractawards.test.fixtures.OP00016891 import text, project
    n.assert_equal(p.project(text), project)

def test_OP00022874():
    from wbcontractawards.test.fixtures.OP00022874 import prc, project
    n.assert_equal(p.project(prc), project)
