import itertools

from wbcontractawards.download import get, search

def contracts():
    for os in itertools.count(0, 10):
        response = search(os)
        
