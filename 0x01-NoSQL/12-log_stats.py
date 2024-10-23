#!/usr/bin/env python3
'''Script that provides stats about Nginx logs stored in MongoDB.
'''

from pymongo import MongoClient


def log_stats():
    '''Displays stats about Nginx logs in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    mongo_collection = client.logs.nginx
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for m in methods:
        count = mongo_collection.count_documents({"method": m})
        print(f"\tmethod {m}: {count}")
    status_check_count = mongo_collection.count_documents({
        "method": "GET",
        "path": "/status"
        })
    print(status_check_count, "status check")


if __name__ == "__main__":
    log_stats()
