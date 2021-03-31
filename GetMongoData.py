import configparser
import json
from pymongo import MongoClient

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
