from neo4j import GraphDatabase

import re
import sys
from bs4 import BeautifulSoup as BeautifulSoup
from collections import defaultdict
import sys

class dig():

    def __init__(self, html, session):
        self.final = {}
        self.session = session
        self.title = ''

        self.title = BeautifulSoup(html, "html.parser").title.text
        self.final.update(self.structure(1, html))

    def structure(self, count, s):
        if(count == 6):
            soup = BeautifulSoup(s, "html.parser")
            arr = []
            
            for a in soup.find_all("dl"):
                arr.append({a.dt.text: a.dd.text})

            return arr

        d = defaultdict(str)
        key = ""
        try:
            for a in BeautifulSoup(s, "html.parser").find("h%d" % count).next_siblings:
                if(a.name == "h%d" % count):
                    key = re.sub("\s+", " ", a.text)
                    continue

                d[key] += str(a)
        except Exception as e:
            return self.structure(count+1, s)

        d_ = {}

        for k, v in d.items():
            x = self.structure(count+1, v)
            if x:
                d_[k] = self.structure(count+1, v)

        if (len(d_) > 0):
            return d_

        return {}
