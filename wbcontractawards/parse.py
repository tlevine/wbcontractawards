import re

from lxml.html import fromstring
import pyparsing as p

def search(response):
    html = fromstring(response.text)
    html.make_links_absolute(response.url)
    return map(str, html.xpath("//ol[@id='search-results']/li/h3/a/@href"))

def bidders(response):
    html = fromstring(re.sub(r'<', '\n<', response.text, flags = re.IGNORECASE))
    text = html.xpath('//div[@class="prc_notice"]')[0].text_content().strip()
    bidder = None
    for line in text.split('\n'):
        if re.search(r'bidder', line, flags = re.IGNORECASE):
            if bidder != None:
                yield bidder
            bidder = {'status': re.match(r'^([a-z]+) ', line, flags = re.IGNORECASE).group(1)}
        elif bidder != None:
            m = re.match(r'( *[^:]+ *):( *[^:]+ *)', line)
            if m:
                bidder[m.group(1).lower()] = m.group(2)

def clean_bidder(bidder):
    remap = { 'opening': 'opening.price.raw', 'name': 'company.name',
              'status': 'status', 'country': 'country', }
    out = {}
    for key, value in bidder.items():
        for old, new in remap.items():
            if old in key:
                out[new] = value
                break
    out['opening.price.currency'], out['opening.price.amount'] = money(out.get('opening.price.raw',''))
    return out

def money(raw):
    'If there are multiple amounts in different currencies, take the first one.'
    match = re.match(r'^[^A-Z]*([A-Z]{3})[^0-9]*([0-9,]+)[^0-9,]*', raw)
    if match:
        currency = match.group(1)
        amount = float(match.group(2).replace(',',''))
    else:
        currency = amount = None
    return currency, amount

def contract(response):
    return list(map(p.clean_bidder, p.bidders(response)))
