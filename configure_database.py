import os
import json
from bson.objectid import ObjectId
from pathlib import Path
from dotenv import load_dotenv
from flask_pymongo import pymongo

BASE_DIR = Path(__file__).resolve(strict=True).parent
ENV_FILE = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE, verbose=True)
else:
    exit(0)


def convert_oid(data):
    for document in data:
        document['_id'] = ObjectId(document['_id']['$oid'])
        if 'author_id' in document:
            document['author_id'] = ObjectId(document['author_id']['$oid'])
        if 'comments' in document:
            for comment in document['comments']:
                comment['author'] = ObjectId(comment['author']['$oid'])
    return data


# create mongo client
client = pymongo.MongoClient(os.getenv('MONGODB_KEY'))

# create database
db = client[str(os.getenv('MONGODB'))]

# load data from json files
with open('data/article.json') as f1:
    data1 = json.load(f1)
    data1 = convert_oid(data1)

with open('data/user.json') as f2:
    data2 = json.load(f2)
    data2 = convert_oid(data2)

# create collections and insert data
collection1 = db['article']
collection1.insert_many(data1)

collection2 = db['user']
collection2.insert_many(data2)
