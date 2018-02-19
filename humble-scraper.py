#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


#TODO Program Python to execute this script when time to finish the bundle is up.

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
    browser.quit()
    return list_of_urls

def get_timer(url):
    options = Options()
    options.add_argument("--headless")
    timer = []
    time_left=[]
    browser = webdriver.Firefox(firefox_options=options)
    browser.get(url)
    countdown = browser.find_elements_by_class_name("redesign-purchase-digit")
    labels = browser.find_elements_by_tag_name("label")

    for element, label in zip(countdown, labels):
        timer.append(element.text+' '+label.text)
        time_left.append(element)
    browser.quit()
    return timer

def parse_bundles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tiers = soup.select(".dd-game-row")
    bundle_name = soup.title.string
    tier_list=[]
    timer = get_timer(url)
    time_left=", ".join(timer)
    for tier in tiers:
        if tier.select(".dd-header-headline"):
            tiername = tier.select(".dd-header-headline")[0].text.strip()
            products = tier.select(".dd-image-box-caption")
            productnames = [prodname.text.strip() for prodname in products]
            tier_list.append({"Tier": tiername, "Products": productnames})
    return tier_list, bundle_name, time_left

def print_it(tier_list, name, time_left):
    print("\nBUNDLE: ", name)
    print("\nTIME LEFT: ", time_left)
    for i in tier_list:
        print("\n")
        print("-"*50)
        print("\tTier: ", i["Tier"])
        print("="*50)
        print("\n")
        print("\tProducts: ")
        for product in i["Products"]:
            print("\t\t", product)
        print("\n")

def main():
    for bundle in get_bundle_links():
        info, name, timer = parse_bundles(bundle)
        print("*"*50)
        print_it(info, name, timer)
        print("*"*50)

if __name__ == '__main__':
    main()

