import logging
import os
import re
from robobrowser import RoboBrowser

logger = logging.getLogger(__name__)

id_re = re.compile("\(([^)]+)\)")

def scrape_snotel_sites(url=None):
    if not url:
        url = "http://www.wcc.nrcs.usda.gov/nwcc/yearcount?network=sntl&counttype=statelist&state="
    browser = RoboBrowser(parser="html5lib")
    browser.open(url)
    browser.response.raise_for_status()
    table = browser.find_all("table")[4]
    sites = [] # list of sites with name and code
    cols = [t.text.strip() for t in table.tr.find_all("th")]
    for row in table.find_all("tr"):
        if row.td and row.td.text.strip() == 'SNTL':
            items = [i.text.strip() for i in row.find_all("td")]
            sites.append(dict(zip(cols, items)))
    return sites

def build_id(listing):
    number = id_re.findall(listing["site_name"])[0]
    state = listing["state"]
    return "{}:{}:{}".format(number, state, "SNTL")

