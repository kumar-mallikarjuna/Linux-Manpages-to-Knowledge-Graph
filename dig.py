import sys
from bs4 import BeautifulSoup as BeautifulSoup
from collections import defaultdict
from pprint import pprint
import sys

html = ""

with open(sys.argv[1]) as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

final = {}
#count = 0

def foo(count, s):
    if(count == 6):
        return s

    d = defaultdict(str)
    key = ""
    try:
        for a in BeautifulSoup(s, "html.parser").find("h%d" % count).next_siblings:
            if(a.name == "h%d" % count):
                key = a.text
                continue

            d[key] += str(a)
    except Exception as e:
        return foo(count+1, s)

    d_ = {}

    for k, v in d.items():
        d_[k] = foo(count+1, v)

    if (len(d_) > 0):
        return d_

    return {}

final.update(foo(1, html))

with open("./out.txt", "w") as f:
    pprint(final, f)
