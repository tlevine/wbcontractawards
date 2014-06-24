import re

from lxml.html import fromstring

def search(response):
    html = fromstring(response.text)
    html.make_links_absolute(response.url)
    return map(str, html.xpath("//ol[@id='search-results']/li/h3/a/@href"))

def prc_notice(response):
    html = fromstring(re.sub(r'<', '\n<', response.text, flags = re.IGNORECASE))
    return html.xpath('//div[@class="prc_notice"]')[0].text_content().strip()

def bidders(prc_notice_text):
    bidder = None
    for line in prc_notice_text.split('\n'):
        m = re.match(r'(awarded|evaluated|rejected).*bidder', line, flags = re.IGNORECASE)
        if m:
            if bidder != None:
                yield bidder
            bidder = {'status': m.group(1)}
        elif bidder != None:
            m = re.match(r'( *[^:]+ *):( *[^:]+ *)', line)
            if m:
                bidder[m.group(1).lower()] = m.group(2).strip()
    if bidder != None:
        yield bidder

def clean_bidder(bidder):
    remap = { 'opening': 'opening.price.raw', 'name': 'bidder.name',
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
    prc = prc_notice(response)
    row = {
        'url': response.url,
        'bids': list(map(clean_bidder, bidders(prc))),
    }
    row.update(methods(prc))

def methods(prc):
    procure = re.compile(r'^method.*procurement: (.+)$', flags = re.IGNORECASE)
    select =  re.compile(r'^method.*selection: (.+)$', flags = re.IGNORECASE)
    out = {}
    for line in prc.split('\n'):
        m = re.match(procure, line)
        if m:
            out['method.procurement'] = m.group(1)
        m = re.match(select, line)
        if m:
            out['method.selection'] = m.group(1)
    return out
