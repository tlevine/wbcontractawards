from lxml.html import fromstring
import pyparsing as p


def search(response):
    html = fromstring(response.text)
    html.make_links_absolute(response.url)
    return map(str, html.xpath("//ol[@id='search-results']/li/h3/a/@href"))

def _contract_parser():
    status = p.oneOf(['awarded','evaluated','rejected'], caseless = True)
    bidder = p.Suppress(p.CaselessLiteral('bidder'))
    to_newline = p.SkipTo(p.oneOf(['\n','<','\r']))
    name = p.Suppress(p.SkipTo(p.Word('Name'))) + p.Suppress(p.Word('Name: ')) + to_newline
    parser = p.Suppress(p.SkipTo(status)) + status + bidder + name
    return p.ZeroOrMore(parser)

def contract(response):
    html = fromstring(response.text)
    text = html.xpath('//div[@class="prc_notice"]')[0].text_content()
    parser = _contract_parser()
    matches = parser.parseString(response.text)
    if len(matches) > 0:
        return [{'status':status, 'name': name} for status, name in zip(matches[0::2], matches[1::2])]
