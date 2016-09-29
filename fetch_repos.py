#!/usr/bin/env python

import requests, json, itertools, math, tqdm
import pymongo


with pymongo.MongoClient("localhost", 27017) as client:
    db = client.get_database("github")
    users = db.get_collection("users")
    people = list(users.find({}, ["login", "repos_url"]))

    params = {
        "access_token": "1d90e32a44098512ae8936772d8e38feeebb02da"
    }

    for person in tqdm.tqdm(people):
        repos = requests.get(person["repos_url"], params=params).json()
        users.update_one({ "login": person["login"] }, { "$set": { "repos": list(repos) } })