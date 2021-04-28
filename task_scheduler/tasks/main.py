from task_scheduler.tasks.db_task import DbTask
from task_scheduler.tasks.config_objects import ConfigDbTask
from pymongo import MongoClient
from redis import Redis
from pprint import pprint
from task_scheduler.tasks.abstract_db_connector import MongoDbConnection, RedisDbConnection
import json

data = {
   "stock": "Brent Crude Futures",
   "qty": 250,
   "type": "sell-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

data1 = {
   "stock": "Brent Crude Futures",
   "qty": 5555,
   "type": "buy-limit"
   }

data2 = {
   "stock": "Brent Crude Futures",
   "qty": 6666,
   "type": "buy-limit"
   }

data3 = {
   "stock": "Brent Crude Futures",
   "qty": 7777,
   "type": "buy-limit"
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

print(db_task.config.db_connection.insert("config-task",data1))
print(db_task.config.db_connection.insert("config-task",data2))
print(db_task.config.db_connection.insert("config-task",data3))
print(db_task.config.db_connection.insert("config-task",data))

print(db_task.config.db_connection.get("config-task",{"type": {"$eq":"buy-limit"}}))

print(db_task.config.db_connection.delete("config-task",{"type": {"$eq":"buy-limit"}}))

print(db_task.config.db_connection.get("config-task",{"type": {"$eq":"buy-limit"}}))

print(db_task.config.db_connection.update("config-task", {"type": {"$eq":"sell-limit"}}, {"$set":{"limit":1}}))

mongo_client_2 = MongoDbConnection(db_name="dbtest2", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27017)
mongo_client_2.connect()
config2 = ConfigDbTask(query={},db_connection=mongo_client_2)
db_task2 = DbTask(priority=0, config=config2)
print(db_task2.config.db_connection.insert("api-task",data))

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

# print(db_task.config.db_connection.insert(data, "config-1"))

# print(db_task.config.db_connection.insert(data1, "config-2"))

# print(db_task.config.db_connection.insert(data2, "config-3"))

# print(db_task.config.db_connection.insert(data3, "api-1"))

# print(db_task.config.db_connection.get("config-*"))

# print(db_task.config.db_connection.delete("config-*"))

# print(db_task.config.db_connection.get("*"))

# redis_client2 = RedisDbConnection(
#                         db_name="1", 
#                         db_host="localhost", 
#                         username=None, 
#                         password=None, 
#                         port=6379)
# redis_client2.connect()