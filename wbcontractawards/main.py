import argparse
import sys
import csv
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

def bids():
    for contract in contracts():
        if contract != None:
            for bid in contract['bids']:
                bid.update(contract)
                yield bid

def contract_splits():
    for contract in contracts():
        contract['n.bids'] = len(contract['bids'])
        del(contract['bids'])
        yield contract

parser = argparse.ArgumentParser('Get data about contracts for projects funded by the World Bank.')
parser.add_argument(dest = 'unit', metavar = '[unit]', choices = ['bids', 'contracts'])

def cli():
    emit(sys.stdout, parser.parse_args().unit)

def emit(stdout, unit):
    fieldnames = {
        'bids': ['project','contract','bidder','status','amount','currency'],
        'contracts': [
            'project', 'contract',
            'method.procurement', 'method.selection',
            'price.amount', 'price.currency',
            'n.bids',
        ],
    }
    generators = {
        'bids': bids,
        'contracts': contract_splits,
    }
    writer = csv.DictWriter(stdout, fieldnames = fieldnames[unit])
    writer.writeheader()
    for row in generators[unit]():
        writer.writerow(row)
