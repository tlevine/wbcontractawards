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
        

def cli(unit):
    writer = csv.writer(sys.stdout)

    if unit == 'bids':
        writer.writerow(['project','contract','bidder','status','amount','currency'])
        for bid in bidders():
            row = [
                bid.get('project'),
                bid['url'],
                bid.get('bidder.name'),
                bid.get('status'),
                bid.get('opening.price.amount'),
                bid.get('opening.price.currency'),
            ]
            writer.writerow(row)
    elif unit == 'contracts':
        writer.writerow(['project','contract',])
        for contract in contract_splits():
            row = [
                contract.get('project'),
                contract['url'],
            ]
            writer.writerow(row)
