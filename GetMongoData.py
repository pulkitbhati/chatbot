import configparser
import json
import logging

import StringBuilder as StringBuilder
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
parser = configparser.ConfigParser()
parser.read('config.ini')
host = parser['dbconfigs']['MONGO_HOST']
port = parser['dbconfigs']['MONGO_PORT']
username = parser['dbconfigs']['MONGO_USER']
password = parser['dbconfigs']['MONGO_PASS']
db = parser['dbconfigs']['MONGO_DB']


connection = MongoClient(host, int(port))
db = connection[db]
db.authenticate(username, password)

mongoDB = db.get_collection('test')
data_file=mongoDB.find({}, {'_id': False})
list_cur = list(data_file)

intents = json.dumps(list_cur[0])
intents2 = json.loads(intents)




def updateQuestions(tag,question):
    global oldPattern
    global tagNew
    logging.info('Inside update questions method')
    print("Question is : ", question)
    global pipeline
    pipeline = [
        {
            u"$project": {
                u"_id": 0.0
            }
        },
        {
            u"$unwind": {
                u"path": u"$intents"
            }
        }
    ]
    pipeline.append({
        u"$match": {
            u"intents.tag": tag
        }
    })
    print("Pipeline is : " , pipeline)
    try:
        print("Final response is below : ")
        cursor = mongoDB.aggregate(
            pipeline,
            allowDiskUse = False
        )
        tagNew=tag
        for doc in cursor:
            oldPattern = doc['intents']['patterns']
            oldPattern.append(question);
            print("Older Pattern is : " , doc['intents']['patterns'])
            mongoDB.update_one({'intents.tag':tagNew},{"$set":{'intents.$.patterns': oldPattern}})
    finally:
        print("query executed")

