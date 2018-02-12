#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
tier_list = []
# tier_dict = {}
test_url = "https://www.humblebundle.com/books/mobile-app-development-books"

# Parse Bundles from list of urls (By now single url, the idea would be to make get_bundles function that returns a list of bundles, then parse all the urls in the list. Should add a level to the nested dict so that it gets the bundle name, the tiers and the products. Also, getting ordering okay would be amazing.)


def parse_bundles(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    bundleName = soup.title.string

    tiers = soup.select(".dd-game-row")

    for tier in tiers:
        if tier.select(".dd-header-headline"):
            tiername = tier.select(".dd-header-headline")[0].text.strip()
            products = tier.select(".dd-image-box-caption")
            productnames = [prodname.text.strip() for prodname in products]
           # tier_dict[tiername] = {"products": productnames}
            tier_list.append({"Tier": tiername, "Products": productnames})
    # return tier_dict
    return tier_list


print(json.dumps(parse_bundles(test_url), indent=1,
                 ensure_ascii=False))
