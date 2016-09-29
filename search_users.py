#!/usr/bin/env python

import requests, json, itertools, math, tqdm
import pymongo

def search(q):
    url = "https://api.github.com/search/users"
    params = {
        "q": str(q),
        "page": 1,
        "per_page": 30,
        "access_token": "1d90e32a44098512ae8936772d8e38feeebb02da"
    }
    first = requests.get(url, params=params)
    body = first.json()
    if first.status_code != 200:
        raise Error("error: " + body.get("message", ""))

    for item in body["items"]:
        yield item
    total = body["total_count"]
    per_page = params["per_page"]
    n_pages = int(math.ceil(float(total)/per_page))

    for page in range(2, n_pages + 1):
        params["page"] = page
        response = requests.get(url, params=params)
        body = response.json()
        if response.status_code != 200:
            raise Error("error: " + body.get("message", ""))
        for item in body["items"]:
            yield item

qs = ["location:vit", "location:vellore"]

with pymongo.MongoClient("localhost", 27017) as client:
    db = client.get_database("github")
    users = db.get_collection("users")
    users.create_index(keys=[("login", pymongo.ASCENDING)], unique=True)

    for q in qs:
        for item in tqdm.tqdm(search(q)):
            try:
                users.insert_one(item)
            except pymongo.errors.DuplicateKeyError:
                pass

    print (users.count())

    
