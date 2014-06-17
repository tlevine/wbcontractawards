import itertools

import wbcontractawards.download as d
import wbcontractawards.parse as p

def contracts():
    for os in itertools.count(0, 10):
        response = d.search(os)
        contract_urls = p.search(response)
        if [] == contract_urls:
            break
        for url in contract_urls:
            response = d.get(url)
            yield p.contract(response)

def cli():
    import sys, json
    for contract in contracts():
        if contract != None:
            sys.stdout.write(json.dumps(contract) + '\n')
