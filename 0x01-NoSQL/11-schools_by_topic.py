#!/usr/bin/env python3
"task 11"


def schools_by_topic(mongo_collection, topic):
    '''Returns the list of schools having a specific topic.
    
    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search for.
        
    Returns:
        list: A list of schools containing the specified topic.
    '''
    topic = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [d for d in mongo_collection.find(topic)]
