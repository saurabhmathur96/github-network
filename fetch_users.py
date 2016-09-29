#!/usr/bin/env python

import requests, json, tqdm

def get_urls(filename):
    with open(filename) as f:
        data = json.load(f)
        return [each["url"] for each in data]

urls = get_urls("results.json")
print len(urls)

params = {
    "access_token": "1d90e32a44098512ae8936772d8e38feeebb02da"
}
profiles = [requests.get(url).json() for url in tqdm.tqdm(urls)]

with open("users.json", "w") as f:
    json.dump(profiles, f) 