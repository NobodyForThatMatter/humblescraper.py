#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

#TODO Maybe scrape the bundle pages using the bundleVars JASON, but seems to be more convoluted than just getting elements by id there.

#TODO Add write-to-file mode/option, sleep, check the file, if no new content found keep old file, else change content and send email.

def get_json_from_api(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'lxml')
    json_raw = soup.find('script', id='webpack-json-data').text # Site-wide data, found both in main url and bundle urls.
    json_loaded = json.loads(json_raw)
    return json_loaded


def get_bundle_links_and_end():
    list_of_bundles=[]
    products = get_json_from_api("http://humblebundle.com")

    for product in products["productTiles"][1:]: # Index 0 is monthly.
        bundle_url="http://humblebundle.com/"+product["url"] # product_url adds a slash at the start, url doesn't.
        list_of_bundles.append({"url": bundle_url, "end": product["tab_end"]})

    return list_of_bundles


def parse_bundles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tiers = soup.select(".dd-game-row")
    bundle_name = soup.title.string
    tier_list=[]
    for tier in tiers:
        if tier.select(".dd-header-headline"):
            tiername = tier.select(".dd-header-headline")[0].text.strip()
            products = tier.select(".dd-image-box-caption")
            productnames = [prodname.text.strip() for prodname in products]
            tier_list.append({"Tier": tiername, "Products": productnames})
    return tier_list, bundle_name

def print_it(tier_list, name, bundle_end):
    print("\nBUNDLE: ", name)
    print("\nBUNDLE ENDS: ", bundle_end)
    for i in tier_list:
        print("\n")
        print("-"*75)
        print("\tTier: ", i["Tier"])
        print("="*75)
        print("\n")
        print("\tProducts: ")
        for product in i["Products"]:
            print("\t\t", product)
        print("\n")

def main():
    for bundle in get_bundle_links_and_end():
        bundle_end = bundle["end"]
        info, name = parse_bundles(bundle["url"])
        print("*"*75)
        print_it(info,name,bundle_end)
        print("*"*75)

if __name__ == '__main__':
    main()
