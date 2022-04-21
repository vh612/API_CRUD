#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# getListCollection.py
#######################

from pymongo import MongoClient

DB_user = os.environ['HOME'].split("/")[-1]

client = MongoClient('localhost:27017')

mydb = client[DB_user]

print(mydb.list_collection_names())
