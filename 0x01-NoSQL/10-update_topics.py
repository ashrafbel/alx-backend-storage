#!/usr/bin/env python3
"task 10"


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school document based on the name.

    Args:
        mongo_collection: The pymongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics to set in the school document.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
