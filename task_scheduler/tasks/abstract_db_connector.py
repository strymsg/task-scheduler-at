from abc import abstractmethod
from pymongo import MongoClient
from redis import Redis
from pymongo.errors import AutoReconnect, ConnectionFailure, ConfigurationError, OperationFailure

class AbstractDbConnector:
    def __init__(
            self, 
            db_name:str, 
            db_host:str, 
            username:str,
            password:str, 
            port:int):

        self.db_name = db_name
        self.db_host = db_host
        self.username = username
        self.password = password
        self.port = port

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def insert(self, params):
        pass

    @abstractmethod
    def delete(self, params):
        pass

    @abstractmethod
    def update(self, params):
        pass


class MongoDbConnection(AbstractDbConnector):

    __instance__ = None

    def __init__(
            self, 
            db_name:str, 
            db_host:str, 
            username:str,
            password:str, 
            port:int):
        """ Constructor.
        """
        super().__init__(db_name, db_host, username, password, port)

        if MongoDbConnection.__instance__ is None:
            MongoDbConnection.__instance__ = self
            self.client = MongoClient(
                        host=self.db_host, 
                        port=self.port, 
                        username=self.username,
                        password=self.password)
            try:
                self.client.admin.command('ismaster')
            except ConnectionFailure as err:
                return("Connection Failure") #Testing
            # finally:
            #     self.client.close()
            return "Connection establish" #Testing
        else:
            raise Exception("You can't create another MongoDbConnection class")

    @staticmethod
    def get_connection():
        """ Static method to fetch the current instance.
        """
        if not MongoDbConnection.__instance__:
            MongoDbConnection()
        return MongoDbConnection.__instance__    
    
    def insert(self, params):
        try:
            if self.client[self.db_name].collection1.count_documents(params, limit = 1):
                print("This document already has this data")
            else: 
                self.client[self.db_name].collection1.insert_many([params])
        except ConnectionFailure as err:
            # return(err)
            return "Connection failure" #Testing

    def get(self, criteria):
        try:
            return self.client[self.db_name].collection1.find(criteria)
        except ConnectionFailure as err:
            # return(err)
            return "Connection failure" #Testing
    def delete(self, criteria):
        try:
            self.client[self.db_name].collection1.delete_one(criteria) 
        except ConnectionFailure as err:
            # return(err)
            return "Connection failure" #Testing
    def update(self, criteria, params):
        try:
            self.client[self.db_name].collection1.update_one(criteria, params) 
        except ConnectionFailure as err:
            # return(err)
            return "Connection failure" #Testing



class RedisDbConnection(AbstractDbConnector):

    __instance__ = None

    def __init__(
            self, 
            db_name:str, 
            db_host:str, 
            username:str,
            password:str, 
            port:int):
        """ Constructor.
        """
        super().__init__(db_name, db_host, username, password, port)

        if RedisDbConnection.__instance__ is None:
            RedisDbConnection.__instance__ = self
            self.client = Redis(
                        host=self.db_host, 
                        port=self.port, 
                        username=self.username,
                        password=self.password)
            try:
                self.client.admin.command('ismaster')
            except ConnectionFailure as err:
                print("Connection Failure")
        else:
            raise Exception("You can't create another RedisDbConnection class")

    @staticmethod
    def get_connection():
        """ Static method to fetch the current instance.
        """
        if not RedisDbConnection.__instance__:
            RedisDbConnection()
        return RedisDbConnection.__instance__    
    
    def insert(self, params):
        # TODO: implement insert method to the dbs
        pass
    
    def delete(self, params):
        # TODO: implement insert method to the dbs
        pass
    
    def update(self, params):
        # TODO: implement insert method to the dbs
        pass      