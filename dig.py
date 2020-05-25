import re
from bs4 import BeautifulSoup as BeautifulSoup
from collections import defaultdict


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
        heading = BeautifulSoup(s, "html.parser").find("h%d" % count)

        if heading is None:
            return self.structure(count+1, s)
        else:
            while heading is not None:
                if(heading.name == "h%d" % count):
                    key = re.sub(r"\s+", " ", heading.text)
                else:
                    d[key] += str(heading)
                heading = heading.next_sibling

        d_ = {}

        for k, v in d.items():
            x = self.structure(count+1, v)
            if x:
                d_[k] = self.structure(count+1, v)

        if (len(d_) > 0):
            return d_

        return {}
