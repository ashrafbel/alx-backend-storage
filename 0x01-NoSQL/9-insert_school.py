#!/usr/bin/env python3
"task 9"


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into the specified collection.

    Parameters:
        mongo_collection: The collection object from pymongo.
        **kwargs: Key-value pairs for document attributes.

    Returns:
        The _id of the newly created document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
