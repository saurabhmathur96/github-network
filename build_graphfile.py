#!/usr/bin/env python

import requests, json, itertools, math, tqdm
import pymongo


with pymongo.MongoClient("localhost", 27017) as client:
    db = client.get_database("github")
    users = db.get_collection("users")
    users.fin
    connections = list(users.find(projection=["login", "connections", "repos"]))
    nodes = list()
    login_to_group = dict()
    for i, connection in enumerate(connections):
        login_to_group[connection["login"]] = i
        nodes.append({ "group": i, "login": connection["login"], "connections": connection.get("connections", []),  "weight": len(repos) })

    links = list()
    for source in connections:
        if "connections" in source:
            for target in source.get("connections", []):
                links.append({ "source": login_to_group[source["login"]], "target": login_to_group[target], "weight": 1 })
        

    with open("graphFile.json", "w") as f:
        json.dump({ "nodes": nodes, "links": links }, f)
    