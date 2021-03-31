from pymongo import MongoClient
import utils  # General utils including config params and database connection
import configparser

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

for doc in db.get_collection("movie").find():
    print(doc['name'])
