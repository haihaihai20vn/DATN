from itertools import product
from datetime import datetime
import argparse
from collections import namedtuple

Param = namedtuple('Param', 'block idx')
pool = (
    "yzewevmeywreomvi"
    "ekwyavygontowaer"
    "udsoyrexvuamtyse"
    "weesuvizpituiqow"
    "uzoretzemuultiaz"
    "icukoqiwolxuykos"
    "upwiymitisneroxe"
    "yxanlekyixxirasi"
    "asxoapuxqaohezwo"
    "oxdigyquziutpave"
    "zohexyvyguqyqidy"
    "ovynumunuwsusyen"
    "xaatyvusivaripfy"
    "oftesaysozuregin"
    "alifkazaadytwuub"
    "zuvoothymivazy"
)

pool +=(10*19*2 - len(pool))*"?"

def dga(date):
    seed = date.strftime("%m%Y")
    params = [
        Param(19, 0),
        Param(19, 1),
        Param(4, 4),
        Param(4, 5)
    ]

    ranges = []
    for p in params:
        s = int(seed[p.idx])
        lower = p.block*s
        upper = lower + p.block
        ranges.append(list(range(lower, upper)))

    domains = set()
    for indices in product(*ranges):
        domain = ""
        for index in indices:
            domain += pool[index*2:index*2 + 2]
        domain += ".bazar"
        domains.add(domain)

    return domains



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--date", help="date used for seeding, e.g., 2020-06-28",
        default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    d = datetime.strptime(args.date, "%Y-%m-%d")
    for domain in dga(d):
        print(domain)
