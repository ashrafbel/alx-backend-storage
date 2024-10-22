#!/usr/bin/env python3
"module for task 8"


def list_all(mongo_collection):
    "desplay all documents in collection"
    return list(mongo_collection.find())
