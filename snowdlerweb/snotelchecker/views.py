from collections import defaultdict
import os

from django.shortcuts import render

from . import snotel_tools
from .models import Site
# Create your views here.


def prep_site(site):
    site_dict = {}
    site_dict["code"] = snotel_tools.build_id(site)
    site_dict["state"] = site["state"]
    site_dict["name"] = site["site_name"]
    site_dict["lat"] = site["lat"]
    site_dict["lon"] = site["lon"]
    site_dict["county"] = site["county"]
    site_dict["selected"] = False
    return site_dict

def update_sites(filepath=None):
    sites = snotel_tools.scrape_snotel_sites(filepath)
    for s in sites:
        site_dict = prep_site(s)
        site_model, created = Site.objects.get_or_create(**site_dict)

def setup(request):
    sites = Site.objects.all()
    sites_by_state = defaultdict(list)
    for site in sites:
        sites_by_state[site.state].append(site)
    # must cast back to dict or it breaks use by django template
    context = {"sites_by_state": sorted(sites_by_state.items())}
    return render(request, 'snotelchecker.html', context)

def index(request):
    pass