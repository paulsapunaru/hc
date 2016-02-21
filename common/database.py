import json
import os

import pymongo

__db = pymongo.MongoClient("localhost", 27017).get_database("hc")
__collection = __db.get_collection("items")

# This index is for simple searches, without keyword
__collection.create_index([("subreddit", pymongo.ASCENDING),
                           ("created_utc", pymongo.DESCENDING)])
# This index is for complex searches, which also include the keyword
# The language is "none" because we don't want a true text search with stemming
# and stop words removal. Instead, a search based on simple tokenization will be
# used.
__collection.create_index([("title", pymongo.TEXT),
                           ("text", pymongo.TEXT),
                           ("body", pymongo.TEXT),
                           ("subreddit", pymongo.ASCENDING),
                           ("created_utc", pymongo.DESCENDING)],
                          default_language="none",
                          background=True)


def insert(obj):
    return __collection.insert_one(obj).inserted_id


def find(subreddit, from_, to, keyword=None):
    # Make sure we lowercase the subreddit parameter in the query
    query = {"subreddit": subreddit.lower(),
             "created_utc": {"$gte": from_, "$lte": to}}
    # Use the $text operator when searching for a specific keyword
    if not (keyword is None):
        query["$text"] = {"$search": keyword}

    items = []
    for found in __collection.find(query, {"_id": False}) \
            .sort("created_utc", pymongo.DESCENDING):
        items.append(found)

    return items
