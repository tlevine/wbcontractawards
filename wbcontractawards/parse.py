import re

from lxml.html import fromstring
import pyparsing as p

def search(response):
    html = fromstring(response.text)
    html.make_links_absolute(response.url)
    return map(str, html.xpath("//ol[@id='search-results']/li/h3/a/@href"))

def contract(response):
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
