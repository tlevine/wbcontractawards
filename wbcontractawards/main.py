import itertools

import wbcontractawards.download as d
import wbcontractawards.parse as p

def contracts():
    for os in itertools.count(0, 10):
        response = d.search(os)
        for url in p.search(response):
            response = d.get(url)
            yield p.contract(response)
