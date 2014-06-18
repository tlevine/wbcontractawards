import sys, json
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
            try:
                yield p.contract(response)
            except:
                sys.stderr.write('Error at %s\n' % url)
                raise

def cli():
    for contract in contracts():
        if contract != None:
            sys.stdout.write(json.dumps(contract) + '\n')
