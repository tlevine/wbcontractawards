import os

import nose.tools as n

import wbcontractawards.parse as p

def test_OP00027656():
    with open(os.path.join('wbcontractawards','test','fixtures','OP00027656.txt')) as fp:
        text = fp.read()
    observed = list(p.bidders(text))
    with open(os.path.join('wbcontractawards','test','fixtures','OP00027656.py'), 'w') as fp:
        fp.write(str(observed))
   #n.assert_list_equal(, [])
