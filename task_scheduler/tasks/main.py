from db_task import DbTask
from config_objects import ConfigDbTask
from pymongo import MongoClient
from redis import Redis
from pprint import pprint
from abstract_db_connector import MongoDbConnection

mongo_client = MongoDbConnection(
                        db_name="dbtest1", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27017)


config1 = ConfigDbTask(query={},db_connection=mongo_client)

data = {
   "stock": "Brent Crude Futures",
   "qty": 250,
   "type": "buy-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

db_task = DbTask(priority=0, config=config1)

db_task.config.db_connection.insert(data)


# db_task.config.db_connection.get()
# mongo_client2 = MongoDbConnection(None,None,None,None,None)