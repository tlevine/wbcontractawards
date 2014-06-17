from lxml.html import fromstring

def search(response):
    html = fromstring(response.text)
