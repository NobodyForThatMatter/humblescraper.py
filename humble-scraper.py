#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import filecmp
from bs4 import BeautifulSoup
import json
import argparse

#TODO Maybe scrape the bundle pages using the bundleVars JSON, but seems to be more convoluted than just getting elements by id there.

#TODO Sleep, check the file, if no new content found keep old file, else change content and send email. Add argparse functionality (daemon/writer  mode).

def update_it(file_old, file_new):
    #files_equal = False
    files_equal = filecmp.cmp(file_old, file_new, shallow=True)
    with open(file_old, "w+") as bundles_old, open(file_new, "r") as bundles_new:
        new_content = bundles_new.read()
        if files_equal:
            print("The bundles are the same than the last time this program was run. No changes are to be made.")
        else:
            print("There are different bundles than last time. Writing...")
            bundles_old.write(new_content)

            print("All ok.")

def clear_it():
    with open ("bundles_new.txt", "w") as file:
        file.write("")

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

def write_it(file, tier_list, name, bundle_end):

    file.write("\nBUNDLE: "+ name)
    file.write("\nBUNDLE ENDS: " + bundle_end)
    for i in tier_list:
        file.write("\n")
        file.write("-"*75+"\n")
        file.write("\tTier: " + i["Tier"] + "\n")
        file.write("="*75 + "\n")
        file.write("\n")
        file.write("\tProducts: "+"\n")
        for product in i["Products"]:
            file.write("\t\t" + product + "\n")


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
        print("*"*75+"\n")
        print_it(info,name,bundle_end)
        print("*"*75+"\n")

        with open('bundles_new.txt', 'a') as file:
            file.write("*"*75+"\n"*5)
            write_it(file, info, name, bundle_end)
            file.write("*"*75)
            file.write("\n"*5)

    update_it("bundles_old.txt", "bundles_new.txt")
    clear_it()


if __name__ == '__main__':
    main()
