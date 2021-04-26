from db_task import DbTask
from config_objects import ConfigDbTask
from pymongo import MongoClient
from redis import Redis
from pprint import pprint
from abstract_db_connector import MongoDbConnection
from abstract_db_connector import RedisDbConnection
import json

data = {
   "stock": "Brent Crude Futures",
   "qty": 250,
   "type": "buy-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

# Connection and queries to MongoDB:

mongo_client = MongoDbConnection(
                        db_name="dbtest1", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27017)

mongo_client.connect()
config1 = ConfigDbTask(query={},db_connection=mongo_client)
db_task = DbTask(priority=0, config=config1)

print(db_task.config.db_connection.insert(data))

print(db_task.config.db_connection.get({"limit": {"$eq":48.90}}))
# print(db_task.config.db_connection.delete({"limit": 48.90}))
print(db_task.config.db_connection.update({"limit": {"$eq":48.90}}, {"$set":{"limit":80}}))

mongo_client_2 = MongoDbConnection(db_name="dbtest2", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27017)
mongo_client_2.connect()
config2 = ConfigDbTask(query={},db_connection=mongo_client_2)
db_task2 = DbTask(priority=0, config=config2)
print(db_task2.config.db_connection.insert(data))

mongo_client4 = MongoDbConnection(
                        db_name="dbtest1", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27017)

# ------------------------------------------------------------

# Connection and queries to RedisDB:
# 
# redis_client = RedisDbConnection(
#                         db_name="0", 
#                         db_host="localhost", 
#                         username=None, 
#                         password=None, 
#                         port=6379)

# redis_client.connect()
# config1 = ConfigDbTask(query={},db_connection=redis_client)
# db_task = DbTask(priority=0, config=config1)

# r = db_task.config.db_connection.insert(data, "DATA1")
# print(r)
# r = db_task.config.db_connection.get("DATA1")
# print(r)
# r = db_task.config.db_connection.delete("DATA1")
# print(r)

# redis_client2 = RedisDbConnection(
#                         db_name="1", 
#                         db_host="localhost", 
#                         username=None, 
#                         password=None, 
#                         port=6379)
# redis_client2.connect()