#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

#TODO Program Python to execute this script when time to finish the bundle is up.

def get_bundle_links_and_end():
    list_of_bundles=[]
    request = requests.get("http://humblebundle.com")
    mosaic_raw = re.findall('(\[{.+?}]),\n', request.text, re.S)
    mosaic_loaded = json.loads(mosaic_raw[1])
    for element in mosaic_loaded:
        if "products" in element:
            for product in element["products"]:
                if product["type"] == "bundle":
                    bundle_url="http://humblebundle.com"+product["product_url"]
                    list_of_bundles.append({"url": bundle_url, "end": product["end_date"]})
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

