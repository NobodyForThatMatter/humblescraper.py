#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


#TODO Make some pprint and get rid of JSON dump.
#TODO Maybe check for time until bundle finishes, to grab new bundles on the go?

def get_bundle_links():
    options = Options()
    options.add_argument("--headless")
    list_of_urls = []
    browser = webdriver.Firefox(firefox_options=options)
    browser.get("https://humblebundle.com")
    button = browser.find_element_by_class_name("button-title")
    button.click()
    bundle_wrapper = browser.find_element_by_class_name("bundle-dropdown-content-wrapper")
    bundles = bundle_wrapper.find_elements_by_class_name("more-details")
    for bundle in bundles:
        link = bundle.get_property("href")
        if link not in list_of_urls:
            list_of_urls.append(link)
    return list_of_urls


# Parse Bundles from list of urls (By now single url, the idea would be to make get_bundles function that returns a list of bundles, then parse all the urls in the list. Should add a level to the nested dict so that it gets the bundle name, the tiers and the products. Also, getting ordering okay would be amazing.)


def parse_bundles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tiers = soup.select(".dd-game-row")
    bundle_name = soup.title.string
    tier_list=[bundle_name]
    for tier in tiers:
        if tier.select(".dd-header-headline"):
            tiername = tier.select(".dd-header-headline")[0].text.strip()
            products = tier.select(".dd-image-box-caption")
            productnames = [prodname.text.strip() for prodname in products]
            # tier_dict[tiername] = {"products": productnames}
            tier_list.append({"Tier": tiername, "Products": productnames})
    # return tier_dict
    return tier_list

def main():
    for bundle in get_bundle_links():
        info = parse_bundles(bundle)
        dump = json.dumps(info, indent=1, ensure_ascii=False)
        print(dump)

if __name__== "__main__":
    main()

